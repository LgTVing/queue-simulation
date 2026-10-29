# tools/update_tong_hop_chi_tiet.py
import re

with open('docs/TONG_HOP_SO_LIEU_CHI_TIET.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize line endings
content = content.replace('\r\n', '\n')

# 1. Update 3.3(b) section
pattern_33b = r'#### \(b\) Đánh giá khi có biến động lưu lượng giữa các ngày.*?(?=---|\n### 3\.4)'
replacement_33b = r'''#### (b) Đánh giá khi có biến động lưu lượng giữa các ngày qua Chỉ số kỳ vọng có điều kiện (Nhiệm vụ S2 & S3, `results/final_v3/chi_so_ky_vong_dieu_kien.csv`):

Chỉ số SLA được định nghĩa chuẩn xác theo xác suất dài hạn qua hàm kỳ vọng có điều kiện $E_h(m) = E[SL_h \mid m]$ ($K=200$ kịch bản ngày $\times R=30$ lần lặp, tách rời hoàn toàn nhiễu lấy mẫu nhị thức cỡ mẫu nhỏ theo giờ):

| Chính sách phục vụ | Quầy-giờ | $SL$ kỳ vọng ngày TB | $P(E_{day} \ge 90\%)$ [Wilson 95%] | $P(\min_h E_h \ge 90\%)$ [Wilson 95%] | Số giờ $E_h < 90\%$ TB | $P(\text{thực tế mọi giờ} \ge 90\%)$ | $P(\text{gộp tháng 20 ngày} \ge 90\%)$ |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Mốc cơ sở (6 quầy)** | 54 | 0.9744 | **100.0% [98.1%, 100%]** | **97.5% [94.3%, 98.9%]** | **0.03 giờ** | **76.2% [75.1%, 77.2%]** | **97.3% [94.8%, 98.6%]** |
| **Bền vững (48 q-h)** | 48 | 0.9545 | **98.5% [95.7%, 99.5%]** | **82.5% [76.6%, 87.1%]** | **0.35 giờ** | **46.1% [44.9%, 47.4%]** | **78.0% [73.0%, 82.3%]** |
| **Tối ưu (44 q-h)** | 44 | 0.9341 | **88.5% [83.3%, 92.2%]** | **65.5% [58.7%, 71.7%]** | **1.17 giờ** | **25.7% [24.6%, 26.8%]** | **58.3% [52.7%, 63.8%]** |

> [!IMPORTANT]
> **Phát hiện cốt lõi từ chỉ số kỳ vọng (Nhiệm vụ S2):**  
> 1. Con số $26.0\%$ trước đây bị chi phối nặng bởi sai số lấy mẫu nhị thức ngẫu nhiên của từng nhóm khách nhỏ ($60-100$ khách/giờ, sai số $\pm 2.8\%$), không phản ánh năng lực thực của hệ thống.
> 2. Khi đo bằng chỉ số kỳ vọng dài hạn, Lịch 44 đạt chuẩn cam kết toàn ngày ở **88.5% các kịch bản** (Wilson 95%: $[83.3\%, 92.2\%]$) và đạt chuẩn mọi giờ ở **65.5% kịch bản** (bình quân chỉ có $1.17$ giờ/ngày rơi dưới 90%).
> 3. Dưới góc nhìn kỳ báo cáo quản trị gộp tháng (20 ngày làm việc), xác suất mọi giờ đều đạt chuẩn cam kết của Lịch 44 là **58.3%** và Lịch 48 là **78.0%**.

#### (c) Phân tích Độ nhạy theo $CV_{\text{ngày}} \in \{8\%, 12\%, 16\%, 20\%\}$ (Nhiệm vụ S3, `results/final_v3/do_nhay_cv_ngay.csv`):

| Chính sách | CV ngày | $P(E_{day} \ge 90\%)$ [Wilson 95%] | $P(\min_h E_h \ge 90\%)$ [Wilson 95%] | Số giờ $E_h < 90\%$ TB | $P(\text{thực tế mọi giờ} \ge 90\%)$ |
|---|:---:|:---:|:---:|:---:|:---:|
| **Lịch 44** | 8.0% | 93.0% [86.3%, 96.6%] | 68.0% [58.3%, 76.3%] | 0.88 | 23.2% [21.4%, 25.1%] |
| | **11.8% (Chuẩn)** | **88.5% [83.3%, 92.2%]** | **65.5% [58.7%, 71.7%]** | **1.17** | **25.7% [24.6%, 26.8%]** |
| | 12.0% | 88.0% [80.2%, 93.0%] | 64.0% [54.2%, 72.7%] | 1.15 | 23.3% [21.5%, 25.2%] |
| | 16.0% | 82.0% [73.3%, 88.3%] | 62.0% [52.2%, 70.9%] | 1.43 | 29.6% [27.6%, 31.6%] |
| | 20.0% | 75.0% [65.7%, 82.5%] | 58.0% [48.2%, 67.2%] | 1.70 | 28.7% [26.8%, 30.7%] |
| **Lịch 48** | 8.0% | 100.0% [96.3%, 100%] | 86.0% [77.9%, 91.5%] | 0.22 | 48.2% [46.0%, 50.4%] |
| | **11.8% (Chuẩn)** | **98.5% [95.7%, 99.5%]** | **82.5% [76.6%, 87.1%]** | **0.35** | **46.1% [44.9%, 47.4%]** |
| | 12.0% | 97.0% [91.5%, 99.0%] | 81.0% [72.2%, 87.5%] | 0.40 | 45.1% [42.9%, 47.3%] |
| | 16.0% | 97.0% [91.5%, 99.0%] | 79.0% [70.0%, 85.8%] | 0.45 | 47.2% [45.0%, 49.4%] |
| | 20.0% | 85.0% [76.7%, 90.7%] | 69.0% [59.4%, 77.2%] | 0.81 | 44.6% [42.4%, 46.8%] |
| **Mốc 54** | **11.8% (Chuẩn)** | **100.0% [98.1%, 100%]** | **97.5% [94.3%, 98.9%]** | **0.03** | **76.2% [75.1%, 77.2%]** |

#### (d) Posterior Predictive Check Mô hình Hệ số Nhân ngày (Nhiệm vụ S3, `results/final_v3/posterior_predictive_check.csv`):
Mô phỏng 1.000 bộ 14 ngày từ mô hình $m_d \sim \text{Gamma}(1/CV^2, CV^2)$ với $CV=11.8\%$, so sánh chỉ số phân tán $D_h$ và $D_{\text{total}}$:
- $D_{\text{total}}$ quan sát: $140.38 \implies$ Kỳ vọng mô hình: $137.94$ (CI95: $[68.12, 237.52]$, Posterior Predictive $p = 0.462$). Mô hình giải thích hoàn hảo biến động tổng thể.
- 9 khung giờ đều có $p$-value trong $[0.05, 0.95]$ (từ $0.069$ đến $0.677$).

#### (e) Phân tích Ngưỡng Lưu lượng $V^*$ và Bộ Dự báo Sớm (Nhiệm vụ S4):
- **Ngưỡng lưu lượng an toàn:** Lịch 44 đạt $SL \ge 90\%$ tại mọi mức $V \le 750$ khách/ngày (hụt khi $V \ge 775$). Ngưỡng an toàn thực nghiệm được xác lập là **$V^* = 700$ khách/ngày** (`results/final_v3/nguong_luu_luong_chi_tiet.csv`).
- **Bộ dự báo OLS sớm (8h–10h):** $\hat{V} = 189.6 + 3.49 \cdot (N_{8h-9h} + N_{9h-10h})$ ($r = 0.842, p = 0.0002, R^2 = 0.708$, RMSE $45.3$ khách).
- **Chính sách ghép:** Kích hoạt Lịch 48 khi $\hat{V} > 700$. Đánh giá trên 14 ngày thực tế đạt quầy-giờ trung bình **46.57 quầy-giờ/ngày**, tiết kiệm thực tế **13.76%** so với 54 quầy-giờ mở và **16.84%** so với 56 quầy-giờ công (`results/final_v3/danh_gia_chinh_sach_du_bao_14ngay.csv`).

'''

content = re.sub(pattern_33b, lambda m: replacement_33b, content, flags=re.DOTALL)

# 2. Update 3.5: Cost table
pattern_35 = r'### 3\.5 Hàm Chi phí Kinh tế.*?(\n### 3\.6)'
replacement_35 = r'''### 3.5 Hàm Chi phí Kinh tế và Phân tích Kịch bản Đánh đổi (`results/final_v3/chi_phi_v3.csv`)

Mô hình hóa chi phí tổng thể $C(k) = \text{Quầy-giờ} + k \cdot N \cdot p_{ab}$ trên quy mô $686.7$ khách/ngày kèm khoảng tin cậy truyền sai số từ $p_{ab}$ và hiệu số theo cặp $\Delta C = C_{44} - C_{48}$ (Nhiệm vụ S11):

| Hệ số $k$ | Chi phí Lịch 44 (CI95) | Chi phí Lịch 48 (CI95) | Chi phí Mốc 6 quầy (CI95) | Hiệu số $C_{44} - C_{48}$ | CI 95% Hiệu số | Có ý nghĩa? | Chính sách kinh tế nhất |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **$k = 0.10$** | **$47.60 \pm 0.15$** | $50.52 \pm 0.12$ | $55.43 \pm 0.09$ | **-2.92** | **[-2.99, -2.86]** | **Có** | **Lịch tối ưu 44** |
| **$k = 0.25$** | **$52.99 \pm 0.38$** | $54.29 \pm 0.30$ | $57.58 \pm 0.22$ | **-1.30** | **[-1.46, -1.14]** | **Có** | **Lịch tối ưu 44** |
| **$k = 0.50$** | $61.99 \pm 0.75$ | **$60.59 \pm 0.60$** | $61.16 \pm 0.45$ | **+1.40** | **[+1.07, +1.72]** | **Có** | **Lịch bền vững 48** |
| **$k = 1.00$** | $79.97 \pm 1.51$ | **$73.18 \pm 1.21$** | $68.32 \pm 0.90$ | **+6.79** | **[+6.14, +7.44]** | **Có** | **Lịch bền vững 48** |
| **$k = 2.00$** | $115.94 \pm 3.01$ | $98.36 \pm 2.42$ | **$82.64 \pm 1.79$** | **+17.58** | **[+16.28, +18.88]** | **Có** | Mốc 6 quầy |

*Điểm cân bằng kinh tế:*  
- Khi $k \le 0.25$: Chi phí bỏ về thấp, Lịch 44 tiết kiệm chi phí quầy vượt trội nên rẻ hơn có ý nghĩa thống kê.
- Khi $k \ge 0.50$: Thiệt hại mất khách gia tăng, Lịch 48 trở nên tối ưu hơn nhờ giảm 30% lượng khách bỏ về.
''' + '\n### 3.6'

content = re.sub(pattern_35, lambda m: replacement_35, content, flags=re.DOTALL)

# 3. Update 3.7: Nested Bootstrap
pattern_37 = r'### 3\.7 Phân tích Độ bất định Tham số.*?(\n### 3\.8)'
replacement_37 = r'''### 3.7 Phân tích Bootstrap Lồng nhau và Phân rã Phương sai ANOVA (`results/final_v3/phan_ra_phuong_sai.csv`)

Thiết kế mô hình lồng nhau: $B = 50$ bộ tham số (resample theo ngày để giữ nguyên cấu trúc quá phân tán) $\times R = 60$ lần lặp/bộ (Nhiệm vụ S5):

| Chỉ số phân rã phương sai | Giá trị thực nghiệm | Khoảng tin cậy 95% | Diễn giải ý nghĩa khoa học |
|---|:---:|:---:|---|
| **SL Toàn ngày danh nghĩa ($R=60$)** | **0.9381** | [0.9335, 0.9427] | Trung bình qua 60 lần lặp độc lập |
| **SL Giờ tệ nhất danh nghĩa ($R=60$)** | **0.9060** | - | Trung bình theo giờ rồi lấy min (cùng định nghĩa) |
| **Phương sai tổng quan sát qua 50 bộ** | $1.294 \times 10^{-4}$ | - | $SD = 0.01138$ |
| **Phương sai do nhiễu mô phỏng (Within / R)** | $5.446 \times 10^{-6}$ | - | Sai số ngẫu nhiên Monte Carlo |
| **Phương sai do bất định tham số (Between)** | $1.240 \times 10^{-4}$ | - | Bất định thực sự từ việc ước lượng tham số |
| **Tỉ lệ phương sai do bất định tham số** | **95.79%** | - | **Bất định tham số chi phối gần như tuyệt đối** |
| **Tỉ lệ phương sai do nhiễu mô phỏng** | **4.21%** | - | Với $R=60$, nhiễu mô phỏng triệt tiêu xuống dưới 5% |
| **Xác suất SL toàn ngày $\ge 90\%$** | **100.0%** | [92.87%, 100.0%] | 50/50 bộ bootstrap đạt chuẩn toàn ngày |
| **Xác suất SL giờ tệ nhất $\ge 90\%$** | **90.0%** | [78.64%, 95.65%] | 45/50 bộ bootstrap đạt chuẩn giờ tệ nhất |
''' + '\n### 3.8'

content = re.sub(pattern_37, lambda m: replacement_37, content, flags=re.DOTALL)

# 4. Update 3.8: Distribution sensitivity
pattern_38 = r'### 3\.8 Độ nhạy theo Phân phối Thời gian Phục vụ.*?(\n### 3\.9)'
replacement_38 = r'''### 3.8 Độ nhạy theo Phân phối Thời gian Phục vụ kèm Giờ Tệ nhất (`results/final_v3/do_nhay_phan_phoi_v3.csv`)

Mô phỏng 150 lần lặp độc lập cho 4 phân phối, báo cáo giờ tệ nhất và CI hiệu số theo cặp (Nhiệm vụ S9):

| Phân phối phục vụ | $SL$ Toàn ngày (CI95) | Giờ tệ nhất | $SL$ Giờ tệ nhất | Giờ tệ nhất Low CI95 | Hiệu số so với Gamma | CI 95% Hiệu số | Khác biệt có ý nghĩa? |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Gamma (AIC tốt nhất)** | **0.9431 ± 0.0028** | 16h - 17h | 0.9252 | **0.9149** | Gốc (0.0000) | [0.0000, 0.0000] | - |
| **Bootstrap thực tế** | 0.9353 ± 0.0035 | 11h - 12h | 0.9159 | **0.9056** | -0.0078 | [-0.0122, -0.0034] | **Có** ($0 \notin CI$) |
| **Exponential (M/M/c)** | 0.9383 ± 0.0032 | 16h - 17h | 0.9177 | **0.9071** | -0.0048 | [-0.0091, -0.0005] | **Có** ($0 \notin CI$) |
| **Lognormal ($cv$ + 20%)** | **0.9321 ± 0.0039** | 16h - 17h | 0.9091 | **0.8940** | **-0.0110** | **[-0.0155, -0.0066]** | **Có (Sát ngưỡng 90%)** |
''' + '\n### 3.9'

content = re.sub(pattern_38, lambda m: replacement_38, content, flags=re.DOTALL)

# 5. Update 3.9: Out of sample
pattern_39 = r'### 3\.9 Đánh giá Ngoài mẫu trên Tập Test 4 Ngày.*?(\n### 3\.10)'
replacement_39 = r'''### 3.9 Đánh giá Ngoài mẫu với Khoảng Dự báo 95% (PI95) và Holm-Bonferroni (`results/final_v3/ngoai_mau_v3.csv`)

So sánh tập Test (4 ngày, $2.969$ khách) với Khoảng dự báo 95% (PI95) sinh từ 1.000 bộ 4 ngày mô phỏng có biến động ngày và kiểm định hiệu chỉnh Holm-Bonferroni (Nhiệm vụ S6):

| Khung giờ | Quầy | SL mô phỏng TB | PI95 Low | PI95 High | SL thực tế quan sát | Thực tế Wilson 95% | Trong PI95? | Holm $p_{\text{adj}}$ | Khác biệt có ý nghĩa? |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **8h - 9h** | 4 | 0.9377 | 0.8627 | 0.9860 | **0.9809** | [0.9561, 0.9918] | **Có** | 0.0229 | **Có (Thực tế tốt hơn)** |
| **9h - 10h** | 5 | 0.9240 | 0.8432 | 0.9783 | **0.9735** | [0.9520, 0.9856] | **Có** | 0.0022 | **Có (Thực tế tốt hơn)** |
| **10h - 11h** | 6 | 0.9508 | 0.8838 | 0.9877 | 0.9283 | [0.9010, 0.9485] | **Có** | 0.1031 | Không |
| **11h - 12h** | 5 | 0.9162 | 0.8282 | 0.9721 | 0.9413 | [0.9128, 0.9609] | **Có** | 0.2359 | Không |
| **12h - 13h** | 5 | 0.9434 | 0.8789 | 0.9861 | **0.9865** | [0.9659, 0.9948] | Không | 0.0091 | **Có (Thực tế tốt hơn)** |
| **13h - 14h** | 5 | 0.9515 | 0.8853 | 0.9885 | 0.9443 | [0.9136, 0.9645] | **Có** | 0.5427 | Không |
| **14h - 15h** | 5 | 0.9298 | 0.8504 | 0.9789 | 0.8958 | [0.8566, 0.9252] | **Có** | 0.0976 | Không |
| **15h - 16h** | 5 | 0.9293 | 0.8451 | 0.9792 | **0.7647** | [0.7141, 0.8088] | Không | 0.0000 | **Có (Thực tế giảm mạnh)** |
| **16h - 17h** | 4 | 0.9105 | 0.8157 | 0.9706 | 0.9387 | [0.9028, 0.9619] | **Có** | 0.2359 | Không |

> [!NOTE]
> 7/9 khung giờ quan sát thực tế nằm gọn trong Khoảng dự báo 95%. Khác biệt tại giờ 15h–16h ($SL = 76.47\%$) được ghi nhận như một **giả thuyết cần kiểm chứng**: vào cuối ngày, các giao dịch viên thực tế có thể phải tập trung chốt sổ, kiểm quỹ hoặc quầy mở thực tế bị rút giảm. Kiểm định Welch giữa tổng khách Train và Test cho thấy không có sự khác biệt có ý nghĩa thống kê về nhu cầu tổng thể ($t=1.74, p=0.115$).
''' + '\n### 3.10'

content = re.sub(pattern_39, lambda m: replacement_39, content, flags=re.DOTALL)

# 6. Update 3.10: Pytest 22/22
pattern_310 = r'### 3\.10 Kết quả Kiểm thử Tự động.*?(\n## PHẦN 4)'
replacement_310 = r'''### 3.10 Kết quả Kiểm thử Tự động pytest 22/22 Passed (`results/final_v3/pytest_log.txt`)

Toàn bộ **22 ca kiểm thử đơn vị tự động** trong thư mục `tests/` chạy qua thành công 100% trong 9.82 giây:
- 12 bài test chuẩn giải tích và mô phỏng (`test_theory.py`, `test_sim.py`).
- 6 bài test tính năng ca làm việc MILP và biến động ngày (`test_v2_features.py`).
- 4 bài test thống kê chuẩn mực mới: `test_wilson_ci_properties`, `test_student_t_ci_degrees_of_freedom`, `test_holm_bonferroni_adjustment`, `test_early_hour_predictor_correlation`.

### 3.11 Khảo sát Vét cạn Pha 3 và Bảng 14 Ngày Thực tế (`results/final_v3/pha3.csv` & `theo_14_ngay_v3.csv`)
1. **Khảo sát Pha 3 (C6):** Thử nghiệm 117 cấu hình lân cận (72 swap 1 quầy + 36 double reduction). Kết quả: **0/117 cấu hình khả thi** đạt chuẩn SLA $\ge 90\%$. Lịch 44 là **nghiệm tối thiểu cục bộ duy nhất**.
2. **Đối chiếu 14 ngày thực tế (S7):** Lịch 44 đạt **12/14 ngày (85.7% [60.1%, 96.0%])** (chỉ hụt ngày 2 và ngày 7 có tải cực đại). Lịch 48 và Mốc 6 quầy đạt **14/14 ngày (100% [78.5%, 100%])**.
''' + '\n## PHẦN 4'

content = re.sub(pattern_310, lambda m: replacement_310, content, flags=re.DOTALL)

with open('docs/TONG_HOP_SO_LIEU_CHI_TIET.md', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated TONG_HOP_SO_LIEU_CHI_TIET.md successfully!')
