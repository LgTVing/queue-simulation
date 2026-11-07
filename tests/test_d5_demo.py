"""
tests/test_d5_demo.py: Kiem thu trang demo SIPP (D5): docs/demo/sipp_math.js (chay bang Node)
cho cung ket qua voi b_theory.py va khop results/final_v5/bang_sipp.csv. Bo qua khi khong co Node.
"""

import json
import os
import shutil
import subprocess

import numpy as np
import pandas as pd
import pytest

import b_theory as th
from common import BASE_DIR, RESULTS_DIR

JS = os.path.join(BASE_DIR, "docs", "demo", "sipp_math.js")
NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="khong co Node.js")

# Tham so train V5 (mo hinh chinh, bang_sipp.csv)
RATES = [0.99, 1.3767, 1.535, 1.39, 1.24, 1.2017, 1.3383, 1.3167, 1.0567]
MEAN_SVC = 2.9236448156318935
THETA = 0.1087


def _node(cases):
    """cases: [(lam, mu, theta, c, t)] -> [{"SL", "Wq", "p_ab", "util", "mmc"}]."""
    code = (f"const m = require({json.dumps(JS)});"
            f"const cases = {json.dumps(cases)};"
            "console.log(JSON.stringify(cases.map(([l, mu, th, c, t]) => "
            "Object.assign(m.erlangA(l, mu, th, c, t), {mmc: m.mmc(l, mu, c, t).P_sla}))));")
    out = subprocess.run([NODE, "-e", code], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def test_js_matches_b_theory():
    rng = np.random.default_rng(3)
    cases = [(float(rng.uniform(0.3, 3.0)), float(1 / rng.uniform(1.5, 5.0)), float(rng.uniform(0.02, 0.5)),
              int(rng.integers(2, 12)), float(rng.choice([2.0, 5.0]))) for _ in range(25)]
    for (lam, mu, theta, c, t), js in zip(cases, _node(cases)):
        py = th.erlang_a(lam, mu, theta, c, t)
        for k in ("SL", "Wq", "p_ab", "util"):
            assert js[k] == pytest.approx(py[k], abs=1e-9), (k, lam, mu, theta, c, t)
        mm = th.mmc(lam, mu, c, t)["P_sla"]
        assert js["mmc"] == pytest.approx(mm, abs=1e-12)


@pytest.mark.skipif(not os.path.exists(os.path.join(RESULTS_DIR, "bang_sipp.csv")), reason="chua co bang_sipp.csv")
def test_js_reproduces_bang_sipp():
    b = pd.read_csv(os.path.join(RESULTS_DIR, "bang_sipp.csv"))
    mu = 1.0 / MEAN_SVC
    code = (f"const m = require({json.dumps(JS)});"
            f"const r = {json.dumps(RATES)};"
            f"console.log(JSON.stringify({{a: m.sippSchedule(r, {mu}, {THETA}, 0.9, 5, true).map(x => x.c),"
            f" c: m.sippSchedule(r, {mu}, 0, 0.9, 5, false).map(x => x.c)}}));")
    sched = json.loads(subprocess.run([NODE, "-e", code], capture_output=True, text=True, check=True).stdout)
    assert sched["a"] == list(b["c_erlang_a"]) and sched["c"] == list(b["c_erlang_c"])
    js = _node([(lam, mu, THETA, int(c), 5.0) for lam, c in zip(b["lambda"], b["c_erlang_a"])])
    np.testing.assert_allclose([x["SL"] for x in js], b["sl_erlang_a"], atol=5e-4)
    np.testing.assert_allclose([x["p_ab"] for x in js], b["p_ab_erlang_a"], atol=5e-4)


def test_js_shift_schedule_matches_milp():
    """Xep ca JS (bước 2 của demo) cho cùng giờ công tối thiểu và độ phủ với b_shifts.solve_shift_scheduling."""
    import b_shifts
    reqs = [[4, 5, 6, 5, 5, 5, 5, 5, 4], [4, 5, 6, 5, 5, 5, 5, 5, 5], [4, 6, 6, 6, 5, 5, 6, 5, 5],
            [5, 6, 6, 6, 6, 5, 6, 6, 5], [2, 3, 4, 4, 3, 3, 4, 3, 2]]
    code = (f"const m = require({json.dumps(JS)});"
            f"console.log(JSON.stringify({json.dumps(reqs)}.map(r => m.shiftSchedule(r, 3, 5))));")
    out = json.loads(subprocess.run([NODE, "-e", code], capture_output=True, text=True, check=True).stdout)
    for req, js in zip(reqs, out):
        py = b_shifts.solve_shift_scheduling(req, "B", (3, 5))
        assert js["work"] == py["total_work_hours"], req
        assert all(c >= r for c, r in zip(js["coverage"], req)), req
        assert js["work"] == 8 * sum(js["n8"]) + 4 * sum(js["n4"])
