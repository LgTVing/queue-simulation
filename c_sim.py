"""
c_sim.py: Dong co mo phong su kien roi rac bang SimPy (Tuan 2):
1. Mo phong quay phuc vu ngan hang voi PriorityResource (VIP, khach thuong)
2. Khach bo ve do het kien nhan (Abandonment)
3. Dieu chinh so quay linh hoat theo gio bang Blocker process
4. Thong ke, tinh khoang tin cay (CI95) va danh gia kha thi SLA
5. Mo phong he thong hang tach rieng (Random vs JSQ) va duong Welch chon warm-up
"""

import os
import atexit
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from typing import List, Dict, Tuple, Optional, Callable, Sequence
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
                    "served": 1,
                    "start_svc": start_service,
                    "end_svc": end_service
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
                    "served": 0,
                    "start_svc": np.nan,
                    "end_svc": np.nan
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
                "served": 1,
                "start_svc": start_service,
                "end_svc": env.now
            })

DRAIN_POLICIES = ("keep_last", "all_open")
RECORD_COLUMNS = ["cid", "hour", "vip", "arr_time", "wait", "svc", "served", "start_svc", "end_svc"]

class _CounterState:
    """Trang thai quay dung chung giua counter_blocker_process va surge_monitor (M8)."""
    def __init__(self):
        self.block_reqs: List = []   # blocker cua gio hien tai (ke ca blocker surge_monitor tao lai)
        self.extra = 0               # so quay du phong dang mo them
        self.extra_minutes = 0.0     # tong phut-quay du phong da mo
        self.n_open = 0              # so lan mo them quay


def counter_blocker_process(
    env: simpy.Environment,
    resource: simpy.PriorityResource,
    c_max: int,
    schedule: List[int],
    hour_len: float,
    drain_policy: str = "keep_last",
    state: Optional[_CounterState] = None
):
    """
    Tien trinh dieu chinh so quay theo gio:
    Trong khung gio h, chi cho phep schedule[h] quay hoat dong.
    c_max - schedule[h] quay con lai bi chiem giu boi blocker voi priority cao nhat (-1).
    drain_policy = 'keep_last': sau gio dong cua giu nguyen so quay cua gio cuoi
        cho den khi phuc vu xong khach da vao hang (gia dinh chinh, F1).
    drain_policy = 'all_open': nha het blocker sau gio cuoi -> mo toan bo c_max quay
        de xa hang (hanh vi cu V1-V3, chi dung de doi chieu).
    """
    if drain_policy not in DRAIN_POLICIES:
        raise ValueError(f"drain_policy khong hop le: {drain_policy}")
    if state is None:
        state = _CounterState()
    for h, active_c in enumerate(schedule):
        # Quay du phong dang mo (M8) duoc giu qua ranh gioi gio
        needed_blocks = max(0, c_max - active_c - state.extra)
        # Chiem giu so quay khong hoat dong
        state.block_reqs = [resource.request(priority=-1) for _ in range(needed_blocks)]

        if h == len(schedule) - 1 and drain_policy == "keep_last":
            return

        yield env.timeout(hour_len)

        # Giai phong khi chuyen gio (de gio sau thiet lap lai).
        # Blocker chua duoc cap quay phai cancel() de go khoi hang doi,
        # neu chi release() thi request van nam trong hang va chiem quay ve sau.
        for req in state.block_reqs:
            if req.triggered:
                resource.release(req)
            else:
                req.cancel()


def surge_monitor(
    env: simpy.Environment,
    resource: simpy.PriorityResource,
    state: _CounterState,
    policy: Dict,
    close_time: float
):
    """
    M8: moi phut dem so khach dang cho (request priority >= 0 trong hang).
    - Hang cho > threshold lien tuc window phut, con duoi max_extra va chua dong cua:
      mo them 1 quay (huy 1 blocker dang cho, neu khong co thi nha 1 blocker dang giu quay).
    - Hang cho = 0 va quay mo them gan nhat da mo >= min_hold phut: khoa lai 1 quay
      (blocker moi chi chiem quay khi nhan vien phuc vu xong, khong ngat khach).
    Khong dung rng nen khong lam doi day so ngau nhien cua khach.
    """
    thr, window = policy["threshold"], policy.get("window", 10)
    max_extra, min_hold = policy.get("max_extra", 1), policy.get("min_hold", 30)
    above, opened_at = 0, []
    while True:
        yield env.timeout(1.0)
        state.extra_minutes += state.extra
        q = sum(1 for r in resource.queue if r.priority >= 0)
        above = above + 1 if q > thr else 0
        if above >= window and state.extra < max_extra and env.now < close_time:
            pending = [r for r in state.block_reqs if not r.triggered]
            held = [r for r in state.block_reqs if r.triggered]
            if pending:
                req = pending[-1]
                req.cancel()
            elif held:
                req = held[-1]
                resource.release(req)
            else:
                continue
            state.block_reqs.remove(req)
            state.extra += 1
            state.n_open += 1
            opened_at.append(env.now)
            above = 0
        elif q == 0 and state.extra > 0 and env.now - opened_at[-1] >= min_hold:
            state.block_reqs.append(resource.request(priority=-1))
            state.extra -= 1
            opened_at.pop()

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
    day_multiplier: Optional[float] = None,
    drain_policy: str = "keep_last",
    surge_policy: Optional[Dict] = None
) -> pd.DataFrame:
    """
    Chay 1 dot mo phong don le.
    Tra ve DataFrame ghi nhan chi tiet lich su moi khach hang.
    day_cv > 0: ap dung he so nhan ngay m_d ~ Gamma(1/day_cv^2, day_cv^2).
    day_multiplier: truyen truc tiep gia tri he so nhan ngay (neu co).
    drain_policy: cach xu ly so quay sau gio dong cua (xem counter_blocker_process).
    surge_policy (M8): None = hanh vi cu (ket qua khong doi); dict {"threshold", "window",
        "max_extra", "min_hold"} = mo them quay khi hang cho dai (xem surge_monitor).
        Phut-quay du phong va so lan mo ghi o df.attrs["extra_counter_min"], df.attrs["n_surge"].
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
    if surge_policy is not None:
        c_max += surge_policy.get("max_extra", 1)
    resource = simpy.PriorityResource(env, capacity=c_max)
    records = []

    total_time = run_time if run_time is not None else float(len(schedule) * model.hour_len)
    hour_len = model.hour_len
    state = _CounterState()

    # Khoi chay tien trinh dieu phoi lich quay neu lich co su thay doi
    if len(schedule) > 1:
        env.process(counter_blocker_process(env, resource, c_max, schedule, hour_len, drain_policy, state))
        if surge_policy is not None:
            env.process(surge_monitor(env, resource, state, surge_policy, len(schedule) * hour_len))

    def arrival_generator():
        """
        Qua trinh Poisson khong dong nhat voi lambda hang so tung khuc (F2).
        Neu lan den tiep theo vuot qua ranh gioi khung gio, nhay toi ranh gioi
        va rut lai voi lambda cua gio moi (hop le nho tinh khong nho cua phan phoi mu).
        Chi so gio duoc dem bang bien h thay vi env.now // hour_len de tranh sai so
        dau phay dong ngay tai ranh gioi.
        """
        cid = 0
        n_h = len(model.rates)
        # Khuc lambda hang so: (ranh gioi, lambda goc, gio). Mac dinh 1 khuc/gio (ranh gioi nhu V4);
        # S15: sub_rates[h] chia gio h thanh cac khuc deu nhau, gio cua khach van la h.
        segs = []
        for h in range(n_h):
            end_h = min((h + 1) * hour_len, total_time) if h < n_h - 1 else total_time
            sub = model.sub_rates[h] if model.sub_rates is not None and h < len(model.sub_rates) else None
            if sub:
                for i, r in enumerate(sub):
                    b = end_h if i == len(sub) - 1 else min(h * hour_len + (i + 1) * hour_len / len(sub), end_h)
                    segs.append((b, r, h))
            else:
                segs.append((end_h, model.rates[h], h))
        j = 0
        while True:
            boundary, lam_base, h = segs[j]
            lam = lam_base * m_d
            if lam > 0:
                inter_arr = rng.exponential(1.0 / lam)
            if lam <= 0 or env.now + inter_arr >= boundary:
                if boundary - env.now > 0:
                    yield env.timeout(boundary - env.now)
                if boundary >= total_time or j == len(segs) - 1:
                    break
                j += 1
                continue
            yield env.timeout(inter_arr)

            # Sinh thuoc tinh khach hang
            h_arrival = h
            if isinstance(model.p_vip, (list, tuple, np.ndarray)):
                pv = model.p_vip[h_arrival] if h_arrival < len(model.p_vip) else model.p_vip[-1]
            else:
                pv = model.p_vip
            is_vip = 1 if rng.random() < pv else 0
            svc_h = model.service_by_hour[h_arrival] if model.service_by_hour is not None else None
            svc_time, _ = (svc_h or model.service)(rng)

            if model.patience is not None:
                patience = model.patience(rng)
            else:
                patience = rng.exponential(1.0 / model.theta) if model.theta > 0 else float("inf")
            
            env.process(customer_process(
                env, cid, h_arrival, is_vip, svc_time, patience, resource, records
            ))
            cid += 1

    env.process(arrival_generator())
    env.run(until=total_time + 1000.0) # Cho den khi giai phong het khach
    
    df = pd.DataFrame(records)
    if len(df) == 0:
        return pd.DataFrame(columns=RECORD_COLUMNS)
        
    # Loai bo doan warm-up neu co
    if warm_up > 0:
        df = df[df["arr_time"] >= warm_up].copy()
    if surge_policy is not None:
        df.attrs["extra_counter_min"] = state.extra_minutes
        df.attrs["n_surge"] = state.n_open

    return df

# =============================================================================
# 3. TINH TOAN CHI SO THONG KE TUNG DOT CHAY VA NHIEU DOT LAP
# =============================================================================

def rep_stats(
    df: pd.DataFrame,
    schedule: List[int],
    hour_len: float = 60.0,
    wait_thresh: float = WAIT_THRESHOLD,
    wait_thresh_vip: float = WAIT_THRESHOLD_VIP,
    t_start: float = 0.0,
    extra_thresh: Tuple[float, ...] = (2.0, 3.0)
) -> Dict:
    """
    Tinh toan cac chi so thong ke toan ngay va theo tung gio tu ket qua 1 dot chay.
    Khung gio h la [t_start + h*hour_len, t_start + (h+1)*hour_len).
    Hieu suat theo gio (F3) = thoi gian ban thuc te giao voi khung gio / (c_h * hour_len),
    tinh tu start_svc, end_svc cua tung khach; thoi gian ban sau gio dong cua
    duoc bao cao rieng o 'busy_after_close'.
    extra_thresh: cac nguong cho bo sung de bao cao SL toan ngay (vd 2 va 3 phut).
    """
    if len(df) == 0:
        return {"sl_all": 0.0, "sl_vip": 0.0, "wq_all": 0.0, "p_ab_all": 0.0, "hourly": []}

    # Trich mang NumPy mot lan (P2); wait khong bao gio NaN, svc chi NaN o khach bo ve
    # (bi loai boi served_mask) nen ket qua trung voi ban pandas.
    served_mask = df["served"].to_numpy() == 1
    wait = df["wait"].to_numpy(dtype=float)
    vip_mask = df["vip"].to_numpy() == 1
    hour_arr = df["hour"].to_numpy()

    # Toan ngay
    n_tot = len(df)
    n_served_sla = np.count_nonzero(served_mask & (wait <= wait_thresh))
    sl_all = n_served_sla / n_tot if n_tot > 0 else 0.0
    sl_extra = {
        f"sl_all_t{t:g}": float(np.count_nonzero(served_mask & (wait <= t)) / n_tot)
        for t in extra_thresh
    }

    n_vip = np.count_nonzero(vip_mask)
    n_vip_sla = np.count_nonzero(vip_mask & served_mask & (wait <= wait_thresh_vip))
    sl_vip = n_vip_sla / n_vip if n_vip > 0 else np.nan

    wq_all = wait.mean()
    p_ab_all = np.count_nonzero(~served_mask) / n_tot

    # Hieu suat su dung toan bo quay
    tot_svc_all = df["svc"].to_numpy(dtype=float)[served_mask].sum() if "svc" in df.columns else 0.0
    tot_c_time = sum(schedule) * hour_len
    util_all = tot_svc_all / tot_c_time if tot_c_time > 0 else 0.0

    # Khoang phuc vu thuc te (F3)
    if "start_svc" in df.columns:
        s_start = df["start_svc"].to_numpy(dtype=float)[served_mask]
        s_end = df["end_svc"].to_numpy(dtype=float)[served_mask]
    else:
        s_start = s_end = np.zeros(0)
    t_close = t_start + len(schedule) * hour_len
    busy_after_close = float(np.clip(s_end - np.maximum(s_start, t_close), 0.0, None).sum())

    # Theo tung khung gio
    hourly = []
    for h, c in enumerate(schedule):
        lo = t_start + h * hour_len
        hi = lo + hour_len
        busy_h = float(np.clip(np.minimum(s_end, hi) - np.maximum(s_start, lo), 0.0, None).sum())
        util_h = busy_h / (c * hour_len) if c > 0 and hour_len > 0 else 0.0
        in_h = hour_arr == h
        n_h = np.count_nonzero(in_h)
        if n_h == 0:
            hourly.append({"hour": h, "sl": 1.0, "sl_vip": 1.0, "wq": 0.0, "p_ab": 0.0, "util": float(util_h)})
            continue

        served_h = served_mask[in_h]
        wait_h = wait[in_h]
        vip_h = vip_mask[in_h]
        sl_h = np.count_nonzero(served_h & (wait_h <= wait_thresh)) / n_h
        n_h_vip = np.count_nonzero(vip_h)
        sl_h_vip = (np.count_nonzero(vip_h & served_h & (wait_h <= wait_thresh_vip)) / n_h_vip) if n_h_vip > 0 else np.nan
        wq_h = wait_h.mean()
        p_ab_h = np.count_nonzero(~served_h) / n_h

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
        "busy_after_close": busy_after_close,
        **sl_extra,
        "hourly": hourly
    }

# =============================================================================
# CHAY SONG SONG (P1)
# =============================================================================
# Moi dot chay co seed rieng (khong phu thuoc dot khac) nen chay song song cho
# ket qua giong het chay tuan tu, mien la gom ket qua dung thu tu job.
# QS_WORKERS=1: chay tuan tu (hanh vi cu). Mac dinh: min(so CPU - 1, 8); moi tien trinh con
# nap lai main.py (~145 MB) nen gioi han 8 de khong can RAM tren may 16 GB.
N_WORKERS = int(os.environ.get("QS_WORKERS") or max(1, min((os.cpu_count() or 2) - 1, 8)))
_POOL: Optional[ProcessPoolExecutor] = None


def _get_pool() -> ProcessPoolExecutor:
    global _POOL
    if _POOL is None:
        _POOL = ProcessPoolExecutor(max_workers=N_WORKERS)
        atexit.register(_POOL.shutdown)
    return _POOL


def _run_job(args):
    post, sim_kwargs, post_args = args
    return post(simulate(**sim_kwargs), *post_args)


def map_sim(jobs: Sequence[Dict], post: Callable, post_args: tuple = ()) -> List:
    """
    Chay simulate(**job) cho tung job roi tra ve post(df, *post_args), dung thu tu jobs.
    post phai la ham cap module (pickle duoc); job chua Model voi bo sinh pickle duoc.
    """
    global _POOL
    tasks = [(post, job, post_args) for job in jobs]
    if N_WORKERS <= 1 or len(tasks) < 2:
        return [_run_job(t) for t in tasks]
    chunk = max(1, len(tasks) // (N_WORKERS * 4))
    try:
        return list(_get_pool().map(_run_job, tasks, chunksize=chunk))
    except BrokenProcessPool:
        # Tien trinh con chet (thuong do thieu RAM): chay lai tuan tu, ket qua khong doi vi seed theo job
        print(f"  [canh bao] process pool hong, chay lai {len(tasks)} job tuan tu (giam QS_WORKERS neu lap lai)")
        _POOL = None
        return [_run_job(t) for t in tasks]


def _rep_stats_post(df: pd.DataFrame, schedule: List[int], hour_len: float, t_start: float) -> Dict:
    return rep_stats(df, schedule, hour_len, t_start=t_start)


def run_reps(
    model: Model,
    schedule: List[int],
    n_reps: int = 30,
    run_time: Optional[float] = None,
    warm_up: float = 0.0,
    seed_base: int = 42,
    day_cv: float = 0.0,
    drain_policy: str = "keep_last",
    keep_reps: bool = False
) -> Dict:
    """
    Chay n_reps lan lap doc lap su dung ky thuat so ngau nhien chung (CRN).
    Tinh trung binh, sai so chuan va khoang tin cay 95% cho moi chi so.
    day_cv > 0: ap dung bien dong he so nhan ngay.
    keep_reps: tra them ma tran SL theo gio tung lan lap (n_reps x H) va SL ngay
        tung lan lap, dung cho hieu so theo cap (CRN) va xac suat gio te nhat.
    """
    reps_data = []
    hourly_reps = [[] for _ in range(len(schedule))]

    # Xac dinh do dai gio hieu dung:
    # Neu he dung chay dai (len(schedule) == 1 va co run_time), do dai thuc te la run_time - warm_up
    # va khung do bat dau tu warm_up
    if run_time is not None and len(schedule) == 1:
        eff_hour_len = max(1.0, run_time - warm_up)
        t_start = warm_up
    else:
        eff_hour_len = model.hour_len
        t_start = 0.0

    jobs = [dict(model=model, schedule=schedule, run_time=run_time, warm_up=warm_up,
                 seed=seed_base + i * 1000, day_cv=day_cv, drain_policy=drain_policy)
            for i in range(n_reps)]
    for st in map_sim(jobs, _rep_stats_post, (schedule, eff_hour_len, t_start)):
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

    # SL toan ngay o cac nguong cho bo sung (2, 3 phut) va so lieu tung lan lap
    extra = {}
    for key in reps_data[0]:
        if key.startswith("sl_all_t"):
            m_x, ci_x, _ = mean_ci([r[key] for r in reps_data])
            extra[key.replace("sl_all_", "sl_") + "_mean"] = round(m_x, 4)
            extra[key.replace("sl_all_", "sl_") + "_ci_half"] = round(ci_x, 4)
    if keep_reps:
        extra["rep_sl_day"] = np.array(sl_vals)
        extra["rep_p_ab"] = np.array(p_ab_vals)
        extra["rep_sl_hourly"] = np.array([[hourly_reps[h][i]["sl"] for h in range(len(schedule))]
                                           for i in range(n_reps)])

    return {
        "n_reps": n_reps,
        **extra,
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

def summary_row(name: str, schedule: List[int], res: Dict, target_sla: float = TARGET_SLA) -> Dict:
    """Mot dong bang so sanh (gia tri so, khong dinh dang chuoi) tu ket qua run_reps."""
    worst = min(res["hourly"], key=lambda x: x["sl_ci95_low"])
    return {
        "chinh_sach": name,
        "lich_quay": str(list(schedule)),
        "quay_gio": int(sum(schedule)),
        "n_reps": res["n_reps"],
        "sl_toan_ngay": res["sl_mean"],
        "sl_ci_half": res["sl_ci_half"],
        "sl_2p": res.get("sl_t2_mean", np.nan),
        "sl_3p": res.get("sl_t3_mean", np.nan),
        "gio_te_nhat": worst["hour"],
        "sl_gio_te_nhat": worst["sl_mean"],
        "sl_gio_te_nhat_low": worst["sl_ci95_low"],
        "sl_vip": res["sl_vip_mean"],
        "ti_le_bo_ve": res["p_ab_mean"],
        "ti_le_bo_ve_ci_half": res["p_ab_ci_half"],
        "wq_phut": res["wq_mean"],
        "wq_ci_half": res["wq_ci_half"],
        "hieu_suat_rho": res["util_mean"],
        "rho_ci_half": res["util_ci_half"],
        "dat_sla": "Y" if worst["sl_ci95_low"] >= target_sla else "N"
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

def is_schedule_feasible(
    eval_res: Dict,
    target_sla: float = TARGET_SLA,
    max_p_ab: Optional[float] = None
) -> Tuple[bool, List[int]]:
    """
    Kiem tra lich co thoa man SLA (feasible) khong:
    Dung can duoi CI95 cua SL theo tung gio: sl_ci95_low >= target_sla.
    max_p_ab (M2): neu khac None, them rang buoc can tren CI95 cua ti le bo ve
    toan ngay <= max_p_ab; khi vi pham, gio co ti le bo ve cao nhat duoc
    dua vao danh sach vi pham (de pha 1 tang quay o gio do).
    Tra ve (feasible, danh sach cac gio bi vi pham).
    """
    violated = []
    for h_info in eval_res["hourly"]:
        h = h_info["hour"]
        if h_info["sl_ci95_low"] < target_sla:
            violated.append(h)
    if max_p_ab is not None and eval_res["p_ab_mean"] + eval_res["p_ab_ci_half"] > max_p_ab:
        worst_ab = max(eval_res["hourly"], key=lambda x: x["p_ab_mean"])["hour"]
        if worst_ab not in violated:
            violated.append(worst_ab)
    return len(violated) == 0, violated

def optimize_schedule(
    model: Model,
    initial_schedule: Optional[List[int]] = None,
    target_sla: float = TARGET_SLA,
    n_reps: int = 60,
    c_cap: int = 15,
    seed_base: int = 1000,
    max_p_ab: Optional[float] = None
) -> Dict:
    """
    Thuat toan toi uu lich quay 2 pha dua tren mo phong SimPy:
    - Khoi tao: Tu lich SIPP (hoac initial_schedule truyen vao).
    - Pha 1 (Ramp-up): Chay mo phong n_reps lan lap voi CRN.
      Moi vong kiem tra gio nao co can duoi CI95 < target_sla thi tang 1 quay.
      Lap lai den khi moi gio deu dat SLA hoac dat c_cap.
    - Pha 2 (Reduction/Pruning): Thu giam 1 quay o tung gio (bat dau tu gio nhieu quay nhat).
      Giu nguyen giam neu toan bo lich van dat SLA (feasible).
    max_p_ab: rang buoc ti le bo ve toan ngay (M2), None = khong rang buoc.
    Tra ve: {"schedule": optimal_schedule, "history": history, "eval": eval_final,
             "feasible": lich cuoi co dat tieu chi kha thi (F10; False khi Pha 1 het buoc / cham c_cap)}
    """
    def feasible(res):
        return is_schedule_feasible(res, target_sla, max_p_ab)

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
        feas, violated = feasible(eval_res)

        worst_hour = min(eval_res["hourly"], key=lambda x: x["sl_ci95_low"])
        worst_sl_low = worst_hour["sl_ci95_low"]

        history.append({
            "step": step,
            "phase": 1,
            "schedule": list(sched),
            "total_c_hours": sum(sched),
            "sl_mean": eval_res["sl_mean"],
            "p_ab_mean": eval_res["p_ab_mean"],
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
            feas_test, violated_test = feasible(eval_test)

            step += 1
            worst_h_test = min(eval_test["hourly"], key=lambda x: x["sl_ci95_low"])
            history.append({
                "step": step,
                "phase": 2,
                "tried_hour_reduction": h,
                "schedule": list(test_sched),
                "total_c_hours": sum(test_sched),
                "sl_mean": eval_test["sl_mean"],
                "p_ab_mean": eval_test["p_ab_mean"],
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
    final_feas, final_viol = feasible(final_eval)
    if not final_feas:
        print(f"  [canh bao] optimize_schedule: lich {sched} khong kha thi (gio vi pham {final_viol})")
    return {
        "schedule": sched,
        "history": history,
        "eval": final_eval,
        "feasible": final_feas
    }

def local_search_phase3(
    model: Model,
    schedule: List[int],
    target_sla: float = TARGET_SLA,
    n_reps: int = 60,
    seed_base: int = 1000,
    max_p_ab: Optional[float] = None
) -> List[Dict]:
    """
    Pha 3: kiem tra tinh toi thieu cuc bo cua lich bang mo phong (cung seed voi toi uu):
    - Swap: bot 1 quay o gio i, them 1 quay o gio j (giu tong quay-gio).
    - Giam 2 quay: bot 1 quay o hai gio i <= j (giam tong 2 quay-gio).
    Lich la toi thieu cuc bo neu khong co phep giam 2 quay nao kha thi.
    """
    candidates = []
    n_h = len(schedule)
    for i in range(n_h):
        for j in range(n_h):
            if i != j and schedule[i] > 1:
                cand = list(schedule)
                cand[i] -= 1
                cand[j] += 1
                candidates.append(("Swap 1 quay", i, j, cand))
    for i in range(n_h):
        for j in range(i, n_h):
            cand = list(schedule)
            cand[i] -= 1
            cand[j] -= 1
            if min(cand) >= 1:
                candidates.append(("Giam 2 quay", i, j, cand))

    rows = []
    for kind, i, j, cand in candidates:
        res = run_reps(model, cand, n_reps=n_reps, seed_base=seed_base)
        feas, violated = is_schedule_feasible(res, target_sla, max_p_ab)
        worst = min(res["hourly"], key=lambda x: x["sl_ci95_low"])
        rows.append({
            "loai_thu_nghiem": kind,
            "gio_i": i,
            "gio_j": j,
            "lich_thu_nghiem": str(cand),
            "tong_quay_gio": sum(cand),
            "sl_toan_ngay": res["sl_mean"],
            "gio_te_nhat": worst["hour"],
            "sl_gio_te_nhat_low": worst["sl_ci95_low"],
            "ti_le_bo_ve": res["p_ab_mean"],
            "gio_vi_pham": str(violated),
            "kha_thi": "Y" if feas else "N"
        })
    return rows
