---
id: guideline-prose-style
title: "Guideline — Prose Style"
category: guideline
produced_by: lifecycle-bootstrap
domains: [meta]
tags: [guideline, voice, style, seed]
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
covers: "Voice and register conventions: source-agnostic prose for `concept`/`insight`/`entity`/`process`/`application`; story-style narrative permitted in `illustration`; no first-person, no meta phrasing about the entry itself."
linted_by: []
---

# Guideline — Prose Style

## Lead

Write entry bodies in clear, source-agnostic prose. Reserve narrative storytelling for `illustration` entries; everywhere else, the prose should describe the subject directly without referring to the entry, the chapter it came from, or the book that mentioned it.

## Recommendation

For `concept`, `insight`, `entity`, `process`, `application`:

- **Source-agnostic.** No "this chapter argues" / "the book describes" / "as introduced in §3". Source attribution lives in `## Sources` and frontmatter.
- **No first person.** Avoid "we", "our", "I". Use third person or impersonal voice.
- **No meta phrasing about the entry.** "This entry covers…" / "Below we discuss…" — drop these. Just say the thing.
- **Definite over hedging.** When the evidence is settled, state it; when contested, set `confidence: contested` and describe the contestation.
- **Active voice when the subject is doing the action.** Passive voice is fine for genuinely passive constructions.

For `illustration`:

- Story style is permitted — protagonist, setting, outcome, drawn from the source.
- Quote sparingly; synthesize most of the time even here.
- The illustration is *about* the protagonist's experience; the abstraction goes in the linked concept(s) listed in `illustrates`.

For `source` entries:

- Write *about* the source — its thesis, methodology, key ideas, notable claims.
- It is the only kind of entry that may discuss the source as an object.

For policy/guideline/essay entries:

- Normative voice is permitted ("editors must…", "an entry should…").

## Rationale

Source-agnostic prose lets entries accumulate citations from multiple sources without rewriting. Meta phrasing ("this entry") rots when the entry is split, merged, or reorganized. First-person voice presumes a single author the vault rarely has.

## Examples

- Pass: "Spaced practice produces stronger long-term retention than massed practice." (definite, source-agnostic)
- Fail: "We learn from Make It Stick that spaced practice produces stronger long-term retention." (source-attached, first-person)
- Pass (illustration): "On the morning of November 7, the choir's tenor section…" (narrative)

## Notes

A guideline; violations are advisory. Each illustration is granted the latitude it needs for narrative effectiveness; meta phrasing is the easier-to-flag pattern in lint.
