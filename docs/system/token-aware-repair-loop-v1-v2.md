# Token-Aware Repair Loop v1/v2 (architecture)

The Repair Loop is the next core Overnight step after Real Test Execution + Snapshot/Rollback Proof v1.
It turns **test failures** and **review findings** into a controlled, token-aware repair workflow, and
governs whether the loop should continue, stop, or ask the user.

  Workers execute. Remedy governs. The Repair Loop decides what should happen next, tracks whether the
  Mission Contract is getting closer to done, and prevents unbounded/expensive/unsafe repair attempts.

This document describes the v1/v2 spine implemented in `packages/orchestration/repair_loop_v2.py`. It is
an **orchestration + metadata + evaluation** layer. It performs **no model execution, no worker
execution, no auto-apply, and no autonomous mutation**.

## The spine

```
Failure Artifact ─┐
                  ├─▶ Repair Work Item ─▶ Repair Context Pack ─▶ Route Recommendation ─┐
Review Finding  ──┘                          (token-aware)         (Worker Registry,    │
                                                                    Route Policy,       │
                                                                    Token Economy,      │
                                                                    Tournament)         │
                                                                                        ▼
            ┌──────────────── Candidate Intake (received ≠ repaired) ◀──────── external builder package
            ▼                                                                    / local candidate (existing rails)
   Candidate Quality ─▶ Review Gate ─▶ Apply Proof (existing approved path) ─▶ Re-Test Gate ─▶ Repaired
        (existing)       (reviewer        (do continue,                          (Real Test
                          PASS, not        approval-gated)                        Execution)
                          Done marker)
```

Each transition is evaluated by `evaluate_repair_loop`, which returns the current status, the required
next actions, optional future ideas, and a user-facing summary. The loop is **bounded** by the
`RepairLoopPolicy` (`max_attempts`, `max_retests`, `max_estimated_tokens_per_attempt`).

## Models

- **RepairLoopPolicy** — per-job bounds and gate requirements (`max_attempts`, `max_retests`,
  `max_estimated_tokens_per_attempt`, `require_reviewer_pass`, `require_tests_green`,
  `require_apply_proof`, `stop_on_repeated_failure`, `prefer_local_for_small_repairs`).
- **RepairWorkItem** — one thing to repair, derived from a failure artifact or a review finding. Carries
  only safe summaries, suspected file refs, and required evidence — never raw output.
- **RepairAttempt** — one attempt at repairing a work item: the route, the context pack, the candidate,
  and the candidate-quality / review / apply / re-test statuses, plus the token estimate band and the
  blocking reasons.
- **RepairLoopEvaluation** — the current evaluation of a work item: status, attempts count, whether the
  repair gate is satisfied, blocked reasons, required next actions, optional future ideas, and a
  user-facing summary.

## Token-aware context minimization

Token reduction is **first-class**. A repair context pack (`build_repair_context_pack`) includes ONLY:

- repair item safe summary
- failure artifact safe summary
- test command id + `output_ref` (never raw stdout/stderr)
- latest test status
- relevant review finding summary
- suspected file refs (minimal; only when already safely identified)
- mission acceptance criteria refs
- token estimate (from Token Economy)
- route recommendation

It NEVER includes full raw logs, full repo dumps, raw candidate output, or huge diffs. If the context
estimate exceeds the policy budget, the pack recommends **compression**. If the context is **unknown**,
the pack requires **context inspection or a human decision** — it never falls back to a blind cheap
route.

## Relationship to other subsystems

- **Real Test Execution** — the re-test gate consumes durable test run results
  (`real_test_execution.list_test_runs`). A failed/timeout latest relevant run blocks `repaired`; a
  passed run can satisfy the re-test gate. Tests are only run via the existing bounded runner, when the
  contract/policy explicitly allows it (bounded by `max_test_runs`). No automatic test runs.
- **Mission Contract** — required repair work items block mission satisfaction; repaired items can
  satisfy the repair gate; abandoned/blocked repairs create a user-decision-required signal.
- **Candidate Quality** — a candidate-quality PASS does not mean applied; the repair loop reads quality
  state but treats `candidate_received` and `quality_pass` as intermediate, not terminal.
- **External Builder Sandbox** — the external builder route produces a `external-builder package-create`
  next action (ingress), never provider execution.
- **Token Economy & Tournament** — route recommendation uses Token Economy estimates and (when present)
  Tournament evidence; an expensive/unknown route requires human-facing approval; small/cheap repairs
  may prefer a local/Ollama-capable route only when it is safe and available.

## Future adapters (NOT built in this block)

- **Claude / Pi / OpenCode / Ollama worker adapter** — a future Main Builder Adapter / Worker Control
  Plane. The Repair Loop only *recommends* routes and *suggests* external builder packages; it never
  executes a provider, model, or worker.
- **MemPalace** — a FUTURE external memory adapter / building block, NOT Remedy core and NOT built here.
  No internal long-term memory, embeddings, or vector DB is added.

## Anti-goals (explicit)

- No provider/model execution (Claude/Pi/OpenCode/Ollama/cloud/local model).
- No direct worker execution; no automatic candidate generation by a model.
- No auto-apply, no auto-approval, no autonomous repair mutation.
- No auto-PR / git automation; no real rollback restore.
- No MemPalace integration / internal long-term memory / embeddings / vector DB.
- No UI redesign; no MCP activation; no `shell=True`; no arbitrary command execution.
- **No fake "repaired" claim**: a work item is `repaired` only when the policy-required gates (reviewer
  PASS, re-test green, apply proof) are satisfied with durable evidence. A builder `Done:` marker is not
  a reviewer `Resolved`.
- **Token reduction principle**: never dump full logs, full repo context, raw stdout/stderr, or huge
  diffs into repair context; unknown/oversized context leads to compression or a human decision.
