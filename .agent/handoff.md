# Handback — F311 round 7 (closing round)

## Session

SESSION 1 of feature F311 · round 7 · rounds so far 7

Context self-assessment: this session verified every prepared file's digest before using it,
executed C1 and C3 exactly as the block ordered with C2 correctly skipped per DECISION F311 D7,
and all four gates passed on their first run, with no stop condition met.

Fortschritt: 100 % (F311 is accepted; its pull request waits for the next session's Open PR Gate)
— Schätzung

## Range

Review of `c2e1db984`..HEAD (C1, then this commit, C3, which also carries this handback).

## Commits

### 2f1a5a170 F311 R7 C1: book round 6, DECISION F311 D7, the plan, the block and the PR body
175 insertions, 6 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f311-r7.md` | +92 (new file) | byte copy of `block.md` |
| `.agent/authored/f311-r7-pr_body.md` | +64 (new file) | byte copy of `src-pr_body.md` |
| `.agent/live_review.md` | +2 | byte copy appending `src-ledger.md` (round 6's PASS verdict) |
| `.agent/decisions.md` | +10 | byte copy appending `src-decisions.md` (DECISION F311 D7) |
| `.agent/plan.md` | +7/-6 | byte copy of `dry-plan.md` |

### This commit F311 R7 C3: accept F311 in STATUS with its README sync and the self-use queue

| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1/-1 | byte copy of `dry-STATUS.md`, flips F311 to accepted |
| `README.md` | +11/-2 | byte copy of `dry-README.md`, counts and Tier 12 list synced |
| `scripts/self_use_queue.json` | +1/-1 | byte copy of `dry-self_use_queue.json`, SU-067 `consumed_by` F311 |
| `.agent/handoff.md` | rewritten | this handback (a handback cannot table the commit that writes it) |

## External actions

`git branch --show-current` read `feature/f311-insight` before every commit. Push after this
commit: `git push origin feature/f311-insight` (outcome reported in the final reply only, as
ordered). `gh pr create --base main --head feature/f311-insight --title "F311: the insight, what
runs now, what the worker does, why it hangs" --body-file .agent/authored/f311-r7-pr_body.md`
(outcome reported in the final reply only). Never merged.

## Verification

Gates run once each, before this commit (gates 1-4), gate 5 after the pull request.

1. `git status --porcelain` → exactly ` M README.md`, ` M docs/roadmap/STATUS.md`,
   ` M scripts/self_use_queue.json`. Then `python3 .remedy-wt/f311-r7/prep/verify.py . --worktree`:
   every line `True`, `absent	C3`, last line `ALL True`.
2. `git diff --numstat -- docs/roadmap/STATUS.md README.md scripts/self_use_queue.json`:
   ```
   11	2	README.md
   1	1	docs/roadmap/STATUS.md
   1	1	scripts/self_use_queue.json
   ```
3. `python3 .remedy-wt/f311-r7/prep/run_selection.py . .remedy-wt/f311-r7-worker/selection-output.txt`:
   `paths 75`, `exit 0`, `3449 passed, 2 skipped in 19.71s`, no FAILED or ERROR line, no
   `process(es) behind` line. SKIPPED lines:
   ```
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   ```
4. `python3 -m apps.cli.main integrity check --json` → exit 1, `fail_count` 1, the one failing
   check `high_blockers_open` naming exactly the twelve ids of DECISION F310 D7 (`R-1335, R-1336,
   R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362`) and no other.
   `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` → `87`.
5. Pending: reported in the final reply, after the push and the pull request.

## Authored-text proofs

All five prepared files used this round (`block.md`, `verify.py`, `run_selection.py`,
`selection.txt`, `digests.txt`) matched their stated sha256 digests before use; the seven files
`digests.txt` itself lists (`dry-STATUS.md`, `dry-README.md`, `dry-self_use_queue.json`,
`dry-live_review.md`, `dry-decisions.md`, `dry-plan.md`, `src-pr_body.md`) likewise matched
before use. C1's five byte copies/appends and C3's three byte copies were each proved equal by a
Python reader before commit, and `verify.py`'s own checks confirm the same equality again: "C1
the block copy", "C1 the pr_body copy", "C1 live_review equals dry-live_review", "C1 decisions
equals dry-decisions", "C1 the plan copy" all read `True`; the worktree checks for
`docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json` against their dry files
also read `True`.

## Deviations & assumptions

None. C1 and C3 landed exactly as the block ordered, in the order ordered; C2 was correctly
skipped per DECISION F311 D7 (no rotation commit, appended by C1). No gate ran more than once. No
production or test file was touched; no file outside the paths named per commit was touched.

## For the operator, in plain sentences

A program such as the Orb can now ask Remedy what runs right now and look into one job's worker,
its stage, its task, how long it has been silent, whether it is stuck and why, and what the
operator can do about it. The worker for the lab's local model now keeps its last lines and the
time of its last output, so the answer survives a restart. A value Remedy cannot know shows as
empty instead of a guess. The whole test collection ran on the code that ships and passed. The
review package is `remedy-review-20261021-041253-READY_FOR_REVIEW.zip`, in
`~/Repos/remedy-history/zips`. A pull request is open and will be merged at the start of the next
session unless the operator merges it earlier. One question waits for the operator, already
answered with the session's recommendation.

## Next

Phase 1 rule 1 (`.agent/STOP`) — absent, no action needed; the Open PR Gate, which merges F311's
pull request in the NEXT session and never in this one; Rule A5, which proposes F313. Operator
questions open: 1. Open findings: 87 (gate 4, rule `open_finding_ids`, commit `2f1a5a170`).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `2f1a5a170` |
| C2 | skipped | no rotation commit: DECISION F311 D7, appended by C1 |
| C3 | done | this commit |
| Gate 1 | done | every line `True`, `absent C3`, last `ALL True` |
| Gate 2 | done | numstat reported above |
| Gate 3 | done | exit 0, 3449 passed, 2 skipped, no FAILED/ERROR/behind |
| Gate 4 | done | `fail_count` 1 on the standing twelve; open findings 87 |
| Gate 5 | pending | reported in the final reply only |
| Push | pending | reported in the final reply only |
| Pull request | pending | reported in the final reply only |
