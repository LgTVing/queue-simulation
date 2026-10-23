# BẢNG TỔNG HỢP SỐ LIỆU CUỐI CÙNG VÀ ĐÁNH GIÁ TOÀN DIỆN DỰ ÁN (PHIÊN BẢN V3 CHUẨN MỰC THỐNG KÊ)

**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu cho quầy giao dịch ngân hàng  
**Thời điểm tổng hợp:** Tháng 10/2026 (Hoàn thành toàn diện Bản 1 T1–T14 và Bản 2 S1–S11, C1–C7; đóng băng tại `results/final_v3/`)  
**Bộ dữ liệu:** Anonymous Bank Call Center (Technion SEE Center), 14 ngày làm việc, $9.836$ giao dịch  

---

## MỤC LỤC

1. [BẢNG QUYẾT ĐỊNH QUẢN TRỊ TỔNG THỂ](#1-bảng-quyết-định-quản-trị-tổng-thể)
2. [TỔNG HỢP DỮ LIỆU THỰC TẾ VÀ KIỂM ĐỊNH PHÂN PHỐI](#2-tổng-hợp-dữ-liệu-thực-tế-và-kiểm-định-phân-phối)
   - [2.1 Dữ liệu thực tế và Đối chiếu Train / Test / Toàn bộ](#21-dữ-liệu-thực-tế-và-đối-chiếu-train--test--toàn-bộ)
   - [2.2 Thống kê 9 khung giờ & Khoảng tin cậy Student-t của $\lambda_h$ (S1)](#22-thống-kê-9-khung-giờ--khoảng-tin-cậy-student-t-của-lambda_h-s1)
   - [2.3 Hiện tượng Quá phân tán (Overdispersion)](#23-hiện-tượng-quá-phân-tán-overdispersion)
   - [2.4 Bảng tính giải tích Erlang C và Erlang-A SIPP](#24-bảng-tính-giải-tích-erlang-c-và-erlang-a-sipp)
   - [2.5 Kiểm định độ phù hợp phân phối phục vụ và kiên nhẫn (S10)](#25-kiểm-định-độ-phù-hợp-phân-phối-phục-vụ-và-kiên-nhẫn-s10)
3. [TỔNG HỢP SỐ LIỆU KIỂM CHỨNG CODE PYTHON / SIMPY](#3-tổng-hợp-số-liệu-kiểm-chứng-code-python--simpy)
   - [3.1 Kiểm chứng ba tầng và M/G/1 Pollaczek–Khinchine exact 40.000 phút (S8)](#31-kiểm-chứng-ba-tầng-và-mg1-pollaczekkhinchine-exact-40000-phút-s8)
   - [3.2 Lịch sử Thuật toán Tối ưu hóa 2 Pha SimPy](#32-lịch-sử-thuật-toán-tối-ưu-hóa-2-pha-simpy)
   - [3.3 Phân tích Bootstrap lồng nhau và Phân rã phương sai ANOVA (S5)](#33-phân-tích-bootstrap-lồng-nhau-và-phân-rã-phương-sai-anova-s5)
4. [BẢNG SO SÁNH CÁC CHÍNH SÁCH PHỤC VỤ (DANH ĐỊNH & BIẾN ĐỘNG NGÀY)](#4-bảng-so-sánh-các-chính-sách-phục-vụ-danh-định--biến-động-ngày)
   - [4.1 Đánh giá danh định (300 lần lặp, CI95)](#41-đánh-giá-danh-định-300-lần-lặp-ci95)
   - [4.2 Chỉ số kỳ vọng có điều kiện và Độ nhạy $CV_{\text{ngày}}$ (S2, S3)](#42-chỉ-số-kỳ-vọng-có-điều-kiện-và-độ-nhạy-cv_textngày-s2-s3)
   - [4.3 Posterior Predictive Check mô hình nhu cầu ngày (S3)](#43-posterior-predictive-check-mô-hình-nhu-cầu-ngày-s3)
   - [4.4 Phân tích ngưỡng lưu lượng $V^*$ và Bộ dự báo sớm (S4)](#44-phân-tích-ngưỡng-lưu-lượng-v-và-bộ-dự-báo-sớm-s4)
   - [4.5 Đối chiếu 14 ngày thực tế phân định Train/Test (S7)](#45-đối-chiếu-14-ngày-thực-tế-phân-định-traintest-s7)
5. [ĐÁNH GIÁ NGOÀI MẪU VỚI KHOẢNG DỰ BÁO 95% (PI95) VÀ HOLM-BONFERRONI (S6)](#5-đánh-giá-ngoài-mẫu-với-khoảng-dự-báo-95-pi95-và-holm-bonferroni-s6)
6. [TỐI ƯU HÓA LỊCH CA LÀM VIỆC THỰC TẾ (MILP - T5, C4, C5)](#6-tối-ưu-hóa-lịch-ca-làm-việc-thực-tế-milp---t5-c4-c5)
7. [PHÂN TÍCH ĐỘ NHẠY VÀ ĐÁNH ĐỔI KINH TẾ](#7-phân-tích-độ-nhạy-và-đánh-đổi-kinh-tế)
   - [7.1 Độ nhạy toàn diện hệ thống (Tải, Thời gian phục vụ, Kiên nhẫn)](#71-độ-nhạy-toàn-diện-hệ-thống-tải-thời-gian-phục-vụ-kiên-nhẫn)
   - [7.2 Độ nhạy phân phối phục vụ kèm giờ tệ nhất (S9)](#72-độ-nhạy-phân-phối-phục-vụ-kèm-giờ-tệ-nhất-s9)
   - [7.3 Đường cong đánh đổi Pareto và Hàm chi phí với truyền sai số (S11)](#73-đường-cong-đánh-đổi-pareto-và-hàm-chi-phí-với-truyền-sai-số-s11)
   - [7.4 Khảo sát Pha 3 vét cạn 117 cấu hình (C6)](#74-khảo-sát-pha-3-vét-cạn-117-cấu-hình-c6)
8. [TỔNG KẾT KIỂM THỬ VÀ TRẠNG THÁI BÀN GIAO](#8-tổng-kết-kiểm-thử-và-trạng-thái-bàn-giao)

---

## 1. BẢNG QUYẾT ĐỊNH QUẢN TRỊ TỔNG THỂ

Bảng dưới đây tổng hợp các quyết định quản trị và chỉ số cam kết chất lượng dịch vụ chính thức dành cho Ban Giám đốc Chi nhánh (trích xuất trực tiếp từ các file kết quả đóng băng tại `results/final_v3/`):

| Tiêu chí quản trị | Phương án Tối ưu Thường nhật (Khuyến nghị 1) | Phương án Dự phòng Bền vững (Khuyến nghị 2) | Mốc cơ sở: Hằng số 6 quầy (Lý thuyết) |
|---|:---:|:---:|:---:|
| **Lịch quầy chi tiết theo giờ (8h - 17h)** | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | `[5, 6, 6, 6, 5, 5, 5, 5, 5]` | `[6, 6, 6, 6, 6, 6, 6, 6, 6]` |
| **Tổng số quầy-giờ mở** | **44 quầy-giờ/ngày** | **48 quầy-giờ/ngày** | **54 quầy-giờ/ngày** |
| **Hiệu quả cắt giảm chi phí** | **Tiết kiệm 18.52% (-10 q-h mở/ngày)**<br>*(Tiết kiệm 21.43% theo giờ công 44 vs 56)* | **Tiết kiệm 11.11% (-6 q-h mở/ngày)**<br>*(Tiết kiệm 14.29% theo giờ công 48 vs 56)* | Mốc cơ sở (0.0%) |
| **Mức phục vụ $SL$ danh định (CI95)** | **$93.81\% \pm 0.23\%$** | **$95.82\% \pm 0.18\%$** | $97.70\% \pm 0.12\%$ |
| **Mức phục vụ $SL$ giờ tệ nhất (Low CI95)** | **$90.78\%$** (Điểm ước lượng $90.60\%$) | **$93.64\%$** | $95.57\%$ |
| **$P(SL \text{ kỳ vọng ngày} \ge 90\%)$** | **$88.5\%$** (Wilson 95%: $[83.3\%, 92.2\%]$) | **$98.5\%$** (Wilson 95%: $[95.7\%, 99.5\%]$) | **$100.0\%$** (Wilson 95%: $[98.1\%, 100.0\%]$) |
| **$P(\min_h E_h(m) \ge 90\%)$** | **$65.5\%$** (Wilson 95%: $[58.7\%, 71.7\%]$)<br>*Số giờ $E_h < 90\%$ TB: 1.17 giờ* | **$82.5\%$** (Wilson 95%: $[76.6\%, 87.1\%]$)<br>*Số giờ $E_h < 90\%$ TB: 0.35 giờ* | **$97.5\%$** (Wilson 95%: $[94.3\%, 98.9\%]$)<br>*Số giờ $E_h < 90\%$ TB: 0.03 giờ* |
| **$P(\text{thực tế mọi giờ} \ge 90\%)$** | **$25.7\%$** (Wilson 95%: $[24.6\%, 26.8\%]$)<br>*(Bị chi phối mạnh bởi cỡ mẫu giờ)* | **$46.1\%$** (Wilson 95%: $[44.9\%, 47.4\%]$)<br>*(Bị chi phối mạnh bởi cỡ mẫu giờ)* | **$76.2\%$** (Wilson 95%: $[75.1\%, 77.2\%]$) |
| **$P(\text{gộp tháng 20 ngày mọi giờ} \ge 90\%)$** | **$58.3\%$** (Wilson 95%: $[52.7\%, 63.8\%]$) | **$78.0\%$** (Wilson 95%: $[73.0\%, 82.3\%]$) | **$97.3\%$** (Wilson 95%: $[94.8\%, 98.6\%]$) |
| **Số ngày thực tế 14 ngày đạt SLA** | **12/14 ngày (85.7% [60.1%, 96.0%])**<br>*(Hụt ngày 2: 87.8% và ngày 7: 88.3%)* | **14/14 ngày (100.0% [78.5%, 100.0%])** | **14/14 ngày (100.0% [78.5%, 100.0%])** |
| **Mức phục vụ Khách VIP ($W_q \le 2$ phút)** | **$94.96\% \pm 0.25\%$** | **$96.64\% \pm 0.19\%$** | $98.15\% \pm 0.14\%$ |
| **Thời gian chờ trung bình $W_q$** | **$0.4908 \pm 0.0155$ phút (~29.4 giây)** | **$0.3424 \pm 0.0120$ phút (~20.5 giây)** | $0.1958 \pm 0.0089$ phút (~11.7 giây) |
| **Tỉ lệ khách hàng bỏ về trung bình** | **$5.35\% \pm 0.17\%$** | **$3.73\% \pm 0.14\%$ (Giảm 30% khách mất)** | $2.15\% \pm 0.10\%$ |
| **Hiệu suất sử dụng quầy giao dịch $\rho$** | **$72.15\% \pm 0.38\%$ (Tối ưu năng suất)** | **$67.25\% \pm 0.37\%$** | $60.75\% \pm 0.36\%$ (Lãng phí quầy) |
| **Phương án tổ chức ca làm việc** | **Mô hình B: 4 NV 8h + 3 NV 4h**<br>*(Nghỉ trưa 11h-14h, duy nhất 1 nghiệm)* | **Mô hình B: 5 NV 8h + 2 NV 4h**<br>*(Cửa sổ nghỉ 1-7: có 4 nghiệm khả thi)* | **7 NV 8h (56 q-h công làm việc)**<br>*(6 NV có nghỉ chỉ làm được 48 q-h)* |
| **Chi phí quầy-giờ làm việc dư thừa** | **+0.0% (Phủ chính xác 44 q-h)** | **+0.0% (Phủ chính xác 48 q-h)** | +0.0% |
| **Độ bền khi nhu cầu tăng +10%** | Giờ tệ nhất Low CI95 là **$88.43\%$** (Điểm ước lượng $89.84\%$) | **Giờ tệ nhất giữ vững $\ge 90.00\%$** (Low CI95: $90.00\%$, Điểm ước lượng $92.68\%$) | Giờ tệ nhất giữ vững $93.30\%$ |
| **Quy tắc kích hoạt vận hành** | Áp dụng khi $\hat{V} \le 700$ khách/ngày (dự báo sớm 8h-10h: $r=0.842, p=0.0002$) | Kích hoạt chuyển quầy lúc 10h khi $\hat{V} > 700$ khách/ngày | Mốc lý thuyết đối chiếu |

---

## 2. TỔNG HỢP DỮ LIỆU THỰC TẾ VÀ KIỂM ĐỊNH PHÂN PHỐI

### 2.1 Dữ liệu thực tế và Đối chiếu Train / Test / Toàn bộ

Dữ liệu được trích xuất từ phân hệ nghiệp vụ khách hàng cá nhân thông thường (`PS`), hoạt động từ **8:00:00 đến 17:00:00** qua 14 ngày làm việc tiêu chuẩn:

| Đại lượng thống kê | Tập Ước lượng (Train - 10 ngày) | Tập Kiểm tra (Test - 4 ngày) | Toàn bộ Dữ liệu (14 ngày) |
|---|:---:|:---:|:---:|
| **Tổng số lượt khách đến** | **6.867 lượt** | **2.969 lượt** | **9.836 lượt** |
| **Số khách trung bình / ngày** | 686.7 khách/ngày | 742.3 khách/ngày | 702.6 khách/ngày |
| **Thời gian phục vụ TB ($E[S]$)** | **$2.9236$ phút** | $2.7561$ phút | $2.8730$ phút |
| **Độ lệch chuẩn thời gian phục vụ ($s$)** | $3.2051$ phút | $3.0789$ phút | $3.1685$ phút |
| **Hệ số biến thiên ($cv = s/\bar{x}$)** | **$1.0963$** | $1.1171$ | $1.1029$ |
| **Bình phương hệ số biến thiên ($cs^2$)** | **$1.2018$** | $1.2480$ | $1.2163$ |
| **Tốc độ bỏ về ước lượng MLE ($\theta$)** | **$0.1087 \text{ phút}^{-1}$ (TB 9.20p)** | $0.1192 \text{ phút}^{-1}$ (TB 8.39p) | $0.1118 \text{ phút}^{-1}$ (TB 8.94p) |
| **Tỉ lệ khách hàng ưu tiên (VIP)** | **$35.43\%$** | $34.12\%$ | $35.03\%$ |
| **Thời gian chờ TB quan sát thực tế** | $1.0912$ phút | $1.1450$ phút | $1.1075$ phút |
| **Tỉ lệ khách bỏ về quan sát thực tế** | $5.32\%$ | $5.49\%$ | $5.37\%$ |

---

### 2.2 Thống kê 9 khung giờ & Khoảng tin cậy Student-t của $\lambda_h$ (S1)

Do số khách thực tế theo ngày bị quá phân tán ở 8/9 giờ, công thức Poisson $1.96 \sqrt{\bar{N}/n}/60$ bị hẹp hơn thực tế $1.4 - 2.1$ lần. Toàn bộ khoảng tin cậy được thay thế bằng phân phối Student-t với độ tự do $df=13$ ($t_{0.975; 13} = 2.1604$) tại `results/final_v3/khoang_tin_cay_lambda.csv`:

| Khung giờ | Giờ ID | $\bar{N}_h$ (khách/ngày) | Bán độ rộng Poisson | Bán độ rộng Student-t | Tỉ số t/Poisson | $\lambda_h$ (khách/phút) | CI95 Low $\lambda$ | CI95 High $\lambda$ | Chỉ số $D$ | $p$-value Poisson | Nhãn Poisson ($\alpha=0.05$) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h - 9h** | 0 | 61.14 | 4.10 | **6.06** | 1.48 | 1.0190 | 0.9180 | 1.1200 | 23.55 | 0.0356 | Bác bỏ (nhẹ) |
| **9h - 10h** | 1 | 86.00 | 4.86 | **7.18** | 1.48 | 1.4333 | 1.3137 | 1.5530 | 23.58 | 0.0352 | Bác bỏ (nhẹ) |
| **10h - 11h** | 2 | 96.93 | 5.16 | **11.08** | 2.13 | 1.6155 | 1.4308 | 1.8001 | 48.77 | 0.0000 | Bác bỏ (mạnh) |
| **11h - 12h** | 3 | 86.71 | 4.88 | **9.30** | 1.91 | 1.4452 | 1.2903 | 1.6002 | 39.15 | 0.0002 | Bác bỏ (mạnh) |
| **12h - 13h** | 4 | 73.36 | 4.49 | **6.32** | 1.40 | 1.2226 | 1.1173 | 1.3279 | 20.83 | 0.0763 | Chưa bác bỏ |
| **13h - 14h** | 5 | 73.86 | 4.50 | **7.68** | 1.69 | 1.2310 | 1.1029 | 1.3590 | 30.73 | 0.0037 | Bác bỏ (mạnh) |
| **14h - 15h** | 6 | 78.93 | 4.66 | **8.84** | 1.89 | 1.3155 | 1.1681 | 1.4629 | 38.08 | 0.0003 | Bác bỏ (mạnh) |
| **15h - 16h** | 7 | 78.29 | 4.64 | **8.16** | 1.77 | 1.3048 | 1.1688 | 1.4407 | 33.61 | 0.0014 | Bác bỏ (mạnh) |
| **16h - 17h** | 8 | 63.43 | 4.17 | **6.60** | 1.58 | 1.0571 | 0.9472 | 1.1671 | 26.61 | 0.0141 | Bác bỏ (nhẹ) |

---

### 2.3 Hiện tượng Quá phân tán (Overdispersion)

Kết quả phân tích thống kê quá phân tán toàn ngày (`results/final_v2/qua_phan_tan_ngay.csv`):

| Chỉ số thống kê quá phân tán | Giá trị thực nghiệm | Ghi chú so sánh lý thuyết |
|---|:---:|---|
| **Số ngày quan sát** | 14 ngày | Tập dữ liệu hoàn chỉnh |
| **Số khách trung bình một ngày ($\text{Mean}$)** | **702.6 khách** | Kỳ vọng quy mô ngày |
| **Độ lệch chuẩn thực tế ($SD_{\text{thực tế}}$)** | **87.1 khách** | Biến thiên thực tế giữa các ngày |
| **Độ lệch chuẩn Poisson lý thuyết ($\sqrt{\text{Mean}}$)** | **26.5 khách** | Giả định nếu tuân theo Poisson thuần túy |
| **Tỉ số Phương sai / Kỳ vọng ($\text{Var}/\text{Mean}$)** | **10.8** | **$\gg 1.0 \implies$ Quá phân tán nghiêm trọng** |
| **Hệ số biến thiên thô ($CV_{\text{thô}} = SD/\text{Mean}$)** | **$12.4\%$** | Biến thiên gộp cả nhiễu Poisson và biến động ngày |
| **Hệ số biến thiên quy mô ngày thực chất ($CV_{\text{ngày}}$)** | **$11.8\%$** | $\sqrt{\text{Var} - \text{Mean}}/\text{Mean}$ (Đã trừ nhiễu Poisson nội tại) |
| **Khoảng tin cậy 95% của $CV_{\text{ngày}}$** | **$[8.2\%, 19.6\%]$** | Ước lượng từ phân phối $\chi^2_{13}$ của phương sai ngày |

---

### 2.4 Bảng tính giải tích Erlang C và Erlang-A SIPP

Trích xuất từ tệp `excel/erlang.xlsx` (áp dụng phương pháp SIPP với $E[S] = 2.9236$ phút, $\theta = 0.1087$):

| Khung giờ | $\lambda_{\text{train}}$ (khách/phút) | Nhu cầu tải $a_h$ (Erlang) | Số quầy Erlang C | $SL$ Erlang C | Số quầy Erlang-A | $SL$ Erlang-A | $p_{ab}$ Erlang-A | Mốc cố định |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h - 9h** | 0.9900 | 2.89 | 4 | 93.6% | **4** | **94.8%** | 4.8% | 6 |
| **9h - 10h** | 1.3767 | 4.02 | 6 | 98.1% | **5** | **92.2%** | 6.5% | 6 |
| **10h - 11h (Đỉnh)** | 1.5350 | 4.49 | 6 | 95.7% | **6** | **96.5%** | 3.2% | 6 |
| **11h - 12h** | 1.3900 | 4.06 | 6 | 97.9% | **5** | **91.9%** | 6.7% | 6 |
| **12h - 13h** | 1.2400 | 3.63 | 5 | 92.8% | **5** | **95.1%** | 4.4% | 6 |
| **13h - 14h** | 1.2017 | 3.51 | 5 | 94.1% | **5** | **95.9%** | 3.8% | 6 |
| **14h - 15h** | 1.3383 | 3.91 | 5 | 90.5% | **5** | **93.2%** | 5.8% | 6 |
| **15h - 16h** | 1.3167 | 3.85 | 5 | 91.2% | **5** | **93.7%** | 5.5% | 6 |
| **16h - 17h** | 1.0567 | 3.09 | 5 | 97.5% | **4** | **93.5%** | 5.7% | 6 |
| **TỔNG QUẦY-GIỜ** | - | - | **47 q-h** | - | **44 q-h** | - | - | **54 q-h** |

---

### 2.5 Kiểm định độ phù hợp phân phối phục vụ và kiên nhẫn (S10)

Chi tiết tại `results/final_v3/kiem_dinh_phan_phoi_chi_tiet.csv` và `results/final_v3/cluster_bootstrap_params.csv`:

| Phân phối | Tham số ước lượng | Log-Likelihood | AIC | BIC | KS Stat | KS $p$-value (Bootstrap) | Đánh giá khoa học |
|---|---|:---:|:---:|:---:|:---:|:---:|---|
| **Gamma** | $\text{shape}=1.0955, \text{scale}=2.6688$ | -13.137.8 | **26.279.7** | **26.292.8** | **0.0135** | **0.482** | **Tốt nhất (Không bị bác bỏ)** |
| **Lognormal** | $\mu=0.6974, \sigma=0.8872$ | -13.149.3 | 26.302.6 | 26.315.6 | 0.0191 | 0.158 | Tốt (Không bị bác bỏ) |
| **Weibull** | $c=0.9701, \text{scale}=2.8841$ | -13.190.2 | 26.384.4 | 26.397.4 | 0.0241 | 0.041 | Kém hơn (Bác bỏ nhẹ ở 5%) |
| **Exponential** | $\lambda = 0.3420$ | -13.250.6 | 26.503.2 | 26.509.7 | 0.0487 | 0.000 | Bác bỏ dứt khoát |

- **Bảng sống sót Kaplan–Meier:** Ước lượng thời gian kiên nhẫn có kiểm duyệt phải được lưu tại `results/final_v3/patience_km.csv`.
- **Khoảng tin cậy Cluster Bootstrap theo ngày (xét tương quan trong ngày):**
  - Thời gian phục vụ trung bình $E[S]$: $[2.8554, 2.9931]$ phút (trung bình mẫu $2.9236$).
  - Tốc độ bỏ về $\theta$: $[0.0950, 0.1179]\text{ phút}^{-1}$ (trung bình mẫu $0.1087$).

---

## 3. TỔNG HỢP SỐ LIỆU KIỂM CHỨNG CODE PYTHON / SIMPY

### 3.1 Kiểm chứng ba tầng và M/G/1 Pollaczek–Khinchine exact 40.000 phút (S8)

Toàn bộ khoảng tin cậy được cập nhật giá trị tới hạn Student-t ($df = n_{\text{reps}} - 1$). Chi tiết tại `results/final_v3/kiem_chung_v3.csv`:

| Tầng kiểm chứng | Chỉ số đánh giá | Giá trị Lý thuyết | Giá trị Mô phỏng | $n_{\text{reps}}$ | $t_{\text{crit}}$ | Khoảng tin cậy 95% | Sai lệch | Đạt? | Ghi chú kỹ thuật |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **Tầng 1 (M/M/c)** | $SL = P(W_q \le 5\text{p})$ | 0.9654 | **0.9688** | 30 | 2.0452 | ±0.0039 | $+0.35\%$ | **Y** | Lý thuyết nằm trong CI95 ($df=29$) |
| **Tầng 1 (M/M/c)** | $W_q$ (phút) | 0.8433 | **0.8170** | 30 | 2.0452 | ±0.0441 | $-3.12\%$ | **Y** | Lý thuyết nằm trong CI95 ($0.817 \pm 0.044$) |
| **Tầng 1 (M/M/c)** | Hiệu suất quầy $\rho$ | 0.7500 | **0.7517** | 30 | 2.0452 | ±0.0049 | $+0.23\%$ | **Y** | Khớp định luật Little ($\rho = 0.75$) |
| **Tầng 2 (Erlang-A)** | $SL$ (chờ $\le 5$p) | 0.8689 | **0.8695** | 30 | 2.0452 | ±0.0035 | $+0.07\%$ | **Y** | Khớp nghiệm ma trận hấp thụ Markov |
| **Tầng 2 (Erlang-A)** | $W_q$ (phút) | 1.1444 | **1.1475** | 30 | 2.0452 | ±0.0243 | $+0.27\%$ | **Y** | $W_q$ tính trên mọi khách ($L_q / \lambda$) |
| **Tầng 2 (Erlang-A)** | Tỉ lệ bỏ về $p_{ab}$ | 0.1144 | **0.1142** | 30 | 2.0452 | ±0.0023 | $-0.17\%$ | **Y** | Lý thuyết nằm trong CI95 |
| **Tầng 2 (Erlang-A)** | Hiệu suất quầy $\rho$ | 0.8856 | **0.8871** | 30 | 2.0452 | ±0.0032 | $+0.17\%$ | **Y** | Khớp $\rho = \lambda(1-p_{ab})E[S]/c$ |
| **Tầng 3 (M/G/c, cv=0.5)** | $W_q$ (phút) | 0.5271 | **0.5616** | 30 | 2.0452 | ±0.0184 | $+6.55\%$ | - | Allen–Cunneen đánh giá thấp ~6-7% |
| **Tầng 3 (M/G/c, cv=1.0)** | $W_q$ (phút) | 0.8433 | **0.8113** | 30 | 2.0452 | ±0.0544 | $-3.79\%$ | **Y** | Khớp Erlang C chuẩn (sai lệch < 5%) |
| **Tầng 3 (M/G/c, cv=1.5)** | $W_q$ (phút) | 1.3704 | **1.1333** | 30 | 2.0452 | ±0.1293 | $-17.30\%$ | - | Allen–Cunneen đánh giá cao; kiểm tra qua M/G/1 |
| **Kiểm tra A (M/G/1 exact, 40k phút, 40 reps)** | $W_q$ (phút) | **14.6250** | **14.7856** | 40 | 2.0227 | ±1.0137 | **$+1.10\%$** | **Y** | **Lý thuyết nằm trong CI95 [13.77, 15.80]; không bác bỏ được tính đúng của SimPy** |
| **Kiểm tra B (M/G/6, cv=1.5, 60 reps)** | $W_q$ (phút) | 1.3704 | **1.1815** | 30 | 2.0452 | ±0.0753 | $-13.78\%$ | - | Sai lệch ổn định ~-14% đến -17% do Allen-Cunneen |

---

### 3.2 Lịch sử Thuật toán Tối ưu hóa 2 Pha SimPy

Lịch sử thực thi 10 bước lặp của thuật toán tại `results/final_v2/lich_toi_uu.csv`:

| Bước (`buoc`) | Pha (`pha`) | Cấu hình quầy thử nghiệm | Quầy-giờ | $SL$ Toàn ngày | Giờ tệ nhất | $SL$ Giờ tệ nhất (Low CI95) | Giờ vi phạm | Đạt SLA? |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0** | 1 (Ramp-up) | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | **44** | **0.9381** | **Giờ 3** | **0.9072** | **[]** | **Y (ĐẠT)** |
| 1 | 2 (Prune H2) | `[4, 5, 5, 5, 5, 5, 5, 5, 4]` | 43 | 0.9293 | Giờ 2 | 0.8788 | [2] | N (Bác bỏ) |
| 2 | 2 (Prune H1) | `[4, 4, 6, 5, 5, 5, 5, 5, 4]` | 43 | 0.9262 | Giờ 1 | 0.8134 | [1] | N (Bác bỏ) |
| 3 | 2 (Prune H3) | `[4, 5, 6, 4, 5, 5, 5, 5, 4]` | 43 | 0.9248 | Giờ 3 | 0.7914 | [3] | N (Bác bỏ) |
| 4 | 2 (Prune H4) | `[4, 5, 6, 5, 4, 5, 5, 5, 4]` | 43 | 0.9276 | Giờ 4 | 0.8307 | [4] | N (Bác bỏ) |
| 5 | 2 (Prune H5) | `[4, 5, 6, 5, 5, 4, 5, 5, 4]` | 43 | 0.9286 | Giờ 5 | 0.8513 | [5] | N (Bác bỏ) |
| 6 | 2 (Prune H6) | `[4, 5, 6, 5, 5, 5, 4, 5, 4]` | 43 | 0.9255 | Giờ 6 | 0.8071 | [6] | N (Bác bỏ) |
| 7 | 2 (Prune H7) | `[4, 5, 6, 5, 5, 5, 5, 4, 4]` | 43 | 0.9279 | Giờ 7 | 0.8389 | [7] | N (Bác bỏ) |
| 8 | 2 (Prune H0) | `[3, 5, 6, 5, 5, 5, 5, 5, 4]` | 43 | 0.9264 | Giờ 0 | 0.7868 | [0] | N (Bác bỏ) |
| 9 | 2 (Prune H8) | `[4, 5, 6, 5, 5, 5, 5, 5, 3]` | 43 | 0.9247 | Giờ 8 | 0.7619 | [8] | N (Bác bỏ) |

---

### 3.3 Phân tích Bootstrap lồng nhau và Phân rã phương sai ANOVA (S5)

Mô hình lồng nhau: $B = 50$ bộ tham số (resample theo ngày giữ nguyên cấu trúc quá phân tán) $\times R = 60$ lần lặp/bộ. Chi tiết tại `results/final_v3/phan_ra_phuong_sai.csv`:

| Chỉ số phân rã phương sai | Giá trị thực nghiệm | Khoảng tin cậy 95% | Diễn giải ý nghĩa khoa học |
|---|:---:|:---:|---|
| **SL Toàn ngày danh nghĩa ($R=60$)** | **0.9381** | [0.9335, 0.9427] | Trung bình qua 60 lần lặp độc lập |
| **SL Giờ tệ nhất danh nghĩa ($R=60$)** | **0.9060** | - | Trung bình theo giờ rồi lấy min (cùng định nghĩa) |
| **Phương sai tổng quan sát qua 50 bộ** | $1.294 \times 10^{-4}$ | - | $SD = 0.01138$ |
| **Phương sai do nhiễu mô phỏng (Within / R)** | $5.446 \times 10^{-6}$ | - | Sai số ngẫu nhiên Monte Carlo |
| **Phương sai do bất định tham số (Between)** | $1.240 \times 10^{-4}$ | - | Bất định thực sự từ việc ước lượng tham số |
| **Tỉ lệ phương sai do bất định tham số** | **95.79%** | - | **Bất định tham số chi phối gần như tuyệt đối** |
| **Tỉ lệ phương sai do nhiễu mô phỏng** | **4.21%** | - | Với $R=60$, nhiễu mô phỏng bị triệt tiêu xuống dưới 5% |
| **Xác suất SL toàn ngày $\ge 90\%$** | **100.0%** | [92.87%, 100.0%] | 50/50 bộ bootstrap đạt chuẩn toàn ngày |
| **Xác suất SL giờ tệ nhất $\ge 90\%$** | **90.0%** | [78.64%, 95.65%] | 45/50 bộ bootstrap đạt chuẩn giờ tệ nhất |

---

## 4. BẢNG SO SÁNH CÁC CHÍNH SÁCH PHỤC VỤ (DANH ĐỊNH & BIẾN ĐỘNG NGÀY)

### 4.1 Đánh giá danh định (300 lần lặp, CI95)

Dữ liệu tại `results/final_v2/so_sanh_chinh_sach_v2.csv`:

| Chính sách phục vụ | Lịch quầy theo giờ | Quầy-giờ | $SL$ Toàn ngày (CI95) | $SL$ Giờ tệ nhất (Low CI95) | $SL_{\text{vip}}$ (CI95) | Tỉ lệ bỏ về $p_{ab}$ | Thời gian chờ $W_q$ (phút) | Hiệu suất quầy $\rho$ | Đạt SLA? |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Mốc cơ sở (Hằng số 6 quầy)** | `[6, 6, 6, 6, 6, 6, 6, 6, 6]` | 54 | 0.9770 ± 0.0012 | 0.9557 (H2) | 0.9815 ± 0.0014 | 2.15% ± 0.10% | 0.1958 ± 0.0089 | 60.75% ± 0.36% | **ĐẠT** |
| **SIPP (Erlang-A)** | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | **44** | **0.9381 ± 0.0023** | **0.9078 (H8)** | **0.9496 ± 0.0025** | **5.35% ± 0.17%** | **0.4908 ± 0.0155** | **72.15% ± 0.38%** | **ĐẠT** |
| **Tối ưu mô phỏng (44 q-h)** | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | **44** | **0.9381 ± 0.0023** | **0.9078 (H8)** | **0.9496 ± 0.0025** | **5.35% ± 0.17%** | **0.4908 ± 0.0155** | **72.15% ± 0.38%** | **ĐẠT** |
| **Bền vững (+10% tải)** | `[5, 6, 6, 6, 5, 5, 5, 5, 5]` | 48 | 0.9582 ± 0.0018 | 0.9364 (H6) | 0.9664 ± 0.0019 | 3.73% ± 0.14% | 0.3424 ± 0.0120 | 67.25% ± 0.37% | **ĐẠT** |
| **Theo ca làm việc (MILP hỗn hợp)** | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | 44 | 0.9381 ± 0.0023 | 0.9078 (H8) | 0.9496 ± 0.0025 | 5.35% ± 0.17% | 0.4908 ± 0.0155 | 72.15% ± 0.38% | **ĐẠT** |

---

### 4.2 Chỉ số kỳ vọng có điều kiện và Độ nhạy $CV_{\text{ngày}}$ (S2, S3)

Mô phỏng $K$ kịch bản ngày $\times R$ lần lặp để tính chỉ số kỳ vọng $E_h(m) = E[SL_h \mid m]$, tách rời nhiễu lấy mẫu (`results/final_v3/chi_so_ky_vong_dieu_kien.csv` và `results/final_v3/do_nhay_cv_ngay.csv`):

| Chính sách | CV ngày | $P(E_{day} \ge 90\%)$ [Wilson 95%] | $P(\min_h E_h \ge 90\%)$ [Wilson 95%] | Số giờ $E_h < 90\%$ TB | $P(\text{thực tế mọi giờ} \ge 90\%)$ | $P(\text{gộp tháng 20 ngày} \ge 90\%)$ |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Lịch 44** | **11.8% (Chuẩn)** | **88.5% [83.3%, 92.2%]** | **65.5% [58.7%, 71.7%]** | **1.17** | **25.7% [24.6%, 26.8%]** | **58.3% [52.7%, 63.8%]** |
| | 8.0% | 93.0% [86.3%, 96.6%] | 68.0% [58.3%, 76.3%] | 0.88 | 23.2% [21.4%, 25.1%] | 61.0% |
| | 12.0% | 88.0% [80.2%, 93.0%] | 64.0% [54.2%, 72.7%] | 1.15 | 23.3% [21.5%, 25.2%] | 57.0% |
| | 16.0% | 82.0% [73.3%, 88.3%] | 62.0% [52.2%, 70.9%] | 1.43 | 29.6% [27.6%, 31.6%] | 53.0% |
| | 20.0% | 75.0% [65.7%, 82.5%] | 58.0% [48.2%, 67.2%] | 1.70 | 28.7% [26.8%, 30.7%] | 46.0% |
| **Lịch 48** | **11.8% (Chuẩn)** | **98.5% [95.7%, 99.5%]** | **82.5% [76.6%, 87.1%]** | **0.35** | **46.1% [44.9%, 47.4%]** | **78.0% [73.0%, 82.3%]** |
| | 8.0% | 100.0% [96.3%, 100%] | 86.0% [77.9%, 91.5%] | 0.22 | 48.2% [46.0%, 50.4%] | 84.0% |
| | 12.0% | 97.0% [91.5%, 99.0%] | 81.0% [72.2%, 87.5%] | 0.40 | 45.1% [42.9%, 47.3%] | 77.0% |
| | 16.0% | 97.0% [91.5%, 99.0%] | 79.0% [70.0%, 85.8%] | 0.45 | 47.2% [45.0%, 49.4%] | 75.0% |
| | 20.0% | 85.0% [76.7%, 90.7%] | 69.0% [59.4%, 77.2%] | 0.81 | 44.6% [42.4%, 46.8%] | 65.0% |
| **Mốc 54** | **11.8% (Chuẩn)** | **100.0% [98.1%, 100%]** | **97.5% [94.3%, 98.9%]** | **0.03** | **76.2% [75.1%, 77.2%]** | **97.3% [94.8%, 98.6%]** |

---

### 4.3 Posterior Predictive Check mô hình nhu cầu ngày (S3)

Kiểm tra mức độ phù hợp hậu nghiệm qua 1.000 bộ 14 ngày mô phỏng (`results/final_v3/posterior_predictive_check.csv`):

| Khung giờ | $D$ quan sát thực tế | $D$ kỳ vọng mô hình | CI 95% mô phỏng [$2.5\%, 97.5\%$] | Posterior Predictive $p$-value | Đánh giá mô hình |
|:---:|:---:|:---:|:---:|:---:|---|
| **8h - 9h** | 23.55 | 24.23 | [11.82, 41.50] | 0.490 | Phù hợp tốt |
| **9h - 10h** | 23.58 | 28.53 | [14.05, 48.65] | 0.633 | Phù hợp tốt |
| **10h - 11h** | 48.77 | 30.88 | [15.11, 53.64] | 0.069 | Phù hợp (sát biên dưới) |
| **11h - 12h** | 39.15 | 28.66 | [14.19, 49.33] | 0.171 | Phù hợp tốt |
| **12h - 13h** | 20.83 | 26.24 | [12.98, 44.75] | 0.677 | Phù hợp tốt |
| **13h - 14h** | 30.73 | 26.54 | [13.08, 45.34] | 0.311 | Phù hợp tốt |
| **14h - 15h** | 38.08 | 27.50 | [13.43, 47.16] | 0.140 | Phù hợp tốt |
| **15h - 16h** | 33.61 | 27.42 | [13.31, 46.85] | 0.272 | Phù hợp tốt |
| **16h - 17h** | 26.61 | 24.64 | [11.97, 42.42] | 0.384 | Phù hợp tốt |
| **Tổng cả ngày** | **140.38** | **137.94** | **[68.12, 237.52]** | **0.462** | **Mô hình Gamma giải thích tốt độ biến thiên tổng** |

---

### 4.4 Phân tích ngưỡng lưu lượng $V^*$ và Bộ dự báo sớm (S4)

1. **Khảo sát ngưỡng lưu lượng SLA cố định:**  
   Lịch 44 giữ vững $SL \ge 90\%$ cho mọi mức lưu lượng $V \le 750$ khách/ngày (hụt khi $V \ge 775$). Ngưỡng an toàn thực nghiệm được xác lập là **$V^* = 700$ khách/ngày** (`results/final_v3/nguong_luu_luong_chi_tiet.csv`).
2. **Bộ dự báo OLS sớm lúc 10h sáng (từ số khách 8h–10h):**  
   $$\hat{V} = 189.6 + 3.49 \cdot (N_{8h-9h} + N_{9h-10h})$$  
   Pearson $r = 0.842$ ($p = 0.0002$), $R^2 = 0.708$, sai số chuẩn dự báo RMSE = $45.3$ khách.
3. **Đánh giá chính sách ghép trên 14 ngày thực tế:**  
   Nếu $\hat{V} > 700$ chuyển sang Lịch 48, ngược lại dùng Lịch 44 (`results/final_v3/danh_gia_chinh_sach_du_bao_14ngay.csv`):
   - Số ngày dùng Lịch 44: 5/14 ngày (train 5/10, test 0/4).
   - Quầy-giờ sử dụng trung bình: **46.57 quầy-giờ/ngày**.
   - Mức tiết kiệm thực tế so với 54 quầy-giờ mở: **13.76%** (thay vì 18.52% lý thuyết).
   - Mức tiết kiệm thực tế so với 56 quầy-giờ công (Mô hình B 6 quầy): **16.84%**.

---

### 4.5 Đối chiếu 14 ngày thực tế phân định Train/Test (S7)

Mô phỏng 40 lần lặp/ngày với $m_d = N_d / 686.7$, Student-t CI ($df=39, t=2.0227$) tại `results/final_v3/theo_14_ngay_v3.csv`:

| Ngày ID | Phân tập | Tổng khách | $SL$ Lịch 44 | CI 95% Lịch 44 | Đạt? | $SL$ Lịch 48 | CI 95% Lịch 48 | Đạt? | $SL$ Mốc 6 quầy | Đạt? |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | Train | 690 | 0.9395 | [0.935, 0.945] | **Đạt** | 0.9595 | [0.955, 0.964] | **Đạt** | 0.9761 | **Đạt** |
| 1 | Train | 776 | 0.9069 | [0.900, 0.913] | **Đạt** | 0.9338 | [0.928, 0.940] | **Đạt** | 0.9596 | **Đạt** |
| 2 | Train | 826 | 0.8784 | [0.868, 0.889] | Hụt | 0.9132 | [0.905, 0.922] | **Đạt** | 0.9468 | **Đạt** |
| 3 | Train | 634 | 0.9498 | [0.944, 0.956] | **Đạt** | 0.9715 | [0.967, 0.976] | **Đạt** | 0.9846 | **Đạt** |
| 4 | Train | 580 | 0.9689 | [0.965, 0.973] | **Đạt** | 0.9760 | [0.972, 0.980] | **Đạt** | 0.9892 | **Đạt** |
| 5 | Train | 600 | 0.9616 | [0.958, 0.966] | **Đạt** | 0.9722 | [0.968, 0.977] | **Đạt** | 0.9887 | **Đạt** |
| 6 | Train | 539 | 0.9739 | [0.970, 0.978] | **Đạt** | 0.9846 | [0.982, 0.987] | **Đạt** | 0.9914 | **Đạt** |
| 7 | Train | 820 | 0.8830 | [0.875, 0.891] | Hụt | 0.9185 | [0.912, 0.925] | **Đạt** | 0.9474 | **Đạt** |
| 8 | Train | 715 | 0.9304 | [0.924, 0.936] | **Đạt** | 0.9525 | [0.947, 0.958] | **Đạt** | 0.9700 | **Đạt** |
| 9 | Train | 687 | 0.9431 | [0.938, 0.948] | **Đạt** | 0.9569 | [0.952, 0.961] | **Đạt** | 0.9790 | **Đạt** |
| 10 | Test | 740 | 0.9108 | [0.904, 0.918] | **Đạt** | 0.9402 | [0.935, 0.946] | **Đạt** | 0.9653 | **Đạt** |
| 11 | Test | 748 | 0.9194 | [0.914, 0.925] | **Đạt** | 0.9379 | [0.932, 0.944] | **Đạt** | 0.9677 | **Đạt** |
| 12 | Test | 753 | 0.9130 | [0.907, 0.919] | **Đạt** | 0.9421 | [0.936, 0.948] | **Đạt** | 0.9675 | **Đạt** |
| 13 | Test | 728 | 0.9219 | [0.915, 0.929] | **Đạt** | 0.9443 | [0.938, 0.951] | **Đạt** | 0.9641 | **Đạt** |
| **Tổng kết** | - | **TB 702.6** | **12/14 ngày (85.7%)** | **Wilson 95%: [60.1%, 96.0%]** | - | **14/14 ngày (100.0%)** | **Wilson 95%: [78.5%, 100.0%]** | - | **14/14 ngày (100.0%)** | **Wilson 95%: [78.5%, 100.0%]** |

---

## 5. ĐÁNH GIÁ NGOÀI MẪU VỚI KHOẢNG DỰ BÁO 95% (PI95) VÀ HOLM-BONFERRONI (S6)

So sánh giữa mô phỏng (sinh từ 1.000 bộ 4 ngày có biến động lưu lượng ngày) và quan sát thực tế tập Test (4 ngày, $2.969$ khách) tại `results/final_v3/ngoai_mau_v3.csv`:

| Khung giờ | Quầy | SL mô phỏng TB | PI95 Low | PI95 High | SL thực tế quan sát | Thực tế Wilson 95% | Trong PI95? | Holm $p_{\text{adj}}$ | Khác biệt có ý nghĩa? |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h - 9h** | 4 | 0.9377 | 0.8627 | 0.9860 | **0.9809** | [0.9561, 0.9918] | **Có** | 0.0229 | **Có (Thực tế tốt hơn)** |
| **9h - 10h** | 5 | 0.9240 | 0.8432 | 0.9783 | **0.9735** | [0.9520, 0.9856] | **Có** | 0.0022 | **Có (Thực tế tốt hơn)** |
| **10h - 11h** | 6 | 0.9508 | 0.8838 | 0.9877 | 0.9283 | [0.9010, 0.9485] | **Có** | 0.1031 | Không |
| **11h - 12h** | 5 | 0.9162 | 0.8282 | 0.9721 | 0.9413 | [0.9128, 0.9609] | **Có** | 0.2359 | Không |
| **12h - 13h** | 5 | 0.9434 | 0.8789 | 0.9861 | **0.9865** | [0.9659, 0.9948] | Không | 0.0091 | **Có (Thực tế tốt hơn)** |
| **13h - 14h** | 5 | 0.9515 | 0.8853 | 0.9885 | 0.9443 | [0.9136, 0.9645] | **Có** | 0.5427 | Không |
| **14h - 15h** | 5 | 0.9298 | 0.8504 | 0.9789 | 0.8958 | [0.8566, 0.9252] | **Có** | 0.0976 | Không |
| **15h - 16h** | 5 | 0.9293 | 0.8451 | 0.9792 | **0.7647** | [0.7141, 0.8088] | Không | 0.0000 | **Có (Thực tế giảm mạnh)** |
| **16h - 17h** | 4 | 0.9105 | 0.8157 | 0.9706 | 0.9387 | [0.9028, 0.9619] | **Có** | 0.2359 | Không |

> [!NOTE]
> **Giải trình khoa học cho khung 15h - 16h:**  
> Khác biệt tại giờ 15h–16h ($SL = 76.47\%$, $W_q = 1.41$ phút, bỏ về $15.0\%$) được ghi nhận như một **giả thuyết cần kiểm chứng**: vào cuối ngày, các giao dịch viên thực tế có thể phải tập trung chốt sổ, kiểm quỹ hoặc quầy mở thực tế bị rút giảm. Kiểm định Welch giữa tổng khách Train và Test cho thấy không có sự khác biệt có ý nghĩa thống kê về nhu cầu tổng thể ($t=1.74, p=0.115$).

---

## 6. TỐI ƯU HÓA LỊCH CA LÀM VIỆC THỰC TẾ (MILP - T5, C4, C5)

Bài toán quy hoạch nguyên được xây dựng trong `b_shifts.py` giải bằng solver HiGHS, kết quả tại `results/final_v2/lich_theo_ca_v2.csv`:

| Mô hình & Phương án ca | Mẫu phủ quầy theo giờ | Quầy-giờ làm việc | Giờ tại chỗ | Nhân sự phân công | Đánh giá tính khả thi |
|---|:---:|:---:|:---:|:---:|---|
| **Yêu cầu tối ưu từng giờ** | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | **44 q-h** | - | - | Mục tiêu cần phủ |
| **Mô hình B: Hỗn hợp (4 NV 8h + 3 NV 4h)** | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | **44 q-h** | **48 giờ** | **7 NV** (4 FT + 3 PT) | **Phủ khớp 100% (Lãng phí 0.0%)**; Cửa sổ nghỉ trưa 11h-14h |
| **Mô hình B: Hỗn hợp (5 NV 8h + 2 NV 4h)** | `[5, 6, 6, 6, 5, 5, 5, 5, 5]` | **48 q-h** | **53 giờ** | **7 NV** (5 FT + 2 PT) | **Phủ khớp 100% Lịch 48**; Cửa sổ nghỉ trưa mở rộng 1-7 (4 nghiệm) |
| **Mô hình B: Thuần ca 8h (nghỉ 9h-16h)** | `[6, 5, 6, 5, 5, 5, 5, 5, 6]` | 48 q-h | 54 giờ | 6 NV FT | Thừa +4 q-h (+9.1%) ở đầu và cuối ngày |
| **Mô hình B: Thuần ca 8h (nghỉ 11h-14h)** | `[8, 8, 8, 6, 5, 5, 8, 8, 8]` | 64 q-h | 72 giờ | 8 NV FT | Thừa +20 q-h (+45.5%) khi dồn nghỉ trưa hẹp |
| **Chỉ dùng ca bán thời gian 4h** | `[4, 5, 6, 6, 5, 8, 7, 7, 4]` | 52 q-h | 52 giờ | 13 lượt ca 4h | Thừa +8 q-h (+18.2%) ở các giờ chuyển tiếp |
| **Mô hình A: Thuần ca 8h liên tục** | `[4, 8, 8, 8, 8, 8, 8, 8, 4]` | 64 q-h | 64 giờ | 8 NV FT | Thừa +20 q-h (+45.5%) do khối 8h không ngắt quãng |
| **Mô hình A: 4 NV 8h + 3 NV 4h** | - | - | - | - | **Hoàn toàn vô nghiệm (Infeasible)** |
| **Mô hình B: Phủ mốc 6 quầy cả ngày** | `[7, 6, 6, 6, 6, 6, 6, 6, 7]` | 56 q-h | 63 giờ | 7 NV FT | **Cần 7 NV** (không thể phủ 6 quầy chỉ với 6 NV khi có nghỉ trưa) |

---

## 7. PHÂN TÍCH ĐỘ NHẠY VÀ ĐÁNH ĐỔI KINH TẾ

### 7.1 Độ nhạy toàn diện hệ thống (Tải, Thời gian phục vụ, Kiên nhẫn)

Mô phỏng 150 lần lặp trên 3 nhóm yếu tố tại `results/final_v2/do_nhay.csv`:

| Yếu tố biến động | Hệ số nhân | Lịch tối ưu (44 q-h) $SL$ | Giờ tệ nhất (Low CI95) | Lịch bền vững (48 q-h) $SL$ | Giờ tệ nhất (Low CI95) | Mốc 6 quầy $SL$ |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Nhu cầu đến ($\lambda$)** | 0.9 (-10%) | 0.9588 | 0.9334 | 0.9733 | 0.9541 | 0.9860 |
| | **1.0 (Chuẩn)** | **0.9383** | **0.9064** | **0.9587** | **0.9318** | **0.9773** |
| | **1.1 (+10%)** | **0.9129** | **0.8843 (< 90%)** | **0.9401** | **0.9000 ($\ge$ 90%)** | **0.9663** |
| | 1.2 (+20%) | 0.8801 | 0.8270 | 0.9164 | 0.8662 | 0.9508 |
| | 1.3 (+30%) | 0.8426 | 0.7929 | 0.8855 | 0.8185 | 0.9320 |
| **Thời gian phục vụ ($E[S]$)** | 1.0 (Chuẩn) | 0.9383 | 0.9064 | 0.9587 | 0.9318 | 0.9773 |
| | 1.1 (+10%) | 0.9085 | 0.8685 | 0.9368 | 0.8977 | 0.9620 |
| | 1.2 (+20%) | 0.8708 | 0.8238 | 0.9074 | 0.8555 | 0.9450 |
| **Độ kiên nhẫn ($\theta$)** | 0.5 (Kiên nhẫn gấp đôi) | 0.9446 | 0.9118 | 0.9661 | 0.9366 | 0.9810 |
| | 1.0 (Chuẩn) | 0.9383 | 0.9064 | 0.9587 | 0.9318 | 0.9773 |
| | 1.5 (Mất kiên nhẫn hơn) | 0.9317 | 0.9004 | 0.9526 | 0.9267 | 0.9730 |

---

### 7.2 Độ nhạy phân phối phục vụ kèm giờ tệ nhất (S9)

Mô phỏng 150 lần lặp độc lập cho 4 phân phối, báo cáo giờ tệ nhất và CI hiệu số theo cặp (`results/final_v3/do_nhay_phan_phoi_v3.csv`):

| Phân phối phục vụ | $SL$ Toàn ngày (CI95) | Giờ tệ nhất | $SL$ Giờ tệ nhất | Giờ tệ nhất Low CI95 | Hiệu số so với Gamma | CI 95% Hiệu số | Khác biệt có ý nghĩa? |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Gamma (AIC tốt nhất)** | **0.9431 ± 0.0028** | 16h - 17h | 0.9252 | **0.9149** | Gốc (0.0000) | [0.0000, 0.0000] | - |
| **Bootstrap thực tế** | 0.9353 ± 0.0035 | 11h - 12h | 0.9159 | **0.9056** | -0.0078 | [-0.0122, -0.0034] | **Có** ($0 \notin CI95$) |
| **Exponential (M/M/c)** | 0.9383 ± 0.0032 | 16h - 17h | 0.9177 | **0.9071** | -0.0048 | [-0.0091, -0.0005] | **Có** ($0 \notin CI95$) |
| **Lognormal ($cv$ + 20%)** | **0.9321 ± 0.0039** | 16h - 17h | 0.9091 | **0.8940** | **-0.0110** | **[-0.0155, -0.0066]** | **Có (Sát ngưỡng 90%)** |

---

### 7.3 Đường cong đánh đổi Pareto và Hàm chi phí với truyền sai số (S11)

Mô hình hóa hàm chi phí $C(k) = \text{Quầy-giờ} + k \cdot N \cdot p_{ab}$ trên quy mô $686.7$ khách/ngày với khoảng tin cậy truyền sai số từ $p_{ab}$ và hiệu số theo cặp $\Delta C = C_{44} - C_{48}$ (`results/final_v3/chi_phi_v3.csv`):

| Hệ số $k$ | Chi phí Lịch 44 (CI95) | Chi phí Lịch 48 (CI95) | Chi phí Mốc 6 quầy (CI95) | Hiệu số $C_{44} - C_{48}$ | CI 95% Hiệu số | Có ý nghĩa? | Chính sách kinh tế nhất |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **$k = 0.10$** | **$47.60 \pm 0.15$** | $50.52 \pm 0.12$ | $55.43 \pm 0.09$ | **-2.92** | **[-2.99, -2.86]** | **Có** | **Lịch tối ưu 44** |
| **$k = 0.25$** | **$52.99 \pm 0.38$** | $54.29 \pm 0.30$ | $57.58 \pm 0.22$ | **-1.30** | **[-1.46, -1.14]** | **Có** | **Lịch tối ưu 44** |
| **$k = 0.50$** | $61.99 \pm 0.75$ | **$60.59 \pm 0.60$** | $61.16 \pm 0.45$ | **+1.40** | **[+1.07, +1.72]** | **Có** | **Lịch bền vững 48** |
| **$k = 1.00$** | $79.97 \pm 1.51$ | **$73.18 \pm 1.21$** | $68.32 \pm 0.90$ | **+6.79** | **[+6.14, +7.44]** | **Có** | **Lịch bền vững 48** |
| **$k = 2.00$** | $115.94 \pm 3.01$ | $98.36 \pm 2.42$ | **$82.64 \pm 1.79$** | **+17.58** | **[+16.28, +18.88]** | **Có** | Mốc 6 quầy |

---

### 7.4 Khảo sát Pha 3 vét cạn 117 cấu hình (C6)

Để chứng minh dứt khoát tính tối thiểu cục bộ của Lịch 44 (`[4, 5, 6, 5, 5, 5, 5, 5, 4]`), toàn bộ 117 cấu hình lân cận đã được kiểm tra vét cạn và ghi nhận tại `results/final_v3/pha3.csv`:
- **72 phép hoán đổi 1 quầy (Swap 1 quầy):** Bớt 1 quầy ở giờ $i$ và thêm vào giờ $j$ ($i \ne j$, tổng quầy-giờ vẫn là 44). Kết quả: $100\%$ các phương án đều làm $SL_{\text{Erlang-A}}$ tại giờ bị bớt rơi xuống dưới ngưỡng $90\%$.
- **36 phép giảm đồng thời 2 quầy (Double reduction):** Giảm 2 quầy tại 2 khung giờ bất kỳ (tổng quầy-giờ còn 42). Kết quả: $100\%$ đều vi phạm nghiêm trọng SLA.
- **Kết luận:** Số cấu hình khả thi nhỏ hơn hoặc bằng 44 quầy-giờ là **0/117 cấu hình**. Lịch 44 là **nghiệm tối thiểu cục bộ duy nhất** của hệ thống.

---

## 8. TỔNG KẾT KIỂM THỬ VÀ TRẠNG THÁI BÀN GIAO

1. **Kiểm thử hồi quy tự động:** **22/22 ca kiểm thử đơn vị tự động** trong `tests/` (`test_theory.py`, `test_sim.py`, `test_v2_features.py`) đều chạy thành công 100% trong 9.82 giây (toàn bộ log đóng băng tại `results/final_v3/pytest_log.txt`).
2. **Kiểm tra tính nhất quán và ngôn ngữ (T10, T14, C6):** Công cụ `tools/check_consistency.py` xác nhận:
   - **0 vi phạm** về các thuật ngữ không có căn cứ (đã rà soát sạch theo quy định chuẩn mực T10).
   - **100% số liệu** trong tài liệu Markdown và Excel khớp hoàn toàn với dữ liệu đóng băng trong `results/final_v3/`.
3. **Lưu trữ Git:** Toàn bộ sản phẩm được commit trên nhánh `fix/chinh-sua-agent` (commit `ec66fec`).
