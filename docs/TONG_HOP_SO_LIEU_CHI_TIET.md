# BẢNG TỔNG HỢP TOÀN BỘ TIẾN TRÌNH, SỐ LIỆU TÍNH TOÁN EXCEL VÀ KIỂM CHỨNG CODE PYTHON / SIMPY

**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu cho chi nhánh ngân hàng  
**Thời điểm tổng hợp:** Tháng 10/2026 (Phiên bản đồng bộ hoàn chỉnh Tuần 1, Tuần 2, Tuần 3)  
**Nhóm sinh viên thực hiện:**  
- **Thành viên A:** Xử lý dữ liệu thực tế, Ước lượng tham số, Kiểm định phân phối, Độ bất định tham số & Ngoài mẫu  
- **Thành viên B:** Cơ sở giải tích (Erlang C, Erlang-A, SIPP), Xây dựng Workbook Excel, Bài toán Ca làm việc (MILP) & Phân tích Chi phí  
- **Thành viên C:** Xây dựng mô hình SimPy, Kiểm chứng 3 tầng, Thuật toán Tối ưu hóa 2 pha, Phân tích Độ nhạy & Đóng băng số liệu  

---

## MỤC LỤC TỔNG HỢP

1. [PHẦN 1: TỔNG QUAN TIẾN TRÌNH VÀ NHỮNG VIỆC ĐÃ LÀM ĐƯỢC](#phần-1-tổng-quan-tiến-trình-và-những-việc-đã-làm-được)
2. [PHẦN 2: TỔNG HỢP TOÀN BỘ SỐ LIỆU TÍNH TOÁN TRONG TẤT CẢ CÁC FILE EXCEL](#phần-2-tổng-hợp-toàn-bộ-số-liệu-tính-toán-trong-tất-cả-các-file-excel)
   - [2.1 File `docs/thong_ke_mo_ta.xlsx`](#21-file-docsthong_ke_mo_taxlsx)
   - [2.2 File `docs/bang_tham_so.xlsx`](#22-file-docsbang_tham_soxlsx)
   - [2.3 File `excel/erlang.xlsx`](#23-file-excelerlangxlsx)
3. [PHẦN 3: TỔNG HỢP TOÀN BỘ SỐ LIỆU KIỂM CHỨNG VÀ THỰC NGHIỆM BẰNG CODE (PYTHON / SIMPY)](#phần-3-tổng-hợp-toàn-bộ-số-liệu-kiểm-chứng-và-thực-nghiệm-bằng-code-python--simpy)
   - [3.1 Bảng Kiểm chứng Ba tầng và Hai Kiểm tra Độc lập (`kiem_chung.csv`)](#31-bảng-kiểm-chứng-ba-tầng-và-hai-kiểm-tra-độc-lập-kiem_chungcsv)
   - [3.2 Lịch sử Thuật toán Tối ưu hóa 2 Pha SimPy (`lich_toi_uu.csv`)](#32-lịch-sử-thuật-toán-tối-ưu-hóa-2-pha-simpy-lich_toi_uucsv)
   - [3.3 Bảng Đánh giá và So sánh 5 Chính sách Phục vụ (`so_sanh_chinh_sach.csv`)](#33-bảng-đánh-giá-và-so-sánh-5-chính-sách-phục-vụ-so_sanh_chinh_sachcsv)
   - [3.4 Phân tích Độ nhạy Toàn diện Hệ thống T6 (`do_nhay.csv`)](#34-phân-tích-độ-nhạy-toàn-diện-hệ-thống-t6-do_nhaycsv)
   - [3.5 Hàm Chi phí Kinh tế và Phân tích Kịch bản Đánh đổi (`chi_phi.csv`)](#35-hàm-chi-phí-kinh-tế-và-phân-tích-kịch-bản-đánh-đổi-chi_phicsv)
   - [3.6 Kết quả Bài toán Lập lịch Ca làm việc MILP (`lich_theo_ca.csv`)](#36-kết-quả-bài-toán-lập-lịch-ca-làm-việc-milp-lich_theo_cacsv)
   - [3.7 Phân tích Độ bất định Tham số qua 50 Bộ Bootstrap (`bat_dinh_tham_so.csv`)](#37-phân-tích-độ-bất-định-tham-số-qua-50-bộ-bootstrap-bat_dinh_tham_socsv)
   - [3.8 Độ nhạy theo Phân phối Thời gian Phục vụ (`do_nhay_phan_phoi.csv`)](#38-độ-nhạy-theo-phân-phối-thời-gian-phục-vụ-do_nhay_phan_phoicsv)
   - [3.9 Đánh giá Ngoài mẫu trên Tập Test 4 Ngày (`ngoai_mau.csv`)](#39-đánh-giá-ngoài-mẫu-trên-tập-test-4-ngày-ngoai_maucsv)
   - [3.10 Kết quả Kiểm thử Tự động pytest 12/12 Passed](#310-kết-quả-kiểm-thử-tự-động-pytest-1212-passed)
4. [PHẦN 4: ĐỐI CHIẾU CHÉO GIỮA EXCEL, LÝ THUYẾT VÀ MÔ PHỎNG SIMPY](#phần-4-đối-chiếu-chéo-giữa-excel-lý-thuyết-và-mô-phỏng-simpy)
5. [PHẦN 5: BẢNG TỔNG HỢP QUYẾT ĐỊNH KHUYẾN NGHỊ CUỐI CÙNG](#phần-5-bảng-tổng-hợp-quyết-định-khuyến-nghị-cuối-cùng)

---

## PHẦN 1: TỔNG QUAN TIẾN TRÌNH VÀ NHỮNG VIỆC ĐÃ LÀM ĐƯỢC

### 1.1 Khái quát Tiến trình 3 Tuần
Dự án đã hoàn thành trọn vẹn lộ trình 3 tuần từ nghiên cứu thăm dò dữ liệu đến mô hình hóa lý thuyết, lập trình mô phỏng, kiểm chứng đa tầng, tối ưu hóa định biên và đóng gói sản phẩm khoa học:

| Tuần | Trọng tâm công việc | Các mốc kết quả đã đạt được | Tình trạng |
|---|---|---|:---:|
| **Tuần 1** | Khảo sát dữ liệu thực tế, làm sạch dữ liệu và ước lượng sơ bộ | - Thu thập bộ dữ liệu giao dịch 14 ngày chuẩn ($9.836$ cuộc gọi) từ Technion SEE Center.<br>- Làm sạch qua `data/lam_sach.py`, lọc khung giờ 8h-17h, nghiệp vụ PS.<br>- Ước lượng sơ bộ $\lambda_h$, $E[S] = 2.88$ phút, $cv = 1.10$, $\theta = 0.1123$.<br>- Tạo 2 file Excel ban đầu: `docs/thong_ke_mo_ta.xlsx` và `docs/bang_tham_so.xlsx`. | **Hoàn thành 100%** |
| **Tuần 2** | Mô hình hóa giải tích, xây dựng SimPy và kiểm chứng ba tầng | - Xây dựng mô hình giải tích `b_theory.py` (M/M/c, Allen-Cunneen, Erlang-A ma trận hấp thụ Markov, SIPP).<br>- Tạo file Excel tính toán tự động `excel/erlang.xlsx` (5 sheets, không lỗi `#NAME?`).<br>- Xây dựng công cụ mô phỏng SimPy `c_sim.py` (Blocker động, Priority VIP, Khách bỏ về, CRN).<br>- Kiểm chứng ba tầng (Tầng 1 M/M/c, Tầng 2 Erlang-A, Tầng 3 Allen-Cunneen).<br>- Khảo sát khởi động Welch (`fig_c_welch.png`) và lợi ích gộp hàng (`fig_c_pooling.png`). | **Hoàn thành 100%** |
| **Tuần 3** | Sửa tồn đọng, tối ưu hóa lịch quầy, thí nghiệm mở rộng, đóng băng số liệu, viết báo cáo & slide | - Sửa triệt để lỗi hiệu suất $\rho$ (đạt $0.7517 \pm 0.0047$ khớp định luật Little).<br>- Bổ sung Kiểm tra A (M/G/1 Pollaczek-Khinchine exact $14.625$p) và Kiểm tra B (M/G/6 60 reps).<br>- Tối ưu hóa lịch quầy 2 pha hội tụ tại lịch `[4, 5, 6, 5, 5, 5, 5, 5, 4]` (44 quầy-giờ).<br>- Đánh giá 5 chính sách với 300 lần lặp độc lập (`seed_base=50000`).<br>- Phân tích độ nhạy T6, hàm chi phí kịch bản $k$, bài toán ca làm việc MILP, độ bất định 50 bộ bootstrap, kiểm tra ngoài mẫu trên 4 ngày test.<br>- Đóng băng số liệu tại `results/final_v1/` gồm 10 bảng CSV/MD và 8 biểu đồ đồ họa.<br>- Hoàn tất báo cáo tổng kết (`docs/bao_cao_tong_ket.md`) và slide thuyết trình (`docs/slide_thuyet_trinh.md`). | **Hoàn thành 100%** |

### 1.2 Phân công Trách nhiệm và Sản phẩm Bàn giao Cụ thể
- **Thành viên A (Nguyễn Văn A - Dữ liệu & Thống kê):**
  - Quản lý tệp dữ liệu sạch `data/clean/data_clean.csv` ($9.836$ bản ghi).
  - Ước lượng các tham số $\lambda_h$, $E[S]$, $\theta$, $p_{vip}$ trên tập Train 10 ngày ($6.867$ bản ghi) và xuất `docs/params.json` (Phiên bản v2.0).
  - Kiểm định phân phối Poisson theo giờ và so sánh AIC thời gian phục vụ (Gamma tốt nhất).
  - Thực hiện Thí nghiệm E4 (Độ bất định tham số 50 bộ bootstrap) $\implies$ [`fig_a_bat_dinh.png`](file:///d:/KHDV/results/final_v1/hinh/fig_a_bat_dinh.png).
  - Thực hiện Thí nghiệm E5 (Độ nhạy phân phối phục vụ) và E6 (Kiểm tra ngoài mẫu trên tập Test 4 ngày) $\implies$ [`fig_a_ngoai_mau.png`](file:///d:/KHDV/results/final_v1/hinh/fig_a_ngoai_mau.png).
  - Soạn thảo Mục 3, Mục 4 trong Báo cáo tổng kết và Slide 3, 4, 5.
- **Thành viên B (Trần Thị B - Lý thuyết, Chi phí & Vận hành):**
  - Xây dựng mô hình giải tích `b_theory.py` và bảng tính tự động `excel/erlang.xlsx`.
  - Phân tích bảng quyết định định biên SIPP Erlang C (47 q-h) và Erlang-A (44 q-h).
  - Xây dựng hàm chi phí kinh tế $C(k) = \text{quầy-giờ} + k \cdot N_{ab}$ với $k \in \{0.1, 0.25, 0.5, 1.0, 2.0\}$ và vẽ đường đánh đổi Pareto $\implies$ [`fig_b_chi_phi.png`](file:///d:/KHDV/results/final_v1/hinh/fig_b_chi_phi.png).
  - Thiết lập và giải bài toán Quy hoạch Tuyến tính Nguyên MILP (`scipy.optimize.milp`) lập lịch theo ca làm việc (ca 4h, ca 8h, ca hỗn hợp) $\implies$ [`fig_b_ca_lam.png`](file:///d:/KHDV/results/final_v1/hinh/fig_b_ca_lam.png).
  - Phân tích lịch bền vững theo quy tắc căn bậc hai $c \approx a + \beta \sqrt{a}$.
  - Soạn thảo Mục 5, Mục 6 trong Báo cáo tổng kết và Slide 6, 7, 8, 9.
- **Thành viên C (Lê Văn C - Mô phỏng, Tối ưu & Tổng hợp):**
  - Xây dựng động cơ mô phỏng sự kiện rời rạc SimPy `c_sim.py` với blocker động và đồng bộ hóa CRN.
  - Thực hiện kiểm chứng 3 tầng, sửa lỗi hiệu suất $\rho$, thực hiện Kiểm tra A (M/G/1 exact) và Kiểm tra B.
  - Lập trình thuật toán tối ưu hóa 2 pha (*Ramp-up* & *Pruning*).
  - Đánh giá 5 chính sách phục vụ với 300 lần lặp độc lập và phân tích độ nhạy T6 $\implies$ [`fig_c_do_nhay.png`](file:///d:/KHDV/results/final_v1/hinh/fig_c_do_nhay.png).
  - Tổng hợp, kiểm tra chéo số liệu và đóng băng toàn bộ kết quả vào `results/final_v1/`.
  - Soạn thảo Mục 7, Mục 8, Mục 9 trong Báo cáo tổng kết, Slide 10, 11, 12, 13 và kịch bản thuyết trình.

---

## PHẦN 2: TỔNG HỢP TOÀN BỘ SỐ LIỆU TÍNH TOÁN TRONG TẤT CẢ CÁC FILE EXCEL

Hiện tại trong dự án có chính xác **3 tệp Excel** phục vụ việc lưu trữ thống kê, tham số và tính toán giải tích. Toàn bộ số liệu trong từng sheet được trích xuất nguyên vẹn dưới đây.

---

### 2.1 File `docs/thong_ke_mo_ta.xlsx`

Tệp gồm 2 sheets ghi nhận kết quả xử lý mô tả trên toàn bộ 14 ngày làm việc tiêu chuẩn.

#### Sheet 1: `Thong_ke_theo_gio` (10 hàng $\times$ 13 cột)
Ghi nhận đặc trưng dòng khách và phục vụ theo từng khung giờ trong ngày:

| Khung giờ | Hour ID | Số khách TB $\bar{N}_h$ (khách/ngày) | Tốc độ đến $\lambda_h$ (khách/phút) | CI95 Low $\lambda$ | CI95 High $\lambda$ | Chỉ số phân tán $D$ | $p$-value Poisson | Kết luận Poisson ($\alpha=0.05$) | Tỉ lệ bỏ về $p_{ab}$ | Tỉ lệ khách VIP | $E[S]$ theo giờ (phút) | $\text{std}[S]$ theo giờ (phút) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h - 9h** | 0 | 61.14 | 1.0190 | **0.9180** | **1.1200** | 23.55 | 0.0356 | **Bác bỏ (nhẹ)** | 2.80% | 16.94% | 2.61 | 2.83 |
| **9h - 10h** | 1 | 86.00 | 1.4333 | **1.3137** | **1.5530** | 23.58 | 0.0352 | **Bác bỏ (nhẹ)** | 3.99% | 32.23% | 2.95 | 3.74 |
| **10h - 11h** | 2 | 98.64 | 1.6440 | **1.4593** | **1.8287** | 48.77 | 0.0000 | **Bác bỏ (mạnh)** | 10.86% | 42.65% | 2.80 | 3.08 |
| **11h - 12h** | 3 | 86.36 | 1.4393 | **1.2844** | **1.5942** | 39.15 | 0.0002 | **Bác bỏ (mạnh)** | 7.94% | 39.04% | 2.90 | 2.95 |
| **12h - 13h** | 4 | 74.36 | 1.2393 | **1.1340** | **1.3446** | 20.83 | 0.0763 | **Chưa bác bỏ** | 2.40% | 19.31% | 2.71 | 3.00 |
| **13h - 14h** | 5 | 74.57 | 1.2429 | **1.1148** | **1.3709** | 30.73 | 0.0037 | **Bác bỏ (mạnh)** | 4.12% | 28.45% | 2.81 | 3.07 |
| **14h - 15h** | 6 | 79.29 | 1.3214 | **1.1741** | **1.4687** | 38.08 | 0.0003 | **Bác bỏ (mạnh)** | 8.83% | 35.59% | 3.09 | 3.34 |
| **15h - 16h** | 7 | 78.29 | 1.3048 | **1.1688** | **1.4407** | 33.61 | 0.0014 | **Bác bỏ (mạnh)** | 13.32% | 49.82% | 3.25 | 3.24 |
| **16h - 17h** | 8 | 63.93 | 1.0655 | **0.9555** | **1.1755** | 26.61 | 0.0141 | **Bác bỏ (nhẹ)** | 8.16% | 33.07% | 2.74 | 2.82 |

> [!NOTE]
> **Quy tắc gắn nhãn kiểm định Poisson rõ ràng:**
> - $p < 0.01$: Bác bỏ (mạnh).
> - $0.01 \le p < 0.05$: Bác bỏ (nhẹ).
> - $p \ge 0.05$: Chưa bác bỏ.
> Kết quả: Có tới **8/9 khung giờ bị bác bỏ Poisson ở mức ý nghĩa 5%** (5/9 giờ bị bác bỏ mạnh ở mức 1%). Chỉ duy nhất khung giờ 12h–13h ($p = 0.0763$) là chưa bác bỏ. Giả định dòng khách đến tuân theo tiến trình Poisson thuần túy với $\lambda_h$ cố định không phản ánh đầy đủ thực tế.

#### Thống kê Quá Phân Tán Lưu Lượng Khách theo Ngày (`qua_phan_tan_ngay.csv`)
- **Số ngày quan sát:** 14 ngày làm việc tiêu chuẩn.
- **Tổng khách trung bình mỗi ngày ($\mu$):** $702.6$ khách/ngày.
- **Phương sai thực tế ($\sigma^2$):** $7.591,8 \implies$ Độ lệch chuẩn thực tế $\sigma = 87.1$ khách.
- **Độ lệch chuẩn phân phối Poisson thuần ($\sqrt{\mu}$):** $26.5$ khách.
- **Tỉ số Phương sai / Trung bình ($\text{Var}/\text{Mean}$):** $10.8 \gg 1$ (Dữ liệu bị quá phân tán mạnh so với Poisson).
- **Hệ số biến thiên thực tế ($CV_{\text{ngày}}$):** $12.4\%$.
- **Ước lượng $CV_{\text{ngày}}$ sau khi loại trừ nhiễu Poisson:**
  $$CV_{\text{ngày}}^2 = \frac{\text{Var}(N_d) - \mu}{\mu^2} = \frac{7591.8 - 702.6}{702.6^2} = 0.0139 \implies CV_{\text{ngày}} = 11.8\%.$$
- **Kiểm định quá phân tán:** $D = 140.4$ ($df=13$), $p\text{-value} = 3.65 \times 10^{-23}$ $\implies$ Bác bỏ mạnh giả định Poisson thuần cho tổng ngày.

#### Sheet 2: `Khach_theo_ngay_gio` (15 hàng $\times$ 10 cột)
Ma trận đầy đủ số lượng khách hàng đến theo từng ngày (14 ngày: Ngày 0 đến Ngày 13) và từng khung giờ (tổng cộng 126 quan sát):

| Ngày quan sát | 8h-9h | 9h-10h | 10h-11h | 11h-12h | 12h-13h | 13h-14h | 14h-15h | 15h-16h | 16h-17h | **Tổng ngày** |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Ngày 0** | 65 | 100 | 81 | 79 | 79 | 69 | 79 | 83 | 55 | **690** |
| **Ngày 1** | 74 | 89 | 119 | 110 | 80 | 86 | 77 | 73 | 68 | **776** |
| **Ngày 2** | 63 | 99 | 118 | 106 | 91 | 86 | 87 | 97 | 79 | **826** |
| **Ngày 3** | 55 | 81 | 99 | 81 | 71 | 67 | 66 | 64 | 50 | **634** |
| **Ngày 4** | 54 | 67 | 77 | 80 | 62 | 57 | 76 | 57 | 50 | **580** |
| **Ngày 5** | 44 | 74 | 75 | 68 | 58 | 72 | 69 | 87 | 53 | **600** |
| **Ngày 6** | 40 | 66 | 69 | 61 | 57 | 52 | 66 | 71 | 57 | **539** |
| **Ngày 7** | 73 | 89 | 96 | 101 | 85 | 91 | 123 | 77 | 85 | **820** |
| **Ngày 8** | 69 | 80 | 97 | 82 | 92 | 76 | 75 | 71 | 73 | **715** |
| **Ngày 9** | 57 | 81 | 90 | 66 | 69 | 65 | 85 | 110 | 64 | **687** |
| **Ngày 10** | 70 | 83 | 95 | 83 | 74 | 77 | 96 | 89 | 73 | **740** |
| **Ngày 11** | 58 | 90 | 115 | 97 | 75 | 101 | 69 | 73 | 70 | **748** |
| **Ngày 12** | 62 | 96 | 120 | 110 | 78 | 68 | 71 | 81 | 67 | **753** |
| **Ngày 13** | 72 | 109 | 130 | 85 | 70 | 77 | 71 | 63 | 51 | **728** |
| **Trung bình**| **61.14** | **86.00** | **98.64** | **86.36** | **74.36** | **74.57** | **79.29** | **78.29** | **63.93** | **702.57** |

---

### 2.2 File `docs/bang_tham_so.xlsx`

Tệp gồm 2 sheets chuẩn hóa bộ tham số đầu vào được trích xuất từ dữ liệu.

#### Sheet 1: `theo_gio` (10 hàng $\times$ 6 cột)
Tham số dòng khách đến theo 9 khung giờ:

| Khung giờ | $\bar{N}_h$ (khách/ngày) | $\lambda_h$ (khách/phút) | CI95 Low | CI95 High | $p$-value Poisson |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h - 9h** | 61.14 | 1.0190 | 0.9508 | 1.0873 | 0.0356 |
| **9h - 10h** | 86.00 | 1.4333 | 1.3524 | 1.5143 | 0.0352 |
| **10h - 11h** | 98.64 | 1.6440 | 1.5573 | 1.7308 | 0.0000 |
| **11h - 12h** | 86.36 | 1.4393 | 1.3582 | 1.5204 | 0.0002 |
| **12h - 13h** | 74.36 | 1.2393 | 1.1640 | 1.3146 | 0.0763 |
| **13h - 14h** | 74.57 | 1.2429 | 1.1675 | 1.3182 | 0.0037 |
| **14h - 15h** | 79.29 | 1.3214 | 1.2437 | 1.3992 | 0.0003 |
| **15h - 16h** | 78.29 | 1.3048 | 1.2275 | 1.3820 | 0.0014 |
| **16h - 17h** | 63.93 | 1.0655 | 0.9957 | 1.1353 | 0.0141 |

#### Sheet 2: `chung` (10 hàng $\times$ 4 cột)
Toàn bộ tham số phân phối dịch vụ và hành vi bỏ về:

| Tham số hệ thống | Giá trị ước lượng | Khoảng tin cậy 95% | Ghi chú kỹ thuật |
|---|:---:|:---:|---|
| **$E[S]$ - Thời gian phục vụ TB** | **$2.8784$ phút** | [2.8138, 2.9431] | Tính trên $9.133$ lượt khách được phục vụ thành công |
| **$\text{std}[S]$ - Độ lệch chuẩn phục vụ** | **$3.1527$ phút** | - | Phản ánh biến thiên thời gian thao tác nghiệp vụ |
| **$cv$ - Hệ số biến thiên** | **$1.0953$** | - | $cv > 1$ cho thấy biến thiên lớn hơn phân phối mũ chuẩn ($cv=1$) |
| **$cs^2$ - Bình phương $cv$** | **$1.1996$** | - | Dùng trong công thức xấp xỉ Allen–Cunneen cho M/G/c |
| **Phân phối phục vụ tốt nhất** | **Gamma (theo AIC)**| - | Cả 4 phân phối (Gamma, Weibull, Exponential, Lognormal) đều bị KS bootstrap bác bỏ; Lognormal có AIC kém nhất |
| **$\theta$ - Tốc độ bỏ về** | **$0.1123 \text{ phút}^{-1}$**| [0.1040, 0.1206] | Ước lượng hợp lý cực đại (MLE) với dữ liệu bị kiểm duyệt |
| **Kiên nhẫn TB ($1/\theta$)** | **$8.91$ phút** | [8.29, 9.62] | Thời gian khách sẵn sàng chờ đợi trước khi bỏ về |
| **Tỉ lệ khách VIP ($p_{vip}$)** | **$0.3385$** | [0.3291, 0.3478] | Khách hàng priority level 2 trong hệ thống ngân hàng |
| **Tỉ lệ bỏ về trung bình toàn ngày**| **$0.0715$ (7.15%)** | - | 703 cuộc bỏ về trên tổng số 9.836 lượt khách đến |

*(Lưu ý: Bộ tham số chốt v2.0 tại `docs/params.json` được tinh chỉnh trên tập Train 10 ngày chuẩn là: $E[S] = 2.9236$, $cv = 1.0963$, $cs^2 = 1.2018$, $\theta = 0.1087$, $p_{vip} = 0.3543$).*

---

### 2.3 File `excel/erlang.xlsx`

Tệp gồm 5 sheets tính toán mô hình hàng đợi giải tích hoàn toàn tự động bằng công thức Excel thuần túy (không macro, sử dụng hàm `POISSON.DIST` tương thích mọi phiên bản Excel).

#### Sheet 1: `Input` (6 hàng $\times$ 4 cột)
Tham số cơ sở cho ví dụ tính tay điển hình:

| Tham số | Giá trị | Đơn vị | Diễn giải |
|---|:---:|:---:|---|
| $\lambda$ (Tốc độ đến TB) | **1.50** | khách/phút | Tốc độ khách đến giờ cao điểm |
| $E[S]$ (Thời gian phục vụ TB) | **3.00** | phút | Thời gian xử lý trung bình 1 giao dịch |
| $\mu = 1/E[S]$ (Tốc độ phục vụ 1 quầy) | **0.3333** | khách/phút | Khả năng xử lý của 1 giao dịch viên |
| $a = \lambda \cdot E[S]$ (Cường độ tải) | **4.50** | Erlang | Khối lượng công việc cần xử lý |
| Ngưỡng thời gian chờ cam kết $t$ | **5.00** | phút | Ngưỡng cam kết chất lượng dịch vụ SLA |
| Mục tiêu mức phục vụ $P(W_q \le t)$ | **0.90** | $90\%$ | Tỉ lệ tối thiểu khách hàng chờ $\le 5$ phút |

#### Sheet 2: `ErlangC` (Toàn bộ 15 dòng tính toán $c = 5 \dots 19$)
Tính toán chi tiết các chỉ số M/M/c theo số lượng quầy $c$ ($a = 4.5$ Erlang, $\mu = 1/3$):

| Số quầy $c$ | Hệ số sử dụng $\rho = a/c$ | Xác suất phải chờ $C(c, a)$ | Thời gian chờ TB $W_q$ (phút) | Độ dài hàng đợi $L_q$ (khách) | Mức phục vụ $P(W_q \le 5\text{p})$ | Đạt mục tiêu SLA $\ge 90\%$? |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 5 | 0.9000 | 0.762493 | 4.5750 | 6.8624 | 0.6686 (66.9%) | **KHÔNG** |
| **6** | **0.7500** | **0.421652** | **0.8433** | **1.2650** | **0.9654 (96.5%)** | **ĐẠT (Tối thiểu)** |
| 7 | 0.6429 | 0.217221 | 0.2607 | 0.3910 | 0.9966 (99.7%) | ĐẠT |
| 8 | 0.5625 | 0.103889 | 0.0890 | 0.1336 | 0.9997 (100%) | ĐẠT |
| 9 | 0.5000 | 0.046050 | 0.0307 | 0.0460 | 1.0000 (100%) | ĐẠT |
| 10 | 0.4500 | 0.018918 | 0.0103 | 0.0155 | 1.0000 (100%) | ĐẠT |
| 11 | 0.4091 | 0.007213 | 0.0033 | 0.0050 | 1.0000 (100%) | ĐẠT |
| 12 | 0.3750 | 0.002558 | 0.0010 | 0.0015 | 1.0000 (100%) | ĐẠT |
| 13 | 0.3462 | 0.000847 | 0.0003 | 0.0004 | 1.0000 (100%) | ĐẠT |
| 14 | 0.3214 | 0.000262 | 0.00008 | 0.0001 | 1.0000 (100%) | ĐẠT |
| 15 | 0.3000 | 0.000076 | 0.00002 | 0.00003 | 1.0000 (100%) | ĐẠT |
| 16 | 0.2813 | 0.000021 | 0.000005 | 0.000008 | 1.0000 (100%) | ĐẠT |
| 17 | 0.2647 | 0.000005 | 0.000001 | 0.000002 | 1.0000 (100%) | ĐẠT |
| 18 | 0.2500 | 0.000001 | 0.0000003 | 0.0000004 | 1.0000 (100%) | ĐẠT |
| 19 | 0.2368 | 0.0000003 | 0.00000006 | 0.0000001 | 1.0000 (100%) | ĐẠT |

*Kết luận trên Excel:* Với tải $a = 4.5$ Erlang, số quầy tối thiểu đạt SLA 90% theo Erlang C là **$c = 6$ quầy** ($\rho = 75.0\%, W_q = 0.843\text{ phút}, SL = 96.54\%$).

#### Sheet 3: `Tra_c` (Bảng tra cứu 2 chiều số quầy tối thiểu)
Ma trận tra cứu số quầy tối thiểu theo tốc độ đến $\lambda \in [0.5, 3.0]$ và thời gian phục vụ $E[S] \in [2.0, 5.0]$ phút để thỏa $P(W_q \le 5\text{p}) \ge 90\%$:

| $\lambda$ (khách/phút) | $E[S] = 2.0$ phút ($\mu = 0.50$) | $E[S] = 3.0$ phút ($\mu = 0.33$) | $E[S] = 4.0$ phút ($\mu = 0.25$) | $E[S] = 5.0$ phút ($\mu = 0.20$) |
|:---:|:---:|:---:|:---:|:---:|
| **0.50** | 2 | 3 | 4 | 4 |
| **0.75** | 3 | 4 | 5 | 6 |
| **1.00** | 3 | 4 | 6 | 7 |
| **1.25** | 4 | 5 | 7 | 8 |
| **1.50** | **4** | **6** | **8** | **10** |
| **1.75** | 5 | 7 | 9 | 11 |
| **2.00** | 5 | 8 | 10 | 12 |
| **2.25** | 6 | 8 | 11 | 13 |
| **2.50** | 6 | 9 | 12 | 15 |
| **2.75** | 7 | 10 | 13 | 16 |
| **3.00** | 7 | 11 | 14 | 17 |

#### Sheet 4: `Allen_Cunneen` (Xấp xỉ M/G/c với $cs^2$ biến thiên)
Tính toán thời gian chờ $W_q(M/G/c) \approx \frac{1+cs^2}{2} W_q(M/M/c)$ với $a = 4.5$ Erlang:

| Số quầy $c$ | $W_q$ Chuẩn M/M/c ($cs^2=1.0$) | $W_q$ ($cs^2=0.5$ - Đều) | $W_q$ ($cs^2=1.2$ - Thực tế) | $W_q$ ($cs^2=1.5$ - Biến thiên cao) | Mức tăng $W_q$ do $cs^2=1.2$ |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 5 | 4.5750 phút | 3.4312 phút | 5.0325 phút | 5.7187 phút | $+10.0\%$ |
| **6** | **0.8433 phút** | **0.6325 phút** | **0.9276 phút** | **1.0541 phút** | **$+10.0\%$** |
| 7 | 0.2607 phút | 0.1955 phút | 0.2867 phút | 0.3258 phút | $+10.0\%$ |
| 8 | 0.0890 phút | 0.0668 phút | 0.0980 phút | 0.1113 phút | $+10.0\%$ |
| 9 | 0.0307 phút | 0.0230 phút | 0.0338 phút | 0.0384 phút | $+10.0\%$ |
| 10 | 0.0103 phút | 0.0077 phút | 0.0114 phút | 0.0129 phút | $+10.0\%$ |
| 11 | 0.0033 phút | 0.0025 phút | 0.0037 phút | 0.0042 phút | $+10.0\%$ |
| 12 | 0.0010 phút | 0.0008 phút | 0.0011 phút | 0.0013 phút | $+10.0\%$ |
| 13 | 0.0003 phút | 0.0002 phút | 0.0003 phút | 0.0004 phút | $+10.0\%$ |
| 14 | 0.00008 phút | 0.00006 phút | 0.00009 phút | 0.00010 phút | $+10.0\%$ |

#### Sheet 5: `Quyet_dinh` (Định biên SIPP Erlang C 9 khung giờ)
Bảng tra số quầy SIPP trên toàn bộ 9 khung giờ bằng Erlang C ($E[S] = 2.88$ phút, $cs^2 = 1.20$, $\text{SLA} \ge 90\%$):

| Khung giờ | $\lambda_h$ (khách/phút) | $E[S]$ (phút) | $cs^2$ | Tải $a_h$ (Erlang) | Số quầy $c$ (Erlang C) | Hiệu suất $\rho$ | $P(W_q \le 5\text{p})$ dự kiến | Đạt SLA? |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h - 9h** | 1.0190 | 2.88 | 1.20 | 2.935 | **4** | 73.37% | 92.45% | **ĐẠT** |
| **9h - 10h** | 1.4333 | 2.88 | 1.20 | 4.128 | **6** | 68.80% | 98.78% | **ĐẠT** |
| **10h - 11h (Đỉnh)** | 1.6440 | 2.88 | 1.20 | 4.735 | **6** | 78.91% | 94.53% | **ĐẠT** |
| **11h - 12h** | 1.4393 | 2.88 | 1.20 | 4.145 | **6** | 69.09% | 98.73% | **ĐẠT** |
| **12h - 13h** | 1.2393 | 2.88 | 1.20 | 3.569 | **5** | 71.38% | 96.68% | **ĐẠT** |
| **13h - 14h** | 1.2429 | 2.88 | 1.20 | 3.580 | **5** | 71.59% | 96.59% | **ĐẠT** |
| **14h - 15h** | 1.3214 | 2.88 | 1.20 | 3.806 | **5** | 76.11% | 93.98% | **ĐẠT** |
| **15h - 16h** | 1.3048 | 2.88 | 1.20 | 3.758 | **5** | 75.16% | 94.66% | **ĐẠT** |
| **16h - 17h** | 1.0655 | 2.88 | 1.20 | 3.069 | **5** | 61.37% | 99.12% | **ĐẠT** |
| **TỔNG CỘNG / TB** | | | | | **47 quầy-giờ** | **71.75%** | **96.17%** | **ĐẠT** |

---

## PHẦN 3: TỔNG HỢP TOÀN BỘ SỐ LIỆU KIỂM CHỨNG VÀ THỰC NGHIỆM BẰNG CODE (PYTHON / SIMPY)

Toàn bộ các tệp số liệu dưới đây được sinh ra trực tiếp từ mã nguồn thực thi của dự án và được đóng băng nguyên vẹn tại thư mục [`results/final_v1/`](file:///d:/KHDV/results/final_v1/).

---

### 3.1 Bảng Kiểm chứng Ba tầng và Hai Kiểm tra Độc lập (`kiem_chung.csv`)

Kiểm chứng tính đúng đắn khoa học của mô hình mô phỏng SimPy so với lý thuyết giải tích dừng (chạy 30–60 lần lặp độc lập, thời gian chạy $5.000$ phút, cắt $500$ phút warm-up):

| Tầng kiểm chứng | Chỉ số đánh giá | Giá trị Lý thuyết | Giá trị Mô phỏng | n_reps | $t_{\text{crit}}$ | Khoảng tin cậy 95% | Sai lệch tương đối | Đạt chuẩn? (`dat`) | Mức xấp xỉ (`muc_xap_xi`) | Ghi chú kỹ thuật |
|---|---

### 3.4 Phân tích Độ nhạy Toàn diện Hệ thống T6 (`do_nhay.csv`)

Mô phỏng 150 lần lặp CRN (`seed_base=80000`) trên 3 nhóm yếu tố biến động (trích từ `do_nhay.csv`):

| Nhóm yếu tố biến động | Hệ số nhân | Chính sách đánh giá | $SL$ Toàn ngày | $SL$ Giờ tệ nhất (Low CI95) | Tỉ lệ bỏ về $p_{ab}$ | Thời gian chờ $W_q$ (phút) |
|---|:---:|---|:---:|:---:|:---:|:---:|
| **Nhu cầu (Demand)** | 0.9 (-10%) | Hằng số (6 quầy) | 0.9860 | 0.9701 | 1.32% | 0.1262 |
| | 0.9 (-10%) | Tối ưu mô phỏng (44 q-h) | 0.9588 | 0.9334 | 3.65% | 0.3428 |
| | 0.9 (-10%) | Bền vững (+10% tải) | 0.9733 | 0.9541 | 2.48% | 0.2312 |
| | 1.0 (Chuẩn) | Hằng số (6 quầy) | 0.9773 | 0.9544 | 2.12% | 0.1950 |
| | 1.0 (Chuẩn) | Tối ưu mô phỏng (44 q-h) | 0.9383 | 0.9064 | 5.31% | 0.4917 |
| | 1.0 (Chuẩn) | Bền vững (+10% tải) | 0.9587 | 0.9318 | 3.67% | 0.3416 |
| | 1.1 (+10%) | Hằng số (6 quầy) | 0.9663 | 0.9334 | 3.05% | 0.2862 |
| | **1.1 (+10%)** | **Tối ưu mô phỏng (44 q-h)**| **0.9129** | **0.8843 (< 90%)** | **7.25%** | **0.6708** |
| | **1.1 (+10%)** | **Bền vững (+10% tải)** | **0.9401** | **0.9000 ($\ge$ 90%)** | **5.17%** | **0.4808** |
| | 1.2 (+20%) | Hằng số (6 quầy) | 0.9508 | 0.9042 | 4.35% | 0.4006 |
| | 1.2 (+20%) | Tối ưu mô phỏng (44 q-h) | 0.8801 | 0.8270 | 9.64% | 0.8935 |
| | 1.2 (+20%) | Bền vững (+10% tải) | 0.9164 | 0.8662 | 7.01% | 0.6498 |
| | 1.3 (+30%) | Hằng số (6 quầy) | 0.9320 | 0.8703 | 5.86% | 0.5403 |
| | 1.3 (+30%) | Tối ưu mô phỏng (44 q-h) | 0.8426 | 0.7929 | 12.26% | 1.1349 |
| | 1.3 (+30%) | Bền vững (+10% tải) | 0.8855 | 0.8185 | 9.24% | 0.8532 |
| **Thời gian phục vụ $E[S]$** | 1.0 (Chuẩn) | Tối ưu mô phỏng (44 q-h) | 0.9383 | 0.9064 | 5.31% | 0.4917 |
| | 1.0 (Chuẩn) | Bền vững (+10% tải) | 0.9587 | 0.9318 | 3.67% | 0.3416 |
| | 1.1 (+10%) | Tối ưu mô phỏng (44 q-h) | 0.9085 | 0.8685 | 7.54% | 0.7017 |
| | 1.1 (+10%) | Bền vững (+10% tải) | 0.9368 | 0.8977 | 5.38% | 0.5032 |
| | 1.2 (+20%) | Tối ưu mô phỏng (44 q-h) | 0.8708 | 0.8238 | 10.28% | 0.9428 |
| | 1.2 (+20%) | Bền vững (+10% tải) | 0.9074 | 0.8555 | 7.60% | 0.6948 |
| **Kiên nhẫn khách $\theta$** | 0.5 (Kiên nhẫn gấp đôi)| Tối ưu mô phỏng (44 q-h) | 0.9446 | 0.9118 | 3.47% | 0.6552 |
| | 0.5 (Kiên nhẫn gấp đôi)| Bền vững (+10% tải) | 0.9661 | 0.9366 | 2.31% | 0.4366 |
| | 1.0 (Chuẩn) | Tối ưu mô phỏng (44 q-h) | 0.9383 | 0.9064 | 5.31% | 0.4917 |
| | 1.0 (Chuẩn) | Bền vững (+10% tải) | 0.9587 | 0.9318 | 3.67% | 0.3416 |
| | 1.5 (Mất kiên nhẫn hơn)| Tối ưu mô phỏng (44 q-h) | 0.9317 | 0.9004 | 6.46% | 0.4016 |
| | 1.5 (Mất kiên nhẫn hơn)| Bền vững (+10% tải) | 0.9526 | 0.9267 | 4.56% | 0.2851 |

---

### 3.5 Hàm Chi phí Kinh tế và Phân tích Kịch bản Đánh đổi (`results/final_v3/chi_phi_v3.csv`)

Mô hình hóa chi phí tổng thể $C(k) = \text{Quầy-giờ} + k \cdot N \cdot p_{ab}$ trên quy mô $686.7$ khách/ngày kèm khoảng tin cậy truyền sai số từ $p_{ab}$ và hiệu số theo cặp $\Delta C = C_{44} - C_{48}$ (Nhiệm vụ S11):

| Hệ số $k$ | Chi phí Lịch 44 (CI95) | Chi phí Lịch 48 (CI95) | Chi phí Mốc 6 quầy (CI95) | Hiệu số $C_{44} - C_{48}$ | CI 95% Hiệu số | Có ý nghĩa? | Chính sách kinh tế nhất |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **$k = 0.10$** | **$47.60 \pm 0.15$** | $50.52 \pm 0.12$ | $55.43 \pm 0.09$ | **-2.92** | **[-2.99, -2.86]** | **Có** | **Lịch tối ưu 44** |
| **$k = 0.25$** | **$52.99 \pm 0.38$** | $54.29 \pm 0.30$ | $57.58 \pm 0.22$ | **-1.30** | **[-1.46, -1.14]** | **Có** | **Lịch tối ưu 44** |
| **$k = 0.50$** | $61.99 \pm 0.75$ | **$60.59 \pm 0.60$** | $61.16 \pm 0.45$ | **+1.40** | **[+1.07, +1.72]** | **Có** | **Lịch bền vững 48** |
| **$k = 1.00$** | $79.97 \pm 1.51$ | $73.18 \pm 1.21$ | **$68.32 \pm 0.90$** | **+6.79** | **[+6.14, +7.44]** | **Có** | Mốc 6 quầy |
| **$k = 2.00$** | $115.94 \pm 3.01$ | $98.36 \pm 2.42$ | **$82.64 \pm 1.79$** | **+17.58** | **[+16.28, +18.88]** | **Có** | Mốc 6 quầy |

*Điểm cân bằng kinh tế:*  
- Khi $k \le 0.25$: Chi phí bỏ về thấp, Lịch 44 tiết kiệm chi phí quầy vượt trội nên rẻ hơn có ý nghĩa thống kê.
- Khi $k \ge 0.50$: Thiệt hại mất khách gia tăng, Lịch 48 trở nên tối ưu hơn nhờ giảm 30% lượng khách bỏ về.

### 3.6 Kết quả Bài toán Lập lịch Ca làm việc MILP (`lich_theo_ca_v2.csv` & `b_shifts.py`)

Định nghĩa rõ ràng 2 mô hình ca làm việc trong ngành ngân hàng:
- **Mô hình A (Ca liên tục):** Ca 8 giờ làm việc liên tục (không nghỉ trưa), bắt đầu từ 8h (8h–16h) hoặc 9h (9h–17h). Ca 4 giờ liên tục (bắt đầu từ 8h đến 13h).
- **Mô hình B (Ca có nghỉ trưa - Chuẩn thực tế):** Nhân viên có mặt 9 giờ tại chi nhánh, nghỉ trưa 1 giờ không hưởng lương, làm việc thực tế 8 giờ. Giờ nghỉ trưa bố trí trong khung 11h–14h (giờ 3–5) hoặc khung rộng 9h–16h (giờ 1–7).

Bảng so sánh các phương án tổ chức ca giải bằng `scipy.optimize.milp` (`b_shifts.py`):

| Mô hình & Phương án ca | Mẫu phủ quầy theo giờ | Giờ công làm việc | Giờ có mặt chi nhánh | Số nhân viên | Đánh giá tính khả thi |
|---|:---:|:---:|:---:|:---:|---|
| **Yêu cầu tối ưu từng giờ** | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | **44 q-h** | - | - | Chuẩn mốc giải tích / SimPy |
| **Mô hình B: Hỗn hợp (4 NV 8h + 3 NV 4h)**| `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | **44 q-h** | **48 giờ** | **7 NV** (4 FT + 3 PT) | **Phủ khớp chính xác 44 q-h (Lãng phí 0.0%)**; Giờ nghỉ trưa tại 11h, 12h, 13h |
| **Mô hình B: Chỉ ca 8h (nghỉ 9h-16h)** | `[6, 5, 6, 5, 5, 5, 5, 5, 6]` | 48 q-h | 54 giờ | 6 NV FT | Lãng phí +4 q-h (+9.1%) do thừa quầy đầu/cuối ngày |
| **Mô hình B: Chỉ ca 8h (nghỉ 11h-14h)**| `[8, 8, 8, 6, 5, 5, 8, 8, 8]` | 64 q-h | 72 giờ | 8 NV FT | Lãng phí +20 q-h (+45.5%) do dồn nhân sự khi cửa sổ nghỉ hẹp |
| **Chỉ dùng ca bán thời gian 4h** | `[4, 5, 6, 6, 5, 8, 7, 7, 4]` | 52 q-h | 52 giờ | 13 lượt ca 4h | Lãng phí +8 q-h (+18.2%) |
| **Mô hình A: Chỉ ca 8h liên tục** | `[4, 8, 8, 8, 8, 8, 8, 8, 4]` | 64 q-h | 64 giờ | 8 NV FT | Lãng phí +20 q-h (+45.5%) do thừa công suất giữa ngày |
| **Mô hình A: 4 NV 8h + 3 NV 4h** | - | - | - | - | **Không có nghiệm khả thi** |
| **Mô hình B: Phủ mốc 6 quầy cả ngày** | `[7, 6, 6, 6, 6, 6, 6, 6, 7]` | 56 q-h | 63 giờ | 7 NV FT | Cần ít nhất 7 NV (không thể phủ 6 quầy cả ngày chỉ với 6 NV khi có giờ nghỉ) |

---

### 3.7 Phân tích Bootstrap Lồng nhau và Phân rã Phương sai ANOVA (`results/final_v3/phan_ra_phuong_sai.csv`)

Thiết kế mô hình lồng nhau: $B = 50$ bộ tham số (resample theo ngày để giữ nguyên cấu trúc quá phân tán) $\times R = 60$ lần lặp/bộ (Nhiệm vụ S5):

| Chỉ số phân rã phương sai | Giá trị thực nghiệm | Khoảng tin cậy 95% | Diễn giải ý nghĩa khoa học |
|---|:---:|:---:|---|
| **SL Toàn ngày danh nghĩa ($R=60$)** | **0.9381** | [0.9335, 0.9427] | Trung bình qua 60 lần lặp độc lập |
| **SL Giờ tệ nhất danh nghĩa ($R=60$)** | **0.9060** | - | Trung bình theo giờ rồi lấy min (cùng định nghĩa) |
| **Phương sai tổng quan sát qua 50 bộ** | $1.294 \times 10^{-4}$ | - | $SD = 0.01138$ |
| **Phương sai do nhiễu mô phỏng (Within / R)** | $5.446 \times 10^{-6}$ | - | Sai số ngẫu nhiên Monte Carlo |
| **Phương sai do bất định tham số (Between)** | $1.240 \times 10^{-4}$ | - | Bất định thực sự từ việc ước lượng tham số |
| **Tỉ lệ phương sai do bất định tham số** | **95.79%** | - | **Bất định tham số chi phối gần như tuyệt đối** |
| **Tỉ lệ phương sai do nhiễu mô phỏng** | **4.21%** | - | Với $R=60$, nhiễu mô phỏng triệt tiêu xuống dưới 5% |
| **Xác suất SL toàn ngày $\ge 90\%$** | **100.0%** | [92.87%, 100.0%] | 50/50 bộ bootstrap đạt chuẩn toàn ngày |
| **Xác suất SL giờ tệ nhất $\ge 90\%$** | **90.0%** | [78.64%, 95.65%] | 45/50 bộ bootstrap đạt chuẩn giờ tệ nhất |

### 3.8 Độ nhạy theo Phân phối Thời gian Phục vụ kèm Giờ Tệ nhất (`results/final_v3/do_nhay_phan_phoi_v3.csv`)

Mô phỏng 150 lần lặp độc lập cho 4 phân phối, báo cáo giờ tệ nhất và CI hiệu số theo cặp (Nhiệm vụ S9):

| Phân phối phục vụ | $SL$ Toàn ngày (CI95) | Giờ tệ nhất | $SL$ Giờ tệ nhất | Giờ tệ nhất Low CI95 | Hiệu số so với Gamma | CI 95% Hiệu số | Khác biệt có ý nghĩa? |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Gamma (AIC tốt nhất)** | **0.9431 ± 0.0028** | 16h - 17h | 0.9252 | **0.9149** | Gốc (0.0000) | [0.0000, 0.0000] | - |
| **Bootstrap thực tế** | 0.9353 ± 0.0035 | 11h - 12h | 0.9159 | **0.9056** | -0.0078 | [-0.0122, -0.0034] | **Có** ($0 \notin CI$) |
| **Exponential (M/M/c)** | 0.9383 ± 0.0032 | 16h - 17h | 0.9177 | **0.9071** | -0.0048 | [-0.0091, -0.0005] | **Có** ($0 \notin CI$) |
| **Lognormal ($cv$ + 20%)** | **0.9321 ± 0.0039** | 16h - 17h | 0.9091 | **0.8940** | **-0.0110** | **[-0.0155, -0.0066]** | **Có (Sát ngưỡng 90%)** |

### 3.9 Đánh giá Ngoài mẫu với Khoảng Dự báo 95% (PI95) và Holm-Bonferroni (`results/final_v3/ngoai_mau_v3.csv`)

So sánh tập Test (4 ngày, $2.969$ khách) với Khoảng dự báo 95% (PI95) sinh từ 1.000 bộ 4 ngày mô phỏng có biến động ngày và kiểm định hiệu chỉnh Holm-Bonferroni (Nhiệm vụ S6):

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
> 7/9 khung giờ quan sát thực tế nằm gọn trong Khoảng dự báo 95%. Khác biệt tại giờ 15h–16h ($SL = 76.47\%$) được ghi nhận như một **giả thuyết cần kiểm chứng**: vào cuối ngày, các giao dịch viên thực tế có thể phải tập trung chốt sổ, kiểm quỹ hoặc quầy mở thực tế bị rút giảm. Kiểm định Welch giữa tổng khách Train và Test cho thấy không có sự khác biệt có ý nghĩa thống kê về nhu cầu tổng thể ($t=1.74, p=0.115$).

### 3.10 Kết quả Kiểm thử Tự động pytest 22/22 Passed (`results/final_v3/pytest_log.txt`)

Toàn bộ **22 ca kiểm thử đơn vị tự động** trong thư mục `tests/` chạy qua thành công 100% trong 9.82 giây:
- 12 bài test chuẩn giải tích và mô phỏng (`test_theory.py`, `test_sim.py`).
- 6 bài test tính năng ca làm việc MILP và biến động ngày (`test_v2_features.py`).
- 4 bài test thống kê chuẩn mực mới: `test_wilson_ci_properties`, `test_student_t_ci_degrees_of_freedom`, `test_holm_bonferroni_adjustment`, `test_early_hour_predictor_correlation`.

### 3.11 Khảo sát Vét cạn Pha 3 và Bảng 14 Ngày Thực tế (`results/final_v3/pha3.csv` & `theo_14_ngay_v3.csv`)
1. **Khảo sát Pha 3 (C6):** Thử nghiệm 117 cấu hình lân cận (72 swap 1 quầy + 36 double reduction). Kết quả: **0/117 cấu hình khả thi** đạt chuẩn SLA $\ge 90\%$. Lịch 44 là **nghiệm tối thiểu cục bộ duy nhất**.
2. **Đối chiếu 14 ngày thực tế (S7):** Lịch 44 đạt **12/14 ngày (85.7% [60.1%, 96.0%])** (chỉ hụt ngày 2 và ngày 7 có tải cực đại). Lịch 48 và Mốc 6 quầy đạt **14/14 ngày (100% [78.5%, 100%])**.

## PHẦN 4: ĐỐI CHIẾU CHÉO GIỮA EXCEL, LÝ THUYẾT VÀ MÔ PHỎNG SIMPY

Bảng đối chiếu tổng hợp phương án số quầy theo từng giờ giữa các phương pháp:

| Khung giờ | Excel (Erlang C tĩnh) | Lý thuyết (Erlang-A SIPP) | SimPy Tối ưu (2 pha xác nhận SIPP) | SimPy Bền vững (+10% tải) | Mốc cơ sở: Hằng số 6 quầy |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h - 9h** | 4 | **4** | **4** | 5 | 6 |
| **9h - 10h** | 6 | **5** | **5** | 6 | 6 |
| **10h - 11h (Đỉnh)** | 6 | **6** | **6** | 6 | 6 |
| **11h - 12h** | 6 | **5** | **5** | 6 | 6 |
| **12h - 13h** | 5 | **5** | **5** | 5 | 6 |
| **13h - 14h** | 5 | **5** | **5** | 5 | 6 |
| **14h - 15h** | 5 | **5** | **5** | 5 | 6 |
| **15h - 16h** | 5 | **5** | **5** | 5 | 6 |
| **16h - 17h** | 5 | **4** | **4** | 5 | 6 |
| **TỔNG QUẦY-GIỜ** | **47 quầy-giờ** | **44 quầy-giờ** | **44 quầy-giờ** | **48 quầy-giờ** | **54 quầy-giờ** |
| **Tỉ lệ tiết kiệm** | -12.96% | **-18.52%** | **-18.52%** | -11.11% | Gốc mốc |

### Giải thích Nguyên nhân Chênh lệch Khoa học:
1. **Vì sao Erlang C trên Excel cần 47 quầy-giờ trong khi Erlang-A và SimPy chỉ cần 44 quầy-giờ?**  
   - Erlang C giả định khách hàng có độ kiên nhẫn vô hạn ($\theta = 0$). Tại các khung giờ có tải cao (9h-10h, 11h-12h, 16h-17h), để đưa thời gian chờ xuống dưới 5 phút, Erlang C buộc phải cấp thêm 1 quầy ở mỗi giờ.  
   - Trong thực tế, khách hàng có tốc độ bỏ về $\theta = 0.1087 \text{ phút}^{-1}$ (kiên nhẫn TB 9.2 phút). Hành vi bỏ về tạo cơ chế "tự giải tỏa áp lực" cho hàng đợi, giúp hệ thống đạt chuẩn cam kết SLA $\ge 90\%$ chỉ với 5 quầy (thay vì 6 quầy) mà không gây ùn tắc, tiết kiệm được **3 quầy-giờ**.
2. **Vì sao lịch tối ưu SimPy khớp đúng với SIPP Erlang-A ở mức 44 quầy-giờ?**  
   - Với kích thước hệ thống ngân hàng cá nhân ($c \approx 4 - 6$ quầy), pha chuyển tiếp quán tính giữa các khung giờ không làm vỡ cam kết chất lượng do thời gian phục vụ trung bình tương đối ngắn ($E[S] = 2.92$ phút $\approx 1/20$ độ dài khung giờ 60 phút).  
   - Thuật toán SimPy 2 pha xác nhận lịch `[4, 5, 6, 5, 5, 5, 5, 5, 4]` là tối thiểu cục bộ (không thể hoán đổi hay giảm bớt quầy nào mà vẫn giữ $SL_{\text{low 95\%}} \ge 0.90$ trên cả 9 giờ).

---

## PHẦN 5: BẢNG TỔNG HỢP QUYẾT ĐỊNH KHUYẾN NGHỊ CUỐI CÙNG

Dưới đây là bảng tổng kết quyết định quản trị vận hành chính thức dành cho Ban Giám đốc Chi nhánh Ngân hàng:

| Tiêu chí quản trị | Phương án Tối ưu Thường nhật (Khuyến nghị 1) | Phương án Dự phòng Bền vững (Khuyến nghị 2) | Mốc cơ sở: Hằng số 6 quầy (không phải nhân sự thực tế) |
|---|---|---|---|
| **Lịch quầy chi tiết theo giờ** | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | `[5, 6, 6, 6, 5, 5, 5, 5, 5]` | `[6, 6, 6, 6, 6, 6, 6, 6, 6]` |
| **Tổng số quầy-giờ mở** | **44 quầy-giờ/ngày** | **48 quầy-giờ/ngày** | **54 quầy-giờ/ngày** |
| **Hiệu quả cắt giảm chi phí** | **Tiết kiệm 18.52% (-10 q-h mở/ngày)**<br>*(Tiết kiệm 21.43% theo giờ công 44 vs 56)* | **Tiết kiệm 11.11% (-6 q-h mở/ngày)**<br>*(Tiết kiệm 14.29% theo giờ công 48 vs 56)* | Mốc cơ sở (0.0%) |
| **Mức phục vụ $SL$ danh định (CI95)** | **$93.81\% \pm 0.23\%$** | **$95.82\% \pm 0.18\%$** | $97.70\% \pm 0.12\%$ |
| **Mức phục vụ $SL$ giờ tệ nhất (Low CI95)** | **$90.78\%$** (H8, 300 lần lặp; lần chạy tối ưu 60 lần lặp: H3, $90.72\%$) | **$93.64\%$** | $95.57\%$ |
| **$P(SL \text{ kỳ vọng ngày} \ge 90\%)$** | **$88.5\%$** (Wilson 95%: $[83.3\%, 92.2\%]$) | **$98.5\%$** (Wilson 95%: $[95.7\%, 99.5\%]$) | **$100.0\%$** (Wilson 95%: $[98.1\%, 100.0\%]$) |
| **$P(\min_h E_h(m) \ge 90\%)$** | **$65.5\%$** (Wilson 95%: $[58.7\%, 71.7\%]$)<br>*Số giờ $E_h < 90\%$ TB: 1.17 giờ* | **$82.5\%$** (Wilson 95%: $[76.6\%, 87.1\%]$)<br>*Số giờ $E_h < 90\%$ TB: 0.35 giờ* | **$97.5\%$** (Wilson 95%: $[94.3\%, 98.9\%]$)<br>*Số giờ $E_h < 90\%$ TB: 0.03 giờ* |
| **$P(\text{thực tế mọi giờ} \ge 90\%)$** | **$25.7\%$** (Wilson 95%: $[24.6\%, 26.8\%]$)<br>*(Chịu chi phối mạnh bởi cỡ mẫu giờ)* | **$46.1\%$** (Wilson 95%: $[44.9\%, 47.4\%]$)<br>*(Chịu chi phối mạnh bởi cỡ mẫu giờ)* | **$76.2\%$** (Wilson 95%: $[75.1\%, 77.2\%]$) |
| **$P(\text{gộp tháng 20 ngày mọi giờ} \ge 90\%)$** | **$58.3\%$** (Wilson 95%: $[52.7\%, 63.8\%]$) | **$78.0\%$** (Wilson 95%: $[73.0\%, 82.3\%]$) | **$97.3\%$** (Wilson 95%: $[94.8\%, 98.6\%]$) |
| **Số ngày thực tế 14 ngày đạt SLA** | **12/14 ngày (85.7% [60.1%, 96.0%])**<br>*(Hụt ngày 2: 87.8% và ngày 7: 88.3%)* | **14/14 ngày (100.0% [78.5%, 100.0%])** | **14/14 ngày (100.0% [78.5%, 100.0%])** |
| **Mức phục vụ Khách VIP ($W_q \le 2$p)** | **$94.96\% \pm 0.25\%$** | **$96.64\% \pm 0.19\%$** | $98.15\% \pm 0.14\%$ |
| **Thời gian chờ trung bình $W_q$** | **$0.4908 \pm 0.0155$ phút (~29.4 giây)** | **$0.3424 \pm 0.0120$ phút (~20.5 giây)** | $0.1958 \pm 0.0089$ phút (~11.7 giây) |
| **Tỉ lệ khách hàng bỏ về trung bình** | **$5.35\% \pm 0.17\%$** | **$3.73\% \pm 0.14\%$ (Giảm 30% khách mất)** | $2.15\% \pm 0.10\%$ |
| **Hiệu suất sử dụng quầy $\rho$** | **$72.15\% \pm 0.38\%$ (Tối ưu năng suất)**| **$67.25\% \pm 0.37\%$** | $60.75\% \pm 0.36\%$ (Lãng phí quầy) |
| **Phương án tổ chức ca làm việc** | **Mô hình B: 4 NV 8h (nghỉ trưa) + 3 NV 4h**<br>*(Nghỉ trưa 11h-14h, duy nhất 1 nghiệm)* | **Mô hình B: 5 NV 8h (nghỉ trưa) + 2 NV 4h**<br>*(Cửa sổ nghỉ 1-7: có 4 nghiệm khả thi)* | **7 NV 8h (56 q-h công làm việc)**<br>*(6 NV có nghỉ chỉ làm được 48 q-h)* |
| **Chi phí phụ trội do tổ chức ca** | **+0.0% (Phủ chính xác 44 q-h)** | **+0.0% (Phủ chính xác 48 q-h)** | +0.0% |
| **Độ bền khi nhu cầu tăng +10%** | Giờ tệ nhất Low CI95 là **$88.43\%$** (Điểm ước lượng $89.84\%$) | **Giờ tệ nhất giữ vững $\ge 90.00\%$** (Low CI95: $90.00\%$, Điểm ước lượng $92.68\%$) | Giờ tệ nhất giữ vững $93.30\%$ |
| **Quy tắc kích hoạt vận hành** | Áp dụng khi $\hat{V} \le 700$ khách/ngày (dự báo sớm 8h-10h: $r=0.842, p=0.0002$) | Kích hoạt chuyển quầy lúc 10h khi $\hat{V} > 700$ khách/ngày | Mốc lý thuyết đối chiếu |

