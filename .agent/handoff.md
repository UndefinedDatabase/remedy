# Handback — F279 Configuration & toolchain truth · Round 8 · Book round 7's PASS, write the feature file's Built State, generate and run the closure's self-use item, run the one full suite

## Session

SESSION 2 of feature F279 · round 8 · rounds so far 8

This round opened the closure sequence's first half: it booked round 7's
PASS into the ledger, appended the feature file's Built State
(`docs/roadmap/features/T2_F279.md`), generated the closure's self-use item
(`SU-028`, "Refresh the pinned toolchain", the order tier) and ran it to its
approval gate, and ran this feature's ONE full suite in the primary
checkout, committing its transcript. The suite came back RED with two bad
nodes — both pre-existing production-code shape checks
(`test_development_artifact_boundary.py::TestWhitelistBoundary::test_no_new_product_dependency`
and
`test_review_subject_resolution.py::TestProductionIsTheOnlyImplementation::test_the_env_var_is_read_in_exactly_one_module`)
— which is this feature's own work per constraint 4, not a reason to stop:
the transcript is committed exactly as measured. Context self-assessment:
the large majority of the session's working budget remains unused at
handback.

## Range

Review of `4f43baf6`..`HEAD`.

## Commits

### ef48fff2 F279 R8 C1: copy round 8 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f279-r8-block.md | +201/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f279-r8-built_state.md | +67/-0 | Payload copy |
| .agent/authored/f279-r8-ledger.md | +2/-0 | Payload copy |
| .agent/authored/f279-r8-plan.md | +32/-0 | Payload copy |

Measured insertions: 302 (block's line count 201 plus 101), matching the
block's formula exactly, well under the 500 cap.

### 6d1d89b3 F279 R8 C2: book round 7's PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | `ledger.md` applied: round 7's `Gate:` entry appended |
| .agent/plan.md | +11/-11 | Rewritten to the round-8 `plan.md` payload |

Measured insertions (`git show --numstat`): 2 live_review.md, 11 plan.md —
matching the block's expected counts exactly.

### 03d435e5 F279 R8 C3: write the feature file's Built State
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F279.md | +67/-0 | `built_state.md` appended: the feature file's Built State |

Measured insertions: 67, matching the block's expected 67 exactly.

### fbe843fb F279 R8 C4: generate and run the closure's self-use item, record its defects
| Path | +/- | Reason |
|---|---|---|
| scripts/self_use_queue.json | +8/-0 | `generate_and_append_if_empty()` appended `SU-028` (order tier) |
| .agent/selfuse_f279/SU-028.md | +66/-0 | NEW FILE: the generated item's job markdown |
| .agent/selfuse_f279/entry_and_job_file.txt | +5/-0 | NEW FILE: entry id/title/provenance/consumed_by, job file path |
| .agent/selfuse_f279/execution_config.txt | +39/-0 | NEW FILE: the returned `JobPlan.execution_config`, sorted-key JSON |
| .agent/selfuse_f279/full_transcript.txt | +39/-0 | NEW FILE: job id/title/state/stop fields, execution config, per-task summary |
| .agent/selfuse_f279/result_state.txt | +13/-0 | NEW FILE: job state, stop reason/source/request id, per-task states |
| .agent/selfuse_f279/run_defects.txt | +4/-0 | NEW FILE: `describe_self_use_run_defects()` output, verbatim |
| .agent/selfuse_f279/timing.txt | +3/-0 | NEW FILE: started/finished/created timestamps |

Measured insertions: 177 total (8 queue, 66 SU-028.md, 5 entry_and_job_file,
39 execution_config, 39 full_transcript, 13 result_state, 4 run_defects, 3
timing), well under the 500 cap. This commit also left behind
`.remedy-wt/job-e7a145761bf04f86` (worktree) and branch
`remedy/job-e7a145761bf04f86`, created by the self-use runner itself — see
External actions.

### (this commit) F279 R8 C5: record the closure suite transcript and rewrite handoff for round 8
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f279-closure-suite.txt | new file | The full suite's summary line, bad node ids and failure detail |
| .agent/handoff.md | rewritten | This handback, per `docs/agents/handback_template.md` |

## External actions

- `npm --prefix apps/ui run build` — ran once before the suite (G4/C5a); real
  exit 0, `git status --porcelain` stayed empty afterward.
- The self-use runner (`run_next_self_use_item`, called from C4(b)) itself
  created `.remedy-wt/job-e7a145761bf04f86` (a worktree at the primary
  checkout's C4 tip) and branch `remedy/job-e7a145761bf04f86`. Neither was
  created, touched or deleted by the worker directly — this is the run's own
  side effect (block constraint 7) — and both are left in place.
- `git push origin feature/f279-configuration-toolchain-truth` — runs after
  this commit; see the session's final reply for the real outcome.
- No `gh pr create`, no `gh pr merge`, no force-push, no `git stash`, no
  checkout of `main` or any other branch/commit in the primary checkout:
  none run, per constraint 6.
- `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`, their
  branches, and every pre-existing stash were left untouched. Nothing was
  deleted that this round did not create as scratch.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `ls: cannot access '.agent/STOP': No such file or directory`, absent — proceed.
- `git status --porcelain` → empty. `git branch --show-current` →
  `feature/f279-configuration-toolchain-truth`. `git log --oneline -1` →
  `4f43baf6 F279 R7 C4: rewrite handoff for round 7`. All three matched.
- Block bytes (R-0954): measured line count (newline count)=201,
  sha256=`d2b63ce2ca83ae2f77625c86d08b309a9bc9a252f243df922edcb6b24e3a0e01`;
  matches both readings given in the delegation message exactly.
- `git branch --list 'remedy/job-*'` before C1 → 39. `git worktree list`
  before C1 → primary checkout at `4f43baf6` plus
  `.remedy-wt/job-129b3ad7206d4f8d` (`09441a92`) and
  `.remedy-wt/job-e7268925db3a4831` (`cc8696a3`).
- `git stash list | head -1` →
  `stash@{0}: WIP on (no branch): 365051fa F277 R17 C3: rewrite handoff for round 17 with the rebuilt package readings`.

PAYLOADS — all 3 measured and matched the block's table exactly (line
count, byte count, sha256): built_state.md (67/5101/`1a8ba931d105432bbaa7ce1735dc336f868950d84e1c6bb7eb9c4309e94969d4`),
ledger.md (2/1873/`e63e3804210b257920edf5297efd48f6cd8d7db0efee4dd086a188614f07ff89`),
plan.md (32/1335/`f411ff3344534c575356e4bab176d521d3364fcdffb4d62f31b0fa6023c9ad2f`).

G1 TRANSPORT — every `.agent/authored/f279-r8-*` copy (4 files, including
the block copy) read back with `git show ef48fff2:<path>` and compared
byte-for-byte against its source (`.remedy-wt/f279-r8-block.md` for the
block, `.remedy-wt/f279-r8-payloads/<name>` for the other three): all 4
matched exactly.

G2 THE BOOKING AND THE BUILT STATE — read with `git show <commit>:<path>`:
`.agent/live_review.md` at C2 (`6d1d89b3`) bytes=388566
sha256=`9a55543b2b8aabcf092102d0b0358421a2a99aa19b8450d46248afe2cb7e99ca`
MATCH; `.agent/plan.md` at C2 bytes=1335
sha256=`f411ff3344534c575356e4bab176d521d3364fcdffb4d62f31b0fa6023c9ad2f`
MATCH; `docs/roadmap/features/T2_F279.md` at C3 (`03d435e5`) bytes=14071
sha256=`4bc6b25f4510d0c7bc9d518d2dd8305a2bdb9d08a4b3ae77f225956b08b3c8e8`
MATCH. Lines beginning `Gate: F279 R7 — ` at C2: 1, matching the block's 1
exactly. Open-finding-id set via `open_finding_ids`
(`scripts/rotate_live_review.py`), computed over `.agent/live_review.md`
text at `4f43baf6` and at C2: 26 and 26, both set differences empty —
matching the block's 26/26 exactly. `python3 -m pytest tests/docs/ -q` at
C3 → `322 passed in 84.92s`, real exit 0 (run again, since C3 writes a
roadmap file).

G3 THE SELF-USE ITEM — at C4: `generate_and_append_if_empty()` returned a
new `SelfUseQueueEntry` — id `SU-028`, title "Refresh the pinned
toolchain", provenance `generated (self-use-generator order tier,
docs/orders/toolchain-refresh.md, 2026-09-23)` — matching the reviewer's
dry-run reading exactly (same id, title and provenance shape, with today's
date, 2026-09-23, stamped in). `next_self_use_item()` answered the same
entry, `SU-028` / "Refresh the pinned toolchain". The runner
(`run_next_self_use_item(dest_dir=".remedy-wt/f279-r8-selfuse")`, no other
argument) planned and ran job `e7a145761bf04f86` to `job_file_path=
/home/decodeux/Repos/remedy/.remedy-wt/f279-r8-selfuse/SU-028.md`. Its
returned `JobPlan.execution_config`:
`builder=claude-cli` (source cli), `builder_model=claude-sonnet-4-6`
(source cli), `builder_effort=medium` (source cli), `reviewer=claude-cli`
(source cli), `reviewer_model=claude-sonnet-4-6` (source cli),
`reviewer_effort=medium` (source cli), `max_tasks=1` (source invocation) —
both roles resolved from the ONE `self_use` role configuration, the
configured frontier provider, never `fake` (DECISION amend0920-selfuse-real
D2). The job's own state came back `stopped` (`RunState.STOPPED`, not
`blocked`): `stop_reason=budget_exhausted:max_cost_usd`,
`stop_source=budget`, `stop_request_id=budget_6d405cad4c984bae` — the
REACTIVE budget-exhaustion safe point fired before T001's first provider
call was dispatched (T001's own `status` stayed `pending`, its
`final_status` reading `stopped`); no provider call was ever made and no
task ran. Elapsed wall time: 356.5s (`created_at`
2026-09-23T05:51:54.736173+00:00 to `finished_at`
2026-09-23T05:57:50.975338+00:00). `describe_self_use_run_defects(job)`
returned exactly two strings, verbatim:
`job e7a145761bf04f86 (stopped): stop_reason=budget_exhausted:max_cost_usd; stop_source=budget`
and `T001 (pending): final_status=stopped`. `python3 -m pytest tests/docs/
-q` after the queue file was written → `322 passed in 86.26s`, real exit 0
— matching the reviewer's stated `322 passed` at exit 0 exactly.
`git branch --list 'remedy/job-*'` before C1: 39; after C4: 40 (the runner's
own `remedy/job-e7a145761bf04f86`). `git worktree list` before C1: primary
checkout plus 2 `job-*` worktrees; after C4: primary checkout plus 3
`job-*` worktrees (the two pre-existing ones plus
`.remedy-wt/job-e7a145761bf04f86`).

G5 THE TREE — at C4, before the UI build and the suite: `python3 -m
apps.cli.main integrity check --json` → all 5 checks `pass`
(`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `high_blockers_open`), `fail_count` 0, `ok`/`passed`
true, real exit 0. `git status --porcelain` → empty, no untracked file.

G4 THE INTEGRATION GATE — UI build: `npm --prefix apps/ui run build` last
line `✓ built in 1.46s`, real exit 0; `git status --porcelain` afterward →
empty. `python3 -m pytest -n auto -q` in the primary checkout: real exit
code 1. Summary line: `2 failed, 18631 passed, 20 skipped, 1 warning in
244.23s (0:04:04)`. Bad node ids (2, the FULL list):
`tests/orchestration/test_development_artifact_boundary.py::TestWhitelistBoundary::test_no_new_product_dependency`
and
`tests/orchestration/test_review_subject_resolution.py::TestProductionIsTheOnlyImplementation::test_the_env_var_is_read_in_exactly_one_module`.
Neither `tests/orchestration/test_import_reachability.py` nor
`tests/test_no_orphan_modules.py` holds a bad node (closure precondition 7
answer: no). Full transcript committed at
`.agent/authored/f279-closure-suite.txt`; the raw log also sits outside the
repository at `~/remedy-gate-scratch/f279-r8-full-suite.log`.

G6 TREE AND PUSH — reported in the session's final reply, not this file,
since it runs after this commit (C5).

## Authored-text proofs

Fidelity protocol (docs/agents/split_workflow.md, R-0147/R-0144/R-0148):
byte-identity proof = mechanical disk-to-disk comparison of the applied
location against the `.agent/authored/` copy.

- This block (`f279-r8-block.md`): `.agent/authored/f279-r8-block.md` at C1
  verified byte-identical to `.remedy-wt/f279-r8-block.md` (G1) and to the
  two readings given in the delegation message.
- All 3 payloads (built_state.md, ledger.md, plan.md): each
  `.agent/authored/f279-r8-<name>` copy verified byte-identical to its
  `.remedy-wt/f279-r8-payloads/<name>` source (G1).
- `ledger.md` (append onto `.agent/live_review.md`, never retyped) and
  `built_state.md` (append onto `docs/roadmap/features/T2_F279.md`, never
  retyped): both by raw byte append (`open(path, "ab").write(...)`); the
  resulting on-disk digests MATCH the reviewer's stated G2 readings exactly.
- `plan.md` (rewrite, never retyped): by `shutil.copyfile`; the resulting
  on-disk digest MATCHES the reviewer's stated G2 reading exactly.
- No payload was retyped or edited anywhere this round.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 302 insertions, matches 201+101 formula |
| C2 | done | round 7's PASS booked, both insertion counts (2/11) match |
| C3 | done | Built State appended, 67 insertions matches, tests/docs/ 322 passed |
| C4 | done | SU-028 generated and run to the approval gate (stopped: budget_exhausted); defects recorded verbatim; tests/docs/ 322 passed |
| C5 | done | this commit — closure-suite transcript + handback |
| G1 TRANSPORT | done | all 4 authored copies byte-identical to source |
| G2 THE BOOKING AND THE BUILT STATE | done | all 3 digests match, 26/26 open-finding set empty diff, 1 Gate-line count matches, tests/docs/ green |
| G3 THE SELF-USE ITEM | done | SU-028 generated and run; execution_config confirms claude-cli/claude-sonnet-4-6 both roles; defects recorded; tests/docs/ green; branch/worktree counts recorded before/after |
| G5 THE TREE | done | integrity check 5/5 pass exit 0, tree clean, no untracked file |
| G4 THE INTEGRATION GATE | done (suite RED) | UI build exit 0; suite exit 1, 2 bad nodes, neither an import-reachability/orphan-module node; transcript committed |
| G6 TREE AND PUSH | done | reported in the session's final reply, since it runs after this commit |

## Deviations & assumptions

The round followed the block's ordered commit sequence (C1, C2, C3, C4, C5)
exactly and touched exactly the tracked path set constraint 3 names —
confirmed by `git diff --name-only 4f43baf6 HEAD` before this commit (the
paths given below, plus this commit's two files).

No oversize commit this round (largest was C1's 302 insertions, well under
the 500 cap; F279's one declared oversize commit remains round 1's
`constraints.txt`).

The self-use run's terminal state was `stopped` (reactive
`budget_exhausted:max_cost_usd`), not `blocked` as the block's prose names
generically ("a blocked job is an outcome to record, not a reason to
stop"). This is not a deviation from what the block ordered — the two
calls it specifies (`generate_and_append_if_empty()` with no arguments,
then `run_next_self_use_item(dest_dir=...)` with nothing else) were made
exactly as written, and the run reached its approval gate and stopped
there, never applying anything, per the runner's own contract. The
resulting state is reported here in full rather than assumed to be
"blocked": zero provider calls were made, so no provider transcript exists
to save beyond what `full_transcript.txt` already carries (job/task-level
fields).

The full suite (C5) came back RED with 2 bad nodes,
`test_development_artifact_boundary.py::TestWhitelistBoundary::test_no_new_product_dependency`
and
`test_review_subject_resolution.py::TestProductionIsTheOnlyImplementation::test_the_env_var_is_read_in_exactly_one_module`.
Per constraint 4 this is this feature's own work, not a reason to stop: the
transcript is committed exactly as measured, both node ids are reported
above and in `.agent/authored/f279-closure-suite.txt`, and no test was
weakened, deleted or marked xfail to reach this reading. The repair round
is the reviewer's to order.

No sandbox friction beyond the block's own anticipated shapes: every
measurement and generation script was written to a file under
`.remedy-wt/f279-r8-scratch/` and run with `python3 <file>` or `bash -c`,
never as an inline heredoc or `VAR=x cmd` shape; no payload was retyped or
edited; no shell `for` loop or chained `cd ... &&` was used (a python loop
substituted where a shell loop would otherwise have been reached for).

No other procedural deviation. Nothing was merged this round, no PR was
created, no STATUS or README edit, no `consumed_by` edit, no review zip, no
evidence job, no checkout of `main` — all per constraint 6.
`.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831` and
their branches were left untouched; the self-use runner's own
`.remedy-wt/job-e7a145761bf04f86` and `remedy/job-e7a145761bf04f86` were
left in place per constraint 7 (not created as scratch by the worker, and
never deleted).

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 8,
then the closure sequence's second half: the registrations the self-use
defects ask for (`job e7a145761bf04f86 (stopped):
stop_reason=budget_exhausted:max_cost_usd; stop_source=budget` and `T001
(pending): final_status=stopped`), the repair the suite's two bad nodes
require, the evidence job and the review zip, and then the closing round:
the ledger rotation, the STATUS line with the README counters in the same
commit, and the pull request. Open findings: 26. Operator questions: 0.
