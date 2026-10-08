# Handoff — F304 session 2, round 6: T004's first part, a second start of one order file is refused, naming its running mission (DECISION F304 D6)

## Session

SESSION 2 of feature F304 · round 6 · rounds so far 6

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~40 % (T002 and T003 done · T004 half done · T005 to T007 open) — Schätzung

## Range

Review of `9cf860628217c9fdba91f02c9eaabbd1752c76b9`..HEAD (HEAD is C3 below, which carries this handback).

## Commits

### 491e960f7 F304 R6 C1: book round 5, DECISION F304 D6, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f304-r6.md` | 118/0 (new) | byte copy of `block.md` (118 lines, sha256 `8cff79ee577db173ea6828ed3016bf4754074a0e058cac1173ab754b96c5e5e6`) |
| `.agent/decisions.md` | 10/0 | its bytes at `9cf860628` followed by `append-decisions.txt` (DECISION F304 D6) |
| `.agent/live_review.md` | 2/0 | its bytes at `9cf860628` followed by `append-live_review.txt` (round 5's gate entry) |
| `.agent/plan.md` | 7/6 | `dry-plan.md`, byte for byte |

### 04910e9b8 F304 R6 C2: a second start of one order file is refused before any step, naming the running mission (T004, DECISION F304 D6)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/client_interface.py` | 3/3 | `do.run`'s `OPERATION_REFUSAL_TOKENS` gains `order_already_running` |
| `apps/cli/command_catalog.py` | 1/0 | `--new-mission` joins `do.run`'s `ArgDef` list |
| `apps/cli/commands/do_cmd.py` | 17/1 | `_cmd_do` refuses an order file a running mission already records, before any step, with `order_already_running`, exit 2 and `mission_id`; the `new_mission` parameter and its `COMMAND_HANDLERS` wiring |
| `docs/system/machine-client-contract-v1.md` | 7/3 | the order-file section's new sentence, the `--new-mission` row and the refusal-tokens line; generated section written again |
| `packages/orchestration/mission_state.py` | 23/0 | `MISSION_ENDED_STATUSES` and `running_mission_for_order_file`, scanning every project for the newest mission still running for a given order file |
| `tests/cli/test_do_order_file.py` | 61/1 | the refusal and its mission id, `--new-mission` starting a second mission, a restart after an abandon, another order file beside a running mission; the earlier `--contract` test now passes `--new-mission` on its second start |
| `tests/orchestration/test_mission_state.py` | 29/0 | `TestRunningMissionForOrderFile`: the newest running mission across projects, an ended mission not running, and an empty path matching no text order |

## External actions

- None before this file is committed. The push of the branch and its outcome (every attempt) are in the worker's final reply (write-once rule; not known when this file is written).
- No `gh` command, no full suite, no mutation, no worktree, no merge, no new branch, no force-push, no pull.

## Verification

0. Before any write: `block.md` (118 lines), `sim-readings.txt` and `digests.txt` matched the prompt's sha256 digests (Python `hashlib.sha256`, 3 of 3 True), and the ten other prepared files listed in `digests.txt` matched it (10 of 10 True). `git rev-parse HEAD` and `origin/feature/f304-machine-client-contract-v1-1-part-two` both read `9cf860628217c9fdba91f02c9eaabbd1752c76b9`, `git status --porcelain` was empty, `.agent/STOP` was absent. `git branch --show-current` read the feature branch before each commit (checked inside each commit script).
1. C1 proofs: the authored copy is 118 lines, sha256 `8cff79ee577db173ea6828ed3016bf4754074a0e058cac1173ab754b96c5e5e6`, byte-equal to its source. `.agent/live_review.md` and `.agent/decisions.md` each equal `git show 9cf860628:<path>` plus their append file, True (the decisions proof by sha256/byte comparison of the built bytes against the file on disk, the file itself never read whole). `.agent/plan.md` equals `dry-plan.md`, True. `git diff --cached --numstat` read `118 0`, `10 0`, `2 0`, `7 6`, the cells of `sim-readings.txt`. The staged diff (184 lines) was written to a file and read whole.
2. C2 proofs: the seven files equal their prepared files, True seven of seven, each sha256-verified. `git diff --cached --numstat` read `3 3`, `1 0`, `17 1`, `7 3`, `23 0`, `61 1`, `29 0`, the cells of `sim-readings.txt`. `git status --porcelain` showed exactly the seven C2 paths staged, nothing else. The staged diff (270 lines) was written to a file and read whole.
3. **Gate 1** (`git -C /home/decodeux/Repos/remedy status --porcelain`, after C2): exit 0, empty; the byte proofs of C1 and C2 above all True.
4. **Gate 2** (`python3 -m ruff check` on the six named files): exit 0, `All checks passed!`.
5. **Gate 3** (`python3 -m pytest -q -rfEs` on the block's selection, run once, through a Python wrapper capturing the exit code): exit 0, last line `1866 passed in 348.14s (0:05:48)`; the full transcript was scanned for FAILED, ERROR and SKIPPED lines, none found.
6. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`, all six `pass`, `"fail_count": 0`; then `open_finding_ids`: exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176']`.
7. **Gate 5** (after the push): reported in the worker's final reply.

## Authored-text proofs

- `block.md` to `.agent/authored/f304-r6.md`: 118 lines, byte-equal, sha256 `8cff79ee577db173ea6828ed3016bf4754074a0e058cac1173ab754b96c5e5e6`.
- `append-live_review.txt` and `append-decisions.txt`: post equals pre plus slice in bytes, once each (Verification item 1 above).
- `dry-plan.md` to `.agent/plan.md`, and the seven C2 files to their targets: byte-equal (Verification items 1 and 2 above).

## Deviations & assumptions

None.

## Round verdicts

Round 5's PASS is booked by C1.

Round 6's verdict is the reviewer's.

## For the operator, in plain sentences

Until now, starting the same order file twice quietly started a second piece of work beside the first. From now on Remedy refuses the second start before it does anything, says which piece of work already runs that order file, and ends with exit code 2. A program can still ask for a second one on purpose with `--new-mission`. An order file whose earlier work was given up starts normally again. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and stop.
2. Then Phase 1 rule 2, the Open PR Gate.
3. Then book round 6's verdict in the next round's first commit.
4. Then T004's second part: the second gate test.

Operator questions open: 1.
Open findings: 11 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172 and R-1176, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 5, DECISION F304 D6, the plan and the block | done | `491e960f7` |
| C2: a second start of one order file is refused before any step, naming the running mission | done | `04910e9b8` |
| Gates 1 to 4 | done | all green, before this file was written |
| C3: handback | done | this commit |
| Push, gate 5 | pending at write time | outcomes in the worker's final reply |
