# origin: from personal wikis to persona markets

this is the path that led to the project described in [intent.md](./intent.md). the intent doc describes what we are building and why, in terms of the final structure; this one describes how we arrived at that framing.

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

this is what we have been building toward: a large, high-quality knowledge base plus a strategy for selecting slices of it as context for specific problems. the shape of that knowledge base, and the mechanism by which slices are selected, is the subject of [intent.md](./intent.md).
