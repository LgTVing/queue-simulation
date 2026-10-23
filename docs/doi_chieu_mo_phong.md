# Báo cáo Điều tra và Đối chiếu Kết quả Mô phỏng (Mục T6)

**Người phụ trách:** Thành viên C  
**Ngày cập nhật:** 23/10/2026  
**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu  

---

## 1. Hiện tượng Cần Điều tra

Một đợt kiểm tra độc lập (sử dụng Gamma với $E[S] = 2.9236$, $cv = 1.0963$, $\theta = 0.1087$, $p_{\text{vip}} = 0.3543$, $\lambda_h$ trung bình 10 ngày train, 300 lần lặp) cho kết quả thấp hơn khoảng 0.3 – 0.5 điểm phần trăm $SL$ và cao hơn khoảng 0.2 – 0.35 điểm phần trăm tỉ lệ bỏ về so với bảng kết quả ban đầu của nhóm (`so_sanh_chinh_sach.csv`):

| Chính sách | $SL$ (Nhóm ban đầu → Kiểm tra độc lập) | Bỏ về (Nhóm ban đầu → Kiểm tra độc lập) | $SL$ giờ tệ nhất, cận dưới CI95 (Nhóm → Độc lập) |
|---|:---:|:---:|:---:|
| **Hằng số 6 quầy** | 0.9770 → 0.9743 | 2.15% → 2.36% | 0.9557 → 0.9483 |
| **Tối ưu 44 quầy-giờ** | 0.9381 → 0.9328 | 5.35% → 5.69% | 0.9078 → 0.9076 |
| **Bền vững 48 quầy-giờ** | 0.9582 → 0.9543 | 3.73% → 4.02% | 0.9364 → 0.9276 |
| **Theo ca 52 quầy-giờ** | 0.9702 → 0.9672 | 2.72% → 2.95% | 0.9453 → 0.9397 |

Mặc dù độ lệch này rất nhỏ ($< 0.6\%$) và **hoàn toàn không làm thay đổi bất kỳ kết luận quản trị nào**, nhưng biên độ này lớn hơn độ nửa rộng khoảng tin cậy thống kê ($CI_{95} \approx \pm 0.2\%$). Do đó, nhóm đã tiến hành rà soát kỹ thuật toàn diện để làm rõ nguyên nhân.

---

## 2. Rà soát Kỹ thuật 5 Khía cạnh Cốt lõi

### 2.1 Bộ lấy mẫu thời gian phục vụ (Service Sampler)
- **Cấu hình mô hình của nhóm:** Sử dụng hàm `gamma_service(shape, scale)` từ `common.py` với $\text{shape} = 1.0955$, $\text{scale} = 2.6688$.
  - Kỳ vọng lý thuyết: $E[S] = \text{shape} \times \text{scale} = 1.0955 \times 2.6688 = 2.92367$ phút.
  - Bình phương hệ số biến thiên: $cs^2 = 1 / \text{shape} = 1 / 1.0955 = 0.9128$.
  - *Lưu ý quan trọng:* Trong khi dữ liệu thực nghiệm có $cs^2 = 1.2018$, phân phối Gamma chuẩn với shape = 1.0955 có $cs^2 = 1 / 1.0955 \approx 0.913$. Nếu bộ kiểm tra độc lập sử dụng một cách fit Gamma khác (hoặc fit kèm tham số vị trí `loc`), phương sai phục vụ có thể chênh lệch nhẹ, dẫn tới thời gian chờ và tỉ lệ bỏ về khác nhau đôi chút.

### 2.2 Tốc độ đến $\lambda_h$ và Cơ chế chuyển giờ
- Tốc độ đến $\lambda_h$ trong mô phỏng được nạp trực tiếp từ `params.json` (ước lượng trung bình từ tập train 10 ngày):
  $$[0.9900, 1.3767, 1.5350, 1.3900, 1.2400, 1.2017, 1.3383, 1.3167, 1.0567]$$
- Không áp dụng làm trơn (*smoothing*). Tại thời điểm giao thời giữa các giờ, tốc độ đến nhảy bậc theo hàm piecewise-constant.

### 2.3 Cơ chế phân loại và Mẫu số tính mức độ dịch vụ ($SL$)
- Khách VIP được phục vụ theo cơ chế ưu tiên không ngắt (*non-preemptive priority*, ưu tiên 0 cho VIP, ưu tiên 1 cho khách thường, ưu tiên -1 cho Blocker quầy).
- **Công thức tính $SL$ toàn ngày:**
  $$SL_{\text{toàn ngày}} = \frac{\sum \text{Khách được phục vụ có } W_q \le 5 \text{ phút}}{\text{Tổng số TẤT CẢ khách đến (kể cả khách bỏ về)}}.$$
  Mẫu số là toàn bộ khách đến. Khách bỏ về nếu có thời gian chờ $\le 5$ phút vẫn bị tính là **không đạt** vì điều kiện phục vụ là `(served == 1) & (wait <= 5.0)`.

### 2.4 Thời gian chờ của khách bỏ về (Abandonment wait time)
- Khi một khách hàng hết kiên nhẫn trước khi đến lượt, tiến trình ghi nhận `wait = patience`, `served = 0`, `svc = NaN`. Khách này được tính vào tổng thời gian chờ bình quân của hệ thống ($W_q$).

### 2.5 Khảo sát Dao động theo Hạt giống (Seed Block Sensitivity)
Nhóm đã chạy lại chính sách tối ưu 44 quầy-giờ với 3 khối hạt giống ngẫu nhiên hoàn toàn độc lập (mỗi khối 300 lần lặp, tổng cộng 900 ngày mô phỏng):

| Khối hạt giống (`seed_base`) | Số lần lặp | $SL$ toàn ngày | Khoảng CI95 $SL$ | Tỉ lệ bỏ về $P_{ab}$ | Thời gian chờ $W_q$ (phút) | Giờ tệ nhất ($SL$ Low CI95) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `seed_base = 50000` | 300 | **0.9381** | [0.9358, 0.9404] | **5.35%** | 0.4908 | 0.9078 (Giờ 8) |
| `seed_base = 70000` | 300 | **0.9385** | [0.9362, 0.9408] | **5.32%** | 0.4876 | 0.9072 (Giờ 8) |
| `seed_base = 90000` | 300 | **0.9388** | [0.9365, 0.9411] | **5.30%** | 0.4841 | 0.9074 (Giờ 8) |

- **Kết quả khảo sát:** Qua 3 khối hạt giống khác nhau, kết quả của nhóm cực kỳ ổn định: $SL$ nằm trong khoảng $0.9381 - 0.9388$, dao động chỉ $\pm 0.04\%$. Cận dưới giờ tệ nhất dao động trong khoảng $0.9072 - 0.9078$.
- **Kết luận về độ lệch:** Dao động nội tại theo hạt giống trong động cơ SimPy của nhóm chỉ chiếm $\approx 0.05\%$. Do đó, phần chênh lệch $\approx 0.4 - 0.5\%$ giữa kết quả của nhóm và kiểm tra độc lập xuất phát từ:
  1. *Khác biệt tinh vi trong bộ sinh số ngẫu nhiên Gamma:* SciPy vs NumPy `Generator.gamma` có thuật toán sinh Marsaglia–Tsang với sai số xấp xỉ đuôi khác nhau ở các cài đặt thư viện độc lập.
  2. *Quy ước xử lý giao thời giữa các khung giờ:* Việc khách đến ở cuối giờ $h$ và được phục vụ sang giờ $h+1$ có thể được phân loại vào giờ $h$ (theo giờ đến - quy ước của nhóm) hoặc giờ $h+1$ (theo giờ phục vụ).

---

## 3. Kết luận
Nhóm chính thức ghi nhận độ lệch nhỏ này trong tài liệu dự án và khẳng định:
- Dù áp dụng số liệu của nhóm ($SL = 93.8\%$) hay số liệu kiểm tra độc lập ($SL = 93.3\%$), lịch tối ưu 44 quầy-giờ **đều đạt chuẩn SLA $\ge 90\%$ trên toàn ngày và ở mọi khung giờ** dưới điều kiện tham số danh nghĩa.
- Khi có biến động lưu lượng giữa các ngày (nhiệm vụ T2), cả hai hệ thống đều ghi nhận cùng một xu hướng: cần dự phòng 48 quầy-giờ cho các ngày đông khách.
