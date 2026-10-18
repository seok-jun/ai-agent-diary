/* Home hero: last-30-day numbers from the public activity JSON. No third-party scripts or credentials. */
(function () {
  "use strict";
  const DAYS = 30;
  const addDays = (date, days) => {
    const d = new Date(date + "T00:00:00Z");
    d.setUTCDate(d.getUTCDate() + days);
    return d.toISOString().slice(0, 10);
  };
  // Tokens for one source on one date: null when the date is outside what was collected.
  function tokensOn(source, date) {
    if (!source || !source.daily.length || date < source.daily[0].date || date > source.asOf) return null;
    const row = source.daily.find(r => r.date === date);
    return row ? row.tokens : 0;
  }
  // The window ends on the last GitHub date, not today, so a late collection never reads as zero.
  function summarize(data) {
    const g = data.github;
    if (!g || !g.from || !g.through) return null;
    const through = g.through;
    const from = addDays(through, -(DAYS - 1));
    const rows = [];
    for (let date = from; date <= through; date = addDays(date, 1)) {
      const day = g.daily.find(r => r.date === date);
      const covered = date >= g.from;
      const codex = tokensOn(data.codex, date);
      const claude = tokensOn(data.claude, date);
      rows.push({
        date,
        mergedPrs: covered ? (day ? day.mergedPrs : 0) : null,
        closedIssues: covered ? (day ? day.closedIssues : 0) : null,
        tokens: codex === null && claude === null ? null : (codex || 0) + (claude || 0)
      });
    }
    const total = key => rows.some(r => r[key] !== null) ? rows.reduce((t, r) => t + (r[key] || 0), 0) : null;
    return {
      from, through, rows,
      mergedPrs: total("mergedPrs"),
      closedIssues: total("closedIssues"),
      tokens: total("tokens"),
      partialTokens: rows.some(r => r.tokens === null) && rows.some(r => r.tokens !== null)
    };
  }
  if (typeof module !== "undefined" && module.exports) module.exports = {summarize};
  if (typeof document === "undefined") return;
  const root = document.getElementById("home-activity");
  if (!root) return;

  const format = new Intl.NumberFormat("ko-KR");
  const compact = new Intl.NumberFormat("ko-KR", {notation: "compact", maximumSignificantDigits: 3});
  const count = value => value === null ? "—" : format.format(value);

  async function start() {
    try {
      const response = await fetch(root.dataset.source, {cache: "no-cache", credentials: "omit"});
      if (!response.ok) return;
      const summary = summarize(await response.json());
      if (!summary || summary.mergedPrs === null) return;
      const set = (name, text) => { root.querySelector("[data-ha=" + name + "]").textContent = text; };
      set("prs", count(summary.mergedPrs));
      set("issues", count(summary.closedIssues));
      set("tokens", summary.tokens === null ? "—" : compact.format(summary.tokens));
      set("tokens-note", summary.partialTokens ? "캐시 포함 · 일부 수집" : "캐시 포함");
      set("asof", summary.through.slice(5).replace("-", ".") + " 기준");
      root.title = summary.from.replaceAll("-", ".") + " – " + summary.through.replaceAll("-", ".");
      root.hidden = false;
    } catch (error) {
      // The line stays hidden; the link to the activity page still works.
    }
  }
  start();
})();
