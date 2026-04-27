#!/usr/bin/env python3
"""
Generate the 13 seed agent-test entries:
  - 8 persona seed tests (§29.7), `authoritative: true`
  - 5 thesis-eval panel tasks (§29.8), `authoritative: true`

Each test names a question and an expected-answer shape. Tests are run as
regressions per §24.3.

Usage:
  python3 scripts/seed-agent-tests.py            # dry run
  python3 scripts/seed-agent-tests.py --apply    # write files
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = REPO_ROOT / "wiki" / "entries"
TODAY = "2026-04-27"

# Persona seed tests (§29.7).
# Each tuple: (slug, agent_target, question, expected_shape)
PERSONA_TESTS: list[tuple[str, str, str, str]] = [
    (
        "agent-test-persona-lt-biological-knowledge",
        "agent-persona-learning-theory",
        "What is the difference between primary and secondary biological knowledge?",
        "Cites [[biologically-primary-and-secondary-knowledge]]; names the distinction (primary: pre-wired, evolutionarily ancient capacities like face-recognition and language; secondary: culturally invented capacities like reading and math, requiring deliberate neural repurposing); references [[david-geary]] as originator.",
    ),
    (
        "agent-test-persona-lt-desirable-difficulty",
        "agent-persona-learning-theory",
        "How does desirable difficulty improve long-term retention?",
        "Cites [[desirable-difficulty]]; describes the mechanism (effortful encoding/retrieval strengthens traces; fluency feels like mastery but produces shallow encoding); references at least one source entry from the [[desirable-difficulty]]'s `sources:` list.",
    ),
    (
        "agent-test-persona-lt-interleaving",
        "agent-persona-learning-theory",
        "What is interleaving, and when is it preferred over blocked practice?",
        "Distinction described (interleaving: mixing problem types within practice; blocked: same type repeatedly); preferred conditions named (when discrimination across problem types matters; when learners need to select strategy, not just execute one); cites [[interleaving]] if it exists, otherwise names the gap.",
    ),
    (
        "agent-test-persona-lt-recall-strength",
        "agent-persona-learning-theory",
        "What does the recall-strength model predict about spaced repetition?",
        "References the recall-strength model entry; describes the prediction (the more effortful the retrieval, the more retention strengthens; weak retrievals reinforce weakly; this implies optimal spacing maximizes effortful-but-successful retrieval); cites [[spaced-repetition]] or names if no entry exists.",
    ),
    (
        "agent-test-persona-lt-goal-vs-intention",
        "agent-persona-learning-theory",
        "What's the difference between a goal and an intention in self-regulation literature?",
        "Distinction drawn (goals: the outcome desired; intentions: a commitment to act, often paired with a when-where cue, as in implementation intentions); key sources cited from the [[self-regulation]] domain.",
    ),
    (
        "agent-test-persona-lt-working-memory-pedagogy",
        "agent-persona-learning-theory",
        "What is the role of working memory in pedagogy?",
        "Causal relationship described (working-memory capacity bottlenecks how much new information a learner can integrate at once; cognitive load theory derives instructional moves from this constraint — worked examples, scaffolding, sequencing); cites at least one of [[working-memory]], a `cognitive-load-theory` entry, or equivalent.",
    ),
    (
        "agent-test-persona-lt-study-strategies",
        "agent-persona-learning-theory",
        "Name three distinct study strategies and their trade-offs.",
        "Three concrete strategies (e.g., retrieval practice, spaced practice, interleaving, elaborative interrogation, dual coding); each with at least one trade-off (effort cost, fluency illusion mismatch, expertise reversal, etc.); cites at least one strategy's entry.",
    ),
    (
        "agent-test-persona-lt-multitasking",
        "agent-persona-learning-theory",
        "Is multi-tasking effective for learning?",
        "Clear no; with evidence (task-switching costs, attention-residue, working-memory partition); cites [[einstellung]] or attention-related entries; names whether the vault has a dedicated entry on multi-tasking and learning, opening a question if not.",
    ),
]

# Thesis-eval panel tasks (§29.8).
# Each tuple: (slug, question, expected_shape)
THESIS_EVAL_TASKS: list[tuple[str, str, str]] = [
    (
        "agent-test-thesis-eval-spaced-repetition-mechanism",
        "Describe the mechanism by which spaced repetition produces stronger long-term retention than massed practice.",
        "Names the encoding-retrieval gap; describes how spacing introduces forgetting that, when followed by successful retrieval, strengthens consolidation more than massed repetition; cites primary-literature sources where available; resolves with at least an A- or B-grade reference.",
    ),
    (
        "agent-test-thesis-eval-primary-secondary-implications",
        "List three pedagogical implications of the primary/secondary biological knowledge distinction.",
        "Three defensible practices (e.g., scaffold secondary material more than primary; expect productive struggle for secondary; use guided rather than discovery instruction for novices; leverage primary capacities like social interaction as a vehicle for secondary content); cites [[biologically-primary-and-secondary-knowledge]] and [[david-geary]].",
    ),
    (
        "agent-test-thesis-eval-difficulty-testing",
        "What is the relationship between desirable difficulty and the testing effect?",
        "Cites both ([[desirable-difficulty]], [[testing-effect]]); names the connection (the testing effect is one mechanism by which desirable difficulty produces stronger learning — effortful retrieval is itself a desirable difficulty; the testing effect's strength scales with retrieval effort, consistent with the desirable-difficulty framework).",
    ),
    (
        "agent-test-thesis-eval-basal-ganglia",
        "Describe the role of the basal ganglia in skill acquisition.",
        "Names basal-ganglia involvement in procedural learning (action selection, stimulus-response associations, habit formation, reinforcement-based selection of motor programs); distinguishes from declarative-system roles; cites primary literature; if the vault lacks the explicit entry, names the gap.",
    ),
    (
        "agent-test-thesis-eval-declarative-procedural",
        "Explain why declarative learning and procedural learning have different forgetting curves.",
        "Names both systems ([[declarative-learning-system]], [[procedural-learning-system]]); names the distinction (declarative: rapid hippocampal indexing, susceptible to interference and relatively rapid decay without retrieval; procedural: slow incremental tuning of basal-ganglia/cerebellar pathways, much more durable once consolidated); cites the [[declarative-procedural-seesaw]] or equivalent.",
    ),
]


PERSONA_TMPL = """---
id: {slug}
title: "Agent Test — {short_title}"
category: agent-test
produced_by: lifecycle-agent-test-create
domains: [meta]
tags: [agent-test, persona, seed, authoritative]
sources: []
aliases: []
created: {today}
updated: {today}
confidence: high
status: complete
notability_status: n/a
edit_hardness: extended-confirmed
high_stakes_class: none
quality: c
agent: "[[{agent_target}]]"
question: "{question}"
expected_shape: "{expected_short}"
authoritative: true
last_run: null
last_result: stale
---

# Agent Test — {short_title}

## Lead

Authoritative seed test for [[{agent_target}]]. Measures whether the persona can answer the question below in the expected shape using only its declared read slice.

## Question

{question}

## Expected answer shape

{expected_full}

## Notes

This test is `authoritative: true` (§24.2.1) — its failure is a blocking finding (§24.4). It is run on every closeout that touches an entry in the persona's slice and on the daily schedule.
"""

THESIS_TMPL = """---
id: {slug}
title: "Agent Test — Thesis Eval — {short_title}"
category: agent-test
produced_by: lifecycle-agent-test-create
domains: [meta]
tags: [agent-test, thesis-eval, seed, authoritative]
sources: []
aliases: []
created: {today}
updated: {today}
confidence: high
status: complete
notability_status: n/a
edit_hardness: extended-confirmed
high_stakes_class: none
quality: c
agent: "[[policy-thesis-eval]]"
question: "{question}"
expected_shape: "{expected_short}"
authoritative: true
last_run: null
last_result: stale
---

# Agent Test — Thesis Eval — {short_title}

## Lead

Thesis-eval panel task per [[policy-thesis-eval]] (§28.5). The panel compares an unaided baseline (model answers without vault context) against vault-augmented runs (model answers with retrieved context); the headline metric is variance reduction.

## Question

{question}

## Expected answer shape

{expected_full}

## Baselines

- **Unaided:** TBD — to be recorded once during seed by running a baseline model N times against this question with no vault context. Variance over N runs is the reference variance.
- **Vault-augmented:** TBD — to be re-run periodically (per [[policy-assessment]] cadence). Per-run variance is compared to the unaided baseline; reduction is logged in the thesis-eval dashboard.

## Notes

This task is `authoritative: true`. Amendments to the panel itself require meta-rule quorum (§9.4). Per-task amendments may be made via the same rule.
"""


def short_title_from_slug(slug: str) -> str:
    # Drop the "agent-test-" prefix and any "persona-lt-" or "thesis-eval-" prefix
    s = slug
    for prefix in ("agent-test-", "persona-lt-", "thesis-eval-"):
        if s.startswith(prefix):
            s = s[len(prefix):]
    return s.replace("-", " ").title()


def yaml_safe(s: str) -> str:
    """Escape double quotes for inclusion in a YAML double-quoted string."""
    return s.replace('"', '\\"')


def shorten_for_yaml(s: str, limit: int = 200) -> str:
    if len(s) <= limit:
        return s
    return s[: limit - 1].rsplit(" ", 1)[0] + "…"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    if not ENTRIES_DIR.is_dir():
        print(f"error: {ENTRIES_DIR} not found", file=sys.stderr)
        return 1

    written = 0
    skipped = 0

    # persona tests
    for slug, agent_target, question, expected in PERSONA_TESTS:
        path = ENTRIES_DIR / f"{slug}.md"
        if path.exists():
            print(f"  SKIP (exists): {slug}")
            skipped += 1
            continue
        content = PERSONA_TMPL.format(
            slug=slug,
            today=TODAY,
            short_title=short_title_from_slug(slug),
            agent_target=agent_target,
            question=yaml_safe(question),
            expected_short=yaml_safe(shorten_for_yaml(expected)),
            expected_full=expected,
        )
        if args.apply:
            path.write_text(content, encoding="utf-8")
            print(f"  WROTE: {slug}")
        else:
            print(f"  WOULD WRITE: {slug}")
        written += 1

    # thesis-eval tasks
    for slug, question, expected in THESIS_EVAL_TASKS:
        path = ENTRIES_DIR / f"{slug}.md"
        if path.exists():
            print(f"  SKIP (exists): {slug}")
            skipped += 1
            continue
        content = THESIS_TMPL.format(
            slug=slug,
            today=TODAY,
            short_title=short_title_from_slug(slug),
            question=yaml_safe(question),
            expected_short=yaml_safe(shorten_for_yaml(expected)),
            expected_full=expected,
        )
        if args.apply:
            path.write_text(content, encoding="utf-8")
            print(f"  WROTE: {slug}")
        else:
            print(f"  WOULD WRITE: {slug}")
        written += 1

    mode = "APPLIED" if args.apply else "DRY RUN"
    print(f"=== seed-agent-tests.py [{mode}] ===")
    print(f"persona tests:    {len(PERSONA_TESTS)}")
    print(f"thesis-eval:      {len(THESIS_EVAL_TASKS)}")
    print(f"would create / created: {written}")
    print(f"skipped (already exist): {skipped}")
    if not args.apply and written > 0:
        print("\nrun with --apply to write files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
