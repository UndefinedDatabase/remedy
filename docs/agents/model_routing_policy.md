# Model Routing Policy (seed for F110, gated by F082)

> Policy document, NOT a prompt segment. Seeds routing.py's class→model map
> and defines when a cheaper/local model may be promoted into a task class.
> Applies uniformly to local endpoints (Ollama/vLLM, F113) and external
> builders (Claude Code, Copilot, API models).

## Seed mapping (initial, per-project overridable)

- format / extract / summarize / boilerplate → cheap tier (local allowed)
- standard build / standard review → mid tier
- architecture / mission / vision / prompt authoring for other agents → top tier
- Repair prompts follow the tier of the original task class.

## Hard rules

1. Reviewer never weaker than the paired worker for the same task
   (equal allowed, stronger preferred). A weak reviewer passing a weak
   worker compounds errors.
2. No silent downgrade of security-relevant roles (F110 anti-goal).
3. routed_model + reason land in evidence for every call (F110).

## Promotion rule (evidence over claims, P1)

A model may be promoted into a task class only after a documented benchmark
run on the F082 corpus (or the class's frozen fixtures):
- each fixture run 3× (small models are high-variance),
- pass thresholds: ≥90% on block-level assertions, ≥75% overall,
- logged per run: model id + quantization, prompt hash, tokens, cost,
  assertion results, reviewer verdict.
Below threshold, the class stays on the stronger tier. Re-run on model
version change or material prompt change. The log doubles as Remedy's
public "measured, not claimed" evidence base.

## Honest ceiling

Conventions + routing raise a local model's floor (less fabrication, cleaner
reports, measurable quality). They do not raise its ceiling to a frontier
model. Heavy reasoning classes stay routed to the top tier until the
promotion rule proves otherwise.
