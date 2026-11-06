# Hướng dẫn làm Tuần 3 (cho cả 3 thành viên)

> **Chủ đề tuần 3: từ mô phỏng đã được kiểm chứng đến kết luận số quầy, báo cáo và thuyết trình.**
> Tuần này có bốn việc: (1) sửa các tồn đọng của Tuần 2, (2) tối ưu lịch quầy, so sánh chính sách, phân tích độ nhạy, (3) làm các thí nghiệm mở rộng, (4) viết báo cáo, làm slide, tập thuyết trình.
>
> Đọc cùng `README.md`, `TUAN_1_HUONG_DAN.md`, `TUAN_2_HUONG_DAN.md`.

---

## Mục lục

0. [Bước 0: sửa các tồn đọng của Tuần 2](#0-bước-0-sửa-các-tồn-đọng-của-tuần-2)
1. [Mục tiêu và sản phẩm cuối tuần](#1-mục-tiêu-và-sản-phẩm-cuối-tuần)
2. [Điều kiện để bắt đầu Tuần 3](#2-điều-kiện-để-bắt-đầu-tuần-3)
3. [Phân công và lịch từng ngày](#3-phân-công-và-lịch-từng-ngày)
4. [Thành viên A: Độ bất định tham số và kiểm tra ngoài mẫu](#4-thành-viên-a-độ-bất-định-tham-số-và-kiểm-tra-ngoài-mẫu)
5. [Thành viên B: Chi phí, ca làm và lịch bền vững](#5-thành-viên-b-chi-phí-ca-làm-và-lịch-bền-vững)
6. [Thành viên C: Tối ưu lịch, so sánh chính sách và độ nhạy](#6-thành-viên-c-tối-ưu-lịch-so-sánh-chính-sách-và-độ-nhạy)
7. [Thiết kế các thí nghiệm](#7-thiết-kế-các-thí-nghiệm)
8. [Đóng băng số liệu và tính nhất quán](#8-đóng-băng-số-liệu-và-tính-nhất-quán)
9. [Báo cáo](#9-báo-cáo)
10. [Thuyết trình](#10-thuyết-trình)
11. [Kiểm tra chất lượng cuối và khả năng tái lập](#11-kiểm-tra-chất-lượng-cuối-và-khả-năng-tái-lập)
12. [Cổng nộp bài](#12-cổng-nộp-bài)
13. [Nếu bị kẹt](#13-nếu-bị-kẹt)
14. [Phụ lục](#14-phụ-lục)

---

## 0. Bước 0: sửa các tồn đọng của Tuần 2

Bảng kiểm chứng cuối Tuần 2 (`ket_qua_kiem_chung.csv` và bảng trình bày) cho thấy tầng 1 và tầng 2 khớp lý thuyết tốt, nhưng còn **một lỗi số liệu và vài chỗ ghi chú sai**. Phải xử lý xong trước khi làm tiếp, vì số liệu tối ưu của Tuần 3 dựa trên cùng bộ code mô phỏng.

### 0.1 Danh sách tồn đọng

| # | Vấn đề | Mức độ | Cách xử lý |
|---|---|---|---|
| 1 | Dòng **hiệu suất ρ**: lý thuyết 0,75, mô phỏng 0,4228, sai lệch −43,63% nhưng cột `dat = Y` và ghi chú "đạt ρ = 0,75 chuẩn" | **Nặng** | Đây là lỗi tính chỉ số, không phải lỗi mô hình (xem 0.2). Sửa, chạy lại, đặt `dat` theo tiêu chí |
| 2 | Dòng ρ **có trong CSV nhưng không có trong bảng trình bày** | Nặng | Bảng trình bày phải khớp CSV. Không bỏ dòng khó giải thích |
| 3 | Ghi chú dòng Wq tầng 1 ghi "sai lệch dưới 1%" trong khi sai lệch là −3,12% | Trung bình | Sửa ghi chú: đạt vì lý thuyết nằm trong khoảng tin cậy 95% (0,817 ± 0,0423), không phải vì sai lệch dưới 1% |
| 4 | Dòng `cv = 0,5` (+6,55%, lý thuyết 0,5271 nằm **ngoài** khoảng 0,5616 ± 0,0176) ghi là "chính xác ở cv ≤ 1,0" và đánh `Y` | Trung bình | Ghi đúng: Allen–Cunneen đang **đánh giá thấp** ở cv = 0,5 (khoảng 6–7%). Không dùng chữ "chính xác" |
| 5 | Dòng `cv = 1,5`: CSV ghi `N`, bảng trình bày ghi "ĐẠT" | Trung bình | Thống nhất cách phân loại tầng 3 (xem 0.3) |
| 6 | Dòng tỉ lệ bỏ về không có khoảng tin cậy ("-") | Nhẹ | Thêm khoảng tin cậy 95% (tính như các chỉ số khác) |
| 7 | Ghi chú kiểu "tiêu chí bỏ về hợp lý" mơ hồ | Nhẹ | Ghi tiêu chí cụ thể: lý thuyết nằm trong CI hoặc sai lệch < 2% |

### 0.2 Chẩn đoán dòng ρ

Có thể kết luận đây là **lỗi tính chỉ số** vì hai lý do:

1. **Định luật Little.** Nếu `SL` và `Wq` của mô phỏng khớp M/M/6 (0,9688 và 0,817) thì hệ thống đang hoạt động đúng như M/M/6, nên mỗi quầy phải bận khoảng `λ·E[S]/c = 1,5·3/6 = 0,75` thời gian. Không thể vừa có hàng đợi đúng như ρ = 0,75 vừa có quầy bận chỉ 42%.
2. **Bản gốc cho kết quả đúng.** Chạy lại với `c_sim.py` gốc (30 lần lặp, 8.000 phút, warm-up 500) cho `ρ = 0,7506 ± 0,0033`. Vậy lỗi nằm ở chỗ nhóm đã sửa hoặc truyền tham số.

Hiệu suất mô phỏng là `tổng thời gian phục vụ của khách đến sau warm-up / (số quầy × (T − warm-up))`. Kiểm tra theo thứ tự:

- [ ] `rep_stats` có nhận đúng `L` (độ dài chạy, ví dụ 8.000) và `warm` (ví dụ 500) không? Nếu `L` bị đặt nhầm (ví dụ mặc định 60) thì mẫu số sai.
- [ ] Mẫu số có đúng là `c × (T − warm)`? Dùng `c × T` (không trừ warm-up) sẽ cho 0,70 thay vì 0,75.
- [ ] Tử số có cộng đủ `svc` (cột 6) của mọi khách được phục vụ, hay đang bỏ sót (ví dụ chỉ cộng một nhóm khách, hoặc `nan` bị thay bằng 0 sai chỗ)?
- [ ] Tính tay một lần chạy: `np.nansum(a[:, 6]) / (c * (T - warm))`, so với giá trị hàm trả về.
- [ ] Nếu đã sửa `simulate` hoặc đổi cấu trúc mảng kết quả thì cột `svc` có còn là cột 6 không?

Sau khi sửa, thêm **kiểm thử tự động** (mục 14.3): `ρ_mô phỏng ≈ λ(1 − p_ab)·E[S]/c` trong sai số 0,01 cho cấu hình tầng 1 và tầng 2.

### 0.3 Cách phân loại tầng 3 (cần nhất quán trong CSV, bảng, báo cáo, slide)

Tầng 1 và 2 là **kiểm chứng đúng sai** (lý thuyết chính xác). Tầng 3 so với **công thức xấp xỉ**, nên sai lệch không chứng minh mô phỏng sai. Dùng hai cột thay cho một cột `dat`:

| Tầng | Cột phân loại | Giá trị có thể có |
|---|---|---|
| 1, 2 | `dat` | `Y` nếu lý thuyết nằm trong CI95 hoặc sai lệch < 2%; `N` nếu không |
| 3 | `muc_xap_xi` | "Tốt" (< 5% và trong CI), "Chấp nhận được" (5–10%), "Kém, cần giải thích" (> 10%) |

Với tầng 3, **bắt buộc có một kiểm tra độc lập chứng minh mô phỏng đúng với phân phối không mũ** (xem 0.4). Nếu không có kiểm tra này, câu "sai lệch do giới hạn Allen–Cunneen" chỉ là suy đoán.

### 0.4 Hai kiểm tra bổ sung cho tầng 3

**Kiểm tra A: M/G/1 chính xác (công thức Pollaczek–Khinchine).** Với 1 quầy, `Wq = ρ·E[S]·(1 + cs²) / (2(1 − ρ))` là kết quả **chính xác**. Với λ = 0,25, E[S] = 3, cv = 1,5 (lognormal): `ρ = 0,75`, `cs² = 2,25`, nên `Wq = 14,625 phút`. Chạy mô phỏng cùng cấu hình (c = 1). Kết quả tham chiếu từ lần chạy của người hướng dẫn: **14,82 ± 0,99 phút**, khớp lý thuyết. Nếu mô phỏng của nhóm cũng khớp, kết luận chắc chắn: mô phỏng đúng với phục vụ lognormal, và chênh lệch ở c = 6 là do công thức Allen–Cunneen.

**Kiểm tra B: lặp lại c = 6, cv = 1,5 với nhiều lần lặp.** Với 100 lần lặp (8.000 phút, warm-up 500), lần chạy tham chiếu cho `Wq = 1,139 ± 0,044` so với Allen–Cunneen 1,370 (lệch khoảng −17%, lý thuyết nằm **ngoài** khoảng tin cậy). Kết quả của nhóm (−17,3%, 1,1333 ± 0,1239) phù hợp với giá trị này. Nghĩa là sai lệch là **hệ thống và ổn định**, không phải nhiễu. Ghi vào báo cáo: Allen–Cunneen đánh giá cao thời gian chờ khoảng 17% khi cv = 1,5 (phân phối lognormal, c = 6, ρ = 0,75).

Hệ quả cho dự án: **không dùng Allen–Cunneen để quyết định số quầy** khi cv lớn. Dùng mô phỏng làm căn cứ chính (đã nêu ở `TUAN_2_HUONG_DAN.md`).

---

## 1. Mục tiêu và sản phẩm cuối tuần

### 1.1 Mục tiêu

1. **Kết luận số quầy theo từng giờ** đạt SLA, kèm khoảng tin cậy, kèm phương án dự phòng.
2. So sánh các chính sách (hằng số, SIPP, tối ưu bằng mô phỏng, lịch bền vững) bằng cùng một bộ số liệu.
3. Phân tích độ nhạy theo nhu cầu, thời gian phục vụ, tốc độ bỏ về, và theo **độ bất định của tham số ước lượng**.
4. Thí nghiệm mở rộng: hàm chi phí, ràng buộc ca làm.
5. **Báo cáo** (20–25 trang), **slide** (14 slide, khoảng 20 phút), **mã nguồn tái lập được**.
6. Cả nhóm sẵn sàng trả lời phản biện.

### 1.2 Sản phẩm bàn giao cuối Tuần 3

| # | Sản phẩm | Người chịu trách nhiệm chính |
|---|---|---|
| 1 | Bảng kiểm chứng đã sửa (CSV và bảng trình bày thống nhất) | C |
| 2 | Lịch quầy tối ưu, bảng so sánh chính sách | C |
| 3 | Phân tích độ nhạy (bảng, hình) | C |
| 4 | Kiểm tra ngoài mẫu trên tập kiểm tra | A |
| 5 | Phân tích độ bất định tham số | A |
| 6 | Hàm chi phí và lịch theo chi phí | B |
| 7 | Lịch theo ca làm | B |
| 8 | Lịch bền vững (dự phòng nhu cầu) | B và C |
| 9 | Thư mục `results/final_v1/` (số liệu đóng băng) | C (tổng hợp) |
| 10 | Báo cáo hoàn chỉnh (PDF và nguồn) | Cả nhóm |
| 11 | Bộ slide thuyết trình (và slide dự phòng) | Cả nhóm |
| 12 | Mã nguồn sạch, `requirements.txt`, hướng dẫn chạy | Cả nhóm |

---

## 2. Điều kiện để bắt đầu Tuần 3

Cổng kiểm soát cuối Tuần 2 phải đạt (mục 10 của `TUAN_2_HUONG_DAN.md`) **và** các tồn đọng ở mục 0 đã sửa. Tối thiểu:

- [ ] `params.json` đã chốt (có version).
- [ ] Bảng quyết định (Erlang C, Erlang-A, SIPP) hoàn chỉnh.
- [ ] Kiểm chứng tầng 1 và 2 **đạt đầy đủ, kể cả dòng ρ**.
- [ ] Tầng 3 có kiểm tra M/G/1 chính xác và phân loại thống nhất.
- [ ] `pytest` chạy qua.

Nếu chưa đạt, dành **tối đa ngày 1** để sửa. Kết quả tối ưu dựa trên mô phỏng chưa kiểm chứng đầy đủ không đáng tin.

---

## 3. Phân công và lịch từng ngày

Khối lượng khoảng **18–22 giờ/người** (tuần cuối nặng nhất vì có viết báo cáo và thuyết trình).

| Ngày | A | B | C | Chung |
|---|---|---|---|---|
| **1** | Sửa tồn đọng phần dữ liệu, kiểm tra `params.json` lần cuối, chuẩn bị tập kiểm tra | Chốt bảng quyết định, thiết kế hàm chi phí | **Sửa lỗi ρ**, thêm kiểm tra M/G/1, sửa CSV và bảng; **chạy thử tối ưu** (20 lần lặp) | Họp mở đầu 45 phút |
| **2** | Thiết kế phân tích độ bất định tham số | Viết hàm chi phí, bài toán ca làm (MILP) | **Tối ưu lịch**: pha 1 và pha 2, 60 lần lặp | Họp nhanh 15 phút |
| **3** | Chạy độ bất định tham số, kiểm tra ngoài mẫu | Lịch theo chi phí và theo ca, kiểm lại bằng mô phỏng cùng C | **Đánh giá cuối** 300 lần lặp với seed mới, so sánh chính sách | Họp nhanh 15 phút |
| **4** | Hoàn thiện hình phần A, viết báo cáo mục 3, 4 | Hoàn thiện hình phần B, viết báo cáo mục 5, 6 | **Độ nhạy**, lịch bền vững, hình; **tối ngày 4: đóng băng số liệu** | Họp nhanh 15 phút, **đóng băng số liệu** |
| **5** | Báo cáo mục 3, 4 (hoàn chỉnh), slide 3–5 | Báo cáo mục 5, 6, slide 6–9 | Báo cáo mục 7, 8, 9, slide 10–13 | **Tập thuyết trình lần 1** |
| **6** | Kiểm tra chéo số liệu và báo cáo | Kiểm tra chéo số liệu và báo cáo | Kiểm tra chéo số liệu và báo cáo | Ghép báo cáo, tập lần 2 (bấm giờ), kiểm tra tái lập |
| **7** | Sửa theo góp ý | Sửa theo góp ý | Sửa theo góp ý | Tập lần 3 (có người ngoài hỏi), cổng nộp bài, nộp |

**Điểm nối quan trọng:** tối Ngày 4 là hạn **đóng băng số liệu**. Sau mốc này không chạy lại mô phỏng để "thử cho đẹp hơn"; chỉ sửa khi phát hiện lỗi thật và phải thông báo cả nhóm, đổi version.

---

## 4. Thành viên A: Độ bất định tham số và kiểm tra ngoài mẫu

**Mục tiêu:** trả lời hai câu hỏi mà giảng viên chắc chắn hỏi: "Kết quả có chắc không khi tham số chỉ là ước lượng?" và "Mô hình có dự đoán đúng với dữ liệu chưa dùng để ước lượng không?"

### 4.1 Ngày 1: chuẩn bị

- Kiểm tra `params.json` đúng với phiên bản chốt, ghi `version` cuối.
- Chuẩn bị **tập kiểm tra** (các ngày không dùng để ước lượng) dưới dạng bảng thống kê theo giờ: số khách, λ_h, thời gian chờ trung bình, tỉ lệ bỏ về, SL thực tế.
- Rà soát lại các hạn chế của dữ liệu để viết vào báo cáo.

### 4.2 Ngày 2–3: phân tích độ bất định tham số (E4)

Tham số ước lượng chỉ là ước lượng (có khoảng tin cậy). Câu hỏi: lịch quầy tối ưu có còn đạt SLA khi tham số dao động trong khoảng tin cậy không?

**Quy trình:**

1. Chọn lịch cần kiểm tra (lịch tối ưu và lịch bền vững của C).
2. Lấy mẫu **N bộ tham số** (ví dụ N = 50):
   - `λ_h` từ phân phối chuẩn quanh ước lượng với độ lệch chuẩn = CI/1,96 (hoặc bootstrap theo ngày);
   - `E[S]` và hình dạng phân phối: **bootstrap theo khách** từ dữ liệu phục vụ;
   - `θ` từ phân phối chuẩn quanh ước lượng.
3. Với mỗi bộ tham số, chạy mô phỏng (ví dụ 20 lần lặp, seed cố định) và tính `SL` toàn ngày và `SL` giờ tệ nhất.
4. Tổng hợp: phân phối của `SL` qua N bộ tham số. Báo cáo **xác suất lịch đạt SLA** (tỉ lệ bộ tham số mà `SL` ≥ 0,90) và khoảng 5%–95% của `SL`.

**Cách đọc kết quả:**
- Nếu lịch tối ưu chỉ đạt SLA ở khoảng 50–60% số bộ tham số thì lịch "mỏng", cần dự phòng (nối với lịch bền vững của B).
- Nếu đạt trên 90% thì kết luận vững.

Dùng hàm `c_sim.run_reps` làm nền (không viết lại mô phỏng). Nhờ C xác nhận cách truyền `Model` mới cho mỗi bộ tham số.

### 4.3 Ngày 3: kiểm tra ngoài mẫu (với dữ liệu thật)

Theo mục 7.5 của `TUAN_2_HUONG_DAN.md`:

- **Nếu có lịch quầy thực tế theo giờ** suy ra được từ dữ liệu: chạy mô phỏng với tham số từ tập ước lượng và lịch thực tế, so với số liệu quan sát của tập kiểm tra (`Wq`, tỉ lệ bỏ về, `SL` theo giờ). Báo cáo chênh lệch và giải thích.
- **Nếu không suy ra được:** thay bằng kiểm tra đầu vào: so λ_h ước lượng từ tập ước lượng với λ_h quan sát ở tập kiểm tra (có nằm trong khoảng tin cậy không), và so phân phối thời gian phục vụ giữa hai tập (KS hai mẫu). Ghi rõ đây là hạn chế.

Ngoài ra, chạy lịch tối ưu dưới **tham số ước lượng từ tập kiểm tra** (thay cho tập ước lượng). Nếu `SL` vẫn gần mục tiêu, lịch bền vững với sai khác giữa hai tập.

### 4.4 Ngày 3–4: độ nhạy theo phân phối thời gian phục vụ (E5)

So lịch tối ưu khi thời gian phục vụ được mô hình bằng các cách khác nhau:

| Cách mô hình | Mục đích |
|---|---|
| Cấu hình đã chọn ở Tuần 2 | Gốc |
| Lấy mẫu trực tiếp từ dữ liệu (bootstrap) | Loại bỏ sai lệch do chọn phân phối |
| Lognormal với cùng trung bình, `cv` tăng 20% | Độ nhạy theo độ biến thiên |
| Mũ với cùng trung bình | Xem mô hình đơn giản hóa làm sai bao nhiêu |

Với mỗi cách: số quầy từng giờ cần để đạt SLA và `SL` của lịch gốc. Điều này cho thấy "sai phân phối thì sai bao nhiêu quầy", rất có giá trị cho phần hạn chế.

### 4.5 Ngày 4–5: báo cáo và slide

- Viết **báo cáo mục 3 và 4** (dữ liệu, ước lượng, kiểm định, kiểm tra ngoài mẫu, độ bất định tham số).
- Làm **slide 3, 4, 5** (xem mục 10).
- Chuẩn bị hình: λ_h có CI, phân phối phục vụ, phân phối của `SL` qua các bộ tham số (histogram hoặc boxplot).

### 4.6 Tiêu chí hoàn thành của A

- [ ] Phân tích độ bất định tham số chạy xong, có xác suất đạt SLA cho từng lịch.
- [ ] Kiểm tra ngoài mẫu hoàn thành hoặc có giải thích hạn chế rõ ràng.
- [ ] Độ nhạy theo phân phối phục vụ có bảng kết quả.
- [ ] Báo cáo mục 3, 4 và slide 3–5 xong, mọi số liệu lấy từ `results/final_v1/`.

---

## 5. Thành viên B: Chi phí, ca làm và lịch bền vững

**Mục tiêu:** đặt kết quả kỹ thuật vào bối cảnh quyết định thực tế: tiền, ca làm, và độ bền.

### 5.1 Ngày 1–2: hàm chi phí (E1)

Tổng chi phí một ngày: `Chi phí = c_q × (số quầy-giờ) + c_a × (số khách bỏ về) + c_w × (tổng phút chờ của khách)`. Trong đó `c_q` là chi phí một quầy-giờ, `c_a` là chi phí mất một khách, `c_w` là chi phí một phút chờ (có thể bằng 0).

**Quan trọng:** các đơn giá này là **giả định** của nhóm (không có số liệu thật), nên:

- Đặt `c_q = 1` (đơn vị chi phí) rồi biểu diễn `c_a` theo bội số: ví dụ `c_a ∈ {0,1; 0,25; 0,5; 1; 2}` quầy-giờ cho mỗi khách bỏ về.
- Trình bày đây là **phân tích kịch bản** ("nếu mất một khách thiệt hại bằng k lần chi phí một quầy-giờ"), không khẳng định số tiền cụ thể.

**Việc cần làm:**

1. Với mỗi `k`, tìm lịch quầy tối thiểu hóa chi phí (dùng số liệu mô phỏng của C cho từng lịch ứng viên: số khách bỏ về, tổng phút chờ). Có thể thử các lịch gần lịch tối ưu (thêm/bớt 1 quầy ở từng giờ) và chọn lịch tốt nhất.
2. So lịch tối thiểu chi phí với lịch tối ưu theo SLA. Chỉ ra khi nào hai lịch khác nhau và vì sao.
3. Vẽ đường **đánh đổi**: tổng quầy-giờ (trục x) và số khách bỏ về (trục y) cho các lịch khác nhau; đánh dấu các lịch thỏa SLA.

### 5.2 Ngày 2–3: ràng buộc ca làm (E2)

Thực tế nhân viên làm theo ca, không đổi quầy từng giờ. Bài toán: cho yêu cầu quầy tối thiểu từng giờ `c_h` (từ lịch tối ưu), chọn số nhân viên bắt đầu mỗi ca sao cho phủ đủ và tốn ít nhất.

**Mô hình hóa (lập trình nguyên):**

- Biến `x_s` = số nhân viên bắt đầu ca tại giờ `s`, ca có độ dài cố định `D` giờ (ví dụ `D = 4` hoặc `D = 8`, hoặc nhiều loại ca).
- Ràng buộc: với mỗi giờ `h`, `Σ_{s: ca bắt đầu ở s phủ giờ h} x_s ≥ c_h`.
- Mục tiêu: tối thiểu `Σ x_s · D_s` (tổng giờ công) hoặc tổng số nhân viên.
- Giải bằng `scipy.optimize.milp` (hoặc `linprog` với ràng buộc nguyên).

**Sau khi giải:**

- Lịch quầy thực tế theo giờ có thể **lớn hơn** `c_h` ở một số giờ (do phải đủ ca). Đưa lịch này cho C chạy mô phỏng (cùng seed) để xem `SL` và tổng quầy-giờ.
- So sánh: lịch tự do theo giờ (ít quầy-giờ nhất) và lịch theo ca (thực tế hơn nhưng tốn hơn). Nêu "chi phí của việc làm theo ca".
- Thử ít nhất hai kiểu ca (ví dụ ca 4 giờ và ca 8 giờ có nghỉ) để thấy ảnh hưởng.

### 5.3 Ngày 3–4: lịch bền vững (E3), làm cùng C

Lịch tối ưu theo mô phỏng thường "mỏng" (độ nhạy ở các lần chạy thử cho thấy chỉ cần nhu cầu tăng 10% là giờ tệ nhất đã rơi dưới 90%). Cần một phương án có dự phòng:

1. **Định nghĩa:** lịch bền vững là lịch vẫn đạt SLA (theo tiêu chí `feasible`) khi nhu cầu nhân với hệ số `1 + δ` (đề xuất `δ = 10%`).
2. **Cách tìm:** chạy `optimize_schedule` với `rates × (1 + δ)` (C hỗ trợ truyền mô hình đã nhân tỷ lệ).
3. **Chi phí của độ bền:** chênh lệch quầy-giờ giữa lịch bền vững và lịch tối ưu thường. Trình bày bằng bảng: `δ` (0%, 5%, 10%, 20%) và tổng quầy-giờ cần có.
4. **Kiểm tra lý thuyết:** quy tắc căn bậc hai `c ≈ a + β√a` cho biết vì sao dự phòng tăng chậm hơn nhu cầu (kinh tế theo quy mô). Dùng để giải thích, không để quyết định.

### 5.4 Ngày 4: độ nhạy lý thuyết so với mô phỏng

Lấy bảng độ nhạy lý thuyết đã làm ở Tuần 2 (`SL` theo Erlang-A khi nhu cầu tăng) và đặt cạnh kết quả mô phỏng của C. So sánh: lý thuyết dự đoán đúng hướng và độ lớn không? Chênh lệch do đâu (SIPP bỏ qua quán tính, VIP, phục vụ không mũ)?

### 5.5 Ngày 4–5: báo cáo và slide

- Viết **báo cáo mục 5 và 6** (cơ sở lý thuyết, bảng quyết định, kết quả chi phí, ca làm, lịch bền vững).
- Làm **slide 6, 7, 8, 9** (xem mục 10).
- Chuẩn bị bảng "quyết định cuối" (14.1) cùng C.

### 5.6 Tiêu chí hoàn thành của B

- [ ] Hàm chi phí với phân tích kịch bản `k`, có đường đánh đổi.
- [ ] Bài toán ca làm giải xong, lịch theo ca đã được C mô phỏng.
- [ ] Lịch bền vững với bảng chi phí độ bền theo `δ`.
- [ ] So sánh độ nhạy lý thuyết và mô phỏng.
- [ ] Báo cáo mục 5, 6 và slide 6–9 xong.

---

## 6. Thành viên C: Tối ưu lịch, so sánh chính sách và độ nhạy

**Mục tiêu:** tạo ra các kết quả chính của dự án, đáng tin và tái lập được.

### 6.1 Ngày 1: sửa lỗi và chạy thử

1. Sửa lỗi ρ theo mục 0.2, thêm kiểm thử tự động (14.3), chạy lại kiểm chứng ba tầng.
2. Thêm kiểm tra **M/G/1 chính xác** (0.4) vào bảng kiểm chứng.
3. Sửa `ket_qua_kiem_chung.csv` và bảng trình bày để khớp nhau (cột `dat`, `muc_xap_xi`, ghi chú đúng).
4. **Chạy thử** `optimize_schedule` với 20 lần lặp để biết thời gian chạy và bắt lỗi (ví dụ lỗi tiêu chí VIP khi không có VIP).

### 6.2 Ngày 2: tối ưu lịch quầy

Theo mục 11 của `README.md`:

1. Khởi tạo bằng lịch SIPP của B (`sipp_schedule`).
2. **Pha 1:** tăng 1 quầy ở giờ vi phạm tiêu chí (`feasible`: cận dưới CI95 ≥ 0,90), lặp đến khi mọi giờ đạt.
3. **Pha 2:** thử bớt 1 quầy ở từng giờ (bắt đầu từ giờ nhiều quầy nhất), giữ nếu toàn lịch vẫn đạt.
4. Dùng 60 lần lặp, seed cố định (CRN), `c_cap` hợp lý.

**Lưu ý với dữ liệu thật:**

- Nếu không có VIP, sửa `feasible` chỉ xét `sl` (khách thường), bỏ `sl_vip`.
- Nếu tối ưu không hội tụ trong số vòng cho phép, ghi lại và báo B (có thể giờ đỉnh đòi hỏi nhiều quầy hơn `c_cap`).
- Ghi lại **toàn bộ lịch sử tối ưu** (mỗi vòng: lịch, giờ vi phạm). Dùng cho slide.

### 6.3 Ngày 3: đánh giá cuối và so sánh chính sách

Đánh giá mỗi chính sách bằng **seed mới**, không dùng lại seed của bước tối ưu, với **300 lần lặp**.

| Chính sách | Nguồn lịch |
|---|---|
| Hằng số | Số quầy nhỏ nhất, giữ cả ngày, đạt SLA mọi giờ |
| SIPP | Lịch chỉ dựa trên lý thuyết (B) |
| Tối ưu bằng mô phỏng | Từ 6.2 |
| Bền vững (+δ nhu cầu) | Từ 5.3 |
| Theo ca (nếu có) | Từ 5.2 |

Chỉ số báo cáo cho mỗi chính sách (đều có CI95): tổng quầy-giờ, `SL` toàn ngày, `SL` giờ tệ nhất (cận dưới), `SL` VIP (nếu có), tỉ lệ bỏ về, `Wq`, hiệu suất.

Kiểm tra thêm: **đánh giá dưới tham số của tập kiểm tra** (cùng A, mục 4.3).

### 6.4 Ngày 4: độ nhạy bằng mô phỏng

Theo mục 7.2. Dùng 150 lần lặp, cùng seed giữa các chính sách (CRN). Mỗi thí nghiệm ghi lại bảng và hình. Tối ngày 4: **đóng băng số liệu** (mục 8).

### 6.5 Ngày 4–5: báo cáo và slide

- Viết **báo cáo mục 7, 8, 9** (mô phỏng, kiểm chứng, tối ưu và độ nhạy).
- Làm **slide 10–13** (xem mục 10).
- Tạo thư mục `results/final_v1/` và tổng hợp mọi số liệu (mục 8).

### 6.6 Hỗ trợ A và B

C là người nắm mô phỏng, nên cần: (i) hướng dẫn A truyền `Model` mới cho từng bộ tham số, (ii) chạy các lịch theo ca của B, (iii) chạy tối ưu với `rates × (1 + δ)` cho lịch bền vững. Dành khoảng một giờ mỗi ngày cho việc này, và ghi vào lịch của C.

### 6.7 Tiêu chí hoàn thành của C

- [ ] Bảng kiểm chứng đã sửa (ρ đạt, tầng 3 có kiểm tra M/G/1 và phân loại thống nhất).
- [ ] Lịch tối ưu có lịch sử hội tụ, được đánh giá bằng seed mới.
- [ ] Bảng so sánh chính sách (đủ các cột, có CI).
- [ ] Độ nhạy theo nhu cầu, E[S], θ.
- [ ] `results/final_v1/` hoàn chỉnh và có bản mô tả.
- [ ] Báo cáo mục 7, 8, 9 và slide 10–13 xong.

---

## 7. Thiết kế các thí nghiệm

### 7.1 Danh sách thí nghiệm của Tuần 3

| # | Thí nghiệm | Người chạy | Mục đích |
|---|---|---|---|
| T4 | Hàng chung và hàng riêng (nếu chưa làm hết ở Tuần 2) | C | Minh họa hiệu ứng gộp hàng |
| T5 | Tối ưu lịch quầy | C | Kết quả chính |
| T5b | So sánh chính sách | C | Chứng minh lợi ích của tối ưu |
| T6 | Độ nhạy theo nhu cầu, E[S], θ | C | Độ bền |
| E1 | Hàm chi phí | B | Đánh đổi chi phí và dịch vụ |
| E2 | Ràng buộc ca làm | B (mô phỏng: C) | Tính thực tế |
| E3 | Lịch bền vững | B và C | Dự phòng |
| E4 | Độ bất định tham số | A | Độ tin cậy kết quả |
| E5 | Độ nhạy theo phân phối phục vụ | A | Rủi ro mô hình |
| E6 | Kiểm tra ngoài mẫu | A | Xác nhận với dữ liệu thật |

### 7.2 Thiết kế độ nhạy (T6)

| Yếu tố | Mức | Giữ nguyên |
|---|---|---|
| Nhu cầu (nhân λ_h) | 0,9; 1,0; 1,1; 1,2; 1,3 | E[S], θ |
| E[S] (nhân) | 1,0; 1,1; 1,2 | λ_h, θ |
| θ (nhân) | 0,5; 1,0; 1,5 | λ_h, E[S] |

Với mỗi mức và mỗi chính sách: `SL` toàn ngày (CI), `SL` giờ tệ nhất (cận dưới CI), tỉ lệ bỏ về. Dùng **cùng seed** cho mọi chính sách. Vẽ đường "SL giờ tệ nhất theo mức nhu cầu" cho từng chính sách, kèm đường mục tiêu 0,90.

**Cách đọc:** chính sách nào giữ được `SL` giờ tệ nhất ≥ 0,90 đến mức nhu cầu cao nhất thì bền nhất; so với số quầy-giờ để thấy chi phí của độ bền.

### 7.3 Quy tắc chung cho mọi thí nghiệm

- Mô phỏng một ngày làm việc bắt đầu từ lúc mở cửa (hệ trống), nên không cần warm-up; hệ dừng chỉ dùng khi kiểm chứng.
- Số lần lặp: 60 khi tìm kiếm, 150 khi độ nhạy, 300 khi đánh giá cuối. Ghi số lần lặp bên cạnh mọi bảng.
- Seed: dùng khối seed riêng cho từng giai đoạn (tối ưu, đánh giá, độ nhạy, độ bất định) để không dùng lại seed.
- Mọi chỉ số kèm CI95. Khi so hai chính sách, nhớ rằng CRN làm chênh lệch có độ chính xác tốt hơn từng giá trị riêng lẻ.

---

## 8. Đóng băng số liệu và tính nhất quán

**Vấn đề thường gặp:** số trong báo cáo, trong slide và trong file kết quả không khớp nhau vì mỗi người chạy lại ở những thời điểm khác nhau.

**Quy tắc:**

1. Tối Ngày 4, C gộp mọi bảng và hình vào `results/final_v1/`:

```
results/final_v1/
├── MO_TA.md                 # ngày chạy, version params, seed, số lần lặp, phiên bản code
├── params.json              # bản sao tham số dùng để chạy
├── kiem_chung.csv
├── lich_toi_uu.csv          # lịch từng giờ, lịch sử tối ưu
├── so_sanh_chinh_sach.csv
├── do_nhay.csv
├── chi_phi.csv              # B
├── lich_theo_ca.csv         # B
├── bat_dinh_tham_so.csv     # A
├── ngoai_mau.csv            # A
└── hinh/                    # mọi hình dùng trong báo cáo và slide
```

2. **Mọi số trong báo cáo và slide phải lấy từ thư mục này** (sao chép trực tiếp, không gõ lại bằng tay từ bộ nhớ).
3. Sau khi đóng băng, nếu phát hiện lỗi phải sửa: ghi vào `MO_TA.md` (version `final_v2`), thông báo cả nhóm, và cập nhật mọi nơi dùng số cũ.
4. Ngày 6 kiểm tra chéo: mỗi người chọn ngẫu nhiên 10 con số trong báo cáo của người khác và đối chiếu với file kết quả.

---

## 9. Báo cáo

### 9.1 Cấu trúc và phân công (20–25 trang)

| Mục | Nội dung | Người viết | Số trang |
|---|---|---|---|
| 1 | Giới thiệu, bài toán, mục tiêu, SLA | Cả nhóm (A viết bản đầu) | 1–2 |
| 2 | Mô tả hệ thống, giả định, phạm vi | C | 1–2 |
| 3 | Dữ liệu: nguồn, làm sạch, thống kê mô tả | A | 2–3 |
| 4 | Ước lượng, kiểm định, độ bất định, kiểm tra ngoài mẫu | A | 2–3 |
| 5 | Cơ sở lý thuyết: M/M/c, M/G/c, Erlang-A, SIPP | B | 3–4 |
| 6 | Bảng quyết định, chi phí, ca làm, lịch bền vững | B | 2–3 |
| 7 | Mô hình mô phỏng SimPy | C | 2 |
| 8 | Kiểm chứng ba tầng và M/G/1 chính xác | C | 2–3 |
| 9 | Tối ưu lịch, so sánh chính sách, độ nhạy | C | 3–4 |
| 10 | Kết luận, khuyến nghị, hạn chế, hướng phát triển | Cả nhóm (B viết bản đầu) | 1–2 |
| | Tài liệu tham khảo, phụ lục | Cả nhóm | |

### 9.2 Quy tắc viết

- Mỗi số liệu có **đơn vị** và, nếu là kết quả mô phỏng, **khoảng tin cậy** và số lần lặp.
- Mỗi hình và bảng có tiêu đề, đơn vị trục, và **được nhắc tới trong văn bản** với một câu kết luận.
- Phần phương pháp đủ để người khác tái lập: tham số, seed, số lần lặp, phiên bản.
- Không đặt kết quả của dữ liệu giả lập lên cùng một bảng với dữ liệu thật mà không ghi chú.
- Nêu **hạn chế một cách thẳng thắn**: nguồn dữ liệu cũ và là tổng đài, giả định Poisson theo giờ, một hàng chung, quầy giống nhau, phân phối bỏ về mũ, đơn giá chi phí là giả định.
- Trích dẫn nguồn dữ liệu và email thông báo như yêu cầu của nơi cung cấp dữ liệu.

### 9.3 Phần kết luận phải trả lời được

1. Số quầy tối thiểu theo từng giờ để đạt SLA là bao nhiêu (kèm khoảng tin cậy)?
2. Lịch tối ưu tiết kiệm bao nhiêu so với lịch hằng số?
3. Lịch có bền khi nhu cầu hoặc tham số thay đổi không? Chi phí để bền là bao nhiêu?
4. Lịch theo ca thực tế tốn thêm bao nhiêu so với lịch tự do?
5. Điều gì làm kết quả có thể không áp dụng được ngoài bối cảnh này?

### 9.4 Kiểm tra trước khi nộp báo cáo

- [ ] Mọi số khớp `results/final_v1/`.
- [ ] Không còn "[..]", "TODO", ghi chú nháp.
- [ ] Hình đọc được khi in (cỡ chữ, màu có phân biệt khi in đen trắng).
- [ ] Công thức đúng ký hiệu, nhất quán xuyên suốt.
- [ ] Mục lục, đánh số trang, tài liệu tham khảo đầy đủ.
- [ ] Người ngoài nhóm đọc thử một mục và hiểu được.

---

## 10. Thuyết trình

### 10.1 Cấu trúc 14 slide (khoảng 20 phút)

| Slide | Nội dung | Người trình bày | Thời gian |
|---|---|---|---|
| 1 | Tên đề tài, nhóm, bối cảnh | Cả nhóm (A nói) | 0:30 |
| 2 | Bài toán, SLA, những phức tạp của thực tế | A | 1:30 |
| 3 | Dữ liệu và tốc độ đến theo giờ | A | 1:30 |
| 4 | Thời gian phục vụ và bỏ về: kiểm định, mô hình chọn | A | 1:30 |
| 5 | Độ bất định tham số và kiểm tra ngoài mẫu | A | 1:30 |
| 6 | M/M/c, M/G/c, Erlang-A (ý tưởng chính, không chép công thức dài) | B | 1:30 |
| 7 | Ví dụ tính tay và bảng quyết định | B | 1:30 |
| 8 | Chi phí và đánh đổi | B | 1:30 |
| 9 | Lịch theo ca và lịch bền vững | B | 1:30 |
| 10 | Kiến trúc mô phỏng SimPy | C | 1:30 |
| 11 | Kiểm chứng ba tầng (bao gồm M/G/1 chính xác và giới hạn Allen–Cunneen) | C | 2:00 |
| 12 | Tối ưu lịch quầy và so sánh chính sách (kết quả chính) | C | 2:00 |
| 13 | Độ nhạy và khuyến nghị | C | 1:30 |
| 14 | Kết luận, hạn chế, hướng phát triển | Cả nhóm | 1:00 |
| | Q&A | Cả nhóm | 5:00 |

**Slide dự phòng (phụ lục, để trả lời phản biện):** công thức Erlang C và Erlang-A, bảng kiểm chứng đầy đủ, `params.json`, lịch sử tối ưu, đường Welch, phân phối kết quả độ bất định.

### 10.2 Quy tắc thiết kế slide

- Mỗi slide **một thông điệp**, nêu ở tiêu đề (ví dụ "Lịch tối ưu dùng ít hơn 25% quầy-giờ nhưng chỉ chịu được nhu cầu tăng 5%", thay vì "Kết quả tối ưu").
- Dưới 40 từ chữ trên một slide; ưu tiên hình lớn có chú thích.
- Số liệu luôn đi kèm khoảng tin cậy hoặc nêu rõ là ước lượng.
- Không đưa bảng nhiều hơn 6 dòng; phần còn lại để phụ lục.
- Nhất quán màu sắc: mỗi chính sách một màu xuyên suốt mọi hình.

### 10.3 Kịch bản chuyển tiếp

Chuẩn bị câu chuyển giữa các phần để không bị rời rạc, ví dụ A sang B: "Với các tham số này, lý thuyết cho biết cần bao nhiêu quầy?". B sang C: "Lý thuyết dựa trên giả định đơn giản; ta dùng mô phỏng để kiểm tra và đi xa hơn". Ghi các câu này vào ghi chú slide.

### 10.4 Tập thuyết trình

| Lần | Ngày | Mục tiêu | Cách làm |
|---|---|---|---|
| 1 | 5 | Nội dung đúng, đủ ý | Nói thử từng phần, góp ý nội dung |
| 2 | 6 | Thời gian và chuyển tiếp | Bấm giờ toàn bài; mỗi phần sai số ≤ 30 giây; sửa chỗ rườm |
| 3 | 7 | Giống buổi thật | Có 1–2 người ngoài nhóm nghe và đặt câu hỏi phản biện; tập trả lời |

Quy tắc: mỗi người phải hiểu **toàn bộ** bài, không chỉ phần của mình, vì giảng viên có thể hỏi bất kỳ ai về bất kỳ phần nào.

### 10.5 Chuẩn bị trả lời phản biện

Mỗi người chuẩn bị câu trả lời 30–60 giây cho các câu ở 14.4. Phân người trả lời chính theo chuyên môn nhưng ai cũng phải biết ý chính. Quy tắc trả lời: trả lời thẳng câu hỏi, nêu bằng chứng (số liệu, hình), thừa nhận hạn chế nếu có, không bịa.

### 10.6 Demo (tùy chọn)

Nếu có demo chạy code, **chuẩn bị bản dự phòng** (video hoặc ảnh chụp kết quả) phòng khi máy lỗi. Demo ngắn (≤ 2 phút): chạy `python main.py` rút gọn (ít lần lặp) hoặc chạy một ngày mô phỏng và hiển thị hình.

---

## 11. Kiểm tra chất lượng cuối và khả năng tái lập

### 11.1 Tái lập

- [ ] Tạo môi trường sạch (máy khác hoặc môi trường ảo mới), `pip install -r requirements.txt`, chạy `python main.py` từ đầu đến cuối **không lỗi**.
- [ ] Kết quả chạy lại khớp `results/final_v1/` đến chữ số thập phân thứ 3 (cùng seed).
- [ ] `pytest` chạy qua.
- [ ] Ít nhất **hai thành viên** đã tự chạy thành công trên máy của mình.
- [ ] `README.md` hướng dẫn chạy đúng với thực tế (tên file, lệnh, thời gian chạy).

### 11.2 Mã nguồn

- [ ] Không còn code chết, `print` gỡ lỗi, đường dẫn tuyệt đối theo máy cá nhân.
- [ ] Mỗi hàm chính có docstring ngắn nêu đầu vào, đầu ra, đơn vị.
- [ ] Hằng số (SLA, seed, số lần lặp) nằm ở một chỗ, không rải rác.
- [ ] `requirements.txt` có phiên bản các thư viện (simpy, numpy, scipy, pandas, matplotlib, pytest).
- [ ] Không có dữ liệu cá nhân trong repository. Dữ liệu gốc của bên thứ ba: ghi nguồn, tuân thủ điều khoản dùng.

### 11.3 Cấu trúc nộp

```
queue_project/
├── README.md, TUAN_1..3_HUONG_DAN.md
├── requirements.txt
├── common.py, a_data.py, b_theory.py, c_sim.py, main.py
├── tests/
├── data/ (raw: không nộp nếu dung lượng lớn, ghi cách tải; clean)
├── excel/
├── docs/
├── results/final_v1/
├── bao_cao.pdf
└── slide.pdf (và .pptx)
```

---

## 12. Cổng nộp bài

Chỉ nộp khi **tất cả** các mục sau được đánh dấu.

**Kết quả**
- [ ] Bảng kiểm chứng đã sửa, nhất quán giữa CSV, báo cáo và slide.
- [ ] Lịch tối ưu và so sánh chính sách có CI, đánh giá bằng seed mới.
- [ ] Độ nhạy và độ bất định tham số đã chạy.
- [ ] Khuyến nghị cuối (14.1) viết rõ ràng, có con số.

**Tài liệu**
- [ ] Báo cáo hoàn chỉnh, mọi số khớp `results/final_v1/`.
- [ ] Slide 14 + phụ lục, đã tập ít nhất 3 lần, đúng thời gian.
- [ ] Hạn chế được nêu thẳng thắn.

**Kỹ thuật**
- [ ] Chạy lại từ đầu thành công trên máy sạch, `pytest` qua.
- [ ] Nguồn dữ liệu được ghi và email thông báo đã gửi.

**Nhóm**
- [ ] Mỗi người trả lời được câu hỏi về mọi phần.
- [ ] Đã tập Q&A với người ngoài nhóm.

---

## 13. Nếu bị kẹt

| Tình huống | Cách xử lý |
|---|---|
| Lịch tối ưu không hội tụ | Kiểm tra `c_cap`, tiêu chí `feasible` (VIP có tồn tại không), số lần lặp quá ít gây nhiễu; thử tăng lần lặp ở vòng cuối |
| Kết quả tối ưu thay đổi mỗi lần chạy | Kiểm tra seed cố định và CRN; nếu hai lịch gần như tương đương về chi phí và SLA, chọn lịch ít quầy hơn và nêu rõ |
| Mô phỏng quá chậm để chạy đủ số lần lặp | Giảm lần lặp khi tìm, tăng khi đánh giá cuối; chạy song song bằng `multiprocessing`; chỉ tối ưu ở giờ có vi phạm |
| Số liệu trong báo cáo không khớp nhau | Quay lại `results/final_v1/`; nếu phải chạy lại, đổi version và cập nhật mọi nơi |
| Phân tích ca làm (MILP) không giải được | Dùng heuristic: duyệt các tổ hợp ca nhỏ; hoặc ràng buộc đơn giản hơn (ca 8 giờ cố định) |
| Hàm chi phí gây tranh cãi vì đơn giá | Chỉ trình bày kịch bản theo bội số `k`, không đưa số tiền cụ thể |
| Hết thời gian | Ưu tiên: kiểm chứng đúng, tối ưu và so sánh chính sách, độ nhạy, báo cáo, slide. Bỏ: E2 (ca làm), E5 (phân phối phục vụ), demo |
| Một thành viên vắng | Hai người còn lại nắm sản phẩm của người vắng qua tài liệu; đây là lý do mọi thứ phải có `docs/` rõ ràng |
| Giảng viên không đồng ý một giả định | Ghi nhận, chạy thêm độ nhạy theo giả định đó nếu kịp, hoặc nêu như hạn chế |

---

## 14. Phụ lục

### 14.1 Mẫu bảng "quyết định cuối"

| Mục | Giá trị |
|---|---|
| Khung giờ làm việc | |
| Lịch quầy tối ưu (từng giờ) | |
| Tổng quầy-giờ | |
| `SL` toàn ngày (CI95) | |
| `SL` giờ tệ nhất (cận dưới CI95) | |
| Tỉ lệ bỏ về | |
| So với lịch hằng số | tiết kiệm .. % quầy-giờ |
| Lịch bền vững (dự phòng +10% nhu cầu) | thêm .. quầy-giờ |
| Xác suất đạt SLA khi tham số dao động (E4) | |
| Lịch theo ca khả thi | tốn thêm .. % |
| Điều kiện áp dụng và hạn chế | |

### 14.2 Mẫu bảng so sánh chính sách

| Chính sách | Quầy-giờ | `SL` toàn ngày | `SL` giờ tệ nhất | Bỏ về | Wq (phút) | Hiệu suất |
|---|---|---|---|---|---|---|
| Hằng số | | | | | | |
| SIPP | | | | | | |
| Tối ưu mô phỏng | | | | | | |
| Bền vững | | | | | | |
| Theo ca | | | | | | |

Mỗi ô kèm CI95 và ghi số lần lặp ở chú thích.

### 14.3 Kiểm thử tự động bổ sung cho mô phỏng (gợi ý)

```python
import numpy as np
import pytest
from common import Model, exp_service
import c_sim as cs

def test_utilization_matches_little():
    lam, ms, c = 1.5, 3.0, 6
    m = Model(np.array([lam]), exp_service(ms), hour_len=8000)
    S, O = cs.run_reps(m, [c], 10, 100, warm=500)
    assert np.mean(O["util"]) == pytest.approx(lam * ms / c, abs=0.02)

def test_same_seed_same_result():
    lam = 1.5
    m = Model(np.array([lam]), exp_service(3.0), hour_len=2000)
    a = cs.simulate(m, [6], 7); b = cs.simulate(m, [6], 7)
    assert np.array_equal(a, b, equal_nan=True)

def test_more_servers_not_worse():
    lam = 1.5
    m = Model(np.array([lam]), exp_service(3.0), hour_len=4000)
    sl5 = np.mean(cs.run_reps(m, [5], 10, 1)[1]["sl"])
    sl7 = np.mean(cs.run_reps(m, [7], 10, 1)[1]["sl"])
    assert sl7 > sl5
```

Chạy: `PYTHONPATH=. pytest tests/`. Bài kiểm tra đầu tiên chính là bài kiểm tra bắt được lỗi ρ ở Tuần 2.

### 14.4 Bộ câu hỏi phản biện cần chuẩn bị

**Về dữ liệu và ước lượng**
1. Dữ liệu của bạn từ đâu, có đại diện cho quầy ngân hàng không?
2. Vì sao dùng khung giờ thay vì một tốc độ đến chung?
3. Vì sao phân phối thời gian phục vụ bạn chọn lại hợp lý? Nếu chọn sai thì sao?
4. Tham số chỉ là ước lượng, làm sao biết kết quả đáng tin?

**Về lý thuyết**
5. Erlang C và Erlang-A khác nhau thế nào, vì sao Erlang C đòi hỏi nhiều quầy hơn?
6. Vì sao Allen–Cunneen lệch nhiều khi cv lớn? Mô phỏng của bạn có sai không?
7. Vì sao hàng chung tốt hơn nhiều hàng riêng?

**Về mô phỏng**
8. Làm sao bạn biết mô phỏng đúng? (ba tầng kiểm chứng, M/G/1 chính xác)
9. Vì sao cần nhiều lần lặp và CRN?
10. Vì sao không cần warm-up khi mô phỏng một ngày, nhưng cần khi kiểm chứng hệ dừng?

**Về kết luận**
11. Vì sao tính khách bỏ về là không đạt SLA?
12. Lịch tối ưu có bền không? Chi phí để bền là bao nhiêu?
13. Đơn giá chi phí lấy ở đâu?
14. Hạn chế lớn nhất của nghiên cứu là gì? Nếu có thêm thời gian bạn làm gì?
15. Nhóm đã phát hiện và sửa lỗi nào trong quá trình làm? (Lỗi ρ ở Tuần 2 là ví dụ tốt: cho thấy nhóm kiểm tra kỹ và trung thực.)

### 14.5 Mẫu báo cáo tuần 3 (1 trang, `docs/bao_cao_tuan_3.md`)

```
# Báo cáo Tuần 3
1. Tồn đọng Tuần 2 đã xử lý: [..]
2. Kết quả chính: lịch tối ưu [..]; tiết kiệm [..]%; SL [..] (CI [..])
3. Độ nhạy và độ bền: [..]
4. Mở rộng đã làm: chi phí [..]; ca làm [..]; bất định tham số [..]; ngoài mẫu [..]
5. Vấn đề và cách xử lý: [..]
6. Cổng nộp bài: đạt / chưa đạt (mục nào)
7. Việc còn lại trước khi nộp: [..]
```

### 14.6 Kiểm tra cuối (tự đánh giá theo tiêu chí chấm điểm thường gặp)

| Tiêu chí | Câu hỏi tự kiểm tra |
|---|---|
| Hiểu biết lý thuyết | Có suy ra và giải thích được công thức, điều kiện áp dụng? |
| Dữ liệu thực tế | Có nguồn thật, làm sạch, kiểm định, nêu hạn chế? |
| Mô phỏng | Được kiểm chứng độc lập? Có CI, seed, số lần lặp? |
| Kết quả | Có kết luận số quầy cụ thể, có dự phòng, có so sánh chính sách? |
| Trung thực khoa học | Nêu sai lệch, giới hạn, lỗi đã sửa thẳng thắn? |
| Trình bày | Thông điệp rõ, đúng giờ, ai cũng trả lời được? |
| Tái lập | Người khác chạy lại và ra cùng kết quả? |
