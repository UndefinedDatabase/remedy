# Handoff — F116 session 3, round 7: book round 6, resolve R-1170 and R-1171, register R-1172;
# T003 second half, first part — `remedy job show` and the report section show a recorded burn alarm
# (DECISION F116 D7)

## Session

SESSION 3 of feature F116 · round 7 · rounds so far 7

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~80 % (T001 built · T002 built · T003 mostly built · its run-log event and the alarm's page, hardening and closure open) — Schätzung

## Range

Review of `f807fe53ccff3217b41921cbf1a35da916e6e732`..HEAD (HEAD is this commit, C4 below).

## Commits

### a1fad5ad9 F116 R7 C1: book round 6, resolve R-1170 and R-1171, register R-1172, DECISION F116 D7, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f116-r7.md` | 115/0 (new) | byte copy of the reviewer's prepared `block.md` |
| `.agent/decisions.md` | 10/0 | append DECISION F116 D7, `append-decisions.txt`'s bytes |
| `.agent/live_review.md` | 8/0 | append the F116 round 6 gate entry, R-1170 and R-1171 resolutions, R-1172, `append-live_review.txt`'s bytes |
| `.agent/plan.md` | 8/8 | replace with the reviewer's prepared `dry-plan.md`, byte for byte |

### bb6539a35 F116 R7 C2: one tolerant reader turns a recorded burn alarm into its sentence (T003, DECISION F116 D7)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/job_burn.py` | 17/0 | `recorded_burn_sentence` and the deliberate-absence paragraph on the parallel-width throttle; byte copy of the prepared file |
| `tests/orchestration/test_job_burn.py` | 25/0 | two tests of the reader; byte copy of the prepared file |

### d738ff550 F116 R7 C3: remedy job show and the report section name a recorded burn alarm (T003, DECISION F116 D7)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/job.py` | 18/0 | `_print_burn_alarm` on stderr after the findings block; `burn_alarm` key and progress line in `_report_section` |
| `tests/cli/test_job_show.py` | 32/0 | tests of the Burn alarm block; byte copy of the prepared file |
| `tests/cli/test_job_report.py` | 30/2 | `PROGRESS_KEYS` gains `burn_alarm`; tests of the report line; byte copy of the prepared file |

### F116 R7 C4: handback (self-reference exception — the handoff is committed by this same commit)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

- `git push origin feature/f116-cost-anomaly-alarm` once, after C4: outcome reported in the
  worker's final reply (write-once rule; not known when this file is written).
- No merge, no branch switch, no new branch, no force-push, no pull, no worktree add/remove, no
  pull request opened.

## Verification

0. Before any write: `git rev-parse HEAD` and `origin/feature/f116-cost-anomaly-alarm` both read
   `f807fe53ccff3217b41921cbf1a35da916e6e732`; `git status --porcelain` empty; `.agent/STOP`
   absent; `block.md` sha256 `444e60aa7b547473856dac1403697afbde7d88f2d7131487a1cc7a7b66f933b9`,
   115 lines; all eight prepared-file digests matched.
1. **Gate 1** (`git status --porcelain`, then `.remedy-wt/f116-r7-worker/proof.py HEAD`): status
   empty; the nine byte proofs of C1 to C3 over the committed blobs all `True`. PASS.
2. **Gate 2** (`.remedy-wt/f116-r7-worker/gates.py 2`, once, from the primary checkout, after
   C3): the block's pytest command, exit 0, no FAILED, ERROR or SKIPPED line. Last line:
   `1454 passed, 2 deselected in 226.11s (0:03:46)`. PASS.
3. **Gate 3** (`python3 -m ruff check` over the five touched Python files): exit 0,
   `All checks passed!`. PASS.
4. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, six of six checks
   `pass`, `"fail_count": 0`. PASS.
5. **Gate 5** (`scripts.rotate_live_review.open_finding_ids`): exit 0,
   `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162',
   'R-1172']` — exact match. PASS.
6. **Gate 6** (after the push): reported in the worker's final reply (not known when this file is
   written).

## Authored-text proofs

- `block.md` → `.agent/authored/f116-r7.md`: 115 lines, byte-equal (`True`), sha256
  `444e60aa7b547473856dac1403697afbde7d88f2d7131487a1cc7a7b66f933b9`.
- `append-live_review.txt` and `append-decisions.txt` appended verbatim to their base blobs:
  proofs `True` before C1 and again over the committed blobs.
- `dry-plan.md` → `.agent/plan.md`: byte-equal, `True`.
- The five C2 and C3 paths equal their `dry/` copies: `True` each, over the committed blobs.

## Findings

R-1170 and R-1171 are resolved by C1. R-1172 is registered by C1: a test-order defect in two
unrelated test files, owned by F297, the next findings paydown, and not repaired in this feature.

## For the operator, in plain sentences

When a job's recent calls suddenly cost far more than its earlier ones, `remedy job show` now
prints a short block called "Burn alarm". It holds one sentence saying how much the calls spent and
what was expected, and it names `remedy job budget` as the place with the full numbers. The report
part of `remedy job show --full` carries the same sentence. A damaged job file never makes either
command fail; it only hides the sentence. Nothing slows a job's parallel work on an alarm, because a
job does one thing at a time. A test-order problem in two unrelated test files was found and
recorded for the next clean-up feature.

## Deviations & assumptions

One slip: a single no-op `cd` into the worker scratch folder (an empty heredoc) was issued once by
mistake; it changed nothing, the shell's working directory is reset between calls, and every other
command used absolute paths. Otherwise none: every commit is the block's, in the block's order, with
the block's subjects; every file is a byte copy of its prepared file. Gate 2 ran once; no mutation,
no full suite, no `-n`, no `REMEDY_TEST_MAX_WORKERS`, nothing written under `/tmp`. No commit was
near the cap (C1 133 insertions). No `Landed:` or `Done:` line was written.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then rule 2, the Open PR Gate.
3. Then confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Then book round 7's verdict in the next round's first commit.
5. Then the rest of T003's second half: one run-log event when a new trip is recorded, and the page
   that documents the whole alarm.

Operator questions open: 0.
Open findings: 10 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162
and R-1172, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 6, resolve R-1170 and R-1171, register R-1172, DECISION F116 D7, the plan | done | `a1fad5ad9` |
| C2: one tolerant reader turns a recorded burn alarm into its sentence | done | `bb6539a35` |
| C3: remedy job show and the report section name a recorded burn alarm | done | `d738ff550` |
| Gates 1 to 5 | done | PASS |
| C4: handback | done | this commit |
| Push | pending | run right after this commit, reported in the worker's final reply |
| Gate 6 | pending | run after the push, reported in the worker's final reply |
