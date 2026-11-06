"""
g_report.py: Giai doan 'report':
1. doi_chieu_v4_v5.csv: moi chi so chinh gia tri V4 (doc tu results/final_v4, cung cach doc
   voi V5), gia tri V5, chenh lech va nguyen nhan; them chi so moi M6 (gio cong), M7 (muc P),
   M8 (tang quay). Ban V3 -> V4 giu trong results/final_v4/doi_chieu_v3_v4.csv
2. MO_TA.md: mo ta tu dong thu muc ket qua (duong dan tuong doi), moi truong,
   he so so lan lap va thoi gian chay tung giai doan
"""

import os
import re
import sys
import json
import datetime
from typing import Dict, List, Optional
import numpy as np
import pandas as pd

import common
from common import TARGET_SLA
import d_experiments as dx
import f_scenarios

# Nguon so lieu V4 de doi chieu (chi doc, khong ghi)
PREV_RESULTS_DIR = os.path.join(common.BASE_DIR, "results", "final_v4")
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
    "toi_uu_sla_khach_thuong.csv": ("optimize / M9", "Lich toi uu khi SLA tinh rieng khach thuong, so voi Lich 45 va Lich 48 (seed danh gia, gio cong xep ca)"),
    "sl_theo_nhom.csv": ("optimize / F6", "SL theo gio: gop moi khach (SLA chinh), khach thuong <= 5 phut va VIP <= 2 phut (giam sat), cung seed danh gia"),
    "doi_chieu_xa_hang.csv": ("optimize / F1", "SL gio cuoi khi xa hang giu so quay gio cuoi vs mo het c_max"),
    "do_nhay_kien_nhan.csv": ("optimize / M1", "Lich va chi so theo kien nhan trung binh 9,2 -> vo cung"),
    "toi_uu_rang_buoc_bo_ve.csv": ("optimize / M2", "Toi uu voi rang buoc ti le bo ve, SL o nguong 2/3/5 phut"),
    "toi_uu_theo_ca.csv": ("optimize / M6", "Moi lich phu theo ca da thu (gio cong, phuong an ca, SL, can duoi gio te nhat)"),
    "toi_uu_xac_suat_ngay.csv": ("optimize / M7", "Lich nho nhat theo muc P(SL ngay >= 90%) co bien dong ngay, quay-gio va theo ca; xac nhan bang dai seed doc lap 2.000 lan lap (F5), doi chieu Lich 48, 14 ngay thuc te"),
    "chinh_sach_tang_quay.csv": ("robust / M8", "Lich 45 + mo them quay khi hang cho dai so voi Lich 45/48 co dinh, 4 kich ban + 14 ngay"),
    "kien_nhan_weibull_fit.csv": ("optimize / S12", "MLE kien nhan Weibull co kiem duyet tren train so voi mu (AIC, ti so hop ly)"),
    "kien_nhan_weibull.csv": ("optimize / S12", "Lich toi uu va danh gia Lich 45/48 duoi kien nhan mu va Weibull"),
    "lambda_nua_gio.csv": ("optimize / S15", "Lambda hai nua moi khung gio (train), kiem dinh binomial va Holm-Bonferroni"),
    "khung_30_phut.csv": ("optimize / S15", "Lich 45/48 va lich toi uu khi lambda 8h-10h theo nua gio"),
    "toi_uu_theo_ca_linh_hoat.csv": ("optimize / M6", "Nhu toi_uu_theo_ca.csv voi nghi trua linh hoat 9h-16h"),
    "toi_uu_theo_ca_linh_hoat_top.csv": ("optimize / M6", "Top-5 lich kha thi, nghi trua linh hoat 9h-16h"),
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
    "doi_chieu_v4_v5.csv": ("report", "Doi chieu chi so chinh V4 vs V5 kem nguyen nhan, chi so moi M6-M8"),
    "pytest_log.txt": ("test", "Log pytest"),
    RUN_LOG: ("report", "Thoi gian chay va he so so lan lap tung giai doan"),
}

# =============================================================================
# DOC SO LIEU MOT THU MUC KET QUA
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
    if not os.path.exists(path):
        return None
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:  # vd toi_uu_theo_ca_top.csv khi M6 khong tim thay lich (smoke test)
        return pd.DataFrame()

def _row(df: Optional[pd.DataFrame], col: str, key) -> Optional[pd.Series]:
    if df is None:
        return None
    sub = df[df[col] == key]
    return None if sub.empty else sub.iloc[0]

def _get(r: Optional[pd.Series], c: str) -> float:
    return float(r[c]) if r is not None and c in r and pd.notna(r[c]) else np.nan

def metrics(R: str) -> Dict[str, object]:
    """Cac chi so chinh doc tu thu muc ket qua R (cung cach doc cho V4 va V5)."""
    out: Dict[str, object] = {}
    sch_path = os.path.join(R, dx.SCHEDULES_FILE)
    sch = {}
    if os.path.exists(sch_path):
        with open(sch_path, encoding="utf-8") as f:
            sch = json.load(f)
    comp = _read(os.path.join(R, "so_sanh_chinh_sach.csv"))
    bd = _read(os.path.join(R, "so_sanh_chinh_sach_bd.csv"))
    d14 = _read(os.path.join(R, "theo_14_ngay_tong_hop.csv"))
    drain = _read(os.path.join(R, "doi_chieu_xa_hang.csv"))
    m3 = _read(os.path.join(R, "m3_dich_vu_thuc_nghiem.csv"))
    ca = _read(os.path.join(R, "lich_theo_ca.csv"))
    opt = _row(comp, "chinh_sach", "Toi uu mo phong")
    rob = _row(comp, "chinh_sach", "Ben vung (+10% nhu cau)")
    opt_bd = _row(bd, "chinh_sach", "Toi uu")
    for k in ("toi_uu", "sipp_erlang_c", "sipp_erlang_a"):
        if k in sch:
            out[f"qh_{k}"] = float(sum(sch[k]))
    if "toi_uu" in sch:
        out["lich_toi_uu"] = str(sch["toi_uu"])
    out.update({
        "sl_toi_uu": _get(opt, "sl_toan_ngay"), "sl_te_nhat_low": _get(opt, "sl_gio_te_nhat_low"),
        "gio_te_nhat": _get(opt, "gio_te_nhat"), "p_ab": _get(opt, "ti_le_bo_ve"), "wq": _get(opt, "wq_phut"),
        "rho": _get(opt, "hieu_suat_rho"), "qh_ben_vung": _get(rob, "quay_gio"), "sl_ben_vung": _get(rob, "sl_toan_ngay"),
        "p_ngay_ge90": _get(opt_bd, "P_SL_ngay_ge90"), "p_moi_gio_ge90": _get(opt_bd, "P_moi_gio_ge90"),
        "so_ngay_dat": _get(_row(d14, "chinh_sach", "Toi uu"), "so_ngay_dat"),
        "sl_gio_cuoi": _get(_row(drain, "drain_policy", "keep_last"), "sl_gio_cuoi"),
    })
    if m3 is not None:
        g = m3[(m3["chinh_sach"] == "Lich toi uu (phuc vu thuc nghiem)") & (m3["mo_hinh_danh_gia"] == "Gamma")]
        out["sl_gamma"] = float(g["sl_toan_ngay"].iloc[0]) if len(g) else np.nan
    # Gio cong: V4 = xep ca MILP sau khi toi uu quay-gio; V5 = M6 toi uu truc tiep theo gio cong
    mix = _row(ca, "truong_hop", "Mo hinh B (nghi 11h-14h): hon hop 8h+4h")
    if mix is not None:
        out["gio_cong_xep_ca"] = _get(mix, "tong_qh_lam_viec")
        out["lich_xep_ca"] = mix["phu_quay"]
        out["ca_xep_ca"] = f"{int(mix['so_nv_8h'])} ca 8h + {int(mix['so_nv_4h'])} ca 4h"
    return out

# =============================================================================
# BANG DOI CHIEU V4 / V5
# =============================================================================

def _v5_rows() -> List[tuple]:
    """Chi so moi o V5 (M6, M7, M8): (chi so, gia tri V4 neu co, gia tri V5, nguyen nhan)."""
    R = common.RESULTS_DIR
    rows = []
    top = _read(os.path.join(R, "toi_uu_theo_ca_top.csv"))
    trials = _read(os.path.join(R, "toi_uu_theo_ca.csv"))
    if top is not None and len(top):
        b = top.iloc[0]
        t = _row(trials, "phu_quay", b["phu_quay"])
        ca = f"{int(t['n_ca_8h'])} ca 8h + {int(t['n_ca_4h'])} ca 4h" if t is not None else b["phuong_an_ca"]
        n_tried = int((trials["gio_cong"] < b["gio_cong"]).sum()) if trials is not None else 0
        rows += [
            ("Lich theo ca tot nhat o gio cong toi thieu (M6)", None, b["phu_quay"],
             "M6: lich dau tien trong top-5 kha thi o gio cong toi thieu (seed danh gia)"),
            ("Phuong an ca (M6)", None, ca, "M6"),
            ("SL toan ngay lich theo ca M6", None, float(b["sl_toan_ngay"]), "M6 (seed danh gia, 300 lan lap)"),
            ("SL gio te nhat (can duoi CI95) lich theo ca M6", None, float(b["sl_gio_te_nhat_low"]), "M6"),
            ("P(SL ngay >= 90%) co bien dong ngay, lich theo ca M6", None, float(b["P_SL_ngay_ge90"]), "M6"),
            ("So lich phu da thu duoi gio cong toi thieu (deu khong kha thi)", None, float(n_tried),
             "M6 pipeline slack=0; tham do slack=1 (3.180 lich, docs/KE_HOACH_V5.md) cung khong co lich kha thi"),
        ]
    p7 = _read(os.path.join(R, "toi_uu_xac_suat_ngay.csv"))
    if p7 is not None:
        ref = p7[p7["khong_gian"] == f_scenarios.REF_P_DAY].dropna(subset=["lich"])
        if len(ref):
            rows.append(("P(SL ngay >= 90%) seed danh gia, Lich 48 doi chieu (M7)", None,
                         float(ref.iloc[0]["P_ngay_danh_gia"]), "M7 (F5): cung dai seed xac nhan doc lap"))
        for r in p7.dropna(subset=["lich", "min_p"]).itertuples():
            label = f"P(SL ngay >= 90%) >= {r.min_p:.0%}, {r.khong_gian}"
            rows += [
                (f"Lich nho nhat dat {label} (M7)", None, r.lich, "M7"),
                (f"Quay-gio / gio cong lich {label}", None, f"{int(r.quay_gio)} / {int(r.gio_cong_ca)}", "M7"),
                (f"P(SL ngay >= 90%) seed danh gia, lich {label}", None, float(r.P_ngay_danh_gia), "M7"),
            ]
    m8 = _read(os.path.join(R, "chinh_sach_tang_quay.csv"))
    if m8 is not None:
        rec = f_scenarios.recommended_surge(m8)
        l48 = _row(m8, "chinh_sach", "Lich 48 co dinh")
        if rec is not None:
            why = "M8: chinh sach khuyen nghi (f_scenarios.recommended_surge)"
            ref = why + "; cot V4 = Lich 48 co dinh cung kich ban"
            rows += [
                ("Chinh sach tang quay khuyen nghi (M8)", None, rec["chinh_sach"], why),
                ("Quay-gio mo TB 14 ngay: Lich 48 co dinh -> Lich 45 + tang quay",
                 _get(l48, "quay_gio_TB_14_ngay"), float(rec["quay_gio_TB_14_ngay"]), ref),
                ("P(SL ngay >= 90%) bien dong ngay: Lich 48 co dinh -> Lich 45 + tang quay",
                 _get(l48, "P_SL_ngay_ge90_bien_dong"), float(rec["P_SL_ngay_ge90_bien_dong"]), ref),
                ("SL gio te nhat (can duoi CI95) nhu cau +10%: Lich 48 co dinh -> Lich 45 + tang quay",
                 _get(l48, "gio_te_nhat_low_nhu cau +10%"), float(rec["gio_te_nhat_low_nhu cau +10%"]), ref),
                ("So ngay quan sat dat SLA (/14), Lich 45 + tang quay", None, float(rec["so_ngay_dat_14"]), why),
            ]
            if "gio_te_nhat_low_ngay 10" in m8:
                rows.append(("SL gio te nhat (can duoi CI95) ngay 10: Lich 48 co dinh -> Lich 45 + tang quay",
                             _get(l48, "gio_te_nhat_low_ngay 10"), float(rec["gio_te_nhat_low_ngay 10"]),
                             "M8 kich ban ngay 10 (E[S] x1.29 o 14h-17h, Model.service_by_hour); cot V4 = Lich 48 co dinh"))
    flex = _read(os.path.join(R, "toi_uu_theo_ca_linh_hoat_top.csv"))
    if flex is not None and len(flex):
        rows += [("Gio cong toi thieu/ngay, nghi trua linh hoat 9h-16h (M6)", None, float(flex.iloc[0]["gio_cong"]), "M6 bien the"),
                 ("Lich theo ca tot nhat, nghi trua 9h-16h (M6)", None, flex.iloc[0]["phu_quay"], "M6 bien the")]
    return rows + _stat_rows(R)


def _stat_rows(R: str) -> List[tuple]:
    """S12-S15: chi so thong ke bo sung; cot V4 la cach lam cu neu co."""
    rows = []
    f4 = _read(os.path.join(PREV_RESULTS_DIR, "du_bao_som_hoi_quy.csv"))
    f5 = _read(os.path.join(R, "du_bao_som_hoi_quy.csv"))
    if f5 is not None and "rmse_test" in f5:
        a, b = (f4.iloc[0] if f4 is not None else None), f5.iloc[0]
        why = "S13: V4 fit tren 14 ngay (RMSE trong mau); V5 fit tren 10 ngay train, RMSE tren 4 ngay test"
        rows += [("Du bao som: he so goc", _get(a, "slope"), float(b["slope"]), why),
                 ("Du bao som: he so tu do", _get(a, "intercept"), float(b["intercept"]), why),
                 ("Du bao som: r", _get(a, "r"), float(b["r_train"]), why),
                 ("Du bao som: RMSE (khach/ngay)", _get(a, "rmse"), float(b["rmse_test"]), why),
                 ("Du bao som: so ngay hut SLA bi bo lo (/2)", None, float(b["so_ngay_bo_lo"]), "S13")]
    ce = _read(os.path.join(R, "chi_so_ky_vong_dieu_kien.csv"))
    if ce is not None and "P_thuc_te_moi_gio_boot_low95" in ce:
        r = _row(ce, "chinh_sach", "Toi uu")
        rows += [("P(thuc te moi gio >= 90%) Lich 45: do rong CI95 (Wilson -> cluster bootstrap)",
                  _get(r, "P_thuc_te_moi_gio_high95") - _get(r, "P_thuc_te_moi_gio_low95"),
                  _get(r, "P_thuc_te_moi_gio_boot_high95") - _get(r, "P_thuc_te_moi_gio_boot_low95"),
                  "S14: Wilson coi 6.000 ngay-lan lap doc lap; bootstrap resample 200 kich ban")]
    fit = _read(os.path.join(R, "kien_nhan_weibull_fit.csv"))
    w = _read(os.path.join(R, "kien_nhan_weibull.csv"))
    if fit is not None and w is not None:
        fr = fit.iloc[0]
        opt_w = _row(w[w["kien_nhan"] == "Weibull"], "chinh_sach", "Toi uu Weibull")
        rows += [("Kien nhan Weibull: shape (mu = 1)", 1.0, float(fr["shape"]), "S12"),
                 ("Kien nhan TB (phut): mu -> Weibull", float(fr["mean_patience_exp"]), float(fr["mean_patience_weibull"]), "S12"),
                 ("AIC kien nhan: mu -> Weibull", float(fr["aic_exp"]), float(fr["aic_weibull"]), "S12"),
                 ("Tong quay-gio lich toi uu: kien nhan mu -> Weibull", None, _get(opt_w, "quay_gio"), "S12")]
    h30 = _read(os.path.join(R, "khung_30_phut.csv"))
    if h30 is not None:
        opt30 = _row(h30[h30["mo_hinh_den"] == "Nua gio 8h-10h"], "chinh_sach", "Toi uu nua gio")
        rows.append(("Tong quay-gio lich toi uu: lambda theo gio -> nua gio 8h-10h", None, _get(opt30, "quay_gio"), "S15"))
    return rows

def build_doi_chieu() -> pd.DataFrame:
    v4, v5 = metrics(PREV_RESULTS_DIR), metrics(common.RESULTS_DIR)
    same = "Khong doi: P1/P2 giu ket qua giong tung byte, M6-M8 khong dong vao chi so V4"
    old = [
        ("Lich toi uu", "lich_toi_uu"), ("Tong quay-gio lich toi uu", "qh_toi_uu"),
        ("Tong quay-gio SIPP Erlang C", "qh_sipp_erlang_c"), ("Tong quay-gio SIPP Erlang-A", "qh_sipp_erlang_a"),
        ("SL toan ngay lich toi uu", "sl_toi_uu"), ("SL gio te nhat (can duoi CI95) lich toi uu", "sl_te_nhat_low"),
        ("Gio te nhat (chi so 0-8)", "gio_te_nhat"), ("Ti le bo ve lich toi uu", "p_ab"),
        ("Wq TB lich toi uu (phut)", "wq"), ("Hieu suat rho lich toi uu", "rho"),
        ("Tong quay-gio lich ben vung (+10%)", "qh_ben_vung"), ("SL toan ngay lich ben vung", "sl_ben_vung"),
        ("P(SL ngay >= 90%) co bien dong ngay, lich toi uu", "p_ngay_ge90"),
        ("P(moi gio >= 90%) co bien dong ngay, lich toi uu", "p_moi_gio_ge90"),
        ("So ngay quan sat dat SLA (/14), lich toi uu", "so_ngay_dat"),
        ("SL gio cuoi lich toi uu (xa hang giu so quay gio cuoi)", "sl_gio_cuoi"),
        ("SL toan ngay lich toi uu danh gia bang phuc vu Gamma", "sl_gamma"),
    ]
    rows = [(name, v4.get(k), v5.get(k), same) for name, k in old]
    top = _read(os.path.join(common.RESULTS_DIR, "toi_uu_theo_ca_top.csv"))
    w5 = float(top.iloc[0]["gio_cong"]) if top is not None and len(top) else np.nan
    rows += [
        ("Gio cong toi thieu/ngay (nghi trua 11h-14h)", v4.get("gio_cong_xep_ca"), w5,
         "V4: xep ca MILP phu lich toi uu quay-gio; V5: M6 toi uu truc tiep theo gio cong ca"),
        ("Lich phu theo ca, V4 (xep ca lich toi uu quay-gio)", v4.get("lich_xep_ca"), None, "V5 thay bang lich M6"),
        ("Phuong an ca, V4 (xep ca lich toi uu quay-gio)", v4.get("ca_xep_ca"), None, "V5 thay bang phuong an M6"),
    ]
    rows += _v5_rows()

    out = []
    for name, a, b, cause in rows:
        a = np.nan if a is None else a
        b = np.nan if b is None else b
        if pd.isna(a) or pd.isna(b):
            diff = "moi o V5" if pd.isna(a) else "chi co o V4"
        else:
            try:
                diff = float(b) - float(a)
            except (TypeError, ValueError):
                diff = "giong" if str(a) == str(b) else "khac"
        if cause == same and diff not in (0.0, "giong"):
            cause = "KHAC V4 NGOAI Y MUON: can dieu tra truoc khi dong bang"
        out.append({"chi_so": name, "gia_tri_V4": a, "gia_tri_V5": b, "chenh_lech": diff, "nguyen_nhan": cause})
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
        f"- **Seed:** chọn lịch `seed_base={dx.SEED_SELECT}`, đánh giá cuối `seed_base={dx.SEED_EVAL}` "
        f"(bước {common.SEED_STEP}; hai dải trùng "
        f"{len(set(common.seed_range('select')) & set(common.seed_range('eval')))}/{common.SEED_BANDS['eval'][1]} lần lặp, "
        f"giữ để không đổi số V5); M7 đánh giá độc lập `seed_base={common.SEED_BANDS['eval_day'][0]}` "
        f"({common.SEED_BANDS['eval_day'][1]} lần lặp). Sổ đăng ký: `common.SEED_BANDS`",
        "- **Mô hình chính:** NHPP theo giờ (F2), phục vụ thực nghiệm lấy mẫu từ train (M3), bỏ về mũ θ, "
        "VIP ưu tiên không ngắt, xả hàng giữ số quầy giờ cuối (F1)",
    ]
    if sch:
        lines.append(f"- **Lịch tối ưu:** `{sch.get('toi_uu')}` ({sum(sch.get('toi_uu', []))} quầy-giờ); "
                     f"bền vững +10%: `{sch.get('ben_vung')}`")
    if "toi_uu_theo_ca" in sch:
        lines.append(f"- **Lịch theo ca ít giờ công nhất (M6):** `{sch['toi_uu_theo_ca']}` "
                     f"({sum(sch['toi_uu_theo_ca'])} quầy-giờ mở; xem `toi_uu_theo_ca_top.csv`)")
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
    df.to_csv(common.out_path("doi_chieu_v4_v5.csv"), index=False, encoding="utf-8-sig")
    print(df.to_string(index=False))
    print(f"  -> {write_mo_ta()}")
