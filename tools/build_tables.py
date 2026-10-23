"""
tools/build_tables.py: Doc cac tep CSV trong results/final_v2/ va tao cac bang Markdown chuan.
Cac tai lieu bao cao se su dung cac bang nay de dam bao tinh dong bo tuyet doi.
"""

import os
import sys
if sys.platform.startswith("win"):
    try: sys.stdout.reconfigure(encoding="utf-8")
    except: pass

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_V2 = os.path.join(BASE_DIR, "results", "final_v2")

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
    
    # 1. Kiem dinh Poisson
    f = os.path.join(RESULTS_V2, "kiem_dinh_poisson.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        df_display = df[["label", "n_bar", "lambda", "D", "p_value", "new_label"]].copy()
        df_display.columns = ["Khung giờ", "Số khách TB (khách/ngày)", "Tốc độ đến λ (khách/phút)", "Chỉ số D", "p-value", "Kết luận (α=0.05)"]
        tables["poisson"] = df_to_markdown_table(df_display)
        
    # 2. Qua phan tan ngay
    f = os.path.join(RESULTS_V2, "qua_phan_tan_ngay.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        tables["qua_phan_tan"] = (
            f"- Số ngày quan sát: {df.loc[0, 'n_days']} ngày\n"
            f"- Trung bình: {df.loc[0, 'mean_day']} khách/ngày, Độ lệch chuẩn thực tế: {df.loc[0, 'std_day']} khách\n"
            f"- Độ lệch chuẩn Poisson: {df.loc[0, 'poisson_std']} khách (Tỉ số Var/Mean = {df.loc[0, 'var_mean_ratio']})\n"
            f"- CV ngày thực tế: {df.loc[0, 'cv_day']}%, CV ngày sau trừ nhiễu Poisson: {df.loc[0, 'cv_day_corrected']}%\n"
            f"- Kiểm định quá phân tán: D = {df.loc[0, 'D_day']}, p-value = {df.loc[0, 'p_day']:.4e} ({df.loc[0, 'p_day_label']})"
        )
        
    # 3. So sanh chinh sach co bien dong
    f = os.path.join(RESULTS_V2, "so_sanh_chinh_sach_v2.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        df.columns = ["Chính sách", "Quầy-giờ", "SL (Không BĐ)", "SL giờ tệ (Không BĐ)", "SL (Có BĐ ngày)", "P(Ngày ≥ 90%)", "P(Mọi giờ ≥ 90%)", "SL Phân vị 5%"]
        tables["so_sanh_chinh_sach"] = df_to_markdown_table(df)

    # 4. Bien dong ngay
    f = os.path.join(RESULTS_V2, "bien_dong_ngay.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        df_disp = df[["chinh_sach", "quay_gio", "sl_toan_ngay", "P_SL_ngay_ge90", "P_moi_gio_ge90", "so_gio_TB_duoi_90", "p_ab", "wq"]].copy()
        df_disp.columns = ["Chính sách", "Quầy-giờ", "SL Toàn ngày", "P(Ngày ≥ 90%)", "P(Mọi giờ ≥ 90%)", "Số giờ TB < 90%", "Tỉ lệ bỏ về", "Wq (phút)"]
        tables["bien_dong_ngay"] = df_to_markdown_table(df_disp)

    # 5. Theo ngay quan sat
    f = os.path.join(RESULTS_V2, "theo_ngay.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        df_disp = df[["ngay", "tong_khach", "sl_opt44", "dat_sl_opt44", "sl_rob48", "dat_sl_rob48", "sl_const6", "dat_sl_const6"]].copy()
        df_disp.columns = ["Ngày", "Tổng khách", "SL Lịch 44", "Đạt SLA 44", "SL Lịch 48", "Đạt SLA 48", "SL Lịch 54", "Đạt SLA 54"]
        tables["theo_ngay"] = df_to_markdown_table(df_disp)

    # 6. Ca lam viec MILP
    f = os.path.join(RESULTS_V2, "lich_theo_ca_v2.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        df.columns = ["Phương án ca làm việc", "Mẫu phủ quầy theo giờ", "Giờ làm việc", "Giờ có mặt", "Số nhân viên"]
        tables["ca_lam_viec"] = df_to_markdown_table(df)

    # 7. Do nhay phan phoi
    f = os.path.join(RESULTS_V2, "do_nhay_phan_phoi_v2.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        df.columns = ["Phân phối phục vụ", "SL toàn ngày", "Nửa rộng CI95", "Cận dưới CI95", "Hiệu số vs Gamma", "CI95 của Hiệu số", "Khác biệt có ý nghĩa?"]
        tables["do_nhay_phan_phoi"] = df_to_markdown_table(df)

    # 8. Ngoai mau
    f = os.path.join(RESULTS_V2, "ngoai_mau_v2.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        df_disp = df[["khung_gio", "so_quay", "diff_lam_pct", "sl_sim_A", "sl_sim_B", "sl_obs", "chenh_sl_A_obs"]].copy()
        df_disp.columns = ["Khung giờ", "Số quầy", "Chênh λ (%)", "SL Mô phỏng A", "SL Mô phỏng B", "SL Thực tế", "Chênh lệch (A - Thực)"]
        tables["ngoai_mau"] = df_to_markdown_table(df_disp)

    # 9. Dao dong seed
    f = os.path.join(RESULTS_V2, "dao_dong_seed.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        df.columns = ["Seed Base", "SL Toàn ngày", "Nửa rộng CI95", "Tỉ lệ bỏ về", "Wq (phút)", "SL Giờ tệ nhất (Low CI)"]
        tables["dao_dong_seed"] = df_to_markdown_table(df)

    # 10. Tham so thanh phan
    f = os.path.join(RESULTS_V2, "tham_so_thanh_phan.csv")
    if os.path.exists(f):
        df = pd.read_csv(f)
        df.columns = ["Thành phần mô hình", "Bộ tham số sử dụng", "Nguồn / Ghi chú"]
        tables["tham_so_thanh_phan"] = df_to_markdown_table(df)

    print(f"Da sinh thanh cong {len(tables)} bang Markdown tu results/final_v2/")
    return tables

if __name__ == "__main__":
    t = build_all_tables()
    for name, tbl in t.items():
        print(f"\n--- BẢNG: {name} ---")
        print(tbl[:200] + "..." if len(tbl) > 200 else tbl)
