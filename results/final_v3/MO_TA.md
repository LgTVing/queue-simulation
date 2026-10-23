# MÔ TẢ KẾT QUẢ ĐỢT 2 (FINAL_V3) - THỐNG KÊ VÀ XÁC SUẤT CHUẨN MỰC

- **Ngày chạy:** 23/10/2026
- **Môi trường:** Python 3.13.3, SimPy 4.1.1, SciPy 1.15.2, Pandas 2.2.3, NumPy 2.2.3
- **Version `params.json`:** 3.0 (Cập nhật Student-t CI df=9 cho tập Train: $[0.7280, 1.4883]$ khách/phút; Gamma service shape=0.8320, scale=3.5140, mean=2.9236; theta=0.1087; p_vip=0.3543)
- **Seeds sử dụng:**
  - S1/S10 (Bootstrap phân phối & tham số): `seed=42`, `B=1000`, `10000` resamples
  - S2 (Kỳ vọng có điều kiện): `seed_base=20000`, $K=200$ kịch bản, $R=30$ reps/kịch bản (tổng 18.000 reps)
  - S3 (Độ nhạy CV ngày): `seed_base=50000 + int(cv*100)`, $K=100$, $R=20$ cho $CV \in \{0.08, 0.12, 0.16, 0.20\}$ (tổng 24.000 reps)
  - S3 (Posterior Predictive Check): $B=1000$ bộ 14 ngày mô phỏng
  - S4 (Ngưỡng lưu lượng): $V \in [550, 850]$, $R=40$ reps/mức; Bộ dự báo hồi quy OLS sớm 8h-10h
  - S5 (Nested Bootstrap & ANOVA): $B=50$ bộ tham số resample theo ngày, $R=60$ reps/bộ (tổng 3.000 reps)
  - S6 (Ngoài mẫu Predictive Interval): $K=1000$ bộ 4 ngày tổng hợp (tổng 4.000 reps ngày)
  - S7 (Đối chiếu 14 ngày): 14 ngày thực tế, $R=40$ reps/ngày cho 3 chính sách (tổng 1.680 reps)
  - S8 (M/G/1 Pollaczek-Khinchine): $T=40.000$ phút, warm-up $5.000$ phút, $R=40$ reps ($df=39, t_{crit}=2.0227$)
  - S9 (Độ nhạy phân phối phục vụ): 4 phân phối, $R=150$ reps/phân phối (tổng 600 reps)
  - S11 (Bảng chi phí & hiệu số cặp): $R=150$ reps, $k \in \{0.10, 0.25, 0.50, 1.00, 2.00\}$
  - C6 (Vét cạn Pha 3): 117 cấu hình thử nghiệm (72 swap 1 quầy + 36 double reduction)
  - C7 (Pytest): 22/22 tests passed (log tại `pytest_log.txt`)

---

## Danh mục tệp trong `results/final_v3/`

| Tên tệp | Nhiệm vụ | Mô tả nội dung |
|---|---|---|
| `khoang_tin_cay_lambda.csv` | S1 | Khoảng tin cậy Student-t ($df=13, t=2.1604$) cho $\lambda_h$ dựa trên phương sai mẫu thực tế, so sánh với công thức Poisson |
| `params.json` | S1 | Bộ tham số hệ thống chuẩn v3 kèm Student-t CI cho tập Train ($df=9, t=2.2622$) |
| `chi_so_ky_vong_dieu_kien.csv` | S2 | Chỉ số kỳ vọng có điều kiện $E_h(m)$, $P(E_{day} \ge 90\%)$, $P(\min_h E_h \ge 90\%)$, $P(\text{thực tế})$, $P(\text{tháng 20 ngày})$ kèm Wilson CIs |
| `do_nhay_cv_ngay.csv` | S3 | Đánh giá độ nhạy chỉ số kỳ vọng theo biến động ngày $CV \in \{8\%, 12\%, 16\%, 20\%\}$ |
| `posterior_predictive_check.csv` | S3 | Kiểm tra mức độ phù hợp hậu nghiệm qua 1.000 bộ 14 ngày mô phỏng, so sánh $D_h$ và $D_{total}$ |
| `nguong_luu_luong_chi_tiet.csv` | S4 | Phân tích ngưỡng lưu lượng $V^*$ từ 550 đến 850 khách/ngày cho Lịch 44 và Lịch 48 |
| `danh_gia_chinh_sach_du_bao_14ngay.csv` | S4 | Đánh giá chính sách động dựa trên bộ dự báo 8h-10h trên 14 ngày thực tế, quầy-giờ và mức tiết kiệm |
| `bat_dinh_nested.csv` | S5 | Kết quả mô phỏng 50 bộ bootstrap tham số $\times$ 60 lần lặp/bộ |
| `phan_ra_phuong_sai.csv` | S5 | Phân rã ANOVA phương sai: phương sai tham số (Between: 95.8%) vs nhiễu mô phỏng (Within/R: 4.2%) |
| `ngoai_mau_v3.csv` | S6 | Đối chiếu ngoài mẫu tập Test (ngày 10-13) với Khoảng dự báo 95% (PI95) và kiểm định Holm-Bonferroni |
| `theo_14_ngay_v3.csv` | S7 | Đối chiếu 14 ngày quan sát phân định Train/Test, Student-t CI cho từng ngày và Wilson CI cho tỉ lệ đạt |
| `kiem_chung_v3.csv` | S8 | Bảng kiểm chứng 3 tầng cập nhật Student-t CIs ($df=29, 39, 59$), M/G/1 P-K exact 40k phút |
| `do_nhay_phan_phoi_v3.csv` | S9 | Độ nhạy 4 phân phối phục vụ, giờ tệ nhất và khoảng tin cậy hiệu số theo cặp |
| `kiem_dinh_phan_phoi_chi_tiet.csv` | S10 | AIC, BIC, Log-Likelihood và bootstrap-corrected KS test cho 4 phân phối thời gian phục vụ |
| `patience_km.csv` | S10 | Bảng sống sót Kaplan-Meier cho thời gian kiên nhẫn có kiểm duyệt phải |
| `cluster_bootstrap_params.csv` | S10 | Khoảng tin cậy Cluster Bootstrap theo ngày cho $E[S]$ và $\theta$ |
| `chi_phi_v3.csv` | S11 | Bảng chi phí kinh tế theo hệ số $k$, truyền sai số và khoảng tin cậy hiệu số theo cặp |
| `pha3.csv` | C6 | Nhật ký 117 phép thử vét cạn Pha 3 chứng minh tính tối thiểu cục bộ của Lịch 44 |
| `pytest_log.txt` | C7 | Toàn bộ log kiểm thử đơn vị tự động 22/22 passed |
