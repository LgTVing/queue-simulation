"""
tools/run_s2_s3_s4.py:
Thuc hien Task S2 (Chi so ky vong co dieu kien),
Task S3 (Bat dinh CV ngay, Do nhay CV, va Posterior Predictive Check),
va Task S4 (Phan tich nguong luu luong va Bo du bao som).
"""

import sys, os
sys.path.insert(0, os.path.abspath('.'))

import json
import numpy as np
import pandas as pd
import scipy.stats as st
from common import Model, gamma_service
import c_sim as cs
from tools.stats_helpers import wilson_ci, t_ci

def get_base_model():
    with open('results/final_v3/params.json', 'r', encoding='utf-8') as f:
        p = json.load(f)
    
    shape = p['service']['gamma_shape']
    scale = p['service']['gamma_scale']
    
    m = Model(
        rates=p['rates_per_min'],
        service=gamma_service(shape, scale),
        theta=p['theta'],
        p_vip=p['p_vip'],
        mean_svc=p['service']['mean'],
        cs2_svc=p['service']['cs2']
    )
    return m

def evaluate_conditional_expectation(model, policies, cv_day=0.118, K_scenarios=200, R_reps=30, seed_base=20000):
    """
    Task S2: Tinh toan chi so ky vong co dieu kien tren K kich ban he so nhan ngay m,
    moi kich ban chay R lan lap doc lap de tinh SL ky vong E_h(m).
    """
    print(f"--- Danh gia ky vong co dieu kien: K={K_scenarios} kich ban, R={R_reps} reps moi kich ban, CV={cv_day:.3f} ---")
    shape_m = 1.0 / (cv_day ** 2)
    scale_m = cv_day ** 2
    
    results = []
    
    for pol_name, sched in policies.items():
        np.random.seed(seed_base)
        
        # Luu tru ket qua tung kich ban
        day_exp_sl = []       # E[SL_day | m]
        min_hour_exp_sl = []  # min_h E_h(m)
        hours_below_90 = []   # so gio co E_h(m) < 0.90
        actual_all_hours_met = [] # Danh gia theo tung lan lap thuc te
        actual_day_sl_all = []
        
        # Monthly pooling: gom nhom 20 ngay
        monthly_arrivals = np.zeros(9)
        monthly_served_in_5 = np.zeros(9)
        month_count = 0
        monthly_all_met_count = 0
        
        day_counter = 0
        for k in range(K_scenarios):
            m_val = float(np.random.gamma(shape_m, scale_m))
            
            # Tinh E_h(m) qua R lan lap
            hour_sl_list = np.zeros((R_reps, 9))
            day_sl_reps = np.zeros(R_reps)
            
            for r in range(R_reps):
                seed_r = seed_base + k * 1000 + r
                df_rep = cs.simulate(model, sched, seed=seed_r, day_multiplier=m_val)
                stats_r = cs.rep_stats(df_rep, sched)
                day_counter += 1
                
                # Tinh thuc te cua rep nay
                rep_h_met = True
                for h in range(9):
                    sl_h = stats_r['hourly'][h]['sl']
                    hour_sl_list[r, h] = sl_h
                    if sl_h < 0.90:
                        rep_h_met = False
                    
                    # Accumulate for monthly
                    sub = df_rep[df_rep['hour'] == h]
                    monthly_arrivals[h] += len(sub)
                    monthly_served_in_5[h] += len(sub[(sub['served'] == 1) & (sub['wait'] <= 5.0)])
                
                actual_all_hours_met.append(rep_h_met)
                day_sl_reps[r] = stats_r['sl_all']
                actual_day_sl_all.append(stats_r['sl_all'])
                
                # Monthly aggregation (20 ngay)
                if day_counter % 20 == 0:
                    month_count += 1
                    month_sl = monthly_served_in_5 / np.maximum(monthly_arrivals, 1)
                    if np.all(month_sl >= 0.90):
                        monthly_all_met_count += 1
                    monthly_arrivals.fill(0)
                    monthly_served_in_5.fill(0)
            
            # Ky vong theo gio E_h(m)
            E_h = np.mean(hour_sl_list, axis=0)
            E_day = np.mean(day_sl_reps)
            
            day_exp_sl.append(E_day)
            min_hour_exp_sl.append(np.min(E_h))
            hours_below_90.append(np.sum(E_h < 0.90))
            
        day_exp_sl = np.array(day_exp_sl)
        min_hour_exp_sl = np.array(min_hour_exp_sl)
        hours_below_90 = np.array(hours_below_90)
        actual_all_hours_met = np.array(actual_all_hours_met)
        actual_day_sl_all = np.array(actual_day_sl_all)
        
        # Tinh ti le va Wilson CI
        p_day_exp, p_day_exp_l, p_day_exp_h, _ = wilson_ci(np.sum(day_exp_sl >= 0.90), K_scenarios)
        p_min_exp, p_min_exp_l, p_min_exp_h, _ = wilson_ci(np.sum(min_hour_exp_sl >= 0.90), K_scenarios)
        p_act_all, p_act_all_l, p_act_all_h, _ = wilson_ci(np.sum(actual_all_hours_met), len(actual_all_hours_met))
        p_month, p_month_l, p_month_h, _ = wilson_ci(monthly_all_met_count, max(1, month_count))
        
        results.append({
            'chinh_sach': pol_name,
            'quay_gio': sum(sched),
            'cv_day': cv_day,
            'SL_ky_vong_ngay_TB': float(np.mean(day_exp_sl)),
            'SL_phim_5pct': float(np.percentile(day_exp_sl, 5)),
            'P_SL_ky_vong_ngay_ge90': p_day_exp,
            'P_SL_ky_vong_ngay_low95': p_day_exp_l,
            'P_SL_ky_vong_ngay_high95': p_day_exp_h,
            'P_min_h_Eh_ge90': p_min_exp,
            'P_min_h_Eh_low95': p_min_exp_l,
            'P_min_h_Eh_high95': p_min_exp_h,
            'so_gio_Eh_duoi_90_TB': float(np.mean(hours_below_90)),
            'P_thuc_te_moi_gio_ge90': p_act_all,
            'P_thuc_te_moi_gio_low95': p_act_all_l,
            'P_thuc_te_moi_gio_high95': p_act_all_h,
            'P_thang_20ngay_moi_gio_ge90': p_month,
            'P_thang_20ngay_low95': p_month_l,
            'P_thang_20ngay_high95': p_month_h
        })
        print(f"  {pol_name}: P(E_day>=90%)={p_day_exp:.3f} [{p_day_exp_l:.3f}, {p_day_exp_h:.3f}], P(min E_h>=90%)={p_min_exp:.3f} [{p_min_exp_l:.3f}, {p_min_exp_h:.3f}], P(thuc te)={p_act_all:.3f}")

    return pd.DataFrame(results)

def task_s3_posterior_predictive_check(matrix_14):
    """
    Task S3: Posterior Predictive Check cho mo hinh 1 he so nhan ngay Gamma(CV=11.8%).
    So sanh chi so phan tan D_h giua mo hinh va thuc te quan sat.
    """
    print("\n--- TASK S3: POSTERIOR PREDICTIVE CHECK (1.000 tap 14 ngay) ---")
    means_14 = matrix_14.mean().values
    
    # D quan sat tren 14 ngay
    d_obs_hours = np.zeros(9)
    for h in range(9):
        col = matrix_14[h].values
        d_obs_hours[h] = np.sum((col - means_14[h]) ** 2) / means_14[h]
    
    tot_obs = matrix_14.sum(axis=1).values
    d_obs_total = np.sum((tot_obs - np.mean(tot_obs)) ** 2) / np.mean(tot_obs)
    
    # Mo phong 1.000 bo 14 ngay tu mo hinh
    B = 1000
    sim_d_hours = np.zeros((B, 9))
    sim_d_total = np.zeros(B)
    
    shape_m = 1.0 / (0.118 ** 2)
    scale_m = 0.118 ** 2
    
    for b in range(B):
        # 14 ngay
        m_sim = np.random.gamma(shape_m, scale_m, size=14)
        sim_mat = np.zeros((14, 9))
        for d in range(14):
            for h in range(9):
                sim_mat[d, h] = np.random.poisson(m_sim[d] * means_14[h])
        
        sim_means = sim_mat.mean(axis=0)
        for h in range(9):
            sim_d_hours[b, h] = np.sum((sim_mat[:, h] - sim_means[h]) ** 2) / max(sim_means[h], 1e-5)
            
        sim_tot = sim_mat.sum(axis=1)
        sim_d_total[b] = np.sum((sim_tot - np.mean(sim_tot)) ** 2) / max(np.mean(sim_tot), 1e-5)
        
    # Tinh p-value posterior: P(D_sim >= D_obs)
    pp_check = []
    for h in range(9):
        d_mean_sim = float(np.mean(sim_d_hours[:, h]))
        d_low_sim = float(np.percentile(sim_d_hours[:, h], 2.5))
        d_high_sim = float(np.percentile(sim_d_hours[:, h], 97.5))
        p_val = float(np.mean(sim_d_hours[:, h] >= d_obs_hours[h]))
        
        pp_check.append({
            'muc': f"{h+8}h - {h+9}h",
            'D_quan_sat': float(d_obs_hours[h]),
            'D_ky_vong_mo_hinh': d_mean_sim,
            'D_sim_ci_low': d_low_sim,
            'D_sim_ci_high': d_high_sim,
            'posterior_predictive_pvalue': p_val,
            'mo_hinh_giai_thich_tot': 'Tot' if 0.05 <= p_val <= 0.95 else 'Kem (qua phan tan manh hon mo hinh)'
        })
        
    p_val_tot = float(np.mean(sim_d_total >= d_obs_total))
    pp_check.append({
        'muc': 'Tong ca ngay',
        'D_quan_sat': float(d_obs_total),
        'D_ky_vong_mo_hinh': float(np.mean(sim_d_total)),
        'D_sim_ci_low': float(np.percentile(sim_d_total, 2.5)),
        'D_sim_ci_high': float(np.percentile(sim_d_total, 97.5)),
        'posterior_predictive_pvalue': p_val_tot,
        'mo_hinh_giai_thich_tot': 'Tot' if 0.05 <= p_val_tot <= 0.95 else 'Kem'
    })
    
    df_pp = pd.DataFrame(pp_check)
    df_pp.to_csv('results/final_v3/posterior_predictive_check.csv', index=False)
    print("Da luu results/final_v3/posterior_predictive_check.csv:")
    print(df_pp[['muc', 'D_quan_sat', 'D_ky_vong_mo_hinh', 'posterior_predictive_pvalue', 'mo_hinh_giai_thich_tot']])
    return df_pp

def task_s4_threshold_and_prediction(matrix_14, model, policies):
    """
    Task S4: Phan tich nguong luu luong V* va Bo du bao som (Early-hour predictor).
    """
    print("\n--- TASK S4: PHAN TICH NGUONG VA BO DU BAO SOM ---")
    
    # 1. Bo du bao tu gio som (8h-10h: gio 0 + gio 1)
    x_early = (matrix_14[0] + matrix_14[1]).values # 8h-10h
    v_total = matrix_14.sum(axis=1).values # ca ngay
    
    # Linear regression: V_total = a + b * x_early
    slope, intercept, r_val, p_val, std_err = st.linregress(x_early, v_total)
    
    # Tinh RMSE va 95% Prediction Interval
    y_pred = intercept + slope * x_early
    residuals = v_total - y_pred
    rmse = np.sqrt(np.mean(residuals ** 2))
    
    print(f"Hoi quy du bao som: V_hat = {intercept:.1f} + {slope:.2f} * (N_8h_10h)")
    print(f"  Pearson r = {r_val:.3f} (p = {p_val:.4f}), R^2 = {r_val**2:.3f}, RMSE = {rmse:.1f} khach")
    
    # Correlation 8h-11h
    x_11h = (matrix_14[0] + matrix_14[1] + matrix_14[2]).values
    r_11h, p_11h = st.pearsonr(x_11h, v_total)
    print(f"  Pearson r (8h-11h vs V_total) = {r_11h:.3f} (p = {p_11h:.4f})")
    
    # 2. Xac dinh nguong V* bang mo phong tai cac moc luu luong co dinh
    volumes = np.array([550, 600, 650, 687, 700, 725, 750, 775, 800, 850])
    v_results = []
    
    for v in volumes:
        m_v = v / 686.7
        # Chay 50 reps cho moi moc V
        sls_44 = []
        sls_48 = []
        for r in range(40):
            df_44 = cs.simulate(model, policies['Toi_uu_44'], seed=30000 + int(v)*10 + r, day_multiplier=m_v)
            df_48 = cs.simulate(model, policies['Ben_vung_48'], seed=40000 + int(v)*10 + r, day_multiplier=m_v)
            sls_44.append(cs.rep_stats(df_44, policies['Toi_uu_44'])['sl_all'])
            sls_48.append(cs.rep_stats(df_48, policies['Ben_vung_48'])['sl_all'])
            
        sl_44 = float(np.mean(sls_44))
        sl_48 = float(np.mean(sls_48))
        
        v_results.append({
            'luu_luong_ngay_V': v,
            'he_so_m': round(m_v, 3),
            'SL_Lich_44': sl_44,
            'SL_Lich_48': sl_48,
            'Lich_44_dat_ge90': 'Dat' if sl_44 >= 0.90 else 'Hut',
            'Lich_48_dat_ge90': 'Dat' if sl_48 >= 0.90 else 'Hut'
        })
        
    df_v = pd.DataFrame(v_results)
    df_v.to_csv('results/final_v3/nguong_luu_luong_chi_tiet.csv', index=False)
    print("Da luu results/final_v3/nguong_luu_luong_chi_tiet.csv")
    print(df_v)
    
    # 3. Danh gia Chinh sach ghep (Composite Dynamic Policy) tren 14 ngay thuc te
    eval_composite = []
    for d in range(14):
        n_early = matrix_14.iloc[d, 0] + matrix_14.iloc[d, 1]
        v_act = matrix_14.iloc[d].sum()
        v_hat = intercept + slope * n_early
        
        # Nguy co vuot 725 (nguong SL < 90%)
        pol_chosen = 'Ben_vung_48' if v_hat > 700 else 'Toi_uu_44'
        qh_used = 48 if pol_chosen == 'Ben_vung_48' else 44
        
        eval_composite.append({
            'ngay': d,
            'tap': 'Train' if d < 10 else 'Test',
            'N_8h_10h': n_early,
            'V_thuc_te': v_act,
            'V_du_bao': round(v_hat, 1),
            'sai_so_du_bao': round(v_hat - v_act, 1),
            'chinh_sach_chon': pol_chosen,
            'quay_gio_su_dung': qh_used
        })
        
    df_comp = pd.DataFrame(eval_composite)
    df_comp.to_csv('results/final_v3/danh_gia_chinh_sach_du_bao_14ngay.csv', index=False)
    
    avg_qh = df_comp['quay_gio_su_dung'].mean()
    tiet_kiem_vs_54 = (54.0 - avg_qh) / 54.0 * 100.0
    tiet_kiem_vs_56 = (56.0 - avg_qh) / 56.0 * 100.0
    print(f"\nChinh sach du bao ghep tren 14 ngay:")
    print(f"  Quay-gio trung binh: {avg_qh:.2f} q-h/ngay")
    print(f"  Tiet kiem so voi 54 q-h: {tiet_kiem_vs_54:.2f}%")
    print(f"  Tiet kiem so voi 56 q-h (gio cong ca 6 NV): {tiet_kiem_vs_56:.2f}%")

def main():
    model = get_base_model()
    policies = {
        'Toi_uu_44': [4, 5, 6, 5, 5, 5, 5, 5, 4],
        'Ben_vung_48': [5, 6, 6, 6, 5, 5, 5, 5, 5],
        'Moc_co_so_54': [6, 6, 6, 6, 6, 6, 6, 6, 6]
    }
    
    # Task S2: Tinh chi so ky vong co dieu kien tren CV chuan 11.8%
    df_s2 = evaluate_conditional_expectation(model, policies, cv_day=0.118, K_scenarios=200, R_reps=30, seed_base=20000)
    df_s2.to_csv('results/final_v3/chi_so_ky_vong_dieu_kien.csv', index=False)
    print("Da luu results/final_v3/chi_so_ky_vong_dieu_kien.csv")
    
    # Task S3: Do nhay theo CV ngay: 8%, 12%, 16%, 20%
    cv_list = [0.08, 0.12, 0.16, 0.20]
    all_cv_results = []
    for cv_val in cv_list:
        df_cv = evaluate_conditional_expectation(model, policies, cv_day=cv_val, K_scenarios=100, R_reps=20, seed_base=50000 + int(cv_val*100))
        all_cv_results.append(df_cv)
    df_all_cv = pd.concat(all_cv_results, ignore_index=True)
    df_all_cv.to_csv('results/final_v3/do_nhay_cv_ngay.csv', index=False)
    print("Da luu results/final_v3/do_nhay_cv_ngay.csv")
    
    # Task S3: Posterior Predictive Check
    df_raw = pd.read_csv('data/clean/data_clean.csv')
    matrix_14 = df_raw.groupby(['day', 'hour']).size().unstack(fill_value=0)
    task_s3_posterior_predictive_check(matrix_14)
    
    # Task S4: Nguong luu luong va Bo du bao som
    task_s4_threshold_and_prediction(matrix_14, model, policies)
    
    print("\nHoan thanh S2, S3, S4!")

if __name__ == '__main__':
    main()
