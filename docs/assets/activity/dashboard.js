/* Numeric public data only. No third-party scripts, analytics, or API credentials. */
(function () {
  "use strict";
  const format = new Intl.NumberFormat("ko-KR");
  const count = value => value == null ? "—" : format.format(value);
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
    const g = data.github;
    const codexStart = c && c.daily.length ? c.daily[0].date : null;
    const cCovered = c && codexStart && start <= c.asOf && end >= codexStart;
    const gCovered = g && start <= g.through && end >= g.from;
    const cRows = cCovered ? c.daily.filter(r => start <= r.date && r.date <= end) : [];
    const gRows = gCovered ? g.daily.filter(r => start <= r.date && r.date <= end) : [];
    return {
      tokens: cCovered ? sum(cRows, "tokens") : null,
      commits: gCovered ? sum(gRows, "commits") : null,
      mergedPrs: gCovered ? sum(gRows, "mergedPrs") : null,
      closedIssues: gCovered ? sum(gRows, "closedIssues") : null,
      additions: gCovered && gRows.every(r => r.additions !== null) ? sum(gRows, "additions") : null,
      deletions: gCovered && gRows.every(r => r.deletions !== null) ? sum(gRows, "deletions") : null,
      measured: sum(gRows, "measuredCommits"),
      partialCodex: !!(cCovered && mode !== "all" && (start < codexStart || end > c.asOf)),
      partialGithub: !!(gCovered && mode !== "all" && (start < g.from || end > g.through))
    };
  }
  function history(data, mode, value) {
    if (mode === "day") return [{label: value, ...select(data, "day", value)}];
    if (mode === "month") {
      const [start, end] = bounds(mode, value);
      const result = [];
      const latest = [data.codex?.asOf, data.github?.through].filter(Boolean).sort().pop();
      const last = latest && start <= latest && latest < end ? Number(latest.slice(-2)) : Number(end.slice(-2));
      for (let d = Number(start.slice(-2)); d <= last; d++) {
        const day = value + "-" + String(d).padStart(2, "0");
        result.push({label: day, ...select(data, "day", day)});
      }
      return result.reverse();
    }
    const months = new Set([...(data.codex?.daily || []), ...(data.github?.daily || [])]
      .map(r => r.date.slice(0, 7)));
    return Array.from(months).sort().reverse().map(month => ({label: month, ...select(data, "month", month)}));
  }
  if (typeof module !== "undefined" && module.exports) module.exports = {bounds, select, history};
  if (typeof document === "undefined") return;
  const root = document.getElementById("activity-dashboard");
  if (!root) return;
  const el = id => document.getElementById("activity-" + id);
  function node(tag, text, className) {
    const n = document.createElement(tag);
    if (text !== undefined) n.textContent = text;
    if (className) n.className = className;
    return n;
  }
  function card(title, value, detail) {
    const article = node("div", undefined, "activity-card");
    article.append(node("span", title, "activity-card-title"), node("strong", value), node("small", detail));
    return article;
  }
  function duration(seconds) {
    return Math.floor(seconds / 3600) + "시간 " + Math.floor(seconds % 3600 / 60) + "분 " + seconds % 60 + "초";
  }
  async function start() {
    try {
      const response = await fetch(root.dataset.source, {cache: "no-cache", credentials: "omit"});
      if (!response.ok) throw new Error();
      const data = await response.json();
      if (data.schemaVersion !== 1 || data.timezone !== "Asia/Seoul") throw new Error();
      const c = data.codex;
      const g = data.github;
      el("lifetime").textContent = c ? count(c.summary.lifetimeTokens) : "미수집";
      el("codex-date").textContent = c ? c.asOf + " 기준 · 프로필 전체 기록" : "Codex 로컬 수집을 기다리고 있습니다.";
      if (c) {
        el("records").append(
          card("연속 활동", count(c.summary.currentStreakDays) + "일", "수집 시점 기준"),
          card("최장 연속 활동", count(c.summary.longestStreakDays) + "일", "프로필 기록"),
          card("최장 작업", duration(c.summary.longestRunningTurnSec), "단일 turn 실행 시간"),
          card("하루 최대 토큰", count(c.summary.peakDailyTokens), "프로필 기록")
        );
      }
      const latest = [c?.asOf, g?.through].filter(Boolean).sort().pop();
      if (!latest) throw new Error();
      el("day").value = latest;
      el("month").value = latest.slice(0, 7);
      const today = new Intl.DateTimeFormat("sv-SE", {timeZone: "Asia/Seoul"}).format(new Date());
      const notes = [c ? "Codex " + c.asOf : "Codex 미수집", g ? "GitHub " + g.from + " ~ " + g.through : "GitHub 미수집 · 대상·인증 설정 후 갱신"];
      if (c && c.asOf < today) notes.push("오늘의 실시간 사용량이 아닙니다");
      el("status").textContent = notes.join(" / ");
      el("content").hidden = false;

      function render() {
        const mode = el("period").value;
        const value = mode === "day" ? el("day").value : el("month").value;
        if (mode !== "all" && !/^\d{4}-\d{2}(-\d{2})?$/.test(value)) return;
        el("day-label").hidden = mode !== "day";
        el("month-label").hidden = mode !== "month";
        const selected = select(data, mode, value);
        const partial = [];
        if (selected.partialCodex) partial.push("Codex 일부 수집");
        if (selected.partialGithub) partial.push("GitHub 일부 수집");
        el("period-note").textContent = (mode === "all" ? "Codex 전체 기록 · GitHub 수집 구간 내 누적" : value) + (partial.length ? " · " + partial.join(" / ") : "") + " · —는 미수집";
        el("metrics").replaceChildren(
          card("사용 토큰", count(selected.tokens), selected.tokens === null ? "미수집" : "선택 기간"),
          card("커밋", count(selected.commits), "기본 브랜치 · 본인 작성"),
          card("병합 PR", count(selected.mergedPrs), "본인 작성 PR"),
          card("완료 이슈", count(selected.closedIssues), "본인 작성 · completed"),
          card("추가 / 삭제 줄", selected.additions === null ? "—" : "+" + count(selected.additions) + " / −" + count(selected.deletions), selected.additions === null ? "변경량 미수집" : "병합 제외 · " + count(selected.measured) + "개 커밋 측정")
        );
        const rows = history(data, mode, value);
        el("table-caption").textContent = mode === "all" ? "월별 내역 · 일부 수집된 월은 * 표시" : value + " 내역";
        const body = rows.map(row => {
          const tr = node("tr");
          const heading = node("th", row.label + (row.partialCodex || row.partialGithub ? " *" : ""));
          heading.scope = "row";
          tr.append(heading);
          [row.tokens, row.commits, row.mergedPrs, row.closedIssues].forEach(v => tr.append(node("td", count(v))));
          tr.append(node("td", row.additions === null ? "—" : "+" + count(row.additions) + " / −" + count(row.deletions)));
          return tr;
        });
        el("history").replaceChildren(...body);
        draw(rows.slice().reverse());
        el("chart-note").textContent = mode === "all" ? "월별 합계 · 정확한 숫자는 아래 표에서 확인할 수 있습니다." : "일별 사용량 · 빈 날짜는 미수집입니다. 정확한 숫자는 아래 표에서 확인할 수 있습니다.";
      }
      function draw(rows) {
        const chart = el("chart");
        chart.replaceChildren();
        if (!rows.some(r => r.tokens !== null)) {
          chart.append(node("p", "이 기간의 Codex 기록이 없습니다."));
          return;
        }
        const max = Math.max(...rows.map(r => r.tokens || 0), 1);
        const bars = node("div", undefined, "activity-bars");
        bars.setAttribute("aria-hidden", "true");
        for (const row of rows) {
          const bar = node("span", undefined, "activity-bar" + (row.tokens === null ? " activity-bar--missing" : ""));
          bar.style.height = (row.tokens === null ? 2 : Math.max(2, row.tokens / max * 100)) + "%";
          bar.title = row.label + ": " + (row.tokens === null ? "미수집" : count(row.tokens) + " 토큰");
          bars.append(bar);
        }
        const axis = node("div", undefined, "activity-chart-axis");
        axis.append(node("span", rows[0].label), node("span", "최대 " + count(max)), node("span", rows[rows.length-1].label));
        chart.append(bars, axis);
      }
      ["period", "day", "month"].forEach(id => el(id).addEventListener("change", render));
      render();
    } catch (_) {
      el("content").hidden = true;
      el("status").textContent = "기록을 불러오지 못했습니다. 잠시 후 다시 열어 주세요.";
    }
  }
  start();
}());
