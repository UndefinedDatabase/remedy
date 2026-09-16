# Repair Loop v1

Turn a real test failure into a bounded, safe, approval-gated repair **proposal**.
Repair Loop v1 never applies code, never runs tests, and never calls a provider.

Flow:

    TestFailureArtifact
      → Repair Context (safe summary)
      → Fix Task
      → Repair Artifact            (fixture builder, optional)
      → Fix Patch Intent           (real, resolvable, pending)
      → approval_required          (safe stop)

Canonical commands:

    remedy repair propose <job_id> <failure_artifact_id> [--fixture-builder] [--json]
    remedy repair status  <job_id> [--failure-artifact-id <id>] [--json]

## What `repair propose` does

- Runs `evaluate_repair_eligibility` (job, failure artifact, linkage, not-already
  -resolved, RunContract allows repair metadata actions).
- Builds a safe `RepairContextSummary` — command display, exit code, failure kind,
  bounded safe summary, related IDs, changed-file basenames, proof + snapshot
  status, bounded hints. No raw stdout/stderr, source, diff, artifact body,
  absolute paths, secrets, or tracebacks.
- Creates (or reuses) a **Fix Task** linked to the failure / test run / original
  task / intent / apply / repair attempt.
- With `--fixture-builder`, runs the deterministic fixture repair builder. For
  supported failure kinds it creates a **Repair Artifact** that yields a real,
  resolvable **Fix Patch Intent** (pending approval) and stops at
  `approval_required`. The next safe action is
  `remedy patch approve <job_id> <repair_intent_id>`.
- Without `--fixture-builder` it stops at `fix_task_created`.
- Unsupported failures (e.g. `timeout`, `collection_failed`, `unknown`) stop at
  `repair_builder_unavailable` — the Fix Task is still created.

**The proposal is a suggested fix, not an applied fix. You must approve it.**
Apply + test happen separately and approval-gated, via
`remedy patch apply <job_id> <repair_intent_id>` and then `remedy test run <job_id>`.

## Idempotency

A repeated `repair propose` for the same failure returns the **same** attempt —
no duplicate Fix Task, Repair Artifact, or Patch Intent. A resolved failure
blocks (`failure_already_resolved`). One RepairAttempt is persisted per
`(failure_artifact_id, source)` in job metadata.

## What it never does

- No `source_apply`, no apply, no test execution, no provider/Ollama.
- No automatic approval, no automatic contract relaxation, no automatic budget
  increase, no automatic revert.
- A pending repair is **never** marked verified. The repair Patch Intent shows as
  proposed / not applied / not verified in the Proof Chain until it is approved,
  applied, and tested.

## Fixture Repair Builder v1 — limitations

The fixture builder is deterministic and intentionally narrow. For supported
deterministic failure kinds (`test_failed`, `command_failed`, `assertion`) it
proposes a docs-only repair note (`docs/repairs/<failure>.md`, create, low risk)
— it does not yet rewrite source. It is meant for tiny repos / fixtures, not for
solving arbitrary code. Real-world repairs return `repair_builder_unavailable`
until a provider-backed builder is enabled.

## RunContract

Repair metadata actions are canonical and allowed by default for safe jobs:
`create_fix_task`, `create_repair_artifact`, `create_repair_patch_intent`. Apply
actions remain denied. If a contract denies repair actions, `repair propose`
blocks with a catalog-backed next action (`remedy job show <job_id> --full --json`).

## `repair start` (v0) vs `repair propose` (v1)

`repair propose` is the canonical v1 command (idempotent attempts, durable
`RepairAttempt`, fixture builder, approval-gated intent). `repair start` remains
as the v0 command for backward compatibility and is unchanged. New callers should
use `repair propose`.

## Approved Repair Apply Cycle (v1)

Once a repair patch intent is **approved** (`remedy patch approve <job> <intent>`),
apply it through the central apply service — there is no repair apply bypass:

    remedy patch apply <job_id> <repair_intent_id> --json
    remedy test run <job_id> --json
    remedy change proof <job_id> --json

> **Status (2026-09-16):** until F261 round 21 this was one word, the deleted
> `do continue`, taking the job id and the repair intent id, which ran
> eligibility → verified snapshot → apply → linked test → proof → truthful stop
> and then RECONCILED repair truth: a passing `source_fix` repair with a verified
> snapshot, complete evidence and verified proof resolved the original failure,
> and a failing one moved the attempt to `tested_failed` and linked the new
> failure artifact to the attempt and the prior failure. DECISION amend0905-vocab
> D4 deleted the command, and `reconcile_repair_after_continue` in
> `packages/orchestration/repair_loop.py` went with it because that command was
> its only production caller. The three commands above reproduce the apply, the
> test and the proof reading; NOTHING reconciles repair truth any more, so a
> repair attempt now stays `approval_required` and a failure is never marked
> `failure_resolved`.

Classification (`repair_kind` / `expected_effect`) distinguishes docs-only,
source-fixture, and (future) provider repairs. `repair status` shows the
classification and the apply state.

### Guarantees
- Repair Loop never applies code or runs tests itself (no `source_apply` /
  `patch_apply` / `test_execution` / provider imports). Apply only via the
  approved apply service. Snapshot mandatory. No auto-approve, no auto-revert,
  no auto repair loop.

## Product readiness (after this block)

End-to-end, with human approval at the gate, Remedy can now:
- run one controlled cycle (`do run` → propose), and on a failing test produce a
  real, bounded repair **proposal**;
- after the user approves the repair intent, apply it through `patch apply` and
  re-test it through `test run`; resolving the original failure needed the
  reconciliation F261 round 21 deleted with `do continue`.

Still requires a human:
- approving every patch/repair intent (`remedy patch approve`);
- enabling apply (contract `stop_before_apply=false`, apply permitted).

Still cannot happen automatically:
- applying without approval; auto-revert; an automatic repair loop / multi-cycle
  overnight run; provider/Ollama execution; contract relaxation; budget increase.

Future provider work:
- a gated, no-cloud-by-default provider repair builder for real source fixes
  (current fixture builder is docs-only unless an explicit safe source target is
  supplied).

## Future

A provider-backed repair builder (gated, no-cloud by default) will replace the
fixture builder for real source repairs.

## See also

- [bounded-overnight-prep-v0.md](../archive/bounded-overnight-prep-v0.md) — read-only readiness/report layer that surfaces repair attempts in its checklist + capability matrix.
- [provider-trust-gate-v0.md](provider-trust-gate-v0.md) — turns UNTRUSTED external model output into a pending Repair Patch Intent behind a trust gate (no provider execution); complements the deterministic fixture builder.
- [provider-patch-materialization-v0.md](provider-patch-materialization-v0.md) — materializes an accepted provider candidate (single `.md`) into a real applyable pending repair intent for `patch apply`.
- [repair-request-builder-v0.md](repair-request-builder-v0.md) — provider-agnostic repair request package for any external actor (output re-enters via provider intake).
