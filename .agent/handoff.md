# Handoff — F105 Cache-optimal prompt ordering, R14 (record half of the R13 gate)

Branch: feature/f105-cache-optimal-prompt-ordering. A `.agent/`-only round: NO
builder was migrated. R14 is the record half of the split the reviewer made
under DECISION F105 D2; migration-order step 2 moves to R15.

## Range

Review of 2d993ed9..HEAD — 4 commits. Path list and count DERIVED from
`git diff --stat 2d993ed9..HEAD` (C1-C3) plus `git diff --stat` on the working
tree (C4), both at write time (R-0235): FIVE paths, all under `.agent/` —
`authored/f105-r14-1.md`, `last_block.md`, `live_review.md`, `plan.md`,
`handoff.md`.

## Commits

### a5dbcd31 chore(f105): save the R14 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f105-r14-1.md | +231/-0 | C1, this block verbatim |
| .agent/last_block.md | +176/-176 | C1, same bytes |

407 insertions, under the 500 cap; from `git log -1 --numstat`.

### 05972bb5 chore(f105): resolve R-0238 and register R-0240 and R-0241
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +31/-0 | C2 pairs A and B |

31 insertions.

### e3473d5a chore(f105): record the R13 gate
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +28/-1 | C3 pair C header ID, pair D gate + R14 step line |

28 insertions.

### C4 chore(f105): record the R14 handback
Grouped table (R-0149): a handoff cannot table the commit that writes it.
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +26/-18 | C4, authored 49-line slice, block lines 164-212 |
| .agent/handoff.md | this file | C4, per docs/agents/handback_template.md |

C4's insertions come from `git diff --cached --numstat` at stage time and are
reported in the completion report; this file predates its own commit.

## External actions

`git push -u origin feature/f105-cache-optimal-prompt-ordering` — run after the
C4 commit, real result in the completion report. No PR created: F105's PR comes
at CLOSURE. No worktree added, no `gh` command run.

## Verification

| # | Command | Exit | Real trimmed output |
|---|---|---|---|
| A1 | `cmp .remedy-wt/f105-r14-1.block.md .agent/authored/f105-r14-1.md` | 0 | (no output) — transport vs the reviewer's original |
| A2 | `cmp .agent/authored/f105-r14-1.md .agent/last_block.md` | 0 | (no output) — the save |
| B | `wc -l` / `wc -c` on `.agent/authored/f105-r14-1.md` | 0 / 0 | `231` / `14237` — 9 under DECISION F105 D2's cap of 240 |
| C | `python3 -m pytest tests/orchestration/test_test_runner.py -q -k "live_review or context_md or plan_md"` | 0 | `4 passed, 47 deselected in 0.11s` |
| D | `python3 -m pytest tests/docs/ -q` | 0 | `294 passed in 0.28s` |
| E | `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) | 0 | `42 passed in 21.45s` |
| F | `git worktree list` / `git status --porcelain` | 0 / 0 | `/home/decodeux/Repos/remedy  e3473d5a [feature/f105-cache-optimal-prompt-ordering]` — primary alone; status showed only `M .agent/plan.md` pre-C4, empty after C4 per the completion report |
| G | `python3 -m apps.cli.grouped integrity check --json` | 0 | `passed= True fail_count= 0 checks= 5` |
| I | `git diff --stat 2d993ed9..HEAD` | 0 | 3 paths (C1-C3) + 2 (C4) = 5, all under `.agent/`; insertions 407, 31, 28, C4 in the completion report — each under 500 |

## Authored-text proofs

Every FROM and TO was SLICED by line index out of
`.agent/authored/f105-r14-1.md` after C1 — A 48 / 51-57, B 61 / 64-89,
C 97 / 100, D 108-110 / 113-142 — never retyped.

| Pair | Shape | FROM before | FROM after | TO after | TO-only tail after |
|---|---|---|---|---|---|
| A (live_review.md) | APPEND | 1x | 1x | 1x | 1x |
| B (live_review.md) | APPEND | 1x | 1x | 1x | 1x |
| C (live_review.md) | REWRITE | 1x | 0x | 1x | n/a (disjoint) |
| D (live_review.md) | APPEND | 1x | 1x | 1x | 1x |

`.agent/plan.md` equals its authored 49-line slice (block lines 164-212):
sha256 `9607d792` both sides.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | 231 lines / 14237 bytes, both `cmp` exit 0 |
| C2 | done | pairs A and B, own commit |
| C3 | done | pairs C and D, own commit |
| C4 | done | plan + handoff, one commit, then push |

## Deviations & assumptions

1. Handoff overage, declared under DECISION D15: 125 lines / ~1460 tokens
   against the 60-line and 800-token caps. Cause is mandated content only —
   four per-commit tables, the nine-row verification table, the four-row
   pair-proof table, the item-status table. No section dropped, no padding.
2. Exit-code transport: this sandbox rejects compound `cmd; echo $?` forms, so
   `cmp`, `wc`, the pytest targets and the integrity check ran through
   `subprocess.run` in a gitignored scratch script with their REAL `returncode`
   printed. Same binaries, same arguments — only the transport differs (the
   deviation the reviewer re-ran and accepted at R13).
3. `.agent/plan.md` was stale between C1 and C3 — still "Next finding ID:
   R-0240" after C2 registered R-0240 and R-0241 — because the block places the
   plan rewrite in C4. Declared, not silently taken.

## Open findings

3 open: R-0221 (carried), R-0240 and R-0241 (registered at C2). Both new ones
have their fixes ON DISK here — R-0240 by pair C's header rewrite to R-0242,
R-0241 by the authored plan text — but only reviewer-authored `Done:` text sets
Resolved, so both stay OPEN until the R15 gate. R-0238 was RESOLVED at C2 by
the reviewer's own `Done:` text. Next free ID: R-0242.

## Next

R15 gates R14 over `2d993ed9..HEAD` FIRST — R14's own gate is owed — then takes
migration-order step 2,
`packages/orchestration/mission_compiler.py::build_mission_prompt`, onto the
registry under `tests/orchestration/test_mission_prompt_golden.py`, with
DECISION F105 D4: the mission rules segment is cap-scoped, because
`gauntlet_runner.py:506` varies `max_milestones`. "Site N" belongs to the
inventory catalogue's headings only (R-0241).
