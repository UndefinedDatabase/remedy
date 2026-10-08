# Handoff — F253 round 2: book round 1, DECISION F253 D2, and S2a: the call ledger, query keys and `GET /api/v1/digest`

## Session

SESSION 1 of feature F253 · round 2 · rounds so far 2

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~16 % (S1, S2a · S2b to S7 open) — Schätzung

## Range

Review of `95d654a5c55267d99db66a96d478613505c978aa`..HEAD (HEAD is C4 below, which carries this
handback and is the last commit on the branch).

## Commits

### 9e9c6d181 F253 R2 C1: book round 1, register R-1187, DECISION F253 D2, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r2.md` | 226/0 | new file, byte copy of `block.md` |
| `.agent/decisions.md` | 10/0 | `append-decisions.txt`'s bytes appended, never read whole |
| `.agent/live_review.md` | 4/0 | `append-live_review.txt`'s bytes appended: round 1's gate entry and R-1187's registration |
| `.agent/plan.md` | 10/10 | `dry-plan.md`, byte for byte |
| `.agent/prose_slips.md` | 1/0 | `append-prose_slips.txt`'s bytes appended: round 1's allowlist deviation, dated |

### 00be6f560 F253 R2 C2: a ledger line for every call under the public HTTP API, query keys a route declares, and GET /api/v1/digest (S2a, DECISION F253 D2)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/data_paths.py` | 2/0 | `DURABLE_CLASSES` gains the `api` class, after `serve` |
| `packages/orchestration/public_api.py` | 110/11 | `PUBLIC_API_VERSION` to `1.1`; `PublicApiRoute` gains `twin_key` and `query`; the `GET /api/v1/digest` route; `answer_public_api_get` now parses the raw query against the route's declared keys and refuses `api_query_invalid`; `_status_digest_answer`; `append_public_api_call` and `PUBLIC_API_LEDGER_NAME`; the page renderer's `Query` column and twin-key `Answers as` cell |
| `packages/orchestration/ui_server.py` | 19/6 | `do_GET` passes the raw query string; `_send_public_api_get` now takes `query`, appends the ledger line before sending with the status/error it decided, catching exactly `OSError` |
| `tests/ui_server/test_public_api.py` | 190/3 | `PINNED_ROUTES` gains the digest route; the shape test checks `twin_key`/`query` against the catalog; new sections H (digest route), I (query refusals), J (the ledger), K (a failed append never changes the answer) |

### 4b0c927b2 F253 R2 C3: the page names the ledger, the query rule and the digest, and the command that starts the cockpit (R-1187)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/public-http-api-v1.md` | 20/9 | "Where it is served" names `remedy ui start` (R-1187); the refusals paragraph gains `api_query_invalid` and the twin-key sentence; new section `## The ledger`; the generated section rewritten by `write_public_api_page()` (version `1.1`, the `Query` column, the digest row) |
| `tests/ui_server/test_public_api.py` | 31/0 | the page states `api/calls.jsonl` and `api_query_invalid`; every `remedy ...` span of the hand-written part names a real catalog command |

### F253 R2 C4: handback (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |

## External actions

- Preconditions, before any write: `git rev-parse HEAD` read `95d654a5c55267d99db66a96d478613505c978aa`,
  equal to `git rev-parse origin/feature/f253-public-http-api`; `git status --porcelain` was empty;
  `.agent/STOP` was absent; `git branch --show-current` read `feature/f253-public-http-api` before
  every commit.
- Single test files and single commands run while writing C2 and C3, one at a time, none of them
  the round's gate-2 selection: `tests/test_data_root_classes.py` and `tests/test_data_paths.py`
  together (72 passed, confirming the new `api` class needed no change to the scanner's test file);
  `tests/ui_server/test_public_api.py` (run twice while writing it: 26 passed and 1 failed — the
  stale generated section, before C3's page edits and regeneration — then, once C3 had rewritten
  the hand-written part, run `write_public_api_page()` and added its own two tests, 29 passed);
  `python3 -m ruff check` on the touched files (clean each time); a one-off read-only `remedy
  status --json` / `remedy status run --json` check against the operator's real data root, to
  confirm the generated page's `remedy status run --json` cell is a real, runnable command line
  (it is: `status`'s own subcommand `run` may be typed explicitly or left implicit).
- `git push -u origin feature/f253-public-http-api`, once, after this commit: reported in the
  worker's reply, not here (Rule A4: this file is written before the push).
- No full suite, no mutation, no worktree, no merge, no new branch, no force-push, no pull, no
  checkout or switch away from the feature branch, no `REMEDY_TEST_MAX_WORKERS`, no `-n`.

## Verification

0. Digests: all five prepared files under `.remedy-wt/f253-r2/` matched their sha256 (Python
   `hashlib`, 5 of 5 True; `block.md` 226 lines, sha256
   `e09407793050eb4a83ed11642565004395ebd0d56f01f3a53cac0b8b89ecf3b4`).
1. C1: every append proved "post equals pre plus slice" in bytes (live_review, prose_slips,
   decisions — three of three True, decisions.md never read whole), the authored copy byte-equal
   to `block.md`, and the plan copy byte-equal to `dry-plan.md` (5 of 5 True in total). `git diff
   --cached --numstat` read `226 0`, `10 0`, `4 0`, `10 10`, `1 0`. The staged diff (314 lines) was
   written to a file and read whole as the self-review.
2. C2: the staged diff (506 lines) was written to a file and read whole as the self-review; single
   runs during writing are in External actions above.
3. C3: `write_public_api_page()` run once from the repository root via a `python3` script that
   captured its own exit code (per the block's constraint on scripts over compound shell); exit 0,
   empty stdout and stderr. The staged diff (97 lines) was written to a file and read whole as the
   self-review.
4. **Gate 1** (after C3, before C4): `git -C /home/decodeux/Repos/remedy status --porcelain` —
   empty. The C1 byte proofs, re-run against the committed tree: 5 of 5 True.
5. **Gate 2**, from the primary checkout, once:

       python3 -m pytest -q -rfEs tests/ui_server/test_public_api.py tests/ui_server/test_command_channel.py tests/orchestration/test_serve_daemon.py tests/test_data_root_classes.py tests/test_data_paths.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/cli/test_status_cmd.py tests/orchestration/test_client_digest.py tests/cli/test_client_interface.py tests/docs/ tests/cli/test_golden_path.py

   exit 0, `758 passed in 101.15s`, no FAILED, ERROR or SKIPPED line.
6. **Gate 3**:

       python3 -m ruff check packages/orchestration/public_api.py packages/orchestration/ui_server.py packages/orchestration/data_paths.py tests/ui_server/test_public_api.py

   exit 0, `All checks passed!`. `tests/test_data_root_classes.py` was not touched by C2 (the
   scanner found the new `api` class dynamically through `data_class_dir("api", ...)`; verified by
   running that file, 72 passed with `tests/test_data_paths.py`), so it was not added to this gate.
7. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`,
   `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`,
   `repo_root_hygiene` and `high_blockers_open` all `pass`, `"fail_count": 0`, `"ok": true`.
8. **Gate 5** (`python3 -c "import scripts.rotate_live_review as r;
   print(r.open_finding_ids(open('.agent/live_review.md').read()))"`): exit 0,
   `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162',
   'R-1172', 'R-1176', 'R-1187']`.
9. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r2.md`: 226 lines, byte-equal, sha256
  `e09407793050eb4a83ed11642565004395ebd0d56f01f3a53cac0b8b89ecf3b4` (Verification item 0 and 1).
- `append-live_review.txt`, `append-prose_slips.txt`, `append-decisions.txt` appended to their base
  blobs at `95d654a5c`: each "post equals pre plus slice" True (Verification item 1); `decisions.md`
  never read whole, per the block.
- `dry-plan.md` to `.agent/plan.md`: byte-equal (Verification item 1).
- `docs/system/public-http-api-v1.md`'s generated section equal to `render_public_api_markdown()`:
  proved by `tests/ui_server/test_public_api.py::test_the_pages_generated_section_equals_the_rendering`,
  part of Gate 2's green run.

## Deviations & assumptions

One minor action beyond the block's letter: while writing C3, this worker ran a read-only `remedy
status --json` / `remedy status run --json` check against the operator's real data root (not a
test file, not a mutation, nothing written) to confirm the generated page's `remedy status run
--json` cell names a command that really runs; the block's single-file allowance during C2/C3
names test files specifically. No file changed and nothing else followed from it. Otherwise: none.
C1 through C3 landed in the order and under the subjects the block gave, touching only the paths
it named for each commit.

## Round verdicts

Round 1's PASS and R-1187's registration are booked by this round's C1. Round 2's verdict is the
reviewer's.

## For the operator, in plain sentences

The first round's work passed review. A program can now read the same overview of projects, jobs,
open decisions and waiting results that the command line gives it, over the web interface. Every
request to that interface, a refused one included, is now written down in a log under Remedy's
data folder, with a fingerprint of the key the program used but never the key itself. A small
mistake on the interface's page, which named the wrong command for starting the cockpit, is
corrected. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then the Open PR Gate.
3. Then book round 2's verdict in the next round's first commit.
4. Then S2b: the proof of a job.

Operator questions open: 0.
Open findings: 12 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172, R-1176 and R-1187, Low; R-1187 owned by F253 and repaired in this round, awaiting the
reviewer's resolution; the rest owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 1, register R-1187, DECISION F253 D2, the plan and the block | done | `9e9c6d181` |
| C2: the call ledger, query keys and `GET /api/v1/digest` | done | `00be6f560` |
| C3: the published page and R-1187's repair | done | `4b0c927b2` |
| Gates 1 to 5 | done | all green, run once each, before this file was written |
| C4: this handback | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
