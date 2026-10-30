# BẢNG TỔNG HỢP SỐ LIỆU CUỐI CÙNG VÀ ĐÁNH GIÁ TOÀN DIỆN DỰ ÁN (PHIÊN BẢN V5)

**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu cho quầy giao dịch ngân hàng  
**Thời điểm tổng hợp:** 2026-10-30 (V5: tối ưu trực tiếp theo giờ công ca M6, chọn lịch theo xác suất đạt SLA ngày M7, mở thêm quầy theo hàng chờ M8, kiên nhẫn Weibull S12, dự báo sớm fit trên train S13, cluster bootstrap S14, λ nửa giờ S15, chạy song song P1–P2; đóng băng tại `results/final_v5/`. Mọi chỉ số của V4 giữ nguyên từng byte, xem mục 8)  
**Bộ dữ liệu:** Anonymous Bank Call Center (Technion SEE Center), 14 ngày làm việc, $9.836$ giao dịch  
**Lệnh tái lập:** `python main.py --stage all --reps-scale 1.0` (15.1 phút với 8 tiến trình song song; seed chọn lịch `1000`, seed đánh giá `50000`)

---

## MỤC LỤC

1. [BẢNG QUYẾT ĐỊNH QUẢN TRỊ TỔNG THỂ](#1-bảng-quyết-định-quản-trị-tổng-thể)
2. [TỔNG HỢP DỮ LIỆU THỰC TẾ VÀ KIỂM ĐỊNH PHÂN PHỐI](#2-tổng-hợp-dữ-liệu-thực-tế-và-kiểm-định-phân-phối)
3. [TỔNG HỢP SỐ LIỆU KIỂM CHỨNG CODE PYTHON / SIMPY](#3-tổng-hợp-số-liệu-kiểm-chứng-code-python--simpy)
4. [BẢNG SO SÁNH CÁC CHÍNH SÁCH PHỤC VỤ (DANH ĐỊNH & BIẾN ĐỘNG NGÀY)](#4-bảng-so-sánh-các-chính-sách-phục-vụ-danh-định--biến-động-ngày)
5. [ĐÁNH GIÁ NGOÀI MẪU VỚI KHOẢNG DỰ BÁO 95% (PI95) VÀ HOLM-BONFERRONI (S6, M4)](#5-đánh-giá-ngoài-mẫu-với-khoảng-dự-báo-95-pi95-và-holm-bonferroni-s6-m4)
6. [TỐI ƯU HÓA LỊCH CA LÀM VIỆC THỰC TẾ (MILP)](#6-tối-ưu-hóa-lịch-ca-làm-việc-thực-tế-milp)
7. [PHÂN TÍCH ĐỘ NHẠY VÀ ĐÁNH ĐỔI KINH TẾ](#7-phân-tích-độ-nhạy-và-đánh-đổi-kinh-tế)
8. [ĐỐI CHIẾU V4 → V5](#8-đối-chiếu-v4--v5)
9. [TỔNG KẾT KIỂM THỬ VÀ TRẠNG THÁI BÀN GIAO](#9-tổng-kết-kiểm-thử-và-trạng-thái-bàn-giao)
10. [HẠN CHẾ CẦN NÊU KHI BÁO CÁO](#10-hạn-chế-cần-nêu-khi-báo-cáo)

---

## 1. BẢNG QUYẾT ĐỊNH QUẢN TRỊ TỔNG THỂ

**Kết luận một dòng:** cần tối thiểu **48 giờ công nhân viên/ngày**, xếp **4 ca 8h + 4 ca 4h** (nghỉ trưa 11h–14h) để mở quầy theo Lịch 48 `[4, 6, 6, 6, 5, 5, 6, 5, 5]`, để $\ge 90\%$ khách chờ dưới 5 phút ở mọi giờ (cận dưới CI95). Không cách xếp ca nào dưới 48 giờ công đạt tiêu chí này, kể cả khi cho nghỉ trưa linh hoạt 9h–16h (M6, mục 7.9). Kết luận không đổi khi thay kiên nhẫn mũ bằng Weibull (S12, mục 7.12) hay dùng λ theo nửa giờ (S15, mục 7.13).

- **Số quầy-giờ mở ít nhất** vẫn là **45** (`[4, 5, 6, 5, 5, 5, 5, 5, 5]`), nhưng Lịch 45 cũng tốn 48 giờ công vì không phủ đúng được bằng ca 8h/4h (mục 6). Cùng 48 giờ công, Lịch 48 cho SL cao hơn và bỏ về thấp hơn.
- **Biến động giữa các ngày:** Lịch 48 đạt SLA ở khoảng 95% số ngày; muốn $\ge 95\%$ số ngày (cận dưới Wilson) cần **52 giờ công** (M7, mục 7.10).
- **Nếu có 1 người dự phòng:** Lịch 45 + mở thêm 1 quầy khi hơn 2 người chờ liên tục 5 phút đạt SLA ở 97.3% số ngày với trung bình 46.17 quầy-giờ mở (M8, mục 7.11).
- **Nếu khách quầy kiên nhẫn hơn khách tổng đài:** số quầy-giờ mở tăng lên 46 (kiên nhẫn 15–60 phút) và tối đa 48 (không ai bỏ về) (M1, mục 7.5).

Số liệu trích từ `results/final_v5/` (300 lần lặp, seed đánh giá tách khỏi seed chọn lịch):

| Tiêu chí quản trị | Lịch 45: ít quầy-giờ mở nhất | Lịch 48: khuyến nghị (ít giờ công nhất, M6) | Mốc cơ sở: Hằng số 6 quầy |
|---|:---:|:---:|:---:|
| **Lịch quầy chi tiết theo giờ (8h - 17h)** | `[4, 5, 6, 5, 5, 5, 5, 5, 5]` | `[4, 6, 6, 6, 5, 5, 6, 5, 5]` | `[6, 6, 6, 6, 6, 6, 6, 6, 6]` |
| **Tổng số quầy-giờ mở** | **45 quầy-giờ/ngày** | **48 quầy-giờ/ngày** | **54 quầy-giờ/ngày** |
| **Tiết kiệm quầy-giờ mở so với mốc 54** | **16.67% (-9 q-h/ngày)** | **11.11% (-6 q-h/ngày)** | Mốc (0.0%) |
| **Mức phục vụ $SL$ danh định (CI95)** | **$94.23\% \pm 0.22\%$** | **$95.79\% \pm 0.17\%$** | $97.63\% \pm 0.12\%$ |
| **Mức phục vụ $SL$ giờ tệ nhất (Low CI95)** | **$92.36\%$** (11h–12h, 300 lần lặp)<br>*(M5, 1.646 lần lặp: 11h–12h là giờ tệ nhất với xác suất 99.7%, cận dưới $92.16\%$)* | **$93.27\%$** (15h–16h) | $94.94\%$ (10h–11h) |
| **$P(SL \text{ kỳ vọng ngày} \ge 90\%)$**, $CV_{\text{ngày}} = 14.0\%$ | **$88.0\%$** (Wilson 95%: $[82.8\%, 91.8\%]$) | **$96.0\%$** (Wilson 95%: $[92.3\%, 98.0\%]$) | **$99.5\%$** (Wilson 95%: $[97.2\%, 99.9\%]$) |
| **$P(\min_h E_h(m) \ge 90\%)$** | **$73.0\%$** (Wilson 95%: $[66.5\%, 78.7\%]$)<br>*Số giờ $E_h < 90\%$ TB: 1.09 giờ* | **$83.5\%$** (Wilson 95%: $[77.7\%, 88.0\%]$)<br>*Số giờ $E_h < 90\%$ TB: 0.51 giờ* | **$93.5\%$** (Wilson 95%: $[89.2\%, 96.2\%]$)<br>*Số giờ $E_h < 90\%$ TB: 0.10 giờ* |
| **$P(\text{thực tế mọi giờ} \ge 90\%)$** | **$29.0\%$** (Wilson 95%: $[27.8\%, 30.1\%]$)<br>*(Bị chi phối mạnh bởi cỡ mẫu giờ)*<br>bootstrap [25.4%, 32.3%] | **$43.9\%$** (Wilson 95%: $[42.7\%, 45.2\%]$)<br>bootstrap [40.0%, 47.5%] | **$71.8\%$** (Wilson 95%: $[70.6\%, 72.9\%]$)<br>bootstrap [68.3%, 74.9%] |
| **$P(\text{gộp tháng 20 ngày mọi giờ} \ge 90\%)$** | **$65.0\%$** (Wilson 95%: $[59.4\%, 70.2\%]$) | **$78.3\%$** (Wilson 95%: $[73.3\%, 82.6\%]$) | **$92.7\%$** (Wilson 95%: $[89.1\%, 95.1\%]$) |
| **Số ngày thực tế 14 ngày đạt SLA** | **12/14 ngày (85.7% [60.1%, 96.0%])**<br>*(Hụt ngày 2: 87.66% và ngày 7: 88.36%)* | **14/14 ngày (100.0% [78.5%, 100.0%])** | **14/14 ngày (100.0% [78.5%, 100.0%])** |
| **Mức phục vụ Khách VIP ($W_q \le 2$ phút)** | **$95.58\%$** | **$96.74\%$** | $98.22\%$ |
| **Thời gian chờ trung bình $W_q$** | **$0.4628 \pm 0.0150$ phút (~27.8 giây)** | **$0.3432 \pm 0.0123$ phút (~20.6 giây)** | $0.2024 \pm 0.0091$ phút (~12.1 giây) |
| **Tỉ lệ khách hàng bỏ về trung bình** | **$4.99\% \pm 0.16\%$** | **$3.70\% \pm 0.13\%$ (giảm 26% khách mất)** | $2.17\% \pm 0.10\%$ |
| **Hiệu suất sử dụng quầy giao dịch $\rho$** | **$70.85\% \pm 0.39\%$** | **$67.33\% \pm 0.39\%$** | $60.77\% \pm 0.37\%$ |
| **Phương án tổ chức ca (nghỉ trưa 11h–14h, ca 8h + 4h)** | **5 NV 8h + 2 NV 4h = 48 q-h công**<br>*(Không có cách phủ đúng 45 q-h; dư 3 q-h)* | **4 NV 8h + 4 NV 4h = 48 q-h công**<br>*(Phủ đúng 48 q-h; tốt nhất trong 33 lịch khả thi ở 48 giờ công, M6)* | **6 NV 8h + 2 NV 4h = 56 q-h công**<br>*(Không phủ đúng được 54; dư 2 q-h)* |
| **Độ bền khi nhu cầu tăng +10%** | Giờ tệ nhất Low CI95 **$87.93\%$** (SL ngày $92.00\%$) | Giờ tệ nhất Low CI95 **$90.87\%$** (SL ngày $94.23\%$) | Giờ tệ nhất Low CI95 $92.67\%$ |
| **Quy tắc kích hoạt vận hành** | Áp dụng khi $\hat{V} \le 803$ khách/ngày (dự báo sớm 8h–10h: $r=0.842, p=0.0002$) | Chuyển sang lúc 10h khi $\hat{V} > 803$ khách/ngày | Mốc đối chiếu |

> [!IMPORTANT]
> **Vì sao khuyến nghị đổi từ Lịch 45 (V4) sang Lịch 48 (V5):** với nghỉ trưa 11h–14h và ca 8h/4h, Lịch 45 và Lịch 48 **cùng tốn 48 giờ công**. V4 tối ưu quầy-giờ mở trước rồi mới xếp ca; V5 (M6) tối ưu thẳng theo giờ công và xác nhận 48 là mức nhỏ nhất. Trong 33 lịch khả thi ở 48 giờ công, Lịch 48 đứng đầu ở cả SL, giờ tệ nhất, bỏ về và độ bền (mục 7.9). Lịch 45 chỉ đáng chọn khi giờ mở quầy có chi phí riêng (điện, hệ thống, quầy) hoặc khi 3 giờ công dư được dùng cho việc khác, chẳng hạn làm người dự phòng của chính sách M8.

**Bổ sung V5: chính sách mở thêm quầy theo hàng chờ (M8).** Cùng bộ seed riêng của M8 (`results/final_v5/chinh_sach_tang_quay.csv`, 300 lần lặp mỗi kịch bản, 40 lần lặp mỗi ngày thực tế), nên SL của Lịch 45/48 cố định hơi khác bảng trên:

| Phương án | Quầy-giờ mở TB (danh định) | $P(SL_{\text{ngày}} \ge 90\%)$, $CV_{\text{ngày}}$ 14% | Nhu cầu +10%: giờ tệ nhất Low CI95 | Ngày thực tế đạt (/14) | Nhân sự |
|---|:---:|:---:|:---:|:---:|---|
| Lịch 45 cố định | 45.00 | 80.3% | 0.8850 | 12 | 48 giờ công |
| **Lịch 48 cố định** | 48.00 | 94.0% | 0.9029 | 14 | **48 giờ công** |
| **Lịch 45 + mở thêm khi > 2 người chờ liên tục 5 phút, tối đa +1** | 46.17 | 97.3% | 0.9193 | 14 | 48 giờ công + 1 người dự phòng |

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

Do số khách thực tế theo ngày bị quá phân tán ở 8/9 giờ, công thức Poisson $1.96 \sqrt{\bar{N}/n}/60$ bị hẹp hơn thực tế $1.4 - 2.1$ lần. Khoảng tin cậy dùng phân phối Student-t với $df=13$ ($t_{0.975; 13} = 2.1604$), tại `results/final_v5/khoang_tin_cay_lambda.csv` và `kiem_dinh_poisson.csv`:

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

> Bảng này tính trên cả 14 ngày (mô tả dữ liệu). Mô hình mô phỏng dùng $\lambda_h$ của **tập train 10 ngày** (bảng 2.4); CI Student-t của tập train ($df=9$) lưu trong `results/final_v5/params.json` (`rates_ci95`, kèm `rates_ci95_poisson` để so sánh).

---

### 2.3 Hiện tượng Quá phân tán (Overdispersion)

Kết quả phân tích quá phân tán toàn ngày (`results/final_v5/qua_phan_tan_ngay.csv`):

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

Tính bằng `b_theory.py` (SIPP, $E[S] = 2.9236$ phút, $\theta = 0.1087$, tham số train), lưu tại `results/final_v5/bang_sipp.csv`. $SL$ Erlang C $= P(W_q \le 5)$ (không có bỏ về); $SL$ Erlang-A $= P(\text{được phục vụ và chờ} \le 5)$:

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

Chi tiết tại `results/final_v5/kiem_dinh_phan_phoi_chi_tiet.csv` và `results/final_v5/cluster_bootstrap_params.csv`:

| Phân phối | Tham số ước lượng | Log-Likelihood | AIC | BIC | KS Stat | KS $p$-value (Bootstrap) | Đánh giá khoa học |
|---|---|:---:|:---:|:---:|:---:|:---:|---|
| **Gamma** | $\text{shape}=1.0955, \text{scale}=2.6688$ ($cs^2 = 0.91$) | -13137.8 | **26279.7** | **26293.2** | 0.0717 | < 0.001 | AIC/BIC thấp nhất, nhưng **bị bác bỏ** |
| **Weibull** | $c=1.0335, \text{scale}=2.9650$ ($cs^2 = 0.94$) | -13148.1 | 26300.2 | 26313.7 | 0.0799 | < 0.001 | Bị bác bỏ |
| **Exponential** | $\text{scale} = 2.9236$ ($cs^2 = 1.00$) | -13154.2 | 26310.4 | 26317.1 | 0.0913 | < 0.001 | Bị bác bỏ |
| **Lognormal** | $s=1.2150, \text{scale}=1.7357$ ($cs^2 = 3.38$) | -13739.5 | 27483.0 | 27496.5 | 0.1159 | < 0.001 | Kém nhất, bị bác bỏ |

- **Kết luận:** với $n = 6.346$ thời gian phục vụ (train), **cả 4 phân phối đều bị bác bỏ** bởi kiểm định KS bootstrap (thống kê KS quy đổi theo cỡ mẫu, mẫu mô phỏng 1.000).
- **Lựa chọn mô hình V4 (M3):** mô phỏng chính lấy mẫu có hoàn lại trực tiếp từ 6.346 thời gian phục vụ train (giữ đúng $cs^2 = 1.20$). Gamma ($cs^2 = 0.91$) đánh giá thấp độ biến động nên chuyển sang phân tích độ nhạy (mục 7.2).
- **Bảng sống sót Kaplan–Meier** (`results/final_v5/patience_km.csv`): đường KM giảm nhanh hơn đường mũ ở vùng chờ ngắn. Khách bỏ về sớm nhiều hơn giả định mũ, nên kiên nhẫn ~ Exponential($\theta$) chỉ là xấp xỉ; ảnh hưởng của kiên nhẫn được kiểm tra ở mục 7.5 (M1) và bằng mô hình Weibull có kiểm duyệt ở mục 7.12 (S12).
- **Khoảng tin cậy Cluster Bootstrap theo ngày (xét tương quan trong ngày):**
  - Thời gian phục vụ trung bình $E[S]$: $[2.8589, 2.9929]$ phút (trung bình mẫu $2.9236$).
  - Tốc độ bỏ về $\theta$: $[0.0936, 0.1182]\text{ phút}^{-1}$ (trung bình mẫu $0.1087$).

---

## 3. TỔNG HỢP SỐ LIỆU KIỂM CHỨNG CODE PYTHON / SIMPY

### 3.1 Kiểm chứng ba tầng và M/G/1 Pollaczek–Khinchine exact 40.000 phút (S8)

Khoảng tin cậy dùng giá trị tới hạn Student-t ($df = n_{\text{reps}} - 1$). Chi tiết tại `results/final_v5/kiem_chung.csv`:

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

Lịch sử 11 bước tại `results/final_v5/lich_toi_uu.csv` (60 lần lặp/bước, seed chọn lịch `1000`; tiêu chí: cận dưới CI95 của SL mọi giờ $\ge 90\%$):

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

Mô hình lồng nhau: $B = 50$ bộ tham số (resample ngày train; mẫu phục vụ resample trực tiếp, không fit lại Gamma) $\times R = 60$ lần lặp/bộ. Chi tiết tại `results/final_v5/phan_ra_phuong_sai.csv` và `bat_dinh_nested.csv`:

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

Dữ liệu tại `results/final_v5/so_sanh_chinh_sach.csv` (seed đánh giá `50000`, tách khỏi seed chọn lịch):

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

Mô phỏng $K$ kịch bản ngày $\times R$ lần lặp để tính chỉ số kỳ vọng $E_h(m) = E[SL_h \mid m]$, tách rời nhiễu lấy mẫu (`results/final_v5/chi_so_ky_vong_dieu_kien.csv`, dòng chuẩn $K=200, R=30$, $CV = 14.0\%$ ước lượng trên train; `results/final_v5/do_nhay_cv_ngay.csv`, $K=100, R=20$):

| Chính sách | CV ngày | $P(E_{day} \ge 90\%)$ [Wilson 95%] | $P(\min_h E_h \ge 90\%)$ [Wilson 95%] | Số giờ $E_h < 90\%$ TB | $P(\text{thực tế mọi giờ} \ge 90\%)$ [Wilson; cluster bootstrap S14] | $P(\text{gộp tháng 20 ngày} \ge 90\%)$ |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Lịch 45** | **14.0% (Chuẩn)** | **88.0% [82.8%, 91.8%]** | **73.0% [66.5%, 78.7%]** | **1.09** | **29.0% [27.8%, 30.1%]**<br>bootstrap [25.4%, 32.3%] | **65.0% [59.4%, 70.2%]** |
|  | 8.0% | 97.0% [91.5%, 99.0%] | 77.0% [67.8%, 84.2%] | 0.44 | 22.4% [20.6%, 24.3%]<br>bootstrap [19.3%, 25.8%] | 73.0% [63.6%, 80.7%] |
|  | 12.0% | 94.0% [87.5%, 97.2%] | 75.0% [65.7%, 82.5%] | 0.72 | 25.8% [23.9%, 27.7%]<br>bootstrap [21.4%, 30.2%] | 71.0% [61.5%, 79.0%] |
|  | 16.0% | 86.0% [77.9%, 91.5%] | 63.0% [53.2%, 71.8%] | 1.40 | 30.3% [28.3%, 32.4%]<br>bootstrap [24.9%, 35.5%] | 59.0% [49.2%, 68.1%] |
|  | 20.0% | 79.0% [70.0%, 85.8%] | 63.0% [53.2%, 71.8%] | 1.68 | 31.9% [29.9%, 34.0%]<br>bootstrap [25.9%, 38.0%] | 61.0% [51.2%, 70.0%] |
| **Lịch 48** | **14.0% (Chuẩn)** | **96.0% [92.3%, 98.0%]** | **83.5% [77.7%, 88.0%]** | **0.51** | **43.9% [42.7%, 45.2%]**<br>bootstrap [40.0%, 47.5%] | **78.3% [73.3%, 82.6%]** |
|  | 8.0% | 99.0% [94.6%, 99.8%] | 92.0% [85.0%, 95.9%] | 0.11 | 41.6% [39.4%, 43.7%]<br>bootstrap [37.8%, 45.4%] | 90.0% [82.6%, 94.5%] |
|  | 12.0% | 98.0% [93.0%, 99.4%] | 90.0% [82.6%, 94.5%] | 0.23 | 41.6% [39.4%, 43.7%]<br>bootstrap [36.9%, 46.4%] | 88.0% [80.2%, 93.0%] |
|  | 16.0% | 94.0% [87.5%, 97.2%] | 76.0% [66.8%, 83.3%] | 0.62 | 43.1% [40.9%, 45.2%]<br>bootstrap [37.4%, 48.9%] | 74.0% [64.6%, 81.6%] |
|  | 20.0% | 90.0% [82.6%, 94.5%] | 73.0% [63.6%, 80.7%] | 0.99 | 43.3% [41.1%, 45.4%]<br>bootstrap [37.0%, 49.4%] | 72.0% [62.5%, 79.9%] |
| **Mốc 54** | **14.0% (Chuẩn)** | **99.5% [97.2%, 99.9%]** | **93.5% [89.2%, 96.2%]** | **0.10** | **71.8% [70.6%, 72.9%]**<br>bootstrap [68.3%, 74.9%] | **92.7% [89.1%, 95.1%]** |
|  | 8.0% | 100.0% [96.3%, 100.0%] | 100.0% [96.3%, 100.0%] | 0.00 | 76.3% [74.3%, 78.1%]<br>bootstrap [73.2%, 79.1%] | 99.0% [94.6%, 99.8%] |
|  | 12.0% | 100.0% [96.3%, 100.0%] | 97.0% [91.5%, 99.0%] | 0.03 | 73.2% [71.2%, 75.1%]<br>bootstrap [69.2%, 77.1%] | 97.0% [91.5%, 99.0%] |
|  | 16.0% | 99.0% [94.6%, 99.8%] | 92.0% [85.0%, 95.9%] | 0.13 | 69.5% [67.4%, 71.5%]<br>bootstrap [64.4%, 74.3%] | 90.0% [82.6%, 94.5%] |
|  | 20.0% | 96.0% [90.2%, 98.4%] | 86.0% [77.9%, 91.5%] | 0.34 | 67.4% [65.3%, 69.4%]<br>bootstrap [61.1%, 73.3%] | 85.0% [76.7%, 90.7%] |

> **Lưu ý thống kê (S14):** khoảng Wilson (dòng trên) của cột $P(\text{thực tế mọi giờ})$ coi mọi ngày-lần lặp là độc lập (dòng chuẩn: 200 × 30 = 6.000; dòng độ nhạy: 100 × 20 = 2.000). Các lần lặp trong cùng một kịch bản có tương quan, nên khoảng này **hẹp hơn thực tế**. Dòng dưới là **khoảng cluster bootstrap**: lấy lại có hoàn lại 200 (hoặc 100) kịch bản, giữ nguyên các lần lặp bên trong, 2.000 lần, phân vị 2.5–97.5%. Khoảng bootstrap rộng gấp khoảng 3 lần và là khoảng nên dùng khi báo cáo. Cột này tăng nhẹ theo CV ở Lịch 45 (22.4% → 31.9%) là do định nghĩa "mọi giờ thực tế" bị chi phối bởi nhiễu nhị thức của từng giờ, không nên diễn giải như xu hướng.

Mô phỏng 300 lần lặp có hệ số nhân ngày ($CV = 14.0\%$, `so_sanh_chinh_sach_bd.csv`): Lịch 45 có SL ngày TB 0.9370, $P(SL_{\text{ngày}} \ge 90\%) = 85.7\%$, phân vị 5% của SL ngày là 0.867; Lịch 48: 0.9542, 95.0%, 0.901; Mốc 54: 0.9734, 99.7%, 0.938.

---

### 4.3 Posterior Predictive Check mô hình nhu cầu ngày (S3)

Kiểm tra qua 1.000 bộ 14 ngày mô phỏng từ mô hình $m_d \sim \text{Gamma}$ với $CV = 14.0\%$ (`results/final_v5/posterior_predictive_check.csv`):

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

1. **Khảo sát ngưỡng lưu lượng** (`results/final_v5/nguong_luu_luong_chi_tiet.csv`, 40 lần lặp mỗi mức):  
   Lịch 45 giữ $SL_{\text{ngày}} \ge 90\%$ đến $V = 800$ khách/ngày (SL 0.9018) và hụt ở $V = 850$ (0.8703). Nội suy tuyến tính cho **$V^* = 803$ khách/ngày**. Lịch 48 vẫn đạt ở 850 (0.9045).
2. **Bộ dự báo OLS sớm lúc 10h (từ số khách 8h–10h), fit trên 10 ngày train (S13)** (`du_bao_som_hoi_quy.csv`):
   $$\hat{V} = 90.9 + 4.20 \cdot (N_{8h-9h} + N_{9h-10h})$$
   Trên train: Pearson $r = 0.907$ ($p = 0.0003$), RMSE $39.7$ khách. **Trên 4 ngày test: RMSE $63.9$ khách.** V4 fit trên cả 14 ngày ($\hat V = 189.6 + 3.49 N$, $r = 0.842$, RMSE trong mẫu 45.3) nên đánh giá quá lạc quan.
3. **Chính sách ghép trên 14 ngày thực tế** ($\hat{V} > 803$ → Lịch 48, ngược lại Lịch 45; `danh_gia_chinh_sach_du_bao_14ngay.csv`):
   - Số ngày dùng Lịch 45: **13/14** (chỉ ngày 13, $\hat{V} = 850.3$, chuyển sang Lịch 48).
   - Quầy-giờ trung bình: **45.21 quầy-giờ/ngày**, tiết kiệm 16.27% so với 54.
   - **Bộ dự báo bỏ lỡ cả 2 ngày hụt SLA:** ngày 2 ($V = 826$, $\hat{V} = 770.6$) và ngày 7 ($V = 820$, $\hat{V} = 770.6$) vượt $V^*$ nhưng dự báo thấp hơn khoảng 50 khách. Ngày 13 được chuyển sang Lịch 48 dù $V$ thực tế chỉ 728. Với sai số ngoài mẫu khoảng 64 khách so với khoảng cách $V^* - \bar{V} \approx 116$, quy tắc này có tác dụng hạn chế; quy tắc phản ứng theo hàng chờ (M8, mục 7.11) thay thế được nó.

---

### 4.5 Đối chiếu 14 ngày thực tế phân định Train/Test (S7)

Mô phỏng 40 lần lặp/ngày với $m_d = N_d / 686.7$, Student-t CI ($df=39$) tại `results/final_v5/theo_14_ngay.csv` và `theo_14_ngay_tong_hop.csv`:

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

So sánh mô phỏng Lịch 45 (1.000 bộ 4 ngày có biến động lưu lượng ngày) với quan sát thực tế tập Test (4 ngày, $2.969$ khách), tại `results/final_v5/ngoai_mau.csv`:

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

Bài toán quy hoạch nguyên trong `b_shifts.py` (solver HiGHS) cho yêu cầu Lịch 45 `[4, 5, 6, 5, 5, 5, 5, 5, 5]`, kết quả tại `results/final_v5/lich_theo_ca.csv`:

| Mô hình & Phương án ca | Mẫu phủ quầy theo giờ | Quầy-giờ làm việc | Giờ tại chỗ | Nhân sự | Dư so với 45 q-h |
|---|:---:|:---:|:---:|:---:|:---:|
| **Mô hình B (nghỉ 11h–14h): hỗn hợp 8h + 4h** | `[5, 5, 6, 5, 5, 5, 6, 6, 5]` | **48** | 53 | **7 NV** (5 ca 8h + 2 ca 4h) | **+3 q-h (+6.7%)** |
| **Mô hình B (nghỉ 11h–14h): hỗn hợp, bắt buộc phủ đúng** | - | - | - | - | **Vô nghiệm** |
| **Mô hình B (nghỉ 9h–16h): chỉ ca 8h** | `[6, 5, 6, 5, 5, 5, 5, 5, 6]` | 48 | 54 | 6 NV ca 8h | +3 q-h (+6.7%) |
| **Mô hình B (nghỉ 11h–14h): chỉ ca 8h** | `[8, 8, 8, 6, 5, 5, 8, 8, 8]` | 64 | 72 | 8 NV ca 8h | +19 q-h (+42.2%) |
| **Chỉ ca 4h** | `[4, 9, 9, 9, 5, 5, 5, 5, 5]` | 56 | 56 | 14 lượt ca 4h | +11 q-h (+24.4%) |
| **Mô hình A: chỉ ca 8h liên tục** | `[4, 9, 9, 9, 9, 9, 9, 9, 5]` | 72 | 72 | 9 NV ca 8h | +27 q-h (+60.0%) |

**Bổ sung** (cùng hàm `solve_shift_scheduling`, mô hình B nghỉ 11h–14h, hỗn hợp 8h + 4h; phương án ca của Lịch 48 nằm trong `toi_uu_theo_ca.csv` của M6, mốc 54 tính riêng):

| Yêu cầu | Mẫu phủ | Quầy-giờ làm việc | Giờ tại chỗ | Nhân sự | Dư |
|---|:---:|:---:|:---:|:---:|:---:|
| Lịch 48 `[4, 6, 6, 6, 5, 5, 6, 5, 5]` | phủ đúng | 48 | 52 | 8 NV (4 ca 8h + 4 ca 4h) | 0 |
| Mốc 54 `[6, 6, 6, 6, 6, 6, 6, 6, 6]` | `[6, 6, 6, 6, 6, 6, 8, 6, 6]` | 56 | 62 | 8 NV (6 ca 8h + 2 ca 4h) | +2 |

Lịch 45 thêm 1 quầy ở 16h–17h so với Lịch 44 của V3. Với ca 4h buổi chiều kết thúc lúc 17h và nghỉ trưa 11h–14h, mẫu `[..., 5, 5, 5, 5, 5]` không còn phủ đúng được (V3: Lịch 44 phủ đúng bằng 4 ca 8h + 3 ca 4h). Hệ quả: tính theo giờ công, Lịch 45 và Lịch 48 cùng chi phí 48 q-h (mục 1). V5 (M6, mục 7.9) bỏ cách làm hai bước "tối ưu quầy-giờ rồi xếp ca" và tối ưu thẳng theo giờ công: 48 là mức nhỏ nhất.

---

## 7. PHÂN TÍCH ĐỘ NHẠY VÀ ĐÁNH ĐỔI KINH TẾ

### 7.1 Độ nhạy toàn diện hệ thống (Tải, Thời gian phục vụ, Kiên nhẫn)

Mô phỏng với số ngẫu nhiên chung (CRN) tại `results/final_v5/do_nhay.csv`:

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

Mô phỏng Lịch 45 với 150 lần lặp, cùng bộ seed (CRN), hiệu số theo cặp so với mô hình chính (thực nghiệm), tại `results/final_v5/do_nhay_phan_phoi.csv`:

| Phân phối phục vụ | $SL$ Toàn ngày (CI95) | Giờ tệ nhất | $SL$ Giờ tệ nhất | Giờ tệ nhất Low CI95 | Hiệu số so với thực nghiệm | CI 95% Hiệu số | Khác biệt có ý nghĩa? |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Thực nghiệm (mô hình chính, $cs^2 = 1.20$)** | **0.9435 ± 0.0030** | 14h - 15h | 0.9277 | **0.9182** | Gốc (0.0000) | - | - |
| **Gamma (AIC tốt nhất, $cs^2 = 0.91$)** | 0.9430 ± 0.0028 | 11h - 12h | 0.9201 | **0.9099** | -0.0005 | [-0.0043, +0.0034] | Không |
| **Exponential ($cs^2 = 1.00$)** | 0.9453 ± 0.0028 | 11h - 12h | 0.9268 | **0.9176** | +0.0017 | [-0.0023, +0.0058] | Không |
| **Lognormal ($cv$ + 20%)** | 0.9344 ± 0.0039 | 11h - 12h | 0.9111 | **0.8979** | **-0.0091** | **[-0.0140, -0.0042]** | **Có** (giờ tệ nhất < 90%) |

Đối chiếu M3 với 300 lần lặp, seed đánh giá (`m3_dich_vu_thuc_nghiem.csv`): cùng Lịch 45, phục vụ thực nghiệm cho SL 0.9423, Gamma cho 0.9443 (Gamma lạc quan hơn 0.0020). Nếu tối ưu với phục vụ Gamma, lịch tìm được là Lịch 44 của V3; Lịch 44 đánh giá bằng phục vụ thực nghiệm có giờ tệ nhất cận dưới 0.9044 (sát ngưỡng).

---

### 7.3 Đường cong đánh đổi Pareto và Hàm chi phí với truyền sai số (S11)

Hàm chi phí $C(k) = \text{Quầy-giờ} + k \cdot N \cdot p_{ab}$ với $N = 686.7$ khách/ngày, CI truyền sai số từ $p_{ab}$ và hiệu số theo cặp $\Delta C = C_{45} - C_{48}$ (`results/final_v5/chi_phi.csv`; chạy riêng 150 lần lặp, seed 70000, nên $p_{ab}$ hơi khác bảng 4.1):

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

Để kiểm tra tính tối thiểu cục bộ của Lịch 45, 117 cấu hình lân cận được **mô phỏng bằng SimPy** (60 lần lặp, cùng tiêu chí cận dưới CI95 $\ge 90\%$ như pha 1–2) và ghi tại `results/final_v5/pha3.csv`:
- **72 phép hoán đổi 1 quầy:** bớt 1 quầy ở giờ $i$, thêm vào giờ $j$ (tổng vẫn 45). Cận dưới giờ tệ nhất từ 0.7820 đến 0.8937; tất cả vi phạm.
- **45 phép giảm 2 quầy** (tổng còn 43): 36 cặp giờ khác nhau và 9 trường hợp giảm 2 quầy cùng giờ. Cận dưới giờ tệ nhất từ 0.5749 đến 0.8848; tất cả vi phạm.
- **Kết luận:** **0/117 cấu hình** lân cận khả thi. Cùng với 9 phép bớt 1 quầy ở pha 2 (mục 3.2), Lịch 45 là **tối thiểu cục bộ** theo tiêu chí mô phỏng. V3 kiểm tra pha 3 bằng công thức Erlang-A; V4 dùng mô phỏng nên kết luận nhất quán với tiêu chí chọn lịch. Đây chưa phải chứng minh tối ưu trên toàn bộ không gian lịch.

---

### 7.5 Kịch bản kiên nhẫn của khách quầy giao dịch (M1)

Dữ liệu là tổng đài, khách quầy giao dịch có thể kiên nhẫn hơn. Chạy lại thuật toán tối ưu với kiên nhẫn trung bình từ 9.2 phút (ước lượng) đến vô cùng (`results/final_v5/do_nhay_kien_nhan.csv`, đánh giá 300 lần lặp):

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

Thêm ràng buộc $p_{ab} \le$ ngưỡng vào thuật toán tối ưu (`results/final_v5/toi_uu_rang_buoc_bo_ve.csv`, 300 lần lặp):

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

### 7.9 Tối ưu trực tiếp theo giờ công ca (M6)

Câu hỏi quản lý là *ít giờ công nhân viên nhất* mà vẫn đạt SLA, không phải ít quầy-giờ mở nhất. `h_staffing.optimize_shift_staffing` liệt kê mọi cách xếp ca mô hình B (ca 8h nghỉ trưa 1 giờ trong 11h–14h, ca 4h) có độ phủ mỗi giờ $\ge$ SIPP Erlang-A `[4, 5, 6, 5, 5, 5, 5, 5, 4]`, theo giờ công tăng dần từ 44 đến 48 (giờ công phủ Lịch 45). Độ phủ được mô phỏng như một lịch quầy (quầy dư vẫn mở), 60 lần lặp, seed chọn lịch `1000`, cùng tiêu chí cận dưới CI95 mọi giờ $\ge 90\%$ (`results/final_v5/toi_uu_theo_ca.csv`):

| Giờ công | Số lịch phủ đã thử | Số lịch khả thi | Cận dưới giờ tệ nhất cao nhất |
|:---:|:---:|:---:|:---:|
| 44 | 1 | 0 | 0.8893 |
| 48 | 94 | 33 | 0.9273 |

- Giờ công là bội của 4 (ca 4h và 8h), nên sau 44 là 48. Ở 44 giờ công chỉ có một độ phủ, đúng bằng SIPP Erlang-A (4 ca 8h + 3 ca 4h); giờ 16h–17h có cận dưới 0.8893 nên không khả thi.
- Lần thăm dò rộng hơn (cho phép thiếu 1 quầy so với SIPP ở mỗi giờ: 3.180 độ phủ, 36–48 giờ công) cũng không có lịch khả thi nào dưới 48 giờ công. Pipeline vì vậy chỉ chạy không gian không thiếu quầy (95 lịch).

Năm lịch khả thi có cận dưới giờ tệ nhất cao nhất được xác nhận bằng seed đánh giá `50000` (300 lần lặp), kèm $P(SL_{\text{ngày}} \ge 90\%)$ khi có biến động ngày ($CV$ 14.0%, 300 lần lặp) và giờ tệ nhất khi nhu cầu +10% (150 lần lặp) (`results/final_v5/toi_uu_theo_ca_top.csv`):

| # | Lịch phủ | Phương án ca | $SL$ ngày (CI95) | Giờ tệ nhất Low CI95 | $p_{ab}$ | $W_q$ (phút) | $P(SL_{\text{ngày}} \ge 90\%)$ | Nhu cầu +10%: giờ tệ nhất Low CI95 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | `[4, 6, 6, 6, 5, 5, 6, 5, 5]` | 4 ca 8h + 4 ca 4h | 0.9579 ± 0.0017 | 0.9327 (15h-16h) | 3.70% | 0.3432 | 94.7% | 0.9146 |
| 2 | `[4, 6, 7, 6, 5, 5, 5, 5, 5]` | 4 ca 8h + 4 ca 4h | 0.9570 ± 0.0018 | 0.9276 (14h-15h) | 3.77% | 0.3512 | 93.3% | 0.8959 |
| 3 | `[4, 6, 6, 5, 6, 5, 6, 5, 5]` | 4 ca 8h + 4 ca 4h | 0.9559 ± 0.0018 | 0.9246 (11h-12h) | 3.85% | 0.3570 | 91.0% | 0.8894 |
| 4 | `[4, 6, 7, 5, 6, 5, 5, 5, 5]` | 4 ca 8h + 4 ca 4h | 0.9550 ± 0.0019 | 0.9249 (11h-12h) | 3.92% | 0.3649 | 90.3% | 0.8909 |
| 5 | `[4, 6, 6, 5, 5, 5, 6, 6, 5]` | 4 ca 8h + 4 ca 4h | 0.9570 ± 0.0018 | 0.9236 (11h-12h) | 3.76% | 0.3512 | 93.7% | 0.8882 |

**Kết luận M6:** tối thiểu **48 giờ công/ngày với 4 ca 8h + 4 ca 4h**. Lịch tốt nhất ở mức này chính là Lịch 48 (V4 chọn thủ công theo dự phòng nhu cầu +10%); nó đứng đầu ở cả 6 chỉ số trong bảng. Đây là tìm kiếm đầy đủ trong không gian ca mô hình B với độ phủ $\ge$ SIPP Erlang-A, không phải chứng minh tối ưu với mọi kiểu ca.

**Biến thể nghỉ trưa linh hoạt 9h–16h** (ca 8h nghỉ 1 giờ bất kỳ trong 9h–16h; cùng thuật toán và seed; `results/final_v5/toi_uu_theo_ca_linh_hoat.csv`, `toi_uu_theo_ca_linh_hoat_top.csv`):

| Giờ công | Số lịch phủ đã thử | Số lịch khả thi | Cận dưới giờ tệ nhất cao nhất |
|:---:|:---:|:---:|:---:|
| 44 | 1 | 0 | 0.8893 |
| 48 | 231 | 99 | 0.9310 |

| # | Lịch phủ | Phương án ca | $SL$ ngày (CI95) | Giờ tệ nhất Low CI95 | $p_{ab}$ | $W_q$ (phút) | $P(SL_{\text{ngày}} \ge 90\%)$ | Nhu cầu +10%: giờ tệ nhất Low CI95 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | `[4, 6, 6, 6, 5, 5, 5, 6, 5]` | 4 ca 8h + 4 ca 4h | 0.9579 ± 0.0017 | 0.9286 (14h-15h) | 3.69% | 0.3446 | 95.0% | 0.8976 |
| 2 | `[4, 6, 6, 6, 5, 5, 6, 5, 5]` (Lịch 48) | 4 ca 8h + 4 ca 4h | 0.9579 ± 0.0017 | 0.9327 (15h-16h) | 3.70% | 0.3432 | 94.7% | 0.9146 |
| 3 | `[4, 6, 6, 6, 5, 5, 5, 5, 6]` | 4 ca 8h + 4 ca 4h | 0.9552 ± 0.0018 | 0.9276 (14h-15h) | 3.91% | 0.3644 | 93.0% | 0.8959 |
| 4 | `[4, 6, 7, 6, 5, 5, 5, 5, 5]` | 4 ca 8h + 4 ca 4h | 0.9570 ± 0.0018 | 0.9276 (14h-15h) | 3.77% | 0.3512 | 93.3% | 0.8959 |
| 5 | `[4, 6, 6, 6, 5, 6, 5, 5, 5]` | 4 ca 8h + 4 ca 4h | 0.9566 ± 0.0018 | 0.9289 (14h-15h) | 3.81% | 0.3529 | 93.7% | 0.8973 |

Nghỉ trưa linh hoạt mở rộng không gian xếp ca (231 độ phủ ở 48 giờ công so với 94) nhưng **không giảm được giờ công**: 44 giờ công vẫn chỉ có lịch SIPP Erlang-A và vẫn không khả thi. Ở 48 giờ công, Lịch 48 vẫn có giờ tệ nhất và độ bền khi nhu cầu +10% tốt nhất trong top-5.

---

### 7.10 Chọn lịch theo xác suất đạt SLA ngày khi có biến động ngày (M7)

Lịch ở các mục trên được chọn trong kịch bản danh định, độ bền chỉ kiểm tra sau. M7 đưa biến động ngày vào tiêu chí chọn: lịch khả thi khi (a) đạt tiêu chí danh định theo giờ và (b) cận dưới Wilson của $P(SL_{\text{ngày}} \ge 90\%)$, ước lượng bằng 300 lần lặp có hệ số nhân ngày ($CV$ 14.0%, seed chọn `3000`), không nhỏ hơn mức $P$ tối thiểu. Tìm trong hai không gian: quầy-giờ (tham lam hai pha như thuật toán chính) và theo ca (khung M6). Lịch tìm được đánh giá lại bằng seed `50000` và 14 ngày thực tế (`results/final_v5/toi_uu_xac_suat_ngay.csv`):

| Mức $P$ tối thiểu | Không gian tìm kiếm | Lịch nhỏ nhất | Quầy-giờ mở | Giờ công ca | $P(SL_{\text{ngày}} \ge 90\%)$ seed đánh giá (Wilson 95%) | Ngày thực tế đạt (/14) |
|:---:|---|:---:|:---:|:---:|:---:|:---:|
| 80% | quầy-giờ | `[4, 5, 6, 5, 5, 5, 5, 5, 5]` | 45 | 48 | 85.7% [81.2%, 89.2%] | 12 |
| 80% | theo ca | `[4, 5, 6, 6, 5, 5, 6, 6, 5]` | 48 | 48 | 95.0% [91.9%, 96.9%] | 14 |
| 90% | quầy-giờ | `[4, 6, 6, 6, 5, 5, 5, 6, 5]` | 48 | 52 | 95.3% [92.3%, 97.2%] | 14 |
| 90% | theo ca | `[4, 5, 6, 6, 5, 5, 6, 6, 5]` | 48 | 48 | 95.0% [91.9%, 96.9%] | 14 |
| 95% | quầy-giờ | `[5, 6, 6, 6, 6, 5, 5, 6, 5]` | 50 | 52 | 98.0% [95.7%, 99.1%] | 14 |
| 95% | theo ca | `[4, 6, 7, 7, 5, 6, 6, 6, 5]` | 52 | 52 | 99.3% [97.6%, 99.8%] | 14 |

- **Đạt SLA ở $\ge 90\%$ số ngày cần 48 giờ công.** Lịch M7 `[4, 5, 6, 6, 5, 5, 6, 6, 5]` (95.0%) và Lịch 48 (94.7%, mục 7.9) không khác biệt có ý nghĩa; Lịch 48 có giờ tệ nhất danh định tốt hơn rõ (cận dưới 0.9273 so với 0.9064 ở seed chọn lịch, `toi_uu_theo_ca.csv`) nên vẫn là khuyến nghị.
- **Đạt SLA ở $\ge 95\%$ số ngày cần 52 giờ công** (thêm 1 ca 4h).
- Trong không gian quầy-giờ, lịch tìm được thường không phủ đúng bằng ca: ở mức 90% lịch 48 quầy-giờ cần 52 giờ công. Chọn lịch theo quầy-giờ rồi mới xếp ca dễ tốn thêm giờ công; cần tìm thẳng trong không gian ca.
- Mức 80% trong không gian theo ca bắt đầu tìm từ 48 giờ công vì 44 giờ công không đạt tiêu chí danh định (mục 7.9).

---

### 7.11 Mở thêm quầy trong ngày theo hàng chờ (M8)

Dự báo sớm lúc 10h bỏ lỡ cả hai ngày hụt SLA (mục 4.4). M8 thử một quy tắc phản ứng trong ngày: `c_sim.simulate(..., surge_policy=...)` kiểm tra hàng chờ mỗi phút; nếu số khách đang chờ vượt ngưỡng liên tục trong cửa sổ cho trước thì mở thêm 1 quầy dự phòng (giữ ít nhất 30 phút, đóng khi hàng chờ về 0). Quầy-giờ mở TB = quầy-giờ lịch + phút quầy dự phòng / 60. Seed riêng `400000`–`1.300.000`; 300 lần lặp mỗi kịch bản, 40 lần lặp mỗi ngày thực tế (`results/final_v5/chinh_sach_tang_quay.csv`):

| Chính sách | Quầy-giờ mở TB (danh định) | $SL$ ngày | Giờ tệ nhất Low CI95 | $p_{ab}$ | $P(SL_{\text{ngày}} \ge 90\%)$, $CV_{\text{ngày}}$ 14% | Nhu cầu +10%: giờ tệ nhất Low CI95 | $E[S]$ +10%: giờ tệ nhất Low CI95 | Ngày 10 ($E[S]$ ×1.29 ở 14h–17h): giờ tệ nhất Low CI95 | Ngày thực tế đạt (/14) | Quầy-giờ mở TB 14 ngày |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Lịch 45 cố định | 45.00 | 0.9429 | 0.9110 | 4.89% | 80.3% | 0.8850 | 0.8802 | 0.8161 | 12 | 45.00 |
| Lịch 48 cố định | 48.00 | 0.9592 | 0.9386 | 3.59% | 94.0% | 0.9029 | 0.9013 | 0.8193 | 14 | 48.00 |
| Lịch 45 + mở thêm khi > 1 người chờ liên tục 5 phút, tối đa +1 | 46.90 | 0.9597 | 0.9409 | 3.74% | 97.3% | 0.9265 | 0.9218 | 0.8874 | 14 | 47.18 |
| **Lịch 45 + mở thêm khi > 2 người chờ liên tục 5 phút, tối đa +1** | 46.17 | 0.9549 | 0.9337 | 4.10% | 97.3% | 0.9193 | 0.9128 | 0.8748 | 14 | 46.43 |
| Lịch 45 + mở thêm khi > 3 người chờ liên tục 5 phút, tối đa +1 | 45.69 | 0.9508 | 0.9268 | 4.38% | 93.0% | 0.9102 | 0.9032 | 0.8615 | 14 | 45.94 |
| Lịch 45 + mở thêm khi > 3 người chờ liên tục 5 phút, tối đa +2 | 45.82 | 0.9518 | 0.9297 | 4.32% | 96.0% | 0.9150 | 0.9068 | 0.8714 | 14 | 46.19 |
| Lịch 45 + mở thêm khi > 2 người chờ liên tục 3 phút, tối đa +1 | 47.01 | 0.9608 | 0.9422 | 3.65% | 97.3% | 0.9303 | 0.9246 | 0.8894 | 14 | 47.25 |

- **Quy tắc chọn** (`f_scenarios.recommended_surge`): ít người dự phòng nhất, rồi trong số đó $P(SL_{\text{ngày}} \ge 90\%)$ không thấp hơn Lịch 48 cố định và đạt 14/14 ngày, chọn quầy-giờ mở TB 14 ngày nhỏ nhất. Kết quả: **mở thêm 1 quầy khi có hơn 2 người chờ liên tục 5 phút**.
- So với Lịch 48 cố định, chính sách này mở ít hơn 1.57 quầy-giờ mỗi ngày (46.43 so với 48.00 trên 14 ngày), đạt SLA ở nhiều ngày hơn khi có biến động ngày (97.3% so với 94.0%) và bền hơn khi nhu cầu hoặc thời gian phục vụ tăng 10%.
- **Điều kiện:** cần 1 nhân viên dự phòng sẵn sàng mở quầy cả ngày. Chi phí người này không nằm trong quầy-giờ mở; nếu tính theo giờ công, chính sách tốn 48 giờ công cho Lịch 45 cộng thời gian của người dự phòng.
- Ngưỡng 4–10 người trong cửa sổ 10 phút (kế hoạch ban đầu) gần như không kích hoạt vì khách bỏ về làm hàng chờ ngắn lại; lưới cuối cùng là ngưỡng 1–3 người, cửa sổ 3–5 phút.
- **Kịch bản ngày 10** (thời gian phục vụ ×1.29 chỉ ở 14h–17h, `Model.service_by_hour`): không chính sách nào giữ được giờ tệ nhất $\ge 90\%$. Lịch 48 cố định chỉ còn 0.8193, chính sách khuyến nghị 0.8748, tốt nhất là 0.8894 (ngưỡng 1 người, tối đa +1). Mở thêm quầy giảm thiệt hại rõ rệt (SL ngày 0.9356 so với 0.9353 của Lịch 48, với ít quầy-giờ hơn: 46.65 so với 48), nhưng một ngày phục vụ chậm như ngày 10 cần thêm hơn 1 quầy dự phòng ở buổi chiều.

---

### 7.12 Kiên nhẫn Weibull có kiểm duyệt (S12)

Mô hình chính giả định kiên nhẫn ~ Exp($\theta$), nhưng đường Kaplan–Meier giảm nhanh hơn đường mũ ở vùng chờ ngắn (mục 2.5). Fit Weibull $S(t) = \exp[-(t/\lambda)^k]$ bằng MLE có kiểm duyệt phải trên train (khách bỏ về đóng góp mật độ, khách được phục vụ đóng góp hàm sống tại thời gian chờ; `results/final_v5/kien_nhan_weibull_fit.csv`):

| Mô hình | Tham số | Kiên nhẫn TB (phút) | Log-likelihood | AIC |
|---|:---:|:---:|:---:|:---:|
| Mũ | $\theta = 0.1087$ | 9.20 | -1677.2 | 3356.5 |
| **Weibull** | $k = 0.855$, $\lambda = 12.04$ | 13.05 | -1666.9 | **3337.8** |

Kiểm định tỉ số hợp lý (mũ là trường hợp $k = 1$): $LR = 20.7$, $p = 5.3e-06$, nên Weibull khớp tốt hơn rõ rệt. $k < 1$ nghĩa là tốc độ bỏ về giảm dần theo thời gian chờ: có một nhóm khách bỏ về rất sớm, nhóm còn lại kiên nhẫn hơn giả định mũ.

Tối ưu lại lịch với `Model.patience` Weibull (seed chọn lịch `1000`) và đánh giá dưới cả hai mô hình kiên nhẫn (seed `50000`, 300 lần lặp; `results/final_v5/kien_nhan_weibull.csv`):

| Kiên nhẫn | Lịch | Lịch quầy | Quầy-giờ | $SL$ ngày (CI95) | Giờ tệ nhất Low CI95 | $p_{ab}$ | $W_q$ (phút) |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Mũ | Lịch 45 | `[4, 5, 6, 5, 5, 5, 5, 5, 5]` | 45 | 0.9423 ± 0.0022 | 0.9236 (11h-12h) | 4.99% | 0.4628 |
| Mũ | Lịch 48 | `[4, 6, 6, 6, 5, 5, 6, 5, 5]` | 48 | 0.9579 ± 0.0017 | 0.9327 (15h-16h) | 3.70% | 0.3432 |
| Mũ | Tối ưu với Weibull | `[4, 5, 6, 5, 5, 5, 5, 5, 5]` | 45 | 0.9423 ± 0.0022 | 0.9236 (11h-12h) | 4.99% | 0.4628 |
| Weibull | Lịch 45 | `[4, 5, 6, 5, 5, 5, 5, 5, 5]` | 45 | 0.9406 ± 0.0022 | 0.9215 (11h-12h) | 5.00% | 0.4668 |
| Weibull | Lịch 48 | `[4, 6, 6, 6, 5, 5, 6, 5, 5]` | 48 | 0.9564 ± 0.0018 | 0.9299 (15h-16h) | 3.75% | 0.3450 |
| Weibull | Tối ưu với Weibull | `[4, 5, 6, 5, 5, 5, 5, 5, 5]` | 45 | 0.9406 ± 0.0022 | 0.9215 (11h-12h) | 5.00% | 0.4668 |

**Kết luận S12:** lịch tối ưu dưới kiên nhẫn Weibull vẫn là 45 quầy-giờ `[4, 5, 6, 5, 5, 5, 5, 5, 5]`. Đổi sang Weibull chỉ làm SL của Lịch 45 giảm 0.0017 và giờ tệ nhất vẫn trên 90%. Giả định kiên nhẫn mũ không làm đổi kết luận về số quầy hay giờ công.

---

### 7.13 Tốc độ đến theo nửa giờ (S15)

λ của hai nửa mỗi khung giờ trên train, kiểm định hai nửa bằng nhau (số khách nửa đầu ~ Binomial($n$, 0.5)), hiệu chỉnh Holm–Bonferroni qua 9 giờ (`results/final_v5/lambda_nua_gio.csv`):

| Khung giờ | λ nửa đầu | λ nửa sau | Tỉ số | $p$ | $p$ Holm | Khác biệt? |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| 8h-9h | 0.8667 | 1.1133 | 1.28 | 0.0027 | 0.0244 | Có |
| 9h-10h | 1.3033 | 1.4500 | 1.11 | 0.1346 | 0.9419 | Không |
| 10h-11h | 1.5633 | 1.5067 | 0.96 | 0.5981 | 1.0000 | Không |
| 11h-12h | 1.4933 | 1.2867 | 0.86 | 0.0346 | 0.2768 | Không |
| 12h-13h | 1.2900 | 1.1900 | 0.92 | 0.2877 | 1.0000 | Không |
| 13h-14h | 1.2200 | 1.1833 | 0.97 | 0.7096 | 1.0000 | Không |
| 14h-15h | 1.3800 | 1.2967 | 0.94 | 0.3970 | 1.0000 | Không |
| 15h-16h | 1.2467 | 1.3867 | 1.11 | 0.1446 | 0.9419 | Không |
| 16h-17h | 1.0233 | 1.0900 | 1.07 | 0.4505 | 1.0000 | Không |

Chỉ 8h–9h khác biệt có ý nghĩa: khách đến thưa hơn ngay khi mở cửa. Mô phỏng với λ theo nửa giờ ở 8h–10h (`Model.sub_rates`, lịch quầy vẫn theo giờ), seed đánh giá 300 lần lặp (`results/final_v5/khung_30_phut.csv`):

| Mô hình đến | Lịch | Lịch quầy | Quầy-giờ | $SL$ ngày | Giờ tệ nhất Low CI95 | 8h–9h Low CI95 | 9h–10h Low CI95 |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Theo giờ | Lịch 45 | `[4, 5, 6, 5, 5, 5, 5, 5, 5]` | 45 | 0.9423 | 0.9236 (11h-12h) | 0.9340 | 0.9298 |
| Theo giờ | Lịch 48 | `[4, 6, 6, 6, 5, 5, 6, 5, 5]` | 48 | 0.9579 | 0.9327 (15h-16h) | 0.9345 | 0.9725 |
| Theo giờ | Tối ưu với λ nửa giờ | `[4, 5, 6, 6, 5, 5, 5, 5, 4]` | 45 | 0.9425 | 0.9044 (16h-17h) | 0.9340 | 0.9298 |
| Nửa giờ 8h–10h | Lịch 45 | `[4, 5, 6, 5, 5, 5, 5, 5, 5]` | 45 | 0.9419 | 0.9178 (11h-12h) | 0.9398 | 0.9241 |
| Nửa giờ 8h–10h | Lịch 48 | `[4, 6, 6, 6, 5, 5, 6, 5, 5]` | 48 | 0.9582 | 0.9308 (15h-16h) | 0.9417 | 0.9682 |
| Nửa giờ 8h–10h | Tối ưu với λ nửa giờ | `[4, 5, 6, 6, 5, 5, 5, 5, 4]` | 45 | 0.9425 | 0.9068 (16h-17h) | 0.9398 | 0.9241 |

**Kết luận S15:** λ theo nửa giờ không đổi tổng số quầy-giờ tối ưu (45); thuật toán chọn một cách phân bổ 45 khác (`[4, 5, 6, 6, 5, 5, 5, 5, 4]`) nằm sát ranh giới khả thi ở seed đánh giá. Lịch 45 và Lịch 48 vẫn đạt mọi giờ. Giờ 8h–9h được lợi (nửa đầu thưa khách), 9h–10h giảm nhẹ. Khung giờ 60 phút đủ cho bài toán này.

---

## 8. ĐỐI CHIẾU V4 → V5

Tại `results/final_v5/doi_chieu_v4_v5.csv` (cột V4 đọc trực tiếp từ `results/final_v4/` bằng cùng hàm `g_report.metrics`). Bảng V3 → V4 giữ ở `results/final_v4/doi_chieu_v3_v4.csv`.

**Chỉ số V4 không đổi.** P1 (chạy song song) và P2 (`rep_stats` bằng NumPy) cho mọi CSV và hình của V4 giống từng byte; M6–M8 chỉ thêm tệp mới. 17 chỉ số chính trong bảng đối chiếu (lịch tối ưu, SIPP, SL, giờ tệ nhất, bỏ về, $W_q$, $\rho$, lịch bền vững, biến động ngày, 14 ngày, xả hàng, Gamma) có chênh lệch bằng 0.

**Chỉ số thay đổi hoặc mới ở V5:**

| Chỉ số | V4 | V5 | Nguyên nhân |
|---|:---:|:---:|---|
| Giờ công tối thiểu/ngày (nghỉ trưa 11h–14h) | 48 | 48 | V4: xếp ca phủ Lịch 45 sau khi tối ưu quầy-giờ; V5: tối ưu thẳng theo giờ công (M6) và chứng minh không có lịch dưới 48 |
| Lịch phủ theo ca | `[5, 5, 6, 5, 5, 5, 6, 6, 5]` | `[4, 6, 6, 6, 5, 5, 6, 5, 5]` | M6: cùng 48 giờ công, Lịch 48 tốt hơn ở mọi chỉ số |
| Phương án ca | 5 ca 8h + 2 ca 4h | 4 ca 8h + 4 ca 4h | M6 |
| Khuyến nghị chính | Lịch 45 (45 quầy-giờ) | Lịch 48 (48 giờ công) | Đổi thước đo chi phí từ quầy-giờ mở sang giờ công |
| Giờ công để đạt SLA ở $\ge 90\%$ / $\ge 95\%$ số ngày | - | 48 / 52 | M7 |
| Lịch 45 + mở thêm 1 quầy khi > 2 người chờ 5 phút: quầy-giờ mở TB 14 ngày | - | 46.43 (Lịch 48: 48.00) | M8 |
| như trên: $P(SL_{\text{ngày}} \ge 90\%)$ có biến động ngày | - | 97.3% (Lịch 48: 94.0%) | M8 |
| như trên: giờ tệ nhất Low CI95 khi nhu cầu +10% | - | 0.9193 (Lịch 48: 0.9029) | M8 |
| Giờ công tối thiểu, nghỉ trưa linh hoạt 9h–16h | - | 48 | M6 biến thể: nghỉ trưa linh hoạt không giảm giờ công |
| Ngày 10 (phục vụ ×1.29 ở 14h–17h): giờ tệ nhất Low CI95 | - | Lịch 48: 0.8193; Lịch 45 + mở thêm quầy: 0.8748 | M8: không chính sách nào đạt; mở thêm quầy giảm thiệt hại |
| Dự báo sớm: phương trình / RMSE | $189.6 + 3.49N$ / 45.3 (trong mẫu, 14 ngày) | $90.9 + 4.20N$ / 63.9 (4 ngày test) | S13: fit trên train; vẫn bỏ lỡ 2/2 ngày hụt |
| $P(\text{thực tế mọi giờ})$ Lịch 45: khoảng 95% | [27.8%, 30.1%] (Wilson) | [25.4%, 32.3%] (cluster bootstrap) | S14 |
| Kiên nhẫn: mô hình / AIC | Mũ, 3356.5 | Weibull $k = 0.855$, 3337.8 | S12: lịch tối ưu không đổi (45) |
| Lịch tối ưu khi λ 8h–10h theo nửa giờ | - | 45 quầy-giờ | S15: tổng không đổi |
| Thời gian chạy pipeline | 33.3 phút | 15.1 phút | P1, P2 (đã gồm M6–M8, S12, S15) |

---

## 9. TỔNG KẾT KIỂM THỬ VÀ TRẠNG THÁI BÀN GIAO

1. **Kiểm thử tự động:** **84 ca kiểm thử** trong `tests/` chạy thành công trong 557 giây (9.3 phút, gồm smoke test toàn pipeline) (log tại `results/final_v5/pytest_log.txt`). V5 thêm test cho chạy song song giống tuần tự (P1), checker số trong báo cáo/slide/README (T2), M6 (cả nghỉ trưa linh hoạt), chính sách tăng quầy (M8), bảng đối chiếu V4 → V5 (R4), các trường mở rộng của `Model` (giá trị tương đương mặc định cho kết quả giống hệt) và S12–S15. Smoke test toàn pipeline (`--reps-scale 0.02`) đánh dấu `slow`.
2. **Pipeline:** `python main.py --stage all` chạy 6 giai đoạn trong 15.1 phút (`thoi_gian_chay.json`; V4: 33.3 phút). Mục tiêu 10 phút của P1 đạt được với phạm vi V4 cộng M6–M8 (9.9 phút); thêm S12, S15 và biến thể M6 nâng lên 15.1 phút. Các lần lặp chạy song song (`c_sim.map_sim`), số tiến trình đặt bằng biến môi trường `QS_WORKERS` (mặc định `min(CPU − 1, 8)`; `QS_WORKERS=1` chạy tuần tự, cho kết quả giống hệt). `results/final_v5/MO_TA.md` sinh tự động, liệt kê nguồn của từng tệp.
3. **Kiểm tra nhất quán:** `tools/check_consistency.py` quét thuật ngữ không có căn cứ, đối chiếu số trong các bảng chính của tài liệu này (1, 2.1, 2.2, 2.4, 2.5, 3.1, 4.1, 4.2, 4.4, 4.5, 5, 7.1–7.6, 7.9–7.13) với `data/clean/data_clean.csv` và CSV trong `results/final_v5/`, và đối chiếu số trong báo cáo, slide, README (T2). CI (`.github/workflows/ci.yml`) chạy test không `slow` và checker mỗi lần push.

---

## 10. HẠN CHẾ CẦN NÊU KHI BÁO CÁO

1. **Dữ liệu tổng đài, không phải quầy giao dịch:** kiên nhẫn của khách quầy có thể khác. Số quầy cần thiết tăng từ 45 lên 46–48 q-h khi kiên nhẫn dài hơn (mục 7.5).
2. **Phân phối phục vụ:** cả 4 phân phối tham số đều bị KS bác bỏ; mô hình chính dùng phân phối thực nghiệm của train (M3), nên không ngoại suy được đuôi dài hơn dữ liệu đã thấy. Lognormal với cv + 20% làm giờ tệ nhất rơi dưới 90% (mục 7.2).
3. **Kiên nhẫn:** Weibull khớp tốt hơn mũ rõ rệt nhưng không đổi lịch tối ưu (mục 7.12); mô hình chính giữ kiên nhẫn mũ để so sánh được với Erlang-A.
4. **Tỉ lệ bỏ về sát 5%:** Lịch 45 đạt SL một phần nhờ khách bỏ về; giới hạn bỏ về 3% cần 51 q-h (mục 7.6).
5. **Ca làm việc:** kết luận 48 giờ công đúng với ca 8h (nghỉ trưa trong 11h–14h hoặc 9h–16h) và ca 4h. Kiểu ca khác (ca 6h, ca chia đôi) chưa xét (mục 6, 7.9).
6. **Dự báo sớm lúc 10h** (fit trên train) có sai số ngoài mẫu 63.9 khách và bỏ lỡ cả hai ngày hụt SLA (mục 4.4); không nên dùng làm quy tắc vận hành.
7. **Lựa chọn Lịch 45 phụ thuộc chi phí mất khách $k$:** với $k > 0.58$, Mốc 6 quầy rẻ hơn (mục 7.3).
8. **Ngoài mẫu 15h–16h:** do một ngày (ngày 10) có nhu cầu cao gặp nhân sự hiệu dụng thấp; dữ liệu chỉ có hoạt động PS nên số phiên chồng lấn là cận dưới của số nhân viên (mục 5).
9. **Chính sách tăng quầy (M8) cần 1 người dự phòng:** chi phí người này không tính trong quầy-giờ mở; quy tắc chỉ có lợi khi người dự phòng làm việc khác lúc không mở quầy (mục 7.11).
10. **Ngày phục vụ chậm như ngày 10:** không chính sách nào (kể cả Lịch 48 và mở thêm 1 quầy) giữ được giờ tệ nhất $\ge 90\%$; cần thêm hơn 1 quầy dự phòng ở buổi chiều (mục 7.11).
11. **Khung giờ 60 phút:** chỉ 8h–9h có λ khác rõ giữa hai nửa giờ và không làm đổi tổng số quầy-giờ (mục 7.13); các khung ngắn hơn 30 phút chưa xét.
