# External Builder Sandbox v0 (Steps 1681–1716)

The first SAFE ingress for EXTERNAL builder work. Remedy can hand an external worker
(Claude / Pi / another agent / a human) a **safe request package**, and ingest the worker's result
— but that result stays **fully untrusted** until it passes the same quarantine → Trust Gate →
Verification → Materialization → human Approval → `do continue` path as a local candidate.

> **Worker execute. Remedy governs.**

## What External Builder Sandbox v0 IS

- an **untrusted candidate ingress** (a quarantined response intake),
- a **safe request-package exporter** (no secrets / raw logs / private paths / unbounded context),
- a **bridge layer** into the existing Trust Gate / Verification / Materialization /
  Candidate-Quality seams.

## What External Builder Sandbox v0 is NOT (anti-goals)

These are explicit non-goals and are enforced by architecture-guard + behavior tests:

- NOT an external agent runner — Remedy never *executes* the external worker.
- NOT a Claude / Pi / OpenAI / Ollama integration — no provider/model SDK, no model calls.
- NOT cloud provider execution.
- NOT MCP execution / activation.
- NOT auto-apply.
- NOT auto-approval / auto-reject.
- NOT auto-test.
- NOT auto-PR / git / merge.
- NOT browser automation.
- NOT automatic generation or repair loops.

## Security boundaries (testable)

1. **No execution surface.** The module imports no network/provider/subprocess/git modules; no
   `shell=True`; no apply/test/approve calls. (`test_*_architecture_guards`)
2. **Bounded, protected intake.** Candidate files are size-capped; binary / unreadable / symlink /
   path-traversal / protected-path inputs are rejected with safe structured errors — never a
   traceback. (`test_submit_*`)
3. **Untrusted by default.** A submission is never an approved intent and never "completed work";
   it is quarantined and must traverse Trust + Verification. (`test_submission_stays_untrusted`)
4. **No raw leakage.** Public package/submission summaries, CLI JSON, review bundle, scorecards and
   UI payloads contain safe IDs / counts / statuses / finding codes only — never the raw candidate,
   raw package context, diffs, stdout/stderr, tracebacks, secrets, or absolute paths. The raw
   candidate lives only in private quarantine (`raw_storage_ref` is an opaque id, never rendered).
   (`test_redaction_*`)
5. **Routing feedback is read-only.** External builder history can only raise/lower a confidence
   signal or recommend human review; it never starts a worker, never starts local generation, never
   applies/approves. (`test_routing_feedback_*`)
6. **Evidence, not claims.** Fake "tests passed" / fake proof claims in candidate text do not become
   truth; Candidate Quality ceilings (≤medium without verification, not excellent without
   proof_verified, rejected→low, pending≠completed) apply identically to external submissions.

## Flow

```
remedy external-builder package-create <job>      → safe request package (private record + safe summary)
   (relay package to an external worker — OUTSIDE Remedy)
remedy external-builder submit <package> --candidate-file <f> --source-label <s>
   → quarantine (private, bounded) → Trust Gate → Verification → Materialization (if passed)
   → pending repair intent (if supported) → approval_required (human)
remedy candidate-quality evaluate --intent-id ... (or via submission ids)
   → evidence-based scorecard (external route/source dimension)
remedy patch approve ... ; remedy do continue ...   (human-gated apply, unchanged)
```

## Future work (not built here)

- **Model/Route Tournament Harness v0** — controlled comparison of multiple generators/workers on
  the same request package + trust + verification + quality scoring. See
  [model-route-tournament-future.md](model-route-tournament-future.md).
- The external **worker contract** (request/response schema, forbidden content) is documented in
  [external-builder-worker-contract-v0.md](external-builder-worker-contract-v0.md).
