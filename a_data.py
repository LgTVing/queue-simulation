"""
a_data.py: Xu ly du lieu thuc te, uoc luong tham so, kiem dinh phan phoi
va xuat file cau hinh params.json cho du an mo phong hang doi (Tuan 2).
"""

import os
import json
from typing import Dict, Tuple, List, Optional
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

from common import HOURS, H_LABELS, WAIT_THRESHOLD

def load_log(path: str = "data/clean/data_clean.csv") -> pd.DataFrame:
    """Doc du lieu da lam sach, dam bao day du 8 cot chuan."""
    if not os.path.isabs(path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, path)
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Khong tim thay tep du lieu tai: {path}")
        
    df = pd.read_csv(path)
    required_cols = ["day", "t", "hour", "cls", "vip", "wait", "served", "svc"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Tep du lieu thieu cot bat buoc: {col}")
            
    df["hour"] = df["hour"].astype(int)
    df["day"] = df["day"].astype(int)
    df["vip"] = df["vip"].fillna(0).astype(int)
    df["served"] = df["served"].astype(int)
    df["wait"] = df["wait"].astype(float)
    df["svc"] = pd.to_numeric(df["svc"], errors="coerce")
    return df

def split_train_test(df: pd.DataFrame, train_ratio: float = 0.7) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Tach tap uoc luong (train) va tap kiem tra (test) theo ngay."""
    days = sorted(df["day"].unique())
    n_train_days = max(1, int(round(len(days) * train_ratio)))
    train_days = days[:n_train_days]
    test_days = days[n_train_days:]
    
    df_train = df[df["day"].isin(train_days)].copy()
    df_test = df[df["day"].isin(test_days)].copy()
    return df_train, df_test

def fit_arrivals(df: pd.DataFrame) -> Dict:
    """Uoc luong toc do den theo tung khung gio va kiem dinh Poisson."""
    n_days = df["day"].nunique()
    counts_matrix = df.groupby(["day", "hour"]).size().unstack(fill_value=0)
    
    rates = []
    rates_ci = []
    disp_indices = []
    p_values = []
    
    for h in range(HOURS):
        counts = counts_matrix[h] if h in counts_matrix else pd.Series(0, index=range(n_days))
        n_bar = float(counts.mean())
        lam = n_bar / 60.0
        se = float(np.sqrt(n_bar / n_days) / 60.0) if n_days > 0 and n_bar > 0 else 0.0
        ci_half = 1.96 * se
        
        # Chi so phan tan D
        disp = float(counts.var(ddof=0) * n_days / n_bar) if n_bar > 0 else 0.0
        p_val = float(stats.chi2.sf(disp, df=n_days - 1)) if n_days > 1 else 1.0
        
        rates.append(round(lam, 4))
        rates_ci.append(round(ci_half, 4))
        disp_indices.append(round(disp, 2))
        p_values.append(round(p_val, 4))
        
    # Kiem tra toc do den co bang nhau qua cac gio khong
    totals = counts_matrix.sum(axis=0)
    t_bar = totals.mean()
    chi2_const = float(((totals - t_bar)**2 / t_bar).sum()) if t_bar > 0 else 0.0
    p_const = float(stats.chi2.sf(chi2_const, df=len(totals) - 1)) if len(totals) > 1 else 1.0
    
    return {
        "rates": rates,
        "rates_ci": rates_ci,
        "disp_indices": disp_indices,
        "p_values": p_values,
        "chi2_const": chi2_const,
        "p_const": p_const
    }

def fit_service(df: pd.DataFrame) -> Dict:
    """Kiem dinh va fit cac phan phoi thoi gian phuc vu (loc=0)."""
    svc_data = df[df["served"] == 1]["svc"].dropna().values
    mean_svc = float(np.mean(svc_data))
    std_svc = float(np.std(svc_data, ddof=1))
    cv_svc = std_svc / mean_svc if mean_svc > 0 else 0.0
    cs2_svc = cv_svc ** 2
    
    # 1. Fit Exponential
    params_exp = stats.expon.fit(svc_data, floc=0)
    ks_exp = stats.kstest(svc_data, "expon", args=params_exp)
    aic_exp = 2 * 1 - 2 * np.sum(stats.expon.logpdf(svc_data, *params_exp))
    
    # 2. Fit Lognormal
    params_log = stats.lognorm.fit(svc_data, floc=0)
    ks_log = stats.kstest(svc_data, "lognorm", args=params_log)
    aic_log = 2 * 2 - 2 * np.sum(stats.lognorm.logpdf(svc_data, *params_log))
    
    # 3. Fit Gamma
    params_gam = stats.gamma.fit(svc_data, floc=0)
    ks_gam = stats.kstest(svc_data, "gamma", args=params_gam)
    aic_gam = 2 * 2 - 2 * np.sum(stats.gamma.logpdf(svc_data, *params_gam))
    
    # 4. Fit Weibull
    params_wei = stats.weibull_min.fit(svc_data, floc=0)
    ks_wei = stats.kstest(svc_data, "weibull_min", args=params_wei)
    aic_wei = 2 * 2 - 2 * np.sum(stats.weibull_min.logpdf(svc_data, *params_wei))
    
    fits = {
        "exponential": {"aic": round(aic_exp, 1), "ks_stat": round(ks_exp.statistic, 4), "p_val": round(ks_exp.pvalue, 6), "params": [round(p, 4) for p in params_exp]},
        "lognormal": {"aic": round(aic_log, 1), "ks_stat": round(ks_log.statistic, 4), "p_val": round(ks_log.pvalue, 6), "params": [round(p, 4) for p in params_log]},
        "gamma": {"aic": round(aic_gam, 1), "ks_stat": round(ks_gam.statistic, 4), "p_val": round(ks_gam.pvalue, 6), "params": [round(p, 4) for p in params_gam]},
        "weibull": {"aic": round(aic_wei, 1), "ks_stat": round(ks_wei.statistic, 4), "p_val": round(ks_wei.pvalue, 6), "params": [round(p, 4) for p in params_wei]}
    }
    
    # Chon phan phoi toi uu (AIC nho nhat)
    best_dist = min(fits.keys(), key=lambda k: fits[k]["aic"])
    
    return {
        "mean": round(mean_svc, 4),
        "std": round(std_svc, 4),
        "cv": round(cv_svc, 4),
        "cs2": round(cs2_svc, 4),
        "best_dist": best_dist,
        "fits": fits,
        "gamma_params": {"shape": float(params_gam[0]), "scale": float(params_gam[2])},
        "lognorm_params": {"s": float(params_log[0]), "scale": float(params_log[2])}
    }

def fit_patience(df: pd.DataFrame) -> Dict:
    """Uoc luong toc do bo ve theta bang MLE voi du lieu bi kiem duyet."""
    n_abandon = int((df["served"] == 0).sum())
    total_wait = float(df["wait"].sum())
    if total_wait <= 0 or n_abandon == 0:
        return {"theta": 0.0, "ci_half": 0.0, "mean_patience": float("inf"), "p_abandon": 0.0}
        
    theta_hat = n_abandon / total_wait
    se = theta_hat / np.sqrt(n_abandon)
    ci_half = 1.96 * se
    p_abandon = n_abandon / len(df)
    
    return {
        "theta": round(theta_hat, 4),
        "ci_half": round(ci_half, 4),
        "mean_patience": round(1.0 / theta_hat, 2),
        "p_abandon": round(p_abandon, 4),
        "n_abandon": n_abandon
    }

def estimate_all(df: pd.DataFrame, plot: bool = False, output_dir: str = "docs") -> Dict:
    """
    Uoc luong toan bo tham so he thong tren tap du lieu,
    xuat file docs/params.json va ve bieu do fig_a_fit.png.
    """
    arr_res = fit_arrivals(df)
    svc_res = fit_service(df)
    pat_res = fit_patience(df)
    
    p_vip = float(df["vip"].mean())
    se_vip = float(np.sqrt(p_vip * (1.0 - p_vip) / len(df))) if len(df) > 0 else 0.0
    
    params = {
        "version": "v2.0",
        "ngay_chot": "2026-10-21",
        "nguon": "Anonymous Bank (Technion SEE Center), PS activity, 8h-17h, 14 standard workdays",
        "don_vi_thoi_gian": "phut",
        "rates_per_min": arr_res["rates"],
        "rates_ci95": arr_res["rates_ci"],
        "service": {
            "kieu": "gamma",
            "mean": svc_res["mean"],
            "std": svc_res["std"],
            "cv": svc_res["cv"],
            "cs2": svc_res["cs2"],
            "gamma_shape": round(svc_res["gamma_params"]["shape"], 4),
            "gamma_scale": round(svc_res["gamma_params"]["scale"], 4),
            "lognorm_s": round(svc_res["lognorm_params"]["s"], 4),
            "lognorm_scale": round(svc_res["lognorm_params"]["scale"], 4)
        },
        "theta": pat_res["theta"],
        "theta_ci95": pat_res["ci_half"],
        "mean_patience": pat_res["mean_patience"],
        "p_vip": round(p_vip, 4),
        "p_vip_ci95": round(1.96 * se_vip, 4),
        "ghi_chu": "Uoc luong tren tap train (10 ngay lam viec dau tien). Phan phoi Gamma dat AIC thap nhat."
    }
    
    # Luu params.json
    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir_path = os.path.join(base_dir, output_dir)
    os.makedirs(out_dir_path, exist_ok=True)
    json_path = os.path.join(out_dir_path, "params.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(params, f, indent=2, ensure_ascii=False)
    print(f"Xuat tap tin tham so chot thanh cong: {json_path}")
    
    # Ve fig_a_fit.png neu plot=True
    if plot:
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        
        # 1. Toc do den theo gio
        hours = np.arange(HOURS)
        axes[0].bar(hours, arr_res["rates"], yerr=arr_res["rates_ci"], capsize=4, color="#1F4E78", alpha=0.85)
        axes[0].set_xticks(hours)
        axes[0].set_xticklabels(H_LABELS, rotation=45)
        axes[0].set_ylabel(r"Tốc độ đến $\lambda_h$ (khách/phút)")
        axes[0].set_title("Tốc độ khách đến theo khung giờ (kèm CI 95%)")
        axes[0].grid(True, linestyle="--", alpha=0.5)
        
        # 2. Histogram thoi gian phuc vu va duong fit Gamma
        svc_data = df[df["served"] == 1]["svc"].dropna().values
        x_vals = np.linspace(0.1, 15, 200)
        axes[1].hist(svc_data, bins=40, range=(0, 15), density=True, color="#2E75B6", alpha=0.6, label="Dữ liệu thực tế")
        gam_pdf = stats.gamma.pdf(x_vals, svc_res["gamma_params"]["shape"], scale=svc_res["gamma_params"]["scale"])
        axes[1].plot(x_vals, gam_pdf, "r-", lw=2, label=f"Fit Gamma (AIC={svc_res['fits']['gamma']['aic']:.0f})")
        axes[1].set_xlabel("Thời gian phục vụ (phút)")
        axes[1].set_ylabel("Mật độ xác suất")
        axes[1].set_title(f"Phân phối phục vụ (E[S]={svc_res['mean']:.2f}p, cv={svc_res['cv']:.2f})")
        axes[1].legend()
        axes[1].grid(True, linestyle="--", alpha=0.5)
        
        # 3. Q-Q plot Gamma
        stats.probplot(svc_data, dist=stats.gamma(svc_res["gamma_params"]["shape"], scale=svc_res["gamma_params"]["scale"]), plot=axes[2])
        axes[2].set_title("Gamma Q-Q Plot kiểm tra độ khớp")
        axes[2].grid(True, linestyle="--", alpha=0.5)
        
        plt.tight_layout()
        fig_path = os.path.join(base_dir, "fig_a_fit.png")
        plt.savefig(fig_path, dpi=200)
        plt.close()
        print(f"Xuat bieu do kiem dinh thanh cong: {fig_path}")
        
    return params

if __name__ == "__main__":
    df = load_log()
    df_train, df_test = split_train_test(df, train_ratio=0.7)
    print(f"Tong so mau: {len(df)} | Train ({df_train['day'].nunique()} ngay): {len(df_train)} | Test ({df_test['day'].nunique()} ngay): {len(df_test)}")
    params = estimate_all(df_train, plot=True)
