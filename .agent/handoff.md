# Handback — F307 round 18: book round 17 with R-1313; T009, the public API's refusals: R-1303, R-1304, R-1308, R-1309 and R-1305

## Session

SESSION 4 of feature F307 · round 18 · rounds so far 18

Context self-assessment: this worker verified every prepared digest before any write, applied C1 through a byte-proof script and C2 to C4 as the prepared patches without a hand edit, read each staged diff before committing, and ran each gate once; context is ample and nothing was lost.

Session end (the reviewer, after its verdict on round 18): this session ran six delegated rounds, 13 to 18, inside the target of six to eight, and closed T005, T006, T008 and T009; it ends here because the next slice, T013, changes keys of the machine client interface and may remove one, which a fresh session should plan whole. One finding of the reviewer's own making, R-1416, was registered and repaired this session; no prose slip was written. Context self-assessment: ample, and the method of building every product commit by script in the disposable dry tree and comparing the worker's commit by bytes held in all six rounds.

Fortschritt: ~78 % (T001 to T006, T008 to T011, T014, R-1280, R-1290, R-1292, R-1297, R-1298, R-1301, R-1414, R-1415 and R-1416 landed, R-1281's writer part landed · the rest open) — Schätzung

## Range

Review of `9d0f2d39a`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### 9f9ecd23a F307 R18 C1: book round 17 with R-1313, DECISION F307 D18, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r18.md` | 95/0 | NEW FILE, this round's block, byte copy (95 lines, sha256 `3365c8b48aa6acb60e2d1cf8d725982043d6f7edb3185471ddb98b2b0b1fbc16`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared slice appended (DECISION F307 D18) |
| `.agent/live_review.md` | 4/0 | prepared slice appended (round 17's Gate verdict PASS, R-1313 done) |
| `.agent/plan.md` | 8/8 | replaced with the prepared file |

119 insertions, 8 deletions over 4 files (`git show --shortstat`).

### 1fc1fab05 F307 R18 C2: PATCH, HEAD and OPTIONS under the public API are refused by name with a ledger line, and the server names itself Remedy (R-1303, R-1304)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/ui_server.py` | 13/15 | one `_refuse_public_api_method` for PUT, DELETE, PATCH, HEAD, OPTIONS; `version_string` answers `Remedy` |
| `packages/orchestration/serve_daemon.py` | 6/28 | the public port forwards all seven methods through one method |
| `packages/orchestration/public_api.py` | 12/9 | `public_api_method_refusal` takes the method and names it; version comment |
| `docs/system/public-http-api-v1.md` | 8/6 | the refused methods and the `Server` header |
| `docs/system/api-release-matrix-v1.json` | 12/0 | two value changes of 1.27 |
| `docs/system/structure-ledger-v1.md` | 1/1 | `ui_server.py` row 1826 to 1824 |
| `tests/test_structure_ratchet.py` | 1/1 | `MAX_FILE_LINES` lowered by 2 |
| `tests/ui_server/test_public_api.py` | 30/0 | method named, ledger lines, `Server: Remedy` |
| `tests/orchestration/test_serve_daemon.py` | 1/1 | PATCH and OPTIONS added to the not-served parametrization |

84 insertions, 61 deletions over 9 files (`git show --shortstat`).

### 341cb6057 F307 R18 C3: a bad query value gets its own sentence and every route refuses a path value that leaves its place (R-1308, R-1309)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/public_api.py` | 31/18 | `_path_value_refusal` shared by GET and POST; the query loop gives a declared key its own sentence |
| `docs/system/public-http-api-v1.md` | 4/1 | the query message and `api_path_invalid` on every route |
| `docs/system/api-release-matrix-v1.json` | 12/0 | two value changes of 1.27 |
| `docs/system/structure-ledger-v1.md` | 1/1 | `answer_public_api_post` row 157 to 151 |
| `tests/test_structure_ratchet.py` | 1/1 | `MAX_FUNCTION_LINES` lowered by 6 |
| `tests/ui_server/test_public_api.py` | 33/6 | new query and path tests; the two `..%2Fx` tests expect the 400 refusal |

82 insertions, 27 deletions over 6 files (`git show --shortstat`).

### 569be24b1 F307 R18 C4: the changes route says when a job's cost fields refresh (R-1305)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/public_api_routes.py` | 3/1 | the changes route's description |
| `packages/orchestration/client_changes.py` | 5/0 | module docstring: the cost ledger is deliberately not watched |
| `docs/system/public-http-api-v1.md` | 1/1 | generated page row |
| `tests/ui_server/test_public_api.py` | 8/0 | route and page carry the sentence |

17 insertions, 2 deletions over 4 files (`git show --shortstat`).

### (this commit) F307 R18 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | HEAD and `origin/feature/f307-findings-paydown-v9` both `9d0f2d39acfc482d3952f43b32098aebb546143e`, tree clean, no pull run, no `.agent/STOP` |
| C1 | done | commit `9f9ecd23a`, 119 insertions, byte proofs all held |
| C2 | done | commit `1fc1fab05`, 84 insertions, patch applied without a hand edit |
| C3 | done | commit `341cb6057`, 82 insertions, patch applied without a hand edit |
| C4 | done | commit `569be24b1`, 17 insertions, patch applied without a hand edit |
| C5 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty |
| Gate 2 | done | `ruff over 8 files: exit 0`, `All checks passed!` |
| Gate 3 | done | `paths 98`, `exit 0`, `4347 passed, 2 skipped in 83.39s` |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | `23` |
| Gate 6 | done | `git diff --stat 202ce9053 HEAD -- packages apps scripts tests docs` empty |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

None before this commit; the push follows it and is reported in the session reply. `.remedy-wt/f307-r18-worker/` (created this round) holds the digest check, the C1 byte-proof, the gate-4 script, the five commit-message files and the selection output. No provider call.

## Verification

1. Digests, before any write: `digests.txt` sha256 `6f65bf65fbe21ff34a04225adce2fb8ca18292e8a94c6f96283f83279f7c9d49` and `block.md` sha256 `3365c8b48aa6acb60e2d1cf8d725982043d6f7edb3185471ddb98b2b0b1fbc16` (95 lines) both equal the delivering prompt; the ten other listed entries matched (by a python3 script, since `digests.txt` is tab-separated).
2. C0: branch `feature/f307-findings-paydown-v9`; HEAD equals `origin/feature/f307-findings-paydown-v9` at `9d0f2d39acfc482d3952f43b32098aebb546143e`; tree clean.
3. Gate 1: `git -C <root> status --porcelain` — empty (read after C4).
4. Gate 2: `python3 .remedy-wt/f307-r18/prep/ruff_touched.py <root>` — `ruff over 8 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r18/prep/run_selection.py <root> .remedy-wt/f307-r18-worker/selection-output.txt` — `paths 98`, `exit 0`, `4347 passed, 2 skipped in 83.39s (0:01:23)`. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175` (opt-in, `REMEDY_INSTALL_SMOKE=1`). No FAILED, ERROR or "process(es) behind" line.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` via a python3 script with `cwd=<root>` — exit 0, `fail_count` 0; `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open` all pass.
7. Gate 5: `python3 .remedy-wt/f307-r10/open_count.py <root>` — `23`.
8. Gate 6: `git -C <root> diff --stat 202ce9053 HEAD -- packages apps scripts tests docs` — empty.

## Authored-text proofs

`.agent/authored/f307-r18.md` equals `block.md`: 95 lines, sha256 `3365c8b48aa6acb60e2d1cf8d725982043d6f7edb3185471ddb98b2b0b1fbc16` on both sides. The `.agent/live_review.md` and `.agent/decisions.md` appends (each equal to pre-image plus slice) and the `.agent/plan.md` replacement were each proved byte for byte by one script right after writing. `c2.patch`, `c3.patch` and `c4.patch` were each applied unchanged after `git apply --check`; gate 6 shows the committed product bytes equal the reviewer's dry run.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1 to C5), each touching only its named paths. No mutation red-proof, no full suite, `REMEDY_TEST_MAX_WORKERS` never set, `.data` never read, no amend, rebase, force-push or `--no-verify`, no PR; each gate ran once and never concurrently. Two shell calls were refused by the sandbox before running (a heredoc and a `$?` reference) and were re-issued differently; nothing was written by them.

## Reviewer verdict of round 18 (carried here under amend0827 rule 1)

VERDICT PASS. Book these six paragraphs byte for byte, each preceded by one empty line, at the end of
`.agent/live_review.md` in the next round's first commit:

Gate: F307 R18 — the F307 round 18 entry, over `9d0f2d39a`..`a3b434c8c` (5 commits, each single-parent; insertions by `git show --shortstat`: `9f9ecd23a` 119, `1fc1fab05` 84, `341cb6057` 82, `569be24b1` 17, `a3b434c8c` 70). VERDICT PASS, verified by dry run, bytes identical: the product trees of `1fc1fab05`, `341cb6057` and `569be24b1` equal the reviewer's dry-run commits `107b09827`, `48e41de1c` and `202ce9053`, the ledger and the decisions file each equal their pre-image plus the prepared slice, and the plan and the saved block equal the prepared files. In a disposable worktree at `202ce9053`, eleven mutations each turned their tests red: PATCH, HEAD or OPTIONS left unrefused, the `Server` header naming Python again, every method given the supervisor's sentence, the handler naming no method, the public port not forwarding PATCH, an empty value or a bad flag given the unknown-key sentence, a GET skipping the path check, and the changes route saying nothing of the cost ledger. The selection, every test file that names a touched module by import or by path (98 paths), read `4347 passed, 2 skipped` with exit 0, the worker's one run the same; ruff read clean over the eight Python files, the integrity check `fail_count` 0, and the open set 23 ids.

Done: R-1303 — RESOLVED at F307 R18 by `1fc1fab05`: `test_a_refused_method_is_named_and_never_sent_to_the_supervisor`, `test_patch_head_and_options_are_refused_and_each_writes_its_ledger_line` and `test_every_answer_names_its_server_as_remedy_only`, in `tests/ui_server/test_public_api.py`, through a real HTTP server, and `test_the_api_port_answers_every_cockpit_only_path_404` in `tests/orchestration/test_serve_daemon.py` for PATCH and OPTIONS on the supervisor's port. RED BEFORE: in a disposable worktree at `202ce9053`, PATCH, HEAD and OPTIONS each left unrefused, the `Server` header naming Python again and the public port not forwarding PATCH each turned one red. GREEN AFTER: the selection read `4347 passed, 2 skipped` at `202ce9053`.

Done: R-1304 — RESOLVED at F307 R18 by `1fc1fab05`: `test_a_refused_method_is_named_and_never_sent_to_the_supervisor`, for PUT, PATCH and OPTIONS. RED BEFORE: in a disposable worktree at `202ce9053`, every method given the supervisor's sentence and the handler naming no method each turned it red. GREEN AFTER: the selection read `4347 passed, 2 skipped` at `202ce9053`.

Done: R-1308 — RESOLVED at F307 R18 by `341cb6057`: `test_a_query_key_given_empty_or_as_a_bad_flag_is_refused_with_its_own_sentence`. RED BEFORE: in a disposable worktree at `202ce9053`, an empty value and a bad flag each given the unknown-key sentence turned it red. GREEN AFTER: the selection read `4347 passed, 2 skipped` at `202ce9053`.

Done: R-1309 — RESOLVED at F307 R18 by `341cb6057`: `test_a_get_refuses_a_path_value_that_leaves_its_place`, through a real HTTP server, and the two poll-route tests that now expect the refusal. RED BEFORE: in a disposable worktree at `202ce9053`, a GET skipping the path check turned all three red. GREEN AFTER: the selection read `4347 passed, 2 skipped` at `202ce9053`.

Done: R-1305 — RESOLVED at F307 R18 by `569be24b1`, by the finding's second repair (DECISION F307 D18 (5)): `test_the_changes_route_says_when_a_jobs_cost_fields_refresh`. RED BEFORE: in a disposable worktree at `202ce9053`, the route's sentence removed turned it red. GREEN AFTER: the selection read `4347 passed, 2 skipped` at `202ce9053`.

## Scoping note for T013 (the reviewer, for the next session)

- R-1282 asks that the digest's mission entry name its orders and each job entry its order. In
  `packages/orchestration/client_digest.py`, `build_client_digest` is a listed function whose steps
  (1) to (3) are done; the mission entry `_mission_entry` and the job entry `_job_entry` are where
  the change lands. Check whether either is listed before planning a structural step.
- The keys reach the machine client interface: `DIGEST_KEY_TREE` and `ANSWER_KEY_TREES` in
  `apps/cli/client_interface.py`. The interface stands at 1.27, still unreleased on this branch, so
  an added key is recorded as an `added` entry of 1.27 in `docs/system/api-release-matrix-v1.json`,
  and the generated page is rewritten by `write_client_interface_page`.
- DECISION F307 D8 moved R-1311's `plan_source` to T013: the key `plan_source` under a mission's
  `orders` leaves the interface, which is a removal. The matrix's rule reads "nothing was removed or
  renamed between 1.17 and 1.27"; decide how a removal is recorded, as a DECISION, before the round.
- The method this session used: each product commit built by a script in the disposable dry tree
  `.remedy-wt/f307-r10-dry`, the round's selection generated from every test file that names a
  touched module by import, module alias or file path (R-1416), the mutations run in a worktree of
  their own, and the worker given the patches to apply. The scripts are under
  `.remedy-wt/f307-r13/` to `.remedy-wt/f307-r18/`.

## For the operator, in plain sentences

A program that asks Remedy's web interface for something it does not offer now always gets a short machine-readable refusal saying what was wrong, and every such request is written to the interface's log; the server no longer tells callers which Python version it runs on; and the description of the "what changed" read now says that a job's cost figures refresh when the job itself changes.

This working session finished four groups of repairs. A backup model that stands in for the usual one now records its work beside the usual model's record, is counted as the extra call it really is, and stops when the run stops. Every line of Remedy's operations log now names the job and the run it belongs to. A broken settings file is reported as the user's file, not as a crash of Remedy's own. And the web interface refuses every request it does not offer in one clear way. About three quarters of this batch of repairs is done; the rest continues in the next session.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Round 18 is reviewed (PASS): book the six paragraphs of the section "Reviewer verdict of round 18" above in
   the next round's first commit.
4. T013, R-1282 with `plan_source`, per the scoping note above; then T015 to T020, T021 and the closure
   sequence.

Operator questions open: 0. Open findings count gate 5 printed: 23; it reads 18 once round 18's five
resolutions are booked.
