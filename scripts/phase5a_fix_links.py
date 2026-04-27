#!/usr/bin/env python3
"""
One-shot Phase 5a fix: resolve the 16 legacy broken-wikilink findings.

Each substitution is text-preserving and exact-match. The script prints what
it would change in dry-run mode and refuses to alter files where the
expected source text is not found (so a re-run after manual edits won't
silently corrupt prose).

Usage:
  python3 scripts/phase5a_fix_links.py            # dry run
  python3 scripts/phase5a_fix_links.py --apply    # write changes
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = REPO_ROOT / "wiki" / "entries"

# Each tuple: (filename, exact_old_text, new_text, kind)
# kind ∈ {"case-fix", "redirect", "plain-text"}
SUBSTITUTIONS: list[tuple[str, str, str, str]] = [
    # Case-bug fixes — target exists, just lowercase the slug.
    ("bdnf-and-exercise.md",
     "[[Sleep-and-learning|Sleep]]",
     "[[sleep-and-learning|Sleep]]",
     "case-fix"),
    ("consolidation.md",
     "[[Brain-breaks]]",
     "[[brain-breaks]]",
     "case-fix"),
    ("consolidation.md",
     "[[Recall-as-learning|Retrieval practice]]",
     "[[recall-as-learning|Retrieval practice]]",
     "case-fix"),
    ("declarative-learning-system.md",
     "[[Consolidation]]",
     "[[consolidation]]",
     "case-fix"),
    ("declarative-procedural-seesaw.md",
     "[[Dopamine-and-learning]]",
     "[[dopamine-and-learning]]",
     "case-fix"),
    ("flipped-classroom-online.md",
     "[[Brain-breaks]]",
     "[[brain-breaks]]",
     "case-fix"),
    ("flipped-classroom-online.md",
     "[[Race-car-and-hiker-brains]]",
     "[[race-car-and-hiker-brains]]",
     "case-fix"),
    ("procedural-learning-system.md",
     "[[Dopamine-and-learning]]",
     "[[dopamine-and-learning]]",
     "case-fix"),
    ("schemas.md",
     "[[Interleaving]]",
     "[[interleaving]]",
     "case-fix"),
    ("spaced-repetition.md",
     "[[Interleaving]]",
     "[[interleaving]]",
     "case-fix"),
    ("transfer.md",
     "[[Interleaving]]",
     "[[interleaving]]",
     "case-fix"),

    # Redirect — source had target/display swapped; redirect to the entry the display implies.
    ("declarative-learning-system.md",
     "[[Retrieval practice|recall-as-learning]]",
     "[[recall-as-learning|retrieval practice]]",
     "redirect"),
    ("schemas.md",
     "[[prior-knowledge|biologically-primary-and-secondary-knowledge]]",
     "[[biologically-primary-and-secondary-knowledge]]",
     "redirect"),

    # Plain-text — target entry does not exist and is not (yet) on the build path.
    # Convert wikilink to plain prose so the lint passes; opening question entries for
    # these gaps is deferred until the question lifecycle is wired up (Phase 6).
    ("curse-of-knowledge.md",
     "[[hindsight-bias]]",
     "hindsight bias",
     "plain-text"),
    ("dooley-football-practice.md",
     "[[mike-ebersold|Ebersold]]",
     "Ebersold",
     "plain-text"),
    ("errorless-learning-myth.md",
     "[[b-f-skinner]]",
     "B. F. Skinner",
     "plain-text"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    if not ENTRIES_DIR.is_dir():
        print(f"error: {ENTRIES_DIR} not found", file=sys.stderr)
        return 1

    applied = 0
    skipped = 0
    not_found: list[tuple[str, str]] = []

    # Coalesce edits per file so we apply all subs to the same content in order.
    by_file: dict[str, list[tuple[str, str, str]]] = {}
    for filename, old, new, kind in SUBSTITUTIONS:
        by_file.setdefault(filename, []).append((old, new, kind))

    for filename, subs in by_file.items():
        path = ENTRIES_DIR / filename
        if not path.exists():
            print(f"  ERROR: {filename} not found")
            skipped += len(subs)
            continue
        text = path.read_text(encoding="utf-8")
        new_text = text
        for old, new, kind in subs:
            if old not in new_text:
                # Skip silently if already applied (idempotency); record if missing entirely.
                if new in new_text:
                    print(f"  SKIP (already applied): {filename}: {old!r} → {new!r}")
                    skipped += 1
                else:
                    print(f"  NOT FOUND: {filename}: {old!r}")
                    not_found.append((filename, old))
                continue
            new_text = new_text.replace(old, new, 1)
            print(f"  {kind:10s}: {filename}: {old!r} → {new!r}")
            applied += 1
        if args.apply and new_text != text:
            path.write_text(new_text, encoding="utf-8")

    mode = "APPLIED" if args.apply else "DRY RUN"
    print(f"\n=== phase5a_fix_links.py [{mode}] ===")
    print(f"substitutions:    {len(SUBSTITUTIONS)}")
    print(f"  applied:        {applied}")
    print(f"  already done:   {skipped}")
    print(f"  not found:      {len(not_found)}")
    if not_found:
        print("Files with substitutions whose source text was not found:")
        for f, t in not_found:
            print(f"  - {f}: {t!r}")
        return 1
    if not args.apply and applied > 0:
        print("\nrun with --apply to write changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
