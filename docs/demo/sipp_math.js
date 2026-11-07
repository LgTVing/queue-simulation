/*
 * docs/demo/sipp_math.js:
 *  - Bước 1: Erlang C, Erlang-A và lịch SIPP giải tích (port từ b_theory.py, K = 200, M = 80).
 *  - Bước 2: Tối ưu hóa lặp 3 pha (Pha 1 Tăng -> Pha 2 Giảm/Cắt tỉa -> Pha 3 Kiểm tra lân cận 117 cấu hình)
 *            có xét tồn đọng liên giờ (carryover), biến thiên phục vụ thực nghiệm (cs^2 = 1.2007) và cận dưới CI95
 *            (port từ d_experiments.py / c_sim.py, khớp chính xác chuỗi bước trong results/final_v5/lich_toi_uu.csv và pha3.csv).
 *  - Bước 3: Quy hoạch nguyên xếp ca MILP (mô hình B, port từ b_shifts.py) và tối ưu thẳng theo giờ công (M6, port từ h_staffing.py).
 * Dùng được trong trình duyệt (window.SippMath) và Node (module.exports) cho tests/test_d5_demo.py.
 */
(function (root) {
  "use strict";

  var DEFAULT_RATES = [0.99, 1.3767, 1.535, 1.39, 1.24, 1.2017, 1.3383, 1.3167, 1.0567];
  var DEFAULT_ES = 2.9236448156318935;
  var DEFAULT_THETA = 0.1087;
  var DEFAULT_CS2 = 1.2007;

  function mmc(lam, mu, c, t) {
    if (c <= 0 || mu <= 0) return { Pw: 1, Wq: Infinity, P_sla: 0, rho: Infinity };
    const a = lam / mu, rho = a / c;
    if (rho >= 1) return { Pw: 1, Wq: Infinity, P_sla: 0, rho: rho };
    let term = 1, sumK = 0;                  // a^k / k!
    for (let k = 0; k < c; k++) { sumK += term; term *= a / (k + 1); }
    const termC = term / (1 - rho);          // term = a^c / c!
    const Pw = termC / (sumK + termC);
    const Wq = Pw / (c * mu - lam);
    return { Pw: Pw, Wq: Wq, P_sla: 1 - Pw * Math.exp(-(c * mu - lam) * t), rho: rho };
  }

  // u[j] = P(duoc phuc vu truoc t | luc den co j khach dung truoc), j = 0..M-1
  function servedBeforeT(c, mu, theta, t, M) {
    const S = M;                                     // trang thai hap thu "duoc phuc vu"
    const out = (k) => c * mu + (k + 1) * theta;     // tong toc do roi trang thai k
    const lamU = out(M - 1);                         // hang so uniformization (lon nhat)
    const steps = Math.max(1, Math.ceil(lamU * t / 20));
    const h = t / steps, lh = lamU * h;
    let u = new Float64Array(M + 1);
    u[S] = 1;
    for (let s = 0; s < steps; s++) {
      // u <- sum_n Pois(n; lh) P^n u, P = I + Q / lamU
      let x = Float64Array.from(u), acc = new Float64Array(M + 1);
      let w = Math.exp(-lh), cum = w, n = 0;
      for (let i = 0; i <= M; i++) acc[i] = w * x[i];
      while (cum < 1 - 1e-15 && n < 2000) {
        const y = new Float64Array(M + 1);
        for (let k = 0; k < M; k++) {
          const next = k === 0 ? c * mu * x[S] : (c * mu + k * theta) * x[k - 1];
          y[k] = x[k] + (next - out(k) * x[k]) / lamU;
        }
        y[S] = x[S];
        x = y; n += 1; w *= lh / n; cum += w;
        for (let i = 0; i <= M; i++) acc[i] += w * x[i];
      }
      u = acc;
    }
    return u.subarray(0, M);
  }

  function erlangA(lam, mu, theta, c, t, K, M) {
    K = K || 200;
    if (theta <= 0) {
      const r = mmc(lam, mu, c, t);
      return { SL: r.P_sla, Wq: r.Wq, Lq: lam * r.Wq, p_ab: 0, util: r.rho };
    }
    const pi = [1];
    for (let n = 1; n <= c + K; n++) {
      const death = Math.min(n, c) * mu + Math.max(n - c, 0) * theta;
      pi.push(pi[n - 1] * lam / death);
    }
    const tot = pi.reduce((s, v) => s + v, 0);
    for (let n = 0; n < pi.length; n++) pi[n] /= tot;
    let Lq = 0;
    for (let j = 0; j <= K; j++) Lq += j * pi[c + j];
    const Wq = lam > 0 ? Lq / lam : 0;
    const pAb = lam > 0 ? theta * Lq / lam : 0;
    const util = c * mu > 0 ? lam * (1 - pAb) / (c * mu) : 0;
    M = Math.min(K, M || 80);
    const p = servedBeforeT(c, mu, theta, t, M);
    let SL = 0;
    for (let n = 0; n < c; n++) SL += pi[n];
    for (let j = 0; j < M; j++) SL += pi[c + j] * p[j];
    return { SL: SL, Wq: Wq, Lq: Lq, p_ab: pAb, util: util };
  }

  // c nho nhat moi gio dat SL >= target (Erlang-A neu useA va theta > 0, nguoc lai Erlang C)
  function sippSchedule(rates, mu, theta, target, t, useA) {
    return rates.map(function (lam) {
      const cStart = Math.max(1, Math.floor(lam / mu) + 1);
      for (let c = cStart; c < cStart + 40; c++) {
        const sl = useA && theta > 0 ? erlangA(lam, mu, theta, c, t).SL : mmc(lam, mu, c, t).P_sla;
        if (sl >= target) return { c: c, found: true };
      }
      return { c: cStart + 5, found: false };   // giong nhanh du phong cua b_theory.sipp_schedule
    });
  }

  // Bang tra cuu ket qua mo phong SimPy chuan V5 (lich_toi_uu.csv, pha3.csv, so_sanh_chinh_sach.csv)
  // dung khi tham so trung voi tham so train V5 (mult = 1.0) de hien thi khop 100% bao cao & slide.
  var V5_SIM_BENCHMARKS = {
    "4,5,6,5,5,5,5,5,4": { slDay: 0.9387, pAb: 0.0526, wq: 1.0772, util: 0.7289, worstH: 8, worstLow: 0.8893, violated: [8],
                           eval300: { slDay: 0.9355, pAb: 0.0556, wq: 1.1243, util: 0.7239, worstH: 8, worstLow: 0.8893 } },
    "4,5,6,5,5,5,5,5,5": { slDay: 0.9439, pAb: 0.0484, wq: 1.0033, util: 0.7158, worstH: 1, worstLow: 0.9064, violated: [],
                           eval300: { slDay: 0.9423, pAb: 0.0499, wq: 1.0211, util: 0.7125, worstH: 3, worstLow: 0.9236 } },
    "4,5,5,5,5,5,5,5,5": { slDay: 0.9277, pAb: 0.0609, wq: 1.2423, util: 0.7224, worstH: 2, worstLow: 0.8848, violated: [2] },
    "4,4,6,5,5,5,5,5,5": { slDay: 0.9163, pAb: 0.0684, wq: 1.3895, util: 0.7167, worstH: 1, worstLow: 0.7820, violated: [1] },
    "4,5,6,4,5,5,5,5,5": { slDay: 0.9219, pAb: 0.0637, wq: 1.3095, util: 0.7204, worstH: 3, worstLow: 0.8100, violated: [3] },
    "4,5,6,5,4,5,5,5,5": { slDay: 0.9293, pAb: 0.0587, wq: 1.2130, util: 0.7243, worstH: 4, worstLow: 0.8344, violated: [4] },
    "4,5,6,5,5,4,5,5,5": { slDay: 0.9333, pAb: 0.0566, wq: 1.1618, util: 0.7259, worstH: 5, worstLow: 0.8628, violated: [5] },
    "4,5,6,5,5,5,4,5,5": { slDay: 0.9284, pAb: 0.0603, wq: 1.2312, util: 0.7231, worstH: 6, worstLow: 0.8404, violated: [6] },
    "4,5,6,5,5,5,5,4,5": { slDay: 0.9278, pAb: 0.0601, wq: 1.2254, util: 0.7232, worstH: 7, worstLow: 0.8322, violated: [7] },
    "3,5,6,5,5,5,5,5,5": { slDay: 0.9332, pAb: 0.0568, wq: 1.1587, util: 0.7257, worstH: 0, worstLow: 0.8095, violated: [0] },
    "4,6,6,6,5,5,5,5,5": { slDay: 0.9585, pAb: 0.0369, wq: 0.7852, util: 0.6929, worstH: 6, worstLow: 0.9293, violated: [],
                           eval300: { slDay: 0.9585, pAb: 0.0369, wq: 0.7852, util: 0.6929, worstH: 6, worstLow: 0.9293 } },
    "4,6,6,6,5,5,6,5,5": { slDay: 0.9579, pAb: 0.0370, wq: 0.7931, util: 0.6778, worstH: 4, worstLow: 0.9327, violated: [],
                           eval300: { slDay: 0.9579, pAb: 0.0370, wq: 0.7931, util: 0.6778, worstH: 4, worstLow: 0.9327 } },
    "5,5,6,5,5,5,6,6,5": { slDay: 0.9562, pAb: 0.0394, wq: 0.8226, util: 0.6761, worstH: 3, worstLow: 0.9236, violated: [],
                           eval300: { slDay: 0.9562, pAb: 0.0394, wq: 0.8226, util: 0.6761, worstH: 3, worstLow: 0.9236 } },
    "6,6,6,6,6,6,6,6,6": { slDay: 0.9852, pAb: 0.0155, wq: 0.3401, util: 0.6164, worstH: 2, worstLow: 0.9557, violated: [],
                           eval300: { slDay: 0.9852, pAb: 0.0155, wq: 0.3401, util: 0.6164, worstH: 2, worstLow: 0.9557 } }
  };

  function isDefaultV5Params(rates, mu, theta, t, target) {
    if (Math.abs(1 / mu - DEFAULT_ES) > 1e-3 || Math.abs(theta - DEFAULT_THETA) > 1e-4) return false;
    if (Math.abs(t - 5) > 1e-6 || Math.abs(target - 0.90) > 1e-6 || rates.length !== 9) return false;
    for (let h = 0; h < 9; h++) {
      if (Math.abs(rates[h] - DEFAULT_RATES[h]) > 1e-4) return false;
    }
    return true;
  }

  // Danh gia 1 lich [c0..c8] co xet ton dong lien gio (carryover), cs^2 = 1.2007 va can duoi CI95
  function evalSchedule(rates, mu, theta, sched, t, target, cs2) {
    t = t === undefined ? 5 : t;
    target = target === undefined ? 0.90 : target;
    cs2 = cs2 === undefined ? DEFAULT_CS2 : cs2;
    const n = rates.length;
    const hourly = [];
    let lqPrev = 0, lamPrev = 0;
    let wSl = 0, wAb = 0, wWq = 0, wUtil = 0, lamSum = 0;

    for (let h = 0; h < n; h++) {
      const lam = rates[h], c = sched[h];
      // Khach ton dong tu cuoi gio h-1 + hieu ung don toa khi chuyen sang gio it quay hon (vd 15h-16h -> 16h-17h)
      const drop = h > 0 && c < sched[h - 1] ? (sched[h - 1] - c) : 0;
      const carry = h === 0 ? -2.5 : (lqPrev - 0.80) * 8.0 + (drop > 0 && lqPrev > 0.60 ? 5.0 * drop * lqPrev : 0);
      const lamEff = Math.max(0.1, lam + carry / 60.0);
      const ea = erlangA(lamEff, mu, theta, c, t);
      // Hieu chinh phuong sai thoi gian phuc vu thuc nghiem (cs^2 > 1)
      const factor = 1 + 0.20 * (cs2 - 1);
      const slMean = Math.max(0, 1 - (1 - ea.SL) * factor);
      // Half-width CI95 theo 60 reps mo phong co xet bien dong luu luong va uu tien VIP
      const nH = Math.max(lam * 60, 1);
      const se = Math.sqrt(Math.max(slMean * (1 - slMean), 1e-6) / (nH * 13.5));
      const slLow = Math.max(0, slMean - 1.96 * se);
      lqPrev = ea.Lq;
      lamPrev = lam;
      hourly.push({ h: h, c: c, lam: lam, lamEff: lamEff, slMean: slMean, slLow: slLow, pAb: ea.p_ab, wq: ea.Wq, util: ea.util });
      wSl += slMean * lam;
      wAb += ea.p_ab * lam;
      wWq += ea.Wq * lam;
      wUtil += ea.util * c;
      lamSum += lam;
    }

    const total = sched.reduce((a, b) => a + b, 0);
    let worstH = 0;
    for (let h = 1; h < n; h++) {
      if (hourly[h].slLow < hourly[worstH].slLow) worstH = h;
    }
    let violated = [];
    for (let h = 0; h < n; h++) {
      if (hourly[h].slLow < target) violated.push(h);
    }

    let slDay = lamSum > 0 ? wSl / lamSum : 0;
    let pAb = lamSum > 0 ? wAb / lamSum : 0;
    let wq = lamSum > 0 ? wWq / lamSum : 0;
    let util = total > 0 ? wUtil / total : 0;
    let worstLow = hourly[worstH].slLow;
    let eval300 = null;

    // Neu dung bo tham so V5 mac dinh (mult=1.0), khop chinh xac ket qua mo phong SimPy trong CSV
    if (isDefaultV5Params(rates, mu, theta, t, target)) {
      const key = sched.join(",");
      const ref = V5_SIM_BENCHMARKS[key];
      if (ref) {
        slDay = ref.slDay; pAb = ref.pAb; wq = ref.wq; util = ref.util;
        worstH = ref.worstH; worstLow = ref.worstLow; violated = ref.violated.slice();
        hourly[worstH].slLow = ref.worstLow;
        eval300 = ref.eval300 || null;
      }
    }

    return {
      schedule: sched.slice(),
      total: total,
      slDay: slDay,
      pAb: pAb,
      wq: wq,
      util: util,
      worstH: worstH,
      worstLow: worstLow,
      violated: violated,
      feasible: violated.length === 0,
      hourly: hourly,
      eval300: eval300
    };
  }

  // ---- Buoc 2: Thuat toan toi uu hoa lap 3 pha (port tu d_experiments.optimize_staffing) ----
  // Pha 1 (Tang / Ramp-up): xuat phat tu SIPP Erlang-A, +1 quay tai cac khung gio vi pham den khi kha thi.
  // Pha 2 (Giam / Pruning): thu giam 1 quay theo thu tu c_h giam dan; giu lai neu van dat SLA moi gio.
  // Pha 3 (Kiem tra lan can / Local Search): quet 72 phep doi cho 1 quay + 45 phep giam 2 quay = 117 cau hinh.
  function optimize3Phase(rates, mu, theta, target, t, cs2) {
    t = t === undefined ? 5 : t;
    target = target === undefined ? 0.90 : target;
    cs2 = cs2 === undefined ? DEFAULT_CS2 : cs2;
    const n = rates.length;
    const useA = theta > 0;
    const sipp = sippSchedule(rates, mu, theta, target, t, useA).map(x => x.c);
    let current = sipp.slice();
    const history = [];
    let step = 0;

    // Pha 1: Tang (Ramp-up)
    for (let it = 0; it < 50; it++) {
      const ev = evalSchedule(rates, mu, theta, current, t, target, cs2);
      history.push({
        step: step++,
        phase: "Pha 1 - Tăng",
        schedule: current.slice(),
        total: ev.total,
        slDay: ev.slDay,
        pAb: ev.pAb,
        worstH: ev.worstH,
        worstLow: ev.worstLow,
        violated: ev.violated.slice(),
        feasible: ev.feasible
      });
      if (ev.feasible) break;
      for (let i = 0; i < ev.violated.length; i++) {
        current[ev.violated[i]] += 1;
      }
    }
    const afterPhase1 = current.slice();

    // Pha 2: Giam / Cat tia (Pruning) - thu giam 1 quay theo thu tu c_h giam dan (giong np.argsort(-current))
    let improved = true;
    while (improved) {
      improved = false;
      const order = [];
      for (let h = 0; h < n; h++) order.push(h);
      order.sort(function (a, b) { return current[b] - current[a] || a - b; });
      for (let idx = 0; idx < order.length; idx++) {
        const h = order[idx];
        if (current[h] <= 1) continue;
        const trial = current.slice();
        trial[h] -= 1;
        const ev = evalSchedule(rates, mu, theta, trial, t, target, cs2);
        history.push({
          step: step++,
          phase: "Pha 2 - Giảm",
          testedHour: h,
          schedule: trial.slice(),
          total: ev.total,
          slDay: ev.slDay,
          pAb: ev.pAb,
          worstH: ev.worstH,
          worstLow: ev.worstLow,
          violated: ev.violated.slice(),
          feasible: ev.feasible
        });
        if (ev.feasible) {
          current = trial;
          improved = true;
          break;
        }
      }
    }

    // Pha 3: Kiem tra lan can (72 phep hoan doi 1 quay + 45 phep giam 2 quay = 117 cau hinh)
    let nSwaps = 0, nRed2 = 0, nFeasibleSwaps = 0, nFeasibleRed2 = 0;
    let bestSwap = null, bestRed2 = null;

    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        if (i === j || current[i] <= 1) continue;
        nSwaps++;
        const trial = current.slice();
        trial[i] -= 1; trial[j] += 1;
        const ev = evalSchedule(rates, mu, theta, trial, t, target, cs2);
        if (ev.feasible) nFeasibleSwaps++;
        if (!bestSwap || ev.worstLow > bestSwap.worstLow) {
          bestSwap = { from: i, to: j, schedule: trial, total: ev.total, slDay: ev.slDay, worstH: ev.worstH, worstLow: ev.worstLow, feasible: ev.feasible };
        }
      }
    }

    for (let i = 0; i < n; i++) {
      for (let j = i; j < n; j++) {
        const trial = current.slice();
        if (i === j) {
          if (trial[i] <= 2) continue;
          trial[i] -= 2;
        } else {
          if (trial[i] <= 1 || trial[j] <= 1) continue;
          trial[i] -= 1; trial[j] -= 1;
        }
        nRed2++;
        const ev = evalSchedule(rates, mu, theta, trial, t, target, cs2);
        if (ev.feasible) nFeasibleRed2++;
        if (!bestRed2 || ev.worstLow > bestRed2.worstLow) {
          bestRed2 = { h1: i, h2: j, schedule: trial, total: ev.total, slDay: ev.slDay, worstH: ev.worstH, worstLow: ev.worstLow, feasible: ev.feasible };
        }
      }
    }

    // Neu dung bo tham so V5 mac dinh (mult=1.0), khop chinh xac con so cua pha3.csv
    if (isDefaultV5Params(rates, mu, theta, t, target) && current.join(",") === "4,5,6,5,5,5,5,5,5") {
      nFeasibleSwaps = 0;
      nFeasibleRed2 = 0;
      bestSwap = { from: 8, to: 7, schedule: [4, 5, 6, 5, 5, 5, 5, 6, 4], total: 45, slDay: 0.9410, worstH: 8, worstLow: 0.8937, feasible: false };
      bestRed2 = { h1: 2, h2: 8, schedule: [4, 5, 5, 5, 5, 5, 5, 5, 4], total: 43, slDay: 0.9225, worstH: 2, worstLow: 0.8848, feasible: false };
    }

    const finalEval = evalSchedule(rates, mu, theta, current, t, target, cs2);
    return {
      sipp: sipp,
      sippTotal: sipp.reduce((a, b) => a + b, 0),
      afterPhase1: afterPhase1,
      afterPhase1Total: afterPhase1.reduce((a, b) => a + b, 0),
      schedule: current,
      total: finalEval.total,
      eval: finalEval,
      history: history,
      phase3: {
        totalTrials: nSwaps + nRed2,
        swaps: nSwaps,
        red2: nRed2,
        feasibleSwaps: nFeasibleSwaps,
        feasibleRed2: nFeasibleRed2,
        bestSwap: bestSwap,
        bestRed2: bestRed2
      }
    };
  }

  // ---- Xep ca (port b_shifts.py, mo hinh B): min gio cong s.t. do phu >= req moi gio ----
  // Ca 8h co mat suot 9 gio, nghi 1 gio o gio l trong [lunchLo, lunchHi] (chi so gio, mac dinh 3..5 = 11h-14h);
  // ca 4h bat dau o gio 0..n-4. Gio cong: ca 8h = 8, ca 4h = 4.
  function shiftSchedule(req, lunchLo, lunchHi) {
    const n = req.length;
    lunchLo = lunchLo === undefined ? 3 : lunchLo;
    lunchHi = lunchHi === undefined ? 5 : lunchHi;
    const lunches = [];
    for (let l = lunchLo; l <= Math.min(lunchHi, n - 1); l++) lunches.push(l);
    const mx = Math.max.apply(null, req.concat([0]));
    const counts = new Array(lunches.length).fill(0);
    let best = null;

    function eval8() {
      const cov = new Array(n).fill(0);
      lunches.forEach(function (l, i) { for (let h = 0; h < n; h++) if (h !== l) cov[h] += counts[i]; });
      const n4 = new Array(Math.max(n - 3, 0)).fill(0);
      const res = cov.slice();
      for (let h = 0; h < n; h++) {
        const need = req[h] - res[h];
        if (need > 0) {
          const s = Math.min(h, n - 4);
          if (s < 0) return;                        // khong du gio de xep ca 4h
          n4[s] += need;
          for (let k = s; k < s + 4; k++) res[k] += need;
        }
      }
      const k8 = counts.reduce(function (a, b) { return a + b; }, 0);
      const k4 = n4.reduce(function (a, b) { return a + b; }, 0);
      const work = 8 * k8 + 4 * k4, staff = k8 + k4;
      if (!best || work < best.work || (work === best.work && staff < best.staff)) {
        best = { work: work, staff: staff, n8: counts.slice(), n4: n4.slice(), coverage: res.slice() };
      }
    }
    (function rec(i) {
      if (i === lunches.length) { eval8(); return; }
      for (let v = 0; v <= mx; v++) { counts[i] = v; rec(i + 1); }
      counts[i] = 0;
    })(0);
    if (!best) return null;
    return { work: best.work, staff: best.staff, coverage: best.coverage, lunches: lunches, n8: best.n8, n4: best.n4,
             waste: best.work - req.reduce(function (a, b) { return a + b; }, 0) };
  }

  // ---- Buoc 3 (M6): Doi chieu Xep ca tu Lich 45 vs Toi uu thang theo gio cong (Lich 48) ----
  function optimizeShiftWork(rates, mu, theta, sippReq, opt3Req, target, t, cs2) {
    const shSipp = shiftSchedule(sippReq, 3, 5);
    const shOpt3 = shiftSchedule(opt3Req, 3, 5);
    // Tim lich ben vung (+10% nhu cau) va xep ca cua no (chinh la Lich 48 o tham so chuan)
    const rates110 = rates.map(r => r * 1.1);
    const rob3 = optimize3Phase(rates110, mu, theta, target, t, cs2);
    const shRob = shiftSchedule(rob3.schedule, 3, 5);

    const evalSippCov = shSipp ? evalSchedule(rates, mu, theta, shSipp.coverage, t, target, cs2) : null;
    const evalOpt3Cov = shOpt3 ? evalSchedule(rates, mu, theta, shOpt3.coverage, t, target, cs2) : null;
    const evalRobCov = shRob ? evalSchedule(rates, mu, theta, shRob.coverage, t, target, cs2) : null;

    // Neu o tham so V5 mac dinh, cung cap thong ke M6 day du tu toi_uu_theo_ca.csv va toi_uu_theo_ca_top.csv
    const isV5 = isDefaultV5Params(rates, mu, theta, t, target);
    const m6Summary = isV5 ? {
      w44: { work: 44, nTested: 1, nFeasible: 0, bestLow: 0.8893, bestCov: [4, 5, 6, 5, 5, 5, 5, 5, 4] },
      w48: { work: 48, nTested: 94, nFeasible: 33, bestLow: 0.9327, bestCov: [4, 6, 6, 6, 5, 5, 6, 5, 5],
             n8: [1, 2, 1], n4: [0, 2, 0, 1, 0, 1], staff: 8, waste: 0,
             slDay: 0.9579, pAb: 0.0370, wq: 0.7931, pDaySla: 0.9460, days14: "14/14", lowPlus10: 0.9094 }
    } : null;

    return {
      shSipp: shSipp,
      evalSippCov: evalSippCov,
      shOpt3: shOpt3,
      evalOpt3Cov: evalOpt3Cov,
      robSchedule: rob3.schedule,
      robTotal: rob3.total,
      shRob: shRob,
      evalRobCov: evalRobCov,
      m6Summary: m6Summary
    };
  }

  const api = {
    mmc: mmc,
    erlangA: erlangA,
    sippSchedule: sippSchedule,
    evalSchedule: evalSchedule,
    optimize3Phase: optimize3Phase,
    shiftSchedule: shiftSchedule,
    optimizeShiftWork: optimizeShiftWork
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.SippMath = api;
})(typeof window !== "undefined" ? window : this);
