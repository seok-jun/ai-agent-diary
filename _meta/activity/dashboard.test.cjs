const test = require("node:test");
const assert = require("node:assert/strict");
const {bounds, select, history} = require("../../docs/assets/activity/dashboard.js");
const data = {codex: {asOf: "2026-10-16", daily: [{date: "2026-09-30", tokens: 10}, {date: "2026-10-01", tokens: 20}]},
  github: {from: "2026-10-01", through: "2026-10-02", daily: [
    {date: "2026-10-01", commits: 1, mergedPrs: 2, closedIssues: 3, additions: 4, deletions: 5, measuredCommits: 1},
    {date: "2026-10-02", commits: 0, mergedPrs: 0, closedIssues: 0, additions: 0, deletions: 0, measuredCommits: 0}]} };
test("KST date labels, calendar months and leap years", () => {
  assert.deepEqual(bounds("month", "2024-02"), ["2024-02-01", "2024-02-29"]);
  assert.equal(history(data, "month", "2026-10").length, 16);
  assert.equal(history(data, "month", "2026-10")[0].label, "2026-10-16");
  assert.equal(history(data, "month", "2026-09").length, 30);
});
test("uncollected differs from a measured zero", () => {
  assert.equal(select(data, "day", "2026-09-29").tokens, null);
  assert.equal(select(data, "day", "2026-10-02").tokens, 0);
  assert.equal(select(data, "day", "2026-10-02").commits, 0);
  assert.equal(select(data, "day", "2026-10-03").commits, null);
  assert.equal(select({...data, github: null}, "all", "").commits, null);
});
test("monthly and lifetime aggregates preserve coverage", () => {
  const month = select(data, "month", "2026-10");
  assert.equal(month.tokens, 20);
  assert.equal(month.commits, 1);
  assert.equal(month.mergedPrs, 2);
  assert.equal(month.closedIssues, 3);
  assert.equal(month.additions, 4);
  assert.equal(month.partialCodex, true);
  assert.equal(month.partialGithub, true);
  assert.equal(select(data, "all", "").tokens, 30);
  assert.deepEqual(history(data, "all", "").map(r => r.label), ["2026-10", "2026-09"]);
});
test("unknown line measurements are never represented as zero", () => {
  const other = structuredClone(data);
  other.github.daily[1].additions = null;
  other.github.daily[1].deletions = null;
  assert.equal(select(other, "month", "2026-10").additions, null);
});
