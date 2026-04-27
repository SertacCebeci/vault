#!/usr/bin/env python3
"""
Phase 5b — first scoped pass: insert `## Lead` sections into the 10 legacy
concept entries that the persona's seed tests and thesis-eval panel reach.
These are the entries where retrieval quality matters most for the v0
thesis-eval baseline run.

The remaining ~159 advisory `lead-missing` findings on legacy concepts can
be cleared via subsequent scoped passes (or, by policy, on-touch as those
entries are otherwise edited).

Idempotent: re-running after apply is a no-op (each insert checks for an
existing `## Lead` section first).

Usage:
  python3 scripts/phase5b_hot_leads.py            # dry run
  python3 scripts/phase5b_hot_leads.py --apply    # write changes
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = REPO_ROOT / "wiki" / "entries"

LEADS: list[tuple[str, str]] = [
    (
        "biologically-primary-and-secondary-knowledge.md",
        "Geary's evolutionary distinction: biologically *primary* abilities (face recognition, first-language acquisition, basic social interaction) are pre-wired and emerge without instruction; biologically *secondary* abilities (reading, writing, mathematics, formal reasoning) require the brain to repurpose evolutionarily older circuits and demand deliberate teaching. The implication for instruction: secondary material genuinely needs scaffolding because the brain was not designed to learn it on its own.",
    ),
    (
        "desirable-difficulty.md",
        "Learning is deeper and more durable when it requires effort. Strategies that feel easy and productive — re-reading, massed practice, cramming — produce a feeling of fluency that masquerades as mastery but fades quickly; effortful strategies like spacing, interleaving, and retrieval practice feel slower but produce stronger and longer-lasting learning. Coined by the Bjorks; the difficulty must be one the learner can overcome through increased effort, otherwise it becomes undesirable.",
    ),
    (
        "declarative-learning-system.md",
        "The neural pathway by which the brain consciously learns facts and events: working memory deposits new information into both the neocortex (the slow but vast permanent store) and the hippocampus (the fast but superficial indexer); consolidation gradually transfers reliance from the hippocampal index to direct neocortical access. The seesaw partner of the procedural-learning system.",
    ),
    (
        "declarative-procedural-seesaw.md",
        "The two learning systems behave like a seesaw: when one is actively engaged, the other is de-emphasized. Once both have learned the same material, the resulting knowledge is complementary — declarative is flexible but slow, procedural is fast but inflexible, and material learned through both is more durable and adaptable than either alone. Implication for teaching: alternate explanation (declarative) and practice (procedural) phases rather than relying on either exclusively.",
    ),
    (
        "einstellung.md",
        "A cognitive roadblock installed by your own expertise: an existing well-developed approach prevents you from finding a better one. The remedy pair is the diffuse mode (stepping back to let attention wander) and interleaving (training flexible selection among approaches rather than defaulting to a single one). Especially relevant where paradigm shifts are needed; explains why outsiders often see solutions experts cannot.",
    ),
    (
        "interleaving.md",
        "Mixing different problem types or concepts during practice rather than repeating the same thing in blocks. Slows the in-session feeling of fluency but produces stronger long-term retention and — most distinctively — builds the discrimination skill of knowing *which* approach to use when. Especially powerful for somewhat-similar categories (preterite vs. imperfect tenses, seal vs. sea lion); less useful for obviously distinct ones.",
    ),
    (
        "procedural-learning-system.md",
        "The brain's second pathway to long-term memory, operating largely outside conscious awareness through the basal ganglia. Unlike the declarative system, it does not route through working memory or the hippocampus: sensory input feeds the basal-ganglia loop directly, building habits, language fluency, motor skills, and intuitive pattern recognition through extensive practice rather than explicit instruction.",
    ),
    (
        "spaced-repetition.md",
        "Reviewing material at increasing intervals rather than massing it. Each retrieval-and-reconsolidation cycle strengthens synaptic connections, and the gaps between sessions let those connections rearrange into simpler, more durable configurations — like letting each layer of brick set before adding the next. The mechanism by which most enduring learning is built; the empirical case for it is among the strongest in cognitive psychology.",
    ),
    (
        "testing-effect.md",
        "The robust empirical finding that actively pulling information out of memory strengthens that knowledge and makes it more durable than additional study does. Testing is not just a dipstick for measuring learning — it is itself one of the most powerful learning events available. Triggered by any retrieval activity (oral quiz, short-answer, silent recall), not only formal exams; the empirical backbone of retrieval practice as a study strategy.",
    ),
    (
        "working-memory.md",
        "The brain's system for temporarily holding and manipulating a small number of items (typically about four) while actively thinking with them. Operates like an octopus juggling balls between the front of the brain and the back; items vanish when juggling stops or when the system is overwhelmed. The bottleneck that cognitive load theory builds its instructional moves around.",
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

    for fname, lead in LEADS:
        path = ENTRIES_DIR / fname
        if not path.exists():
            errors.append(f"missing entry: {fname}")
            continue
        text = path.read_text(encoding="utf-8")
        if "## Lead" in text:
            actions.append(f"  SKIP (lead present): {fname}")
            continue
        new_text = insert_lead(text, lead)
        if new_text is None:
            errors.append(f"could not insert lead into {fname} (no `## Section` heading found)")
            continue
        actions.append(f"  ADD-LEAD: {fname}")
        if args.apply:
            path.write_text(new_text, encoding="utf-8")

    mode = "APPLIED" if args.apply else "DRY RUN"
    print(f"=== phase5b_hot_leads.py [{mode}] ===\n")
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
