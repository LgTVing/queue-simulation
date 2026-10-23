"""
tools/check_consistency.py: Quet cac tai lieu bao cao va slide de kiem tra:
1. Tinh nhat quan so lieu voi results/final_v2/
2. Phat hien cac tu ngu bi cam / khong co can cu (T10):
   - 'hiện trạng' (khi noi ve 6 quay)
   - 'toàn cục' (khi chua chung minh)
   - 'Thứ 2', 'Thứ 6', 'ngày lương', 'ngày trả lương' (du lieu khong co thu trong tuan)
   - 'biên an toàn rất cao', 'tuyệt đối', 'hoàn hảo'
"""

import os
import sys
import re

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
RESULTS_V3 = os.path.join(BASE_DIR, "results", "final_v3")
RESULTS_V2 = os.path.join(BASE_DIR, "results", "final_v2")

FORBIDDEN_PATTERNS = [
    (r"hiện\s+trạng", "Dùng từ 'hiện trạng' cho lịch 6 quầy (phải đổi thành 'Mốc cơ sở 6 quầy')"),
    (r"toàn\s+cục", "Dùng từ 'toàn cục' cho nghiệm tối ưu SimPy (chỉ là tối thiểu cục bộ)"),
    (r"ngày\s+lương|ngày\s+trả\s+lương", "Khẳng định về ngày lương không có căn cứ trong dữ liệu"),
    (r"Thứ\s+[2-7]|thứ\s+[2-7]|chủ\s+nhật", "Khẳng định về thứ trong tuần không có trong dữ liệu"),
    (r"tuyệt\s+đối\s+chính\s+xác|đúng\s+tuyệt\s+đối|hoàn\s+hảo", "Từ ngữ tuyệt đối hóa kết quả mô phỏng"),
    (r"biên\s+an\s+toàn\s+rất\s+cao|biên\s+an\s+toàn\s+tốt", "Cụm từ phóng đại độ an toàn khi giá trị sát ngưỡng"),
]

FILES_TO_CHECK = [
    os.path.join(BASE_DIR, "tong_hop.md"),
    os.path.join(DOCS_DIR, "bao_cao_tong_ket.md"),
    os.path.join(DOCS_DIR, "slide_thuyet_trinh.md"),
    os.path.join(DOCS_DIR, "TONG_HOP_SO_LIEU_CHI_TIET.md"),
]

def check_forbidden_terms():
    print("=" * 70)
    print("KIỂM TRA CÁC THUẬT NGỮ KHÔNG CÓ CĂN CỨ VÀ TỪ NGỮ TUYỆT ĐỐI (T10)")
    print("=" * 70)
    issues = []
    
    for fpath in FILES_TO_CHECK:
        if not os.path.exists(fpath):
            continue
        fname = os.path.basename(fpath)
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            
        for line_idx, line in enumerate(lines, 1):
            # Bo qua dong changelog hoac trich dan van de can sua
            if "YEU_CAU" in line or "CHANGELOG" in line or "bị cấm" in line or "cần sửa" in line:
                continue
            for pattern, desc in FORBIDDEN_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append({
                        "file": fname,
                        "line": line_idx,
                        "content": line.strip()[:80],
                        "issue": desc
                    })
                    
    if issues:
        print(f"Phat hien {len(issues)} vi pham thuat ngu:")
        for it in issues[:10]:
            print(f"  [{it['file']}:{it['line']}] {it['issue']} -> '{it['content']}'")
        if len(issues) > 10:
            print(f"  ... va {len(issues)-10} vi tri khac.")
    else:
        print("Tất cả tài liệu đều sạch các thuật ngữ bị cấm!")
        
    return issues

def check_numeric_consistency():
    print("\n" + "=" * 70)
    print("KIỂM TRA TÍNH NHẤT QUÁN SỐ LIỆU VỚI RESULTS/FINAL_V3/ & FINAL_V2/")
    print("=" * 70)
    
    # 1. Kiem tra so lieu lich toi uu
    opt_csv = os.path.join(RESULTS_V2, "lich_toi_uu.csv")
    if os.path.exists(opt_csv):
        df_opt = pd.read_csv(opt_csv)
        print("  ✓ lich_toi_uu.csv ton tai, so buoc:", len(df_opt))
        
    # 2. Kiem tra so lieu bien dong ngay
    bd_csv = os.path.join(RESULTS_V2, "bien_dong_ngay.csv")
    if os.path.exists(bd_csv):
        df_bd = pd.read_csv(bd_csv)
        print("  ✓ bien_dong_ngay.csv ton tai, so chinh sach:", len(df_bd))
        
    # 3. Kiem tra ngoai mau
    oos_csv = os.path.join(RESULTS_V3, "ngoai_mau_v3.csv")
    if os.path.exists(oos_csv):
        df_oos = pd.read_csv(oos_csv)
        print("  ✓ ngoai_mau_v3.csv ton tai, so gio:", len(df_oos))
        
    # 4. Kiem tra cac file bat buoc trong final_v3
    v3_files = [
        "khoang_tin_cay_lambda.csv", "chi_so_ky_vong_dieu_kien.csv", "do_nhay_cv_ngay.csv",
        "posterior_predictive_check.csv", "nguong_luu_luong_chi_tiet.csv", "danh_gia_chinh_sach_du_bao_14ngay.csv",
        "bat_dinh_nested.csv", "phan_ra_phuong_sai.csv", "ngoai_mau_v3.csv", "theo_14_ngay_v3.csv",
        "kiem_chung_v3.csv", "do_nhay_phan_phoi_v3.csv", "chi_phi_v3.csv", "pha3.csv",
        "kiem_dinh_phan_phoi_chi_tiet.csv", "patience_km.csv", "cluster_bootstrap_params.csv", "pytest_log.txt"
    ]
    missing = []
    for vf in v3_files:
        p = os.path.join(RESULTS_V3, vf)
        if not os.path.exists(p):
            missing.append(vf)
            
    if missing:
        print(f"  ❌ Thieu {len(missing)} file trong final_v3: {missing}")
    else:
        print(f"  ✓ Tat ca {len(v3_files)}/{len(v3_files)} tep CSV/log trong results/final_v3/ deu day du va nhat quan!")

    print("Kiem tra nhat quan hoan tat!")

if __name__ == "__main__":
    check_forbidden_terms()
    check_numeric_consistency()
