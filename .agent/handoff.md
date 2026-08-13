# Handoff — F115 Prompt breakdown & cost report · Round 15 (T003a/4)

Branch `feature/f115-prompt-cost-report`, HEAD `3e7810eb` before this commit.
Started clean at `5c7f5159`. NO PR exists; closure has NOT started.
Deviations, declared: this file is **99 lines**, over the 60-line cap
(AGENTS.md DECISION D15). Cause is mandated content: the C1..C7 item-status
table, the seven-row commit table, the eleven-row changed-files table, and
twelve gate values (a)..(l) including the gate-(d) discrepancy that C5's own
STOP clause orders reported in full. No section is dropped.

## Item status (R15)
| Item | Status | Reason |
|------|--------|--------|
| C1 | done | own commit, FIRST of the round |
| C2 | done | |
| C3 | done | own commit — C2+C3 together would be 502 insertions, over the cap |
| C4 | deviated | ordered content complete; ALSO refreshed the two `Public API::` signature lines and the one test-module docstring line enumerating `query_cost`'s filters, since both restate the signature this item changes and would otherwise be false on disk (the R-0330 class) |
| C5 | deviated | ordered content complete; the json golden moved `3  2`, not the `2  1` of gate (d) — see (d) |
| C6 | done | |
| C7 | done | |

## Commits — R15
| SHA | Item | Subject |
|-----|------|---------|
| f77554bf | C1 | close R-0334 at the R14 gate and register R-0335 |
| f48a43f7 | C2 | save the R15 authored block verbatim |
| e089be2d | C3 | mirror the R15 block into last_block |
| d285fef0 | C4 | give the ledger queries an exclusive until filter |
| 1bd90227 | C5 | surface until in both cost report renderings |
| 3e7810eb | C6 | record DECISION F115 D5 for the half-open period |
| (this commit) | C7 | refresh the plan and write the R15 handoff |

## Changed files
| Path | Items |
|------|-------|
| .agent/live_review.md | C1 — append only, 4 insertions, 0 deletions |
| .agent/authored/f115-r15-1.md | C2 (new, 251 lines) |
| .agent/last_block.md | C3 |
| packages/orchestration/token_ledger.py | C4 |
| tests/orchestration/test_token_ledger.py | C4 (+3 tests) |
| packages/orchestration/cost_report.py | C5 |
| tests/orchestration/test_cost_report.py | C5 (+2 tests) |
| tests/…/fixtures/cost_report/golden/cost_report.md | C5 |
| tests/…/fixtures/cost_report/golden/cost_report.json | C5 |
| .agent/decisions.md | C6 — append only, 40 insertions, 0 deletions |
| .agent/plan.md, .agent/handoff.md | C7 |

## Gates — real measured values
- (a) `cmp` is DENIED by this session's sandbox, so equality was measured twice
  otherwise: `sha256sum` gives both files
  `e3a1ea5706f77fccdb2953ab1db9c35a32cf493c598a6981cb4bc02d05d5d39b`, and a
  python byte compare prints `True 18389 18389`. `wc -lc` → **251 18389**.
- (b) `git show f77554bf -- .agent/live_review.md`: `^+Done: R-0334` **1**,
  `^+- R-0335` **1**. `git show --numstat f77554bf` → **4  0**, ZERO deletions.
  Whole file after C1: `^Done:` **8**, `^- R-0` **16**, `^## Steps` **1**,
  `^Landed:` **0**.
- (c) `git log --oneline 5c7f5159..HEAD`, newest first: 3e7810eb, 1bd90227,
  d285fef0, e089be2d, f48a43f7, **f77554bf** — C1 is LAST, the oldest.
- (d) markdown golden → **1  1**, as predicted. json golden → **3  2**, NOT the
  predicted `2  1`. Not a re-bless and not extra data movement: both goldens
  were hand-edited, no test regenerates them, and the CONTENT change is exactly
  what (d) names — `"report_version": 1` → `2` plus one added `"until": ""`
  after `"timezone"`. The extra pair is a JSON SEPARATOR artifact: inserting a
  key after the last one puts a trailing comma on the `"timezone": "UTC"` line,
  which git counts as one deletion plus one addition. No figure, bucket or
  segment row moved. Full diff of both goldens is in commit 1bd90227.
- (e) `python3 -m ruff check` over the four files → `All checks passed!`, exit 0.
- (f) `pytest` over the two files → **119 passed**. Baseline 114 (99 + 15), +3
  from C4 and +2 from C5.
- (g) `pytest tests/cli/test_stats_cost.py -q` → **41 passed**, unmoved.
- (h) Canary `pytest tests/cli/test_golden_path.py -q` → **42 passed**.
- (i) One disposable worktree `.remedy-wt/f115-r15-probe`, detached at 3e7810eb.
  P1 (delete the `until` clause from `_cost_filters`) fails exactly
  `TestQueryCostFilters::test_a_call_at_exactly_until_is_out_while_one_at_exactly_since_is_in`,
  `TestMergeCostReports::test_the_merge_carries_the_period_end_of_its_inputs`,
  `TestQuerySegmentShares::test_until_narrows_the_shares_exactly_as_it_narrows_the_cost`
  — 3 failed, 116 passed. Restored to an empty porcelain; P2 (drop `until` from
  `_same_question`'s tuple) fails exactly
  `test_a_pair_covering_two_different_periods_is_refused_by_both_renderers`
  — 1 failed, 118 passed. Worktree removed and pruned, list back to one line.
- (j) `wc -l .agent/plan.md` → **43**. SLICE C verified byte for byte against
  the slice extracted from last_block.md.
- (k) `git status --porcelain` empty at handback; `git rev-list --left-right
  --count origin/<branch>...HEAD` → **0  0** after the last push.
- (l) `git diff --name-only 0d6c97aa..HEAD` → **38** paths, **0** matching
  `remedy-wt`.

## Findings
Open: **10** — R-0320, R-0322, R-0323, R-0324, R-0327, R-0328, R-0331, R-0333,
R-0334, R-0335. Next free ID **R-0336**. The worker authored no finding text;
the two live-review paragraphs are the block's SLICE A verbatim.

## Resume here
T003b — the prior-period comparison over the half-open period: the equal-length
window immediately before `since`, with "no comparison data" where that window
holds nothing. No CLI is wired and no `--until` validation exists; both are
T003c.

Fortschritt: 84 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung
