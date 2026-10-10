# Handback — F205 round 4: book round 3, and `remedy do` over an order that names several projects

## Session

SESSION 1 of feature F205 · round 4 · rounds so far 4

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~50 % (the record and remedy do over several projects · the loop, the digest and API, the upkeep and the fixture mission open) — Schätzung

## Range

Review of `58e141e51`..`4f45bcb5c` (3 commits on `feature/f205-multi-repo-missions` — C1
`d3c91c11d`, C2 `92fe3cd27`, C3 `4f45bcb5c` — plus this handback, C4).

## Commits

### `d3c91c11d` F205 R4 C1: book round 3, a prose slip, DECISION F205 D4, the plan, save the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f205-r4.md` | 136/0 | NEW FILE — byte copy of `block.md` |
| `.agent/decisions.md` | 10/0 | appended `src/append-decisions.txt` — DECISION F205 D4 |
| `.agent/live_review.md` | 2/0 | appended `src/ledger-append.txt` — books F205 R3 PASS |
| `.agent/plan.md` | 9/12 | rewritten with `prep/c1/.agent/plan.md` — round 4's goal, current step and next steps |
| `.agent/prose_slips.md` | 1/0 | appended `src/prose-append.txt` — one round 3 prose slip |

### `92fe3cd27` F205 R4 C2: an order names several projects, and remedy do runs one job in each project's repository (DECISION F205 D4)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/client_interface.py` | 13/3 | interface rises to `1.8`; `landed.repo` and `push.repositories` key trees added |
| `apps/cli/commands/do_order_input.py` | 54/5 | refuses `--project`/`--repo` beside several projects; `_several_projects_repo` picks the first project's registered repository |
| `docs/system/machine-client-contract-v1.md` | 15/3 | page regenerated: version `1.8`, new paragraph on an order naming several projects, `landed`/`push` key lists updated |
| `packages/orchestration/do_apply.py` | 76/30 | `do_job_repo`, `do_landed_by_repo`; each job applies and lands in its own repository, each repository's upstream asked before any push, each repository pushed once |
| `packages/orchestration/do_context.py` | 16/3 | third shape `DO_SHAPE_REPOSITORIES`; `DoContext.projects`, `project_repos`, `project_ids` |
| `packages/orchestration/do_sequence.py` | 8/6 | `create_mission` gets `project_ids`; each job's plan uses its own `DoJobTarget` |
| `packages/orchestration/do_summary.py` | 14/3 | `_job_ledger_project`; each job's cost read from its own project's ledger |
| `packages/orchestration/do_targets.py` | 95/14 | `DoJobTarget`; `_init_several_projects` selects every project; `resolve_do_shape` refuses a force flag with several projects; `do_project_order` |
| `packages/orchestration/order_file.py` | 25/5 | `project` may repeat, one per project; `OrderFile.projects`, `project_selector` |
| `tests/cli/test_client_interface.py` | 1/1 | interface-version assertion moves to `1.8` |
| `tests/cli/test_do_commit_flags.py` | 2/1 | a landed entry now carries `repo` |
| `tests/orchestration/test_order_file.py` | 14/2 | repeated-project test renamed to same-project-twice; new test for several projects read in order |

### `4f45bcb5c` F205 R4 C3: the tests of an order over several projects (DECISION F205 D4)

| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_do_several_projects.py` | 242/0 | NEW FILE — the plan, the per-repository commit and push, the upstream-first refusal, the ignore entries, and every refusal of DECISION F205 D4 |

### This commit — F205 R4 C4: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

- `git -C /home/decodeux/Repos/remedy push origin feature/f205-multi-repo-missions` — pending,
  reported in the worker's final reply only (runs after this commit, per the block's `THEN`).
- No `gh pr create`, no `gh pr list` run this round (the block's C0 did not order it; round 3 left
  no PR open and the Open PR Gate is deferred to the next round's `## Next`). No `claude` process
  started. No merge, no branch creation/move/deletion, no force-push, no stash entry touched, no
  worktree added or removed.

## Verification

**Opening verification** (one Python sha256/line-count reader, run as `python3 -I <path>`, before
the block was read whole): `block.md` sha256
`0ed30b00845091a1f27fc822d8f773ccf104b60271a65265ac905466e6e54e30`, 136 lines — both equal the
order's stated values.

**Gate 1** (`gate1_digests.py`, after C0 and before C1): every line of `digests.txt` (23 entries)
checked against the file it names — all 23 `True`.

**C0 preconditions** (`c0_checks.py`): `git rev-parse HEAD` read `58e141e51a8fe90810ca2fed4673c8124cff7ea3`,
equal to `origin/feature/f205-multi-repo-missions`; `git status --porcelain` empty; `.agent/STOP`
absent; `git branch --show-current` read `feature/f205-multi-repo-missions`. No pull. Branch
re-checked before every commit and read `feature/f205-multi-repo-missions` each time.

**C1** (`c1_copy.py`, ran once; `c1_equality_proof.py`, `c1_concat_proof.py`, read-only): copied
`block.md` to `.agent/authored/f205-r4.md`, and the four `prep/c1/.agent/` files over their paths.
Proofs: each of the five copies byte-equal to its prepared file, `True` (5 of 5); the new authored
file's sha256/line count re-read as `0ed30b00845091a1f27fc822d8f773ccf104b60271a65265ac905466e6e54e30`/136,
matching the opening check; and `live_review.md`, `prose_slips.md`, `decisions.md` each equal
`git show 58e141e51:<path>` followed by its slice (`ledger-append.txt`, `prose-append.txt`,
`append-decisions.txt`), `True` (3 of 3). Self-review: the whole `git diff --cached` (215 lines)
written to `.remedy-wt/f205-r4-worker/c1_cached_diff.txt` and read whole — exactly the five ordered
paths, one new file, no unrelated edit. `git diff --cached --numstat` matched the table above.
Committed as `d3c91c11d`; `git show --numstat` matched.

**C2** (`c2_copy.py`, ran once; `c2_equality_proof.py`, read-only): copied the twelve prepared files
over their paths. Checked against DECISION F205 D4's CHOSEN (1) to (8) and nothing more:
`order_file.py` reads one project per `project` line; `do_order_input.py` refuses `--project`,
`--repo` and a project without a repository beside several projects; `do_context.py` gains the
third shape, `projects`, `project_repos`, `project_ids`; `do_targets.py` selects every project,
refuses a force flag and gives each job its project's repository; `do_sequence.py` passes the
projects to the mission, the shape and the plan of each job; `do_apply.py` applies each job in its
own repository and pushes each repository once; `do_summary.py` reads each job's cost from its own
project; `client_interface.py` adds `landed.repo` and `push.repositories` at `1.8`, the contract
page is regenerated with one new paragraph; the three test files change only where DECISION F205 D4
changes what they assert. All held and nothing more was found changed. Proofs: all twelve copied
files byte-equal to their prepared file, `True` (12 of 12). `git diff --cached` (859 lines) written
to `.remedy-wt/f205-r4-worker/c2_cached_diff.txt` and read whole — exactly the twelve ordered paths,
no unrelated edit; 333 insertions, under the 500-line cap. Committed as `92fe3cd27`; `git show
--numstat` matched.

**C3** (`c3_copy_and_proof.py`, ran once and read-only in the same script): copied the one prepared
file over its path, a confirmed new file. Proof: byte-equal to its prepared file, `True`.
`git diff --cached` (248 lines) written to `.remedy-wt/f205-r4-worker/c3_cached_diff.txt` and read
whole — exactly the one ordered path, one new file, no unrelated edit; 242 insertions. Committed as
`4f45bcb5c`; `git show --numstat` matched.

**Gate 2** (`gate2.py`, after C3): `git status --porcelain` empty. The byte proofs of C1 to C3
re-run at this commit against `git show <commit>:<path>` for each commit's own paths: 18 of 18
comparisons `True`.

**Gate 3** (`gate3_pytest.py`, run once, from the primary checkout):
```
python3 -m pytest -q -rfEs @/home/decodeux/Repos/remedy/.remedy-wt/f205-r4/selection.txt
```
exit 0; `7512 passed, 3 skipped in 728.81s (0:12:08)`, no FAILED or ERROR line. The three SKIPPED
lines: `tests/test_agent_tooling.py:43` (D12 quarantine, F252, pre-existing),
`tests/test_install_smoke.py:175` (install smoke is opt-in),
`tests/test_repair_context_reviewer_memory.py:257` (UI source not found).

**Gate 4** (`gate4_ruff.py`):
```
python3 -m ruff check packages/orchestration/order_file.py apps/cli/commands/do_order_input.py packages/orchestration/do_context.py packages/orchestration/do_targets.py packages/orchestration/do_sequence.py packages/orchestration/do_apply.py packages/orchestration/do_summary.py apps/cli/client_interface.py tests/cli/test_client_interface.py tests/cli/test_do_commit_flags.py tests/orchestration/test_order_file.py tests/cli/test_do_several_projects.py
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

**No new line in this round's commits (`58e141e51`..`4f45bcb5c`) carries `promot`** except the one
line inside `.agent/authored/f205-r4.md` quoting that very constraint — `.agent/` is outside
`tests/docs/test_retired_promote_word.py`'s scanned scope (`apps`, `packages`, `scripts`, `tests`,
`docs`, `README.md`), the same situation every earlier round's saved block carried without a
finding (checked with `promot_check.py`: one hit, that line, 0 elsewhere).

**After the push** — reported in the worker's final reply only.

## Authored-text proofs

`.agent/authored/f205-r4.md` = `block.md`, sha256 and line count both equal, proven in C1 and
re-proven at the opening check. No other reviewer-authored free text was applied this round; every
C1 append and every C2–C3 path was applied by a plain byte copy or a bytes-append of a prepared
file and proven byte-equal against that file, not authored free text from the worker.

## Deviations & assumptions

Before C0, the worker's own opening sha256/line-count verification script for `block.md` was first
written to `.remedy-wt/f205-r4/verify_block.py` — inside the reviewer's prepared folder — instead of
`.remedy-wt/f205-r4-worker/`, where the block's constraints require every worker script to live. It
was deleted immediately on discovery, before C0 or any other action ran, and it never read or
altered the contents of any prepared file; no prepared file was modified, and the opening
sha256/line-count readings it produced were correct and unaffected. Every later script ran under
`.remedy-wt/f205-r4-worker/` throughout. Apart from this, C0 through C3 and gates 1 through 5 ran
in the block's order, each copy script ran exactly once, every later proof ran as a separate
read-only script, every script ran as `python3 -I <absolute path>` with the explicit working
directory of `/home/decodeux/Repos/remedy`, no `cd`/`&&`/pipes/heredocs were used in any shell
call, gate 3 ran once as a saved script capturing pytest's own exit code with no extra flags and
no pipe, and gates 1, 2, 4 and 5 ran at the point and in the command the block orders.

## Round verdicts

Round 3's PASS is booked by C1 (appended into `.agent/live_review.md` as the "Gate: F205 R3" entry,
part of `src/ledger-append.txt`). Round 4's verdict is the reviewer's.

## For the operator, in plain sentences

An order file can now name several projects, one line each. `remedy do` then plans one job in each
project's own repository, in the order the file names them, under one mission. With a commit flag
each job is applied and committed in its own repository, and with `--push` each repository is
pushed once, but only after Remedy has checked that every repository can be pushed. An order like
this refuses `--project` and `--repo`, because each job already has its repository. Programs that
read `remedy do`'s answer see which repository each commit and each push belongs to, in a new
version of the interface, 1.8. The next round lets the mission loop run each job in its own
project. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Rule 2 (the Open PR Gate).
3. Book round 4's verdict in the next round's first commit.
4. The mission loop runs each job in its own project's repository.

Operator questions open: 0.
Open findings: 16 (R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176,
R-1196, R-1219, R-1220, R-1225, R-1230 and R-1235, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0: base and branch | done | preconditions all confirmed; no pull; branch checked before every commit |
| Gate 1 | passed | 23 of 23 digest comparisons `True` |
| C1: book round 3, a prose slip, DECISION F205 D4, the plan, save the block | done | 5 of 5 byte proofs `True`, 3 of 3 concatenation proofs `True`; committed `d3c91c11d` |
| C2: an order names several projects, and remedy do runs one job in each project's repository | done | 12 of 12 byte proofs `True`; checked against DECISION F205 D4's CHOSEN (1)-(8); committed `92fe3cd27` |
| C3: the tests of an order over several projects | done | 1 of 1 byte proof `True`; committed `4f45bcb5c` |
| Gate 2 | passed | status clean; 18 of 18 byte proofs re-run `True` |
| Gate 3 | passed | `7512 passed, 3 skipped` at exit 0, no FAILED/ERROR, run once as a saved script |
| Gate 4 | passed | ruff `All checks passed!`, exit 0 |
| Gate 5 | passed | integrity 6/6 `pass`, `fail_count 0`; open-findings list matches exactly |
| Push | pending | reported in the worker's final reply |
