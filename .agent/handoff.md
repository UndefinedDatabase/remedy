# Handback — F307 round 14: book round 13 (FAIL, R-1416) with R-1277; repair R-1416; `pingpong_provider.py` structural step (2); R-1278 and R-1276 together

## Session

SESSION 4 of feature F307 · round 14 · rounds so far 14

Context self-assessment: this worker verified every prepared digest before any write, applied C1 through a byte-proof script and C2 to C5 as the four prepared patches without a hand edit, read each staged diff before committing, and ran each gate once; context is ample and nothing was lost.

Fortschritt: ~65 % (T001 to T004, T010, T011, T014, R-1277, R-1280, R-1290, R-1292, R-1297, R-1298, R-1301, R-1414 and R-1415 landed, R-1281's writer part landed, R-1416, R-1278, R-1276 and pingpong_provider.py's step (2) under review · the rest open) — Schätzung

## Range

Review of `63cd621a8`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### 37ad6c38f F307 R14 C1: book round 13 (FAIL) with R-1416 and R-1277, DECISION F307 D14, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r14.md` | 97/0 | NEW FILE, this round's block, byte copy (97 lines, sha256 `208c1daaf46036911f4ef5c8812a61b4dac81d7f84c41ab7542ad9c421a6e030`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared slice appended (DECISION F307 D14) |
| `.agent/live_review.md` | 6/0 | prepared slice appended (round 13's Gate verdict FAIL, R-1416 registered, R-1277 done) |
| `.agent/plan.md` | 8/7 | replaced with the prepared file |

123 insertions, 7 deletions over 4 files.

### f68357a30 F307 R14 C2: the structured-output tests patch the backoff where it now lives (R-1416)
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_structured_outputs.py` | 2/1 | `_run_loop` patches the sleep on `pingpong_provider_call` |

### d55cf7e23 F307 R14 C3: the Ollama provider moves to pingpong_provider_ollama.py, structural step (2) of pingpong_provider.py
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_provider_ollama.py` | 218/0 | NEW FILE: the Ollama provider moved |
| `packages/orchestration/pingpong_provider.py` | 2/201 | the class removed; `create_provider` imports it when it builds one |
| `docs/system/structure-ledger-v1.md` | 4/2 | step (2) recorded, file row 1964 to 1765 |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | the new module |
| `tests/test_structure_ratchet.py` | 1/1 | `MAX_FILE_LINES` 63917 to 63718 |
| `tests/orchestration/test_pingpong_provider_ollama.py`, `test_provider_neutrality.py`, `test_relaunch_session_resume.py` | 4 insertions, 6 deletions in total | import lines only |

230 insertions, 210 deletions over 8 files.

### 75fbae8d8 F307 R14 C4: a backup link is built once, hears each call's hints and numbers its stream on from the primary's (R-1278)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/model_failover.py` | 45/10 | links built once and kept; stream hint and stable prefix handed on |
| `packages/orchestration/pingpong_provider.py` | 4/4 | `stream_counters` constructor argument of `ClaudeCliProvider` |
| `packages/orchestration/role_provider_factory.py` | 8/0 | one shared stream count per role |
| `tests/orchestration/test_model_failover.py` | 117/2 | three test classes, stub attribute renamed |
| `docs/system/model-failover-v1.md` | 3/1 | a backup is built once and numbers its stream on |

177 insertions, 17 deletions over 5 files.

### 252cf081d F307 R14 C5: every real call behind a failed-over call is booked with its own provider and model (R-1276)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/model_failover.py` | 34/6 | `FailoverCall`, `_with_calls`, the walk collects every real call |
| `packages/orchestration/pingpong_provider_call.py` | 39/25 | `ProviderAttempt.model`; `_record_attempt` books one row per call and returns the rows; the callback hears each |
| `packages/orchestration/pingpong_loop.py` | 1/1 | the evidence lists each attempt's `model` |
| `tests/orchestration/test_model_failover.py` | 102/0 | tests of the booking |
| `tests/orchestration/test_provider_retry.py` | 12/0 | an ordinary call's row names the configured model |
| `docs/system/model-failover-v1.md` | 4/1 | the booking sentence |
| `docs/system/structure-ledger-v1.md` | 1/1 | `_call_with_retry` row 142 to 140 |
| `tests/test_structure_ratchet.py` | 1/1 | `MAX_FUNCTION_LINES` 28703 to 28701 |

194 insertions, 35 deletions over 8 files.

### (this commit) F307 R14 C6: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | HEAD and `origin/feature/f307-findings-paydown-v9` both `63cd621a817325eaf6c1f21035582f19b0d64a54`, tree clean, no pull run |
| C1 | done | commit `37ad6c38f`, 123 insertions, byte proofs all True |
| C2 | done | commit `f68357a30`, 2 insertions, patch applied without a hand edit |
| C3 | done | commit `d55cf7e23`, 230 insertions, patch applied without a hand edit |
| C4 | done | commit `75fbae8d8`, 177 insertions, patch applied without a hand edit |
| C5 | done | commit `252cf081d`, 194 insertions, patch applied without a hand edit |
| C6 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty |
| Gate 2 | done | `ruff over 13 files: exit 0`, `All checks passed!` |
| Gate 3 | done | `paths 209`, `exit 0`, `8009 passed, 2 skipped in 118.77s` |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | `30` |
| Gate 6 | done | `git diff --stat fd3d556e4 HEAD -- packages apps scripts tests docs` empty |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

None before this commit; the push follows it and is reported in the session reply. `.remedy-wt/f307-r14-worker/` (created this round) holds the C1 byte-proof and gate-4 scripts, the five commit-message files and the selection output. No provider call.

## Verification

1. Digests, before any write: `digests.txt` sha256 `d2a9b5120a18b8ca97e622107d0ddbefbc135a8313f91410ce29342f7f56b36e` and `block.md` sha256 `208c1daaf46036911f4ef5c8812a61b4dac81d7f84c41ab7542ad9c421a6e030` (97 lines) both equal the delivering prompt; the ten other files listed matched their digests.
2. C0: branch `feature/f307-findings-paydown-v9`; HEAD equals `origin/feature/f307-findings-paydown-v9` at `63cd621a817325eaf6c1f21035582f19b0d64a54`; tree clean; `.agent/STOP` absent.
3. Gate 1: `git -C <root> status --porcelain` — empty (read after C5).
4. Gate 2: `python3 .remedy-wt/f307-r14/prep/ruff_touched.py <root>` — `ruff over 13 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r14/prep/run_selection.py <root> .remedy-wt/f307-r14-worker/selection-output.txt` — `paths 209`, `exit 0`, `8009 passed, 2 skipped in 118.77s (0:01:58)`. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252) and `tests/test_install_smoke.py:175` (opt-in, `REMEDY_INSTALL_SMOKE=1`). No FAILED, ERROR or "process(es) behind" line (a search of the output file for those words counted 0).
6. Gate 4: `python3 -m apps.cli.main integrity check --json` via a python3 script with `cwd=<root>` — exit 0, `fail_count` 0; `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open` all pass.
7. Gate 5: `python3 .remedy-wt/f307-r10/open_count.py <root>` — `30`.
8. Gate 6: `git -C <root> diff --stat fd3d556e4 HEAD -- packages apps scripts tests docs` — empty.

## Authored-text proofs

`.agent/authored/f307-r14.md` equals `block.md`: 97 lines, sha256 `208c1daaf46036911f4ef5c8812a61b4dac81d7f84c41ab7542ad9c421a6e030` on both sides. The `.agent/live_review.md` and `.agent/decisions.md` appends and the `.agent/plan.md` replacement were each proved byte for byte by one script right after writing: all four checks read `True`. `c2.patch` to `c5.patch` were applied unchanged after `git apply --check`, their digests matching; gate 6 shows the committed product bytes equal the reviewer's dry run.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1 to C6), each touching only its named paths. No mutation red-proof, no full suite, `REMEDY_TEST_MAX_WORKERS` never set, `.data` never read, no amend, rebase, force-push or `--no-verify`, no PR; each gate ran once and never concurrently.

## For the operator, in plain sentences

The local Ollama model's code now lives in a file of its own. When a backup model stands in for the usual one, its record of the call is written beside the usual model's record instead of over it. A call that needed a backup now counts as the two or three calls it really was, each named with the model it ran on, so the cost figures and the limit on the number of calls see all of them.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Review round 14's handback and book its verdict, with R-1416, R-1278 and R-1276, in the next round's first commit.
4. R-1287 and R-1289, which close T005.

Operator questions open: 0. Open findings count gate 5 printed: 30.
