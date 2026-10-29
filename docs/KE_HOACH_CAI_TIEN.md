# KẾ HOẠCH CẢI TIẾN DỰ ÁN MÔ PHỎNG HÀNG ĐỢI (V3 → V4)

> **Mục tiêu:** sửa các lỗi kỹ thuật làm sai lệch kết quả, củng cố tính hợp lệ khi chuyển kết luận từ tổng đài (dữ liệu Anonymous Bank) sang quầy giao dịch, dọn repo để chạy lại được từ một lệnh duy nhất, và rút gọn thông điệp khi bảo vệ.
>
> **Nguyên tắc chung:**
> 1. Gom **toàn bộ** thay đổi code (giai đoạn 1) trước, chạy lại **một lần**, đóng băng vào `results/final_v4/`. Không vá từng số trong tài liệu.
> 2. Mọi số liệu trong `tong_hop.md`, báo cáo, slide phải sinh tự động từ CSV trong `results/final_v4/` (hoặc được `tools/check_consistency.py` đối chiếu).
> 3. Mỗi việc có **tiêu chí hoàn thành (DoD)** rõ ràng; chưa đạt DoD thì chưa sang việc phụ thuộc.

---

## Mục lục

0. [Tóm tắt ưu tiên](#0-tóm-tắt-ưu-tiên)
1. [Giai đoạn 1 — Sửa lỗi code ảnh hưởng kết quả (P0)](#1-giai-đoạn-1--sửa-lỗi-code-ảnh-hưởng-kết-quả-p0)
2. [Giai đoạn 2 — Hợp nhất pipeline và dọn repo (P0)](#2-giai-đoạn-2--hợp-nhất-pipeline-và-dọn-repo-p0)
3. [Giai đoạn 3 — Bổ sung kiểm thử (P1)](#3-giai-đoạn-3--bổ-sung-kiểm-thử-p1)
4. [Giai đoạn 4 — Củng cố nội dung mô hình (P1)](#4-giai-đoạn-4--củng-cố-nội-dung-mô-hình-p1)
5. [Giai đoạn 5 — Chạy lại, đóng băng V4, đối chiếu V3 (P0)](#5-giai-đoạn-5--chạy-lại-đóng-băng-v4-đối-chiếu-v3-p0)
6. [Giai đoạn 6 — Báo cáo, slide, chuẩn bị phản biện (P1)](#6-giai-đoạn-6--báo-cáo-slide-chuẩn-bị-phản-biện-p1)
7. [Việc tùy chọn (P2)](#7-việc-tùy-chọn-p2)
8. [Phân công và lịch](#8-phân-công-và-lịch)
9. [Checklist bàn giao cuối](#9-checklist-bàn-giao-cuối)

---

## 0. Tóm tắt ưu tiên

| Mã | Việc | Mức | Ảnh hưởng | Công sức |
|---|---|:---:|---|:---:|
| F1 | Sửa xả hàng sau 17h mở hết `c_max` quầy | **P0** | SL giờ 16h–17h (giờ hay là "tệ nhất") đang bị lạc quan | 0,5 h |
| F2 | Sinh khách đến đúng quá trình Poisson không đồng nhất | **P0** | Sai lệch λ ở ranh giới giờ | 1 h |
| F3 | Hiệu suất theo giờ tính theo thời gian bận thực tế | P1 | `util_h` gán theo giờ đến, sai khi khách vắt qua giờ | 1–2 h |
| R1 | Một nguồn cấu hình `RESULTS_DIR`, bỏ số hard-code trong `main.py` | **P0** | `main.py` đang đọc `final_v1`, in số cũ | 1 h |
| R2 | Đưa logic S1–S11, C1–C7 từ `tools/` vào module chính | **P0** | V3 không tái lập được từ `main.py` | 4–6 h |
| R3 | Dọn repo (PNG gốc, v1/v2, đường dẫn `file:///d:/KHDV`) | P1 | Dễ đọc, tránh nhầm phiên bản | 1–2 h |
| T1 | Bổ sung test cho F1, F2, blocker, SIPP tối thiểu | P1 | Chặn lỗi tái phát | 3 h |
| M1 | Kịch bản "quầy giao dịch thật": kiên nhẫn dài (θ nhỏ) | **P0 (nội dung)** | Trả lời câu hỏi phản biện lớn nhất | 3 h |
| M2 | Thêm ràng buộc tỉ lệ bỏ về (vd ≤ 3%) | P1 | Lịch 44 đang để 5,35% khách bỏ về | 2 h |
| M3 | Dùng phân phối thực nghiệm (bootstrap) cho kịch bản chính | P1 | Gamma đánh giá thấp cs² (0,91 vs 1,20) | 2 h |
| M4 | Điều tra bất thường ngoài mẫu 15h–16h | P1 | SL 76,5% nằm ngoài PI95 chưa giải thích | 2 h |
| M5 | Ổn định giờ tệ nhất (tăng reps, CRN, báo cáo sai số giữa lần chạy) | P1 | Giờ tệ nhất nhảy H3 ↔ H8 | 2 h |
| D1 | Tái cấu trúc thông điệp báo cáo/slide | P1 | Kết luận chính bị chìm | 4 h |

---

## 1. Giai đoạn 1 — Sửa lỗi code ảnh hưởng kết quả (P0)

### F1. Sau 17h mô phỏng mở hết `c_max` quầy để xả hàng

**Hiện trạng.** [c_sim.py:102-114](../c_sim.py#L102-L114): `counter_blocker_process` nhả mọi blocker ở cuối **mỗi** giờ, kể cả giờ cuối. Sau phút 540, không còn blocker, nên toàn bộ `c_max = max(schedule)` quầy (6 với Lịch 44) phục vụ khách còn tồn. Lịch 44 có 4 quầy lúc 16h–17h → khách đến cuối giờ được 6 quầy phục vụ, SL giờ 8 bị **lạc quan**. Đây chính là giờ được báo là "tệ nhất" (H8, 90,78%).

**Việc cần làm.**
```python
def counter_blocker_process(env, resource, c_max, schedule, hour_len):
    for h, active_c in enumerate(schedule):
        block_reqs = [resource.request(priority=-1)
                      for _ in range(max(0, c_max - active_c))]
        if h == len(schedule) - 1:
            return  # giữ nguyên số quầy giờ cuối cho đến khi xả hết hàng
        yield env.timeout(hour_len)
        for req in block_reqs:
            resource.release(req)
```
- Ghi rõ giả định trong `docs/dac_ta_mo_hinh.md`: "Sau giờ đóng cửa không nhận khách mới; số quầy giữ như giờ cuối đến khi phục vụ xong khách đã vào hàng."
- (Tùy chọn) tham số `drain_policy ∈ {"keep_last", "all_open"}` để báo cáo cả hai, chứng minh mức ảnh hưởng.

**DoD.** Test T1-a pass; chạy Lịch 44 60 reps, ghi lại SL giờ 8 trước/sau vào `results/final_v4/doi_chieu_v3_v4.csv`.

### F2. Quá trình đến không đồng nhất sai ở ranh giới giờ

**Hiện trạng.** [c_sim.py:162-171](../c_sim.py#L162-L171): khoảng cách đến được rút theo λ của giờ hiện tại, kể cả khi lần đến rơi sang giờ sau. Khi λ giờ sau lớn hơn (8h→9h, 9h→10h), đầu giờ sau bị thiếu khách và ngược lại.

**Việc cần làm** (tận dụng tính không nhớ của phân phối mũ):
```python
def arrival_generator():
    cid = 0
    n_h = len(model.rates)
    while env.now < total_time:
        h = min(int(env.now // hour_len), n_h - 1)
        lam = model.rates[h] * m_d
        boundary = (h + 1) * hour_len if h < n_h - 1 else total_time
        if lam <= 0:
            yield env.timeout(boundary - env.now)
            continue
        inter_arr = rng.exponential(1.0 / lam)
        if env.now + inter_arr >= boundary:
            yield env.timeout(boundary - env.now)  # sang giờ mới, rút lại với λ mới
            continue
        yield env.timeout(inter_arr)
        ...  # phần sinh thuộc tính khách giữ nguyên
```
- Lưu ý: dùng `int(env.now // hour_len)` ngay tại `boundary` có thể dính sai số dấu phẩy động → tính `h` từ biến đếm thay vì từ `env.now` nếu cần.

**DoD.** Test T1-b: 2.000 ngày mô phỏng với `rates` dạng bậc thang mạnh (vd `[0.5, 3.0]`), số khách trung bình mỗi giờ nằm trong CI95 của `λ_h · 60`.

### F3. Hiệu suất theo giờ gán theo giờ đến

**Hiện trạng.** [c_sim.py:245-248](../c_sim.py#L245-L248): `util_h = Σ svc của khách ĐẾN trong giờ h / (c·60)`. Khách đến 9h55 phục vụ đến 10h05 bị tính hết vào 9h.

**Việc cần làm.** Ghi `start_svc`, `end_svc` vào `records`; tính thời gian bận giao với `[h·60, (h+1)·60)`. Giữ `util_all` như cũ (đã đúng ở mức cả ngày).

**DoD.** Tổng `util_h · c_h · 60` qua các giờ bằng tổng thời gian bận (sai số < 1e-6).

---

## 2. Giai đoạn 2 — Hợp nhất pipeline và dọn repo (P0)

### R1. Một nguồn cấu hình, bỏ số hard-code

**Hiện trạng.**
- [main.py:74](../main.py#L74), [main.py:93](../main.py#L93) đọc `results/final_v1/`; [d_experiments.py:46](../d_experiments.py#L46) ghi vào `final_v1`.
- [main.py:68](../main.py#L68), [main.py:109](../main.py#L109), [main.py:122](../main.py#L122), [main.py:130](../main.py#L130) in số cố định (54, 18,5%, "13.87 ± 1.54" — trong khi V3 là 14.79 ± 1.01).

**Việc cần làm.**
- Thêm vào [common.py](../common.py): `RESULTS_VERSION = "final_v4"`, `RESULTS_DIR = os.path.join(BASE_DIR, "results", RESULTS_VERSION)`, `BASELINE_C = 6`.
- Mọi module đọc/ghi qua `common.RESULTS_DIR`.
- `main.py` chỉ in số lấy từ biến đã tính hoặc CSV vừa ghi; baseline tính bằng `BASELINE_C * common.HOURS`.

**DoD.** `grep -rn "final_v1\|final_v2\|final_v3" *.py` không còn kết quả (ngoài thư mục archive); `grep -n "13.87\|18.5%\|= 54" main.py` rỗng.

### R2. Đưa phân tích V3 vào module chính

**Hiện trạng.** Logic thống kê V3 nằm rải trong `tools/run_s1_s10.py`, `tools/run_s2_s3_s4.py`, `tools/run_s5_s6_s7_s8_s9_s11.py`, `tools/run_fixes.py` (1.000 dòng), `tools/t1_fix_poisson.py`. Các hàm này tự dựng lại `get_base_model()` (lặp code ở 2 file) và hard-code `sched=[4,5,6,5,5,5,5,5,4]`.

**Việc cần làm.**
- Tạo `e_robustness.py` (hoặc gói `analysis/`) gồm các hàm thuần, nhận `model`, `policies`, `rng/seed`, trả `DataFrame`:
  - `conditional_expectation()` (S2), `posterior_predictive_check()` (S3), `volume_threshold()` (S4),
  - `nested_bootstrap()` (S5), `out_of_sample()` (S6), `fourteen_days()` (S7),
  - `mg1_and_tier_verification()` (S8), `service_dist_sensitivity()` (S9), `cost_analysis()` (S11).
- Chuyển `tools/stats_helpers.py` (Wilson, t-CI, Holm) vào `common.py` hoặc `stats_utils.py`.
- Lịch tối ưu truyền vào từ kết quả `optimize_schedule`, **không** hard-code.
- `main.py` có cờ chạy theo giai đoạn:
  ```
  python main.py --stage all|data|theory|verify|optimize|robust|report --reps-scale 1.0
  ```
  `--reps-scale 0.1` để chạy nhanh khi phát triển.
- Các script `tools/run_*.py`, `tools/t1_fix_poisson.py`, `tools/run_fixes.py` chuyển vào `tools/archive/` kèm README một dòng "đã hợp nhất vào …".

**DoD.** Từ repo sạch: `pip install -r requirements.txt && python main.py --stage all` sinh đủ mọi CSV/hình mà `tong_hop.md` trích dẫn. Ghi thời gian chạy vào `results/final_v4/MO_TA.md`.

### R3. Dọn repo

- Chuyển 8 file `fig_*.png` ở thư mục gốc và `ket_qua_kiem_chung.csv` vào `results/final_v4/hinh/` (hoặc xóa vì đã có bản trong results).
- Gộp `results/final_v1`, `final_v2` vào `results/archive/` (giữ để truy vết, ghi chú trong README).
- Sửa đường dẫn tuyệt đối `file:///d:/KHDV/...` trong template MO_TA ([d_experiments.py:829-848](../d_experiments.py#L829-L848)) thành đường dẫn tương đối.
- Gom tài liệu: `docs/BAO_CAO_SUA_DOI*.md`, `YEU_CAU_CHINH_SUA_*.md`, `TUAN_*_HUONG_DAN.md` vào `docs/lich_su/`. Ở `docs/` chỉ giữ: báo cáo tổng kết, đặc tả mô hình, công thức, mô tả dữ liệu, slide, bảng quyết định.
- `requirements.txt`: ghim phiên bản cụ thể (`simpy==4.1.1`, …) để tái lập; tạo `requirements-dev.txt` có `pytest`.
- README: thêm mục "Chạy nhanh trong 3 lệnh" ở đầu.

**DoD.** Thư mục gốc chỉ còn: code `*.py`, `README.md`, `CHANGELOG.md`, `requirements*.txt`, `tong_hop.md`, các thư mục `data/ docs/ excel/ results/ tests/ tools/`.

---

## 3. Giai đoạn 3 — Bổ sung kiểm thử (P1)

Hiện có 21 test (~250 dòng). Môi trường hiện tại **chưa cài pytest** → cài trước (`pip install -r requirements-dev.txt`) và chạy để xác nhận baseline.

| Mã | Test | Kiểm tra |
|---|---|---|
| T1-a | `test_drain_keeps_last_hour_servers` | Lịch `[6, 2]`, ghi số quầy bận theo thời gian; sau phút 120 số quầy bận ≤ 2 |
| T1-b | `test_nhpp_hourly_counts` | `rates=[0.5, 3.0]`, 2.000 ngày: số khách giờ 0 ≈ 30, giờ 1 ≈ 180 (trong CI95) |
| T1-c | `test_blocker_respects_schedule` | Trong mọi giờ h (trừ thời gian chuyển tiếp khi quầy đang phục vụ dở) số quầy bận ≤ `schedule[h]` |
| T1-d | `test_sipp_is_minimal` | Với mỗi giờ: `c_h` đạt SL ≥ 90% và `c_h − 1` không đạt (cả Erlang C và Erlang-A) |
| T1-e | `test_erlang_a_sl_vs_sim` | 1 cấu hình Erlang-A, sim 30 reps, SL lý thuyết nằm trong CI95 |
| T1-f | `test_erlang_a_truncation` | Tăng `K`/`M` (200→400, 80→160) SL đổi < 1e-6 ([b_theory.py:110](../b_theory.py#L110) đang cắt `M = min(K, 80)`) |
| T1-g | `test_util_hourly_sums` | Kiểm tra DoD của F3 |
| T1-h | `test_results_consistency` | Gọi `tools/check_consistency.py` như một test: mọi số trong `tong_hop.md` khớp CSV V4 |
| T1-i | `test_pipeline_smoke` | `main.py --stage all --reps-scale 0.02` chạy hết, không lỗi (đánh dấu `@pytest.mark.slow`) |

**DoD.** `pytest -q` pass; log lưu `results/final_v4/pytest_log.txt`.

---

## 4. Giai đoạn 4 — Củng cố nội dung mô hình (P1)

### M1. Kịch bản "quầy giao dịch thật" — kiên nhẫn dài

**Vấn đề.** θ = 0,109/phút (kiên nhẫn TB ~9 phút, KM cho thấy bỏ về rất sớm) là hành vi **cúp máy tổng đài**. Ở quầy có lấy số, khách ít bỏ về hơn nhiều. Lịch 44 thấp hơn Erlang C (47) chính là nhờ bỏ về giảm tải. Hội đồng gần như chắc chắn hỏi điểm này.

**Việc cần làm.**
- Chạy SIPP (Erlang-A) và tối ưu mô phỏng với kiên nhẫn TB ∈ {9,2 (gốc), 15, 20, 30, 60, ∞} phút.
- Bảng kết quả: kiên nhẫn TB → lịch theo giờ → tổng quầy-giờ → SL → p_ab → W_q.
- Kỳ vọng: khi kiên nhẫn → ∞, lịch hội tụ về Erlang C (47 q-h); nêu rõ "nếu áp dụng cho quầy thật, khuyến nghị nằm trong khoảng 44–47 q-h tùy kiên nhẫn đo được".
- Liên hệ `docs/ke_hoach_khao_sat.md`: nêu cụ thể cần đo những gì để xác định θ tại chỗ (thời gian chờ của khách bỏ về + khách được phục vụ, ≥ 100 khách bỏ về để CI θ ±20%).

**Sản phẩm.** `results/final_v4/do_nhay_kien_nhan.csv`, hình `fig_kien_nhan_vs_quay_gio.png`, một đoạn trong báo cáo mục "Tính chuyển giao".

### M2. Thêm ràng buộc tỉ lệ bỏ về

**Vấn đề.** SLA chỉ ràng buộc "phục vụ và chờ ≤ 5 phút"; W_q TB chỉ ~0,5 phút nên ngưỡng 5 phút rất lỏng, ràng buộc thật là bỏ về. 5,35% khách bỏ về là con số đáng lo trong ngân hàng.

**Việc cần làm.**
- Mở rộng `is_schedule_feasible` ([c_sim.py:506](../c_sim.py#L506)) nhận thêm `max_p_ab` (mặc định `None` để giữ hành vi cũ).
- Chạy tối ưu với `max_p_ab ∈ {5%, 3%, 2%}` → bảng "mức bỏ về chấp nhận được ↔ số quầy-giờ".
- Thêm cột "SL với ngưỡng 2 phút / 3 phút" để chỉ ra ngưỡng 5 phút lỏng đến mức nào.

**Sản phẩm.** `results/final_v4/toi_uu_rang_buoc_bo_ve.csv`; một hình Pareto 3 trục (q-h, SL, p_ab) hoặc bảng.

### M3. Phân phối thực nghiệm làm kịch bản chính

**Vấn đề.** Cả 4 phân phối bị KS bác bỏ; Gamma có cs² = 0,91 < 1,20 thực tế → mô phỏng lạc quan (bootstrap giảm SL 0,78 điểm %).

**Việc cần làm.**
- Dùng `common.empirical_service(train_svc)` đã có sẵn làm **mô hình chính**; Gamma chuyển thành phân tích độ nhạy.
- Chạy lại tối ưu với dịch vụ thực nghiệm. Nếu lịch đổi (ví dụ cần 45 q-h), báo cáo lịch mới là khuyến nghị chính.
- Trong báo cáo giải thích: "KS bác bỏ mọi phân phối là chuyện bình thường với n = 6.346; vì vậy dùng trực tiếp dữ liệu".

### M4. Điều tra bất thường ngoài mẫu 15h–16h

**Việc cần làm.**
- So sánh λ, E[S], cs², θ, tỉ lệ VIP của giờ 7 giữa train và test (4 ngày test, từng ngày).
- Kiểm tra số quầy thực tế có thể đã ít hơn (dữ liệu không ghi số nhân viên → suy ra số người phục vụ đồng thời tối đa từ timestamp bắt đầu/kết thúc phục vụ trong `data_clean.csv`).
- Kết luận một trong ba: (a) do nhu cầu test cao hơn, (b) do nhân sự thực tế ít hơn, (c) chưa giải thích được — kèm số liệu.

**Sản phẩm.** Mục mới trong `docs/ngoai_mau.md`.

> Gợi ý mở rộng: ước lượng **số nhân viên thực tế theo giờ** từ dữ liệu (số phiên phục vụ chồng lấn) cho phép so sánh trực tiếp mô phỏng với thực tế — hiện `tong_hop.md` mục 2.1 ghi là "không so sánh được". Nếu làm được, đây là điểm cộng lớn về kiểm định mô hình.

### M5. Ổn định giờ tệ nhất và sai số giữa các lần chạy

**Vấn đề.** Giờ tệ nhất đổi H3 ↔ H8 giữa các lần chạy; sai số Monte Carlo giữa lần chạy (~±0,005) lớn hơn CI trong lần chạy.

**Việc cần làm.**
- Đánh giá cuối các lịch ứng viên với `n_reps` đủ lớn để bán độ rộng CI SL mỗi giờ ≤ 0,3 điểm % (ước lượng R cần thiết từ phương sai hiện có: `R ≈ (2·s/0,003)²`).
- Tách bạch: bộ seed **chọn lịch** (`seed_base=1000`) và bộ seed **đánh giá** (`seed_base=50000`) — đã có, ghi rõ trong báo cáo để tránh bị hỏi về selection bias.
- Báo cáo "giờ tệ nhất" dưới dạng **xác suất mỗi giờ là giờ tệ nhất** qua các lần chạy thay vì một giờ duy nhất.

---

## 5. Giai đoạn 5 — Chạy lại, đóng băng V4, đối chiếu V3 (P0)

1. Sau khi F1–F3, R1–R2, M1–M3 xong: `python main.py --stage all` một lần, seed cố định.
2. Đóng băng vào `results/final_v4/`, sinh `MO_TA.md` tự động (đường dẫn tương đối).
3. Tạo `results/final_v4/doi_chieu_v3_v4.csv`: mỗi chỉ số chính (lịch tối ưu, SL toàn ngày, SL giờ tệ nhất, p_ab, W_q, ρ, 12/14 ngày đạt) — giá trị V3, V4, chênh lệch, nguyên nhân (F1/F2/M3…).
4. Cập nhật `tong_hop.md`, `docs/TONG_HOP_SO_LIEU_CHI_TIET.md` **bằng script** (`tools/update_tong_hop_chi_tiet.py` trỏ sang V4), rồi chạy `tools/check_consistency.py`.
5. Ghi `CHANGELOG.md` mục V4.

**DoD.** `check_consistency.py` báo 0 lệch; bảng đối chiếu V3/V4 có đủ cột nguyên nhân.

---

## 6. Giai đoạn 6 — Báo cáo, slide, chuẩn bị phản biện (P1)

### D1. Tái cấu trúc thông điệp

Báo cáo chính (≤ 25 trang) theo mạch: **Bài toán → Dữ liệu → Lý thuyết → Kiểm chứng → Kết quả → Độ bền → Hạn chế**. Đưa S2–S11, PPC, nested bootstrap, Holm-Bonferroni xuống **phụ lục**.

Slide (12–15 trang) chỉ cần 4 hình/bảng cốt lõi:
1. λ theo giờ (có CI) + lịch quầy khuyến nghị chồng lên.
2. Lý thuyết vs mô phỏng (3 tầng) — một biểu đồ cột sai lệch %.
3. Bảng quyết định: Lịch tối ưu / Lịch dự phòng / 6 quầy cố định (q-h, SL, p_ab, W_q, ρ).
4. Đường đánh đổi: quầy-giờ ↔ SL ↔ bỏ về, kèm kịch bản kiên nhẫn (M1).

Câu kết luận một dòng phải trả lời đúng đề: *"Cần tối thiểu X quầy-giờ/ngày, phân bổ [..] theo giờ, để ≥ 90% khách chờ dưới 5 phút; nếu khách quầy ít bỏ về hơn tổng đài, con số tăng lên tối đa Y."*

### D2. Bộ câu hỏi phản biện (bổ sung vào README mục 18)

| Câu hỏi | Trả lời ngắn + bằng chứng |
|---|---|
| Dữ liệu tổng đài có dùng cho quầy được không? | Kết quả M1: số quầy theo kiên nhẫn; điểm chung về cấu trúc hàng đợi; điều kiện cần đo tại chỗ |
| Poisson và phân phối phục vụ đều bị bác bỏ, sao còn dùng M/M/c? | M/M/c là mốc tham chiếu; mô phỏng dùng hệ số nhân ngày + phân phối thực nghiệm (M3) |
| Sao Erlang-A ít quầy hơn Erlang C? | Bỏ về giảm tải; đổi lại 5% khách mất (M2) |
| Lịch tối ưu có bị overfit seed không? | Tách seed chọn/đánh giá, R đủ lớn (M5) |
| Tại sao 15h–16h ngoài mẫu kém? | Kết quả M4 |
| Mô phỏng có đúng không? | 3 tầng + M/G/1 P-K exact + test tự động |
| Sau giờ đóng cửa xử lý thế nào? | Giả định F1 |

### D3. Tập dượt
- Mỗi thành viên tự trình bày được toàn bộ mạch chính trong 10 phút và trả lời được ≥ 5/7 câu trên.

---

## 7. Việc tùy chọn (P2)

- **Kiểm định quá trình đến chặt hơn:** test khoảng cách đến theo mũ trong từng giờ có hiệu chỉnh (Lewis/Brown et al. 2005 — biến đổi khoảng đến trong khung ngắn). Đây là kiểm định chuẩn trong tài liệu call center, trích dẫn được.
- **Dự báo nhu cầu ngày:** fit dự báo sớm V̂ chỉ trên train, đánh giá trên test (hiện fit trên cả 14 ngày — hạn chế số 5 trong `tong_hop.md`).
- **Khung 30 phút** thay cho 60 phút ở các giờ λ đổi nhanh (8h–10h), so sánh lợi ích.
- **Dashboard nhỏ** (Streamlit hoặc trang HTML tĩnh) cho phép chọn λ, E[S], θ, SLA → ra lịch quầy theo Erlang-A tức thì; tiện demo khi bảo vệ.
- **Wilson cho "thực tế mọi giờ"** đang bỏ qua tương quan trong kịch bản → thay bằng cluster bootstrap theo kịch bản.

---

## 8. Phân công và lịch

Giữ vai trò như hiện tại: **A** — dữ liệu & thống kê, **B** — lý thuyết & Excel & ca làm, **C** — mô phỏng & tối ưu.

| Ngày | A | B | C |
|---|---|---|---|
| 1 | Cài môi trường, chạy pytest baseline; R3 (dọn repo, docs) | R1 (cấu hình, bỏ hard-code) | F1, F2 + T1-a, T1-b |
| 2 | M4 (điều tra 15h–16h, ước lượng số NV thực tế) | T1-d, T1-f; chuẩn bị bảng Erlang C/A theo kiên nhẫn (phần lý thuyết M1) | F3, T1-c, T1-g; M2 (ràng buộc bỏ về) |
| 3 | R2 phần thống kê (S1, S3, S4, S6, S7) | R2 phần chi phí/ca (S11, C4–C6) | R2 phần mô phỏng (S2, S5, S8, S9) |
| 4 | M3 (dịch vụ thực nghiệm) | M1 (kịch bản kiên nhẫn, cả lý thuyết + sim) | M5; T1-e, T1-h, T1-i |
| 5 | **Cả nhóm:** Giai đoạn 5 — chạy V4, đóng băng, đối chiếu V3/V4, cập nhật `tong_hop.md` | | |
| 6 | D1 báo cáo (Dữ liệu, Hạn chế) | D1 báo cáo (Lý thuyết, Kết quả) | D1 slide + hình |
| 7 | **Cả nhóm:** D2, D3 tập dượt; checklist mục 9 | | |

> Nếu thời gian ít hơn: làm tối thiểu **F1, F2, R1, M1, Giai đoạn 5, D1** (~2,5 ngày).

---

## 9. Checklist bàn giao cuối

- [ ] F1, F2 đã sửa, có test; F3 đã sửa hoặc ghi rõ là hạn chế
- [ ] `grep` không còn `final_v1/v2/v3` và số hard-code trong code chạy chính
- [ ] `python main.py --stage all` chạy được từ repo sạch, thời gian chạy đã ghi
- [ ] `pytest -q` pass, log lưu trong `results/final_v4/`
- [ ] `results/final_v4/doi_chieu_v3_v4.csv` có đủ nguyên nhân thay đổi
- [ ] `tools/check_consistency.py` báo 0 lệch với `tong_hop.md`
- [ ] Bảng kiên nhẫn (M1) và ràng buộc bỏ về (M2) có trong báo cáo
- [ ] Mô hình chính dùng phân phối phục vụ thực nghiệm (M3), Gamma ở độ nhạy
- [ ] Mục 15h–16h (M4) có kết luận
- [ ] Câu kết luận một dòng trả lời đúng đề bài có trong báo cáo, slide, README
- [ ] Mỗi thành viên trả lời được bộ câu hỏi D2
- [ ] Ghi nguồn dữ liệu Technion SEE Center và đã thông báo cho GS. Mandelbaum theo điều kiện sử dụng
