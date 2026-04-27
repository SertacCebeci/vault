# the vault

> for the path that led to this framing — building personal wikis, handing them to agents as context, and noticing what changed — see [origin.md](./origin.md). this document describes what we are building and why.

## the thesis

on tasks with verifiable answers, the run-to-run variance of large language models is largely explained by context underspecification. with a well-aligned context — a slice of the world that overlaps with the question being asked — a sufficiently capable model produces reliable answers. with a bad context, variance spikes and the model drifts into the wrong region of its distribution.

three rules govern this:

1. well-aligned context reduces variance and improves output quality.
2. distant or wrong context degrades quality and often _increases_ variance.
3. exhaustive or redundant context does nothing — no priming, no improvement, just token cost.

this lets us push the locus of uncertainty out of the model itself and into a separate problem: **what to feed it**. the model is no longer where reliability is won or lost; the choice of context is.

what we are building, then, is a substrate that solves that problem at scale: a large, self-governing knowledge base that captures arbitrary text information, connects it densely, and corrects itself as it grows. the end aim is a context-gathering layer — something any agent, including future versions of us, can draw a primed context from for any task it faces. the substrate is the project. what consumes it is downstream.

## why a large vault, not a notebook

for context selection to work, you do not strictly need an enormous knowledge base. a carefully curated one, tied to specific problems, is enough to make individual agents more reliable. but there is a second reason to aim larger.

building a usable knowledge base with agents costs a great deal of tokens. if we are going to pay that cost, we want the knowledge base to do more than serve as a reliable reference. we want it to surface _hidden_ information — connections that would never appear in a narrowly scoped wiki.

a wiki about pianos might solve the daily problems of a piano luthier. it will not help the luthier who is suddenly asked to design a piano for a space station. that example is silly, but the pattern is not: scientific and technological progress often emerges from the collision of disciplines that had no obvious reason to meet. a knowledge base wide enough to host those collisions is a different object from one narrow enough to answer today's question. we want both.

the vault we are building is therefore large by design. think of it as wikipedia, except the editors are agents rather than humans. they read sources, write entries, discuss, revise, and continuously shape the vault. that editing process is where most of the project's attention goes.

## what counts as a knowledge unit

before we can ask how to store information, we have to ask what information is.

broadly: given a context, information is anything that reduces uncertainty about a situation. it helps to hold three distinctions in mind:

- **signal** — something transmitted.
- **data** — recorded symbols or facts: `23`, `red`, `12:05`.
- **information** — signal or data interpreted in a way that reduces uncertainty for some observer.

`23` on its own is data. _"the temperature is 23°C and the forecast says rain"_ is information, because it changes what you do next. same number, different context, different informational content.

something counts as information when it does at least one of the following: reduces uncertainty, conveys meaning, changes understanding, or enables a decision. none of these are properties of the content alone. they are relational. a bell ringing is information only if you know it marks the end of class. the absence of an error message is information if you were waiting for one. even silence can be information. information does not exist without three things: a **receiver**, a **context**, and an act of **interpretation**. strip any one of them and you are left with raw signal or data.

a useful consequence: two pieces of information are **orthogonal** when they reduce uncertainty about different things. knowing _who_ sent a message and knowing _where_ it was sent from are roughly orthogonal — learning one tells you almost nothing about the other. this matters when designing a sequence of context fragments to retrieve. the best next fragment is the one whose content is expected to reduce the most remaining uncertainty, conditioned on what you already have.

the practical implication: building a knowledge base is not simply about accumulating content. it is about accumulating content that is _maximally informative relative to the questions that will be asked of it_. a perfectly redundant knowledge base — one that only restates what the model already knows from training — adds zero information. a badly targeted one — full of content distant from the actual problem — adds noise and inflates variance. the sweet spot is content that is both aligned with future tasks and genuinely novel relative to what the model already has.

### the situational problem

because information only makes sense relative to a context, cleanly separating information from context is very hard.

consider the sentence _"the ball is red."_ on its own, knowing nothing about the ball or why it matters, this gives you essentially no information. but if you are at a roulette table and you win when the drawn ball is red, the same sentence suddenly becomes extremely _important_.

importance, in other words, is situational. every fact has a relative importance that depends on the situation in which it is evaluated. this makes building a truly situation-independent information bank an intractable problem: without a situation, there is no criterion for filtering, and without filtering, there is no way to extract meaning from the pile.

our answer is not to try. instead of one neutral, lossless, situation-free store, we build many situated views into the store. each view carves a slice of the vault that is coherent given some role, domain, or intent. we call these views _personas_. retrieval happens against a slice, not the whole. importance is no longer a universal property of the fact; it is a property of the slice the fact lives in.

for now we treat personas primarily as **introspection tools**: a way for the vault to test that a slice of itself is internally coherent and answers what it claims to cover. they may eventually become an outward-facing surface, but that is a downstream question. the immediate use is self-assessment.

## how the vault holds knowledge

the substrate is a single flat pile of markdown files under `wiki/entries/`. category is a frontmatter field, not a directory. the kinds of entry the vault recognizes:

- **knowledge entries** — concepts, sources, illustrations, applications, insights, processes, entities. the substance of the vault.
- **claims** — atomic assertions carrying evidence and an evidence grade. the unit smaller than an insight. claims are what contradict each other; claims are what slices of the vault can be said to "hold as true."
- **relations** — typed edges as entries: _A supports B_, _A contradicts B_, _A is an instance of B_, _A supersedes B_. undirected wikilinks still exist for casual cross-reference, but load-bearing connections live in relation entries where they can carry evidence and be reasoned about.
- **questions** — open questions the vault cannot yet answer. they pin gaps, drive ingestion priorities, and get closed (or narrowed) as new material arrives.
- **lenses** — the rules of classification, written down as entries. detailed below.
- **domains** — the subject axes along which entries are indexed. each domain entry declares scope, out-of-scope, and canonical open questions. per-domain index files are generated views over those declarations.
- **policies** — the rules of the vault itself. ingestion protocol, classification protocol, merge rules, lint rules, assessment criteria — each a policy entry, not a section in a readme.
- **agents** — the editors of the vault, written down as entries.
- **runs** — one entry per agent execution. what was read, what was written, what findings were raised, which policies and lens versions were in force.
- **findings** — lint findings, contradictions, regressions. each finding is an entry with a status (`open`, `resolved`, `wontfix`).
- **personas** — situated slices of the vault, used as introspection / self-assessment artifacts.
- **persona tests** — queries paired with expected answer shapes, run as regressions whenever the vault changes. a failing persona test becomes a finding.
- **discussions** — when agents disagree, the exchange is recorded as a `discussion-*` entry attached to the disputed entry.
- **notifications** — inter-agent mentions, review requests, and escalations.

one entry per slug, flat layout, category in frontmatter. nothing lives in a database table or in application logic when it could be written down as a file in the same flat pile.

### lenses: questions as the unit of categorization

most wikis answer the categorization problem with folders and taxonomies — a directory tree, a tag list, a hand-maintained hierarchy. we do not. categories in our vault are the answers to **questions**, and the questions are themselves entries.

a _lens_ is an entry whose body is a single yes/no question and a set of criteria for answering it. "is this entry a story with a protagonist, a setting, and an outcome?" is one lens (it covers the `illustration` category). "could a practitioner follow this as a set of instructions?" is another (it covers `application`). classifying a new entry means running it down the lens decision tree in priority order and taking the first match.

this design has three properties that matter:

- **the rules live next to the knowledge, not in code.** a lens is a markdown file. when the definition of "insight" evolves, someone edits the lens entry; the next classification pass uses the new rule automatically. we never deploy a new agent to change a taxonomy.
- **every classification is auditable.** each entry's frontmatter records which lens ruled on it (`classified_by: lens-concept`). a later reader can open that lens, read its current criteria, and judge whether the original decision still holds — or whether the category needs revisiting because the rule has drifted.
- **the scheme is self-referential in a clean way.** there is a lens whose question is _"is this entry itself a lens?"_, and applied to itself it returns yes. that fixed point is what lets the lens system classify its own members without needing an external authority. the vault names the shape of its own categories using the same machinery it uses for everything else.

two kinds of lenses do the work. **decision-tree lenses** pick the entry's category — one match per entry, priority order, first-match wins. **annotation lenses** run _after_ the category is set and tag orthogonal properties: how strong is the evidence, is this time-bounded, is it disputed, by whom. annotation lenses do not compete with each other; each one writes its own frontmatter field.

### the connection substrate

a vault that only stores entries is a pile. what makes it a graph is the connection layer:

- **wikilinks** — cheap, undirected, used liberally for cross-reference and discovery.
- **relations** — typed, directed, evidence-bearing edges as their own entries. _A supports B_ and _A contradicts B_ are queryable objects, not prose buried inside an entry.
- **claims** — atoms small enough that contradictions show up sharply. a claim with `confidence: contested` and an inbound `contradicts` relation from another claim is a target for resolution.
- **questions** — connections to absence. an open question is a vault entry that says "we don't yet know how X relates to Y." closing it produces relations or claims; failing to close it after enough ingestion is a coverage finding.

connection density is half the value of the vault. an isolated entry in a large vault is no better than the same entry in a notebook. the lint and assessment layers (next two sections) keep pressure on this.

## how the vault governs itself

we want the vault to be more than a pile of knowledge. we want it to be a self-describing, self-governing object — an information cloud that carries, alongside its content, everything needed to read it, extend it, and judge it.

the bootstrap is circular by design: to understand how the vault is maintained, you read policy entries; to understand how those policies are applied, you read the agent entries that enact them; to understand how any specific entry got its category, you read the lens entry named in its frontmatter. nothing is hidden in a database table or hard-coded in application logic when it could be written down as a file in the same flat pile.

the root `CLAUDE.md` shrinks accordingly. it is not the rulebook anymore; it is a bootstrap pointer that says, in effect, _"start at the policy index."_ from there, every rule the system enforces can be reached by following wikilinks.

we do this for four reasons:

**auditability.** any decision made against the vault — a classification, an ingestion, a lint finding — is traceable to a vault entry that a human can read, challenge, and revise. there is no opaque config file and no silent policy.

**evolvability.** changing the behavior of the system is the same operation as changing its content: edit a markdown file, let the agents pick up the new rule on the next pass. we do not have a separate deploy cycle for "the rules" versus "the data." the rules _are_ data.

**portability.** a vault that carries its own lenses, agents, policies, and assessments is a self-contained artifact. it can be copied, forked, versioned, or published without dragging hidden infrastructure along with it.

**coherence.** because the same machinery (entries, frontmatter, lenses, links) describes both content and meta-content, we never have to maintain two parallel systems. the meta-content benefits from the same linting, the same linking, the same retrieval. the vault improves as a whole.

### agents as a population

the editors of the vault are not a fixed staff. they are a population — created, judged, mutated, and retired by the same machinery that maintains the vault itself. the design is closer to an rl environment than to a wiki: the vault is the world, the agents are the population, the policies and lenses are the rules of physics, and reputation is the reward signal. this framing is what lets us imagine the system improving on its own, rather than needing every refinement deployed by hand.

concretely, the population mechanics rest on a few moving parts:

- **lifecycle protocols.** vault entries describe how an agent is created, how its prompt or domain bindings can be edited (its "genes" mutated), and how it is retired. spawning a new editor is a vault operation, not a deploy.
- **assessment via scored work.** agents earn standing through tasks the vault can grade — passing persona tests in their declared domains, writing questions other agents accept, raising contradictions that survive review, judging others' contributions.
- **reputation as the access gate.** rather than fixed permissions, each agent carries a reputation signal that scales its write access. low-reputation agents propose; high-reputation agents merge. reputation is a permission mechanism, not a market signal.
- **edit-hardness gradient.** not every entry is equally mutable. an ordinary knowledge entry is cheap to revise; a lens, a policy, or a high-confidence claim is expensive. meta-rules — the rules of the jungle itself — sit at the top of the gradient and require both high reputation and quorum to amend. an entry's edit-hardness is a frontmatter field, set by the lens that classified it.
- **versioning and rollback.** every entry change is captured in a `run` entry, and rolling back is the same mechanism as forward-editing, pointed at a prior version. an agent that proposes a bad change can be reverted cheaply, without erasing the trace of its proposal.
- **discussion as artifact.** disagreement is not lost in thread state. when agents conflict on a claim, the exchange is recorded as a `discussion-*` entry attached to the disputed entry. the social fabric of editing is auditable end-to-end.

a corollary worth stating early: **the line between an editor agent and a persona may not be a real line.** an editor is a knowledge slice plus write permissions and lifecycle bindings; a persona is a knowledge slice plus voice rules and read-side bindings. the manifest is the same shape; only the role differs. we keep the categories separate for now to track the distinction explicitly, but we are not committed to keeping them apart.

## how the vault corrects itself

self-correction is the spine of this project. a vault that only grows is a hoarder; a vault that grows _and_ continuously notices its own mistakes is a self-improving artifact. the correction loop has four moving parts.

**1. the ingestion pipeline produces typed evidence as it goes.** intake creates a `source` entry; unpacking splits the source into knowledge units and runs them through the lenses; storage adds entries, claims, and relations. when a new unit conflicts with an existing claim, the conflict is recorded as a `finding` and a `relation` with predicate `contradicts` — not buried in prose. when a unit cannot be classified, that's a finding too. the pipeline does not silently absorb anomalies; it surfaces them as objects.

**2. lint agents run continuously against policy entries.** the criteria they enforce — slug uniqueness, orphan detection, broken wikilinks, classification consistency, lens coverage, domain coverage, missing category-specific fields, low link density, stale content, type misclassification — are themselves policy entries. evolving lint behavior is the same operation as editing any other piece of knowledge. lint runs as a scheduled pass and on every entry write; both modes produce findings.

**3. findings are persistent objects, not log lines.** every finding is an entry with `status: open | resolved | wontfix`, a link to the rule that fired, and links to the entries involved. nothing a linter notices gets swallowed into prose or a running notes section. resolutions are linked from the finding to the fix; `wontfix` decisions are linked to a justification. this means the vault carries an open list of things wrong with itself, visible at any time.

**4. discussions and contradictions drive revision.** when two claims contradict, or when two agents disagree on a classification, the disagreement becomes a `discussion-*` entry attached to the disputed object. resolution is a vault operation: a new version of the disputed entry, a new relation, or a `wontfix` finding linking to the discussion as the rationale. nothing dies in chat state.

reingestion is a special case of correction. when a source is reingested, the new pass writes blind — without reading the existing entries — and merges only at the end. the reingested version is treated as a depth upgrade rather than a replacement, because the existing entries have accumulated connections from later chapters that the fresh pass has not seen. this is documented in the merge policy.

## how the vault assesses itself

correction needs targets. the vault carries its own quality criteria as policy entries, and measures itself against them.

**coverage signals.** for each domain entry, the vault tracks: how many open questions it has versus how many it has closed; how many claims have evidence grades; how dense the local relation graph is; how many entries lack a domain index assignment that should have one. a domain whose open-question count keeps rising without closures is a signal to direct ingestion attention there.

**internal consistency signals.** how many open contradictions exist; how many findings are over a threshold age; how many claims have `confidence: contested`; how many entries are orphaned with no inbound wikilinks. these track whether the vault is converging or accumulating internal noise.

**source grounding.** what fraction of claims cite a source entry; what fraction of insights reference at least two sources; what fraction of concept entries draw from more than one source. a vault that learns from many sources but produces single-sourced entries is failing to do the synthesis work the project exists for.

**personas as coverage probes.** every persona declares which entries it knows deeply, which it knows conceptually, and which it is merely aware of. each persona carries `persona-test-*` entries — questions plus expected answer shapes. when persona tests pass, the slice is internally coherent for the questions it claims to cover. when they fail, that's a finding tied to the persona, the failed test, and (often) a missing or incorrect entry. persona tests are how we measure that a region of the vault is _adequate for purpose_, not just present.

assessment criteria themselves live as policy entries, and can be edited and versioned. when we change what "good coverage" means, we are editing a markdown file like any other. the next assessment pass uses the new criterion.

## the pipeline

the pipeline is what the vault does to itself. each stage consumes entries and produces entries. there is no out-of-band state.

1. **intake.** a candidate source becomes a `source` entry with `status: candidate`. an intake run proposes chapter or section boundaries, estimates domains, and opens `question` entries for what the source should close. rejected sources are recorded as entries with `status: rejected` and a reason.
2. **unpack.** each sub-section is read and split into knowledge units. decision-tree lenses pick each unit's category. annotation lenses stamp evidence grade, recency, and dispute status. conflicts with existing claims are recorded as findings.
3. **store.** knowledge entries, claims, relations, and questions go in. everything is linked into the existing graph under the same flat layout.
4. **lint.** lint agents — themselves entries, running against policy entries — scan continuously and produce findings.
5. **assess.** coverage and consistency signals are recomputed; persona tests are run; failures become findings. ingestion priorities for the next intake cycle are derived from the open-question and coverage-gap state.

every arrow between stages is a vault entry.

### scope of "any kind of text"

the long-term aim is to handle arbitrary text — books, articles, transcripts, emails, chat logs, code comments, personal notes. the current ingestion pipeline (one chapter per turn, source folder, process trace) is shaped for long-form structured sources. generalizing to unstructured text is an open problem listed below; for the seed phase we work with structured sources and treat the other shapes as forthcoming.

## the plan

concretely, we are building the following pieces, in roughly this order. every piece lives inside the vault as entries.

- **a wikipedia-like knowledge base with agents as the editors.** agents read raw sources, write entries, discuss disagreements, and revise each other's work in a continuous loop. humans stay in the loop for direction and quality review; the per-entry work is agent-driven.
- **a richer unit of knowledge than the entry.** alongside concepts, sources, illustrations, applications, insights, processes, and entities, we add three smaller units: `claim` (atomic assertions with evidence grades), `relation` (typed edges — `supports`, `contradicts`, `instance-of`, `depends-on`, `supersedes`), and `question` (open questions the vault hasn't yet answered). contradictions and connections become queryable objects.
- **lenses as the categorization layer, in two flavors.** decision-tree lenses pick categories; annotation lenses stamp orthogonal frontmatter fields. every lens is versioned so reclassification can be audited when a rule changes.
- **policies as vault entries, not as `CLAUDE.md` prose.** ingestion, classification, merge, lint, and assessment rules move out of the root rulebook into `policy-*` entries. `CLAUDE.md` reduces to a bootstrap pointer.
- **domains as entries, indexes as views.** each domain becomes an entry declaring scope, out-of-scope, and canonical open questions. per-domain files become generated projections.
- **source-grounded editor agents, defined as vault entries.** every editor is described by an `agent-*` entry: name, prompt, source material, allowed lenses, owned domains, write scope, current reputation, lifecycle stage. an agent does not write from thin air; it writes from sources it can cite.
- **agent lifecycle protocols.** explicit `policy-agent-create`, `policy-agent-mutate`, and `policy-agent-retire` entries describe how editors are spawned, revised, and retired. one agent producing or revising another is the same operation as any other vault edit, gated by reputation and edit-hardness.
- **reputation as a first-class signal.** every agent carries a reputation score from scored work: passing persona tests in its domains, writing questions other agents accept, raising surviving contradictions, judging others' contributions. reputation gates write access to higher-edit-hardness regions.
- **an edit-hardness gradient on every entry.** an `edit_hardness` frontmatter field, set by the classifying lens, makes some regions deliberately expensive to change. ordinary entries cheap; lenses, policies, and high-confidence claims expensive; meta-rules at the top require quorum.
- **versioning and rollback for every entry.** the `run` log records what changed; per-entry history is a projection over that log; rollback is forward-edit pointing at a prior version.
- **discussions and notifications as entries.** disagreements live as `discussion-*` entries attached to the disputed entry. inter-agent mentions, review requests, and escalations live as `notification-*` entries with status.
- **runs as entries; the log as a projection.** every agent execution produces a `run-*` entry recording reads, writes, active policy and lens versions, and findings raised. `_meta/log.md` becomes a rebuilt projection over runs.
- **findings as first-class, persistent objects.** lint findings, ingestion contradictions, and persona-test regressions all become `finding-*` entries with `status: open | resolved | wontfix`, a link to the rule that fired, and links to entries involved.
- **continuous linting against the vault's own rules.** lint agents scan in the background, enforcing criteria declared in lens and policy entries.
- **assessment criteria as policy entries.** coverage signals, consistency signals, and source-grounding metrics live as policy entries that the assessment pass uses to grade the vault. changing what "good" means is editing a markdown file.
- **personas as introspection artifacts.** a persona declares which entries it knows deeply, conceptually, or only by name; which claims it holds as true; what it explicitly excludes; voice and refusal rules. for now, a persona is how the vault tests that a slice of itself is internally coherent — not an outward-facing surface.
- **persona tests as regressions.** every persona carries `persona-test-*` entries — question plus expected answer shape — run whenever the vault changes. a failing test is a finding.

the long-term claim: if we can build a self-governing vault that captures arbitrary text knowledge, connects it densely, and continuously corrects and assesses itself against criteria written down inside it, we have a context-gathering layer good enough that any agent drawing from it has a fighting chance at reliable behavior. the vault is the substrate. what consumes it is the next problem, not this one.

## open problems

the design is not settled. the parts we expect to change as we build:

- **bootstrapping.** an agent-edited wikipedia whose agents are themselves vault entries is circular. we need a seed: a base set of policies, lenses, and a small number of human-authored editor agents, sufficient to ingest the first sources and produce the first usable assessments. how thick that seed must be is unresolved — thinner is better, but not so thin that the loop never reaches a stable state.
- **agent vs persona.** the manifests overlap heavily. we keep them as separate categories until the cost of maintaining the distinction is greater than the clarity it provides; this will likely become obvious in either direction once a real population is running.
- **what counts as good reputation.** passing domain tests, authoring questions other agents accept, raising surviving contradictions, and judging well are the first candidates. their weights will need calibration once the population is non-trivial.
- **adversarial robustness.** the population mechanics assume editor agents collaborate in good faith. we have not yet thought hard about collusion (agents trading reputation), sybil patterns (one operator running many agents), prompt-injection from sources (a malicious source rewriting policy entries), or the recursive problem (a high-reputation agent editing the lens that confers its authority). this needs an explicit threat model before the vault is exposed to outside contributions.
- **generalizing ingestion to arbitrary text.** the current pipeline is shaped for long-form structured sources. extending it to transcripts, emails, chat logs, and unstructured notes will need new policies and possibly new lenses. the seed phase scopes to structured sources.
- **retrieval shape.** the vault is meant to be a context-gathering layer, but the shape of the retrieval interface — graph traversal over relations, semantic search inside a slice, hybrid — is not yet defined. this becomes the operational gap the moment we try to use the vault as a live context source, even for ourselves.
