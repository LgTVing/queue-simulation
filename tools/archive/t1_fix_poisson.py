"""
T1: Sửa nhãn kiểm định Poisson và thêm kiểm định quá phân tán theo ngày.
- Gắn nhãn chính xác: p<0.01 = "Bác bỏ (mạnh)", 0.01<=p<0.05 = "Bác bỏ (nhẹ)", p>=0.05 = "Chưa bác bỏ"
- Thêm thống kê quá phân tán: tổng khách/ngày, phương sai/trung bình, CV ngày
- Ước lượng CV_ngay^2 = (Var(N_d) - mu) / mu^2
"""
import sys, os
if sys.platform.startswith("win"):
    try: sys.stdout.reconfigure(encoding="utf-8")
    except: pass

import numpy as np
import pandas as pd
import scipy.stats as stats
import openpyxl
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
import a_data
from common import HOURS, H_LABELS

def poisson_label(p_val):
    """Gắn nhãn kiểm định Poisson theo quy tắc tường minh."""
    if p_val < 0.01:
        return "Bác bỏ (mạnh)"
    elif p_val < 0.05:
        return "Bác bỏ (nhẹ)"
    else:
        return "Chưa bác bỏ"

def run_t1():
    # 1. Load dữ liệu
    df = a_data.load_log()
    n_days = df["day"].nunique()
    days = sorted(df["day"].unique())
    
    # 2. Ma trận khách đến theo ngày x giờ
    counts_matrix = df.groupby(["day", "hour"]).size().unstack(fill_value=0)
    
    # 3. Kiểm định Poisson từng giờ với nhãn mới
    print("=" * 70)
    print("T1: KIỂM ĐỊNH POISSON THEO GIỜ (Nhãn sửa đúng)")
    print("=" * 70)
    print(f"{'Giờ':>10} {'p-value':>10} {'D':>8} {'Nhãn cũ':>18} {'Nhãn mới':>20}")
    print("-" * 70)
    
    old_labels = {
        0: "Chưa bác bỏ", 1: "Chưa bác bỏ", 2: "Lệch nhẹ", 3: "Lệch nhẹ",
        4: "Chưa bác bỏ", 5: "Lệch nhẹ", 6: "Lệch nhẹ", 7: "Lệch nhẹ", 8: "Chưa bác bỏ"
    }
    
    hourly_results = []
    for h in range(HOURS):
        counts_h = counts_matrix[h].values if h in counts_matrix.columns else np.zeros(n_days)
        n_bar = float(np.mean(counts_h))
        # Chỉ số phân tán D = sum((x_i - x_bar)^2 / x_bar)
        disp = float(np.sum((counts_h - n_bar)**2) / n_bar) if n_bar > 0 else 0.0
        p_val = float(stats.chi2.sf(disp, df=n_days - 1))
        
        new_label = poisson_label(p_val)
        hourly_results.append({
            "hour": h,
            "label": H_LABELS[h],
            "n_bar": round(n_bar, 2),
            "lambda": round(n_bar / 60.0, 4),
            "D": round(disp, 2),
            "p_value": round(p_val, 4),
            "old_label": old_labels.get(h, "?"),
            "new_label": new_label
        })
        print(f"{H_LABELS[h]:>10} {p_val:10.4f} {disp:8.2f} {old_labels.get(h, '?'):>18} {new_label:>20}")
    
    # 4. Thống kê quá phân tán theo ngày
    print("\n" + "=" * 70)
    print("T1: THỐNG KÊ QUÁ PHÂN TÁN THEO NGÀY")
    print("=" * 70)
    
    daily_totals = counts_matrix.sum(axis=1).values
    mu_day = float(np.mean(daily_totals))
    var_day = float(np.var(daily_totals, ddof=1))
    std_day = float(np.std(daily_totals, ddof=1))
    poisson_std = np.sqrt(mu_day)
    var_mean_ratio = var_day / mu_day if mu_day > 0 else 0.0
    cv_day = std_day / mu_day if mu_day > 0 else 0.0
    
    # CV_ngay^2 = (Var(N_d) - mu) / mu^2
    cv2_day_corrected = (var_day - mu_day) / (mu_day**2) if mu_day > 0 else 0.0
    cv_day_corrected = np.sqrt(max(0, cv2_day_corrected))
    
    # Kiểm định quá phân tán cho tổng ngày
    D_day = float(np.sum((daily_totals - mu_day)**2) / mu_day) if mu_day > 0 else 0.0
    p_day = float(stats.chi2.sf(D_day, df=n_days - 1))
    
    overdispersion = {
        "n_days": n_days,
        "daily_totals": daily_totals.tolist(),
        "mean_day": round(mu_day, 1),
        "std_day": round(std_day, 1),
        "var_day": round(var_day, 1),
        "poisson_std": round(poisson_std, 1),
        "var_mean_ratio": round(var_mean_ratio, 1),
        "cv_day": round(cv_day * 100, 1),  # percent
        "cv2_day_corrected": round(cv2_day_corrected, 4),
        "cv_day_corrected": round(cv_day_corrected * 100, 1),  # percent
        "D_day": round(D_day, 1),
        "p_day": p_day,
        "p_day_label": poisson_label(p_day)
    }
    
    print(f"  Tổng khách mỗi ngày: {daily_totals.tolist()}")
    print(f"  Trung bình μ = {mu_day:.1f}")
    print(f"  Độ lệch chuẩn thực tế σ = {std_day:.1f}")
    print(f"  Độ lệch chuẩn Poisson √μ = {poisson_std:.1f}")
    print(f"  Tỉ số Var/Mean = {var_mean_ratio:.1f} (>> 1 → quá phân tán)")
    print(f"  CV ngày = {cv_day*100:.1f}%")
    print(f"  CV_ngay^2 (trừ nhiễu Poisson) = {cv2_day_corrected:.4f}")
    print(f"  CV_ngay (sau hiệu chỉnh) = {cv_day_corrected*100:.1f}%")
    print(f"  Kiểm định quá phân tán: D = {D_day:.1f}, p-value = {p_day:.6f} → {poisson_label(p_day)}")
    
    # 5. Đếm nhãn
    n_reject_5pct = sum(1 for r in hourly_results if r["p_value"] < 0.05)
    n_reject_1pct = sum(1 for r in hourly_results if r["p_value"] < 0.01)
    
    print(f"\n  Tóm tắt nhãn mới:")
    print(f"    {n_reject_5pct}/9 giờ bác bỏ Poisson ở mức 5%")
    print(f"    {n_reject_1pct}/9 giờ bác bỏ ở mức 1%")
    print(f"    Chỉ giờ 12h-13h (p = {hourly_results[4]['p_value']}) chưa bác bỏ")
    
    # 6. Lưu vào CSV cho final_v2
    results_dir = os.path.join(BASE_DIR, "results", "final_v2")
    os.makedirs(results_dir, exist_ok=True)
    
    df_hourly = pd.DataFrame(hourly_results)
    df_hourly.to_csv(os.path.join(results_dir, "kiem_dinh_poisson.csv"), index=False, encoding="utf-8-sig")
    
    df_overdisp = pd.DataFrame([overdispersion])
    df_overdisp.to_csv(os.path.join(results_dir, "qua_phan_tan_ngay.csv"), index=False, encoding="utf-8-sig")
    
    print(f"\n  Đã lưu: results/final_v2/kiem_dinh_poisson.csv")
    print(f"  Đã lưu: results/final_v2/qua_phan_tan_ngay.csv")
    
    # 7. Cập nhật file Excel docs/thong_ke_mo_ta.xlsx
    update_excel_labels(hourly_results)
    
    # 8. Cập nhật file Excel docs/bang_tham_so.xlsx - thêm sheet quá phân tán
    update_bangthamsô_excel(overdispersion)
    
    return hourly_results, overdispersion

def update_excel_labels(hourly_results):
    """Cập nhật nhãn kiểm định trong file thong_ke_mo_ta.xlsx"""
    xlsx_path = os.path.join(BASE_DIR, "docs", "thong_ke_mo_ta.xlsx")
    if not os.path.exists(xlsx_path):
        print(f"  [WARN] Không tìm thấy {xlsx_path}")
        return
        
    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb["Thong_ke_theo_gio"]
    
    # Tìm cột "Kết luận Poisson" - duyệt header row
    header_row = 1
    ket_luan_col = None
    for col in range(1, ws.max_column + 1):
        val = ws.cell(row=header_row, column=col).value
        if val and "Ket luan" in str(val).replace(" ", "").replace("ế","e").replace("ậ","a"):
            ket_luan_col = col
            break
    
    if ket_luan_col is None:
        # Thêm cột mới
        ket_luan_col = ws.max_column + 1
        ws.cell(row=1, column=ket_luan_col, value="Ket luan Poisson (alpha=0.05)")
    
    for i, r in enumerate(hourly_results):
        ws.cell(row=i + 2, column=ket_luan_col, value=r["new_label"])
    
    wb.save(xlsx_path)
    print(f"  Đã cập nhật nhãn trong {xlsx_path}")

def update_bangthamsô_excel(overdispersion):
    """Thêm thông tin quá phân tán vào bang_tham_so.xlsx"""
    xlsx_path = os.path.join(BASE_DIR, "docs", "bang_tham_so.xlsx")
    if not os.path.exists(xlsx_path):
        print(f"  [WARN] Không tìm thấy {xlsx_path}")
        return
    
    wb = openpyxl.load_workbook(xlsx_path)
    
    # Thêm sheet mới cho quá phân tán nếu chưa có
    sheet_name = "qua_phan_tan"
    if sheet_name in wb.sheetnames:
        del wb[sheet_name]
    ws = wb.create_sheet(sheet_name)
    
    headers = ["Chi so", "Gia tri", "Ghi chu"]
    for i, h in enumerate(headers, 1):
        ws.cell(row=1, column=i, value=h)
    
    rows = [
        ("Trung binh khach/ngay (mu)", overdispersion["mean_day"], "14 ngay lam viec tieu chuan"),
        ("Do lech chuan thuc te (sigma)", overdispersion["std_day"], ""),
        ("Do lech chuan Poisson (sqrt(mu))", overdispersion["poisson_std"], ""),
        ("Phuong sai / Trung binh (Var/Mean)", overdispersion["var_mean_ratio"], f">> 1 cho thay qua phan tan manh"),
        ("CV ngay (%)", overdispersion["cv_day"], ""),
        ("CV_ngay^2 sau hieu chinh nhieu Poisson", overdispersion["cv2_day_corrected"], "(Var(N_d) - mu) / mu^2"),
        ("CV_ngay sau hieu chinh (%)", overdispersion["cv_day_corrected"], "He so nhan ngay dung cho mo phong"),
        ("D kiem dinh qua phan tan", overdispersion["D_day"], ""),
        ("p-value kiem dinh", overdispersion["p_day"], overdispersion["p_day_label"]),
    ]
    for i, (k, v, note) in enumerate(rows, 2):
        ws.cell(row=i, column=1, value=k)
        ws.cell(row=i, column=2, value=v)
        ws.cell(row=i, column=3, value=note)
    
    wb.save(xlsx_path)
    print(f"  Đã thêm sheet '{sheet_name}' vào {xlsx_path}")

if __name__ == "__main__":
    run_t1()
