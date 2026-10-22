# Biên Bản Đóng Băng Dữ Liệu và Kết Quả Dự Án (results/final_v1/)

**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu  
**Phiên bản đóng băng:** `final_v1`  
**Ngày đóng băng:** 23/10/2026  
**Người tổng hợp:** Thành viên C (Đại diện nhóm nghiên cứu)  
**Môi trường thực thi:** Python 3.13, SimPy 4.1, SciPy 1.15, NumPy 2.2, Pandas 2.2  

---

## 1. Danh mục các tệp số liệu đóng băng

| Tên tệp | Nội dung tệp | Người phụ trách | Số lần lặp | Ghi chú kỹ thuật |
|---|---|:---:|:---:|---|
| [`params.json`](file:///d:/KHDV/results/final_v1/params.json) | Bộ tham số gốc ước lượng từ tập train (10 ngày) | Thành viên A | - | Phân phối Gamma ($E[S]=2.9236$, shape=1.0955, scale=2.6688) |
| [`kiem_chung.csv`](file:///d:/KHDV/results/final_v1/kiem_chung.csv) | Kết quả kiểm chứng mô phỏng 3 tầng và 2 kiểm tra độc lập | Thành viên C | 30–60 reps | Khớp Little $\rho = 0.75$, M/G/1 P-K exact $14.625$p |
| [`lich_toi_uu.csv`](file:///d:/KHDV/results/final_v1/lich_toi_uu.csv) | Toàn bộ lịch sử thuật toán tối ưu 2 pha (Ramp-up & Pruning) | Thành viên C | 60 reps | Hội tụ tại lịch `[4, 5, 6, 5, 5, 5, 5, 5, 4]` (44 q-h) |
| [`so_sanh_chinh_sach.csv`](file:///d:/KHDV/results/final_v1/so_sanh_chinh_sach.csv) | Bảng so sánh 5 chính sách phục vụ với các chỉ số đo | Thành viên C | 300 reps | Seed độc lập mới (`seed_base=50000`), có CI95 đầy đủ |
| [`do_nhay.csv`](file:///d:/KHDV/results/final_v1/do_nhay.csv) | Phân tích độ nhạy theo Nhu cầu, $E[S]$, $\theta$ | Thành viên C | 150 reps | Kỹ thuật số ngẫu nhiên chung (CRN) |
| [`chi_phi.csv`](file:///d:/KHDV/results/final_v1/chi_phi.csv) | Đánh đổi chi phí quầy-giờ và khách bỏ về ($k \in \{0.1, 0.25, 0.5, 1, 2\}$) | Thành viên B | 300 reps | Phân tích kịch bản chi phí mất khách |
| [`lich_theo_ca.csv`](file:///d:/KHDV/results/final_v1/lich_theo_ca.csv) | Kết quả bài toán lập lịch theo ca MILP (4h, 8h, Hỗn hợp) | Thành viên B | MILP exact | Giải bằng `scipy.optimize.milp` |
| [`bat_dinh_tham_so.csv`](file:///d:/KHDV/results/final_v1/bat_dinh_tham_so.csv) | Phân phối mức độ phục vụ qua 50 bộ tham số bootstrap | Thành viên A | 50 x 20 reps | Xác định xác suất duy trì SLA khi tham số dao động |
| [`ngoai_mau.csv`](file:///d:/KHDV/results/final_v1/ngoai_mau.csv) | Kiểm định ngoài mẫu trên tập test 4 ngày (2.969 cuộc gọi) | Thành viên A | 150 reps | Kiểm định KS 2 mẫu và so sánh giờ đỉnh |

---

## 2. Danh mục biểu đồ đồ họa trong thư mục `hinh/`

1. [`fig_a_fit.png`](file:///d:/KHDV/results/final_v1/hinh/fig_a_fit.png): Kiểm định phân phối Poisson theo giờ và so sánh AIC các phân phối thời gian phục vụ.
2. [`fig_c_welch.png`](file:///d:/KHDV/results/final_v1/hinh/fig_c_welch.png): Đường cong Welch xác định điểm cắt warm-up (~200 khách / 150 phút).
3. [`fig_c_pooling.png`](file:///d:/KHDV/results/final_v1/hinh/fig_c_pooling.png): So sánh hiệu quả hàng chung bốc số tự động (96.5%) vs hàng riêng ngẫu nhiên (50.6%).
4. [`fig_c_do_nhay.png`](file:///d:/KHDV/results/final_v1/hinh/fig_c_do_nhay.png): Độ bền vững của 3 chính sách chính khi nhu cầu khách đến tăng từ 90% đến 130%.
5. [`fig_b_chi_phi.png`](file:///d:/KHDV/results/final_v1/hinh/fig_b_chi_phi.png): Đường đánh đổi Pareto giữa tổng quầy-giờ nhân sự và số lượt khách bỏ về mỗi ngày.
6. [`fig_b_ca_lam.png`](file:///d:/KHDV/results/final_v1/hinh/fig_b_ca_lam.png): Mức độ phủ quầy thực tế của các phương án ca làm (Hỗn hợp, Thuần 8h, Thuần 4h).
7. [`fig_a_bat_dinh.png`](file:///d:/KHDV/results/final_v1/hinh/fig_a_bat_dinh.png): Phân phối tần số của mức độ phục vụ qua 50 bộ tham số bootstrap.
8. [`fig_a_ngoai_mau.png`](file:///d:/KHDV/results/final_v1/hinh/fig_a_ngoai_mau.png): Đánh giá ngoài mẫu so sánh mức đạt SLA giữa tập Train và tập Test.

---

## 3. Quy ước và Cam kết Tính Nhất Quán
- **Nguyên tắc bất biến:** Toàn bộ bảng biểu, biểu đồ, con số xuất hiện trong **Báo cáo tổng kết** (`docs/bao_cao_tong_ket.md`) và **Bộ slide thuyết trình** (`docs/slide_thuyet_trinh.md`) đều được trích xuất 100% từ các tệp dữ liệu đã đóng băng tại thư mục này.
- Mọi điều chỉnh (nếu có sau ngày 23/10) bắt buộc phải tạo phiên bản mới `results/final_v2/` và cập nhật lại toàn bộ tài liệu liên quan.
