# Handoff — F271 No more legacy: ownership, reachability, replace-is-delete · Round 2

## Session

SESSION 1 of feature F271 · round 2 · rounds so far 2

Context self-assessment: the worker read the block, AGENTS.md, `docs/roadmap/features/T2_F271.md`, DECISION F271 D2 and every non-deletion hunk of `prototype_final.diff` in full once each, and every figure below comes from a command run in this round.

## Range

Review of c798fd2d..HEAD — branch `feature/f271-no-more-legacy`.

## Summary

- C1 is the bookkeeping. It saves the four payload copies, sets `.agent/plan.md` to plan.md, appends ledger.md to `.agent/live_review.md` (the F271 R1 gate entry, `Done: R-0893`, and R-0980, R-0981 and R-0982), and appends DECISION F271 D2 to `.agent/decisions.md`.
- C2 is the D2 (4) deletion. It removes `diagnostic_comparison.py`, `task_plan_evidence.py` and `execution_config_evidence.py`, together with the test file that existed only for each.
- C3 is the orphan-module test. It adds `tests/test_no_orphan_modules.py` with its 16 `ALLOWED_UNWIRED` entries and registers it in `ARCHITECTURE_FILES` in `tests/conftest.py` and in the `budgets` stage `test_paths` in `packages/orchestration/ci_stages.py`.
- C4 is this handoff.

## Commits

### 3b616e49 F271 R2 C1: book F271 round 1's verdict and R-0893, register R-0980 to R-0982, land DECISION F271 D2, save the round 2 payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f271-r2-block.md` | +89 / -0 | Byte copy of the block |
| `.agent/authored/f271-r2-decisions.md` | +50 / -0 | Byte copy |
| `.agent/authored/f271-r2-ledger.md` | +10 / -0 | Byte copy |
| `.agent/authored/f271-r2-plan.md` | +27 / -0 | Byte copy |
| `.agent/decisions.md` | +50 / -0 | `c798fd2d` bytes + decisions.md (DECISION F271 D2) |
| `.agent/live_review.md` | +10 / -0 | `c798fd2d` bytes + ledger.md |
| `.agent/plan.md` | +9 / -11 | := plan.md |

245 insertions, 11 deletions (`git show --numstat`).

### 430a0832 F271 R2 C2: delete diagnostic_comparison, task_plan_evidence and execution_config_evidence with their tests under DECISION F271 D2
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/diagnostic_comparison.py` | +0 / -172 | deleted (D2 (4)) |
| `packages/orchestration/execution_config_evidence.py` | +0 / -64 | deleted (D2 (4)) |
| `packages/orchestration/task_plan_evidence.py` | +0 / -72 | deleted (D2 (4)) |
| `tests/orchestration/test_diagnostic_comparison.py` | +0 / -179 | deleted with its module |
| `tests/orchestration/test_execution_config_evidence.py` | +0 / -144 | deleted with its module |
| `tests/orchestration/test_task_plan_evidence.py` | +0 / -78 | deleted with its module |

0 insertions, 709 deletions.

### e6d73a51 F271 R2 C3: T001 orphan-module test with its ALLOWED_UNWIRED list, registered in ARCHITECTURE_FILES and the budgets CI stage
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/ci_stages.py` | +1 / -0 | `budgets` stage `test_paths` gains the new file |
| `tests/conftest.py` | +1 / -0 | `ARCHITECTURE_FILES` gains the new file |
| `tests/test_no_orphan_modules.py` | +308 / -0 | the orphan scan, four tests, 16 `ALLOWED_UNWIRED` entries |

310 insertions, 0 deletions.

### C4 (this commit) F271 R2 C4: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C3, with 310.

## External actions

- `git worktree add --detach .remedy-wt/f271-r2-g5 e6d73a51` for G5, then `git worktree remove .remedy-wt/f271-r2-g5`. Afterwards `git worktree list` shows the primary checkout alone: `/home/decodeux/Repos/remedy  e6d73a51 [feature/f271-no-more-legacy]`.
- `git push` after C4, not forced. No pull request is opened.
- No evidence job and no zip.

## Verification

All gates below ran at C3 (`e6d73a51`) before C4.

- **Transport**, before any write: `sha256sum` matched all four payload digests (plan.md `495356e5…`, ledger.md `9209c91f…`, decisions.md `30628c17…`, prototype_final.diff `3678d741…`) and the block's `1dd7da8f4ee1e9b3da46c8c70629b8c91e39e903b2d0dc6c1fa8d51b4298299c`. `git apply --check` on the prototype passed at `c798fd2d`.
- **G1**: `python3 .remedy-wt/f271-r2/g1.py` printed `8 checks True` (exit 0). The checks are: the five digests; `.agent/plan.md` equals plan.md; `.agent/live_review.md` equals its `c798fd2d` bytes + ledger.md; `.agent/decisions.md` equals its `c798fd2d` bytes + decisions.md; and each of the four `.agent/authored/f271-r2-*` copies equals its payload. All are read at `e6d73a51`.
- **G2**: `git diff --binary c798fd2d e6d73a51 -- . ':!.agent' | git patch-id --stable` printed `6d27af6437b714b225d8d96a2524cde9985403cc 0000000000000000000000000000000000000000`. `git patch-id --stable < prototype_final.diff` printed the same first field (exit 0). `git show --numstat 430a0832` lists exactly the six deleted paths, each `0` insertions (table above).
- **G3**: `git status --porcelain` was empty. The eleven-target command, as ordered, run serially in the primary checkout, printed `544 passed in 71.15s (0:01:11)` (exit 0, 0 failed).
- **G4**: `python3 -m ruff check tests/test_no_orphan_modules.py tests/conftest.py packages/orchestration/ci_stages.py` printed `All checks passed!` (exit 0). `git grep -n -E "diagnostic_comparison|task_plan_evidence|execution_config_evidence" -- . ':!.agent' ':!docs/roadmap'` (exit 0) printed exactly three lines, the ones D2 (4) keeps:
  - `tests/docs/test_docs_consistency.py:2022:        assert "diagnostic_comparison" in doc`
  - `tests/docs/test_docs_consistency.py:2023:        assert "produce_diagnostic_comparison" in doc or "validate_diagnostic_comparison" in doc`
  - `tests/orchestration/test_job_evidence.py:1406:        assert "test_execution_config_evidence.py" not in src`
- **G5**: disposable worktree `.remedy-wt/f271-r2-g5` at `e6d73a51`, driven by `.remedy-wt/f271-r2/g5.py`. Every run was `python3 -B -m pytest -q -p no:cacheprovider -rf tests/test_no_orphan_modules.py` from the worktree root, with `__pycache__` purged before it. Each change was reverted before the next.
  - Control, unmutated: `4 passed in 1.24s`, exit 0.
  - (a) `packages/orchestration/zz_orphan_probe.py` holding `X = 1`: `1 failed, 3 passed in 1.26s`, exit 1, `FAILED tests/test_no_orphan_modules.py::test_no_module_is_an_orphan`. The assertion output names `zz_orphan_probe` on two lines.
  - (b) the two-line `scripts/rotate_live_review.py` entry removed: `1 failed, 3 passed in 1.24s`, exit 1, `FAILED tests/test_no_orphan_modules.py::test_no_module_is_an_orphan`. The output names `rotate_live_review` on two lines.
  - (c) `("scripts/build_review_zip.py", "probe"),` added to `ALLOWED_UNWIRED`: `1 failed, 3 passed in 1.28s`, exit 1, `FAILED tests/test_no_orphan_modules.py::test_every_allowed_unwired_entry_is_a_live_orphan`. The output names `build_review_zip` on two lines.
  - After the last revert, `git status --porcelain` in the worktree was empty. No change stayed green.
- **G6** comes after the push, so the round report carries it.
- Full suite not run (amend0917-throughput).

## Authored-text proofs

- The byte copies are at `.agent/authored/f271-r2-*`, four files. Each is `True` against its payload (G1). The block copy's digest is `1dd7da8f4ee1e9b3da46c8c70629b8c91e39e903b2d0dc6c1fa8d51b4298299c`.
- `.agent/plan.md`, `.agent/live_review.md` and `.agent/decisions.md` were each built from payload bytes, or from `git show c798fd2d:` bytes plus the payload, and each byte check is `True` (G1).
- The code of C2 and C3 is the prototype, byte for byte by patch-id (G2).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `3b616e49` |
| C2 deletion (D2 (4)) | done | `430a0832`; G4 grep leaves only the three kept lines |
| C3 orphan-module test | done | `e6d73a51`; G5 red-proof holds for (a), (b) and (c) |
| C4 handoff | done | This commit |

## Open findings

By distinct id on the committed `.agent/live_review.md` at C3, `^- R-\d+ — ` gives 136 ids and `^Done: R-\d+ — ` gives 5, all of them within the 136, so 131 are open. That is round 1's 129, minus R-0893 (now Done), plus R-0980, R-0981 and R-0982.

## Deviations & assumptions

- **Commit sequence:** as ordered (C1, C2, C3, C4, then the push). No extra commit.
- **Prototype:** `git apply` put the whole prototype on the working tree at `c798fd2d` + C1. C2 staged and committed only the six deletions. C3 committed the three remaining paths. Nothing in the prototype was changed, and the worker found no defect in it.
- **Driver scripts:** gates ran through gitignored scratch in `.remedy-wt/f271-r2/`: `g1.py`, `g5.py` and `openset.py`. The bash guard rejected the inline forms. The G3 run that was piped to `tail` was repeated with the output sent to `.remedy-wt/f271-r2/g3.log`, so the real exit code (0) could be read. Both runs read `544 passed`.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. The review of round 2.

Operator questions open: 5
