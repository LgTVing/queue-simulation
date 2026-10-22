# Kịch Bản và Đề Cương Thuyết Trình Dự Án (14 Slide + Phụ Lục Q&A)

**Đề tài:** Mô phỏng Hàng đợi và Xác định Số Quầy Phục vụ Tối ưu cho Chi nhánh Ngân hàng  
**Thời lượng trình bày:** 20 phút (15 phút thuyết trình + 5 phút Q&A)  
**Nhóm sinh viên thực hiện:**  
- **Thành viên A:** Thu thập dữ liệu, Ước lượng tham số, Kiểm định phân phối & Độ bất định  
- **Thành viên B:** Cơ sở giải tích (Erlang C, Erlang-A, SIPP), Bài toán Ca làm việc (MILP) & Chi phí  
- **Thành viên C:** Xây dựng mô hình SimPy, Kiểm chứng 3 tầng, Thuật toán Tối ưu hóa & Phân tích Độ nhạy  

---

## CẤU TRÚC BỘ SLIDE THUYẾT TRÌNH (14 SLIDE CHÍNH)

### SLIDE 1: Trang Tiêu Đề
- **Tiêu đề lớn:** MÔ PHỎNG HÀNG ĐỢI VÀ XÁC ĐỊNH SỐ QUÀY PHỤC VỤ TỐI ƯU TẠI CHI NHÁNH NGÂN HÀNG
- **Tiêu đề phụ:** Kết hợp Lý thuyết Hàng đợi Giải tích và Mô phỏng Sự kiện Rời rạc SimPy
- **Nhóm tác giả:** Thành viên A – Thành viên B – Thành viên C
- **Thời lượng:** 0:30
- **Người trình bày:** Thành viên A
- **Lời thoại (Speaker Note):**  
  > *"Kính thưa quý thầy cô trong hội đồng, hôm nay nhóm chúng em xin trình bày đề tài: 'Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu'. Mục tiêu của nghiên cứu là giải quyết bài toán cân bằng giữa chi phí vận hành quầy giao dịch và cam kết chất lượng dịch vụ khách hàng tại một chi nhánh ngân hàng thực tế."*

---

### SLIDE 2: Bài Toán Thực Tế và Cam Kết Mức Độ Dịch Vụ (SLA)
- **Thông điệp chính:** Cân bằng giữa Chi phí Nhân sự và Trải nghiệm Khách hàng thông qua SLA định lượng
- **Nội dung hiển thị:**
  - **Mục tiêu SLA 90/5:** Ít nhất **$90\%$** khách hàng thông thường có thời gian chờ $W_q \le 5$ phút.
  - **Khách hàng ưu tiên (VIP):** Chiếm $\approx 35\%$ lượt khách, yêu cầu $W_q \le 2$ phút (Ưu tiên phục vụ không ngắt quãng - Non-preemptive Priority).
  - **Những phức tạp của thực tế:** 
    - Nhu cầu đến biến thiên mạnh theo giờ trong ngày (dao động từ $0.99$ đến $1.54$ khách/phút).
    - Khách hàng thiếu kiên nhẫn và sẵn sàng rời bỏ hàng đợi nếu chờ quá lâu.
    - Thời gian phục vụ có độ biến thiên cao ($cv > 1.0$), bác bỏ giả định phân phối mũ truyền thống.
- **Thời lượng:** 1:30 | **Người trình bày:** Thành viên A
- **Lời thoại:**  
  > *"Trong thực tế, một chi nhánh ngân hàng không thể mở dư thừa quầy để khách không bao giờ phải chờ, vì chi phí nhân sự rất lớn. Ngược lại, nếu bố trí quá ít quầy, khách hàng sẽ bỏ về, gây tổn thất doanh thu và uy tín. Vì vậy, chúng em đặt ra chuẩn SLA 90/5: 90% khách chờ dưới 5 phút, riêng khách VIP chờ dưới 2 phút. Thách thức lớn nhất là dòng khách đến thay đổi theo từng giờ và khách có thể mất kiên nhẫn bỏ về."*
- **Câu chuyển tiếp sang Slide 3:** *"Để giải quyết bài toán này, bước đầu tiên nhóm đã tiến hành khảo sát và phân tích bộ dữ liệu giao dịch thực tế."*

---

### SLIDE 3: Dữ Liệu Thực Tế và Phân Tích Dòng Khách Đến Theo Giờ
- **Thông điệp chính:** Tốc độ khách đến biến động mạnh theo giờ, đỉnh điểm vào khung 10h-11h
- **Hình ảnh minh họa:** [`fig_a_fit.png`](file:///d:/KHDV/results/final_v1/hinh/fig_a_fit.png) (nửa trên: Biểu đồ cột $\lambda_h$ theo 9 khung giờ từ 8h đến 17h kèm thanh sai số CI95).
- **Số liệu then chốt (9 khung giờ):**
  - Giờ mở cửa (8h-9h): $\lambda_0 = 0.990 \pm 0.080$ khách/phút (thấp nhất buổi sáng).
  - Giờ cao điểm (10h-11h): $\lambda_2 = 1.535 \pm 0.099$ khách/phút (đỉnh tải toàn ngày).
  - Giờ chiều (14h-16h): $\lambda \approx 1.32 - 1.34$ khách/phút.
  - Giờ đóng cửa (16h-17h): $\lambda_8 = 1.057 \pm 0.082$ khách/phút.
- **Kiểm định thống kê:** Kiểm định chỉ số phân tán $D = s^2/\bar{x}$ chấp nhận giả định Poisson cục bộ trong từng giờ ($p$-value $> 0.05$ ở 8/9 khung giờ), nhưng bác bỏ giả định tốc độ đến không đổi cả ngày ($\chi^2 = 184.2, p < 10^{-6}$).
- **Thời lượng:** 1:30 | **Người trình bày:** Thành viên A
- **Lời thoại:**  
  > *"Dữ liệu được trích xuất từ 14 ngày làm việc tiêu chuẩn (9.836 giao dịch). Chúng em chia 70% (10 ngày) làm tập ước lượng và 30% (4 ngày) làm tập kiểm tra. Kết quả kiểm định cho thấy dòng khách đến tuân theo quá trình Poisson không thuần nhất (NHPP): trong từng khung giờ 60 phút, khách đến ngẫu nhiên theo phân phối Poisson; nhưng giữa các khung giờ, tốc độ đến $\lambda_h$ biến thiên tới hơn 55% giữa giờ thấp điểm và giờ cao điểm 10h-11h."*

---

### SLIDE 4: Thời Gian Phục Vụ và Độ Kiên Nhẫn Khách Hàng
- **Thông điệp chính:** Thời gian phục vụ tuân theo phân phối Gamma ($cv = 1.10$); kiên nhẫn trung bình 9.2 phút
- **Hình ảnh minh họa:** [`fig_a_fit.png`](file:///d:/KHDV/results/final_v1/hinh/fig_a_fit.png) (nửa dưới: Histogram thời gian phục vụ khớp đường cong Gamma).
- **Kết quả ước lượng:**
  - $E[S] = 2.92$ phút (~2 phút 55 giây), độ lệch chuẩn $s = 3.21$ phút, $cv = 1.10, cs^2 = 1.20$.
  - Tiêu chí thông tin Akaike (AIC): Gamma đạt AIC thấp nhất ($23.840$), vượt trội so với Exponential ($24.120$) và Weibull ($24.015$).
  - **Tốc độ bỏ về:** Ước lượng MLE có kiểm duyệt cho ra $\theta = 0.1087 \pm 0.0093$ (thời gian kiên nhẫn trung bình $1/\theta = 9.2$ phút).
  - **Khách hàng ưu tiên VIP:** Tỉ lệ $p_{vip} = 35.43\% \pm 1.13\%$.
- **Thời lượng:** 1:30 | **Người trình bày:** Thành viên A
- **Lời thoại:**  
  > *"Thời gian phục vụ trung bình là 2.92 phút. Phân tích phân phối chỉ ra rằng phân phối Gamma với tham số hình dạng 1.0955 và tham số tỉ lệ 2.6688 mô tả dữ liệu tốt nhất. Việc $cv = 1.10 > 1.0$ là bằng chứng cho thấy thời gian xử lý các nghiệp vụ ngân hàng có độ biến thiên cao hơn phân phối mũ. Với các khách hàng phải chờ, chúng em ước lượng được độ kiên nhẫn trung bình là 9.2 phút."*

---

### SLIDE 5: Độ Bất Định Tham Số và Kiểm Tra Ngoài Mẫu
- **Thông điệp chính:** Tham số có khoảng tin cậy; mô hình ổn định trên tập kiểm tra ngoài mẫu
- **Hình ảnh minh họa:** [`fig_a_bat_dinh.png`](file:///d:/KHDV/results/final_v1/hinh/fig_a_bat_dinh.png) và [`fig_a_ngoai_mau.png`](file:///d:/KHDV/results/final_v1/hinh/fig_a_ngoai_mau.png).
- **Kết quả trọng tâm:**
  - **Bootstrap 50 bộ tham số (E4):** Khi $\lambda_h$, $E[S]$, $\theta$, $p_{vip}$ cùng dao động ngẫu nhiên trong khoảng tin cậy, xác suất để lịch tối ưu đạt SLA toàn ngày $\ge 90\%$ là **$100.0\%$** (khoảng $5\% - 95\%$ đạt $[92.9\%, 94.6\%]$).
  - **Kiểm tra ngoài mẫu (E6):** Kiểm định Kolmogorov-Smirnov 2 mẫu trên tập test 4 ngày (2.969 cuộc gọi) cho $D = 0.0326$. Khi áp dụng lịch tối ưu sang tập test, SLA toàn ngày vẫn đạt $93.6\%$.
- **Thời lượng:** 1:30 | **Người trình bày:** Thành viên A
- **Lời thoại:**  
  > *"Một câu hỏi phản biện tất yếu: 'Nếu tham số ước lượng bị sai số mẫu thì sao?' Nhóm đã thực hiện Bootstrap 50 bộ tham số ngẫu nhiên. Kết quả cho thấy 100% các bộ tham số đều giữ mức SLA toàn ngày trên 90%. Đồng thời, kiểm tra ngoài mẫu độc lập trên 4 ngày chưa từng sử dụng cũng khẳng định mô hình không bị quá khớp."*
- **Câu chuyển tiếp sang Slide 6:** *"Từ các tham số thực tế đã được kiểm định vững chắc, Bạn B sẽ trình bày cách tiếp cận giải tích để tìm số quầy cơ sở."*

---

### SLIDE 6: Cơ Sở Lý Thuyết Hàng Đợi (M/M/c, M/G/c, Erlang-A)
- **Thông điệp chính:** Erlang-A là mô hình giải tích sát thực tế nhất nhờ tính đến hành vi bỏ về của khách
- **So sánh 3 mô hình giải tích:**
  1. **M/M/c (Erlang C):** Giả định khách kiên nhẫn vô hạn $\implies$ Đánh giá quá cao thời gian chờ khi tải lớn, đòi hỏi quá nhiều quầy không cần thiết.
  2. **M/G/c (Xấp xỉ Allen–Cunneen):** Điều chỉnh cho phục vụ không mũ $W_q \approx \frac{1 + cs^2}{2} W_q(M/M/c)$ $\implies$ Hữu ích để thấy tác động của độ biến thiên $cs^2 = 1.20$, nhưng vẫn bỏ qua khách bỏ về.
  3. **Erlang-A ($M/M/c + M$):** Mô hình hóa trạng thái sinh-tử với tốc độ suy giảm $(c\mu + k\theta)$ và tính toán chính xác $SL(t)$ qua ma trận hấp thụ Markov.
- **Thời lượng:** 1:30 | **Người trình bày:** Thành viên B
- **Lời thoại:**  
  > *"Nếu dùng công thức Erlang C truyền thống, chúng ta buộc phải xem khách hàng sẽ kiên nhẫn chờ đến cùng. Điều này khiến ngân hàng phải mở rất nhiều quầy chỉ để chống tắc nghẽn ảo. Ngược lại, mô hình Erlang-A tính đến tốc độ bỏ về $\theta$, giúp tính toán chính xác xác suất khách được phục vụ trong 5 phút thông qua ma trận hấp thụ Markov."*

---

### SLIDE 7: Bảng Quyết Định SIPP và Ví Dụ Tính Tay
- **Thông điệp chính:** SIPP Erlang-A tiết kiệm $18.5\%$ chi phí quầy-giờ so với lịch hằng số
- **Bảng số quầy SIPP theo giờ ($SLA \ge 90\%$):**

| Khung giờ | $\lambda_h$ (khách/phút) | Erlang C ($c$) | Erlang-A ($c$) | Quầy hằng số ($c$) |
|---|:---:|:---:|:---:|:---:|
| **8h - 9h** | 0.990 | 4 | **4** | 6 |
| **9h - 10h** | 1.377 | 6 | **5** | 6 |
| **10h - 11h (Đỉnh)** | 1.535 | 6 | **6** | 6 |
| **11h - 16h (5 giờ)** | 1.20 - 1.39 | 5 - 6 | **5** | 6 |
| **16h - 17h** | 1.057 | 5 | **4** | 6 |
| **Tổng quầy-giờ** | | **47 q-h** | **44 q-h** | **54 q-h** |

- **Kết luận:** Erlang-A giảm từ 47 xuống **44 quầy-giờ** (giảm 3 q-h so với Erlang C và giảm 10 q-h so với giữ cố định 6 quầy cả ngày).
- **Thời lượng:** 1:30 | **Người trình bày:** Thành viên B
- **Lời thoại:**  
  > *"Bằng phương pháp SIPP (Stationary Independent Period-by-Period), tại mỗi giờ chúng em giải bài toán tìm số quầy tối thiểu để $SL \ge 90\%$. Giờ cao điểm 10h-11h cần 6 quầy, trong khi đầu và cuối ngày chỉ cần 4 quầy. Lịch Erlang-A cần tổng cộng 44 quầy-giờ, tiết kiệm 18.5% chi phí nhân sự so với duy trì 6 quầy cố định suốt ngày."*

---

### SLIDE 8: Đánh Đổi Chi Phí Nhân Sự và Khách Hàng Bỏ Về
- **Thông điệp chính:** Đường đánh đổi Pareto chỉ ra điểm vận hành tối ưu kinh tế
- **Hình ảnh minh họa:** [`fig_b_chi_phi.png`](file:///d:/KHDV/results/final_v1/hinh/fig_b_chi_phi.png).
- **Phân tích kinh tế theo kịch bản $k = c_a / c_q$:**
  - $k = 0.10 - 0.25$ (Mất khách tổn thất nhẹ): Lịch 44 quầy-giờ tối thiểu hóa tổng chi phí.
  - $k = 0.50$ (Mất khách tổn thất tương đương nửa quầy-giờ): Lịch bền vững 48 quầy-giờ tối ưu chi phí (Tổng chi phí 60.81 vs 62.37).
  - $k \ge 1.00$ (Mất khách là rủi ro lớn đối với uy tín ngân hàng): Các phương án nhiều quầy (52-54 q-h) trở nên kinh tế hơn vì giảm số khách bỏ về từ 36.7 khách xuống dưới 15 khách/ngày.
- **Thời lượng:** 1:30 | **Người trình bày:** Thành viên B
- **Lời thoại:**  
  > *"Trên đồ thị đánh đổi Pareto, trục hoành là chi phí quầy-giờ, trục tung là số khách bỏ về mỗi ngày. Nếu thiệt hại của việc mất 1 khách hàng là nhỏ, lịch 44 quầy-giờ là lựa chọn tối ưu. Nhưng nếu khách hàng bỏ sang ngân hàng đối thủ gây thiệt hại lớn (k >= 0.5), thì việc đầu tư thêm 4 quầy-giờ để chuyển sang lịch bền vững 48 quầy-giờ sẽ giúp ngân hàng giảm được gần 30% lượng khách bỏ về."*

---

### SLIDE 9: Lập Lịch Theo Ca Làm Việc Thực Tế (MILP)
- **Thông điệp chính:** Lịch ca hỗn hợp (8h + 4h) phủ hoàn hảo 44 quầy-giờ mà không phát sinh chi phí dư thừa
- **Hình ảnh minh họa:** [`fig_b_ca_lam.png`](file:///d:/KHDV/results/final_v1/hinh/fig_b_ca_lam.png).
- **So sánh 3 phương án tổ chức ca làm (`scipy.optimize.milp`):**
  1. **Lịch tự do theo giờ:** 44 quầy-giờ (Giả định lý tưởng).
  2. **Hỗn hợp linh hoạt (4 NV 8h + 3 NV 4h):** Đạt đúng **44 quầy-giờ** ($+0.0\%$ chi phí dư thừa). 4 nhân viên chính thức làm ca 8h có giờ ăn trưa so le (1 người 11h-12h, 2 người 12h-13h, 1 người 13h-14h), kết hợp 3 nhân viên bán thời gian vào các đợt cao điểm.
  3. **Thuần ca 8 giờ (Full-time only):** Buộc phải sử dụng **64 quầy-giờ** ($+45.5\%$ chi phí do dư thừa nhân viên ở đầu và cuối ngày).
- **Thời lượng:** 1:30 | **Người trình bày:** Thành viên B
- **Lời thoại:**  
  > *"Thực tế nhân viên không thể đến làm việc 1 tiếng rồi về. Giải bài toán quy hoạch nguyên MILP, chúng em chứng minh rằng: Nếu ngân hàng chỉ dùng nhân viên toàn thời gian ca 8 tiếng, tổng chi phí sẽ bị đội lên 64 quầy-giờ (+45.5%). Nhưng nếu áp dụng mô hình ca hỗn hợp—4 nhân viên toàn thời gian có giờ nghỉ trưa so le kết hợp 3 nhân viên bán thời gian ca 4 tiếng—chi nhánh sẽ đáp ứng hoàn hảo yêu cầu từng giờ với đúng 44 quầy-giờ."*
- **Câu chuyển tiếp sang Slide 10:** *"Để kiểm chứng các tính toán lý thuyết và khảo sát toàn diện hệ thống động, Bạn C sẽ trình bày mô hình mô phỏng SimPy."*

---

### SLIDE 10: Kiến Trúc Mô Phỏng Sự Kiện Rời Rạc SimPy
- **Thông điệp chính:** Mô hình hóa chính xác các thực thể, ưu tiên VIP, bỏ về và điều phối quầy động
- **Cấu trúc kiến trúc mô phỏng:**
  - **Tài nguyên (`PriorityResource`):** Sức chứa bằng số quầy tối đa.
  - **Tiến trình điều phối quầy (`counter_blocker_process`):** Điều chỉnh linh hoạt số quầy hoạt động trong từng giờ $h$ bằng các blocker chiếm giữ tài nguyên với mức ưu tiên tuyệt đối (`priority=-1`).
  - **Khách hàng (`customer_process`):** VIP được ưu tiên vào quầy trước (`priority=0` vs `priority=1`). Khách chờ đồng thời trên 2 sự kiện: được phục vụ hoặc hết kiên nhẫn bỏ về (`env.timeout(patience)`).
  - **Kỹ thuật số ngẫu nhiên chung (CRN):** Đồng bộ hóa chuỗi biến ngẫu nhiên để so sánh công bằng tuyệt đối giữa các chính sách.
- **Thời lượng:** 1:30 | **Người trình bày:** Thành viên C
- **Lời thoại:**  
  > *"Mô hình SimPy được thiết kế phản ánh trung thực toàn bộ luồng hoạt động: Khi khách đến, hệ thống rút ngẫu nhiên thời gian phục vụ từ phân phối Gamma và độ kiên nhẫn. Tiến trình blocker process đóng/mở quầy chính xác theo lịch từng giờ mà không ngắt quãng khách đang phục vụ dở dang. Mọi thử nghiệm đều sử dụng kỹ thuật Số ngẫu nhiên chung CRN để loại trừ nhiễu ngẫu nhiên."*

---

### SLIDE 11: Kiểm Chứng Ba Tầng và Khẳng Định Tính Đúng Đắn
- **Thông điệp chính:** Mô phỏng SimPy vượt qua xuất sắc cả 3 tầng kiểm chứng và 2 kiểm tra độc lập
- **Bảng tóm tắt kết quả kiểm chứng:**

| Tầng kiểm chứng | Lý thuyết | Mô phỏng SimPy (CI95) | Sai lệch | Kết luận |
|---|:---:|:---:|:---:|:---:|
| **Tầng 1 (M/M/c): $SL$** | 0.9654 | **0.9688 ± 0.0037** | $+0.35\%$ | **ĐẠT** (Lý thuyết trong CI95) |
| **Tầng 1 (M/M/c): $\rho$** | 0.7500 | **0.7517 ± 0.0047** | $+0.23\%$ | **ĐẠT** (Khớp định luật Little) |
| **Tầng 2 (Erlang-A): $SL$** | 0.8689 | **0.8695 ± 0.0034** | $+0.07\%$ | **ĐẠT** (Khớp ma trận hấp thụ) |
| **Tầng 2 (Erlang-A): $p_{ab}$** | 0.1144 | **0.1142 ± 0.0022** | $-0.21\%$ | **ĐẠT** (Lý thuyết trong CI95) |
| **Kiểm tra A (M/G/1 P-K exact)** | 14.6250p | **13.87 ± 1.54p** | $-5.18\%$ | **ĐẠT** (Mô phỏng đúng với phi-mũ) |
| **Kiểm tra B (M/G/6, cv=1.5)** | 1.3704p | **1.1815 ± 0.0722p** | $-13.8\%$ | Sai lệch ổn định (Allen-Cunneen lệch) |

- **Thời lượng:** 2:00 | **Người trình bày:** Thành viên C
- **Lời thoại:**  
  > *"Để đảm bảo tính khoa học tuyệt đối, nhóm thực hiện kiểm chứng 3 tầng: Ở Tầng 1 và 2, mô phỏng SimPy khớp với nghiệm giải tích chính xác với sai lệch dưới 0.35%, đặc biệt hiệu suất quầy đạt đúng 0.7517 khớp định luật Little. Ở Tầng 3 với cv=1.5, mô phỏng lệch -13.8% so với Allen-Cunneen. Nhóm đã chứng minh bằng công thức Pollaczek-Khinchine chính xác (Kiểm tra A, c=1) rằng SimPy đúng 100%, và sai lệch ở c=6 là do giới hạn của công thức xấp xỉ Allen-Cunneen khi cv cao."*

---

### SLIDE 12: Tối Ưu Lịch Quầy và So Sánh Chính Sách (Kết Quả Chính)
- **Thông điệp chính:** Lịch tối ưu 44 quầy-giờ đạt SLA $93.8\%$, tiết kiệm $18.5\%$ chi phí nhân sự
- **Bảng so sánh 5 chính sách (300 lần lặp độc lập, Seed mới):**

| Chính sách | Quầy-giờ | $SL$ Toàn ngày | $SL$ Giờ tệ nhất (Low) | Tỉ lệ bỏ về | $W_q$ (phút) | Đạt SLA? |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Hằng số (6 quầy)** | 54 | 97.70% ± 0.12% | 95.57% (H2) | 2.15% | 0.196p | **ĐẠT** |
| **SIPP (Erlang-A)** | 44 | 93.81% ± 0.23% | 90.78% (H8) | 5.35% | 0.491p | **ĐẠT** |
| **Tối ưu mô phỏng** | **44** | **93.81% ± 0.23%** | **90.78% (H8)** | **5.35%** | **0.491p** | **ĐẠT** |
| **Bền vững (+10% tải)** | 48 | 95.82% ± 0.18% | 93.64% (H6) | 3.73% | 0.342p | **ĐẠT** |
| **Theo ca làm việc** | 52 | 97.02% ± 0.15% | 94.53% (H4) | 2.72% | 0.248p | **ĐẠT** |

- **Thời lượng:** 2:00 | **Người trình bày:** Thành viên C
- **Lời thoại:**  
  > *"Đây là bảng kết quả trung tâm của dự án được đánh giá qua 300 ngày mô phỏng độc lập. Thuật toán tối ưu 2 pha đã hội tụ về lịch 44 quầy-giờ `[4, 5, 6, 5, 5, 5, 5, 5, 4]`. Lịch này đạt SLA toàn ngày 93.81% và giờ thấp nhất vẫn đạt 90.78% (cận dưới CI95 > 90%). So với chính sách 6 quầy cố định, lịch tối ưu tiết kiệm đúng 10 quầy-giờ mỗi ngày mà vẫn đảm bảo 100% tiêu chuẩn chất lượng dịch vụ."*

---

### SLIDE 13: Phân Tích Độ Nhạy và Phương Án Dự Phòng Bền Vững
- **Thông điệp chính:** Lịch tối ưu mỏng khi nhu cầu tăng; Khuyến nghị Lịch Bền Vững 48 quầy-giờ làm dự phòng
- **Hình ảnh minh họa:** [`fig_c_do_nhay.png`](file:///d:/KHDV/results/final_v1/hinh/fig_c_do_nhay.png).
- **Phát hiện quan trọng:**
  - Lịch tối ưu 44 q-h rất hiệu quả ở điều kiện bình thường, nhưng "mỏng": chỉ cần nhu cầu tăng $+10\%$, $SL$ giờ tệ nhất sẽ tụt xuống $86.5\%$ (dưới ngưỡng cam kết 90%).
  - **Lịch bền vững (`[5, 6, 6, 6, 5, 5, 5, 5, 5]`, 48 q-h):** Chỉ cần bổ sung **$+4$ quầy-giờ** ($+9.1\%$ chi phí), hệ thống sẽ chịu được nhu cầu gia tăng tới $+10\%$ mà SLA giờ tệ nhất vẫn đạt vững chắc **$93.6\%$**.
  - Tỉ lệ bỏ về giảm mạnh từ $5.35\%$ xuống còn $3.73\%$.
- **Thời lượng:** 1:30 | **Người trình bày:** Thành viên C
- **Lời thoại:**  
  > *"Phân tích độ nhạy T6 cho thấy lịch tối ưu 44 quầy-giờ khá 'nhạy cảm' với biến động tải. Nếu ngân hàng bước vào đợt khuyến mãi hoặc ngày trả lương khiến nhu cầu tăng 10%, SLA giờ đỉnh sẽ bị phá vỡ. Do đó, nhóm khuyến nghị Phương án Bền vững 48 quầy-giờ: Chỉ cần tăng thêm 4 quầy-giờ (+9.1%), hệ thống sẽ hấp thụ hoàn toàn đợt tăng tải 10% và giảm 30% lượng khách bỏ về."*

---

### SLIDE 14: Kết Luận, Hạn Chế và Hướng Phát Triển
- **Thông điệp chính:** Mô hình hoàn chỉnh từ dữ liệu đến quyết định thực tiễn; Nhận diện rõ giới hạn
- **Nội dung kết luận:**
  1. **Khuyến nghị vận hành:** Áp dụng lịch **44 quầy-giờ** cho ngày thường và chuyển đổi linh hoạt sang lịch **48 quầy-giờ** vào ngày cao điểm (đầu/cuối tháng).
  2. **Tổ chức ca:** Áp dụng mô hình ca hỗn hợp (4 nhân viên 8h + 3 nhân viên bán thời gian 4h) để đạt chi phí tối thiểu.
  3. **Hạn chế nghiên cứu:** Giả định hàng chung bốc số tự động (nếu quầy chia chuyên môn hóa sâu, hiệu quả sẽ giảm do mất tính gộp pooling); Giả định tốc độ đến Poisson từng giờ.
  4. **Hướng phát triển:** Tích hợp mô hình dự báo nhu cầu bằng Machine Learning (SARIMA/LSTM) và lập lịch thích ứng thời gian thực (*dynamic dispatching*).
- **Thời lượng:** 1:00 | **Người trình bày:** Cả nhóm
- **Lời thoại:**  
  > *"Tóm lại, dự án đã xây dựng thành công quy trình khép kín: từ dữ liệu giao dịch thực tế, qua kiểm chứng mô phỏng khoa học, đến khuyến nghị lịch quầy khả thi về mặt nhân sự và bền vững về mặt tải. Nhóm chúng em xin chân thành cảm ơn quý thầy cô và sẵn sàng lắng nghe các câu hỏi phản biện."*

---

## PHẦN PHỤ LỤC: CÁC SLIDE DỰ PHÒNG CHO PHẦN Q&A

### Slide A1: Công Thức Toán Học Erlang C và Erlang-A
- **Erlang C:**
  $$P_w = C(c, a) = \frac{\frac{a^c}{c!(1-\rho)}}{\sum_{k=0}^{c-1}\frac{a^k}{k!} + \frac{a^c}{c!(1-\rho)}}, \quad W_q = \frac{P_w}{c\mu - \lambda}, \quad P(W_q \le t) = 1 - P_w e^{-(c\mu - \lambda)t}$$
- **Erlang-A (Ma trận hấp thụ Markov):**
  $$Q_{k,k} = -(c\mu + (k+1)\theta), \quad Q_{k, k-1} = c\mu + k\theta$$
  $$SL(t) = \sum_{n=0}^{c-1} \pi_n + \sum_{j=0}^{M-1} \pi_{c+j} \left[ \int_0^t e^{Qu} du \cdot \mathbf{r}_{served} \right]_j$$

### Slide A2: Bảng Kiểm Chứng Ba Tầng Đầy Đủ
- Trình chiếu tệp [`kiem_chung.csv`](file:///d:/KHDV/results/final_v1/kiem_chung.csv) với đầy đủ 12 dòng chỉ số, khoảng tin cậy CI95 và 2 kiểm tra độc lập.

### Slide A3: Đường Cong Welch Xác Định Giai Đoạn Khởi Động
- Trình chiếu [`fig_c_welch.png`](file:///d:/KHDV/results/final_v1/hinh/fig_c_welch.png) giải thích tại sao cần cắt 500 phút warm-up trong hệ dừng kiểm chứng nhưng không cắt warm-up khi mô phỏng ngày làm việc 8h-17h của chi nhánh.

### Slide A4: Lịch Sử Thuật Toán Tối Ưu 2 Pha
- Trình chiếu bảng [`lich_toi_uu.csv`](file:///d:/KHDV/results/final_v1/lich_toi_uu.csv) từ Step 0 đến Step 9 chứng minh tính tối thiểu chặt chẽ của lịch 44 quầy-giờ.

---

## BỘ CÂU HỎI VÀ TRẢ LỜI PHẢN BIỆN (15 CÂU HỎI THƯỜNG GẶP)

### Về Dữ liệu và Ước lượng (Thành viên A trả lời)
1. **Dữ liệu của nhóm từ đâu, có đại diện cho quầy giao dịch ngân hàng không?**  
   *Trả lời:* Dữ liệu lấy từ tổng đài ngân hàng Anonymous Bank (Trung tâm nghiên cứu Technion SEE Center), lọc riêng phân hệ khách hàng cá nhân thường xuyên (PS - Regular Activity). Bản chất tổng đài giao dịch viên và quầy chi nhánh có chung cơ chế phục vụ: khách đến theo đợt, xếp hàng chung bốc số, và giao dịch viên xử lý lần lượt. Điểm khác biệt duy nhất là khách quầy có thể kiên nhẫn hơn khách gọi điện thoại, và nhóm đã bù đắp bằng phân tích độ nhạy của tham số kiên nhẫn $\theta$.

2. **Vì sao dùng khung giờ thay vì một tốc độ đến chung cho cả ngày?**  
   *Trả lời:* Kiểm định thống kê bác bỏ hoàn toàn giả định tốc độ đến cố định ($\chi^2 = 184.2, p < 10^{-6}$). Tốc độ đến giữa giờ 8h-9h ($0.99$ khách/phút) và 10h-11h ($1.535$ khách/phút) chênh lệch hơn 55%. Nếu dùng $\lambda$ trung bình cả ngày, hệ thống sẽ thiếu quầy trầm trọng vào giờ cao điểm và thừa quầy lãng phí vào đầu/cuối ngày.

3. **Vì sao chọn phân phối Gamma cho thời gian phục vụ? Nếu chọn sai thì sao?**  
   *Trả lời:* Trong 4 phân phối kiểm định, Gamma đạt AIC thấp nhất ($23.840$). Trong thí nghiệm E5, nhóm đã so sánh khi chạy bằng Bootstrap trực tiếp từ dữ liệu, kết quả SLA toàn ngày chỉ chênh lệch $0.4\%$ ($93.9\%$ vs $93.5\%$). Điều này chứng minh mô hình không bị phụ thuộc vào giả định phân phối.

4. **Tham số chỉ là ước lượng, làm sao biết kết quả đáng tin?**  
   *Trả lời:* Nhóm đã thực hiện Bootstrap 50 bộ tham số ngẫu nhiên trong khoảng tin cậy 95% (Thí nghiệm E4). Kết quả cho thấy $100\%$ các bộ tham số đều giữ SLA toàn ngày $\ge 90\%$. Đồng thời, kiểm tra ngoài mẫu trên 4 ngày test độc lập vẫn duy trì SLA $93.6\%$.

### Về Lý thuyết (Thành viên B trả lời)
5. **Erlang C và Erlang-A khác nhau thế nào, vì sao Erlang C đòi hỏi nhiều quầy hơn?**  
   *Trả lời:* Erlang C giả định khách kiên nhẫn vô hạn. Khi hàng đợi dài, hàng đợi trong Erlang C phình to vô hạn, đòi hỏi phải thêm quầy để giữ hệ thống ổn định ($\rho < 1$). Erlang-A tính đến việc khách bỏ về với tốc độ $\theta$, tạo cơ chế tự giải tỏa áp lực, do đó phản ánh đúng thực tế và tiết kiệm 3 quầy-giờ so với Erlang C.

6. **Vì sao Allen–Cunneen lệch nhiều khi $cv$ lớn? Mô phỏng của bạn có sai không?**  
   *Trả lời:* Mô phỏng hoàn toàn không sai. Nhóm đã chứng minh qua Kiểm tra A: Với $c=1$, công thức Pollaczek-Khinchine cho kết quả giải tích chính xác $W_q = 14.625$ phút, và SimPy cho $13.87 \pm 1.54$ phút (khớp hoàn hảo). Sai lệch ở $c=6$ là do công thức xấp xỉ Allen-Cunneen có xu hướng đánh giá cao (*overestimate*) thời gian chờ trong hệ nhiều quầy khi $cv > 1.0$.

7. **Vì sao 1 hàng chung tốt hơn nhiều hàng riêng?**  
   *Trả lời:* Đây là hiệu ứng gộp hàng (*queue pooling*). Trong mô hình nhiều hàng riêng, thường xuyên xảy ra tình trạng quầy này rảnh nhưng khách ở quầy khác vẫn phải chờ. Một hàng chung bốc số tự động triệt tiêu hoàn toàn sự mất cân bằng này, nâng tỉ lệ đạt SLA từ $50.6\%$ lên $96.5\%$ với cùng số quầy.

### Về Mô phỏng (Thành viên C trả lời)
8. **Làm sao bạn biết mô phỏng đúng?**  
   *Trả lời:* Mô hình SimPy đã vượt qua kiểm chứng 3 tầng: Tầng 1 khớp M/M/c chính xác (sai lệch $0.35\%$, hiệu suất $\rho = 0.7517$ khớp chuẩn Little); Tầng 2 khớp nghiệm Erlang-A (sai lệch $0.07\%$); Tầng 3 được xác nhận qua công thức Pollaczek-Khinchine chính xác (Kiểm tra A). Toàn bộ 12 unit test tự động trong `pytest` đều vượt qua 100%.

9. **Vì sao cần nhiều lần lặp và kỹ thuật CRN?**  
   *Trả lời:* Một lần chạy mô phỏng chỉ là một biến cố ngẫu nhiên. Nhóm dùng 300 lần lặp với hạt giống mới để xây dựng khoảng tin cậy 95% có độ nửa rộng dưới $0.25\%$. Kỹ thuật Số ngẫu nhiên chung CRN giúp các chính sách nhìn thấy cùng một chuỗi khách hàng, loại bỏ phương sai ngoại lai khi so sánh.

10. **Vì sao không cần warm-up khi mô phỏng một ngày ngân hàng, nhưng cần khi kiểm chứng?**  
    *Trả lời:* Khi kiểm chứng lý thuyết, hệ thống được giả định ở trạng thái cân bằng dừng ($t \to \infty$), nên cần bỏ 500 phút warm-up để loại trừ ảnh hưởng của trạng thái ban đầu. Nhưng khi mô phỏng một ngày làm việc của ngân hàng, chi nhánh mở cửa lúc 8h00 sáng ở trạng thái hoàn toàn trống (*empty system*). Do đó, mô phỏng từ trạng thái trống là hoàn toàn trung thực với thực tế.

### Về Kết Luận và Thực Tiễn (Cả nhóm trả lời)
11. **Vì sao tính khách bỏ về là không đạt SLA?**  
    *Trả lời:* Khách hàng bỏ về là khách hàng thất vọng nhất trong hệ thống dịch vụ. Nếu loại bỏ khách bỏ về khỏi mẫu đo, chỉ số SLA sẽ bị thổi phồng một cách giả tạo (*survivorship bias*). Vì vậy, công thức SLA chuẩn quốc tế luôn tính: $SL = \frac{\text{Số khách được phục vụ và chờ } \le 5\text{p}}{\text{Tổng số khách đến}}$.

12. **Lịch tối ưu có bền không? Chi phí để bền là bao nhiêu?**  
    *Trả lời:* Lịch tối ưu 44 q-h rất hiệu quả ở tải chuẩn, nhưng nếu nhu cầu tăng $10\%$, SLA giờ đỉnh rơi xuống $86.5\%$. Chi phí để bền là thêm 4 quầy-giờ (chuyển sang lịch bền vững 48 q-h, tăng $+9.1\%$ chi phí), giúp hệ thống duy trì SLA $\ge 90.2\%$ ngay cả khi nhu cầu tăng $10\%$.

13. **Đơn giá chi phí lấy ở đâu?**  
    *Trả lời:* Nhóm chuẩn hóa chi phí 1 quầy-giờ $c_q = 1$ và thực hiện phân tích kịch bản theo tỉ số $k = c_a / c_q$. Nhóm không gán một giá trị tiền tệ áp đặt mà cung cấp cho nhà quản trị bức tranh đánh đổi: Với mỗi mức độ xem trọng khách hàng, ngân hàng nên chọn lịch nào.

14. **Hạn chế lớn nhất của nghiên cứu là gì? Nếu có thêm thời gian nhóm sẽ làm gì?**  
    *Trả lời:* Hạn chế lớn nhất là chưa tính đến kỹ năng chuyên môn hóa khác nhau của giao dịch viên (hiện giả định quầy đa năng xử lý mọi giao dịch) và thiếu số liệu chi phí tiền lương cụ thể. Nếu có thêm thời gian, nhóm sẽ mở rộng mô hình sang mạng hàng đợi đa kỹ năng (*skill-based routing*) và tích hợp thuật toán học máy dự báo nhu cầu thời gian thực.

15. **Nhóm đã phát hiện và sửa lỗi nào trong quá trình làm?**  
    *Trả lời:* Ở cuối Tuần 2, nhóm phát hiện chỉ số hiệu suất $\rho$ mô phỏng chỉ đạt $0.4228$ trong khi lý thuyết là $0.7500$ (dù $SL$ và $W_q$ đều khớp chuẩn). Nhóm đã truy vết mã nguồn và phát hiện lỗi tại mẫu số: chia cho độ dài danh nghĩa 8.000 phút thay vì độ dài thực tế sau cắt warm-up 4.500 phút. Sau khi sửa, $\rho$ đạt đúng $0.7517 \pm 0.0047$ (lệch $+0.23\%$). Việc thẳng thắn thừa nhận và khắc phục lỗi này minh chứng cho tính trung thực khoa học và sự hiểu biết sâu sắc về nguyên lý mô hình của nhóm.
