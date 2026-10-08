# Handoff — F253 round 3: book round 2, R-1188, DECISION F253 D3, and S2b: `GET /api/v1/jobs/{job}/proof`

## Session

SESSION 1 of feature F253 · round 3 · rounds so far 3

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~24 % (S1, S2 · S3 to S7 open) — Schätzung

## Range

Review of `a274e5fb7a9c6a28a68b375fa9869719800237aa`..HEAD (HEAD is C5 below, which carries this
handback and is the last commit on the branch).

## Commits

### da9e33a3e F253 R3 C1: book round 2, R-1187's recurrence, register R-1188, DECISION F253 D3, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r3.md` | 216/0 | new file, byte copy of `block.md` |
| `.agent/decisions.md` | 10/0 | `append-decisions.txt`'s bytes appended, never read whole |
| `.agent/live_review.md` | 6/0 | `append-live_review.txt`'s bytes appended: round 2's gate entry, R-1187's recurrence and R-1188's registration |
| `.agent/plan.md` | 15/14 | `dry-plan.md`, byte for byte |
| `.agent/prose_slips.md` | 1/0 | `append-prose_slips.txt`'s bytes appended: round 2's slip, dated |

### 352e1d17b F253 R3 C2: GET /api/v1/jobs/{job}/proof, named path segments and each route's refusal statuses (S2b, DECISION F253 D3)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/public_api.py` | 125/27 | `PUBLIC_API_VERSION` to `1.2`; the docstring's paragraph on routes; `PublicApiRoute` gains `refusals`; `_match_route_path`; the third route `GET /api/v1/jobs/{job}/proof` twinned with `change.proof`; `_change_proof_answer`; `answer_public_api_get` matches a route's template, binds segments and answers the status a refusal's token declares; the page renderer's `Refusals` column |
| `tests/ui_server/test_public_api.py` | 109/1 | `PINNED_ROUTES` gains the proof route; the shape test checks path segments and `refusals` against `OPERATION_REFUSAL_TOKENS`; new section H2 (the proof route, its refusals and its neighbouring 404/400 paths) |

### 026f65563 F253 R3 C3: POST, PUT and DELETE under the public HTTP API answer api_method_not_allowed in the envelope and are ledgered (R-1188, DECISION F253 D3)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/public_api.py` | 10/0 | `public_api_method_refusal` |
| `packages/orchestration/ui_server.py` | 59/13 | `_send_public_api_answer` (the shared ledgered-send tail), `_send_public_api_get` rewritten to use it, `_send_public_api_refused_method`; `do_POST` calls it for a public-API path before the commands door; `do_PUT` and `do_DELETE` read the path defensively and call it too |
| `tests/ui_server/test_command_channel.py` | 23/4 | `_walkable_paths` writes each registry path with its `{name}` segments replaced by the test's job id; the walk expects `api_method_not_allowed` on public-API paths and `method not allowed` elsewhere |
| `tests/ui_server/test_public_api.py` | 39/0 | new section L: `POST`/`PUT`/`DELETE` on `/api/v1/interface` answer 405 `api_method_not_allowed` with the token and 401 without it, each ledgered |

### a0e359340 F253 R3 C4: the page names the proof route, the refusal statuses and the refused methods, and R-1187's test reads a group named alone by its run command

| Path | +/- | Reason |
|---|---|---|
| `docs/system/public-http-api-v1.md` | 18/11 | the hand-written part names path segments in braces, the `Refusals` column and the 401/405 split for `POST`/`PUT`/`DELETE`; the generated section rewritten by `write_public_api_page()` (version `1.2`, the `Refusals` column, the proof route's row) |
| `tests/ui_server/test_public_api.py` | 15/1 | the bare-group branch of `test_every_remedy_command_the_pages_hand_written_part_names_is_in_the_catalog` now requires that group's `run` command (R-1187's recurrence repair); a new test holds `api_method_not_allowed` on the page |

### F253 R3 C5: handback (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |

## External actions

- Preconditions, before any write: `git rev-parse HEAD` read `a274e5fb7a9c6a28a68b375fa9869719800237aa`,
  equal to `git rev-parse origin/feature/f253-public-http-api`; `git status --porcelain` was empty;
  `.agent/STOP` was absent; `git branch --show-current` read `feature/f253-public-http-api` before
  every commit.
- Single test files run while writing C2 and C3, one at a time, none of them the round's gate-2
  selection: `tests/ui_server/test_public_api.py` (run several times while writing the proof route
  — one run caught a real bug: `_change_proof_answer`'s envelope carries `build_proof_chain`'s own
  fresh `generated_at` timestamp, which never equals the reference command's; the test gained
  `_without_generated_at` and the run after was green; later runs, before `ui_server.py`'s C3 edits
  landed, correctly still showed the three `POST`/`PUT`/`DELETE` sections failing, and after they
  landed showed only the one expected, pre-C4 failure — the stale generated page section);
  `tests/ui_server/test_command_channel.py` (110 passed, once C3's walk changes were written);
  `python3 -m ruff check` on the touched files (clean each time).
- `write_public_api_page()` run once from the repository root via a `python3` script that captured
  its own exit code (per the block's constraint on scripts over compound shell): exit 0, empty
  stdout and stderr.
- `git push -u origin feature/f253-public-http-api`, once, after this commit: reported in the
  worker's reply, not here (Rule A4: this file is written before the push).
- No full suite, no mutation, no worktree, no merge, no new branch, no force-push, no pull, no
  checkout or switch away from the feature branch, no `REMEDY_TEST_MAX_WORKERS`, no `-n`.

## Verification

0. Digests: all five prepared files under `.remedy-wt/f253-r3/` matched their sha256 (Python
   `hashlib`, 5 of 5 True; `block.md` 216 lines, sha256
   `38c5e574a05f6407815ff7caec043388978188b6f981f498871b97359ee92943`).
1. C1: every append proved "post equals pre plus slice" in bytes (live_review, prose_slips,
   decisions — three of three True, decisions.md never read whole), the authored copy byte-equal
   to `block.md`, and the plan copy byte-equal to `dry-plan.md` (5 of 5 True in total). `git diff
   --cached --numstat` read `216 0`, `10 0`, `6 0`, `15 14`, `1 0`. The staged diff (312 lines) was
   written to a file and read whole as the self-review.
2. C2: the staged diff (401 lines) was written to a file and read whole as the self-review; single
   runs during writing are in External actions above.
3. C3: the staged diff (242 lines) was written to a file and read whole as the self-review.
4. C4: `write_public_api_page()`'s run is in External actions above. The staged diff (82 lines) was
   written to a file and read whole as the self-review.
5. **Gate 1** (after C4, before C5): `git -C /home/decodeux/Repos/remedy status --porcelain` —
   empty. The C1 byte proofs, re-run against the committed tree: all True (`authored_copy_byte_equal
   True`, `live_review_post_equals_pre_plus_slice True`, `prose_slips_post_equals_pre_plus_slice
   True`, `decisions_post_size_equals_pre_plus_slice_size True`,
   `decisions_post_hash_equals_pre_plus_slice_hash True`, `plan_copy_byte_equal True`).
6. **Gate 2**, from the primary checkout, once:

       python3 -m pytest -q -rfEs tests/ui_server/test_public_api.py tests/ui_server/test_command_channel.py tests/orchestration/test_serve_daemon.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/cli/test_change_proof_cli.py tests/cli/test_client_interface.py tests/docs/ tests/cli/test_golden_path.py

   exit 0, `642 passed in 99.86s`, no FAILED, ERROR or SKIPPED line.
7. **Gate 3**:

       python3 -m ruff check packages/orchestration/public_api.py packages/orchestration/ui_server.py tests/ui_server/test_public_api.py tests/ui_server/test_command_channel.py

   exit 0, `All checks passed!`.
8. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`,
   `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`,
   `repo_root_hygiene` and `high_blockers_open` all `pass`, `"fail_count": 0`, `"ok": true`.
9. **Gate 5** (`python3 -c "import scripts.rotate_live_review as r;
   print(r.open_finding_ids(open('.agent/live_review.md').read()))"`): exit 0,
   `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162',
   'R-1172', 'R-1176', 'R-1187', 'R-1188']`.
10. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r3.md`: 216 lines, byte-equal, sha256
  `38c5e574a05f6407815ff7caec043388978188b6f981f498871b97359ee92943` (Verification item 0 and 1).
- `append-live_review.txt`, `append-prose_slips.txt`, `append-decisions.txt` appended to their base
  blobs at `a274e5fb7`: each "post equals pre plus slice" True (Verification item 1); `decisions.md`
  never read whole, per the block.
- `dry-plan.md` to `.agent/plan.md`: byte-equal (Verification item 1).
- `docs/system/public-http-api-v1.md`'s generated section equal to `render_public_api_markdown()`:
  proved by `tests/ui_server/test_public_api.py::test_the_pages_generated_section_equals_the_rendering`,
  part of Gate 2's green run.

## Deviations & assumptions

None. C1 through C4 landed in the order and under the subjects the block gave, touching only the
paths it named for each commit. The gates ran in the block's order, once each, after C4 and before
this commit.

## Round verdicts

Round 2's PASS, R-1187's recurrence and R-1188's registration are booked by this round's C1.
Round 3's verdict is the reviewer's.

## For the operator, in plain sentences

The second round's work passed review, with two small gaps the review found and this round
repaired. A program can now read the proof of one job over the web interface, exactly as the
command line shows it, and gets the same refusal with a fitting web status when the job does not
exist or its short id fits more than one job. A request that tries to change something where the
interface only reads is now refused in the interface's own format and written to its log like
every other request. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then the Open PR Gate.
3. Then book round 3's verdict in the next round's first commit.
4. Then S3: what changed since a cursor.

Operator questions open: 0.
Open findings: 13 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172, R-1176, R-1187 and R-1188, Low; R-1187 and R-1188 owned by F253 and repaired in this round,
awaiting the reviewer's resolution; the rest owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 2, R-1187's recurrence, register R-1188, DECISION F253 D3, the plan and the block | done | `da9e33a3e` |
| C2: `GET /api/v1/jobs/{job}/proof`, named path segments and each route's refusal statuses | done | `352e1d17b` |
| C3: `POST`/`PUT`/`DELETE` answer `api_method_not_allowed` and are ledgered (R-1188) | done | `026f65563` |
| C4: the page and R-1187's recurrence repair | done | `a0e359340` |
| Gates 1 to 5 | done | all green, run once each, before this file was written |
| C5: this handback | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
