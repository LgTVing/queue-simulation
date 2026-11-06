# BẢNG TỔNG HỢP TOÀN BỘ TIẾN TRÌNH, SỐ LIỆU TÍNH TOÁN EXCEL VÀ KIỂM CHỨNG CODE PYTHON / SIMPY

**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu cho chi nhánh ngân hàng  
**Thời điểm tổng hợp:** Tháng 10/2026; Phần 3–5 cập nhật theo V5 ngày 2026-10-30 (`results/final_v5/`). Phần 1–2 là lịch sử 3 tuần và số liệu Excel, không phụ thuộc mô phỏng.  
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
3. [PHẦN 3: SỐ LIỆU KIỂM CHỨNG VÀ THỰC NGHIỆM BẰNG CODE (V4)](#phần-3-số-liệu-kiểm-chứng-và-thực-nghiệm-bằng-code-v4)
4. [PHẦN 4: ĐỐI CHIẾU CHÉO GIỮA EXCEL, LÝ THUYẾT VÀ MÔ PHỎNG SIMPY](#phần-4-đối-chiếu-chéo-giữa-excel-lý-thuyết-và-mô-phỏng-simpy)
5. [PHẦN 5: BẢNG QUYẾT ĐỊNH KHUYẾN NGHỊ CUỐI CÙNG](#phần-5-bảng-quyết-định-khuyến-nghị-cuối-cùng)

---

## PHẦN 1: TỔNG QUAN TIẾN TRÌNH VÀ NHỮNG VIỆC ĐÃ LÀM ĐƯỢC

### 1.1 Khái quát Tiến trình 3 Tuần
Dự án đã hoàn thành trọn vẹn lộ trình 3 tuần từ nghiên cứu thăm dò dữ liệu đến mô hình hóa lý thuyết, lập trình mô phỏng, kiểm chứng đa tầng, tối ưu hóa định biên và đóng gói sản phẩm khoa học:

| Tuần | Trọng tâm công việc | Các mốc kết quả đã đạt được | Tình trạng |
|---|---|---|:---:|
| **Tuần 1** | Khảo sát dữ liệu thực tế, làm sạch dữ liệu và ước lượng sơ bộ | - Thu thập bộ dữ liệu giao dịch 14 ngày chuẩn ($9.836$ cuộc gọi) từ Technion SEE Center.<br>- Làm sạch qua `data/lam_sach.py`, lọc khung giờ 8h-17h, nghiệp vụ PS.<br>- Ước lượng sơ bộ $\lambda_h$, $E[S] = 2.88$ phút, $cv = 1.10$, $\theta = 0.1123$.<br>- Tạo 2 file Excel ban đầu: `docs/thong_ke_mo_ta.xlsx` và `docs/bang_tham_so.xlsx`. | **Hoàn thành 100%** |
| **Tuần 2** | Mô hình hóa giải tích, xây dựng SimPy và kiểm chứng ba tầng | - Xây dựng mô hình giải tích `b_theory.py` (M/M/c, Allen-Cunneen, Erlang-A ma trận hấp thụ Markov, SIPP).<br>- Tạo file Excel tính toán tự động `excel/erlang.xlsx` (5 sheets, không lỗi `#NAME?`).<br>- Xây dựng công cụ mô phỏng SimPy `c_sim.py` (Blocker động, Priority VIP, Khách bỏ về, CRN).<br>- Kiểm chứng ba tầng (Tầng 1 M/M/c, Tầng 2 Erlang-A, Tầng 3 Allen-Cunneen).<br>- Khảo sát khởi động Welch (`fig_c_welch.png`) và lợi ích gộp hàng (`fig_c_pooling.png`). | **Hoàn thành 100%** |
| **Tuần 3** | Sửa tồn đọng, tối ưu hóa lịch quầy, thí nghiệm mở rộng, đóng băng số liệu, viết báo cáo & slide | - Sửa triệt để lỗi hiệu suất $\rho$ (đạt $0.7517 \pm 0.0047$ khớp định luật Little).<br>- Bổ sung Kiểm tra A (M/G/1 Pollaczek-Khinchine exact $14.625$p) và Kiểm tra B (M/G/6 60 reps).<br>- Tối ưu hóa lịch quầy 2 pha hội tụ tại lịch `[4, 5, 6, 5, 5, 5, 5, 5, 4]` (44 quầy-giờ).<br>- Đánh giá 5 chính sách với 300 lần lặp độc lập (`seed_base=50000`).<br>- Phân tích độ nhạy T6, hàm chi phí kịch bản $k$, bài toán ca làm việc MILP, độ bất định 50 bộ bootstrap, kiểm tra ngoài mẫu trên 4 ngày test.<br>- Đóng băng số liệu tại `results/final_v1/` gồm 10 bảng CSV/MD và 8 biểu đồ đồ họa.<br>- Hoàn tất báo cáo tổng kết (`docs/bao_cao_tong_ket.md`) và slide thuyết trình (`docs/slide_thuyet_trinh.md`). | **Hoàn thành 100%** |
| **V4 (2026-10-29)** | Sửa động cơ mô phỏng, hợp nhất pipeline, củng cố mô hình, đóng băng lại | - F1–F3: xả hàng giữ số quầy giờ cuối, NHPP đúng ranh giới giờ, hiệu suất theo thời gian bận.<br>- M1–M5: kịch bản kiên nhẫn, ràng buộc bỏ về, phục vụ thực nghiệm làm mô hình chính, điều tra 15h–16h, ổn định giờ tệ nhất.<br>- Một lệnh `python main.py --stage all` (33.3 phút) sinh `results/final_v4/`; lịch tối ưu đổi thành `[4, 5, 6, 5, 5, 5, 5, 5, 5]` (45 quầy-giờ).<br>- 35/35 test pass; `tools/check_consistency.py` đối chiếu 1.052 giá trị trong `tong_hop.md`. | **Hoàn thành** |
| **V5 (2026-10-30)** | Chạy song song, tối ưu theo giờ công, xác suất đạt SLA ngày, tăng quầy theo hàng chờ | - P1–P2: chạy song song các lần lặp, `rep_stats` bằng NumPy; pipeline 33.3 → 15.1 phút (gồm M6–M8, S12–S15), số V4 giữ nguyên từng byte.<br>- M6: tối thiểu **48 giờ công**, 4 ca 8h + 4 ca 4h theo Lịch 48 `[4, 6, 6, 6, 5, 5, 6, 5, 5]`.<br>- M7: đạt SLA ở ≥ 90% số ngày cần 48 giờ công, ≥ 95% cần 52.<br>- M8: Lịch 45 + mở thêm 1 quầy khi > 2 người chờ liên tục 5 phút (TB 46.17 quầy-giờ mở, 97.3% số ngày đạt SLA).<br>- T2–T3: checker đối chiếu cả báo cáo, slide, README; CI GitHub Actions.<br>- S12–S15: kiên nhẫn Weibull, dự báo sớm fit trên train, cluster bootstrap, λ nửa giờ; không đổi kết luận 48 giờ công. 84 test pass. | **Hoàn thành** |
| **V5.1 (2026-11-02)** | Sửa sau rà soát mã: seed đánh giá độc lập, định nghĩa SLA, tái lập dữ liệu | - F4–F5: sổ đăng ký seed `common.SEED_BANDS`; M7 xác nhận bằng 2.000 lần lặp seed độc lập (Lịch 48: 94.6% số ngày đạt SLA).<br>- F6, M9: SLA chính tính trên mọi khách; riêng khách thường Lịch 45 hụt 11h–12h, tối ưu theo khách thường cần 47 quầy-giờ, vẫn 48 giờ công.<br>- F9, S16: seed riêng cho bootstrap S5; p-value S6 từ phân phối mô phỏng (sau Holm không giờ nào khác biệt có ý nghĩa).<br>- F7–F8: `lam_sach.py` tái lập được; dữ liệu thô không còn trong repo. O1–O2: bộ nhớ đệm `run_reps`, smoke test 84 giây. D5: `docs/demo/sipp.html`. 115 test (114 pass, 1 xfail). | **Hoàn thành** |

### 1.2 Phân công Trách nhiệm và Sản phẩm Bàn giao Cụ thể
- **Thành viên A (Nguyễn Văn A - Dữ liệu & Thống kê):**
  - Quản lý tệp dữ liệu sạch `data/clean/data_clean.csv` ($9.836$ bản ghi).
  - Ước lượng các tham số $\lambda_h$, $E[S]$, $\theta$, $p_{vip}$ trên tập Train 10 ngày ($6.867$ bản ghi) và xuất `docs/params.json` (hiện là bản v4.0, trùng `results/final_v5/params.json`; tham số không đổi ở V5).
  - Kiểm định phân phối Poisson theo giờ và so sánh AIC thời gian phục vụ (Gamma tốt nhất).
  - Thực hiện Thí nghiệm E4 (Độ bất định tham số 50 bộ bootstrap) $\implies$ [`fig_a_bat_dinh.png`](../results/archive/final_v1/hinh/fig_a_bat_dinh.png).
  - Thực hiện Thí nghiệm E5 (Độ nhạy phân phối phục vụ) và E6 (Kiểm tra ngoài mẫu trên tập Test 4 ngày) $\implies$ [`fig_a_ngoai_mau.png`](../results/archive/final_v1/hinh/fig_a_ngoai_mau.png).
  - Soạn thảo Mục 3, Mục 4 trong Báo cáo tổng kết và Slide 3, 4, 5.
- **Thành viên B (Trần Thị B - Lý thuyết, Chi phí & Vận hành):**
  - Xây dựng mô hình giải tích `b_theory.py` và bảng tính tự động `excel/erlang.xlsx`.
  - Phân tích bảng quyết định định biên SIPP Erlang C (47 q-h) và Erlang-A (44 q-h).
  - Xây dựng hàm chi phí kinh tế $C(k) = \text{quầy-giờ} + k \cdot N_{ab}$ với $k \in \{0.1, 0.25, 0.5, 1.0, 2.0\}$ và vẽ đường đánh đổi Pareto $\implies$ [`fig_b_chi_phi.png`](../results/archive/final_v1/hinh/fig_b_chi_phi.png).
  - Thiết lập và giải bài toán Quy hoạch Tuyến tính Nguyên MILP (`scipy.optimize.milp`) lập lịch theo ca làm việc (ca 4h, ca 8h, ca hỗn hợp) $\implies$ [`fig_b_ca_lam.png`](../results/archive/final_v1/hinh/fig_b_ca_lam.png).
  - Phân tích lịch bền vững theo quy tắc căn bậc hai $c \approx a + \beta \sqrt{a}$.
  - Soạn thảo Mục 5, Mục 6 trong Báo cáo tổng kết và Slide 6, 7, 8, 9.
- **Thành viên C (Lê Văn C - Mô phỏng, Tối ưu & Tổng hợp):**
  - Xây dựng động cơ mô phỏng sự kiện rời rạc SimPy `c_sim.py` với blocker động và đồng bộ hóa CRN.
  - Thực hiện kiểm chứng 3 tầng, sửa lỗi hiệu suất $\rho$, thực hiện Kiểm tra A (M/G/1 exact) và Kiểm tra B.
  - Lập trình thuật toán tối ưu hóa 2 pha (*Ramp-up* & *Pruning*).
  - Đánh giá 5 chính sách phục vụ với 300 lần lặp độc lập và phân tích độ nhạy T6 $\implies$ [`fig_c_do_nhay.png`](../results/archive/final_v1/hinh/fig_c_do_nhay.png).
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

| Khung giờ | Hour ID | Số khách TB $\bar{N}_h$ (khách/ngày) | Tốc độ đến $\lambda_h$ (khách/phút) | CI95 Poisson Low | CI95 Poisson High | Chỉ số phân tán $D$ | $p$-value Poisson | Kết luận Poisson ($\alpha=0.05$) | Tỉ lệ bỏ về $p_{ab}$ | Tỉ lệ khách VIP | $E[S]$ theo giờ (phút) | $\text{std}[S]$ theo giờ (phút) |
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
>
> Cột CI95 trong Excel là khoảng Poisson $\hat\lambda \pm 1.96\sqrt{\bar N/14}/60$. Vì số khách quá phân tán, khoảng này hẹp hơn thực tế 1.4–2.1 lần; khoảng Student-t ($df = 13$) nằm ở `tong_hop.md` mục 2.2.
> Kết quả: Có tới **8/9 khung giờ bị bác bỏ Poisson ở mức ý nghĩa 5%** (5/9 giờ bị bác bỏ mạnh ở mức 1%). Chỉ duy nhất khung giờ 12h–13h ($p = 0.0763$) là chưa bác bỏ. Giả định dòng khách đến tuân theo tiến trình Poisson thuần túy với $\lambda_h$ cố định không phản ánh đầy đủ thực tế.

#### Thống kê Quá Phân Tán Lưu Lượng Khách theo Ngày (`qua_phan_tan_ngay.csv`)
- **Số ngày quan sát:** 14 ngày làm việc tiêu chuẩn.
- **Tổng khách trung bình mỗi ngày ($\mu$):** $702.6$ khách/ngày.
- **Phương sai thực tế ($\sigma^2$):** $7.586,7 \implies$ Độ lệch chuẩn thực tế $\sigma = 87.1$ khách.
- **Độ lệch chuẩn phân phối Poisson thuần ($\sqrt{\mu}$):** $26.5$ khách.
- **Tỉ số Phương sai / Trung bình ($\text{Var}/\text{Mean}$):** $10.8 \gg 1$ (Dữ liệu bị quá phân tán mạnh so với Poisson).
- **Hệ số biến thiên thực tế ($CV_{\text{ngày}}$):** $12.4\%$.
- **Ước lượng $CV_{\text{ngày}}$ sau khi loại trừ nhiễu Poisson:**
  $$CV_{\text{ngày}}^2 = \frac{\text{Var}(N_d) - \mu}{\mu^2} = \frac{7586.7 - 702.6}{702.6^2} = 0.0139 \implies CV_{\text{ngày}} = 11.8\%.$$
- **Kiểm định quá phân tán:** $D = 140.4$ ($df=13$), $p\text{-value} = 1.77 \times 10^{-23}$ $\implies$ Bác bỏ mạnh giả định Poisson thuần cho tổng ngày.

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

Tệp gồm 3 sheets: `theo_gio`, `chung` và `qua_phan_tan` (các chỉ số quá phân tán đã nêu ở mục 2.1).

#### Sheet 1: `theo_gio` (10 hàng $\times$ 6 cột)
Tham số dòng khách đến theo 9 khung giờ:

| Khung giờ | $\bar{N}_h$ (khách/ngày) | $\lambda_h$ (khách/phút) | CI95 Poisson Low | CI95 Poisson High | $p$-value Poisson |
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

*(Lưu ý: sheet này tính trên 14 ngày. Bộ tham số mô hình v4.0 (`docs/params.json`) ước lượng trên tập Train 10 ngày: $E[S] = 2.9236$, $cv = 1.0963$, $cs^2 = 1.2018$, $\theta = 0.1087$, $p_{vip} = 0.3543$).*

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

#### Sheet 5: `Quyet_dinh` (Định biên SIPP Erlang C và Erlang-A, 9 khung giờ)
Tham số tập train (10 ngày): $E[S] = 2.9236$ phút, $\theta = 0.1087$/phút; SLA: $P(\text{phục vụ và chờ} \le 5\text{p}) \ge 90\%$. Số liệu trùng `results/final_v5/bang_sipp.csv`:

| Khung giờ | $\lambda_h$ train | Quầy Erlang C | SL Erlang C | Quầy Erlang-A | SL Erlang-A | $p_{ab}$ Erlang-A | $\rho$ Erlang-A |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h - 9h** | 0.9900 | **4** | 92.97% | **4** | 93.63% | 5.77% | 68.19% |
| **9h - 10h** | 1.3767 | **6** | 99.01% | **5** | 93.07% | 6.43% | 75.32% |
| **10h - 11h (Đỉnh)** | 1.5350 | **6** | 96.85% | **6** | 95.78% | 4.09% | 71.74% |
| **11h - 12h** | 1.3900 | **6** | 98.90% | **5** | 92.83% | 6.64% | 75.88% |
| **12h - 13h** | 1.2400 | **5** | 96.01% | **5** | 95.23% | 4.52% | 69.23% |
| **13h - 14h** | 1.2017 | **5** | 96.99% | **5** | 95.74% | 4.05% | 67.42% |
| **14h - 15h** | 1.3383 | **5** | 91.89% | **5** | 93.73% | 5.85% | 73.67% |
| **15h - 16h** | 1.3167 | **5** | 93.04% | **5** | 94.09% | 5.54% | 72.73% |
| **16h - 17h** | 1.0567 | **5** | 99.01% | **4** | 92.19% | 6.98% | 71.84% |
| **TỔNG QUẦY-GIỜ** | | **47** | | **44** | | | |

*Lưu ý:* `excel/erlang.xlsx` do `excel/tao_erlang_excel.py` sinh bằng openpyxl nên các ô công thức chưa có giá trị lưu sẵn; cần mở bằng Excel/LibreOffice (tự tính lại) để thấy số.

---

## PHẦN 3: SỐ LIỆU KIỂM CHỨNG VÀ THỰC NGHIỆM BẰNG CODE (V5)

Toàn bộ số liệu mô phỏng được sinh bằng một lệnh `python main.py --stage all` và đóng băng tại `results/final_v5/` (danh mục tệp và nguồn của từng tệp: `results/final_v5/MO_TA.md`). V5 giữ nguyên mọi số của V4 và thêm M6–M8. Bảng số chi tiết **chỉ được duy trì ở một nơi** là [`tong_hop.md`](../tong_hop.md), và được `tools/check_consistency.py` đối chiếu tự động với CSV (1.502 giá trị, 0 lệch tại ngày 2026-10-30). Phần này chỉ tóm tắt và trỏ tới mục tương ứng.

| Nội dung | Kết quả chính | Tệp nguồn | Mục trong `tong_hop.md` |
|---|---|---|:---:|
| Kiểm chứng ba tầng + M/G/1 P-K exact | Tầng 1–2 khớp lý thuyết; Kiểm tra A: $W_q$ 14.2179 so với 14.625 (CI95 [13.59, 14.85]) | `kiem_chung.csv` | 3.1 |
| Tối ưu 2 pha SimPy | Khởi tạo Erlang-A 44 q-h vi phạm ở 16h–17h; thêm 1 quầy → **45 q-h** `[4, 5, 6, 5, 5, 5, 5, 5, 5]`; 9 phép bớt đều vi phạm | `lich_toi_uu.csv` | 3.2 |
| Bootstrap lồng nhau (S5) | 94.2% phương sai do bất định tham số; $P(SL_{\text{giờ tệ nhất}} \ge 90\%) = 86\%$ | `phan_ra_phuong_sai.csv` | 3.3 |
| So sánh 6 chính sách (300 lần lặp) | Lịch 45: SL 0.9423 ± 0.0022, giờ tệ nhất cận dưới 0.9236, bỏ về 4.99% | `so_sanh_chinh_sach.csv` | 4.1 |
| Chỉ số kỳ vọng có điều kiện, CV ngày (S2, S3) | $P(E_{\text{day}} \ge 90\%)$: 88.0% / 96.0% / 99.5% (Lịch 45 / 48 / Mốc 54) | `chi_so_ky_vong_dieu_kien.csv`, `do_nhay_cv_ngay.csv` | 4.2 |
| Ngưỡng lưu lượng và dự báo sớm (S4) | $V^* = 803$ khách/ngày; chính sách ghép dùng TB 45.21 q-h | `nguong_luu_luong_chi_tiet.csv`, `du_bao_som_hoi_quy.csv` | 4.4 |
| 14 ngày thực tế (S7) | Lịch 45: 12/14 ngày; Lịch 48 và Mốc 54: 14/14 | `theo_14_ngay.csv` | 4.5 |
| Ngoài mẫu (S6) + điều tra 15h–16h (M4) | 7/9 giờ trong PI95; 15h–16h lệch do riêng ngày 10 | `ngoai_mau.csv`, `dieu_tra_15h_16h.csv` | 5 |
| Ca làm việc MILP | Lịch 45 không phủ đúng được; 5 ca 8h + 2 ca 4h = 48 q-h công | `lich_theo_ca.csv` | 6 |
| Độ nhạy nhu cầu, $E[S]$, $\theta$ | Lịch 45 không chịu được +10% nhu cầu (cận dưới 0.8793) | `do_nhay.csv` | 7.1 |
| Độ nhạy phân phối phục vụ (S9, M3) | Gamma và Exponential không khác thực nghiệm có ý nghĩa; Lognormal cv+20% thấp hơn 0.0091 | `do_nhay_phan_phoi.csv`, `m3_dich_vu_thuc_nghiem.csv` | 7.2 |
| Chi phí (S11) | Lịch 45 rẻ nhất khi $k < 0.33$; Mốc 54 rẻ nhất khi $k > 0.58$ | `chi_phi.csv` | 7.3 |
| Pha 3 vét cạn (C6) | 0/117 cấu hình lân cận khả thi (mô phỏng SimPy) | `pha3.csv` | 7.4 |
| Kiên nhẫn (M1) | 46 q-h cho kiên nhẫn 15–60 phút; 48 q-h khi không bỏ về | `do_nhay_kien_nhan.csv` | 7.5 |
| Ràng buộc bỏ về (M2) | $p_{ab} \le 5\%$: 46 q-h; $\le 3\%$: 51 q-h; $\le 2\%$: 55 q-h | `toi_uu_rang_buoc_bo_ve.csv` | 7.6 |
| Giờ tệ nhất và số lần lặp (M5) | Lịch 45: 11h–12h là giờ tệ nhất với xác suất 99.7% (R = 1.646) | `gio_te_nhat.csv`, `so_lan_lap_can_thiet.csv` | 7.7 |
| Tối ưu theo giờ công ca (M6) | 44 giờ công: không khả thi; 48 giờ công: 33/94 lịch khả thi, tốt nhất Lịch 48 (4 ca 8h + 4 ca 4h) | `toi_uu_theo_ca.csv`, `toi_uu_theo_ca_top.csv` | 7.9 |
| Xác suất đạt SLA ngày (M7) | ≥ 90% số ngày: 48 giờ công; ≥ 95%: 52 giờ công | `toi_uu_xac_suat_ngay.csv` | 7.10 |
| Tăng quầy theo hàng chờ (M8) | Lịch 45 + mở thêm khi > 2 người chờ 5 phút: 46.17 quầy-giờ TB, $P(SL_{\text{ngày}} \ge 90\%)$ 97.3% (Lịch 48: 94.0%) | `chinh_sach_tang_quay.csv` | 7.11 |
| Kiên nhẫn Weibull (S12) | $k = 0.855$, AIC thấp hơn mũ 18.7; lịch tối ưu vẫn 45 quầy-giờ | `kien_nhan_weibull*.csv` | 7.12 |
| λ theo nửa giờ (S15) | Chỉ 8h–9h khác rõ giữa hai nửa giờ; tổng quầy-giờ tối ưu vẫn 45 | `lambda_nua_gio.csv`, `khung_30_phut.csv` | 7.13 |
| Dự báo sớm fit trên train (S13) | RMSE ngoài mẫu 63.9 khách; vẫn bỏ lỡ 2/2 ngày hụt | `du_bao_som_hoi_quy.csv` | 4.4 |
| Cluster bootstrap (S14) | P(thực tế mọi giờ) Lịch 45: [25.4%, 32.3%], rộng gấp khoảng 3 lần Wilson | `chi_so_ky_vong_dieu_kien.csv` | 4.2 |
| Đối chiếu V4 → V5 | 17 chỉ số V4 không đổi; giờ công tối thiểu 48 (M6) | `doi_chieu_v4_v5.csv` | 8 |
| Kiểm thử tự động | 84 test pass trong 557 giây (9.3 phút, gồm smoke test toàn pipeline) | `pytest_log.txt` | 9 |

---

## PHẦN 4: ĐỐI CHIẾU CHÉO GIỮA EXCEL, LÝ THUYẾT VÀ MÔ PHỎNG SIMPY

Bảng đối chiếu số quầy theo từng giờ giữa các phương pháp (Excel và lý thuyết: `bang_sipp.csv`; SimPy: `lich_khuyen_nghi.json`):

| Khung giờ | Excel / Erlang C (SIPP) | Lý thuyết Erlang-A (SIPP) | SimPy Tối ưu quầy-giờ | SimPy Lịch 48 (tối ưu giờ công, M6) | Mốc cơ sở: Hằng số 6 quầy |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h - 9h** | 4 | **4** | **4** | 4 | 6 |
| **9h - 10h** | 6 | **5** | **5** | 6 | 6 |
| **10h - 11h (Đỉnh)** | 6 | **6** | **6** | 6 | 6 |
| **11h - 12h** | 6 | **5** | **5** | 6 | 6 |
| **12h - 13h** | 5 | **5** | **5** | 5 | 6 |
| **13h - 14h** | 5 | **5** | **5** | 5 | 6 |
| **14h - 15h** | 5 | **5** | **5** | 6 | 6 |
| **15h - 16h** | 5 | **5** | **5** | 5 | 6 |
| **16h - 17h** | 5 | **4** | **5** | 5 | 6 |
| **TỔNG QUẦY-GIỜ** | **47 quầy-giờ** | **44 quầy-giờ** | **45 quầy-giờ** | **48 quầy-giờ** | **54 quầy-giờ** |
| **Tỉ lệ tiết kiệm so với 54** | -12.96% | -18.52% | **-16.67%** | -11.11% | Gốc mốc |

Cột Excel/Erlang C và Erlang-A dùng cùng tham số train ($E[S] = 2.9236$, $\theta = 0.1087$), trùng Sheet 5 mục 2.3 và `bang_sipp.csv`.

### Giải thích chênh lệch

1. **Vì sao Erlang C cần 47 quầy-giờ còn Erlang-A chỉ cần 44?**  
   Erlang C giả định khách kiên nhẫn vô hạn ($\theta = 0$). Ở 9h–10h, 11h–12h và 16h–17h, muốn đưa thời gian chờ dưới 5 phút thì Erlang C phải thêm 1 quầy mỗi giờ. Dữ liệu cho $\theta = 0.1087\text{ phút}^{-1}$ (kiên nhẫn TB 9.2 phút): một phần khách bỏ về làm giảm tải, nên Erlang-A đạt SLA với 5 quầy ở các giờ đó. Cái giá là khoảng 5% khách bỏ về (`tong_hop.md` mục 7.6).
2. **Vì sao SimPy V4 cần 45 quầy-giờ, nhiều hơn Erlang-A 1 quầy ở 16h–17h?**  
   Erlang-A giả định thời gian phục vụ mũ ($cs^2 = 1$) và hệ dừng trong từng giờ. Mô phỏng V4 dùng phân phối phục vụ thực nghiệm ($cs^2 = 1.20$) và tiêu chí cận dưới CI95 của SL mỗi giờ. Với 4 quầy, giờ 16h–17h có cận dưới 0.8893 (60 lần lặp, seed chọn lịch) nên bị loại. Tối ưu cùng pipeline nhưng phục vụ Gamma ($cs^2 = 0.91$) vẫn cho lịch 44 của V3; vậy chênh lệch đến từ độ biến động thời gian phục vụ.
3. **Lịch 45 là tối thiểu cục bộ:** 9 phép bớt 1 quầy (pha 2) và 117 phép hoán đổi/giảm 2 quầy (pha 3) đều vi phạm tiêu chí mô phỏng.
4. **Vì sao khuyến nghị là Lịch 48 dù Lịch 45 mở ít quầy hơn?**  
   Với ca 8h (nghỉ trưa 11h–14h) và ca 4h, Lịch 45 không phủ đúng được nên vẫn tốn 48 giờ công. Tối ưu thẳng theo giờ công (M6) cho thấy 48 là mức nhỏ nhất và Lịch 48 là cách xếp tốt nhất ở mức đó (`tong_hop.md` mục 7.9).

---

## PHẦN 5: BẢNG QUYẾT ĐỊNH KHUYẾN NGHỊ CUỐI CÙNG

Bảng quyết định đầy đủ (lịch, SL, giờ tệ nhất, các xác suất Wilson, $W_q$, bỏ về, ca làm việc, quy tắc kích hoạt) nằm ở [`tong_hop.md` mục 1](../tong_hop.md#1-bảng-quyết-định-quản-trị-tổng-thể). Tóm tắt:

| Phương án | Lịch theo giờ | Quầy-giờ mở | $SL$ ngày | Giờ tệ nhất (cận dưới CI95) | Bỏ về | Giờ công ca (nghỉ trưa 11h–14h) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Khuyến nghị: Lịch 48 (ít giờ công nhất, M6)** | `[4, 6, 6, 6, 5, 5, 6, 5, 5]` | **48** | 95.79% | 93.27% | 3.70% | **48 (4 ca 8h + 4 ca 4h)** |
| **Ít quầy-giờ mở nhất: Lịch 45** | `[4, 5, 6, 5, 5, 5, 5, 5, 5]` | **45** | 94.23% | 92.36% | 4.99% | 48 (5 ca 8h + 2 ca 4h) |
| **Mốc cơ sở 6 quầy** | `[6, 6, 6, 6, 6, 6, 6, 6, 6]` | 54 | 97.63% | 94.94% | 2.17% | 56 (6 ca 8h + 2 ca 4h) |

Bổ sung V5: nếu có 1 nhân viên dự phòng, Lịch 45 + mở thêm 1 quầy khi hơn 2 người chờ liên tục 5 phút cho trung bình 46.17 quầy-giờ mở và đạt SLA ở 97.3% số ngày (M8); muốn đạt SLA ở ≥ 95% số ngày cần 52 giờ công (M7).
