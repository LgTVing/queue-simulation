# YÊU CẦU CHỈNH SỬA ĐỢT 2: THỐNG KÊ VÀ XÁC SUẤT (dành cho Agent)

> **Cách dùng:** đặt file này ở thư mục gốc dự án, cùng với `YEU_CAU_CHINH_SUA_AGENT.md` (đợt 1). Giao cho agent:
> *"Đọc `YEU_CAU_CHINH_SUA_THONG_KE_V2.md` và thực hiện lần lượt các nhiệm vụ từ P0 đến P2. Tuân thủ mục 'Quy tắc bắt buộc'. Cuối cùng nộp `docs/BAO_CAO_SUA_DOI_V2.md`."*

---

## 0. Bối cảnh

Bản tổng hợp số liệu mới (`TONG_HOP_SO_LIEU_CHI_TIET_1.md`) đã sửa được nhiều lỗi của đợt 1: nhãn kiểm định Poisson, thống kê quá phân tán theo ngày, mô hình có hệ số nhân ngày, các mô hình ca làm việc A/B, hiệu số theo cặp ở mục 3.8, ghi chú về nhân sự thực ở mục 3.9, cách gọi "mốc cơ sở" thay cho "hiện trạng".

**Đã kiểm tra và đúng (không cần sửa):** ma trận khách theo ngày–giờ và mọi trung bình, λ_h, chỉ số phân tán D theo giờ, thống kê tổng ngày (D = 140,4, CV ngày 11,8% sau khi trừ nhiễu Poisson), các bảng Excel, bảng chi phí (trừ dòng "Theo ca", xem C3), phần lớn bảng ca làm việc (4h = 52, ca 8h mô hình A = 64, mô hình B = 48, hỗn hợp 44 duy nhất khi nghỉ trong 11h–14h, phủ 6 quầy cần 7 nhân viên), độ nhạy 3.4 (đơn điệu, nhất quán), tỉ lệ ngày đạt SL kỳ vọng ≥ 90% (85% / 95,3% / 100% khớp với kiểm tra độc lập: 85% / 97,5% / 100%).

**Còn các vấn đề về thống kê và xác suất**, làm cho một số con số **không đủ tin cậy để dùng làm kết luận** như cách đang trình bày. Tài liệu này yêu cầu sửa các vấn đề đó. Mục tiêu vẫn là **trung thực với dữ liệu**, không làm số liệu đẹp hơn.

---

## 1. Quy tắc bắt buộc

1. **Không bịa và không chỉnh số cho đẹp.** Mọi con số trong tài liệu phải sinh từ lần chạy lại và được trích **tự động** từ CSV (xem C7). Không gõ tay.
2. **Không đổi seed, số lần lặp hay tiêu chí chỉ để kết quả đạt SLA.** Mọi thay đổi cấu hình ghi vào `CHANGELOG.md` kèm lý do.
3. Giữ nguyên `results/final_v1/` và `results/final_v2/` hiện có làm lưu trữ. Kết quả mới ghi vào `results/final_v3/` kèm `MO_TA.md` (ngày chạy, version `params.json`, seed, số lần lặp, commit).
4. **Không sửa `data/raw/`.**
5. Mọi **tỉ lệ** (xác suất, phần trăm ngày đạt) phải kèm **khoảng tin cậy** (Wilson hoặc Clopper–Pearson). Mọi **trung bình mô phỏng** phải nêu số lần lặp và dùng giá trị tới hạn Student-t thay cho 1,96 khi số lần lặp dưới 100.
6. Nếu kết quả mới làm yếu hoặc đảo ngược một kết luận cũ, phải sửa kết luận và nêu rõ trong báo cáo.
7. Nếu thiếu dữ liệu hoặc thông tin, **không tự giả định**. Ghi vào mục "Việc chưa làm được".
8. Giữ quy ước giờ: giờ 0 = 8h–9h, giờ 8 = 16h–17h.
9. Chạy `pytest tests/` sau mọi thay đổi code và lưu log.

---

## 2. Danh sách nhiệm vụ

| ID | Mức | Nhiệm vụ ngắn gọn |
|---|---|---|
| S1 | P0 | Khoảng tin cậy của λ_h đang giả định Poisson nên quá hẹp, sửa lại |
| S2 | P0 | Chỉ số "P(mọi giờ ≥ 90%)" bị nhiễu lấy mẫu chi phối, thay bằng chỉ số kỳ vọng có điều kiện |
| S3 | P0 | Độ bất định của CV ngày và kiểm tra mức phù hợp của mô hình hệ số nhân ngày |
| S4 | P0 | Quy tắc vận hành theo ngưỡng 687 khách/ngày không có căn cứ, đánh giá lại |
| S5 | P0 | Phân tích bootstrap (3.7): thiết kế, so sánh chỉ số, phân rã nhiễu |
| S6 | P0 | Kiểm tra ngoài mẫu (3.9): so sánh quan sát với khoảng dự báo đúng nghĩa |
| S7 | P1 | Báo cáo "10/14 ngày thực tế đạt SLA" thiếu phương pháp và khoảng tin cậy |
| S8 | P1 | Kiểm chứng M/G/1: nói quá, thiếu năng lực kiểm định; giá trị tới hạn t; đa so sánh |
| S9 | P1 | Mục 3.8: "CRN" không giảm phương sai; cột giờ tệ nhất còn thiếu |
| S10 | P1 | Các giả định phân phối (bỏ về, phục vụ) chưa được kiểm định đầy đủ |
| S11 | P1 | Bảng chi phí: xếp hạng chính sách không xét sai số |
| C1 | P1 | Số liệu Phần 5 không khớp mục 3.3(b) |
| C2 | P1 | "86,5%" ở Phần 5 không có trong bảng nào |
| C3 | P1 | Mục 3.5 còn dòng "Theo ca" cũ (52 q-h) trái với 3.3(a) |
| C4 | P1 | Phần 5, cột "Mốc cơ sở": nhân sự và cơ sở tính chi phí sai |
| C5 | P1 | Phần 5, cột "Dự phòng": giả định giờ nghỉ cho ca 48 chưa nêu |
| C6 | P1 | Phát biểu quá mạnh ("đúng tuyệt đối", "biên an toàn tốt", "đạt mục tiêu") |
| C7 | P2 | Tự động hóa trích số, pytest, các lỗi nhỏ |

---

## 3. Nhiệm vụ P0

### S1. Khoảng tin cậy của λ_h giả định Poisson nên quá hẹp

**Vấn đề.** Cột "CI95 λ" (sheet `Thong_ke_theo_gio`, `bang_tham_so.xlsx`) dùng công thức `λ ± 1,96·√(N̄/n)/60`. Công thức này đúng **chỉ khi số khách theo ngày là Poisson**. Chính bảng 2.1 đã bác bỏ Poisson ở 8/9 giờ (quá phân tán), nên khoảng tin cậy này **hẹp hơn thực tế 1,4–2,1 lần**.

So sánh nửa độ rộng khoảng tin cậy 95% (khách/ngày), tính lại từ ma trận 14 ngày:

| Giờ | 8h | 9h | 10h | 11h | 12h | 13h | 14h | 15h | 16h |
|---|---|---|---|---|---|---|---|---|---|
| Công thức Poisson (đang dùng) | 4,1 | 4,9 | 5,2 | 4,9 | 4,5 | 4,5 | 4,7 | 4,6 | 4,2 |
| Khoảng t theo phương sai thực tế | 6,1 | 7,2 | 11,1 | 9,3 | 6,3 | 7,7 | 8,8 | 8,2 | 6,6 |
| Tỉ số | 1,48 | 1,48 | 2,13 | 1,91 | 1,40 | 1,69 | 1,89 | 1,77 | 1,58 |

(Chia cho 60 để đổi sang khách/phút.)

**Việc cần làm.**
1. Thay khoảng tin cậy của λ_h bằng khoảng t: `N̄ ± t(0,975; 13)·s/√14` với `s` là độ lệch chuẩn mẫu theo ngày của giờ đó. Ghi chú: đây là khoảng cho **trung bình dài hạn** của giờ đó.
2. Cập nhật mọi nơi dùng CI này: `thong_ke_mo_ta.xlsx`, `bang_tham_so.xlsx`, `params.json` (`rates_ci95`), báo cáo, slide, hình `fig_a_fit.png`.
3. Với phần bootstrap tham số (S5), λ_h phải được lấy mẫu **bằng cách resample theo ngày** (giữ nguyên cấu trúc quá phân tán), không lấy mẫu chuẩn từ khoảng tin cậy Poisson.

**Nghiệm thu.** Không còn khoảng tin cậy λ_h tính bằng công thức Poisson ở bất kỳ file nào. Bảng đối chiếu 3 cột ở trên được tái tạo bằng code.

---

### S2. Chỉ số "P(mọi giờ ≥ 90%)" bị nhiễu lấy mẫu chi phối

**Vấn đề.** Mục 3.3(b) và Phần 5 báo cáo "xác suất mọi 9 giờ đều SL ≥ 90%" chỉ **26%** cho lịch 44 và **47%** cho lịch 48. Chỉ số này đo **tỉ lệ khách thực tế đạt trong từng giờ của một ngày** (khoảng 60–100 khách mỗi giờ). Với cỡ mẫu nhỏ như vậy, sai số lấy mẫu nhị thức của một giờ lên tới khoảng ±2,8 điểm phần trăm, nên **ngay cả khi hệ thống đúng như thiết kế**, xác suất tồn tại ít nhất một giờ thực tế rơi dưới 90% đã rất cao. SLA được định nghĩa theo xác suất dài hạn, không phải theo tỉ lệ thực tế của 60–100 khách.

Kiểm tra độc lập (300 ngày mô phỏng, **không có biến động ngày**, λ_h cố định): `P(mọi giờ thực tế ≥ 90%)` = 0,76 (6 quầy), **0,12** (lịch 44), 0,34 (lịch 48). Nghĩa là chỉ riêng nhiễu nhị thức đã kéo chỉ số của lịch 44 xuống còn 12%, trước khi tính bất kỳ biến động nhu cầu nào.

Khi dùng chỉ số **kỳ vọng có điều kiện** (tách biến động nhu cầu khỏi nhiễu lấy mẫu), với hệ số nhân ngày Gamma CV 11,8% (40 kịch bản ngày × 25 lần lặp):

| Lịch | P(SL kỳ vọng ngày ≥ 90%) | P(SL kỳ vọng MỌI giờ ≥ 90%) | P(mọi giờ thực tế ≥ 90%) |
|---|---|---|---|
| 6 quầy | 1,000 | 0,975 | 0,666 |
| 44 | 0,850 | 0,575 | 0,191 |
| 48 | 0,975 | 0,750 | 0,360 |

Chỉ số ở cột 2–3 là thước đo đúng cho "hệ thống có đạt cam kết không". Cột 4 là hỗn hợp của nhu cầu và nhiễu lấy mẫu. Ngoài ra các tỉ lệ trong bảng của nhóm (78% / 47% / 26%) cao hơn kiểm tra độc lập (66,6% / 36,0% / 19,1%) khoảng 8–11 điểm, vượt sai số Monte Carlo (±5 điểm), cần giải thích.

**Việc cần làm.**
1. Định nghĩa lại chỉ số: với mỗi ngày kịch bản (hệ số nhân `m` rút từ phân phối ngày), chạy **đủ nhiều lần lặp** (khuyến nghị ≥ 200) và tính `E_h(m)` = SL kỳ vọng của giờ h = trung bình qua các lần lặp. Báo cáo:
   - `P_m(SL kỳ vọng ngày ≥ 90%)`;
   - `P_m(min_h E_h(m) ≥ 90%)`;
   - số giờ trung bình có `E_h(m) < 90%`.
2. Giữ chỉ số thực tế cũ làm phụ, đổi tên thành "Tỉ lệ ngày mà mọi giờ thực tế đạt (bao gồm nhiễu lấy mẫu)" và thêm chú thích: chỉ số này chịu ảnh hưởng mạnh của cỡ mẫu nhỏ theo giờ.
3. Thêm góc nhìn quản trị theo **kỳ báo cáo**: SL theo giờ **gộp khách của 20 ngày làm việc** (một tháng), vì cam kết dịch vụ thường được đánh giá theo kỳ. Báo cáo `P(SL gộp theo giờ ≥ 90%)`.
4. Mọi tỉ lệ kèm khoảng Wilson. Cho 300 ngày mô phỏng: 85,0% có khoảng [80,5%; 88,6%], 26,0% có [21,4%; 31,2%].
5. Điều tra vì sao con số của nhóm (78/47/26) cao hơn kiểm tra độc lập (66,6/36,0/19,1): so sánh hệ số nhân ngày, cách tính giờ, số lần lặp, seed.
6. Sửa mọi lời diễn giải: không dùng "26% ngày đạt mọi giờ" như bằng chứng lịch 44 hỏng.

**Nghiệm thu.** Bảng 3.3(b) có đủ ba chỉ số, đều có khoảng tin cậy. Báo cáo giải thích sự khác nhau giữa chỉ số kỳ vọng và chỉ số thực tế.

---

### S3. Độ bất định của CV ngày và mức phù hợp của hệ số nhân ngày

**Vấn đề.**
1. `CV_ngày = 11,8%` ước lượng từ **14 ngày**. Khoảng tin cậy 95% (từ phân phối χ² của phương sai) của `CV_ngày²` là [0,0067; 0,0385], tức `CV_ngày` thuộc khoảng **[8,2%; 19,6%]**. Mọi xác suất ở 3.3(b) phụ thuộc mạnh vào giá trị này nhưng chỉ chạy với một giá trị.
2. Mô hình dùng **một hệ số nhân chung** cho cả 9 giờ. Cần kiểm tra mô hình có tái tạo được độ phân tán **theo từng giờ**. Với một hệ số nhân CV 11,8% thì chỉ số phân tán kỳ vọng `D_h = 13·(1 + CV²·μ_h)` so với quan sát:

| Giờ | 8h | 9h | 10h | 11h | 12h | 13h | 14h | 15h | 16h |
|---|---|---|---|---|---|---|---|---|---|
| D quan sát | 23,5 | 23,6 | 48,8 | 39,2 | 20,8 | 30,7 | 38,1 | 33,6 | 26,6 |
| D kỳ vọng (1 hệ số nhân) | 24,1 | 28,6 | 30,9 | 28,7 | 26,5 | 26,5 | 27,4 | 27,2 | 24,6 |

Các giờ 10h, 11h, 13h, 14h, 15h có độ phân tán quan sát **cao hơn** mô hình đã giải thích (đặc biệt 10h: 48,8 so với 30,9). Tương quan giữa các giờ trong cùng ngày trung bình 0,45 (từ −0,07 đến 0,77), tức hệ số nhân chung chưa đủ.

**Việc cần làm.**
1. **Phân tích độ nhạy theo CV ngày:** chạy lại 3.3(b) với `CV_ngày ∈ {8%, 12%, 16%, 20%}` (bao phủ khoảng tin cậy). Báo cáo bảng và nêu rõ kết luận phụ thuộc vào CV thế nào.
2. **Kiểm tra mức phù hợp (posterior predictive check):** mô phỏng 1.000 "bộ 14 ngày" từ mô hình, tính `D_h` từng giờ và tổng ngày, so với quan sát. Báo cáo giờ nào mô hình không tái tạo được.
3. **Thử mô hình tốt hơn** và so sánh: (a) hệ số nhân chung kèm hệ số riêng theo giờ (hai tầng); (b) phân phối nhị thức âm cho số khách theo giờ (`μ_h`, tham số phân tán riêng cho mỗi giờ); (c) resample trực tiếp các **ngày thực tế** (bootstrap theo ngày) làm đối chiếu không tham số.
4. Chọn mô hình theo kết quả kiểm tra phù hợp và ghi lý do. Chạy lại đánh giá chính sách với mô hình được chọn.

**Nghiệm thu.** Có bảng độ nhạy theo CV ngày và bảng posterior predictive check. Báo cáo nêu mô hình nào được chọn và vì sao.

---

### S4. Quy tắc vận hành theo ngưỡng 687 khách/ngày không có căn cứ

**Vấn đề.** Phần 5 đề xuất dùng lịch 44 khi lưu lượng ≤ 687 khách/ngày và lịch 48 khi > 687. Ngưỡng 687 chỉ là **trung bình tập train (686,7)**, không xuất phát từ phân tích SLA. Ngoài ra:
- Lưu lượng cả ngày **chưa biết** lúc xếp lịch; chưa có phân tích về khả năng dự báo.
- Trong 14 ngày, chỉ **5/14** ngày có tổng ≤ 687 (train 5/10, test **0/4**). Nếu áp dụng quy tắc, lịch 44 chỉ dùng khoảng 36% số ngày, nên mức tiết kiệm kỳ vọng là `(5×44 + 9×48)/14 = 46,6` quầy-giờ, tức **tiết kiệm 13,8%**, không phải 18,5% như đang ghi.
- Chất lượng của chính sách ghép (quy tắc + hai lịch) chưa được đánh giá ở đâu.

Có tín hiệu dự báo: tương quan giữa số khách 8h–10h và số khách 10h–17h là **r = 0,74** (p = 0,002); giữa 8h–11h và phần còn lại là r = 0,61 (p = 0,021). Có thể dùng số khách các giờ đầu để quyết định lịch cho phần còn lại của ngày.

**Việc cần làm.**
1. Tính xác suất `P(SL ngày đạt | lưu lượng ngày = V)` bằng mô phỏng, rồi **chọn ngưỡng V\*** sao cho lịch 44 đạt mục tiêu (ví dụ P ≥ 90%) khi lưu lượng ≤ V\*. Ngưỡng này không phải trung bình dữ liệu.
2. Nghiên cứu **bộ dự báo**: hồi quy lưu lượng cả ngày (hoặc phần còn lại) theo số khách các giờ đầu, báo cáo sai số dự báo (RMSE, khoảng dự báo). Đánh giá lệnh chuyển lịch giữa ngày (ví dụ quyết định lúc 10h) có khả thi về vận hành không (nhân viên 4 giờ có thể được gọi thêm).
3. **Đánh giá chính sách ghép** bằng mô phỏng có dự báo không hoàn hảo: báo cáo quầy-giờ kỳ vọng, `P(SL ngày ≥ 90%)`, `P(SL kỳ vọng mọi giờ ≥ 90%)`, so với lịch 44, 48, 6 quầy cố định. Báo cáo mức tiết kiệm **thực tế** có tính đến sai số dự báo.
4. Nếu không dự báo được đủ tốt, **bỏ quy tắc theo lưu lượng** và nêu rõ lịch 44 chỉ phù hợp cho ngày trung bình, kèm xác suất đạt tương ứng.
5. Sửa Phần 5: bỏ con số 687 nếu không có căn cứ, sửa tỉ lệ tiết kiệm theo kết quả mới.

**Nghiệm thu.** Ngưỡng (nếu còn) có căn cứ từ mô phỏng. Có đánh giá chính sách ghép, mức tiết kiệm thực tế, và báo cáo sai số dự báo.

---

### S5. Phân tích bootstrap tham số (mục 3.7)

**Vấn đề.**
1. **Không nêu số lần lặp mô phỏng cho mỗi bộ tham số.** Điều này quyết định phần nhiễu mô phỏng. Từ khoảng tin cậy ở 3.3(a), độ lệch chuẩn mỗi lần lặp của SL toàn ngày (lịch 44) khoảng 0,0203. Nếu mỗi bộ tham số chỉ 20 lần lặp, sai số mô phỏng là 0,0045, giải thích khoảng **79%** phương sai quan sát được của SL toàn ngày qua các bộ (độ lệch chuẩn khoảng 0,0051). Với 30, 50, 60 lần lặp: 53%, 32%, 26%. Khi đó khoảng [0,9289; 0,9457] phần lớn phản ánh nhiễu mô phỏng, không phải bất định tham số.
2. **So sánh hai chỉ số khác bản chất:** 90,78% (cận dưới của giờ tệ nhất trên 300 lần lặp, tham số danh nghĩa) với "trung bình giờ tệ nhất" qua bootstrap. Việc lấy **nhỏ nhất của 9 ước lượng nhiễu** làm lệch xuống (thiên lệch cực trị), nên phần chênh lệch có thể do nhiễu chứ không chỉ do sai số tham số. Ghi chú "phản ánh tác động của sai số mẫu trong ước lượng tham số" chưa có bằng chứng.
3. **Không nêu cách lấy mẫu λ_h.** Nếu lấy từ khoảng tin cậy Poisson thì bất định bị đánh giá thấp (xem S1).
4. Các xác suất `50/50`, `3/50`, `19/50` không có khoảng tin cậy: Wilson cho `50/50` là [92,9%; 100%], `3/50` là [2,1%; 16,2%], `19/50` là [25,9%; 51,8%].

**Việc cần làm.**
1. Ghi rõ trong tài liệu và CSV: số bộ bootstrap, số lần lặp mỗi bộ, cách lấy mẫu từng tham số (λ_h bằng resample theo ngày, E[S] và phân phối bằng bootstrap khách phục vụ, θ bằng bootstrap hoặc phân phối xấp xỉ).
2. Thiết kế lại thành **mô hình lồng nhau** (nested): `B` bộ tham số × `R` lần lặp mỗi bộ, với `R ≥ 60` (khuyến nghị 100). Phân rã phương sai: phần giữa các bộ (bất định tham số) và phần trong bộ (nhiễu mô phỏng), báo cáo hai phần này.
3. Tính "SL giờ tệ nhất" **cùng định nghĩa** cho tham số danh nghĩa và cho mỗi bộ bootstrap: lấy **trung bình theo giờ** rồi lấy nhỏ nhất; và chạy tham số danh nghĩa với cùng `R` để so sánh trực tiếp. Thêm cột "hiệu chỉnh thiên lệch cực trị" bằng cách ước lượng thiên lệch từ mô phỏng danh nghĩa lặp lại nhiều lần.
4. Báo cáo mọi xác suất kèm khoảng Wilson.
5. Gỡ các câu giải thích nhân quả chưa có bằng chứng.

**Nghiệm thu.** Có bảng phân rã phương sai, định nghĩa thống nhất cho "SL giờ tệ nhất", và mọi tỉ lệ kèm khoảng tin cậy.

---

### S6. Kiểm tra ngoài mẫu (mục 3.9)

**Vấn đề.**
1. **So sánh điểm với khoảng sai.** Cột "SL Low CI95" là khoảng tin cậy của **trung bình mô phỏng** (độ chính xác của mô hình). Giá trị quan sát là **một mẫu thực tế của 4 ngày** (khoảng 260–300 khách mỗi giờ, sai số nhị thức khoảng ±1,5 điểm cho SL gần 0,93), cộng thêm biến động ngày. Phải so sánh với **khoảng dự báo** (predictive interval), không phải với khoảng tin cậy của trung bình.
2. **Giá trị quan sát không có khoảng tin cậy.** Cần khoảng Wilson cho SL, bỏ về, và khoảng cho Wq.
3. **Tập test quá nhỏ và không đại diện cho biến động:** 4 ngày, độ lệch chuẩn tổng ngày chỉ **10,9** (tập train **99,7**), trung bình 742,3 so với 686,7. Kiểm định Welch cho thấy chênh lệch trung bình **không có ý nghĩa** (t = 1,74; p = 0,115), nên không nên khẳng định "nhu cầu test cao hơn". Ngoài ra, 4 ngày test đều có tổng > 687.
4. **Đoạn giải thích nguyên nhân sụt giảm lúc 15h–16h** ("dồn hóa đơn, đóng sổ cuối ngày, rút bớt quầy") được trình bày như một hiện tượng đã biết nhưng **không có dữ liệu chứng minh**. Đây là giả thuyết.
5. **Chưa giải thích được độ lệch với kiểm tra độc lập:** chạy lịch 44 tại λ_test với tham số train cho SL toàn ngày khoảng 0,906 (bỏ về 7,65%, Wq 0,70 phút), trong khi cột mô phỏng của nhóm cho khoảng 0,930 (bỏ về 6,3%, Wq 0,50). Chưa nêu rõ tham số, hệ số nhân ngày, số lần lặp đã dùng.

**Việc cần làm.**
1. Ghi vào `docs/ngoai_mau.md`: λ, E[S], phân phối, θ, p_vip, hệ số nhân ngày, số lần lặp, seed của phần mô phỏng cho tập test.
2. Tính **khoảng dự báo 95%** cho từng giờ và cho toàn ngày: mô phỏng nhiều "tập 4 ngày" (mỗi ngày với hệ số nhân và nhiễu khách riêng), lấy phân vị 2,5%–97,5% của SL, bỏ về, Wq tổng hợp trên 4 ngày. Kiểm tra giá trị quan sát có nằm trong khoảng không.
3. Tính khoảng Wilson cho SL và bỏ về quan sát từng giờ. Dùng kiểm định (ví dụ z hai tỉ lệ hoặc kiểm định χ² phù hợp) với hiệu chỉnh đa so sánh (Holm) để kết luận giờ nào lệch có ý nghĩa.
4. Bỏ đoạn giải thích nguyên nhân hoặc đổi thành "giả thuyết, cần kiểm chứng", và **kiểm chứng bằng dữ liệu** những gì có thể: E[S] theo giờ trên tập test, tỉ lệ VIP theo giờ, độ dài phục vụ lúc 15h–16h.
5. Nêu rõ trong kết luận: kiểm tra ngoài mẫu trên 4 ngày có **năng lực thống kê thấp**, chỉ có giá trị kiểm tra tính hợp lý.
6. Điều tra độ lệch với kiểm tra độc lập và báo cáo kết quả.

**Nghiệm thu.** `ngoai_mau_v3.csv` có khoảng dự báo, khoảng tin cậy quan sát, kết quả kiểm định có hiệu chỉnh. Không còn đoạn giải thích nguyên nhân thiếu bằng chứng.

---

## 4. Nhiệm vụ P1

### S7. "10/14 ngày thực tế đạt SLA" thiếu phương pháp và khoảng tin cậy

**Vấn đề.** Phần 5 ghi "10/14 ngày" (lịch 44, hụt ngày 1, 2, 7, 12) và "13/14" (lịch 48). Không nêu phương pháp. Nếu dùng số khách thực của từng ngày làm tốc độ đến rồi mô phỏng, nhiễu Poisson bị đếm hai lần (kết quả hơi bi quan). 10 trong 14 ngày thuộc tập train nên đây là kết quả **trong mẫu**. Kiểm tra độc lập cho lịch 44 đạt 9/14 (ngày 13 có SL 0,893, sát ngưỡng). Khoảng Wilson: 10/14 là [45%; 88%], 13/14 là [69%; 99%], 14/14 là [79%; 100%].

**Việc cần làm.** Ghi rõ phương pháp và số lần lặp; báo cáo SL từng ngày (cả 14 giá trị) và khoảng tin cậy; đánh dấu ngày thuộc train/test; nêu rõ đây là minh họa trong mẫu; thêm khoảng Wilson cho mọi tỉ lệ ngày. Không dùng tỉ lệ này như bằng chứng chính.

---

### S8. Kiểm chứng M/G/1: nói quá và thiếu năng lực kiểm định

**Vấn đề.**
1. "SimPy đúng tuyệt đối" ở Kiểm tra A: kết quả 13,87 ± 1,54 với giá trị đúng 14,625 chỉ cho thấy **không bác bỏ được**; khoảng tin cậy rộng ±11% nên kiểm định có năng lực thấp. Sai lệch −5,18% có thể do thiên lệch khởi động (chạy 5.000 phút, warm-up 500, ρ = 0,75, cv = 1,5, thời gian hồi phục dài). Kiểm tra độc lập với 40.000 phút và 40 lần lặp cho 14,82 ± 0,99.
2. Mọi khoảng tin cậy mô phỏng dùng hệ số 1,96. Với 30 lần lặp phải dùng `t(0,975; 29) = 2,045` (hẹp thiếu khoảng 4%); với 60 lần là 2,001.
3. Các khẳng định "mọi giờ ≥ 90%" dựa trên cận dưới từng giờ với z = 1,96. Cận dưới này đúng cho **từng giờ riêng lẻ**, không đồng thời cho cả 9 giờ. Muốn khẳng định đồng thời cần hiệu chỉnh (Bonferroni một phía với 9 giờ cho z ≈ 2,54).

**Việc cần làm.** Chạy lại Kiểm tra A với độ dài chạy và số lần lặp lớn hơn (≥ 40.000 phút, ≥ 40 lần lặp) và dùng warm-up được xác nhận bằng Welch cho cấu hình này; đổi lời văn thành "không bác bỏ"; thay 1,96 bằng giá trị t trong mọi khoảng tin cậy có dưới 100 lần lặp; thêm hiệu chỉnh đồng thời cho các kết luận "mọi giờ".

---

### S9. Mục 3.8: "CRN" không giảm phương sai và thiếu cột giờ tệ nhất

**Vấn đề.**
1. Khoảng tin cậy của hiệu số (±0,0044–0,0047) xấp xỉ `√2 × ` khoảng tin cậy từng cấu hình (±0,0030–0,0038). Điều này cho thấy các cấu hình thực tế **chạy độc lập**, không hưởng lợi từ số ngẫu nhiên chung, vì các bộ sinh thời gian phục vụ khác nhau tiêu thụ luồng ngẫu nhiên khác nhau.
2. Văn bản nói "cận dưới giờ tệ nhất của các cấu hình nằm sát ngưỡng 90%", nhưng bảng chỉ có SL toàn ngày; không có số liệu giờ tệ nhất.

**Việc cần làm.** Hoặc thực hiện CRN thật (rút số ngẫu nhiên đều dùng chung và đổi qua hàm phân phối ngược), hoặc đổi tên thành "so sánh độc lập" và ghi rõ; thêm cột SL giờ tệ nhất (cận dưới) cho từng cấu hình; chỉ giữ kết luận "sát ngưỡng" nếu số liệu hỗ trợ.

---

### S10. Các giả định phân phối chưa được kiểm định đầy đủ

**Vấn đề.**
1. **Kiên nhẫn của khách bỏ về** được giả định phân phối mũ và ước lượng bằng MLE, nhưng không có kiểm tra độ phù hợp. Có thể kiên nhẫn có tốc độ nguy cơ thay đổi theo thời gian chờ hoặc theo giờ (tỉ lệ bỏ về từ 2,4% đến 13,3% giữa các giờ).
2. **Phân phối thời gian phục vụ:** kết luận "Gamma/Lognormal tốt nhất, mũ bị bác bỏ" không kèm số liệu (AIC, KS) trong tài liệu. P-value KS khi tham số ước lượng từ chính mẫu bị lạc quan (cần Lilliefors hoặc bootstrap tham số).
3. Khoảng tin cậy của E[S] và θ giả định các quan sát độc lập; chưa xét tương quan trong cùng ngày hoặc cùng giờ.

**Việc cần làm.**
1. Vẽ ước lượng **Kaplan–Meier** (hoặc hàm nguy cơ) của thời gian kiên nhẫn có kiểm duyệt và so với đường mũ; kiểm định log-rank hoặc kiểm tra tốc độ nguy cơ không đổi; thử θ riêng theo khung giờ.
2. Đưa bảng AIC/BIC và KS (hiệu chỉnh bằng bootstrap tham số) cho các phân phối thời gian phục vụ vào tài liệu.
3. Ước lượng khoảng tin cậy E[S] và θ bằng bootstrap theo **ngày** (cluster bootstrap) và so với khoảng hiện tại.
4. Nếu giả định mũ cho bỏ về bị bác bỏ rõ rệt, chạy độ nhạy bằng mô hình kiên nhẫn khác (Weibull hoặc theo bảng KM).

---

### S11. Bảng chi phí: xếp hạng chính sách không xét sai số

**Vấn đề.** Mục 3.5 in đậm "chính sách rẻ nhất" cho từng k. Nhưng sai số của tỉ lệ bỏ về (±0,10–0,17 điểm phần trăm, tương đương ±0,7–1,2 khách/ngày) làm chi phí ở k = 0,5 có sai số khoảng ±0,5. Ở k = 0,5 các giá trị 60,81, 61,34, 61,38 chênh nhau trong phạm vi sai số.

**Việc cần làm.** Thêm khoảng tin cậy cho mỗi chi phí (truyền từ sai số bỏ về); dùng **hiệu số theo cặp** giữa các chính sách với khoảng tin cậy để kết luận chính sách nào rẻ hơn **có ý nghĩa**; chỉ in đậm khi khác biệt có ý nghĩa; ngược lại ghi "không phân biệt được". Nêu rõ đơn giá k là giả định.

---

## 5. Sửa số liệu mâu thuẫn và lời văn (P1)

### C1. Phần 5 không khớp mục 3.3(b)
Cột "Mốc cơ sở" ghi `99,4%` (ngày đạt) và `77,8%` (mọi giờ), nhưng 3.3(b) ghi `100,0%` và `78,0%`. Lịch 44 và 48 khớp (85,0/26,0 và 95,3/47,0). Thống nhất giá trị theo CSV mới và thêm khoảng tin cậy.

### C2. "86,5%" không có trong bảng nào
Phần 5 ghi lịch tối ưu "giờ đỉnh rơi xuống 86,5%" khi nhu cầu tăng 10%. Mục 3.4 ghi `0,8843`. (Kiểm tra độc lập: 0,857.) Dùng giá trị từ CSV hiện hành và thay tên cột cho đúng ("SL giờ tệ nhất, cận dưới CI95").

### C3. Mục 3.5 còn dòng "Theo ca" cũ
Mục 3.5 vẫn ghi "Theo ca làm việc: 52 quầy-giờ, bỏ về 2,72%", trong khi mục 3.3(a) và Phần 5 dùng "Theo ca (MILP hỗn hợp) = 44 quầy-giờ, bỏ về 5,35%". Chạy lại chi phí cho đúng lịch hiện dùng hoặc bỏ dòng này; thống nhất số liệu toàn tài liệu. Cùng lúc, hai dòng "SIPP" và "Tối ưu" (cùng lịch) cần gộp hoặc ghi rõ là một.

### C4. Phần 5, cột "Mốc cơ sở": nhân sự và cơ sở tính chi phí sai
- Ghi "6 NV 8h (nghỉ trưa 1–7: 6 NV làm việc 48 q-h)" cho lịch hằng số 6 quầy. Theo mục 3.6, phủ `[6]*9` cần **7 nhân viên, 56 quầy-giờ làm việc** (63 giờ có mặt). 6 nhân viên có nghỉ chỉ phủ `[6,5,6,5,5,5,5,5,6]` (48 quầy-giờ).
- Mức "tiết kiệm 18,52%" tính theo **giờ quầy mở** (44 so với 54), trong khi các phần ca làm việc dùng **giờ công làm việc** và **giờ có mặt**. Phải thống nhất một cơ sở tính chi phí và tính lại (ví dụ cùng dùng giờ công làm việc: 44 so với 56 cho cùng hệ thống ca). Ghi rõ cơ sở đã chọn.

### C5. Phần 5, cột "Dự phòng": giả định giờ nghỉ cho lịch 48
"5 NV 8h + 2 NV 4h phủ chính xác 48 q-h" **không có nghiệm nếu giờ nghỉ chỉ nằm trong 11h–14h**; chỉ có nghiệm khi cho một số nhân viên nghỉ ngoài khung đó (cửa sổ giờ 1–7, kiểm tra độc lập: 4 nghiệm). Cần ghi rõ cửa sổ nghỉ giả định cho từng phương án hoặc đổi phương án.

### C6. Phát biểu quá mạnh
- "SimPy đúng tuyệt đối" → "không bác bỏ được tính đúng (xem S8)".
- Lịch 44 "đạt mục tiêu ≥ 90%" ở giờ tệ nhất → chỉ đúng với tham số danh nghĩa; ghi thêm xác suất đạt theo bootstrap (S5) và theo biến động ngày (S2).
- Lịch 48 "biên an toàn tốt" ở giờ tệ nhất (93,64%) và "giữ vững ≥ 90,0%" ở nhu cầu +10% (đúng bằng ngưỡng 0,9000) → bỏ các cụm này; thay bằng số liệu và khoảng tin cậy.
- "Pha 3 xác nhận không có lịch khả thi nhỏ hơn 44" → hiện không có dữ liệu minh chứng; thêm `results/.../pha3.csv` (các lịch đã thử, kết quả) hoặc bỏ câu này.
- Mục lục ghi "pytest 12/12" trong khi nội dung là 18/18; sửa cho khớp.
- Chênh lệch nhỏ: phương sai tổng ngày ghi 7.591,8 (kiểm tra độc lập 7.586,7 với n−1); xác nhận công thức tính.

### C7. Tự động hóa và kiểm thử
1. `tools/build_tables.py` sinh mọi bảng từ CSV; `tools/check_consistency.py` đối chiếu số trong tài liệu với CSV và báo lỗi nếu lệch (đã yêu cầu ở đợt 1, kiểm tra lại thật sự có chạy).
2. Thêm kiểm thử thống kê **có tính đến ngẫu nhiên**: so sánh mô phỏng với lý thuyết bằng kiểm định (lý thuyết nằm trong khoảng tin cậy với hạt giống cố định), không dùng sai số tuyệt đối cố định.
3. Thêm kiểm thử cho: khoảng tin cậy t của λ_h (S1), chỉ số kỳ vọng có điều kiện (S2), phân rã phương sai (S5), khoảng Wilson.
4. Lưu log `pytest -v` vào `results/final_v3/pytest_log.txt`.

---

## 6. Thứ tự thực hiện đề xuất

1. S1 (khoảng tin cậy λ_h) → S3 (CV ngày, mô hình hệ số nhân).
2. S2 (chỉ số kỳ vọng) → S4 (quy tắc vận hành) → chạy lại đánh giá chính sách.
3. S5 (bootstrap lồng nhau) → S6 (ngoài mẫu).
4. S8, S9, S10, S11.
5. C1–C6 (sửa số liệu và lời văn, dựa trên kết quả mới).
6. C7, đóng băng `final_v3`.

Không bắt đầu C1–C6 trước khi xong S1–S6, vì số liệu và kết luận phụ thuộc vào đó.

---

## 7. Tiêu chí nghiệm thu tổng

- [ ] Không còn khoảng tin cậy Poisson cho λ_h (S1).
- [ ] Chỉ số "mọi giờ" được định nghĩa theo kỳ vọng có điều kiện, kèm khoảng tin cậy (S2).
- [ ] Có độ nhạy theo CV ngày và kiểm tra mức phù hợp của mô hình nhu cầu (S3).
- [ ] Quy tắc vận hành (nếu còn) có ngưỡng và mức tiết kiệm tính từ mô phỏng; bộ dự báo có sai số (S4).
- [ ] Bootstrap lồng nhau có phân rã phương sai, định nghĩa chỉ số thống nhất (S5).
- [ ] Kiểm tra ngoài mẫu có khoảng dự báo và kiểm định hiệu chỉnh đa so sánh (S6).
- [ ] Mọi tỉ lệ kèm khoảng Wilson; mọi trung bình mô phỏng dùng t khi < 100 lần lặp (S7, S8).
- [ ] Bảng chi phí chỉ kết luận khi khác biệt có ý nghĩa (S11).
- [ ] Phần 5 và các mục 3.x khớp tuyệt đối với CSV (C1–C5).
- [ ] Không còn "đúng tuyệt đối", "biên an toàn tốt", "đạt mục tiêu" khi chưa có bằng chứng (C6).
- [ ] `results/final_v3/`, `CHANGELOG.md`, `docs/BAO_CAO_SUA_DOI_V2.md`, log pytest đã tạo.

---

## 8. Mẫu báo cáo cuối của agent (`docs/BAO_CAO_SUA_DOI_V2.md`)

```
# Báo cáo sửa đổi đợt 2

## 1. Tóm tắt
- Số nhiệm vụ hoàn thành / tổng:
- Kết luận nào thay đổi so với bản trước (kèm số trước và sau):

## 2. Chi tiết từng nhiệm vụ
| ID | Trạng thái | File sửa | Số trước → sau | Ghi chú |
|----|------------|----------|----------------|---------|

## 3. Kết quả mới quan trọng
- Khoảng tin cậy λ_h mới (S1):
- P(SL kỳ vọng ngày ≥ 90%), P(SL kỳ vọng mọi giờ ≥ 90%) theo CV ngày {8,12,16,20}% (S2, S3):
- Ngưỡng vận hành, bộ dự báo, mức tiết kiệm thực tế (S4):
- Phân rã phương sai bootstrap (S5):
- Khoảng dự báo ngoài mẫu và giờ lệch có ý nghĩa (S6):

## 4. Việc chưa làm được và thông tin cần bổ sung

## 5. Rủi ro còn lại
```

---

## 9. Phụ lục: số liệu tham chiếu từ kiểm tra độc lập

Chỉ để đối chiếu **sau khi tự chạy**. Không sao chép. Nếu kết quả của agent lệch đáng kể, phải điều tra nguyên nhân trước khi chấp nhận. Mô phỏng tham chiếu dùng phân phối Gamma (E[S] = 2,9236; cv = 1,0963), θ = 0,1087, p_vip = 0,3543, λ_h trung bình 10 ngày train.

**Phân tán tổng ngày.** Trung bình 702,6; độ lệch chuẩn 87,1; Poisson 26,5; D = 140,4 (13 bậc tự do); khoảng tin cậy 95% của `CV_ngày²` là [0,0067; 0,0385], tức `CV_ngày` thuộc [8,2%; 19,6%].

**Tương quan dự báo.** Số khách 8h–10h so với 10h–17h: r = 0,74 (p = 0,002). 8h–11h so với phần còn lại: r = 0,61 (p = 0,021). Tương quan cặp giữa các giờ: trung bình 0,45 (từ −0,07 đến 0,77).

**Khác biệt train/test.** Tổng ngày train: trung bình 686,7, độ lệch chuẩn 99,7. Test: 742,3 và 10,9. Welch: t = 1,74, p = 0,115. Số ngày có tổng ≤ 687: 5/14 (train 5/10, test 0/4).

**Chỉ số "mọi giờ ≥ 90%" (nhiễu lấy mẫu).** Không có biến động ngày, 300 ngày: 6 quầy 0,76; lịch 44 0,12; lịch 48 0,34. Với hệ số nhân ngày Gamma CV 11,8% (40 kịch bản × 25 lần lặp):

| Lịch | P(SL kỳ vọng ngày ≥ 90%) | P(SL kỳ vọng mọi giờ ≥ 90%) | P(mọi giờ thực tế ≥ 90%) |
|---|---|---|---|
| 6 quầy | 1,000 | 0,975 | 0,666 |
| 44 | 0,850 | 0,575 | 0,191 |
| 48 | 0,975 | 0,750 | 0,360 |

Các tỉ lệ này có sai số Monte Carlo khoảng ±5 đến ±15 điểm tùy cỡ mẫu kịch bản; chạy lại với nhiều kịch bản hơn.

**Phân rã nhiễu mô phỏng (lịch 44).** Độ lệch chuẩn mỗi lần lặp SL ngày khoảng 0,0203. Tỉ lệ phương sai bootstrap (độ lệch chuẩn quan sát 0,0051) do nhiễu mô phỏng nếu mỗi bộ chỉ có 20, 30, 50, 60 lần lặp: 79%, 53%, 32%, 26%.

**Khoảng Wilson.** 50/50: [92,9%; 100%]. 3/50: [2,1%; 16,2%]. 19/50: [25,9%; 51,8%]. 10/14: [45,3%; 88,3%]. 13/14: [68,5%; 98,7%]. 14/14: [78,5%; 100%].

**Quầy-giờ kỳ vọng theo quy tắc ngưỡng 687 (5/14 ngày dùng lịch 44, 9/14 dùng lịch 48).** 46,6; tiết kiệm 13,8% so với 54.

**Kiểm tra M/G/1 (cv = 1,5, ρ = 0,75).** Lý thuyết 14,625; mô phỏng 14,82 ± 0,99 (40 lần lặp, 40.000 phút).

**Mô phỏng lịch 44 tại λ_test, tham số train.** SL toàn ngày 0,906; bỏ về 7,65%; Wq 0,70 phút (200 lần lặp). SL theo giờ: 0,921; 0,886; 0,891; 0,866; 0,935; 0,932; 0,936; 0,939; 0,904.
