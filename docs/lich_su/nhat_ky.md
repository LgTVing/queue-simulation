# Nhật ký tiến độ làm việc nhóm - Tuần 1

**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu  
**Thành viên:** A (Dữ liệu & Thống kê), B (Toán & Excel), C (Đặc tả mô hình & Khảo sát)  

---

## Ngày 1
- **A:** Đã tải bộ dữ liệu `Anonymous Bank` (tệp `September1999.txt`, dung lượng 3.19 MB) và tài liệu mô tả `AnonymousBank.pdf`; soạn email thông báo cho GS. Avi Mandelbaum; sẽ đọc kỹ cấu trúc 17 cột dữ liệu; chưa gặp trở ngại lớn.
- **B:** Đã đọc mục 7 của `README.md`; thiết lập sheet `Input` trong file `excel/erlang.xlsx`; sẽ lập công thức Erlang C cho sheet `ErlangC`; đang xem lại cách tính giai thừa lớn trong Excel để tránh tràn số.
- **C:** Đã soạn thư xin phép khảo sát thực địa (mẫu 11.2) và biểu mẫu ghi dữ liệu; liên hệ chi nhánh ngân hàng và phòng đào tạo; sẽ hoàn thiện sơ đồ luồng khách; đang chờ phản hồi cấp phép khảo sát.
- **Quyết định chung:** Thống nhất đơn vị thời gian xuyên suốt dự án là **phút**; định nghĩa SLA: $P(W_q \le 5\text{ phút}) \ge 90\%$ tính trên toàn bộ khách đến (khách bỏ về tính là không đạt); tạo cấu trúc thư mục chung (`data/raw/`, `data/clean/`, `docs/`, `excel/`).

---

## Ngày 2
- **A:** Đọc cấu trúc tệp dữ liệu thô; phát hiện các bản ghi lỗi định dạng và cuộc gọi ảo `PHANTOM`; bắt đầu viết script làm sạch `data/lam_sach.py`; sẽ trích xuất khung giờ 8h–17h và các ngày làm việc tiêu chuẩn; kẹt nhẹ ở việc xử lý thời điểm vào hàng khi `q_start = 0:00:00`.
- **B:** Cài đặt công thức Erlang C trên Excel sử dụng hàm `POISSON.DIST` để tránh lỗi tràn số do giai thừa $c!$; thiết lập các cột tính $W_q, L_q, P(W_q \le 5)$; sẽ chuẩn bị dữ liệu kiểm tra ví dụ tính tay.
- **C:** Vẽ hoàn chỉnh sơ đồ luồng khách (Mermaid diagram); xác định các thực thể (Khách, Quầy, Hàng đợi) và các sự kiện chính trong mô phỏng; thảo luận với A về các thuộc tính của khách hàng.
- **Quyết định chung:** Giải quyết thắc mắc của A: với khách được phục vụ ngay không phải chờ (`q_start = 0:00:00`), thời điểm đến được tính bằng `vru_exit` (thời điểm thoát tổng đài tự động). Chọn nghiệp vụ `PS` (giao dịch thường nhật) làm phân tích trọng tâm.

---

## Ngày 3
- **A:** Hoàn thành script `data/lam_sach.py`; xuất tệp dữ liệu sạch `data/clean/data_clean.csv` với 9.836 bản ghi trên 14 ngày làm việc chuẩn; sẽ tiến hành phân tích thống kê mô tả theo khung giờ.
- **B:** Hoàn thành ví dụ tính tay độc lập cho trường hợp $c = 5$ và $c = 6$ với $\lambda = 1.5, E[S] = 3.0$; đối chiếu với sheet `ErlangC` trong `excel/erlang.xlsx`: kết quả khớp chính xác 100% ($c=5 \to W_q = 4.58$p, $c=6 \to W_q = 0.84$p, $c_{\min} = 6$); sẽ viết tài liệu `docs/cong_thuc.md`.
- **C:** Viết chi tiết các mục 1–8 của `docs/dac_ta_mo_hinh.md` (mục đích, thực thể, sự kiện, giả định, chỉ số đo lường); bắt đầu thiết kế danh sách 6 thí nghiệm mô phỏng.
- **Quyết định chung:** Xác nhận kết quả ví dụ tính tay của B hoàn toàn chính xác. Thành viên A kiểm tra chéo công thức Excel của B và xác nhận đạt yêu cầu.

---

## Ngày 4
- **A:** Tính toán thống kê theo từng khung giờ: tính $\bar{N}_h, \lambda_h$, chỉ số phân tán $D_h$, kiểm định Poisson và kiểm định tốc độ đến đều qua các giờ ($\chi^2 = 191.69, p = 3.59 \times 10^{-37}$); sẽ ước lượng phân phối phục vụ và tốc độ bỏ về $\theta$.
- **B:** Mở rộng file `excel/erlang.xlsx`: thêm sheet `Tra_c` (bảng tra số quầy theo $\lambda$ và $E[S]$) và sheet `Allen_Cunneen` (mô hình $M/G/c$); hoàn thành bản thảo `docs/cong_thuc.md`.
- **C:** Hoàn thiện toàn bộ 11 mục của `docs/dac_ta_mo_hinh.md`; lên kế hoạch 6 thí nghiệm (T1 đến T6) cho Tuần 2 và Tuần 3; chuẩn bị kế hoạch khảo sát thực địa `docs/ke_hoach_khao_sat.md`.
- **Quyết định chung:** Kết quả kiểm định của A khẳng định tốc độ đến giữa các giờ chênh lệch rất lớn $\implies$ kiên quyết áp dụng mô hình theo khung giờ (SIPP/hourly schedule), không dùng một $\lambda$ chung.

---

## Ngày 5
- **A:** Hoàn thành ước lượng $E[S] = 2.88$ phút, $cv = 1.095, cs^2 = 1.20$, tốc độ bỏ về $\theta = 0.1123$ (kiên nhẫn TB = 8.91 phút), tỉ lệ VIP = 33.85%; xuất 2 file Excel `docs/thong_ke_mo_ta.xlsx` và `docs/bang_tham_so.xlsx`; bàn giao chính thức cho B và C.
- **B:** Nhận bảng tham số thật từ A; tạo sheet `Quyet_dinh` trong `excel/erlang.xlsx` điền đầy đủ 9 khung giờ với số liệu thực tế; xác định số quầy lý thuyết theo giờ dao động từ 4 đến 7 quầy.
- **C:** Cập nhật các tham số thực tế từ `bang_tham_so.xlsx` vào `docs/dac_ta_mo_hinh.md`; hoàn thành `docs/ke_hoach_khao_sat.md`; thiết lập kịch bản dự phòng nếu không xin được phép khảo sát ngân hàng.
- **Quyết định chung:** Mọi tham số thực tế đã được thống nhất và đồng bộ giữa các tài liệu đặc tả, bảng tính toán toán học và dữ liệu thống kê.

---

## Ngày 6
- **Họp kiểm tra chéo (60 phút):**
  - Thành viên A kiểm tra công thức và bảng tính của B: Các ô tham chiếu và công thức Erlang C chính xác, định dạng rõ ràng.
  - Thành viên B kiểm tra đặc tả của C: Các định nghĩa SLA và quy tắc chuyển ca không mâu thuẫn với lý thuyết.
  - Thành viên C kiểm tra dữ liệu và bảng tham số của A: Tệp `data_clean.csv` đúng 8 cột chuẩn, dữ liệu toàn vẹn, không có giá trị âm hoặc rác.
- **Biên bản kiểm tra chéo:** Không có lỗi mức độ "Nặng". Một số góp ý nhỏ về định dạng hiển thị phần trăm đã được B chỉnh sửa ngay trong buổi họp.

---

## Ngày 7
- **Họp tổng kết Tuần 1 và Đánh giá Cổng kiểm soát (60 phút):**
  - Cả nhóm rà soát lại 8 sản phẩm bàn giao cuối Tuần 1.
  - Soạn thảo và thông qua `docs/bao_cao_tuan_1.md`.
  - Đánh giá đạt 100% các tiêu chí của Cổng kiểm soát (Gate Control).
  - Phân chia công việc cho Tuần 2: Bắt đầu lập trình mô phỏng SimPy theo đúng đặc tả.
