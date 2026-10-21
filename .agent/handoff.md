# Handback — F313 round 2

## Session

SESSION 1 of feature F313 · round 2 · rounds so far 2

Context self-assessment: this session verified every prepared file's digest before use and applied
each one as a byte copy proved equal; all five gates passed on their first run, with no stop
condition met.

Fortschritt: ~55 % (contract 1.22, its pages and R-1390 landed · the recorded answers open) — Schätzung

## Range

Review of `dd419b84e`..HEAD (C1, C2, C3, then this commit C4, which carries this handback).

## Commits

### ff41ad35d F313 R2 C1: book round 1, register R-1390, DECISION F313 D1 addendum, the plan
139 insertions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f313-r2.md` | +119 (new file) | byte copy of `block.md` |
| `.agent/live_review.md` | +4 | byte copy, round 1's verdict and the registered finding |
| `.agent/decisions.md` | +10 | byte copy, DECISION F313 D1's addendum |
| `.agent/plan.md` | +6/-7 | byte copy of the prepared plan |

### 008836c95 F313 R2 C2: the digest's decisions carry a budget stop's blockers (R-1390)
30 insertions.

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/client_digest.py` | +3 | `_decision_entry` reads `blockers` from a `token_budget` decision's payload, an empty list for any other |
| `apps/cli/client_interface_digest.py` | +1 | `DIGEST_KEY_TREE` names `blockers` after `clarifications` |
| `tests/orchestration/test_client_digest.py` | +2 | the two whole-entry assertions gain `"blockers": []` |
| `tests/orchestration/test_lab_stop_20261020.py` | +19 | one new test reads the lab stop's entry and the remainder decision's entry |
| `docs/system/api-release-matrix-v1.json` | +2/-1 | the 1.22 `added` gains one line |
| `docs/system/machine-client-contract-v1.md` | +3/-3 | the generated section names `blockers` under `decisions` (three places) |

### aa77653b7 F313 R2 C3: the two pages describe contract 1.22
117 insertions.

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/public_api_routes.py` | +5/-4 | the decision route's sentence on `extend`, and "since 1.22" for the two new routes |
| `docs/system/public-http-api-v1.md` | +86/-3 | sections "Budget stops" and "What runs now, and why a job hangs", the "Budget profiles (since 1.22)" paragraph, the generated route table |
| `docs/system/machine-client-contract-v1.md` | +26/-8 | step 3, the `--answer` and `closed_decisions` rows, the `token_budget` row, section "Watching what runs" |

### This commit F313 R2 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback (a handback cannot table the commit that writes it) |

## External actions

`git branch --show-current` read `feature/f313-contract-1-22` before every commit; no pull. Push
after this commit: `git push origin feature/f313-contract-1-22` (outcome in the final reply). No
pull request opened, nothing merged.

## Verification

1. `git status --porcelain` empty; `python3 .remedy-wt/f313-r2/prep/verify.py .` → every line
   `True`, `absent C4`, last line `ALL True` (C1 insertions 139, C2 30, C3 117).
2. `python3 -m ruff check` over the five named files → `All checks passed!`
3. `python3 .remedy-wt/f313-r2/prep/run_selection.py . .remedy-wt/f313-r2-worker/selection-output.txt`
   → `paths 84`, `exit 0`, `3892 passed, 2 skipped in 31.32s`, no FAILED, ERROR or
   `process(es) behind` line. SKIPPED lines:
   ```
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   ```
4. `python3 -m apps.cli.main integrity check --json` → exit 1, `fail_count` 1, the one failing
   check `high_blockers_open` naming exactly the twelve ids of DECISION F310 D7 (`R-1335, R-1336,
   R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362`) and no other.
5. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` → `88`.

## Authored-text proofs

All five prepared files named in the prompt and the thirteen files `digests.txt` lists matched
their sha256 digests before use (`block.md` 119 lines, sha256 `587135c7…1b38`, equal to the
prompt's). Each of C1's four, C2's six and C3's three byte copies was proved equal by a Python
reader at copy time, and `verify.py` re-proved every pair against the committed bytes.

## Deviations & assumptions

None. The commits landed in the ordered sequence, no gate ran more than once, and no file outside
the paths named per commit was touched. Every one of C2's and C3's diffs read as the block's
reviewer reading. One observation, not a deviation: the new line in the release matrix's 1.22
`added` list is indented by three spaces where its neighbours use four; the prepared bytes were
committed unchanged. One slip of mine: a first ruff attempt ran in the worker scratch directory
(a `cd` I should not have used) and failed with E902 on every path; the gate was then run once
from the repository root and passed, so no gate result was read from the failed attempt. The
worker's copy script lives under `.remedy-wt/f313-r2-worker/` (gitignored scratch).

## For the operator, in plain sentences

The status view that programs read now tells them, for a job that stopped on its budget, what is
still blocking the mission, so a client can show the one question together with what is left. The
two documentation pages for version 1.22 are written: they explain what a budget stop is and how
it is answered, how to see what runs right now, and why a job can seem to hang. The earlier
review round's verdict is booked and the one defect it found is repaired. The relevant tests ran
on the code as it stands and passed. The recorded answers are still to be written.

## Next

Phase 1 rule 1 (`.agent/STOP`), then rule 2 (Open PR Gate), then book round 2's verdict and
resolve R-1390 in the next round's first commit, then T003, the recorded answers. Operator
questions open: 1. Open findings: 88 (gate 5, rule `open_finding_ids`, commit `aa77653b7`).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | base `dd419b84e`, clean tree |
| C1 | done | `ff41ad35d` |
| C2 | done | `008836c95` |
| C3 | done | `aa77653b7` |
| C4 | done | this commit |
| Gate 1 | done | `ALL True` |
| Gate 2 | done | `All checks passed!` |
| Gate 3 | done | exit 0, 3892 passed, 2 skipped |
| Gate 4 | done | `fail_count` 1 on the standing twelve |
| Gate 5 | done | 88 |
| R-1390 | done | repaired in C2, documented in C3; to be resolved in the next round's first commit |
