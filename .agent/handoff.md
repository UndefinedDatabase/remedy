# Handback — F051 R1 (LARGE round, T001–T003)

## Range
`894375e..HEAD` · feature/f051-escalate-instead-of-block · 9 commits.
Base = main after the #164 merge. PR open, base `main`, **NOT merged**.
Verdict R1: **PENDING**. Closure and the integration gate are their own rounds.

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 Open PR Gate | done | exactly #164, `feature/docs-discoverability-amend`→`main`, non-draft → merged + branch deleted; list then empty |
| 2 branch | done | off main `894375e` |
| 3 three authored texts | done | all three sha256 matched first try, no rejoin |
| 4 claim + state commit | done | `d6b723b`; STATUS grep 1/0; docs gate 292 exit 0 right after |
| 5 inspection | done | map below |
| 6 T001 | done | `8b52454` + `da80634`; slice gate 36 + 475 green |
| 7 T002 | done | `4d92873` + `3bbadf7` + `f0bd12b`; slice gate 153 green |
| 8 T003 | done | `2756b09` + `1e7fbc2`; slice gate 26 green |
| 9 round gate | done | 182 · 292 · 42, all exit 0 (raw below) |
| 10 final commit + push + PR | done | this commit, PR created, not merged |
| 11 handback | done | this file + completion report |

## Authored-text verification — `sha256sum` output verbatim
    f705d2dc19bb275bf9e4589e2d91671c0fbc2fb2a96e1e7ba87d84045e283634  .agent/authored/f051-r1-1.md
    a07541e48bb64d631902c3578e6ee451a4425fac0cd0952bf082f2794f54fed9  .agent/authored/f051-r1-2.md
    2ae860a6ece29b057c12a3c79a08bf1ab0d6ce128723e55a7ee51788046c7f10  .agent/authored/f051-r1-3.md
All three equal their BEGIN-marker hashes; no transport fault in the authored
bytes. STATUS proofs: new `- [~] F051 …` grep -cF = **1**, old `- [ ] F051 …`
= **0**, diff on STATUS.md = +1/-1. `cmp` live_review vs f051-r1-2 → 0;
`cmp` plan vs f051-r1-3 → 0.

## Inspection map (item 5 — the seams built on)
| What | Where |
|---|---|
| Decision queue = read-only DERIVATION, not a mutable store | `packages/orchestration/decision_queue.py:56` `list_decisions` — 7 producer branches, each deriving from an existing record |
| Record type + registry | `decision_queue.py:26` `HumanDecision` (has additive `payload`), `:49` `DECISION_TYPES` |
| Enqueue call sites it derives from | plan approval: `decision_queue.py:236` off `job.flight_plan["_approval"]`; budget stops: `:158-211` off `job_stopped` events + `budget_guard`; patch approvals `:67`; stop reasons `:93` via `stop_reasons.derive_stop_reasons` |
| Answer CLI | `apps/cli/commands/decision.py:124` `_cmd_decision_resolve`, dispatching on the `sr:` / `fp:` id prefix; catalog entry `apps/cli/command_catalog.py:2334` `decision.resolve` |
| Executor batch boundary (F050) | `long_run_executor.py:862` per-cycle `ready_tasks` + `:891` the after-every-task recompute; `ready_tasks` at `:592`; in-run `blocked_ids` at `:835`; `TERMINAL_BLOCKED` → `JOB_BLOCKED`/`PAUSED` at `:94,:103,:114` |
| Status / report render | `apps/cli/commands/job.py:1522` `_cmd_job_status`, `:1604` `_cmd_job_report`, shared truth at `:1414` `_extract_job_truth` |

Two facts that shaped the design: (a) `RunState` has **no** awaiting/blocked
member, so awaiting had to be derived, not stored on the task — same reason
F050 keeps `blocked_ids` in the loop; (b) the queue derives, so "enqueue" =
write a record the queue reads. Records live on `job.metadata["escalations"]`
and are derived as `task_decision` — **no second queue, no new CLI group**.

## Commits
| Commit | Files | +/- | Note |
|---|---|---|---|
| `d6b723b` chore claim + state | `.agent/authored/f051-r1-{1,2,3}.md`, `.agent/{live_review,plan,last_block}.md`, `docs/roadmap/STATUS.md` | +235/-159 | STATUS `[~]` claim, state reset |
| `8b52454` feat T001 | `packages/orchestration/escalation.py` (new), `decision_queue.py` | +427 | records, enqueue, cross-refs, answering, awaiting derivation, assumption log; additive queue branch 8 + `task_decision` type |
| `da80634` test T001 | `tests/orchestration/test_escalation.py` (new) | +432 | 36 unit tests |
| `4d92873` feat T002 | `packages/orchestration/long_run_executor.py` | +189/-13 | `TaskAttempt.needs_decision`, `ready_tasks(awaiting_ids=…)`, `awaiting_downstream_tasks`, boundary re-check, blocked terminal, 4 additive `CycleRecord` fields, 2 additive result fields, 2 ledger events, `unattended` flag |
| `3bbadf7` test T002 | `tests/orchestration/test_escalation.py` | +489/-7 | three-branch fixture, pickup, check count, linear regression |
| `2756b09` feat T003 | `apps/cli/commands/job.py`, `decision_queue.py` | +114/-2 | open-decisions block first in status + report, `open_decisions*` view helpers |
| `1e7fbc2` test T003 | `tests/cli/test_open_decisions_view.py` (new) | +335 | 26 view tests |
| `f0bd12b` feat T002 | `apps/cli/commands/decision.py`, `tests/orchestration/test_escalation.py` | +119 | `td:` branch in the EXISTING `decision resolve` + 3 CLI tests |
| this commit | `.agent/handoff.md`, `.agent/last_block.md` | rewrite | handback, OUTCOME executed |

Every commit is under the 500-line limit. The first T001 attempt was staged as
one 859-line commit; it was **not** pushed and was split into `8b52454` +
`da80634` before any push, so no oversize commit exists in the history.

## Fixture pause/resume timeline (`make_fanout_job`: R → (B1a → B1b, B2, B3))
    boundary 1  awaiting {}      cycle 1  executed R
    boundary 2  awaiting {}      cycle 2  B1a raises needs_decision -> td:<b1a8>
                                          escalated 1, failed 0, executed []
    boundary 3  awaiting {B1a}   cycle 3  executed B2      (disjoint branch)
    boundary 4  awaiting {B1a}   cycle 4  executed B3      (disjoint branch)
    boundary 5  awaiting {B1a}   nothing ready -> terminal blocked,
                                 stop_reason "awaiting_decision; open_decisions=td:<b1a8>"
                                 job.state PAUSED (resumable), tasks_failed total 0
    answer via remedy decision resolve <job8> td:<b1a8> --reason "fast"
    resume      awaiting {}      executed B1a, B1b -> terminal all_green
    awaiting_checks 5 == cycles_run 4 + 1  (the no-polling proof)
Mid-run pickup, ONE run, no restart: R · B2 (answers the decision as a side
effect) · **B1a · B1b** · B3 → all_green — branch 1 rejoins in plan order at
the next boundary.

## Round gate — raw
    $ python3 -m pytest tests/orchestration/test_escalation.py \
        tests/orchestration/test_long_run_executor.py \
        tests/orchestration/test_dag_schedule.py \
        tests/cli/test_open_decisions_view.py -q
    182 passed in 0.65s
    EXIT=0

    $ python3 -m pytest tests/docs/ -q
    292 passed in 0.25s
    EXIT=0

    $ python3 -m pytest tests/cli/test_golden_path.py -q
    42 passed in 19.18s
    EXIT=0

Per-slice gates (all exit 0): T001 `test_escalation.py` 36 + the nine existing
decision-queue test files 475 passed / 2 skipped · T002 escalation +
long_run_executor + dag_schedule 153 · T003 `test_open_decisions_view.py` 26.
Extra regression I ran unasked, on every suite that touches status/report or
the queue (13 files): **707 passed, 2 skipped, exit 0**. `ruff check` clean on
every file I touched.

## Deviations & judgment calls — READ THIS
1. **`decision resolve` gained a `td:` branch** (`f0bd12b`). The block says
   reuse the queue and CLI "unchanged"; the acceptance criterion says answering
   happens "via the EXISTING decision CLI". Those cannot both hold literally:
   `_cmd_decision_resolve`'s else-branch REFUSES unknown prefixes, so a task
   decision would have been unanswerable. I extended the existing command
   additively (new `elif`, same command, `--reason` carries the answer) rather
   than adding a command or a queue. Reviewer call if you disagree.
2. **The mid-run assumption log is its own file**,
   `escalation_assumptions.md`, NOT the flight plan's `assumptions.md`. That
   log's own first paragraph states every question in it was asked at plan time
   and nothing mid-run; writing escalations into it would make it lie. Same
   table shape, same evidence dir.
3. **The status/report block is queue-wide, not task-decision-only.** A job
   with no repo attached already has an open `stop_reason` blocker, so it now
   also leads with the decision block and its `next_safe_action` is
   `remedy job attach-repo …`. That follows the feature text ("open decisions
   render FIRST") and is pinned by its own test, but it is a visible change for
   existing repo-less jobs — flagging it rather than hiding it.
4. **`blockers[0] = "awaiting_decision"`** fires for any open decision, not
   only task decisions (same reason as 3).
5. **T001's executor wiring landed in the T002 commits.** The block lists
   "enqueue" under T001; the enqueue FUNCTION and the queue derivation are
   T001, the call site inside `run_cycles` is `4d92873`. Splitting it the other
   way would have put an unreachable call site in T001.
6. **Not in this round's declared scope, needed before closure:** F051's
   feature file has no `## Built State` section yet (F050's does,
   `T1_F050.md:66`). The block's Change list excludes
   `docs/roadmap/features/T1_F051.md`, so I did not add it. No `docs/` ist-doc
   mentions the executor, so no index/ist-doc update is due.
7. One pre-existing `ruff` UP035 in `dag_schedule.py:36` (F050 code, typing vs
   collections.abc imports). Untouched — not my scope, no "while I'm here".
8. Two test expectations of mine were wrong and were corrected, not the code:
   the mid-run pickup order (branch 1 legitimately resumes ahead of B3, plan
   order) and the checkpoint assertion (a checkpoint written BEFORE the question
   was raised may name the task; the invariant only holds from the escalating
   cycle onwards).

## Open findings
2 open, both planning-routed carry-forwards: **R-0155** (Low), **R-0156**
(Medium). Next free ID: **R-0157**. No new findings raised by me — worker
never writes findings.

## Next expected action
Reviewer R1 verdict on the open PR. Then, as their own rounds: the F051 Built
State block, an integration-gate round per `docs/agents/integration_gate.md`,
and closure per `docs/roadmap/STATUS_closure_protocol.md`.
