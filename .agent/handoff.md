# Handoff — F304 session 1, round 2: T002's first part, an order that names a project runs in that project's registered repository (DECISION F304 D2)

## Session

SESSION 1 of feature F304 · round 2 · rounds so far 2

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~10 % (T002's first part · T002's second part and T003 to T007 open) — Schätzung

## Range

Review of `cdf31a5cfc710b861af505dffdfc9e9e35431bc2`..HEAD (HEAD is C3 below, which carries this handback).

## Commits

### 228f06835 F304 R2 C1: book round 1, DECISION F304 D2, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f304-r2.md` | 120/0 (new) | byte copy of `block.md` (120 lines, sha256 `556e988fedaa625649bf0fa5380659a606351c539128efb222b582694e3cfaca`) |
| `.agent/decisions.md` | 10/0 | its bytes at `cdf31a5cf` followed by `append-decisions.txt` (DECISION F304 D2) |
| `.agent/live_review.md` | 2/0 | its bytes at `cdf31a5cf` followed by `append-live_review.txt` (F304 round 1's gate entry) |
| `.agent/plan.md` | 7/7 | `dry-plan.md`, byte for byte |

### 902b5064b F304 R2 C2: an order that names a project runs in its registered repository (T002, DECISION F304 D2)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/client_interface.py` | 2/1 | `project_has_no_repo` and `repo_not_in_project` join the `do.run` refusal tokens |
| `apps/cli/command_catalog.py` | 1/1 | `do.run`'s `--repo` defaults to nothing; its help names the new default |
| `apps/cli/commands/do_cmd.py` | 52/2 | `_order_repo` and its call before the commit and push refusals; the handler passes `--repo` as given |
| `docs/system/machine-client-contract-v1.md` | 9/4 | order-file section states the rule and the two refusals; generated section written again |
| `tests/cli/test_do_flags.py` | 3/2 | the pin reads the named project's repository |
| `tests/cli/test_do_project_repo.py` | 174/0 (new) | an order in `a`, in no repository, with `--repo` naming `b` and `a`, and a project without a repository |

### C3 F304 R2 C3: handback

C3's hash is not known when this file is written (a handoff cannot table the commit that writes it).

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten per `docs/agents/handback_template.md` |

## External actions

- None before this file is committed. The push of the branch and its outcome (every attempt) are in the worker's final reply (write-once rule; not known when this file is written).
- No `gh` command, no full suite, no mutation, no worktree, no merge, no new branch, no force-push, no pull.

## Verification

0. Before any write: `block.md` (120 lines), `sim-readings.txt` and `digests.txt` matched the prompt's sha256 digests, and the nine other prepared files matched `digests.txt` (Python `hashlib.sha256`). `git rev-parse HEAD` and `origin/feature/f304-machine-client-contract-v1-1-part-two` both read `cdf31a5cfc710b861af505dffdfc9e9e35431bc2`, `git status --porcelain` was empty, `.agent/STOP` was absent. `git branch --show-current` read the feature branch before each commit (checked inside the commit script).
1. C1 proofs: `.agent/decisions.md` and `.agent/live_review.md` each equal `git show cdf31a5cf:<path>` plus the append file, True; `.agent/plan.md` equals `dry-plan.md`, True; the block copy is 120 lines, sha256 as above. `git diff --cached --numstat` read `120 0`, `10 0`, `2 0`, `7 7`, the cells of `sim-readings.txt`. The staged diff was written to a file and read whole.
2. C2 proofs: the six files equal their prepared files, True six of six. `git diff --cached --numstat` read `2 1`, `1 1`, `52 2`, `9 4`, `3 2`, `174 0`, the cells of `sim-readings.txt`. The staged diff was written to a file and read whole.
3. **Gate 1** (`git -C /home/decodeux/Repos/remedy status --porcelain`, after C2): exit 0, empty; the byte proofs above all True.
4. **Gate 2** (`python3 -m ruff check` on the five files): exit 0, `All checks passed!`.
5. **Gate 3** (`python3 -m pytest -q -rfEs` on the block's selection, run once, through a Python wrapper): exit 0, last line `1189 passed in 231.27s (0:03:51)`; no FAILED, ERROR or SKIPPED line.
6. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`, all six `pass`, `"fail_count": 0`.
7. **Gate 5** (`open_finding_ids`): exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176']`.
8. **Gate 6** (after the push): reported in the worker's final reply.

## Authored-text proofs

- `block.md` to `.agent/authored/f304-r2.md`: 120 lines, byte-equal, sha256 `556e988fedaa625649bf0fa5380659a606351c539128efb222b582694e3cfaca`.
- `append-decisions.txt` and `append-live_review.txt`: post equals pre plus slice in bytes, once each (item 1 above).
- `dry-plan.md` to `.agent/plan.md`, and the six C2 files to their targets: byte-equal.

## Deviations & assumptions

None. (Gates ran one script at a time, after C2 and before C3, as ordered; gate 1's status read was taken after C2 was committed, its byte proofs before.)

## Round verdicts

Round 1's PASS is booked by C1. Round 2's verdict is the reviewer's, booked in the next round's first commit.

## For the operator, in plain sentences

An order that names a project now runs in that project's own folder, wherever the program that sends it stands. Before, it ran in the folder the program stood in and only filed its records under the named project. An order naming a project with no folder, or naming a folder that does not belong to that project, is now refused before anything starts, with a clear word a program can read and a sentence saying how to fix it. The description Remedy gives a program, and the page a person reads, say so. The next round adds one command that registers a folder for a program and leaves that folder's files untouched. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and stop.
2. Then Phase 1 rule 2, the Open PR Gate.
3. Then book round 2's verdict in the next round's first commit.
4. Then T002's second part: one command registers a repository for a client and leaves its working copy clean.

Operator questions open: 1.
Open findings: 11 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172 and R-1176, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 1, DECISION F304 D2, the plan and the block | done | `228f06835` |
| C2: an order that names a project runs in its registered repository | done | `902b5064b` |
| C3: handback | done | this commit |
| Gates 1 to 5 | done | all green, before this file was written |
| Push, gate 6 | pending at write time | outcomes in the worker's final reply |
