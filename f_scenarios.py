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
V5:
- M6 (h_staffing) toi uu theo gio cong ca -> toi_uu_theo_ca.csv, toi_uu_theo_ca_top.csv;
  bien the nghi trua 9h-16h -> toi_uu_theo_ca_linh_hoat*.csv
- M7 p_day_levels(): lich nho nhat theo muc P(SL ngay >= 90%) -> toi_uu_xac_suat_ngay.csv
- M8 surge_policies(): mo them quay khi hang cho dai -> chinh_sach_tang_quay.csv;
  recommended_surge() chon chinh sach khuyen nghi
- S12 patience_weibull_scenario(): kien nhan Weibull -> kien_nhan_weibull_fit.csv, kien_nhan_weibull.csv
- S15 half_hour_scenario(): lambda nua gio 8h-10h -> lambda_nua_gio.csv, khung_30_phut.csv
"""

import dataclasses
import math
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from common import (Model, HOURS, H_LABELS, TARGET_SLA, SEED_BANDS, scaled, out_path, empirical_service,
                    weibull_patience)
import a_data
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

def patience_weibull_scenario(ctx: Dict, sch: Dict[str, List[int]]):
    """
    S12: kien nhan Weibull co kiem duyet (fit tren train) thay cho mu. Toi uu lai lich (seed chon
    lich, 60 lan lap) va danh gia Lich 45, Lich 48, lich toi uu Weibull duoi ca hai mo hinh kien nhan
    (seed danh gia, 300 lan lap, cung seed nen so sanh theo cap).
    Tra (bang tham so fit, bang chinh sach).
    """
    fit = a_data.fit_patience_weibull(ctx["df_train"])
    model = ctx["model"]
    model_w = dataclasses.replace(model, patience=weibull_patience(fit["shape"], fit["scale"]))
    sched_w = dx.optimize(model_w)["schedule"]
    print(f"  • S12 Weibull(k={fit['shape']:.3f}, scale={fit['scale']:.2f}): lich toi uu {sched_w} = {sum(sched_w)} q-h")
    pols = {"Lich 45": sch["toi_uu"], "Lich 48": sch["ben_vung"], "Toi uu Weibull": sched_w}
    rows = []
    for m_name, m in (("Mu", model), ("Weibull", model_w)):
        for p_name, sched in pols.items():
            row = sim.summary_row(p_name, sched, dx.evaluate(m, sched))
            row["kien_nhan"] = m_name
            rows.append(row)
    return pd.DataFrame([fit]), pd.DataFrame(rows)


S15_HOURS = (0, 1)  # 8h-9h, 9h-10h theo ke hoach V5


def half_hour_scenario(ctx: Dict, sch: Dict[str, List[int]]):
    """
    S15: lambda theo nua gio o 8h-10h (Model.sub_rates, lich quay van theo gio). Danh gia Lich 45,
    Lich 48 duoi mo hinh theo gio va theo nua gio (seed danh gia, 300 lan lap) va toi uu lai lich.
    Tra (bang lambda nua gio 9 khung, bang chinh sach).
    """
    rates = a_data.half_hour_rates(ctx["df_train"])
    model = ctx["model"]
    sub = [[float(rates.loc[h, "lambda_nua_dau"]), float(rates.loc[h, "lambda_nua_sau"])] if h in S15_HOURS else None
           for h in range(HOURS)]
    model_30 = dataclasses.replace(model, sub_rates=sub)
    sched_30 = dx.optimize(model_30)["schedule"]
    print(f"  • S15 lambda nua gio 8h-10h: lich toi uu {sched_30} = {sum(sched_30)} q-h")
    rows = []
    for m_name, m in (("Theo gio", model), ("Nua gio 8h-10h", model_30)):
        for p_name, sched in {"Lich 45": sch["toi_uu"], "Lich 48": sch["ben_vung"], "Toi uu nua gio": sched_30}.items():
            res = dx.evaluate(m, sched)
            row = sim.summary_row(p_name, sched, res)
            row.update({"mo_hinh_den": m_name, "sl_8h_9h_low": res["hourly"][0]["sl_ci95_low"],
                        "sl_9h_10h_low": res["hourly"][1]["sl_ci95_low"]})
            rows.append(row)
    return rates, pd.DataFrame(rows)


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

# =============================================================================
# HINH V5 (M6, M7, M8)
# =============================================================================
# Mau phan loai co dinh (slot 1-2 bang mau tham chieu, da kiem dinh CVD), chu va luoi trung tinh
C1, C2, INK, INK2, GRID = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e3df"


def _style(ax, xlabel: str, ylabel: str, title: str) -> None:
    ax.set_xlabel(xlabel, color=INK2)
    ax.set_ylabel(ylabel, color=INK2)
    ax.set_title(title, color=INK, loc="left", fontsize=11)
    ax.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(INK2)
    ax.tick_params(colors=INK2)


def fig_m6(trials: pd.DataFrame, trials_flex: pd.DataFrame, best: str) -> None:
    """Can duoi gio te nhat (seed chon lich) cua moi lich phu theo gio cong, hai kieu nghi trua."""
    fig, ax = plt.subplots(figsize=(7, 4.2))
    rng = np.random.default_rng(0)
    x_std = None
    for df, off, color, label in ((trials, -0.7, C1, "Nghỉ trưa 11h–14h"), (trials_flex, 0.7, C2, "Nghỉ trưa 9h–16h")):
        x = df["gio_cong"].to_numpy() + off + rng.uniform(-0.35, 0.35, len(df))
        x_std = x if x_std is None else x_std
        ax.scatter(x, df["sl_gio_te_nhat_low"] * 100, s=22, color=color, alpha=0.75, edgecolor="white",
                   linewidth=0.6, label=f"{label} ({len(df)} lịch)")
    ax.axhline(TARGET_SLA * 100, color=INK2, linestyle="--", linewidth=1)
    ax.text(43.0, TARGET_SLA * 100 + 0.15, "Ngưỡng khả thi 90%", color=INK2, fontsize=8, va="bottom")
    b = np.flatnonzero(trials["phu_quay"].to_numpy() == best)
    if len(b):
        y = float(trials["sl_gio_te_nhat_low"].iloc[b[0]]) * 100
        ax.annotate(f"Lịch 48 {best}", xy=(x_std[b[0]], y), xytext=(44.3, 91.55), fontsize=8, color=INK,
                    arrowprops=dict(arrowstyle="-", color=INK2, linewidth=0.8))
    ax.set_xticks(sorted(set(trials["gio_cong"]) | set(trials_flex["gio_cong"])))
    ax.set_xlim(42.5, 49.5)
    _style(ax, "Giờ công nhân viên/ngày", "SL giờ tệ nhất, cận dưới CI95 (%)",
           "M6: không cách xếp ca nào dưới 48 giờ công đạt SLA")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.savefig(out_path("fig_m6_gio_cong.png", "hinh"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig_m7(p: pd.DataFrame) -> None:
    """Gio cong can thiet theo muc P(SL ngay >= 90%) toi thieu, hai khong gian tim kiem."""
    fig, ax = plt.subplots(figsize=(6, 3.8))
    labelled = set()
    for space, color, label in (("theo ca", C1, "Tìm thẳng theo ca"), ("quay-gio", C2, "Tìm theo quầy-giờ rồi xếp ca")):
        d = p[p["khong_gian"] == space].dropna(subset=["lich"])
        x = d["min_p"].to_numpy() * 100
        ax.plot(x, d["gio_cong_ca"], color=color, linewidth=2, marker="o", markersize=7, label=label)
        for xi, yi in zip(x, d["gio_cong_ca"]):
            if (xi, yi) not in labelled:  # hai duong trung diem: chi ghi mot nhan
                labelled.add((xi, yi))
                ax.text(xi, yi + 0.6, f"{int(yi)}", color=INK, fontsize=8, ha="center")
    ax.set_xticks([80, 90, 95])
    ax.set_xticklabels(["≥ 80%", "≥ 90%", "≥ 95%"])
    ax.set_ylim(44, 55)
    _style(ax, "Tỉ lệ ngày đạt SLA tối thiểu (cận dưới Wilson)", "Giờ công/ngày",
           "M7: giờ công cần thiết theo mức tin cậy")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.savefig(out_path("fig_m7_muc_tin_cay.png", "hinh"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig_m8(m: pd.DataFrame) -> None:
    """Hai bang chung truc doc: quay-gio mo TB (14 ngay) va P(SL ngay >= 90%) co bien dong ngay, moi chinh sach 1 hang."""
    rec = recommended_surge(m)
    d = m.reset_index(drop=True).iloc[::-1]
    labels, colors, bold = [], [], []
    for _, r in d.iterrows():
        if pd.isna(r["nguong_cho"]):
            labels.append(r["chinh_sach"].replace("Lich", "Lịch").replace("co dinh", "cố định"))
            colors.append(C2)
        else:
            labels.append(f"Lịch 45 + mở thêm khi > {int(r['nguong_cho'])} người chờ {int(r['cua_so_phut'])} phút, "
                          f"tối đa +{int(r['quay_du_phong_toi_da'])}")
            colors.append(C1)
        bold.append(rec is not None and r["chinh_sach"] == rec["chinh_sach"])
    y = np.arange(len(d))
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.9), sharey=True, gridspec_kw={"wspace": 0.08})
    panels = ((d["quay_gio_TB_14_ngay"].to_numpy(), "Quầy-giờ mở TB/ngày (14 ngày thực tế)", "{:.2f}"),
              (d["P_SL_ngay_ge90_bien_dong"].to_numpy() * 100, "P(SL ngày ≥ 90%), CV ngày 14% (%)", "{:.1f}%"))
    for ax, (vals, xlabel, fmt) in zip(axes, panels):
        lo = vals.min() - 0.12 * (vals.max() - vals.min())
        ax.hlines(y, lo, vals, color=GRID, linewidth=1.5)
        ax.scatter(vals, y, s=55, color=colors, edgecolor="white", linewidth=1, zorder=3)
        for yi, v in zip(y, vals):
            ax.text(v, yi + 0.28, fmt.format(v), fontsize=8, color=INK, ha="center")
        ax.set_xlim(lo, vals.max() + 0.12 * (vals.max() - vals.min()))
        _style(ax, xlabel, "", "")
        ax.grid(axis="y", visible=False)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels(labels, fontsize=8)
    for t, b in zip(axes[0].get_yticklabels(), bold):
        t.set_fontweight("bold" if b else "normal")
        t.set_color(INK)
    fig.suptitle("M8: mở thêm quầy theo hàng chờ so với lịch cố định (in đậm: khuyến nghị)", x=0.02, ha="left",
                 fontsize=11, color=INK)
    from matplotlib.lines import Line2D
    axes[1].legend(handles=[Line2D([], [], marker="o", linestyle="", color=C2, label="Lịch cố định"),
                            Line2D([], [], marker="o", linestyle="", color=C1, label="Lịch 45 + mở thêm quầy")],
                   frameon=False, fontsize=8, loc="center left")
    fig.savefig(out_path("fig_m8_tang_quay.png", "hinh"), dpi=200, bbox_inches="tight")
    plt.close(fig)


LUNCH_FLEX = (1, 7)  # M6 bien the: nghi trua 1 gio trong 9h-16h


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
    print("[S12] Kien nhan Weibull co kiem duyet...")
    fit, pol_w = patience_weibull_scenario(ctx, sch)
    _save(fit, "kien_nhan_weibull_fit.csv")
    _save(pol_w, "kien_nhan_weibull.csv")
    print("[S15] Lambda theo nua gio 8h-10h...")
    rates30, pol30 = half_hour_scenario(ctx, sch)
    _save(rates30, "lambda_nua_gio.csv")
    _save(pol30, "khung_30_phut.csv")
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
    print("[M6] Bien the nghi trua linh hoat 9h-16h...")
    w_max_f = b_shifts.solve_shift_scheduling(sch["toi_uu"], lunch_window=LUNCH_FLEX)["total_work_hours"]
    m6f = hs.optimize_shift_staffing(model, sch["sipp_erlang_a"], lunch_window=LUNCH_FLEX, slack=0, w_max=w_max_f,
                                     cv_day=ctx["params"]["day_cv"])
    _save(m6f["trials"], "toi_uu_theo_ca_linh_hoat.csv")
    _save(m6f["top"], "toi_uu_theo_ca_linh_hoat_top.csv")
    if len(m6["top"]):
        fig_m6(m6["trials"], m6f["trials"], m6["top"].iloc[0]["phu_quay"])
    print("[M7] Chon lich theo xac suat dat SLA ngay (bien dong ngay)...")
    p7 = p_day_levels(ctx, sch)
    _save(p7, "toi_uu_xac_suat_ngay.csv")
    fig_m7(p7)


SEED_EVAL_DAY, N_EVAL_DAY = SEED_BANDS["eval_day"]  # F5: dai danh gia doc lap voi seed chon lich M7
REF_P_DAY = "doi chieu"                            # khong_gian cua dong Lich 48 doi chieu


def p_day_levels(ctx: Dict, sch: Dict[str, List[int]], levels=(0.80, 0.90, 0.95)) -> pd.DataFrame:
    """
    M7: voi moi muc min_p, lich nho nhat co can duoi Wilson P(SL_ngay >= 90%) >= min_p
    (bien dong ngay CV train), trong khong gian quay-gio va theo ca; xac nhan bang dai seed
    doc lap eval_day (N_EVAL_DAY lan lap, F5) va 14 ngay thuc te. Mot muc chi duoc neu la dat
    khi can duoi Wilson cua lan xac nhan >= min_p (cot dat_muc_danh_gia).
    Them dong doi chieu Lich 48 (sch["ben_vung"]) cung seed xac nhan de so theo cap.
    """
    import e_robustness as er
    model, cv = ctx["model"], ctx["params"]["day_cv"]
    rows, pols = [], {}

    def confirm(lich: List[int]) -> Dict:
        return hs.p_day(model, lich, cv, n_reps=N_EVAL_DAY, seed=SEED_EVAL_DAY)

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
            ev = confirm(lich)
            gc = b_shifts.solve_shift_scheduling(lich)["total_work_hours"]
            pols[f"{space} p>={mp:.2f}"] = lich
            rows.append({"min_p": mp, "khong_gian": space, "lich": str(lich), "quay_gio": sum(lich), "gio_cong_ca": gc,
                         "phuong_an_ca": ca, "P_ngay_danh_gia": ev["p"], "P_ngay_danh_gia_low95": ev["low"],
                         "P_ngay_danh_gia_high95": ev["high"], "dat_muc_danh_gia": "Y" if ev["low"] >= mp else "N"})
    # Doi chieu Lich 48 cung seed xac nhan; them CUOI pols de seed 14 ngay cua cac lich tren khong doi
    lich48 = list(sch["ben_vung"])
    ev = confirm(lich48)
    pols[f"{REF_P_DAY} Lich 48"] = lich48
    rows.append({"min_p": np.nan, "khong_gian": REF_P_DAY, "lich": str(lich48), "quay_gio": sum(lich48),
                 "gio_cong_ca": b_shifts.solve_shift_scheduling(lich48)["total_work_hours"],
                 "phuong_an_ca": "Lich 48", "P_ngay_danh_gia": ev["p"], "P_ngay_danh_gia_low95": ev["low"],
                 "P_ngay_danh_gia_high95": ev["high"], "dat_muc_danh_gia": "-"})
    _, summ = er.fourteen_days(model, ctx["df_all"], pols, ctx["n_day_mean"])
    ok = summ.set_index("chinh_sach")["so_ngay_dat"]
    out = pd.DataFrame(rows)
    out["so_ngay_dat_14"] = [ok.get(f"{REF_P_DAY} Lich 48" if r.khong_gian == REF_P_DAY else f"{r.khong_gian} p>={r.min_p:.2f}")
                             for r in out.itertuples()]
    return out

def run_scenarios_robust(ctx: Dict) -> None:
    """M5 (thuoc giai doan robust)."""
    sch = dx.load_schedules()
    print("[M5] On dinh gio te nhat...")
    need, worst = worst_hour_stability(ctx["model"], {"Toi uu": sch["toi_uu"], "Ben vung (+10%)": sch["ben_vung"]})
    _save(need, "so_lan_lap_can_thiet.csv")
    _save(worst, "gio_te_nhat.csv")
    print("[M8] Tang quay trong ngay theo hang cho...")
    m8 = surge_policies(ctx, sch)
    _save(m8, "chinh_sach_tang_quay.csv")
    fig_m8(m8)


# =============================================================================
# M8: CHINH SACH TANG QUAY TRONG NGAY THEO HANG CHO
# =============================================================================
SEED_M8 = 400000  # dai seed rieng cho M8

def _post_surge(df: pd.DataFrame, sched: List[int]):
    stt = sim.rep_stats(df, sched)
    return stt["sl_all"], [h["sl"] for h in stt["hourly"]], stt["p_ab_all"], df.attrs.get("extra_counter_min", 0.0)


def _eval_surge(model: Model, sched: List[int], surge, n: int, seed: int, day_cv: float = 0.0,
                multipliers=None) -> Dict:
    """Chay n lan lap (hoac moi he so nhan ngay trong multipliers), tra chi so tong hop."""
    if multipliers is None:
        jobs = [dict(model=model, schedule=sched, seed=seed + 1000 * i, day_cv=day_cv, surge_policy=surge) for i in range(n)]
    else:
        jobs = [dict(model=model, schedule=sched, seed=seed + 1000 * i, day_multiplier=m, surge_policy=surge)
                for i, m in enumerate(multipliers)]
    out = sim.map_sim(jobs, _post_surge, (sched,))
    sl_day = np.array([o[0] for o in out])
    hour = np.array([o[1] for o in out])
    t = 1.96 if len(out) > 30 else 2.0
    low = hour.mean(axis=0) - t * hour.std(axis=0, ddof=1) / np.sqrt(len(out))
    return {"sl_day": sl_day, "sl_ngay": float(sl_day.mean()), "gio_te_nhat_low": float(low.min()),
            "p_ab": float(np.mean([o[2] for o in out])), "phut_quay_du_phong": float(np.mean([o[3] for o in out]))}


# Luoi tham so: lan quet tham do (nguong 4-10, cua so 10 phut) gan nhu khong kich hoat (khach bo ve
# lam hang ngan lai); luoi duoi day la vung co tac dung (quet nguong 1-3, cua so 3/5, 1-2 quay).
NGAY10_SVC_FACTOR, NGAY10_FROM_HOUR = 1.29, 6
SURGE_GRID = [(1, 5, 1), (2, 5, 1), (3, 5, 1), (3, 5, 2), (2, 3, 1)]


def surge_policies(ctx: Dict, sch: Dict[str, List[int]], grid=SURGE_GRID, R: int = 300, R14: int = 40) -> pd.DataFrame:
    """
    M8: so sanh Lich 45 + mo them quay khi hang cho dai voi Lich 45 va Lich 48 co dinh.
    Kich ban: danh dinh, bien dong ngay (CV train), nhu cau +10%, E[S] +10%, ngay 10 (E[S] x1.29
    o 14h-17h, Model.service_by_hour), 14 ngay thuc te.
    Quay-gio TB = quay-gio lich + phut-quay du phong / 60.
    """
    model, cv = ctx["model"], ctx["params"]["day_cv"]
    R, R14 = scaled(R), scaled(R14)
    totals = ctx["df_all"].groupby("day").size()
    pols = [("Lich 45 co dinh", sch["toi_uu"], None), ("Lich 48 co dinh", sch["ben_vung"], None)]
    pols += [(f"Lich 45 + tang quay (cho > {t} trong {w} phut, toi da +{e})", sch["toi_uu"],
              {"threshold": t, "window": w, "max_extra": e, "min_hold": 30}) for t, w, e in grid]
    scen = {"danh dinh": (model, 0.0), "bien dong ngay": (model, cv),
            "nhu cau +10%": (dx.scale_demand(model, 1.1), 0.0),
            "E[S] +10%": (dataclasses.replace(model, service=empirical_service(ctx["svc_train"] * 1.1),
                                              mean_svc=model.mean_svc * 1.1), 0.0),
            # Ngay 10 (M4): thoi gian phuc vu cao hon 29% o 14h-17h, cac gio khac nhu train
            "ngay 10": (dataclasses.replace(model, service_by_hour=[None] * NGAY10_FROM_HOUR + [empirical_service(
                ctx["svc_train"] * NGAY10_SVC_FACTOR)] * (HOURS - NGAY10_FROM_HOUR)), 0.0)}
    rows = []
    for name, sched, surge in pols:
        row = {"chinh_sach": name, "lich_quay": str(sched), "quay_gio_lich": sum(sched),
               "nguong_cho": surge["threshold"] if surge else None, "cua_so_phut": surge["window"] if surge else None,
               "quay_du_phong_toi_da": surge["max_extra"] if surge else 0}
        for k, (sname, (m, dcv)) in enumerate(scen.items()):
            r = _eval_surge(m, sched, surge, R, SEED_M8 + 100000 * k, day_cv=dcv)
            row.update({f"SL_{sname}": r["sl_ngay"], f"gio_te_nhat_low_{sname}": r["gio_te_nhat_low"],
                        f"bo_ve_{sname}": r["p_ab"], f"quay_gio_TB_{sname}": sum(sched) + r["phut_quay_du_phong"] / 60.0})
            if dcv > 0:
                row["P_SL_ngay_ge90_bien_dong"] = float(np.mean(r["sl_day"] >= TARGET_SLA))
        ok = 0
        extra14 = []
        for i, (d, n_d) in enumerate(totals.items()):
            r = _eval_surge(model, sched, surge, R14, SEED_M8 + 900000 + 100 * int(d),
                            multipliers=[n_d / ctx["n_day_mean"]] * R14)
            ok += int(r["sl_ngay"] >= TARGET_SLA)
            extra14.append(r["phut_quay_du_phong"])
        row.update({"so_ngay_dat_14": ok, "quay_gio_TB_14_ngay": sum(sched) + float(np.mean(extra14)) / 60.0})
        rows.append(row)
        print(f"  • M8 {name}: SL {row['SL_danh dinh']:.4f}, 14 ngay {ok}/14, q-h TB {row['quay_gio_TB_14_ngay']:.2f}")
    return pd.DataFrame(rows)


def recommended_surge(df: pd.DataFrame) -> Optional[pd.Series]:
    """
    Chinh sach tang quay khuyen nghi tu chinh_sach_tang_quay.csv: it nguoi du phong nhat
    (quay_du_phong_toi_da), roi trong so do P(SL ngay >= 90%) co bien dong ngay >= Lich 48 co dinh
    va dat 14/14 ngay thuc te; chon quay-gio TB 14 ngay nho nhat. None neu khong co chinh sach nao dat.
    """
    ref = df.loc[df["chinh_sach"] == "Lich 48 co dinh", "P_SL_ngay_ge90_bien_dong"]
    cand = df[df["nguong_cho"].notna() & (df["so_ngay_dat_14"] == 14)]
    if len(ref):
        cand = cand[cand["P_SL_ngay_ge90_bien_dong"] >= float(ref.iloc[0])]
    if cand.empty:
        return None
    cand = cand[cand["quay_du_phong_toi_da"] == cand["quay_du_phong_toi_da"].min()]
    return cand.sort_values("quay_gio_TB_14_ngay").iloc[0]
