---
id: lens-policy-tier
title: "Lens — Policy Tier"
category: lens
classified_by: lens-lens
domains: [meta]
tags: [classification, rules, governance]
sources: []
aliases: []
created: 2026-04-27
updated: 2026-04-27
confidence: high
status: complete
notability_status: n/a
edit_hardness: restricted
high_stakes_class: none
quality: c
produced_by: lifecycle-bootstrap
lens_question: "Is this entry a rule about how the vault works, and which tier of binding force does it carry?"
lens_priority: 5
lens_covers_category: [policy, guideline, essay]
lens_kind: decision-tree
lens_criteria:
  - "The body is normative — it states how editors, agents, or the vault must behave; it does not assert empirical facts about a subject the vault studies."
  - "The slug uses one of the reserved prefixes `policy-`, `guideline-`, or `essay-`."
  - "A sub-decision determines tier: blocking-finding-on-violation → `policy`; advisory-finding-on-violation → `guideline`; under-development with no enforcement → `essay`."
  - "Tier transitions happen via `policy-rule-promotion` (§13.4), not by ordinary edits to this entry."
---

# Lens — Policy Tier

## Question

Is this entry a rule about how the vault works, and which tier of binding force does it carry?

## How to apply

Run after [[lens-lens]] (priority 0) and before [[lens-source]] (priority 10). This lens fires for every entry whose work is *normative* — telling the population how to act — rather than *descriptive* of some subject the vault studies. If the entry asserts how spaced practice affects retention, it is a `concept`; if the entry asserts that editors must cite sources for every claim in a contentious domain, this lens fires.

When the lens matches, walk a sub-decision tree to pick the tier (per §13.2):

1. Does the rule, when violated, produce a **blocking** finding that prevents the merge or downgrades quality? → `policy`.
2. Does the rule, when violated, produce an **advisory** finding that does not block but is reviewed? → `guideline`.
3. Is the rule under development, explicitly not yet ratified, binding nothing? → `essay`.

The tier shows up in three places: the `category` field, the slug prefix, and the `rule_tier` extension field. All three must agree. Promotion across tiers is a separate event handled by `policy-rule-promotion` and is recorded in the entry's `promotion_history`.

## Worked matches

- `policy-ingestion` — rule covering the four-phase ingestion pipeline; violations block the closeout. Tier: `policy`.
- `guideline-naming-slugs` — preferred slug-naming patterns; violations produce advisory findings. Tier: `guideline`.
- `essay-when-to-promote-borderline` — observation about borderline-notability units gaining inbound links; binds nothing. Tier: `essay`.

## Worked non-matches

- [[desirable-difficulty]] — describes a learning-theory phenomenon, not a rule. Route to [[lens-concept]].
- [[make-it-stick]] — synthesized literature note about a book. Route to [[lens-source]].
- An entry titled "Why we cite primary sources" that happens to discuss the *value* of citation but does not normatively prescribe behavior — route to [[lens-concept]] or [[lens-insight]] depending on shape.

## Notes

`lens_covers_category` is multi-valued for this lens — an exception in §7.2 — because a single sub-decision tree resolves to one of three categories. `classified_by` on the resulting entry is `lens-policy-tier` regardless of which sub-tier won.

## Related lenses

- Meta-lens: [[lens-lens]]
- Previous lens in priority: [[lens-lens]]
- Next lens in priority: [[lens-source]]
