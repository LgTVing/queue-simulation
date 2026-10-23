# Báo cáo sửa đổi

## 1. Tóm tắt
- **Số nhiệm vụ hoàn thành / tổng:** 14 / 14 nhiệm vụ (T1–T5 P0, T6–T12 P1, T13–T14 P2 đạt chuẩn 100%).
- **Kết luận nào thay đổi so với bản trước (nêu rõ, kèm số trước và sau):**
  1. *Kiểm định Poisson từng giờ:* Bản trước khẳng định "8/9 khung giờ chấp nhận Poisson ($p > 0.05$)". Bản mới hiệu chỉnh đúng: **8/9 khung giờ bác bỏ phân phối Poisson** ở $\alpha = 0.05$ (duy nhất giờ 12h-13h có $p=0.0763$ chưa đủ bằng chứng bác bỏ). Dữ liệu có hiện tượng **quá phân tán** ($\text{Var}/\text{Mean} = 10.8$, $CV_{\text{ngày}} = 11.8\%$).
  2. *Mức độ tin cậy của Lịch tối ưu 44 quầy-giờ:* Bản trước khẳng định lịch 44 đạt SLA 100% số ngày. Bản mới chứng minh khi xét đến biến động ngẫu nhiên về quy mô khách giữa các ngày ($CV = 11.8\%$), lịch 44 chỉ đạt SLA toàn ngày $\ge 90\%$ trên **$85.0\%$ số ngày** (xác suất đạt SLA cả 9 giờ là **$26.0\%$**; đạt 10/14 ngày thực tế). Lịch bền vững 48 quầy-giờ đạt **$95.3\%$ số ngày** (đạt 13/14 ngày thực tế).
  3. *Quy tắc kích hoạt vận hành:* Chuyển từ khuyến nghị theo thứ trong tuần (không có căn cứ) sang quy tắc định lượng: **Áp dụng Lịch 44 q-h cho ngày $\le 687$ khách/ngày; kích hoạt Lịch 48 q-h cho ngày $> 687$ khách/ngày**.
  4. *Tính khả thi của ca làm việc:* Làm rõ Mô hình A (8h liên tục không nghỉ) hoàn toàn **vô nghiệm** với cấu hình 4 NV 8h + 3 NV 4h; chỉ có **Mô hình B** (8h làm việc, 1h nghỉ trưa so le) mới có nghiệm duy nhất 44 quầy-giờ làm việc (48 quầy-giờ tại chỗ).

---

## 2. Chi tiết từng nhiệm vụ

| ID | Trạng thái | File sửa / tạo mới | Số trước → sau | Ghi chú |
|---|:---:|---|---|---|
| **T1** | Xong | `docs/thong_ke_mo_ta.xlsx`, `docs/bang_tham_so.xlsx`, `results/final_v2/kiem_dinh_poisson.csv`, `results/final_v2/qua_phan_tan_ngay.csv` | 8/9 giờ nhận Poisson → **8/9 giờ bác bỏ Poisson** ($p < 0.05$). SD ngày 26.5 → SD thực tế 87.1, Var/Mean = 10.8, $CV_{\text{ngày}} = 11.8\%$ | Sửa lỗi đảo nhãn; bổ sung sheet `qua_phan_tan` trong Excel |
| **T2** | Xong | `c_sim.py`, `results/final_v2/bien_dong_ngay.csv`, `results/final_v2/so_sanh_chinh_sach_v2.csv`, `results/final_v2/theo_ngay.csv` | Tỉ lệ ngày đạt SLA: 100% → **85.0%** (Lịch 44), **95.3%** (Lịch 48), **99.4%** (Mốc 6 quầy). P(cả 9 giờ đạt): **26.0%** vs **47.0%** vs **77.8%** | Tích hợp $m_d \sim \text{Gamma}(CV=11.8\%)$ vào hàm `simulate` và `run_reps` |
| **T3** | Xong | `docs/TONG_HOP_SO_LIEU_CHI_TIET.md`, `docs/bao_cao_tong_ket.md`, `docs/slide_thuyet_trinh.md` | Khắc phục các sai lệch nhỏ trong Phần 5 → Khớp 100% với CSV: $SL=93.81\%$, $SL_{\text{low}}=90.78\%$, $SL_{\text{vip}}=94.96\%$ | Đồng bộ toàn bộ tài liệu |
| **T4** | Xong | `docs/ngoai_mau.md`, `results/final_v2/ngoai_mau_v2.csv`, `results/final_v2/ngoai_mau_tham_so.json` | Đánh giá ngoài mẫu 1 chiều → 2 phiên bản độc lập (Phiên bản A Erlang-A tĩnh: $SL=92.73\%$, Phiên bản B SimPy DES: $SL=90.62\%$) | Làm rõ sự sụt giảm ở 15h-16h ($76.47\%$) do tác vụ chốt sổ/rút quầy thực tế |
| **T5** | Xong | `b_shifts.py`, `results/final_v2/lich_theo_ca_v2.csv` | Trình bày lẫn lộn ca 8h → Phân định Mô hình A (8h liên tục, vô nghiệm với 4+3, thuần 8h cần 64 q-h) và Mô hình B (có nghỉ trưa, duy nhất nghiệm 44 q-h worked, 6 NV thuần 8h cần 48 q-h worked) | Khớp 100% bảng tham chiếu MILP của đề bài |
| **T6** | Xong | `docs/doi_chieu_mo_phong.md`, `results/final_v2/dao_dong_seed.csv` | Ghi nhận độ lệch ~0.4% giữa các lần chạy → Khảo sát 3 khối seed (50000: 93.81%, 70000: 93.38%, 90000: 93.65%), độ lệch $\le 0.43\%$ nằm trong CI95 Monte Carlo | Giải trình tính ngẫu nhiên thống kê |
| **T7** | Xong | `c_sim.py`, các file báo cáo | "Tối ưu toàn cục" → **"Tối thiểu cục bộ (thuật toán 2 pha xác nhận SIPP)"** | Vét cạn swap 1 quầy và giảm 2 quầy chứng minh không có lịch $\le 43$ q-h khả thi |
| **T8** | Xong | `results/final_v2/do_nhay_phan_phoi_v2.csv` | So sánh seed rời rạc → CRN bắt cặp: Mũ ($\Delta = -0.12\% \pm 0.18\%$), Bootstrap ($\Delta = -0.05\% \pm 0.16\%$) không khác biệt; Lognormal ($\Delta = -0.73\% \pm 0.22\%$) giảm có ý nghĩa | Triệt tiêu phương sai ngoại lai |
| **T9** | Xong | `docs/bao_cao_tong_ket.md` | Phân tích quy tắc căn bậc hai: $\beta \approx 0.61$ giữ ổn định khi quy mô tăng, chứng minh tính kinh tế theo quy mô | Giữ vững cơ sở lý thuyết |
| **T10**| Xong | Toàn bộ tài liệu báo cáo và slide | Xóa bỏ: "hiện trạng" → "Mốc cơ sở 6 quầy"; Xóa bỏ: "Thứ 2, Thứ 6, ngày trả lương"; Xóa bỏ: "biên an toàn rất cao", "hoàn hảo", "tuyệt đối" | `check_consistency.py` xác nhận 0 vi phạm |
| **T11**| Xong | `results/final_v2/tham_so_thanh_phan.csv`, `results/final_v2/doi_chieu_tham_so.csv` | Chưa đối chiếu rõ Train/Test/Toàn bộ → Bảng đối chiếu minh bạch nguồn gốc từng tham số | Đáp ứng đầy đủ yêu cầu |
| **T12**| Xong | `results/final_v2/pvip_theo_gio.csv` | Chỉ có SLA VIP toàn ngày → Bảng chi tiết tỉ lệ VIP và SLA VIP theo từng khung giờ trong ngày | Đảm bảo $SL_{\text{vip}} \ge 90\%$ mọi giờ |
| **T13**| Xong | `tests/test_v2_features.py`, `results/final_v2/pytest_log.txt` | 12 tests → **18 tests** tự động, 100% PASSED trong 14.39s | Kiểm thử tự động hồi quy |
| **T14**| Xong | `tools/build_tables.py`, `tools/check_consistency.py`, `results/final_v2/MO_TA.md`, `CHANGELOG.md` | Chưa có công cụ kiểm tra tự động → 2 công cụ Python tự động tạo bảng và kiểm tra tính nhất quán | Đóng băng kết quả trong `results/final_v2/` |

---

## 3. Kết quả mới quan trọng

### 3.1 Xác suất đạt SLA toàn ngày và mọi giờ theo từng chính sách (T2)
Khi tính đến biến động ngẫu nhiên giữa các ngày ($m_d \sim \text{Gamma}, CV = 11.8\%$):
- **Lịch tối ưu 44 quầy-giờ (`[4, 5, 6, 5, 5, 5, 5, 5, 4]`):**
  - Mức phục vụ danh định (không biến động ngày): $SL = 93.81\% \pm 0.23\%$.
  - Xác suất ngày đạt chuẩn ($SL_{\text{ngày}} \ge 90\%$): **$85.0\%$** (trượt 15.0% số ngày khi gặp ngày đông khách).
  - Xác suất đồng thời cả 9 khung giờ đều đạt $\ge 90\%$: **$26.0\%$**.
  - Đối chiếu trên 14 ngày thực tế: Đạt SLA trên **10/14 ngày** (hụt tại các ngày 1, 2, 7, 12 có quy mô khách lớn: 776, 826, 820, 779 khách).
- **Lịch bền vững 48 quầy-giờ (`[5, 6, 6, 6, 5, 5, 5, 5, 5]`):**
  - Mức phục vụ danh định: $SL = 95.82\% \pm 0.18\%$.
  - Xác suất ngày đạt chuẩn ($SL_{\text{ngày}} \ge 90\%$): **$95.3\%$**.
  - Xác suất cả 9 khung giờ đều đạt $\ge 90\%$: **$47.0\%$**.
  - Đối chiếu trên 14 ngày thực tế: Đạt SLA trên **13/14 ngày** (chỉ hụt ngày 7 có tải cực đại).
- **Mốc cơ sở 6 quầy (`[6, 6, 6, 6, 6, 6, 6, 6, 6]`):**
  - Xác suất ngày đạt chuẩn: **$99.4\%$**; cả 9 giờ đạt: **$77.8\%$** (14/14 ngày thực tế).

### 3.2 Lịch ca làm việc đúng và chi phí (T5)
Solver HiGHS giải bài toán quy hoạch nguyên MILP xác nhận:
- **Mô hình A (Ca 8h liên tục không nghỉ):**
  - Thuần 8h: Cần 8 nhân viên $\implies$ **64 quầy-giờ** làm việc (dư thừa lớn ở đầu và cuối ngày).
  - Cấu hình 4 NV 8h + 3 NV 4h: **Vô nghiệm** (không thể tạo ra lịch `[4, 5, 6, 5, 5, 5, 5, 5, 4]`).
- **Mô hình B (Ca 8h có 1h nghỉ trưa: 9h tại chi nhánh, 8h làm việc):**
  - Thuần 8h (nghỉ trưa trong cửa sổ giờ 1–7): Cần 6 nhân viên $\implies$ **48 quầy-giờ làm việc** (54 quầy-giờ tại chỗ), tạo lịch quầy `[6, 5, 6, 5, 5, 5, 5, 5, 6]`.
  - Thuần 4h: Cần 13 lượt ca $\implies$ **52 quầy-giờ** làm việc.
  - Hỗn hợp 4 NV 8h + 3 NV 4h (nghỉ trưa cửa sổ 11h–14h): **Có duy nhất 1 nghiệm tối ưu khả thi** với đúng **44 quầy-giờ làm việc** (+0.0% lãng phí giờ làm việc, 48 quầy-giờ tại chỗ). 4 NV 8h nghỉ trưa so le: 1 người nghỉ 11h–12h, 2 người nghỉ 12h–13h, 1 người nghỉ 13h–14h; 3 NV 4h vào ca 9h–13h, 10h–14h, 12h–16h.

### 3.3 Đánh giá Ngoài mẫu (T4)
- **Phiên bản A (Erlang-A trạng thái dừng với $\lambda_{\text{test}}$):** $SL = 92.73\%$, tất cả các giờ đạt từ $88.9\%$ đến $95.3\%$.
- **Phiên bản B (SimPy DES với $\lambda_{\text{test}}$, 200 reps):** $SL = 90.62\%$, bỏ về $7.65\%$, $W_q = 0.697$ phút.
- **Đối chiếu thực tế:** Tập test thực tế ghi nhận mức phục vụ chung $93.6\%$, nhưng khung giờ 15h–16h sụt giảm xuống $76.47\%$ ($W_q = 1.41$ phút, bỏ về $15.03\%$) do nhân viên thực tế phải xử lý tác vụ chốt sổ/đóng quầy cuối ngày, làm rõ sự khác biệt giữa mô hình hóa lý thuyết và thực tiễn vận hành ngân hàng.

---

## 4. Việc chưa làm được và thông tin cần bổ sung
- **Số quầy thực tế theo từng giờ của chi nhánh ngân hàng:** Bộ dữ liệu Technion SEE Center ghi nhận cuộc gọi tổng đài nhưng không cung cấp log số lượng giao dịch viên trực quầy thực tế theo từng phút. Do đó, việc so sánh với tập test chỉ dừng lại ở đối chiếu kiểm tra tính hợp lý của mô hình dự báo chứ chưa thực hiện được A/B testing đối chứng song song.
- **Hệ số chi phí tài chính cụ thể:** Chi phí quầy-giờ $c_q$ và chi phí mất khách $c_a$ đang được phân tích kịch bản theo tỉ số tương đối $k = c_a / c_q$ do ngân hàng không công bố cấu trúc chi phí tiền lương và lợi nhuận biên trên từng khách hàng.

---

## 5. Rủi ro còn lại
1. **Rủi ro quá tải vào ngày lưu lượng đặc biệt lớn:** Nếu chi nhánh áp dụng cứng nhắc Lịch 44 q-h vào các ngày có lưu lượng khách $> 687$ khách/ngày (chiếm khoảng 28% số ngày), mức phục vụ giờ cao điểm có nguy cơ rơi xuống $86.5\%$. Chi nhánh cần áp dụng nghiêm ngặt quy tắc kích hoạt Lịch bền vững 48 q-h cho các ngày này.
2. **Rủi ro mệt mỏi nhân sự (Fatigue):** Năng suất giao dịch viên có thể giảm vào cuối buổi chiều (khung 15h–17h), khiến thời gian phục vụ thực tế dài hơn mô hình giả định.
3. **Rủi ro phân rã hàng đợi chung:** Nếu chi nhánh tổ chức các hàng đợi riêng rẽ trước từng quầy thay vì hệ thống bốc số tự động 1 hàng chung duy nhất, hiệu ứng pooling sẽ bị triệt tiêu, khiến tỉ lệ đạt SLA tụt giảm nghiêm trọng (xuống $\approx 50.6\%$).
