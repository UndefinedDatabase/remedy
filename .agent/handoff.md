# Handoff — F116 session 3, round 6: book round 5, resolve R-1168 and R-1169, register R-1170 and
# R-1171, repair both; T003 first half — the watchdog's burn tripwire calls the burn detector
# (DECISION F116 D6)

## Session

SESSION 3 of feature F116 · round 6 · rounds so far 6

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~75 % (T001 built · T002 built · T003 first half built · T003 second half, hardening and closure open) — Schätzung

## Range

Review of `cf6b6868ac56a30a9c6e0f34a20bdadcbc4b1d73`..HEAD (HEAD is this commit, C5 below).

## Commits

### a10a877a6 F116 R6 C1: book round 5, resolve R-1168 and R-1169, register R-1170 and R-1171, DECISION F116 D6, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f116-r6.md` | 124/0 (new) | byte copy of the reviewer's prepared `block.md` |
| `.agent/decisions.md` | 10/0 | append DECISION F116 D6, `append-decisions.txt`'s bytes |
| `.agent/live_review.md` | 10/0 | append the F116 round 5 gate entry, R-1168 and R-1169 resolutions, R-1170 and R-1171, `append-live_review.txt`'s bytes |
| `.agent/plan.md` | 13/8 | replace with the reviewer's prepared `dry-plan.md`, byte for byte |

### 06026bfc9 F116 R6 C2: sort the job_burn import and drop an unused test import (R-1170)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/job_burn.py` | 1/1 | `ruff check --fix`: the `burn_detector` import sorted |
| `tests/orchestration/test_job_burn.py` | 0/1 | `ruff check --fix`: the unused `BASIS_CLASS_DEFAULT` import dropped |

### efe22ea0c F116 R6 C3: the burn decision test asserts the replaced impact (R-1171)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_job_burn.py` | 4/0 | the in-place-update test also asserts the reused decision's `impact`; byte copy of the prepared file |

### 61b2bc35a F116 R6 C4: the watchdog's burn tripwire calls the burn detector and its own arithmetic is deleted (T003, DECISION F116 D6)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/watchdog.py` | 28/27 | `evaluate_burn_anomaly` becomes a translation to and from the detector; its own mean, minimum and multiple comparison deleted; trip carries `basis` |
| `packages/orchestration/burn_detector.py` | 5/5 | module docstring says the watchdog calls the detector |
| `tests/orchestration/test_watchdog.py` | 19/1 | literal gains the `basis` key; new test for a negative total not being counted |
| `tests/orchestration/test_burn_detector.py` | 5/5 | module docstring, present tense |
| `docs/system/autonomy-watchdog-v1.md` | 13/4 | `basis` among the trip numbers, the detector's trailing basis, the negative-total rule, the deliberate absence reworded |

### F116 R6 C5: handback (self-reference exception — the handoff is committed by this same commit)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

- `git push origin feature/f116-cost-anomaly-alarm` once, after C5: outcome reported in the
  worker's final reply (write-once rule; not known when this file is written).
- No merge, no branch switch, no new branch, no force-push, no pull, no worktree add/remove, no
  pull request opened.

## Verification

0. Before any write: `git rev-parse HEAD` and `origin/feature/f116-cost-anomaly-alarm` both read
   `cf6b6868ac56a30a9c6e0f34a20bdadcbc4b1d73`; `git status --porcelain` empty; `.agent/STOP`
   absent; `block.md` sha256 `24d0e5c6fccd2e5e77055f5414df871a4048856b4d74ae57b98a31e27e1f42d8`,
   124 lines; all ten prepared-file digests matched.
1. **Gate 1** (`git status --porcelain`, then `.remedy-wt/f116-r6-worker/gates.py 1`): status
   empty; the 13 byte proofs of C1 to C4 over the committed blobs all `True`. PASS.
2. **Gate 2** (`.remedy-wt/f116-r6-worker/gates.py 2`, once, from the primary checkout, after
   C4): the block's pytest command, exit 0, no FAILED, ERROR or SKIPPED line. Last line:
   `1174 passed, 2 deselected in 132.67s (0:02:12)`. PASS.
3. **Gate 3** (`python3 -m ruff check` over the six touched Python files): exit 0,
   `All checks passed!`. PASS.
4. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, six of six checks
   `pass`, `"fail_count": 0`. PASS.
5. **Gate 5** (`scripts.rotate_live_review.open_finding_ids`): exit 0,
   `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162',
   'R-1170', 'R-1171']` — exact match. PASS.
6. **Gate 6** (after the push): reported in the worker's final reply (not known when this file is
   written).

## Authored-text proofs

- `block.md` → `.agent/authored/f116-r6.md`: 124 lines, byte-equal (`True`), sha256
  `24d0e5c6fccd2e5e77055f5414df871a4048856b4d74ae57b98a31e27e1f42d8`.
- `append-live_review.txt` and `append-decisions.txt` appended verbatim to their base blobs:
  proofs `True` before C1 and again over the committed blobs.
- `dry-plan.md` → `.agent/plan.md`: byte-equal, `True`.
- The five C4 paths, `job_burn.py` (C2) and `test_job_burn.py` (C3) equal their `dry/` copies:
  `True` each, before the commit and again over the committed blobs.

## Findings

R-1168 and R-1169 are resolved by C1. R-1170 and R-1171 are registered by C1 and repaired by C2
and C3; their resolutions are the reviewer's to write. No new finding.

## For the operator, in plain sentences

The mission watchdog, which pauses a long unattended mission when something looks wrong, no longer
does its own sums to decide whether the mission is spending tokens too fast. It now asks the same
burn detector that guards single jobs, so both give the same answer for the same numbers. Each
warning now says which kind of comparison it used. A ledger entry with a negative token count,
which no provider reports, is now ignored instead of counted. One test now checks the sentence that
tells a person how to continue a paused job.

## Deviations & assumptions

None. Every commit is the block's, in the block's order, with the block's subjects; every file is a
byte copy of its prepared file or, for C2, the output of the ordered `ruff check --fix`, which then
equalled the prepared `job_burn.py`. Gate 2 ran once; no mutation, no full suite, no `-n`, no
`REMEDY_TEST_MAX_WORKERS`, no `cd`, nothing written under `/tmp`. No commit was near the cap
(C1 157 insertions, C4 70). No `Landed:` or `Done:` line was written.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then rule 2, the Open PR Gate.
3. Then confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Then book round 6's verdict and resolve R-1170 and R-1171 in the next round's first commit.
5. Then T003's second half: the job's report names a recorded trip, and the documentation of the
   whole alarm.

Operator questions open: 0.
Open findings: 11 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1170 and R-1171, Low; R-1170 and R-1171 owned by F116 and repaired, awaiting the reviewer; the
rest owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 5, resolve R-1168 and R-1169, register R-1170 and R-1171, DECISION F116 D6, the plan | done | `a10a877a6` |
| C2: sort the job_burn import and drop an unused test import (R-1170) | done | `06026bfc9` |
| C3: the burn decision test asserts the replaced impact (R-1171) | done | `efe22ea0c` |
| C4: the watchdog's burn tripwire calls the burn detector (T003, DECISION F116 D6) | done | `61b2bc35a` |
| Gates 1 to 5 | done | PASS |
| C5: handback | done | this commit |
| Push | pending | run right after this commit, reported in the worker's final reply |
| Gate 6 | pending | run after the push, reported in the worker's final reply |
