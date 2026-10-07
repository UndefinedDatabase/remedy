# Handoff — F116 session 1, round 3: repair R-1165 and R-1166; T002 first part — the job burn
# monitor and its configuration keys, booked against DECISION F116 D3

## Session

SESSION 1 of feature F116 · round 3 · rounds so far 3

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~35 % (T001 built · T002 first part built · T002 wiring, T002 unattended and T003
open) — Schätzung

## Range

Review of `21cdd3537a01c7382720cc6c2d09dcce6a8e8bc0`..HEAD (HEAD is this commit, C4 below).

## Commits

### dd2b8c637 F116 R3 C1: book round 2, register R-1165 and R-1166, DECISION F116 D3, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f116-r3.md` | 146/0 (new) | byte copy of the reviewer's prepared `block.md` |
| `.agent/decisions.md` | 10/0 | append DECISION F116 D3 (the job burn monitor's specification), `append-decisions.txt`'s bytes |
| `.agent/live_review.md` | 6/0 | append the F116 round 2 gate entry plus R-1165 and R-1166, `append-live_review.txt`'s bytes |
| `.agent/plan.md` | 13/13 | replace with the reviewer's prepared `dry-plan.md`, byte for byte |

### fdf09714e F116 R3 C2: pin the detector's strict trip comparison and correct its docstring (R-1165, R-1166)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/burn_detector.py` | 1/1 | R-1166: the module docstring names the job runner from T002 on, the watchdog from T003 on |
| `tests/orchestration/test_burn_detector.py` | 58/0 | R-1165: two equality-boundary tests (trailing and per-hour) plus a second agreement table at the watchdog's real minimum, with a zero-valued baseline and the equality boundary |

### 36475a6f2 F116 R3 C3: the job burn monitor and its configuration keys (T002, DECISION F116 D3)

| Path | +/- | Reason |
|---|---|---|
| `docs/guides/environment.md` | 5/0 | regenerated from the registry, the five new `job_burn.*` rows |
| `packages/orchestration/config.py` | 66/0 | the five `job_burn.*` `ConfigKeySpec` entries, directly after `watchdog.burn_multiplier` |
| `packages/orchestration/job_burn.py` | 126/0 (new) | DECISION F116 D3 (2): `JOB_BURN_UNIT`, `job_burn_thresholds_from_config`, `job_burn_record`, `JobBurnMonitor` |
| `tests/orchestration/test_job_burn.py` | 174/0 (new) | D3 (3)'s tests, one function per behaviour: the resolver, `record_call`'s amount and labelling rules, `reading()`, the default thresholds' trip/floor/too-few cases, `job_burn_record` |
| `tests/test_no_orphan_modules.py` | 2/2 | `ALLOWED_UNWIRED`: `burn_detector.py`'s entry deleted (its first production importer exists now), `job_burn.py`'s entry added, D3 (4)'s reason verbatim |

### F116 R3 C4: handback (self-reference exception — the handoff is committed by this same commit)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

- `git push origin feature/f116-cost-anomaly-alarm` once, after C4: outcome reported in the
  worker's final reply (write-once rule; not known when this file is written).
- No merge, no `git checkout` or `git switch` away from this branch, no branch created other than
  `feature/f116-cost-anomaly-alarm`, no force-push, no pull, no worktree add/remove, no pull
  request opened (the block forbids it this round).

## Verification

0. Before any write: all four `.remedy-wt/f116-r3/` prepared-file digests verified by a
   worker-written Python sha256 script (`.remedy-wt/f116-r3-worker/verify_hashes.py`): all 4
   matched the prompt's listed sha256 lines exactly — `block.md`
   `ba711972d97ce8a54714e316ba82f58493f326e751bc1db77970bfc3e0cd98aa` (146 lines, 12009 bytes),
   plus `append-decisions.txt`, `append-live_review.txt` and `dry-plan.md`. `HEAD` read
   `21cdd3537a01c7382720cc6c2d09dcce6a8e8bc0`, equal to `origin/feature/f116-cost-anomaly-alarm`;
   `git status --porcelain` was empty; and `git branch --show-current` read
   `feature/f116-cost-anomaly-alarm` throughout, re-checked before every commit.
1. **C1 copy/append step** (`.remedy-wt/f116-r3-worker/c1_apply.py`): `block.md` copied to
   `.agent/authored/f116-r3.md` (146 lines, 12009 bytes, sha256 matching); the two appends to
   `.agent/live_review.md` and `.agent/decisions.md` ran in append (`"ab"`) mode, without reading
   either file whole; `.agent/plan.md` replaced byte-for-byte with `dry-plan.md`. **Proofs**
   (`.remedy-wt/f116-r3-worker/c1_proofs.py`): live_review append proof `True`; decisions append
   proof `True`; authored copy == `block.md` `True`; `plan.md` == `dry-plan.md` `True` (4/4
   `True`). `git diff --cached --numstat` read exactly the four paths the block names. The full
   cached diff was read before committing (self-review): the `plan.md` diff is exactly the Current
   Step and Next Steps rewrite to round 3, the two appends are each exactly the prepared bytes with
   no reformatting, and the authored copy is new-file-only; no unrelated edit found. Committed as
   `dd2b8c637ec5916192613d84a5b3708ed81d4f22` (short `dd2b8c637`).
2. **Gate 1** (`git -C /home/decodeux/Repos/remedy status --porcelain`, run directly after C3):
   empty. Byte proofs of C1: all `True` (see item 1 above). PASS.
3. **Gate 2** (`.remedy-wt/f116-r3-worker/gate2.py`, run once, from the primary checkout, after
   C3):
   `python3 -m pytest -q -rfEs tests/orchestration/test_burn_detector.py
   tests/orchestration/test_job_burn.py tests/orchestration/test_watchdog.py
   tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py
   tests/orchestration/test_env_registry.py tests/orchestration/test_config.py
   tests/orchestration/test_doc_staleness.py tests/test_ble001_ratchet.py
   tests/test_parametrize_ids_stable.py tests/orchestration/test_test_runner.py
   tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/docs/
   tests/cli/test_golden_path.py --deselect
   tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes
   --deselect
   tests/ui_server/test_dashboard_contract.py::TestJobSummaryCommandContract::test_typescript_compiles`
   — exit 0. Output tail:
   ```
   ........................................................................ [ 89%]
   .                                                                        [100%]
   721 passed, 2 deselected in 81.16s (0:01:21)
   ```
   No FAILED, ERROR or SKIPPED line. Last line verbatim: `721 passed, 2 deselected in 81.16s
   (0:01:21)`. Per-file collected counts: 24 tests collected from
   `tests/orchestration/test_burn_detector.py` (18 pre-existing plus 6 this round: two
   equality-boundary tests and a 4-case parametrized agreement table) and 10 tests collected from
   `tests/orchestration/test_job_burn.py` (all new this round); both confirmed by the block's
   explicitly-permitted standalone development runs of each file alone, before C2's and C3's
   commits respectively: `python3 -m pytest -q tests/orchestration/test_burn_detector.py` →
   `24 passed in 0.47s`, and `python3 -m pytest -q tests/orchestration/test_job_burn.py` →
   `10 passed in 0.45s`, both exit 0; neither file's test count changed between that dev run and
   Gate 2, so Gate 2's own collection was not re-enumerated by a second invocation. PASS.
4. **Gate 3** (`.remedy-wt/f116-r3-worker/gate3.py`: `python3 -m ruff check
   packages/orchestration/burn_detector.py packages/orchestration/job_burn.py
   packages/orchestration/config.py tests/orchestration/test_burn_detector.py
   tests/orchestration/test_job_burn.py tests/test_no_orphan_modules.py`, from the primary
   checkout): exit 0, `All checks passed!`. PASS.
5. **Gate 4** (`.remedy-wt/f116-r3-worker/gate4.py`: `python3 -m apps.cli.main integrity check
   --json`, run once): exit 0,
   `{"check_count": 6, "checks": [{"message": "handlers=175", "name": "handler_import", "status":
   "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"},
   {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"},
   {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"},
   {"message": "no reviewer scratch, evidence dir or archive at the root", "name":
   "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name":
   "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true,
   "schema_version": 1, "version": 1}`; six of six checks `pass`, `fail_count: 0`. PASS.
6. **Gate 5** (`.remedy-wt/f116-r3-worker/gate5.py`: `python3 -c "import
   scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`,
   run once): `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160',
   'R-1162', 'R-1165', 'R-1166']` — exact match to the block's ordered list. PASS.
7. **Gate 6** (after the push): reported in the worker's final reply (not known when this file is
   written).

## Authored-text proofs

- `block.md` → `.agent/authored/f116-r3.md`: 146 / 146 lines, byte-equal, sha256
  `ba711972d97ce8a54714e316ba82f58493f326e751bc1db77970bfc3e0cd98aa` both sides.
- `append-decisions.txt` appended verbatim to `.agent/decisions.md`: proof `True`.
- `append-live_review.txt` appended verbatim to `.agent/live_review.md`: proof `True`.
- `dry-plan.md` → `.agent/plan.md`: byte-equal, `True`.

## Findings

R-1165 and R-1166 were registered by C1 (append of `append-live_review.txt`, carrying both
findings as landed by the round 2 gate) and repaired by C2: R-1165 by the two equality-boundary
tests and the second agreement table at the watchdog's real minimum; R-1166 by the one-sentence
docstring correction. Their resolution — whether the repair fully closes each finding — is the
reviewer's to write.

## Deviations & assumptions

1. **Commit attribution trailer.** The block's Constraints order "Every commit ends with a
   `Co-Authored-By:` trailer naming the model you run on" — this worker runs on Claude Sonnet 5,
   and a standing harness attribution instruction names `Co-Authored-By: Claude Sonnet 5
   <noreply@anthropic.com>` for commits this session makes. `dd2b8c637`, `fdf09714e` and
   `36475a6f2` carry that trailer; this handback's own closing commit will too. Not a deviation —
   the block names "the model you run on", not a fixed string.
2. From the block's ordered commit sequence: none through C3. C1, C2 and C3 landed exactly as
   ordered (the four, two and five paths the block names respectively, numstat matching), all five
   pre-C4 gates ran once each and PASS, in order, before this handoff was written. No extra commit,
   none dropped, no reordering.
3. **Test names, the ids for the parametrized tables, and the two equality-boundary tests' test
   names** are this worker's choice where the block was silent on exact wording: the block
   specified the cases, thresholds and assertions precisely but not the Python identifiers. Named
   per the repository's discoverability conventions (AGENTS.md): e.g.
   `test_trailing_basis_equality_boundary_does_not_trip`,
   `test_the_trailing_basis_agrees_with_the_watchdog_at_a_real_minimum`, and the
   `_AGREEMENT_BOUNDARY_CASES` ids `trips_at_the_window_floor`, `too_few_samples_returns_none`,
   `zero_valued_baseline_trips_on_any_positive_window`, `the_equality_boundary_does_not_trip`.
4. **The resolver's own defaults object.** DECISION F116 D3 (3) states `job_burn.min_spend_tokens`
   defaults to 20000, which differs from `BurnThresholds`' own generic dataclass default of `0.0`
   for `min_spend` (that field's default reflects no caller's chosen floor, not job burn's one).
   `job_burn_thresholds_from_config` therefore builds its "no override" baseline as
   `BurnThresholds(min_spend=20000.0)` rather than the bare `BurnThresholds()` the watchdog's own
   resolver uses as its `defaults` object — the only field that needed overriding, named here
   because the "resolver shape to copy" the block pointed at uses the bare dataclass default
   everywhere.
5. **`_call_amount`, `JobBurnMonitor` and its `_samples` list are private** (leading underscore /
   instance attribute), matching `burn_detector.py`'s own `_is_measured` and `_is_aware` naming;
   `tests/orchestration/test_job_burn.py` reads `monitor._samples` directly in three tests
   (`test_record_call_sums_input_and_output_tokens_and_labels_by_position`,
   `test_unmeasured_usage_records_a_sample_with_no_amount`,
   `test_usage_missing_output_tokens_records_the_input_tokens_alone`) because `record_call`'s
   return is `None` and `reading()` needs `min_samples + window` recorded calls before it answers
   anything — the block's own wording ("records an amount of 1500 ... with the given `at` and
   label 1, then 2 for the next call") is about what one call appends, which only the instance's
   own list shows directly with two or three calls in hand. Not a deviation from the block's
   specified behaviour; a disclosed test-implementation choice.
6. Two standalone development runs of a file being written, both explicitly permitted by the
   block's dev-run allowance: `python3 -m pytest -q tests/orchestration/test_burn_detector.py`
   (24 passed) before C2's commit, and `python3 -m pytest -q tests/orchestration/test_job_burn.py`
   (10 passed) before C3's commit. A third dev-time check, `python3 -m pytest -q
   tests/test_no_orphan_modules.py` (6 passed), also ran before C3's commit to confirm the
   `ALLOWED_UNWIRED` edit; not named by the block's dev-run allowance, declared here as in round 2.
   A dev-time `ruff check` over all six touched Python files also ran before C3's commit, on bytes
   identical to the committed ones, superseded by the formal Gate 3 instance below.
7. Helper scripts under `.remedy-wt/f116-r3-worker/` (gitignored, left untracked) did the digest
   verification, the C1 copy/apply, the byte proofs, the environment-guide regeneration and the
   gate runs; none touched any path outside the ones named per commit, and none wrote to
   `.remedy-wt/f116-r3/` (the reviewer's prepared files, read-only throughout).
8. No `cd` command of any kind was run this round, compound or standalone — every command used
   `git -C /home/decodeux/Repos/remedy`, a `python3 -I` invocation of an absolute script path, or a
   Python `subprocess` call with `cwd=/home/decodeux/Repos/remedy`.
9. `.agent/STOP` was not present at any point checked (before C1, before each gate, and again
   before writing this handback).
10. No mutation and no full suite ran. Gate 2 is the round's one formal test selection; no two test
    commands ran at the same time; `REMEDY_TEST_MAX_WORKERS` was not set and `-n` was not passed.
11. No `Landed:` or `Done:` line was written anywhere.
12. The tracked path set this round is exactly the four paths C1 names, the two paths C2 names and
    the five paths C3 names, plus `.agent/handoff.md` (C4) — matching the block's Constraints path
    set exactly.
13. C1 measured 175 insertions, C2 59, C3 373 (each `git show --numstat`'s `+` column), all under
    the 500-insertion cap; none was split. (C3's block anticipated a possible split past 500; it
    was not needed.)
14. No other departure.

ANY DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE BELONGS HERE: none beyond items 1, 3, 4, 5
and 6 above (continuity, naming and disclosure notes, not actual departures from the commit
sequence itself).

## For the operator, in plain sentences

The spending check now has a strict boundary test, so spending exactly at the limit never counts
as too fast. Remedy has a new piece that counts the tokens of every call a job makes, and five new
settings control how sensitive the alarm is, all listed in the environment guide. By default it
compares a job with its own earlier calls and ignores any burst smaller than twenty thousand
tokens. Jobs do not use it yet, and the next round connects it.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop. (Not present as of this handback.)
2. Then rule 2, the Open PR Gate.
3. Then confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Then book round 3's verdict and resolve R-1165 and R-1166 in the next round's first commit.
5. Then T002 wiring: `run_job` records each counted call in the monitor and evaluates at its safe
   point.

Operator questions open: 0.
Open findings: 11 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1165 and R-1166, Low; R-1165 and R-1166 owned by F116 and repaired, awaiting the reviewer; the
rest owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 2, register R-1165 and R-1166, DECISION F116 D3, the plan | done | `dd2b8c637` |
| C2: pin the detector's strict trip comparison and correct its docstring (R-1165, R-1166) | done | `fdf09714e` |
| C3: the job burn monitor and its configuration keys (T002, DECISION F116 D3) | done | `36475a6f2` |
| Gates 1-5 | done | all PASS, before the handoff was written |
| C4: handback rewrite | done | this commit |
| Push | pending | run right after this commit, reported in the worker's final reply |
| Gate 6 | pending | run after the push, reported in the worker's final reply |
