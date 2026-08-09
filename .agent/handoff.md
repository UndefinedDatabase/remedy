# Handoff — F105 R9 (T003 inventory)

F105 Cache-optimal prompt ordering, R9: record the R8 gate, resolve R-0233 and
R-0234 with the reviewer's `Done:` text, register and fix R-0235, and inventory
every prompt-assembly site T003 must migrate. `.agent/` state only; READ-ONLY on
the code. Branch `feature/f105-cache-optimal-prompt-ordering`; no PR exists or
was created.

## Range
Review of `337ba21f..HEAD` — the five commits below.

## Commits

### 87953d7a chore(f105): save the R9 inventory block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f105-r9-1.md | +254/-0 | C1 — the R9 block, byte for byte |
| .agent/last_block.md | +234/-61 | C1 — same bytes; 488 ins, under the cap |

### 4465fe2f chore(f105): register R-0235
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +14/-1 | C2 — pairs A and B; finding registered first |

### c0e59290 chore(f105): record the R8 gate and resolve R-0233 and R-0234
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +35/-2 | C3 — pairs C, D, E |

### cc3d4877 chore(f105): inventory the prompt assembly sites for T003
| Path | +/- | Reason |
|---|---|---|
| .agent/t003_inventory.md | +262/-0 | C4 — the survey, written by the worker |

### (this commit) chore(f105): record the R9 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +1/-0 | C5 — pair F, the R-0235 `Landed:` line |
| .agent/plan.md | rewrite | C5 — the authored 42-line text, verbatim |
| .agent/handoff.md | rewrite | C5 — this file |

Path counts, per R-0235's fix, are DERIVED from `git diff --stat 337ba21f..HEAD`
run at write time and from no other source. That command listed FOUR paths for
C1-C4 (`.agent/authored/f105-r9-1.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/t003_inventory.md`); this C5 commit adds
`.agent/plan.md` and `.agent/handoff.md`, so the round's total is SIX, every one
under `.agent/`.

## External actions
No worktree, no PR, no `gh`, no amend/rebase/revert/cherry-pick/force-push.
`git push -u origin feature/f105-cache-optimal-prompt-ordering` runs after this
commit; its real outcome is in the completion report.

## Verification
| # | Command (full paths) | Exit | Real trimmed output |
|---|---|---|---|
| A | `cmp .agent/authored/f105-r9-1.md .agent/last_block.md` | 0 | no output |
| B | `python3 -m pytest tests/orchestration/test_test_runner.py -q -k "live_review or context_md or plan_md"` | 0 | `4 passed, 47 deselected in 0.11s` |
| C | `python3 -m pytest tests/docs/ -q` | 0 | `294 passed in 0.25s` |
| D | `python3 -m pytest tests/orchestration/test_role_conventions.py tests/orchestration/test_prompt_segments.py -q` | 0 | `48 passed in 0.12s` |
| E | `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) | 0 | `42 passed in 19.49s` |
| F | `git status --porcelain` | 0 | EMPTY at cc3d4877; re-run after this commit |
| G | `git worktree list` | 0 | `/home/decodeux/Repos/remedy  cc3d4877 [feature/f105-…]` alone |
| H | `python3 -m apps.cli.grouped integrity check --json` | 0 | `passed= True fail_count= 0 check_count= 5` |
| I | pair counts A-F, every needle sliced by line index | 0 | 6/6 as declared (below) |
| J | `grep -c "^> Branch: .*Next free ID: " .agent/live_review.md` | 0 | `1`; line 8 reads `R-0236` |
| K | `sed -n '<line>p' <file>` for every site in the inventory | 0 | 21/21 `def` lines confirmed; quotes in the completion report |
| L | `git diff --stat 337ba21f..HEAD` | 0 | 4 paths for C1-C4, 6 for the round; ins 488, 14, 35, 262 — each under 500 |

Gate I, by shape: rewrites B, C, D end FROM 0x / TO 1x. Appends A, E, F end
FROM 1x with their TO-ONLY addition exactly 1x. Every FROM occurred exactly 1x
before its edit, verified before the write.

## Authored-text proofs
- C1: `cmp` exit 0, no output. Block is 254 lines / 15664 bytes — 14 lines OVER
  the DECISION F105 D2 cap of 240; stated, not fitted. No CR, no trailing
  whitespace, final newline present.
- C5: `.agent/plan.md` equals lines 188-229 of `.agent/authored/f105-r9-1.md`
  exactly — 42 lines / 2415 bytes, sha256
  `9702bc68991f98c4509232700c7451facb013798956335ffb1f79b030f35a8f4` on both
  sides, byte comparison True. Not a byte edited.
- Every pair FROM and TO was SLICED by line index out of the committed authored
  file on disk; nothing was retyped.

## Deviations & assumptions
- The R9 block is 254 lines against DECISION F105 D2's 240-line cap. The worker
  saved it verbatim as instructed and reports the count rather than trimming it;
  the cap binds reviewer authoring, so this is reported, not repaired.
- `.agent/t003_inventory.md` is the worker's own text, as C4 instructs. It lists
  eight further prompt-assembly sites beyond the feature file's six, and a
  "Deliberate absences" section naming eight more that were NOT listed.
- Declared: this handoff is 120 lines (`wc -l`), over the 60-line cap. D15 stated cause:
  five per-commit tables, the twelve-row verification table, the pair-shape
  proof, the two authored-text equality proofs, the path-count derivation
  R-0235's fix mandates, and the item-status table. No section was dropped.
- Nothing under `packages/`, `apps/`, `tests/`, `docs/`, `docs/roadmap/`,
  `AGENTS.md`, `.agent/context.md`, `.agent/decisions.md` or
  `.agent/candidates.md` changed — confirmed by `git diff --stat`.

## Item status
| Item | Status | Reason |
|---|---|---|
| C1 | done | block saved to both paths, `cmp` exit 0, count reported |
| C2 | done | pairs A and B; R-0235 registered before any fix |
| C3 | done | pairs C, D, E; R8 gate and R9 step line filed under `## Steps` |
| C4 | done | inventory written from the source, every line number confirmed |
| C5 | done | pair F, plan rewrite, this handoff, then the push |

## Open findings
R-0221 OPEN (carried from F103). R-0229 through R-0234 RESOLVED with
reviewer-authored `Done:` text. R-0235 is FIXED but carries a `Landed:` line
only — a worker never writes `Done:` (docs/agents/planner_reviewer_prompt.md
§4.4), so the next reviewer gates R9 and authors its resolution. Next free ID
**R-0236**. `LAST_REVIEWED_SHA` stays 337ba21f until R9 gates.

## Next
Gate R9 over `337ba21f..HEAD`, then T003 proper — ONE builder per round in the
order `.agent/t003_inventory.md` proposes, starting with
`packages/orchestration/intake.py::_build_intake_prompt`, its content golden
landing before any composition moves.
