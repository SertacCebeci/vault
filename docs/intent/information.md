Question:
What does constitude as information

Answer:
“Information” usually means **data that has meaning to someone or something**.

A simple way to think about it:

- **Data** = raw facts or signals
  Example: `23`, `red`, `12:05`
- **Information** = data interpreted in context
  Example: “The temperature is 23°C” or “The traffic light is red”

Something constitutes information when it does at least one of these:

- **reduces uncertainty**
- **conveys meaning**
- **changes understanding**
- **can be used to make a decision**

Examples:

- A random number by itself may be just data.
- “Your package will arrive tomorrow” is information.
- A bell sound is information if it tells you class has ended.
- Even absence can be information: “No error messages appeared.”

In a broader sense, information can be:

- words
- numbers
- images
- sounds
- symbols
- patterns
- relationships between things

So, what constitutes as information is not just the content itself, but also **the context and interpretation**.

Your sentence is more naturally written as:
**“What constitutes information?”**

If you want, I can also explain it from:
**everyday use, philosophy, computer science, or Shannon information theory.**

Qestion:
So basically anything that reduces uncertanity is information

Answer:
Yes—**roughly speaking, yes**.

That is one of the strongest general definitions:

**Information is anything that reduces uncertainty.**

But there is a nuance:

- In **information theory**, that idea is very central.
- In **everyday language**, people usually also expect **meaning** or **usefulness**.

Examples:

- If I tell you “the coin landed heads,” your uncertainty about the coin flip is gone. That is information.
- If I give you a random string like `XQ-17B`, it may reduce uncertainty **only if** it matters in some context, like a password, code, or label.

So a better version is:

**Anything that reduces uncertainty for an observer, within some context, can count as information.**

Not literally “anything” in all cases, because without:

- a receiver
- a context
- interpretation

it may just be raw signal or data.

A compact distinction:

- **Signal** = something transmitted
- **Data** = recorded symbols/facts
- **Information** = data/signal interpreted in a way that reduces uncertainty

Your sentence corrected:
**“So basically, anything that reduces uncertainty is information?”**

And the answer is:
**Yes, with context and interpretation, that’s a very good definition.**

Question:
Assume correct answers given to some questions about a specific context. Answers to who and where question are orthogonal. Given somethin how to measure orthogonality of 2 questions

Answer:
Model it as **iterative uncertainty reduction over a latent task state**.

Your agent is not really “making the prompt denser” in a vague sense. It is trying to infer some hidden variable:

- the user’s true intent
- constraints
- preferences
- relevant world state
- success criteria

Call that hidden state (Z).

The initial user prompt is (P_0).
Each follow-up question-answer pair adds evidence:

- question (q_1), answer (a_1)
- question (q_2), answer (a_2)
- ...
- after (t) rounds, accumulated context (C_t = (P_0, q_1,a_1,\dots,q_t,a_t))

Then prompt enrichment can be measured as:

## 1. Information gain per pass

The cleanest measure is how much uncertainty about (Z) is removed by each answer:

[
IG_t = I(Z; a_t \mid C_{t-1}, q_t)
]

Equivalent form:

[
IG_t = H(Z \mid C_{t-1}) - H(Z \mid C_t)
]

Interpretation:

- high (IG_t): the question revealed something important
- low (IG_t): the question was mostly redundant

This is the most principled “density increase” measure.

## 2. Total enrichment after multiple passes

[
IG_{\text{total}} = H(Z \mid P_0) - H(Z \mid C_t)
]

This tells you how much the enriched prompt reduced uncertainty compared with the original prompt.

## 3. Information density

You probably also want **efficiency**, not just total gain. A very verbose agent may gather lots of info but waste tokens.

Define density as information gained per added token:

[
D_t = \frac{IG_t}{\Delta T_t}
]

where (\Delta T_t) is the number of tokens added in pass (t), usually the question plus answer, or only the answer depending on what you want to optimize.

And total density:

[
D_{\text{total}} = \frac{IG_{\text{total}}}{T(C_t)-T(P_0)}
]

This gives you a real “bits per token” style measure.

## 4. Redundancy penalty

Some follow-up questions produce answers already implied by earlier context. You want to penalize that.

Let the new answer be (a_t). Its non-redundant contribution is already captured by conditional mutual information:

[
I(Z; a_t \mid C_{t-1}, q_t)
]

If you want a direct redundancy score:

[
R_t = I(a_t; C_{t-1})
]

High redundancy means the answer overlaps a lot with what you already knew.

A practical usefulness score is:

[
U_t = \frac{I(Z; a_t \mid C_{t-1}, q_t)}{\Delta T_t}
]

This is likely your best per-question optimization target.

## 5. Task-performance view

If (Z) is hard to define directly, use downstream task success as a proxy.

Let (Y) be the ideal output or correct action. Then measure:

[
I(Y; C_t) - I(Y; P_0)
]

or more practically, improvement in:

- task accuracy
- judge score
- human preference
- constraint satisfaction
- success rate

This is often easier than estimating entropy over “true intent.”

## 6. Useful latent decomposition

Instead of one monolithic (Z), split it into components:

- (Z_I): intent
- (Z_C): constraints
- (Z_P): preferences
- (Z_E): evaluation criteria
- (Z_W): world/context facts

Then:

[
Z = (Z_I, Z_C, Z_P, Z_E, Z_W)
]

Now you can measure what each question extracted. For example:

- “What tone do you want?” mostly reduces (H(Z_P))
- “What exactly should be included?” reduces (H(Z_C)) and (H(Z_E))

This helps design specialized question policies.

## 7. Prompt densification as description length reduction

Another useful lens is MDL/compression.

A denser prompt is one that lets the model identify the right output with fewer plausible interpretations.

So define effective description length of the task after context (C_t):

[
L_t \approx H(Z \mid C_t)
]

Then good enrichment minimizes (L_t) with minimal token cost.

So your agent is solving:

[
\max \frac{H(Z \mid C_{t-1}) - H(Z \mid C_t)}{\Delta T_t}
]

at each step.

That is a formal “ask the most informative next question” rule.

## 8. Choosing the next question

The ideal next question is the one with highest expected information gain:

[
q*t^* = \arg\max*q \mathbb{E}*{a \sim p(a \mid q, C\*{t-1})}
\left[ I(Z; a \mid C_{t-1}, q) \right]
]

This is the key acquisition rule.

In words:

> Ask the question whose possible answers are expected to reduce uncertainty about the task the most.

If you also care about brevity:

[
q_t^\* = \arg\max_q \frac{\mathbb{E}[IG(q)]}{\mathbb{E}[\text{tokens}(q,a)]}
]

## 9. When to stop asking questions

Stop when marginal information density drops below threshold:

[
\frac{IG_t}{\Delta T_t} < \epsilon
]

or when expected task-performance improvement is too small.

This prevents over-enrichment.

## 10. Practical estimation, since true entropy is hard

In practice you usually cannot compute true (H(Z \mid C)). So estimate it with proxies:

### A. Posterior uncertainty over candidate task specs

Represent (Z) as a structured schema:

- goal
- output format
- constraints
- audience
- tone
- required facts
- exclusions

Have a model estimate a probability distribution over missing fields. Entropy over these fields approximates uncertainty.

### B. Ensemble disagreement

Generate several candidate interpretations of the task from current context. High disagreement means high entropy. After a new answer, disagreement should drop.

Examples:

- variance in generated plans
- variance in extracted schemas
- disagreement among judge models

### C. Output entropy

Sample multiple outputs conditioned on the current enriched prompt. If outputs differ wildly, the prompt is still underspecified. Enrichment should reduce this entropy.

### D. Success-on-heldout

For benchmark tasks where you know the correct target, measure how each added QA turn improves task success. That is an empirical information proxy.

## 11. A concrete framework for your agent

Define a task schema (Z) such as:

- objective
- audience
- format
- must_include
- must_avoid
- tone
- domain assumptions
- evaluation rule

At each pass:

1. Infer posterior over missing/uncertain fields.
2. Compute entropy for each field.
3. Generate candidate follow-up questions.
4. Estimate expected entropy reduction for each question.
5. Choose the question with highest expected gain per token.
6. Update posterior after answer.
7. Stop when residual entropy or gain-per-token is low.

Then your measurable metrics become:

- **total info gain**: reduction in schema entropy
- **density**: info gain per token
- **redundancy**: overlap with already known fields
- **utility**: downstream success improvement
- **efficiency**: gain per pass or per latency unit

## 12. A compact score you can actually use

A very usable score is:

[
\text{EnrichmentScore}_t =
\alpha \cdot \Delta H_{\text{schema}}

- \beta \cdot \Delta \text{TaskSuccess}

* \gamma \cdot \text{AddedTokens}
* \delta \cdot \text{Redundancy}
  ]

Where:

- (\Delta H\_{\text{schema}}): reduction in uncertainty over task schema
- (\Delta \text{TaskSuccess}): improvement in judged output quality
- AddedTokens: cost
- Redundancy: repeated information

This is often more implementable than pure Shannon math alone.

## 13. Best conceptual summary

The most correct information-theoretic framing is:

> Prompt enrichment quality is the reduction in uncertainty about the latent intended task, normalized by the cost of acquiring that reduction.

So the core measure is:

[
\boxed{
\text{Prompt Density Gain}
==========================

\frac{H(Z \mid P_0)-H(Z \mid C_t)}{T(C_t)-T(P_0)}
}
]

And the core decision rule is:

[
\boxed{
q^\*=\arg\max_q \frac{\mathbb{E}[I(Z;a\mid C,q)]}{\mathbb{E}[\text{token cost}]}
}
]

That is the right formal backbone for a multi-pass prompt enrichment agent.

I can turn this into a concrete system design next, with:

- a schema for (Z)
- a scoring algorithm
- pseudocode for question selection
- and an eval harness for your agent.
