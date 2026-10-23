"""
b_shifts.py: Module toi uu hoa lap lich ca lam viec bang MILP (Thanh vien B).
Ho tro:
- Mo hinh A: Ca 8h lam viec lien tuc (khong nghi trua), bat dau gio 0 hoac gio 1.
- Mo hinh B: Ca 8h co nghi 1 gio (co mat 9h, lam viec 8h), gio nghi nam trong cua so quy dinh.
- Ca 4h: 4 gio lam viec lien tuc (bat dau gio 0 den gio 5).
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

from common import HOURS, H_LABELS

def create_shifts(
    model_type: str = "B",
    lunch_window: Tuple[int, int] = (3, 5),
    allow_4h: bool = True,
    allow_8h: bool = True,
    n_hours: int = HOURS
) -> Tuple[np.ndarray, np.ndarray, List[str], List[int]]:
    """
    Tao ma tran phu A va vector chi phi c cho cac loai ca.
    model_type: 'A' (8h lien tuc) hoac 'B' (8h co nghi 1h).
    lunch_window: (start_h, end_h) chi so gio duoc phep nghi trua (inclusive).
    """
    shift_cols = []
    costs = []
    shift_names = []
    shift_work_hours = []

    # 1. Ca 4h
    if allow_4h:
        for s in range(n_hours - 3):
            cov = [1 if s <= h < s + 4 else 0 for h in range(n_hours)]
            shift_cols.append(cov)
            costs.append(4)  # 4 gio lam viec
            shift_names.append(f"Ca 4h ({s+8}h-{s+12}h)")
            shift_work_hours.append(4)

    # 2. Ca 8h
    if allow_8h:
        if model_type == "A":
            # 8h lien tuc: bat dau tu gio 0 hoac gio 1
            for s in range(n_hours - 7):
                cov = [1 if s <= h < s + 8 else 0 for h in range(n_hours)]
                shift_cols.append(cov)
                costs.append(8)
                shift_names.append(f"Ca 8h liên tục ({s+8}h-{s+16}h)")
                shift_work_hours.append(8)
        elif model_type == "B":
            # 8h co nghi 1h: co mat suot 9 gio, nghi 1 gio trong lunch_window
            l_start, l_end = lunch_window
            for l in range(l_start, l_end + 1):
                cov = [0 if h == l else 1 for h in range(n_hours)]
                shift_cols.append(cov)
                costs.append(8)  # Chi phi luong tinh tren 8 gio lam viec
                shift_names.append(f"Ca 8h (nghỉ {l+8}h-{l+9}h)")
                shift_work_hours.append(8)
        else:
            raise ValueError(f"Loai mo hinh khong hop le: {model_type}")

    A = np.array(shift_cols).T
    c = np.array(costs)
    return A, c, shift_names, shift_work_hours

def solve_shift_scheduling(
    target_schedule: List[int],
    model_type: str = "B",
    lunch_window: Tuple[int, int] = (3, 5),
    allow_4h: bool = True,
    allow_8h: bool = True,
    exact_coverage: bool = False,
    max_staff: int = 30
) -> Dict:
    """
    Giai bai toan lap lich ca MILP:
    min sum(c_j * x_j)
    s.t. A * x >= target_schedule (hoac == neu exact_coverage=True)
         x_j in Z_+, x_j >= 0
    """
    c_req = np.array(target_schedule, dtype=float)
    A, c, shift_names, shift_work_hours = create_shifts(
        model_type=model_type,
        lunch_window=lunch_window,
        allow_4h=allow_4h,
        allow_8h=allow_8h,
        n_hours=len(target_schedule)
    )

    lb = c_req
    ub = c_req if exact_coverage else np.full_like(c_req, np.inf)

    constraints = LinearConstraint(A, lb=lb, ub=ub)
    bounds = Bounds(0, max_staff)
    integrality = np.ones(len(c))

    res = milp(c=c, integrality=integrality, constraints=constraints, bounds=bounds)

    if not res.success:
        return {
            "success": False,
            "status": res.status,
            "message": res.message,
            "model_type": model_type,
            "target_schedule": target_schedule
        }

    x = np.round(res.x).astype(int)
    staffing_hourly = (A @ x).tolist()
    total_work_hours = int(np.sum(x * shift_work_hours))

    # Tinh gio co mat (on-site hours): voi ca 8h mo hinh B la 9h
    total_presence_hours = 0
    for name, cnt in zip(shift_names, x):
        if "Ca 8h" in name and model_type == "B":
            total_presence_hours += cnt * 9
        elif "Ca 8h" in name:
            total_presence_hours += cnt * 8
        elif "Ca 4h" in name:
            total_presence_hours += cnt * 4

    # Dem so nhan vien
    n_4h = sum(cnt for name, cnt in zip(shift_names, x) if "Ca 4h" in name)
    n_8h = sum(cnt for name, cnt in zip(shift_names, x) if "Ca 8h" in name)
    total_staff = n_4h + n_8h

    schedule_details = {name: int(cnt) for name, cnt in zip(shift_names, x) if cnt > 0}

    return {
        "success": True,
        "model_type": model_type,
        "target_schedule": target_schedule,
        "actual_coverage": staffing_hourly,
        "total_work_hours": total_work_hours,
        "total_presence_hours": total_presence_hours,
        "total_staff": total_staff,
        "n_staff_4h": n_4h,
        "n_staff_8h": n_8h,
        "shift_breakdown": schedule_details,
        "waste_work_hours": total_work_hours - sum(target_schedule),
        "waste_pct": ((total_work_hours - sum(target_schedule)) / sum(target_schedule)) * 100.0
    }
