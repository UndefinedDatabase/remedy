# Handback — F307 round 13: book round 12; `pingpong_loop.py` structural step (3), the provider call to `pingpong_provider_call.py`; R-1277

## Session

SESSION 4 of feature F307 · round 13 · rounds so far 13

Context self-assessment: this worker verified every prepared digest before any write, applied C1 through a byte-proof script and C2 and C3 as the two prepared patches without a hand edit, read each staged diff before committing, and ran each gate once; context is ample and nothing was lost.

Fortschritt: ~62 % (T001 to T004, T010, T011, T014, R-1280, R-1290, R-1292, R-1297, R-1298, R-1301, R-1414 and R-1415 landed, R-1281's writer part landed, pingpong_loop.py's step (3) and R-1277 under review · the rest open) — Schätzung

## Range

Review of `76008d17a`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### 8971c57a8 F307 R13 C1: book round 12 with R-1281 landed in part, DECISION F307 D13, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r13.md` | 97/0 | NEW FILE, this round's block, byte copy (97 lines, sha256 `745de3975d53086d0b65d7540742f02645eac34dc27af57b54700ed3f2447690`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared slice appended (DECISION F307 D13) |
| `.agent/live_review.md` | 4/0 | prepared slice appended (round 12's Gate verdict PASS, R-1281 landed in part) |
| `.agent/plan.md` | 10/8 | replaced with the prepared file |

### 3ba0b954b F307 R13 C2: the provider call moves to pingpong_provider_call.py, structural step (3) of pingpong_loop.py
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_provider_call.py` | 266/0 | NEW FILE: `ProviderAttempt`, `_begin_stream_call`, `_offer_stable_prefix`, `_record_attempt`, `_record_rate_limit_wait`, `_call_with_retry`, moved verbatim |
| `packages/orchestration/pingpong_loop.py` | 7/246 | the six names removed, imports adjusted |
| `packages/orchestration/pi_provider.py` | 1/1 | docstring names the new module |
| `docs/system/structure-ledger-v1.md` | 12/8 | boundary gains the provider call, step (3) recorded, `_call_with_retry` row moved, file row 5192 to 4953 |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | the new module |
| `tests/test_structure_ratchet.py` | 1/1 | `MAX_FILE_LINES` 64156 to 63917 |
| 10 test files under `tests/orchestration/` | 53/51 in total; import lines and the `_time.sleep` patch target only | `test_budget_stop_integration.py`, `test_claude_cli_resume.py`, `test_failure_wiring.py`, `test_job_budgets.py`, `test_model_failover.py`, `test_pi_provider.py`, `test_predictive_budget.py`, `test_provider_evidence_integration.py`, `test_provider_retry.py`, `test_stream_evidence_integration.py` |

341 insertions, 307 deletions over 16 files.

### 7f8425f3b F307 R13 C3: a retry waits out a backup link's rate limit on that link's slot (R-1277)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_provider_call.py` | 6/7 | the governor seam observes and waits on `out.provider`, falling back to the configured provider |
| `tests/orchestration/test_provider_retry.py` | 28/0 | `test_a_backup_links_rate_limit_is_waited_out_on_that_links_slot` |
| `tests/test_structure_ratchet.py` | 1/1 | `MAX_FUNCTION_LINES` 28704 to 28703 |
| `docs/system/structure-ledger-v1.md` | 1/1 | `_call_with_retry` row 143 to 142 |
| `docs/system/model-failover-v1.md` | 4/1 | two sentences and a file-list entry |

(The five rows above total 40 insertions: 6 + 28 + 1 + 1 + 4.)

40 insertions, 10 deletions.

### (this commit) F307 R13 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | HEAD and `origin/feature/f307-findings-paydown-v9` both `76008d17a76ad6b10214418db1136a7d1877ac79`, tree clean, no pull run |
| C1 | done | commit `8971c57a8`, 123 insertions |
| C2 | done | commit `3ba0b954b`, 341 insertions, patch applied without a hand edit |
| C3 | done | commit `7f8425f3b`, 40 insertions, patch applied without a hand edit |
| C4 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty |
| Gate 2 | done | `ruff over 14 files: exit 0`, `All checks passed!` |
| Gate 3 | done | `paths 96`, `exit 0`, `4580 passed, 2 skipped in 26.00s` |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | `30` |
| Gate 6 | done | `git diff --stat 441bf1313 HEAD -- packages apps scripts tests docs` empty |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

None before this commit; the push follows it and is reported in the session reply. `.remedy-wt/f307-r13-worker/` (created this round) holds the digest, C1 byte-proof and gate-4 scripts, the four commit-message files and the selection output. No provider call.

## Verification

1. Digests, before any write: `digests.txt` sha256 `daafac71b5474bb2b2694005011c75625b779f81b237291a4f11477d0353fdfe` and `block.md` sha256 `745de3975d53086d0b65d7540742f02645eac34dc27af57b54700ed3f2447690` (97 lines) both equal the delivering prompt; the seven other files listed matched their digests.
2. C0: branch `feature/f307-findings-paydown-v9`; HEAD equals `origin/feature/f307-findings-paydown-v9` at `76008d17a76ad6b10214418db1136a7d1877ac79`; tree clean; `.agent/STOP` absent.
3. Gate 1: `git -C <root> status --porcelain` — empty.
4. Gate 2: `python3 .remedy-wt/f307-r13/prep/ruff_touched.py <root>` — `ruff over 14 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r13/prep/run_selection.py <root> .remedy-wt/f307-r13-worker/selection-output.txt` — `paths 96`, `exit 0`, `4580 passed, 2 skipped in 26.00s`. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252) and `tests/test_install_smoke.py:175` (opt-in, `REMEDY_INSTALL_SMOKE=1`). No FAILED, ERROR or "process(es) behind" line.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` via a python3 script with `cwd=<root>` — `fail_count` 0; `handler_import` pass (`handlers=194`), `live_review_verdict` pass (last Gate verdict PASS), `plan_consistency` pass (`unchecked=0, context_complete=False`), `relevant_untracked` pass, `repo_root_hygiene` pass, `high_blockers_open` pass.
7. Gate 5: `python3 .remedy-wt/f307-r10/open_count.py <root>` — `30`.
8. Gate 6: `git -C <root> diff --stat 441bf1313 HEAD -- packages apps scripts tests docs` — empty.

## Authored-text proofs

`.agent/authored/f307-r13.md` equals `block.md`: 97 lines, sha256 `745de3975d53086d0b65d7540742f02645eac34dc27af57b54700ed3f2447690` on both sides. The `.agent/live_review.md` and `.agent/decisions.md` appends and the `.agent/plan.md` replacement were each proved byte for byte (pre-image plus prepared slice equals result, or copy equals source) by one script right after writing: all four checks read `True`. `c2.patch` and `c3.patch` were applied unchanged after their digests matched; gate 6 shows the committed product bytes equal the reviewer's dry run.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1, C2, C3, C4), each touching only its named paths (C2 touched the 16 paths the patch carries). No mutation red-proof, no full suite, `REMEDY_TEST_MAX_WORKERS` never set, `.data` never read, no amend, rebase, force-push or `--no-verify`, no PR; each gate ran once and never concurrently. Gate 1's reading was taken after C3 and again after the last gate, both empty.

## For the operator, in plain sentences

The part of Remedy that calls a model, retries it and books each call now lives in a file of its own, so the fixes to backup models can be made without growing the largest file. When a backup model is rate limited, Remedy now waits for that backup's limit to pass instead of booking the wait to the model it stood in for.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Review round 13's handback and book its verdict, with R-1277, in the next round's first commit.
4. The rest of T005 in `pingpong_provider_call.py`: R-1276, then R-1278, then R-1287 and R-1289.

Operator questions open: 0. Open findings count gate 5 printed: 30.
