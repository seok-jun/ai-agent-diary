const test = require("node:test");
const assert = require("node:assert/strict");
const {summarize} = require("../../docs/assets/activity/home-summary.js");

const github = (from, through, daily) => ({from, through, daily});
const day = (date, mergedPrs, closedIssues = 0) => ({date, commits: 0, mergedPrs, closedIssues});

test("window is the 30 days ending on the last GitHub date", () => {
  const s = summarize({github: github("2026-09-01", "2026-10-17", [day("2026-10-17", 3), day("2026-09-17", 9), day("2026-09-18", 2)])});
  assert.equal(s.from, "2026-09-18");
  assert.equal(s.through, "2026-10-17");
  assert.equal(s.rows.length, 30);
  assert.equal(s.mergedPrs, 5);
});

test("days before GitHub collection are uncollected, not zero", () => {
  const s = summarize({github: github("2026-10-10", "2026-10-17", [day("2026-10-10", 1)])});
  assert.equal(s.rows[0].mergedPrs, null);
  assert.equal(s.rows.find(r => r.date === "2026-10-11").mergedPrs, 0);
  assert.equal(s.mergedPrs, 1);
});

test("tokens add both tools, count gaps inside coverage as zero, and flag partial windows", () => {
  const s = summarize({
    github: github("2026-09-01", "2026-10-17", []),
    codex: {asOf: "2026-10-17", daily: [{date: "2026-09-01", tokens: 10}, {date: "2026-10-17", tokens: 5}]},
    claude: {asOf: "2026-10-17", daily: [{date: "2026-10-16", tokens: 7}]}
  });
  assert.equal(s.tokens, 12);
  assert.equal(s.rows.find(r => r.date === "2026-10-01").tokens, 0);
  assert.equal(s.partialTokens, false);
  const late = summarize({
    github: github("2026-09-01", "2026-10-17", []),
    codex: {asOf: "2026-10-17", daily: [{date: "2026-10-10", tokens: 4}]}
  });
  assert.equal(late.rows[0].tokens, null);
  assert.equal(late.tokens, 4);
  assert.equal(late.partialTokens, true);
});

test("no GitHub data means no summary", () => {
  assert.equal(summarize({github: null}), null);
  assert.equal(summarize({github: github("2026-10-01", "2026-10-01", [])}).mergedPrs, 0);
});
