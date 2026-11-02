"""
tests/test_f4_seeds.py: Kiem thu so dang ky dai seed (F4, docs/KE_HOACH_V5_1.md):
1. Hang seed trong cac module lay dung tu common.SEED_BANDS
2. Cap "chon lich / danh gia" cua cung thi nghiem khong giao nhau
3. Cac trung lap da biet nhung giu de khong doi so V5 duoc danh dau xfail co ly do
"""

import pytest

import common
from common import SEED_BANDS, SEED_STEP, seed_range
import c_sim as cs
import d_experiments as dx
import h_staffing as hs
import f_scenarios as fs


def test_module_constants_from_registry():
    assert (dx.SEED_SELECT, dx.SEED_EVAL) == (SEED_BANDS["select"][0], SEED_BANDS["eval"][0])
    assert (hs.SEED_SELECT, hs.SEED_EVAL) == (dx.SEED_SELECT, dx.SEED_EVAL)
    assert hs.SEED_SELECT_DAY == SEED_BANDS["select_day"][0]
    assert hs.SEED_SCREEN_DAY == SEED_BANDS["screen_day"][0]
    assert (fs.SEED_EVAL_DAY, fs.N_EVAL_DAY) == SEED_BANDS["eval_day"]  # F5


def test_seed_range_matches_run_reps(monkeypatch):
    """seed_range sinh dung cac seed run_reps dung (seed_base + SEED_STEP * i)."""
    seen = []
    orig = cs.map_sim

    def spy(jobs, post, post_args=()):
        seen.extend(j["seed"] for j in jobs)
        return orig(jobs, post, post_args)

    monkeypatch.setattr(cs, "map_sim", spy)
    m = common.Model(rates=[0.5], service=common.exp_service(1.0), theta=0.1)
    cs.run_reps(m, [2], n_reps=4, seed_base=SEED_BANDS["select_day"][0])
    assert seen == list(seed_range("select_day", 4))


@pytest.mark.parametrize("a, b", [
    ("select_day", "eval_day"),     # M7: chon lich vs danh gia (F5)
    ("screen_day", "eval_day"),     # M7: sang loc vs danh gia
    ("select", "eval_day"),
    ("eval", "eval_day"),
])
def test_select_eval_disjoint(a, b):
    assert not set(seed_range(a)) & set(seed_range(b))


@pytest.mark.xfail(strict=True, reason="optimize/M6: trung 11/300, giu de khong doi so V5 (KE_HOACH_V5_1 F4, phuong an A)")
def test_select_eval_main_disjoint():
    assert not set(seed_range("select")) & set(seed_range("eval"))


@pytest.mark.xfail(strict=True, reason="S5 dung lai seed giua cac bo bootstrap; sua o F9 (KE_HOACH_V5_1)")
def test_nested_bootstrap_seeds_distinct():
    # Cong thuc trong e_robustness.nested_bootstrap: seed_base = 60000 + 100 b, lan lap + SEED_STEP * i
    seeds = [60000 + 100 * b + SEED_STEP * i for b in range(50) for i in range(60)]
    assert len(set(seeds)) == len(seeds)
