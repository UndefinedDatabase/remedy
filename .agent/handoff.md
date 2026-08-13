# Handoff — F115 Prompt breakdown & cost report · R18 (T003d) · STOP-ENDED

Branch `feature/f115-prompt-cost-report`; HEAD is the commit carrying this
file. NO PR exists; closure has NOT started. `.agent/STOP` is on disk (zero
bytes, mtime 2026-08-13 11:59, created by neither planner nor worker), so this
session ended at guardrail G6 of docs/agents/self_drive_protocol.md. A session
that ends at a stop signal with a written handoff is a SUCCESS.

## Rounds this session
| Round | Slice | Commits | Verdict |
|-------|-------|---------|---------|
| R18 | T003d/4 | `aff20fa3..b047aa38` (8682c987…b047aa38) | PASS WITH RISKS |
| close-out | — | `b047aa38..HEAD`, `.agent/**` only | state only, not a round |

The R18 verdict is on disk in `.agent/live_review.md` as the `Gate: R18` entry,
not only in this file — which every handback overwrites (R-0335).

## Item status (R18)
| Item | Status | Reason |
|------|--------|--------|
| C1 | done | |
| C2 | done | |
| C3 | done | applied verbatim; the REVIEWER's own text carried one false claim, registered as R-0338 |
| C4 | done | |
| C5 | done | |

## Changed files (R18)
| Path | Change |
|------|--------|
| `.agent/authored/f115-r18-1.md` | new, 350 lines |
| `.agent/last_block.md` | replaced, byte mirror of the block |
| `docs/guides/cost-report-user-guide-v0.md` | new, 142 lines |
| `docs/README.md` | +2 rows, -0 |
| `.agent/plan.md` | replaced, 42 lines |
| `.agent/handoff.md` | rewritten |

## Verification — re-run by the reviewer, not copied
cmp authored↔last_block exit 0, sha256 `2a93345b…d17940` over both, `wc -lc`
350 19149. The guide's fenced example is byte-identical to the T002 golden,
sha256 `ba48c81c…da138d` over both, 30 lines each; SLICE A equals the committed
guide. Catalog args `['--since','--until','--job','--by','--label','--project','--json']`,
`--all-projects` absent. Golden json: the ten keys the guide lists,
`report_version` 3, `unmeasured_notation` `'null'`. `COST_DEFAULT_LABEL =
"(unlabelled)"`. `grep -c cost-report-user-guide-v0.md docs/README.md` 2, C4
numstat `2 0`. `tests/docs/` 294 passed (baseline 294); canary 42 passed
(baseline 42); `test_cost_report.py` + `test_stats_report.py` 32 passed — the
run that binds the guide's example to the live renderer. `wc -l .agent/plan.md`
42, `0 0` against origin, no `remedy-wt` path in the change set,
`git worktree list` one line. At the moment of the verdict
`git status --porcelain` carried exactly one line, `?? .agent/STOP`.

## The work tree is dirty, and no agent of this session made it so
`git status --porcelain` NOW carries two lines: `?? .agent/STOP` (zero bytes,
mtime 11:59:11) and ` M scripts/make_review_zip.sh` (mtime 12:03:06). The
second is a one-line addition to that script's `find` prune list,
`-path './.remedy-wt' -o \`, which excludes the gitignored worktree scratch
directory from the review zip. It appeared AFTER the reviewer's own
post-R18 status check, which showed only `?? .agent/STOP`, and no commit of
this session touches the file — `git log 0d6c97aa..HEAD -- scripts/make_review_zip.sh`
is empty. It was neither committed nor reverted, deliberately: committing
another actor's unreviewed change into a feature branch and destroying their
uncommitted work are both worse than reporting it. Read it as operator work
in progress, alongside the STOP file that arrived four minutes earlier, and
confirm with the operator before touching it.

## Findings
Open: **12** — R-0320, R-0322, R-0323, R-0324, R-0327, R-0328, R-0331,
R-0333, R-0334, R-0336, R-0337, R-0338. Next free ID **R-0339**.
R-0338 is the only one with an on-disk fix pending.

## Resume here — repair FIRST, on THIS branch
1. R-0338: `docs/guides/cost-report-user-guide-v0.md` says "The existing
   `remedy stats cost` view already prints that limit in its own output." The
   note is `_ROLE_LIMIT_NOTE`, emitted only by `_render_cache_human`
   (`apps/cli/commands/stats_ledger_cmd.py:489`) and `_cache_payload:436` —
   `remedy stats cache --by role`. `stats report` never prints it.
2. Integration gate (docs/agents/integration_gate.md), full suite `-n auto`.
3. Closure per docs/roadmap/STATUS_closure_protocol.md.
The Open PR Gate has nothing to merge, so it does not block this resume.
Clear `.agent/STOP` only on the operator's instruction.

Deviations, declared: this handoff is 88 lines against the 60-line cap
(AGENTS.md DECISION D15). The cause is mandated content — the per-commit
table, the item-status table, the changed-files table and the re-run
verification values — and no section was dropped to meet the cap.

Fortschritt: 96 % (T001 ✅ · T002 ✅ · T003 ✅ — R-0338-Repair,
Integration-Gate und Closure offen) — Schätzung
