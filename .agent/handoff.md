# Handback — F031 Decision inbox, R15

Feature F031 · Round R15 · Branch `feature/f031-decision-inbox` · Base `e12a4d46`
Fortschritt: ~55 % (F031 claimed; R1 through R14 landed and gated ·
             T001 SHIPPED · T002a MODEL shipped, red-proofed and wired
             · this round renders it · T002b ordering/filtering/badge
             und T003 offen) — Schaetzung

## Range
Review of `e12a4d46989ec1780771b94fee0fbb44c528a8d0..HEAD`, where HEAD is the C4 commit that writes this file — its own SHA cannot exist in the text it writes.

## Commits

### a9d519cc chore(agent): save the F031 R15 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r15.md | +451/-0 | C0a, the block saved verbatim |

### d0fd744b chore(agent): mirror the R15 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +238/-231 | C0b, byte-identical mirror of the C0a blob |

### 7add6592 docs(agent): set the F031 plan to the R15 step
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20/-20 | C1, PLANF031R15 applied whole |

### f885c65b docs(agent): record the F031 R14 verdict and register the R-0441 recurrence
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2, LEDGER15 appended |

### 58506912 feat(ui): render the decision inbox in the right live panel
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/panels/DecisionInboxCard.tsx | +64/-0 | C3, the new component (S1) |
| apps/ui/src/components/panels/RightLivePanel.module.css | +32/-0 | C3, appended classes (S3) |
| apps/ui/src/components/panels/RightLivePanel.tsx | +2/-0 | C3, import and mount (S2) |

### C4 docs(agent): write the F031 R15 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-reference | C4 writes this file; its own numstat cannot exist while the text is written (R-0149) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| push | done | ordered after C4; outcome carried by G11 to the reviewer |

## External actions
- `git worktree add --detach .remedy-wt/r15-mutant HEAD` rc 0, then `git worktree remove .remedy-wt/r15-mutant` rc 0 — the G5 mutant.
- `git worktree add --detach .remedy-wt/r15-mount HEAD` rc 0, then the matching `git worktree remove` of that exact path rc 0 — the G9 probe.
- `git push origin feature/f031-decision-inbox`, run after C4. The reviewer measures the pushed tips at the next gate and records them in the R15 entry of `.agent/live_review.md`.
- No pull request created, edited or merged; no `gh` command run; no history rewritten.

## Verification
- G1 — `git branch --show-current` printed `feature/f031-decision-inbox`, not `main`. `.agent/STOP` read from disk: ABSENT before C0a and ABSENT before C4. `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3.
- G2 — four readings (scratch before C0a, committed C0a blob, committed C0b blob, `.agent/last_block.md` off disk) all sha256 `a54c7a0ba757764d1eae510dfdc1680ba8ba8b568609045c7021a463c0ea541f`, 34734 bytes, 451 lines, ALL FOUR EQUAL. C0a's and C0b's file is the SAME git blob `dc1cc6863a19439c9a6b3983d87cac7a7a11fd64`.
- G3 — my extractor over the committed C0a blob printed: 2 slices, 52 content lines inside markers, 451 total lines.
- G4 — `.agent/plan.md` at C1 byte-equal to PLANF031R15, 2894 bytes each, under the newline-INCLUDED convention (the slice ends in a newline and nothing is appended after it). NEGATIVE CONTROL against the slice with its trailing newline removed: FALSE. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 49, strictly under 50.
- G5 — the one equality in the shape constraint 7 states: TRUE, with 604055 + 1 + 7664 = 611720 against an actual 611720. Independent reader: blank-line units 292 before and 294 after; my split of LEDGER15 measured N = 2; the last 2 units equal the slice's 2 paragraphs IN ORDER. NEGATIVE CONTROL, written only inside `.remedy-wt/r15-mutant`: one byte flipped at file offset 604156 inside the FIRST paragraph the append added — BOTH readers reject the mutant and BOTH accept the true file.
- G6 — `^- R-\d+ — ` 241 to 241, all DISTINCT, ids ADDED the EMPTY SET and ids REMOVED the EMPTY SET, maximum `R-0680` UNCHANGED. `^Done: R-` 3 to 3. `^Recurrence: R-` 15 to 16, added exactly `R-0441`. `^Gate: R\d+ — ` 14 to 15, gaining exactly the key `R14`, with `R19` and `R1` through `R13` still present and all 15 keys DISTINCT. §3 item 10 open set at C2: 238.
- G7 — `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2, and each of the three `apps/` files at C3. The range names no path under `packages/`, `tests/` or `docs/`, no `apps/` path beyond the three section 5 names, and neither `.agent/decisions.md` nor `.agent/context.md` nor either inventory. Range MINUS change set: EMPTY. Change set MINUS range: exactly `.agent/handoff.md`. Every commit C0a..C3 single-parent; `git diff --numstat` insertions C0a 451, C0b 238, C1 20, C2 4, C3 98, each under 500 and each equal cell for cell to the `## Commits` table above. `git ls-files .remedy-wt` 0; `git ls-files` over the zip glob 0. Reflog scoped to this round's entries only — 5 of them — read by the operation prefix before the first colon: all 5 are `commit`, so `amend` 0, `rebase` 0, `cherry` 0.
- G8 — `npm run typecheck` real exit 0 with no diagnostic line on stdout. `npm run test:unit` real exit 0 at 21 test files and 316 tests, both UNCHANGED from the base. Over the new `DecisionInboxCard.tsx` at C3, each number measured by me: `switch` 0; `type` or `status` followed by `===`, `!==`, `==` or `!=` 0, and 0 again under a looser same-line variant; the import line is `import type { DecisionCardModel } from "../../api/decisionCard";`. Token gate: the `--remedy-*` properties `RightLivePanel.module.css` USES via `var(...)` (24 of them) minus those `apps/ui/src/styles/` DEFINES (58 of them) is the EMPTY SET, as at the base; hex literals among the 32 lines C3 adds to that file: 0, and 0 `#` characters of any kind.
- G9 — a PROBE, and this is what actually happened. Mounted at C3: `RightLivePanel.tsx` line 7 imports the component and line 22 reads `      <DecisionInboxCard decisions={dashboard.decisionInbox} />`; `DecisionInboxCard.tsx` resolves at C3 as a blob. In `.remedy-wt/r15-mount` with that mounting line DELETED, `npx vitest run --root <wt>/apps/ui --config <primary>/apps/ui/vitest.config.ts` from the primary `apps/ui` gave rc 1, 307 passed, 1 file failed — and the UNMUTATED control in the SAME worktree gave the identical rc 1, 307 passed, and the same single failing file `src/components/prompt/promptTraceLens.test.ts`, which R-0653's resolution names as a worktree artifact rather than a result. NOTHING WENT RED FROM THE DELETION: no test reaches this markup, exactly as DECISION F031 D5 says, and that is the honest limit of this round's evidence. Worktree removed by its exact path; afterwards `git worktree list` 1 line and `git status --porcelain` 0 in the primary checkout. The typecheck half of this probe is declared below.
- G10 — SHA-shaped `[0-9a-f]{7,40}` tokens in the committed C0a blob: 19 occurrences, 7 distinct. FAILING SET EMPTY. Types: `cb5e9ea8188e9ec89b9419238a53bfa4813e0ebe` is `blob`; `475f0f36`, `597c20ce`, `6325ac2f`, `d63a146f`, `e12a4d46` and `e12a4d46989ec1780771b94fee0fbb44c528a8d0` are `commit`. `git worktree list` 1 line immediately before the first pytest. Run SERIALLY, never two alive: `tests/ui_server/` rc 0 at 474 passed; `test_test_runner.py` rc 0 at 52; `test_resource_safety.py` rc 0 at 21; `test_integrity_gate.py` rc 0 at 16; `test_golden_path.py` rc 0 at 42 — identical to the base readings, so there is no difference to account for.
- G11 — run after C4; the command is in `## External actions` and its outcome is carried by the reviewer, not by any file this round writes.

## Authored-text proofs
- PLANF031R15 — extracted programmatically from the COMMITTED C0a blob by its marker lines, written to `.agent/plan.md`. Disk-to-disk equality against the extracted slice: TRUE, 2894 bytes each; negative control FALSE.
- LEDGER15 — extracted the same way, appended to `.agent/live_review.md`. Whole-file equality against base blob plus one newline plus the slice: TRUE at 611720 bytes, corroborated by the independent blank-line reader.

## Deviations & assumptions
- No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, C4 — six commits, none extra, none dropped, none reordered.
- ASSUMPTION (S1): section 5 names the component's prop only as "the models to render". I named it `decisions`, matching `dashboard.decisionInbox` and the one-noun prop idiom of `TaskChecklistCard({ tasks, jobId, onSelectNode })`.
- DECLARED READING (C0b `+/-`): `git commit` reported 451 insertions and 444 deletions for `.agent/last_block.md` under its own rewrite detection, while `git diff --numstat` reports 238 and 231. G7 orders the column from `git diff --numstat`, so the table carries 238/231. Both readings are under the 500 cap.
- DECLARED LIMIT (the G9 typecheck half): R-0653's resolution supplies a worktree route for VITEST only. `npx tsc --noEmit --project <wt>/apps/ui/tsconfig.json` from the primary `apps/ui` cannot resolve the worktree's absent `node_modules`, so the UNMUTATED control in that worktree already emits 795 diagnostics (codes TS2307, TS2503, TS2875, TS6133, TS7006, TS7026). Deleting the mount line changes that output by exactly one NEW diagnostic beyond line-number shift — `TS6133: 'DecisionInboxCard' is declared but its value is never read` — which is a statement about the now-unused import, not evidence that anything tests the markup. The usable typecheck reading is G8's, taken in the primary checkout.
- SCRATCH HYGIENE: two disposable worktrees created and removed BY EXACT PATH (`.remedy-wt/r15-mutant`, `.remedy-wt/r15-mount`); three scratch files I created myself removed by exact path (`.remedy-wt/r15_slice_PLANF031R15.txt`, `.remedy-wt/r15_slice_LEDGER15.txt`, `.remedy-wt/r15_tsc_control.txt`). Nothing pre-existing under `.remedy-wt/` was created, moved or deleted.
- NO CONTRADICTION FOUND inside the block: every base reading it states reproduced at `e12a4d46`, including the ledger sets, the 58 defined tokens, and the empty used-minus-defined set.
- FINDINGS. This round mints no id and writes no `Done:` line; it writes one `Recurrence:` line, for `R-0441`. By §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the set is 238, measured at C2 `f885c65b`. The narrower set, the findings this feature must still act on, is the list `.agent/plan.md` names at `7add6592`: R-0403, R-0413, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0622, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679 — counted mechanically at 20 distinct ids, of which R-0495 and R-0574 are the two Highs. Both numerals were counted by script before this file was committed, which is the widened R-0441 rule LEDGER15 registers.
- HANDBACK TIER: constraint 3 fixes the round at 6 commits, so AGENTS.md `### handoff.md` gives the >5-commit tier of ≤100 lines. Measured with `wc -l`: 94 lines, within that tier.

## Next
1. Phase 1 rule 1: re-read `.agent/STOP` from disk.
2. Phase 1 rule 2, the Open PR Gate: run `gh pr list --state open`, report what it printed, and report whether any pull request exists for `feature/f031-decision-inbox`.
3. The R15 verdict is UNRECORDED and is owed by the next round's ledger commit — by DECISION F085 D9 no artefact of this round can carry it.
4. The next build step is T002b: ordering over age and blocked size, filtering, and the badge, under DECISION F031 D2.
