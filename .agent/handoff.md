# Handoff — F300 round 1: claim F300, book F299 R9, land T001 (the structure measure and `remedy integrity structure`)

## Session

SESSION 1 of feature F300 · round 1 · rounds so far 1

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~20 % (claim and T001 · T002, T003 and T004 open) — Schätzung

## Range

Review of `b25d87a2436fefbdc9d6ce5df40c2ba8e6e39697`..HEAD (five commits on
`feature/f300-structure-ledger-size-ratchet`: C1, C2, C3 part 1, C3 part 2, and this handback, C4).

## Commits

### `369034108` F300 R1 C1: save the round 1 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f300-r1.md` | 248/0 | NEW FILE — byte copy of `block.md`; sha256 `b4fe4c8fd84f6f16e1667bcfeaf9731028a6884dc27a068036627a2b8541482f`, 248 lines |

### `c6207f2b5` F300 R1 C2: claim F300, book F299 R9, the claim's measurement, DECISION F300 D1, R-1160 to F300, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/context.md` | 13/14 | replaced with `dry-context.md`: F300's scope, do-not-touch, active assumptions |
| `.agent/decisions.md` | 10/0 | DECISION F300 D1 appended (`append-decisions.txt`'s bytes) |
| `.agent/f300_inventory.md` | 234/0 | NEW FILE — byte copy of `f300_inventory.md`: the claim's measurement at `b25d87a24` |
| `.agent/live_review.md` | 28/26 | re-headed at the F300 claim; R-1160's owner line inserted after its paragraph; F299 R9's gate entry appended |
| `.agent/plan.md` | 19/17 | replaced with `dry-plan.md`: round 1's goal and current step |
| `docs/roadmap/STATUS.md` | 1/1 | F300's line `[ ]` → `[~]` |
| `docs/roadmap/features/T2_F300.md` | 11/0 | replaced with `dry-T2_F300.md`: R-1160's Acceptance line and the DECISION F300 D1 amendment paragraph |

### `83fcd315a` F300 R1 C3 (part 1): the structure measure and its tests (T001, DECISION F300 D1)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/structure_measure.py` | 220/0 | NEW FILE — the measure module: `measure_repository`, `function_sizes`, `count_lines`, `measure_as_dict`, `render_measure` |
| `tests/orchestration/test_structure_measure.py` | 279/0 | NEW FILE — 23 tests across 8 classes (acceptance, strictly-above, names, count_lines, skipped/listed, subfolder scoping, not-a-git-repo, the handler, the way a user reaches it) |

Split from the single C3 commit the block describes because the combined diff measured 562
insertions, over the 500-insertion cap; see Deviations.

### `435be0819` F300 R1 C3 (part 2): remedy integrity structure, its catalog entry and exit code (T001, DECISION F300 D1)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog.py` | 20/0 | `integrity.structure` `CommandEntry` directly after `integrity.block` |
| `apps/cli/commands/integrity_cmd.py` | 41/0 | `_cmd_integrity_structure` handler and its `COMMAND_HANDLERS` key |
| `docs/guides/exit-codes.md` | 1/0 | `remedy integrity structure` row (exit code 4) after the table's last row |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | `packages.orchestration.structure_measure` line, in sorted place |

### This commit — F300 R1 C4: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

None. The push is ordered by the block AFTER this commit (the "THEN" section); its outcome is
reported in the worker's final reply, not in this file, because the handback is written and
committed once, before it. No `gh pr create` — the block explicitly orders "Do not open a pull
request." No `gh pr merge`, no new branch beyond the one C0 created, no stash entry touched, no
`git worktree add`/`remove` at any point this round.

## Verification

**Gate 1** (after C0, before C1): a Python script compared every line of `digests.txt` against
the file it names.
```
python3 -I .remedy-wt/f300-r1-worker/01_gate1_digests.py
```
Exit 0. All 12 comparisons `True`; `GATE1 ALL True: True`.

**Gate 2** (after C3, both parts): `git status --porcelain` empty; the C2 byte proofs re-run at
this commit.
```
git -C /home/decodeux/Repos/remedy status --porcelain
python3 -I .remedy-wt/f300-r1-worker/05_c2_proofs.py
```
Exit 0 both. Status: empty. All 7 copy proofs `True`; `decisions.md equals base+append: True`;
`ALL COPY PROOFS True: True`.

**Gate 3**, run once, through a Python wrapper (`subprocess.run`, `cwd=/home/decodeux/Repos/remedy`)
capturing the real exit code:
```
python3 -m pytest -q -rfEs @.remedy-wt/f300-r1/selection.txt
```
Exit **0**. `4841 passed, 3 skipped in 238.46s (0:03:58)`. No FAILED or ERROR line. SKIPPED
lines: `tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175`
(opt-in, needs network), `tests/test_repair_context_reviewer_memory.py:257` (UI source not found)
— the same three the reviewer's own `sim-run.txt` lists.

**Gate 4**:
```
python3 -m ruff check packages/orchestration/structure_measure.py apps/cli/commands/integrity_cmd.py apps/cli/command_catalog.py tests/orchestration/test_structure_measure.py
```
Exit **0**. `All checks passed!`

**Gate 5**:
```
python3 -B .remedy-wt/f300-r1/check_fixture.py .remedy-wt/f300-r1-worker/fixture
```
Exit **0**. Last line `ALL True`. Full output:
```
whole: exit 0
whole: exit and envelope True; root True; answer True
pkg: exit 0
pkg: exit and envelope True; root True; answer True
ALL True
```

**Gate 6**:
```
python3 -m apps.cli.main integrity check --json
```
Exit **0**. `"check_count": 6`, `"fail_count": 0`, `"ok": true`, `"passed": true`, all six checks
`"status": "pass"` (`handler_import`, `live_review_verdict` — "last Gate verdict PASS" —
`plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`).
```
python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
Exit **0**. Output, verbatim:
```
['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230']
```
Matches the block's ordered list exactly.

**After the push** (reported in the worker's final reply, not here): `git status --porcelain`
empty, `git stash list`, `git log --oneline -n 6`, and the local tip equal to
`origin/feature/f300-structure-ledger-size-ratchet`.

## Authored-text proofs

`.agent/authored/f300-r1.md` (saved block, C1) equals `block.md` byte for byte: sha256
`b4fe4c8fd84f6f16e1667bcfeaf9731028a6884dc27a068036627a2b8541482f`, 248 lines, both sides.
`docs/roadmap/STATUS.md`, `.agent/live_review.md`, `.agent/plan.md`, `.agent/context.md`,
`docs/roadmap/features/T2_F300.md` and `.agent/f300_inventory.md` (C2) each equal their prepared
`dry-*`/source file byte for byte, proved both at write time and again read-only after staging
(gate 2's re-run). `.agent/decisions.md` equals the blob at `b25d87a24` followed by
`append-decisions.txt`'s bytes exactly.

## Deviations & assumptions

- **C3 was split into two commits** — "part 1" (`packages/orchestration/structure_measure.py` and
  `tests/orchestration/test_structure_measure.py`, 499 insertions) and "part 2" (the CLI handler,
  the catalog entry, the exit-codes row and the allowlist line, 63 insertions) — instead of the
  single C3 commit the block's prose describes, because the combined diff measured 562 insertions,
  over the 500-insertion cap. The block itself authorizes exactly this split: "if yours would pass
  500, split it into (part 1) with the module and its tests and (part 2) with the rest, and say
  so." The reviewer's own dry run of the combined commit measured 418 insertions; this worker's
  test file is more thorough (23 tests across 8 classes) and pushed the total over the reviewer's
  figure. Part 1 alone is 499 insertions, one under the cap.
- Gate 5's fixture check (`check_fixture.py`) was run once as an early sanity check immediately
  after authoring the module, before C3's second commit existed, to confirm the module's behaviour
  against the reviewer's expected fixture before wiring the CLI, and again as the official gate 5
  after both C3 commits landed. Both runs read `ALL True`; neither wrote outside the worker's own
  scratch fixture folder; this is not the pytest selection gate 3 governs and is not forbidden, but
  is flagged for transparency.
- `ruff check` over the same four C3 files was likewise run once ahead of the official gate 4
  (immediately after authoring each file) and once as gate 4 itself; both runs read
  `All checks passed!` / exit 0.
- One shell command — a `cd ... && python3 -m ruff check ... && echo "EXIT:$?"` compound typed to
  fold gate 4's exit-code check into one line — was refused by the sandbox before it ran; no git
  state, no file and no test outcome was touched by it. Gate 4 was then run correctly, as a single
  command inside a Python script.
- No other deviation: C0, C1, C2 and gates 1, 2, 3, 6 ran exactly as the block ordered, each
  exactly once, in the block's sequence; no file outside each commit's named paths was touched;
  gate 3's pytest selection was the round's only test run, with no `-n` and no
  `REMEDY_TEST_MAX_WORKERS`, run once; no mutation, no worktree add/remove, nothing merged; no
  pull request was opened; `.agent/STOP` did not appear at any point.

## Round verdicts

F299's round 9 PASS is booked by C2, into `.agent/live_review.md`'s re-headed ledger. Round 1's
verdict is the reviewer's.

## For the operator, in plain sentences

The feature that checks a project other than Remedy itself is merged into the main line after both
of GitHub's checks passed. The new feature gives Remedy a measure of how large its code has grown.
Remedy now has a command that lists every Python function longer than 100 lines and every file
longer than 1,000 lines in any project it is pointed at, and changes nothing while doing so.
Measured on Remedy itself today, 162 functions and 40 files in its program code are above those
limits, and the largest function, the one that runs a job, has grown from 1,522 to 1,665 lines
since the feature was planned two days ago. The next round writes those sizes down and adds a test
that lets them shrink and never grow. One known problem, that pausing a job while one of its tasks
is being saved ends the job as if its budget ran out, moved to this feature, because its last step
rewrites exactly that place. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Phase 1 rule 2 (the Open PR Gate).
3. Book round 1's verdict in the next round's first commit.
4. T002 and T003: the ledger page, the ratchet test with its record of sizes, and the paydown
   rule.

Operator questions open: 0.
Open findings: 16 (R-1160, Medium, owned by F300; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157,
R-1158, R-1162, R-1172, R-1176, R-1196, R-1219, R-1220, R-1225 and R-1230, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0: base and branch | done | preconditions verified, branch created |
| Gate 1 | passed | all 12 digests `True` |
| C1: save the round 1 block | done | sha256/line count equal; committed `369034108` |
| C2: claim F300, book F299 R9, the measurement, DECISION F300 D1, R-1160, the plan | done | all byte proofs `True`; committed `c6207f2b5` |
| C3: the structure measure and `remedy integrity structure` | done, deviated | split into part 1 (`83fcd315a`) and part 2 (`435be0819`) — declared above |
| Gate 2 | passed | status clean; all 7 byte proofs `True` |
| Gate 3 | passed | 4841 passed, exit 0, no FAILED/ERROR |
| Gate 4 | passed | ruff exit 0, all checks passed |
| Gate 5 | passed | fixture check exit 0, `ALL True` |
| Gate 6 | passed | six integrity checks pass, fail_count 0; open findings match the block's list |
| C4: handback | done | this commit |
| Push | pending | reported in the worker's final reply, after this commit |
