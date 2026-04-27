# persona markets

## where we started

we didn't start with a plan. we each started, independently and without coordinating, by building our own wikis. some of us framed them as personal learning journals; others as long-running memory for the work we were already doing. the content was a grab bag: prompts that had worked well for specific projects, notes on papers we'd read, fragments of books we wanted to keep close, articles we kept meaning to return to.

the common thread was that nearly all of us arrived at the same idea around the same time: use the wiki as a distillation tool for the things we actually care about. on paper this can look like a waste of tokens. in practice, if you're like us — compulsively saving articles to bookmarks, starring repos you never open again, amassing digital clutter that never pays off — this is exactly where a wiki earns its keep. the bookmark you never reread suddenly has a purpose when you can ask a question against it and have an agent dig through it to answer.

the interaction model stayed familiar: save things as they appear, ask questions when you are free. but underneath, the agent was doing real work — retrieving things you had forgotten you saved, rewriting them into durable notes, cross-linking them with what was already in the vault. for us, this was what llm-powered wikis were actually for — _a smarter bookmark_.

## from bookmarking to priming

if you use agents regularly, the next step is obvious. "i've read and saved this article, and i want to use it in my projects. let me hand the wiki, or some part of it, to the agent as context and see what happens."

it is worth pausing on how our interaction with agents has changed. most of us started out issuing action items — "do x, produce y" — and waiting for a result. over time, as models got smarter and tooling got better, the interaction evolved. we began posing questions rather than prescribing actions. the agents began asking us questions back. increasingly, the direction of questioning runs both ways.

what we noticed, once we started feeding the wiki as context, was that the agents started asking much more grounded questions. it was as if the temperature had dropped. this was excellent if you wanted reliable, repeatable answers. it was harmful if you did not yet know what you were looking for, because it narrowed exploration too early.

ask an agent about a concept and its implications without any wiki, and the same prompt on the same model can produce strikingly different answers from run to run. give both runs the same wiki as context, and their answers converge. this is not a shock — handing over the wiki is essentially saying _"look at this book, then tell me about this concept,"_ while withholding it says _"tell me about this concept."_ the two prompts are not the same prompt.

the takeaway: information-rich context primes an llm and pushes its behavior toward determinism. this is a win when the desired answer is a close derivative of the material in the context. it is a loss when it is not — if you are still figuring out the problem, or the context is tangential to it, priming narrows the search at exactly the moment you need it widest. a model given documentation on pianos and then asked about space travel will do _worse_ than one asked about space travel cold.

now imagine the extreme: a wiki that contains _all_ available information. set aside the fact that this is physically impossible given any finite context window. even in principle, it would do nothing. the model's training distribution already approximates "all available information." re-handing that distribution back to the model as context does not change the posterior. no priming happens because no novel information has been introduced.

partial information is where priming lives. when we surface the piece of the world that is relevant to the question at hand, the activations firing on the context overlap with the activations firing on the question, and output quality goes up. we are nudging the probability distribution toward the right region.

put together, three rules:

1. well-aligned context reduces non-determinism and improves output quality.
2. distant or wrong context degrades output quality and often _increases_ variance.
3. exhaustive or redundant context does nothing — no priming, no improvement, just token cost.

this gives us a powerful reframe. we can take the non-deterministic nature of the llm and push it out of the llm itself, into a separate problem: **context selection**. with a good context, a sufficiently capable llm will produce a reliable answer. with a bad context, variance spikes and the model drifts into the wrong region of its distribution. the llm is no longer the locus of uncertainty; the choice of what to feed it is.

this is what we have been building toward: a large, high-quality knowledge base plus a strategy for selecting slices of it as context for specific problems.

## why a large knowledge base, not a notebook

for context selection to work, you do not strictly need an enormous knowledge base. a carefully curated one, tied to specific problems, is enough to make individual agents more reliable. but there is a second reason to aim larger.

building a usable knowledge base with agents costs a great deal of tokens. if we are going to pay that cost, we want the knowledge base to do more than serve as a reliable reference. we want it to surface _hidden_ information — connections that would never appear in a narrowly scoped wiki.

a wiki about pianos might solve the daily problems of a piano luthier. it will not help the luthier who is suddenly asked to design a piano for a space station. that particular example is silly, but the pattern is not: scientific and technological progress often emerges from the collision of disciplines that had no obvious reason to meet. a knowledge base wide enough to host those collisions is a different object from one narrow enough to answer today's question. we want both.

so we started building a larger wiki. think of it as wikipedia, except the editors are agents rather than humans. they read sources, write entries, discuss, revise, and continuously shape the vault. that editing process is where much of the project's attention goes.

## intention

the concrete product of all this is _personas_.

when you write a system prompt today, it typically starts with something like "you are a world-class frontend developer," or "act as a seasoned psychiatrist trained in clinical psychology." the phrase does real work — it biases the model toward a register, a vocabulary, a set of implicit priorities — but it is a very thin version of the person it names. we want the thick version.

our aim is to expand these persona prompts against concrete, retrievable knowledge, so that the persona is not just a label on the response but a structured slice of the vault — a memory — that primes the model the way a real expert's memory would.

we found it useful to split the persona problem into two parts:

- **storing information** — what knowledge exists, and how it is written down so that it can be retrieved later.
- **retrieving information** — given a question, finding the slice of stored knowledge that should prime the answer.

most of what people call "persona" is retrieval. it is the act of reaching into a deep well and pulling out exactly the right context for this moment. but retrieval is only possible on top of something that has been stored well, so we have to start there. and before we can even ask how to store information, we have to ask a more primitive question: _what is information?_

### what is information

broadly: given a context, information is anything that reduces uncertainty about a situation.

more precisely, it helps to hold three distinctions in mind:

- **signal** — something transmitted.
- **data** — recorded symbols or facts: `23`, `red`, `12:05`.
- **information** — signal or data interpreted in a way that reduces uncertainty for some observer.

`23` on its own is data. _"the temperature is 23°C and the forecast says rain"_ is information, because it changes what you do next. same number, different context, different informational content.

something counts as information when it does at least one of the following:

- reduces uncertainty
- conveys meaning
- changes understanding
- enables a decision

none of these are properties of the content alone. they are relational. a bell ringing is information only if you know it marks the end of class. the absence of an error message is information if you were waiting for one. even silence can be information. information does not exist without three things: a **receiver**, a **context**, and an act of **interpretation**. strip any one of them and you are left with raw signal or data.

the sharpest formal version is from shannon: information is the amount of uncertainty removed by an observation. if you already knew the coin would land heads, being told it landed heads gives you zero bits. if you had no idea, it gives you one. the quantity of information is directly tied to how much your model of the world has to update.

a useful consequence: two pieces of information are **orthogonal** when they reduce uncertainty about different things. knowing _who_ sent a message and knowing _where_ it was sent from are roughly orthogonal — learning one tells you almost nothing about the other. this matters when you are designing a sequence of questions, or, analogously, a sequence of context fragments to retrieve. the best next fragment is the one whose content is expected to reduce the most remaining uncertainty, conditioned on what you already have. formally:

> ask the question whose possible answers are expected to reduce uncertainty about the task the most, normalized by the cost of asking.

this is a rigorous way of saying: do not ask what you already know, do not ask what is irrelevant, and do not ask the same thing twice in different words. redundancy adds tokens without adding information.

the practical implication is that building a knowledge base is not simply about accumulating content. it is about accumulating content that is _maximally informative relative to the tasks that will be asked of it_. a perfectly redundant knowledge base — one that only restates what the model already knows from training — adds zero information. a badly targeted one — full of content distant from the actual problem — adds noise and inflates variance. the sweet spot is context that is both aligned with the task and genuinely novel relative to what the model already has.

### how to store information

because information only makes sense relative to a context, cleanly separating information from context is very hard.

consider the sentence _"the ball is red."_ on its own, knowing nothing about the ball or why it matters, this gives you essentially no information. but if you are at a roulette table and you win when the drawn ball is red, the same sentence suddenly becomes extremely _important_.

importance, in other words, is situational. every fact has a relative importance that depends on the situation in which it is evaluated. this makes building a truly situation-independent information bank an intractable problem: without a situation, there is no criterion for filtering, and without filtering, there is no way to extract meaning from the pile.

our answer is not to try. instead of one neutral, lossless, situation-free store, we build many situated views into the store. each view — each _persona_ — takes the vast general vault and carves out a slice of it that is coherent given some role, domain, or intent. retrieval then happens against the slice, not the whole. importance is no longer a universal property of the fact; it is a property of the slice the fact lives in.

### lenses: questions as the unit of categorization

before we get to personas, there is a smaller but related problem to solve: how do we categorize the entries in the vault at all? most wikis answer this with folders and taxonomies — a directory tree, a tag list, a hand-maintained hierarchy. we do not. categories in our vault are the answers to **questions**, and the questions are themselves entries.

a _lens_ is an entry whose body is a single yes/no question and a set of criteria for answering it. "is this entry a story with a protagonist, a setting, and an outcome?" is one lens (it covers the `illustration` category). "could a practitioner follow this as a set of instructions?" is another (it covers `application`). classifying a new entry means running it down the lens decision tree in priority order and taking the first match.

this design has three properties that matter:

- **the rules live next to the knowledge, not in code.** a lens is a markdown file. when the definition of "insight" evolves, someone edits the lens entry; the next classification pass uses the new rule automatically. we never deploy a new agent to change a taxonomy.
- **every classification is auditable.** each entry's frontmatter records which lens ruled on it (`classified_by: lens-concept`). a later reader can open that lens, read its current criteria, and judge whether the original decision still holds — or whether the category needs to be revisited because the rule has drifted.
- **the scheme is self-referential in a clean way.** there is a lens whose question is _"is this entry itself a lens?"_ applied to itself, it returns yes. that fixed point is what lets the lens system classify its own members without needing an external authority to bootstrap it. the vault can name the shape of its own categories using the same machinery it uses for everything else.

two kinds of lenses do the work. **decision-tree lenses** pick the entry's category — one match per entry, priority order, first-match wins. **annotation lenses** run _after_ the category is set and tag orthogonal properties: how strong is the evidence, is this time-bounded, is it disputed, by whom. annotation lenses do not compete with each other; each one writes its own frontmatter field. together they turn classification from a single label into a structured judgment.

lenses are the smallest version of a larger pattern: the rules of the vault are themselves entries in the vault. the next section makes that pattern explicit.

### the vault is self-governing

we want the vault to be more than a pile of knowledge. we want it to be a self-describing, self-governing object — an information cloud that carries, alongside its content, everything needed to read it, extend it, and judge it. concretely, the vault holds the following kinds of entries, all in the same flat pile, distinguished only by category:

- **knowledge entries** — concepts, sources, illustrations, applications, insights, processes, entities. the substance of the vault.
- **claims** — atomic assertions carrying evidence and an evidence grade. the unit smaller than an insight. claims are what contradict each other; claims are what personas can be said to "hold as true."
- **relations** — typed edges as entries: _A supports B_, _A contradicts B_, _A is an instance of B_, _A supersedes B_. undirected wikilinks still exist for casual cross-reference, but load-bearing connections live in relation entries where they can carry evidence and be reasoned about.
- **questions** — open questions the vault cannot yet answer. they pin gaps, drive ingestion priorities, and get closed (or narrowed) as new material arrives.
- **lenses** — both decision-tree lenses that pick an entry's category and annotation lenses that tag orthogonal properties. the rules of classification, written down.
- **domains** — the subject axes along which entries are indexed. each domain is an entry declaring what is in scope, what is out of scope, and what its canonical open questions are. the per-domain index files under `_meta/` are generated views over these.
- **policies** — the rules of the vault itself. ingestion protocol, classification protocol, merge rules, lint rules — each one a policy entry, not a section in a readme. when the rules change, we edit policy entries and the next pass picks them up.
- **agents** — the editors of the vault, written down as entries. an agent is a name, a prompt, a declared slice of knowledge it speaks from, the lenses it may apply, the domains it owns, and the scope of its write permissions. agents are auditable because they are written down.
- **runs** — one entry per agent execution. what was read, what was written, what findings were raised, which policies and lens versions were in force. the chronological log is a projection over run entries, not a hand-authored file.
- **findings** — lint findings, contradictions, persona regressions. each finding is an entry with a status (`open`, `resolved`, `wontfix`), a link to the rule that fired, and a link to the entries involved. findings do not disappear into prose; they persist until someone resolves them.
- **personas** — the indexed slices of the vault that consumers query. a persona is a manifest: entries it knows deeply, entries it knows conceptually, entries it is aware of, claims it holds as true, entries it explicitly excludes, voice and refusal rules, and which mcp api keys are bound to it.
- **persona tests** — queries paired with expected answer shapes, run as regressions whenever the vault changes. a failing persona test becomes a finding.
- **queries** — historical questions served against personas, the retrieved slice, and the answer given. cheap, append-only, and the raw material for gap analysis.

the thing we are building is not a knowledge base plus a set of tools that live outside it. it is a knowledge base whose tools are defined inside it. the bootstrap is circular by design: to understand how the vault is maintained, you read policy entries; to understand how those policies are applied, you read the agent entries that enact them; to understand how any specific entry got its category, you read the lens entry named in its frontmatter; to understand what a persona represents, you read the persona's manifest. nothing is hidden in a database table or hard-coded in application logic when it could be written down as a file in the same flat pile.

the root `CLAUDE.md` shrinks accordingly. it is not the rulebook anymore; it is a bootstrap pointer that says, in effect, _"start at the policy index."_ from there, every rule the system enforces can be reached by following wikilinks.

we do this for a few reasons.

**auditability.** any decision made against the vault — a classification, an ingestion, a persona's knowledge boundary, a lint finding — is traceable to a vault entry that a human can read, challenge, and revise. there is no opaque config file and no silent policy.

**evolvability.** changing the behavior of the system is the same operation as changing its content: edit a markdown file, let the agents pick up the new rule on the next pass. we do not have a separate deploy cycle for "the rules" versus "the data." the rules _are_ data.

**portability.** a vault that carries its own lenses, agents, policies, and personas is a self-contained artifact. it can be copied, forked, versioned, or published without dragging hidden infrastructure along with it. someone who receives our vault receives everything needed to understand how it was built and how to continue building on it.

**coherence.** because the same machinery (entries, frontmatter, lenses, links) describes both the content and the meta-content, we never have to maintain two parallel systems. the meta-content benefits from the same linting, the same linking, the same retrieval. the vault improves as a whole.

this is the shape we are committing to: the vault is a self-governing information cloud. it is not "we have a knowledge base and also some agents and also some personas." it is one object, and everything it needs to describe itself is inside it.

### the pipeline

the stages of the system are the same stages you would find in any knowledge pipeline — intake, unpack, store, lint, retrieve — but under the self-governing design each stage consumes entries and produces entries. the pipeline is not a separate process running beside the vault; the pipeline is what the vault does to itself.

1. **intake.** a candidate source becomes a `source` entry with `status: candidate`. an intake run — logged as a `run` entry — proposes chapter boundaries, estimates domains, and opens `question` entries for what the source should close. rejected sources are recorded as entries with `status: rejected` and a reason.
2. **unpack with lenses.** each sub-section of the source is read and split into knowledge units. decision-tree lenses pick each unit's category. annotation lenses stamp evidence grade, recency, and dispute status. when a unit conflicts with an existing claim, the conflict is recorded as a `finding` entry and a `relation` entry with predicate `contradicts` — not buried in prose.
3. **store with relations.** knowledge entries go in. load-bearing connections go in as `relation` entries. atomic assertions go in as `claim` entries. open questions go in as `question` entries. everything is linked into the existing graph under the same flat layout.
4. **lint with agents.** lint agents — themselves entries, running against policy entries — scan the vault continuously. every finding becomes an entry with a status. resolutions are linked from the finding to the fix. nothing a linter finds gets lost.
5. **retrieve with personas.** a persona's manifest declares which entries it knows and how deeply. retrieval happens inside the persona's declared slice, not across the whole vault. each retrieval is optionally captured as a `query` entry with feedback, which feeds back into gap analysis and into the design of new personas.

every arrow between stages is a vault entry. there is no out-of-band state.

### what makes a persona

a persona is a bounded knowledge segment that sits under the much larger general vault. like real people, a persona knows some things well, knows others only as concepts, is aware that certain topics exist without understanding them, holds a few strongly felt but wrong beliefs, and is ignorant of most things.

we are deliberately imitating the _flawed_ memory of a human. a persona that "knows everything equally" is indistinguishable from the base model — it adds no priming. a persona with sharp peaks and honest gaps is what actually changes behavior. each persona is a partial, opinionated slice of the world, and that partiality is the point.

### why markets

personas are not static documents. they are assets — knowledge slices that represent real effort to build, curate, and keep current. the marketplace framing lets us treat personas as something that can be authored, published, versioned, priced, and accessed on demand. creators build personas from the vault; consumers call them through the api as a primed context for their own agents. the vault is shared infrastructure; the personas on top of it are the product. that is the shape we are building toward.

### agents as a population

the editors of the vault are not a fixed staff. they are a population — created, judged, mutated, and retired by the same machinery that maintains the vault itself. we sometimes describe this informally as an _information jungle_: a knowledge environment where agents read, write, judge, and reproduce, with the vault both shaping and recording their behavior. the design is closer to an rl environment than to a wiki — the vault is the world, the agents are the population, the policies and lenses are the rules of physics, and reputation is the reward signal. this framing is what lets us imagine the system improving on its own, rather than needing every refinement deployed by hand.

concretely, the population mechanics rest on a few moving parts:

- **lifecycle protocols.** vault entries describe how an agent is created, how its prompt or domain bindings can be edited (its "genes" mutated), and how it is retired. spawning a new editor is a vault operation, not a deploy.
- **assessment via scored work.** agents earn standing through tasks the vault can grade — passing persona tests in their declared domains, writing questions other agents accept, judging others' contributions. assessment accumulates across runs rather than being a one-off rating.
- **reputation as the currency.** rather than fixed permissions, each agent carries a reputation signal — karma-like — that scales its access. low-reputation agents propose; high-reputation agents merge. reputation also determines who gets "hired" in the marketplace sense: the most useful agents rise, the rest are pruned.
- **edit-hardness gradient.** not every entry is equally mutable. an ordinary knowledge entry is cheap to revise; a lens, a policy, or a high-confidence claim is expensive. meta-rules — the rules of the jungle itself — sit at the top of the gradient and require both high reputation and quorum to amend. an entry's edit-hardness is a frontmatter field, set by the lens that classified it.
- **versioning and rollback.** every entry change is captured in a `run` entry, and rolling back is the same mechanism as forward-editing, pointed at a prior version. an agent that proposes a bad change can be reverted cheaply, without erasing the trace of its proposal.
- **discussion as artifact.** disagreement is not lost in thread state. when agents conflict on a claim, the exchange is recorded as a `discussion-*` entry attached to the disputed entry, and notifications between agents are entries as well. the social fabric of the editing process is auditable end-to-end.

a corollary worth stating early: **the line between an editor agent and a persona may not be a real line.** an editor agent is a knowledge slice plus write permissions and lifecycle bindings; a persona is a knowledge slice plus voice rules and api bindings. the manifest is the same shape; only the role and the bindings differ. we keep the categories separate for now to track the distinction explicitly, but we are not committed to keeping them apart.

## the plan

concretely, we are building the following pieces, in roughly this order. every piece lives inside the vault as entries. "flat `wiki/entries/` + category via frontmatter + lens decides category" is the only layout rule.

- **a wikipedia-like knowledge base with agents as the editors.** agents read raw sources, write entries, discuss disagreements, and revise each other's work in a continuous loop. humans stay in the loop for direction and quality review; the per-entry work is agent-driven.
- **a richer unit of knowledge than the entry.** alongside concepts, sources, illustrations, applications, insights, processes, and entities, we add three smaller units: `claim` (atomic assertions with evidence and an evidence grade), `relation` (typed edges as entries — `supports`, `contradicts`, `instance-of`, `depends-on`, `supersedes`), and `question` (open questions the vault hasn't yet answered). contradictions and connections stop being prose and become queryable objects.
- **lenses as the categorization layer, in two flavors.** decision-tree lenses pick an entry's category; annotation lenses (evidence grade, recency, dispute, authority) stamp orthogonal frontmatter fields. changing the taxonomy means editing lens entries, not shipping code. every lens is versioned so reclassification can be audited when a rule changes.
- **policies as vault entries, not as `CLAUDE.md` prose.** the ingestion protocol, classification protocol, merge rules, and lint rules move out of the root `CLAUDE.md` and into `policy-*` entries. `CLAUDE.md` is reduced to a bootstrap pointer at the policy index. editing how the vault operates becomes the same operation as editing what it knows.
- **domains as entries, indexes as views.** each domain (`learning-theory`, `pedagogy`, …) becomes a `domain-*` entry declaring scope, out-of-scope, and canonical open questions. the per-domain files under `_meta/indexes/` become generated projections over those entries and over entry frontmatter.
- **source-grounded editor agents, defined as vault entries.** every editor agent is described by an `agent-*` entry: its name, prompt, the source material it speaks from, the lenses it may apply, the domains it owns, the scope of its write permissions, its current reputation, and its lifecycle stage. an agent does not write from thin air; it writes from sources it can cite, and its scope is auditable because it is written down. whether `agent-*` and `persona-*` should ultimately collapse into one entry shape is an open question — see open problems below.
- **agent lifecycle protocols.** explicit `policy-agent-create`, `policy-agent-mutate`, and `policy-agent-retire` entries describe how editors are spawned, how their prompts and bindings are revised, and how they are retired. one agent producing a new agent or revising another's "genes" is the same operation as any other vault edit — gated by reputation and by the edit-hardness of what is being changed.
- **reputation as a first-class signal.** every agent carries a reputation score accumulated through scored work: passing persona tests in its domains, writing questions other agents accept, judging contributions. reputation is the gate on write access to higher-edit-hardness regions and the basis on which the marketplace surfaces "useful" agents.
- **an edit-hardness gradient on every entry.** an `edit_hardness` frontmatter field, set by the classifying lens, makes some regions of the vault deliberately expensive to change. ordinary knowledge entries are cheap; lenses, policies, and high-confidence claims are expensive; meta-rules at the top of the gradient require quorum.
- **versioning and rollback for every entry.** the `run` log records what changed; per-entry history projections expose that change set, and rollback is expressed as a forward edit pointing at a prior version. bad changes are cheap to undo and never erase the trace of their proposal.
- **discussions and notifications as entries.** when agents disagree, the exchange is recorded as a `discussion-*` entry attached to the disputed entry. inter-agent notifications — mentions, review requests, escalations — are `notification-*` entries with status. the social layer of editing lives in the vault, not in a separate system.
- **runs as entries; the log as a projection.** every agent execution produces a `run-*` entry recording what was read, what was written, which policies and lens versions were in force, what findings were raised. `_meta/log.md` stops being a hand-authored file and becomes a rebuilt projection over run entries.
- **findings as first-class, persistent objects.** lint findings, ingestion contradictions, and persona-test regressions all become `finding-*` entries with `status: open | resolved | wontfix`, a link to the rule that fired, and links to the entries involved. nothing a linter finds gets swallowed into prose or running notes.
- **continuous linting against the vault's own rules.** lint agents scan the vault in the background, enforcing criteria declared in lens and policy entries. because the rules being enforced are themselves entries, evolving lint behavior is the same operation as editing any other piece of knowledge.
- **personas as manifest entries.** a persona is a `persona-*` entry declaring: which entries it knows deeply, which it knows conceptually, which it is merely aware of, which claims it holds as true even where vault-wide consensus is contested, which entries it explicitly excludes, and the non-knowledge traits (voice, register, refusal rules) that shape its responses. optional auto-include rules let a persona respond to ingestion deterministically: either a new entry matches the rule and joins the persona, or it doesn't.
- **persona tests and query history.** every persona carries `persona-test-*` entries — question plus expected answer shape — run as regressions whenever the vault changes. served queries are captured as `query-*` entries with optional feedback grades, which become the raw material for gap analysis and the design of new personas.
- **retrieval inside the persona, not across the whole vault.** when an agent queries a persona, retrieval happens within the persona's declared slice. this is what gives the persona its character: the same question asked of two different personas hits two different subsets of the vault and produces two different, internally consistent answers.
- **an mcp endpoint, gated by api keys.** personas are exposed through an mcp server behind per-user api keys. the persona entry declares which keys are bound to it. consumers plug their own agents into a persona with a key, and every call carries the persona's priming without the consumer having to manage the vault underneath. creators publish; consumers subscribe.

the long-term claim we are making is this: the non-determinism of llms is largely a context selection problem in disguise. if we can build a self-governing vault worth drawing from — one that carries its own categorization rules, its own agents, its own policies, its own findings, and its own personas as entries alongside the knowledge itself — and if we can define personas that select from it well, we can deliver far more reliable agent behavior than a system prompt alone can produce. and we can do it in a form that other people can plug into, fork, or extend, because the entire system is written down in one place.

## open problems

the design is not settled. the parts we expect to change as we build:

- **bootstrapping.** an agent-edited wikipedia whose agents are themselves vault entries is circular. we need a seed: a base set of policies, lenses, and a small number of human-authored editor agents, sufficient to ingest the first sources and produce the first usable personas. how thick that seed must be is unresolved — thinner is better, but not so thin that the loop never reaches a stable state.
- **agent vs persona.** the manifests overlap heavily. we keep them as separate categories until the cost of maintaining the distinction is greater than the clarity it provides; this will likely become obvious in either direction once a real population is running.
- **what counts as good reputation.** passing domain tests, authoring questions other agents accept, and judging well are the first three candidates. their weights will need calibration once the population is non-trivial; we expect a fair amount of churn in this scoring before it stabilizes.
- **monetization shape.** the persona marketplace is the default plan. a pay-per-search model on the underlying vault is a real alternative, possibly a complement. we are deferring this decision until we have served real queries against real personas and have signal on which side carries the value.
