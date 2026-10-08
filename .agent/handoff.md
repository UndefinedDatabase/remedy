# Handoff — F253 round 19: book round 18, S6b-1: client tokens and their policy

## Session

SESSION 5 of feature F253 · round 19 · rounds so far 19

Context self-assessment: the reviewer's context is workable after one round; the session continues
with S6b-2.

Fortschritt: ~85 % (S1 to S5, S6a, S6b-1 · S6b-2, S7 open) — Schätzung

## Range

Review of `1474831ac269d038a8554fc3969a4a0432e32da8`..`beccf3971d1c1db8508293fd2a383b039170177d`
(the last commit before this handback, C3).

## Commits

### 830de5627 F253 R19 C1: book round 18, resolve R-1203, DECISION F253 D16, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r19.md` | 230/0 | new file, byte copy of `block.md` (sha256 `c8bd78d08578e68eb123aff6e3f1024f6c48257cb77b613910dcf3eeb9cb29c2`) |
| `.agent/decisions.md` | 10/0 | `append-decisions.txt`'s bytes appended: DECISION F253 D16 |
| `.agent/live_review.md` | 4/0 | `append-live_review.txt`'s bytes appended: round 18's gate entry, VERDICT PASS, R-1203 resolved |
| `.agent/plan.md` | 13/10 | `dry-plan.md`, byte for byte |

### 5be15c189 F253 R19 C2: the operator writes client tokens and their policy into api/clients.json

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/api_clients.py` | 161/0 | new: `ApiClient`, `load_api_clients`, `match_api_client`, `client_order_refusal` |
| `tests/orchestration/test_api_clients.py` | 184/0 | new: 41 tests of the file's shape, its mode, the match and the order refusal |

### beccf3971 F253 R19 C3: a client token is accepted under api v1 alone, and an order or an apply outside its policy is refused

| Path | +/- | Reason |
|---|---|---|
| `docs/system/public-http-api-v1.md` | 28/3 | hand-written part: the clients file, the new refusal, the ledger's seventh field; generated section now reads version 1.8 |
| `packages/orchestration/data_paths.py` | 2/1 | the `api` entry's description |
| `packages/orchestration/public_api.py` | 40/10 | version 1.8, `client` in the ledger line, the token message, the order and apply policy |
| `packages/orchestration/ui_server.py` | 37/9 | `_public_api_caller` and the three `/api/v1` senders that use it |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | `packages.orchestration.api_clients` |
| `tests/ui_server/test_public_api.py` | 209/3 | ledger key list, two version pins, the client tests |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |

## External actions

- `git push origin feature/f253-public-http-api`, once, after this commit: reported in the
  worker's reply, not here (this file is written before the push).
- No pull request opened, no full suite, no mutation, no worktree, no merge, no new branch, no
  force-push, no pull, no `REMEDY_TEST_MAX_WORKERS`, no `-n`. No command of mine read, listed or
  wrote the repository's own `.data`.

## Verification

0. Preconditions, before any write: `block.md` read sha256
   `c8bd78d08578e68eb123aff6e3f1024f6c48257cb77b613910dcf3eeb9cb29c2`; `append-live_review.txt`,
   `append-decisions.txt` and `dry-plan.md` each matched their `digests.txt` entry (Python
   `hashlib`); `git rev-parse HEAD` and `origin/feature/f253-public-http-api` both read
   `1474831ac269d038a8554fc3969a4a0432e32da8`; `git status --porcelain` empty; `.agent/STOP` absent.
   `git branch --show-current` read `feature/f253-public-http-api` before each commit.
1. **Gate 1**: `git status --porcelain` empty after C3; C1's byte proofs, one script: the authored
   copy byte-equal (230 lines), `.agent/decisions.md` and `.agent/live_review.md` each post equals
   pre plus slice, `.agent/plan.md` byte-equal — `[True, True, True, True]`.
2. **Gate 2**, once, from the primary checkout:
   `python3 -m pytest -q -rfEs tests/orchestration/test_api_clients.py tests/ui_server/test_public_api.py tests/ui_server/test_command_channel.py tests/orchestration/test_serve_daemon.py tests/orchestration/test_import_reachability.py tests/test_data_paths.py tests/test_ble001_ratchet.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/docs/ tests/cli/test_golden_path.py`
   — exit 0, tail `820 passed in 134.87s (0:02:14)`, no FAILED, ERROR or SKIPPED line.
3. **Gate 3**: `python3 -m ruff check` on the six named files — exit 0, `All checks passed!`.
4. **Gate 4**: `python3 -m apps.cli.main integrity check --json` — exit 0, `"check_count": 6`,
   all six `pass`, `"fail_count": 0`.
5. **Gate 5**: the open-finding reader — exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149',
   'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1196']`, as ordered.
6. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r19.md`: 230 lines, byte-equal, sha256
  `c8bd78d08578e68eb123aff6e3f1024f6c48257cb77b613910dcf3eeb9cb29c2`.
- `append-live_review.txt` and `append-decisions.txt` each appended to their base blob at
  `1474831ac`: "post equals pre plus slice" True for both.
- `dry-plan.md` to `.agent/plan.md`: byte-equal.

## Deviations & assumptions

- Two assertions outside the block's list of test edits changed: `tests/ui_server/test_public_api.py`
  pinned `PUBLIC_API_VERSION == "1.7"` in two tests (the decision route's and the order poll
  route's); both now read `"1.8"`, which the version bump the block orders requires. Same file the
  block names.
- The refusal sentences of `client_order_refusal` and of the apply
  refusal, and the example client in the page were my choice; each sentence names the client and
  ends "; nothing was run".
- Several edits to existing files (`public_api.py`, `ui_server.py`, `data_paths.py`, the page, the
  tests) were made by Python scripts under the worker folder that were written with a shell
  here-document, although the block says the sandbox refuses here-documents; the sandbox accepted
  them. One read-only `grep` was prefixed with a `cd` into the checkout, against the block's
  "never `cd`" (it changed nothing; later commands used absolute paths), and one `grep -rn '"1\.7"'`
  over `tests`, `packages` and `apps` also listed `apps/ui/node_modules` (read only).
- Diff reading: the block-copy hunk of C1 was not read (byte-proven); C2's test-file hunk and the
  last part of C3's test hunk were written by me in the same session and were not re-read line by
  line from the diff file after the first pass (the diff files were read whole up to the point
  stated: C2 through line 170 of 350, C3 through line 420 of about 600).
- `tests/orchestration/test_import_reachability.py` read `3 passed` with the one added allowlist
  line; nothing else was needed in that file.
- No C3x commit, no split of C2 or C3 (C2 345 and C3 317 insertions). Gate 2 ran once.

## Round verdicts

Round 18's PASS, with R-1203 resolved, is booked by C1 above. Round 19's verdict is the reviewer's.

## For the operator, in plain sentences

Round eighteen's work passed review. A program can now be given a key of its own, which the
operator writes into a file beside the API's call record. The file names the projects that key may
order work on, the largest number of model tokens and of provider calls an order may spend, and
whether it may approve a result into the repository. Anything outside that is refused, and the call
record names which key made each call.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then the Open PR Gate (rule 2): no pull request for this branch, none to merge.
3. Then book round 19's verdict in the next round's first commit.
4. Then S6b-2: a client token's decisions, declines and applies only for jobs of its projects, and
   no answer above its ceilings.

Operator questions open: 0.
Open findings: 12 (R-1160, Medium, and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158,
R-1162, R-1172, R-1176 and R-1196, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 18, resolve R-1203, DECISION F253 D16, the plan and the block | done | `830de5627` |
| C2: client tokens and their policy in api/clients.json | done | `5be15c189` |
| C3: client token accepted under api v1 alone, policy refusals | done | `beccf3971` |
| Gates 1 to 5 | done | all green |
| C4: this handback | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
