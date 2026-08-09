# Handoff — F105 R7 (session terminator)

F105 Cache-optimal prompt ordering, R7: register and fix R-0231 and R-0232, move
the misfiled R5 gate + R6 step into `## Steps`, record the R6 gate. `.agent/`
state only. Branch `feature/f105-cache-optimal-prompt-ordering`; no PR exists or
was created. The session ended at its DECLARED FOUR-ROUND CAP (R4-R7) with this
handoff — docs/agents/self_drive_protocol.md G7 counts that a SUCCESS. T003 is
untouched and starts next session.

## Range
Review of `c0ce100a..HEAD` — four commits below plus this handoff commit.

## Commits

### 0cc7f8a7 chore(f105): save the R7 terminator block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f105-r7-1.md | +206 | C1 — the R7 block, byte for byte |
| .agent/last_block.md | +153/-162 | C1 — same bytes, `cmp` clean |

359 insertions (< 500): C1 is ONE commit, the split clause did not fire. The
block is 206 lines — the reviewer's count exactly.

### f8e88b70 chore(f105): register R-0231 and R-0232
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +18 | C2 — pair A, both findings registered first |

### eabb5675 chore(f105): file the R5 gate under Steps and record the R6 gate
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +45/-21 | C3 — region moved, pair B, `Landed: R-0231` |

### c24f9176 chore(f105): correct the next free finding ID in the header
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-1 | C4 — pair C, `Landed: R-0232` |

### (this commit) chore(f105): close the session with the R7 handoff
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | rewrite | C5 — authored rewrite, verbatim and whole |
| .agent/handoff.md | rewrite | C5 — this file |

## External actions
No worktree added or removed. No PR, no `gh` command. `.agent/context.md`
untouched, as the block ordered. `git push -u origin <this branch>` runs after
this commit; its real outcome is in the completion report.

## Verification
| # | Command | Exit | Real trimmed output |
|---|---|---|---|
| A | `cmp .agent/authored/f105-r7-1.md .agent/last_block.md` | 0 | no output |
| C | `pytest test_test_runner.py -k "live_review or context_md or plan_md"` | 0 | `4 passed, 47 deselected in 0.12s` |
| D | `pytest tests/docs/ -q` | 0 | `294 passed in 0.32s` |
| E | `pytest tests/orchestration/test_role_conventions.py -q` | 0 | `26 passed in 0.09s` |
| F | `pytest tests/cli/test_golden_path.py -q` (canary) | 0 | `42 passed in 22.25s` |
| G | `git status --porcelain` | 0 | empty (after this commit) |
| H | `git worktree list` | 0 | `/home/decodeux/Repos/remedy … [feature/f105-…]` alone |
| I | integrity `--json` via `apps.cli.grouped:main` | 0 | `passed=True fail_count=0`, 5 checks; returned `None`, no `SystemExit` |
| J | `grep -c "Next free ID" .agent/live_review.md` | 0 | `2`, not 1 — see Deviations |
| J' | `grep -c "^> Branch: ….Next free ID: "` | 0 | `1`; line 8 reads `R-0233` |

B — moved region (21 lines, `- Reviewer gate on R5 …` → `  703, both under the
cap …`): sha256 `ddc20469025a33b4e7e4b99af21090a343553ef3f39ed81eb3ea27279dbbf5e0`
BEFORE the move and the SAME sha256 AFTER; slice-equality `True`; occurrences 1
before, 1 after. Carried in memory from cut to paste, never re-derived.

## Authored-text proofs
- `cmp` exit 0, no output. Block 206 lines / 12802 bytes, no trailing whitespace,
  no CR, final newline.
- Pairs A, B, C, both `Landed:` lines and the `plan.md` body were SLICED by line
  index out of `.agent/authored/f105-r7-1.md` on disk, never retyped.
- A and B APPEND-shaped: TO `startswith` FROM asserted, FROM `== 1` before, TO 1x
  after. C REWRITE-shaped: FROM 1x before, FROM 0x and TO 1x after.
- `.agent/plan.md` equals its authored slice exactly (`True`), 48 lines.

## Deviations & assumptions
- Declared: this handoff is 119 lines / ~1500 estimated tokens, over the 60-line
  and 800-token caps. D15 stated cause: five commit tables, the ten-row
  verification table, the byte-identity proof, the pair proofs and the
  item-status table. No mandated section was dropped.
- Gate J is UNSATISFIABLE as written: it counts `Next free ID`, and the
  reviewer's own R-0232 text, applied in C2 from this same block, quotes it
  (`reads \`Next free ID: R-0229\``). The count is 2 and cannot be 1 while the
  finding stands — the F104 R11 "gate quotes its own marker" class. Nothing was
  edited to make the number fit; J' proves the substance instead: exactly ONE
  header declaration, reading `R-0233`. Flagged, not corrected.
- `Landed: R-0231` is ONE line: in the block it broke after `## Steps` only
  because the quoting overhead pushed it to 81 columns; the block calls it "the
  single line" and joined it is 79 characters. Sliced, not retyped.
- Assumption (unchanged from R6): the authored `plan.md` runs from `# Plan` to
  the last Risks bullet; `Done when:` / `Handback:` is step-block text.
- `.agent/plan.md` described R6 through C1-C4 and is brought current here,
  because the block ordered its rewrite in C5.
- Four paths total, all under `.agent/`. No `packages/`, `tests/`, `apps/`,
  `docs/`, `docs/roadmap/`, `AGENTS.md` or `.agent/context.md` byte changed.

## Item status
| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | region moved byte-identically; pair B appended |
| C4 | done | |
| C5 | done | |

## Open findings
R-0221 OPEN (carried from F103). R-0229, R-0230 RESOLVED. R-0231 and R-0232 are
FIXED with `Landed:` lines only — a worker never writes `Done:` (§4.4), so the
next reviewer gates R7 and authors their resolutions. Next free ID **R-0233**.
`LAST_REVIEWED_SHA` stays c0ce100a until R7 gates.

## Next
Next session: run the Phase 0 state probe (docs/agents/self_drive_protocol.md) —
clean tree, branch, log, open PRs, `remedy plan status` / `plan next`, then read
`handoff.md`, `plan.md`, `live_review.md`, `candidates.md`, the F105 feature file
— gate R7 over `c0ce100a..HEAD`, then START AT T003: inventory the prompt
assembly sites first, then migrate one builder per round.
