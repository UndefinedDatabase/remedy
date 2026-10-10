# Handback — F301 round 7: book round 6, R-1233 and R-1234, DECISION F301 D5; then T005: upkeep_preview, the digest's upkeep counts, client interface 1.6, and `remedy mission show`

## Session

SESSION 1 of feature F301 · round 7 · rounds so far 7

Context self-assessment: the reviewer's context still serves; the session takes one more round,
the acceptance fixture, and then ends so that the closure starts fresh.

Fortschritt: ~85 % (claim, T001 to T005, the structural steps · the six-job fixture and closure
open) — Schätzung

## Range

Review of `4752f7812`..HEAD (five commits on `feature/f301-mission-upkeep` — C1, C2, C3, C4, and
this handback, C5).

## Commits

### `958844f44` F301 R7 C1: save the round 7 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f301-r7.md` | 153/0 | NEW FILE — byte copy of `block.md`; sha256 `5f556031e3c682e9cab95532d45e780d127ecf2bb8868a8cc92f91c00d8d0202`, 153 lines, equal to `block.md`'s own |

### `22e0c6152` F301 R7 C2: book round 6, resolve R-1233 and R-1234, DECISION F301 D5, the plan, a prose slip

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | 10/0 | base blob at `4752f7812` + `append-decisions.txt`'s bytes: DECISION F301 D5 appended — `upkeep_preview`, `upkeep_digest_counts`, the three `_mission_entry` keys, and `CLIENT_INTERFACE_VERSION` rising to `1.6` |
| `.agent/live_review.md` | 6/0 | base blob at `4752f7812` + `append-live_review.txt`'s bytes: round 6's Gate entry, VERDICT PASS, and the resolutions of R-1233 and R-1234 booked |
| `.agent/plan.md` | 9/9 | replaced with `dry-plan.md`: round 7's current step and the T005/fixture/closure next steps |
| `.agent/prose_slips.md` | 1/0 | base blob at `4752f7812` + `append-prose_slips.txt`'s bytes: one prose-slip line appended |

### `004dd6a30` F301 R7 C3: the upkeep preview and the digest's upkeep counts, client interface 1.6 (T005, DECISION F301 D5)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/client_interface.py` | 6/2 | `CLIENT_INTERFACE_VERSION` raised `"1.5"` → `"1.6"`; the `missions` tree gains `upkeep_every`, `upkeep_jobs_left`, `upkeep_open_findings` |
| `docs/system/machine-client-contract-v1.md` | 4/4 | regenerated: interface version `1.6`; all three rendered lists of a mission's keys gain the upkeep keys |
| `packages/orchestration/client_digest.py` | 11/1 | `_mission_entry` gains the three upkeep keys as literals, read from `upkeep_digest_counts` |
| `packages/orchestration/mission_upkeep.py` | 65/17 | `record_closed_jobs` refactored onto a new shared `_closed_bodies` helper; `upkeep_preview` added (reads the ledger plus the in-memory lines the mission's ended jobs would get, writes nothing, raises `UpkeepError` on a bad setting); `upkeep_digest_counts` added (never raises, never reads the repository, answers `None`s on failure) |
| `tests/cli/test_client_interface.py` | 1/1 | asserts `CLIENT_INTERFACE_VERSION == "1.6"` |
| `tests/cli/test_status_cmd.py` | 9/0 | `test_the_digest_names_the_jobs_left_until_the_next_upkeep_job` |
| `tests/orchestration/test_mission_upkeep.py` | 65/0 | `TestThePreview` and `TestTheDigestCounts` added |

### `b3e225e6d` F301 R7 C4: remedy mission show says when the upkeep job comes and what it carries (T005, DECISION F301 D5)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/mission_cmd.py` | 44/1 | `_upkeep_preview_or_error` and `_print_upkeep_preview` added; `_cmd_mission_show` computes the preview for a mission with at least one job (`None` for a mission with none), prints the upkeep section, and adds `upkeep` to the `--json` answer; a bad setting is shown in the printed text and the `--json` `error` key, the command still exiting 0 |
| `docs/system/mission-upkeep-v1.md` | 14/3 | new "What a person and a client see" section naming both the `remedy mission show` view and the digest's three counts; status banner updated to DECISIONs F301 D1–D5 and the new built-so-far line |
| `tests/cli/test_mission_cmd.py` | 40/0 | three new tests in `TestContinueWithUpkeep`: `test_show_says_when_the_upkeep_job_comes_and_what_it_carries`, `test_show_counts_down_and_says_nothing_for_a_mission_without_jobs`, `test_show_names_a_bad_setting_and_still_shows_the_mission` |

### This commit — F301 R7 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

None yet. The block's one push happens AFTER this commit (the "THEN" step), reported in the
worker's final reply after this commit. No pull request is opened this round.

## Verification

**Gate 1** (after C0, before C1): `python3 /home/decodeux/Repos/remedy/.remedy-wt/f301-r7-worker/gate1_check_digests.py`
— sha256 and line-count check of every file `digests.txt` names in `.remedy-wt/f301-r7/`. All 19
files' hash and line-count checks `True`; `ALL_TRUE: True`.

**Gate 2** (after C4): `git -C /home/decodeux/Repos/remedy status --porcelain` read empty. Re-ran,
via `python3 /home/decodeux/Repos/remedy/.remedy-wt/f301-r7-worker/c2_proof.py`,
`c3_copy_and_proof.py` and `c4_copy_and_proof.py`, the C2 step 2 proofs (3 blob-at-`4752f7812`-plus-
append proofs + 4 copy-equal checks), the C3 byte proofs (7 of 7) and the C4 byte proofs (3 of 3),
all at this commit's own HEAD. All `True`; `ALL_TRUE: True` in each script. `git status --porcelain`
read empty again after the re-run.

**Gate 3** (the round's one test selection, run once, after C4):
```
python3 -m pytest -q -rfEs @/home/decodeux/Repos/remedy/.remedy-wt/f301-r7/selection.txt
```
Exit code 0. Summary line: `7175 passed, 4 skipped in 508.84s (0:08:28)`. No `FAILED` or `ERROR`
line anywhere. SKIPPED lines, verbatim:
```
SKIPPED [1] tests/regression/test_f293_acceptance.py:191: main holds F293, so its own changes are history
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
```
This full selection run includes `tests/docs/` (line 20 of `selection.txt`), so the retired-word
guard `tests/docs/test_retired_promote_word.py` ran clean over every file this round touched.

**Gate 4**:
```
python3 -m ruff check packages/orchestration/mission_upkeep.py packages/orchestration/client_digest.py apps/cli/client_interface.py apps/cli/commands/mission_cmd.py tests/orchestration/test_mission_upkeep.py tests/cli/test_client_interface.py tests/cli/test_status_cmd.py tests/cli/test_mission_cmd.py
```
Exit 0. Output: `All checks passed!`

**Gate 5**:
```
python3 -m apps.cli.main integrity check --json
```
Exit 0. `{"check_count": 6, ..., "fail_count": 0, "ok": true, "passed": true, ...}` — all six checks
`status: pass` (`handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`repo_root_hygiene`, `high_blockers_open`).
```
python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
Exit 0. Output, verbatim:
```
['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1162', 'R-1172', 'R-1176', 'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230']
```
Matches the block's ordered list exactly.

**THEN (the push)**: after this commit, reported in the worker's final reply.

## Authored-text proofs

`.agent/authored/f301-r7.md` (C1) equals `block.md` byte for byte: sha256
`5f556031e3c682e9cab95532d45e780d127ecf2bb8868a8cc92f91c00d8d0202`, 153 lines, checked at write
time (C1) and not among gate 2's re-run proofs (the block names only C2 step 2, C3 step 3 and C4
step 3 for the re-run).

## Deviations & assumptions

- Three one-off checks ran as inline `python3 -c "..."` commands rather than as script files saved
  under `.remedy-wt/f301-r7-worker/`: the block.md sha256 pre-check done before reading AGENTS.md
  (required "before anything else" by the governing instructions), the `os.makedirs` creation of
  `.remedy-wt/f301-r7-worker/` together with a second sha256 re-check and a directory listing, and
  the `.agent/STOP`-absence check in C0. None of the three wrote, copied or compared a tracked file
  — each only read `block.md`, created an empty directory, or checked for an absent file — and every
  result each printed is shown verbatim earlier in this round's transcript and in the worker's final
  reply. Declared because the constraint "every script lives under
  `/home/decodeux/Repos/remedy/.remedy-wt/f301-r7-worker/`" names scripts generally, and these three
  snippets, though each is a single Python invocation rather than a saved `.py` file, fall under
  that wording on a strict reading. Every script from C1 onward (`gate1_check_digests.py`,
  `c1_copy_block.py`, `c1_msg.py`, `c2_copy.py`, `c2_proof.py`, `c2_msg.py`, `c3_copy_and_proof.py`,
  `c3_msg.py`, `c4_copy_and_proof.py`, `c4_msg.py`, `gate3_pytest.py`, `gate4_ruff.py`,
  `gate5_integrity_and_findings.py`) was saved under `.remedy-wt/f301-r7-worker/` and run from there
  with absolute paths to `/home/decodeux/Repos/remedy`, as the block requires.

Otherwise: None. C0 through C4 ran exactly as the block ordered, each exactly once, in the block's
sequence; `git branch --show-current` was the literal call immediately before each of the four
`git commit` calls, with nothing between; every copy and byte-equality proof the block names was a
Python file operation inside a saved script (`c1_copy_block.py`, `c2_copy.py`, `c2_proof.py`,
`c3_copy_and_proof.py`, `c4_copy_and_proof.py`), and every other command a script ran
(`git show`, `pytest`, `ruff`, the integrity check, the open-finding-ids check) went through
`subprocess.run` with its own exit code printed; every git command outside a script was its own
single `git -C /home/decodeux/Repos/remedy ...` call; no file outside the round's named paths was
touched; no `REMEDY_TEST_MAX_WORKERS` was set and no `-n` was passed; no mutation, no full suite
(one selection run, once, after C4); no worktree created or removed, no stash entry touched, no
branch created, nothing merged, no force-push; `.agent/STOP` did not appear at any point; commit
subjects carry no leading-slash token and no absolute path; this round introduced no new line
under `packages/`, `apps/`, `tests/` or `docs/` that carries the retired word
`tests/docs/test_retired_promote_word.py` guards, confirmed by gate 3's full pass of `tests/docs/`,
which includes that guard's own test.

## Round verdicts

F301 round 6's PASS verdict is booked by C2 — the `dry-live_review.md` bytes, proved equal to the
base blob at `4752f7812` plus `append-live_review.txt`'s bytes, now carry round 6's Gate entry
forward in `.agent/live_review.md`, together with the resolutions of R-1233 and R-1234. Round 7's
verdict is the reviewer's, to be booked in the next round's first commit.

## For the operator, in plain sentences

`remedy mission show` now says how many more finished jobs come before the next cleanup job, or
that it is due now, and what it would take on. The status that a program reads from Remedy, and
the same answer the web interface gives, now carry three numbers per mission: after how many
finished jobs a cleanup job comes, how many are left, and how many problems are waiting for it.
Showing these never changes anything, and it never reads through the project's whole code. The two
gaps written down earlier in this feature are closed. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Phase 1 rule 2 (the Open PR Gate).
3. Book round 7's verdict in the next round's first commit.
4. The acceptance fixture of six jobs and the Built State, then the closure.

Operator questions open: 0.
Open findings: 15 (R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176,
R-1196, R-1219, R-1220, R-1225 and R-1230, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0: base and branch preconditions | done | branch `feature/f301-mission-upkeep`, HEAD = origin = `4752f7812e8cb722ee071431ae860df82448fde5`, `status --porcelain` empty, `.agent/STOP` absent |
| Gate 1 | passed | all 19 digests `True` (hash and line count) |
| C1: save the round 7 block | done | sha256/line count equal to `block.md`; committed `958844f44` |
| C2: book round 6, resolve R-1233 and R-1234, DECISION F301 D5, the plan, a prose slip | done | all 7 byte proofs `True` (3 blob+append, 4 copy-equal); 26 insertions; committed `22e0c6152` |
| C3: the upkeep preview and the digest's upkeep counts, client interface 1.6 | done | self-review checks held (`_closed_bodies` shared, `upkeep_preview` writes nothing, `upkeep_digest_counts` never raises/never reads the repo, literal `_mission_entry` keys, interface tree + version 1.6, three contract-page mission-key lists, `TestThePreview`/`TestTheDigestCounts`/the new status test); 161 insertions; all 7 byte proofs `True`; committed `004dd6a30` |
| C4: remedy mission show says when the upkeep job comes and what it carries | done | self-review checks held (upkeep section + `upkeep` key for a mission with a job, none for a mission without one, a bad setting shown with exit 0, three `TestContinueWithUpkeep` tests, the page); 98 insertions; all 3 byte proofs `True`; committed `b3e225e6d` |
| Gate 2 | passed | status clean; all re-run byte proofs `True` |
| Gate 3 | passed | `7175 passed, 4 skipped in 508.84s`, exit 0, no FAILED/ERROR |
| Gate 4 | passed | ruff exit 0, `All checks passed!` |
| Gate 5 | passed | integrity six checks pass, fail_count 0; open findings match the block's list exactly |
| C5: handback | done | this commit |
| Push | pending | reported in the worker's final reply, after this commit |
