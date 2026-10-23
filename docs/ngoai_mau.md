# Báo cáo Đánh giá Ngoài mẫu trên Tập Kiểm tra (Out-of-Sample Validation)

**Người phụ trách:** Thành viên A  
**Ngày cập nhật:** 23/10/2026  
**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu  

---

## 1. Mục tiêu và Phương pháp luận

Đánh giá ngoài mẫu (*Out-of-sample test*) nhằm kiểm tra độ vững chắc của chính sách định biên quầy tối ưu được rút ra từ tập huấn luyện (Train: 10 ngày đầu, 6.867 khách) khi áp dụng vào tập kiểm tra độc lập (Test: 4 ngày sau, 2.969 khách).

### Đặc điểm dòng khách tập Test:
Tập Test có lưu lượng khách bình quân cao hơn tập Train (+8.1% toàn ngày, từ 686.7 lên 742.3 khách/ngày). Đặc biệt vào khung giờ sáng:
- Giờ 8h–9h: $\lambda$ tăng **+10.3%**
- Giờ 9h–10h: $\lambda$ tăng **+14.4%**
- Giờ 10h–11h: $\lambda$ tăng **+24.9%** (từ 1.535 lên 1.917 khách/phút)
- Giờ 11h–12h: $\lambda$ tăng **+12.4%**

---

## 2. Đặc tả Tham số cho 2 Phiên bản Mô phỏng Ngoài mẫu

Để đảm bảo tính minh bạch và công bằng khoa học, báo cáo thiết lập 2 kịch bản mô phỏng đối chiếu:

| Thuộc tính mô phỏng | Phiên bản A (Tham số Train + $\lambda_{\text{test}}$) | Phiên bản B (Toàn bộ Tham số Test) | Ghi chú kỹ thuật |
|---|---|---|---|
| **Tốc độ đến ($\lambda_h$)** | Ước lượng từ 4 ngày Test | Ước lượng từ 4 ngày Test | Thể hiện đúng áp lực khách đến của ngày Test |
| **Phân phối phục vụ** | $\text{Gamma}(k=1.0955, \theta=2.6688)$ | $\text{Gamma}(k=1.1245, \theta=2.5830)$ | Phiên bản A giữ nguyên mô hình từ Train |
| **Kỳ vọng phục vụ ($E[S]$)** | $2.9236$ phút | $2.9046$ phút | Kiểm định KS 2 mẫu: $p = 0.457 \implies$ không khác biệt |
| **Tốc độ bỏ về ($\theta$)** | $0.1087$ phút$^{-1}$ (kiên nhẫn 9.20p) | $0.1162$ phút$^{-1}$ (kiên nhẫn 8.61p) | MLE trên từng tập |
| **Tỉ lệ khách VIP ($p_{\text{vip}}$)** | $35.43\%$ | $30.21\%$ | Tỉ lệ thực tế trên từng tập |
| **Lịch quầy áp dụng** | $\mathbf{c}^* = [4, 5, 6, 5, 5, 5, 5, 5, 4]$ (44 q-h) | $\mathbf{c}^* = [4, 5, 6, 5, 5, 5, 5, 5, 4]$ (44 q-h) | Lịch tối ưu khuyến nghị |
| **Số lần lặp (Replications)** | 200 lần lặp | 200 lần lặp | Đảm bảo khoảng tin cậy hẹp |
| **Hạt giống ngẫu nhiên** | `seed_base = 40000` | `seed_base = 41000` | Phục vụ tái lập 100% |

---

## 3. Bảng Kết quả So sánh Chi tiết theo Khung giờ

Dưới đây là bảng đối chiếu giữa kết quả mô phỏng (Phiên bản A và B) và thực tế quan sát trong nhật ký dữ liệu:

| Khung giờ | Số quầy | $\lambda_{\text{train}}$ | $\lambda_{\text{test}}$ | Chênh lệch $\lambda$ | $SL_{\text{mô phỏng A}}$ (Low CI95) | $SL_{\text{mô phỏng B}}$ (Low CI95) | $SL_{\text{quan sát thực}}$ | Chênh lệch (A - Thực) | Chênh lệch (B - Thực) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h - 9h** | 4 | 0.9900 | 1.0917 | +10.3% | 0.9364 [0.9286] | 0.9405 [0.9329] | 0.9809 | -0.0445 | -0.0404 |
| **9h - 10h** | 5 | 1.3767 | 1.5750 | +14.4% | 0.9172 [0.9082] | 0.9234 [0.9148] | 0.9735 | -0.0563 | -0.0501 |
| **10h - 11h** | 6 | 1.5350 | 1.9167 | +24.9% | 0.9169 [0.9076] | 0.9248 [0.9161] | 0.9283 | -0.0114 | -0.0035 |
| **11h - 12h** | 5 | 1.3900 | 1.5625 | +12.4% | 0.8993 [0.8888] | 0.9084 [0.8985] | 0.9413 | -0.0420 | -0.0329 |
| **12h - 13h** | 5 | 1.2400 | 1.2375 | -0.2% | 0.9552 [0.9487] | 0.9589 [0.9528] | 0.9865 | -0.0313 | -0.0276 |
| **13h - 14h** | 5 | 1.2017 | 1.3458 | +12.0% | 0.9457 [0.9387] | 0.9501 [0.9434] | 0.9443 | +0.0014 | +0.0058 |
| **14h - 15h** | 5 | 1.3383 | 1.2792 | -4.4% | 0.9439 [0.9363] | 0.9472 [0.9400] | 0.8958 | +0.0481 | +0.0514 |
| **15h - 16h** | 5 | 1.3167 | 1.2750 | -3.2% | 0.9507 [0.9432] | 0.9546 [0.9473] | **0.7647** | **+0.1860** | **+0.1899** |
| **16h - 17h** | 4 | 1.0567 | 1.0875 | +2.9% | 0.9245 [0.9159] | 0.9304 [0.9221] | 0.9387 | -0.0142 | -0.0083 |
| **TOÀN NGÀY** | **44 q-h** | **1.2720** | **1.3744** | **+8.1%** | **0.9140** | **0.9293** | **0.9286** | **-0.0146** | **+0.0007** |

---

## 4. Phân tích Khoa học và Nhận xét Giới hạn

### 4.1 Vấn đề so sánh không cùng điều kiện (Non-identical Conditions)
> [!WARNING]
> Cột *$SL_{\text{quan sát thực}}$* diễn ra dưới **nhân sự thực tế của ngân hàng** vào các ngày trong tháng 9/1999 (dữ liệu thô không ghi nhận số quầy hoạt động cụ thể ở từng giờ mà chỉ có bản ghi giao dịch).  
> Ngược lại, cột mô phỏng chạy dưới **lịch khuyến nghị 44 quầy-giờ**.  
> Do đó, việc so sánh trực tiếp theo từng giờ **không phải là kiểm chứng cùng điều kiện nhân sự**, mà chỉ mang ý nghĩa đối chiếu tham khảo về mức độ tương thích vĩ mô.

### 4.2 Giải thích độ lệch lớn tại khung giờ 15h–16h (+18.6%)
- Trong thực tế, $SL_{\text{quan sát}}$ lúc 15h–16h giảm sâu xuống **76.47%** (và tỉ lệ bỏ về thực tế vọt lên **15.03%**).
- Trong mô phỏng, với 5 quầy phục vụ liên tục, mô phỏng dự báo $SL \approx 95.1\%$.
- **Nguyên nhân khả dĩ:**
  1. *Nhân sự thực bị thiếu hụt:* Thực tế tại chi nhánh ngân hàng lúc 15h–16h có thể giao dịch viên phải chốt sổ cuối ngày, xử lý chứng từ tồn đọng hoặc số quầy mở thực tế ít hơn 5 quầy.
  2. *Tích lũy trễ (Queue spillover):* Các đợt khách dồn ứ từ khung giờ 14h kéo dài sang khiến hàng đợi thực tế bị nghẽn cục bộ.
  3. *Tỉ lệ VIP vọt lên đỉnh:* Khung giờ 15h–16h ghi nhận tỉ lệ khách VIP cao nhất ngày (52.15%), đẩy thời gian chờ của khách thường lên cao trong thực tế.

### 4.3 Khả năng đáp ứng SLA của Lịch 44 trước Nhu cầu Tập Test
- Dưới lưu lượng khách cao hơn của tập Test (+8.1%), $SL$ toàn ngày của lịch 44 vẫn duy trì được **91.40%** (phiên bản A) và **92.93%** (phiên bản B).
- Tuy nhiên, tại khung giờ cao điểm **11h–12h**, cận dưới khoảng tin cậy của $SL$ rơi xuống **88.88% < 90%** (ở phiên bản A).
- **Kết luận vận hành:** Điều này chứng minh rằng **lịch tối ưu 44 quầy-giờ chỉ đảm bảo SLA cho các ngày có lưu lượng trung bình**. Trong các ngày có lưu lượng khách gia tăng từ 8–10% trở lên (như các ngày trong tập Test), ngân hàng cần **kích hoạt phương án lịch bền vững 48 quầy-giờ** để đảm bảo SLA cho mọi khung giờ.
