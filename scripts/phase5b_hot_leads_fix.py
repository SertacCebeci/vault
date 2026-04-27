#!/usr/bin/env python3
"""
Correct phase5b_hot_leads.py's mistake.

The first pass blindly inserted `## Lead` sections between the title and the
first `## Section` heading — but the 10 hot entries had **implicit leads**
(an opening paragraph after the title that already served as the lead). The
result was duplication: an implicit lead, then my added `## Lead`.

This script:
  1. Removes the `## Lead\\n\\n{my-authored-lead}\\n\\n` blocks I inserted.
  2. Promotes the existing implicit-lead paragraph to a real `## Lead` section
     by inserting the `## Lead` heading right after the title heading.

The existing implicit leads were stylistically a better fit — author-voice,
already source-grounded, mechanism-rich — so we keep them. Any extra context
my added leads carried (Bjorks attribution, etc.) was already present
elsewhere in each entry's body.

Idempotent. Safe to re-run.

Usage:
  python3 scripts/phase5b_hot_leads_fix.py            # dry run
  python3 scripts/phase5b_hot_leads_fix.py --apply    # write changes
"""

from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = REPO_ROOT / "wiki" / "entries"

# Files modified by phase5b_hot_leads.py — same list, exact filenames.
HOT_FILES = [
    "biologically-primary-and-secondary-knowledge.md",
    "desirable-difficulty.md",
    "declarative-learning-system.md",
    "declarative-procedural-seesaw.md",
    "einstellung.md",
    "interleaving.md",
    "procedural-learning-system.md",
    "spaced-repetition.md",
    "testing-effect.md",
    "working-memory.md",
]


def correct_one(text: str) -> tuple[str, str]:
    """
    Returns (new_text, status). status ∈ {"corrected", "no-change", "no-implicit-lead"}.
    """
    # 1. Locate the title heading line and the next '## ' heading.
    title_match = re.search(r"(?m)^# .+$", text)
    if not title_match:
        return text, "no-title"

    title_end = title_match.end()
    # Find the next `##` heading after the title.
    next_h2 = re.search(r"(?m)^## ", text[title_end:])
    if not next_h2:
        return text, "no-h2"

    h2_abs_start = title_end + next_h2.start()
    between = text[title_end:h2_abs_start]

    # If there's no prose between title and first `##`, there is no implicit lead.
    # (The entry was already in canonical form before phase5b_hot_leads.py touched it.)
    if not between.strip():
        return text, "no-implicit-lead"

    # The first `##` heading should be `## Lead` if phase5b_hot_leads.py applied.
    # We want to detect that case and consume the `## Lead\n\n{my-lead}\n\n` block.
    if not text[h2_abs_start:].startswith("## Lead\n"):
        return text, "no-pending-fix"

    # Find the `##` heading after `## Lead` (i.e., the section that came BEFORE my insert).
    after_lead_start = h2_abs_start + len("## Lead\n")
    # Skip the immediate blank line(s) and lead body until next `## ` heading.
    next_after_lead = re.search(r"(?m)^## ", text[after_lead_start:])
    if not next_after_lead:
        return text, "no-section-after-my-lead"
    my_lead_end_abs = after_lead_start + next_after_lead.start()

    # Compose the corrected text:
    # = text[:title_end]                     # `# Title`
    # + "\n\n## Lead\n"                       # promoted heading
    # + (implicit-lead body, stripped of leading/trailing blanks but with one trailing \n\n)
    # + (the `##` section that originally followed the implicit lead)
    title_segment = text[:title_end]
    implicit_body = between.strip("\n")  # keep internal blank lines if multi-paragraph
    after_my_lead = text[my_lead_end_abs:]

    new_text = (
        title_segment
        + "\n\n## Lead\n\n"
        + implicit_body
        + "\n\n"
        + after_my_lead
    )
    return new_text, "corrected"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    actions: list[str] = []
    errors: list[str] = []

    for fname in HOT_FILES:
        path = ENTRIES_DIR / fname
        if not path.exists():
            errors.append(f"missing: {fname}")
            continue
        text = path.read_text(encoding="utf-8")
        new_text, status = correct_one(text)
        if status == "corrected":
            actions.append(f"  CORRECTED: {fname}")
            if args.apply:
                path.write_text(new_text, encoding="utf-8")
        else:
            actions.append(f"  SKIP ({status}): {fname}")

    mode = "APPLIED" if args.apply else "DRY RUN"
    print(f"=== phase5b_hot_leads_fix.py [{mode}] ===\n")
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
