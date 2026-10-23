# NHẬT KÝ THAY ĐỔI VÀ HIỆU CHỈNH KHOA HỌC (CHANGELOG v1 -> v2)

Tài liệu này ghi nhận chi tiết toàn bộ các thay đổi giữa kết quả ban đầu (`results/final_v1/`) và kết quả chuẩn hóa khoa học (`results/final_v2/`) theo 14 nhiệm vụ kỹ thuật được chỉ định trong `YEU_CAU_CHINH_SUA_AGENT.md`.

---

## TỔNG HỢP THEO 14 NHIỆM VỤ (T1 - T14)

### T1 (P0): Sửa nhãn kiểm định Poisson & Bổ sung phân tích quá phân tán (Overdispersion)
- **Số liệu trước (v1):** Báo cáo ghi: "8/9 khung giờ chấp nhận giả định Poisson cục bộ ($p > 0.05$)".
- **Số liệu sau (v2):** 
  - Thống kê chỉ số phân tán chuẩn: $(n-1)D \sim \chi^2_{13}$.
  - Kết quả kiểm định: **8/9 khung giờ bác bỏ giả thuyết Poisson** ở mức ý nghĩa $\alpha = 0.05$ (5/9 giờ bác bỏ ở $\alpha = 0.01$). Duy nhất khung 12h - 13h ($D = 20.83, p = 0.0763$) chưa đủ bằng chứng bác bỏ.
  - Phân tích quá phân tán toàn ngày: Số khách/ngày có Mean = 702.6, SD thực tế = 87.1 trong khi SD Poisson lý thuyết chỉ là $\sqrt{702.6} = 26.5$. Tỉ số $\text{Var}/\text{Mean} = 10.8 \gg 1$.
  - Hệ số biến thiên quy mô ngày: $CV_{\text{thô}} = 12.4\%$; sau khi trừ nhiễu Poisson thuần túy $\sqrt{Var - Mean}/Mean = 11.8\%$.
- **Lý do sửa:** Khắc phục lỗi đảo nhãn logic trong script v1; thừa nhận và lượng hóa tính chất quá phân tán (overdispersion) của dòng khách thực tế.
- **Tệp cập nhật:** `docs/thong_ke_mo_ta.xlsx` (bảng kiem_dinh_poisson), `docs/bang_tham_so.xlsx` (sheet qua_phan_tan), `results/final_v2/kiem_dinh_poisson.csv`, `results/final_v2/qua_phan_tan_ngay.csv`.

---

### T2 (P0): Tích hợp biến động lưu lượng giữa các ngày ($m_d$) vào mô phỏng
- **Số liệu trước (v1):** Mô phỏng giả định các ngày hoàn toàn đồng nhất. Lịch tối ưu 44 quầy-giờ đạt $100\%$ các ngày $\ge 90\%$, SLA toàn ngày $93.81\% \pm 0.23\%$.
- **Số liệu sau (v2):**
  - Đưa hệ số nhân ngày $m_d \sim \text{Gamma}(\text{mean}=1, CV=11.8\%)$ vào `c_sim.py`.
  - Lịch tối ưu 44 q-h: Xác suất ngày đạt SLA ($SL_{\text{ngày}} \ge 90\%$) giảm xuống **$85.0\%$** (300 ngày mô phỏng). Xác suất đồng thời cả 9 giờ đạt SLA chỉ còn **$26.0\%$**. Trên 14 ngày thực tế, lịch 44 đạt 10/14 ngày (hụt tại các ngày 1, 2, 7, 12 có lưu lượng cao).
  - Lịch bền vững 48 q-h: Đạt SLA ngày trên **$95.3\%$** số ngày (cả 9 giờ đạt **$47.0\%$**). Trên 14 ngày thực tế, lịch 48 đạt 13/14 ngày (chỉ hụt ngày 7 có tải cực đại 820 khách).
  - Mốc cơ sở 6 quầy: Đạt SLA ngày $99.4\%$, cả 9 giờ đạt $77.8\%$ (14/14 ngày thực tế).
- **Lý do sửa:** Mô hình hóa rủi ro thực tế khi lưu lượng biến động ngẫu nhiên theo ngày; hình thành quy tắc vận hành linh hoạt hai cấp độ.
- **Tệp cập nhật:** `c_sim.py`, `results/final_v2/bien_dong_ngay.csv`, `results/final_v2/so_sanh_chinh_sach_v2.csv`, `results/final_v2/theo_ngay.csv`, `results/final_v2/nguong_luu_luong.csv`.

---

### T3 (P0): Khắc phục triệt để mâu thuẫn số liệu giữa các phần
- **Số liệu trước (v1):** Bảng Phần 5 của báo cáo có độ lệch nhỏ ở một số chỉ số VIP và Wq so với bảng chi tiết Phần 3 và file CSV.
- **Số liệu sau (v2):** Đồng bộ hóa 100% số liệu:
  - Lịch 44: $SL = 93.81\% \pm 0.23\%$, $SL_{\text{low 95\%}} = 90.78\%$, $SL_{\text{vip}} = 94.96\% \pm 0.25\%$, $W_q = 0.4908 \pm 0.0155$p, $p_{ab} = 5.35\% \pm 0.17\%$, $\rho = 72.15\% \pm 0.38\%$.
  - Lịch 48: $SL = 95.82\% \pm 0.18\%$, $SL_{\text{low 95\%}} = 93.64\%$, $SL_{\text{vip}} = 96.64\% \pm 0.19\%$, $W_q = 0.3424 \pm 0.0120$p, $p_{ab} = 3.73\% \pm 0.14\%$, $\rho = 67.25\% \pm 0.37\%$.
- **Lý do sửa:** Đảm bảo tính trung thực khoa học tuyệt đối, mọi con số đều trích xuất trực tiếp từ các file kết quả đóng băng.
- **Tệp cập nhật:** `docs/TONG_HOP_SO_LIEU_CHI_TIET.md`, `docs/bao_cao_tong_ket.md`, `docs/slide_thuyet_trinh.md`.

---

### T4 (P0): Hoàn thiện đối chiếu ngoài mẫu (Out-of-sample)
- **Số liệu trước (v1):** Đánh giá ngoài mẫu so sánh trực tiếp mô phỏng với quan sát thực tế tập test 4 ngày mà không nêu rõ điều kiện biên nhân sự; không giải thích nguyên nhân giờ 15h-16h thực tế sụt giảm còn $76.47\%$.
- **Số liệu sau (v2):**
  - Xây dựng 2 phiên bản độc lập:
    - *Phiên bản A (Erlang-A trạng thái dừng với $\lambda_{\text{test}}$):* SLA toàn ngày đạt $92.73\%$, các giờ dao động từ $88.9\%$ đến $95.3\%$.
    - *Phiên bản B (SimPy DES với $\lambda_{\text{test}}$, 200 lần lặp):* SLA toàn ngày đạt $90.62\%$, bỏ về $7.65\%$, $W_q = 0.697$ phút.
  - Bổ sung tài liệu tham số đầy đủ tại `results/final_v2/ngoai_mau_tham_so.json`.
  - Thuyết minh nguyên nhân giờ 15h-16h: Thực tế ngân hàng chịu ảnh hưởng của các tác vụ chốt sổ cuối ngày hoặc số quầy thực tế bị rút giảm, không tương thích với điều kiện giả định 5 quầy lý tưởng của mô hình.
- **Lý do sửa:** Tránh ngụy biện phương pháp luận khi so sánh 2 điều kiện vận hành không tương đương.
- **Tệp cập nhật:** `docs/ngoai_mau.md`, `results/final_v2/ngoai_mau_v2.csv`, `results/final_v2/ngoai_mau_tham_so.json`.

---

### T5 (P0): Tách bạch và giải đúng Mô hình MILP Lập lịch theo Ca
- **Số liệu trước (v1):** Không phân định rõ ràng giữa ca làm việc liên tục 8 tiếng và ca 8 tiếng có nghỉ trưa; khẳng định chưa chính xác rằng ca 8h liên tục kết hợp ca 4h phủ được 44 quầy-giờ.
- **Số liệu sau (v2):** Xây dựng module `b_shifts.py` chuẩn hóa 2 mô hình toán:
  - *Mô hình A (Ca 8h liên tục không nghỉ):*
    - Thuần 8h: Cần 8 nhân viên $\implies$ **64 quầy-giờ** làm việc (`[4, 8, 8, 8, 8, 8, 8, 8, 4]`).
    - Cấu hình 4 NV 8h + 3 NV 4h: **Vô nghiệm (Infeasible)** do không thể hạ quầy xuống 5 ở giữa ngày.
  - *Mô hình B (Ca 8h có nghỉ trưa: 9h tại chỗ, 8h làm việc, 1h nghỉ):*
    - Thuần 8h (cửa sổ nghỉ 1-7): Cần 6 nhân viên $\implies$ **48 quầy-giờ làm việc** (54 quầy-giờ tại chỗ), tạo lịch quầy `[6, 5, 6, 5, 5, 5, 5, 5, 6]`.
    - Thuần 4h: Cần 13 lượt ca $\implies$ **52 quầy-giờ** (`[4, 5, 6, 6, 5, 8, 7, 7, 4]`).
    - Cấu hình hỗn hợp (4 NV 8h + 3 NV 4h, cửa sổ nghỉ trưa 11h-14h): Solver HiGHS xác nhận **duy nhất 1 nghiệm tối ưu khả thi** với đúng **44 quầy-giờ làm việc** (48 quầy-giờ tại chỗ), phủ chính xác `[4, 5, 6, 5, 5, 5, 5, 5, 4]`.
    - Phủ hằng số 6 quầy Mô hình B cần $\ge 7$ nhân viên.
- **Lý do sửa:** Phù hợp chặt chẽ với Bộ luật Lao động và tính khả thi trong thực tế quản trị nhân sự.
- **Tệp cập nhật:** `b_shifts.py`, `results/final_v2/lich_theo_ca_v2.csv`.

---

### T6 (P1): Giải thích độ lệch mô phỏng nhỏ giữa các khối seed
- **Số liệu trước (v1):** Báo cáo ghi nhận các con số SLA có dao động nhỏ (~0.4 - 0.5%) giữa các lần chạy mà chưa có phân tích giải trình.
- **Số liệu sau (v2):**
  - Chạy khảo sát 3 khối hạt giống độc lập (300 reps mỗi khối):
    - Block 1 (seed 50000): $SL = 93.81\% \pm 0.23\%$
    - Block 2 (seed 70000): $SL = 93.38\% \pm 0.24\%$
    - Block 3 (seed 90000): $SL = 93.65\% \pm 0.23\%$
  - Tổng hợp 900 reps: $SL = 93.61\% \pm 0.14\%$. Chênh lệch giữa các block $\le 0.43\%$, hoàn toàn nằm gọn trong khoảng tin cậy Monte Carlo $CI95$.
- **Lý do sửa:** Minh bạch hóa sai số ngẫu nhiên mô phỏng và khẳng định tính vững chắc của kết quả.
- **Tệp cập nhật:** `docs/doi_chieu_mo_phong.md`, `results/final_v2/dao_dong_seed.csv`.

---

### T7 (P1): Chuẩn hóa thuật ngữ tối ưu hóa (Bỏ chữ "Toàn cục")
- **Trước (v1):** Dùng thuật ngữ "tối ưu toàn cục" cho lịch 44 quầy-giờ.
- **Sau (v2):** Chuyển sang định danh chính xác: **"Tối thiểu cục bộ (thuật toán 2 pha xác nhận SIPP)"**.
  - Kiểm chứng vét cạn: Kiểm tra toàn bộ 9 phương án giảm 1 quầy, 72 phương án hoán đổi 1 quầy (swap), và 36 phương án giảm 2 quầy. Không tồn tại bất kỳ cấu hình nào $\le 43$ quầy-giờ hoặc cấu hình 44 quầy-giờ khác đạt điều kiện $SL_{\text{low 95\%}} \ge 0.90$ trên cả 9 giờ.
- **Lý do sửa:** Chính xác hóa thuật ngữ toán học trong tối ưu hóa tổ hợp ngẫu nhiên.
- **Tệp cập nhật:** `c_sim.py`, `docs/TONG_HOP_SO_LIEU_CHI_TIET.md`, `docs/bao_cao_tong_ket.md`, `docs/slide_thuyet_trinh.md`.

---

### T8 (P1): Kiểm tra độ nhạy phân phối phục vụ bằng CRN bắt cặp
- **Trước (v1):** So sánh phân phối phục vụ (Gamma, Weibull, Mũ, Lognormal) bằng các chuỗi ngẫu nhiên độc lập.
- **Sau (v2):**
  - Áp dụng kỹ thuật Số ngẫu nhiên chung CRN bắt cặp (paired differences):
    - Chênh lệch Mũ so với Gamma: $\Delta SL = -0.12\% \pm 0.18\%$ ($0 \in CI95 \implies$ Không khác biệt có ý nghĩa).
    - Chênh lệch Bootstrap so với Gamma: $\Delta SL = -0.05\% \pm 0.16\%$ ($0 \in CI95 \implies$ Không khác biệt có ý nghĩa).
    - Chênh lệch Lognormal ($cv + 20\%$) so với Gamma: $\Delta SL = -0.73\% \pm 0.22\%$ ($0 \notin CI95 \implies$ Giảm có ý nghĩa thống kê).
- **Lý do sửa:** Triệt tiêu hoàn toàn phương sai ngoại lai khi so sánh dạng phân phối.
- **Tệp cập nhật:** `results/final_v2/do_nhay_phan_phoi_v2.csv`.

---

### T9 (P1): Đánh giá tác động của Quy tắc Căn bậc hai
- **Nội dung:** Giữ vững kết luận về tính kinh tế theo quy mô ($c \approx a + \beta \sqrt{a}$). Với $\beta \approx 0.61$, khi nhu cầu tăng $+10\%$, số quầy-giờ chỉ cần tăng $+9.1\%$ (từ 44 lên 48 q-h) là đủ bù đắp tải.

---

### T10 (P1): Loại bỏ triệt để các khẳng định không căn cứ và từ ngữ tuyệt đối hóa
- **Trước (v1):**
  - Gọi lịch 6 quầy là "Hiện trạng chi nhánh".
  - Đưa ra các giả định không có trong dữ liệu: "Thứ 2, Thứ 6, ngày trả lương, đầu tuần, cuối tuần".
  - Dùng các từ tuyệt đối hóa: "biên an toàn rất cao", "hoàn hảo", "tuyệt đối".
- **Sau (v2):**
  - Đổi "Hiện trạng" $\to$ **"Mốc cơ sở: Hằng số 6 quầy (không phải nhân sự thực tế)"**.
  - Đổi "Thứ 2, Thứ 6, ngày trả lương" $\to$ **"Ngày lưu lượng cao (> 687 khách/ngày)"**.
  - Bỏ toàn bộ từ ngữ phóng đại; công cụ `tools/check_consistency.py` xác nhận 0 vi phạm trên toàn bộ tài liệu.
- **Lý do sửa:** Tuân thủ tính liêm chính học thuật, bám sát dữ liệu thực nghiệm.
- **Tệp cập nhật:** Toàn bộ các tệp tài liệu trong `docs/` và `README.md`.

---

### T11 (P1): Minh bạch hóa nguồn gốc và đối chiếu các bộ tham số
- **Sau (v2):** Xuất bảng `results/final_v2/tham_so_thanh_phan.csv` và `results/final_v2/doi_chieu_tham_so.csv` đối chiếu chi tiết giữa tập Train (10 ngày, 6.867 khách), tập Test (4 ngày, 2.969 khách) và toàn bộ 14 ngày.
- **Tệp cập nhật:** `results/final_v2/tham_so_thanh_phan.csv`, `results/final_v2/doi_chieu_tham_so.csv`.

---

### T12 (P1): Bổ sung thống kê Khách ưu tiên (VIP) theo từng khung giờ
- **Sau (v2):** Xuất bảng `results/final_v2/pvip_theo_gio.csv` chi tiết tỉ lệ khách VIP ($30.9\% - 39.8\%$) và mức phục vụ VIP ($W_q \le 2$ phút) trên từng giờ trong ngày, đảm bảo mọi giờ đều đạt chuẩn $\ge 90\%$.
- **Tệp cập nhật:** `results/final_v2/pvip_theo_gio.csv`.

---

### T13 (P2): Mở rộng bộ kiểm thử tự động pytest lên 18 ca kiểm thử
- **Trước (v1):** 12 bài unit test trong `test_theory.py` và `test_sim.py`.
- **Sau (v2):** Bổ sung file `tests/test_v2_features.py` với 6 ca kiểm thử mới kiểm tra toàn diện các tính năng v2:
  1. `test_milp_pure_4h_52`: Kiểm tra MILP thuần ca 4h ra đúng 52 quầy-giờ.
  2. `test_milp_pure_8h_model_a_64`: Kiểm tra Mô hình A thuần 8h ra đúng 64 quầy-giờ.
  3. `test_milp_pure_8h_model_b_48`: Kiểm tra Mô hình B thuần 8h ra đúng 48 quầy-giờ làm việc (6 nhân viên).
  4. `test_milp_model_a_infeasible`: Kiểm tra Mô hình A vô nghiệm với 4 NV 8h + 3 NV 4h.
  5. `test_milp_model_b_unique_44`: Kiểm tra Mô hình B có duy nhất 1 nghiệm 44 quầy-giờ với 4 NV 8h + 3 NV 4h.
  6. `test_day_variation_reduces_sla`: Kiểm tra việc đưa biến động ngày vào làm giảm xác suất đạt SLA mọi giờ.
- **Kết quả:** 18/18 passed in pytest (15.77s), log lưu tại `results/final_v2/pytest_log.txt`.

---

### T14 (P2): Tự động hóa và đóng băng toàn diện thư mục `results/final_v2/`
- **Sau (v2):**
  - Xây dựng `tools/build_tables.py` tự động đọc CSV và sinh bảng Markdown.
  - Xây dựng `tools/check_consistency.py` tự động quét các thuật ngữ bị cấm và đối chiếu số liệu.
  - Tạo `results/final_v2/MO_TA.md` mô tả cấu trúc và nội dung của toàn bộ 15 tệp kết quả mới.
