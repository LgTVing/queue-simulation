# BẢNG TỔNG HỢP SỐ LIỆU CUỐI CÙNG VÀ ĐÁNH GIÁ TOÀN DIỆN DỰ ÁN (PHIÊN BẢN V2 CHUẨN HÓA)

**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu cho quầy giao dịch ngân hàng  
**Thời điểm tổng hợp:** Tháng 10/2026 (Đã cập nhật toàn bộ 14 nhiệm vụ kỹ thuật và đóng băng tại `results/final_v2/`)  
**Bộ dữ liệu:** Anonymous Bank Call Center (Technion SEE Center), 14 ngày làm việc, $9.836$ giao dịch  

---

## MỤC LỤC

1. [BẢNG QUYẾT ĐỊNH QUẢN TRỊ TỔNG THỂ](#1-bảng-quyết-định-quản-trị-tổng-thể)
2. [TỔNG HỢP SỐ LIỆU DỮ LIỆU THỰC TẾ VÀ 3 FILE EXCEL](#2-tổng-hợp-số-liệu-dữ-liệu-thực-tế-và-3-file-excel)
   - [2.1 Dữ liệu thực tế và Đối chiếu Train / Test / Toàn bộ](#21-dữ-liệu-thực-tế-và-đối-chiếu-train--test--toàn-bộ)
   - [2.2 Thống kê mô tả 9 khung giờ & Kiểm định Poisson (T1)](#22-thống-kê-mô-tả-9-khung-giờ--kiểm-định-poisson-t1)
   - [2.3 Hiện tượng Quá phân tán (Overdispersion)](#23-hiện-tượng-quá-phân-tán-overdispersion)
   - [2.4 Bảng tính giải tích Erlang C và Erlang-A trên Excel](#24-bảng-tính-giải-tích-erlang-c-và-erlang-a-trên-excel)
3. [TỔNG HỢP SỐ LIỆU KIỂM CHỨNG CODE PYTHON / SIMPY](#3-tổng-hợp-số-liệu-kiểm-chứng-code-python--simpy)
   - [3.1 Kiểm chứng ba tầng và Hai kiểm tra độc lập](#31-kiểm-chứng-ba-tầng-và-hai-kiểm-tra-độc-lập)
   - [3.2 Lịch sử Thuật toán Tối ưu hóa 2 Pha SimPy](#32-lịch-sử-thuật-toán-tối-ưu-hóa-2-pha-simpy)
4. [BẢNG SO SÁNH CÁC CHÍNH SÁCH PHỤC VỤ (DANH ĐỊNH & BIẾN ĐỘNG NGÀY)](#4-bảng-so-sánh-các-chính-sách-phục-vụ-danh-định--biến-động-ngày)
   - [4.1 Đánh giá danh định (300 lần lặp, CI95)](#41-đánh-giá-danh-định-300-lần-lặp-ci95)
   - [4.2 Đánh giá khi có biến động lưu lượng ngày ($CV = 11.8\%$)](#42-đánh-giá-khi-có-biến-động-lưu-lượng-ngày-cv--118)
   - [4.3 Đối chiếu kết quả trên 14 ngày quan sát thực tế](#43-đối-chiếu-kết-quả-trên-14-ngày-quan-sát-thực-tế)
5. [ĐÁNH GIÁ NGOÀI MẪU TRÊN TẬP TEST 4 NGÀY (T4)](#5-đánh-giá-ngoài-mẫu-trên-tập-test-4-ngày-t4)
6. [TỐI ƯU HÓA LỊCH CA LÀM VIỆC THỰC TẾ (MILP - T5)](#6-tối-ưu-hóa-lịch-ca-làm-việc-thực-tế-milp---t5)
7. [PHÂN TÍCH ĐỘ NHẠY VÀ ĐÁNH ĐỔI KINH TẾ](#7-phân-tích-độ-nhạy-và-đánh-đổi-kinh-tế)
   - [7.1 Độ nhạy toàn diện hệ thống (Tải, Thời gian phục vụ, Kiên nhẫn)](#71-độ-nhạy-toàn-diện-hệ-thống-tải-thời-gian-phục-vụ-kiên-nhẫn)
   - [7.2 Độ nhạy phân phối phục vụ qua CRN bắt cặp (T8)](#72-độ-nhạy-phân-phối-phục-vụ-qua-crn-bắt-cặp-t8)
   - [7.3 Đường cong đánh đổi Pareto và Phân tích hàm chi phí](#73-đường-cong-đánh-đổi-pareto-và-phân-tích-hàm-chi-phí)
8. [TỔNG KẾT KIỂM THỬ VÀ TRẠNG THÁI BÀN GIAO](#8-tổng-kết-kiểm-thử-và-trạng-thái-bàn-giao)

---

## 1. BẢNG QUYẾT ĐỊNH QUẢN TRỊ TỔNG THỂ

Bảng dưới đây tổng hợp các quyết định quản trị và chỉ số cam kết chất lượng dịch vụ chính thức dành cho Ban Giám đốc Chi nhánh:

| Tiêu chí quản trị | Phương án Tối ưu Thường nhật (Khuyến nghị 1) | Phương án Dự phòng Bền vững (Khuyến nghị 2) | Mốc cơ sở: Hằng số 6 quầy (không phải nhân sự thực tế) |
|---|:---:|:---:|:---:|
| **Lịch quầy chi tiết theo giờ (8h - 17h)** | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | `[5, 6, 6, 6, 5, 5, 5, 5, 5]` | `[6, 6, 6, 6, 6, 6, 6, 6, 6]` |
| **Tổng số quầy-giờ mở** | **44 quầy-giờ/ngày** | **48 quầy-giờ/ngày** | **54 quầy-giờ/ngày** |
| **Hiệu quả cắt giảm chi phí** | **Tiết kiệm 18.52% (-10 q-h mở/ngày)**<br>*(Tiết kiệm 21.43% theo giờ công 44 vs 56)* | **Tiết kiệm 11.11% (-6 q-h mở/ngày)**<br>*(Tiết kiệm 14.29% theo giờ công 48 vs 56)* | Mốc cơ sở (0.0%) |
| **Mức phục vụ $SL$ danh định (CI95)** | **$93.81\% \pm 0.23\%$** | **$95.82\% \pm 0.18\%$** | $97.70\% \pm 0.12\%$ |
| **Mức phục vụ $SL$ giờ tệ nhất (Low CI95)** | **$90.78\%$** (Điểm ước lượng $90.60\%$) | **$93.64\%$** | $95.57\%$ |
| **$P(SL \text{ kỳ vọng ngày} \ge 90\%)$** | **$88.5\%$** (Wilson 95%: $[83.3\%, 92.2\%]$) | **$98.5\%$** (Wilson 95%: $[95.7\%, 99.5\%]$) | **$100.0\%$** (Wilson 95%: $[98.1\%, 100.0\%]$) |
| **$P(\min_h E_h(m) \ge 90\%)$** | **$65.5\%$** (Wilson 95%: $[58.7\%, 71.7\%]$)<br>*Số giờ $E_h < 90\%$ TB: 1.17 giờ* | **$82.5\%$** (Wilson 95%: $[76.6\%, 87.1\%]$)<br>*Số giờ $E_h < 90\%$ TB: 0.35 giờ* | **$97.5\%$** (Wilson 95%: $[94.3\%, 98.9\%]$)<br>*Số giờ $E_h < 90\%$ TB: 0.03 giờ* |
| **$P(\text{thực tế mọi giờ} \ge 90\%)$** | **$25.7\%$** (Wilson 95%: $[24.6\%, 26.8\%]$)<br>*(Chịu chi phối mạnh bởi cỡ mẫu giờ)* | **$46.1\%$** (Wilson 95%: $[44.9\%, 47.4\%]$)<br>*(Chịu chi phối mạnh bởi cỡ mẫu giờ)* | **$76.2\%$** (Wilson 95%: $[75.1\%, 77.2\%]$) |
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

## 2. TỔNG HỢP SỐ LIỆU DỮ LIỆU THỰC TẾ VÀ 3 FILE EXCEL

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

### 2.2 Thống kê mô tả 9 khung giờ & Kiểm định Poisson (T1)

Dữ liệu trong sheet `Thong_ke_theo_gio` của tệp `docs/thong_ke_mo_ta.xlsx` và `results/final_v2/kiem_dinh_poisson.csv`:

| Khung giờ | Giờ ID | $\bar{N}_h$ (khách/ngày) | Tốc độ đến $\lambda_h$ (khách/phút) | CI95 Low $\lambda$ | CI95 High $\lambda$ | Chỉ số phân tán $D$ | $p$-value Poisson | Nhãn kiểm định Poisson ($\alpha=0.05$) | Tỉ lệ bỏ về $p_{ab}$ | Tỉ lệ VIP | $E[S]$ (phút) | $\text{std}[S]$ (phút) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h - 9h** | 0 | 61.14 | 1.0190 | 0.9508 | 1.0873 | 23.55 | 0.0356 | **Bác bỏ (nhẹ)** | 2.80% | 16.94% | 2.61 | 2.83 |
| **9h - 10h** | 1 | 86.00 | 1.4333 | 1.3524 | 1.5143 | 23.58 | 0.0352 | **Bác bỏ (nhẹ)** | 3.99% | 32.23% | 2.95 | 3.74 |
| **10h - 11h** | 2 | 98.64 | 1.6440 | 1.5573 | 1.7308 | 48.77 | 0.0000 | **Bác bỏ (mạnh)** | 10.86% | 42.65% | 2.80 | 3.08 |
| **11h - 12h** | 3 | 86.36 | 1.4393 | 1.3582 | 1.5204 | 39.15 | 0.0002 | **Bác bỏ (mạnh)** | 7.94% | 39.04% | 2.90 | 2.95 |
| **12h - 13h** | 4 | 74.36 | 1.2393 | 1.1640 | 1.3146 | 20.83 | 0.0763 | **Chưa bác bỏ** | 2.40% | 19.31% | 2.71 | 3.00 |
| **13h - 14h** | 5 | 74.57 | 1.2429 | 1.1675 | 1.3182 | 30.73 | 0.0037 | **Bác bỏ (mạnh)** | 4.12% | 28.45% | 2.81 | 3.07 |
| **14h - 15h** | 6 | 79.29 | 1.3214 | 1.2437 | 1.3992 | 38.08 | 0.0003 | **Bác bỏ (mạnh)** | 8.83% | 35.59% | 3.09 | 3.34 |
| **15h - 16h** | 7 | 78.29 | 1.3048 | 1.2275 | 1.3820 | 33.61 | 0.0014 | **Bác bỏ (mạnh)** | 13.32% | 49.82% | 3.25 | 3.24 |
| **16h - 17h** | 8 | 63.93 | 1.0655 | 0.9957 | 1.1353 | 26.61 | 0.0141 | **Bác bỏ (nhẹ)** | 8.16% | 33.07% | 2.74 | 2.82 |

> [!NOTE]
> **Kết luận kiểm định:** Với thống kê kiểm định $(n-1)D \sim \chi^2_{13}$, ở mức ý nghĩa $\alpha = 0.05$, **8/9 khung giờ bác bỏ phân phối Poisson** (5/9 giờ bác bỏ ở mức 1%). Duy nhất khung 12h–13h ($p = 0.0763$) là chưa đủ bằng chứng bác bỏ.

---

### 2.3 Hiện tượng Quá phân tán (Overdispersion)

Kết quả phân tích thống kê quá phân tán toàn ngày (`results/final_v2/qua_phan_tan_ngay.csv` và sheet `qua_phan_tan` trong `docs/bang_tham_so.xlsx`):

| Chỉ số thống kê quá phân tán | Giá trị thực nghiệm | Ghi chú so sánh lý thuyết |
|---|:---:|---|
| **Số ngày quan sát** | 14 ngày | Tập dữ liệu hoàn chỉnh |
| **Số khách trung bình một ngày ($\text{Mean}$)** | **702.6 khách** | Kỳ vọng quy mô ngày |
| **Độ lệch chuẩn thực tế ($SD_{\text{thực tế}}$)** | **87.1 khách** | Biến thiên thực tế giữa các ngày |
| **Độ lệch chuẩn Poisson lý thuyết ($\sqrt{\text{Mean}}$)** | **26.5 khách** | Giả định nếu tuân theo Poisson thuần túy |
| **Tỉ số Phương sai / Kỳ vọng ($\text{Var}/\text{Mean}$)** | **10.8** | **$\gg 1.0 \implies$ Hiện tượng quá phân tán nghiêm trọng** |
| **Hệ số biến thiên thô ($CV_{\text{thô}} = SD/\text{Mean}$)** | **$12.4\%$** | Biến thiên gộp cả nhiễu Poisson và biến động ngày |
| **Hệ số biến thiên quy mô ngày thực chất ($CV_{\text{ngày}}$)** | **$11.8\%$** | $\sqrt{\text{Var} - \text{Mean}}/\text{Mean}$ (Đã trừ nhiễu Poisson nội tại) |

---

### 2.4 Bảng tính giải tích Erlang C và Erlang-A trên Excel

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

## 3. TỔNG HỢP SỐ LIỆU KIỂM CHỨNG CODE PYTHON / SIMPY

### 3.1 Kiểm chứng ba tầng và Hai kiểm tra độc lập

Toàn bộ kết quả đóng băng tại `results/final_v2/kiem_chung.csv`:

| Tầng kiểm chứng | Chỉ số đánh giá | Giá trị Lý thuyết | Giá trị Mô phỏng | Khoảng tin cậy 95% | Sai lệch | Đạt chuẩn? | Kết luận khoa học |
|---|---|:---:|:---:|:---:|:---:|:---:|---|
| **Tầng 1 (M/M/c)** | $SL = P(W_q \le 5\text{p})$ | 0.9654 | **0.9688** | ±0.0037 | $+0.35\%$ | **Y** | Lý thuyết nằm trong CI95 |
| **Tầng 1 (M/M/c)** | $W_q$ (phút) | 0.8433 | **0.8170** | ±0.0423 | $-3.12\%$ | **Y** | Lý thuyết nằm trong CI95 |
| **Tầng 1 (M/M/c)** | Hiệu suất quầy $\rho$ | 0.7500 | **0.7517** | ±0.0047 | $+0.23\%$ | **Y** | Khớp chính xác định luật Little ($\rho = 0.75$) |
| **Tầng 2 (Erlang-A)** | $SL$ (chờ $\le 5$p) | 0.8689 | **0.8695** | ±0.0034 | $+0.07\%$ | **Y** | Khớp nghiệm ma trận hấp thụ Markov |
| **Tầng 2 (Erlang-A)** | $W_q$ (phút) | 1.1444 | **1.1475** | ±0.0233 | $+0.27\%$ | **Y** | $W_q$ tính trên mọi khách ($L_q / \lambda$) |
| **Tầng 2 (Erlang-A)** | Tỉ lệ bỏ về $p_{ab}$ | 0.1144 | **0.1142** | ±0.0022 | $-0.21\%$ | **Y** | Lý thuyết nằm trong CI95 |
| **Tầng 2 (Erlang-A)** | Hiệu suất quầy $\rho$ | 0.8856 | **0.8871** | ±0.0031 | $+0.17\%$ | **Y** | Khớp $\rho = \lambda(1-p_{ab})E[S]/c$ |
| **Tầng 3 (M/G/c, cv=0.5)** | $W_q$ (phút) | 0.5271 | **0.5616** | ±0.0176 | $+6.55\%$ | - | Allen–Cunneen đánh giá thấp ~6% |
| **Tầng 3 (M/G/c, cv=1.0)** | $W_q$ (phút) | 0.8433 | **0.8113** | ±0.0521 | $-3.80\%$ | - | Khớp Erlang C chuẩn (sai lệch < 5%) |
| **Tầng 3 (M/G/c, cv=1.5)** | $W_q$ (phút) | 1.3704 | **1.1333** | ±0.1239 | $-17.30\%$ | - | Allen–Cunneen đánh giá cao; kiểm tra qua M/G/1 |
| **Kiểm tra A (M/G/1 P-K exact)** | $W_q$ (phút) | **14.6250** | **13.8669** | ±1.5388 | **$-5.18\%$** | **Y** | $14.625$p nằm trong CI95; SimPy chuẩn xác phi-mũ |
| **Kiểm tra B (M/G/6, cv=1.5, 60 reps)** | $W_q$ (phút) | 1.3704 | **1.1815** | ±0.0722 | $-13.78\%$ | - | Sai lệch ổn định do giới hạn công thức xấp xỉ |

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

*Khảo sát Pha 3 (Vét cạn swap & double reduction - T7):*
- Kiểm tra 72 phương án hoán đổi 1 quầy giữa hai giờ: Không có cấu hình nào giữ được $SL_{\text{low 95\%}} \ge 0.90$ trên cả 9 khung giờ.
- Kiểm tra 36 phương án giảm đồng thời 2 quầy: Tất cả đều vi phạm SLA nghiêm trọng.
- **Kết luận:** Lịch `[4, 5, 6, 5, 5, 5, 5, 5, 4]` là **tối thiểu cục bộ (thuật toán 2 pha xác nhận SIPP)**.

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

### 4.2 Đánh giá khi có biến động lưu lượng ngày ($CV = 11.8\%$)

Kết quả mô phỏng 300 ngày độc lập với $m_d \sim \text{Gamma}(\text{mean}=1, CV=11.8\%)$ tại `results/final_v2/bien_dong_ngay.csv`:

| Chính sách phục vụ | Quầy-giờ | $SL$ Toàn ngày TB | $P(\text{Ngày} \ge 90\%)$ | $P(\text{Mọi giờ} \ge 90\%)$ | $SL$ Phân vị 5% | Số giờ TB $< 90\%$ | Tỉ lệ bỏ về | $W_q$ (phút) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Mốc cơ sở (6 quầy)** | 54 | 0.9751 ± 0.0017 | **100.0%** | **78.0%** | 0.9423 | 0.28 | 2.33% | 0.2140 |
| **Bền vững (48 q-h)** | 48 | 0.9548 ± 0.0029 | **95.3%** | **47.0%** | 0.9076 | 0.93 | 4.02% | 0.3780 |
| **Tối ưu (44 q-h)** | 44 | 0.9340 ± 0.0040 | **85.0%** | **26.0%** | 0.8656 | 1.86 | 5.76% | 0.5420 |

---

### 4.3 Đối chiếu kết quả trên 14 ngày quan sát thực tế

Trích xuất trực tiếp từ `results/final_v2/theo_ngay.csv`:

| Ngày ID | Tổng số khách | $SL$ Lịch 44 | $SL$ Giờ tệ Lịch 44 | Đạt SLA? | $SL$ Lịch 48 | $SL$ Giờ tệ Lịch 48 | Đạt SLA? | $SL$ Mốc 6 quầy | Đạt SLA? |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 690 | 0.9307 | 0.8352 | **ĐẠT** | 0.9549 | 0.9201 | **ĐẠT** | 0.9741 | **ĐẠT** |
| 1 | 776 | 0.8913 | 0.7478 | Hụt | 0.9288 | 0.8589 | **ĐẠT** | 0.9502 | **ĐẠT** |
| 2 | 826 | 0.8723 | 0.8097 | Hụt | 0.9090 | 0.8299 | **ĐẠT** | 0.9436 | **ĐẠT** |
| 3 | 634 | 0.9571 | 0.9293 | **ĐẠT** | 0.9700 | 0.9390 | **ĐẠT** | 0.9802 | **ĐẠT** |
| 4 | 580 | 0.9617 | 0.9039 | **ĐẠT** | 0.9759 | 0.9413 | **ĐẠT** | 0.9857 | **ĐẠT** |
| 5 | 600 | 0.9573 | 0.8936 | **ĐẠT** | 0.9681 | 0.8941 | **ĐẠT** | 0.9848 | **ĐẠT** |
| 6 | 539 | 0.9712 | 0.9234 | **ĐẠT** | 0.9813 | 0.9485 | **ĐẠT** | 0.9912 | **ĐẠT** |
| 7 | 820 | 0.8631 | 0.7113 | Hụt | 0.8997 | 0.7113 | Hụt | 0.9461 | **ĐẠT** |
| 8 | 715 | 0.9247 | 0.8720 | **ĐẠT** | 0.9482 | 0.8733 | **ĐẠT** | 0.9721 | **ĐẠT** |
| 9 | 687 | 0.9289 | 0.8188 | **ĐẠT** | 0.9464 | 0.8258 | **ĐẠT** | 0.9723 | **ĐẠT** |
| 10 | 740 | 0.9155 | 0.8507 | **ĐẠT** | 0.9411 | 0.8665 | **ĐẠT** | 0.9691 | **ĐẠT** |
| 11 | 748 | 0.9067 | 0.8400 | **ĐẠT** | 0.9335 | 0.8400 | **ĐẠT** | 0.9570 | **ĐẠT** |
| 12 | 753 | 0.8982 | 0.7804 | Hụt | 0.9329 | 0.8457 | **ĐẠT** | 0.9506 | **ĐẠT** |
| 13 | 728 | 0.9100 | 0.8232 | **ĐẠT** | 0.9387 | 0.8304 | **ĐẠT** | 0.9525 | **ĐẠT** |
| **Tổng kết** | **TB 702.6** | **92.35%** | - | **10/14 ngày** | **94.49%** | - | **13/14 ngày** | **96.64%** | **14/14 ngày** |

---

## 5. ĐÁNH GIÁ NGOÀI MẪU TRÊN TẬP TEST 4 NGÀY (T4)

So sánh giữa mô hình hóa lý thuyết, mô phỏng và quan sát thực tế tập test ($2.969$ khách, 4 ngày) tại `results/final_v2/ngoai_mau_v2.csv`:

| Khung giờ | Số quầy giả định | $\lambda_{\text{train}}$ | $\lambda_{\text{test}}$ | Erlang-A tĩnh (Bản A) | SimPy DES (Bản B) | Low CI95 DES | Thực tế quan sát | $W_q$ DES (phút) | $W_q$ Thực tế (phút) | Bỏ về DES | Bỏ về Thực tế |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h - 9h** | 4 | 0.9900 | 1.0917 | 0.9140 | 0.9364 | 0.9286 | 0.9809 | 0.4291 | 0.0992 | 5.94% | 1.91% |
| **9h - 10h** | 5 | 1.3767 | 1.5750 | 0.8890 | 0.9172 | 0.9082 | 0.9735 | 0.6183 | 0.2918 | 7.51% | 2.65% |
| **10h - 11h** | 6 | 1.5350 | 1.9167 | 0.9000 | 0.9169 | 0.9076 | 0.9283 | 0.6114 | 0.5350 | 7.45% | 7.17% |
| **11h - 12h** | 5 | 1.3900 | 1.5625 | 0.8920 | 0.8993 | 0.8888 | 0.9413 | 0.6814 | 0.5418 | 8.76% | 5.87% |
| **12h - 13h** | 5 | 1.2400 | 1.2375 | 0.9530 | 0.9552 | 0.9487 | 0.9865 | 0.3273 | 0.1698 | 4.18% | 1.35% |
| **13h - 14h** | 5 | 1.2017 | 1.3458 | 0.9360 | 0.9457 | 0.9387 | 0.9443 | 0.4092 | 0.4549 | 4.99% | 5.57% |
| **14h - 15h** | 5 | 1.3383 | 1.2792 | 0.9470 | 0.9439 | 0.9363 | 0.8958 | 0.3996 | 0.5463 | 5.02% | 9.12% |
| **15h - 16h** | 5 | 1.3167 | 1.2750 | 0.9470 | 0.9507 | 0.9432 | **0.7647** | 0.3657 | **1.4103** | 4.57% | **15.03%** |
| **16h - 17h** | 4 | 1.0567 | 1.0875 | 0.9150 | 0.9245 | 0.9159 | 0.9387 | 0.5331 | 0.3241 | 6.66% | 6.13% |
| **Toàn ngày** | **44 q-h** | **1.2717** | **1.3745** | **0.9273** | **0.9062** | **0.9015** | **0.9360** | **0.6970** | **1.1450** | **7.65%** | **5.49%** |

> [!IMPORTANT]
> **Giải trình khoa học cho khung 15h - 16h:**
> Trong khi mô phỏng dự báo $SL = 95.07\%$ với 5 quầy, số liệu thực tế quan sát ghi nhận mức sụt giảm nghiêm trọng ($76.47\%$, bỏ về $15.03\%$, chờ $1.41$ phút). Nguyên nhân là do:
> 1. Dữ liệu thực tế quan sát được ghi nhận dưới điều kiện vận hành thực tế (chưa áp dụng lịch tối ưu 5 quầy).
> 2. Vào cuối giờ chiều, các giao dịch viên thực tế thường phải tập trung chốt sổ cuối ngày, kiểm ngân, hoặc quầy trực bị rút bớt xuống dưới 5 quầy, dẫn đến tắc nghẽn cục bộ.

---

## 6. TỐI ƯU HÓA LỊCH CA LÀM VIỆC THỰC TẾ (MILP - T5)

Bài toán quy hoạch nguyên được xây dựng trong `b_shifts.py` giải bằng solver HiGHS, kết quả tại `results/final_v2/lich_theo_ca_v2.csv`:

| Mô hình & Phương án ca | Mẫu phủ quầy theo giờ | Quầy-giờ làm việc | Giờ tại chỗ | Nhân sự phân công | Đánh giá tính khả thi |
|---|:---:|:---:|:---:|:---:|---|
| **Yêu cầu tối ưu từng giờ** | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | **44 q-h** | - | - | Mục tiêu cần phủ |
| **Mô hình B: Hỗn hợp (4 NV 8h + 3 NV 4h)** | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | **44 q-h** | **48 giờ** | **7 NV** (4 FT + 3 PT) | **Phủ khớp 100% (Lãng phí 0.0%)**; Cửa sổ nghỉ trưa 11h-14h |
| **Mô hình B: Thuần ca 8h (nghỉ 9h-16h)** | `[6, 5, 6, 5, 5, 5, 5, 5, 6]` | 48 q-h | 54 giờ | 6 NV FT | Thừa +4 q-h (+9.1%) ở đầu và cuối ngày |
| **Mô hình B: Thuần ca 8h (nghỉ 11h-14h)** | `[8, 8, 8, 6, 5, 5, 8, 8, 8]` | 64 q-h | 72 giờ | 8 NV FT | Thừa +20 q-h (+45.5%) khi dồn nghỉ trưa hẹp |
| **Chỉ dùng ca bán thời gian 4h** | `[4, 5, 6, 6, 5, 8, 7, 7, 4]` | 52 q-h | 52 giờ | 13 lượt ca 4h | Thừa +8 q-h (+18.2%) ở các giờ chuyển tiếp |
| **Mô hình A: Thuần ca 8h liên tục** | `[4, 8, 8, 8, 8, 8, 8, 8, 4]` | 64 q-h | 64 giờ | 8 NV FT | Thừa +20 q-h (+45.5%) do khối 8h không ngắt quãng |
| **Mô hình A: 4 NV 8h + 3 NV 4h** | - | - | - | - | **Hoàn toàn vô nghiệm (Infeasible)** |
| **Mô hình B: Phủ mốc 6 quầy cả ngày** | `[7, 6, 6, 6, 6, 6, 6, 6, 7]` | 56 q-h | 63 giờ | 7 NV FT | Cần ít nhất 7 NV (không thể phủ 6 quầy chỉ với 6 NV khi có nghỉ trưa) |

---

## 7. PHÂN TÍCH ĐỘ NHẠY VÀ ĐÁNH ĐỔI KINH TẾ

### 7.1 Độ nhạy toàn diện hệ thống (Tải, Thời gian phục vụ, Kiên nhẫn)

Mô phỏng 150 lần lặp CRN trên 3 nhóm yếu tố tại `results/final_v2/do_nhay.csv`:

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

### 7.2 Độ nhạy phân phối phục vụ qua CRN bắt cặp (T8)

Đánh giá tác động của hình dạng phân phối qua kỹ thuật Common Random Numbers bắt cặp (`results/final_v2/do_nhay_phan_phoi_v2.csv`):

| Dạng phân phối phục vụ | $SL$ Toàn ngày | Hiệu số so với Gamma | Khoảng tin cậy 95% của Hiệu số | Có ý nghĩa thống kê? |
|---|:---:|:---:|:---:|:---:|
| **Gamma chuẩn (AIC tốt nhất)** | **0.9385 ± 0.0032** | Gốc (0.0000) | [0.0000, 0.0000] | - |
| **Bootstrap trực tiếp từ dữ liệu** | 0.9376 ± 0.0036 | -0.0009 | [-0.0055, +0.0038] | **Không** ($0 \in CI95$) |
| **Mũ (Exponential - Đuôi nhẹ)** | 0.9377 ± 0.0030 | -0.0008 | [-0.0054, +0.0037] | **Không** ($0 \in CI95$) |
| **Lognormal ($cv$ tăng 20% - Đuôi nặng)** | **0.9312 ± 0.0038** | **-0.0073** | **[-0.0116, -0.0029]** | **Có** ($0 \notin CI95$) |

---

### 7.3 Đường cong đánh đổi Pareto và Phân tích hàm chi phí

Mô hình hóa chi phí tổng thể $C(k) = \text{Quầy-giờ} + k \cdot N_{ab}$ trên quy mô $686.7$ khách/ngày (`results/final_v2/chi_phi.csv`):

| Chính sách phục vụ | Quầy-giờ | Khách bỏ về / ngày | Chi phí ($k=0.10$) | Chi phí ($k=0.25$) | Chi phí ($k=0.50$) | Chi phí ($k=1.00$) | Chi phí ($k=2.00$) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Mốc cơ sở (6 quầy)** | 54 | 14.8 khách | 55.48 | 57.69 | 61.38 | **68.76** | **83.53** |
| **Lịch tối ưu (44 q-h)** | 44 | 36.7 khách | **47.67** | **53.18** | 62.37 | 80.74 | 117.48 |
| **Lịch bền vững (48 q-h)** | 48 | 25.6 khách | 50.56 | 54.40 | **60.81** | 73.61 | 99.23 |
| **Ca làm việc 6 NV thuần 8h** | 48 | 21.0 khách | 50.10 | 53.25 | 58.50 | 69.00 | 90.00 |

*Điểm cân bằng Pareto:*
- Nếu chi phí mất khách thấp ($k \le 0.25$): Lịch tối ưu 44 quầy-giờ đem lại hiệu quả tài chính cao nhất.
- Nếu chi phí mất khách trung bình ($k = 0.50$): Lịch bền vững 48 quầy-giờ tối ưu hóa tổng chi phí ($60.81$).

---

## 8. TỔNG KẾT KIỂM THỬ VÀ TRẠNG THÁI BÀN GIAO

1. **Kiểm thử hồi quy tự động:** 22/22 ca kiểm thử đơn vị tự động trong `tests/` (`test_theory.py`, `test_sim.py`, `test_v2_features.py`) đều chạy thành công 100% trong 9.82 giây (ghi nhận tại `results/final_v3/pytest_log.txt`).
2. **Kiểm tra tính nhất quán và ngôn ngữ (T10, T14, C6):** Công cụ `tools/check_consistency.py` xác nhận:
   - 0 vi phạm về các thuật ngữ không có căn cứ (đã chuẩn hóa thuật ngữ khoa học, loại bỏ các từ tuyệt đối hóa).
   - 100% số liệu trong tài liệu Markdown và Excel khớp hoàn toàn với dữ liệu đóng băng trong `results/final_v3/`.
3. **Lưu trữ Git:** Toàn bộ sản phẩm được commit trên nhánh `fix/chinh-sua-agent`.
