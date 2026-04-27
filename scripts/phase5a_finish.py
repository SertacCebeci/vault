#!/usr/bin/env python3
"""
Finish Phase 5a:
  1. Rename `structure-building` → `structure-building-skill` so the slug no
     longer collides with the `structure-` reserved prefix (entry stays
     `category: concept`; it describes a learner skill, not an organizing note).
     - Renames the file
     - Updates `id:` and `title:` in the new file
     - Updates 11 inbound wikilinks across 6 files
     - Adjusts the note in `lens-structure-note` that flagged the legacy slug
  2. Add a `## Lead` section to the 4 source entries that lacked one
     (`make-it-stick`, `learning-how-to-learn`, `small-teaching`,
     `uncommon-sense-teaching`). Sources require a `## Lead` regardless of
     body size per §5.2.1.

Idempotent: re-running after a successful apply is a no-op (each step checks
state before writing).

Usage:
  python3 scripts/phase5a_finish.py            # dry run
  python3 scripts/phase5a_finish.py --apply    # write changes
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = REPO_ROOT / "wiki" / "entries"

OLD_SLUG = "structure-building"
NEW_SLUG = "structure-building-skill"

OLD_PATH = ENTRIES_DIR / f"{OLD_SLUG}.md"
NEW_PATH = ENTRIES_DIR / f"{NEW_SLUG}.md"

# Files containing inbound wikilinks; we replace `[[structure-building]]` and
# `[[structure-building|...]]` patterns. The `]` and `|` boundaries prevent
# accidental matches against `[[structure-building-skill]]` itself once the
# replacement is applied.
INBOUND_FILES = [
    "bruce-hendry-winding-stair.md",
    "learning-styles-myth.md",
    "make-it-stick.md",
    "mental-models.md",
    "rule-learning.md",
    "lens-structure-note.md",
]

# Source-entry leads to insert. Each: (filename, lead_paragraph)
SOURCE_LEADS: list[tuple[str, str]] = [
    (
        "make-it-stick.md",
        "A 2014 cognitive-psychology synthesis (Brown, Roediger, McDaniel) arguing that the most effective learning strategies are deeply counterintuitive: the strategies most learners rely on — re-reading, massed practice, cramming — produce illusions of mastery without durable learning. The book introduces retrieval practice, spaced practice, interleaving, elaboration, generation, and calibration as the evidence-based core, anchored to controlled experiments and illustrated through cases from pilots, surgeons, athletes, and students.",
    ),
    (
        "learning-how-to-learn.md",
        "Transcript of the Coursera MOOC by Barbara Oakley and Terrence Sejnowski — translates neuroscience research into practical learning strategies across four weeks. Builds from the focused-vs-diffuse mode distinction through chunking as the core mechanism of learning, into procrastination remedies and long-term-memory consolidation, and finally to deliberate practice and effective test-taking.",
    ),
    (
        "small-teaching.md",
        "Lang (2021, 2nd ed.) — argues instructors can materially improve student learning through small, manageable modifications to their existing courses rather than wholesale transformation. Three parts: Knowledge (predicting, retrieving, interleaving), Understanding (connecting, practicing, explaining), Inspiration (belonging, motivating, learning). Each chapter pairs theory with concrete implementation models, guiding principles, and quick tips.",
    ),
    (
        "uncommon-sense-teaching.md",
        "Oakley, Sejnowski, and Rogowsky bridging neuroscience and K-12 / higher-ed classroom practice. The central argument: many commonsense intuitions about teaching are wrong; understanding how the brain actually learns — through neural-link formation, working- and long-term-memory dynamics, and the declarative/procedural pathways — lets teachers make small but powerful adjustments to instruction.",
    ),
]


def insert_lead(text: str, lead: str) -> str | None:
    """
    Insert `## Lead\\n\\n{lead}\\n\\n` between the title heading (`# Title`)
    and the first `## Section` heading. Returns the new text, or None if a
    `## Lead` section is already present.
    """
    if "## Lead" in text:
        return None
    # Find the first `## ...` line; insert before it.
    lines = text.split("\n")
    out: list[str] = []
    inserted = False
    for line in lines:
        if not inserted and line.startswith("## ") and not line.startswith("## Lead"):
            out.append("## Lead")
            out.append("")
            out.append(lead)
            out.append("")
            inserted = True
        out.append(line)
    if not inserted:
        return None
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    actions: list[str] = []
    errors: list[str] = []

    # --- step 1a: rename the file ------------------------------------------
    file_renamed = False
    if NEW_PATH.exists():
        actions.append(f"  SKIP: {NEW_PATH.name} already exists (rename done)")
        file_renamed = True
    elif OLD_PATH.exists():
        actions.append(f"  RENAME: {OLD_PATH.name} → {NEW_PATH.name}")
        if args.apply:
            text = OLD_PATH.read_text(encoding="utf-8")
            # Rewrite id: and title: in frontmatter
            new_text = text.replace(
                f"id: {OLD_SLUG}\n", f"id: {NEW_SLUG}\n"
            ).replace(
                'title: "Structure Building"\n',
                'title: "Structure Building (Skill)"\n',
            )
            NEW_PATH.write_text(new_text, encoding="utf-8")
            OLD_PATH.unlink()
        file_renamed = True
    else:
        errors.append(f"neither {OLD_PATH.name} nor {NEW_PATH.name} exists")

    # --- step 1b: rewrite inbound wikilinks ---------------------------------
    if file_renamed:
        for fname in INBOUND_FILES:
            path = ENTRIES_DIR / fname
            if not path.exists():
                errors.append(f"inbound file not found: {fname}")
                continue
            text = path.read_text(encoding="utf-8")
            # Replace `[[structure-building]]` and `[[structure-building|...]]`
            # but NOT `[[structure-building-skill...]]` (already migrated).
            new_text = (
                text
                .replace("[[structure-building]]", f"[[{NEW_SLUG}]]")
                .replace("[[structure-building|", f"[[{NEW_SLUG}|")
            )
            if new_text == text:
                actions.append(f"  SKIP (no inbound found): {fname}")
                continue
            n = text.count("[[structure-building]]") + text.count("[[structure-building|")
            actions.append(f"  RELINK: {fname} ({n} link{'s' if n != 1 else ''})")
            if args.apply:
                path.write_text(new_text, encoding="utf-8")

    # --- step 1c: update lens-structure-note's reclassification note --------
    lsn = ENTRIES_DIR / "lens-structure-note.md"
    if lsn.exists():
        text = lsn.read_text(encoding="utf-8")
        # The source file's note still references the old slug at this point;
        # the relink step updates it to `structure-building-skill` on apply.
        # We match against either form so the rewrite is idempotent.
        old_note_v1 = (
            "[[structure-building]] currently lives at `category: concept` "
            "but reads more like a structure note. It is a candidate for "
            "reclassification in a later phase — Phase 5 of the spec migration."
        )
        old_note_v2 = (
            "[[structure-building-skill]] currently lives at `category: concept` "
            "but reads more like a structure note. It is a candidate for "
            "reclassification in a later phase — Phase 5 of the spec migration."
        )
        old_note = old_note_v1 if old_note_v1 in text else old_note_v2
        new_note = (
            "[[structure-building-skill]] is a single cognitive skill (a learner's "
            "ability to extract central ideas and organize them into a coherent "
            "framework). It was renamed during Phase 5a from `structure-building` "
            "to clear the reserved-prefix collision (§6.5); the entry remains "
            "`category: concept` because it describes one principle, not a cluster's "
            "organizing prose."
        )
        if old_note in text:
            actions.append("  RENOTE: lens-structure-note.md (Notes section)")
            if args.apply:
                lsn.write_text(text.replace(old_note, new_note), encoding="utf-8")
        elif new_note in text:
            actions.append("  SKIP (already updated): lens-structure-note.md")
        else:
            actions.append("  SKIP (note not found verbatim): lens-structure-note.md")

    # --- step 2: add `## Lead` to 4 source entries --------------------------
    for fname, lead in SOURCE_LEADS:
        path = ENTRIES_DIR / fname
        if not path.exists():
            errors.append(f"source entry not found: {fname}")
            continue
        text = path.read_text(encoding="utf-8")
        if "## Lead" in text:
            actions.append(f"  SKIP (lead present): {fname}")
            continue
        new_text = insert_lead(text, lead)
        if new_text is None:
            errors.append(f"could not insert lead into {fname}")
            continue
        actions.append(f"  ADD-LEAD: {fname}")
        if args.apply:
            path.write_text(new_text, encoding="utf-8")

    mode = "APPLIED" if args.apply else "DRY RUN"
    print(f"=== phase5a_finish.py [{mode}] ===\n")
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
