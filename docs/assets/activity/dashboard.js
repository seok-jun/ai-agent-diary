/* Numeric public data only. No third-party scripts, analytics, or API credentials. */
(function () {
  "use strict";
  const format = new Intl.NumberFormat("ko-KR");
  const count = value => value == null ? "—" : format.format(value);
  const rateFormat = new Intl.NumberFormat("ko-KR", {maximumFractionDigits: 3});
  const rate = value => value == null ? "—" : value > 0 && value < 0.001 ? "0.001 미만" : rateFormat.format(value);
  const sum = (rows, key) => rows.reduce((total, row) => total + row[key], 0);
  function bounds(mode, value) {
    if (mode === "all") return ["0000-01-01", "9999-12-31"];
    if (mode === "day") return [value, value];
    const [year, month] = value.split("-").map(Number);
    const last = new Date(Date.UTC(year, month, 0)).getUTCDate();
    return [value + "-01", value + "-" + String(last).padStart(2, "0")];
  }
  function select(data, mode, value) {
    const [start, end] = bounds(mode, value);
    const c = data.codex;
    const a = data.claude;
    const g = data.github;
    const codexStart = c && c.daily.length ? c.daily[0].date : null;
    const claudeStart = a && a.daily.length ? a.daily[0].date : null;
    const cCovered = c && codexStart && start <= c.asOf && end >= codexStart;
    const aCovered = a && claudeStart && start <= a.asOf && end >= claudeStart;
    const gCovered = g && start <= g.through && end >= g.from;
    const cRows = cCovered ? c.daily.filter(r => start <= r.date && r.date <= end) : [];
    const gRows = gCovered ? g.daily.filter(r => start <= r.date && r.date <= end) : [];
    return {
      tokens: cCovered ? sum(cRows, "tokens") : null,
      claudeTokens: aCovered ? sum(a.daily.filter(r => start <= r.date && r.date <= end), "tokens") : null,
      commits: gCovered ? sum(gRows, "commits") : null,
      mergedPrs: gCovered ? sum(gRows, "mergedPrs") : null,
      closedIssues: gCovered ? sum(gRows, "closedIssues") : null,
      additions: gCovered && gRows.every(r => r.additions !== null) ? sum(gRows, "additions") : null,
      deletions: gCovered && gRows.every(r => r.deletions !== null) ? sum(gRows, "deletions") : null,
      measured: sum(gRows, "measuredCommits"),
      partialCodex: !!(cCovered && mode !== "all" && (start < codexStart || end > c.asOf)),
      partialClaude: !!(aCovered && mode !== "all" && (start < claudeStart || end > a.asOf)),
      partialGithub: !!(gCovered && mode !== "all" && (start < g.from || end > g.through))
    };
  }
  function history(data, mode, value) {
    if (mode === "day") return [{label: value, ...select(data, "day", value)}];
    if (mode === "month") {
      const [start, end] = bounds(mode, value);
      const result = [];
      const latest = [data.codex?.asOf, data.claude?.asOf, data.github?.through].filter(Boolean).sort().pop();
      const last = latest && start <= latest && latest < end ? Number(latest.slice(-2)) : Number(end.slice(-2));
      for (let d = Number(start.slice(-2)); d <= last; d++) {
        const day = value + "-" + String(d).padStart(2, "0");
        result.push({label: day, ...select(data, "day", day)});
      }
      return result.reverse();
    }
    const months = new Set([...(data.codex?.daily || []), ...(data.claude?.daily || []), ...(data.github?.daily || [])]
      .map(r => r.date.slice(0, 7)));
    return Array.from(months).sort().reverse().map(month => ({label: month, ...select(data, "month", month)}));
  }
  const SOURCES = {codex: ["codex"], claude: ["claude"], total: ["codex", "claude"]};
  function comparison(data, mode, value, source = "codex") {
    const [requestedStart, requestedEnd] = bounds(mode, value);
    const tokenSources = SOURCES[source].map(key => data[key]);
    const g = data.github;
    const empty = {from: null, through: null, tokens: null, mergedPrs: null,
      closedIssues: null, prsPerMillion: null, issuesPerMillion: null};
    if (tokenSources.some(t => !t?.daily.length) || !g?.daily.length) return empty;
    // A combined source compares only dates that Codex, Claude Code and GitHub all cover.
    const from = [requestedStart, g.from, ...tokenSources.map(t => t.daily[0].date)].sort().pop();
    const through = [requestedEnd, g.through, ...tokenSources.map(t => t.asOf)].sort()[0];
    if (from > through) return empty;
    const tokens = tokenSources.reduce((total, t) =>
      total + sum(t.daily.filter(r => from <= r.date && r.date <= through), "tokens"), 0);
    const github = g.daily.filter(r => from <= r.date && r.date <= through);
    const mergedPrs = sum(github, "mergedPrs");
    const closedIssues = sum(github, "closedIssues");
    return {from, through, tokens, mergedPrs, closedIssues,
      prsPerMillion: tokens > 0 ? mergedPrs / tokens * 1000000 : null,
      issuesPerMillion: tokens > 0 ? closedIssues / tokens * 1000000 : null};
  }
  // Clean axis maximum: 1, 2, 2.5 or 5 times a power of ten.
  function niceMax(value) {
    if (!(value > 0)) return 1;
    const power = 10 ** Math.floor(Math.log10(value));
    return [1, 2, 2.5, 5, 10].find(step => step * power >= value) * power;
  }
  // Null only when neither source was collected; a single collected source is still a total.
  function tokenTotal(row) {
    return row.tokens === null && row.claudeTokens === null ? null : (row.tokens || 0) + (row.claudeTokens || 0);
  }
  if (typeof module !== "undefined" && module.exports) module.exports = {bounds, select, history, comparison, niceMax, tokenTotal};
  if (typeof document === "undefined") return;
  const root = document.getElementById("activity-dashboard");
  if (!root) return;
  const compact = new Intl.NumberFormat("ko-KR", {notation: "compact", maximumSignificantDigits: 3});
  const el = id => document.getElementById("activity-" + id);
  function node(tag, text, className) {
    const n = document.createElement(tag);
    if (text !== undefined) n.textContent = text;
    if (className) n.className = className;
    return n;
  }
  const swatch = key => node("i", undefined, "ad-key ad-key--" + key);
  function kpi(label, value, detail, key) {
    const item = node("div", undefined, "ad-kpi");
    const head = node("span", undefined, "ad-kpi-label");
    if (key) head.append(swatch(key));
    head.append(label);
    item.append(head, node("strong", value), node("small", detail));
    return item;
  }
  function facts(target, pairs) {
    target.replaceChildren(...pairs.flatMap(([term, value]) => {
      const row = node("div");
      row.append(node("dt", term), node("dd", value));
      return [row];
    }));
  }
  function duration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor(seconds % 3600 / 60);
    return (hours ? hours + "시간 " : "") + minutes + "분";
  }
  const shortLabel = label => label.length === 10 ? label.slice(5).replace("-", "/") : label.replace("-", ".");

  // Plain-DOM column chart. Stacked: segments share one column. Grouped: side by side.
  function chart(target, rows, series, options) {
    target.replaceChildren();
    target.setAttribute("role", "img");
    target.setAttribute("aria-label", options.title + ". 숫자는 아래 활동 내역 표에서 확인할 수 있습니다.");
    if (!rows.some(row => series.some(s => row[s.key] !== null))) {
      target.append(node("p", "이 기간에는 수집된 기록이 없습니다.", "ad-empty"));
      return;
    }
    const peak = Math.max(0, ...rows.map(row => options.stacked
      ? series.reduce((total, s) => total + (row[s.key] || 0), 0)
      : Math.max(...series.map(s => row[s.key] || 0))));
    const max = niceMax(peak);
    const plot = node("div", undefined, "ad-plot");
    for (const fraction of [1, 0.5, 0]) {
      const line = node("div", undefined, "ad-gridline");
      line.style.bottom = fraction * 100 + "%";
      if (fraction) line.append(node("span", compact.format(max * fraction) + (options.unit === "건" ? "건" : "")));
      plot.append(line);
    }
    const cols = node("div", undefined, "ad-cols");
    rows.forEach((row, index) => {
      const col = node("div", undefined, "ad-col" + (row.label === options.selected ? " is-selected" : ""));
      col.dataset.index = index;
      const marks = node("div", undefined, options.stacked ? "ad-stack" : "ad-bars");
      if (series.every(s => row[s.key] === null)) {
        marks.append(node("span", undefined, "ad-mark ad-mark--missing"));
      } else {
        for (const s of series) {
          const value = row[s.key];
          if (options.stacked && !value) continue;
          const mark = node("span", undefined, "ad-mark ad-mark--" + s.key);
          mark.style.height = (value || 0) / max * 100 + "%";
          marks.append(mark);
        }
      }
      col.append(marks);
      cols.append(col);
    });
    plot.append(cols);
    const axis = node("div", undefined, "ad-xaxis");
    const step = rows.length > 16 ? 7 : rows.length > 8 ? 2 : 1;
    rows.forEach((row, index) => {
      if (index % step) return;
      const tick = node("span", shortLabel(row.label));
      tick.style.left = (index + 0.5) / rows.length * 100 + "%";
      axis.append(tick);
    });
    const tip = node("div", undefined, "ad-tooltip");
    tip.hidden = true;
    target.append(plot, axis, tip);
    let hovered = null;
    cols.addEventListener("pointermove", event => {
      const col = event.target.closest(".ad-col");
      if (!col || col === hovered) return;
      if (hovered) hovered.classList.remove("is-hover");
      hovered = col;
      col.classList.add("is-hover");
      const row = rows[Number(col.dataset.index)];
      const lines = [node("strong", row.label)];
      for (const s of series) {
        const line = node("span");
        line.append(swatch(s.color), s.name + " ", node("b", row[s.key] === null ? "미수집" : count(row[s.key]) + " " + options.unit));
        lines.push(line);
      }
      if (options.stacked && series.some(s => row[s.key] !== null)) {
        lines.push(node("span", "합계 " + count(series.reduce((total, s) => total + (row[s.key] || 0), 0)) + " " + options.unit, "ad-tooltip-total"));
      }
      tip.replaceChildren(...lines);
      tip.hidden = false;
      const box = target.getBoundingClientRect();
      const colBox = col.getBoundingClientRect();
      const center = colBox.left - box.left + colBox.width / 2;
      const left = Math.min(Math.max(center - tip.offsetWidth / 2, 0), box.width - tip.offsetWidth);
      tip.style.left = left + "px";
    });
    cols.addEventListener("pointerleave", () => {
      if (hovered) hovered.classList.remove("is-hover");
      hovered = null;
      tip.hidden = true;
    });
  }

  async function start() {
    try {
      const response = await fetch(root.dataset.source, {cache: "no-cache", credentials: "omit"});
      if (!response.ok) throw new Error();
      const data = await response.json();
      if (data.schemaVersion !== 1 || data.timezone !== "Asia/Seoul") throw new Error();
      const c = data.codex;
      const a = data.claude || null;
      data.claude = a;
      const g = data.github;

      el("codex-total").textContent = c ? compact.format(c.summary.lifetimeTokens) : "미수집";
      el("codex-asof").textContent = c ? c.asOf + " 기준" : "";
      el("codex-total").title = c ? count(c.summary.lifetimeTokens) + " 토큰" : "";
      if (c) facts(el("codex-facts"), [
        ["정확한 값", count(c.summary.lifetimeTokens)],
        ["하루 최대", count(c.summary.peakDailyTokens)],
        ["연속 활동", count(c.summary.currentStreakDays) + "일 (최장 " + count(c.summary.longestStreakDays) + "일)"],
        ["최장 작업", duration(c.summary.longestRunningTurnSec)]
      ]);
      el("claude-total").textContent = a ? compact.format(a.summary.totalTokens) : "미수집";
      el("claude-asof").textContent = a ? a.asOf + " 기준" : "";
      el("claude-total").title = a ? count(a.summary.totalTokens) + " 토큰" : "";
      if (a) {
        el("claude-range").textContent = (a.daily.length ? a.daily[0].date + "부터 " : "") + "이 PC에 남은 기록 · 토큰";
        facts(el("claude-facts"), [
          ["정확한 값", count(a.summary.totalTokens)],
          ["하루 최대", count(a.summary.peakDailyTokens)],
          ["활동일", count(a.summary.activeDays) + "일"]
        ]);
      }

      const latest = [c?.asOf, a?.asOf, g?.through].filter(Boolean).sort().pop();
      if (!latest) throw new Error();
      el("day").value = latest;
      el("month").value = latest.slice(0, 7);
      const today = new Intl.DateTimeFormat("sv-SE", {timeZone: "Asia/Seoul"}).format(new Date());
      const notes = ["마지막 수집 · Codex " + (c ? c.asOf : "미수집"), "Claude Code " + (a ? a.asOf : "미수집"),
        "GitHub " + (g ? g.through + "까지" : "미수집")];
      el("status").textContent = notes.join(" · ") + ([c?.asOf, a?.asOf].some(day => day && day < today) ? " · 실시간 사용량이 아닙니다" : "");
      el("content").hidden = false;

      const periodInputs = Array.from(root.querySelectorAll('input[name="activity-period"]'));
      function render() {
        const mode = periodInputs.find(input => input.checked).value;
        const value = mode === "day" ? el("day").value : el("month").value;
        if (mode !== "all" && !/^\d{4}-\d{2}(-\d{2})?$/.test(value)) return;
        el("day-label").hidden = mode !== "day";
        el("month-label").hidden = mode !== "month";
        const selected = select(data, mode, value);
        const partial = [];
        if (selected.partialCodex) partial.push("Codex");
        if (selected.partialClaude) partial.push("Claude Code");
        if (selected.partialGithub) partial.push("GitHub");
        el("period-note").textContent = partial.length ? partial.join("·") + " 일부 날짜만 수집됨" : "";

        const total = tokenTotal(selected);
        const totalDetail = selected.tokens === null && selected.claudeTokens !== null ? "Codex 미수집"
          : selected.claudeTokens === null && selected.tokens !== null ? "Claude Code 미수집" : "두 도구 합계";
        el("token-kpis").replaceChildren(
          kpi("Codex", count(selected.tokens), selected.tokens === null ? "미수집" : compact.format(selected.tokens) + " 토큰", "codex"),
          kpi("Claude Code", count(selected.claudeTokens), selected.claudeTokens === null ? "미수집" : compact.format(selected.claudeTokens) + " 토큰", "claude"),
          kpi("합계", count(total), total === null ? "미수집" : totalDetail)
        );
        el("github-kpis").replaceChildren(
          kpi("커밋", count(selected.commits), "기본 브랜치 · 본인 작성"),
          kpi("병합 PR", count(selected.mergedPrs), "본인 작성", "prs"),
          kpi("완료 이슈", count(selected.closedIssues), "본인 작성 · completed", "issues")
        );

        // A single day is shown inside its month so the chart still has context.
        const rows = mode === "day" ? history(data, "month", value.slice(0, 7)) : history(data, mode, value);
        const ordered = rows.slice().reverse();
        const unitName = mode === "all" ? "월별" : "일별";
        el("token-chart-title").textContent = unitName + " 토큰";
        el("github-chart-title").textContent = unitName + " 병합 PR·완료 이슈";
        const pick = mode === "day" ? value : null;
        chart(el("token-chart"), ordered, [{key: "tokens", name: "Codex", color: "codex"}, {key: "claudeTokens", name: "Claude Code", color: "claude"}],
          {stacked: true, unit: "토큰", selected: pick, title: unitName + " Codex·Claude Code 토큰 누적 막대"});
        chart(el("github-chart"), ordered, [{key: "mergedPrs", name: "병합 PR", color: "prs"}, {key: "closedIssues", name: "완료 이슈", color: "issues"}],
          {stacked: false, unit: "건", selected: pick, title: unitName + " 병합 PR·완료 이슈 막대"});

        el("rates").replaceChildren(...[["codex", "Codex"], ["claude", "Claude Code"], ["total", "합계"]].map(([source, name]) => {
          const result = comparison(data, mode, value, source);
          const tr = node("tr");
          const th = node("th");
          th.scope = "row";
          if (source !== "total") th.append(swatch(source));
          th.append(name);
          const period = !result.from ? "함께 수집된 날짜 없음" : result.tokens === 0 ? "사용 토큰 0" : result.from + " ~ " + result.through;
          tr.append(th, node("td", rate(result.prsPerMillion)), node("td", rate(result.issuesPerMillion)), node("td", period, "ad-muted"));
          return tr;
        }));

        el("table-caption").textContent = (mode === "all" ? "월별 내역" : value.slice(0, 7) + " 일별 내역") + " · *는 일부 수집, —는 미수집";
        el("history").replaceChildren(...rows.map(row => {
          const tr = node("tr", undefined, row.label === pick ? "is-selected" : "");
          const heading = node("th", row.label + (row.partialCodex || row.partialClaude || row.partialGithub ? " *" : ""));
          heading.scope = "row";
          tr.append(heading);
          [row.tokens, row.claudeTokens, row.commits, row.mergedPrs, row.closedIssues].forEach(v => tr.append(node("td", count(v))));
          return tr;
        }));
      }
      [...periodInputs, el("day"), el("month")].forEach(input => input.addEventListener("change", render));
      render();
    } catch (_) {
      el("content").hidden = true;
      el("status").textContent = "기록을 불러오지 못했습니다. 잠시 후 다시 열어 주세요.";
    }
  }
  start();
}());
