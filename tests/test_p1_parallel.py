"""
tests/test_p1_parallel.py: Kiem thu chay song song (P1):
1. Moi bo sinh thoi gian phuc vu va Model pickle duoc (dieu kien cho ProcessPoolExecutor tren Windows)
2. Bo sinh dang class cho cung day so voi ban lambda cu
3. run_reps chay song song cho ket qua giong het chay tuan tu
4. map_sim giu dung thu tu job
"""

import pickle
import numpy as np
import pytest
from common import (Model, exp_service, lognorm_service, gamma_service, weibull_service,
                    empirical_service, mix_service)
import c_sim as cs
import e_robustness as er

SAMPLERS = {
    "exp": exp_service(3.0),
    "lognorm": lognorm_service(3.0, 1.5),
    "gamma": gamma_service(1.1, 2.7),
    "weibull": weibull_service(1.03, 2.96),
    "empirical": empirical_service(np.array([1.0, 2.5, 4.0, 7.5])),
    "mix": mix_service(0.7, exp_service(1.0), gamma_service(2.0, 3.0)),
}


@pytest.mark.parametrize("name", SAMPLERS)
def test_samplers_picklable(name):
    s = SAMPLERS[name]
    s2 = pickle.loads(pickle.dumps(s))
    a = [s(np.random.default_rng(7)) for _ in range(5)]
    b = [s2(np.random.default_rng(7)) for _ in range(5)]
    assert a == b
    m = Model(rates=[1.0], service=s, theta=0.1)
    pickle.loads(pickle.dumps(m))


def test_samplers_match_lambda_version():
    """Cung rng, bo sinh class cho day so giong cong thuc lambda truoc P1."""
    sigma2 = np.log(1.0 + 1.5 ** 2)
    mu_log = np.log(3.0) - 0.5 * sigma2
    refs = {
        "exp": lambda rng: (float(rng.exponential(3.0)), 0),
        "lognorm": lambda rng: (float(rng.lognormal(mu_log, np.sqrt(sigma2))), 0),
        "gamma": lambda rng: (float(rng.gamma(1.1, 2.7)), 0),
        "weibull": lambda rng: (float(2.96 * rng.weibull(1.03)), 0),
    }
    for name, ref in refs.items():
        r1, r2 = np.random.default_rng(11), np.random.default_rng(11)
        assert [SAMPLERS[name](r1) for _ in range(20)] == [ref(r2) for _ in range(20)], name


def _model():
    return Model(rates=[1.2, 1.6, 1.0], service=empirical_service(np.random.default_rng(1).gamma(1.1, 2.7, 500)),
                 theta=0.1, p_vip=0.35)


def test_run_reps_parallel_identical(monkeypatch):
    sched = [4, 5, 4]
    monkeypatch.setattr(cs, "N_WORKERS", 1)
    serial = cs.run_reps(_model(), sched, n_reps=12, seed_base=500, keep_reps=True)
    monkeypatch.setattr(cs, "N_WORKERS", 3)
    par = cs.run_reps(_model(), sched, n_reps=12, seed_base=500, keep_reps=True)
    assert serial.keys() == par.keys()
    for k in serial:
        a, b = serial[k], par[k]
        if isinstance(a, np.ndarray):
            np.testing.assert_array_equal(a, b)
        else:
            assert a == b, k


def _rep_stats_pandas(df, schedule, hour_len=60.0, t_start=0.0, wt=5.0, wtv=2.0):
    """Ban pandas cua rep_stats truoc P2 (tham chieu, chi cac chi so chinh)."""
    served = df["served"] == 1
    out = {"sl_all": float((served & (df["wait"] <= wt)).sum() / len(df)),
           "wq_all": float(df["wait"].mean()), "p_ab_all": float((df["served"] == 0).mean()),
           "util_all": float(df[served]["svc"].sum() / (sum(schedule) * hour_len))}
    dv = df[df["vip"] == 1]
    out["sl_vip"] = float(((dv["served"] == 1) & (dv["wait"] <= wtv)).sum() / len(dv))
    hourly = []
    for h in range(len(schedule)):
        dh = df[df["hour"] == h]
        hourly.append((float(((dh["served"] == 1) & (dh["wait"] <= wt)).sum() / len(dh)),
                       float(dh["wait"].mean()), float((dh["served"] == 0).mean())))
    return out, hourly


@pytest.mark.parametrize("seed", range(5))
def test_rep_stats_matches_pandas(seed):
    """P2: rep_stats ban NumPy cho ket qua trung tung bit voi ban pandas."""
    sched = [4, 5, 4]
    df = cs.simulate(_model(), sched, seed=seed, day_cv=0.14)
    ref, ref_h = _rep_stats_pandas(df, sched)
    st = cs.rep_stats(df, sched)
    for k, v in ref.items():
        assert st[k] == v, k
    assert [(x["sl"], x["wq"], x["p_ab"]) for x in st["hourly"]] == ref_h


def test_map_sim_order_and_post(monkeypatch):
    sched = [4, 5, 4]
    jobs = [dict(model=_model(), schedule=sched, seed=900 + i, day_multiplier=1.0 + 0.05 * i) for i in range(8)]
    monkeypatch.setattr(cs, "N_WORKERS", 1)
    serial = cs.map_sim(jobs, er._post_sl_all, (sched,))
    monkeypatch.setattr(cs, "N_WORKERS", 3)
    par = cs.map_sim(jobs, er._post_sl_all, (sched,))
    assert serial == par
