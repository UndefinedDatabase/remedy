# Handoff — F105 R20 (worker → planner/reviewer)

R20 gated R19 on disk and migrated prompt-assembly site 4 —
`build_orchestrator_prompt` AND its system half — onto the segment registry
under a BYTE-equality golden. Production and test files changed, so a mutation
red-proof was owed and is recorded below.
Deviations, declared: this file is 97 lines against the AGENTS.md cap of 60.
Cause per DECISION D15, all of it mandated: the changed-files table over SIX
commits, the A-G gate table, SIX pair proofs, the item-status table over
C1a-C6 plus the deferral, the three-mutation red-proof and seven declared
deviations. No section dropped, no padding.

## Range
Review of 04a3396d..HEAD — 6 commits. The block's `c65d663e..HEAD` also
contains R19's five, already gated this round at PAIR_C.

## Commits — changed files, one row per path
| Commit | Path | +/- | Reason |
|---|---|---|---|
| 23e168e4 `save the R20 block verbatim` | `.agent/authored/f105-r20-1.md` | +471/-0 | C1a — block ALONE; 471 lines, OVER D5's 400 (dev. 1) |
| 8035b7a8 `mirror the R20 block to last_block` | `.agent/last_block.md` | +422/-181 | C1b — `cp`, verbatim rewrite of ONE state file |
| 4b6e0ebd `record the R19 gate and register R-0249` | `.agent/live_review.md` | +58/-1 | C2 — pairs A (append), B (header rewrite), C (R19 gate) |
| 94591bbc `compose the orchestrator prompt…` | `packages/orchestration/orchestrator_loop.py` | +89/-7 | C3 — three segments, two composers, both builders reduced to `.text` |
| df521e3c `pin the orchestrator prompt…` | `tests/orchestration/test_orchestrator_prompt_golden.py` | +232/-0 | C4 — new; 6 tests |
| cd2245eb `amend DECISION D6 and record D7` | `.agent/decisions.md` | +51/-4 | C5 — pair D (D6 amendment, fixes R-0248), pair E (D7) |
| cd2245eb | `.agent/live_review.md` | +8/-1 | C5 — pair F, the reviewer-authored resolution text for R-0248 |
| (this commit) `update the plan and write the R20 handoff` | `.agent/plan.md` | +28/-18 | C6 — PAIR_G slice; 56 lines, OVER the <50 rule (dev. 2) |
| (this commit) | `.agent/handoff.md` | rewrite | C6 — this file; cannot table its own commit (R-0149) |

Insertions: 471, 422, 58, 89, 232, 59, this one — each under 500.

## Item status
| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| evidence-gap deferral | deviated | DEFERRED by the block itself to the round wiring `on_call` for all three sites; recorded in `.agent/plan.md` |

## External actions
`git push -u origin feature/f105-cache-optimal-prompt-ordering`. No PR — F105's
comes at CLOSURE. No gh. Worktree `.remedy-wt/r20-redproof` created, used for
three mutations, removed and pruned; `git worktree list` shows the primary alone.

## Verification
| Gate | Command | Exit | Real output (trimmed) |
|---|---|---|---|
| A | `sha256sum` authored+last_block; `cmp` | 0 / 0 | both `52edfd1d…`; no output |
| B | `wc -l` authored | 0 | `471` — FAILS the <=400 rule (dev. 1) |
| C | six greps + `sed -n 8p` + `wc -l` plan | 0 | `1`; `1`; `1`; `…Next free ID: R-0250.`; `1`; `1` (expected 0, dev. 3); markers `0/0/0`; plan `56` (expected <50, dev. 2) |
| D | golden; `test_orchestrator_loop.py`; `test_prompt_segments.py`; `tests/docs/` | 0/0/0/0 | `6 passed`; `192 passed` (baseline 192, unchanged); `22 passed`; `294 passed` |
| E | `tests/cli/test_golden_path.py` | 0 | `42 passed in 19.50s` |
| F | red-proof, see below | 1/1/1 then 0 | three mutations RED, each reverted GREEN |
| G | `git status --porcelain`; `git log --numstat` | 0/0 | empty; per-commit `+` above, all <500 |

## Red-proof (disposable worktree at cd2245eb, never the primary checkout)
| # | Mutation | Exit | Failing tests |
|---|---|---|---|
| M1 | `orchestrator_protocol` rank CONVENTIONS → STEERING | 1 | `test_full_prompt_is_byte_equal_to_the_pre_migration_render`, `test_manifest_carries_the_three_declared_segments_in_rank_order`, `test_composition_injects_no_bytes_of_its_own`, `test_only_the_mission_state_segment_moves_with_the_context`, `test_the_system_manifest_is_the_prefix_of_the_full_one` (5 failed, 1 passed) |
| M2 | drop `# Mission state\n\n` from segment 3 | 1 | `test_full_prompt_is_byte_equal_to_the_pre_migration_render`, `test_composition_injects_no_bytes_of_its_own` (2 failed, 4 passed) |
| M3 | `orchestrator_system` keeps its trailing newline | 1 | `test_system_prompt_is_byte_equal_to_the_pre_migration_render`, `test_full_prompt_is_byte_equal_to_the_pre_migration_render`, `test_composition_injects_no_bytes_of_its_own` (3 failed, 3 passed) |
After each revert: `6 passed`, exit 0, `git status --porcelain` empty in the worktree.

## Authored-text proofs
Transport: `.agent/authored/f105-r20-1.md` and `.agent/last_block.md` both sha256
`52edfd1d…`, `cmp` exit 0, both 471 lines. Every pair SLICED by marker;
`grep -c '^===BEGIN\|^===END'` is 0 in live_review, decisions and plan.
| Pair | Target | Declared | Measured | FROM before/after | TO before/after |
|---|---|---|---|---|---|
| A | live_review | APPEND | APPEND | 1 / 1 | 0 / 1; 16 TO-only lines, min 1x |
| B | live_review | REWRITE | REWRITE | 1 / 0 | 0 / 1 |
| C | live_review | APPEND | APPEND | 1 / 1 | 0 / 1; 41 TO-only lines, min 1x |
| D | decisions | REWRITE | REWRITE | 1 / 0 | 0 / 1 |
| E | decisions | APPEND | APPEND | 1 / 1 | 0 / 1; 30 TO-only lines, min 1x |
| F | live_review | APPEND | REWRITE (dev. 4) | 1 / 0 | 0 / 1; 8 TO-only lines, min 1x |
Stray added lines 0 in every state commit: C1a 471/0, C1b 422/0, C2 58/0, C5 59/0.
PAIR_G: `.agent/plan.md` equals its slice byte for byte, sha256 `dc8b12f6…`.

## Deviations & assumptions
1. The block is 471 lines, over D5's 400-line cap. Measured before C1a and again after; it is a property of the authored text, which must be saved verbatim, so it could not be fixed without retyping. Done-when B FAILS as written and is reported failing rather than rounded.
2. `.agent/plan.md` is 56 lines, over AGENTS.md's <50 and over done-when C. PAIR_G is a full replacement the block requires to be byte-for-byte equal to its slice; trimming it would be authoring text. Applied verbatim, declared.
3. `grep -c 'committed BEFORE any of them at C1b' .agent/decisions.md` returns 1, not the required 0 — because PAIR_D_TO deliberately QUOTES that retired phrase so a reader sees what changed without diffing. The substantive intent holds: the original overclaiming sentence is gone (D6 now reads "from C1b onward"); the single remaining hit at line 3921 is the amendment's own quotation. Unsatisfiable-gate class.
4. PAIR_F was declared APPEND but is a REWRITE: its TO drops the FROM line's trailing " OPEN." before appending. FROM is 0x after, TO 1x after, stray 0.
5. Test 5's block wording asks the shared prefix to end EXACTLY at the protocol segment's last byte. Structurally impossible: the next segment opens with the constant `# Mission state` header, so any two renders share it too. The test asserts the whole stable prefix is byte-identical and the first divergence falls inside the volatile segment, and reports the measured shared-prefix length in its message. Stated in the test's own docstring.
6. Gates ran via python subprocess wrappers where the shell layer rejects inline `$?` (carried from R15-R19 dev. 1). Scratch and the red-proof worktree live in gitignored `.remedy-wt/`.
7. Segments 1 and 2 are registered through one private helper, `_register_orchestrator_prefix`, shared by both composers. The block's constraint — do not string-concatenate the system `ComposedPrompt.text` — holds: each composer builds its OWN registry and the full one lists all three manifest entries.

## Next
The next round gates R20 over `04a3396d..HEAD` — production and test files
changed, so a mutation red-proof IS owed — then takes migration-order step 5,
`pingpong_loop.py::_build_builder_prompt`.
Open findings: 5 (R-0221, R-0239, R-0246, R-0247, R-0249). R-0248 carries
reviewer-authored resolution text applied this round at PAIR_F.
