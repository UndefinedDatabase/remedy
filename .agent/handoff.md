# Handback — F307 round 20: book round 19; R-1417 repair; `pingpong_provider.py` structural step (3); T015, R-1323

## Session

SESSION 5 of feature F307 · round 20 · rounds so far 20

Context self-assessment: this worker verified every prepared digest before any write, applied C1 by a byte-proof script, applied C2 through C4 by `git apply` from the reviewer's cut patches with no hand-retyping, read each staged diff in full before committing (for C3, the stat plus every hunk outside the plain import-repoint lines), and ran each gate once; context is ample and nothing was lost.

Fortschritt: ~83 % (T001 to T006, T008 to T011, T013, T014, R-1280, R-1290, R-1292, R-1297, R-1298, R-1301, R-1414, R-1415 and R-1416 landed, R-1281's writer part landed, R-1417 and T015 under review · the rest open) — Schätzung

## Range

Review of `83d2f2e4e`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### 229adc1e4 F307 R20 C1: book round 19 with R-1417, R-1282 and R-1311, DECISION F307 D20, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r20.md` | 93/0 | NEW FILE, this round's block, byte copy (93 lines, sha256 `13ad11d85276c8a67b066c17eaf66634d583c002733ffd81c4f859c1598e76b0`, equal to `block.md`) |
| `.agent/live_review.md` | 8/0 | prepared slice appended (round 19's Gate verdict FAIL, R-1417 registered, R-1282 and R-1311 done) |
| `.agent/decisions.md` | 12/0 | prepared slice appended (DECISION F307 D20) |
| `.agent/plan.md` | 9/9 | replaced with the prepared file |

122 insertions, 9 deletions over 4 files (`git show --shortstat`).

### 75f42a453 F307 R20 C2: F295's gate test reads the mission's order and the job's order, and its byte pin moves with it (R-1417)
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_client_interface.py` | 1/1 | `F295_GATE_TEST_SHA256` pin moved to the new byte hash of `test_machine_client_contract.py` |
| `tests/cli/test_machine_client_contract.py` | 4/0 | the gate test now reads the mission's one order (`order["job_ids"]`) and the job's `order_id` against it (R-1282, R-1417) |

5 insertions, 1 deletion over 2 files (`git show --shortstat`); applied from `c2.patch`, not hand-retyped.

### 38096d95c F307 R20 C3: the fake provider moves to a module of its own, structural step (3) of pingpong_provider.py
| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | 3/2 | boundary note gains step (3); the file-size table row for `pingpong_provider.py` drops to 1,574 |
| `packages/orchestration/pingpong_provider.py` | 1/192 | `FakeProvider` (192 lines) deleted; module docstring's bullet repointed |
| `packages/orchestration/pingpong_provider_fake.py` | 197/0 | NEW FILE — `FakeProvider`, moved verbatim with a new header docstring |
| `packages/orchestration/pingpong_loop.py` | 1/1 | `FakeProvider` import repointed to the new module |
| `packages/orchestration/fake_deliverable.py` | 1/1 | `FakeProvider` import repointed to the new module |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | `packages.orchestration.pingpong_provider_fake` registered |
| `tests/orchestration/test_call_modes_agree.py` | 16/10 | mode collector now reads all three provider modules (`pingpong_provider`, `pingpong_provider_ollama`, `pingpong_provider_fake`); non-vacuity test names the Ollama modes step (2) had left uncollected |
| `tests/test_structure_ratchet.py` | 1/1 | `MAX_FILE_LINES` lowered 63296 → 63105, matching the 191-line shrink of the listed file |
| 85 other test files under `tests/cli/` and `tests/orchestration/` and `tests/ui_server/` | 133/127 | one-line `FakeProvider` import repointed from `pingpong_provider` to `pingpong_provider_fake` (some files import it at more than one point); no behaviour change |

354 insertions, 334 deletions over 93 files (`git show --shortstat`); applied from `c3.patch`, not hand-retyped.

### dde931bbd F307 R20 C4: the fake provider reports fixed tokens and no cost, and the story gate reads them (R-1323)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_provider_fake.py` | 20/4 | `FAKE_BUILD_USAGE`, `FAKE_REVIEW_USAGE` and `fake_usage_actuals()` added; build/review now set fixed usage with null cost instead of a session-id-only block |
| `tests/orchestration/test_pingpong_provider_fake.py` | 37/0 | NEW FILE — three tests on the fixed tokens, the session-id passthrough and the failed-call no-tokens case |
| `packages/orchestration/pingpong_loop.py` | 1/1 | comment updated (FakeProvider's attempts are skipped in token accounting, not absent) |
| `packages/orchestration/job_evidence.py` | 1/1 | docstring updated (the fake's usage is not counted, not absent) |
| `tests/cli/test_status_cmd.py` | 6/4 | test renamed and its assertion reads the fake's fixed token totals instead of all-null |
| `tests/orchestration/test_do_then_story.py` | 3/0 | story gate asserts measured (non-null, >0) token figures on a fake run |
| `tests/orchestration/test_token_ledger.py` | 4/4 | ledger-row assertions read the fake's fixed `tokens_in` by role instead of `None` |
| `docs/system/api-release-matrix-v1.json` | 6/0 | 1.27's `value_changes` gains the token-figures entry |
| `docs/system/public-http-api-v1.md` | 2/1 | prose updated: the fake providers report fixed tokens and no cost |

80 insertions, 15 deletions over 9 files (`git show --shortstat`); applied from `c4.patch`, not hand-retyped.

### (this commit) F307 R20 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | HEAD and `origin/feature/f307-findings-paydown-v9` both `83d2f2e4eb55d7b87fa681623f8e10cb303afb48`, tree clean, no pull run, no `.agent/STOP` |
| C1 | done | commit `229adc1e4`, 122 insertions, byte proofs all held |
| C2 | done | commit `75f42a453`, 5 insertions, applied from `c2.patch` |
| C3 | done | commit `38096d95c`, 354 insertions, applied from `c3.patch` |
| C4 | done | commit `dde931bbd`, 80 insertions, applied from `c4.patch` |
| C5 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty |
| Gate 2 | done | `ruff over 96 files: exit 0`, `All checks passed!` |
| Gate 3 | done | `paths 266`, `exit 0`, `9491 passed, 2 skipped in 215.73s` |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | `17` |
| Gate 6 | done | `git diff --stat 1ba836d8f HEAD -- packages apps scripts tests docs` empty |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

None before this commit; the push follows it and is reported in the session reply. `.remedy-wt/f307-r20-worker/` (created this round) holds the digest-verification script, the C1 byte-proof script, the integrity-check script, the four commit-message files and the selection output. No provider call.

## Verification

1. Digests, before any write: `digests.txt` sha256 `a419550af2b505554d1a08cdc819a492198c266c6bb0940ae8ccbd54241f436c` and `block.md` sha256 `13ad11d85276c8a67b066c17eaf66634d583c002733ffd81c4f859c1598e76b0` (93 lines) both equal the delivering prompt; the ten other listed entries matched (by a python3 script, since `digests.txt` is tab-separated).
2. C0: branch `feature/f307-findings-paydown-v9`; HEAD equals `origin/feature/f307-findings-paydown-v9` at `83d2f2e4eb55d7b87fa681623f8e10cb303afb48`; tree clean.
3. Gate 1: `git -C <root> status --porcelain` — empty (read after C4, before C5).
4. Gate 2: `python3 .remedy-wt/f307-r20/prep/ruff_touched.py <root>` — 96 touched files listed, `ruff over 96 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r20/prep/run_selection.py <root> .remedy-wt/f307-r20-worker/selection-output.txt` — `paths 266`, `exit 0`, `9491 passed, 2 skipped in 215.73s (0:03:35)`. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175` (opt-in, `REMEDY_INSTALL_SMOKE=1`). No FAILED, ERROR or "process(es) behind" line.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` via a python3 script with `cwd=<root>` — exit 0, `fail_count` 0; `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open` all pass.
7. Gate 5: `python3 .remedy-wt/f307-r10/open_count.py <root>` — `17`.
8. Gate 6: `git -C <root> diff --stat 1ba836d8f HEAD -- packages apps scripts tests docs` — empty output, confirming the committed product bytes equal the reviewer's dry run.

## Authored-text proofs

`.agent/authored/f307-r20.md` equals `block.md`: 93 lines, sha256 `13ad11d85276c8a67b066c17eaf66634d583c002733ffd81c4f859c1598e76b0` on both sides. The `.agent/live_review.md` and `.agent/decisions.md` appends (each equal to pre-image plus slice) and the `.agent/plan.md` replacement were each proved byte for byte by one script right after writing, in the same run that applied them. C2, C3 and C4 were the reviewer's cut patches (`c2.patch`, `c3.patch`, `c4.patch`) applied with `git apply --check` then `git apply`, never retyped; each staged diff was read in full before its commit (for C3, the stat plus every hunk outside the plain import-repoint lines, confirmed against `pingpong_provider.py`'s deletion and `pingpong_provider_fake.py`'s new content being byte-equal apart from the header).

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1 to C5), each touching only its named paths. No mutation red-proof, no full suite outside the selection, `REMEDY_TEST_MAX_WORKERS` never set, `.data` never read, no amend, rebase, force-push or `--no-verify`, no PR; each gate ran once and never concurrently.

## For the operator, in plain sentences

A practice run on Remedy's stand-in model now shows token figures in its overview, its story and its cost records, the way a real run does, and still no money, because the stand-in costs nothing. And a check that last round's change had broken works again.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Review round 20's handback and book its verdict, with R-1417 and R-1323, in the next round's first commit.
4. T016, R-1332 then R-1331.

Operator questions open: 0. Open findings count gate 5 printed: 17.
