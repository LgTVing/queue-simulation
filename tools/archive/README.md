# tools/archive

Script V2/V3 đã được hợp nhất vào pipeline chính (`python main.py --stage ...`), chỉ giữ để truy vết:

| Script cũ | Đã hợp nhất vào |
|---|---|
| `t1_fix_poisson.py` | `a_data.poisson_overdispersion()` (stage `data`) |
| `run_s1_s10.py` | `a_data.lambda_ci_table()`, `service_fit_details()`, `patience_km()`, `cluster_bootstrap_params()` (stage `data`) |
| `run_s2_s3_s4.py` | `e_robustness.conditional_expectation()`, `cv_day_sensitivity()`, `posterior_predictive_check()`, `volume_threshold()` (stage `robust`) |
| `run_s5_s6_s7_s8_s9_s11.py` | `e_robustness.nested_bootstrap()`, `out_of_sample()`, `fourteen_days()`, `service_dist_sensitivity()`, `cost_analysis()`; S8 vào `chay_kiem_chung.py`; C6 vào `c_sim.local_search_phase3()` |
| `run_fixes.py` | `d_experiments.run_optimize()` (so sánh chính sách, biến động ngày, xếp ca), `e_robustness` (độ nhạy phân phối, ngoài mẫu) |
| `gen_theo_ngay.py` | `e_robustness.fourteen_days()` |

Các script này đọc/ghi `results/final_v2`, `final_v3` với lịch hard-code và **không** còn chạy được với code V4.
