import contextlib
import copy
import datetime as dt
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import collect as c

CANARY = "PRIVATE_REPO_PATH_TITLE_MESSAGE_TOKEN_CANARY"
DAY = "2026-10-01"
USER = {"login": "sample-user"}


def codex():
    return {"contractVersion": 1, "capturedAt": "2026-10-02T00:00:00Z",
            "summary": dict(zip(c.SUMMARY, (10, 10, 50, 1, 1))),
            "dailyUsageBuckets": [{"startDate": DAY, "tokens": 10}]}


def config(lines=True):
    return {"login": "sample-user", "repositories": ["sample/placeholder"],
            "since": DAY, "withLines": lines}


def commit(sha="a" * 40, stamp="2026-09-30T15:00:00Z", parents=1, user=USER):
    return {"sha": sha, "author": user, "commit": {"committer": {"date": stamp},
            "message": CANARY}, "parents": [{}] * parents}


class FakeAPI:
    def __init__(self, commits=None):
        self.commits = commits if commits is not None else [commit()]
        self.details = 0

    def get(self, path, params=None):
        if "/commits/" in path:
            self.details += 1
            return {"stats": {"additions": 8, "deletions": 3}, "files": [CANARY]}
        return {"default_branch": "main", "name": CANARY}

    def pages(self, path, params=None, stop_before=None):
        if path.endswith("/commits"):
            return iter(self.commits)
        if path.endswith("/pulls"):
            return iter([
                {"user": USER, "merged_at": "2026-09-30T15:00:00Z", "title": CANARY},
                {"user": USER, "merged_at": "2026-10-01T15:00:00Z"},
                {"user": {"login": "someone-else"}, "merged_at": "2026-10-01T00:00:00Z"},
                {"user": USER, "merged_at": None}])
        return iter([
            {"user": USER, "state_reason": "completed", "closed_at": "2026-10-01T00:00:00Z", "title": CANARY},
            {"user": USER, "state_reason": "not_planned", "closed_at": "2026-10-01T00:00:00Z"},
            {"user": USER, "state_reason": "completed", "closed_at": "2026-10-01T00:00:00Z", "pull_request": {}},
            {"user": USER, "state_reason": "completed", "closed_at": "2026-09-30T14:59:59Z"}])


class PublicDataTests(unittest.TestCase):
    def test_allowlist_discards_private_fields_at_every_input_level(self):
        raw = codex()
        raw["source"] = CANARY
        raw["summary"]["path"] = CANARY
        raw["dailyUsageBuckets"][0]["session"] = CANARY
        result = c.sanitize_codex(raw)
        self.assertNotIn(CANARY, json.dumps(result))
        self.assertEqual(result["summary"]["lifetimeTokens"], 10)

    def test_rejects_bad_dates_counts_contracts_duplicates_and_totals(self):
        mutations = [
            lambda r: r.update(contractVersion=2),
            lambda r: r.update(contractVersion=True),
            lambda r: r.update(capturedAt="2026-10-01"),
            lambda r: r["dailyUsageBuckets"][0].update(startDate="2026-02-30"),
            lambda r: r["dailyUsageBuckets"][0].update(tokens=True),
            lambda r: r["dailyUsageBuckets"][0].update(tokens=-1),
            lambda r: r["dailyUsageBuckets"][0].update(tokens=1.0),
            lambda r: r["dailyUsageBuckets"].append(copy.deepcopy(r["dailyUsageBuckets"][0])),
            lambda r: r["summary"].update(lifetimeTokens=11),
            lambda r: r["summary"].update(peakDailyTokens=11),
            lambda r: r["summary"].update(longestRunningTurnSec=2**53),
            lambda r: r["summary"].update(currentStreakDays=2)]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                raw = codex()
                mutate(raw)
                with self.assertRaises(c.SafeError):
                    c.sanitize_codex(raw)

    def test_closed_public_schema_rejects_unknown_fields(self):
        base = {"schemaVersion": 1, "timezone": "Asia/Seoul", "codex": c.sanitize_codex(codex()), "github": None}
        for target in [base, base["codex"], base["codex"]["summary"], base["codex"]["daily"][0]]:
            target["private"] = CANARY
            with self.assertRaises(c.SafeError):
                c.validate(base)
            del target["private"]

    def test_json_duplicates_and_nan_fail(self):
        for text in ['{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}']:
            with self.assertRaises(c.SafeError):
                c.decode(text)

    def test_atomic_idempotent_write_and_failures_preserve_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "public.json"
            data = {"schemaVersion": 1, "timezone": "Asia/Seoul", "codex": c.sanitize_codex(codex()), "github": None}
            self.assertTrue(c.save_public(data, path))
            original = path.read_bytes()
            self.assertFalse(c.save_public(data, path))
            data["codex"]["private"] = CANARY
            with self.assertRaises(c.SafeError):
                c.save_public(data, path)
            self.assertEqual(path.read_bytes(), original)
            del data["codex"]["private"]
            data["codex"]["summary"]["longestRunningTurnSec"] += 1
            with patch.object(c.os, "replace", side_effect=OSError(CANARY)):
                with self.assertRaises(OSError):
                    c.save_public(data, path)
            self.assertEqual(path.read_bytes(), original)
            self.assertEqual(len(list(Path(folder).iterdir())), 1)

    def test_errors_do_not_log_arguments_upstream_body_or_paths(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "public.json"
            base = {"schemaVersion": 1, "timezone": "Asia/Seoul", "codex": c.sanitize_codex(codex()), "github": None}
            c.save_public(base, path)
            original = path.read_bytes()
            for argv in [["codex", "--input", CANARY], ["github", "--unknown-" + CANARY], ["github"]]:
                stdout, stderr = io.StringIO(), io.StringIO()
                with patch.object(c, "OUTPUT", path), patch.object(c.GitHub, "get", side_effect=RuntimeError(CANARY)), patch.dict(c.os.environ, {"ACTIVITY_CONFIG_JSON": json.dumps(config()), "ACTIVITY_READ_TOKEN": CANARY}), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    self.assertEqual(c.main(argv), 1)
                self.assertNotIn(CANARY, stdout.getvalue() + stderr.getvalue())
                self.assertEqual(path.read_bytes(), original)

    def test_no_raw_inputs_inside_checkout(self):
        with self.assertRaises(c.SafeError):
            c.private_file(c.ROOT / "docs/raw.json")

    def test_analyzer_stdout_is_sanitized_and_stderr_is_never_printed(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "data.json"
            executable = Path(folder) / "analyzer.cmd"
            executable.touch()
            raw = codex()
            raw["private"] = CANARY
            stdout, stderr = io.StringIO(), io.StringIO()
            process = c.subprocess.CompletedProcess([], 0, json.dumps(raw).encode(), CANARY.encode())
            with patch.object(c, "OUTPUT", output), patch.object(c.subprocess, "run", return_value=process), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                self.assertEqual(c.main(["codex", "--analyzer", str(executable)]), 0)
            self.assertNotIn(CANARY, output.read_text() + stdout.getvalue() + stderr.getvalue())
            original = output.read_bytes()
            process.returncode = 1
            with patch.object(c, "OUTPUT", output), patch.object(c.subprocess, "run", return_value=process), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                self.assertEqual(c.main(["codex", "--analyzer", str(executable)]), 1)
            self.assertEqual(output.read_bytes(), original)
            self.assertNotIn(CANARY, stdout.getvalue() + stderr.getvalue())

    def test_lock_prevents_overlapping_updates(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(c, "OUTPUT", Path(folder) / "data.json"):
            with c.lock_output():
                with self.assertRaises(FileExistsError):
                    with c.lock_output():
                        self.fail("second collector entered")
            self.assertFalse((Path(folder) / ".collect.lock").exists())


class GitHubTests(unittest.TestCase):
    def test_duplicate_repo_case_is_rejected_before_requests(self):
        cfg = config()
        cfg["repositories"].append("SAMPLE/PLACEHOLDER")
        api = FakeAPI()
        with patch.object(api, "get") as get:
            with self.assertRaises(c.SafeError):
                c.collect_github(api, cfg, DAY, "2026-10-02")
            get.assert_not_called()

    def test_kst_boundaries_identity_completed_and_private_canary(self):
        api = FakeAPI([commit(), commit("b"*40, "2026-09-30T14:59:59Z"), commit("c"*40, "2026-10-01T15:00:00Z"), commit("d"*40, user={"login": "other"})])
        result = c.collect_github(api, config(), DAY, "2026-10-02")
        row = result["daily"][0]
        self.assertEqual((row["commits"], row["mergedPrs"], row["closedIssues"]), (1, 1, 1))
        self.assertEqual((row["additions"], row["deletions"], row["measuredCommits"]), (8, 3, 1))
        self.assertNotIn(CANARY, json.dumps(result))
        c.validate({"schemaVersion": 1, "timezone": "Asia/Seoul", "codex": None, "github": result})

    def test_merge_count_but_no_merge_lines_and_cross_repo_sha_dedup(self):
        api = FakeAPI([commit(), commit("b"*40, parents=2)])
        cfg = config()
        cfg["repositories"].append("sample/fork")
        result = c.collect_github(api, cfg, DAY, "2026-10-02")
        row = result["daily"][0]
        self.assertEqual((row["commits"], row["measuredCommits"], api.details), (2, 1, 1))

    def test_no_lines_and_repeat_recomputation(self):
        one = c.collect_github(FakeAPI(), config(False), DAY, "2026-10-02")
        two = c.collect_github(FakeAPI(), config(False), DAY, "2026-10-02")
        self.assertEqual(one, two)
        self.assertIsNone(one["daily"][0]["additions"])
        self.assertEqual(one["daily"][0]["measuredCommits"], 0)

    def test_pagination_consumes_all_pages_and_stops_sorted_history(self):
        api = c.GitHub("test-token")
        with patch.object(api, "get", side_effect=[[{"n": i} for i in range(100)], [{"n": 100}]]):
            self.assertEqual(len(list(api.pages("/repos/sample/repo/commits"))), 101)
        cutoff = dt.datetime.fromisoformat("2026-10-01T00:00:00+09:00")
        with patch.object(api, "get", return_value=[{"updated_at": "2026-10-01T00:00:00Z"}, {"updated_at": "2026-09-01T00:00:00Z"}]):
            self.assertEqual(len(list(api.pages("/repos/sample/repo/pulls", stop_before=cutoff))), 1)

    def test_failure_does_not_return_partial_aggregates(self):
        api = FakeAPI()
        with patch.object(api, "get", side_effect=RuntimeError(CANARY)):
            with self.assertRaises(RuntimeError):
                c.collect_github(api, config(), DAY, "2026-10-02")
        with self.assertRaises(c.SafeError):
            c.GitHub("test-token", budget=0).get("/repos/sample/repo")

    def test_complete_dense_coverage_and_strict_github_fields(self):
        data = {"schemaVersion": 1, "timezone": "Asia/Seoul", "codex": None,
                "github": c.collect_github(FakeAPI([]), config(), "2026-10-02", "2026-10-03")}
        c.validate(data)
        data["github"]["daily"][0]["repo"] = CANARY
        with self.assertRaises(c.SafeError):
            c.validate(data)
        del data["github"]["daily"][0]["repo"]
        data["github"]["daily"].pop()
        with self.assertRaises(c.SafeError):
            c.validate(data)



class AutoDiscoveryTests(unittest.TestCase):
    class FakeAuthenticatedAPI(FakeAPI):
        def __init__(self, repositories=None, login="sample-user", commits=None):
            super().__init__(commits)
            self.repos = repositories if repositories is not None else [
                {"full_name": "PrivateCompany/Internal", "private": True},
                {"full_name": "Sample/Open", "private": False},
            ]
            self.login = login
            self.discovery_params = None

        def get(self, path, params=None):
            if path == "/user":
                return {"login": self.login, "email": CANARY}
            return super().get(path, params)

        def pages(self, path, params=None, stop_before=None):
            if path == "/user/repos":
                self.discovery_params = params
                return iter(self.repos)
            return super().pages(path, params, stop_before)

    def test_all_token_visible_public_and_private_repos_are_discovered(self):
        api = self.FakeAuthenticatedAPI()
        config, private_count = c.discover_authenticated_repositories(api, DAY)
        self.assertEqual(config["login"], "sample-user")
        self.assertEqual(config["repositories"],
                         ["PrivateCompany/Internal", "Sample/Open"])
        self.assertEqual(private_count, 1)
        self.assertEqual(config["since"], DAY)
        self.assertFalse(config["withLines"])
        self.assertIn("organization_member", api.discovery_params["affiliation"])
        self.assertEqual(api.discovery_params["visibility"], "all")
        aggregated = c.collect_github(api, config, DAY, "2026-10-02")
        document = json.dumps(aggregated)
        for secret in (CANARY, "PrivateCompany", "Internal", "Sample/Open"):
            self.assertNotIn(secret, document)
        self.assertEqual(aggregated["daily"][0]["commits"], 1)
        self.assertEqual(aggregated["daily"][0]["mergedPrs"], 2)

    def test_wrong_authenticated_identity_stops_before_private_listing(self):
        api = self.FakeAuthenticatedAPI(login="sample-user")
        with patch.object(api, "pages", wraps=api.pages) as list_pages:
            with self.assertRaises(c.SafeError):
                c.discover_authenticated_repositories(
                    api, DAY, expected_login="another-user"
                )
            list_pages.assert_not_called()

    def test_auto_mode_uses_codex_oldest_date_without_any_manual_config(self):
        with tempfile.TemporaryDirectory() as folder:
            public_path = Path(folder) / "data.json"
            base = {"schemaVersion": 1, "timezone": "Asia/Seoul",
                    "codex": c.sanitize_codex(codex()), "github": None}
            c.save_public(base, public_path)
            api = self.FakeAuthenticatedAPI()
            stdout = io.StringIO()
            with patch.object(c, "OUTPUT", public_path), \
                    patch.object(c, "GitHub", return_value=api), \
                    patch.dict(c.os.environ, {"ACTIVITY_READ_TOKEN": "secret"}), \
                    contextlib.redirect_stdout(stdout):
                self.assertEqual(c.main(["github-auto", "--through", DAY]), 0)
            saved = json.loads(public_path.read_text())
            self.assertEqual(saved["github"]["from"], DAY)
            self.assertEqual(saved["github"]["through"], DAY)
            self.assertIn("2 token-accessible repositories (1 private)", stdout.getvalue())
            for secret in (CANARY, "PrivateCompany", "Internal"):
                self.assertNotIn(secret, public_path.read_text())

    def test_auto_mode_without_codex_reference_fails_without_publishing(self):
        with tempfile.TemporaryDirectory() as folder:
            public_path = Path(folder) / "data.json"
            base = {"schemaVersion": 1, "timezone": "Asia/Seoul",
                    "codex": None, "github": None}
            c.save_public(base, public_path)
            original = public_path.read_bytes()
            with patch.object(c, "OUTPUT", public_path), \
                    patch.dict(c.os.environ, {"ACTIVITY_READ_TOKEN": "secret"}), \
                    contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(c.main(["github-auto", "--through", DAY]), 1)
            self.assertEqual(public_path.read_bytes(), original)

    def test_invalid_or_duplicate_discovery_fails_closed(self):
        cases = [
            self.FakeAuthenticatedAPI(login="wrong user"),
            self.FakeAuthenticatedAPI(repositories=[]),
            self.FakeAuthenticatedAPI(repositories=[
                {"full_name": "Sample/A", "private": True},
                {"full_name": "sample/a", "private": False}]),
            self.FakeAuthenticatedAPI(repositories=[
                {"full_name": "Sample/A", "private": "yes"}]),
        ]
        for api in cases:
            with self.subTest(api=api):
                with self.assertRaises(c.SafeError):
                    c.discover_authenticated_repositories(api, DAY)

    def test_automatic_publisher_commit_is_not_counted(self):
        auto_commit = commit()
        auto_commit["commit"]["message"] = "Update safe AI development activity aggregates"
        result = c.collect_github(
            FakeAPI([auto_commit]),
            config(False),
            DAY,
            "2026-10-02",
        )
        self.assertEqual(result["daily"][0]["commits"], 0)

    def test_empty_repository_still_allows_issue_and_pr_count(self):
        class EmptyFake(FakeAPI):
            def get(self, path, params=None):
                return {"default_branch": None}
        result = c.collect_github(EmptyFake(), config(False), DAY, "2026-10-02")
        self.assertEqual(result["daily"][0]["commits"], 0)
        self.assertEqual(result["daily"][0]["closedIssues"], 1)


if __name__ == "__main__":
    unittest.main()
