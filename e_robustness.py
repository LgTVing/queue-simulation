"""
e_robustness.py: Phan tich do ben va kiem dinh thong ke (giai doan 'robust'),
hop nhat tu tools/run_s2_s3_s4.py, tools/run_s5_s6_s7_s8_s9_s11.py, d_experiments V3:
- sensitivity(): do nhay theo nhu cau, E[S], theta -> do_nhay.csv, fig_c_do_nhay.png
- conditional_expectation() (S2): chi so ky vong co dieu kien theo he so nhan ngay (S14: CI cluster bootstrap)
- cv_day_sensitivity(), posterior_predictive_check() (S3)
- volume_threshold() (S4): nguong luu luong ngay va chinh sach du bao som (S13: hoi quy fit tren train)
- nested_bootstrap() (S5): bootstrap tham so long nhau va phan ra phuong sai
- out_of_sample() (S6): khoang du bao 95% cho tap test va Holm-Bonferroni
- fourteen_days() (S7): doi chieu 14 ngay quan sat
- service_dist_sensitivity() (S9): do nhay phan phoi phuc vu (hieu so theo cap CRN)
- cost_analysis() (S11): chi phi quay-gio + mat khach voi CI hieu so theo cap
Moi ham la ham thuan: nhan model/policies/seed, tra DataFrame; run_robust() ghi CSV.
Lich chinh sach lay tu lich_khuyen_nghi.json, khong hard-code.
"""

import dataclasses
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import common
from common import (
    Model, HOURS, H_LABELS, TARGET_SLA, WAIT_THRESHOLD, scaled, out_path,
    exp_service, gamma_service, lognorm_service, empirical_service
)
import a_data
import c_sim as sim
import d_experiments as dx
from stats_utils import wilson_ci, t_ci, holm_bonferroni

def _gamma_mult(rng: np.random.Generator, cv: float, size=None):
    """He so nhan ngay m ~ Gamma(1/cv^2, cv^2) (E[m] = 1, CV = cv)."""
    return rng.gamma(1.0 / cv ** 2, cv ** 2, size=size)

def _day_sl(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """So khach den va so khach dat SLA theo tung gio cua 1 ngay mo phong."""
    hours = df["hour"].to_numpy(dtype=int)
    ok = ((df["served"] == 1) & (df["wait"] <= WAIT_THRESHOLD)).to_numpy()
    return (np.bincount(hours, minlength=HOURS)[:HOURS],
            np.bincount(hours, weights=ok, minlength=HOURS)[:HOURS])

# Ham hau xu ly chay trong tien trinh con cua sim.map_sim (phai o cap module de pickle duoc)

def _post_sl_all(df: pd.DataFrame, sched: List[int]) -> float:
    return sim.rep_stats(df, sched)["sl_all"]

def _post_hour_day(df: pd.DataFrame, sched: List[int]):
    stt = sim.rep_stats(df, sched)
    arr, ok = _day_sl(df)
    return [x["sl"] for x in stt["hourly"]], stt["sl_all"], arr, ok

# =============================================================================
# DO NHAY THEO NHU CAU, E[S], THETA
# =============================================================================

def sensitivity(model: Model, svc: np.ndarray, policies: Dict[str, List[int]],
                n_reps: int = 150, seed: int = 80000) -> pd.DataFrame:
    """Do nhay mot yeu to mot lan voi CRN (cung seed giua cac muc)."""
    R = scaled(n_reps)
    variants = []
    for f in [0.9, 1.0, 1.1, 1.2, 1.3]:
        variants.append(("Nhu cau", f, dx.scale_demand(model, f), list(policies)))
    for f in [1.0, 1.1, 1.2]:
        m_f = dataclasses.replace(model, service=empirical_service(svc * f), mean_svc=model.mean_svc * f)
        variants.append(("E[S]", f, m_f, list(policies)[:2]))
    for f in [0.5, 1.0, 1.5]:
        variants.append(("Theta", f, dataclasses.replace(model, theta=model.theta * f), list(policies)[:2]))
    rows = []
    for group, f, m, names in variants:
        for name in names:
            r = sim.run_reps(m, policies[name], n_reps=R, seed_base=seed)
            worst = min(r["hourly"], key=lambda x: x["sl_ci95_low"])
            rows.append({"nhom_yeu_to": group, "he_so": f, "chinh_sach": name,
                         "sl_toan_ngay": r["sl_mean"], "sl_gio_te_nhat_low": worst["sl_ci95_low"],
                         "ti_le_bo_ve": r["p_ab_mean"], "wq_phut": r["wq_mean"]})
    df = pd.DataFrame(rows)

    plt.figure(figsize=(9, 5))
    dem = df[df["nhom_yeu_to"] == "Nhu cau"]
    for name, color, marker in zip(policies, ["#1F4E78", "#2CA02C", "#595959"], ["o", "^", "s"]):
        sub = dem[dem["chinh_sach"] == name]
        plt.plot(sub["he_so"], sub["sl_gio_te_nhat_low"] * 100, label=f"{name} {policies[name]}",
                 color=color, marker=marker)
    plt.axhline(y=TARGET_SLA * 100, color="red", linestyle="--", lw=1.5, label="Mục tiêu SLA = 90%")
    plt.xlabel("Hệ số nhu cầu (1.0 = nhu cầu chuẩn)")
    plt.ylabel("Cận dưới CI95 của SL giờ tệ nhất (%)")
    plt.title("Độ bền của các chính sách khi nhu cầu tăng")
    plt.legend(loc="lower left", fontsize=8)
    plt.grid(True, linestyle="--")
    plt.savefig(out_path("fig_c_do_nhay.png", "hinh"), dpi=200, bbox_inches="tight")
    plt.close()
    return df

# =============================================================================
# S2 / S3: KY VONG CO DIEU KIEN THEO HE SO NHAN NGAY, PPC
# =============================================================================

B_S14 = 2000
SEED_S14 = 1500000  # rng rieng cho resample S14 (khong dung trong mo phong)


def cluster_bootstrap_ci(cluster_means: np.ndarray, B: int = B_S14, seed: int = SEED_S14) -> Tuple[float, float]:
    """S14: CI 95% phan vi cho trung binh qua cum (cac cum cung co so quan sat)."""
    rng = np.random.default_rng(seed)
    idx = rng.integers(len(cluster_means), size=(B, len(cluster_means)))
    boot = cluster_means[idx].mean(axis=1)
    return float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))


def conditional_expectation(model: Model, policies: Dict[str, List[int]], cv_day: float,
                            K: int = 200, R: int = 30, seed: int = 20000) -> pd.DataFrame:
    """
    S2: Voi K kich ban he so nhan ngay m, chay R lan lap de uoc luong E_h(m) = SL ky vong gio h.
    Bao cao P(E_ngay >= 90%), P(min_h E_h >= 90%), P(thuc te moi gio >= 90%) va
    P(gop 20 ngay moi gio >= 90%) kem Wilson CI.
    S14: Wilson coi K*R ngay-lan lap la doc lap nen qua hep cho "thuc te moi gio"; them CI cluster
    bootstrap (resample K kich ban, giu R lan lap ben trong, B_S14 lan, phan vi 2.5-97.5%).
    """
    K, R = scaled(K, 10), scaled(R, 3)
    rows = []
    for name, sched in policies.items():
        rng = np.random.default_rng(seed)
        e_day, e_min, n_below, actual_ok = [], [], [], []
        m_arr = np.zeros(HOURS)
        m_ok = np.zeros(HOURS)
        n_month = month_ok = 0
        day_counter = 0
        m_vals = [float(_gamma_mult(rng, cv_day)) for _ in range(K)]
        out = sim.map_sim([dict(model=model, schedule=sched, seed=seed + k * 1000 + r, day_multiplier=m_vals[k])
                           for k in range(K) for r in range(R)], _post_hour_day, (sched,))
        for k in range(K):
            hour_sl = np.zeros((R, HOURS))
            day_sl = np.zeros(R)
            for r in range(R):
                h_sl, sl_all, arr, ok = out[k * R + r]
                hour_sl[r] = h_sl
                day_sl[r] = sl_all
                actual_ok.append(bool(np.all(hour_sl[r] >= TARGET_SLA)))
                m_arr += arr
                m_ok += ok
                day_counter += 1
                if day_counter % 20 == 0:
                    n_month += 1
                    month_ok += int(np.all(m_ok / np.maximum(m_arr, 1) >= TARGET_SLA))
                    m_arr[:] = 0
                    m_ok[:] = 0
            e_h = hour_sl.mean(axis=0)
            e_day.append(day_sl.mean())
            e_min.append(e_h.min())
            n_below.append(int(np.sum(e_h < TARGET_SLA)))
        e_day, e_min = np.array(e_day), np.array(e_min)
        p_d = wilson_ci(int(np.sum(e_day >= TARGET_SLA)), K)
        p_m = wilson_ci(int(np.sum(e_min >= TARGET_SLA)), K)
        p_a = wilson_ci(int(np.sum(actual_ok)), len(actual_ok))
        p_a_boot = cluster_bootstrap_ci(np.asarray(actual_ok, dtype=float).reshape(K, R).mean(axis=1))
        p_mo = wilson_ci(month_ok, max(1, n_month))
        rows.append({
            "chinh_sach": name, "lich_quay": str(sched), "quay_gio": sum(sched), "cv_day": cv_day,
            "K_kich_ban": K, "R_lan_lap": R,
            "SL_ky_vong_ngay_TB": float(e_day.mean()), "SL_phan_vi_5pct": float(np.percentile(e_day, 5)),
            "P_SL_ky_vong_ngay_ge90": p_d[0], "P_SL_ky_vong_ngay_low95": p_d[1], "P_SL_ky_vong_ngay_high95": p_d[2],
            "P_min_h_Eh_ge90": p_m[0], "P_min_h_Eh_low95": p_m[1], "P_min_h_Eh_high95": p_m[2],
            "so_gio_Eh_duoi_90_TB": float(np.mean(n_below)),
            "P_thuc_te_moi_gio_ge90": p_a[0], "P_thuc_te_moi_gio_low95": p_a[1], "P_thuc_te_moi_gio_high95": p_a[2],
            "P_thuc_te_moi_gio_boot_low95": p_a_boot[0], "P_thuc_te_moi_gio_boot_high95": p_a_boot[1],
            "P_thang_20ngay_moi_gio_ge90": p_mo[0], "P_thang_20ngay_low95": p_mo[1], "P_thang_20ngay_high95": p_mo[2],
            "so_thang": n_month
        })
    return pd.DataFrame(rows)

def cv_day_sensitivity(model: Model, policies: Dict[str, List[int]],
                       cvs=(0.08, 0.12, 0.16, 0.20)) -> pd.DataFrame:
    """S3: Lap lai S2 voi CV ngay khac nhau (K=100, R=20)."""
    return pd.concat([conditional_expectation(model, policies, cv, K=100, R=20, seed=50000 + int(cv * 100))
                      for cv in cvs], ignore_index=True)

def posterior_predictive_check(df_all: pd.DataFrame, cv_day: float, B: int = 1000,
                               seed: int = 777) -> pd.DataFrame:
    """
    S3: So sanh chi so phan tan D_h quan sat (14 ngay) voi phan phoi D_h cua
    mo hinh Poisson x he so nhan ngay Gamma(CV = cv_day) qua B bo 14 ngay mo phong.
    """
    rng = np.random.default_rng(seed)
    cm = a_data.counts_matrix(df_all).values.astype(float)
    n_d = cm.shape[0]
    means = cm.mean(axis=0)

    def disp(mat):
        mu = np.maximum(mat.mean(axis=0), 1e-9)
        return ((mat - mu) ** 2).sum(axis=0) / mu

    d_obs = disp(cm)
    tot = cm.sum(axis=1)
    d_obs_tot = float(((tot - tot.mean()) ** 2).sum() / tot.mean())
    sim_h = np.zeros((scaled(B, 50), HOURS))
    sim_tot = np.zeros(len(sim_h))
    for b in range(len(sim_h)):
        m = _gamma_mult(rng, cv_day, size=n_d)
        mat = rng.poisson(m[:, None] * means[None, :]).astype(float)
        sim_h[b] = disp(mat)
        t_b = mat.sum(axis=1)
        sim_tot[b] = ((t_b - t_b.mean()) ** 2).sum() / t_b.mean()
    rows = []
    for label, obs, sims in [(H_LABELS[h], d_obs[h], sim_h[:, h]) for h in range(HOURS)] + \
                            [("Tong ca ngay", d_obs_tot, sim_tot)]:
        p_val = float(np.mean(sims >= obs))
        rows.append({"muc": label, "D_quan_sat": float(obs), "D_ky_vong_mo_hinh": float(sims.mean()),
                     "D_sim_ci_low": float(np.percentile(sims, 2.5)), "D_sim_ci_high": float(np.percentile(sims, 97.5)),
                     "posterior_predictive_pvalue": p_val,
                     "mo_hinh_giai_thich_tot": "Tot" if 0.05 <= p_val <= 0.95 else "Kem"})
    return pd.DataFrame(rows)

# =============================================================================
# S4: NGUONG LUU LUONG VA CHINH SACH DU BAO SOM
# =============================================================================

def early_forecast(cm: pd.DataFrame, train_days):
    """S13: V_ngay = a + b * N_8h-10h fit tren cac ngay train; tra (reg, x, V, mat na train, RMSE train, RMSE test)."""
    x_early = (cm[0] + cm[1]).to_numpy()
    v_total = cm.sum(axis=1).to_numpy()
    is_train = np.isin(np.asarray(cm.index), list(train_days))
    reg = st.linregress(x_early[is_train], v_total[is_train])
    resid = v_total - (reg.intercept + reg.slope * x_early)
    return (reg, x_early, v_total, is_train, float(np.sqrt(np.mean(resid[is_train] ** 2))),
            float(np.sqrt(np.mean(resid[~is_train] ** 2))))


def volume_threshold(model: Model, df_all: pd.DataFrame, policies: Dict[str, List[int]],
                     n_mean: float, train_days, R: int = 40) -> Tuple[pd.DataFrame, pd.DataFrame, Dict]:
    """
    S4: (1) SL toan ngay theo luu luong ngay V co dinh (m = V / n_mean) cho lich toi uu va ben vung;
    V* = luu luong lon nhat lich toi uu con dat SL >= 90% (noi suy tuyen tinh).
    (2) Hoi quy V_ngay theo so khach 8h-10h, fit chi tren 10 ngay train (S13), RMSE tach train/test;
    chinh sach ghep tren 14 ngay: dung lich ben vung khi V_du_bao > V*.
    """
    R = scaled(R)
    opt_name, rob_name = list(policies)[:2]
    volumes = np.array([550, 600, 650, 700, 725, 750, 775, 800, 850])
    rows = []
    for v in volumes:
        m_v = v / n_mean
        sl = {}
        for k, name in enumerate([opt_name, rob_name]):
            vals = sim.map_sim([dict(model=model, schedule=policies[name],
                                     seed=30000 + 10000 * k + int(v) * 10 + r, day_multiplier=m_v)
                                for r in range(R)], _post_sl_all, (policies[name],))
            sl[name] = float(np.mean(vals))
        rows.append({"luu_luong_ngay_V": int(v), "he_so_m": round(m_v, 3),
                     f"SL_{opt_name}": sl[opt_name], f"SL_{rob_name}": sl[rob_name],
                     f"{opt_name}_dat_ge90": "Dat" if sl[opt_name] >= TARGET_SLA else "Hut",
                     f"{rob_name}_dat_ge90": "Dat" if sl[rob_name] >= TARGET_SLA else "Hut"})
    df_v = pd.DataFrame(rows)
    sl_opt = df_v[f"SL_{opt_name}"].to_numpy()
    below = np.where(sl_opt < TARGET_SLA)[0]
    if len(below) == 0:
        v_star = float(volumes[-1])
    elif below[0] == 0:
        v_star = float(volumes[0])
    else:
        i = below[0]
        v_star = float(np.interp(TARGET_SLA, [sl_opt[i], sl_opt[i - 1]], [volumes[i], volumes[i - 1]]))

    cm = a_data.counts_matrix(df_all)
    reg, x_early, v_total, is_train, rmse_tr, rmse_te = early_forecast(cm, train_days)
    q_opt, q_rob = sum(policies[opt_name]), sum(policies[rob_name])
    comp = []
    for i, d in enumerate(cm.index):
        v_hat = reg.intercept + reg.slope * x_early[i]
        use_rob = v_hat > v_star
        comp.append({"ngay": int(d), "tap": "Train" if is_train[i] else "Test", "N_8h_10h": int(x_early[i]),
                     "V_thuc_te": int(v_total[i]), "V_du_bao": round(float(v_hat), 1),
                     "sai_so_du_bao": round(float(v_hat - v_total[i]), 1),
                     "chinh_sach_chon": rob_name if use_rob else opt_name,
                     "quay_gio_su_dung": q_rob if use_rob else q_opt,
                     "V_thuc_te_vuot_V_sao": "Y" if v_total[i] > v_star else "N"})
    miss = [c for c in comp if c["V_thuc_te_vuot_V_sao"] == "Y" and c["chinh_sach_chon"] == opt_name]
    info = {"V_sao": v_star, "intercept": reg.intercept, "slope": reg.slope, "r_train": reg.rvalue,
            "p_train": reg.pvalue, "n_train": int(is_train.sum()), "rmse_train": rmse_tr, "rmse_test": rmse_te,
            "qh_tb": float(np.mean([c["quay_gio_su_dung"] for c in comp])), "so_ngay_bo_lo": len(miss)}
    return df_v, pd.DataFrame(comp), info

# =============================================================================
# S5: BOOTSTRAP THAM SO LONG NHAU VA PHAN RA PHUONG SAI
# =============================================================================

def nested_bootstrap(model: Model, df_train: pd.DataFrame, sched: List[int],
                     B: int = 50, R: int = 60, seed: int = 88888) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    S5: B bo tham so, moi bo resample ngay train (cluster) de lay lambda_h, mau phuc vu
    thuc nghiem, theta, p_vip; chay R lan lap. Phan ra phuong sai SL toan ngay giua cac bo
    thanh phan bat dinh tham so va nhieu mo phong (Var_within / R).
    seed: rng resample ngay. Seed mo phong lay tu common.SEED_BANDS["nested_boot"], ["nested_nom"] (F9):
    moi bo co dai rieng nen nhieu mo phong doc lap giua cac bo, dung gia dinh cua phan ra phuong sai.
    """
    B, R = scaled(B, 10), scaled(R, 5)
    boot_base, r_max = common.SEED_BANDS["nested_boot"]
    if R > r_max or common.SEED_STEP * R > common.NESTED_BOOT_STEP:
        raise ValueError(f"nested_bootstrap: R = {R} vuot dai seed moi bo ({r_max})")
    rng = np.random.default_rng(seed)
    days = df_train["day"].unique()
    by_day = {d: g for d, g in df_train.groupby("day")}
    boot_rows = []
    for b in range(B):
        sub = pd.concat([by_day[d] for d in rng.choice(days, size=len(days), replace=True)])
        counts = sub.groupby("hour").size()
        rates_b = [float(counts.get(h, 0)) / (len(days) * 60.0) for h in range(HOURS)]
        svc_b = a_data.train_service_samples(sub)
        pat_b = a_data.fit_patience(sub)
        m_b = dataclasses.replace(model, rates=rates_b, service=empirical_service(svc_b),
                                  theta=pat_b["theta"], p_vip=float(sub["vip"].mean()),
                                  mean_svc=float(svc_b.mean()))
        res = sim.run_reps(m_b, sched, n_reps=R, seed_base=boot_base + common.NESTED_BOOT_STEP * b, keep_reps=True)
        boot_rows.append({"boot_id": b, "mean_sl_day": float(res["rep_sl_day"].mean()),
                          "worst_hour_sl": float(res["rep_sl_hourly"].mean(axis=0).min()),
                          "mean_svc": float(svc_b.mean()), "theta": pat_b["theta"],
                          "p_vip": float(sub["vip"].mean()), "lambda_tb": float(np.mean(rates_b))})
    df_boot = pd.DataFrame(boot_rows)

    nom = sim.run_reps(model, sched, n_reps=R, seed_base=common.SEED_BANDS["nested_nom"][0], keep_reps=True)
    nom_sl = nom["rep_sl_day"]
    var_total = float(np.var(df_boot["mean_sl_day"], ddof=1))
    var_noise = float(np.var(nom_sl, ddof=1)) / R
    var_param = max(0.0, var_total - var_noise)
    p_day = wilson_ci(int(np.sum(df_boot["mean_sl_day"] >= TARGET_SLA)), B)
    p_worst = wilson_ci(int(np.sum(df_boot["worst_hour_sl"] >= TARGET_SLA)), B)
    nan = np.nan
    decomp = pd.DataFrame([
        {"chi_so": f"SL toan ngay danh nghia (R={R})", "gia_tri": float(nom_sl.mean()),
         "ci_low": float(nom_sl.mean() - 1.96 * np.sqrt(var_noise)), "ci_high": float(nom_sl.mean() + 1.96 * np.sqrt(var_noise))},
        {"chi_so": f"SL gio te nhat danh nghia (R={R})", "gia_tri": float(nom["rep_sl_hourly"].mean(axis=0).min()), "ci_low": nan, "ci_high": nan},
        {"chi_so": "Phuong sai tong qua cac bo bootstrap", "gia_tri": var_total, "ci_low": nan, "ci_high": nan},
        {"chi_so": "Phuong sai do nhieu mo phong (Within / R)", "gia_tri": var_noise, "ci_low": nan, "ci_high": nan},
        {"chi_so": "Phuong sai do bat dinh tham so (Between)", "gia_tri": var_param, "ci_low": nan, "ci_high": nan},
        {"chi_so": "Ti le phuong sai do bat dinh tham so (%)", "gia_tri": var_param / var_total * 100 if var_total > 0 else nan, "ci_low": nan, "ci_high": nan},
        {"chi_so": "Ti le phuong sai do nhieu mo phong (%)", "gia_tri": var_noise / var_total * 100 if var_total > 0 else nan, "ci_low": nan, "ci_high": nan},
        {"chi_so": "Xac suat SL toan ngay >= 90%", "gia_tri": p_day[0], "ci_low": p_day[1], "ci_high": p_day[2]},
        {"chi_so": "Xac suat SL gio te nhat >= 90%", "gia_tri": p_worst[0], "ci_low": p_worst[1], "ci_high": p_worst[2]},
    ])
    return df_boot, decomp

# =============================================================================
# S6: KIEM TRA NGOAI MAU VOI KHOANG DU BAO
# =============================================================================

def simulated_p_value(sims: np.ndarray, obs: float) -> float:
    """S16: p-value hai phia cua quan sat obs so voi phan phoi mo phong sims (hieu chinh +1, chan tren 1)."""
    sims = np.asarray(sims, dtype=float)
    k = len(sims)
    upper = (np.count_nonzero(sims >= obs) + 1) / (k + 1)
    lower = (np.count_nonzero(sims <= obs) + 1) / (k + 1)
    return float(min(1.0, 2.0 * min(upper, lower)))


def out_of_sample(model: Model, df_test: pd.DataFrame, sched: List[int], cv_day: float,
                  K: int = 1000, seed: int = 54321) -> pd.DataFrame:
    """
    S6: Sinh K tap "n ngay test" tu mo hinh (co he so nhan ngay), lay PI95 cua SL theo gio;
    so voi SL quan sat tren tap test (Wilson CI). p-value hai phia lay tu chinh phan phoi mo phong
    (S16): p = min(1, 2 min((#sim >= obs + 1)/(K + 1), (#sim <= obs + 1)/(K + 1))), roi Holm-Bonferroni.
    Truoc S16 dung z-test SE nhi thuc (coi moi khach doc lap, bo qua tuong quan trong ngay va bien
    dong ngay) nen gio nam trong PI95 van bi gan "lech co y nghia"; giu o cot raw_p_value_nhi_thuc.
    Luu y: SL quan sat duoc tao boi nhan su thuc te (khong biet), khong phai lich mo phong.
    """
    K = scaled(K, 30)
    n_days = df_test["day"].nunique()
    rng = np.random.default_rng(seed)
    sim_sl = np.zeros((K, HOURS))
    # Rut he so nhan ngay truoc, dung thu tu (k, d) nhu khi chay tuan tu, roi moi chia job
    mults = [float(_gamma_mult(rng, cv_day)) for _ in range(K * n_days)]
    out = sim.map_sim([dict(model=model, schedule=sched, seed=seed + k * 10 + d, day_multiplier=mults[k * n_days + d])
                       for k in range(K) for d in range(n_days)], _day_sl)
    for k in range(K):
        arr = np.zeros(HOURS)
        ok = np.zeros(HOURS)
        for d in range(n_days):
            a, o = out[k * n_days + d]
            arr += a
            ok += o
        sim_sl[k] = ok / np.maximum(arr, 1)
    rows, p_raw = [], []
    for h in range(HOURS):
        sub = df_test[df_test["hour"] == h]
        n_h = len(sub)
        s5 = int(((sub["served"] == 1) & (sub["wait"] <= WAIT_THRESHOLD)).sum())
        p_obs, lo, hi, _ = wilson_ci(s5, n_h)
        mu_sim = float(sim_sl[:, h].mean())
        pi_lo, pi_hi = np.percentile(sim_sl[:, h], [2.5, 97.5])
        p_val = simulated_p_value(sim_sl[:, h], p_obs)
        se = np.sqrt(mu_sim * (1 - mu_sim) / n_h) if n_h > 0 else 1.0
        p_binom = float(2 * (1 - st.norm.cdf(abs((p_obs - mu_sim) / max(se, 1e-9)))))
        p_raw.append(p_val)
        rows.append({"khung_gio": H_LABELS[h], "so_quay": sched[h], "SL_mo_phong_TB": mu_sim,
                     "PI95_low": float(pi_lo), "PI95_high": float(pi_hi), "SL_thuc_te": p_obs,
                     "SL_thuc_te_Wilson_low": lo, "SL_thuc_te_Wilson_high": hi,
                     "trong_PI95": "Co" if pi_lo <= p_obs <= pi_hi else "Khong", "raw_p_value": p_val,
                     "raw_p_value_nhi_thuc": p_binom,
                     "Wq_thuc_te": float(sub["wait"].mean()), "Bo_ve_thuc_te": float((sub["served"] == 0).mean())})
    adj, rej = holm_bonferroni(p_raw)
    for h in range(HOURS):
        rows[h]["adj_p_value_Holm"] = float(adj[h])
        rows[h]["lech_co_y_nghia"] = "Co" if rej[h] else "Khong"
    return pd.DataFrame(rows)

# =============================================================================
# S7: DOI CHIEU 14 NGAY QUAN SAT
# =============================================================================

def fourteen_days(model: Model, df_all: pd.DataFrame, policies: Dict[str, List[int]],
                  n_mean: float, R: int = 40) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """S7: Moi ngay quan sat d, mo phong R lan voi m_d = N_d / n_mean cho tung chinh sach."""
    R = scaled(R)
    totals = df_all.groupby("day").size()
    train_days = set(a_data.split_train_test(df_all, train_ratio=0.7)[0]["day"])
    rows = []
    for d, n_d in totals.items():
        row = {"ngay": int(d), "phan_tap": "Train" if d in train_days else "Test", "tong_khach": int(n_d)}
        for k, (name, s) in enumerate(policies.items()):
            vals = sim.map_sim([dict(model=model, schedule=s, seed=10000 * (k + 1) + int(d) * 100 + r,
                                     day_multiplier=n_d / n_mean) for r in range(R)], _post_sl_all, (s,))
            m, lo, hi, _, _ = t_ci(vals)
            row.update({f"SL_{name}": m, f"CI95_low_{name}": lo, f"CI95_high_{name}": hi,
                        f"Dat_SLA_{name}": "Dat" if m >= TARGET_SLA else "Hut"})
        rows.append(row)
    df14 = pd.DataFrame(rows)
    summ = []
    for name in policies:
        n_ok = int((df14[f"Dat_SLA_{name}"] == "Dat").sum())
        p, lo, hi, _ = wilson_ci(n_ok, len(df14))
        summ.append({"chinh_sach": name, "so_ngay_dat": n_ok, "tong_so_ngay": len(df14),
                     "ti_le": p, "wilson_low": lo, "wilson_high": hi})
    return df14, pd.DataFrame(summ)

# =============================================================================
# S9: DO NHAY PHAN PHOI PHUC VU
# =============================================================================

def service_dist_sensitivity(model: Model, params: Dict, svc: np.ndarray, sched: List[int],
                             R: int = 150, seed: int = 45000) -> pd.DataFrame:
    """
    S9: So sanh mo hinh chinh (thuc nghiem) voi Gamma, Mu, Lognormal (cv+20%) bang
    hieu so theo cap tren cung seed (CRN). Mo hinh chinh la moc so sanh.
    """
    R = scaled(R)
    s = params["service"]
    samplers = {
        "Thuc nghiem (mo hinh chinh)": (empirical_service(svc), float(svc.mean())),
        "Gamma (AIC tot nhat)": (gamma_service(s["gamma_shape"], s["gamma_scale"]), s["gamma_shape"] * s["gamma_scale"]),
        "Exponential (M/M/c)": (exp_service(s["mean"]), s["mean"]),
        "Lognormal (cv+20%)": (lognorm_service(s["mean"], s["cv"] * 1.2), s["mean"]),
    }
    base = None
    rows = []
    for name, (sampler, mean_s) in samplers.items():
        m = dataclasses.replace(model, service=sampler, mean_svc=mean_s)
        res = sim.run_reps(m, sched, n_reps=R, seed_base=seed, keep_reps=True)
        day = res["rep_sl_day"]
        hour_mean = res["rep_sl_hourly"].mean(axis=0)
        w = int(np.argmin(hour_mean))
        m_w, lo_w, _, _, _ = t_ci(res["rep_sl_hourly"][:, w])
        if base is None:
            base = day
            d_m, d_lo, d_hi, sig = 0.0, 0.0, 0.0, "-"
        else:
            d_m, d_lo, d_hi, _, _ = t_ci(day - base)
            sig = "Co" if (d_lo > 0 or d_hi < 0) else "Khong"
        rows.append({"phan_phoi": name, "SL_toan_ngay": res["sl_mean"], "SL_ci_half": res["sl_ci_half"],
                     "gio_te_nhat": H_LABELS[w], "SL_gio_te_nhat": m_w, "SL_gio_te_nhat_low95": lo_w,
                     "ti_le_bo_ve": res["p_ab_mean"], "hieu_so_vs_thuc_nghiem": d_m,
                     "CI95_hieu_so_low": d_lo, "CI95_hieu_so_high": d_hi, "khac_biet_co_y_nghia": sig})
    return pd.DataFrame(rows)

# =============================================================================
# S11: CHI PHI VOI TRUYEN SAI SO VA HIEU SO THEO CAP
# =============================================================================

def cost_analysis(model: Model, policies: Dict[str, List[int]], n_mean: float,
                  R: int = 150, seed: int = 70000, k_list=(0.10, 0.25, 0.50, 1.00, 2.00)) -> pd.DataFrame:
    """
    S11: Chi phi/ngay = quay-gio + k * so khach bo ve (k = c_bo_ve / c_quay_gio).
    p_ab tung lan lap tren cung seed -> CI hieu so theo cap giua cac chinh sach.
    """
    R = scaled(R)
    pab = {name: sim.run_reps(model, s, n_reps=R, seed_base=seed, keep_reps=True)["rep_p_ab"]
           for name, s in policies.items()}
    names = list(policies)
    rows = []
    for k in k_list:
        costs = {name: sum(policies[name]) + k * n_mean * pab[name] for name in names}
        row = {"k_he_so_mat_khach": k}
        for name in names:
            m, _, _, hw, _ = t_ci(costs[name])
            row[f"Chi_phi_{name}"] = m
            row[f"CI95_half_{name}"] = hw
        d_m, d_lo, d_hi, _, _ = t_ci(costs[names[0]] - costs[names[1]])
        row.update({f"Hieu_so_{names[0]}_tru_{names[1]}": d_m, "CI95_hieu_so_low": d_lo, "CI95_hieu_so_high": d_hi,
                    "Khac_biet_co_y_nghia": "Co" if (d_lo > 0 or d_hi < 0) else "Khong"})
        best = min(names, key=lambda n: costs[n].mean())
        ties = [n for n in names if n != best and t_ci(costs[n] - costs[best])[1] <= 0]
        row["Chinh_sach_kinh_te_nhat"] = best + (f" (khong phan biet duoc voi {', '.join(ties)})" if ties else "")
        rows.append(row)
    return pd.DataFrame(rows)

# =============================================================================
# CHAY TOAN BO GIAI DOAN ROBUST
# =============================================================================

def run_robust(ctx: Dict) -> Dict:
    model, params = ctx["model"], ctx["params"]
    sch = dx.load_schedules()
    pol = dx.main_policies(sch)
    opt = sch["toi_uu"]
    cv_d = params["day_cv"]
    n_mean = ctx["n_day_mean"]

    def save(df: pd.DataFrame, name: str):
        df.to_csv(out_path(name), index=False, encoding="utf-8-sig")
        print(f"  -> {name}")

    print("[R.1] Do nhay nhu cau / E[S] / theta...")
    save(sensitivity(model, ctx["svc_train"], pol), "do_nhay.csv")
    print("[R.2] S2 ky vong co dieu kien...")
    save(conditional_expectation(model, pol, cv_d), "chi_so_ky_vong_dieu_kien.csv")
    print("[R.3] S3 do nhay CV ngay va PPC...")
    save(cv_day_sensitivity(model, pol), "do_nhay_cv_ngay.csv")
    save(posterior_predictive_check(ctx["df_all"], cv_d), "posterior_predictive_check.csv")
    print("[R.4] S4 nguong luu luong va du bao som...")
    df_v, df_comp, info = volume_threshold(model, ctx["df_all"], pol, n_mean, set(ctx["df_train"]["day"]))
    save(df_v, "nguong_luu_luong_chi_tiet.csv")
    save(df_comp, "danh_gia_chinh_sach_du_bao_14ngay.csv")
    save(pd.DataFrame([info]), "du_bao_som_hoi_quy.csv")
    print("[R.5] S5 bootstrap long nhau...")
    df_boot, decomp = nested_bootstrap(model, ctx["df_train"], opt)
    save(df_boot, "bat_dinh_nested.csv")
    save(decomp, "phan_ra_phuong_sai.csv")
    print("[R.6] S6 ngoai mau...")
    save(out_of_sample(model, ctx["df_test"], opt, cv_d), "ngoai_mau.csv")
    print("[R.7] S7 doi chieu 14 ngay...")
    df14, summ14 = fourteen_days(model, ctx["df_all"], pol, n_mean)
    save(df14, "theo_14_ngay.csv")
    save(summ14, "theo_14_ngay_tong_hop.csv")
    print("[R.8] S9 do nhay phan phoi phuc vu...")
    save(service_dist_sensitivity(model, params, ctx["svc_train"], opt), "do_nhay_phan_phoi.csv")
    print("[R.9] S11 chi phi...")
    save(cost_analysis(model, pol, n_mean), "chi_phi.csv")
    return info
