# Báo cáo sửa đổi đợt 2: Thống kê và Xác suất Chuẩn mực

Tài liệu báo cáo nghiệm thu kỹ thuật theo đúng cấu trúc chỉ đạo tại Mục 8 của `YEU_CAU_CHINH_SUA_THONG_KE_V2.md`. Toàn bộ số liệu được trích xuất tự động và đối chiếu trực tiếp từ thư mục kết quả đóng băng `results/final_v3/`.

---

## 1. Tóm tắt
- **Số nhiệm vụ hoàn thành / tổng:** 18 / 18 nhiệm vụ (100% hoàn thành, bao gồm S1–S11 và C1–C7).
- **Kết luận nào thay đổi so với bản trước (kèm số trước và sau):**
  1. **Khoảng tin cậy tốc độ đến $\lambda_h$ (S1):** Từ khoảng hẹp Poisson $\pm 4.1 - 5.2$ khách/ngày $\implies$ khoảng Student-t thực tế $\pm 6.1 - 11.1$ khách/ngày (rộng hơn $1.4\times - 2.1\times$ do overdispersion).
  2. **Bản chất của chỉ số "P(mọi giờ $\ge 90\%$)" (S2):** Từ việc coi $26.0\%$ là bằng chứng "Lịch 44 bị vỡ SLA" $\implies$ định nghĩa lại: $26.0\%$ bị chi phối bởi nhiễu lấy mẫu nhị thức của $60-100$ khách/giờ ($\pm 2.8\%$). Chỉ số kỳ vọng có điều kiện đúng nghĩa $P(E_{day} \ge 90\%)$ đạt **$88.5\%$** [83.3%, 92.2%], $P(\min_h E_h \ge 90\%)$ đạt **$65.5\%$** [58.7%, 71.7%], và gộp tháng 20 ngày đạt **$58.3\%$** [52.7%, 63.8%].
  3. **Quy tắc vận hành và mức tiết kiệm thực tế (S4):** Bỏ ngưỡng $687$ khách/ngày không có căn cứ $\implies$ Ngưỡng SLA thực nghiệm $V^* = 700$ khách/ngày và bộ dự báo sớm 8h–10h ($\hat{V} = 189.6 + 3.49 N_{8h-10h}, r=0.842$). Mức tiết kiệm kỳ vọng thực tế của chính sách ghép là **$13.76\%$** (46.57 q-h/ngày so với 54 q-h mở) và **$16.84\%$** so với 56 q-h công (thay vì 18.52% lý thuyết).
  4. **Nhiễu mô phỏng trong Bootstrap tham số (S5):** Từ việc phương sai bootstrap bị nghi ngờ do nhiễu mô phỏng $\implies$ mô hình lồng nhau $50 \times 60$ reps chứng minh nhiễu mô phỏng chỉ chiếm **$4.2\%$**, trong khi bất định tham số thực tế chiếm **$95.8\%$**.
  5. **Kiểm tra ngoài mẫu (S6):** Từ so sánh điểm với CI trung bình $\implies$ so sánh với Khoảng dự báo 95% (PI95). 7/9 giờ nằm trong PI95; kiểm định Holm xác nhận chỉ có 4 giờ khác biệt có ý nghĩa (3 giờ thực tế tốt hơn, duy nhất giờ 15h sụt giảm được đặt dưới dạng giả thuyết chốt sổ cuối ngày).
  6. **Kiểm chứng M/G/1 (S8):** Từ phát biểu "SimPy đúng tuyệt đối" $\implies$ "Không bác bỏ được tính đúng đắn của SimPy" ($W_q = 14.7856 \pm 1.0137$p so với lý thuyết $14.625$p, sai lệch $+1.10\%$, nằm trong CI95).
  7. **Cơ sở tính chi phí và nhân sự Mốc cơ sở (C4):** Từ "6 NV 8h làm việc 48 q-h" $\implies$ Phủ 6 quầy 9 giờ cần **7 nhân viên, 56 quầy-giờ công làm việc** (63 giờ có mặt).

---

## 2. Chi tiết từng nhiệm vụ

| ID | Mức | Trạng thái | File sửa / File kết quả | Số trước → sau | Ghi chú khoa học |
|---|---|:---:|---|---|---|
| **S1** | P0 | Hoàn thành | `results/final_v3/khoang_tin_cay_lambda.csv`, `params.json` | HW Poisson: 4.1–5.2 $\implies$ HW Student-t: 6.1–11.1 khách/ngày | $df=13, t=2.1604$. Tỉ số $t/\text{Poisson} = [1.48, 1.48, 2.13, 1.91, 1.40, 1.69, 1.89, 1.77, 1.58]$ |
| **S2** | P0 | Hoàn thành | `results/final_v3/chi_so_ky_vong_dieu_kien.csv` | Lịch 44: 26% thực tế $\implies P(E_{day} \ge 90\%)=88.5\%$, $P(\min E_h \ge 90\%)=65.5\%$ | $K=200, R=30$ (18k reps). Kèm Wilson CIs và góc nhìn gộp tháng 20 ngày (58.3%) |
| **S3** | P0 | Hoàn thành | `results/final_v3/do_nhay_cv_ngay.csv`, `posterior_predictive_check.csv` | 1 giá trị $CV=11.8\% \implies CV \in \{8\%, 12\%, 16\%, 20\%\}$; $D_{total}=140.4$ ($p=0.462$) | Posterior predictive check 1.000 bộ 14 ngày xác nhận mô hình hệ số nhân phù hợp tốt |
| **S4** | P0 | Hoàn thành | `results/final_v3/nguong_luu_luong_chi_tiet.csv`, `danh_gia_chinh_sach_du_bao_14ngay.csv` | Ngưỡng 687 $\implies V^*=700$; Tiết kiệm 18.5% $\implies$ thực tế 13.76% (46.57 q-h/ngày) | Bộ dự báo $\hat{V} = 189.6 + 3.49 N_{8h-10h}$ ($r=0.842, p=0.0002$, RMSE $45.3$ khách) |
| **S5** | P0 | Hoàn thành | `results/final_v3/bat_dinh_nested.csv`, `phan_ra_phuong_sai.csv` | Không rõ số reps $\implies 50 \times 60$ reps; Phân rã ANOVA phương sai | Bất định tham số chiếm 95.8% phương sai; nhiễu mô phỏng chỉ chiếm 4.2% |
| **S6** | P0 | Hoàn thành | `results/final_v3/ngoai_mau_v3.csv` | So sánh CI trung bình $\implies$ Khoảng dự báo PI95 & Holm adj p-value | 7/9 giờ trong PI95; 5/9 giờ không lệch có ý nghĩa; giờ 15h là giả thuyết chốt sổ |
| **S7** | P1 | Hoàn thành | `results/final_v3/theo_14_ngay_v3.csv` | 10/14 ngày (không CI) $\implies 12/14$ ngày (85.7% [60.1%, 96.0%]) | Đánh giá 40 reps/ngày, Student-t CI từng ngày và Wilson CI tỉ lệ đạt |
| **S8** | P1 | Hoàn thành | `results/final_v3/kiem_chung_v3.csv` | $W_q=13.87 \pm 1.54$p ("đúng tuyệt đối") $\implies 14.79 \pm 1.01$p ("không bác bỏ") | Chạy 40.000 phút, 40 reps ($df=39, t=2.0227$), sai lệch $+1.10\%$, nằm trong CI95 |
| **S9** | P1 | Hoàn thành | `results/final_v3/do_nhay_phan_phoi_v3.csv` | Thiếu giờ tệ nhất $\implies$ Có đủ giờ tệ nhất và CI hiệu số cặp | Lognormal cv+20% có giờ tệ nhất sát ngưỡng ($89.40\%$ Low CI95) |
| **S10** | P1 | Hoàn thành | `results/final_v3/kiem_dinh_phan_phoi_chi_tiet.csv`, `patience_km.csv`, `cluster_bootstrap_params.csv` | Thiếu AIC/BIC $\implies$ AIC Gamma 26279.7 (thấp nhất), nhưng KS bootstrap bác bỏ cả 4 phân phối ($p < 0.001$); Bảng Kaplan-Meier | Cluster bootstrap theo ngày: $E[S] \in [2.855, 2.993]$, $\theta \in [0.095, 0.118]$ |
| **S11** | P1 | Hoàn thành | `results/final_v3/chi_phi_v3.csv` | Xếp hạng không sai số $\implies$ CI truyền sai số và CI hiệu số theo cặp | $k \le 0.25$: Lịch 44 rẻ hơn có ý nghĩa; $k \ge 0.50$: Lịch 48 rẻ hơn ($\Delta C = +1.40$) |
| **C1** | P1 | Hoàn thành | `docs/TONG_HOP_SO_LIEU_CHI_TIET.md`, `tong_hop.md` | Lệch giữa Phần 5 và 3.3(b) $\implies$ Khớp 100% với CSV | Đồng bộ toàn bộ bảng tổng hợp với kết quả `final_v3` |
| **C2** | P1 | Hoàn thành | `docs/TONG_HOP_SO_LIEU_CHI_TIET.md`, `tong_hop.md` | "86.5%" không có trong bảng $\implies$ Sửa thành Low CI95 $88.43\%$ | Điểm ước lượng mô phỏng là $89.84\%$ |
| **C3** | P1 | Hoàn thành | `docs/TONG_HOP_SO_LIEU_CHI_TIET.md`, `tong_hop.md` | Dòng "Theo ca 52 q-h" cũ $\implies$ Chuẩn hóa ca 44 q-h thống nhất | Đồng bộ chi phí và giờ công lao động |
| **C4** | P1 | Hoàn thành | `docs/TONG_HOP_SO_LIEU_CHI_TIET.md`, `tong_hop.md` | Mốc cơ sở: 6 NV 48 q-h $\implies 7$ NV 56 q-h công (63h tại chỗ) | Nêu rõ 2 cơ sở tiết kiệm: 18.52% theo giờ mở và 21.43% theo giờ công |
| **C5** | P1 | Hoàn thành | `docs/TONG_HOP_SO_LIEU_CHI_TIET.md`, `tong_hop.md` | Chưa nêu giờ nghỉ ca 48 $\implies$ Cửa sổ nghỉ mở rộng 1-7 (4 nghiệm) | Minh bạch điều kiện biên nhân sự thực tế |
| **C6** | P1 | Hoàn thành | `results/final_v3/pha3.csv`, các tài liệu Markdown | "Đúng tuyệt đối", "biên an toàn tốt" $\implies$ Bỏ toàn bộ; Xuất `pha3.csv` | 117 phép thử vét cạn chứng minh tính tối thiểu cục bộ của Lịch 44 |
| **C7** | P2 | Hoàn thành | `tools/build_tables.py`, `tools/check_consistency.py`, `pytest_log.txt` | 18 tests $\implies 22/22$ tests passed; script tự động hóa hoàn chỉnh | 100% tài liệu sạch từ cấm và khớp số liệu `final_v3` |

---

## 3. Kết quả mới quan trọng

### Khoảng tin cậy $\lambda_h$ mới (S1)
Dựa trên ma trận 14 ngày với độ tự do $df = 13$ và $t(0.975; 13) = 2.1604$:
- **8h–9h:** $61.14 \pm 6.08$ khách/ngày $\implies \lambda_0 \in [0.918, 1.120]$ khách/phút (Poisson cũ: $\pm 4.10$).
- **9h–10h:** $86.00 \pm 7.21$ khách/ngày $\implies \lambda_1 \in [1.313, 1.554]$ khách/phút (Poisson cũ: $\pm 4.86$).
- **10h–11h:** $98.64 \pm 11.11$ khách/ngày $\implies \lambda_2 \in [1.459, 1.829]$ khách/phút (Poisson cũ: $\pm 5.20$).
- **11h–12h:** $86.36 \pm 9.31$ khách/ngày $\implies \lambda_3 \in [1.284, 1.594]$ khách/phút (Poisson cũ: $\pm 4.87$).
- **12h–13h:** $74.36 \pm 6.30$ khách/ngày $\implies \lambda_4 \in [1.134, 1.344]$ khách/phút (Poisson cũ: $\pm 4.52$).
- **13h–14h:** $74.57 \pm 7.67$ khách/ngày $\implies \lambda_5 \in [1.115, 1.371]$ khách/phút (Poisson cũ: $\pm 4.52$).
- **14h–15h:** $79.29 \pm 8.80$ khách/ngày $\implies \lambda_6 \in [1.175, 1.468]$ khách/phút (Poisson cũ: $\pm 4.66$).
- **15h–16h:** $78.29 \pm 8.21$ khách/ngày $\implies \lambda_7 \in [1.168, 1.442]$ khách/phút (Poisson cũ: $\pm 4.63$).
- **16h–17h:** $63.93 \pm 6.60$ khách/ngày $\implies \lambda_8 \in [0.955, 1.176]$ khách/phút (Poisson cũ: $\pm 4.19$).

### Chỉ số kỳ vọng có điều kiện và độ nhạy theo CV ngày (S2, S3)
| Lịch quầy | CV ngày | $P(E_{day} \ge 90\%)$ [Wilson 95%] | $P(\min_h E_h \ge 90\%)$ [Wilson 95%] | Số giờ $E_h < 90\%$ TB | $P(\text{thực tế mọi giờ} \ge 90\%)$ | $P(\text{tháng 20 ngày} \ge 90\%)$ |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Lịch 44** | **11.8% (Chuẩn)** | **88.5% [83.3%, 92.2%]** | **65.5% [58.7%, 71.7%]** | **1.17** | **25.7% [24.6%, 26.8%]** | **58.3% [52.7%, 63.8%]** |
|  | 8.0% | 93.0% [86.3%, 96.6%] | 68.0% [58.3%, 76.3%] | 0.79 | 23.2% [21.4%, 25.1%] | 66.0% [56.3%, 74.5%] |
|  | 12.0% | 88.0% [80.2%, 93.0%] | 64.0% [54.2%, 72.7%] | 1.18 | 23.2% [21.5%, 25.2%] | 59.0% [49.2%, 68.1%] |
|  | 16.0% | 82.0% [73.3%, 88.3%] | 62.0% [52.2%, 70.9%] | 1.51 | 29.6% [27.7%, 31.7%] | 59.0% [49.2%, 68.1%] |
|  | 20.0% | 75.0% [65.7%, 82.5%] | 58.0% [48.2%, 67.2%] | 2.22 | 28.7% [26.8%, 30.8%] | 55.0% [45.2%, 64.4%] |
| **Lịch 48** | **11.8% (Chuẩn)** | **98.5% [95.7%, 99.5%]** | **82.5% [76.6%, 87.1%]** | **0.35** | **46.1% [44.9%, 47.4%]** | **78.0% [73.0%, 82.3%]** |
|  | 8.0% | 100.0% [96.3%, 100.0%] | 86.0% [77.9%, 91.5%] | 0.20 | 48.2% [46.0%, 50.4%] | 83.0% [74.5%, 89.1%] |
|  | 12.0% | 97.0% [91.5%, 99.0%] | 81.0% [72.2%, 87.5%] | 0.43 | 45.1% [42.9%, 47.2%] | 79.0% [70.0%, 85.8%] |
|  | 16.0% | 97.0% [91.5%, 99.0%] | 79.0% [70.0%, 85.8%] | 0.60 | 47.2% [45.0%, 49.4%] | 77.0% [67.8%, 84.2%] |
|  | 20.0% | 85.0% [76.7%, 90.7%] | 69.0% [59.4%, 77.2%] | 1.28 | 44.6% [42.4%, 46.8%] | 67.0% [57.3%, 75.4%] |
| **Mốc 54** | **11.8% (Chuẩn)** | **100.0% [98.1%, 100.0%]** | **97.5% [94.3%, 98.9%]** | **0.03** | **76.2% [75.1%, 77.2%]** | **97.3% [94.8%, 98.6%]** |
|  | 8.0% | 100.0% [96.3%, 100.0%] | 99.0% [94.6%, 99.8%] | 0.01 | 80.0% [78.2%, 81.7%] | 99.0% [94.6%, 99.8%] |
|  | 12.0% | 100.0% [96.3%, 100.0%] | 96.0% [90.2%, 98.4%] | 0.07 | 75.8% [73.9%, 77.7%] | 96.0% [90.2%, 98.4%] |
|  | 16.0% | 100.0% [96.3%, 100.0%] | 93.0% [86.3%, 96.6%] | 0.08 | 75.3% [73.4%, 77.2%] | 92.0% [85.0%, 95.9%] |
|  | 20.0% | 94.0% [87.5%, 97.2%] | 85.0% [76.7%, 90.7%] | 0.50 | 68.6% [66.5%, 70.6%] | 85.0% [76.7%, 90.7%] |

### Ngưỡng vận hành, Bộ dự báo và Mức tiết kiệm thực tế (S4)
- **Khảo sát ngưỡng SLA:** Lịch 44 giữ vững $SL \ge 90\%$ tại các mức lưu lượng ngày $V \in \{550, 600, 650, 687, 700, 725, 750\}$ khách/ngày ($SL = 97.5\%, 96.0\%, 94.6\%, 93.8\%, 93.1\%, 91.6\%, 90.1\%$). Khi $V \ge 775$, Lịch 44 hụt ($SL = 88.5\%$). Do đó, ngưỡng vận hành an toàn là $V^* = 700$ khách/ngày.
- **Bộ dự báo OLS sớm (8h–10h):** 
  $$\hat{V} = 189.6 + 3.49 \cdot (N_{8h-9h} + N_{9h-10h})$$
  Pearson $r = 0.842$ ($p = 0.0002$), $R^2 = 0.708$, RMSE = $45.3$ khách.
- **Chính sách ghép động:** Đánh giá trên 14 ngày thực tế, có 5 ngày dự báo $\hat{V} \le 700$ (dùng Lịch 44) và 9 ngày $\hat{V} > 700$ (kích hoạt Lịch 48):
  - Quầy-giờ sử dụng trung bình: **$46.57$ quầy-giờ/ngày**.
  - Mức tiết kiệm thực tế so với 54 quầy-giờ mở: **$13.76\%$** (thay vì 18.52% tĩnh).
  - Mức tiết kiệm thực tế so với 56 quầy-giờ công (Mô hình B 6 quầy): **$16.84\%$**.

### Phân rã phương sai Bootstrap lồng nhau (S5)
- SL Toàn ngày danh nghĩa ($R=60$): $0.9381 \pm 0.0046$ (CI95: $[0.9335, 0.9427]$).
- SL Giờ tệ nhất danh nghĩa ($R=60$, cùng định nghĩa min trung bình giờ): $0.9060$.
- **Tổng phương sai quan sát:** $\text{Var}_{\text{total}} = 1.294 \times 10^{-4}$ ($SD = 0.01138$).
- **Phương sai do nhiễu mô phỏng:** $\text{Var}_{\text{within}}/R = 5.446 \times 10^{-6}$ (**$4.21\%$** tổng phương sai).
- **Phương sai do bất định tham số thực tế:** $\text{Var}_{\text{between}} = 1.240 \times 10^{-4}$ (**$95.79\%$** tổng phương sai).
- Xác suất $SL_{\text{toàn ngày}} \ge 90\%$: **$100.0\%$** (Wilson 95%: $[92.9\%, 100.0\%]$).
- Xác suất $SL_{\text{giờ tệ nhất}} \ge 90\%$: **$90.0\%$** (Wilson 95%: $[78.6\%, 95.7\%]$).

### Khoảng dự báo ngoài mẫu và Giờ lệch có ý nghĩa (S6)
Đối chiếu 2.969 cuộc gọi tập Test (ngày 10–13) với Khoảng dự báo 95% (PI95) và hiệu chỉnh Holm-Bonferroni ($\alpha = 0.05$):
- **8h–9h:** Mô phỏng TB $93.77\%$, PI95 $[86.27\%, 98.60\%]$, Thực tế **$98.09\%$** [95.61%, 99.18%] (Trong PI95, Holm $p_{\text{adj}} = 0.0229 \implies$ Lệch có ý nghĩa, thực tế tốt hơn).
- **9h–10h:** Mô phỏng TB $92.40\%$, PI95 $[84.32\%, 97.83\%]$, Thực tế **$97.35\%$** [95.20%, 98.56%] (Trong PI95, Holm $p_{\text{adj}} = 0.0022 \implies$ Lệch có ý nghĩa, thực tế tốt hơn).
- **10h–11h:** Mô phỏng TB $95.08\%$, PI95 $[88.38\%, 98.77\%]$, Thực tế $92.83\%$ [90.10%, 94.85%] (Trong PI95, Holm $p_{\text{adj}} = 0.1031 \implies$ **Không lệch có ý nghĩa**).
- **11h–12h:** Mô phỏng TB $91.62\%$, PI95 $[82.82\%, 97.21\%]$, Thực tế $94.13\%$ [91.28%, 96.09%] (Trong PI95, Holm $p_{\text{adj}} = 0.2359 \implies$ **Không lệch có ý nghĩa**).
- **12h–13h:** Mô phỏng TB $94.34\%$, PI95 $[87.89\%, 98.61\%]$, Thực tế $98.65\%$ [96.59%, 99.48%] (Ngoài PI95, Holm $p_{\text{adj}} = 0.0091 \implies$ Lệch có ý nghĩa, thực tế tốt hơn).
- **13h–14h:** Mô phỏng TB $95.15\%$, PI95 $[88.53\%, 98.85\%]$, Thực tế $94.43\%$ [91.36%, 96.45%] (Trong PI95, Holm $p_{\text{adj}} = 0.5427 \implies$ **Không lệch có ý nghĩa**).
- **14h–15h:** Mô phỏng TB $92.98\%$, PI95 $[85.04\%, 97.89\%]$, Thực tế $89.58\%$ [85.66%, 92.52%] (Trong PI95, Holm $p_{\text{adj}} = 0.0976 \implies$ **Không lệch có ý nghĩa**).
- **15h–16h:** Mô phỏng TB $92.93\%$, PI95 $[84.51\%, 97.92\%]$, Thực tế $76.47\%$ [71.41%, 80.88%] (Ngoài PI95, Holm $p_{\text{adj}} < 0.0001 \implies$ Lệch có ý nghĩa, thực tế sụt giảm mạnh, $W_q = 1.41$ phút, bỏ về $15.0\%$).
- **16h–17h:** Mô phỏng TB $91.05\%$, PI95 $[81.57\%, 97.06\%]$, Thực tế $93.87\%$ [90.28%, 96.19%] (Trong PI95, Holm $p_{\text{adj}} = 0.2359 \implies$ **Không lệch có ý nghĩa**).

---

## 4. Việc chưa làm được và thông tin cần bổ sung
1. **Kiểm chứng cơ chế chốt sổ cuối ngày (15h–16h):** Hiện tượng sụt giảm mức phục vụ xuống $76.47\%$ tại giờ 15h–16h ở tập Test hiện mới dừng lại ở dạng giả thuyết (do dồn chứng từ, đóng sổ giao dịch hoặc giảm quầy thực tế). Dữ liệu hiện tại không ghi nhận số quầy vật lý thực tế mở tại quầy theo từng phút. Cần bổ sung nhật ký quầy giao dịch (teller log) để kiểm chứng dứt khoát.
2. **Khảo sát chuỗi thời gian nhiều tháng:** Cỡ mẫu 14 ngày (10 ngày train, 4 ngày test) tuy đủ để ước lượng các tham số tĩnh nhưng có năng lực thống kê thấp đối với kiểm định ngoài mẫu. Cần thu thập dữ liệu $2-3$ tháng để đánh giá tính mùa vụ và kiểm định độ co dãn nhu cầu hoàn chỉnh hơn.

---

## 5. Rủi ro còn lại
1. **Rủi ro dự báo sai lệch ngày tải cực đoan:** Bộ dự báo 8h–10h có sai số RMSE khoảng 45 khách. Trong trường hợp khách hàng dồn đến bất thường vào buổi chiều (không phát tín hiệu trong 2 giờ đầu), hệ thống vận hành theo Lịch 44 có thể chịu mức phục vụ thấp hơn $90\%$ ở một số giờ cao điểm.
2. **Rủi ro linh hoạt nhân sự ca 4 giờ:** Chính sách ghép đòi hỏi khả năng điều động thêm nhân viên ca 4 giờ hoặc nhân viên bán thời gian vào lúc 10h sáng khi phát hiện tín hiệu tải cao. Nếu quy chế nội bộ ngân hàng không cho phép gọi ca linh hoạt trước 2 tiếng, ngân hàng nên áp dụng trực tiếp Phương án Dự phòng Bền vững (Lịch 48).
