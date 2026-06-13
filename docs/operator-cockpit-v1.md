# Operator Cockpit v1

A read-only operator view of a Remedy job: top metrics, a task brain graph, a
process timeline, and a live right panel. It renders only evidence-backed truth
and never mutates anything.

Launch:

    remedy ui start <job_id>

The server binds `127.0.0.1` only, is token-gated, and serves the built React
app from `apps/ui/dist` (auto-built on first serve).

## Scope

- **Read-only.** `POST`/`PUT`/`DELETE` return `405`. There are no mutation
  endpoints and no buttons that execute anything. The only "actions" copy a safe
  CLI command to the clipboard for the operator to run themselves.
- **No raw content.** The payload and UI carry counts, booleans, safe enum
  labels, safe file basenames, and opaque IDs only — never diffs, stdout/stderr,
  tracebacks, absolute paths, recovery blobs, secrets, or raw prompts.
- **No fabricated state.** Nothing claims a state it has no evidence for: the
  LIVE pill is shown only when the backend reports a running job; the agent card
  says Idle/Needs your decision/Blocked rather than inventing activity; the task
  checklist renders exactly the real tasks; decorative graph dots are
  non-interactive and never counted.

## Data sources (authoritative only)

The dashboard payload (`_build_dashboard` in `packages/orchestration/ui_server.py`)
derives the cockpit truth sections from authoritative sources:

| Section | Source | Notes |
|---|---|---|
| `metrics.tests` | `test_run_completed` events | runs/passed/failed/latest_state; missing `exit_code` is uncounted, never a fake fail |
| `metrics.proof` | `build_proof_chain` (authoritative) | total_changes vs verified; state verified/partial/none |
| `snapshot` | `build_snapshot_truth` over `list_durable_apply_ids` | apply_records/verified/reverted/drift_detected; `source = durable_apply_records` |
| `continuation` | `do_continue_stopped` events + approved intents | available (approved-intent light check) + last_result/last_stop_reason (safe enums) |

When the data root cannot be resolved, every derived value is reported as the
explicit string `"unknown"` (and the frontend renders `—`). Zeros are never
faked to stand in for unknown data.

## Frontend truth contract

- `apps/ui/src/api/remedyApi.ts` maps the payload to typed view models;
  unresolved/unknown backend values become `"—"`/`"unknown"`, never invented
  numbers.
- Cockpit decision logic lives in `apps/ui/src/cockpitLogic.ts` (pure, CSS-free,
  unit-tested): `liveIsActive`, `deriveAgentStatus`, `selectChecklistRows`.
- The graph model (`buildForceBrainModel.ts`) marks decorative `layout_only`
  dots `clickable: false`, paints no pointer hit-area for them, caps them at 90,
  and never counts them; `n` real tasks yield exactly `n` clickable nodes.

## Deliberately NOT included

- No approve/reject/apply/revert/run controls — those remain CLI + central
  services, gated by permission/contract/snapshot/test policy.
- No chat or "ask" input, no "+ Add Task" creator. The command bar is a local
  jump-to filter only.
- No demo/synthetic data path in normal operation.

## See also

- [do-continue-v1.md](do-continue-v1.md) — the continuation cycle whose outcome
  feeds the cockpit `continuation` section.
- [snapshot-rollback-v1.md](snapshot-rollback-v1.md) — the durable snapshot/apply
  truth behind the `snapshot` section.
