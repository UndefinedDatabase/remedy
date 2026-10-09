# Handoff — F301 round 2: book round 1, T002 — the project's upkeep ledger

## Session

SESSION 1 of feature F301 · round 2 · rounds so far 2

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~30 % (claim, T001, the loop's structural step and T002 · T003 to T005 open) — Schätzung

## Range

Review of `5b0cc5879`..HEAD (four commits on `feature/f301-mission-upkeep` — C1, C2, C3, and this
handback, C4).

## Commits

### `7763d1928` F301 R2 C1: save the round 2 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f301-r2.md` | 150/0 | NEW FILE — byte copy of `block.md`; sha256 `4a601be8a5f5f98faff364ec6e2f66dbd9f71791470e030e7c6822c9fc383d70`, 150 lines |

### `789efae86` F301 R2 C2: book round 1, the plan, a prose slip

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/0 | the base blob at `5b0cc5879` followed by `append-live_review.txt`'s bytes: F301 round 1's Gate entry, VERDICT PASS, booked |
| `.agent/plan.md` | 13/13 | replaced with `dry-plan.md`: round 2's current step, T002, the project's upkeep ledger |
| `.agent/prose_slips.md` | 1/0 | the base blob at `5b0cc5879` followed by `append-prose_slips.txt`'s bytes: the round 1 sandbox-discipline slip line |

### `93b6cd1a9` F301 R2 C3: the project's upkeep ledger, written by mission continue (T002, DECISION F301 D1)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/mission_cmd.py` | 4/0 | `_cmd_mission_continue` calls `record_closed_jobs(project_id, mission.id)` after the mission is loaded and before `continue_mission`, with a two-line comment naming DECISION F301 D1; its output is unchanged |
| `packages/orchestration/mission_upkeep.py` | 194/0 | NEW FILE — the project's upkeep ledger: `upkeep_ledger_path`, `append_upkeep_line` (refuses a kind outside `UPKEEP_LINE_KINDS`), `read_upkeep_ledger` (skips a torn line), `finding_key`, `job_open_findings`, `replaced_pairs_from_findings`, `record_closed_jobs`, `open_findings` |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | `packages.orchestration.mission_upkeep` added directly after `packages.orchestration.mission_state` |
| `tests/orchestration/test_mission_upkeep.py` | 276/0 | NEW FILE — the module's test suite, including a subprocess test of `remedy mission continue` through the CLI |

### This commit — F301 R2 C4: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

None yet. The block's one push happens AFTER this commit (the "THEN" step), reported in the
worker's final reply after this commit. No pull request is opened this round.

## Verification

**Gate 1** (after C0, before C1): a Python script (`gate1_digests.py`) checked every line of
`digests.txt` against the file it names in `.remedy-wt/f301-r2/` — 11 of 11 files, sha256 and line
count both `True`. Exit implicit 0 (script printed `ALL_TRUE True`).

**Gate 2** (after C3): `git -C /home/decodeux/Repos/remedy status --porcelain` read empty. The C2
step 2 byte proofs (`gate2_reproofs.py`) re-run at this commit: `.agent/live_review.md` equals the
base blob at `5b0cc5879` plus `append-live_review.txt`'s bytes, `True`; `.agent/prose_slips.md`
equals the base blob at `5b0cc5879` plus `append-prose_slips.txt`'s bytes, `True`; and the three C2
copied files each equal their prepared file, `True` — 5 of 5 `True`. The C3 step 3 byte proofs
re-run at this commit: all four C3 copied files equal their prepared file, 4 of 4 `True`.

**Gate 3** (the round's one test selection, run once):
```
python3 -m pytest -q -rfEs @/home/decodeux/Repos/remedy/.remedy-wt/f301-r2/selection.txt
```
Exit code 0 (captured directly by the running script's own `subprocess.run`, printed as
`GATE3_EXIT_CODE 0`). Summary line: `6235 passed, 4 skipped in 339.50s (0:05:39)`. SKIPPED lines,
verbatim:
```
SKIPPED [1] tests/regression/test_f293_acceptance.py:191: main holds F293, so its own changes are history
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
```
No `FAILED` or `ERROR` line anywhere in the output.

**Gate 4**:
```
python3 -m ruff check packages/orchestration/mission_upkeep.py tests/orchestration/test_mission_upkeep.py apps/cli/commands/mission_cmd.py
```
Exit 0. Output: `All checks passed!`

**Gate 5**:
```
python3 -m apps.cli.main integrity check --json
```
Exit 0. `{"check_count": 6, ... "fail_count": 0, "ok": true, "passed": true, ...}` — all six checks
`status: pass` (`handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`repo_root_hygiene`, `high_blockers_open`).
```
python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
Exit 0. Output, verbatim:
```
['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1162', 'R-1172', 'R-1176', 'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230', 'R-1233']
```
Matches the block's ordered list exactly.

**Gate 6** (the push): after this commit, reported in the worker's final reply.

## Authored-text proofs

`.agent/authored/f301-r2.md` (C1) equals `block.md` byte for byte: sha256
`4a601be8a5f5f98faff364ec6e2f66dbd9f71791470e030e7c6822c9fc383d70`, 150 lines, checked at write
time (C1). Gate 2 re-checks only the C2 step 2 and C3 step 3 proofs the block names; C1's proof is
not among them and was not re-run at gate 2.

## Deviations & assumptions

One sandbox-discipline slip, which touched no commit's content, no push, no gate's verdict and no
file outside the round's named paths:
- Before gate 1, C0's four read-only checks (`git branch --show-current`, `git rev-parse HEAD`,
  `git rev-parse origin/feature/f301-mission-upkeep`, `git status --porcelain`, and `ls` for
  `.agent/STOP`) were run as separate commands within a single shell tool call (newline-separated;
  no `&&`, `;`, pipe, `$(...)` or other compound operator was used), rather than each as its own
  tool call as the block's "every git command is a single `git -C` call" discipline intends. Every
  individual result was read correctly: branch `feature/f301-mission-upkeep`, HEAD and origin both
  `5b0cc58793501c0575132caffe2c524a69039b23`, an empty `status --porcelain`, and `.agent/STOP`
  absent (confirmed by the `ls` error). No later command in the round was combined this way; every
  git command, python3 script and proof from gate 1 onward ran as its own single tool call.

Otherwise: None. C0 through C3 ran exactly as the block ordered, each exactly once, in the block's
sequence; every copy, hash, run and proof besides the one slip above was performed by a dedicated
Python script under `.remedy-wt/f301-r2-worker/`, run with an explicit working directory of
`/home/decodeux/Repos/remedy`; no file outside the round's named paths was touched; no
`REMEDY_TEST_MAX_WORKERS` was set and no `-n` was passed; no mutation, no full suite, no worktree
created or removed; `.agent/STOP` did not appear at any point; the branch read
`feature/f301-mission-upkeep` before every commit, checked immediately before each of C1, C2 and
C3.

## Round verdicts

F301 round 1's PASS verdict (the Gate: F301 R1 entry, over `fdbf0802e`..`5b0cc5879`) is booked by
C2 — the `dry-live_review.md` bytes, proved equal to the base blob at `5b0cc5879` plus
`append-live_review.txt`'s bytes, now carry that entry forward in `.agent/live_review.md`. Round
2's verdict is the reviewer's, to be booked in the next round's first commit.

## For the operator, in plain sentences

Remedy now keeps, for each project, a written record of what the jobs of its missions left
unfinished: the problems a reviewer still saw when a job ended, and any file that was replaced by a
new one and not deleted. The record only grows, and a problem leaves it only when a cleanup job
that took it on has finished. When the operator continues a mission, Remedy first writes down what
the jobs that have ended left behind. The next round makes Remedy start the cleanup job itself
after every fifth finished job. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Phase 1 rule 2 (the Open PR Gate).
3. Book round 2's verdict in the next round's first commit.
4. T003: the boundary and one step of `config.py`, then the setting, the cadence and the upkeep job
   through `remedy mission continue`.

Operator questions open: 0.
Open findings: 16 (R-1233, Low, owned by F301; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157,
R-1158, R-1162, R-1172, R-1176, R-1196, R-1219, R-1220, R-1225 and R-1230, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0: base and branch | done | HEAD `5b0cc5879`, equal to origin, clean tree, no STOP, branch `feature/f301-mission-upkeep` |
| C1: save the round 2 block | done | 150 lines, sha256 matches `block.md`; committed `7763d1928` |
| C2: book round 1, the plan, a prose slip | done | all 5 proofs `True`, numstat matches exactly; committed `789efae86` |
| C3: the project's upkeep ledger (T002) | done | all 4 proofs `True`, numstat matches exactly (475 insertions); committed `93b6cd1a9` |
| Gate 1 | passed | 11 of 11 digests `True` |
| Gate 2 | passed | status empty; 5+4 byte proofs `True` |
| Gate 3 | passed | `6235 passed, 4 skipped`, no FAILED/ERROR, exit 0 |
| Gate 4 | passed | `All checks passed!`, exit 0 |
| Gate 5 | passed | six checks `pass`, `fail_count: 0`; open finding ids match exactly; exit 0 |
| C4: handback | done | this commit |
| Gate 6 (push) | pending | reported in the worker's final reply |
