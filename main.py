"""
main.py: Chuong trinh chinh chay toan bo pipeline du an theo giai doan:
  data     - doc du lieu, tach train/test, uoc luong tham so (params.json),
             S1, T1, S10, M4 (dieu tra 15h-16h, uoc luong so nhan vien thuc te)
  theory   - lich SIPP Erlang C / Erlang-A
  verify   - kiem chung mo phong 3 tang + M/G/1 P-K + M/G/6
  optimize - toi uu lich, Pha 3, lich ben vung, xep ca, so sanh chinh sach, F1,
             kich ban M1 (kien nhan), M2 (rang buoc bo ve), M3 (phuc vu thuc nghiem vs Gamma)
  robust   - do nhay, S2-S9, S11, M5 (on dinh gio te nhat)
  report   - doi_chieu_v3_v4.csv, MO_TA.md
  all      - chay lan luot tat ca giai doan

Vi du:
  python main.py --stage all
  python main.py --stage optimize --reps-scale 0.1   # chay nhanh khi phat trien
Moi ket qua ghi vao results/<common.RESULTS_VERSION>/.
"""

import sys
import os
import json
import time
import argparse
import datetime
import pandas as pd

# Thiet lap ma hoa UTF-8 cho console tren Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import common
from common import H_LABELS, out_path, scaled
import a_data
import chay_kiem_chung
import d_experiments as dx
import e_robustness
import f_scenarios
import g_report

STAGES = ["data", "theory", "verify", "optimize", "robust", "report"]

def save(df: pd.DataFrame, name: str) -> None:
    df.to_csv(out_path(name), index=False, encoding="utf-8-sig")
    print(f"  -> {name}")

def stage_data(ctx):
    df_all, df_train, df_test, p = ctx["df_all"], ctx["df_train"], ctx["df_test"], ctx["params"]
    print(f"  • Tong so ban ghi: {len(df_all):,} | Train: {len(df_train):,} ({df_train['day'].nunique()} ngay)"
          f" | Test: {len(df_test):,} ({df_test['day'].nunique()} ngay)")
    print(f"  • E[S] = {p['service']['mean']:.4f} phut, cs² = {p['service']['cs2']:.4f} "
          f"(Gamma cs² = {p['service']['gamma_cs2']:.4f}); theta = {p['theta']:.4f} "
          f"(kien nhan TB {p['mean_patience']:.1f} phut); p_vip = {p['p_vip']:.4f}; CV ngay = {p['day_cv']:.4f}")
    save(a_data.lambda_ci_table(df_all), "khoang_tin_cay_lambda.csv")
    hourly, over = a_data.poisson_overdispersion(df_all)
    save(hourly, "kiem_dinh_poisson.csv")
    save(over, "qua_phan_tan_ngay.csv")
    save(a_data.service_fit_details(ctx["svc_train"], B=scaled(300, 20)), "kiem_dinh_phan_phoi_chi_tiet.csv")
    save(a_data.patience_km(df_train, p["theta"]), "patience_km.csv")
    save(a_data.cluster_bootstrap_params(df_train, B=scaled(1000, 50)), "cluster_bootstrap_params.csv")
    # M4: khung 15h-16h (gio 7) va so nhan vien thuc te uoc luong tu so phien chong lan
    save(a_data.investigate_hour(df_train, df_test, hour=7), "dieu_tra_15h_16h.csv")
    conc = a_data.estimate_concurrency(df_all)
    conc["tap"] = conc["day"].map(lambda d: "Train" if d in set(df_train["day"]) else "Test")
    save(conc, "nhan_vien_uoc_luong.csv")
    by_hour = conc.groupby(["hour", "tap"])[["max_dong_thoi", "tb_dong_thoi"]].mean().unstack("tap")
    by_hour.columns = [f"{a}_{b}" for a, b in by_hour.columns]
    by_hour.insert(0, "khung_gio", H_LABELS)
    save(by_hour.reset_index(), "nhan_vien_uoc_luong_theo_gio.csv")

def stage_theory(ctx):
    dx.run_theory(ctx)

def stage_verify(ctx):
    chay_kiem_chung.run_all_verification()

def stage_optimize(ctx):
    dx.run_optimize(ctx)
    f_scenarios.run_scenarios_optimize(ctx)

def stage_robust(ctx):
    e_robustness.run_robust(ctx)
    f_scenarios.run_scenarios_robust(ctx)

def stage_report(ctx):
    g_report.run_report(ctx)

STAGE_FUNCS = {
    "data": stage_data, "theory": stage_theory, "verify": stage_verify,
    "optimize": stage_optimize, "robust": stage_robust, "report": stage_report,
}

def log_stage(stage: str, minutes: float) -> None:
    """Ghi thoi gian chay tung giai doan vao thoi_gian_chay.json."""
    path = out_path(g_report.RUN_LOG)
    log = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            log = json.load(f)
    log.setdefault("stages", {})[stage] = {
        "phut": round(minutes, 2), "reps_scale": common.REPS_SCALE,
        "luc": datetime.datetime.now().isoformat(timespec="seconds")}
    log["reps_scale"] = common.REPS_SCALE
    log["tong_phut"] = round(sum(s["phut"] for s in log["stages"].values()), 2)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

def print_recommendation() -> None:
    """Bang quyet dinh: chi in so lieu doc tu CSV vua ghi."""
    path = os.path.join(common.RESULTS_DIR, "so_sanh_chinh_sach.csv")
    if not os.path.exists(path):
        return
    comp = pd.read_csv(path).set_index("chinh_sach")
    opt, rob = comp.loc["Toi uu mo phong"], comp.loc["Ben vung (+10% nhu cau)"]
    base_qh = common.BASELINE_C * common.HOURS
    print("\n" + "=" * 75)
    print("                    BANG QUYET DINH (doc tu so_sanh_chinh_sach.csv)")
    print("=" * 75)
    print(f"  • Lich toi uu:                 {opt['lich_quay']} ({opt['quay_gio']} quay-gio)")
    print(f"  • SL toan ngay:                {opt['sl_toan_ngay']:.4f} ± {opt['sl_ci_half']:.4f}")
    print(f"  • SL gio te nhat (can duoi):   {opt['sl_gio_te_nhat_low']:.4f} ({H_LABELS[int(opt['gio_te_nhat'])]})")
    print(f"  • Ti le bo ve:                 {opt['ti_le_bo_ve'] * 100:.2f}% ± {opt['ti_le_bo_ve_ci_half'] * 100:.2f}%")
    print(f"  • Wq TB:                       {opt['wq_phut']:.4f} phut | rho = {opt['hieu_suat_rho'] * 100:.2f}%")
    print(f"  • So voi moc {common.BASELINE_C} quay ({base_qh} q-h): "
          f"{(base_qh - opt['quay_gio']) / base_qh * 100:+.1f}% quay-gio tiet kiem")
    print(f"  • Lich ben vung (+10%):        {rob['lich_quay']} ({rob['quay_gio']} q-h, SL {rob['sl_toan_ngay']:.4f})")
    m1 = os.path.join(common.RESULTS_DIR, "do_nhay_kien_nhan.csv")
    if os.path.exists(m1):
        k = pd.read_csv(m1)
        print(f"  • Theo kien nhan (M1):         {int(k['quay_gio'].min())}–{int(k['quay_gio'].max())} q-h "
              f"(kien nhan {k['kien_nhan_TB_phut'].iloc[0]:.1f} phut -> vo cung)")

def main(argv=None):
    parser = argparse.ArgumentParser(description="Pipeline mo phong hang doi va xac dinh so quay toi uu")
    parser.add_argument("--stage", default="all", choices=["all"] + STAGES)
    parser.add_argument("--reps-scale", type=float, default=1.0,
                        help="He so nhan so lan lap/so kich ban (vd 0.1 de chay nhanh)")
    args = parser.parse_args(argv)
    common.set_reps_scale(args.reps_scale)

    stages = STAGES if args.stage == "all" else [args.stage]
    print("=" * 75)
    print(f"  PIPELINE {common.RESULTS_VERSION} | giai doan: {', '.join(stages)} | reps-scale = {common.REPS_SCALE}")
    print("=" * 75)
    ctx = dx.load_context(estimate="data" in stages)
    for st in stages:
        print(f"\n>>> GIAI DOAN: {st.upper()}")
        t0 = time.time()
        STAGE_FUNCS[st](ctx)
        log_stage(st, (time.time() - t0) / 60.0)
    if "report" in stages:
        g_report.write_mo_ta()  # cap nhat thoi gian chay cua giai doan report
    print_recommendation()

if __name__ == "__main__":
    main()
