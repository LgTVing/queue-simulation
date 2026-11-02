# KẾ HOẠCH NÂNG CẤP V5.1

**Ngày lập:** 2026-11-02
**Điểm xuất phát:** commit `116fdcc` trên nhánh `feat/v5`. V5 đã đóng băng tại `results/final_v5/`; `pytest -q` 84/84 (kể cả smoke test), checker 1.502 + 132 giá trị khớp, CI trên GitHub xanh.
**Nguồn:** rà soát mã nguồn ngày 2026-11-02 (đọc mã, chạy test, chạy script kiểm chứng chỉ đọc). Số liệu kiểm chứng ở [Phụ lục A](#phụ-lục-a--số-liệu-kiểm-chứng-của-rà-soát).
**Mục đích:** sửa các điểm làm yếu kết luận trước buổi bảo vệ (seed đánh giá không độc lập, định nghĩa SLA lệch giữa tài liệu và mã), tăng khả năng tái lập, giảm thời gian chạy. **Không đổi số V5 khi chưa chủ đích**; mọi thay đổi số phải có bảng trước/sau.

---

## Trạng thái

Đánh dấu `[x]` khi xong, ghi commit vào cột cuối.

| Mã | Việc | Ưu tiên | Người gợi ý | Trạng thái | Commit |
|---|---|:---:|---|:---:|---|
| F4 | Sổ đăng ký dải seed + test không giao nhau | **P1** | Thọ | [x] | `b503b66` |
| F5 | Đánh giá M7 bằng seed độc lập | **P1** | Quang | [x] | `47328f7` |
| F6 | Chốt định nghĩa SLA, thêm bảng SL theo nhóm khách | **P1** | Thọ + cả nhóm | [x] | `f4f19ba` |
| F7 | Sửa đường dẫn cứng `data/lam_sach.py` + test tái lập | P2 | Vinh | [x] | `788a845` |
| F8 | Kiểm tra điều khoản phân phối lại dữ liệu thô | P2 | Vinh | [x] gỡ dữ liệu thô; [ ] **gửi email cho người quản lý dữ liệu** | `0478ead` |
| T4 | Sửa test `poisson_label` kiểm bản sao | P2 | Vinh | [x] | `8e46bd7` |
| F9 | Seed bootstrap lồng nhau S5 | P2 | Quang | [x] | `7778e40` |
| S16 | p-value ngoài mẫu S6 từ phân phối mô phỏng | P2 | Vinh | [x] | `7778e40` |
| F10 | Cờ khả thi cho bộ tối ưu và SIPP | P2 | Thọ | [x] | `06de1cc` |
| F11 | Đếm khách chưa xử lý xong khi cắt mô phỏng | P3 | Thọ | [x] | `e6151ae` |
| F12 | Dọn nợ kỹ thuật nhỏ | P3 | cả nhóm | [x] (giữ `version` trong `params.json` tới lần chạy lại giai đoạn `data`) | `bde0a34` |
| T5 | Bộ test bổ sung | P2 | theo mảng | [x] `test_f4_seeds`, `test_f7_clean`, `test_v51_fixes`, `test_d5_demo` | nhiều commit |
| O1 | Bộ nhớ đệm kết quả `run_reps` | P3 | Thọ | [x] `optimize` 11.1 → 8.3 phút | `c39f124` |
| O2 | Rút thời gian smoke test | P3 | Thọ | [x] 10–13 phút → 84 giây | `34fdd79` |
| M9 | Tùy chọn tối ưu theo SLA khách thường | P3 (tùy chọn) | Thọ | [x] 47 quầy-giờ, vẫn 48 giờ công | `3588b3c` |
| R5 | Chạy lại, cập nhật `final_v5` thành v5.1 | **P1** | Vinh | [x] chạy `optimize` + `report`; `doi_chieu_v5_v5_1.csv` thay bằng mục 8 `tong_hop.md` và `results/archive/final_v5_0/` | `results(R5)` |
| D7 | Cập nhật tài liệu theo v5.1 | **P1** | theo mảng | [x] | `docs(D7)` |
| D5 | Trang HTML demo SIPP (đã có trong `PHAN_CONG.md`) | P2 | Quang | [x] `docs/demo/sipp.html` | `29e211b` |
| D6 | Slide thật và tập dượt (đã có trong `PHAN_CONG.md`) | P1 | Vinh, Thọ | [ ] | |

---

## Mục lục

0. [Tóm tắt phát hiện](#0-tóm-tắt-phát-hiện)
1. [Thứ tự triển khai](#1-thứ-tự-triển-khai)
2. [Quy tắc chung](#2-quy-tắc-chung)
3. [Giai đoạn 1 — Sửa](#3-giai-đoạn-1--sửa)
4. [Giai đoạn 2 — Cải thiện](#4-giai-đoạn-2--cải-thiện)
5. [Giai đoạn 3 — Tối ưu hiệu năng](#5-giai-đoạn-3--tối-ưu-hiệu-năng)
6. [Giai đoạn 4 — Mở rộng](#6-giai-đoạn-4--mở-rộng)
7. [Chạy lại và cập nhật tài liệu (R5, D7)](#7-chạy-lại-và-cập-nhật-tài-liệu-r5-d7)
8. [Checklist](#8-checklist)
9. [Không nên làm lúc này](#9-không-nên-làm-lúc-này)
10. [Câu hỏi cần chốt](#10-câu-hỏi-cần-chốt)
- [Phụ lục A — Số liệu kiểm chứng của rà soát](#phụ-lục-a--số-liệu-kiểm-chứng-của-rà-soát)
- [Phụ lục B — Dải seed đang dùng](#phụ-lục-b--dải-seed-đang-dùng)
- [Phụ lục C — Lệnh tái hiện kiểm chứng](#phụ-lục-c--lệnh-tái-hiện-kiểm-chứng)

---

## 0. Tóm tắt phát hiện

**Giữ nguyên, không cần sửa:** `b_theory.py` (Erlang-A ma trận hấp thụ đúng), động cơ `c_sim.simulate` (blocker `cancel`/`release`, kiên nhẫn, NHPP, CRN), lớp chạy song song `map_sim`, checker và CI, cách chia train/test. Giả định "mở cửa trống lúc 8h" đúng với dữ liệu thô (trung bình 0 khách đang chờ, ~1,4 khách đang phục vụ lúc 8:00).

| # | Phát hiện | Mức | Đổi kết luận? | Việc |
|---|---|:---:|---|---|
| 1 | M7: 253/300 lần lặp đánh giá **giống hệt** lần lặp chọn lịch nên P báo cáo lạc quan. Một dải độc lập 300 lần lặp cho 0,92 [0,884]; nhưng 2 dải độc lập × 1.000 lần lặp lệch nhau ~2,5 điểm, cho thấy 300 lần lặp là quá ít. Gộp 2.000 lần lặp độc lập: lịch 48 giờ công 0,937–0,946 (cận dưới ≥ 0,926), lịch 52 giờ công 0,968–0,989 (cận dưới ≥ 0,959) | P1 | **Không đổi kết luận** ("≥ 90% số ngày cần 48 giờ công", "≥ 95% cần 52"), nhưng số P và CI trong tài liệu phải thay bằng số đánh giá độc lập | F4, F5 |
| 2 | Đặc tả SLA tách khách thường (≤ 5 phút) và VIP (≤ 2 phút) ([dac_ta_mo_hinh.md:27-28](dac_ta_mo_hinh.md#L27-L28), README:55, :401) nhưng mã chỉ xét SL gộp mọi khách ([c_sim.py:754-776](../c_sim.py#L754-L776)). Theo đặc tả, Lịch 45 không đạt ở 11h–12h (khách thường 0,887–0,8997 trên 3 dải seed); Lịch 48 đạt (0,913–0,915) | P1 | Câu "Lịch 45 đạt SLA" phụ thuộc định nghĩa. **Khuyến nghị Lịch 48 vẫn đứng vững** | F6 |
| 3 | Optimize, M6: 11/300 lần lặp đánh giá trùng lần lặp chọn lịch, trong khi `MO_TA.md` ghi "tách biệt" | P2 | Không: seed tách hẳn cho Lịch 45 giờ tệ nhất 0,914 (bảng ghi 0,924), vẫn khả thi | F4 (ghi chú) |
| 4 | S5: 3.000 cặp (bộ bootstrap, lần lặp) chỉ dùng 640 seed khác nhau → nhiễu mô phỏng tương quan giữa các bộ, phân rã phương sai sai lệch | P2 | Chưa đo | F9 |
| 5 | `data/lam_sach.py` dùng `d:\KHDV` (không tồn tại). Sửa đường dẫn thì tái lập khớp `data_clean.csv` từng giá trị | P2 | Không | F7 |
| 6 | S6: z-test dùng SE nhị thức ([e_robustness.py:376](../e_robustness.py#L376)); 8h–9h, 9h–10h nằm **trong** PI95 vẫn bị gắn "lệch có ý nghĩa" | P2 | Có (mục 5 `tong_hop.md`) | S16 |
| 7 | `test_poisson_labels_strict` kiểm bản sao cục bộ của `poisson_label` | P3 | Không | T4 |
| 8 | Repo GitHub **công khai** chứa dữ liệu thô của bên thứ ba (`data/raw/`) | P2 | Không | F8 |

Nguyên nhân gốc của #1, #3, #4: quy ước seed ở `KE_HOACH_V5.md` mục 1 (`seed_base + 1000·i`, "dùng dải riêng") chỉ quy định điểm bắt đầu, không quy định độ dài dải; 300 lần lặp × bước 1000 chiếm 300.000 seed nên các dải chồng nhau.

---

## 1. Thứ tự triển khai

| # | Mã | Việc | Ưu tiên | Phụ thuộc | Đổi số V5? | Ước lượng |
|:---:|---|---|:---:|---|---|:---:|
| 1 | F4 | Sổ đăng ký seed + test | P1 | – | Không (chỉ thêm test, ghi chú) | 1–2 h |
| 2 | F5 | M7 đánh giá độc lập | P1 | F4 | **Có**: `toi_uu_xac_suat_ngay.csv` cột đánh giá | 1 h + chạy |
| 3 | F6 | Định nghĩa SLA + `sl_theo_nhom.csv` | P1 | Chốt câu hỏi Q1 | Thêm tệp mới; CSV cũ giữ nguyên | 2–3 h |
| 4 | F7 | Đường dẫn `lam_sach.py` + test | P2 | – | Không | 1 h |
| 5 | T4 | Sửa test `poisson_label` | P2 | – | Không | 15 phút |
| 6 | F9 | Seed S5 | P2 | F4 | **Có**: `bat_dinh_nested.csv`, `phan_ra_phuong_sai.csv` | 30 phút + chạy |
| 7 | S16 | p-value S6 | P2 | – | **Có**: `ngoai_mau.csv` cột p-value, nhãn | 1–2 h |
| 8 | F10 | Cờ khả thi | P2 | – | Không | 1 h |
| 9 | T5 | Test bổ sung | P2 | F4, F6, F10 | Không | 2–3 h |
| 10 | F8 | Điều khoản dữ liệu | P2 | – | Không | 30 phút |
| 11 | O1 | Cache `run_reps` | P3 | – | Không (phải giống từng byte) | 2–3 h |
| 12 | F11, F12, O2 | Dọn dẹp, cắt mô phỏng, smoke test | P3 | – | Gần như không (xem từng mục) | 2–3 h |
| 13 | R5 | Chạy lại, cập nhật v5.1 | P1 | mọi việc đổi số | – | 1 h + 15 phút chạy |
| 14 | D7 | Tài liệu | P1 | R5 | – | 3–5 h |
| 15 | M9 | Tối ưu theo SLA khách thường | P3 | F6 | Thêm kết quả mới | 3 h |
| 16 | D5, D6 | Demo, slide | P1–P2 | D7 | Không | theo `PHAN_CONG.md` |

```
F4 ──┬── F5 ──┐
     └── F9 ──┤
F6 ───────────┤
S16 ──────────┼── R5 ── D7 ── D6
F7, T4, F10, T5, F8, O1, F11, F12, O2 (độc lập, không đổi số)
F6 ── M9 (tùy chọn, sau bảo vệ cũng được)
```

**Bộ tối thiểu trước buổi bảo vệ:** F4 → F5 → F6 → R5 → D7. Khoảng 1 ngày công. Mọi việc khác làm khi còn thời gian.

**Lý do của thứ tự:**
- F5 và F6 là hai chỗ hội đồng có thể bắt lỗi trực tiếp vào kết luận. F4 làm trước để F5, F9 dùng dải seed đúng ngay từ đầu.
- Gom mọi việc đổi số (F5, F9, S16, F6) vào **một lần** R5 + D7, vì mỗi lần đổi số đều phải cập nhật tài liệu.
- Việc không đổi số (F7, T4, F10, O1…) làm xen kẽ được, không cần chạy lại pipeline.

---

## 2. Quy tắc chung

1. **Nhánh và commit:** tạo nhánh `feat/v5.1` từ `feat/v5`. Mỗi mã việc một commit, tiêu đề dạng `fix(F5): ...`, `test(T4): ...`, `perf(O1): ...`, `docs(D7): ...`.
2. **Không ghi đè `final_v5` khi đang phát triển.** Chạy thử với `QS_RESULTS_DIR` trỏ ra thư mục tạm. Chỉ ở R5 mới ghi vào `results/final_v5/` (xem [mục 7](#7-chạy-lại-và-cập-nhật-tài-liệu-r5-d7)).
3. **Việc "không đổi số"** phải chứng minh bằng `diff -rq` giữa thư mục tạm và `results/final_v5/` khi chạy cùng `--reps-scale` (bỏ qua `MO_TA.md`, `thoi_gian_chay.json`, ngày chốt trong `params.json`).
4. **Việc "đổi số"** ghi bảng trước/sau vào `results/final_v5/doi_chieu_v5_v5_1.csv` (xem R5) kèm nguyên nhân.
5. **Seed (thay quy tắc 5 của `KE_HOACH_V5.md`):** mọi dải seed khai báo trong sổ đăng ký `common.SEED_BANDS` (F4) với **điểm bắt đầu, bước và số lần lặp tối đa**. Cặp "chọn lịch / đánh giá" của cùng một thí nghiệm **không được giao nhau**; test `tests/test_f4_seeds.py` kiểm tra. Dải chung giữa các cấu hình *khác nhau* (CRN) được phép và nên ghi rõ là cố ý.
6. **Test:** mỗi việc có ít nhất một test; `pytest -q` pass trước khi merge; `python tools/check_consistency.py` pass.
7. **Từ ngữ trong tài liệu:** checker quét mọi `docs/*.md`; tránh các cụm trong `FORBIDDEN_PATTERNS` của `tools/check_consistency.py`.

---

## 3. Giai đoạn 1 — Sửa

### F4. Sổ đăng ký dải seed và test không giao nhau

**Hiện nay.** Hằng seed nằm rải ở 4 module và định nghĩa trùng:
- [d_experiments.py:41-42](../d_experiments.py#L41-L42): `SEED_SELECT = 1000`, `SEED_EVAL = 50000`.
- [h_staffing.py:24-26](../h_staffing.py#L24-L26): định nghĩa lại `SEED_SELECT`, `SEED_EVAL`; [h_staffing.py:129](../h_staffing.py#L129): `SEED_SELECT_DAY = 3000` ("tách khỏi seed đánh giá 50000" — không đúng).
- [e_robustness.py:312](../e_robustness.py#L312), [:319](../e_robustness.py#L319): `60000 + b*100`, `90000`.
- [f_scenarios.py:439](../f_scenarios.py#L439): `SEED_M8 = 400000`.
- Bước lặp: [c_sim.py:508](../c_sim.py#L508) `seed_base + i * 1000`.

**Cách làm.**
1. Trong `common.py` thêm sổ đăng ký (chỉ khai báo, **giữ nguyên giá trị cũ** để không đổi số V5):
   ```python
   # (bat dau, buoc, so lan lap toi da) - dai seed cua run_reps: bat_dau + buoc * i, i < so_lan_lap
   SEED_STEP = 1000
   SEED_BANDS = {
       "select":       (1000,      SEED_STEP, 60),    # optimize_schedule, Pha 3, M6 chon lich
       "eval":         (50000,     SEED_STEP, 300),   # so sanh chinh sach, M6 xac nhan
       "select_day":   (3000,      SEED_STEP, 300),   # M7 chon lich (bien dong ngay)
       "screen_day":   (503000,    SEED_STEP, 100),   # M7 sang loc
       "eval_day":     (20_000_000, SEED_STEP, 2000), # M7 danh gia doc lap, 2000 lan lap (F5, moi)
       "nested_boot":  (60_000_000, 100_000, 50),     # S5: moi bo b co base rieng (F9, moi)
       "nested_nom":   (70_000_000, SEED_STEP, 60),   # S5 danh nghia (F9, moi)
       ...
   }
   def seed_range(name: str) -> range: ...
   ```
2. `d_experiments`, `h_staffing`, `e_robustness`, `f_scenarios` đọc từ `common.SEED_BANDS`; bỏ định nghĩa trùng trong `h_staffing.py`.
3. Test mới `tests/test_f4_seeds.py`:
   - tập seed thực tế của từng cặp chọn/đánh giá (sinh bằng đúng công thức trong mã) không giao nhau: (`select_day`, `eval_day`), (`screen_day`, `eval_day`), các bộ con của `nested_boot` với nhau và với `nested_nom`;
   - cặp (`select`, `eval`) **được đánh dấu `xfail` có lý do** ("trùng 11/300, giữ để không đổi số V5, xem KE_HOACH_V5_1 F4") — test nhắc việc này còn tồn tại thay vì giấu đi.
4. Sửa câu trong `g_report.write_mo_ta` ([g_report.py:311](../g_report.py#L311)): ghi đúng "trùng 11/300 lần lặp với seed chọn lịch".

**Quyết định cho cặp `select`/`eval` (optimize, M6):**
- **Phương án A (khuyến nghị trước bảo vệ):** giữ 50000, ghi chú trùng 11/300 và dẫn kết quả kiểm chứng seed tách hẳn (Phụ lục A, E2). Không đổi số nào.
- **Phương án B (sau bảo vệ / V6):** dời `eval` sang 5.000.000 → **mọi** số đánh giá đổi, phải cập nhật toàn bộ tài liệu.

**DoD:** `pytest tests/test_f4_seeds.py` pass (1 xfail có lý do); không còn hằng seed nào định nghĩa ngoài `common.SEED_BANDS` (`grep -n "SEED_" *.py`); chạy pipeline vào thư mục tạm cho CSV giống từng byte `final_v5` (F4 không đổi giá trị seed).

---

### F5. Đánh giá M7 bằng seed độc lập

**Hiện nay.** `p_day_levels` đánh giá lại lịch M7 bằng `seed=dx.SEED_EVAL` ([f_scenarios.py:411](../f_scenarios.py#L411)). Dải đánh giá 50.000–349.000 chồng 253/300 lần lặp với dải chọn 3.000–302.000; cùng model, lịch, CV ngày nên lần chạy giống hệt. Phần "đánh giá" thực chất là chạy lại trong mẫu, nên P bị lạc quan (winner's curse: lịch được chọn vì P cao trên chính các lần lặp đó).

**Bằng chứng (Phụ lục A, E4, E5):** P(SL ngày ≥ 90%), CV ngày train, Wilson 95%.

| Lịch | Giờ công | Báo cáo (seed 50000, trùng seed chọn) | Độc lập 300 lần lặp (9.000.000) | **Độc lập 2.000 lần lặp (20.000.000)** |
|---|:---:|---|---|---|
| Lịch 48 `[4,6,6,6,5,5,6,5,5]` | 48 | – | – | **0,9455 [0,9347; 0,9546]** |
| `[4,5,6,6,5,5,6,6,5]` (M7 theo ca, mức 0,80 và 0,90) | 48 | 0,950 [0,919] | 0,920 [0,884] | **0,9370 [0,9255; 0,9468]** |
| `[4,6,6,6,5,5,5,6,5]` (M7 quầy-giờ, mức 0,90) | 52 | 0,953 [0,923] | 0,920 [0,884] | **0,9415 [0,9303; 0,9510]** |
| `[5,6,6,6,6,5,5,6,5]` (M7 quầy-giờ, mức 0,95) | 52 | 0,980 [0,957] | 0,953 [0,923] | **0,9680 [0,9593; 0,9749]** |
| `[4,6,7,7,5,6,6,6,5]` (M7 theo ca, mức 0,95) | 52 | 0,993 [0,976] | – | **0,9885 [0,9828; 0,9923]** |

Hai nửa của dải 2.000 lần lặp (20.000.000 và 21.000.000, mỗi nửa 1.000) lệch nhau 1–2,5 điểm và **cùng chiều ở mọi lịch**: nhiễu chủ yếu đến từ mẫu hệ số nhân ngày $m_d$ (CRN giữa các lịch nên cùng lệch). Vì vậy 300 lần lặp không đủ để so với ngưỡng cách 2–4 điểm.

**Quyết định Q2 (đã chốt, xem [mục 10](#10-câu-hỏi-cần-chốt)):** chọn lịch như cũ (seed `select_day`, 300 lần lặp), **xác nhận** bằng `eval_day` 2.000 lần lặp độc lập; một mức `min_p` chỉ được nêu là đạt khi **cận dưới Wilson của lần xác nhận ≥ `min_p`**. Theo số ở bảng trên, kết luận giữ nguyên: ≥ 90% số ngày cần 48 giờ công (cận dưới ≥ 0,926); ≥ 95% cần 52 giờ công (48 giờ công có cận trên ≤ 0,955 nên không khẳng định được 95%).

**Cách làm.**
1. [f_scenarios.py:411](../f_scenarios.py#L411): `hs.p_day(model, lich, cv, seed=dx.SEED_EVAL)` → `hs.p_day(model, lich, cv, n_reps=2000, seed=common.SEED_BANDS["eval_day"][0])`.
2. Thêm Lịch 48 vào bảng đánh giá (cùng seed) để so theo cặp với lịch M7 ở 48 giờ công. Lịch M7 `[4,5,6,6,5,5,6,6,5]` được chọn vì P cao trên chính các lần lặp chọn; đánh giá độc lập cho thấy nó không tốt hơn Lịch 48 (0,937 so với 0,946). Vì vậy **khuyến nghị dùng một lịch duy nhất là Lịch 48** cho mức 90%, thay vì nêu thêm lịch M7 riêng.
3. Thêm cột `dat_muc_danh_gia` = `"Y"` nếu `P_ngay_danh_gia_low95 >= min_p`.
4. Cập nhật tài liệu (D7): README:556, `tong_hop.md` mục 1 và 7.10, báo cáo, slide, `PHAN_CONG.md` mục 1. Câu kết luận giữ nguyên, số P đổi sang số xác nhận, ví dụ: "Lịch 48 (48 giờ công): 94,6% số ngày đạt SLA [93,5%; 95,5%]".
5. Ghi hạn chế: P là xác suất **có điều kiện trên mô hình** (CV ngày 14%, tham số train); bất định tham số (S5) không nằm trong CI này.

**Thời gian chạy:** khoảng 7 lịch × 2.000 lần lặp ≈ 14.000 lần chạy một ngày; với pool song song khoảng 1–3 phút (rà soát chạy tuần tự vì pool hỏng do thiếu bộ nhớ ảo, mất lâu hơn nhiều; giữ `QS_WORKERS` ≤ 8).

**Đổi số:** chỉ các cột `P_ngay_danh_gia*` (và dòng Lịch 48 mới) của `toi_uu_xac_suat_ngay.csv`; lựa chọn lịch không đổi vì seed chọn không đổi. Các CSV khác phải giống từng byte.

**DoD:** test F4 cho cặp (`select_day`, `eval_day`) pass; với seed 20.000.000 và 2.000 lần lặp, `P_ngay_danh_gia` phải ra đúng các số ở cột cuối bảng trên (Lịch 48 = 0,9455); checker 0 lệch sau D7.

**Cải tiến tùy chọn (O3):** lấy mẫu phân tầng cho $m_d$ (lượng tử Gamma tại $(k + U_k)/n$, hoán vị ngẫu nhiên) để giảm phương sai do hệ số ngày; với cùng 2.000 lần lặp CI sẽ hẹp hơn. Đổi phương pháp nên chỉ làm sau bảo vệ.

---

### F6. Chốt định nghĩa SLA và bảng SL theo nhóm khách

**Hiện nay.**
- README:55 "Khách thường ≥ 90% … ≤ 5 phút", VIP ≤ 2 phút; README:58 "tính trên mọi khách đến"; README:401 "Pha 1 tăng quầy nếu SL thường hoặc SL VIP dưới mục tiêu".
- [dac_ta_mo_hinh.md:27-28](dac_ta_mo_hinh.md#L27-L28): khách thường (`vip = 0`) và VIP mỗi nhóm cận dưới CI ≥ 90%.
- `PHAN_CONG.md` mục 1 và mã: "≥ 90% khách được phục vụ trong ≤ 5 phút, tính trên mọi khách đến" — **gộp** VIP và thường. `is_schedule_feasible` chỉ xét `sl_ci95_low` gộp; SL VIP chỉ được báo cáo, không ràng buộc.

**Bằng chứng (Phụ lục A, E3):** cận dưới CI95 giờ tệ nhất, 300 lần lặp.

| Lịch | SL gộp ≤ 5 phút | SL khách thường ≤ 5 phút | SL VIP ≤ 2 phút |
|---|---|---|---|
| Lịch 45 `[4,5,6,5,5,5,5,5,5]` | 0,9236 (11h–12h) | **0,8997** (11h–12h) — 3 dải seed: 0,8997 / 0,8867 / 0,8932 | 0,9420 |
| Lịch 48 `[4,6,6,6,5,5,6,5,5]` | 0,9327 (15h–16h) | 0,9133 (15h–16h) — 3 dải seed: 0,9133 / 0,9130 / 0,9149 | 0,9425 |
| Mốc 6 quầy | 0,9494 | 0,9324 | 0,9658 |

**Cách làm.**
1. **Định nghĩa (Q1, đã chốt phương án A, xem [mục 10](#10-câu-hỏi-cần-chốt)):** SLA chính là SL gộp mọi khách (đúng như mã và mọi số V5). SL khách thường và SL VIP là chỉ số **giám sát**, báo cáo riêng. Câu chữ thay cho README §1.2 và `dac_ta_mo_hinh.md:27-28`:
   > **Cam kết dịch vụ (SLA):** trong từng khung giờ, cận dưới CI95 của SL(5 phút) ≥ 90%, với SL(t) = P(khách được phục vụ và chờ ≤ t) tính trên **mọi khách đến** (VIP và thường; khách bỏ về tính là không đạt).
   > **Chỉ số giám sát (không ràng buộc khi tối ưu):** SL(2 phút) của khách VIP và SL(5 phút) của riêng khách thường, theo giờ, báo cáo ở `sl_theo_nhom.csv`.

   README:401 bỏ cụm "hoặc `SL` VIP". Thêm hạn chế: "riêng khách thường, Lịch 45 không đạt 90% ở 11h–12h (cận dưới 0,887–0,900); Lịch 48 đạt (≥ 0,913)". Phương án B (SLA theo từng nhóm, tối ưu lại) để ở M9.
2. Thêm hàm `class_sl_table(model, policies)` (đặt trong `d_experiments.py`, gọi ở `run_optimize` sau bước O.5) sinh **tệp mới** `sl_theo_nhom.csv`, để không đổi cột của các CSV cũ:
   - mỗi (chính sách, giờ): SL gộp, SL khách thường (≤ 5 phút), SL VIP (≤ 2 phút), mỗi chỉ số có trung bình và cận dưới CI95;
   - cùng seed `eval` và 300 lần lặp như `so_sanh_chinh_sach.csv` để so sánh theo cặp;
   - hàm hậu xử lý phải ở cấp module (pickle được), mẫu: `post_class_sl` trong script kiểm chứng (Phụ lục C).
3. Thêm `sl_theo_nhom.csv` vào `FILE_DESC` của `g_report.py` và `required` của checker; thêm `check_class_sl` vào checker cho bảng mới trong `tong_hop.md`.

**Đổi số:** không đổi CSV cũ; thêm 1 tệp. Chạy lại chỉ cần giai đoạn `optimize`.

**DoD:** README, `dac_ta_mo_hinh.md`, `PHAN_CONG.md` cùng một định nghĩa; `sl_theo_nhom.csv` có số Lịch 45 khách thường 11h–12h = 0,8997 (cùng seed `eval`); test T5 "SL khách thường ≤ SL gộp" pass.

---

### F7. Đường dẫn `data/lam_sach.py` và test tái lập

**Hiện nay.** [data/lam_sach.py:11-12](../data/lam_sach.py#L11-L12) dùng `os.path.join(r"d:\KHDV", ...)`; thư mục này không tồn tại trên máy làm việc. Việc "chạy lại toàn bộ trên máy sạch" trong `PHAN_CONG.md` 3.1 sẽ hỏng ở bước này.

**Cách làm.**
1. ```python
   BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   def clean_data(raw_path=None, clean_path=None):
       raw_path = raw_path or os.path.join(BASE, "data", "raw", "September1999.txt")
       clean_path = clean_path or os.path.join(BASE, "data", "clean", "data_clean.csv")
   ```
2. Test `tests/test_f7_clean.py`: gọi `clean_data(clean_path=tmp_path / "x.csv")` rồi so với `data/clean/data_clean.csv` (`pd.testing.assert_frame_equal`). Bỏ qua (`skipif`) nếu không có tệp thô (xem F8). Đánh dấu `slow` nếu quá 10 giây.
3. Có thể thay `df.apply(get_arrival_seconds, axis=1)` bằng phép vector hóa, nhưng **chỉ khi** test vẫn khớp.

**DoD:** `python data/lam_sach.py` chạy được từ bất kỳ thư mục làm việc nào; test khớp (rà soát đã xác nhận: 9.836 × 8, trùng khớp từng giá trị).

---

### F8. Điều khoản phân phối lại dữ liệu thô

**Hiện nay.** `gh repo view`: repo `LgTVing/queue-simulation` là **PUBLIC**, chứa `data/raw/September1999.txt`, `October1999.txt`, `AnonymousBank.rar`, `AnonymousBank.pdf`. README 3.2 ghi điều kiện: thông báo GS Mandelbaum và ghi nguồn; chưa rõ có cho phép phân phối lại hay không.

**Điều khoản tìm được (2026-11-02):** tài liệu gốc `AnonymousBank.pdf` (Guedj và Mandelbaum, 2000) ghi: *"The data is free for use. If used, please notify Avi Mandelbaum, at avim@ie.technion.ac.il and do acknowledge the data source in any of your work."* Không có điều khoản nào về phân phối lại; trang `see-center.iem.technion.ac.il/databases/AnonymousBank/` chỉ là danh sách tệp. Tệp `AnonymousBank.pdf` (35.223 byte) và `AnonymousBank.rar` (10.625.021 byte) trong repo trùng kích thước từng byte với bản công khai tại `.../AnonymousBank/Data/`.

**Quyết định Q3 (đã chốt, xem [mục 10](#10-câu-hỏi-cần-chốt)):** dùng là được phép; phân phối lại bản thô thì chưa được phép rõ ràng. Vậy: **không giữ bản thô trong repo, giữ dữ liệu đã làm sạch kèm ghi nguồn, hỏi xin phép**.

**Cách làm.**
1. **Gửi email thông báo ngay** (điều kiện bắt buộc của nguồn, README 3.2), đồng thời hỏi xin phép giữ dữ liệu trong repo môn học công khai. Lưu email và trả lời vào `docs/lich_su/`.
2. Commit mới: `git rm` các tệp `data/raw/*.txt`, `*.rar`, `*.pdf`; thêm `data/raw/*` vào `.gitignore` (trừ `data/raw/README.md`). Các thành viên giữ bản trên máy.
3. Thêm `data/raw/README.md`: đường dẫn tải chính thức, tên tệp và kích thước để kiểm tra, cách giải nén lấy `September1999.txt`, câu ghi nguồn.
4. **Giữ `data/clean/data_clean.csv`** (tập con đã xử lý, 465 KB): pipeline, test và CI chỉ cần tệp này; thêm dòng ghi nguồn ở đầu `docs/mo_ta_du_lieu.md`. Nếu người quản lý dữ liệu trả lời không đồng ý thì gỡ cả tệp này.
5. **Không viết lại lịch sử git:** chính bản này vẫn được Technion công khai nên không tăng mức lộ; viết lại lịch sử làm hỏng nhánh và bản clone của cả nhóm. Chỉ làm nếu người quản lý dữ liệu yêu cầu.
6. Test F7 tự `skip` khi thiếu tệp thô.

**DoD:** `git ls-files data/raw` chỉ còn `README.md`; email đã gửi; `pytest -q` và CI vẫn xanh.

---

### T4. Test `poisson_label` kiểm đúng hàm thật

**Hiện nay.** [tests/test_v2_features.py](../tests/test_v2_features.py) tự định nghĩa `poisson_label` rồi kiểm chính nó; `a_data.poisson_label` không được kiểm.

**Cách làm.** Xóa hàm cục bộ, `from a_data import poisson_label`. Giữ nguyên các assert.

**DoD:** sửa thử ngưỡng trong `a_data.poisson_label` thì test đỏ.

---

## 4. Giai đoạn 2 — Cải thiện

### F9. Seed bootstrap lồng nhau S5

**Hiện nay.** `nested_bootstrap` ([e_robustness.py:312](../e_robustness.py#L312)) dùng `seed_base = 60000 + b*100`, mỗi lần lặp `+ 1000·i` với R = 60 → bộ `b` và `b + 10` dùng chung 59/60 seed; 3.000 cặp chỉ có 640 seed khác nhau. Bản danh nghĩa `seed_base = 90000` cũng trùng. Phân rã phương sai giả định nhiễu mô phỏng độc lập giữa các bộ; nhiễu tương quan làm `Var_total` nhỏ đi nên phần "do tham số" bị ước lượng thấp (hướng sai lệch dự đoán, chưa đo).

**Cách làm.** `seed_base = 60_000_000 + b * 100_000` (R ≤ 100 thì dải mỗi bộ ≤ 99.000 < 100.000), danh nghĩa `70_000_000`. Đăng ký trong `SEED_BANDS`.

**Đổi số:** `bat_dinh_nested.csv`, `phan_ra_phuong_sai.csv` → `tong_hop.md` mục 3.3, báo cáo mục liên quan.

**DoD:** test F4 cho S5 pass; bảng trước/sau trong `doi_chieu_v5_v5_1.csv`.

---

### S16. p-value ngoài mẫu S6 từ phân phối mô phỏng

**Hiện nay.** [e_robustness.py:376-377](../e_robustness.py#L376-L377): `se = sqrt(mu(1-mu)/n_h)` coi mọi khách là Bernoulli độc lập, bỏ qua tương quan trong ngày và biến động ngày. Hệ quả trong `ngoai_mau.csv`: 8h–9h và 9h–10h `trong_PI95 = Co` nhưng `lech_co_y_nghia = Co`.

**Cách làm.**
1. Dùng chính `sim_sl[:, h]` (K bộ 4 ngày mô phỏng đã có): `p = 2 * min(mean(sim >= obs), mean(sim <= obs))`, chặn dưới `1/K`.
2. Holm–Bonferroni như cũ trên p mới.
3. Giữ cột cũ đổi tên `raw_p_value_nhi_thuc` để đối chiếu, hoặc bỏ hẳn (ghi trong bảng trước/sau).

**Đổi số:** `ngoai_mau.csv` (p-value, nhãn) → `tong_hop.md` mục 5, `docs/ngoai_mau.md`.

**DoD:** không còn giờ nào vừa "trong PI95" vừa "lệch có ý nghĩa" ở mức 5% (hai tiêu chí cùng dựa trên một phân phối nên phải nhất quán); test trên dữ liệu giả lập: quan sát bằng trung vị mô phỏng → p ≈ 1.

---

### F10. Cờ khả thi cho bộ tối ưu và SIPP

**Hiện nay.**
- `optimize_schedule` ([c_sim.py:813-878](../c_sim.py#L813-L878)): Pha 1 dừng sau 25 bước hoặc khi chạm `c_cap` vẫn trả lịch như bình thường, không báo không khả thi.
- `sipp_schedule` ([b_theory.py:174-175](../b_theory.py#L174-L175)): không tìm thấy c trong 40 giá trị thì âm thầm trả `c_start + 5`.

**Cách làm.** Trả thêm `"feasible": bool` trong kết quả `optimize_schedule` (kiểm tra lại `final_eval`); `d_experiments.optimize` in cảnh báo khi `False`. `sipp_schedule` in cảnh báo (hoặc `warnings.warn`) ở nhánh fallback. Không đổi giá trị trả về cũ.

**DoD:** test model quá tải với `c_cap = 2` → `feasible is False`; pipeline cho CSV giống từng byte.

---

### F11. Đếm khách chưa xử lý xong khi cắt mô phỏng

**Hiện nay.** `env.run(until=total_time + 1000.0)` ([c_sim.py:311](../c_sim.py#L311)); khách chưa phục vụ xong hoặc chưa bỏ về không có bản ghi, nên bị loại khỏi mẫu số và SL bị thổi cao. Chỉ xảy ra khi hệ quá tải và θ = 0 (không xảy ra với các lịch hiện có).

**Cách làm.** Đếm `cid` đã sinh trừ số bản ghi, ghi `df.attrs["n_unfinished"]`; `run_reps` cảnh báo nếu tổng > 0. Không đổi kết quả khi bằng 0.

**DoD:** test model θ = 0, ρ > 1 → `n_unfinished > 0`; pipeline giống từng byte.

---

### F12. Dọn nợ kỹ thuật nhỏ

| Việc | Vị trí | Đổi số? |
|---|---|---|
| `eval(...)` → `ast.literal_eval(...)` | [h_staffing.py:99](../h_staffing.py#L99), [f_scenarios.py:377](../f_scenarios.py#L377) | Không |
| `0.90` cứng → `target_sla` | [c_sim.py:528](../c_sim.py#L528), [:535](../c_sim.py#L535) | Không (cùng giá trị) |
| `"Train" if i < 10` → theo `df_train["day"]` | [e_robustness.py:401](../e_robustness.py#L401) | Không |
| `60.0` cứng → `common.DEFAULT_HOUR_LEN` | `a_data.fit_arrivals`, `lambda_ci_table`, `poisson_overdispersion` | Không |
| `"version": "v4.0"` → `"v5.1"` | [a_data.py:213](../a_data.py#L213) | `params.json` (chỉ metadata) |
| `save_schedules` giữ khóa cũ khi M6 không tìm thấy lịch | [f_scenarios.py:376-377](../f_scenarios.py#L376-L377) | Không (xóa khóa `toi_uu_theo_ca` khi không có lịch) |
| `_CACHE` khóa theo `id(model)` | [h_staffing.py:139](../h_staffing.py#L139) | Không (đổi sang khóa nội dung như O1, hoặc ghi chú giả định model sống suốt giai đoạn) |
| `test_holm_bonferroni_adjustment` chỉ kiểm `adj ≥ raw` | `tests/test_v2_features.py` | Không (thêm assert giá trị `[0.04, 0.09, 0.09, 0.80]`) |

---

### T5. Bộ test bổ sung

| Test | Kỳ vọng | Module | Gắn với |
|---|---|---|---|
| Các cặp dải seed chọn/đánh giá | Giao = ∅ (trừ `select`/`eval` xfail) | `common.SEED_BANDS` | F4 |
| SL khách thường ≤ SL gộp ≤ SL VIP cùng ngưỡng, hệ tải cao, `p_vip = 0.35` | Bất đẳng thức đúng | `c_sim` | F6 |
| `optimize_schedule` quá tải, `c_cap` nhỏ | `feasible is False` | `c_sim` | F10 |
| Surge: hàng chờ về 0, chờ `min_hold` | `state.extra == 0`, số quầy bận ≤ lịch | `c_sim.surge_monitor` | – |
| `rep_stats` có giờ không khách | `sl = 1.0`, không lỗi chia 0 | `c_sim` | – |
| `erlang_a` với θ = 1e-9 | Gần `mmc` (sai số < 1e-4) | `b_theory` | – |
| `lam_sach.clean_data` vào `tmp_path` | Khớp `data_clean.csv` | `data/lam_sach.py` | F7 |
| S6 quan sát = trung vị mô phỏng | p ≈ 1, không "lệch" | `e_robustness` | S16 |

---

## 5. Giai đoạn 3 — Tối ưu hiệu năng

Thời gian hiện nay (`results/final_v5/thoi_gian_chay.json`): `optimize` 9,8 phút, `robust` 5,0 phút, tổng 15,1 phút; smoke test `--reps-scale 0.02` mất 9–13 phút (`pytest_log.txt`: cả bộ 557 giây). **Mọi việc ở giai đoạn này phải cho CSV giống từng byte.**

### O1. Bộ nhớ đệm kết quả `run_reps`

**Hiện nay.** Nhiều thí nghiệm chạy lại đúng cùng cấu hình (cùng model, lịch, số lần lặp, seed), ví dụ:
- `abandonment_constraint` mức `cap=None` lặp lại nguyên `optimize(model)` của bước O.1 ([f_scenarios.py:94](../f_scenarios.py#L94));
- `service_model_comparison`, S12 (kiên nhẫn mũ), S15 (theo giờ) đánh giá lại Lịch 45/48 bằng seed `eval`, trùng bước O.5;
- `optimize_schedule` đánh giá lại lịch cuối ([c_sim.py:873](../c_sim.py#L873)) dù đã đánh giá ở bước chấp nhận cuối cùng;
- M6 thử lại các lịch đã chạy trong optimize với cùng seed `select`.

**Cách làm.**
1. Trong `c_sim.run_reps`: khóa = `hashlib.sha1(pickle.dumps((model, tuple(schedule), n_reps, run_time, warm_up, seed_base, day_cv, drain_policy, keep_reps))).hexdigest()`; lưu trong dict cấp module; trả `copy.deepcopy` để nơi gọi không sửa được bản trong cache.
2. Bật/tắt bằng biến môi trường `QS_CACHE` (mặc định bật); test so sánh bật/tắt.
3. Lưu ý: `dataclasses.replace(model, theta=1.0 / (1.0 / theta))` có thể khác bit cuối → cache trượt, vẫn đúng, chỉ không tiết kiệm.
4. Có thể bỏ `_CACHE` riêng của `h_staffing` sau khi O1 xong.

**Ước lượng tiết kiệm:** chưa đo; kỳ vọng 1–3 phút ở `optimize`. Đo bằng `thoi_gian_chay.json` trên máy rảnh, 3 lần, lấy trung vị.

**DoD:** `diff -rq` thư mục tạm với `final_v5` không khác (ngoài các tệp metadata); test `QS_CACHE=0` và `=1` cho kết quả `run_reps` bằng nhau.

### O2. Rút thời gian smoke test

**Hiện nay.** Ở `--reps-scale 0.02`, CI rất rộng nên M6 và M7 duyệt nhiều mức giờ công, chiếm phần lớn 9–13 phút.

**Cách làm.** Thêm tham số `max_levels` (số mức giờ công tối đa duyệt) cho `optimize_shift_staffing` và `optimize_p_day_shifts`, đọc từ biến môi trường `QS_SMOKE=1` chỉ trong smoke test. Không đổi hành vi khi không đặt biến.

**DoD:** smoke test < 5 phút; pipeline đầy đủ giống từng byte.

---

## 6. Giai đoạn 4 — Mở rộng

### M9. Tùy chọn tối ưu theo SLA khách thường (tùy chọn)

**Mục đích:** trả lời câu hỏi "nếu SLA tính riêng khách thường như đặc tả thì cần bao nhiêu quầy-giờ?".

**Cách làm.** `is_schedule_feasible(..., scope="all" | "regular")`; `rep_stats` thêm `sl_reg` theo giờ; `run_reps` thêm `sl_reg_ci95_low`. Mặc định `"all"` để giữ số V5. Chạy `optimize(model, scope="regular")` và đánh giá bằng seed `eval`, ghi `toi_uu_sla_khach_thuong.csv`.

**Kỳ vọng (chưa kiểm chứng):** lịch tối ưu tăng lên khoảng 46–48 quầy-giờ (Lịch 45 hụt 11h–12h; Lịch 48 đạt).

**DoD:** test mặc định giống từng byte; bảng mới trong `tong_hop.md` mục 7.

### D5. Trang HTML demo SIPP (đã có trong `PHAN_CONG.md` 3.2)

Bổ sung kỹ thuật:
- Ma trận Q của Erlang-A là hai đường chéo (tam giác dưới) nên `expm` tính được trong JS bằng **uniformization** (chuỗi Poisson, cắt khi phần dư < 1e-12), không cần thư viện ma trận.
- Không đưa SimPy hay bộ tối ưu vào demo; chỉ lý thuyết, tính tức thì.
- DoD giữ như cũ: khớp `bang_sipp.csv` đến 3 chữ số với tham số train.

### D6. Slide và tập dượt

Thêm vào phụ lục Q&A hai câu do rà soát phát hiện, kèm câu trả lời lấy từ v5.1:
1. "SLA tính gộp hay riêng khách thường? Nếu riêng thì Lịch 45 còn đạt không?" → `sl_theo_nhom.csv` (F6).
2. "Xác suất đạt SLA theo ngày được đánh giá độc lập chưa?" → `toi_uu_xac_suat_ngay.csv` sau F5.

### Kiểm chứng kiểu "phát lại" theo vết dữ liệu (để sau)

Mô phỏng từng ngày test với dòng khách thật và số nhân viên ước lượng, so với SL quan sát. Chỉ có ý nghĩa nếu biết số nhân viên thật; hiện chỉ có cận dưới số phiên chồng lấn (`nhan_vien_uoc_luong.csv`), nên chưa nên làm.

---

## 7. Chạy lại và cập nhật tài liệu (R5, D7)

### R5. Cập nhật `final_v5` thành v5.1

**Quyết định:** cập nhật tại chỗ trong `results/final_v5/` (không tạo thư mục mới, để không phải đổi mọi đường dẫn trong tài liệu và `common.RESULTS_VERSION`), nhưng **lưu bản cũ của các tệp sẽ đổi** trước khi chạy.

1. Trước khi chạy: sao các tệp sẽ đổi sang `results/archive/final_v5_0/`: `toi_uu_xac_suat_ngay.csv`, `bat_dinh_nested.csv`, `phan_ra_phuong_sai.csv`, `ngoai_mau.csv`, `params.json`, `lich_khuyen_nghi.json`, `MO_TA.md`, `thoi_gian_chay.json`. Ghi `results/archive/final_v5_0/MO_TA.md` (nguồn: commit `116fdcc`).
2. Chạy `python main.py --stage all --reps-scale 1.0` (khoảng 15 phút; máy bận có thể lâu hơn; pool hỏng thì giảm `QS_WORKERS`).
3. `diff -rq results/archive/final_v5_0 results/final_v5` và `git diff --stat results/final_v5`: **chỉ** các tệp ở bước 1 và tệp mới (`sl_theo_nhom.csv`, `doi_chieu_v5_v5_1.csv`) được khác. Khác ở tệp nào khác là lỗi, phải tìm nguyên nhân trước khi đi tiếp.
4. Sinh `results/final_v5/doi_chieu_v5_v5_1.csv`: mỗi chỉ số bị đổi, giá trị cũ, giá trị mới, nguyên nhân (F5, F9, S16). Có thể viết một hàm nhỏ trong `g_report.py` đọc `results/archive/final_v5_0/` bằng cùng cách đọc của `metrics()`; thêm vào `FILE_DESC` và `required` của checker.
5. `pytest -q > results/final_v5/pytest_log.txt`.
6. Commit `results(R5): cập nhật final_v5 lên v5.1`.

### D7. Cập nhật tài liệu

Làm theo thứ tự; sau mỗi tệp chạy `python tools/check_consistency.py`.

| Tệp | Mục cần sửa | Do việc |
|---|---|---|
| `tong_hop.md` | Mục 1 (bảng quyết định, câu kết luận M7); 3.3 (S5); 5 (S6); 7.10 (M7, thêm cột đánh giá độc lập); mục mới "SL theo nhóm khách" (F6); 8 (thêm đối chiếu v5 → v5.1); 9 (số test, thời gian); 10 (hạn chế: SLA khách thường, seed trùng 11/300) | F5, F6, F9, S16 |
| `README.md` | §1.2 và dòng 58 (định nghĩa SLA); §11.1 dòng 401 (bỏ "hoặc SL VIP" nếu chọn phương án A); §15.5 dòng 556 (M7) | F5, F6 |
| `docs/dac_ta_mo_hinh.md` | Dòng 27–28 (SLA) | F6 |
| `docs/bao_cao_tong_ket.md` | Mục SLA, M7, S5, S6, hạn chế | F5, F6, F9, S16 |
| `docs/slide_thuyet_trinh.md` | Slide M7, kết luận, phụ lục Q&A (2 câu mới) | F5, F6 |
| `docs/ngoai_mau.md` | Phần kiểm định S6 | S16 |
| `docs/PHAN_CONG.md` | Mục 1: định nghĩa SLA, câu "≥ 95% cần 52 giờ công" | F5, F6 |
| `docs/mo_ta_du_lieu.md` | Điều khoản dữ liệu, cách chạy `lam_sach.py` | F7, F8 |
| `tools/check_consistency.py` | `required` thêm 2 tệp; `check_class_sl`; cập nhật `check_p_day`, `check_out_of_sample` nếu cột đổi; `_expected_report_strings` nếu báo cáo/slide thêm số | F5, F6, S16 |
| `CHANGELOG.md` | Mục `v5.1` | tất cả |
| `docs/KE_HOACH_V5_1.md` | Bảng trạng thái | tất cả |

Commit `docs(D7): cập nhật tài liệu theo v5.1`.

---

## 8. Checklist

### Mỗi PR
- [ ] Một mã việc mỗi commit/PR; tiêu đề có mã (F5, S16…).
- [ ] `pytest -q -m "not slow"` pass; có test mới cho việc này.
- [ ] Việc "không đổi số": đã `diff -rq` thư mục tạm với `results/final_v5/`, không khác.
- [ ] Việc "đổi số": có dòng trong `doi_chieu_v5_v5_1.csv` kèm nguyên nhân.
- [ ] Seed mới đăng ký trong `common.SEED_BANDS`, test F4 pass.
- [ ] Hàm mới có docstring nêu thí nghiệm, số lần lặp, dải seed, tệp đầu ra.
- [ ] `python tools/check_consistency.py` pass.

### Bàn giao v5.1
- [ ] F4: không còn hằng seed ngoài sổ đăng ký; test cặp chọn/đánh giá pass (1 xfail có lý do).
- [ ] F5: kết luận M7 dựa trên đánh giá độc lập, có CI.
- [ ] F6: một định nghĩa SLA trong mọi tài liệu; có `sl_theo_nhom.csv`.
- [ ] F7: `lam_sach.py` chạy được, test tái lập pass.
- [ ] F8: có câu trả lời về điều khoản dữ liệu.
- [ ] R5: `doi_chieu_v5_v5_1.csv`, bản cũ trong `results/archive/final_v5_0/`, `pytest_log.txt` mới.
- [ ] D7: checker 0 lệch; `CHANGELOG.md` có `v5.1`.
- [ ] CI xanh trên `feat/v5.1`.

---

## 9. Không nên làm lúc này

| Việc | Lý do |
|---|---|
| Dời `SEED_EVAL` (phương án B của F4) trước bảo vệ | Đổi mọi số đánh giá, khối lượng tài liệu lớn; tác động đo được nhỏ (E2) |
| Tối ưu lại theo SLA từng nhóm (phương án B của F6) trước bảo vệ | Đổi lịch chính; làm M9 như phân tích bổ sung thay vì đổi mô hình chính |
| Viết lại bộ tối ưu (OCBA, ranking & selection, metaheuristic) | Bài toán 9 biến; tham lam + Pha 3 đã kiểm tra tối thiểu cục bộ; kết quả ổn định khi đổi seed |
| Thêm kịch bản thống kê mới (S17 trở đi) | Mỗi kịch bản thêm tài liệu và thời gian chạy; giá trị biên thấp |
| Đưa SimPy vào trang demo, biến dự án thành web app | Ngoài mục tiêu môn học; demo lý thuyết là đủ |
| Đóng băng thư mục mới `final_v6` | v5.1 cập nhật tại chỗ có lưu bản cũ là đủ cho phạm vi thay đổi này |

---

## 10. Câu hỏi cần chốt

| # | Câu hỏi | Đề xuất (đã chốt trong kế hoạch) | Lý do chính | Còn cần ai xác nhận |
|---|---|---|---|---|
| Q1 | SLA chính tính gộp mọi khách hay riêng khách thường / VIP? | **Gộp mọi khách** là SLA chính; SL khách thường và SL VIP là chỉ số giám sát (F6) | (1) Khớp mã và mọi số V5. (2) Lý thuyết Erlang C/A và SIPP không tách nhóm, nên chuỗi lý thuyết → kiểm chứng → tối ưu chỉ nhất quán với định nghĩa gộp. (3) Khuyến nghị cuối (Lịch 48) đạt **cả hai** định nghĩa, nên chọn gộp không làm yếu kết luận. (4) Tối ưu lại theo từng nhóm sẽ đổi lịch tối ưu 45 dùng khắp tài liệu, kể cả M8. | Giảng viên (nếu đề bài bắt buộc tách nhóm thì làm M9) |
| Q2 | Kết luận M7 dựa trên tiêu chí lúc chọn hay cả đánh giá độc lập? | **Chọn rồi xác nhận độc lập 2.000 lần lặp; nêu "đạt mức" chỉ khi cận dưới Wilson của lần xác nhận ≥ mức** (F5) | Tách chọn/đánh giá loại winner's curse; 2.000 lần lặp đủ hẹp (±1 điểm) để không quá bảo thủ. Kết quả: kết luận 48 / 52 giờ công giữ nguyên, Lịch 48 là lịch duy nhất cho mức 90%. | Không |
| Q3 | Dữ liệu thô có được để trong repo công khai không? | **Gỡ bản thô khỏi repo (commit mới, không viết lại lịch sử), giữ `data_clean.csv` kèm ghi nguồn, gửi email thông báo và xin phép** (F8) | Điều khoản chỉ cho phép dùng và yêu cầu thông báo, ghi nguồn; không nói về phân phối lại. Bản thô đã công khai tại Technion nên tải lại dễ. | Người quản lý dữ liệu (trả lời email) |
| Q4 | Có cần đóng băng lại (`final_v6`) hay cập nhật tại chỗ v5.1 là đủ? | Cập nhật tại chỗ, lưu bản cũ các tệp đổi vào `results/archive/final_v5_0/` (R5) | Phạm vi đổi số nhỏ (M7, S5, S6) | Cả nhóm |

---

## Phụ lục A — Số liệu kiểm chứng của rà soát

Tất cả chạy ngày 2026-11-02 trên `feat/v5` (`116fdcc`), Python 3.12.10, SimPy 4.1.2, NumPy 2.5.4, SciPy 1.18.1, pandas 3.1.0; tham số đọc từ `results/final_v5/params.json`, mô hình chính (phục vụ thực nghiệm từ train).

**Test và checker**

| Kiểm tra | Kết quả |
|---|---|
| `pytest -q -m "not slow"` | 83 passed, 34 giây |
| `pytest -q -m slow` (smoke test `--reps-scale 0.02`, thư mục tạm) | 1 passed, 12 phút 48 giây (máy đang chạy việc khác) |
| `python tools/check_consistency.py` | 1.502 giá trị `tong_hop.md` + 132 giá trị báo cáo/slide/README khớp |
| GitHub Actions `feat/v5` (3 lần gần nhất) | success |
| `data/lam_sach.py` với đường dẫn sửa, ghi ra thư mục tạm | 9.836 × 8, khớp `data_clean.csv` từng giá trị |
| Dữ liệu thô lúc 8:00 (14 ngày, PS) | trung bình 0 khách đang chờ, 1,43 khách đang phục vụ |

**E1 — Giao giữa các dải seed**

| Cặp | Số seed chung |
|---|---|
| optimize chọn (1000, 60 lần lặp) ∩ đánh giá (50000, 300) | 11; lần lặp chọn 49–59 giống hệt lần lặp đánh giá 0–10 (`np.array_equal` = True) |
| M7 chọn (3000, 300) ∩ đánh giá (50000, 300) | 253 |
| S5: 50 bộ × 60 lần lặp | 3.000 cặp, 640 seed khác nhau |

**E2 — Đánh giá lại bằng seed tách hẳn (`seed_base = 7.000.000`, 300 lần lặp)**

| Lịch | SL ngày | Giờ tệ nhất (cận dưới CI95) | Số đang báo cáo |
|---|---|---|---|
| Lịch 45 | 0,9429 | 0,9144 (11h–12h) | 0,9423; 0,9236 |
| SIPP Erlang-A (44) | 0,9376 | 0,9059 (16h–17h) | 0,9369; 0,9044 |
| Lịch 48 | 0,9596 | 0,9326 (15h–16h) | 0,9579; 0,9327 |

Giờ tệ nhất dao động khoảng ±0,01 theo dải seed: số 4 chữ số thập phân trong tài liệu nên đi kèm ghi chú độ dao động (M5 đã có phân tích này).

**E3 — SL theo nhóm khách** (seed 50000, 300 lần lặp; kiểm tra thêm ở seed 7.000.000 và 8.000.000): xem bảng ở [F6](#f6-chốt-định-nghĩa-sla-và-bảng-sl-theo-nhóm-khách). SL khách thường cả ngày: Lịch 45 0,9260; Lịch 48 0,9465; mốc 6 quầy 0,9704.

**E4 — M7 đánh giá độc lập, 300 lần lặp** (CV ngày train, seed 9.000.000): xem bảng ở [F5](#f5-đánh-giá-m7-bằng-seed-độc-lập).

**E5 — M7 đánh giá độc lập, 2 × 1.000 lần lặp** (seed 20.000.000 và 21.000.000; gộp lại chính là `eval_day` 2.000 lần lặp):

| Lịch | Giờ công | Dải 20.000.000 | Dải 21.000.000 | Gộp 2.000 |
|---|:---:|---|---|---|
| Lịch 48 `[4,6,6,6,5,5,6,5,5]` | 48 | 0,958 [0,944; 0,969] | 0,933 [0,916; 0,947] | 0,9455 [0,9347; 0,9546] |
| `[4,5,6,6,5,5,6,6,5]` | 48 | 0,947 [0,931; 0,959] | 0,927 [0,909; 0,942] | 0,9370 [0,9255; 0,9468] |
| `[4,6,6,6,5,5,5,6,5]` | 52 | 0,955 [0,940; 0,966] | 0,928 [0,910; 0,942] | 0,9415 [0,9303; 0,9510] |
| `[5,6,6,6,6,5,5,6,5]` | 52 | 0,978 [0,967; 0,985] | 0,958 [0,944; 0,969] | 0,9680 [0,9593; 0,9749] |
| `[4,6,7,7,5,6,6,6,5]` | 52 | 0,993 [0,986; 0,997] | 0,984 [0,974; 0,990] | 0,9885 [0,9828; 0,9923] |

Lần chạy này pool tiến trình hỏng ("paging file is too small") và tự chạy lại tuần tự; kết quả không đổi vì seed gắn theo job.

---

## Phụ lục B — Dải seed đang dùng

Mỗi lần lặp của `run_reps` dùng `seed_base + 1000·i`. "Chung giữa cấu hình khác nhau" là CRN, không phải lỗi; chỉ cặp chọn/đánh giá của **cùng** cấu hình mới làm sai lệch.

| Thí nghiệm | Vị trí | seed_base / công thức | Lần lặp | Dải | Ghi chú |
|---|---|---|:---:|---|---|
| Tối ưu 2 pha, Pha 3, M1–M3, S12, S15 chọn lịch | `d_experiments.optimize` | 1000 | 60 | 1.000–60.000 | |
| Đánh giá chính sách | `d_experiments.evaluate` | 50000 | 300 | 50.000–349.000 | **trùng 11 với chọn** |
| M6 chọn / xác nhận | `h_staffing` | 1000 / 50000 | 60 / 300 | như trên | trùng 11 |
| M6 độ bền | `h_staffing._confirm` | 81000 (CV ngày), 131000 (+10%) | 300 / 150 | 81.000–380.000 | cấu hình khác, không ảnh hưởng |
| M7 chọn | `h_staffing.p_day` | 3000 | 300 | 3.000–302.000 | |
| M7 sàng lọc | `h_staffing.optimize_p_day_shifts` | 503000 | 100 | 503.000–602.000 | |
| M7 đánh giá | `f_scenarios.p_day_levels` | 50000 | 300 | 50.000–349.000 | **trùng 253 với chọn**; F5 đổi sang 20.000.000, 2.000 lần lặp (20.000.000–21.999.000) |
| Độ nhạy | `e_robustness.sensitivity` | 80000 | 150 | 80.000–229.000 | CRN giữa các mức, cố ý |
| S2 | `conditional_expectation` | 20000 + 1000k + r | K × R | | |
| S3 | `cv_day_sensitivity` | 50000 + int(cv·100) + 1000k + r | | | |
| S4 | `volume_threshold` | 30000 + 10000k + 10V + r | | | |
| S5 | `nested_bootstrap` | 60000 + 100b; danh nghĩa 90000 | 60 | 60.000–149.000 | **640 seed / 3.000 cặp** |
| S6 | `out_of_sample` | 54321 + 10k + d | | | |
| S7 | `fourteen_days` | 10000(k+1) + 100d + r | | | |
| S9 | `service_dist_sensitivity` | 45000 | 150 | | CRN giữa phân phối, cố ý |
| S11 | `cost_analysis` | 70000 | 150 | | CRN giữa chính sách, cố ý |
| M5 | `worst_hour_stability` | 100000 (pilot), 600000 | 300 / ≤ 3000 | | |
| M8 | `surge_policies` | 400000 + 100000k; 14 ngày 1.300.000 + 100d | 300 / 40 | | CRN giữa chính sách, cố ý |
| Kiểm chứng | `chay_kiem_chung` | 101, 202, 303+, 404, 77000 | 30–60 | | |

---

## Phụ lục C — Lệnh tái hiện kiểm chứng

Các script rà soát chỉ đọc dữ liệu, không ghi vào repo. Muốn tái hiện, đặt script ngoài repo và chạy từ thư mục repo:

```bash
# Test và checker
pytest -q -m "not slow"
python tools/check_consistency.py

# Seed trùng (E1): lần lặp chọn 49-59 giống lần lặp đánh giá 0-10
python - <<'EOF'
import json, numpy as np, common, a_data, c_sim as sim
p = json.load(open("results/final_v5/params.json", encoding="utf-8"))
tr, _ = a_data.split_train_test(a_data.load_log(), 0.7)
m = a_data.build_model(p, a_data.train_service_samples(tr))
s = [4, 5, 6, 5, 5, 5, 5, 5, 5]
a = sim.run_reps(m, s, n_reps=60, seed_base=1000, keep_reps=True)["rep_sl_day"][49:]
b = sim.run_reps(m, s, n_reps=11, seed_base=50000, keep_reps=True)["rep_sl_day"]
print(np.array_equal(a, b))   # True
EOF
```

Hàm hậu xử lý SL theo nhóm khách dùng cho E3 (mẫu cho F6, phải đặt ở cấp module để pickle được khi chạy song song):

```python
def post_class_sl(df, sched):
    """SL theo gio: gop (<= 5 phut), khach thuong (<= 5 phut), VIP (<= 2 phut)."""
    H = len(sched)
    out = np.full((3, H), np.nan)
    hr, srv = df["hour"].to_numpy(), df["served"].to_numpy() == 1
    w, vip = df["wait"].to_numpy(dtype=float), df["vip"].to_numpy() == 1
    for h in range(H):
        m = hr == h
        for k, (mask, thr) in enumerate(((m, 5.0), (m & ~vip, 5.0), (m & vip, 2.0))):
            if mask.any():
                out[k, h] = np.mean(srv[mask] & (w[mask] <= thr))
    return out
```
