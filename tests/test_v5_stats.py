"""
tests/test_v5_stats.py: Kiem thu thong ke bo sung V5:
1. S13: hoi quy du bao som fit chi tren 10 ngay train (so tinh tay trong ke hoach V5)
2. S14: CI cluster bootstrap rong hon Wilson khi cac lan lap trong cung kich ban tuong quan
3. S12: MLE kien nhan Weibull co kiem duyet khoi phuc tham so; so tren tap train
"""

import numpy as np
import pandas as pd

import a_data
import e_robustness as er
from common import DATA_CLEAN
from stats_utils import wilson_ci


def test_early_forecast_fit_on_train():
    df = pd.read_csv(DATA_CLEAN)
    tr, _ = a_data.split_train_test(df)
    reg, _, _, is_train, rmse_tr, rmse_te = er.early_forecast(a_data.counts_matrix(df), set(tr["day"]))
    assert is_train.sum() == 10
    assert abs(reg.intercept - 90.9) < 0.05 and abs(reg.slope - 4.20) < 0.005
    assert abs(rmse_te - 63.9) < 0.05 and rmse_tr < rmse_te


def test_cluster_bootstrap_wider_than_wilson():
    # 200 kich ban x 30 lan lap, ket qua hoan toan tuong quan trong kich ban
    means = np.repeat([0.0, 1.0], [140, 60])
    lo, hi = er.cluster_bootstrap_ci(means)
    _, w_lo, w_hi, _ = wilson_ci(60 * 30, 200 * 30)
    assert lo < 0.3 < hi
    assert (hi - lo) > 3 * (w_hi - w_lo)


def test_weibull_patience_recovers_parameters():
    """S12: du lieu Weibull(0.8, 10) bi kiem duyet boi thoi gian cho Exp(TB 4 phut) -> MLE khoi phuc tham so."""
    rng = np.random.default_rng(5)
    pat = 10.0 * rng.weibull(0.8, 20000)
    cens = rng.exponential(4.0, 20000)
    df = pd.DataFrame({"wait": np.minimum(pat, cens), "served": (cens < pat).astype(int)})
    fit = a_data.fit_patience_weibull(df)
    assert abs(fit["shape"] - 0.8) < 0.03 and abs(fit["scale"] - 10.0) < 0.8
    assert fit["aic_weibull"] < fit["aic_exp"]


def test_weibull_patience_train():
    df = pd.read_csv(DATA_CLEAN)
    tr, _ = a_data.split_train_test(df)
    fit = a_data.fit_patience_weibull(tr)
    assert abs(fit["theta_exp"] - 0.1087) < 1e-4
    assert 0.8 < fit["shape"] < 0.9 and fit["lr_pvalue"] < 0.001
