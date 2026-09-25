# Handback — F025 Pause/resume (global & per node) · Round 8

## Session

SESSION 2 of feature F025 · round 8 · rounds so far 8

The large majority of the session's context budget remained at the point this handback was
written. The round booked round 7's FAIL verdict (the ledger payload also carries round 7's
already-fixed R-1053/R-1054 Done lines), registered R-1056, then landed DECISION F025 D6 whole:
`paused` joins the manifest's status vocabulary
with its own lifecycle rows, `_park_job` and the task cap's own pause each record the parked
episode's manifest, three evidence-side readers found by M3's grep were widened to hold a paused
job to the same rule as a terminal one, and the end-to-end test now compares the manifest error
too instead of exempting it. No spec-impossibility was hit; constraint 4 was not invoked.

## Range

Review of 3f36bd811..HEAD

## Commits

### fe4c76932 F025 R8 C1a: copy round 8 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-r8-block.md | +176/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f025-r8-d6.md | +42/-0 | copy of the d6.md payload (DECISION F025 D6) |
| .agent/authored/f025-r8-ledger.md | +8/-0 | copy of the ledger.md payload (round 7's FAIL, R-1056) |
| .agent/authored/f025-r8-plan.md | +29/-0 | copy of the plan.md payload |

255 insertions by `git show --numstat` — the block's stated expectation (this block's own line
count, 176, plus 79: 42+8+29 = 79) — matches exactly.

### a7945b5a1 F025 R8 C1b: book round 7's FAIL, register R-1056, record D6
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +42/-0 | d6.md appended (bytes to bytes) |
| .agent/live_review.md | +8/-0 | ledger.md appended (bytes to bytes) |
| .agent/plan.md | +7/-7 | rewritten whole to the plan.md payload |

42/0, 8/0, 7/7 — matches the block's stated expectation exactly. `open_finding_ids` over
`.agent/live_review.md` at this commit reads `['R-1008', 'R-1055', 'R-1056']`, the reviewer's own
simulated reading.

### 09ebd31db F025 R8 C2: DECISION F025 D6 M1 — the paused status joins the manifest lifecycle
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/run_manifest.py | +28/-8 | M1: `paused` joins `_VALID_STATUS`; two new `_LIFECYCLE_MATRIX` rows (`pre_work_stop`, `worked`), each equal to the `stopped` row for that phase except `stop_request: False`; the comment above the matrix corrected; the two other `("completed", "stopped")` branches that are about an episode ending before completion (the published-reference zero-calls/coverage-completeness gate, and the terminal-snapshot-must-be-ok gate) widened to include `paused`; the `stop_request_id` rule (only a stopped manifest carries one) is untouched, as M1 orders |
| tests/orchestration/test_run_manifest_reference_coverage.py | +3/-1 | T2: `TestPublishedTerminalReferenceNeedsCompleteCoverage.test_incomplete_terminal_reference_is_rejected`'s `@pytest.mark.parametrize("status", ...)` widened from `["completed", "stopped"]` to add `"paused"` — the coverage-completeness gate M1 widened is now exercised for a paused reference too |
| tests/orchestration/test_run_manifest_writer_postconditions.py | +3/-1 | T2: `assert_canonically_readable`'s `if latest.status in ("completed", "stopped"):` gate (coverage-completeness + reference-validation postcondition, shared by every writer/recovery test in the file) widened to add `"paused"` |

34 insertions, under the cap. `python3 -m ruff check` clean.

### 16cca2693 F025 R8 C3: DECISION F025 D6 M2/M3 — parks write a paused manifest, evidence readers widened, T1
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | +27/-5 | M2: `_park_job` now captures the episode-start snapshot at `_PHASE_PRE_WORK_STOP` when not yet bound (mirroring `run_job`'s own pre-work-stop branch) and writes the parked episode's manifest under status `paused` through `_write_run_manifest_record`, before calling `park_job_pause` — a failed write is kept in `run_manifest_error`, the park proceeds regardless; the task cap's own pause (`run_job`'s `elif job.state == JOB_PAUSED`) now writes its own `paused` manifest exactly where the completion writes `completed`, since a max-tasks boundary carries no `job.pause` record and so has no other route to the manifest chain |
| packages/orchestration/job_evidence.py | +23/-17 | M3: the three readers found by grepping `packages/`, `apps/`, `scripts/` and `docs/` for a closed manifest-status set that actually branches on `RunManifestV1.status`/`JobPlan.state` and describes an episode ending before completion — `_crosscheck_job_episodes_vs_index`'s "terminal job's active episode is recorded" gate, `_crosscheck_terminal_jobplan_manifest`'s whole-field agreement gate (plus its now-generalized "carries stopped-only stop_request_id" message), and `_write_run_manifest_export`'s `mandatory`-manifest gate — each widened from `(JOB_COMPLETED, JOB_STOPPED)` to add `JOB_PAUSED`; full reader list and dispositions below |
| tests/orchestration/test_pause_manifest.py | +174/-0 | T1, NEW FILE: five scenarios reusing `test_pause_resume.py`'s fixtures by import — job-scope park mid-build, task-scope park in-flight, a job-scope pause requested before any work, the task-cap pause, and a paused manifest forged with a `stop_request_id` refused by the validator; each park scenario also proves the relaunch's completed manifest over two episodes (`paused` then `completed`) with an empty `run_manifest_error` |

224 insertions, under the cap.

### 66eaea5c5 F025 R8 C4: DECISION F025 D6 M4 — the end-to-end test compares the manifest error too
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_pause_e2e_live.py | +16/-6 | M4: `run_manifest.error`'s entry (and its reason paragraph) removed from `E4_REMOVED_FIELDS`, and `"error"` removed from `_normalized_export`'s hardcoded pop list, so it is now compared for real (both sides read empty); both `TestJobScopeE2ELive` and `TestTaskScopeE2ELive` gain an explicit assertion that the relaunched job's `run_manifest.error` is `""` and that `run_manifest.episodes` names exactly two episodes, `["paused", "completed"]` |

16 insertions, under the cap.

### 8556b9bb5 F025 R8 C5: the round's red-proof mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-r8-mutations.py | +243/-0 | the five named mutations (m1-m5), each FROM verified single-occurrence against the primary checkout before commit (see External actions) and re-verified live in a disposable worktree after; reuses `f025-r7-mutations.py`'s live-worktree-prep route (symlink `apps/ui/node_modules`, copy `apps/ui/dist` with mtimes bumped, never npm) since the e2e file it runs starts a real UI server |

243 insertions, under the cap.

### (this commit) F025 R8 C6: rewrite handoff for round 8
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured after this commit exists, in the final reply | this handback |

## External actions

- Read-only check of the mutation tool's five FROM patterns against the primary checkout's real
  files (m1, m4, m5 against `packages/orchestration/pingpong_job.py`; m2, m3 against
  `packages/orchestration/run_manifest.py`) before it was committed: each occurs exactly once, and
  each mutated form still parses as valid Python (`ast.parse`). No primary file was mutated by
  this check — the scratch check scripts lived under `.remedy-wt/f025-r8-worker/` (gitignored, per
  the block's own directory rule).
- `git worktree add --detach .remedy-wt/f025-r8-mut 8556b9bb5` (C5's HEAD) — succeeded, for G5's
  one official run against the committed tool.
- `python3 -B .agent/authored/f025-r8-mutations.py .../f025-r8-mut` — all 5 mutations caught, all
  restores byte-identical, both controls green first and last, final line `True`.
- `git worktree remove --force .remedy-wt/f025-r8-mut` — succeeded; `git worktree prune` —
  succeeded (no-op); `git worktree list` afterward shows only the primary checkout and the
  pre-existing worktrees found at session start — nothing new left behind.
- `git push origin feature/f025-pause-resume` — runs immediately after this commit (C6); its real
  outcome is reported in the final reply, since the handoff commit precedes the push.

No `gh pr create`, no `gh pr merge`, no other `gh` command this round (constraint 5: nothing is
merged). No `git stash`, no force-push, no checkout of another branch.

## Verification

```
$ ls .agent/STOP; echo "REAL_EXIT=$?"
ls: cannot access '.agent/STOP': No such file or directory
REAL_EXIT=2
(absent, as required — checked before step one)
```

```
$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f025-pause-resume
$ git log --oneline -1
3f36bd811 F025 R7 C6: rewrite handoff for round 7
```

```
$ (line count and sha256 of .remedy-wt/f025-r8/block.md, measured)
line_count: 176
sha256: 18dc08e38f59ad25e613b9608e5b1f078de6a046397b2de48be4ba07f569adf8
```
Matches both readings the delegation message gave exactly.

```
$ git worktree list
(reported: primary checkout + the pre-existing F015/F020/F023/F024/F025/F284 dry/sim worktrees
and several remedy/job-* worktrees already present at session start — left alone throughout, per
constraint 5)
```

### Payload transport (G1)

```
$ wc -l / sha256sum .remedy-wt/f025-r8/{d6.md,ledger.md,plan.md}
d6.md:     42 lines, 3553 bytes, e13bf1650d7984ace350cf6a0f011bc0b1980db6e44849e3ac32a50d0b345105
ledger.md:  8 lines, 6383 bytes, 7795684e9664648d965784c736e125e9f50384d12285b6ca7b5d7d3622a83fec
plan.md:   29 lines,  953 bytes, c957d58d7f273b049f2d855d5813db791ccce861a09ee0e92321ab042a6a37c8
```
Every payload's measured lines/bytes/sha256 matched the block's table exactly.

```
$ python3 -c "committed = git show HEAD:<path>; source = open(<src>, 'rb').read(); committed == source"
f025-r8-block.md  True (13542 bytes both sides)
f025-r8-d6.md     True (3553 bytes both sides)
f025-r8-ledger.md True (6383 bytes both sides)
f025-r8-plan.md   True (953 bytes both sides)
```
Each `.agent/authored/f025-r8-*` copy, read back with `git show fe4c76932:<path>`, is byte-identical
to its `.remedy-wt/f025-r8/` source (block copy included).

```
$ git diff --numstat -- .agent/plan.md .agent/decisions.md .agent/live_review.md   # staged, pre-C1b
42	0	.agent/decisions.md
8	0	.agent/live_review.md
7	7	.agent/plan.md
```
At C1b: `.agent/decisions.md` and `.agent/live_review.md` equal their `3f36bd81` bytes plus their
payloads (python `bytes + bytes`, confirmed by the exact numstat match); `.agent/plan.md` equals
`plan.md`'s bytes exactly (`shutil.copyfile`, confirmed by the 7/7 diff matching the two changed
paragraphs by hand-inspection above).

```
$ python3 -c "from scripts.rotate_live_review import open_finding_ids; print(open_finding_ids(open('.agent/live_review.md').read()))"
['R-1008', 'R-1055', 'R-1056']
```
Matches the block's stated reviewer reading exactly.

### G2 — the code

```
$ python3 -m ruff check packages/orchestration/run_manifest.py packages/orchestration/pingpong_job.py packages/orchestration/job_evidence.py tests/orchestration/test_pause_manifest.py tests/ui_server/test_pause_e2e_live.py tests/orchestration/test_run_manifest_reference_coverage.py tests/orchestration/test_run_manifest_writer_postconditions.py .agent/authored/f025-r8-mutations.py
All checks passed!
```

```
$ git diff --stat 3f36bd81 8556b9bb5 -- packages/orchestration/long_run_executor.py packages/orchestration/safe_points.py packages/orchestration/pingpong_loop.py packages/orchestration/checkpoints.py apps/ui docs/roadmap
(empty)
```

```
$ git diff 3f36bd81 8556b9bb5 -- packages apps scripts | grep -c "noqa: BLE001"
0
```

```
$ git diff --name-only a7945b5a1 8556b9bb5
.agent/authored/f025-r8-mutations.py
packages/orchestration/job_evidence.py
packages/orchestration/pingpong_job.py
packages/orchestration/run_manifest.py
tests/orchestration/test_pause_manifest.py
tests/orchestration/test_run_manifest_reference_coverage.py
tests/orchestration/test_run_manifest_writer_postconditions.py
tests/ui_server/test_pause_e2e_live.py
```
Every path is inside constraint 3's tracked set.

### G3 — the tests nearest the change

```
$ python3 -m pytest -q -p no:cacheprovider -rfEs tests/orchestration/test_pause_manifest.py tests/orchestration/test_pause_resume.py tests/orchestration/test_pause_resume_cycles.py tests/orchestration/test_job_stop_integration.py tests/orchestration/test_run_manifest.py tests/orchestration/test_run_manifest_prework_resume.py tests/orchestration/test_run_manifest_call_expectation_lifecycle.py tests/orchestration/test_run_manifest_reference_coverage.py tests/orchestration/test_run_manifest_terminal_consistency.py tests/orchestration/test_run_manifest_writer_postconditions.py tests/ui_server/test_pause_e2e_live.py tests/ui_server/test_pause_door_live.py tests/test_ble001_ratchet.py tests/cli/test_golden_path.py
235 passed in 128.46s (0:02:08)
```
Exit 0, zero SKIPPED lines.

```
$ python3 -m pytest -q -p no:cacheprovider tests/ui_server/test_pause_e2e_live.py
2 passed in 15.30s
$ python3 -m pytest -q -p no:cacheprovider tests/ui_server/test_pause_e2e_live.py
2 passed in 15.28s
```
The e2e file alone, twice more, serially, as ordered.

### G4 — the neighbours

```
$ python3 -m pytest -q -p no:cacheprovider tests/ui_server/test_command_channel.py
109 passed in 7.38s
```

```
$ python3 .remedy-wt/f025-r8/run_sel.py /home/decodeux/Repos/remedy 8
files 182 exit 1 wall 151 s
FAILED tests/cli/test_study_cmd.py::TestStudyRunWritesCards::test_study_run_writes_cards_for_a_fixture_repo
FAILED tests/cli/test_study_cmd.py::TestStudyRunWritesCards::test_study_run_defaults_path_to_cwd
FAILED tests/cli/test_study_cmd.py::TestStudyRunWritesCards::test_study_run_resolves_same_project_as_teacher_ask_via_registered_project
FAILED tests/cli/test_study_cmd.py::TestStudyRunWritesCards::test_study_run_warns_and_falls_back_when_no_project_registered
FAILED tests/cli/test_study_cmd.py::TestStudyRunRecordsStudyOnce::test_a_registered_project_gets_studied_at_and_studied_head
FAILED tests/cli/test_study_cmd.py::TestStudyRunRecordsStudyOnce::test_an_unscoped_study_writes_no_project_record
SKIPPED [1] tests/regression/test_named_bugs.py:383 ... (D3 quarantine, F252)
SKIPPED [1] tests/regression/test_named_bugs.py:392 ... (D3 quarantine, F252)
SKIPPED [1] tests/regression/test_named_bugs.py:399 ... (D3 quarantine, F252)
SKIPPED [1] tests/regression/test_named_bugs.py:295 ... (D3 quarantine, F252)
SKIPPED [1] tests/regression/test_named_bugs.py:312 ... (D3 quarantine, F252)
SKIPPED [1] tests/regression/test_named_bugs.py:321 ... (D3 quarantine, F252)
SKIPPED [1] tests/test_agent_tooling.py:43 ... (D12 quarantine, F252)
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257 ... (UI source not found)
SKIPPED [1] tests/test_install_smoke.py:175 ... (install smoke opt-in)
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441 ... (D3 quarantine, F252)
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484 ... (D3 quarantine, F252)
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507 ... (D3 quarantine, F252)
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543 ... (D3 quarantine, F252)
6 failed, 10364 passed, 13 skipped in 150.60s (0:02:30)
```
Exit 1, over 182 files (round 7's 181 plus T1). Matches the reviewer's `3f36bd81` reading exactly
except `+6 passed` (10358 → 10364): T1's 5 new tests plus the one new `paused` parametrize case in
`test_run_manifest_reference_coverage.py` (T2). The same six failures, all in
`tests/cli/test_study_cmd.py`, the known ordering class; the same 13 skipped.

```
$ python3 -m pytest -q -p no:cacheprovider tests/cli/test_study_cmd.py
12 passed in 0.63s
```
The failing file alone: `12 passed`, matching the reviewer's own stated reading of this known,
unrelated flake class exactly.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"name": "handler_import", "status": "pass"}, {"name": "live_review_verdict", "status": "pass"}, {"name": "plan_consistency", "status": "pass"}, {"name": "relevant_untracked", "status": "pass"}, {"name": "repo_root_hygiene", "status": "pass"}, {"name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true}
```
Six `pass`, `fail_count` 0.

### G5 — the red proofs

```
$ git worktree add --detach .remedy-wt/f025-r8-mut 8556b9bb5
Preparing worktree (detached HEAD 8556b9bb5)
$ python3 -B .agent/authored/f025-r8-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f025-r8-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f025-r8-mut
.../apps/ui/node_modules: symlinked from the primary checkout
.../apps/ui/dist: copied from the primary checkout, mtimes bumped +60s
CONTROL FIRST: control: exit=0 failed=0 failing=[(none parsed)]
m1 (_park_job writes no manifest): exit=1 failed=6
  failing=[test_pause_manifest.py::TestJobScopeParkMidBuild..., ::TestTaskScopeParkInFlight...,
  ::TestJobScopePauseBeforeAnyWork..., ::TestAPausedManifestRefusesAStopRequestId...,
  test_pause_e2e_live.py::TestJobScopeE2ELive..., ::TestTaskScopeE2ELive...]
  caught=True restored byte-identical=True
m2 (paused is removed from _VALID_STATUS): exit=1 failed=7
  failing=[...TestJobScopeParkMidBuild, ...TestTaskScopeParkInFlight, ...TestJobScopePauseBeforeAnyWork,
  ...TestTaskCapPause, ...TestAPausedManifestRefusesAStopRequestId, e2e::TestJobScopeE2ELive,
  e2e::TestTaskScopeE2ELive]
  caught=True restored byte-identical=True
m3 (the worked-phase paused row loses EXPECT_NOT_DISPATCHED): exit=1 failed=3
  failing=[...TestTaskCapPause, e2e::TestJobScopeE2ELive, e2e::TestTaskScopeE2ELive]
  caught=True restored byte-identical=True
m4 (the task cap's pause writes no manifest): exit=1 failed=1
  failing=[...TestTaskCapPause]
  caught=True restored byte-identical=True
m5 (_park_job's manifest write passes the pause request id as stop_request_id): exit=1 failed=6
  failing=[...TestJobScopeParkMidBuild, ...TestTaskScopeParkInFlight, ...TestJobScopePauseBeforeAnyWork,
  ...TestAPausedManifestRefusesAStopRequestId, e2e::TestJobScopeE2ELive, e2e::TestTaskScopeE2ELive]
  caught=True restored byte-identical=True
CONTROL LAST: control: exit=0 failed=0 failing=[(none parsed)]
packages/orchestration/pingpong_job.py: restored byte-identical: True
packages/orchestration/run_manifest.py: restored byte-identical: True
.../apps/ui/node_modules: removed
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```

```
$ git worktree remove --force .remedy-wt/f025-r8-mut
$ git worktree prune
$ git worktree list
(no f025-r8-mut entry; every pre-existing worktree still present, untouched)
```

## Authored-text proofs

`.agent/authored/f025-r8-block.md`, `f025-r8-d6.md`, `f025-r8-ledger.md` and `f025-r8-plan.md` were
built with `shutil.copyfile` from the reviewer's payload files — never retyped, never edited — and
G1 compared every one byte for byte, read back with `git show fe4c76932:<path>`, against its
source: all four BYTE-IDENTICAL. `.agent/decisions.md` and `.agent/live_review.md` were appended
with raw bytes read from `d6.md`/`ledger.md` (python `open(..., 'ab').write(payload_bytes)`), never
retyped; `.agent/plan.md` was rewritten whole from `plan.md`'s bytes via `shutil.copyfile`. G1's
numstat comparisons confirm all three match the payloads' expected insertion counts exactly.
`packages/orchestration/run_manifest.py`, `packages/orchestration/pingpong_job.py`,
`packages/orchestration/job_evidence.py`, `tests/orchestration/test_pause_manifest.py`,
`tests/ui_server/test_pause_e2e_live.py`, the two T2-widened test files and
`.agent/authored/f025-r8-mutations.py` are WORKER-authored production code, tests and the G5 tool
against DECISION F025 D6's own specification — not reviewer payloads — so no authored-text proof
applies to them.

## M3 — readers of a closed manifest-status set

Searched `packages/`, `apps/`, `scripts/` and `docs/` (excluding `docs/roadmap/`, `apps/ui/` and
build artifacts under `apps/ui/dist`) for `run_manifest`/`RunManifestV1`/`manifest.status`
references, then for each hit, whether it actually branches on a CLOSED set of manifest statuses
describing an episode's lifecycle (as opposed to importing a decoder, a redaction helper, or
referencing an unrelated field/vocabulary that happens to share a word like "completed").

**Widened** (all in `packages/orchestration/job_evidence.py`, landed in C3):
- `_crosscheck_job_episodes_vs_index`'s "a terminal job's active episode must be recorded" gate —
  `(JOB_COMPLETED, JOB_STOPPED)` → add `JOB_PAUSED`.
- `_crosscheck_terminal_jobplan_manifest`'s whole-field JobPlan/index/manifest agreement gate —
  same widening; its "carries stopped-only stop_request_id" message generalized to name the
  actual status rather than hardcoding "completed".
- `_write_run_manifest_export`'s `mandatory = terminal and marked` gate (the evidence export named
  by DECISION F025 D6 clause 4) — same widening.

**Read and left alone, with why:**
- `packages/orchestration/proof_chain.py` `_VALID_STATUSES` — a different vocabulary entirely
  (`verified`/`failed`/`incomplete`/`unverified`/`not_applicable`, the Proof Chain's own
  `proof_status`), not the manifest's lifecycle status.
- `packages/orchestration/runtime_integration_gate.py` — references `run_manifest.py` only as a
  file-path string for a static call-existence check (`f018_run_manifest_decode_budgets`); no
  status enumeration.
- `packages/orchestration/self_use_findings.py` — reads `run_manifest_error` as a non-blank string
  only; no status set.
- `packages/orchestration/rate_governor.py` — a comment naming a line number in `run_manifest.py`;
  no status set.
- `packages/orchestration/job_apply.py` — `apply_manifest.status` is `ApplyManifest`'s own field
  (`applied`/`blocked`), a different type from `RunManifestV1.status`.
- `packages/orchestration/pingpong_loop.py` — imports `FinalizedCallContext`/`on_call_finalized`
  for call finalization, not status; also out of scope by constraint 3 regardless.
- `packages/orchestration/call_identity.py`, `handoff.py`, `review_subject.py`, `run_report.py`,
  `manifest_schema.py`, `ci_stages.py`, `scripts/build_review_manifest.py` — each references
  `run_manifest.py` only for a decoder, a redaction helper, or a doc comment; no closed status set.
- `docs/system/vocabulary.md`, `docs/system/self-use-track-v1.md`,
  `docs/system/job-budget-enforcement-v0.md` — mention `run_manifest` fields but carry no closed
  status enumeration.
- `docs/roadmap/features/T0_F012.md` — DOES enumerate the closed set (`status (completed | stopped
  | planned)`, and again at lines ~706/773/1108/1324) and is now stale. Left alone: constraint 3
  forbids touching `docs/roadmap/`. Flagged below under Deviations as a known gap for the
  reviewer/closure sequence.
- The `apps/ui/*.ts`/`*.test.ts` files an early broad grep matched on the bare word "completed"
  (`brainView.ts`, `digestCardCopy.ts`, `jobDigest.test.ts`, etc.) — none of them import or read
  Python's `run_manifest` module (impossible across the language boundary); their "completed"
  refers to the UI's own job/task display state. Also out of scope by constraint 3 regardless.

## T2 — existing tests widened

- `tests/orchestration/test_run_manifest_reference_coverage.py::TestPublishedTerminalReferenceNeedsCompleteCoverage::test_incomplete_terminal_reference_is_rejected`
  — `@pytest.mark.parametrize("status", ["completed", "stopped"])` → add `"paused"`.
- `tests/orchestration/test_run_manifest_writer_postconditions.py::assert_canonically_readable` —
  `if latest.status in ("completed", "stopped"):` → add `"paused"`.

## Deviations & assumptions

1. **`docs/roadmap/features/T0_F012.md`'s closed status enumeration is now stale and was left
   untouched.** M3's own instruction is to widen every reader of a closed manifest-status set, and
   this doc names one (`status (completed | stopped | planned)`) several times; constraint 3
   explicitly forbids touching `docs/roadmap/`, so the two orders conflict for this one file.
   Resolved in constraint 3's favor (the narrower, explicitly-named prohibition), per AGENTS.md's
   "preserve scope discipline" tie-break rule. Not treated as constraint 4's "impossible as
   written" clause, because M1-M4 and the tests are all fully satisfiable without touching this
   doc — only M3's doc-reading half has one file it cannot act on. Flagged here for the reviewer;
   the fix (adding `paused` to this doc's own status list) belongs to a normal PR against
   `docs/roadmap/features/T0_F012.md`, not this round.
2. **Two existing tests widened beyond the block's literally-named files (T2).** T1 names only the
   new file; T2 orders "any existing test whose only edit widens a status set it pins to paused",
   found by inspecting the G3 test list for the same `("completed", "stopped")` shape M1 widened in
   production. Both are single-line-plus-comment edits (see the T2 section above and C2's table),
   verified passing before and after.
3. **No production file outside `run_manifest.py`, `pingpong_job.py` and `job_evidence.py` needed
   changing.** `long_run_executor.py`, `safe_points.py`, `pingpong_loop.py`, `checkpoints.py`,
   `apps/ui/` and `docs/roadmap/` are confirmed untouched by G2's `git diff --stat` (constraint 3).
4. **No full-suite run.** Per constraint 6 (amend0917 rule 1), only G3's and G4's targeted
   selections ran; the one full-suite run per feature belongs to F025's closure, not this round.

No payload was edited or retyped. The one worktree this round created (`.remedy-wt/f025-r8-mut`)
was removed the same round, per constraint 5; every pre-existing worktree was left alone.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 255 insertions, matches the block's expectation (176+79) exactly |
| C1b | done | 42/0, 8/0, 7/7 insertions, matches the block's expectation exactly; `open_finding_ids` reads `['R-1008', 'R-1055', 'R-1056']` |
| C2 | done | M1 landed (paused status + lifecycle rows + two widened validator gates) with T2's two widened tests; 34 insertions |
| C3 | done | M2 (`_park_job` + task-cap pause write `paused` manifests) and M3 (three `job_evidence.py` readers widened) landed with T1's five new tests; 224 insertions |
| C4 | done | M4 landed: `run_manifest.error` leaves `E4_REMOVED_FIELDS`, both scopes assert two episodes `["paused","completed"]` and an empty error; 16 insertions |
| C5 | done | 243 insertions; the G5 tool landed, its FROM patterns pre-checked against the primary checkout and against `ast.parse` |
| C6 | done | this handback |
| G1 | done | all payload and copy identity checks byte-identical; open-finding set matched at C1b |
| G2 | done | ruff clean over every changed .py file; the four do-not-touch files/dirs untouched; no new noqa: BLE001; name-only diff exactly inside constraint 3 |
| G3 | done | 235 passed, exit 0, no SKIPPED; e2e file alone green twice more |
| G4 | done | 109 passed (neighbour); 10364 passed / 6 failed (known flake, unrelated) / 13 skipped, exit 1 (selection + T1, 8 workers), matching the reviewer's baseline plus the round's own new tests exactly; the failing file alone reads 12 passed, matching the reviewer's own known reading; integrity check 6/6 pass |
| G5 | done | all 5 mutations caught, all restores byte-identical, `True`; officially run at C5's HEAD in a disposable worktree, which was then removed |
| G6 | done | reported in the final reply, after C6 and the push |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 8. Then F025's closure
sequence. Open findings: 3 — `R-1008` and `R-1055`, owned by F285, and `R-1056`, owned by F025 and
repaired this round — the count `open_finding_ids` reads at C1b. Operator questions open: 4 — the
count of `### Q` headings in `.agent/operator_questions.md` at C1b (unchanged this round).
