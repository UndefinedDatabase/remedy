# Handback — F313 round 3

## Session

SESSION 1 of feature F313 · round 3 · rounds so far 3

Context self-assessment: this session verified every prepared file's digest before use and applied
each one as a byte copy proved equal; all five gates passed on their first run, with no stop
condition met.

Fortschritt: ~70 % (T001 to T003 landed · the closure open) — Schätzung

## Range

Review of `046ec1ec1`..HEAD (C1, C2, then this commit C3, which carries this handback).

## Commits

### 94ed12faa F313 R3 C1: book round 2, resolve R-1390, DECISION F313 D2 addendum, the plan
134 insertions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f313-r3.md` | +112 (new file) | byte copy of `block.md` |
| `.agent/live_review.md` | +4 | byte copy, round 2's verdict and R-1390's resolution |
| `.agent/prose_slips.md` | +1 | byte copy, the one line for the matrix indentation |
| `.agent/decisions.md` | +11 | byte copy, DECISION F313 D2's addendum |
| `.agent/plan.md` | +6/-7 | byte copy of the prepared plan |

### 4616cdb6c F313 R3 C2: the recorded answers for the universe's kit and the command that records them
372 insertions.

| Path | +/- | Reason |
|---|---|---|
| `scripts/record_client_answers.py` | +241 (new file) | the recorder and its `--check` |
| `tests/orchestration/test_record_client_answers.py` | +101 (new file) | the test that runs the recorder's check |
| `docs/system/client-answers-v1/*.json` (5 files) | +1 each (new files) | the five recorded answers, applied as bytes |
| `docs/system/public-http-api-v1.md` | +19 | section "Recorded answers" before "Staying current" |
| `docs/README.md` | +2 | two rows for the folder |
| `docs/system/api-release-matrix-v1.json` | +1/-1 | the `blockers` line re-indented from three spaces to four, nothing else |
| `tests/test_no_orphan_modules.py` | +3 | one `ALLOWED_UNWIRED` entry naming the script |

### This commit F313 R3 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback (a handback cannot table the commit that writes it) |

## External actions

`git branch --show-current` read `feature/f313-contract-1-22` before every commit; no pull. Push
after this commit: `git push origin feature/f313-contract-1-22` (outcome in the final reply). No
pull request opened, nothing merged.

## Verification

1. `git status --porcelain` empty; `python3 .remedy-wt/f313-r3/prep/verify.py .` → every line
   `True`, `absent C3`, last line `ALL True` (C1 insertions 134, C2 372).
2. `python3 -m ruff check scripts/record_client_answers.py tests/orchestration/test_record_client_answers.py tests/test_no_orphan_modules.py`
   → `All checks passed!`
3. `python3 .remedy-wt/f313-r3/prep/run_selection.py . .remedy-wt/f313-r3-worker/selection-output.txt`
   → `paths 80`, `exit 0`, `3689 passed, 2 skipped in 33.22s`, no FAILED, ERROR or
   `process(es) behind` line. SKIPPED lines:
   ```
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   ```
4. `python3 -m apps.cli.main integrity check --json` → exit 1, `fail_count` 1, the one failing
   check `high_blockers_open` naming exactly the twelve ids of DECISION F310 D7 (`R-1335, R-1336,
   R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362`) and no other.
5. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` → `87`.

## Authored-text proofs

All five prepared files named in the prompt matched their sha256 digests before use, and every
file `digests.txt` lists matched at copy time. `block.md` (112 lines, sha256 `65c31dd7…ba24`,
equal to the prompt's) was committed as `.agent/authored/f313-r3.md`. Each of C1's five and C2's
eleven byte copies was proved equal by a Python reader at copy time, and `verify.py` re-proved
every pair against the committed bytes. The recorder was not run; the five answers are applied as
bytes.

## Deviations & assumptions

One slip of mine: my first command, the digest check, began with a `cd` into the repository root
(the block forbids any `cd`); nothing was written by it and every later command used absolute
paths or `git -C`. Two compound shell commands were refused by the sandbox before they ran and
were split into separate calls; no gate ran more than once and no result was read from a refused
call. The commits landed in the ordered sequence and no file outside the paths named per commit
was touched. The C2 diff read as the block's reviewer reading. The worker's scripts live under
`.remedy-wt/f313-r3-worker/` (gitignored scratch).

## For the operator, in plain sentences

The documentation now carries answers recorded from the real commands that show what is running
and what one job is doing, for a client such as the universe's kit to test against without a
running system. A small command records them again and a test checks that the recorded files still
match, so they cannot drift unnoticed. The page for the programs' interface has a new section that
says where they are and how to refresh them. The earlier review round's verdict is booked and its
one defect is closed. The relevant tests ran on the code as it stands and passed. What remains is
the closure of this feature.

## Next

Phase 1 rule 1 (`.agent/STOP`), then rule 2 (Open PR Gate), then book round 3's verdict in the
next round's first commit, then the closure's integration-gate round. Operator questions open: 1.
Open findings: 87 (gate 5, rule `open_finding_ids`, commit `4616cdb6c`).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | base `046ec1ec1`, clean tree |
| C1 | done | `94ed12faa` |
| C2 | done | `4616cdb6c` |
| C3 | done | this commit |
| Gate 1 | done | `ALL True` |
| Gate 2 | done | `All checks passed!` |
| Gate 3 | done | exit 0, 3689 passed, 2 skipped |
| Gate 4 | done | `fail_count` 1 on the standing twelve |
| Gate 5 | done | 87 |
