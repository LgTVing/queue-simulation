"""The demo uses the real V5 engine, validates requests and serves local assets."""

import json
import threading
from http.client import HTTPConnection

import pandas as pd
import pytest

import demo


def options(**updates):
    return demo.validate_request({"schedule": [4, 6, 6, 6, 5, 5, 6, 5, 5],
                                  "reps": 30, "compare_baseline": False, **updates})


@pytest.mark.parametrize("updates", [
    {"schedule": [4] * 8}, {"schedule": [0] * 9}, {"schedule": [True] * 9},
    {"demand_percent": float("nan")}, {"demand_percent": 201},
    {"reps": 31}, {"reps": 30.0}, {"seed": -1}, {"compare_baseline": "false"},
])
def test_invalid_demo_inputs(updates):
    with pytest.raises(ValueError):
        options(**updates)


def test_demo_reproduces_frozen_v5():
    """The UI adapter preserves the model, seeds, metrics and hourly SLA rule."""
    result = demo.run_scenario(options(reps=300))
    frozen = pd.read_csv(demo.REFERENCE / "so_sanh_chinh_sach.csv").set_index("chinh_sach").loc["Ben vung (+10% nhu cau)"]
    for key, column in [("sl", "sl_toan_ngay"), ("wait", "wq_phut"),
                        ("abandonment", "ti_le_bo_ve"), ("worst_hour_low", "sl_gio_te_nhat_low")]:
        assert result["summary"][key] == frozen[column]
    assert result["summary"]["feasible"] == all(h["sl_ci95_low"] >= .9 for h in result["hourly"])


def test_baseline_and_demand_options():
    result = demo.run_scenario(options(schedule=[6] * 9, demand_percent=150,
                                       compare_baseline=True, day_variability=True))
    assert result["summary"]["sl"] == result["baseline"]["sl"]
    assert result["hourly"] == result["baseline"]["hourly"]
    assert result["expected_arrivals"] == round(demo.demo_config()["expected_arrivals"] * 1.5)
    assert result["scenario"]["day_variability"] is True


def test_http_routes_and_submission():
    server = demo.ThreadingHTTPServer(("127.0.0.1", 0), demo.DemoHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    conn = HTTPConnection("127.0.0.1", server.server_port, timeout=30)
    try:
        for path, mime in [("/", "text/html"), ("/app.js", "text/javascript"), ("/style.css", "text/css")]:
            conn.request("GET", path)
            response = conn.getresponse()
            assert response.status == 200
            assert response.headers["Content-Type"].startswith(mime)
            assert len(response.read()) > 100
        conn.request("GET", "/api/config")
        response = conn.getresponse()
        config = json.loads(response.read())
        assert len(config["presets"]) == 5
        conn.request("GET", "/../common.py")
        response = conn.getresponse()
        assert response.status == 404
        response.read()
        conn.request("POST", "/api/simulate", json.dumps(options()), {"Content-Type": "application/json"})
        response = conn.getresponse()
        result = json.loads(response.read())
        assert response.status == 200 and len(result["hourly"]) == 9
        conn.request("POST", "/api/simulate", "{}")
        response = conn.getresponse()
        assert response.status == 400 and "error" in json.loads(response.read())
        conn.request("POST", "/api/simulate", "{}", {"Origin": "https://example.com"})
        response = conn.getresponse()
        assert response.status == 403
        response.read()
    finally:
        conn.close()
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
