# Vault — LLM Wiki Schema

You are maintaining a **Zettelkasten-style knowledge wiki** stored as a single flat vault. Every entry — concept, entity, illustration, application, insight, process, source, *and* the category-defining lenses themselves — is a markdown file under `wiki/entries/`. Category is a frontmatter field assigned by a lens, not a directory.

For architectural rationale see [`../../docs/intent/2026-04-21-vault-architecture.md`](../../docs/intent/2026-04-21-vault-architecture.md) (long-form) and the migration plan at [`../../docs/plans/2026-04-21-vault-migration.md`](../../docs/plans/2026-04-21-vault-migration.md).

## Project intent

This wiki is a compounding knowledge graph built through disciplined ingestion. The user feeds in sources; the system ingests them chapter by chapter, producing densely linked entries and maintaining indexes.

- If a source is organized into chapters, a normal ingestion request means **one chapter per turn** unless the user explicitly asks for more.
- If an ingestion tracker already exists for that source, a generic ingestion request means **resume or reconcile**, not restart.

## Directory structure

```
raw/                       # Per-source folders — one folder per source, named by source slug
  {source-slug}/
    {source-slug}.md       # The source document (immutable — never modify)
    {source-slug}-process-trace.md   # Ingestion tracker for this source
    assets/                # Optional: images/attachments extracted from or supporting the source
temp/                      # Ephemeral per-chapter staging; flat; cleared between chapters
wiki/
  entries/                 # EVERY knowledge entry lives here, flat, one file per slug
  _meta/
    index.md               # Main index — catalog of every entry, grouped by category
    log.md                 # Chronological activity log
    overview.md            # Narrative map (not an enumerative catalog)
    indexes/               # Per-domain indexes
      learning-theory.md
      neuroscience.md
      pedagogy.md
      self-regulation.md
      assessment.md
      meta.md
```

- `wiki/entries/` is the only flat pile. Readers do not need to know about paths — category is in frontmatter.
- `wiki/_meta/` is structural pages *about* the vault, not knowledge entries *in* the vault.
- `raw/` and `temp/` are outside `wiki/` and are not indexed. Each source lives in its own folder under `raw/` alongside its process trace.
- Indexing glob for the qmd collection: `wiki/**/*.md` (matches entries + meta, excludes raw/temp).

## Zettelkasten principles

1. **Atomicity.** One idea per entry. If an entry covers two ideas, split it.
2. **Connectivity over hierarchy.** The value is in links between entries. Every entry must link to at least one other entry.
3. **Synthesize; don't paste.** Never copy-paste from sources. Source entries cite; other entries synthesize.
4. **Link density.** Use `[[wikilinks]]` liberally. Slugs are globally unique so bare-slug links resolve anywhere.
5. **Emergence.** Let structure emerge from connections. The overview page tracks the emerging narrative; lenses track the classification meta.

## Canonical frontmatter schema

Every entry under `wiki/entries/` carries this head:

```yaml
---
id: desirable-difficulty              # must equal filename without .md
title: "Desirable Difficulty"
category: concept                     # lens | source | concept | entity | illustration |
                                      #   application | insight | process
classified_by: lens-concept           # slug of the lens that assigned category
domains: [learning-theory]            # 1..N enumerated domain slugs; NEVER empty
tags: [effort, memory, encoding]      # free-form, lowercase, hyphenated
sources: [make-it-stick]              # bare slugs of source-category entries
aliases: []                           # optional search aliases
created: 2026-04-15
updated: 2026-04-21
confidence: high                      # high | medium | low | contested
status: complete                      # draft | stub | complete
---
```

### Category-specific extensions

- **Lens** (`category: lens`): `lens_question` (non-empty string), `lens_priority` (integer), `lens_covers_category` (single category slug), `lens_criteria` (list of checklist items). See any file matching `wiki/entries/lens-*.md`.
- **Source** (`category: source`): `author`, `year`, `source_file` (path `raw/{slug}/{slug}.md`), `date_ingested`.
- **Entity** (`category: entity`): `entity_kind` ∈ `person | institution | theory | framework | method`.
- **Illustration** (`category: illustration`): `source: "[[source-slug]]"` (quoted wikilink), `illustrates: [concept-slug, …]`, `chapter`, `pages`.
- **Application** (`category: application`): `applies: [concept-slug, …]`.
- **Insight** (`category: insight`): `connects: [concept-slug, …]`.
- **Process** (`category: process`): `stages: [stage-slug, …]` (order matters).
- **Concept** (`category: concept`): no additional required fields.

### Rules

- `id` equals filename without `.md`.
- `category` is always the output of a lens decision; never set by hand without also recording `classified_by`.
- `domains` is mandatory and non-empty. Every entry must appear in at least one domain index.
- `sources` (frontmatter) is the machine-readable shorthand; the body's `## Sources` section is the rich attribution with page ranges.
- `status: stub` marks thin or draft entries; `complete` marks ratified ones. Lint uses this.
- `confidence: contested` flags entries where the source material or the classification itself is in active revision.

## Categories are lens-assigned — not hand-picked

Each category has a dedicated lens entry under `wiki/entries/lens-{category}.md`. The lens is itself a wiki entry: its frontmatter declares the question it asks, its priority in the decision tree, and the category it covers; its body lays out criteria and worked examples.

### The lens set (priority order)

| slug | covers | priority | question |
|------|--------|---------:|----------|
| [[lens-lens]] | `lens` | 0 | Is this entry itself a lens? |
| [[lens-source]] | `source` | 10 | Is this a literature note about one raw document? |
| [[lens-illustration]] | `illustration` | 20 | Does it have protagonist, setting, outcome — a story? |
| [[lens-application]] | `application` | 30 | Could a practitioner follow this as instructions? |
| [[lens-entity]] | `entity` | 40 | Is the subject a proper noun? |
| [[lens-process]] | `process` | 50 | Multi-stage sequence with transitions? |
| [[lens-insight]] | `insight` | 60 | Requires naming 2+ concepts and their relationship? |
| [[lens-concept]] | `concept` | 99 | Otherwise: one idea, explained on its own terms. |

When a lens's rule evolves, edit the lens's body — not this file. This file names the lenses; the lenses carry the rules.

### Classification protocol

When authoring a new entry:

1. Draft body + canonical frontmatter (everything except `category` and `classified_by`).
2. Apply the decision tree:
   - Apply [[lens-lens]] first. If match → `category: lens`, `classified_by: lens-lens`, done.
   - Else iterate the remaining lenses in ascending `lens_priority`. Read each lens's criteria; first match wins. Set `category` to that lens's `lens_covers_category`; set `classified_by` to that lens's slug.
3. If no lens matches (rare — [[lens-concept]] at priority 99 is the catch-all), escalate to the user. This signals a gap that warrants a new lens or an updated criterion.

This protocol is deterministic given a stable lens set, and auditable: `classified_by` records which lens ruled, so a future reader can trace the decision back to the lens's current body.

## Domains — the orthogonal axis

Categories answer "what kind of thing is this". Domains answer "what subject area does this belong to". They are orthogonal: one entry may be `category: concept`, `domains: [learning-theory, neuroscience]`.

Valid domains at any time are exactly the set of files in `wiki/_meta/indexes/`. Seed domains:
- `learning-theory` — cognitive mechanisms of learning
- `neuroscience` — brain mechanisms underlying learning
- `pedagogy` — teaching practice and instructional design
- `self-regulation` — metacognition, procrastination, habit, motivation
- `assessment` — testing, feedback, calibration
- `meta` — entries about the wiki itself (lenses, indexes)

Adding a new domain means creating a new index file under `wiki/_meta/indexes/{domain}.md`. Removing one means reassigning every entry that claimed it.

## Index files

Three structural files under `wiki/_meta/`, all hand-authored and maintained:

- **`wiki/_meta/index.md`** — master catalog of every entry, grouped by category, with domain tags inline and a one-line description where available.
- **`wiki/_meta/indexes/{domain}.md`** — per-domain catalog; lists every entry whose `domains` frontmatter includes this domain, grouped by category.
- **`wiki/_meta/overview.md`** — narrative prose map. Not a catalog; it captures synthesis across entries.
- **`wiki/_meta/log.md`** — chronological activity log, append-only.

Indexes are rebuilt by `pnpm build:vault-indexes` (walks `wiki/entries/`, reads each frontmatter, emits the catalog files). Regenerate after any Phase 3 closeout, or by hand if only a few entries changed.

## Ingestion workflow

Each chapter is processed in four phases: **Setup**, **Stage** (per sub-section), **Merge**, **Closeout**.

### Phase 0 — Setup

1. Mark the chapter row `in-progress` in the process trace at `raw/{source-slug}/{source-slug}-process-trace.md`.
2. Clear `temp/` — delete all files under `temp/`, preserving the directory.
3. Read the chapter, identify 2–5 coherent sub-sections based on topic boundaries. Scale with length (≤25 pp: 2; 25–40: 2–3; 40–60: 3–5; >60: 4–5).
4. Record sub-sections in the tracker as nested rows.
5. Create `temp/_staging-index.md` (underscore-prefix avoids collisions with entry slugs).

### Phase 1 — Stage (per sub-section)

For each sub-section, in order:

1. Read the sub-section.
2. For each knowledge unit, draft body + canonical frontmatter.
3. Run the decision tree (§Classification protocol) to set `category` and `classified_by`.
4. Pick a slug. Check it against:
   - existing filenames in `wiki/entries/`
   - already-staged filenames in `temp/`

   Map each slug to:
   - `new` — no match anywhere
   - `merges-with: {existing-slug}` — a `wiki/entries/` file exists; stage under the same slug in `temp/` so Merge matches
   - `extends: {temp-slug}` — a `temp/` file from a prior sub-section covers this topic; enrich in place
5. **Write into `temp/{slug}.md` without reading the existing `wiki/entries/` version.** This eliminates anchoring bias. Link freely.
6. Update `temp/_staging-index.md` with what was staged this sub-section.
7. Mark the sub-section row complete.

### Phase 2 — Merge

Run once, after all sub-sections are staged. For each file in `temp/` except `_staging-index.md`:

- Look up `wiki/entries/{slug}.md` by slug.
- Apply the merge rule for the entry's `category`:

| category | merge rule |
|----------|------------|
| `concept`, `insight` | Full prose consolidation. Rewrite body by synthesizing both versions. `## Connections`, `## Illustrations`, `## Sources` are **append-only**. |
| `entity`, `application`, `process` | Structured merge. Append-only link sections. Union category-specific fields (`applies`, `stages`, key contributions). Keep the richer prose for each section. |
| `illustration` | Replace. Temp version is a fresher, unanchored rewrite. |
| `source` | Structured merge. Append to Summary, Key ideas, Notable claims, Connections. |
| `lens` | Full prose consolidation. Criteria section is append-only. `lens_priority` only changes by explicit decision. |

#### Frontmatter merge (mechanical)

| field | rule |
|-------|------|
| `id` | keep original (must match filename) |
| `title` | keep original unless explicitly re-canonicalized |
| `category` | must agree; mismatch → halt and escalate |
| `classified_by` | must agree; mismatch → halt and escalate |
| `domains` | union, deduplicated |
| `tags` | union, deduplicated |
| `sources` | union, deduplicated |
| `aliases` | union, deduplicated |
| `created` | keep original |
| `updated` | today's date |
| `confidence` | most conservative (`contested` > `low` > `medium` > `high`) |
| `status` | highest of {`draft`, `stub`, `complete`} |
| category-specific lists | union, deduplicated |

### Phase 3 — Closeout

1. Update the source entry (`wiki/entries/{source-slug}.md`) — append Key ideas, Notable claims, Connections from this chapter.
2. Update `wiki/_meta/index.md` — add new entries, remove deleted ones. `pnpm build:vault-indexes` does this mechanically.
3. Update affected `wiki/_meta/indexes/{domain}.md` files — same run.
4. Append to `wiki/_meta/log.md` with a per-chapter summary.
5. Update `wiki/_meta/overview.md` if the new material reshapes the narrative map.
6. Update the ingestion tracker — mark the chapter row complete, list entries created/updated, note cross-chapter observations.
7. Clean `temp/` (including `_staging-index.md`).

Target: each chapter touches 3–10 entries across categories. If you're only creating 1 per chapter, you're not linking enough.

### Resuming ingestion

When the user says "continue", "next chapter", or re-ingests a source:

1. Read the process trace at `raw/{source-slug}/{source-slug}-process-trace.md` to find current state.
2. Reconcile partial state before reading new material:
   - If a chapter is `in-progress` with some sub-sections complete, resume at the next incomplete sub-section.
   - If `temp/_staging-index.md` exists, read it — do not duplicate.
   - If notes were created without corresponding tracker/index/log updates, finish that bookkeeping first.
3. Explicit chapter request overrides the default next-unit behavior.
4. Otherwise continue with the lowest-numbered incomplete unit.
5. Stop after that chapter unless the user explicitly asks for more.

### Reingesting a completed chapter

When asked to reingest (e.g., "redo chapter 3"):

1. Confirm from the tracker that the chapter was previously `complete`.
2. Mark it back to `in-progress`; add `Reingesting chapter {N} — {date}` to Running notes.
3. Run the full per-chapter workflow (Setup → Stage → Merge → Closeout). Temp starts empty; notes are written fresh, blind to existing versions.
4. **During Merge, treat the existing wiki entries as richer** — they have accumulated connections from later chapters. The reingested version is a depth upgrade, not a replacement. Append-only links are especially load-bearing here.
5. On completion, update the tracker row; append `(reingested)` to the Notes cell. Do not change the tracker's overall `status` or `chapters_completed`.

### Completing a source

When all chapters are done:

1. Mark tracker status `complete`.
2. Review the source entry — Summary reflects the full work, Key Ideas comprehensive, Connections complete.
3. Review Running notes — promote any cross-chapter observations worth their own entry into concept or insight entries.
4. If the touched-page history is incomplete, reconstruct from tracker rows, source backlinks, and recent log entries before linting.
5. Run lint on all pages touched during this ingestion.

## Query workflow

When the user asks a question:

1. Read `wiki/_meta/index.md` and the relevant per-domain indexes to find pages.
2. If the indexes appear stale for the question, verify by searching `wiki/entries/` directly.
3. Read relevant entries and synthesize an answer.
4. Cite entries via `[[wikilinks]]`.
5. If the answer is substantial, offer to file it as a new concept or insight entry.
6. If the question reveals a gap, note it and offer to investigate.

## Lint workflow

When asked to lint:

1. **Slug uniqueness** — filesystem enforces it; sanity-check.
2. **Orphan entries** — no inbound `[[wikilinks]]`.
3. **Broken wikilinks** — links to a slug with no file.
4. **Main-index coverage** — every `entries/*.md` file appears in `_meta/index.md`.
5. **Domain-index coverage** — every entry appears in every domain index its `domains` names, and nowhere else.
6. **Classification consistency** — `classified_by` names a lens whose `lens_covers_category` equals this entry's `category`.
7. **Lens coverage** — every category value in use has a lens covering it.
8. **Category-specific field presence** — illustrations have `illustrates`, processes have `stages`, etc.
9. **Stale content** — older claims superseded by newer sources.
10. **Thin entries** — `status: stub` older than N days, or body below size threshold.
11. **Low link density** — entries with fewer than 2 outbound wikilinks.
12. **Type misclassification** — entries the decision tree would now classify differently.
13. **Missing insights** — overview threads that should be promoted.
14. **Missing processes** — multi-stage sequences described in concept entries that warrant their own process entry.
15. Suggest new questions and sources to look for.

`scripts/wiki-lint.ts` (follow-up) will mechanize the first 8 checks.

## Conventions

- `[[wikilinks]]` for internal links (Obsidian-compatible, bare slugs).
- Filenames: lowercase, hyphenated slugs (`spaced-repetition.md`).
- Before creating a new slug, check for collisions and near-duplicates. Disambiguate with a stable contextual suffix rather than overwriting.
- Tags: lowercase, hyphenated, free-form. A tag that reduces to a domain name should be listed as a domain and dropped from tags.
- Dates: `YYYY-MM-DD` always.
- Update `updated` whenever modifying an entry.
- When a new source contradicts an existing entry, flag the contradiction and update `confidence` accordingly.
- Prefer depth over breadth — a few well-developed, densely-linked entries beat many stubs.
- When metadata (author, year, chapter label, page range) is ambiguous, mark the uncertainty rather than fabricating specificity.
- Keep concept/entity/application/insight/process prose source-agnostic. Put source attribution in `## Sources`, `## Mentioned in`, frontmatter, and trackers. Illustration entries may retell source narratives but avoid meta phrasing about chapter structure.

## Learning-specific guidance

This wiki focuses on learning theory, pedagogy, and evidence-based study. Keep these active:

- **Elaborative interrogation**: When creating concept entries, address "why does this work?" and "how does this connect?" — not just "what is this?"
- **Dual coding**: When concepts have visual representations (diagrams, models, frameworks), note them and reference images under `raw/{source-slug}/assets/` when available.
- **Convergence tracking**: When multiple sources converge on the same finding, record the convergence explicitly. When they diverge, flag it with `confidence: contested`.
- **Practice-science gap**: Many findings about what works in learning *feel wrong* because they run against the subjective sense of fluency. When writing application entries, state the counterintuitive part explicitly.

## Scripts quick reference

```
pnpm migrate:vault [--apply]      # one-shot: rewrite learning-assist → vault
pnpm build:vault-indexes          # rebuild _meta/index.md and every domain index
pnpm vault:add vaults/vault --name vault --mask 'wiki/**/*.md'
pnpm vault:update
pnpm vault:embed
```
