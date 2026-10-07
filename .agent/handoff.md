# Handoff — F116 session 1, round 4: book round 3, resolve R-1165 and R-1166; T002 wiring —
# run_job records every counted call in the burn monitor and remedy job budget shows the trip,
# booked against DECISION F116 D4

## Session

SESSION 1 of feature F116 · round 4 · rounds so far 4

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~50 % (T001 built · T002 recording built · T002 unattended pause and T003 open) —
Schätzung

## Range

Review of `901526c7ee0413a3e4a3f8e64dc473ef7cedfd8b`..HEAD (HEAD is this commit, C5 below).

## Commits

### 4490c1f45 F116 R4 C1: book round 3, resolve R-1165 and R-1166, register R-1167, DECISION F116 D4, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f116-r4.md` | 171/0 (new) | byte copy of the reviewer's prepared `block.md` |
| `.agent/decisions.md` | 10/0 | append DECISION F116 D4 (the wiring's specification), `append-decisions.txt`'s bytes |
| `.agent/live_review.md` | 8/0 | append the F116 round 3 gate entry plus R-1167's registration, `append-live_review.txt`'s bytes |
| `.agent/plan.md` | 10/11 | replace with the reviewer's prepared `dry-plan.md`, byte for byte |

### 27ea8a462 F116 R4 C2: the job_burn key descriptions say the minimum binds only the trailing basis (R-1167)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/config.py` | 12/4 | R-1167's repair: the `job_burn.window`, `job_burn.min_samples` and `job_burn.multiplier` descriptions now say the minimum applies only while no hourly expectation is set, and that with one set the monitor needs one call more than the window |
| `docs/guides/environment.md` | 3/3 | regenerated from the registry; the three corrected rows |

### a3a61a564 F116 R4 C3: run_job records every counted call in the burn monitor and keeps the newest trip on the job (T002, DECISION F116 D4)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_job.py` | 55/0 | DECISION F116 D4 (1)-(4): one `JobBurnMonitor` per run built in a try/except naming exactly `(ValueError, OSError)` and logging one error with `exc_info=True`; `record_call` in `_on_provider_call` placed after the `fake` early return; the reading in `_stop_check`'s no-stop branch, before the predictive check, setting and persisting `job.burn_reading` only when a tripped record differs; the `burn_reading` field with its export and load lines |
| `packages/orchestration/job_burn.py` | 5/4 | D4 (7): the module docstring and the `JobBurnMonitor` comment now say `run_job` calls this module; no code line changed |
| `tests/test_no_orphan_modules.py` | 0/2 | the `job_burn.py` entry of `ALLOWED_UNWIRED` deleted (its first production importer exists now) |
| `tests/orchestration/import_reachability_allowlist.txt` | 2/0 | `packages.orchestration.burn_detector` and `packages.orchestration.job_burn` added, each in sorted position |
| `tests/orchestration/test_job_burn.py` | 216/0 | one test function per behaviour: the registry's own defaults through the resolver; a real two-task `run_job` whose trip read before the fourth call stays the job's record after the fourth call's reading no longer trips; the same run with no trip; the same run under a `fake` provider; the same run with the resolver raising `ValueError`, logging one ERROR record |

### 6c80719ed F116 R4 C4: remedy job budget shows the recorded burn alarm (T002, DECISION F116 D4)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/job.py` | 22/0 | D4 (5): `_cmd_job_budget` adds `burn_reading` to the JSON output beside `recorded_prediction`; the text output prints `recorded burn alarm:` with its `rate:` and `window:` lines, directly after the recorded stop prediction, each value read with `.get` |
| `docs/system/job-budget-enforcement-v0.md` | 16/8 | "What `remedy job budget` shows" names the recorded burn alarm and the `burn_reading` JSON key; "Deliberately not built" keeps calibration and per-task-class caps and names F116's burn-rate anomaly detection instead of denying it exists |
| `tests/orchestration/test_job_budgets.py` | 77/0 | `TestJobBudgetCliRendersBurnReading`, beside `TestJobBudgetCliRendersPredictions` and using its helpers: the JSON `burn_reading` equals a persisted record verbatim, is null when none was recorded; the text prints the heading and a rate line containing `15000.0 tokens per call against an expected 1500.0 (trailing_baseline)`; no heading for a job with or without a money limit when none was recorded |

### F116 R4 C5: handback (self-reference exception — the handoff is committed by this same commit)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

- `git push origin feature/f116-cost-anomaly-alarm` once, after C5: outcome reported in the
  worker's final reply (write-once rule; not known when this file is written).
- No merge, no `git checkout` or `git switch` away from this branch, no branch created other than
  `feature/f116-cost-anomaly-alarm`, no force-push, no pull, no worktree add/remove, no pull
  request opened (the block forbids it this round).

## Verification

0. Before any write: all four `.remedy-wt/f116-r4/` prepared-file digests verified by a
   worker-written Python sha256 script (`.remedy-wt/f116-r4-worker/verify_hashes.py`): all 4
   matched the prompt's listed sha256 lines exactly — `block.md`
   `58569402f91904968d8b9c9a56b8f5b362ffaa42b8f06e5bf007d339cff703f8` (171 lines, 14508 bytes),
   plus `append-decisions.txt`, `append-live_review.txt` and `dry-plan.md`. `HEAD` read
   `901526c7ee0413a3e4a3f8e64dc473ef7cedfd8b`, equal to `origin/feature/f116-cost-anomaly-alarm`;
   `git status --porcelain` was empty; and `git branch --show-current` read
   `feature/f116-cost-anomaly-alarm` throughout, re-checked before every commit.
1. **C1 copy/append step** (`.remedy-wt/f116-r4-worker/c1_apply.py`): `block.md` copied to
   `.agent/authored/f116-r4.md` (171 lines, byte identical); the two appends to
   `.agent/live_review.md` and `.agent/decisions.md` ran in append (`"ab"`) mode, without reading
   either file whole; `.agent/plan.md` replaced byte-for-byte with `dry-plan.md`. **Proofs**
   (`.remedy-wt/f116-r4-worker/c1_proofs.py`): live_review append proof `True`; decisions append
   proof `True`; authored copy == `block.md` `True`; `plan.md` == `dry-plan.md` `True` (4/4
   `True`). `git diff --cached --numstat` read exactly the four paths the block names. The full
   cached diff was read before committing (self-review): the `plan.md` diff is exactly the Current
   Step, Next Steps and Risks rewrite to round 4, the two appends are each exactly the prepared
   bytes with no reformatting, and the authored copy is new-file-only; no unrelated edit found.
   Committed as `4490c1f457e5fc57e174a2070ca47f564cfa94f9` (short `4490c1f45`).
2. **Gate 1** (`git -C /home/decodeux/Repos/remedy status --porcelain`, run after C4): empty. Byte
   proofs of C1: all `True` (see item 1 above). PASS.
3. **Gate 2** (`.remedy-wt/f116-r4-worker/gate2.py`, run once, from the primary checkout, after
   C4):
   `python3 -m pytest -q -rfEs tests/orchestration/test_job_burn.py
   tests/orchestration/test_burn_detector.py tests/orchestration/test_job_budgets.py
   tests/orchestration/test_predictive_budget.py tests/orchestration/test_job_digest.py
   tests/orchestration/test_budget_stop_integration.py
   tests/orchestration/test_f018_authority_integration.py tests/orchestration/test_disk_floor.py
   tests/cli/test_job_budget_set.py tests/cli/test_job_refusal_envelope.py
   tests/cli/test_exit_codes.py tests/orchestration/test_watchdog.py
   tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py
   tests/orchestration/test_env_registry.py tests/orchestration/test_config.py
   tests/orchestration/test_doc_staleness.py tests/test_ble001_ratchet.py
   tests/test_parametrize_ids_stable.py tests/orchestration/test_durable_write_guard.py
   tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py
   tests/regression/test_resource_safety.py tests/docs/ tests/cli/test_golden_path.py --deselect
   tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes
   --deselect
   tests/ui_server/test_dashboard_contract.py::TestJobSummaryCommandContract::test_typescript_compiles`
   — exit 0. Output tail:
   ```
   ......................................................................   [100%]
   1654 passed, 2 deselected in 112.93s (0:01:52)
   ```
   No FAILED, ERROR or SKIPPED line. Last line verbatim: `1654 passed, 2 deselected in 112.93s
   (0:01:52)`. 15 tests collected from `tests/orchestration/test_job_burn.py` (10 pre-existing plus
   5 this round: the registered-defaults resolver test and four `run_job`-wiring tests),
   confirmed by the block's explicitly-permitted standalone development run of the file alone,
   before C3's commit: `python3 -m pytest -q tests/orchestration/test_job_burn.py` → `15 passed`,
   exit 0; that count did not change between the dev run and Gate 2, so Gate 2's own collection was
   not re-enumerated by a second invocation. PASS.
4. **Gate 3** (`.remedy-wt/f116-r4-worker/gate3.py`: `python3 -m ruff check
   packages/orchestration/pingpong_job.py packages/orchestration/job_burn.py
   packages/orchestration/config.py apps/cli/commands/job.py tests/orchestration/test_job_burn.py
   tests/orchestration/test_job_budgets.py tests/test_no_orphan_modules.py`, from the primary
   checkout): exit 0, `All checks passed!`. PASS.
5. **Gate 4** (`.remedy-wt/f116-r4-worker/gate4.py`: `python3 -m apps.cli.main integrity check
   --json`, run once): exit 0,
   `{"check_count": 6, "checks": [{"message": "handlers=175", "name": "handler_import", "status":
   "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"},
   {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"},
   {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"},
   {"message": "no reviewer scratch, evidence dir or archive at the root", "name":
   "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name":
   "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true,
   "schema_version": 1, "version": 1}`; six of six checks `pass`, `fail_count: 0`. PASS.
6. **Gate 5** (`.remedy-wt/f116-r4-worker/gate5.py`: `python3 -c "import
   scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`,
   run once): `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160',
   'R-1162', 'R-1167']` — exact match to the block's ordered list. PASS.
7. **Gate 6** (after the push): reported in the worker's final reply (not known when this file is
   written).

## Authored-text proofs

- `block.md` → `.agent/authored/f116-r4.md`: 171 / 171 lines, byte-equal, sha256
  `58569402f91904968d8b9c9a56b8f5b362ffaa42b8f06e5bf007d339cff703f8` both sides.
- `append-decisions.txt` appended verbatim to `.agent/decisions.md`: proof `True`.
- `append-live_review.txt` appended verbatim to `.agent/live_review.md`: proof `True`.
- `dry-plan.md` → `.agent/plan.md`: byte-equal, `True`.

## Findings

R-1165 and R-1166 were resolved by C1 (booking the round 3 gate verdict that read them repaired);
R-1167 was registered by C1 (append of `append-live_review.txt`, carrying the finding landed by the
round 3 gate) and repaired by C2: the three `job_burn.*` key descriptions now say the minimum
applies only while no hourly expectation is set, and that with one set the monitor needs one call
more than the window. Its resolution — whether the repair fully closes the finding — is the
reviewer's to write.

## For the operator, in plain sentences

A running job now watches how many tokens each of its calls spends; when the recent calls suddenly
cost much more than the job's earlier ones, the job writes that down with the numbers, and `remedy
job budget` shows it under "recorded burn alarm". The job keeps running for now, and the next round
makes a job that runs without a person pause and ask instead. The descriptions of three of the new
settings were corrected.

## Deviations & assumptions

1. **Commit attribution trailer.** The block's Constraints order "Every commit ends with a
   `Co-Authored-By:` trailer naming the model you run on" — this worker runs on Claude Sonnet 5,
   and a standing harness attribution instruction names `Co-Authored-By: Claude Sonnet 5
   <noreply@anthropic.com>` for commits this session makes. `4490c1f45`, `27ea8a462`, `a3a61a564`
   and `6c80719ed` carry that trailer; this handback's own closing commit will too. Not a
   deviation — the block names "the model you run on", not a fixed string.
2. From the block's ordered commit sequence: none through C4. C1, C2, C3 and C4 landed exactly as
   ordered (the four, two, five and three paths the block names respectively, numstat matching),
   all five pre-C5 gates ran once each and PASS, in order, before this handoff was written. No
   extra commit, none dropped, no reordering.
3. **A ruff auto-fix was applied to `packages/orchestration/pingpong_job.py` before C3's commit**
   (`python3 -m ruff check --fix`), splitting one combined `from packages.orchestration.job_burn
   import (JobBurnMonitor as ..., job_burn_thresholds_from_config as ...)` into two separate `from`
   statements per ruff's I001 import-sort rule. Applied, re-verified by re-running the test file and
   ruff again, and committed as part of C3 — not a behaviour change, a formatting one, on bytes the
   dev-time ruff pass and Gate 3 both then read as clean.
4. **Test names and the stand-in/stub class names** are this worker's choice where the block was
   silent on exact wording: the block specified the cases, sequence and assertions precisely but
   not the Python identifiers. Named per the repository's discoverability conventions (AGENTS.md):
   `_RegisteredDefaultsConfig` for the registry-default stand-in, `_BurnSequenceProvider` for the
   stub whose calls report a scripted token sequence (provider name
   `burn-sequence-stub`, never `fake`, so its calls are counted), and
   `test_run_job_keeps_the_trip_read_before_the_fourth_call` for the central behaviour test.
5. **The shared-counter shape of `_BurnSequenceProvider`.** The block's four-call sequence (1500,
   1500, 15000, 1500) must read in the order `run_job` actually calls builder and reviewer, not in
   each role's own separate count; the test therefore passes ONE `counter` list, shared by the
   builder and reviewer stub instances, as the block's "give the stub its own provider name" clause
   implies but does not spell the mechanism for.
6. **`_cmd_job_budget`'s `_burn_per` local name and the burn-reading rendering's exact line
   breaks** are this worker's choice of expression within the block's exact two line templates
   (`    rate:                ...` and `    window:              ...`, both verified byte-for-byte
   against the block's own text before writing); the literal prefixes match the block exactly.
7. **`TestJobBudgetCliRendersBurnReading`'s helper `_save_with_burn_reading`** sets `burn_reading`
   on the `JobPlan` `_save_budget_job` already persists and re-saves it, rather than extending
   `_save_budget_job` itself with a new parameter — the block said "using its helpers", and this
   keeps `_save_budget_job`'s existing signature and every caller of it byte-for-byte unchanged.
8. Two standalone development runs of a file being written, both explicitly permitted by the
   block's dev-run allowance: `python3 -m pytest -q tests/orchestration/test_job_burn.py`
   (15 passed) before C3's commit, and `python3 -m pytest -q tests/orchestration/test_job_budgets.py`
   (146 passed) before C4's commit. Two further dev-time checks before C3's commit, not named by
   the block's dev-run allowance, declared here as in prior rounds: `python3 -m pytest -q
   tests/test_no_orphan_modules.py` (6 passed) and `python3 -m pytest -q
   tests/orchestration/test_import_reachability.py` (3 passed). A dev-time `ruff check` over the
   touched files also ran before each of C3's and C4's commits, on bytes identical to the committed
   ones, superseded by the formal Gate 3 instance below.
9. Helper scripts under `.remedy-wt/f116-r4-worker/` (gitignored, left untracked) did the digest
   verification, the C1 copy/apply, the byte proofs, the environment-guide regeneration and the
   gate runs; none touched any path outside the ones named per commit, and none wrote to
   `.remedy-wt/f116-r4/` (the reviewer's prepared files, read-only throughout).
10. No `cd` command of any kind was run this round, compound or standalone — every command used
    `git -C /home/decodeux/Repos/remedy`, a `python3 -I` invocation of an absolute script path, or
    a Python `subprocess` call with `cwd=/home/decodeux/Repos/remedy`.
11. `.agent/STOP` was not present at any point checked (before C1, before each gate, and again
    before writing this handback).
12. No mutation and no full suite ran. Gate 2 is the round's one formal test selection; no two test
    commands ran at the same time; `REMEDY_TEST_MAX_WORKERS` was not set and `-n` was not passed.
13. No `Landed:` or `Done:` line was written anywhere.
14. The tracked path set this round is exactly the four paths C1 names, the two paths C2 names,
    the five paths C3 names and the three paths C4 names, plus `.agent/handoff.md` (C5) — matching
    the block's Constraints path set exactly.
15. C1 measured 199 insertions, C2 15, C3 278, C4 115 (each `git show --numstat`'s `+` column), all
    well under the 500-insertion cap; no commit was split.
16. No other departure.

ANY DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE BELONGS HERE: none beyond items 1, 3, 4, 5,
6 and 7 above (continuity, formatting, naming and disclosure notes, not actual departures from the
commit sequence itself).

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop. (Not present as of this handback.)
2. Then rule 2, the Open PR Gate.
3. Then confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Then book round 4's verdict and resolve R-1167 in the next round's first commit.
5. Then T002 unattended: a trip pauses an unattended job with one decision carrying the
   arithmetic.

Operator questions open: 0.
Open findings: 10 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162
and R-1167, Low; R-1167 owned by F116 and repaired, awaiting the reviewer; the rest owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 3, resolve R-1165 and R-1166, register R-1167, DECISION F116 D4, the plan | done | `4490c1f45` |
| C2: the job_burn key descriptions say the minimum binds only the trailing basis (R-1167) | done | `27ea8a462` |
| C3: run_job records every counted call in the burn monitor and keeps the newest trip on the job (T002, DECISION F116 D4) | done | `a3a61a564` |
| C4: remedy job budget shows the recorded burn alarm (T002, DECISION F116 D4) | done | `6c80719ed` |
| Gates 1-5 | done | all PASS, before the handoff was written |
| C5: handback rewrite | done | this commit |
| Push | pending | run right after this commit, reported in the worker's final reply |
| Gate 6 | pending | run after the push, reported in the worker's final reply |
