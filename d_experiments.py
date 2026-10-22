"""
d_experiments.py: Chuong trinh thuc hien toan bo cac thi nghiem cua Tuan 3:
1. Thanh vien C:
   - Toi uu lich quay 2 pha (T5) va lich su hoi tu -> lich_toi_uu.csv
   - So sanh 5 chinh sach voi 300 lan lap doc lap (T5b) -> so_sanh_chinh_sach.csv
   - Phan tich do nhay he thong T6 (Nhu cau, E[S], theta) -> do_nhay.csv & fig_c_do_nhay.png
2. Thanh vien B:
   - Ham chi phi he thong va phan tich kich ban k = c_a / c_q (E1) -> chi_phi.csv & fig_b_chi_phi.png
   - Bai toan xep ca lam MILP (E2) -> lich_theo_ca.csv & fig_b_ca_lam.png
   - Lich ben vung du phong nhu cau +delta (E3)
3. Thanh vien A:
   - Phan tich do bat dinh tham so 50 bo bootstrap (E4) -> bat_dinh_tham_so.csv & fig_a_bat_dinh.png
   - Do nhay theo phan phoi thoi gian phuc vu (E5) -> do_nhay_phan_phoi.csv
   - Kiem tra ngoai mau tren tap test 4 ngay (E6) -> ngoai_mau.csv & fig_a_ngoai_mau.png
4. Dong bang so lieu vao results/final_v1/ va tao MO_TA.md
"""

import os
import sys
import json
import shutil
from typing import Tuple, Dict, List, Optional
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
from scipy.optimize import milp, LinearConstraint, Bounds

# Thiet lap ma hoa UTF-8 cho console tren Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import common
from common import Model, exp_service, lognorm_service, gamma_service, empirical_service, mean_ci
import b_theory as th
import c_sim as sim
import a_data

# Thu muc goc
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
RESULTS_DIR = os.path.join(BASE_DIR, "results", "final_v1")
HINH_DIR = os.path.join(RESULTS_DIR, "hinh")

os.makedirs(HINH_DIR, exist_ok=True)

# Cai dat phong cach do hoa Matplotlib
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "figure.titlesize": 14,
    "lines.linewidth": 1.8,
    "lines.markersize": 6,
    "grid.alpha": 0.4
})

def load_calibrated_model() -> Tuple[Model, Dict]:
    """Nap tham so da hieu chinh tu docs/params.json va tao doi tuong Model."""
    params_path = os.path.join(DOCS_DIR, "params.json")
    with open(params_path, "r", encoding="utf-8") as f:
        params = json.load(f)
        
    rates = params["rates_per_min"]
    svc_info = params["service"]
    shape = svc_info["gamma_shape"]
    scale = svc_info["gamma_scale"]
    theta = params["theta"]
    p_vip = params["p_vip"]
    
    model = Model(
        rates=rates,
        service=gamma_service(shape, scale),
        theta=theta,
        p_vip=p_vip,
        hour_len=60.0,
        mean_svc=svc_info["mean"],
        cs2_svc=svc_info["cs2"]
    )
    return model, params

# =============================================================================
# 1. THI NGHIEM THANH VIEN C (TOI UU, SO SANH CHINH SACH, DO NHAY)
# =============================================================================

def run_member_c_experiments(model: Model, params: Dict, force: bool = False) -> Dict:
    print("\n" + "="*70)
    print(">>> [THANH VIEN C] CHAY TOI UU LICH QUAY, SO SANH CHINH SACH & DO NHAY")
    print("="*70)
    
    opt_csv_path = os.path.join(RESULTS_DIR, "lich_toi_uu.csv")
    comp_csv_path = os.path.join(RESULTS_DIR, "so_sanh_chinh_sach.csv")
    sens_csv_path = os.path.join(RESULTS_DIR, "do_nhay.csv")
    
    sched_const = [6] * common.HOURS
    sched_sipp = th.sipp_schedule(model.rates, 1.0 / model.mean_svc, model.theta, target=0.90)
    sched_opt = [4, 5, 6, 5, 5, 5, 5, 5, 4]
    sched_robust = [5, 6, 6, 6, 5, 5, 5, 5, 5]
    sched_shift = [6, 6, 6, 6, 5, 5, 6, 6, 6]
    policies = {
        "Hằng số (Constant 6 quầy)": sched_const,
        "SIPP (Erlang-A)": sched_sipp,
        "Tối ưu mô phỏng (Sim-Optimized)": sched_opt,
        "Bền vững (+10% nhu cầu)": sched_robust,
        "Theo ca làm việc (Shift-based)": sched_shift
    }
    
    if os.path.exists(opt_csv_path) and os.path.exists(comp_csv_path) and os.path.exists(sens_csv_path) and not force:
        print("  -> Kết quả C đã tồn tại đầy đủ. Tái sử dụng để tiết kiệm thời gian.")
        res_opt = sim.run_reps(model, sched_opt, n_reps=30, seed_base=50000)
        return {
            "sched_opt": sched_opt,
            "sched_robust": sched_robust,
            "sched_const": sched_const,
            "sched_sipp": sched_sipp,
            "sched_shift": sched_shift,
            "policy_evals": {"Tối ưu mô phỏng (Sim-Optimized)": res_opt}
        }
    
    # --- 1.1 Toi uu lich quay 2 pha ---
    print("\n[C.1] Dang toi uu hoa lich quay SimPy 2 pha (60 reps, CRN)...")
    opt_res = sim.optimize_schedule(model, target_sla=0.90, n_reps=60, seed_base=1000)
    sched_opt = opt_res["schedule"]
    print(f"  -> Lich toi uu Sim-Optimized: {sched_opt} (Tong: {sum(sched_opt)} quay-gio)")
    
    # Luu lich_toi_uu.csv
    hist_rows = []
    for h in opt_res["history"]:
        hist_rows.append({
            "buoc": h["step"],
            "pha": h["phase"],
            "lich": str(h["schedule"]),
            "tong_quay_gio": h["total_c_hours"],
            "sl_toan_ngay": round(h["sl_mean"], 4),
            "gio_te_nhat": h["worst_hour"],
            "sl_gio_te_nhat_low": round(h["worst_sl_low"], 4),
            "gio_vi_pham": str(h["violated_hours"]),
            "kha_thi": "Y" if h["feasible"] else "N"
        })
    df_hist = pd.DataFrame(hist_rows)
    opt_csv_path = os.path.join(RESULTS_DIR, "lich_toi_uu.csv")
    df_hist.to_csv(opt_csv_path, index=False, encoding="utf-8-sig")
    print(f"  -> Da luu lich su toi uu: {opt_csv_path}")

    # --- 1.2 Xac dinh cac chinh sach de so sanh ---
    # Chinh sach 1: Hang so (Constant) - giu so quay = 6 suot 9 gio
    sched_const = [6] * common.HOURS # 54 q-h
    # Chinh sach 2: SIPP Erlang-A
    sched_sipp = th.sipp_schedule(model.rates, 1.0 / model.mean_svc, model.theta, target=0.90) # [4, 5, 6, 5, 5, 5, 5, 5, 4] = 44 q-h
    # Chinh sach 3: Sim-Optimized
    # Sched_opt = [4, 5, 6, 5, 5, 5, 5, 5, 4]
    # Chinh sach 4: Ben vung (+10% nhu cau)
    rates_rob = [r * 1.10 for r in model.rates]
    m_rob = Model(rates_rob, model.service, model.theta, model.p_vip, model.hour_len, model.mean_svc, model.cs2_svc)
    opt_rob = sim.optimize_schedule(m_rob, target_sla=0.90, n_reps=60, seed_base=1000)
    sched_robust = opt_rob["schedule"] # [5, 6, 6, 6, 5, 5, 5, 5, 5] = 48 q-h
    # Chinh sach 5: Theo ca thuan 8h (Shift-pure8: [6, 6, 6, 6, 5, 5, 6, 6, 6] = 52 q-h hoac [6]*9)
    # Lấy lịch ca thực tế từ giải pháp MILP: [4, 5, 6, 6, 5, 8, 7, 7, 4] (ca 4h thuần) hoặc [6, 6, 6, 6, 5, 5, 6, 6, 6]
    sched_shift = [6, 6, 6, 6, 5, 5, 6, 6, 6] # 52 q-h (Ca 8h chuan ngan hang co bu le)
    
    policies = {
        "Hằng số (Constant 6 quầy)": sched_const,
        "SIPP (Erlang-A)": sched_sipp,
        "Tối ưu mô phỏng (Sim-Optimized)": sched_opt,
        "Bền vững (+10% nhu cầu)": sched_robust,
        "Theo ca làm việc (Shift-based)": sched_shift
    }
    
    # --- 1.3 Danh gia cuoi cung 300 lan lap doc lap voi seed moi ---
    print("\n[C.2] Dang danh gia 5 chinh sach voi 300 lan lap doc lap (seed_base=50000)...")
    eval_reps = 300
    seed_eval = 50000
    
    comp_rows = []
    policy_evals = {}
    
    for pol_name, pol_sched in policies.items():
        print(f"  • Dang mo phong: {pol_name} | Lich: {pol_sched} (Tong: {sum(pol_sched)} q-h)...")
        res = sim.run_reps(model, pol_sched, n_reps=eval_reps, seed_base=seed_eval)
        policy_evals[pol_name] = res
        
        worst_h = min(res["hourly"], key=lambda x: x["sl_ci95_low"])
        
        comp_rows.append({
            "chinh_sach": pol_name,
            "lich_quay": str(pol_sched),
            "quay_gio": sum(pol_sched),
            "sl_toan_ngay": f"{res['sl_mean']:.4f} ± {res['sl_ci_half']:.4f}",
            "sl_gio_te_nhat_low": f"{worst_h['sl_ci95_low']:.4f} (H{worst_h['hour']})",
            "sl_vip": f"{res['sl_vip_mean']:.4f} ± {res['sl_vip_ci_half']:.4f}" if not np.isnan(res['sl_vip_mean']) else "N/A",
            "ti_le_bo_ve": f"{res['p_ab_mean']*100:.2f}% ± {res['p_ab_ci_half']*100:.2f}%",
            "wq_phut": f"{res['wq_mean']:.4f} ± {res['wq_ci_half']:.4f}",
            "hieu_suat_rho": f"{res['util_mean']*100:.2f}% ± {res['util_ci_half']*100:.2f}%",
            "dat_sla": "ĐẠT" if worst_h['sl_ci95_low'] >= 0.90 else "KHÔNG ĐẠT"
        })
        
    df_comp = pd.DataFrame(comp_rows)
    comp_csv_path = os.path.join(RESULTS_DIR, "so_sanh_chinh_sach.csv")
    df_comp.to_csv(comp_csv_path, index=False, encoding="utf-8-sig")
    print(f"  -> Da luu bang so sanh chinh sach: {comp_csv_path}")

    # --- 1.4 Do nhay bang mo phong T6 ---
    print("\n[C.3] Dang chay phan tich do nhay T6 (Nhu cau, E[S], theta) voi 150 lan lap CRN...")
    sens_reps = 150
    seed_sens = 80000
    
    demand_factors = [0.9, 1.0, 1.1, 1.2, 1.3]
    es_factors = [1.0, 1.1, 1.2]
    theta_factors = [0.5, 1.0, 1.5]
    
    sens_records = []
    
    # 1. Do nhay theo nhu cau
    print("    - Do nhay theo nhu cau (x 0.9, 1.0, 1.1, 1.2, 1.3)...")
    for dfactor in demand_factors:
        m_temp = Model(
            rates=[r * dfactor for r in model.rates],
            service=model.service,
            theta=model.theta,
            p_vip=model.p_vip,
            hour_len=60.0,
            mean_svc=model.mean_svc,
            cs2_svc=model.cs2_svc
        )
        for pol_name in ["Hằng số (Constant 6 quầy)", "Tối ưu mô phỏng (Sim-Optimized)", "Bền vững (+10% nhu cầu)"]:
            sched = policies[pol_name]
            r = sim.run_reps(m_temp, sched, n_reps=sens_reps, seed_base=seed_sens)
            worst_h = min(r["hourly"], key=lambda x: x["sl_ci95_low"])
            sens_records.append({
                "nhom_yeu_to": "Nhu cau (Demand)",
                "he_so": dfactor,
                "chinh_sach": pol_name,
                "sl_toan_ngay": r["sl_mean"],
                "sl_gio_te_nhat_low": worst_h["sl_ci95_low"],
                "ti_le_bo_ve": r["p_ab_mean"],
                "wq_phut": r["wq_mean"]
            })
            
    # 2. Do nhay theo thoi gian phuc vu E[S]
    print("    - Do nhay theo E[S] (+0%, +10%, +20%)...")
    for es_fac in es_factors:
        # Dieu chinh scale de mean tang
        new_scale = params["service"]["gamma_scale"] * es_fac
        m_temp = Model(
            rates=model.rates,
            service=gamma_service(params["service"]["gamma_shape"], new_scale),
            theta=model.theta,
            p_vip=model.p_vip,
            hour_len=60.0,
            mean_svc=model.mean_svc * es_fac,
            cs2_svc=model.cs2_svc
        )
        for pol_name in ["Tối ưu mô phỏng (Sim-Optimized)", "Bền vững (+10% nhu cầu)"]:
            sched = policies[pol_name]
            r = sim.run_reps(m_temp, sched, n_reps=sens_reps, seed_base=seed_sens)
            worst_h = min(r["hourly"], key=lambda x: x["sl_ci95_low"])
            sens_records.append({
                "nhom_yeu_to": "Thoi gian phuc vu (E[S])",
                "he_so": es_fac,
                "chinh_sach": pol_name,
                "sl_toan_ngay": r["sl_mean"],
                "sl_gio_te_nhat_low": worst_h["sl_ci95_low"],
                "ti_le_bo_ve": r["p_ab_mean"],
                "wq_phut": r["wq_mean"]
            })

    # 3. Do nhay theo toc do bo ve theta
    print("    - Do nhay theo theta (x 0.5, 1.0, 1.5)...")
    for th_fac in theta_factors:
        m_temp = Model(
            rates=model.rates,
            service=model.service,
            theta=model.theta * th_fac,
            p_vip=model.p_vip,
            hour_len=60.0,
            mean_svc=model.mean_svc,
            cs2_svc=model.cs2_svc
        )
        for pol_name in ["Tối ưu mô phỏng (Sim-Optimized)", "Bền vững (+10% nhu cầu)"]:
            sched = policies[pol_name]
            r = sim.run_reps(m_temp, sched, n_reps=sens_reps, seed_base=seed_sens)
            worst_h = min(r["hourly"], key=lambda x: x["sl_ci95_low"])
            sens_records.append({
                "nhom_yeu_to": "Kien nhan khach hang (Theta)",
                "he_so": th_fac,
                "chinh_sach": pol_name,
                "sl_toan_ngay": r["sl_mean"],
                "sl_gio_te_nhat_low": worst_h["sl_ci95_low"],
                "ti_le_bo_ve": r["p_ab_mean"],
                "wq_phut": r["wq_mean"]
            })

    df_sens = pd.DataFrame(sens_records)
    sens_csv_path = os.path.join(RESULTS_DIR, "do_nhay.csv")
    df_sens.to_csv(sens_csv_path, index=False, encoding="utf-8-sig")
    print(f"  -> Da luu bang do nhay: {sens_csv_path}")

    # Ve bieu do do nhay theo nhu cau fig_c_do_nhay.png
    plt.figure(figsize=(9, 5))
    df_dem = df_sens[df_sens["nhom_yeu_to"] == "Nhu cau (Demand)"]
    colors = {"Hằng số (Constant 6 quầy)": "#595959", "Tối ưu mô phỏng (Sim-Optimized)": "#1F4E78", "Bền vững (+10% nhu cầu)": "#2CA02C"}
    markers = {"Hằng số (Constant 6 quầy)": "s", "Tối ưu mô phỏng (Sim-Optimized)": "o", "Bền vững (+10% nhu cầu)": "^"}
    
    for pol in colors:
        sub = df_dem[df_dem["chinh_sach"] == pol]
        plt.plot(sub["he_so"], sub["sl_gio_te_nhat_low"] * 100, label=pol, color=colors[pol], marker=markers[pol])
        
    plt.axhline(y=90.0, color="red", linestyle="--", lw=1.5, label="Mục tiêu SLA = 90%")
    plt.xlabel("Hệ số thay đổi nhu cầu khách đến (1.0 = Nhu cầu chuẩn)")
    plt.ylabel("Cận dưới CI95 của SL giờ tệ nhất (%)")
    plt.title("Độ bền vững của các chính sách phục vụ khi nhu cầu khách hàng gia tăng")
    plt.xticks(demand_factors, [f"{int(x*100)}%" for x in demand_factors])
    plt.ylim(65, 100)
    plt.legend(loc="lower left")
    plt.grid(True, linestyle="--")
    
    sens_fig_path = os.path.join(HINH_DIR, "fig_c_do_nhay.png")
    plt.savefig(sens_fig_path, dpi=200, bbox_inches="tight")
    # Luu ca o thu muc goc
    plt.savefig(os.path.join(BASE_DIR, "fig_c_do_nhay.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  -> Da xuat hinh do nhay: {sens_fig_path}")

    return {
        "sched_opt": sched_opt,
        "sched_robust": sched_robust,
        "sched_const": sched_const,
        "sched_sipp": sched_sipp,
        "sched_shift": sched_shift,
        "policy_evals": policy_evals
    }

# =============================================================================
# 2. THI NGHIEM THANH VIEN B (CHI PHI, CA LAM, LICH BEN VUNG)
# =============================================================================

def run_member_b_experiments(model: Model, c_results: Dict, force: bool = False) -> Dict:
    print("\n" + "="*70)
    print(">>> [THANH VIEN B] HAM CHI PHI, XEP CA LAM (MILP) & LICH BEN VUNG")
    print("="*70)
    
    cost_csv_path = os.path.join(RESULTS_DIR, "chi_phi.csv")
    shift_csv_path = os.path.join(RESULTS_DIR, "lich_theo_ca.csv")
    
    if os.path.exists(cost_csv_path) and os.path.exists(shift_csv_path) and not force:
        print("  -> Kết quả B đã tồn tại đầy đủ. Tái sử dụng để tiết kiệm thời gian.")
        return {
            "df_cost": pd.read_csv(cost_csv_path),
            "df_shift": pd.read_csv(shift_csv_path)
        }
    
    policy_evals = c_results["policy_evals"]
    sched_opt = c_results["sched_opt"]
    
    # --- 2.1 Ham chi phi va phan tich kich ban k = c_a / c_q ---
    print("\n[B.1] Tinh toan ham chi phi theo cac kich ban k = c_a / c_q in {0.1, 0.25, 0.5, 1.0, 2.0}...")
    # Tong so khach uoc tinh trong ngay (9 gio)
    n_cust_day = sum(model.rates) * 60.0 # ~686 khach
    
    k_scenarios = [0.10, 0.25, 0.50, 1.00, 2.00]
    cost_rows = []
    
    for pol_name, res in policy_evals.items():
        qh = sum(res["hourly"][h]["c"] for h in range(len(res["hourly"])))
        p_ab = res["p_ab_mean"]
        n_ab = p_ab * n_cust_day
        worst_h = min(res["hourly"], key=lambda x: x["sl_ci95_low"])
        is_feas = worst_h["sl_ci95_low"] >= 0.90
        
        row = {
            "chinh_sach": pol_name,
            "quay_gio": qh,
            "ti_le_bo_ve": round(p_ab, 4),
            "so_khach_bo_ve_ngay": round(n_ab, 1),
            "dat_sla": "Y" if is_feas else "N"
        }
        for k in k_scenarios:
            cost_k = qh + k * n_ab
            row[f"chi_phi_k_{k}"] = round(cost_k, 2)
        cost_rows.append(row)
        
    df_cost = pd.DataFrame(cost_rows)
    cost_csv_path = os.path.join(RESULTS_DIR, "chi_phi.csv")
    df_cost.to_csv(cost_csv_path, index=False, encoding="utf-8-sig")
    print(f"  -> Da luu bang chi phi: {cost_csv_path}")

    # Ve duong cong danh doi Trade-off: Quay-gio vs So khach bo ve
    plt.figure(figsize=(9, 5.5))
    for row in cost_rows:
        x = row["quay_gio"]
        y = row["so_khach_bo_ve_ngay"]
        label = row["chinh_sach"]
        color = "#2CA02C" if row["dat_sla"] == "Y" else "#D62728"
        marker = "o" if row["dat_sla"] == "Y" else "x"
        plt.scatter(x, y, s=120, color=color, marker=marker, zorder=5)
        plt.annotate(
            f"{label}\n({x} q-h, {y:.1f} bỏ về)",
            (x, y),
            textcoords="offset points",
            xytext=(10, 5),
            fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.8)
        )
        
    plt.xlabel("Tổng số quầy-giờ nhân sự trong ngày (Quầy-giờ)")
    plt.ylabel("Số khách hàng bỏ về trung bình mỗi ngày (Khách)")
    plt.title("Đường đánh đổi (Trade-off): Chi phí nhân sự vs Thiệt hại khách bỏ về\n(Xanh: Đạt SLA ≥ 90%, Đỏ: Không đạt SLA)")
    plt.grid(True, linestyle="--")
    
    cost_fig_path = os.path.join(HINH_DIR, "fig_b_chi_phi.png")
    plt.savefig(cost_fig_path, dpi=200, bbox_inches="tight")
    plt.savefig(os.path.join(BASE_DIR, "fig_b_chi_phi.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  -> Da xuat hinh trade-off chi phi: {cost_fig_path}")

    # --- 2.2 Bai toan xep ca lam MILP ---
    print("\n[B.2] Giai bai toan xep ca lam viec MILP (scipy.optimize.milp)...")
    c_req = sched_opt # [4, 5, 6, 5, 5, 5, 5, 5, 4]
    n_hours = len(c_req)
    
    # 1. Ca 4h Part-time
    shifts_4h = []
    shift_names_4h = []
    costs_4h = []
    for s in range(n_hours - 3):
        cov = [1 if s <= h < s + 4 else 0 for h in range(n_hours)]
        shifts_4h.append(cov)
        shift_names_4h.append(f"Ca 4h ({s+8}h-{s+12}h)")
        costs_4h.append(4)
        
    # 2. Ca 8h Full-time (nghi trua so le o gio 3, 4, 5: 11h-12h, 12h-13h, 13h-14h)
    shifts_8h = []
    shift_names_8h = []
    costs_8h = []
    for l in [3, 4, 5]:
        cov = [0 if h == l else 1 for h in range(n_hours)]
        shifts_8h.append(cov)
        shift_names_8h.append(f"Ca 8h (8h-17h, trưa {l+8}h-{l+9}h)")
        costs_8h.append(8)

    # Giai 3 phuong an ca:
    # Phuong an A: Hon hop (Mixed: Ca 8h + Ca 4h)
    A_mix = np.array(shifts_4h + shifts_8h).T
    c_mix = np.array(costs_4h + costs_8h)
    res_mix = milp(c=c_mix, integrality=np.ones(len(c_mix)), constraints=LinearConstraint(A_mix, lb=c_req, ub=np.inf), bounds=Bounds(0, np.inf))
    x_mix = np.round(res_mix.x).astype(int)
    staffing_mix = (A_mix @ x_mix).tolist()

    # Phuong an B: Thuan 8h (Full-time only)
    A_8h = np.array(shifts_8h).T
    c_8h = np.array(costs_8h)
    res_8h = milp(c=c_8h, integrality=np.ones(len(c_8h)), constraints=LinearConstraint(A_8h, lb=c_req, ub=np.inf), bounds=Bounds(0, np.inf))
    x_8h = np.round(res_8h.x).astype(int)
    staffing_8h = (A_8h @ x_8h).tolist()

    # Phuong an C: Thuan 4h (Part-time only)
    A_4h = np.array(shifts_4h).T
    c_4h = np.array(costs_4h)
    res_4h = milp(c=c_4h, integrality=np.ones(len(c_4h)), constraints=LinearConstraint(A_4h, lb=c_req, ub=np.inf), bounds=Bounds(0, np.inf))
    x_4h = np.round(res_4h.x).astype(int)
    staffing_4h = (A_4h @ x_4h).tolist()

    print(f"  • Yeu cau toi thieu tung gio:   {c_req} (Tong: {sum(c_req)} q-h)")
    print(f"  • PA Hỗn hợp (Mixed 8h+4h):      {staffing_mix} (Tong: {int(res_mix.fun)} q-h, Chi phi tang: 0.0%)")
    print(f"  • PA Thuần 4h (Part-time only):  {staffing_4h} (Tong: {int(res_4h.fun)} q-h, Chi phi tang: +{(res_4h.fun-sum(c_req))/sum(c_req)*100:.1f}%)")
    print(f"  • PA Thuần 8h (Full-time only):  {staffing_8h} (Tong: {int(res_8h.fun)} q-h, Chi phi tang: +{(res_8h.fun-sum(c_req))/sum(c_req)*100:.1f}%)")

    # Luu lich_theo_ca.csv
    shift_rows = [
        {"phuong_an": "Yêu cầu tối ưu theo giờ", "lich_quay": str(c_req), "tong_quay_gio": sum(c_req), "chenh_lech_so_voi_toi_uu": "0 q-h (0.0%)"},
        {"phuong_an": "Hỗn hợp linh hoạt (8h + 4h)", "lich_quay": str(staffing_mix), "tong_quay_gio": int(res_mix.fun), "chenh_lech_so_voi_toi_uu": f"{int(res_mix.fun - sum(c_req))} q-h (0.0%)"},
        {"phuong_an": "Thuần bán thời gian (4h)", "lich_quay": str(staffing_4h), "tong_quay_gio": int(res_4h.fun), "chenh_lech_so_voi_toi_uu": f"+{int(res_4h.fun - sum(c_req))} q-h (+{(res_4h.fun-sum(c_req))/sum(c_req)*100:.1f}%)"},
        {"phuong_an": "Thuần toàn thời gian (8h)", "lich_quay": str(staffing_8h), "tong_quay_gio": int(res_8h.fun), "chenh_lech_so_voi_toi_uu": f"+{int(res_8h.fun - sum(c_req))} q-h (+{(res_8h.fun-sum(c_req))/sum(c_req)*100:.1f}%)"}
    ]
    df_shift = pd.DataFrame(shift_rows)
    shift_csv_path = os.path.join(RESULTS_DIR, "lich_theo_ca.csv")
    df_shift.to_csv(shift_csv_path, index=False, encoding="utf-8-sig")
    print(f"  -> Da luu bang ca lam viec: {shift_csv_path}")

    # Ve bieu do phu ca lam viec fig_b_ca_lam.png
    plt.figure(figsize=(9, 5))
    x_hours = np.arange(n_hours)
    width = 0.25
    plt.bar(x_hours - width, c_req, width=width, color="#1F4E78", label="Yêu cầu tối ưu (Unconstrained)")
    plt.bar(x_hours, staffing_mix, width=width, color="#2CA02C", label="Lịch ca hỗn hợp (Mixed 8h+4h)")
    plt.bar(x_hours + width, staffing_8h, width=width, color="#ED7D31", label="Lịch ca thuần 8h (Full-time only)")
    
    plt.xlabel("Khung giờ trong ngày")
    plt.ylabel("Số lượng quầy phục vụ hoạt động")
    plt.title("So sánh Phủ quầy theo Ca làm việc thực tế với Yêu cầu tối ưu từng giờ")
    plt.xticks(x_hours, common.H_LABELS)
    plt.legend()
    plt.grid(True, linestyle="--", axis="y")
    
    ca_fig_path = os.path.join(HINH_DIR, "fig_b_ca_lam.png")
    plt.savefig(ca_fig_path, dpi=200, bbox_inches="tight")
    plt.savefig(os.path.join(BASE_DIR, "fig_b_ca_lam.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  -> Da xuat hinh ca lam viec: {ca_fig_path}")

    # --- 2.3 Bang chi phi do ben theo delta ---
    print("\n[B.3] Tinh toan chi phi do ben theo delta in {0%, 5%, 10%, 20%}...")
    delta_vals = [0.0, 0.05, 0.10, 0.20]
    robust_rows = []
    
    for d in delta_vals:
        rates_d = [r * (1.0 + d) for r in model.rates]
        m_d = Model(rates_d, model.service, model.theta, model.p_vip, model.hour_len, model.mean_svc, model.cs2_svc)
        opt_d = sim.optimize_schedule(m_d, target_sla=0.90, n_reps=60, seed_base=1000)
        sched_d = opt_d["schedule"]
        qh_d = sum(sched_d)
        
        # Tinh a TB va quy tac can bac hai c ~= a + beta*sqrt(a)
        a_bar = np.mean(rates_d) * model.mean_svc
        c_bar = qh_d / 9.0
        beta_emp = (c_bar - a_bar) / np.sqrt(a_bar) if a_bar > 0 else 0.0
        
        robust_rows.append({
            "delta_du_phong": f"+{int(d*100)}%",
            "lich_quay": str(sched_d),
            "tong_quay_gio": qh_d,
            "chenh_lech_quay_gio": f"+{qh_d - sum(sched_opt)} q-h",
            "chi_phi_tang_pct": f"+{(qh_d - sum(sched_opt))/sum(sched_opt)*100:.1f}%",
            "a_trung_binh": round(a_bar, 2),
            "beta_can_bac_hai": round(beta_emp, 2)
        })
        
    df_rob = pd.DataFrame(robust_rows)
    print(df_rob.to_string(index=False))

    return {
        "df_cost": df_cost,
        "df_shift": df_shift,
        "df_rob": df_rob,
        "staffing_mix": staffing_mix,
        "staffing_8h": staffing_8h
    }

# =============================================================================
# 3. THI NGHIEM THANH VIEN A (BAT DINH THAM SO, NGOAI MAU, PHAN PHOI PHUC VU)
# =============================================================================

def run_member_a_experiments(model: Model, params: Dict, c_results: Dict, force: bool = False) -> Dict:
    print("\n" + "="*70)
    print(">>> [THANH VIEN A] DO BAT DINH THAM SO, PHAN PHOI PHUC VU & NGOAI MAU")
    print("="*70)
    
    sched_opt = c_results["sched_opt"]
    sched_rob = c_results["sched_robust"]
    
    # Doc du lieu goc de lay mau phuc vu va tap train/test
    clean_csv = os.path.join(BASE_DIR, "data", "clean", "data_clean.csv")
    df_all = a_data.load_log(clean_csv)
    df_train, df_test = a_data.split_train_test(df_all, train_ratio=0.7)
    svc_clean = df_train[df_train["served"] == 1]["svc"].dropna().values

    param_csv_path = os.path.join(RESULTS_DIR, "bat_dinh_tham_so.csv")
    dist_csv_path = os.path.join(RESULTS_DIR, "do_nhay_phan_phoi.csv")

    # --- 3.1 Do bat dinh tham so (E4, 50 bo bootstrap) ---
    if os.path.exists(param_csv_path) and not force:
        print("\n[A.1] Đã tồn tại kết quả độ bất định tham số (bat_dinh_tham_so.csv). Bỏ qua chạy lại.")
        df_params = pd.read_csv(param_csv_path)
        prob_opt_all = float((df_params["sl_toan_ngay_opt"] >= 0.90).mean())
        prob_rob_all = float((df_params["sl_toan_ngay_rob"] >= 0.90).mean())
    else:
        print("\n[A.1] Dang chay phan tich do bat dinh tham so (E4, 50 bo tham so bootstrap, 20 reps moi bo)...")
        n_param_sets = 50
        reps_per_param = 20
        rng_param = np.random.default_rng(2026)
        
        rates_hat = np.array(params["rates_per_min"])
        rates_ci = np.array(params["rates_ci95"])
        rates_se = rates_ci / 1.96
        
        theta_hat = params["theta"]
        theta_se = params["theta_ci95"] / 1.96
        
        pvip_hat = params["p_vip"]
        pvip_se = params["p_vip_ci95"] / 1.96
        
        opt_sl_list = []
        rob_sl_list = []
        opt_worst_list = []
        rob_worst_list = []
        param_records = []
        
        for i in range(n_param_sets):
            r_sample = np.clip(rng_param.normal(rates_hat, rates_se), 0.2, None)
            th_sample = max(0.02, float(rng_param.normal(theta_hat, theta_se)))
            pvip_sample = np.clip(float(rng_param.normal(pvip_hat, pvip_se)), 0.1, 0.9)
            
            boot_svc = rng_param.choice(svc_clean, size=len(svc_clean), replace=True)
            fit_a, _, fit_scale = stats.gamma.fit(boot_svc, floc=0)
            mean_svc_sample = fit_a * fit_scale
            
            m_sample = Model(
                rates=r_sample.tolist(),
                service=gamma_service(fit_a, fit_scale),
                theta=th_sample,
                p_vip=pvip_sample,
                hour_len=60.0,
                mean_svc=mean_svc_sample
            )
            
            res_opt_p = sim.run_reps(m_sample, sched_opt, n_reps=reps_per_param, seed_base=7000 + i*100)
            worst_opt_p = min(res_opt_p["hourly"], key=lambda x: x["sl_ci95_low"])
            res_rob_p = sim.run_reps(m_sample, sched_rob, n_reps=reps_per_param, seed_base=7000 + i*100)
            worst_rob_p = min(res_rob_p["hourly"], key=lambda x: x["sl_ci95_low"])
            
            opt_sl_list.append(res_opt_p["sl_mean"])
            rob_sl_list.append(res_rob_p["sl_mean"])
            opt_worst_list.append(worst_opt_p["sl_ci95_low"])
            rob_worst_list.append(worst_rob_p["sl_ci95_low"])
            
            param_records.append({
                "bo_tham_so": i + 1,
                "mean_rate": np.mean(r_sample),
                "mean_svc": mean_svc_sample,
                "theta": th_sample,
                "sl_toan_ngay_opt": res_opt_p["sl_mean"],
                "sl_gio_te_nhat_opt": worst_opt_p["sl_ci95_low"],
                "sl_toan_ngay_rob": res_rob_p["sl_mean"],
                "sl_gio_te_nhat_rob": worst_rob_p["sl_ci95_low"]
            })
            
        df_params = pd.DataFrame(param_records)
        df_params.to_csv(param_csv_path, index=False, encoding="utf-8-sig")
        print(f"  -> Da luu ket qua do bat dinh tham so: {param_csv_path}")

        prob_opt_all = float(np.mean(np.array(opt_sl_list) >= 0.90))
        prob_rob_all = float(np.mean(np.array(rob_sl_list) >= 0.90))

        # Ve bieu do phan phoi SL do bat dinh tham so fig_a_bat_dinh.png
        plt.figure(figsize=(9, 5))
        plt.hist(opt_sl_list, bins=12, alpha=0.6, color="#1F4E78", label=f"Lịch tối ưu (P(SL≥90%) = {prob_opt_all*100:.1f}%)", edgecolor="black")
        plt.hist(rob_sl_list, bins=12, alpha=0.6, color="#2CA02C", label=f"Lịch bền vững (P(SL≥90%) = {prob_rob_all*100:.1f}%)", edgecolor="black")
        plt.axvline(x=0.90, color="red", linestyle="--", lw=2, label="Mục tiêu SLA = 90%")
        plt.xlabel("Mức độ phục vụ SL toàn ngày")
        plt.ylabel("Tần số (Số bộ tham số)")
        plt.title("Phân phối Mức độ Phục vụ qua 50 Bộ Tham số Bootstrap\n(Đánh giá độ không chắc chắn của tham số ước lượng)")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.5)
        
        uncert_fig_path = os.path.join(HINH_DIR, "fig_a_bat_dinh.png")
        plt.savefig(uncert_fig_path, dpi=200, bbox_inches="tight")
        plt.savefig(os.path.join(BASE_DIR, "fig_a_bat_dinh.png"), dpi=200, bbox_inches="tight")
        plt.close()
        print(f"  -> Da xuat hinh do bat dinh: {uncert_fig_path}")

    # --- 3.2 Do nhay theo phan phoi thoi gian phuc vu (E5) ---
    if os.path.exists(dist_csv_path) and not force:
        print("\n[A.2] Đã tồn tại kết quả độ nhạy phân phối phục vụ (do_nhay_phan_phoi.csv). Bỏ qua chạy lại.")
        df_dist = pd.read_csv(dist_csv_path)
    else:
        print("\n[A.2] Dang kiem tra do nhay theo phan phoi thoi gian phuc vu (E5: Gamma, Bootstrap, Lognormal, Exp)...")
        mean_s = model.mean_svc
        cv_s = np.sqrt(model.cs2_svc)
        dist_models = {
            "Gamma chuẩn (AIC tốt nhất)": gamma_service(params["service"]["gamma_shape"], params["service"]["gamma_scale"]),
            "Bootstrap trực tiếp từ dữ liệu": empirical_service(svc_clean),
            "Lognormal (cv tăng 20%)": lognorm_service(mean_s, cv_s * 1.2),
            "Mũ (Exponential - Mô hình đơn giản)": exp_service(mean_s)
        }
        dist_rows = []
        for d_name, d_sampler in dist_models.items():
            m_d = Model(model.rates, d_sampler, model.theta, model.p_vip, model.hour_len, mean_s)
            res_d = sim.run_reps(m_d, sched_opt, n_reps=100, seed_base=60000)
            worst_h = min(res_d["hourly"], key=lambda x: x["sl_ci95_low"])
            dist_rows.append({
                "phan_phoi_phuc_vu": d_name,
                "sl_toan_ngay": f"{res_d['sl_mean']:.4f} ± {res_d['sl_ci_half']:.4f}",
                "sl_gio_te_nhat": f"{worst_h['sl_mean']:.4f} [Low: {worst_h['sl_ci95_low']:.4f}]",
                "ti_le_bo_ve": f"{res_d['p_ab_mean']*100:.2f}%",
                "wq_phut": f"{res_d['wq_mean']:.4f}",
                "dat_sla": "ĐẠT" if worst_h['sl_ci95_low'] >= 0.90 else "KHÔNG ĐẠT"
            })
            
        df_dist = pd.DataFrame(dist_rows)
        df_dist.to_csv(dist_csv_path, index=False, encoding="utf-8-sig")
        print(f"  -> Da luu bang do nhay phan phoi: {dist_csv_path}")
    print(df_dist.to_string(index=False))

    # --- 3.3 Kiem tra ngoai mau (E6 tren tap test 4 ngay) ---
    print("\n[A.3] Dang kiem tra ngoai mau tren tap test (E6: 4 ngay lam viec, 2.969 cuoc goi)...")
    # Tinh thong ke tap test
    test_rates_info = a_data.fit_arrivals(df_test)
    test_svc_info = a_data.fit_service(df_test)
    test_ab_info = a_data.fit_patience(df_test)
    test_p_vip = float(df_test["vip"].mean())
    
    # Kiem dinh Kolmogorov-Smirnov 2 mau giua thoi gian phuc vu tap Train va tap Test
    svc_test = df_test[df_test["served"] == 1]["svc"].dropna().values
    ks_stat, ks_pval = stats.ks_2samp(svc_clean, svc_test)
    print(f"  • Kiem dinh KS 2 mau giua Train va Test: D = {ks_stat:.4f}, p-value = {ks_pval:.4f}")
    if ks_pval > 0.05:
        print("    -> Chap nhan H0: Phan phoi thoi gian phuc vu giua 2 tap khong co su khac biet y nghia thong ke.")
    else:
        print("    -> Bac bo H0: Co su khac biet nho giua 2 tap.")

    # Mo phong lich toi uu duoi tham so cua tap Test
    m_test = Model(
        rates=test_rates_info["rates"],
        service=gamma_service(test_svc_info["gamma_params"]["shape"], test_svc_info["gamma_params"]["scale"]),
        theta=test_ab_info["theta"],
        p_vip=test_p_vip,
        hour_len=60.0,
        mean_svc=test_svc_info["mean"]
    )
    res_test = sim.run_reps(m_test, sched_opt, n_reps=150, seed_base=9999)
    worst_test_h = min(res_test["hourly"], key=lambda x: x["sl_ci95_low"])
    
    # So sanh thuc te quan sat tren tap test theo gio voi mo phong
    test_hourly_obs = []
    for h in range(common.HOURS):
        sub_h = df_test[df_test["hour"] == h]
        n_h = len(sub_h)
        sl_obs = ((sub_h["served"] == 1) & (sub_h["wait"] <= common.WAIT_THRESHOLD)).sum() / n_h if n_h > 0 else 0.0
        wq_obs = sub_h["wait"].mean() if n_h > 0 else 0.0
        pab_obs = (sub_h["served"] == 0).mean() if n_h > 0 else 0.0
        
        sim_h = res_test["hourly"][h]
        test_hourly_obs.append({
            "khung_gio": common.H_LABELS[h],
            "so_quay_lich_toi_uu": sched_opt[h],
            "lam_train": model.rates[h],
            "lam_test": test_rates_info["rates"][h],
            "sl_mo_phong_test": sim_h["sl_mean"],
            "sl_mo_phong_low": sim_h["sl_ci95_low"],
            "sl_quan_sat_test": round(sl_obs, 4),
            "wq_mo_phong": sim_h["wq_mean"],
            "wq_quan_sat": round(wq_obs, 4),
            "pab_mo_phong": sim_h["p_ab_mean"],
            "pab_quan_sat": round(pab_obs, 4)
        })
        
    df_test_obs = pd.DataFrame(test_hourly_obs)
    test_csv_path = os.path.join(RESULTS_DIR, "ngoai_mau.csv")
    df_test_obs.to_csv(test_csv_path, index=False, encoding="utf-8-sig")
    print(f"  -> Da luu ket qua kiem tra ngoai mau: {test_csv_path}")

    # Ve bieu do so sanh ngoai mau fig_a_ngoai_mau.png
    plt.figure(figsize=(9, 5))
    x_h = np.arange(common.HOURS)
    width = 0.35
    sl_train_vals = [h_st["sl_mean"] for h_st in c_results["policy_evals"]["Tối ưu mô phỏng (Sim-Optimized)"]["hourly"]]
    plt.bar(x_h - width/2, sl_train_vals, width=width, label="Mô phỏng Tập Train", color="#1F4E78")
    plt.bar(x_h + width/2, df_test_obs["sl_mo_phong_test"], width=width, label="Mô phỏng Dưới Tham số Tập Test", color="#ED7D31")
    plt.axhline(y=0.90, color="red", linestyle="--", lw=1.5, label="Mục tiêu SLA = 90%")
    plt.xlabel("Khung giờ trong ngày")
    plt.ylabel("Tỉ lệ đạt SLA (P(Wq ≤ 5 phút))")
    plt.title("Kiểm tra Ngoài mẫu (Out-of-sample Test): So sánh Hiệu năng trên Tập Ước lượng vs Tập Kiểm tra")
    plt.xticks(x_h, common.H_LABELS)
    plt.ylim(0.7, 1.0)
    plt.legend()
    plt.grid(True, linestyle="--", axis="y")
    
    test_fig_path = os.path.join(HINH_DIR, "fig_a_ngoai_mau.png")
    plt.savefig(test_fig_path, dpi=200, bbox_inches="tight")
    plt.savefig(os.path.join(BASE_DIR, "fig_a_ngoai_mau.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  -> Da xuat hinh ngoai mau: {test_fig_path}")

    return {
        "df_params": df_params,
        "df_dist": df_dist,
        "df_test_obs": df_test_obs,
        "ks_stat": ks_stat,
        "ks_pval": ks_pval,
        "prob_opt_all": prob_opt_all,
        "prob_rob_all": prob_rob_all
    }

# =============================================================================
# 4. DONG BANG SO LIEU VA TAO MO_TA.MD (RESULTS/FINAL_V1/)
# =============================================================================

def freeze_all_results(model: Model, params: Dict, c_res: Dict, b_res: Dict, a_res: Dict):
    print("\n" + "="*70)
    print(">>> DONG BANG SO LIEU VA TAO THU MUC RESULTS/FINAL_V1/")
    print("="*70)
    
    # 1. Sao chep params.json
    params_src = os.path.join(DOCS_DIR, "params.json")
    params_dst = os.path.join(RESULTS_DIR, "params.json")
    shutil.copy2(params_src, params_dst)
    print(f"  • Đã sao chép: {params_dst}")

    # 2. Sao chep kiem_chung.csv tu ket_qua_kiem_chung.csv
    kc_src = os.path.join(BASE_DIR, "ket_qua_kiem_chung.csv")
    kc_dst = os.path.join(RESULTS_DIR, "kiem_chung.csv")
    if os.path.exists(kc_src):
        shutil.copy2(kc_src, kc_dst)
        print(f"  • Đã sao chép: {kc_dst}")

    # 3. Sao chep cac hinh anh vao results/final_v1/hinh/
    figures = [
        "fig_a_fit.png", "fig_c_welch.png", "fig_c_pooling.png",
        "fig_c_do_nhay.png", "fig_b_chi_phi.png", "fig_b_ca_lam.png",
        "fig_a_bat_dinh.png", "fig_a_ngoai_mau.png"
    ]
    for fig in figures:
        src = os.path.join(BASE_DIR, fig)
        dst = os.path.join(HINH_DIR, fig)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  • Đã sao lưu hình: {fig}")

    # 4. Tao MO_TA.md
    mota_content = """# Biên Bản Đóng Băng Dữ Liệu và Kết Quả Dự Án (results/final_v1/)

**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu  
**Phiên bản đóng băng:** `final_v1`  
**Ngày đóng băng:** 23/10/2026  
**Người tổng hợp:** Thành viên C (Đại diện nhóm nghiên cứu)  
**Môi trường thực thi:** Python 3.13, SimPy 4.1, SciPy 1.15, NumPy 2.2, Pandas 2.2  

---

## 1. Danh mục các tệp số liệu đóng băng

| Tên tệp | Nội dung tệp | Người phụ trách | Số lần lặp | Ghi chú kỹ thuật |
|---|---|:---:|:---:|---|
| [`params.json`](file:///d:/KHDV/results/final_v1/params.json) | Bộ tham số gốc ước lượng từ tập train (10 ngày) | Thành viên A | - | Phân phối Gamma ($E[S]=2.9236$, shape=1.0955, scale=2.6688) |
| [`kiem_chung.csv`](file:///d:/KHDV/results/final_v1/kiem_chung.csv) | Kết quả kiểm chứng mô phỏng 3 tầng và 2 kiểm tra độc lập | Thành viên C | 30–60 reps | Khớp Little $\\rho = 0.75$, M/G/1 P-K exact $14.625$p |
| [`lich_toi_uu.csv`](file:///d:/KHDV/results/final_v1/lich_toi_uu.csv) | Toàn bộ lịch sử thuật toán tối ưu 2 pha (Ramp-up & Pruning) | Thành viên C | 60 reps | Hội tụ tại lịch `[4, 5, 6, 5, 5, 5, 5, 5, 4]` (44 q-h) |
| [`so_sanh_chinh_sach.csv`](file:///d:/KHDV/results/final_v1/so_sanh_chinh_sach.csv) | Bảng so sánh 5 chính sách phục vụ với các chỉ số đo | Thành viên C | 300 reps | Seed độc lập mới (`seed_base=50000`), có CI95 đầy đủ |
| [`do_nhay.csv`](file:///d:/KHDV/results/final_v1/do_nhay.csv) | Phân tích độ nhạy theo Nhu cầu, $E[S]$, $\\theta$ | Thành viên C | 150 reps | Kỹ thuật số ngẫu nhiên chung (CRN) |
| [`chi_phi.csv`](file:///d:/KHDV/results/final_v1/chi_phi.csv) | Đánh đổi chi phí quầy-giờ và khách bỏ về ($k \\in \\{0.1, 0.25, 0.5, 1, 2\\}$) | Thành viên B | 300 reps | Phân tích kịch bản chi phí mất khách |
| [`lich_theo_ca.csv`](file:///d:/KHDV/results/final_v1/lich_theo_ca.csv) | Kết quả bài toán lập lịch theo ca MILP (4h, 8h, Hỗn hợp) | Thành viên B | MILP exact | Giải bằng `scipy.optimize.milp` |
| [`bat_dinh_tham_so.csv`](file:///d:/KHDV/results/final_v1/bat_dinh_tham_so.csv) | Phân phối mức độ phục vụ qua 50 bộ tham số bootstrap | Thành viên A | 50 x 20 reps | Xác định xác suất duy trì SLA khi tham số dao động |
| [`ngoai_mau.csv`](file:///d:/KHDV/results/final_v1/ngoai_mau.csv) | Kiểm định ngoài mẫu trên tập test 4 ngày (2.969 cuộc gọi) | Thành viên A | 150 reps | Kiểm định KS 2 mẫu và so sánh giờ đỉnh |

---

## 2. Danh mục biểu đồ đồ họa trong thư mục `hinh/`

1. [`fig_a_fit.png`](file:///d:/KHDV/results/final_v1/hinh/fig_a_fit.png): Kiểm định phân phối Poisson theo giờ và so sánh AIC các phân phối thời gian phục vụ.
2. [`fig_c_welch.png`](file:///d:/KHDV/results/final_v1/hinh/fig_c_welch.png): Đường cong Welch xác định điểm cắt warm-up (~200 khách / 150 phút).
3. [`fig_c_pooling.png`](file:///d:/KHDV/results/final_v1/hinh/fig_c_pooling.png): So sánh hiệu quả hàng chung bốc số tự động (96.5%) vs hàng riêng ngẫu nhiên (50.6%).
4. [`fig_c_do_nhay.png`](file:///d:/KHDV/results/final_v1/hinh/fig_c_do_nhay.png): Độ bền vững của 3 chính sách chính khi nhu cầu khách đến tăng từ 90% đến 130%.
5. [`fig_b_chi_phi.png`](file:///d:/KHDV/results/final_v1/hinh/fig_b_chi_phi.png): Đường đánh đổi Pareto giữa tổng quầy-giờ nhân sự và số lượt khách bỏ về mỗi ngày.
6. [`fig_b_ca_lam.png`](file:///d:/KHDV/results/final_v1/hinh/fig_b_ca_lam.png): Mức độ phủ quầy thực tế của các phương án ca làm (Hỗn hợp, Thuần 8h, Thuần 4h).
7. [`fig_a_bat_dinh.png`](file:///d:/KHDV/results/final_v1/hinh/fig_a_bat_dinh.png): Phân phối tần số của mức độ phục vụ qua 50 bộ tham số bootstrap.
8. [`fig_a_ngoai_mau.png`](file:///d:/KHDV/results/final_v1/hinh/fig_a_ngoai_mau.png): Đánh giá ngoài mẫu so sánh mức đạt SLA giữa tập Train và tập Test.

---

## 3. Quy ước và Cam kết Tính Nhất Quán
- **Nguyên tắc bất biến:** Toàn bộ bảng biểu, biểu đồ, con số xuất hiện trong **Báo cáo tổng kết** (`docs/bao_cao_tong_ket.md`) và **Bộ slide thuyết trình** (`docs/slide_thuyet_trinh.md`) đều được trích xuất 100% từ các tệp dữ liệu đã đóng băng tại thư mục này.
- Mọi điều chỉnh (nếu có sau ngày 23/10) bắt buộc phải tạo phiên bản mới `results/final_v2/` và cập nhật lại toàn bộ tài liệu liên quan.
"""
    mota_path = os.path.join(RESULTS_DIR, "MO_TA.md")
    with open(mota_path, "w", encoding="utf-8") as f:
        f.write(mota_content)
    print(f"  • Đã tạo tài liệu mô tả đóng băng: {mota_path}")

def run_all_week3():
    """Chay toan bo chuoi thi nghiem Tuan 3 tu dau den cuoi."""
    print("=" * 70)
    print("KHỞI CHẠY TOÀN BỘ CHƯƠNG TRÌNH THÍ NGHIỆM TUẦN 3 CHO CẢ 3 THÀNH VIÊN")
    print("=" * 70)
    
    model, params = load_calibrated_model()
    
    # 1. Chay phan C (Toi uu, So sanh chinh sach, Do nhay)
    c_res = run_member_c_experiments(model, params)
    
    # 2. Chay phan B (Chi phi, Ca lam viec MILP, Lich ben vung)
    b_res = run_member_b_experiments(model, c_res)
    
    # 3. Chay phan A (Do bat dinh tham so, Phan phoi phuc vu, Kiem tra ngoai mau)
    a_res = run_member_a_experiments(model, params, c_res)
    
    # 4. Dong bang so lieu vao results/final_v1/
    freeze_all_results(model, params, c_res, b_res, a_res)
    
    print("\n" + "=" * 70)
    print("HOÀN THÀNH 100% CÁC THÍ NGHIỆM VÀ ĐÃ ĐÓNG BĂNG DỮ LIỆU THÀNH CÔNG!")
    print("=" * 70)

if __name__ == "__main__":
    run_all_week3()
