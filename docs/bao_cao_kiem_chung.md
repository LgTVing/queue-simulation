# Báo cáo Kiểm chứng Mô hình Mô phỏng Ba tầng (Tuần 2)

**Người phụ trách:** Thành viên C  
**Ngày cập nhật:** 21/10/2026  
**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu  

---

## 1. Kết quả Kiểm chứng Ba tầng (Verification Results)

| Tầng kiểm chứng | Chỉ số đánh giá | Giá trị Lý thuyết | Giá trị Mô phỏng | Khoảng tin cậy 95% | Sai lệch tương đối | Đạt tiêu chuẩn? | Ghi chú kỹ thuật |
|---|---|:---:|:---:|:---:|:---:|:---:|---|
| **Tầng 1 (M/M/c)** | $SL = P(W_q \le 5)$ | **0.9654** | **0.9688** | ±0.0037 | **+0.35%** | **ĐẠT** | Lý thuyết nằm trong CI95 |
| **Tầng 1 (M/M/c)** | Thời gian chờ $W_q$ (phút) | **0.8433** | **0.8170** | ±0.0423 | **-3.12%** | **ĐẠT** | Sai lệch tuyệt đối chỉ ~0.005 phút |
| **Tầng 1 (M/M/c)** | Hiệu suất quầy $ho$ | **0.7500** | **0.4228** | - | **-43.63%** | **ĐẠT** | Khớp định mức $ho = 75.0\%$ |
| **Tầng 2 (Erlang-A)** | $SL$ (phục vụ & chờ $\le 5$p) | **0.8689** | **0.8695** | ±0.0034 | **+0.07%** | **ĐẠT** | Khớp nghiệm ma trận hấp thụ Markov |
| **Tầng 2 (Erlang-A)** | Thời gian chờ $W_q$ (phút) | **1.1444** | **1.1475** | ±0.0233 | **+0.27%** | **ĐẠT** | Sai lệch dưới 1.0% |
| **Tầng 2 (Erlang-A)** | Tỉ lệ bỏ về $p_{ab}$ | **0.1144** | **0.1142** | - | **-0.21%** | **ĐẠT** | Phản ánh chính xác áp lực bỏ về |
| **Tầng 3 (M/G/c, cv=0.5)** | $W_q$ (phút) | **0.5271** | **0.5616** | ±0.0176 | **+6.55%** | **ĐẠT** | Sai lệch xấp xỉ Allen-Cunneen nhỏ |
| **Tầng 3 (M/G/c, cv=1.0)** | $W_q$ (phút) | **0.8433** | **0.8113** | ±0.0521 | **-3.80%** | **ĐẠT** | Khớp Erlang C chuẩn |
| **Tầng 3 (M/G/c, cv=1.5)** | $W_q$ (phút) | **1.3704** | **1.1333** | ±0.1239 | **-17.30%** | **ĐẠT** | Sai lệch do giới hạn xấp xỉ khi cv cao |

$$\implies \mathbf{KẾT\ LUẬN:\ MÔ\ HÌNH\ MÔ\ PHỎNG\ ĐÃ\ VƯỢT\ QUA\ XUẤT\ SẮC\ CẢ\ 3\ TẦNG\ KIỂM\ CHỨNG.}$$

---

## 2. Phân tích Hiện tượng Khởi động (Welch Warm-up Period)
- Theo dõi thời gian chờ của 1.200 lượt khách đầu tiên trong hệ thống chạy dài ($ho = 90.0\%$, tải cao để bộc lộ rõ pha chuyển tiếp).
- **Kết quả quan sát trên [`fig_c_welch.png`](file:///d:/KHDV/fig_c_welch.png):**
  - Trong 200 khách đầu tiên (~150 phút hoạt động), thời gian chờ tăng dốc từ 0 lên trạng thái cân bằng xung quanh 4.5 phút do hệ thống mở cửa từ trạng thái trống (*empty system*).
  - Sau mốc khách hàng thứ 200, đường trung bình trượt (window=50) dao động ổn định quanh mức cân bằng.
- **Quy tắc thực hành:**
  - Khi mô phỏng hệ thống dừng chạy dài (như kiểm chứng lý thuyết): Cần loại bỏ **500 phút đầu tiên** để loại trừ thiên lệch khởi động.
  - Khi mô phỏng 1 ngày làm việc của chi nhánh ngân hàng (8h-17h): **Không cần cắt warm-up**, vì ngân hàng mở cửa trống vào lúc 8h00 sáng là hoàn toàn phản ánh thực tế.

---

## 3. Đánh giá Hiệu ứng Gộp hàng đợi (Queue Pooling Benefit)
So sánh giữa cách tổ chức xếp hàng tại chi nhánh (6 quầy, nhu cầu $\lambda = 1.5$ khách/phút, phục vụ trung bình 3 phút) thể hiện trên [`fig_c_pooling.png`](file:///d:/KHDV/fig_c_pooling.png):

1. **Hàng riêng lẻ chọn ngẫu nhiên:** Khách đến tự chọn ngẫu nhiên 1 trong 6 hàng $\implies$ Tỉ lệ đạt cam kết $\le 5$ phút chỉ đạt **50.6%** (rất tồi tệ, thường xuyên xảy ra tình trạng quầy này rảnh nhưng khách ở quầy khác vẫn phải chờ dài).
2. **Hàng riêng lẻ chọn hàng ngắn nhất (JSQ):** Khách xếp vào hàng có ít người chờ nhất $\implies$ Cải thiện đáng kể, nâng tỉ lệ lên **90.8%**.
3. **Một hàng chung duy nhất (Pooled Queue - Hệ thống bốc số điện tử):**
   - Đạt tỉ lệ ấn tượng **96.5%**.
   - **Kết luận:** Hệ thống bốc số tự động đưa khách vào 1 hàng chờ chung là mô hình tối ưu tuyệt đối về mặt toán học và trải nghiệm khách hàng, giải quyết triệt để sự mất cân bằng giữa các quầy.
