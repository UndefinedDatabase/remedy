# Handback — F115 · R21 (blocker repair + gate re-run)

## Range
Review of fbaab57f..28dddb5c (branch feature/f115-prompt-cost-report).

## Commits

### d3e21942 chore(f115): save the R21 repair block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f115-r21-1.md | +156/-0 | C0 block, verbatim |
| .agent/last_block.md | +136/-144 | same bytes, cmp exit 0 |

### 7a21ac5c docs(f115): record the R20 gate FAIL and findings R-0340, R-0341
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +7/-1 | D4→D7 rewrite; R-0340, R-0341, `Gate: R20 — FAIL` |

### c64016c1 test(f115): mirror the on_prompt_composed hook in the plan-job double
| Path | +/- | Reason |
|---|---|---|
| tests/test_run_log_cli.py | +4/-1 | double takes `*, on_prompt_composed=None`; no assertion moved |

### 28dddb5c chore(f115): commit the R21 integration-gate re-run evidence
| Path | +/- | Reason |
|---|---|---|
| .agent/gate_f115_r21/ | +96/-0 | 7 files: tail, FAILED list, meta, both comm outputs, attribution, provenance |

## External actions
`git push -u origin feature/f115-prompt-cost-report` after the C4 commit; its raw
output is in the completion report. No worktree add/remove — the base side was
reused from committed R20 evidence. No gh, no PR, no merge.

## Verification
- (a) `cmp .agent/authored/f115-r21-1.md .agent/last_block.md` → exit 0, no output.
- (b) C1 gates: `DECISION F115 D4 below` 0 · `DECISION F115 D7` 1 · `^- R-0340 — High` 1 ·
  `^- R-0341 — Low` 1 · `^Gate: R20 — FAIL` 1 · `^## Steps` 1. Six of six as ordered.
- (c) C2 gates: old `def` line 0 · new `def` line 1 · `ruff check tests/test_run_log_cli.py`
  → `All checks passed!` · `pytest tests/test_run_log_cli.py -q` → `61 passed in 0.30s`,
  EXIT 0. Before the repair the same file gave `6 failed, 55 passed`.
- (d) `python3 -m pytest -n auto -q` → EXIT_CODE=1, WALL_SECONDS=129, tail
  `5 failed, 16706 passed, 19 skipped in 129.05s`. The five are R-0322's
  `reviewer_conventions` token-cap reds, present at the merge base too, so exit 1 is
  the expected outcome and not the gate.
- (e) `comm -13 base_failed_union branch_failed` → EMPTY, 0 lines. Zero branch-only
  failures: R-0340's six ids are gone and nothing replaced them.
- (f) `comm -23` → 9 lines: 8× `tests/ui_server/test_live_state.py::TestUIServerIntegration::*`
  (R20's base worktree had no built `apps/ui/dist`; this branch touches neither
  `ui_server.py` nor `apps/ui`) + 1× `test_review_bundle_runtime.py::TestSubprocessCleanup::`
  `test_timeout_raises_with_cleanup` (load-sensitive timing). Both are R20's known
  environment class; base-only ids cannot be branch regressions by construction.
  Both comm inputs verified sorted (`sort -c` exit 0) and in one line format —
  pytest's leading `FAILED ` token kept, matching the committed R20 file.
- (g) `ls .agent/gate_f115_r21/` → attribution.txt, branch_failed.txt, branch_meta.txt,
  branch_run_tail.txt, comm_base_only_failures.txt, comm_branch_only_failures.txt,
  full_log_provenance.txt.
- (h) `git worktree list` → one line. `git branch --list tmp/base-gate` → empty.
- (i) `wc -l .agent/plan.md` → 48.
- (j) `git status --porcelain` → ` M scripts/make_review_zip.sh`, and nothing else.
- (k) `git log --oneline fbaab57f..HEAD` → the four commits tabled above.
- (l) `git diff --name-only 0d6c97aa..HEAD -- packages/ apps/` → 7 paths:
  `apps/cli/command_catalog.py`, `apps/cli/commands/job.py`,
  `apps/cli/commands/stats_ledger_cmd.py`, `packages/orchestration/cost_report.py`,
  `packages/orchestration/llm_planner.py`, `packages/orchestration/pingpong_loop.py`,
  `packages/orchestration/token_ledger.py`.

## Authored-text proofs
`.agent/authored/f115-r21-1.md` vs `.agent/last_block.md`: `cmp` exit 0, 156 lines, no
trailing whitespace on any line. PAIR 1 applied as a substring rewrite (FROM 0x, TO 1x).
PAIR 2 was appended by slicing the committed authored file itself, so the appended
bytes ARE the authored bytes. The C2 FROM/TO pair applied as written.

## Deviations & assumptions
| Item | Status | Reason |
|---|---|---|
| C0 | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
No deviation from the block. The 478-line branch log stays uncommitted under the
500-insertion cap; its line count and sha256 are in `full_log_provenance.txt`, in the
R20 shape. Assumption: the merge base 0d6c97aa is unmoved, so reusing R20's
`base_failed_union.txt` is sound — the block states it and no base run was ordered.
Deviations, declared: this handoff is 92 lines, over the 60-line cap (AGENTS.md
DECISION D15). Cause is mandated content — four per-commit tables, raw transcripts for
all twelve ordered gates (a)-(l), the authored-text proofs and the item-status table.
No section was dropped.

## Next
Reviewer gates R21 and issues its verdict; then closure per
docs/roadmap/STATUS_closure_protocol.md.
