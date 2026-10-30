"""
tests/test_v4_pipeline.py: Kiem thu bo sung V4:
1. T1-d: Lich SIPP la toi thieu (c_h dat SL, c_h - 1 khong dat) cho ca Erlang C va Erlang-A
2. T1-e: SL Erlang-A ly thuyet nam trong CI95 cua mo phong
3. T1-f: Cat cut K, M cua Erlang-A khong anh huong ket qua
4. T1-h: tools/check_consistency.py bao 0 lech
5. T1-i: Smoke test toan bo pipeline voi --reps-scale nho (danh dau slow)
"""

import os
import sys
import subprocess
import pytest
from common import Model, exp_service, BASE_DIR
import b_theory as th
import c_sim as cs

# Tham so tap train (rates, E[S], theta) dung lam cau hinh thu
RATES = [0.99, 1.3767, 1.535, 1.39, 1.24, 1.2017, 1.3383, 1.3167, 1.0567]
MU = 1.0 / 2.9236
THETA = 0.1087


@pytest.mark.parametrize("use_a", [False, True])
def test_sipp_is_minimal(use_a):
    """T1-d: Moi gio, c_h dat SL >= 90% va c_h - 1 khong dat."""
    sched = th.sipp_schedule(RATES, MU, THETA, target=0.90, use_erlang_a=use_a)

    def sl(lam, c):
        return th.erlang_a(lam, MU, THETA, c)["SL"] if use_a else th.mmc(lam, MU, c)["P_sla"]

    for lam, c in zip(RATES, sched):
        assert sl(lam, c) >= 0.90
        assert c == 1 or sl(lam, c - 1) < 0.90


def test_erlang_a_sl_vs_sim():
    """T1-e: Erlang-A (lam=2, E[S]=3, theta=0.1, c=6): SL ly thuyet trong CI95 cua 30 lan lap."""
    lam, es, theta, c = 2.0, 3.0, 0.1, 6
    sl_th = th.erlang_a(lam, 1.0 / es, theta, c)["SL"]
    m = Model([lam], exp_service(es), theta=theta, p_vip=0.0, hour_len=8000.0)
    res = cs.run_reps(m, [c], n_reps=30, run_time=5000.0, warm_up=500.0, seed_base=303)
    assert abs(res["sl_mean"] - sl_th) <= res["sl_ci_half"]


@pytest.mark.parametrize("lam,c", [(1.535, 5), (1.0567, 4), (2.0, 6), (1.39, 4)])
def test_erlang_a_truncation(lam, c):
    """T1-f: Tang K/M (200 -> 400, 80 -> 160) lam SL, Wq, p_ab doi < 1e-6."""
    base = th.erlang_a(lam, MU, THETA, c, K=200, M=80)
    big = th.erlang_a(lam, MU, THETA, c, K=400, M=160)
    for key in ["SL", "Wq", "p_ab", "util"]:
        assert abs(base[key] - big[key]) < 1e-6


def test_results_consistency():
    """T1-h: Moi so trong tong_hop.md khop CSV nguon (tools/check_consistency.py tra exit 0)."""
    r = subprocess.run([sys.executable, os.path.join(BASE_DIR, "tools", "check_consistency.py")],
                       cwd=BASE_DIR, capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stdout[-2000:]


@pytest.mark.slow
def test_pipeline_smoke(tmp_path):
    """T1-i: main.py --stage all --reps-scale 0.02 chay het, sinh bang so sanh va MO_TA.md."""
    env = dict(os.environ, QS_RESULTS_DIR=str(tmp_path))
    r = subprocess.run([sys.executable, os.path.join(BASE_DIR, "main.py"), "--stage", "all", "--reps-scale", "0.02"],
                       cwd=BASE_DIR, env=env, capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr[-3000:]
    for name in ["params.json", "so_sanh_chinh_sach.csv", "kiem_chung.csv", "do_nhay_kien_nhan.csv",
                 "doi_chieu_v4_v5.csv", "MO_TA.md"]:
        assert (tmp_path / name).exists(), name
