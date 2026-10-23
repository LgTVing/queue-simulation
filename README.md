# Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu

> Dự án nhóm 3 sinh viên, thời lượng 3 tuần. Hệ thống nghiên cứu: **quầy giao dịch ngân hàng** (tổng quát hóa được cho phòng khám, căng tin, trung tâm hành chính công).
> Quy trình xuyên suốt: **số liệu thực tế → tính toán bằng toán học (Excel) → bảng số quầy → mới viết code mô phỏng để kiểm chứng và tối ưu.**

---

## Mục lục

1. [Tổng quan và mục tiêu](#1-tổng-quan-và-mục-tiêu)
2. [Phạm vi và giả định](#2-phạm-vi-và-giả-định)
3. [Nguồn dữ liệu](#3-nguồn-dữ-liệu)
4. [Quy trình tổng thể 8 giai đoạn](#4-quy-trình-tổng-thể-8-giai-đoạn)
5. [Giai đoạn 1: Thu thập và làm sạch dữ liệu](#5-giai-đoạn-1-thu-thập-và-làm-sạch-dữ-liệu)
6. [Giai đoạn 2: Phân tích thống kê và kiểm định](#6-giai-đoạn-2-phân-tích-thống-kê-và-kiểm-định)
7. [Giai đoạn 3: Mô hình toán học](#7-giai-đoạn-3-mô-hình-toán-học)
8. [Giai đoạn 4: Bảng quyết định (tính tay/Excel)](#8-giai-đoạn-4-bảng-quyết-định-tính-tayexcel)
9. [Giai đoạn 5: Mô phỏng sự kiện rời rạc bằng SimPy](#9-giai-đoạn-5-mô-phỏng-sự-kiện-rời-rạc-bằng-simpy)
10. [Giai đoạn 6: Kiểm chứng mô hình](#10-giai-đoạn-6-kiểm-chứng-mô-hình)
11. [Giai đoạn 7: Tối ưu lịch quầy và phân tích độ nhạy](#11-giai-đoạn-7-tối-ưu-lịch-quầy-và-phân-tích-độ-nhạy)
12. [Giai đoạn 8: Báo cáo và thuyết trình](#12-giai-đoạn-8-báo-cáo-và-thuyết-trình)
13. [Cấu trúc mã nguồn và cách chạy](#13-cấu-trúc-mã-nguồn-và-cách-chạy)
14. [Chuyển từ dữ liệu giả lập sang dữ liệu thật](#14-chuyển-từ-dữ-liệu-giả-lập-sang-dữ-liệu-thật)
15. [Kết quả tham chiếu từ bản chạy thử](#15-kết-quả-tham-chiếu-từ-bản-chạy-thử)
16. [Kế hoạch 3 tuần và phân công](#16-kế-hoạch-3-tuần-và-phân-công)
17. [Rủi ro và cách xử lý](#17-rủi-ro-và-cách-xử-lý)
18. [Câu hỏi phản biện thường gặp](#18-câu-hỏi-phản-biện-thường-gặp)
19. [Hướng mở rộng](#19-hướng-mở-rộng)
20. [Tài liệu tham khảo](#20-tài-liệu-tham-khảo)

---

## 1. Tổng quan và mục tiêu

### 1.1 Bài toán

Một điểm giao dịch có khách đến ngẫu nhiên, xếp hàng và được phục vụ bởi một số quầy. Mở ít quầy thì khách chờ lâu, thậm chí bỏ về. Mở nhiều quầy thì tốn chi phí và quầy rảnh nhiều. Cần xác định **số quầy tối thiểu** để đáp ứng một **cam kết dịch vụ (SLA)**.

### 1.2 Cam kết dịch vụ dùng trong dự án

| Nhóm khách | Cam kết |
|---|---|
| Khách thường | ≥ 90% khách được phục vụ trong ≤ 5 phút kể từ lúc vào hàng |
| Khách VIP (nếu có) | ≥ 90% khách được phục vụ trong ≤ 2 phút |

Định nghĩa chính xác: **SL(t) = P(khách được phục vụ và thời gian chờ ≤ t)**, tính trên **mọi khách đến**. Khách bỏ về được tính là không đạt. Đây là định nghĩa bảo thủ, cần ghi rõ trong báo cáo.

### 1.3 Mục tiêu cụ thể

1. Thu thập hoặc lấy số liệu thực tế về thời gian đến, thời gian phục vụ, hành vi bỏ về.
2. Kiểm định phân phối và ước lượng tham số từ dữ liệu.
3. Tính các chỉ số theo mô hình M/M/c (thời gian chờ, độ dài hàng đợi, hiệu suất sử dụng) và các mô hình mở rộng.
4. Lập **bảng quyết định số quầy theo từng khung giờ** bằng tính toán, trước khi viết code.
5. Xây dựng mô phỏng sự kiện rời rạc bằng SimPy, kiểm chứng với lý thuyết (sai lệch dưới vài %).
6. Dùng mô phỏng để xử lý những gì công thức không làm được: ưu tiên VIP, lịch đổi theo giờ, tối ưu, độ nhạy.
7. Kết luận số quầy cụ thể theo từng giờ, kèm khuyến nghị và giới hạn của kết quả.

---

## 2. Phạm vi và giả định

### 2.1 Trong phạm vi

- Một hàng đợi chung, FIFO (có ưu tiên VIP không ngắt), c quầy giống nhau.
- Tốc độ đến thay đổi theo giờ (quá trình Poisson không đồng nhất, chia khung giờ).
- Hai loại giao dịch (nhanh, phức tạp) với phân phối thời gian phục vụ riêng.
- Khách bỏ về khi chờ quá lâu (kiên nhẫn có phân phối mũ).
- Lịch quầy thay đổi theo giờ, nhân viên chỉ rời quầy sau khi phục vụ xong khách đang xử lý.

### 2.2 Ngoài phạm vi (ghi vào phần hạn chế)

- Tốc độ đến thay đổi theo ngày trong tuần hoặc theo đợt cuối tháng.
- Khách rời hàng sang quầy khác (jockeying), nhóm khách đến cùng nhau.
- Quầy có kỹ năng khác nhau (chỉ một số quầy làm được giao dịch phức tạp).
- Chi phí chi tiết bằng tiền.

### 2.3 Giả định cần nêu rõ

- Trong từng khung giờ, tốc độ đến xem như hằng số.
- Thời gian phục vụ độc lập với thời gian đến và với kiên nhẫn của khách.
- Mỗi quầy có năng suất như nhau.
- Hệ thống mở cửa trống (không có khách tồn từ trước giờ mở cửa).

---

## 3. Nguồn dữ liệu

### 3.1 Chiến lược khuyến nghị: kết hợp hai nguồn

| Phương án | Ưu điểm | Rủi ro |
|---|---|---|
| **A. Thu thập tại chỗ** (chi nhánh ngân hàng, bộ phận một cửa, phòng đào tạo, ký túc xá) | Đúng bối cảnh Việt Nam, thuyết phục | Cần xin phép, cỡ mẫu nhỏ, ngân hàng hay từ chối |
| **B. Bộ dữ liệu thật "Anonymous Bank" của Technion SEELab** | Có sẵn, cỡ mẫu lớn, trích dẫn được | Là tổng đài (không phải quầy trực tiếp), dữ liệu cũ |

**Cách kết hợp:** dùng B làm dữ liệu chính, làm thêm một đợt khảo sát nhỏ ở A (2–3 buổi, mỗi buổi khoảng 2 giờ) để địa phương hóa và đối chiếu.

### 3.2 Về bộ dữ liệu Anonymous Bank

- Nguồn: Technion SEE Center (Israel). Địa chỉ trang dữ liệu: `https://see-center.iem.technion.ac.il/databases/AnonymousBank/` (tìm tài liệu mô tả `AnonymousBank.pdf` trên trang này).
- Dữ liệu là lịch sử từng cuộc gọi của tổng đài một ngân hàng ở Israel, gồm 12 file theo tháng, mỗi tháng khoảng 20.000–30.000 cuộc gọi, ghi cả kết quả (được phục vụ hoặc bỏ về).
- **Điều kiện sử dụng:** dữ liệu được dùng tự do, nhưng cần thông báo cho giáo sư Avi Mandelbaum (email có trên trang dữ liệu) và **ghi nguồn** trong báo cáo, slide.
- Phép tương đương: nhân viên trực = quầy, cuộc gọi = khách, thời gian chờ trước khi gặp nhân viên = thời gian chờ, cúp máy khi chờ = bỏ về. Nhóm phải nói rõ phép tương đương này.
- Khi đọc dữ liệu, chú ý: đơn vị thời gian (đối chiếu tài liệu mô tả), các loại kết quả đặc biệt cần loại bỏ (ví dụ bản ghi ảo), múi giờ và ngày làm việc của Israel (tuần làm việc không giống Việt Nam).
- Nên lọc về một khung làm việc tương tự quầy ngân hàng (ví dụ ngày làm việc, từ 8h đến 17h) và chọn một loại dịch vụ để mô hình thống nhất.

### 3.3 Xin dữ liệu tại chỗ (phương án A)

Ưu tiên theo thứ tự dễ xin:

1. **Log máy lấy số thứ tự đã ẩn danh** (thời điểm lấy số, thời điểm gọi số, thời điểm kết thúc). Đây là dữ liệu tốt nhất vì không cần ngồi đo.
2. Nếu không có log: quan sát trực tiếp bằng đồng hồ bấm giờ hoặc bảng tính trên điện thoại.
3. Nếu ngân hàng từ chối: chọn nơi dễ xin hơn như phòng đào tạo, phòng công tác sinh viên, căng tin, thư viện của trường.

Cần giấy giới thiệu của giảng viên và cam kết không ghi tên, giấy tờ hay thông tin cá nhân của khách.

---

## 4. Quy trình tổng thể 8 giai đoạn

```
[1 Dữ liệu] -> [2 Thống kê, kiểm định] -> [3 Mô hình toán] -> [4 Bảng quyết định (Excel)]
                                                                         |
                                                                         v  (cổng kiểm soát: bảng đã xong, có ví dụ tính tay)
[8 Báo cáo, thuyết trình] <- [7 Tối ưu, độ nhạy] <- [6 Kiểm chứng] <- [5 Mô phỏng SimPy]
```

**Nguyên tắc:** chỉ bắt đầu viết code mô phỏng (giai đoạn 5) khi giai đoạn 4 đã hoàn thành và có ít nhất một dòng của bảng quyết định được hai người tính độc lập cho cùng kết quả. Code dùng để **tái hiện và mở rộng**, không dùng để khám phá.

---

## 5. Giai đoạn 1: Thu thập và làm sạch dữ liệu

### 5.1 Biến cần ghi cho mỗi khách

| Biến | Ý nghĩa | Ghi chú |
|---|---|---|
| `day` | Ngày quan sát (0, 1, 2, ...) | |
| `t` | Thời điểm khách vào hàng, tính bằng phút kể từ giờ mở cửa | |
| `hour` | Khung giờ (0 ứng với giờ đầu tiên) | Tính từ `t` |
| `cls` | Loại giao dịch (0 = nhanh, 1 = phức tạp) | Khách bỏ về thì không biết, để trống |
| `vip` | 1 nếu khách VIP, 0 nếu thường | |
| `wait` | Thời gian chờ (phút) | Với khách bỏ về là thời gian chờ đến khi rời hàng |
| `served` | 1 nếu được phục vụ, 0 nếu bỏ về | |
| `svc` | Thời gian phục vụ (phút) | Để trống nếu bỏ về |

Đây cũng chính là định dạng cột mà `a_data.py` và `c_sim.py` đang dùng. Dữ liệu thật cần quy về cùng dạng này (xem [mục 14](#14-chuyển-từ-dữ-liệu-giả-lập-sang-dữ-liệu-thật)).

### 5.2 Quy trình quan sát tại chỗ (nếu phải tự đo)

- Mỗi buổi 2–3 người: một người đếm khách đến và ghi giờ vào hàng, một người ghi giờ bắt đầu và kết thúc phục vụ ở từng quầy, một người ghi khách bỏ về và đối chiếu.
- Dùng một đồng hồ chung (cùng đồng hồ điện thoại, đã đồng bộ) và một mẫu bảng cố định, nhập vào bảng tính ngay trong buổi.
- Ghi số quầy đang mở theo từng thời điểm, vì đây là điều kiện để diễn giải thời gian chờ.
- Đo tối thiểu 3 buổi, ưu tiên các khung giờ khác nhau (sáng, trưa, chiều, giờ cao điểm).

### 5.3 Cỡ mẫu tối thiểu

- Ước lượng thời gian phục vụ trung bình với sai số ±10%, độ tin cậy 95%: `n ≈ (1,96 · cv / 0,1)²`. Với cv ≈ 0,8–1 cần khoảng **250–400 lượt phục vụ**.
- Ước lượng tốc độ đến của một khung giờ với sai số ±10%: cần khoảng **384 lượt đến** trong khung giờ đó (vì sai số tương đối ≈ `1,96/√N`). Nếu mỗi giờ có 60 khách thì cần khoảng 6 ngày. Nếu khảo sát ngắn, gộp các khung 30–60 phút có hành vi giống nhau, hoặc chấp nhận sai số ±20% (khoảng 100 lượt đến).

### 5.4 Làm sạch dữ liệu

- Loại bản ghi thiếu thời gian, thời gian âm, hoặc bản ghi ảo/thử nghiệm.
- Kiểm tra thời gian phục vụ bằng 0 hoặc quá dài (ngoại lai), quyết định giữ hay loại và ghi vào báo cáo.
- Kiểm tra tính toàn vẹn: `wait ≥ 0`, `svc > 0` với khách được phục vụ, số khách đến theo giờ không bất thường.
- Tách riêng phần dùng để **ước lượng** (train) và phần dùng để **kiểm tra** (test), ví dụ chia theo ngày.

---

## 6. Giai đoạn 2: Phân tích thống kê và kiểm định

### 6.1 Thống kê mô tả theo khung giờ

Với mỗi khung giờ h tính: số khách trung bình mỗi ngày, `λ_h` (khách/phút), thời gian phục vụ trung bình `E[S]`, hệ số biến thiên `cv`, tỉ lệ bỏ về.

### 6.2 Quá trình đến

- **Poisson trong từng khung giờ:** với `n` ngày quan sát, đếm số khách mỗi ngày trong khung giờ h, tính chỉ số phân tán `D = Σ(Nᵢ − N̄)² / N̄`. Nếu quá trình là Poisson thì `D ~ χ²(n−1)`. P-value lớn nghĩa là chưa bác bỏ được giả thuyết Poisson.
- **Tốc độ đến có đổi theo giờ không:** kiểm định chi-bình phương với giả thuyết các giờ có cùng tốc độ. Nếu bị bác bỏ (thường rất mạnh) thì phải dùng mô hình theo khung giờ, không dùng M/M/c thuần với một λ.
- Kiểm tra bổ sung: khoảng cách giữa các lần đến trong một khung giờ có phân phối mũ không (KS, Q-Q plot).

### 6.3 Thời gian phục vụ

- Fit các phân phối: exponential, lognormal, gamma, Weibull (cố định `loc = 0`). So sánh bằng **AIC**, **KS**, **Q-Q plot**.
- Thử gộp mọi loại giao dịch và thử tách theo loại. Thường dữ liệu gộp không khớp phân phối đơn nào, nhưng tách theo loại giao dịch thì lognormal khớp tốt. Đây là kết quả đáng đưa vào báo cáo.
- **Lưu ý:** p-value của KS khi tham số được ước lượng từ chính mẫu là hơi lạc quan. Dùng KS như tham khảo, kết hợp AIC và Q-Q plot.
- Với hỗn hợp hai loại: ước lượng tỉ lệ `p_quick` và tham số lognormal `(μ, σ)` của từng loại. Tính trung bình và `cs²` của hỗn hợp (công thức ở [mục 7.3](#73-m-g-c-xấp-xỉ-allencunneen)).

### 6.4 Hành vi bỏ về (dữ liệu bị kiểm duyệt)

Khách được phục vụ cho ta biết "kiên nhẫn ≥ thời gian chờ", khách bỏ về cho ta biết "kiên nhẫn = thời gian chờ". Với phân phối mũ, ước lượng hợp lý cực đại:

```
θ̂ = (số khách bỏ về) / (tổng thời gian chờ của TẤT CẢ khách)
```

Khoảng tin cậy gần đúng 95%: `θ̂ · (1 ± 1,96/√số_khách_bỏ_về)`. Kiên nhẫn trung bình = `1/θ̂`.

### 6.5 Khách VIP

Ước lượng tỉ lệ `p_vip` bằng tỉ lệ mẫu, kèm khoảng tin cậy nhị thức.

---

## 7. Giai đoạn 3: Mô hình toán học

Ký hiệu: `λ` tốc độ đến, `μ = 1/E[S]` tốc độ phục vụ mỗi quầy, `c` số quầy, `a = λ/μ` tải (Erlang), `ρ = a/c` hiệu suất sử dụng. **Luôn dùng cùng một đơn vị thời gian (phút) cho λ và μ.**

### 7.1 M/M/c (công thức Erlang C)

Điều kiện ổn định: **ρ < 1**, tức `c > a`.

```
Xác suất phải chờ:   C(c, a) = [ aᶜ / (c! · (1−ρ)) ] / [ Σ_{k=0}^{c-1} aᵏ/k!  +  aᶜ / (c! · (1−ρ)) ]
Thời gian chờ TB:    Wq = C / (c·μ − λ)
Độ dài hàng đợi:     Lq = λ · Wq          (định luật Little)
Thời gian trong hệ:  W  = Wq + 1/μ
Số khách trong hệ:   L  = Lq + a
Mức đáp ứng:         P(Wq ≤ t) = 1 − C · exp(−(c·μ − λ)·t)
```

Số quầy nhỏ nhất cho SLA: tăng dần `c` từ `⌊a⌋ + 1` đến khi `P(Wq ≤ t) ≥ p`.

### 7.2 Quy tắc căn bậc hai (kiểm tra nhanh)

`c ≈ a + β·√a`. Hệ số β liên hệ với xác suất phải chờ (xấp xỉ Halfin–Whitt): `P(phải chờ) ≈ [1 + β·Φ(β)/φ(β)]⁻¹`, trong đó Φ, φ là hàm phân phối và hàm mật độ chuẩn. Dùng để kiểm tra kết quả Erlang C có hợp lý về cỡ, không dùng làm kết quả cuối.

### 7.3 M/G/c: xấp xỉ Allen–Cunneen

Khi thời gian phục vụ không phải phân phối mũ, với `cs²` là bình phương hệ số biến thiên:

```
Wq(M/G/c) ≈ (1 + cs²)/2 · Wq(M/M/c)
```

Với hỗn hợp hai lognormal (tỉ lệ `p`, tham số `(μ₁,σ₁)` và `(μ₂,σ₂)`):

```
E[S]   = p·exp(μ₁ + σ₁²/2) + (1−p)·exp(μ₂ + σ₂²/2)
E[S²]  = p·exp(2μ₁ + 2σ₁²) + (1−p)·exp(2μ₂ + 2σ₂²)
cs²    = (E[S²] − E[S]²) / E[S]²
```

Xấp xỉ này kém chính xác hơn khi `cs²` lớn (xem [mục 15](#15-kết-quả-tham-chiếu-từ-bản-chạy-thử)), nên cần mô phỏng để kiểm tra.

### 7.4 Có khách bỏ về: Erlang-A (M/M/c + M)

Chuỗi sinh–tử với tốc độ chết ở trạng thái `n`: `min(n, c)·μ + max(n − c, 0)·θ`. Phân phối dừng:

```
π_n = π_{n-1} · λ / ( min(n,c)·μ + max(n−c,0)·θ ),  chuẩn hóa Σ π_n = 1
Lq = Σ_{j≥0} j · π_{c+j}
Wq (trung bình của MỌI khách, kể cả khách bỏ về) = Lq / λ
Tỉ lệ bỏ về = θ · Lq / λ
Hiệu suất thực = λ·(1 − tỉ lệ bỏ về) / (c·μ)
```

**Mức đáp ứng chính xác** `SL(t)`: dùng tính chất PASTA (khách đến thấy trạng thái dừng). Khách đánh dấu thấy `j` khách đứng trước trong hàng, ta lập chuỗi Markov hấp thụ với trạng thái `k` = số khách đứng trước nó:

- `k → k−1` với tốc độ `c·μ + k·θ` (đầu hàng vào phục vụ, hoặc một khách trước bỏ về).
- Từ `k = 0`: vào phục vụ với tốc độ `c·μ`.
- Ở mọi trạng thái: bỏ về với tốc độ `θ`.

```
SL(t) = Σ_{n<c} π_n  +  Σ_{j≥0} π_{c+j} · P(vào phục vụ trước t | bắt đầu ở trạng thái j)
```

Xác suất hấp thụ tính bằng ma trận mũ `expm(Q·t)`. Cài đặt có trong `b_theory.py` (hàm `erlang_a`).

### 7.5 Tốc độ đến đổi theo giờ: phương pháp SIPP

Coi mỗi khung giờ là một hệ ở trạng thái dừng với `λ_h` của giờ đó, tìm `c_h` nhỏ nhất thỏa SLA (dùng Erlang C hoặc Erlang-A). Đây là lịch **ban đầu**; thực tế hệ thống có quán tính (khách tồn từ giờ trước, nhân viên chỉ rời quầy khi xong việc), nên cần mô phỏng để hiệu chỉnh.

### 7.6 Hàng chung hay hàng riêng

- Hàng chung với `c` quầy: M/M/c.
- `c` hàng riêng, khách chọn ngẫu nhiên: `c` hệ M/M/1 độc lập với `λ/c`. Khi đó `P(Wq > t) = ρ · exp(−μ(1−ρ)t)`.
- Vào hàng ngắn nhất (JSQ): không có công thức đơn giản, cần mô phỏng.

Kết quả cho thấy gộp hàng đợi (pooling) cải thiện rất mạnh.

---

## 8. Giai đoạn 4: Bảng quyết định (tính tay/Excel)

### 8.1 Mẫu bảng (sản phẩm cuối của phần toán)

| Khung giờ | λ (khách/phút) | E[S] (phút) | cs² | a = λ·E[S] | c theo Erlang C | c theo Erlang-A | ρ | SL dự kiến |
|---|---|---|---|---|---|---|---|---|
| 8h | | | | | | | | |
| 9h | | | | | | | | |
| ... | | | | | | | | |

Từ bảng này suy ra **số quầy cụ thể theo từng giờ**, tổng quầy-giờ, và ca làm đề xuất.

### 8.2 Ví dụ tính tay (số MINH HỌA, không phải số liệu thật)

Giả sử `λ = 1,5 khách/phút`, `E[S] = 3 phút` nên `μ = 1/3`, `a = 4,5`. Cần `c ≥ 5`. Mục tiêu: `P(Wq ≤ 5 phút) ≥ 90%`.

**Với c = 5** (`ρ = 0,9`):

```
Σ_{k=0}^{4} 4,5ᵏ/k!           = 1 + 4,5 + 10,125 + 15,1875 + 17,0859 = 47,898
4,5⁵ / (5! · (1 − 0,9))        = 15,377 / 0,1 = 153,77
C = 153,77 / (47,898 + 153,77) = 0,7625          (76% khách phải chờ)
Wq = 0,7625 / (5/3 − 1,5)      = 4,58 phút
P(Wq ≤ 5) = 1 − 0,7625 · e^{−(1/6)·5} = 1 − 0,7625 · 0,4346 = 0,669    -> KHÔNG đạt
```

**Với c = 6** (`ρ = 0,75`):

```
Σ_{k=0}^{5} 4,5ᵏ/k!           = 47,898 + 15,377 = 63,275
4,5⁶ / (6! · (1 − 0,75))       = 11,533 / 0,25 = 46,13
C = 46,13 / (63,275 + 46,13)   = 0,4217
Wq = 0,4217 / (2 − 1,5)        = 0,84 phút
P(Wq ≤ 5) = 1 − 0,4217 · e^{−0,5·5} = 1 − 0,4217 · 0,0821 = 0,965   -> ĐẠT
```

**Kết luận ví dụ: cần 6 quầy.** Kết quả này khớp với mô phỏng SimPy (sai lệch dưới 1%), xem [mục 15](#15-kết-quả-tham-chiếu-từ-bản-chạy-thử).

### 8.3 Cổng kiểm soát trước khi viết code

- [ ] Bảng quyết định đã điền đủ các khung giờ bằng số liệu thật.
- [ ] Ít nhất một dòng được hai thành viên tính độc lập và cho cùng kết quả.
- [ ] Đơn vị thời gian thống nhất (phút) trong mọi công thức và mọi cột.
- [ ] Đã ghi rõ giả định và định nghĩa SLA.

---

## 9. Giai đoạn 5: Mô phỏng sự kiện rời rạc bằng SimPy

### 9.1 Thực thể và sự kiện

- **Khách**: có giờ đến, loại giao dịch, thời gian phục vụ, cờ VIP, độ kiên nhẫn (đều được rút ngẫu nhiên khi khách đến).
- **Tài nguyên**: `simpy.PriorityResource` với sức chứa bằng số quầy tối đa trong ngày.
- **Sự kiện**: khách đến, vào hàng, bắt đầu phục vụ, kết thúc phục vụ, bỏ về.

### 9.2 Các quyết định thiết kế quan trọng

| Vấn đề | Cách làm | Lý do |
|---|---|---|
| Tốc độ đến đổi theo giờ | Trong mỗi giờ rút khoảng cách đến theo phân phối mũ với `λ_h`; hết giờ chuyển sang tốc độ mới | Tính không nhớ của phân phối mũ làm cách này chính xác |
| Ưu tiên VIP | `PriorityResource`, VIP có mức ưu tiên cao hơn, không ngắt khách đang được phục vụ | Phản ánh thực tế |
| Khách bỏ về | Chờ đồng thời trên "được phục vụ" và "hết kiên nhẫn", cái nào đến trước thắng | Đúng mô hình Erlang-A |
| Lịch quầy đổi theo giờ | Các tiến trình "khóa quầy" giữ bớt `c_max − c_h` quầy trong giờ `h` với ưu tiên cao nhất | Nhân viên chỉ rời quầy khi xong khách đang xử lý |
| Số ngẫu nhiên chung (CRN) | Mọi giá trị ngẫu nhiên của khách được rút lúc khách đến, độc lập với trạng thái hệ thống | Khi so sánh hai lịch với cùng seed, chúng thấy đúng cùng một dãy khách, giảm phương sai |
| Điều kiện đầu | Hệ thống trống lúc mở cửa, chạy đến khi mọi khách được xử lý xong | Mô hình "kết thúc" (terminating), không cần warm-up |
| Hệ dừng (khi kiểm chứng) | Chạy dài, bỏ đoạn khởi động (warm-up) chọn bằng phương pháp Welch | Loại bỏ thiên lệch do bắt đầu từ trạng thái trống |

### 9.3 Số lần lặp và khoảng tin cậy

- Mỗi cấu hình chạy nhiều lần lặp độc lập (ví dụ 60 lần khi tìm kiếm tối ưu, 300 lần khi đánh giá cuối).
- Với mỗi chỉ số: lấy trung bình giữa các lần lặp, khoảng tin cậy 95% = `1,96 · s / √n`.
- Tiêu chí "đạt SLA" dùng **cận dưới** của khoảng tin cậy, không dùng giá trị trung bình, để chắc chắn đạt chứ không chỉ "may mắn đạt".

### 9.4 Chỉ số đo

- Mức đáp ứng `SL` (toàn ngày và theo từng giờ), `SL` của khách VIP.
- Thời gian chờ trung bình `Wq`, độ dài hàng đợi `Lq` (qua định luật Little).
- Tỉ lệ bỏ về.
- Hiệu suất sử dụng quầy.
- Tổng quầy-giờ.

---

## 10. Giai đoạn 6: Kiểm chứng mô hình

Kiểm chứng theo ba tầng, từ đơn giản đến phức tạp. Mỗi tầng so mô phỏng với lý thuyết, báo cáo sai lệch phần trăm và khoảng tin cậy.

| Tầng | Cấu hình mô phỏng | So với | Tiêu chí đạt |
|---|---|---|---|
| 1 | Poisson, phục vụ mũ, không bỏ về, không VIP | M/M/c chính xác | Lý thuyết nằm trong CI hoặc sai lệch < 2% |
| 2 | Như trên, thêm bỏ về | Erlang-A chính xác | Sai lệch < 2% |
| 3 | Phục vụ lognormal (cv khác nhau) | Allen–Cunneen (xấp xỉ) | Sai lệch nhỏ; sai lệch lớn phải giải thích được bằng giới hạn của xấp xỉ |

Lưu ý: ở tầng 3, sai lệch phản ánh cả sai số xấp xỉ của công thức lẫn nhiễu mô phỏng. Cần xem khoảng tin cậy trước khi kết luận.

**Kiểm tra ngoài mẫu:**
- Với dữ liệu giả lập: chạy lịch tối ưu trên "hệ thống thật" (tham số gốc) bằng các seed mới.
- Với dữ liệu thật: chia dữ liệu theo ngày thành tập ước lượng và tập kiểm tra. Ước lượng tham số và tối ưu lịch trên tập đầu, rồi so sánh chỉ số mô phỏng với chỉ số quan sát trên tập sau (SL, Wq, tỉ lệ bỏ về).

---

## 11. Giai đoạn 7: Tối ưu lịch quầy và phân tích độ nhạy

### 11.1 Thuật toán tối ưu dựa trên mô phỏng

1. Khởi tạo bằng lịch SIPP từ lý thuyết.
2. **Pha 1 (tăng):** chạy mô phỏng với CRN. Giờ nào vi phạm SLA (cận dưới CI95 của `SL` thường hoặc `SL` VIP dưới mục tiêu) thì tăng 1 quầy. Lặp đến khi mọi giờ đạt.
3. **Pha 2 (giảm):** thử bớt 1 quầy ở từng giờ (bắt đầu từ giờ đang nhiều quầy nhất). Giữ lại nếu toàn bộ lịch vẫn đạt SLA.
4. Đánh giá lịch cuối bằng nhiều lần lặp mới với seed khác.

### 11.2 So sánh chính sách

| Chính sách | Mô tả |
|---|---|
| Hằng số | Số quầy nhỏ nhất, giữ nguyên cả ngày, đạt SLA mọi giờ |
| SIPP | Lịch chỉ dựa trên lý thuyết |
| Tối ưu bằng mô phỏng | Lịch từ thuật toán ở 11.1 |

Báo cáo: tổng quầy-giờ, `SL` toàn ngày, `SL` giờ tệ nhất (cận dưới CI), `SL` VIP, tỉ lệ bỏ về, `Wq`, hiệu suất.

### 11.3 Phân tích độ nhạy

- Nhân tốc độ đến với các hệ số 0,9, 1,0, 1,1, 1,2, 1,3 và đánh giá lại các lịch.
- Thay đổi `E[S]` (+10%, +20%) và `cs²`.
- Kết luận về độ bền: lịch tối ưu thường "mỏng". Nên đề xuất thêm **phương án có dự phòng** (ví dụ chịu được nhu cầu tăng 10%) cùng chi phí tăng thêm bao nhiêu quầy-giờ.

---

## 12. Giai đoạn 8: Báo cáo và thuyết trình

### 12.1 Cấu trúc báo cáo (khoảng 20–25 trang)

1. Giới thiệu bài toán, mục tiêu, SLA.
2. Mô tả hệ thống, giả định, phạm vi.
3. Dữ liệu: nguồn, cách thu thập, làm sạch, thống kê mô tả.
4. Ước lượng và kiểm định phân phối.
5. Cơ sở lý thuyết: M/M/c, M/G/c, Erlang-A, SIPP.
6. Bảng quyết định và ví dụ tính tay.
7. Mô hình mô phỏng SimPy.
8. Kiểm chứng ba tầng.
9. Tối ưu lịch quầy, so sánh chính sách, độ nhạy.
10. Kết luận, khuyến nghị số quầy, hạn chế, hướng phát triển.
11. Tài liệu tham khảo, phụ lục (code, bảng số liệu).

### 12.2 Dàn ý thuyết trình (khoảng 20 phút, 14 slide)

1. Bối cảnh và mục tiêu SLA.
2. Mô tả hệ thống và những phức tạp của bài toán thực tế.
3. Dữ liệu và quá trình đến (tốc độ đổi theo giờ).
4. Phân phối thời gian phục vụ: gộp bị bác bỏ, tách loại thì khớp lognormal.
5. Ước lượng khách bỏ về bằng dữ liệu bị kiểm duyệt.
6. M/M/c và M/G/c.
7. Erlang-A và mức đáp ứng chính xác.
8. SIPP và giới hạn.
9. Bảng quyết định và ví dụ tính tay.
10. Kiến trúc mô phỏng SimPy.
11. Kiểm chứng ba tầng, warm-up.
12. Hàng chung và hàng riêng.
13. Tối ưu lịch quầy, so sánh chính sách, độ nhạy.
14. Kết luận, hạn chế, hướng phát triển, Q&A.

---

## 13. Cấu trúc mã nguồn và cách chạy

```
queue_project/
├── README.md        # tài liệu tổng quan và hướng dẫn
├── common.py        # tham số chung, cấu trúc Model, bộ sinh thời gian phục vụ, hàm CI
├── a_data.py        # [Thành viên A] đọc log, ước lượng, kiểm định, chia tập train/test
├── b_theory.py      # [Thành viên B] M/M/c, Allen-Cunneen, Erlang-A ma trận hấp thụ, SIPP
├── b_shifts.py      # [Thành viên B] Lập lịch theo ca MILP (Mô hình A & Mô hình B, HiGHS solver)
├── c_sim.py         # [Thành viên C] Động cơ mô phỏng SimPy, blocker quầy động, CRN, tối ưu lịch
├── d_experiments.py # [Cả nhóm] Kịch bản thực thi các thí nghiệm mở rộng và xuất dữ liệu
├── main.py          # Ghép nối quy trình chuẩn
├── tests/           # 18 ca kiểm thử đơn vị tự động (pytest)
├── tools/           # Công cụ kiểm tra nhất quán (check_consistency.py) và tạo bảng (build_tables.py)
├── results/final_v1/# Kết quả đóng băng đợt 1
└── results/final_v2/# Kết quả đóng băng đợt 2 (hiệu chỉnh theo yêu cầu)
```

### 13.1 Cài đặt và chạy

```bash
pip install -r requirements.txt
pytest
python main.py
python tools/build_tables.py
python tools/check_consistency.py
```

Thời gian chạy khoảng 2 phút.

### 13.2 Vai trò từng module và hàm chính

| Module | Hàm chính | Việc làm |
|---|---|---|
| `common.py` | `Model`, `mix_service`, `mix_moments`, `mean_ci` | Cấu trúc mô hình, bộ sinh phục vụ, tính cs² hỗn hợp, CI |
| `a_data.py` | `generate_log`, `fit_arrivals`, `fit_service`, `fit_patience`, `estimate_all` | Tạo log giả lập, ước lượng λ theo giờ, kiểm định Poisson, fit phân phối, ước lượng θ |
| `b_theory.py` | `mmc`, `allen_cunneen`, `mm1_random_split`, `erlang_a`, `sipp_schedule` | Công thức lý thuyết và lịch ban đầu |
| `c_sim.py` | `simulate`, `rep_stats`, `run_reps`, `feasible`, `optimize_schedule`, `simulate_separate`, `welch_curve` | Mô phỏng, thống kê theo giờ, tối ưu, so sánh hàng riêng, Welch |
| `main.py` | | Chạy 6 bước: dữ liệu, kiểm chứng, warm-up và pooling, tối ưu, đánh giá cuối, độ nhạy |

### 13.3 Hình và bảng sinh ra

- `fig_a_fit.png`: tốc độ đến theo giờ, phân phối phục vụ, Q-Q plot theo loại giao dịch.
- `fig_c_welch.png`: đường Welch chọn warm-up.
- `fig_c_pooling.png`: so sánh hàng chung và hàng riêng.
- `fig_c_lich_quay.png`: lịch quầy và SLA theo giờ.
- `fig_c_do_nhay.png`: độ nhạy theo nhu cầu.
- `ket_qua_kiem_chung.csv`, `ket_qua_hang_chung_vs_rieng.csv`, `ket_qua_danh_gia_chinh_sach.csv`, `ket_qua_do_nhay.csv`.

---

## 14. Chuyển từ dữ liệu giả lập sang dữ liệu thật

Bản code hiện tại dùng **dữ liệu giả lập** (hàm `generate_log` trong `a_data.py` chạy mô phỏng một "hệ thống thật" với các tham số `TRUE_*` trong `common.py`). Khi có dữ liệu thật, thay đổi như sau.

1. **Viết hàm đọc dữ liệu** `load_log(path)` trong `a_data.py`, trả về DataFrame có đúng các cột `day, t, hour, cls, vip, wait, served, svc` (ý nghĩa ở [mục 5.1](#51-biến-cần-ghi-cho-mỗi-khách)). Với Anonymous Bank, ánh xạ cột dựa vào tài liệu mô tả đi kèm bộ dữ liệu: giờ vào hàng, thời gian chờ, thời gian phục vụ, kết quả cuộc gọi (được phục vụ hay bỏ về). Chú ý đổi đơn vị sang **phút** nếu dữ liệu gốc tính bằng giây.
2. **Chọn khung giờ và số giờ:** sửa `HOURS`, `H_LABELS` trong `common.py` theo giờ mở cửa thực tế, và để `t` tính từ giờ mở cửa.
3. **Thay lệnh gọi trong `main.py`:** dùng `df = a_data.load_log(...)` thay cho `a_data.generate_log(...)`.
4. **Bỏ phần "hệ thống thật":** các hàm và hằng `TRUE_*`, `true_model()`, `REF_SCHEDULE` chỉ dùng cho dữ liệu giả lập. Bước "kiểm tra trên hệ thống THẬT" trong `main.py` không còn ý nghĩa, thay bằng **kiểm tra theo ngày** (ước lượng trên một số ngày, so sánh với các ngày còn lại, xem [mục 10](#10-giai-đoạn-6-kiểm-chứng-mô-hình)).
5. **Nếu dữ liệu không có loại giao dịch:** bỏ tách hai loại, fit một phân phối lognormal hoặc gamma duy nhất, dùng `lognorm_service(mean, cv)` trong `common.py`.
6. **Nếu dữ liệu không ghi nhận khách bỏ về:** đặt `theta = 0` và nêu rõ đây là hạn chế.
7. **Nếu không có VIP:** đặt `p_vip = 0` và bỏ tiêu chí VIP trong hàm `feasible`.
8. Chạy lại toàn bộ và đối chiếu bảng quyết định tính tay (mục 8) với kết quả mô phỏng.

---

## 15. Kết quả tham chiếu từ bản chạy thử

> **Lưu ý quan trọng:** các số dưới đây lấy từ **dữ liệu giả lập** (10 ngày, khoảng 7.900 bản ghi, chi nhánh mở 9 giờ, đỉnh khoảng 120 khách/giờ). Chúng dùng để minh họa quy trình và kiểm tra code, **không phải kết luận về một ngân hàng thật**. Khi có dữ liệu thật, nhóm cần thay bằng kết quả của mình.

### 15.1 Dữ liệu và ước lượng

- Tốc độ đến ước lượng sát giá trị thật. Số khách đến trong từng giờ khớp Poisson (p-value của kiểm định phân tán từ 0,05 đến 0,94).
- Giả thuyết "mọi giờ cùng tốc độ" bị bác bỏ rất mạnh, nên bắt buộc dùng mô hình theo khung giờ.
- Thời gian phục vụ gộp hai loại không khớp phân phối đơn nào (KS p ≈ 0). Tách theo loại giao dịch thì lognormal khớp tốt (KS p = 0,99 và 0,62).
- Tỉ lệ giao dịch nhanh ước lượng 0,694. Tốc độ bỏ về `θ̂ = 0,092 ± 0,008`. Thời gian phục vụ trung bình hỗn hợp 3,24 phút, `cs² = 1,11`.

### 15.2 Kiểm chứng mô phỏng và lý thuyết (hệ dừng)

| Mô hình | Chỉ số | Lý thuyết | Mô phỏng | Sai lệch |
|---|---|---|---|---|
| M/M/c | SL = P(Wq ≤ 5) | 0,9654 | 0,9664 | +0,1% |
| M/M/c | Wq (phút) | 0,8433 | 0,8385 | −0,6% |
| M/M/c | Hiệu suất ρ | 0,7500 | 0,7506 | +0,1% |
| M/M/c+M | SL (phục vụ và chờ ≤ 5) | 0,8689 | 0,8694 | +0,1% |
| M/M/c+M | Wq (phút) | 1,1444 | 1,1334 | −1,0% |
| M/M/c+M | Tỉ lệ bỏ về | 0,1144 | 0,1140 | −0,3% |
| M/G/c (cv = 0,5) | Wq theo Allen–Cunneen | 0,5271 | 0,5473 | +3,8% |
| M/G/c (cv = 1,5) | Wq theo Allen–Cunneen | 1,3704 | 1,1935 | −12,9% |

Nhận xét: tầng 1 và 2 khớp rất tốt. Tầng 3 sai lệch tăng theo `cs²`, với cv = 1,5 sai lệch −12,9% trong khi khoảng tin cậy của mô phỏng là ±8%, nên một phần là sai số xấp xỉ của công thức Allen–Cunneen.

### 15.3 Hàng chung và hàng riêng (6 quầy, 90 khách/giờ, phục vụ trung bình 3 phút)

| Cách tổ chức | P(chờ ≤ 5 phút) |
|---|---|
| Hàng chung (M/M/6), lý thuyết | 0,965 |
| 6 hàng riêng, chọn ngẫu nhiên, lý thuyết | 0,506 |
| 6 hàng riêng, chọn ngẫu nhiên, mô phỏng | 0,500 |
| 6 hàng riêng, vào hàng ngắn nhất, mô phỏng | 0,908 |

### 15.4 Lịch quầy (đánh giá 300 ngày mới, trên hệ thống "thật")

| Chính sách | Lịch (8h → 16h) | Quầy-giờ | SL toàn ngày | SL giờ tệ nhất (cận dưới CI) |
|---|---|---|---|---|
| Hằng số | 8 quầy cả ngày | 72 | 0,982 | 0,960 |
| SIPP (chỉ lý thuyết) | 4, 5, 6, 7, 6, 6, 7, 7, 4 | 52 | 0,931 | 0,880 (vi phạm) |
| Tối ưu bằng mô phỏng | 4, 5, 6, 7, 6, 6, 7, 8, 5 | 54 | 0,944 | 0,915 |

Lịch tối ưu tiết kiệm khoảng **25%** quầy-giờ so với lịch hằng số. Lịch SIPP bỏ sót hai giờ cuối vì lý thuyết bỏ qua VIP và phân phối hỗn hợp, và mô phỏng bổ sung đúng vào hai giờ đó.

### 15.5 Độ nhạy theo nhu cầu (SL của giờ tệ nhất, cận dưới CI)

| Nhu cầu | Hằng số | Tối ưu bằng mô phỏng |
|---|---|---|
| ×0,9 | 0,974 | 0,939 |
| ×1,0 | 0,957 | 0,903 |
| ×1,1 | 0,935 | 0,863 |
| ×1,2 | 0,894 | 0,793 |
| ×1,3 | 0,847 | 0,721 |

Lịch tối ưu rất sát giới hạn: nhu cầu tăng 10% là giờ tệ nhất đã xuống dưới 90%. Đây là điểm để thảo luận giữa chi phí và độ bền, và là lý do nên đề xuất thêm phương án có dự phòng.

(Giá trị ×1,0 trong bảng này dùng 150 lần lặp nên hơi khác với 0,915 ở mục 15.4 dùng 300 lần lặp; sự khác biệt đến từ nhiễu mẫu.)

---

## 16. Kế hoạch 3 tuần và phân công

### 16.1 Phân công

| | **Thành viên A: Dữ liệu và thống kê** | **Thành viên B: Lý thuyết** | **Thành viên C: Mô hình và mô phỏng** |
|---|---|---|---|
| Module | `a_data.py` | `b_theory.py` | `c_sim.py` |
| Báo cáo | Mục 3, 4 | Mục 5, 6 | Mục 7, 8, 9 |
| Slide | 3–5 | 6–9 | 10–13 |

Cả nhóm cùng làm: mục 1, 2, 10 của báo cáo, slide 1, 2, 14, `main.py`, tập thuyết trình. Việc kiểm chứng chéo: B kiểm tra mô phỏng của C, A kiểm tra công thức của B, C kiểm tra việc ước lượng của A.

### 16.2 Tuần 1 (chưa viết code mô phỏng)

- **A:** xin phép và đi khảo sát thực địa, tải và làm sạch dữ liệu Anonymous Bank (nhớ gửi thông báo cho giáo sư phụ trách dữ liệu), thống kê mô tả theo khung giờ.
- **B:** dựng bảng Excel với công thức Erlang C, Erlang-A, SIPP, tính tay ví dụ mẫu và xác nhận với một người khác.
- **C:** vẽ sơ đồ luồng khách, viết đặc tả mô hình (giả định, tham số, kịch bản, chỉ số đo), chuẩn bị khung thí nghiệm; cùng đi khảo sát thực địa.
- **Mốc cuối tuần:** hệ thống đã mô tả đầy đủ, có dữ liệu sạch, có bảng Excel tính được c theo λ và E[S] cho trước.

### 16.3 Tuần 2 (từ dữ liệu đến bảng quyết định, rồi bắt đầu code)

- **A:** ước lượng và kiểm định phân phối, chốt tham số theo khung giờ, vẽ `fig_a_fit.png`.
- **B:** điền bảng quyết định bằng số thật, đối chiếu chéo với A và C.
- **C:** sau khi bảng quyết định qua cổng kiểm soát (mục 8.3), viết code SimPy theo đặc tả và kiểm chứng ba tầng.
- **Mốc cuối tuần:** bảng quyết định hoàn chỉnh, mô phỏng khớp lý thuyết ở tầng 1 và 2.

### 16.4 Tuần 3 (tối ưu, báo cáo, thuyết trình)

- **C:** tối ưu lịch quầy, so sánh chính sách, độ nhạy.
- **A và B:** viết phần báo cáo của mình, làm slide, kiểm tra tính nhất quán số liệu.
- Cả nhóm: ghép báo cáo, tập thuyết trình ít nhất hai lần, chuẩn bị trả lời phản biện (mục 18).
- **Mốc cuối tuần:** báo cáo hoàn chỉnh, slide, mã nguồn chạy lại được bằng một lệnh.

### 16.5 Danh sách sản phẩm bàn giao

- [ ] Dữ liệu đã làm sạch (kèm mô tả nguồn).
- [ ] Bảng quyết định (Excel) và ví dụ tính tay.
- [ ] Mã nguồn chạy được bằng `python main.py`.
- [ ] Các bảng kết quả và hình.
- [ ] Báo cáo.
- [ ] Slide thuyết trình.

---

## 17. Rủi ro và cách xử lý

| Rủi ro | Cách xử lý |
|---|---|
| Không xin được dữ liệu ngân hàng | Chuyển sang trung tâm hành chính hoặc dịch vụ của trường, vẫn dùng Anonymous Bank làm dữ liệu chính |
| Dữ liệu khảo sát quá ít | Nêu rõ khoảng tin cậy rộng, dùng dữ liệu lớn để xác định dạng phân phối, dữ liệu nhỏ chỉ dùng để đối chiếu tham số |
| Dữ liệu Anonymous Bank đã cũ, bối cảnh khác (tổng đài) | Nói rõ hạn chế, dùng khảo sát tại chỗ để đối chiếu |
| Kết quả tính tay và code lệch nhau | Coi là phát hiện lỗi; kiểm tra lần lượt: đơn vị thời gian, công thức, định nghĩa SL, số lần lặp |
| KS bác bỏ mọi phân phối đơn | Tách theo loại giao dịch hoặc dùng hỗn hợp; dựa vào AIC và Q-Q plot |
| Công thức Allen–Cunneen lệch nhiều khi cs² lớn | Dùng mô phỏng làm căn cứ chính, công thức chỉ dùng để định hướng |
| Lịch tối ưu quá mỏng, không chịu được biến động | Đề xuất thêm phương án có dự phòng và nêu chi phí |
| Mô phỏng chạy chậm | Giảm số lần lặp khi tìm kiếm, tăng khi đánh giá cuối; dùng CRN |

---

## 18. Câu hỏi phản biện thường gặp

1. **Vì sao dùng khung giờ thay vì một λ chung?** Vì kiểm định cho thấy tốc độ đến khác nhau rõ rệt giữa các giờ; dùng một λ sẽ thiếu quầy ở giờ cao điểm và thừa ở giờ thấp điểm.
2. **Vì sao thời gian phục vụ không dùng phân phối mũ?** Dữ liệu gộp bị bác bỏ phân phối mũ và các phân phối đơn khác; tách theo loại giao dịch thì lognormal khớp tốt. Đây là kết quả của dữ liệu, không phải giả định.
3. **Vì sao cần mô phỏng khi đã có công thức?** Công thức chỉ chính xác cho trường hợp đơn giản (Poisson, phục vụ mũ, hệ dừng). Với VIP, lịch đổi theo giờ, phân phối hỗn hợp, cần mô phỏng; công thức dùng để kiểm chứng và làm điểm khởi đầu.
4. **Vì sao tính cả khách bỏ về vào SLA?** Khách bỏ về là khách không được phục vụ kịp, bỏ qua họ sẽ làm SLA đẹp một cách giả tạo.
5. **Vì sao dùng cận dưới của khoảng tin cậy để quyết định?** Để chắc chắn lịch đạt SLA, không phải chỉ đạt "trung bình".
6. **CRN là gì, tại sao dùng?** Dùng cùng dãy số ngẫu nhiên cho các lịch được so sánh, để chênh lệch giữa các lịch phản ánh đúng sự khác biệt của lịch chứ không phải nhiễu ngẫu nhiên.
7. **Warm-up là gì, bao giờ cần?** Cần khi nghiên cứu hệ dừng chạy dài bắt đầu từ trạng thái trống; bỏ đoạn đầu để loại thiên lệch. Mô phỏng một ngày làm việc bắt đầu từ lúc mở cửa không cần warm-up vì trạng thái trống là đúng thực tế.
8. **Vì sao hàng chung tốt hơn nhiều hàng riêng?** Hàng chung không để quầy rảnh trong khi khách đứng chờ ở hàng khác (hiệu ứng gộp hàng đợi).
9. **Kết quả có áp dụng cho ngân hàng khác được không?** Quy trình áp dụng được, còn số quầy cụ thể phụ thuộc dữ liệu của từng nơi.

---

## 19. Hướng mở rộng

- Ràng buộc ca làm (ví dụ ca tối thiểu 4 giờ) thay cho đổi quầy tùy ý từng giờ.
- Hàm chi phí: chi phí quầy cộng chi phí khách bỏ về, tìm điểm cân bằng.
- Lịch bền vững: chọn lịch vẫn đạt SLA khi nhu cầu tăng một mức cho trước.
- Quầy có kỹ năng khác nhau (một số quầy chuyên giao dịch phức tạp).
- Tốc độ đến đổi theo ngày trong tuần và đợt cuối tháng.
- Mô hình khách bỏ về không phải phân phối mũ (hàm sống sót Kaplan–Meier).
- Mô hình thông tin dự báo thời gian chờ cho khách.

---

## 20. Tài liệu tham khảo

1. Brown, L., Gans, N., Mandelbaum, A., Sakov, A., Shen, H., Zeltyn, S., Zhao, L. (2005). *Statistical Analysis of a Telephone Call Center: A Queueing-Science Perspective.* Journal of the American Statistical Association, 100(469), 36–50.
2. Technion SEE Center. *"Anonymous Bank" Call-Center Data* (tài liệu mô tả `AnonymousBank.pdf` và dữ liệu): `https://see-center.iem.technion.ac.il/databases/AnonymousBank/`. Khi sử dụng cần thông báo cho giáo sư Avi Mandelbaum và ghi nguồn.
3. Gross, D., Shortle, J., Thompson, J., Harris, C. *Fundamentals of Queueing Theory.* Wiley (Erlang C, M/M/c, M/G/c).
4. Law, A. *Simulation Modeling and Analysis.* McGraw-Hill (kiểm chứng, warm-up, phân tích đầu ra, số ngẫu nhiên chung).
5. Tài liệu SimPy: `https://simpy.readthedocs.io/`.
6. Allen, A. O. (1990). *Probability, Statistics, and Queueing Theory with Computer Science Applications.* Academic Press (xấp xỉ Allen–Cunneen).

> Ghi chú: các sách ở mục 3, 4, 6 là tài liệu kinh điển về lý thuyết hàng đợi và mô phỏng; nhóm nên kiểm tra thông tin xuất bản chính xác (năm, lần xuất bản) trước khi ghi vào báo cáo.
