#!/usr/bin/env python3
"""
Second rename pass: `structure-building-skill` → `mental-structure-building`.
The first rename in `phase5a_finish.py` cleared the file-name collision but
the new slug still starts with the `structure-` reserved prefix (§6.5), so
the `reserved-prefix-misuse` lint rule still fires. The right slug for this
concept is one that does not start with a reserved prefix at all.

Idempotent. Re-runs on a completed state are no-ops.

Usage:
  python3 scripts/phase5a_rerename.py            # dry run
  python3 scripts/phase5a_rerename.py --apply    # write changes
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = REPO_ROOT / "wiki" / "entries"

OLD_SLUG = "structure-building-skill"
NEW_SLUG = "mental-structure-building"

OLD_PATH = ENTRIES_DIR / f"{OLD_SLUG}.md"
NEW_PATH = ENTRIES_DIR / f"{NEW_SLUG}.md"

# Files that referenced [[structure-building-skill]] after the first rename.
INBOUND_FILES = [
    "bruce-hendry-winding-stair.md",
    "learning-styles-myth.md",
    "make-it-stick.md",
    "mental-models.md",
    "rule-learning.md",
    "lens-structure-note.md",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    actions: list[str] = []
    errors: list[str] = []

    # 1) Rename the file
    if NEW_PATH.exists():
        actions.append(f"  SKIP: {NEW_PATH.name} already exists")
    elif OLD_PATH.exists():
        actions.append(f"  RENAME: {OLD_PATH.name} → {NEW_PATH.name}")
        if args.apply:
            text = OLD_PATH.read_text(encoding="utf-8")
            new_text = text.replace(
                f"id: {OLD_SLUG}\n", f"id: {NEW_SLUG}\n"
            )
            NEW_PATH.write_text(new_text, encoding="utf-8")
            OLD_PATH.unlink()
    else:
        errors.append(f"neither {OLD_PATH.name} nor {NEW_PATH.name} exists")

    # 2) Rewrite inbound wikilinks
    for fname in INBOUND_FILES:
        path = ENTRIES_DIR / fname
        if not path.exists():
            errors.append(f"inbound file not found: {fname}")
            continue
        text = path.read_text(encoding="utf-8")
        new_text = (
            text
            .replace(f"[[{OLD_SLUG}]]", f"[[{NEW_SLUG}]]")
            .replace(f"[[{OLD_SLUG}|", f"[[{NEW_SLUG}|")
        )
        if new_text == text:
            actions.append(f"  SKIP (no inbound found): {fname}")
            continue
        n = text.count(f"[[{OLD_SLUG}]]") + text.count(f"[[{OLD_SLUG}|")
        actions.append(f"  RELINK: {fname} ({n} link{'s' if n != 1 else ''})")
        if args.apply:
            path.write_text(new_text, encoding="utf-8")

    # 3) Update lens-structure-note's note (mention the final slug)
    lsn = ENTRIES_DIR / "lens-structure-note.md"
    if lsn.exists():
        text = lsn.read_text(encoding="utf-8")
        old_note = (
            "[[structure-building-skill]] is a single cognitive skill (a learner's "
            "ability to extract central ideas and organize them into a coherent "
            "framework). It was renamed during Phase 5a from `structure-building` "
            "to clear the reserved-prefix collision (§6.5); the entry remains "
            "`category: concept` because it describes one principle, not a cluster's "
            "organizing prose."
        )
        new_note = (
            "[[mental-structure-building]] is a single cognitive skill (a learner's "
            "ability to extract central ideas and organize them into a coherent "
            "framework). It was renamed during Phase 5a from `structure-building` "
            "to `mental-structure-building` to clear the `structure-` reserved-prefix "
            "collision (§6.5); the entry remains `category: concept` because it "
            "describes one principle, not a cluster's organizing prose."
        )
        if old_note in text:
            actions.append("  RENOTE: lens-structure-note.md")
            if args.apply:
                lsn.write_text(text.replace(old_note, new_note), encoding="utf-8")
        elif new_note in text:
            actions.append("  SKIP (already renoted): lens-structure-note.md")
        else:
            actions.append("  SKIP (note not found verbatim): lens-structure-note.md")

    mode = "APPLIED" if args.apply else "DRY RUN"
    print(f"=== phase5a_rerename.py [{mode}] ===\n")
    for a in actions:
        print(a)
    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  {e}")
        return 1
    if not args.apply:
        print("\nrun with --apply to execute.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
