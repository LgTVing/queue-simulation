# Báo cáo Tiến độ Tuần 2

**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu  
**Thời gian thực hiện:** Tuần 2 (Từ Ngày 1 đến Ngày 7)  
**Nhóm thực hiện:** 3 sinh viên (Thành viên A, B, C)  

---

## 1. Mục tiêu Tuần 2
- Tham số hóa hoàn chỉnh từ dữ liệu thực nghiệm (chốt `params.json` v2.0).
- Xây dựng bảng quyết định số quầy hoàn chỉnh (Erlang C, Erlang-A, SIPP) và bộ kiểm thử tự động lý thuyết (`pytest`).
- Lập trình mô phỏng sự kiện rời rạc bằng SimPy và hoàn thành Kiểm chứng Ba tầng so với giải tích lý thuyết.
- Phân tích giai đoạn khởi động (Welch warm-up) và chứng minh hiệu quả của mô hình hàng chung (Pooling).

---

## 2. Các tham số chính thức đã chốt (`docs/params.json` v2.0)
- **Tập ước lượng (Train):** 10 ngày đầu (6.867 bản ghi); **Tập kiểm tra (Test):** 4 ngày cuối (2.969 bản ghi).
- **Tốc độ đến ($\lambda_h$ khách/phút):** `[0.9900, 1.3767, 1.5350, 1.3900, 1.2400, 1.2017, 1.3383, 1.3167, 1.0567]`.
- **Mô hình phục vụ tối ưu:** Phân phối **Gamma** ($\text{shape} = 1.0955, \text{scale} = 2.6688$), $E[S] = 2.9236$ phút, $cv = 1.0963, cs^2 = 1.2018$. Đạt chỉ số AIC tốt nhất ($26.314,2$), vượt trội so với phân phối Mũ, Lognormal và Weibull.
- **Tốc độ bỏ về ($\theta$):** $\hat{\theta} = 0.1087$ (1/phút) $\implies$ Kiên nhẫn trung bình = $9.20$ phút.
- **Tỉ lệ khách VIP:** $35.43\%$.

---

## 3. Bảng quyết định và So sánh Chính sách Lịch quầy
- **Lịch Hằng số (Constant):** Duy trì cố định 6 quầy cả ngày $\implies$ **54 quầy-giờ** (Lãng phí lớn ở đầu và cuối ngày).
- **Lịch SIPP Erlang C:** `[4, 6, 6, 6, 5, 5, 5, 5, 5]` $\implies$ **47 quầy-giờ** (Tiết kiệm $-13.0\%$, đạt SLA $\ge 91.9\%$).
- **Lịch SIPP Erlang-A:** `[4, 5, 6, 5, 5, 5, 5, 5, 4]` $\implies$ **44 quầy-giờ** (Tiết kiệm $-18.5\%$, đạt SLA $\ge 92.2\%$).
- **Độ nhạy lý thuyết:** Lịch Erlang-A rất nhạy với biến động: khi nhu cầu tăng $+10\%$, SLA giờ thấp nhất giảm xuống $89.5\%$ (dưới ngưỡng 90%). Nhóm khuyến nghị bổ sung 1 quầy dự phòng ở giờ 16h (thành 45 quầy-giờ) để bảo đảm an toàn.

---

## 4. Kết quả Kiểm chứng Ba tầng và Thí nghiệm Mô phỏng
- **Bộ kiểm thử tự động lý thuyết:** `tests/test_theory.py` chạy qua 7/7 test cases (100% Passed trên `pytest`).
- **Tầng 1 (M/M/c):** Mô phỏng khớp giải tích lý thuyết Erlang C: $SL = 96.6\%$ (Lý thuyết $96.54\%$, sai lệch $+0.1\%$, nằm trong CI 95%), $W_q = 0.84$ phút (sai lệch $< 0.5\%$).
- **Tầng 2 (Erlang-A):** Mô phỏng khớp nghiệm ma trận hấp thụ Markov: $SL = 86.9\%$ (Lý thuyết $86.89\%$, sai lệch $< 0.1\%$), $W_q = 1.14$ phút, $p_{ab} = 11.4\%$.
- **Tầng 3 (M/G/c Allen-Cunneen):** Khớp tốt ở $cv = 0.5$ và $cv = 1.0$; ở $cv = 1.5$ sai lệch phản ánh đúng giới hạn xấp xỉ của công thức Allen-Cunneen khi độ biến thiên dịch vụ cao.
- **Đường cong Welch:** Xác nhận thời gian chuyển tiếp khởi động cần khoảng 200 khách (~150 phút). Do chi nhánh mở cửa trống lúc 8h sáng, mô phỏng ngày làm việc thực tế không cần cắt warm-up.
- **Hiệu ứng gộp hàng đợi (Pooling):** Chứng minh xếp 1 hàng chung nâng tỉ lệ đạt SLA từ $50.6\%$ (hàng riêng ngẫu nhiên) lên **$96.5\%$**.

---

## 5. Vấn đề phát sinh và Cách xử lý
1. **Lỗi hiển thị `#NAME?` trong Excel:** Khắc phục triệt để bằng cách thay thế hàm `POISSON.DIST` sang hàm tương thích toàn cầu `POISSON`, rà soát và xác nhận 0 lỗi trên toàn bộ các tệp `.xlsx`.
2. **Kiểm định KS quá nhạy với mẫu lớn:** Nhóm đã kết hợp thêm tiêu chuẩn AIC và Q-Q plot trực quan để chọn phân phối Gamma khách quan nhất.

---

## 6. Đánh giá Cổng kiểm soát Tuần 2 (Gate Control)

| Hạng mục kiểm soát | Tiêu chuẩn đánh giá | Kết quả |
|---|---|:---:|
| **Dữ liệu & Tham số** | `params.json` v2.0 đã chốt, phân phối có căn cứ AIC/Q-Q, số liệu test set đã bàn giao | **ĐẠT** |
| **Lý thuyết** | Bảng quyết định hoàn chỉnh, kiểm thử `pytest` 100% Passed, phân tích độ nhạy | **ĐẠT** |
| **Mô phỏng** | SimPy chạy tham số thật, qua kiểm chứng 3 tầng (sai lệch $< 2\%$), có hình Welch & Pooling | **ĐẠT** |
| **Quản trị** | Báo cáo tuần hoàn thành, mã nguồn chạy đồng nhất end-to-end | **ĐẠT** |

$$\implies \mathbf{KẾT\ LUẬN:\ ĐẠT\ TOÀN\ DIỆN\ CỔNG\ KIỂM\ SOÁT\ TUẦN\ 2.}$$

---

## 7. Kế hoạch trọng tâm Tuần 3
- Chạy thuật toán tối ưu hóa lịch quầy 2 pha (Heuristic tăng/giảm) trên SimPy.
- So sánh chi tiết 3 chính sách (Hằng số vs SIPP vs Tối ưu mô phỏng).
- Phân tích độ nhạy chi tiết trên mô phỏng (tăng tải $+10\%, +20\%, +30\%$).
- Ghép nối toàn bộ báo cáo tổng kết 25 trang và slide thuyết trình 14 trang.
