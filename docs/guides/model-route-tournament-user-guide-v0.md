# Comparing routes — Tournament user guide (v0)

This guide explains, in plain language, how Remedy compares worker **routes** and recommends one —
without running any model or spending money. It looks at what actually happened (the evidence) and
tells you which route earned trust for a given kind of task.

## What "Tournament" means here

A tournament is a **comparison**, not a race that runs anything. Remedy lines up the available
routes (local candidate, external builder, the human, the reviewer, and the not-yet-runnable
Ollama/cloud placeholders) and scores each one from durable evidence.

```
remedy tournament report <job_id> --json
remedy tournament show <tournament_id> --json
remedy tournament list <job_id> --json
```

## Why it does not run models

Tournament never calls a model, Ollama, a cloud provider, or runs a worker. It only reads evidence
Remedy already has. That keeps it safe, cheap, and honest: it can tell you a route *looks* good
without gambling on it.

## How Remedy compares routes

Each route gets a score band: **excellent**, **strong**, **usable**, **weak**, **blocked**, or
**insufficient evidence**. The signals come from:

- candidate quality (did its candidates have proof? get verified? get rejected?)
- token economy (estimated token/cost band, context fit)
- worker registry (cost tier, risk tier, whether approval is required)
- external builder submission history
- trust / verification / approval state

## Why cheap is not automatically best

A route can be cheap and still wrong. If a route keeps getting rejected or fails verification, a low
token cost does **not** lift its score — it stays weak or blocked. Safety and proof come first.

## Why proof beats model confidence

Remedy never believes a model that says "I tested it" or "this is correct". Only **durable proof**
(verification, proof chain, test state) lifts a route to strong or excellent. No proof → it cannot
be excellent, no matter how confident the route sounds.

## No winner when evidence is thin

If there isn't enough evidence, Remedy refuses to crown a winner. The report says
`insufficient_evidence` and points you at a safe way to gather more (e.g. run an external builder
package, or a local candidate) — it will not invent a "best model".

## How this prepares future routes

- When a real **Ollama** or provider adapter is added, its route can compete for real. Today those
  are placeholders and are only "usable for planning", never executable.
- Repeated tournament learnings are exactly what a future **MemPalace** memory layer will remember
  across runs. Today nothing is stored as long-term memory.

## What is *not* built yet

- Remedy does **not** run Ollama, cloud, or any model here.
- Token/cost numbers are **estimates** (bands), not billed measurements.
- No durable memory is stored yet.
- No automatic apply, approve, test, or PR — you stay in the loop.
