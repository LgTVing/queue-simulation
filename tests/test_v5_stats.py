"""
tests/test_v5_stats.py: Kiem thu thong ke bo sung V5:
1. S13: hoi quy du bao som fit chi tren 10 ngay train (so tinh tay trong ke hoach V5)
2. S14: CI cluster bootstrap rong hon Wilson khi cac lan lap trong cung kich ban tuong quan
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
