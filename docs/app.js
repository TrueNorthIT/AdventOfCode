// Display only: everything here is computed by build_readme.py into data/<year>.json.
(async () => {
  const $ = (id) => document.getElementById(id);
  const el = (tag, cls, text) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text; // names come from AoC: never innerHTML
    return e;
  };
  const status = $("status");

  let years = [];
  try {
    const r = await fetch("data/years.json", { cache: "no-cache" });
    if (r.ok) years = await r.json();
  } catch { /* fall through to the empty state */ }
  if (!years.length) {
    status.textContent = "No data yet. The leaderboard appears here after the first star of December.";
    return;
  }

  const wanted = Number(new URLSearchParams(location.search).get("year"));
  const year = years.includes(wanted) ? wanted : years[years.length - 1];
  for (const y of years) {
    const a = el("a", y === year ? "current" : "", `[${y}]`);
    a.href = `?year=${y}`;
    $("years").append(a);
  }
  $("year-title").textContent = String(year);
  document.title = `TrueNorth Advent of Code ${year}`;

  let data;
  try {
    const r = await fetch(`data/${year}.json`, { cache: "no-cache" });
    if (!r.ok) throw new Error(r.status);
    data = await r.json();
  } catch {
    status.textContent = `Couldn't load the ${year} leaderboard.`;
    return;
  }
  status.hidden = true;

  const tn = data.tn;
  const name = (m) => m.name || `(anonymous user #${m.id})`;
  const rows = tn.order.map((id) => data.members[id]);
  const numDays = data.num_days || 25;

  // --- Leaderboard ---
  const nameWidth = Math.max(4, ...rows.map((m) => name(m).length)) + 3;
  const span = (cls, text, width) => {
    const s = el("span", cls, text);
    if (width) s.style.width = `${width}ch`;
    return s;
  };
  const days = (label) => {
    const d = el("span", "days");
    for (let day = 1; day <= numDays; day++) d.append(span("day", label(day)));
    return d;
  };
  const head = (n, sc, st, digit) => {
    const r = el("div", "row head");
    r.append(span("rank", ""), span("name", n, nameWidth), span("num", sc), span("num", st), days(digit));
    return r;
  };
  const table = $("table");
  table.append(
    head("", "", "", (d) => (d >= 10 ? String(Math.floor(d / 10)) : " ")),
    head("Name", "Score", "Stars", (d) => String(d % 10)),
  );
  rows.forEach((m, i) => {
    const r = el("div", "row");
    const branch = tn.branches[m.id];
    const d = el("span", "days");
    for (let day = 1; day <= numDays; day++) {
      const parts = m.completion_day_level[day] || {};
      const n = parts[2] ? 2 : parts[1] ? 1 : 0;
      const c = el(n && branch ? "a" : "span", `day ${["none", "silver", "gold"][n]}`, ["·", "☆", "★"][n]);
      c.title = `Day ${day}: ${["no stars", "part one", "both parts"][n]}`;
      if (c.tagName === "A") c.href = `https://github.com/TrueNorthIT/AdventOfCode/tree/${branch}/${year}/day${String(day).padStart(2, "0")}`;
      d.append(c);
    }
    r.append(span("rank", `${i + 1})`), span("name", name(m), nameWidth), span("num", String(m.local_score)), span("num", String(m.stars)), d);
    table.append(r);
  });
  $("board").hidden = false;

  // --- Achievements ---
  const item = (e, i) => {
    const li = el("li");
    li.append(el("span", "place", `${i + 1}.`), `${e.name} (${e.value})`);
    if (e.langs) li.append(el("span", "langs", e.langs.join(", ")));
    return li;
  };
  for (const a of tn.achievements) {
    const box = el("div");
    box.append(el("h3", "", a.title), el("p", "dim", a.description));
    const top = el("ol");
    a.entries.slice(0, 3).forEach((e, i) => top.append(item(e, i)));
    box.append(a.entries.length ? top : el("p", "none", "Nobody yet."));
    if (a.entries.length > 3) {
      const more = el("details");
      const rest = el("ol");
      a.entries.slice(3).forEach((e, i) => rest.append(item(e, i + 3)));
      more.append(el("summary", "", `[+${a.entries.length - 3} more]`), rest);
      box.append(more);
    }
    $("ach").append(box);
  }
  $("achievements").hidden = false;

  // --- Race chart ---
  if (!window.Chart) return; // CDN blocked: the rest of the page still works
  const series = rows.map((m) => tn.series[m.id]);
  const start = Math.min(...series.map((s) => s[0][0])) * 1000;
  // Race runs through December only; later solves are off the right edge
  const end = Math.min(Math.max(...series.map((s) => s[s.length - 1][0])) * 1000, Date.UTC(year + 1, 0, 1));
  const css = getComputedStyle(document.documentElement);
  Chart.defaults.font.family = getComputedStyle(document.body).fontFamily;
  Chart.defaults.color = css.getPropertyValue("--dim").trim();
  const grid = { color: "#1a2142" };
  $("race").hidden = false; // must be visible before Chart.js measures it
  new Chart($("chart"), {
    type: "line",
    data: {
      datasets: rows.map((m, i) => {
        const pts = series[i].map(([t, y]) => ({ x: t * 1000, y }));
        if (pts[pts.length - 1].x < end) pts.push({ x: end, y: pts[pts.length - 1].y }); // carry each line to the end
        const colour = `hsl(${Math.round((i * 360) / rows.length)}, 75%, 62%)`;
        return { label: name(m), data: pts, stepped: "after", borderColor: colour, backgroundColor: colour, borderWidth: 1.5, pointRadius: 0 };
      }),
    },
    options: {
      maintainAspectRatio: false,
      animation: false,
      interaction: { mode: "nearest", intersect: false },
      scales: {
        x: { type: "linear", min: start, max: end, grid, ticks: { stepSize: 86400000, callback: (v) => `Dec ${new Date(v).getUTCDate()}` } },
        y: { beginAtZero: true, grid },
      },
      plugins: {
        legend: { position: "bottom", labels: { boxWidth: 10, color: css.getPropertyValue("--text").trim() } },
        tooltip: { callbacks: { title: (items) => `${new Date(items[0].parsed.x).toISOString().slice(5, 16).replace("T", " ")} UTC` } },
      },
    },
  });
})();
