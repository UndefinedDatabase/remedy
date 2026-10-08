# Handoff — F304 session 1, round 3: R-1183's repair, then T002's second part, `remedy project register` (DECISION F304 D3)

## Session

SESSION 1 of feature F304 · round 3 · rounds so far 3

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~18 % (T002 done · T003 to T007 open) — Schätzung

## Range

Review of `15dcffc1b8eb4e30ae0c197b19469d1368c93b4e`..HEAD (HEAD is C4 below, which carries this handback).

## Commits

### b99301d48 F304 R3 C1: book round 2, register R-1183, DECISION F304 D3, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f304-r3.md` | 133/0 (new) | byte copy of `block.md` (133 lines, sha256 `afd060c16dfff646192d15cdb75d9052cbc9bff412d645390db5b718c9f71b2a`) |
| `.agent/decisions.md` | 10/0 | its bytes at `15dcffc1b` followed by `append-decisions.txt` (DECISION F304 D3) |
| `.agent/live_review.md` | 4/0 | its bytes at `15dcffc1b` followed by `append-live_review.txt` (round 2's gate entry, R-1183) |
| `.agent/plan.md` | 9/10 | `dry-plan.md`, byte for byte |

### 0729d19da F304 R3 C2: an order whose project has no repository is refused with exit 3 (R-1183)

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/0 | its bytes at C1 followed by `append-landed.txt` (R-1183 landed) |
| `apps/cli/command_catalog.py` | 3/0 | `do.run` declares `exit_codes=(0, 1, 2, 3)` |
| `apps/cli/commands/do_cmd.py` | 5/4 | `project_has_no_repo` exits 3; docstring names both codes |
| `docs/guides/exit-codes.md` | 1/0 | `remedy do run` lists 3 |
| `docs/system/machine-client-contract-v1.md` | 5/5 | order-file section names exit 3 and exit 2; generated section written again |
| `tests/cli/test_do_project_repo.py` | 4/4 | `_refused` takes the expected code: 3 for `project_has_no_repo`, 2 for `repo_not_in_project` |

### 5c65e63d5 F304 R3 C3: remedy project register registers a repository for a client and leaves its working copy clean (T002, DECISION F304 D3)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/client_interface.py` | 4/0 | `project.register` joins the operations first, with its token, answer keys and an empty answer tree |
| `apps/cli/command_catalog.py` | 14/0 | the `project.register` entry, exit codes 0, 1, 2, 4 |
| `apps/cli/commands/project.py` | 39/0 | `_cmd_project_register` and its handler entry |
| `docs/guides/exit-codes.md` | 1/0 | `remedy project register` lists 4 |
| `docs/system/machine-client-contract-v1.md` | 19/1 | order-file section names the command; generated section written again |
| `tests/cli/test_client_interface.py` | 1/0 | the real-run test calls `project.register` once |
| `tests/cli/test_project_register.py` | 102/0 (new) | clean working copy, twice answers the same project, an order runs in the registered repository, a path that is no repository |

### C4 F304 R3 C4: handback

C4's hash is not known when this file is written (a handoff cannot table the commit that writes it).

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten per `docs/agents/handback_template.md` |

## External actions

- None before this file is committed. The push of the branch and its outcome (every attempt) are in the worker's final reply (write-once rule; not known when this file is written).
- No `gh` command, no full suite, no mutation, no worktree, no merge, no new branch, no force-push, no pull.

## Verification

0. Before any write: `block.md` (133 lines), `sim-readings.txt` and `digests.txt` matched the prompt's sha256 digests, and the sixteen other prepared files matched `digests.txt` (Python `hashlib.sha256`, 19 of 19 True). `git rev-parse HEAD` and `origin/feature/f304-machine-client-contract-v1-1-part-two` both read `15dcffc1b8eb4e30ae0c197b19469d1368c93b4e`, `git status --porcelain` was empty, `.agent/STOP` was absent. `git branch --show-current` read the feature branch before each commit (checked inside the commit script).
1. C1 proofs: `.agent/decisions.md` and `.agent/live_review.md` each equal `git show 15dcffc1b:<path>` plus the append file, True; `.agent/plan.md` equals `dry-plan.md`, True; the block copy is 133 lines, sha256 as above. `git diff --cached --numstat` read `133 0`, `10 0`, `4 0`, `9 10`, the cells of `sim-readings.txt`. The staged diff was written to a file and read whole.
2. C2 proofs: the five files equal their prepared files, True five of five; `.agent/live_review.md` equals its bytes at C1 plus `append-landed.txt`, True. `git diff --cached --numstat` read `2 0`, `3 0`, `5 4`, `1 0`, `5 5`, `4 4`, the cells of `sim-readings.txt`. The staged diff was written to a file and read whole.
3. C3 proofs: the seven files equal their prepared files, True seven of seven. `git diff --cached --numstat` read `4 0`, `14 0`, `39 0`, `1 0`, `19 1`, `1 0`, `102 0`, the cells of `sim-readings.txt`. The staged diff was written to a file and read whole.
4. **Gate 1** (`git -C /home/decodeux/Repos/remedy status --porcelain`, after C3): exit 0, empty; the byte proofs above all True.
5. **Gate 2** (`python3 -m ruff check` on the seven files): exit 0, `All checks passed!`.
6. **Gate 3** (`python3 -m pytest -q -rfEs` on the block's selection, run once, through a Python wrapper): exit 0, last line `1514 passed in 255.04s (0:04:15)`; no FAILED, ERROR or SKIPPED line.
7. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`, all six `pass`, `"fail_count": 0`.
8. **Gate 5** (`open_finding_ids`): exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1183']`.
9. **Gate 6** (after the push): reported in the worker's final reply.

## Authored-text proofs

- `block.md` to `.agent/authored/f304-r3.md`: 133 lines, byte-equal, sha256 `afd060c16dfff646192d15cdb75d9052cbc9bff412d645390db5b718c9f71b2a`.
- `append-decisions.txt`, `append-live_review.txt` and `append-landed.txt`: post equals pre plus slice in bytes, once each (items 1 and 2 above).
- `dry-plan.md` to `.agent/plan.md`, the five C2 files and the seven C3 files to their targets: byte-equal.

## Deviations & assumptions

None. (Gates ran one script at a time, after C3 and before C4, as ordered; gate 1's status read was taken after C3 was committed, its byte proofs before.)

## Round verdicts

Round 2's PASS is booked by C1. Round 3's verdict is the reviewer's, booked in the next round's first commit.

## For the operator, in plain sentences

A program can now register a project's folder with Remedy in one command, `remedy project register`, from wherever it stands. Unlike `remedy init`, this command leaves no new file in that folder. Asking twice answers the same project. The description Remedy gives a program lists this command first, because a program registers before it sends an order. The reviewer found a small slip of its own from the round before: a refusal that answered with the code meaning "you typed the command wrong" where it should say "what you named is not ready"; this round corrected it. This finishes the first of the six open parts. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and stop.
2. Then Phase 1 rule 2, the Open PR Gate.
3. Then book round 3's verdict and R-1183's resolution in the next round's first commit.
4. Then T003: honest refusals under `--approve --json`, and a command that declines a result.

Operator questions open: 1.
Open findings: 12 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172 and R-1176, Low, owned by F297; R-1183, Low, owned by F304, landed).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 2, register R-1183, DECISION F304 D3, the plan and the block | done | `b99301d48` |
| C2: an order whose project has no repository is refused with exit 3 | done | `0729d19da` |
| C3: remedy project register | done | `5c65e63d5` |
| C4: handback | done | this commit |
| Gates 1 to 5 | done | all green, before this file was written |
| Push, gate 6 | pending at write time | outcomes in the worker's final reply |
