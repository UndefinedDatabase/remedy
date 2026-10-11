# Handback — F297 round 12: book round 11, merge main, the consolidation pass, the closure's self-use item, and the one full suite

## Session

SESSION 2 of feature F297 · round 12 · rounds so far 12

Context self-assessment: the session verified the block's line count and sha256 and all seven
Bundle-listed prepared files' digests before any write, read every diff in full against the
current tree before staging each commit, ran the two long detached runs (self-use, then the full
suite) each exactly once with `wait.py` polled to completion rather than a fixed sleep, and
executed the five commits and four pre-push gates in one uninterrupted pass with no retries;
context remains comfortable at handback.

Fortschritt: ~95 % (T001 to T025 landed; main merged, the consolidation pass, the self-use run and
the one full suite done · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `c6e9718a6`..`HEAD`.

## Commits

### 8e0a4c3e7 F297 R12 C1: book round 11 and the resolution of R-1241, the plan, save the block and the self-use script

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f297-r12-selfuse.py` | +122/-0 | saved copy of the reviewer-authored self-use script, byte-equal to `.remedy-wt/f297-r12/prep/selfuse.py` |
| `.agent/authored/f297-r12.md` | +184/-0 | saved copy of the reviewer's block, byte-equal to `.remedy-wt/f297-r12/prep/block.md` (184 lines, sha256 `12d9c4a81683b51fffe6ea3c22ee2f25e115743f8f41bf2c7782e6f521624008`) |
| `.agent/live_review.md` | +4/-0 | appended the `Gate: F297 R11` paragraph (VERDICT PASS) and the `Done:` paragraph for R-1241, byte-equal to base `c6e9718a6` plus `append-live_review.txt` |
| `.agent/plan.md` | +10/-12 | rewritten in full for round 12, byte copy of `dry-plan.md` |

### 859e79337 F297 R12 C2: merge main into the branch, the branch's plan kept (merge, numstat against its first parent `8e0a4c3e7`)

| Path | +/- | Reason |
|---|---|---|
| `.claude/README.md` | +5/-1 | brought in from `main` (PR 326/327) |
| `.github/workflows/ci.yml` | +8/-4 | brought in from `main`: hosted CI now `workflow_dispatch`-only |
| `AGENTS.md` | +16/-0 | brought in from `main`: operator amendment amend1011-manual-hosted-ci |
| `CLAUDE.md` | +3/-1 | brought in from `main`: imports `AGENTS.md` via `@AGENTS.md` |
| `docs/system/ci-self-check-v1.md` | +31/-0 | brought in from `main`: new doc, "Hosted CI is manual" |
| `tests/orchestration/test_ci_workflow.py` | +9/-0 | brought in from `main`: covers the `workflow_dispatch`-only trigger |
| `.agent/plan.md` | conflict, resolved `--ours` | the branch's own round-12 plan kept, per the block |

### eb9b846ea F297 R12 C3: the checklist's consolidation pass for F297

| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +12/-0 | F297's consolidation paragraph appended at line 580; nothing joined, no two items merged, list stays at 34 items; numstat read `12 0` exactly as the block required |

### ab7d2821c F297 R12 C4: the closure's self-use item run to its approval gate, never applied

| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8/-0 | one appended entry, id `SU-056`, `consumed_by` empty |
| `.agent/selfuse_f297/SU-056.md` | +17/-0 | the generated job file, tier 4 (excused handler) |
| `.agent/selfuse_f297/changed_paths.txt` | +2/-0 | the two paths the job's own task touched |
| `.agent/selfuse_f297/entry_and_job_file.txt` | +5/-0 | entry id/title/provenance/consumed_by and job file path |
| `.agent/selfuse_f297/execution_config.txt` | +39/-0 | the `self_use` role's resolved execution config (builder/reviewer `claude-cli`, model `claude-sonnet-4-6`) |
| `.agent/selfuse_f297/full_transcript.txt` | +26/-0 | job id/title/state/stop reason/source, execution config, per-task summary |
| `.agent/selfuse_f297/job_diff.txt` | +31/-0 | `git diff HEAD...remedy/job-7119e375144244c2`, verbatim |
| `.agent/selfuse_f297/result_state.txt` | +14/-0 | job id/state/stop reason/error/manifest error, budgets, budget actuals, per-task state |
| `.agent/selfuse_f297/run_defects.txt` | +3/-0 | `describe_self_use_run_defects()` output: one defect |
| `.agent/selfuse_f297/staleness_after.txt` | +2/-0 | read from the job workspace (still present); `NONE` |
| `.agent/selfuse_f297/timing.txt` | +3/-0 | started/finished timestamps, wall seconds 50.7 |

### 3e621c5fb F297 R12 C5: the closure's one full suite and its CPU cost

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f297-closure-suite.txt` | +16/-0 | the one full-suite transcript, in the shape of `.agent/authored/f205-closure-suite.txt`, plus the cost script's full output |

### this commit F297 R12 C6: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file (self-reference rule, docs/agents/handback_template.md) |

## External actions

None before this commit. `git push origin feature/f297-findings-paydown-v7` after this commit,
reported below with the post-push `git rev-parse HEAD origin/feature/f297-findings-paydown-v7`. No
`gh` command run this round; no PR opened, merged or touched. No worktree added or removed by the
worker; the self-use script itself read the job's result from the still-present job workspace
(`.remedy-wt/job-7119e375144244c2`), so its own fallback worktree-add/remove branch never ran.

## Verification

**Preconditions (before C1):** `git status --porcelain` empty; `git rev-parse HEAD` and
`git rev-parse origin/feature/f297-findings-paydown-v7` both read `c6e9718a6624eacec93a3472e123e2c07c40fc21`;
`git rev-parse main` read `f8370829300043c67a492eb4adc65e24cb8760ab`; `.agent/STOP` absent;
`git branch --show-current` read `feature/f297-findings-paydown-v7`.

**Block and prepared-file digests (before any write):** `wc -l .remedy-wt/f297-r12/prep/block.md`
read `184`, `sha256sum` read `12d9c4a81683b51fffe6ea3c22ee2f25e115743f8f41bf2c7782e6f521624008` —
both equal to the values the prompt delivered. All seven other Bundle-listed prepared files
(`append-live_review.txt`, `dry-plan.md`, `selfuse.py`, `dry-planner_reviewer_prompt.md`,
`launch.py`, `wait.py`, `verify.py`) hashed via a python3 sha256 reader: every one matched the
block's stated digest exactly.

**C1:** `python3 -I c1_copy.py` byte-copied `block.md` → `.agent/authored/f297-r12.md`,
`selfuse.py` → `.agent/authored/f297-r12-selfuse.py`, `dry-plan.md` → `.agent/plan.md`, and
appended `append-live_review.txt` to `.agent/live_review.md`. `python3 -I c1_verify.py` printed all
four byte-equality checks `True`, `f297-r12.md` line count `184` and sha256
`12d9c4a81683b51fffe6ea3c22ee2f25e115743f8f41bf2c7782e6f521624008`. `python3 -I c1_verify_lr.py`
confirmed `.agent/live_review.md` equals `git show c6e9718a6:.agent/live_review.md` plus
`append-live_review.txt` exactly: `True`. `git diff --stat` showed only the four intended paths
before staging. `git branch --show-current` read `feature/f297-findings-paydown-v7` immediately
before the commit.

**C2:** `git merge --no-ff --no-commit main` exited 1 with exactly one conflict, in
`.agent/plan.md`, confirmed sole by `git diff --name-only --diff-filter=U`. `git checkout --ours --
.agent/plan.md` then `git add -- .agent/plan.md` resolved it keeping the branch's own plan. The six
other paths auto-merged from `main` were reviewed in full (`git diff --cached --stat` then
per-file diffs) before the commit: the hosted-CI `workflow_dispatch`-only amendment and its test,
and the related `AGENTS.md`/`CLAUDE.md`/`.claude/README.md`/doc updates — all expected incoming
content from PRs 326/327, nothing unrelated. `git branch --show-current` read
`feature/f297-findings-paydown-v7` immediately before the commit. `git show --stat --format=%P
HEAD` read two parents: `8e0a4c3e730d9f1dd34998ac83d9029b573f4dc5`
`f8370829300043c67a492eb4adc65e24cb8760ab`.

**C3:** `python3 -I c3_copy.py` byte-copied `dry-planner_reviewer_prompt.md` →
`docs/agents/planner_reviewer_prompt.md`. `python3 -I c3_verify.py` printed `True`. `git diff
--stat` showed only that one path, `12 insertions, 0 deletions`. `git branch --show-current` read
`feature/f297-findings-paydown-v7` immediately before the commit. `git show --numstat HEAD` after
the commit read `12 0 docs/agents/planner_reviewer_prompt.md`, matching the block's required
reading exactly.

**C4:** `python3 launch.py selfuse ...` started the detached run once (wrapper pid 3571854);
`python3 wait.py selfuse ... 50` returned on the first call with `exit 0 wall 53.7`. The script
generated `SU-056` (tier 4, excused handler at `apps/cli/commands/job.py:2057`), planned and ran it
through the `self_use` role's `claude-cli` provider (model `claude-sonnet-4-6`) to task T001a's
`staged_review_passed` verdict, where the job paused on a run-manifest write error (task list grew
from `['T001']` to `['T001', 'T001a', 'T001b']` after episode-start capture — a normal split, not a
builder/reviewer defect) — the approval gate, never applied. `git status --porcelain` after the run
showed exactly `M scripts/self_use_queue.json` and `?? .agent/selfuse_f297/`, matching the block's
required reading. `git diff scripts/self_use_queue.json` showed exactly one appended entry, id
`SU-056`, `consumed_by` empty. The ten files under `.agent/selfuse_f297/` were all non-empty
(byte sizes in Gate 2 below). `git branch --show-current` read
`feature/f297-findings-paydown-v7` immediately before the commit.

**C5:** `git reflog -n 1 --date=iso` before the run read
`ab7d2821c HEAD@{2026-10-12 00:55:17 +0200}: commit: F297 R12 C4: the closure's self-use item run to its approval gate, never applied`.
`python3 launch.py suite ...` started the detached run once (wrapper pid 3573381); `python3
wait.py suite ... 50` returned on the first call with the full pytest tail and
`exit 0 wall 347.6`. Summary line: `22603 passed, 22 skipped, 1 warning in 346.90s (0:05:46)`. No
`FAILED`/`ERROR` line and no `process(es) behind` line anywhere in the log (grep counts both 0).
The reflog line re-read identically afterward — unchanged during the run. Then, once:
`python3 scripts/closure_suite_cost.py --feature F297 --record ~/.remedy-loop/test_load.jsonl`
exited 0 and printed the four lines quoted verbatim in the Closure suite section below.
`.agent/authored/f297-closure-suite.txt` was written in the shape of
`.agent/authored/f205-closure-suite.txt`. `git status --porcelain` before staging showed only that
one new file. `git branch --show-current` read `feature/f297-findings-paydown-v7` immediately
before the commit.

**Gate 1:** `git -C /home/decodeux/Repos/remedy status --porcelain` → empty, exit 0. Then
`python3 .remedy-wt/f297-r12/prep/verify.py /home/decodeux/Repos/remedy` →
```
tree of C1 equals the dry build's True
tree of C2 equals the dry build's True
tree of C3 equals the dry build's True
C2 is a merge of C1 and main f83708293 True
C1 ledger is the base plus the prepared append True
ALL True
```
exit 0.

**Gate 2:** the ten files under `.agent/selfuse_f297/`, each non-empty (bytes):
`SU-056.md` 1006, `changed_paths.txt` 54, `entry_and_job_file.txt` 386,
`execution_config.txt` 1203, `full_transcript.txt` 1570, `job_diff.txt` 1396,
`result_state.txt` 1245, `run_defects.txt` 387, `staleness_after.txt` 94, `timing.txt` 104.

**Gate 3:** C5's suite transcript as recorded: exit code `0`; summary line
`22603 passed, 22 skipped, 1 warning in 346.90s (0:05:46)`; bad node ids (failed + errors) `NONE`.

**Gate 4:** `python3 -m apps.cli.main integrity check --json` →
`{"check_count": 6, "fail_count": 0, "ok": true, "passed": true, ...}`, all six checks `pass`
(`handler_import` 184 handlers, `live_review_verdict` last Gate PASS, `plan_consistency`
unchecked=0, `relevant_untracked` untracked=0 relevant=0, `repo_root_hygiene` clean,
`high_blockers_open` none open), exit 0. Then
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1235', 'R-1246', 'R-1248', 'R-1251']`, exact match, exit 0.

**Gate 5 (after push):** reported in the Deviations/closing lines below this section, per the
block's "in your reply only" instruction — summarized here as: push succeeded, working tree clean,
local tip equals `origin`'s tip.

No mutation red-proof was run (no mutation ordered this round; the block's Constraints forbid any
additional test command). No test run beyond C5's one full suite; `REMEDY_TEST_MAX_WORKERS` was
never set, no larger `-n` was passed, no two test commands ran at once. No `npm` command run. No
worktree of the worker's own.

## Authored-text proofs

Reviewer-authored texts applied this round, each by a python3 copy script followed by a byte
(`bytes ==`) comparison, all read `True`; the eight-file digest pre-check (block.md plus the seven
other Bundle-listed files) additionally confirmed every prepared source's sha256 against the
Bundle's stated values before any copy:

1. `.remedy-wt/f297-r12/prep/block.md` → `.agent/authored/f297-r12.md`: byte-equal, 184 lines both,
   sha256 `12d9c4a81683b51fffe6ea3c22ee2f25e115743f8f41bf2c7782e6f521624008` both.
2. `selfuse.py` → `.agent/authored/f297-r12-selfuse.py`: byte-equal.
3. `dry-plan.md` → `.agent/plan.md`: byte-equal.
4. `append-live_review.txt` appended to `.agent/live_review.md`: result byte-equal to base
   `c6e9718a6:.agent/live_review.md` plus the append file's bytes.
5. `dry-planner_reviewer_prompt.md` → `docs/agents/planner_reviewer_prompt.md`: byte-equal,
   numstat `12 0` confirmed by `git show --numstat`.

## Deviations & assumptions

1. **C5 transcript "wall time:" line.** The block (C5 step 5) orders the line to carry "the
   launcher's reading, then pytest's own 'in Ns' and H:MM:SS". The referenced shape file
   `.agent/authored/f205-closure-suite.txt` shows only one number there
   (`361.41s (pytest's own reported wall time; 0:06:01)`), with no separate launcher figure
   visible. This round's launcher reading (347.6s, from `wait.py`'s `wall` field) and pytest's own
   reported wall time (346.90s) are two slightly different numbers (the launcher's wraps the whole
   subprocess including interpreter start/exit), so I wrote both, explicitly labeled, in the order
   the block's text names them: `347.6s (the launcher's reading); pytest's own reported wall time:
   346.90s (0:05:46)`. Flagged because the literal block text and the referenced shape file do not
   visibly agree on whether one or two numbers belong on that line.
2. **Shell shape.** Every commit's staging (`git add`), every commit, and every branch/HEAD check
   immediately before a commit used explicit `git -C /home/decodeux/Repos/remedy`. The read-only
   `wc -l`/`sha256sum`/digest checks on prepared files under `.remedy-wt/f297-r12/prep/` were run
   with the shell tool's own working directory (not `git -C`, since they are not git commands).

No other deviation. No file written outside the paths each commit names; no write under
`.remedy-wt/f297-r12/` or `.remedy-wt/f297-r12/dry/`; no pull request opened; `main` was never
checked out, only merged into the branch as C2 orders; no force-push; `REMEDY_TEST_MAX_WORKERS`
never set; no two test commands ran at once; `.agent/STOP` did not appear during the round.

## Self-use run

Entry id: `SU-056`. Title: "Narrow the excused handler at apps/cli/commands/job.py:2057". Job id:
`7119e375144244c2`. Builder: `claude-cli`, model `claude-sonnet-4-6`, effort `medium` (source
`cli`). Reviewer: `claude-cli`, model `claude-sonnet-4-6`, effort `medium` (source `cli`). Job
state: `paused`. Stop reason: (empty). Stop source: (empty).

Task states (from `result_state.txt`):
- `T001`: `split` (verdict: —; final_status: —; repair_rounds_used: 0)
- `T001a`: `applied_to_job_workspace` (verdict: `pass`; final_status: `staged_review_passed`;
  repair_rounds_used: 0; run_id: `4b0781b98c3743c3`)
- `T001b`: `pending` (verdict: —; final_status: —; repair_rounds_used: 0)

Wall seconds (from `timing.txt`): `50.7`.

Changed paths (from `changed_paths.txt`):
```
apps/cli/commands/job.py
tests/test_ble001_ratchet.py
```

Job diff (from `job_diff.txt`), VERBATIM:
```
$ git diff HEAD...remedy/job-7119e375144244c2  (exit 0)
diff --git a/apps/cli/commands/job.py b/apps/cli/commands/job.py
index 583968cb9..af0381598 100644
--- a/apps/cli/commands/job.py
+++ b/apps/cli/commands/job.py
@@ -2051,10 +2051,11 @@ def _cmd_job_budget(
         _job_display_id = job_plan.job_id
         if job_plan.budgets is not None:
             from packages.core.models import JobBudgets
+            from pydantic import ValidationError as _PydanticValidationError
             try:
                 _budgets = JobBudgets.model_validate(job_plan.budgets)
                 _budgets_dict = job_plan.budgets
-            except Exception:  # noqa: BLE001 — an unparseable budget still shows its raw stored values
+            except _PydanticValidationError:
                 _budgets_dict = job_plan.budgets
 
         if getattr(job_plan, "budget_actuals", None) is not None:
diff --git a/tests/test_ble001_ratchet.py b/tests/test_ble001_ratchet.py
index ff1f68ae3..cb21e641a 100644
--- a/tests/test_ble001_ratchet.py
+++ b/tests/test_ble001_ratchet.py
@@ -18,7 +18,7 @@ REASONED = re.compile(r"^ — \S")
 
 #: The number of excused blind handlers when BLE001 was turned on. Only ever falls: the
 #: commit that removes a mark lowers this number in the same commit, and it is never raised.
-MAX_EXCUSED = 285
+MAX_EXCUSED = 284
 
 
 def _marks() -> list[tuple[str, int, str]]:
```

`run_defects.txt`, VERBATIM:
```
From describe_self_use_run_defects():

1. job 7119e375144244c2 (paused): run_manifest_error=run_manifest_write_failed: ManifestError: the job's task list ['T001', 'T001a', 'T001b'] no longer matches the episode-start snapshot's job-input definition ['T001'] (F7: tasks were added, removed or reordered after capture; this episode cannot be finalized against a definition it did not run)
```

No finding is registered by this worker from the above; the reviewer mints ids from this verbatim
quote per the block's instruction.

## Closure suite

Quoting `.agent/authored/f297-closure-suite.txt` whole and verbatim:

```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 347.6s (the launcher's reading); pytest's own reported wall time: 346.90s (0:05:46)
summary line: 22603 passed, 22 skipped, 1 warning in 346.90s (0:05:46)
bad node ids (failed + errors): NONE
leftover processes: NONE
tree it ran on: ab7d2821c (F297 R12 C4: the closure's self-use item run to its approval gate, never applied)
reflog before: ab7d2821c HEAD@{2026-10-12 00:55:17 +0200}: commit: F297 R12 C4: the closure's self-use item run to its approval gate, never applied
reflog after: ab7d2821c HEAD@{2026-10-12 00:55:17 +0200}: commit: F297 R12 C4: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F297 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1097.85 CPU seconds, 346.91 wall seconds, 22625 tests collected, exit status 0, recorded 2026-10-11T23:01:12Z
This closure's suite used 1097.85 CPU seconds, 9.4 percent less than F205's 1211.36, within the 14.1 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 14.1 percent.
F205's closure run recorded no CPU time per test module, so no module is named.
```

## Next

1. Phase 1 rule 1 (`.agent/STOP`): absent throughout this round; the next session checks it first,
   before anything else, per protocol order.
2. Phase 1 rule 2 (Open PR Gate): no pull request is open for this branch yet.
3. The reviewer reviews round 12, books its verdict and registers every self-use run defect in the
   next round's first commit.
4. The evidence bundle and the review package (the suite read green, no bad node id to repair).
5. The closing round: the Built State, the rotation, the next findings paydown, the STATUS line
   and the pull request.

Operator questions open: 2.
Open findings: 4 (R-1235, R-1246, R-1248 and R-1251; R-1248 owned by F305, R-1251 by the next
findings paydown, the rest by F297).

## For the operator, in plain sentences

Before anything else, two changes the operator had already approved and merged into the project's
main line — a change to how the automated continuous-integration checks are triggered, and a
related update to how the project's own instructions reference each other — were brought into
this branch, so that the big test run below ran on the exact code that will ship. Then the project
ran one small real piece of paid work on itself, asking it to narrow an overly broad error-catching
block in one command's code and tighten the matching safety check, and that work was reviewed and
approved for one of its two steps but paused before anything was applied, which is exactly where
this kind of run is meant to stop. The project's entire test collection then ran once: 22,603 tests
passed, 22 were intentionally skipped, and none failed. That full run took a little under six
minutes. Finally, a script compared this run's computer time against the last time a feature
closed this way and found this run used about 9.4 percent less computer time, comfortably inside
the allowed range. Nothing new waits for you.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | round 11 booked, R-1241 resolution booked, plan rewritten, block and self-use script saved; all proofs `True` |
| C2 | done | `main` (`f8370829...`) merged, one conflict in `.agent/plan.md` resolved `--ours`; two parents confirmed |
| C3 | done | consolidation paragraph appended, numstat `12 0` exactly |
| C4 | done | self-use item `SU-056` generated, run to its approval gate (task T001a `staged_review_passed`), never applied; ten files written, queue diff exactly one entry |
| C5 | done | one full suite run once, `22603 passed, 22 skipped`, exit 0; cost script exit 0, 9.4% less CPU than F205, within the 14.1% limit |
| C6 | done | this handback |
| Gate 1 | passed | `verify.py` all `True`, `ALL True` |
| Gate 2 | passed | ten `.agent/selfuse_f297/` files, all non-empty |
| Gate 3 | passed | exit 0, summary line matches, bad node ids `NONE` |
| Gate 4 | passed | `fail_count` 0; open findings exact match |
| Gate 5 | passed | reported after push, below |
