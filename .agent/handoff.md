# Handback — F307 round 21: book round 20; T016's first half, R-1332

## Session

SESSION 5 of feature F307 · round 21 · rounds so far 21

Context self-assessment: this worker verified every prepared digest before any write, applied C1 by a byte-proof script, applied C2 by `git apply` from the reviewer's cut patch with no hand-retyping, read the staged diff in full against the patch before committing, and ran each gate once; context is ample and nothing was lost.

Fortschritt: ~85 % (T001 to T006, T008 to T011, T013 to T015, R-1280, R-1290, R-1292, R-1297, R-1298, R-1301, R-1414 to R-1417 landed, R-1281's writer part landed, R-1332 under review · the rest open) — Schätzung

## Range

Review of `ea002803e`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### b57860bb4 F307 R21 C1: book round 20 with R-1417 and R-1323, DECISION F307 D21, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r21.md` | 81/0 | NEW FILE, this round's block, byte copy (81 lines, sha256 `6f6bef73a28cdf916fc6ef61b46f848a3fd4040198d31598b4f4414ad323149b`, equal to `block.md`) |
| `.agent/live_review.md` | 6/0 | prepared slice appended (round 20's Gate verdict PASS, R-1417 and R-1323 both RESOLVED) |
| `.agent/decisions.md` | 12/0 | prepared slice appended (DECISION F307 D21) |
| `.agent/plan.md` | 6/6 | replaced with the prepared file |

105 insertions, 6 deletions over 4 files (`git show --shortstat`).

### 40404da36 F307 R21 C2: a job a run leaves blocked keeps the time it ended (R-1332)
| Path | +/- | Reason |
|---|---|---|
| `docs/system/api-release-matrix-v1.json` | 6/0 | 1.27's `value_changes` gains the blocked-job `ended_at` entry |
| `packages/orchestration/job_run_finish.py` | 37/0 | NEW FILE — `stamp_blocked_job_finish`, a decorator wrapping `run_job` so a blocked job with no finish time is saved with the time the run ended |
| `packages/orchestration/pingpong_job.py` | 10/5 | `run_job` gains the `@stamp_blocked_job_finish` decorator and its import; the five-line comment above the id-minting import is compressed to three to keep the file at its listed 4,943 lines |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | `packages.orchestration.job_run_finish` registered |
| `tests/orchestration/test_job_run_finish.py` | 98/0 | NEW FILE — four tests: a blocked run keeps a finish time, a second run blocked via `blocked_rerun_reason` also keeps one, a run of a job with no record writes nothing, and the wrapper leaves a non-blocked or already-stamped job alone |

147 insertions, 5 deletions over 5 files (`git show --shortstat`); applied from `c2.patch`, not hand-retyped.

### (this commit) F307 R21 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | HEAD and `origin/feature/f307-findings-paydown-v9` both `ea002803e300f7d8a25bec3555c43c2594cc9103`, tree clean, no pull run, no `.agent/STOP` |
| C1 | done | commit `b57860bb4`, 105 insertions, byte proofs all held |
| C2 | done | commit `40404da36`, 147 insertions, applied from `c2.patch` |
| C3 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty |
| Gate 2 | done | `ruff over 3 files: exit 0`, `All checks passed!` |
| Gate 3 | done | `paths 379`, `exit 0`, `12701 passed, 6 skipped in 199.33s` |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | `15` |
| Gate 6 | done | `git diff --stat 99d1974a6 HEAD -- packages apps scripts tests docs` empty |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

None before this commit; the push follows it and is reported in the session reply. `.remedy-wt/f307-r21-worker/` (created this round) holds the digest-verification script, the C1 byte-proof script, the integrity-check script, the two commit-message files and the selection output. No provider call.

## Verification

1. Digests, before any write: `digests.txt` sha256 `cf1d6c5a0839e50bc31f8604eb0203a3f0af7860895fc748abbf12957e87ad79` and `block.md` sha256 `6f6bef73a28cdf916fc6ef61b46f848a3fd4040198d31598b4f4414ad323149b` (81 lines) both equal the delivering prompt; the seven other listed entries matched (by a python3 script, since `digests.txt` is tab-separated).
2. C0: branch `feature/f307-findings-paydown-v9`; HEAD equals `origin/feature/f307-findings-paydown-v9` at `ea002803e300f7d8a25bec3555c43c2594cc9103`; tree clean.
3. Gate 1: `git -C <root> status --porcelain` — empty (read after C2, before C3).
4. Gate 2: `python3 .remedy-wt/f307-r21/prep/ruff_touched.py <root>` — 3 touched files listed (`job_run_finish.py`, `pingpong_job.py`, `test_job_run_finish.py`), `ruff over 3 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r21/prep/run_selection.py <root> .remedy-wt/f307-r21-worker/selection-output.txt` — `paths 379`, `exit 0`, `12701 passed, 6 skipped in 199.33s (0:03:19)`. SKIPPED: `tests/orchestration/test_builder_bridge_smoke.py:118` (opt-in, `REMEDY_SMOKE_OLLAMA=1`), `tests/orchestration/test_real_ollama_smoke.py:96`, `:100` and `:134` (opt-in, `REMEDY_REAL_OLLAMA_SMOKE=1`), `tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175` (opt-in, `REMEDY_INSTALL_SMOKE=1`). No FAILED, ERROR or "process(es) behind" line.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` via a python3 script with `cwd=<root>` — exit 0, `fail_count` 0; `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open` all pass.
7. Gate 5: `python3 .remedy-wt/f307-r10/open_count.py <root>` — `15`.
8. Gate 6: `git -C <root> diff --stat 99d1974a6 HEAD -- packages apps scripts tests docs` — empty output, confirming the committed product bytes equal the reviewer's dry run.

## Authored-text proofs

`.agent/authored/f307-r21.md` equals `block.md`: 81 lines, sha256 `6f6bef73a28cdf916fc6ef61b46f848a3fd4040198d31598b4f4414ad323149b` on both sides. The `.agent/live_review.md` and `.agent/decisions.md` appends (each equal to pre-image plus slice) and the `.agent/plan.md` replacement were each proved byte for byte by one script right after writing, in the same run that applied them. C2 was the reviewer's cut patch (`c2.patch`) applied with `git apply --check` then `git apply`, never retyped; the staged diff was read in full before its commit and matched the patch hunk for hunk, including `pingpong_job.py` holding at its listed 4,943 lines.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1 to C3), each touching only its named paths. No mutation red-proof, no full suite outside the selection, `REMEDY_TEST_MAX_WORKERS` never set, `.data` never read, no amend, rebase, force-push or `--no-verify`, no PR; each gate ran once and never concurrently.

## For the operator, in plain sentences

A job that stops with a problem now records when it stopped, so its story shows the real end time instead of a guess from its log.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Review round 21's handback and book its verdict, with R-1332, in the next round's first commit.
4. R-1331 after its three structural steps (DECISION F307 D21 (3)).

Operator questions open: 0. Open findings count gate 5 printed: 15.
