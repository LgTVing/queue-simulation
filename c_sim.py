"""
c_sim.py: Dong co mo phong su kien roi rac bang SimPy (Tuan 2):
1. Mo phong quay phuc vu ngan hang voi PriorityResource (VIP, khach thuong)
2. Khach bo ve do het kien nhan (Abandonment)
3. Dieu chinh so quay linh hoat theo gio bang Blocker process
4. Thong ke, tinh khoang tin cay (CI95) va danh gia kha thi SLA
5. Mo phong he thong hang tach rieng (Random vs JSQ) va duong Welch chon warm-up
"""

from typing import List, Dict, Tuple, Optional, Callable
import numpy as np
import pandas as pd
import simpy
import matplotlib.pyplot as plt

from common import (
    Model, HOURS, H_LABELS, TARGET_SLA, WAIT_THRESHOLD, WAIT_THRESHOLD_VIP,
    mean_ci, exp_service, lognorm_service
)
import b_theory as th

# =============================================================================
# 1. TIEN TRINH KHACH HANG VA BLOCKER TRONG SIMPY
# =============================================================================

def customer_process(
    env: simpy.Environment,
    cid: int,
    hour: int,
    is_vip: int,
    svc_time: float,
    patience: float,
    resource: simpy.PriorityResource,
    records: List[Dict]
):
    """Tien trinh vong doi cua 1 khach hang trong he thong."""
    arr_time = env.now
    # Priority: Blocker (-1) > VIP (0) > Thuong (1)
    prio = 0 if is_vip == 1 else 1
    
    with resource.request(priority=prio) as req:
        # Chờ đồng thời 2 sự kiện: được phục vụ HOẶC hết kiên nhẫn
        if patience < float("inf"):
            patience_event = env.timeout(patience)
            result = yield req | patience_event
            
            if req in result:
                # Duoc vao phuc vu
                start_service = env.now
                wait_time = start_service - arr_time
                yield env.timeout(svc_time)
                end_service = env.now
                records.append({
                    "cid": cid,
                    "hour": hour,
                    "vip": is_vip,
                    "arr_time": arr_time,
                    "wait": wait_time,
                    "svc": svc_time,
                    "served": 1
                })
            else:
                # Het kien nhan bo ve
                wait_time = env.now - arr_time
                records.append({
                    "cid": cid,
                    "hour": hour,
                    "vip": is_vip,
                    "arr_time": arr_time,
                    "wait": wait_time,
                    "svc": np.nan,
                    "served": 0
                })
        else:
            # Khong bao gio bo ve (patience = inf)
            yield req
            start_service = env.now
            wait_time = start_service - arr_time
            yield env.timeout(svc_time)
            records.append({
                "cid": cid,
                "hour": hour,
                "vip": is_vip,
                "arr_time": arr_time,
                "wait": wait_time,
                "svc": svc_time,
                "served": 1
            })

def counter_blocker_process(
    env: simpy.Environment,
    resource: simpy.PriorityResource,
    c_max: int,
    schedule: List[int],
    hour_len: float
):
    """
    Tien trinh dieu chinh so quay theo gio:
    Trong khung gio h, chi cho phep schedule[h] quay hoat dong.
    c_max - schedule[h] quay con lai bi chiem giu boi blocker voi priority cao nhat (-1).
    """
    for h, active_c in enumerate(schedule):
        needed_blocks = max(0, c_max - active_c)
        block_reqs = []
        # Chiem giu so quay khong hoat dong
        for _ in range(needed_blocks):
            req = resource.request(priority=-1)
            block_reqs.append(req)
            
        yield env.timeout(hour_len)
        
        # Giai phong khi chuyen gio (de gio sau thiet lap lai)
        for req in block_reqs:
            resource.release(req)

# =============================================================================
# 2. HAM MO PHONG TOAN BO NGAY / DOT CHAY
# =============================================================================

def simulate(
    model: Model,
    schedule: List[int],
    run_time: Optional[float] = None,
    warm_up: float = 0.0,
    seed: int = 42,
    day_cv: float = 0.0,
    day_multiplier: Optional[float] = None
) -> pd.DataFrame:
    """
    Chay 1 dot mo phong don le.
    Tra ve DataFrame ghi nhan chi tiet lich su moi khach hang.
    day_cv > 0: ap dung he so nhan ngay m_d ~ Gamma(1/day_cv^2, day_cv^2).
    day_multiplier: truyen truc tiep gia tri he so nhan ngay (neu co).
    """
    rng = np.random.default_rng(seed)
    env = simpy.Environment()
    
    # Xac dinh he so nhan ngay m_d (neu co)
    if day_multiplier is not None:
        m_d = float(day_multiplier)
    elif day_cv > 0.0:
        shape_m = 1.0 / (day_cv ** 2)
        scale_m = day_cv ** 2
        m_d = float(rng.gamma(shape_m, scale_m))
    else:
        m_d = 1.0
    
    c_max = max(schedule) if len(schedule) > 0 else 1
    resource = simpy.PriorityResource(env, capacity=c_max)
    records = []
    
    total_time = run_time if run_time is not None else float(len(schedule) * model.hour_len)
    hour_len = model.hour_len
    
    # Khoi chay tien trinh dieu phoi lich quay neu lich co su thay doi
    if len(schedule) > 1:
        env.process(counter_blocker_process(env, resource, c_max, schedule, hour_len))
        
    def arrival_generator():
        cid = 0
        while env.now < total_time:
            # Xac dinh khung gio hien tai
            h = min(int(env.now // hour_len), len(model.rates) - 1)
            lam = model.rates[h] * m_d
            if lam <= 0:
                yield env.timeout(1.0)
                continue
                
            # Sinh khoang thoi gian den tiep theo (Exp(lam))
            inter_arr = rng.exponential(1.0 / lam)
            yield env.timeout(inter_arr)
            if env.now >= total_time:
                break
                
            # Sinh thuoc tinh khach hang
            h_arrival = min(int(env.now // hour_len), len(model.rates) - 1)
            if isinstance(model.p_vip, (list, tuple, np.ndarray)):
                pv = model.p_vip[h_arrival] if h_arrival < len(model.p_vip) else model.p_vip[-1]
            else:
                pv = model.p_vip
            is_vip = 1 if rng.random() < pv else 0
            svc_time, _ = model.service(rng)
            
            patience = rng.exponential(1.0 / model.theta) if model.theta > 0 else float("inf")
            
            env.process(customer_process(
                env, cid, h_arrival, is_vip, svc_time, patience, resource, records
            ))
            cid += 1

    env.process(arrival_generator())
    env.run(until=total_time + 1000.0) # Cho den khi giai phong het khach
    
    df = pd.DataFrame(records)
    if len(df) == 0:
        return pd.DataFrame(columns=["cid", "hour", "vip", "arr_time", "wait", "svc", "served"])
        
    # Loai bo doan warm-up neu co
    if warm_up > 0:
        df = df[df["arr_time"] >= warm_up].copy()
        
    return df

# =============================================================================
# 3. TINH TOAN CHI SO THONG KE TUNG DOT CHAY VA NHIEU DOT LAP
# =============================================================================

def rep_stats(
    df: pd.DataFrame,
    schedule: List[int],
    hour_len: float = 60.0,
    wait_thresh: float = WAIT_THRESHOLD,
    wait_thresh_vip: float = WAIT_THRESHOLD_VIP
) -> Dict:
    """Tinh toan cac chi so thong ke toan ngay va theo tung gio tu ket qua 1 dot chay."""
    if len(df) == 0:
        return {"sl_all": 0.0, "sl_vip": 0.0, "wq_all": 0.0, "p_ab_all": 0.0, "hourly": []}
        
    # Toan ngay
    n_tot = len(df)
    n_served_sla = ((df["served"] == 1) & (df["wait"] <= wait_thresh)).sum()
    sl_all = n_served_sla / n_tot if n_tot > 0 else 0.0
    
    df_vip = df[df["vip"] == 1]
    n_vip = len(df_vip)
    n_vip_sla = ((df_vip["served"] == 1) & (df_vip["wait"] <= wait_thresh_vip)).sum()
    sl_vip = n_vip_sla / n_vip if n_vip > 0 else np.nan
    
    wq_all = df["wait"].mean()
    p_ab_all = (df["served"] == 0).mean()

    # Hieu suat su dung toan bo quay
    tot_svc_all = df[df["served"] == 1]["svc"].sum() if "svc" in df.columns else 0.0
    tot_c_time = sum(schedule) * hour_len
    util_all = tot_svc_all / tot_c_time if tot_c_time > 0 else 0.0
    
    # Theo tung khung gio
    hourly = []
    for h, c in enumerate(schedule):
        df_h = df[df["hour"] == h]
        n_h = len(df_h)
        if n_h == 0:
            hourly.append({"hour": h, "sl": 1.0, "sl_vip": 1.0, "wq": 0.0, "p_ab": 0.0, "util": 0.0})
            continue
            
        sl_h = ((df_h["served"] == 1) & (df_h["wait"] <= wait_thresh)).sum() / n_h
        df_h_vip = df_h[df_h["vip"] == 1]
        sl_h_vip = (((df_h_vip["served"] == 1) & (df_h_vip["wait"] <= wait_thresh_vip)).sum() / len(df_h_vip)) if len(df_h_vip) > 0 else np.nan
        wq_h = df_h["wait"].mean()
        p_ab_h = (df_h["served"] == 0).mean()
        
        # Hieu suat su dung quay trong gio h: tong thoi gian phuc vu / (c * hour_len)
        tot_svc_h = df_h[df_h["served"] == 1]["svc"].sum()
        util_h = tot_svc_h / (c * hour_len) if c > 0 and hour_len > 0 else 0.0
        
        hourly.append({
            "hour": h,
            "sl": float(sl_h),
            "sl_vip": float(sl_h_vip) if not np.isnan(sl_h_vip) else np.nan,
            "wq": float(wq_h),
            "p_ab": float(p_ab_h),
            "util": float(util_h)
        })
        
    return {
        "sl_all": float(sl_all),
        "sl_vip": float(sl_vip) if not np.isnan(sl_vip) else np.nan,
        "wq_all": float(wq_all),
        "p_ab_all": float(p_ab_all),
        "util_all": float(util_all),
        "hourly": hourly
    }

def run_reps(
    model: Model,
    schedule: List[int],
    n_reps: int = 30,
    run_time: Optional[float] = None,
    warm_up: float = 0.0,
    seed_base: int = 42,
    day_cv: float = 0.0
) -> Dict:
    """
    Chay n_reps lan lap doc lap su dung ky thuat so ngau nhien chung (CRN).
    Tinh trung binh, sai so chuan va khoang tin cay 95% cho moi chi so.
    day_cv > 0: ap dung bien dong he so nhan ngay.
    """
    reps_data = []
    hourly_reps = [[] for _ in range(len(schedule))]
    
    # Xac dinh do dai gio hieu dung:
    # Neu he dung chay dai (len(schedule) == 1 va co run_time), do dai thuc te la run_time - warm_up
    if run_time is not None and len(schedule) == 1:
        eff_hour_len = max(1.0, run_time - warm_up)
    else:
        eff_hour_len = model.hour_len
    
    for i in range(n_reps):
        seed = seed_base + i * 1000
        df_rep = simulate(model, schedule, run_time, warm_up, seed, day_cv=day_cv)
        st = rep_stats(df_rep, schedule, eff_hour_len)
        reps_data.append(st)
        for h, h_st in enumerate(st["hourly"]):
            hourly_reps[h].append(h_st)
            
    # Tinh CI95 toan ngay
    sl_vals = [r["sl_all"] for r in reps_data]
    wq_vals = [r["wq_all"] for r in reps_data]
    p_ab_vals = [r["p_ab_all"] for r in reps_data]
    util_vals = [r.get("util_all", 0.0) for r in reps_data]
    vip_vals = [r["sl_vip"] for r in reps_data if not np.isnan(r["sl_vip"])]
    
    m_sl, ci_sl, (low_sl, high_sl) = mean_ci(sl_vals)
    m_wq, ci_wq, (low_wq, high_wq) = mean_ci(wq_vals)
    m_ab, ci_ab, (low_ab, high_ab) = mean_ci(p_ab_vals)
    m_ut, ci_ut, (low_ut, high_ut) = mean_ci(util_vals)

    # Chi so xac suat dat SLA theo ngay
    sl_day_ge90 = float(sum(1 for s in sl_vals if s >= 0.90) / n_reps) if n_reps > 0 else 0.0
    all_hours_ge90_cnt = 0
    cnt_below_list = []
    for rep_i in range(n_reps):
        all_ok = True
        cnt_below = 0
        for h in range(len(schedule)):
            if hourly_reps[h][rep_i]["sl"] < 0.90:
                all_ok = False
                cnt_below += 1
        if all_ok:
            all_hours_ge90_cnt += 1
        cnt_below_list.append(cnt_below)
    sl_allhours_ge90 = float(all_hours_ge90_cnt / n_reps) if n_reps > 0 else 0.0
    avg_hours_below = float(np.mean(cnt_below_list)) if n_reps > 0 else 0.0
    sl_p5 = float(np.percentile(sl_vals, 5)) if n_reps > 0 else 0.0
    sl_p95 = float(np.percentile(sl_vals, 95)) if n_reps > 0 else 0.0
    
    if len(vip_vals) > 0:
        m_vip, ci_vip, (low_vip, high_vip) = mean_ci(vip_vals)
    else:
        m_vip, ci_vip, low_vip, high_vip = np.nan, np.nan, np.nan, np.nan
    
    # Theo gio
    hourly_summary = []
    for h, h_list in enumerate(hourly_reps):
        sl_h_vals = [x["sl"] for x in h_list]
        sl_vip_h = [x["sl_vip"] for x in h_list if not np.isnan(x["sl_vip"])]
        wq_h_vals = [x["wq"] for x in h_list]
        ab_h_vals = [x["p_ab"] for x in h_list]
        util_h_vals = [x["util"] for x in h_list]
        
        m_sl_h, ci_sl_h, (low_sl_h, high_sl_h) = mean_ci(sl_h_vals)
        m_wq_h, ci_wq_h, _ = mean_ci(wq_h_vals)
        m_ab_h, ci_ab_h, _ = mean_ci(ab_h_vals)
        m_ut_h, ci_ut_h, _ = mean_ci(util_h_vals)
        
        if len(sl_vip_h) > 0:
            m_vip_h, ci_vip_h, (low_vip_h, _) = mean_ci(sl_vip_h)
        else:
            m_vip_h, ci_vip_h, low_vip_h = np.nan, np.nan, np.nan
        
        hourly_summary.append({
            "hour": h,
            "c": schedule[h],
            "sl_mean": round(m_sl_h, 4),
            "sl_ci95_low": round(low_sl_h, 4),
            "sl_ci95_high": round(high_sl_h, 4),
            "sl_ci_half": round(ci_sl_h, 4),
            "sl_vip_mean": round(m_vip_h, 4) if not np.isnan(m_vip_h) else np.nan,
            "sl_vip_ci95_low": round(low_vip_h, 4) if not np.isnan(low_vip_h) else np.nan,
            "wq_mean": round(m_wq_h, 4),
            "wq_ci_half": round(ci_wq_h, 4),
            "p_ab_mean": round(m_ab_h, 4),
            "p_ab_ci_half": round(ci_ab_h, 4),
            "util_mean": round(m_ut_h, 4),
            "util_ci_half": round(ci_ut_h, 4)
        })
        
    return {
        "n_reps": n_reps,
        "sl_mean": round(m_sl, 4),
        "sl_ci95": [round(low_sl, 4), round(high_sl, 4)],
        "sl_ci_half": round(ci_sl, 4),
        "sl_vip_mean": round(m_vip, 4) if not np.isnan(m_vip) else np.nan,
        "sl_vip_ci95": [round(low_vip, 4), round(high_vip, 4)] if not np.isnan(low_vip) else None,
        "sl_vip_ci_half": round(ci_vip, 4) if not np.isnan(ci_vip) else np.nan,
        "wq_mean": round(m_wq, 4),
        "wq_ci_half": round(ci_wq, 4),
        "p_ab_mean": round(m_ab, 4),
        "p_ab_ci_half": round(ci_ab, 4),
        "util_mean": round(m_ut, 4),
        "util_ci_half": round(ci_ut, 4),
        "sl_day_ge90_prob": round(sl_day_ge90, 4),
        "sl_allhours_ge90_prob": round(sl_allhours_ge90, 4),
        "avg_hours_below_90": round(avg_hours_below, 2),
        "sl_p5": round(sl_p5, 4),
        "sl_p95": round(sl_p95, 4),
        "hourly": hourly_summary
    }

# =============================================================================
# 4. CAC THI NGHIEM BO SUNG (HANG CHUNG VS HANG RIENG, WELCH WARM-UP)
# =============================================================================

def simulate_separate(
    lam: float,
    mu: float,
    c: int,
    run_time: float = 5000.0,
    policy: str = "random",
    seed: int = 42
) -> Dict:
    """
    Mo phong he thong c hang doi rieng le:
    policy = 'random': khach chon ngau nhien deu vao 1 trong c quay
    policy = 'jsq': khach chon hang co so nguoi it nhat (Join the Shortest Queue)
    """
    rng = np.random.default_rng(seed)
    env = simpy.Environment()
    resources = [simpy.Resource(env, capacity=1) for _ in range(c)]
    records = []

    def customer(cid: int, q_idx: int):
        arr_time = env.now
        svc_time = float(rng.exponential(1.0 / mu))
        with resources[q_idx].request() as req:
            yield req
            wait_time = env.now - arr_time
            yield env.timeout(svc_time)
            records.append({"cid": cid, "wait": wait_time, "served": 1})

    def arrival_gen():
        cid = 0
        while env.now < run_time:
            inter = rng.exponential(1.0 / lam)
            yield env.timeout(inter)
            if env.now >= run_time:
                break
            if policy == "random":
                q_idx = int(rng.integers(c))
            elif policy == "jsq":
                # Chon hang co so khach dang cho it nhat
                q_idx = int(np.argmin([len(res.queue) for res in resources]))
            else:
                q_idx = 0
            env.process(customer(cid, q_idx))
            cid += 1

    env.process(arrival_gen())
    env.run(until=run_time + 500.0)
    
    df = pd.DataFrame(records)
    sl = ((df["wait"] <= WAIT_THRESHOLD).sum() / len(df)) if len(df) > 0 else 0.0
    wq = df["wait"].mean() if len(df) > 0 else 0.0
    return {"policy": policy, "sl": float(sl), "wq": float(wq)}

def welch_curve(
    lam: float = 1.8,
    mu: float = 1.0 / 3.0,
    c: int = 6,
    n_reps: int = 30,
    n_cust: int = 1200,
    window: int = 50,
    seed_base: int = 42
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Tao duong cong Welch de xac dinh giai doan warm-up:
    Theo doi thoi gian cho Wq theo thu tu khach hang den qua nhieu lan lap doc lap.
    """
    all_reps_wait = np.zeros((n_reps, n_cust))
    
    for i in range(n_reps):
        rng = np.random.default_rng(seed_base + i * 100)
        env = simpy.Environment()
        res = simpy.Resource(env, capacity=c)
        waits = []

        def cust():
            arr = env.now
            svc = float(rng.exponential(1.0 / mu))
            with res.request() as req:
                yield req
                w = env.now - arr
                waits.append(w)
                yield env.timeout(svc)

        def arr_gen():
            for _ in range(n_cust):
                yield env.timeout(rng.exponential(1.0 / lam))
                env.process(cust())

        env.process(arr_gen())
        env.run()
        all_reps_wait[i, :] = waits[:n_cust]
        
    # Trung binh qua cac lan lap
    mean_curve = np.mean(all_reps_wait, axis=0)
    
    # Trung binh truot (Moving Average)
    smoothed = np.convolve(mean_curve, np.ones(window) / window, mode="valid")
    return mean_curve, smoothed

# =============================================================================
# 5. THUAT TOAN TOI UU LICH QUAY DUA TREN MO PHONG (SIMULATION OPTIMIZATION)
# =============================================================================

def is_schedule_feasible(eval_res: Dict, target_sla: float = TARGET_SLA) -> Tuple[bool, List[int]]:
    """
    Kiem tra lich co thoa man SLA (feasible) khong:
    Dung can duoi CI95 cua SL theo tung gio: sl_ci95_low >= target_sla.
    Tra ve (feasible, danh sach cac gio bi vi pham).
    """
    violated = []
    for h_info in eval_res["hourly"]:
        h = h_info["hour"]
        if h_info["sl_ci95_low"] < target_sla:
            violated.append(h)
    return len(violated) == 0, violated

def optimize_schedule(
    model: Model,
    initial_schedule: Optional[List[int]] = None,
    target_sla: float = TARGET_SLA,
    n_reps: int = 60,
    c_cap: int = 15,
    seed_base: int = 1000
) -> Dict:
    """
    Thuat toan toi uu lich quay 2 pha dua tren mo phong SimPy:
    - Khoi tao: Tu lich SIPP (hoac initial_schedule truyen vao).
    - Pha 1 (Ramp-up): Chay mo phong n_reps lan lap voi CRN.
      Moi vong kiem tra gio nao co can duoi CI95 < target_sla thi tang 1 quay.
      Lap lai den khi moi gio deu dat SLA hoac dat c_cap.
    - Pha 2 (Reduction/Pruning): Thu giam 1 quay o tung gio (bat dau tu gio nhieu quay nhat).
      Giu nguyen giam neu toan bo lich van dat SLA (feasible).
    Tra ve: {"schedule": optimal_schedule, "history": history, "eval": eval_final}
    """
    if initial_schedule is None:
        import b_theory as th
        sched = th.sipp_schedule(model.rates, 1.0 / model.mean_svc, model.theta, target=target_sla)
    else:
        sched = list(initial_schedule)
        
    history = []
    
    # --- PHA 1: TANG QUAY CHO DEN KHI DAT SLA ---
    step = 0
    max_steps_phase1 = 25
    
    while step < max_steps_phase1:
        eval_res = run_reps(model, sched, n_reps=n_reps, seed_base=seed_base)
        feas, violated = is_schedule_feasible(eval_res, target_sla)
        
        worst_hour = min(eval_res["hourly"], key=lambda x: x["sl_ci95_low"])
        worst_sl_low = worst_hour["sl_ci95_low"]
        
        history.append({
            "step": step,
            "phase": 1,
            "schedule": list(sched),
            "total_c_hours": sum(sched),
            "sl_mean": eval_res["sl_mean"],
            "worst_hour": worst_hour["hour"],
            "worst_sl_low": worst_sl_low,
            "violated_hours": list(violated),
            "feasible": feas
        })
        
        if feas:
            break
            
        # Tang 1 quay cho cac gio bi vi pham
        for vh in violated:
            if sched[vh] < c_cap:
                sched[vh] += 1
        step += 1
        
    # --- PHA 2: TIAT BOT QUAY DU THUA (PRUNING) ---
    sorted_hours = sorted(range(len(sched)), key=lambda h: sched[h], reverse=True)
    
    for h in sorted_hours:
        if sched[h] > 1:
            test_sched = list(sched)
            test_sched[h] -= 1
            eval_test = run_reps(model, test_sched, n_reps=n_reps, seed_base=seed_base)
            feas_test, violated_test = is_schedule_feasible(eval_test, target_sla)
            
            step += 1
            worst_h_test = min(eval_test["hourly"], key=lambda x: x["sl_ci95_low"])
            history.append({
                "step": step,
                "phase": 2,
                "tried_hour_reduction": h,
                "schedule": list(test_sched),
                "total_c_hours": sum(test_sched),
                "sl_mean": eval_test["sl_mean"],
                "worst_hour": worst_h_test["hour"],
                "worst_sl_low": worst_h_test["sl_ci95_low"],
                "violated_hours": list(violated_test),
                "feasible": feas_test,
                "accepted": feas_test
            })
            
            if feas_test:
                sched = test_sched # Chap nhan cat giam
                
    # Danh gia lai lich cuoi cung
    final_eval = run_reps(model, sched, n_reps=n_reps, seed_base=seed_base)
    return {
        "schedule": sched,
        "history": history,
        "eval": final_eval
    }
