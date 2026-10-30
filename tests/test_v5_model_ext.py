"""
tests/test_v5_model_ext.py: Kiem thu cac truong mo rong cua Model (S12, S15, M8 ngay 10):
1. patience = Exp(theta), sub_rates = 1 khuc/gio, service_by_hour = service chung
   cho ket qua giong het mac dinh (cung chuoi so ngau nhien)
2. sub_rates: so khach moi nua gio xap xi lambda khuc * 30 phut
3. service_by_hour: gio co phuc vu cham hon thi thoi gian phuc vu TB cao hon
4. Bo sinh kien nhan pickle duoc
"""

import dataclasses
import pickle
import numpy as np
import pandas as pd

from common import Model, empirical_service, exp_service, exp_patience, weibull_patience
import c_sim as cs

RATES = [1.0, 1.5, 1.4, 1.3, 1.1, 1.2, 1.3, 1.2, 1.0]
SCHED = [4, 5, 6, 5, 5, 5, 5, 5, 5]
BASE = Model(rates=RATES, service=empirical_service(np.array([1.0, 2.0, 3.5, 6.0])), theta=0.11, p_vip=0.35)


def _sim(model, seed=11):
    return cs.simulate(model, SCHED, seed=seed)


def test_extensions_default_equivalent_identical():
    ref = _sim(BASE)
    for m in (dataclasses.replace(BASE, patience=exp_patience(BASE.theta)),
              dataclasses.replace(BASE, sub_rates=[[r] for r in RATES]),
              dataclasses.replace(BASE, sub_rates=[None] * len(RATES)),
              dataclasses.replace(BASE, service_by_hour=[BASE.service] * len(RATES))):
        pd.testing.assert_frame_equal(_sim(m), ref)


def test_sub_rates_half_hour_counts():
    m = dataclasses.replace(BASE, rates=[1.0] * 9, sub_rates=[[0.4, 1.6]] + [None] * 8)
    n1 = n2 = 0
    for s in range(40):
        df = _sim(m, seed=100 + s)
        t = df.loc[df["hour"] == 0, "arr_time"]
        n1 += int((t < 30).sum())
        n2 += int((t >= 30).sum())
    assert abs(n1 / 40 - 12) < 2.5 and abs(n2 / 40 - 48) < 4


def test_service_by_hour_slower():
    slow = empirical_service(np.array([1.0, 2.0, 3.5, 6.0]) * 1.5)
    m = dataclasses.replace(BASE, service_by_hour=[None] * 6 + [slow] * 3)
    df = pd.concat([_sim(m, seed=200 + s) for s in range(10)])
    early, late = df.loc[df["hour"] < 6, "svc"].mean(), df.loc[df["hour"] >= 6, "svc"].mean()
    assert late > 1.3 * early


def test_patience_samplers_picklable():
    for s in (exp_patience(0.1), weibull_patience(0.8, 9.0)):
        s2 = pickle.loads(pickle.dumps(s))
        assert s(np.random.default_rng(3)) == s2(np.random.default_rng(3))
    pickle.loads(pickle.dumps(dataclasses.replace(BASE, patience=weibull_patience(0.8, 9.0),
                                                  sub_rates=[[1.0, 2.0]] + [None] * 8,
                                                  service_by_hour=[exp_service(3.0)] * 9)))
