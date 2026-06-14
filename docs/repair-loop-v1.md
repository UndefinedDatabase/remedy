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
Apply + test happen separately and approval-gated, in the next block via
`remedy do continue <job_id> --intent-id <repair_intent_id>`.

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
blocks with a catalog-backed next action (`remedy contract inspect …`).

## `repair start` (v0) vs `repair propose` (v1)

`repair propose` is the canonical v1 command (idempotent attempts, durable
`RepairAttempt`, fixture builder, approval-gated intent). `repair start` remains
as the v0 command for backward compatibility and is unchanged. New callers should
use `repair propose`.

## Approved Repair Apply Cycle (v1)

Once a repair patch intent is **approved** (`remedy patch approve <job> <intent>`),
apply it through the SAME safe continuation path — there is no repair apply bypass:

    remedy do continue <job_id> --intent-id <repair_intent_id> --json

`do continue` runs one cycle: eligibility → verified snapshot → apply (central
`apply_patch_intent`) → linked test (Test Execution Service) → proof → truthful
stop. After the cycle, repair truth is reconciled:

- **passed** → repair attempt `tested_passed`. The original failure is resolved
  **only** when the repair's `expected_effect == source_fix` AND the snapshot is
  verified AND the linked post-repair test passed AND proof is verified AND
  evidence is complete. A `documentation_only` / `unknown` repair is **never**
  claimed as a source fix, even if a test passes.
- **failed/timeout** → repair attempt `tested_failed`; the original failure stays
  open; a new failure artifact is linked to the repair attempt + prior failure.
  No automatic second repair loop.
- **degraded evidence** → `evidence_incomplete`; never resolved.

Classification (`repair_kind` / `expected_effect`) distinguishes docs-only,
source-fixture, and (future) provider repairs. `repair status` shows the
classification, apply state, and `resolved_failure`.

### Idempotency
Re-running `do continue` on a completed repair resumes from durable truth: no
second apply, no second test budget, no duplicate failure, no double resolve.

### Guarantees
- Repair Loop never applies code or runs tests itself (no `source_apply` /
  `patch_apply` / `test_execution` / provider imports). Apply only via the
  approved continue/apply service. Snapshot mandatory. No auto-approve, no
  auto-revert, no auto repair loop.
- A repair is never `verified` / `resolved` unless a linked test passes after the
  repair apply with a verified snapshot and supporting proof.

## Product readiness (after this block)

End-to-end, with human approval at the gate, Remedy can now:
- run one controlled cycle (`do run` → propose), and on a failing test produce a
  real, bounded repair **proposal**;
- after the user approves the repair intent, apply it through `do continue`,
  re-test it, update proof, and resolve the original failure **only** with
  verified evidence.

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

- [bounded-overnight-prep-v0.md](bounded-overnight-prep-v0.md) — read-only readiness/report layer that surfaces repair attempts in its checklist + capability matrix.
- [bounded-overnight-executor-v0.md](bounded-overnight-executor-v0.md) — the foreground one-step executor invokes THIS propose path (docs-only, no apply) when `--allow-one-cycle --allow-repair-propose` is given and all gates pass.
- [provider-trust-gate-v0.md](provider-trust-gate-v0.md) — turns UNTRUSTED external model output into a pending Repair Patch Intent behind a trust gate (no provider execution); complements the deterministic fixture builder.
