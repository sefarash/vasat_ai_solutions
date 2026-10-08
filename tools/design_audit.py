#!/usr/bin/env python3
"""Read a Stitch export (DESIGN.md + <screen>/code.html) and report what the build needs to know.

  python3 tools/design_audit.py tokens     [--screen home] [--write]   # colours, fonts, radius, spacing; DESIGN.md vs code.html conflicts
  python3 tools/design_audit.py inventory  [--screen home]             # sections, headings, images, icons, fonts, external scripts
  python3 tools/design_audit.py claims     [--screen home]             # facts and claims in the copy that need the owner's confirmation
  python3 tools/design_audit.py all        [--screen home]

--write (tokens) saves the resolved tokens to design/tokens.json for the build to import.
code.html is what the designer saw rendered, so it wins over DESIGN.md wherever they disagree.
Exit 0 always for inventory/claims; tokens exits 1 only if code.html has no Tailwind config.
"""
from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import DESIGN_DIR, REPO, SITE_JSON, is_todo, load_json, walk_strings

STITCH = DESIGN_DIR / "stitch"


# ---------------------------------------------------------------- parsing
def tailwind_config(page: str) -> Dict[str, Any]:
    """The inline `tailwind.config = {...}` object, converted from a JS literal to a dict."""
    start = page.find("tailwind.config")
    if start < 0:
        return {}
    start = page.index("{", start)
    depth, end = 0, start
    for i in range(start, len(page)):
        depth += {"{": 1, "}": -1}.get(page[i], 0)
        if depth == 0:
            end = i + 1
            break
    js = page[start:end]
    js = re.sub(r"([{,]\s*)([A-Za-z_$][\w$-]*)\s*:", r'\1"\2":', js)  # quote bare keys
    js = re.sub(r",\s*([}\]])", r"\1", js)                             # trailing commas
    try:
        return json.loads(js).get("theme", {}).get("extend", {})
    except json.JSONDecodeError:
        return {}


def design_md_tokens(text: str) -> Dict[str, Any]:
    """The YAML front matter of DESIGN.md. Two or three levels of `key: value`, nothing fancier."""
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    root: Dict[str, Any] = {}
    stack: List[Tuple[int, Dict[str, Any]]] = [(-1, root)]
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        key, _, value = line.strip().partition(":")
        value = value.strip().strip("'\"")
        while stack[-1][0] >= indent:
            stack.pop()
        if value:
            stack[-1][1][key] = value
        else:
            child: Dict[str, Any] = {}
            stack[-1][1][key] = child
            stack.append((indent, child))
    return root


def visible_text(page: str) -> List[str]:
    body = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", "", page)
    body = re.sub(r'(?s)<span[^>]*material-symbols[^>]*>.*?</span>', "", body)  # icon ligatures are not copy
    return [t for t in (html.unescape(s).strip() for s in re.sub(r"<[^>]+>", "\n", body).split("\n")) if t]


# ---------------------------------------------------------------- reports
def report_tokens(page: str, write: bool) -> int:
    code = tailwind_config(page)
    md = design_md_tokens((STITCH / "DESIGN.md").read_text(encoding="utf-8")) if (STITCH / "DESIGN.md").exists() else {}
    if not code:
        print("tokens: no tailwind.config found in code.html; cannot resolve tokens")
        return 1
    colors, md_colors = code.get("colors", {}), md.get("colors", {})
    fonts = sorted({v[0] for v in code.get("fontFamily", {}).values() if v})
    md_fonts = sorted({v.get("fontFamily", "") for v in md.get("typography", {}).values() if isinstance(v, dict)} - {""})
    radius = code.get("borderRadius", {})
    used_radius = Counter(re.findall(r"\brounded(?:-[a-z0-9]+)*\b", page))

    print(f"tokens — {len(colors)} colours, fonts {fonts}, radius scale {radius}")
    print("\n  brand colours (code.html):")
    for name in ("primary", "secondary", "tertiary", "cobalt", "gold", "gold-hover", "background", "surface", "on-surface", "inverse-surface"):
        if name in colors:
            print(f"    {name.ljust(16)} {colors[name]}")
    arbitrary = Counter(c.lower() for c in re.findall(r"\[(#[0-9a-fA-F]{6})\]", page))
    if arbitrary:
        print(f"\n  one-off hex values used in class names (promote the repeated ones to tokens): {dict(arbitrary.most_common(8))}")

    conflicts = []
    for name in sorted(set(colors) & set(md_colors)):
        if colors[name].lower() != md_colors[name].lower():
            conflicts.append(f"colour {name}: code.html {colors[name]} vs DESIGN.md {md_colors[name]}")
    if md_fonts and set(md_fonts) != set(fonts):
        conflicts.append(f"fonts: code.html {fonts} vs DESIGN.md {md_fonts}")
    md_body = (STITCH / "DESIGN.md").read_text(encoding="utf-8") if md else ""
    if re.search(r"0px (border )?radius|zero-radius", md_body) and sum(used_radius.values()):
        conflicts.append(f"radius: DESIGN.md says strict 0px; code.html uses rounded corners {dict(used_radius.most_common(4))}")
    print(f"\n  DESIGN.md vs code.html: {len(conflicts)} conflict(s). code.html wins unless the owner says otherwise.")
    for c in conflicts[:12]:
        print(f"    - {c}")
    if len(conflicts) > 12:
        print(f"    (+{len(conflicts) - 12} more colour differences)")

    if write:
        out = DESIGN_DIR / "tokens.json"
        resolved = {"_readme": "Generated by tools/design_audit.py tokens --write from design/stitch. Do not edit; change the design and re-run.",
                    "colors": colors, "fontFamily": code.get("fontFamily", {}), "fontSize": code.get("fontSize", {}),
                    "borderRadius": radius, "spacing": code.get("spacing", {})}
        out.write_text(json.dumps(resolved, indent=2) + "\n", encoding="utf-8")
        print(f"\n  wrote {out.relative_to(REPO)}")
    return 0


def report_inventory(page: str) -> int:
    print("inventory")
    print("\n  sections, in order:")
    for tag, attrs in re.findall(r"<(header|section|footer)\b([^>]*)>", page):
        sid = re.search(r'id="([^"]+)"', attrs)
        dark = bool(re.search(r"bg-\[#0|from-\[#0|text-white", attrs))
        print(f"    <{tag}> {('#' + sid.group(1)) if sid else '(no id)':18} {'dark' if dark else 'light'}")
    print("\n  headings:")
    for level, inner in re.findall(r"(?s)<h([1-3])\b[^>]*>(.*?)</h\1>", page):
        text = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", inner)).split())
        print(f"    h{level}  {text[:100]}")
    h1 = len(re.findall(r"<h1\b", page))
    if h1 != 1:
        print(f"    note: the design has {h1} <h1>; the built page needs exactly one")
    print("\n  images (all must be downloaded or replaced; Stitch URLs expire and are not ours to hot-link):")
    for src, alt in [(re.search(r'src="([^"]+)"', t), re.search(r'alt="([^"]*)"', t)) for t in re.findall(r"<img\b[^>]*>", page)]:
        print(f"    {(alt.group(1) if alt else '(no alt)')[:70]:70}  {(src.group(1) if src else '')[:60]}")
    icons = Counter(re.findall(r'(?s)<span[^>]*material-symbols[^>]*>\s*([a-z0-9_]+)\s*</span>', page))
    print(f"\n  Material Symbols icons ({len(icons)} distinct; ship as inline SVG, not the 300 KB+ icon font): {', '.join(sorted(icons))}")
    print("\n  external resources in the export:")
    for url in sorted(set(re.findall(r'(?:src|href)="(https?://[^"]+)"', page))):
        if "googleusercontent" not in url:
            print(f"    {html.unescape(url)[:110]}")
    forms = re.findall(r"<form\b[^>]*>", page)
    fields = re.findall(r'<(?:input|select|textarea)\b[^>]*?(?:name|id)="([^"]+)"', page)
    print(f"\n  forms: {len(forms)}; fields: {', '.join(dict.fromkeys(fields)) or 'none'}")
    anchors = set(re.findall(r'href="#([^"]+)"', page)) - set(re.findall(r'id="([^"]+)"', page))
    if anchors:
        print(f"  nav anchors with no matching id: {', '.join(sorted(anchors))}")
    dead = len(re.findall(r'href="#"', page))
    if dead:
        print(f"  links going nowhere (href=\"#\"): {dead}; each needs a real target or to be removed")
    return 0


def report_claims(page: str) -> int:
    lines = visible_text(page)
    text = "\n".join(lines)
    facts = {}
    try:
        facts = {k: v for k, v in walk_strings(load_json(SITE_JSON)) if not is_todo(v)}
    except Exception:
        pass
    known = " ".join(facts.values())
    print("claims — everything below is design filler until the owner confirms it. Do not ship an unconfirmed item.")

    def section(title: str, items: List[str]) -> None:
        items = list(dict.fromkeys(items))
        print(f"\n  {title} ({len(items)}):")
        for i in items[:20]:
            print(f"    - {i[:150]}")

    phones = re.findall(r"\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}", text)
    emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    section("contact details not in data/site.json", [x for x in phones + emails if x not in known])
    section("statistics and numeric promises", [l for l in lines if re.search(r"\d+(\.\d+)?\s?%|\b\d+(\.\d+)?x\b|\$\d|\b\d+ (days?|hours?|seconds?)\b|< ?\d", l, re.I)])
    section("testimonials (a quote needs a real, consenting customer)", [l for l in lines if l.startswith(('"', "“")) and len(l) > 40])
    section("named people and businesses", [l for l in lines if re.search(r"^(Owner|Founder|CEO|President|Manager),? ", l)]
            + [lines[i - 1] for i, l in enumerate(lines) if i and re.search(r"^(Owner|Founder|CEO|President|Manager),? ", l)])
    section("third-party products named (integration must exist before it is advertised)",
            [l for l in lines if re.search(r"ServiceTitan|Housecall|Jobber|QuickBooks|Salesforce|HubSpot|Zapier|Calendly|Twilio", l)])
    section("absolute or guarantee language", [l for l in lines if re.search(r"\b(guarantee|100%|never|always|zero|0 risk|#1|best)\b", l, re.I)])
    try:
        names = [s["name"] for s in load_json(SITE_JSON).get("services", [])]
        offered = [l for l in lines if re.search(r"Google Ads|Meta Ads|SEO|Voice Agent|CRM|Website", l) and len(l) < 60]
        missing = [o for o in dict.fromkeys(offered) if not any(set(o.lower().split()) & set(n.lower().split()) - {"ai", "&"} for n in names)]
        section("services in the design with no match in data/site.json", missing)
    except Exception:
        pass
    return 0


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] not in ("tokens", "inventory", "claims", "all"):
        print(__doc__)
        return 2
    screen = args[args.index("--screen") + 1] if "--screen" in args else "home"
    code = STITCH / screen / "code.html"
    if not code.exists():
        have = sorted(p.parent.name for p in STITCH.glob("*/code.html"))
        print(f"no {code.relative_to(REPO)}; screens available: {have or 'none'}")
        return 2
    page = code.read_text(encoding="utf-8")
    print(f"design audit — {code.relative_to(REPO)}\n")
    rc = 0
    for name in (["tokens", "inventory", "claims"] if args[0] == "all" else [args[0]]):
        if name == "tokens":
            rc |= report_tokens(page, "--write" in args)
        elif name == "inventory":
            report_inventory(page)
        else:
            report_claims(page)
        print()
    return rc


if __name__ == "__main__":
    sys.exit(main())
