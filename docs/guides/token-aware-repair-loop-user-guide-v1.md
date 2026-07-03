# Token-Aware Repair Loop — user guide (v1)

This guide explains, in plain language, how Remedy turns a test failure or a review finding into a
controlled repair, and what it does and does **not** do automatically.

## How test failures become repair work

When an allowed test fails, Remedy records a safe Test Failure Artifact (a summary + an `output_ref`,
never raw logs). You can turn that into a **repair work item**:

```
remedy repair item-create-from-failure <failure_artifact_id> --job-id <job_id> --json
remedy repair item-create-from-review <finding_id> --job-id <job_id> --json
remedy repair item-list <job_id> --json
remedy repair evaluate <repair_id> --json
```

A review finding can also become a repair work item — but only when it is an **open** Blocker/High/Medium
finding. A finding that the reviewer marked `Resolved` (or one that only has a builder `Done:` marker but
is not `Open`) does **not** create a required repair item. A `Done:` marker is not a reviewer `Resolved`.

## Why Remedy minimizes context

Repair is expensive when you dump everything into it. Remedy builds a **minimal, token-aware** context
pack:

```
remedy repair context-pack <repair_id> --json
```

It includes only the safe failure summary, the test command id, the `output_ref`, the latest test
status, the relevant review finding summary, suspected file names, mission acceptance refs, a token
estimate, and a route recommendation. It never dumps full logs, full repo context, raw stdout/stderr, or
huge diffs. If the estimate is too large it recommends **compression**; if the context is **unknown** it
asks for context inspection or a human decision — it never falls back to a blind expensive route.

## Why candidates are not automatically trusted

A repair candidate (from an external builder, or a future local generator) is **untrusted** until it is
reviewed. Remedy is explicit about this:

- **candidate received ≠ repaired**
- **candidate-quality pass ≠ applied**
- **applied ≠ repaired** until the re-test passes

```
remedy repair route-recommend <repair_id> --json
```

The route recommendation respects your Worker Registry, Route Policy, and Token Economy. A small, cheap
repair may be recommended for a safe, available local route; an expensive or unknown route requires your
approval; an external builder route produces a `external-builder package-create` action (ingress only) —
Remedy never executes a provider, model, or worker.

## Why review and re-test gates matter

A repair is only `repaired` when the policy-required gates are satisfied with durable evidence: a
reviewer pass, an apply proof (through the existing approval-gated apply path), and a green re-test. You
control the bounds:

```
remedy repair policy-show <job_id> --json
remedy repair policy-set <job_id> --max-attempts 3 --max-retests 3 --require-reviewer-pass true --json
```

If a repair hits its maximum attempts or re-tests, Remedy stops and asks you to decide — there is no
infinite loop and no automatic mutation.

## What is not automated yet

- No model/provider execution (Claude/Pi/OpenCode/Ollama/cloud/local model).
- No automatic candidate generation by a model; no direct worker execution.
- No auto-apply, no auto-approval, no autonomous repair mutation, no auto-PR.
- No real rollback restore (snapshot/rollback proof stays metadata-only).
- No external memory adapter (MemPalace), no internal long-term memory, no embeddings.

## How this moves Remedy toward overnight autonomy

The Repair Loop is the spine the future **Worker Control Plane** will plug into: Remedy already decides
*what* should happen next, *how small* the context should be, *which* route is justified, and *whether*
the Mission Contract is getting closer to done — safely, and without overclaiming autonomy. The next step
is a real builder adapter that executes the route Remedy recommends, still behind the same review and
re-test gates.
