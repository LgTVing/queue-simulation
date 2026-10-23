"""
Tao tep results/final_v2/theo_ngay.csv tong hop ca 3 chinh sach qua 14 ngay quan sat.
"""
import sys, os
if sys.platform.startswith("win"):
    try: sys.stdout.reconfigure(encoding="utf-8")
    except: pass

import numpy as np
import pandas as pd
import a_data
import c_sim as sim
from common import Model, gamma_service, HOURS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df_all = a_data.load_log()
counts_matrix = df_all.groupby(["day", "hour"]).size().unstack(fill_value=0)
days = sorted(df_all["day"].unique())

import json
with open(os.path.join(BASE_DIR, "docs", "params.json"), "r", encoding="utf-8") as f:
    params = json.load(f)

svc_info = params["service"]
sched_opt = [4, 5, 6, 5, 5, 5, 5, 5, 4]      # 44
sched_rob = [5, 6, 6, 6, 5, 5, 5, 5, 5]      # 48
sched_c6  = [6] * HOURS                       # 54

policies = {
    "opt44": sched_opt,
    "rob48": sched_rob,
    "const6": sched_c6
}

rows = []
for day in days:
    counts = counts_matrix.loc[day].values
    total_cust = int(counts.sum())
    rates_day = [float(c) / 60.0 for c in counts]
    
    m_day = Model(
        rates=rates_day,
        service=gamma_service(svc_info["gamma_shape"], svc_info["gamma_scale"]),
        theta=params["theta"],
        p_vip=params["p_vip"],
        hour_len=60.0,
        mean_svc=svc_info["mean"]
    )
    
    day_row = {
        "ngay": day,
        "tong_khach": total_cust,
    }
    
    for pol_key, sched in policies.items():
        res = sim.run_reps(m_day, sched, n_reps=40, seed_base=30000 + day * 100)
        worst_h = min(res["hourly"], key=lambda x: x["sl_ci95_low"])
        all_ok = all(h_info["sl_ci95_low"] >= 0.90 for h_info in res["hourly"])
        
        day_row[f"sl_{pol_key}"] = round(res["sl_mean"], 4)
        day_row[f"sl_worst_{pol_key}"] = round(worst_h["sl_ci95_low"], 4)
        day_row[f"dat_sl_{pol_key}"] = "Y" if res["sl_mean"] >= 0.90 else "N"
        day_row[f"dat_moigio_{pol_key}"] = "Y" if all_ok else "N"
        day_row[f"pab_{pol_key}"] = round(res["p_ab_mean"], 4)
        
    rows.append(day_row)

df_out = pd.DataFrame(rows)
out_path = os.path.join(BASE_DIR, "results", "final_v2", "theo_ngay.csv")
df_out.to_csv(out_path, index=False, encoding="utf-8-sig")
print("Da xuat thanh cong:", out_path)
print(df_out[["ngay", "tong_khach", "sl_opt44", "dat_sl_opt44", "sl_rob48", "dat_sl_rob48", "sl_const6", "dat_sl_const6"]].to_string(index=False))

# Tong ket
n_opt_day = (df_out["dat_sl_opt44"] == "Y").sum()
n_opt_all = (df_out["dat_moigio_opt44"] == "Y").sum()
n_rob_day = (df_out["dat_sl_rob48"] == "Y").sum()
n_rob_all = (df_out["dat_moigio_rob48"] == "Y").sum()
n_c6_day = (df_out["dat_sl_const6"] == "Y").sum()
n_c6_all = (df_out["dat_moigio_const6"] == "Y").sum()

print("\nTONG KET 14 NGAY:")
print(f"Lich 44: {n_opt_day}/14 ngay dat SL toan ngay, {n_opt_all}/14 ngay dat moi gio")
print(f"Lich 48: {n_rob_day}/14 ngay dat SL toan ngay, {n_rob_all}/14 ngay dat moi gio")
print(f"Lich 54: {n_c6_day}/14 ngay dat SL toan ngay, {n_c6_all}/14 ngay dat moi gio")
