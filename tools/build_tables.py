"""
tools/build_tables.py: Doc cac tep CSV trong common.RESULTS_DIR (results/final_v4/) va tao cac bang Markdown chuan.
Cac tai lieu bao cao se su dung cac bang nay de dam bao tinh dong bo tuyet doi.
"""

import os
import sys
if sys.platform.startswith("win"):
    try: sys.stdout.reconfigure(encoding="utf-8")
    except: pass

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
import common  # noqa: E402

def get_file(filename: str) -> str:
    return os.path.join(common.RESULTS_DIR, filename)

def df_to_markdown_table(df: pd.DataFrame, headers=None) -> str:
    """Chuyen DataFrame thanh Markdown table dep mat."""
    if headers is None:
        headers = list(df.columns)
    
    lines = []
    lines.append("| " + " | ".join(str(h) for h in headers) + " |")
    lines.append("|" + "|".join("---" for _ in headers) + "|")
    
    for _, row in df.iterrows():
        row_str = "| " + " | ".join(str(val) for val in row.values) + " |"
        lines.append(row_str)
        
    return "\n".join(lines)

def build_all_tables() -> dict:
    tables = {}
    
    # 1. Khoang tin cay Lambda Student-t (S1)
    f = get_file("khoang_tin_cay_lambda.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        df_disp = df[["khung_gio", "mean_khach_ngay", "poisson_hw_ngay", "t_hw_ngay", "ti_so_t_vs_poisson", "lambda_phut", "lambda_low_ci95", "lambda_high_ci95"]].copy()
        df_disp.columns = ["Khung giờ", "Số khách TB", "Poisson HW", "Student-t HW", "Tỉ số t/Poisson", "λ (khách/phút)", "CI95 Low", "CI95 High"]
        tables["lambda_ci"] = df_to_markdown_table(df_disp)
        
    # 2. Kiem dinh phan phoi phuc vu chi tiet (S10)
    f = get_file("kiem_dinh_phan_phoi_chi_tiet.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        df.columns = ["Phân phối", "Tham số", "Log-Likelihood", "AIC", "BIC", "KS Stat", "KS p-value (Bootstrap)", "cs² mô hình"]
        tables["fit_service"] = df_to_markdown_table(df)

    # 3. Chi so ky vong co dieu kien (S2)
    f = get_file("chi_so_ky_vong_dieu_kien.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        df_disp = df[["chinh_sach", "quay_gio", "SL_ky_vong_ngay_TB", "P_SL_ky_vong_ngay_ge90", "P_min_h_Eh_ge90", "so_gio_Eh_duoi_90_TB", "P_thuc_te_moi_gio_ge90", "P_thang_20ngay_moi_gio_ge90"]].copy()
        df_disp.columns = ["Chính sách", "Quầy-giờ", "SL kỳ vọng ngày TB", "P(SL ngày ≥ 90%)", "P(min_h E_h ≥ 90%)", "Số giờ E_h < 90%", "P(thực tế mọi giờ ≥ 90%)", "P(tháng 20 ngày ≥ 90%)"]
        tables["conditional_expectation"] = df_to_markdown_table(df_disp)

    # 4. Do nhay theo CV ngay (S3)
    f = get_file("do_nhay_cv_ngay.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        tables["do_nhay_cv"] = df_to_markdown_table(df)

    # 5. Posterior predictive check (S3)
    f = get_file("posterior_predictive_check.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        tables["pp_check"] = df_to_markdown_table(df)

    # 6. Nguong luu luong va Bo du bao som (S4)
    f = get_file("nguong_luu_luong_chi_tiet.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        tables["nguong_v"] = df_to_markdown_table(df)
        
    f_comp = get_file("danh_gia_chinh_sach_du_bao_14ngay.csv")
    if os.path.exists(f_comp):
        df_comp = pd.read_csv(f_comp)
        tables["chinh_sach_ghep_14ngay"] = df_to_markdown_table(df_comp)

    # 7. Kiem chung 3 tang (S8)
    f = get_file("kiem_chung.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        tables["kiem_chung"] = df_to_markdown_table(df)

    # 8. Phan ra phuong sai bootstrap (S5)
    f = get_file("phan_ra_phuong_sai.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        tables["phan_ra_phuong_sai"] = df_to_markdown_table(df)

    # 9. Ngoai mau (S6)
    f = get_file("ngoai_mau.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        tables["ngoai_mau"] = df_to_markdown_table(df)

    # 10. 14 ngay phan dinh Train/Test (S7)
    f = get_file("theo_14_ngay.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        tables["theo_14_ngay"] = df_to_markdown_table(df)

    # 11. Do nhay phan phoi (S9)
    f = get_file("do_nhay_phan_phoi.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        tables["do_nhay_phan_phoi"] = df_to_markdown_table(df)

    # 12. Chi phi (S11)
    f = get_file("chi_phi.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        tables["chi_phi"] = df_to_markdown_table(df)

    # 13. Pha 3 vet can (C6)
    f = get_file("pha3.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        n = df["loai_thu_nghiem"].value_counts()
        tables["pha3_summary"] = (f"- Tổng số phép thử nghiệm vét cạn Pha 3: {len(df)} cấu hình "
                                  f"({n.get('Swap 1 quay', 0)} hoán đổi 1 quầy + {n.get('Giam 2 quay', 0)} giảm 2 quầy).\n"
                                  f"- Số cấu hình khả thi: {int((df['kha_thi'] == 'Y').sum())}/{len(df)}.")

    print(f"Da sinh thanh cong {len(tables)} bang Markdown tu results/")
    return tables

if __name__ == "__main__":
    t = build_all_tables()
    for name, tbl in t.items():
        print(f"\n--- BẢNG: {name} ---")
        print(tbl[:200] + "..." if len(tbl) > 200 else tbl)
