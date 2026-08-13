# Handoff — F045 Loop definitions · ROUND 3 HALTED on a block/disk contradiction

A round that stops at an honest blocker with a written handoff is a success.
Session type: one-session self-drive (docs/agents/self_drive_protocol.md).

Deviations, declared: 100 lines, over the 60-line cap. Cause: the mandated
item-status table (one row per R3 block ITEM 1-11), the mandated gate table
(11 rows) and the two blocker statements, which are the round's only product.
No section is dropped. Second deviation: ITEM 1 was split into TWO commits —
writing both files in one is 654 insertions, over the AGENTS.md 500-insertion
cap, so the block's own budget clause ("if any one exceeds it, split and
declare") applies.

## State
Branch `feature/f045-loop-definitions`, cut from main at `cb3ef34f`. No PR open,
nothing merged, main untouched, no force-push, no worktrees. HEAD `eadad2db`;
LAST_REVIEWED_SHA `3f92fbcd`. R1 PASS at `fbd5168b`, R2 PASS at `3f92fbcd`, R3
HALTED. `.agent/STOP` re-read from disk at round start and at handoff: ABSENT.
Open findings: 4 (R-0344..R-0347). Next free finding ID: R-0348.

## Commits this round
| SHA | Subject | Files | Insertions |
|---|---|---|---|
| `0ff5e71e` | chore(f045): save the R3 block verbatim | `.agent/authored/f045-r3-1.md` | 338 |
| `eadad2db` | chore(f045): point last_block at the R3 block | `.agent/last_block.md` | 315 |
| (this one) | docs(f045): halt round 3 on the decision-record blocker | `.agent/plan.md`, `.agent/handoff.md` | see history |

## BLOCKER 1 — ITEM 3, DECISION F045 D5, verbatim and wrong
D5's rationale is contradicted by the file it describes.
`packages/orchestration/mission_state.py` docstring lines 175-179 state that
`mission_plan` (F069) is an ADDITIVE, OPTIONAL field added to the frozen
`Mission` dataclass "which is why :data:`MISSION_SCHEMA_VERSION` does NOT move
for it." D5 asserts the opposite general rule — provenance "could only be added
as a NEW FIELD, which moves that schema version" — with a live counterexample
in the same class. Its reversal clause ("bumping `MISSION_SCHEMA_VERSION`")
would break every stored mission: `Mission.from_json` line 217 refuses any
record whose `version != MISSION_SCHEMA_VERSION`. Its field enumeration also
omits `dossier_ref` (line 190) and `mission_plan` (line 192).
ITEM 3 orders those bytes written verbatim, so the worker cannot repair them.
D5's CONCLUSION (loop_ref rides on the JOB) is unaffected — only the stated
reason and the reversal instruction are.

## BLOCKER 2 — ITEM 8 names a function that does not exist
ITEM 8 orders `job.mission = mission.goal` "the shape
`mission_state.start_follow_up` already uses". `grep -rn "start_follow_up" .
--exclude-dir=.git` returns NOTHING. The function that sets `job.mission` is
`mission_state.continue_mission` (line 946-954). Repairable by naming the real
owner, but not silently: this is the R-0338/R-0342/R-0343 family.

## Gates actually run (real exit codes, real output)
| Gate | Command | Exit | Output |
|---|---|---|---|
| (a) | `cmp .agent/authored/f045-r3-1.md .agent/last_block.md` | 0 | (none) |
| (b) | `grep -c "^Done: R-0344" .agent/live_review.md` | 1 | `0` |
| (c) | `grep -c "^Done: R-0347" .agent/live_review.md` | 1 | `0` |
| (d) | `grep -c "^## DECISION F045 D" .agent/decisions.md` | 0 | `3` |
| (e) | `grep -c "re-reads" docs/agents/self_drive_protocol.md` | 1 | `0` |
| (f) | `pytest tests/orchestration/test_loop_run.py test_loop_spec.py -q` | 0 | `23 passed in 0.14s` |
| (g) | `pytest tests/test_agent_tooling.py -q` | 0 | `10 passed, 1 skipped in 0.04s` |
| (h) | `pytest tests/docs/ -q` | 0 | `294 passed in 0.19s` |
| (i) | `pytest tests/cli/test_golden_path.py -q` (canary) | 0 | `42 passed in 15.94s` |
| (j) | `ruff check` the four loop files | 0 | `All checks passed!` |
| (k) | `git status --porcelain` | 0 | empty at each commit |

(b)-(e) miss the block's expected values BECAUSE the round halted after ITEM 1:
nothing was written to `.agent/live_review.md`, `.agent/decisions.md` or
`docs/agents/self_drive_protocol.md`. (f)-(k) describe the tree at `eadad2db`.

## Item status (R3 block)
| Item | Status | Reason |
|---|---|---|
| ITEM 1 | deviated | done, but split into two commits for the 500-insertion cap |
| ITEM 2 | skipped | halted; its R-0346/R-0347 `Done:` lines assert D4/D5 and the protocol edit landed, which they did not |
| ITEM 3 | skipped | BLOCKER 1 — verbatim D5 text contradicts mission_state.py |
| ITEM 4 | skipped | halted; unaffected by either blocker |
| ITEM 5 | skipped | halted; unaffected by either blocker |
| ITEM 6 | skipped | halted; unaffected by either blocker |
| ITEM 7 | skipped | halted; unaffected by either blocker |
| ITEM 8 | skipped | BLOCKER 2 — names `mission_state.start_follow_up`, which does not exist |
| ITEM 9 | skipped | depends on ITEM 8 |
| ITEM 10 | deviated | plan + handoff rewritten to the HALT state, not the "R3 done" state the item dictates |
| ITEM 11 | deviated | every gate run and recorded; (b)-(e) observed at their halted values |

## Verified against disk, do not re-derive
- Every factual claim in ITEM 2's four `Done:` lines checks out as written:
  `test_loop_spec.py:115` and `:265` are the lines named, the three DECISION
  headings sit at 4626/4648/4664, `re-reads` grepped 0, and the five R2 commits
  are 5/59/168/182/74 insertions (the R2 block-save commit `f99a3407`, 491, is
  a sixth the enumeration omits; still under the cap).
- `storage.list_jobs_safe(root)` sorts by `created_at` reverse=True — the
  DESCENDING claim in ITEM 8 is correct.
- The feature file's A9 line is about goal templates, as DECISION D4 says.

## Next session starts here
FIRST action is Phase 1 rule 1 — read `.agent/STOP` from disk. THEN Phase 1
rule 2, the Open PR Gate. Then the reviewer reissues ITEM 3's D5 with a
rationale that matches `mission_state.py` and ITEM 8 with the real function
name; the rest of the block needs no change.

Fortschritt: ~35 % (T001 ✅ · T002 ✅ · T003 offen) — Schätzung
