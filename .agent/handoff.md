# Handoff — F299 round 4: book round 3 + R-1227's resolution + R-1228/R-1229, repair both, and T004

## Session

SESSION 1 of feature F299 · round 4 · rounds so far 4

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~80 % (T001 to T004 · the closure open) — Schätzung

## Range

Review of `4ccf09be0d6ac73cbfda90795e904531d28e4f38`..HEAD (six commits on
`feature/f299-acceptance-checks-other-repos`: C1 through C5 and this handback).

## Commits

### `d97544208` F299 R4 C1: save the round 4 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f299-r4.md` | 172/0 | NEW FILE — a verbatim copy of `block.md`; sha256 and line count checked equal to the source (both `221a612f4aa0b34a8e3ae4341bd6d6f4281b190b21cddf9c8a07dc92719e7672`, 172 lines) |

### `6b40e103b` F299 R4 C2: book round 3, resolve R-1227, register R-1228 and R-1229, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 8/0 | appends `Gate: F299 R3` (FAIL), `Done: R-1227` (resolved), and R-1228/R-1229, booking round 3's verdict |
| `.agent/plan.md` | 12/10 | rewritten for round 4's current step, next steps and risks |

### `ab2bde44f` F299 R4 C3: the refusal's new sentence in the loop's test, and the two words of DECISION F299 D2 (4) under test (R-1228, R-1229)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_orchestrator_loop.py` | 1/1 | R-1228: the pinned refusal string reads `"status is open, met, unmet or unchecked"`, matching the production message round 3 already wrote; nothing else in the file changes |
| `tests/orchestration/test_dod_gate.py` | 27/2 | R-1229: `TestJobDodCommand._show` is narrowed to the `Dod` section's own text (stopping before `--- Tour ---`), so its existing "no check ran" assertion is pinned to `_dod_section`'s own line rather than satisfied by `Tour`'s echo of the same sentence; `TestReportMatrix` gains a test giving `_dod_lines` a held gate with one truly red check and one `no_test_command` check, asserting the held sentence counts and names only the red one |

### `9d72a3cb4` F299 R4 C4: four scratch projects through remedy do to the push (T004)

| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_do_project_targets.py` | 178/0 | NEW FILE — four tests driving `remedy do --commit ... --push` on scratch projects of their own: a Python project with its own `.venv` (criterion `met`, check kind `project_tests`, evidence command begins with the venv's `python -m pytest`, one push, both criteria lists empty); a Node project via `npm test` (criterion `met`, evidence command `npm test`, one push); a project with only `README.md` (criterion `unchecked`, `unmet_blocking_criteria` empty, pushed with the id under `push["unchecked_blocking_criteria"]`, the gate released with the check in `not_run`, the apply detail, the contract summary line and `job show --full`'s own text all carrying `NO_CHECK_RAN_WORDS`); and the first project's test given a wrong assertion (criterion `unmet`, exit 1, no push, the push error naming "are unmet, so nothing is pushed") |

### `4cbf0db76` F299 R4 C5: the page on a project's own test command, and its index rows (T004)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/acceptance-checks-v1.md` | 78/0 | NEW FILE — a verbatim copy of the reviewer's prepared page, proved byte-equal |
| `docs/README.md` | 2/0 | the two prepared index rows (quick-find table and the system-docs list), proved byte-equal against the reviewer's `dry-README.md` |

### This commit (self-reference) — F299 R4 C6: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

None besides the push below: no `gh pr create`, no `gh pr merge`, no new branch, no stash entry
touched, no `git worktree add`/`remove` by the worker itself.

`git push origin feature/f299-acceptance-checks-other-repos` after C6 — reported in the worker's
final reply.

## Verification

**Gate 1** (before C1, from the primary checkout): a Python sha256 reader over `digests.txt`'s
five files (`block.md`, `dry-live_review.md`, `dry-plan.md`, `acceptance-checks-v1.md`,
`dry-README.md`). Exit 0 (script). All five sha256 digests **and** line counts matched.

**Gate 2** (after C5): `git -C /home/decodeux/Repos/remedy status --porcelain` empty: **True**.
C2 step 2's two byte-equality proofs, re-run read-only at `4cbf0db76`: both **True**
(`.agent/live_review.md` == blob at `4ccf09be0` + `src/ledger-append.txt`; `.agent/live_review.md`
== `dry-live_review.md`; `.agent/plan.md` == `dry-plan.md`). C5's two byte-equality proofs,
re-run read-only at the same commit: both **True** (`docs/system/acceptance-checks-v1.md` ==
`acceptance-checks-v1.md`; `docs/README.md` == `dry-README.md`).

**Gate 3** (once, after C5), from the primary checkout:
```
python3 -m pytest -q -rfEs @/home/decodeux/Repos/remedy/.remedy-wt/f299-r4/selection.txt
```
Exit **0**. Summary line: `3961 passed, 3 skipped in 187.05s (0:03:07)`. No FAILED or ERROR line.
The 3 SKIPPED lines, verbatim (pre-existing quarantines, unrelated to this round's files):
```
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
```

**Gate 4**:
```
python3 -m ruff check tests/orchestration/test_orchestrator_loop.py tests/orchestration/test_dod_gate.py tests/cli/test_do_project_targets.py
```
Exit **0**. Output: `All checks passed!`

**Gate 5**:
```
python3 -m pytest -q -rfEs tests/cli/test_do_project_targets.py --collect-only
```
Exit **0**. The four node ids, verbatim:
```
tests/cli/test_do_project_targets.py::test_a_python_project_with_its_own_venv_is_judged_by_its_own_pytest_and_pushed
tests/cli/test_do_project_targets.py::test_a_node_project_run_by_npm_test_is_judged_by_it_and_pushed
tests/cli/test_do_project_targets.py::test_a_project_with_no_test_command_reads_unchecked_and_pushes_anyway
tests/cli/test_do_project_targets.py::test_a_python_projects_own_failing_test_refuses_the_push
```

**Gate 6**:
```
python3 -m apps.cli.main integrity check --json
```
Exit **0**. `"check_count": 6`, `"fail_count": 0`, `"ok": true`, `"passed": true`, all six checks
`"status": "pass"` (`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`).
```
python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
Exit **0**. Output, verbatim:
```
['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1228', 'R-1229']
```
Matches the block's ordered list exactly.

## Authored-text proofs

`.agent/authored/f299-r4.md` (the saved block, C1) equals `block.md` byte for byte: sha256
`221a612f4aa0b34a8e3ae4341bd6d6f4281b190b21cddf9c8a07dc92719e7672` on both sides, 172 lines each.
The other reviewer-prepared files applied this round (`dry-live_review.md`, `dry-plan.md` in C2;
`acceptance-checks-v1.md`, `dry-README.md` in C5) were proved byte-equal to their committed copies
both at the time of their commit and again, read-only, at gate 2 — see Verification above.

## Deviations & assumptions

- **C0**: all of C0's checks (HEAD at `4ccf09be0d6ac73cbfda90795e904531d28e4f38`, branch
  `feature/f299-acceptance-checks-other-repos`, `git status --porcelain` empty, `.agent/STOP`
  absent) held exactly as the block states, checked before any write; the branch was re-checked
  with `git branch --show-current` immediately before every commit (C1 through C5).
- **Two transient, uncommitted diagnostic mutations, made and reversed before any commit touched
  them**: while writing C3's repair for R-1229, the worker needed to confirm its two test changes
  were genuinely load-bearing (red under the defect they repair) rather than coincidentally
  passing. It temporarily removed the `if not_run:` block from `_dod_section` in
  `apps/cli/commands/job.py` (confirming `test_a_not_run_check_reads_released_with_no_blocking_red_and_no_reported_reds`
  then failed, and passed again once reverted with `git checkout -- apps/cli/commands/job.py`),
  and temporarily removed the `and c.reason != REASON_NO_TEST_COMMAND` clause from the held branch
  of `_dod_lines` in `packages/orchestration/run_report.py` (confirming the new
  `test_a_held_gate_counts_only_the_truly_red_check_not_the_one_that_did_not_run` then failed, and
  passed again once reverted with `git checkout -- packages/orchestration/run_report.py`).
  `git status --porcelain` was checked clean after each revert, before any staging or commit. No
  commit ever carried either mutation, and no production file changed this round. Declared here
  per the "any departure, even when corrected" rule, not because any committed state was ever
  wrong — the block's "no production code changes this round" held throughout.
- **C1 through C5 and gates 1 through 6** ran exactly as ordered, each gate once, in the block's
  order (gate 1 before C1; C1–C5 in sequence; gates 2–6 in sequence after C5; C6 last). No commit
  was split, none exceeded the 500-insertion cap (largest: C4's 178), and no file outside each
  commit's named paths was touched.

## Round verdicts

Round 3's FAIL is booked into `.agent/live_review.md` by C2 as `Gate: F299 R3`, with R-1227's
resolution recorded as `Done: R-1227` and R-1228 and R-1229 registered beneath it (both repaired
by C3 of this round, not yet resolved by the reviewer). Round 4's own verdict is the reviewer's,
not yet written.

## For the operator, in plain sentences

The last round left one old test expecting the earlier wording of an error, and two of the new
messages without a test; this round fixed both; it then ran Remedy's whole order-to-push path on
four small sample projects — a Python project with its own environment, a JavaScript project, a
project without tests and a Python project whose test fails — and each ends as it should: the
first two pass and push, the third pushes and says that no check ran, the fourth is refused; a new
page explains the rule; nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback
   and stop.
2. Phase 1 rule 2 (the Open PR Gate):
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft` before any further
   branch work.
3. Book round 4's verdict and the resolutions of R-1228 and R-1229 in the next round's first
   commit.
4. The closure's first round: the Built State and the self-use item.

Operator questions open: 0.
Open findings: 17 (R-1160, Medium; R-1228 and R-1229, Low, owned by F299; R-1138, R-1139, R-1143,
R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219, R-1220 and R-1225, Low,
owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0: base checks + gate 1 | done | HEAD, branch, status and STOP all confirmed before any write; gate 1 green |
| C1: save the block | done | `.agent/authored/f299-r4.md`, byte- and line-identical to `block.md` |
| C2: book round 3, resolve R-1227, register R-1228/R-1229, the plan | done | both copies byte-proved against the prepared files and against the base blob + ledger-append slice, re-proved at gate 2 |
| C3: the loop test's new refusal sentence + the two words under test (R-1228, R-1229) | done | both repairs proven load-bearing by a reverted diagnostic mutation; no `Landed:` line written |
| C4: four scratch projects through `remedy do` to the push (T004) | done | all four tests proven green, collected cleanly (gate 5), ruff clean (gate 4) |
| C5: the page + index rows (T004) | done | both copies byte-proved against the prepared files, re-proved at gate 2 |
| C6: handback | done | this commit |
| Gate 1 | passed | all five digests and line counts matched before C1 |
| Gate 2 | passed | status clean; all C2 and C5 byte proofs True at `4cbf0db76` |
| Gate 3 | passed | `3961 passed, 3 skipped` at exit 0, no FAILED/ERROR line |
| Gate 4 | passed | ruff exit 0, all checks passed |
| Gate 5 | passed | exit 0, four node ids collected |
| Gate 6 | passed | six integrity checks pass, fail_count 0; open finding ids match exactly |
| Push | done | reported in the worker's final reply |
