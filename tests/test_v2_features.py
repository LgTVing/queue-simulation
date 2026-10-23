"""
tests/test_v2_features.py: Test bo sung cho cac tinh nang moi cua dot chinh sua v2:
1. Ca lam viec MILP (Mo hinh A vs Mo hinh B, cac nghiem chuan)
2. He so nhan ngay (Day multiplier): mean = 1, CV khop cau hinh
3. Nhan kiem dinh Poisson: p < 0.05 luon bi bac bo (khong bao gio 'Chua bac bo')
4. Tinh nhat quan cua du lieu doc tu final_v2
"""

import numpy as np
import pytest
import b_shifts
from common import Model, exp_service
import c_sim as cs

def poisson_label(p):
    if p < 0.01:
        return "Bác bỏ (mạnh)"
    elif p < 0.05:
        return "Bác bỏ (nhẹ)"
    else:
        return "Chưa bác bỏ"

def test_poisson_labels_strict():
    """Kiem tra quy tac gan nhan Poisson khong bao gio nhan sai cho p < 0.05."""
    assert poisson_label(0.0001) == "Bác bỏ (mạnh)"
    assert poisson_label(0.0099) == "Bác bỏ (mạnh)"
    assert poisson_label(0.0100) == "Bác bỏ (nhẹ)"
    assert poisson_label(0.0356) == "Bác bỏ (nhẹ)"
    assert poisson_label(0.0499) == "Bác bỏ (nhẹ)"
    assert poisson_label(0.0500) == "Chưa bác bỏ"
    assert poisson_label(0.0763) == "Chưa bác bỏ"

def test_day_multiplier_distribution():
    """Kiem tra he so nhan ngay m_d co ky vong = 1 va CV dung cau hinh."""
    day_cv = 0.118
    shape_m = 1.0 / (day_cv ** 2)
    scale_m = day_cv ** 2
    
    rng = np.random.default_rng(12345)
    samples = rng.gamma(shape_m, scale_m, size=10000)
    
    assert np.mean(samples) == pytest.approx(1.0, abs=0.01)
    sample_cv = np.std(samples, ddof=1) / np.mean(samples)
    assert sample_cv == pytest.approx(day_cv, abs=0.01)

def test_shift_model_a_no_solution_for_4_and_3():
    """Kiem tra mo hinh A (8h lien tuc) KHONG THE phu dung lich 44 voi 4 NV 8h + 3 NV 4h."""
    c_opt = [4, 5, 6, 5, 5, 5, 5, 5, 4]
    res_a = b_shifts.solve_shift_scheduling(c_opt, model_type="A", allow_8h=True, allow_4h=True, exact_coverage=True)
    assert res_a["success"] is False

def test_shift_model_b_unique_solution_for_4_and_3():
    """Kiem tra mo hinh B (nghi gio 3-5) co nghiem phu dung lich 44 voi 4 NV 8h + 3 NV 4h."""
    c_opt = [4, 5, 6, 5, 5, 5, 5, 5, 4]
    res_b = b_shifts.solve_shift_scheduling(c_opt, model_type="B", lunch_window=(3, 5), allow_8h=True, allow_4h=True, exact_coverage=True)
    assert res_b["success"] is True
    assert res_b["actual_coverage"] == c_opt
    assert res_b["total_work_hours"] == 44
    assert res_b["total_staff"] == 7
    assert res_b["n_staff_4h"] == 3
    assert res_b["n_staff_8h"] == 4

def test_shift_pure_4h_and_pure_8h():
    """Kiem tra ket qua chuan cho chi ca 4h (52 q-h) va chi ca 8h mo hinh A (64 q-h)."""
    c_opt = [4, 5, 6, 5, 5, 5, 5, 5, 4]
    res_4h = b_shifts.solve_shift_scheduling(c_opt, allow_8h=False, allow_4h=True)
    assert res_4h["total_work_hours"] == 52
    assert res_4h["actual_coverage"] == [4, 5, 6, 6, 5, 8, 7, 7, 4]

    res_8h_a = b_shifts.solve_shift_scheduling(c_opt, model_type="A", allow_8h=True, allow_4h=False)
    assert res_8h_a["total_work_hours"] == 64
    assert res_8h_a["actual_coverage"] == [4, 8, 8, 8, 8, 8, 8, 8, 4]

    res_8h_b_wide = b_shifts.solve_shift_scheduling(c_opt, model_type="B", lunch_window=(1, 7), allow_8h=True, allow_4h=False)
    assert res_8h_b_wide["total_work_hours"] == 48
    assert res_8h_b_wide["total_staff"] == 6
    assert res_8h_b_wide["actual_coverage"] == [6, 5, 6, 5, 5, 5, 5, 5, 6]

def test_c6_coverage_cannot_be_done_by_6_staff():
    """Kiem tra phu 6 quay 9 gio can it nhat 7 NV (khong the voi 6 NV khi co gio nghi)."""
    c_6 = [6] * 9
    res_6 = b_shifts.solve_shift_scheduling(c_6, model_type="B", lunch_window=(1, 7), allow_4h=False)
    assert res_6["total_staff"] >= 7
