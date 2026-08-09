# Handoff — F105 Cache-optimal prompt ordering, R15 (record half of the R14 gate)

Branch: feature/f105-cache-optimal-prompt-ordering. A `.agent/`-only round: NO
builder was migrated. R15 is the record half of the split the reviewer made
under DECISION F105 D2; migration-order step 2 moves to R16.

## Range

Review of 73e159b7..HEAD — 4 commits. Path list and count DERIVED from
`git diff --stat 73e159b7..HEAD` (C1-C3) plus `git diff --stat` on the working
tree (C4), both at write time (R-0235): FIVE paths, all under `.agent/` —
`authored/f105-r15-1.md`, `last_block.md`, `live_review.md`, `plan.md`,
`handoff.md`.

## Commits

### a7e9dc26 chore(f105): save the R15 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f105-r15-1.md | +227/-0 | C1, this block verbatim |
| .agent/last_block.md | +161/-165 | C1, same bytes |

388 insertions per `git log --numstat`, 454 per `git commit` with rewrite
detection. Both under 500.

### a8cf5f09 chore(f105): resolve R-0240 and R-0241 and register R-0242
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +38/-1 | C2 pair A (Done text + R-0242 + R-0243), pair B (header ID) |

38 insertions.

### 34e6b841 chore(f105): record the R14 gate
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +26/-0 | C3 pair C, R14 gate PASS + the R15 step line |

26 insertions.

### C4 chore(f105): close the session with the R15 handoff
Grouped table (R-0149): a handoff cannot table the commit that writes it.
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +30/-25 | C4, authored 54-line slice, block lines 155-208 |
| .agent/handoff.md | this file | C4, per docs/agents/handback_template.md |

plan.md's +30/-25 is from `git diff --numstat` before staging; C4's total
insertions are in the completion report — this file predates its own commit.

## External actions

`git push -u origin feature/f105-cache-optimal-prompt-ordering` — run after the
C4 commit, real result in the completion report. No PR created: F105's PR comes
at CLOSURE. No worktree added, no `gh` command run.

## Verification

| # | Command | Exit | Real trimmed output |
|---|---|---|---|
| A1 | `cmp .remedy-wt/f105-r15-1.block.md .agent/authored/f105-r15-1.md` | 0 | no output — transport vs the reviewer's surviving original |
| A2 | `cmp .agent/authored/f105-r15-1.md .agent/last_block.md` | 0 | no output — the save |
| B | `wc -l` / `wc -c` on `.agent/authored/f105-r15-1.md` | 0 / 0 | `227` / `14333` — 13 under DECISION F105 D2's cap of 240 |
| C | `python3 -m pytest tests/orchestration/test_test_runner.py -q -k "live_review or context_md or plan_md"` | 0 | `4 passed, 47 deselected in 0.11s` |
| D | `python3 -m pytest tests/docs/ -q` | 0 | `294 passed in 0.25s` |
| E | `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) | 0 | `42 passed in 19.76s` |
| F1 | `git status --porcelain` | 0 | pre-C4: `M .agent/plan.md` only; post-C4 EMPTY per the completion report |
| F2 | `git worktree list` | 0 | `/home/decodeux/Repos/remedy  73e159b7 [feature/f105-cache-optimal-prompt-ordering]` — primary alone |
| G | `python3 -m apps.cli.grouped integrity check --json` | 0 | `passed= True`, `fail_count= 0`; all 5 checks `pass` |
| I | `git diff --stat 73e159b7..HEAD` | 0 | 3 paths (C1-C3) + 2 (C4) = 5, all under `.agent/`; insertions 388, 38, 26, C4 in the completion report — each under 500 |

## Authored-text proofs

Every FROM and TO was SLICED by line index out of
`.agent/authored/f105-r15-1.md` after C1 — A 44-45 / 48-86, B 91 / 94,
C 102-103 / 106-133 — never retyped. sha256 `b0bbc7d6` is shared by the
reviewer's scratch original, `.agent/authored/f105-r15-1.md` and
`.agent/last_block.md`.

| Pair | Shape | FROM before | FROM after | TO after | TO-only tail after |
|---|---|---|---|---|---|
| A (live_review.md) | APPEND | 1x | 1x | 1x | 1x (block lines 50-86) |
| B (live_review.md) | REWRITE | 1x | 0x | 1x | n/a (disjoint) |
| C (live_review.md) | APPEND | 1x | 1x | 1x | 1x (block lines 108-133) |

`.agent/plan.md` equals its authored 54-line slice (block lines 155-208):
sha256 `4fb762f5` both sides.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | 227 lines / 14333 bytes, both `cmp` exit 0 |
| C2 | done | pairs A and B, own commit |
| C3 | done | pair C, own commit |
| C4 | done | plan + handoff, one commit, then push |

## Deviations & assumptions

1. Handoff overage, declared under DECISION D15: 135 lines / ~1630 tokens
   against the 60-line and 800-token caps. Cause is mandated content only —
   four per-commit tables, the ten-row verification table, the three-row
   pair-proof table, the item-status table, five declared deviations. No
   section dropped, no padding.
2. Exit-code transport: this sandbox rejects the compound `cmd; echo $?` form,
   so every gate ran inside one `bash -c` printing the REAL `$?` (or
   `${PIPESTATUS[0]}` behind a `tail`). Same binaries, same arguments; a shell
   wrapper this time, not the `subprocess.run` of R13/R14.
3. `.agent/plan.md` was stale between C1 and C3 — still "Next finding ID:
   R-0242" while C2 registered R-0242 and R-0243 — because the block places the
   plan rewrite in C4. This is R-0242's own condition, declared, not silently
   taken.
4. `.agent/plan.md` is 54 lines, over the AGENTS.md `<50 lines` guidance for
   plan.md. Not fixed: the block mandates the authored text VERBATIM and whole,
   and the worker may not trim reviewer-authored state text.
5. The pairs were applied by a gitignored scratch script,
   `.remedy-wt/r15_apply.py`: it slices FROM/TO by line index from the committed
   authored file, refuses to write unless FROM occurs 1x, and prints the counts
   quoted above. `.remedy-wt/` is ignored (`.gitignore:235`), nothing tracked.

## Open findings

4 open: R-0221 and R-0239 (carried), R-0242 and R-0243 (registered at C2 from
the reviewer's own text). R-0240 and R-0241 were RESOLVED at C2 by the
reviewer-authored `Done:` text. Next free ID: R-0244.

## Next

R16 gates R15 over `73e159b7..HEAD` FIRST — R15's own gate is owed — then takes
migration-order step 2,
`packages/orchestration/mission_compiler.py::build_mission_prompt`, onto the
registry under a new `tests/orchestration/test_mission_prompt_golden.py`, with
DECISION F105 D4: the mission rules segment is cap-scoped, because
`gauntlet_runner.py:506` varies `max_milestones`. Settle R-0243 before
authoring that block, or R16 splits the same way. "Site N" belongs to the
inventory catalogue's headings only (R-0241).
