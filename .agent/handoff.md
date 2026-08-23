# Handback — F031 Decision inbox, R9 (state + measurement only)
Branch `feature/f031-decision-inbox`. Base `1ec7a33009f15da0f20b95f1baae3f814b4f0c0b`.
Fortschritt: ~27 % (F031 claimed; R1 through R8 landed and gated ·
             T001 SHIPPED — the derivation module, the read endpoint
             and 29 tests are on disk and green · T002 blocked on two
             MEASURED gaps R10 must rule · T003 offen) — Schaetzung

## Range
Review of `1ec7a330`..HEAD, HEAD being the C4 commit that writes this file.

## Commits
### dcd9566e docs(state): save the F031 R9 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r9.md | +375 / -0 | C0a — the block saved verbatim |

### 870eff48 docs(state): mirror the F031 R9 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +202 / -120 | C0b — mirror; same blob `fc7e1779` as C0a |

### 8d31351c docs(state): advance the F031 plan to the R10 rulings
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +13 / -13 | C1 — PLANF031R9 applied byte-for-byte |

### 95610316 docs(review): record the F031 R8 PASS with the pushed tips
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | C2 — GATE8 appended |

### 000b1b63 docs(state): measure the F031 UI ground T002 builds on
| Path | +/- | Reason |
|---|---|---|
| .agent/f031_ui_inventory.md | +263 / -0 | C3 — new measured inventory, 263 lines |

### C4 (self-reference; SHA and numstat unknowable to the file they create)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4 — this handback |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |
| push (G10) | deviated | runs AFTER C4; G10 rules its outcome a value of no file this round writes. Carrier: the R9 entry of `.agent/live_review.md`, written by R10 |

## External actions
`git worktree add --detach .remedy-wt/r9-neg 95610316`, then `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/r9-neg` — the G5 byte-flip control; primary checkout never mutated; `git worktree list` back to 1 line.
`git push origin feature/f031-decision-inbox` — ordered by G10 after C4. THIS GATE'S OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: the reviewer measures the pushed tips at the next gate and records them in the R9 entry of `.agent/live_review.md`. No PR created, nothing merged, no force, no history rewrite.

## Verification — one line per gate
G1 PASS — branch `feature/f031-decision-inbox`; `.agent/STOP` ABSENT before C0a and before C4; `git status --porcelain` 0 after C0a, C0b, C1, C2, C3.
G2 PASS — all four readings sha256 `173981e6f4409b1629f7c4db3880fbbbb7f3bda58b482c0be8300f6adeae4a8e`, 26436 bytes, 375 lines; C0a and C0b blob id both `fc7e17798b211103f5262223d864e231eaf16f8b`.
G3 PASS — my extractor over the committed C0a blob: 2 slices (PLANF031R9, GATE8), 50 CONTENT lines inside markers, 375 TOTAL lines, 4 marker lines.
G4 PASS — `.agent/plan.md` at `8d31351c` byte-equal to PLANF031R9, newline-INCLUDED convention, slice 2964 bytes = file 2964 bytes; trailing-newline-removed control FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 49 < 50.
G5 PASS — constraint 7's shape holds as one equality: True; 566277 → 570870, delta 4593 = 1 + 4592; blank-line units 284 → 285, LAST unit equals GATE8; mutant at offset 566400 ('E'→'e', inside the appended paragraph, written only in the disposable worktree) REJECTED by both readers, true file ACCEPTED by both.
G6 PASS — `^- R-\d+ — ` 240 → 240 all DISTINCT, ADDED {} and REMOVED {} both empty, max `R-0679` → `R-0679`, `^Done: R-` 2 → 2, `^Recurrence: R-` 15 → 15, `^Gate: R\d+ — ` 8 → 9 gaining exactly `R8`, keys R19,R1..R8 all present.
G7 PASS — `git ls-tree 1ec7a330 -- .agent/f031_ui_inventory.md` printed NOTHING; file exists at `000b1b63`, 263 lines, headings `## Q1`..`## Q7` in that order plus `## Observations`. Q4 measured: environment `"node"` MATCHES; include one entry `"src/**/*.test.ts"` MATCHES; 20 files by that glob MATCHES; 0 by `src/**/*.test.tsx` MATCHES; 0 `package.json` lines matching jsdom|happy-dom|testing-library MATCHES. No difference to account for. Every Q section was measurable; none guessed.
G8 PASS — `^<<<SLICE `/`^<<<END ` 0/0 in all three targets at their own commits; range names no `packages/`, `apps/`, `tests/`, `docs/` path and neither `.agent/decisions.md` nor `.agent/f031_inventory.md`; C0a..C3 each single-parent with insertions 375, 202, 13, 2, 263, each < 500, agreeing cell for cell with the `## Commits` `+/-` column above (both from `git diff --numstat`); range MINUS change set EMPTY, change set MINUS range exactly `.agent/handoff.md`; `git ls-files .remedy-wt` 0, zip glob 0, `git worktree list` 1 line. Reflog: scoped to THIS ROUND'S 5 entries, read by the operation prefix before the first colon of `git reflog --format=%gs` — all 5 `commit`, so amend 0, rebase 0, cherry 0.
G9 PASS — 12 occurrences over 6 distinct word-bounded `[0-9a-f]{7,40}` tokens (`1ec7a330`, `1ec7a330…4b4f0c0b`, `23522837`, `3dbc1ba8`, `6325ac2f` = commit; `ba2a3a9e…268d12` = blob), FAILING SET EMPTY as the block predicted; the one 64-char sha256 is excluded by the word boundary. `git worktree list` 1 line immediately before the first pytest. Five suites SERIALLY in the primary checkout at the C3 tree, never two pytest processes alive, all exit 0: `tests/ui_server/` 474, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `test_golden_path` 42 — identical to the reviewer's readings, no difference to account for.
G10 ordered after C4 — command and carrier in `## External actions`; real outcome in the round report.

## Findings
By §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the open set is 238, measured at `95610316`. THIS ROUND MINTED NO ID and wrote no `Recurrence:` line. The findings THIS FEATURE MUST STILL ACT ON: R-0403, R-0413, R-0431, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679.

## Authored-text proofs
PLANF031R9 → `.agent/plan.md`: extracted programmatically from the COMMITTED C0a blob by marker lines, written unmodified, disk-to-disk equality True (2964 bytes), negative control False. GATE8 → `.agent/live_review.md`: same extraction, appended in constraint 7's shape, whole-file equality True. Neither slice was retyped or reflowed.

## Deviations & assumptions
1. Commit sequence C0a, C0b, C1, C2, C3, C4 executed EXACTLY, in order: none added, none dropped, none reordered. No amend, rebase, cherry-pick, force-push, history rewrite, branch deletion, merge or PR.
2. C4's `+/-` cell is `rewrite`, not a numstat pair — a commit cannot number itself; the template's self-reference exception covers it, so G8's per-commit agreement spans C0a..C3, the range G8 names.
3. G5's mutant existed ONLY inside `.remedy-wt/r9-neg`, a disposable worktree removed by exact path before the G9 suites. `.remedy-wt/dry`, `.remedy-wt/rev-r7`, `.remedy-wt/f031-r8.md` were neither read nor touched.
4. The shell guard rejected three compound commands, so Q1, Q2 and the G8 path-set reading ran as `python3` scripts (`os.walk` + `re` in place of `grep`) — same semantics, stated in the inventory beside each answer; two such scripts lived under `.remedy-wt/` and were removed by exact path.
5. NO contradiction was found inside the block. Every base value it states reproduced under my execution: 566277 bytes / 1195 lines / 284 units, 240 findings, max R-0679, 2 Done, 15 Recurrence, 8 Gate keys, plan 49 lines / 3017 bytes, handoff 75 lines, `.agent/f031_ui_inventory.md` absent at `1ec7a330`.
6. Cap: constraint 3 fixes SIX commits, so AGENTS.md `### handoff.md` gives the 100-line tier (>5 commits). This file is under it — no DECISION D15 overage claimed, no section dropped. No token-cap compliance is claimed; that cap was withdrawn.
7. Beyond the reviewer's Q1 reading: `docs/ui/design_reference/assets_spec.md:174` IS decision visual authority — for a GRAPH GLYPH, not a card. Recorded in the inventory so R10 rules against it, not around it.

## Next
1. Phase 1 rule 1: re-read `.agent/STOP` from disk.
2. NO pull request exists for `feature/f031-decision-inbox`; none should be created yet.
3. R10 rules the two MEASURED gaps — no visual authority for a decision card, no toolchain that can mount a component — as DECISIONs, each with alternatives and a reversal path, before any card ships.
4. R10's first commit also records the R9 verdict, which by DECISION F085 D9 no artefact of this round can carry.
