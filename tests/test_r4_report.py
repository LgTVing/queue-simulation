"""
tests/test_r4_report.py: Kiem thu bang doi chieu V4 -> V5 (R4):
1. recommended_surge chon chinh sach it nguoi du phong nhat, dat P >= Lich 48 va 14/14 ngay,
   quay-gio TB nho nhat
2. Doi chieu final_v4 voi chinh no: moi chi so V4 deu "giong"/0, khong dong nao bi gan co dieu tra
"""

import os
import pandas as pd
import pytest

import common
import f_scenarios
import g_report


def _surge_df():
    cols = ["chinh_sach", "nguong_cho", "quay_du_phong_toi_da", "P_SL_ngay_ge90_bien_dong",
            "so_ngay_dat_14", "quay_gio_TB_14_ngay"]
    rows = [
        ("Lich 48 co dinh", None, 0, 0.94, 14, 48.0),
        ("t1", 1, 1, 0.97, 14, 47.2),
        ("t2", 2, 1, 0.97, 14, 46.4),
        ("t3", 3, 1, 0.93, 14, 45.9),   # P thap hon Lich 48
        ("t3e2", 3, 2, 0.96, 14, 46.2),  # can 2 nguoi du phong
        ("t0", 0, 1, 0.99, 13, 45.0),   # hut 1 ngay
    ]
    return pd.DataFrame(rows, columns=cols)


def test_recommended_surge_rule():
    assert f_scenarios.recommended_surge(_surge_df())["chinh_sach"] == "t2"


def test_recommended_surge_none_when_no_candidate():
    df = _surge_df()
    df.loc[df["nguong_cho"].notna(), "so_ngay_dat_14"] = 13
    assert f_scenarios.recommended_surge(df) is None


V4_DIR = os.path.join(common.BASE_DIR, "results", "final_v4")


@pytest.mark.skipif(not os.path.isdir(V4_DIR), reason="chua co results/final_v4")
def test_doi_chieu_v4_self_identical(monkeypatch):
    monkeypatch.setattr(common, "RESULTS_DIR", V4_DIR)
    df = g_report.build_doi_chieu()
    old = df[df["nguyen_nhan"].str.startswith("Khong doi")]
    assert len(old) >= 15
    assert set(old["chenh_lech"].astype(str)) <= {"0.0", "giong"}
    assert not df["nguyen_nhan"].str.contains("NGOAI Y MUON").any()
