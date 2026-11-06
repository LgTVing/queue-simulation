# Biên Bản Đóng Băng Dữ Liệu và Kết Quả Dự Án (results/final_v2/)

**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu cho ngân hàng  
**Phiên bản đóng băng:** `final_v2` (Phiên bản hiệu chỉnh theo đợt kiểm tra độc lập)  
**Ngày chạy và cập nhật:** 23/10/2026  
**Phiên bản tham số:** `params.json` v2.0 (tập Train 10 ngày)  
**Hạt giống ngẫu nhiên (Seeds):**
- Đánh giá chính sách cơ sở: `seed_base = 50000` (300 reps)
- Đánh giá biến động theo ngày: `seed_base = 20000` (300 reps, $CV_{\text{ngày}} = 11.8\%$)
- Khảo sát theo 14 ngày thực tế: `seed_base = 30000` (40 reps/ngày)
- Kiểm tra ngoài mẫu: `seed_base = 40000` (Phiên bản A, 200 reps) & `41000` (Phiên bản B, 200 reps)
- Kiểm tra độ nhạy phân phối: `seed_base = 60000` (150 reps CRN paired)
- Độ nhạy T6: `seed_base = 80000` (150 reps)
**Môi trường thực thi:** Python 3.13.3, SimPy 4.1.1, SciPy 1.15.2, NumPy 2.2.3, Pandas 2.2.3, pytest 9.1.1  
**Mã commit cơ sở:** `f058650` (Nhánh: `fix/chinh-sua-agent`)  

---

## 1. Danh mục các Tệp Số liệu trong `results/final_v2/`

| Tên tệp | Nội dung tệp | Nhiệm vụ liên quan | Ghi chú kỹ thuật |
|---|---|:---:|---|
| [`params.json`](file:///d:/KHDV/results/final_v2/params.json) | Bộ tham số ước lượng từ 10 ngày Train | T11 | Version v2.0 ($E[S]=2.9236$, $\theta=0.1087$) |
| [`kiem_dinh_poisson.csv`](file:///d:/KHDV/results/final_v2/kiem_dinh_poisson.csv) | Kiểm định Poisson theo giờ với nhãn nghiêm ngặt | T1 | 8/9 giờ bị bác bỏ ở mức 5% |
| [`qua_phan_tan_ngay.csv`](file:///d:/KHDV/results/final_v2/qua_phan_tan_ngay.csv) | Thống kê quá phân tán lưu lượng theo ngày | T1 | $\text{Var}/\text{Mean} = 10.8$, $CV_{\text{ngày}} = 11.8\%$ |
| [`bien_dong_ngay.csv`](file:///d:/KHDV/results/final_v2/bien_dong_ngay.csv) | Đánh giá chính sách khi có biến động lưu lượng ngày | T2 | Bổ sung $m_d \sim \text{Gamma}$, xác suất đạt SLA |
| [`theo_ngay.csv`](file:///d:/KHDV/results/final_v2/theo_ngay.csv) | Hiệu năng 3 chính sách trên từng ngày trong 14 ngày thật | T2 | Lịch 44 đạt 10/14 ngày; Lịch 48 đạt 13/14 ngày |
| [`nguong_luu_luong.csv`](file:///d:/KHDV/results/final_v2/nguong_luu_luong.csv) | Ngưỡng khách/ngày để chuyển đổi giữa các lịch | T2, T10 | Ngưỡng 687 khách/ngày ($\le 100\%$ danh nghĩa) |
| [`so_sanh_chinh_sach_v2.csv`](file:///d:/KHDV/results/final_v2/so_sanh_chinh_sach_v2.csv) | Bảng so sánh chính sách tổng hợp (có và không biến động) | T2 | Thể hiện cả $SL$ trung bình và xác suất đạt ngày |
| [`lich_theo_ca_v2.csv`](file:///d:/KHDV/results/final_v2/lich_theo_ca_v2.csv) | Nghiệm bài toán ca làm việc MILP cho các mô hình | T5 | Mô hình A & B, phân biệt giờ làm vs giờ có mặt |
| [`do_nhay_phan_phoi_v2.csv`](file:///d:/KHDV/results/final_v2/do_nhay_phan_phoi_v2.csv) | Độ nhạy phân phối phục vụ so sánh cặp CRN | T8 | Hiệu số so với Gamma kèm khoảng tin cậy 95% |
| [`ngoai_mau_v2.csv`](file:///d:/KHDV/results/final_v2/ngoai_mau_v2.csv) | Đánh giá ngoài mẫu 2 phiên bản (A và B) | T4 | So sánh công bằng, ghi rõ điều kiện nhân sự |
| [`ngoai_mau_tham_so.json`](file:///d:/KHDV/results/final_v2/ngoai_mau_tham_so.json) | Tài liệu hóa chi tiết tham số tập Test | T4 | Chi tiết cấu hình chạy ngoài mẫu |
| [`dao_dong_seed.csv`](file:///d:/KHDV/results/final_v2/dao_dong_seed.csv) | Khảo sát độ nhạy mô phỏng qua 3 khối hạt giống | T6 | Dao động nội tại $\pm 0.04\%$ |
| [`pvip_theo_gio.csv`](file:///d:/KHDV/results/final_v2/pvip_theo_gio.csv) | Tỉ lệ khách VIP theo từng khung giờ trong ngày | T12 | Dao động từ 18.35% (8h) đến 52.15% (15h) |
| [`doi_chieu_tham_so.csv`](file:///d:/KHDV/results/final_v2/doi_chieu_tham_so.csv) | Đối chiếu tham số 14 ngày vs 10 ngày Train | T11 | Phân định rõ mục đích sử dụng từng bộ |
| [`tham_so_thanh_phan.csv`](file:///d:/KHDV/results/final_v2/tham_so_thanh_phan.csv) | Phân công bộ tham số cho từng cấu phần | T11 | Rạch ròi giữa Excel, SIPP, SimPy |
| [`pytest_log.txt`](file:///d:/KHDV/results/final_v2/pytest_log.txt) | Nhật ký chạy kiểm thử tự động pytest 18/18 passed | T13 | Đính kèm đầy đủ log kiểm thử tự động |
| [`kiem_chung.csv`](file:///d:/KHDV/results/final_v2/kiem_chung.csv) | Kiểm chứng 3 tầng lý thuyết và 2 kiểm tra độc lập | - | Kế thừa từ final_v1 |
| [`lich_toi_uu.csv`](file:///d:/KHDV/results/final_v2/lich_toi_uu.csv) | Lịch sử thuật toán tối ưu hóa 2 pha SimPy | T7 | Kế thừa từ final_v1 |
| [`chi_phi.csv`](file:///d:/KHDV/results/final_v2/chi_phi.csv) | Hàm chi phí kinh tế đánh đổi Pareto | - | Kế thừa từ final_v1 |
| [`do_nhay.csv`](file:///d:/KHDV/results/final_v2/do_nhay.csv) | Độ nhạy toàn diện hệ thống T6 | - | Kế thừa từ final_v1 |
| [`bat_dinh_tham_so.csv`](file:///d:/KHDV/results/final_v2/bat_dinh_tham_so.csv) | Độ bất định tham số qua 50 bộ bootstrap | T9 | Kế thừa từ final_v1 |

---

## 2. Các Biểu đồ Đồ họa trong `results/final_v2/hinh/`
Toàn bộ các đồ thị được lưu trữ đồng thời tại thư mục gốc và thư mục `results/final_v2/hinh/`.
