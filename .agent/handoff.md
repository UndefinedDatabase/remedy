# Handback — F296 round 5: the closure's integration-gate round — book round 4, T003's Amendment, the consolidation pass, the self-use item run, and the one full suite

## Session

SESSION 1 of feature F296 · round 5 · rounds so far 5

Context self-assessment: this worker verified both prepared digests and every listed digest before any write, copied each prepared file by a script with a byte-for-byte proof, ran its self-review over each commit's staged diff before committing, ran the self-use script and the full suite each exactly once through the block's launch/wait scripts without ending its turn while either was alive, ran every gate once, and context stayed ample throughout.

Fortschritt: ~80 % (T001a to T003 landed; the consolidation pass, the self-use run and the one full suite done · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `6e4bd5788`..`HEAD` on `feature/f296-tier-escalation`.

## Commits

### d426215bb F296 R5 C1: book round 4, T003's Amendment and DECISION F296 D5, the plan, the block and the self-use script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f296-r5.md` | +157/-0 | NEW FILE, this round's block, byte copy, equal to `block.md` by line count (157) and sha256 (`ce52bff3...a8220`) |
| `.agent/authored/f296-r5-selfuse.py` | +127/-0 | NEW FILE, the reviewer-authored self-use script for this round, byte copy, never edited |
| `.agent/decisions.md` | +12/-0 | DECISION F296 D5: T003 ran no benchmark (no round of the feature buys thirty paid missions), default stays off |
| `.agent/live_review.md` | +2/-0 | round 4's verdict booked (amend0827-process-diet rule 1) |
| `.agent/plan.md` | +10/-11 | rewritten for round 5's scope |
| `docs/roadmap/features/T3_F296.md` | +16/-0 | T003's Amendment (DECISION F296 D5): no benchmark ran, the default stays off, what a later run needs is already in place |
| `docs/system/tier-escalation-v1.md` | +2/-1 | names the default and the Amendment's reason |

### 9c9bd95ba F296 R5 C2: the checklist's consolidation pass for F296
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +4/-0 | F296's consolidation paragraph: nothing joined, no two items merged, the list stays at 34 items; `git show --numstat` read `4	0` |

### 4e22c749a F296 R5 C3: the closure's self-use item run to its approval gate, never applied
| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8/-0 | the generator's one appended entry, `SU-074`, unconsumed |
| `.agent/selfuse_f296/` (10 files) | +126/-0 total | the self-use run's own record: `SU-074.md`, `entry_and_job_file.txt`, `execution_config.txt`, `result_state.txt`, `timing.txt`, `changed_paths.txt`, `full_transcript.txt`, `staleness_after.txt`, `job_diff.txt`, `run_defects.txt` — the job ran to its approval gate and was never applied |

### cce706535 F296 R5 C4: the closure's one full suite and its CPU cost
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f296-closure-suite.txt` | +28/-0 | NEW FILE, the one full-suite transcript (green, 23248 passed) and the cost script's reading (exit 1: 12.0 percent over F307's CPU seconds, above the 10 percent limit — owed to the rolling findings paydown, not a failure of this round) |

### (this commit) F296 R5 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | C5: this handback (a handoff cannot table the commit that writes it) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 (preconditions) | done | branch `feature/f296-tier-escalation` at `6e4bd5788`, HEAD equal to `origin/feature/f296-tier-escalation`, `git status --porcelain` empty, `.agent/STOP` absent — all confirmed before any write |
| C1 | done | commit `d426215bb`; all seven paths byte-proved equal to their `c1-` source; `block.md` read 157 lines, sha256 `ce52bff320c87dae8d2558177195139e3762ea2cb40c7b3684ac353ca05a8220`, matching the prompt's own digest |
| C2 | done | commit `9c9bd95ba`; byte-proved equal to its `c2-` source; `git show --numstat` read `4	0` |
| C3 | done | commit `4e22c749a`; self-use entry `SU-074` run to its approval gate (job `86c18d48d1194552`, state `completed`, verdict `pass`), never applied; ten files written, each non-empty, none holding a machine path; queue diff showed exactly one appended entry with an empty `consumed_by`; the commit hook refused nothing |
| C4 | done | commit `cce706535`; the suite ran once (green, exit 0) and the cost script ran once (exit 1, a finding reading, not a round failure); transcript committed alone |
| C5 | done | this commit, the handback |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` printed `True` on every check, `absent` for C5 (not yet committed when run), last line `ALL True` |
| Gate 2 | done | all ten `.agent/selfuse_f296/` files confirmed non-empty, sizes recorded below |
| Gate 3 | done | exit 0, `23248 passed, 11 skipped, 1 warning in 380.20s (0:06:20)`, bad node ids `NONE` |
| Gate 4 | done | `integrity check --json` exit 0, six checks `pass`, `fail_count` 0; open-finding-id lookup printed the required six ids |
| Push | done | reported below |

## External actions

No `gh pr list` call was made this round — the block's own Open PR Gate line states no pull request is open for this branch yet, and no PR step is asked of this round. `git push origin feature/f296-tier-escalation` ran once after this commit; its result is reported in the session reply. No fetch, pull, merge, `gh pr create` or worktree add/remove. The self-use script itself added and removed one temporary worktree (`.remedy-wt/f296-r5-jobtree`, for the job branch's staleness read) and left none behind — confirmed by `staleness_after.txt`'s own content and by `git status --porcelain` showing no stray worktree after. The scratch folder `.remedy-wt/f296-r5-worker/` holds the digest checker, the precondition checker, the copy-and-verify scripts, the launch/wait wrapper scripts (needed because this worker never changes its own cwd), the gate scripts and the commit-message files.

## Verification

1. Digests before any write: `block.md` (157 lines, sha256 `ce52bff320c87dae8d2558177195139e3762ea2cb40c7b3684ac353ca05a8220`) and `digests.txt` (sha256 `063736d18381a674141fe195140a1082c5b544bd8d35748e6df2c78cc90f141a`) matched the two hashes given in the prompt; every one of the twelve entries listed in `digests.txt` matched its sha256 (checked with a script, last line `ALL OK`).
2. Preconditions: `git rev-parse --short=9 HEAD` read `6e4bd5788`, `git rev-parse HEAD` equalled `git rev-parse origin/feature/f296-tier-escalation` (`6e4bd5788e1ce41073f4fd848e1c2450a446c1d6`), `git status --porcelain` printed nothing, `git branch --show-current` read `feature/f296-tier-escalation`, `.agent/STOP` did not exist — all before any write.
3. C1: all seven named paths copied by a script, then compared byte-for-byte against the prepared source; `git diff --stat` showed exactly the seven named paths (42 insertions, 12 deletions across the five modified files, plus the two new files), matching the block's own path list.
4. C2: the one named path copied the same way; `git diff` was read in full as self-review before staging — the added paragraph states the consolidation outcome (nothing joined, list stays at 34); `git show --numstat HEAD` after commit read `4	0`.
5. C3: `python3 .remedy-wt/f296-r5/prep/launch.py selfuse .remedy-wt/f296-r5-worker` started the run (pid reported); `python3 .remedy-wt/f296-r5/prep/wait.py selfuse .remedy-wt/f296-r5-worker 50` returned on the first call with `exit 0 wall 71.9`. `git status --porcelain` afterward showed only `scripts/self_use_queue.json` modified and `.agent/selfuse_f296/` new, matching the block; `git diff scripts/self_use_queue.json` showed exactly one appended entry, id `SU-074`, empty `consumed_by`. The script was never edited.
6. C4: `git reflog -n 1 --date=iso` read `4e22c749a HEAD@{2026-10-22 08:08:36 +0200}: commit: F296 R5 C3: ...` both before and after the run — unchanged. `python3 .remedy-wt/f296-r5/prep/launch.py suite .remedy-wt/f296-r5-worker` started the run; `wait.py suite .remedy-wt/f296-r5-worker 50` returned on the first call with `exit 0 wall 381.1`. The log held no `FAILED`, `ERROR` or "process(es) behind" line. `python3 scripts/closure_suite_cost.py --feature F296 --record ~/.remedy-loop/test_load.jsonl` ran once, exit 1 (a cost-ceiling finding reading per the block, not a round failure); every line it printed was copied verbatim into the transcript.
7. Gate 1: `git status --porcelain` printed nothing; `python3 .remedy-wt/f296-r5/prep/verify.py .` (run with `cwd=` set to the repository root) printed `True` on every check for C1 through C4, `absent` for C5 (not yet committed when the gate ran), and `ALL True` last.
8. Gate 2: all ten files under `.agent/selfuse_f296/` confirmed non-empty — `SU-074.md` 1076 bytes, `changed_paths.txt` 68 bytes, `entry_and_job_file.txt` 402 bytes, `execution_config.txt` 1367 bytes, `full_transcript.txt` 1586 bytes, `job_diff.txt` 1343 bytes, `result_state.txt` 856 bytes, `run_defects.txt` 5 bytes, `staleness_after.txt` 200 bytes, `timing.txt` 104 bytes.
9. Gate 3: the transcript's own exit code (0), summary line (`23248 passed, 11 skipped, 1 warning in 380.20s (0:06:20)`) and bad node ids (`NONE`) were read back from the committed `.agent/authored/f296-closure-suite.txt`.
10. Gate 4: `python3 -m apps.cli.main integrity check --json` (from the primary checkout) returned six checks, all `pass` (handler import, live-review verdict, plan consistency, relevant-untracked, repo-root hygiene, open high-severity findings), `"fail_count": 0`. `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"` printed `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418']`, matching the block's required list exactly.

## Authored-text proofs

Applied this round, each proved equal over bytes by a script that only reads, against the prepared file: all seven paths of C1 (plus `.agent/authored/f296-r5.md` additionally proved equal to the prompt's own `block.md` by line count and sha256), the one path of C2. C3 and C4 are the worker's own run outputs, not reviewer-authored text, and carry no such proof; C3's script itself (`.agent/authored/f296-r5-selfuse.py`) is reviewer-authored and was proved byte-equal in C1, then run unedited.

## Self-use run

Entry id `SU-074`, title "Narrow the excused handler at apps/cli/commands/worker_facade_cmd.py:309" (tier 4, excused-handler provenance). Job id `86c18d48d1194552`.

Builder and reviewer provider/model (from `execution_config.txt`): builder `claude-cli`, model `claude-sonnet-4-6`, effort `medium`; reviewer `claude-cli`, model `claude-sonnet-4-6`, effort `medium`. Repair provider/model/effort: none configured (blank/default).

Job state: `completed`. Stop reason: (blank). Stop source: (blank).

Task states, from `result_state.txt`:
- `T001`: status `applied_to_job_workspace`; reviewer verdict `pass`; final status `staged_review_passed`; repair rounds used `0`; run id `fbc24b58b6cd4856`.

Wall seconds (from `timing.txt`): `67.1`.

Paths (from `changed_paths.txt`):
```
apps/cli/commands/worker_facade_cmd.py
tests/test_ble001_ratchet.py
```

Job diff (from `job_diff.txt`), verbatim:
```
$ git diff HEAD...remedy/job-86c18d48d1194552  (exit 0)
diff --git a/apps/cli/commands/worker_facade_cmd.py b/apps/cli/commands/worker_facade_cmd.py
index c22649d44..c022e85b8 100644
--- a/apps/cli/commands/worker_facade_cmd.py
+++ b/apps/cli/commands/worker_facade_cmd.py
@@ -306,7 +306,7 @@ def doctor_core_report() -> DoctorCoreReport:
         cat = importlib.import_module("apps.cli.command_catalog")
         _check("command_catalog", True,
                f"{len(cat.CATALOG)} commands, {len(cat.GROUPS)} groups")
-    except Exception as exc:  # noqa: BLE001 — a catalog import failure is that check's own result
+    except (ImportError, AttributeError) as exc:
         _check("command_catalog", False, report_safe_text(exc, limit=120))
 
     _try_import("run_contract", "packages.orchestration.run_contract", "ContractAction")
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

`run_defects.txt`, verbatim:
```
NONE
```

No finding is registered by this worker for this run.

## Closure suite

`.agent/authored/f296-closure-suite.txt`, whole and verbatim:
```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 381.1s (the launcher's reading); pytest's own reported wall time: 380.20s (0:06:20)
summary line: 23248 passed, 11 skipped, 1 warning in 380.20s (0:06:20)
bad node ids (failed + errors):
  - NONE
leftover processes: NONE
tree it ran on: 4e22c749a (F296 R5 C3: the closure's self-use item run to its approval gate, never applied)
tree note: C1 to C3 changed only .agent/ files, the feature file, the tier escalation page, the checklist page and the self-use queue
reflog before: 4e22c749a HEAD@{2026-10-22 08:08:36 +0200}: commit: F296 R5 C3: the closure's self-use item run to its approval gate, never applied
reflog after: 4e22c749a HEAD@{2026-10-22 08:08:36 +0200}: commit: F296 R5 C3: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F296 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 1
Test load: 1369.23 CPU seconds, 380.21 wall seconds, 23259 tests collected, exit status 0, recorded 2026-10-22T06:15:07Z
This closure's suite used 1369.23 CPU seconds, 12.0 percent more than F307's 1222.15; that is above the 10 percent limit, so this closure registers a finding owned by the rolling findings paydown.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F307's closure run:
  +9.58 s  tests/orchestration/test_review_zip_hygiene.py (32.56 -> 42.14)
  +8.10 s  tests/cli/test_do_scale_matrix.py (33.47 -> 41.57)
  +7.48 s  tests/runtimes/test_supervisor_portability.py (42.72 -> 50.20)
  +5.73 s  tests/serve_http_handler/test_public_api.py (12.00 -> 17.73)
  +4.81 s  tests/orchestration/test_job_task_runner.py (17.51 -> 22.32)
  +4.65 s  tests/orchestration/test_subtree_rerun_prepare.py (10.66 -> 15.31)
  +3.46 s  tests/cli/test_do_sequence_cli.py (28.05 -> 31.51)
  +3.45 s  tests/cli/test_do_order_file.py (9.68 -> 13.13)
  +3.44 s  tests/orchestration/test_job_worktree_integrity.py (7.28 -> 10.72)
  +3.44 s  tests/cli/test_do_several_projects.py (8.38 -> 11.82)
```

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1, C2, C3, C4, then this C5), each commit touching only its named paths. The self-use script and the full suite each ran exactly once through the block's own `launch.py`/`wait.py`, with this worker's shell tool using its longest timeout and calling `wait.py` again until each printed `exit <code> wall <seconds>` on the first call. No amend, rebase, force-push or `--no-verify` was used. `REMEDY_TEST_MAX_WORKERS` was never set, no larger `-n` was passed, and no two test commands ran at the same time. `.data` was never read. The cost script's exit 1 is the block's own named non-deviation ("a reading the reviewer registers as a finding, not a failure of this round"), so it is recorded in the transcript and here, not treated as a blocker. This worker never changed its own working directory; every command needing the repository root as cwd ran through a small `python3` script under `.remedy-wt/f296-r5-worker/` that passes `cwd=`.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate — no pull request is open for this branch yet.
3. The reviewer reviews round 5, books its verdict and registers every self-use run defect in the next round's first commit.
4. The evidence bundle and the review package (the suite came back green).
5. The closing round: the Built State, the rotation, the STATUS line, the README and the pull request.

Operator questions open: 0. Open findings: 6.

## For the operator, in plain sentences

This session asked a paid helper model to narrow one overly broad error-catching block in a command-line health check down to the specific errors it can actually raise, and the helper's own reviewer approved the result without needing a repair round. All 23,248 of the project's automated tests passed, 11 were intentionally skipped, and none failed; the whole run took about six minutes and twenty seconds. The computer-time cost reading showed this run used about twelve percent more processing time than the previous feature's closure run, which is above the ten percent comparison limit, so that gets written down as a cost item for a later session to look at, not something that blocks today's work. Handing a failing task to a stronger, more expensive model stays switched off until a real measured comparison shows it actually passes more often or costs less that way.

A pull request will be opened once the evidence bundle, the review package and the closing round have landed; it is not opened yet.
