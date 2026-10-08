"""Shared helpers for the tools in this folder. Stdlib only, Python 3.9 compatible."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator, List, Tuple

REPO = Path(__file__).resolve().parents[1]
SITE_JSON = REPO / "data" / "site.json"
PAGES_JSON = REPO / "data" / "pages.json"
DESIGN_DIR = REPO / "design"
SITE_DIR = REPO / "site"
DIST_DIR = SITE_DIR / "dist"

Row = Tuple[str, str, str]  # (check name, PASS|FAIL|WARN|SKIP, detail)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def is_todo(value: Any) -> bool:
    return isinstance(value, str) and value.strip().upper().startswith("TODO")


def walk_strings(node: Any, path: str = "") -> Iterator[Tuple[str, str]]:
    """Yield (dotted.path, value) for every string in a JSON tree, skipping _readme-style keys."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k.startswith("_"):
                continue
            yield from walk_strings(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_strings(v, f"{path}[{i}]")
    elif isinstance(node, str):
        yield path, node


def some(items: List[str], limit: int = 6) -> str:
    """First few items, then a count, so a table cell stays readable."""
    items = list(items)
    if len(items) <= limit:
        return ", ".join(items)
    return ", ".join(items[:limit]) + f" (+{len(items) - limit} more)"


def print_table(title: str, rows: List[Row]) -> int:
    """Print the rows and return the exit code: 1 if any FAIL, else 0."""
    width = max((len(r[0]) for r in rows), default=10)
    print(f"\n{title}\n")
    for name, status, detail in rows:
        print(f"  {name.ljust(width)}  {status:4}  {detail}")
    counts = {s: sum(1 for r in rows if r[1] == s) for s in ("PASS", "FAIL", "WARN", "SKIP")}
    print(f"\n{counts['PASS']} pass, {counts['FAIL']} fail, {counts['WARN']} warn, {counts['SKIP']} skip")
    return 1 if counts["FAIL"] else 0
