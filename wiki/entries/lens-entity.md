---
id: lens-entity
title: "Lens — Entity"
category: lens
classified_by: lens-lens
domains: [meta]
tags: [classification, reference]
sources: []
aliases: []
created: 2026-04-21
updated: 2026-04-21
confidence: high
status: complete
lens_question: "Is the subject a proper noun — a person, institution, named theory, framework, or method?"
lens_priority: 40
lens_covers_category: entity
lens_criteria:
  - "The entry's subject is a proper noun: a person, institution, named theory, framework, or method."
  - "The note is about the entity itself — who or what it is and why it matters — not about the ideas it produced."
  - "Body is reference-card shaped: brief description, key contributions, mentions, pointers to concept notes."
  - "Frontmatter declares `entity_kind`."
notability_status: n/a
edit_hardness: restricted
high_stakes_class: none
quality: c
produced_by: lifecycle-bootstrap
---

# Lens — Entity

## Question

Is the subject a proper noun — a person, institution, named theory, framework, or method?

## How to apply

An entity entry is a reference card. The person (or institution, or framework) is the subject; the ideas they contributed live in their own concept notes linked from `## Key contributions`.

If the note is *about Robert Bjork*, it's an entity. If the note is *about desirable difficulty* (the principle he coined), it's a concept — even though Bjork is mentioned.

Valid `entity_kind` values: `person`, `institution`, `theory`, `framework`, `method`.

A named theory or framework counts as an entity when the note is a reference card about the theory's origin, authorship, and scope. The *content* of the theory lives in one or more concept notes the entity links to.

## Worked matches

- [[robert-bjork]] — a person. Has key contributions; pointers to [[desirable-difficulty]] and related concepts.
- [[eric-mazur]] — a person. Contributed peer instruction, whose mechanism lives in its own concept note.
- Any `entity_kind: institution` entry for a named research lab or school.

## Worked non-matches

- [[desirable-difficulty]] — the *idea* Bjork coined, not Bjork the person. Route to [[lens-concept]].
- [[testing-effect]] — a named cognitive phenomenon, not a proper noun for an entity. Route to [[lens-concept]].
- [[make-it-stick]] — a book, not a person/institution/theory. Route to [[lens-source]].

## Related lenses

- Meta-lens: [[lens-lens]]
- Previous lens in priority: [[lens-application]]
- Next lens in priority: [[lens-process]]
- Routes away to: [[lens-concept]], [[lens-source]].
