# Handoff — F115 Prompt breakdown & cost report · Round 12 (T002-Goldens)

Branch `feature/f115-prompt-cost-report`, HEAD `887061b4` before this commit.
NO PR exists and closure has NOT started. The round started on a clean tree.
Deviations, declared: (1) this file is over the 60-line limit (AGENTS.md
DECISION D15) — the cause is the mandated content: the item-status table, the
commit table, the changed-files table, fourteen gate values and both probe
results; no section is dropped. (2) Gate (j) predicted that BOTH golden
byte-comparisons must fail; only the MARKDOWN one does. Real value reported
below, nothing adjusted to meet the prediction.

## Item status (R12)
| Item | Status | Reason |
|------|--------|--------|
| C1a  | done   | |
| C1b  | done   | |
| C2   | done   | |
| C3   | done   | |
| C4   | done   | |
| C5   | done   | |
| C6   | done   | |

## Commits — R12
| SHA | Item | Subject |
|-----|------|---------|
| 3821c33c | C1a | save the R12 authored block verbatim |
| 72d1860b | C1b | mirror the R12 block into last_block |
| 2915c13d | C2 | close R-0330 at the R11 gate and register R-0331 and R-0332 |
| cfeecdf7 | C3 | make the ledger part of the cost report question (R-0332) |
| 6de8429b | C4 | build the golden fixture ledger and commit the golden pair |
| 887061b4 | C5 | pin the golden bytes and the numbers they state |
| (this commit) | C6 | refresh the plan and write the R12 handoff |

## Changed files
| Path | Items |
|------|-------|
| .agent/authored/f115-r12-1.md | C1a (new, 276 lines) |
| .agent/last_block.md | C1b |
| .agent/live_review.md | C2 (Done: R-0330, + R-0331, + R-0332) |
| packages/orchestration/cost_report.py | C3 (docstring + ledger guard, +19) |
| tests/orchestration/test_cost_report.py | C3/C4/C5 (+222, 11 → 15 tests) |
| tests/orchestration/fixtures/cost_report/golden/cost_report.md | C4 (new, 26) |
| tests/orchestration/fixtures/cost_report/golden/cost_report.json | C4 (new, 93) |
| .agent/plan.md | C6 |
| .agent/handoff.md | C6 |

No CLI, no query change, no schema change, no `token_ledger.py` edit.

## Gates — real values
- (a) `cmp .agent/authored/f115-r12-1.md .agent/last_block.md` exit **0**;
  sha256 of both
  `a3106079f0a10af038120b60380b35c46ceac247c8e66dbb90de15fde38560ca`;
  `wc -lc .agent/last_block.md` → **276 19049**.
- (b) `.agent/live_review.md`: `^Landed: R-0330` **0**, `^Done:` **5**,
  `^- R-0` **13**, `^## Steps` **1**. Scoped to `2915c13d`'s ADDED lines,
  `^+Done: R-0330` **1**, `^+- R-0331` **1**, `^+- R-0332` **1**.
- (c) `ruff check cost_report.py test_cost_report.py` → **All checks passed!**
- (d) `python3 -c "import packages.orchestration.cost_report"` exit **0**.
- (e) `pytest tests/orchestration/test_cost_report.py -q` → **15 passed**
  (10 from R11 + 1 from C3 + 4 from C5), the ordered count.
- (f) `pytest tests/orchestration/test_token_ledger.py -q` → **99 passed**.
- (g) Canary `pytest tests/cli/test_golden_path.py -q` → **42 passed**.
- (h) Determinism: the two golden tests were run in TWO separate pytest
  invocations under two different `--basetemp` roots; **4 passed** each time,
  so the same bytes came out of eight independently rebuilt fixture ledgers
  under eight different `tmp_path`s. Stronger still: all eight
  `ledger.sqlite` files hash to
  `f82312caee762b03bab34188b3dfa16df1b98d8e108472917d64c5973dc5c32a`.
- (k) `wc -l .agent/plan.md` → **43** (below 50).
- (l) `git status --porcelain` → empty at handback.
- (m) `git rev-list --left-right --count origin/…HEAD` → **0  0** after push.
- (n) `git diff --name-only 0d6c97aa..HEAD | wc -l` → **35**; zero of them
  match `remedy-wt`.

## Fixture values — measured, not copied
Every number the block stated was recomputed here against a real backfill and
every one MATCHED: total 4 calls, 4000/800, cache 64/32, cost 0.25, 1 measured
and 3 unmeasured; day buckets `2026-08-01` (1, 1000/200, rest null, 0
measured), `2026-08-05` (same), `2026-08-09` (2, 2000/400, 64/32, 0.25, 1
measured); shares `diff` 1/1/400/100, `schema_tail` 1/1/60/100, `task_brief`
1/1/120/30; attribution 2/2; totals 3/580/230; cells 43.5%, 43.5%, 13.0%,
TOTAL 100.0%; `cost_usd` renders `0.2500`. No number was adjusted.

## Probes — as measured, in disposable worktrees under `.remedy-wt/`
- (i) Probe 1, the whole `if (cost.ledger_path, cost.ledger_exists) != (…)`
  block deleted: **1 failed, 14 passed** —
  `tests/orchestration/test_cost_report.py::test_a_pair_from_two_different_ledgers_is_refused_by_both_renderers`,
  `Failed: DID NOT RAISE <class 'ValueError'>`. Nothing else moved, which is
  right: no other test builds a pair whose two halves name different ledgers.
- (j) Probe 2, `_share_percent` format `.1f` → `.2f`: **2 failed, 13 passed** —
  `…::test_the_share_column_uses_the_attributed_total_as_its_denominator` and
  `…::test_the_golden_markdown_matches_the_fixture_ledger`. DEVIATION from the
  ordered prediction: the JSON golden comparison
  (`…::test_the_golden_json_matches_the_fixture_ledger`) stayed passing, and it
  is right that it did — `cost_report_json` renders no percentage at all, the
  share is a markdown-only presentation over raw ints, so `_share_percent` is
  unreachable from the json path. The ordered COLOUR held for the markdown
  golden; the ordered BLAST RADIUS was one test too wide. Nothing was mutated
  further to reach the predicted count.
  `…::test_the_golden_files_state_the_numbers_the_ledger_holds` also stayed
  passing on its `43.5%`/`13.0%` substring assertions — correct, because it
  reads the FILES on disk, which the mutation cannot touch; that is exactly the
  separation of duties it exists for.
- Both worktrees removed and pruned; `git worktree list` ends at **one line**.

## Findings
Open: **8** — R-0320, R-0322, R-0323, R-0324, R-0327, R-0328, R-0331, R-0332.
R-0332's FIX landed at `cfeecdf7` and awaits review. R-0330 is closed `Done:`
by the reviewer-authored C2 text. Next free ID **R-0333**.

## Resume here
Next expected action: review R12, then T003 — the `remedy stats report` CLI,
`--until`, the prior-period comparison and the json schema, plus the docs page
the new user-visible behaviour needs. The goldens are DATA on disk: nothing
regenerates them, so a renderer change from here on has to move those two
files in its own argued commit.

Fortschritt: 80 % (T001 ✅ · T002 ✅ · T003 offen) — Schätzung
