"""
a_data.py: Xu ly du lieu thuc te, uoc luong tham so, kiem dinh phan phoi
va xuat file cau hinh params.json cho du an mo phong hang doi.
V4 bo sung (hop nhat tu tools/):
- S1: khoang tin cay Student-t cho lambda_h
- T1: kiem dinh Poisson theo gio va qua phan tan theo ngay
- S10: kiem dinh phan phoi phuc vu (AIC/BIC/KS bootstrap), Kaplan-Meier kien nhan,
  cluster bootstrap theo ngay cho E[S] va theta
- M4: dieu tra khung gio bat thuong ngoai mau va uoc luong so nhan vien thuc te
  tu so phien phuc vu chong lan
"""

import os
import json
import datetime
from typing import Dict, Tuple, List, Optional
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import common
from common import (
    HOURS, H_LABELS, WAIT_THRESHOLD, Model,
    gamma_service, empirical_service
)

def load_log(path: str = common.DATA_CLEAN) -> pd.DataFrame:
    """Doc du lieu da lam sach, dam bao day du 8 cot chuan."""
    if not os.path.isabs(path):
        path = os.path.join(common.BASE_DIR, path)

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

def counts_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Ma tran so khach den theo ngay x gio."""
    return df.groupby(["day", "hour"]).size().unstack(fill_value=0).reindex(columns=range(HOURS), fill_value=0)

def day_cv(df: pd.DataFrame) -> float:
    """
    CV cua he so nhan ngay sau khi tru nhieu Poisson:
    CV^2 = (Var(N_d) - mean(N_d)) / mean(N_d)^2.
    """
    totals = counts_matrix(df).sum(axis=1).values.astype(float)
    mu = float(np.mean(totals))
    cv2 = max(0.0, (float(np.var(totals, ddof=1)) - mu) / mu ** 2)
    return float(np.sqrt(cv2))

def fit_arrivals(df: pd.DataFrame) -> Dict:
    """
    Uoc luong toc do den theo tung khung gio va kiem dinh Poisson.
    rates_ci: nua do rong CI95 theo cong thuc Poisson.
    rates_ci_t: nua do rong CI95 Student-t qua cac ngay (tinh ca qua phan tan, S1).
    """
    n_days = df["day"].nunique()
    cm = counts_matrix(df)
    t_val = stats.t.ppf(0.975, df=n_days - 1) if n_days > 1 else 0.0

    rates = []
    rates_ci = []
    rates_ci_t = []
    disp_indices = []
    p_values = []

    for h in range(HOURS):
        counts = cm[h]
        n_bar = float(counts.mean())
        lam = n_bar / 60.0
        se = float(np.sqrt(n_bar / n_days) / 60.0) if n_days > 0 and n_bar > 0 else 0.0
        ci_half = 1.96 * se
        ci_t = float(t_val * counts.std(ddof=1) / np.sqrt(n_days) / 60.0) if n_days > 1 else 0.0

        # Chi so phan tan D
        disp = float(counts.var(ddof=0) * n_days / n_bar) if n_bar > 0 else 0.0
        p_val = float(stats.chi2.sf(disp, df=n_days - 1)) if n_days > 1 else 1.0

        rates.append(round(lam, 4))
        rates_ci.append(round(ci_half, 4))
        rates_ci_t.append(round(ci_t, 4))
        disp_indices.append(round(disp, 2))
        p_values.append(round(p_val, 4))

    # Kiem tra toc do den co bang nhau qua cac gio khong
    totals = cm.sum(axis=0)
    t_bar = totals.mean()
    chi2_const = float(((totals - t_bar)**2 / t_bar).sum()) if t_bar > 0 else 0.0
    p_const = float(stats.chi2.sf(chi2_const, df=len(totals) - 1)) if len(totals) > 1 else 1.0

    return {
        "rates": rates,
        "rates_ci": rates_ci,
        "rates_ci_t": rates_ci_t,
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

def estimate_all(df: pd.DataFrame, plot: bool = False, output_dir: Optional[str] = None) -> Dict:
    """
    Uoc luong toan bo tham so he thong tren tap du lieu (tap train),
    xuat params.json vao output_dir (mac dinh common.RESULTS_DIR) va ban sao docs/params.json,
    ve bieu do fig_a_fit.png vao thu muc hinh.
    V4: mo hinh phuc vu chinh la phan phoi thuc nghiem (bootstrap tu tap train, M3);
    tham so Gamma giu lai cho phan tich do nhay.
    """
    output_dir = output_dir or common.RESULTS_DIR
    arr_res = fit_arrivals(df)
    svc_res = fit_service(df)
    pat_res = fit_patience(df)

    p_vip = float(df["vip"].mean())
    se_vip = float(np.sqrt(p_vip * (1.0 - p_vip) / len(df))) if len(df) > 0 else 0.0

    params = {
        "version": "v4.0",
        "ngay_chot": datetime.date.today().isoformat(),
        "nguon": "Anonymous Bank (Technion SEE Center), PS activity, 8h-17h, 14 standard workdays",
        "don_vi_thoi_gian": "phut",
        "rates_per_min": arr_res["rates"],
        "rates_ci95": arr_res["rates_ci_t"],
        "rates_ci95_method": f"Student-t qua {df['day'].nunique()} ngay train (tinh ca qua phan tan)",
        "rates_ci95_poisson": arr_res["rates_ci"],
        "day_cv": round(day_cv(df), 4),
        "service": {
            "kieu": "empirical",
            "n_mau": int(df[df["served"] == 1]["svc"].notna().sum()),
            "mean": svc_res["mean"],
            "std": svc_res["std"],
            "cv": svc_res["cv"],
            "cs2": svc_res["cs2"],
            "gamma_shape": round(svc_res["gamma_params"]["shape"], 4),
            "gamma_scale": round(svc_res["gamma_params"]["scale"], 4),
            "gamma_cs2": round(1.0 / svc_res["gamma_params"]["shape"], 4),
            "lognorm_s": round(svc_res["lognorm_params"]["s"], 4),
            "lognorm_scale": round(svc_res["lognorm_params"]["scale"], 4),
            "best_aic": svc_res["best_dist"]
        },
        "theta": pat_res["theta"],
        "theta_ci95": pat_res["ci_half"],
        "mean_patience": pat_res["mean_patience"],
        "p_abandon": pat_res["p_abandon"],
        "p_vip": round(p_vip, 4),
        "p_vip_ci95": round(1.96 * se_vip, 4),
        "ghi_chu": ("Uoc luong tren tap train (10 ngay lam viec dau tien). Mo hinh phuc vu chinh: "
                    "lay mau co hoan lai tu thoi gian phuc vu tap train (KS bac bo ca 4 phan phoi "
                    "tham so; Gamma danh gia thap cs^2). Gamma dung cho phan tich do nhay.")
    }

    # Luu params.json (ket qua dong bang + ban sao trong docs/, tru khi chay thu vao QS_RESULTS_DIR)
    os.makedirs(output_dir, exist_ok=True)
    json_paths = [os.path.join(output_dir, "params.json")]
    if not os.environ.get("QS_RESULTS_DIR"):
        json_paths.append(os.path.join(common.BASE_DIR, "docs", "params.json"))
    for json_path in json_paths:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(params, f, indent=2, ensure_ascii=False)
        print(f"Xuat tap tin tham so: {json_path}")

    # Ve fig_a_fit.png neu plot=True
    if plot:
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))

        # 1. Toc do den theo gio
        hours = np.arange(HOURS)
        axes[0].bar(hours, arr_res["rates"], yerr=arr_res["rates_ci_t"], capsize=4, color="#1F4E78", alpha=0.85)
        axes[0].set_xticks(hours)
        axes[0].set_xticklabels(H_LABELS, rotation=45)
        axes[0].set_ylabel(r"Tốc độ đến $\lambda_h$ (khách/phút)")
        axes[0].set_title("Tốc độ khách đến theo khung giờ (CI 95% Student-t)")
        axes[0].grid(True, linestyle="--", alpha=0.5)

        # 2. Histogram thoi gian phuc vu va duong fit Gamma
        svc_data = df[df["served"] == 1]["svc"].dropna().values
        x_vals = np.linspace(0.1, 15, 200)
        axes[1].hist(svc_data, bins=40, range=(0, 15), density=True, color="#2E75B6", alpha=0.6, label="Dữ liệu thực tế (mô hình chính)")
        gam_pdf = stats.gamma.pdf(x_vals, svc_res["gamma_params"]["shape"], scale=svc_res["gamma_params"]["scale"])
        axes[1].plot(x_vals, gam_pdf, "r-", lw=2, label=f"Fit Gamma (AIC={svc_res['fits']['gamma']['aic']:.0f})")
        axes[1].set_xlabel("Thời gian phục vụ (phút)")
        axes[1].set_ylabel("Mật độ xác suất")
        axes[1].set_title(f"Phân phối phục vụ (E[S]={svc_res['mean']:.2f}p, cs²={svc_res['cs2']:.2f})")
        axes[1].legend()
        axes[1].grid(True, linestyle="--", alpha=0.5)

        # 3. Q-Q plot Gamma
        stats.probplot(svc_data, dist=stats.gamma(svc_res["gamma_params"]["shape"], scale=svc_res["gamma_params"]["scale"]), plot=axes[2])
        axes[2].set_title("Gamma Q-Q Plot kiểm tra độ khớp")
        axes[2].grid(True, linestyle="--", alpha=0.5)

        plt.tight_layout()
        fig_path = common.out_path("fig_a_fit.png", "hinh")
        plt.savefig(fig_path, dpi=200)
        plt.close()
        print(f"Xuat bieu do kiem dinh thanh cong: {fig_path}")

    return params

def train_service_samples(df_train: pd.DataFrame) -> np.ndarray:
    """Mau thoi gian phuc vu cua khach duoc phuc vu trong tap train."""
    return df_train[df_train["served"] == 1]["svc"].dropna().values.astype(float)

def build_model(params: Dict, svc_samples: np.ndarray, service: str = "empirical") -> Model:
    """
    Tao Model tu params.json.
    service = 'empirical' (mo hinh chinh V4, lay mau tu svc_samples) hoac 'gamma' (do nhay).
    """
    svc = params["service"]
    if service == "empirical":
        sampler = empirical_service(svc_samples)
        mean_s = float(np.mean(svc_samples))
        cs2 = float(np.var(svc_samples, ddof=1) / mean_s ** 2)
    elif service == "gamma":
        sampler = gamma_service(svc["gamma_shape"], svc["gamma_scale"])
        mean_s = svc["gamma_shape"] * svc["gamma_scale"]
        cs2 = 1.0 / svc["gamma_shape"]
    else:
        raise ValueError(f"Loai mo hinh phuc vu khong hop le: {service}")
    return Model(
        rates=list(params["rates_per_min"]),
        service=sampler,
        theta=params["theta"],
        p_vip=params["p_vip"],
        hour_len=common.DEFAULT_HOUR_LEN,
        mean_svc=mean_s,
        cs2_svc=cs2
    )

# =============================================================================
# S1 / T1: KHOANG TIN CAY LAMBDA_H VA KIEM DINH POISSON, QUA PHAN TAN
# =============================================================================

def poisson_label(p_val: float) -> str:
    """Gan nhan kiem dinh Poisson theo quy tac tuong minh."""
    if p_val < 0.01:
        return "Bác bỏ (mạnh)"
    elif p_val < 0.05:
        return "Bác bỏ (nhẹ)"
    return "Chưa bác bỏ"

def lambda_ci_table(df: pd.DataFrame) -> pd.DataFrame:
    """S1: CI95 cua lambda_h theo Poisson va Student-t qua cac ngay (14 ngay)."""
    cm = counts_matrix(df)
    n = len(cm)
    means = cm.mean()
    stds = cm.std(ddof=1)
    t_val = stats.t.ppf(0.975, df=n - 1)
    poi_hw = 1.96 * np.sqrt(means / n)
    t_hw = t_val * stds / np.sqrt(n)
    return pd.DataFrame({
        "gio": range(HOURS),
        "khung_gio": H_LABELS,
        "mean_khach_ngay": means.values,
        "std_khach_ngay": stds.values,
        "poisson_hw_ngay": poi_hw.values,
        "t_hw_ngay": t_hw.values,
        "ti_so_t_vs_poisson": (t_hw / poi_hw).values,
        "lambda_phut": (means / 60.0).values,
        "lambda_low_ci95": ((means - t_hw) / 60.0).values,
        "lambda_high_ci95": ((means + t_hw) / 60.0).values
    })

def poisson_overdispersion(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    T1: Kiem dinh phan tan chi^2 theo tung gio (nhan chuan) va qua phan tan
    cua tong khach theo ngay, uoc luong CV ngay sau hieu chinh Poisson.
    """
    cm = counts_matrix(df)
    n_days = len(cm)
    rows = []
    for h in range(HOURS):
        x = cm[h].values.astype(float)
        n_bar = float(x.mean())
        disp = float(np.sum((x - n_bar) ** 2) / n_bar) if n_bar > 0 else 0.0
        p_val = float(stats.chi2.sf(disp, df=n_days - 1))
        rows.append({"hour": h, "label": H_LABELS[h], "n_bar": round(n_bar, 2),
                     "lambda": round(n_bar / 60.0, 4), "D": round(disp, 2),
                     "p_value": round(p_val, 4), "nhan": poisson_label(p_val)})
    totals = cm.sum(axis=1).values.astype(float)
    mu = float(totals.mean())
    var = float(totals.var(ddof=1))
    d_day = float(np.sum((totals - mu) ** 2) / mu)
    p_day = float(stats.chi2.sf(d_day, df=n_days - 1))
    over = {
        "n_days": n_days,
        "daily_totals": str(totals.astype(int).tolist()),
        "mean_day": round(mu, 1),
        "std_day": round(np.sqrt(var), 1),
        "var_day": round(var, 1),
        "poisson_std": round(np.sqrt(mu), 1),
        "var_mean_ratio": round(var / mu, 1),
        "cv_day": round(np.sqrt(var) / mu * 100, 1),
        "cv2_day_corrected": round((var - mu) / mu ** 2, 4),
        "cv_day_corrected": round(day_cv(df) * 100, 1),
        "D_day": round(d_day, 1),
        "p_day": p_day,
        "p_day_label": poisson_label(p_day)
    }
    return pd.DataFrame(rows), pd.DataFrame([over])

# =============================================================================
# S10: PHAN PHOI PHUC VU, KIEN NHAN (KAPLAN-MEIER), CLUSTER BOOTSTRAP
# =============================================================================

_DISTS = {
    "Gamma": (stats.gamma, 2),
    "Lognormal": (stats.lognorm, 2),
    "Weibull": (stats.weibull_min, 2),
    "Exponential": (stats.expon, 1),
}

def service_fit_details(svc: np.ndarray, B: int = 300, seed: int = 42) -> pd.DataFrame:
    """
    S10: AIC, BIC, log-likelihood, thong ke KS va p-value KS hieu chinh bang
    bootstrap tham so (kieu Lilliefors, uoc luong lai tham so moi mau, n_mau <= 1000).
    """
    rng = np.random.default_rng(seed)
    n = len(svc)
    n_sim = min(1000, n)
    rows = []
    for name, (dist, k) in _DISTS.items():
        par = dist.fit(svc, floc=0)
        ll = float(np.sum(dist.logpdf(svc, *par)))
        ks = float(stats.kstest(svc, dist.name, args=par).statistic)
        ks_sims = np.empty(B)
        for b in range(B):
            sim = dist.rvs(*par, size=n_sim, random_state=rng)
            par_b = dist.fit(sim, floc=0)
            ks_sims[b] = stats.kstest(sim, dist.name, args=par_b).statistic
        # KS cua mau goc tinh tren n diem, mau mo phong n_sim diem -> quy doi theo sqrt(n)
        ks_scaled = ks * np.sqrt(n / n_sim)
        p_boot = float(np.mean(ks_sims >= ks_scaled))
        shown = [p for i, p in enumerate(par) if i != len(par) - 2]  # bo loc=0
        rows.append({
            "phan_phoi": name,
            "tham_so": ", ".join(f"{p:.4f}" for p in shown),
            "log_likelihood": ll,
            "AIC": 2 * k - 2 * ll,
            "BIC": k * np.log(n) - 2 * ll,
            "KS_stat": ks,
            "KS_pvalue_boot": p_boot,
            "cs2_mo_hinh": float(dist(*par).var() / dist(*par).mean() ** 2)
        })
    rows.append({"phan_phoi": "Thuc nghiem (du lieu)", "tham_so": f"n={n}", "log_likelihood": np.nan,
                 "AIC": np.nan, "BIC": np.nan, "KS_stat": 0.0, "KS_pvalue_boot": np.nan,
                 "cs2_mo_hinh": float(np.var(svc, ddof=1) / np.mean(svc) ** 2)})
    return pd.DataFrame(rows)

def patience_km(df: pd.DataFrame, theta: float) -> pd.DataFrame:
    """
    S10: Ham song Kaplan-Meier cua kien nhan (khach bo ve = su kien,
    khach duoc phuc vu = kiem duyet phai tai thoi gian cho), so voi mu exp(-theta t).
    """
    w = df[df["wait"] > 0]
    times = w["wait"].values
    events = (w["served"] == 0).astype(int).values
    rows = []
    s_t = 1.0
    for t_i in np.sort(np.unique(times[events == 1])):
        d_i = int(np.sum((times == t_i) & (events == 1)))
        n_i = int(np.sum(times >= t_i))
        s_t *= (1.0 - d_i / n_i)
        rows.append({"time": t_i, "at_risk": n_i, "events": d_i,
                     "survival_km": s_t, "survival_expon": float(np.exp(-theta * t_i))})
    return pd.DataFrame(rows)

def cluster_bootstrap_params(df: pd.DataFrame, B: int = 1000, seed: int = 42) -> pd.DataFrame:
    """S10: CI95 cluster bootstrap theo ngay cho E[S] va theta."""
    rng = np.random.default_rng(seed)
    days = df["day"].unique()
    by_day = {d: g for d, g in df.groupby("day")}
    es, th = [], []
    for _ in range(B):
        sub = pd.concat([by_day[d] for d in rng.choice(days, size=len(days), replace=True)])
        es.append(sub.loc[sub["served"] == 1, "svc"].mean())
        tw = sub["wait"].sum()
        if tw > 0:
            th.append((sub["served"] == 0).sum() / tw)
    pat = fit_patience(df)
    rows = []
    for name, point, vals in [("E[S] (phut)", float(df.loc[df["served"] == 1, "svc"].mean()), es),
                              ("theta (phut^-1)", pat["theta"], th)]:
        lo, hi = np.percentile(vals, [2.5, 97.5])
        rows.append({"tham_so": name, "point_est": point, "cluster_boot_ci_low": lo,
                     "cluster_boot_ci_high": hi, "se_cluster": float(np.std(vals, ddof=1))})
    return pd.DataFrame(rows)

# =============================================================================
# M4: DIEU TRA KHUNG GIO NGOAI MAU VA UOC LUONG SO NHAN VIEN THUC TE
# =============================================================================

def estimate_concurrency(df: pd.DataFrame, grid_step: float = 0.5) -> pd.DataFrame:
    """
    Uoc luong so nhan vien phuc vu dong thoi theo ngay x gio tu timestamp:
    bat dau phuc vu = t + wait, ket thuc = bat dau + svc (chi khach duoc phuc vu).
    Tra ve so phien chong lan toi da (can duoi so nhan vien thuc te) va
    so phien trung binh (so quay ban trung binh) trong tung gio.
    """
    rows = []
    grid_h = np.arange(0.0, 60.0, grid_step)
    for d, g in df[df["served"] == 1].groupby("day"):
        s = (g["t"] + g["wait"]).to_numpy()[:, None]
        e = s + g["svc"].to_numpy()[:, None]
        for h in range(HOURS):
            grid = (h * 60.0 + grid_h)[None, :]
            busy = ((s <= grid) & (e > grid)).sum(axis=0)
            rows.append({"day": int(d), "hour": h, "max_dong_thoi": int(busy.max()),
                         "tb_dong_thoi": float(busy.mean())})
    return pd.DataFrame(rows)

def investigate_hour(df_train: pd.DataFrame, df_test: pd.DataFrame, hour: int) -> pd.DataFrame:
    """
    M4: So sanh lambda, E[S], cs^2, theta, ti le VIP, SL quan sat va so nhan vien
    uoc luong cua mot khung gio giua tap train (gop) va tung ngay test.
    """
    conc = estimate_concurrency(pd.concat([df_train, df_test]))
    conc_h = conc[conc["hour"] == hour].set_index("day")

    def describe(sub: pd.DataFrame, label: str, days: List[int]) -> Dict:
        n_days = len(days)
        svc = sub.loc[sub["served"] == 1, "svc"].dropna()
        tw = sub["wait"].sum()
        c_sub = conc_h.loc[conc_h.index.isin(days)]
        return {
            "nhom": label,
            "so_ngay": n_days,
            "so_khach": len(sub),
            "lambda_phut": len(sub) / (60.0 * n_days),
            "E_S": float(svc.mean()),
            "cs2": float(svc.var(ddof=1) / svc.mean() ** 2) if len(svc) > 1 else np.nan,
            "theta": float((sub["served"] == 0).sum() / tw) if tw > 0 else 0.0,
            "ti_le_vip": float(sub["vip"].mean()),
            "ti_le_bo_ve": float((sub["served"] == 0).mean()),
            "SL_quan_sat": float(((sub["served"] == 1) & (sub["wait"] <= WAIT_THRESHOLD)).mean()),
            "Wq_TB": float(sub["wait"].mean()),
            "tai_a": len(sub) / (60.0 * n_days) * float(svc.mean()),
            "NV_dong_thoi_max": float(c_sub["max_dong_thoi"].mean()),
            "NV_dong_thoi_TB": float(c_sub["tb_dong_thoi"].mean()),
        }

    tr_h = df_train[df_train["hour"] == hour]
    te_h = df_test[df_test["hour"] == hour]
    rows = [describe(tr_h, "Train (gop)", sorted(df_train["day"].unique())),
            describe(te_h, "Test (gop)", sorted(df_test["day"].unique()))]
    for d in sorted(df_test["day"].unique()):
        rows.append(describe(te_h[te_h["day"] == d], f"Test ngay {d}", [d]))
    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = load_log()
    df_train, df_test = split_train_test(df, train_ratio=0.7)
    print(f"Tong so mau: {len(df)} | Train ({df_train['day'].nunique()} ngay): {len(df_train)} | Test ({df_test['day'].nunique()} ngay): {len(df_test)}")
    params = estimate_all(df_train, plot=True)
