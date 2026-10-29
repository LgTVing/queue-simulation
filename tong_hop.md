# BẢNG TỔNG HỢP SỐ LIỆU CUỐI CÙNG VÀ ĐÁNH GIÁ TOÀN DIỆN DỰ ÁN (PHIÊN BẢN V4)

**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu cho quầy giao dịch ngân hàng  
**Thời điểm tổng hợp:** 2026-10-29 (V4: sửa động cơ mô phỏng F1–F3, phục vụ thực nghiệm M3, kịch bản kiên nhẫn M1, ràng buộc bỏ về M2, điều tra 15h–16h M4, ổn định giờ tệ nhất M5; đóng băng tại `results/final_v4/`)  
**Bộ dữ liệu:** Anonymous Bank Call Center (Technion SEE Center), 14 ngày làm việc, $9.836$ giao dịch  
**Lệnh tái lập:** `python main.py --stage all --reps-scale 1.0` (33.3 phút; seed chọn lịch `1000`, seed đánh giá `50000`)

---

## MỤC LỤC

1. [BẢNG QUYẾT ĐỊNH QUẢN TRỊ TỔNG THỂ](#1-bảng-quyết-định-quản-trị-tổng-thể)
2. [TỔNG HỢP DỮ LIỆU THỰC TẾ VÀ KIỂM ĐỊNH PHÂN PHỐI](#2-tổng-hợp-dữ-liệu-thực-tế-và-kiểm-định-phân-phối)
3. [TỔNG HỢP SỐ LIỆU KIỂM CHỨNG CODE PYTHON / SIMPY](#3-tổng-hợp-số-liệu-kiểm-chứng-code-python--simpy)
4. [BẢNG SO SÁNH CÁC CHÍNH SÁCH PHỤC VỤ (DANH ĐỊNH & BIẾN ĐỘNG NGÀY)](#4-bảng-so-sánh-các-chính-sách-phục-vụ-danh-định--biến-động-ngày)
5. [ĐÁNH GIÁ NGOÀI MẪU VỚI KHOẢNG DỰ BÁO 95% (PI95) VÀ HOLM-BONFERRONI (S6, M4)](#5-đánh-giá-ngoài-mẫu-với-khoảng-dự-báo-95-pi95-và-holm-bonferroni-s6-m4)
6. [TỐI ƯU HÓA LỊCH CA LÀM VIỆC THỰC TẾ (MILP)](#6-tối-ưu-hóa-lịch-ca-làm-việc-thực-tế-milp)
7. [PHÂN TÍCH ĐỘ NHẠY VÀ ĐÁNH ĐỔI KINH TẾ](#7-phân-tích-độ-nhạy-và-đánh-đổi-kinh-tế)
8. [ĐỐI CHIẾU V3 → V4](#8-đối-chiếu-v3--v4)
9. [TỔNG KẾT KIỂM THỬ VÀ TRẠNG THÁI BÀN GIAO](#9-tổng-kết-kiểm-thử-và-trạng-thái-bàn-giao)
10. [HẠN CHẾ CẦN NÊU KHI BÁO CÁO](#10-hạn-chế-cần-nêu-khi-báo-cáo)

---

## 1. BẢNG QUYẾT ĐỊNH QUẢN TRỊ TỔNG THỂ

**Kết luận một dòng:** cần tối thiểu **45 quầy-giờ/ngày**, phân bổ `[4, 5, 6, 5, 5, 5, 5, 5, 5]` theo giờ 8h–17h, để $\ge 90\%$ khách chờ dưới 5 phút ở mọi giờ (cận dưới CI95); nếu khách quầy kiên nhẫn hơn khách tổng đài, con số tăng lên **46 quầy-giờ** (kiên nhẫn 15–60 phút) và tối đa **48 quầy-giờ** (không ai bỏ về).

Số liệu trích từ `results/final_v4/` (300 lần lặp, seed đánh giá tách khỏi seed chọn lịch):

| Tiêu chí quản trị | Phương án Tối ưu Thường nhật (Khuyến nghị 1) | Phương án Dự phòng Bền vững (Khuyến nghị 2) | Mốc cơ sở: Hằng số 6 quầy |
|---|:---:|:---:|:---:|
| **Lịch quầy chi tiết theo giờ (8h - 17h)** | `[4, 5, 6, 5, 5, 5, 5, 5, 5]` | `[4, 6, 6, 6, 5, 5, 6, 5, 5]` | `[6, 6, 6, 6, 6, 6, 6, 6, 6]` |
| **Tổng số quầy-giờ mở** | **45 quầy-giờ/ngày** | **48 quầy-giờ/ngày** | **54 quầy-giờ/ngày** |
| **Tiết kiệm quầy-giờ mở so với mốc 54** | **16.67% (-9 q-h/ngày)** | **11.11% (-6 q-h/ngày)** | Mốc (0.0%) |
| **Mức phục vụ $SL$ danh định (CI95)** | **$94.23\% \pm 0.22\%$** | **$95.79\% \pm 0.17\%$** | $97.63\% \pm 0.12\%$ |
| **Mức phục vụ $SL$ giờ tệ nhất (Low CI95)** | **$92.36\%$** (11h–12h, 300 lần lặp)<br>*(M5, 1.646 lần lặp: 11h–12h là giờ tệ nhất với xác suất 99.7%, cận dưới $92.16\%$)* | **$93.27\%$** (15h–16h) | $94.94\%$ (10h–11h) |
| **$P(SL \text{ kỳ vọng ngày} \ge 90\%)$**, $CV_{\text{ngày}} = 14.0\%$ | **$88.0\%$** (Wilson 95%: $[82.8\%, 91.8\%]$) | **$96.0\%$** (Wilson 95%: $[92.3\%, 98.0\%]$) | **$99.5\%$** (Wilson 95%: $[97.2\%, 99.9\%]$) |
| **$P(\min_h E_h(m) \ge 90\%)$** | **$73.0\%$** (Wilson 95%: $[66.5\%, 78.7\%]$)<br>*Số giờ $E_h < 90\%$ TB: 1.09 giờ* | **$83.5\%$** (Wilson 95%: $[77.7\%, 88.0\%]$)<br>*Số giờ $E_h < 90\%$ TB: 0.51 giờ* | **$93.5\%$** (Wilson 95%: $[89.2\%, 96.2\%]$)<br>*Số giờ $E_h < 90\%$ TB: 0.10 giờ* |
| **$P(\text{thực tế mọi giờ} \ge 90\%)$** | **$29.0\%$** (Wilson 95%: $[27.8\%, 30.1\%]$)<br>*(Bị chi phối mạnh bởi cỡ mẫu giờ)* | **$43.9\%$** (Wilson 95%: $[42.7\%, 45.2\%]$) | **$71.8\%$** (Wilson 95%: $[70.6\%, 72.9\%]$) |
| **$P(\text{gộp tháng 20 ngày mọi giờ} \ge 90\%)$** | **$65.0\%$** (Wilson 95%: $[59.4\%, 70.2\%]$) | **$78.3\%$** (Wilson 95%: $[73.3\%, 82.6\%]$) | **$92.7\%$** (Wilson 95%: $[89.1\%, 95.1\%]$) |
| **Số ngày thực tế 14 ngày đạt SLA** | **12/14 ngày (85.7% [60.1%, 96.0%])**<br>*(Hụt ngày 2: 87.66% và ngày 7: 88.36%)* | **14/14 ngày (100.0% [78.5%, 100.0%])** | **14/14 ngày (100.0% [78.5%, 100.0%])** |
| **Mức phục vụ Khách VIP ($W_q \le 2$ phút)** | **$95.58\%$** | **$96.74\%$** | $98.22\%$ |
| **Thời gian chờ trung bình $W_q$** | **$0.4628 \pm 0.0150$ phút (~27.8 giây)** | **$0.3432 \pm 0.0123$ phút (~20.6 giây)** | $0.2024 \pm 0.0091$ phút (~12.1 giây) |
| **Tỉ lệ khách hàng bỏ về trung bình** | **$4.99\% \pm 0.16\%$** | **$3.70\% \pm 0.13\%$ (giảm 26% khách mất)** | $2.17\% \pm 0.10\%$ |
| **Hiệu suất sử dụng quầy giao dịch $\rho$** | **$70.85\% \pm 0.39\%$** | **$67.33\% \pm 0.39\%$** | $60.77\% \pm 0.37\%$ |
| **Phương án tổ chức ca (nghỉ trưa 11h–14h, ca 8h + 4h)** | **5 NV 8h + 2 NV 4h = 48 q-h công**<br>*(Không có cách phủ đúng 45 q-h; dư 3 q-h)* | **4 NV 8h + 4 NV 4h = 48 q-h công**<br>*(Phủ đúng 48 q-h)* | **6 NV 8h + 2 NV 4h = 56 q-h công**<br>*(Không phủ đúng được 54; dư 2 q-h)* |
| **Độ bền khi nhu cầu tăng +10%** | Giờ tệ nhất Low CI95 **$87.93\%$** (SL ngày $92.00\%$) | Giờ tệ nhất Low CI95 **$90.87\%$** (SL ngày $94.23\%$) | Giờ tệ nhất Low CI95 $92.67\%$ |
| **Quy tắc kích hoạt vận hành** | Áp dụng khi $\hat{V} \le 803$ khách/ngày (dự báo sớm 8h–10h: $r=0.842, p=0.0002$) | Chuyển sang lúc 10h khi $\hat{V} > 803$ khách/ngày | Mốc đối chiếu |

> [!IMPORTANT]
> **Hệ quả của bảng ca làm việc:** với nghỉ trưa 11h–14h và ca 8h/4h, Lịch 45 và Lịch 48 **cùng tốn 48 quầy-giờ công**. Nếu chi phí là giờ công nhân viên chứ không phải giờ mở quầy, Lịch 48 (bền vững) có cùng chi phí nhân sự với Lịch 45 nhưng SL cao hơn và bỏ về thấp hơn. Lịch 45 chỉ tiết kiệm hơn khi giờ mở quầy có chi phí riêng (điện, hệ thống, quầy) hoặc khi có thể bố trí 3 quầy-giờ dư cho việc khác. Phương án ca cho Lịch 48 và mốc 54 giải bằng cùng hàm `b_shifts.solve_shift_scheduling` (pipeline hiện chỉ ghi `lich_theo_ca.csv` cho lịch tối ưu, xem mục 6).

---

## 2. TỔNG HỢP DỮ LIỆU THỰC TẾ VÀ KIỂM ĐỊNH PHÂN PHỐI

### 2.1 Dữ liệu thực tế và Đối chiếu Train / Test / Toàn bộ

Dữ liệu được trích xuất từ phân hệ nghiệp vụ khách hàng cá nhân thông thường (`PS`), hoạt động từ **8:00:00 đến 17:00:00** qua 14 ngày làm việc tiêu chuẩn:

| Đại lượng thống kê | Tập Ước lượng (Train - 10 ngày) | Tập Kiểm tra (Test - 4 ngày) | Toàn bộ Dữ liệu (14 ngày) |
|---|:---:|:---:|:---:|
| **Tổng số lượt khách đến** | **6.867 lượt** | **2.969 lượt** | **9.836 lượt** |
| **Số khách trung bình / ngày** | 686.7 khách/ngày | 742.3 khách/ngày | 702.6 khách/ngày |
| **Thời gian phục vụ TB ($E[S]$)** | **$2.9236$ phút** | $2.7755$ phút | $2.8784$ phút |
| **Độ lệch chuẩn thời gian phục vụ ($s$)** | $3.2051$ phút | $3.0280$ phút | $3.1527$ phút |
| **Hệ số biến thiên ($cv = s/\bar{x}$)** | **$1.0963$** | $1.0910$ | $1.0953$ |
| **Bình phương hệ số biến thiên ($cs^2$)** | **$1.2018$** | $1.1903$ | $1.1996$ |
| **Tốc độ bỏ về ước lượng MLE ($\theta$)** | **$0.1087 \text{ phút}^{-1}$ (TB 9.20p)** | $0.1241 \text{ phút}^{-1}$ (TB 8.06p) | $0.1123 \text{ phút}^{-1}$ (TB 8.91p) |
| **Tỉ lệ khách hàng ưu tiên (VIP)** | **$35.43\%$** | $30.18\%$ | $33.85\%$ |
| **Thời gian chờ TB quan sát thực tế (mọi khách)** | $0.6981$ phút | $0.4940$ phút | $0.6365$ phút |
| **Tỉ lệ khách bỏ về quan sát thực tế** | $7.59\%$ | $6.13\%$ | $7.15\%$ |

> Ghi chú: hai dòng cuối tính trực tiếp từ `data/clean/data_clean.csv` (cột `wait`, `served`). Thỏa mãn đẳng thức MLE $\hat{p}_{ab} = \hat\theta \cdot \overline{W}$ (train: $0.1087 \times 0.6981 = 7.59\%$). Số quầy mở thực tế của ngân hàng không có trong dữ liệu; ước lượng số người phục vụ đồng thời ở mục 5.

---

### 2.2 Thống kê 9 khung giờ & Khoảng tin cậy Student-t của $\lambda_h$ (S1)

Do số khách thực tế theo ngày bị quá phân tán ở 8/9 giờ, công thức Poisson $1.96 \sqrt{\bar{N}/n}/60$ bị hẹp hơn thực tế $1.4 - 2.1$ lần. Khoảng tin cậy dùng phân phối Student-t với $df=13$ ($t_{0.975; 13} = 2.1604$), tại `results/final_v4/khoang_tin_cay_lambda.csv` và `kiem_dinh_poisson.csv`:

| Khung giờ | Giờ ID | $\bar{N}_h$ (khách/ngày) | Bán độ rộng Poisson | Bán độ rộng Student-t | Tỉ số t/Poisson | $\lambda_h$ (khách/phút) | CI95 Low $\lambda$ | CI95 High $\lambda$ | Chỉ số $D$ | $p$-value Poisson | Nhãn Poisson ($\alpha=0.05$) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h-9h** | 0 | 61.14 | 4.10 | **6.08** | 1.48 | 1.0190 | 0.9178 | 1.1203 | 23.55 | 0.0356 | Bác bỏ (nhẹ) |
| **9h-10h** | 1 | 86.00 | 4.86 | **7.21** | 1.48 | 1.4333 | 1.3131 | 1.5535 | 23.58 | 0.0352 | Bác bỏ (nhẹ) |
| **10h-11h** | 2 | 98.64 | 5.20 | **11.11** | 2.13 | 1.6440 | 1.4589 | 1.8292 | 48.77 | 0.0000 | Bác bỏ (mạnh) |
| **11h-12h** | 3 | 86.36 | 4.87 | **9.31** | 1.91 | 1.4393 | 1.2841 | 1.5945 | 39.15 | 0.0002 | Bác bỏ (mạnh) |
| **12h-13h** | 4 | 74.36 | 4.52 | **6.30** | 1.40 | 1.2393 | 1.1342 | 1.3443 | 20.83 | 0.0763 | Chưa bác bỏ |
| **13h-14h** | 5 | 74.57 | 4.52 | **7.67** | 1.69 | 1.2429 | 1.1151 | 1.3706 | 30.73 | 0.0037 | Bác bỏ (mạnh) |
| **14h-15h** | 6 | 79.29 | 4.66 | **8.80** | 1.89 | 1.3214 | 1.1748 | 1.4681 | 38.08 | 0.0003 | Bác bỏ (mạnh) |
| **15h-16h** | 7 | 78.29 | 4.63 | **8.21** | 1.77 | 1.3048 | 1.1679 | 1.4417 | 33.61 | 0.0014 | Bác bỏ (mạnh) |
| **16h-17h** | 8 | 63.93 | 4.19 | **6.60** | 1.58 | 1.0655 | 0.9554 | 1.1755 | 26.61 | 0.0141 | Bác bỏ (nhẹ) |

> Bảng này tính trên cả 14 ngày (mô tả dữ liệu). Mô hình mô phỏng dùng $\lambda_h$ của **tập train 10 ngày** (bảng 2.4); CI Student-t của tập train ($df=9$) lưu trong `results/final_v4/params.json` (`rates_ci95`, kèm `rates_ci95_poisson` để so sánh).

---

### 2.3 Hiện tượng Quá phân tán (Overdispersion)

Kết quả phân tích quá phân tán toàn ngày (`results/final_v4/qua_phan_tan_ngay.csv`):

| Chỉ số thống kê quá phân tán | Giá trị thực nghiệm | Ghi chú so sánh lý thuyết |
|---|:---:|---|
| **Số ngày quan sát** | 14 ngày | Tập dữ liệu hoàn chỉnh |
| **Số khách trung bình một ngày ($\text{Mean}$)** | **702.6 khách** | Kỳ vọng quy mô ngày |
| **Độ lệch chuẩn thực tế ($SD_{\text{thực tế}}$)** | **87.1 khách** | Biến thiên thực tế giữa các ngày |
| **Độ lệch chuẩn Poisson lý thuyết ($\sqrt{\text{Mean}}$)** | **26.5 khách** | Giả định nếu tuân theo Poisson thuần túy |
| **Tỉ số Phương sai / Kỳ vọng ($\text{Var}/\text{Mean}$)** | **10.8** | **$\gg 1.0 \implies$ Quá phân tán nghiêm trọng** |
| **Hệ số biến thiên thô ($CV_{\text{thô}} = SD/\text{Mean}$)** | **$12.4\%$** | Biến thiên gộp cả nhiễu Poisson và biến động ngày |
| **Hệ số biến thiên quy mô ngày, 14 ngày ($CV_{\text{ngày}}$)** | **$11.8\%$** | $\sqrt{\text{Var} - \text{Mean}}/\text{Mean}$ (đã trừ nhiễu Poisson) |
| **$CV_{\text{ngày}}$ ước lượng trên train (dùng trong mô phỏng V4)** | **$14.0\%$** | `params.json` (`day_cv`); V3 dùng 11.8% của cả 14 ngày |

---

### 2.4 Bảng tính giải tích Erlang C và Erlang-A SIPP

Tính bằng `b_theory.py` (SIPP, $E[S] = 2.9236$ phút, $\theta = 0.1087$, tham số train), lưu tại `results/final_v4/bang_sipp.csv`. $SL$ Erlang C $= P(W_q \le 5)$ (không có bỏ về); $SL$ Erlang-A $= P(\text{được phục vụ và chờ} \le 5)$:

| Khung giờ | $\lambda_{\text{train}}$ (khách/phút) | Nhu cầu tải $a_h$ (Erlang) | Số quầy Erlang C | $SL$ Erlang C | Số quầy Erlang-A | $SL$ Erlang-A | $p_{ab}$ Erlang-A | Lịch tối ưu mô phỏng |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h - 9h** | 0.9900 | 2.89 | 4 | 93.0% | **4** | **93.6%** | 5.8% | 4 |
| **9h - 10h** | 1.3767 | 4.02 | 6 | 99.0% | **5** | **93.1%** | 6.4% | 5 |
| **10h - 11h (Đỉnh)** | 1.5350 | 4.49 | 6 | 96.9% | **6** | **95.8%** | 4.1% | 6 |
| **11h - 12h** | 1.3900 | 4.06 | 6 | 98.9% | **5** | **92.8%** | 6.6% | 5 |
| **12h - 13h** | 1.2400 | 3.63 | 5 | 96.0% | **5** | **95.2%** | 4.5% | 5 |
| **13h - 14h** | 1.2017 | 3.51 | 5 | 97.0% | **5** | **95.7%** | 4.1% | 5 |
| **14h - 15h** | 1.3383 | 3.91 | 5 | 91.9% | **5** | **93.7%** | 5.9% | 5 |
| **15h - 16h** | 1.3167 | 3.85 | 5 | 93.0% | **5** | **94.1%** | 5.5% | 5 |
| **16h - 17h** | 1.0567 | 3.09 | 5 | 99.0% | **4** | **92.2%** | 7.0% | **5** |
| **TỔNG QUẦY-GIỜ** | - | - | **47 q-h** | - | **44 q-h** | - | - | **45 q-h** |

> Lịch tối ưu mô phỏng chỉ khác Erlang-A ở giờ 16h–17h. Erlang-A coi giờ 16h–17h như hệ dừng; trong mô phỏng V4, hàng còn tồn lúc 17h được xả bằng đúng số quầy giờ cuối (F1), và phục vụ thực nghiệm có $cs^2 = 1.20$ thay vì 1.0 (M3).

---

### 2.5 Kiểm định độ phù hợp phân phối phục vụ và kiên nhẫn (S10)

Chi tiết tại `results/final_v4/kiem_dinh_phan_phoi_chi_tiet.csv` và `results/final_v4/cluster_bootstrap_params.csv`:

| Phân phối | Tham số ước lượng | Log-Likelihood | AIC | BIC | KS Stat | KS $p$-value (Bootstrap) | Đánh giá khoa học |
|---|---|:---:|:---:|:---:|:---:|:---:|---|
| **Gamma** | $\text{shape}=1.0955, \text{scale}=2.6688$ ($cs^2 = 0.91$) | -13137.8 | **26279.7** | **26293.2** | 0.0717 | < 0.001 | AIC/BIC thấp nhất, nhưng **bị bác bỏ** |
| **Weibull** | $c=1.0335, \text{scale}=2.9650$ ($cs^2 = 0.94$) | -13148.1 | 26300.2 | 26313.7 | 0.0799 | < 0.001 | Bị bác bỏ |
| **Exponential** | $\text{scale} = 2.9236$ ($cs^2 = 1.00$) | -13154.2 | 26310.4 | 26317.1 | 0.0913 | < 0.001 | Bị bác bỏ |
| **Lognormal** | $s=1.2150, \text{scale}=1.7357$ ($cs^2 = 3.38$) | -13739.5 | 27483.0 | 27496.5 | 0.1159 | < 0.001 | Kém nhất, bị bác bỏ |

- **Kết luận:** với $n = 6.346$ thời gian phục vụ (train), **cả 4 phân phối đều bị bác bỏ** bởi kiểm định KS bootstrap (thống kê KS quy đổi theo cỡ mẫu, mẫu mô phỏng 1.000).
- **Lựa chọn mô hình V4 (M3):** mô phỏng chính lấy mẫu có hoàn lại trực tiếp từ 6.346 thời gian phục vụ train (giữ đúng $cs^2 = 1.20$). Gamma ($cs^2 = 0.91$) đánh giá thấp độ biến động nên chuyển sang phân tích độ nhạy (mục 7.2).
- **Bảng sống sót Kaplan–Meier** (`results/final_v4/patience_km.csv`): đường KM giảm nhanh hơn đường mũ ở vùng chờ ngắn. Khách bỏ về sớm nhiều hơn giả định mũ, nên kiên nhẫn ~ Exponential($\theta$) chỉ là xấp xỉ; ảnh hưởng của kiên nhẫn được kiểm tra ở mục 7.5 (M1).
- **Khoảng tin cậy Cluster Bootstrap theo ngày (xét tương quan trong ngày):**
  - Thời gian phục vụ trung bình $E[S]$: $[2.8589, 2.9929]$ phút (trung bình mẫu $2.9236$).
  - Tốc độ bỏ về $\theta$: $[0.0936, 0.1182]\text{ phút}^{-1}$ (trung bình mẫu $0.1087$).

---

## 3. TỔNG HỢP SỐ LIỆU KIỂM CHỨNG CODE PYTHON / SIMPY

### 3.1 Kiểm chứng ba tầng và M/G/1 Pollaczek–Khinchine exact 40.000 phút (S8)

Khoảng tin cậy dùng giá trị tới hạn Student-t ($df = n_{\text{reps}} - 1$). Chi tiết tại `results/final_v4/kiem_chung.csv`:

| Tầng kiểm chứng | Chỉ số đánh giá | Giá trị Lý thuyết | Giá trị Mô phỏng | $n_{\text{reps}}$ | $t_{\text{crit}}$ | Khoảng tin cậy 95% | Sai lệch | Đạt? | Ghi chú kỹ thuật |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **Tầng 1 (M/M/c)** | $SL = P(W_q \le 5\text{p})$ | 0.9654 | **0.9688** | 30 | 2.0452 | ±0.0037 | $+0.35\%$ | **Y** | Lý thuyết nằm trong CI95 [0.9651, 0.9725] |
| **Tầng 1 (M/M/c)** | $W_q$ (phút) | 0.8433 | **0.8170** | 30 | 2.0452 | ±0.0423 | $-3.12\%$ | **Y** | Lý thuyết nằm trong CI95 [0.775, 0.859] |
| **Tầng 1 (M/M/c)** | Hiệu suất quầy $\rho$ | 0.7500 | **0.7511** | 30 | 2.0452 | ±0.0048 | $+0.15\%$ | **Y** | Khớp định luật Little ($\rho = 0.75$) |
| **Tầng 2 (Erlang-A)** | $SL$ (chờ $\le 5$p) | 0.8689 | **0.8695** | 30 | 2.0452 | ±0.0034 | $+0.07\%$ | **Y** | Khớp nghiệm ma trận hấp thụ Markov |
| **Tầng 2 (Erlang-A)** | $W_q$ (phút) | 1.1444 | **1.1475** | 30 | 2.0452 | ±0.0233 | $+0.27\%$ | **Y** | $W_q$ tính trên mọi khách ($L_q / \lambda$) |
| **Tầng 2 (Erlang-A)** | Tỉ lệ bỏ về $p_{ab}$ | 0.1144 | **0.1142** | 30 | 2.0452 | ±0.0022 | $-0.21\%$ | **Y** | Lý thuyết nằm trong CI95 [0.1120, 0.1164] |
| **Tầng 2 (Erlang-A)** | Hiệu suất quầy $\rho$ | 0.8856 | **0.8863** | 30 | 2.0452 | ±0.0032 | $+0.08\%$ | **Y** | Khớp $\rho = \lambda(1-p_{ab})E[S]/c$ |
| **Tầng 3 (M/G/c, cv=0.5)** | $W_q$ (phút) | 0.5271 | **0.5616** | 30 | 2.0452 | ±0.0176 | $+6.55\%$ | - | Allen–Cunneen đánh giá thấp ~6-7% |
| **Tầng 3 (M/G/c, cv=1.0)** | $W_q$ (phút) | 0.8433 | **0.8113** | 30 | 2.0452 | ±0.0521 | $-3.80\%$ | - | Khớp Erlang C chuẩn (sai lệch < 5%) |
| **Tầng 3 (M/G/c, cv=1.5)** | $W_q$ (phút) | 1.3704 | **1.1333** | 30 | 2.0452 | ±0.1239 | $-17.30\%$ | - | Allen–Cunneen đánh giá cao; kiểm tra qua M/G/1 |
| **Kiểm tra A (M/G/1 exact, 40k phút, 40 reps)** | $W_q$ (phút) | **14.6250** | **14.2179** | 40 | 2.0227 | ±0.6273 | **$-2.78\%$** | **Y** | **Lý thuyết nằm trong CI95 [13.59, 14.85]; không bác bỏ được tính đúng của SimPy** |
| **Kiểm tra B (M/G/6, cv=1.5, 60 lần lặp)** | $W_q$ (phút) | 1.3704 | **1.1815** | 60 | 2.0010 | ±0.0722 | $-13.78\%$ | - | Allen–Cunneen đánh giá cao khi cv > 1 (xấp xỉ, không phải nghiệm đúng) |

Tầng 3 so với công thức xấp xỉ Allen–Cunneen nên không gán "Đạt"; tính đúng của động cơ với phục vụ tổng quát được kiểm tra bằng nghiệm chính xác M/G/1 (Kiểm tra A). Kiểm chứng gộp hàng (`kiem_chung_pooling.csv`): 1 hàng chung M/M/6 đạt SL 96.5%, 6 hàng riêng ngẫu nhiên 50.6% (lý thuyết) / 50.7% (SimPy), 6 hàng chọn ngắn nhất 81.1%.

---

### 3.2 Lịch sử Thuật toán Tối ưu hóa 2 Pha SimPy

Lịch sử 11 bước tại `results/final_v4/lich_toi_uu.csv` (60 lần lặp/bước, seed chọn lịch `1000`; tiêu chí: cận dưới CI95 của SL mọi giờ $\ge 90\%$):

| Bước (`buoc`) | Pha (`pha`) | Cấu hình quầy thử nghiệm | Quầy-giờ | $SL$ Toàn ngày | Giờ tệ nhất | $SL$ Giờ tệ nhất (Low CI95) | Giờ vi phạm | Đạt SLA? |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 1 (Khởi tạo SIPP Erlang-A) | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | 44 | 0.9387 | Giờ 8 | 0.8893 | [8] | N |
| **1** | **1 (Thêm quầy H8)** | `[4, 5, 6, 5, 5, 5, 5, 5, 5]` | **45** | **0.9439** | **Giờ 1** | **0.9064** | **[]** | **Y (ĐẠT)** |
| 2 | 2 (Bớt H2) | `[4, 5, 5, 5, 5, 5, 5, 5, 5]` | 44 | 0.9361 | Giờ 2 | 0.8848 | [2] | N |
| 3 | 2 (Bớt H1) | `[4, 4, 6, 5, 5, 5, 5, 5, 5]` | 44 | 0.9296 | Giờ 1 | 0.7820 | [1] | N |
| 4 | 2 (Bớt H3) | `[4, 5, 6, 4, 5, 5, 5, 5, 5]` | 44 | 0.9311 | Giờ 3 | 0.8100 | [3] | N |
| 5 | 2 (Bớt H4) | `[4, 5, 6, 5, 4, 5, 5, 5, 5]` | 44 | 0.9336 | Giờ 4 | 0.8344 | [4] | N |
| 6 | 2 (Bớt H5) | `[4, 5, 6, 5, 5, 4, 5, 5, 5]` | 44 | 0.9361 | Giờ 5 | 0.8628 | [5] | N |
| 7 | 2 (Bớt H6) | `[4, 5, 6, 5, 5, 5, 4, 5, 5]` | 44 | 0.9339 | Giờ 6 | 0.8404 | [6] | N |
| 8 | 2 (Bớt H7) | `[4, 5, 6, 5, 5, 5, 5, 4, 5]` | 44 | 0.9337 | Giờ 7 | 0.8322 | [7] | N |
| 9 | 2 (Bớt H8) | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | 44 | 0.9387 | Giờ 8 | 0.8893 | [8] | N |
| 10 | 2 (Bớt H0) | `[3, 5, 6, 5, 5, 5, 5, 5, 5]` | 44 | 0.9335 | Giờ 0 | 0.8095 | [0] | N |

---

### 3.3 Phân tích Bootstrap lồng nhau và Phân rã phương sai ANOVA (S5)

Mô hình lồng nhau: $B = 50$ bộ tham số (resample ngày train; mẫu phục vụ resample trực tiếp, không fit lại Gamma) $\times R = 60$ lần lặp/bộ. Chi tiết tại `results/final_v4/phan_ra_phuong_sai.csv` và `bat_dinh_nested.csv`:

| Chỉ số phân rã phương sai | Giá trị thực nghiệm | Khoảng tin cậy 95% | Diễn giải |
|---|:---:|:---:|---|
| **SL Toàn ngày danh nghĩa ($R=60$)** | **0.9424** | [0.9377, 0.9470] | Trung bình qua 60 lần lặp độc lập |
| **SL Giờ tệ nhất danh nghĩa ($R=60$)** | **0.9225** | - | Trung bình theo giờ rồi lấy min |
| **Phương sai tổng quan sát qua 50 bộ** | $9.548 \times 10^{-5}$ | - | $SD = 0.00977$ |
| **Phương sai do nhiễu mô phỏng (Within / R)** | $5.723 \times 10^{-6}$ | - | Sai số Monte Carlo |
| **Phương sai do bất định tham số (Between)** | $8.976 \times 10^{-5}$ | - | Bất định từ việc ước lượng tham số |
| **Tỉ lệ phương sai do bất định tham số** | **94.01%** | - | **Bất định tham số chi phối** |
| **Tỉ lệ phương sai do nhiễu mô phỏng** | **5.99%** | - | Với $R=60$, nhiễu mô phỏng khoảng 6% |
| **Xác suất SL toàn ngày $\ge 90\%$** | **100.0%** | [92.87%, 100.0%] | 50/50 bộ bootstrap đạt chuẩn toàn ngày |
| **Xác suất SL giờ tệ nhất $\ge 90\%$** | **90.0%** | [78.64%, 95.65%] | 45/50 bộ bootstrap đạt chuẩn giờ tệ nhất |

---

## 4. BẢNG SO SÁNH CÁC CHÍNH SÁCH PHỤC VỤ (DANH ĐỊNH & BIẾN ĐỘNG NGÀY)

### 4.1 Đánh giá danh định (300 lần lặp, CI95)

Dữ liệu tại `results/final_v4/so_sanh_chinh_sach.csv` (seed đánh giá `50000`, tách khỏi seed chọn lịch):

| Chính sách phục vụ | Lịch quầy theo giờ | Quầy-giờ | $SL$ Toàn ngày (CI95) | $SL$ Giờ tệ nhất (Low CI95) | $SL_{\text{vip}}$ | Tỉ lệ bỏ về $p_{ab}$ | Thời gian chờ $W_q$ (phút) | Hiệu suất quầy $\rho$ | Đạt SLA? |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Mốc cơ sở 6 quầy** | `[6, 6, 6, 6, 6, 6, 6, 6, 6]` | 54 | 0.9763 ± 0.0012 | 0.9494 (H2) | 0.9822 | 2.17% ± 0.10% | 0.2024 ± 0.0091 | 60.77% ± 0.37% | **ĐẠT** |
| **SIPP (Erlang C)** | `[4, 6, 6, 6, 5, 5, 5, 5, 5]` | 47 | 0.9530 ± 0.0019 | 0.9276 (H6) | 0.9635 | 4.10% ± 0.14% | 0.3807 ± 0.0131 | 68.47% ± 0.39% | **ĐẠT** |
| **SIPP (Erlang-A)** | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | 44 | 0.9369 ± 0.0023 | 0.9044 (H8) | 0.9510 | 5.43% ± 0.17% | 0.5017 ± 0.0158 | 72.10% ± 0.39% | Sát ngưỡng |
| **Tối ưu mô phỏng (45 q-h)** | `[4, 5, 6, 5, 5, 5, 5, 5, 5]` | **45** | **0.9423 ± 0.0022** | **0.9236 (H3)** | **0.9558** | **4.99% ± 0.16%** | **0.4628 ± 0.0150** | **70.85% ± 0.39%** | **ĐẠT** |
| **Bền vững (+10% nhu cầu)** | `[4, 6, 6, 6, 5, 5, 6, 5, 5]` | 48 | 0.9579 ± 0.0017 | 0.9327 (H7) | 0.9674 | 3.70% ± 0.13% | 0.3432 ± 0.0123 | 67.33% ± 0.39% | **ĐẠT** |
| **Theo ca 8h (MILP, nghỉ 11h–14h)** | `[8, 8, 8, 6, 5, 5, 8, 8, 8]` | 64 | 0.9842 ± 0.0010 | 0.9462 (H4) | 0.9873 | 1.41% ± 0.08% | 0.1344 ± 0.0076 | 51.69% ± 0.32% | **ĐẠT** |

> **Lịch Erlang-A 44 q-h "sát ngưỡng":** với seed đánh giá (300 lần lặp), cận dưới giờ 16h–17h là 0.9044, vừa trên 90%; với seed chọn lịch (60 lần lặp, bước 0 mục 3.2) là 0.8893, dưới 90%. Hai bộ seed cho kết luận ngược nhau, tức lịch 44 nằm đúng tại ranh giới. Thuật toán chọn lịch trên bộ seed riêng rồi đánh giá trên bộ khác để tránh thiên lệch chọn lựa (M5), và giữ 45 q-h.

---

### 4.2 Chỉ số kỳ vọng có điều kiện và Độ nhạy $CV_{\text{ngày}}$ (S2, S3)

Mô phỏng $K$ kịch bản ngày $\times R$ lần lặp để tính chỉ số kỳ vọng $E_h(m) = E[SL_h \mid m]$, tách rời nhiễu lấy mẫu (`results/final_v4/chi_so_ky_vong_dieu_kien.csv`, dòng chuẩn $K=200, R=30$, $CV = 14.0\%$ ước lượng trên train; `results/final_v4/do_nhay_cv_ngay.csv`, $K=100, R=20$):

| Chính sách | CV ngày | $P(E_{day} \ge 90\%)$ [Wilson 95%] | $P(\min_h E_h \ge 90\%)$ [Wilson 95%] | Số giờ $E_h < 90\%$ TB | $P(\text{thực tế mọi giờ} \ge 90\%)$ | $P(\text{gộp tháng 20 ngày} \ge 90\%)$ |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Lịch 45** | **14.0% (Chuẩn)** | **88.0% [82.8%, 91.8%]** | **73.0% [66.5%, 78.7%]** | **1.09** | **29.0% [27.8%, 30.1%]** | **65.0% [59.4%, 70.2%]** |
|  | 8.0% | 97.0% [91.5%, 99.0%] | 77.0% [67.8%, 84.2%] | 0.44 | 22.4% [20.6%, 24.3%] | 73.0% [63.6%, 80.7%] |
|  | 12.0% | 94.0% [87.5%, 97.2%] | 75.0% [65.7%, 82.5%] | 0.72 | 25.8% [23.9%, 27.7%] | 71.0% [61.5%, 79.0%] |
|  | 16.0% | 86.0% [77.9%, 91.5%] | 63.0% [53.2%, 71.8%] | 1.40 | 30.3% [28.3%, 32.4%] | 59.0% [49.2%, 68.1%] |
|  | 20.0% | 79.0% [70.0%, 85.8%] | 63.0% [53.2%, 71.8%] | 1.68 | 31.9% [29.9%, 34.0%] | 61.0% [51.2%, 70.0%] |
| **Lịch 48** | **14.0% (Chuẩn)** | **96.0% [92.3%, 98.0%]** | **83.5% [77.7%, 88.0%]** | **0.51** | **43.9% [42.7%, 45.2%]** | **78.3% [73.3%, 82.6%]** |
|  | 8.0% | 99.0% [94.6%, 99.8%] | 92.0% [85.0%, 95.9%] | 0.11 | 41.6% [39.4%, 43.7%] | 90.0% [82.6%, 94.5%] |
|  | 12.0% | 98.0% [93.0%, 99.4%] | 90.0% [82.6%, 94.5%] | 0.23 | 41.6% [39.4%, 43.7%] | 88.0% [80.2%, 93.0%] |
|  | 16.0% | 94.0% [87.5%, 97.2%] | 76.0% [66.8%, 83.3%] | 0.62 | 43.1% [40.9%, 45.2%] | 74.0% [64.6%, 81.6%] |
|  | 20.0% | 90.0% [82.6%, 94.5%] | 73.0% [63.6%, 80.7%] | 0.99 | 43.3% [41.1%, 45.4%] | 72.0% [62.5%, 79.9%] |
| **Mốc 54** | **14.0% (Chuẩn)** | **99.5% [97.2%, 99.9%]** | **93.5% [89.2%, 96.2%]** | **0.10** | **71.8% [70.6%, 72.9%]** | **92.7% [89.1%, 95.1%]** |
|  | 8.0% | 100.0% [96.3%, 100.0%] | 100.0% [96.3%, 100.0%] | 0.00 | 76.3% [74.3%, 78.1%] | 99.0% [94.6%, 99.8%] |
|  | 12.0% | 100.0% [96.3%, 100.0%] | 97.0% [91.5%, 99.0%] | 0.03 | 73.2% [71.2%, 75.1%] | 97.0% [91.5%, 99.0%] |
|  | 16.0% | 99.0% [94.6%, 99.8%] | 92.0% [85.0%, 95.9%] | 0.13 | 69.5% [67.4%, 71.5%] | 90.0% [82.6%, 94.5%] |
|  | 20.0% | 96.0% [90.2%, 98.4%] | 86.0% [77.9%, 91.5%] | 0.34 | 67.4% [65.3%, 69.4%] | 85.0% [76.7%, 90.7%] |

> **Lưu ý thống kê:** khoảng Wilson của cột $P(\text{thực tế mọi giờ})$ coi mọi ngày-lần lặp là độc lập (dòng chuẩn: 200 × 30 = 6.000; dòng độ nhạy: 100 × 20 = 2.000). Các lần lặp trong cùng một kịch bản có tương quan, nên khoảng này **hẹp hơn thực tế**. Cột này tăng nhẹ theo CV ở Lịch 45 (22.4% → 31.9%) là do định nghĩa "mọi giờ thực tế" bị chi phối bởi nhiễu nhị thức của từng giờ, không nên diễn giải như xu hướng.

Mô phỏng 300 lần lặp có hệ số nhân ngày ($CV = 14.0\%$, `so_sanh_chinh_sach_bd.csv`): Lịch 45 có SL ngày TB 0.9370, $P(SL_{\text{ngày}} \ge 90\%) = 85.7\%$, phân vị 5% của SL ngày là 0.867; Lịch 48: 0.9542, 95.0%, 0.901; Mốc 54: 0.9734, 99.7%, 0.938.

---

### 4.3 Posterior Predictive Check mô hình nhu cầu ngày (S3)

Kiểm tra qua 1.000 bộ 14 ngày mô phỏng từ mô hình $m_d \sim \text{Gamma}$ với $CV = 14.0\%$ (`results/final_v4/posterior_predictive_check.csv`):

| Khung giờ | $D$ quan sát thực tế | $D$ kỳ vọng mô hình | CI 95% mô phỏng [$2.5\%, 97.5\%$] | Posterior Predictive $p$-value | Đánh giá mô hình |
|:---:|:---:|:---:|:---:|:---:|---|
| **8h - 9h** | 23.55 | 29.20 | [11.43, 56.02] | 0.656 | Phù hợp |
| **9h - 10h** | 23.58 | 35.89 | [12.86, 70.23] | 0.794 | Phù hợp |
| **10h - 11h** | 48.77 | 38.66 | [16.73, 72.82] | 0.217 | Phù hợp |
| **11h - 12h** | 39.15 | 35.71 | [13.79, 66.66] | 0.351 | Phù hợp |
| **12h - 13h** | 20.83 | 32.84 | [11.99, 62.80] | 0.832 | Phù hợp |
| **13h - 14h** | 30.73 | 32.35 | [12.55, 59.90] | 0.493 | Phù hợp |
| **14h - 15h** | 38.08 | 33.68 | [12.42, 62.87] | 0.327 | Phù hợp |
| **15h - 16h** | 33.61 | 33.52 | [12.27, 66.65] | 0.440 | Phù hợp |
| **16h - 17h** | 26.61 | 29.74 | [11.48, 58.19] | 0.541 | Phù hợp |
| **Tổng cả ngày** | **140.38** | **197.31** | **[77.48, 381.68]** | **0.760** | **Phù hợp** |

Với $CV = 14.0\%$ (train), $D$ kỳ vọng của mô hình lớn hơn giá trị quan sát trên 14 ngày (197 so với 140) nhưng quan sát vẫn nằm trong CI95 ở mọi giờ. Mô hình hơi bi quan về biến động ngày so với 14 ngày quan sát.

---

### 4.4 Phân tích ngưỡng lưu lượng $V^*$ và Bộ dự báo sớm (S4)

1. **Khảo sát ngưỡng lưu lượng** (`results/final_v4/nguong_luu_luong_chi_tiet.csv`, 40 lần lặp mỗi mức):  
   Lịch 45 giữ $SL_{\text{ngày}} \ge 90\%$ đến $V = 800$ khách/ngày (SL 0.9018) và hụt ở $V = 850$ (0.8703). Nội suy tuyến tính cho **$V^* = 803$ khách/ngày**. Lịch 48 vẫn đạt ở 850 (0.9045).
2. **Bộ dự báo OLS sớm lúc 10h (từ số khách 8h–10h)** (`du_bao_som_hoi_quy.csv`):  
   $$\hat{V} = 189.6 + 3.49 \cdot (N_{8h-9h} + N_{9h-10h})$$  
   Pearson $r = 0.842$ ($p = 0.0002$), $R^2 = 0.708$, RMSE trong mẫu $= 45.3$ khách. Phương trình fit trên cả 14 ngày. Khi fit lại chỉ trên 10 ngày train ($\hat{V} = 90.9 + 4.20 \cdot N_{8-10h}$, $r = 0.907$), RMSE trên 4 ngày test là 63.9 khách; leave-one-out trên 14 ngày cho RMSE 55.0 khách (phân tích bổ sung từ V3, chỉ phụ thuộc dữ liệu).
3. **Chính sách ghép trên 14 ngày thực tế** ($\hat{V} > 803$ → Lịch 48, ngược lại Lịch 45; `danh_gia_chinh_sach_du_bao_14ngay.csv`):
   - Số ngày dùng Lịch 45: **13/14** (chỉ ngày 13, $\hat{V} = 820.6$, chuyển sang Lịch 48).
   - Quầy-giờ trung bình: **45.21 quầy-giờ/ngày**, tiết kiệm 16.27% so với 54.
   - **Bộ dự báo bỏ lỡ đúng hai ngày hụt SLA:** ngày 2 ($V = 826$, $\hat{V} = 754.4$) và ngày 7 ($V = 820$, $\hat{V} = 754.4$) vượt $V^*$ nhưng dự báo thấp hơn khoảng 70 khách. Ngày 13 được chuyển sang Lịch 48 dù $V$ thực tế chỉ 728. Với sai số dự báo 45–64 khách so với khoảng cách $V^* - \bar{V} \approx 116$, quy tắc này có tác dụng hạn chế.

---

### 4.5 Đối chiếu 14 ngày thực tế phân định Train/Test (S7)

Mô phỏng 40 lần lặp/ngày với $m_d = N_d / 686.7$, Student-t CI ($df=39$) tại `results/final_v4/theo_14_ngay.csv` và `theo_14_ngay_tong_hop.csv`:

| Ngày ID | Phân tập | Tổng khách | $SL$ Lịch 45 | CI 95% Lịch 45 | Đạt? | $SL$ Lịch 48 | CI 95% Lịch 48 | Đạt? | $SL$ Mốc 6 quầy | Đạt? |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | Train | 690 | 0.9397 | [0.934, 0.946] | **Đạt** | 0.9554 | [0.950, 0.961] | **Đạt** | 0.9743 | **Đạt** |
| 1 | Train | 776 | 0.9088 | [0.902, 0.915] | **Đạt** | 0.9322 | [0.925, 0.940] | **Đạt** | 0.9609 | **Đạt** |
| 2 | Train | 826 | 0.8766 | [0.867, 0.886] | Hụt | 0.9167 | [0.910, 0.924] | **Đạt** | 0.9509 | **Đạt** |
| 3 | Train | 634 | 0.9580 | [0.953, 0.963] | **Đạt** | 0.9696 | [0.966, 0.973] | **Đạt** | 0.9839 | **Đạt** |
| 4 | Train | 580 | 0.9666 | [0.961, 0.972] | **Đạt** | 0.9797 | [0.976, 0.983] | **Đạt** | 0.9882 | **Đạt** |
| 5 | Train | 600 | 0.9639 | [0.958, 0.970] | **Đạt** | 0.9774 | [0.974, 0.981] | **Đạt** | 0.9865 | **Đạt** |
| 6 | Train | 539 | 0.9748 | [0.971, 0.978] | **Đạt** | 0.9834 | [0.980, 0.987] | **Đạt** | 0.9901 | **Đạt** |
| 7 | Train | 820 | 0.8836 | [0.874, 0.893] | Hụt | 0.9100 | [0.900, 0.920] | **Đạt** | 0.9526 | **Đạt** |
| 8 | Train | 715 | 0.9304 | [0.921, 0.939] | **Đạt** | 0.9539 | [0.950, 0.958] | **Đạt** | 0.9729 | **Đạt** |
| 9 | Train | 687 | 0.9408 | [0.932, 0.949] | **Đạt** | 0.9546 | [0.948, 0.961] | **Đạt** | 0.9773 | **Đạt** |
| 10 | Test | 740 | 0.9264 | [0.918, 0.935] | **Đạt** | 0.9447 | [0.938, 0.951] | **Đạt** | 0.9646 | **Đạt** |
| 11 | Test | 748 | 0.9238 | [0.915, 0.932] | **Đạt** | 0.9427 | [0.938, 0.948] | **Đạt** | 0.9641 | **Đạt** |
| 12 | Test | 753 | 0.9268 | [0.920, 0.934] | **Đạt** | 0.9406 | [0.934, 0.948] | **Đạt** | 0.9614 | **Đạt** |
| 13 | Test | 728 | 0.9248 | [0.918, 0.932] | **Đạt** | 0.9507 | [0.945, 0.956] | **Đạt** | 0.9680 | **Đạt** |
| **Tổng kết** | - | **TB 702.6** | **12/14 ngày (85.7%)** | **Wilson 95%: [60.1%, 96.0%]** | - | **14/14 ngày (100.0%)** | **Wilson 95%: [78.5%, 100.0%]** | - | **14/14 ngày (100.0%)** | **Wilson 95%: [78.5%, 100.0%]** |

---

## 5. ĐÁNH GIÁ NGOÀI MẪU VỚI KHOẢNG DỰ BÁO 95% (PI95) VÀ HOLM-BONFERRONI (S6, M4)

So sánh mô phỏng Lịch 45 (1.000 bộ 4 ngày có biến động lưu lượng ngày) với quan sát thực tế tập Test (4 ngày, $2.969$ khách), tại `results/final_v4/ngoai_mau.csv`:

| Khung giờ | Quầy | SL mô phỏng TB | PI95 Low | PI95 High | SL thực tế quan sát | Thực tế Wilson 95% | Trong PI95? | Holm $p_{\text{adj}}$ | Khác biệt có ý nghĩa? |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h - 9h** | 4 | 0.9359 | 0.8523 | 0.9893 | **0.9809** | [0.9561, 0.9918] | **Có** | 0.0176 | **Có (Thực tế tốt hơn)** |
| **9h - 10h** | 5 | 0.9187 | 0.8231 | 0.9802 | **0.9735** | [0.9520, 0.9856] | **Có** | 0.0008 | **Có (Thực tế tốt hơn)** |
| **10h - 11h** | 6 | 0.9449 | 0.8660 | 0.9871 | 0.9283 | [0.9010, 0.9485] | **Có** | 0.2350 | Không |
| **11h - 12h** | 5 | 0.9076 | 0.7989 | 0.9727 | 0.9413 | [0.9128, 0.9609] | **Có** | 0.1197 | Không |
| **12h - 13h** | 5 | 0.9361 | 0.8508 | 0.9863 | **0.9865** | [0.9659, 0.9948] | Không | 0.0027 | **Có (Thực tế tốt hơn)** |
| **13h - 14h** | 5 | 0.9475 | 0.8690 | 0.9891 | 0.9443 | [0.9136, 0.9645] | **Có** | 0.7939 | Không |
| **14h - 15h** | 5 | 0.9229 | 0.8236 | 0.9826 | 0.8958 | [0.8566, 0.9252] | **Có** | 0.2242 | Không |
| **15h - 16h** | 5 | 0.9252 | 0.8278 | 0.9820 | **0.7647** | [0.7141, 0.8088] | Không | 0.0000 | **Có (Thực tế giảm mạnh)** |
| **16h - 17h** | 5 | 0.9642 | 0.9046 | 0.9959 | 0.9387 | [0.9028, 0.9619] | **Có** | 0.1197 | Không |

7/9 giờ có SL thực tế nằm trong PI95. Ba giờ thực tế tốt hơn mô phỏng có ý nghĩa (8h, 9h, 12h), phù hợp với việc ngân hàng thực có nhiều người phục vụ hơn lịch (xem dưới). Riêng 15h–16h thực tế kém hơn nhiều.

> [!NOTE]
> **Kết luận điều tra 15h–16h (M4, `dieu_tra_15h_16h.csv`, chi tiết `docs/ngoai_mau.md` mục 5):**  
> Bất thường tập trung ở **một ngày (ngày 10)**: SL 15h–16h chỉ 31.5%, bỏ về 39.3%. Ba ngày test còn lại có SL 93.2%, 97.5%, 93.7%, khớp mô phỏng. Ngày 10 có λ cao hơn train 13% và $E[S]$ cao hơn 29% (4.14 so với 3.21 phút), nên tải đề nghị $a = 6.14$ Erlang, cao nhất trong 14 ngày (13 ngày còn lại: 2.88–5.33). Số phiên phục vụ chồng lấn trung bình trong giờ đó chỉ 3.67, tức nhân sự hiệu dụng khoảng 4 người. Đây là ngày nhu cầu cao gặp nhân sự hiệu dụng thấp, không phải sai lệch của mô hình. Hệ quả vận hành: cần cơ chế tăng cường quầy trong ngày khi thời gian phục vụ hoặc hàng chờ tăng bất thường.

---

## 6. TỐI ƯU HÓA LỊCH CA LÀM VIỆC THỰC TẾ (MILP)

Bài toán quy hoạch nguyên trong `b_shifts.py` (solver HiGHS) cho yêu cầu Lịch 45 `[4, 5, 6, 5, 5, 5, 5, 5, 5]`, kết quả tại `results/final_v4/lich_theo_ca.csv`:

| Mô hình & Phương án ca | Mẫu phủ quầy theo giờ | Quầy-giờ làm việc | Giờ tại chỗ | Nhân sự | Dư so với 45 q-h |
|---|:---:|:---:|:---:|:---:|:---:|
| **Mô hình B (nghỉ 11h–14h): hỗn hợp 8h + 4h** | `[5, 5, 6, 5, 5, 5, 6, 6, 5]` | **48** | 53 | **7 NV** (5 ca 8h + 2 ca 4h) | **+3 q-h (+6.7%)** |
| **Mô hình B (nghỉ 11h–14h): hỗn hợp, bắt buộc phủ đúng** | - | - | - | - | **Vô nghiệm** |
| **Mô hình B (nghỉ 9h–16h): chỉ ca 8h** | `[6, 5, 6, 5, 5, 5, 5, 5, 6]` | 48 | 54 | 6 NV ca 8h | +3 q-h (+6.7%) |
| **Mô hình B (nghỉ 11h–14h): chỉ ca 8h** | `[8, 8, 8, 6, 5, 5, 8, 8, 8]` | 64 | 72 | 8 NV ca 8h | +19 q-h (+42.2%) |
| **Chỉ ca 4h** | `[4, 9, 9, 9, 5, 5, 5, 5, 5]` | 56 | 56 | 14 lượt ca 4h | +11 q-h (+24.4%) |
| **Mô hình A: chỉ ca 8h liên tục** | `[4, 9, 9, 9, 9, 9, 9, 9, 5]` | 72 | 72 | 9 NV ca 8h | +27 q-h (+60.0%) |

**Bổ sung** (cùng hàm `solve_shift_scheduling`, mô hình B nghỉ 11h–14h, hỗn hợp 8h + 4h; chưa nằm trong pipeline):

| Yêu cầu | Mẫu phủ | Quầy-giờ làm việc | Giờ tại chỗ | Nhân sự | Dư |
|---|:---:|:---:|:---:|:---:|:---:|
| Lịch 48 `[4, 6, 6, 6, 5, 5, 6, 5, 5]` | phủ đúng | 48 | 52 | 8 NV (4 ca 8h + 4 ca 4h) | 0 |
| Mốc 54 `[6, 6, 6, 6, 6, 6, 6, 6, 6]` | `[6, 6, 6, 6, 6, 6, 8, 6, 6]` | 56 | 62 | 8 NV (6 ca 8h + 2 ca 4h) | +2 |

Lịch 45 thêm 1 quầy ở 16h–17h so với Lịch 44 của V3. Với ca 4h buổi chiều kết thúc lúc 17h và nghỉ trưa 11h–14h, mẫu `[..., 5, 5, 5, 5, 5]` không còn phủ đúng được (V3: Lịch 44 phủ đúng bằng 4 ca 8h + 3 ca 4h). Hệ quả: tính theo giờ công, Lịch 45 và Lịch 48 cùng chi phí 48 q-h (mục 1).

---

## 7. PHÂN TÍCH ĐỘ NHẠY VÀ ĐÁNH ĐỔI KINH TẾ

### 7.1 Độ nhạy toàn diện hệ thống (Tải, Thời gian phục vụ, Kiên nhẫn)

Mô phỏng với số ngẫu nhiên chung (CRN) tại `results/final_v4/do_nhay.csv`:

| Yếu tố biến động | Hệ số nhân | Lịch 45 $SL$ | Giờ tệ nhất (Low CI95) | Lịch 48 $SL$ | Giờ tệ nhất (Low CI95) | Mốc 6 quầy $SL$ |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Nhu cầu đến ($\lambda$)** | 0.9 (-10%) | 0.9618 | 0.9441 | 0.9724 | 0.9513 | 0.9857 |
| | **1.0 (Chuẩn)** | **0.9427** | **0.9180** | **0.9584** | **0.9330** | **0.9762** |
| | **1.1 (+10%)** | **0.9200** | **0.8793 (< 90%)** | **0.9423** | **0.9087 ($\ge$ 90%)** | **0.9654** |
| | 1.2 (+20%) | 0.8850 | 0.8337 | 0.9145 | 0.8512 | 0.9488 |
| | 1.3 (+30%) | 0.8575 | 0.8020 | 0.8940 | 0.8458 | 0.9331 |
| **Thời gian phục vụ ($E[S]$)** | 1.0 (Chuẩn) | 0.9427 | 0.9180 | 0.9584 | 0.9330 | - |
| | 1.1 (+10%) | 0.9138 | 0.8788 | 0.9362 | 0.8958 | - |
| | 1.2 (+20%) | 0.8767 | 0.8331 | 0.9072 | 0.8572 | - |
| **Tốc độ bỏ về ($\theta$)** | 0.5 (Kiên nhẫn gấp đôi) | 0.9480 | 0.9206 | 0.9652 | 0.9296 | - |
| | 1.0 (Chuẩn) | 0.9427 | 0.9180 | 0.9584 | 0.9330 | - |
| | 1.5 (Mất kiên nhẫn hơn) | 0.9353 | 0.9109 | 0.9519 | 0.9245 | - |

Lịch 45 chịu được nhu cầu tăng dưới 10%; Lịch 48 chịu được +10% nhu cầu nhưng không chịu được +10% thời gian phục vụ (giờ tệ nhất 0.8958).

---

### 7.2 Độ nhạy phân phối phục vụ kèm giờ tệ nhất (S9, M3)

Mô phỏng Lịch 45 với 150 lần lặp, cùng bộ seed (CRN), hiệu số theo cặp so với mô hình chính (thực nghiệm), tại `results/final_v4/do_nhay_phan_phoi.csv`:

| Phân phối phục vụ | $SL$ Toàn ngày (CI95) | Giờ tệ nhất | $SL$ Giờ tệ nhất | Giờ tệ nhất Low CI95 | Hiệu số so với thực nghiệm | CI 95% Hiệu số | Khác biệt có ý nghĩa? |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Thực nghiệm (mô hình chính, $cs^2 = 1.20$)** | **0.9435 ± 0.0030** | 14h - 15h | 0.9277 | **0.9182** | Gốc (0.0000) | - | - |
| **Gamma (AIC tốt nhất, $cs^2 = 0.91$)** | 0.9430 ± 0.0028 | 11h - 12h | 0.9201 | **0.9099** | -0.0005 | [-0.0043, +0.0034] | Không |
| **Exponential ($cs^2 = 1.00$)** | 0.9453 ± 0.0028 | 11h - 12h | 0.9268 | **0.9176** | +0.0017 | [-0.0023, +0.0058] | Không |
| **Lognormal ($cv$ + 20%)** | 0.9344 ± 0.0039 | 11h - 12h | 0.9111 | **0.8979** | **-0.0091** | **[-0.0140, -0.0042]** | **Có** (giờ tệ nhất < 90%) |

Đối chiếu M3 với 300 lần lặp, seed đánh giá (`m3_dich_vu_thuc_nghiem.csv`): cùng Lịch 45, phục vụ thực nghiệm cho SL 0.9423, Gamma cho 0.9443 (Gamma lạc quan hơn 0.0020). Nếu tối ưu với phục vụ Gamma, lịch tìm được là Lịch 44 của V3; Lịch 44 đánh giá bằng phục vụ thực nghiệm có giờ tệ nhất cận dưới 0.9044 (sát ngưỡng).

---

### 7.3 Đường cong đánh đổi Pareto và Hàm chi phí với truyền sai số (S11)

Hàm chi phí $C(k) = \text{Quầy-giờ} + k \cdot N \cdot p_{ab}$ với $N = 686.7$ khách/ngày, CI truyền sai số từ $p_{ab}$ và hiệu số theo cặp $\Delta C = C_{45} - C_{48}$ (`results/final_v4/chi_phi.csv`; chạy riêng 150 lần lặp, seed 70000, nên $p_{ab}$ hơi khác bảng 4.1):

| Hệ số $k$ | Chi phí Lịch 45 (CI95) | Chi phí Lịch 48 (CI95) | Chi phí Mốc 6 quầy (CI95) | Hiệu số $C_{45} - C_{48}$ | CI 95% Hiệu số | Có ý nghĩa? | Chính sách kinh tế nhất |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **$k = 0.10$** | **$48.43 \pm 0.16$** | $50.54 \pm 0.12$ | $55.50 \pm 0.09$ | **-2.10** | **[-2.17, -2.03]** | **Có** | **Lịch tối ưu 45** |
| **$k = 0.25$** | **$53.59 \pm 0.39$** | $54.34 \pm 0.30$ | $57.76 \pm 0.24$ | **-0.75** | **[-0.93, -0.58]** | **Có** | **Lịch tối ưu 45** |
| **$k = 0.50$** | $62.17 \pm 0.78$ | **$60.68 \pm 0.60$** | $61.51 \pm 0.47$ | **+1.49** | **[+1.14, +1.84]** | **Có** | **Lịch bền vững 48** |
| **$k = 1.00$** | $79.35 \pm 1.56$ | $73.36 \pm 1.20$ | **$69.03 \pm 0.94$** | **+5.99** | **[+5.29, +6.69]** | **Có** | Mốc 6 quầy |
| **$k = 2.00$** | $113.70 \pm 3.12$ | $98.72 \pm 2.40$ | **$84.06 \pm 1.89$** | **+14.97** | **[+13.58, +16.37]** | **Có** | Mốc 6 quầy |

> **Điểm hòa vốn** (từ $p_{ab}$ trung bình: 5.00% / 3.69% / 2.19%): Lịch 45 rẻ nhất khi $k < 0.33$; Lịch 48 rẻ nhất khi $0.33 < k < 0.58$; **Mốc 6 quầy rẻ nhất khi $k > 0.58$**, tức khi chi phí mất một khách lớn hơn khoảng 0.58 quầy-giờ. Việc chọn Lịch 45 phụ thuộc vào giả định $k$ nhỏ. Hàm chi phí tính theo quầy-giờ mở; nếu tính theo giờ công ca làm việc thì Lịch 45 và 48 cùng 48 q-h (mục 6) và Lịch 48 rẻ hơn ở mọi $k > 0$.

---

### 7.4 Khảo sát Pha 3 vét cạn 117 cấu hình (C6)

Để kiểm tra tính tối thiểu cục bộ của Lịch 45, 117 cấu hình lân cận được **mô phỏng bằng SimPy** (60 lần lặp, cùng tiêu chí cận dưới CI95 $\ge 90\%$ như pha 1–2) và ghi tại `results/final_v4/pha3.csv`:
- **72 phép hoán đổi 1 quầy:** bớt 1 quầy ở giờ $i$, thêm vào giờ $j$ (tổng vẫn 45). Cận dưới giờ tệ nhất từ 0.7820 đến 0.8937; tất cả vi phạm.
- **45 phép giảm 2 quầy** (tổng còn 43): 36 cặp giờ khác nhau và 9 trường hợp giảm 2 quầy cùng giờ. Cận dưới giờ tệ nhất từ 0.5749 đến 0.8848; tất cả vi phạm.
- **Kết luận:** **0/117 cấu hình** lân cận khả thi. Cùng với 9 phép bớt 1 quầy ở pha 2 (mục 3.2), Lịch 45 là **tối thiểu cục bộ** theo tiêu chí mô phỏng. V3 kiểm tra pha 3 bằng công thức Erlang-A; V4 dùng mô phỏng nên kết luận nhất quán với tiêu chí chọn lịch. Đây chưa phải chứng minh tối ưu trên toàn bộ không gian lịch.

---

### 7.5 Kịch bản kiên nhẫn của khách quầy giao dịch (M1)

Dữ liệu là tổng đài, khách quầy giao dịch có thể kiên nhẫn hơn. Chạy lại thuật toán tối ưu với kiên nhẫn trung bình từ 9.2 phút (ước lượng) đến vô cùng (`results/final_v4/do_nhay_kien_nhan.csv`, đánh giá 300 lần lặp):

| Kiên nhẫn TB | $\theta$ | Lịch tối ưu mô phỏng | Quầy-giờ | SIPP Erlang-A | $SL$ ngày | Giờ tệ nhất Low CI95 | $p_{ab}$ | $W_q$ (phút) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **9.2 phút (ước lượng)** | 0.1087 | `[4, 5, 6, 5, 5, 5, 5, 5, 5]` | **45** | 44 | 0.9423 | 0.9236 | 4.99% | 0.4628 |
| 15 phút | 0.0667 | `[4, 6, 6, 5, 5, 5, 5, 5, 5]` | **46** | 44 | 0.9517 | 0.9243 | 3.43% | 0.5195 |
| 20 phút | 0.0500 | `[4, 6, 6, 5, 5, 5, 5, 5, 5]` | **46** | 44 | 0.9527 | 0.9228 | 2.87% | 0.5781 |
| 30 phút | 0.0333 | `[4, 6, 6, 5, 5, 5, 5, 5, 5]` | **46** | 44 | 0.9526 | 0.9172 | 2.18% | 0.6543 |
| 60 phút | 0.0167 | `[4, 6, 6, 5, 5, 5, 5, 5, 5]` | **46** | 44 | 0.9498 | 0.9061 | 1.31% | 0.7771 |
| **Vô cùng (không bỏ về)** | 0 | `[4, 6, 6, 6, 5, 5, 5, 6, 5]` | **48** | 47 (Erlang C) | 0.9605 | 0.9099 | 0.00% | 0.7301 |

Khi khách kiên nhẫn hơn, ít người bỏ về nên hàng dài hơn và cần thêm quầy: 46 quầy-giờ cho kiên nhẫn 15–60 phút, 48 quầy-giờ khi không ai bỏ về. Đây là khoảng 45–48 q-h trong câu kết luận ở mục 1.

---

### 7.6 Ràng buộc tỉ lệ bỏ về (M2)

Thêm ràng buộc $p_{ab} \le$ ngưỡng vào thuật toán tối ưu (`results/final_v4/toi_uu_rang_buoc_bo_ve.csv`, 300 lần lặp):

| Ràng buộc | Lịch tối ưu | Quầy-giờ | $SL$ ngày | Giờ tệ nhất Low CI95 | $p_{ab}$ | $W_q$ (phút) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Chỉ SL** | `[4, 5, 6, 5, 5, 5, 5, 5, 5]` | **45** | 0.9423 | 0.9236 | 4.99% | 0.4628 |
| **SL + $p_{ab} \le 5\%$** | `[4, 6, 6, 5, 5, 5, 5, 5, 5]` | **46** | 0.9474 | 0.9236 | 4.55% | 0.4239 |
| **SL + $p_{ab} \le 3\%$** | `[5, 6, 6, 6, 6, 5, 6, 6, 5]` | **51** | 0.9698 | 0.9494 | 2.72% | 0.2532 |
| **SL + $p_{ab} \le 2\%$** | `[5, 7, 7, 6, 6, 6, 6, 6, 6]` | **55** | 0.9810 | 0.9705 | 1.77% | 0.1655 |

Lịch 45 có $p_{ab} = 4.99\%$, sát ngưỡng 5%. Khi chỉ đặt chỉ tiêu SL, mô hình Erlang-A "tiết kiệm" quầy một phần nhờ khách bỏ về. Hạ tỉ lệ bỏ về xuống 3% cần thêm 6 quầy-giờ, xuống 2% cần 55 quầy-giờ, nhiều hơn mốc 6 quầy.

---

### 7.7 Ổn định giờ tệ nhất và số lần lặp cần thiết (M5)

Số lần lặp $R$ cần để nửa độ rộng CI95 của SL mỗi giờ $\le 0.003$ (`so_lan_lap_can_thiet.csv`): Lịch 45 cần tối đa 1.646 lần (giờ 11h–12h), Lịch 48 cần tối đa 1.489 lần (giờ 8h–9h). Chạy với đúng số lần đó (`gio_te_nhat.csv`):

| Chính sách | Giờ tệ nhất | $SL$ TB (CI95) | Cận dưới CI95 | $P$(là giờ tệ nhất), bootstrap | $P$(là giờ tệ nhất), theo khối |
|---|:---:|:---:|:---:|:---:|:---:|
| **Lịch 45** (R = 1.646) | **11h–12h** | 0.9247 ± 0.0031 | 0.9216 | 99.7% | 74.1% (27 khối) |
| **Lịch 48** (R = 1.489) | **15h–16h** | 0.9415 ± 0.0027 | 0.9389 | 88.2% | 58.3% (24 khối) |

V3 báo giờ tệ nhất của Lịch 44 đổi giữa 11h–12h (H3) và 16h–17h (H8) tùy lần chạy. Với Lịch 45, giờ 16h–17h đã có 5 quầy (SL 0.9707) và giờ tệ nhất ổn định ở 11h–12h.

---

### 7.8 Giả định xả hàng sau 17h (F1)

`doi_chieu_xa_hang.csv` (Lịch 45, 60 lần lặp, cùng seed): giữ số quầy giờ cuối (V4, `keep_last`) cho SL giờ 16h–17h 0.9704; mở hết `c_max` quầy (hành vi V3, `all_open`) cho 0.9706. Chênh lệch 0.0002 cho lịch có 5 quầy giờ cuối. Thay đổi lịch 44 → 45 vì vậy không phải do F1. Nguyên nhân chính là phục vụ thực nghiệm (M3): tối ưu cùng pipeline V4 nhưng phục vụ Gamma vẫn cho Lịch 44 (`lich_khuyen_nghi.json`, khóa `toi_uu_gamma`; xem mục 7.2 và 8).

---

## 8. ĐỐI CHIẾU V3 → V4

Tại `results/final_v4/doi_chieu_v3_v4.csv`:

| Chỉ số | V3 | V4 | Chênh lệch | Nguyên nhân chính |
|---|:---:|:---:|:---:|---|
| Lịch tối ưu | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | `[4, 5, 6, 5, 5, 5, 5, 5, 5]` | +1 quầy ở 16h–17h | F1 + F2, M3, seed/R mới |
| Tổng quầy-giờ lịch tối ưu | 44 | 45 | +1 | như trên |
| Tổng quầy-giờ SIPP Erlang C / Erlang-A | 47 / 44 | 47 / 44 | 0 | Tham số không đổi |
| SL toàn ngày lịch tối ưu | 0.9381 | 0.9423 | +0.0042 | Lịch thêm 1 quầy; M3 |
| SL giờ tệ nhất (cận dưới CI95) | 0.9078 | 0.9236 | +0.0158 | 16h–17h thêm quầy; M5 |
| Giờ tệ nhất | 16h–17h (H8) | 11h–12h (H3) | - | Không ổn định ở V3; ổn định ở V4 (mục 7.7) |
| Tỉ lệ bỏ về lịch tối ưu | 5.35% | 4.99% | -0.36 điểm % | Lịch thêm quầy |
| $W_q$ TB lịch tối ưu (phút) | 0.4908 | 0.4628 | -0.0280 | Lịch thêm quầy |
| Hiệu suất $\rho$ lịch tối ưu | 72.15% | 70.85% | -1.30 điểm % | Lịch thêm quầy; F3 |
| Lịch bền vững (+10%) | `[5, 6, 6, 6, 5, 5, 5, 5, 5]` | `[4, 6, 6, 6, 5, 5, 6, 5, 5]` | cùng 48 q-h | Phân bổ lại 8h → 14h |
| SL toàn ngày lịch bền vững | 0.9582 | 0.9579 | -0.0003 | - |
| $P(SL_{\text{ngày}} \ge 90\%)$ có biến động ngày | 85.0% | 85.7% | +0.7 điểm % | CV ngày ước lượng trên train (14.0%) |
| Số ngày quan sát đạt SLA (/14) | 12 | 12 | 0 | - |
| Ngưỡng lưu lượng $V^*$ | 700 | 803 | +103 | V4 nội suy theo SL ≥ 90%; V3 chọn mức trung bình |
| Ca làm việc lịch tối ưu (nghỉ 11h–14h) | 4 ca 8h + 3 ca 4h, phủ đúng 44 | 5 ca 8h + 2 ca 4h, 48 q-h (dư 3) | +4 q-h công | Lịch 45 không phủ đúng được |
| Pha 3 vét cạn | 0/117 (Erlang-A) | 0/117 (SimPy) | - | C6 dùng mô phỏng |
| Độ nhạy phân phối: Gamma so với mốc | Bootstrap thấp hơn Gamma có ý nghĩa | Không khác biệt có ý nghĩa | - | Mốc so sánh đổi sang thực nghiệm (M3) |

Tách riêng từng nguyên nhân trên cùng lịch và seed: F1 riêng lẻ đổi SL giờ cuối 0.9706 → 0.9704; M3 riêng lẻ đổi SL toàn ngày 0.9443 (Gamma) → 0.9423 (thực nghiệm).

---

## 9. TỔNG KẾT KIỂM THỬ VÀ TRẠNG THÁI BÀN GIAO

1. **Kiểm thử tự động:** **35/35 ca kiểm thử** trong `tests/` chạy thành công trong 64.5 giây (log tại `results/final_v4/pytest_log.txt`). V4 thêm 13 test (T1-a … T1-i), gồm số khách theo giờ của NHPP (F2), xả hàng giữ số quầy giờ cuối (F1), hiệu suất theo thời gian bận (F3).
2. **Pipeline:** `python main.py --stage all` chạy 6 giai đoạn trong 33.3 phút (`thoi_gian_chay.json`); `results/final_v4/MO_TA.md` sinh tự động, liệt kê nguồn của từng tệp.
3. **Kiểm tra nhất quán:** `tools/check_consistency.py` quét thuật ngữ không có căn cứ và đối chiếu số trong các bảng chính của tài liệu này (2.1, 2.2, 2.4, 2.5, 3.1, 4.1, 4.2, 4.5, 5, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6) với `data/clean/data_clean.csv` và CSV trong `results/final_v4/`.

---

## 10. HẠN CHẾ CẦN NÊU KHI BÁO CÁO

1. **Dữ liệu tổng đài, không phải quầy giao dịch:** kiên nhẫn của khách quầy có thể khác. Số quầy cần thiết tăng từ 45 lên 46–48 q-h khi kiên nhẫn dài hơn (mục 7.5).
2. **Phân phối phục vụ:** cả 4 phân phối tham số đều bị KS bác bỏ; mô hình chính dùng phân phối thực nghiệm của train (M3), nên không ngoại suy được đuôi dài hơn dữ liệu đã thấy. Lognormal với cv + 20% làm giờ tệ nhất rơi dưới 90% (mục 7.2).
3. **Kiên nhẫn:** đường Kaplan–Meier lệch khỏi giả định mũ ở vùng chờ ngắn (mục 2.5).
4. **Tỉ lệ bỏ về sát 5%:** Lịch 45 đạt SL một phần nhờ khách bỏ về; giới hạn bỏ về 3% cần 51 q-h (mục 7.6).
5. **Ca làm việc:** Lịch 45 không phủ đúng được bằng ca 8h/4h có nghỉ trưa 11h–14h; tính theo giờ công, nó tốn bằng Lịch 48 (mục 6).
6. **Khoảng Wilson cho xác suất "thực tế mọi giờ"** bỏ qua tương quan trong cùng kịch bản, nên quá hẹp (mục 4.2).
7. **Dự báo sớm** fit trên cả 14 ngày; sai số ngoài mẫu 55–64 khách và bỏ lỡ cả hai ngày hụt SLA (mục 4.4).
8. **Lựa chọn Lịch 45 phụ thuộc chi phí mất khách $k$:** với $k > 0.58$, Mốc 6 quầy rẻ hơn (mục 7.3).
9. **Ngoài mẫu 15h–16h:** do một ngày (ngày 10) có nhu cầu cao gặp nhân sự hiệu dụng thấp; dữ liệu chỉ có hoạt động PS nên số phiên chồng lấn là cận dưới của số nhân viên (mục 5).
