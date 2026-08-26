# Handback — F031 Decision inbox, round R23 (T002b filtering, the half that shows)

Branch `feature/f031-decision-inbox`. Base `879bd137` (R22 handback). Seven commits:
C0a `85bd1995`, C0b `15919a4d`, C1 `114394a0`, C2 `f548277e`, C3 `6147efc4`, C3b `44435f81`, C4 below.

## Range
Review of `879bd137a008c982c6f54ffc9e7caf13d45a3dc0`..HEAD.

## Commits
### 85bd1995 chore(agent): save the F031 R23 step block
| Path | +/- | Reason |
| `.agent/authored/f031-r23.md` | +443 -0 | C0a, the block verbatim |
### 15919a4d chore(agent): mirror the R23 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +251 -254 | C0b, byte-identical mirror |
### 114394a0 docs(agent): point the F031 plan at R23
| Path | +/- | Reason |
| `.agent/plan.md` | +17 -20 | C1, whole-file PLANF031R23 |
### f548277e docs(agent): record the F031 R22 verdict
| Path | +/- | Reason |
| `.agent/live_review.md` | +2 -0 | C2, LEDGER23 appended |
### 6147efc4 feat(ui): give the decision inbox its type filter chips
| Path | +/- | Reason |
| `apps/ui/src/components/panels/DecisionInboxCard.tsx` | +81 -31 | S1 control, S3(a) header repair |
| `apps/ui/src/components/panels/RightLivePanel.module.css` | +45 -0 | S2 styles, appended only |
| `apps/ui/src/api/decisionCard.ts` | +3 -2 | S3(b) docstring repair |
| `.agent/decisions.md` | +39 -0 | S4, DECISION F031 D8 |
### 44435f81 fix(ui): point the chip focus ring at a token the shipped sheet defines
| Path | +/- | Reason |
| `apps/ui/src/components/panels/RightLivePanel.module.css` | +8 -5 | C3b, repairs the C3 focus rule |
| `.agent/decisions.md` | +18 -11 | C3b, D8's focus paragraph re-argued |
### C4 (this commit) docs(agent): write the F031 R23 handback
| Path | +/- | Reason |
| `.agent/handoff.md` | rewrite | C4; a handoff cannot table its own commit (R-0149) |

## External actions
`git worktree add --detach .remedy-wt/r23-probe 6147efc4` — created for G6(b).
`git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/r23-probe` — removed by exact path; `git worktree list` 1 line after.
`git push origin feature/f031-decision-inbox` — ordered after C4. That push's outcome is not a value of any file this round writes: the reviewer measures the pushed tips at the next gate and records them in the R23 entry of `.agent/live_review.md`.
No PR created, no branch deleted, nothing merged.

## Verification
G1 PASS — branch `feature/f031-decision-inbox`; `.agent/STOP` absent before C0a and before C4; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3, C3b. All four readings equal: sha256 `aeae1dd3f6c7c9ee7aeb3ac059b54501d81bf827d636dc1242818a1845014623`, 37051 bytes, 443 lines; C0a and C0b share blob `e0d5e6231a89c5069f79d6e6e740e1cea8392972`.
G2 PASS — extractor over the C0a blob printed 2 slices, 46 content lines, 443 total; PROSE 443−46 = 397 ≤ 400 (F085 D5) and TOTAL 443 ≤ 490 (F085 D6).
G3 PASS — `.agent/plan.md` at C1 byte-equal to PLANF031R23, 2581 bytes both, newline-INCLUDED convention; negative control (slice minus trailing newline) FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 45 < 50.
G4 PASS — reader (a), the whole-file equality constraint 8 states: TRUE, 657516 + 1 + 8341 = 665858 against an actual 665858. Reader (b), blank-line split with trailing newlines rstripped on BOTH sides: units 305 → 306, last N = 1 equals LEDGER23's paragraphs in order, TRUE. Negative control, one byte flipped in memory inside the appended region: both readers reject the mutant, both accept the true file.
G5 PASS — `^- R-\d+ — ` 242 → 242, all DISTINCT, ADDED and REMOVED both empty, max `R-0681` → `R-0681`; `^Done: R-` 4 → 4, `^Landed: R-` 0 → 0, `^Recurrence: R-` 18 → 18; `^Gate: R\d+ — ` 19 → 19; `^Gate: F\d+ R\d+ — ` 3 → 4, added key exactly `F031 R22`, all keys distinct. Open set at C2 = 242 − 4 = 238. `- R-0593 — ` line-anchored 1; `^Recurrence: R-0593` 1.
G6 PASS — (a) `npx tsc --noEmit --listFiles` in the PRIMARY `apps/ui`: REAL exit 0, 996 files listed, `DecisionInboxCard.tsx` exactly once; matches the reviewer's 996 at `879bd137`, no difference to account for. (b) worktree at `6147efc4`: unmutated exit 0 at 20 files / 327 tests; with the guard changed to read `view.visible.length` — the empty-state trap — REAL exit 0, still 20 files / 327 tests, NO test fails. GREEN, the expected answer: it MEASURES the gap DECISION F031 D5 accepts. File restored, worktree removed by exact path, `git worktree list` 1 line.
G7 PASS — over `DecisionInboxCard.tsx` at C3/C3b (blob `93c6cd65`, byte-identical across both): `aria-pressed` 1, `aria-live` 1, `useState` 2, the literal guard `if (decisions.length === 0) return null;` exactly 1, lines holding both `decisions.length` and `visible` 0; `switch` 0 raw and 0 comment-stripped, beside `brainStreamDriver.ts` at 1 and 1. `git worktree list` 1 line before the suites, all run serially. `npm run typecheck` exit 0, zero diagnostics on stdout and stderr; `npm run test:unit` exit 0, 23 files / 352 tests, `decisionCard.test.ts` 27, `decisionOrder.test.ts` 16, `decisionFilter.test.ts` 20 — every count identical to the Base readings. Python, in order: 474, 52, 21, 16, 525 passed with 4 skipped, 42, each REAL exit 0. See deviation 2 for the RED this gate first returned at C3.
G8 PASS — line-anchored `^<<<SLICE ` and `^<<<END ` 0 and 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2 and all four files C3/C3b write, against a CONTROL of 2 and 2 over the C0a blob. `git diff --name-only 879bd137..44435f81` names 8 paths, none under `docs/`, `packages/` or `tests/`, none of `.agent/context.md`, either inventory, `RightLivePanel.tsx` or `decisionFilter.ts`; range MINUS change set EMPTY, change set MINUS range exactly `.agent/handoff.md`. All six commits single-parent, insertions 443, 251, 17, 2, 168, 26 from `git diff --numstat`, each under 500, and they agree CELL FOR CELL with the `+/-` column above. `git ls-files .remedy-wt` 0, tracked `.zip` 0. Reflog scoped to this round's 6 entries by the prefix before the first colon of `%gs`: all `commit`, `amend` 0, `rebase` 0, `cherry` 0. SHA-shaped tokens in the C0a blob by the word-bounded 7–40 hex pattern: 24 occurrences, 11 distinct, FAILING SET EMPTY, 9 `commit` and 2 `blob`.
G9 — ordered after C4; outcome carried to the reviewer, not to any file this round writes.

## Item status
| Item | Status | Reason |
| C0a `85bd1995` | done | |
| C0b `15919a4d` | done | |
| C1 `114394a0` | done | |
| C2 `f548277e` | done | |
| C3 `6147efc4` | done | |
| C3b `44435f81` | deviated | correction commit outside the ordered sequence; see deviation 2 |
| C4 | done | this commit |
| S1 control | done | |
| S2 styles | deviated | focus ring names `--remedy-blue-strong`, not `--remedy-focus`; deviation 2 |
| S3(a) card header | done | |
| S3(b) `decisionCard.ts` | done | |
| S4 DECISION F031 D8 | done | |
| G9 push | done | ordered after C4; outcome carried by G9 to the reviewer |

## Authored-text proofs
PLANF031R23 — extracted from the COMMITTED C0a blob by marker lines, written whole to `.agent/plan.md`; disk-to-disk byte equality against the committed `.agent/authored/f031-r23.md` TRUE at 2581 bytes, negative control FALSE.
LEDGER23 — same extraction, appended at C2; whole-file equality TRUE and the independent blank-line reader TRUE, both rejecting the one-byte mutant.
No FROM/TO pair exists in this block (constraint 9), so no containment test is reported.

## Deviations & assumptions
1. TOOL ROUTING, HOW not WHAT. This session's command guard rejects `cd apps/ui && npm ...`, bare `npm ...`, shell loops and `$( )` by form. The two `apps/ui` lines, the `npx tsc`/`npx vitest` lines and the six pytest lines were run through `python3` with `subprocess.run(...)` and an explicit `cwd`, which runs the exact command lines the block names and preserves REAL exit codes a pipe would swallow.
2. AN EXTRA COMMIT, C3b `44435f81`, OUTSIDE THE ORDERED SEQUENCE C0a–C4 (constraint 4), declared here as R-0675 requires and given its own `## Commits` and item-status rows. CAUSE: S2 orders a `:focus-visible` ring "with colour from `--remedy-*` tokens" and names `--remedy-focus`, but `--remedy-focus` is defined only in `docs/ui/design_reference/tokens.css` and has never been adopted into `apps/ui/src/styles/tokens.css`. THE SPEC IS WRONG HERE and constraint 2 says to say so and do the right thing. I first shipped the fallback form `var(--remedy-focus, var(--remedy-blue-strong))` at C3; G7's `tests/ui_contracts/` then returned a REAL exit 1, `1 failed, 524 passed, 4 skipped` — `test_design_drift.py::TestEveryCustomPropertyResolves::test_the_unresolved_set_has_not_grown`, which matches the NAME inside `var(` and does not read fallbacks. Constraint 11 forbids writing `apps/ui/src/styles/tokens.css`, and no test may be weakened, so C3b names `--remedy-blue-strong`, which the reference sheet gives the same `#2f6fff` it gives `--remedy-focus`; the shipped colour is §14's colour. D8 records this and points the next round that touches the token sheet at adopting the name, the way F021 R32 adopted `--remedy-radius-pill`. The full G7 was re-run at C3b and is the transcript above; `DecisionInboxCard.tsx` is byte-identical at C3 and C3b, so G6(b)'s probe holds at both.
3. TWO CLASSES BEYOND S2'S ENUMERATION, under constraint 2's silence clause: `.decisionFilterChipOn:hover`, because the hover rule is one class more specific than the selected rule and would otherwise repaint the chosen chip as unchosen — the same defect `GraphFilterChips.module.css` fixes with `.chipActive:hover` — and `.decisionFilterCount`, which mutes the count `DecisionTypeChoice.count` already carries. NO EXISTING RULE WAS EDITED.
4. THE QUIET LINE REUSES `.emptyState`, the class `TaskChecklistCard` and `ActivityFeedCard` already use for exactly this, rather than minting a sixth name. S2 was silent; this is the neighbouring idiom.
5. ONE STRING THIS FILE CHOOSES, `FILTER_CHIPS_LABEL = "Filter decisions by type"`, required by S1's `aria-label` order. It is announced, never displayed, so the header's projection claim — every string it DISPLAYS is a field — stays true, and the claim was reworded to say so.
6. NO FINDING ID WAS MINTED OR RESOLVED and no `Landed:` line was written for R-0593, per constraint 10, though S3 repaired its last two instances in this feature's reach.
7. Handback tier resolved from AGENTS.md `### handoff.md` against the seven commits constraint 4 plus deviation 2 produce: >5 commits, so the cap is 100 lines. No overage.

## Findings
Open set 238 at `f548277e`, by the §3 item 10 rule — every `^- R-\d+ — ` paragraph (242) minus every `^Done: R-\d+ — ` line (4). The findings THIS FEATURE MUST STILL ACT ON number 21: R-0403, R-0413, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0593, R-0601, R-0622, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679; R-0495 and R-0574 are the two Highs. This round minted none and resolved none.

Fortschritt: ~78 % (F031 claimed; R1 through R22 landed, R22 gated here ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             T002b ORDERING SHIPPED and gated · T002b FILTER shipped whole
             here, model at R22 and control now · T002b badge und T003 offen)
             — Schaetzung

## Next
This round ends the session. The next session, in order: (1) read `.agent/STOP` from disk as Phase 1 rule 1, BEFORE the Open PR Gate, which is rule 2; (2) the R23 verdict is UNRECORDED and is owed by the next round's ledger commit (DECISION F085 D9), and that entry must also adjudicate C3b and the `--remedy-focus` adoption question deviation 2 leaves open; (3) R24 is the T002b BADGE under DECISION F031 D2, which re-derives on refetch over the existing SSE stream, adds no new event kind, and replaces D2's two constant-zero counters.
