# Handoff — F104 Hard budget enforcement, R7 (repair + integration gate)

Feature F104, round **R7**, branch `feature/f104-hard-budget-enforcement`, build
mode one-session self-drive, one delegated worker. R-0227 registered and fixed,
then the full integration gate. **Awaiting review.** No PR, no merge, no
force-push.

## Range
Review of `8e78c575..HEAD` (HEAD = this commit). `LAST_REVIEWED_SHA` is still
**549f2bac**: R6 (`549f2bac..8e78c575`) is tabled in the previous handoff and
also still awaits review.

## Commits

### d5411025 chore(f104): save the R7 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f104-r7-1.md | +140 | the R7 block, verbatim (item 1) |
| .agent/last_block.md | +130/-187 | same bytes; replaces the R6 block |

### 7949a251 chore(f104): register finding R-0227 before fixing it
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +19/-1 | R-0227 appended verbatim; next free ID → R-0228 |

### d3fe8011 fix(f104): make a failed budget ledger read say so (R-0227)
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/job.py | +32/-2 | ERROR log + `_cost_read_error` → `cost_read:` text line + `cost_read_error` JSON key |
| tests/orchestration/test_job_budgets.py | +66 | 4 pins driving the REAL command via capsys/caplog |

### dcd85d0a chore(f104): record the R7 integration gate and its attribution
| Path | +/- | Reason |
|---|---|---|
| .agent/gate_f104_r7/ | +344 | 10 files: both run logs, both FAILED lists, both comm lists, the serial re-run, dist parity, worktree cleanup, attribution |

### (this commit) chore(f104): record the R7 state and hand back
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +19/-1 | `Done: R-0227` + the R7 `## Steps` line, authored text verbatim |
| .agent/plan.md | +42/-24 | rewritten, 50 lines, R7-complete-awaiting-review |
| .agent/handoff.md | rewrite | this file (template self-reference exception) |

## External actions
`git worktree add -b tmp/base-gate .remedy-wt/base_gate_f104_r7 94f69b0f` → ok.
`git worktree remove --force` + `git worktree prune` + `git branch -D
tmp/base-gate` → each exit 0; transcript in `gate_f104_r7/worktree_cleanup.txt`.
`git push -u origin feature/f104-hard-budget-enforcement` → `8e78c575..HEAD`.
No PR, no merge, no gh command.

## Verification
Run by me from the repo root, real exit codes:

| Gate | Command | Exit | Result |
|---|---|---|---|
| A | `pytest tests/orchestration/test_job_budgets.py -q` | **0** | 135 passed in 30.52s |
| B | `pytest tests/orchestration/test_predictive_budget.py tests/orchestration/test_budget_guard.py -q` | **0** | 167 passed in 4.28s |
| C | `pytest tests/cli/test_golden_path.py -q` (canary) | **0** | 42 passed in 19.33s |
| D | gate, BRANCH: `REMEDY_UI_NO_AUTO_BUILD=1 pytest -n auto -q` | **0** | 16305 passed, 19 skipped in 120.14s; wall 121 s |
| D | gate, BASE @ 94f69b0f, same command in the worktree | **1** | 6 failed, 16125 passed, 19 skipped in 122.66s; wall 123 s |

`comm -13` BRANCH-ONLY: **0 ids** — `comm_branch_only_failures.txt` is a 0-byte
file and that is the evidence. Nothing to re-run, nothing to classify, and the
step-4 blocker rule cannot fire.
`comm -23` BASE-ONLY: **6 ids**, all
`tests/ui_server/test_live_state.py::TestUIServerIntegration::` —
`test_server_starts_and_writes_info`, `test_url_is_localhost_only`,
`test_api_invalid_token_403`, `test_api_missing_job_404`, `test_put_rejected`,
`test_dashboard_no_raw_leaks`. Attribution for each of the six, identical:
serial re-run at base PASSES with a fresh dist (6 passed in 0.86s); FAILS when
the dist mtimes are pushed back behind `apps/ui/src` without one byte changing
(6 failed in 30.44s, each with "ERROR: React UI not built."); PASSES again when
restored (6 passed in 0.83s) — dist content hash `fb68a729…` identical in all
three. Classification: pre-existing **environment / R-0221 dist-mtime class**;
not xdist-flake, not feature-coupled. Attributed, not chased.

## Authored-text proofs
`cmp .agent/authored/f104-r7-1.md .agent/last_block.md` → **exit 0**. The R-0227
finding text and the R7 `## Steps` line were applied verbatim.

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 save the block | done | cmp exit 0 |
| 2 persist R-0227 | done | own commit, before any fix |
| 3 fix R-0227 + pins | done | 4 new tests, all through the real command |
| 4 integration gate | done | 0 branch-only; 6 base-only all attributed |
| 5 state files + handback | deviated | `.agent/context.md` untouched — see D2 |

## Open findings
**1** — R-0221 (Low, carried, not F104's to fix, F252 flake-debt class).
R-0227 carries a worker `Done: R-0227` and awaits the reviewer's own text.

## State
`git status --porcelain` **EMPTY**; branch pushed; `git worktree list` shows
ONLY the primary checkout; `tmp/base-gate` deleted; `docs/roadmap/STATUS.md`
and `ROADMAP.md` untouched, F104 still `[~]`.

## Deviations & assumptions — declared
- **D1 (item 4).** `REMEDY_UI_NO_AUTO_BUILD=1` was set on BOTH suite runs, not
  the base run alone, so step 2's "identical command" holds (F103 R5
  precedent). It is not claimed as a full neutralization: R-0221 pops the
  variable and builds for real, which is the entire cause of the six base-only
  ids. Parity was therefore also proven by content hash and each id attributed.
- **D2 (item 5).** `.agent/context.md` untouched — its round numbering (R7
  gate → R8 closure) is still correct, so the block's stated condition for
  editing it is not met.
- **D3 (item 4).** The committed run logs are trimmed to head + decisive tail +
  one verbatim failure excerpt (F103 R5 precedent). The raw 234-line and
  612-line dot-progress logs stay in the gitignored `.remedy-wt/` scratchpad,
  which is where they were written while the suites ran (R-0176).
- **D4 (item 4).** `base_serial_rerun.txt` PASS 1 printed a wrong header
  ("NEGATIVE CONTROL"); it is the POSITIVE control. The header is corrected in
  place and the correction is stated inside the file. No command re-run, no
  number altered.
- Largest commit: 344 insertions (dcd85d0a). Under the 500 cap; nothing split.
- **This handoff is 124 lines** (AGENTS.md D15 stated cause): five per-commit
  changed-files tables, the five-row gate table, the full per-id base-only
  attribution the gate mandates, the item-status table and four declared
  deviations. No section dropped.

## Next
**R8 — closure** per docs/roadmap/STATUS_closure_protocol.md, once the reviewer
has gated R6 and R7.
