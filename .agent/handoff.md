# Handback — F080 R1 (sweep + claim + T001 + T002)

Branch: feature/f080-roadmap-mirror, pushed. No PR — F080's PR is
created only at closure. Open PR Gate: PR #182 merged (exactly one
open, feature/*→main, non-draft, MERGEABLE); main is now 1da1b07a and
the branch was cut from it.

## Changed files per commit
| Commit | Path | +/- | Reason |
|---|---|---|---|
| 6f529456 | docs/roadmap/features/T9_F163.md | +9/-0 | R-0200 appended as Carried findings |
| 6f529456 | docs/roadmap/features/T2_F085.md | +10/-0 | R-0202 appended as Carried findings |
| 6f529456 | docs/roadmap/features/T7_F135.md | +9/-0 | R-0204 appended as Carried findings |
| 6f529456 | .agent/candidates.md | +4/-23 | replaced: no open candidates + sweep provenance |
| 6f529456 | .agent/authored/f080-r1-{1..4}.md | new | receipts for the four applied texts |
| 5017822c | docs/roadmap/STATUS.md | +1/-1 | F080 `[ ]` → `[~]` (single line, A4 untouched) |
| 5017822c | .agent/live_review.md | +43/-95 | reset to the F080 round record |
| 5017822c | .agent/plan.md | +36/-... | F080 R1 state, operator constraint + sequence verbatim |
| 5017822c | .agent/context.md | +44/-... | branch/scope/constraints for F080 R1 |
| 5017822c | .agent/authored/f080-r1-{5,6}.md | new | receipts for the two applied texts |
| ba30d5f8 | packages/orchestration/roadmap_index.py | +484/-0 | parser, grammar validation, index writer |
| 9e462224 | packages/orchestration/roadmap_index.py | +49/-0 | Rule A5 readers (active/next/proposed/blockers) |
| 9e462224 | tests/orchestration/test_roadmap_index.py | +284/-0 | this repo + one fixture per violation class |
| 1e1f4352 | apps/cli/commands/plan_cmd.py | +154/-0 | `plan status` / `plan next` handlers |
| 1e1f4352 | apps/cli/command_catalog.py | +29/-0 | `plan` group + two read_only entries |
| 1e1f4352 | apps/cli/commands/__init__.py | +2/-1 | handler module registration |
| 1e1f4352 | tests/cli/test_plan_cli.py | +279/-0 | CLI surface + no-side-effects assertions |
| 79e7a5c3 | packages/orchestration/roadmap_index.py | +54/-2 | T002 consistency checks (report-only) |
| 79e7a5c3 | tests/orchestration/test_roadmap_index.py | +111/-2 | T002 tests incl. zero-findings on this repo |
| (final) | .agent/plan.md, .agent/handoff.md | rewrite | R1 done state + this handback |

Commit sizes: largest is ba30d5f8 at 484 lines. The parser and its
tests were split across ba30d5f8/9e462224 precisely to stay under the
500-line rule; no oversize commit in this feature.

## Authored-text receipts (.agent/authored/, R-0148)
All six saved and hash-verified before application:
| File | Computed sha256 | Match |
|---|---|---|
| f080-r1-1.md | 5c6240abcaa5a1ceab47cf8f795dc9df24aed274cc731f3fbbcaf3b161171fb1 | yes |
| f080-r1-2.md | 909d677c5343155f657ad8a33e4ffc58926ffe7311035154c9809277166a9486 | yes |
| f080-r1-3.md | 7415c6a2d45ccea9020a2a53d78d822a4e6389d8c2b759638d39ba34ee1aab54 | yes (see below) |
| f080-r1-4.md | 39e2c393cb1c221545bafa770fcc32d0f37ff8461411ae21fec787503b262eba | yes |
| f080-r1-5.md | 7ad1d02ebaa4176caa42af794bd45e019cb348c56848396eb7c15dc13649cb9b | yes |
| f080-r1-6.md | ed0dfe1dc47dbbb7b4233393552817183da014150ff7ee577654a0c21bffc8b5 | yes |

Text 3 first hashed 90a6fe162d1cca664947c3ee2fea4cee9c0f323ee9ab0648b7a9eab76d8d6dc2
— mismatch. Cause: display wrapping had split the pytest node id, so
`…ShareLogicalId` + a continuation line `entity::test_…` reached the
worker as two lines. Rejoining them into the single node id
`…::TestTwoRealRunsShareLogicalIdentity::test_different_execution_identities_same_logical_hash`
reproduced the declared hash exactly; nothing was reworded. Wrap is
recoverable, and the hash is what proved the recovery.

## Verification transcripts
    # PART 0 preconditions (before any edit)
    python3 -m pytest tests/docs/ -q                        -> 0 · 293 passed in 0.25s
    python3 -m pytest tests/cli/test_golden_path.py -q      -> 0 · 42 passed in 19.55s
    # PART A gate
    gh pr list --state open …            -> 1 PR: #182 feature/reg-f255-teacher-role→main, draft=false
    gh pr view 182 --json state,mergeable-> OPEN / MERGEABLE
    gh pr merge 182 --merge              -> 0
    git checkout main && git pull --ff-only -> 7007cf2a..1da1b07a (fast-forward)
    git checkout -b feature/f080-roadmap-mirror -> 0, worktree clean
    # PART B (after sweep)
    python3 -m pytest tests/docs/ -q                        -> 0 · 293 passed in 0.41s
    python3 -m pytest tests/cli/test_golden_path.py -q      -> 0 · 42 passed in 20.00s
    # PART C (after claim)
    python3 -m pytest tests/docs/ -q                        -> 0 · 293 passed in 0.25s
    python3 -m pytest tests/cli/test_golden_path.py -q      -> 0 · 42 passed in 19.37s
    python3 -m pytest tests/ui_server/test_dashboard_contract.py -q  -> 0 · 70 passed in 3.89s
    python3 -m pytest tests/regression/test_resource_safety.py -q    -> 0 · 21 passed in 10.96s
    # PART D gate (T001)
    python3 -m pytest tests/orchestration/test_roadmap_index.py -q   -> 0 · 20 passed in 0.17s
    python3 -m pytest tests/cli/test_plan_cli.py -q                  -> 0 · 21 passed in 3.50s
    python3 -m pytest tests/cli/test_golden_path.py -q               -> 0 · 42 passed in 19.42s
    # PART E gate (T002)
    python3 -m pytest tests/orchestration/test_roadmap_index.py -q   -> 0 · 30 passed in 0.21s
    python3 -m pytest tests/cli/test_plan_cli.py -q                  -> 0 · 21 passed in 3.50s
    python3 -m pytest tests/cli/test_golden_path.py -q               -> 0 · 42 passed in 19.41s
    # touched-surface extras (catalog change) + final state-file re-run
    pytest tests/cli/test_command_catalog.py tests/cli/test_cli_ux.py
           tests/test_grouped_cli.py tests/test_command_catalog.py -q -> 0 · 585 passed
    python3 -m pytest tests/docs/ -q                        -> 0 · 293 passed
    python3 -m pytest tests/ui_server/test_dashboard_contract.py -q -> 0 · 70 passed
    python3 -m pytest tests/regression/test_resource_safety.py -q   -> 0 · 21 passed
    python3 -m ruff check <all touched python files>        -> 0 · All checks passed
No red command this round; the STOP rule never fired.

## Real-run evidence (this repo, not a fixture)
`remedy plan status` → Active F080, blocker F070 [done], milestone
M2 "It builds itself", 255 features · 255 scheduled, "Consistency: no
findings", mirror written to <data root>/roadmap/index.json.
`remedy plan next` → F080, docs/roadmap/features/T1_F080.md, "State: in
progress (Rule A5: the active line) · docs/roadmap/STATUS.md:48",
"Proposal only — nothing was started."

## Open findings / questions
- 0 blocking. Next free finding id: R-0205.
- Open for R2/closure, deliberately out of this round's change scope:
  a docs/ entry for the new `plan` CLI group (AGENTS.md documentation
  rule). No test forces it; tests/docs/ is green.
- A9 spec note for the reviewer: `plan status`/`plan next` both report
  the `[~]` line as active and fall back to the first `[ ]` — recorded
  in the module and in the CLI docstring.

## Next expected action
Reviewer gates R1 on the next relay. Then R2: T003 feature→mission
adapter + one real feature file compiled end to end, zero jobs started.

## Item status
| Item | Status | Reason |
|---|---|---|
| Part 0 preconditions | done | both green before any edit |
| Part A Open PR Gate | done | #182 merged, main 1da1b07a, branch cut |
| Part B candidate sweep | done | commit 6f529456, texts 1–4 applied |
| Part C claim | done | commit 5017822c, texts 5–6 applied |
| Part D T001 | done | commits ba30d5f8, 9e462224, 1e1f4352 · gate green |
| Part E T002 | done | commit 79e7a5c3 · gate green |
| Handback | done | clean worktree, branch pushed, this file |
