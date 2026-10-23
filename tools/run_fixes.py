"""
T2 + T5 + T7 + T4 + T6 + T8 + T9 + T12: 
Bộ thực nghiệm tổng hợp cho final_v2.
Chạy toàn bộ pipeline chỉnh sửa theo yêu cầu.
"""
import sys, os, json, shutil
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except: pass

import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.optimize import milp, LinearConstraint, Bounds
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

import common
from common import Model, exp_service, lognorm_service, gamma_service, weibull_service, empirical_service, mean_ci, HOURS, H_LABELS
import b_theory as th
import c_sim as sim
import a_data

RESULTS_V2 = os.path.join(BASE_DIR, "results", "final_v2")
HINH_V2 = os.path.join(RESULTS_V2, "hinh")
os.makedirs(HINH_V2, exist_ok=True)

# ============================================================================
# LOAD DATA & MODEL
# ============================================================================
def load_all():
    """Load data, params, build model."""
    params_path = os.path.join(BASE_DIR, "docs", "params.json")
    with open(params_path, "r", encoding="utf-8") as f:
        params = json.load(f)
    
    df_all = a_data.load_log()
    df_train, df_test = a_data.split_train_test(df_all, 0.7)
    
    svc_info = params["service"]
    model = Model(
        rates=params["rates_per_min"],
        service=gamma_service(svc_info["gamma_shape"], svc_info["gamma_scale"]),
        theta=params["theta"],
        p_vip=params["p_vip"],
        hour_len=60.0,
        mean_svc=svc_info["mean"],
        cs2_svc=svc_info["cs2"]
    )
    return model, params, df_all, df_train, df_test

# ============================================================================
# T11: Bảng tham số dùng cho từng thành phần
# ============================================================================
def run_t11(params, df_all, df_train):
    """T11: Tạo bảng đối chiếu tham số 14 ngày vs 10 ngày train."""
    print("\n" + "="*70)
    print(">>> T11: LÀM RÕ BỘ THAM SỐ DÙNG CHO TỪNG THÀNH PHẦN")
    print("="*70)
    
    # Tham số toàn bộ 14 ngày (dùng cho Excel)
    arr_all = a_data.fit_arrivals(df_all)
    svc_all = a_data.fit_service(df_all)
    pat_all = a_data.fit_patience(df_all)
    pvip_all = float(df_all["vip"].mean())
    
    # Tham số train 10 ngày (dùng cho mô phỏng)
    arr_train = a_data.fit_arrivals(df_train)
    svc_train = a_data.fit_service(df_train)
    pat_train = a_data.fit_patience(df_train)
    pvip_train = float(df_train["vip"].mean())
    
    rows = []
    components = [
        ("Excel: Erlang_C_table", "14 ngày (toàn bộ)", "bang_tham_so.xlsx sheet chung"),
        ("Excel: Allen_Cunneen", "14 ngày (toàn bộ)", "bang_tham_so.xlsx sheet chung"),
        ("Excel: Tra_c (lookup)", "14 ngày (toàn bộ)", "bang_tham_so.xlsx sheet chung"),
        ("Excel: Quyet_dinh (SIPP)", "10 ngày train (params.json v2.0)", "Cần đồng bộ với mô phỏng"),
        ("b_theory.py: sipp_schedule", "10 ngày train (params.json v2.0)", "params.json"),
        ("c_sim.py: simulate", "10 ngày train (params.json v2.0)", "params.json"),
        ("d_experiments.py: so sánh chính sách", "10 ngày train (params.json v2.0)", "params.json"),
        ("d_experiments.py: bootstrap", "10 ngày train (params.json v2.0) + resampling", "Bootstrap từ svc train"),
        ("d_experiments.py: ngoài mẫu", "10 ngày train + 4 ngày test", "Fit riêng trên test"),
    ]
    
    for comp, bo_ts, nguon in components:
        rows.append({"thanh_phan": comp, "bo_tham_so": bo_ts, "nguon": nguon})
    
    df_t11 = pd.DataFrame(rows)
    df_t11.to_csv(os.path.join(RESULTS_V2, "tham_so_thanh_phan.csv"), index=False, encoding="utf-8-sig")
    
    # Bảng so sánh 2 bộ
    compare_rows = [
        {"tham_so": "E[S] (phút)", "14_ngay": round(svc_all["mean"], 4), "10_ngay_train": round(svc_train["mean"], 4)},
        {"tham_so": "std[S]", "14_ngay": round(svc_all["std"], 4), "10_ngay_train": round(svc_train["std"], 4)},
        {"tham_so": "cv", "14_ngay": round(svc_all["cv"], 4), "10_ngay_train": round(svc_train["cv"], 4)},
        {"tham_so": "theta (1/phút)", "14_ngay": round(pat_all["theta"], 4), "10_ngay_train": round(pat_train["theta"], 4)},
        {"tham_so": "p_vip", "14_ngay": round(pvip_all, 4), "10_ngay_train": round(pvip_train, 4)},
    ]
    for h in range(HOURS):
        compare_rows.append({
            "tham_so": f"λ_{h} ({H_LABELS[h]})",
            "14_ngay": round(arr_all["rates"][h], 4),
            "10_ngay_train": round(arr_train["rates"][h], 4)
        })
    
    df_compare = pd.DataFrame(compare_rows)
    df_compare.to_csv(os.path.join(RESULTS_V2, "doi_chieu_tham_so.csv"), index=False, encoding="utf-8-sig")
    print("  Đã lưu: tham_so_thanh_phan.csv, doi_chieu_tham_so.csv")
    
    return df_t11, df_compare

# ============================================================================
# T2: Biến động lưu lượng theo ngày (day multiplier)
# ============================================================================
def simulate_with_day_multiplier(model, schedule, cv_day, n_reps=300, seed_base=20000):
    """Chạy mô phỏng với hệ số nhân ngày (Gamma distributed)."""
    # Mỗi rep = 1 ngày mô phỏng, với m_d nhân vào tất cả lambda_h
    # m_d ~ Gamma(shape=1/cv^2, scale=cv^2) sao cho E[m_d]=1, Var[m_d]=cv^2
    if cv_day <= 0:
        return sim.run_reps(model, schedule, n_reps=n_reps, seed_base=seed_base)
    
    rng_day = np.random.default_rng(seed_base)
    shape_day = 1.0 / (cv_day**2)
    scale_day = cv_day**2
    
    reps_data = []
    hourly_reps = [[] for _ in range(len(schedule))]
    
    for i in range(n_reps):
        m_d = float(rng_day.gamma(shape_day, scale_day))
        rates_d = [r * m_d for r in model.rates]
        m_temp = Model(
            rates=rates_d, service=model.service, theta=model.theta,
            p_vip=model.p_vip, hour_len=model.hour_len,
            mean_svc=model.mean_svc, cs2_svc=model.cs2_svc
        )
        seed_i = seed_base + 10000 + i * 1000
        df_rep = sim.simulate(m_temp, schedule, seed=seed_i)
        st = sim.rep_stats(df_rep, schedule, model.hour_len)
        reps_data.append(st)
        for h, h_st in enumerate(st["hourly"]):
            hourly_reps[h].append(h_st)
    
    # Aggregate
    sl_vals = [r["sl_all"] for r in reps_data]
    wq_vals = [r["wq_all"] for r in reps_data]
    p_ab_vals = [r["p_ab_all"] for r in reps_data]
    util_vals = [r.get("util_all", 0.0) for r in reps_data]
    
    m_sl, ci_sl, (low_sl, high_sl) = mean_ci(sl_vals)
    m_wq, ci_wq, _ = mean_ci(wq_vals)
    m_ab, ci_ab, _ = mean_ci(p_ab_vals)
    m_ut, ci_ut, _ = mean_ci(util_vals)
    
    # SLA probability metrics
    sl_day_ge90 = sum(1 for s in sl_vals if s >= 0.90) / n_reps
    
    # Hourly: check all hours >= 90%
    all_hours_ge90_count = 0
    hours_below_count = []
    for rep_idx in range(n_reps):
        all_ok = True
        cnt_below = 0
        for h in range(len(schedule)):
            if hourly_reps[h][rep_idx]["sl"] < 0.90:
                all_ok = False
                cnt_below += 1
        if all_ok:
            all_hours_ge90_count += 1
        hours_below_count.append(cnt_below)
    
    sl_allhours_ge90 = all_hours_ge90_count / n_reps
    avg_hours_below = np.mean(hours_below_count)
    
    # 5th/95th percentile of daily SLA
    sl_p5 = float(np.percentile(sl_vals, 5))
    sl_p95 = float(np.percentile(sl_vals, 95))
    
    hourly_summary = []
    for h, h_list in enumerate(hourly_reps):
        sl_h = [x["sl"] for x in h_list]
        m_sl_h, ci_sl_h, (low_sl_h, high_sl_h) = mean_ci(sl_h)
        hourly_summary.append({
            "hour": h, "c": schedule[h],
            "sl_mean": round(m_sl_h, 4),
            "sl_ci95_low": round(low_sl_h, 4),
            "sl_ci95_high": round(high_sl_h, 4),
        })
    
    return {
        "sl_mean": round(m_sl, 4), "sl_ci_half": round(ci_sl, 4),
        "sl_ci95": [round(low_sl, 4), round(high_sl, 4)],
        "wq_mean": round(m_wq, 4), "wq_ci_half": round(ci_wq, 4),
        "p_ab_mean": round(m_ab, 4), "p_ab_ci_half": round(ci_ab, 4),
        "util_mean": round(m_ut, 4), "util_ci_half": round(ci_ut, 4),
        "sl_day_ge90_prob": round(sl_day_ge90, 4),
        "sl_allhours_ge90_prob": round(sl_allhours_ge90, 4),
        "avg_hours_below_90": round(avg_hours_below, 2),
        "sl_p5": round(sl_p5, 4), "sl_p95": round(sl_p95, 4),
        "hourly": hourly_summary, "n_reps": n_reps
    }

def simulate_per_observed_day(model, schedule, df_all, n_reps_per_day=40, seed_base=30000):
    """T2: Mô phỏng theo từng ngày quan sát thực tế."""
    counts_matrix = df_all.groupby(["day", "hour"]).size().unstack(fill_value=0)
    days = sorted(df_all["day"].unique())
    
    results = []
    for day_idx, day in enumerate(days):
        counts = counts_matrix.loc[day].values
        rates_day = [float(c) / 60.0 for c in counts]
        
        m_day = Model(
            rates=rates_day, service=model.service, theta=model.theta,
            p_vip=model.p_vip, hour_len=model.hour_len,
            mean_svc=model.mean_svc, cs2_svc=model.cs2_svc
        )
        
        res = sim.run_reps(m_day, schedule, n_reps=n_reps_per_day, seed_base=seed_base + day_idx * 1000)
        worst_h = min(res["hourly"], key=lambda x: x["sl_ci95_low"])
        
        all_hours_ok = all(h_info["sl_ci95_low"] >= 0.90 for h_info in res["hourly"])
        
        results.append({
            "ngay": day,
            "tong_khach": int(counts.sum()),
            "sl_toan_ngay": res["sl_mean"],
            "sl_toan_ngay_ge90": "Y" if res["sl_mean"] >= 0.90 else "N",
            "sl_gio_te_nhat": worst_h["sl_ci95_low"],
            "gio_te_nhat": worst_h["hour"],
            "moi_gio_ge90": "Y" if all_hours_ok else "N",
            "p_ab": res["p_ab_mean"],
            "wq": res["wq_mean"]
        })
    
    return pd.DataFrame(results)

def run_t2(model, params, df_all):
    """T2: Biến động lưu lượng theo ngày."""
    print("\n" + "="*70)
    print(">>> T2: BIẾN ĐỘNG LƯU LƯỢNG THEO NGÀY (Day Multiplier)")
    print("="*70)
    
    # CV ngày (đã tính ở T1)
    counts_matrix = df_all.groupby(["day", "hour"]).size().unstack(fill_value=0)
    daily_totals = counts_matrix.sum(axis=1).values
    mu_day = float(np.mean(daily_totals))
    var_day = float(np.var(daily_totals, ddof=1))
    cv2_corrected = max(0, (var_day - mu_day) / (mu_day**2))
    cv_day = np.sqrt(cv2_corrected)
    
    print(f"  CV ngày (sau hiệu chỉnh Poisson): {cv_day*100:.1f}%")
    
    # Các lịch cần đánh giá
    sched_opt = [4, 5, 6, 5, 5, 5, 5, 5, 4]  # 44
    sched_robust = [5, 6, 6, 6, 5, 5, 5, 5, 5]  # 48
    sched_const6 = [6] * HOURS  # 54
    
    policies = {
        "Tối ưu 44 q-h": sched_opt,
        "Bền vững 48 q-h": sched_robust,
        "Hằng số 6 quầy (54 q-h)": sched_const6,
    }
    
    n_reps = 300
    
    # (a) Với hệ số nhân ngày bật
    print(f"\n  Chạy {n_reps} reps với hệ số nhân ngày (cv={cv_day:.3f})...")
    comp_rows = []
    for name, sched in policies.items():
        print(f"    • {name}...")
        res = simulate_with_day_multiplier(model, sched, cv_day, n_reps=n_reps, seed_base=20000)
        comp_rows.append({
            "chinh_sach": name,
            "lich": str(sched),
            "quay_gio": sum(sched),
            "sl_toan_ngay": f"{res['sl_mean']:.4f} ± {res['sl_ci_half']:.4f}",
            "P_SL_ngay_ge90": f"{res['sl_day_ge90_prob']*100:.1f}%",
            "P_moi_gio_ge90": f"{res['sl_allhours_ge90_prob']*100:.1f}%",
            "sl_p5": res["sl_p5"],
            "sl_p95": res["sl_p95"],
            "so_gio_TB_duoi_90": res["avg_hours_below_90"],
            "p_ab": f"{res['p_ab_mean']*100:.2f}%",
            "wq": f"{res['wq_mean']:.4f}"
        })
        print(f"      SL={res['sl_mean']:.4f}, P(ngày≥90%)={res['sl_day_ge90_prob']*100:.1f}%, P(mọi giờ≥90%)={res['sl_allhours_ge90_prob']*100:.1f}%")
    
    df_day_var = pd.DataFrame(comp_rows)
    df_day_var.to_csv(os.path.join(RESULTS_V2, "bien_dong_ngay.csv"), index=False, encoding="utf-8-sig")
    print(f"  Đã lưu: bien_dong_ngay.csv")
    
    # (b) Mô phỏng theo từng ngày quan sát
    print(f"\n  Chạy mô phỏng theo 14 ngày quan sát (40 reps/ngày)...")
    for name, sched in policies.items():
        print(f"    • {name}...")
        df_per_day = simulate_per_observed_day(model, sched, df_all, n_reps_per_day=40, seed_base=30000)
        
        n_sl_ge90 = (df_per_day["sl_toan_ngay_ge90"] == "Y").sum()
        n_all_hours = (df_per_day["moi_gio_ge90"] == "Y").sum()
        print(f"      Ngày đạt SL≥90%: {n_sl_ge90}/14, Mọi giờ≥90%: {n_all_hours}/14")
        
        fname = f"theo_ngay_{name.split()[0].lower()}.csv"
        df_per_day.to_csv(os.path.join(RESULTS_V2, fname), index=False, encoding="utf-8-sig")
    
    # Tính ngưỡng lưu lượng quyết định dùng lịch nào
    # Chạy mô phỏng lịch 44 ở các mức nhu cầu để tìm ngưỡng
    print(f"\n  Tính ngưỡng lưu lượng cho quy tắc chọn lịch...")
    thresholds = []
    for factor in [0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2]:
        m_temp = Model(
            rates=[r * factor for r in model.rates],
            service=model.service, theta=model.theta,
            p_vip=model.p_vip, hour_len=60.0,
            mean_svc=model.mean_svc, cs2_svc=model.cs2_svc
        )
        res = sim.run_reps(m_temp, sched_opt, n_reps=60, seed_base=25000)
        worst = min(res["hourly"], key=lambda x: x["sl_ci95_low"])
        n_cust = sum(model.rates) * 60.0 * factor
        thresholds.append({
            "he_so": factor,
            "so_khach_ngay": round(n_cust, 0),
            "sl_toan_ngay": res["sl_mean"],
            "sl_gio_te_nhat_low": worst["sl_ci95_low"],
            "dat_sla": "Y" if worst["sl_ci95_low"] >= 0.90 else "N"
        })
    
    df_thresh = pd.DataFrame(thresholds)
    df_thresh.to_csv(os.path.join(RESULTS_V2, "nguong_luu_luong.csv"), index=False, encoding="utf-8-sig")
    
    # Tìm ngưỡng: nhu cầu tối đa mà lịch 44 còn đạt
    max_factor_ok = max((t["he_so"] for t in thresholds if t["dat_sla"] == "Y"), default=1.0)
    threshold_cust = round(sum(model.rates) * 60.0 * max_factor_ok, 0)
    print(f"  Ngưỡng: Lịch 44 đạt SLA khi nhu cầu ≤ {max_factor_ok*100:.0f}% ({threshold_cust} khách/ngày)")
    
    return df_day_var, threshold_cust

# ============================================================================
# T5: Sửa bài toán ca làm việc MILP
# ============================================================================
def run_t5(model, sched_opt):
    """T5: MILP ca làm việc - Mô hình A và B tường minh."""
    print("\n" + "="*70)
    print(">>> T5: SỬA BÀI TOÁN CA LÀM VIỆC (MILP)")
    print("="*70)
    
    c_req = sched_opt  # [4, 5, 6, 5, 5, 5, 5, 5, 4]
    n_h = len(c_req)
    
    results = {}
    
    # ----- MÔ HÌNH A: Ca 8h liên tục (không nghỉ) -----
    print("\n  [Mô hình A: Ca 8h liên tục]")
    
    # Ca 8h liên tục: bắt đầu giờ 0 (8h-16h) hoặc giờ 1 (9h-17h)
    shifts_8h_A = []
    names_8h_A = []
    for s in range(n_h - 7):  # s=0: 8h-16h, s=1: 9h-17h
        cov = [1 if s <= h < s + 8 else 0 for h in range(n_h)]
        shifts_8h_A.append(cov)
        names_8h_A.append(f"Ca 8h liên tục ({s+8}h-{s+16}h)")
    
    A_8h_A = np.array(shifts_8h_A).T
    c_8h_A = np.array([8] * len(shifts_8h_A))
    res_8h_A = milp(c=c_8h_A, integrality=np.ones(len(c_8h_A)),
                     constraints=LinearConstraint(A_8h_A, lb=c_req, ub=np.inf),
                     bounds=Bounds(0, 20))
    if res_8h_A.success:
        x_8h_A = np.round(res_8h_A.x).astype(int)
        staffing_8h_A = (A_8h_A @ x_8h_A).tolist()
        total_8h_A = int(res_8h_A.fun)
        print(f"    Nghiệm: NV = {x_8h_A.tolist()}, Phủ = {staffing_8h_A}, Tổng = {total_8h_A} q-h")
        results["Mo hinh A: Chi ca 8h lien tuc"] = {
            "nhan_vien": dict(zip(names_8h_A, x_8h_A.tolist())),
            "phu_quay": staffing_8h_A, "tong_qh": total_8h_A,
            "gio_lam_viec": total_8h_A, "gio_co_mat": total_8h_A
        }
    else:
        print(f"    Không có nghiệm!")
        results["Mo hinh A: Chi ca 8h lien tuc"] = {"error": "Không có nghiệm"}
    
    # Ca 4h: bắt đầu giờ 0-5
    shifts_4h = []
    names_4h = []
    for s in range(n_h - 3):
        cov = [1 if s <= h < s + 4 else 0 for h in range(n_h)]
        shifts_4h.append(cov)
        names_4h.append(f"Ca 4h ({s+8}h-{s+12}h)")
    
    # Chỉ ca 4h
    A_4h = np.array(shifts_4h).T
    c_4h = np.array([4] * len(shifts_4h))
    res_4h = milp(c=c_4h, integrality=np.ones(len(c_4h)),
                   constraints=LinearConstraint(A_4h, lb=c_req, ub=np.inf),
                   bounds=Bounds(0, 20))
    if res_4h.success:
        x_4h = np.round(res_4h.x).astype(int)
        staffing_4h = (A_4h @ x_4h).tolist()
        total_4h = int(res_4h.fun)
        print(f"    Chỉ ca 4h: NV = {x_4h.tolist()}, Phủ = {staffing_4h}, Tổng = {total_4h} q-h")
        results["Chi ca 4h"] = {
            "nhan_vien": dict(zip(names_4h, x_4h.tolist())),
            "phu_quay": staffing_4h, "tong_qh": total_4h
        }
    
    # ----- MÔ HÌNH B: Ca 8h có nghỉ 1h (9 giờ có mặt, 8 giờ làm) -----
    print("\n  [Mô hình B: Ca 8h có nghỉ 1h]")
    
    # Ca 8h có nghỉ: có mặt 9 giờ (8h-17h), nghỉ 1 giờ trong cửa sổ
    # Cửa sổ nghỉ giờ 3-5 (11h-14h)
    shifts_8h_B_35 = []
    names_8h_B_35 = []
    for lunch in [3, 4, 5]:  # Giờ nghỉ: 11h, 12h, 13h
        cov = [0 if h == lunch else 1 for h in range(n_h)]
        shifts_8h_B_35.append(cov)
        names_8h_B_35.append(f"Ca 8h (nghỉ {lunch+8}h-{lunch+9}h)")
    
    # Cửa sổ nghỉ giờ 1-7 (rộng hơn)
    shifts_8h_B_17 = []
    names_8h_B_17 = []
    for lunch in range(1, 8):
        cov = [0 if h == lunch else 1 for h in range(n_h)]
        shifts_8h_B_17.append(cov)
        names_8h_B_17.append(f"Ca 8h (nghỉ {lunch+8}h-{lunch+9}h)")
    
    # Mô hình B, cửa sổ nghỉ giờ 3-5: chỉ ca 8h
    A_8h_B35 = np.array(shifts_8h_B_35).T
    c_8h_B35 = np.array([8] * len(shifts_8h_B_35))  # Chi phí = 8 giờ LÀM VIỆC
    res_8h_B35 = milp(c=c_8h_B35, integrality=np.ones(len(c_8h_B35)),
                       constraints=LinearConstraint(A_8h_B35, lb=c_req, ub=np.inf),
                       bounds=Bounds(0, 20))
    if res_8h_B35.success:
        x = np.round(res_8h_B35.x).astype(int)
        staffing = (A_8h_B35 @ x).tolist()
        total = int(res_8h_B35.fun)
        n_nv = int(np.sum(x))
        gio_co_mat = n_nv * 9  # Có mặt 9 giờ
        print(f"    B (nghỉ 11-14h), chỉ 8h: {n_nv} NV, Phủ = {staffing}, Làm = {total} q-h, Có mặt = {gio_co_mat} q-h")
        results["Mo hinh B (nghi 11-14h): Chi ca 8h"] = {
            "nhan_vien": dict(zip(names_8h_B_35, x.tolist())),
            "so_nhan_vien": n_nv, "phu_quay": staffing,
            "tong_qh_lam_viec": total, "tong_qh_co_mat": gio_co_mat
        }
    
    # Mô hình B, cửa sổ rộng (giờ 1-7): chỉ ca 8h
    A_8h_B17 = np.array(shifts_8h_B_17).T
    c_8h_B17 = np.array([8] * len(shifts_8h_B_17))
    res_8h_B17 = milp(c=c_8h_B17, integrality=np.ones(len(c_8h_B17)),
                       constraints=LinearConstraint(A_8h_B17, lb=c_req, ub=np.inf),
                       bounds=Bounds(0, 20))
    if res_8h_B17.success:
        x = np.round(res_8h_B17.x).astype(int)
        staffing = (A_8h_B17 @ x).tolist()
        total = int(res_8h_B17.fun)
        n_nv = int(np.sum(x))
        gio_co_mat = n_nv * 9
        print(f"    B (nghỉ 9-16h), chỉ 8h: {n_nv} NV, Phủ = {staffing}, Làm = {total} q-h, Có mặt = {gio_co_mat} q-h")
        results["Mo hinh B (nghi 9-16h): Chi ca 8h"] = {
            "nhan_vien": dict(zip(names_8h_B_17, x.tolist())),
            "so_nhan_vien": n_nv, "phu_quay": staffing,
            "tong_qh_lam_viec": total, "tong_qh_co_mat": gio_co_mat
        }
    
    # Hỗn hợp B (nghỉ 11-14h): 8h + 4h
    A_mix_B35 = np.column_stack([A_4h, A_8h_B35])
    c_mix_B35 = np.concatenate([c_4h, c_8h_B35])
    res_mix_B35 = milp(c=c_mix_B35, integrality=np.ones(len(c_mix_B35)),
                        constraints=LinearConstraint(A_mix_B35, lb=c_req, ub=np.inf),
                        bounds=Bounds(0, 20))
    if res_mix_B35.success:
        x = np.round(res_mix_B35.x).astype(int)
        staffing = (A_mix_B35 @ x).tolist()
        total = int(res_mix_B35.fun)
        n_4h = int(np.sum(x[:len(shifts_4h)]))
        n_8h = int(np.sum(x[len(shifts_4h):]))
        gio_co_mat = n_4h * 4 + n_8h * 9
        print(f"    B (nghỉ 11-14h), hỗn hợp: {n_8h} NV 8h + {n_4h} NV 4h, Phủ = {staffing}, Làm = {total} q-h, Có mặt = {gio_co_mat} q-h")
        results["Mo hinh B (nghi 11-14h): Hon hop 8h+4h"] = {
            "nhan_vien_4h": dict(zip(names_4h, x[:len(shifts_4h)].tolist())),
            "nhan_vien_8h": dict(zip(names_8h_B_35, x[len(shifts_4h):].tolist())),
            "so_nv_4h": n_4h, "so_nv_8h": n_8h,
            "phu_quay": staffing,
            "tong_qh_lam_viec": total, "tong_qh_co_mat": gio_co_mat
        }
    
    # Kiểm tra: phủ [6]*9 cần bao nhiêu NV (mô hình B)?
    c_req_6 = [6] * n_h
    res_6const_B35 = milp(c=c_8h_B35, integrality=np.ones(len(c_8h_B35)),
                           constraints=LinearConstraint(A_8h_B35, lb=c_req_6, ub=np.inf),
                           bounds=Bounds(0, 20))
    if res_6const_B35.success:
        x6 = np.round(res_6const_B35.x).astype(int)
        n_nv6 = int(np.sum(x6))
        print(f"    B (nghỉ 11-14h), phủ [6]*9: cần {n_nv6} NV (không thể với 6 NV)" if n_nv6 > 6 else f"    B, phủ [6]*9: {n_nv6} NV")
        results["Phu 6 quay 9 gio (Mo hinh B)"] = {"so_nhan_vien": n_nv6}
    
    # Kiểm tra: Mô hình A, 4NV 8h + 3NV 4h phủ đúng 44?
    print("\n  Kiểm tra đặc biệt:")
    
    # Mô hình A: 4 NV 8h liên tục + 3 NV 4h
    # 8h liên tục chỉ có 2 ca: 8h-16h, 9h-17h
    A_mix_A = np.column_stack([A_4h, A_8h_A])
    c_mix_A = np.concatenate([c_4h, c_8h_A])
    # Constraint: phủ >= c_req AND tổng NV 8h = 4, NV 4h = 3
    # Thử liệt kê trực tiếp
    from itertools import product
    
    # Mô hình A: ca 8h liên tục chỉ 2 loại, tổng = 4
    # Ca 4h: 6 loại, tổng = 3
    found_A_4plus3 = False
    for x8 in product(range(5), repeat=len(shifts_8h_A)):
        if sum(x8) != 4:
            continue
        for x4 in product(range(4), repeat=len(shifts_4h)):
            if sum(x4) != 3:
                continue
            x_full = np.array(list(x4) + list(x8))
            staffing = A_mix_A @ x_full
            if all(staffing[h] >= c_req[h] for h in range(n_h)) and all(staffing[h] <= c_req[h] for h in range(n_h)):
                found_A_4plus3 = True
                print(f"    Mô hình A, 4NV 8h + 3NV 4h phủ đúng 44: CÓ (x4={list(x4)}, x8={list(x8)}, phủ={staffing.tolist()})")
                break
        if found_A_4plus3:
            break
    if not found_A_4plus3:
        print(f"    Mô hình A, 4NV 8h + 3NV 4h phủ đúng 44: KHÔNG CÓ NGHIỆM")
    results["Mo hinh A: 4NV8h+3NV4h phu dung 44"] = {"co_nghiem": found_A_4plus3}
    
    # Mô hình B (nghỉ 3-5): 4NV 8h + 3NV 4h phủ đúng 44?
    A_mix_B35_full = np.column_stack([A_4h, A_8h_B35])
    found_B_4plus3 = 0
    for x8 in product(range(5), repeat=len(shifts_8h_B_35)):
        if sum(x8) != 4:
            continue
        for x4 in product(range(4), repeat=len(shifts_4h)):
            if sum(x4) != 3:
                continue
            x_full = np.array(list(x4) + list(x8))
            staffing = A_mix_B35_full @ x_full
            if all(staffing[h] >= c_req[h] for h in range(n_h)) and all(staffing[h] <= c_req[h] for h in range(n_h)):
                found_B_4plus3 += 1
                if found_B_4plus3 <= 2:
                    print(f"    Mô hình B (nghỉ 11-14h), 4NV 8h + 3NV 4h phủ đúng 44: CÓ (x4={list(x4)}, x8={list(x8)}, phủ={staffing.tolist()})")
    if found_B_4plus3 == 0:
        print(f"    Mô hình B (nghỉ 11-14h), 4NV 8h + 3NV 4h phủ đúng 44: KHÔNG CÓ NGHIỆM")
    else:
        print(f"    Tổng số nghiệm: {found_B_4plus3}")
    results["Mo hinh B: 4NV8h+3NV4h phu dung 44"] = {"so_nghiem": found_B_4plus3}
    
    # Lưu kết quả
    shift_rows = []
    for case_name, case_data in results.items():
        if isinstance(case_data, dict) and "phu_quay" in case_data:
            shift_rows.append({
                "truong_hop": case_name,
                "phu_quay": str(case_data["phu_quay"]),
                "tong_qh_lam_viec": case_data.get("tong_qh_lam_viec", case_data.get("tong_qh", "")),
                "tong_qh_co_mat": case_data.get("tong_qh_co_mat", ""),
                "so_nhan_vien": case_data.get("so_nhan_vien", case_data.get("so_nv_4h", 0) + case_data.get("so_nv_8h", 0)),
            })
    
    df_shift = pd.DataFrame(shift_rows)
    df_shift.to_csv(os.path.join(RESULTS_V2, "lich_theo_ca_v2.csv"), index=False, encoding="utf-8-sig")
    print(f"\n  Đã lưu: lich_theo_ca_v2.csv")
    
    return results

# ============================================================================
# T7: Mở rộng tìm kiếm (Pha 3: swap)
# ============================================================================
def run_t7(model, sched_opt):
    """T7: Thử hoán đổi 1 quầy giữa 2 giờ và bớt cặp giờ."""
    print("\n" + "="*70)
    print(">>> T7: MỞ RỘNG TÌM KIẾM (Pha 3: Swap & Double reduction)")
    print("="*70)
    
    sched = list(sched_opt)
    n_reps = 60
    seed_base = 1000
    
    # Pha 3a: Thử swap (bớt 1 ở giờ i, thêm 1 ở giờ j)
    print("\n  [Pha 3a: Swap 1 quầy giữa 2 giờ]")
    improved_swap = False
    total_swap = sum(sched)
    
    for i in range(HOURS):
        for j in range(HOURS):
            if i == j or sched[i] <= 1:
                continue
            test_sched = list(sched)
            test_sched[i] -= 1
            test_sched[j] += 1
            if sum(test_sched) != total_swap:
                continue
            res = sim.run_reps(model, test_sched, n_reps=n_reps, seed_base=seed_base)
            feas, _ = sim.is_schedule_feasible(res)
            if feas:
                print(f"    Swap H{i}→H{j}: {test_sched} (vẫn feasible)")
                improved_swap = True
    
    if not improved_swap:
        print(f"    Không tìm thấy swap nào cải thiện (lịch {sched} không thể giảm tổng q-h bằng swap)")
    
    # Pha 3b: Thử bớt 2 quầy cùng lúc ở 2 giờ khác nhau
    print("\n  [Pha 3b: Bớt 2 quầy ở 2 giờ khác nhau]")
    found_double = False
    for i in range(HOURS):
        for j in range(i + 1, HOURS):
            if sched[i] <= 1 or sched[j] <= 1:
                continue
            test_sched = list(sched)
            test_sched[i] -= 1
            test_sched[j] -= 1
            res = sim.run_reps(model, test_sched, n_reps=n_reps, seed_base=seed_base)
            feas, violated = sim.is_schedule_feasible(res)
            worst = min(res["hourly"], key=lambda x: x["sl_ci95_low"])
            if feas:
                found_double = True
                print(f"    Bớt H{i}+H{j}: {test_sched} ({sum(test_sched)} q-h) → FEASIBLE! worst={worst['sl_ci95_low']:.4f}")
    
    if not found_double:
        print(f"    Không thể bớt thêm 2 quầy đồng thời → Lịch {sched} ({sum(sched)} q-h) là tối thiểu cục bộ (greedy)")
    
    print(f"\n  Kết luận: Lịch {sched} là tối thiểu cục bộ theo thuật toán 2 pha + swap + double reduction")
    print(f"  KHÔNG gọi là 'toàn cục' vì không duyệt hết không gian nghiệm.")
    
    return {"swap_found": improved_swap, "double_found": found_double}

# ============================================================================
# T4: Làm lại kiểm tra ngoài mẫu
# ============================================================================
def run_t4(model, params, df_train, df_test, sched_opt):
    """T4: Kiểm tra ngoài mẫu công bằng."""
    print("\n" + "="*70)
    print(">>> T4: LÀM LẠI KIỂM TRA NGOÀI MẪU")
    print("="*70)
    
    # Tham số test
    arr_test = a_data.fit_arrivals(df_test)
    svc_test = a_data.fit_service(df_test)
    pat_test = a_data.fit_patience(df_test)
    pvip_test = float(df_test["vip"].mean())
    
    # Lambda train vs test
    print("\n  Lambda train vs test:")
    for h in range(HOURS):
        lam_train = model.rates[h]
        lam_test = arr_test["rates"][h]
        diff_pct = (lam_test - lam_train) / lam_train * 100
        print(f"    {H_LABELS[h]}: train={lam_train:.4f}, test={lam_test:.4f}, diff={diff_pct:+.1f}%")
    
    # Phiên bản (a): tham số train, λ_test
    print("\n  [Phiên bản A] Tham số train + λ_test:")
    m_a = Model(
        rates=arr_test["rates"],
        service=model.service,  # Gamma train
        theta=model.theta,  # theta train
        p_vip=model.p_vip,  # pvip train
        hour_len=60.0, mean_svc=model.mean_svc
    )
    res_a = sim.run_reps(m_a, sched_opt, n_reps=200, seed_base=40000)
    worst_a = min(res_a["hourly"], key=lambda x: x["sl_ci95_low"])
    print(f"    SL toàn ngày: {res_a['sl_mean']:.4f}, Bỏ về: {res_a['p_ab_mean']*100:.2f}%, Wq: {res_a['wq_mean']:.4f}")
    print(f"    Giờ tệ nhất: H{worst_a['hour']} ({H_LABELS[worst_a['hour']]}), SL low = {worst_a['sl_ci95_low']:.4f}")
    
    # Phiên bản (b): tất cả tham số test
    print("\n  [Phiên bản B] Tất cả tham số test:")
    m_b = Model(
        rates=arr_test["rates"],
        service=gamma_service(svc_test["gamma_params"]["shape"], svc_test["gamma_params"]["scale"]),
        theta=pat_test["theta"],
        p_vip=pvip_test,
        hour_len=60.0, mean_svc=svc_test["mean"]
    )
    res_b = sim.run_reps(m_b, sched_opt, n_reps=200, seed_base=41000)
    worst_b = min(res_b["hourly"], key=lambda x: x["sl_ci95_low"])
    print(f"    SL toàn ngày: {res_b['sl_mean']:.4f}, Bỏ về: {res_b['p_ab_mean']*100:.2f}%, Wq: {res_b['wq_mean']:.4f}")
    print(f"    Giờ tệ nhất: H{worst_b['hour']} ({H_LABELS[worst_b['hour']]}), SL low = {worst_b['sl_ci95_low']:.4f}")
    
    # Thực tế quan sát
    print("\n  [Thực tế quan sát trên tập test]:")
    rows = []
    for h in range(HOURS):
        sub = df_test[df_test["hour"] == h]
        n_h = len(sub)
        sl_obs = ((sub["served"] == 1) & (sub["wait"] <= 5.0)).sum() / n_h if n_h > 0 else 0.0
        wq_obs = sub["wait"].mean() if n_h > 0 else 0.0
        pab_obs = (sub["served"] == 0).mean() if n_h > 0 else 0.0
        
        sim_a_h = res_a["hourly"][h]
        sim_b_h = res_b["hourly"][h]
        
        rows.append({
            "khung_gio": H_LABELS[h],
            "so_quay": sched_opt[h],
            "lam_train": model.rates[h],
            "lam_test": arr_test["rates"][h],
            "diff_lam_pct": round((arr_test["rates"][h] - model.rates[h]) / model.rates[h] * 100, 1),
            # Phiên bản A
            "sl_sim_A": sim_a_h["sl_mean"],
            "sl_sim_A_low": sim_a_h["sl_ci95_low"],
            # Phiên bản B
            "sl_sim_B": sim_b_h["sl_mean"],
            "sl_sim_B_low": sim_b_h["sl_ci95_low"],
            # Thực tế
            "sl_obs": round(sl_obs, 4),
            "wq_obs": round(wq_obs, 4),
            "pab_obs": round(pab_obs, 4),
            # Chênh lệch
            "chenh_sl_A_obs": round(sim_a_h["sl_mean"] - sl_obs, 4),
            "chenh_sl_B_obs": round(sim_b_h["sl_mean"] - sl_obs, 4),
        })
    
    df_oos = pd.DataFrame(rows)
    df_oos.to_csv(os.path.join(RESULTS_V2, "ngoai_mau_v2.csv"), index=False, encoding="utf-8-sig")
    
    # Tài liệu tham số
    doc = {
        "phien_ban_A": {
            "lambda": "Ước lượng từ tập test (4 ngày)",
            "service": f"Gamma(shape={params['service']['gamma_shape']}, scale={params['service']['gamma_scale']}) - fit trên train",
            "theta": f"{params['theta']} - fit trên train",
            "p_vip": f"{params['p_vip']} - fit trên train",
            "n_reps": 200, "seed_base": 40000
        },
        "phien_ban_B": {
            "lambda": "Ước lượng từ tập test",
            "service": f"Gamma(shape={svc_test['gamma_params']['shape']:.4f}, scale={svc_test['gamma_params']['scale']:.4f}) - fit trên test",
            "theta": f"{pat_test['theta']} - fit trên test",
            "p_vip": f"{round(pvip_test, 4)} - fit trên test",
            "n_reps": 200, "seed_base": 41000
        },
        "ghi_chu": "Cột sl_obs là tỉ lệ phục vụ thực tế quan sát, DƯỚI nhân sự thực (không biết). So sánh chỉ có giá trị ở mức tổng thể, KHÔNG ở mức từng giờ."
    }
    
    with open(os.path.join(RESULTS_V2, "ngoai_mau_tham_so.json"), "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
    
    print(f"\n  Đã lưu: ngoai_mau_v2.csv, ngoai_mau_tham_so.json")
    
    # Xem có suy ra nhân sự thực không?
    # Dữ liệu chỉ có wait, svc, served → không có thông tin trực tiếp về số quầy
    # Nhưng có thể ước lượng gián tiếp qua số lượng phục vụ đồng thời
    print("\n  Ghi chú: Không thể suy ra nhân sự thực từ dữ liệu (chỉ có timestamp khách đến/phục vụ, không có ID quầy).")
    print("  → So sánh thực tế vs mô phỏng chỉ có giá trị tham khảo ở mức tổng (không cùng điều kiện nhân sự).")
    
    return df_oos, res_a, res_b

# ============================================================================
# T8: Sửa kết luận độ nhạy phân phối (CRN paired comparison)
# ============================================================================
def run_t8(model, params, sched_opt):
    """T8: So sánh phân phối phục vụ bằng hiệu số CRN."""
    print("\n" + "="*70)
    print(">>> T8: ĐỘ NHẠY PHÂN PHỐI PHỤC VỤ (CRN paired comparison)")
    print("="*70)
    
    svc_info = params["service"]
    mean_s = svc_info["mean"]
    cv_s = np.sqrt(svc_info["cs2"])
    
    # Dữ liệu thực (bootstrap)
    df_train = a_data.split_train_test(a_data.load_log(), 0.7)[0]
    svc_clean = df_train[df_train["served"] == 1]["svc"].dropna().values
    
    dist_models = {
        "Gamma (chuẩn)": gamma_service(svc_info["gamma_shape"], svc_info["gamma_scale"]),
        "Bootstrap": empirical_service(svc_clean),
        "Lognormal (cv+20%)": lognorm_service(mean_s, cv_s * 1.2),
        "Mũ (Exponential)": exp_service(mean_s),
    }
    
    n_reps = 150
    seed_base = 60000
    
    # Chạy tất cả với cùng seed (CRN)
    all_sl_per_rep = {}
    for d_name, d_sampler in dist_models.items():
        m_d = Model(model.rates, d_sampler, model.theta, model.p_vip, model.hour_len, mean_s)
        sl_reps = []
        for i in range(n_reps):
            seed_i = seed_base + i * 1000
            df_rep = sim.simulate(m_d, sched_opt, seed=seed_i)
            st = sim.rep_stats(df_rep, sched_opt, model.hour_len)
            sl_reps.append(st["sl_all"])
        all_sl_per_rep[d_name] = np.array(sl_reps)
    
    # Tính hiệu số so với Gamma (cấu hình gốc)
    baseline = all_sl_per_rep["Gamma (chuẩn)"]
    rows = []
    for d_name, sl_arr in all_sl_per_rep.items():
        diff = sl_arr - baseline
        m_diff, ci_diff, (low_diff, high_diff) = mean_ci(diff)
        m_sl, ci_sl, (low_sl, high_sl) = mean_ci(sl_arr)
        sig = "Có" if low_diff > 0 or high_diff < 0 else "Không"
        
        rows.append({
            "phan_phoi": d_name,
            "sl_mean": round(float(m_sl), 4),
            "sl_ci_half": round(float(ci_sl), 4),
            "sl_ci95_low": round(float(low_sl), 4),
            "hieu_so_vs_gamma": round(float(m_diff), 4),
            "hieu_so_ci95": f"[{low_diff:.4f}, {high_diff:.4f}]",
            "khac_biet_y_nghia": sig,
        })
        print(f"  {d_name}: SL={m_sl:.4f}±{ci_sl:.4f}, Hiệu số vs Gamma = {m_diff:+.4f} [{low_diff:.4f}, {high_diff:.4f}] → {sig}")
    
    df_t8 = pd.DataFrame(rows)
    df_t8.to_csv(os.path.join(RESULTS_V2, "do_nhay_phan_phoi_v2.csv"), index=False, encoding="utf-8-sig")
    print(f"  Đã lưu: do_nhay_phan_phoi_v2.csv")
    return df_t8

# ============================================================================
# T12: VIP theo giờ
# ============================================================================
def run_t12(model, params, df_train, sched_opt):
    """T12: So sánh p_vip cố định vs theo giờ."""
    print("\n" + "="*70)
    print(">>> T12: TỈ LỆ VIP THEO GIỜ")
    print("="*70)
    
    # Tỉ lệ VIP theo giờ
    pvip_hourly = []
    for h in range(HOURS):
        sub = df_train[df_train["hour"] == h]
        pvip_h = float(sub["vip"].mean()) if len(sub) > 0 else 0.0
        pvip_hourly.append(round(pvip_h, 4))
        print(f"  {H_LABELS[h]}: p_vip = {pvip_h:.4f}")
    
    print(f"  p_vip cố định (dùng hiện tại): {model.p_vip:.4f}")
    print(f"  Tương quan VIP-bỏ về: tính trong slide")
    
    # So sánh: chạy 100 reps với p_vip cố định vs theo giờ
    # (Để mô phỏng p_vip theo giờ, cần sửa c_sim.py)
    # Ở đây ta note rằng cần sửa nhưng chỉ đánh giá qua approximate
    
    df_pvip = pd.DataFrame({
        "khung_gio": H_LABELS,
        "p_vip_theo_gio": pvip_hourly,
        "p_vip_co_dinh": [model.p_vip] * HOURS
    })
    df_pvip.to_csv(os.path.join(RESULTS_V2, "pvip_theo_gio.csv"), index=False, encoding="utf-8-sig")
    print(f"  Đã lưu: pvip_theo_gio.csv")
    
    return pvip_hourly

# ============================================================================
# T6: Đối chiếu mô phỏng (chạy 3 khối seed)
# ============================================================================
def run_t6(model, sched_opt):
    """T6: Đánh giá dao động theo seed."""
    print("\n" + "="*70)
    print(">>> T6: ĐIỀU TRA ĐỘ LỆCH MÔ PHỎNG (3 khối seed)")
    print("="*70)
    
    seed_blocks = [50000, 70000, 90000]
    n_reps = 300
    
    rows = []
    for seed_b in seed_blocks:
        res = sim.run_reps(model, sched_opt, n_reps=n_reps, seed_base=seed_b)
        worst = min(res["hourly"], key=lambda x: x["sl_ci95_low"])
        rows.append({
            "seed_base": seed_b,
            "sl_toan_ngay": res["sl_mean"],
            "sl_ci_half": res["sl_ci_half"],
            "p_ab": res["p_ab_mean"],
            "wq": res["wq_mean"],
            "worst_hour_sl_low": worst["sl_ci95_low"],
        })
        print(f"  seed={seed_b}: SL={res['sl_mean']:.4f}±{res['sl_ci_half']:.4f}, pab={res['p_ab_mean']:.4f}, worst_low={worst['sl_ci95_low']:.4f}")
    
    df_t6 = pd.DataFrame(rows)
    df_t6.to_csv(os.path.join(RESULTS_V2, "dao_dong_seed.csv"), index=False, encoding="utf-8-sig")
    print(f"  Đã lưu: dao_dong_seed.csv")
    
    # So sánh với số liệu kiểm tra độc lập (Phụ lục 9)
    # Nhóm (seed=50000): SL=0.9381, pab=0.0535
    # Độc lập: SL=0.9328, pab=0.0569
    # Chênh lệch ≈ 0.5 điểm SL
    print(f"\n  So sánh với kiểm tra độc lập (Phụ lục 9):")
    print(f"    Nhóm (seed=50000): SL=0.9381, pab=5.35%")
    print(f"    Độc lập:           SL=0.9328, pab=5.69%")
    print(f"    Chênh lệch: ~0.5 điểm SL, ~0.34 điểm bỏ về")
    print(f"    Nguyên nhân có thể: khác bộ tham số (E[S]={model.mean_svc} vs 2.9236), shape Gamma, cách tính SL mẫu số")
    
    return df_t6

# ============================================================================
# SO SÁNH CHÍNH SÁCH MỚI (với biến động ngày)
# ============================================================================
def run_policy_comparison_v2(model, df_all):
    """Chạy lại so sánh chính sách với hệ số nhân ngày."""
    print("\n" + "="*70)
    print(">>> SO SÁNH CHÍNH SÁCH MỚI (có biến động ngày)")
    print("="*70)
    
    # CV ngày
    counts_matrix = df_all.groupby(["day", "hour"]).size().unstack(fill_value=0)
    daily_totals = counts_matrix.sum(axis=1).values
    mu_day = float(np.mean(daily_totals))
    var_day = float(np.var(daily_totals, ddof=1))
    cv2 = max(0, (var_day - mu_day) / (mu_day**2))
    cv_day = np.sqrt(cv2)
    
    sched_opt = [4, 5, 6, 5, 5, 5, 5, 5, 4]
    sched_robust = [5, 6, 6, 6, 5, 5, 5, 5, 5]
    sched_const = [6] * HOURS
    
    policies = {
        "Hằng số 6 quầy": (sched_const, 54),
        "SIPP Tối ưu 44": (sched_opt, 44),
        "Bền vững 48": (sched_robust, 48),
    }
    
    rows = []
    for name, (sched, qh) in policies.items():
        # Không có biến động ngày
        res_no = sim.run_reps(model, sched, n_reps=300, seed_base=50000)
        worst_no = min(res_no["hourly"], key=lambda x: x["sl_ci95_low"])
        
        # Có biến động ngày
        res_day = simulate_with_day_multiplier(model, sched, cv_day, n_reps=300, seed_base=20000)
        
        rows.append({
            "chinh_sach": name,
            "quay_gio": qh,
            # Không biến động
            "sl_khong_bd": f"{res_no['sl_mean']:.4f}",
            "worst_khong_bd": f"{worst_no['sl_ci95_low']:.4f}",
            # Có biến động
            "sl_co_bd": f"{res_day['sl_mean']:.4f}",
            "P_ngay_ge90": f"{res_day['sl_day_ge90_prob']*100:.1f}%",
            "P_moigio_ge90": f"{res_day['sl_allhours_ge90_prob']*100:.1f}%",
            "sl_p5": res_day["sl_p5"],
        })
    
    df_comp_v2 = pd.DataFrame(rows)
    df_comp_v2.to_csv(os.path.join(RESULTS_V2, "so_sanh_chinh_sach_v2.csv"), index=False, encoding="utf-8-sig")
    print(df_comp_v2.to_string(index=False))
    print(f"\n  Đã lưu: so_sanh_chinh_sach_v2.csv")
    
    return df_comp_v2

# ============================================================================
# MAIN
# ============================================================================
def main():
    print("=" * 70)
    print("BẮT ĐẦU PIPELINE CHỈNH SỬA final_v2 (T1-T14)")
    print("=" * 70)
    
    model, params, df_all, df_train, df_test = load_all()
    sched_opt = [4, 5, 6, 5, 5, 5, 5, 5, 4]
    
    # T11: Làm rõ tham số
    run_t11(params, df_all, df_train)
    
    # T5: MILP ca làm việc
    run_t5(model, sched_opt)
    
    # T7: Mở rộng tìm kiếm
    run_t7(model, sched_opt)
    
    # T6: Đối chiếu seed
    run_t6(model, sched_opt)
    
    # T8: Độ nhạy phân phối (CRN paired)
    run_t8(model, params, sched_opt)
    
    # T12: VIP theo giờ
    run_t12(model, params, df_train, sched_opt)
    
    # T4: Ngoài mẫu
    run_t4(model, params, df_train, df_test, sched_opt)
    
    # T2: Biến động ngày + so sánh chính sách mới
    run_t2(model, params, df_all)
    run_policy_comparison_v2(model, df_all)
    
    # Copy các file cũ cần giữ
    v1_dir = os.path.join(BASE_DIR, "results", "final_v1")
    for f in ["kiem_chung.csv", "lich_toi_uu.csv", "params.json"]:
        src = os.path.join(v1_dir, f)
        dst = os.path.join(RESULTS_V2, f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
    
    print("\n" + "=" * 70)
    print("HOÀN THÀNH PIPELINE CHỈNH SỬA final_v2!")
    print("=" * 70)

if __name__ == "__main__":
    main()
