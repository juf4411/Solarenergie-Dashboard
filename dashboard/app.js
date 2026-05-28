const watt = new Intl.NumberFormat("de-DE", { maximumFractionDigits: 0 });
const kwh = new Intl.NumberFormat("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

function formatTime(value) {
  return new Date(value).toLocaleTimeString("de-DE", { hour: "2-digit", minute: "2-digit" });
}

function setText(id, value) {
  document.getElementById(id).textContent = value;
}

function drawLineChart(canvas, readings, key, color, unit) {
  const ctx = canvas.getContext("2d");
  const width = canvas.width;
  const height = canvas.height;
  const padding = { top: 22, right: 18, bottom: 42, left: 58 };
  const values = readings.map((reading) => Number(reading[key]));
  const maxValue = Math.max(...values, 1);
  const plotWidth = width - padding.left - padding.right;
  const plotHeight = height - padding.top - padding.bottom;

  ctx.clearRect(0, 0, width, height);
  ctx.strokeStyle = "#dbe5e1";
  ctx.lineWidth = 1;
  ctx.font = "13px Segoe UI, Arial";
  ctx.fillStyle = "#6c7b80";

  for (let i = 0; i <= 4; i += 1) {
    const y = padding.top + (plotHeight / 4) * i;
    ctx.beginPath();
    ctx.moveTo(padding.left, y);
    ctx.lineTo(width - padding.right, y);
    ctx.stroke();
    const label = Math.round(maxValue - (maxValue / 4) * i);
    ctx.fillText(`${label} ${unit}`, 8, y + 4);
  }

  const points = readings.map((reading, index) => {
    const x = padding.left + (plotWidth / Math.max(readings.length - 1, 1)) * index;
    const y = padding.top + plotHeight - (Number(reading[key]) / maxValue) * plotHeight;
    return { x, y, reading };
  });

  ctx.strokeStyle = color;
  ctx.lineWidth = 3;
  ctx.beginPath();
  points.forEach((point, index) => {
    if (index === 0) {
      ctx.moveTo(point.x, point.y);
    } else {
      ctx.lineTo(point.x, point.y);
    }
  });
  ctx.stroke();

  ctx.fillStyle = color;
  points.forEach((point) => {
    ctx.beginPath();
    ctx.arc(point.x, point.y, 4, 0, Math.PI * 2);
    ctx.fill();
  });

  ctx.fillStyle = "#6c7b80";
  points.forEach((point, index) => {
    if (index % Math.ceil(points.length / 5) === 0 || index === points.length - 1) {
      ctx.fillText(formatTime(point.reading.timestamp), point.x - 18, height - 14);
    }
  });
}

function fillTable(readings) {
  const rows = document.getElementById("readingRows");
  rows.innerHTML = "";
  readings.slice(-6).reverse().forEach((reading) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${formatTime(reading.timestamp)}</td>
      <td>${watt.format(reading.power_w)} W</td>
      <td>${kwh.format(reading.energy_today_kwh)} kWh</td>
    `;
    rows.appendChild(row);
  });
}

async function loadDashboard() {
  const [summaryResponse, readingsResponse] = await Promise.all([
    fetch("/summary"),
    fetch("/readings?limit=24"),
  ]);
  const summary = await summaryResponse.json();
  const readingsNewestFirst = await readingsResponse.json();
  const readings = [...readingsNewestFirst].reverse();
  const latest = summary.latest || readings[readings.length - 1] || {};

  setText("plantName", latest.plant_id || "keine Anlage");
  setText("currentPower", `${watt.format(latest.power_w || 0)} W`);
  setText("averagePower", `${watt.format(summary.average_power_w || 0)} W`);
  setText("dailyEnergy", `${kwh.format(summary.energy_today_kwh || 0)} kWh`);
  setText("temperature", `${Number(latest.temperature_c || 0).toFixed(1)} C`);
  setText("sourceName", latest.data_source || "unbekannt");
  setText("readingCount", `${summary.reading_count || readings.length} Werte`);
  setText("dataStatus", summary.latest_is_test_data ? "TESTDATEN" : "ECHTDATEN");

  const loadPercent = Math.min(Math.round(((latest.power_w || 0) / 5500) * 100), 100);
  setText("donutValue", `${loadPercent}%`);
  document.getElementById("powerDonut").style.background =
    `conic-gradient(#246bfe ${loadPercent * 3.6}deg, #e7eef1 0deg)`;

  if (readings.length > 0) {
    drawLineChart(document.getElementById("powerChart"), readings, "power_w", "#246bfe", "W");
    drawLineChart(document.getElementById("energyChart"), readings, "energy_today_kwh", "#21a675", "kWh");
    fillTable(readings);
  }
}

loadDashboard();
setInterval(loadDashboard, 30000);
