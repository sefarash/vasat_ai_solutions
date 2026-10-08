#!/usr/bin/env python3
"""SEO and ship-readiness audit over built static HTML. Prints a PASS/FAIL table; exit 1 on any FAIL.

  python3 tools/seo_check.py                      # audits site/dist against data/pages.json
  python3 tools/seo_check.py --dir .              # audits the legacy static site in the repo root
  python3 tools/seo_check.py --dir <path> --no-plan --base https://example.com
  python3 tools/seo_check.py --json out.json      # also write the rows as JSON

It reads the built output, so it sees exactly what a crawler sees. Fix failures in the
source (site/src, data/*.json), never in dist. Exit 2 if the directory has no HTML.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, Set
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import DIST_DIR, PAGES_JSON, REPO, SITE_JSON, Row, is_todo, load_json, print_table, some

TITLE_MAX, META_MAX, MIN_WORDS = 60, 155, 150
ALWAYS_SKIP = {".git", "node_modules", ".claude", ".astro", ".netlify"}
ROOT_SKIP = {"design", "site", "docs", "tools", "data", "workflows", ".tmp"}  # only when auditing the repo root itself
HOME_TYPES = {"Organization", "LocalBusiness", "ProfessionalService", "MarketingAgency"}
VOID_TEXT = {"script", "style", "noscript", "template", "svg"}
CHROME = {"nav", "header", "footer"}


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""; self.meta = ""; self.robots = ""; self.canonical = ""
        self.h1: List[str] = []; self.links: List[str] = []; self.ids: Set[str] = set()
        self.img_no_alt: List[str] = []; self.srcs: List[str] = []; self.jsonld: List[str] = []
        self.words = 0; self.lang = ""; self.viewport = False; self.og: Set[str] = set(); self.tel: List[str] = []
        self._stack: List[str] = []; self._buf: Optional[List[str]] = None; self._kind = ""

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang", "")
        elif tag == "meta":
            name = (a.get("name") or a.get("property") or "").lower()
            if name == "description": self.meta = a.get("content", "").strip()
            elif name == "robots": self.robots = a.get("content", "").lower()
            elif name == "viewport": self.viewport = True
            elif name.startswith("og:"): self.og.add(name)
        elif tag == "link":
            if a.get("rel", "").lower() == "canonical": self.canonical = a.get("href", "")
            if a.get("href"): self.srcs.append(a["href"])
        elif tag == "a" and "href" in a:
            self.links.append(a["href"])
            if a["href"].startswith("tel:"): self.tel.append(a["href"][4:])
        elif tag == "img":
            if "alt" not in a: self.img_no_alt.append(a.get("src", "")[:60])
            if a.get("src"): self.srcs.append(a["src"])
        elif tag in ("script", "source", "iframe", "video") and a.get("src"):
            self.srcs.append(a["src"])
        if tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._buf, self._kind = [], "jsonld"
        elif tag == "title" and not self.title:
            self._buf, self._kind = [], "title"
        elif tag == "h1":
            self._buf, self._kind = [], "h1"
        if tag not in ("meta", "link", "img", "br", "hr", "input", "source"):
            self._stack.append(tag)

    def handle_endtag(self, tag):
        if self._buf is not None and tag in ("script", "title", "h1"):
            text = "".join(self._buf)
            if self._kind == "jsonld": self.jsonld.append(text)
            elif self._kind == "title": self.title = " ".join(text.split())
            elif self._kind == "h1": self.h1.append(" ".join(text.split()))
            self._buf = None
        if tag in self._stack:  # ignore a stray end tag rather than unwinding the whole stack
            while self._stack.pop() != tag:
                pass

    def handle_data(self, data):
        if self._buf is not None:
            self._buf.append(data)
        if not (set(self._stack) & (VOID_TEXT | CHROME)) and "body" in self._stack:
            self.words += len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’-]*", data))


def route_of(rel: str) -> str:
    rel = rel.replace(os.sep, "/")
    if rel == "index.html": return "/"
    if rel.endswith("/index.html"): return "/" + rel[: -len("/index.html")]
    return "/" + rel[: -len(".html")]


def norm(route: str) -> str:
    route = route.split("#")[0].split("?")[0]
    return "/" if route in ("", "/") else route.rstrip("/")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=str(DIST_DIR)); ap.add_argument("--base", default="")
    ap.add_argument("--no-plan", action="store_true"); ap.add_argument("--json", default="")
    args = ap.parse_args()
    root = Path(args.dir).resolve()
    if not root.is_dir():
        print(f"no directory {root}. Build the site first (cd site && npm run build), or pass --dir."); return 2
    skip = ALWAYS_SKIP | (ROOT_SKIP if root == REPO else set())
    pages: Dict[str, Page] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for f in filenames:
            if f.endswith(".html"):
                p = Page()
                try:
                    p.feed((Path(dirpath) / f).read_text(encoding="utf-8", errors="ignore"))
                except Exception:
                    pass
                pages[route_of(str((Path(dirpath) / f).relative_to(root)))] = p
    if not pages:
        print(f"no .html files under {root}"); return 2
    pages.pop("/404", None)

    base = args.base
    booking = ""
    try:
        site = load_json(SITE_JSON)
        base = base or ("" if is_todo(site["business"].get("url")) else site["business"]["url"])
        booking = site.get("booking", {}).get("url", "")
        booking = "" if is_todo(booking) else booking
    except Exception:
        pass
    base = base.rstrip("/")
    plan = {}
    if not args.no_plan and PAGES_JSON.exists():
        plan = {p["route"]: p for p in load_json(PAGES_JSON)["pages"]}

    def noindex(r: str) -> bool:
        return "noindex" in pages[r].robots
    indexable = sorted(r for r in pages if not noindex(r))
    rows: List[Row] = []

    def add(name: str, bad: List[str], ok: str = "", warn: bool = False) -> None:
        rows.append((name, ("WARN" if warn else "FAIL") if bad else "PASS", some(bad) or ok or f"{len(pages)} pages"))

    # on-page ---------------------------------------------------------------------
    add("on-page: exactly one <h1>", [f"{r} ({len(p.h1)})" for r, p in pages.items() if len(p.h1) != 1])
    add(f"on-page: <title> present and <= {TITLE_MAX} chars", [f"{r} ({len(p.title)})" for r, p in pages.items() if not 0 < len(p.title) <= TITLE_MAX])
    add(f"on-page: meta description present and <= {META_MAX} chars", [f"{r} ({len(p.meta)})" for r, p in pages.items() if not 0 < len(p.meta) <= META_MAX])
    titles: Dict[str, str] = {}
    dup = []
    for r in sorted(pages):
        t = pages[r].title.lower()
        if t and t in titles: dup.append(f"{r} = {titles[t]}")
        titles.setdefault(t, r)
    add("on-page: titles are unique", dup)
    add("on-page: <html lang> and viewport meta", [r for r, p in pages.items() if not p.lang or not p.viewport])
    if base:
        add("on-page: canonical is absolute and self-referencing",
            [f"{r} -> {pages[r].canonical or '(none)'}" for r in indexable if norm(pages[r].canonical.replace(base, "", 1) if pages[r].canonical.startswith(base) else "!") != r])
    else:
        rows.append(("on-page: canonical is absolute and self-referencing", "SKIP", "no base URL (business.url is TODO; pass --base)"))
    add("social: og:title, og:description and og:image on indexable pages",
        [r for r in indexable if not {"og:title", "og:description", "og:image"} <= pages[r].og], warn=True)

    # indexing ----------------------------------------------------------------------
    if plan:
        add("indexing: noindex exactly where the plan says", [f"{r} ({'noindex' if noindex(r) else 'indexable'})" for r in pages if r in plan and bool(plan[r].get("index")) == noindex(r)])
    sm = root / "sitemap.xml"
    sm_index = root / "sitemap-index.xml"
    locs: Set[str] = set()
    for f in [sm, sm_index] + sorted(root.glob("sitemap-*.xml")):
        if f.exists():
            locs |= {norm(urlparse(u).path) for u in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", f.read_text(errors="ignore")) if not u.endswith(".xml")}
    if not (sm.exists() or sm_index.exists()):
        rows.append(("indexing: sitemap lists every indexable page, no noindex page", "FAIL", "no sitemap.xml or sitemap-index.xml"))
    else:
        add("indexing: sitemap lists every indexable page, no noindex page",
            [f"missing {r}" for r in indexable if r not in locs] + [f"noindex {r} listed" for r in pages if noindex(r) and r in locs])
    robots = (root / "robots.txt").read_text(errors="ignore") if (root / "robots.txt").exists() else ""
    add("indexing: robots.txt exists with a Sitemap: line", [] if re.search(r"(?im)^sitemap:\s*https?://", robots) else ["missing robots.txt or Sitemap: line"])
    add("indexing: robots.txt does not Disallow a noindex page",
        [r for r in pages if noindex(r) and re.search(r"(?im)^disallow:\s*" + re.escape(r) + r"\b", robots)])

    # structured data ------------------------------------------------------------------
    bad_ld, types_home = [], set()
    for r in indexable:
        ok = bool(pages[r].jsonld)
        for block in pages[r].jsonld:
            try:
                data = json.loads(block)
            except Exception:
                ok = False; continue
            items = data.get("@graph", [data]) if isinstance(data, dict) else data
            for it in items if isinstance(items, list) else []:
                t = it.get("@type") if isinstance(it, dict) else None
                if r == "/" and isinstance(it, dict) and it.get("name") and it.get("url"):
                    types_home |= set(t if isinstance(t, list) else [t])
                ok = ok and bool(t)
        if not ok: bad_ld.append(r)
    add("schema: every indexable page has valid JSON-LD", bad_ld)
    if "/" in pages:
        add("schema: home has Organization/ProfessionalService with name and url", [] if types_home & HOME_TYPES else ["/ has none of " + ", ".join(sorted(HOME_TYPES))])

    # links ----------------------------------------------------------------------------
    def exists(path: str) -> bool:
        path = path.lstrip("/")
        return any((root / c).is_file() for c in ([path, path + ".html", path.rstrip("/") + "/index.html"] if path else ["index.html"]))
    broken, anchors, dead, inbound = [], [], [], {r: 0 for r in pages}
    for r, p in pages.items():
        for href in p.links:
            if href in ("#", "", "javascript:void(0)"):
                dead.append(r); continue
            if re.match(r"(?i)(mailto:|tel:|sms:|https?:|//)", href):
                if base and href.startswith(base):
                    href = href[len(base):] or "/"
                else:
                    continue
            if href.startswith("#"):
                if href[1:] not in p.ids: anchors.append(f"{r}{href}")
                continue
            target = norm(href if href.startswith("/") else (r.rsplit("/", 1)[0] + "/" + href))
            if not exists(target):
                broken.append(f"{r} -> {href}")
            elif target in inbound and target != r:
                inbound[target] += 1
    add("links: internal links resolve", sorted(set(broken)))
    add("links: #anchors point at an id on the page", sorted(set(anchors)))
    add('links: no placeholder href="#"', [f"{r} ({dead.count(r)})" for r in sorted(set(dead))])
    add("links: no orphan indexable page", [r for r in indexable if r != "/" and not inbound[r]])
    add("links: organic pages do not link to noindex landing pages",
        sorted({f"{r} -> {h}" for r in indexable for h in pages[r].links if h.startswith("/lp/")}))

    # content, media, ship-blockers -------------------------------------------------------
    add(f"content: >= {MIN_WORDS} words outside nav/header/footer", [f"{r} ({pages[r].words})" for r in indexable if pages[r].words < MIN_WORDS])
    add("media: every <img> has an alt attribute", [f"{r} ({len(p.img_no_alt)})" for r, p in pages.items() if p.img_no_alt])
    add("ship: no Tailwind CDN script", [r for r, p in pages.items() if any("cdn.tailwindcss.com" in s for s in p.srcs)])
    add("ship: no hot-linked Stitch image", [r for r, p in pages.items() if any("googleusercontent.com" in s for s in p.srcs)])
    add("ship: no fictional 555 phone number", [f"{r} ({t})" for r, p in pages.items() for t in p.tel if re.search(r"555\D?01\d\d", t)])
    if booking and "/" in pages:
        add("ship: home links to the booking URL from data/site.json", [] if booking in pages["/"].links else [f"/ has no link to {booking}"])
        add("ship: no link to a retired booking page (Calendly)", [r for r, p in pages.items() if "calendly.com" not in booking and any("calendly.com" in h for h in p.links)])
    elif "/" in pages:
        rows.append(("ship: home links to the booking URL from data/site.json", "WARN", "booking.url is TODO"))

    # plan --------------------------------------------------------------------------------
    if plan:
        add("plan: every planned page is built", [r for r in plan if r not in pages])
        add("plan: every built page is planned", [r for r in pages if r not in plan])
        diff = []
        for r, want in plan.items():
            if r not in pages: continue
            for field, got in (("title", pages[r].title), ("meta", pages[r].meta), ("h1", pages[r].h1[0] if pages[r].h1 else "")):
                if not is_todo(want.get(field)) and want.get(field, "") != got:
                    diff.append(f"{r} {field}")
        add("plan: title, meta and H1 match data/pages.json", diff)
        todo = [r for r, w in plan.items() if any(is_todo(w.get(k)) for k in ("title", "meta", "h1"))]
        if todo:
            rows.append(("plan: no page still has TODO title/meta/H1", "WARN", some(todo)))
    else:
        rows.append(("plan: built pages match data/pages.json", "SKIP", "--no-plan"))

    if args.json:
        Path(args.json).write_text(json.dumps([{"check": n, "status": s, "detail": d} for n, s, d in rows], indent=2))
    try:
        shown = root.relative_to(REPO)
    except ValueError:
        shown = root
    return print_table(f"seo check — {shown} ({len(pages)} pages, {len(indexable)} indexable, base {base or 'unset'})", rows)


if __name__ == "__main__":
    sys.exit(main())
