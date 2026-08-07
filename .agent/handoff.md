# Handback — F254 R7 (worker)

Feature T2_F254 · Round R7 · Branch `feature/f254-model-alias-table`
Review range ac54592c..HEAD. Commit 1 `0ea95c88`, commit 2 = this handoff.

## Changed files (generated: `git diff --numstat ac54592c..HEAD`)
| Path | + | - |
|---|---|---|
| .agent/authored/f254-r7-1.md | 126 | 0 |
| .agent/authored/f254-r7-2.md | 80 | 0 |
| .agent/live_review.md | 77 | 11 |
| .agent/plan.md | 16 | 11 |
| .agent/handoff.md | rewritten (commit 2, self-reference) | |

## A — transport proofs
`cp` then `cmp` against the reviewer's scratchpad originals: both exit 0.
sha256 (original == applied, identical both sides):
f254-r7-1.md `7fae7e27a67442bafb43e94975069947bd1749155457bd7c1ea3177ab9535a77`
f254-r7-2.md `451c83da70bd076036f6cccde513d7d602c47501a04ee97588fe7150334f8c5f`

Six pairs, all REWRITE-shaped, pre → post:
| Receipt | Pair | pre FROM/TO | post FROM/TO |
|---|---|---|---|
| f254-r7-1 → live_review.md | 1 | 1x / 0x | 0x / 1x |
| f254-r7-1 → live_review.md | 2 | 1x / 0x | 0x / 1x |
| f254-r7-1 → live_review.md | 3 | 1x / 0x | 0x / 1x |
| f254-r7-2 → plan.md | 1 | 1x / 0x | 0x / 1x |
| f254-r7-2 → plan.md | 2 | 1x / 0x | 0x / 1x |
| f254-r7-2 → plan.md | 3 | 1x / 0x | 0x / 1x |

Structure: live_review.md keeps `## Steps`, `## Findings`, `## Decisions`,
`## Verdicts`, 1x each. plan.md keeps `## Goal` and `## Next Steps`.

## B — integration gate (docs/agents/integration_gate.md)
Branch run, repo root at 0ea95c88, command `python3 -m pytest -n auto -q`:
exit **1** · **1 failed, 16015 passed, 19 skipped** · 128.16s (wall 129s).
Base run, throwaway worktree on branch `tmp/base-gate` at merge-base
`fc023265`, parity restored by `cp -a` of apps/ui/node_modules and
apps/ui/dist (copied, not symlinked), `REMEDY_UI_NO_AUTO_BUILD=1`,
same command: exit **1** · **5 failed, 15950 passed, 19 skipped** · 147.03s.
dist hash before == after (`5ff2033ab95c…`) — no rebuild at base, so the
auto-build neutralization is verified, not assumed. Neither run reported
xfail. Both under the ~5 min budget, so no perf pass is owed.

`comm -13` branch-only failures: **0**. `comm -12` both: 1. `comm -23`
base-only: 4.

| Node id | Branch | Base | Attribution |
|---|---|---|---|
| tests/orchestration/test_product_smoke.py::test_no_zombie_processes_after_every_outcome | FAIL | FAIL | pre-existing, present at merge base; serial re-run on branch exit 0 (1 passed) ⇒ xdist-flake class, not branch-caused |
| tests/ui_server/test_live_state.py::TestUIServerIntegration::test_server_starts_and_writes_info | pass | FAIL | environment class |
| …::test_app_shell_served_without_token | pass | FAIL | environment class |
| …::test_api_invalid_token_403 | pass | FAIL | environment class |
| …::test_api_missing_job_404 | pass | FAIL | environment class |

`comm -23` attribution, per id by direct evidence: each of the four
captured stderr names the missing artifact — "ERROR: React UI not built …
cd apps/ui && npm install && npm run build" — the apps/ui build-output
class of the R-0155/R-0158 amendment. Proven not genuine base failures:
re-run at base in isolation, 16 passed serial and 42 passed under
`-n auto` three times. The asymmetry has a measured cause: the full suite
invalidates apps/ui/dist mid-run, and the primary checkout's
dist/index.html mtime 1786117392 falls inside the branch-run window
(1786117307..1786117436), i.e. the branch run silently rebuilt it, while
at base the env var correctly suppressed that rebuild.

Cleanup: `git worktree remove --force` 0, `git worktree prune` 0,
`git branch -D tmp/base-gate` 0. `git worktree list` shows the primary
only; no `tmp/*` branch remains; `git status --porcelain` empty. No stray
pytest, npm or ui_server process (`ps -eo pid,cmd` checked, none).

## Deviations
1. `grep -c '^- R6' .agent/live_review.md` is **2**, not the block's
   expected 1 — receipt f254-r7-1 PAIR 3 turns the Verdicts line
   `- R6: PENDING` into `- R6: PASS …`, itself a `^- R6` line, so the
   check cannot return 1 while an R6 verdict exists. R-0216's substance
   holds: inside `## Steps` the count is exactly 1 and the duplicate
   bullet is gone.
2. `.agent/plan.md` is **54 lines**, over the block's "under 50" and over
   AGENTS.md's <50 cap. Cause is the authored text: f254-r7-2's TO blocks
   are net +5 lines. Not repairable without editing outside an authored
   FROM/TO, which the worker may not do. Reviewer's call.
3. integration_gate.md §2 copies gate logs into a `.agent/gate_*` evidence
   dir; the block's Change list forbids any path beyond the five named, so
   the logs stayed in the session scratchpad only and no `.agent/gate_*`
   was created. Files: branch_run, base_run, branch_failed, base_failed,
   branch_serial, dist_before, dist_after (all `.txt`).

4. This handoff is **111 lines**, 51 over the 60-line target and 11 over
   the 100-line ceiling, with no >5-commit table to justify it. Recorded
   as measurement, not excuse — it is R-0214's evidence, fourth running.

Observation (no code change made, per the block): the full suite rewrites
`apps/ui/dist` in the primary checkout while it runs. It touches no
tracked file, but it is the R-0169/R-0176 class and is why a base run
needs the env var. Worth a finding, not a fix here.

## Item status
| Item | Status | Reason |
|---|---|---|
| A receipts + R-0216 fix | done | commit 0ea95c88, before the gate |
| B integration gate | done | RED, reported; 0 branch-only failures |
| C record + handoff | done | this file, commit 2 |

Open findings: 0 (R-0216 registered and Done). Next free ID R-0217.
No PR created, STATUS line untouched — closure is R8.

## Next expected action
Reviewer re-reads ac54592c..HEAD, re-runs whatever gate evidence it
chooses to distrust, and issues the R7 verdict into
`.agent/live_review.md`. No failure is attributable to this branch.
