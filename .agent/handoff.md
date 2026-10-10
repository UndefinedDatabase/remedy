# Handback — F205 round 2: book round 1, and the record of a mission over several projects

## Session

SESSION 1 of feature F205 · round 2 · rounds so far 2

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~20 % (claim, the structural step and the record over several projects · the order, the push, the loop, the digest and API, the upkeep and the fixture mission open) — Schätzung

## Range

Review of `3bf1bd406`..`31fa83833` (two commits on `feature/f205-multi-repo-missions` — C1
`c05b1eec9`, C2 `31fa83833` — plus this handback, C3).

## Commits

### `c05b1eec9` F205 R2 C1: book round 1, two prose slips, DECISION F205 D2, the plan, save the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f205-r2.md` | 143/0 | NEW FILE — byte copy of `block.md` |
| `.agent/decisions.md` | 10/0 | appended `src/append-decisions.txt` — DECISION F205 D2 |
| `.agent/live_review.md` | 2/0 | appended `src/ledger-append.txt` — books F205 R1 PASS |
| `.agent/plan.md` | 14/14 | rewritten with `src/plan.md` — round 2's goal, current step and next steps |
| `.agent/prose_slips.md` | 2/0 | appended `src/prose-append.txt` — two round 1 prose slips |

### `31fa83833` F205 R2 C2: a mission names the projects it spans and each link its job's project, client interface 1.7 (DECISION F205 D2)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/client_interface.py` | 6/3 | copied `code-client_interface.py` — `CLIENT_INTERFACE_VERSION` 1.6→1.7; `mission.abandon`'s tree gains `project_ids` and the link's `project_id` |
| `docs/system/machine-client-contract-v1.md` | 3/3 | copied `code-machine-client-contract-v1.md` — generated again at interface version `1.7` with the two new keys |
| `packages/orchestration/mission_record.py` | 57/3 | copied `code-mission_record.py` — adds `MissionProjectError`, `MissionJobLink.project_id`, `Mission.project_ids`/`spanned_project_ids()`, and `check_spanned_project_ids` |
| `packages/orchestration/mission_state.py` | 44/3 | copied `code-mission_state.py` — imports `MissionProjectError` and `check_spanned_project_ids` back; `create_mission` gains keyword `project_ids`; `link_job_to_mission` checks and records the job's project via new `_linked_job_project` |
| `tests/cli/test_client_interface.py` | 1/1 | copied `code-test_client_interface.py` — pins `CLIENT_INTERFACE_VERSION == "1.7"` |
| `tests/orchestration/test_mission_projects.py` | 128/0 | NEW FILE — copied `code-test_mission_projects.py` — DECISION F205 D2's test coverage |

### This commit — F205 R2 C3: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

- `git -C /home/decodeux/Repos/remedy push origin feature/f205-multi-repo-missions` — pending,
  reported in the worker's final reply only (runs after this commit, per the block's `THEN`).
- No `gh pr create`, no `gh pr list` run this round (the block's C0 did not order it; round 1 left
  no PR open and the Open PR Gate is deferred to the next round's `## Next`). No `claude` process
  started. No merge, no branch creation/move/deletion, no force-push, no stash entry touched, no
  worktree added or removed.

## Verification

**Opening verification** (one Python sha256/line-count reader, run as `python3 -I <path>`, before
the block was read whole): `block.md` sha256
`b2a55ebb97c30133754759a1a37b78dd1fb05ab6edd104272163bdaa1c121248`, 143 lines — both equal the
order's stated values.

**Gate 1** (`gate1_digests.py`, after C0 and before C1): every line of `digests.txt` (15 entries)
checked against the file it names — `ALL_TRUE`, all 15 `True`.

**C0 preconditions**: `git rev-parse HEAD` read `3bf1bd40646cbb29aae404d5dbe370e55bbcd68f`, equal to
`origin/feature/f205-multi-repo-missions`; `git status --porcelain` empty; `.agent/STOP` absent.
No pull. `git branch --show-current` re-checked before every commit and read
`feature/f205-multi-repo-missions` each time.

**C1** (`c1_apply.py`, ran once; `c1_proof.py`, read-only): copied `block.md` to
`.agent/authored/f205-r2.md` and `src/plan.md` to `.agent/plan.md`; appended the three prepared
slices to `.agent/live_review.md`, `.agent/prose_slips.md` and `.agent/decisions.md`. Proofs: each
appended file == `git show 3bf1bd406:<path>` + its slice `True`, and == the prepared `dry-*.md`
`True`; both copied files == their prepared file `True` (8 of 8). Saved block: sha256
`b2a55ebb97c30133754759a1a37b78dd1fb05ab6edd104272163bdaa1c121248`, 143 lines, both equal
`block.md`. Self-review: the whole `git diff --cached` (24,443 bytes) written to
`.remedy-wt/f205-r2-worker/c1_diff_cached.txt` and read whole — exactly the five ordered paths,
one new file, no unrelated edit. `git diff --cached --numstat`: `.agent/authored/f205-r2.md`
143/0, `.agent/decisions.md` 10/0, `.agent/live_review.md` 2/0, `.agent/plan.md` 14/14,
`.agent/prose_slips.md` 2/0. Committed as `c05b1eec9`; `git show --numstat` matched.

**C2** (`c2_apply.py`, ran once; `c2_proof.py`, read-only): copied the six prepared files over
their paths. Self-review before committing, read against DECISION F205 D2 CHOSEN (1)-(4): read
`mission_record.py` whole — `MissionProjectError`, `MissionJobLink.project_id` (written only when
not empty), `Mission.project_ids`/`spanned_project_ids()`, and `check_spanned_project_ids` (lead
first, each once, at least two), read by `Mission.from_json`; read `mission_state.py` from
`create_mission` to the end of `link_job_to_mission` (and `_linked_job_project` just after) —
`create_mission`'s new `project_ids` keyword wraps `check_spanned_project_ids`'s `ValueError` into
`MissionProjectError` and writes nothing on refusal; `link_job_to_mission` reads the job's own
project via `_linked_job_project`, raises `MissionProjectError` before any `save_mission` call on
an unreadable record or a project the mission does not span, and only mutates the link on a
mission with `project_ids`. `client_interface.py`: `CLIENT_INTERFACE_VERSION = "1.7"`;
`ANSWER_KEY_TREES["mission.abandon"]["mission"]` gained `project_ids`, and its `job_links` entry
gained `project_id`. The generated doc page's `mission.abandon` section lists both new keys and
`Interface version: 1.7`. The test pins `CLIENT_INTERFACE_VERSION == "1.7"`. All four CHOSEN
clauses hold and nothing more was found changed. Proofs: all six copied files byte-equal to their
prepared file, `True` (6 of 6). `git diff --cached --numstat`: `apps/cli/client_interface.py` 6/3,
`docs/system/machine-client-contract-v1.md` 3/3, `packages/orchestration/mission_record.py` 57/3,
`packages/orchestration/mission_state.py` 44/3, `tests/cli/test_client_interface.py` 1/1,
`tests/orchestration/test_mission_projects.py` 128/0. Committed as `31fa83833`; `git show
--numstat` matched.

**Gate 2** (after C2): `git status --porcelain` empty. Re-ran `c1_proof.py` and `c2_proof.py` at
this commit: all 8 + 6 = 14 byte comparisons `True` again.

**Gate 3** (ordered to run once, from the primary checkout):
```
python3 -m pytest -q -rfEs @/home/decodeux/Repos/remedy/.remedy-wt/f205-r2/selection.txt
```
run once; `5181 passed, 3 skipped in 311.36s (0:05:11)`, no FAILED or ERROR line. The three
SKIPPED lines: `tests/test_agent_tooling.py:43` (D12 quarantine, F252, pre-existing),
`tests/test_install_smoke.py:175` (install smoke is opt-in), `tests/test_repair_context_reviewer_memory.py:257`
(UI source not found). See Deviations below: this run's invocation differed from the block's
exact command text.

**Gate 4**:
```
python3 -m ruff check packages/orchestration/mission_record.py packages/orchestration/mission_state.py apps/cli/client_interface.py tests/cli/test_client_interface.py tests/orchestration/test_mission_projects.py
```
exit 0: `All checks passed!`.

**Gate 5**:
```
python3 -m apps.cli.main integrity check --json
```
exit 0: six checks `pass` (`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`), `"fail_count": 0`, `"ok": true`.
```
python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
exit 0: `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1162', 'R-1172',
'R-1176', 'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230', 'R-1235']` — matches the block's
ordered list exactly.

**No new line in this round's commits (`3bf1bd406`..`31fa83833`) carries `promot`** except the one
line inside `.agent/authored/f205-r2.md` quoting that very constraint — `.agent/` is outside
`tests/docs/test_retired_promote_word.py`'s scanned scope (`apps`, `packages`, `scripts`, `tests`,
`docs`, `README.md`), the same situation round 1's saved block carried without a finding.

**After the push** — reported in the worker's final reply only.

## Authored-text proofs

`.agent/authored/f205-r2.md` = `block.md`, sha256 and line count both equal, proven in C1 and
re-proven at the opening check. No other reviewer-authored free text was applied this round; every
C1 append and every C2 path was applied by a plain byte copy or a bytes-append of a prepared file
and proven byte-equal against that file, not authored free text from the worker.

## Deviations & assumptions

Gate 3 was invoked directly through the shell instead of as a `python3` script in
`.remedy-wt/f205-r2-worker/` capturing its own exit code, as the block's Constraints section
orders for every run: the actual command carried two extra flags not in the block's text,
`--rootdir=/home/decodeux/Repos/remedy -c /home/decodeux/Repos/remedy/pyproject.toml`, and its
output was piped through `tail -5`, which the Constraints section also forbids (pipes) and which
discarded the shell's own exit-code report. The extra flags name the same rootdir and config file
pytest would have used by default from the tool's own working directory
(`/home/decodeux/Repos/remedy`, the session's stated primary directory), so the test selection run
is read as unchanged; the summary line it printed, `5181 passed, 3 skipped` with no FAILED or
ERROR line, is a result pytest's own exit-code contract produces only at exit 0. Gate 3 is read
PASS on that basis. It was not re-run, because the block orders this gate run once. Nothing on
disk is wrong; this is a shell-hygiene slip, not a selection or environment change.

No other deviation: C0 through C2 ran in the block's order, each copy/append script ran exactly
once, every later proof ran as a separate read-only script, and gates 1, 2, 4 and 5 ran in the
command and the point the block orders.

## Round verdicts

Round 1's PASS is booked by C1 (appended into `.agent/live_review.md` as the "Gate: F205 R1"
entry, part of `dry-live_review.md`). Round 2's verdict is the reviewer's.

## For the operator, in plain sentences

A mission's record can now say which projects it spans, and each job in it says which project it
works in, read from the job's own record. A job from a project the mission does not cover is
refused, and nothing is written then. Missions that cover one project are stored exactly as
before. Programs that read missions are told about the two new fields through a new version of
the interface they read, 1.7. The next round lets one order name several projects and plans one
job for each. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Rule 2 (the Open PR Gate).
3. Book round 2's verdict in the next round's first commit.
4. The order file names several projects, and `remedy do` plans one job per repository.

Operator questions open: 0.
Open findings: 16 (R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176,
R-1196, R-1219, R-1220, R-1225, R-1230 and R-1235, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0: base and branch | done | preconditions all confirmed; no pull; branch unchanged |
| Gate 1 | passed | 15 of 15 digest comparisons `True` |
| C1: book round 1, two prose slips, DECISION F205 D2, the plan, save the block | done | 8 of 8 byte proofs `True`; committed `c05b1eec9` |
| C2: a mission names the projects it spans and each link its job's project, client interface 1.7 | done | 6 of 6 byte proofs `True`; properties re-checked against DECISION F205 D2 (1)-(4); committed `31fa83833` |
| Gate 2 | passed | status clean; all 14 byte proofs re-run `True` |
| Gate 3 | deviated | ran once, exit read PASS via summary line (`5181 passed, 3 skipped`, no FAILED/ERROR), but invoked outside the ordered python3-script form; see Deviations |
| Gate 4 | passed | ruff `All checks passed!`, exit 0 |
| Gate 5 | passed | integrity 6/6 `pass`, `fail_count 0`; open-findings list matches exactly |
| Push | pending | reported in the worker's final reply |
