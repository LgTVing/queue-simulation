# Bản V5.0 của các tệp đổi ở V5.1

Sao từ `results/final_v5/` tại commit `116fdcc` (nhánh `feat/v5`, 2026-10-30) trước khi chạy lại R5 của `docs/KE_HOACH_V5_1.md`. Chỉ gồm các tệp có thể đổi ở V5.1; mọi tệp khác của V5.0 vẫn nằm nguyên trong `results/final_v5/`.

| Tệp | Lý do đổi ở V5.1 |
|---|---|
| `toi_uu_xac_suat_ngay.csv` | F5: M7 xác nhận bằng dải seed độc lập 2.000 lần lặp (V5.0 dùng seed 50000 trùng 253/300 lần lặp với seed chọn lịch) |
| `doi_chieu_v4_v5.csv` | Các dòng M7 đọc từ `toi_uu_xac_suat_ngay.csv` |
| `MO_TA_final_v5.md` | `MO_TA.md` của V5.0 (ghi chú seed, danh mục tệp) |
| `thoi_gian_chay.json` | Thời gian chạy giai đoạn `optimize`, `report` |
| `lich_khuyen_nghi.json` | Ghi lại khi chạy `optimize`; V5.1 thêm khóa `toi_uu_khach_thuong` (M9) |
| `bat_dinh_nested.csv`, `phan_ra_phuong_sai.csv` | F9: bootstrap lồng nhau S5 dùng dải seed riêng cho từng bộ (V5.0 chỉ có 640 seed khác nhau cho 3.000 cặp bộ × lần lặp) |
| `ngoai_mau.csv` | S16: p-value ngoài mẫu S6 lấy từ phân phối mô phỏng (V5.0 dùng z-test SE nhị thức) |
