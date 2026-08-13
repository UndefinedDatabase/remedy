# Handoff — F115 Prompt breakdown & cost report · Round 17 (T003c/4)

Branch `feature/f115-prompt-cost-report`, HEAD `f6677195` before this commit.
Started clean at `aa7ad8df`. NO PR exists; closure has NOT started.
Deviations, declared: this file is **99 lines**, over the block's 60-line cap
and within AGENTS.md's ≤100 allowance for a >5-commit round (DECISION D15).
Cause is mandated content: the C1..C7 item-status table with a reason for each
`deviated` item, the seven-row commit table, the eight-row changed-files table
and twelve gate values (a)..(l), two of which carry an ordered baseline and
one a probe NAME list. No section is dropped.

## Item status (R17)
| Item | Status | Reason |
|------|--------|--------|
| C1 | done | own commit, FIRST of the round |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | deviated | ordered content complete; ALSO the module docstring, which said "Three commands" and never named `stats cache` — adding a fifth command under a false count would have left a wrong claim on disk beside new code |
| C6 | deviated | the six ordered properties are one test each; FOUR more tests were added because gate (k) orders the wiring proven "the way the suite does" and that proof is a test. The fixtures `data_root`/`project_id`/`ledger_path` are IMPORTED from `tests/cli/test_stats_cost.py`; only the evidence tree is new, because this command needs two adjacent windows, a second job present in only one of them, and a prompt trace |
| C7 | done | |

## Commits — R17
| SHA | Item | Subject |
|-----|------|---------|
| 7899fdb0 | C1 | record the R16 gate verdict against R-0336 |
| bfbfd1b1 | C2 | save the R17 authored block verbatim |
| aee34ee6 | C3 | mirror the R17 block into last_block |
| a8459693 | C4 | add the stats report entry to the command catalog |
| e38fc1b2 | C5 | render the cost report from a stats report handler |
| f6677195 | C6 | pin the cost report CLI and its prior-period comparison |
| (this commit) | C7 | refresh the plan and write the R17 handoff |

## Changed files
| Path | Items |
|------|-------|
| .agent/live_review.md | C1 — append only, 2 insertions, 0 deletions |
| .agent/authored/f115-r17-1.md | C2 (new, 228 lines) |
| .agent/last_block.md | C3 |
| apps/cli/command_catalog.py | C4 — 31 insertions, 0 deletions |
| apps/cli/commands/stats_ledger_cmd.py | C5 — 114 insertions, 5 deletions |
| tests/cli/test_stats_report.py | C6 (new, 246 lines, +10 tests) |
| .agent/plan.md, .agent/handoff.md | C7 |

## Gates — real measured values
- (a) `cmp .agent/authored/f115-r17-1.md .agent/last_block.md` exit **0** —
  this session's sandbox ALLOWED `cmp`, unlike R14/R16 — corroborated by
  `sha256sum`, BOTH files
  `86e36a908de1a25dd126a96849407636fb952d8e39e4a87407ea0ab4502c70a9`, and by a
  python byte compare printing `True 17476 17476`. `wc -lc` → **228 17476**.
- (b) `git show 7899fdb0 -- .agent/live_review.md`: `^+Done: R-0336` **1**.
  `git show --numstat 7899fdb0` → **2  0**, ZERO deletions. Whole file after
  C1: `^Done:` **10**, `^- R-0` **17**, `^## Steps` **1**, `^Landed:` **0**.
- (c) `git log --oneline aa7ad8df..HEAD`, newest first: f6677195, e38fc1b2,
  a8459693, aee34ee6, bfbfd1b1, **7899fdb0** — C1 is LAST, the oldest.
- (d) `python3 -m ruff check` over the three python files this round touches
  (`command_catalog.py`, `stats_ledger_cmd.py`, `test_stats_report.py`) →
  `All checks passed!`, exit 0.
- (e) `pytest tests/cli/test_stats_report.py -q` → **10 passed**.
- (f) `pytest tests/cli/test_stats_cost.py -q` → baseline BEFORE C5 **41
  passed**, after C5 **41 passed**. No count and no assertion moved.
- (g) `pytest tests/test_command_catalog.py tests/test_grouped_cli.py -q` →
  baseline BEFORE C4 **505 passed**, after C4 **505 passed**. Both parametrise
  over GROUPS, not commands, so an entry in an existing group adds no case.
- (h) Canary `pytest tests/cli/test_golden_path.py -q` → **42 passed**.
- (i) `pytest tests/orchestration/test_cost_report.py
  tests/orchestration/test_token_ledger.py -q` → **134 passed**. Neither
  module was touched.
- (j) One disposable worktree `.remedy-wt/f115-r17-probe`, detached at
  f6677195. The prior `query_cost` was given `job_id=None` in place of the
  report's job. EXACTLY ONE test fails, by name:
  `TestPriorPeriodComparison::test_a_job_filter_narrows_the_prior_query_too`
  (`assert True is False` on `comparison["available"]`). Worktree removed and
  pruned; `git worktree list` shows one line.
- (k) The `remedy` binary was NOT invoked — it is refused by this session's
  sandbox — so no `--help` output is quoted. The wiring is proven the way the
  suite proves it: `get_command("stats.report")` resolves as `read_only` and
  `supports_json`, its arg names are exactly `--since --until --job --by
  --label --project --json` with NO `--all-projects`, `"stats.report"` is in
  both `CMD.COMMAND_HANDLERS` and `collect_all_handlers()`, and dispatching an
  argparse Namespace through the handler returns `filters.by == "role"`.
- (l) `wc -l .agent/plan.md` → **41**. SLICE B was extracted from the committed
  `.agent/authored/f115-r17-1.md` and compared with `cmp`: exit 0, sha256
  `340b76230f162af21ef95ef38ac240ac9c4e6cbcb12b1c4ecfde784ba3d729d5` both
  sides. `git status --porcelain` empty at handback;
  `git rev-list --left-right --count origin/<branch>...HEAD` → **0  0**;
  `git diff --name-only 0d6c97aa..HEAD` → **43** paths, **0** matching
  `remedy-wt`.

## Findings
Open: **10** — R-0320, R-0322, R-0323, R-0324, R-0327, R-0328, R-0331, R-0333,
R-0334, R-0336. Next free ID **R-0337**. The worker authored no finding text;
the live-review paragraph is SLICE A, applied byte for byte.

## Resume here
T003d — the docs page `remedy stats report` now needs, registered in the
`docs/README.md` index in the same PR. Then the integration gate, then closure.

Fortschritt: 93 % (T001 ✅ · T002 ✅ · T003 fast fertig) — Schätzung
