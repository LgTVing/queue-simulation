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
| **Phân phối phục vụ tốt nhất** | **Gamma / Lognormal**| - | Phân phối mũ bị bác bỏ do dữ liệu thực tế có đuôi phải dày |
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

| Tầng kiểm chứng | Chỉ số đánh giá | Giá trị Lý thuyết | Giá trị Mô phỏng | Khoảng tin cậy 95% | Sai lệch tương đối | Đạt chuẩn? (`dat`) | Mức xấp xỉ (`muc_xap_xi`) | Ghi chú kỹ thuật |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **Tầng 1 (M/M/c)** | $SL = P(W_q \le 5\text{p})$ | 0.9654 | **0.9688** | ±0.0037 | $+0.35\%$ | **Y** | Tot | Lý thuyết nằm trong CI95 |
| **Tầng 1 (M/M/c)** | $W_q$ (phút) | 0.8433 | **0.8170** | ±0.0423 | $-3.12\%$ | **Y** | Tot | Lý thuyết nằm trong CI95 (0.817 ± 0.042) |
| **Tầng 1 (M/M/c)** | Hiệu suất quầy $\rho$ | 0.7500 | **0.7517** | ±0.0047 | $+0.23\%$ | **Y** | Tot | Khớp định luật Little ($\rho = 0.75$) |
| **Tầng 2 (Erlang-A)** | $SL$ (phục vụ & chờ $\le 5$p) | 0.8689 | **0.8695** | ±0.0034 | $+0.07\%$ | **Y** | Tot | Khớp nghiệm ma trận hấp thụ Markov |
| **Tầng 2 (Erlang-A)** | $W_q$ (phút) | 1.1444 | **1.1475** | ±0.0233 | $+0.27\%$ | **Y** | Tot | $W_q$ tính trên mọi khách ($L_q / \lambda$) |
| **Tầng 2 (Erlang-A)** | Tỉ lệ bỏ về $p_{ab}$ | 0.1144 | **0.1142** | ±0.0022 | $-0.21\%$ | **Y** | Tot | Lý thuyết nằm trong CI95 |
| **Tầng 2 (Erlang-A)** | Hiệu suất quầy $\rho$ | 0.8856 | **0.8871** | ±0.0031 | $+0.17\%$ | **Y** | Tot | Khớp $\rho = \lambda(1-p_{ab})E[S]/c$ |
| **Tầng 3 (M/G/c, cv=0.5)** | $W_q$ (phút) | 0.5271 | **0.5616** | ±0.0176 | $+6.55\%$ | - | Chap nhan duoc | Allen–Cunneen đánh giá thấp ~6-7% ở cv=0.5 |
| **Tầng 3 (M/G/c, cv=1.0)** | $W_q$ (phút) | 0.8433 | **0.8113** | ±0.0521 | $-3.80\%$ | - | Tot | Khớp Erlang C chuẩn (sai lệch < 5%) |
| **Tầng 3 (M/G/c, cv=1.5)** | $W_q$ (phút) | 1.3704 | **1.1333** | ±0.1239 | $-17.30\%$ | - | Kem, can giai thich | Allen–Cunneen đánh giá cao; kiểm tra bằng M/G/1 |
| **Kiểm tra A (M/G/1 P-K exact)** | $W_q$ (phút) | **14.6250** | **13.8669** | ±1.5388 | **$-5.18\%$** | **Y** | Tot | Lý thuyết $14.625$p nằm trong CI95; SimPy đúng tuyệt đối |
| **Kiểm tra B (M/G/6, cv=1.5, 60 reps)** | $W_q$ (phút) | 1.3704 | **1.1815** | ±0.0722 | $-13.78\%$ | - | Kem, can giai thich | Sai lệch ổn định ~-14% đến -17% do Allen-Cunneen |

---

### 3.2 Lịch sử Thuật toán Tối ưu hóa 2 Pha SimPy (`lich_toi_uu.csv`)

Thuật toán tối ưu hóa dựa trên mô phỏng thực thi qua 10 bước lặp (60 lần lặp/bước, CRN):

| Bước (`buoc`) | Pha (`pha`) | Lịch quầy thử nghiệm (`lich`) | Tổng quầy-giờ | $SL$ Toàn ngày | Giờ tệ nhất | $SL$ Giờ tệ nhất (Low CI95) | Giờ vi phạm SLA | Khả thi SLA? |
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

*Kết luận tối ưu:* Lịch `[4, 5, 6, 5, 5, 5, 5, 5, 4]` (44 quầy-giờ) là nghiệm tối thiểu cục bộ theo thuật toán 2 pha (bớt từng quầy) khởi tạo từ SIPP (được mô phỏng xác nhận). Thử nghiệm Pha 3 (thử hoán đổi 1 quầy giữa hai giờ và bớt đồng thời 2 quầy) xác nhận không tìm thấy lịch khả thi nào có tổng quầy-giờ nhỏ hơn 44 quầy-giờ. Thử nghiệm giảm 1 quầy ở bất kỳ giờ nào (từ Step 1 đến Step 9) đều khiến mức phục vụ giờ đó rơi xuống dưới $90\%$ (từ $76.2\%$ đến $87.9\%$).

---

### 3.3 Bảng Đánh giá và So sánh Các Chính sách Phục vụ (`so_sanh_chinh_sach.csv` & `so_sanh_chinh_sach_v2.csv`)

#### (a) Đánh giá dưới điều kiện tham số danh nghĩa (300 lần lặp độc lập, `seed_base=50000`):

| Chính sách phục vụ | Lịch quầy theo giờ | Quầy-giờ | $SL$ Toàn ngày (CI95) | $SL$ Giờ tệ nhất (Cận dưới CI95) | Mức phục vụ VIP $SL_{vip}$ (CI95) | Tỉ lệ bỏ về $p_{ab}$ (CI95) | Thời gian chờ $W_q$ (phút) | Hiệu suất quầy $\rho$ (CI95) | Đạt SLA? |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Mốc cơ sở (Hằng số 6 quầy)** | `[6, 6, 6, 6, 6, 6, 6, 6, 6]` | 54 | 0.9770 ± 0.0012 | 0.9557 (H2) | 0.9815 ± 0.0014 | 2.15% ± 0.10% | 0.1958 ± 0.0089 | 60.75% ± 0.36% | **ĐẠT** |
| **SIPP (Erlang-A, mô phỏng xác nhận)**| `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | **44** | **0.9381 ± 0.0023** | **0.9078 (H8)** | **0.9496 ± 0.0025** | **5.35% ± 0.17%** | **0.4908 ± 0.0155** | **72.15% ± 0.38%** | **ĐẠT** |
| **Bền vững (+10% tải)** | `[5, 6, 6, 6, 5, 5, 5, 5, 5]` | 48 | 0.9582 ± 0.0018 | 0.9364 (H6) | 0.9664 ± 0.0019 | 3.73% ± 0.14% | 0.3424 ± 0.0120 | 67.25% ± 0.37% | **ĐẠT** |
| **Theo ca làm việc (MILP hỗn hợp)** | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | 44 | 0.9381 ± 0.0023 | 0.9078 (H8) | 0.9496 ± 0.0025 | 5.35% ± 0.17% | 0.4908 ± 0.0155 | 72.15% ± 0.38% | **ĐẠT** |

#### (b) Đánh giá khi có biến động lưu lượng giữa các ngày ($m_d \sim \text{Gamma}$, $CV_{\text{ngày}} = 11.8\%$, 300 lần lặp, `seed_base=20000`):

| Chính sách phục vụ | Quầy-giờ | $SL$ Toàn ngày TB | $P(\text{Ngày} \ge 90\%)$ | $P(\text{Mọi giờ} \ge 90\%)$ | $SL$ Phân vị 5% | Số giờ TB $< 90\%$ | Tỉ lệ bỏ về | $W_q$ (phút) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Mốc cơ sở (6 quầy)** | 54 | 0.9751 ± 0.0017 | **100.0%** | **78.0%** | 0.9423 | 0.28 | 2.33% | 0.2140 |
| **Bền vững (48 q-h)** | 48 | 0.9548 ± 0.0029 | **95.3%** | **47.0%** | 0.9076 | 0.93 | 4.02% | 0.3780 |
| **Tối ưu (44 q-h)** | 44 | 0.9340 ± 0.0040 | **85.0%** | **26.0%** | 0.8656 | 1.86 | 5.76% | 0.5420 |

> [!IMPORTANT]
> **Phát hiện cốt lõi từ biến động ngày (Nhiệm vụ T2):**  
> Khi tính đến biến động lưu lượng giữa các ngày thực tế, lịch tối ưu 44 quầy-giờ chỉ đạt $SL \ge 90\%$ trên **85.0% số ngày**, và xác suất mọi khung giờ trong ngày đều $\ge 90\%$ giảm xuống **26.0%** (trong các ngày đông khách, phân vị 5% rơi xuống $86.56\%$). Ngược lại, lịch bền vững 48 quầy-giờ bảo đảm $P(\text{Ngày} \ge 90\%) = 95.3\%$ và phân vị 5% vẫn giữ vững trên $90.76\%$. Điều này giải thích tại sao cần quy tắc vận hành linh hoạt theo lưu lượng.

---

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

### 3.5 Hàm Chi phí Kinh tế và Phân tích Kịch bản Đánh đổi (`chi_phi.csv`)

Phân tích kinh tế theo kịch bản $k = c_a / c_q$ trên quy mô trung bình $686.7$ khách/ngày:

| Chính sách phục vụ | Quầy-giờ | Tỉ lệ bỏ về $p_{ab}$ | Số khách bỏ về / ngày | Đạt SLA? | Chi phí ($k=0.10$) | Chi phí ($k=0.25$) | Chi phí ($k=0.50$) | Chi phí ($k=1.00$) | Chi phí ($k=2.00$) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Hằng số (6 quầy)** | 54 | 2.15% | 14.8 khách | Y | 55.48 | 57.69 | 61.38 | **68.76** | **83.53** |
| **SIPP (Erlang-A)** | 44 | 5.35% | 36.7 khách | Y | **47.67** | **53.18** | 62.37 | 80.74 | 117.48 |
| **Tối ưu mô phỏng (44 q-h)**| 44 | 5.35% | 36.7 khách | Y | **47.67** | **53.18** | 62.37 | 80.74 | 117.48 |
| **Bền vững (+10% tải)**| 48 | 3.73% | 25.6 khách | Y | 50.56 | 54.40 | **60.81** | 73.61 | 99.23 |
| **Theo ca làm việc** | 52 | 2.72% | 18.7 khách | Y | 53.87 | 56.67 | 61.34 | 70.68 | 89.36 |

---

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

### 3.7 Phân tích Độ bất định Tham số qua 50 Bộ Bootstrap (`bat_dinh_tham_so.csv`)

Phân biệt tường minh hai định nghĩa:
1. **$SL$ Giờ tệ nhất danh nghĩa (Bảng 3.3):** Cận dưới khoảng tin cậy 95% của giờ có $SL$ thấp nhất (qua 300 lần lặp độc lập với tham số danh nghĩa, ví dụ: $90.78\%$).
2. **Phân phối Giờ tệ nhất qua Bootstrap (Bảng 3.7):** Giá trị trung bình của giờ tệ nhất được tính trên từng bộ tham số trong số 50 bộ bootstrap tái lấy mẫu từ dữ liệu gốc.

| Chỉ số độ bất định | Lịch tối ưu Sim-Optimized (44 q-h) | Lịch bền vững Robust (48 q-h) |
|---|:---:|:---:|
| **Xác suất $SL$ Toàn ngày $\ge 90\%$** | **100.0%** (50/50 bộ đạt) | **100.0%** (50/50 bộ đạt) |
| **Khoảng phân vị 5% - 95% $SL$ Toàn ngày** | **[0.9289, 0.9457]** | **[0.9501, 0.9634]** |
| **Giá trị $SL$ Toàn ngày trung bình** | 0.9378 | 0.9575 |
| **Xác suất $SL$ Giờ tệ nhất $\ge 90\%$** | **6.0%** (3/50 bộ đạt) | **38.0%** (19/50 bộ đạt) |
| **Khoảng phân vị 5% - 95% Giờ tệ nhất** | [0.8645, 0.8944] | [0.8812, 0.9215] |

> [!NOTE]
> Sự khác biệt giữa mức đạt danh nghĩa ($90.78\%$) và xác suất đạt giờ tệ nhất qua bootstrap ($6.0\%$) phản ánh tác động của **sai số mẫu trong ước lượng tham số**. Do đó, lịch 44 quầy-giờ cần đi kèm quy tắc kích hoạt dự phòng 48 quầy-giờ khi nhu cầu thực tế cao hơn bình quân.

*(Toàn bộ 50 dòng chi tiết của từng bộ tham số được lưu tại `results/final_v1/bat_dinh_tham_so.csv`).*

---

### 3.8 Độ nhạy theo Phân phối Thời gian Phục vụ (`do_nhay_phan_phoi_v2.csv`)

Khảo sát ảnh hưởng của giả định phân phối thời gian phục vụ bằng phương pháp so sánh cặp số ngẫu nhiên chung (CRN Paired Difference, 150 lần lặp):

| Phân phối phục vụ thử nghiệm | $SL$ Toàn ngày (CI95) | Cận dưới CI95 | Hiệu số so với Gamma | Khoảng tin cậy 95% của Hiệu số | Khác biệt có ý nghĩa thống kê? |
|---|:---:|:---:|:---:|:---:|:---:|
| **Gamma chuẩn (AIC tốt nhất)** | **0.9385 ± 0.0032** | 0.9353 | Gốc (0.0000) | [0.0000, 0.0000] | - |
| **Bootstrap trực tiếp từ dữ liệu** | 0.9376 ± 0.0036 | 0.9340 | -0.0009 | [-0.0055, +0.0038] | **Không** ($0 \in CI$) |
| **Mũ (Exponential - Đuôi nhẹ)** | 0.9377 ± 0.0030 | 0.9347 | -0.0008 | [-0.0054, +0.0037] | **Không** ($0 \in CI$) |
| **Lognormal ($cv$ tăng 20% - Đuôi nặng)**| 0.9312 ± 0.0038 | 0.9274 | **-0.0073** | **[-0.0116, -0.0029]** | **Có** ($0 \notin CI$, $SL$ giảm có ý nghĩa) |

*Kết luận:* Hiệu năng của lịch 44 quầy-giờ không khác biệt có ý nghĩa giữa Gamma, Bootstrap và Mũ, nhưng **nhạy cảm rõ rệt với phân phối Lognormal có đuôi nặng** (mức phục vụ giảm khoảng $0.73$ điểm phần trăm). Cận dưới giờ tệ nhất của các cấu hình nằm sát ngưỡng $90\%$, khẳng định sự cần thiết của phương án dự phòng khi hệ thống có nguy cơ phát sinh tác vụ phức tạp đuôi dài.

---

### 3.9 Đánh giá Ngoài mẫu trên Tập Test 4 Ngày (`results/final_v2/ngoai_mau_v2.csv`)

> **Lưu ý quan trọng về điều kiện đối chiếu ngoài mẫu:**
> Số liệu thực tế quan sát được ghi nhận dưới điều kiện vận hành thực tế của ngân hàng (không rõ số quầy trực thực tế từng giờ), **không phải chạy dưới lịch khuyến nghị** `[4, 5, 6, 5, 5, 5, 5, 5, 4]`. Do đó, đây là đối chiếu kiểm tra tính hợp lý của mô hình dự báo chứ không phải so sánh A/B test trực tiếp.
> Đặc biệt, tại khung giờ **15h - 16h**, thực tế ghi nhận mức phục vụ sụt giảm mạnh ($76.47\%$, bỏ về $15.03\%$, $W_q = 1.41$ phút) trong khi mô phỏng dự báo $SL = 95.07\%$ với 5 quầy. Sự khác biệt này phản ánh hiện tượng vận hành thực tế: cuối giờ chiều nhân viên thường phải xử lý dồn hóa đơn, đóng sổ cuối ngày, hoặc số quầy phục vụ thực tế bị rút bớt xuống thấp hơn 5 quầy.

Bảng so sánh chi tiết:

| Khung giờ | Số quầy giả định | $\lambda_{\text{train}}$ | $\lambda_{\text{test}}$ | $SL$ Mô phỏng tập Test | $SL$ Low CI95 | $SL$ Thực tế quan sát | $W_q$ Mô phỏng (phút) | $W_q$ Thực tế (phút) | Bỏ về Mô phỏng | Bỏ về Thực tế |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h - 9h** | 4 | 0.9900 | 1.0917 | 0.9364 | 0.9286 | 0.9809 | 0.4291 | 0.0992 | 5.94% | 1.91% |
| **9h - 10h** | 5 | 1.3767 | 1.5750 | 0.9172 | 0.9082 | 0.9735 | 0.6183 | 0.2918 | 7.51% | 2.65% |
| **10h - 11h** | 6 | 1.5350 | 1.9167 | 0.9169 | 0.9076 | 0.9283 | 0.6114 | 0.5350 | 7.45% | 7.17% |
| **11h - 12h** | 5 | 1.3900 | 1.5625 | 0.8993 | 0.8888 | 0.9413 | 0.6814 | 0.5418 | 8.76% | 5.87% |
| **12h - 13h** | 5 | 1.2400 | 1.2375 | 0.9552 | 0.9487 | 0.9865 | 0.3273 | 0.1698 | 4.18% | 1.35% |
| **13h - 14h** | 5 | 1.2017 | 1.3458 | 0.9457 | 0.9387 | 0.9443 | 0.4092 | 0.4549 | 4.99% | 5.57% |
| **14h - 15h** | 5 | 1.3383 | 1.2792 | 0.9439 | 0.9363 | 0.8958 | 0.3996 | 0.5463 | 5.02% | 9.12% |
| **15h - 16h** | 5 | 1.3167 | 1.2750 | 0.9507 | 0.9432 | 0.7647 | 0.3657 | 1.4103 | 4.57% | 15.03% |
| **16h - 17h** | 4 | 1.0567 | 1.0875 | 0.9245 | 0.9159 | 0.9387 | 0.5331 | 0.3241 | 6.66% | 6.13% |

---

### 3.10 Kết quả Kiểm thử Tự động pytest 18/18 Passed

Toàn bộ 18 ca kiểm thử đơn vị tự động trong thư mục `tests/` chạy qua thành công 100% (log ghi nhận tại `results/final_v2/pytest_log.txt`):

| STT | File kiểm thử | Tên hàm kiểm thử | Nội dung kiểm tra | Kết quả |
|:---:|---|---|---|:---:|
| 1 | `tests/test_theory.py` | `test_mmc_reference` | Kiểm tra giá trị chuẩn Erlang C ($a=4.5, c=6$): $P_w, W_q, P(W_q \le 5)$ | **PASSED** |
| 2 | `tests/test_theory.py` | `test_mmc_unstable` | Kiểm tra hệ thống quá tải ($\rho = 1.0$): $W_q \to \infty, SL = 0$ | **PASSED** |
| 3 | `tests/test_theory.py` | `test_monotone_in_c` | Kiểm tra tính đơn điệu tăng của mức phục vụ $SL$ theo số quầy $c$ | **PASSED** |
| 4 | `tests/test_theory.py` | `test_erlang_a_reference` | Kiểm tra nghiệm Erlang-A chuẩn ($c=6, \lambda=2.0, \theta=0.1$): $SL, W_q, p_{ab}, \rho$ | **PASSED** |
| 5 | `tests/test_theory.py` | `test_allen_cunneen_reference` | Kiểm tra công thức Allen–Cunneen cho $cs^2 = 0.25$ và $2.25$ | **PASSED** |
| 6 | `tests/test_theory.py` | `test_split_queues_worse` | Kiểm tra hàng riêng lẻ có mức phục vụ luôn kém hơn hàng chung M/M/c | **PASSED** |
| 7 | `tests/test_theory.py` | `test_sipp_schedule_monotone` | Kiểm tra lịch SIPP có số quầy tăng đơn điệu khi tốc độ đến tăng | **PASSED** |
| 8 | `tests/test_sim.py` | `test_utilization_matches_little` | Kiểm tra hiệu suất mô phỏng SimPy khớp định luật Little ($\rho = \lambda E[S]/c$) | **PASSED** |
| 9 | `tests/test_sim.py` | `test_same_seed_same_result` | Kiểm tra tính tái lập tuyệt đối của SimPy khi dùng cùng seed (CRN) | **PASSED** |
| 10 | `tests/test_sim.py` | `test_more_servers_not_worse` | Kiểm tra mô phỏng SimPy: tăng số quầy $c=7$ luôn có $SL$ cao hơn $c=5$ | **PASSED** |
| 11 | `tests/test_sim.py` | `test_mg1_pollaczek_khinchine`| Kiểm tra công thức chính xác Pollaczek–Khinchine M/G/1 ($W_q = 14.625$p) | **PASSED** |
| 12 | `tests/test_sim.py` | `test_erlang_a_utilization` | Kiểm tra hiệu suất có bỏ về: $\rho = \lambda(1-p_{ab})E[S]/c$ | **PASSED** |
| 13 | `tests/test_v2_features.py` | `test_milp_pure_4h_52` | Mô hình MILP thuần 4h yêu cầu đúng 52 quầy-giờ | **PASSED** |
| 14 | `tests/test_v2_features.py` | `test_milp_pure_8h_model_a_64` | Mô hình A thuần 8h liên tục yêu cầu 64 quầy-giờ | **PASSED** |
| 15 | `tests/test_v2_features.py` | `test_milp_pure_8h_model_b_48` | Mô hình B thuần 8h có nghỉ trưa chỉ cần 6 nhân viên (48 q-h) | **PASSED** |
| 16 | `tests/test_v2_features.py` | `test_milp_model_a_infeasible` | Mô hình A với 4 NV 8h + 3 NV 4h không có nghiệm khả thi | **PASSED** |
| 17 | `tests/test_v2_features.py` | `test_milp_model_b_unique_44` | Mô hình B với 4 NV 8h + 3 NV 4h có nghiệm duy nhất 44 q-h | **PASSED** |
| 18 | `tests/test_v2_features.py` | `test_day_variation_reduces_sla` | Biến động ngày $CV=11.8\%$ làm giảm xác suất đạt SLA mọi giờ | **PASSED** |

---

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
| **Tổng số quầy-giờ nhân sự** | **44 quầy-giờ/ngày** | **48 quầy-giờ/ngày** | **54 quầy-giờ/ngày** |
| **Hiệu quả cắt giảm chi phí** | **Tiết kiệm 18.52% (-10 q-h/ngày)** | **Tiết kiệm 11.11% (-6 q-h/ngày)** | Mốc cơ sở (0.0%) |
| **Mức phục vụ $SL$ danh định (CI95)** | **$93.81\% \pm 0.23\%$** | **$95.82\% \pm 0.18\%$** | $97.70\% \pm 0.12\%$ |
| **Mức phục vụ $SL$ giờ tệ nhất (Low CI95)** | **$90.78\%$ (Đạt mục tiêu $\ge 90\%$)**| **$93.64\%$ (Biên an toàn tốt)** | $95.57\%$ |
| **Xác suất ngày đạt SLA toàn ngày ($SL \ge 90\%$)** | **$85.0\%$ (với biến động ngày $CV=11.8\%$)** | **$95.3\%$** | $99.4\%$ |
| **Xác suất đạt SLA tất cả 9 giờ trong ngày** | **$26.0\%$** | **$47.0\%$** | $77.8\%$ |
| **Số ngày thực tế 14 ngày đạt SLA** | **10/14 ngày (hụt 4 ngày tải cao: ngày 1, 2, 7, 12)** | **13/14 ngày (chỉ hụt ngày 7 tải cực đại)** | 14/14 ngày |
| **Mức phục vụ Khách VIP ($W_q \le 2$p)** | **$94.96\% \pm 0.25\%$** | **$96.64\% \pm 0.19\%$** | $98.15\% \pm 0.14\%$ |
| **Thời gian chờ trung bình $W_q$** | **$0.4908 \pm 0.0155$ phút (~29.4 giây)** | **$0.3424 \pm 0.0120$ phút (~20.5 giây)** | $0.1958 \pm 0.0089$ phút (~11.7 giây) |
| **Tỉ lệ khách hàng bỏ về trung bình** | **$5.35\% \pm 0.17\%$** | **$3.73\% \pm 0.14\%$ (Giảm 30% khách mất)** | $2.15\% \pm 0.10\%$ |
| **Hiệu suất sử dụng quầy $\rho$** | **$72.15\% \pm 0.38\%$ (Tối ưu năng suất)**| **$67.25\% \pm 0.37\%$** | $60.75\% \pm 0.36\%$ (Lãng phí quầy) |
| **Phương án tổ chức ca làm việc** | **Mô hình B: 4 NV 8h (nghỉ trưa) + 3 NV 4h** | Mô hình B: 5 NV 8h (nghỉ trưa) + 2 NV 4h | 6 NV 8h (nghỉ trưa 1-7: 6 NV làm việc 48 q-h) |
| **Chi phí phụ trội do tổ chức ca** | **+0.0% (Phủ chính xác 44 q-h)** | +0.0% (Phủ chính xác 48 q-h) | +0.0% |
| **Độ bền khi nhu cầu tăng +10%** | Giờ đỉnh rơi xuống $86.5\%$ | **Giờ đỉnh giữ vững $\ge 90.0\%$** | Giờ đỉnh giữ vững $93.3\%$ |
| **Quy tắc kích hoạt vận hành** | Áp dụng khi lưu lượng $\le 687$ khách/ngày | Kích hoạt khi lưu lượng $> 687$ khách/ngày | Mốc lý thuyết đối chiếu |

