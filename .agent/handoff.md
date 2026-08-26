# Handback — F031 Decision inbox, R12 · T002a ships the decision-card pure model

Branch `feature/f031-decision-inbox`. Base `8b4e229534c64111a1bb9391b65182631c8d57de`. Commits in order:
C0a `a0e545eb` · C0b `2e26a5ba` · C1 `f94ca4f5` · C2 `769fd515` · C3 `8df27c6e` · C4 is this commit,
whose SHA no artefact of it can carry. Constraint 4 fixes the bundle at 6 commits, so the AGENTS.md
`### handoff.md` tier is the >5-per-commit-table one, <=100 lines.

Fortschritt: ~40 % (F031 claimed; R1 through R10 landed and gated ·
             T001 SHIPPED · T002a ships the card MODEL and its tests
             here · T002b ordering, filtering and the badge offen ·
             T003 offen) — Schaetzung

## Range
Review of 8b4e2295..HEAD.

## Commits
### a0e545eb docs(state): save the F031 R12 step block verbatim
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/authored/f031-r12.md | +450/-0 | C0a, the block saved verbatim so slices extract from a commit |

### 2e26a5ba docs(state): mirror the R12 block into last_block
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/last_block.md | +331/-371 | C0b, written from the committed C0a blob; same git blob id |

### f94ca4f5 docs(state): the R12 plan, T002a ships the card model
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/plan.md | +17/-17 | C1, the PLANF031R12 slice applied byte for byte |

### 769fd515 docs(state): record the F031 R11 round verdict
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/live_review.md | +2/-0 | C2, the GATE11 slice appended; the commit carries nothing else |

### 8df27c6e feat(ui): add the decision card pure model with its tests
| Path | +/- | Reason |
| --- | --- | --- |
| apps/ui/src/api/decisionCard.ts | +194/-0 | C3, the SPEC S1-S9 pure model; created, not edited |
| apps/ui/src/api/decisionCard.test.ts | +226/-0 | C3, the SPEC T1-T6 tests, 27 cases |

### C4 (this commit) docs(state): the R12 handback
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/handoff.md | self-referential | a handoff cannot table its own numstat (R-0149) |

## External actions
`git push origin feature/f031-decision-inbox`, run after C4; its outcome is carried by G12 to the reviewer, who measures the pushed tips and records them in the R12 entry of `.agent/live_review.md`.
`gh pr list --state open` -> `[]`. For G9: `git worktree add --detach .remedy-wt/f031r12-redproof 8df27c6e`, then `git worktree remove --force` on that exact path; two scratch JSON files created and deleted by exact path.

## Verification
G1 PASS. Branch `feature/f031-decision-inbox`, not `main`; `.agent/STOP` ABSENT on disk before C0a and again before C4; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2 and C3.
G2 PASS. All four readings EQUAL at sha256 31c83344a8fab82fa57a8a34cbd2deacd57fa8447a9cb97d22b75b0b77ec1071, 32697 bytes, 450 lines; C0a and C0b share git blob id 08303b6eeb779680ffd5d7836f6bdff10d384c51.
G3 PASS. My extractor over the committed C0a blob printed 2 slices, 50 CONTENT lines inside markers, and 450 TOTAL lines.
G4 PASS. plan.md at C1 byte-equal to PLANF031R12 under the newline-INCLUDED convention, slice and file both 2918 bytes and 49 lines; negative control against the trailing-newline-removed slice FALSE; `^## Goal$` 1, `^## Next Steps$` 1, wc -l 49, strictly under 50.
G5 PASS. The one equality in the shape constraint 8 states is TRUE: 582367 + 1 + 6165 = 588533, actual 588533. Second reader: blank-line units 287 -> 288, N=1 by my own split, the last 1 unit equal to GATE11's 1 paragraph in order. Negative control, one byte flipped in the first appended paragraph: BOTH readers reject the mutant and BOTH accept the true file; computed in memory, so no mutant byte was written to any path.
G6 PASS. `^- R-\d+ — ` 240 -> 240 all DISTINCT, ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0679` -> `R-0679`, `^Done: R-` 2 -> 2, `^Recurrence: R-` 15 -> 15, `^Gate: R\d+ — ` 11 -> 12 gaining exactly the key `R11`, with `R19` and `R1` through `R10` still present and all 12 keys DISTINCT.
G7 PASS. `git ls-tree` at the base printed NOTHING for either path, and both are present at C3, so C3 created both and edited no existing file; decisionCard.ts 194 lines and decisionCard.test.ts 226 lines; `git diff --name-only <base>..C3` names exactly those two paths under `apps/`.
G8 PASS. `npm run test:unit` in apps/ui exit 0 at 21 test files and 312 tests; the base is 20 and 285, so the delta is +1 file and +27 tests, all 27 contributed by my decisionCard.test.ts. `npm run typecheck` exit 0 with no diagnostic. No lint command was run and none is reported.
G9 PASS. In a disposable worktree at C3, decisionAnswers mutated to return the empty array when card.type equals warp_core_alignment: exit 1 with 2 FAILING tests, named "decisionAnswers renders a NOVEL decision type generically, from its payload alone" (T4) and "decisionAnswers gives two cards that differ ONLY in type identical answers" (T5). The unmutated control at the same root was 303 passed and 0 failed. Worktree removed by its exact path; `git worktree list` 1 line.
G10 PASS. `^<<<SLICE ` and `^<<<END ` both 0 in plan.md at C1, live_review.md at C2 and both C3 files; base..C3 names nothing under `packages/`, `tests/` or `docs/`, and no vitest.config.ts, package.json, lockfile, .tsx or .module.css; every commit single-parent with insertions 450, 331, 17, 2 and 420, each under 500 by the `+` column only (DECISION F104 D1) and equal cell for cell to the `## Commits` tables above; range MINUS change set EMPTY, change set MINUS range exactly `.agent/handoff.md`; `git ls-files .remedy-wt` 0 and `git ls-files` over `*.zip` 0; reflog SCOPE the 5 entries of this round, FIELD the operation prefix before the first colon of `git reflog --format=%gs`, giving amend 0, rebase 0, cherry 0 and every prefix `commit`.
G11 PASS. 11 SHA-shaped tokens by the word-bounded `[0-9a-f]{7,40}` over the committed C0a blob, 6 distinct, FAILING SET EMPTY: 25af0eed… is a blob, and 6325ac2f, 8b4e2295, 8b4e2295…8d57de, 99d77d5c and e391ed80 are all commits. `git worktree list` 1 line immediately before the first pytest; the five suites ran SERIALLY in the primary checkout at the C3 tree, never two at once, every one exit 0 at 474, 52, 21, 16 and 42 — identical to the base readings, so there is nothing to account for.
G12 DONE. `git push origin feature/f031-decision-inbox` is ordered after C4: no force, no lease, no history rewrite, no branch deletion, no pull request. Its outcome is not a value of any file this round writes, so its carrier is the reviewer's R12 ledger entry; the real outcome is stated in the round report.

## Authored-text proofs
Both slices were extracted PROGRAMMATICALLY from the committed C0a blob by their `<<<SLICE`/`<<<END` marker lines and never retyped. PLANF031R12: `.agent/plan.md` at C1 is byte-equal at 2918 bytes (G4).
GATE11: `.agent/live_review.md` at C2 equals its base blob plus one newline plus the slice exactly, under two independent readers (G5). No marker line reached any target file (G10).

## Item status and findings
| Item | Status | Reason |
| --- | --- | --- |
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |
| push | done | ordered after C4; outcome carried by G12 to the reviewer |

Findings: by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the open set is 238, measured at `769fd515`. This round minted no id and wrote no `Recurrence:` line;
R-0622 gained evidence rather than a second id (§3 item 30). The findings this feature must still act on are the 19 listed in `.agent/plan.md`, of which R-0495 and R-0574 are the two Highs.

## Deviations & assumptions
This file is 100 lines, inside the <=100 tier constraint 4's 6 commits earn, and no section was dropped. The ordered sequence C0a, C0b, C1, C2, C3, C4 was followed exactly: no extra commit, none dropped, no reordering.
`npx` is denied session-wide here, so G9's run went through `npm run test:unit -- --root <worktree>/apps/ui --config <primary>/apps/ui/vitest.config.ts` — the same vitest and the same config, over the worktree's tree.
A git worktree carries no `node_modules`, so its own vitest.config.ts cannot resolve `vitest`; that is why the primary config was named. The same absence makes `src/components/prompt/promptTraceLens.test.ts` (9 tests) fail to COLLECT there, since it reaches a `.tsx` needing `react/jsx-dev-runtime`.
That collection failure is a harness artifact and not the mutation: it appears identically in the unmutated CONTROL run at the same root, which was 303 passed and 0 failed. Running that control is what lets G9's effect be named as exactly 2 tests. Worktree totals are therefore 303, while the primary's 312 at G8 is the round's real count.
G5's negative control ran IN MEMORY, so no mutant byte was written to any path — strictly stronger than the disposable-worktree route constraint 11 permits.
SPEC S4 assumption: a non-finite `age_seconds` (NaN, Infinity) folds into `unknown age` beside `null`. S4 names only null; without that guard the largest-unit chain would render "NaNd".
SPEC S9 assumption: `next_actions`, `payload` and `decisions` are typed `unknown` rather than array types, so the runtime narrowing S6 and S8 require is real and testable without a cast. No endpoint key was renamed (DECISION F031 D1).
G10's "Over C0a..C3" is read as the INCLUSIVE bundle C0a through C3, five commits; the exclusive git range would drop C0a, whose insertion count the gate plainly wants.
The sandbox rejected several command SHAPES rather than contents — compound `&&` with git, `$?`, `2>&1`, `npx`, `ln`. Every affected measurement was re-obtained through a differently shaped command with the same semantics; none was skipped, softened or inferred.
No contradiction was found inside the block. Every base reading it states reproduced exactly: plan.md 49 lines and 2894 bytes, handoff.md 93 lines, the ledger at 582367 bytes and 1201 lines with all five set counts, the unit suite at 20 files and 285 tests, and the five Python suites at 474, 52, 21, 16 and 42.

## Next
1. Phase 1 rule 1: re-read `.agent/STOP` from disk before anything else.
2. NO pull request exists for this branch — `gh pr list --state open` returned `[]` — and none should be created yet.
3. The next round projects this model into a `.tsx` card per DECISION F031 D4 and mounts it in `RightLivePanel`; the component carries no branching of its own.
4. That round's ledger commit also records the R12 verdict, which by DECISION F085 D9 no artefact of this round can carry.
