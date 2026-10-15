# Operator Cockpit v1

A read-only operator view of a Remedy job: top metrics, a task brain graph, a
process timeline, and a live right panel. It renders only evidence-backed truth
and never mutates anything.

Launch:

    remedy ui start <job_id>

By default `remedy ui start` binds all IPv4 interfaces, is token-gated, and serves the
built React app from `apps/ui/dist` (auto-built on first serve). The same tokenized
session is reachable through both `http://127.0.0.1:<port>/...` and
`http://<outer-ip>:<port>/...`; the session registry records both URL forms. Passing
`--host 127.0.0.1` keeps the cockpit loopback-only.

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
| `continuation` | approved intents | available (approved-intent light check) only; the last_result/last_stop_reason half, fed by `do_continue_stopped` events nothing writes since F261 round 21, was deleted by F273 (R-0919) |
| `overnight` | `build_overnight_readiness` (read-only) | readiness_level + ready/can_run_unattended + blocker_count + next-action label + checklist counts; `unknown` when data root unavailable; never a button |

F273 deleted the `repair` and `repair_request` sections (R-0926): they read the
repair-attempt store and the repair request packages, which nothing writes since
F261 round 22 deleted the `repair` group.

When the data root cannot be resolved, every derived value is reported as the
explicit string `"unknown"` (and the frontend renders `—`). Zeros are never
faked to stand in for unknown data.

## A project's missions

Every path below a project, `/api/projects/<slug or id>/...`, is answered by
`packages/orchestration/cockpit_project_routes.py` (DECISION F305 D2), token-gated like every
other read route:

| Route | Answer |
|---|---|
| `.../summary` | the project's card (F042) |
| `.../missions` | one card per mission of the project, newest first: goal, status, and how many orders and jobs it holds |
| `.../missions/<mission id>/orders` | that mission's newest 25 orders, newest first, with a count of the earlier ones |

Each order row names its title (the first line of the order's text), its job count, the calls and
tokens its jobs in this project made (from the project's token ledger, never a cost in US
dollars), and its chain: one chip per job of the order, in the order the jobs were linked. An
order given for several repositories at once is one batch in each repository's own mission, the
batches sharing a correlation id, so its chain also holds the jobs of the other repositories'
batches. A chip names a job by references and titles only: the job's id, its project, the folder
name of its repository, its title and its state. It never carries another project's evidence,
calls, tokens or paths. A project that does not exist answers 404 `project not found`, a mission
the project does not hold answers 404 `mission not found`, and a path that names no route answers
the server's own 404.

The right panel's **Missions** button opens the missions panel
(`apps/ui/src/components/missions/MissionPanel.tsx`, DECISION F305 D3) over the project the cockpit
shows. It lists the project's missions as cards; a card's orders are read only when the card is
opened. Each order shows its title, its calls and tokens and its chain band, and a click on a chip
opens that job in its own project's cockpit (`?project=<slug>&job=<job id>`). A chip whose job the
job store no longer holds or cannot read is shown and cannot be clicked.

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
- No "ask" input that puts a question to a model, no "+ Add Task" creator. The
  command bar is a local jump-to filter only. The one text input is the steering
  input at the bottom of the activity card, which records a steering message for
  the running job and never reaches a model call in flight; see
  [steering-user-guide-v1.md](../guides/steering-user-guide-v1.md).
- No demo/synthetic data path in normal operation.

## See also

- [do-continue-v1.md](../guides/do-continue-v1.md) — the deleted continuation cycle whose
  outcome used to feed the cockpit `continuation` section.
- [snapshot-rollback-v1.md](snapshot-rollback-v1.md) — the durable snapshot/apply
  truth behind the `snapshot` section.
- [repair-loop-v1.md](repair-loop-v1.md) — the repair attempts the deleted `repair`
  section used to surface.
- [bounded-overnight-prep-v0.md](../archive/bounded-overnight-prep-v0.md) — the read-only
  `overnight` readiness section (level/blockers/next action/checklist counts).
