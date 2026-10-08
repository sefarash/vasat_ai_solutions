#!/usr/bin/env python3
"""Deploy gates for the website. Runs the checks that must pass before (pre) and after (post) a deploy.
It never deploys anything itself; the deploy skill says how a deploy happens.

  python3 tools/deploy_gate.py pre                     # conventions, page plan, build, SEO audit, clean tree
  python3 tools/deploy_gate.py post <url>              # fetch every planned page from a deploy preview or production
  python3 tools/deploy_gate.py log <url> "<note>"      # append a line to docs/DEPLOY-LOG.md

pre audits site/dist when site/package.json exists, otherwise the legacy static site in the repo root.
Exit 0 = GO, 1 = NO-GO.
"""
from __future__ import annotations

import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import PAGES_JSON, REPO, SITE_DIR, SITE_JSON, Row, is_todo, load_json

rows: List[Row] = []
UA = {"User-Agent": "vasat-deploy-gate/1.0"}


def run(name: str, cmd: List[str], cwd: Path = REPO, required: bool = True) -> bool:
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=900)
    except FileNotFoundError as e:
        rows.append((name, "FAIL", f"cannot run: {e}")); return False
    except subprocess.TimeoutExpired:
        rows.append((name, "FAIL", "timed out")); return False
    ok = r.returncode == 0
    last = ([l for l in (r.stdout + r.stderr).splitlines() if l.strip()] or ["(no output)"])[-1].strip()
    rows.append((name, "PASS" if ok else ("FAIL" if required else "WARN"), last[:110]))
    return ok or not required


def fetch(url: str, tries: int = 3) -> Tuple[int, str]:
    """GET a URL. Status 0 means the request never completed; network errors are retried."""
    err = ""
    for _ in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
                return r.status, r.read(600_000).decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            return e.code, ""
        except Exception as e:
            err = str(e)
    return 0, err


def pre() -> bool:
    ok = True
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    rows.append(("git: working tree is clean and committed", "FAIL" if dirty else "PASS", f"{len(dirty.splitlines())} uncommitted path(s)" if dirty else "clean"))
    ok &= not dirty
    ok &= run("conventions (strict: no placeholder, no secret)", [sys.executable, "tools/check_conventions.py", "--strict"])
    ok &= run("page plan (strict: no TODO)", [sys.executable, "tools/page_plan.py", "validate", "--strict"])
    if (SITE_DIR / "package.json").exists():
        ok &= run("site: build", ["npm", "run", "build", "--silent"], cwd=SITE_DIR)
        ok &= run("site: SEO audit on site/dist", [sys.executable, "tools/seo_check.py"])
    else:
        rows.append(("site: build", "SKIP", "no site/package.json yet; auditing the legacy static site in the repo root"))
        ok &= run("legacy site: SEO audit on repo root", [sys.executable, "tools/seo_check.py", "--dir", "."])
    return ok


def post(base: str) -> bool:
    base = base.rstrip("/")
    ok = True
    site = load_json(SITE_JSON)
    plan = load_json(PAGES_JSON)["pages"]
    production = base == str(site["business"].get("url", "")).rstrip("/")
    home_html = ""
    bad_status, bad_title, bad_index = [], [], []
    for p in plan:
        status, body = fetch(base + p["route"])
        if status != 200:
            bad_status.append(f"{p['route']} ({status or body[:40]})"); continue
        if p["route"] == "/":
            home_html = body
        m = re.search(r"(?is)<title[^>]*>(.*?)</title>", body)
        got = " ".join((m.group(1) if m else "").split()).replace("&amp;", "&")
        if not is_todo(p.get("title")) and got != p.get("title"):
            bad_title.append(p["route"])
        has_noindex = bool(re.search(r'(?i)<meta[^>]+name=["\']robots["\'][^>]+noindex', body))
        if has_noindex == bool(p.get("index")):
            bad_index.append(f"{p['route']} ({'noindex' if has_noindex else 'indexable'})")

    def add(name: str, bad: List[str], detail: str = "", warn: bool = False) -> bool:
        rows.append((name, ("WARN" if warn else "FAIL") if bad else "PASS", ", ".join(bad[:6]) or detail))
        return warn or not bad

    ok &= add("every planned page returns 200", bad_status, f"{len(plan)} pages")
    ok &= add("live <title> matches the plan", bad_title, "match")
    # a preview that is indexable is fine (Netlify adds X-Robots-Tag on previews); production must match exactly
    ok &= add("index / noindex matches the plan", bad_index, "match", warn=not production)
    booking = site.get("booking", {}).get("url", "")
    booking = "" if is_todo(booking) else booking
    ok &= add("home links to the booking URL", [] if booking and booking in home_html else [f"{booking or '(no booking url)'} not found on /"])
    ok &= add("home has none of the Stitch preview leftovers",
              [w for w, rx in (("Tailwind CDN", r"cdn\.tailwindcss\.com"), ("hot-linked Stitch image", r"lh3\.googleusercontent\.com"), ("555 phone number", r"555[ .-]?01\d\d")) if re.search(rx, home_html)], "clean")
    status, robots = fetch(base + "/robots.txt")
    ok &= add("robots.txt is served with a Sitemap: line", [] if status == 200 and re.search(r"(?im)^sitemap:", robots) else [f"status {status}"])
    sm = re.search(r"(?im)^sitemap:\s*(\S+)", robots)
    if sm:
        s_status, _ = fetch(sm.group(1))
        ok &= add("the sitemap URL in robots.txt is served", [] if s_status == 200 else [f"{sm.group(1)} -> {s_status}"], warn=not production)
    status, _ = fetch(base + "/this-page-should-not-exist-" + datetime.now().strftime("%H%M%S"))
    ok &= add("an unknown URL returns 404, not the home page", [] if status == 404 else [f"got {status}: a catch-all rewrite is masking 404s"])
    return ok


def log(url: str, note: str) -> int:
    f = REPO / "docs" / "DEPLOY-LOG.md"
    f.parent.mkdir(exist_ok=True)
    if not f.exists():
        f.write_text("# Deploy log\n\n| When (UTC) | Commit | URL | Note |\n|---|---|---|---|\n")
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip() or "?"
    f.write_text(f.read_text() + f"| {datetime.now(timezone.utc):%Y-%m-%d %H:%M} | {commit} | {url} | {note} |\n")
    print(f"logged to {f.relative_to(REPO)}")
    return 0


def main() -> int:
    a = sys.argv[1:]
    if not a or a[0] not in ("pre", "post", "log") or (a[0] != "pre" and len(a) < 2):
        print(__doc__); return 2
    if a[0] == "log":
        return log(a[1], " ".join(a[2:]))
    ok = pre() if a[0] == "pre" else post(a[1])
    width = max(len(r[0]) for r in rows)
    print(f"\ndeploy gate — {' '.join(a[:2])}\n")
    for name, status, detail in rows:
        print(f"  {name.ljust(width)}  {status:4}  {detail}")
    count = lambda *s: sum(1 for r in rows if r[1] in s)
    print(f"\n{'GO' if ok else 'NO-GO'}: {count('PASS')} pass, {count('FAIL')} fail, {count('WARN', 'SKIP')} warn/skip")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
