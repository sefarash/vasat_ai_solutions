#!/usr/bin/env python3
"""The page plan (data/pages.json): which pages exist, and the keyword, title, meta and H1 of each.

  python3 tools/page_plan.py validate [--strict]        # lengths, uniqueness, keyword placement; --strict fails TODOs
  python3 tools/page_plan.py keyword "ai voice agent for hvac"    # is this keyword free? exit 1 if a page already owns it
  python3 tools/page_plan.py add --route /services/ai-voice-agent --type service \
        --keyword "ai voice agent for contractors" --title "..." --meta "..." --h1 "..." [--noindex] [--dry-run]
  python3 tools/page_plan.py list

Page types: home, service, industry, landing, legal, utility. landing and utility pages are noindex.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import PAGES_JSON, REPO, SITE_JSON, Row, is_todo, load_json, print_table, some

TITLE_MAX, META_MAX, META_MIN = 60, 155, 70
TYPES = {"home", "service", "industry", "landing", "legal", "utility"}
NOINDEX_TYPES = {"landing", "utility"}
STOP = {"a", "an", "the", "for", "in", "of", "and", "to", "with", "near", "me", "&"}


def words(s: str) -> List[str]:
    return [w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP]


def covers(text: str, keyword: str) -> bool:
    """Every meaningful word of the keyword appears in the text (order free, plural-tolerant)."""
    have = {w.rstrip("s") for w in words(text)}
    return all(w.rstrip("s") in have for w in words(keyword))


def validate(pages: List[Dict], strict: bool) -> List[Row]:
    rows: List[Row] = []

    def add(name: str, bad: List[str], ok: str = "") -> None:
        rows.append((name, "FAIL" if bad else "PASS", some(bad, 5) or ok or f"{len(pages)} pages"))

    routes = [p.get("route", "") for p in pages]
    add("route: present, starts with /, no trailing slash, unique",
        [r or "(empty)" for r in routes if not r.startswith("/") or (len(r) > 1 and r.endswith("/")) or routes.count(r) > 1])
    add("route: lowercase words joined by hyphens", [r for r in routes if not re.fullmatch(r"(/[a-z0-9]+(-[a-z0-9]+)*)*/?", r)])
    add("type: one of " + ", ".join(sorted(TYPES)), [f"{p.get('route')} ({p.get('type')})" for p in pages if p.get("type") not in TYPES])
    add("index: landing and utility pages are noindex", [p["route"] for p in pages if p.get("type") in NOINDEX_TYPES and p.get("index")])
    add("home: exactly one page of type home at /", [] if [p.get("route") for p in pages if p.get("type") == "home"] == ["/"] else ["need one home at /"])

    todo = [f"{p.get('route')}.{k}" for p in pages for k in ("primary_keyword", "title", "meta", "h1") if is_todo(p.get(k))]
    rows.append(("todo: no TODO placeholder left", "PASS" if not todo else ("FAIL" if strict else "WARN"), some(todo, 5) or "none"))

    done = [p for p in pages if not any(is_todo(p.get(k)) for k in ("title", "meta", "h1"))]
    add(f"title: present and <= {TITLE_MAX} chars", [f"{p['route']} ({len(p.get('title', ''))})" for p in done if not 0 < len(p.get("title", "")) <= TITLE_MAX])
    add(f"meta: {META_MIN}-{META_MAX} chars", [f"{p['route']} ({len(p.get('meta', ''))})" for p in done if not META_MIN <= len(p.get("meta", "")) <= META_MAX])
    add("h1: present and different from the title", [p["route"] for p in done if not p.get("h1") or p.get("h1") == p.get("title")])
    for field in ("title", "meta", "h1"):
        seen: Dict[str, str] = {}
        dup = []
        for p in done:
            v = p.get(field, "").strip().lower()
            if v in seen:
                dup.append(f"{p['route']} = {seen[v]}")
            seen.setdefault(v, p["route"])
        add(f"{field}: unique across pages", dup)

    # keywords: only pages meant to rank need one
    ranking = [p for p in pages if p.get("index") and p.get("type") not in ("legal", "utility")]
    kw = [p for p in ranking if not is_todo(p.get("primary_keyword"))]
    add("keyword: every ranking page has a primary keyword", [p["route"] for p in kw if not p.get("primary_keyword")])
    owners: Dict[str, str] = {}
    clash = []
    for p in kw:
        key = " ".join(sorted(w.rstrip("s") for w in words(p.get("primary_keyword", ""))))
        if key and key in owners:
            clash.append(f"{p['route']} and {owners[key]} both target '{p['primary_keyword']}'")
        owners.setdefault(key, p["route"])
    add("keyword: no two pages target the same keyword", clash)
    placed = [p for p in kw if p.get("primary_keyword") and p in done]
    add("keyword: appears in the title", [p["route"] for p in placed if not covers(p["title"], p["primary_keyword"])])
    add("keyword: appears in the H1", [p["route"] for p in placed if not covers(p["h1"], p["primary_keyword"])])

    try:
        site = load_json(SITE_JSON)
        for group, prefix in (("services", "/services/"), ("industries", "/industries/")):
            planned = {r[len(prefix):] for r in routes if r.startswith(prefix)}
            known = {x["slug"] for x in site.get(group, [])}
            add(f"{group}: every {prefix}<slug> page exists in data/site.json", sorted(planned - known), f"{len(planned)} planned, {len(known)} in site.json")
    except Exception as e:
        rows.append(("site.json readable", "FAIL", str(e)[:90]))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    v = sub.add_parser("validate"); v.add_argument("--strict", action="store_true")
    k = sub.add_parser("keyword"); k.add_argument("phrase")
    sub.add_parser("list")
    a = sub.add_parser("add")
    for flag in ("--route", "--type", "--keyword", "--title", "--meta", "--h1"):
        a.add_argument(flag, required=flag in ("--route", "--type"), default="TODO")
    a.add_argument("--noindex", action="store_true"); a.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.cmd:
        ap.print_help(); return 2

    plan = load_json(PAGES_JSON)
    pages = plan["pages"]

    if args.cmd == "list":
        for p in pages:
            print(f"  {p['route']:36} {p.get('type', '?'):9} {'index  ' if p.get('index') else 'noindex'}  {p.get('primary_keyword') or '-'}")
        return 0

    if args.cmd == "keyword":
        owner = [p for p in pages if p.get("primary_keyword") and not is_todo(p["primary_keyword"])
                 and covers(p["primary_keyword"], args.phrase) and covers(args.phrase, p["primary_keyword"])]
        near = [p for p in pages if p not in owner and (covers(p.get("title", ""), args.phrase) or covers(p.get("h1", ""), args.phrase))]
        if owner:
            print(f"TAKEN: {owner[0]['route']} already targets '{owner[0]['primary_keyword']}'. Strengthen that page instead of adding one.")
            return 1
        print(f"FREE: no page has '{args.phrase}' as its primary keyword.")
        for p in near:
            print(f"  note: {p['route']} already uses these words in its title or H1; a new page needs a different search intent, not a rewording.")
        return 0

    if args.cmd == "add":
        if any(p["route"] == args.route for p in pages):
            print(f"refusing: {args.route} is already in the plan"); return 1
        entry = {"route": args.route, "type": args.type, "index": not (args.noindex or args.type in NOINDEX_TYPES),
                 "primary_keyword": args.keyword, "title": args.title, "meta": args.meta, "h1": args.h1}
        rows = validate(pages + [entry], strict=False)
        code = print_table(f"page plan with {args.route} added", rows)
        if code:
            print("\nnot written: fix the FAIL rows and run again"); return 1
        if args.dry_run:
            print("\ndry run, nothing written:\n" + json.dumps(entry, indent=2)); return 0
        pages.append(entry)
        PAGES_JSON.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"\nadded {args.route} to {PAGES_JSON.relative_to(REPO)}")
        return 0

    return print_table(f"page plan — {PAGES_JSON.relative_to(REPO)}{' (strict)' if args.strict else ''}", validate(pages, args.strict))


if __name__ == "__main__":
    sys.exit(main())
