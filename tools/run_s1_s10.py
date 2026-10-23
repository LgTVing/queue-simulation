"""
tools/run_s1_s10.py:
Thuc hien Task S1 (Khoang tin cay lambda_h theo Student-t)
va Task S10 (Kiem dinh nang cao cho phuc vu va kien nhan).
"""

import json
import numpy as np
import pandas as pd
import scipy.stats as st

def main():
    print("=== TASK S1: KHOANG TIN CAY LAMBDA_H THEO STUDENT-T ===")
    df = pd.read_csv('data/clean/data_clean.csv')
    
    # 1. Ma tran 14 ngay x 9 gio
    matrix_14 = df.groupby(['day', 'hour']).size().unstack(fill_value=0)
    means_14 = matrix_14.mean()
    stds_14 = matrix_14.std(ddof=1)
    n_14 = len(matrix_14) # 14
    t_val_14 = st.t.ppf(0.975, df=n_14 - 1) # df=13 -> ~2.1604
    
    poisson_hw_ngay_14 = 1.96 * np.sqrt(means_14 / n_14)
    t_hw_ngay_14 = t_val_14 * stds_14 / np.sqrt(n_14)
    ratio_14 = t_hw_ngay_14 / poisson_hw_ngay_14
    
    df_s1 = pd.DataFrame({
        'gio': range(9),
        'khung_gio': [f"{h+8}h - {h+9}h" for h in range(9)],
        'mean_khach_ngay': means_14.values,
        'std_khach_ngay': stds_14.values,
        'poisson_hw_ngay': poisson_hw_ngay_14.values,
        't_hw_ngay': t_hw_ngay_14.values,
        'ti_so_t_vs_poisson': ratio_14.values,
        'lambda_phut': (means_14 / 60.0).values,
        'poisson_hw_phut': (poisson_hw_ngay_14 / 60.0).values,
        't_hw_phut': (t_hw_ngay_14 / 60.0).values,
        'lambda_low_ci95': ((means_14 - t_hw_ngay_14) / 60.0).values,
        'lambda_high_ci95': ((means_14 + t_hw_ngay_14) / 60.0).values
    })
    df_s1.to_csv('results/final_v3/khoang_tin_cay_lambda.csv', index=False)
    print("Da luu results/final_v3/khoang_tin_cay_lambda.csv")
    print(df_s1[['khung_gio', 'poisson_hw_ngay', 't_hw_ngay', 'ti_so_t_vs_poisson', 'lambda_low_ci95', 'lambda_high_ci95']])
    
    # 2. Tap Train (10 ngay) de cap nhat params.json
    train_df = df[df['day'] < 10]
    matrix_10 = train_df.groupby(['day', 'hour']).size().unstack(fill_value=0)
    means_10 = matrix_10.mean()
    stds_10 = matrix_10.std(ddof=1)
    n_10 = len(matrix_10) # 10
    t_val_10 = st.t.ppf(0.975, df=n_10 - 1) # df=9 -> ~2.2622
    t_hw_phut_10 = (t_val_10 * stds_10 / np.sqrt(n_10)) / 60.0
    
    # Cap nhat params.json v3
    with open('results/final_v2/params.json', 'r', encoding='utf-8') as f:
        p_dict = json.load(f)
    
    p_dict['version'] = 'v3.0'
    p_dict['ngay_chot'] = '2026-10-23'
    p_dict['rates_ci95'] = [round(float(x), 4) for x in t_hw_phut_10.values]
    p_dict['rates_ci95_method'] = 'Student-t across 10 train days (accounting for empirical overdispersion)'
    
    with open('results/final_v3/params.json', 'w', encoding='utf-8') as f:
        json.dump(p_dict, f, indent=2, ensure_ascii=False)
    print("Da cap nhat results/final_v3/params.json voi rates_ci95 Student-t.")
    
    print("\n=== TASK S10: PHAN TICH CHUYEN SAU PHAN PHOI PHUC VU & KIEN NHAN ===")
    # Phuc vu tap Train
    svc_data = train_df[train_df['served'] == 1]['svc'].dropna().values
    n_svc = len(svc_data)
    
    # Fit 4 phan phoi
    # 1. Gamma
    g_a, g_loc, g_scale = st.gamma.fit(svc_data, floc=0)
    ll_gamma = np.sum(st.gamma.logpdf(svc_data, g_a, loc=0, scale=g_scale))
    aic_gamma = 2 * 2 - 2 * ll_gamma
    bic_gamma = 2 * np.log(n_svc) - 2 * ll_gamma
    ks_gamma, _ = st.kstest(svc_data, 'gamma', args=(g_a, 0, g_scale))
    
    # 2. Lognormal
    ln_s, ln_loc, ln_scale = st.lognorm.fit(svc_data, floc=0)
    ll_ln = np.sum(st.lognorm.logpdf(svc_data, ln_s, loc=0, scale=ln_scale))
    aic_ln = 2 * 2 - 2 * ll_ln
    bic_ln = 2 * np.log(n_svc) - 2 * ll_ln
    ks_ln, _ = st.kstest(svc_data, 'lognorm', args=(ln_s, 0, ln_scale))
    
    # 3. Weibull
    w_c, w_loc, w_scale = st.weibull_min.fit(svc_data, floc=0)
    ll_weibull = np.sum(st.weibull_min.logpdf(svc_data, w_c, loc=0, scale=w_scale))
    aic_weibull = 2 * 2 - 2 * ll_weibull
    bic_weibull = 2 * np.log(n_svc) - 2 * ll_weibull
    ks_weibull, _ = st.kstest(svc_data, 'weibull_min', args=(w_c, 0, w_scale))
    
    # 4. Exponential
    e_loc, e_scale = st.expon.fit(svc_data, floc=0)
    ll_expon = np.sum(st.expon.logpdf(svc_data, loc=0, scale=e_scale))
    aic_expon = 2 * 1 - 2 * ll_expon
    bic_expon = 1 * np.log(n_svc) - 2 * ll_expon
    ks_expon, _ = st.kstest(svc_data, 'expon', args=(0, e_scale))
    
    # Bootstrap p-value cho KS test (Lilliefors-type parametric bootstrap)
    def bootstrap_ks_pvalue(dist_name, fit_params, orig_ks, B=500):
        ks_sims = []
        for _ in range(B):
            if dist_name == 'gamma':
                sim = st.gamma.rvs(fit_params[0], scale=fit_params[1], size=min(1000, n_svc))
                p_sim = st.gamma.fit(sim, floc=0)
                ks_val, _ = st.kstest(sim, 'gamma', args=(p_sim[0], 0, p_sim[2]))
            elif dist_name == 'lognorm':
                sim = st.lognorm.rvs(fit_params[0], scale=fit_params[1], size=min(1000, n_svc))
                p_sim = st.lognorm.fit(sim, floc=0)
                ks_val, _ = st.kstest(sim, 'lognorm', args=(p_sim[0], 0, p_sim[2]))
            elif dist_name == 'weibull':
                sim = st.weibull_min.rvs(fit_params[0], scale=fit_params[1], size=min(1000, n_svc))
                p_sim = st.weibull_min.fit(sim, floc=0)
                ks_val, _ = st.kstest(sim, 'weibull_min', args=(p_sim[0], 0, p_sim[2]))
            else:
                sim = st.expon.rvs(scale=fit_params[0], size=min(1000, n_svc))
                p_sim = st.expon.fit(sim, floc=0)
                ks_val, _ = st.kstest(sim, 'expon', args=(0, p_sim[1]))
            ks_sims.append(ks_val)
        return np.mean(np.array(ks_sims) >= orig_ks)
    
    p_boot_gamma = bootstrap_ks_pvalue('gamma', (g_a, g_scale), ks_gamma, B=300)
    p_boot_ln = bootstrap_ks_pvalue('lognorm', (ln_s, ln_scale), ks_ln, B=300)
    p_boot_weibull = bootstrap_ks_pvalue('weibull', (w_c, w_scale), ks_weibull, B=300)
    p_boot_expon = bootstrap_ks_pvalue('expon', (e_scale,), ks_expon, B=300)
    
    df_fit = pd.DataFrame([
        {'phan_phoi': 'Gamma', 'tham_so': f"shape={g_a:.4f}, scale={g_scale:.4f}", 'log_likelihood': ll_gamma, 'AIC': aic_gamma, 'BIC': bic_gamma, 'KS_stat': ks_gamma, 'KS_pvalue_boot': p_boot_gamma},
        {'phan_phoi': 'Lognormal', 'tham_so': f"s={ln_s:.4f}, scale={ln_scale:.4f}", 'log_likelihood': ll_ln, 'AIC': aic_ln, 'BIC': bic_ln, 'KS_stat': ks_ln, 'KS_pvalue_boot': p_boot_ln},
        {'phan_phoi': 'Weibull', 'tham_so': f"shape={w_c:.4f}, scale={w_scale:.4f}", 'log_likelihood': ll_weibull, 'AIC': aic_weibull, 'BIC': bic_weibull, 'KS_stat': ks_weibull, 'KS_pvalue_boot': p_boot_weibull},
        {'phan_phoi': 'Exponential', 'tham_so': f"scale={e_scale:.4f}", 'log_likelihood': ll_expon, 'AIC': aic_expon, 'BIC': bic_expon, 'KS_stat': ks_expon, 'KS_pvalue_boot': p_boot_expon}
    ])
    df_fit.to_csv('results/final_v3/kiem_dinh_phan_phoi_chi_tiet.csv', index=False)
    print("Da luu results/final_v3/kiem_dinh_phan_phoi_chi_tiet.csv:")
    print(df_fit[['phan_phoi', 'AIC', 'BIC', 'KS_stat', 'KS_pvalue_boot']])
    
    # Kaplan-Meier cho kien nhan khach hang
    # Khach bo ve: event = 1 (thoi gian kiem duyet la wait)
    # Khach duoc phuc vu: event = 0 (right-censored tai wait)
    # Chi xet nhung khach co wait > 0
    waiting_customers = train_df[train_df['wait'] > 0].copy()
    times = waiting_customers['wait'].values
    events = (waiting_customers['served'] == 0).astype(int).values # 1 if abandoned
    
    # Tinh Kaplan-Meier thu cong
    unique_times = np.sort(np.unique(times[events == 1]))
    km_data = []
    S_t = 1.0
    for t_i in unique_times:
        d_i = np.sum((times == t_i) & (events == 1))
        n_i = np.sum(times >= t_i)
        if n_i > 0:
            S_t *= (1.0 - d_i / n_i)
            # Hazard rate xap xi: d_i / (n_i * dt)
            km_data.append({'time': t_i, 'at_risk': n_i, 'events': d_i, 'survival_km': S_t, 'survival_expon': np.exp(-0.1087 * t_i)})
    df_km = pd.DataFrame(km_data)
    df_km.to_csv('results/final_v3/patience_km.csv', index=False)
    print("Da luu results/final_v3/patience_km.csv (so moc:", len(df_km), ")")
    
    # Cluster bootstrap theo ngay cho E[S] va theta
    print("\n--- Cluster Bootstrap theo ngay (1.000 reps) ---")
    days = train_df['day'].unique()
    boot_es = []
    boot_theta = []
    for _ in range(1000):
        sampled_days = np.random.choice(days, size=len(days), replace=True)
        boot_df = pd.concat([train_df[train_df['day'] == d] for d in sampled_days])
        
        # E[S]
        s_vals = boot_df[boot_df['served'] == 1]['svc'].dropna()
        boot_es.append(s_vals.mean())
        
        # theta MLE: so khach bo ve / tong thoi gian cho
        n_ab = np.sum(boot_df['served'] == 0)
        tot_wait = np.sum(boot_df['wait'])
        if tot_wait > 0:
            boot_theta.append(n_ab / tot_wait)
            
    es_low, es_high = np.percentile(boot_es, [2.5, 97.5])
    th_low, th_high = np.percentile(boot_theta, [2.5, 97.5])
    print(f"E[S] cluster bootstrap CI95: [{es_low:.4f}, {es_high:.4f}] (mean = {np.mean(boot_es):.4f})")
    print(f"theta cluster bootstrap CI95: [{th_low:.4f}, {th_high:.4f}] (mean = {np.mean(boot_theta):.4f})")
    
    cluster_df = pd.DataFrame([
        {'tham_so': 'E[S] (phut)', 'point_est': 2.9236, 'cluster_boot_ci_low': es_low, 'cluster_boot_ci_high': es_high, 'se_cluster': np.std(boot_es)},
        {'tham_so': 'theta (phut^-1)', 'point_est': 0.1087, 'cluster_boot_ci_low': th_low, 'cluster_boot_ci_high': th_high, 'se_cluster': np.std(boot_theta)}
    ])
    cluster_df.to_csv('results/final_v3/cluster_bootstrap_params.csv', index=False)
    print("Da luu results/final_v3/cluster_bootstrap_params.csv")

if __name__ == '__main__':
    main()
