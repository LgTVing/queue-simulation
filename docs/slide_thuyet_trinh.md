# Kịch Bản và Đề Cương Thuyết Trình Dự Án (14 Slide + Phụ Lục Q&A)

**Đề tài:** Mô phỏng Hàng đợi và Xác định Số Quầy Phục vụ Tối ưu cho Chi nhánh Ngân hàng  
**Thời lượng trình bày:** 20 phút (15 phút thuyết trình + 5 phút Q&A)  
**Số liệu:** V5, `results/final_v5/` (2026-10-30). Mọi con số dưới đây có nguồn trong [`tong_hop.md`](../tong_hop.md).  
**Nhóm sinh viên thực hiện:**  
- **Thành viên A:** Dữ liệu, ước lượng tham số, kiểm định phân phối, ngoài mẫu  
- **Thành viên B:** Lý thuyết (Erlang C, Erlang-A, SIPP), ca làm việc (MILP), chi phí  
- **Thành viên C:** Mô phỏng SimPy, kiểm chứng, tối ưu hóa, độ nhạy  

---

## CẤU TRÚC BỘ SLIDE (14 SLIDE CHÍNH)

### SLIDE 1: Trang Tiêu Đề
- **Tiêu đề:** MÔ PHỎNG HÀNG ĐỢI VÀ XÁC ĐỊNH SỐ QUẦY PHỤC VỤ TỐI ƯU TẠI CHI NHÁNH NGÂN HÀNG
- **Tiêu đề phụ:** Kết hợp lý thuyết hàng đợi và mô phỏng sự kiện rời rạc SimPy
- **Thời lượng:** 0:30 | **Người trình bày:** Thành viên A
- **Lời thoại:**
  > *"Kính thưa thầy cô, nhóm em trình bày đề tài xác định số quầy tối thiểu theo từng giờ để đạt cam kết dịch vụ, và kiểm tra con số đó bền đến đâu."*

---

### SLIDE 2: Bài Toán và Cam Kết Dịch Vụ (SLA)
- **Thông điệp chính:** Cân bằng chi phí quầy và trải nghiệm khách bằng một SLA đo được
- **Nội dung:**
  - **SLA 90/5:** $\ge 90\%$ khách được phục vụ với thời gian chờ $\le 5$ phút. Khách bỏ về tính là không đạt.
  - **VIP (~35% khách):** theo dõi $P(W_q \le 2) \ge 90\%$, ưu tiên không ngắt.
  - **Tiêu chí chọn lịch:** cận dưới CI95 của SL **ở mọi giờ** $\ge 90\%$.
  - **Khó khăn:** nhu cầu đổi theo giờ (0.99–1.54 khách/phút), khách bỏ về khi chờ lâu, thời gian phục vụ biến động cao ($cs^2 = 1.20$).
- **Thời lượng:** 1:00 | **Người trình bày:** Thành viên A
- **Lời thoại:**
  > *"Chúng em tính SL trên mọi khách đến, kể cả người bỏ về, nên đây là định nghĩa bảo thủ. Một lịch chỉ được chấp nhận khi giờ tệ nhất vẫn đạt 90% ở cận dưới khoảng tin cậy."*
- **Chuyển tiếp:** *"Các tham số lấy từ dữ liệu thật."*

---

### SLIDE 3: Dữ Liệu Thực Tế
- **Thông điệp chính:** Nhu cầu biến động theo giờ và giữa các ngày
- **Hình:** [`fig_a_fit.png`](../results/final_v5/hinh/fig_a_fit.png)
- **Nội dung:**
  - Anonymous Bank (Technion SEE Center), nghiệp vụ `PS`, 8h–17h, 14 ngày, **9.836 khách**. Train 10 ngày (6.867), test 4 ngày (2.969).
  - Đỉnh 10h–11h: $\lambda = 1.535$ khách/phút (train). 8/9 giờ bác bỏ Poisson giữa các ngày.
  - Quá phân tán ngày: độ lệch chuẩn 87.1 khách so với 26.5 nếu Poisson. Mô hình dùng hệ số nhân ngày với $CV = 14.0\%$.
  - Lưu ý: đây là dữ liệu **tổng đài**; cúp máy tương đương bỏ về.
- **Thời lượng:** 1:00 | **Người trình bày:** Thành viên A
- **Lời thoại:**
  > *"Số khách giữa các ngày dao động gấp khoảng ba lần so với Poisson, nên mô hình phải có biến động ngày, nếu không sẽ quá lạc quan."*

---

### SLIDE 4: Thời Gian Phục Vụ và Kiên Nhẫn
- **Thông điệp chính:** Không phân phối tham số nào khớp; dùng phân phối thực nghiệm
- **Nội dung:**
  - $E[S] = 2.92$ phút, $cs^2 = 1.20$ (train, 6.346 quan sát).
  - Gamma có AIC tốt nhất nhưng cả 4 phân phối (Gamma, Weibull, Exponential, Lognormal) đều bị KS bootstrap bác bỏ. Gamma có $cs^2 = 0.91$, đánh giá thấp độ biến động.
  - **Mô hình chính:** lấy mẫu trực tiếp từ dữ liệu train.
  - Kiên nhẫn: $\hat\theta = 521 / 4.793,6 = 0.1087$ phút$^{-1}$ (trung bình 9.2 phút), MLE có kiểm duyệt.
  - Weibull có kiểm duyệt khớp tốt hơn mũ ($k = 0.855$, AIC thấp hơn 18.7), nhưng tối ưu lại vẫn ra cùng lịch 45 quầy-giờ (S12).
- **Thời lượng:** 1:00 | **Người trình bày:** Thành viên A
- **Lời thoại:**
  > *"Chọn Gamma theo AIC sẽ làm thời gian phục vụ đều hơn thực tế. Vì vậy chúng em lấy mẫu trực tiếp, và Gamma chỉ dùng để kiểm tra độ nhạy."*

---

### SLIDE 5: Bảng Quyết Định Giải Tích (SIPP)
- **Thông điệp chính:** Tính tay trước khi mô phỏng: Erlang C 47 q-h, Erlang-A 44 q-h

| Giờ | 8h | 9h | 10h | 11h | 12h | 13h | 14h | 15h | 16h | Tổng |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Erlang C | 4 | 6 | 6 | 6 | 5 | 5 | 5 | 5 | 5 | **47** |
| Erlang-A | 4 | 5 | 6 | 5 | 5 | 5 | 5 | 5 | 4 | **44** |

- Erlang-A tính đến khách bỏ về nên bớt 1 quầy ở 9h, 11h, 16h. Cái giá: khoảng 5% khách bỏ về.
- **Thời lượng:** 1:00 | **Người trình bày:** Thành viên B
- **Lời thoại:**
  > *"Bảng này làm bằng Excel và Python độc lập, cho cùng kết quả. Nó là điểm xuất phát cho thuật toán mô phỏng."*

---

### SLIDE 6: Mô Hình Mô Phỏng SimPy
- **Thông điệp chính:** Mô phỏng xử lý những gì công thức bỏ qua
- **Nội dung:**
  - Lịch quầy đổi theo giờ; nhân viên chỉ rời quầy khi phục vụ xong; sau 17h xả hàng bằng số quầy giờ cuối.
  - Ưu tiên VIP, khách bỏ về, phục vụ thực nghiệm, biến động ngày.
  - Số ngẫu nhiên chung (CRN); **chọn lịch bằng seed 1000, đánh giá bằng seed 50000** để tránh thiên lệch chọn lựa.
- **Thời lượng:** 1:00 | **Người trình bày:** Thành viên C

---

### SLIDE 7: Kiểm Chứng Mô Hình
- **Thông điệp chính:** Động cơ mô phỏng khớp nghiệm chính xác

| Kiểm tra | Lý thuyết | Mô phỏng (CI95) | Sai lệch |
|---|:---:|:---:|:---:|
| M/M/c: SL | 0.9654 | 0.9688 ± 0.0037 | +0.35% |
| Erlang-A: SL | 0.8689 | 0.8695 ± 0.0034 | +0.07% |
| Erlang-A: $p_{ab}$ | 0.1144 | 0.1142 ± 0.0022 | −0.21% |
| M/G/1 P-K chính xác: $W_q$ | 14.625 | 14.218 ± 0.627 | −2.78% |
| M/G/6, cv 1.5 (Allen–Cunneen, xấp xỉ) | 1.370 | 1.182 ± 0.072 | −13.8% |

- Gộp hàng: 1 hàng chung 96.5% so với 6 hàng riêng 50.7%.
- **Hình:** [`fig_c_pooling.png`](../results/final_v5/hinh/fig_c_pooling.png)
- **Thời lượng:** 1:30 | **Người trình bày:** Thành viên C
- **Lời thoại:**
  > *"Với các mô hình có nghiệm chính xác, lý thuyết luôn nằm trong khoảng tin cậy. Sai lệch lớn chỉ xuất hiện khi so với công thức xấp xỉ Allen–Cunneen, nên chúng em không dùng công thức đó để chọn số quầy."*

---

### SLIDE 8: Tối Ưu Lịch Quầy Bằng Mô Phỏng
- **Thông điệp chính:** Lịch tối ưu `[4, 5, 6, 5, 5, 5, 5, 5, 5]` = **45 quầy-giờ**
- **Nội dung:**
  - Bắt đầu từ Erlang-A 44 q-h: giờ 16h–17h cận dưới 0.889 < 0.90 → thêm 1 quầy.
  - Bớt 1 quầy ở bất kỳ giờ nào (9 phép) đều vi phạm; 117 cấu hình lân cận (hoán đổi, giảm 2 quầy) đều vi phạm.
  - → **Tối thiểu cục bộ** theo tiêu chí mô phỏng (chưa phải tối ưu toàn không gian).
  - Lý do cần hơn Erlang-A 1 quầy: phục vụ thực tế biến động hơn mũ ($cs^2 = 1.20$). Tối ưu lại với Gamma vẫn ra 44.
  - **Tối ưu theo giờ công (M6):** liệt kê mọi cách xếp ca 8h/4h phủ SIPP Erlang-A. 44 giờ công: không khả thi; 48 giờ công: 33/94 cách khả thi, tốt nhất là **Lịch 48 `[4, 6, 6, 6, 5, 5, 6, 5, 5]`, 4 ca 8h + 4 ca 4h**. → **Tối thiểu 48 giờ công/ngày.**
- **Thời lượng:** 1:30 | **Người trình bày:** Thành viên C
- **Lời thoại:**
  > *"45 là số quầy-giờ mở ít nhất. Nhưng câu hỏi của quản lý là bao nhiêu giờ công nhân viên. Tối ưu thẳng theo giờ công cho đáp số 48, và cách xếp tốt nhất ở mức đó chính là Lịch 48."*

---

### SLIDE 9: Kết Quả So Sánh Chính Sách (300 Lần Lặp)
- **Thông điệp chính:** Lịch 45 tiết kiệm 16.7% quầy-giờ mở so với 6 quầy cố định

| Chính sách | Q-h | SL ngày | Giờ tệ nhất (cận dưới) | Bỏ về | $W_q$ |
|---|:---:|:---:|:---:|:---:|:---:|
| 6 quầy cố định | 54 | 97.63% | 94.94% | 2.17% | 0.20 p |
| SIPP Erlang C | 47 | 95.30% | 92.76% | 4.10% | 0.38 p |
| SIPP Erlang-A | 44 | 93.69% | 90.44% (sát ngưỡng) | 5.43% | 0.50 p |
| **Tối ưu mô phỏng** | **45** | **94.23%** | **92.36%** | **4.99%** | **0.46 p** |
| Bền vững (+10%) | 48 | 95.79% | 93.27% | 3.70% | 0.34 p |

- Hiệu suất quầy: 60.8% (6 quầy) → 70.9% (Lịch 45). Khách VIP: 95.6% chờ $\le 2$ phút.
- **Thời lượng:** 1:30 | **Người trình bày:** Thành viên C
- **Lời thoại:**
  > *"Lịch 45 đạt chuẩn ở mọi giờ, giờ tệ nhất là 11h–12h. Lịch 44 của Erlang-A nằm đúng ranh giới: đạt với bộ seed này nhưng hụt với bộ seed khác, nên chúng em giữ 45."*

---

### SLIDE 10: Lịch 45 Mỏng Đến Đâu?
- **Thông điệp chính:** Lịch 45 đủ cho ngày bình thường nhưng không chịu được ngày đông
- **Hình:** [`fig_c_do_nhay.png`](../results/final_v5/hinh/fig_c_do_nhay.png)
- **Nội dung:**
  - 14 ngày thực tế: Lịch 45 đạt **12/14** (hụt ngày 2 và ngày 7, hai ngày đông nhất); Lịch 48 đạt 14/14.
  - Có biến động ngày: $P(SL_{\text{ngày}} \ge 90\%)$ = 85.7% (Lịch 45) và 95.0% (Lịch 48).
  - Nhu cầu +10%: giờ tệ nhất Lịch 45 còn **87.9%**, Lịch 48 còn **90.9%**.
  - Lịch 45 đạt SL đến khoảng **803 khách/ngày** (trung bình train là 687).
  - **Chọn lịch theo xác suất đạt SLA ngày (M7):** đạt SLA ở $\ge 90\%$ số ngày cần **48 giờ công** (Lịch 48: 94.5% [93.5%, 95.5%], xác nhận độc lập 2.000 lần lặp); $\ge 95\%$ số ngày cần **52 giờ công**.
- **Thời lượng:** 1:30 | **Người trình bày:** Thành viên C

---

### SLIDE 11: Nếu Khách Quầy Kiên Nhẫn Hơn Khách Tổng Đài?
- **Thông điệp chính:** Con số thực tế nằm trong khoảng 45–48 q-h
- **Hình:** [`fig_kien_nhan_vs_quay_gio.png`](../results/final_v5/hinh/fig_kien_nhan_vs_quay_gio.png), [`fig_pareto_bo_ve.png`](../results/final_v5/hinh/fig_pareto_bo_ve.png)
- **Nội dung:**
  - Kiên nhẫn 9.2 phút (ước lượng): 45 q-h; 15–60 phút: **46 q-h**; không ai bỏ về: **48 q-h**.
  - Lịch 45 có 4.99% khách bỏ về, sát 5%. Giới hạn bỏ về ≤ 3% cần 51 q-h; ≤ 2% cần 55 q-h.
- **Thời lượng:** 1:00 | **Người trình bày:** Thành viên B
- **Lời thoại:**
  > *"Khi khách kiên nhẫn hơn, ít người bỏ về nên hàng dài hơn và cần thêm quầy. Một phần tiết kiệm của Lịch 45 đến từ việc khách bỏ về; đây là điều quản lý cần biết."*

---

### SLIDE 12: Ca Làm Việc và Chi Phí
- **Thông điệp chính:** Tính theo giờ công, Lịch 45 và Lịch 48 tốn như nhau
- **Hình:** [`fig_b_ca_lam.png`](../results/final_v5/hinh/fig_b_ca_lam.png)
- **Nội dung:**
  - Ca 8h (nghỉ trưa 11h–14h) + ca 4h: Lịch 45 **không phủ đúng được**, cần 5 ca 8h + 2 ca 4h = **48 q-h công** (dư 3). Lịch 48 phủ đúng bằng 4 ca 8h + 4 ca 4h = **48 q-h công**.
  - Chi phí $C = \text{quầy-giờ} + k \cdot N \cdot p_{ab}$: Lịch 45 rẻ nhất khi $k < 0.33$; Lịch 48 khi $0.33 < k < 0.58$; 6 quầy cố định khi $k > 0.58$.
  - **Mở thêm quầy theo hàng chờ (M8):** Lịch 45 + mở thêm 1 quầy khi có hơn 2 người chờ liên tục 5 phút: trung bình **46.17 quầy-giờ** mở, đạt SLA ở **97.3%** số ngày (Lịch 48 cố định: 94.0%), 14/14 ngày thực tế. Cần 1 nhân viên dự phòng.
- **Thời lượng:** 1:30 | **Người trình bày:** Thành viên B
- **Lời thoại:**
  > *"Nếu chi phí chính là lương nhân viên, Lịch 48 có cùng chi phí với Lịch 45 nhưng bền hơn và ít khách bỏ về hơn."*

---

### SLIDE 13: Ngoài Mẫu và Bất Thường 15h–16h
- **Thông điệp chính:** Mô hình khớp 3/4 ngày test; ngày lệch có nguyên nhân rõ
- **Nội dung:**
  - 7/9 giờ có SL thực tế nằm trong khoảng dự báo 95%.
  - 15h–16h thực tế chỉ 76.5%, nhưng **do riêng ngày 10**: SL 31.5%, thời gian phục vụ cao hơn 29%, tải 6.14 Erlang, trong khi chỉ khoảng 4 người phục vụ. Ba ngày còn lại đạt 93–98%.
  - Bài học: cần cơ chế tăng cường quầy trong ngày khi hàng chờ tăng bất thường (M8, slide 12). Dự báo sớm lúc 10h (fit trên train, sai số ngoài mẫu 64 khách) không bắt được cả hai ngày hụt.
  - Mô phỏng lại kiểu ngày 10 (phục vụ chậm 29% ở 14h–17h): không lịch nào giữ được giờ tệ nhất ≥ 90%; mở thêm quầy giảm thiệt hại (0.82 → 0.87).
- **Thời lượng:** 1:00 | **Người trình bày:** Thành viên A

---

### SLIDE 14: Kết Luận và Khuyến Nghị
- **Thông điệp chính:** Tối thiểu 48 giờ công/ngày, xếp 4 ca 8h + 4 ca 4h theo Lịch 48
- **Nội dung:**
  1. **Khuyến nghị:** `[4, 6, 6, 6, 5, 5, 6, 5, 5]` = 48 giờ công (mức tối thiểu, M6), phủ đúng bằng 4 ca 8h + 4 ca 4h, SL 95.8%, giờ tệ nhất 93.3%, đạt 14/14 ngày thực tế, chịu được nhu cầu +10%.
  2. **Ít quầy-giờ mở nhất:** `[4, 5, 6, 5, 5, 5, 5, 5, 5]` = 45 q-h, SL 94.2%, giờ tệ nhất 92.4%, tiết kiệm 9 q-h/ngày (16.7%) so với 6 quầy cố định, nhưng cũng tốn 48 giờ công.
  3. **Có người dự phòng:** Lịch 45 + mở thêm 1 quầy khi hơn 2 người chờ liên tục 5 phút (M8). Cần đạt SLA ở $\ge 95\%$ số ngày: 52 giờ công (M7).
  4. **Giữ một hàng chung** (bốc số).
  5. **Hạn chế:** dữ liệu tổng đài; kiên nhẫn quầy cần đo thực tế (45–48 q-h tùy kiên nhẫn); kết luận chi phí phụ thuộc $k$; chỉ xét ca 8h/4h nghỉ trưa 11h–14h.
- **Thời lượng:** 1:30 | **Người trình bày:** Thành viên C
- **Lời thoại:**
  > *"Câu trả lời ngắn: cần ít nhất 48 giờ công nhân viên mỗi ngày, xếp 4 ca 8h và 4 ca 4h theo Lịch 48. Lịch 45 mở ít quầy hơn nhưng vẫn tốn 48 giờ công, nên Lịch 48 bền hơn mà không tăng chi phí nhân sự. Xin cảm ơn thầy cô."*

---

## PHỤ LỤC: CÂU HỎI PHẢN BIỆN DỰ KIẾN

1. **Vì sao không dùng thẳng Erlang-A (44 q-h)?**
   *Trả lời:* Erlang-A giả định phục vụ mũ và hệ dừng trong từng giờ. Với phục vụ thực tế ($cs^2 = 1.20$), giờ 16h–17h có cận dưới 0.889 (seed chọn lịch) hoặc 0.904 (seed đánh giá), tức nằm đúng ranh giới. Mô phỏng thêm 1 quầy để chắc chắn.

2. **Dữ liệu tổng đài có áp dụng được cho quầy không?**
   *Trả lời:* Cơ chế hàng đợi giống nhau, khác ở kiên nhẫn. Chúng em đã chạy lại với kiên nhẫn 15 phút đến vô cùng: kết quả 46–48 q-h. Bước tiếp theo là đo kiên nhẫn tại quầy (`docs/ke_hoach_khao_sat.md`).

3. **Lịch 45 có chắc là nhỏ nhất trong mọi lịch có thể không?**
   *Trả lời:* Không. Đã kiểm 9 phép bớt và 117 cấu hình lân cận đều vi phạm, nên đây là tối thiểu cục bộ theo tiêu chí mô phỏng.

4. **Làm sao biết mô phỏng đúng?**
   *Trả lời:* So với nghiệm chính xác M/M/c, Erlang-A và M/G/1 Pollaczek–Khinchine, lý thuyết đều nằm trong CI95. 84 kiểm thử tự động pass; `tools/check_consistency.py` đối chiếu 1.502 con số trong `tong_hop.md` với CSV.

5. **Vì sao số liệu khác bản trước (44 q-h)?**
   *Trả lời:* V4 sửa ba lỗi động cơ (xả hàng sau 17h, dòng đến tại ranh giới giờ, hiệu suất theo giờ) và đổi sang phục vụ thực nghiệm. Tách riêng: sửa xả hàng chỉ đổi SL giờ cuối 0.9706 → 0.9704; nguyên nhân chính là phân phối phục vụ (tối ưu với Gamma vẫn ra 44).

6. **Bất định tham số ảnh hưởng thế nào?**
   *Trả lời:* 94% phương sai kết quả đến từ bất định tham số, không phải nhiễu mô phỏng. Qua 50 bộ tham số bootstrap, Lịch 45 đạt SL ngày ≥ 90% ở 50/50 bộ và giờ tệ nhất ≥ 90% ở 45/50 bộ.

7. **Vì sao kết luận là 48 giờ công mà không phải 45 quầy-giờ?**
   *Trả lời:* Chi phí chính là lương nhân viên, tính theo giờ công. Với ca 8h (nghỉ trưa 11h–14h) và ca 4h, Lịch 45 không phủ đúng được nên vẫn tốn 48 giờ công. Tối ưu thẳng theo giờ công (M6) cho thấy không cách xếp ca nào dưới 48 giờ công đạt SLA; ở 48 giờ công, Lịch 48 tốt nhất trong 33 cách khả thi.

8. **Chính sách mở thêm quầy theo hàng chờ cần những gì?**
   *Trả lời:* Một nhân viên dự phòng (làm việc khác khi chưa cần), một quầy trống, và người theo dõi hàng chờ (hoặc màn hình bốc số). Quy tắc: hơn 2 người chờ liên tục 5 phút thì mở thêm 1 quầy, giữ ít nhất 30 phút, đóng khi hết hàng chờ. Quầy dự phòng mở trung bình 1.17 giờ/ngày (danh định) đến 1.43 giờ/ngày (14 ngày thực tế); chi phí người dự phòng không nằm trong quầy-giờ mở.

9. **Các giả định (kiên nhẫn mũ, λ cố định trong giờ) có làm sai kết luận không?**
   *Trả lời:* Đã kiểm tra cả hai. Kiên nhẫn Weibull khớp dữ liệu tốt hơn nhưng lịch tối ưu vẫn 45 quầy-giờ. λ theo nửa giờ chỉ khác rõ ở 8h–9h và cũng không đổi tổng quầy-giờ. Nghỉ trưa linh hoạt 9h–16h không giảm được giờ công dưới 48.

10. **SLA tính gộp mọi khách hay riêng khách thường? Nếu riêng thì Lịch 45 còn đạt không?**
   *Trả lời:* SLA chính tính trên mọi khách đến, vì Erlang C, Erlang-A và SIPP không tách nhóm khách. Riêng khách thường (VIP được ưu tiên nên khách thường chờ lâu hơn), Lịch 45 hụt ở 11h–12h (cận dưới 0.8997); Lịch 48 đạt cả SL mọi khách (0.9327), SL khách thường (0.9133) và SL VIP ≤ 2 phút (0.9425) ở mọi giờ. Khuyến nghị Lịch 48 không phụ thuộc cách định nghĩa (`sl_theo_nhom.csv`).

11. **Xác suất đạt SLA theo ngày có bị đánh giá trên chính dữ liệu đã dùng để chọn lịch không?**
   *Trả lời:* Ở V5.0 có: dải seed đánh giá trùng 253/300 lần lặp với dải chọn lịch. V5.1 xác nhận lại bằng dải seed độc lập 2.000 lần lặp: Lịch 48 đạt 94.5% [93.5%, 95.5%] số ngày, nên kết luận "≥ 90% số ngày cần 48 giờ công, ≥ 95% cần 52" không đổi; các số $P$ của M7 thấp hơn bản cũ 0.4–1.3 điểm ở 5/6 dòng.
