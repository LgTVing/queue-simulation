"""
h_staffing.py: Toi uu truc tiep theo gio cong ca lam viec (M6, docs/KE_HOACH_V5.md).

Bien quyet dinh: so nhan vien theo tung loai ca x_s (b_shifts.create_shifts, mo hinh B).
Lich quay dua vao mo phong = do phu A.x (quay du van mo, dung thuc te).
Muc tieu: min gio cong W = sum(gio lam viec cua ca * x_s) sao cho lich A.x kha thi
(can duoi CI95 SL moi gio >= 90%, cung tieu chi c_sim.is_schedule_feasible).

Thuat toan: W la boi cua 4 (ca 4h/8h) va tong do phu = W. Duyet W tang dan; o moi muc,
liet ke MOI lich phu khac nhau co moi gio >= lich SIPP - slack, mo phong tung lich
(seed chon lich 1000, 60 lan lap). Dung o W nho nhat co lich kha thi. Cac lich kha thi
xep theo can duoi gio te nhat; top-k duoc xac nhan bang seed danh gia (300 lan lap),
kem do ben: bien dong ngay (CV ngay) va nhu cau +10%.
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd

from common import Model, TARGET_SLA, scaled
import b_shifts
import c_sim as sim

SEED_SELECT = 1000      # trung seed chon lich cua optimize_schedule
SEED_EVAL = 50000       # trung seed danh gia chinh sach
SEED_ROBUST = 81000     # bien dong ngay va nhu cau +10% cho top-k (dai seed moi)


def coverage_vectors(W: int, lower: List[int], lunch_window: Tuple[int, int] = (3, 5)) -> Dict[tuple, List[int]]:
    """
    Moi do phu A.x khac nhau voi tong gio cong W va do phu >= lower o moi gio.
    Tra ve {do phu: x dau tien tim thay} (x theo thu tu ca cua b_shifts.create_shifts).
    """
    A, c, _, _ = b_shifts.create_shifts("B", lunch_window)
    k = len(c)
    out: Dict[tuple, List[int]] = {}

    def rec(i: int, budget: int, x: List[int]):
        if i == k:
            if budget == 0:
                cov = tuple(int(v) for v in A @ np.array(x))
                if all(a >= b for a, b in zip(cov, lower)) and cov not in out:
                    out[cov] = list(x)
            return
        for n in range(budget // int(c[i]) + 1):
            rec(i + 1, budget - n * int(c[i]), x + [n])

    rec(0, W, [])
    return out


def _describe_x(x: List[int], lunch_window: Tuple[int, int]) -> str:
    _, _, names, _ = b_shifts.create_shifts("B", lunch_window)
    return "; ".join(f"{n} x{v}" for n, v in zip(names, x) if v > 0)


def optimize_shift_staffing(model: Model, sipp: List[int], lunch_window: Tuple[int, int] = (3, 5),
                            slack: int = 1, n_reps: int = 60, w_max: int = 64, top_k: int = 5,
                            cv_day: float = 0.0) -> Dict:
    """
    M6: tim gio cong nho nhat va phuong an ca kha thi.
    slack: do phu moi gio duoc thap hon lich SIPP toi da slack quay (khong gian tim kiem).
    Tra ve {"W": gio cong toi uu, "trials": DataFrame moi lich da thu, "top": DataFrame top-k da xac nhan}.
    """
    n_reps = scaled(n_reps)
    lower = [max(0, s - slack) for s in sipp]
    w = 4 * int(np.ceil(sum(lower) / 4))
    rows = []
    while w <= w_max:
        cands = coverage_vectors(w, lower, lunch_window)
        found = False
        for cov, x in sorted(cands.items()):
            res = sim.run_reps(model, list(cov), n_reps=n_reps, seed_base=SEED_SELECT)
            feas, viol = sim.is_schedule_feasible(res)
            worst = min(res["hourly"], key=lambda r: r["sl_ci95_low"])
            rows.append({"gio_cong": w, "phu_quay": str(list(cov)), "quay_gio_mo": sum(cov),
                         "phuong_an_ca": _describe_x(x, lunch_window), "n_ca_8h": sum(x[-3:]), "n_ca_4h": sum(x[:-3]),
                         "sl_toan_ngay": res["sl_mean"], "ti_le_bo_ve": res["p_ab_mean"],
                         "gio_te_nhat": worst["hour"], "sl_gio_te_nhat_low": worst["sl_ci95_low"],
                         "gio_vi_pham": str(viol), "kha_thi": "Y" if feas else "N"})
            found |= feas
        print(f"  • M6: gio cong {w}: {len(cands)} lich phu, {sum(r['kha_thi'] == 'Y' for r in rows if r['gio_cong'] == w)} kha thi")
        if found:
            break
        w += 4
    trials = pd.DataFrame(rows)
    if not found:
        # Chi xay ra khi so lan lap qua nho (vd smoke test): CI qua rong, khong lich nao kha thi
        print(f"  [canh bao] M6: khong co lich kha thi voi gio cong <= {w_max}")
        return {"W": None, "trials": trials, "top": pd.DataFrame()}
    feas_rows = trials[(trials["gio_cong"] == w) & (trials["kha_thi"] == "Y")]
    feas_rows = feas_rows.sort_values("sl_gio_te_nhat_low", ascending=False).head(top_k)
    top = [_confirm(model, eval(r.phu_quay), r, cv_day) for r in feas_rows.itertuples()]
    return {"W": w, "trials": trials, "top": pd.DataFrame(top)}


def _confirm(model: Model, cov: List[int], r, cv_day: float) -> Dict:
    """Xac nhan 1 lich bang seed danh gia va do ben (bien dong ngay, nhu cau +10%)."""
    res = sim.run_reps(model, cov, n_reps=scaled(300), seed_base=SEED_EVAL)
    feas, _ = sim.is_schedule_feasible(res)
    worst = min(res["hourly"], key=lambda h: h["sl_ci95_low"])
    out = {"gio_cong": r.gio_cong, "phu_quay": str(cov), "quay_gio_mo": sum(cov), "phuong_an_ca": r.phuong_an_ca,
           "sl_toan_ngay": res["sl_mean"], "sl_ci_half": res["sl_ci_half"], "gio_te_nhat": worst["hour"],
           "sl_gio_te_nhat_low": worst["sl_ci95_low"], "ti_le_bo_ve": res["p_ab_mean"], "wq_phut": res["wq_mean"],
           "kha_thi_seed_danh_gia": "Y" if feas else "N"}
    if cv_day > 0:
        bd = sim.run_reps(model, cov, n_reps=scaled(300), seed_base=SEED_ROBUST, day_cv=cv_day, keep_reps=True)
        out["P_SL_ngay_ge90"] = float(np.mean(np.asarray(bd["rep_sl_day"]) >= TARGET_SLA))
    m_up = Model(rates=[x * 1.1 for x in model.rates], service=model.service, theta=model.theta,
                 p_vip=model.p_vip, hour_len=model.hour_len, mean_svc=model.mean_svc, cs2_svc=model.cs2_svc)
    up = sim.run_reps(m_up, cov, n_reps=scaled(150), seed_base=SEED_ROBUST + 50000)
    out["nhu_cau_110_gio_te_nhat_low"] = min(h["sl_ci95_low"] for h in up["hourly"])
    return out
