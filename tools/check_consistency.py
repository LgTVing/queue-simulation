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
    
    # 1. Kiem tra cac file bat buoc trong final_v3
    v3_files = [
        "khoang_tin_cay_lambda.csv", "chi_so_ky_vong_dieu_kien.csv", "do_nhay_cv_ngay.csv",
        "posterior_predictive_check.csv", "nguong_luu_luong_chi_tiet.csv", "danh_gia_chinh_sach_du_bao_14ngay.csv",
        "bat_dinh_nested.csv", "phan_ra_phuong_sai.csv", "ngoai_mau_v3.csv", "theo_14_ngay_v3.csv",
        "kiem_chung_v3.csv", "do_nhay_phan_phoi_v3.csv", "chi_phi_v3.csv", "pha3.csv",
        "kiem_dinh_phan_phoi_chi_tiet.csv", "patience_km.csv", "cluster_bootstrap_params.csv", "pytest_log.txt"
    ]
    missing = [vf for vf in v3_files if not os.path.exists(os.path.join(RESULTS_V3, vf))]
    if missing:
        print(f"  ❌ Thieu {len(missing)} file trong final_v3: {missing}")
        return [f"thieu file {m}" for m in missing]
    print(f"  ✓ Du {len(v3_files)}/{len(v3_files)} tep CSV/log trong results/final_v3/")

    # 2. Doi chieu tung con so trong cac bang chinh cua tong_hop.md
    md = open(os.path.join(BASE_DIR, "tong_hop.md"), encoding="utf-8").read()
    checker = TableChecker(md)
    for check in (check_data_summary, check_lambda_table, check_erlang_table, check_distribution_fits,
                  check_verification, check_cv_sensitivity, check_cost_table, check_phase3):
        check(checker)

    n_err = len(checker.errors)
    print(f"  Da doi chieu {checker.n_checked} gia tri trong tong_hop.md")
    if n_err:
        print(f"  ❌ {n_err} gia tri KHONG khop nguon:")
        for e in checker.errors:
            print("     -", e)
    else:
        print("  ✓ Tat ca gia tri da doi chieu deu khop du lieu nguon")
    return checker.errors


# =============================================================================
# DOI CHIEU BANG MARKDOWN VOI DU LIEU NGUON
# =============================================================================

NUM_RE = re.compile(r"[-+]?\d+(?:\.\d+)?")


class TableChecker:
    """Tach bang Markdown theo muc va so sanh so hien thi voi gia tri tinh tu nguon."""

    def __init__(self, md: str):
        self.md = md
        self.errors = []
        self.n_checked = 0

    def section(self, heading: str) -> str:
        start = self.md.index(heading)
        nxt = [p for p in (self.md.find("\n### ", start + 1), self.md.find("\n## ", start + 1)) if p != -1]
        return self.md[start:min(nxt) if nxt else len(self.md)]

    def rows(self, heading: str):
        out = []
        for line in self.section(heading).splitlines():
            if line.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", line):
                out.append([c.strip() for c in line.strip().strip("|").split("|")])
        return out

    def row(self, heading: str, key: str):
        for cells in self.rows(heading):
            if key in cells[0]:
                return cells
        raise KeyError(f"{heading}: khong tim thay dong '{key}'")

    def num(self, cell: str, idx: int = 0):
        nums = NUM_RE.findall(cell.replace(",", ""))
        return nums[idx] if len(nums) > idx else None

    def expect(self, label: str, cell: str, expected: float, idx: int = 0):
        """So sanh so thu idx trong o voi expected, dung sai theo so chu so thap phan hien thi."""
        self.n_checked += 1
        shown = self.num(cell, idx)
        if shown is None:
            self.errors.append(f"{label}: khong doc duoc so trong '{cell}'")
            return
        dec = len(shown.split(".")[1]) if "." in shown else 0
        tol = 0.51 * 10 ** (-dec) + 1e-9
        if abs(float(shown) - expected) > tol:
            self.errors.append(f"{label}: tai lieu = {shown}, nguon = {expected:.{dec + 1}f}")


def _load_data():
    df = pd.read_csv(os.path.join(BASE_DIR, "data", "clean", "data_clean.csv"))
    return df, df[df["day"] < 10], df[df["day"] >= 10]


def check_data_summary(ck: TableChecker):
    h = "### 2.1"
    df, tr, te = _load_data()
    for col, d in ((1, tr), (2, te), (3, df)):
        svc = d.loc[d["served"] == 1, "svc"].dropna()
        theta = (d["served"] == 0).sum() / d["wait"].sum()
        vals = {
            "Thời gian phục vụ TB": svc.mean(),
            "Độ lệch chuẩn thời gian phục vụ": svc.std(ddof=1),
            "Hệ số biến thiên": svc.std(ddof=1) / svc.mean(),
            "Bình phương hệ số biến thiên": (svc.std(ddof=1) / svc.mean()) ** 2,
            "Tốc độ bỏ về": theta,
            "Tỉ lệ khách hàng ưu tiên": d["vip"].mean() * 100,
            "Thời gian chờ TB quan sát": d["wait"].mean(),
            "Tỉ lệ khách bỏ về quan sát": (d["served"] == 0).mean() * 100,
        }
        for key, v in vals.items():
            ck.expect(f"2.1 {key} (cot {col})", ck.row(h, key)[col], v)


def check_lambda_table(ck: TableChecker):
    k = pd.read_csv(os.path.join(RESULTS_V3, "khoang_tin_cay_lambda.csv"))
    for _, r in k.iterrows():
        cells = ck.row("### 2.2", r["khung_gio"])
        lab = f"2.2 {r['khung_gio']}"
        ck.expect(lab + " N_bar", cells[2], r["mean_khach_ngay"])
        ck.expect(lab + " Poisson hw", cells[3], r["poisson_hw_ngay"])
        ck.expect(lab + " t hw", cells[4], r["t_hw_ngay"])
        ck.expect(lab + " lambda", cells[6], r["lambda_phut"])
        ck.expect(lab + " CI low", cells[7], r["lambda_low_ci95"])
        ck.expect(lab + " CI high", cells[8], r["lambda_high_ci95"])


def check_erlang_table(ck: TableChecker):
    import json
    sys.path.insert(0, BASE_DIR)
    import b_theory as bt
    with open(os.path.join(RESULTS_V3, "params.json"), encoding="utf-8") as f:
        prm = json.load(f)
    mu, theta = 1.0 / prm["service"]["mean"], prm["theta"]
    rows = [c for c in ck.rows("### 2.4") if "h -" in c[0]]
    for h, (lam, cells) in enumerate(zip(prm["rates_per_min"], rows)):
        c_c = bt.sipp_schedule([lam], mu, theta, use_erlang_a=False)[0]
        c_a = bt.sipp_schedule([lam], mu, theta)[0]
        res_a = bt.erlang_a(lam, mu, theta, c_a)
        lab = f"2.4 gio {h}"
        ck.expect(lab + " lambda", cells[1], lam)
        ck.expect(lab + " c ErlangC", cells[3], c_c)
        ck.expect(lab + " SL ErlangC", cells[4], bt.mmc(lam, mu, c_c)["P_sla"] * 100)
        ck.expect(lab + " c ErlangA", cells[5], c_a)
        ck.expect(lab + " SL ErlangA", cells[6], res_a["SL"] * 100)
        ck.expect(lab + " p_ab ErlangA", cells[7], res_a["p_ab"] * 100)


def check_distribution_fits(ck: TableChecker):
    d = pd.read_csv(os.path.join(RESULTS_V3, "kiem_dinh_phan_phoi_chi_tiet.csv"))
    for _, r in d.iterrows():
        cells = ck.row("### 2.5", r["phan_phoi"])
        lab = f"2.5 {r['phan_phoi']}"
        ck.expect(lab + " LL", cells[2], r["log_likelihood"])
        ck.expect(lab + " AIC", cells[3], r["AIC"])
        ck.expect(lab + " BIC", cells[4], r["BIC"])
        ck.expect(lab + " KS", cells[5], r["KS_stat"])
        ck.n_checked += 1
        if r["KS_pvalue_boot"] < 0.05 and "bác bỏ" not in cells[7]:
            ck.errors.append(f"{lab}: p_boot = {r['KS_pvalue_boot']} nhung tai lieu khong ghi 'bị bác bỏ'")


def check_verification(ck: TableChecker):
    k = pd.read_csv(os.path.join(RESULTS_V3, "kiem_chung_v3.csv"))
    rows = ck.rows("### 3.1")[1:]
    for (_, r), cells in zip(k.iterrows(), rows):
        lab = f"3.1 {r['kiem_chung']} {r['chi_so']}"
        ck.expect(lab + " ly thuyet", cells[2], r["ly_thuyet"])
        ck.expect(lab + " mo phong", cells[3], r["mo_phong"])
        ck.expect(lab + " n_reps", cells[4], r["n_reps"])
        ck.expect(lab + " t_crit", cells[5], r["t_critical"])
        ck.expect(lab + " CI hw", cells[6], r["nua_khoang_tin_cay_95"])


def check_cv_sensitivity(ck: TableChecker):
    a = pd.read_csv(os.path.join(RESULTS_V3, "chi_so_ky_vong_dieu_kien.csv"))
    d = pd.read_csv(os.path.join(RESULTS_V3, "do_nhay_cv_ngay.csv"))
    names = {"Lịch 44": "Toi_uu_44", "Lịch 48": "Ben_vung_48", "Mốc 54": "Moc_co_so_54"}
    cols = ["P_SL_ky_vong_ngay_ge90", "P_min_h_Eh_ge90", "so_gio_Eh_duoi_90_TB",
            "P_thuc_te_moi_gio_ge90", "P_thang_20ngay_moi_gio_ge90"]
    policy = None
    for cells in ck.rows("### 4.2")[1:]:
        for label, key in names.items():
            if label in cells[0]:
                policy = key
        cv = float(ck.num(cells[1])) / 100
        src = a if "Chuẩn" in cells[1] else d
        match = src[(src["chinh_sach"] == policy) & ((src["cv_day"] - cv).abs() < 1e-6)]
        if match.empty:
            ck.errors.append(f"4.2 {policy} CV={cv}: khong co dong tuong ung trong CSV")
            continue
        r = match.iloc[0]
        for i, col in enumerate(cols):
            scale = 1 if col == "so_gio_Eh_duoi_90_TB" else 100
            ck.expect(f"4.2 {policy} CV={cv} {col}", cells[2 + i], r[col] * scale)


def check_cost_table(ck: TableChecker):
    c = pd.read_csv(os.path.join(RESULTS_V3, "chi_phi_v3.csv"))
    labels = {"Toi_uu_44": "44", "Ben_vung_48": "48", "Moc_co_so_54": "6 quầy"}
    rows = [x for x in ck.rows("### 7.3") if "k =" in x[0]]
    for (_, r), cells in zip(c.iterrows(), rows):
        lab = f"7.3 k={r['k_he_so_mat_khach']}"
        ck.expect(lab + " C44", cells[1], r["Chi_phi_44"])
        ck.expect(lab + " C48", cells[2], r["Chi_phi_48"])
        ck.expect(lab + " C54", cells[3], r["Chi_phi_Moc_6"])
        ck.expect(lab + " C44-C48", cells[4], r["Hieu_so_Cost44_tru_Cost48"])
        ck.n_checked += 1
        best = labels[r["Chinh_sach_kinh_te_nhat"].split(" ")[0]]
        if best not in cells[7]:
            ck.errors.append(f"{lab}: chinh sach re nhat theo CSV la {r['Chinh_sach_kinh_te_nhat']}, tai lieu ghi '{cells[7]}'")


def check_phase3(ck: TableChecker):
    p = pd.read_csv(os.path.join(RESULTS_V3, "pha3.csv"))
    sec = ck.section("### 7.4")
    counts = p["loai_thu_nghiem"].value_counts()
    for n, phrase in ((len(p), "cấu hình"), (counts.get("Swap 1 quay", 0), "phép hoán đổi"),
                      (counts.get("Giam 2 quay", 0), "phép giảm 2 quầy")):
        ck.n_checked += 1
        if not re.search(rf"\b{n}\b[^\n]{{0,15}}{phrase}", sec):
            ck.errors.append(f"7.4: khong tim thay '{n} {phrase}' (pha3.csv)")
    ck.n_checked += 1
    n_fea = int((p["kha_thi_SLA"] == "Y").sum())
    if f"{n_fea}/{len(p)}" not in sec:
        ck.errors.append(f"7.4: so cau hinh kha thi theo pha3.csv la {n_fea}/{len(p)}")


if __name__ == "__main__":
    term_issues = check_forbidden_terms()
    num_issues = check_numeric_consistency()
    sys.exit(1 if (term_issues or num_issues) else 0)
