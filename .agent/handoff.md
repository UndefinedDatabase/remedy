# Handback — F205 round 7: book round 6, register R-1237, the upkeep over several projects, the leak regression, and R-1237's repair

## Session

SESSION 1 of feature F205 · round 7 · rounds so far 7

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~80 % (every building slice done · closure open) — Schätzung

## Range

Review of `492d336a4`..`ca79bfa5f` (4 commits on `feature/f205-multi-repo-missions` — C1
`3f7f25b71`, C2 `1a4c68b73`, C3 `1ac22f9cf`, C4 `ca79bfa5f` — plus this handback, C5).

## Commits

### `3f7f25b71` F205 R7 C1: book round 6, a prose slip, register R-1237, DECISION F205 D7, the plan, save the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f205-r7.md` | 137/0 | NEW FILE — byte copy of `block.md` |
| `.agent/decisions.md` | 10/0 | appended `src/append-decisions.txt` — DECISION F205 D7 |
| `.agent/live_review.md` | 4/0 | appended `src/ledger-append.txt` — books F205 R6 PASS and registers R-1237 |
| `.agent/plan.md` | 10/9 | rewritten with `prep/c1/.agent/plan.md` — round 7's goal, current step and next steps |
| `.agent/prose_slips.md` | 1/0 | appended `src/prose-append.txt` — round 6's prose slip |

### `1a4c68b73` F205 R7 C2: the upkeep of a mission over several projects works where its next job works, and a leak regression over mission data (DECISION F205 D7)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/mission-upkeep-v1.md` | 6/0 | one paragraph on the upkeep page: a mission over several projects |
| `packages/orchestration/mission_upkeep.py` | 40/5 | `upkeep_target` added; `plan_upkeep` takes `root` and filters to the target project's jobs for a mission over several projects |
| `tests/cli/test_do_several_projects.py` | 27/0 | the leak regression: each project lists its own job, the mission is named by reference only |
| `tests/orchestration/test_mission_upkeep.py` | 43/0 | the cadence counts jobs of every repository; the upkeep job works and carries where the chain ends |

### `1ac22f9cf` F205 R7 C3: the contract test imports study before it replaces the model-call factories (R-1237)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_mission_contract.py` | 3/0 | `test_a_do_job_is_bound_to_its_own_repo_path_and_granted` imports `packages.orchestration.study` before replacing the model-call factories |

### `ca79bfa5f` F205 R7 C4: resolve R-1237

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/0 | appended `src/done-append.txt` — R-1237's `Done:` paragraph |

### This commit — F205 R7 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

- `git -C /home/decodeux/Repos/remedy push origin feature/f205-multi-repo-missions` — pending,
  reported in the worker's final reply only (runs after this commit, per the block's `THEN`).
- No `gh pr create`, no `gh pr list` run this round (the block's C0 did not order it, and the
  block's own `THEN` says not to open a pull request). No `claude` process started. No merge, no
  branch creation/move/deletion, no force-push, no stash entry touched, no worktree added or
  removed.

## Verification

**Opening verification** (`verify_block.py`, run as `python3 -I <path>`, before the block was read
whole): `block.md` sha256 `bd716408632d66476ad628f08bb0b0b43834801843c7bd7b9e61abb0bd5b79e6`, 137
lines — both equal the order's stated values.

**Gate 1** (`gate1_digests.py`, after C0 and before C1): every line of `digests.txt` (17 entries)
checked against the file it names — all 17 `True`.

**C0 preconditions**: `git rev-parse HEAD` read `492d336a4f259c7abd07bb64f939a96c20baf1bc`, equal
to `origin/feature/f205-multi-repo-missions`; `git status --porcelain` empty; `.agent/STOP` absent.
No pull. `git branch --show-current` re-run explicitly as a command of its own immediately before
C1, C2, C3 and C4, and read `feature/f205-multi-repo-missions` every time.

**C1** (`c1_copy.py`, ran once; `c1_verify.py`, read-only): copied `block.md` to
`.agent/authored/f205-r7.md`, and the four `prep/c1/.agent/` files over their paths. Proofs: each
of the five copies byte-equal to its prepared file, `True` (5 of 5); the new authored file's
sha256/line count re-read as
`bd716408632d66476ad628f08bb0b0b43834801843c7bd7b9e61abb0bd5b79e6`/137, matching the opening check;
and `live_review.md`, `prose_slips.md`, `decisions.md` each equal `git show 492d336a4:<path>`
followed by its slice (`ledger-append.txt`, `prose-append.txt`, `append-decisions.txt`), `True` (3
of 3). Self-review: the whole `git diff --cached` (218 lines) written to
`.remedy-wt/f205-r7-worker/c1_diff_cached.txt` and read whole — exactly the five ordered paths, one
new file, no unrelated edit. `git diff --cached --numstat` (162 insertions, 9 deletions, under the
500-line cap) matched the table above. Committed as `3f7f25b71`; `git show --numstat` matched.

**C2** (`c2_copy.py`, ran once; `c2_verify.py`, read-only): copied the four prepared files over
their paths. Checked against CHOSEN (1) to (5) of DECISION F205 D7 and nothing more:
`upkeep_target` answers the project and repository an upkeep job works in, through
`follow_up_target` for a mission over several projects, else the mission's own project and its
registered repository; `plan_upkeep` takes `root`, measures that repository and, for a mission
over several projects, filters the ledger lines to the target project's own jobs before carrying
findings and replaced files; the cadence (`upkeep_cadence`) is unchanged and gains a test over two
repositories; the leak regression holds `remedy job list`/`remedy mission list`/`remedy mission
show` scoped per F148; the upkeep page gains one paragraph. Nothing more was found changed.
Proofs: all four copied files byte-equal to their prepared file, `True` (4 of 4). `git diff
--cached` (183 lines) written to `.remedy-wt/f205-r7-worker/c2_diff_cached.txt` and read whole —
exactly the four ordered paths, no unrelated edit; 116 insertions, 5 deletions, under the 500-line
cap. Committed as `1a4c68b73`; `git show --numstat` matched.

**C3** (`c3_copy.py`, ran once; `c3_verify.py`, read-only): copied the one prepared file over its
path. Checked: `test_a_do_job_is_bound_to_its_own_repo_path_and_granted` gains the import of
`packages.orchestration.study` and its two comment lines, placed before the `monkeypatch.setattr`
calls that replace the model-call factories, and nothing else in the file changed. Proof: the
copied file byte-equal to its prepared file, `True`. `git diff --cached` (14 lines) written to
`.remedy-wt/f205-r7-worker/c3_diff_cached.txt` and read whole — exactly the one ordered path, the
import and its two comment lines only; 3 insertions, under the 500-line cap. Committed as
`1ac22f9cf`; `git show --numstat` matched.

**C4** (`c4_preverify.py`, read-only, before the copy; `c4_copy.py`, ran once; `c4_verify.py`,
read-only, after the copy): proved the prepared file equal to `git show HEAD:.agent/live_review.md`
(the file as it stood after C3) followed by the bytes of `src/done-append.txt`, `True`, before
copying; copied the one prepared file over its path; proved the copy byte-equal to the prepared
file, `True`, after copying. `git diff --cached` (10 lines) written to
`.remedy-wt/f205-r7-worker/c4_diff_cached.txt` and read whole — exactly `.agent/live_review.md`,
the `Done:` paragraph only, no unrelated edit; 2 insertions, under the 500-line cap. Committed as
`ca79bfa5f`; `git show --numstat` matched.

**Gate 2** (`gate2_verify.py`, after C4): `git status --porcelain` empty. The byte proofs of C1 to
C4 re-run at this commit against `git show <commit>:<path>` for each commit's own paths: 11 of 11
comparisons `True`.

**Gate 3** (`gate3_pytest.py`, run once, from the primary checkout):
```
python3 -m pytest -q -rfEs @/home/decodeux/Repos/remedy/.remedy-wt/f205-r7/selection.txt
```
exit 0; `5486 passed, 3 skipped in 379.89s (0:06:19)`, no FAILED or ERROR line. The three SKIPPED
lines: `tests/test_agent_tooling.py:43` (D12 quarantine, F252, pre-existing),
`tests/test_install_smoke.py:175` (install smoke is opt-in),
`tests/test_repair_context_reviewer_memory.py:257` (UI source not found).

**Gate 4** (`gate4_ruff.py`):
```
python3 -m ruff check packages/orchestration/mission_upkeep.py tests/orchestration/test_mission_upkeep.py tests/cli/test_do_several_projects.py tests/orchestration/test_mission_contract.py
```
exit 0: `All checks passed!`.

**Gate 5** (`gate5_integrity.py`):
```
python3 -m apps.cli.main integrity check --json
```
exit 0: six checks `pass` (`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`), `"fail_count": 0`, `"ok": true`.

```
python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
exit 0: `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1162', 'R-1172',
'R-1176', 'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230', 'R-1235']` — matches the block's ordered
list exactly.

**No new line in this round's commits (`492d336a4`..`ca79bfa5f`) carries `promot`** except the one
line inside `.agent/authored/f205-r7.md` quoting that very constraint sentence — `.agent/` is
outside `tests/docs/test_retired_promote_word.py`'s scanned scope (`apps`, `packages`, `scripts`,
`tests`, `docs`, `README.md`), the same situation every earlier round's saved block carried without
a finding (checked with `promot_check.py`: one hit, that line, 0 elsewhere).

**After the push** — reported in the worker's final reply only.

## Authored-text proofs

`.agent/authored/f205-r7.md` = `block.md`, sha256 and line count both equal, proven in C1 and
re-proven at the opening check. No other reviewer-authored free text was applied this round; every
C1 append, the C4 append, and every C2/C3 path was applied by a plain byte copy or a bytes-append
of a prepared file and proven byte-equal against that file, not authored free text from the
worker.

## Deviations & assumptions

None.

## Round verdicts

Round 6's PASS is booked by C1 (appended into `.agent/live_review.md` as the "Gate: F205 R6" entry,
part of `src/ledger-append.txt`). Round 7's verdict is the reviewer's.

## For the operator, in plain sentences

The cleanup job a mission makes after every fifth finished job now counts the jobs of every
repository a mission covers, and works in the repository where the mission's next job would work,
carrying only the problems found there. A new test shows that each project still lists only its
own jobs and that a mission shows only the names and states of its jobs in other projects.
Remedy's reviewer also found an old test that could make an unrelated test fail when both ran in
the same process, and fixed it. This was the last building round, and the next rounds close the
feature. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Rule 2 (the Open PR Gate).
3. Book round 7's verdict in the next round's first commit.
4. Closure: the checklist's consolidation pass, the self-use item, the one full suite.

Operator questions open: 0.
Open findings: 16 (R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176,
R-1196, R-1219, R-1220, R-1225, R-1230 and R-1235, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0: base and branch | done | preconditions all confirmed; no pull; branch checked before C0, C1, C2, C3, C4 |
| Gate 1 | passed | 17 of 17 digest comparisons `True` |
| C1: book round 6, a prose slip, register R-1237, DECISION F205 D7, the plan, save the block | done | 5 of 5 byte proofs `True`, 3 of 3 concatenation proofs `True`; committed `3f7f25b71` |
| C2: the upkeep of a mission over several projects works where its next job works, and a leak regression over mission data | done | 4 of 4 byte proofs `True`; checked against CHOSEN (1) to (5) of DECISION F205 D7; committed `1a4c68b73` |
| C3: the contract test imports study before it replaces the model-call factories | done | 1 of 1 byte proof `True`; committed `1ac22f9cf` |
| C4: resolve R-1237 | done | pre-copy and post-copy proofs `True`; committed `ca79bfa5f` |
| Gate 2 | passed | status clean; 11 of 11 byte proofs re-run `True` |
| Gate 3 | passed | `5486 passed, 3 skipped` at exit 0, no FAILED/ERROR, run once as a saved script |
| Gate 4 | passed | ruff `All checks passed!`, exit 0 |
| Gate 5 | passed | integrity 6/6 `pass`, `fail_count 0`; open-findings list matches exactly |
| Push | pending | reported in the worker's final reply |
