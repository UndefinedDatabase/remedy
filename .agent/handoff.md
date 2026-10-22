# Handback — F307 round 22: book round 21 with R-1332; _cmd_job_run's step (1); command_catalog's step (7); R-1331, the retry of a blocked job

## Session

SESSION 6 of feature F307 · round 22 · rounds so far 22

Context self-assessment: this worker verified every prepared digest before any write, applied C1 by a byte-proof script, applied C2, C3 and C4 by `git apply` from the reviewer's cut patches with no hand-retyping, read each staged diff in full against its patch before committing, and ran each gate once; context is ample and nothing was lost.

Fortschritt: ~88 % (T001 to T006, T008 to T011, T013 to T015, R-1280, R-1290, R-1292, R-1297, R-1298, R-1301, R-1332, R-1414 to R-1417 landed, R-1281's writer part landed, R-1331 under review · the rest open) — Schätzung

## Range

Review of `d241ed7d0`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### cf5a9713f F307 R22 C1: book round 21 with R-1332, DECISION F307 D22, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r22.md` | 89/0 | NEW FILE, this round's block, byte copy (89 lines, sha256 `6b88cdc17f4e046e52679e723c08301e432922940b4494f1a9133e4dbd41feed`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared slice appended (DECISION F307 D22) |
| `.agent/live_review.md` | 4/0 | prepared slice appended (round 21's Gate verdict PASS, R-1332 RESOLVED) |
| `.agent/plan.md` | 6/8 | replaced with the prepared file |

111 insertions, 8 deletions over 4 files (`git show --shortstat`).

### 0f0989cde F307 R22 C2: the refusals of job run before anything runs become one function, structural step (1)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/do_cmd.py` | 5/27 | `_cmd_job_run`'s refusals before anything runs replaced by one call to `refuse_job_run_before_it_starts`; falls from 205 to 183 lines |
| `apps/cli/commands/job_run_refusals.py` | 44/5 | `refuse_job_run_before_it_starts` added (step (1) of `_cmd_job_run`'s boundary), module docstring updated |
| `docs/system/structure-ledger-v1.md` | 3/2 | step (1) marked done; the function-row table's `_cmd_job_run` line updated to 183 |
| `tests/test_structure_ratchet.py` | 1/1 | `MAX_FUNCTION_LINES` lowered from 28683 to 28661 |

53 insertions, 35 deletions over 4 files (`git show --shortstat`); applied from `c2.patch`, not hand-retyped.

### c1888bd3e F307 R22 C3: the job run entry moves to a catalog module of its own, structural step (7)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog.py` | 2/40 | the `job.run` `CommandEntry` replaced by `*JOB_RUN_COMMANDS`, spliced at its own place; import added |
| `apps/cli/command_catalog_job_run.py` | 53/0 | NEW FILE — `JOB_RUN_COMMANDS`, the `job run` entry moved unchanged |
| `docs/system/structure-ledger-v1.md` | 3/2 | step (7) marked done; the file-row table's `command_catalog.py` line updated from 2293 to 2255 |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | `apps.cli.command_catalog_job_run` registered |
| `tests/test_structure_ratchet.py` | 1/1 | `MAX_FILE_LINES` lowered from 63105 to 63067 |

60 insertions, 43 deletions over 5 files (`git show --shortstat`); applied from `c3.patch`, not hand-retyped.

### 952ca8898 F307 R22 C4: a retry puts a blocked job's stuck tasks back to pending and runs them again (R-1331)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog_job_run.py` | 2/0 | `--retry` flag added to the `job.run` entry's args |
| `apps/cli/commands/do_cmd.py` | 9/8 | `_cmd_job_run` gains a `retry: bool = False` parameter (signature lines joined to hold the row), calls `retry_blocked_job_tasks` before the run when set; `COMMAND_HANDLERS["job.run"]` passes it through |
| `docs/system/api-release-matrix-v1.json` | 9/1 | route `POST /api/v1/jobs/{job}/retry` and `--retry` added at 1.27; story `next` value-change entry |
| `docs/system/machine-client-contract-v1.md` | 1/0 | `--retry` row added to `job run`'s option table |
| `docs/system/public-http-api-v1.md` | 17/5 | `POST /api/v1/jobs/{job}/retry` documented; `retry` story word's paragraph rewritten; route table row added |
| `packages/orchestration/client_story.py` | 9/5 | `_next` gains a `retryable` parameter; returns `retry`/`POST .../retry` for a `failed` state when `job_is_retryable` |
| `packages/orchestration/client_story_words.py` | 2/2 | comment above `STORY_NEXT_ACTIONS` rewritten to describe `retry`'s new route |
| `packages/orchestration/job_retry.py` | 53/0 | NEW FILE — `retry_blocked_job_tasks`, resets a blocked job's stuck/skipped-after tasks to pending, respecting the veto fold |
| `packages/orchestration/job_run_ending.py` | 8/0 | `job_is_retryable` added, the one reading of "blocked with a stuck task" |
| `packages/orchestration/public_api.py` | 5/3 | `_start_run_answer` prefixes the matched route's `run_options` (e.g. `--retry`) before the body-derived options |
| `packages/orchestration/public_api_routes.py` | 22/2 | `run_options` field added to `PublicApiRoute`; new route `POST /api/v1/jobs/{job}/retry` registered with `run_options=("--retry",)` |
| `tests/cli/test_do_verified_repair.py` | 2/1 | story's `next.action` assertion updated from `none` to `retry` |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | `packages.orchestration.job_retry` registered |
| `tests/orchestration/test_blocked_job_rerun.py` | 1/1 | docstring updated to describe `--retry` rather than the old (incorrect) retry-is-the-run-route claim |
| `tests/orchestration/test_client_story.py` | 14/4 | renamed/rewritten test for a retryable failed job's `next`; new test for a job failed for good offering `none` |
| `tests/orchestration/test_do_then_story.py` | 24/11 | renamed/rewritten end-to-end gate test: a plain run re-attempts nothing, the retry route runs the stuck task and the job ends done |
| `tests/orchestration/test_job_retry.py` | 141/0 | NEW FILE — unit and CLI-level tests for `retry_blocked_job_tasks` and `remedy job run <job> --retry` |
| `tests/ui_server/test_public_api.py` | 30/0 | pinned-route entry and two new tests for the retry route's shape and its `run_options` ordering |

350 insertions, 43 deletions over 18 files (`git show --shortstat`); applied from `c4.patch`, not hand-retyped.

### (this commit) F307 R22 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | HEAD and `origin/feature/f307-findings-paydown-v9` both `d241ed7d0fb4a9c39020800f7892dea942140a27`, tree clean, no pull run, no `.agent/STOP` |
| C1 | done | commit `cf5a9713f`, 111 insertions, byte proofs all held |
| C2 | done | commit `0f0989cde`, 53 insertions, applied from `c2.patch` |
| C3 | done | commit `c1888bd3e`, 60 insertions, applied from `c3.patch` |
| C4 | done | commit `952ca8898`, 350 insertions, applied from `c4.patch` |
| C5 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty |
| Gate 2 | done | `ruff over 17 files: exit 0`, `All checks passed!` |
| Gate 3 | done | `paths 213`, `exit 0`, `8901 passed, 2 skipped in 175.85s` |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | `14` |
| Gate 6 | done | `git diff --stat 9b2767154 HEAD -- packages apps scripts tests docs` empty |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

None before this commit; the push follows it and is reported in the session reply. `.remedy-wt/f307-r22-worker/` (created this round) holds the digest-verification script, the C1 byte-proof script, the integrity-check script, the four commit-message files and the selection output. No provider call.

## Verification

1. Digests, before any write: `digests.txt` sha256 `fb544b052c4476719872e499a1ce7de1c1ee18844f328db334340fde40a1c964` and `block.md` sha256 `6b88cdc17f4e046e52679e723c08301e432922940b4494f1a9133e4dbd41feed` (89 lines) both equal the delivering prompt; the nine other listed entries (`c1-.agent__plan.md`, `c1-decisions-append.txt`, `c1-live_review-append.txt`, `c2.patch`, `c3.patch`, `c4.patch`, `ruff_touched.py`, `run_selection.py`, `selection.txt`) matched (by a python3 script, since `digests.txt` is tab-separated).
2. C0: branch `feature/f307-findings-paydown-v9`; HEAD equals `origin/feature/f307-findings-paydown-v9` at `d241ed7d0fb4a9c39020800f7892dea942140a27`; tree clean.
3. Gate 1: `git -C <root> status --porcelain` — empty (read after C4, before C5).
4. Gate 2: `python3 .remedy-wt/f307-r22/prep/ruff_touched.py <root>` — 17 touched files listed, `ruff over 17 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r22/prep/run_selection.py <root> .remedy-wt/f307-r22-worker/selection-output.txt` — `paths 213`, `exit 0`, `8901 passed, 2 skipped in 175.85s (0:02:55)`. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175` (opt-in, `REMEDY_INSTALL_SMOKE=1`). No FAILED, ERROR or "process(es) behind" line.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` via a python3 script with `cwd=<root>` — exit 0, `fail_count` 0; `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open` all pass.
7. Gate 5: `python3 .remedy-wt/f307-r10/open_count.py <root>` — `14`.
8. Gate 6: `git -C <root> diff --stat 9b2767154 HEAD -- packages apps scripts tests docs` — empty output, confirming the committed product bytes equal the reviewer's dry run.

## Authored-text proofs

`.agent/authored/f307-r22.md` equals `block.md`: 89 lines, sha256 `6b88cdc17f4e046e52679e723c08301e432922940b4494f1a9133e4dbd41feed` on both sides. The `.agent/live_review.md` and `.agent/decisions.md` appends (each equal to pre-image plus slice) and the `.agent/plan.md` replacement were each proved byte for byte by one script right after writing, in the same run that applied them. C2, C3 and C4 were the reviewer's cut patches (`c2.patch`, `c3.patch`, `c4.patch`) applied with `git apply --check` then `git apply`, never retyped; each staged diff was read in full before its commit and matched its patch hunk for hunk.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1 to C5), each touching only its named paths. No mutation red-proof, no full suite outside the selection, `REMEDY_TEST_MAX_WORKERS` never set, `.data` never read, no amend, rebase, force-push or `--no-verify`, no PR; each gate ran once and never concurrently.

## For the operator, in plain sentences

When a job stopped because one of its steps could not be finished, for example because the model was not reachable, a person can now try that step again, and the job's overview offers it as the next step.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Review round 22's handback and book its verdict, with R-1331, in the next round's first commit.
4. T017, R-1325 then R-1327.

Operator questions open: 0. Open findings count gate 5 printed: 14.
