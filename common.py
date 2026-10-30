"""
common.py: Tham so dung chung, cau truc Model, bo sinh thoi gian phuc vu,
va cac ham tien ich thong ke cho du an mo phong hang doi.
"""

import os
from dataclasses import dataclass
from typing import Callable, Tuple, List, Optional, Union
import numpy as np
import scipy.stats as stats

# =============================================================================
# CAU HINH DUONG DAN VA PHIEN BAN KET QUA (NGUON DUY NHAT)
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_CLEAN = os.path.join(BASE_DIR, "data", "clean", "data_clean.csv")
RESULTS_VERSION = "final_v5"
# QS_RESULTS_DIR: ghi ket qua ra thu muc khac (chay thu / smoke test), khong dong vao ban dong bang
RESULTS_DIR = os.environ.get("QS_RESULTS_DIR") or os.path.join(BASE_DIR, "results", RESULTS_VERSION)
HINH_DIR = os.path.join(RESULTS_DIR, "hinh")

# Moc co so: so quay co dinh ca ngay (BASELINE_C * HOURS quay-gio)
BASELINE_C = 6

# He so nhan so lan lap (--reps-scale); 0.1 de chay nhanh khi phat trien
REPS_SCALE = 1.0

def set_reps_scale(scale: float) -> None:
    """Dat he so nhan so lan lap cho toan bo pipeline."""
    global REPS_SCALE
    REPS_SCALE = float(scale)

def scaled(n: int, min_n: int = 3) -> int:
    """So lan lap/so kich ban sau khi nhan REPS_SCALE (toi thieu min_n)."""
    return max(min_n, int(round(n * REPS_SCALE)))

def out_path(name: str, sub: str = "") -> str:
    """Duong dan tep ket qua trong RESULTS_DIR (tu tao thu muc)."""
    d = os.path.join(RESULTS_DIR, sub) if sub else RESULTS_DIR
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, name)

# Khung gio lam viec ban ngay (8h - 17h: 9 khung gio)
HOURS = 9
H_LABELS = [
    "8h-9h", "9h-10h", "10h-11h", "11h-12h", "12h-13h",
    "13h-14h", "14h-15h", "15h-16h", "16h-17h"
]

# Cam ket muc do dich vu (SLA)
TARGET_SLA = 0.90            # 90%
WAIT_THRESHOLD = 5.0         # 5 phut cho khach thuong
WAIT_THRESHOLD_VIP = 2.0     # 2 phut cho khach VIP
DEFAULT_HOUR_LEN = 60.0      # 60 phut moi khung gio

@dataclass
class Model:
    """Cau truc tham so he thong hang doi."""
    rates: List[float]                       # lambda_h (khach/phut) theo tung khung gio
    service: Callable[[np.random.Generator], Tuple[float, int]] # Sampler: rng -> (svc_time, cls)
    theta: float                             # Toc do bo ve (1/phut)
    p_vip: Union[float, List[float]] = 0.0   # Ti le khach VIP (co dinh hoac theo gio)
    hour_len: float = DEFAULT_HOUR_LEN       # Do dai moi khung gio (phut)
    mean_svc: float = 2.88                   # E[S] tham chieu (phut)
    cs2_svc: float = 1.20                    # cs^2 tham chieu


# =============================================================================
# CAC BO SINH THOI GIAN PHUC VU (SERVICE SAMPLERS)
# =============================================================================

# Cac bo sinh la class co __call__ (khong dung lambda/closure) de pickle duoc khi
# chay song song bang ProcessPoolExecutor tren Windows (spawn) - P1.
# Thu tu goi rng giu nguyen nhu ban lambda cu de ket qua khong doi.

class _ExpService:
    def __init__(self, mean: float):
        self.mean = mean

    def __call__(self, rng: np.random.Generator) -> Tuple[float, int]:
        return float(rng.exponential(self.mean)), 0


class _LognormService:
    def __init__(self, mu_log: float, sigma: float):
        self.mu_log, self.sigma = mu_log, sigma

    def __call__(self, rng: np.random.Generator) -> Tuple[float, int]:
        return float(rng.lognormal(self.mu_log, self.sigma)), 0


class _GammaService:
    def __init__(self, shape: float, scale: float):
        self.shape, self.scale = shape, scale

    def __call__(self, rng: np.random.Generator) -> Tuple[float, int]:
        return float(rng.gamma(self.shape, self.scale)), 0


class _WeibullService:
    def __init__(self, shape: float, scale: float):
        self.shape, self.scale = shape, scale

    def __call__(self, rng: np.random.Generator) -> Tuple[float, int]:
        return float(self.scale * rng.weibull(self.shape)), 0


class _EmpiricalService:
    def __init__(self, samples: np.ndarray):
        self.s = np.asarray(samples, dtype=float)
        self.n = len(self.s)

    def __call__(self, rng: np.random.Generator) -> Tuple[float, int]:
        return float(self.s[rng.integers(self.n)]), 0


class _MixService:
    def __init__(self, p_quick: float, quick_sampler, complex_sampler):
        self.p_quick = p_quick
        self.quick_sampler, self.complex_sampler = quick_sampler, complex_sampler

    def __call__(self, rng: np.random.Generator) -> Tuple[float, int]:
        if rng.random() < self.p_quick:
            svc, _ = self.quick_sampler(rng)
            return svc, 0
        svc, _ = self.complex_sampler(rng)
        return svc, 1


def exp_service(mean: float) -> Callable[[np.random.Generator], Tuple[float, int]]:
    """Phan phoi mu (Exponential) voi ky vong mean (cv = 1.0)."""
    return _ExpService(mean)

def lognorm_service(mean: float, cv: float) -> Callable[[np.random.Generator], Tuple[float, int]]:
    """Phan phoi Lognormal voi ky vong mean va he so bien thien cv."""
    sigma2 = np.log(1.0 + cv**2)
    sigma = np.sqrt(sigma2)
    mu_log = np.log(mean) - 0.5 * sigma2
    return _LognormService(mu_log, sigma)

def gamma_service(shape: float, scale: float) -> Callable[[np.random.Generator], Tuple[float, int]]:
    """Phan phoi Gamma voi tham so shape (k) va scale (theta)."""
    return _GammaService(shape, scale)

def weibull_service(shape: float, scale: float) -> Callable[[np.random.Generator], Tuple[float, int]]:
    """Phan phoi Weibull voi tham so shape (k) va scale (lambda)."""
    return _WeibullService(shape, scale)

def empirical_service(samples: np.ndarray) -> Callable[[np.random.Generator], Tuple[float, int]]:
    """Lay mau co hoan lai tu du lieu thuc te (Bootstrap)."""
    return _EmpiricalService(samples)

def mix_service(
    p_quick: float,
    quick_sampler: Callable[[np.random.Generator], Tuple[float, int]],
    complex_sampler: Callable[[np.random.Generator], Tuple[float, int]]
) -> Callable[[np.random.Generator], Tuple[float, int]]:
    """Hon hop hai loai dich vu: nhanh (cls=0) va phuc tap (cls=1)."""
    return _MixService(p_quick, quick_sampler, complex_sampler)


# =============================================================================
# TIEN ICH THONG KE VA TINH MOMENT
# =============================================================================

def mix_moments(p: float, m1: float, v1: float, m2: float, v2: float) -> Tuple[float, float, float]:
    """
    Tinh ky vong, phuong sai va cs^2 cua bien ngau nhien hon hop hai thanh phan.
    p: ti le loai 1, (m1, v1): ky vong va phuong sai loai 1, (m2, v2): loai 2.
    """
    mean = p * m1 + (1.0 - p) * m2
    es2 = p * (v1 + m1**2) + (1.0 - p) * (v2 + m2**2)
    var = es2 - mean**2
    cs2 = var / (mean**2) if mean > 0 else 0.0
    return mean, var, cs2

def mean_ci(data: np.ndarray, alpha: float = 0.05) -> Tuple[float, float, Tuple[float, float]]:
    """
    Tinh trung binh mau, do nua rong khoang tin cậy (CI half-width),
    va khoang tin cay (1 - alpha)% (mac dinh 95%).
    """
    arr = np.asarray(data, dtype=float)
    n = len(arr)
    if n == 0:
        return 0.0, 0.0, (0.0, 0.0)
    mean = float(np.mean(arr))
    if n == 1:
        return mean, 0.0, (mean, mean)
    std = float(np.std(arr, ddof=1))
    se = std / np.sqrt(n)
    t_val = stats.t.ppf(1.0 - alpha / 2.0, df=n - 1)
    half = float(t_val * se)
    return mean, half, (mean - half, mean + half)
