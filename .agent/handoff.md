# Handoff — F062 R1 (T001)

## Range

Review of `b836d364..HEAD` (branch `feature/f062-product-smoke`), HEAD `1e3e58b0`.

## Commits

### 4d763887 chore(f062): record the R1 block and its authored texts
| Path | +/- | Reason |
| --- | --- | --- |
| `.agent/authored/f062-r1-{1,2}.md` | +29 | authored texts, sha256-verified before use |
| `.agent/last_block.md` | +107/-32 | the R1 block verbatim, OUTCOME pending |

### b538b1e4 chore(f062): claim F062 — STATUS [~] + state reset
| Path | +/- | Reason |
| --- | --- | --- |
| `docs/roadmap/STATUS.md` | +1/-1 | the F062 claim line only |
| `.agent/live_review.md` | +17/-67 | full-file copy of f062-r1-1 |
| `.agent/plan.md`, `.agent/context.md` | +71/-47 | rewritten for F062 (R-0162 readers) |

### dcf7775e feat(f062): product-smoke block — schema kind, applicability, registration
| Path | +/- | Reason |
| --- | --- | --- |
| `packages/orchestration/product_smoke.py` | +142 | the block: checks, applicability, seam registration |
| `packages/orchestration/dod_schema.py` | +20/-1 | `product_smoke` kind + spec validation |
| `packages/orchestration/dod_compiler.py` | +23/-6 | `worktree_root` on the standard-check context (additive) |

### cf543a47 feat(f062): app_starts runner — shared cycle, bounded retry, teardown always
| Path | +/- | Reason |
| --- | --- | --- |
| `packages/orchestration/dod_runners.py` | +127/-38 | `_run_app_once` extracted from the flow runner; smoke runner |
| `tests/orchestration/test_dod_runners.py` | +5/-2 | the kind-set pin now names six kinds (deviation 2) |

### f266f4f5 test(f062): two real fixture mini-apps
| Path | +/- | Reason |
| --- | --- | --- |
| `tests/orchestration/fixtures/smoke/good_app.py` | +50 | starts clean, answers `/health` |
| `tests/orchestration/fixtures/smoke/broken_start_app.py` | +39 | pure logic green, startup fatal |

### 1e3e58b0 test(f062): app_starts red and green, not-applicable, held job
| Path | +/- | Reason |
| --- | --- | --- |
| `tests/orchestration/test_product_smoke.py` | +480 | 27 tests: registration, green, red, retry, port clash, teardown |

## External actions

- `gh pr list --state open …` → `[]` (Open PR Gate: no open PRs, as expected).
- `git worktree add -b tmp/f062-redproof … HEAD` → mutation red-proof; removed,
  pruned, branch deleted; `git worktree list` → primary only. No push, no PR.

## Verification

    $ python3 -m pytest tests/orchestration/test_product_smoke.py -q   27 passed  EXIT=0
    $ python3 -m pytest tests/docs/ -q                                293 passed  EXIT=0
    $ python3 -m pytest tests/cli/test_golden_path.py -q               42 passed  EXIT=0
    $ python3 -m pytest <F061 dod suites + schemas + smoke> -q        227 passed  EXIT=0
    $ git status --porcelain                                          (empty)

Broken-start red→green evidence. Real run of the broken fixture:

    status: failed | reason: smoke_start_failed
      start failed: the application exited before it answered /health (exit code 78)
      broken-start-app: FATAL config error: PAYMENTS_ENDPOINT is not set
      stop: the application family was stopped

Mutation proof (throwaway worktree; runner made to report a failed start green):

    4 failed, 2 passed  EXIT=1  ← all of TestBrokenStartHoldsTheJob
    AssertionError: assert 'passed' == 'failed'; unmutated HEAD: 6 passed EXIT=0

## Authored-text proofs

    sha256sum .agent/authored/f062-r1-1.md → 49e41f96…  (matches BEGIN marker)
    sha256sum .agent/authored/f062-r1-2.md → 549239c5…  (matches BEGIN marker)
    cmp .agent/authored/f062-r1-1.md .agent/live_review.md → EXIT=0
    STATUS.md: FROM count 1→0, TO count 0→1, `git diff --numstat` = 1 1

## Deviations & assumptions

1. **New DoD check kind `product_smoke`** (schema + runner) rather than reusing
   `runtime_flow`. The ordered semantics — bounded retry with "passed on retry",
   and not-applicable as non-gating — have no home in the flow runner, and a
   check needs a kind to reach the gate at all.
2. **One F061 assertion updated** (`test_dod_runners.py` kind-set pin: five →
   six) — a necessary consequence of 1, outside the block's literal change
   list; the invariant it guards is unchanged.
3. **`StandardCheckContext.worktree_root`** added (defaulted, additive) so
   applicability is decided at compile time. Empty worktree → the block
   contributes nothing rather than guessing.
4. **Not-applicable is a non-blocking RED**, not a pass: it lands in the gate's
   `reported_red` — visible in the matrix, gating nothing (P6).
5. **`_run_app_once`** extracted from the flow runner (and `_flow_evidence` →
   `_harness_evidence`), now shared with the smoke: one place owns the process
   discipline. Harness semantics untouched. Pre-existing `dag_schedule.py` ruff
   error left alone (reproduces at base).

## Next

Handing back to Window 1 for review of `b836d364..HEAD`.
