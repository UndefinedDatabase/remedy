# Handback — F307 round 15: book round 14 with R-1416, R-1278 and R-1276; `run_pingpong`'s structural step (6); R-1289 and R-1287, which close T005

## Session

SESSION 4 of feature F307 · round 15 · rounds so far 15

Context self-assessment: this worker verified every prepared digest before any write, applied C1 through a byte-proof script and C2 and C3 as the two prepared patches without a hand edit, read each staged diff before committing, and ran each gate once; context is ample and nothing was lost.

Fortschritt: ~68 % (T001 to T004, T010, T011, T014, R-1276, R-1277, R-1278, R-1280, R-1290, R-1292, R-1297, R-1298, R-1301, R-1414, R-1415 and R-1416 landed, R-1281's writer part landed, run_pingpong's step (6), R-1289 and R-1287 under review · the rest open) — Schätzung

## Range

Review of `7022f4f4f`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### f59097ee7 F307 R15 C1: book round 14 with R-1416, R-1278 and R-1276, DECISION F307 D15, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r15.md` | 90/0 | NEW FILE, this round's block, byte copy (90 lines, sha256 `4cde8bec015c1d0fbc7a3b98c516c8b7b441eb027cdb46aa3e5fa2d7a11d88e5`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared slice appended (DECISION F307 D15) |
| `.agent/live_review.md` | 8/0 | prepared slice appended (round 14's Gate verdict PASS, R-1416, R-1278 and R-1276 done) |
| `.agent/plan.md` | 9/8 | replaced with the prepared file |

119 insertions, 8 deletions over 4 files (`git show --shortstat`).

### bf9ea3d5b F307 R15 C2: run_pingpong builds both role providers in one block, structural step (6)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_loop.py` | one block for both providers; `_create_provider_with_cwd` hands every keyword on | no behaviour change |
| `docs/system/structure-ledger-v1.md` | step (6) recorded; row 1274 to 1263; file row 4953 to 4924 | |
| `tests/test_structure_ratchet.py` | `MAX_FUNCTION_LINES` 28701 to 28690; `MAX_FILE_LINES` 63718 to 63689 | |

26 insertions, 54 deletions over 3 files (`git show --shortstat`).

### b2aa4a654 F307 R15 C3: a run reads the failover chains once and a stop ends the chain between links (R-1289, R-1287)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/model_failover.py` | `stop_check` on `FailoverProvider`, consulted before each link | R-1287 |
| `packages/orchestration/role_provider_factory.py` | `chains` and `stop_check` arguments | R-1289, R-1287 |
| `packages/orchestration/pingpong_loop.py` | the block reads `resolve_failover_chains()` once and hands it and `stop_check` to both roles | R-1289, R-1287 |
| `tests/orchestration/test_model_failover.py` | `TestAStopBetweenLinksEndsTheChain`, `TestTheRunReadsTheChainsOnce` | tests |
| `docs/system/model-failover-v1.md` | the stop between links and the single table read | |
| `docs/system/structure-ledger-v1.md` | `run_pingpong` row 1263 to 1262 | |
| `tests/test_structure_ratchet.py` | `MAX_FUNCTION_LINES` 28690 to 28689 | |

102 insertions, 11 deletions over 7 files (`git show --shortstat`).

### (this commit) F307 R15 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | HEAD and `origin/feature/f307-findings-paydown-v9` both `7022f4f4f0c381efbd9cb2b04035b0f4170ca404`, tree clean, no pull run |
| C1 | done | commit `f59097ee7`, 119 insertions, byte proofs all True |
| C2 | done | commit `bf9ea3d5b`, 26 insertions, patch applied without a hand edit |
| C3 | done | commit `b2aa4a654`, 102 insertions, patch applied without a hand edit |
| C4 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty |
| Gate 2 | done | `ruff over 5 files: exit 0`, `All checks passed!` |
| Gate 3 | done | `paths 209`, `exit 0`, `8012 passed, 2 skipped in 118.79s` |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | `27` |
| Gate 6 | done | `git diff --stat de191b86f HEAD -- packages apps scripts tests docs` empty |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

None before this commit; the push follows it and is reported in the session reply. `.remedy-wt/f307-r15-worker/` (created this round) holds the digest-check, C1 byte-proof and gate-4 scripts, the three commit-message files and the selection output. No provider call.

## Verification

1. Digests, before any write: `digests.txt` sha256 `ef45447f850dbbc127489f87e9ef76069854c0bef535e94c6ea5869336d42cb3` and `block.md` sha256 `4cde8bec015c1d0fbc7a3b98c516c8b7b441eb027cdb46aa3e5fa2d7a11d88e5` (90 lines) both equal the delivering prompt; the eight other files listed matched their digests.
2. C0: branch `feature/f307-findings-paydown-v9`; HEAD equals `origin/feature/f307-findings-paydown-v9` at `7022f4f4f0c381efbd9cb2b04035b0f4170ca404`; tree clean; `.agent/STOP` absent.
3. Gate 1: `git -C <root> status --porcelain` — empty (read after C3).
4. Gate 2: `python3 .remedy-wt/f307-r15/prep/ruff_touched.py <root>` — `ruff over 5 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r15/prep/run_selection.py <root> .remedy-wt/f307-r15-worker/selection-output.txt` — `paths 209`, `exit 0`, `8012 passed, 2 skipped in 118.79s (0:01:58)`. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252) and `tests/test_install_smoke.py:175` (opt-in, `REMEDY_INSTALL_SMOKE=1`). No FAILED, ERROR or "process(es) behind" line (a search of the output file for those words counted 0).
6. Gate 4: `python3 -m apps.cli.main integrity check --json` via a python3 script with `cwd=<root>` — exit 0, `fail_count` 0; `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open` all pass.
7. Gate 5: `python3 .remedy-wt/f307-r10/open_count.py <root>` — `27`.
8. Gate 6: `git -C <root> diff --stat de191b86f HEAD -- packages apps scripts tests docs` — empty.

## Authored-text proofs

`.agent/authored/f307-r15.md` equals `block.md`: 90 lines, sha256 `4cde8bec015c1d0fbc7a3b98c516c8b7b441eb027cdb46aa3e5fa2d7a11d88e5` on both sides. The `.agent/live_review.md` and `.agent/decisions.md` appends and the `.agent/plan.md` replacement were each proved byte for byte by one script right after writing: all four checks read `True`. `c2.patch` and `c3.patch` were applied unchanged after `git apply --check`, their digests matching; gate 6 shows the committed product bytes equal the reviewer's dry run.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1 to C4), each touching only its named paths. No mutation red-proof, no full suite, `REMEDY_TEST_MAX_WORKERS` never set, `.data` never read, no amend, rebase, force-push or `--no-verify`, no PR; each gate ran once and never concurrently.

## For the operator, in plain sentences

When a run is stopped, or its budget runs out, while Remedy is trying backup models one after another, it no longer tries the next backup. A run now reads its list of backup models once instead of once for each of its two roles.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Review round 15's handback and book its verdict, with R-1289 and R-1287, in the next round's first commit.
4. T006, R-1279, with its structural step first.

Operator questions open: 0. Open findings count gate 5 printed: 27.
