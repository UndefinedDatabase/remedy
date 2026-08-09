# Handoff — F105 R21 (worker → planner/reviewer)

R21 is the SESSION TERMINATOR. It gated R20 on disk, resolved R-0249, registered
R-0250, and installed the fix for the unsatisfiable-gate class as a pre-emission
checklist in docs/agents/planner_reviewer_prompt.md §3 plus DECISION F105 D8.
No production file and no test file changed, so NO red-proof is owed and no
worktree was created. Its own gate is owed to the NEXT session's reviewer
(docs/agents/planner_reviewer_prompt.md §4.13) — do not open a repair round.
Branch: feature/f105-cache-optimal-prompt-ordering. Base 9cb128d7.
Deviations, declared: this file is 79 lines against the AGENTS.md cap of 60.
Cause per DECISION D15, all of it mandated: the changed-files table over six
commits, the A-G gate table, five pair proofs, the item-status table and three
declared deviations. No section dropped, no padding.

## Commits — changed files, one row per path
| Commit | Path | +/- | Reason |
|---|---|---|---|
| 71e3f75f `save the R21 block verbatim` | `.agent/authored/f105-r21-1.md` | +328/-0 | C1a — block ALONE, 328 lines, under D5's 400 |
| 39bcf956 `mirror the R21 block to last_block` | `.agent/last_block.md` | +242/-385 | C1b — `cp`, verbatim rewrite of ONE state file |
| 83ad4543 `record the R20 gate and register R-0250` | `.agent/live_review.md` | +80/-2 | C2 — pairs A (R-0249 `Done:` + R-0250), B (next free ID), C (R20 gate) |
| 94707eef `add the pre-emission block checklist…` | `docs/agents/planner_reviewer_prompt.md` | +29/-0 | C3 — pair D, the §3 checklist |
| 94707eef | `.agent/decisions.md` | +33/-0 | C3 — pair E, DECISION F105 D8 |
| c9eb7bb8 `update the plan and close the session…` | `.agent/plan.md` | +16/-22 | C4 — PAIR_F full replacement; the FILE is 50 lines, over the <50 rule (dev. 1) |
| c9eb7bb8 | `.agent/handoff.md` | +44/-65 | C4 — this file at its first write |
| (this commit) `correct two changed-files rows…` | `.agent/handoff.md` | rewrite | C5, dev. 3 — cannot table its own commit (R-0149) |

Insertions: 328, 242, 80, 62, 60, this one — each under 500.

## Item status
| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 (not in the block) | deviated | dev. 3 — correction commit; the C4 handoff tabled `.agent/plan.md` with full-file counts, not `git numstat` |

## External actions
`git push -u origin feature/f105-cache-optimal-prompt-ordering`. No PR — F105's
comes at CLOSURE. No gh, no merge, no worktree.

## Verification
| Gate | Command | Exit | Real output (trimmed) |
|---|---|---|---|
| A | `sha256sum` authored+last_block; `cmp` | 0 / 0 | both `a9732812…`; `cmp` no output |
| B | `wc -l` authored | 0 | `328` — under the 400 cap |
| C | six greps + `sed -n 8p` + marker grep + `wc -l` plan | 0 | `1`; `1`; `1`; `…Next free ID: R-0251.`; `1`; `1`; markers `0/0/0/0`; plan `50` (expected <50, dev. 1) |
| D | `tests/docs/`; `test_dashboard_contract.py` | 0 / 0 | `294 passed in 0.30s`; `70 passed in 3.89s` |
| E | `tests/cli/test_golden_path.py` | 0 | `42 passed in 19.45s` |
| F | red-proof | n/a | NOT OWED — this round changes no executable file; no worktree created, none exists |
| G | `git status --porcelain`; `git worktree list`; `git log --numstat` | 0/0/0 | empty; primary alone; per-commit `+` above, all <500 |

## Authored-text proofs
Transport: `.agent/authored/f105-r21-1.md` and `.agent/last_block.md` both sha256
`a9732812…`, `cmp` exit 0, both 328 lines. Every pair SLICED by marker;
`grep -c '^===BEGIN\|^===END'` is 0 in live_review, decisions, plan and the
prompt doc.
| Pair | Target | Declared | Measured | FROM before/after | TO before/after |
|---|---|---|---|---|---|
| A | live_review | REWRITE | REWRITE | 1 / 0 | 0 / 1; 33 TO-only lines, min 1x |
| B | live_review | REWRITE | REWRITE | 1 / 0 | 0 / 1 |
| C | live_review | APPEND | APPEND | 1 / 1 | 0 / 1; 46 TO-only lines, min 1x |
| D | prompt doc | APPEND | APPEND | 1 / 1 | 0 / 1; 28 TO-only lines, min 1x |
| E | decisions | APPEND | APPEND | 1 / 1 | 0 / 1; 27 TO-only lines, min 1x |
Stray added lines 0 in every commit: C2 80/0, C3 29/0 and 33/0.
PAIR_F: `.agent/plan.md` equals its slice byte for byte, sha256 `d263bfd0…`.

## Deviations & assumptions
1. `.agent/plan.md` is 50 lines, one over AGENTS.md's <50 and over done-when C, which demands <50. PAIR_F is a full replacement the block requires to be byte-for-byte equal to its slice, so the applier cannot trim it without authoring text. Applied verbatim and declared — exactly the behaviour DECISION F105 D8 item 3, installed this same round, prescribes. This is a second live instance of the R-0250 class, in the very block that fixes it.
2. Gates ran through python subprocess wrappers: this shell layer rejects inline `$?`, pipes into `sed`/`awk`, and `for` loops (carried from R15-R20). Slice extraction used a python marker reader rather than `sed -n '/BEGIN/,/END/p'` for the same reason; it is still purely mechanical, marker-driven, and never retypes an authored text. Scratch lives in gitignored `.remedy-wt/r21slices/`.
3. A FIFTH commit, outside the block's declared C1a-C4 order, touches only `.agent/handoff.md` — a declared path. Cause: the C4 handoff tabled `.agent/plan.md` as `+50/-57`, the file's own line counts, where every other row and the reviewer's own `git log --numstat` read `+16/-22`. The branch was already pushed, so amending would have required a force-push, which is forbidden. A correction commit was preferred to leaving a false number in the record the reviewer resumes from. No other path and no other content changed.

## Next
The NEXT session gates R21 over `9cb128d7..HEAD` — state and docs only, so no
red-proof is owed — then takes migration-order step 5,
`pingpong_loop.py::_build_builder_prompt`.
Open findings: 4 (R-0221, R-0239, R-0246, R-0247). R-0249 and R-0250 both carry
reviewer-authored resolution text applied this round at PAIR_A.
