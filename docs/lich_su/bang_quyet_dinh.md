# Báo cáo Bảng Quyết định Số quầy và Phân tích Độ nhạy Lý thuyết (Tuần 2)

**Người phụ trách:** Thành viên B  
**Ngày cập nhật:** 21/10/2026  
**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu  

---

## 1. Bảng Quyết định Số quầy theo Khung giờ (SIPP Hoàn chỉnh)

Sử dụng bộ tham số chính thức từ [`docs/params.json`](file:///d:/KHDV/docs/params.json) (ước lượng trên tập train):
- Thời gian phục vụ trung bình: $E[S] = 2.9236$ phút ($\mu = 0.3420$ khách/phút).
- Tốc độ bỏ về: $\theta = 0.1087$ (1/phút) $\implies$ Kiên nhẫn trung bình = $9.20$ phút.
- Hệ số biến thiên thời gian phục vụ: $cs^2 = 1.2018$.
- Cam kết dịch vụ SLA: $P(W_q \le 5.0\text{ phút}) \ge 90.0\%$.

| Khung giờ | $\lambda_h$ (khách/p) | Tải $a$ (Erlang) | $c_{\min}$ ổn định | Số quầy Erlang C | $\rho$ (Erlang C) | SL Erlang C | Số quầy Erlang-A | Tỉ lệ bỏ về $p_{ab}$ | SL Erlang-A | $W_q$ dự kiến (phút) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h - 9h** | 0.9900 | 2.89 | 3 | **4** | 72.4% | 93.0% | **4** | 4.8% | **93.6%** | 0.53 |
| **9h - 10h** | 1.3767 | 4.02 | 5 | **6** | 67.1% | 99.0% | **5** | 4.7% | **93.1%** | 0.59 |
| **10h - 11h** | 1.5350 | 4.49 | 5 | **6** | 74.8% | 96.9% | **6** | 3.4% | **95.8%** | 0.38 |
| **11h - 12h** | 1.3900 | 4.06 | 5 | **6** | 67.7% | 98.9% | **5** | 4.8% | **92.8%** | 0.61 |
| **12h - 13h** | 1.2400 | 3.63 | 4 | **5** | 72.5% | 96.0% | **5** | 3.7% | **95.2%** | 0.42 |
| **13h - 14h** | 1.2017 | 3.51 | 4 | **5** | 70.3% | 97.0% | **5** | 3.3% | **95.7%** | 0.37 |
| **14h - 15h** | 1.3383 | 3.91 | 4 | **5** | 78.3% | 91.9% | **5** | 4.4% | **93.7%** | 0.54 |
| **15h - 16h** | 1.3167 | 3.85 | 4 | **5** | 77.0% | 93.0% | **5** | 4.2% | **94.1%** | 0.51 |
| **16h - 17h** | 1.0567 | 3.09 | 4 | **5** | 61.8% | 99.0% | **4** | 5.8% | **92.2%** | 0.64 |
| **TỔNG CỘNG** | - | - | - | **47 quầy-giờ** | 71.3% | **96.1%** | **44 quầy-giờ** | **4.4%** | **94.0%** | **0.51** |

---

## 2. So sánh các Chính sách Lịch quầy Lý thuyết

| Chính sách | Lịch quầy chi tiết (8h $\to$ 16h) | Tổng quầy-giờ | Tiết kiệm chi phí | Mức SLA giờ thấp nhất | Đánh giá tổng thể |
|---|:---:|:---:|:---:|:---:|---|
| **1. Hằng số (Constant)** | `[6, 6, 6, 6, 6, 6, 6, 6, 6]` | **54** | Chuẩn (0%) | 96.9% | Lãng phí lớn ở giờ thấp điểm (8h và 16h) |
| **2. SIPP Erlang C** | `[4, 6, 6, 6, 5, 5, 5, 5, 5]` | **47** | **-13.0%** | 91.9% | Tiết kiệm 7 quầy-giờ, đáp ứng tốt SLA |
| **3. SIPP Erlang-A** | `[4, 5, 6, 5, 5, 5, 5, 5, 4]` | **44** | **-18.5%** | 92.2% | Tiết kiệm 10 quầy-giờ, tối ưu hóa triệt để |

> **Nhận xét lý thuyết quan trọng:**
> - Mô hình **Erlang C** giả định khách kiên nhẫn vô hạn (không bao giờ bỏ về). Do đó hàng đợi bị dồn ứ ảo, dẫn đến yêu cầu nhiều quầy hơn (**47 quầy-giờ** so với 44 của Erlang-A).
> - Mô hình **Erlang-A** tính đến hành vi thực tế của khách hàng (bỏ về khi chờ quá lâu với tốc độ $\theta$), giúp giải phóng bớt áp lực hàng đợi tại các khung giờ cận biên, giảm bớt 1 quầy ở các giờ 9h, 11h và 16h mà vẫn bảo đảm $\ge 92.2\%$ khách được phục vụ trong vòng 5 phút.

---

## 3. Phân tích Độ nhạy Lý thuyết (Theoretical Sensitivity Analysis)

Kiểm tra độ bền vững của lịch quầy tối ưu Erlang-A (`[4, 5, 6, 5, 5, 5, 5, 5, 4]`) trước các biến động của môi trường thực tế:

### 3.1 Biến động nhu cầu khách đến ($\lambda$)
| Mức nhu cầu ($\lambda$) | Tỉ lệ SLA trung bình ngày | SLA giờ thấp nhất | Thời gian chờ TB tối đa | Tỉ lệ bỏ về $p_{ab}$ | Đánh giá |
|:---:|:---:|:---:|:---:|:---:|:---:|
| $\times 0.9$ (-10%) | 95.9% | 94.4% | 0.47 phút | 3.9% | Rất an toàn |
| **$\times 1.0$ (Cơ sở)** | **94.0%** | **92.2%** | **0.64 phút** | **5.5%** | **Đạt SLA (Chuẩn)** |
| $\times 1.1$ (+10%) | 91.7% | 89.5% | 0.84 phút | 7.5% | **Vi phạm SLA nhẹ ở giờ 16h** |
| $\times 1.2$ (+20%) | 88.8% | 86.3% | 1.09 phút | 9.9% | Vi phạm SLA toàn diện |
| $\times 1.3$ (+30%) | 85.4% | 82.3% | 1.38 phút | 12.6% | Nghẽn nghiêm trọng |

### 3.2 Biến động thời gian phục vụ ($E[S]$)
- Khi nhân viên thao tác chậm hơn do hệ thống CNTT chập chờn ($E[S]$ tăng $+10\%$ lên 3.22 phút): SLA giờ thấp nhất giảm từ $92.2\% \to 88.8\%$ (vi phạm SLA).
- Khi $E[S]$ tăng $+20\%$ lên 3.51 phút: SLA giờ thấp nhất tụt dốc xuống $84.7\%$.

### 3.3 Biến động độ kiên nhẫn của khách hàng ($\theta$)
- Nếu khách kiên nhẫn hơn gấp đôi ($\theta \times 0.5$, kiên nhẫn 18.4 phút): SLA đạt $92.8\%$, tỉ lệ bỏ về giảm còn $3.7\%$.
- Nếu khách mất kiên nhẫn hơn ($\theta \times 1.5$, kiên nhẫn 6.1 phút): SLA đạt $91.2\%$, tỉ lệ bỏ về tăng lên $6.8\%$.

### Kết luận khuyến nghị:
Lịch tối ưu Erlang-A là lịch **"tối thiểu hóa chi phí"** nên biên dự phòng rất mỏng. Nhóm đề xuất phương án **Lịch bền vững (Robust Schedule)** cho ngân hàng: mở thêm 1 quầy dự phòng ở khung giờ 16h (thành `[4, 5, 6, 5, 5, 5, 5, 5, 5]`, tổng 45 quầy-giờ), giúp hệ thống an toàn chịu được biến động nhu cầu tăng $+10\%$ mà chi phí chỉ tăng vỏn vẹn 1 quầy-giờ/ngày.
