"""
tools/check_consistency.py: Quet cac tai lieu bao cao va slide de kiem tra:
1. Tinh nhat quan so lieu tong_hop.md voi results/<common.RESULTS_VERSION>/
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
sys.path.insert(0, BASE_DIR)
import common  # noqa: E402

RESULTS = common.RESULTS_DIR

FORBIDDEN_PATTERNS = [
    (r"hiện\s+trạng", "Dùng từ 'hiện trạng' cho lịch 6 quầy (phải đổi thành 'Mốc cơ sở 6 quầy')"),
    (r"toàn\s+cục", "Dùng từ 'toàn cục' cho nghiệm tối ưu SimPy (chỉ là tối thiểu cục bộ)"),
    (r"ngày\s+lương|ngày\s+trả\s+lương", "Khẳng định về ngày lương không có căn cứ trong dữ liệu"),
    (r"Thứ\s+[2-7]|thứ\s+[2-7]|chủ\s+nhật", "Khẳng định về thứ trong tuần không có trong dữ liệu"),
    (r"tuyệt\s+đối\s+chính\s+xác|đúng\s+tuyệt\s+đối|hoàn\s+hảo", "Từ ngữ tuyệt đối hóa kết quả mô phỏng"),
    (r"biên\s+an\s+toàn\s+rất\s+cao|biên\s+an\s+toàn\s+tốt", "Cụm từ phóng đại độ an toàn khi giá trị sát ngưỡng"),
    (r"file:///", "Link tuyệt đối tới máy cá nhân (dùng đường dẫn tương đối)"),
]

# Tai lieu hien hanh: tong_hop.md, README.md va docs/*.md (tru docs/lich_su/ va ke hoach trich dan trang thai cu)
EXCLUDED_DOCS = {"KE_HOACH_CAI_TIEN.md"}
FILES_TO_CHECK = [os.path.join(BASE_DIR, "tong_hop.md"), os.path.join(BASE_DIR, "README.md")] + sorted(
    os.path.join(DOCS_DIR, f) for f in os.listdir(DOCS_DIR) if f.endswith(".md") and f not in EXCLUDED_DOCS
)

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
    print(f"KIỂM TRA TÍNH NHẤT QUÁN SỐ LIỆU VỚI results/{common.RESULTS_VERSION}/")
    print("=" * 70)

    # 1. Kiem tra cac file bat buoc
    required = [
        "khoang_tin_cay_lambda.csv", "kiem_dinh_poisson.csv", "bang_sipp.csv", "chi_so_ky_vong_dieu_kien.csv",
        "do_nhay_cv_ngay.csv", "posterior_predictive_check.csv", "nguong_luu_luong_chi_tiet.csv",
        "danh_gia_chinh_sach_du_bao_14ngay.csv", "bat_dinh_nested.csv", "phan_ra_phuong_sai.csv",
        "ngoai_mau.csv", "theo_14_ngay.csv", "kiem_chung.csv", "do_nhay.csv", "do_nhay_phan_phoi.csv",
        "chi_phi.csv", "pha3.csv", "kiem_dinh_phan_phoi_chi_tiet.csv", "patience_km.csv",
        "cluster_bootstrap_params.csv", "so_sanh_chinh_sach.csv", "do_nhay_kien_nhan.csv",
        "toi_uu_rang_buoc_bo_ve.csv", "gio_te_nhat.csv", "doi_chieu_v4_v5.csv", "params.json", "pytest_log.txt",
        "toi_uu_theo_ca.csv", "toi_uu_theo_ca_top.csv", "toi_uu_xac_suat_ngay.csv", "chinh_sach_tang_quay.csv",
    ]
    missing = [f for f in required if not os.path.exists(os.path.join(RESULTS, f))]
    if missing:
        print(f"  ❌ Thieu {len(missing)} file trong {common.RESULTS_VERSION}: {missing}")
        return [f"thieu file {m}" for m in missing]
    print(f"  ✓ Du {len(required)}/{len(required)} tep trong results/{common.RESULTS_VERSION}/")

    # 2. Doi chieu tung con so trong cac bang chinh cua tong_hop.md
    md = open(os.path.join(BASE_DIR, "tong_hop.md"), encoding="utf-8").read()
    checker = TableChecker(md)
    for check in (check_decision_table, check_data_summary, check_lambda_table, check_erlang_table,
                  check_distribution_fits, check_verification, check_policy_table, check_cv_sensitivity,
                  check_fourteen_days, check_out_of_sample, check_sensitivity, check_service_dist,
                  check_cost_table, check_phase3, check_patience, check_abandon_constraint):
        try:
            check(checker)
        except (KeyError, ValueError, IndexError) as e:
            checker.errors.append(f"{check.__name__}: {e}")

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
    k = pd.read_csv(os.path.join(RESULTS, "khoang_tin_cay_lambda.csv"))
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
    with open(os.path.join(RESULTS, "params.json"), encoding="utf-8") as f:
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


def _csv(name: str) -> pd.DataFrame:
    return pd.read_csv(os.path.join(RESULTS, name))


# Ten chinh sach trong CSV V4
OPT, ROB, BASE = "Toi uu", "Ben vung (+10%)", "Moc co so 6 quay"


def _same_hour(cell: str, label: str) -> bool:
    return cell.replace(" ", "").replace("*", "").startswith(label.replace(" ", ""))


def check_decision_table(ck: TableChecker):
    h = "## 1."
    pol = _csv("so_sanh_chinh_sach.csv").set_index("chinh_sach")
    ce = _csv("chi_so_ky_vong_dieu_kien.csv").set_index("chinh_sach")
    names = ["Toi uu mo phong", "Ben vung (+10% nhu cau)", "Moc co so 6 quay"]
    ce_names = [OPT, ROB, BASE]
    rows = {
        "Tổng số quầy-giờ mở": lambda r: [(0, r["quay_gio"])],
        "danh định": lambda r: [(0, r["sl_toan_ngay"] * 100), (1, r["sl_ci_half"] * 100)],
        "giờ tệ nhất (Low CI95)": lambda r: [(0, r["sl_gio_te_nhat_low"] * 100)],
        "Khách VIP": lambda r: [(0, r["sl_vip"] * 100)],
        "Thời gian chờ trung bình": lambda r: [(0, r["wq_phut"]), (1, r["wq_ci_half"])],
        "bỏ về trung bình": lambda r: [(0, r["ti_le_bo_ve"] * 100), (1, r["ti_le_bo_ve_ci_half"] * 100)],
        "Hiệu suất sử dụng quầy": lambda r: [(0, r["hieu_suat_rho"] * 100), (1, r["rho_ci_half"] * 100)],
    }
    for key, f in rows.items():
        cells = ck.row(h, key)
        for col, name in enumerate(names, 1):
            for idx, val in f(pol.loc[name]):
                ck.expect(f"1 {key} ({name})", cells[col], val, idx)
    # Cot Wilson: so thu 0 = diem uoc luong, 2-3 = khoang (so thu 1 la "95" trong "Wilson 95%")
    wil = {
        "kỳ vọng ngày": ("P_SL_ky_vong_ngay_ge90", "P_SL_ky_vong_ngay_low95", "P_SL_ky_vong_ngay_high95"),
        "min_h": ("P_min_h_Eh_ge90", "P_min_h_Eh_low95", "P_min_h_Eh_high95"),
        "thực tế mọi giờ": ("P_thuc_te_moi_gio_ge90", "P_thuc_te_moi_gio_low95", "P_thuc_te_moi_gio_high95"),
        "gộp tháng": ("P_thang_20ngay_moi_gio_ge90", "P_thang_20ngay_low95", "P_thang_20ngay_high95"),
    }
    for key, cols in wil.items():
        cells = ck.row(h, key)
        for col, name in enumerate(ce_names, 1):
            r = ce.loc[name]
            for idx, c in zip((0, 2, 3), cols):
                ck.expect(f"1 {key} ({name})", cells[col], r[c] * 100, idx)
            if key == "min_h":
                ck.expect(f"1 so gio E_h<90 ({name})", cells[col], r["so_gio_Eh_duoi_90_TB"], 5)


def check_distribution_fits(ck: TableChecker):
    d = _csv("kiem_dinh_phan_phoi_chi_tiet.csv").dropna(subset=["log_likelihood"])
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
    k = _csv("kiem_chung.csv")
    rows = ck.rows("### 3.1")[1:]
    if len(rows) != len(k):
        ck.errors.append(f"3.1: tai lieu co {len(rows)} dong, kiem_chung.csv co {len(k)} dong")
    for (_, r), cells in zip(k.iterrows(), rows):
        lab = f"3.1 {r['kiem_chung']} {r['chi_so']}"
        ck.expect(lab + " ly thuyet", cells[2], r["ly_thuyet"])
        ck.expect(lab + " mo phong", cells[3], r["mo_phong"])
        ck.expect(lab + " n_reps", cells[4], r["n_reps"])
        ck.expect(lab + " t_crit", cells[5], r["t_critical"])
        ck.expect(lab + " CI hw", cells[6], float(str(r["ci95"]).lstrip("±")))
        ck.expect(lab + " sai lech", cells[7], float(str(r["sai_lech_pct"]).rstrip("%")))


def check_policy_table(ck: TableChecker):
    p = _csv("so_sanh_chinh_sach.csv")
    keys = {"Mốc cơ sở 6 quầy": "Moc co so 6 quay", "SIPP (Erlang C)": "SIPP (Erlang C)",
            "SIPP (Erlang-A)": "SIPP (Erlang-A)", "Tối ưu mô phỏng": "Toi uu mo phong",
            "Bền vững": "Ben vung (+10% nhu cau)", "Theo ca 8h": "Theo ca 8h (MILP)"}
    for key, name in keys.items():
        r = p[p["chinh_sach"] == name].iloc[0]
        cells = ck.row("### 4.1", key)
        lab = f"4.1 {name}"
        ck.n_checked += 1
        if cells[1].strip("` ") != r["lich_quay"]:
            ck.errors.append(f"{lab}: lich tai lieu {cells[1]} khac CSV {r['lich_quay']}")
        ck.expect(lab + " quay_gio", cells[2], r["quay_gio"])
        ck.expect(lab + " SL", cells[3], r["sl_toan_ngay"])
        ck.expect(lab + " SL ci", cells[3], r["sl_ci_half"], 1)
        ck.expect(lab + " low", cells[4], r["sl_gio_te_nhat_low"])
        ck.expect(lab + " gio te nhat", cells[4], r["gio_te_nhat"], 1)
        ck.expect(lab + " vip", cells[5], r["sl_vip"])
        ck.expect(lab + " p_ab", cells[6], r["ti_le_bo_ve"] * 100)
        ck.expect(lab + " p_ab ci", cells[6], r["ti_le_bo_ve_ci_half"] * 100, 1)
        ck.expect(lab + " wq", cells[7], r["wq_phut"])
        ck.expect(lab + " wq ci", cells[7], r["wq_ci_half"], 1)
        ck.expect(lab + " rho", cells[8], r["hieu_suat_rho"] * 100)
        ck.expect(lab + " rho ci", cells[8], r["rho_ci_half"] * 100, 1)


def check_cv_sensitivity(ck: TableChecker):
    a = _csv("chi_so_ky_vong_dieu_kien.csv")
    d = _csv("do_nhay_cv_ngay.csv")
    names = {"Lịch 45": OPT, "Lịch 48": ROB, "Mốc 54": BASE}
    cols = [("P_SL_ky_vong_ngay_ge90", "P_SL_ky_vong_ngay_low95", "P_SL_ky_vong_ngay_high95"),
            ("P_min_h_Eh_ge90", "P_min_h_Eh_low95", "P_min_h_Eh_high95"),
            ("so_gio_Eh_duoi_90_TB",),
            ("P_thuc_te_moi_gio_ge90", "P_thuc_te_moi_gio_low95", "P_thuc_te_moi_gio_high95"),
            ("P_thang_20ngay_moi_gio_ge90", "P_thang_20ngay_low95", "P_thang_20ngay_high95")]
    policy = None
    for cells in ck.rows("### 4.2")[1:]:
        for label, key in names.items():
            if label in cells[0]:
                policy = key
        if "Chuẩn" in cells[1]:
            match = a[a["chinh_sach"] == policy]
        else:
            cv = float(ck.num(cells[1])) / 100
            match = d[(d["chinh_sach"] == policy) & ((d["cv_day"] - cv).abs() < 1e-6)]
        if match.empty:
            ck.errors.append(f"4.2 {policy} '{cells[1]}': khong co dong tuong ung trong CSV")
            continue
        r = match.iloc[0]
        lab = f"4.2 {policy} CV={r['cv_day']:.4f}"
        ck.expect(lab + " CV", cells[1], r["cv_day"] * 100)
        for i, group in enumerate(cols):
            for idx, col in enumerate(group):
                scale = 1 if col == "so_gio_Eh_duoi_90_TB" else 100
                ck.expect(f"{lab} {col}", cells[2 + i], r[col] * scale, idx)


def check_fourteen_days(ck: TableChecker):
    t = _csv("theo_14_ngay.csv")
    rows = [c for c in ck.rows("### 4.5") if c[0].isdigit()]
    for (_, r), cells in zip(t.iterrows(), rows):
        lab = f"4.5 ngay {r['ngay']}"
        ck.expect(lab + " tong khach", cells[2], r["tong_khach"])
        for col, name in ((3, OPT), (6, ROB), (9, BASE)):
            ck.expect(f"{lab} SL {name}", cells[col], r[f"SL_{name}"])
            ck.n_checked += 1
            dat = "Đạt" in cells[col + (2 if col < 9 else 1)]
            if dat != (r[f"Dat_SLA_{name}"] == "Dat"):
                ck.errors.append(f"{lab} {name}: nhan Dat/Hut khong khop CSV")
            if col < 9:
                ck.expect(f"{lab} CI low {name}", cells[col + 1], r[f"CI95_low_{name}"], 0)
                ck.expect(f"{lab} CI high {name}", cells[col + 1], r[f"CI95_high_{name}"], 1)
    s = _csv("theo_14_ngay_tong_hop.csv").set_index("chinh_sach")
    tot = ck.row("### 4.5", "Tổng kết")
    for col, name in ((3, OPT), (6, ROB), (9, BASE)):
        ck.expect(f"4.5 tong ket {name}", tot[col], s.loc[name, "so_ngay_dat"])


def check_out_of_sample(ck: TableChecker):
    o = _csv("ngoai_mau.csv")
    rows = [c for c in ck.rows("## 5.") if "h -" in c[0]]
    for (_, r), cells in zip(o.iterrows(), rows):
        lab = f"5 {r['khung_gio']}"
        ck.n_checked += 1
        if not _same_hour(cells[0], r["khung_gio"]):
            ck.errors.append(f"{lab}: thu tu dong khong khop ({cells[0]})")
        ck.expect(lab + " quay", cells[1], r["so_quay"])
        ck.expect(lab + " SL mo phong", cells[2], r["SL_mo_phong_TB"])
        ck.expect(lab + " PI low", cells[3], r["PI95_low"])
        ck.expect(lab + " PI high", cells[4], r["PI95_high"])
        ck.expect(lab + " SL thuc te", cells[5], r["SL_thuc_te"])
        ck.expect(lab + " Wilson low", cells[6], r["SL_thuc_te_Wilson_low"], 0)
        ck.expect(lab + " Wilson high", cells[6], r["SL_thuc_te_Wilson_high"], 1)
        ck.expect(lab + " Holm", cells[8], r["adj_p_value_Holm"])
        ck.n_checked += 2
        if ("Có" in cells[7]) != (r["trong_PI95"] == "Co"):
            ck.errors.append(f"{lab}: nhan trong PI95 khong khop CSV")
        if cells[9].strip("* ").startswith("Có") != (r["lech_co_y_nghia"] == "Co"):
            ck.errors.append(f"{lab}: nhan khac biet co y nghia khong khop CSV")


def check_sensitivity(ck: TableChecker):
    d = _csv("do_nhay.csv")
    groups = {"Nhu cầu": "Nhu cau", "Thời gian phục vụ": "E[S]", "Tốc độ bỏ về": "Theta"}
    group = None
    for cells in ck.rows("### 7.1")[1:]:
        for label, key in groups.items():
            if label in cells[0]:
                group = key
        f = float(ck.num(cells[1]))
        sub = d[(d["nhom_yeu_to"] == group) & ((d["he_so"] - f).abs() < 1e-9)].set_index("chinh_sach")
        lab = f"7.1 {group} x{f}"
        for col, name, field in ((2, OPT, "sl_toan_ngay"), (3, OPT, "sl_gio_te_nhat_low"),
                                 (4, ROB, "sl_toan_ngay"), (5, ROB, "sl_gio_te_nhat_low"),
                                 (6, BASE, "sl_toan_ngay")):
            if cells[col].strip() == "-":
                continue
            ck.expect(f"{lab} {name} {field}", cells[col], sub.loc[name, field])


def check_service_dist(ck: TableChecker):
    d = _csv("do_nhay_phan_phoi.csv")
    keys = {"Thực nghiệm": "Thuc nghiem", "Gamma": "Gamma", "Exponential": "Exponential", "Lognormal": "Lognormal"}
    for key, prefix in keys.items():
        r = d[d["phan_phoi"].str.startswith(prefix)].iloc[0]
        cells = ck.row("### 7.2", key)
        lab = f"7.2 {r['phan_phoi']}"
        ck.expect(lab + " SL", cells[1], r["SL_toan_ngay"])
        ck.expect(lab + " SL ci", cells[1], r["SL_ci_half"], 1)
        ck.n_checked += 1
        if not _same_hour(cells[2], r["gio_te_nhat"]):
            ck.errors.append(f"{lab}: gio te nhat tai lieu '{cells[2]}', CSV '{r['gio_te_nhat']}'")
        ck.expect(lab + " SL gio te nhat", cells[3], r["SL_gio_te_nhat"])
        ck.expect(lab + " low", cells[4], r["SL_gio_te_nhat_low95"])
        if r["khac_biet_co_y_nghia"] != "-":
            ck.expect(lab + " hieu so", cells[5], r["hieu_so_vs_thuc_nghiem"])
            ck.expect(lab + " CI low", cells[6], r["CI95_hieu_so_low"], 0)
            ck.expect(lab + " CI high", cells[6], r["CI95_hieu_so_high"], 1)
            ck.n_checked += 1
            if cells[7].strip("* ").startswith("Có") != (r["khac_biet_co_y_nghia"] == "Co"):
                ck.errors.append(f"{lab}: nhan co y nghia khong khop CSV")


def check_cost_table(ck: TableChecker):
    c = _csv("chi_phi.csv")
    labels = {OPT: "45", ROB: "48", BASE: "6 quầy"}
    rows = [x for x in ck.rows("### 7.3") if "k =" in x[0]]
    for (_, r), cells in zip(c.iterrows(), rows):
        lab = f"7.3 k={r['k_he_so_mat_khach']}"
        ck.expect(lab + " k", cells[0], r["k_he_so_mat_khach"])
        for col, name in ((1, OPT), (2, ROB), (3, BASE)):
            ck.expect(f"{lab} C {name}", cells[col], r[f"Chi_phi_{name}"])
            ck.expect(f"{lab} CI {name}", cells[col], r[f"CI95_half_{name}"], 1)
        ck.expect(lab + " hieu so", cells[4], r[f"Hieu_so_{OPT}_tru_{ROB}"])
        ck.expect(lab + " CI low", cells[5], r["CI95_hieu_so_low"], 0)
        ck.expect(lab + " CI high", cells[5], r["CI95_hieu_so_high"], 1)
        ck.n_checked += 1
        if labels[r["Chinh_sach_kinh_te_nhat"]] not in cells[7]:
            ck.errors.append(f"{lab}: chinh sach re nhat theo CSV la {r['Chinh_sach_kinh_te_nhat']}, tai lieu ghi '{cells[7]}'")


def check_phase3(ck: TableChecker):
    p = _csv("pha3.csv")
    sec = ck.section("### 7.4")
    counts = p["loai_thu_nghiem"].value_counts()
    for n, phrase in ((len(p), "cấu hình"), (counts.get("Swap 1 quay", 0), "phép hoán đổi"),
                      (counts.get("Giam 2 quay", 0), "phép giảm 2 quầy")):
        ck.n_checked += 1
        if not re.search(rf"\b{n}\b[^\n]{{0,15}}{phrase}", sec):
            ck.errors.append(f"7.4: khong tim thay '{n} {phrase}' (pha3.csv)")
    ck.n_checked += 1
    n_fea = int((p["kha_thi"] == "Y").sum())
    if f"{n_fea}/{len(p)}" not in sec:
        ck.errors.append(f"7.4: so cau hinh kha thi theo pha3.csv la {n_fea}/{len(p)}")


def check_patience(ck: TableChecker):
    k = _csv("do_nhay_kien_nhan.csv")
    rows = ck.rows("### 7.5")[1:]
    if len(rows) != len(k):
        ck.errors.append(f"7.5: tai lieu co {len(rows)} dong, do_nhay_kien_nhan.csv co {len(k)} dong")
    for (_, r), cells in zip(k.iterrows(), rows):
        lab = f"7.5 {r['chinh_sach']}"
        ck.expect(lab + " theta", cells[1], r["theta"])
        ck.n_checked += 1
        if cells[2].strip("` ") != r["lich_quay"]:
            ck.errors.append(f"{lab}: lich tai lieu {cells[2]} khac CSV {r['lich_quay']}")
        ck.expect(lab + " quay_gio", cells[3], r["quay_gio"])
        ck.expect(lab + " quay_gio SIPP", cells[4], r["quay_gio_sipp"])
        ck.expect(lab + " SL", cells[5], r["sl_toan_ngay"])
        ck.expect(lab + " low", cells[6], r["sl_gio_te_nhat_low"])
        ck.expect(lab + " p_ab", cells[7], r["ti_le_bo_ve"] * 100)
        ck.expect(lab + " wq", cells[8], r["wq_phut"])


def check_abandon_constraint(ck: TableChecker):
    t = _csv("toi_uu_rang_buoc_bo_ve.csv")
    rows = ck.rows("### 7.6")[1:]
    for (_, r), cells in zip(t.iterrows(), rows):
        lab = f"7.6 {r['chinh_sach']}"
        ck.n_checked += 1
        if cells[1].strip("` ") != r["lich_quay"]:
            ck.errors.append(f"{lab}: lich tai lieu {cells[1]} khac CSV {r['lich_quay']}")
        ck.expect(lab + " quay_gio", cells[2], r["quay_gio"])
        ck.expect(lab + " SL", cells[3], r["sl_toan_ngay"])
        ck.expect(lab + " low", cells[4], r["sl_gio_te_nhat_low"])
        ck.expect(lab + " p_ab", cells[5], r["ti_le_bo_ve"] * 100)
        ck.expect(lab + " wq", cells[6], r["wq_phut"])


# =============================================================================
# DOI CHIEU SO TRONG BAO CAO, SLIDE, README (T2)
# =============================================================================

REPORT_FILES = {
    "bao_cao_tong_ket.md": os.path.join(DOCS_DIR, "bao_cao_tong_ket.md"),
    "slide_thuyet_trinh.md": os.path.join(DOCS_DIR, "slide_thuyet_trinh.md"),
    "README.md": os.path.join(BASE_DIR, "README.md"),
}
# Chinh sach xuat hien trong bang tom tat cua slide va README
SUMMARY_POLICIES = ["Moc co so 6 quay", "SIPP (Erlang C)", "SIPP (Erlang-A)", "Toi uu mo phong", "Ben vung (+10% nhu cau)"]


def _expected_report_strings() -> dict:
    """Moi tai lieu -> danh sach (nhan, chuoi phai xuat hien), sinh tu CSV theo dung dinh dang hien thi."""
    pol = _csv("so_sanh_chinh_sach.csv").set_index("chinh_sach")
    bc, sl, rd = [], [], []
    for name, r in pol.iterrows():
        lab = f"9.2 {name}"
        bc += [(lab + " SL", f"{r.sl_toan_ngay:.4f} ± {r.sl_ci_half:.4f}"),
               (lab + " gio te nhat", f"{r.sl_gio_te_nhat_low:.4f}"),
               (lab + " VIP", f"{r.sl_vip:.4f}"),
               (lab + " bo ve", f"{r.ti_le_bo_ve * 100:.2f}%"),
               (lab + " Wq", f"{r.wq_phut:.4f}"),
               (lab + " rho", f"{r.hieu_suat_rho * 100:.2f}%")]
    for name in SUMMARY_POLICIES:
        r = pol.loc[name]
        sl += [(f"slide 9 {name} SL", f"{r.sl_toan_ngay * 100:.2f}%"),
               (f"slide 9 {name} gio te nhat", f"{r.sl_gio_te_nhat_low * 100:.2f}%")]
        rd += [(f"README 15.3 {name} SL", f"{r.sl_toan_ngay:.3f}".replace(".", ",")),
               (f"README 15.3 {name} gio te nhat", f"{r.sl_gio_te_nhat_low:.3f}".replace(".", ","))]
    for _, r in _csv("kiem_chung.csv").iterrows():
        bc += [(f"8 {r.kiem_chung} {r.chi_so}", f"{r.mo_phong:.4f} | {r.ci95}")]
    for _, r in _csv("bang_sipp.csv").iterrows():
        bc += [(f"6.1 {r.khung_gio}", f"| {r.c_erlang_c} | {r.sl_erlang_c * 100:.1f}% | {r.c_erlang_a} | "
                                     f"{r.sl_erlang_a * 100:.1f}% | {r.p_ab_erlang_a * 100:.1f}% |")]
    for _, r in _csv("chi_phi.csv").iterrows():
        lab = f"6.2 k={r.k_he_so_mat_khach}"
        for c in (OPT, ROB, BASE):
            bc += [(f"{lab} {c}", f"{r['Chi_phi_' + c]:.2f} ± {r['CI95_half_' + c]:.2f}")]
        d = r[f"Hieu_so_{OPT}_tru_{ROB}"]
        bc += [(lab + " hieu so", f"{d:+.2f} [{r.CI95_hieu_so_low:+.2f}, {r.CI95_hieu_so_high:+.2f}]".lstrip("+"))]
    for _, r in _csv("do_nhay.csv").iterrows():
        bc += [(f"9.4 {r.nhom_yeu_to} x{r.he_so} {r.chinh_sach}", f"{r.sl_gio_te_nhat_low:.4f}")]
    for _, r in _csv("lich_ben_vung_delta.csv").iterrows():
        bc += [(f"6.4 delta={r.delta_du_phong}", f"`{r.lich_quay}`")]
    for _, r in _csv("lich_theo_ca.csv").dropna().iterrows():
        bc += [(f"6.3 {r.truong_hop}", f"`{r.phu_quay}`")]
    return {"bao_cao_tong_ket.md": bc, "slide_thuyet_trinh.md": sl, "README.md": rd}


def check_report_numbers(texts: dict = None) -> list:
    """
    T2: doi chieu so trong bao cao tong ket, slide va README voi CSV nguon.
    texts: {ten tep: noi dung} de kiem tra van ban tuy y (test); mac dinh doc tu dia.
    Chuan hoa dau tru Unicode '−' thanh '-' truoc khi so.
    """
    print("\n" + "=" * 70)
    print("ĐỐI CHIẾU SỐ TRONG BÁO CÁO, SLIDE, README (T2)")
    print("=" * 70)
    if texts is None:
        texts = {k: open(p, encoding="utf-8").read() for k, p in REPORT_FILES.items()}
    errors, n = [], 0
    for fname, items in _expected_report_strings().items():
        text = texts[fname].replace("−", "-")
        for label, needle in items:
            n += 1
            if needle not in text:
                errors.append(f"{fname} [{label}]: khong tim thay '{needle}'")
    print(f"  Da doi chieu {n} gia tri trong {len(texts)} tai lieu")
    if errors:
        print(f"  ❌ {len(errors)} gia tri KHONG khop nguon:")
        for e in errors:
            print("     -", e)
    else:
        print("  ✓ Tat ca gia tri da doi chieu deu khop du lieu nguon")
    return errors


if __name__ == "__main__":
    term_issues = check_forbidden_terms()
    num_issues = check_numeric_consistency()
    report_issues = check_report_numbers()
    sys.exit(1 if (term_issues or num_issues or report_issues) else 0)
