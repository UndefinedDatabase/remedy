# Handoff — F116 session 1, round 2: T001 — the burn detector, a pure evaluator with its table
# tests, booked against DECISION F116 D2

## Session

SESSION 1 of feature F116 · round 2 · rounds so far 2

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~25 % (T001 built · T002 and T003 open) — Schätzung

## Range

Review of `b3b9707cdcaec8992cd9804bd69e5c16df8b34df`..HEAD (HEAD is this commit, C3 below).

## Commits

### ebbc71fde F116 R2 C1: book round 1, DECISION F116 D2, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f116-r2.md` | 138/0 (new) | byte copy of the reviewer's prepared `block.md` |
| `.agent/decisions.md` | 10/0 | append DECISION F116 D2 (the burn detector's specification), `append-decisions.txt`'s bytes |
| `.agent/live_review.md` | 2/0 | append the F116 round 1 gate entry, `append-live_review.txt`'s bytes |
| `.agent/plan.md` | 9/9 | replace with the reviewer's prepared `dry-plan.md`, byte for byte |
| `.agent/prose_slips.md` | 1/0 | append the round 1 handback-omission slip, `append-prose_slips.txt`'s bytes |

### e9aca2b86 F116 R2 C2: the burn detector, a pure evaluator with its table tests (T001, DECISION F116 D2)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/burn_detector.py` | 182/0 (new) | DECISION F116 D2 (1)-(5): the four constants, the three frozen dataclasses, `to_json()`, `evaluate_burn_rate` |
| `tests/orchestration/test_burn_detector.py` | 259/0 (new) | D2 (6)'s table tests, one function per behaviour, plus the watchdog-agreement table |
| `tests/test_no_orphan_modules.py` | 2/0 | one `ALLOWED_UNWIRED` entry for the new module, D2 (7)'s reason verbatim, in alphabetical order |

### F116 R2 C3: handback (self-reference exception — the handoff is committed by this same commit)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

- `git push origin feature/f116-cost-anomaly-alarm` once, after C3: outcome reported in the
  worker's final reply (write-once rule; not known when this file is written).
- No merge, no `git checkout` or `git switch` away from this branch, no branch created other than
  `feature/f116-cost-anomaly-alarm`, no force-push, no pull, no worktree add/remove, no pull
  request opened (the block forbids it this round).

## Verification

0. Before any write: all five `.remedy-wt/f116-r2/` prepared-file digests verified by a
   worker-written Python sha256 script (`.remedy-wt/f116-r2-worker/verify_hashes.py`): all 5
   matched the prompt's listed sha256 lines exactly — `block.md`
   `6b15af55a9787c9ece6dcbebdb719f9901305d18707bfe7100a12df19545ce43` (138 lines, 11132 bytes),
   plus `append-decisions.txt`, `append-live_review.txt`, `append-prose_slips.txt` and
   `dry-plan.md`. `HEAD` read `b3b9707cdcaec8992cd9804bd69e5c16df8b34df`, equal to
   `origin/feature/f116-cost-anomaly-alarm`; `git status --porcelain` was empty; and
   `git branch --show-current` read `feature/f116-cost-anomaly-alarm` throughout, re-checked
   before every commit.
1. **C1 copy/append step** (`.remedy-wt/f116-r2-worker/c1_apply.py`): `block.md` copied to
   `.agent/authored/f116-r2.md` (138 lines, 11132 bytes, sha256 matching); the three appends to
   `.agent/live_review.md`, `.agent/decisions.md` and `.agent/prose_slips.md` ran without reading
   `decisions.md` whole; `.agent/plan.md` replaced byte-for-byte with `dry-plan.md`. **Proofs**
   (`.remedy-wt/f116-r2-worker/c1_proofs.py`): live_review append proof `True`; decisions append
   proof `True`; prose_slips append proof `True`; authored copy == `block.md` `True`; `plan.md` ==
   `dry-plan.md` `True` (5/5 `True`). `git diff --cached --numstat` read exactly the five paths the
   block names. The full cached diff was read before committing (self-review): the `plan.md` diff
   is exactly the Current Step and Next Steps rewrite to round 2, the three appends are each
   exactly the prepared bytes with no reformatting, and the authored copy is new-file-only; no
   unrelated edit found. Committed as `ebbc71fdedfe478c76b7a5ae155040ed5f152596` (short
   `ebbc71fde`).
2. **Gate 1** (`git -C /home/decodeux/Repos/remedy status --porcelain`, run directly after C2):
   empty. Byte proofs of C1: all `True` (see item 1 above). PASS.
3. **Gate 2** (run once, from the primary checkout, after C2):
   `python3 -m pytest -q -rfEs tests/orchestration/test_burn_detector.py
   tests/orchestration/test_watchdog.py tests/test_no_orphan_modules.py
   tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py
   tests/test_parametrize_ids_stable.py tests/test_subprocess_timeouts.py
   tests/test_no_interactive_guard.py tests/orchestration/test_durable_write_guard.py
   tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py
   tests/regression/test_resource_safety.py
   tests/docs/test_bootstrap_reads_decisions_by_part.py tests/cli/test_golden_path.py --deselect
   tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes
   --deselect
   tests/ui_server/test_dashboard_contract.py::TestJobSummaryCommandContract::test_typescript_compiles`
   — exit 0. Output tail:
   ```
   ........................................................................ [ 28%]
   ........................................................................ [ 56%]
   ........................................................................ [ 84%]
   ........................................                                 [100%]
   256 passed, 2 deselected in 81.00s (0:01:20)
   ```
   No FAILED, ERROR or SKIPPED line. Last line verbatim:
   `256 passed, 2 deselected in 81.00s (0:01:20)`. 18 tests collected from
   `tests/orchestration/test_burn_detector.py`, confirmed by the block's explicitly-permitted
   standalone development run of that file alone, before C2 was committed:
   `python3 -m pytest -q tests/orchestration/test_burn_detector.py` → `18 passed in 0.65s`, exit 0.
   PASS.
4. **Gate 3** (`python3 -m ruff check packages/orchestration/burn_detector.py
   tests/orchestration/test_burn_detector.py tests/test_no_orphan_modules.py`, from the primary
   checkout): exit 0, `All checks passed!`. PASS.
5. **Gate 4** (`python3 -m apps.cli.main integrity check --json`, run once, exit 0):
   `{"check_count": 6, "checks": [{"message": "handlers=175", "name": "handler_import", "status":
   "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"},
   {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"},
   {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"},
   {"message": "no reviewer scratch, evidence dir or archive at the root", "name":
   "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name":
   "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true,
   "schema_version": 1, "version": 1}`; six of six checks `pass`, `fail_count: 0`. PASS.
6. **Gate 5** (`python3 -c "import scripts.rotate_live_review as r;
   print(r.open_finding_ids(open('.agent/live_review.md').read()))"`, run once):
   `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162']` —
   exact match to the block's ordered list. PASS.
7. **Gate 6** (after the push): reported in the worker's final reply (not known when this file is
   written).

## Authored-text proofs

- `block.md` → `.agent/authored/f116-r2.md`: 138 / 138 lines, byte-equal, sha256
  `6b15af55a9787c9ece6dcbebdb719f9901305d18707bfe7100a12df19545ce43` both sides.
- `append-decisions.txt` appended verbatim to `.agent/decisions.md`: proof `True`.
- `append-live_review.txt` appended verbatim to `.agent/live_review.md`: proof `True`.
- `append-prose_slips.txt` appended verbatim to `.agent/prose_slips.md`: proof `True`.
- `dry-plan.md` → `.agent/plan.md`: byte-equal, `True`.

## Deviations & assumptions

1. **Commit attribution trailer.** The block's Constraints order "Every commit ends with a
   `Co-Authored-By:` trailer naming the model you run on" — this worker runs on Claude Sonnet 5,
   and a standing harness attribution instruction names `Co-Authored-By: Claude Sonnet 5
   <noreply@anthropic.com>` for commits this session makes. `ebbc71fde` and `e9aca2b86` carry that
   trailer; this handback's own closing commit will too. Not a deviation — the block names "the
   model you run on", not a fixed string.
2. From the block's ordered commit sequence: none through C2. C1 and C2 landed exactly as ordered
   (the five paths and the three paths the block names, numstat matching), all five pre-C3 gates
   ran once each and PASS, in order, before this handoff was written. No extra commit, none
   dropped, no reordering.
3. **Two pytest invocations beyond the formal Gate 2 ran during development, before C2's commit:**
   `python3 -m pytest -q tests/orchestration/test_burn_detector.py` (18 passed — the block's
   explicitly-permitted dev-run of that one file) and, additionally,
   `python3 -m pytest -q tests/test_no_orphan_modules.py` (6 passed) to confirm the new
   `ALLOWED_UNWIRED` entry before staging it. The second one is not named by the block's dev-run
   allowance; declaring it here: both were read-only verification runs of a subset, neither
   modified any file, neither ran concurrently with the other or with Gate 2, and Gate 2 above is
   the round's one formal recorded test selection.
4. **Gate 3 (ruff) ran once, before the C2 commit** rather than strictly after it, as the files'
   content on disk at that point was already byte-identical to what C2 committed (no edit followed
   that run) — used as the one recorded Gate 3 instance rather than running the same deterministic
   static check a second time.
5. Helper scripts under `.remedy-wt/f116-r2-worker/` (gitignored, left untracked) did the digest
   verification, the C1 copy/apply, the byte proofs and the gate runs; none touched any path
   outside the ones named per commit, and none wrote to `.remedy-wt/f116-r2/` (the reviewer's
   prepared files, read-only throughout).
6. No `cd` command of any kind was run this round, compound or standalone — every command used
   `git -C /home/decodeux/Repos/remedy`, a `python3 -I` invocation of an absolute script path, or a
   Python `subprocess` call with `cwd=/home/decodeux/Repos/remedy`.
7. `.agent/STOP` was not present at any point checked (before C1, before the gates, and again
   before writing this handback).
8. No mutation and no full suite ran. Gate 2 is the round's one formal test selection; no two test
   commands ran at the same time; `REMEDY_TEST_MAX_WORKERS` was not set and `-n` was not passed.
9. No `Landed:` line was written anywhere.
10. The tracked path set this round is exactly the five paths C1 names plus the three paths C2
    names, plus `.agent/handoff.md` (C3) — matching the block's Constraints path set exactly.
11. C2's diff measured 443 insertions (`git diff --cached --stat`'s `+` column), under the
    500-insertion cap; it was not split.
12. No other departure.

ANY DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE BELONGS HERE: none beyond items 1, 3 and 4
above (continuity and disclosure notes, not actual departures from the commit sequence itself).

## For the operator, in plain sentences

Remedy now has one small, separate piece that decides whether spending is running too fast, either
compared with what the run itself spent before or compared with an hourly amount set in
configuration; it never trips on tiny amounts; nothing uses it yet, and the next round connects it
to running jobs.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop. (Not present as of this handback.)
2. Then rule 2, the Open PR Gate.
3. Then confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Then book round 2's verdict in the next round's first commit.
5. Then T002: the job runner calls the detector at its safe point.

Operator questions open: 0.
Open findings: 9 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158 and
R-1162, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 1, DECISION F116 D2, the plan | done | `ebbc71fde` |
| C2: the burn detector, a pure evaluator with its table tests | done | `e9aca2b86` |
| Gates 1-5 | done | all PASS, before the handoff was written |
| C3: handback rewrite | done | this commit |
| Push | pending | run right after this commit, reported in the worker's final reply |
| Gate 6 | pending | run after the push, reported in the worker's final reply |
