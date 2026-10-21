"""
b_theory.py: Mo hinh giai tich ly thuyet hang doi:
1. M/M/c (Erlang C)
2. M/G/c (Xap xi Allen-Cunneen)
3. Erlang-A (M/M/c + M, co khach bo ve va ma tran hap thu SL(t))
4. M/M/1 tach dong ngau nhien (Separate Queues)
5. Xac dinh so quay SIPP theo gio
"""

import math
from typing import Dict, List, Optional
import numpy as np
import scipy.linalg as la
import scipy.stats as stats

def mmc(lam: float, mu: float, c: int, t: float = 5.0) -> Dict[str, float]:
    """
    Mo hinh M/M/c co ban (Erlang C).
    lam: toc do den (khach/phut)
    mu: toc do phuc vu 1 quay (khach/phut)
    c: so quay phuc vu
    t: nguong thoi gian cho SLA (phut)
    """
    if c <= 0 or mu <= 0:
        return {"Pw": 1.0, "Wq": float("inf"), "Lq": float("inf"), "P_sla": 0.0, "rho": float("inf")}
    
    a = lam / mu
    rho = a / c
    
    # Neu he thong qua tai hoac khong on dinh (rho >= 1)
    if rho >= 1.0:
        return {"Pw": 1.0, "Wq": float("inf"), "Lq": float("inf"), "P_sla": 0.0, "rho": rho}
    
    # Tinh Pw = C(c, a)
    # Dung Poisson tranh tran so: p(k) = e^-a * a^k / k!
    sum_k = sum((a**k) / math.factorial(k) for k in range(c))
    term_c = (a**c) / (math.factorial(c) * (1.0 - rho))
    Pw = term_c / (sum_k + term_c)
    
    # Wq, Lq
    Wq = Pw / (c * mu - lam)
    Lq = lam * Wq
    
    # P(Wq <= t) = 1 - C * exp(-(c*mu - lam)*t)
    P_sla = 1.0 - Pw * math.exp(-(c * mu - lam) * t)
    
    return {
        "Pw": float(Pw),
        "Wq": float(Wq),
        "Lq": float(Lq),
        "P_sla": float(P_sla),
        "rho": float(rho)
    }

def allen_cunneen(lam: float, es: float, cs2: float, c: int) -> float:
    """
    Xap xi Allen-Cunneen cho hang doi M/G/c:
    Wq(M/G/c) ~= (1 + cs^2)/2 * Wq(M/M/c)
    lam: toc do den (khach/phut)
    es: thoi gian phuc vu TB (phut) -> mu = 1/es
    cs2: binh phuong he so bien thien thoi gian phuc vu
    c: so quay
    """
    mu = 1.0 / es if es > 0 else 0.0
    res_mmc = mmc(lam, mu, c)
    if math.isinf(res_mmc["Wq"]):
        return float("inf")
    return float((1.0 + cs2) / 2.0 * res_mmc["Wq"])

def mm1_random_split(lam: float, mu: float, c: int, t: float = 5.0) -> float:
    """
    He thong c hang doi doc lap, khach chon ngau nhien deu vao 1 trong c quay.
    Moi quay la 1 he M/M/1 doc lap voi toc do den lam/c.
    Tra ve xac suat cho <= t: P(Wq <= t) = 1 - rho * exp(-mu*(1 - rho)*t)
    """
    if c <= 0 or mu <= 0:
        return 0.0
    lam_i = lam / c
    rho = lam_i / mu
    if rho >= 1.0:
        return 0.0
    return float(1.0 - rho * math.exp(-mu * (1.0 - rho) * t))

def erlang_a(lam: float, mu: float, theta: float, c: int, t: float = 5.0, K: int = 200) -> Dict[str, float]:
    """
    Mo hinh Erlang-A (M/M/c + M): chuoi sinh tu co khach bo ve voi toc do theta.
    Tinh toan chinh xac:
    - SL(t) = P(khach duoc phuc vu VA cho <= t) bang ma tran hap thu Markov
    - Wq: thoi gian cho trung binh tren MOI khach (Lq / lam)
    - p_ab: ti le bo ve (theta * Lq / lam)
    - util: hieu suat thuc te cua quay
    """
    if theta <= 0:
        # Khi theta = 0, tro ve M/M/c
        res = mmc(lam, mu, c, t)
        return {
            "SL": res["P_sla"],
            "Wq": res["Wq"],
            "p_ab": 0.0,
            "util": res["rho"]
        }
    
    # 1. Tinh phan phoi xac suat dung pi_n
    pi = [1.0]
    for n in range(1, c + K + 1):
        death = min(n, c) * mu + max(n - c, 0) * theta
        pi.append(pi[-1] * lam / death)
    sum_pi = sum(pi)
    pi = [p / sum_pi for p in pi]
    
    Lq = sum(j * pi[c + j] for j in range(K + 1))
    Wq = Lq / lam if lam > 0 else 0.0
    p_ab = (theta * Lq / lam) if lam > 0 else 0.0
    util = (lam * (1.0 - p_ab) / (c * mu)) if (c * mu) > 0 else 0.0
    
    # 2. Tinh SL(t) chinh xac bang chuoi Markov hap thu
    M = min(K, 80)
    Q = np.zeros((M, M))
    for k in range(M):
        diag = -(c * mu + (k + 1) * theta) if k > 0 else -(c * mu + theta)
        Q[k, k] = diag
        if k > 0:
            Q[k, k - 1] = c * mu + k * theta
            
    P_trans = la.expm(Q * t)
    inv_Q = np.linalg.inv(Q)
    integral_P = (P_trans - np.eye(M)) @ inv_Q
    rate_served = np.zeros(M)
    rate_served[0] = c * mu
    p_served_before_t = integral_P @ rate_served
    
    sl_imm = sum(pi[n] for n in range(c))
    sl_wait = sum(pi[c + j] * p_served_before_t[j] for j in range(M))
    SL = sl_imm + sl_wait
    
    return {
        "SL": float(SL),
        "Wq": float(Wq),
        "p_ab": float(p_ab),
        "util": float(util)
    }

def sipp_schedule(
    rates: List[float],
    mu: float,
    theta: float,
    target: float = 0.90,
    t: float = 5.0,
    use_erlang_a: bool = True
) -> List[int]:
    """
    Xac dinh so quay toi thieu theo tung khung gio (SIPP).
    Voi moi khung gio h co toc do den rates[h]:
    Tim c_min sao cho SL(t) >= target.
    """
    schedule = []
    for lam in rates:
        a = lam / mu
        c_start = max(1, int(math.floor(a)) + 1)
        found = False
        for c in range(c_start, c_start + 40):
            if use_erlang_a and theta > 0:
                res = erlang_a(lam, mu, theta, c, t)
                sl = res["SL"]
            else:
                res = mmc(lam, mu, c, t)
                sl = res["P_sla"]
            if sl >= target:
                schedule.append(c)
                found = True
                break
        if not found:
            schedule.append(c_start + 5)
    return schedule
