"""
g_report.py: Giai doan 'report':
1. doi_chieu_v3_v4.csv: moi chi so chinh gia tri V3 (doc tu results/final_v3 va
   results/archive/final_v1, final_v2), gia tri V4, chenh lech va nguyen nhan
2. MO_TA.md: mo ta tu dong thu muc ket qua (duong dan tuong doi), moi truong,
   he so so lan lap va thoi gian chay tung giai doan
"""

import os
import re
import sys
import json
import datetime
from typing import Dict, Optional
import numpy as np
import pandas as pd

import common
from common import TARGET_SLA
import b_theory as th
import d_experiments as dx

# Nguon so lieu V3 de doi chieu (chi doc, khong ghi)
ARCHIVE_DIR = os.path.join(common.BASE_DIR, "results", "archive")
PREV_RESULTS_DIR = os.path.join(common.BASE_DIR, "results", "final_v3")
RUN_LOG = "thoi_gian_chay.json"

# Mo ta tep ket qua: ten -> (giai doan / nhiem vu, noi dung)
FILE_DESC = {
    "params.json": ("data", "Tham so uoc luong tren 10 ngay train; phuc vu chinh: thuc nghiem (M3)"),
    "khoang_tin_cay_lambda.csv": ("data / S1", "CI95 lambda_h theo Poisson va Student-t qua 14 ngay"),
    "kiem_dinh_poisson.csv": ("data / T1", "Kiem dinh phan tan chi^2 theo gio, nhan chuan"),
    "qua_phan_tan_ngay.csv": ("data / T1", "Qua phan tan tong khach theo ngay, CV ngay sau hieu chinh Poisson"),
    "kiem_dinh_phan_phoi_chi_tiet.csv": ("data / S10", "AIC, BIC, KS bootstrap (da quy doi co mau) cho 4 phan phoi phuc vu"),
    "patience_km.csv": ("data / S10", "Kaplan-Meier cua kien nhan so voi mu"),
    "cluster_bootstrap_params.csv": ("data / S10", "CI95 cluster bootstrap theo ngay cho E[S], theta"),
    "dieu_tra_15h_16h.csv": ("data / M4", "So sanh tham so khung 15h-16h giua train va tung ngay test"),
    "nhan_vien_uoc_luong.csv": ("data / M4", "So phien phuc vu chong lan (toi da, trung binh) theo ngay x gio"),
    "nhan_vien_uoc_luong_theo_gio.csv": ("data / M4", "So nhan vien uoc luong theo gio (train vs test)"),
    "bang_sipp.csv": ("theory", "Lich SIPP Erlang C va Erlang-A theo gio"),
    "lich_khuyen_nghi.json": ("theory / optimize", "Cac lich da tinh (SIPP, toi uu, ben vung, theo ca, Gamma)"),
    "kiem_chung.csv": ("verify / S8", "Kiem chung 3 tang + M/G/1 P-K 40.000 phut + M/G/6, CI95 Student-t"),
    "kiem_chung_pooling.csv": ("verify", "Hang chung vs hang rieng (ly thuyet va SimPy)"),
    "lich_toi_uu.csv": ("optimize", "Lich su toi uu 2 pha"),
    "pha3.csv": ("optimize / C6", "Pha 3 bang mo phong: swap 1 quay va giam 2 quay"),
    "lich_ben_vung_delta.csv": ("optimize", "Lich toi uu theo muc du phong nhu cau +5/10/20%"),
    "lich_theo_ca.csv": ("optimize", "Xep ca MILP (mo hinh A/B, ca 4h, hon hop)"),
    "so_sanh_chinh_sach.csv": ("optimize", "So sanh 6 chinh sach, 300 lan lap, seed danh gia rieng"),
    "so_sanh_chinh_sach_bd.csv": ("optimize", "So sanh chinh sach co he so nhan ngay"),
    "doi_chieu_xa_hang.csv": ("optimize / F1", "SL gio cuoi khi xa hang giu so quay gio cuoi vs mo het c_max"),
    "do_nhay_kien_nhan.csv": ("optimize / M1", "Lich va chi so theo kien nhan trung binh 9,2 -> vo cung"),
    "toi_uu_rang_buoc_bo_ve.csv": ("optimize / M2", "Toi uu voi rang buoc ti le bo ve, SL o nguong 2/3/5 phut"),
    "toi_uu_theo_ca.csv": ("optimize / M6", "Moi lich phu theo ca da thu (gio cong, phuong an ca, SL, can duoi gio te nhat)"),
    "toi_uu_xac_suat_ngay.csv": ("optimize / M7", "Lich nho nhat theo muc P(SL ngay >= 90%) co bien dong ngay, quay-gio va theo ca, 14 ngay thuc te"),
    "chinh_sach_tang_quay.csv": ("robust / M8", "Lich 45 + mo them quay khi hang cho dai so voi Lich 45/48 co dinh, 4 kich ban + 14 ngay"),
    "toi_uu_theo_ca_top.csv": ("optimize / M6", "Top-5 lich kha thi o gio cong nho nhat: seed danh gia, bien dong ngay, nhu cau +10%"),
    "m3_dich_vu_thuc_nghiem.csv": ("optimize / M3", "Lich toi uu va danh gia duoi phuc vu thuc nghiem vs Gamma"),
    "do_nhay.csv": ("robust", "Do nhay nhu cau, E[S], theta (CRN)"),
    "chi_so_ky_vong_dieu_kien.csv": ("robust / S2", "Chi so ky vong co dieu kien theo he so nhan ngay"),
    "do_nhay_cv_ngay.csv": ("robust / S3", "S2 voi CV ngay 8-20%"),
    "posterior_predictive_check.csv": ("robust / S3", "Posterior predictive check chi so phan tan"),
    "nguong_luu_luong_chi_tiet.csv": ("robust / S4", "SL theo luu luong ngay co dinh"),
    "danh_gia_chinh_sach_du_bao_14ngay.csv": ("robust / S4", "Chinh sach ghep theo du bao 8h-10h tren 14 ngay"),
    "du_bao_som_hoi_quy.csv": ("robust / S4", "Hoi quy du bao som va nguong V*"),
    "bat_dinh_nested.csv": ("robust / S5", "Ket qua tung bo tham so bootstrap long nhau"),
    "phan_ra_phuong_sai.csv": ("robust / S5", "Phan ra phuong sai tham so vs nhieu mo phong"),
    "ngoai_mau.csv": ("robust / S6", "Ngoai mau: PI95 vs SL quan sat, Holm-Bonferroni"),
    "theo_14_ngay.csv": ("robust / S7", "Doi chieu 14 ngay quan sat"),
    "theo_14_ngay_tong_hop.csv": ("robust / S7", "So ngay dat SLA va Wilson CI"),
    "do_nhay_phan_phoi.csv": ("robust / S9", "Do nhay phan phoi phuc vu, hieu so theo cap voi mo hinh chinh"),
    "chi_phi.csv": ("robust / S11", "Chi phi quay-gio + mat khach, CI hieu so theo cap"),
    "so_lan_lap_can_thiet.csv": ("robust / M5", "So lan lap de CI SL moi gio <= 0,3 diem %"),
    "gio_te_nhat.csv": ("robust / M5", "Xac suat moi gio la gio te nhat"),
    "doi_chieu_v3_v4.csv": ("report", "Doi chieu chi so chinh V3 vs V4 kem nguyen nhan"),
    "pytest_log.txt": ("test", "Log pytest"),
    RUN_LOG: ("report", "Thoi gian chay va he so so lan lap tung giai doan"),
}

# =============================================================================
# DOC SO LIEU V3
# =============================================================================

def _num(s) -> float:
    """'0.9381 ± 0.0023' -> 0.9381; '5.35% ± 0.17%' -> 0.0535; '85.0%' -> 0.85."""
    if isinstance(s, (int, float, np.number)):
        return float(s)
    m = re.match(r"\s*([-+]?\d+(?:\.\d+)?)\s*(%?)", str(s))
    if not m:
        return np.nan
    v = float(m.group(1))
    return v / 100.0 if m.group(2) == "%" else v

def _read(path: str) -> Optional[pd.DataFrame]:
    return pd.read_csv(path) if os.path.exists(path) else None

def v3_reference() -> Dict[str, float]:
    """So lieu V3 da dong bang (bang so sanh chinh sach V1-V3, bien dong ngay V2, 14 ngay V3)."""
    ref = {}
    v1 = os.path.join(ARCHIVE_DIR, "final_v1")
    v2 = os.path.join(ARCHIVE_DIR, "final_v2")
    comp = _read(os.path.join(v1, "so_sanh_chinh_sach.csv"))
    if comp is not None:
        opt = comp[comp["chinh_sach"].str.contains("Sim-Optimized")].iloc[0]
        rob = comp[comp["chinh_sach"].str.contains("Bền vững")].iloc[0]
        ref.update({
            "lich_toi_uu": opt["lich_quay"], "qh_toi_uu": float(opt["quay_gio"]),
            "sl_toi_uu": _num(opt["sl_toan_ngay"]), "sl_te_nhat_low": _num(opt["sl_gio_te_nhat_low"]),
            "gio_te_nhat": re.search(r"H(\d)", opt["sl_gio_te_nhat_low"]).group(1),
            "p_ab": _num(opt["ti_le_bo_ve"]), "wq": _num(opt["wq_phut"]), "rho": _num(opt["hieu_suat_rho"]),
            "qh_ben_vung": float(rob["quay_gio"]), "sl_ben_vung": _num(rob["sl_toan_ngay"]),
        })
    bd = _read(os.path.join(v2, "so_sanh_chinh_sach_v2.csv"))
    if bd is not None:
        r = bd[bd["chinh_sach"].str.contains("44")].iloc[0]
        ref.update({"p_ngay_ge90": _num(r["P_ngay_ge90"]), "p_moi_gio_ge90": _num(r["P_moigio_ge90"])})
    d14 = _read(os.path.join(PREV_RESULTS_DIR, "theo_14_ngay_v3.csv"))
    if d14 is not None:
        ref["so_ngay_dat"] = float((d14["Dat_SLA_44"] == "Dat").sum())
    p3 = os.path.join(PREV_RESULTS_DIR, "params.json")
    if os.path.exists(p3):
        with open(p3, encoding="utf-8") as f:
            p = json.load(f)
        mu = 1.0 / p["service"]["mean"]
        ref["qh_erlang_c"] = float(sum(th.sipp_schedule(p["rates_per_min"], mu, 0.0, use_erlang_a=False)))
        ref["qh_erlang_a"] = float(sum(th.sipp_schedule(p["rates_per_min"], mu, p["theta"])))
    return ref

# =============================================================================
# BANG DOI CHIEU V3 / V4
# =============================================================================

def build_doi_chieu() -> pd.DataFrame:
    v3 = v3_reference()
    R = common.RESULTS_DIR
    sch = dx.load_schedules(required=False)
    comp = _read(os.path.join(R, "so_sanh_chinh_sach.csv"))
    bd = _read(os.path.join(R, "so_sanh_chinh_sach_bd.csv"))
    d14 = _read(os.path.join(R, "theo_14_ngay_tong_hop.csv"))
    drain = _read(os.path.join(R, "doi_chieu_xa_hang.csv"))
    m3 = _read(os.path.join(R, "m3_dich_vu_thuc_nghiem.csv"))

    def row_of(df, col, key):
        if df is None:
            return None
        sub = df[df[col] == key]
        return None if sub.empty else sub.iloc[0]

    opt = row_of(comp, "chinh_sach", "Toi uu mo phong")
    rob = row_of(comp, "chinh_sach", "Ben vung (+10% nhu cau)")
    opt_bd = row_of(bd, "chinh_sach", "Toi uu")
    d14_opt = row_of(d14, "chinh_sach", "Toi uu")
    keep = row_of(drain, "drain_policy", "keep_last")
    allo = row_of(drain, "drain_policy", "all_open")
    get = lambda r, c: (float(r[c]) if r is not None else np.nan)

    cause_all = "F1+F2 (dong co mo phong), M3 (phuc vu thuc nghiem cs2 cao hon Gamma), seed/R moi"
    rows = [
        ("Lich toi uu", v3.get("lich_toi_uu"), str(sch.get("toi_uu")), cause_all),
        ("Tong quay-gio lich toi uu", v3.get("qh_toi_uu"), float(sum(sch["toi_uu"])) if "toi_uu" in sch else np.nan, cause_all),
        ("Tong quay-gio SIPP Erlang C", v3.get("qh_erlang_c"), float(sum(sch["sipp_erlang_c"])) if "sipp_erlang_c" in sch else np.nan,
         "Tham so v4 (E[S] lay tu mau thuc nghiem); khong doi neu tham so giong V3"),
        ("Tong quay-gio SIPP Erlang-A", v3.get("qh_erlang_a"), float(sum(sch["sipp_erlang_a"])) if "sipp_erlang_a" in sch else np.nan,
         "Tham so v4"),
        ("SL toan ngay lich toi uu", v3.get("sl_toi_uu"), get(opt, "sl_toan_ngay"), cause_all),
        ("SL gio te nhat (can duoi CI95) lich toi uu", v3.get("sl_te_nhat_low"), get(opt, "sl_gio_te_nhat_low"),
         "F1 (gio 16h-17h het duoc xa hang bang c_max quay), F2, M3, M5 (R lon hon)"),
        ("Gio te nhat (chi so 0-8)", float(v3["gio_te_nhat"]) if "gio_te_nhat" in v3 else np.nan, get(opt, "gio_te_nhat"),
         "Gio te nhat khong on dinh giua cac lan chay; xem gio_te_nhat.csv (M5)"),
        ("Ti le bo ve lich toi uu", v3.get("p_ab"), get(opt, "ti_le_bo_ve"), cause_all),
        ("Wq TB lich toi uu (phut)", v3.get("wq"), get(opt, "wq_phut"), cause_all),
        ("Hieu suat rho lich toi uu", v3.get("rho"), get(opt, "hieu_suat_rho"),
         "rho toan ngay khong doi dinh nghia (F3 chi doi rho theo gio); doi theo lich va M3"),
        ("Tong quay-gio lich ben vung (+10%)", v3.get("qh_ben_vung"), get(rob, "quay_gio"), cause_all),
        ("SL toan ngay lich ben vung", v3.get("sl_ben_vung"), get(rob, "sl_toan_ngay"), cause_all),
        ("P(SL ngay >= 90%) co bien dong ngay, lich toi uu", v3.get("p_ngay_ge90"), get(opt_bd, "P_SL_ngay_ge90"),
         cause_all + "; CV ngay uoc luong tren train"),
        ("P(moi gio >= 90%) co bien dong ngay, lich toi uu", v3.get("p_moi_gio_ge90"), get(opt_bd, "P_moi_gio_ge90"), cause_all),
        ("So ngay quan sat dat SLA (/14), lich toi uu", v3.get("so_ngay_dat"), get(d14_opt, "so_ngay_dat"), cause_all),
        ("SL gio cuoi lich toi uu: mo het c_max (hanh vi V3) -> giu so quay gio cuoi (V4)",
         get(allo, "sl_gio_cuoi"), get(keep, "sl_gio_cuoi"), "F1 rieng le (cung lich, cung seed)"),
    ]
    if m3 is not None:
        same = m3[(m3["chinh_sach"] == "Lich toi uu (phuc vu thuc nghiem)")].set_index("mo_hinh_danh_gia")
        if {"Gamma", "Thuc nghiem"} <= set(same.index):
            rows.append(("SL toan ngay cung lich: phuc vu Gamma -> thuc nghiem",
                         float(same.loc["Gamma", "sl_toan_ngay"]), float(same.loc["Thuc nghiem", "sl_toan_ngay"]),
                         "M3 rieng le (cung lich, cung seed)"))

    out = []
    for name, a, b, cause in rows:
        try:
            diff = float(b) - float(a)
        except (TypeError, ValueError):
            diff = "khac" if str(a) != str(b) else "giong"
        out.append({"chi_so": name, "gia_tri_V3": a, "gia_tri_V4": b, "chenh_lech": diff, "nguyen_nhan": cause})
    return pd.DataFrame(out)

# =============================================================================
# MO_TA.MD
# =============================================================================

def write_mo_ta() -> str:
    import numpy, scipy, simpy, pandas, matplotlib
    R = common.RESULTS_DIR
    log = {}
    if os.path.exists(os.path.join(R, RUN_LOG)):
        with open(os.path.join(R, RUN_LOG), encoding="utf-8") as f:
            log = json.load(f)
    sch = dx.load_schedules(required=False)
    lines = [
        f"# Mô tả kết quả `{common.RESULTS_VERSION}` (sinh tự động bởi `g_report.py`)",
        "",
        f"- **Ngày sinh:** {datetime.date.today().isoformat()}",
        f"- **Môi trường:** Python {sys.version.split()[0]}, SimPy {simpy.__version__}, NumPy {numpy.__version__}, "
        f"SciPy {scipy.__version__}, pandas {pandas.__version__}, Matplotlib {matplotlib.__version__}",
        f"- **Lệnh tái lập:** `python main.py --stage all --reps-scale {log.get('reps_scale', common.REPS_SCALE)}`",
        f"- **Seed:** chọn lịch `seed_base={dx.SEED_SELECT}`, đánh giá cuối `seed_base={dx.SEED_EVAL}` (tách biệt để tránh selection bias)",
        "- **Mô hình chính:** NHPP theo giờ (F2), phục vụ thực nghiệm lấy mẫu từ train (M3), bỏ về mũ θ, "
        "VIP ưu tiên không ngắt, xả hàng giữ số quầy giờ cuối (F1)",
    ]
    if sch:
        lines.append(f"- **Lịch tối ưu:** `{sch.get('toi_uu')}` ({sum(sch.get('toi_uu', []))} quầy-giờ); "
                     f"bền vững +10%: `{sch.get('ben_vung')}`")
    if log.get("stages"):
        lines += ["", "## Thời gian chạy", "", "| Giai đoạn | Hệ số lần lặp | Thời gian (phút) | Lúc chạy |", "|---|:---:|:---:|---|"]
        for st, info in log["stages"].items():
            lines.append(f"| {st} | {info['reps_scale']} | {info['phut']:.1f} | {info['luc']} |")
    lines += ["", "## Danh mục tệp", "", "| Tệp | Giai đoạn / nhiệm vụ | Nội dung |", "|---|---|---|"]
    for name in sorted(os.listdir(R)):
        if os.path.isdir(os.path.join(R, name)) or name == "MO_TA.md":
            continue
        stage, desc = FILE_DESC.get(name, ("-", ""))
        lines.append(f"| [`{name}`]({name}) | {stage} | {desc} |")
    hinh = os.path.join(R, "hinh")
    if os.path.isdir(hinh):
        lines += ["", "## Hình", ""]
        lines += [f"- [`hinh/{n}`](hinh/{n})" for n in sorted(os.listdir(hinh))]
    path = os.path.join(R, "MO_TA.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path

def run_report(ctx: Dict = None) -> None:
    df = build_doi_chieu()
    df.to_csv(common.out_path("doi_chieu_v3_v4.csv"), index=False, encoding="utf-8-sig")
    print(df.to_string(index=False))
    print(f"  -> {write_mo_ta()}")
