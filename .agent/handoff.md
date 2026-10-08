# Handoff — F253 round 5: book round 4, R-1189/R-1190, DECISION F253 D5, and S3b: `GET /api/v1/changes`

## Session

SESSION 1 of feature F253 · round 5 · rounds so far 5

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~40 % (S1 to S3 · S4 to S7 open) — Schätzung

## Range

Review of `7726b184b5575ba8779999548d2eed7c4b3d8d51`..HEAD (HEAD is C5 below, which carries this
handback and is the last commit on the branch).

## Commits

### 8aaaa957f F253 R5 C1: book round 4, register R-1189 and R-1190, DECISION F253 D5, the operator's note, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r5.md` | 174/0 | new file, byte copy of `block.md` |
| `.agent/decisions.md` | 10/0 | `append-decisions.txt`'s bytes appended: DECISION F253 D5 |
| `.agent/live_review.md` | 6/0 | `append-live_review.txt`'s bytes appended: round 4's gate entry and R-1189's and R-1190's registrations |
| `.agent/operator_questions.md` | 23/1 | `dry-operator_questions.md`, byte for byte: Q10, the stray test records |
| `.agent/plan.md` | 12/12 | `dry-plan.md`, byte for byte |

### bea065b85 F253 R5 C2: tests that a restricted digest lists an ended job and that a run-log change alone lists a job (R-1189, R-1190)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_client_digest.py` | 13/0 | `test_build_client_digest_restricted_to_an_ended_job_lists_it_outside_the_ended_job_window`: a `job_ids`-restricted call on a job that has ended (terminal, not awaiting apply, no open decision) lists it in `jobs`, `job_window` null and 0 (R-1189) |
| `tests/orchestration/test_client_changes.py` | 24/0 | `test_a_job_whose_run_log_alone_changed_is_listed_by_build_client_changes`: a job whose `job.json` predates the cursor but whose run log gains an event after it (via `packages/orchestration/timeline.py`'s own `append_run_event`) is listed only after the event is appended (R-1190) |

No production file changed in this commit, as the block required.

### c3fe32384 F253 R5 C3: GET /api/v1/changes, twinned with remedy client changes, with the first query key that takes a value (S3b, DECISION F253 D5)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/client_cmd.py` | 6/3 | `_cmd_client_changes`'s refusal message moved into `client_cursor_refusal_message`, imported and called; the `fail("invalid_cursor", ..., exit_code=2)` call stays in the handler |
| `packages/orchestration/client_changes.py` | 7/0 | `client_cursor_refusal_message(value: str) -> str`, the sentence the command and its HTTP twin both send for a cursor `parse_client_cursor` cannot read |
| `packages/orchestration/public_api.py` | 70/18 | `PUBLIC_API_VERSION` to `1.3`; `PublicApiRoute` gains `query_values`; the query check of `answer_public_api_get` accepts one non-empty value per declared `query_values` key, refuses a repeated or empty one or an undeclared key with `api_query_invalid`; fourth route `GET /api/v1/changes`, twin `client.changes`, `query_values=("since",)`, `refusals=(("invalid_cursor", 400),)`, answered by the new `_client_changes_answer`; the page renderer's Query column renders a value key as `` `key=<value>` `` |
| `tests/ui_server/test_public_api.py` | 64/0 | `PINNED_ROUTES` gains the changes route; `test_every_route_is_well_formed` holds every `query_values` key to a twin option that takes a value; `test_changes_route_answers_the_client_changes_command`: the route equals `remedy client changes --json` with no cursor, with a cursor before the seeded job, and with `yesterday` (200, 200, 400), plus `since=` and `since=a&since=b` answering 400 `api_query_invalid` |

### 4f0690d17 F253 R5 C4: the page names the changes route and query keys that take a value

| Path | +/- | Reason |
|---|---|---|
| `docs/system/public-http-api-v1.md` | 16/6 | hand-written part: a query key is either a flag or a value key written `key=<value>`, given at most once, never empty, else 400 `api_query_invalid`; new "Staying current" section on reading the digest once and following the changes route with each answer's cursor; generated section rewritten by `write_public_api_page()` (version `1.3`, the new route's row) |
| `tests/ui_server/test_public_api.py` | 6/0 | `test_the_page_states_the_changes_route_and_the_value_query_key`: `/api/v1/changes` and `since=<value>` are on the page |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |

## External actions

- Preconditions, before any write: `git rev-parse HEAD` read `7726b184b5575ba8779999548d2eed7c4b3d8d51`,
  equal to `git rev-parse origin/feature/f253-public-http-api`; `git status --porcelain` was empty;
  `.agent/STOP` was absent; the five prepared files under `.remedy-wt/f253-r5/` (`append-decisions.txt`,
  `append-live_review.txt`, `block.md`, `dry-operator_questions.md`, `dry-plan.md`) matched their
  sha256 in `digests.txt` (Python `hashlib`, 5 of 5 True; `block.md` 174 lines, sha256
  `f1bc56ec2e45b6e662d317eb510856a114560114d8eff78f67d5f59a79444d3b`); `git branch --show-current`
  read `feature/f253-public-http-api` before every commit.
- Single test runs while writing C2 to C4, one at a time, none of them the round's gate-2 selection
  as a WHOLE: `tests/orchestration/test_client_digest.py` (74 passed) and
  `tests/orchestration/test_client_changes.py` (13 passed) after C2; `tests/ui_server/test_public_api.py`
  (40 passed, 1 expected failure — `test_the_pages_generated_section_equals_the_rendering`, red
  because C4 had not yet regenerated the page) and `tests/cli/test_client_changes_cmd.py` plus
  `tests/cli/test_client_interface.py` (71 passed) after C3; `tests/ui_server/test_public_api.py`
  again after C4 (42 passed, the generated-section test now green); ruff on every touched Python
  file after each commit (clean each time).
- `write_public_api_page()` run once from the repository root via a `python3` script that captured
  its own exit code: exit 0, no stdout, no stderr.
- `git push -u origin feature/f253-public-http-api`, once, after this commit: reported in the
  worker's reply, not here (Rule A4: this file is written before the push).
- No full suite, no mutation, no worktree, no merge, no new branch, no force-push, no pull, no
  checkout or switch away from the feature branch, no `REMEDY_TEST_MAX_WORKERS`, no `-n`.

## Verification

0. Digests: all five prepared files under `.remedy-wt/f253-r5/` matched their sha256 in
   `digests.txt` (Python `hashlib`, 5 of 5 True).
1. C1: `authored_copy_byte_equal True`, `live_review_post_equals_pre_plus_slice True`,
   `decisions_post_size_equals_pre_plus_slice_size True`,
   `decisions_post_hash_equals_pre_plus_slice_hash True` (`decisions.md` never read whole, streamed
   through `hashlib` in 1 MiB chunks), `plan_copy_byte_equal True`,
   `operator_questions_copy_byte_equal True` — 6 of 6. `git diff --cached --numstat` read `174 0`,
   `10 0`, `6 0`, `23 1`, `12 12`. The staged diff (290 lines) was written to a file and read whole
   as the self-review.
2. C2: the staged diff (59 lines) was written to a file and read whole as the self-review; single
   runs during writing are in External actions above.
3. C3: the staged diff (306 lines) was written to a file and read whole as the self-review.
4. C4: `write_public_api_page()`'s run is in External actions above. The staged diff (70 lines) was
   written to a file and read whole as the self-review.
5. **Gate 1** (after C4, before C5): `git -C /home/decodeux/Repos/remedy status --porcelain` —
   empty. The C1 byte proofs, re-run against the committed tree via `git show` (streamed for
   `decisions.md`, never read whole): all True (same six booleans as item 1).
6. **Gate 2**, from the primary checkout, once:

       python3 -m pytest -q -rfEs tests/ui_server/test_public_api.py tests/ui_server/test_command_channel.py tests/orchestration/test_client_changes.py tests/orchestration/test_client_digest.py tests/cli/test_client_changes_cmd.py tests/cli/test_client_interface.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/docs/ tests/cli/test_golden_path.py

   exit 0, `691 passed in 93.96s`, no FAILED, ERROR or SKIPPED line.
7. **Gate 3**:

       python3 -m ruff check tests/orchestration/test_client_digest.py tests/orchestration/test_client_changes.py apps/cli/commands/client_cmd.py packages/orchestration/client_changes.py packages/orchestration/public_api.py tests/ui_server/test_public_api.py

   exit 0, `All checks passed!`.
8. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`,
   `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`,
   `repo_root_hygiene` and `high_blockers_open` all `pass`, `"fail_count": 0`, `"ok": true`.
9. **Gate 5** (`python3 -c "import scripts.rotate_live_review as r;
   print(r.open_finding_ids(open('.agent/live_review.md').read()))"`): exit 0,
   `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162',
   'R-1172', 'R-1176', 'R-1189', 'R-1190']`.
10. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r5.md`: 174 lines, byte-equal, sha256
  `f1bc56ec2e45b6e662d317eb510856a114560114d8eff78f67d5f59a79444d3b` (Verification items 0 and 1).
- `append-live_review.txt` and `append-decisions.txt` appended to their base blobs at `7726b184b`:
  each "post equals pre plus slice" True (Verification item 1); `decisions.md` never read whole,
  per the block.
- `dry-plan.md` to `.agent/plan.md` and `dry-operator_questions.md` to `.agent/operator_questions.md`:
  byte-equal (Verification item 1).
- `docs/system/public-http-api-v1.md`'s generated section equal to `render_public_api_markdown()`:
  proved by `tests/ui_server/test_public_api.py::test_the_pages_generated_section_equals_the_rendering`,
  part of Gate 2's green run.

## Deviations & assumptions

None. C1 through C4 landed in the order and under the subjects the block gave, touching only the
paths it named for each commit. The gates ran in the block's order, once each, after C4 and before
this commit. No commit's insertions passed 500 (the largest, C3, was 147 total across its four
files, well under the cap), so none needed splitting.

## Round verdicts

Round 4's PASS and the registrations of R-1189 and R-1190 are booked by this round's C1.
Round 5's verdict is the reviewer's.

## For the operator, in plain sentences

The fourth round's work passed review, and two missing tests it found are added. A program can now
ask the web interface what changed since its last look, with the same answer the command line
gives. One early draft of a test in the fourth round wrote a small practice project, mission and
job into the operator's real data folder, which the loop has not deleted, and the question file
says where they are and that leaving them does no harm. One operator question is open.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then the Open PR Gate.
3. Then book round 5's verdict in the next round's first commit.
4. Then S4: answer a decision, approve an apply, decline a result, through the F009 door.

Operator questions open: 1.
Open findings: 13 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172, R-1176, R-1189 and R-1190, Low; R-1189 and R-1190 owned by F253 and repaired in this round,
awaiting the reviewer's resolution; the rest owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 4, register R-1189 and R-1190, DECISION F253 D5, the operator's note, the plan and the block | done | `8aaaa957f` |
| C2: tests that a restricted digest lists an ended job and that a run-log change alone lists a job | done | `bea065b85` |
| C3: `GET /api/v1/changes`, twinned with `remedy client changes` | done | `c3fe32384` |
| C4: the page names the changes route and query keys that take a value | done | `4f0690d17` |
| Gates 1 to 5 | done | all green, run once each, before this file was written |
| C5: this handback | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
