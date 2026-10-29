"""
f_scenarios.py: Cac kich ban cung co noi dung mo hinh (V4):
- M1 patience_scenarios(): kich ban "quay giao dich that" voi kien nhan trung binh dai hon
  (theta nho) -> do_nhay_kien_nhan.csv, fig_kien_nhan_vs_quay_gio.png
- M2 abandonment_constraint(): toi uu voi rang buoc ti le bo ve toan ngay
  -> toi_uu_rang_buoc_bo_ve.csv, fig_pareto_bo_ve.png
- M3 service_model_comparison(): toi uu voi phuc vu thuc nghiem (mo hinh chinh) vs Gamma
  -> m3_dich_vu_thuc_nghiem.csv
- M5 worst_hour_stability(): so lan lap can thiet de CI SL moi gio <= 0,3 diem %,
  xac suat moi gio la gio te nhat -> gio_te_nhat.csv, so_lan_lap_can_thiet.csv
"""

import dataclasses
import math
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from common import Model, HOURS, H_LABELS, TARGET_SLA, scaled, out_path
import b_theory as th
import c_sim as sim
import d_experiments as dx
import h_staffing as hs
import b_shifts

# =============================================================================
# M1: KICH BAN KIEN NHAN DAI (QUAY GIAO DICH CO LAY SO)
# =============================================================================

def patience_scenarios(model: Model, patience_list: Optional[List[float]] = None) -> pd.DataFrame:
    """
    Voi moi muc kien nhan trung binh (phut), theta = 1 / kien nhan (inf -> theta = 0, Erlang C):
    lich SIPP ly thuyet, lich toi uu mo phong va danh gia 300 lan lap.
    Khi kien nhan -> inf, lich hoi tu ve Erlang C.
    """
    if patience_list is None:
        patience_list = [1.0 / model.theta, 15.0, 20.0, 30.0, 60.0, math.inf]
    mu = 1.0 / model.mean_svc
    rows = []
    for p in patience_list:
        theta = 0.0 if math.isinf(p) else 1.0 / p
        m_p = dataclasses.replace(model, theta=theta)
        sipp = th.sipp_schedule(model.rates, mu, theta, target=TARGET_SLA, use_erlang_a=theta > 0)
        opt = dx.optimize(m_p)["schedule"]
        res = dx.evaluate(m_p, opt)
        label = "Kien nhan vo cung (khong bo ve)" if math.isinf(p) else f"Kien nhan {p:.1f} phut"
        row = sim.summary_row(label, opt, res)
        row.update({"kien_nhan_TB_phut": p, "theta": theta, "lich_sipp": str(sipp),
                    "quay_gio_sipp": sum(sipp), "la_muc_goc": "Y" if abs(theta - model.theta) < 1e-12 else "N"})
        rows.append(row)
        print(f"  • {label}: SIPP {sum(sipp)} q-h, mo phong {opt} = {sum(opt)} q-h, p_ab={res['p_ab_mean']:.4f}")
    df = pd.DataFrame(rows)

    sipp_c = sum(th.sipp_schedule(model.rates, mu, 0.0, target=TARGET_SLA, use_erlang_a=False))
    x_lbl = [("∞" if math.isinf(p) else f"{p:.1f}".rstrip("0").rstrip(".")) for p in df["kien_nhan_TB_phut"]]
    x = np.arange(len(df))
    plt.figure(figsize=(9, 5))
    plt.plot(x, df["quay_gio"], "o-", color="#1F4E78", label="Tối ưu mô phỏng")
    plt.plot(x, df["quay_gio_sipp"], "s--", color="#ED7D31", label="SIPP lý thuyết (Erlang-A)")
    plt.axhline(sipp_c, color="gray", linestyle=":", label=f"Erlang C (không bỏ về) = {sipp_c} q-h")
    for xi, (qh, pab) in enumerate(zip(df["quay_gio"], df["ti_le_bo_ve"])):
        plt.annotate(f"bỏ về {pab * 100:.1f}%", (xi, qh), textcoords="offset points", xytext=(0, 8),
                     ha="center", fontsize=8)
    plt.xticks(x, x_lbl)
    plt.xlabel("Kiên nhẫn trung bình của khách (phút)")
    plt.ylabel("Tổng quầy-giờ/ngày")
    plt.title("Số quầy-giờ cần thiết theo mức kiên nhẫn của khách")
    plt.legend()
    plt.grid(True, linestyle="--")
    plt.savefig(out_path("fig_kien_nhan_vs_quay_gio.png", "hinh"), dpi=200, bbox_inches="tight")
    plt.close()
    return df

# =============================================================================
# M2: RANG BUOC TI LE BO VE
# =============================================================================

def abandonment_constraint(model: Model, caps=(None, 0.05, 0.03, 0.02)) -> pd.DataFrame:
    """Toi uu voi rang buoc can tren CI95 cua ti le bo ve <= cap; kem SL o nguong 2 va 3 phut."""
    rows = []
    for cap in caps:
        opt = dx.optimize(model, max_p_ab=cap)["schedule"]
        res = dx.evaluate(model, opt)
        label = "Chi rang buoc SL" if cap is None else f"SL + bo ve <= {cap * 100:g}%"
        row = sim.summary_row(label, opt, res)
        row["rang_buoc_bo_ve"] = np.nan if cap is None else cap
        rows.append(row)
        print(f"  • {label}: {opt} = {sum(opt)} q-h, p_ab={res['p_ab_mean']:.4f}")
    df = pd.DataFrame(rows)

    fig, ax = plt.subplots(figsize=(8, 5))
    sc = ax.scatter(df["quay_gio"], df["ti_le_bo_ve"] * 100, c=df["sl_toan_ngay"] * 100, cmap="viridis", s=120)
    for _, r in df.iterrows():
        ax.annotate(r["chinh_sach"], (r["quay_gio"], r["ti_le_bo_ve"] * 100), textcoords="offset points",
                    xytext=(6, 6), fontsize=8)
    fig.colorbar(sc, label="SL toàn ngày (%)")
    ax.set_xlabel("Tổng quầy-giờ/ngày")
    ax.set_ylabel("Tỉ lệ khách bỏ về (%)")
    ax.set_title("Đánh đổi quầy-giờ ↔ bỏ về ↔ SL")
    ax.grid(True, linestyle="--")
    fig.savefig(out_path("fig_pareto_bo_ve.png", "hinh"), dpi=200, bbox_inches="tight")
    plt.close(fig)
    return df

# =============================================================================
# M3: PHUC VU THUC NGHIEM (CHINH) VS GAMMA
# =============================================================================

def service_model_comparison(model: Model, model_gamma: Model, sched_emp: List[int]) -> pd.DataFrame:
    """
    Toi uu lai voi Gamma; danh gia ca hai lich duoi ca hai mo hinh phuc vu.
    Mo hinh thuc nghiem duoc coi la gan du lieu nhat (giu dung cs^2 quan sat).
    """
    sched_g = dx.optimize(model_gamma)["schedule"]
    rows = []
    for sched_name, s in [("Lich toi uu (phuc vu thuc nghiem)", sched_emp), ("Lich toi uu (phuc vu Gamma)", sched_g)]:
        for eval_name, m in [("Thuc nghiem", model), ("Gamma", model_gamma)]:
            row = sim.summary_row(sched_name, s, dx.evaluate(m, s))
            row["mo_hinh_danh_gia"] = eval_name
            row["cs2_mo_hinh"] = m.cs2_svc
            rows.append(row)
    dx.save_schedules({"toi_uu_gamma": sched_g})
    return pd.DataFrame(rows)

# =============================================================================
# M5: ON DINH GIO TE NHAT VA SO LAN LAP CAN THIET
# =============================================================================

def worst_hour_stability(model: Model, policies: Dict[str, List[int]], target_hw: float = 0.003,
                         R_cap: int = 3000, block: int = 60, B: int = 1000, seed: int = 100000):
    """
    1. Pilot 300 lan lap -> s_h (do lech chuan SL gio h giua cac lan lap);
       R can thiet = ceil((1,96 s_h / target_hw)^2), gioi han R_cap.
    2. Chay R lan lap (seed rieng), bao cao SL moi gio, CI95, va xac suat moi gio la gio te nhat:
       (a) bootstrap B lan tren cac lan lap, (b) ty le qua cac khoi 'block' lan lap
       (mo phong viec chay lai voi so lan lap nhu khi toi uu).
    """
    rng = np.random.default_rng(seed)
    need_rows, worst_rows = [], []
    for name, s in policies.items():
        pilot = sim.run_reps(model, s, n_reps=scaled(300), seed_base=seed, keep_reps=True)
        s_h = pilot["rep_sl_hourly"].std(axis=0, ddof=1)
        r_need = np.ceil((1.96 * s_h / target_hw) ** 2).astype(int)
        R = scaled(int(min(R_cap, r_need.max())), 30)
        for h in range(HOURS):
            need_rows.append({"chinh_sach": name, "gio": h, "khung_gio": H_LABELS[h], "s_h": float(s_h[h]),
                              "R_can_thiet": int(r_need[h]), "R_su_dung": R})
        res = sim.run_reps(model, s, n_reps=R, seed_base=seed + 500000, keep_reps=True)
        mat = res["rep_sl_hourly"]
        boot = np.zeros(HOURS)
        for _ in range(scaled(B, 100)):
            idx = rng.integers(0, R, size=R)
            boot[np.argmin(mat[idx].mean(axis=0))] += 1
        boot /= boot.sum()
        n_blk = max(1, R // block)
        blk = np.zeros(HOURS)
        for b in range(n_blk):
            blk[np.argmin(mat[b * block:(b + 1) * block].mean(axis=0))] += 1
        blk /= n_blk
        for h, hs in enumerate(res["hourly"]):
            worst_rows.append({"chinh_sach": name, "lich_quay": str(s), "gio": h, "khung_gio": H_LABELS[h],
                               "c": s[h], "n_reps": R, "sl_mean": hs["sl_mean"], "sl_ci_half": hs["sl_ci_half"],
                               "sl_ci95_low": hs["sl_ci95_low"], "P_gio_te_nhat_bootstrap": float(boot[h]),
                               "P_gio_te_nhat_khoi": float(blk[h]), "so_khoi": n_blk})
    return pd.DataFrame(need_rows), pd.DataFrame(worst_rows)

# =============================================================================
# CHAY CAC KICH BAN
# =============================================================================

def _save(df: pd.DataFrame, name: str) -> None:
    df.to_csv(out_path(name), index=False, encoding="utf-8-sig")
    print(f"  -> {name}")

def run_scenarios_optimize(ctx: Dict) -> None:
    """M1, M2, M3 (thuoc giai doan optimize)."""
    model = ctx["model"]
    sch = dx.load_schedules()
    print("[M1] Kich ban kien nhan...")
    _save(patience_scenarios(model), "do_nhay_kien_nhan.csv")
    print("[M2] Rang buoc ti le bo ve...")
    _save(abandonment_constraint(model), "toi_uu_rang_buoc_bo_ve.csv")
    print("[M3] Phuc vu thuc nghiem vs Gamma...")
    _save(service_model_comparison(model, ctx["model_gamma"], sch["toi_uu"]), "m3_dich_vu_thuc_nghiem.csv")
    print("[M6] Toi uu theo gio cong ca (nghi trua 11h-14h)...")
    # slack=0: lan tham do slack=1 (3.180 lich phu, gio cong 36-48) khong co lich kha thi nao
    # co gio thieu quay so voi SIPP Erlang-A (tot nhat 0.8867), xem docs/KE_HOACH_V5.md M6.
    # Can tren gio cong: so gio cong phu lich toi uu quay-gio. Lich phu do co moi gio >= lich toi uu
    # (da kha thi o seed chon lich) nen luon co ung vien kha thi o muc nay (V4: 48).
    w_max = b_shifts.solve_shift_scheduling(sch["toi_uu"])["total_work_hours"]
    m6 = hs.optimize_shift_staffing(model, sch["sipp_erlang_a"], slack=0, w_max=w_max, cv_day=ctx["params"]["day_cv"])
    _save(m6["trials"], "toi_uu_theo_ca.csv")
    _save(m6["top"], "toi_uu_theo_ca_top.csv")
    if len(m6["top"]):
        dx.save_schedules({"toi_uu_theo_ca": eval(m6["top"].iloc[0]["phu_quay"])})
    print("[M7] Chon lich theo xac suat dat SLA ngay (bien dong ngay)...")
    _save(p_day_levels(ctx, sch), "toi_uu_xac_suat_ngay.csv")


def p_day_levels(ctx: Dict, sch: Dict[str, List[int]], levels=(0.80, 0.90, 0.95)) -> pd.DataFrame:
    """
    M7: voi moi muc min_p, lich nho nhat co can duoi Wilson P(SL_ngay >= 90%) >= min_p
    (bien dong ngay CV train), trong khong gian quay-gio va theo ca; danh gia lai bang seed
    danh gia 50000 (300 lan lap) va 14 ngay thuc te.
    """
    import e_robustness as er
    model, cv = ctx["model"], ctx["params"]["day_cv"]
    rows, pols = [], {}
    for mp in levels:
        found = {"quay-gio": (hs.optimize_p_day_counters(model, sch["toi_uu"], cv, mp)["schedule"], ""),
                 "theo ca": None}
        s = hs.optimize_p_day_shifts(model, sch["sipp_erlang_a"], cv, mp)
        found["theo ca"] = (s["lich"], s["phuong_an_ca"])
        for space, (lich, ca) in found.items():
            print(f"  • M7 p>={mp:.2f} {space}: {lich}")
            if lich is None:
                rows.append({"min_p": mp, "khong_gian": space, "lich": None})
                continue
            ev = hs.p_day(model, lich, cv, seed=dx.SEED_EVAL)
            gc = b_shifts.solve_shift_scheduling(lich)["total_work_hours"]
            pols[f"{space} p>={mp:.2f}"] = lich
            rows.append({"min_p": mp, "khong_gian": space, "lich": str(lich), "quay_gio": sum(lich), "gio_cong_ca": gc,
                         "phuong_an_ca": ca, "P_ngay_danh_gia": ev["p"], "P_ngay_danh_gia_low95": ev["low"],
                         "P_ngay_danh_gia_high95": ev["high"]})
    _, summ = er.fourteen_days(model, ctx["df_all"], pols, ctx["n_day_mean"])
    ok = summ.set_index("chinh_sach")["so_ngay_dat"]
    out = pd.DataFrame(rows)
    out["so_ngay_dat_14"] = [ok.get(f"{r.khong_gian} p>={r.min_p:.2f}") for r in out.itertuples()]
    return out

def run_scenarios_robust(ctx: Dict) -> None:
    """M5 (thuoc giai doan robust)."""
    sch = dx.load_schedules()
    print("[M5] On dinh gio te nhat...")
    need, worst = worst_hour_stability(ctx["model"], {"Toi uu": sch["toi_uu"], "Ben vung (+10%)": sch["ben_vung"]})
    _save(need, "so_lan_lap_can_thiet.csv")
    _save(worst, "gio_te_nhat.csv")
