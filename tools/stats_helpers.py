"""
tools/stats_helpers.py:
Cac ham tien ich thong ke:
1. Khoang tin cay Wilson cho ti le (binomial proportion)
2. Khoang tin cay Student-t cho trung binh mau
3. Hieu chinh da so sanh Holm-Bonferroni
"""

import numpy as np
import scipy.stats as st

def wilson_ci(x, n, conf=0.95):
    """
    Tinh khoang tin cay Wilson cho ti le p = x / n.
    Tra ve: (p_hat, low, high, half_width)
    """
    if n <= 0:
        return 0.0, 0.0, 0.0, 0.0
    p = float(x) / float(n)
    alpha = 1.0 - conf
    z = st.norm.ppf(1.0 - alpha / 2.0)
    
    denom = 1.0 + (z**2) / n
    center = (p + (z**2) / (2.0 * n)) / denom
    margin = (z / denom) * np.sqrt((p * (1.0 - p) / n) + ((z**2) / (4.0 * n**2)))
    
    if x <= 0:
        low = 0.0
    else:
        low = max(0.0, float(center - margin))
        
    if x >= n:
        high = 1.0
    else:
        high = min(1.0, float(center + margin))
        
    hw = (high - low) / 2.0
    return float(p), float(low), float(high), float(hw)

def t_ci(data, conf=0.95):
    """
    Tinh khoang tin cay Student-t cho trung binh mang 1D.
    Tra ve: (mean, low, high, half_width, std)
    """
    arr = np.array(data, dtype=float)
    n = len(arr)
    if n < 2:
        m = float(np.mean(arr)) if n == 1 else 0.0
        return m, m, m, 0.0, 0.0
    m = float(np.mean(arr))
    s = float(np.std(arr, ddof=1))
    t_val = st.t.ppf(1.0 - (1.0 - conf) / 2.0, df=n - 1)
    hw = t_val * s / np.sqrt(n)
    return m, m - hw, m + hw, hw, s

def holm_bonferroni(p_values, alpha=0.05):
    """
    Hieu chinh da so sanh Holm-Bonferroni cho mang p-values.
    Tra ve: (adjusted_p_values, reject_flags)
    """
    p_vals = np.array(p_values, dtype=float)
    m = len(p_vals)
    order = np.argsort(p_vals)
    adj_p = np.zeros(m)
    
    running_max = 0.0
    for rank, idx in enumerate(order):
        # multiplier: m - rank
        raw_adj = p_vals[idx] * (m - rank)
        running_max = max(running_max, raw_adj)
        adj_p[idx] = min(1.0, running_max)
        
    reject = adj_p <= alpha
    return adj_p, reject
