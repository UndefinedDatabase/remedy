# Handoff — F045 Loop definitions · ROUND 4 COMPLETE

Session type: one-session self-drive (docs/agents/self_drive_protocol.md).

Deviations, declared: 81 lines, over the 60-line cap. Cause: the mandated
per-commit table (8 rows), the mandated gate table (12 rows) and the mandated
item-status table (9 rows) are 29 rows plus headers on their own. No section is
dropped. No other deviation: every ITEM landed as ordered, every gate was run.

## State
Branch `feature/f045-loop-definitions`, cut from main at `cb3ef34f`. No PR open,
nothing merged, main untouched, no force-push, no worktrees. HEAD is the C7
commit below; LAST_REVIEWED_SHA `3f92fbcd`. R1 PASS at `fbd5168b`, R2 PASS at
`3f92fbcd`, R3 HALTED at `7912bbdb`, R4 complete.
`.agent/STOP` re-read from disk at round start and after the last gate: ABSENT.
Open findings: 2 (R-0348, R-0349). Next free finding ID: R-0350.

## Commits this round
| SHA | Subject | Files | Ins |
|---|---|---|---|
| `99ecc0c5` | chore(f045): save the R4 block verbatim | `.agent/authored/f045-r4-1.md` | 246 |
| `aa019a46` | chore(f045): point last_block at the R4 block | `.agent/last_block.md` | 158 |
| `ab45dd05` | docs(f045): register R-0348 and R-0349, the R3 block defects | `.agent/live_review.md` | 4 |
| `548d2212` | docs(agents): give the stop sentinel a re-check point | `docs/agents/self_drive_protocol.md` | 7 |
| `6c177365` | docs(f045): record decisions D4 and D5 | `.agent/decisions.md` | 58 |
| `0b1dba47` | feat(f045): validate the mission action's goal template | `packages/orchestration/loop_spec.py` | 8 |
| `09121164` | test(f045): pin the mission template validation | `tests/orchestration/test_loop_spec.py` | 24 |
| `a4d31b87` | docs(f045): resolve R-0344 to R-0347 | `.agent/live_review.md` | 8 |
| (this one) | docs(f045): update the plan and handoff for R4 | `.agent/plan.md`, `.agent/handoff.md` | see history |

Every commit is under its block budget and under the AGENTS.md 500-insertion
cap. Each was pushed immediately after it was made.

## Gates actually run (real exit codes, real output)
| Gate | Command | Exit | Output |
|---|---|---|---|
| (a) | `cmp .agent/authored/f045-r4-1.md .agent/last_block.md` | 0 | (none) |
| (b) | `grep -c "^- R-0348 — Medium" .agent/live_review.md` | 0 | `1` |
| (c) | `grep -c "^- R-0349 — Medium" .agent/live_review.md` | 0 | `1` |
| (d) | `grep -c "^Done: R-" .agent/live_review.md` | 0 | `4` |
| (e) | `grep -c "^## DECISION F045 D" .agent/decisions.md` | 0 | `5` |
| (f) | `grep -c "re-reads" docs/agents/self_drive_protocol.md` | 0 | `1` |
| (g) | `pytest test_loop_spec.py test_loop_run.py -q` | 0 | `25 passed in 0.15s` |
| (h) | `pytest tests/test_agent_tooling.py -q` | 0 | `10 passed, 1 skipped in 0.03s` |
| (i) | `pytest tests/docs/ -q` | 0 | `294 passed in 0.19s` |
| (j) | `pytest tests/cli/test_golden_path.py -q` (canary) | 0 | `42 passed in 15.82s` |
| (k) | `ruff check loop_spec.py test_loop_spec.py` | 0 | `All checks passed!` |
| (l) | `git status --porcelain` | 0 | empty |

(f) printed `0` before the C2 edit and `1` after, so the R-0347 gap was proved
real before it was closed. (g) was 23 before C5 and 25 after, the two added
tests.

## Item status (R4 block)
| Item | Status | Reason |
|---|---|---|
| ITEM 1 | done | two commits as ordered, `cmp` exit 0 |
| ITEM 2 | done | R-0348 and R-0349 appended verbatim after R-0347 |
| ITEM 3 | done | FROM found once at line 64; TO contains it verbatim |
| ITEM 4 | done | D4 and D5 appended at the very end, nothing above changed |
| ITEM 5 | done | FROM matched `_semantic_errors` exactly; TO contains it |
| ITEM 6 | done | two tests, `_write` reused, both assert whole lists |
| ITEM 7 | done | four `Done:` lines; R-0348/R-0349 left without one |
| ITEM 8 | done | this commit |
| ITEM 9 | done | all twelve gates run; values above are OBSERVED |

## For the reviewer — one falsifiable claim in the block
The block's Insertion-budget clause states that ITEM 1 was split "because one
commit carrying both copies of the block exceeds the 500-insertion cap". The
disk says otherwise: C0a is 246 insertions and C0b is 158, so one combined
commit would have been 404, under the cap. The SPLIT itself is correct and was
followed as ordered — two small commits beat one — but the stated reason is
arithmetic the block did not compute. Reported, not silently corrected.

## Next session starts here
FIRST action is Phase 1 rule 1 — read `.agent/STOP` from disk. THEN Phase 1
rule 2, the Open PR Gate. Then R5: the dispatch — `run_loop`, the inert-trigger
notice on the run path, the shared job builder both action kinds use, and
`last_run_for_loop`. R6 is the CLI.

Fortschritt: ~45 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung
