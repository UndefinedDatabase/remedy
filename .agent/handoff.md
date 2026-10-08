# Handoff — F298 session 4, round 18: T001's seventeenth part, every operation has an entry, and job resume's plain keys

## Session

SESSION 4 of feature F298 · round 18 · rounds so far 18

Context self-assessment: the reviewer's context is still sufficient after five rounds in this session; the session ends after this round, because the next part replaces the page written by hand with one rendered from the interface and needs a design decision that is best started with a fresh context.

Fortschritt: ~48 % (claim · T001 seventeen parts landed · T001 page, T002 to T007 open) — Schätzung

## Range

Review of `f27eac67a1ca1bc8ed7a8ce2daaa837e019dab36`..HEAD (HEAD is C4 below).

## Commits

### 5f2c93fd6 F298 R18 C1: book round 17, DECISION F298 D18, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f298-r18.md` | 129/0 (new) | byte copy of the reviewer's `block.md` (129 lines, sha256 `3d209ceb822995555ae289f3cabcc971e33c3fc38f96ec77dbf43116d9da7cf2`) |
| `.agent/decisions.md` | 10/0 | base blob at `f27eac67a` followed by `append-decisions.txt` (DECISION F298 D18) |
| `.agent/live_review.md` | 2/0 | base blob at `f27eac67a` followed by `append-live_review.txt` (books round 17's PASS) |
| `.agent/plan.md` | 8/10 | `dry-plan.md`, byte for byte |
| `.agent/prose_slips.md` | 1/0 | base blob at `f27eac67a` followed by `append-prose_slips.txt` |

### 3bf4ccd25 F298 R18 C2: every operation has an answer tree entry, and job resume's keys without a tree are plain (T001, DECISION F298 D18)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/client_interface.py` | 3/3 | byte copy of `dry-client_interface.py`: two comments say every operation has an entry |
| `tests/cli/test_client_interface.py` | 128/1 | byte copy of `dry-test_client_interface.py`: the entry assertion, the tables read by hand and the plain keys test of `job.resume` |

### 301a2cd2b F298 R18 C3: the machine client page names the proof of job resume's plain keys

| Path | +/- | Reason |
|---|---|---|
| `docs/system/machine-client-contract-v1.md` | 3/1 | byte copy of `dry-machine-client-contract-v1.md`: the page names the proof of `remedy job resume`'s plain keys |

### F298 R18 C4: handback (self-reference exception: the handoff is committed by this same commit)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten per `docs/agents/handback_template.md` |

## External actions

- `git push origin feature/f298-machine-client-contract-v1-1`: outcome, including whether an HTTP
  500 retry was needed, is in the worker's final reply (write-once rule; not known when this file
  is written).
- No merge, no branch switch, no new branch, no force-push, no pull, no pull request opened.

## Verification

0. Before any write: `block.md` and every `append-*` and `dry-*` file named in the prompt matched
   its sha256 digest and line count (8 of 8, Python `hashlib.sha256` over the bytes). `git rev-parse HEAD`
   read `f27eac67a1ca1bc8ed7a8ce2daaa837e019dab36`, equal to
   `origin/feature/f298-machine-client-contract-v1-1`; `git branch --show-current` read
   `feature/f298-machine-client-contract-v1-1`; `git status --porcelain` empty.
1. `git branch --show-current` read `feature/f298-machine-client-contract-v1-1` before every commit
   below (the commit script asserts it).
2. C1: five byte-equality proofs all `True` (block copy; `.agent/live_review.md`,
   `.agent/prose_slips.md` and `.agent/decisions.md` each equal to their base blob at `f27eac67a`
   plus the matching `append-*.txt`; `.agent/plan.md` equal to `dry-plan.md`). Numstat before
   commit: `129 0` block copy, `10 0` decisions.md, `2 0` live_review.md, `8 10` plan.md, `1 0`
   prose_slips.md, matching the block exactly. The WHOLE `git diff --cached` was read as
   self-review before the commit.
3. C2: two byte-equality proofs, both `True`. Numstat before commit: `3 3` client_interface.py,
   `128 1` test_client_interface.py, matching the block exactly. The whole `git diff --cached` was
   read as self-review before the commit.
4. C3: one byte-equality proof, `True`. Numstat before commit: `3 1` the page, matching the block
   exactly. The whole `git diff --cached` was read before the commit.
5. **Gate 1** (run after C3): `git -C /home/decodeux/Repos/remedy status --porcelain` — captured
   exit code `0`, empty. All 8 byte proofs of C1, C2 and C3 run again against the committed blobs
   (`git show` of `5f2c93fd6`, `3bf4ccd25`, `301a2cd2b`), all `True`.
6. **Gate 2**:
   `python3 -m pytest -q -rfEs tests/cli/test_client_interface.py tests/cli/test_exit_codes.py tests/cli/test_machine_client_contract.py tests/cli/test_golden_path.py tests/docs/ tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py`
   — captured exit code `0`, no FAILED, ERROR or SKIPPED line, last line verbatim
   `843 passed in 67.11s (0:01:07)`. Run once, as the round's one test selection.
7. **Gate 3**: `python3 -m ruff check apps/cli/client_interface.py tests/cli/test_client_interface.py`
   — captured exit code `0`, whole output `All checks passed!`.
8. **Gate 4**: `python3 -m apps.cli.main integrity check --json` — captured exit code `0`:
   ```
   {"check_count": 6, "checks": [{"message": "handlers=176", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
   ```
   Six of six `pass`, `"fail_count": 0`.
9. **Gate 5**:
   `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   — captured exit code `0`, whole output:
   `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176']`
   — an exact match to the block's expected list.
10. **Gate 6** (after the push): reported in the worker's final reply.

## Authored-text proofs

- `block.md` → `.agent/authored/f298-r18.md`: 129 lines, byte-equal (`True`), sha256
  `3d209ceb822995555ae289f3cabcc971e33c3fc38f96ec77dbf43116d9da7cf2`.
- `dry-plan.md` → `.agent/plan.md`: byte-equal (`True`).
- base `.agent/live_review.md`, `.agent/prose_slips.md` and `.agent/decisions.md` blobs at
  `f27eac67a` + their `append-*.txt` → the files at C1: byte-equal (`True`, three of three).
- `dry-client_interface.py` → `apps/cli/client_interface.py`: byte-equal (`True`).
- `dry-test_client_interface.py` → `tests/cli/test_client_interface.py`: byte-equal (`True`).
- `dry-machine-client-contract-v1.md` → `docs/system/machine-client-contract-v1.md`: byte-equal
  (`True`).
- Each of these proofs ran twice: before its commit against the working file, and in gate 1 after
  C3 against the committed blob.

## Deviations & assumptions

One: gates 3, 4 and 5 (ruff, the integrity check and the open-findings reading, none of them a test
command) were issued as three tool calls in one batch, so they may have run at the same time rather
than one after another; each captured its own exit code and none read the others' output. Gate 2,
the only test command, ran alone and exactly once. Otherwise C1, C2 and C3 follow the block's order
with its subjects, with no file written outside the named paths. No `cd`, nothing written under
`/tmp`, no `-n`, no `REMEDY_TEST_MAX_WORKERS`; no mutation and no full suite were run. Gate 1's
byte proofs ran after C3 as ordered. No command was refused. Every numstat the block named was
checked before its commit and matched exactly. C1, C2 and C3 were each committed after reading
their whole staged diff. The Co-Authored-By trailer names `Claude Sonnet 5.5`, the model the
worker runs on.

## For the operator, in plain sentences

Every command a program uses now has its names described, and a test fails if a command is ever
left out. The command that continues a stopped job answers in many ways that the long end-to-end
test does not reach. A new test reads all of them and fails unless every part without names of its
own holds only a single value or a plain list. The earlier plan to prove this for every command was
narrowed to that one command, and the record says why. The next step makes the page itself come
from the description.

## Round verdicts

Round 17's PASS and its prose slip are booked by this round's C1, in `.agent/live_review.md` and
`.agent/prose_slips.md`.

Round 18: VERDICT PASS, verified by dry run, bytes identical, given by the reviewer of session 4
after this handback. `.remedy-wt/f298-r18/review18.py`, whose readings are saved beside it as
`review18-readings.txt`, read the saved block and `.agent/plan.md` at `5f2c93fd6`, the three
appended records there, the two files of `3bf4ccd25` and the page of `301a2cd2b` equal to the
prepared files of the reviewer's dry run on `f27eac67a`, and the four records and the saved block
unchanged by `c8d83ffb5`, thirteen of thirteen; `c8d83ffb5` touches only this file. The dry run's
readings, saved as `.remedy-wt/f298-r18/build-readings-b.txt`: the round's selection `843 passed`
at exit 0, ruff clean on the two touched Python files, integrity six of six `pass`, and the open
set unchanged. The dry run's copy of the saved block differed from the committed one only in this
file's context self-assessment sentence, which the reviewer corrected before delegating, and no
test of the selection reads a saved block. The reviewer's ten mutation red-proofs, saved as
`.remedy-wt/f298-r18/mutations.txt`, each turned `tests/cli/test_client_interface.py` red, with
the unmutated control green before and after. The worker's one run read `843 passed`. The worker
declared its one deviation, gates 3 to 5 issued together, none of them a test command. The next
session books this verdict into `.agent/live_review.md` in its first round's first commit; there
is no prose slip for round 18.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback
   and stop.
2. Then rule 2, the Open PR Gate.
3. Then confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Then book round 18's verdict, quoted above, in the next round's first commit.
5. Then T001, last part: `docs/system/machine-client-contract-v1.md` rendered from
   `build_client_interface` in `apps/cli/client_interface.py`, with the test that fails when page
   and interface differ. First fix in a DECISION, in the same round as its patch, what happens to
   the page's tables that F295 wrote by hand, which `tests/cli/test_machine_client_contract.py`
   holds equal to what that gate test uses: rendered, kept beside the rendering, or replaced, and
   how the rendering is produced (a script, or the command itself) so that no part is written by
   hand. Read that test's page checks before deciding.
6. The soft limit is 25 rounds or 7 sessions. F298 stands at 18 rounds and 4 sessions with the
   page part and T002 to T007 open, so the split DECISION F298 D1 names will be needed: the session
   that reaches the limit writes the scope report and executes the split-and-close default, which
   moves the remaining slices of T005 to T007 to a feature placed directly behind this one.

Operator questions open: 0.
Open findings: 11 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172 and R-1176, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 17, DECISION F298 D18, the plan | done | `5f2c93fd6` |
| C2: every operation has an answer tree entry, and job resume's keys without a tree are plain | done | `3bf4ccd25` |
| C3: the machine client page names the proof of job resume's plain keys | done | `301a2cd2b` |
| C4: handback | done | this commit |
| Gates 1 to 5 | done | all green, see Verification |
| Push | done | outcome in the worker's final reply |
| Gate 6 | done | reported in the worker's final reply |
| Session close: round 18's verdict and the session's end | done | this commit |
