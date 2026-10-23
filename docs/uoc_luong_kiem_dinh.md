# Báo cáo Ước lượng và Kiểm định Phân phối Thống kê (Phiên bản Hiệu chỉnh v2.0)

**Người phụ trách:** Thành viên A  
**Ngày cập nhật:** 23/10/2026  
**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu  

---

## 1. Dữ liệu thực nghiệm và Phân chia Tập dữ liệu

- **Nguồn dữ liệu:** Bộ dữ liệu chuẩn *Anonymous Bank* (Technion SEE Center), gồm các cuộc gọi giao dịch thường nhật tại quầy ngân hàng (`PS`), khung giờ 8:00 – 17:00 trên 14 ngày làm việc tiêu chuẩn tháng 9/1999.
- **Tổng số quan sát:** 9.836 khách hàng.
- **Phương pháp phân chia:** Phân chia theo **đơn vị ngày** (không chia ngẫu nhiên từng khách để bảo toàn trọn vẹn đặc tính tương quan chuỗi thời gian trong ngày):
  - **Tập ước lượng (Train - 70%):** 10 ngày làm việc đầu tiên (`990901` đến `990915`), gồm **6.867 bản ghi**. Dùng để ước lượng mọi tham số hệ thống cho mô hình mô phỏng.
  - **Tập kiểm tra (Test - 30%):** 4 ngày làm việc độc lập còn lại (`990916` đến `990923`), gồm **2.969 bản ghi**. Dùng để đánh giá ngoài mẫu (*out-of-sample validation*).

---

## 2. Quá trình khách đến và Kiểm định Poisson theo giờ

### 2.1 Tốc độ đến theo từng khung giờ và Kiểm định Poisson (Toàn bộ 14 ngày)

Quy tắc gắn nhãn kiểm định Poisson với độ tự do $df = 13$ ($n_{\text{ngày}} = 14$):
- $p < 0.01$: **Bác bỏ (mạnh)**
- $0.01 \le p < 0.05$: **Bác bỏ (nhẹ)**
- $p \ge 0.05$: **Chưa bác bỏ** (chấp nhận $H_0$ ở mức ý nghĩa 5%)

| Khung giờ ($h$) | Số khách TB/ngày ($\bar{N}_h$) | Tốc độ đến $\lambda_h$ (khách/phút) | Khoảng tin cậy 95% | Chỉ số phân tán $D_h$ | $p$-value Poisson | Kết luận Poisson ($\alpha=0.05$) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 8h - 9h ($h=0$) | 61.14 | **1.0190** | [0.9508, 1.0873] | 23.55 | 0.0356 | **Bác bỏ (nhẹ)** |
| 9h - 10h ($h=1$) | 86.00 | **1.4333** | [1.3524, 1.5143] | 23.58 | 0.0352 | **Bác bỏ (nhẹ)** |
| 10h - 11h ($h=2$) | 98.64 | **1.6440** | [1.5573, 1.7308] | 48.77 | 0.0000 | **Bác bỏ (mạnh)** |
| 11h - 12h ($h=3$) | 86.36 | **1.4393** | [1.3582, 1.5204] | 39.15 | 0.0002 | **Bác bỏ (mạnh)** |
| 12h - 13h ($h=4$) | 74.36 | **1.2393** | [1.1640, 1.3146] | 20.83 | 0.0763 | **Chưa bác bỏ** |
| 13h - 14h ($h=5$) | 74.57 | **1.2429** | [1.1675, 1.3182] | 30.73 | 0.0037 | **Bác bỏ (mạnh)** |
| 14h - 15h ($h=6$) | 79.29 | **1.3214** | [1.2437, 1.3992] | 38.08 | 0.0003 | **Bác bỏ (mạnh)** |
| 15h - 16h ($h=7$) | 78.29 | **1.3048** | [1.2275, 1.3820] | 33.61 | 0.0014 | **Bác bỏ (mạnh)** |
| 16h - 17h ($h=8$) | 63.93 | **1.0655** | [0.9957, 1.1353] | 26.61 | 0.0141 | **Bác bỏ (nhẹ)** |

> [!IMPORTANT]
> **Nhận xét quan trọng về kiểm định Poisson:**
> - Ở mức ý nghĩa $\alpha = 0.05$, có tới **8/9 khung giờ bị bác bỏ giả thuyết Poisson** (trong đó 5/9 giờ bị bác bỏ mạnh ở mức 1%). Chỉ duy nhất khung giờ 12h–13h ($p = 0.0763$) là chưa bác bỏ.
> - Do đó, giả định *"Dòng khách đến tuân theo tiến trình Poisson thuần túy với $\lambda_h$ cố định"* **không hoàn toàn chính xác trong thực tế**.
> - Hệ quả: Mô phỏng chỉ dùng Poisson thuần túy có thể **đánh giá cao mức độ dịch vụ (SLA)** do chưa tính đến hiện tượng gom cụm (*burstiness*) và biến động lưu lượng giữa các ngày.

---

### 2.2 Thống kê Quá Phân Tán theo Ngày (Overdispersion Analysis)

Tổng số khách mỗi ngày trong 14 ngày làm việc chuẩn:
$$[690, 776, 826, 634, 580, 600, 539, 820, 715, 687, 740, 748, 753, 728]$$

Các chỉ số thống kê quá phân tán:
- **Số ngày quan sát:** $n = 14$ ngày.
- **Số khách trung bình mỗi ngày ($\mu$):** $702.6$ khách/ngày.
- **Phương sai thực tế ($\sigma^2$):** $7.591,8$.
- **Độ lệch chuẩn thực tế ($\sigma$):** $87.1$ khách.
- **Độ lệch chuẩn theo phân phối Poisson thuần ($\sqrt{\mu}$):** $26.5$ khách.
- **Tỉ số Phương sai / Trung bình ($\text{Var}/\text{Mean}$):** $10.8 \gg 1$.
- **Hệ số biến thiên thực tế ($CV_{\text{ngày}}$):** $12.4\%$.
- **Kiểm định quá phân tán cho tổng ngày:**
  $$D = \sum_{d=1}^{14} \frac{(N_d - \mu)^2}{\mu} = 140.4 \implies p\text{-value} = 3.65 \times 10^{-23} \ll 0.01 \implies \text{\textbf{Bác bỏ triệt để Poisson}}.$$
- **Ước lượng $CV_{\text{ngày}}$ sau khi trừ nhiễu Poisson:**
  $$CV_{\text{ngày}}^2 = \frac{\text{Var}(N_d) - \mu}{\mu^2} = \frac{7591.8 - 702.6}{702.6^2} = 0.0139 \implies CV_{\text{ngày}} \approx 11.8\%.$$

**Hệ quả mô hình hóa:**  
Trong phiên bản hiệu chỉnh v2.0, mô hình bổ sung hệ số nhân ngày $m_d \sim \text{Gamma}(\text{shape}=1/CV^2, \text{scale}=CV^2)$ với $CV = 11.8\%$ vào động cơ SimPy để đánh giá độ bền vững thực tế của các chính sách định biên.

---

## 3. Phân phối Thời gian Phục vụ (Service Time)

### 3.1 Thống kê mô tả (Tập Train 10 ngày)
- Số lượng khách phục vụ thành công: 6.388 lượt.
- Thời gian phục vụ trung bình: $E[S] = 2.9236$ phút ($\approx 175.4$ giây).
- Độ lệch chuẩn: $\sigma_S = 3.2051$ phút.
- Hệ số biến thiên: $cv = \frac{\sigma}{E[S]} = 1.0963 \implies cs^2 = 1.2018$.
- Phân phối Gamma khớp tốt nhất theo chỉ số AIC ($26.314,2$), với tham số $\text{shape} = 1.0955$, $\text{scale} = 2.6688$.

---

## 4. Hành vi Khách hàng Bỏ về (Abandonment Behavior)

Ước lượng hợp lý cực đại (MLE) trên tập Train 10 ngày:
$$\hat{\theta} = \frac{479}{4.406,6 \text{ phút}} = \mathbf{0.1087\ \text{khách/phút}} \implies \text{Thời gian kiên nhẫn TB } \frac{1}{\hat{\theta}} = \mathbf{9.20\ \text{phút}}.$$

---

## 5. Khách hàng Ưu tiên (VIP)

- Tỉ lệ khách VIP trung bình: $p_{\text{vip}} = 35.43\%$ trên tập Train (33.85% trên toàn bộ 14 ngày).
- Tỉ lệ VIP biến thiên mạnh theo giờ: từ 18.35% (8h–9h) lên đến 52.15% (15h–16h).
