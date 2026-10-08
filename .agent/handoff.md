# Handoff — F253 round 12: book round 11, S4c: approve an apply over HTTP

## Session

SESSION 3 of feature F253 · round 12 · rounds so far 12

Context self-assessment: the reviewer's context is workable after three rounds; the session continues with S5.

Fortschritt: ~70 % (S1 to S3, S4a to S4c, S6a · S5, S6b, S7 open) — Schätzung

## Range

Review of `140785dbe0070ec5c57e274a37c49e04022ea9c6`..HEAD (HEAD is C3 below, which carries this
handback and is the last commit on the branch).

## Commits

### 3d9ec26a8 F253 R12 C1: book round 11, DECISION F253 D12, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r12.md` | 118/0 | new file, byte copy of `block.md` |
| `.agent/live_review.md` | 2/0 | `append-live_review.txt`'s bytes appended: round 11's gate entry |
| `.agent/decisions.md` | 10/0 | `append-decisions.txt`'s bytes appended: DECISION F253 D12 |
| `.agent/plan.md` | 11/11 | `dry-plan.md`, byte for byte |

### 28e949aea F253 R12 C2: a client approves an apply over HTTP, into the job's own repository (DECISION F253 D12)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/public_api.py` | 88/9 | the route `POST /api/v1/jobs/{job}/apply`, its argument builder, the body kind `flag`, `PublicApiWriteRefusal`, `PUBLIC_API_VERSION` `1.6` |
| `docs/system/public-http-api-v1.md` | 15/11 | the page: the kind `flag`, the refusal `api_job_repository_unknown`, the route row, version |
| `tests/ui_server/test_public_api.py` | 84/3 | route pin, argument tests, flag and key refusal tests, flag consistency in the well-formed test |
| `tests/orchestration/test_serve_daemon.py` | 86/2 | a real supervisor lands one commit in the job's own repository and refuses as the command does or before it |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |

## External actions

- `git push origin feature/f253-public-http-api`, once, after this commit: reported in the worker's
  reply, not here (this file is written before the push).
- No pull request opened, no full suite, no mutation, no worktree, no merge, no new branch, no
  force-push, no pull, no `REMEDY_TEST_MAX_WORKERS`, no `-n`. No command read, listed or wrote the
  repository's `.data`.

## Verification

1. Preconditions, before any write: `git rev-parse HEAD` read `140785dbe0070ec5c57e274a37c49e04022ea9c6`,
   equal to `git rev-parse origin/feature/f253-public-http-api`; `git status --porcelain` was empty;
   `.agent/STOP` was absent; `block.md` read sha256
   `39e1830c76f86698aaddcda06d7682f28db628381f16df188161125a8a654191` and all eight files listed in
   `digests.txt` matched (Python `hashlib`, 8 of 8 True); `git branch --show-current` read
   `feature/f253-public-http-api` before each commit.
2. Every commit: its staged diff was written to a file in the worker folder and read whole before the
   commit (C1 the three non-block files whole, the 118 lines of the block copy proven byte-equal
   instead; C2 432 lines whole).
3. **Gate 1**: `git status --porcelain` empty; `.agent/live_review.md` and `.agent/decisions.md` each
   equal their blob at `140785dbe` followed by their append file, True (in the working tree and in
   the committed blob); `.agent/authored/f253-r12.md` 118 lines, sha256
   `39e1830c76f86698aaddcda06d7682f28db628381f16df188161125a8a654191`; the plan and the four files of
   C2 each byte-equal to its prepared file, all True (16 of 16).
4. **Gate 2**, from the primary checkout, once: exit 0, `848 passed in 154.66s (0:02:34)`; no FAILED,
   ERROR or SKIPPED line.
5. **Gate 3**: `python3 -m ruff check` on the three Python files — exit 0, `All checks passed!`.
6. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`, all six
   `pass`, `"fail_count": 0`, `"ok": true`.
7. **Gate 5**: exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158',
   'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1196']`.
8. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r12.md`: 118 lines, byte-equal, sha256
  `39e1830c76f86698aaddcda06d7682f28db628381f16df188161125a8a654191`.
- The two append files appended to their base blobs at `140785dbe`: "post equals pre plus slice"
  True for each.
- `dry-plan.md` to `.agent/plan.md`, and the four prepared files of C2 to their paths: byte-equal.

## Deviations & assumptions

None.

## Round verdicts

Round 11's PASS is booked by C1. Round 12's verdict is the reviewer's, written into the next round's
first commit.

## For the operator, in plain sentences

Round eleven's work passed review. A program can now approve a finished result through the web
interface, and Remedy then applies it, makes the commit and pushes it if asked. Remedy always applies
it to the repository the job itself was run in, never to one the program names, and it never runs a
test command a program sends. A job whose record does not say which repository it belongs to is
refused with a clear answer.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then the Open PR Gate (rule 2): there is no pull request for this branch yet, so it finds none to
   merge.
3. Then book round 12's verdict in the next round's first commit.
4. Then S5: submit an order over HTTP, created and then polled.

Operator questions open: 0.
Open findings: 12 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172, R-1176 and R-1196, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 11, DECISION F253 D12, the plan and the block | done | `3d9ec26a8` |
| C2: `POST /api/v1/jobs/{job}/apply` | done | `28e949aea` |
| Gates 1 to 5 | done | all green, run once each, after C2 and before this file |
| C3: this handback | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
