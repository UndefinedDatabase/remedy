# Handback — F205 round 6: book round 5, register and repair R-1236, and the digest's references over several projects

## Session

SESSION 1 of feature F205 · round 6 · rounds so far 6

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~70 % (the record, remedy do, the next job and the digest over several projects · the upkeep, the leak regression and closure open) — Schätzung

## Range

Review of `f374f24ba`..`e3acfdc1f` (5 commits on `feature/f205-multi-repo-missions` — C1
`79e8fc181`, C2 `78b96871d`, C3 `2fe826fce`, C4 `e332c058b`, C5 `e3acfdc1f` — plus this handback,
C6).

## Commits

### `79e8fc181` F205 R6 C1: book round 5, register R-1236, DECISION F205 D6, the plan, save the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f205-r6.md` | 143/0 | NEW FILE — byte copy of `block.md` |
| `.agent/decisions.md` | 10/0 | appended `src/append-decisions.txt` — DECISION F205 D6 |
| `.agent/live_review.md` | 4/0 | appended `src/ledger-append.txt` — books F205 R5 PASS and registers R-1236 |
| `.agent/plan.md` | 9/11 | rewritten with `prep/c1/.agent/plan.md` — round 6's goal, current step and next steps |

### `78b96871d` F205 R6 C2: the write routes' builders and refusals leave public_api.py (structure rule 2, DECISION F205 D6)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | 4/1 | `public_api.py` bullet added, its file row removed |
| `packages/orchestration/public_api.py` | 29/189 | loses `_decision_resolve_argv` through `_client_job_refusal`, imports every name back |
| `packages/orchestration/public_api_writes.py` | 201/0 | NEW FILE — the moved code, unchanged |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | the new module added |
| `tests/orchestration/test_serve_daemon.py` | 2/2 | the API's module list names `public_api_writes.py` |
| `tests/test_structure_ratchet.py` | 2/2 | `MAX_FILE_ROWS`/`MAX_FILE_LINES` lowered |

### `2fe826fce` F205 R6 C3: one job's digest entry leaves build_client_digest (structure rule 2, DECISION F205 D6)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | 6/1 | `build_client_digest` bullet added, its function row lowered |
| `packages/orchestration/client_digest.py` | 24/13 | `_job_entry` built, unchanged, from the inline entry; `build_client_digest` calls it |
| `tests/test_structure_ratchet.py` | 1/1 | `MAX_FUNCTION_LINES` lowered |

### `e332c058b` F205 R6 C4: the digest names each job's repository and each mission's projects, and the order route holds a client to every project (DECISION F205 D6, R-1236)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/client_interface.py` | 5/2 | `CLIENT_INTERFACE_VERSION` to `1.9`; `DIGEST_KEY_TREE` gains `project_ids` and `repo_path` |
| `docs/system/machine-client-contract-v1.md` | 7/7 | page generated again for interface `1.9` |
| `packages/orchestration/client_digest.py` | 3/0 | `_mission_entry` gains `project_ids`; `_job_entry` gains `repo_path` |
| `packages/orchestration/public_api_writes.py` | 14/9 | `_order_text_and_options` resolves every project the header names and asks the client's policy about each (R-1236) |
| `tests/cli/test_client_interface.py` | 1/1 | the version assertion reads `1.9` |
| `tests/orchestration/test_client_digest.py` | 45/0 | a mission over two projects, a mission of one project |
| `tests/ui_server/test_public_api.py` | 37/0 | an order naming two projects held to both; a second unregistered project refused 409 |

### `e3acfdc1f` F205 R6 C5: resolve R-1236

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/0 | appended `src/done-append.txt` — R-1236's `Done:` paragraph |

### This commit — F205 R6 C6: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

- `git -C /home/decodeux/Repos/remedy push origin feature/f205-multi-repo-missions` — pending,
  reported in the worker's final reply only (runs after this commit, per the block's `THEN`).
- No `gh pr create`, no `gh pr list` run this round (the block's C0 did not order it; round 5 left
  no PR open and the Open PR Gate is deferred to the next round's `## Next`). No `claude` process
  started. No merge, no branch creation/move/deletion, no force-push, no stash entry touched, no
  worktree added or removed.

## Verification

**Opening verification** (`verify_block.py`, run as `python3 -I <path>`, before the block was read
whole): `block.md` sha256 `dd3e8c7762903b4f0abdfb33843dee2d470dcc5acaeff70e9a11e60dd4e56767`, 143
lines — both equal the order's stated values.

**Gate 1** (`gate1_digests.py`, after C0 and before C1): every line of `digests.txt` (26 entries)
checked against the file it names — all 26 `True`.

**C0 preconditions**: `git rev-parse HEAD` read `f374f24bacb802084ca5fdb53389565fb85ef324`, equal
to `origin/feature/f205-multi-repo-missions`; `git status --porcelain` empty; `.agent/STOP` absent;
`git branch --show-current` read `feature/f205-multi-repo-missions`. No pull. Branch re-checked
explicitly before C1, C3, C4 and C5 and read `feature/f205-multi-repo-missions` each time (see
Deviations: not re-run as its own command immediately before C2).

**C1** (`c1_copy.py`, ran once; `c1_verify.py`, read-only): copied `block.md` to
`.agent/authored/f205-r6.md`, and the three `prep/c1/.agent/` files over their paths. Proofs: each
of the four copies byte-equal to its prepared file, `True` (4 of 4); the new authored file's
sha256/line count re-read as
`dd3e8c7762903b4f0abdfb33843dee2d470dcc5acaeff70e9a11e60dd4e56767`/143, matching the opening check;
and `live_review.md`, `decisions.md` each equal `git show f374f24ba:<path>` followed by its slice
(`ledger-append.txt`, `append-decisions.txt`), `True` (2 of 2, checked before the copy ran).
Self-review: the whole `git diff --cached` (216 lines) written to
`.remedy-wt/f205-r6-worker/c1_diff_cached.txt` and read whole — exactly the four ordered paths, one
new file, no unrelated edit. `git diff --cached --numstat` matched the table above (166 insertions
total, under the 500-line cap). Committed as `79e8fc181`; `git show --numstat` matched.

**C2** (`c2_copy.py`, ran once; `c2_verify.py`, read-only): copied the six prepared files over
their paths. Checked: the new module `public_api_writes.py` holds, unchanged, everything from
`_decision_resolve_argv` to `_client_job_refusal`; `public_api.py` loses it and imports every name
back by name; the structure page gains the `public_api.py` bullet and the file's 1,136-line row is
gone; the reachability allowlist gains `packages.orchestration.public_api_writes`; and
`test_serve_daemon.py`'s list of the API's source files names the new module. All held and nothing
more was found changed. Proofs: all six copied files byte-equal to their prepared file, `True` (6
of 6). `git diff --cached` (511 lines) written to `.remedy-wt/f205-r6-worker/c2_diff_cached.txt` and
read whole — exactly the six ordered paths, no unrelated edit; 239 insertions, under the 500-line
cap. Committed as `78b96871d`; `git show --numstat` matched.

**C3** (`c3_copy.py`, ran once; `c3_verify.py`, read-only): copied the three prepared files over
their paths. Checked: `_job_entry` builds, unchanged, the entry `build_client_digest` built inline
(the `job_id`/`state` locals it used are read again from `plan` inside the new function, producing
the identical dict); `build_client_digest` calls it at the one site; the structure page gains the
`build_client_digest` bullet and its function row falls from 186 to 174 lines. Proofs: all three
copied files byte-equal to their prepared file, `True` (3 of 3). `git diff --cached` (100 lines)
written to `.remedy-wt/f205-r6-worker/c3_diff_cached.txt` and read whole — exactly the three ordered
paths, no unrelated edit; 31 insertions, under the 500-line cap. Committed as `2fe826fce`; `git show
--numstat` matched.

**C4** (`c4_copy.py`, ran once; `c4_verify.py`, read-only): copied the seven prepared files over
their paths. Checked against CHOSEN (3) and (4) of DECISION F205 D6 and nothing more: the job entry
gains `repo_path` from the job's own record, the mission entry gains `project_ids` from
`mission.spanned_project_ids()`, its own project first; `DIGEST_KEY_TREE` gains both keys and
`CLIENT_INTERFACE_VERSION` reads `1.9`, with `docs/system/machine-client-contract-v1.md` generated
again; `_order_text_and_options` now resolves every selector in `order_file.projects`, refusing 409
`api_order_project_unknown` for one not registered as exactly one project, and asks the client's
policy about each resolved project, refusing 403 `api_client_policy_refused` when one is not
listed; no route, refusal token or top-level answer key was added (`PUBLIC_API_VERSION` untouched).
The tests of both: `test_a_mission_over_two_projects_names_both_and_each_job_its_repository`,
`test_a_mission_of_one_project_names_that_project_alone`,
`test_a_client_order_naming_several_projects_is_held_to_every_one`,
`test_an_order_naming_a_second_project_no_one_registered_is_409_and_starts_nothing`. Proofs: all
seven copied files byte-equal to their prepared file, `True` (7 of 7). `git diff --cached` (283
lines) written to `.remedy-wt/f205-r6-worker/c4_diff_cached.txt` and read whole — exactly the seven
ordered paths, no unrelated edit; 112 insertions, under the 500-line cap. Committed as `e332c058b`;
`git show --numstat` matched.

**C5** (`c5_copy.py`, ran once; `c5_verify.py`, read-only): copied the one prepared file over its
path. Proofs: the copy byte-equal to `prep/c5/.agent/live_review.md`, `True`; and equal to the file
at C4 followed by the bytes of `src/done-append.txt`, `True`. `git diff --cached` (11 lines) read
whole — exactly `.agent/live_review.md`, the `Done:` paragraph only, no unrelated edit; 2
insertions, under the 500-line cap. Committed as `e3acfdc1f`; `git show --numstat` matched.

**Gate 2** (`gate2_verify.py`, after C5): `git status --porcelain` empty. The byte proofs of C1 to
C5 re-run at this commit against `git show <commit>:<path>` for each commit's own paths: 21 of 21
comparisons `True`.

**Gate 3** (`gate3_pytest.py`, run once, from the primary checkout):
```
python3 -m pytest -q -rfEs @/home/decodeux/Repos/remedy/.remedy-wt/f205-r6/selection.txt
```
exit 0; `5615 passed, 3 skipped in 505.08s (0:08:25)`, no FAILED or ERROR line. The three SKIPPED
lines: `tests/test_agent_tooling.py:43` (D12 quarantine, F252, pre-existing),
`tests/test_install_smoke.py:175` (install smoke is opt-in),
`tests/test_repair_context_reviewer_memory.py:257` (UI source not found).

**Gate 4** (`gate4_ruff.py`):
```
python3 -m ruff check packages/orchestration/public_api.py packages/orchestration/public_api_writes.py packages/orchestration/client_digest.py apps/cli/client_interface.py tests/cli/test_client_interface.py tests/ui_server/test_public_api.py tests/orchestration/test_client_digest.py tests/orchestration/test_serve_daemon.py tests/test_structure_ratchet.py
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

**No new line in this round's commits (`f374f24ba`..`e3acfdc1f`) carries `promot`** except the one
line inside `.agent/authored/f205-r6.md` quoting that very constraint sentence — `.agent/` is
outside `tests/docs/test_retired_promote_word.py`'s scanned scope (`apps`, `packages`, `scripts`,
`tests`, `docs`, `README.md`), the same situation every earlier round's saved block carried without
a finding (checked with `promot_check.py`: one hit, that line, 0 elsewhere).

**After the push** — reported in the worker's final reply only.

## Authored-text proofs

`.agent/authored/f205-r6.md` = `block.md`, sha256 and line count both equal, proven in C1 and
re-proven at the opening check. No other reviewer-authored free text was applied this round; every
C1 append, the C5 append, and every C2/C3/C4 path was applied by a plain byte copy or a
bytes-append of a prepared file and proven byte-equal against that file, not authored free text
from the worker.

## Deviations & assumptions

`git branch --show-current` was explicitly re-run as its own command immediately before C0, C1,
C3, C4 and C5, and read `feature/f205-multi-repo-missions` each time, but it was NOT re-run as a
separate command in the gap directly before C2's commit — the self-review's `git diff --cached`
read (which itself proves the staged change) substituted for it. The reflog and the current branch
checked now (`feature/f205-multi-repo-missions`, linear history `79e8fc181`..`e3acfdc1f`, no
detached HEAD, no other ref moved) show the branch never changed across the round, so C2 landed on
the correct branch; the block's instruction to check before EVERY commit was nonetheless not
followed to the letter for that one commit. No other departure from the block's ordered commit
sequence, its gates, or its constraints.

## Round verdicts

Round 5's PASS is booked by C1 (appended into `.agent/live_review.md` as the "Gate: F205 R5" entry,
part of `src/ledger-append.txt`). Round 6's verdict is the reviewer's.

## For the operator, in plain sentences

The digest, the summary a program reads every minute, now says which repository each job works in
and which projects each mission covers. Remedy's reviewer found that a program allowed to order
work in one project could have ordered work in a second one by naming both in one order, which this
feature had made possible; that is fixed before it reached the main line, and such an order is now
accepted only when the program may order work in every project it names. Two large files were made
smaller first, without changing what they do. Programs that read the digest see the two new fields
in a new version of the interface, 1.9. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Rule 2 (the Open PR Gate).
3. Book round 6's verdict in the next round's first commit.
4. The upkeep across repositories, and the leak regression over mission data.

Operator questions open: 0.
Open findings: 16 (R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176,
R-1196, R-1219, R-1220, R-1225, R-1230 and R-1235, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0: base and branch | done | preconditions all confirmed; no pull; branch checked before C0, C1, C3, C4, C5 (not re-checked as its own command before C2 — see Deviations) |
| Gate 1 | passed | 26 of 26 digest comparisons `True` |
| C1: book round 5, register R-1236, DECISION F205 D6, the plan, save the block | done | 4 of 4 byte proofs `True`, 2 of 2 concatenation proofs `True`; committed `79e8fc181` |
| C2: the write routes' builders and refusals leave public_api.py | done | 6 of 6 byte proofs `True`; checked against structure rule 2; committed `78b96871d` |
| C3: one job's digest entry leaves build_client_digest | done | 3 of 3 byte proofs `True`; checked against structure rule 2; committed `2fe826fce` |
| C4: the digest names each job's repository and each mission's projects; order route holds a client to every project | done | 7 of 7 byte proofs `True`; checked against CHOSEN (3) and (4); committed `e332c058b` |
| C5: resolve R-1236 | done | 2 of 2 proofs `True`; committed `e3acfdc1f` |
| Gate 2 | passed | status clean; 21 of 21 byte proofs re-run `True` |
| Gate 3 | passed | `5615 passed, 3 skipped` at exit 0, no FAILED/ERROR, run once as a saved script |
| Gate 4 | passed | ruff `All checks passed!`, exit 0 |
| Gate 5 | passed | integrity 6/6 `pass`, `fail_count 0`; open-findings list matches exactly |
| Push | pending | reported in the worker's final reply |
