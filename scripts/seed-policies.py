#!/usr/bin/env python3
"""
Generate the 22 seed policy entries (§29.2). Each policy is a stub: the body
delegates to the relevant spec section, names the lint rules that enforce it,
and provides a one-paragraph rationale. The spec is the authority during seed
(§1.3); policy bodies are fleshed out as findings accumulate.

Usage:
  python3 scripts/seed-policies.py            # dry run (lists what would be created)
  python3 scripts/seed-policies.py --apply    # write files (refuses to overwrite existing)
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = REPO_ROOT / "wiki" / "entries"
SPEC_REL = "../../docs/spec/specification.md"
TODAY = "2026-04-27"

# Each tuple: (slug, title, spec_section, covers_one_line, linted_by, rationale)
# linted_by is a list of lint-rule names from §20.2 (empty when no specific lint enforces).
POLICIES: list[tuple[str, str, str, str, list[str], str]] = [
    (
        "policy-ingestion",
        "Policy — Ingestion",
        "§17",
        "The four-phase ingestion pipeline (intake, chapter setup, per-sub-section staging, merge, closeout) governs how a raw source becomes vault content.",
        [],
        "A predictable per-chapter cycle keeps a long source from drifting out of sync with the vault's classification and merge rules. The phase boundaries are also the natural points at which lint, structure-note coverage, and notability promotion are run.",
    ),
    (
        "policy-classification",
        "Policy — Classification",
        "§7",
        "Every content entry must be classified by exactly one decision-tree lens, with `classified_by` recording which lens ruled, and the annotation pass must run for every applicable annotation lens.",
        ["classification-consistency", "infrastructure-classified-by-lens", "lens-self-classification"],
        "Classification is auditable only if the deciding lens is recorded. Multiple-lens output, missing `classified_by`, or a lens whose `lens_covers_category` does not match the entry's `category` are all symptoms that the decision tree was not run.",
    ),
    (
        "policy-merge",
        "Policy — Merge",
        "§19",
        "Per-kind merge rules govern how a temp file combines with an existing entry: prose consolidation for `concept` and `insight`, structured append for `entity`, `application`, `process`, replace for `illustration`, append-only sections for `structure-note`, and immutability for runs/findings/discussions/notifications.",
        ["agent-direct-merge", "immutable-merge"],
        "Merge rules protect accumulated connections from being overwritten by fresh blind reads. The append-only convention for `## Connections`, `## Sources`, structure-note `## Load-bearing entries`, etc. is the canonical mechanism.",
    ),
    (
        "policy-lint",
        "Policy — Lint",
        "§20",
        "Every named lint rule is enforced on every write that affects an entry under its scope, on every closeout, and on a daily full pass; advisory findings are recorded for later review while blocking findings stop the offending write or merge.",
        ["slug-uniqueness", "id-filename-mismatch", "unknown-category", "broken-wikilink"],
        "Lint is the vault's continuous self-check. Without lint as a first-class infrastructure citizen, schema drift accumulates silently.",
    ),
    (
        "policy-assessment",
        "Policy — Assessment",
        "§28",
        "Periodic assessment passes compute coverage, internal-consistency, and source-grounding signals; results are recorded in `run-assess-*` entries and projected onto domain dashboards.",
        [],
        "Assessment is how the vault notices its own slow trends — domains saturating, evidence quality drifting, contradictions accumulating. The signals defined here are the early-warning system.",
    ),
    (
        "policy-claim-segmentation",
        "Policy — Claim Segmentation",
        "§10.1.1",
        "A sentence splits into multiple claim entries when it carries multiple independently verifiable assertions, when the assertions are qualified differently, or when the assertion is the locus of a known disagreement; otherwise prefer the coarser claim.",
        [],
        "Atomicity at the wrong scale produces either un-citeable mush (too coarse) or a fog of fragments (too fine). The default of `prefer the coarser claim` errs on the safer side because joining is easier than splitting.",
    ),
    (
        "policy-agent-lifecycle",
        "Policy — Agent Lifecycle",
        "§16.3",
        "An agent's lifecycle has three named protocols: `lifecycle-agent-create`, `lifecycle-agent-mutate`, `lifecycle-agent-retire`; each requires an explicit run entry and (for create/retire) quorum approval.",
        [],
        "Agents are the writes that change the vault's behavior; the lifecycle gates them so a population's composition does not drift quietly.",
    ),
    (
        "policy-archival",
        "Policy — Archival",
        "§26.3",
        "Infrastructure entries (runs, resolved findings, closed discussions, retired notifications) older than 30 days are moved to `wiki/_meta/archive/{kind}/{year}/{month}/`; runs older than 30 days are also rolled up into `run-rollup-{agent}-{period}` summaries.",
        [],
        "Without aggressive archival, the entry pile is dominated by `run-*` and `notification-*` entries within weeks. Content lives forever; infrastructure ages out of the hot index.",
    ),
    (
        "policy-reputation-weighting",
        "Policy — Reputation Weighting",
        "§9.6",
        "Reputation events (gain and loss) and their weights are catalogued here; the external anchor (human review and thesis-eval results) counts for 3× internal-event weight at v0 and is recalibrated annually or when policy-thesis-eval registers a variance-reduction change.",
        [],
        "Reputation drives every edit-hardness gate, so its calibration is itself a load-bearing decision. The external anchor is what keeps in-population events from drifting.",
    ),
    (
        "policy-runtime",
        "Policy — Runtime",
        "§26.6",
        "The `runner/` directory holds the runtime; it is the only enforcer of write-scope, reputation gates, edit-hardness, and pending-changes routing; it does not decide content, classification, or promotion.",
        [],
        "The boundary between vault state (entries) and runtime behavior (the writer-gate) must be sharp; otherwise it becomes impossible to reason about either.",
    ),
    (
        "policy-thesis-eval",
        "Policy — Thesis Evaluation",
        "§28.5",
        "A fixed panel of verifiable tasks is run periodically with and without vault context; the headline metric is variance reduction (var(unaided) − var(vault-augmented)), and the panel is amended only by meta-rule quorum.",
        [],
        "The vault's reason to exist is variance reduction on consequential tasks. The thesis-eval panel keeps that claim falsifiable.",
    ),
    (
        "policy-notability",
        "Policy — Notability",
        "§8",
        "A unit deserves its own entry iff it has multi-source coverage, routing necessity (≥2 inbound), or a policy carve-out; borderline units are staged as `pending-` and either promoted on later inbound link / second source or retired after 90 days.",
        ["notability-stamp-missing"],
        "Without an explicit gate, the vault floods with one-source asides; without explicit promotion, useful borderline units retire silently. This policy makes both paths legible.",
    ),
    (
        "policy-structure-notes",
        "Policy — Structure Notes",
        "§11",
        "A structure note is required for every connected component of >8 content entries; the body must follow the section template (Lead, How the cluster is held together, Load-bearing entries, Subregions, Open questions, Cross-cluster bridges).",
        ["structure-note-coverage", "structure-note-low-link-density"],
        "Big clusters need narrative substrate or they degrade into bag-of-entries. The structure-note pattern is how the vault carries cluster-level information without imposing a hierarchy.",
    ),
    (
        "policy-entry-layout",
        "Policy — Entry Layout",
        "§5",
        "Every entry's body follows the section template appropriate to its kind; a `## Lead` is required when body length exceeds the threshold and unconditionally for structure notes, sources, and entries in contentious domains.",
        ["lead-missing", "lead-too-long", "low-quality-lead", "body-section-order"],
        "Retrieval returns leads first; the lead is therefore a load-bearing artifact, not optional decoration. Section order makes orthogonality predictable for downstream tools.",
    ),
    (
        "policy-high-stakes",
        "Policy — High-Stakes",
        "§14",
        "Claims classified `medical`, `legal`, `safety`, or `identifiable-individual` carry a higher evidence floor; below-floor high-stakes claims are replaced by a placeholder and a blocking finding rather than persisted.",
        ["high-stakes-floor-violation"],
        "The asymmetric removal regime is the wikipedia-MEDRS / BLP analog: weak evidence on consequential claims is more harmful than absence. Better a hole and a finding than a vague assertion.",
    ),
    (
        "policy-contentious-domain",
        "Policy — Contentious Domain",
        "§15",
        "Domains flagged `contentious: true` raise floors across every entry whose `domains` includes them: evidence grade one tier stricter, edit-hardness one tier higher, discussion bound from 5→3 rounds, citation mandatory, lead unconditional.",
        ["evidence-below-floor", "source-missing-contentious", "discussion-round-bound-exceeded"],
        "Contestation merits stricter handling; the elevations make that explicit and consistent across the contentious domain rather than relying on case-by-case judgement.",
    ),
    (
        "policy-pending-changes",
        "Policy — Pending Changes",
        "§9.5",
        "Writes from agents below the relevant edit-hardness threshold land as `pending-{run-id}-{target}` proposals; reviewers (confirmed-and-above) accept, reject, or supersede; unreviewed proposals raise `finding-stale-pending` after 14 days but never auto-accept.",
        ["stale-pending"],
        "Pending changes are how a young population contributes safely. The proposal mechanism preserves the work for review without letting it land before the gate.",
    ),
    (
        "policy-content-quality",
        "Policy — Content Quality",
        "§4.2 and §10",
        "Every claim cites at least one source via `evidence_pointers`; every entry's `confidence` reflects actual cross-source convergence; original research (assertions not traceable to sources) is not added to content entries; framing aspires to neutral point of view, with contestation stamped as `confidence: contested` and elaborated in the body.",
        ["evidence-below-floor", "source-frontmatter-mismatch"],
        "Wikipedia's verifiability + NPOV + no-original-research adapted for an agent-population context. Without these, the population can drift into self-citation cycles.",
    ),
    (
        "policy-rule-promotion",
        "Policy — Rule Promotion",
        "§13.4",
        "An essay promotes to guideline after 3 citations + a closed-resolved discussion + endorsement from one essay-author and one independent agent at reputation ≥60; a guideline promotes to policy after 5 advisory findings citing it + a closed-resolved discussion + meta-rule quorum.",
        [],
        "Promotion paths are the population's mechanism for proposing and ratifying its own rules. The thresholds are placeholders (§35.3) and recalibrate against observed quality.",
    ),
    (
        "policy-edit-hardness",
        "Policy — Edit Hardness",
        "§9",
        "The five tiers (`open`, `confirmed`, `extended-confirmed`, `restricted`, `locked`) gate writes by reputation and (for `extended-confirmed`) declared scope; defaults are set by kind (§9.2), raised by domain inheritance, raised by high-stakes class, and never lowered by ordinary edits.",
        ["edit-hardness-consistency"],
        "Edit-hardness is the population's permission lattice; a tier is a claim about how rare and how scrutinized writes to this entry should be.",
    ),
    (
        "policy-discussions",
        "Policy — Discussions",
        "§22",
        "Discussions are bounded to 5 rounds (3 in contentious domains); termination protocols (`content-quorum`, `meta-rule-quorum`, `human-escalation`, `confirmed-vote`) are selected by the disputed object's kind; discussions inactive past 4 weeks raise `finding-stale-discussion`.",
        ["stale-discussion", "discussion-round-bound-exceeded"],
        "Disputes resolve in finite time or become findings; nothing dangles in chat state. Round bounds force termination; protocols match the gravity of the disputed object.",
    ),
    (
        "policy-reingestion",
        "Policy — Reingestion",
        "§18",
        "A previously-completed chapter may be reingested by reverting its row to `in-progress`, running phases 1–3 fresh, and treating the existing entry as the richer side at merge time (the reingested version is a depth upgrade on prose, not a replacement on connections).",
        [],
        "Reingestion is how a chapter benefits from later context without erasing the connections accumulated since it first ran. The depth-upgrade rule is what makes reingestion safe.",
    ),
]


HEADER_TMPL = """---
id: {slug}
title: "{title}"
category: policy
produced_by: lifecycle-bootstrap
domains: [meta]
tags: [policy, seed]
sources: []
aliases: []
created: {today}
updated: {today}
confidence: high
status: stub
notability_status: n/a
edit_hardness: restricted
high_stakes_class: none
quality: stub
rule_tier: policy
covers: "{covers_one_line}"
linted_by: {linted_by_yaml}
---

# {title}

## Lead

{covers_one_line}

## Rule

The binding rule covered by this policy is specified in [`{spec_rel}`]({spec_rel}) at section **{spec_section}**. Until policy-tier prose is ratified separately, the spec section is authoritative.

## Rationale

{rationale}

## How violation is detected

{lint_section}

## Promotion history

- {today}: created at seed as `policy` (bootstrap; see [`{spec_rel}`]({spec_rel}) §29.2).

## Notes

This entry is a **seed stub**. The spec is the authority during seed (§1.3); this entry exists to make the rule citeable from other entries and to reserve the slug. Flesh out the rule, examples, and edge cases as findings accumulate.
"""


def render_lint_section(linted_by: list[str]) -> str:
    if not linted_by:
        return "_No named lint rule directly enforces this policy in the catalog (§20.2). Violations surface through closeout review or via findings raised by editor or assessment runs._"
    bullets = "\n".join(f"- `{rule}` (§20.2)" for rule in linted_by)
    return f"Lint rules from §20.2 that enforce this policy:\n\n{bullets}"


def render_yaml_list(items: list[str]) -> str:
    if not items:
        return "[]"
    return "[" + ", ".join(items) + "]"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write files")
    args = parser.parse_args()

    if not ENTRIES_DIR.is_dir():
        print(f"error: {ENTRIES_DIR} not found", file=sys.stderr)
        return 1

    created = 0
    skipped_exists = 0
    for slug, title, spec_section, covers, linted_by, rationale in POLICIES:
        path = ENTRIES_DIR / f"{slug}.md"
        if path.exists():
            skipped_exists += 1
            print(f"  SKIP (exists): {slug}")
            continue
        content = HEADER_TMPL.format(
            slug=slug,
            title=title,
            today=TODAY,
            covers_one_line=covers,
            linted_by_yaml=render_yaml_list(linted_by),
            spec_rel=SPEC_REL,
            spec_section=spec_section,
            rationale=rationale,
            lint_section=render_lint_section(linted_by),
        )
        if args.apply:
            path.write_text(content, encoding="utf-8")
            print(f"  WROTE: {slug}")
        else:
            print(f"  WOULD WRITE: {slug}")
        created += 1

    mode = "APPLIED" if args.apply else "DRY RUN"
    print(f"=== seed-policies.py [{mode}] ===")
    print(f"policies in spec list: {len(POLICIES)}")
    print(f"would create / created: {created}")
    print(f"skipped (already exist): {skipped_exists}")
    if not args.apply and created > 0:
        print("\nrun with --apply to write files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
