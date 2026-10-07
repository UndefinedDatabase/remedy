# Handoff — F116 session 2, round 5 (resumed): book round 4, resolve R-1167, register R-1168 and
# R-1169; T002 unattended — a trip pauses an unattended job with one decision, booked against
# DECISION F116 D5

## Session

SESSION 2 of feature F116 · round 5 (resumed) · rounds so far 5

Session 1 ended inside C3 and session 2 resumed it from the uncommitted draft.

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~65 % (T001 built · T002 built · T003, hardening and closure open) — Schätzung

## Range

Review of `8effa367afddb795830c417e1141449a2af60e53`..HEAD (HEAD is this commit, C4 below).

## Commits

### f3952cac2 F116 R5 C1: book round 4, resolve R-1167, register R-1168 and R-1169, DECISION F116 D5, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f116-r5.md` | 149/0 (new) | byte copy of the reviewer's prepared `block.md` |
| `.agent/decisions.md` | 10/0 | append DECISION F116 D5, `append-decisions.txt`'s bytes |
| `.agent/live_review.md` | 8/0 | append the F116 round 4 gate entry plus R-1168 and R-1169, `append-live_review.txt`'s bytes |
| `.agent/plan.md` | 9/10 | replace with the reviewer's prepared `dry-plan.md`, byte for byte |

### 47d00224b F116 R5 C2: no bare finding id in the job_burn key descriptions (R-1169)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/config.py` | 3/3 | R-1169's repair: the three ` (R-1167)` tokens deleted from the `job_burn.*` descriptions, each final full stop kept |
| `docs/guides/environment.md` | 3/3 | regenerated from the registry; the three corrected rows |

### e1734aab3 F116 R5 C3: a trip pauses an unattended job with one burn_alarm decision (T002, DECISION F116 D5; R-1168)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/job_burn.py` | 54/5 | D5 (1) and (2): `job_approved_unattended`, `BURN_DECISION_MARKER`, `BURN_PAUSE_SOURCE` and `job_burn_sentence`, each with a WHY comment; the docstring names the one import inside `job_approved_unattended`; `RATE_UNIT_PER_HOUR` imported |
| `packages/orchestration/pingpong_job.py` | 72/0 | D5 (3): inside the burn branch of `_stop_check`, after the new record is persisted, an unattended job gets the pause request (a `PauseControlError` returns the error signal), then the open `[burn_alarm]` decision updated in place or one enqueued, then `_persist_job`; plus a 6-line addition to the in-task halt handling so a failed pause request blocks the job (see Deviations 2) |
| `tests/orchestration/test_job_burn.py` | 200/1 | the attended spike test also asserts the job completed; a stand-in that reads the job from disk at its fourth call; `job_approved_unattended` true and false cases; `job_burn_sentence` per-sample and per-hour; the unattended run pausing with one decision; the open decision updated in place; the failing pause request blocking the job; `_run_burn_job` gains an optional `prepare` hook |

### F116 R5 C4: handback (self-reference exception — the handoff is committed by this same commit)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |
| `.agent/authored/f116-r5-resume.md` | this commit | byte copy of the resume instruction, 34 lines |

## External actions

- `git push origin feature/f116-cost-anomaly-alarm` once, after C4: outcome reported in the
  worker's final reply (write-once rule; not known when this file is written).
- No merge, no branch switch, no new branch, no force-push, no pull, no worktree add/remove, no
  pull request opened.

## Verification

0. Before any write: `git rev-parse HEAD` read `47d00224b71ccdff0c6256d5aa7d92607506cf1b`;
   `git status --porcelain` listed exactly the three C3 paths; `.agent/STOP` was absent. The
   resume file's sha256 read `c4c730dd27645a2f545062f5c0169bf98ae51e0fa226f96465942e781f62f915`
   and `.agent/authored/f116-r5.md` read
   `27b1d65ac961047657edb6b5c33c9a62cff5a7f6a109c4e0ac62afc73935e50e` (149 lines).
1. **Gate 1** (`git -C /home/decodeux/Repos/remedy status --porcelain`, then
   `.remedy-wt/f116-r5-worker/c1_proofs.py`, which still applies to C1's bytes): status empty;
   live_review append, decisions append, authored copy and plan proofs all `True`. PASS.
2. **Gate 2** (`.remedy-wt/f116-r5-worker/gates.py 2`, run once, from the primary checkout, after
   C3): the block's pytest command, exit 0, no FAILED, ERROR or SKIPPED line. Last line:
   `1070 passed, 2 deselected in 104.88s (0:01:44)`. 23 tests collected from
   `tests/orchestration/test_job_burn.py` (confirmed by the standalone development run: `23
   passed`). PASS.
3. **Gate 3** (`python3 -m ruff check packages/orchestration/pingpong_job.py
   packages/orchestration/job_burn.py packages/orchestration/config.py
   tests/orchestration/test_job_burn.py`): exit 1, **RED**, not re-run and not repaired, per the
   block's red-gate rule. Two findings:
   - `I001 [*] Import block is un-sorted or un-formatted` at `packages/orchestration/job_burn.py:26`
     (`RATE_UNIT_PER_HOUR` sits after `BurnThresholds` in the `burn_detector` import and ruff wants
     it first);
   - `F401 [*] packages.orchestration.burn_detector.BASIS_CLASS_DEFAULT imported but unused` at
     `tests/orchestration/test_job_burn.py:15`.
   `Found 2 errors. [*] 2 fixable with the --fix option.` Both are import hygiene in C3's bytes
   (one was the session 1 draft's, one was the draft's test imports); no behaviour is involved.
4. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, six of six checks
   `pass`, `"fail_count": 0`. PASS.
5. **Gate 5** (`scripts.rotate_live_review.open_finding_ids`): exit 0,
   `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162',
   'R-1168', 'R-1169']` — exact match. PASS.
6. **Gate 6** (after the push): reported in the worker's final reply (not known when this file is
   written).

## Authored-text proofs

- `block.md` → `.agent/authored/f116-r5.md`: 149 lines, byte-equal (gate 1 proof `True`), sha256
  `27b1d65ac961047657edb6b5c33c9a62cff5a7f6a109c4e0ac62afc73935e50e`.
- `append-decisions.txt` and `append-live_review.txt` appended verbatim: proofs `True`.
- `dry-plan.md` → `.agent/plan.md`: byte-equal, `True`.
- `.remedy-wt/f116-r5-resume/resume.md` → `.agent/authored/f116-r5-resume.md`: 34 lines, byte-equal,
  sha256 `c4c730dd27645a2f545062f5c0169bf98ae51e0fa226f96465942e781f62f915` both sides.

## Findings

R-1167 was resolved by C1. R-1168 and R-1169 were registered by C1 and repaired by C3 and C2; their
resolutions are the reviewer's to write. New: gate 3 is red on two import-hygiene lines in C3's
bytes (see Verification 3); they are not registered here.

## For the operator, in plain sentences

A job that was approved to run without a person, as `remedy do run --yes` does, now pauses itself
before its next call when its recent calls suddenly cost far more than its earlier ones. It leaves
one question for a person that says, in a full sentence, how much the calls spent and what was
expected, with the answers "resume" and "abandon". `remedy job unpause` lets it continue. A job a
person started keeps running and only records the warning. Three setting descriptions no longer
carry an internal reference number.

## Deviations & assumptions

1. Session 1 ended inside C3; this session resumed from the uncommitted draft of the three C3
   paths and edited it rather than discarding it. Drafted lines kept unchanged: all of `job_burn.py`
   and the whole burn-branch block in `pingpong_job.py` (they match D5 (1) to (3) and the block's
   two sentences exactly). Drafted lines changed: none in those two files except as in item 2; in
   `tests/orchestration/test_job_burn.py` the draft held only imports, which I kept and extended
   (`BASIS_CLASS_DEFAULT` was in the draft and is unused, causing gate 3's F401).
2. **Production addition beyond the draft.** The block's failing-pause-request test (job ends
   blocked) failed against the draft: the in-task halt handling re-derives the pause with
   `_pause_park_signal(in_flight_task=task)`, which finds nothing on disk when `request_pause`
   itself failed, so the job fell through to an ordinary stop and ended `running`. I added six
   lines in `pingpong_job.py` right after the `_park_job` return in that halt branch: when
   `_reason_is_pause_error(_halt_reason)` holds and nothing was re-read, the job is blocked with
   `_block_for_pause_error`. Reviewer please confirm this widening of D5 (3) is acceptable.
3. **Gate 3 is red** and was not re-run or repaired, per the block's rule (Verification 3). The
   handoff is written and the branch pushed as ordered. The two fixes are `ruff --fix` (sort the
   import, drop `BASIS_CLASS_DEFAULT`).
4. Test names and the stand-ins (`_DiskReadingProvider`, `_approve_unattended`,
   `_run_unattended_spike`) are this worker's choice; the block fixed the behaviours, not the
   identifiers. `_run_burn_job` gained a `prepare` hook (default None) so a test can set the
   plan's `task_plan` or seed a decision before the plan is saved.
5. Two standalone runs of `tests/orchestration/test_job_burn.py` (the second after the item 2
   addition), both permitted for a file being written; gate 2 ran once. No mutation, no full suite,
   no `-n`, no `REMEDY_TEST_MAX_WORKERS`, no `cd`, nothing written under `/tmp` by the worker.
6. C3 measured 326 insertions, C4 well under the cap; no commit was split. No `Landed:` or `Done:`
   line was written.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then rule 2, the Open PR Gate.
3. Then confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Then book round 5's verdict and resolve R-1168 and R-1169 in the next round's first commit; the
   same commit repairs gate 3's two import lines.
5. Then T003: the watchdog's burn tripwire calls the detector.

Operator questions open: 0.
Open findings: 11 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1168 and R-1169, Low; R-1168 and R-1169 owned by F116 and repaired, awaiting the reviewer; the
rest owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 4, resolve R-1167, register R-1168 and R-1169, DECISION F116 D5, the plan | done | `f3952cac2` |
| C2: no bare finding id in the job_burn key descriptions (R-1169) | done | `47d00224b` |
| C3: a trip pauses an unattended job with one burn_alarm decision (T002, DECISION F116 D5; R-1168) | done | `e1734aab3`; with the item 2 addition |
| Gates 1, 2, 4, 5 | done | PASS |
| Gate 3 | deviated | RED, two import-hygiene lines, not re-run per the block |
| C4: handback | done | this commit |
| Push | pending | run right after this commit, reported in the worker's final reply |
| Gate 6 | pending | run after the push, reported in the worker's final reply |
