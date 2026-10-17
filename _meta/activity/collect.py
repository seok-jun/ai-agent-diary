"""Publish only validated numeric aggregates. Python 3.10+, standard library only."""
import argparse
from contextlib import contextmanager
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "docs/assets/activity/data.json"
KST = dt.timezone(dt.timedelta(hours=9))
SUMMARY = ("lifetimeTokens", "peakDailyTokens", "longestRunningTurnSec",
           "currentStreakDays", "longestStreakDays")
COUNTS = ("commits", "mergedPrs", "closedIssues", "measuredCommits")
MAX_INT = 9007199254740991  # JavaScript safe integer


class SafeError(Exception):
    """Never attach source data, URLs, paths, or upstream errors."""


def require(condition):
    if not condition:
        raise SafeError()


def keys(obj, expected):
    require(type(obj) is dict and set(obj) == set(expected))


def number(value):
    require(type(value) is int and 0 <= value <= MAX_INT)
    return value


def date(value):
    require(type(value) is str and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value))
    try:
        parsed = dt.date.fromisoformat(value)
    except ValueError:
        raise SafeError() from None
    require(dt.date(2020, 1, 1) <= parsed <= dt.datetime.now(KST).date())
    return value


def timestamp(value):
    require(type(value) is str)
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        require(parsed.tzinfo is not None)
        return parsed.astimezone(KST)
    except (ValueError, TypeError):
        raise SafeError() from None


def decode(text):
    # Reject duplicate object keys and non-standard NaN/Infinity.
    def unique(pairs):
        result = {}
        for k, v in pairs:
            require(k not in result)
            result[k] = v
        return result
    try:
        return json.loads(text.lstrip("\ufeff"), object_pairs_hook=unique,
                          parse_constant=lambda _: require(False))
    except (ValueError, TypeError):
        raise SafeError() from None


def sanitize_codex(raw):
    require(type(raw) is dict and type(raw.get("contractVersion")) is int
            and raw["contractVersion"] == 1)
    as_of = date(timestamp(raw.get("capturedAt")).date().isoformat())
    source = raw.get("summary")
    require(type(source) is dict)
    summary = {k: number(source.get(k)) for k in SUMMARY}
    require(summary["currentStreakDays"] <= summary["longestStreakDays"])
    buckets = raw.get("dailyUsageBuckets")
    require(type(buckets) is list and len(buckets) <= 10000)
    daily, seen = [], set()
    for row in buckets:
        require(type(row) is dict)
        day = date(row.get("startDate"))
        require(day <= as_of and day not in seen)
        seen.add(day)
        daily.append({"date": day, "tokens": number(row.get("tokens"))})
    daily.sort(key=lambda x: x["date"])
    require(sum(x["tokens"] for x in daily) == summary["lifetimeTokens"])
    require(max((x["tokens"] for x in daily), default=0) == summary["peakDailyTokens"])
    return {"asOf": as_of, "summary": summary, "daily": daily}


def validate(data):
    keys(data, ("schemaVersion", "timezone", "codex", "github"))
    require(type(data["schemaVersion"]) is int and data["schemaVersion"] == 1
            and data["timezone"] == "Asia/Seoul")
    codex = data["codex"]
    if codex is not None:
        keys(codex, ("asOf", "summary", "daily"))
        keys(codex["summary"], SUMMARY)
        require(type(codex["daily"]) is list)
        for row in codex["daily"]:
            keys(row, ("date", "tokens"))
        sanitized = sanitize_codex({"contractVersion": 1,
            "capturedAt": date(codex["asOf"]) + "T00:00:00+09:00",
            "summary": codex["summary"],
            "dailyUsageBuckets": [{"startDate": r["date"], "tokens": r["tokens"]}
                                  for r in codex["daily"]]})
        require(sanitized == codex)
    github = data["github"]
    if github is not None:
        keys(github, ("asOf", "from", "through", "daily"))
        require(date(github["from"]) <= date(github["through"]) <= date(github["asOf"]))
        require(type(github["daily"]) is list)
        expected = days(github["from"], github["through"])
        require(len(github["daily"]) == len(expected))
        for day, row in zip(expected, github["daily"]):
            keys(row, ("date", *COUNTS, "additions", "deletions"))
            require(row["date"] == day)
            for field in COUNTS:
                number(row[field])
            require(row["measuredCommits"] <= row["commits"])
            require((row["additions"] is None) == (row["deletions"] is None))
            if row["additions"] is None:
                require(row["measuredCommits"] == 0)
            else:
                number(row["additions"])
                number(row["deletions"])
    return data


def days(start, end):
    first, last = dt.date.fromisoformat(date(start)), dt.date.fromisoformat(date(end))
    require(0 <= (last - first).days <= 3660)
    return [(first + dt.timedelta(days=i)).isoformat() for i in range((last-first).days+1)]


def load_public(path=None):
    path = OUTPUT if path is None else path
    if not path.exists():
        return {"schemaVersion": 1, "timezone": "Asia/Seoul", "codex": None, "github": None}
    return validate(decode(path.read_text(encoding="utf-8")))


def save_public(data, path=None):
    path = OUTPUT if path is None else path
    validate(data)  # Validate the entire document, including previously stored data.
    content = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                         dir=path.parent, delete=False) as stream:
            temp = Path(stream.name)
            stream.write(content)
        os.replace(temp, path)
    finally:
        if temp and temp.exists():
            temp.unlink()
    return True


def private_file(value):
    path = Path(value).expanduser().resolve()
    # Raw inputs and repo lists must live outside this public checkout.
    require(not path.is_relative_to(ROOT))
    return path


class GitHub:
    def __init__(self, token, budget=1000):
        require(type(token) is str and len(token) > 0)
        self.token, self.budget = token, budget

    def get(self, path, params=None):
        require(self.budget > 0 and (path.startswith("/repos/") or path in ("/user", "/user/repos")))
        self.budget -= 1
        url = "https://api.github.com" + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        request = urllib.request.Request(url, headers={
            "Authorization": "Bearer " + self.token,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "numeric-activity-collector"})
        # A redirect could send credentials elsewhere; API endpoints should not redirect.
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args):
                raise SafeError()
        try:
            with urllib.request.build_opener(NoRedirect).open(request, timeout=30) as response:
                return decode(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            # GitHub returns 409 for commits on an uninitialized repository.
            if error.code == 409 and path.endswith("/commits"):
                return []
            raise SafeError() from None
        except (urllib.error.URLError, OSError, UnicodeError):
            raise SafeError() from None

    def pages(self, path, params=None, stop_before=None):
        for page in range(1, 1001):
            rows = self.get(path, {**(params or {}), "per_page": 100, "page": page})
            require(type(rows) is list)
            for row in rows:
                require(type(row) is dict)
                # Only used with GitHub's descending updated_at order.
                if stop_before and timestamp(row.get("updated_at")) < stop_before:
                    return
                yield row
            if len(rows) < 100:
                return
        raise SafeError()


def discover_authenticated_repositories(api, since, with_lines=False):
    """Only token-visible GitHub repositories; never serialize their identities."""
    identity = api.get("/user")
    require(type(identity) is dict)
    login = identity.get("login")
    require(type(login) is str and re.fullmatch(r"[A-Za-z0-9-]{1,39}", login))

    # GET /user/repos is permission-scoped for fine-grained PATs and includes
    # owner, collaborator and organization-member repositories. Fetch ALL pages.
    found = {}
    for row in api.pages("/user/repos", {
        "affiliation": "owner,collaborator,organization_member",
        "visibility": "all",
        "sort": "full_name",
        "direction": "asc",
    }):
        require(type(row) is dict)
        name = row.get("full_name")
        private = row.get("private")
        require(type(name) is str and re.fullmatch(
            r"[A-Za-z0-9-]+/[A-Za-z0-9_.-]+", name))
        require(type(private) is bool)
        key = name.casefold()
        require(key not in found)
        found[key] = (name, private)

    require(1 <= len(found) <= 1000)
    config = {
        "login": login,
        "repositories": sorted((value[0] for value in found.values()),
                               key=str.casefold),
        "since": date(since),
        "withLines": with_lines,
    }
    parse_config(config)
    return config, sum(private for _, private in found.values())


def parse_config(raw):
    keys(raw, ("login", "repositories", "since", "withLines"))
    require(type(raw["login"]) is str and re.fullmatch(r"[A-Za-z0-9-]{1,39}", raw["login"]))
    repos = raw["repositories"]
    require(type(repos) is list and 1 <= len(repos) <= 1000)
    for repo in repos:
        require(type(repo) is str and re.fullmatch(r"[A-Za-z0-9-]+/[A-Za-z0-9_.-]+", repo))
        require(repo.split("/")[1] not in (".", ".."))
    require(len({repo.casefold() for repo in repos}) == len(repos))
    date(raw["since"])
    require(type(raw["withLines"]) is bool)
    return raw


def collect_github(api, config, through, as_of=None):
    config = parse_config(config)
    start = dt.datetime.fromisoformat(config["since"] + "T00:00:00+09:00")
    end = dt.datetime.fromisoformat(date(through) + "T00:00:00+09:00") + dt.timedelta(days=1)
    require(end.date() <= dt.datetime.now(KST).date())  # Completed KST days only.
    rows = {day: {"date": day, "commits": 0, "mergedPrs": 0, "closedIssues": 0,
                  "measuredCommits": 0, "additions": 0 if config["withLines"] else None,
                  "deletions": 0 if config["withLines"] else None}
            for day in days(config["since"], through)}
    login = config["login"].lower()

    def mine(user):
        return type(user) is dict and str(user.get("login", "")).lower() == login

    def bucket(value):
        stamp = timestamp(value)
        return rows.get(stamp.date().isoformat()) if start <= stamp < end else None

    # Deduplicate commits across selected forks, in memory only; never publish SHAs.
    seen = set()
    for repo in config["repositories"]:
        base = "/repos/" + repo
        # Fail on inaccessible or empty repos rather than silently publishing partial counts.
        meta = api.get(base)
        require(type(meta) is dict)
        default_branch = meta.get("default_branch")
        require(default_branch is None or (type(default_branch) is str and default_branch))
        commits = (api.pages(base + "/commits", {"author": config["login"],
            "sha": default_branch, "since": start.isoformat(),
            "until": (end - dt.timedelta(seconds=1)).isoformat()})
                   if default_branch else ())
        for commit in commits:
            if not mine(commit.get("author")):
                continue
            # The dashboard publisher commits with the user PAT. Exclude this
            # bookkeeping commit so it does not inflate development activity.
            if commit.get("commit", {}).get("message", "").splitlines()[0:1] == [
                    "Update safe AI development activity aggregates"] :
                continue
            row = bucket(commit["commit"]["committer"]["date"])
            sha = commit.get("sha")
            require(type(sha) is str and re.fullmatch(r"[0-9a-f]{40,64}", sha))
            if row is None or sha in seen:
                continue
            seen.add(sha)
            row["commits"] += 1
            if config["withLines"] and len(commit.get("parents", [])) <= 1:
                detail = api.get(base + "/commits/" + sha)
                row["additions"] += number(detail["stats"]["additions"])
                row["deletions"] += number(detail["stats"]["deletions"])
                row["measuredCommits"] += 1
        for pr in api.pages(base + "/pulls", {"state": "closed", "sort": "updated",
                                               "direction": "desc"}, stop_before=start):
            if mine(pr.get("user")) and pr.get("merged_at"):
                row = bucket(pr["merged_at"])
                if row is not None:
                    row["mergedPrs"] += 1
        for issue in api.pages(base + "/issues", {"state": "closed", "since": start.isoformat()}):
            if "pull_request" not in issue and mine(issue.get("user")) and issue.get("state_reason") == "completed":
                row = bucket(issue.get("closed_at"))
                if row is not None:
                    row["closedIssues"] += 1
    # Recompute the whole configured period; no scope hashes, identities or event cache.
    return {"asOf": date(as_of or dt.datetime.now(KST).date().isoformat()),
            "from": config["since"], "through": through, "daily": list(rows.values())}


def parser():
    class PrivateParser(argparse.ArgumentParser):
        def error(self, message):
            raise SafeError()
    result = PrivateParser(description="Publish numeric activity aggregates only.")
    commands = result.add_subparsers(dest="command", required=True)
    codex = commands.add_parser("codex")
    source = codex.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", help="Private JSON file outside checkout")
    source.add_argument("--analyzer", help="Already installed, trusted executable path")
    auto = commands.add_parser("github-auto",
                               help="Automatically collect every token-accessible repository")
    auto.add_argument("--through",
                      default=(dt.datetime.now(KST).date()-dt.timedelta(days=1)).isoformat())
    github = commands.add_parser("github")
    github.add_argument("--config", help="Private config file outside checkout; otherwise ACTIVITY_CONFIG_JSON")
    github.add_argument("--through", default=(dt.datetime.now(KST).date()-dt.timedelta(days=1)).isoformat())
    commands.add_parser("validate")
    return result


@contextmanager
def lock_output():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    lock = OUTPUT.parent / ".collect.lock"
    handle = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        os.close(handle)
        yield
    finally:
        lock.unlink()


def run(args):
    with lock_output():
        return update(args)


def update(args):
    data = load_public()
    if args.command == "codex":
        if args.input:
            raw = private_file(args.input).read_text(encoding="utf-8-sig")
        else:
            require(Path(args.analyzer).is_absolute() and Path(args.analyzer).is_file())
            process = subprocess.run([args.analyzer, "--json"], capture_output=True,
                                     timeout=300, check=False)
            require(process.returncode == 0)
            raw = process.stdout.decode("utf-8-sig")
        data["codex"] = sanitize_codex(decode(raw))
    elif args.command == "github-auto":
        # Align GitHub daily stats to the oldest *live* Codex activity bucket.
        # No username, repository list or start date is requested from the user.
        codex = data.get("codex")
        require(type(codex) is dict and len(codex.get("daily", [])) > 0)
        since = codex["daily"][0]["date"]
        api = GitHub(os.environ.get("ACTIVITY_READ_TOKEN"))
        config, private_count = discover_authenticated_repositories(api, since)
        data["github"] = collect_github(api, config, args.through)
        print("GitHub collected from %d token-accessible repositories (%d private)."
              % (len(config["repositories"]), private_count))
    elif args.command == "github":
        raw = (private_file(args.config).read_text(encoding="utf-8-sig")
               if args.config else os.environ.get("ACTIVITY_CONFIG_JSON", ""))
        data["github"] = collect_github(GitHub(os.environ.get("ACTIVITY_READ_TOKEN")),
                                          decode(raw), args.through)
    else:
        print("Public activity data is valid.")
        return 0
    changed = save_public(data)
    print("Safe aggregate updated." if changed else "Safe aggregate unchanged.")
    return 0


def main(argv=None):
    # Do not echo argparse input on errors; config may contain a private path.
    try:
        return run(parser().parse_args(argv))
    except (Exception, KeyboardInterrupt):
        # Intentionally suppress traceback, stderr, response bodies and file paths.
        print("Activity collection failed; existing public data preserved. Check private configuration, input contract and read permissions.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
