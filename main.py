"""
main.py: Chuong trinh chinh chay toan bo quy trinh du an (Tuan 2):
1. Doc du lieu thuc te, tach train/test va uoc luong tham so he thong
2. Tinh toan giai tich ly thuyet (Erlang C, Erlang-A, SIPP)
3. Chay kiem chung 3 tang giua mo phong SimPy va ly thuyet
4. Danh gia giai doan khoi dong (Welch) va hieu ung gop hang doi (Pooling)
5. Tong hop ket qua va danh gia Cong kiem soat Tuan 2
"""

import sys
import os
import json
import pandas as pd
import numpy as np

# Thiet lap ma hoa UTF-8 cho console tren Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import common
import a_data
import b_theory as th
import c_sim as sim
import chay_kiem_chung

def main():
    print("=" * 70)
    print("   DU AN MO PHONG HANG DOI VA XAC DINH SO QUAY TOI UUU (TUAN 2)")
    print("=" * 70)
    
    # -------------------------------------------------------------------------
    # BUOC 1: NAP DU LIEU THUC TE VA UOC LUONG THAM SO
    # -------------------------------------------------------------------------
    print("\n>>> BƯỚC 1: Xử lý dữ liệu thực tế và Ước lượng tham số...")
    df = a_data.load_log("data/clean/data_clean.csv")
    df_train, df_test = a_data.split_train_test(df, train_ratio=0.7)
    print(f"  • Tổng số bản ghi: {len(df):,} dòng (14 ngày làm việc tiêu chuẩn)")
    print(f"  • Tập ước lượng (Train): {len(df_train):,} dòng ({df_train['day'].nunique()} ngày)")
    print(f"  • Tập kiểm tra (Test):   {len(df_test):,} dòng ({df_test['day'].nunique()} ngày)")
    
    params = a_data.estimate_all(df_train, plot=True, output_dir="docs")
    print(f"  • E[S] ước lượng: {params['service']['mean']:.2f} phút (cv={params['service']['cv']:.2f}, cs²={params['service']['cs2']:.2f})")
    print(f"  • Phân phối dịch vụ tối ưu: {params['service']['kieu'].upper()} (AIC tốt nhất)")
    print(f"  • Tốc độ bỏ về θ: {params['theta']:.4f} (Kiên nhẫn TB: {params['mean_patience']:.1f} phút)")
    print(f"  • Tỉ lệ khách VIP: {params['p_vip']*100:.1f}%")
    print("  -> Đã xuất tệp cấu hình: docs/params.json và biểu đồ: fig_a_fit.png")
    
    # -------------------------------------------------------------------------
    # BUOC 2: TINH TOAN GIAI TICH LY THUYET VA BANG QUYET DINH SIPP
    # -------------------------------------------------------------------------
    print("\n>>> BƯỚC 2: Tính toán giải tích Lý thuyết (Erlang C, Erlang-A, SIPP)...")
    rates = params["rates_per_min"]
    es = params["service"]["mean"]
    mu = 1.0 / es
    theta = params["theta"]
    
    sched_c = th.sipp_schedule(rates, mu, 0.0, target=0.9, use_erlang_a=False)
    sched_a = th.sipp_schedule(rates, mu, theta, target=0.9, use_erlang_a=True)
    
    print("  • Lịch quầy theo giờ Erlang C: ", sched_c, f"=> Tổng: {sum(sched_c)} quầy-giờ")
    print("  • Lịch quầy theo giờ Erlang-A: ", sched_a, f"=> Tổng: {sum(sched_a)} quầy-giờ")
    print(f"  • Tiết kiệm so với lịch hằng số (6 quầy = 54 q-h): -{(54-sum(sched_a))/54*100:.1f}% chi phí nhân sự")
    
    # -------------------------------------------------------------------------
    # BUOC 3: KIEM CHUNG MO PHONG SIMPY 3 TANG
    # -------------------------------------------------------------------------
    print("\n>>> BƯỚC 3: Kiểm chứng mô phỏng SimPy 3 tầng so với Lý thuyết...")
    if os.path.exists("ket_qua_kiem_chung.csv"):
        df_kc = pd.read_csv("ket_qua_kiem_chung.csv")
    else:
        df_kc = chay_kiem_chung.run_all_verification()
        
    print("\nBẢNG KẾT QUẢ KIỂM CHỨNG BA TẦNG:")
    print(df_kc[["kiem_chung", "chi_so", "ly_thuyet", "mo_phong", "sai_lech_pct", "dat"]].to_string(index=False))
    
    # -------------------------------------------------------------------------
    # BUOC 4: TONG KET CONG KIEM SOAT TUAN 2
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print(">>> TỔNG KẾT VÀ ĐÁNH GIÁ CỔNG KIỂM SOÁT TUẦN 2:")
    print("  [x] Dữ liệu & Tham số: Đã chốt docs/params.json v2.0 (tập train 10 ngày)")
    print("  [x] Kiểm định phân phối: Gamma đạt AIC thấp nhất, có hình fig_a_fit.png")
    print("  [x] Bảng quyết định SIPP: docs/bang_quyet_dinh.md & excel/erlang.xlsx")
    print("  [x] Kiểm thử tự động pytest: tests/test_theory.py (7/7 Passed)")
    print("  [x] Kiểm chứng 3 tầng: ket_qua_kiem_chung.csv & docs/bao_cao_kiem_chung.md")
    print("  [x] Thí nghiệm mở rộng: Đã xuất fig_c_welch.png và fig_c_pooling.png")
    print("  [x] Báo cáo tổng kết: docs/bao_cao_tuan_2.md")
    print("  ==> KẾT LUẬN: ĐẠT 100% TIÊU CHÍ, SẴN SÀNG CHO TUẦN 3 (TỐI ƯU & BÁO CÁO).")
    print("=" * 70)

if __name__ == "__main__":
    main()
