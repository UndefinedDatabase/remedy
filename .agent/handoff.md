# Handoff — F115 Prompt breakdown & cost report · Round 11 (T002-Renderer)

Branch `feature/f115-prompt-cost-report`, HEAD `57a1da9b` before this commit.
NO PR exists and closure has NOT started. `.agent/STOP` is gone — the round
started on a clean tree.
Deviations, declared: this file is over the 60-line limit (AGENTS.md DECISION
D15). The cause is the mandated content — the item-status table, the commit
table, the changed-files table, twelve gate values and both probe results. No
section is dropped.

## Item status (R11)
| Item | Status | Reason |
|------|--------|--------|
| C1a  | done   | |
| C1b  | done   | |
| C2   | done   | |
| C3   | done   | |
| C4   | done   | |
| C5   | done   | |

## Commits — R11
| SHA | Item | Subject |
|-----|------|---------|
| de7cba1f | C1a | save the R11 step block verbatim |
| 02b2e84f | C1b | mirror the R11 block into last_block |
| a74e0668 | C2 | scope the segment-share never-raises claim to absence |
| b11b652d | C3 | render the cost pair as markdown and json, deterministically |
| 57a1da9b | C4 | pin the cost report bytes, its absences and its shares |
| (this commit) | C5 | refresh the plan and write the R11 handoff |

## Changed files
| Path | Items |
|------|-------|
| .agent/authored/f115-r11-1.md | C1a (new) |
| .agent/last_block.md | C1b |
| packages/orchestration/token_ledger.py | C2 (one docstring line) |
| packages/orchestration/cost_report.py | C3 (new, 315 lines) |
| tests/orchestration/test_cost_report.py | C4 (new, 262 lines, 10 tests) |
| .agent/live_review.md | C5 (one `Landed:` line for R-0330) |
| .agent/plan.md | C5 |
| .agent/handoff.md | C5 |

No CLI, no golden file, no migration, no query change.

## Gates — real values
- (a) `cmp .agent/authored/f115-r11-1.md .agent/last_block.md` exit **0**;
  sha256 of both
  `431da8edba356a9521f58fec5be40f182cd7223addac54f1895a7799034dba74`;
  `wc -lc .agent/last_block.md` → **449 20234**.
- (b) `grep -c 'READ-ONLY, never raises\.' …/token_ledger.py` → **0**;
  `grep -c 'READ-ONLY, and never raises on absence\.' …` → **2**;
  `git show --numstat a74e0668 -- …/token_ledger.py` → **1  1**.
- (c) `ruff check cost_report.py token_ledger.py test_cost_report.py` →
  **All checks passed!**
- (d) `python3 -c "import packages.orchestration.cost_report"` exit **0**.
- (e) `pytest tests/orchestration/test_cost_report.py -q` → **10 passed**.
- (f) `pytest tests/orchestration/test_token_ledger.py -q` → **99 passed**,
  unchanged by C2.
- (g) Canary `pytest tests/cli/test_golden_path.py -q` → **42 passed**.
- (j) `wc -l .agent/plan.md` → **46** (below 50).
- (k) `git status --porcelain` → empty at handback.
- (l) `git rev-list --left-right --count origin/…HEAD` → **0  0** after push.

## Probes — as measured, in disposable worktrees under `.remedy-wt/`
- Probe 1, `_same_question`'s body replaced by a bare `return`:
  **1 failed, 9 passed** —
  `tests/orchestration/test_cost_report.py::test_a_mismatched_pair_is_refused_by_both_renderers`,
  `Failed: DID NOT RAISE <class 'ValueError'>`.
- Probe 2, `_figure`'s `None` branch changed to `return "0"`:
  **1 failed, 9 passed** —
  `tests/orchestration/test_cost_report.py::test_an_unmeasured_figure_prints_the_word_and_never_a_zero`,
  `assert 'unmeasured' in …`. Honest note: the other nine stayed passing and
  rightly so — they assert bytes-equality, absence of two machine strings, a
  refusal, the missing-ledger sentence, the attribution sentence and the share
  percentages, none of which a changed UNMEASURED spelling can violate. Test 3's
  own json half (`is None`) also still holds, because the mutation is in the
  markdown formatter only. No mutation was adjusted to reach a count.
- Both worktrees removed and pruned; `git worktree list` ends at **one line**.

## Findings
Open: **7** — R-0320, R-0322, R-0323, R-0324, R-0327, R-0328, R-0330.
R-0330's FIX landed at `a74e0668` and awaits review (marked `Landed:` in
`.agent/live_review.md`, one line, nothing else). Next free ID **R-0331**.

## Resume here
Next expected action: review R11, then R12 — the golden PAIR on disk over the
fixture ledger, following `packages/orchestration/gauntlet_matrix.py` and the
`share_ledger` fixture at `tests/orchestration/test_token_ledger.py:1845-1867`.
The renderer is pure and deterministic by construction (no clock, no path, no
UUID), so a golden can be blessed once rather than re-blessed per machine.

Fortschritt: 72 % (T001 ✅ · T002-Query ✅ · T002-Renderer ✅ ·
T002-Goldens · T003 offen) — Schätzung
