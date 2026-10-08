# Handoff — F298 session 5, round 19: T001's eighteenth part, an argument's value and repetition read from the parser (R-1178)

## Session

SESSION 5 of feature F298 · round 19 · rounds so far 19

Context self-assessment: the reviewer's context is sufficient after the first round of this session, and the session continues with the page rendered from the interface.

Fortschritt: ~50 % (claim · T001 eighteen parts landed · T001 page, T002 to T007 open) — Schätzung

## Range

Review of `c04575133bb571d2ec8f91acabb22988849be6af`..HEAD (HEAD is C3 below).

## Commits

### aeff42edb F298 R19 C1: book round 18, register R-1178, DECISION F298 D19, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f298-r19.md` | 126/0 (new) | byte copy of the reviewer's `block.md` (126 lines, sha256 `cce27e7e46f2c292dcfe3488617e971f9785d84b8a7aed696182a3e82fc1265f`) |
| `.agent/decisions.md` | 10/0 | base blob at `c04575133` followed by `append-decisions.txt` (DECISION F298 D19) |
| `.agent/live_review.md` | 4/0 | base blob at `c04575133` followed by `append-live_review.txt` (books round 18's PASS, registers R-1178) |
| `.agent/plan.md` | 6/5 | `dry-plan.md`, byte for byte |

### f290ec945 F298 R19 C2: an argument's value and repetition are read from the parser (T001, R-1178, DECISION F298 D19)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/client_interface.py` | 25/8 | byte copy of `dry-client_interface.py`: `takes_value` and `repeatable` are read from the parser's action for each argument |
| `tests/cli/test_client_interface.py` | 39/5 | byte copy of `dry-test_client_interface.py`: both fields held to the parser `remedy` runs, and the switches pinned by name |
| `.agent/live_review.md` | 2/0 | blob at C1 followed by `append-landed.txt` (the `Landed:` line for R-1178) |

### F298 R19 C3: handback (self-reference exception: the handoff is committed by this same commit)

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
   its sha256 digest and line count (7 of 7, Python `hashlib.sha256` over the bytes). `git rev-parse HEAD`
   read `c04575133bb571d2ec8f91acabb22988849be6af`, equal to
   `origin/feature/f298-machine-client-contract-v1-1`; `git branch --show-current` read
   `feature/f298-machine-client-contract-v1-1`; `git status --porcelain` empty.
1. `git branch --show-current` read `feature/f298-machine-client-contract-v1-1` before every commit
   (the commit script asserts it).
2. C1: four byte-equality proofs all `True` (block copy, 126 lines; `.agent/live_review.md` and
   `.agent/decisions.md` each equal to their base blob at `c04575133` plus the matching
   `append-*.txt`; `.agent/plan.md` equal to `dry-plan.md`). Numstat before commit: `126 0` block
   copy, `10 0` decisions.md, `4 0` live_review.md, `6 5` plan.md, matching the block exactly.
3. C2: three byte-equality proofs, all `True`. Numstat before commit: `25 8` client_interface.py,
   `39 5` test_client_interface.py, `2 0` live_review.md, matching the block exactly.
4. **Gate 1** (after C2): `git -C /home/decodeux/Repos/remedy status --porcelain` — empty. All 8
   byte proofs of C1 and C2 run again against the committed blobs (`git show` of `aeff42edb` and
   `f290ec945`), all `True`.
5. **Gate 2**:
   `python3 -m pytest -q -rfEs tests/cli/test_client_interface.py tests/cli/test_exit_codes.py tests/cli/test_machine_client_contract.py tests/cli/test_golden_path.py tests/docs/ tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py`
   — captured exit code `0`, no FAILED, ERROR or SKIPPED line, last line verbatim
   `844 passed in 66.78s (0:01:06)`. Run once, as the round's one test selection.
6. **Gate 3**: `python3 -m ruff check apps/cli/client_interface.py tests/cli/test_client_interface.py`
   — captured exit code `0`, whole output `All checks passed!`.
7. **Gate 4**: `python3 -m apps.cli.main integrity check --json` — captured exit code `0`:
   ```
   {"check_count": 6, "checks": [{"message": "handlers=176", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
   ```
   Six of six `pass`, `"fail_count": 0`.
8. **Gate 5**:
   `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   — captured exit code `0`, whole output:
   `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1178']`
   — an exact match to the block's expected list.
9. **Gate 6** (after the push): reported in the worker's final reply.

## Authored-text proofs

- `block.md` → `.agent/authored/f298-r19.md`: 126 lines, byte-equal (`True`), sha256
  `cce27e7e46f2c292dcfe3488617e971f9785d84b8a7aed696182a3e82fc1265f`.
- `dry-plan.md` → `.agent/plan.md`: byte-equal (`True`).
- base `.agent/live_review.md` and `.agent/decisions.md` blobs at `c04575133` + their `append-*.txt`
  → the files at C1: byte-equal (`True`, two of two).
- `dry-client_interface.py` → `apps/cli/client_interface.py`: byte-equal (`True`).
- `dry-test_client_interface.py` → `tests/cli/test_client_interface.py`: byte-equal (`True`).
- C1's `.agent/live_review.md` blob + `append-landed.txt` → the file at C2: byte-equal (`True`).
- Each of these proofs ran twice: before its commit against the working file, and in gate 1 after
  C2 against the committed blob.

## Deviations & assumptions

Two, both of order and form. First, gates 1, 3, 4, 5 and 2 ran in one script one after another, in
that order (gate 2 last), not in the numbered order; each captured its own exit code, and gate 2,
the only test command, ran alone and exactly once. Second, `.agent/authored/f298-r19.md` was staged
with `git add -f`, in case the path is ignored; no other path was forced. Otherwise C1 and C2 follow
the block's order with its subjects, with no file written outside the named paths. No `cd`, nothing
written under `/tmp`, no `-n`, no `REMEDY_TEST_MAX_WORKERS`; no mutation and no full suite were run.
Gate 1's byte proofs ran after C2 as ordered. No command was refused. Every numstat the block named
was checked before its commit and matched exactly. C1 and C2 were each committed after reading their
whole staged diff. The Co-Authored-By trailer names `Claude Sonnet 5.5`, the model the worker runs
on.

## For the operator, in plain sentences

The description of Remedy's commands that a program reads said that some on-off switches, the
approval switch among them, expect a value after them, and that one option could not be given twice.
That was wrong, because the part of Remedy that reads a command line treats those switches by their
names. The description now asks that part directly, and a test fails if the two ever disagree. The
next step makes the page itself come from the description.

## Round verdicts

Round 18's PASS is booked by this round's C1, in `.agent/live_review.md`.

Round 19's verdict is the reviewer's. The reviewer books it, with the resolution of R-1178, in the
next round's first commit.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback
   and stop.
2. Then rule 2, the Open PR Gate.
3. Then confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Then book round 19's verdict and resolve R-1178 in the next round's first commit.
5. Then T001, last part: the page rendered from the interface, `docs/system/machine-client-contract-v1.md`
   rendered from `build_client_interface` in `apps/cli/client_interface.py`, with the test that fails
   when page and interface differ. First fix in a DECISION, in the same round as its patch, what
   happens to the page's tables that F295 wrote by hand, which
   `tests/cli/test_machine_client_contract.py` holds equal to what that gate test uses.
6. The soft limit is 25 rounds or 7 sessions. F298 stands at 19 rounds and 5 sessions with the
   page part and T002 to T007 open, so the split DECISION F298 D1 names will be needed when the
   limit is reached.

Operator questions open: 0.
Open findings: 12 (R-1160 and R-1178, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172 and R-1176, Low; R-1178 owned by F298 and landed, the rest owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 18, register R-1178, DECISION F298 D19, the plan | done | `aeff42edb` |
| C2: an argument's value and repetition are read from the parser | done | `f290ec945` |
| C3: handback | done | this commit |
| Gates 1 to 5 | done | all green, see Verification |
| Push | done | outcome in the worker's final reply |
| Gate 6 | done | reported in the worker's final reply |
