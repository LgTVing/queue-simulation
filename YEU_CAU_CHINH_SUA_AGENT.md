# YÊU CẦU CHỈNH SỬA DỰ ÁN (dành cho Agent)

> **Cách dùng:** đặt file này ở thư mục gốc dự án, rồi giao cho agent câu lệnh sau:
> *"Đọc `YEU_CAU_CHINH_SUA_AGENT.md` và thực hiện lần lượt từng nhiệm vụ từ P0 đến P2. Tuân thủ mục 'Quy tắc bắt buộc'. Cuối cùng nộp `docs/BAO_CAO_SUA_DOI.md` theo mẫu ở mục 6."*

---

## 0. Bối cảnh

Dự án: mô phỏng hàng đợi và xác định số quầy tối ưu cho chi nhánh ngân hàng (dữ liệu thật 14 ngày, 9 khung giờ 8h–17h, SLA: ≥ 90% khách được phục vụ trong ≤ 5 phút; VIP ≤ 2 phút).

Một đợt kiểm tra độc lập (tính lại số liệu và chạy lại mô phỏng) đã kết luận:

- **Phần đúng, không cần đụng tới:** số liệu dữ liệu thô và thống kê theo giờ, 3 file Excel (Erlang C, `Tra_c`, Allen–Cunneen, `Quyet_dinh`), hàm giải tích `b_theory.py`, bảng chi phí (3.5), bảng kiểm chứng ba tầng (3.1), tính nhất quán số học của các bảng.
- **Phần cần sửa:** một số kết luận bị nói quá hoặc mâu thuẫn với chính số liệu, một số nhãn kiểm định sai, phần ca làm việc chưa nhất quán, và mô hình chưa tính đến biến động lưu lượng giữa các ngày.

**Mục tiêu của đợt chỉnh sửa:** làm cho kết luận **trung thực với số liệu**. Không nhằm làm số liệu "đẹp hơn".

---

## 1. Quy tắc bắt buộc

1. **Không bịa và không chỉnh số cho đẹp.** Mọi con số trong báo cáo, slide, bảng tổng hợp phải sinh ra từ lần chạy lại và được trích **tự động** từ file CSV (xem T14). Cấm gõ tay số từ trí nhớ.
2. **Không đổi hạt giống (seed), số lần lặp hay tiêu chí chỉ để kết quả đạt SLA.** Nếu thay đổi cấu hình phải ghi lý do trong `CHANGELOG.md`.
3. **Giữ nguyên `results/final_v1/`** làm bản lưu. Kết quả mới ghi vào `results/final_v2/`, kèm `MO_TA.md` (ngày chạy, version `params.json`, seed, số lần lặp, commit).
4. **Không sửa dữ liệu thô** trong `data/raw/`.
5. Mỗi nhiệm vụ làm trên nhánh hoặc commit riêng, thông báo rõ **số trước và số sau** khi một con số thay đổi.
6. Nếu kết quả mới **làm yếu hoặc đảo ngược một kết luận cũ**, phải sửa kết luận và nói rõ trong báo cáo, không giữ câu chữ cũ.
7. Nếu không làm được một việc (thiếu dữ liệu, thiếu thông tin), **không tự giả định**. Ghi vào mục "Việc chưa làm được" và nêu thông tin cần bổ sung.
8. Giữ nguyên quy ước chỉ số giờ: giờ 0 = 8h–9h, giờ 8 = 16h–17h.
9. Sau mọi thay đổi code phải chạy `pytest tests/` và đính kèm log.

---

## 2. Danh sách nhiệm vụ

| ID | Mức | Nhiệm vụ ngắn gọn |
|---|---|---|
| T1 | P0 | Sửa nhãn kiểm định Poisson và thêm kiểm định quá phân tán theo ngày |
| T2 | P0 | Đưa biến động lưu lượng theo ngày vào mô hình và đánh giá lại các lịch |
| T3 | P0 | Sửa các con số mâu thuẫn và lời văn quá mạnh ở Phần 5 (khuyến nghị cuối) |
| T4 | P0 | Làm lại kiểm tra ngoài mẫu (3.9) cho công bằng và có tài liệu hóa |
| T5 | P0 | Sửa bài toán ca làm việc (MILP) và các số liên quan |
| T6 | P1 | Điều tra độ lệch nhỏ giữa mô phỏng của nhóm và mô phỏng kiểm tra độc lập |
| T7 | P1 | Sửa diễn giải bước tối ưu và mở rộng tìm kiếm |
| T8 | P1 | Sửa cách kết luận ở độ nhạy theo phân phối (3.8) |
| T9 | P1 | Làm rõ và đồng bộ chỉ số trong phân tích độ bất định tham số (3.7) |
| T10 | P1 | Sửa thuật ngữ và các khẳng định không có căn cứ trong dữ liệu |
| T11 | P1 | Làm rõ bộ tham số dùng cho từng thành phần |
| T12 | P1 | Xử lý tỉ lệ VIP thay đổi theo giờ |
| T13 | P2 | Bổ sung kiểm thử và log pytest |
| T14 | P2 | Tự động hóa việc tạo bảng và cập nhật toàn bộ tài liệu |

---

## 3. Chi tiết nhiệm vụ P0

### T1. Sửa nhãn kiểm định Poisson và thêm kiểm định quá phân tán

**Vấn đề.** Trong `docs/thong_ke_mo_ta.xlsx` (sheet `Thong_ke_theo_gio`) và `docs/bang_tham_so.xlsx`, cột "Kết luận Poisson" ghi **"Chưa bác bỏ"** cho các giờ có p-value 0,0356 (8h), 0,0352 (9h), 0,0141 (16h). Ở mức ý nghĩa 5% các giờ này **bị bác bỏ**. Số liệu đúng: **8/9 giờ bác bỏ Poisson ở mức 5%**, 5/9 giờ ở mức 1% (chỉ giờ 12h–13h, p = 0,0763, chưa bác bỏ). Nhãn "Lệch nhẹ" cho p ≈ 0 cũng không chính xác.

Ngoài ra tổng số khách mỗi ngày dao động mạnh: trung bình 702,6, độ lệch chuẩn khoảng 87, trong khi Poisson chỉ cho khoảng 26,5 (phương sai gấp khoảng 10,8 lần trung bình, CV theo ngày khoảng 12%). Dữ liệu **quá phân tán** so với Poisson thuần.

**Việc cần làm.**
1. Gắn nhãn theo quy tắc rõ ràng: `p < 0,01` = "Bác bỏ (mạnh)", `0,01 ≤ p < 0,05` = "Bác bỏ (nhẹ)", `p ≥ 0,05` = "Chưa bác bỏ". Ghi mức ý nghĩa trong chú thích.
2. Thêm vào cả hai file Excel và `docs/uoc_luong_kiem_dinh.md`:
   - tổng số khách mỗi ngày, trung bình, độ lệch chuẩn, tỉ số phương sai/trung bình, CV;
   - kiểm định quá phân tán cho tổng ngày;
   - ước lượng CV của hệ số nhân ngày sau khi trừ nhiễu Poisson: `CV_ngày² = (Var(N_d) − μ) / μ²` với `N_d` là tổng khách ngày d và `μ` là trung bình.
3. Cập nhật Mục 3, 4 của báo cáo và slide 3–5 cho đúng. Nêu thẳng: giả định "Poisson với λ_h cố định" **không đúng hoàn toàn**, và hệ quả là mô phỏng hiện tại có thể đánh giá cao mức dịch vụ.

**Nghiệm thu.** Không còn nhãn "Chưa bác bỏ" cho p < 0,05. Có bảng thống kê tổng ngày và CV ngày. Báo cáo và slide đã sửa.

---

### T2. Đưa biến động lưu lượng theo ngày vào mô hình

**Vấn đề.** Mô phỏng dùng λ_h cố định cho mọi ngày. Khi tôi mô phỏng lại các lịch trên **từng ngày quan sát** (dùng số khách thực của ngày đó làm tốc độ đến, 40 lần lặp mỗi ngày), kết quả như sau (ước lượng hơi bi quan vì cộng thêm nhiễu Poisson):

| Lịch | Ngày đạt SL toàn ngày ≥ 90% | Ngày mà mọi giờ đều ≥ 90% |
|---|---|---|
| Tối ưu 44 quầy-giờ | 9/14 | 4/14 |
| Bền vững 48 quầy-giờ | 13/14 | 5/14 |
| Hằng số 6 quầy | 14/14 | 8/14 |

Các ngày đông (ngày 1, 2, 7 với 776–826 khách) là ngày kém nhất. Báo cáo hiện tại chưa phản ánh điều này.

**Việc cần làm.**
1. Thêm tùy chọn vào `c_sim.py`: **hệ số nhân ngày** `m_d` (trung bình 1, CV = `CV_ngày` ước lượng ở T1), phân phối Gamma hoặc lognormal, nhân vào mọi λ_h của một ngày mô phỏng. Mặc định tắt để tái lập kết quả cũ.
2. Chạy lại **đánh giá chính sách** (hằng số, SIPP/Sim-opt, bền vững, theo ca) với hệ số nhân ngày bật, 300 lần lặp, seed mới (ghi vào `final_v2`).
3. Với mỗi chính sách báo cáo thêm: `P(SL toàn ngày ≥ 90%)`, `P(mọi giờ ≥ 90%)` (xác suất trên các ngày mô phỏng), trung bình và phân vị 5%–95% của `SL` toàn ngày, và số giờ trung bình dưới 90% mỗi ngày.
4. Làm thêm bản **mô phỏng theo từng ngày quan sát** (14 ngày thật) làm đối chiếu, ghi rõ giới hạn (nhiễu Poisson bị đếm hai lần).
5. Đề xuất **quy tắc chọn lịch theo lưu lượng dự kiến** (xem T10).
6. Cập nhật kết luận (mục khuyến nghị) theo kết quả mới.

**Nghiệm thu.** Có `results/final_v2/theo_ngay.csv` và bảng so sánh chính sách mới. Khuyến nghị nêu rõ lịch 44 chỉ đảm bảo cho ngày trung bình, kèm xác suất đạt SLA.

---

### T3. Sửa các con số mâu thuẫn và lời văn quá mạnh ở Phần 5

**Vấn đề (cụ thể).**
- "Độ bền khi nhu cầu +10%: giờ đỉnh rơi xuống **86,5%**" cho lịch tối ưu. Bảng 3.4 (`do_nhay.csv`) cho giá trị **0,8843**. Số 86,5% không có trong bảng nào.
- Lịch bền vững được ghi "**biên an toàn rất cao**" cho giờ tệ nhất (93,64%), trong khi mục 3.7 cho thấy chỉ **38%** bộ tham số (19/50) đạt điều kiện giờ tệ nhất ≥ 90% (lịch 44 chỉ 6%, 3/50).
- Ở nhu cầu +10%, lịch bền vững được ghi "giữ vững ≥ 90,0%", trong khi giá trị là **0,9000 (sát ngưỡng)**, kết quả tái lập độc lập cho 0,893.
- Khi thời gian phục vụ tăng 10%, cả hai lịch đều **không** giữ được mức 90% ở giờ tệ nhất (0,8685 và 0,8977), điều này chưa được nêu.
- "Tiết kiệm 18,52%" tính so với "Hiện trạng" (xem T10).

**Việc cần làm.**
1. Rà soát **mọi** con số trong `TONG_HOP_SO_LIEU_CHI_TIET.md`, `docs/bao_cao_tong_ket.md`, `docs/slide_thuyet_trinh.md` và đối chiếu với CSV trong `results/final_v2/`. Lập bảng các chỗ lệch.
2. Sửa Phần 5 theo hướng:
   - ghi riêng "SL giờ tệ nhất (cận dưới CI95, tham số danh nghĩa)" và "xác suất đạt điều kiện giờ tệ nhất khi tham số dao động";
   - không dùng các cụm "biên an toàn rất cao", "giữ vững" khi giá trị sát hoặc dưới ngưỡng;
   - thêm độ nhạy theo E[S] (+10%) và kết quả của T2.
3. Mỗi khẳng định bằng lời phải trỏ tới đúng một dòng CSV (ghi tên file và dòng).

**Nghiệm thu.** Không còn số nào trong tài liệu không truy được về CSV. Không còn mâu thuẫn giữa Phần 5 và các mục 3.3, 3.4, 3.7.

---

### T4. Làm lại kiểm tra ngoài mẫu (mục 3.9)

**Vấn đề.**
1. Cột "SL thực tế quan sát" xảy ra dưới **nhân sự thực** (không biết trong tài liệu), còn cột mô phỏng chạy **lịch khuyến nghị**. Hai cột này không so sánh trực tiếp được.
2. Ở mức tổng, kết quả khớp: SL mô phỏng ≈ 0,930 so với thực tế ≈ 0,929, bỏ về ≈ 6,3% so với 6,1%, Wq ≈ 0,50 so với 0,49 (trung bình có trọng số theo λ_test). Nhưng **từng giờ lệch rất mạnh** (15h–16h: mô phỏng 0,951, thực tế 0,765; 8h–9h: 0,936 và 0,981). Tài liệu chưa nói rõ điều này.
3. Khi kiểm tra độc lập chạy lịch 44 với tham số train tại λ_test, kết quả là **SL toàn ngày ≈ 0,906, bỏ về ≈ 7,65%, Wq ≈ 0,70**, các giờ 9–10h, 10–11h, 11–12h, 16–17h xấp xỉ hoặc dưới 0,90 (SL theo giờ khoảng 0,921, 0,886, 0,891, 0,866, 0,935, 0,932, 0,936, 0,939, 0,904). Con số của nhóm cao hơn đáng kể mà không có giải thích về bộ tham số đã dùng cho tập test.
4. Nhu cầu ngày test cao hơn ngày train 10–25% ở các giờ 8h–12h. Theo bảng của nhóm, giờ 11–12h có cận dưới 0,8888 dưới ngưỡng, tức lịch 44 **không đạt** ở nhu cầu của ngày test. Điều này chưa được nêu.

**Việc cần làm.**
1. Ghi vào `docs/ngoai_mau.md` chính xác tham số dùng cho phần mô phỏng của tập test: λ (train hay test), E[S], phân phối, θ, p_vip, số lần lặp, seed.
2. Chạy **hai phiên bản**: (a) tham số train với λ_test; (b) tất cả tham số ước lượng trên tập test. Báo cáo cả hai.
3. Kiểm tra xem dữ liệu có cho phép **suy ra nhân sự thực theo giờ** hay không (ví dụ số nhân viên phân biệt phục vụ trong mỗi giờ). Nếu có: chạy mô phỏng với lịch thực để so sánh công bằng. Nếu không: ghi rõ đây là so sánh **không cùng điều kiện**, chỉ có giá trị ở mức tổng.
4. Thêm hai cột "chênh lệch" và nhận xét theo giờ. Nêu rõ giờ nào lệch lớn (15h–16h) và các nguyên nhân khả dĩ (nhân sự thực khác lịch, biến động ngày, bỏ về).
5. Nêu rõ trong kết luận: ở nhu cầu của ngày test, lịch 44 không đạt mọi giờ, ủng hộ việc dùng lịch dự phòng khi lưu lượng cao.

**Nghiệm thu.** `ngoai_mau.csv` có cả hai phiên bản và cột chênh lệch. Có mô tả đầy đủ tham số. Báo cáo không dùng từ "kiểm chứng" cho phần so sánh theo giờ nếu điều kiện không giống nhau.

---

### T5. Sửa bài toán ca làm việc (MILP) và các số liên quan

**Vấn đề (kiểm tra độc lập, kèm tiêu chí).** Cần định nghĩa rõ hai cách hiểu "ca 8 giờ":
- **Mô hình A:** 8 giờ làm việc **liên tục**, bắt đầu giờ 0 hoặc giờ 1.
- **Mô hình B:** có mặt 9 giờ, **nghỉ 1 giờ** (nghỉ trưa), làm 8 giờ; giờ nghỉ nằm trong một cửa sổ cho phép (ví dụ giờ 3–5 tức 11h–14h).

Ca 4 giờ: 4 giờ liên tục, bắt đầu giờ 0 đến giờ 5.

Các kết quả hiện tại có chỗ không nhất quán:
- "4 NV 8h + 3 NV 4h phủ đúng `[4,5,6,5,5,5,5,5,4]`": **không có nghiệm** ở mô hình A. Ở mô hình B có nghiệm duy nhất khi giờ nghỉ nằm trong giờ 3–5. Chưa nêu giả định.
- "5 NV 8h + 2 NV 4h phủ đúng `[5,6,6,6,5,5,5,5,5]` (48 q-h)": ở mô hình B **không có nghiệm** nếu giờ nghỉ chỉ trong giờ 3–5. Chỉ có nghiệm khi một số giờ nghỉ nằm ngoài 11h–14h.
- "6 NV 8h cố định" cho lịch hằng số 6 quầy (54 q-h): **không thể** phủ 6 quầy ở cả 9 giờ. Cần 7 nhân viên (có nghỉ).
- "Chỉ ca 8h = 64 quầy-giờ (`[8,8,8,6,5,5,8,8,8]`)": không tối thiểu. Ở mô hình B, **6 nhân viên** phủ được lịch 44 với 48 quầy-giờ (`[6,5,6,5,5,5,5,5,6]`). Ở mô hình A, nghiệm tối thiểu là **64** nhưng với mẫu phủ `[4,8,8,8,8,8,8,8,4]`. Mẫu `[8,8,8,6,5,5,8,8,8]` không phải nghiệm tối ưu của cả hai mô hình.
- Chính sách "Theo ca làm việc" trong 3.3 và 3.5 dùng lịch `[6,6,6,6,5,5,6,6,6]` (52), **không phải** kết quả của 3.6, và mâu thuẫn với dòng "chi phí phụ trội +0,0%" ở Phần 5.
- Chi phí cần thống nhất đo bằng **giờ công làm việc** hay **giờ có mặt có lương**.

**Kết quả đúng để đối chiếu (không được copy, phải tái tạo bằng MILP của nhóm):**

| Trường hợp | Kết quả đúng |
|---|---|
| Chỉ ca 4 giờ, phủ ≥ `[4,5,6,5,5,5,5,5,4]` | Tối thiểu **52** quầy-giờ, mẫu phủ `[4,5,6,6,5,8,7,7,4]` |
| Chỉ ca 8 giờ liên tục (mô hình A) | Tối thiểu **64**, mẫu phủ `[4,8,8,8,8,8,8,8,4]` |
| Chỉ ca 8 giờ có nghỉ 1 giờ (mô hình B, nghỉ giờ 1–7) | 6 NV, **48** quầy-giờ, ví dụ mẫu phủ `[6,5,6,5,5,5,5,5,6]` |
| 4 NV 8h + 3 NV 4h, phủ đúng 44 | Mô hình A: không có nghiệm. Mô hình B, nghỉ giờ 3–5: 1 nghiệm |
| 5 NV 8h + 2 NV 4h, phủ đúng `[5,6,6,6,5,5,5,5,5]` | Mô hình B, nghỉ giờ 3–5: không nghiệm. Nghỉ giờ 1–7: có 4 nghiệm |
| Phủ `[6]*9` | Mô hình B cần **7** NV (không thể với 6) |

**Việc cần làm.**
1. Viết lại `lich_theo_ca` (module của thành viên B) với **cấu hình tường minh**: chọn mô hình A hoặc B, cửa sổ giờ nghỉ, các loại ca, cách tính chi phí. Mặc định dùng mô hình B với giờ nghỉ trong giờ 3–5 và ghi rõ.
2. Giải lại cho các trường hợp trong bảng trên, so với kết quả đúng ở trên. Nếu khác, tìm lỗi trong mô hình MILP chứ không điều chỉnh bảng đối chiếu.
3. Với mỗi phương án ca ghi: số nhân viên theo từng loại ca, lịch quầy thực tế theo giờ, giờ công làm việc, giờ có mặt có lương, chi phí tăng so với lịch lý tưởng 44.
4. Chạy mô phỏng **chính các lịch thực tế này** và dùng chúng làm chính sách "Theo ca làm việc" trong 3.3 và 3.5 (thay `[6,6,6,6,5,5,6,6,6]` nếu không phải kết quả của MILP).
5. Sửa Phần 5: số nhân viên của từng phương án, chi phí phụ trội, giả định về giờ nghỉ.

**Nghiệm thu.** `lich_theo_ca.csv` khớp bảng đối chiếu. Số nhân viên và chi phí nhất quán giữa 3.3, 3.5, 3.6 và Phần 5. Có test tự động cho các trường hợp trên (xem T13).

---

## 4. Chi tiết nhiệm vụ P1

### T6. Điều tra độ lệch nhỏ giữa mô phỏng của nhóm và mô phỏng kiểm tra độc lập

**Vấn đề.** Mô phỏng độc lập (Gamma với E[S] = 2,9236, cv = 1,0963, θ = 0,1087, p_vip = 0,3543, λ_h trung bình 10 ngày train, 300 lần lặp) cho kết quả thấp hơn khoảng 0,3–0,5 điểm SL và cao hơn khoảng 0,2–0,35 điểm bỏ về so với `so_sanh_chinh_sach.csv`:

| Chính sách | SL (nhóm → độc lập) | Bỏ về (nhóm → độc lập) | Giờ tệ nhất, cận dưới (nhóm → độc lập) |
|---|---|---|---|
| Hằng số 6 | 0,9770 → 0,9743 | 2,15% → 2,36% | 0,9557 → 0,9483 |
| Tối ưu 44 | 0,9381 → 0,9328 | 5,35% → 5,69% | 0,9078 → 0,9076 |
| Bền vững 48 | 0,9582 → 0,9543 | 3,73% → 4,02% | 0,9364 → 0,9276 |
| Theo ca 52 | 0,9702 → 0,9672 | 2,72% → 2,95% | 0,9453 → 0,9397 |

Độ lệch nhỏ và kết luận không đổi, nhưng lớn hơn khoảng tin cậy nên cần giải thích.

**Việc cần làm.** Kiểm tra lần lượt và ghi kết quả vào `docs/doi_chieu_mo_phong.md`:
1. Bộ lấy mẫu thời gian phục vụ thực sự dùng (Gamma hay bootstrap hay hỗn hợp), tham số hình dạng/tỉ lệ.
2. λ_h dùng trong mô phỏng (đọc từ `params.json` hay trung bình train) và có làm trơn không.
3. Cách xử lý VIP (ưu tiên không ngắt, ngưỡng 2 phút) và cách tính `SL` toàn ngày (mẫu số là mọi khách đến).
4. Cách tính thời gian chờ của khách bỏ về.
5. Ảnh hưởng của hạt giống: chạy lại với 3 khối seed khác nhau, báo cáo dao động.
Nếu tìm ra nguyên nhân, nêu rõ. Nếu không, ghi nhận là chênh lệch nhỏ chưa giải thích được.

**Nghiệm thu.** Có tài liệu đối chiếu. Dao động theo seed đã được ước lượng.

---

### T7. Sửa diễn giải bước tối ưu và mở rộng tìm kiếm

**Vấn đề.**
- Báo cáo ghi lịch 44 là "nghiệm tối thiểu **toàn cục** chặt chẽ". Thuật toán chỉ thử **bớt 1 quầy ở từng giờ** (tối thiểu cục bộ), không thử hoán đổi (bớt 1 ở giờ i, thêm 1 ở giờ j), cũng không thử bớt nhiều giờ cùng lúc.
- Lịch "Tối ưu mô phỏng" **trùng hoàn toàn** lịch SIPP (lịch ban đầu đã đạt ngay ở bước 0). Hai dòng trong bảng 3.3 giống nhau từng chữ số, nên mô phỏng chỉ **xác nhận** SIPP.

**Việc cần làm.**
1. Sửa lời văn thành "tối thiểu cục bộ theo thuật toán 2 pha (bớt từng quầy)".
2. Thêm pha 3 vào `optimize_schedule`: thử hoán đổi một quầy giữa hai giờ và thử bớt cặp giờ. Dùng cùng CRN và tiêu chí `feasible`. Báo cáo có tìm thấy lịch tốt hơn hay không.
3. Trong bảng so sánh chính sách, gộp hoặc ghi rõ hai dòng SIPP và Sim-opt là cùng một lịch ("SIPP, được mô phỏng xác nhận").

**Nghiệm thu.** Báo cáo không còn chữ "toàn cục" nếu chưa chứng minh. Nêu kết quả pha 3.

---

### T8. Sửa cách kết luận ở độ nhạy theo phân phối (3.8)

**Vấn đề.** Phân phối mũ bị ghi "KHÔNG ĐẠT" với cận dưới 0,8997 (sát ngưỡng 0,90). Mũ cho SL thấp hơn Gamma (0,9362 so với 0,9393) dù ít biến thiên hơn, nhưng hiệu này nằm trong sai số (±0,0034 đến ±0,0037). Gắn nhãn cứng ở mức này gây hiểu lầm.

**Việc cần làm.**
1. Tính **hiệu số so với cấu hình gốc** (Gamma) với CRN, kèm khoảng tin cậy 95% của hiệu số, thay vì chỉ so từng khoảng tin cậy.
2. Phân loại: "khác biệt có ý nghĩa" khi khoảng tin cậy của hiệu số không chứa 0. Ghi cận dưới giờ tệ nhất nhưng không gắn nhãn đạt/không đạt riêng cho các trường hợp sát ngưỡng.
3. Kết luận: lịch 44 **nhạy** với giả định phân phối (hai trên bốn cấu hình có cận dưới giờ tệ nhất dưới 0,90), nên cần dự phòng.

**Nghiệm thu.** Bảng 3.8 có cột hiệu số và khoảng tin cậy. Kết luận được viết lại.

---

### T9. Làm rõ và đồng bộ chỉ số trong phân tích độ bất định (3.7)

**Vấn đề.** Hai chỉ số "SL giờ tệ nhất" đang được định nghĩa khác nhau mà không nói rõ:
- Bảng 3.3: giá trị **nhỏ nhất theo giờ của cận dưới CI95** (300 lần lặp), tham số danh nghĩa. Ví dụ 0,9078.
- Bảng 3.7: phân phối của giờ tệ nhất qua 50 bộ tham số, với khoảng [0,8645, 0,8944] và xác suất đạt 6%.

Việc ít lần lặp mỗi bộ tham số cũng làm "nhỏ nhất theo giờ" bị lệch xuống do nhiễu.

**Việc cần làm.**
1. Ghi định nghĩa chính xác của từng chỉ số ở đầu mỗi bảng.
2. Với mỗi bộ tham số bootstrap, tăng số lần lặp (khuyến nghị tối thiểu 60) và tính giờ tệ nhất bằng **giá trị trung bình** theo giờ (không dùng CI), để so sánh công bằng với tham số danh nghĩa.
3. Báo cáo cả hai: tham số danh nghĩa và phân phối qua bootstrap, với cùng định nghĩa.
4. Giải thích sự chênh lệch (nhiễu nhỏ so với ảnh hưởng của sai số tham số) bằng lời.

**Nghiệm thu.** Một định nghĩa duy nhất cho "SL giờ tệ nhất" trong toàn bộ tài liệu, hoặc nếu giữ hai định nghĩa thì đặt tên khác nhau.

---

### T10. Sửa thuật ngữ và các khẳng định không có căn cứ trong dữ liệu

**Vấn đề và cách sửa.**
1. **"Hiện trạng"** cho lịch hằng số 6 quầy: đây là **mốc so sánh do nhóm dựng**, không phải nhân sự thực. Đổi thành "Mốc cơ sở: hằng số 6 quầy (không phải nhân sự thực tế)". "Tiết kiệm 18,52%" phải ghi rõ là so với mốc này. Nếu suy ra được nhân sự thực từ dữ liệu (T4) thì thêm so sánh với nhân sự thực.
2. **Ngày trong tuần ("Thứ 3–Thứ 5", "Thứ 2, Thứ 6, ngày trả lương"):** dữ liệu chỉ có số thứ tự ngày, không có thứ trong tuần hay ngày lương, nên **không có căn cứ**. Xóa các cụm này. Thay bằng **quy tắc theo lưu lượng dự kiến** rút ra từ T2: ví dụ dùng lịch 44 khi lưu lượng dự kiến dưới ngưỡng X khách/ngày, lịch 48 hoặc cao hơn khi trên ngưỡng. Ngưỡng X phải được tính từ kết quả mô phỏng (T2), không đặt tùy ý.
3. **"Phương án tổ chức ca làm việc"** ở Phần 5: sửa theo T5.
4. **Từ ngữ tuyệt đối** ("tuyệt đối", "hoàn hảo", "rất cao", "toàn cục") phải bỏ hoặc thay bằng số liệu cụ thể.

**Nghiệm thu.** Không còn khẳng định về thứ trong tuần hoặc ngày lương. Có bảng quy tắc theo lưu lượng, ghi rõ nguồn.

---

### T11. Làm rõ bộ tham số dùng cho từng thành phần

**Vấn đề.** Hai bộ tham số cùng tồn tại: toàn dữ liệu 14 ngày (Excel `Quyet_dinh`, E[S] = 2,88, θ = 0,1123 trong `bang_tham_so.xlsx`) và tập train 10 ngày (`params.json` v2.0: E[S] = 2,9236, θ = 0,1087, p_vip = 0,3543; dùng cho mô phỏng và SIPP). Phần 4 trộn cả hai (ví dụ nêu "θ = 0,1087, kiên nhẫn 9,2 phút" bên cạnh các bảng dùng bộ khác).

Kết luận **không** thay đổi: với cùng một bộ tham số (cả hai bộ), Erlang C cho 47 quầy-giờ và Erlang-A cho 44, đúng như giải thích trong báo cáo.

**Việc cần làm.**
1. Thêm bảng "Tham số dùng cho từng thành phần" vào báo cáo (cột: thành phần, bộ tham số, nguồn).
2. Tính lại sheet `Quyet_dinh` bằng bộ tham số train (v2.0) để đồng bộ với mô phỏng, giữ bản cũ ở sheet khác nếu cần.
3. Ghi rõ lịch khuyến nghị được **ước lượng chỉ từ 10 ngày train**, rồi kiểm tra trên 4 ngày test (T4).

**Nghiệm thu.** Mỗi bảng trong báo cáo ghi rõ bộ tham số nào. Không còn chỗ trộn hai bộ.

---

### T12. Xử lý tỉ lệ VIP thay đổi theo giờ

**Vấn đề.** Tỉ lệ VIP theo giờ dao động từ 16,9% (8h–9h) đến 49,8% (15h–16h) và tương quan mạnh với tỉ lệ bỏ về theo giờ (r ≈ 0,93), trong khi mô phỏng dùng một p_vip cố định (0,3543). Mức VIP trong dữ liệu (34%) cũng khá cao so với khái niệm "khách VIP".

**Việc cần làm.**
1. Thêm tùy chọn `p_vip` **theo giờ** vào `Model`/`simulate` (mảng độ dài H).
2. Chạy lại đánh giá chính sách ở cấu hình này và so sánh với p_vip cố định. Báo cáo chênh lệch ở SL, SL VIP, bỏ về.
3. Làm rõ định nghĩa "VIP" trong dữ liệu (nhãn gốc là gì, ưu tiên theo cơ chế nào) trong `docs/mo_ta_du_lieu.md`.
4. Nếu chênh lệch nhỏ, ghi nhận như một độ nhạy. Nếu lớn, dùng p_vip theo giờ cho kết quả chính.

**Nghiệm thu.** Có bảng so sánh hai cấu hình và mô tả định nghĩa VIP.

---

## 5. Chi tiết nhiệm vụ P2

### T13. Bổ sung kiểm thử và log pytest

1. Chạy `pytest tests/ -v` và lưu log vào `results/final_v2/pytest_log.txt`. Hiện tài liệu ghi "12/12 passed" nhưng chưa có log đính kèm.
2. Thêm kiểm thử cho:
   - ca làm việc: các trường hợp trong bảng ở T5 (đặc biệt "không có nghiệm" ở mô hình A và nghiệm ở mô hình B);
   - hệ số nhân ngày: trung bình bằng 1 và CV đúng như cấu hình;
   - nhãn Poisson: p < 0,05 không bao giờ ra "Chưa bác bỏ";
   - tính nhất quán: mọi số trong báo cáo khớp CSV (xem T14).
3. Đảm bảo `PYTHONPATH=. pytest tests/` chạy qua trên máy sạch.

### T14. Tự động hóa việc tạo bảng và cập nhật toàn bộ tài liệu

1. Viết `tools/build_tables.py`: đọc CSV trong `results/final_v2/` và sinh các bảng Markdown dùng trong `TONG_HOP_SO_LIEU_CHI_TIET.md`, báo cáo, slide. Tài liệu chỉ **nhúng** bảng do script sinh ra.
2. Viết `tools/check_consistency.py`: quét báo cáo và slide, trích các con số được gắn thẻ (ví dụ `{{so_sanh.Toi_uu.SL}}`) và đối chiếu với CSV, báo lỗi nếu lệch.
3. Cập nhật: `docs/bao_cao_tong_ket.md`, `docs/slide_thuyet_trinh.md`, `TONG_HOP_SO_LIEU_CHI_TIET.md`, `README.md`, `docs/uoc_luong_kiem_dinh.md`.
4. Tạo `CHANGELOG.md` liệt kê mọi thay đổi theo từng nhiệm vụ: số cũ, số mới, lý do.
5. Cập nhật `README.md`: cách chạy lại từ đầu, thời gian chạy, thứ tự bước.

---

## 6. Thứ tự thực hiện đề xuất

1. T1 (nhãn Poisson, quá phân tán) → T11 (làm rõ tham số).
2. T2 (hệ số nhân ngày) → chạy lại đánh giá chính sách → T9, T7, T8.
3. T5 (ca làm việc) → chạy lại các chính sách theo ca.
4. T4 (ngoài mẫu), T6 (đối chiếu mô phỏng), T12 (VIP theo giờ).
5. T10, T3 (sửa kết luận và lời văn, dựa trên kết quả đã có).
6. T13, T14 (kiểm thử, tự động hóa, đóng băng `final_v2`).

Không bắt đầu T3 và T10 trước khi có kết quả của T2, T4, T5, vì các kết luận phụ thuộc vào đó.

---

## 7. Tiêu chí nghiệm thu tổng

- [ ] Không còn nhãn kiểm định Poisson sai (T1).
- [ ] Mô hình có biến động theo ngày, kết luận khuyến nghị nêu xác suất đạt SLA (T2).
- [ ] Không còn con số nào trong tài liệu không truy được về CSV; không còn mâu thuẫn giữa Phần 5 và các bảng (T3, T14).
- [ ] Kiểm tra ngoài mẫu có tài liệu tham số, hai phiên bản, nhận xét theo giờ (T4).
- [ ] MILP ca làm việc khớp bảng đối chiếu; số nhân viên và chi phí nhất quán (T5).
- [ ] Đã giải thích hoặc ghi nhận độ lệch mô phỏng nhỏ (T6).
- [ ] Không còn chữ "toàn cục", "hiện trạng", "Thứ 2/Thứ 6/ngày lương" khi không có căn cứ (T7, T10).
- [ ] `pytest` chạy qua kèm log (T13).
- [ ] `results/final_v2/`, `CHANGELOG.md`, `docs/BAO_CAO_SUA_DOI.md` đã tạo.

---

## 8. Mẫu báo cáo cuối của agent (`docs/BAO_CAO_SUA_DOI.md`)

```
# Báo cáo sửa đổi

## 1. Tóm tắt
- Số nhiệm vụ hoàn thành / tổng:
- Kết luận nào thay đổi so với bản trước (nêu rõ, kèm số trước và sau):

## 2. Chi tiết từng nhiệm vụ
| ID | Trạng thái (xong / một phần / chưa) | File sửa | Số trước → sau | Ghi chú |
|----|-------------------------------------|----------|----------------|---------|

## 3. Kết quả mới quan trọng
- Xác suất đạt SLA toàn ngày và mọi giờ theo từng chính sách (T2):
- Lịch ca làm việc đúng và chi phí (T5):
- Ngoài mẫu (T4):

## 4. Việc chưa làm được và thông tin cần bổ sung

## 5. Rủi ro còn lại
```

---

## 9. Phụ lục: số liệu tham chiếu từ đợt kiểm tra độc lập

Các số dưới đây chỉ để agent **đối chiếu sau khi tự chạy**. Không được sao chép vào kết quả. Nếu kết quả của agent lệch so với các số này trên 1 điểm phần trăm SL hoặc khác dấu, phải điều tra nguyên nhân trước khi chấp nhận.

**Kiểm định theo giờ (từ ma trận khách đến, 14 ngày).**

| Giờ | 8h | 9h | 10h | 11h | 12h | 13h | 14h | 15h | 16h |
|---|---|---|---|---|---|---|---|---|---|
| Chỉ số phân tán D | 23,55 | 23,58 | 48,77 | 39,15 | 20,83 | 30,73 | 38,08 | 33,61 | 26,61 |
| p-value | 0,0356 | 0,0352 | 0,0000 | 0,0002 | 0,0763 | 0,0037 | 0,0003 | 0,0014 | 0,0141 |

Tổng ngày: trung bình 702,6, độ lệch chuẩn 87,1, độ lệch chuẩn Poisson 26,5, tỉ số phương sai/trung bình 10,8, CV 12,4%.

**Chia train/test.** Train (ngày 0–9): 6.867 khách (686,7 mỗi ngày). Test (ngày 10–13): 2.969 khách (742,25 mỗi ngày). λ_test/λ_train − 1 theo giờ: +10,3%, +14,4%, +24,9%, +12,4%, −0,2%, +12,0%, −4,4%, −3,2%, +2,9%.

**Erlang-A tại trạng thái dừng, lịch 44, λ_test (tham số train).** SL theo giờ: 0,914, 0,889, 0,900, 0,892, 0,953, 0,936, 0,947, 0,947, 0,915.

**Mô phỏng độc lập tại λ_test, lịch 44 (200 lần lặp).** SL toàn ngày 0,906, bỏ về 7,65%, Wq 0,697 phút. SL theo giờ: 0,921, 0,886, 0,891, 0,866, 0,935, 0,932, 0,936, 0,939, 0,904.

**Mô phỏng độc lập theo từng ngày quan sát (40 lần lặp mỗi ngày).** SL toàn ngày của lịch 44 theo ngày 0–13: 0,929, 0,889, 0,874, 0,945, 0,963, 0,951, 0,967, 0,863, 0,918, 0,916, 0,909, 0,904, 0,891, 0,893. Ngày kém nhất: ngày 7 (820 khách, 0,863), ngày 2 (826 khách, 0,874), ngày 1 (776 khách, 0,889).

**Mô phỏng độc lập, nhu cầu ×1,1 (150 lần lặp).** Giờ tệ nhất (cận dưới): lịch 44 là 0,857, lịch 48 là 0,893, hằng số 6 là 0,934. Thời gian phục vụ ×1,1: lịch 44 là 0,859, lịch 48 là 0,887.
