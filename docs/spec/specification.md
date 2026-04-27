# vault specification

> this is the vault's operational specification. it describes — in extreme detail — what the end product is: every process, every entry kind, every frontmatter field, every gate, every lifecycle is named and given concrete rules. it is the source from which working documents are generated under a clean-room implementation schema; it is itself not a working document. anything still under discussion is collected in §35 (open issues / deferred decisions); everything else is binding within the spec.

## table of contents

1. [document scope and conventions](#1-document-scope-and-conventions)
2. [vault layout](#2-vault-layout)
3. [entry kinds — the complete catalog](#3-entry-kinds--the-complete-catalog)
4. [canonical frontmatter schema](#4-canonical-frontmatter-schema)
5. [body structure and the lead convention](#5-body-structure-and-the-lead-convention)
6. [slugs and disambiguation](#6-slugs-and-disambiguation)
7. [the lens system](#7-the-lens-system)
8. [the notability gate](#8-the-notability-gate)
9. [edit-hardness, reputation, and pending changes](#9-edit-hardness-reputation-and-pending-changes)
10. [connections — claims, relations, questions](#10-connections--claims-relations-questions)
11. [structure notes](#11-structure-notes)
12. [domains](#12-domains)
13. [policy, guideline, essay — the three-tier rule system](#13-policy-guideline-essay--the-three-tier-rule-system)
14. [high-stakes claims](#14-high-stakes-claims)
15. [contentious domains](#15-contentious-domains)
16. [agents](#16-agents)
17. [the ingestion pipeline](#17-the-ingestion-pipeline)
18. [reingestion](#18-reingestion)
19. [merge rules — full catalog](#19-merge-rules--full-catalog)
20. [lint workflow](#20-lint-workflow)
21. [findings](#21-findings)
22. [discussions](#22-discussions)
23. [noticeboards](#23-noticeboards)
24. [agent tests](#24-agent-tests)
25. [runs and versioning](#25-runs-and-versioning)
26. [operations](#26-operations)
27. [retrieval contract (v0)](#27-retrieval-contract-v0)
28. [assessment and the thesis-eval panel](#28-assessment-and-the-thesis-eval-panel)
29. [seed configuration](#29-seed-configuration)
30. [bootstrap procedure](#30-bootstrap-procedure)
31. [governance: edits to this document](#31-governance-edits-to-this-document)
32. [vocabulary index](#32-vocabulary-index)
33. [worked example — ingesting a single chapter end-to-end](#33-worked-example--ingesting-a-single-chapter-end-to-end)
34. [error and failure handling](#34-error-and-failure-handling)
35. [open issues / deferred decisions](#35-open-issues--deferred-decisions)

---

## 1. document scope and conventions

### 1.1 purpose

this document describes — in extreme, unambiguous detail — what the end product is. its purpose is to serve as the blueprint from which the end product is produced under a clean-room implementation schema: the blueprint is read once, the end product is realized from it, and the result thereafter stands on its own. the spec itself is a blueprint, not part of what it describes.

### 1.2 translation to working documents

the spec follows a clean-room implementation schema. it is consulted to produce working documents — the runtime under `runner/`, the seed entries under `wiki/entries/`, the policy/guideline/essay corpus, the build scripts and lint runners. once a working document is produced, it stands on its own and is governed by its own rules. working documents do not contain references back to this spec; the relationship is one-way and one-time. the spec is a high-fidelity blueprint, not a runtime reference.

### 1.3 authority

this spec is the highest-authority document at the moment working documents are produced from it: nothing else outranks it for that purpose. it confers no ongoing authority against working documents that already exist. once a working document is produced — a policy entry, a runtime module, a lens entry, a configuration — it carries its own authority and is governed by its own rules. divergence between a working document and this spec is not a conflict to be resolved against the spec: the working document is the authority on its own behavior; the spec, at most, is a record of the original blueprint.

### 1.4 notation

- `slug` — bare entry identifier, lowercase, hyphenated. always equal to the filename without `.md`.
- `[[slug]]` — wikilink to the entry whose filename is `{slug}.md`. obsidian-compatible.
- `policy-*`, `lens-*`, etc. — entry-slug pattern. the `*` is a placeholder.
- `frontmatter:field` — the named field in an entry's yaml frontmatter.
- `kind` — the value of the `category` frontmatter field. (the term "category" is retained from the existing schema; see [open issue 35.1](#351-the-category-vocabulary-clash) for the planned rename to `kind`.)
- `confirmed`, `extended-confirmed`, etc. — edit-hardness tiers (§9).
- `passes`, `borderline`, `fails` — notability stamps (§8).
- `A`, `B`, `C`, `D` — evidence grades (§10).
- timestamps and dates — `YYYY-MM-DD` always.
- counts are integers; thresholds are integers unless explicitly fractional.
- prose is lowercase.

### 1.5 stability of this document

this document is itself an artifact under the same edit-hardness rules as a policy entry. amendments require the meta-rule quorum (§9.4). the seed phase relaxes this — until reputation gates can take over, edits to this document require human review. each substantive edit produces a `run-spec-amend-{date}` entry recording the change.

### 1.6 phases of vault evolution

the vault is designed to migrate over time from a human-bootstrapped scaffold to an agent-autonomous knowledge graph. the phase the vault is currently operating in is recorded in `policy-phase`. each phase changes who is allowed to edit which kinds of entries.

#### 1.6.1 phase 1 — frozen structure (current phase)

in phase 1, **only humans set wiki structure**. agents may operate within that structure, but cannot edit it.

what counts as "wiki structure" in phase 1, and is therefore locked against agent writes regardless of the default tier defined in §9.2:

- every `lens-*` entry (the classification rules)
- every `policy-*`, `guideline-*`, `essay-*` entry (the rule tiers — every tier; essays are locked too because authoring an essay is a structural act of proposing a future rule)
- every entry whose `category` is `domain` (the subject axes)
- every `agent-*` entry (the population manifest)
- this specification

agents may **read** all of the above. agents may **discuss** all of the above (§22) — but discussion termination is advisory until phase 2 (§16.8.3).

what agents may write in phase 1:

- content entries — `concept`, `source`, `illustration`, `application`, `entity`, `process`, `insight`, `claim`, `relation`, `structure-note`, `disambiguation`, `question` — subject to per-entry edit-hardness and notability rules.
- their own work products — `run-*`, `finding-*`, `discussion-*` (rounds and termination on content disputes), `notification-*`, `pending-*`. these are agent outputs by construction.

the §9.2 edit-hardness defaults describe the steady-state (phase 2+) tiers. phase 1 overrides them for the kinds listed above by setting their effective tier to `locked` against any agent write. the runtime rejects such writes pre-check; no reputation is consumed and no partial state is written. rejection emits `finding-phase-1-lockdown-violation-{target-slug}`.

#### 1.6.2 phase 2 — population maturity (future)

phase 2 unlocks structural edits, but only via the meta-rule quorum (§9.4). agents may then:

- propose new lenses, domains, policies, guidelines, essays via the relevant lifecycle / promotion paths.
- propose new agent manifests via `lifecycle-agent-create` (§16.3.1).
- propose amendments to this specification.

every structural edit still requires either (a) 3 agents at reputation ≥ 80 voting independently within a 7-day window, or (b) a human reviewer. the difference from phase 1 is that the agent-quorum path now exists — humans are no longer the sole route.

#### 1.6.3 phase 3 — full autonomy (design end-state)

phase 3 begins when the meta-rule quorum has demonstrated stable, beneficial structural evolution over a measurement window (per `policy-thesis-eval`). at phase 3:

- humans no longer participate in quorum.
- the human's role narrows to two acts: directing material in (curating sources for ingestion) and consuming output (retrieval).
- structural edits proceed entirely through the agent quorum.

phase 3 is the design end-state. phase 1 and 2 are scaffolding.

#### 1.6.4 phase transition criteria

transitions are explicit. they are themselves meta-rule actions amending `policy-phase`.

| from    | to      | criteria                                                                                                                                                                                                                                |
| ------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| phase 1 | phase 2 | population has ≥3 active editor agents at reputation ≥30; thesis-eval shows positive variance reduction sustained over 4 weeks; no open `severity: blocking` findings against runtime or seed policies; human reviewer ratifies.        |
| phase 2 | phase 3 | meta-rule quorum has resolved ≥10 structural amendments without human override; thesis-eval variance reduction has improved over phase-1 baseline by a target margin set in `policy-thesis-eval`; meta-rule quorum ratifies.            |

a transition does not roll back automatically. demotion (phase 2 → phase 1) is a meta-rule action with the same machinery, triggered by a quorum decision that the previous phase was unstable.

### 1.7 the three pillars

the vault has three pillars. every section of this specification belongs to exactly one. the table is the navigation aid for the rest of the document.

| pillar                  | what it defines                                                                                | sections                                                                                                                                              |
| ----------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **wiki structure**      | what entries exist, how they are shaped, how they are organized                                | §2 layout · §3 entry kinds · §4 frontmatter · §5 body · §6 slugs · §7 lenses · §8 notability · §11 structure notes · §12 domains                      |
| **wiki governance**     | the rules that bind agent behavior, how those rules are enforced and amended                   | §9 edit-hardness · §13 policy/guideline/essay · §14 high-stakes · §15 contentious · §19 merge · §20 lint · §21 findings · §22 discussions · §23 noticeboards · §31 spec governance |
| **agentic structure**   | who acts, what they may act on, how they are created, retired, scored                          | §10 claims/relations/questions · §16 agents · §17–18 ingestion · §24 agent tests · §25 runs · §26 operations · §27 retrieval · §28 assessment         |

phase 1 freezes the entirety of "wiki structure" and "wiki governance" against agent edits, plus the agent manifests that define "agentic structure" itself. only the work agents do — content edits, run records, findings, content discussions, pending proposals — is agent-driven in phase 1.

---

## 2. vault layout

### 2.1 top-level directory structure

```
.
├── docs/
│   └── spec/
│       └── specification.md       # this document
├── raw/
│   └── {source-slug}/
│       ├── {source-slug}.md       # the source document, immutable
│       ├── {source-slug}-process-trace.md
│       └── assets/                # optional supporting media
├── temp/                          # ephemeral per-chapter staging; cleared between chapters
├── wiki/
│   ├── entries/                   # every entry, flat
│   └── _meta/
│       ├── index.md               # main index
│       ├── indexes/
│       │   └── {domain}.md        # per-domain index, one per active domain
│       └── noticeboards/
│           └── {kind}.md          # per-finding-kind projection
└── runner/                        # the runtime that executes agents
    └── …                          # outside the vault; small, versioned
```

### 2.2 directory rules

- **`raw/`**. one folder per source. the source document under `raw/{source-slug}/{source-slug}.md` is **immutable** — never modified after intake. process trace under the same folder records ingestion progress. assets (images, attachments) under the source's `assets/` subfolder.
- **`temp/`**. ephemeral. cleared between chapters as part of phase 0 setup. flat layout (no nesting). underscore-prefixed files (e.g., `_staging-index.md`) are reserved for staging metadata and never collide with entry slugs.
- **`wiki/entries/`**. the only flat pile of entries. every entry is a single markdown file named `{slug}.md`. nesting is forbidden. directory listing alone must reveal every entry the vault holds.
- **`wiki/_meta/`**. structural files _about_ the vault — never entries _in_ the vault. contents are either cached projections (the main index, the per-domain indexes, the noticeboards, the assessment dashboard) rebuilt mechanically from `wiki/entries/`, or cold archives (older runs, resolved findings, closed discussions, retired notifications) moved here per `policy-archival` (§26.3). nothing in `_meta/` is hand-authored, and nothing here is the source of truth for anything: projections are reproducible by rebuild; archives are recoverable from git. this is deliberate. hand-authored cross-vault narrative belongs in structure-note entries (§11), not in `_meta/`; chronological activity belongs in `run-*` entries and git history, not in a synthesized log file.
- **`wiki/_meta/indexes/`**. one file per active domain. generated by `pnpm build:vault-indexes`. the domain entry under `wiki/entries/{domain-slug}.md` is the source of truth; the file under `_meta/indexes/{domain-slug}.md` is its rendered projection.
- **`wiki/_meta/noticeboards/`**. one file per finding kind. rebuilt by the same projection rule as indexes (§23). subscribed agents read these instead of scanning `wiki/entries/finding-*.md`.
- **`runner/`**. outside the vault. the only enforcer of write-scope, reputation gates, and edit-hardness; described in `policy-runtime` once that policy lands.

### 2.3 indexing globs

| consumer                  | glob                | excludes                                          |
| ------------------------- | ------------------- | ------------------------------------------------- |
| qmd vault collection      | `wiki/**/*.md`      | `raw/**`, `temp/**`, `docs/**`, `node_modules/**` |
| index/noticeboard rebuild | `wiki/entries/*.md` | none                                              |
| lint full pass            | `wiki/entries/*.md` | none                                              |

`raw/`, `temp/`, `docs/`, and `runner/` are never indexed for retrieval.

### 2.4 path forbiddens

- no `wiki/entries/` subdirectories. ever.
- no entry filenames containing `/`, `\`, spaces, or characters outside `[a-z0-9-]`.
- no entry filename starting with `_`. underscore is reserved for staging metadata in `temp/` and structural files in `wiki/_meta/`.
- no two entries with the same slug. uniqueness is enforced by the filesystem and re-checked by lint.

---

## 3. entry kinds — the complete catalog

### 3.1 the two-tier split

entries split into **content** (the substance of the vault) and **infrastructure** (the vault's own state). they share the flat layout and frontmatter schema; they differ in classification path, retention, and write rate.

| tier           | classified via                                                      | retention                     | typical write rate          |
| -------------- | ------------------------------------------------------------------- | ----------------------------- | --------------------------- |
| content        | the lens decision tree (§7)                                         | persistent                    | one per knowledge unit      |
| infrastructure | a named lifecycle protocol; `produced_by` frontmatter records which | aggressively archived (§26.3) | a `run` per agent execution |

### 3.2 content kinds

| slug prefix       | kind             | what it carries                                                                                                           | notes                                                              |
| ----------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| (free slug)       | `concept`        | one idea, explained on its own terms. the catch-all when no narrower kind applies.                                        | richest body. always has a lead if above threshold.                |
| (free slug)       | `source`         | literature note for one raw document — book, article, transcript. cites; does not synthesize.                             | always has a lead. one source entry per `raw/{source-slug}/`.      |
| (free slug)       | `illustration`   | a story with protagonist, setting, outcome. retells a source narrative to anchor a concept.                               | only kind allowed to retell source prose closely.                  |
| (free slug)       | `application`    | a practitioner-followable instruction set.                                                                                | written as steps a reader can execute.                             |
| (free slug)       | `entity`         | a proper-noun subject — person, institution, theory, framework, method.                                                   | `entity_kind` frontmatter required.                                |
| (free slug)       | `process`        | multi-stage sequence with named transitions.                                                                              | `stages` frontmatter is ordered.                                   |
| (free slug)       | `insight`        | a connection between 2+ existing concepts that names a non-trivial relationship.                                          | always references at least 2 concepts in `connects`.               |
| `claim-`          | `claim`          | one atomic assertion with evidence and grade. the smallest content unit.                                                  | atomicity policed by `policy-claim-segmentation`.                  |
| `relation-`       | `relation`       | a typed, directed edge between entries. predicates: `supports`, `contradicts`, `instance-of`, `supersedes`, `depends-on`. | carries its own evidence grade.                                    |
| `structure-`      | `structure-note` | organizing prose plus annotated links into a cluster. holds a region of the graph together.                               | replaces wikipedia's parent-article pattern. lead always required. |
| `disambiguation-` | `disambiguation` | routing entry for a polysemous term.                                                                                      | body lists variants with one-line distinguishers.                  |
| `question-`       | `question`       | an open question the vault cannot yet answer. pins a gap.                                                                 | closes when an entry, claim, or relation answers it.               |

### 3.3 infrastructure kinds

| slug prefix                    | kind                 | what it carries                                                                                                                                                          | notes                                                 |
| ------------------------------ | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------- |
| `lens-`                        | `lens`               | a classification rule, written as a yes/no question and criteria.                                                                                                        | self-classifying via `lens-lens`.                     |
| (free slug, often domain name) | `domain`             | a subject axis: scope, out-of-scope, canonical questions, contentious flag, evidence-grade floor, edit-hardness floor, subscribed editors, load-bearing structure notes. | one per active domain.                                |
| `policy-`                      | `policy`             | a binding rule. lint enforces; meta-rule edits required.                                                                                                                 | highest of the three rule tiers (§13).                |
| `guideline-`                   | `guideline`          | a best-practice norm. violations produce advisory findings.                                                                                                              | middle tier.                                          |
| `essay-`                       | `essay`              | an under-development take. binds nothing.                                                                                                                                | lowest tier; promotion path leads upward.             |
| `agent-`                       | `agent`              | the manifest of an active process — editor, persona, or lint. slice + bindings + lifecycle + reputation.                                                                 | `kind` frontmatter is `editor`, `persona`, or `lint`. |
| `run-`                         | `run`                | one agent execution. records reads, writes, findings, active policy/lens versions, identity.                                                                             | dominates file count; archived to rollups (§26.3).    |
| `finding-`                     | `finding`            | a problem the vault has noticed about itself. open/resolved/wontfix.                                                                                                     | links to the rule that fired.                         |
| `agent-test-`                  | `agent-test`         | a query with an expected answer shape, attached to an agent. run as regression.                                                                                          | failure becomes a finding.                            |
| `discussion-`                  | `discussion`         | a recorded exchange between agents disputing an entry.                                                                                                                   | round-bounded (§22).                                  |
| `notification-`                | `notification`       | inter-agent mention, review request, or escalation.                                                                                                                      | short-lived; archived.                                |
| `pending-`                     | `pending` (proposal) | a staged write from a sub-confirmed agent awaiting review.                                                                                                               | parallel state attached to a target entry (§9.5).     |

### 3.4 forbidden combinations

- a content entry must not have `produced_by` frontmatter. `produced_by` is the marker of infrastructure-protocol authorship.
- an infrastructure entry must not be classified by a lens. its category is set by the lifecycle protocol that produced it. lint check `infrastructure-classified-by-lens` enforces this.
- a lens entry must classify itself via `lens-lens`. lint check `lens-self-classification` enforces this.

---

## 4. canonical frontmatter schema

### 4.1 the common head

every entry — content or infrastructure — carries this frontmatter at the top of the file, between `---` fences:

```yaml
---
id: { slug } # must equal filename without .md
title: '{Title Case Title}'
category: { kind } # one of the kinds in §3
classified_by: { lens-slug } # for content entries
produced_by: { protocol-name } # for infrastructure entries
domains: [{ domain-slug }, ...] # 1..N; never empty
tags: [{ tag }, ...] # free-form, lowercase, hyphenated
sources: [{ source-slug }, ...] # bare slugs of source-kind entries
aliases: [] # optional search aliases
created: { YYYY-MM-DD }
updated: { YYYY-MM-DD }
confidence: high # high | medium | low | contested
status: complete # draft | stub | complete
notability_status: passes # passes | borderline | fails | n/a (n/a for infrastructure)
edit_hardness: open # open | confirmed | extended-confirmed | restricted | locked
high_stakes_class: none # none | medical | legal | safety | identifiable-individual
quality: c # stub | start | c | b | a | featured  (cf. wikipedia GA/FA)
---
```

### 4.2 field-by-field rules

| field               | type   | required?                         | rule                                                                                                                                                        |
| ------------------- | ------ | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                | string | yes                               | exactly equal to filename without `.md`. lint `id-filename-mismatch`.                                                                                       |
| `title`             | string | yes                               | title case, quoted. one entry, one canonical title.                                                                                                         |
| `category`          | enum   | yes                               | one of the kinds in §3.2 or §3.3. lint `unknown-category`.                                                                                                  |
| `classified_by`     | string | content only                      | the slug of the lens that ruled. its `lens_covers_category` must equal this entry's `category`. lint `classification-consistency`.                          |
| `produced_by`       | string | infrastructure only               | name of the lifecycle protocol that produced this entry, e.g., `pipeline-unpack`, `lifecycle-agent-create`. lint `infrastructure-without-produced-by`.      |
| `domains`           | list   | yes                               | non-empty. every value must equal an existing domain entry's `id`. lint `unknown-domain`, `entry-without-domain`.                                           |
| `tags`              | list   | optional                          | lowercase, hyphenated. tags reducing to a domain name must instead live in `domains`. lint `tag-shadowing-domain`.                                          |
| `sources`           | list   | optional                          | bare slugs of source-kind entries. machine-readable shorthand; the body's `## Sources` section is the rich attribution. lint `source-frontmatter-mismatch`. |
| `aliases`           | list   | optional                          | alternative titles a search query might use.                                                                                                                |
| `created`           | date   | yes                               | first-write date. never modified after creation.                                                                                                            |
| `updated`           | date   | yes                               | most recent modification date. updated by every write. lint `updated-not-current` after any edit.                                                           |
| `confidence`        | enum   | yes                               | `high` (multiple sources converge), `medium` (one source or weak convergence), `low` (single weak source), `contested` (sources actively disagree).         |
| `status`            | enum   | yes                               | `draft` (work in progress, do not retrieve), `stub` (thin but published), `complete` (ratified).                                                            |
| `notability_status` | enum   | content yes; infrastructure `n/a` | set by `lens-notability` at unpack. transitions per §8.                                                                                                     |
| `edit_hardness`     | enum   | yes                               | one of the five tiers (§9.1). set by the classifying lens or the producing protocol; raised by domain inheritance; never lowered.                           |
| `high_stakes_class` | enum   | yes                               | `none` is the default. non-`none` triggers asymmetric removal regime when evidence is below floor (§14).                                                    |
| `quality`           | enum   | optional but recommended          | quality tier (§5.7); separate from `status`.                                                                                                                |

### 4.3 per-kind extensions

each kind may carry additional fields beyond the common head. enumerated below; lint `category-fields-presence` enforces required fields per kind.

#### 4.3.1 lens

```yaml
lens_question: '...' # non-empty string, the yes/no question the lens asks
lens_priority: 0 # integer; lower = earlier in decision-tree order
lens_covers_category: lens # the kind this lens ranges over
lens_criteria: # ordered list of checklist items
  - 'criterion 1'
  - 'criterion 2'
lens_kind: decision-tree # decision-tree | annotation
```

#### 4.3.2 source

```yaml
author: '{Author Name}'
year: 2019
source_file: 'raw/{source-slug}/{source-slug}.md'
date_ingested: 2026-04-21
```

#### 4.3.3 entity

```yaml
entity_kind: person # person | institution | theory | framework | method
```

#### 4.3.4 illustration

```yaml
source: '[[{source-slug}]]' # quoted wikilink, single source
illustrates: [{ concept-slug }, ...]
chapter: 'Chapter 4' # if known; mark "unknown" otherwise
pages: '120–135' # if known
```

#### 4.3.5 application

```yaml
applies: [{ concept-slug }, ...]
prerequisites: [{ slug }, ...] # optional
```

#### 4.3.6 process

```yaml
stages: [{ stage-slug }, ...] # ordered; the order is meaningful
preconditions: [{ slug }, ...] # optional
postconditions: [{ slug }, ...] # optional
```

#### 4.3.7 insight

```yaml
connects: [{ slug }, ...] # at least 2 entries
```

#### 4.3.8 claim

```yaml
claim_text: '...' # the assertion as a single declarative sentence
evidence_grade: A # A | B | C | D — see §10.2
evidence_pointers:
  - source: '[[{source-slug}]]'
    pages: '...'
    quote: '...' # optional
asserts_about: [{ slug }, ...] # entries the claim is about
verifiable: true # boolean — is the claim, in principle, verifiable?
```

#### 4.3.9 relation

```yaml
predicate: supports # supports | contradicts | instance-of | supersedes | depends-on
from: '[[{slug}]]'
to: '[[{slug}]]'
evidence_grade: B
evidence_pointers: [...]
```

#### 4.3.10 structure-note

```yaml
organizes: [{ slug }, ...] # entries the note holds together; usually >5
domain_frame: learning-theory # the frame from which this note organizes the cluster; one of the entry's domains
```

#### 4.3.11 disambiguation

```yaml
variants:
  - slug: '{variant-slug-1}'
    distinguisher: '{one-line distinguisher}'
  - slug: '{variant-slug-2}'
    distinguisher: '...'
```

#### 4.3.12 question

```yaml
asks_about: [{ slug }, ...]
priority: medium # low | medium | high
opened_by: '[[{run-or-finding-slug}]]'
closes_when: '...' # human-readable success criterion
```

#### 4.3.13 domain

```yaml
scope: '...' # what the domain covers
out_of_scope: '...' # what it explicitly excludes
canonical_questions: [{ question-slug }, ...]
contentious: false # boolean; raises floors when true
evidence_grade_floor: D # minimum evidence grade for new claims; D = no floor
edit_hardness_floor: open # tier; raises per-entry default by one tier when above open
subscribed_agents: [{ agent-slug }, ...]
load_bearing_structure_notes: [{ slug }, ...]
```

#### 4.3.14 policy / guideline / essay

```yaml
rule_tier: policy # policy | guideline | essay
covers: '...' # one-sentence summary of the rule's scope
linted_by: [{ lint-rule-name }, ...] # for policies; lint rules that enforce it
promotion_history: # for entries that have been promoted
  - from: essay
    to: guideline
    on: 2026-05-12
    via: '[[discussion-{slug}]]'
```

#### 4.3.15 agent

```yaml
agent_kind: editor # editor | persona | lint
prompt_ref: '...' # path or slug to the prompt definition
slice: # what the agent reads/writes
  read_domains: [{ domain-slug }, ...]
  write_domains: [{ domain-slug }, ...]
  voice_rules: [...] # for persona
  refusal_rules: [...] # for persona
  policy_targets: [{ policy-slug }, ...] # for lint
reputation: 0.0 # current reputation score, 0.0–100.0
lifecycle_stage: active # proposed | active | retired
seed_tests: [{ agent-test-slug }, ...]
created_via: '[[run-{slug}]]'
```

#### 4.3.16 run

```yaml
run_kind: edit                     # edit | lint | assess | ingest | review
agent: "[[agent-{slug}]]"
started: 2026-04-27T10:23:00Z
finished: 2026-04-27T10:31:00Z
reads: ["[[slug-1]]", "[[slug-2]]"]
writes: ["[[slug-3]]", ...]
findings_raised: ["[[finding-{slug}]]", ...]
policy_versions:                  # which version of each policy was active
  policy-ingestion: "v3"
  policy-classification: "v2"
lens_versions:
  lens-concept: "v4"
  ...
```

#### 4.3.17 finding

```yaml
finding_kind: broken-wikilink # one of the named lint rules in §20
status: open # open | resolved | wontfix
fired_by: '[[lint-{rule-slug}]]'
involves: ['[[slug-1]]', '[[slug-2]]']
opened: 2026-04-27
resolved: null # date when status flips to resolved
resolution_run: null # link to the run that resolved it
wontfix_justification: null # required when status is wontfix
severity: blocking # advisory | blocking
```

#### 4.3.18 agent-test

```yaml
agent: '[[agent-{slug}]]'
question: '...' # the query
expected_shape: '...' # what a passing answer looks like
authoritative: true # human-authored seed test; gates promotion to test list
last_run: 2026-04-26
last_result: pass # pass | fail | stale
```

#### 4.3.19 discussion

```yaml
disputed_object: '[[{slug}]]'
opened: 2026-04-25
participants: ['[[agent-{slug}]]', ...]
rounds: 0 # 0..5
status: open # open | closed-resolved | closed-wontfix | escalated | stale
termination_protocol: content-quorum # content-quorum | meta-rule-quorum | human-escalation
```

#### 4.3.20 notification

```yaml
to: '[[agent-{slug}]]'
from: '[[agent-{slug}]]'
about: '[[{slug}]]'
notification_kind: review-request # mention | review-request | escalation
status: unread # unread | read | acted
```

#### 4.3.21 pending (proposal)

```yaml
target: '[[{slug}]]' # the entry the proposal would modify or create
proposal_kind: create # create | modify | retire
proposed_by: '[[agent-{slug}]]'
proposed_at: 2026-04-27T11:00:00Z
diff: '...' # rendered diff or full body for create
status: pending # pending | accepted | rejected | superseded
reviewed_by: null # set on accept/reject
review_run: null # link to the run that reviewed it
```

### 4.4 frontmatter parsing rules

- the frontmatter block is the first content of the file. anything before it is invalid.
- yaml strict mode. quotes are required for any string containing `:`, `#`, `[`, `]`, `{`, `}`, or starting with `- `.
- every list field, when empty, must be `[]`, never absent. lint `missing-required-list`.
- enum fields are case-sensitive. always lowercase except for `evidence_grade` (capital `A`–`D`).
- dates are ISO `YYYY-MM-DD`. timestamps are ISO 8601 with `Z` suffix when needed.

---

## 5. body structure and the lead convention

### 5.1 body anatomy

every entry's body follows this structural template, with sections appearing in this order when present:

```markdown
# {Title}

## Lead # required when body length exceeds threshold; see §5.2

{1–3 sentences compressing the entry's content.}

## {Kind-specific main section}

{The substantive body of the entry.}

## Connections # optional but recommended for content entries

- relation-1: [[other-slug]] — annotation
- relation-2: [[other-slug]] — annotation

## Sources # required for any entry citing sources

- [[{source-slug}]], chapter X, pages Y–Z
- [[{source-slug}]], pages …

## Mentioned in # optional; backlink list

- [[{slug}]] — context
```

sections beyond these may appear when meaningful (e.g., `## Examples`, `## Counterexamples`). order is not enforced beyond the constraint that `## Lead` (when present) must be the first heading after the title.

### 5.2 the lead convention

#### 5.2.1 the threshold rule

an entry must carry a `## Lead` section when its body (everything after the title and frontmatter, excluding the lead itself) exceeds either:

- **200 words**, or
- **two paragraphs of prose**, where a paragraph is a block of contiguous lines separated by blank lines and containing more than one sentence.

if the body is below both thresholds, the lead may be omitted; the first sentence of the body acts as the implicit lead.

structure notes (§11) and source entries (§4.3.2) carry a `## Lead` regardless of size, because their leads are load-bearing for retrieval at the cluster and source level respectively.

#### 5.2.2 the lead format

- one to three sentences.
- written as a self-contained compression of the entry's content, not as an introduction that depends on later prose.
- no wikilinks in the lead unless removing the wikilink would make the lead ungrammatical. the lead is a retrieval target, and gratuitous links increase token cost without improving compression.
- no first-person voice ("we") and no metadata phrasing ("this entry covers"). just claims.

#### 5.2.3 how retrieval uses leads

retrieval (§27) returns leads first; full bodies only when the consumer's budget permits and the lead is insufficient. a lead written sloppily — that mostly restates the title or that hedges where the body is decisive — degrades retrieval quality across every query that lands on the entry. lead quality is therefore lint-checked (§20) and contributes to entry quality grading (§5.7).

### 5.3 wikilinks

#### 5.3.1 syntax and resolution

- `[[slug]]` — bare slug. resolves to `wiki/entries/{slug}.md`. case-sensitive.
- `[[slug|display text]]` — bare slug, with custom display text.
- `[[#anchor]]` — within-entry anchor. valid only inside the same file.
- `[[slug#anchor]]` — anchored cross-entry link.

#### 5.3.2 link-density requirement

every content entry must carry at least 2 outbound `[[wikilinks]]` to other content entries. lint `low-link-density` produces an advisory finding for entries below this floor. structure notes carry many more outbound links by their nature; a structure note with fewer than 5 outbound links to entries it claims to organize is a finding (`structure-note-low-link-density`).

#### 5.3.3 broken links

every wikilink must resolve to a file that exists in `wiki/entries/`. lint `broken-wikilink` blocks merges that introduce an unresolved link, except when the link points at a `question-{slug}` that is opened in the same merge.

### 5.4 connections section format

the `## Connections` section uses a controlled list format rather than free prose:

```markdown
## Connections

- {Predicate}: [[other-slug]] — {annotation}
- {Predicate}: [[other-slug]] — {annotation}
```

predicates that may appear inline (without producing a `relation-*` entry):

- `Related to`
- `Coined by`
- `Used in`
- `Contrasts with`
- `Discussed in`

predicates that require their own `relation-*` entry (because they are load-bearing):

- `Supports` → produces `[[relation-{from}-supports-{to}]]`
- `Contradicts` → produces `[[relation-{from}-contradicts-{to}]]`
- `Instance of` → produces `[[relation-{from}-instance-of-{to}]]`
- `Supersedes` → produces `[[relation-{from}-supersedes-{to}]]`
- `Depends on` → produces `[[relation-{from}-depends-on-{to}]]`

an inline `Supports:` in connections without a corresponding `relation-*` entry is a finding (`relation-not-formalized`).

### 5.5 sources section format

```markdown
## Sources

- [[{source-slug}]], chapter {N}, pages {start}–{end} — {brief annotation}
- [[{source-slug}]], pages {start}–{end}
```

frontmatter `sources:` must include the bare slug of every source-kind entry referenced in this section. lint `source-frontmatter-mismatch` enforces.

### 5.6 mentioned-in section

optional. lists entries that link _to_ this entry, with a one-line context for each. functions like a curated backlink list. it is **not** automatically generated; an editor populates it when the inbound links carry meaningful context that the linking entry would not surface. the list is hand-maintained and kept short.

### 5.7 quality grading

distinct from `status`. quality reflects how well-developed the entry is.

| quality    | criteria                                                                                                                            |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `stub`     | minimal viable entry; identifies the topic; few sources; few links.                                                                 |
| `start`    | structurally complete with a real explanation; some sourcing; minimal connections.                                                  |
| `c`        | reasonable depth; multiple sources; established connections; lead present where required.                                           |
| `b`        | strong depth; multiple high-grade sources; rich connections; structure-note backing if part of a cluster; passes all advisory lint. |
| `a`        | comprehensive; primary-literature sources where relevant; load-bearing for the cluster; cited by other entries.                     |
| `featured` | the vault's best work in this domain. peer-reviewed via discussion.                                                                 |

quality is reviewed in assessment passes (§28). promotion to `b`, `a`, or `featured` requires a discussion or review run that records the rationale.

---

## 6. slugs and disambiguation

### 6.1 slug format

- lowercase ascii letters, digits, and hyphens only: `[a-z0-9]+(-[a-z0-9]+)*`.
- no leading or trailing hyphens.
- no double hyphens.
- maximum 80 characters. longer slugs are usually a sign that the title is overspecified.

### 6.2 slug uniqueness

- enforced by the filesystem (one file per filename in a flat directory).
- re-checked by lint (`slug-uniqueness`) every full pass.
- a temp file in `temp/` shares the namespace; staging two different topics under the same slug in the same chapter is a phase 1 error (§17.3).

### 6.3 picking a slug for a new entry

procedure (apply in order):

1. start with the title, lowercased and hyphenated. drop articles ("the", "a", "an"), drop trailing punctuation.
2. check `wiki/entries/` for an existing file with that slug.
3. check `temp/` for an already-staged file with that slug in this chapter.
4. if both checks return no match, the slug is `new`.
5. if `wiki/entries/{slug}.md` exists and is the same subject, mark `merges-with: {existing-slug}`. write into `temp/{slug}.md`.
6. if `wiki/entries/{slug}.md` exists but is a _different_ subject, this is a collision. proceed to disambiguation (§6.4).
7. if `temp/{slug}.md` exists from a prior sub-section of this chapter and is the same subject, mark `extends: {temp-slug}` and enrich in place.
8. if `temp/{slug}.md` exists but is a different subject, halt and resolve manually before continuing the sub-section.

### 6.4 disambiguation

when a new entry's natural slug collides with an existing entry of a different subject:

1. choose a **disambiguator suffix** for the new entry that distinguishes it: `{base-slug}-{disambiguator}`. the disambiguator is a noun naming the variant's domain or kind. examples:
   - `transfer-learning` (concept) vs. `transfer-finance` (concept) → both keep the suffix.
   - `mercury-element` vs. `mercury-planet` vs. `mercury-mythology`.
2. if the existing entry's slug is the bare base slug, it must be renamed to take its own disambiguator suffix. the rename is a phase 4 closeout step, not phase 1; phase 1 just stages the new entry under its disambiguated slug.
3. create or extend the disambiguation entry at `wiki/entries/disambiguation-{base-slug}.md`. this entry's body lists the variants:

   ```markdown
   # {Base Term}

   ## Lead

   "{Base Term}" can refer to several distinct subjects in this vault. Pick the variant that matches your context.

   ## Variants

   - [[transfer-learning]] — the educational-psychology concept
   - [[transfer-finance]] — the financial-services concept
   ```

4. add inline hatnotes to each variant's body, near the top:
   ```markdown
   > For the financial concept, see [[transfer-finance]]. For routing, see [[disambiguation-transfer]].
   ```
5. update the disambiguation entry's frontmatter `variants` list (§4.3.11).

### 6.5 reserved slug prefixes

the following prefixes are reserved for specific kinds and may not be used for other kinds:

| prefix            | reserved for             |
| ----------------- | ------------------------ |
| `lens-`           | lens entries             |
| `policy-`         | policy entries           |
| `guideline-`      | guideline entries        |
| `essay-`          | essay entries            |
| `agent-`          | agent entries            |
| `run-`            | run entries              |
| `finding-`        | finding entries          |
| `agent-test-`     | agent-test entries       |
| `discussion-`     | discussion entries       |
| `notification-`   | notification entries     |
| `pending-`        | pending proposal entries |
| `claim-`          | claim entries            |
| `relation-`       | relation entries         |
| `structure-`      | structure-note entries   |
| `disambiguation-` | disambiguation entries   |
| `question-`       | question entries         |

a content entry of kind `concept`, `source`, `illustration`, `application`, `entity`, `process`, or `insight` must **not** use any reserved prefix. lint `reserved-prefix-misuse` enforces this.

---

## 7. the lens system

### 7.1 the two flavors

- **decision-tree lenses** decide an entry's `category`. exactly one decision-tree lens rules per entry. priorities define the tree-walk order; first match wins.
- **annotation lenses** stamp orthogonal frontmatter fields. they run after `category` is set. multiple annotation lenses run on each entry without competing.

a lens entry's frontmatter `lens_kind` field declares which flavor it is.

### 7.2 the seed lens set — decision-tree

priority order. lower number runs first. first-match wins.

| priority | slug                  | covers (`category`)          | yes-question                                                                                                     |
| -------: | --------------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------------- |
|        0 | `lens-lens`           | `lens`                       | is this entry itself a lens?                                                                                     |
|        5 | `lens-policy-tier`    | `policy`/`guideline`/`essay` | is this entry a rule about how the vault works, and which tier of binding force?                                 |
|       10 | `lens-source`         | `source`                     | is this a literature note about one raw document?                                                                |
|       15 | `lens-structure-note` | `structure-note`             | does the body organize a cluster of entries via annotated links rather than assert facts about a single subject? |
|       18 | `lens-disambiguation` | `disambiguation`             | is this entry a routing target for a polysemous slug?                                                            |
|       20 | `lens-illustration`   | `illustration`               | does the entry have protagonist, setting, and outcome — a story?                                                 |
|       22 | `lens-relation`       | `relation`                   | is this entry a typed, directed edge between two other entries with evidence?                                    |
|       25 | `lens-claim`          | `claim`                      | is this entry a single atomic assertion with evidence?                                                           |
|       30 | `lens-application`    | `application`                | could a practitioner follow this as instructions?                                                                |
|       35 | `lens-question`       | `question`                   | is this entry an open question pinning a gap?                                                                    |
|       40 | `lens-entity`         | `entity`                     | is the subject a proper noun — a person, institution, theory, framework, or method?                              |
|       50 | `lens-process`        | `process`                    | is this entry a multi-stage sequence with named transitions?                                                     |
|       60 | `lens-insight`        | `insight`                    | does this entry name a non-trivial relationship between 2+ existing concepts?                                    |
|       99 | `lens-concept`        | `concept`                    | otherwise: one idea, explained on its own terms.                                                                 |

`lens-policy-tier` is structured as a single lens that resolves to one of three categories (`policy`, `guideline`, `essay`) based on the binding force the rule claims. its `lens_covers_category` is the multi-value list `[policy, guideline, essay]` (an exception to the otherwise single-value field). the lens body contains a sub-decision tree:

1. does the rule bind agent behavior, with violations producing blocking findings? → `policy`.
2. does the rule advise behavior, with violations producing advisory findings? → `guideline`.
3. is the rule under development, not yet ratified, binding nothing? → `essay`.

### 7.3 the seed lens set — annotation

annotation lenses do not compete. each runs on every relevant entry and stamps its own frontmatter field.

| slug                  | stamps field        | values                                                              | applies to                                                                |
| --------------------- | ------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `lens-notability`     | `notability_status` | `passes` / `borderline` / `fails`                                   | every candidate content unit at unpack                                    |
| `lens-evidence-grade` | `evidence_grade`    | `A` / `B` / `C` / `D`                                               | claim and relation entries                                                |
| `lens-high-stakes`    | `high_stakes_class` | `none` / `medical` / `legal` / `safety` / `identifiable-individual` | every claim entry; concept entries that contain claims                    |
| `lens-confidence`     | `confidence`        | `high` / `medium` / `low` / `contested`                             | every content entry                                                       |
| `lens-recency`        | (a tag in `tags`)   | `time-bounded` if applicable                                        | claim and source entries                                                  |
| `lens-edit-hardness`  | `edit_hardness`     | one of the five tiers                                               | every entry; default set by `classified_by`, raised by domain inheritance |

annotation lenses run in a fixed order (the order above). later lenses may read earlier lenses' stamps; specifically, `lens-edit-hardness` reads `lens-high-stakes` to raise the default tier when the high-stakes class is not `none`.

### 7.4 lens entry schema

a lens entry's frontmatter (§4.3.1) declares its question, priority, kind, and the category it covers. its body is structured:

```markdown
# {Title}

## Lead

{1-2 sentence summary of when this lens applies.}

## Question

{The yes/no question the lens asks, restated for clarity.}

## Criteria

A unit matches this lens when **all** of the following are true:

1. {criterion 1, with worked example or counterexample}
2. {criterion 2, …}

## Worked examples

- "{Title of an existing entry}" — matches because {…}
- "{Title of an existing entry}" — does not match because {…}

## Notes

{Any qualifications or known edge cases.}
```

### 7.5 the classification protocol — how to classify a candidate

input: a draft body and partial frontmatter (everything except `category`, `classified_by`, and the annotation-stamped fields).

procedure:

1. **notability gate first.** apply `lens-notability` (§8). if the unit fails the notability test, write the unit's content into the parent entry's body and emit `finding-deferred-{parent-slug}-{topic}`. abort classification.
2. **decision-tree pass.**
   1. apply `lens-lens`. if the unit's body and frontmatter match the lens criteria, set `category: lens` and `classified_by: lens-lens`. proceed to annotation pass.
   2. otherwise, walk the remaining decision-tree lenses in ascending `lens_priority` order. for each lens, evaluate the criteria in §7.4's `## Criteria` section. first match wins. set `category` to that lens's `lens_covers_category`; set `classified_by` to that lens's slug.
   3. if no lens matches (rare; `lens-concept` at priority 99 is the catch-all), emit `finding-classification-gap-{candidate-id}` and halt classification for this unit. the finding is a coverage signal that the lens set needs extension.
3. **annotation pass.** run each annotation lens in the order listed in §7.3. each lens writes its own frontmatter field. lenses that don't apply to this kind (e.g., `lens-evidence-grade` on a `concept`) are skipped silently.
4. emit a classification record into the producing run's `## Notes` section: `classified candidate-id as {category} via {classified_by}; annotations: {…}`. the run entry under §25 captures this.

### 7.6 lens versioning

every lens entry has a `lens_version: N` field (integer, monotonically increasing). a lens edit increments the version. an entry's `classified_by` field implicitly references the lens version active at classification time, captured in the producing `run-*` entry's `lens_versions` map.

when a lens is edited, lint runs `lens-version-drift` over all entries classified by that lens. each entry is re-evaluated against the new criteria. mismatches produce `finding-classification-drift-{slug}` for review. resolution either reclassifies the entry (a normal edit) or records a `wontfix` justification on the finding.

---

## 8. the notability gate

### 8.1 the predicate

a unit deserves its own entry if and only if **at least one** of the following holds:

1. **multi-source coverage.** the unit is covered by at least two independent sources, where "independent" means the sources are not derivative of each other (translations, abridgements, and reprints are not independent).
2. **routing necessity.** the unit is referenced by at least N other entries (v0: N=2) that would have to use anchor links into a parent entry instead of a clean wikilink. a routing target reduces brittleness.
3. **explicit policy carve-out.** the unit is in a class declared notable by `policy-notability`. the seed list includes: any entry classified as `source`, `domain`, `lens`, `policy`, `guideline`, `essay`, `agent`, `agent-test`, or `discussion` (these are notable by virtue of their kind); any concept that names a foundational framework cited in primary literature.

### 8.2 the lens — `lens-notability`

stamps `notability_status: passes | borderline | fails`.

- **`passes`** — at least one of the predicates in §8.1 is satisfied.
- **`borderline`** — none of the predicates is satisfied at the moment of unpack, but the unit is referenced exactly once or is plausibly notable on its content. held in the pending-changes layer (§9.5).
- **`fails`** — clearly fails all predicates: a passing mention, a one-source asides, a unit better expressed inline.

### 8.3 staging and promotion

#### 8.3.1 staging

borderline units are staged as `pending-{run-id}-{slug}.md` files in `temp/` during phase 1. at phase 4 (closeout), borderline units that have not been promoted in this chapter are migrated to a per-source pending area at `raw/{source-slug}/pending/{slug}.md`. they remain there until promoted or retired.

#### 8.3.2 promotion

a borderline unit promotes to `passes` and becomes a regular entry under `wiki/entries/{slug}.md` when:

- a later sub-section, chapter, or source produces a wikilink to its slug, **or**
- a later ingestion adds a second independent source that mentions the unit.

promotion is mechanical: at every closeout, the pending area is walked, and any entry whose promotion condition is met is moved to `wiki/entries/`. a `run-promotion-{slug}` entry records the move and the trigger that satisfied the predicate.

#### 8.3.3 retirement

a borderline unit retires when:

- the source completes and the unit was never referenced (closeout of the final chapter), **or**
- the unit has been pending for 90 days without promotion (per `policy-notability`), **or**
- a later finding declares the unit a duplicate of an existing entry.

retirement is also mechanical. the unit is removed from `raw/{source-slug}/pending/`. a `run-retirement-{slug}` entry records the action and the reason. the unit's content remains preserved inside the parent entry's body (where it was also folded at unpack, per §17.3.4).

### 8.4 failed units

units stamped `fails` at unpack are folded into the parent entry's body in phase 1 (the staging step writes them into `temp/{parent-slug}.md` rather than as their own file). a `finding-deferred-{parent-slug}-{topic}` is emitted at the same time, indexing the deferred unit so a future ingestion can promote it if more material arrives. the finding's `severity` is `advisory`.

### 8.5 special cases

- a `claim` is always notable when it is being asserted in the body of another entry. claims do not pass through the notability gate the same way as concepts; instead, the gate decides whether the claim deserves its own `claim-{slug}` entry (yes if the claim has multiple inbound `supports`/`contradicts` relations, or carries `high_stakes_class != none`) versus living inline in the parent entry as a sentence with a citation.
- `relation` entries are notable iff they connect two notable entries and carry a load-bearing predicate (`supports`, `contradicts`, `supersedes`, `depends-on`, `instance-of`). casual cross-reference does not need a relation entry; a wikilink suffices.
- `question` entries are always notable. opening a question is an explicit act of pinning a gap.
- `disambiguation` entries are always notable. they exist precisely because more than one variant is notable.

---

## 9. edit-hardness, reputation, and pending changes

### 9.1 the five tiers

every entry carries `edit_hardness` in its common frontmatter. the value is one of:

| tier                 | gating rule                                                          | who edits                                    |
| -------------------- | -------------------------------------------------------------------- | -------------------------------------------- |
| `open`               | none                                                                 | any active agent in the population.          |
| `confirmed`          | reputation ≥ 30                                                      | confirmed agents and above.                  |
| `extended-confirmed` | reputation ≥ 60 **and** declared scope in one of the entry's domains | scoped, well-trusted agents.                 |
| `restricted`         | quorum of 3 agents at reputation ≥ 80, **or** human reviewer         | meta-rule edits, lens edits, runtime policy. |
| `locked`             | human reviewer only                                                  | runtime-critical entries only.               |

reputation is a 0.0–100.0 scale (§9.6). the thresholds above are v0 placeholders; they live in `policy-edit-hardness` and are revised against measured population behavior.

### 9.2 default tiers per kind

| kind                                           | default tier                                                |
| ---------------------------------------------- | ----------------------------------------------------------- |
| `concept`, `illustration`, `application`       | `open`                                                      |
| `entity`, `process`, `insight`                 | `open`                                                      |
| `claim`, `relation`, `question`                | `open`                                                      |
| `structure-note`                               | `confirmed`                                                 |
| `disambiguation`                               | `confirmed`                                                 |
| `source`                                       | `confirmed` (changes to summary, key ideas, connections)    |
| `domain`                                       | `restricted`                                                |
| `lens`                                         | `restricted`                                                |
| `policy`                                       | `restricted`                                                |
| `guideline`                                    | `extended-confirmed`                                        |
| `essay`                                        | `open`                                                      |
| `agent`                                        | `extended-confirmed` (mutate); `restricted` (retire)        |
| `run`, `finding`, `discussion`, `notification` | `locked` (immutable; new run entry replaces)                |
| `agent-test`                                   | `extended-confirmed`                                        |
| `pending`                                      | the proposing agent edits its own; reviewer edits on accept |

defaults are floors. an entry's `edit_hardness` may be raised by:

- the classifying lens (e.g., a lens for "high-confidence load-bearing concepts" raises to `confirmed`).
- domain inheritance (§15.2): if any of the entry's domains has `edit_hardness_floor` above the default, the floor takes effect.
- explicit promotion via `policy-edit-hardness-promote` (a discussion-driven event).

an entry's `edit_hardness` is never lowered by ordinary edits. demotion requires `policy-edit-hardness-demote` and a meta-rule quorum.

the table above describes steady-state (phase 2+) defaults. **in phase 1 (§1.6.1), `lens`, `policy`, `guideline`, `essay`, `domain`, and `agent` entries are effectively `locked` against any agent write regardless of these defaults.** the §9 machinery applies to content kinds normally; structural kinds are out of reach until phase 2.

### 9.3 the pending state

below `open` sits a parallel state: `pending`. writes from agents below the `confirmed` reputation threshold do not land directly. they accumulate as `pending-{run-id}` proposal entries (§4.3.21) attached to the target entry.

a confirmed agent (or a human reviewer during seed) processes pending proposals. each proposal has one of three outcomes:

- **accept**: the proposal merges into the target entry. a `run-merge-{slug}` records the merge, names the reviewer, and the proposal is marked `status: accepted`.
- **reject**: the proposal does not merge. the proposal is marked `status: rejected`. a `notification-rejection-{run-id}` is sent to the proposer.
- **supersede**: a later proposal addresses the same target with overlapping content. earlier proposals are marked `status: superseded` with a pointer to the superseding one.

### 9.4 quorum

a quorum action requires:

- 3 agents, each at reputation ≥ 80, voting independently within a 7-day window, **or**
- 1 human reviewer.

quorum applies to:

- meta-rule edits (`policy-*` at `restricted` tier, edits to this specification, edits to `lens-lens`).
- agent retirement.
- lens demotion or removal.
- domain `contentious` flag toggle (§15.3).
- `wontfix` resolution of a `severity: blocking` finding.

quorum runs are recorded as `run-quorum-{action}` entries that link to each voter's vote (a `notification-vote-*` per voter) and to the action they ratify.

### 9.5 pending-changes mechanics, in detail

#### 9.5.1 when an agent's write becomes a pending proposal

the runtime intercepts the write at submission time, examines:

1. the target entry's `edit_hardness`.
2. the agent's reputation.
3. the agent's `slice.write_domains` overlap with the target's `domains`.

if (reputation ≥ tier-threshold) and (target's domains ∩ slice.write_domains) is non-empty, the write lands directly. otherwise, it is converted to a `pending-{run-id}-{target-slug}.md` entry. the original agent's run records the conversion.

#### 9.5.2 the proposal entry

frontmatter per §4.3.21. body is the proposed content for `proposal_kind: create`, or a unified diff for `proposal_kind: modify`. the proposal lives at `wiki/entries/pending-{run-id}-{target-slug}.md`. it is itself an entry, indexed and linked, but it does not affect the target entry's content until accepted.

#### 9.5.3 the review flow

reviewers (confirmed-or-above agents) read the noticeboard `_meta/noticeboards/pending-changes.md` (§23) to find proposals to review. for each:

1. read the proposal's diff or body.
2. read the target entry.
3. apply the merge rules in §19 mentally.
4. either:
   - **accept**: write the merged content to the target. mark the proposal `status: accepted`. emit `run-merge-{target-slug}`. update the target's `updated` field.
   - **reject**: mark `status: rejected`. emit `notification-rejection-{proposal-slug}` to the proposer. write a one-line justification into the proposal's `wontfix_justification` field-equivalent (or a new field `rejection_justification`).
5. if the proposal stays unreviewed for >14 days, lint emits `finding-stale-pending-{run-id}`. unreviewed proposals do not auto-accept.

#### 9.5.4 borderline-notability units share this mechanism

a borderline-notability unit (§8.3.1) lives in the same proposal flow but with `proposal_kind: create` and a target slug under `wiki/entries/{slug}.md` that does not yet exist. promotion (§8.3.2) is the act of accepting the proposal.

### 9.6 reputation

#### 9.6.1 sources of reputation gain

| event                                                                                       | delta             |
| ------------------------------------------------------------------------------------------- | ----------------- |
| agent-test passes (per test, per run)                                                       | +0.1              |
| editor agent's `run-edit` produces an entry that passes lint                                | +0.5              |
| editor agent's contribution is cited (wikilinked) by an entry produced by a different agent | +0.2 per citation |
| editor agent raises a finding that is later resolved (not wontfix)                          | +1.0              |
| editor agent's claim is relied on by a later `relation: supports`                           | +0.3 per relation |
| persona agent's slice passes a quarterly assessment                                         | +2.0              |
| lint agent flags an issue that becomes a confirmed finding                                  | +0.2              |
| agent participates in a discussion that closes-resolved within bound                        | +0.5              |
| external anchor: agent's work is rated highly by a human reviewer or the thesis-eval panel  | +5.0              |

#### 9.6.2 sources of reputation loss

| event                                                                                        | delta |
| -------------------------------------------------------------------------------------------- | ----- |
| agent-test fails                                                                             | -0.5  |
| agent's contribution is reverted via discussion                                              | -1.5  |
| agent introduces a finding that turns out to be a false positive                             | -0.5  |
| agent's pending proposal is rejected                                                         | -0.3  |
| agent's contribution is wontfix-ed (acknowledging it was malformed but not actively harmful) | -0.5  |
| agent fails to act on a notification within deadline                                         | -0.1  |
| a human reviewer flags the agent's work as low quality on the external anchor                | -3.0  |

#### 9.6.3 the external anchor

reputation, computed only from in-population events, drifts. the external anchor binds it back. weights between internal events (§9.6.1, §9.6.2) and external events (human review, thesis-eval panel measurements) are set in `policy-reputation-weighting`. v0 weight: external events count for **3×** their internal-event equivalent. weights are recalibrated annually or when policy-thesis-eval registers a change in variance reduction.

#### 9.6.4 starting reputation

new agents start at reputation = 5.0. this puts them squarely below `confirmed` (30). promotion to `confirmed` requires sustained scored work (a few dozen runs that each produce small gains, plus avoidance of major losses).

#### 9.6.5 reputation decay

reputation does not decay automatically. an agent that stops running stays at its last known reputation. if the agent is later reactivated and produces work, scoring resumes.

#### 9.6.6 reputation is not a market signal

reputation is a **permission** mechanism. it gates access to higher-edit-hardness regions. it is not transferable between agents, not bartered, and not used for any economic purpose. agents do not "spend" reputation; reputation rises and falls based on scored work.

---

## 10. connections — claims, relations, questions

### 10.1 claims as atoms

a **claim** is the smallest verifiable assertion the vault recognizes.

#### 10.1.1 segmentation rule (`policy-claim-segmentation`, v0)

split a sentence into multiple claims when:

1. the sentence carries more than one verifiable assertion that could independently be true or false.
2. the assertions are qualified differently (e.g., "X is true under condition Y, but Z under condition W" — two claims).
3. the assertion is the locus of a known disagreement in the field (split at the disagreement boundary).

do not split when:

- the sentence's parts are bound by causation or sequence such that one cannot be true without the other.
- the split would produce a fragment that needs context from a sibling sentence to be interpretable.

if uncertain, prefer the coarser claim in v0 — fragmentation is harder to reverse than splitting later.

#### 10.1.2 evidence grades

| grade | meaning                                                                                                 |
| ----- | ------------------------------------------------------------------------------------------------------- |
| `A`   | primary literature: peer-reviewed empirical studies, meta-analyses, or original derivations from those. |
| `B`   | secondary scholarly: textbooks, review articles, expert syntheses citing primary work.                  |
| `C`   | popular or applied: well-regarded practitioner books, expert essays, applied references.                |
| `D`   | anecdotal: single-case reports, blog posts, opinion pieces, claims without traceable evidence.          |

claims default to the lowest grade their sources support. multi-source claims take the grade of their strongest source unless there is contradiction (in which case `confidence: contested` is set and grade reflects the contradiction).

#### 10.1.3 in-domain evidence-grade floor

a domain entry's `evidence_grade_floor` sets the minimum grade for new claims in that domain. claims below the floor produce `finding-evidence-below-floor-{slug}` on creation. resolution: improve the evidence (find a higher-graded source), retire the claim, or escalate to `wontfix` with rationale.

### 10.2 relations as typed edges

a **relation** is a directed, typed edge between two entries, carrying its own evidence.

#### 10.2.1 predicates

| predicate     | meaning                                                                                                |
| ------------- | ------------------------------------------------------------------------------------------------------ |
| `supports`    | A's content makes B more likely to be true (or, if B is a process, makes B's outcome more achievable). |
| `contradicts` | A's content makes B less likely to be true.                                                            |
| `instance-of` | A is a specific case of B.                                                                             |
| `supersedes`  | A is a newer or more accurate version of B; B is retained for history.                                 |
| `depends-on`  | A cannot be applied or evaluated without B in context.                                                 |

`is-a` is **not** a predicate; use `instance-of`. `related-to` is **not** a predicate; that's a wikilink. relation predicates are load-bearing only when retrieval can traverse them and reasoning over them is meaningful.

#### 10.2.2 when to formalize as a relation entry

formalize when at least one is true:

- the predicate is in the load-bearing set (`supports`, `contradicts`, `supersedes`, `depends-on`, `instance-of`).
- the relation carries evidence that is not visible in either endpoint.
- the relation is itself the locus of a discussion or contradiction.

inline `## Connections` entries with informal predicates ("Related to", "Coined by") do not require a relation entry.

#### 10.2.3 relation entry placement

a relation between entries A and B with predicate `P` lives at `wiki/entries/relation-{a-slug}-{p}-{b-slug}.md`. the slug is deterministic and prevents duplicates.

### 10.3 questions

a **question** is an explicit gap. an editor or lint agent opens a question when:

- ingestion noticed a topic referenced but not explained.
- assessment found a domain whose canonical questions list has a gap.
- a discussion's closure produced a residual unanswered question.

#### 10.3.1 question lifecycle

```
open → answered → closed
        ↘ partially-answered
              ↘ refined → open (as a narrower question)
```

closing a question requires an entry, claim, or relation that resolves it. the resolving artifact is named in the question's `closes_when` field at opening; if the resolving artifact is added later, the closeout records the link. lint `unanswered-old-question` fires for questions older than 6 months without progress.

---

## 11. structure notes

### 11.1 purpose

a structure note holds a region of the graph together. it is the substrate's answer to "how do you carry big information without imposing a hierarchy."

### 11.2 body conventions

a structure note's body is **organizing prose plus annotated links**. the structure is not free-form:

```markdown
# {Cluster Title}

## Lead

{1–3 sentences compressing the cluster's shape: what's in it, what's at stake, what frames it.}

## How the cluster is held together

{2–4 paragraphs describing the cluster's organizing logic — the dominant axis, the major sub-regions, the unresolved tensions, the cross-domain bridges.}

## Load-bearing entries

- [[concept-1]] — annotation: {what role this entry plays in the cluster, in 1–2 sentences}
- [[concept-2]] — annotation: ...
- [[insight-3]] — annotation: ...

## Subregions or themes

### {Subregion 1}

{1 paragraph describing the subregion, with annotated links.}

- [[entry-a]] — {one-line annotation}
- [[entry-b]] — {one-line annotation}

### {Subregion 2}

...

## Open questions in this cluster

- [[question-{slug}]] — {one-line context}
- [[question-{slug}]] — ...

## Cross-cluster bridges

- [[other-structure-note]] — {how the two clusters relate}
- [[other-structure-note]] — ...
```

### 11.3 multiple structure notes per cluster

a cluster may be held together by more than one structure note, each from a different `domain_frame`. for example:

- `structure-memory-learning-theory.md` — frames "memory" through the cognitive-mechanism lens.
- `structure-memory-neuroscience.md` — frames "memory" through the brain-mechanism lens.
- `structure-memory-pedagogy.md` — frames "memory" through the teaching-practice lens.

each structure note is a peer; none is the canonical "parent" of the cluster. consumers query the frame they need.

### 11.4 coverage findings

lint `structure-note-coverage`:

- finds every connected component of content entries above size threshold (v0: 8 entries connected by wikilinks).
- checks whether at least one structure note has the component's entries in its `organizes` frontmatter list.
- if not, emits `finding-cluster-without-structure-note-{cluster-id}` with severity `advisory`. the cluster id is generated deterministically from the sorted slug list.

resolution: an editor (or a lint agent with confirmed reputation) writes a structure note. the finding closes when the structure note's `organizes` list covers the cluster.

### 11.5 structure note merge rule

per §19.7. summary: the body's organizing prose may be consolidated; the load-bearing entries list and subregion annotations are append-only.

---

## 12. domains

### 12.1 the domain entry

a domain is itself an entry under `wiki/entries/{domain-slug}.md`. its frontmatter (§4.3.13) carries the domain's metadata; its body declares scope, purpose, and load-bearing entries.

### 12.2 domain entry body

```markdown
# {Domain Title}

## Lead

{1–2 sentences describing the domain's scope.}

## Scope

{What this domain covers, in prose.}

## Out of scope

{What this domain explicitly excludes, even if it might appear adjacent.}

## Canonical questions

- [[question-{slug}]] — the central open question
- [[question-{slug}]] — ...

## Load-bearing structure notes

- [[structure-{slug}]] — frame: {frame name}
- [[structure-{slug}]] — frame: {frame name}

## Subscribed editor agents

- [[agent-{slug}]] — write scope: {summary}
- [[agent-{slug}]] — ...

## Sourcing standards

- minimum evidence grade: {A/B/C/D} (matches `evidence_grade_floor`)
- mandatory citation: {yes/no — derived from contentious flag}

## Related domains

- [[other-domain]] — relationship
```

### 12.3 contentious flag mechanics

setting `contentious: true` raises floors across every entry whose `domains` list includes this domain:

| dimension                                   | non-contentious default                        | contentious override                                                                               |
| ------------------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| minimum evidence grade for new claims       | as set by `evidence_grade_floor` (default `D`) | one grade higher (`D`→`C`, `C`→`B`, `B`→`A`); never below `B` regardless of `evidence_grade_floor` |
| default `edit_hardness` for new entries     | per §9.2                                       | one tier higher                                                                                    |
| maximum discussion rounds before escalation | 5 (§22.4)                                      | 3                                                                                                  |
| citation of source for every claim          | recommended                                    | mandatory; lint blocks merge of claims without sources                                             |

setting `contentious: true` on a domain is a `restricted`-tier edit; it requires meta-rule quorum. unsetting is identical.

### 12.4 in-domain edit by non-subscribed agent

when an agent edits an entry whose `domains` includes a domain the agent does not subscribe to:

- the write is permitted if the agent's reputation and the entry's `edit_hardness` allow it.
- an advisory finding `finding-domain-non-subscriber-edit-{slug}` is emitted, listing the agent and the domain.
- subscribed editor agents in that domain are notified.

this is the wikiproject pattern: not a permission gate, but visibility into who is editing what. systematic non-subscriber edits in a domain are a signal that the subscription list needs updating, not necessarily that the edits are wrong.

### 12.5 adding and removing domains

#### 12.5.1 adding a domain

1. draft a domain entry under `wiki/entries/{domain-slug}.md`.
2. classify via the domain lifecycle protocol (`produced_by: lifecycle-domain-create`).
3. open at least one `question-{slug}` for the domain's canonical questions list.
4. seed the domain entry's `subscribed_agents` (may be empty initially).
5. create `wiki/_meta/indexes/{domain-slug}.md` as a placeholder; first index rebuild populates it.

#### 12.5.2 removing a domain

1. every entry whose `domains` list includes the domain must be reassigned. lint `unassigned-domain-removal` blocks the removal until reassignment is complete.
2. the domain entry's `lifecycle_stage` flips to `retired`. it remains in `wiki/entries/` for history but stops appearing in fresh assessments.
3. `wiki/_meta/indexes/{domain-slug}.md` is moved to `wiki/_meta/indexes/_retired/{domain-slug}.md`.

---

## 13. policy, guideline, essay — the three-tier rule system

### 13.1 the three tiers, summarized

| tier        | binds?       | violation produces                               | edit-hardness default |
| ----------- | ------------ | ------------------------------------------------ | --------------------- |
| `policy`    | yes          | blocking finding                                 | `restricted`          |
| `guideline` | no (advises) | advisory finding                                 | `extended-confirmed`  |
| `essay`     | no           | no finding (essays are content, not enforcement) | `open`                |

### 13.2 distinguishing tiers — lens criteria

`lens-policy-tier` (priority 5) walks this sub-decision-tree:

1. does the rule, when violated, produce a blocking finding that prevents merge or downgrades quality? → `policy`.
2. does the rule, when violated, produce an advisory finding that does not block but is reviewed? → `guideline`.
3. is the rule under development, with the explicit understanding that it has not been ratified? → `essay`.

a rule cannot be both `policy` and `guideline`. promotion (§13.4) is the only legitimate tier change.

### 13.3 the body of a rule entry

```markdown
# {Rule Title}

## Lead

{1-2 sentences stating what the rule says.}

## Rule

{The rule itself, in normative language. "Editors must…", "An entry should…", "Lint flags…"}

## Rationale

{Why this rule exists. The motivating failure mode, the problem it prevents, the goal it serves.}

## How violation is detected

- {Lint rule name and its `severity`}
- {Manual review trigger, if any}

## Examples

- A passing case: {…}
- A failing case: {…}

## Promotion history

{For entries that have been promoted, list the path:}

- 2026-04-01: created as `essay`.
- 2026-05-15: promoted to `guideline` via [[discussion-{slug}]].
- 2026-07-22: promoted to `policy` via [[discussion-{slug}]].
```

### 13.4 the promotion path

#### 13.4.1 essay → guideline

triggered by:

- the essay has been cited (wikilinked) by at least 3 other entries (any kind).
- a discussion has been opened proposing promotion, and the discussion closed with `closed-resolved` outcome.
- at least one author of the essay and one independent agent at reputation ≥ 60 endorsed the promotion in the discussion.

mechanics: the entry's `category` flips from `essay` to `guideline`. its `edit_hardness` is raised to `extended-confirmed`. its `promotion_history` gains an entry. the promotion is a single `run-promotion-{slug}` recording the move.

#### 13.4.2 guideline → policy

triggered by:

- the guideline has at least 5 advisory findings whose resolution cited the guideline as the rule.
- a discussion has closed proposing promotion.
- meta-rule quorum (§9.4) ratifies.

mechanics: `category: guideline` → `policy`. `edit_hardness` raised to `restricted`. `linted_by` field populated with the lint rule that now enforces blocking. `promotion_history` updated. `run-promotion-{slug}` records.

#### 13.4.3 demotion

a policy may demote to guideline (or further) if:

- the rule has produced no findings in 12 months **and**
- a discussion proposing demotion closes-resolved **and**
- meta-rule quorum ratifies.

a guideline may demote to essay similarly. demotion is rare; the design intent is forward growth, not churn.

#### 13.4.4 retirement

a rule entry is retired (not deleted) when its content is fully subsumed by another rule, or when the rule's premise is invalidated. retirement: `lifecycle_stage: retired` (an additional infrastructure-frontmatter field for rule entries; see §35.4). the retired rule remains in `wiki/entries/` for history.

### 13.5 essays as content vs. policies as content

essays sit at the boundary of "vault content" and "vault rules." they are content (free-form prose, edited by anyone, no enforcement) but they speak about how the vault should work. this is intentional: essays are how the population proposes new rules to itself. lint does not enforce essays; readers do.

### 13.6 phase-1 lockdown applies to all three tiers

despite their nominally different `edit_hardness` defaults (§9.2), in phase 1 (§1.6.1) all three tiers — `policy`, `guideline`, and `essay` — are locked against agent writes. essays are locked because authoring an essay is a structural act of proposing a future rule. only the human bootstrap (§30) and human-initiated `run-spec-amend-*` may write rule entries in phase 1. promotion paths (§13.4) are inert until phase 2.

---

## 14. high-stakes claims

### 14.1 the classes (v0)

| class                     | examples                                                                                                     |
| ------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `medical`                 | claims about clinical efficacy, dosage, contraindications, diagnostic procedures, treatment recommendations. |
| `legal`                   | claims about legal liability, statutory requirements, regulatory compliance, court rulings.                  |
| `safety`                  | claims about physical safety, accident risk, hazard procedures, emergency response.                          |
| `identifiable-individual` | claims about specific named living people (analog of wikipedia's BLP).                                       |
| `none`                    | the default; claim is not high-stakes.                                                                       |

new classes may be added by amending `policy-high-stakes`. addition is a meta-rule edit.

### 14.2 the lens — `lens-high-stakes`

stamps `high_stakes_class` on every claim entry and on concept entries that contain inline claims.

criteria for stamping:

- **`medical`** — the claim is about a human-health intervention, condition, or biological mechanism, **and** the claim is consequential for choosing or refusing care. abstract physiology that does not direct care is `none`.
- **`legal`** — the claim asserts a legal status, requirement, or consequence, **and** acting on the claim could expose the agent or a reader to legal risk.
- **`safety`** — the claim is about a procedure, threshold, or condition where being wrong creates physical risk to a human.
- **`identifiable-individual`** — the claim identifies a specific living person and asserts something contestable about them (their actions, their views, their character, their associations).
- **`none`** — none of the above.

multi-class is not allowed; a claim that fits two classes takes the highest-stakes class (medical > legal > safety > identifiable-individual).

### 14.3 the asymmetric removal regime

if a claim is stamped `high_stakes_class != none` **and** its evidence grade is below the high-stakes floor (v0: floor = `B` for `medical` and `legal`; `B` for `safety`; `A` for `identifiable-individual`), the asymmetric removal regime fires.

#### 14.3.1 mechanics on creation

at unpack (phase 2), if a candidate claim fails the floor:

1. the claim is **not** written into the staging entry. instead, a placeholder string is left at the location: `> [HIGH-STAKES CLAIM REMOVED — see [[finding-{slug}]]]`.
2. a `finding-high-stakes-removal-{candidate-id}` is emitted with `severity: blocking`, status `open`. the finding records the original claim text, the source pointer, and the gap (which evidence grade was needed).
3. the parent entry's `confidence` is downgraded by one tier (`high` → `medium`, `medium` → `low`, etc.) until the finding resolves.
4. retrieval treats the placeholder string as a non-fragment (it is not returned as a candidate fragment).

#### 14.3.2 mechanics on existing entries

if `lens-high-stakes` re-runs on an existing entry (e.g., after the policy class set is amended) and finds a claim that was previously stamped `none` but should now be a high-stakes class with insufficient evidence, the same regime fires retroactively:

1. the claim is replaced by the placeholder.
2. a `finding-high-stakes-removal-{slug}` is emitted.
3. the entry's `updated` field changes; a `run-high-stakes-retroactive-{slug}` records.

#### 14.3.3 reinstatement

a finding closes when:

- a new source provides evidence at or above the floor.
- a confirmed agent edits the parent entry, replacing the placeholder with the cited claim.
- the run is recorded; the finding's `status` flips to `resolved`.

### 14.4 high-stakes regime is orthogonal to evidence grade

the evidence grade describes the evidence; the high-stakes class describes the **action when evidence is weak**. a `B`-grade claim is acceptable for ordinary content and unacceptable for `medical` content. graders do not need to know the high-stakes class to grade evidence; the action layer responds to the asymmetry.

### 14.5 high-stakes noticeboard

`wiki/_meta/noticeboards/high-stakes.md` lists every open `finding-high-stakes-removal-*`. specialized review agents (and human reviewers) subscribe to this board. it rebuilds on every closeout that produces a high-stakes finding.

---

## 15. contentious domains

### 15.1 declaration

a domain becomes contentious by setting its `contentious` frontmatter field to `true`. this is a `restricted`-tier edit; meta-rule quorum required.

### 15.2 elevated rules — exact mechanics

when an entry's `domains` list includes a contentious domain:

| rule                                        | non-contentious                                                           | contentious                                                                         |
| ------------------------------------------- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| minimum evidence grade for new claims       | per `evidence_grade_floor` of all the entry's domains, take the strictest | one grade stricter; never below `B`                                                 |
| default `edit_hardness` for new entries     | per §9.2                                                                  | one tier higher                                                                     |
| maximum discussion rounds before escalation | 5                                                                         | 3                                                                                   |
| citation of source for every claim          | recommended                                                               | mandatory; missing source produces blocking finding `finding-source-missing-{slug}` |
| lead-section requirement                    | per §5.2.1 (size threshold)                                               | required regardless of size                                                         |
| stale-pending threshold for promotion       | 90 days                                                                   | 30 days                                                                             |

multiple contentious domains in the same entry compose: the strictest rule wins per dimension.

### 15.3 toggling contentious

flipping `contentious: false → true` on a domain entry triggers retroactive re-evaluation:

1. lint `domain-contentious-flag-change` runs over every entry whose `domains` includes the toggled domain.
2. each entry's `edit_hardness` is recomputed (raise only; never lower).
3. each claim in those entries is checked against the new floor; failures emit `finding-evidence-below-floor-{slug}`.
4. each entry's lead-section requirement is re-evaluated; missing leads emit `finding-lead-missing-{slug}`.

flipping `contentious: true → false` does **not** retroactively lower `edit_hardness` or evidence grades. it only relaxes the rule for future entries.

---

## 16. agents

### 16.1 agent kinds — the v0 population catalog

every agent is an entry under `wiki/entries/agent-*.md`. its frontmatter (§4.3.15) declares its kind, slice, prompt reference, lifecycle stage, and reputation. its body declares voice, prompt strategy, and behavioral notes. the runtime (`runner/`, §26.6) executes agents per their manifests.

#### 16.1.1 the three kinds

| `agent_kind` | what it does                                                                                                                                          | reads                                  | writes (direct)                                                                | produces                                                                                              |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| `editor`     | reads sources, writes content entries during ingestion. takes specific role (ingestion / reviewer / assessor / archiver / etc.) via `slice.role`.     | per `slice.read_domains`               | content entries within `slice.write_domains`, subject to edit-hardness gates  | `run-edit-*`, `run-merge-*`, `run-review-*`, `run-assess-*`, `run-archival-*`, `pending-*`, `finding-*` |
| `persona`    | answers queries against a declared slice; surfaces gaps; participates in content discussions                                                          | per `slice.read_domains`               | nothing direct — does not author content                                       | `run-persona-*`, `finding-persona-test-fail-*`, `discussion-*` participation, `notification-*`        |
| `lint`       | mechanical rule enforcement — runs continuously on writes and on schedule                                                                             | every entry under `policy_targets`     | nothing direct — emits findings                                                | `run-lint-*`, `finding-*`, `notification-*`                                                           |

a single agent is exactly one kind. a deployment may instantiate multiple agents per kind (e.g., one editor per source domain). there is no global "supervisor" agent in v0.

#### 16.1.2 editor sub-roles via `slice.role`

an editor's specific work pattern is declared in its manifest's `slice.role`:

| role                          | does                                                                  | minimum reputation tier                              |
| ----------------------------- | --------------------------------------------------------------------- | ---------------------------------------------------- |
| `ingestion`                   | runs phases 0–4 of the ingestion pipeline (§17). default for a domain editor. | `open` (writes land as pending below `confirmed`)    |
| `reviewer`                    | processes `pending-*` proposals (§9.5.3); accepts or rejects.         | `confirmed`                                          |
| `assessor`                    | runs assessment passes (§28); updates dashboards.                     | `confirmed`                                          |
| `archiver`                    | rolls up old runs, moves cold infrastructure to archive (§25.7, §26.3). | `confirmed`                                        |
| `structure-note-enrichment`   | updates structure notes during phase 4 (§17.6.1.3) without authoring fresh content. | `confirmed`                                          |
| `disambiguation-resolver`     | handles slug collisions per §6.4 in a dedicated review pass.          | `confirmed`                                          |

a single editor agent declares exactly one role per manifest. multi-role behavior requires multiple agent entries.

#### 16.1.3 humans are not agents

the human reviewer is a stand-in for `confirmed`-tier review during phase 1. they accept pending proposals, ratify quorum actions, approve agent promotions. their actions are recorded as `notification-approval-*` linked from the relevant runs. they have no agent manifest. once phase 2 begins, their role narrows to participation in quorum alongside agents (§1.6.2). in phase 3, the human reviewer step is removed entirely from the operational loop; humans still curate sources in and read retrieval out.

### 16.2 the agent manifest

every agent is described by an `agent-{slug}.md` entry. the manifest is the entry's frontmatter (§4.3.15) plus a body that elaborates voice, prompt strategy, and constraints. the body template:

```markdown
# {Agent Title}

## Lead

{1-2 sentences describing the agent's role, slice, and intended use.}

## Slice

- read domains: {list}
- write domains: {list, for editors only}
- voice rules: {for personas}
- refusal rules: {for personas}
- policy targets: {for linters}

## Prompt strategy

{The high-level shape of how this agent is prompted. Not the raw prompt itself — that lives in `runner/prompts/{slug}.md` outside the vault.}

## Reputation history

- {YYYY-MM-DD}: started at 5.0
- {YYYY-MM-DD}: +0.5 (entry passed lint)
- ...

## Seed tests

- [[agent-test-{slug}]]
- [[agent-test-{slug}]]

## Notes

{Any operational notes, known limitations, or behavioral quirks.}
```

### 16.3 lifecycle protocols

#### 16.3.0 phase 1 freeze

in phase 1 (§1.6.1), all three lifecycle protocols below are inert. agents are bootstrapped exclusively by humans (§29.6, §30). a runtime attempt to invoke any lifecycle protocol from an agent in phase 1 is rejected with `finding-phase-1-lockdown-violation-agent-{slug}`. the protocols are described here so the machinery is in place for phase 2; they execute only once `policy-phase` declares phase 2 active.

in phase 1, the only paths that mutate an `agent-*` entry are: (a) initial bootstrap by direct human authorship (§30); (b) a `run-spec-amend-*` that revises a manifest as part of a structural correction; (c) a human edit setting `lifecycle_stage: retired` on an agent that must be taken offline.

#### 16.3.1 `lifecycle-agent-create`

inputs: a draft agent manifest, a starting reputation, a list of seed tests.

procedure:

1. validate the manifest. all fields present; `slice` non-empty; `prompt_ref` resolves.
2. write the agent entry under `wiki/entries/agent-{slug}.md` with `lifecycle_stage: proposed`.
3. open a discussion `discussion-agent-create-{slug}` for review.
4. seed tests are run against a baseline vault state. a `run-agent-test-{test-slug}` per test records pass/fail.
5. on quorum approval (3 agents at reputation ≥ 80, or 1 human reviewer), `lifecycle_stage` flips to `active`.
6. `run-lifecycle-agent-create-{slug}` records the action.

#### 16.3.2 `lifecycle-agent-mutate`

inputs: an existing agent entry, a proposed change to manifest fields (slice, voice, prompt strategy, etc.).

procedure:

1. the change is submitted as a `pending-{run-id}-agent-{slug}` proposal.
2. review proceeds per §9.5.3.
3. on accept, the agent's manifest updates. a `run-lifecycle-agent-mutate-{slug}` records the change.
4. seed tests re-run against the new manifest. failures trigger automatic `lifecycle_stage: proposed` (the agent reverts to needing re-approval).

#### 16.3.3 `lifecycle-agent-retire`

inputs: an agent entry, a retirement justification.

procedure:

1. open `discussion-agent-retire-{slug}` linking the agent and the justification.
2. quorum required (`restricted` edit on the agent entry).
3. on quorum approval, `lifecycle_stage: retired`.
4. retired agents do not run, but their past `run-*` entries remain.
5. their reputation is preserved as a final state.

### 16.4 editor agents

editors carry `slice.write_domains`. their writes are subject to the per-entry `edit_hardness` and the agent's reputation. editors typically run on a per-source basis: one editor agent ingests one source over its chapters; the agent's reputation grows or shrinks based on how the source's writes pass lint and assessment.

### 16.5 persona agents

personas declare which entries they know deeply, conceptually, or only by name. they do not write content. they answer queries against their declared slice — this is how the vault tests that a slice of itself is internally coherent.

a persona's manifest carries `seed_tests` — questions whose expected-answer shape is human-authored. the persona answers; the answer is graded against the expected shape; pass/fail is logged. a failing seed test is `finding-persona-test-fail-{persona}-{test}`.

a persona's `voice_rules` describe tone, register, and formality; `refusal_rules` describe topics the persona explicitly does not answer (e.g., a learning-theory persona refuses medical-treatment questions).

### 16.6 lint agents

lint agents have `policy_targets` — the policies and guidelines they enforce. each lint agent runs:

- continuously: on every entry write that affects an entry under one of its `policy_targets`.
- scheduled: a full pass on the daily schedule (per `policy-archival` for budget allocation).

a lint agent's only output is `finding-*` entries and `notification-*` entries.

### 16.7 agent reputation interaction with edit-hardness

the runtime checks reputation at write time, not in advance. an editor agent attempting to write to an `extended-confirmed` entry must satisfy reputation ≥ 60 **and** declared scope in one of the entry's domains. if either check fails, the write becomes a pending proposal.

### 16.8 where agents discuss

agents discuss via `discussion-*` entries (§22). discussions are the only sanctioned channel for agent-to-agent disagreement; ad-hoc conversation outside discussion entries is not part of the model.

#### 16.8.1 when a discussion opens

per §22.1, a discussion opens when:

- two agents disagree on the content of an entry.
- a contradiction is raised between two claims and authors disagree on resolution.
- a classification is contested (one agent argues a different lens should have ruled).
- a promotion is proposed (essay → guideline → policy).
- a wontfix justification is challenged.
- an agent retirement is proposed.

opening a discussion is the write of a new `wiki/entries/discussion-{disputed-slug}-{disambiguator}.md`. the opening agent populates the disputed object, the participants, and the first round.

#### 16.8.2 how an agent participates

once a discussion exists, any active agent (subject to its `slice`) may add a round. each round is one statement per participant. discussions are bounded at 5 rounds (3 in contentious domains, §22.3). termination is decided by the protocol named in the discussion's frontmatter (`content-quorum`, `meta-rule-quorum`, or `human-escalation`, §22.4).

#### 16.8.3 phase 1 — discussions about structural objects are advisory

a discussion whose `disputed_object` is a structural entry (a `lens-*`, `policy-*`, `guideline-*`, `essay-*`, `domain`, `agent-*`, or this spec) may run in phase 1, but its termination is **advisory only**. the disputed object is not modified by the discussion's outcome until phase 2 ratifies the termination via meta-rule quorum.

advisory terminations produce `finding-deferred-structural-discussion-{slug}` for human review. the human reviewer (during phase 1) or the meta-rule quorum (in phase 2) decides whether to apply the discussion's outcome.

discussions whose `disputed_object` is a content entry (concept, claim, relation, illustration, application, insight, process, entity, structure-note, disambiguation, question) terminate normally in phase 1.

### 16.9 phase-1 lockdown — what agents cannot edit

in phase 1 (§1.6.1), agent writes to entries of the following kinds are rejected by the runtime regardless of reputation. this overrides the §9.2 default tiers for these kinds.

| entry kind                            | rationale                                                                                            |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `lens`                                | classification rules. changing them changes how every later entry is classified.                     |
| `policy`, `guideline`, `essay`        | rule entries at every tier. changing a policy changes lint enforcement; authoring an essay is a structural act of proposing a future rule. |
| `domain`                              | the subject axes. adding or removing one reshapes coverage and indexes.                              |
| `agent`                               | the population manifest. creating or mutating an agent redefines who acts.                           |
| this specification                    | the master rule.                                                                                     |

rejected writes produce `finding-phase-1-lockdown-violation-{target-slug}` with `severity: blocking`. the rejecting check is pre-write — no reputation is consumed and no partial state is written.

agents may **read** all locked entries. agents may **discuss** locked entries (§16.8.3) — but discussion termination is advisory until phase 2.

phase 2 unlocks every kind in this table. the unlock is itself a `policy-phase` amendment requiring meta-rule quorum.

### 16.10 actions × entities matrix (phase 1)

the complete map of read / write / produce permissions for each agent kind in phase 1. this is the canonical answer to "what can each agent do."

legend:
- ✅ — direct write allowed, gated by per-entry `edit_hardness` and agent reputation per §9.
- 🅿️ — write allowed but converted to `pending-*` proposal when agent reputation < `confirmed` (per §9.5).
- 🅿️→✅ — same write, but accepted via reviewer flow (§9.5.3).
- 🟡 — read-only.
- 🚫 — phase-1 lockdown; runtime rejects writes pre-check (§16.9).

| entry kind                                                              | `editor` (ingestion)                              | `editor` (reviewer)               | `persona`                       | `lint`                          |
| ----------------------------------------------------------------------- | ------------------------------------------------- | --------------------------------- | ------------------------------- | ------------------------------- |
| concept, illustration, application, entity, process, insight            | ✅ / 🅿️                                          | 🅿️→✅                            | 🟡                              | 🟡                              |
| claim, relation                                                         | ✅ / 🅿️                                          | 🅿️→✅                            | 🟡                              | 🟡                              |
| structure-note                                                          | ✅ / 🅿️ (≥ `confirmed` default)                 | 🅿️→✅                            | 🟡                              | 🟡                              |
| source (summary, key ideas, connections only — body text is immutable)  | ✅ / 🅿️                                          | 🅿️→✅                            | 🟡                              | 🟡                              |
| disambiguation, question                                                | ✅ / 🅿️                                          | 🅿️→✅                            | 🟡                              | 🟡                              |
| lens, policy, guideline, essay, domain, agent, this spec                | 🚫                                                | 🚫                                | 🚫                              | 🚫                              |
| run                                                                     | ✅ (own only; immutable after write)              | ✅ (own)                          | ✅ (own)                        | ✅ (own)                        |
| finding                                                                 | ✅ (raise)                                        | ✅ (resolve / wontfix)            | ✅ (raise)                      | ✅ (raise)                      |
| discussion                                                              | ✅ (open + rounds, content disputes)              | ✅ (terminate)                    | ✅ (open + rounds, content)     | ✅ (open + rounds, lint disputes) |
| notification                                                            | ✅ (send)                                         | ✅ (send + mark acted)            | ✅ (send)                       | ✅ (send)                       |
| pending                                                                 | ✅ (propose own)                                  | ✅ (accept / reject / supersede)  | n/a                             | n/a                             |

phase 2 transforms every 🚫 cell into 🅿️→✅ via the meta-rule quorum (§9.4). no other change to this matrix.

---

## 17. the ingestion pipeline

### 17.1 phase shape

```
phase 0: source intake  (once per source)
  ↓
phase 1: chapter setup  (once per chapter)
  ↓
phase 2: per-sub-section staging  (repeated across sub-sections)
  ↓
phase 3: chapter merge  (once per chapter)
  ↓
phase 4: chapter closeout  (once per chapter)
  ↓
[loop back to phase 1 for next chapter]
  ↓
source completion  (once, after all chapters)
```

### 17.2 phase 0 — source intake (once per source)

#### 17.2.1 inputs

- the raw source document.
- a candidate source slug.
- a candidate domain assignment (one or more existing domain slugs).

#### 17.2.2 steps

1. **place the source.** create `raw/{source-slug}/`. write the source document at `raw/{source-slug}/{source-slug}.md`. immutable from this point. add assets to `raw/{source-slug}/assets/` if any.
2. **create the process trace.** write `raw/{source-slug}/{source-slug}-process-trace.md` with:
   - title, author, year, isbn or equivalent identifier.
   - estimated total length (words, pages, chapters).
   - candidate domain assignment.
   - candidate high-stakes class for the source as a whole (if any).
   - editor agent assigned.
   - chapter list with `not-started` status for each row.
3. **draft or update the source entry.** at `wiki/entries/{source-slug}.md`:
   - frontmatter per §4.3.2 (and the common head per §4.1).
   - body with a `## Lead` (mandatory for sources), a `## Summary` (initial — to be enriched chapter by chapter), `## Key ideas` (empty, populated per chapter), `## Notable claims` (empty), `## Connections` (empty), `## Sources` (the source itself).
4. **classify domain inheritance.** for each domain in the source entry's `domains`:
   - read the domain entry's `contentious` flag.
   - record the in-domain `evidence_grade_floor`.
   - record the in-domain `edit_hardness_floor`.
   - record the subscribed editor agents.
5. **decide source-level high-stakes.** stamp the source entry's `high_stakes_class` based on the source's primary subject. medical textbook → `medical`. learning-theory book → `none`. recorded so `lens-high-stakes` knows the default during chapter passes.
6. **confirm editor agent.** the editor agent assigned to this source must:
   - have at least one of the source's domains in its `slice.write_domains`, **or**
   - run sub-confirmed (writes will land as pending proposals).
   - meet any in-domain reputation floor.
7. **emit `run-source-intake-{source-slug}`** recording the intake action.

#### 17.2.3 phase 0 output

- a populated `raw/{source-slug}/` folder.
- a draft source entry at `wiki/entries/{source-slug}.md`.
- a process trace listing chapters as `not-started`.

### 17.3 phase 1 — chapter setup (once per chapter)

#### 17.3.1 inputs

- the chapter index (chapter N).
- the process trace.

#### 17.3.2 steps

1. **mark chapter `in-progress`** in the process trace.
2. **clear `temp/`.** delete every file under `temp/`. preserve the directory.
3. **read the chapter.** identify 2–5 coherent sub-sections based on topic boundaries:
   - ≤25 pages: 2 sub-sections.
   - 25–40 pages: 2–3.
   - 40–60 pages: 3–5.
   - > 60 pages: 4–5.
4. **record sub-sections** as nested rows in the process trace, each `not-started`.
5. **create `temp/_staging-index.md`**:

   ```markdown
   # staging index — {source-slug} chapter {N}

   ## sub-sections

   - sub-section 1 (status): ...
   - sub-section 2 (status): ...

   ## staged so far

   (populated as phase 2 progresses)
   ```

6. **emit `run-chapter-setup-{source-slug}-{N}`**.

#### 17.3.3 phase 1 output

- a clean `temp/` with `_staging-index.md`.
- the chapter row marked `in-progress`.
- nested sub-section rows.

### 17.4 phase 2 — per-sub-section staging (repeated)

run this once per sub-section, in chapter order.

#### 17.4.1 inputs

- the sub-section text.
- the chapter context (preceding sub-sections' staged units).
- the source entry.

#### 17.4.2 steps for each sub-section

1. **read the sub-section.** identify candidate knowledge units. a candidate is a coherent assertion or coherent grouping of assertions about a single subject.
2. **for each candidate unit, draft body and partial frontmatter.**
   - draft the body. write **blind** with respect to any existing entry that might exist on this topic (do not read `wiki/entries/{slug}.md` before writing; this eliminates anchoring bias).
   - draft the common-head frontmatter, leaving `category`, `classified_by`, and the annotation-stamped fields blank.
3. **run the notability gate.** apply `lens-notability` per §8.2.
   - `passes`: proceed to step 4.
   - `borderline`: stage the unit as `temp/pending-{run-id}-{slug}.md` per §8.3.1. do not classify further; continue with the next candidate.
   - `fails`: fold the unit's content into the parent entry's body (the parent is the entry the candidate would have nested under — usually a concept entry being staged in this same sub-section). emit `finding-deferred-{parent-slug}-{topic}` with `severity: advisory`. do not stage as a separate file.
4. **run the decision-tree.** classify per §7.5.2. set `category` and `classified_by`.
5. **run annotation lenses.** stamp:
   - `notability_status` — already done in step 3.
   - `evidence_grade` — for claim and relation entries.
   - `confidence` — every content entry.
   - `high_stakes_class` — claims and concepts that contain claims. apply the asymmetric removal regime per §14.3 if the resulting class is non-`none` and evidence is below floor.
   - `edit_hardness` — default per §9.2, then raised by domain inheritance and high-stakes stamps.
6. **pick a slug.** apply §6.3.
   - `new`: write into `temp/{slug}.md`.
   - `merges-with: {existing-slug}`: write into `temp/{slug}.md` using the same slug as the existing entry. do **not** read the existing entry. phase 3 will merge.
   - `extends: {temp-slug}`: open `temp/{temp-slug}.md` and enrich in place.
   - collision with a different subject: handle disambiguation per §6.4.
7. **lead-section requirement.**
   - if the entry's body exceeds the threshold (§5.2.1), draft a `## Lead` section explicitly.
   - if the entry is a structure note, source, or in a contentious domain, draft a `## Lead` regardless of size.
   - otherwise, the first sentence of the body is the implicit lead; no separate section.
8. **link to existing entries liberally.** every wikilink must resolve; if a referenced concept does not have an entry, either:
   - open a `question-{slug}` for it (and wikilink to the question), or
   - mark the link as a "link expected" and resolve in phase 4.
9. **update `temp/_staging-index.md`** with what was staged this sub-section.
10. **mark the sub-section row complete** in the process trace.

#### 17.4.3 sub-section invariants

after every sub-section completes:

- every candidate unit has been classified, folded, or staged pending.
- every staged file has valid frontmatter.
- every wikilink in staged files resolves (to existing entries, to entries staged earlier in this chapter, or to opened questions).
- `temp/_staging-index.md` is current.

if any invariant fails, the sub-section is **not** marked complete; the editor must repair before continuing.

### 17.5 phase 3 — chapter merge (once per chapter)

run after every sub-section is staged.

#### 17.5.1 inputs

- the contents of `temp/`.
- the existing `wiki/entries/`.

#### 17.5.2 steps

for each file in `temp/` (excluding `_staging-index.md` and any `pending-*`):

1. **look up `wiki/entries/{slug}.md`.**
2. **if no existing entry, the temp file becomes a new entry.**
   - move `temp/{slug}.md` to `wiki/entries/{slug}.md`.
   - emit `run-merge-create-{slug}`.
3. **if an existing entry, apply the per-kind merge rule** (§19).
4. **on `category` or `classified_by` mismatch between temp and existing**, halt the merge for that file and emit `finding-merge-classification-mismatch-{slug}` with `severity: blocking`. resolution is manual.
5. **on `high_stakes_class` mismatch**, halt and emit `finding-merge-high-stakes-mismatch-{slug}`.

for each `pending-*` file in `temp/`:

- migrate to `raw/{source-slug}/pending/{slug}.md`. these are borderline-notability units carried forward.

#### 17.5.3 phase 3 output

- `wiki/entries/` updated with the chapter's writes.
- `temp/` still contains: `_staging-index.md`, possibly `pending-*` files (which are migrated), and any merge-blocked files (which await manual repair).

### 17.6 phase 4 — chapter closeout (once per chapter)

#### 17.6.1 steps

1. **update the source entry's body.**
   - append to `## Key ideas` from this chapter.
   - append to `## Notable claims` from this chapter.
   - append to `## Connections` from this chapter.
   - update the source entry's `updated` field.
2. **structure-note coverage check.** lint `structure-note-coverage` runs on every cluster touched by this chapter. for any cluster of >8 entries without an associated structure note, emit `finding-cluster-without-structure-note-{cluster-id}` with `severity: advisory`.
3. **structure-note enrichment.** for every existing structure note that links to entries created or modified this chapter, the editor (or a structure-note-enrichment lint agent) updates the structure note's "Load-bearing entries" or "Subregions" sections. structure-note merge rules (§19.7) apply.
4. **notability promotion check.** walk every entry whose `notability_status` is `borderline`:
   - count inbound wikilinks created or updated this chapter that point at the entry's slug.
   - if the count crosses the promotion threshold (v0: 1 new inbound), promote per §8.3.2.
5. **high-stakes review.** walk every claim newly stamped `high_stakes_class != none`. if the asymmetric removal regime fired for any claim, ensure the placeholder and finding are in place; if the claim has improved evidence (e.g., a later sub-section provided primary literature), close the finding.
6. **lint sweep on touched entries.** run every relevant lint check (§20) over the entries this chapter touched. each finding is logged.
7. **pending-changes review.** if the editor agent ran sub-confirmed:
   - all writes from this chapter landed as `pending-*` proposals.
   - a confirmed agent (or human reviewer during seed) walks the proposals via §9.5.3.
   - until this step completes, the chapter's writes are not visible to retrieval.
8. **mechanical index rebuild.** run `pnpm build:vault-indexes`:
   - rebuild `wiki/_meta/index.md`.
   - rebuild every per-domain index file under `wiki/_meta/indexes/`.
9. **noticeboard rebuild.** rebuild affected noticeboards under `wiki/_meta/noticeboards/`. the rebuild scope is determined by which finding kinds were emitted this chapter; minimum: deferred-notability, high-stakes, pending-changes, broken-wikilink.
10. **structure-note narrative pass.** if the chapter materially reshapes how a cluster hangs together, update the relevant structure note's `## How the cluster is held together` section and `## Cross-cluster bridges` section. structure notes are where cross-cluster narrative lives; if no existing structure note covers the new material and the cluster has crossed the size threshold, the structure-note coverage finding raised in step 2 will drive its creation in a follow-up run.
11. **update the process trace.** mark the chapter row `complete`. list entries created and updated. note any open findings the chapter produced. record per-chapter counts (entries created, entries merged, units folded, units staged pending, structure notes touched, high-stakes claims processed, pending proposals raised) directly in the tracker row — the tracker is the per-source activity record; vault-wide activity is queryable from `run-*` entries on demand.
12. **clean `temp/`** including `_staging-index.md`. pending files have already been migrated in phase 3. merge-blocked files remain until repaired (a follow-up run, not this closeout).
13. **emit `run-chapter-closeout-{source-slug}-{N}`** with reads, writes, findings raised, and policy/lens versions per the run schema (§25.3). this run entry, together with git history, is the canonical record of what the chapter did; no separate hand-authored log is maintained.

#### 17.6.2 phase 4 output

- `wiki/entries/` reflecting all chapter writes that passed review.
- updated source entry, indexes, and noticeboards.
- updated structure notes for any cluster the chapter materially reshaped.
- a clean `temp/`.
- the chapter row marked `complete`.
- new open findings tracked in the relevant noticeboards.

### 17.7 source completion

after every chapter has gone through phase 4:

1. **walk surviving pending-notability units** in `raw/{source-slug}/pending/`. any not promoted by source completion are retired per §8.3.3.
2. **walk surviving high-stakes findings.** if primary-literature evidence has arrived during ingestion, close the findings; otherwise they remain open as ingestion priorities for the next source.
3. **promote cross-chapter observations.** review the process trace's running notes; for any observation that warrants its own entry, draft and stage as a normal phase-2 unit (in a one-shot mini-chapter for closeout).
4. **review the source entry** end-to-end. summary, key ideas, connections, lead all reflect the full work. update `quality` to a finer grade if applicable.
5. **final structure-note pass.** for every domain the source covered, examine its load-bearing structure notes; regenerate leads where appropriate.
6. **lint full pass on all touched pages.**
7. **mark the process trace `complete`.** the source's `status` flips from `in-progress` to `complete`.
8. **emit `run-source-complete-{source-slug}`**.

---

## 18. reingestion

### 18.1 trigger

reingestion is triggered when:

- a chapter previously marked `complete` is requested for reingestion (e.g., "redo chapter 3").
- a major change in lenses or policies invalidates earlier classification (rare; usually targeted reclassification, not full reingestion).
- the source has been updated (a new edition arrives) — though typically this is treated as a new source with `supersedes` relations.

### 18.2 procedure

1. confirm from the process trace that the chapter was `complete`.
2. mark the chapter row `in-progress`. add `Reingesting chapter {N} — {date}` to the running notes.
3. run phases 1–3 fresh. temp starts empty; staging is **blind** (no reading of existing wiki entries).
4. phase 3 merge proceeds with this rule: **the existing wiki entry is treated as the richer side** in the merge — it has accumulated connections from later chapters. the reingested version is a depth upgrade on prose, not a replacement on connections. append-only sections (especially `## Connections` and the structure-note `## Load-bearing entries` list) are preserved in full.
5. phase 4 closeout proceeds normally, but the chapter's `chapters_completed` count in the process trace does not increment; the row's `Notes` cell gains `(reingested)`.

### 18.3 the depth-upgrade merge rule

in §19, the merge rules name "full prose consolidation" and "append-only" sections. in reingestion, "full prose consolidation" tilts toward the reingested version (the editor's fresh blind read), while "append-only" sections remain protected.

### 18.4 reingestion of a single sub-section vs. full chapter

partial reingestion (a single sub-section) is permitted when only one sub-section's content has materially changed (e.g., the source's e-book updated one section). procedure: phase 1 setup is full-chapter, but phase 2 only re-runs the named sub-section; phase 3 merges only files staged in phase 2; phase 4 closeout proceeds normally.

---

## 19. merge rules — full catalog

### 19.1 the frontmatter merge — mechanical, applies to all kinds

| field                                                                             | rule on merge                                                                                                         |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `id`                                                                              | keep original; must match filename. mismatch is `finding-id-filename-mismatch-{slug}` blocking.                       |
| `title`                                                                           | keep original unless explicitly re-canonicalized in temp; recanonicalization requires a discussion.                   |
| `category`                                                                        | must agree. mismatch → halt, emit `finding-merge-classification-mismatch-{slug}`.                                     |
| `classified_by`                                                                   | must agree. mismatch → halt, emit `finding-merge-classified-by-mismatch-{slug}`.                                      |
| `produced_by`                                                                     | must agree. mismatch → halt.                                                                                          |
| `domains`                                                                         | union, deduplicated.                                                                                                  |
| `tags`                                                                            | union, deduplicated.                                                                                                  |
| `sources`                                                                         | union, deduplicated.                                                                                                  |
| `aliases`                                                                         | union, deduplicated.                                                                                                  |
| `created`                                                                         | keep original.                                                                                                        |
| `updated`                                                                         | today's date.                                                                                                         |
| `confidence`                                                                      | most conservative: `contested` > `low` > `medium` > `high`.                                                           |
| `status`                                                                          | most advanced: `complete` > `stub` > `draft`.                                                                         |
| `notability_status`                                                               | most permissive: `passes` > `borderline` > `fails`.                                                                   |
| `edit_hardness`                                                                   | strictest: `locked` > `restricted` > `extended-confirmed` > `confirmed` > `open`. never lower.                        |
| `high_stakes_class`                                                               | must agree. mismatch → halt, emit `finding-merge-high-stakes-mismatch-{slug}`.                                        |
| `quality`                                                                         | strictest: `featured` > `a` > `b` > `c` > `start` > `stub`.                                                           |
| category-specific lists (e.g., `illustrates`, `applies`, `connects`, `organizes`) | union, deduplicated.                                                                                                  |
| `evidence_grade` (claim, relation)                                                | strongest of the two; if they disagree by more than one grade, set `confidence: contested` and keep the higher grade. |
| `evidence_pointers` (claim, relation)                                             | union, deduplicated.                                                                                                  |
| `lens_priority`                                                                   | keep original; changes only via discussion.                                                                           |

### 19.2 concept merge

**body merge rule: full prose consolidation.**

procedure:

1. read the existing entry's body and the temp body.
2. produce a consolidated body by synthesizing both.
3. preserve the most precise wording from each side. when phrasing conflicts, prefer the version with better source attribution.
4. `## Connections`, `## Illustrations`, `## Sources`, `## Mentioned in` sections are **append-only**: deduplicate but never delete entries that exist on either side.
5. the lead section is rewritten if either side's lead is materially different from a faithful summary of the consolidated body.

### 19.3 insight merge

**body merge rule: full prose consolidation, same as concept.** insights are typically harder to consolidate because they assert relationships; verify the relationship is preserved across both sources.

### 19.4 entity merge

**body merge rule: structured merge.** sections like `## Background`, `## Key contributions`, `## Influences` are append-only at the bullet level. prose paragraphs are consolidated. union the category-specific fields (`entity_kind` must agree).

### 19.5 application merge

**body merge rule: structured merge.** the `## Steps` section is the load-bearing one; if both sides have a steps list and they differ, the canonical version is the one in the existing entry, with new steps inserted from the temp side at the locations the temp version implies. if the steps fundamentally disagree on order, halt and emit `finding-application-steps-conflict-{slug}`.

### 19.6 process merge

**body merge rule: structured merge with stage-list union.** the `stages` frontmatter is unioned but order-preserving: existing stages keep their position; new stages from temp are inserted at the position the temp version implies. order conflict → halt and emit `finding-process-stages-conflict-{slug}`.

### 19.7 structure-note merge

**body merge rule: organizing prose consolidated; load-bearing-entries and subregion annotations append-only.**

procedure:

1. consolidate the `## How the cluster is held together` section by synthesizing both sides.
2. the `## Load-bearing entries` section is append-only at the bullet level. deduplicate by slug; if both sides have an annotation for the same slug, prefer the temp side's annotation (fresher) but keep both as `existing annotation: …` and `revised annotation: …` until a discussion ratifies.
3. `## Subregions or themes` sections: each subregion's bullet list is append-only; subregion prose is consolidated.
4. `## Open questions in this cluster` is append-only.
5. `## Cross-cluster bridges` is append-only.

### 19.8 illustration merge

**body merge rule: replace.** the temp version is a fresher, unanchored retelling. it replaces the existing body. the `illustrates` frontmatter is union; `chapter`, `pages`, `source` fields take temp values if present.

rationale: an illustration is a story retold from a single source; the second telling is usually a refinement, not an addition. earlier connections drawn from the illustration are preserved in inbound wikilinks (which the merge does not modify).

### 19.9 source merge

**body merge rule: structured append.**

- `## Lead` — replace if the new lead more accurately captures the now-fuller summary.
- `## Summary` — append a paragraph or rewrite the summary to incorporate new chapters.
- `## Key ideas` — append.
- `## Notable claims` — append.
- `## Connections` — append.
- `## Sources` — the source itself; do not append (would create circularity).

### 19.10 claim merge

**body merge rule: structured.**

- `claim_text` — must agree. mismatch → halt, emit `finding-claim-text-mismatch-{slug}`.
- `evidence_pointers` — union. if pointers from different sources support the same claim, claim's `evidence_grade` may upgrade per §19.1.
- `asserts_about` — union.
- `verifiable` — must agree.

### 19.11 relation merge

**body merge rule: structured.**

- `predicate`, `from`, `to` — must agree. mismatch → halt.
- `evidence_pointers` — union.
- `evidence_grade` — strongest of the two unless they disagree by more than one grade, in which case `confidence: contested`.

### 19.12 question merge

**body merge rule: structured append.**

- `asks_about` — union.
- `priority` — strictest: `high` > `medium` > `low`. raises only.
- `closes_when` — keep original unless temp explicitly refines it; refinement notes both versions until a discussion ratifies.
- body — append (the question gains new framings).

### 19.13 lens merge

**body merge rule: full prose consolidation; criteria append-only.**

- `lens_question`, `lens_priority`, `lens_covers_category`, `lens_kind` — must agree. mismatch → halt; lens edits go through quorum, not ordinary merge.
- `## Criteria` section is append-only at the bullet level.
- `## Worked examples` is append-only.
- `lens_version` increments.

### 19.14 policy / guideline / essay merge

**body merge rule: full prose consolidation. promotion is not a merge.**

merge rules apply only to ordinary edits at a tier. tier transitions (`essay → guideline`, `guideline → policy`, demotion, retirement) follow the promotion-path mechanics in §13.4 and produce `run-promotion-*` rather than `run-merge-*`.

### 19.15 disambiguation merge

**body merge rule: append-only on variants list and on the body's `## Variants` section.** new variants merge in; existing variants remain. annotations are append-only at the bullet level (variant-distinguisher prose may be refined; refinement keeps both versions until discussion ratifies).

### 19.16 domain merge

domain entries change rarely. ordinary edits use full prose consolidation on body sections; subscribed-agents list, load-bearing-structure-notes list, canonical-questions list are append-only. `contentious` flag toggle is not an ordinary merge — it requires meta-rule quorum (§9.4) and produces `run-domain-contentious-toggle-{slug}`.

### 19.17 agent merge

agent manifest mutations follow `lifecycle-agent-mutate` (§16.3.2). ordinary merges may not occur on agent entries; lint `agent-direct-merge` blocks any merge run that targets an `agent-*` entry without going through the lifecycle protocol.

### 19.18 run, finding, discussion, notification, pending merge

these kinds are immutable once written. attempted merges produce `finding-immutable-merge-{slug}` blocking. updates to status (e.g., closing a finding, advancing a discussion to `closed-resolved`) are recorded as new entries linked to the original, not as merges.

---

## 20. lint workflow

### 20.1 when lint runs

- **on every write** — every `run-*` that writes an entry triggers a focused lint pass on that entry and on entries it references.
- **on every closeout** — phase 4 includes a chapter-scope lint pass.
- **scheduled** — a daily full pass over `wiki/entries/`.
- **on demand** — a human or agent can request a targeted lint over a slug, a domain, or the full vault.

### 20.2 lint rule catalog

each rule has a name, scope, severity, and a finding-kind. severity is `advisory` (does not block writes; produces a finding for review) or `blocking` (prevents the write or merge until resolved).

| rule name                            | scope                                 | severity                                           | finding kind                                          |
| ------------------------------------ | ------------------------------------- | -------------------------------------------------- | ----------------------------------------------------- |
| `slug-uniqueness`                    | full vault                            | blocking                                           | `finding-slug-collision-{slug}`                       |
| `id-filename-mismatch`               | per entry                             | blocking                                           | `finding-id-filename-mismatch-{slug}`                 |
| `unknown-category`                   | per entry                             | blocking                                           | `finding-unknown-category-{slug}`                     |
| `classification-consistency`         | per content entry                     | blocking                                           | `finding-classification-consistency-{slug}`           |
| `infrastructure-without-produced-by` | per infra entry                       | blocking                                           | `finding-infrastructure-without-produced-by-{slug}`   |
| `infrastructure-classified-by-lens`  | per infra entry                       | blocking                                           | `finding-infrastructure-classified-by-lens-{slug}`    |
| `lens-self-classification`           | per lens entry                        | blocking                                           | `finding-lens-self-classification-{slug}`             |
| `unknown-domain`                     | per entry                             | blocking                                           | `finding-unknown-domain-{slug}`                       |
| `entry-without-domain`               | per entry                             | blocking                                           | `finding-entry-without-domain-{slug}`                 |
| `tag-shadowing-domain`               | per entry                             | advisory                                           | `finding-tag-shadowing-domain-{slug}`                 |
| `source-frontmatter-mismatch`        | per entry                             | advisory                                           | `finding-source-frontmatter-mismatch-{slug}`          |
| `missing-required-list`              | per entry                             | blocking                                           | `finding-missing-required-list-{slug}-{field}`        |
| `category-fields-presence`           | per entry                             | blocking                                           | `finding-category-fields-presence-{slug}`             |
| `reserved-prefix-misuse`             | per entry                             | blocking                                           | `finding-reserved-prefix-misuse-{slug}`               |
| `lead-missing`                       | per entry                             | advisory or blocking (see §20.3)                   | `finding-lead-missing-{slug}`                         |
| `lead-too-long`                      | per entry                             | advisory                                           | `finding-lead-too-long-{slug}`                        |
| `low-link-density`                   | per content entry                     | advisory                                           | `finding-low-link-density-{slug}`                     |
| `structure-note-low-link-density`    | per structure note                    | blocking                                           | `finding-structure-note-low-link-density-{slug}`      |
| `broken-wikilink`                    | per entry                             | blocking                                           | `finding-broken-wikilink-{slug}-{target}`             |
| `relation-not-formalized`            | per entry                             | advisory                                           | `finding-relation-not-formalized-{slug}`              |
| `orphan-entry`                       | full vault                            | advisory                                           | `finding-orphan-entry-{slug}`                         |
| `main-index-coverage`                | full vault                            | advisory                                           | `finding-main-index-coverage-{slug}`                  |
| `domain-index-coverage`              | full vault                            | advisory                                           | `finding-domain-index-coverage-{slug}`                |
| `lens-version-drift`                 | full vault                            | advisory                                           | `finding-classification-drift-{slug}`                 |
| `unanswered-old-question`            | per question                          | advisory                                           | `finding-unanswered-old-question-{slug}`              |
| `evidence-below-floor`               | per claim                             | blocking in contentious domain; advisory otherwise | `finding-evidence-below-floor-{slug}`                 |
| `source-missing-contentious`         | per claim in contentious domain       | blocking                                           | `finding-source-missing-{slug}`                       |
| `high-stakes-floor-violation`        | per claim with non-`none` class       | blocking                                           | `finding-high-stakes-removal-{slug}`                  |
| `structure-note-coverage`            | full vault                            | advisory                                           | `finding-cluster-without-structure-note-{cluster-id}` |
| `stale-pending`                      | per pending proposal                  | advisory                                           | `finding-stale-pending-{run-id}`                      |
| `stale-discussion`                   | per discussion                        | advisory                                           | `finding-stale-discussion-{slug}`                     |
| `stale-finding`                      | per finding open >90 days             | advisory                                           | `finding-stale-finding-{slug}`                        |
| `domain-non-subscriber-edit`         | per write to domain by non-subscriber | advisory                                           | `finding-domain-non-subscriber-edit-{slug}`           |
| `agent-direct-merge`                 | per merge run on agent entry          | blocking                                           | `finding-agent-direct-merge-{slug}`                   |
| `immutable-merge`                    | per merge run on immutable entry      | blocking                                           | `finding-immutable-merge-{slug}`                      |
| `disambiguation-orphan`              | per disambiguation entry              | advisory                                           | `finding-disambiguation-orphan-{slug}`                |
| `disambiguation-no-hatnote`          | per variant of a disambiguation       | advisory                                           | `finding-disambiguation-no-hatnote-{slug}`            |
| `notability-stamp-missing`           | per content entry                     | blocking                                           | `finding-notability-stamp-missing-{slug}`             |
| `edit-hardness-consistency`          | per entry                             | blocking                                           | `finding-edit-hardness-consistency-{slug}`            |
| `frontmatter-yaml-invalid`           | per entry                             | blocking                                           | `finding-frontmatter-yaml-invalid-{slug}`             |
| `body-section-order`                 | per entry with explicit lead          | advisory                                           | `finding-body-section-order-{slug}`                   |
| `wontfix-without-justification`      | per finding                           | blocking                                           | `finding-wontfix-without-justification-{slug}`        |
| `discussion-round-bound-exceeded`    | per discussion                        | blocking                                           | `finding-discussion-round-exceeded-{slug}`            |
| `low-quality-lead`                   | per entry with explicit lead          | advisory                                           | `finding-low-quality-lead-{slug}`                     |
| `seed-test-fail`                     | per persona agent                     | advisory or blocking depending on test authority   | `finding-persona-test-fail-{persona}-{test}`          |

### 20.3 the `lead-missing` rule — severity rules

- if the entry's body exceeds the threshold and lacks a `## Lead`, the rule fires.
- in a non-contentious domain, the finding is `advisory`.
- in a contentious domain, the finding is `blocking` (the lead is required regardless of size in contentious domains, per §15.2).
- structure notes and source entries always require a lead; missing lead is `blocking` regardless of domain.

### 20.4 lint findings vs. other findings

every lint output is a `finding-*` entry per §21. the `fired_by` field always points at a `lint-*` rule entry (or a `policy-*` for blocking findings tied to a policy). lint runs that produce no findings still emit a `run-lint-{scope}-{date}` recording the empty result.

### 20.5 the `severity: advisory` vs. `blocking` distinction

- **advisory** — finding is recorded; no write is blocked. resolution is review-and-fix at the editor's pace.
- **blocking** — the offending write or merge cannot complete until resolved or `wontfix`-ed.

a write that produces a blocking finding fails atomically: nothing is written. the agent receives the finding, may revise and resubmit, or open a discussion if the rule itself is contested.

### 20.6 lint agent population

at seed, lint is enacted by a small set of named lint agents (§29.6), each with `policy_targets` listing the rules it enforces. lint agents may be added, mutated, or retired through the standard lifecycle. as the population grows, lint coverage is composed by combining agents' targets.

---

## 21. findings

### 21.1 finding entry schema

every finding is an entry under `wiki/entries/finding-*.md`. its frontmatter is per §4.3.17. its body:

```markdown
# {Finding Title}

## Lead

{1-2 sentences naming the issue, the entry it touches, and the rule that fired.}

## What the rule says

{Excerpt or summary of the rule that fired.}

## What the entry has

{The state of the entry that triggered the finding.}

## Resolution path

{How the finding can be resolved. May be empty until a resolution is proposed.}

## Resolution

{Filled when status flips to `resolved`.}

## Wontfix justification

{Filled when status flips to `wontfix`. Required for blocking findings.}
```

### 21.2 finding lifecycle

```
open → resolved
     ↘ wontfix
```

#### 21.2.1 from `open` to `resolved`

an editor (or lint) writes a fix that removes the cause of the finding. the next lint pass on the affected entry no longer fires the rule. the finding's `status` flips to `resolved`; `resolved` date and `resolution_run` are populated.

#### 21.2.2 from `open` to `wontfix`

an editor (or a discussion) determines that the finding cannot be resolved without violating another rule, or that the finding is a false positive, or that the rule itself is overzealous. the editor populates `wontfix_justification` with prose explaining the decision. for blocking findings, `wontfix` requires meta-rule quorum (§9.4); for advisory findings, `wontfix` requires confirmed-tier reputation.

#### 21.2.3 reopening

a `resolved` or `wontfix` finding may be reopened if:

- the entry that resolved it is reverted.
- a later edit re-introduces the issue.
- a new sub-source contradicts the wontfix justification.

reopening creates a new `run-finding-reopen-{slug}` entry; the finding's `status` returns to `open`; the prior resolution becomes prior history.

### 21.3 findings as first-class persistent objects

findings are not log lines. every finding the vault notices is an entry. the open list of things wrong with the vault is therefore visible at any time as the union of `wiki/entries/finding-*.md` with `status: open`. this is the substrate for the noticeboards (§23) and for the assessment layer (§28).

### 21.4 finding-kind taxonomy (selected)

while the lint catalog (§20.2) names every lint rule and its corresponding finding-kind, findings also arise from other origins:

- ingestion contradictions: `finding-contradiction-{claim-a}-{claim-b}`.
- pipeline failures: `finding-pipeline-failure-{phase}-{date}`.
- agent-test failures: `finding-persona-test-fail-{persona}-{test}`.
- assessment regressions: `finding-coverage-regression-{domain}-{date}`.
- write conflicts: `finding-write-conflict-{slug}-{run-id}`.
- discussion bound exceeded: `finding-discussion-round-exceeded-{slug}`.

each finding-kind has a corresponding noticeboard projection (§23.2).

---

## 22. discussions

### 22.1 when a discussion opens

- two agents disagree on the content of an entry (e.g., one writes that X is `true`, another wants to change to `contested`).
- a contradiction is raised between two claims and both authors disagree on resolution.
- a classification is contested.
- a promotion (essay → guideline → policy) is proposed.
- a wontfix justification is challenged.
- an agent retirement is proposed.

a discussion is opened by writing a `discussion-{slug}.md` entry. the slug is `discussion-{disputed-object-slug}-{short-disambiguator}`.

### 22.2 discussion entry body

```markdown
# {Title}

## Lead

{1-2 sentences: what is disputed, who participates, what termination protocol applies.}

## Disputed object

[[{slug}]] — {one-line context}

## Round 1

### {Agent slug}

{Argument, with citations.}

### {Agent slug}

{Counter-argument.}

## Round 2

...

## Termination

{Filled at close. Names the protocol applied (content-quorum, meta-rule-quorum, human-escalation), the outcome, and the resulting vault operation.}
```

### 22.3 round bound

a discussion holds at most **5 rounds** of exchange. each round is one statement per participant. after 5 rounds, the discussion **must** terminate; lint `discussion-round-bound-exceeded` fires blocking if the discussion crosses round 5 without a termination.

in contentious domains, the bound is **3 rounds** (§15.2).

### 22.4 termination protocols

per the disputed object's kind:

| disputed object                                                                                         | termination protocol                                                                                     |
| ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| content (concept, claim, relation, illustration, application, insight, process, entity, structure-note) | `content-quorum`: a quorum of in-domain agents at reputation ≥ 60 votes; outcome ratifies or rejects.    |
| lens, policy, runtime, this specification                                                               | `meta-rule-quorum`: 3 agents at reputation ≥ 80, or 1 human reviewer.                                    |
| anything that splits along human/agent lines                                                            | `human-escalation`: a human reviewer makes the call.                                                     |
| guideline, essay                                                                                        | `confirmed-vote`: a single confirmed agent (reputation ≥ 30) closes; appeal escalates to content-quorum. |

termination produces:

- a new version of the disputed entry, **or**
- a new relation entry (e.g., `relation-{a}-supersedes-{b}`), **or**
- a `wontfix` finding linking to the discussion as rationale.

### 22.5 stale discussions

a discussion inactive past 4 weeks (no new round, no termination) becomes `finding-stale-discussion-{slug}`. resolution: someone in the participant set advances a round or terminates. failing that, the meta-rule quorum may close the discussion administratively, with the disputed object reverting to its pre-discussion state.

### 22.6 discussions are bounded but auditable

every discussion ends within bound or becomes a finding. nothing dangles in chat state. every round is preserved in the discussion entry; termination records the outcome and the protocol. an outsider can always reconstruct why the disputed object now has the form it does.

---

## 23. noticeboards

### 23.1 noticeboards are projections

a noticeboard is **not** an entry. it is a generated file under `wiki/_meta/noticeboards/{kind}.md` that lists open findings of a particular kind. it rebuilds:

- on every closeout that produces a finding of the relevant kind.
- on the daily scheduled lint pass.
- on demand.

each noticeboard records its last-rebuild timestamp at the top.

### 23.2 the seed noticeboard set

| file                             | lists                                                                                  |
| -------------------------------- | -------------------------------------------------------------------------------------- |
| `slug-uniqueness.md`             | `finding-slug-collision-*`                                                             |
| `broken-wikilink.md`             | `finding-broken-wikilink-*`                                                            |
| `contradictions.md`              | open relation entries with predicate `contradicts` whose dispute is unresolved         |
| `high-stakes.md`                 | `finding-high-stakes-removal-*`                                                        |
| `evidence-below-floor.md`        | `finding-evidence-below-floor-*`                                                       |
| `pending-changes.md`             | open `pending-*` entries awaiting review                                               |
| `notability-deferrals.md`        | `finding-deferred-*`                                                                   |
| `cluster-coverage.md`            | `finding-cluster-without-structure-note-*`                                             |
| `stale-discussions.md`           | `finding-stale-discussion-*` and discussions inactive >2 weeks                         |
| `stale-findings.md`              | `finding-stale-finding-*` and findings open >60 days                                   |
| `agent-test-failures.md`         | `finding-persona-test-fail-*`                                                          |
| `domain-non-subscriber-edits.md` | `finding-domain-non-subscriber-edit-*`                                                 |
| `frontmatter-violations.md`      | every finding tied to a frontmatter rule                                               |
| `lifecycle-issues.md`            | `finding-agent-direct-merge-*`, `finding-immutable-merge-*`, agent retirement findings |
| `coverage-regressions.md`        | `finding-coverage-regression-*`                                                        |

new noticeboard files may be added when a finding kind needs its own visible board. removal: empty the file's source query and let the rebuild produce an empty board; or delete the file (which forces a full rebuild on next pass).

### 23.3 subscribe semantics for review agents

agents subscribe to noticeboards via their manifest (or via a dedicated `agent-test`-like construct). a review agent that processes contradictions reads `wiki/_meta/noticeboards/contradictions.md` rather than scanning all findings. this keeps the agent's working set bounded.

### 23.4 noticeboards as the operational dashboard

at any moment, the union of all noticeboards is the open list of things wrong with the vault. this is the operational dashboard. assessment (§28) and operations (§26) both rely on it.

---

## 24. agent tests

### 24.1 the schema

per §4.3.18. each agent-test entry attaches to one agent, names a question, and declares the expected answer shape. tests run as regressions whenever the vault changes materially.

### 24.2 test authorship rules

#### 24.2.1 seed tests

at agent creation, **seed tests are human-authored**. they define what "adequate for purpose" means for the agent's slice. their `authoritative: true` field marks them as the canonical regression set.

#### 24.2.2 proposed tests

other agents may propose tests for an existing persona or lint agent. proposed tests are accepted only after:

1. they pass against the agent's current state in a baseline run.
2. they are reviewed by a confirmed agent (or human reviewer) with the same edit-hardness rules as a lens (`extended-confirmed`).
3. they are added to the agent's `seed_tests` list.

a proposed test that an agent fails on first run is **not** accepted; failure indicates either the test is wrong or the agent has a real gap. the gap path is to first fix the gap, then re-propose.

### 24.3 run cadence

- on every closeout, the agent-tests of personas whose slice overlaps the touched entries run.
- daily, every persona's full agent-test set runs.
- on demand.

### 24.4 failure handling

a failing agent-test produces `finding-persona-test-fail-{persona}-{test}`. the finding's `severity` is:

- `blocking` if the test is `authoritative: true` (a seed test failed).
- `advisory` otherwise.

resolution: typically requires either repairing the persona's slice (an entry the persona depends on is missing or wrong), or the persona's prompt strategy needs revision (a `lifecycle-agent-mutate` per §16.3.2).

### 24.5 test versioning

agent tests have `created` and `updated` fields. a test edit increments an implicit version; the test's `last_run` and `last_result` are reset to `stale` until the next run. a stale test is included in the daily run by default but excluded from on-write triggers until it has a fresh result.

---

## 25. runs and versioning

### 25.1 a run is a record of one execution

every agent execution that produces side effects (writes, findings, notifications) emits a `run-*` entry. runs are immutable.

### 25.2 run kinds (v0)

| run-kind             | what it records                                                             |
| -------------------- | --------------------------------------------------------------------------- |
| `edit`               | an editor agent wrote one or more entries                                   |
| `lint`               | a lint pass scanned a scope; lists findings raised and findings resolved    |
| `assess`             | an assessment pass computed signals                                         |
| `ingest`             | a phase 0/1/2/3/4 step from the ingestion pipeline                          |
| `review`             | a confirmed agent reviewed pending proposals                                |
| `merge`              | a merge run combined a temp file with an existing entry                     |
| `promotion`          | a tier promotion (essay→guideline→policy, or pending→passes for notability) |
| `quorum`             | a quorum action (lens edit, policy promotion, contentious flag toggle)      |
| `lifecycle`          | an agent lifecycle action (create, mutate, retire)                          |
| `rollback`           | a rollback to a prior version                                               |
| `notification-flush` | bulk processing of notifications                                            |
| `archival`           | a roll-up archive operation                                                 |

### 25.3 run frontmatter and body

per §4.3.16. body is templated:

```markdown
# run {kind} — {date} — {short summary}

## Lead

{1 sentence: what this run did, in active voice.}

## Reads

- [[slug]]
- ...

## Writes

- [[slug]] — {action: created | modified | merged}
- ...

## Findings raised

- [[finding-{slug}]]
- ...

## Findings resolved

- [[finding-{slug}]]
- ...

## Active versions

policy-ingestion: v3
lens-concept: v4
...

## Notes

{Anything not captured above.}
```

### 25.4 versioning

each entry's history is the ordered sequence of `run-*` entries that wrote it. this is implicit, not stored as a per-entry version field. to retrieve the history of an entry, query: every run whose `writes` includes the entry's slug, in chronological order.

### 25.5 rollback

rollback is implemented as a forward edit pointing at a prior version.

procedure:

1. identify the target version (a prior run that wrote the entry).
2. read the entry as it existed immediately after that run (reconstructable from the run's record of the write content).
3. write that body and frontmatter as the entry's current state.
4. emit `run-rollback-{slug}` recording: the prior run's slug, the rationale, the reverter agent.
5. lint runs against the rolled-back state.

rollback respects edit-hardness: rolling back a `restricted` entry requires meta-rule quorum.

### 25.6 querying activity over time

there is no hand-authored or rendered "vault log" file. the canonical record of vault activity at the agent-action level is the set of `run-*` entries; at the file level, it is git history. both are queryable on demand:

- "what did agent X do this week?" — `run-*` entries whose `agent` field matches and whose `started` date falls in the window.
- "what changed in entry Y?" — `run-*` entries whose `writes` list includes the slug, ordered chronologically; or `git log` on the file.
- "what happened across the vault today?" — `run-*` entries with today's `started` date.

if a recent-changes-style operational view ever proves load-bearing for a review or patrol agent, build it as a noticeboard (§23) — a cached projection over runs by date, computed on the same rebuild schedule as the other noticeboards. the design principle is that `_meta/` files are computed from entries, never the source of truth and never hand-authored; runs and git already carry the activity record, so a separate log artifact would be a third copy of the same information with no canonical authority.

### 25.7 run rollups

old `run-*` entries are aggressively archived. per `policy-archival`:

- runs older than 30 days are eligible for rollup.
- a rollup combines all runs of a given agent over a period (week, month) into a single `run-rollup-{agent}-{period}` entry summarizing the activity.
- the original `run-*` entries are retained but moved to `wiki/_meta/archive/` (outside the indexed entry pile, but reachable for forensics).

---

## 26. operations

### 26.1 concurrency

#### 26.1.1 file-level optimistic locking

writes are file-level. an agent prepares a write, the runtime acquires a per-entry advisory lock, the write applies, the lock releases. the lock is not pre-acquired during long thinking; it is taken at submission.

#### 26.1.2 simultaneous-write conflicts

if two agents submit writes to the same entry within the lock window:

1. the runtime accepts the first; the second receives a write-conflict signal.
2. the second's run records `finding-write-conflict-{slug}-{run-id-2}` linking both runs.
3. the higher-reputation agent's write wins by default.
4. on tie, a human reviewer or meta-rule quorum resolves.

write conflicts are findings, not silent overwrites.

#### 26.1.3 read consistency

reads are eventually consistent. a reader may see an entry in a state that has just been overwritten; the next read after the lock release sees the new state. retrieval (§27) does not pin a snapshot — it reads from the current state of `wiki/entries/`.

### 26.2 compute budget

every agent run carries a token budget in its prompt. lint and assessment passes share a daily budget the runtime tracks. over-budget runs queue rather than drop. queue depth becomes an assessment signal — sustained queue depth implies the budget is too low or the work too dense.

`policy-compute-budget` declares:

- per-agent default token budget per run.
- per-policy daily budget (e.g., daily lint full pass: N tokens).
- queue-depth thresholds that trigger findings.
- escalation: when queue depth exceeds threshold, a `finding-compute-budget-saturated` is emitted; resolution may be raising the budget or reducing the work.

### 26.3 archival

#### 26.3.1 hot-cold split

infrastructure entries — runs, findings (resolved), notifications, discussions (closed) — would dominate file count without archival. per `policy-archival`:

- **hot window**: 30 days. entries less than 30 days old remain in `wiki/entries/`.
- **cold archive**: entries older than 30 days are moved to `wiki/_meta/archive/` per their kind.
  - `archive/runs/{year}/{month}/{slug}.md`
  - `archive/findings/{year}/{month}/{slug}.md`
  - etc.
- **rollups**: per §25.7, runs older than 30 days are also summarized into rollups in `wiki/_meta/archive/rollups/`.

content entries are **never** archived this way. content persists.

#### 26.3.2 retrieval over archives

`wiki/_meta/archive/` is reachable but not indexed for retrieval. searches default to the live `wiki/entries/` directory. archive forensics use a separate explicit query.

### 26.4 indexes

#### 26.4.1 cached projections

`wiki/_meta/index.md` and the per-domain index files under `wiki/_meta/indexes/` are cached projections. they rebuild:

- on every closeout that touches their scope.
- on a daily schedule.
- on demand.

each index records its last-rebuild timestamp. consumers may read an index's timestamp to decide whether to trust it.

#### 26.4.2 the rebuild script

`pnpm build:vault-indexes` walks `wiki/entries/`, reads each frontmatter, and emits the catalog files. it is deterministic given the same vault state.

#### 26.4.3 main index format

```markdown
# main index

last rebuild: {YYYY-MM-DD HH:MM}

## by category

### concept (N entries)

- [[slug]] — title — domains: ...
- ...

### source (N entries)

- ...

(every category, with entry counts)
```

#### 26.4.4 per-domain index format

```markdown
# domain: {Domain Title}

last rebuild: {YYYY-MM-DD HH:MM}

## load-bearing structure notes

- [[structure-{slug}]] — frame: ...

## by category

### concept (N entries in this domain)

- [[slug]] — title
- ...

(per category in this domain)

## open questions

- [[question-{slug}]]
- ...
```

### 26.5 noticeboards (cached projections, like indexes)

§23. rebuild on closeout, daily, on demand. record last-rebuild timestamp.

### 26.6 runtime

`runner/` is the only enforcer of write-scope, reputation gates, edit-hardness, and pending-changes routing. it lives outside `wiki/`. it is small and versioned. it is described in `policy-runtime` once that policy lands.

`runner/`'s responsibilities:

1. read agent manifests and execute agents per their prompt strategy.
2. intercept writes; apply edit-hardness and reputation gates; route to direct write or pending proposal.
3. emit `run-*` entries for every execution.
4. maintain advisory file-level locks.
5. report queue depth, token usage, and run statistics for assessment.

`runner/` does **not**:

- decide content (that is the agent's job).
- enforce lens criteria (lint agents do that).
- decide promotion outcomes (discussions and quorum do that).

### 26.7 backup, audit, and provenance

every entry is a markdown file under version control (git). git history is the canonical record of every change at the file level. `run-*` entries are the canonical record of every change at the agent-action level. the two layers are redundant — git can answer "what changed when in this file"; runs can answer "which agent changed this file and why." together, they support full auditability.

### 26.8 failure modes and recovery

| failure                                  | response                                                                                                                                                                                                                                              |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| an entry's frontmatter becomes malformed | lint `frontmatter-yaml-invalid` blocking; the offending write is rejected.                                                                                                                                                                            |
| `temp/` is not cleared between chapters  | phase 1 detects and blocks; the editor is notified to clean before retry.                                                                                                                                                                             |
| an agent's runtime crashes mid-run       | the partial run is recorded as `run-{kind}-{slug}` with `status: aborted` (an additional run field; see §35.5). subsequent retry produces a new run entry. partial writes that landed are linted as if they were complete; broken state is a finding. |
| `runner/` is misconfigured               | the runtime fails closed: rejects writes until the misconfiguration is fixed.                                                                                                                                                                         |
| disk corruption                          | recovery from git history.                                                                                                                                                                                                                            |

---

## 27. retrieval contract (v0)

### 27.1 the consumer interface

a consumer agent invokes retrieval with:

- a **task**: a natural-language query.
- a **slice**: a domain-slug list, a persona-agent slug, or both.
- a **budget**: a token budget for the returned context.
- optional: **filters** (evidence-grade floor, kind filter, recency).

### 27.2 the selection algorithm

```
input: task, slice, budget, filters
output: ordered list of fragments, total token cost ≤ budget
```

algorithm (v0):

1. **resolve the slice.** intersect declared domains; resolve persona's `read_domains` if a persona is given.
2. **pull the slice's load-bearing artifacts.**
   - the per-domain indexes for every domain in the slice.
   - the leads of every load-bearing structure note declared by those domains.
   - the leads of high-evidence-grade entries (grade ≥ B by default; tunable via filter) within the slice.
3. **traverse one hop** over `supports`, `contradicts`, `instance-of`, `supersedes`, `depends-on` relations from the entries pulled in step 2. add the leads of the destination entries.
4. **semantic-similarity fill.** with remaining budget, run semantic similarity over leads first, then over chunked entry bodies. add candidates in order of similarity, applying orthogonality maximization (§27.3) at each addition.
5. **expand to full body** for entries already in the candidate set, in order of relevance, until budget is exhausted.

#### 27.2.1 ordering invariant

within the budget, the consumer receives:

1. domain index headers (compact).
2. structure-note leads (cluster-level summaries).
3. high-grade entry leads (atom-level summaries).
4. relation traversal (typed-edge leads).
5. semantic similarity (leads first, bodies if budget allows).
6. full bodies of the most relevant entries.

### 27.3 orthogonality

orthogonality maximization rejects candidates whose information overlaps what is already in context. concretely: at each addition step, the candidate fragment is compared (semantically) to the existing fragment set; if the overlap exceeds a threshold (v0: 0.85 cosine similarity in fragment-embedding space), the candidate is dropped.

orthogonality is applied at lead-level first (cheap) and at body-level only for fragments that survived lead-level selection.

### 27.4 confidence and high-stakes filtering

retrieval respects confidence and high-stakes:

- `confidence: contested` entries are returned with an explicit marker (a prefix `[CONTESTED] `) so the consumer knows.
- entries with `high_stakes_class != none` and an open removal finding are returned as the placeholder string (per §14.3.1), not as the original claim.
- `status: draft` entries are excluded from default retrieval. an explicit filter `include_drafts: true` overrides.

### 27.5 retrieval output format

the consumer receives:

```
[Slice: {domain slugs and/or persona slug}]
[Budget: {tokens used} / {budget}]
[Fragment count: N]

## Domain index — {domain}
{headers}

## Structure note — [[structure-{slug}]] (lead)
{lead text}

## Entry — [[slug]] (lead, A-grade)
{lead text}

...

## Entry — [[slug]] (full body)
{full body}
```

### 27.6 retrieval quality measurement

retrieval is measured against the thesis-eval panel (§28.5). the consumer's task is graded; the variance reduction over an unaided baseline is the headline metric. retrieval quality is one of the levers; the others are vault state and the consumer's prompt.

---

## 28. assessment and the thesis-eval panel

### 28.1 the assessment pass

a periodic pass that computes signals about the vault's state. per `policy-assessment`, it runs:

- daily for fast signals (lint findings counts, pending queue depth).
- weekly for slower signals (coverage, source grounding, link density).
- on demand.

each pass produces a `run-assess-{date}` entry recording every signal computed. signals are stored as structured frontmatter in the run entry; a per-domain dashboard projection (§28.6) visualizes them over time.

### 28.2 coverage signals

per domain:

- `open_questions_count` — number of `question-*` entries with `status: open` and `domains` ∋ this domain.
- `open_questions_closed_this_period` — closed in the last week.
- `claims_with_evidence` — fraction of claim entries in this domain whose `evidence_grade` is set (always, in correct vaults) and `evidence_pointers` non-empty.
- `claims_above_floor` — fraction of claims at or above the domain's `evidence_grade_floor`.
- `relation_density` — average number of relation-\* entries per content entry in this domain.
- `domain_orphans` — entries in this domain with no inbound wikilinks.
- `structure_note_coverage` — fraction of clusters in this domain with at least one structure note.

a domain whose `open_questions_count` keeps rising without closures is a signal to direct ingestion attention.

### 28.3 internal-consistency signals

vault-wide:

- `open_contradictions` — count of `relation-*` entries with predicate `contradicts` whose dispute is open.
- `findings_open_count` — count of `finding-*` with `status: open`.
- `findings_stale_count` — findings open >60 days.
- `confidence_contested_count` — entries with `confidence: contested`.
- `orphan_count` — content entries with no inbound wikilinks.
- `pending_queue_depth` — count of `pending-*` entries awaiting review.

### 28.4 source grounding signals

vault-wide:

- `claims_cite_source` — fraction of claim entries whose `evidence_pointers` include a source entry.
- `insights_multi_source` — fraction of insight entries that reference at least 2 source entries.
- `concepts_multi_source` — fraction of concept entries that draw from more than one source entry.

a vault that learns from many sources but produces single-sourced entries is failing to do the synthesis work.

### 28.5 the thesis-eval panel

a fixed set of verifiable tasks. for each task:

- the **unaided baseline** is recorded once: a sufficiently capable model attempts the task with no vault context. variance over N runs is recorded.
- the **vault-augmented run** is recorded periodically: the same model attempts the same task with retrieved context from the current vault. variance over N runs is recorded.

the headline metric is **variance reduction**: `var(unaided) - var(vault-augmented)`. positive values indicate the vault is doing the thing it claims to do.

the panel itself is a `policy-thesis-eval` entry (and accompanying agent-tests). amendments to the panel require meta-rule quorum.

### 28.6 dashboards

`wiki/_meta/dashboard.md` (or per-domain `wiki/_meta/indexes/{domain}-dashboard.md`) is a projection over recent assessment runs. it shows:

- the latest values of every signal.
- trend over the last 4 weeks.
- thesis-eval panel results (unaided baseline, vault-augmented runs).

dashboards are not assessment; they are how assessment is read.

### 28.7 assessment criteria as policy

the criteria that define each signal — what counts as a closure, what threshold makes a domain "saturating," how variance is computed — live in `policy-assessment` and `policy-thesis-eval`. changing what "good coverage" means is a policy edit.

---

## 29. seed configuration

### 29.1 seed scope

the seed is the phase-1 starting state (§1.6.1). everything in this section is **human-authored**: agents do not write any structural entry, in any tier, during seed. once seed is complete, agents begin operating against the bootstrapped scaffold per §30.3.

at v0 startup, the vault must contain at minimum:

- a base policy set.
- a small seed of guidelines and essays.
- the lens set covering every kind in §3.
- one domain entry per active subject area.
- one editor agent per seed domain, manifest authored by hand, starting reputation = 5.0.
- one persona agent with human-authored seed tests.
- a `policy-phase` entry declaring the operative phase as `phase-1`.
- a thesis-eval panel with recorded unaided baseline.
- a small runtime under `runner/` capable of executing agents per the per-entry lock model.

### 29.2 seed policies (must exist before chapter 1 of the first source)

| slug                          | covers                                                                                 | tier   |
| ----------------------------- | -------------------------------------------------------------------------------------- | ------ |
| `policy-ingestion`            | the four-phase pipeline (§17)                                                          | policy |
| `policy-classification`       | the lens decision tree and protocol (§7)                                               | policy |
| `policy-merge`                | merge rules per kind (§19)                                                             | policy |
| `policy-lint`                 | the lint rule catalog (§20)                                                            | policy |
| `policy-assessment`           | assessment signals and cadence (§28)                                                   | policy |
| `policy-claim-segmentation`   | when to split a sentence into multiple claims (§10.1.1)                                | policy |
| `policy-agent-lifecycle`      | create / mutate / retire (§16.3)                                                       | policy |
| `policy-archival`             | hot-cold window, rollup rules (§26.3)                                                  | policy |
| `policy-reputation-weighting` | reputation events, weights, external anchor (§9.6)                                     | policy |
| `policy-runtime`              | runner responsibilities and boundaries (§26.6)                                         | policy |
| `policy-thesis-eval`          | the eval panel and variance-reduction metric (§28.5)                                   | policy |
| `policy-notability`           | the notability predicate, promotion, retirement (§8)                                   | policy |
| `policy-structure-notes`      | when a structure note is required, body conventions (§11)                              | policy |
| `policy-entry-layout`         | the lead convention, body section order (§5)                                           | policy |
| `policy-high-stakes`          | the class catalog, the asymmetric removal regime (§14)                                 | policy |
| `policy-contentious-domain`   | what gets elevated, by how much (§15)                                                  | policy |
| `policy-pending-changes`      | staging mechanics, review flow (§9.5)                                                  | policy |
| `policy-content-quality`      | npov-equivalent (§4.2 and §10), verifiability, no original research adapted for agents | policy |
| `policy-rule-promotion`       | essay→guideline→policy mechanics (§13.4)                                               | policy |
| `policy-edit-hardness`        | tier definitions, gating rules (§9)                                                    | policy |
| `policy-discussions`          | round bound, termination protocols (§22)                                               | policy |
| `policy-reingestion`          | reingestion procedure (§18)                                                            | policy |
| `policy-phase`                | operative phase (phase-1 / phase-2 / phase-3) and transition criteria (§1.6)           | policy |

### 29.3 seed guidelines and essays

a small seed of soft-tier rules so the soft tiers exist with content from start. examples:

| slug                                | tier      | covers                                                                                                                                                                    |
| ----------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `guideline-naming-slugs`            | guideline | preferred slug-naming patterns: noun-first, lowercase, no source-specific suffixes.                                                                                       |
| `guideline-prose-style`             | guideline | prose voice: clear, source-agnostic in concept entries; story-style in illustrations.                                                                                     |
| `guideline-cluster-organization`    | guideline | when a structure note adds value: clusters of >8 entries, or clusters bridging domains.                                                                                   |
| `essay-when-to-promote-borderline`  | essay     | observation: borderline-notability units that gain a single inbound link in a different chapter often promote successfully; one-link promotion is a defensible heuristic. |
| `essay-illustration-vs-application` | essay     | observation: the boundary is fuzzy; an "application" with a single concrete subject often reads as an illustration. proposes a rule of thumb.                             |
| `essay-cross-domain-bridges`        | essay     | observation: structure notes that span multiple domains tend to grow large; consider splitting by frame.                                                                  |

### 29.4 seed lens set

per §7.2 (decision-tree) and §7.3 (annotation). 14 decision-tree lenses and 6 annotation lenses at seed. each lens entry includes worked examples drawn from the existing vault entries.

### 29.5 seed domain set

| slug              | scope summary                                                                   |
| ----------------- | ------------------------------------------------------------------------------- |
| `learning-theory` | cognitive mechanisms of learning.                                               |
| `neuroscience`    | brain mechanisms underlying learning.                                           |
| `pedagogy`        | teaching practice and instructional design.                                     |
| `self-regulation` | metacognition, procrastination, habit, motivation.                              |
| `assessment`      | testing, feedback, calibration.                                                 |
| `meta`            | entries about the vault itself (lenses, indexes, policies, guidelines, essays). |

each domain entry is hand-authored at seed. `contentious: false` everywhere at seed. `evidence_grade_floor: D` everywhere at seed. one canonical question per domain at minimum.

### 29.6 seed agent set

| slug                            | kind    | scope                                                                                   | starting reputation |
| ------------------------------- | ------- | --------------------------------------------------------------------------------------- | ------------------- |
| `agent-editor-learning-theory`  | editor  | write_domains: [learning-theory, pedagogy]                                              | 5.0                 |
| `agent-editor-neuroscience`     | editor  | write_domains: [neuroscience]                                                           | 5.0                 |
| `agent-persona-learning-theory` | persona | read_domains: [learning-theory, pedagogy, self-regulation, assessment]                  | 5.0                 |
| `agent-lint-frontmatter`        | lint    | policy_targets: [policy-classification, policy-entry-layout, policy-lint]               | 10.0                |
| `agent-lint-links`              | lint    | policy_targets: [policy-classification, policy-lint]                                    | 10.0                |
| `agent-lint-evidence`           | lint    | policy_targets: [policy-content-quality, policy-high-stakes, policy-contentious-domain] | 10.0                |

lint agents start at 10.0 because their work is mechanical and a small reputation buffer prevents pending-routing of mechanically correct findings.

### 29.7 seed agent tests

at minimum, the persona agent has 8 human-authored seed tests:

1. "what is the difference between primary and secondary biological knowledge?" — expected: cite [[biologically-primary-and-secondary-knowledge]]; name the distinction; reference [[david-geary]].
2. "how does desirable difficulty improve long-term retention?" — expected: cite [[desirable-difficulty]]; describe the mechanism; reference at least one source entry.
3. "what is interleaving, and when is it preferred over blocked practice?" — expected: distinction described, preferred conditions named.
4. "what does the recall-strength model predict about spaced repetition?" — expected: reference the model entry, describe the relation.
5. "what's the difference between a goal and an intention in self-regulation literature?" — expected: distinction drawn, key sources cited.
6. "what is the role of working memory in pedagogy?" — expected: causal relationship described.
7. "name three distinct study strategies and their trade-offs." — expected: three concrete strategies, with trade-offs.
8. "is multi-tasking effective for learning?" — expected: clear no, with evidence.

these are author-authored; their `authoritative: true` flag marks them as canonical.

### 29.8 seed thesis-eval panel

a fixed set of verifiable tasks with recorded unaided baselines. example tasks (drawn from the existing wiki seed):

1. "describe the mechanism by which spaced repetition produces stronger long-term retention than massed practice." — verifiable: must name encoding-retrieval gap, cite primary sources.
2. "list three pedagogical implications of the primary/secondary biological knowledge distinction." — verifiable: each implication must be a defensible practice.
3. "what is the relationship between desirable difficulty and the testing effect?" — verifiable: cite both, name the connection.
4. "describe the role of the basal ganglia in skill acquisition." — verifiable: cite primary literature.
5. "explain why declarative learning and procedural learning have different forgetting curves." — verifiable: name both, name the distinction.

each task has 5 unaided runs with a baseline model recorded as the variance baseline. the panel and baselines live in `policy-thesis-eval` and accompanying agent-tests.

### 29.9 seed runtime

the runtime under `runner/` at seed is small enough to specify here:

- a process-launcher capable of running an agent per its `prompt_ref`.
- a write-interceptor that gates per `edit_hardness` and reputation.
- a per-entry advisory lock manager.
- a `run-*` emitter.
- a queue for over-budget runs.

it does not implement: rich UIs, multi-tenant orchestration, real-time discussions, automated discussion-moderator agents. those are downstream.

---

## 30. bootstrap procedure

### 30.1 the bootstrap order

at first run, the vault is empty. bootstrap is **entirely human-authored** — agents do not exist yet, and even after their manifests are written, they have no permission to write structural entries (§1.6.1). the bootstrap order:

1. **write `lens-lens` first.** without it, no other lens can be classified.
2. **write the other 13 decision-tree lenses** in priority order.
3. **write the 6 annotation lenses.**
4. **write the 6 seed domain entries.**
5. **write the seed policies** (§29.2). order:
   - `policy-phase` first, declaring the operative phase as `phase-1` (the runtime reads this to enforce §1.6.1 lockdown on every subsequent write).
   - `policy-runtime` next (the runtime needs to know its boundaries).
   - `policy-classification`, `policy-entry-layout`, `policy-claim-segmentation`, `policy-edit-hardness` next (they shape every subsequent write).
   - `policy-ingestion`, `policy-merge`, `policy-lint`, `policy-assessment`, `policy-archival`, `policy-reputation-weighting`, `policy-thesis-eval`.
   - `policy-notability`, `policy-structure-notes`, `policy-high-stakes`, `policy-contentious-domain`, `policy-pending-changes`, `policy-rule-promotion`, `policy-discussions`, `policy-reingestion`, `policy-content-quality`.
   - `policy-agent-lifecycle` last (it depends on most of the others; inert in phase 1 per §16.3.0).
6. **write the seed guidelines and essays** (§29.3).
7. **write the seed agent entries** (§29.6) with `lifecycle_stage: proposed`.
8. **write the seed agent-test entries** (§29.7), `authoritative: true`.
9. **run the seed agent-tests** against the bootstrapped vault. record results in `run-seed-tests-{date}`.
10. **write the seed thesis-eval panel** entries and run the unaided baseline. record in `run-seed-thesis-eval-baseline-{date}`.
11. **promote seed agents** from `proposed` to `active` via human review.
12. **build initial indexes** via `pnpm build:vault-indexes`.
13. **emit `run-bootstrap-{date}`** recording the entire bootstrap.

### 30.2 bootstrap human-review check

the bootstrap is the period before reputation gates can take over. a human reviewer:

1. reads every seed lens and approves.
2. reads every seed policy and approves.
3. reads every seed agent manifest and approves promotion to `active`.
4. reads the seed thesis-eval baseline and approves it as the reference.

the human reviewer's approvals are recorded as `notification-approval-*` entries linked from the seed runs.

### 30.3 first-source ingestion

once bootstrap is complete, the first source can be ingested per §17. the first ingestion is the test of whether bootstrap was correct: lint must run, findings must surface, the agent's writes must land (subject to edit-hardness), and the closeout must emit a clean `run-chapter-closeout-*` entry.

if any of those fails, the failure is debugged in the seed phase before opening to a second source. seed-phase failures are not findings; they are bootstrap defects, recorded in a `run-bootstrap-defect-{date}` entry and corrected by human edit.

---

## 31. governance: edits to this document

### 31.1 this spec is itself a governance object

amendments to this document are `restricted`-tier edits. they require:

- a `discussion-spec-amend-{date}` entry where the proposed change is described and debated.
- meta-rule quorum (§9.4).
- a `run-spec-amend-{date}` entry that records the change.

### 31.2 the spec is descriptive once working documents exist

once a working document has been generated from this spec — a policy entry, a runtime module, a lens — that working document is the authority on its own behavior. divergence between such a working document and this spec is not a conflict that the spec adjudicates: the working document governs itself; the spec, if it still serves any purpose, may be updated as a historical record of the original blueprint, but it does not enforce against the working artifact.

### 31.3 the spec is not referenced from working documents

per §1.2, working documents do not link back to this spec. the spec's reach ends at the moment of translation. amendments to this spec therefore have no effect on already-generated working documents; their effect is limited to subsequent translation passes that produce new working documents from the amended blueprint.

---

## 32. vocabulary index

a quick reference for terms used throughout this spec.

| term                      | section                                                                                         |
| ------------------------- | ----------------------------------------------------------------------------------------------- |
| atom                      | §3.2, §11.1                                                                                     |
| advisory finding          | §20.5                                                                                           |
| annotation lens           | §7.1, §7.3                                                                                      |
| asymmetric removal        | §14.3                                                                                           |
| blocking finding          | §20.5                                                                                           |
| borderline (notability)   | §8.2                                                                                            |
| bootstrap                 | §30                                                                                             |
| category                  | §1.4, §3 (synonymous with `kind` in this spec; see [§35.1](#351-the-category-vocabulary-clash)) |
| claim                     | §10.1                                                                                           |
| classified_by             | §4.2                                                                                            |
| cluster                   | §11.1, §11.4                                                                                    |
| confidence                | §4.2                                                                                            |
| confirmed (tier)          | §9.1                                                                                            |
| content (tier)            | §3.1                                                                                            |
| contentious domain        | §15                                                                                             |
| decision-tree lens        | §7.1, §7.2                                                                                      |
| disambiguation entry      | §6.4                                                                                            |
| domain                    | §12                                                                                             |
| edit-hardness             | §9                                                                                              |
| evidence grade            | §10.1.2                                                                                         |
| extended-confirmed (tier) | §9.1                                                                                            |
| finding                   | §21                                                                                             |
| guideline                 | §13                                                                                             |
| high-stakes               | §14                                                                                             |
| indexes                   | §26.4                                                                                           |
| infrastructure (tier)     | §3.1                                                                                            |
| ingestion pipeline        | §17                                                                                             |
| lead                      | §5.2                                                                                            |
| lens                      | §7                                                                                              |
| locked (tier)             | §9.1                                                                                            |
| meta-rule quorum          | §9.4                                                                                            |
| noticeboard               | §23                                                                                             |
| notability                | §8                                                                                              |
| open (tier)               | §9.1                                                                                            |
| pending changes           | §9.5                                                                                            |
| persona                   | §16.5                                                                                           |
| policy                    | §13                                                                                             |
| reputation                | §9.6                                                                                            |
| reingestion               | §18                                                                                             |
| relation                  | §10.2                                                                                           |
| restricted (tier)         | §9.1                                                                                            |
| run                       | §25                                                                                             |
| runtime                   | §26.6                                                                                           |
| slice                     | §16.2, §27.1                                                                                    |
| slug                      | §6                                                                                              |
| structure note            | §11                                                                                             |
| thesis-eval               | §28.5                                                                                           |
| three-tier rule system    | §13                                                                                             |

---

## 33. worked example — ingesting a single chapter end-to-end

a concrete walkthrough of phases 0–4 for one chapter of one source. illustrative only; not normative beyond the rules already given.

### 33.1 the source

book: "make it stick: the science of successful learning" by peter c. brown, henry l. roediger iii, and mark a. mcdaniel. published 2014.

source slug: `make-it-stick`.

### 33.2 phase 0 — source intake

1. `raw/make-it-stick/make-it-stick.md` — the source text. immutable.
2. `raw/make-it-stick/make-it-stick-process-trace.md`:
   ```
   title: Make It Stick
   author: Brown, Roediger, McDaniel
   year: 2014
   chapters: 8
   editor_agent: agent-editor-learning-theory
   high_stakes_class: none
   domains: [learning-theory, pedagogy]
   ```
3. `wiki/entries/make-it-stick.md`:
   ```yaml
   ---
   id: make-it-stick
   title: 'Make It Stick'
   category: source
   produced_by: pipeline-source-intake
   domains: [learning-theory, pedagogy]
   tags: [book]
   sources: [make-it-stick]
   aliases: ['Make It Stick: The Science of Successful Learning']
   created: 2026-04-27
   updated: 2026-04-27
   confidence: high
   status: stub
   notability_status: passes
   edit_hardness: confirmed
   high_stakes_class: none
   quality: stub
   author: 'Brown, Roediger, McDaniel'
   year: 2014
   source_file: 'raw/make-it-stick/make-it-stick.md'
   date_ingested: 2026-04-27
   ---
   ```
   body has `## Lead`, `## Summary` (initial), empty `## Key ideas`, `## Notable claims`, `## Connections`.
4. domain inheritance: both `learning-theory` and `pedagogy` are non-contentious. `evidence_grade_floor: D`. defaults apply.
5. source-level high-stakes: `none`.
6. editor agent: `agent-editor-learning-theory`, reputation 5.0 (sub-confirmed; writes will land as pending). human reviewer is the confirmed proxy for seed.
7. emit `run-source-intake-make-it-stick`.

### 33.3 phase 1 — chapter 1 setup

chapter 1: "learning is misunderstood" (32 pages).

1. tracker row: `chapter 1 — in-progress`.
2. `temp/` cleared.
3. read the chapter. identify 3 sub-sections: "what we get wrong about learning", "the testing effect introduced", "fluency illusion and metacognitive failure".
4. tracker rows for sub-sections added.
5. `temp/_staging-index.md` created.

### 33.4 phase 2 — sub-section 1 ("what we get wrong about learning")

candidates identified:

- a concept: "the fluency illusion" — a metacognitive trap where re-reading produces a feeling of mastery without actual learning.
- a claim: "highlighting and re-reading are among the least effective study strategies" (asserts about [[highlighting]] and [[rereading]]).
- a passing mention of david geary's primary/secondary distinction (already an entry in vault).

processing each:

1. **fluency illusion**:
   - notability: `passes` (covered in multiple sources, referenced widely).
   - decision tree: walks past lens-lens, lens-policy-tier, lens-source, lens-structure-note, lens-disambiguation, lens-illustration (no story), lens-relation (not an edge), lens-claim (not a single atom), lens-application (not steps), lens-question (not a question), lens-entity (not a proper noun), lens-process (not stages), lens-insight (not a 2+ concept relationship), lens-concept → match. `category: concept`, `classified_by: lens-concept`.
   - annotation: `confidence: high`, `evidence_grade` n/a (not a claim), `high_stakes_class: none`, `edit_hardness: open`.
   - slug: `fluency-illusion`. check `wiki/entries/fluency-illusion.md` — does not exist. `new`.
   - lead: body is ~300 words; lead required. drafted: "the fluency illusion is the metacognitive failure of mistaking the ease of recognizing material for the ability to recall it; readers who re-read fluent text feel they have mastered it but cannot reproduce its content under test."
   - written to `temp/fluency-illusion.md` blind.
2. **claim "highlighting and re-reading are among the least effective"**:
   - notability: `passes` (multi-source, foundational claim).
   - decision tree: lens-claim matches.
   - annotation: `evidence_grade: B` (cited in make-it-stick as a synthesis of multiple primary studies; not the primary literature itself), `high_stakes_class: none`, `confidence: high`.
   - slug: `claim-highlighting-rereading-low-effective`.
   - lead: not required (single-sentence claim).
   - written to `temp/claim-highlighting-rereading-low-effective.md`.
3. **geary mention**:
   - already an entry. no new staging needed; the sub-section will produce a wikilink in the body of `fluency-illusion` ("contrast with [[biologically-primary-and-secondary-knowledge]]") that resolves to existing.

`temp/_staging-index.md` updated. sub-section 1 row marked complete.

### 33.5 phase 2 — sub-sections 2, 3 (compressed)

sub-section 2 produces: a concept entry `testing-effect`, a claim about retrieval-strength asymmetry, an illustration retold from a study described in the chapter.

sub-section 3 produces: a structure-note candidate? — the chapter introduces an organizing frame for "what learners get wrong" with multiple traps. `lens-structure-note` evaluates: does the body organize via annotated links rather than assert? — yes if the editor synthesizes the chapter into a structure note. classified as `structure-note`. slug: `structure-misunderstood-learning-traps`. lead drafted; load-bearing-entries section enumerates `fluency-illusion`, `testing-effect`, `metacognitive-failure`.

each sub-section's invariants are checked and marked complete.

### 33.6 phase 3 — chapter 1 merge

for each temp file:

- `fluency-illusion.md` — `wiki/entries/fluency-illusion.md` does not exist → move temp to wiki.
- `claim-highlighting-rereading-low-effective.md` — does not exist → move to wiki.
- `testing-effect.md` — already exists in vault. apply concept-merge rule (full prose consolidation; appended sources and connections). resolve. emit `run-merge-testing-effect`.
- `structure-misunderstood-learning-traps.md` — does not exist → move to wiki.
- claims and other staged units handled likewise.

### 33.7 phase 4 — chapter 1 closeout

1. update source entry: append "fluency illusion", "testing effect", "metacognitive failure" to `## Key ideas`. update `## Connections` with the new entries.
2. structure-note coverage: chapter created a new structure note covering 3 entries. cluster size below threshold (8) elsewhere. no findings.
3. notability promotion: no borderline entries from this chapter.
4. high-stakes review: no high-stakes claims.
5. lint sweep: every touched entry. fluency-illusion's body has 2 outbound wikilinks; passes `low-link-density` floor. lead present; passes `lead-missing`. no blocking findings.
6. pending review: editor was sub-confirmed, so all writes landed as pending. human reviewer accepts each. on accept, the proposals merge; final entries appear under `wiki/entries/`. emit `run-merge-*` per acceptance.
7. index rebuild: `pnpm build:vault-indexes`. main index gains 3 new entries; learning-theory and pedagogy domain indexes gain entries.
8. noticeboard rebuild: no findings of note this chapter, so most boards unchanged. `notability-deferrals.md` unchanged. `pending-changes.md` shrinks (proposals accepted).
9. structure-note narrative pass: `structure-misunderstood-learning-traps` is the chapter's own contribution, so its `## How the cluster is held together` section is fully written this pass; no other structure notes were materially reshaped, so no further updates.
10. tracker: chapter 1 row marked complete with per-chapter counts recorded inline (4 entries created, 1 merged, 1 structure note added, 0 findings raised).
11. clean `temp/`.
12. emit `run-chapter-closeout-make-it-stick-1` recording reads, writes, findings, and active policy/lens versions per §25.3. this run entry plus git history is the canonical record of the chapter's work; no separate vault-wide log is appended.

### 33.8 lessons illustrated

- the editor agent's sub-confirmed reputation is the load-bearing constraint that puts every write through human review during seed.
- the structure note is what gives the chapter cohesion at retrieval time — its lead summarizes the chapter's organizing frame in 1–3 sentences.
- the claim is treated as its own entry because it is multi-source and load-bearing; if the chapter had only one weak source, the claim would be borderline-notability and stage as pending.
- merging an existing entry (testing-effect) preserves the existing entry's connections from later chapters of other sources; the temp version's prose is consolidated, but the connections remain intact.

---

## 34. error and failure handling

### 34.1 errors classed by stage

| stage   | error class                                                | response                                                                                |
| ------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| phase 0 | source slug collision                                      | halt; rename and retry.                                                                 |
| phase 0 | malformed process trace                                    | halt; repair; retry.                                                                    |
| phase 1 | `temp/` not clean                                          | halt; clear; retry.                                                                     |
| phase 1 | sub-section identification failure                         | halt; manual sub-section assignment by editor.                                          |
| phase 2 | candidate classification gap                               | emit `finding-classification-gap`; continue with other candidates; revisit at closeout. |
| phase 2 | slug collision (different subject)                         | per §6.4 disambiguation.                                                                |
| phase 2 | slug collision in temp (different subject in same chapter) | halt sub-section; manual repair.                                                        |
| phase 3 | merge classification mismatch                              | emit blocking finding; halt that file's merge; other files proceed.                     |
| phase 3 | merge high-stakes mismatch                                 | emit blocking finding; halt that file's merge.                                          |
| phase 4 | lint blocking finding                                      | halt closeout for affected entry; finding must resolve before closeout completes.       |
| phase 4 | pending-review timeout                                     | continue closeout; pending proposals roll forward; advisory finding.                    |

### 34.2 partial completion

a chapter that does not reach closeout cleanly remains `in-progress`. retry is the same procedure; the editor reads the tracker, identifies which sub-section to resume from, and continues. the `_staging-index.md` and `temp/` state from the failed run is the recovery starting point.

### 34.3 catastrophic recovery

git history is the canonical recovery substrate. a vault that becomes inconsistent (e.g., simultaneous lock failure) is rolled back via `git revert` of the offending commits. `run-*` history may show writes that no longer exist on disk; lint `dangling-run-references` flags these for cleanup.

### 34.4 human-in-the-loop handoffs

the seed phase has the human reviewer in the loop for every quorum action and every pending-review acceptance. as the population matures, these handoffs migrate to confirmed agents. the migration is a per-policy decision: each policy declares when reputation-gating supersedes human review.

---

## 35. open issues / deferred decisions

### 35.1 the "category" vocabulary clash

the vault uses "category" for the lens-output kind of an entry. wikipedia uses "category" for navigational hierarchies, which are closer to the vault's domains plus tags. reader confusion is real. the planned rename is "category" → "kind" everywhere, with corresponding lens nomenclature shift (`lens_covers_category` → `lens_covers_kind`). mechanical but invasive across the codebase. retained through seed; revisited before opening to outside contributions.

### 35.2 reputation thresholds

the v0 thresholds in §9.1 (30, 60, 80) are placeholders. once population behavior is observable, they will be recalibrated. the recalibration is itself a `policy-edit-hardness` edit.

### 35.3 promotion-path calibration

the citation-count and finding-count thresholds for essay→guideline→policy promotion are placeholders. specifically:

- "3 citations" for essay→guideline.
- "5 findings citing the guideline" for guideline→policy.

these are guesses. once promotion has been exercised a few dozen times, the rule will be recalibrated against observed quality.

### 35.4 lifecycle stage on rule entries

§13.4.4 names retirement of rules. an additional infrastructure-frontmatter field `lifecycle_stage: active | proposed | retired` for rule entries (parallel to agents) is implied but not added to §4.3.14. resolution: add the field, lint enforces.

### 35.5 aborted run status

§26.8 names a `status: aborted` field on `run-*` entries. the field is not in §4.3.16. resolution: add.

### 35.6 seed-thickness calibration

the seed in §29 is a v0 commitment. how much can be cut without the loop failing to reach a stable state, and how much must be added before reputation gates can take over from human review, will become clear only once the seed runs. expect revision.

### 35.7 generalizing ingestion to arbitrary text

the pipeline (§17) is shaped for long-form structured sources. extending to transcripts, emails, chat logs, and unstructured notes will need new policies and possibly new lenses. seed phase scopes to structured sources.

### 35.8 retrieval shape beyond v0

the v0 retrieval algorithm (§27) is a sketch. the right shape is whatever maximizes variance reduction per token. expect revisions to:

- the slice-resolution step.
- the orthogonality threshold.
- the lead-vs-body switch logic.
- the relation-traversal depth (currently fixed at 1 hop).

each revision is a `policy-content-quality` or `policy-thesis-eval` edit.

### 35.9 adversarial robustness

population mechanics assume good-faith collaboration. collusion, sybil patterns, prompt-injection from sources, and recursive privilege-escalation (a high-reputation agent editing the lens that confers its authority) are not yet modeled. an explicit threat model is required before the vault is exposed to outside contributions.

### 35.10 the runtime / vault boundary

`runner/` is described in §26.6 and `policy-runtime`, but the exact api between vault entries and runtime invocation is not spelled out here. resolution: a `policy-runtime` entry with the api specification, written before the seed agents are activated.

### 35.11 backup and migration

archival (§26.3) describes hot-cold split; backup of the cold archive is not specified. resolution: the cold archive is backed up to a write-ahead log managed by `runner/` per `policy-archival`.

### 35.12 cross-language and cross-locale

every entry assumes a single language (english at seed). multilingual ingestion (translations, source in another language) is not specified. resolution: deferred until a non-english source is required.

### 35.13 the agent-test answer-shape grader

agent tests have an `expected_shape`. how exactly the grader compares an answer to the shape is not specified. resolution: a `policy-agent-test-grading` entry, with a v0 grader that uses semantic similarity over key concepts plus a checklist over named entities.

### 35.14 what counts as good reputation, formally

the events in §9.6 are first candidates. the weighting in `policy-reputation-weighting` is a placeholder. resolution: ongoing calibration during seed and for the first six months of operation.

### 35.15 retrieval quality measurement granularity

the variance-reduction metric in §28.5 is computed over the panel as a whole. per-task and per-domain variance reduction are useful too. resolution: extend `policy-thesis-eval` to track per-domain metrics once enough data accumulates.

---

_end of specification_
