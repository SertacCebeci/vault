---
id: lens-source
title: "Lens — Source"
category: lens
classified_by: lens-lens
domains: [meta]
tags: [classification, literature]
sources: []
aliases: []
created: 2026-04-21
updated: 2026-04-21
confidence: high
status: complete
lens_question: "Is this entry a literature note about a specific raw source document?"
lens_priority: 10
lens_covers_category: source
lens_criteria:
  - "The entry is a synthesized literature note summarizing one raw source document (book, paper, transcript, MOOC, etc.)."
  - "Frontmatter declares `author`, `year`, `source_file`, and `date_ingested`."
  - "Body has sections along the lines of Summary, Key ideas, Notable claims, Questions raised, Connections."
---

# Lens — Source

## Question

Is this entry a literature note about a specific raw source document?

## How to apply

A source entry is the synthesized counterpart to an immutable raw document under `raw/`. It is the only category whose entries *are* about a specific book/paper — every other category synthesizes source-independent knowledge and cites sources via the `sources` frontmatter field.

Apply by checking:

1. The entry summarizes one specific document (one book, one paper, one transcript).
2. Its frontmatter points at a file under `raw/` via `source_file`.
3. The body discusses *the source itself* — its thesis, methodology, key ideas, notable claims — rather than the topic the source is about.
4. Other entries reference this entry via `sources: [[this-slug]]`.

If all four hold, category is `source`. Otherwise, the entry synthesizes a topic across (possibly many) sources — route to a later lens.

## Worked matches

- [[make-it-stick]] — literature note on Brown, Roediger & McDaniel (2014). Points to `raw/make-it-stick/make-it-stick.pdf`. Body covers the book's thesis and chapter-by-chapter ideas.
- [[learning-how-to-learn]] — literature note on the Oakley/Sejnowski Coursera MOOC.

## Worked non-matches

- [[desirable-difficulty]] — a concept the source *discusses*, not a literature note about the source. Route to [[lens-concept]].
- [[beanbag-toss-study]] — a specific study *reported in* a source, not a summary of the source itself. Route to [[lens-illustration]].

## Related lenses

- Meta-lens: [[lens-lens]]
- Next lens in priority order: [[lens-illustration]]
- Routes away to: every other lens if the entry is topic-about rather than source-about.
