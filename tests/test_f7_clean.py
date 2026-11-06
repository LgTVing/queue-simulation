"""
tests/test_f7_clean.py: Kiem thu tai lap lam sach du lieu (F7):
lam_sach.clean_data doc du lieu tho bang duong dan tuong doi va cho ket qua
trung tung gia tri voi data/clean/data_clean.csv. Bo qua khi khong co tep tho
(du lieu tho khong nam trong repo, xem data/raw/README.md).
"""

import os
import sys
import pandas as pd
import pytest

from common import BASE_DIR, DATA_CLEAN

sys.path.insert(0, os.path.join(BASE_DIR, "data"))
import lam_sach  # noqa: E402


@pytest.mark.skipif(not os.path.exists(lam_sach.RAW_PATH), reason="khong co data/raw/September1999.txt")
def test_clean_data_reproduces_committed_csv(tmp_path):
    out = tmp_path / "data_clean.csv"
    lam_sach.clean_data(clean_path=str(out))
    pd.testing.assert_frame_equal(pd.read_csv(out), pd.read_csv(DATA_CLEAN))


def test_default_paths_inside_repo():
    assert os.path.commonpath([lam_sach.RAW_PATH, BASE_DIR]) == BASE_DIR
    assert os.path.samefile(lam_sach.CLEAN_PATH, DATA_CLEAN)
