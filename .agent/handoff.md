# Handoff — F298 session 1, round 3: T001's second part, the digest's key tree

## Session

SESSION 1 of feature F298 · round 3 · rounds so far 3

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~12 % (claim · T001 two parts landed · T001 rest and T002 to T007 open) — Schätzung

## Range

Review of `d9697d902b79332e1e31a4d92755b8a20b641e13`..HEAD (HEAD is C4 below).

## Commits

### a252d2b72 F298 R3 C1: book round 2, DECISION F298 D3, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f298-r3.md` | 120/0 (new) | byte copy of the reviewer's `block.md` (120 lines, sha256 `bd23d51237a958c5d4e3c7d4419cb214f4d79c3940ed123db53b723c1c16f807`) |
| `.agent/decisions.md` | 10/0 | base blob at `d9697d902` followed by `append-decisions.txt` (DECISION F298 D3) |
| `.agent/live_review.md` | 2/0 | base blob at `d9697d902` followed by `append-live_review.txt` (books round 2's PASS) |
| `.agent/plan.md` | 6/7 | `dry-plan.md`, byte for byte |

### a8eddfdb5 F298 R3 C2: the digest's keys as one tree in the machine client interface (T001, DECISION F298 D3)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/client_interface.py` | 62/2 | byte copy of `dry-client_interface.py`: `DIGEST_KEY_TREE` and `build_client_interface()` carrying it under `digest` |
| `apps/cli/commands/client_cmd.py` | 1/0 | byte copy of `dry-client_cmd.py`: the text summary names the digest's top-level keys |
| `tests/cli/test_client_interface.py` | 82/0 | byte copy of `dry-test_client_interface.py`: the syntax-tree test against `client_digest.py` and `project_cost_of_day`, and the live-run test against a real digest |

### 08be40a0c F298 R3 C3: the machine client page names the digest's key tree

| Path | +/- | Reason |
|---|---|---|
| `docs/system/machine-client-contract-v1.md` | 4/2 | byte copy of `dry-machine-client-contract-v1.md`: "The interface as data" names the `digest` tree and the test that holds it |

### F298 R3 C4: handback (self-reference exception: the handoff is committed by this same commit)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten per `docs/agents/handback_template.md` |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` run before the push:
  empty list, so the Open PR Gate passed with no action needed.
- `git push origin feature/f298-machine-client-contract-v1-1`: outcome, including whether an HTTP
  500 retry was needed, is in the worker's final reply (write-once rule; not known when this file
  is written).
- No merge, no branch switch, no new branch, no force-push, no pull, no pull request opened.

## Verification

0. Before any write: `block.md` and every `append-*` and `dry-*` file named in the prompt matched
   its sha256 digest (8 of 8, Python `hashlib.sha256` over the bytes); `block.md` is 120 lines,
   matching its stated line count. `git rev-parse HEAD` read
   `d9697d902b79332e1e31a4d92755b8a20b641e13`, equal to `origin/feature/f298-machine-client-contract-v1-1`;
   `git branch --show-current` read `feature/f298-machine-client-contract-v1-1`; `git status --porcelain`
   empty.
1. `git branch --show-current` read `feature/f298-machine-client-contract-v1-1` before every commit
   below.
2. C1: four byte-equality proofs all `True` (block copy; `.agent/live_review.md` and
   `.agent/decisions.md` each equal to their base blob at `d9697d902` plus the matching
   `append-*.txt`; `.agent/plan.md` equal to `dry-plan.md`). Numstat before commit: `120 0` block
   copy, `2 0` live_review.md, `10 0` decisions.md, `6 7` plan.md — matching the block exactly.
3. C2: three byte-equality proofs, one per path against its `dry-*` file, all `True`. Numstat
   before commit: `62 2` client_interface.py, `1 0` client_cmd.py, `82 0`
   test_client_interface.py — matching the block exactly. `git diff --cached` read as self-review
   before commit.
4. C3: one byte-equality proof, `True`. Numstat before commit: `4 2` the page — matching the
   block exactly.
5. **Gate 1**: `git -C /home/decodeux/Repos/remedy status --porcelain` — empty, captured exit
   code `0`. All 8 byte proofs of C1, C2 and C3 re-run after all three commits, all `True`.
6. **Gate 2**:
   `python3 -m pytest -q -rfEs tests/cli/test_client_interface.py tests/cli/test_machine_client_contract.py tests/orchestration/test_client_digest.py tests/orchestration/test_project_cockpit.py tests/cli/test_status_cmd.py tests/orchestration/test_import_reachability.py tests/cli/test_golden_path.py tests/docs/ tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py`
   — whole output: 8 lines of dots (511 dots total), no `F`, `E` or `s` character in any line,
   captured exit code `0` (`subprocess.run(...).returncode`), last line verbatim `511 passed in
   69.16s (0:01:09)`. Run once, as the round's one test selection.
7. **Gate 3**: `python3 -m ruff check apps/cli/client_interface.py apps/cli/commands/client_cmd.py
   tests/cli/test_client_interface.py` — captured exit code `0`, whole output `All checks
   passed!`.
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
10. **Gate 6**: `python3 -m apps.cli.main client interface` — captured exit code `0`, next-to-last
    line verbatim: `Digest (remedy status --json, under client): version, read_at, supervisor,
    projects, jobs, awaiting_apply, decisions, degraded, skipped_files` — matching the block
    exactly.
11. **Gate 7** (after the push): reported in the worker's final reply.

## Authored-text proofs

- `block.md` → `.agent/authored/f298-r3.md`: 120 lines, byte-equal (`True`), sha256
  `bd23d51237a958c5d4e3c7d4419cb214f4d79c3940ed123db53b723c1c16f807`.
- `dry-plan.md` → `.agent/plan.md`: byte-equal (`True`).
- base `.agent/live_review.md` blob at `d9697d902` + `append-live_review.txt` →
  `.agent/live_review.md`: byte-equal (`True`).
- base `.agent/decisions.md` blob at `d9697d902` + `append-decisions.txt` → `.agent/decisions.md`:
  byte-equal (`True`).
- `dry-client_interface.py` → `apps/cli/client_interface.py`: byte-equal (`True`).
- `dry-client_cmd.py` → `apps/cli/commands/client_cmd.py`: byte-equal (`True`).
- `dry-test_client_interface.py` → `tests/cli/test_client_interface.py`: byte-equal (`True`).
- `dry-machine-client-contract-v1.md` → `docs/system/machine-client-contract-v1.md`: byte-equal
  (`True`).

## Deviations & assumptions

None: C1, C2 and C3 follow the block's order with its subjects, with no file written outside the
named paths. No `cd`, nothing written under `/tmp`, no `-n`, no `REMEDY_TEST_MAX_WORKERS`, no two
test commands run at the same time; Gate 2 was the round's one test selection, run exactly once,
with its exit code captured inside the script that ran it. No mutation and no full suite were run
(the reviewer ran them, per the block). Every numstat the block named was checked before its
commit and matched exactly. The Open PR Gate (`gh pr list`) was additionally run before the push,
though the block did not order it for this round, because it is read-only, costs nothing, and
confirms the branch is still safe to push.

## For the operator, in plain sentences

The summary a program reads to learn the state of everything, the part of `remedy status --json`
named `client`, is now described key by key in what `remedy client interface` prints; two tests
keep that description honest, one by reading the code that writes the summary and one by running
a small job with stand-in workers and reading the summary it leaves; if a key is added, renamed
or put in another place, one of them fails until the description says the same.

## Round verdicts

Round 2's PASS is booked by this round's C1, in `.agent/live_review.md`. Round 3's verdict is the
reviewer's to give and book in the next round's first commit.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback
   and stop.
2. Then rule 2, the Open PR Gate.
3. Then confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Then book round 3's verdict in the next round's first commit.
5. Then T001, next part: the answer keys of the path's commands and the refusal tokens, held to
   the real commands.

Operator questions open: 0.
Open findings: 11 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172 and R-1176, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 2, DECISION F298 D3, the plan | done | `a252d2b72` |
| C2: the digest's keys as one tree in the machine client interface | done | `a8eddfdb5` |
| C3: the machine client page names the digest's key tree | done | `08be40a0c` |
| C4: handback | done | this commit |
| Gates 1 to 6 | done | all green, see Verification |
| Push | pending | run right after this commit, reported in the worker's final reply |
| Gate 7 | pending | reported in the worker's final reply |
