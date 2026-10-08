#!/usr/bin/env python3
"""Mechanical checks for the project-conventions skill. Exit 1 on any FAIL.

  python3 tools/check_conventions.py            # building: placeholders are WARN
  python3 tools/check_conventions.py --strict   # before production: placeholders are FAIL

Checks:
  1. No secret-looking file or value in anything git would commit.
  2. data/site.json and data/pages.json parse; TODO placeholders are listed.
  3. Business facts (phone, email, booking URL, prices) are not hard-coded in site/src;
     they are read from data/site.json.
  4. Nothing that only works inside the Stitch preview ships: Tailwind CDN script,
     hot-linked Stitch images, fictional 555 phone numbers.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import PAGES_JSON, REPO, SITE_DIR, SITE_JSON, Row, is_todo, load_json, print_table, some, walk_strings

STRICT = "--strict" in sys.argv
TEXT_EXT = {".py", ".js", ".mjs", ".ts", ".astro", ".json", ".yaml", ".yml", ".toml", ".sh", ".html", ".css", ".md", ".txt"}
SRC_EXT = {".astro", ".html", ".js", ".mjs", ".ts", ".css", ".md", ".mdx"}
SKIP_DIRS = {".git", "node_modules", "dist", ".astro", "__pycache__", ".netlify"}

SECRET_FILE = re.compile(r"(^|/)(\.env(\..+)?|credentials\.json|token\.json|service-account[^/]*\.json|[^/]+\.(pem|key))$")
SECRET_VALUE = [
    (re.compile(r"sk_[A-Za-z0-9]{20,}"), "secret key (sk_...)"),
    (re.compile(r"AC[0-9a-f]{32}"), "Twilio account SID"),
    (re.compile(r"AIza[0-9A-Za-z_-]{35}"), "Google API key"),
    (re.compile(r"ya29\.[0-9A-Za-z_-]{30,}"), "Google OAuth access token"),
    (re.compile(r"nfp_[A-Za-z0-9]{30,}"), "Netlify personal access token"),
    (re.compile(r"-----BEGIN (RSA |EC )?PRIVATE KEY-----"), "private key"),
    (re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[=:]\s*[\"']?(?!change-me|test-key|\$|<|\{|xxx|your)[A-Za-z0-9_\-]{24,}"),
     "long literal assigned to a secret-named variable"),
]
PREVIEW_ONLY = [
    (re.compile(r"cdn\.tailwindcss\.com"), "Tailwind CDN script (compile Tailwind at build time instead)"),
    (re.compile(r"lh3\.googleusercontent\.com/aida"), "hot-linked Stitch image (download it into site/src/assets)"),
    (re.compile(r"\(?\d{3}\)?[ .-]?555[ .-]?01\d{2}"), "fictional 555 phone number from the design"),
]
PHONE = re.compile(r"(?<![\w.#-])(?:\+1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\d)")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PRICE = re.compile(r"\$(\d{1,3}(?:,\d{3})+|\d{3,})")


def numbers_in(node) -> set:
    """Every number >= 100 in the facts file: the prices a template must not retype."""
    if isinstance(node, dict):
        return set().union(*[numbers_in(v) for v in node.values()]) if node else set()
    if isinstance(node, list):
        return set().union(*[numbers_in(v) for v in node]) if node else set()
    return {int(node)} if isinstance(node, (int, float)) and not isinstance(node, bool) and node >= 100 else set()


def git_files() -> List[str]:
    try:
        out = ""
        for args in (["git", "ls-files"], ["git", "ls-files", "--others", "--exclude-standard"]):
            out += subprocess.run(args, cwd=REPO, capture_output=True, text=True, check=True).stdout
        return [f for f in out.split("\n") if f]
    except Exception:
        return []


def src_files() -> List[Path]:
    found = []
    src = SITE_DIR / "src"
    if not src.exists():
        return found
    for dirpath, dirnames, filenames in os.walk(src):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        found += [Path(dirpath) / f for f in filenames if Path(f).suffix in SRC_EXT]
    return found


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def main() -> int:
    rows: List[Row] = []

    # 1. secrets ---------------------------------------------------------------
    candidates = git_files()
    bad = [f for f in candidates if SECRET_FILE.search(f) and not f.endswith(".env.example")]
    rows.append(("secrets: no secret file would be committed", "FAIL" if bad else "PASS", some(bad) or f"{len(candidates)} committable files"))
    hits = []
    for f in candidates:
        p = REPO / f
        if not p.is_file() or p.suffix not in TEXT_EXT or f.startswith("design/") or f == "tools/check_conventions.py":
            continue
        text = p.read_text(errors="ignore")
        for rx, what in SECRET_VALUE:
            m = rx.search(text)
            if m:
                hits.append(f"{f}:{line_of(text, m.start())} {what}")
                break
    rows.append(("secrets: no secret-looking value in files", "FAIL" if hits else "PASS", some(hits, 3) or "clean"))

    # 2. facts files --------------------------------------------------------------
    site = None
    for path in (SITE_JSON, PAGES_JSON):
        rel = str(path.relative_to(REPO))
        try:
            data = load_json(path)
        except Exception as e:
            rows.append((f"facts: {rel} parses", "FAIL", str(e)[:90]))
            continue
        if path == SITE_JSON:
            site = data
        todos = [k for k, v in walk_strings(data) if is_todo(v)]
        status = "PASS" if not todos else ("FAIL" if STRICT else "WARN")
        rows.append((f"facts: {rel} has no TODO placeholder", status, some(todos, 5) or "none"))

    # 3 + 4. the site source ----------------------------------------------------------
    files = src_files()
    if not files:
        rows.append(("site/src: facts come from data/site.json", "SKIP", "site/src does not exist yet"))
        rows.append(("site/src: nothing preview-only ships", "SKIP", "site/src does not exist yet"))
    else:
        known, prices = set(), set()
        if site:
            known = {v for _, v in walk_strings(site) if not is_todo(v)}
            prices = numbers_in(site)
        hard, preview = [], []
        for p in files:
            rel = str(p.relative_to(REPO))
            text = p.read_text(errors="ignore")
            for rx, what in PREVIEW_ONLY:
                m = rx.search(text)
                if m:
                    preview.append(f"{rel}:{line_of(text, m.start())} {what}")
            legal = "legal" in rel or "privacy" in rel or "terms" in rel  # legal prose may name contact details
            for rx, what in ((PHONE, "phone"), (EMAIL, "email")):
                m = None if legal else rx.search(text)
                if m:
                    hard.append(f"{rel}:{line_of(text, m.start())} {what} {m.group(0)}")
            # a price is a fact only when it is one we sell at; "$1,500 repair job" in copy is not
            for m in PRICE.finditer(text):
                if int(m.group(1).replace(",", "")) in prices:
                    hard.append(f"{rel}:{line_of(text, m.start())} price {m.group(0)}")
                    break
            booking = (site or {}).get("booking", {}).get("url", "")
            for value in ([booking] if booking.startswith("http") else []) + ["calendly.com/", "calendar.app.google/", "calendar.google.com/calendar/appointments"]:
                if value in text:
                    hard.append(f"{rel}:{line_of(text, text.index(value))} booking URL")
                    break
        rows.append(("site/src: facts come from data/site.json", "FAIL" if hard else "PASS", some(hard, 4) or f"{len(files)} files, no hard-coded phone, email, price or booking URL"))
        rows.append(("site/src: nothing preview-only ships", "FAIL" if preview else "PASS", some(preview, 4) or "no Tailwind CDN, hot-linked Stitch image or 555 number"))

    return print_table(f"project-conventions check{' (strict)' if STRICT else ''} — {REPO}", rows)


if __name__ == "__main__":
    sys.exit(main())
