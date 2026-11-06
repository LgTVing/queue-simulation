# Báo cáo Kiểm chứng Mô hình Mô phỏng Ba tầng

**Người phụ trách:** Thành viên C  
**Ngày cập nhật:** 30/10/2026 (số liệu V4, giữ nguyên ở V5; `results/final_v5/kiem_chung.csv`, `kiem_chung_pooling.csv`)  
**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu  

---

## 1. Kết quả Kiểm chứng Ba tầng và Hai Kiểm tra Độc lập

Khoảng tin cậy dùng Student-t ($df = n_{\text{reps}} - 1$).

| Tầng kiểm chứng | Chỉ số | Lý thuyết | Mô phỏng | $n_{\text{reps}}$ | CI95 | Sai lệch | Đạt? | Ghi chú |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **Tầng 1 (M/M/c)** | SL = P(Wq ≤ 5) | 0.9654 | 0.9688 | 30 | ±0.0037 | +0.35% | Y | Lý thuyết nằm trong CI95 [0.9651, 0.9725] |
| **Tầng 1 (M/M/c)** | Wq (phút) | 0.8433 | 0.8170 | 30 | ±0.0423 | −3.12% | Y | Lý thuyết nằm trong CI95 [0.775, 0.859] |
| **Tầng 1 (M/M/c)** | Hiệu suất ρ | 0.7500 | 0.7511 | 30 | ±0.0048 | +0.15% | Y | Khớp định luật Little |
| **Tầng 2 (Erlang-A)** | SL (phục vụ và chờ ≤ 5) | 0.8689 | 0.8695 | 30 | ±0.0034 | +0.07% | Y | Khớp nghiệm ma trận hấp thụ Markov |
| **Tầng 2 (Erlang-A)** | Wq (phút) | 1.1444 | 1.1475 | 30 | ±0.0233 | +0.27% | Y | Wq tính trên mọi khách ($L_q/\lambda$) |
| **Tầng 2 (Erlang-A)** | Tỉ lệ bỏ về $p_{ab}$ | 0.1144 | 0.1142 | 30 | ±0.0022 | −0.21% | Y | Lý thuyết nằm trong CI95 [0.1120, 0.1164] |
| **Tầng 2 (Erlang-A)** | Hiệu suất ρ | 0.8856 | 0.8863 | 30 | ±0.0032 | +0.08% | Y | Khớp $\rho = \lambda(1-p_{ab})E[S]/c$ |
| **Tầng 3 (M/G/c, cv = 0.5)** | Wq (phút) | 0.5271 | 0.5616 | 30 | ±0.0176 | +6.55% | – | Allen–Cunneen đánh giá thấp 6.6% (xấp xỉ) |
| **Tầng 3 (M/G/c, cv = 1.0)** | Wq (phút) | 0.8433 | 0.8113 | 30 | ±0.0521 | −3.80% | – | Trùng Erlang C |
| **Tầng 3 (M/G/c, cv = 1.5)** | Wq (phút) | 1.3704 | 1.1333 | 30 | ±0.1239 | −17.30% | – | Allen–Cunneen đánh giá cao (xấp xỉ) |
| **Kiểm tra A (M/G/1 P-K chính xác, 40.000 phút)** | Wq (phút) | 14.6250 | 14.2179 | 40 | ±0.6273 | −2.78% | Y | Lý thuyết nằm trong CI95 [13.59, 14.85] |
| **Kiểm tra B (M/G/6, cv = 1.5)** | Wq (phút) | 1.3704 | 1.1815 | 60 | ±0.0722 | −13.78% | – | Allen–Cunneen đánh giá cao khi cv > 1 |

**Kết luận:** ở mọi phép so với nghiệm chính xác (tầng 1, tầng 2, Kiểm tra A), giá trị lý thuyết nằm trong CI95 của mô phỏng. Tầng 3 và Kiểm tra B so với công thức **xấp xỉ** Allen–Cunneen nên không gán "Đạt"; sai lệch ở đó phản ánh giới hạn của công thức.

### Phân tích Tầng 3 và hai kiểm tra độc lập
1. **Kiểm tra A (M/G/1 Pollaczek–Khinchine chính xác):**
   - $c = 1$, $\lambda = 0.25$, $E[S] = 3.0$, phục vụ lognormal $cv = 1.5$ ($cs^2 = 2.25$):
     $$W_q = \frac{\rho E[S] (1 + cs^2)}{2(1 - \rho)} = \frac{0.75 \times 3.0 \times (1 + 2.25)}{2(1 - 0.75)} = 14.625\text{ phút}$$
   - Chạy 40.000 phút (bỏ 5.000 phút khởi động), 40 lần lặp: $14.2179 \pm 0.6273$ phút. Giá trị lý thuyết nằm trong CI95, nên không bác bỏ được tính đúng của động cơ SimPy với phục vụ phi-mũ.
2. **Kiểm tra B (M/G/6, $cv = 1.5$, 60 lần lặp):**
   - Mô phỏng 1.1815 phút so với Allen–Cunneen 1.3704 phút (−13.8%); với 30 lần lặp ở Tầng 3 là −17.3%. Sai lệch luôn cùng chiều: Allen–Cunneen đánh giá cao thời gian chờ của hệ nhiều quầy khi $cv > 1$.
   - **Hệ quả:** không dùng Allen–Cunneen để quyết định số quầy khi $cv$ lớn; dùng mô phỏng.

---

## 2. Phân tích Hiện tượng Khởi động (Welch)
- Theo dõi thời gian chờ của 1.200 khách đầu tiên trong hệ chạy dài ($\rho = 0.90$, tải cao để thấy rõ pha chuyển tiếp). Hình: [`fig_c_welch.png`](../results/final_v5/hinh/fig_c_welch.png).
- Khoảng 200 khách đầu (~150 phút), thời gian chờ tăng từ 0 lên mức cân bằng; sau đó đường trung bình trượt (window = 50) dao động ổn định.
- **Quy tắc:**
  - Mô phỏng hệ dừng (kiểm chứng lý thuyết): bỏ **500 phút đầu**.
  - Mô phỏng một ngày làm việc 8h–17h: **không cắt warm-up**, vì chi nhánh thực sự mở cửa với hệ thống trống.

---

## 3. Hiệu ứng Gộp hàng đợi (Queue Pooling)
6 quầy, $\lambda = 1.5$ khách/phút, phục vụ trung bình 3 phút (`kiem_chung_pooling.csv`, hình [`fig_c_pooling.png`](../results/final_v5/hinh/fig_c_pooling.png)):

| Cách tổ chức | P(chờ ≤ 5 phút) |
|---|:---:|
| 1 hàng chung (M/M/6, lý thuyết) | **96.5%** |
| 6 hàng riêng, chọn ngẫu nhiên (lý thuyết) | 50.6% |
| 6 hàng riêng, chọn ngẫu nhiên (SimPy) | 50.7% |
| 6 hàng riêng, chọn hàng ngắn nhất (JSQ, SimPy) | 81.1% |

**Kết luận:** một hàng chung (bốc số) cho mức phục vụ cao nhất. Chọn hàng ngắn nhất cải thiện nhiều so với chọn ngẫu nhiên nhưng vẫn thấp hơn hàng chung khoảng 15 điểm phần trăm, vì quầy rảnh không lấy được khách đang chờ ở hàng khác. Các kết quả về số quầy trong dự án giả định chi nhánh dùng một hàng chung.
