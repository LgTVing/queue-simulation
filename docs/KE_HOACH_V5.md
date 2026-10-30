# KẾ HOẠCH PHÁT TRIỂN V5

**Ngày lập:** 2026-10-29  
**Điểm xuất phát:** commit `6a1083d` trên nhánh `feat/v4`. V4 đã đóng băng tại `results/final_v4/` và mọi tài liệu đã đồng bộ. Kế hoạch V4 (`docs/KE_HOACH_CAI_TIEN.md`) đã hoàn tất.  
**Mục đích:** củng cố kết luận chính ("bao nhiêu quầy, tổ chức ca thế nào") và rút thời gian chạy pipeline từ 33 phút xuống dưới 10 phút. Không làm thay đổi kết quả V4 khi chưa chủ đích.  
**Cập nhật trạng thái:** 2026-10-30, nhánh `feat/v5`; R4 và D4 đã xong (commit `results(R4): ...`, `docs(D4): ...`).

---

## Trạng thái (cập nhật 2026-10-30)

### Đã làm

| Mã | Commit | Kết quả chính | Khác kế hoạch / lưu ý |
|---|---|---|---|
| P1 | `6978fcb` | Chạy song song bằng `c_sim.map_sim`; bộ sinh phục vụ đổi sang class pickle được. Pipeline 33.3 → 5.5–6.5 phút; CSV và hình giống từng byte với `final_v4`. | Mặc định `min(CPU − 1, 8)` tiến trình (19 tiến trình làm hết RAM, pool hỏng); pool hỏng thì tự chạy lại tuần tự. |
| P2 | `17a9f6d` | `rep_stats` dùng NumPy: 0.82 → 0.06 s/60 lần lặp; đo A/B cùng điều kiện máy pipeline 9.0 → 6.55 phút; vẫn giống từng byte. | Thời gian tuyệt đối dao động theo tải máy (5.5–9 phút cho cùng code). |
| T2 | `8d97391` | `check_report_numbers()` đối chiếu 132 số trong báo cáo, slide, README; test âm. | – |
| T3 | `62436fb` | `.github/workflows/ci.yml` (pytest `not slow` + checker). | **Chưa kiểm chứng**: cần push lên GitHub. |
| M6 | `6c7927d` | `h_staffing.optimize_shift_staffing`. Thăm dò đầy đủ 3.180 lịch phủ: ≤ 44 giờ công không lịch nào khả thi → **tối thiểu 48 giờ công**; tốt nhất trong 48 giờ công là Lịch 48 `[4,6,6,6,5,5,6,5,5]` (4 ca 8h + 4 ca 4h), trội ở mọi chỉ số. | Pipeline dùng `slack=0` (95 lịch) vì ở W = 48 không lịch nào thiếu quầy so với SIPP lại khả thi; cận trên W = giờ công phủ lịch tối ưu quầy-giờ. |
| M7 | `66db6d1` | `toi_uu_xac_suat_ngay.csv`: đạt SLA ở ≥ 90% số ngày cần **48 giờ công**, ≥ 95% cần **52 giờ công**. | Ở 48 giờ công, lịch M7 `[4,5,6,6,5,5,6,6,5]` (P 95.0%) và Lịch 48 (94.7%) không khác biệt có ý nghĩa. Có sàng lọc 100 lần lặp và cache để giai đoạn `optimize` còn ~6–10 phút. |
| M8 | `87f94aa` | `surge_policy` trong `c_sim.simulate`; `chinh_sach_tang_quay.csv`. Lịch 45 + mở thêm 1 quầy khi > 2 người chờ liên tục 5 phút: TB 46.2 quầy-giờ mở, P(SL ngày ≥ 90%) 97.3% (Lịch 48: 94.0%), nhu cầu +10% 0.919 (0.903), 14/14 ngày. | Ngưỡng 4–10 người / 10 phút trong kế hoạch gần như không kích hoạt; lưới cuối là ngưỡng 1–3, cửa sổ 3–5 phút. Kịch bản "ngày 10" (E[S] tăng chỉ 14h–17h) thay bằng E[S] +10% cả ngày vì `Model` chưa hỗ trợ phục vụ theo giờ. Cần 1 người dự phòng (chi phí không nằm trong quầy-giờ mở). |

**Kiểm chứng chung:** lần chạy đầy đủ cuối (`--reps-scale 1.0`, 9.9 phút) cho mọi CSV và hình của V4 giống từng byte; chỉ thêm 5 tệp mới (`toi_uu_theo_ca.csv`, `toi_uu_theo_ca_top.csv`, `toi_uu_xac_suat_ngay.csv`, `chinh_sach_tang_quay.csv`, khóa `toi_uu_theo_ca` trong `lich_khuyen_nghi.json`) và ngày chốt trong `params.json`. `pytest -q` 59/59 (4–7 phút do smoke test chạy M6–M8); checker sạch.

| R4 | `results(R4)` | `results/final_v5/` đóng băng. `diff -rq` với `final_v4`: mọi CSV và hình V4 giống từng byte; chỉ khác `MO_TA.md`, `thoi_gian_chay.json`, ngày chốt `params.json`, khóa `toi_uu_theo_ca`, 4 tệp M6–M8 và `doi_chieu_v3_v4.csv` → `doi_chieu_v4_v5.csv`. `g_report.metrics(R)` đọc V4 và V5 bằng cùng một hàm; 17 chỉ số V4 chênh 0. `pytest -q` 66/66 (549 s). | Pipeline 17.2 phút ở lần đóng băng (máy đang tải việc khác; lần chạy thử khi máy rảnh 9.9 phút). Chính sách M8 khuyến nghị chọn bằng quy tắc `f_scenarios.recommended_surge`, không gõ cứng. |
| D4 | `docs(D4)` | `tong_hop.md` (mục 1, 6, 7.9–7.11, 8, 9, 10), báo cáo (6.3, 9.5–9.7, 10), slide (8, 10, 12–14, Q&A 7–8), README §13, §15.5, `TONG_HOP_SO_LIEU_CHI_TIET.md`, CHANGELOG v5.0; tài liệu phụ trỏ sang `final_v5`. Checker thêm `check_shift_staffing`, `check_p_day`, `check_surge`: 1.249 giá trị, 0 lệch; test âm cho 4 mục. | Khuyến nghị chính đổi từ Lịch 45 sang Lịch 48 (48 giờ công). Hạn chế 6, 7 trong `tong_hop.md` mục 10 vẫn giữ vì chưa làm S13, S14. |

| S12–S15, M6b, M8b | `feat(model)`, `feat(S13, S14)`, `feat(S12)`, `feat(S15)`, `feat(M8)`, `feat(M6)`, `feat(M6-M8)`, `results+docs` | S12: Weibull $k = 0.855$, AIC tốt hơn mũ 18.7, lịch tối ưu vẫn 45. S13: fit train, RMSE test 63.9, vẫn bỏ lỡ 2/2 ngày hụt. S14: CI bootstrap rộng gấp khoảng 3 lần Wilson. S15: chỉ 8h–9h khác rõ, tổng quầy-giờ vẫn 45. M6 nghỉ trưa 9h–16h: vẫn 48 giờ công. M8 ngày 10: không chính sách nào giữ giờ tệ nhất ≥ 90%. Ba hình M6–M8. Checker 1.502 giá trị; `pytest -q` 84/84. | M6b (nghỉ trưa linh hoạt) là phần còn thiếu của kế hoạch M6; M8b (ngày 10) dùng `Model.service_by_hour`. Pipeline 15.1 phút (vượt mục tiêu 10 phút do thêm S12, S15, M6b). |

**Kết luận V5 (đã đưa vào tài liệu):** cần **48 giờ công/ngày**, xếp 4 ca 8h + 4 ca 4h theo Lịch 48; nếu có người dự phòng, Lịch 45 + quy tắc mở thêm quầy bền hơn với ít quầy-giờ mở hơn. Muốn ≥ 95% số ngày đạt SLA cần 52 giờ công. Kết luận vững với kiên nhẫn Weibull, λ nửa giờ và nghỉ trưa linh hoạt.

### Chưa làm

| Mã | Việc | Ghi chú |
|---|---|---|
| T3 | Kiểm chứng CI trên GitHub | **Làm tiếp theo** (cần người có quyền push). Push nhánh `feat/v5`, xem tab Actions ([mục 9.3](#93-t3--kiểm-chứng-ci)) |
| D5, D6 | Dashboard demo, slide thật, tập dượt | [Mục 9.5](#95-d5-d6--trình-bày) |

---

## Mục lục

0. [Thứ tự triển khai](#0-thứ-tự-triển-khai)
1. [Quy tắc chung](#1-quy-tắc-chung)
2. [Giai đoạn 1 — Nền kỹ thuật](#2-giai-đoạn-1--nền-kỹ-thuật)
3. [Giai đoạn 2 — Mô hình ảnh hưởng kết luận](#3-giai-đoạn-2--mô-hình-ảnh-hưởng-kết-luận)
4. [Giai đoạn 3 — Thống kê bổ sung](#4-giai-đoạn-3--thống-kê-bổ-sung)
5. [Giai đoạn 4 — Chạy lại, đóng băng V5, cập nhật tài liệu](#5-giai-đoạn-4--chạy-lại-đóng-băng-v5-cập-nhật-tài-liệu)
6. [Giai đoạn 5 — Trình bày và bảo vệ](#6-giai-đoạn-5--trình-bày-và-bảo-vệ)
7. [Checklist rà soát mỗi PR](#7-checklist-rà-soát-mỗi-pr)
8. [Checklist bàn giao V5](#8-checklist-bàn-giao-v5)
9. [Hướng dẫn các bước còn lại](#9-hướng-dẫn-các-bước-còn-lại)

---

## 0. Thứ tự triển khai

| # | Mã | Việc | Ưu tiên | Phụ thuộc | Đổi kết quả V4? | Ước lượng |
|:---:|---|---|:---:|---|:---:|:---:|
| 1 | P1 | Chạy song song các lần lặp mô phỏng | **P0** | – | Không (phải giống hệt) | 4–6 h |
| 2 | P2 | Đo profile và giảm chi phí mỗi lần lặp | P1 | P1 | Không (phải giống hệt) | 3–4 h |
| 3 | T2 | Checker đối chiếu số trong báo cáo và slide | **P0** | – | Không | 3 h |
| 4 | T3 | CI chạy test + checker mỗi lần push | P2 | T2 | Không | 1 h |
| 5 | M6 | Tối ưu trực tiếp theo giờ công ca | **P0** | P1 | Có (kết luận chính) | 6–8 h |
| 6 | M7 | Chọn lịch theo xác suất đạt SLA có biến động ngày | P1 | P1, M6 | Có | 4 h |
| 7 | M8 | Chính sách tăng quầy trong ngày theo hàng chờ | P1 | P1 | Thêm kết quả mới | 6–8 h |
| 8 | S12 | Kiên nhẫn không mũ (Weibull có kiểm duyệt) | P2 | P1 | Có thể | 4 h |
| 9 | S13 | Dự báo sớm fit trên train, đánh giá trên test | P2 | – | Có (mục 4.4) | 1–2 h |
| 10 | S14 | Cluster bootstrap cho "thực tế mọi giờ" | P2 | – | Có (khoảng tin cậy) | 2 h |
| 11 | S15 | Khung 30 phút cho 8h–10h | P3 (tùy chọn) | P1 | Có thể | 4 h |
| 12 | R4 | Chạy lại, đóng băng `final_v5`, đối chiếu V4 → V5 | **P0** | mọi việc chọn làm | – | 3 h |
| 13 | D4 | Cập nhật `tong_hop.md`, báo cáo, slide | **P0** | R4 | – | 4–6 h |
| 14 | D5 | Dashboard demo Erlang-A | P2 | – | Không | 3–4 h |
| 15 | D6 | Slide thật + tập dượt | P1 | D4 | – | 4 h |

**Lý do của thứ tự:**
- **P1 làm trước**: mọi thí nghiệm M/S đều chạy hàng trăm đến hàng nghìn lần lặp. Rút thời gian chạy 5–8 lần giúp các bước sau lặp nhanh.
- **T2 làm sớm**: giữ tài liệu không lệch trong suốt V5, vì V5 sẽ đổi số.
- **M6 là việc quan trọng nhất về nội dung**. Nó trả lời đúng câu hỏi quản lý (giờ công nhân viên) thay vì quầy-giờ mở. M7 dùng lại khung tìm kiếm của M6.
- **S12–S15** độc lập với nhau, làm khi còn thời gian.
- **Bộ tối thiểu nếu thiếu thời gian:** P1 → T2 → M6 → R4 → D4.

```
P1 ──┬── P2
     ├── M6 ── M7
     ├── M8
     ├── S12, S15
T2 ── T3
S13, S14 (độc lập)
mọi việc ── R4 ── D4 ── D6
```

---

## 1. Quy tắc chung

1. **Nhánh và commit:** làm trên nhánh `feat/v5`, mỗi mã việc là một commit (hoặc PR) riêng, tiêu đề dạng `perf(P1): ...`, `feat(M6): ...`, `test(T2): ...`, `docs(D4): ...`.
2. **Không ghi đè V4.** Trong lúc phát triển, chạy pipeline với `QS_RESULTS_DIR` trỏ ra thư mục tạm. Chỉ ở bước R4 mới đổi `common.RESULTS_VERSION = "final_v5"`.
3. **Việc "không đổi kết quả"** (P1, P2) phải chứng minh bằng so sánh byte-by-byte các CSV với `results/final_v4/` khi chạy cùng `--reps-scale` (xem P1).
4. **Việc "đổi kết quả"** phải ghi lại số trước/sau vào một CSV đối chiếu (giống `doi_chieu_v3_v4.csv`) và giải thích nguyên nhân.
5. **Seed:** giữ nguyên quy ước hiện tại (chọn lịch 1000, đánh giá 50000; mỗi lần lặp `seed_base + 1000·i`). Thí nghiệm mới dùng dải seed riêng, ghi trong docstring.
6. **Test:** mỗi việc thêm ít nhất một test; `pytest -q` phải pass trước khi merge.

---

## 2. Giai đoạn 1 — Nền kỹ thuật

### P1. Chạy song song các lần lặp mô phỏng

**Hiện nay.** `c_sim.run_reps` ([c_sim.py:362-368](../c_sim.py#L362-L368)) chạy tuần tự từng lần lặp. Máy có 20 CPU. Giai đoạn `robust` mất 24.9 phút, `optimize` 8.0 phút (`results/final_v4/thoi_gian_chay.json`).

**Trở ngại.** Trên Windows, `ProcessPoolExecutor` khởi tạo tiến trình con bằng `spawn`, nên mọi tham số phải pickle được. Các bộ sinh phục vụ trong [common.py:72-114](../common.py#L72-L114) (`exp_service`, `lognorm_service`, `gamma_service`, `weibull_service`, `empirical_service`, `mix_service`) đều trả về `lambda`/closure, không pickle được. `Model.service` chứa chúng.

**Thiết kế.**
1. Đổi mỗi bộ sinh thành class nhỏ có `__call__(self, rng)`, giữ nguyên chữ ký hàm tạo (ví dụ `empirical_service(samples)` trả về `EmpiricalService(samples)`). Thứ tự lời gọi `rng` phải giữ y hệt để số ngẫu nhiên không đổi.
2. Thêm vào `c_sim.py`:
   - biến cấu hình `N_WORKERS` (đọc từ biến môi trường `QS_WORKERS`, mặc định `min(os.cpu_count() - 1, 8)`; giá trị 1 = chạy tuần tự như cũ). **Đã triển khai:** giới hạn 8 vì mỗi tiến trình con nạp lại `main.py` (~145 MB); 19 tiến trình làm hỏng pool trên máy 16 GB còn trống 3.3 GB;
   - hàm `_run_job(args)` ở cấp module: gọi `simulate` rồi hàm hậu xử lý `post`;
   - hàm `map_sim(jobs, post, post_args)` dùng một `ProcessPoolExecutor` dùng chung (tạo lười, đóng khi thoát), `executor.map` giữ đúng thứ tự; nếu pool hỏng (`BrokenProcessPool`) thì chạy lại lô đó tuần tự.
3. `run_reps` dựng danh sách job (tham số của `simulate`) rồi gọi `map_sim` với `_rep_stats_post`. Phần tổng hợp phía sau giữ nguyên.
4. Các vòng gọi `sim.simulate` trực tiếp trong [e_robustness.py](../e_robustness.py) (dòng 114, 211, 323, 363) đổi sang `map_reps`. **Chú ý dòng 323** (`out_of_sample`): hệ số nhân ngày được rút tuần tự từ một `rng` ở tiến trình cha. Phải rút toàn bộ hệ số trước theo đúng thứ tự cũ, rồi mới phát job, để kết quả không đổi.
5. Với job quá ngắn (kiểm chứng hệ dừng, vài chục lần lặp), gom theo lô (`chunksize`) để giảm chi phí liên tiến trình.

**Kiểm thử.**
- `test_parallel_identical`: cùng model và lịch, `run_reps` với `QS_WORKERS=1` và `QS_WORKERS=4` cho dict kết quả bằng nhau tuyệt đối (so `sl_mean`, `hourly`, `rep_p_ab`…).
- `test_samplers_picklable`: `pickle.dumps` thành công cho mọi bộ sinh và cho `Model`.
- Kiểm tra cấp pipeline: chạy `python main.py --stage all --reps-scale 0.1` hai lần (`QS_WORKERS=1` và mặc định) ra hai thư mục tạm rồi `diff -r`: không khác byte nào (trừ `thoi_gian_chay.json`, `MO_TA.md`).

**DoD.**
- Test trên pass.
- Chạy đầy đủ `--reps-scale 1.0` cho CSV giống hệt `results/final_v4/`.
- Thời gian chạy toàn pipeline ≤ 10 phút (ghi trong `thoi_gian_chay.json`).

**Rủi ro.**
- Tiến trình con import lại module chính: mọi code chạy ở `main.py` phải nằm sau `if __name__ == "__main__":` (đã có, kiểm tra lại).
- Bộ nhớ: mỗi job trả về `st` (dict nhỏ) chứ không trả `DataFrame` khách, nên không tăng bộ nhớ đáng kể.

---

### P2. Đo profile và giảm chi phí mỗi lần lặp

**Hiện nay.** Mỗi lần lặp: `records.append(dict)` cho từng khách → `pd.DataFrame(records)` ([c_sim.py:226](../c_sim.py#L226)) → `rep_stats` tính bằng pandas.

**Các bước.**
1. Đo trước: `python -m cProfile -o prof.out` trên `run_reps(model, opt, 60)`; ghi tỉ lệ thời gian SimPy / tạo DataFrame / `rep_stats` vào mô tả PR.
2. Chỉ tối ưu nếu phần ngoài SimPy chiếm > 25%. Hướng làm: ghi bản ghi vào các list cột (hoặc mảng NumPy), `rep_stats` tính bằng `np.bincount` theo giờ thay vì `groupby`.
3. Giữ nguyên `simulate()` trả về `DataFrame` cho các nơi khác dùng; thêm đường nhanh nội bộ cho `run_reps`.

**DoD.** Kết quả giống hệt (cùng kiểm tra như P1); thời gian mỗi lần lặp giảm, ghi số đo trước/sau.

---

### T2. Checker đối chiếu số trong báo cáo và slide

**Hiện nay.** [tools/check_consistency.py](../tools/check_consistency.py) chỉ đối chiếu số trong `tong_hop.md`. Lần rà ngày 2026-10-29 đã đối chiếu 144 số trong `docs/bao_cao_tong_ket.md`, `docs/slide_thuyet_trinh.md`, `README.md` bằng script tạm.

**Thiết kế.** Thêm nhóm kiểm tra `check_report_numbers()`:
- Với mỗi bảng nguồn (`so_sanh_chinh_sach.csv`, `kiem_chung.csv`, `bang_sipp.csv`, `chi_phi.csv`, `do_nhay.csv`, `lich_ben_vung_delta.csv`, `lich_theo_ca.csv`), sinh chuỗi kỳ vọng theo đúng định dạng hiển thị trong tài liệu và kiểm tra chuỗi có xuất hiện.
- Chuẩn hóa trước khi so: dấu trừ Unicode `−` thành `-`, dấu phẩy thập phân trong README thành dấu chấm.
- Mỗi tài liệu khai báo danh sách bảng nó phải chứa (ví dụ slide chỉ cần SL ngày và giờ tệ nhất).

**Kiểm thử.** `test_results_consistency` (đã có trong `tests/test_v4_pipeline.py`) tự động bao luôn phần mới. Thêm một test âm: sửa một số trong bản sao tài liệu thì checker phải báo lỗi.

**DoD.** Checker báo 0 lỗi trên tài liệu hiện tại, và báo lỗi khi cố ý làm sai một số.

---

### T3. CI

Workflow `.github/workflows/ci.yml`: Python 3.12, `pip install -r requirements-dev.txt`, `pytest -q -m "not slow"`, `python tools/check_consistency.py`. Chạy trên `push` và `pull_request`. **DoD:** badge xanh trên nhánh `feat/v5`.

---

## 3. Giai đoạn 2 — Mô hình ảnh hưởng kết luận

### M6. Tối ưu trực tiếp theo giờ công ca

**Vấn đề.** Thuật toán hiện tại ([c_sim.optimize_schedule](../c_sim.py#L633)) tìm lịch quầy-giờ nhỏ nhất (45), sau đó [b_shifts.solve_shift_scheduling](../b_shifts.py#L67) mới xếp ca và phát hiện cần 48 giờ công. Lịch 48 bền vững cũng tốn 48 giờ công. Kết luận vì thế bị lệch: "tối thiểu 45 nhưng khuyến nghị 48". Câu hỏi quản lý đúng là: **ít giờ công nhất mà vẫn đạt SLA**.

**Thiết kế.**
- Biến quyết định: số nhân viên theo từng loại ca `x_s` (danh sách ca lấy từ `b_shifts.create_shifts(model_type="B", lunch_window=(3, 5))`).
- Độ phủ `c = A·x` chính là lịch quầy đưa vào mô phỏng (quầy dư vẫn mở, đúng thực tế).
- Mục tiêu: `min Σ giờ công(x)`; ràng buộc: `is_schedule_feasible(run_reps(model, A·x))`.
- Thuật toán (hàm mới `optimize_shift_staffing` trong `d_experiments.py` hoặc module mới `h_staffing.py`):
  1. **Khởi tạo:** nghiệm MILP phủ lịch tối ưu V4 (5 ca 8h + 2 ca 4h, 48 giờ công).
  2. **Tìm cận dưới:** liệt kê mọi tổ hợp `x` có giờ công < giờ công hiện tại và độ phủ ≥ SIPP Erlang-A trừ 1 quầy ở mỗi giờ (không gian nhỏ, có thể liệt kê bằng MILP với ràng buộc tổng giờ công cố định, lấy nhiều nghiệm bằng cách cắt nghiệm đã thấy).
  3. **Đánh giá** từng ứng viên bằng mô phỏng (60 lần lặp, seed 1000), sắp theo giờ công tăng dần; dừng ở mức giờ công nhỏ nhất có ứng viên khả thi.
  4. **Xác nhận** nghiệm bằng 300 lần lặp seed 50000.
- Báo cáo thêm hai biến thể: nghỉ trưa 11h–14h (hiện tại) và nghỉ trưa 9h–16h (linh hoạt).

**Đầu ra.**
- `toi_uu_theo_ca.csv`: mỗi ứng viên đã thử gồm `x`, độ phủ, giờ công, SL, cận dưới giờ tệ nhất, khả thi.
- Khóa `toi_uu_theo_ca` trong `lich_khuyen_nghi.json`.

**Kiểm thử.**
- `test_staffing_coverage`: với `x` bất kỳ, `A·x` khớp `solve_shift_scheduling` cho cùng mẫu.
- `test_staffing_not_worse`: nghiệm M6 có giờ công ≤ 48 và khả thi.

**DoD.**
- Có câu trả lời một dòng: "Tối thiểu N giờ công/ngày với X ca 8h + Y ca 4h".
- So sánh nghiệm này với Lịch 45 và Lịch 48 về SL, bỏ về, và độ bền (nhu cầu +10%).

**Rủi ro.** Nếu không gian ứng viên lớn hơn dự kiến, giới hạn số ứng viên mỗi mức giờ công (ví dụ 50) và ghi rõ trong báo cáo đây là tìm kiếm có giới hạn.

---

### M7. Chọn lịch theo xác suất đạt SLA khi có biến động ngày

**Vấn đề.** Lịch được chọn ở kịch bản danh định (không biến động ngày), độ bền chỉ kiểm tra sau. Lịch 45 có $P(SL_{\text{ngày}} \ge 90\%) = 85.7\%$ khi có biến động ngày (`so_sanh_chinh_sach_bd.csv`). Lịch 48 "+10%" là lựa chọn thủ công.

**Thiết kế.**
- Thêm tham số `day_cv` và `min_p_day` vào `is_schedule_feasible` (hoặc hàm khả thi mới). Lịch khả thi khi **cận dưới Wilson** của $P(SL_{\text{ngày}} \ge 90\%)$ ≥ `min_p_day`, đánh giá bằng `run_reps(..., day_cv=0.1401)`.
- Chạy với `min_p_day ∈ {0.80, 0.90, 0.95}`; dùng cả hai không gian tìm kiếm (quầy-giờ và theo ca của M6).
- Cần nhiều lần lặp hơn (ví dụ 300 khi chọn lịch) vì đây là xác suất; nhờ P1 vẫn chạy được.

**Đầu ra.** `toi_uu_xac_suat_ngay.csv` (mức `min_p_day`, lịch, quầy-giờ, giờ công, P đạt, số ngày thực tế đạt / 14).

**DoD.** Thay được cách nói "Lịch bền vững +10%" bằng "lịch nhỏ nhất đạt SLA ở ít nhất 90% số ngày", kèm đường cong chi phí theo mức tin cậy.

---

### M8. Chính sách tăng quầy trong ngày theo hàng chờ

**Vấn đề.** Dự báo lúc 10h bỏ lỡ cả hai ngày hụt SLA. Ngày 10 hụt vì thời gian phục vụ tăng đột ngột, điều mà dự báo theo số khách không thấy được.

**Thiết kế.**
- Thêm vào `simulate` tham số `surge_policy` (mặc định `None` = hành vi cũ, kết quả không đổi). Ví dụ: `{"threshold": N, "window": 10, "extra": 1, "min_hold": 30, "max_extra": 2}`.
- Thêm tiến trình `surge_monitor` mỗi phút kiểm tra số khách đang chờ (các request có `priority >= 0` trong `resource.queue`):
  - nếu vượt `threshold` liên tục `window` phút thì nhả 1 blocker (mở thêm quầy), giữ ít nhất `min_hold` phút;
  - khi hàng chờ về 0 thì trả lại blocker.
- **Lưu ý kỹ thuật:** blocker của giờ hiện tại do `counter_blocker_process` ([c_sim.py:99-131](../c_sim.py#L99-L131)) quản lý. Cần chuyển danh sách `block_reqs` sang đối tượng dùng chung để hai tiến trình không nhả cùng một request. `c_max` phải đủ lớn để có quầy dự phòng (`max(schedule) + max_extra`).
- Ghi thêm cột "quầy dự phòng đã mở (phút)" để tính chi phí.

**Thí nghiệm.**
- So sánh Lịch 45 + surge với Lịch 48 cố định: SL, giờ tệ nhất, bỏ về, quầy-giờ trung bình (kể cả phần dự phòng). Chạy trên ba kịch bản:
  1. danh định;
  2. có biến động ngày (CV 14%);
  3. 14 ngày thực tế (như `theo_14_ngay.csv`).
- Thêm kịch bản "ngày 10": $E[S] \times 1.29$ ở 14h–17h.
- Quét `threshold ∈ {4, 6, 8, 10}`.

**Kiểm thử.**
- `test_surge_none_identical`: `surge_policy=None` cho kết quả giống hệt V4.
- `test_surge_opens_counter`: dựng hàng chờ dài nhân tạo, kiểm tra số quầy bận vượt lịch.

**DoD.** Bảng so sánh và một khuyến nghị cụ thể ("mở thêm 1 quầy khi có hơn N khách chờ trong 10 phút"), kèm chi phí quầy-giờ dự phòng trung bình.

---

## 4. Giai đoạn 3 — Thống kê bổ sung

### S12. Kiên nhẫn không theo phân phối mũ

- **Hiện nay:** kiên nhẫn ~ Exp(θ) ([c_sim.py:216](../c_sim.py#L216)). Kaplan–Meier (`patience_km.csv`) giảm nhanh hơn đường mũ ở vùng chờ ngắn.
- **Các bước:**
  1. Fit Weibull có kiểm duyệt phải (khách được phục vụ = kiểm duyệt tại `wait`) bằng MLE trên train; so AIC với mũ.
  2. Thêm `Model.patience` (bộ sinh pickle được, như P1), mặc định mũ để giữ kết quả V4.
  3. Chạy lại tối ưu với Weibull.
- **DoD:** bảng so sánh mũ vs Weibull (tham số, AIC, lịch tối ưu, SL, bỏ về); kết luận có đổi lịch hay không.

### S13. Dự báo sớm fit trên train

- Fit $\hat V = a + b \cdot N_{8-10h}$ chỉ trên 10 ngày train; đánh giá RMSE trên 4 ngày test. Số đã tính tay: $\hat V = 90.9 + 4.20 N$, RMSE test 63.9.
- Áp lại quy tắc ngưỡng $V^*$ trên 14 ngày.
- Sửa `du_bao_som_hoi_quy.csv` và `danh_gia_chinh_sach_du_bao_14ngay.csv`; xóa hạn chế số 7 trong `tong_hop.md`.

### S14. Cluster bootstrap cho "thực tế mọi giờ"

- **Hiện nay:** khoảng Wilson coi 200 × 30 ngày-lần lặp là độc lập nên quá hẹp (hạn chế số 6).
- **Cách làm:** bootstrap theo kịch bản (resample 200 kịch bản, giữ nguyên 30 lần lặp bên trong), lấy phân vị 2.5–97.5%.
- **DoD:** cột CI mới trong `chi_so_ky_vong_dieu_kien.csv`, `do_nhay_cv_ngay.csv`; ghi chú trong mục 4.2 `tong_hop.md` được cập nhật.

### S15. Khung 30 phút cho 8h–10h (tùy chọn)

Ước lượng λ theo nửa giờ ở 8h–10h; mô phỏng hỗ trợ `hour_len` khác nhau theo khung (cần mở rộng `Model.rates` và `counter_blocker_process` sang danh sách độ dài khung). Chỉ làm khi M6–M8 xong.

---

## 5. Giai đoạn 4 — Chạy lại, đóng băng V5, cập nhật tài liệu

### R4. Đóng băng `final_v5`

1. Đặt `common.RESULTS_VERSION = "final_v5"`; `python main.py --stage all --reps-scale 1.0`.
2. Sinh `doi_chieu_v4_v5.csv` theo mẫu `doi_chieu_v3_v4.csv`. Mỗi chỉ số đổi phải có cột nguyên nhân (M6, M7, M8, S12…).
3. `pytest -q`, lưu log vào `results/final_v5/pytest_log.txt`.
4. Giữ `results/final_v4/` nguyên vẹn làm mốc đối chiếu.

### D4. Cập nhật tài liệu

Thứ tự:
1. `tong_hop.md`: mục 1 bảng quyết định (thêm cột giờ công tối ưu M6), các mục mới cho M6, M7, M8, bảng V4 → V5.
2. Checker (T2) phải pass.
3. Cập nhật `docs/bao_cao_tong_ket.md` (mục 9, 10), `docs/slide_thuyet_trinh.md` (slide 8–14), `docs/TONG_HOP_SO_LIEU_CHI_TIET.md` phần 3–5, README §15, `CHANGELOG.md`.

---

## 6. Giai đoạn 5 — Trình bày và bảo vệ

### D5. Dashboard demo
- **Mục đích:** hội đồng hỏi "nếu tham số khác thì sao" thì trả lời ngay.
- **Đầu vào:** λ theo giờ, E[S], θ, ngưỡng SLA. **Đầu ra:** lịch SIPP Erlang C và Erlang-A, SL và bỏ về từng giờ, tổng quầy-giờ.
- **Cách làm:** trang HTML tĩnh tính Erlang-A bằng JavaScript (port công thức từ `b_theory.py`).
- **DoD:** với tham số train, kết quả khớp `bang_sipp.csv` đến 3 chữ số.

### D6. Slide và tập dượt
- Chuyển `docs/slide_thuyet_trinh.md` thành bộ slide thật.
- Mỗi thành viên trình bày được mạch chính trong 10 phút và trả lời ≥ 5/6 câu trong phụ lục Q&A.

---

## 7. Checklist rà soát mỗi PR

- [ ] Commit/PR chỉ chứa một mã việc; tiêu đề có mã (P1, M6…).
- [ ] `pytest -q` pass; có test mới cho việc này.
- [ ] Việc "không đổi kết quả": đã `diff -r` CSV với lần chạy tuần tự hoặc với `final_v4` cùng `--reps-scale`, không khác.
- [ ] Việc "đổi kết quả": có bảng trước/sau và nguyên nhân; chưa ghi đè `results/final_v4/`.
- [ ] Seed mới (nếu có) ghi trong docstring và không trùng dải đã dùng.
- [ ] Hàm mới có docstring nêu thí nghiệm, số lần lặp, seed, tệp đầu ra.
- [ ] Thời gian chạy giai đoạn bị ảnh hưởng ghi trong mô tả PR.
- [ ] `python tools/check_consistency.py` pass.

## 8. Checklist bàn giao V5

- [x] P1: pipeline đầy đủ ≤ 10 phút (9.9 phút có M6–M8), CSV V4 tái lập giống hệt khi tắt tính năng mới.
- [x] T2: checker đối chiếu cả `tong_hop.md`, báo cáo, slide, README.
- [x] M6: có số giờ công tối thiểu (48) và phương án ca cụ thể (4 ca 8h + 4 ca 4h).
- [x] M7, M8: có bảng so sánh và khuyến nghị vận hành (`toi_uu_xac_suat_ngay.csv`, `chinh_sach_tang_quay.csv`).
- [x] `results/final_v5/` đóng băng, có `doi_chieu_v4_v5.csv`, `MO_TA.md`, `pytest_log.txt`.
- [x] Tài liệu cập nhật; `CHANGELOG.md` có mục v5.0.
- [x] Hạn chế trong `tong_hop.md` mục 10 cập nhật (xóa hạn chế Wilson nhờ S14, viết lại dự báo sớm theo S13, kiên nhẫn theo S12, ca làm việc theo M6b, ngày 10 theo M8b).

---

## 9. Hướng dẫn các bước còn lại

Viết cho người làm tiếp. Trạng thái xuất phát: nhánh `feat/v5`, commit `87f94aa`, `results/final_v4/` vẫn là bản đóng băng hiện hành, mọi tài liệu còn mang số V4.

### 9.1 R4 — Đóng băng `final_v5`

1. **Bản đối chiếu V4 → V5.** Hiện `g_report.py` sinh `doi_chieu_v3_v4.csv` từ `PREV_RESULTS_DIR = results/final_v3` (`g_report.py:25`, `v3_reference()` dòng 96, `build_doi_chieu()` dòng 132). Cần:
   - đổi `PREV_RESULTS_DIR` sang `results/final_v4`, viết `v4_reference()` đọc trực tiếp CSV V4 (`so_sanh_chinh_sach.csv`, `theo_14_ngay_tong_hop.csv`, `lich_khuyen_nghi.json`…) thay cho các khóa V3;
   - đổi tên tệp đầu ra thành `doi_chieu_v4_v5.csv` (`g_report.py:74`, `:245`), sửa `main.py:10` (docstring), `tests/test_v4_pipeline.py:70` và danh sách `required` trong `tools/check_consistency.py:97`;
   - thêm các dòng mới: giờ công tối thiểu (M6), lịch theo mức P (M7), chính sách tăng quầy (M8). Các chỉ số V4 cũ phải **không đổi** (đã kiểm chứng giống từng byte), nên cột nguyên nhân chủ yếu là "mới ở V5".
2. **Đổi phiên bản:** `common.py:17` `RESULTS_VERSION = "final_v5"`. Thêm 4 tệp mới vào `required` của checker.
3. **Chạy:** `python main.py --stage all --reps-scale 1.0` (~10 phút; máy bận có thể tới 15 phút). Nếu thấy cảnh báo "process pool hong" thì giảm `QS_WORKERS` (vd 4).
4. **Kiểm tra:** `diff -rq results/final_v4 results/final_v5` chỉ được khác ở `MO_TA.md`, `thoi_gian_chay.json`, `params.json` (ngày chốt), `lich_khuyen_nghi.json` (thêm khóa `toi_uu_theo_ca`) và tệp mới/đổi tên. Khác ở CSV nào khác là lỗi, phải tìm nguyên nhân trước khi đi tiếp.
5. **Log test:** `pytest -q > results/final_v5/pytest_log.txt` (4–7 phút).
6. Commit `results(R4): đóng băng V5`. Giữ nguyên `results/final_v4/` làm mốc.

### 9.2 D4 — Cập nhật tài liệu

Làm theo thứ tự; sau mỗi tệp chạy `python tools/check_consistency.py`.

1. **`tong_hop.md`** (nguồn số duy nhất):
   - Mục 1 (bảng quyết định): thêm dòng "Giờ công tối thiểu" = 48 (M6) và cột/khối "Lịch 45 + tăng quầy" (M8); câu kết luận một dòng đổi thành "tối thiểu 48 giờ công/ngày, 4 ca 8h + 4 ca 4h theo Lịch 48".
   - Thêm mục mới: 7.9 Tối ưu theo ca (M6, từ `toi_uu_theo_ca_top.csv` + số lịch thử theo giờ công từ `toi_uu_theo_ca.csv`), 7.10 Xác suất đạt SLA ngày (M7, `toi_uu_xac_suat_ngay.csv`), 7.11 Tăng quầy theo hàng chờ (M8, `chinh_sach_tang_quay.csv`).
   - Mục 8: thay bảng V3 → V4 bằng V4 → V5 (`doi_chieu_v4_v5.csv`).
   - Mục 9: số test (59), thời gian pipeline (~10 phút), mô tả song song (`QS_WORKERS`).
   - Mục 10 (hạn chế): thêm "M8 cần 1 người dự phòng, chi phí không tính trong quầy-giờ mở", "kịch bản ngày 10 chưa mô phỏng được vì phục vụ không đổi theo giờ".
   - Đường dẫn `results/final_v4/` → `results/final_v5/` (trừ chỗ nói về V4).
2. **Checker:** thêm hàm kiểm tra cho 3 mục mới vào `check_numeric_consistency()` (theo mẫu `check_patience`, `check_abandon_constraint`), và cập nhật `_expected_report_strings()` nếu báo cáo/slide thêm bảng mới.
3. **`docs/bao_cao_tong_ket.md`:** mục 6.3 (ca làm việc) và 9 (tối ưu) thêm M6; mục 9.3–9.4 thêm M7, M8; mục 10.1 câu 1 và 3, mục 10.2 khuyến nghị đổi theo kết luận mới; tiêu đề "Phiên bản số liệu" → V5.
4. **`docs/slide_thuyet_trinh.md`:** slide 8 (tối ưu) thêm M6; slide 10–12 thêm M7, M8; slide 14 kết luận mới; phụ lục Q&A thêm câu "vì sao 48 giờ công mà không phải 45 quầy-giờ" và "chính sách tăng quầy cần gì".
5. **`README.md` §15**, **`docs/TONG_HOP_SO_LIEU_CHI_TIET.md` phần 3–5**: cập nhật tóm tắt và đường dẫn.
6. **`CHANGELOG.md`:** đổi tiêu đề "v5 (đang phát triển)" thành "v5.0" kèm ngày đóng băng.
7. Commit `docs(D4): cập nhật tài liệu theo V5`.

### 9.3 T3 — Kiểm chứng CI

`git push -u origin feat/v5`, mở tab Actions trên GitHub. Nếu lỗi cài đặt do phiên bản ghim trong `requirements.txt` chưa có trên PyPI cho Linux, ghi lại lỗi và nới phiên bản trong workflow (không sửa `requirements.txt` của bản đóng băng). Smoke test đánh dấu `slow` không chạy trên CI.

### 9.4 S12–S15 — Thống kê bổ sung (tùy chọn)

Làm **sau R4/D4** nếu còn thời gian; mỗi việc làm thay đổi kết quả nên cần chạy lại pipeline và cập nhật tài liệu liên quan.

- **S12 (kiên nhẫn Weibull):** thêm `Model.patience` là bộ sinh class (như `_ExpService` trong `common.py`), mặc định mũ để giữ V5; dòng cần đổi `c_sim.py` (`patience = rng.exponential(...)` trong `arrival_generator`). Fit Weibull có kiểm duyệt trên train bằng `scipy.optimize.minimize` (log-likelihood: khách bỏ về đóng góp mật độ, khách được phục vụ đóng góp hàm sống tại `wait`).
- **S13 (dự báo fit trên train):** số đã tính tay ở `tong_hop.md` mục 4.4 ($\hat V = 90.9 + 4.20 N$, RMSE test 63.9); sửa `e_robustness.volume_threshold`.
- **S14 (cluster bootstrap):** trong `e_robustness.conditional_expectation`, resample 200 kịch bản (giữ 30 lần lặp bên trong) để lấy CI cho cột "thực tế mọi giờ".
- **S15 (khung 30 phút):** cần `Model.rates` và `counter_blocker_process` hỗ trợ độ dài khung khác nhau; cùng thay đổi này cũng mở đường cho kịch bản "ngày 10" của M8 (phục vụ theo giờ).

### 9.5 D5, D6 — Trình bày

- **D5:** trang HTML tĩnh tính SIPP Erlang-A (port từ `b_theory.erlang_a`, `sipp_schedule`); kiểm tra khớp `bang_sipp.csv` đến 3 chữ số.
- **D6:** chuyển `docs/slide_thuyet_trinh.md` (sau D4) thành bộ slide; tập dượt theo phụ lục Q&A.

### 9.6 Lưu ý kỹ thuật cho người làm tiếp

- **RAM:** mỗi tiến trình con ~145 MB; máy 16 GB còn trống ~3 GB thì giữ `QS_WORKERS` ≤ 8.
- **Đo thời gian:** đừng chạy pytest/benchmark song song với pipeline khi đo; số tuyệt đối dao động 5.5–9 phút cho cùng code.
- **Log khi chạy song song:** ghi log bằng `>>` (append) và `PYTHONUNBUFFERED=1`, nếu không traceback của tiến trình con bị ghi đè.
- **Smoke test** (`tests/test_v4_pipeline.py::test_pipeline_smoke`, `--reps-scale 0.02`) mất ~3–4 phút vì M6–M8 phải duyệt nhiều lịch khi số lần lặp nhỏ.
- **Seed đã dùng:** chọn lịch 1000, đánh giá 50000, M7 chọn 3000 (sàng lọc 503000), M6 độ bền 81000/131000, M8 400000–1.300.000. Thí nghiệm mới nên dùng dải khác.
