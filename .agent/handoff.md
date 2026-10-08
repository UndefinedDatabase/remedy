# Handoff — F253 round 14: book round 13, repair R-1197 to R-1200

## Session

SESSION 4 of feature F253 · round 14 · rounds so far 14

Context self-assessment: the reviewer's context is workable after two rounds; the session continues with S5b.

Fortschritt: ~73 % (S1 to S3, S4a to S4c, S5a, S6a · S5b, S5c, S6b, S7 open) — Schätzung

## Range

Review of `483efc3c3d65ba3228bff5a43518892263b29fcc`..HEAD (HEAD is C3 below, which carries this
handback and is the last commit on the branch).

## Commits

### 9f3a83851 F253 R14 C1: book round 13, register R-1197 to R-1200, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r14.md` | 122/0 | new file, byte copy of `block.md` |
| `.agent/live_review.md` | 10/0 | `append-live_review.txt`'s bytes appended: round 13's gate entry and R-1197 to R-1200 |
| `.agent/plan.md` | 7/6 | `dry-plan.md`, byte for byte |
| `.agent/prose_slips.md` | 1/0 | `append-prose_slips.txt`'s bytes appended: the round 13 prose slip |

### f51f2b1ec F253 R14 C2: an order reads running under a linked data root, and its rules gain their tests (R-1197 to R-1200)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/serve_runs.py` | 7/3 | `_process_is_this_order` compares the process's working folder with the order's folder resolved (`Path.resolve()`); docstring says why (R-1197) |
| `tests/orchestration/test_serve_runs.py` | 44/0 | three new tests: a symlinked data root reads `running` (R-1197); a planted, well-formed record at a malformed id's path still reads None (R-1198); a live pid working in another folder still reads `lost` (R-1199) |
| `tests/cli/test_client_order_cmd.py` | 59/1 | two new tests: the same planted-record guard through `remedy client order ../x --json` (R-1198); a running order's answer is null, then the printed envelope once ended (R-1200) |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |

## External actions

- `git push origin feature/f253-public-http-api`, once, after this commit: reported in the
  worker's reply, not here (this file is written before the push).
- No pull request opened, no full suite, no mutation, no worktree, no merge, no new branch, no
  force-push, no pull, no `REMEDY_TEST_MAX_WORKERS`, no `-n`. No command read, listed or wrote the
  repository's `.data`.

## Verification

1. Preconditions, before any write: `git rev-parse HEAD` read
   `483efc3c3d65ba3228bff5a43518892263b29fcc`, equal to
   `git rev-parse origin/feature/f253-public-http-api`; `git status --porcelain` was empty;
   `.agent/STOP` was absent; `block.md` read sha256
   `edf57ef7defa15c8af2ff0741d406f094686ee84a32064e564842acf6a1722d4` and all four files listed in
   `digests.txt` matched (Python `hashlib`, 4 of 4 True); `git branch --show-current` read
   `feature/f253-public-http-api` before each commit.
2. Every commit: its staged diff was written to a file in the worker folder and read whole before
   the commit (C1's three non-`authored/` files read whole; its 122-line block copy to
   `.agent/authored/f253-r14.md` proven byte-equal instead and so not re-read in full, though it
   was short enough that the diff tool showed it anyway; C2's 110 lines read whole).
3. **Gate 1**: `git status --porcelain` empty; the C1 byte proofs — `.agent/authored/f253-r14.md`
   byte-equal to `block.md` (122 lines, sha256
   `edf57ef7defa15c8af2ff0741d406f094686ee84a32064e564842acf6a1722d4`); `.agent/live_review.md`
   post == pre (235569 bytes) + slice (6738 bytes) = 242307 bytes, True; `.agent/prose_slips.md`
   post == pre (393641 bytes) + slice (297 bytes) = 393938 bytes, True; `.agent/plan.md` byte-equal
   to `dry-plan.md`, True — all True.
4. **Gate 2**, from the primary checkout, once:
   `python3 -m pytest -q -rfEs tests/orchestration/test_serve_runs.py tests/cli/test_client_order_cmd.py tests/cli/test_client_interface.py tests/test_ble001_ratchet.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py`
   — exit 0, `231 passed in 39.74s`; no FAILED, ERROR or SKIPPED line.
5. **Gate 3**: `python3 -m ruff check packages/orchestration/serve_runs.py tests/orchestration/test_serve_runs.py tests/cli/test_client_order_cmd.py`
   — exit 0, `All checks passed!`.
6. **Gate 4**: `python3 -m apps.cli.main integrity check --json` — exit 0, `"check_count": 6`, all
   six `pass`, `"fail_count": 0`, `"ok": true`.
7. **Gate 5**: `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   — exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160',
   'R-1162', 'R-1172', 'R-1176', 'R-1196', 'R-1197', 'R-1198', 'R-1199', 'R-1200']`, exactly as
   ordered.
8. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r14.md`: 122 lines, byte-equal, sha256
  `edf57ef7defa15c8af2ff0741d406f094686ee84a32064e564842acf6a1722d4`.
- `append-live_review.txt` appended to `.agent/live_review.md`'s base blob at `483efc3c3`:
  "post equals pre plus slice" True (235569 + 6738 = 242307 bytes).
- `append-prose_slips.txt` appended to `.agent/prose_slips.md`'s base blob at `483efc3c3`:
  "post equals pre plus slice" True (393641 + 297 = 393938 bytes).
- `dry-plan.md` to `.agent/plan.md`: byte-equal.

## Deviations & assumptions

- No departure from the block's ordered commit sequence: exactly C1, C2, this C3, in order; no
  C2b was needed because Gate 2 read green on its one and only run.
- **Choices the block left to me, inside C2's specification.** Each finding's "THE REPAIR"
  sentence states the behavior a test must hold; the exact test names, fixture shape and literal
  values were mine to pick: the planted-record tests (R-1198) use a placeholder `OrderRecord`
  whose fields are never read (the id-shape guard refuses before the file is even opened); the
  live-process test (R-1199) uses this test process's own `os.getpid()` as "a live process working
  in another folder", since the test runner's cwd is never an order's folder; the running-order
  test (R-1200) adds a new stand-in child (`_RUNNING_ORDER_CHILD`) that prints its envelope before
  waiting on a release file, modeled on the existing `_ORDER_CHILD`/`_ENDED_ORDER_CHILD` stand-ins
  already in the two test files rather than reusing either directly, because neither existing
  stand-in both prints early and waits. The docstring addition to `_process_is_this_order`
  explaining the resolve fix is my own wording of the reason the finding and the block both state.
- Everything else matches the block exactly: the one production comparison changed
  (`order_dir.resolve()`), nothing else in production code; the four findings' tests placed in the
  two files the block names; the gates' order, commands and content.

## Round verdicts

Round 13's PASS, with R-1197 to R-1200 registered, is booked by C1 above. Round 14's verdict is
the reviewer's, to be written into round 15's first commit.

## For the operator, in plain sentences

Round thirteen's work passed review, and the review found four things to fix. Remedy now reports
an order as still running when its data folder is reached through a link, and three rules about
orders that no test checked now each have a test.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback
   and stop.
2. Then the Open PR Gate (rule 2): there is no pull request for this branch, so it finds none to
   merge.
3. Then book round 14's verdict and resolve R-1197 to R-1200 in the next round's first commit.
4. Then S5b: `POST /api/v1/orders` and `GET /api/v1/orders/{order}`.

Operator questions open: 0.
Open findings: 16 (R-1197, Medium, and R-1198, R-1199, R-1200, Low, owned by F253; R-1160,
Medium, and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176 and
R-1196, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 13, register R-1197 to R-1200, the plan and the block | done | `9f3a83851` |
| C2: an order reads running under a linked data root, and its rules gain their tests | done | `f51f2b1ec` |
| Gates 1 to 5 | done | all green, run once each, after C2 and before this file |
| C3: this handback | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
