# runner — seed-phase stub

Per spec §26.6 and `policy-runtime`, `runner/` is the only enforcer of:

1. write-scope (does the agent's `slice.write_domains` cover the target's `domains`?)
2. reputation gates (does the agent meet the target entry's `edit_hardness` threshold?)
3. pending-changes routing (when gates fail, the write becomes a `pending-{run-id}-{target}` proposal)
4. per-entry advisory locks
5. `run-*` emission for every execution

It does **not** decide content (that is the agent's job), enforce lens criteria (lint agents do that), or decide promotion outcomes (discussions and quorum do that).

## what's here at seed

This directory is intentionally skeletal. During the seed phase, the **human reviewer plays the runtime role** for every edit-hardness gate and every quorum action — see [`docs/spec/specification.md`](../docs/spec/specification.md) §30.2.

What's checked in:

- **`run_emitter.py`** — a small helper that scaffolds a `run-*` entry given a kind, agent, reads, writes, and findings. Used by humans (and later, by agents) to record actions.

What's deferred (will land before seed agents are activated; tracked in spec §35.10):

- the write-interceptor that gates by `edit_hardness` and reputation
- the `pending-*` proposal routing
- the per-entry advisory lock manager
- the queue for over-budget runs
- the api between agent prompts and vault entries

## human-as-runtime checklist

When making a write to an entry whose `edit_hardness` is above `open` during seed:

1. Read [[policy-edit-hardness]] for the tier definitions and the agent-reputation thresholds the runtime *will* check.
2. Verify the change is within scope: the writing identity has at least one of the entry's `domains` in scope.
3. Apply the change manually.
4. Use `run_emitter.py` to produce a `run-edit-{slug}-{date}` entry recording reads, writes, and active policy/lens versions.

## why this is small at seed

The runtime is a load-bearing piece of infrastructure. Building it before there is a population of agents to gate would optimize for a specification that has not yet been pressure-tested. The plan is: ingest one source by hand (Phase 6), see which gates and locks actually matter in practice, then build the runtime to fit.
