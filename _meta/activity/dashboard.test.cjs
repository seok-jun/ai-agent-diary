const test = require("node:test");
const assert = require("node:assert/strict");
const {bounds, select, history, comparison, niceMax, tokenTotal} = require("../../docs/assets/activity/dashboard.js");
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

test("comparison clips both sources to the same dates", () => {
  const result = comparison(data, "all", "");
  assert.equal(result.from, "2026-10-01");
  assert.equal(result.through, "2026-10-02");
  assert.equal(result.tokens, 20); // September tokens are outside GitHub coverage.
  assert.equal(result.mergedPrs, 2);
  assert.equal(result.closedIssues, 3);
  assert.equal(result.prsPerMillion, 100000);
  assert.equal(comparison(data, "month", "2026-10").tokens, 20);
});

test("rates use total counts divided by total tokens, not daily rate averages", () => {
  const sample = structuredClone(data);
  sample.codex.daily = [{date: "2026-10-01", tokens: 1000000}, {date: "2026-10-02", tokens: 3000000}];
  sample.github.daily[1].mergedPrs = 6;
  assert.equal(comparison(sample, "all", "").prsPerMillion, 2);
  assert.equal(comparison(sample, "day", "2026-10-01").prsPerMillion, 2);
  assert.equal(comparison(sample, "all", "").issuesPerMillion, 0.75);
});

test("zero tokens are distinct from missing coverage and zero outcomes", () => {
  const zero = comparison(data, "day", "2026-10-02");
  assert.equal(zero.tokens, 0);
  assert.equal(zero.prsPerMillion, null);
  const sample = structuredClone(data);
  sample.codex.daily.push({date: "2026-10-02", tokens: 1000000});
  assert.equal(comparison(sample, "day", "2026-10-02").prsPerMillion, 0);
  for (const missing of [{...data, codex: null}, {...data, github: null},
    {...data, codex: {...data.codex, daily: []}},
    {...data, github: {...data.github, daily: []}}]) {
    assert.equal(comparison(missing, "all", "").tokens, null);
  }
  assert.equal(comparison(data, "month", "2026-09").from, null);
  assert.equal(comparison(data, "day", "2026-10-03").tokens, null);
});

test("partial months and Codex end dates constrain the comparison", () => {
  const sample = structuredClone(data);
  sample.codex.asOf = "2026-10-01";
  sample.github.daily[1].mergedPrs = 50;
  const result = comparison(sample, "month", "2026-10");
  assert.equal(result.from, "2026-10-01");
  assert.equal(result.through, "2026-10-01");
  assert.equal(result.mergedPrs, 2);
  assert.equal(comparison(sample, "day", "2026-10-02").tokens, null);
});

test("Claude tokens are a separate source with their own coverage", () => {
  const sample = {...structuredClone(data), claude: {asOf: "2026-10-02", daily: [{date: "2026-10-02", tokens: 7}]}};
  assert.equal(select(sample, "day", "2026-10-01").claudeTokens, null);
  assert.equal(select(sample, "day", "2026-10-02").claudeTokens, 7);
  assert.equal(select(sample, "month", "2026-10").claudeTokens, 7);
  assert.equal(select(sample, "month", "2026-10").partialClaude, true);
  assert.equal(select(sample, "month", "2026-10").tokens, 20);
  assert.equal(select(data, "all", "").claudeTokens, null);
  assert.equal(history(sample, "month", "2026-10")[0].label, "2026-10-16");
});

test("comparison can use Claude Code or the combined token total", () => {
  const sample = {...structuredClone(data), claude: {asOf: "2026-10-02", daily: [
    {date: "2026-10-01", tokens: 30}, {date: "2026-10-02", tokens: 50}]}};
  assert.equal(comparison(sample, "all", "").tokens, 20);
  const claude = comparison(sample, "all", "", "claude");
  assert.equal(claude.tokens, 80);
  assert.equal(claude.mergedPrs, 2);
  assert.equal(claude.prsPerMillion, 25000);
  const total = comparison(sample, "all", "", "total");
  assert.equal(total.from, "2026-10-01");
  assert.equal(total.tokens, 100); // Codex 20 + Claude 80 within shared coverage.
  sample.claude.daily.shift();
  // The combined total starts only when every source is collected.
  assert.equal(comparison(sample, "all", "", "total").from, "2026-10-02");
  assert.equal(comparison(sample, "all", "", "total").tokens, 50);
  assert.equal(comparison(data, "all", "", "claude").tokens, null);
  assert.equal(comparison(data, "all", "", "total").tokens, null);
});

test("chart axis maximum rounds up to a clean number", () => {
  assert.equal(niceMax(0), 1);
  assert.equal(niceMax(7), 10);
  assert.equal(niceMax(29), 50);
  assert.equal(niceMax(385210248), 500000000);
  assert.equal(niceMax(1293574512), 2000000000);
  assert.equal(niceMax(200), 200);
});

test("token total is missing only when neither tool was collected", () => {
  assert.equal(tokenTotal({tokens: null, claudeTokens: null}), null);
  assert.equal(tokenTotal({tokens: 5, claudeTokens: null}), 5);
  assert.equal(tokenTotal({tokens: 0, claudeTokens: 7}), 7);
  assert.equal(tokenTotal({tokens: 5, claudeTokens: 7}), 12);
});
