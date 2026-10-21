# Báo cáo Tiến độ Tuần 1

**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu  
**Thời gian thực hiện:** Tuần 1 (Từ Ngày 1 đến Ngày 7)  
**Nhóm thực hiện:** 3 sinh viên (Thành viên A, B, C)  

---

## 1. Mục tiêu Tuần 1
- **Nguyên tắc xuyên suốt:** Chưa viết code mô phỏng; tập trung chuẩn bị nền tảng dữ liệu thực nghiệm, tính toán giải tích bằng Excel và xây dựng bản đặc tả mô hình hoàn chỉnh.
- **Sản phẩm trọng tâm:** Tệp dữ liệu sạch chuẩn hóa, bảng tính toán Erlang C trên Excel có kiểm chứng bằng tính tay, và đặc tả mô hình mô phỏng SimPy để sẵn sàng triển khai code ở Tuần 2.

---

## 2. Kết quả thực hiện theo từng thành viên

| Thành viên | Nhiệm vụ đảm nhiệm | Sản phẩm hoàn thành | Trạng thái |
|---|---|---|:---:|
| **A (Dữ liệu & Thống kê)** | Tải, làm sạch dữ liệu `Anonymous Bank`, kiểm định phân phối | `data/clean/data_clean.csv`, `data/lam_sach.py`, `docs/mo_ta_du_lieu.md`, `docs/thong_ke_mo_ta.xlsx`, `docs/bang_tham_so.xlsx` | **Hoàn thành 100%** |
| **B (Toán học & Excel)** | Lập bảng tính Erlang C, chứng minh công thức, tính tay đối chứng | `excel/erlang.xlsx` (5 sheets), `docs/cong_thuc.md` | **Hoàn thành 100%** |
| **C (Đặc tả & Khảo sát)** | Soạn đặc tả 11 mục, vẽ sơ đồ luồng, lập kế hoạch khảo sát thực tế | `docs/dac_ta_mo_hinh.md`, `docs/ke_hoach_khao_sat.md`, `docs/nhat_ky.md` | **Hoàn thành 100%** |
| **Cả nhóm** | Kiểm tra chéo, đánh giá cổng kiểm soát, báo cáo tuần | `docs/bao_cao_tuan_1.md`, họp mở đầu và tổng kết | **Hoàn thành 100%** |

---

## 3. Các số liệu thực nghiệm chính đã xác lập

- **Quy mô mẫu dữ liệu sạch:** 9.836 lượt giao dịch trên 14 ngày làm việc tiêu chuẩn (trung bình 702.6 khách/ngày, ~78 khách/giờ).
- **Tốc độ đến theo giờ ($\lambda_h$):**
  - Dao động từ **$1.019$ khách/phút** (đầu giờ 8h-9h) đến đỉnh cao điểm **$1.644$ khách/phút** (10h-11h).
  - Kiểm định tốc độ đến đồng nhất qua các giờ: $\chi^2 = 191.69, p = 3.59 \times 10^{-37} \implies$ Bác bỏ giả thuyết tốc độ đến không đổi; bắt buộc áp dụng mô hình theo khung giờ (SIPP).
- **Thời gian phục vụ:** Trung bình $E[S] = 2.88$ phút ($\sigma_S = 3.15$ phút, hệ số biến thiên $cv = 1.095, cs^2 = 1.20$). Phân phối Gamma/Lognormal khớp tốt hơn phân phối mũ.
- **Tốc độ bỏ về ($\theta$):** $\hat{\theta} = 0.1123$ (1/phút) $\implies$ Thời gian kiên nhẫn trung bình của khách là **$8.91$ phút**. Tỉ lệ bỏ về trung bình toàn ngày là $7.15\%$.
- **Tỉ lệ khách ưu tiên / VIP:** $33.85\%$.
- **Kết quả kiểm chứng ví dụ mẫu ($M/M/c$ với $\lambda = 1.5, E[S] = 3.0$):**
  - $c = 5$ quầy: $\rho = 90.0\%, W_q = 4.58$ phút, $P(W_q \le 5\text{p}) = 66.9\% \implies$ **Không đạt SLA**.
  - $c = 6$ quầy: $\rho = 75.0\%, W_q = 0.84$ phút, $P(W_q \le 5\text{p}) = 96.5\% \implies$ **Đạt SLA**.
  - Số quầy tối thiểu: **$c_{\min} = 6$ quầy** (Khớp tuyệt đối giữa Excel, Python và tính tay).

---

## 4. Vấn đề phát sinh và giải pháp xử lý

1. **Tràn số trong Excel khi tính giai thừa $c!$:** Thành viên B đã chuyển đổi công thức Erlang C sang hàm mật độ tích lũy `POISSON.DIST`, triệt tiêu thừa số $e^{-a}$ ở cả tử và mẫu.
2. **Khách hàng không vào hàng đợi tổng đài:** Các bản ghi cúp máy ngay trong lời chào tự động (`q_start = 0:00:00`) được Thành viên A lọc bỏ để đảm bảo chỉ giữ lại đúng đối tượng khách thực sự bước vào sảnh chờ.
3. **Thủ tục xin cấp phép ngân hàng phức tạp:** Kế hoạch khảo sát đã chuẩn bị sẵn kịch bản dự phòng: tập trung 100% vào bộ dữ liệu chuẩn `Anonymous Bank` làm dữ liệu định lượng chính, và tổ chức 1 buổi khảo sát tại bộ phận một cửa/căng tin trường để đối chiếu thực tế Việt Nam.

---

## 5. Đánh giá Cổng kiểm soát Tuần 1 (Gate Control)

| Hạng mục kiểm soát | Tiêu chí đánh giá | Kết quả |
|---|---|:---:|
| **Dữ liệu** | Tệp dữ liệu sạch đúng định dạng 8 cột, có script tái lập được, có bảng tham số | **ĐẠT** |
| **Toán học** | Bảng Excel Erlang C khớp ví dụ tính tay $c=5$ và $c=6$, có bảng quyết định SIPP | **ĐẠT** |
| **Đặc tả** | Bản đặc tả đủ 11 mục, có sơ đồ luồng Mermaid, danh sách thí nghiệm T1-T6 | **ĐẠT** |
| **Quản trị** | Biên bản kiểm tra chéo hoàn tất, không còn lỗi mức nặng | **ĐẠT** |

$$\implies \mathbf{KẾT\ LUẬN:\ ĐỦ\ ĐIỀU\ KIỆN\ VƯỢT\ QUA\ CỔNG\ KIỂM\ SOÁT\ ĐỂ\ BƯỚC\ VÀO\ TUẦN\ 2.}$$

---

## 6. Kế hoạch trọng tâm Tuần 2
1. **Thành viên A:** Hoàn thiện module `a_data.py` (hàm đọc dữ liệu sạch, tự động hóa kiểm định và trực quan hóa phân phối).
2. **Thành viên B:** Lập trình module `b_theory.py` (tính giải tích $M/M/c$, Erlang-A ma trận mũ hấp thụ, xấp xỉ Allen-Cunneen và lịch ban đầu SIPP).
3. **Thành viên C:** Xây dựng mô hình mô phỏng SimPy trong `c_sim.py` và tiến hành Kiểm chứng ba tầng (Tầng 1: $M/M/c$, Tầng 2: Erlang-A, Tầng 3: $M/G/c$).
4. **Cả nhóm:** Ghép nối pipeline trong `main.py` và kiểm tra sai lệch mô phỏng so với lý thuyết (mục tiêu sai lệch $< 2\%$).
