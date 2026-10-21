# Kế hoạch khảo sát thực tế tại chỗ (Tuần 1)

**Người phụ trách:** Thành viên C (phối hợp Thành viên A)  
**Ngày lập:** 21/10/2026  
**Dự án:** Mô phỏng hàng đợi và xác định số quầy phục vụ tối ưu  

---

## 1. Mục tiêu đợt khảo sát thực địa

1. **Khảo sát thí điểm (Pilot test):** Chạy thử 1 buổi (khoảng 1–2 giờ) để kiểm tra tính khả thi của quy trình đo thủ công, biểu mẫu ghi chép và sự đồng bộ đồng hồ giữa 3 thành viên.
2. **Thu thập dữ liệu đối chứng địa phương:** Đo lường các chỉ số thực tế tại Việt Nam (thời gian khách đến, thời gian phục vụ tại quầy, tỉ lệ kiên nhẫn) nhằm đối chiếu và kiểm chứng mức độ phù hợp của bộ dữ liệu quốc tế `Anonymous Bank`.
3. **Ưu tiên lấy log điện tử:** Xin dữ liệu log máy bốc số thứ tự tự động (đã ẩn danh) để có cỡ mẫu lớn mà không gây xáo trộn hoạt động tại quầy.

---

## 2. Danh sách địa điểm liên hệ và trạng thái

| STT | Địa điểm khảo sát dự kiến | Loại hình dịch vụ | Phương án tiếp cận | Trạng thái hiện tại | Kế hoạch dự phòng |
|---|---|---|---|---|---|
| **1** | Chi nhánh Ngân hàng Agribank / Vietcombank gần trường | Quầy giao dịch tài chính | Xin log máy bốc số thứ tự qua Giấy giới thiệu của Giảng viên | Đang gửi thư xin phép (Mẫu 11.2) | Nếu từ chối do bảo mật $\implies$ chuyển sang Địa điểm 2 hoặc 3 |
| **2** | Bộ phận Tiếp nhận & Trả kết quả (Một cửa) UBND Phường/Quận | Dịch vụ hành chính công | Quan sát trực tiếp tại sảnh chờ có bảng số điện tử | Đã liên hệ sơ bộ, chờ phê duyệt | Tiến hành đo khung giờ 8h30 - 10h30 |
| **3** | Phòng Đào tạo / Phòng Công tác sinh viên trường Đại học | Dịch vụ học vụ sinh viên | Quan sát trực tiếp giờ tiếp sinh viên | Khả thi cao, dễ xin phép | Làm địa điểm dự phòng chính |
| **4** | Căng tin trường / Quầy thanh toán siêu thị mini | Dịch vụ bán lẻ ăn uống | Bấm giờ trực tiếp tại quầy thanh toán | Sẵn sàng bất kỳ lúc nào | Dự phòng khẩn cấp nếu các nơi khác bị từ chối |

---

## 3. Phân công vai trò trong buổi khảo sát thực địa (3 thành viên)

Để tránh nhầm lẫn và sót dữ liệu khi khách đến dồn dập, 3 thành viên phân chia nhiệm vụ chuyên biệt:

- **Thành viên A (Quan sát đầu vào & Bỏ về):**
  - Đứng gần cửa ra vào / máy lấy số.
  - Ghi nhận chính xác: STT khách, thời điểm vào hàng (giờ:phút:giây), cờ khách ưu tiên (VIP/người cao tuổi).
  - Quan sát và ghi nhận các trường hợp khách bỏ về (rời hàng trước khi được gọi tên) kèm thời điểm bỏ về.
- **Thành viên B (Quan sát thời điểm phục vụ tại quầy):**
  - Đứng ở vị trí quan sát rõ các quầy giao dịch.
  - Ghi nhận: Quầy số mấy bắt đầu phục vụ khách nào, thời điểm bắt đầu phục vụ (giờ:phút:giây).
  - Theo dõi số lượng quầy đang thực tế mở và hoạt động tại từng thời điểm.
- **Thành viên C (Quan sát kết thúc & Phân loại nghiệp vụ):**
  - Ghi nhận thời điểm khách rời quầy (kết thúc phục vụ).
  - Phân loại nhanh giao dịch: Nhanh (nộp/rút tiền, in sao kê) hoặc Phức tạp (mở tài khoản, hồ sơ tín dụng).
  - Đối chiếu chéo số liệu với A và B sau mỗi 30 phút để đảm bảo không bị lệch dòng.

---

## 4. Biểu mẫu ghi dữ liệu thực địa (In sẵn cho mỗi buổi)

> **Ghi chú chuẩn bị trước buổi đo:**
> - Đồng bộ đồng hồ điện thoại của cả 3 thành viên theo trang web chuẩn `time.is` (chính xác đến từng giây).
> - Ghi rõ: Ngày đo, Địa điểm, Thời tiết, Số quầy mở ban đầu.

| STT | Giờ vào hàng (A) | Giờ bắt đầu phục vụ (B) | Giờ kết thúc phục vụ (C) | Quầy số (B) | Phân loại (C) (Nhanh/Phức tạp) | Khách VIP (A) (0/1) | Bỏ về? (A) (0/1) | Giờ bỏ về (A) | Ghi chú bất thường |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| 01 | 08:32:15 | 08:33:02 | 08:35:40 | Quầy 2 | Nhanh | 0 | 0 | - | - |
| 02 | 08:33:10 | 08:34:15 | 08:38:22 | Quầy 1 | Phức tạp | 0 | 0 | - | Khách hỏi nhiều |
| 03 | 08:34:05 | - | - | - | - | 0 | 1 | 08:37:12 | Chờ 3p rồi bỏ đi |
| 04 | 08:35:20 | 08:35:50 | 08:37:10 | Quầy 2 | Nhanh | 1 | 0 | - | Khách ưu tiên |

---

## 5. Cam kết bảo mật và quy tắc ứng xử

1. **Không thu thập dữ liệu cá nhân (PII):** Tuyệt đối không ghi lại họ tên, số căn cước công dân, số tài khoản, số điện thoại hay số tiền giao dịch của khách hàng.
2. **Không quay phim, chụp ảnh:** Chỉ sử dụng bảng ghi chép trên giấy hoặc ứng dụng ghi chú điện tử cá nhân.
3. **Không cản trở vận hành:** Giữ khoảng cách tối thiểu 2 mét với quầy giao dịch, không đứng chắn lối đi của khách hàng và nhân viên.
4. **Chia sẻ kết quả nghiên cứu:** Sau khi hoàn thành đồ án, nhóm sẽ gửi tặng lại báo cáo kết quả tối ưu số quầy cho đơn vị nếu đơn vị có nhu cầu tham khảo.

---

## 6. Kế hoạch dự phòng (Fallback Strategy)

Nếu sau Ngày 3 của Tuần 1, các ngân hàng và đơn vị hành chính đều từ chối cấp phép hoặc không kịp phê duyệt:
- **Nguyên tắc:** **Tuyệt đối không chờ đợi làm đình trệ tiến độ.**
- Toàn bộ trọng tâm phân tích định lượng sẽ sử dụng bộ dữ liệu chuẩn `Anonymous Bank` (Technion SEE Center) với 9.836 giao dịch đã được làm sạch hoàn chỉnh.
- Tiến hành đo nhanh 1 buổi 2 tiếng tại **Căng tin hoặc Phòng Đào tạo của trường** để có ví dụ minh họa thực tế tại Việt Nam đưa vào phần thảo luận và đối chiếu trong báo cáo.
