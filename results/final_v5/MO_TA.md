# Mô tả kết quả `final_v5` (sinh tự động bởi `g_report.py`)

- **Ngày sinh:** 2026-10-30
- **Môi trường:** Python 3.12.10, SimPy 4.1.2, NumPy 2.5.4, SciPy 1.18.1, pandas 3.1.0, Matplotlib 3.11.2
- **Lệnh tái lập:** `python main.py --stage all --reps-scale 1.0`
- **Seed:** chọn lịch `seed_base=1000`, đánh giá cuối `seed_base=50000` (tách biệt để tránh selection bias)
- **Mô hình chính:** NHPP theo giờ (F2), phục vụ thực nghiệm lấy mẫu từ train (M3), bỏ về mũ θ, VIP ưu tiên không ngắt, xả hàng giữ số quầy giờ cuối (F1)
- **Lịch tối ưu:** `[4, 5, 6, 5, 5, 5, 5, 5, 5]` (45 quầy-giờ); bền vững +10%: `[4, 6, 6, 6, 5, 5, 6, 5, 5]`
- **Lịch theo ca ít giờ công nhất (M6):** `[4, 6, 6, 6, 5, 5, 6, 5, 5]` (48 quầy-giờ mở; xem `toi_uu_theo_ca_top.csv`)

## Thời gian chạy

| Giai đoạn | Hệ số lần lặp | Thời gian (phút) | Lúc chạy |
|---|:---:|:---:|---|
| data | 1.0 | 0.1 | 2026-10-30T08:20:23 |
| theory | 1.0 | 0.0 | 2026-10-30T08:20:23 |
| verify | 1.0 | 0.2 | 2026-10-30T08:20:37 |
| optimize | 1.0 | 9.8 | 2026-10-30T08:30:24 |
| robust | 1.0 | 5.0 | 2026-10-30T08:35:24 |
| report | 1.0 | 0.0 | 2026-10-30T08:35:24 |

## Danh mục tệp

| Tệp | Giai đoạn / nhiệm vụ | Nội dung |
|---|---|---|
| [`bang_sipp.csv`](bang_sipp.csv) | theory | Lich SIPP Erlang C va Erlang-A theo gio |
| [`bat_dinh_nested.csv`](bat_dinh_nested.csv) | robust / S5 | Ket qua tung bo tham so bootstrap long nhau |
| [`chi_phi.csv`](chi_phi.csv) | robust / S11 | Chi phi quay-gio + mat khach, CI hieu so theo cap |
| [`chi_so_ky_vong_dieu_kien.csv`](chi_so_ky_vong_dieu_kien.csv) | robust / S2 | Chi so ky vong co dieu kien theo he so nhan ngay |
| [`chinh_sach_tang_quay.csv`](chinh_sach_tang_quay.csv) | robust / M8 | Lich 45 + mo them quay khi hang cho dai so voi Lich 45/48 co dinh, 4 kich ban + 14 ngay |
| [`cluster_bootstrap_params.csv`](cluster_bootstrap_params.csv) | data / S10 | CI95 cluster bootstrap theo ngay cho E[S], theta |
| [`danh_gia_chinh_sach_du_bao_14ngay.csv`](danh_gia_chinh_sach_du_bao_14ngay.csv) | robust / S4 | Chinh sach ghep theo du bao 8h-10h tren 14 ngay |
| [`dieu_tra_15h_16h.csv`](dieu_tra_15h_16h.csv) | data / M4 | So sanh tham so khung 15h-16h giua train va tung ngay test |
| [`do_nhay.csv`](do_nhay.csv) | robust | Do nhay nhu cau, E[S], theta (CRN) |
| [`do_nhay_cv_ngay.csv`](do_nhay_cv_ngay.csv) | robust / S3 | S2 voi CV ngay 8-20% |
| [`do_nhay_kien_nhan.csv`](do_nhay_kien_nhan.csv) | optimize / M1 | Lich va chi so theo kien nhan trung binh 9,2 -> vo cung |
| [`do_nhay_phan_phoi.csv`](do_nhay_phan_phoi.csv) | robust / S9 | Do nhay phan phoi phuc vu, hieu so theo cap voi mo hinh chinh |
| [`doi_chieu_v4_v5.csv`](doi_chieu_v4_v5.csv) | report | Doi chieu chi so chinh V4 vs V5 kem nguyen nhan, chi so moi M6-M8 |
| [`doi_chieu_xa_hang.csv`](doi_chieu_xa_hang.csv) | optimize / F1 | SL gio cuoi khi xa hang giu so quay gio cuoi vs mo het c_max |
| [`du_bao_som_hoi_quy.csv`](du_bao_som_hoi_quy.csv) | robust / S4 | Hoi quy du bao som va nguong V* |
| [`gio_te_nhat.csv`](gio_te_nhat.csv) | robust / M5 | Xac suat moi gio la gio te nhat |
| [`khoang_tin_cay_lambda.csv`](khoang_tin_cay_lambda.csv) | data / S1 | CI95 lambda_h theo Poisson va Student-t qua 14 ngay |
| [`khung_30_phut.csv`](khung_30_phut.csv) | optimize / S15 | Lich 45/48 va lich toi uu khi lambda 8h-10h theo nua gio |
| [`kiem_chung.csv`](kiem_chung.csv) | verify / S8 | Kiem chung 3 tang + M/G/1 P-K 40.000 phut + M/G/6, CI95 Student-t |
| [`kiem_chung_pooling.csv`](kiem_chung_pooling.csv) | verify | Hang chung vs hang rieng (ly thuyet va SimPy) |
| [`kiem_dinh_phan_phoi_chi_tiet.csv`](kiem_dinh_phan_phoi_chi_tiet.csv) | data / S10 | AIC, BIC, KS bootstrap (da quy doi co mau) cho 4 phan phoi phuc vu |
| [`kiem_dinh_poisson.csv`](kiem_dinh_poisson.csv) | data / T1 | Kiem dinh phan tan chi^2 theo gio, nhan chuan |
| [`kien_nhan_weibull.csv`](kien_nhan_weibull.csv) | optimize / S12 | Lich toi uu va danh gia Lich 45/48 duoi kien nhan mu va Weibull |
| [`kien_nhan_weibull_fit.csv`](kien_nhan_weibull_fit.csv) | optimize / S12 | MLE kien nhan Weibull co kiem duyet tren train so voi mu (AIC, ti so hop ly) |
| [`lambda_nua_gio.csv`](lambda_nua_gio.csv) | optimize / S15 | Lambda hai nua moi khung gio (train), kiem dinh binomial va Holm-Bonferroni |
| [`lich_ben_vung_delta.csv`](lich_ben_vung_delta.csv) | optimize | Lich toi uu theo muc du phong nhu cau +5/10/20% |
| [`lich_khuyen_nghi.json`](lich_khuyen_nghi.json) | theory / optimize | Cac lich da tinh (SIPP, toi uu, ben vung, theo ca, Gamma) |
| [`lich_theo_ca.csv`](lich_theo_ca.csv) | optimize | Xep ca MILP (mo hinh A/B, ca 4h, hon hop) |
| [`lich_toi_uu.csv`](lich_toi_uu.csv) | optimize | Lich su toi uu 2 pha |
| [`m3_dich_vu_thuc_nghiem.csv`](m3_dich_vu_thuc_nghiem.csv) | optimize / M3 | Lich toi uu va danh gia duoi phuc vu thuc nghiem vs Gamma |
| [`ngoai_mau.csv`](ngoai_mau.csv) | robust / S6 | Ngoai mau: PI95 vs SL quan sat, Holm-Bonferroni |
| [`nguong_luu_luong_chi_tiet.csv`](nguong_luu_luong_chi_tiet.csv) | robust / S4 | SL theo luu luong ngay co dinh |
| [`nhan_vien_uoc_luong.csv`](nhan_vien_uoc_luong.csv) | data / M4 | So phien phuc vu chong lan (toi da, trung binh) theo ngay x gio |
| [`nhan_vien_uoc_luong_theo_gio.csv`](nhan_vien_uoc_luong_theo_gio.csv) | data / M4 | So nhan vien uoc luong theo gio (train vs test) |
| [`params.json`](params.json) | data | Tham so uoc luong tren 10 ngay train; phuc vu chinh: thuc nghiem (M3) |
| [`patience_km.csv`](patience_km.csv) | data / S10 | Kaplan-Meier cua kien nhan so voi mu |
| [`pha3.csv`](pha3.csv) | optimize / C6 | Pha 3 bang mo phong: swap 1 quay va giam 2 quay |
| [`phan_ra_phuong_sai.csv`](phan_ra_phuong_sai.csv) | robust / S5 | Phan ra phuong sai tham so vs nhieu mo phong |
| [`posterior_predictive_check.csv`](posterior_predictive_check.csv) | robust / S3 | Posterior predictive check chi so phan tan |
| [`pytest_log.txt`](pytest_log.txt) | test | Log pytest |
| [`qua_phan_tan_ngay.csv`](qua_phan_tan_ngay.csv) | data / T1 | Qua phan tan tong khach theo ngay, CV ngay sau hieu chinh Poisson |
| [`so_lan_lap_can_thiet.csv`](so_lan_lap_can_thiet.csv) | robust / M5 | So lan lap de CI SL moi gio <= 0,3 diem % |
| [`so_sanh_chinh_sach.csv`](so_sanh_chinh_sach.csv) | optimize | So sanh 6 chinh sach, 300 lan lap, seed danh gia rieng |
| [`so_sanh_chinh_sach_bd.csv`](so_sanh_chinh_sach_bd.csv) | optimize | So sanh chinh sach co he so nhan ngay |
| [`theo_14_ngay.csv`](theo_14_ngay.csv) | robust / S7 | Doi chieu 14 ngay quan sat |
| [`theo_14_ngay_tong_hop.csv`](theo_14_ngay_tong_hop.csv) | robust / S7 | So ngay dat SLA va Wilson CI |
| [`thoi_gian_chay.json`](thoi_gian_chay.json) | report | Thoi gian chay va he so so lan lap tung giai doan |
| [`toi_uu_rang_buoc_bo_ve.csv`](toi_uu_rang_buoc_bo_ve.csv) | optimize / M2 | Toi uu voi rang buoc ti le bo ve, SL o nguong 2/3/5 phut |
| [`toi_uu_theo_ca.csv`](toi_uu_theo_ca.csv) | optimize / M6 | Moi lich phu theo ca da thu (gio cong, phuong an ca, SL, can duoi gio te nhat) |
| [`toi_uu_theo_ca_linh_hoat.csv`](toi_uu_theo_ca_linh_hoat.csv) | optimize / M6 | Nhu toi_uu_theo_ca.csv voi nghi trua linh hoat 9h-16h |
| [`toi_uu_theo_ca_linh_hoat_top.csv`](toi_uu_theo_ca_linh_hoat_top.csv) | optimize / M6 | Top-5 lich kha thi, nghi trua linh hoat 9h-16h |
| [`toi_uu_theo_ca_top.csv`](toi_uu_theo_ca_top.csv) | optimize / M6 | Top-5 lich kha thi o gio cong nho nhat: seed danh gia, bien dong ngay, nhu cau +10% |
| [`toi_uu_xac_suat_ngay.csv`](toi_uu_xac_suat_ngay.csv) | optimize / M7 | Lich nho nhat theo muc P(SL ngay >= 90%) co bien dong ngay, quay-gio va theo ca, 14 ngay thuc te |

## Hình

- [`hinh/fig_a_fit.png`](hinh/fig_a_fit.png)
- [`hinh/fig_b_ca_lam.png`](hinh/fig_b_ca_lam.png)
- [`hinh/fig_c_do_nhay.png`](hinh/fig_c_do_nhay.png)
- [`hinh/fig_c_pooling.png`](hinh/fig_c_pooling.png)
- [`hinh/fig_c_welch.png`](hinh/fig_c_welch.png)
- [`hinh/fig_kien_nhan_vs_quay_gio.png`](hinh/fig_kien_nhan_vs_quay_gio.png)
- [`hinh/fig_m6_gio_cong.png`](hinh/fig_m6_gio_cong.png)
- [`hinh/fig_m7_muc_tin_cay.png`](hinh/fig_m7_muc_tin_cay.png)
- [`hinh/fig_m8_tang_quay.png`](hinh/fig_m8_tang_quay.png)
- [`hinh/fig_pareto_bo_ve.png`](hinh/fig_pareto_bo_ve.png)
