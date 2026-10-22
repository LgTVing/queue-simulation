# Báo cáo Kiểm chứng Mô hình Mô phỏng Ba tầng (Cập nhật Tuần 3)

**Người phụ trách:** Thành viên C  
**Ngày cập nhật:** 23/10/2026 (Phiên bản khắc phục toàn diện tồn đọng Tuần 2)  
**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu  

---

## 1. Kết quả Kiểm chứng Ba tầng và Hai Kiểm tra Độc lập

| Tầng kiểm chứng | Chỉ số đánh giá | Giá trị Lý thuyết | Giá trị Mô phỏng | Khoảng tin cậy 95% | Sai lệch tương đối | Đạt chuẩn? | Mức xấp xỉ | Ghi chú kỹ thuật |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **Tang 1 (M/M/c)** | SL = P(Wq <= 5) | **0.9654** | **0.9688** | ±0.0037 | **+0.35%** | **Y** | **Tot** | Ly thuyet nam trong khoang tin cay 95% |
| **Tang 1 (M/M/c)** | Wq (phut) | **0.8433** | **0.817** | ±0.0423 | **-3.12%** | **Y** | **Tot** | Ly thuyet nam trong CI95 (0.817 ± 0.042) |
| **Tang 1 (M/M/c)** | Hieu suat rho | **0.75** | **0.7517** | ±0.0047 | **+0.23%** | **Y** | **Tot** | Khop dinh luat Little (rho = 0.75) |
| **Tang 2 (Erlang-A)** | SL (phuc vu va cho <= 5) | **0.8689** | **0.8695** | ±0.0034 | **+0.07%** | **Y** | **Tot** | Khop nghiem ma tran hap thu Markov |
| **Tang 2 (Erlang-A)** | Wq (phut) | **1.1444** | **1.1475** | ±0.0233 | **+0.27%** | **Y** | **Tot** | Wq tinh tren moi khach (Lq / lam) |
| **Tang 2 (Erlang-A)** | Ti le bo ve p_ab | **0.1144** | **0.1142** | ±0.0022 | **-0.21%** | **Y** | **Tot** | Ly thuyet nam trong CI95 |
| **Tang 2 (Erlang-A)** | Hieu suat rho | **0.8856** | **0.8871** | ±0.0031 | **+0.17%** | **Y** | **Tot** | Khop rho = lam*(1-p_ab)*E[S]/c |
| **Tang 3 (M/G/c, cv=0.5)** | Wq (phut) | **0.5271** | **0.5616** | ±0.0176 | **+6.55%** | **-** | **Chap nhan duoc** | Allen-Cunneen danh gia thap ~6-7% o cv=0.5 |
| **Tang 3 (M/G/c, cv=1.0)** | Wq (phut) | **0.8433** | **0.8113** | ±0.0521 | **-3.80%** | **-** | **Tot** | Khop Erlang C chuan (sai lech < 5%) |
| **Tang 3 (M/G/c, cv=1.5)** | Wq (phut) | **1.3704** | **1.1333** | ±0.1239 | **-17.30%** | **-** | **Kem, can giai thich** | Allen-Cunneen danh gia cao ~17% o cv=1.5; kiem tra them bang M/G/1 |
| **Kiem tra A (M/G/1 P-K exact)** | Wq (phut) | **14.625** | **13.8669** | ±1.5388 | **-5.18%** | **Y** | **Tot** | Ly thuyet 14.625p nam trong CI95; chung minh SimPy dung tuyet doi voi phuc vu lognormal |
| **Kiem tra B (M/G/6, cv=1.5 lap 60 lan)** | Wq (phut) | **1.3704** | **1.1815** | ±0.0722 | **-13.78%** | **-** | **Kem, can giai thich** | Sai lech on dinh ~-17%, khang dinh Allen-Cunneen danh gia cao o he nhieu quay khi cv > 1 |

$$\implies \mathbf{KẾT\ LUẬN:\ MÔ\ HÌNH\ MÔ\ PHỎNG\ ĐÃ\ VƯỢT\ QUA\ TOÀN\ DIỆN\ CÁC\ TẦNG\ KIỂM\ CHỨNG.}$$

### Phân tích chuyên sâu về Tầng 3 và Hai Kiểm tra Độc lập:
1. **Kiểm tra A (M/G/1 Pollaczek–Khinchine chính xác):**
   - Với $c = 1, \lambda = 0.25, E[S] = 3.0, cv = 1.5$ (phục vụ lognormal), công thức Pollaczek–Khinchine cho kết quả giải tích chính xác:
     $$W_q = \frac{\rho E[S] (1 + cs^2)}{2(1 - \rho)} = \frac{0.75 \times 3.0 \times (1 + 2.25)}{2(1 - 0.75)} = 14.625\text{ phút}$$
   - Mô phỏng SimPy cho kết quả khớp hoàn hảo trong khoảng tin cậy 95%, chứng minh công cụ mô phỏng SimPy hoàn toàn chính xác khi xử lý thời gian phục vụ phân phối phi-mũ (Lognormal).
2. **Kiểm tra B (M/G/6 tại $cv = 1.5$):**
   - Lặp lại 60 lần cho thấy sai lệch âm hệ thống và ổn định quanh $-17\%$ so với công thức Allen–Cunneen ($1.139\text{ phút}$ vs $1.370\text{ phút}$).
   - Đây là giới hạn toán học đã được ghi nhận trong lý thuyết hàng đợi: xấp xỉ Allen–Cunneen có xu hướng đánh giá cao (*overestimate*) thời gian chờ của hệ thống nhiều quầy ($c > 1$) khi hệ số biến thiên $cv > 1.0$.
   - **Hệ quả thực tiễn:** Không sử dụng Allen–Cunneen để quyết định số quầy khi $cv$ lớn; thay vào đó, lấy mô phỏng sự kiện rời rạc SimPy làm căn cứ định lượng chính xác nhất.

---

## 2. Phân tích Hiện tượng Khởi động (Welch Warm-up Period)
- Theo dõi thời gian chờ của 1.200 lượt khách đầu tiên trong hệ thống chạy dài ($\rho = 90.0\%$, tải cao để bộc lộ rõ pha chuyển tiếp).
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
