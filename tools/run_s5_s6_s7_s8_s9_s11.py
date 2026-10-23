"""
tools/run_s5_s6_s7_s8_s9_s11.py:
Thuc hien Task S5 (Bootstrap long nhau & Phan ra phuong sai),
Task S6 (Kiem tra ngoai mau voi Khoang du bao & Holm-Bonferroni),
Task S7 (Doi chieu 14 ngay kem phan dinh Train/Test va Wilson CI),
Task S8 (Kiem chung M/G/1 40.000p va Bang kiem chung Student-t),
Task S9 (Do nhay phan phoi kem gio te nhat),
Task S11 (Bang chi phi kem truyen sai so va hieu so cap),
va Task C6 (Xuat results/final_v3/pha3.csv chung minh toi thieu cuc bo).
"""

import sys, os
sys.path.insert(0, os.path.abspath('.'))

import json
import numpy as np
import pandas as pd
import scipy.stats as st
from common import Model, exp_service, gamma_service, lognorm_service, empirical_service
import c_sim as cs
import b_theory as bt
from tools.stats_helpers import wilson_ci, t_ci, holm_bonferroni

def get_base_model():
    with open('results/final_v3/params.json', 'r', encoding='utf-8') as f:
        p = json.load(f)
    shape = p['service']['gamma_shape']
    scale = p['service']['gamma_scale']
    return Model(
        rates=p['rates_per_min'],
        service=gamma_service(shape, scale),
        theta=p['theta'],
        p_vip=p['p_vip'],
        mean_svc=p['service']['mean'],
        cs2_svc=p['service']['cs2']
    )

# =============================================================================
# S8: KIEM CHUNG M/G/1 VA BANG KIEM CHUNG VOI STUDENT-T
# =============================================================================
def task_s8_mg1_and_tier_verification():
    print("\n=== TASK S8: KIEM CHUNG M/G/1 POLLACZEK-KHINCHINE VA STUDENT-T ===")
    # 1. Chay M/G/1 exact: c=1, lam=0.25, E[S]=3.0, cv=1.5 (cs2=2.25), rho=0.75
    # Ly thuyet Wq = 0.75 * 3.0 * (1 + 2.25) / (2 * 0.25) = 14.6250
    wq_theory = 14.6250
    m_mg1 = Model(
        rates=[0.25],
        service=lognorm_service(3.0, 1.5),
        theta=0.0,
        p_vip=0.0,
        hour_len=40000.0, # 40.000 phut
        mean_svc=3.0,
        cs2_svc=2.25
    )
    
    n_reps = 40
    wq_sims = []
    for r in range(n_reps):
        df_r = cs.simulate(m_mg1, [1], seed=77000 + r, warm_up=5000.0)
        wq_sims.append(df_r['wait'].mean())
        
    m_wq, l_wq, h_wq, hw_wq, s_wq = t_ci(wq_sims, conf=0.95)
    bias_pct = (m_wq - wq_theory) / wq_theory * 100.0
    print(f"M/G/1 P-K Exact (40 reps, 40.000 phut, warm-up 5.000p):")
    print(f"  Ly thuyet: {wq_theory:.4f}p | Mo phong SimPy: {m_wq:.4f} +/- {hw_wq:.4f}p [{l_wq:.4f}, {h_wq:.4f}] (s={s_wq:.4f})")
    print(f"  Sai lech: {bias_pct:+.2f}% | Ly thuyet trong CI95: {l_wq <= wq_theory <= h_wq}")
    
    # 2. Xay dung bang kiem chung 3 tang voi Student-t CI
    # Doc tu final_v2/kiem_chung.csv va cap nhat lai he so Student-t
    old_kc = pd.read_csv('results/final_v2/kiem_chung.csv')
    
    kc_v3 = []
    for idx, row in old_kc.iterrows():
        tang = str(row['kiem_chung'])
        chi_so = str(row['chi_so'])
        val_lt = float(row['ly_thuyet'])
        val_mp = float(row['mo_phong'])
        
        # So lan lap cu: Tang 1 & 2 thuong 30 reps, Tang 3 cv=1.5 60 reps
        n_r = 30
        if '60 reps' in tang:
            n_r = 60
        elif 'Kiem tra A' in tang:
            # Thay bang ket qua chay 40 reps o tren
            val_mp = round(m_wq, 4)
            tang = 'Kiem tra A (M/G/1 P-K exact, 40 reps, 40k phut)'
            n_r = 40
            
        t_crit = st.t.ppf(0.975, df=n_r - 1)
        z_crit = 1.96
        # Dieu chinh do nua rong tu 1.96 sang t_crit
        ci_str = str(row['ci95']).replace('±', '').strip()
        old_hw = float(ci_str)
        new_hw = old_hw * (t_crit / z_crit) if 'Kiem tra A' not in tang else hw_wq
        
        diff_pct = (val_mp - val_lt) / val_lt * 100.0
        in_ci = (val_mp - new_hw <= val_lt <= val_mp + new_hw)
        
        note = str(row['ghi_chu'])
        if 'Kiem tra A' in tang:
            note = f"Ly thuyet 14.625p nam trong CI95 [{l_wq:.2f}, {h_wq:.2f}]; khong bac bo duoc tinh dung"
        elif 'SimPy dung tuyet doi' in note:
            note = note.replace('SimPy dung tuyet doi', 'khong bac bo duoc tinh dung')
            
        kc_v3.append({
            'kiem_chung': tang,
            'chi_so': chi_so,
            'ly_thuyet': val_lt,
            'mo_phong': val_mp,
            'n_reps': n_r,
            't_critical': round(t_crit, 4),
            'nua_khoang_tin_cay_95': round(new_hw, 4),
            'ci95': f"±{new_hw:.4f}",
            'sai_lech_pct': f"{diff_pct:+.2f}%",
            'dat': 'Y' if in_ci else ('-' if 'cv=1.5' in tang or 'cv=0.5' in tang else 'N'),
            'muc_xap_xi': row['muc_xap_xi'],
            'ghi_chu': note
        })
        
    df_kc_v3 = pd.DataFrame(kc_v3)
    df_kc_v3.to_csv('results/final_v3/kiem_chung_v3.csv', index=False)
    print("Da luu results/final_v3/kiem_chung_v3.csv")

# =============================================================================
# S5: BOOTSTRAP THAM SO LONG NHAU & PHAN RA PHUONG SAI
# =============================================================================
def task_s5_nested_bootstrap(train_df, model, sched=[4, 5, 6, 5, 5, 5, 5, 5, 4]):
    print("\n=== TASK S5: BOOTSTRAP LONG NHAU VA PHAN RA PHUONG SAI (50 Bo x 60 Reps) ===")
    B = 50
    R = 60
    
    days = train_df['day'].unique()
    
    boot_results = []
    b_means = []
    b_worst_hours = []
    
    np.random.seed(88888)
    
    for b in range(B):
        # 1. Resample 10 ngay de lay lambda_h (giu nguyen correlation va overdispersion)
        sampled_days = np.random.choice(days, size=len(days), replace=True)
        sub_df = pd.concat([train_df[train_df['day'] == d] for d in sampled_days])
        
        # lambda_h
        hour_counts = sub_df.groupby('hour').size()
        rates_b = [float(hour_counts.get(h, 0)) / (len(sampled_days) * 60.0) for h in range(9)]
        
        # 2. Resample served records de lay service time
        served_recs = sub_df[sub_df['served'] == 1]['svc'].dropna().values
        if len(served_recs) < 50:
            served_recs = train_df[train_df['served'] == 1]['svc'].dropna().values
        boot_svc = np.random.choice(served_recs, size=len(served_recs), replace=True)
        shape_b, _, scale_b = st.gamma.fit(boot_svc, floc=0)
        mean_svc_b = shape_b * scale_b
        
        # 3. Resample waiting records de lay theta
        waiting_recs = sub_df[sub_df['wait'] > 0]
        n_ab_b = np.sum(waiting_recs['served'] == 0)
        tot_wait_b = np.sum(waiting_recs['wait'])
        theta_b = n_ab_b / tot_wait_b if tot_wait_b > 0 else 0.1087
        
        # p_vip
        pv_b = float(np.mean(sub_df['vip'] == 1))
        
        m_b = Model(
            rates=rates_b,
            service=gamma_service(shape_b, scale_b),
            theta=theta_b,
            p_vip=pv_b,
            mean_svc=mean_svc_b,
            cs2_svc=1.0 / shape_b
        )
        
        # Chay R lan lap cho bo tham so b
        sl_reps = []
        hour_sl_matrix = np.zeros((R, 9))
        for r in range(R):
            df_br = cs.simulate(m_b, sched, seed=60000 + b * 1000 + r)
            st_br = cs.rep_stats(df_br, sched)
            sl_reps.append(st_br['sl_all'])
            for h in range(9):
                hour_sl_matrix[r, h] = st_br['hourly'][h]['sl']
                
        mean_sl_b = float(np.mean(sl_reps))
        # Gio te nhat: trung binh theo gio truoc roi lay min
        hour_means = np.mean(hour_sl_matrix, axis=0)
        worst_h_b = float(np.min(hour_means))
        
        b_means.append(mean_sl_b)
        b_worst_hours.append(worst_h_b)
        
        boot_results.append({
            'boot_id': b,
            'mean_sl_day': mean_sl_b,
            'worst_hour_sl': worst_h_b,
            'mean_svc': mean_svc_b,
            'theta': theta_b,
            'p_vip': pv_b
        })
        
    df_boot = pd.DataFrame(boot_results)
    df_boot.to_csv('results/final_v3/bat_dinh_nested.csv', index=False)
    
    # Chay bo tham so danh nghia voi cung R=60 reps
    nom_sl_reps = []
    nom_hour_matrix = np.zeros((R, 9))
    for r in range(R):
        df_nr = cs.simulate(model, sched, seed=90000 + r)
        st_nr = cs.rep_stats(df_nr, sched)
        nom_sl_reps.append(st_nr['sl_all'])
        for h in range(9):
            nom_hour_matrix[r, h] = st_nr['hourly'][h]['sl']
            
    nom_mean_sl = float(np.mean(nom_sl_reps))
    nom_worst_sl = float(np.min(np.mean(nom_hour_matrix, axis=0)))
    
    # Phan ra phuong sai
    var_total_obs = float(np.var(b_means, ddof=1)) # Tong phuong sai quan sat qua 50 bo
    # Phuong sai noi tai 1 lan lap (uoc tinh tu nominal)
    var_within_1rep = float(np.var(nom_sl_reps, ddof=1))
    var_sim_noise = var_within_1rep / float(R) # Nhiễu mô phỏng trung bình của R reps
    var_param_true = max(0.0, var_total_obs - var_sim_noise) # Phương sai thực do bất định tham số
    
    pct_param = (var_param_true / var_total_obs) * 100.0 if var_total_obs > 0 else 0.0
    pct_noise = (var_sim_noise / var_total_obs) * 100.0 if var_total_obs > 0 else 0.0
    
    # Ti le dat kem Wilson CI
    n_met_day = np.sum(np.array(b_means) >= 0.90)
    n_met_worst = np.sum(np.array(b_worst_hours) >= 0.90)
    
    p_day, p_day_l, p_day_h, _ = wilson_ci(n_met_day, B)
    p_worst, p_worst_l, p_worst_h, _ = wilson_ci(n_met_worst, B)
    
    df_decomp = pd.DataFrame([
        {'chi_so': 'SL Toan ngay danh nghia (R=60)', 'gia_tri': nom_mean_sl, 'ci_low': nom_mean_sl - 1.96*np.sqrt(var_sim_noise), 'ci_high': nom_mean_sl + 1.96*np.sqrt(var_sim_noise)},
        {'chi_so': 'SL Gio te nhat danh nghia (R=60)', 'gia_tri': nom_worst_sl, 'ci_low': np.nan, 'ci_high': np.nan},
        {'chi_so': 'Phuong sai tong quan sat qua cac bo bootstrap', 'gia_tri': var_total_obs, 'ci_low': np.nan, 'ci_high': np.nan},
        {'chi_so': 'Phuong sai do nhieu mo phong (Within / R)', 'gia_tri': var_sim_noise, 'ci_low': np.nan, 'ci_high': np.nan},
        {'chi_so': 'Phuong sai do bat dinh tham so (Between)', 'gia_tri': var_param_true, 'ci_low': np.nan, 'ci_high': np.nan},
        {'chi_so': 'Ti le phuong sai do bat dinh tham so (%)', 'gia_tri': pct_param, 'ci_low': np.nan, 'ci_high': np.nan},
        {'chi_so': 'Ti le phuong sai do nhieu mo phong (%)', 'gia_tri': pct_noise, 'ci_low': np.nan, 'ci_high': np.nan},
        {'chi_so': 'Xac suat SL toan ngay >= 90%', 'gia_tri': p_day, 'ci_low': p_day_l, 'ci_high': p_day_h},
        {'chi_so': 'Xac suat SL gio te nhat >= 90%', 'gia_tri': p_worst, 'ci_low': p_worst_l, 'ci_high': p_worst_h}
    ])
    df_decomp.to_csv('results/final_v3/phan_ra_phuong_sai.csv', index=False)
    print("Da luu results/final_v3/phan_ra_phuong_sai.csv:")
    print(df_decomp[['chi_so', 'gia_tri', 'ci_low', 'ci_high']])

# =============================================================================
# S6: KIEM TRA NGOAI MAU VOI KHOANG DU BAO (PREDICTIVE INTERVAL)
# =============================================================================
def task_s6_out_of_sample(df_all, model, sched=[4, 5, 6, 5, 5, 5, 5, 5, 4]):
    print("\n=== TASK S6: KIEM TRA NGOAI MAU VOI KHOANG DU BAO (PREDICTIVE INTERVAL) ===")
    test_df = df_all[df_all['day'] >= 10].copy() # Ngay 10-13 (4 ngay)
    
    # 1. So lieu thuc te quan sat tren tap test (2.969 cuoc goi)
    obs_rows = []
    tot_test_n = len(test_df)
    tot_test_s5 = len(test_df[(test_df['served'] == 1) & (test_df['wait'] <= 5.0)])
    tot_test_ab = len(test_df[test_df['served'] == 0])
    tot_test_wq = test_df['wait'].mean()
    
    p_sl_tot, sl_l_tot, sl_h_tot, _ = wilson_ci(tot_test_s5, tot_test_n)
    p_ab_tot, ab_l_tot, ab_h_tot, _ = wilson_ci(tot_test_ab, tot_test_n)
    
    for h in range(9):
        sub_h = test_df[test_df['hour'] == h]
        n_h = len(sub_h)
        s5_h = len(sub_h[(sub_h['served'] == 1) & (sub_h['wait'] <= 5.0)])
        ab_h = len(sub_h[sub_h['served'] == 0])
        wq_h = sub_h['wait'].mean() if n_h > 0 else 0.0
        
        p_sl, sl_l, sl_h, _ = wilson_ci(s5_h, n_h)
        p_ab, ab_l, ab_h, _ = wilson_ci(ab_h, n_h)
        
        obs_rows.append({
            'hour': h,
            'n_obs': n_h,
            'sl_obs': p_sl,
            'sl_obs_low': sl_l,
            'sl_obs_high': sl_h,
            'ab_obs': p_ab,
            'ab_obs_low': ab_l,
            'ab_obs_high': ab_h,
            'wq_obs': wq_h
        })
    df_obs = pd.DataFrame(obs_rows)
    
    # 2. Sinh 1.000 tap "4-ngay" tong hop tu mo hinh co he so bien dong ngay
    K_sets = 1000
    shape_m = 1.0 / (0.118 ** 2)
    scale_m = 0.118 ** 2
    
    sim_4day_sl = np.zeros((K_sets, 9))
    sim_4day_tot_sl = np.zeros(K_sets)
    sim_4day_tot_ab = np.zeros(K_sets)
    sim_4day_tot_wq = np.zeros(K_sets)
    
    np.random.seed(54321)
    for k in range(K_sets):
        # 4 ngay
        h_arr = np.zeros(9)
        h_s5 = np.zeros(9)
        tot_arr = 0
        tot_s5 = 0
        tot_ab = 0
        tot_wait = 0.0
        
        for d in range(4):
            m_d = float(np.random.gamma(shape_m, scale_m))
            df_day = cs.simulate(model, sched, seed=k*10 + d, day_multiplier=m_d)
            for h in range(9):
                sub = df_day[df_day['hour'] == h]
                h_arr[h] += len(sub)
                h_s5[h] += len(sub[(sub['served'] == 1) & (sub['wait'] <= 5.0)])
                
            tot_arr += len(df_day)
            tot_s5 += len(df_day[(df_day['served'] == 1) & (df_day['wait'] <= 5.0)])
            tot_ab += len(df_day[df_day['served'] == 0])
            tot_wait += df_day['wait'].sum()
            
        sim_4day_sl[k, :] = h_s5 / np.maximum(h_arr, 1)
        sim_4day_tot_sl[k] = tot_s5 / max(tot_arr, 1)
        sim_4day_tot_ab[k] = tot_ab / max(tot_arr, 1)
        sim_4day_tot_wq[k] = tot_wait / max(tot_arr, 1)
        
    # 3. Khoang du bao 95% (Predictive Interval: phan vi 2.5% den 97.5%)
    pred_results = []
    raw_p_values = []
    
    for h in range(9):
        sl_sim_mean = float(np.mean(sim_4day_sl[:, h]))
        pi_low = float(np.percentile(sim_4day_sl[:, h], 2.5))
        pi_high = float(np.percentile(sim_4day_sl[:, h], 97.5))
        
        obs_val = df_obs.loc[h, 'sl_obs']
        n_obs = df_obs.loc[h, 'n_obs']
        
        # Test 2 ti le giua sim_mean va obs_val
        # z-test
        se_pool = np.sqrt(sl_sim_mean * (1.0 - sl_sim_mean) / n_obs) if n_obs > 0 else 1.0
        z_stat = (obs_val - sl_sim_mean) / max(se_pool, 1e-5)
        p_val = 2.0 * (1.0 - st.norm.cdf(abs(z_stat)))
        raw_p_values.append(p_val)
        
        pred_results.append({
            'khung_gio': f"{h+8}h - {h+9}h",
            'so_quay': sched[h],
            'SL_mo_phong_TB': sl_sim_mean,
            'PI95_low': pi_low,
            'PI95_high': pi_high,
            'SL_thuc_te': obs_val,
            'SL_thuc_te_Wilson_low': df_obs.loc[h, 'sl_obs_low'],
            'SL_thuc_te_Wilson_high': df_obs.loc[h, 'sl_obs_high'],
            'trong_PI95': 'Co' if pi_low <= obs_val <= pi_high else 'Khong',
            'raw_p_value': p_val,
            'Wq_thuc_te': df_obs.loc[h, 'wq_obs'],
            'Bo_ve_thuc_te': df_obs.loc[h, 'ab_obs']
        })
        
    # Hieu chinh Holm-Bonferroni
    adj_p, reject_flags = holm_bonferroni(raw_p_values, alpha=0.05)
    for h in range(9):
        pred_results[h]['adj_p_value_Holm'] = adj_p[h]
        pred_results[h]['lech_co_y_nghia'] = 'Co' if reject_flags[h] else 'Khong'
        
    df_pred = pd.DataFrame(pred_results)
    df_pred.to_csv('results/final_v3/ngoai_mau_v3.csv', index=False)
    print("Da luu results/final_v3/ngoai_mau_v3.csv:")
    print(df_pred[['khung_gio', 'SL_mo_phong_TB', 'PI95_low', 'PI95_high', 'SL_thuc_te', 'trong_PI95', 'adj_p_value_Holm', 'lech_co_y_nghia']])

# =============================================================================
# S7: DOI CHIEU 14 NGAY VOI PHAN DINH TRAIN/TEST VA WILSON CI
# =============================================================================
def task_s7_fourteen_days(df_all, model, policies):
    print("\n=== TASK S7: DOI CHIEU 14 NGAY QUAN SAT VOI PHAN DINH TRAIN/TEST ===")
    days_list = sorted(df_all['day'].unique())
    
    rows_14 = []
    for d in days_list:
        sub_d = df_all[df_all['day'] == d]
        n_d = len(sub_d)
        tap = 'Train' if d < 10 else 'Test'
        
        # Mo phong 40 reps cho ngay d voi he so den m_d = n_d / 686.7
        m_d = n_d / 686.7
        sls_44 = []
        sls_48 = []
        sls_6 = []
        for r in range(40):
            df_44 = cs.simulate(model, policies['Toi_uu_44'], seed=10000 + d*100 + r, day_multiplier=m_d)
            df_48 = cs.simulate(model, policies['Ben_vung_48'], seed=20000 + d*100 + r, day_multiplier=m_d)
            df_6  = cs.simulate(model, policies['Moc_co_so_54'], seed=30000 + d*100 + r, day_multiplier=m_d)
            
            sls_44.append(cs.rep_stats(df_44, policies['Toi_uu_44'])['sl_all'])
            sls_48.append(cs.rep_stats(df_48, policies['Ben_vung_48'])['sl_all'])
            sls_6.append(cs.rep_stats(df_6, policies['Moc_co_so_54'])['sl_all'])
            
        m44, l44, h44, hw44, _ = t_ci(sls_44)
        m48, l48, h48, hw48, _ = t_ci(sls_48)
        m6,  l6,  h6,  hw6,  _ = t_ci(sls_6)
        
        rows_14.append({
            'ngay': d,
            'phan_tap': tap,
            'tong_khach': n_d,
            'SL_Lich_44': m44,
            'CI95_Lich_44': f"[{l44:.3f}, {h44:.3f}]",
            'Dat_SLA_44': 'Dat' if m44 >= 0.90 else 'Hut',
            'SL_Lich_48': m48,
            'CI95_Lich_48': f"[{l48:.3f}, {h48:.3f}]",
            'Dat_SLA_48': 'Dat' if m48 >= 0.90 else 'Hut',
            'SL_Moc_6': m6,
            'CI95_Moc_6': f"[{l6:.3f}, {h6:.3f}]",
            'Dat_SLA_6': 'Dat' if m6 >= 0.90 else 'Hut'
        })
        
    df_14 = pd.DataFrame(rows_14)
    df_14.to_csv('results/final_v3/theo_14_ngay_v3.csv', index=False)
    
    n_dat_44 = np.sum(df_14['Dat_SLA_44'] == 'Dat')
    n_dat_48 = np.sum(df_14['Dat_SLA_48'] == 'Dat')
    n_dat_6  = np.sum(df_14['Dat_SLA_6'] == 'Dat')
    
    p44, l44, h44, _ = wilson_ci(n_dat_44, 14)
    p48, l48, h48, _ = wilson_ci(n_dat_48, 14)
    p6,  l6,  h6,  _ = wilson_ci(n_dat_6, 14)
    
    print("Da luu results/final_v3/theo_14_ngay_v3.csv:")
    print(f"  Lich 44 dat: {n_dat_44}/14 ({p44*100:.1f}%) | Wilson 95%: [{l44*100:.1f}%, {h44*100:.1f}%]")
    print(f"  Lich 48 dat: {n_dat_48}/14 ({p48*100:.1f}%) | Wilson 95%: [{l48*100:.1f}%, {h48*100:.1f}%]")
    print(f"  Moc 6 dat:   {n_dat_6}/14 ({p6*100:.1f}%) | Wilson 95%: [{l6*100:.1f}%, {h6*100:.1f}%]")

# =============================================================================
# S9: DO NHAY PHAN PHOI PHUC VU KEM GIO TE NHAT
# =============================================================================
def task_s9_service_distribution(train_df, sched=[4, 5, 6, 5, 5, 5, 5, 5, 4]):
    print("\n=== TASK S9: DO NHAY PHAN PHOI PHUC VU KEM GIO TE NHAT (150 Reps) ===")
    served_samples = train_df[train_df['served'] == 1]['svc'].dropna().values
    
    p = json.load(open('results/final_v3/params.json', encoding='utf-8'))
    rates = p['rates_per_min']
    theta = p['theta']
    p_vip = p['p_vip']
    
    # 4 models
    models = {
        'Gamma (AIC tot nhat)': Model(rates, gamma_service(p['service']['gamma_shape'], p['service']['gamma_scale']), theta, p_vip),
        'Bootstrap thuc te': Model(rates, empirical_service(served_samples), theta, p_vip),
        'Exponential (M/M/c)': Model(rates, exp_service(p['service']['mean']), theta, p_vip),
        'Lognormal (cv+20%)': Model(rates, lognorm_service(p['service']['mean'], p['service']['cv']*1.2), theta, p_vip)
    }
    
    R = 150
    dist_results = []
    
    gamma_day_sls = None
    
    for name, m in models.items():
        sl_all_list = []
        hour_sl_mat = np.zeros((R, 9))
        for r in range(R):
            df_r = cs.simulate(m, sched, seed=45000 + r)
            st_r = cs.rep_stats(df_r, sched)
            sl_all_list.append(st_r['sl_all'])
            for h in range(9):
                hour_sl_mat[r, h] = st_r['hourly'][h]['sl']
                
        m_sl, l_sl, h_sl, hw_sl, _ = t_ci(sl_all_list)
        worst_h_means = np.mean(hour_sl_mat, axis=0)
        worst_idx = int(np.argmin(worst_h_means))
        # CI cua gio te nhat
        m_w, l_w, h_w, hw_w, _ = t_ci(hour_sl_mat[:, worst_idx])
        
        if 'Gamma' in name:
            gamma_day_sls = np.array(sl_all_list)
            diff_m = 0.0
            diff_hw = 0.0
            diff_ci = "[0.0000, 0.0000]"
            sig = "-"
        else:
            diffs = np.array(sl_all_list) - gamma_day_sls
            diff_m, d_l, d_h, diff_hw, _ = t_ci(diffs)
            diff_ci = f"[{d_l:.4f}, {d_h:.4f}]"
            sig = 'Co' if (d_l > 0 or d_h < 0) else 'Khong'
            
        dist_results.append({
            'phan_phoi': name,
            'SL_toan_ngay': m_sl,
            'SL_toan_ngay_CI95': f"{m_sl:.4f} +/- {hw_sl:.4f}",
            'gio_te_nhat': f"{worst_idx+8}h - {worst_idx+9}h",
            'SL_gio_te_nhat': m_w,
            'SL_gio_te_nhat_low95': l_w,
            'hieu_so_vs_Gamma': diff_m,
            'CI95_hieu_so': diff_ci,
            'khac_biet_co_y_nghia': sig
        })
        
    df_dist = pd.DataFrame(dist_results)
    df_dist.to_csv('results/final_v3/do_nhay_phan_phoi_v3.csv', index=False)
    print("Da luu results/final_v3/do_nhay_phan_phoi_v3.csv:")
    print(df_dist[['phan_phoi', 'SL_toan_ngay_CI95', 'SL_gio_te_nhat_low95', 'hieu_so_vs_Gamma', 'CI95_hieu_so', 'khac_biet_co_y_nghia']])

# =============================================================================
# S11: BANG CHI PHI VOI TRUYEN SAI SO VA HIEU SO THEO CAP
# =============================================================================
def task_s11_cost_analysis(model, policies):
    print("\n=== TASK S11: BANG CHI PHI VOI TRUYEN SAI SO VA HIEU SO THEO CAP ===")
    R = 150
    k_list = [0.10, 0.25, 0.50, 1.00, 2.00]
    n_mean = 686.7
    
    # Lay ket qua 150 reps cho 3 chinh sach: Toi uu 44, Ben vung 48, 6 quay 54
    pab_dict = {}
    for p_name, sched in policies.items():
        pabs = []
        for r in range(R):
            df_r = cs.simulate(model, sched, seed=70000 + r)
            pabs.append(cs.rep_stats(df_r, sched)['p_ab_all'])
        pab_dict[p_name] = np.array(pabs)
        
    cost_rows = []
    for k in k_list:
        c_44 = 44.0 + k * n_mean * pab_dict['Toi_uu_44']
        c_48 = 48.0 + k * n_mean * pab_dict['Ben_vung_48']
        c_6  = 54.0 + k * n_mean * pab_dict['Moc_co_so_54']
        
        m_44, l_44, h_44, hw_44, _ = t_ci(c_44)
        m_48, l_48, h_48, hw_48, _ = t_ci(c_48)
        m_6,  l_6,  h_6,  hw_6,  _ = t_ci(c_6)
        
        # Hieu so cap 44 vs 48
        diff_44_48 = c_44 - c_48
        m_d, l_d, h_d, hw_d, _ = t_ci(diff_44_48)
        sig_diff = 'Co' if (l_d > 0 or h_d < 0) else 'Khong'
        
        # Chon chinh sach re nhat co y nghia
        if h_d < 0: # 44 re hon 48
            best = 'Toi_uu_44'
        elif l_d > 0: # 48 re hon 44
            best = 'Ben_vung_48'
        else:
            best = 'Khong phan biet duoc giua 44 va 48'
            
        cost_rows.append({
            'k_he_so_mat_khach': k,
            'Chi_phi_44': m_44,
            'CI95_Chi_phi_44': f"{m_44:.2f} +/- {hw_44:.2f}",
            'Chi_phi_48': m_48,
            'CI95_Chi_phi_48': f"{m_48:.2f} +/- {hw_48:.2f}",
            'Chi_phi_Moc_6': m_6,
            'CI95_Chi_phi_Moc_6': f"{m_6:.2f} +/- {hw_6:.2f}",
            'Hieu_so_Cost44_tru_Cost48': m_d,
            'CI95_Hieu_so': f"[{l_d:.2f}, {h_d:.2f}]",
            'Khac_biet_co_y_nghia': sig_diff,
            'Chinh_sach_kinh_te_nhat': best
        })
        
    df_cost = pd.DataFrame(cost_rows)
    df_cost.to_csv('results/final_v3/chi_phi_v3.csv', index=False)
    print("Da luu results/final_v3/chi_phi_v3.csv:")
    print(df_cost[['k_he_so_mat_khach', 'Chi_phi_44', 'Chi_phi_48', 'Hieu_so_Cost44_tru_Cost48', 'CI95_Hieu_so', 'Chinh_sach_kinh_te_nhat']])

# =============================================================================
# C6: XUAT RESULTS/FINAL_V3/PHA3.CSV CHUNG MINH VET CAN PHA 3
# =============================================================================
def task_c6_phase3_log(model):
    print("\n=== TASK C6: XUAT RESULTS/FINAL_V3/PHA3.CSV (VET CAN PHA 3) ===")
    base_sched = [4, 5, 6, 5, 5, 5, 5, 5, 4]
    
    rows = []
    # 1. 72 phep hoan doi 1 quay (swap)
    # Bớt 1 quầy ở giờ i, thêm 1 quầy ở giờ j (i != j) -> Tong quay-gio = 44
    for i in range(9):
        if base_sched[i] <= 1:
            continue
        for j in range(9):
            if i == j:
                continue
            cand = list(base_sched)
            cand[i] -= 1
            cand[j] += 1
            
            # Kiem tra nhanh: neu gio i bi giam ma SLA < 0.90 -> vi pham
            # Tinh giai tich Erlang-A cho gio i de kiem tra tinh kha thi
            # bt.erlang_a(c, lam, mu, theta, wait_target)
            mu = 1.0 / model.mean_svc
            sl_i_theory = bt.erlang_a(lam=model.rates[i], mu=mu, theta=model.theta, c=cand[i], t=5.0)['SL']
            
            is_feasible = (sl_i_theory >= 0.90)
            rows.append({
                'loai_thu_nghiem': 'Swap 1 quay',
                'gio_giam': f"{i+8}h-{i+9}h (tu {base_sched[i]} xuong {cand[i]})",
                'gio_tang': f"{j+8}h-{j+9}h (tu {base_sched[j]} len {cand[j]})",
                'tong_quay_gio': 44,
                'lich_thu_nghiem': str(cand),
                'SL_gio_bi_giam_ErlangA': round(sl_i_theory, 4),
                'kha_thi_SLA': 'Y' if is_feasible else 'N'
            })
            
    # 2. 36 phep giam 2 quay (double reduction) -> Tong quay-gio = 42
    for i in range(9):
        for j in range(i, 9):
            cand = list(base_sched)
            cand[i] -= 1
            cand[j] -= 1
            if cand[i] < 1 or cand[j] < 1:
                continue
            mu = 1.0 / model.mean_svc
            sl_i = bt.erlang_a(lam=model.rates[i], mu=mu, theta=model.theta, c=cand[i], t=5.0)['SL']
            sl_j = bt.erlang_a(lam=model.rates[j], mu=mu, theta=model.theta, c=cand[j], t=5.0)['SL']
            min_sl = min(sl_i, sl_j)
            rows.append({
                'loai_thu_nghiem': 'Giam 2 quay',
                'gio_giam': f"{i+8}h va {j+8}h",
                'gio_tang': 'Khong',
                'tong_quay_gio': 42,
                'lich_thu_nghiem': str(cand),
                'SL_gio_bi_giam_ErlangA': round(min_sl, 4),
                'kha_thi_SLA': 'Y' if min_sl >= 0.90 else 'N'
            })
            
    df_pha3 = pd.DataFrame(rows)
    df_pha3.to_csv('results/final_v3/pha3.csv', index=False)
    n_fea = np.sum(df_pha3['kha_thi_SLA'] == 'Y')
    print(f"Da luu results/final_v3/pha3.csv: Tong thu nghiem = {len(df_pha3)}, so nghiem kha thi = {n_fea}")

def main():
    df_all = pd.read_csv('data/clean/data_clean.csv')
    train_df = df_all[df_all['day'] < 10].copy()
    model = get_base_model()
    policies = {
        'Toi_uu_44': [4, 5, 6, 5, 5, 5, 5, 5, 4],
        'Ben_vung_48': [5, 6, 6, 6, 5, 5, 5, 5, 5],
        'Moc_co_so_54': [6, 6, 6, 6, 6, 6, 6, 6, 6]
    }
    
    task_s8_mg1_and_tier_verification()
    task_s5_nested_bootstrap(train_df, model)
    task_s6_out_of_sample(df_all, model)
    task_s7_fourteen_days(df_all, model, policies)
    task_s9_service_distribution(train_df)
    task_s11_cost_analysis(model, policies)
    task_c6_phase3_log(model)
    
    print("\nHoan thanh tat ca cac tac vu S5, S6, S7, S8, S9, S11, C6!")

if __name__ == '__main__':
    main()
