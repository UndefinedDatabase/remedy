# Handback — F312 round 7 (the closing round)

## Session

SESSION 1 of feature F312 · round 7 · rounds so far 7

Context self-assessment: this session verified all eleven prepared-file digests with a Python
sha256 reader before using any of them, executed C1 and C3 exactly as the block ordered with no
deviation, and gates 1 to 4 passed on their first run.

Fortschritt: 100 % (F312 is accepted; its pull request waits for the next session's Open PR Gate) —
Schätzung

## Range

Review of `c5e30c07f`..HEAD (C1 below, then this commit, C3, which also carries this handback).

## Commits

### 8c9dc7b49 F312 R7 C1: book round 6, register and resolve R-1382, resolve R-1369, DECISION F312 D5, the plan, the block and the PR body
200 insertions, 19 deletions.
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f312-r7.md` | +101 (new file) | byte copy of `block.md` |
| `.agent/authored/f312-r7-pr_body.md` | +62 (new file) | byte copy of `src-pr_body.md` |
| `.agent/live_review.md` | +8 | byte copy over the prepared re-head, R-1382 register/resolve and R-1369 resolve |
| `.agent/decisions.md` | +10 | byte copy appending DECISION F312 D5 |
| `.agent/plan.md` | +7/-7 | byte copy of the prepared round-7 plan |

### this commit (C3) F312 R7 C3: accept F312 in STATUS with its README sync and the self-use queue
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1/-1 | byte copy flipping F312 to accepted |
| `README.md` | +10/-3 | byte copy syncing counts and the Tier 2 list |
| `scripts/self_use_queue.json` | +1/-1 | byte copy marking SU-066 `consumed_by` F312 |
| `.agent/handoff.md` | rewritten | this file (a handoff cannot table its own commit) |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` before C1: `[]`, no open
PR — the Open PR Gate passes trivially. No other `gh` command before this commit. No worktree
add/remove of my own. The push and the pull request are both ordered to run after this commit, so
their outcomes are reported in the final reply only.

## Verification

Gates run once each, after C3's three copies and before this commit.

1. `git status --porcelain` → ` M README.md`, ` M docs/roadmap/STATUS.md`,
   ` M scripts/self_use_queue.json` (exactly the three ordered paths). Then
   `python3 .remedy-wt/f312-r7/prep/verify.py . --worktree`:
   ```
   True	8c9dc7b49 single parent equal to the commit before it
   True	every commit carries an F312 R7 C1 or C3 subject: 1 of 1
   True	C1 paths exactly [...]: [same]
   True	C1 .agent/authored/f312-r7.md equals block.md
   True	C1 .agent/authored/f312-r7-pr_body.md equals src-pr_body.md
   True	C1 .agent/live_review.md equals dry-live_review.md
   True	C1 .agent/decisions.md equals dry-decisions.md
   True	C1 .agent/plan.md equals dry-plan.md
   absent	C3
   True	worktree docs/roadmap/STATUS.md equals dry-STATUS.md
   True	worktree README.md equals dry-README.md
   True	worktree scripts/self_use_queue.json equals dry-self_use_queue.json
   ALL True
   ```
2. `git diff --numstat -- docs/roadmap/STATUS.md README.md scripts/self_use_queue.json`:
   ```
   10	3	README.md
   1	1	docs/roadmap/STATUS.md
   1	1	scripts/self_use_queue.json
   ```
3. `python3 .remedy-wt/f312-r7/prep/run_selection.py . .remedy-wt/f312-r7-worker/selection-output.txt`:
   ```
   paths 75
   exit 0
   3449 passed, 2 skipped in 19.83s
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   ```
   No `FAILED` or `ERROR` line, no `process(es) behind` line.
4. `python3 -m apps.cli.main integrity check --json` → exit 1, `fail_count` 1:
   ```
   {"check_count": 6, "checks": [..., {"message": "12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362", "name": "high_blockers_open", "status": "fail"}], "error": "integrity_failed", "fail_count": 1, "message": "integrity gate failed with 1 failing check(s)", "ok": false, "passed": false, "schema_version": 1, "version": 1}
   ```
   The one failing check is `high_blockers_open`, naming the twelve ids of DECISION F310 D7's
   thirteen less R-1369 (which this round's C1 resolved). Then
   `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
   → `87` (round 6's base of 88, less the two this round's C1 resolved — R-1369 and R-1382 — plus
   the one R-1382 registered in the same commit: 88 − 2 + 1 = 87).

## Authored-text proofs

C1's five byte copies (`.agent/authored/f312-r7.md` ← `block.md`;
`.agent/authored/f312-r7-pr_body.md` ← `src-pr_body.md`; `.agent/live_review.md` ←
`dry-live_review.md`; `.agent/decisions.md` ← `dry-decisions.md`; `.agent/plan.md` ← `dry-plan.md`)
and C3's three byte copies (`docs/roadmap/STATUS.md` ← `dry-STATUS.md`; `README.md` ←
`dry-README.md`; `scripts/self_use_queue.json` ← `dry-self_use_queue.json`) were each proved equal
by a Python bytes-equality script before their commit
(`.remedy-wt/f312-r7-worker/c1_apply.py` and `c3_apply.py`, both `ALL True`), and `verify.py`'s
lines above confirm the C1 half again. All eleven prepared-file digests named in the block
(`block.md`, `verify.py`, `run_selection.py`, `selection.txt`, `dry-live_review.md`,
`dry-decisions.md`, `dry-plan.md`, `src-pr_body.md`, `dry-STATUS.md`, `dry-README.md`,
`dry-self_use_queue.json`) matched before any file was used.

## Deviations & assumptions

None. C1 and C3 landed exactly as the block ordered, on the first attempt, with no amendment. C2
was not run and no commit was numbered C2, as the block orders under DECISION F312 D5. Gates 1 to
4 each passed on their first run, so no gate needed a re-run.

## For the operator, in plain sentences

An order that names no file, such as asking for a nicer design, now gets a plan made of the files
the planner itself picks, instead of failing before any work starts. A plan the planner wrote for
one part of an order no longer limits a job to only the files the person named. When the planner's
plan for such an order is refused twice, Remedy now asks which files are meant, and the answer
becomes the job's work. The whole test collection ran on the code that ships and passed. The
review package built for this feature is named
`remedy-review-20261021-011120-READY_FOR_REVIEW.zip`, in the folder `~/Repos/remedy-history/zips`.
A pull request is now open for this feature and will be merged at the start of the next session
unless the operator merges it earlier. One question still waits for the operator, and it is
already answered with this session's recommendation.

## Next

In order: Phase 1 rule 1 (`.agent/STOP`) — absent, no action needed; the Open PR Gate, which merges
F312's pull request in the NEXT session and never in this one; Rule A5, which proposes F311.
Operator questions open: 1. Open findings: 87 (gate 4, `open_finding_ids` of
`scripts/rotate_live_review.py` over `.agent/live_review.md`, measured at `8c9dc7b49` before C3).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `8c9dc7b49` |
| C2 | skipped | no rotation this closure, DECISION F312 D5 |
| C3 | done | this commit |
| Gate 1 | done | `ALL True` |
| Gate 2 | done | numstat recorded above |
| Gate 3 | done | exit 0, `3449 passed, 2 skipped in 19.83s` |
| Gate 4 | done | `fail_count` 1 on the standing twelve; 87 open findings |
| Gate 5 | pending | reported in the final reply only |
| Push | pending | reported in the final reply only |
| Pull request | pending | reported in the final reply only |
