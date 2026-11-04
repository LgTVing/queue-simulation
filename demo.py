"""Local demo UI. Reuses the V5 model and SimPy engine without writing results."""

import argparse
import dataclasses
import json
import logging
import math
import os
from pathlib import Path
import tempfile
import threading
import time
from functools import lru_cache
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

os.environ.setdefault("QS_WORKERS", "1")
os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "queue-simulation-mpl"))

import a_data
import c_sim
import common

ROOT = Path(__file__).resolve().parent
REFERENCE = ROOT / "results" / "final_v5"
UI = ROOT / "ui"
RUN_LOCK = threading.Lock()
PRESETS = {
    "toi_uu_theo_ca": ("Khuyến nghị · 48 quầy-giờ", "Lịch V5 khuyến nghị: cân bằng chất lượng phục vụ và giờ công."),
    "toi_uu": ("Tiết kiệm · 45 quầy-giờ", "Ít quầy-giờ mở hơn; dễ hụt SLA khi lượng khách tăng."),
    "moc_co_so": ("Cố định · 6 quầy", "Mở 6 quầy trong cả 9 giờ, dùng làm mốc so sánh."),
    "sipp_erlang_c": ("Lý thuyết · Erlang C", "Lịch tính bằng công thức hàng đợi không có khách bỏ về."),
    "sipp_erlang_a": ("Lý thuyết · Erlang-A", "Lịch tính bằng công thức có xét khách bỏ về."),
}


@lru_cache(maxsize=1)
def load_demo():
    """Read frozen inputs only; never estimate again or overwrite V5 artifacts."""
    params = json.loads((REFERENCE / "params.json").read_text(encoding="utf-8"))
    schedules = json.loads((REFERENCE / "lich_khuyen_nghi.json").read_text(encoding="utf-8"))
    train, _ = a_data.split_train_test(a_data.load_log(), train_ratio=0.7)
    model = a_data.build_model(params, a_data.train_service_samples(train))
    return model, params, schedules


def demo_config():
    model, params, schedules = load_demo()
    return {
        "hours": common.H_LABELS,
        "presets": [{"id": key, "label": label, "description": desc, "schedule": schedules[key]}
                    for key, (label, desc) in PRESETS.items()],
        "default_preset": "toi_uu_theo_ca",
        "expected_arrivals": sum(model.rates) * model.hour_len,
        "day_cv": params["day_cv"],
        "target_sla": common.TARGET_SLA,
        "wait_threshold": common.WAIT_THRESHOLD,
    }


def integer(value, label, low, high):
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        raise ValueError(f"{label} phải là số nguyên từ {low} đến {high}.")
    return value


def validate_request(payload):
    if not isinstance(payload, dict):
        raise ValueError("Thiết lập kịch bản không hợp lệ.")
    schedule = payload.get("schedule")
    if not isinstance(schedule, list) or len(schedule) != common.HOURS:
        raise ValueError("Cần nhập đủ số quầy cho 9 khung giờ.")
    schedule = [integer(c, "Số quầy", 1, 12) for c in schedule]
    demand = payload.get("demand_percent", 100)
    if isinstance(demand, bool) or not isinstance(demand, (int, float)) or not math.isfinite(demand) or not 50 <= demand <= 200:
        raise ValueError("Lượng khách phải nằm trong khoảng 50% đến 200%.")
    reps = integer(payload.get("reps", 100), "Số ngày mô phỏng", 30, 300)
    if reps not in (30, 100, 300):
        raise ValueError("Chọn 30, 100 hoặc 300 ngày mô phỏng.")
    seed = integer(payload.get("seed", 50000), "Seed", 0, 2**31 - 1)
    for name in ("day_variability", "compare_baseline"):
        if name in payload and not isinstance(payload[name], bool):
            raise ValueError("Tùy chọn kịch bản không hợp lệ.")
    return dict(schedule=schedule, demand_percent=demand, reps=reps, seed=seed,
                day_variability=payload.get("day_variability", False),
                compare_baseline=payload.get("compare_baseline", True))


def summarize(result, schedule):
    feasible, violated = c_sim.is_schedule_feasible(result)
    worst = min(result["hourly"], key=lambda h: h["sl_ci95_low"])
    return {
        "counter_hours": sum(schedule), "sl": result["sl_mean"],
        "sl_ci": result["sl_ci95"], "wait": result["wq_mean"],
        "wait_ci_half": result["wq_ci_half"], "abandonment": result["p_ab_mean"],
        "abandonment_ci_half": result["p_ab_ci_half"], "vip_sl": result["sl_vip_mean"],
        "utilization": result["util_mean"], "feasible": feasible, "violated_hours": violated,
        "worst_hour": worst["hour"], "worst_hour_low": worst["sl_ci95_low"],
    }


def run_scenario(options):
    started = time.perf_counter()
    model, params, _ = load_demo()
    model = dataclasses.replace(model, rates=[r * options["demand_percent"] / 100 for r in model.rates])
    kwargs = dict(n_reps=options["reps"], seed_base=options["seed"],
                  day_cv=params["day_cv"] if options["day_variability"] else 0.0)
    result = c_sim.run_reps(model, options["schedule"], **kwargs)
    baseline = None
    if options["compare_baseline"]:
        base_schedule = [common.BASELINE_C] * common.HOURS
        base_result = result if options["schedule"] == base_schedule else c_sim.run_reps(model, base_schedule, **kwargs)
        baseline = {**summarize(base_result, base_schedule), "hourly": base_result["hourly"]}
    return {"scenario": options, "summary": summarize(result, options["schedule"]),
            "hourly": result["hourly"], "baseline": baseline,
            "expected_arrivals": round(sum(model.rates) * model.hour_len),
            "elapsed_seconds": round(time.perf_counter() - started, 2)}


class DemoHandler(BaseHTTPRequestHandler):
    def send_content(self, status, data, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; object-src 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, status, data):
        self.send_content(status, json.dumps(data, ensure_ascii=False, allow_nan=False).encode(), "application/json; charset=utf-8")

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/api/config":
            self.send_json(200, demo_config())
            return
        files = {"/": ("index.html", "text/html"), "/app.js": ("app.js", "text/javascript"),
                 "/style.css": ("style.css", "text/css")}
        if path not in files:
            self.send_json(404, {"error": "Không tìm thấy trang."})
            return
        name, mime = files[path]
        self.send_content(200, (UI / name).read_bytes(), mime + "; charset=utf-8")

    def do_POST(self):
        if self.path != "/api/simulate":
            self.send_json(404, {"error": "Không tìm thấy chức năng."})
            return
        # Only the same-origin local UI may submit jobs from a browser.
        origin = self.headers.get("Origin")
        if origin and origin != "http://" + self.headers.get("Host", ""):
            self.send_json(403, {"error": "Hãy chạy mô phỏng từ giao diện demo."})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 4096:
                raise ValueError("Thiết lập kịch bản không hợp lệ.")
            options = validate_request(json.loads(self.rfile.read(length)))
        except (ValueError, TypeError) as exc:
            message = str(exc) if isinstance(exc, ValueError) and not isinstance(exc, json.JSONDecodeError) else "Dữ liệu gửi lên không hợp lệ."
            self.send_json(400, {"error": message})
            return
        if not RUN_LOCK.acquire(blocking=False):
            self.send_json(409, {"error": "Một mô phỏng đang chạy. Vui lòng chờ rồi thử lại."})
            return
        try:
            self.send_json(200, run_scenario(options))
        except Exception:
            logging.exception("Simulation failed")
            self.send_json(500, {"error": "Chưa chạy được mô phỏng. Kiểm tra cửa sổ terminal rồi thử lại."})
        finally:
            RUN_LOCK.release()


def main():
    parser = argparse.ArgumentParser(description="Giao diện demo mô phỏng hàng đợi (localhost).")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    load_demo()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), DemoHandler)
    print(f"Demo sẵn sàng: http://127.0.0.1:{args.port} — Ctrl+C để dừng.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
