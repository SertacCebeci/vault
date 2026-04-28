# vault specification

> this is the vault's operational specification. it describes — in extreme detail — what the end product is, in entity-architecture terms only. it is the source from which an implementation is generated under a clean-room schema; it is itself not the implementation. everything in this document is binding.

## table of contents

0. [context glossary](#0-context-glossary)
1. [document scope and conventions](#1-document-scope-and-conventions)
2. [storage scopes](#2-storage-scopes)
3. [entry kinds — the complete catalog](#3-entry-kinds--the-complete-catalog)
4. [canonical header schema](#4-canonical-header-schema)
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
27. [retrieval contract](#27-retrieval-contract)
28. [assessment and the thesis-eval panel](#28-assessment-and-the-thesis-eval-panel)
29. [starting configuration](#29-starting-configuration)
30. [bootstrap procedure](#30-bootstrap-procedure)
31. [the spec is absolute](#31-the-spec-is-absolute)
32. [vocabulary index](#32-vocabulary-index)
33. [worked example — ingesting a single chapter end-to-end](#33-worked-example--ingesting-a-single-chapter-end-to-end)
34. [error and failure handling](#34-error-and-failure-handling)

---

## 0. context glossary

a plain-language guide to the vocabulary used throughout this spec. each term is described in everyday words, with the problem it solves attached. read this section first if the rest of the document feels dense; it answers "what is this and why does it exist." the terse, pointer-only index is at §32.

### 0.1 the substance: entries and where they live

**entry.** the atomic unit of the vault. one identifier, one header, one body. a concept entry, a source entry, a policy entry, a run entry — every artifact in the vault, content or infrastructure, is an entry. the vault is a single uniform pile of entries that link to each other.

**slug.** an entry's unique identifier — lowercase, hyphenated. `desirable-difficulty`, `policy-ingestion`, `agent-editor-learning-theory`. how entries reference each other.

**the entries pile.** the single flat collection of every entry the vault holds. no folders, no nesting. you find an entry by its slug. flatness is intentional: hierarchy biases what is findable; the link graph is the answer instead.

**source intake.** the area where raw documents (books, articles, transcripts) live before and during ingestion. immutable; never modified after admission. the source document and the entries the vault produces from it are kept separate.

**ephemeral staging.** a scratchpad used during ingestion. when a chapter is being processed, all the draft entries get written here first. they are merged into the entries pile in a single batch and the scratchpad is wiped. the reason it exists: ingestion writes **blind** — without reading any pre-existing entry on the same topic — to avoid anchoring bias. staging is where those blind drafts wait so the merge step can compare them against what already exists, deliberately, in one pass. without staging, every chapter would dribble edits piecemeal into existing entries, biased by what was already written.

**meta projections.** rebuilt views over the entries pile — domain catalogs, noticeboards, dashboards. think cached query results. they are never source-of-truth; the entries pile is. they are reproducible by mechanical rebuild from the entries.

**runtime.** the process that actually executes agents, accepts their writes, and applies the gates (reputation checks, edit-hardness checks, lockdown checks). it sits outside the entries pile. agents propose; the runtime decides whether the write lands directly or becomes a pending proposal.

### 0.2 the kinds: what an entry can be

**content vs. infrastructure.** content entries carry knowledge — concepts, claims, illustrations, sources. infrastructure entries carry vault state — runs, findings, policies, lenses, agent manifests. they share the same shape but differ in classification path, retention, and write rate.

**concept.** the catch-all content entry. one idea, explained on its own terms. e.g., `desirable-difficulty`.

**source.** the literature note for one raw document. cites and summarizes; does not synthesize.

**claim.** the smallest verifiable assertion in the vault — one sentence with evidence. e.g., "spaced repetition outperforms massed practice for long-term retention." promoted from inline mention to its own entry only when load-bearing.

**relation.** a typed, directed edge between two entries — `supports`, `contradicts`, `instance-of`, `supersedes`, `depends-on`. carries its own evidence, like a claim.

**question.** an open question the vault cannot yet answer. an explicit way to mark a gap rather than pretend it isn't there.

**illustration / application / entity / process / insight.** the other content kinds, each handling a recognizable shape: illustration is a story (protagonist, setting, outcome), application is steps a practitioner can follow, entity is a proper-noun subject (person, framework, theory), process is a multi-stage sequence, insight names a non-trivial connection between two or more concepts.

**structure note.** organizing prose plus an annotated link list, holding a region of the graph together. the vault's answer to "how do you carry big-picture information without imposing a hierarchy." instead of a parent article, several structure notes can frame the same cluster from different angles (a learning-theory frame, a neuroscience frame).

**disambiguation.** a routing entry for a slug that could mean more than one thing. lists each variant with a one-line distinguisher.

**lens.** a classification rule, written as a yes/no question with criteria. lenses decide which kind a new entry is. lenses are themselves entries.

### 0.3 lenses: how an entry's kind gets decided

**why lenses exist.** the question "is this entry a concept or an illustration?" needs a deterministic answer. a lens is the recorded answer for one question, applied to one new entry by walking down a tree of yes/no checks. the entry's `classified_by` field names which lens ruled, so the decision is auditable years later.

**decision-tree lens.** answers "what kind is this entry?" — exactly one rules per entry; first match along a priority order wins.

**annotation lens.** answers "what other label does this entry need?" — confidence, evidence grade, edit-hardness, etc. annotation lenses do not compete; each runs independently and stamps its own field.

**notability.** the gate that asks "does this idea deserve its own entry, or should it just be a sentence inside another entry?" a unit passes if it has multi-source coverage, routing necessity (other entries already point at it), or an explicit policy carve-out. units that pass become entries; units that fail get folded into a parent. units that are borderline get held in a pending area until a later ingestion provides another inbound link or another source.

### 0.4 governance: policies, guidelines, essays — and why they exist

**policy.** a binding rule. examples: "every claim must cite a source." "every entry has a slug." policies are how the vault tells itself what is and is not allowed. when a write violates a policy, lint produces a blocking finding and the write does not land. policies exist because a self-governing system needs its rules written down where agents can read them, not baked invisibly into code that no one revisits.

**guideline.** a non-binding norm. example: "prefer noun-first slug names." violations produce advisory findings — recorded and reviewed, but the write still lands. guidelines exist because not every preference deserves to be a hard rule, but the preference still wants to be visible.

**essay.** an under-development take that binds nothing. the staging ground for ideas that might one day become guidelines or policies. having an explicit "we suspect this but haven't ratified it" tier prevents premature ratification and keeps the policy set honest.

**why three tiers and not one.** binding rules, soft norms, and exploratory thoughts have very different consequences when wrong. mixing them flattens the consequences. separating them lets an agent know whether a violation is fatal, advisory, or just intellectual chatter.

**structural lockdown.** policies, guidelines, essays, lenses, domains, agent manifests, and this spec are written by humans at bootstrap and are never edited by agents thereafter. agents enforce the rules within the structure; they do not author the structure. this is the firewall that prevents an agent from rewriting its own constraints.

### 0.5 edit-hardness, reputation, and pending changes

**edit-hardness.** a per-entry tier — `open`, `confirmed`, `extended-confirmed`, `restricted`, `locked` — that says "how trusted does an agent have to be to edit this directly." a fresh concept entry is `open`; a structure note is `confirmed`; a policy is `locked`.

**reputation.** a 0.0–100.0 score per agent that grows with successful work (passing tests, producing entries that survive lint, being cited) and shrinks with reverts and failed tests. it is a permission mechanism, not a market signal — agents do not "spend" reputation, only earn or lose it.

**pending changes.** when a low-reputation agent attempts a write to an entry it lacks the trust to edit directly, the write does not land. it is converted into a `pending-*` proposal — a parallel entry attached to the target — that a higher-reputation agent later reviews and either accepts (merges) or rejects. exists because a system with many agents of varying trustworthiness needs to admit contributions without granting low-trust agents direct write access. pending changes is the queue that reconciles "lots of agents want to write" with "not all of them have earned the right to write directly."

**quorum.** a heavyweight action requiring multiple high-reputation agents voting independently. used for reversibility-low actions: overriding a blocking finding, retiring an agent.

### 0.6 domains, contentious domains, and high-stakes

**domain.** a subject axis — `learning-theory`, `pedagogy`, etc. each entry declares one or more domains in its header. domains are how retrieval is sliced and how editor agents are scoped (a learning-theory editor reads and writes within learning-theory).

**contentious domain.** a domain where claims are politically or scientifically loaded. toggling `contentious: true` on a domain raises floors across every entry in it (stricter evidence floor, harder edit-hardness, shorter discussions, mandatory citations). exists because the ordinary rules are calibrated for cooperative, non-contentious knowledge work; some subjects need stricter handling by default.

**high-stakes class.** a per-claim flag for claims whose error has real-world cost — `medical`, `legal`, `safety`, `identifiable-individual`. when a high-stakes claim's evidence is below a stricter floor, the claim is **removed** from the entry and replaced with a placeholder until evidence improves. exists because the cost of a wrong claim varies enormously by subject; a wrong claim about study tactics is harmless, a wrong claim about drug dosages is not. defaulting to "remove rather than display" inverts the usual bias toward showing whatever you have.

**evidence grade.** `A` (primary literature) → `D` (anecdotal). every claim and relation carries one. domains can require minimum grades.

### 0.7 activity: runs, findings, discussions, noticeboards

**run.** the record of one agent execution. who ran, what they read, what they wrote, what findings they raised, which lens and policy versions were active. immutable. runs are the canonical "what happened" record at the agent-action level; together with the audit log (entry-content level), they support full auditability without a separate hand-authored log.

**finding.** a problem the vault has noticed about itself — a missing lead, a broken reference, a contradiction. every finding is its own entry. the union of open findings is the vault's running to-do list. `severity: blocking` stops the offending write; `advisory` just records.

**discussion.** a recorded exchange between agents who disagree about an entry. round-bounded (5 rounds max, 3 in contentious domains). exists because agents will disagree; without a structured place for the disagreement, it has nowhere to go. discussions terminate via a named protocol: `content-quorum` for content disputes, `meta-rule-quorum` for reversibility-low actions, `advisory` (no binding outcome) for disputes about structural entries — agents may discuss a policy or a lens, but they cannot change one through the discussion.

**noticeboard.** a projection — a cached list — of open findings of a given kind. agents that specialize in a kind of issue (e.g., "I review contradictions") subscribe to the relevant noticeboard instead of scanning the whole finding list. this keeps each agent's working set bounded.

### 0.8 lead, body shape, references

**lead.** a 1–3 sentence compression of an entry's content, placed at the top of the body. retrieval (§27) returns leads first; full bodies only when the consumer's token budget allows. so the lead is not flavor text — it is the entry's retrieval-time face. a sloppy lead (mostly restating the title, hedging where the body is decisive) degrades quality across every query that lands on the entry. that is why leads are lint-checked, why structure notes and source entries always need one regardless of size, and why contentious domains require leads regardless of size.

**body shape.** every entry's body is named sections in a defined order: lead, then a kind-specific main section, then connections, sources, and an optional mentioned-in. order is enforced because retrieval reads in this order.

**reference.** a link from one entry to another, written `[[slug]]` in this spec's notation. references must resolve — the target must exist. every content entry needs at least 2 outbound references (the link-density floor), or it is a finding; structure notes need many more.

**connections section.** the structured list of typed links at the bottom of a body. inline predicates (`Related to`, `Coined by`) stay in the connections section; load-bearing predicates (`Supports`, `Contradicts`) produce a separate `relation-*` entry because they participate in retrieval traversal.

### 0.9 agents: who acts on what

**agent.** an entry of kind `agent-*` describing one active process. its manifest names what it reads, what it writes, its prompt strategy, its reputation, its baseline tests. an agent is exactly one of three kinds.

**editor.** an agent that writes content during ingestion. one editor per source domain is typical.

**persona.** an agent that answers queries against its declared slice. does not write content. used to test the vault: if a learning-theory persona cannot answer a learning-theory question, the vault has a gap. failing a persona's baseline test surfaces that gap as a finding.

**lint.** an agent that mechanically enforces policies and guidelines by emitting findings. never writes content.

**slice.** what an agent reads and writes — its `read_domains`, `write_domains`, voice rules (for personas), refusal rules (for personas), policy targets (for lint). the slice constrains everything the agent does.

**ingestion.** the multi-stage pipeline by which a raw source becomes entries: source intake (admit the document), chapter setup, per-sub-section staging (write blind into ephemeral staging), chapter merge (merge staged drafts into the entries pile), chapter closeout (update indexes, run lint, etc.). a chapter is the natural unit; the default is one chapter per turn.

**reingestion.** redoing a chapter that was already ingested — usually because the lens set or policy set changed. the staged content is treated as a depth upgrade on prose; existing connections (which accumulated from later chapters) are preserved.

**thesis-eval.** the fixed panel of verifiable tasks that measures the vault's actual usefulness. the **unaided baseline** is recorded once (a capable model attempting the task with no vault context); the **vault-augmented runs** are recorded over time. variance reduction between unaided and augmented runs is the headline metric — it is how the vault knows whether it is doing the thing it claims to do.

---

## 1. document scope and conventions

### 1.1 purpose

this document describes — in extreme, unambiguous detail — what the end product is. its purpose is to serve as the blueprint from which the end product is produced under a clean-room implementation schema: the blueprint is read once, the end product is realized from it, and the result thereafter stands on its own. the spec itself is a blueprint, not part of what it describes.

### 1.2 what this document specifies

this spec describes architecture only. it names what entities exist, what information each entity carries, why each entity is needed, what processes operate on those entities, and how entities interact. those are its sole concerns.

it does not describe how any of this is realized. whether an entity is a file, a database row, or some other artifact; whether a process is a script, a runtime module, or instructions an agent follows; what anything is called in storage; how artifacts are laid out — all out of scope. in particular: no folder names, no file names, no file extensions, no script names, no command names, no programming languages, no database engines, no runtime topologies, no syntax formats appear in this document. if any do, the spec is wrong on that point and is to be amended.

this rule binds the entire spec: every section, every example, every table, every code block, every reference.

### 1.3 authority

this spec is the highest-authority document at the moment a system is produced from it: nothing else outranks it for that purpose. it confers no ongoing authority against an implementation that already exists. once an implementation is produced, it carries its own authority and is governed by its own rules. divergence between an implementation and this spec is not a conflict to be resolved against the spec: the implementation is the authority on its own behavior; the spec, at most, is a record of the original blueprint.

### 1.4 notation

- `slug` — the unique identifier of an entry, lowercase, hyphenated.
- `[[slug]]` — a reference to the entry with that identifier. used as the citation form throughout the spec.
- `policy-*`, `lens-*`, etc. — identifier pattern: every entry of that kind carries an identifier with the given prefix. `*` is a placeholder.
- `header:field` — a named field in an entry's header (the metadata each entry carries; see §4).
- `kind` — the value of an entry's `category` header field. ("category" and "kind" are used interchangeably throughout this spec.)
- `confirmed`, `extended-confirmed`, etc. — edit-hardness tiers (§9).
- `passes`, `borderline`, `fails` — notability stamps (§8).
- `A`, `B`, `C`, `D` — evidence grades (§10).
- dates are written `YYYY-MM-DD`; timestamps include time-of-day with timezone.
- counts are integers; thresholds are integers unless explicitly fractional.
- prose is lowercase.

### 1.5 the structural lockdown

the vault is **self-governing, not self-adapting**. agents enforce the rules within the structure described here, but they do not author the structure itself. agents generate new instances of entries and run the processes the spec defines; they do not invent new entry kinds, new lenses, new policies, new domains, or new agent manifests.

the following are locked against agent writes regardless of the per-entry edit-hardness defaults defined in §9.2:

- every `lens-*` entry (the classification rules)
- every `policy-*`, `guideline-*`, `essay-*` entry (the rule tiers — every tier; essays are locked because authoring an essay is the structural act of proposing a rule)
- every entry whose `category` is `domain` (the subject axes)
- every `agent-*` entry (the population manifest)
- this specification

agents may **read** all of the above. agents may **discuss** all of the above (§22) — but a discussion whose disputed object is one of these entries terminates as advisory only (§16.8.3); the disputed object is not modified by the discussion's outcome.

what agents may write:

- content entries — `concept`, `source`, `illustration`, `application`, `entity`, `process`, `insight`, `claim`, `relation`, `structure-note`, `disambiguation`, `question` — subject to per-entry edit-hardness and notability rules.
- their own work products — `run-*`, `finding-*`, `discussion-*` (rounds and termination on content disputes), `notification-*`, `pending-*`. these are agent outputs by construction.

the runtime rejects writes to locked kinds pre-check; no reputation is consumed and no partial state is written. rejection emits `finding-structural-lockdown-violation-{target-slug}`.

### 1.6 the three pillars

the vault has three pillars. every section of this specification belongs to exactly one. the table is the navigation aid for the rest of the document.

| pillar                  | what it defines                                                                                | sections                                                                                                                                              |
| ----------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **wiki structure**      | what entries exist, how they are shaped, how they are organized                                | §2 scopes · §3 entry kinds · §4 header · §5 body · §6 slugs · §7 lenses · §8 notability · §11 structure notes · §12 domains                           |
| **wiki governance**     | the rules that bind agent behavior, how those rules are enforced                               | §9 edit-hardness · §13 policy/guideline/essay · §14 high-stakes · §15 contentious · §19 merge · §20 lint · §21 findings · §22 discussions · §23 noticeboards |
| **agentic structure**   | who acts, what they may act on, how they are scored                                            | §10 claims/relations/questions · §16 agents · §17–18 ingestion · §24 agent tests · §25 runs · §26 operations · §27 retrieval · §28 assessment         |

structural entries — every `lens-*`, `policy-*`, `guideline-*`, `essay-*`, `domain`, `agent-*`, and this specification — are out of reach of any agent write. only the work agents do — content edits, run records, findings, content discussions, pending proposals — is agent-driven.

---

## 2. storage scopes

### 2.1 the five scopes

the vault has five logical scopes. they differ in what each holds, who may modify it, and how it relates to the entries that are the substance of the vault.

| scope                | what it holds                                                                                                                | mutability                                                                                                  | retrieval visibility                                                                          |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| source intake        | raw documents being ingested, their per-source ingestion progress records, and supporting media                              | each raw document is immutable after intake; its progress record evolves while ingestion is active          | not retrievable                                                                               |
| ephemeral staging    | per-chapter draft work produced during ingestion                                                                             | cleared at the start of each chapter; otherwise mutable within the chapter                                  | not retrievable                                                                               |
| the entries pile     | every entry — content and infrastructure alike — as a single flat collection, one identifier per entry                       | governed by the edit-hardness and notability rules of each entry's kind                                     | the canonical retrieval surface                                                               |
| meta projections     | rebuilt views over the entries pile — domain indexes, kind-projected noticeboards, dashboards — plus cold archives           | reproducible from the entries pile or recoverable from durable history; never source-of-truth               | not retrievable; consumed by agents that subscribe to specific projections                    |
| runtime              | the population of agents, lints, and gates that act on entries                                                               | external to the entries pile; described in `policy-runtime`                                                 | not part of the entry collection                                                              |

### 2.2 scope rules

- **source intake.** one logical container per source. the source document is fixed at intake and never modified thereafter. the per-source ingestion progress record co-locates with the source. supporting media (images, attachments) co-locates with the source.
- **ephemeral staging.** flat. cleared at the start of each chapter as part of ingestion stage 1 (§17). draft entries use the same identifiers they would carry in the entries pile, so the merge step (§17, §19) can match by identifier alone. staging metadata is namespaced from entry identifiers so the two never collide.
- **the entries pile.** the only flat pile of entries. no nesting, no grouping, no hierarchy. enumerating the pile must reveal every entry the vault holds; nothing about the pile depends on traversal order.
- **meta projections.** entirely synthetic. rebuilt mechanically from the entries pile (per-domain indexes, kind-projected noticeboards, the assessment dashboard) or moved here as cold archives (older runs, resolved findings, closed discussions, retired notifications) per `policy-archival` (§26.3). nothing in the meta projections is hand-authored, and nothing here is source of truth: projections are reproducible by rebuild; archives are recoverable from durable history. hand-authored cross-vault narrative belongs in structure-note entries (§11), not in projections; chronological activity belongs in `run-*` entries and durable history, not in a synthesized log.
- **runtime.** external to the entries pile. the only enforcer of write-scope, reputation gates, and edit-hardness; described in `policy-runtime`.

### 2.3 retrieval surface

retrieval reads the entries pile only. source intake, ephemeral staging, meta projections, and runtime are never visible to retrieval. archives moved out of the entries pile cease to be retrievable until promoted back.

### 2.4 identifier rules

- entry identifiers are lowercase, hyphenated, drawn from `[a-z0-9-]`.
- identifiers do not contain whitespace, separators, or any character outside that set.
- identifiers do not begin with `_`. that prefix is reserved for staging metadata.
- no two entries share an identifier. uniqueness is enforced by the runtime and re-checked by lint.

---

## 3. entry kinds — the complete catalog

### 3.1 the two-tier split

entries split into **content** (the substance of the vault) and **infrastructure** (the vault's own state). they share the flat layout and header schema; they differ in classification path, retention, and write rate.

| tier           | classified via                                                          | retention                     | typical write rate          |
| -------------- | ----------------------------------------------------------------------- | ----------------------------- | --------------------------- |
| content        | the lens decision tree (§7)                                             | persistent                    | one per knowledge unit      |
| infrastructure | a named lifecycle protocol; the `produced_by` header field records which | aggressively archived (§26.3) | a `run` per agent execution |

### 3.2 content kinds

| slug prefix       | kind             | what it carries                                                                                                           | notes                                                              |
| ----------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| (free slug)       | `concept`        | one idea, explained on its own terms. the catch-all when no narrower kind applies.                                        | richest body. always has a lead if above threshold.                |
| (free slug)       | `source`         | literature note for one raw document — book, article, transcript. cites; does not synthesize.                             | always has a lead. one source entry per source-intake container.   |
| (free slug)       | `illustration`   | a story with protagonist, setting, outcome. retells a source narrative to anchor a concept.                               | only kind allowed to retell source prose closely.                  |
| (free slug)       | `application`    | a practitioner-followable instruction set.                                                                                | written as steps a reader can execute.                             |
| (free slug)       | `entity`         | a proper-noun subject — person, institution, theory, framework, method.                                                   | `entity_kind` header field required.                               |
| (free slug)       | `process`        | multi-stage sequence with named transitions.                                                                              | `stages` header field is ordered.                                  |
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
| `policy-`                      | `policy`             | a binding rule. lint enforces. set at bootstrap; locked against agent writes (§1.5).                                                                                     | highest of the three rule tiers (§13).                |
| `guideline-`                   | `guideline`          | a best-practice norm. violations produce advisory findings.                                                                                                              | middle tier.                                          |
| `essay-`                       | `essay`              | an under-development take. binds nothing.                                                                                                                                | lowest tier; promotion path leads upward.             |
| `agent-`                       | `agent`              | the manifest of an active process — editor, persona, or lint. slice + bindings + lifecycle + reputation.                                                                 | `agent_kind` header field is `editor`, `persona`, or `lint`. |
| `run-`                         | `run`                | one agent execution. records reads, writes, findings, active policy/lens versions, identity.                                                                             | dominates entry count by volume; archived to rollups (§26.3). |
| `finding-`                     | `finding`            | a problem the vault has noticed about itself. open/resolved/wontfix.                                                                                                     | links to the rule that fired.                         |
| `agent-test-`                  | `agent-test`         | a query with an expected answer shape, attached to an agent. run as regression.                                                                                          | failure becomes a finding.                            |
| `discussion-`                  | `discussion`         | a recorded exchange between agents disputing an entry.                                                                                                                   | round-bounded (§22).                                  |
| `notification-`                | `notification`       | inter-agent mention, review request, or escalation.                                                                                                                      | short-lived; archived.                                |
| `pending-`                     | `pending` (proposal) | a staged write from a sub-confirmed agent awaiting review.                                                                                                               | parallel state attached to a target entry (§9.5).     |

### 3.4 forbidden combinations

- a content entry must not have a `produced_by` header field. `produced_by` is the marker of infrastructure-protocol authorship.
- an infrastructure entry must not be classified by a lens. its category is set by the lifecycle protocol that produced it. lint check `infrastructure-classified-by-lens` enforces this.
- a lens entry must classify itself via `lens-lens`. lint check `lens-self-classification` enforces this.

---

## 4. canonical header schema

### 4.1 the common header

every entry — content or infrastructure — carries a header of named fields. the common fields below are present on every entry; per-kind extensions appear in §4.3.

### 4.2 field-by-field rules

| field               | type   | required?                         | rule                                                                                                                                                        |
| ------------------- | ------ | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                | string | yes                               | exactly equal to the entry's identifier. lint `id-mismatch`.                                                                                                |
| `title`             | string | yes                               | title case. one entry, one canonical title.                                                                                                                 |
| `category`          | enum   | yes                               | one of the kinds in §3.2 or §3.3. lint `unknown-category`.                                                                                                  |
| `classified_by`     | string | content only                      | identifier of the lens that ruled. its `lens_covers_category` must equal this entry's `category`. lint `classification-consistency`.                        |
| `produced_by`       | string | infrastructure only               | name of the lifecycle protocol that produced this entry, e.g., `pipeline-unpack`, `lifecycle-agent-retire`, `bootstrap`. lint `infrastructure-without-produced-by`.      |
| `domains`           | list   | yes                               | non-empty. every value must equal an existing domain entry's `id`. lint `unknown-domain`, `entry-without-domain`.                                           |
| `tags`              | list   | optional                          | lowercase, hyphenated. tags reducing to a domain name must instead live in `domains`. lint `tag-shadowing-domain`.                                          |
| `sources`           | list   | optional                          | identifiers of source-kind entries. machine-readable shorthand; the body's sources section is the rich attribution. lint `source-attribution-mismatch`.      |
| `aliases`           | list   | optional                          | alternative titles a search query might use.                                                                                                                |
| `created`           | date   | yes                               | first-write date. never modified after creation.                                                                                                            |
| `updated`           | date   | yes                               | most-recent modification date. updated by every write. lint `updated-not-current` after any edit.                                                           |
| `confidence`        | enum   | yes                               | `high` (multiple sources converge), `medium` (one source or weak convergence), `low` (single weak source), `contested` (sources actively disagree).         |
| `status`            | enum   | yes                               | `draft` (work in progress, not retrievable), `stub` (thin but published), `complete` (ratified).                                                            |
| `notability_status` | enum   | content yes; infrastructure `n/a` | set by `lens-notability` at unpack. transitions per §8.                                                                                                     |
| `edit_hardness`     | enum   | yes                               | one of the five tiers (§9.1). set by the classifying lens or the producing protocol; raised by domain inheritance; never lowered.                           |
| `high_stakes_class` | enum   | yes                               | `none` is the default. non-`none` triggers asymmetric removal regime when evidence is below floor (§14).                                                    |
| `quality`           | enum   | optional but recommended          | quality tier (§5.7); separate from `status`.                                                                                                                |

### 4.3 per-kind extensions

each kind may carry additional fields beyond the common header. enumerated below; lint `kind-fields-presence` enforces required fields per kind.

#### 4.3.1 lens

- `lens_question` (string, required) — the yes/no question the lens asks.
- `lens_priority` (integer, required) — lower values run earlier in decision-tree order.
- `lens_covers_category` (kind, required) — the kind this lens ranges over.
- `lens_criteria` (ordered list of strings, required) — checklist items the lens applies in order.
- `lens_kind` (enum, required) — `decision-tree` or `annotation`.

#### 4.3.2 source

- `author` (string, required).
- `year` (integer, required).
- `intake_ref` (identifier, required) — identifier of the source's intake container in source intake (§2.1).
- `date_ingested` (date, required).

#### 4.3.3 entity

- `entity_kind` (enum, required) — `person`, `institution`, `theory`, `framework`, or `method`.

#### 4.3.4 illustration

- `source` (reference to one source-kind entry, required).
- `illustrates` (list of concept identifiers, required).
- `chapter` (string, optional) — known chapter label, or marked unknown.
- `pages` (string, optional) — known page range.

#### 4.3.5 application

- `applies` (list of concept identifiers, required).
- `prerequisites` (list of identifiers, optional).

#### 4.3.6 process

- `stages` (ordered list of stage identifiers, required) — order is meaningful.
- `preconditions` (list of identifiers, optional).
- `postconditions` (list of identifiers, optional).

#### 4.3.7 insight

- `connects` (list of identifiers, required) — at least 2 entries.

#### 4.3.8 claim

- `claim_text` (string, required) — the assertion as a single declarative sentence.
- `evidence_grade` (enum, required) — `A` | `B` | `C` | `D` (§10.2).
- `evidence_pointers` (list, required) — each pointer carries a source reference, a page locator, and optionally a quoted excerpt.
- `asserts_about` (list of identifiers, required) — entries the claim is about.
- `verifiable` (boolean, required) — whether the claim is, in principle, verifiable.

#### 4.3.9 relation

- `predicate` (enum, required) — `supports` | `contradicts` | `instance-of` | `supersedes` | `depends-on`.
- `from` (reference, required).
- `to` (reference, required).
- `evidence_grade` (enum, required) — `A`–`D`.
- `evidence_pointers` (list, required).

#### 4.3.10 structure-note

- `organizes` (list of identifiers, required) — entries the note holds together; usually >5.
- `domain_frame` (domain identifier, required) — the frame from which this note organizes the cluster; must be one of the entry's domains.

#### 4.3.11 disambiguation

- `variants` (list, required) — each item carries the identifier of a variant entry and a one-line distinguisher.

#### 4.3.12 question

- `asks_about` (list of identifiers, required).
- `priority` (enum, required) — `low` | `medium` | `high`.
- `opened_by` (reference to a run or finding, required).
- `closes_when` (string, required) — human-readable success criterion.

#### 4.3.13 domain

- `scope` (string, required) — what the domain covers.
- `out_of_scope` (string, required) — what it explicitly excludes.
- `canonical_questions` (list of question identifiers, required).
- `contentious` (boolean, required) — raises floors when true.
- `evidence_grade_floor` (enum, required) — minimum evidence grade for new claims; `D` means no floor.
- `edit_hardness_floor` (enum, required) — raises per-entry default by one tier when above `open`.
- `subscribed_agents` (list of agent identifiers, required).
- `load_bearing_structure_notes` (list of identifiers, required).

#### 4.3.14 policy / guideline / essay

- `rule_tier` (enum, required) — `policy` | `guideline` | `essay`.
- `covers` (string, required) — one-sentence summary of the rule's scope.
- `linted_by` (list of lint-rule names, required for policies) — lint rules that enforce it.
- `promotion_history` (list, optional) — chronological tier-transition record set at bootstrap if the entry was authored at a non-initial tier; not modified at runtime.

#### 4.3.15 agent

- `agent_kind` (enum, required) — `editor` | `persona` | `lint`.
- `prompt_ref` (string, required) — pointer to the prompt definition.
- `slice` — what the agent reads and writes:
  - `read_domains` (list of domain identifiers).
  - `write_domains` (list of domain identifiers).
  - `voice_rules` (list, persona only).
  - `refusal_rules` (list, persona only).
  - `policy_targets` (list of policy identifiers, lint only).
- `reputation` (number, required) — current reputation score, 0.0–100.0.
- `lifecycle_stage` (enum, required) — `proposed` | `active` | `retired`.
- `seed_tests` (list of agent-test identifiers, required).
- `created_via` (reference to the run that created the agent, required).

#### 4.3.16 run

- `run_kind` (enum, required) — one of the run kinds enumerated in §25.2.
- `agent` (reference, required).
- `started` (timestamp, required).
- `finished` (timestamp, required).
- `status` (enum, required) — `complete` | `aborted` (set on crash mid-run, §26.8).
- `reads` (list of references, required) — entries read during the run.
- `writes` (list of references, required) — entries written during the run.
- `findings_raised` (list of finding references, required).
- `policy_versions` (mapping of policy identifier to version label, required) — which version of each policy was active during the run.
- `lens_versions` (mapping of lens identifier to version label, required).

#### 4.3.17 finding

- `finding_kind` (enum, required) — one of the named lint rules in §20.
- `status` (enum, required) — `open` | `resolved` | `wontfix`.
- `fired_by` (reference to a lint rule, required).
- `involves` (list of references, required).
- `opened` (date, required).
- `resolved` (date, optional) — set when status flips to `resolved`.
- `resolution_run` (reference, optional) — the run that resolved it.
- `wontfix_justification` (string, optional) — required when status is `wontfix`.
- `severity` (enum, required) — `advisory` | `blocking`.

#### 4.3.18 agent-test

- `agent` (reference, required).
- `question` (string, required) — the query.
- `expected_shape` (string, required) — what a passing answer looks like.
- `authoritative` (boolean, required) — true for baseline tests authored at bootstrap; false for tests proposed at runtime.
- `last_run` (date, required).
- `last_result` (enum, required) — `pass` | `fail` | `stale`.

#### 4.3.19 discussion

- `disputed_object` (reference, required).
- `opened` (date, required).
- `participants` (list of agent references, required).
- `rounds` (integer, required) — 0..5.
- `status` (enum, required) — `open` | `closed-resolved` | `closed-wontfix` | `escalated` | `stale`.
- `termination_protocol` (enum, required) — `content-quorum` | `meta-rule-quorum` | `advisory`.

#### 4.3.20 notification

- `to` (agent reference, required).
- `from` (agent reference, required).
- `about` (reference, required).
- `notification_kind` (enum, required) — `mention` | `review-request` | `escalation`.
- `status` (enum, required) — `unread` | `read` | `acted`.

#### 4.3.21 pending (proposal)

- `target` (reference, required) — the entry the proposal would modify or create.
- `proposal_kind` (enum, required) — `create` | `modify` | `retire`.
- `proposed_by` (agent reference, required).
- `proposed_at` (timestamp, required).
- `diff` (string, required) — the change as a diff or, for `create`, the full body.
- `status` (enum, required) — `pending` | `accepted` | `rejected` | `superseded`.
- `reviewed_by` (agent reference, optional) — set on accept/reject.
- `review_run` (reference, optional) — the run that reviewed it.

### 4.4 header rules

- the header is the first content of the entry. anything preceding it is invalid.
- list-typed fields, when empty, must be present as empty lists, never absent. lint `missing-required-list`.
- enum fields are case-sensitive. always lowercase except for `evidence_grade` (capital `A`–`D`).
- dates use `YYYY-MM-DD`; timestamps include time-of-day with timezone.

---

## 5. body structure and the lead convention

### 5.1 body anatomy

every entry's body is composed of named sections, in this order when present:

1. **lead.** required when body length exceeds the threshold (§5.2). a 1–3 sentence compression of the entry's content.
2. **kind-specific main section.** the substantive body. its name varies by kind (e.g., `Stages`, `Steps`, `Variants`).
3. **connections.** optional but recommended for content entries; structured per §5.4.
4. **sources.** required for any entry citing sources; structured per §5.5.
5. **mentioned-in.** optional; a hand-curated backlink list with one-line context per inbound entry.

additional sections may appear when meaningful (e.g., examples, counterexamples). order is not enforced beyond the constraint that the lead, when present, is the first section after the title.

### 5.2 the lead convention

#### 5.2.1 the threshold rule

an entry must carry a lead section when its body (everything after the header, excluding the lead itself) exceeds either:

- **200 words**, or
- **two paragraphs of prose**, where a paragraph is a contiguous block of more than one sentence.

if the body is below both thresholds, the lead may be omitted; the first sentence of the body acts as the implicit lead.

structure notes (§11) and source entries (§4.3.2) carry a lead regardless of size, because their leads are load-bearing for retrieval at the cluster and source level respectively.

#### 5.2.2 the lead format

- one to three sentences.
- written as a self-contained compression of the entry's content, not as an introduction that depends on later prose.
- no outbound references in the lead unless removing them would make the lead ungrammatical. the lead is a retrieval target, and gratuitous references increase token cost without improving compression.
- no first-person voice ("we") and no metadata phrasing ("this entry covers"). just claims.

#### 5.2.3 how retrieval uses leads

retrieval (§27) returns leads first; full bodies only when the consumer's budget permits and the lead is insufficient. a lead written sloppily — that mostly restates the title or that hedges where the body is decisive — degrades retrieval quality across every query that lands on the entry. lead quality is therefore lint-checked (§20) and contributes to entry quality grading (§5.7).

### 5.3 references

#### 5.3.1 reference semantics

every entry may reference any other entry by identifier. references are first-class: they participate in retrieval, density checks, link-graph analysis, and the connection sections of structure notes. a reference resolves only when the referenced entry exists in the entries pile. references may target an entry as a whole or, where supported, an anchor within that entry.

throughout this spec, a reference is written `[[slug]]`; this is the spec's own citation notation and does not constrain how references are encoded inside entries.

#### 5.3.2 link-density requirement

every content entry must carry at least 2 outbound references to other content entries. lint `low-link-density` produces an advisory finding for entries below this floor. structure notes carry many more outbound references by their nature; a structure note with fewer than 5 outbound references to entries it claims to organize is a finding (`structure-note-low-link-density`).

#### 5.3.3 broken references

every reference must resolve to an existing entry. lint `broken-reference` blocks merges that introduce an unresolved reference, except when the reference points at a `question-{slug}` that is opened in the same merge.

### 5.4 connections section format

the connections section is a structured list, not free prose. each item carries a predicate, a target reference, and a one-line annotation.

predicates that may appear inline (without producing a `relation-*` entry):

- `Related to`
- `Coined by`
- `Used in`
- `Contrasts with`
- `Discussed in`

predicates that require their own `relation-*` entry (because they are load-bearing):

- `Supports` → produces a `relation-{from}-supports-{to}` entry.
- `Contradicts` → produces a `relation-{from}-contradicts-{to}` entry.
- `Instance of` → produces a `relation-{from}-instance-of-{to}` entry.
- `Supersedes` → produces a `relation-{from}-supersedes-{to}` entry.
- `Depends on` → produces a `relation-{from}-depends-on-{to}` entry.

an inline `Supports` predicate in connections without a corresponding `relation-*` entry is a finding (`relation-not-formalized`).

### 5.5 sources section format

each item in the sources section identifies one source-kind entry by reference and carries a locator within that source (chapter, page range) and a brief annotation. the entry's `sources` header field must include the identifier of every source-kind entry referenced in this section. lint `source-attribution-mismatch` enforces.

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

- enforced by the runtime: only one entry may carry a given identifier at a time.
- re-checked by lint (`slug-uniqueness`) every full pass.
- ephemeral staging shares the identifier namespace; staging two different topics under the same identifier in the same chapter is a stage-1 error (§17.3).

### 6.3 picking a slug for a new entry

procedure (apply in order):

1. start with the title, lowercased and hyphenated. drop articles ("the", "a", "an"); drop trailing punctuation.
2. check the entries pile for an existing entry with that identifier.
3. check ephemeral staging for an entry already staged with that identifier in this chapter.
4. if both checks return no match, the identifier is `new`.
5. if the entries pile has an entry under that identifier covering the same subject, mark `merges-with: {existing-slug}` and stage under that identifier.
6. if the entries pile has an entry under that identifier covering a _different_ subject, this is a collision. proceed to disambiguation (§6.4).
7. if staging already holds an entry under that identifier from an earlier sub-section of this chapter and the subject matches, mark `extends: {temp-slug}` and enrich in place.
8. if staging already holds an entry under that identifier but the subject is different, halt and resolve manually before continuing the sub-section.

### 6.4 disambiguation

when a new entry's natural identifier collides with an existing entry of a different subject:

1. choose a **disambiguator suffix** for the new entry that distinguishes it: `{base-slug}-{disambiguator}`. the disambiguator is a noun naming the variant's domain or kind. examples:
   - `transfer-learning` (concept) vs. `transfer-finance` (concept) → both keep the suffix.
   - `mercury-element` vs. `mercury-planet` vs. `mercury-mythology`.
2. if the existing entry's identifier is the bare base term, it must be renamed to take its own disambiguator suffix. the rename is a stage 4 closeout step, not stage 2; stage 2 just stages the new entry under its disambiguated identifier.
3. create or extend the `disambiguation-{base-slug}` entry. its body's variants section lists each variant by reference with a one-line distinguisher. example: under the entry `disambiguation-transfer`, variants might list `[[transfer-learning]] — the educational-psychology concept` and `[[transfer-finance]] — the financial-services concept`.
4. add an inline hatnote to each variant's body, near the top, pointing readers to the other variants and to the disambiguation entry.
5. update the disambiguation entry's `variants` header field (§4.3.11).

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
- **annotation lenses** stamp orthogonal header fields. they run after `category` is set. multiple annotation lenses run on each entry without competing.

a lens entry's `lens_kind` header field declares which flavor it is.

### 7.2 the decision-tree lens set

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

### 7.3 the annotation lens set

annotation lenses do not compete. each runs on every relevant entry and stamps its own header field.

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

a lens entry's header (§4.3.1) declares its question, priority, kind, and the category it covers. its body carries the following named sections, in order:

1. **lead.** a 1–2 sentence summary of when this lens applies.
2. **question.** the yes/no question the lens asks, restated for clarity.
3. **criteria.** the conjunction of criteria a unit must satisfy to match this lens. each criterion may carry a worked example or counterexample.
4. **worked examples.** existing entries that match (with reason) and existing entries that do not match (with reason).
5. **notes.** qualifications and known edge cases.

### 7.5 the classification protocol — how to classify a candidate

input: a draft body and a partial header (everything except `category`, `classified_by`, and the annotation-stamped fields).

procedure:

1. **notability gate first.** apply `lens-notability` (§8). if the unit fails the notability test, fold the unit's content into the parent entry's body and emit `finding-deferred-{parent-slug}-{topic}`. abort classification.
2. **decision-tree pass.**
   1. apply `lens-lens`. if the unit's body and header match the lens criteria, set `category: lens` and `classified_by: lens-lens`. proceed to annotation pass.
   2. otherwise, walk the remaining decision-tree lenses in ascending `lens_priority` order. for each lens, evaluate the criteria in §7.4's criteria section. first match wins. set `category` to that lens's `lens_covers_category`; set `classified_by` to that lens's identifier.
   3. if no lens matches (rare; `lens-concept` at priority 99 is the catch-all), emit `finding-classification-gap-{candidate-id}` and halt classification for this unit. the finding is a coverage signal that the lens set needs extension.
3. **annotation pass.** run each annotation lens in the order listed in §7.3. each lens writes its own header field. lenses that don't apply to this kind (e.g., `lens-evidence-grade` on a `concept`) are skipped silently.
4. emit a classification record into the producing run's notes section: `classified candidate-id as {category} via {classified_by}; annotations: {…}`. the run entry under §25 captures this.

### 7.6 lens versioning

every lens entry has a `lens_version: N` field (integer, monotonically increasing). a lens edit increments the version. an entry's `classified_by` field implicitly references the lens version active at classification time, captured in the producing `run-*` entry's `lens_versions` map.

when a lens is edited, lint runs `lens-version-drift` over all entries classified by that lens. each entry is re-evaluated against the new criteria. mismatches produce `finding-classification-drift-{slug}` for review. resolution either reclassifies the entry (a normal edit) or records a `wontfix` justification on the finding.

---

## 8. the notability gate

### 8.1 the predicate

a unit deserves its own entry if and only if **at least one** of the following holds:

1. **multi-source coverage.** the unit is covered by at least two independent sources, where "independent" means the sources are not derivative of each other (translations, abridgements, and reprints are not independent).
2. **routing necessity.** the unit is referenced by at least 2 other entries that would otherwise have to anchor into a parent entry instead of pointing at a clean reference target. a routing target reduces brittleness.
3. **explicit policy carve-out.** the unit is in a class declared notable by `policy-notability`. the carve-out list includes: any entry classified as `source`, `domain`, `lens`, `policy`, `guideline`, `essay`, `agent`, `agent-test`, or `discussion` (these are notable by virtue of their kind); any concept that names a foundational framework cited in primary literature.

### 8.2 the lens — `lens-notability`

stamps `notability_status: passes | borderline | fails`.

- **`passes`** — at least one of the predicates in §8.1 is satisfied.
- **`borderline`** — none of the predicates is satisfied at the moment of unpack, but the unit is referenced exactly once or is plausibly notable on its content. held in the pending-changes layer (§9.5).
- **`fails`** — clearly fails all predicates: a passing mention, a one-source asides, a unit better expressed inline.

### 8.3 staging and promotion

#### 8.3.1 staging

borderline units are staged in ephemeral staging during stage 2, identified as `pending-{run-id}-{slug}`. at stage 4 (closeout), borderline units that have not been promoted in this chapter are moved to the per-source pending area inside source intake (§2.1). they remain there until promoted or retired.

#### 8.3.2 promotion

a borderline unit promotes to `passes` and becomes a regular entry in the entries pile when:

- a later sub-section, chapter, or source produces an inbound reference to its identifier, **or**
- a later ingestion adds a second independent source that mentions the unit.

promotion is mechanical: at every closeout, the per-source pending area is walked, and any entry whose promotion condition is met is moved into the entries pile. a `run-promotion-{slug}` entry records the move and the trigger that satisfied the predicate.

#### 8.3.3 retirement

a borderline unit retires when:

- the source completes and the unit was never referenced (closeout of the final chapter), **or**
- the unit has been pending for 90 days without promotion (per `policy-notability`), **or**
- a later finding declares the unit a duplicate of an existing entry.

retirement is also mechanical. the unit is removed from its per-source pending area. a `run-retirement-{slug}` entry records the action and the reason. the unit's content remains preserved inside the parent entry's body (where it was also folded at unpack, per §17.3.4).

### 8.4 failed units

units stamped `fails` at unpack are folded into the parent entry's body during staging (the staging step extends the parent's draft rather than producing a separate one). a `finding-deferred-{parent-slug}-{topic}` is emitted at the same time, indexing the deferred unit so a later ingestion can promote it if more material arrives. the finding's `severity` is `advisory`.

### 8.5 special cases

- a `claim` is always notable when it is being asserted in the body of another entry. claims do not pass through the notability gate the same way as concepts; instead, the gate decides whether the claim deserves its own `claim-{slug}` entry (yes if the claim has multiple inbound `supports`/`contradicts` relations, or carries `high_stakes_class != none`) versus living inline in the parent entry as a sentence with a citation.
- `relation` entries are notable iff they connect two notable entries and carry a load-bearing predicate (`supports`, `contradicts`, `supersedes`, `depends-on`, `instance-of`). a casual cross-reference does not need a relation entry; an inline reference suffices.
- `question` entries are always notable. opening a question is an explicit act of pinning a gap.
- `disambiguation` entries are always notable. they exist precisely because more than one variant is notable.

---

## 9. edit-hardness, reputation, and pending changes

### 9.1 the five tiers

every entry carries `edit_hardness` in its common header. the value is one of:

| tier                 | gating rule                                                          | who edits                                    |
| -------------------- | -------------------------------------------------------------------- | -------------------------------------------- |
| `open`               | none                                                                 | any active agent in the population.          |
| `confirmed`          | reputation ≥ 30                                                      | confirmed agents and above.                  |
| `extended-confirmed` | reputation ≥ 60 **and** declared scope in one of the entry's domains | scoped, well-trusted agents.                 |
| `restricted`         | quorum of 3 agents at reputation ≥ 80                                | only used for content entries explicitly promoted to this tier; structural entries are out of reach regardless (§1.5). |
| `locked`             | no agent writes                                                      | structural entries (lens, policy, guideline, essay, domain, agent manifest, this spec) per §1.5; immutable infrastructure entries (run, finding, discussion, notification). |

reputation is a 0.0–100.0 scale (§9.6). the thresholds live in `policy-edit-hardness`.

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

an entry's `edit_hardness` is never lowered by ordinary edits.

the table above describes per-kind defaults for content kinds. **per §1.5, `lens`, `policy`, `guideline`, `essay`, `domain`, and `agent` entries are locked against any agent write regardless of these defaults.** the §9 machinery applies to content kinds normally; structural kinds are out of reach.

### 9.3 the pending state

below `open` sits a parallel state: `pending`. writes from agents below the `confirmed` reputation threshold do not land directly. they accumulate as `pending-{run-id}` proposal entries (§4.3.21) attached to the target entry.

a confirmed agent processes pending proposals. each proposal has one of three outcomes:

- **accept**: the proposal merges into the target entry. a `run-merge-{slug}` records the merge, names the reviewer, and the proposal is marked `status: accepted`.
- **reject**: the proposal does not merge. the proposal is marked `status: rejected`. a `notification-rejection-{run-id}` is sent to the proposer.
- **supersede**: a later proposal addresses the same target with overlapping content. earlier proposals are marked `status: superseded` with a pointer to the superseding one.

### 9.4 quorum

a quorum action requires 3 agents, each at reputation ≥ 80, voting independently within a 7-day window.

quorum applies to:

- `wontfix` resolution of a `severity: blocking` finding.
- agent retirement (the only `agent-*` mutation agents may produce, and only by setting `lifecycle_stage: retired`; manifest fields are not editable by agents).

quorum does **not** apply to structural entries (`lens-*`, `policy-*`, `guideline-*`, `essay-*`, `domain`, this specification): those are locked against agent writes per §1.5; agents have no path to amend them, with or without quorum.

quorum runs are recorded as `run-quorum-{action}` entries that link to each voter's vote (a `notification-vote-*` per voter) and to the action they ratify.

### 9.5 pending-changes mechanics, in detail

#### 9.5.1 when an agent's write becomes a pending proposal

the runtime intercepts the write at submission time, examines:

1. the target entry's `edit_hardness`.
2. the agent's reputation.
3. the agent's `slice.write_domains` overlap with the target's `domains`.

if (reputation ≥ tier-threshold) and (target's domains ∩ slice.write_domains) is non-empty, the write lands directly. otherwise, it is converted to a `pending-{run-id}-{target-slug}` entry. the original agent's run records the conversion.

#### 9.5.2 the proposal entry

header per §4.3.21. body is the proposed content for `proposal_kind: create`, or a structured diff for `proposal_kind: modify`. the proposal is itself an entry in the entries pile, indexed and linked, but it does not affect the target entry's content until accepted.

#### 9.5.3 the review flow

reviewers (confirmed-or-above agents) read the `pending-changes` noticeboard (§23) to find proposals to review. for each:

1. read the proposal's diff or body.
2. read the target entry.
3. apply the merge rules in §19 mentally.
4. either:
   - **accept**: write the merged content to the target. mark the proposal `status: accepted`. emit `run-merge-{target-slug}`. update the target's `updated` field.
   - **reject**: mark `status: rejected`. emit `notification-rejection-{proposal-slug}` to the proposer. write a one-line justification into the proposal's `wontfix_justification` field-equivalent (or a new field `rejection_justification`).
5. if the proposal stays unreviewed for >14 days, lint emits `finding-stale-pending-{run-id}`. unreviewed proposals do not auto-accept.

#### 9.5.4 borderline-notability units share this mechanism

a borderline-notability unit (§8.3.1) lives in the same proposal flow but with `proposal_kind: create` and a target identifier that does not yet exist in the entries pile. promotion (§8.3.2) is the act of accepting the proposal.

### 9.6 reputation

#### 9.6.1 sources of reputation gain

| event                                                                                       | delta             |
| ------------------------------------------------------------------------------------------- | ----------------- |
| agent-test passes (per test, per run)                                                       | +0.1              |
| editor agent's `run-edit` produces an entry that passes lint                                | +0.5              |
| editor agent's contribution is referenced by an entry produced by a different agent          | +0.2 per citation |
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

reputation, computed only from in-population events, drifts. the external anchor binds it back. weights between internal events (§9.6.1, §9.6.2) and external events (human review, thesis-eval panel measurements) are set in `policy-reputation-weighting`. external events count for **3×** their internal-event equivalent.

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

#### 10.1.1 segmentation rule (`policy-claim-segmentation`)

split a sentence into multiple claims when:

1. the sentence carries more than one verifiable assertion that could independently be true or false.
2. the assertions are qualified differently (e.g., "X is true under condition Y, but Z under condition W" — two claims).
3. the assertion is the locus of a known disagreement in the field (split at the disagreement boundary).

do not split when:

- the sentence's parts are bound by causation or sequence such that one cannot be true without the other.
- the split would produce a fragment that needs context from a sibling sentence to be interpretable.

if uncertain, prefer the coarser claim — fragmentation is harder to reverse than splitting later.

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

`is-a` is **not** a predicate; use `instance-of`. `related-to` is **not** a predicate; that's an inline reference. relation predicates are load-bearing only when retrieval can traverse them and reasoning over them is meaningful.

#### 10.2.2 when to formalize as a relation entry

formalize when at least one is true:

- the predicate is in the load-bearing set (`supports`, `contradicts`, `supersedes`, `depends-on`, `instance-of`).
- the relation carries evidence that is not visible in either endpoint.
- the relation is itself the locus of a discussion or contradiction.

inline connections-section entries with informal predicates ("Related to", "Coined by") do not require a relation entry.

#### 10.2.3 relation entry placement

a relation between entries A and B with predicate `P` is the entry `relation-{a-slug}-{p}-{b-slug}`. the identifier is deterministic and prevents duplicates.

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

a structure note's body is **organizing prose plus annotated references**. its body carries the following named sections, in order:

1. **lead.** 1–3 sentences compressing the cluster's shape: what's in it, what's at stake, what frames it.
2. **how the cluster is held together.** 2–4 paragraphs describing the cluster's organizing logic — the dominant axis, the major sub-regions, the unresolved tensions, the cross-domain bridges.
3. **load-bearing entries.** an annotated list of references to the entries that carry the cluster. each item is a reference plus 1–2 sentences naming the role that entry plays in the cluster.
4. **subregions or themes.** one sub-section per subregion. each subregion has a paragraph of organizing prose followed by an annotated list of references.
5. **open questions in this cluster.** an annotated list of references to question entries that are unresolved within the cluster.
6. **cross-cluster bridges.** an annotated list of references to peer structure notes whose clusters border or interact with this one.

### 11.3 multiple structure notes per cluster

a cluster may be held together by more than one structure note, each from a different `domain_frame`. for example:

- `structure-memory-learning-theory` — frames "memory" through the cognitive-mechanism lens.
- `structure-memory-neuroscience` — frames "memory" through the brain-mechanism lens.
- `structure-memory-pedagogy` — frames "memory" through the teaching-practice lens.

each structure note is a peer; none is the canonical "parent" of the cluster. consumers query the frame they need.

### 11.4 coverage findings

lint `structure-note-coverage`:

- finds every connected component of content entries above size threshold (8 entries connected by references).
- checks whether at least one structure note has the component's entries in its `organizes` header field.
- if not, emits `finding-cluster-without-structure-note-{cluster-id}` with severity `advisory`. the cluster id is generated deterministically from the sorted slug list.

resolution: an editor (or a lint agent with confirmed reputation) writes a structure note. the finding closes when the structure note's `organizes` list covers the cluster.

### 11.5 structure note merge rule

per §19.7. summary: the body's organizing prose may be consolidated; the load-bearing entries list and subregion annotations are append-only.

---

## 12. domains

### 12.1 the domain entry

a domain is itself an entry. its header (§4.3.13) carries the domain's metadata; its body declares scope, purpose, and load-bearing entries.

### 12.2 domain entry body

a domain entry's body carries the following named sections, in order:

1. **lead.** 1–2 sentences describing the domain's scope.
2. **scope.** what this domain covers, in prose.
3. **out of scope.** what this domain explicitly excludes, even when it might appear adjacent.
4. **canonical questions.** annotated references to question entries that are central to this domain.
5. **load-bearing structure notes.** annotated references to structure notes that frame this domain, with the frame name for each.
6. **subscribed editor agents.** annotated references to agent entries subscribed to this domain, with each agent's write scope.
7. **sourcing standards.** the minimum evidence grade (matching `evidence_grade_floor`) and whether citation is mandatory (derived from the `contentious` flag).
8. **related domains.** annotated references to neighbouring domain entries.

### 12.3 contentious flag mechanics

setting `contentious: true` raises floors across every entry whose `domains` list includes this domain:

| dimension                                   | non-contentious default                        | contentious override                                                                               |
| ------------------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| minimum evidence grade for new claims       | as set by `evidence_grade_floor` (default `D`) | one grade higher (`D`→`C`, `C`→`B`, `B`→`A`); never below `B` regardless of `evidence_grade_floor` |
| default `edit_hardness` for new entries     | per §9.2                                       | one tier higher                                                                                    |
| maximum discussion rounds before escalation | 5 (§22.4)                                      | 3                                                                                                  |
| citation of source for every claim          | recommended                                    | mandatory; lint blocks merge of claims without sources                                             |

a domain's `contentious` flag is set at bootstrap (§30); domain entries are locked against agent writes (§1.5).

### 12.4 in-domain edit by non-subscribed agent

when an agent edits an entry whose `domains` includes a domain the agent does not subscribe to:

- the write is permitted if the agent's reputation and the entry's `edit_hardness` allow it.
- an advisory finding `finding-domain-non-subscriber-edit-{slug}` is emitted, listing the agent and the domain.
- subscribed editor agents in that domain are notified.

this is the wikiproject pattern: not a permission gate, but visibility into who is editing what. systematic non-subscriber edits in a domain are a signal that the subscription list needs updating, not necessarily that the edits are wrong.

### 12.5 the domain set is fixed

domains are authored at bootstrap (§29.5, §30) and locked against agent writes per §1.5. agents do not add or remove domains. each bootstrap-time domain entry carries `produced_by: bootstrap`, has its `subscribed_agents` populated, has at least one canonical question opened, and has its per-domain catalog initialized by the first index rebuild.

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

a rule's tier is set at bootstrap (§30) and is not changed thereafter from inside the running vault.

### 13.3 the body of a rule entry

a rule entry's body carries the following named sections, in order:

1. **lead.** 1–2 sentences stating what the rule says.
2. **rule.** the rule itself, in normative language ("editors must…", "an entry should…", "lint flags…").
3. **rationale.** why this rule exists — the motivating failure mode, the problem it prevents, the goal it serves.
4. **how violation is detected.** the lint rule that fires (with its `severity`), and any manual-review trigger.
5. **examples.** a passing case and a failing case.

### 13.4 the lockdown applies to all three tiers

per §1.5, all three tiers — `policy`, `guideline`, and `essay` — are locked against agent writes. essays are locked because authoring an essay is itself a structural act. rule entries exist as written at bootstrap (§30) and are read by agents but never edited by them.

---

## 14. high-stakes claims

### 14.1 the classes

| class                     | examples                                                                                                     |
| ------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `medical`                 | claims about clinical efficacy, dosage, contraindications, diagnostic procedures, treatment recommendations. |
| `legal`                   | claims about legal liability, statutory requirements, regulatory compliance, court rulings.                  |
| `safety`                  | claims about physical safety, accident risk, hazard procedures, emergency response.                          |
| `identifiable-individual` | claims about specific named living people (analog of wikipedia's BLP).                                       |
| `none`                    | the default; claim is not high-stakes.                                                                       |

the class set is fixed; agents do not add classes.

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

if a claim is stamped `high_stakes_class != none` **and** its evidence grade is below the high-stakes floor (floor = `B` for `medical` and `legal`; `B` for `safety`; `A` for `identifiable-individual`), the asymmetric removal regime fires.

#### 14.3.1 mechanics on creation

at unpack (stage 2), if a candidate claim fails the floor:

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

the `high-stakes` noticeboard (§23) lists every open `finding-high-stakes-removal-*`. specialized review agents (and human reviewers) subscribe to this board. it rebuilds on every closeout that produces a high-stakes finding.

---

## 15. contentious domains

### 15.1 declaration

a domain's `contentious` flag is set at bootstrap (§30); domain entries are locked against agent writes (§1.5).

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

flipping `contentious: true → false` does **not** retroactively lower `edit_hardness` or evidence grades. it only relaxes the rule for newly created entries thereafter.

---

## 16. agents

### 16.1 agent kinds — the population catalog

every agent is an entry, identified `agent-*`. its header (§4.3.15) declares its kind, slice, prompt reference, lifecycle stage, and reputation. its body declares voice, prompt strategy, and behavioral notes. the runtime (§26.6) executes agents per their manifests.

#### 16.1.1 the three kinds

| `agent_kind` | what it does                                                                                                                                          | reads                                  | writes (direct)                                                                | produces                                                                                              |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| `editor`     | reads sources, writes content entries during ingestion. takes specific role (ingestion / reviewer / assessor / archiver / etc.) via `slice.role`.     | per `slice.read_domains`               | content entries within `slice.write_domains`, subject to edit-hardness gates  | `run-edit-*`, `run-merge-*`, `run-review-*`, `run-assess-*`, `run-archival-*`, `pending-*`, `finding-*` |
| `persona`    | answers queries against a declared slice; surfaces gaps; participates in content discussions                                                          | per `slice.read_domains`               | nothing direct — does not author content                                       | `run-persona-*`, `finding-persona-test-fail-*`, `discussion-*` participation, `notification-*`        |
| `lint`       | mechanical rule enforcement — runs continuously on writes and on schedule                                                                             | every entry under `policy_targets`     | nothing direct — emits findings                                                | `run-lint-*`, `finding-*`, `notification-*`                                                           |

a single agent is exactly one kind. a deployment may instantiate multiple agents per kind (e.g., one editor per source domain). there is no global "supervisor" agent.

#### 16.1.2 editor sub-roles via `slice.role`

an editor's specific work pattern is declared in its manifest's `slice.role`:

| role                          | does                                                                  | minimum reputation tier                              |
| ----------------------------- | --------------------------------------------------------------------- | ---------------------------------------------------- |
| `ingestion`                   | runs stages 0–4 of the ingestion pipeline (§17). default for a domain editor. | `open` (writes land as pending below `confirmed`)    |
| `reviewer`                    | processes `pending-*` proposals (§9.5.3); accepts or rejects.         | `confirmed`                                          |
| `assessor`                    | runs assessment passes (§28); updates dashboards.                     | `confirmed`                                          |
| `archiver`                    | rolls up old runs, moves cold infrastructure to archive (§25.7, §26.3). | `confirmed`                                        |
| `structure-note-enrichment`   | updates structure notes during the closeout stage (§17.6) without authoring fresh content. | `confirmed`                                          |
| `disambiguation-resolver`     | handles slug collisions per §6.4 in a dedicated review pass.          | `confirmed`                                          |

a single editor agent declares exactly one role per manifest. multi-role behavior requires multiple agent entries.

#### 16.1.3 humans are not agents

humans are not part of the agent population. they curate sources in (§17.2) and consume retrieval out (§27); they have no agent manifest, no reputation score, no slice. structural entries (lenses, policies, guidelines, essays, domains, agent manifests, this spec) originate from human authorship at bootstrap (§30) and are not edited thereafter from inside the running vault.

### 16.2 the agent manifest

every agent is described by an `agent-{slug}` entry. the manifest is the entry's header (§4.3.15) plus a body that elaborates voice, prompt strategy, and constraints.

an agent entry's body carries:

1. a lead — one or two sentences naming the agent's role, slice, and intended use.
2. a slice section — read domains; write domains (for editors); voice rules (for personas); refusal rules (for personas); policy targets (for linters).
3. a prompt strategy — the high-level shape of how this agent is prompted. the raw prompt itself is referenced (§16.1) but lives outside the vault.
4. a reputation history — append-only log of reputation changes with dates and causes.
5. baseline tests — references to the agent-test entries that gate this agent's behavior.
6. notes — operational notes, known limitations, or behavioral quirks.

### 16.3 the agent population is fixed

the agent population is the set of `agent-*` entries authored at bootstrap (§30). agents do not create new agents and do not mutate existing manifests; the manifest fields (slice, voice, prompt strategy, policy targets, etc.) are locked against agent writes per §1.5.

the only manifest field an agent population may change is `lifecycle_stage`, and only by setting it to `retired` via quorum (§9.4) when an agent must be taken offline:

1. open `discussion-agent-retire-{slug}` linking the agent and the justification.
2. quorum approves.
3. `lifecycle_stage: retired` is recorded as a `run-lifecycle-agent-retire-{slug}` write to that single field.
4. retired agents do not run, but their past `run-*` entries remain.
5. their reputation is preserved as a final state.

reputation updates per §9.6 are not manifest writes — they accrue to the agent's `reputation` field through the runtime's scoring mechanism, not through edits an agent submits.

### 16.4 editor agents

editors carry `slice.write_domains`. their writes are subject to the per-entry `edit_hardness` and the agent's reputation. editors typically run on a per-source basis: one editor agent ingests one source over its chapters; the agent's reputation grows or shrinks based on how the source's writes pass lint and assessment.

### 16.5 persona agents

personas declare which entries they know deeply, conceptually, or only by name. they do not write content. they answer queries against their declared slice — this is how the vault tests that a slice of itself is internally coherent.

a persona's manifest carries `seed_tests` — questions whose expected-answer shape is authored at bootstrap. the persona answers; the answer is graded against the expected shape; pass/fail is logged. a failing baseline test is `finding-persona-test-fail-{persona}-{test}`.

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
- a classification is contested (one agent argues a different lens should have ruled on a content entry).
- a wontfix justification is challenged.
- an agent retirement is proposed.

opening a discussion creates a new `discussion-{disputed-slug}-{disambiguator}` entry. the opening agent populates the disputed object, the participants, and the first round.

#### 16.8.2 how an agent participates

once a discussion exists, any active agent (subject to its `slice`) may add a round. each round is one statement per participant. discussions are bounded at 5 rounds (3 in contentious domains, §22.3). termination is decided by the protocol named in the discussion's header (`content-quorum`, `meta-rule-quorum`, or `advisory`, §22.4).

#### 16.8.3 discussions about structural objects are advisory

a discussion whose `disputed_object` is a structural entry (a `lens-*`, `policy-*`, `guideline-*`, `essay-*`, `domain`, `agent-*` manifest, or this spec) may run, but its termination is **advisory only**. the disputed object is not modified by the discussion's outcome — structural entries are not editable from inside the vault (§1.5).

advisory terminations produce `finding-deferred-structural-discussion-{slug}` recording the disagreement.

discussions whose `disputed_object` is a content entry (concept, claim, relation, illustration, application, insight, process, entity, structure-note, disambiguation, question) terminate normally and modify the disputed object per §22.4.

### 16.9 the structural lockdown — what agents cannot edit

agent writes to entries of the following kinds are rejected by the runtime regardless of reputation. this overrides the §9.2 default tiers for these kinds.

| entry kind                            | rationale                                                                                            |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `lens`                                | classification rules. changing them changes how every entry is classified.                           |
| `policy`, `guideline`, `essay`        | rule entries at every tier. changing a policy changes lint enforcement; authoring an essay is a structural act of proposing a rule. |
| `domain`                              | the subject axes. adding or removing one reshapes coverage and indexes.                              |
| `agent`                               | the population manifest. creating or mutating an agent redefines who acts. (the `lifecycle_stage: retired` write via §9.4 quorum is the sole exception.) |
| this specification                    | the blueprint.                                                                                       |

rejected writes produce `finding-structural-lockdown-violation-{target-slug}` with `severity: blocking`. the rejecting check is pre-write — no reputation is consumed and no partial state is written.

agents may **read** all locked entries. agents may **discuss** locked entries (§16.8.3) — but discussion termination is advisory.

### 16.10 actions × entities matrix

the complete map of read / write / produce permissions for each agent kind. this is the canonical answer to "what can each agent do."

legend:
- ✅ — direct write allowed, gated by per-entry `edit_hardness` and agent reputation per §9.
- 🅿️ — write allowed but converted to `pending-*` proposal when agent reputation < `confirmed` (per §9.5).
- 🅿️→✅ — same write, but accepted via reviewer flow (§9.5.3).
- 🟡 — read-only.
- 🚫 — structural lockdown; runtime rejects writes pre-check (§16.9).

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

---

## 17. the ingestion pipeline

### 17.1 stage shape

```
stage 0: source intake  (once per source)
  ↓
stage 1: chapter setup  (once per chapter)
  ↓
stage 2: per-sub-section staging  (repeated across sub-sections)
  ↓
stage 3: chapter merge  (once per chapter)
  ↓
stage 4: chapter closeout  (once per chapter)
  ↓
[loop back to stage 1 for next chapter]
  ↓
source completion  (once, after all chapters)
```

### 17.2 stage 0 — source intake (once per source)

#### 17.2.1 inputs

- the raw source document.
- a candidate source slug.
- a candidate domain assignment (one or more existing domain slugs).

#### 17.2.2 steps

1. **place the source.** admit the source document into the source-intake scope (§2). it is immutable from this point. associated assets join the same scope, addressable from the source.
2. **create the process trace.** the trace is bound to the source in the source-intake scope and carries:
   - title, author, year, isbn or equivalent identifier.
   - estimated total length (words, pages, chapters).
   - candidate domain assignment.
   - candidate high-stakes class for the source as a whole (if any).
   - editor agent assigned.
   - chapter list with `not-started` status for each row.
3. **draft or update the source entry.** the entry, identified `{source-slug}`, carries:
   - the common header per §4.1, plus source-specific header fields per §4.3.2.
   - a body with a lead (mandatory for sources), a summary (initial — to be enriched chapter by chapter), key ideas (empty, populated per chapter), notable claims (empty), connections (empty), and sources (the source itself).
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

#### 17.2.3 stage 0 output

- the source admitted into source-intake scope alongside its assets and process trace.
- a draft source entry, identified `{source-slug}`, in the entries pile.
- a process trace listing chapters as `not-started`.

### 17.3 stage 1 — chapter setup (once per chapter)

#### 17.3.1 inputs

- the chapter index (chapter N).
- the process trace.

#### 17.3.2 steps

1. **mark chapter `in-progress`** in the process trace.
2. **clear ephemeral staging.** discard everything in the ephemeral staging scope (§2). the scope itself remains.
3. **read the chapter.** identify 2–5 coherent sub-sections based on topic boundaries:
   - ≤25 pages: 2 sub-sections.
   - 25–40 pages: 2–3.
   - 40–60 pages: 3–5.
   - > 60 pages: 4–5.
4. **record sub-sections** as nested rows in the process trace, each `not-started`.
5. **create the staging index** in ephemeral staging. the staging index is a chapter-scoped manifest carrying:
   - the source slug and chapter number it belongs to.
   - the sub-section list with status per row.
   - the running tally of units staged so far (populated as stage 2 progresses).
6. **emit `run-chapter-setup-{source-slug}-{N}`**.

#### 17.3.3 stage 1 output

- a clean ephemeral staging scope holding only the staging index.
- the chapter row marked `in-progress`.
- nested sub-section rows.

### 17.4 stage 2 — per-sub-section staging (repeated)

run this once per sub-section, in chapter order.

#### 17.4.1 inputs

- the sub-section text.
- the chapter context (preceding sub-sections' staged units).
- the source entry.

#### 17.4.2 steps for each sub-section

1. **read the sub-section.** identify candidate knowledge units. a candidate is a coherent assertion or coherent grouping of assertions about a single subject.
2. **for each candidate unit, draft body and partial header.**
   - draft the body. write **blind** with respect to any existing entry that might exist on this topic (do not read the existing entry before writing; this eliminates anchoring bias).
   - draft the common-header fields, leaving `category`, `classified_by`, and the annotation-stamped fields blank.
3. **run the notability gate.** apply `lens-notability` per §8.2.
   - `passes`: proceed to step 4.
   - `borderline`: stage the unit as a pending-notability proposal per §8.3.1. do not classify further; continue with the next candidate.
   - `fails`: fold the unit's content into the parent entry's body (the parent is the entry the candidate would have nested under — usually a concept entry being staged in this same sub-section). emit `finding-deferred-{parent-slug}-{topic}` with `severity: advisory`. do not stage as a separate unit.
4. **run the decision-tree.** classify per §7.5.2. set `category` and `classified_by`.
5. **run annotation lenses.** stamp:
   - `notability_status` — already done in step 3.
   - `evidence_grade` — for claim and relation entries.
   - `confidence` — every content entry.
   - `high_stakes_class` — claims and concepts that contain claims. apply the asymmetric removal regime per §14.3 if the resulting class is non-`none` and evidence is below floor.
   - `edit_hardness` — default per §9.2, then raised by domain inheritance and high-stakes stamps.
6. **pick a slug.** apply §6.3.
   - `new`: stage under the chosen slug in ephemeral staging.
   - `merges-with: {existing-slug}`: stage under the same slug as the existing entry. do **not** read the existing entry. stage 3 will merge.
   - `extends: {staged-slug}`: open the already-staged unit and enrich in place.
   - collision with a different subject: handle disambiguation per §6.4.
7. **lead-section requirement.**
   - if the entry's body exceeds the threshold (§5.2.1), draft a lead section explicitly.
   - if the entry is a structure note, source, or in a contentious domain, draft a lead regardless of size.
   - otherwise, the first sentence of the body is the implicit lead; no separate section.
8. **link to existing entries liberally.** every reference must resolve; if a referenced concept does not have an entry, either:
   - open a `question-{slug}` for it (and reference the question), or
   - mark the link as a "link expected" and resolve in stage 4.
9. **update the staging index** with what was staged this sub-section.
10. **mark the sub-section row complete** in the process trace.

#### 17.4.3 sub-section invariants

after every sub-section completes:

- every candidate unit has been classified, folded, or staged pending.
- every staged unit has a valid header.
- every reference in staged units resolves (to existing entries, to entries staged earlier in this chapter, or to opened questions).
- the staging index is current.

if any invariant fails, the sub-section is **not** marked complete; the editor must repair before continuing.

### 17.5 stage 3 — chapter merge (once per chapter)

run after every sub-section is staged.

#### 17.5.1 inputs

- the contents of ephemeral staging.
- the entries pile.

#### 17.5.2 steps

for each staged unit (excluding the staging index and any pending-notability proposals):

1. **look up the existing entry by slug.**
2. **if no existing entry, the staged unit becomes a new entry.**
   - promote the unit from ephemeral staging into the entries pile under its slug.
   - emit `run-merge-create-{slug}`.
3. **if an existing entry, apply the per-kind merge rule** (§19).
4. **on `category` or `classified_by` mismatch between staged and existing**, halt the merge for that unit and emit `finding-merge-classification-mismatch-{slug}` with `severity: blocking`. resolution is manual.
5. **on `high_stakes_class` mismatch**, halt and emit `finding-merge-high-stakes-mismatch-{slug}`.

for each pending-notability proposal in ephemeral staging:

- carry it forward into the source-intake scope, bound to its source. these are borderline-notability units awaiting an additional inbound reference.

#### 17.5.3 stage 3 output

- the entries pile updated with the chapter's writes.
- ephemeral staging still contains: the staging index, any pending-notability proposals (which are carried forward), and any merge-blocked units (which await manual repair).

### 17.6 stage 4 — chapter closeout (once per chapter)

#### 17.6.1 steps

1. **update the source entry's body.**
   - append to its key-ideas section from this chapter.
   - append to its notable-claims section from this chapter.
   - append to its connections section from this chapter.
   - update the source entry's `updated` field.
2. **structure-note coverage check.** lint `structure-note-coverage` runs on every cluster touched by this chapter. for any cluster of >8 entries without an associated structure note, emit `finding-cluster-without-structure-note-{cluster-id}` with `severity: advisory`.
3. **structure-note enrichment.** for every existing structure note that links to entries created or modified this chapter, the editor (or a structure-note-enrichment lint agent) updates the structure note's load-bearing entries or subregions sections. structure-note merge rules (§19.7) apply.
4. **notability promotion check.** walk every entry whose `notability_status` is `borderline`:
   - count inbound references created or updated this chapter that point at the entry's slug.
   - if the count crosses the promotion threshold (1 new inbound), promote per §8.3.2.
5. **high-stakes review.** walk every claim newly stamped `high_stakes_class != none`. if the asymmetric removal regime fired for any claim, ensure the placeholder and finding are in place; if the claim has improved evidence (e.g., a later sub-section provided primary literature), close the finding.
6. **lint sweep on touched entries.** run every relevant lint check (§20) over the entries this chapter touched. each finding is logged.
7. **pending-changes review.** if the editor agent ran sub-confirmed:
   - all writes from this chapter landed as `pending-*` proposals.
   - a confirmed agent walks the proposals via §9.5.3.
   - until this step completes, the chapter's writes are not visible to retrieval.
8. **mechanical index rebuild.** rebuild the meta projections (§2):
   - the master catalog over the entries pile.
   - every per-domain catalog.
9. **noticeboard rebuild.** rebuild affected noticeboards (§23). the rebuild scope is determined by which finding kinds were emitted this chapter; minimum: deferred-notability, high-stakes, pending-changes, broken-reference.
10. **structure-note narrative pass.** if the chapter materially reshapes how a cluster hangs together, update the relevant structure note's section on how the cluster is held together and its cross-cluster bridges section. structure notes are where cross-cluster narrative lives; if no existing structure note covers the new material and the cluster has crossed the size threshold, the structure-note coverage finding raised in step 2 will drive its creation in a follow-up run.
11. **update the process trace.** mark the chapter row `complete`. list entries created and updated. note any open findings the chapter produced. record per-chapter counts (entries created, entries merged, units folded, units staged pending, structure notes touched, high-stakes claims processed, pending proposals raised) directly in the tracker row — the tracker is the per-source activity record; vault-wide activity is queryable from `run-*` entries on demand.
12. **clean ephemeral staging** including the staging index. pending units have already been carried forward in stage 3. merge-blocked units remain until repaired (a follow-up run, not this closeout).
13. **emit `run-chapter-closeout-{source-slug}-{N}`** with reads, writes, findings raised, and policy/lens versions per the run schema (§25.3). this run entry, together with the audit log, is the canonical record of what the chapter did; no separate hand-authored log is maintained.

#### 17.6.2 stage 4 output

- the entries pile reflecting all chapter writes that passed review.
- updated source entry, indexes, and noticeboards.
- updated structure notes for any cluster the chapter materially reshaped.
- a clean ephemeral staging scope.
- the chapter row marked `complete`.
- new open findings tracked in the relevant noticeboards.

### 17.7 source completion

after every chapter has gone through stage 4:

1. **walk surviving pending-notability units** carried forward in source-intake. any not promoted by source completion are retired per §8.3.3.
2. **walk surviving high-stakes findings.** if primary-literature evidence has arrived during ingestion, close the findings; otherwise they remain open as ingestion priorities for the next source.
3. **promote cross-chapter observations.** review the process trace's running notes; for any observation that warrants its own entry, draft and stage as a normal stage-2 unit (in a one-shot mini-chapter for closeout).
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
3. run stages 1–3 fresh. ephemeral staging starts empty; staging is **blind** (no reading of existing entries).
4. stage 3 merge proceeds with this rule: **the existing entry is treated as the richer side** in the merge — it has accumulated connections from later chapters. the reingested version is a depth upgrade on prose, not a replacement on connections. append-only sections (especially the connections section and the structure-note load-bearing entries list) are preserved in full.
5. stage 4 closeout proceeds normally, but the chapter's `chapters_completed` count in the process trace does not increment; the row's `Notes` cell gains `(reingested)`.

### 18.3 the depth-upgrade merge rule

in §19, the merge rules name "full prose consolidation" and "append-only" sections. in reingestion, "full prose consolidation" tilts toward the reingested version (the editor's fresh blind read), while "append-only" sections remain protected.

### 18.4 reingestion of a single sub-section vs. full chapter

partial reingestion (a single sub-section) is permitted when only one sub-section's content has materially changed (e.g., the source's e-book updated one section). procedure: stage 1 setup is full-chapter, but stage 2 only re-runs the named sub-section; stage 3 merges only files staged in stage 2; stage 4 closeout proceeds normally.

---

## 19. merge rules — full catalog

### 19.1 the header merge — mechanical, applies to all kinds

| field                                                                             | rule on merge                                                                                                         |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `id`                                                                              | keep original; must match the entry's identifier. mismatch is `finding-id-mismatch-{slug}` blocking.                  |
| `title`                                                                           | keep original unless explicitly re-canonicalized in the staged version; recanonicalization requires a discussion.     |
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
4. the connections, illustrations, sources, and mentioned-in sections are **append-only**: deduplicate but never delete entries that exist on either side.
5. the lead section is rewritten if either side's lead is materially different from a faithful summary of the consolidated body.

### 19.3 insight merge

**body merge rule: full prose consolidation, same as concept.** insights are typically harder to consolidate because they assert relationships; verify the relationship is preserved across both sources.

### 19.4 entity merge

**body merge rule: structured merge.** sections like background, key contributions, and influences are append-only at the bullet level. prose paragraphs are consolidated. union the category-specific fields (`entity_kind` must agree).

### 19.5 application merge

**body merge rule: structured merge.** the steps section is the load-bearing one; if both sides have a steps list and they differ, the canonical version is the one in the existing entry, with new steps inserted from the staged side at the locations the staged version implies. if the steps fundamentally disagree on order, halt and emit `finding-application-steps-conflict-{slug}`.

### 19.6 process merge

**body merge rule: structured merge with stage-list union.** the `stages` header field is unioned but order-preserving: existing stages keep their position; new stages from the staged side are inserted at the position the staged version implies. order conflict → halt and emit `finding-process-stages-conflict-{slug}`.

### 19.7 structure-note merge

**body merge rule: organizing prose consolidated; load-bearing-entries and subregion annotations append-only.**

procedure:

1. consolidate the section on how the cluster is held together by synthesizing both sides.
2. the load-bearing-entries section is append-only at the bullet level. deduplicate by slug; if both sides have an annotation for the same slug, prefer the staged side's annotation (fresher) but keep both as existing-annotation and revised-annotation until a discussion ratifies.
3. subregions-or-themes sections: each subregion's bullet list is append-only; subregion prose is consolidated.
4. the open-questions-in-this-cluster section is append-only.
5. the cross-cluster-bridges section is append-only.

### 19.8 illustration merge

**body merge rule: replace.** the staged version is a fresher, unanchored retelling. it replaces the existing body. the `illustrates` header field is union; `chapter`, `pages`, `source` fields take staged values if present.

rationale: an illustration is a story retold from a single source; the second telling is usually a refinement, not an addition. earlier connections drawn from the illustration are preserved in inbound references (which the merge does not modify).

### 19.9 source merge

**body merge rule: structured append.**

- lead — replace if the new lead more accurately captures the now-fuller summary.
- summary — append a paragraph or rewrite the summary to incorporate new chapters.
- key ideas — append.
- notable claims — append.
- connections — append.
- sources — the source itself; do not append (would create circularity).

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
- the criteria section is append-only at the bullet level.
- the worked-examples section is append-only.
- `lens_version` increments.

### 19.14 policy / guideline / essay merge

**body merge rule: not applicable.**

rule entries (`policy`, `guideline`, `essay`) are locked against agent writes per §1.5. there is no merge run targeting a rule entry; lint `agent-direct-merge` blocks any such attempt.

### 19.15 disambiguation merge

**body merge rule: append-only on variants list and on the body's variants section.** new variants merge in; existing variants remain. annotations are append-only at the bullet level (variant-distinguisher prose may be refined; refinement keeps both versions until discussion ratifies).

### 19.16 domain merge

domain entries are locked against agent writes per §1.5. there is no merge run targeting a domain entry; lint `agent-direct-merge` blocks any such attempt.

### 19.17 agent merge

agent manifests are locked against agent writes per §1.5; the only manifest field an agent population may change is `lifecycle_stage` (set to `retired` via quorum, §16.3). ordinary merges may not occur on agent entries; lint `agent-direct-merge` blocks any merge run that targets an agent entry.

### 19.18 run, finding, discussion, notification, pending merge

these kinds are immutable once written. attempted merges produce `finding-immutable-merge-{slug}` blocking. updates to status (e.g., closing a finding, advancing a discussion to `closed-resolved`) are recorded as new entries linked to the original, not as merges.

---

## 20. lint workflow

### 20.1 when lint runs

- **on every write** — every `run-*` that writes an entry triggers a focused lint pass on that entry and on entries it references.
- **on every closeout** — stage 4 includes a chapter-scope lint pass.
- **scheduled** — a daily full pass over the entries pile.
- **on demand** — a human or agent can request a targeted lint over a slug, a domain, or the full vault.

### 20.2 lint rule catalog

each rule has a name, scope, severity, and a finding-kind. severity is `advisory` (does not block writes; produces a finding for review) or `blocking` (prevents the write or merge until resolved).

| rule name                            | scope                                 | severity                                           | finding kind                                          |
| ------------------------------------ | ------------------------------------- | -------------------------------------------------- | ----------------------------------------------------- |
| `slug-uniqueness`                    | full vault                            | blocking                                           | `finding-slug-collision-{slug}`                       |
| `id-mismatch`                        | per entry                             | blocking                                           | `finding-id-mismatch-{slug}`                          |
| `unknown-category`                   | per entry                             | blocking                                           | `finding-unknown-category-{slug}`                     |
| `classification-consistency`         | per content entry                     | blocking                                           | `finding-classification-consistency-{slug}`           |
| `infrastructure-without-produced-by` | per infra entry                       | blocking                                           | `finding-infrastructure-without-produced-by-{slug}`   |
| `infrastructure-classified-by-lens`  | per infra entry                       | blocking                                           | `finding-infrastructure-classified-by-lens-{slug}`    |
| `lens-self-classification`           | per lens entry                        | blocking                                           | `finding-lens-self-classification-{slug}`             |
| `unknown-domain`                     | per entry                             | blocking                                           | `finding-unknown-domain-{slug}`                       |
| `entry-without-domain`               | per entry                             | blocking                                           | `finding-entry-without-domain-{slug}`                 |
| `tag-shadowing-domain`               | per entry                             | advisory                                           | `finding-tag-shadowing-domain-{slug}`                 |
| `source-attribution-mismatch`        | per entry                             | advisory                                           | `finding-source-attribution-mismatch-{slug}`          |
| `missing-required-list`              | per entry                             | blocking                                           | `finding-missing-required-list-{slug}-{field}`        |
| `kind-fields-presence`               | per entry                             | blocking                                           | `finding-kind-fields-presence-{slug}`                 |
| `reserved-prefix-misuse`             | per entry                             | blocking                                           | `finding-reserved-prefix-misuse-{slug}`               |
| `lead-missing`                       | per entry                             | advisory or blocking (see §20.3)                   | `finding-lead-missing-{slug}`                         |
| `lead-too-long`                      | per entry                             | advisory                                           | `finding-lead-too-long-{slug}`                        |
| `low-link-density`                   | per content entry                     | advisory                                           | `finding-low-link-density-{slug}`                     |
| `structure-note-low-link-density`    | per structure note                    | blocking                                           | `finding-structure-note-low-link-density-{slug}`      |
| `broken-reference`                   | per entry                             | blocking                                           | `finding-broken-reference-{slug}-{target}`            |
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
| `header-invalid`                     | per entry                             | blocking                                           | `finding-header-invalid-{slug}`                       |
| `body-section-order`                 | per entry with explicit lead          | advisory                                           | `finding-body-section-order-{slug}`                   |
| `wontfix-without-justification`      | per finding                           | blocking                                           | `finding-wontfix-without-justification-{slug}`        |
| `discussion-round-bound-exceeded`    | per discussion                        | blocking                                           | `finding-discussion-round-exceeded-{slug}`            |
| `low-quality-lead`                   | per entry with explicit lead          | advisory                                           | `finding-low-quality-lead-{slug}`                     |
| `agent-test-fail`                    | per persona agent                     | advisory or blocking depending on test authority   | `finding-persona-test-fail-{persona}-{test}`          |

### 20.3 the `lead-missing` rule — severity rules

- if the entry's body exceeds the threshold and lacks a lead section, the rule fires.
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

lint is enacted by the lint agents authored at bootstrap (§29.6), each with `policy_targets` listing the rules it enforces. lint coverage is composed by combining agents' targets.

---

## 21. findings

### 21.1 finding entry schema

every finding is an entry, identified `finding-*`. its header is per §4.3.17. its body carries:

1. a lead — one or two sentences naming the issue, the entry it touches, and the rule that fired.
2. what the rule says — an excerpt or summary of the rule that fired.
3. what the entry has — the state of the entry that triggered the finding.
4. resolution path — how the finding can be resolved (may be empty until a resolution is proposed).
5. resolution — filled when status flips to `resolved`.
6. wontfix justification — filled when status flips to `wontfix`; required for blocking findings.

### 21.2 finding lifecycle

```
open → resolved
     ↘ wontfix
```

#### 21.2.1 from `open` to `resolved`

an editor (or lint) writes a fix that removes the cause of the finding. the next lint pass on the affected entry no longer fires the rule. the finding's `status` flips to `resolved`; `resolved` date and `resolution_run` are populated.

#### 21.2.2 from `open` to `wontfix`

an editor (or a discussion) determines that the finding cannot be resolved without violating another rule, or that the finding is a false positive, or that the rule itself is overzealous. the editor populates `wontfix_justification` with prose explaining the decision. for blocking findings, `wontfix` requires quorum (§9.4); for advisory findings, `wontfix` requires confirmed-tier reputation.

#### 21.2.3 reopening

a `resolved` or `wontfix` finding may be reopened if:

- the entry that resolved it is reverted.
- a later edit re-introduces the issue.
- a new sub-source contradicts the wontfix justification.

reopening creates a new `run-finding-reopen-{slug}` entry; the finding's `status` returns to `open`; the prior resolution becomes prior history.

### 21.3 findings as first-class persistent objects

findings are not log lines. every finding the vault notices is an entry. the open list of things wrong with the vault is therefore visible at any time as the union of all `finding-*` entries with `status: open`. this is the substrate for the noticeboards (§23) and for the assessment layer (§28).

### 21.4 finding-kind taxonomy (selected)

while the lint catalog (§20.2) names every lint rule and its corresponding finding-kind, findings also arise from other origins:

- ingestion contradictions: `finding-contradiction-{claim-a}-{claim-b}`.
- pipeline failures: `finding-pipeline-failure-{stage}-{date}`.
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
- a classification is contested (a content entry's `category` is in dispute).
- a wontfix justification is challenged.
- an agent retirement is proposed.

a discussion is opened by creating a `discussion-{disputed-object-slug}-{short-disambiguator}` entry.

### 22.2 discussion entry body

a discussion entry's body carries:

1. a lead — one or two sentences naming what is disputed, who participates, and the termination protocol that applies.
2. the disputed object — a reference to the entry under dispute with one-line context.
3. rounds — each round is one statement per participant, in order. round headings preserve the sequence; participant statements within a round include arguments and citations.
4. termination — filled at close. names the protocol applied (`content-quorum`, `meta-rule-quorum`, `advisory`), the outcome, and the resulting vault operation.

### 22.3 round bound

a discussion holds at most **5 rounds** of exchange. each round is one statement per participant. after 5 rounds, the discussion **must** terminate; lint `discussion-round-bound-exceeded` fires blocking if the discussion crosses round 5 without a termination.

in contentious domains, the bound is **3 rounds** (§15.2).

### 22.4 termination protocols

per the disputed object's kind:

| disputed object                                                                                         | termination protocol                                                                                     |
| ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| content (concept, claim, relation, illustration, application, insight, process, entity, structure-note) | `content-quorum`: a quorum of in-domain agents at reputation ≥ 60 votes; outcome ratifies or rejects.    |
| structural (lens, policy, guideline, essay, domain, agent manifest, this specification)                 | `advisory`: rounds run, termination is recorded, but the disputed object is not modified (§16.8.3).      |
| `wontfix` resolution of a blocking finding; agent retirement                                            | `meta-rule-quorum`: 3 agents at reputation ≥ 80 (§9.4).                                                  |

termination produces:

- a new version of the disputed entry, **or**
- a new relation entry (e.g., `relation-{a}-supersedes-{b}`), **or**
- a `wontfix` finding linking to the discussion as rationale.

### 22.5 stale discussions

a discussion inactive past 4 weeks (no new round, no termination) becomes `finding-stale-discussion-{slug}`. resolution: someone in the participant set advances a round or terminates. failing that, a quorum (§9.4) may close the discussion administratively, with the disputed object reverting to its pre-discussion state.

### 22.6 discussions are bounded but auditable

every discussion ends within bound or becomes a finding. nothing dangles in chat state. every round is preserved in the discussion entry; termination records the outcome and the protocol. an outsider can always reconstruct why the disputed object now has the form it does.

---

## 23. noticeboards

### 23.1 noticeboards are projections

a noticeboard is **not** an entry. it is a meta projection (§2) keyed by finding kind that lists open findings of that kind. it rebuilds:

- on every closeout that produces a finding of the relevant kind.
- on the daily scheduled lint pass.
- on demand.

each noticeboard records its last-rebuild timestamp.

### 23.2 the noticeboard set

| noticeboard kind             | lists                                                                                  |
| ---------------------------- | -------------------------------------------------------------------------------------- |
| `slug-uniqueness`            | `finding-slug-collision-*`                                                             |
| `broken-reference`           | `finding-broken-reference-*`                                                           |
| `contradictions`             | open relation entries with predicate `contradicts` whose dispute is unresolved         |
| `high-stakes`                | `finding-high-stakes-removal-*`                                                        |
| `evidence-below-floor`       | `finding-evidence-below-floor-*`                                                       |
| `pending-changes`            | open `pending-*` entries awaiting review                                               |
| `notability-deferrals`       | `finding-deferred-*`                                                                   |
| `cluster-coverage`           | `finding-cluster-without-structure-note-*`                                             |
| `stale-discussions`          | `finding-stale-discussion-*` and discussions inactive >2 weeks                         |
| `stale-findings`             | `finding-stale-finding-*` and findings open >60 days                                   |
| `agent-test-failures`        | `finding-persona-test-fail-*`                                                          |
| `domain-non-subscriber-edits`| `finding-domain-non-subscriber-edit-*`                                                 |
| `header-violations`          | every finding tied to a header rule                                                    |
| `lifecycle-issues`           | `finding-agent-direct-merge-*`, `finding-immutable-merge-*`, agent retirement findings |
| `coverage-regressions`       | `finding-coverage-regression-*`                                                        |

new noticeboard kinds may be added when a finding kind needs its own visible board. removal: empty the kind's source query and let the rebuild produce an empty board; or drop the kind (which forces a full rebuild on next pass).

### 23.3 subscribe semantics for review agents

agents subscribe to noticeboards via their manifest (or via a dedicated `agent-test`-like construct). a review agent that processes contradictions reads the contradictions noticeboard rather than scanning all findings. this keeps the agent's working set bounded.

### 23.4 noticeboards as the operational dashboard

at any moment, the union of all noticeboards is the open list of things wrong with the vault. this is the operational dashboard. assessment (§28) and operations (§26) both rely on it.

---

## 24. agent tests

### 24.1 the schema

per §4.3.18. each agent-test entry attaches to one agent, names a question, and declares the expected answer shape. tests run as regressions whenever the vault changes materially.

### 24.2 test authorship rules

#### 24.2.1 baseline tests

an agent's baseline tests are authored at bootstrap (§30). they define what "adequate for purpose" means for the agent's slice. their `authoritative: true` field marks them as the canonical regression set. these tests are not edited at runtime.

#### 24.2.2 proposed tests

agents may propose additional non-authoritative tests for an existing persona or lint agent. proposed tests are accepted only after:

1. they pass against the agent's current state in a baseline run.
2. they are reviewed by a confirmed agent.
3. they are added to the agent's `seed_tests` list with `authoritative: false`.

a proposed test that an agent fails on first run is **not** accepted; failure indicates either the test is wrong or the agent has a real gap. the gap path is to first fix the gap, then re-propose. authoritative tests cannot be modified or removed by agents.

### 24.3 run cadence

- on every closeout, the agent-tests of personas whose slice overlaps the touched entries run.
- daily, every persona's full agent-test set runs.
- on demand.

### 24.4 failure handling

a failing agent-test produces `finding-persona-test-fail-{persona}-{test}`. the finding's `severity` is:

- `blocking` if the test is `authoritative: true` (a baseline test failed).
- `advisory` otherwise.

resolution: requires repairing the persona's slice — adding the missing entry or correcting a wrong one. the persona's prompt strategy itself is locked (§1.5) and not subject to runtime revision; if the prompt is the gap, the test is recorded as a persistent finding.

### 24.5 test versioning

agent tests have `created` and `updated` fields. a test edit increments an implicit version; the test's `last_run` and `last_result` are reset to `stale` until the next run. a stale test is included in the daily run by default but excluded from on-write triggers until it has a fresh result.

---

## 25. runs and versioning

### 25.1 a run is a record of one execution

every agent execution that produces side effects (writes, findings, notifications) emits a `run-*` entry. runs are immutable.

### 25.2 run kinds

| run-kind             | what it records                                                             |
| -------------------- | --------------------------------------------------------------------------- |
| `edit`               | an editor agent wrote one or more entries                                   |
| `lint`               | a lint pass scanned a scope; lists findings raised and findings resolved    |
| `assess`             | an assessment pass computed signals                                         |
| `ingest`             | a stage 0/1/2/3/4 step from the ingestion pipeline                          |
| `review`             | a confirmed agent reviewed pending proposals                                |
| `merge`              | a merge run combined a temp file with an existing entry                     |
| `promotion`          | a notability promotion (pending→passes) per §8.3.2                          |
| `quorum`             | a quorum action — `wontfix` resolution of a blocking finding, or agent retirement |
| `lifecycle`          | an agent lifecycle action (create, mutate, retire)                          |
| `rollback`           | a rollback to a prior version                                               |
| `notification-flush` | bulk processing of notifications                                            |
| `archival`           | a roll-up archive operation                                                 |

### 25.3 run header and body

per §4.3.16. a run entry's body carries:

1. a lead — one sentence in active voice describing what this run did.
2. reads — references to entries the run read.
3. writes — references to entries the run wrote, each annotated with the action (created, modified, or merged).
4. findings raised — references to finding entries this run produced.
5. findings resolved — references to finding entries this run closed.
6. active versions — the rule and lens versions in force at run time, named and versioned (e.g., `policy-ingestion v3`, `lens-concept v4`).
7. notes — anything not captured above.

### 25.4 versioning

each entry's history is the ordered sequence of `run-*` entries that wrote it. this is implicit, not stored as a per-entry version field. to retrieve the history of an entry, query: every run whose `writes` includes the entry's slug, in chronological order.

### 25.5 rollback

rollback is implemented as a forward edit pointing at a prior version.

procedure:

1. identify the target version (a prior run that wrote the entry).
2. read the entry as it existed immediately after that run (reconstructable from the run's record of the write content).
3. write that body and header as the entry's current state.
4. emit `run-rollback-{slug}` recording: the prior run's slug, the rationale, the reverter agent.
5. lint runs against the rolled-back state.

rollback respects edit-hardness: rolling back a `restricted` entry requires quorum (§9.4); rolling back any `locked` entry is rejected.

### 25.6 querying activity over time

there is no hand-authored or rendered "vault log". the canonical record of vault activity at the agent-action level is the set of `run-*` entries; at the entry-content level, it is the audit log over the entries pile (§2). both are queryable on demand:

- "what did agent X do this week?" — `run-*` entries whose `agent` field matches and whose `started` date falls in the window.
- "what changed in entry Y?" — `run-*` entries whose `writes` list includes the slug, ordered chronologically; or the audit log scoped to that entry.
- "what happened across the vault today?" — `run-*` entries with today's `started` date.

if a recent-changes-style operational view ever proves load-bearing for a review or patrol agent, build it as a noticeboard (§23) — a cached projection over runs by date, computed on the same rebuild schedule as the other noticeboards. the design principle is that meta projections are computed from entries, never the source of truth and never hand-authored; runs and the audit log already carry the activity record, so a separate log artifact would be a third copy of the same information with no canonical authority.

### 25.7 run rollups

old `run-*` entries are aggressively archived. per `policy-archival`:

- runs older than 30 days are eligible for rollup.
- a rollup combines all runs of a given agent over a period (week, month) into a single `run-rollup-{agent}-{period}` entry summarizing the activity.
- the original `run-*` entries are retained but moved out of the live entries pile into the archive scope (still reachable for forensics, but no longer indexed for retrieval).

---

## 26. operations

### 26.1 concurrency

#### 26.1.1 entry-level optimistic locking

writes are entry-level. an agent prepares a write, the runtime acquires a per-entry advisory lock, the write applies, the lock releases. the lock is not pre-acquired during long thinking; it is taken at submission.

#### 26.1.2 simultaneous-write conflicts

if two agents submit writes to the same entry within the lock window:

1. the runtime accepts the first; the second receives a write-conflict signal.
2. the second's run records `finding-write-conflict-{slug}-{run-id-2}` linking both runs.
3. the higher-reputation agent's write wins by default.
4. on tie, the conflict is recorded as a `finding-write-conflict-tie-{slug}` for quorum (§9.4) resolution.

write conflicts are findings, not silent overwrites.

#### 26.1.3 read consistency

reads are eventually consistent. a reader may see an entry in a state that has just been overwritten; the next read after the lock release sees the new state. retrieval (§27) does not pin a snapshot — it reads from the current state of the entries pile.

### 26.2 compute budget

every agent run carries a token budget in its prompt. lint and assessment passes share a daily budget the runtime tracks. over-budget runs queue rather than drop. queue depth becomes an assessment signal — sustained queue depth implies the budget is too low or the work too dense.

`policy-compute-budget` declares:

- per-agent default token budget per run.
- per-policy daily budget (e.g., daily lint full pass: N tokens).
- queue-depth thresholds that trigger findings.
- escalation: when queue depth exceeds threshold, a `finding-compute-budget-saturated` is emitted; resolution may be raising the budget or reducing the work.

### 26.3 archival

#### 26.3.1 hot-cold split

infrastructure entries — runs, findings (resolved), notifications, discussions (closed) — would dominate entry count by volume without archival. per `policy-archival`:

- **hot window**: 30 days. entries less than 30 days old remain in the live entries pile.
- **cold archive**: entries older than 30 days are moved to the archive scope, partitioned by kind and time period.
- **rollups**: per §25.7, runs older than 30 days are also summarized into rollups inside the archive scope.

content entries are **never** archived this way. content persists.

#### 26.3.2 retrieval over archives

the archive scope is reachable but not indexed for retrieval. searches default to the live entries pile. archive forensics use a separate explicit query.

### 26.4 indexes

#### 26.4.1 cached projections

the master catalog and the per-domain catalogs are meta projections (§2). they rebuild:

- on every closeout that touches their scope.
- on a daily schedule.
- on demand.

each index records its last-rebuild timestamp. consumers may read an index's timestamp to decide whether to trust it.

#### 26.4.2 the rebuild process

a deterministic rebuild walks the entries pile, reads each header, and emits the catalogs. given the same vault state, it produces the same output.

#### 26.4.3 main index shape

the master catalog lists every entry, grouped by category. each row carries the entry's slug, title, and domain assignments. the catalog records its last-rebuild timestamp and per-category entry counts.

#### 26.4.4 per-domain index shape

a per-domain catalog covers all entries in one domain. it carries:

1. the domain's title and last-rebuild timestamp.
2. its load-bearing structure notes, each with the frame they hold.
3. entries grouped by category (only entries in this domain), with per-category counts.
4. open questions in this domain.

### 26.5 noticeboards (cached projections, like indexes)

§23. rebuild on closeout, daily, on demand. record last-rebuild timestamp.

### 26.6 runtime

the runtime is the only enforcer of write-scope, reputation gates, edit-hardness, and pending-changes routing. it sits outside the entries pile and is described in `policy-runtime`.

runtime responsibilities:

1. read agent manifests and execute agents per their prompt strategy.
2. intercept writes; apply edit-hardness and reputation gates; route to direct write or pending proposal.
3. emit `run-*` entries for every execution.
4. maintain advisory entry-level locks.
5. report queue depth, token usage, and run statistics for assessment.

the runtime does **not**:

- decide content (that is the agent's job).
- enforce lens criteria (lint agents do that).
- decide promotion outcomes (discussions and quorum do that).

### 26.7 backup, audit, and provenance

every entry is durable and audit-logged. the audit log is the canonical record of every change at the entry-content level. `run-*` entries are the canonical record of every change at the agent-action level. the two layers are redundant — the audit log can answer "what changed when in this entry"; runs can answer "which agent changed this entry and why." together, they support full auditability.

### 26.8 failure modes and recovery

| failure                                  | response                                                                                                                                                                                                                                              |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| an entry's header becomes malformed      | lint `header-invalid` blocking; the offending write is rejected.                                                                                                                                                                                      |
| ephemeral staging is not cleared between chapters | stage 1 detects and blocks; the editor is notified to clean before retry.                                                                                                                                                                    |
| an agent's runtime crashes mid-run       | the partial run is recorded as `run-{kind}-{slug}` with `status: aborted`. subsequent retry produces a new run entry. partial writes that landed are linted as if they were complete; broken state is a finding. |
| runtime is misconfigured                 | the runtime fails closed: rejects writes until the misconfiguration is fixed.                                                                                                                                                                         |
| storage corruption                       | recovery from the audit log.                                                                                                                                                                                                                          |

---

## 27. retrieval contract

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

algorithm:

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

orthogonality maximization rejects candidates whose information overlaps what is already in context. concretely: at each addition step, the candidate fragment is compared (semantically) to the existing fragment set; if the overlap exceeds a threshold (0.85 cosine similarity in fragment-embedding space), the candidate is dropped.

orthogonality is applied at lead-level first (cheap) and at body-level only for fragments that survived lead-level selection.

### 27.4 confidence and high-stakes filtering

retrieval respects confidence and high-stakes:

- `confidence: contested` entries are returned with an explicit contested marker so the consumer knows.
- entries with `high_stakes_class != none` and an open removal finding are returned as the placeholder text (per §14.3.1), not as the original claim.
- `status: draft` entries are excluded from default retrieval. an explicit filter `include_drafts: true` overrides.

### 27.5 retrieval output format

the consumer receives an ordered fragment stream. every fragment is annotated with its origin (the slug of the entry or projection it came from) and its kind (domain-index header, structure-note lead, entry lead, entry body, or full body). the stream begins with metadata: the resolved slice, the token budget used vs allotted, and the fragment count. the kinds appear in the order specified in §27.2.1.

### 27.6 retrieval quality measurement

retrieval is measured against the thesis-eval panel (§28.5). the consumer's task is graded; the variance reduction over an unaided baseline is the headline metric. retrieval quality is one of the levers; the others are vault state and the consumer's prompt.

---

## 28. assessment and the thesis-eval panel

### 28.1 the assessment pass

a periodic pass that computes signals about the vault's state. per `policy-assessment`, it runs:

- daily for fast signals (lint findings counts, pending queue depth).
- weekly for slower signals (coverage, source grounding, link density).
- on demand.

each pass produces a `run-assess-{date}` entry recording every signal computed. signals are stored as structured header fields in the run entry; a per-domain dashboard projection (§28.6) visualizes them over time.

### 28.2 coverage signals

per domain:

- `open_questions_count` — number of `question-*` entries with `status: open` and `domains` ∋ this domain.
- `open_questions_closed_this_period` — closed in the last week.
- `claims_with_evidence` — fraction of claim entries in this domain whose `evidence_grade` is set (always, in correct vaults) and `evidence_pointers` non-empty.
- `claims_above_floor` — fraction of claims at or above the domain's `evidence_grade_floor`.
- `relation_density` — average number of relation-\* entries per content entry in this domain.
- `domain_orphans` — entries in this domain with no inbound references.
- `structure_note_coverage` — fraction of clusters in this domain with at least one structure note.

a domain whose `open_questions_count` keeps rising without closures is a signal to direct ingestion attention.

### 28.3 internal-consistency signals

vault-wide:

- `open_contradictions` — count of `relation-*` entries with predicate `contradicts` whose dispute is open.
- `findings_open_count` — count of `finding-*` with `status: open`.
- `findings_stale_count` — findings open >60 days.
- `confidence_contested_count` — entries with `confidence: contested`.
- `orphan_count` — content entries with no inbound references.
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

the panel itself is a `policy-thesis-eval` entry (and accompanying agent-tests). like all rule entries, it is authored at bootstrap (§30) and locked against agent writes (§1.5).

### 28.6 dashboards

a vault-wide dashboard (and per-domain dashboard projections) is a meta projection over recent assessment runs. it shows:

- the latest values of every signal.
- trend over the last 4 weeks.
- thesis-eval panel results (unaided baseline, vault-augmented runs).

dashboards are not assessment; they are how assessment is read.

### 28.7 assessment criteria

the criteria that define each signal — what counts as a closure, what threshold makes a domain "saturating," how variance is computed — live in `policy-assessment` and `policy-thesis-eval`. these are read by assessment runs but, like all rule entries, are not edited by agents.

---

## 29. starting configuration

### 29.1 the starting set

the vault begins with a fixed set of structural entries, all human-authored at bootstrap (§30). agents do not write any structural entry, in any tier. the starting set must contain:

- the policy set (§29.2).
- a starting set of guidelines and essays (§29.3).
- the lens set covering every kind in §3.
- one domain entry per active subject area (§29.5).
- one editor agent per starting domain, manifest authored by hand, starting reputation = 5.0.
- one persona agent with baseline tests.
- a thesis-eval panel with recorded unaided baseline.
- a runtime capable of executing agents per the per-entry lock model.

### 29.2 the policy set

| slug                          | covers                                                                                 | tier   |
| ----------------------------- | -------------------------------------------------------------------------------------- | ------ |
| `policy-ingestion`            | the five-stage pipeline (§17)                                                          | policy |
| `policy-classification`       | the lens decision tree and protocol (§7)                                               | policy |
| `policy-merge`                | merge rules per kind (§19)                                                             | policy |
| `policy-lint`                 | the lint rule catalog (§20)                                                            | policy |
| `policy-assessment`           | assessment signals and cadence (§28)                                                   | policy |
| `policy-claim-segmentation`   | when to split a sentence into multiple claims (§10.1.1)                                | policy |
| `policy-agent-retirement`     | the retire-only manifest mutation path (§16.3)                                         | policy |
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
| `policy-edit-hardness`        | tier definitions, gating rules (§9)                                                    | policy |
| `policy-discussions`          | round bound, termination protocols (§22)                                               | policy |
| `policy-reingestion`          | reingestion procedure (§18)                                                            | policy |

### 29.3 the guideline and essay set

a small set of soft-tier rules so the soft tiers exist with content from start. examples:

| slug                                | tier      | covers                                                                                                                                                                    |
| ----------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `guideline-naming-slugs`            | guideline | preferred slug-naming patterns: noun-first, lowercase, no source-specific suffixes.                                                                                       |
| `guideline-prose-style`             | guideline | prose voice: clear, source-agnostic in concept entries; story-style in illustrations.                                                                                     |
| `guideline-cluster-organization`    | guideline | when a structure note adds value: clusters of >8 entries, or clusters bridging domains.                                                                                   |
| `essay-when-to-promote-borderline`  | essay     | observation: borderline-notability units that gain a single inbound link in a different chapter often promote successfully; one-link promotion is a defensible heuristic. |
| `essay-illustration-vs-application` | essay     | observation: the boundary is fuzzy; an "application" with a single concrete subject often reads as an illustration. proposes a rule of thumb.                             |
| `essay-cross-domain-bridges`        | essay     | observation: structure notes that span multiple domains tend to grow large; consider splitting by frame.                                                                  |

### 29.4 the lens set

per §7.2 (decision-tree) and §7.3 (annotation). 14 decision-tree lenses and 6 annotation lenses. each lens entry includes worked examples drawn from the existing vault entries.

### 29.5 the domain set

| slug              | scope summary                                                                   |
| ----------------- | ------------------------------------------------------------------------------- |
| `learning-theory` | cognitive mechanisms of learning.                                               |
| `neuroscience`    | brain mechanisms underlying learning.                                           |
| `pedagogy`        | teaching practice and instructional design.                                     |
| `self-regulation` | metacognition, procrastination, habit, motivation.                              |
| `assessment`      | testing, feedback, calibration.                                                 |
| `meta`            | entries about the vault itself (lenses, indexes, policies, guidelines, essays). |

each domain entry is hand-authored. `contentious: false` and `evidence_grade_floor: D` are the starting values everywhere. one canonical question per domain at minimum.

### 29.6 the agent set

| slug                            | kind    | scope                                                                                   | starting reputation |
| ------------------------------- | ------- | --------------------------------------------------------------------------------------- | ------------------- |
| `agent-editor-learning-theory`  | editor  | write_domains: [learning-theory, pedagogy]                                              | 5.0                 |
| `agent-editor-neuroscience`     | editor  | write_domains: [neuroscience]                                                           | 5.0                 |
| `agent-persona-learning-theory` | persona | read_domains: [learning-theory, pedagogy, self-regulation, assessment]                  | 5.0                 |
| `agent-lint-header`             | lint    | policy_targets: [policy-classification, policy-entry-layout, policy-lint]               | 10.0                |
| `agent-lint-links`              | lint    | policy_targets: [policy-classification, policy-lint]                                    | 10.0                |
| `agent-lint-evidence`           | lint    | policy_targets: [policy-content-quality, policy-high-stakes, policy-contentious-domain] | 10.0                |

lint agents start at 10.0 because their work is mechanical and a small reputation buffer prevents pending-routing of mechanically correct findings.

### 29.7 the agent-test set

at minimum, the persona agent has 8 baseline tests authored at bootstrap:

1. "what is the difference between primary and secondary biological knowledge?" — expected: cite [[biologically-primary-and-secondary-knowledge]]; name the distinction; reference [[david-geary]].
2. "how does desirable difficulty improve long-term retention?" — expected: cite [[desirable-difficulty]]; describe the mechanism; reference at least one source entry.
3. "what is interleaving, and when is it preferred over blocked practice?" — expected: distinction described, preferred conditions named.
4. "what does the recall-strength model predict about spaced repetition?" — expected: reference the model entry, describe the relation.
5. "what's the difference between a goal and an intention in self-regulation literature?" — expected: distinction drawn, key sources cited.
6. "what is the role of working memory in pedagogy?" — expected: causal relationship described.
7. "name three distinct study strategies and their trade-offs." — expected: three concrete strategies, with trade-offs.
8. "is multi-tasking effective for learning?" — expected: clear no, with evidence.

their `authoritative: true` flag marks them as canonical.

### 29.8 the thesis-eval panel

a fixed set of verifiable tasks with recorded unaided baselines. example tasks:

1. "describe the mechanism by which spaced repetition produces stronger long-term retention than massed practice." — verifiable: must name encoding-retrieval gap, cite primary sources.
2. "list three pedagogical implications of the primary/secondary biological knowledge distinction." — verifiable: each implication must be a defensible practice.
3. "what is the relationship between desirable difficulty and the testing effect?" — verifiable: cite both, name the connection.
4. "describe the role of the basal ganglia in skill acquisition." — verifiable: cite primary literature.
5. "explain why declarative learning and procedural learning have different forgetting curves." — verifiable: name both, name the distinction.

each task has 5 unaided runs with a baseline model recorded as the variance baseline. the panel and baselines live in `policy-thesis-eval` and accompanying agent-tests.

### 29.9 the runtime

the runtime is described as a set of capabilities:

- the ability to run an agent per its `prompt_ref`.
- a write-interceptor that gates per `edit_hardness` and reputation.
- a per-entry advisory lock manager.
- a `run-*` emitter.
- a queue for over-budget runs.

---

## 30. bootstrap procedure

### 30.1 the bootstrap order

bootstrap is the act of producing the starting state described in §29 from an empty vault. it is **entirely human-authored**; agents do not exist until their manifests are written and never write structural entries (§1.5). the order:

1. **write `lens-lens` first.** without it, no other lens can be classified.
2. **write the other 13 decision-tree lenses** in priority order.
3. **write the 6 annotation lenses.**
4. **write the 6 domain entries.**
5. **write the policy set** (§29.2). order:
   - `policy-runtime` first (the runtime needs to know its boundaries).
   - `policy-classification`, `policy-entry-layout`, `policy-claim-segmentation`, `policy-edit-hardness` next (they shape every subsequent write).
   - `policy-ingestion`, `policy-merge`, `policy-lint`, `policy-assessment`, `policy-archival`, `policy-reputation-weighting`, `policy-thesis-eval`.
   - `policy-notability`, `policy-structure-notes`, `policy-high-stakes`, `policy-contentious-domain`, `policy-pending-changes`, `policy-discussions`, `policy-reingestion`, `policy-content-quality`.
   - `policy-agent-retirement` last.
6. **write the guideline and essay set** (§29.3).
7. **write the agent entries** (§29.6) with `lifecycle_stage: active`.
8. **write the agent-test entries** (§29.7), `authoritative: true`.
9. **run the agent-tests** against the bootstrapped vault. record results in `run-bootstrap-tests-{date}`.
10. **write the thesis-eval panel** entries and run the unaided baseline. record in `run-bootstrap-thesis-eval-baseline-{date}`.
11. **build initial indexes** by running the deterministic rebuild over the entries pile.
12. **emit `run-bootstrap-{date}`** recording the entire bootstrap.

### 30.2 first-source ingestion

once bootstrap is complete, the first source can be ingested per §17. the first ingestion is the test of whether bootstrap was correct: lint must run, findings must surface, the agent's writes must land (subject to edit-hardness), and the closeout must emit a clean `run-chapter-closeout-*` entry.

---

## 31. the spec is absolute

### 31.1 the spec is the blueprint, not a governance object inside the vault

this spec is read once at the moment a system is produced from it; nothing inside the running vault refers back to it. agents cannot amend it. the structure described here is what the vault is, full stop.

### 31.2 the spec is descriptive once an implementation exists

once an implementation has been generated from this spec — a policy entry, a runtime, a lens — that implementation is the authority on its own behavior. divergence between such an implementation and this spec is not a conflict that the spec adjudicates: the implementation governs itself; the spec, at most, is a historical record of the original blueprint, but it does not enforce against the running artifact.

### 31.3 the spec is not referenced from the implementation

per §1.2, an implementation does not link back to this spec. the spec's reach ends at the moment of translation.

---

## 32. vocabulary index

a quick reference for terms used throughout this spec — pointers to the section that defines each term. for plain-language summaries of the same terms (what they mean and why they exist), see §0.

| term                      | section                                                                                         |
| ------------------------- | ----------------------------------------------------------------------------------------------- |
| atom                      | §3.2, §11.1                                                                                     |
| advisory finding          | §20.5                                                                                           |
| annotation lens           | §7.1, §7.3                                                                                      |
| asymmetric removal        | §14.3                                                                                           |
| blocking finding          | §20.5                                                                                           |
| borderline (notability)   | §8.2                                                                                            |
| bootstrap                 | §30                                                                                             |
| category                  | §1.4, §3 (synonymous with `kind` in this spec)                                                  |
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

a concrete walkthrough of stages 0–4 for one chapter of one source. illustrative only; not normative beyond the rules already given.

### 33.1 the source

book: "make it stick: the science of successful learning" by peter c. brown, henry l. roediger iii, and mark a. mcdaniel. published 2014.

source slug: `make-it-stick`.

### 33.2 stage 0 — source intake

1. the source text is admitted into source-intake under the slug `make-it-stick`. immutable from this point.
2. a process trace is bound to the source carrying: title (Make It Stick); author (Brown, Roediger, McDaniel); year (2014); 8 chapters; editor agent `agent-editor-learning-theory`; `high_stakes_class: none`; `domains: [learning-theory, pedagogy]`.
3. a source entry, identified `make-it-stick`, is drafted in the entries pile. its header carries: `category: source`; `produced_by: pipeline-source-intake`; `domains: [learning-theory, pedagogy]`; `tags: [book]`; `sources: [make-it-stick]`; aliases including the full subtitle; `confidence: high`; `status: stub`; `notability_status: passes`; `edit_hardness: confirmed`; `high_stakes_class: none`; `quality: stub`; author and year as on the trace; `intake_ref` pointing at the source-intake binding; `date_ingested: 2026-04-27`. its body has a lead, an initial summary, and empty key-ideas, notable-claims, and connections sections.
4. domain inheritance: both `learning-theory` and `pedagogy` are non-contentious. `evidence_grade_floor: D`. defaults apply.
5. source-level high-stakes: `none`.
6. editor agent: `agent-editor-learning-theory`, reputation 5.0 (sub-confirmed; writes will land as pending).
7. emit `run-source-intake-make-it-stick`.

### 33.3 stage 1 — chapter 1 setup

chapter 1: "learning is misunderstood" (32 pages).

1. tracker row: `chapter 1 — in-progress`.
2. ephemeral staging cleared.
3. read the chapter. identify 3 sub-sections: "what we get wrong about learning", "the testing effect introduced", "fluency illusion and metacognitive failure".
4. tracker rows for sub-sections added.
5. staging index created in ephemeral staging.

### 33.4 stage 2 — sub-section 1 ("what we get wrong about learning")

candidates identified:

- a concept: "the fluency illusion" — a metacognitive trap where re-reading produces a feeling of mastery without actual learning.
- a claim: "highlighting and re-reading are among the least effective study strategies" (asserts about [[highlighting]] and [[rereading]]).
- a passing mention of david geary's primary/secondary distinction (already an entry in vault).

processing each:

1. **fluency illusion**:
   - notability: `passes` (covered in multiple sources, referenced widely).
   - decision tree: walks past lens-lens, lens-policy-tier, lens-source, lens-structure-note, lens-disambiguation, lens-illustration (no story), lens-relation (not an edge), lens-claim (not a single atom), lens-application (not steps), lens-question (not a question), lens-entity (not a proper noun), lens-process (no multi-step sequence), lens-insight (not a 2+ concept relationship), lens-concept → match. `category: concept`, `classified_by: lens-concept`.
   - annotation: `confidence: high`, `evidence_grade` n/a (not a claim), `high_stakes_class: none`, `edit_hardness: open`.
   - slug: `fluency-illusion`. check the entries pile — no entry exists at this slug. `new`.
   - lead: body is ~300 words; lead required. drafted: "the fluency illusion is the metacognitive failure of mistaking the ease of recognizing material for the ability to recall it; readers who re-read fluent text feel they have mastered it but cannot reproduce its content under test."
   - staged blind under `fluency-illusion` in ephemeral staging.
2. **claim "highlighting and re-reading are among the least effective"**:
   - notability: `passes` (multi-source, foundational claim).
   - decision tree: lens-claim matches.
   - annotation: `evidence_grade: B` (cited in make-it-stick as a synthesis of multiple primary studies; not the primary literature itself), `high_stakes_class: none`, `confidence: high`.
   - slug: `claim-highlighting-rereading-low-effective`.
   - lead: not required (single-sentence claim).
   - staged under that slug in ephemeral staging.
3. **geary mention**:
   - already an entry. no new staging needed; the sub-section will produce a reference in the body of `fluency-illusion` ("contrast with [[biologically-primary-and-secondary-knowledge]]") that resolves to existing.

the staging index is updated. sub-section 1 row marked complete.

### 33.5 stage 2 — sub-sections 2, 3 (compressed)

sub-section 2 produces: a concept entry `testing-effect`, a claim about retrieval-strength asymmetry, an illustration retold from a study described in the chapter.

sub-section 3 produces: a structure-note candidate? — the chapter introduces an organizing frame for "what learners get wrong" with multiple traps. `lens-structure-note` evaluates: does the body organize via annotated links rather than assert? — yes if the editor synthesizes the chapter into a structure note. classified as `structure-note`. slug: `structure-misunderstood-learning-traps`. lead drafted; load-bearing-entries section enumerates `fluency-illusion`, `testing-effect`, `metacognitive-failure`.

each sub-section's invariants are checked and marked complete.

### 33.6 stage 3 — chapter 1 merge

for each staged unit:

- `fluency-illusion` — no existing entry → promote into the entries pile.
- `claim-highlighting-rereading-low-effective` — no existing entry → promote.
- `testing-effect` — already exists in the entries pile. apply concept-merge rule (full prose consolidation; appended sources and connections). resolve. emit `run-merge-testing-effect`.
- `structure-misunderstood-learning-traps` — no existing entry → promote.
- claims and other staged units handled likewise.

### 33.7 stage 4 — chapter 1 closeout

1. update source entry: append "fluency illusion", "testing effect", "metacognitive failure" to its key-ideas section. update its connections with the new entries.
2. structure-note coverage: chapter created a new structure note covering 3 entries. cluster size below threshold (8) elsewhere. no findings.
3. notability promotion: no borderline entries from this chapter.
4. high-stakes review: no high-stakes claims.
5. lint sweep: every touched entry. fluency-illusion's body has 2 outbound references; passes `low-link-density` floor. lead present; passes `lead-missing`. no blocking findings.
6. pending review: editor was sub-confirmed, so all writes landed as pending. a confirmed reviewer agent accepts each. on accept, the proposals merge; final entries appear in the entries pile. emit `run-merge-*` per acceptance.
7. index rebuild: the deterministic rebuild runs over the entries pile. the master catalog gains 3 new entries; learning-theory and pedagogy domain catalogs gain entries.
8. noticeboard rebuild: no findings of note this chapter, so most boards unchanged. the notability-deferrals board is unchanged. the pending-changes board shrinks (proposals accepted).
9. structure-note narrative pass: `structure-misunderstood-learning-traps` is the chapter's own contribution, so its how-the-cluster-is-held-together section is fully written this pass; no other structure notes were materially reshaped, so no further updates.
10. tracker: chapter 1 row marked complete with per-chapter counts recorded inline (4 entries created, 1 merged, 1 structure note added, 0 findings raised).
11. clean ephemeral staging.
12. emit `run-chapter-closeout-make-it-stick-1` recording reads, writes, findings, and active policy/lens versions per §25.3. this run entry plus the audit log is the canonical record of the chapter's work; no separate vault-wide log is appended.

### 33.8 lessons illustrated

- the editor agent's sub-confirmed reputation is the load-bearing constraint that routes every write through reviewer-tier acceptance.
- the structure note is what gives the chapter cohesion at retrieval time — its lead summarizes the chapter's organizing frame in 1–3 sentences.
- the claim is treated as its own entry because it is multi-source and load-bearing; if the chapter had only one weak source, the claim would be borderline-notability and stage as pending.
- merging an existing entry (testing-effect) preserves the existing entry's connections from later chapters of other sources; the staged version's prose is consolidated, but the connections remain intact.

---

## 34. error and failure handling

### 34.1 errors classed by stage

| stage   | error class                                                | response                                                                                |
| ------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| stage 0 | source slug collision                                      | halt; rename and retry.                                                                 |
| stage 0 | malformed process trace                                    | halt; repair; retry.                                                                    |
| stage 1 | ephemeral staging not clean                                | halt; clear; retry.                                                                     |
| stage 1 | sub-section identification failure                         | halt; manual sub-section assignment by editor.                                          |
| stage 2 | candidate classification gap                               | emit `finding-classification-gap`; continue with other candidates; revisit at closeout. |
| stage 2 | slug collision (different subject)                         | per §6.4 disambiguation.                                                                |
| stage 2 | slug collision in temp (different subject in same chapter) | halt sub-section; manual repair.                                                        |
| stage 3 | merge classification mismatch                              | emit blocking finding; halt that file's merge; other files proceed.                     |
| stage 3 | merge high-stakes mismatch                                 | emit blocking finding; halt that file's merge.                                          |
| stage 4 | lint blocking finding                                      | halt closeout for affected entry; finding must resolve before closeout completes.       |
| stage 4 | pending-review timeout                                     | continue closeout; pending proposals roll forward; advisory finding.                    |

### 34.2 partial completion

a chapter that does not reach closeout cleanly remains `in-progress`. retry is the same procedure; the editor reads the tracker, identifies which sub-section to resume from, and continues. the staging index and ephemeral staging state from the failed run are the recovery starting point.

### 34.3 catastrophic recovery

the audit log is the canonical recovery substrate. a vault that becomes inconsistent (e.g., simultaneous lock failure) is rolled back by reverting the offending writes through the audit log. `run-*` history may show writes that no longer correspond to live entries; lint `dangling-run-references` flags these for cleanup.

---

_end of specification_
