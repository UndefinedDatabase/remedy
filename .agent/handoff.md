# Handoff — F115 Prompt breakdown & cost report · Round 18 (T003d/4)

Branch `feature/f115-prompt-cost-report`, base `aff20fa3`. NO PR, no merge, no
force-push. Docs-only round: the guide for `remedy stats report` plus its index
rows. No code, no test added.

## Commits
| # | SHA | Subject | Pushed |
|---|-----|---------|--------|
| C1 | `8682c987` | chore(f115): save the R18 block as the authored round text | yes |
| C2 | `23dd690b` | chore(f115): mirror the R18 block into the last-block state file | yes |
| C3 | `3715a76c` | docs(f115): add the cost report user guide | yes |
| C4 | `ec673f2d` | docs(f115): register the cost report guide in the docs index | yes |
| C5 | this commit | chore(f115): refresh the plan and write the R18 handoff | yes |

## Changed files
| Path | Change | Reason |
|------|--------|--------|
| `.agent/authored/f115-r18-1.md` | new | R18 block verbatim |
| `.agent/last_block.md` | replaced | byte mirror of the block |
| `docs/guides/cost-report-user-guide-v0.md` | new | SLICE A verbatim, 142 lines |
| `docs/README.md` | +2 rows | quick-find + Guides registration |
| `.agent/plan.md` | replaced | SLICE C verbatim |
| `.agent/handoff.md` | rewritten | this file |

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C1 | done | |
| C2 | done | |
| C3 | done | every claim checked against source before commit; none false |
| C4 | done | |
| C5 | done | |

## Gate values (measured, with baselines)
- (a) `cmp` ran and was silent → byte identical. sha256 of BOTH:
  `2a93345b696dffc6768ac45ab5bcbb7287b6b0e154ca203bfd1cbb9efad17940`.
  `wc -lc .agent/last_block.md` → `350 19149`.
- (b) `test -f` exit 0; `wc -l` → **142**.
- (c) The ordered `diff <(awk …) …` was REFUSED: "Contains process_substitution".
  Substitute: the same awk filter replicated in python3 into
  `.remedy-wt/f115-r18-worker/extracted.md`, then `diff <that> <golden>` →
  **exit 0, no output**; `cmp` on the same pair also silent.
- (d) `COMMAND_CATALOG` does not exist (ImportError). Real name found by the
  ordered grep: `CATALOG`. Printed list:
  `['--since', '--until', '--job', '--by', '--label', '--project', '--json']`
  — the guide names exactly these seven; `--all-projects` in neither.
- (e) `['buckets', 'comparison', 'filters', 'label', 'ledger_exists', 'note', 'report_version', 'segments', 'total', 'unmeasured_notation']`
  then `3 'null'` — same set, same spelling, same version and notation word.
- (f) `grep -c` → `docs/guides/cost-report-user-guide-v0.md:1`,
  `packages/orchestration/cost_report.py:1`; `COST_DEFAULT_LABEL = ` count 1,
  line 64 `COST_DEFAULT_LABEL = "(unlabelled)"` — the guide states `(unlabelled)`.
- (g) `git show --numstat ec673f2d -- docs/README.md` → `2	0	docs/README.md`;
  `grep -c` → **2**; added rows `^+|` → **2**; each FROM anchor 1x and each
  TO-only line 1x in the whole file (python line count).
- (h) `git diff --name-only aff20fa3..HEAD` → exactly the six Constraints paths;
  `.agent/live_review.md` absent, as the Findings clause requires.
- (i) `python3 -m pytest tests/docs/ -q` → **294 passed** (baseline 294).
- (j) `python3 -m pytest tests/cli/test_golden_path.py -q` → **42 passed** (42).
- (k) `wc -l .agent/plan.md` → 42 (<50); `git status --porcelain` empty;
  `rev-list --left-right --count` → `0	0`; no `remedy-wt` path in
  `git diff --name-only 0d6c97aa..HEAD`.
- (l) `remedy stats report --help` REFUSED: "This command requires approval".
  No output fabricated; the flag list rests on gate (d).

## Findings
Open: **11** — R-0320, R-0322, R-0323, R-0324, R-0327, R-0328, R-0331, R-0333,
R-0334, R-0336, R-0337. Next free ID **R-0338**. This round registered none.

## Next expected action
Reviewer re-runs (a)..(l). Then the integration gate
(docs/agents/integration_gate.md, full suite `-n auto`, R-0322's five
pre-existing reds expected), then closure per
docs/roadmap/STATUS_closure_protocol.md.

Deviations, declared (DECISION D15): this file is 82 lines. The overage is the
mandated content itself — the per-commit table, the changed-files table, the
item-status table and all twelve gate values (a)..(l) with their baselines and
two sandbox-refusal records. No section was dropped.

Fortschritt: 96 % (T001 ✅ · T002 ✅ · T003 ✅ — Integration-Gate + Closure
offen) — Schätzung
