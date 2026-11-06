"""
d_experiments.py: Ngu canh chung va cac thi nghiem toi uu hoa (giai doan 'optimize'):
1. Nap ngu canh: du lieu, tap train/test, tham so, mo hinh chinh (phuc vu thuc nghiem)
   va mo hinh Gamma (do nhay); doc/ghi lich khuyen nghi (lich_khuyen_nghi.json)
2. Toi uu lich quay 2 pha + Pha 3 tim kiem cuc bo -> lich_toi_uu.csv, pha3.csv
3. Lich ben vung theo muc du phong nhu cau -> lich_ben_vung_delta.csv
4. So sanh chinh sach (300 lan lap, seed danh gia rieng) -> so_sanh_chinh_sach.csv
   va co bien dong ngay -> so_sanh_chinh_sach_bd.csv
5. Doi chieu gia dinh xa hang F1 (keep_last vs all_open) -> doi_chieu_xa_hang.csv
6. Xep ca lam viec MILP -> lich_theo_ca.csv, fig_b_ca_lam.png
Moi duong dan doc/ghi qua common.RESULTS_DIR; so lan lap nhan common.REPS_SCALE.
"""

import os
import json
import dataclasses
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import common
from common import Model, HOURS, H_LABELS, TARGET_SLA, scaled, out_path
import a_data
import b_theory as th
import b_shifts
import c_sim as sim

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "lines.linewidth": 1.8,
    "grid.alpha": 0.4
})

# Seed: bo chon lich (toi uu) va bo danh gia cuoi (M5); dai lay tu common.SEED_BANDS (F4).
# Luu y: 2 dai trung 11/300 lan lap (giu de khong doi so V5, KE_HOACH_V5_1 F4).
SEED_SELECT = common.SEED_BANDS["select"][0]
SEED_EVAL = common.SEED_BANDS["eval"][0]

SCHEDULES_FILE = "lich_khuyen_nghi.json"

# =============================================================================
# 1. NGU CANH CHUNG
# =============================================================================

def load_context(estimate: bool = False) -> Dict:
    """
    Nap du lieu va tham so. estimate=True: uoc luong lai params.json tu tap train
    (giai doan 'data'); nguoc lai doc params.json da dong bang trong RESULTS_DIR.
    """
    df_all = a_data.load_log()
    df_train, df_test = a_data.split_train_test(df_all, train_ratio=0.7)
    params_path = os.path.join(common.RESULTS_DIR, "params.json")
    if estimate or not os.path.exists(params_path):
        params = a_data.estimate_all(df_train, plot=True)
    else:
        with open(params_path, "r", encoding="utf-8") as f:
            params = json.load(f)
    svc_train = a_data.train_service_samples(df_train)
    return {
        "params": params,
        "df_all": df_all,
        "df_train": df_train,
        "df_test": df_test,
        "svc_train": svc_train,
        "model": a_data.build_model(params, svc_train, "empirical"),
        "model_gamma": a_data.build_model(params, svc_train, "gamma"),
        "n_day_mean": float(sum(params["rates_per_min"]) * 60.0),
    }

def save_schedules(updates: Dict[str, Optional[List[int]]]) -> Dict[str, List[int]]:
    """Cap nhat lich_khuyen_nghi.json (giu cac lich da co); gia tri None xoa khoa do."""
    sch = load_schedules(required=False)
    for k, v in updates.items():
        if v is None:
            sch.pop(k, None)
        else:
            sch[k] = [int(c) for c in v]
    with open(out_path(SCHEDULES_FILE), "w", encoding="utf-8") as f:
        json.dump(sch, f, indent=2, ensure_ascii=False)
    return sch

def load_schedules(required: bool = True) -> Dict[str, List[int]]:
    """Doc lich khuyen nghi da tinh o giai doan theory/optimize."""
    path = os.path.join(common.RESULTS_DIR, SCHEDULES_FILE)
    if not os.path.exists(path):
        if required:
            raise FileNotFoundError(f"Chua co {path}: hay chay --stage theory va optimize truoc")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def scale_demand(model: Model, factor: float) -> Model:
    """Mo hinh voi nhu cau nhan he so factor."""
    return dataclasses.replace(model, rates=[r * factor for r in model.rates])

def main_policies(sch: Dict[str, List[int]]) -> Dict[str, List[int]]:
    """Ba chinh sach chinh dung trong cac phan tich do ben."""
    return {
        "Toi uu": sch["toi_uu"],
        "Ben vung (+10%)": sch["ben_vung"],
        "Moc co so 6 quay": sch["moc_co_so"],
    }

# =============================================================================
# 2. GIAI DOAN THEORY: SIPP ERLANG C / ERLANG-A
# =============================================================================

def run_theory(ctx: Dict) -> Dict[str, List[int]]:
    """Lich SIPP theo Erlang C va Erlang-A, bang ly thuyet theo gio -> bang_sipp.csv."""
    model = ctx["model"]
    mu = 1.0 / model.mean_svc
    sched_c = th.sipp_schedule(model.rates, mu, 0.0, target=TARGET_SLA, use_erlang_a=False)
    sched_a = th.sipp_schedule(model.rates, mu, model.theta, target=TARGET_SLA, use_erlang_a=True)
    rows = []
    for h, lam in enumerate(model.rates):
        ea = th.erlang_a(lam, mu, model.theta, sched_a[h])
        ec = th.mmc(lam, mu, sched_c[h])
        rows.append({
            "gio": h, "khung_gio": H_LABELS[h], "lambda": lam, "tai_a": lam / mu,
            "c_erlang_c": sched_c[h], "sl_erlang_c": ec["P_sla"], "wq_erlang_c": ec["Wq"],
            "c_erlang_a": sched_a[h], "sl_erlang_a": ea["SL"], "wq_erlang_a": ea["Wq"],
            "p_ab_erlang_a": ea["p_ab"], "rho_erlang_a": ea["util"]
        })
    pd.DataFrame(rows).to_csv(out_path("bang_sipp.csv"), index=False, encoding="utf-8-sig")
    print(f"  Erlang C: {sched_c} = {sum(sched_c)} q-h | Erlang-A: {sched_a} = {sum(sched_a)} q-h")
    return save_schedules({
        "sipp_erlang_c": sched_c,
        "sipp_erlang_a": sched_a,
        "moc_co_so": [common.BASELINE_C] * HOURS,
    })

# =============================================================================
# 3. GIAI DOAN OPTIMIZE
# =============================================================================

def history_frame(history: List[Dict]) -> pd.DataFrame:
    return pd.DataFrame([{
        "buoc": h["step"],
        "pha": h["phase"],
        "lich": str(h["schedule"]),
        "tong_quay_gio": h["total_c_hours"],
        "sl_toan_ngay": round(h["sl_mean"], 4),
        "ti_le_bo_ve": round(h["p_ab_mean"], 4),
        "gio_te_nhat": h["worst_hour"],
        "sl_gio_te_nhat_low": round(h["worst_sl_low"], 4),
        "gio_vi_pham": str(h["violated_hours"]),
        "kha_thi": "Y" if h["feasible"] else "N"
    } for h in history])

def optimize(model: Model, max_p_ab: Optional[float] = None, scope: str = "all") -> Dict:
    """Toi uu 2 pha voi bo seed chon lich; scope = "regular" rang buoc SL rieng khach thuong (M9)."""
    return sim.optimize_schedule(model, target_sla=TARGET_SLA, n_reps=scaled(60),
                                 seed_base=SEED_SELECT, max_p_ab=max_p_ab, scope=scope)

def evaluate(model: Model, sched: List[int], n_reps: int = 300, **kw) -> Dict:
    """Danh gia cuoi voi bo seed danh gia (doc lap voi bo seed chon lich)."""
    return sim.run_reps(model, sched, n_reps=scaled(n_reps), seed_base=SEED_EVAL, **kw)

CLASS_SL = (("gop", "SL(5 phut) moi khach - SLA chinh"),
            ("thuong", "SL(5 phut) rieng khach thuong - giam sat"),
            ("vip", "SL(2 phut) rieng khach VIP - giam sat"))


def _post_class_sl(df: pd.DataFrame, sched: List[int]) -> np.ndarray:
    """SL theo gio (3 x H): gop moi khach <= 5 phut, khach thuong <= 5 phut, VIP <= 2 phut (NaN neu gio khong co khach nhom do)."""
    out = np.full((len(CLASS_SL), len(sched)), np.nan)
    hour = df["hour"].to_numpy()
    ok = df["served"].to_numpy() == 1
    wait = df["wait"].to_numpy(dtype=float)
    vip = df["vip"].to_numpy() == 1
    for h in range(len(sched)):
        in_h = hour == h
        for k, (mask, thr) in enumerate(((in_h, common.WAIT_THRESHOLD), (in_h & ~vip, common.WAIT_THRESHOLD),
                                         (in_h & vip, common.WAIT_THRESHOLD_VIP))):
            if mask.any():
                out[k, h] = np.count_nonzero(ok[mask] & (wait[mask] <= thr)) / np.count_nonzero(mask)
    return out


def class_sl_table(model: Model, policies: Dict[str, List[int]], n_reps: int = 300) -> pd.DataFrame:
    """
    F6: SL theo gio cua tung nhom khach, cung seed va so lan lap voi evaluate() (so theo cap voi
    so_sanh_chinh_sach.csv). SLA chinh (dung khi toi uu) la SL gop; SL khach thuong va SL VIP chi de giam sat.
    """
    R = scaled(n_reps)
    rows = []
    for name, sched in policies.items():
        jobs = [dict(model=model, schedule=sched, seed=s) for s in common.seed_range("eval", R)]
        mats = np.stack(sim.map_sim(jobs, _post_class_sl, (sched,)))
        for h in range(len(sched)):
            row = {"chinh_sach": name, "lich_quay": str(list(sched)), "gio": h, "khung_gio": H_LABELS[h], "c": sched[h]}
            for k, (key, _) in enumerate(CLASS_SL):
                vals = mats[:, k, h]
                m, half, (low, _) = common.mean_ci(vals[~np.isnan(vals)])
                row.update({f"sl_{key}": m, f"sl_{key}_ci_half": half, f"sl_{key}_ci95_low": low,
                            f"dat_{key}": "Y" if low >= TARGET_SLA else "N"})
            rows.append(row)
    return pd.DataFrame(rows)


def run_optimize(ctx: Dict) -> Dict[str, List[int]]:
    model = ctx["model"]

    print("\n[O.1] Toi uu lich quay 2 pha (mo hinh chinh: phuc vu thuc nghiem)...")
    opt = optimize(model)
    sched_opt = opt["schedule"]
    history_frame(opt["history"]).to_csv(out_path("lich_toi_uu.csv"), index=False, encoding="utf-8-sig")
    print(f"  -> Lich toi uu: {sched_opt} = {sum(sched_opt)} q-h")

    print("[O.2] Pha 3: kiem tra toi thieu cuc bo (swap / giam 2 quay)...")
    pha3 = pd.DataFrame(sim.local_search_phase3(model, sched_opt, n_reps=scaled(60), seed_base=SEED_SELECT))
    pha3.to_csv(out_path("pha3.csv"), index=False, encoding="utf-8-sig")
    n_red = int(((pha3["loai_thu_nghiem"] == "Giam 2 quay") & (pha3["kha_thi"] == "Y")).sum())
    print(f"  -> {len(pha3)} phep thu, {n_red} phep giam 2 quay kha thi")

    print("[O.3] Lich ben vung theo muc du phong nhu cau...")
    rob_rows = []
    sched_rob = None
    for d in [0.05, 0.10, 0.20]:
        s_d = optimize(scale_demand(model, 1.0 + d))["schedule"]
        if abs(d - 0.10) < 1e-9:
            sched_rob = s_d
        a_bar = np.mean(model.rates) * (1.0 + d) * model.mean_svc
        rob_rows.append({
            "delta_du_phong": d,
            "lich_quay": str(s_d),
            "tong_quay_gio": sum(s_d),
            "chenh_lech_quay_gio": sum(s_d) - sum(sched_opt),
            "chi_phi_tang_pct": (sum(s_d) - sum(sched_opt)) / sum(sched_opt) * 100.0,
            "a_trung_binh": a_bar,
            "beta_can_bac_hai": (sum(s_d) / HOURS - a_bar) / np.sqrt(a_bar)
        })
    pd.DataFrame(rob_rows).to_csv(out_path("lich_ben_vung_delta.csv"), index=False, encoding="utf-8-sig")

    sch = save_schedules({"toi_uu": sched_opt, "ben_vung": sched_rob})

    print("[O.4] Xep ca lam viec MILP cho lich toi uu...")
    shifts = run_shifts(sched_opt)
    sched_shift = shifts["Mo hinh B (nghi 11h-14h): chi ca 8h"]
    sch = save_schedules({"theo_ca_8h": sched_shift})

    print("[O.5] So sanh chinh sach (seed danh gia rieng)...")
    policies = {
        "Moc co so 6 quay": sch["moc_co_so"],
        "SIPP (Erlang C)": sch["sipp_erlang_c"],
        "SIPP (Erlang-A)": sch["sipp_erlang_a"],
        "Toi uu mo phong": sched_opt,
        "Ben vung (+10% nhu cau)": sched_rob,
        "Theo ca 8h (MILP)": sched_shift,
    }
    rows = []
    for name, s in policies.items():
        rows.append(sim.summary_row(name, s, evaluate(model, s)))
        print(f"  • {name}: {s} -> SL={rows[-1]['sl_toan_ngay']:.4f}, p_ab={rows[-1]['ti_le_bo_ve']:.4f}")
    pd.DataFrame(rows).to_csv(out_path("so_sanh_chinh_sach.csv"), index=False, encoding="utf-8-sig")

    print("[O.5b] SL theo nhom khach (F6: SLA gop, khach thuong va VIP de giam sat)...")
    class_sl_table(model, policies).to_csv(out_path("sl_theo_nhom.csv"), index=False, encoding="utf-8-sig")

    print("[O.6] So sanh chinh sach co bien dong ngay...")
    cv_d = ctx["params"]["day_cv"]
    rows_bd = []
    for name, s in main_policies(sch).items():
        res = evaluate(model, s, day_cv=cv_d)
        row = sim.summary_row(name, s, res)
        row.update({"cv_ngay": cv_d, "P_SL_ngay_ge90": res["sl_day_ge90_prob"],
                    "P_moi_gio_ge90": res["sl_allhours_ge90_prob"],
                    "so_gio_TB_duoi_90": res["avg_hours_below_90"], "sl_p5": res["sl_p5"]})
        rows_bd.append(row)
    pd.DataFrame(rows_bd).to_csv(out_path("so_sanh_chinh_sach_bd.csv"), index=False, encoding="utf-8-sig")

    print("[O.7] Doi chieu gia dinh xa hang sau 17h (F1)...")
    drain_rows = []
    for policy in sim.DRAIN_POLICIES:
        res = evaluate(model, sched_opt, n_reps=60, drain_policy=policy)
        last = res["hourly"][-1]
        drain_rows.append({"drain_policy": policy, "lich_quay": str(sched_opt), "n_reps": res["n_reps"],
                           "sl_toan_ngay": res["sl_mean"], "sl_gio_cuoi": last["sl_mean"],
                           "sl_gio_cuoi_low": last["sl_ci95_low"], "ti_le_bo_ve": res["p_ab_mean"]})
    pd.DataFrame(drain_rows).to_csv(out_path("doi_chieu_xa_hang.csv"), index=False, encoding="utf-8-sig")
    return sch

def run_shifts(c_req: List[int]) -> Dict[str, List[int]]:
    """Xep ca MILP (b_shifts) cho lich yeu cau theo gio -> lich_theo_ca.csv, fig_b_ca_lam.png."""
    cases = {
        "Mo hinh A: chi ca 8h lien tuc": dict(model_type="A", allow_4h=False),
        "Chi ca 4h": dict(allow_8h=False),
        "Mo hinh B (nghi 11h-14h): chi ca 8h": dict(model_type="B", lunch_window=(3, 5), allow_4h=False),
        "Mo hinh B (nghi 9h-16h): chi ca 8h": dict(model_type="B", lunch_window=(1, 7), allow_4h=False),
        "Mo hinh B (nghi 11h-14h): hon hop 8h+4h": dict(model_type="B", lunch_window=(3, 5)),
        "Mo hinh B (nghi 11h-14h): hon hop 8h+4h, phu dung": dict(model_type="B", lunch_window=(3, 5), exact_coverage=True),
    }
    rows = []
    coverage = {}
    for name, kw in cases.items():
        r = b_shifts.solve_shift_scheduling(c_req, **kw)
        if not r["success"]:
            rows.append({"truong_hop": name, "co_nghiem": "N"})
            continue
        coverage[name] = r["actual_coverage"]
        rows.append({
            "truong_hop": name, "co_nghiem": "Y", "phu_quay": str(r["actual_coverage"]),
            "tong_qh_lam_viec": r["total_work_hours"], "tong_qh_co_mat": r["total_presence_hours"],
            "so_nhan_vien": r["total_staff"], "so_nv_8h": r["n_staff_8h"], "so_nv_4h": r["n_staff_4h"],
            "du_thua_qh": r["waste_work_hours"], "du_thua_pct": r["waste_pct"]
        })
    pd.DataFrame(rows).to_csv(out_path("lich_theo_ca.csv"), index=False, encoding="utf-8-sig")

    x = np.arange(HOURS)
    width = 0.27
    plt.figure(figsize=(9, 5))
    plt.bar(x - width, c_req, width=width, color="#1F4E78", label=f"Yêu cầu tối ưu ({sum(c_req)} q-h)")
    for k, (name, color) in enumerate([("Mo hinh B (nghi 11h-14h): hon hop 8h+4h", "#2CA02C"),
                                       ("Mo hinh B (nghi 11h-14h): chi ca 8h", "#ED7D31")]):
        if name in coverage:
            plt.bar(x + k * width, coverage[name], width=width, color=color,
                    label=f"{name} ({sum(coverage[name])} q-h)")
    plt.xlabel("Khung giờ trong ngày")
    plt.ylabel("Số quầy hoạt động")
    plt.title("Phủ quầy theo ca làm việc so với yêu cầu tối ưu từng giờ")
    plt.xticks(x, H_LABELS)
    plt.legend(fontsize=8)
    plt.grid(True, linestyle="--", axis="y")
    plt.savefig(out_path("fig_b_ca_lam.png", "hinh"), dpi=200, bbox_inches="tight")
    plt.close()
    return coverage
