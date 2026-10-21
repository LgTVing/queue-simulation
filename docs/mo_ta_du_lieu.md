# Mô tả nguồn và quy trình làm sạch dữ liệu (Tuần 1)

**Người phụ trách:** Thành viên A  
**Ngày cập nhật:** 21/10/2026  
**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu  

---

## 1. Nguồn dữ liệu gốc

- **Tên bộ dữ liệu:** *Anonymous Bank Call-Center Data*
- **Đơn vị cung cấp:** Trung tâm Nghiên cứu Kỹ thuật Dịch vụ (SEE Center), Viện Công nghệ Technion (Israel).
- **Tài liệu tham chiếu:** *Statistical Analysis of a Telephone Call Center: A Queueing-Science Perspective* (Brown, Gans, Mandelbaum, Sakov, Shen, Zeltyn, Zhao - JASA 2005).
- **Địa chỉ truy cập chính thức:** `https://see-center.iem.technion.ac.il/databases/AnonymousBank/`
- **File tài liệu mô tả gốc:** [`AnonymousBank.pdf`](file:///d:/KHDV/data/raw/AnonymousBank.pdf)
- **File dữ liệu sử dụng:** `September1999.txt` (Tháng 9/1999, dung lượng thô 3.19 MB, gồm 31.371 cuộc gọi).

### Điều kiện sử dụng và bản quyền
Dữ liệu được cấp quyền sử dụng tự do cho mục đích nghiên cứu và học thuật với hai điều kiện bắt buộc:
1. Gửi thông báo sử dụng tới Giáo sư Avi Mandelbaum (`avim@ie.technion.ac.il`). *(Xem mẫu email tại mục 11.1 của TUAN_1_HUONG_DAN.md)*.
2. Trích dẫn đầy đủ nguồn dữ liệu và tài liệu trong báo cáo và slide thuyết trình.

---

## 2. Phép tương đương giữa Tổng đài và Quầy giao dịch ngân hàng

Do đặc thù ngân hàng thương mại tại Việt Nam bảo mật thông tin nội bộ rất nghiêm ngặt, việc xin log máy bốc số trong 3 tuần gặp nhiều rào cản hành chính. Bộ dữ liệu tổng đài của Technion được thiết kế chuẩn xác theo mô hình hàng đợi đa kênh:

| Yếu tố trong Tổng đài (Dữ liệu gốc) | Tương đương tại Quầy giao dịch Ngân hàng |
|---|---|
| Cuộc gọi vào (`call_id`) | Khách hàng đến chi nhánh giao dịch |
| Nhân viên tổng đài (`server`) | Giao dịch viên tại quầy |
| Hàng đợi trên tổng đài (`q_time`) | Khách ngồi chờ sau khi bấm số thứ tự |
| Cúp máy khi chờ (`outcome = HANG`) | Khách rời khỏi hàng / bỏ về do chờ quá lâu |
| Thời gian đàm thoại (`ser_time`) | Thời gian giao dịch viên thao tác xử lý nghiệp vụ tại quầy |
| Khách hàng ưu tiên (`priority = 2`) | Khách hàng VIP / Priority Banking |

---

## 3. Cấu trúc trường dữ liệu thô (`September1999.txt`)

Tệp dữ liệu phân tách bằng tab (`\t`), mã hóa `latin1`, gồm 17 trường:
1. `vru+line`: Mã tổng đài tự động và line vào.
2. `call_id`: Mã định danh cuộc gọi.
3. `customer_id`: Mã khách hàng (0 nếu không xác định).
4. `priority`: Mức ưu tiên (0 = không định danh, 1 = khách thường, 2 = khách VIP).
5. `type`: Mã loại giao dịch (`PS`: Giao dịch thường nhật - Peilut Shotefet; `NE`: Chứng khoán; `IN`: Internet; `NW`: Khách mới; `TT`: Gọi lại; `PE`: Tiếng Anh).
6. `date`: Ngày theo định dạng `YYMMDD`.
7. `vru_entry`, `vru_exit`, `vru_time`: Thời điểm vào/ra và thời gian tương tác tổng đài tự động.
8. `q_start`, `q_exit`, `q_time`: Thời điểm bắt đầu vào hàng đợi, thời điểm thoát hàng đợi, và tổng thời gian chờ (giây).
9. `outcome`: Kết quả cuộc gọi (`AGENT`: gặp nhân viên; `HANG`: bỏ về; `PHANTOM`: bản ghi ảo).
10. `ser_start`, `ser_exit`, `ser_time`: Thời điểm bắt đầu phục vụ, kết thúc và thời gian phục vụ (giây).
11. `server`: Tên giao dịch viên phục vụ.

---

## 4. Các quy tắc làm sạch dữ liệu (`data/lam_sach.py`)

1. **Loại bỏ bản ghi rác và bất thường:**
   - Loại bỏ các dòng lỗi định dạng phân tách (ví dụ dòng bị tràn cột do ký tự đặc biệt).
   - Loại bỏ cuộc gọi ảo `outcome == 'PHANTOM'`.
   - Giữ lại hai trạng thái hợp lệ: `AGENT` (được phục vụ) và `HANG` (bỏ về).
2. **Xác định khách thực sự vào hàng:**
   - Những khách `outcome == 'HANG'` nhưng `q_start == '0:00:00'` là khách cúp máy ngay trong lời chào tự động (chưa bấm phím gặp nhân viên, tương đương khách bước vào sảnh rồi quay ra không lấy số). Các cuộc gọi này được loại bỏ.
   - Khách có `q_start != '0:00:00'` hoặc `outcome == 'AGENT'` được tính là đã vào hàng đợi.
3. **Thống nhất loại nghiệp vụ:**
   - Chọn loại nghiệp vụ `PS` (*Peilut Shotefet* - Giao dịch thường nhật tại quầy), chiếm đa số áp đảo (hơn 66% tổng cuộc gọi), đảm bảo phân phối thời gian phục vụ có tính đồng nhất cao.
4. **Khung giờ làm việc chuẩn (Bank Daytime Hours):**
   - Lọc các cuộc gọi đến từ **8:00 sáng đến 17:00 chiều** (tương đương 9 khung giờ: $h = 0, 1, \dots, 8$).
5. **Chọn ngày làm việc tiêu chuẩn (Standard Workdays):**
   - Tại Israel, tuần làm việc chính từ Chủ Nhật đến Thứ Năm (Thứ Sáu làm nửa buổi, Thứ Bảy nghỉ lễ Sabbath). Trong tháng 9/1999 có một số ngày lễ lớn (Rosh Hashanah, Yom Kippur) lượng khách giảm đột biến.
   - Lọc ra 14 ngày làm việc tiêu chuẩn đầy đủ có lượng khách trên 1.300 cuộc/ngày: `990901`, `990902`, `990905`, `990906`, `990907`, `990908`, `990909`, `990913`, `990914`, `990915`, `990916`, `990921`, `990922`, `990923`.
6. **Quy đổi đơn vị:**
   - Đổi toàn bộ thời gian chờ (`q_time`) và thời gian phục vụ (`ser_time`) từ **giây sang phút** (chia 60.0).
   - Biến `t` là số phút tính từ 8:00 sáng.
7. **Kiểm tra tính toàn vẹn (Integrity Checks):**
   - `wait >= 0` (thời gian chờ không âm).
   - `svc > 0` và `svc <= 60` phút đối với khách được phục vụ (loại bỏ thời gian phục vụ âm hoặc ngoại lai > 1 tiếng do quên ngắt máy).

---

## 5. Cấu trúc tệp dữ liệu sạch (`data/clean/data_clean.csv`)

| Tên cột | Ý nghĩa | Kiểu dữ liệu | Phạm vi giá trị |
|---|---|---|---|
| `day` | Chỉ số ngày quan sát (0 đến 13) | Số nguyên | 0, 1, ..., 13 |
| `t` | Thời điểm khách vào hàng (phút từ 8:00) | Số thực | $[0.0, 540.0)$ |
| `hour` | Khung giờ trong ngày | Số nguyên | 0 (8h-9h) đến 8 (16h-17h) |
| `cls` | Phân loại giao dịch nghiệp vụ | Chuỗi / Trống | Để trống (nghiệp vụ chuẩn `PS`) |
| `vip` | Khách hàng ưu tiên / VIP | 0 hoặc 1 | 1 nếu `priority == 2`, ngược lại 0 |
| `wait` | Thời gian chờ trong hàng đợi (phút) | Số thực | $\ge 0.0$ |
| `served` | Trạng thái phục vụ thành công | 0 hoặc 1 | 1 nếu gặp nhân viên, 0 nếu bỏ về |
| `svc` | Thời gian được phục vụ (phút) | Số thực | $> 0.0$ nếu `served == 1`, trống nếu bỏ về |

---

## 6. Tổng kết số lượng sau làm sạch

- **Số dòng ban đầu:** 31.371 dòng.
- **Số dòng sạch hợp lệ:** 9.836 dòng (đạt 31.4% toàn bộ dữ liệu, bao gồm 100% các cuộc gọi nghiệp vụ chuẩn trong giờ hành chính của 14 ngày làm việc trọn vẹn).
- **Lượng khách trung bình:** 702.6 khách/ngày (~78 khách/giờ).
- **Tỉ lệ khách VIP:** 33.8%.
- **Tỉ lệ khách bỏ về (Abandonment rate):** 7.15%.
- **Thời gian phục vụ trung bình $E[S]$:** 2.88 phút ($\sigma = 3.15$ phút, $cv \approx 1.095$).
