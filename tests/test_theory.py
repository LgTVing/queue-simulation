import math
import pytest
import b_theory as th

def test_mmc_reference():
    m = th.mmc(1.5, 1.0 / 3.0, 6)
    assert m["Pw"] == pytest.approx(0.4217, abs=5e-4)
    assert m["Wq"] == pytest.approx(0.8433, abs=5e-3)
    assert m["P_sla"] == pytest.approx(0.9654, abs=5e-4)

def test_mmc_unstable():
    m = th.mmc(2.0, 1.0 / 3.0, 6)  # rho = 1.0
    assert math.isinf(m["Wq"]) and m["P_sla"] == 0.0

def test_monotone_in_c():
    sl = [th.mmc(1.5, 1.0 / 3.0, c)["P_sla"] for c in range(5, 10)]
    assert all(b >= a for a, b in zip(sl, sl[1:]))

def test_erlang_a_reference():
    e = th.erlang_a(2.0, 1.0 / 3.0, 0.1, 6)
    assert e["SL"] == pytest.approx(0.8689, abs=5e-4)
    assert e["Wq"] == pytest.approx(1.1444, abs=5e-3)
    assert e["p_ab"] == pytest.approx(0.1144, abs=5e-4)
    assert e["util"] == pytest.approx(0.8856, abs=5e-4)

def test_allen_cunneen_reference():
    assert th.allen_cunneen(1.5, 3.0, 0.25, 6) == pytest.approx(0.5271, abs=5e-3)
    assert th.allen_cunneen(1.5, 3.0, 2.25, 6) == pytest.approx(1.3704, abs=5e-3)

def test_split_queues_worse():
    assert th.mm1_random_split(1.5, 1.0 / 3.0, 6) < th.mmc(1.5, 1.0 / 3.0, 6)["P_sla"]

def test_sipp_schedule_monotone():
    rates = [1.0, 1.5, 2.0]
    sched = th.sipp_schedule(rates, 1.0 / 3.0, 0.1, target=0.90)
    assert all(b >= a for a, b in zip(sched, sched[1:]))
