# Handback — F313 round 1

## Session

SESSION 1 of feature F313 · round 1 · rounds so far 1

Context self-assessment: this session verified every prepared file's digest before use and applied
each one as a byte copy proved equal; all five gates passed on their first run, with no stop
condition met.

Fortschritt: ~30 % (claim and contract 1.22 landed · the pages' hand-written parts and the recorded answers open) — Schätzung

## Range

Review of `25ab7c98b`..HEAD (C1, C2, then this commit C3, which carries this handback).

## Commits

### df8d4fe49 F313 R1 C1: claim F313, re-head the ledger, DECISIONs F313 D1 and D2
165 insertions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f313-r1.md` | +108 (new file) | byte copy of `block.md` |
| `docs/roadmap/STATUS.md` | +1/-1 | byte copy of `dry-docs__roadmap__STATUS.md`, F313 claimed |
| `.agent/live_review.md` | +17/-19 | byte copy of the prepared re-head |
| `.agent/decisions.md` | +20 | byte copy, DECISIONs F313 D1 and D2 |
| `.agent/plan.md` | +13/-10 | byte copy of the prepared plan |
| `.agent/context.md` | +6/-8 | byte copy of the prepared context |

### f02abc501 F313 R1 C2: contract 1.22, its release matrix entry and the insight words in the matrix
122 insertions.

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/public_api.py` | +4/-2 | version 1.22 and one more clause of history |
| `apps/cli/client_interface.py` | +3/-2 | version 1.22 and one more clause of history |
| `docs/system/api-release-matrix-v1.json` | +97/-4 | current, rule, two routes moved to 1.22, five insight categories, the 1.22 entry |
| `docs/system/public-http-api-v1.md` | +1/-1 | generated version line |
| `docs/system/machine-client-contract-v1.md` | +1/-1 | generated version line |
| `docs/README.md` | +2/-2 | the index's two lines naming 1.22 |
| `tests/ui_server/test_public_api.py` | +8/-8 | eight pins 1.21 to 1.22 |
| `tests/cli/test_client_interface.py` | +1/-1 | one pin 1.21 to 1.22 |
| `tests/orchestration/test_api_release_matrix.py` | +5/-1 | matrix test reads `insight_words()` |

### This commit F313 R1 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback (a handback cannot table the commit that writes it) |

## External actions

`git checkout -b feature/f313-contract-1-22` from `main` at `25ab7c98b`; `git branch
--show-current` read `feature/f313-contract-1-22` before every commit. Push after this commit:
`git push -u origin feature/f313-contract-1-22` (outcome in the final reply). No pull request
opened, nothing merged.

## Verification

1. `git status --porcelain` empty; `python3 .remedy-wt/f313-r1/prep/verify.py .` → every line
   `True`, `absent C3`, last line `ALL True` (C1 insertions 165, C2 insertions 122).
2. `python3 -m ruff check` over the five named files → `All checks passed!`
3. `python3 .remedy-wt/f313-r1/prep/run_selection.py . .remedy-wt/f313-r1-worker/selection-output.txt`
   → `paths 81`, `exit 0`, `3810 passed, 2 skipped in 31.69s`, no FAILED, ERROR or
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

All five prepared files named in the prompt and the fourteen files `digests.txt` lists matched
their sha256 digests before use. Each of C1's six and C2's nine byte copies was proved equal by a
Python reader at copy time, and `verify.py` re-proved every pair against the committed bytes.

## Deviations & assumptions

None. The commits landed in the ordered sequence, no gate ran more than once, and no file outside
the paths named per commit was touched. The worker's copy script lives under
`.remedy-wt/f313-r1-worker/` (gitignored scratch).

## For the operator, in plain sentences

Remedy's public interface now carries version 1.22. It adds the two new reads that let a program
ask what runs right now and look into one job, and the release table lists those and the words
they use. The feature is claimed in the roadmap ledger, and the decisions that shape it are
recorded. The pages' hand-written parts and the recorded answers are still to be written in the
next round. The relevant tests ran on the code as it stands and passed.

## Next

Phase 1 rule 1 (`.agent/STOP`), then rule 2 (Open PR Gate), then book round 1's verdict in the
next round's first commit, then T002, the hand-written parts of the two pages. Operator questions
open: 1. Open findings: 87 (gate 5, rule `open_finding_ids`, commit `f02abc501`).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | branch from `25ab7c98b` |
| C1 | done | `df8d4fe49` |
| C2 | done | `f02abc501` |
| C3 | done | this commit |
| Gate 1 | done | `ALL True` |
| Gate 2 | done | `All checks passed!` |
| Gate 3 | done | exit 0, 3810 passed, 2 skipped |
| Gate 4 | done | `fail_count` 1 on the standing twelve |
| Gate 5 | done | 87 |
