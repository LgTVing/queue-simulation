# Hướng dẫn làm Tuần 2 (cho cả 3 thành viên)

> **Chủ đề tuần 2: từ dữ liệu đến bảng quyết định, rồi mới viết code mô phỏng và kiểm chứng.**
> Thứ tự bắt buộc trong tuần: (1) A chốt tham số từ dữ liệu thật, (2) B hoàn thành bảng quyết định bằng tham số đó, (3) C viết/chỉnh code mô phỏng và kiểm chứng với bảng của B.
>
> Đọc cùng `README.md` (kế hoạch tổng thể) và `TUAN_1_HUONG_DAN.md` (tuần trước).

---

## Mục lục

1. [Mục tiêu và sản phẩm cuối tuần](#1-mục-tiêu-và-sản-phẩm-cuối-tuần)
2. [Điều kiện để bắt đầu Tuần 2](#2-điều-kiện-để-bắt-đầu-tuần-2)
3. [Phân công và lịch từng ngày](#3-phân-công-và-lịch-từng-ngày)
4. [Thành viên A: Tham số từ dữ liệu thật và nối code](#4-thành-viên-a-tham-số-từ-dữ-liệu-thật-và-nối-code)
5. [Thành viên B: Bảng quyết định và kiểm thử lý thuyết](#5-thành-viên-b-bảng-quyết-định-và-kiểm-thử-lý-thuyết)
6. [Thành viên C: Mô phỏng SimPy và kiểm chứng](#6-thành-viên-c-mô-phỏng-simpy-và-kiểm-chứng)
7. [Quy trình kiểm chứng chi tiết](#7-quy-trình-kiểm-chứng-chi-tiết)
8. [Ghép nối: luồng dữ liệu giữa các module](#8-ghép-nối-luồng-dữ-liệu-giữa-các-module)
9. [Việc chung và kiểm tra chéo](#9-việc-chung-và-kiểm-tra-chéo)
10. [Cổng kiểm soát cuối Tuần 2](#10-cổng-kiểm-soát-cuối-tuần-2)
11. [Nếu bị kẹt](#11-nếu-bị-kẹt)
12. [Phụ lục](#12-phụ-lục)

---

## 1. Mục tiêu và sản phẩm cuối tuần

### 1.1 Mục tiêu

1. **Tham số hóa từ dữ liệu thật:** λ theo giờ, phân phối và tham số thời gian phục vụ, tốc độ bỏ về, tỉ lệ VIP/loại giao dịch (nếu có), kèm khoảng tin cậy.
2. **Bảng quyết định hoàn chỉnh** (Excel và Python đối chiếu nhau): số quầy từng giờ theo Erlang C, Erlang-A, SIPP.
3. **Mô phỏng SimPy chạy đúng với dữ liệu thật** và **qua kiểm chứng ba tầng** so với lý thuyết.
4. Có bước đầu về Welch (chọn warm-up) và hiệu ứng hàng chung so với hàng riêng.
5. Mã nguồn có **kiểm thử tự động** cho phần lý thuyết và có thể chạy lại bằng một lệnh.

### 1.2 Sản phẩm bàn giao cuối Tuần 2

| # | Sản phẩm | Người chịu trách nhiệm | File gợi ý |
|---|---|---|---|
| 1 | Hàm đọc dữ liệu thật và dữ liệu đã nạp | A | `a_data.py` (hàm `load_log`) |
| 2 | Bảng tham số cuối cùng (xuất ra file) | A | `docs/params.json`, `docs/bang_tham_so.xlsx` |
| 3 | Báo cáo ước lượng và kiểm định phân phối | A | `docs/uoc_luong_kiem_dinh.md`, `fig_a_fit.png` |
| 4 | Bảng quyết định hoàn chỉnh | B | `excel/erlang.xlsx` (sheet `Quyet_dinh`), `docs/bang_quyet_dinh.md` |
| 5 | Bộ kiểm thử lý thuyết | B | `tests/test_theory.py` |
| 6 | Mô phỏng chạy trên dữ liệu thật, bảng kiểm chứng ba tầng | C | `c_sim.py`, `ket_qua_kiem_chung.csv` |
| 7 | Hình Welch và hình hàng chung/hàng riêng | C | `fig_c_welch.png`, `fig_c_pooling.png` |
| 8 | Báo cáo kiểm chứng | C | `docs/bao_cao_kiem_chung.md` |
| 9 | Báo cáo tuần 2 (1 trang) | Cả nhóm | `docs/bao_cao_tuan_2.md` |

---

## 2. Điều kiện để bắt đầu Tuần 2

Chỉ vào Tuần 2 khi **cổng kiểm soát cuối Tuần 1 đã đạt** (mục 9 của `TUAN_1_HUONG_DAN.md`). Tối thiểu cần có:

- [ ] Dữ liệu sạch đúng định dạng 8 cột (`day, t, hour, cls, vip, wait, served, svc`).
- [ ] Bảng tham số sơ bộ của A đã bàn giao.
- [ ] Excel Erlang C của B khớp ví dụ tính tay (c = 5 không đạt, c = 6 đạt).
- [ ] Đặc tả mô hình của C đã được A và B đọc.

Nếu một mục chưa xong, **việc đầu tiên của Tuần 2 là hoàn thành nó**, rồi mới làm tiếp. Không viết code mô phỏng trên tham số chưa chắc chắn.

---

## 3. Phân công và lịch từng ngày

Khối lượng khoảng **15–18 giờ/người** (tuần này nặng hơn tuần 1 vì có code).

| Ngày | A | B | C | Chung |
|---|---|---|---|---|
| **1** | Viết `load_log`, nạp dữ liệu thật, chạy thử các hàm hiện có | Điền bảng quyết định bằng tham số sơ bộ (Excel) | Đọc lại đặc tả, kiểm tra từng hàm trong `c_sim.py` theo đặc tả | Họp mở đầu 30 phút |
| **2** | Ước lượng phân phối thời gian phục vụ (quyết định mô hình dịch vụ), `fit_patience` | Viết `tests/test_theory.py`, kiểm tra Python so với Excel | Chuẩn bị cấu hình kiểm chứng tầng 1, chạy thử | Họp nhanh 15 phút |
| **3** | Tách train/test theo ngày, **chốt `params.json`** | Hoàn thành bảng quyết định bằng `params.json` (Erlang C, Erlang-A, SIPP) | **Nhận `params.json`**, chạy tầng 1 và 2 | Họp nhanh 15 phút |
| **4** | Vẽ hình, viết báo cáo ước lượng | Phân tích độ nhạy lý thuyết (λ, E[S], θ) | Chạy tầng 3, Welch, hàng chung và hàng riêng | Họp nhanh 15 phút |
| **5** | Hỗ trợ C đối chiếu tham số, kiểm tra mô hình dịch vụ trong code | Đối chiếu bảng quyết định với mô phỏng cùng C | Bảng kiểm chứng, báo cáo kiểm chứng | Họp nhanh 15 phút |
| **6** | Kiểm tra chéo công việc của B | Kiểm tra chéo công việc của C | Kiểm tra chéo công việc của A | Họp kiểm tra chéo 60 phút |
| **7** | Sửa theo góp ý | Sửa theo góp ý | Sửa theo góp ý | Họp tổng kết 60 phút, báo cáo tuần 2, cổng kiểm soát |

**Điểm nối quan trọng:** Ngày 3 là điểm nối của cả tuần. A phải chốt `params.json` trước khi B hoàn thành bảng và C chạy kiểm chứng trên tham số thật. Nếu A trễ, B và C dùng tham số sơ bộ từ tuần 1 để không bị chặn, rồi chạy lại khi có bản chốt.

---

## 4. Thành viên A: Tham số từ dữ liệu thật và nối code

**Mục tiêu:** từ dữ liệu sạch, sinh ra `params.json` chính thức mà B và C dùng, và làm cho `a_data.py` chạy được trên dữ liệu thật.

### 4.1 Ngày 1: viết `load_log` và nạp dữ liệu

Trong `a_data.py` thêm hàm `load_log(path)` trả về DataFrame có đúng 8 cột như ở `TUAN_1_HUONG_DAN.md`, mục 4.2. Hàm chỉ đọc file `data/clean/` đã làm sạch từ tuần 1.

Các điểm cần kiểm tra khi nạp:

- `hour` nằm trong `0 … H−1` với `H = len(H_LABELS)` trong `common.py`. Sửa `HOURS`, `H_LABELS` trong `common.py` cho khớp khung giờ thật (ví dụ 8h–17h là 9 khung).
- Cột `cls` có thể trống (không biết loại giao dịch) và `vip` có thể bằng 0 hết. Các hàm hiện có phải xử lý được hai trường hợp này (xem 4.3).
- Đơn vị phút ở mọi cột thời gian.
- `day` bắt đầu từ 0 và liên tục.

Chạy thử `fit_arrivals(df)`, `fit_patience(df)` trên dữ liệu thật. Ghi lại lỗi gặp phải và cách sửa vào `docs/nhat_ky.md`.

**Nếu muốn dùng khung 30 phút:** đặt `Model.hour_len = 30` và `H` gấp đôi. Chỉ làm vậy khi có đủ dữ liệu (cần khoảng 100 lượt đến cho mỗi ô mới đạt sai số ±20%).

### 4.2 Ngày 2: quyết định mô hình thời gian phục vụ

Hàm `fit_service` hiện đang giả định hai loại giao dịch (`cls = 0/1`) và lognormal. Với dữ liệu thật phải quyết định theo kết quả kiểm định, không áp đặt. Quy trình:

1. Fit exponential, lognormal, gamma, Weibull trên dữ liệu gộp. So AIC, KS, Q-Q plot.
2. Nếu dữ liệu có phân loại dịch vụ rõ ràng (hoặc histogram có hai đỉnh) thì tách theo loại và fit riêng.
3. Chọn **một** trong ba cấu hình và ghi lý do:

| Cấu hình | Khi nào dùng | Sampler trong `common.py` |
|---|---|---|
| Một phân phối đơn (lognormal/gamma/Weibull) | Dữ liệu gộp khớp tốt một phân phối | Dùng `lognorm_service(mean, cv)`; với gamma/Weibull thêm hàm sampler mới (xem mã gợi ý ở 12.4) |
| Hỗn hợp hai loại | Có phân loại giao dịch, tách ra thì khớp | `mix_service(p_quick, q, c)` (đã có) |
| **Lấy mẫu trực tiếp từ dữ liệu** (bootstrap) | Không phân phối nào khớp, hoặc cần phương án an toàn | Hàm `empirical_service(samples)` (xem 12.4) |

Phương án lấy mẫu trực tiếp luôn dùng được và tránh sai lệch do chọn sai phân phối, nhưng không ngoại suy được đuôi phân phối; ghi chú điều này vào báo cáo.

### 4.3 Ngày 2–3: làm cho code chịu được dữ liệu thật

Những chỗ cần xử lý trong `a_data.py`:

- Nếu `cls` toàn trống: bỏ phần tách hai loại trong `fit_service` và `estimate_all`; `est` chỉ cần chứa tham số của cấu hình đã chọn ở 4.2.
- Nếu `vip` toàn 0: `p_vip = 0`. Ghi rõ trong báo cáo và nhắc C bỏ tiêu chí VIP khi tối ưu (hàm `feasible`).
- Nếu không có khách bỏ về: `θ = 0`. Hàm `fit_patience` chia cho 0; cần xử lý riêng.
- `estimate_all` hiện trả về `est` gồm `rates, p_quick, q, c, theta, p_vip`. Thay đổi cấu trúc này thì phải báo B và C (xem mục 8).

### 4.4 Ngày 3: tách train/test theo ngày và chốt tham số

1. Chia các ngày thành tập **ước lượng** (khoảng 70%) và tập **kiểm tra** (khoảng 30%). Chia theo **ngày**, không theo khách, để giữ cấu trúc ngày.
2. Ước lượng mọi tham số chỉ trên tập ước lượng. Xuất ra `docs/params.json` (xem định dạng ở 8.2).
3. Tính trên tập kiểm tra các số quan sát được để C đối chiếu: số khách theo giờ, thời gian chờ trung bình, tỉ lệ bỏ về, SL thực tế.
4. Cập nhật `docs/bang_tham_so.xlsx` cho khớp `params.json`, ghi ngày chốt và phiên bản (v1, v2). **Mọi thay đổi sau ngày 3 phải báo B và C ngay.**

### 4.5 Ngày 4: hình và báo cáo ước lượng

- Chạy lại `estimate_all(df, plot=True)` trên dữ liệu thật. Hình `fig_a_fit.png` gồm tốc độ đến theo giờ, phân phối phục vụ, Q-Q plot.
- Viết `docs/uoc_luong_kiem_dinh.md`: dữ liệu dùng, cách chia train/test, kết quả kiểm định Poisson, so sánh các phân phối, lý do chọn mô hình dịch vụ, ước lượng θ kèm khoảng tin cậy, hạn chế.
- Với kiểm định KS khi tham số ước lượng từ mẫu: ghi rõ p-value hơi lạc quan.

### 4.6 Ngày 5: hỗ trợ đối chiếu

Cùng C kiểm tra mô phỏng có "nhìn giống" dữ liệu thật không: so histogram thời gian phục vụ và số khách theo giờ do mô phỏng sinh ra với dữ liệu thật (so bằng mắt và bằng vài thống kê cơ bản).

### 4.7 Tiêu chí hoàn thành của A

- [ ] `load_log` chạy trên dữ liệu thật, hàm ước lượng chạy không lỗi.
- [ ] Đã quyết định mô hình thời gian phục vụ và ghi lý do (có số liệu AIC/KS).
- [ ] `docs/params.json` chốt từ tập ước lượng, có khoảng tin cậy, có phiên bản.
- [ ] Số liệu quan sát của tập kiểm tra đã bàn giao cho C.
- [ ] `docs/uoc_luong_kiem_dinh.md` và hình hoàn chỉnh.

---

## 5. Thành viên B: Bảng quyết định và kiểm thử lý thuyết

**Mục tiêu:** có bảng số quầy từng giờ bằng tham số thật, hai nguồn (Excel và Python) cho cùng kết quả, kèm kiểm thử tự động.

### 5.1 Ngày 1: điền bảng bằng tham số sơ bộ

Dùng bảng tham số tuần 1 để điền sheet `Quyet_dinh` (Excel) theo mẫu ở 12.1. Mục đích là chạy thử quy trình trước khi có tham số chốt, để Ngày 3 chỉ cần thay số.

### 5.2 Ngày 2: kiểm thử tự động cho `b_theory.py`

Tạo `tests/test_theory.py` (mẫu ở 12.3) kiểm tra các hàm lý thuyết với các **giá trị chuẩn** sau. Các giá trị này đã được kiểm tra bằng tính tay và bằng mô phỏng:

| Hàm và tham số | Kết quả chuẩn |
|---|---|
| `mmc(1.5, 1/3, 6)` | `Pw = 0,4217`, `Wq = 0,8433`, `P_sla = 0,9654` |
| `mmc(1.5, 1/3, 5)` | `Pw = 0,7625`, `Wq ≈ 4,57`, `P_sla = 0,669` |
| `erlang_a(2.0, 1/3, 0.1, 6)` | `SL = 0,8689`, `Wq = 1,1444`, `p_ab = 0,1144`, `util = 0,8856` |
| `mm1_random_split(1.5, 1/3, 6)` | `0,5056` |
| `allen_cunneen(1.5, 3.0, 0.25, 6)` | `0,5271` |
| `allen_cunneen(1.5, 3.0, 2.25, 6)` | `1,3704` |

(`Wq` của c = 5 là 4,575 khi tính tay với `C` đã làm tròn, 4,57 khi chạy code; chấp nhận sai số làm tròn.)

Thêm các kiểm tra **tính chất** (không phụ thuộc số cụ thể):

- `P_sla` tăng khi `c` tăng; `Wq` giảm khi `c` tăng.
- `mmc` với `ρ ≥ 1` trả về `Wq = ∞` và `P_sla = 0`.
- `erlang_a` khi `θ → 0` và `ρ < 1` tiến tới kết quả của `mmc`.
- `sipp_schedule` trả về số quầy không giảm khi `λ` tăng (với các tham số khác giữ nguyên).

Chạy bằng `pytest tests/` (cài `pip install pytest`).

### 5.3 Ngày 2–3: đối chiếu Excel và Python

Chạy cùng một bộ tham số (λ = 1,5, E[S] = 3, c = 5 và 6, t = 5) ở cả Excel và Python. Hai nguồn phải khớp đến chữ số thập phân thứ 3. Nếu lệch: kiểm tra đơn vị, cách tính `μ`, và định nghĩa SL (Erlang C không có bỏ về, Erlang-A có).

### 5.4 Ngày 3: bảng quyết định bằng `params.json`

Với mỗi khung giờ h dùng `λ_h`, `E[S]`, `cs²`, `θ` từ `params.json`:

| Cột | Cách tính |
|---|---|
| `a = λ_h·E[S]` | Tải theo giờ |
| `c_min ổn định` | `⌊a⌋ + 1` |
| `c theo Erlang C` | Nhỏ nhất đạt `P(Wq ≤ t) ≥ p` (bỏ qua bỏ về) |
| `c theo Erlang-A` | Nhỏ nhất đạt `SL(t) ≥ p` (có bỏ về), hàm `sipp_schedule` |
| `ρ` | `a/c` |
| `SL dự kiến` | Theo mô hình tương ứng |
| `Wq` dự kiến | Theo mô hình, có hiệu chỉnh Allen–Cunneen nếu `cs²` khác 1 |

Từ đó xuất ra: **lịch quầy theo giờ** (hai phương án), tổng quầy-giờ, và so sánh với lịch hằng số (số quầy lớn nhất của các giờ).

**Lưu ý lý thuyết quan trọng khi viết báo cáo:**
- Erlang C bỏ qua khách bỏ về, nên thường **đòi nhiều quầy hơn** Erlang-A (khách bỏ về giải phóng hàng đợi). Nêu rõ điều này khi so sánh hai cột.
- Allen–Cunneen chỉ hiệu chỉnh `Wq` trung bình; nó **không** cho `SL(t)`. Không dùng nó để quyết định số quầy, chỉ để ước lượng xem phân phối không mũ làm hàng đợi dài thêm hay ngắn đi bao nhiêu.
- SIPP bỏ qua quán tính giữa các giờ (khách tồn từ giờ trước). Mô phỏng sẽ làm rõ chỗ này.

### 5.5 Ngày 4: độ nhạy lý thuyết

Cho lịch Erlang-A, tính `SL` khi:

- λ tăng 10%, 20%, 30% (giữ lịch cũ);
- E[S] tăng 10%, 20%;
- θ thay đổi ±50%.

Trình bày bằng bảng hoặc biểu đồ. Đây là phần lý thuyết của phân tích độ nhạy, sau này so với kết quả mô phỏng ở tuần 3.

### 5.6 Ngày 5: đối chiếu với mô phỏng cùng C

Mang bảng quyết định đến buổi đối chiếu với C. Quy trình:

1. C chạy mô phỏng **hệ dừng** cho từng khung giờ (λ_h cố định, c theo bảng, chạy dài) với cùng tham số.
2. So `SL`, `Wq`, `ρ`, tỉ lệ bỏ về giữa bảng và mô phỏng (xem mục 7).
3. Giải thích mọi chênh lệch lớn hơn 2% hoặc nằm ngoài khoảng tin cậy.

### 5.7 Tiêu chí hoàn thành của B

- [ ] `tests/test_theory.py` chạy qua (pytest xanh), gồm cả giá trị chuẩn và tính chất.
- [ ] Excel và Python khớp nhau.
- [ ] Bảng quyết định bằng `params.json` đã xong, có hai phương án (Erlang C, Erlang-A) và lịch SIPP.
- [ ] Có bảng độ nhạy lý thuyết.
- [ ] `docs/bang_quyet_dinh.md` giải thích cách đọc bảng, giả định và giới hạn.

---

## 6. Thành viên C: Mô phỏng SimPy và kiểm chứng

**Mục tiêu:** mô phỏng đúng đặc tả, chạy được với tham số thật, và **qua kiểm chứng ba tầng**.

### 6.1 Ngày 1: rà soát code theo đặc tả

Tuần 1 đã có bảng "đặc tả ↔ hàm trong code". Tuần này kiểm tra từng hàm trong `c_sim.py`:

| Hàm | Kiểm tra gì |
|---|---|
| `simulate` | Đúng thực thể và sự kiện của đặc tả; khách đến theo λ từng giờ; VIP có ưu tiên; bỏ về; lịch quầy |
| `rep_stats` | `SL` tính đúng theo định nghĩa (được phục vụ **và** chờ ≤ t, mẫu số là mọi khách đến) |
| `run_reps` | Seed khác nhau cho mỗi lần lặp, seed cố định để lặp lại được |
| `feasible` | Dùng cận dưới của CI95 |
| `welch_curve` | Trung bình theo thứ tự khách qua nhiều lần chạy |

Viết ngắn gọn các điểm khác biệt giữa code và đặc tả (nếu có) rồi bàn với nhóm sửa bên nào.

### 6.2 Ngày 1–2: nối mô phỏng với dữ liệu thật

- `Model` gồm: `rates` (từ `params.json`), `service` (sampler theo cấu hình đã chọn ở 4.2), `theta`, `p_vip`, `hour_len`.
- Khi `p_vip = 0`, mô phỏng vẫn chạy bình thường; `SL` của VIP sẽ là `NaN`. Hàm `feasible` đang yêu cầu cả `sl_vip`; nếu không có VIP, sửa `feasible` để chỉ xét `sl` khi `p_vip = 0`.
- Kiểm tra số liệu hợp lý: số khách mô phỏng mỗi ngày gần số khách thực tế mỗi ngày (so với dữ liệu tập ước lượng).

### 6.3 Ngày 2–3: kiểm chứng tầng 1 và 2

Chi tiết ở mục 7. Tóm tắt: chạy hệ dừng, so với M/M/c (tầng 1) và Erlang-A chính xác (tầng 2).

**Nhận `params.json` từ A ở Ngày 3** và chạy lại các bước sau trên tham số thật:

- Chạy mô phỏng cho từng khung giờ với `c` theo bảng quyết định của B.
- So với số liệu quan sát của tập kiểm tra do A bàn giao (chỉ khi dữ liệu có đủ thông tin số quầy; xem 7.5).

### 6.4 Ngày 4: tầng 3, Welch, hàng chung và hàng riêng

- **Tầng 3:** phục vụ không mũ (lognormal với cv khác nhau) so với Allen–Cunneen. Tăng số lần lặp (ví dụ 100) để khoảng tin cậy hẹp lại, vì sai lệch lớn khi cv = 1,5 chưa chắc là sai số xấp xỉ mà có thể là nhiễu.
- **Welch:** vẽ đường trung bình trượt thời gian chờ theo thứ tự khách (ρ cao như 0,9 để thấy rõ giai đoạn khởi động). Chọn điểm warm-up nơi đường phẳng, ghi lại.
- **Hàng chung và hàng riêng:** chạy `simulate_separate` cho `random` và `jsq`, so với `mmc` và `mm1_random_split`.

### 6.5 Ngày 5: bảng kiểm chứng và báo cáo

Hoàn thành `ket_qua_kiem_chung.csv` (mẫu ở 12.2). Viết `docs/bao_cao_kiem_chung.md`: cấu hình từng tầng, kết quả, sai lệch, nhận xét, các hạn chế, và tiêu chí đạt (mục 7.3).

### 6.6 Ngày 5–7: chuẩn bị cho Tuần 3

Chạy thử `optimize_schedule` với số lần lặp nhỏ (ví dụ 20) để biết thời gian chạy và phát hiện lỗi sớm. Kết quả chính thức để Tuần 3. Ghi lại: thời gian chạy một lần đánh giá, các điểm cần sửa.

### 6.7 Tiêu chí hoàn thành của C

- [ ] Mô phỏng chạy với tham số thật mà không lỗi.
- [ ] Kiểm chứng tầng 1 và 2 đạt tiêu chí (mục 7.3).
- [ ] Kiểm chứng tầng 3 có kết quả, kèm giải thích mọi sai lệch lớn.
- [ ] Có hình Welch và hình hàng chung/hàng riêng.
- [ ] `docs/bao_cao_kiem_chung.md` hoàn chỉnh.
- [ ] Đã chạy thử `optimize_schedule` để biết thời gian chạy.

---

## 7. Quy trình kiểm chứng chi tiết

### 7.1 Cấu hình chuẩn

| Tầng | Mô hình lý thuyết | Cấu hình mô phỏng | Số liệu so sánh |
|---|---|---|---|
| 1 | M/M/c (Erlang C) | 1 khung giờ dài, λ cố định, phục vụ mũ, không bỏ về, không VIP, c cố định | `SL`, `Wq`, `ρ` |
| 2 | Erlang-A | Như trên nhưng thêm `θ` | `SL`, `Wq`, tỉ lệ bỏ về, `ρ` |
| 3 | Allen–Cunneen | Như tầng 1 nhưng phục vụ lognormal với cv thay đổi (0,5; 1,0; 1,5) | `Wq` |

Tham số tham chiếu: λ = 1,5, E[S] = 3 phút, c = 6 (tầng 1 và 3); λ = 2,0, E[S] = 3, θ = 0,1, c = 6 (tầng 2). Sau khi chạy với bộ tham số tham chiếu này, **thêm một bộ tham số theo dữ liệu thật** (λ_h của giờ đỉnh, E[S] và θ ước lượng).

### 7.2 Thiết lập mô phỏng hệ dừng

- Độ dài chạy: 8.000 phút cho mỗi lần lặp, bỏ 500 phút đầu (warm-up, điều chỉnh sau khi có kết quả Welch).
- Số lần lặp: ít nhất 30 (tầng 3 nên 100).
- Seed khác nhau cho mỗi lần lặp.
- `SL` đo trên mọi khách đến (được phục vụ **và** chờ ≤ 5 phút).
- `Wq` đo trên mọi khách đến (kể cả khách bỏ về, theo thời gian đã chờ) để khớp công thức Little `Wq = Lq/λ`.

### 7.3 Tiêu chí đạt

| Tầng | Tiêu chí đạt |
|---|---|
| 1 và 2 | Giá trị lý thuyết nằm trong khoảng tin cậy 95% của mô phỏng, **hoặc** sai lệch tương đối < 2% |
| 3 | Sai lệch ghi lại và giải thích. Với cv gần 1, kỳ vọng sai lệch nhỏ. Với cv lớn, chấp nhận sai lệch lớn hơn nhưng phải nêu rõ nguyên nhân (giới hạn của xấp xỉ, nhiễu) |

Khi không đạt: kiểm tra theo thứ tự: (1) đơn vị thời gian, (2) định nghĩa `SL` và `Wq` có khớp giữa lý thuyết và mô phỏng không, (3) warm-up có đủ không, (4) số lần lặp có đủ không, (5) lỗi trong logic mô phỏng (ví dụ thứ tự ưu tiên, cách tính bỏ về).

### 7.4 Kết quả tham chiếu (để biết đang ở mức nào)

Lần chạy trên dữ liệu giả lập cho thấy (30 lần lặp, chạy 8.000 phút, warm-up 500 phút):

| Mô hình | Chỉ số | Lý thuyết | Mô phỏng |
|---|---|---|---|
| M/M/c | SL | 0,9654 | 0,9664 ± 0,0043 |
| M/M/c | Wq (phút) | 0,8433 | 0,8385 ± 0,0449 |
| M/M/c+M | SL | 0,8689 | 0,8694 ± 0,0031 |
| M/M/c+M | Tỉ lệ bỏ về | 0,1144 | 0,1140 ± 0,0022 |
| M/G/c, cv = 0,5 | Wq (Allen–Cunneen) | 0,5271 | 0,5473 ± 0,0184 |
| M/G/c, cv = 1,5 | Wq (Allen–Cunneen) | 1,3704 | 1,1935 ± 0,0940 |

Nếu kết quả của nhóm ở tầng 1 và 2 lệch rõ ràng so với bảng này (cùng tham số), nhiều khả năng có lỗi cần tìm.

### 7.5 So sánh với dữ liệu thật (kiểm chứng ngoài mẫu)

Chỉ làm được khi dữ liệu có đủ thông tin về **số quầy (nhân viên) đang làm việc theo từng giờ**. Nếu dữ liệu cho phép suy ra (ví dụ qua định danh nhân viên phục vụ theo giờ):

1. Lập lịch quầy thực tế `c_h` theo giờ từ tập kiểm tra.
2. Chạy mô phỏng với tham số ước lượng từ tập ước lượng và lịch `c_h` thực tế.
3. So sánh với số liệu quan sát ở tập kiểm tra: `Wq` trung bình, tỉ lệ bỏ về, `SL` theo giờ.
4. Báo cáo chênh lệch và giải thích; chênh lệch lớn có thể do mô hình bỏ sót (ví dụ nhân viên làm việc không liên tục, khách trở lại).

Nếu không suy ra được số quầy: ghi rõ đây là hạn chế, chỉ làm kiểm chứng theo lý thuyết (ba tầng) và so sánh phân phối đầu vào (số khách theo giờ, thời gian phục vụ).

---

## 8. Ghép nối: luồng dữ liệu giữa các module

### 8.1 Luồng chung

```
data/clean/*.csv ──► a_data.load_log ──► a_data.estimate_all ──► docs/params.json
                                                                      │
                          ┌───────────────────────────────────────────┤
                          ▼                                           ▼
              b_theory (bảng quyết định)                  c_sim (Model từ params.json)
                          │                                           │
                          └──────────► so sánh, kiểm chứng ◄──────────┘
```

### 8.2 Định dạng `params.json`

Thống nhất một định dạng duy nhất (đề xuất, có thể thêm trường nhưng không đổi tên trường đã có mà không báo cả nhóm):

```json
{
  "version": "v1",
  "ngay_chot": "2026-..-..",
  "nguon": "Anonymous Bank, thang .., ngay lam viec, ..h-..h",
  "don_vi_thoi_gian": "phut",
  "rates_per_min": [0.80, 1.20, 1.60],
  "rates_ci95": [0.05, 0.06, 0.07],
  "service": {
    "kieu": "mix_lognormal | lognormal | gamma | weibull | empirical",
    "mean": 3.24,
    "cv": 1.05,
    "p_quick": 0.69,
    "quick": {"mu": 0.0, "sigma": 0.0},
    "complex": {"mu": 0.0, "sigma": 0.0},
    "samples_file": "data/clean/service_samples.csv"
  },
  "theta": 0.092,
  "theta_ci95": 0.008,
  "p_vip": 0.0,
  "ghi_chu": "..."
}
```

Chỉ các trường thuộc cấu hình đã chọn ở 4.2 là bắt buộc. B và C **không tự ước lượng lại** mà đọc từ file này. Mỗi lần A cập nhật phải đổi `version` và thông báo.

### 8.3 Thay đổi nhỏ cần làm ở `main.py`

- Thay `a_data.generate_log(...)` bằng `a_data.load_log(...)`.
- Đọc `params.json` thay vì dùng `est` do code sinh ra (hoặc xuất `est` ra `params.json` rồi các bước sau đọc lại).
- Với dữ liệu thật, bỏ các bước dùng "hệ thống thật" (`true_model`, đánh giá "THẬT") vì không có hệ thống thật để kiểm tra; thay bằng so sánh với tập kiểm tra (mục 7.5).

---

## 9. Việc chung và kiểm tra chéo

### 9.1 Họp mở đầu (Ngày 1, 30 phút)

1. Xem lại cổng kiểm soát tuần 1, xử lý mục còn thiếu.
2. Thống nhất **định dạng `params.json`** và quy tắc cập nhật (đổi version, báo nhóm).
3. Chốt điểm nối Ngày 3 và phương án dự phòng (dùng tham số sơ bộ nếu A trễ).
4. Phân công người đọc lại README mục 7, 9, 10.

### 9.2 Họp nhanh hằng ngày

15 phút, ba câu hỏi như tuần 1, ghi vào `docs/nhat_ky.md`.

### 9.3 Kiểm tra chéo (Ngày 6)

| Người kiểm tra | Sản phẩm của | Cần xem gì |
|---|---|---|
| A | B | Bảng quyết định dùng đúng `params.json`? Đơn vị và công thức nhất quán? Giới hạn được nêu? |
| B | C | Mô phỏng khớp đặc tả? Định nghĩa `SL` và `Wq` khớp với lý thuyết? Kiểm chứng đạt tiêu chí? |
| C | A | Hàm đọc dữ liệu, ước lượng đúng? Mô hình dịch vụ có lý do? Tách train/test đúng cách? |

Ghi nhận xét theo bảng (Mục / Phát hiện / Mức độ / Đã sửa?). Lỗi mức nặng sửa trước cổng.

### 9.4 Báo cáo tuần 2

Một trang: kết quả (tham số chốt, bảng quyết định, kiểm chứng), vấn đề gặp và cách xử lý, kế hoạch Tuần 3.

---

## 10. Cổng kiểm soát cuối Tuần 2

Chỉ bắt đầu Tuần 3 (tối ưu, độ nhạy, báo cáo, thuyết trình) khi **tất cả** các mục sau được đánh dấu.

**Dữ liệu và tham số**
- [ ] `params.json` đã chốt (có version, từ tập ước lượng).
- [ ] Mô hình thời gian phục vụ đã chọn có căn cứ (AIC/KS/Q-Q) và được ghi lý do.
- [ ] Số liệu quan sát của tập kiểm tra đã bàn giao.

**Lý thuyết**
- [ ] Bảng quyết định hoàn chỉnh (Erlang C, Erlang-A, SIPP).
- [ ] Kiểm thử tự động chạy qua; Excel và Python khớp.
- [ ] Có bảng độ nhạy lý thuyết.

**Mô phỏng**
- [ ] Mô phỏng chạy với tham số thật.
- [ ] Kiểm chứng tầng 1 và 2 đạt tiêu chí; tầng 3 có giải thích.
- [ ] Welch đã dùng để xác nhận warm-up.
- [ ] Đã biết thời gian chạy của bước tối ưu.

**Quản lý**
- [ ] Kiểm tra chéo xong, lỗi nặng đã sửa.
- [ ] Báo cáo tuần 2 đã viết, kế hoạch Tuần 3 đã chia việc.
- [ ] `python main.py` chạy từ đầu đến cuối trên máy của ít nhất hai thành viên.

Nếu **kiểm chứng tầng 1 hoặc 2 chưa đạt**, không chuyển sang Tuần 3: mọi kết quả tối ưu sẽ không đáng tin.

---

## 11. Nếu bị kẹt

| Tình huống | Cách xử lý |
|---|---|
| `params.json` của A trễ | B và C dùng tham số sơ bộ tuần 1; khi có bản chốt, chạy lại các bước phụ thuộc |
| Không phân phối nào khớp thời gian phục vụ | Dùng lấy mẫu trực tiếp từ dữ liệu (`empirical_service`), ghi hạn chế |
| Mô phỏng lệch lý thuyết tầng 1 | Kiểm tra định nghĩa `SL`, `Wq` (mọi khách hay chỉ khách được phục vụ), đơn vị, warm-up, số lần lặp |
| Mô phỏng chạy quá chậm | Giảm độ dài chạy hoặc số lần lặp khi thử, tăng khi chạy chính thức; tìm đoạn mã chậm bằng `cProfile` |
| Excel và Python lệch | Cùng đưa một bộ tham số vào hai nơi; so từng cột (ρ, C, Wq, SL) để biết lệch từ bước nào |
| Dữ liệu không có khách bỏ về | Đặt `θ = 0`, bỏ tầng 2 trên dữ liệu thật (vẫn chạy tầng 2 với tham số tham chiếu), ghi hạn chế |
| Dữ liệu không có VIP hoặc loại giao dịch | Đặt `p_vip = 0`, dùng cấu hình dịch vụ đơn, sửa `feasible` bỏ tiêu chí VIP |
| Ít dữ liệu cho từng khung giờ | Gộp các khung có hành vi giống nhau, hoặc chấp nhận khoảng tin cậy rộng và nêu rõ |
| Kiểm chứng tầng 3 lệch nhiều | Tăng số lần lặp để loại trừ nhiễu; nếu vẫn lệch, ghi nhận đây là giới hạn của Allen–Cunneen và dựa vào mô phỏng |
| Quá tải việc | Ưu tiên: `params.json` đúng, bảng quyết định, kiểm chứng tầng 1–2. Hoãn: Welch chi tiết, hàng riêng, độ nhạy lý thuyết |

---

## 12. Phụ lục

### 12.1 Mẫu bảng quyết định (sheet `Quyet_dinh`)

| Giờ | λ_h | E[S] | cs² | a | c ổn định | c Erlang C | c Erlang-A | ρ (Erlang-A) | SL dự kiến | Wq dự kiến | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 8h | | | | | | | | | | | |
| 9h | | | | | | | | | | | |
| … | | | | | | | | | | | |

Hàng cuối: tổng quầy-giờ cho từng phương án và lịch hằng số (số quầy lớn nhất).

### 12.2 Mẫu bảng kiểm chứng (`ket_qua_kiem_chung.csv`)

| kiem_chung | chi_so | ly_thuyet | mo_phong | ci95 | sai_lech_pct | dat (Y/N) | ghi_chu |
|---|---|---|---|---|---|---|---|

Các tầng và chỉ số như mục 7.1. Cột `dat` điền theo tiêu chí 7.3.

### 12.3 Mẫu kiểm thử tự động (`tests/test_theory.py`)

```python
import math
import pytest
import b_theory as th

def test_mmc_reference():
    m = th.mmc(1.5, 1/3, 6)
    assert m["Pw"] == pytest.approx(0.4217, abs=5e-4)
    assert m["Wq"] == pytest.approx(0.8433, abs=5e-3)
    assert m["P_sla"] == pytest.approx(0.9654, abs=5e-4)

def test_mmc_unstable():
    m = th.mmc(2.0, 1/3, 6)          # rho = 1
    assert math.isinf(m["Wq"]) and m["P_sla"] == 0

def test_monotone_in_c():
    sl = [th.mmc(1.5, 1/3, c)["P_sla"] for c in range(5, 10)]
    assert all(b >= a for a, b in zip(sl, sl[1:]))

def test_erlang_a_reference():
    e = th.erlang_a(2.0, 1/3, 0.1, 6)
    assert e["SL"] == pytest.approx(0.8689, abs=5e-4)
    assert e["Wq"] == pytest.approx(1.1444, abs=5e-3)
    assert e["p_ab"] == pytest.approx(0.1144, abs=5e-4)

def test_allen_cunneen_reference():
    assert th.allen_cunneen(1.5, 3.0, 0.25, 6) == pytest.approx(0.5271, abs=5e-3)
    assert th.allen_cunneen(1.5, 3.0, 2.25, 6) == pytest.approx(1.3704, abs=5e-3)

def test_split_queues_worse():
    assert th.mm1_random_split(1.5, 1/3, 6) < th.mmc(1.5, 1/3, 6)["P_sla"]
```

Chạy từ thư mục dự án: `PYTHONPATH=. pytest tests/` (hoặc đặt `conftest.py` rỗng ở thư mục gốc để pytest tự thêm đường dẫn).

### 12.4 Gợi ý mã cho sampler mới (thêm vào `common.py`)

```python
from scipy import stats
import numpy as np

def gamma_service(shape, scale):
    return lambda rng: (rng.gamma(shape, scale), 0)

def weibull_service(shape, scale):
    return lambda rng: (scale * rng.weibull(shape), 0)

def empirical_service(samples):
    """Lấy mẫu có hoàn lại từ dữ liệu thật (bootstrap)."""
    s = np.asarray(samples, float)
    return lambda rng: (float(s[rng.integers(len(s))]), 0)
```

Mỗi sampler có dạng `rng -> (thời gian phục vụ, loại giao dịch)` giống `exp_service`, `lognorm_service`, `mix_service` hiện có để `simulate` dùng chung được.

### 12.5 Kiểm tra tính hợp lý (sanity checks) trước khi tin vào kết quả

- Tổng số khách mô phỏng một ngày gần số khách thực tế trung bình một ngày.
- Hiệu suất `ρ` của mô phỏng ≈ `λ·E[S]·(1 − tỉ lệ bỏ về)/(c·1)` theo từng giờ.
- Thời gian chờ trung bình tăng khi bớt quầy và giảm khi thêm quầy.
- Khi `θ = 0` và `ρ < 1`, tỉ lệ bỏ về mô phỏng bằng 0 và kết quả tiến tới M/M/c (nếu phục vụ mũ).
- Hai lần chạy với cùng seed cho đúng cùng kết quả.

### 12.6 Mẫu báo cáo tuần 2 (1 trang, `docs/bao_cao_tuan_2.md`)

```
# Báo cáo Tuần 2
1. Mục tiêu tuần: [..]
2. Tham số chốt (version, ngày): λ_h [..]; mô hình dịch vụ [..]; θ [..]
3. Bảng quyết định: lịch Erlang C [..]; lịch Erlang-A [..]; tổng quầy-giờ [..]
4. Kiểm chứng: tầng 1 [..]; tầng 2 [..]; tầng 3 [..] (đạt/chưa, sai lệch)
5. Vấn đề và cách xử lý: [..]
6. Cổng kiểm soát: đạt / chưa đạt (mục nào, vì sao)
7. Kế hoạch Tuần 3: [..]
```
