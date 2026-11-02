# Báo cáo Đánh giá Ngoài mẫu trên Tập Kiểm tra (Out-of-Sample Validation)

**Người phụ trách:** Thành viên A  
**Ngày cập nhật:** 30/10/2026 (số liệu V4, giữ nguyên ở V5; `results/final_v5/`)  
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

## 2. Phương pháp (V4, `results/final_v5/ngoai_mau.csv`)

| Thuộc tính | Giá trị |
|---|---|
| **Lịch đánh giá** | Lịch tối ưu V4 `[4, 5, 6, 5, 5, 5, 5, 5, 5]` (45 q-h) |
| **Tham số mô phỏng** | Toàn bộ từ tập train: $\lambda_h$ train, phục vụ thực nghiệm (6.346 mẫu, $cs^2 = 1.20$), $\theta = 0.1087$, $p_{vip} = 0.3543$ |
| **Biến động ngày** | Hệ số nhân ngày $m_d \sim$ Gamma, $CV = 14.0\%$ (ước lượng trên train) |
| **Khoảng dự báo** | Sinh $K = 1.000$ bộ "4 ngày test" từ mô hình; PI95 = phân vị 2.5%–97.5% của SL mỗi giờ (seed 54321) |
| **So sánh** | SL quan sát trên 4 ngày test (khoảng Wilson); p-value hai phía lấy từ chính 1.000 bộ mô phỏng (V5.1, S16; V5.0 dùng z-test SE nhị thức, quá hẹp), hiệu chỉnh Holm–Bonferroni cho 9 giờ |

Kiểm định KS 2 mẫu thời gian phục vụ train ($n = 6.346$) và test ($n = 2.787$): $D = 0.0326$, $p = 0.031$. Khác biệt có ý nghĩa thống kê do cỡ mẫu lớn, nhưng nhỏ về thực tiễn.

---

## 3. Kết quả theo khung giờ

| Khung giờ | Quầy | SL mô phỏng TB | PI95 | SL thực tế | Wilson 95% | Trong PI95? | Holm $p_{adj}$ | Khác biệt có ý nghĩa? |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 8h–9h | 4 | 0.9359 | [0.8523, 0.9893] | 0.9809 | [0.9561, 0.9918] | Có | 0.8392 | Không |
| 9h–10h | 5 | 0.9187 | [0.8231, 0.9802] | 0.9735 | [0.9520, 0.9856] | Có | 0.6573 | Không |
| 10h–11h | 6 | 0.9449 | [0.8660, 0.9871] | 0.9283 | [0.9010, 0.9485] | Có | 1.0000 | Không |
| 11h–12h | 5 | 0.9076 | [0.7989, 0.9727] | 0.9413 | [0.9128, 0.9609] | Có | 1.0000 | Không |
| 12h–13h | 5 | 0.9361 | [0.8508, 0.9863] | 0.9865 | [0.9659, 0.9948] | Không | 0.4156 | Không |
| 13h–14h | 5 | 0.9475 | [0.8690, 0.9891] | 0.9443 | [0.9136, 0.9645] | Có | 1.0000 | Không |
| 14h–15h | 5 | 0.9229 | [0.8236, 0.9826] | 0.8958 | [0.8566, 0.9252] | Có | 1.0000 | Không |
| 15h–16h | 5 | 0.9252 | [0.8278, 0.9820] | **0.7647** | [0.7141, 0.8088] | Không | 0.1079 | Không |
| 16h–17h | 5 | 0.9642 | [0.9046, 0.9959] | 0.9387 | [0.9028, 0.9619] | Có | 1.0000 | Không |

**7/9 giờ** có SL thực tế nằm trong PI95. Sau hiệu chỉnh Holm không giờ nào khác biệt có ý nghĩa ở mức 5%; hai giờ ngoài PI95 là 12h–13h (thực tế tốt hơn, $p$ thô 0.052) và 15h–16h (thực tế kém hơn nhiều, $p$ thô 0.012, Holm 0.108).

---

## 4. Nhận xét và giới hạn

### 4.1 So sánh không cùng điều kiện nhân sự
> [!WARNING]
> SL quan sát diễn ra dưới **nhân sự thực tế của tổng đài** (dữ liệu không ghi số người trực từng giờ), còn mô phỏng chạy dưới **Lịch 45**. Phép so sánh theo giờ vì vậy chỉ là đối chiếu tham khảo, không phải kiểm chứng cùng điều kiện.

### 4.2 Diễn giải
- Ba giờ thực tế **tốt hơn** mô phỏng (8h, 9h, 12h), phù hợp với việc tổng đài thực có nhiều người phục vụ hơn lịch (số phiên chồng lấn tối đa 5.5–8 người, mục 5). Sau Holm, khác biệt không có ý nghĩa ở mức 5% (V5.0 báo có ý nghĩa do SE nhị thức quá hẹp).
- 15h–16h thực tế **kém hơn nhiều** (76.5%), nằm ngoài PI95 ($p$ thô 0.012) nhưng không còn có ý nghĩa sau hiệu chỉnh cho 9 giờ (Holm 0.108). Mục 5 cho thấy nguyên nhân nằm ở riêng ngày 10, không phải sai lệch của mô hình.
- Tập test đông hơn train 8.1%. Trên 14 ngày thực tế, Lịch 45 đạt SLA 12/14 ngày (hụt hai ngày đông nhất); Lịch 48 đạt 14/14 (`tong_hop.md` mục 4.5).

---

## 5. Điều tra bất thường 15h–16h (V4, nhiệm vụ M4)

> Nguồn số liệu: `results/final_v5/dieu_tra_15h_16h.csv`, `nhan_vien_uoc_luong.csv`, `nhan_vien_uoc_luong_theo_gio.csv` (giai đoạn `data`, chỉ phụ thuộc dữ liệu, không phụ thuộc số lần lặp mô phỏng). Mục này kiểm tra bằng số liệu các giả thuyết về bất thường 15h–16h (nhân sự thiếu, tích lũy hàng chờ, tỉ lệ VIP cao).

### 5.1 Tham số khung 15h–16h: train so với từng ngày test

| Nhóm | λ (khách/phút) | E[S] (phút) | cs² | θ | Tỉ lệ VIP | Bỏ về | SL quan sát | Tải a = λ·E[S] | Số phiên chồng lấn TB | Số phiên chồng lấn tối đa |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Train (10 ngày gộp) | 1,317 | 3,21 | 1,04 | 0,094 | 52,2% | 12,7% | 85,3% | 4,22 | 3,72 | 6,1 |
| Test (4 ngày gộp) | 1,275 | 3,36 | 0,88 | 0,107 | 43,8% | 15,0% | **76,5%** | 4,29 | 3,85 | 6,75 |
| Test ngày 10 | 1,483 | **4,14** | 0,80 | 0,111 | 52,8% | **39,3%** | **31,5%** | **6,14** | 3,67 | 6 |
| Test ngày 11 | 1,217 | 3,32 | 0,82 | 0,074 | 56,2% | 6,8% | 93,2% | 4,05 | 4,11 | 7 |
| Test ngày 12 | 1,350 | 2,92 | 0,78 | 0,111 | 28,4% | 2,5% | 97,5% | 3,95 | 4,00 | 8 |
| Test ngày 13 | 1,050 | 3,29 | 1,10 | 0,134 | 36,5% | 6,3% | 93,7% | 3,45 | 3,61 | 6 |

"Số phiên chồng lấn" = số khách đang được phục vụ cùng lúc, dựng lại từ timestamp (bắt đầu phục vụ = giờ đến + thời gian chờ, kết thúc = bắt đầu + thời gian phục vụ), lấy mẫu mỗi 30 giây trong giờ.

### 5.2 Nhận định

1. **Bất thường tập trung ở một ngày.** Bỏ ngày 10, ba ngày test còn lại có SL 15h–16h = 94,9% (217 khách, bỏ về 5,1%), phù hợp với mô phỏng. Toàn bộ mức tụt xuống 76,5% của tập test đến từ ngày 10 (SL 31,5%, bỏ về 39,3%).
2. **Ngày 10 có nhu cầu cao bất thường.** λ cao hơn train 13% và E[S] cao hơn 29% (4,14 so với 3,21 phút), nên tải đề nghị a = 6,14 Erlang, cao nhất trong 14 ngày (13 ngày còn lại: 2,88–5,33). Chất lượng phục vụ ngày 10 đã giảm từ 14h–15h (SL 80,2%) và chưa hồi phục hẳn lúc 16h–17h (84,9%).
3. **Nhân sự hiệu dụng thấp hơn nhu cầu.** Lúc 15h–16h ngày 10 có hàng chờ gần như liên tục (Wq TB 3,55 phút, chỉ 31,5% khách đạt SLA), nghĩa là mọi người phục vụ đều bận. Dù vậy số phiên chồng lấn trung bình chỉ 3,67, bằng tải đã phục vụ (tổng thời gian phục vụ / 60 = 3,73). Vậy số người phục vụ hoạt động PS hiệu dụng trong giờ đó vào khoảng 4, thấp hơn 5 quầy trong lịch khuyến nghị và thấp hơn nhiều so với 6,1 Erlang tải đề nghị.
4. **Tỉ lệ VIP không phải nguyên nhân chính.** Ngày 11 có tỉ lệ VIP cao hơn ngày 10 (56,2% so với 52,8%) nhưng SL vẫn 93,2%.

**Kết luận M4:** thuộc trường hợp (a) + (b): một ngày có nhu cầu cao (λ và E[S] cùng tăng) gặp nhân sự hiệu dụng khoảng 4 người. Đây không phải sai lệch của mô hình mô phỏng; 3/4 ngày test khớp mô phỏng. Hệ quả vận hành: cần cơ chế tăng cường quầy trong ngày khi thời gian phục vụ hoặc hàng chờ tăng bất thường (xem chính sách dự báo sớm S4 và lịch bền vững).

**Giới hạn:** dữ liệu chỉ gồm hoạt động PS. Nhân viên có thể đồng thời xử lý loại cuộc gọi khác, nên số phiên chồng lấn là *cận dưới* của số nhân viên có mặt, không phải số nhân viên thật. Số phiên chồng lấn tối đa theo giờ (5,5–8 người, `nhan_vien_uoc_luong_theo_gio.csv`) cho thấy tổng đài thực có ít nhất khoảng 6–7 người cùng xử lý PS ở giờ cao điểm.
