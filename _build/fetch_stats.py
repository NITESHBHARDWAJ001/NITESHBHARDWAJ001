"""Fetches live numbers from GitHub and draws assets/github-live.svg.

Runs inside the GitHub Action in .github/workflows/update-stats.yml, once a day.
With a token (the Action provides GITHUB_TOKEN) commits and pull requests come from the GraphQL
contributions API, summed year by year since the account was created. Without a token it falls
back to the public search API (public commits only), so it also works on your own machine.

    python _build/fetch_stats.py
"""
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_assets as ba  # noqa: E402

USER = os.environ.get("PROFILE_USER", "NITESHBHARDWAJ001")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
API = "https://api.github.com"


def call(url, body=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-stats", "X-GitHub-Api-Version": "2022-11-28"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def safe(fn, default=None):
    try:
        return fn()
    except (urllib.error.URLError, KeyError, ValueError, TypeError) as ex:
        print("warning:", ex)
        return default


def profile():
    u = call(f"{API}/users/{USER}")
    langs, page = set(), 1
    while True:
        repos = call(f"{API}/users/{USER}/repos?per_page=100&type=owner&page={page}")
        langs |= {r["language"] for r in repos if r.get("language")}
        if len(repos) < 100:
            break
        page += 1
    return u, len(langs)


def graphql_totals(created_iso):
    """Commits and pull requests across every year since the account was created."""
    q = """query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){contributionsCollection(from:$from,to:$to){
        totalCommitContributions restrictedContributionsCount totalPullRequestContributions}}}"""
    start = dt.datetime.fromisoformat(created_iso.replace("Z", "+00:00"))
    now = dt.datetime.now(dt.timezone.utc)
    commits = prs = 0
    cur = start
    while cur < now:
        nxt = min(cur + dt.timedelta(days=364), now)
        res = call(f"{API}/graphql", {"query": q, "variables": {"login": USER, "from": cur.isoformat(), "to": nxt.isoformat()}})
        c = res["data"]["user"]["contributionsCollection"]
        commits += c["totalCommitContributions"] + c["restrictedContributionsCount"]
        prs += c["totalPullRequestContributions"]
        cur = nxt + dt.timedelta(seconds=1)
    return commits, prs


def search_totals():
    commits = call(f"{API}/search/commits?q=author:{USER}&per_page=1")["total_count"]
    prs = call(f"{API}/search/issues?q=author:{USER}+type:pr&per_page=1")["total_count"]
    return commits, prs


def fmt(n):
    return "—" if n is None else f"{n:,}"


def draw(values):
    W, H = 1280, 190
    cells = [
        ("COMMITS", values["commits"], ba.CYAN),
        ("PULL REQUESTS", values["prs"], ba.CORAL),
        ("PUBLIC REPOS", values["repos"], ba.GOLD),
        ("LANGUAGES USED", values["langs"], ba.VIOLET),
        ("FOLLOWERS", values["followers"], ba.MINT),
    ]
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%d %b %Y").upper()
    body = f"""
<circle cx="52" cy="40" r="6" fill="{ba.MINT}"><animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/></circle>
<text x="70" y="45" font-family="{ba.M}" font-size="13" letter-spacing="3" fill="{ba.MINT}">LIVE FROM GITHUB</text>
<text x="{W - 40}" y="45" text-anchor="end" font-family="{ba.M}" font-size="12" letter-spacing="1.6" fill="{ba.MUTED}">@{ba.e(USER)}  ·  UPDATED {stamp}</text>
{ba.dash(40, 64, W - 40, 64, ba.LINE, 1.2, 3)}
"""
    cw = (W - 80) / len(cells)
    for i, (label, val, col) in enumerate(cells):
        x = 40 + i * cw
        if i:
            body += f'<line x1="{x}" y1="86" x2="{x}" y2="{H - 28}" stroke="{ba.LINE}" stroke-dasharray="4 5"/>'
        body += f'<text x="{x + 28}" y="136" font-family="{ba.D}" font-size="56" font-weight="800" fill="{col}" letter-spacing="-2" filter="url(#soft)">{fmt(val)}</text>'
        body += f'<text x="{x + 30}" y="164" font-family="{ba.M}" font-size="12.5" letter-spacing="1.6" fill="{ba.MUTED}">{label}</text>'
    ba.save("github-live.svg", W, H, body)


def main():
    user, langs = safe(profile, (None, None)) or (None, None)
    values = {"commits": None, "prs": None, "repos": None, "langs": langs, "followers": None}
    if user:
        values["repos"] = user["public_repos"]
        values["followers"] = user["followers"]
    totals = None
    if TOKEN and user:
        totals = safe(lambda: graphql_totals(user["created_at"]))
    if totals is None:
        totals = safe(search_totals, (None, None))
    values["commits"], values["prs"] = totals
    print(values)
    draw(values)


if __name__ == "__main__":
    main()
