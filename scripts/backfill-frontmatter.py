#!/usr/bin/env python3
"""
Phase 1 backfill: add the new common-head frontmatter fields introduced by
docs/spec/specification.md to every entry under wiki/entries/.

The added fields are (per §4.1):
  - notability_status
  - edit_hardness
  - high_stakes_class
  - quality
  - produced_by  (infrastructure entries only — at this stage, only `lens`)

The script is text-preserving: it parses the frontmatter block as text,
inserts only the missing fields, and leaves all other formatting alone.
Running it twice is a no-op.

Usage:
  python3 scripts/backfill-frontmatter.py            # dry run
  python3 scripts/backfill-frontmatter.py --apply    # write changes
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = REPO_ROOT / "wiki" / "entries"

# Defaults per category. notability_status `n/a` for infrastructure.
# edit_hardness defaults follow §9.2.
DEFAULTS = {
    # content kinds (free slug)
    "concept":        {"notability_status": "passes", "edit_hardness": "open",       "high_stakes_class": "none", "quality": "c"},
    "illustration":   {"notability_status": "passes", "edit_hardness": "open",       "high_stakes_class": "none", "quality": "c"},
    "application":    {"notability_status": "passes", "edit_hardness": "open",       "high_stakes_class": "none", "quality": "c"},
    "entity":         {"notability_status": "passes", "edit_hardness": "open",       "high_stakes_class": "none", "quality": "c"},
    "process":        {"notability_status": "passes", "edit_hardness": "open",       "high_stakes_class": "none", "quality": "c"},
    "insight":        {"notability_status": "passes", "edit_hardness": "open",       "high_stakes_class": "none", "quality": "c"},
    "source":         {"notability_status": "passes", "edit_hardness": "confirmed",  "high_stakes_class": "none", "quality": "c"},
    "structure-note": {"notability_status": "passes", "edit_hardness": "confirmed",  "high_stakes_class": "none", "quality": "c"},
    # infrastructure. Per §3.4 these have `produced_by` instead of `classified_by`,
    # except `lens` which keeps `classified_by: lens-lens` AND gains `produced_by`.
    "lens":           {"notability_status": "n/a",    "edit_hardness": "restricted", "high_stakes_class": "none", "quality": "c", "produced_by": "lifecycle-bootstrap"},
    "domain":         {"notability_status": "n/a",    "edit_hardness": "restricted", "high_stakes_class": "none", "quality": "c", "produced_by": "lifecycle-bootstrap"},
    "policy":         {"notability_status": "n/a",    "edit_hardness": "restricted", "high_stakes_class": "none", "quality": "c", "produced_by": "lifecycle-bootstrap"},
    "guideline":      {"notability_status": "n/a",    "edit_hardness": "extended-confirmed", "high_stakes_class": "none", "quality": "c", "produced_by": "lifecycle-bootstrap"},
    "essay":          {"notability_status": "n/a",    "edit_hardness": "open",       "high_stakes_class": "none", "quality": "c", "produced_by": "lifecycle-bootstrap"},
    # Per §9.2: agent default is `extended-confirmed` (mutate), `restricted` (retire);
    # we use `extended-confirmed` for the manifest itself.
    "agent":          {"notability_status": "n/a",    "edit_hardness": "extended-confirmed", "high_stakes_class": "none", "quality": "c", "produced_by": "lifecycle-agent-create"},
    "agent-test":     {"notability_status": "n/a",    "edit_hardness": "extended-confirmed", "high_stakes_class": "none", "quality": "c", "produced_by": "lifecycle-agent-test-create"},
    # The remaining infrastructure kinds (run, finding, discussion, notification,
    # pending) carry `edit_hardness: locked` per §9.2 — they're immutable once
    # written. They are produced by their own protocols, not by lifecycle-bootstrap.
    "run":            {"notability_status": "n/a",    "edit_hardness": "locked",     "high_stakes_class": "none", "quality": "c", "produced_by": "lifecycle-run-emit"},
    "finding":        {"notability_status": "n/a",    "edit_hardness": "locked",     "high_stakes_class": "none", "quality": "c", "produced_by": "lifecycle-finding-emit"},
    "discussion":     {"notability_status": "n/a",    "edit_hardness": "locked",     "high_stakes_class": "none", "quality": "c", "produced_by": "lifecycle-discussion-open"},
    "notification":   {"notability_status": "n/a",    "edit_hardness": "locked",     "high_stakes_class": "none", "quality": "c", "produced_by": "lifecycle-notification-emit"},
    "pending":        {"notability_status": "n/a",    "edit_hardness": "open",       "high_stakes_class": "none", "quality": "c", "produced_by": "lifecycle-pending-stage"},
}

# The order new fields are inserted in (within the frontmatter block).
FIELD_ORDER = ["notability_status", "edit_hardness", "high_stakes_class", "quality", "produced_by"]

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def parse_frontmatter_block(text: str) -> tuple[str, str, str] | None:
    """Return (block_with_fences, inner, rest) or None if no frontmatter."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    return m.group(0), m.group(1), text[m.end():]


def field_present(inner: str, field: str) -> bool:
    # match a top-level YAML key at column 0 (no leading whitespace, no list bullet).
    return re.search(rf"(?m)^{re.escape(field)}\s*:", inner) is not None


def get_category(inner: str) -> str | None:
    m = re.search(r"(?m)^category\s*:\s*(\S+)", inner)
    return m.group(1).strip() if m else None


def build_insert_block(missing: dict[str, str]) -> str:
    # Emit fields in canonical order, one per line, no quotes (all values are bare enums).
    lines = [f"{k}: {missing[k]}" for k in FIELD_ORDER if k in missing]
    return "\n".join(lines) + "\n"


def process_file(path: Path) -> tuple[str, dict[str, str]]:
    """
    Returns (status, fields_added).
    status ∈ {"ok", "skip-no-frontmatter", "skip-unknown-category", "noop"}
    """
    original = path.read_text(encoding="utf-8")
    parsed = parse_frontmatter_block(original)
    if parsed is None:
        return "skip-no-frontmatter", {}
    block, inner, rest = parsed

    category = get_category(inner)
    if category is None or category not in DEFAULTS:
        return "skip-unknown-category", {"category": category or "<missing>"}

    targets = DEFAULTS[category]
    missing = {k: v for k, v in targets.items() if not field_present(inner, k)}
    if not missing:
        return "noop", {}

    insert = build_insert_block(missing)
    new_inner = inner.rstrip("\n") + "\n" + insert.rstrip("\n")
    new_block = f"---\n{new_inner}\n---\n"
    new_text = new_block + rest

    # Write only when caller requests; the caller will dispatch.
    return "ok", {"_new_text": new_text, **missing}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write changes (default: dry run)")
    parser.add_argument("--verbose", action="store_true", help="Print per-file actions")
    args = parser.parse_args()

    if not ENTRIES_DIR.is_dir():
        print(f"error: {ENTRIES_DIR} not found", file=sys.stderr)
        return 1

    files = sorted(ENTRIES_DIR.glob("*.md"))
    counts = Counter()
    field_counts = Counter()
    skipped_unknown = []

    for path in files:
        status, info = process_file(path)
        counts[status] += 1
        if status == "ok":
            for k in info:
                if k != "_new_text":
                    field_counts[k] += 1
            if args.apply:
                path.write_text(info["_new_text"], encoding="utf-8")
            if args.verbose:
                added = ", ".join(k for k in info if k != "_new_text")
                print(f"  {path.name}: +{added}")
        elif status == "skip-unknown-category":
            skipped_unknown.append((path.name, info.get("category")))
            if args.verbose:
                print(f"  {path.name}: SKIP (category={info.get('category')})")

    mode = "APPLIED" if args.apply else "DRY RUN"
    print(f"=== backfill-frontmatter.py [{mode}] ===")
    print(f"entries scanned:           {len(files)}")
    print(f"  needed updates (ok):     {counts['ok']}")
    print(f"  already complete (noop): {counts['noop']}")
    print(f"  no frontmatter:          {counts['skip-no-frontmatter']}")
    print(f"  unknown category:        {counts['skip-unknown-category']}")
    if field_counts:
        print("fields added (sum across files):")
        for f in FIELD_ORDER:
            if field_counts[f]:
                print(f"  {f}: {field_counts[f]}")
    if skipped_unknown:
        print("skipped (unknown category, not in DEFAULTS):")
        for name, cat in skipped_unknown:
            print(f"  {name} (category={cat})")
    if not args.apply and counts["ok"] > 0:
        print("\nrun with --apply to write changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
