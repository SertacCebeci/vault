---
id: guideline-cluster-organization
title: "Guideline — Cluster Organization"
category: guideline
produced_by: lifecycle-bootstrap
domains: [meta]
tags: [guideline, structure-notes, clusters, seed]
sources: []
aliases: []
created: 2026-04-27
updated: 2026-04-27
confidence: high
status: stub
notability_status: n/a
edit_hardness: extended-confirmed
high_stakes_class: none
quality: stub
rule_tier: guideline
covers: "When to write a structure note: cluster size >8 entries, cluster bridges multiple domains, or cluster has accumulated unresolved tensions worth naming."
linted_by: ["structure-note-coverage"]
---

# Guideline — Cluster Organization

## Lead

Write a structure note when a cluster of related entries grows past ~8 members, when a cluster bridges multiple domains, or when the cluster has accumulated unresolved tensions worth naming. Per-domain frames may each have their own structure note for the same cluster — that is the intended pattern.

## Recommendation

A structure note adds value when:

1. **Size threshold reached.** A connected component of >8 entries linked by wikilinks. Below this, the wikilinks themselves carry the structure; above it, the cluster gets hard to navigate without a summary.
2. **Domain bridging.** The cluster spans two or more domains and a domain-frame view is useful from each side. In this case, write *multiple* structure notes — one per `domain_frame` — rather than try to make one structure note describe everything (§11.3).
3. **Unresolved tension.** The cluster has accumulated `confidence: contested` entries, open questions, or competing framings. The structure note's `## How the cluster is held together` section is the natural home for naming the tension.

A structure note is **not** the right answer when:

- The cluster is small (<5 entries) — a high-quality `insight` entry is enough.
- The cluster is really one extended concept that should be one entry — split entries first, then revisit.
- The cluster is a hierarchy disguised — Wikipedia-style parent articles. Resist; write peer structure notes by frame instead.

## Rationale

Structure notes are how the vault carries cluster-level information without imposing a hierarchy. The lint rule `structure-note-coverage` raises an advisory finding for clusters over the size threshold without one — that is the operationalization of this guideline.

## Examples

- Pass: A `structure-memory-learning-theory` covering encoding/consolidation/retrieval/forgetting from the cognitive frame; a peer `structure-memory-neuroscience` covering the same cluster from the brain frame.
- Fail (over-structuring): A structure note for a 4-entry cluster on a single sub-topic. The cluster is small enough that the four entries' connections speak for themselves.

## Notes

When in doubt, write a `## How the cluster is held together` paragraph inside the largest concept entry first. If that paragraph keeps growing or starts repeating across multiple entries, promote it to a structure note.
