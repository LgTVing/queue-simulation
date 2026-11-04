"use strict";

const $ = (id) => document.getElementById(id);
const percent = (value, digits = 1) => `${(value * 100).toLocaleString("vi-VN", { minimumFractionDigits: digits, maximumFractionDigits: digits })}%`;
const number = (value, digits = 2) => value.toLocaleString("vi-VN", { minimumFractionDigits: digits, maximumFractionDigits: digits });
let config;
let latestResult;

function currentSchedule() {
  return [...document.querySelectorAll(".schedule-input")].map((input) => Number(input.value));
}

function updateEstimates() {
  $("counter-total").textContent = `${currentSchedule().reduce((sum, c) => sum + c, 0)} quầy-giờ`;
  $("demand-value").value = `${$("demand").value}%`;
  const count = Math.round(config.expected_arrivals * Number($("demand").value) / 100);
  $("expected-arrivals").replaceChildren(document.createTextNode("Khoảng "));
  const strong = document.createElement("strong");
  strong.textContent = `${count.toLocaleString("vi-VN")} khách / ngày`;
  $("expected-arrivals").append(strong, document.createTextNode(" theo nhu cầu đã chọn."));
}

function markDirty() {
  updateEstimates();
  if (latestResult) {
    $("status").textContent = "Thông số đã thay đổi. Bấm Chạy mô phỏng để cập nhật kết quả bên dưới.";
    $("status").classList.add("dirty");
    $("result-tag").textContent = "Kết quả trước";
  }
}

function applyPreset() {
  const preset = config.presets.find((item) => item.id === $("preset").value);
  if (preset) {
    document.querySelectorAll(".schedule-input").forEach((input, i) => { input.value = preset.schedule[i]; });
    $("preset-description").textContent = preset.description;
  } else {
    $("preset-description").textContent = "Lịch của bạn: chỉnh số quầy ở từng khung giờ bên dưới.";
  }
  markDirty();
}

function setBusy(busy) {
  document.querySelector(".results").setAttribute("aria-busy", String(busy));
  document.querySelectorAll("#scenario-form input, #scenario-form select, #run, #reset").forEach((el) => { el.disabled = busy; });
  $("run-label").textContent = busy ? "Đang mô phỏng…" : "Chạy mô phỏng";
}

function drawChart(data) {
  const width = 800, height = 245;
  const left = 39, right = 13, top = 21, bottom = 35;
  const plotHeight = height - top - bottom;
  const y = (value) => top + (1 - Math.max(0, Math.min(1, value))) * plotHeight;
  const step = (width - left - right) / 9;
  const baseline = data.baseline;
  let svg = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Biểu đồ mức phục vụ theo 9 khung giờ, so với mục tiêu SLA 90%"><title>Mức phục vụ theo giờ và khoảng tin cậy 95%</title>`;
  for (const tick of [0, .25, .5, .75, 1]) {
    svg += `<line x1="${left}" y1="${y(tick)}" x2="${width-right}" y2="${y(tick)}" stroke="#e9ede3"/><text x="${left-9}" y="${y(tick)+3}" text-anchor="end" fill="#96a08f" font-size="9">${tick*100}%</text>`;
  }
  data.hourly.forEach((hour, i) => {
    const center = left + step * (i + .5);
    const barWidth = baseline ? 21 : 30;
    const x = center - (baseline ? 24 : 15);
    const color = hour.sl_ci95_low >= config.target_sla ? "#557653" : "#d99c75";
    svg += `<rect x="${x}" y="${y(hour.sl_mean)}" width="${barWidth}" height="${y(0)-y(hour.sl_mean)}" rx="3" fill="${color}"><title>${config.hours[i]}: ${percent(hour.sl_mean)}, CI95 ${percent(hour.sl_ci95_low)}–${percent(hour.sl_ci95_high)}</title></rect>`;
    if (baseline) {
      const sl = baseline.hourly[i].sl_mean;
      svg += `<rect x="${center+3}" y="${y(sl)}" width="21" height="${y(0)-y(sl)}" rx="3" fill="#d6e0c6"><title>6 quầy: ${percent(sl)}</title></rect>`;
    }
    const cx = x + barWidth / 2;
    svg += `<path d="M${cx} ${y(hour.sl_ci95_low)} V${y(hour.sl_ci95_high)} M${cx-4} ${y(hour.sl_ci95_low)} H${cx+4} M${cx-4} ${y(hour.sl_ci95_high)} H${cx+4}" stroke="#223f30" stroke-width="1.2" fill="none"/>`;
    svg += `<text x="${center}" y="${height-14}" text-anchor="middle" fill="#7c8a74" font-size="10">${String(i+8).padStart(2,"0")}–${String(i+9).padStart(2,"0")}</text>`;
  });
  svg += `<line x1="${left}" y1="${y(.9)}" x2="${width-right}" y2="${y(.9)}" stroke="#b78b4e" stroke-width="1" stroke-dasharray="4 4"/><text x="${width-right}" y="12" text-anchor="end" fill="#a38458" font-size="9">SLA ≥ 90%</text></svg>`;
  $("chart").innerHTML = svg;
  $("baseline-legend").hidden = !baseline;
}

function render(data) {
  latestResult = data;
  const s = data.summary, b = data.baseline;
  $("sl-value").textContent = percent(s.sl);
  $("sl-detail").textContent = `CI95: ${percent(s.sl_ci[0])} – ${percent(s.sl_ci[1])}`;
  $("wait-value").textContent = number(s.wait);
  $("wait-detail").textContent = `Khoảng ${number(s.wait * 60, 1)} giây · mọi khách đến`;
  $("abandon-value").textContent = percent(s.abandonment);
  $("abandon-detail").textContent = `CI95: ± ${number(s.abandonment_ci_half * 100, 2)} điểm %`;
  $("hours-value").textContent = `${s.counter_hours} quầy-giờ`;
  $("util-value").textContent = percent(s.utilization);
  $("vip-value").textContent = s.vip_sl === null ? "Không có khách VIP" : percent(s.vip_sl);
  $("sl-delta").textContent = b ? `${s.sl >= b.sl ? "+" : "−"}${number(Math.abs(s.sl-b.sl)*100, 2)} điểm % so với 6 quầy` : "Mục tiêu: ít nhất 90% khách";
  $("wait-delta").textContent = b ? `${s.wait <= b.wait ? "Ít hơn" : "Nhiều hơn"} ${number(Math.abs(s.wait-b.wait)*60, 1)} giây so với 6 quầy` : "";
  $("abandon-delta").textContent = b ? `${s.abandonment <= b.abandonment ? "Ít hơn" : "Nhiều hơn"} ${number(Math.abs(s.abandonment-b.abandonment)*100, 2)} điểm % so với 6 quầy` : "";
  $("verdict").className = `verdict ${s.feasible ? "" : "warning"}`;
  $("verdict-icon").textContent = s.feasible ? "✓" : "!";
  $("verdict-title").textContent = s.feasible ? "Lịch này đạt SLA ở cả 9 khung giờ." : `${s.violated_hours.length} khung giờ chưa đạt SLA theo cận dưới CI95.`;
  $("verdict-copy").textContent = `Giờ có cận dưới thấp nhất: ${config.hours[s.worst_hour]}, đạt ${percent(s.worst_hour_low)}. ${s.feasible ? "Mọi giờ đều có cận dưới CI95 ≥ 90%." : "Có thể thử tăng số quầy ở những giờ chưa đạt."}`;
  $("result-tag").textContent = `${data.scenario.reps} ngày mô phỏng`;
  $("status").classList.remove("dirty");
  const preset = config.presets.find((item) => item.schedule.every((c, i) => c === data.scenario.schedule[i]));
  $("status").textContent = `${preset ? preset.label : "Lịch tùy chỉnh"} · ${data.scenario.demand_percent}% lượng khách · khoảng ${data.expected_arrivals} khách/ngày · ${number(data.elapsed_seconds, 1)} giây`;
  $("run-note").textContent = `Seed ${data.scenario.seed} · ${data.scenario.day_variability ? "Có" : "Không"} dao động quy mô ngày`;
  $("hourly-body").replaceChildren();
  for (const hour of data.hourly) {
    const tr = document.createElement("tr");
    const values = [config.hours[hour.hour], hour.c, `${number(hour.wq_mean)} phút`, percent(hour.p_ab_mean), percent(hour.sl_mean)];
    for (const value of values) {
      const td = document.createElement("td");
      td.textContent = value;
      tr.append(td);
    }
    const td = document.createElement("td");
    const pill = document.createElement("span");
    const ok = hour.sl_ci95_low >= config.target_sla;
    pill.className = `pill${ok ? "" : " fail"}`;
    pill.textContent = ok ? "Đạt" : "Chưa đạt";
    pill.title = `Cận dưới CI95: ${percent(hour.sl_ci95_low)}`;
    td.append(pill);
    tr.append(td);
    $("hourly-body").append(tr);
  }
  drawChart(data);
  $("download").disabled = false;
}

async function runSimulation(event) {
  if (event) event.preventDefault();
  if (!$("scenario-form").reportValidity()) return;
  const payload = { schedule: currentSchedule(), demand_percent: Number($("demand").value),
    reps: Number($("reps").value), seed: Number($("seed").value),
    day_variability: $("variability").checked, compare_baseline: $("compare").checked };
  setBusy(true);
  $("error").hidden = true;
  $("status").classList.remove("dirty");
  $("status").textContent = `Đang chạy ${payload.reps} ngày mô phỏng${payload.compare_baseline ? " và phương án 6 quầy" : ""}…`;
  $("result-tag").textContent = "Đang chạy";
  try {
    const response = await fetch("/api/simulate", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Chưa chạy được mô phỏng.");
    render(data);
  } catch (error) {
    $("error").textContent = error instanceof TypeError ? "Không kết nối được máy chủ. Kiểm tra terminal đang chạy demo.py rồi thử lại." : error.message;
    $("error").hidden = false;
    $("status").textContent = latestResult ? "Chưa cập nhật được. Các số liệu bên dưới thuộc lần chạy trước." : "Chưa có kết quả. Vui lòng thử lại.";
    $("result-tag").textContent = latestResult ? "Kết quả trước" : "Chưa chạy được";
  } finally {
    setBusy(false);
  }
}

function downloadCsv() {
  if (!latestResult) return;
  const d = latestResult;
  const rows = [["khung_gio", "so_quay", "cho_tb_phut", "ty_le_bo_ve", "muc_phuc_vu", "sl_ci95_low", "sl_ci95_high", "dat_sla", "luong_khach_pct", "so_ngay", "seed", "dao_dong_ngay"],
    ...d.hourly.map((h) => [config.hours[h.hour], h.c, h.wq_mean, h.p_ab_mean, h.sl_mean, h.sl_ci95_low, h.sl_ci95_high, h.sl_ci95_low >= config.target_sla, d.scenario.demand_percent, d.scenario.reps, d.scenario.seed, d.scenario.day_variability])];
  const csv = "\uFEFF" + rows.map((row) => row.join(",")).join("\r\n");
  const url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8" }));
  const a = document.createElement("a");
  a.href = url;
  a.download = `mo-phong-${d.scenario.demand_percent}pct-seed-${d.scenario.seed}.csv`;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

async function init() {
  setBusy(true);
  try {
    const response = await fetch("/api/config");
    if (!response.ok) throw new Error("Không tải được cấu hình V5. Hãy tải lại trang.");
    config = await response.json();
    for (const preset of [...config.presets, { id: "custom", label: "Tùy chỉnh theo giờ" }]) {
      const option = document.createElement("option");
      option.value = preset.id;
      option.textContent = preset.label;
      $("preset").append(option);
    }
    config.hours.forEach((hour, i) => {
      const label = document.createElement("label");
      label.className = "schedule-cell";
      const text = document.createElement("span");
      text.textContent = hour;
      const input = document.createElement("input");
      input.type = "number";
      input.className = "schedule-input";
      input.min = "1"; input.max = "12"; input.step = "1"; input.required = true;
      input.setAttribute("aria-label", `Số quầy ${hour}`);
      input.addEventListener("input", () => { $("preset").value = "custom"; $("preset-description").textContent = "Lịch của bạn: chỉnh số quầy ở từng khung giờ bên dưới."; markDirty(); });
      label.append(text, input);
      $("schedule-grid").append(label);
    });
    $("preset").value = config.default_preset;
    applyPreset();
    $("preset").addEventListener("change", applyPreset);
    for (const id of ["demand", "reps", "seed", "variability", "compare"]) $(id).addEventListener("input", markDirty);
    $("scenario-form").addEventListener("submit", runSimulation);
    $("download").addEventListener("click", downloadCsv);
    $("reset").addEventListener("click", () => {
      $("scenario-form").reset();
      $("preset").value = config.default_preset;
      $("error").hidden = true;
      applyPreset();
    });
    setBusy(false);
    await runSimulation();
  } catch (error) {
    $("error").textContent = error.message;
    $("error").hidden = false;
    $("status").textContent = "Chưa tải được dữ liệu. Vui lòng tải lại trang.";
    $("result-tag").textContent = "Lỗi kết nối";
  }
}

init();
