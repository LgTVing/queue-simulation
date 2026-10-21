# Cơ sở lý thuyết và công thức toán học hàng đợi (Tuần 1)

**Người phụ trách:** Thành viên B  
**Ngày cập nhật:** 21/10/2026  
**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu  

---

## 1. Ký hiệu và định nghĩa cơ bản

| Ký hiệu | Ý nghĩa | Đơn vị | Mối quan hệ |
|---|---|---|---|
| $\lambda$ | Tốc độ khách đến hệ thống | khách/phút | $\lambda = \bar{N}/60$ |
| $E[S]$ | Thời gian phục vụ trung bình một khách | phút | $E[S] = 1/\mu$ |
| $\mu$ | Năng suất/tốc độ phục vụ của 1 quầy | khách/phút | $\mu = 1/E[S]$ |
| $c$ | Số quầy phục vụ đang mở | quầy | Số nguyên dương ($c \ge 1$) |
| $a$ | Cường độ tải giao thông (*traffic offered*) | Erlang | $a = \frac{\lambda}{\mu} = \lambda \cdot E[S]$ |
| $\rho$ | Hệ số sử dụng trung bình mỗi quầy (*traffic intensity*) | - | $\rho = \frac{a}{c} = \frac{\lambda}{c \cdot \mu}$ |
| $W_q$ | Thời gian chờ trung bình trong hàng đợi | phút | Little: $L_q = \lambda \cdot W_q$ |
| $L_q$ | Độ dài trung bình của hàng đợi | khách | - |
| $W$ | Tổng thời gian trong hệ thống (chờ + phục vụ) | phút | $W = W_q + E[S]$ |
| $L$ | Tổng số khách trong hệ thống | khách | $L = L_q + a$ |
| $SL(t)$ | Mức cam kết dịch vụ (xác suất chờ $\le t$) | - | $P(W_q \le t)$ |

---

## 2. Mô hình $M/M/c$ (Hệ thống Erlang C)

### 2.1 Điều kiện ổn định hệ thống
Để hàng đợi không tăng vô hạn (hệ thống đạt trạng thái cân bằng dừng), **bắt buộc**:
$$\rho = \frac{\lambda}{c\mu} < 1 \iff c > a$$
Nếu $c \le a$, tốc độ khách đến lớn hơn hoặc bằng tổng công suất tối đa của các quầy, hàng đợi sẽ nổ tung ($L_q \to \infty, W_q \to \infty$).

### 2.2 Công thức xác suất phải chờ $C(c, a)$ (Erlang C)
Xác suất để một khách đến nơi gặp tất cả $c$ quầy đều đang bận và phải vào hàng chờ:
$$C(c, a) = P(\text{phải chờ}) = \frac{\frac{a^c}{c! (1 - \rho)}}{\sum_{k=0}^{c-1} \frac{a^k}{k!} + \frac{a^c}{c! (1 - \rho)}}$$

> **Mẹo tính toán tránh tràn số trong Excel:**  
> Nhân cả tử và mẫu với $e^{-a}$:
> $$C(c, a) = \frac{\frac{\text{POISSON}(c, a, \text{FALSE})}{1 - \rho}}{\frac{\text{POISSON}(c, a, \text{FALSE})}{1 - \rho} + \text{POISSON}(c-1, a, \text{TRUE})}$$

### 2.3 Các chỉ số vận hành chính
- **Thời gian chờ trung bình trong hàng:**
  $$W_q = \frac{C(c, a)}{c\mu - \lambda} = \frac{C(c, a)}{c\mu(1 - \rho)}$$
- **Độ dài hàng đợi trung bình (Định luật Little):**
  $$L_q = \lambda \cdot W_q$$
- **Hàm phân phối thời gian chờ (SLA):**
  $$P(W_q > t) = C(c, a) \cdot e^{-(c\mu - \lambda)t}$$
  $$P(W_q \le t) = 1 - C(c, a) \cdot e^{-(c\mu - \lambda)t}$$

---

## 3. Ví dụ tính tay mẫu chi tiết (Kiểm tra chéo hai thành viên)

### Đề bài ví dụ:
- Tốc độ đến: $\lambda = 1.5$ khách/phút
- Thời gian phục vụ trung bình: $E[S] = 3.0$ phút $\implies \mu = 1/3 \approx 0.3333$ khách/phút
- Tải giao thông: $a = \lambda \cdot E[S] = 1.5 \times 3.0 = 4.5$ Erlang.
- Điều kiện ổn định: $c > a \implies c \ge 5$.
- Mục tiêu SLA: $P(W_q \le 5\text{ phút}) \ge 90\%$.

---

### Trường hợp 1: Xét $c = 5$ quầy
1. **Hệ số sử dụng quầy:**
   $$\rho = \frac{a}{c} = \frac{4.5}{5} = 0.90 \quad (< 1, \text{ ổn định nhưng rất nghẽn})$$
   $$1 - \rho = 0.10$$
2. **Tổng hữu hạn $\sum_{k=0}^{4} \frac{a^k}{k!}$:**
   - $k=0: 4.5^0 / 0! = 1$
   - $k=1: 4.5^1 / 1! = 4.5$
   - $k=2: 4.5^2 / 2! = 20.25 / 2 = 10.125$
   - $k=3: 4.5^3 / 6 = 91.125 / 6 = 15.1875$
   - $k=4: 4.5^4 / 24 = 410.0625 / 24 = 17.0859$
   $$\implies \sum_{k=0}^{4} \frac{4.5^k}{k!} = 1 + 4.5 + 10.125 + 15.1875 + 17.0859 = 47.8984$$
3. **Thành phần trạng thái đầy $k=5$:**
   $$\frac{a^5}{5! (1 - \rho)} = \frac{1845.28125}{120 \times 0.10} = \frac{1845.28125}{12} = 153.7734$$
4. **Xác suất phải chờ $C(5, 4.5)$:**
   $$C(5, 4.5) = \frac{153.7734}{47.8984 + 153.7734} = \frac{153.7734}{201.6718} \approx \mathbf{0.7625} \quad (76.25\% \text{ khách phải chờ})$$
5. **Dư lượng công suất phục vụ:**
   $$c\mu - \lambda = 5 \times \frac{1}{3} - 1.5 = \frac{5}{3} - \frac{4.5}{3} = \frac{0.5}{3} = \frac{1}{6} \approx 0.1667 \text{ khách/phút}$$
6. **Thời gian chờ trung bình $W_q$:**
   $$W_q = \frac{C}{c\mu - \lambda} = \frac{0.7625}{1/6} = 0.7625 \times 6 = \mathbf{4.575 \text{ phút}} \approx 4.58 \text{ phút}$$
7. **Độ dài hàng đợi trung bình $L_q$:**
   $$L_q = \lambda \cdot W_q = 1.5 \times 4.575 = \mathbf{6.86 \text{ khách}}$$
8. **Mức cam kết dịch vụ tại $t = 5$ phút:**
   $$P(W_q \le 5) = 1 - C \cdot e^{-(c\mu - \lambda) \cdot 5} = 1 - 0.7625 \cdot e^{-(5/6)} = 1 - 0.7625 \cdot 0.4346 \approx \mathbf{0.6686} = \mathbf{66.9\%}$$
   $$\implies 66.9\% < 90\% \implies \mathbf{KHÔNG\ ĐẠT\ SLA!}$$

---

### Trường hợp 2: Tăng lên $c = 6$ quầy
1. **Hệ số sử dụng quầy:**
   $$\rho = \frac{a}{c} = \frac{4.5}{6} = 0.75 \implies 1 - \rho = 0.25$$
2. **Tổng hữu hạn $\sum_{k=0}^{5} \frac{a^k}{k!}$:**
   $$\sum_{k=0}^{5} \frac{4.5^k}{k!} = 47.8984 + \frac{4.5^5}{120} = 47.8984 + 15.3773 = 63.2757$$
3. **Thành phần trạng thái đầy $k=6$:**
   $$\frac{a^6}{6! (1 - \rho)} = \frac{4.5^6}{720 \times 0.25} = \frac{8303.7656}{180} = 46.1320$$
4. **Xác suất phải chờ $C(6, 4.5)$:**
   $$C(6, 4.5) = \frac{46.1320}{63.2757 + 46.1320} = \frac{46.1320}{109.4077} \approx \mathbf{0.4217} \quad (42.17\% \text{ khách phải chờ})$$
5. **Dư lượng công suất phục vụ:**
   $$c\mu - \lambda = 6 \times \frac{1}{3} - 1.5 = 2.0 - 1.5 = \mathbf{0.50 \text{ khách/phút}}$$
6. **Thời gian chờ trung bình $W_q$:**
   $$W_q = \frac{0.4217}{0.50} = \mathbf{0.8434 \text{ phút}} \approx 0.84 \text{ phút}$$
7. **Độ dài hàng đợi trung bình $L_q$:**
   $$L_q = 1.5 \times 0.8434 = \mathbf{1.265 \text{ khách}}$$
8. **Mức cam kết dịch vụ tại $t = 5$ phút:**
   $$P(W_q \le 5) = 1 - 0.4217 \cdot e^{-0.5 \times 5} = 1 - 0.4217 \cdot e^{-2.5} = 1 - 0.4217 \cdot 0.08208 = 1 - 0.0346 = \mathbf{0.9654} = \mathbf{96.5\%}$$
   $$\implies 96.5\% \ge 90\% \implies \mathbf{ĐẠT\ SLA!}$$

### Kết luận ví dụ:
**Số quầy tối thiểu cần mở là $c = 6$ quầy.**  
*(Kết quả này khớp hoàn toàn giữa bảng Excel `excel/erlang.xlsx`, code Python và tính tay độc lập!)*

---

## 4. Mở rộng 1: Xấp xỉ Allen - Cunneen cho mô hình $M/G/c$

Trong thực tế ngân hàng, thời gian phục vụ $S$ thường có độ lệch chuẩn $\sigma_S > E[S]$ (tức hệ số biến thiên $cv > 1, cs^2 > 1$). Công thức xấp xỉ Allen - Cunneen hiệu chỉnh thời gian chờ như sau:
$$W_q(M/G/c) \approx \frac{c_a^2 + c_s^2}{2} \cdot W_q(M/M/c)$$
Với dòng đến Poisson thì $c_a^2 = 1$, do đó:
$$W_q(M/G/c) \approx \frac{1 + c_s^2}{2} \cdot W_q(M/M/c)$$
- Nếu $c_s^2 = 1.20$ (số liệu thực tế từ `September1999.txt`): thời gian chờ tăng $\frac{1 + 1.20}{2} = 1.10$ lần (+10%).
- Nếu $c_s^2 = 0.5$ (dịch vụ đồng đều hơn phân phối mũ): thời gian chờ giảm còn $\frac{1 + 0.5}{2} = 0.75$ lần (-25%).

---

## 5. Mở rộng 2: Mô hình có khách bỏ về $M/M/c + M$ (Erlang-A)

Khi khách chờ quá lâu, họ có xu hướng rời hàng với thời gian kiên nhẫn tuân theo phân phối mũ tham số $\theta$. Hệ thống chuyển thành chuỗi sinh tử dừng với tốc độ chuyển dời:
- Trạng thái $n \le c$: tốc độ phục vụ $n\mu$, không ai bỏ về.
- Trạng thái $n > c$: $c$ quầy phục vụ với tốc độ $c\mu$, và $n - c$ khách trong hàng bỏ về với tốc độ $(n - c)\theta$. Tổng tốc độ thoát:
  $$d_n = c\mu + (n - c)\theta$$
Phân phối xác suất dừng:
$$\pi_n = \pi_{n-1} \cdot \frac{\lambda}{\min(n, c)\mu + \max(n - c, 0)\theta}$$
Khách bỏ về làm giảm tải cho hàng đợi, do đó $W_q$ thực tế của người được phục vụ thường thấp hơn một chút so với mô hình Erlang C thuần túy, nhưng bù lại xuất hiện tỉ lệ mất khách ($P(\text{bỏ về}) = \frac{\theta L_q}{\lambda}$).

---

## 6. Phương pháp SIPP cho hệ thống biến thiên theo giờ

Do $\lambda$ thay đổi mạnh theo từng khung giờ (từ 1.02 khách/phút lúc 8h lên 1.64 khách/phút lúc 10h), phương pháp SIPP (*Stationary Independent Period-by-Period*) giải bài toán Erlang C độc lập cho từng giờ $h$ để tìm $c_h$ ban đầu:
$$c_h = \min \{ c \in \mathbb{N} \mid P(W_q \le 5 \mid \lambda_h, \mu) \ge 90\% \}$$

**Giới hạn của SIPP:** SIPP giả định hệ thống đạt trạng thái dừng ngay lập tức tại mỗi đầu giờ và bỏ qua khách tồn từ giờ trước truyền sang giờ sau. Vì vậy, sang Tuần 2, mô phỏng SimPy sẽ được dùng để hiệu chỉnh quán tính này.
