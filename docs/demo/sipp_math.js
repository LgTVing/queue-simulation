/*
 * docs/demo/sipp_math.js: Erlang C, Erlang-A va lich SIPP cho trang demo D5.
 * Port tu b_theory.py (mmc, erlang_a, sipp_schedule), cung tham so cat K = 200, M = 80.
 * SL(t) cua Erlang-A: P(vao phuc vu truoc t) tu trang thai j khach dung truoc, tinh bang
 * uniformization tren chuoi hap thu (b_theory dung expm); hai cach trung nhau den sai so may.
 * Dung duoc trong trinh duyet (window.SippMath) va Node (module.exports) cho tests/test_d5_demo.py.
 */
(function (root) {
  "use strict";

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
      return { SL: r.P_sla, Wq: r.Wq, p_ab: 0, util: r.rho };
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
    return { SL: SL, Wq: Wq, p_ab: pAb, util: util };
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

  const api = { mmc: mmc, erlangA: erlangA, sippSchedule: sippSchedule };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.SippMath = api;
})(typeof window !== "undefined" ? window : this);
