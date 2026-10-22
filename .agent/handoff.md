# Handback — F074 round 3: the closure's integration gate — Acceptance, consolidation, self-use, one full suite

## Session

SESSION 1 of feature F074 · round 3 · rounds so far 3

Context self-assessment: this worker checked both prompt digests and every prepared file's digest
before any write, byte-copied every C1-C3 file with a disk-to-disk equality proof, ran the self-use
item and the full suite exactly once each through the prepared launch/wait helpers with no overlap,
and context stayed ample throughout.

Fortschritt: ~80 % (T001 to T003 landed; the Acceptance, the consolidation pass, the self-use run and
the one full suite done · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `6b865ba74`..`HEAD` on `feature/f074-estimate-calibration`.

## Commits

### 716440d67 F074 R3 C1: book round 2, the plan, the block and the self-use script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f074-r3.md` | +164/-0 | NEW FILE, this round's block, byte copy of `block.md` (sha256 `e086bac8...4479e1d3`) |
| `.agent/authored/f074-r3-selfuse.py` | +127/-0 | NEW FILE, reviewer-authored self-use runner script for C4, never edited |
| `.agent/live_review.md` | +2/-0 | round 2's PASS verdict booked |
| `.agent/plan.md` | +5/-4 | rewritten for F074 round 3 |

### 1e2f2ad85 F074 R3 C2: the Acceptance held on one project's calibration, read by all three consumers
| Path | +/- | Reason |
|---|---|---|
| `tests/regression/test_f074_acceptance.py` | +132/-0 | NEW FILE, the feature's Done line: one project's calibration read by the plan-band rows, the predictive stop, the cost preview and `remedy stats calibration`; the thin class honestly on defaults |
| `docs/system/estimate-calibration-v1.md` | +4/-2 | status banner names the Acceptance test |

### c482b8ec2 F074 R3 C3: the checklist's consolidation pass for F074
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +5/-0 | F074's consolidation paragraph; the checklist stays at 34 items |

### a5c62ff9e F074 R3 C4: the closure's self-use item run to its approval gate, never applied
| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8/-0 | one appended entry, `SU-076`, `consumed_by` empty |
| `.agent/selfuse_f074/SU-076.md` | +17/-0 | NEW FILE, the job markdown the generator produced |
| `.agent/selfuse_f074/changed_paths.txt` | +2/-0 | NEW FILE |
| `.agent/selfuse_f074/entry_and_job_file.txt` | +5/-0 | NEW FILE |
| `.agent/selfuse_f074/execution_config.txt` | +43/-0 | NEW FILE |
| `.agent/selfuse_f074/full_transcript.txt` | +14/-0 | NEW FILE |
| `.agent/selfuse_f074/job_diff.txt` | +27/-0 | NEW FILE |
| `.agent/selfuse_f074/result_state.txt` | +12/-0 | NEW FILE |
| `.agent/selfuse_f074/run_defects.txt` | +1/-0 | NEW FILE, `NONE` |
| `.agent/selfuse_f074/staleness_after.txt` | +2/-0 | NEW FILE |
| `.agent/selfuse_f074/timing.txt` | +3/-0 | NEW FILE |

### ca0ed9fd2 F074 R3 C5: the closure's one full suite and its CPU cost
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f074-closure-suite.txt` | +28/-0 | NEW FILE, the one full-suite transcript and its CPU cost reading, shaped like `f113-closure-suite.txt` |

## Item status

| Item | Status | Reason |
|---|---|---|
| Both prompt digests checked (`block.md`, `digests.txt`) | done | both matched before any read |
| Every prepared file's digest checked | done | 11 of 11 matched |
| Preconditions | done | clean status, correct branch, HEAD `6b865ba74` equal to origin, `.agent/STOP` absent, no open PR |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | self-use run exit 0, queue diff and `.agent/selfuse_f074/` exactly as required, no commit-hook refusal |
| C5 | done | suite green, reflog unchanged across the run, cost script exit 0 |
| C6 (this handback) | done | |
| Gate 1 | done | |
| Gate 2 | done | |
| Gate 3 | done | |
| Gate 4 | done | |
| Push | done | see External actions |
| Pull request | skipped | the block orders no PR this round; none is open |

## External actions

- `python3 .remedy-wt/f074-r3/prep/launch.py selfuse .remedy-wt/f074-r3-worker` then `wait.py` (repeatedly until ended): self-use run, exit 0, wall 80.2s (script's own internal timing: 75.7s).
- Inside that run, `.agent/authored/f074-r3-selfuse.py` itself added and removed one detached worktree at `.remedy-wt/f074-r3-jobtree` over the job's own branch `remedy/job-f45fc09ff3464a9e`, to read post-run staleness — the script's documented behavior (the runner had already removed the job workspace), not a worktree of this worker's own.
- `python3 .remedy-wt/f074-r3/prep/launch.py suite .remedy-wt/f074-r3-worker` then `wait.py` (repeatedly until ended): full suite, exit 0, wall 355.4s.
- `python3 scripts/closure_suite_cost.py --feature F074 --record ~/.remedy-loop/test_load.jsonl`: exit 0.
- `git push origin feature/f074-estimate-calibration`: outcome in the worker's reply (written after this file is committed).
- No merge, no PR create, no stash, no rebase, no amend, no force push. The only provider calls this round are the self-use run's two.

## Verification

Gate 1a: `git status --porcelain` (through `git -C <repository root>`) — empty output.

Gate 1b: `python3 .remedy-wt/f074-r3/prep/verify.py .` — every line `True` (C1's four paths and byte
equalities, C2's two, C3's one, C4's path set/one-appended-entry/unconsumed/no-machine-path checks,
C5's path set, `absent C6` before this commit existed, the saved block equals `block.md`), last line
`ALL True`.

Gate 2: the ten files under `.agent/selfuse_f074/`, each non-empty (bytes): `SU-076.md` 1081,
`changed_paths.txt` 68, `entry_and_job_file.txt` 407, `execution_config.txt` 1367,
`full_transcript.txt` 1586, `job_diff.txt` 1414, `result_state.txt` 856, `run_defects.txt` 5,
`staleness_after.txt` 200, `timing.txt` 104.

Gate 3: the suite of C5 — exit code `0`; summary line `23400 passed, 11 skipped, 1 warning in
354.52s (0:05:54)`; bad node ids (failed + errors): `NONE`; leftover processes: `NONE`.

Gate 4: `python3 -m apps.cli.main integrity check --json` — `"fail_count": 0`, `"ok": true`,
`"passed": true`; `handler_import` pass (handlers=196), `live_review_verdict` pass (last Gate verdict
PASS), `plan_consistency` pass (unchecked=0, context_complete=False), `relevant_untracked` pass
(untracked=0, relevant=0), `repo_root_hygiene` pass, `high_blockers_open` pass (no open blocker/high
findings). `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
— `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418', 'R-1421']` (7 ids), matching the
prompt's expected list exactly.

## Authored-text proofs

`.agent/authored/f074-r3.md`: `wc -l` reads `164`, `sha256sum` reads
`e086bac8800dfb5ccbe1031c068932cf922391ba7ff419cb48dac71b4479e1d3`, equal to both `block.md` and the
digest the delivering prompt named.

Every C1-C3 prepared file was copied by a Python byte copy (`c1_copy.py`, `c2_copy.py`, `c3_copy.py`
under `.remedy-wt/f074-r3-worker/`) and proven equal over bytes at copy time by comparing the
destination's re-read bytes against the source's; `verify.py` at gate 1 re-proved every one of them
plus the whole-digest-list check (run separately against `digests.txt` before any write), and
reported `True` throughout. `.agent/authored/f074-r3-selfuse.py` was never edited after the byte copy;
it was only read, then run.

## Self-use run

- Entry id: `SU-076`. Title: "Narrow the excused handler at
  `apps/cli/commands/worker_facade_cmd.py:397`". Job id: `f45fc09ff3464a9e`.
- Builder: `claude-cli`, model `claude-sonnet-4-6`, effort `medium` (all from `execution_config.txt`).
  Reviewer: `claude-cli`, model `claude-sonnet-4-6`, effort `medium` — same provider/model/effort as
  the builder, both read from the `self_use` role's own configuration.
- Job state: `completed`. Stop reason: (empty — the job ran to completion, not to a budget or error
  stop).
- Task `T001`: status `applied_to_job_workspace`; reviewer verdict `pass`; final status
  `staged_review_passed`; repair rounds used `0`.
- Wall seconds (from `timing.txt`): `75.7`.
- Paths (from `changed_paths.txt`):
  ```
  apps/cli/commands/worker_facade_cmd.py
  tests/test_ble001_ratchet.py
  ```
- Job diff (`job_diff.txt`), verbatim:
  ```
  $ git diff HEAD...remedy/job-f45fc09ff3464a9e  (exit 0)
  diff --git a/apps/cli/commands/worker_facade_cmd.py b/apps/cli/commands/worker_facade_cmd.py
  index c22649d44..fecfe3d33 100644
  --- a/apps/cli/commands/worker_facade_cmd.py
  +++ b/apps/cli/commands/worker_facade_cmd.py
  @@ -394,7 +394,7 @@ def doctor_core_report() -> DoctorCoreReport:
                        f"(env {spec.env_var}). Fix: change {spec.key} to a live "
                        f"id. {_dead_provenance(value, dead_entry_by_id)}",
                        subject=value)
  -        except Exception as exc:  # noqa: BLE001 — a dead-model mismatch becomes an advisory, not a blocker
  +        except (ImportError, OSError, ValueError) as exc:
               # Already compact, and there is no fuller record to hold back:
               # both renderings are the same sentence.
               comparison_failed = ("the known-dead ids could not be compared "
  diff --git a/tests/test_ble001_ratchet.py b/tests/test_ble001_ratchet.py
  index 1fa195707..e1cce97e9 100644
  --- a/tests/test_ble001_ratchet.py
  +++ b/tests/test_ble001_ratchet.py
  @@ -18,7 +18,7 @@ REASONED = re.compile(r"^ — \S")

   #: The number of excused blind handlers when BLE001 was turned on. Only ever falls: the
   #: commit that removes a mark lowers this number in the same commit, and it is never raised.
  -MAX_EXCUSED = 282
  +MAX_EXCUSED = 281


   def _marks() -> list[tuple[str, int, str]]:
  ```
- `run_defects.txt`, verbatim:
  ```
  NONE
  ```

No finding is registered by this worker for this run; the block orders that into the next round's
first commit.

## Closure suite

`.agent/authored/f074-closure-suite.txt`, whole and verbatim:
```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 355.4s (the launcher's reading); pytest's own reported wall time: 354.52s (0:05:54)
summary line: 23400 passed, 11 skipped, 1 warning in 354.52s (0:05:54)
bad node ids (failed + errors):
  - NONE
leftover processes: NONE
tree it ran on: a5c62ff9e (F074 R3 C4: the closure's self-use item run to its approval gate, never applied)
tree note: C1 to C4 changed only .agent/ files, the acceptance test, the estimate calibration page, the checklist page and the self-use queue
reflog before: a5c62ff9e HEAD@{2026-10-22 11:56:08 +0200}: commit: F074 R3 C4: the closure's self-use item run to its approval gate, never applied
reflog after: a5c62ff9e HEAD@{2026-10-22 11:56:08 +0200}: commit: F074 R3 C4: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F074 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1334.99 CPU seconds, 354.55 wall seconds, 23411 tests collected, exit status 0, recorded 2026-10-22T10:02:10Z
This closure's suite used 1334.99 CPU seconds, 0.9 percent less than F113's 1347.63, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F113's closure run:
  +2.66 s  tests/cli/test_scoped_listings.py (9.56 -> 12.22)
  +2.46 s  tests/orchestration/test_serve_daemon.py (22.05 -> 24.51)
  +2.15 s  tests/orchestration/test_run_manifest_task_lifecycle_binding.py (2.87 -> 5.02)
  +2.06 s  tests/orchestration/test_job_apply_history.py (7.98 -> 10.04)
  +1.66 s  tests/cli/test_do_scale_matrix.py (37.47 -> 39.13)
  +1.41 s  tests/cli/test_init_cmd.py (6.77 -> 8.18)
  +1.39 s  tests/orchestration/test_run_manifest.py (5.39 -> 6.78)
  +1.36 s  tests/orchestration/test_public_api_gate_paths.py (19.02 -> 20.38)
  +1.18 s  tests/cli/test_plan_approval.py (7.63 -> 8.81)
  +1.18 s  tests/orchestration/test_ci_stage_selection.py (10.73 -> 11.91)
```

## Deviations & assumptions

None. The block's ordered commit sequence (C1 through C5, gates 1-4, this handback, the push) was
followed exactly; no extra commit, no dropped commit, no reordering. The self-use run and the full
suite each ran exactly once, through the prepared launch/wait helpers, with no overlap between them.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Rule 2, the Open PR Gate; no pull request is open for this branch yet.
3. The reviewer reviews round 3, books its verdict and registers every self-use run defect in the
   next round's first commit.
4. The evidence bundle and the review package.
5. The closing round: the Built State, the rotation, the STATUS line, the README and the pull
   request.

Operator questions open: 0. Open findings: 7.

## For the operator, in plain sentences

This round asked Remedy to narrow an overly broad exception handler in one of its own command
handlers down to the exceptions that code can really raise, using a paid frontier model as both the
one doing the work and the one reviewing it, and that reviewer approved the result on the first try
with no rework needed. Separately, the round ran Remedy's whole test collection once end to end:
every test passed and none failed, with a small, expected number skipped. That whole test run took
a little under six minutes. The cost reading said this run's computer time came in essentially flat
against the previous feature's closure run, well inside the allowed margin. Remedy's cost estimates
now come from what each kind of task really used once enough of them have run, every such estimate
says how many tasks it rests on, and a new command shows that measurement.
