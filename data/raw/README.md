# Dữ liệu thô (không lưu trong repo)

Dữ liệu thô của bộ **Anonymous Bank call-center data** (SEE Center, Technion – Israel Institute of Technology) không được lưu trong repo này (F8, `docs/KE_HOACH_V5_1.md`). Điều khoản của nguồn chỉ cho phép sử dụng (kèm thông báo và ghi nguồn), không nói về phân phối lại.

Pipeline chính không cần thư mục này: `main.py` đọc tập đã làm sạch `data/clean/data_clean.csv`. Chỉ cần dữ liệu thô khi muốn chạy lại bước làm sạch `data/lam_sach.py`.

## Cách tải

1. Tải hai tệp tại `https://see-center.iem.technion.ac.il/databases/AnonymousBank/Data/`:

   | Tệp | Kích thước (byte) |
   |---|---:|
   | `AnonymousBank.pdf` (tài liệu mô tả) | 35.223 |
   | `AnonymousBank.rar` (dữ liệu 12 tháng năm 1999) | 10.625.021 |

2. Giải nén `AnonymousBank.rar` (WinRAR, 7-Zip hoặc `unrar x AnonymousBank.rar`), chép `September1999.txt` (3.222.120 byte) vào thư mục này. Bản V5 còn dùng `October1999.txt` (3.529.771 byte) để tham khảo.
3. Chạy `python data/lam_sach.py`. Kết quả phải trùng `data/clean/data_clean.csv` (kiểm bằng `pytest tests/test_f7_clean.py`).

Các tệp trong thư mục này (trừ `README.md`) bị `.gitignore` bỏ qua.

## Điều kiện sử dụng

> "The data is free for use. If used, please notify Avi Mandelbaum, at avim@ie.technion.ac.il and do acknowledge the data source in any of your work." — `AnonymousBank.pdf` (Guedj và Mandelbaum, 2000)

Ghi nguồn trong báo cáo và slide: *Anonymous Bank call-center data, Service Enterprise Engineering (SEE) Center, Technion – Israel Institute of Technology.*
