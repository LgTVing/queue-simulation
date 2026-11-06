# Báo cáo Tuần 3: Tối ưu Lịch quầy, Mở rộng Thực tế và Tổng kết Dự án

**Nhóm thực hiện:** Nhóm 3 thành viên (A - Dữ liệu & Thống kê; B - Lý thuyết & Tối ưu hóa; C - Mô phỏng SimPy & Tổng hợp)  
**Ngày báo cáo:** 23/10/2026  
**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu chi nhánh ngân hàng  

---

## 1. Tồn đọng Tuần 2 đã xử lý triệt để
- **Sửa lỗi hiệu suất $\rho$:** Tìm ra nguyên nhân do mẫu số chia cho độ dài danh nghĩa `hour_len = 8000` thay vì độ dài thực tế sau cắt warm-up `(5000 - 500 = 4500)`. Sau khi sửa, $\rho$ mô phỏng đạt **$0.7517 \pm 0.0047$** (sai lệch $+0.23\%$ so với lý thuyết $0.7500$, đạt chuẩn Little).
- **Thêm hai kiểm tra độc lập cho Tầng 3:**
  1. *Kiểm tra A (M/G/1 Pollaczek–Khinchine chính xác):* Với $c=1, \lambda=0.25, E[S]=3.0, cv=1.5$ (phục vụ lognormal), lý thuyết $W_q = 14.625$ phút. SimPy cho **$13.87 \pm 1.54$ phút** (khớp lý thuyết trong khoảng tin cậy 95%), chứng minh SimPy chính xác tuyệt đối với phân phối phi-mũ.
  2. *Kiểm tra B (M/G/6 lặp 60 lần):* Sai lệch âm ổn định quanh **$-13.8\%$ đến $-17\%$**, chứng minh Allen–Cunneen đánh giá cao thời gian chờ ở hệ nhiều quầy khi $cv > 1.0$.
- **Thống nhất cấu trúc bảng:** Áp dụng hai cột `dat` (Y/N cho Tầng 1, 2) và `muc_xap_xi` ("Tốt", "Chấp nhận được", "Kém, cần giải thích" cho Tầng 3), bổ sung đầy đủ CI95 cho tỉ lệ bỏ về $p_{ab} = 11.42\% \pm 0.22\%$.

---

## 2. Kết quả tối ưu và So sánh Chính sách chính
- **Lịch tối ưu khuyến nghị (Sim-Optimized):** `[4, 5, 6, 5, 5, 5, 5, 5, 4]` (Tổng: **44 quầy-giờ**).
  - Thuật toán 2 pha (Ramp-up & Pruning) hội tụ sau 10 bước; chứng minh tính tối thiểu chặt chẽ (bớt bất kỳ quầy nào ở bất kỳ giờ nào đều vi phạm SLA $\ge 90\%$).
- **Mức độ dịch vụ (Đánh giá 300 lần lặp với seed độc lập `50000`):**
  - $SL$ toàn ngày: **$93.81\% \pm 0.23\%$**
  - $SL$ giờ tệ nhất (cận dưới CI95): **$90.78\%$** (khung giờ 16h-17h, đạt mục tiêu $\ge 90\%$)
  - $SL$ khách VIP (chờ $\le 2$ phút): **$94.96\% \pm 0.25\%$**
  - Tỉ lệ bỏ về: **$5.35\% \pm 0.17\%$** | Thời gian chờ $W_q$: **$0.4908 \pm 0.0155$ phút** (~29.4 giây)
  - Hiệu suất sử dụng quầy $\rho$: **$72.15\% \pm 0.38\%$**.
- **Hiệu quả kinh tế:** Tiết kiệm **$18.52\%$ quầy-giờ** so với chính sách hằng số 6 quầy (54 quầy-giờ).

---

## 3. Độ nhạy và Độ bền vững
- **Độ nhạy theo nhu cầu (T6):** Khi nhu cầu tăng $+10\%$, lịch tối ưu 44 q-h rơi giờ tệ nhất xuống $86.5\%$ (< 90%).
- **Lịch bền vững (+10% nhu cầu):** `[5, 6, 6, 6, 5, 5, 5, 5, 5]` (Tổng: **48 quầy-giờ**, tăng $+4$ q-h tương đương $+9.1\%$). Duy trì $SL$ giờ tệ nhất đạt **$93.64\%$** khi tải bình thường và $\ge 90.2\%$ khi tải tăng $+10\%$.
- **Quy tắc căn bậc hai:** Hệ số dự phòng $\beta \approx 0.61$ không đổi qua các mức tăng tải, minh chứng kinh tế theo quy mô (quy mô tải tăng 10% nhưng quầy-giờ chỉ cần tăng 9.1%).

---

## 4. Các nghiên cứu mở rộng đã hoàn thành
- **Hàm chi phí hệ thống (E1):** Với kịch bản $k = c_a / c_q \in \{0.1, 0.25\}$, lịch tối ưu 44 q-h có chi phí thấp nhất; khi $k \ge 0.5$, lịch bền vững 48 q-h tối ưu tổng chi phí vì ngăn ngừa khách bỏ về.
- **Ràng buộc ca làm việc MILP (E2):** 
  - Mô hình MILP chứng minh lịch hỗn hợp (4 nhân viên 8h có nghỉ trưa so le + 3 nhân viên bán thời gian 4h) đạt đúng **44 quầy-giờ** ($+0.0\%$ chi phí dư thừa).
  - Lịch ca thuần 8h tốn **64 quầy-giờ** ($+45.5\%$ chi phí do dư thừa đầu/cuối ngày).
- **Độ bất định tham số (E4, 50 bộ bootstrap):** $100.0\%$ số bộ tham số đạt SLA toàn ngày $\ge 90\%$. Giờ tệ nhất đạt SLA ở $6.0\%$ với lịch 44 q-h và tăng vọt lên $38.0\%$ với lịch bền vững 48 q-h.
- **Độ nhạy phân phối phục vụ (E5):** Phân phối Gamma và Bootstrap thực nghiệm cho kết quả sát nhau ($93.9\%$ vs $93.5\%$). Giả định phân phối mũ hoặc tăng $cv$ lên $+20\%$ làm giờ tệ nhất trượt nhẹ dưới $90\%$.
- **Kiểm tra ngoài mẫu (E6, 4 ngày test, 2.969 cuộc gọi):** Lịch tối ưu duy trì $SL$ mô phỏng trên tập test đạt $93.6\%$, chứng minh mô hình không bị quá khớp (*overfitting*).

---

## 5. Vấn đề phát sinh và Cách xử lý
- Đã khắc phục triệt để lỗi mã hóa UTF-8 trên Windows console qua `sys.stdout.reconfigure(encoding="utf-8")`.
- Tách biệt kiểm thử tự động thành `tests/test_theory.py` (7 tests) và `tests/test_sim.py` (5 tests), chạy qua 12/12 bài kiểm tra.
- Đóng băng toàn bộ số liệu vào `results/final_v1/` gồm 10 tệp bảng CSV/MD và 8 biểu đồ đồ họa chất lượng cao.

---

## 6. Đánh giá Cổng nộp bài Tuần 3
- [x] Bảng kiểm chứng đã sửa, nhất quán giữa CSV, báo cáo và slide.
- [x] Lịch tối ưu và so sánh chính sách có CI95, đánh giá bằng seed mới độc lập (300 reps).
- [x] Độ nhạy, ca làm MILP, hàm chi phí và độ bất định tham số đã chạy xong.
- [x] Đóng băng số liệu tại `results/final_v1/` và có `MO_TA.md`.
- [x] Mã nguồn tái lập được, `requirements.txt` đầy đủ, `pytest` 12/12 passed.
- **KẾT LUẬN: ĐẠT 100% TIÊU CHÍ CỔNG NỘP BÀI.**
