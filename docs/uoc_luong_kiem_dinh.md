# Báo cáo Ước lượng và Kiểm định Phân phối Thống kê (Tuần 2)

**Người phụ trách:** Thành viên A  
**Ngày cập nhật:** 21/10/2026  
**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu  

---

## 1. Dữ liệu thực nghiệm và Phân chia Tập dữ liệu

- **Nguồn dữ liệu:** Bộ dữ liệu chuẩn *Anonymous Bank* (Technion SEE Center), gồm các cuộc gọi giao dịch thường nhật tại quầy ngân hàng (`PS`), khung giờ 8:00 – 17:00 trên 14 ngày làm việc tiêu chuẩn tháng 9/1999.
- **Tổng số quan sát:** 9.836 khách hàng.
- **Phương pháp phân chia:** Phân chia theo **đơn vị ngày** (không chia ngẫu nhiên từng khách để bảo toàn trọn vẹn đặc tính tương quan chuỗi thời gian trong ngày):
  - **Tập ước lượng (Train - 70%):** 10 ngày làm việc đầu tiên (`990901` đến `990915`), gồm **6.867 bản ghi**. Dùng để ước lượng mọi tham số hệ thống.
  - **Tập kiểm tra (Test - 30%):** 4 ngày làm việc độc lập còn lại (`990916` đến `990923`), gồm **2.969 bản ghi**. Dùng để đánh giá ngoài mẫu (*out-of-sample validation*).

---

## 2. Quá trình khách đến và Kiểm định Poisson theo giờ

### 2.1 Tốc độ đến theo từng khung giờ ($\lambda_h$)
Ước lượng $\lambda_h = \frac{\bar{N}_h}{60}$ (khách/phút) kèm khoảng tin cậy 95% ($CI_{95} = \lambda_h \pm 1.96 \cdot \frac{\sqrt{\bar{N}_h / n_{\text{ngày}}}}{60}$):

| Khung giờ ($h$) | Số khách TB/ngày ($\bar{N}_h$) | Tốc độ đến $\lambda_h$ (khách/phút) | Khoảng tin cậy 95% | Chỉ số phân tán $D_h$ | $p$-value Poisson | Kết luận |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 8h - 9h ($h=0$) | 59.40 | **0.9900** | [0.9104, 1.0696] | 18.25 | 0.0323 | Chưa bác bỏ |
| 9h - 10h ($h=1$) | 82.60 | **1.3767** | [1.2828, 1.4706] | 18.42 | 0.0305 | Chưa bác bỏ |
| 10h - 11h ($h=2$) | 92.10 | **1.5350** | [1.4359, 1.6341] | 32.14 | 0.0002 | Lệch nhẹ cao điểm |
| 11h - 12h ($h=3$) | 83.40 | **1.3900** | [1.2957, 1.4843] | 28.51 | 0.0008 | Lệch nhẹ cao điểm |
| 12h - 13h ($h=4$) | 74.40 | **1.2400** | [1.1509, 1.3291] | 14.88 | 0.0943 | Khớp tốt Poisson |
| 13h - 14h ($h=5$) | 72.10 | **1.2017** | [1.1140, 1.2894] | 22.15 | 0.0084 | Lệch nhẹ |
| 14h - 15h ($h=6$) | 80.30 | **1.3383** | [1.2457, 1.4309] | 26.40 | 0.0018 | Lệch nhẹ |
| 15h - 16h ($h=7$) | 79.00 | **1.3167** | [1.2249, 1.4085] | 23.50 | 0.0052 | Lệch nhẹ |
| 16h - 17h ($h=8$) | 63.40 | **1.0567** | [0.9744, 1.1390] | 20.12 | 0.0172 | Chưa bác bỏ |

### 2.2 Kiểm định giả thuyết tốc độ đến không đổi (Homogeneous Poisson Test)
- Giả thuyết $H_0$: Tốc độ khách đến là như nhau giữa tất cả các khung giờ trong ngày ($\lambda_0 = \lambda_1 = \dots = \lambda_8$).
- Tiêu chuẩn kiểm định: $\chi^2 = \sum_{h=0}^8 \frac{(T_h - \bar{T})^2}{\bar{T}} = 127.84$ với bậc tự do $df = 8$.
- Giá trị $p$-value: $p = 7.42 \times 10^{-24} < 10^{-5} \implies$ **Bác bỏ triệt để giả thuyết $H_0$**.
- **Ý nghĩa thực tiễn:** Tốc độ khách đến dao động rất mạnh trong ngày (đạt đỉnh vào 10h–11h sáng và giảm mạnh sau 16h). Mô hình quản lý hàng đợi bắt buộc phải điều chỉnh số quầy theo từng khung giờ (SIPP/Dynamic staffing), không thể dùng một số quầy cố định.

---

## 3. Phân phối Thời gian Phục vụ (Service Time)

### 3.1 Thống kê mô tả
- Số lượng khách phục vụ thành công: 6.388 lượt.
- Thời gian phục vụ trung bình: $E[S] = 2.92$ phút ($\approx 175.4$ giây).
- Độ lệch chuẩn: $\sigma_S = 3.21$ phút.
- Hệ số biến thiên: $cv = \frac{\sigma}{E[S]} = 1.0963 \implies cs^2 = 1.2018$.
- Do $cv > 1.0$, phân phối thời gian phục vụ thực tế có độ biến thiên cao hơn và đuôi dài hơn so với phân phối mũ thuần túy ($cv = 1.0$).

### 3.2 So sánh các mô hình phân phối liên tục (cố định $loc = 0$)

| Phân phối | Số tham số | Giá trị AIC | Thống kê KS | $p$-value KS | Đánh giá & Xếp hạng |
|---|:---:|:---:|:---:|:---:|:---|
| **Gamma** | 2 | **26.314,2** | **0.0762** | $< 10^{-6}$ | **Khớp tốt nhất (Hạng 1)** |
| **Weibull** | 2 | 26.335,8 | 0.0828 | $< 10^{-6}$ | Khớp khá tốt (Hạng 2) |
| **Exponential** | 1 | 26.340,1 | 0.0915 | $< 10^{-6}$ | Đuôi ngắn, đánh giá thấp rủi ro |
| **Lognormal** | 2 | 27.580,4 | 0.1241 | $< 10^{-6}$ | Sai lệch ở vùng thời gian ngắn |

> **Lưu ý phương pháp luận về kiểm định KS:**  
> Do các tham số được ước lượng trực tiếp từ chính mẫu dữ liệu (*estimated parameters*), $p$-value của kiểm định Kolmogorov-Smirnov có xu hướng khắt khe với cỡ mẫu lớn ($N > 6.000$). Tiêu chuẩn lựa chọn mô hình dựa trên sự kết hợp giữa **chỉ số AIC nhỏ nhất** và kiểm tra trực quan trên **Q-Q plot** (Xem hình [`fig_a_fit.png`](file:///d:/KHDV/fig_a_fit.png)).

**Quyết định lựa chọn mô hình phục vụ:**
Nhóm lựa chọn phân phối **Gamma** với tham số $\text{shape} (k) = 1.0955$, $\text{scale} (\theta) = 2.6688$ làm mô hình phục vụ chính trong mô phỏng SimPy.

---

## 4. Hành vi Khách hàng Bỏ về (Abandonment Behavior)

Dữ liệu thời gian chờ của khách hàng là dữ liệu bị kiểm duyệt (*censored data*):
- Khách được phục vụ cho biết: $\text{Kiên nhẫn} \ge \text{Thời gian chờ thực tế}$.
- Khách bỏ về cho biết: $\text{Kiên nhẫn} = \text{Thời gian chờ thực tế}$.

Áp dụng phương pháp ước lượng hợp lý cực đại (MLE) cho phân phối mũ:
$$\hat{\theta} = \frac{\text{Số khách bỏ về}}{\text{Tổng thời gian chờ của TẤT CẢ khách đến}} = \frac{479}{4.406,6 \text{ phút}} = \mathbf{0.1087\ \text{khách/phút}}$$
- Khoảng tin cậy 95%: $\hat{\theta} \pm 1.96 \cdot \frac{\hat{\theta}}{\sqrt{479}} = [0.0994,\ 0.1180]$.
- **Thời gian kiên nhẫn trung bình:** $\frac{1}{\hat{\theta}} = \mathbf{9.20\ \text{phút}}$ (Khách hàng sẵn sàng chờ trung bình khoảng 9 phút 12 giây trước khi bỏ cuộc).
- Tỉ lệ bỏ về trên tập ước lượng: $479 / 6.867 = \mathbf{6.98\%}$.

---

## 5. Khách hàng Ưu tiên (VIP)

- Tỉ lệ khách VIP trung bình: $p_{\text{vip}} = \mathbf{35.43\%}$ ($CI_{95}: [34.30\%,\ 36.56\%]$).
- Tỉ lệ khách VIP tăng cao vào giờ cao điểm buổi sáng (hơn 40% lúc 10h–11h).

---

## 6. Bàn giao Tập số liệu Quan sát trên Tập Kiểm tra (Test Set)

Để phục vụ kiểm chứng ngoài mẫu (*out-of-sample*) của Thành viên C ở Tuần 2:
- Tổng số khách trong 4 ngày kiểm tra: 2.969 khách (trung bình 742 khách/ngày).
- Tỉ lệ bỏ về thực tế quan sát được: $7.54\%$.
- Thời gian chờ trung bình thực tế: $W_q = 0.95$ phút.
- Tỉ lệ khách chờ $\le 5$ phút thực tế: $93.1\%$.
