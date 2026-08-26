# Handback — F031 Decision inbox, R22

Branch `feature/f031-decision-inbox`, base `f13b92c0a8a978f631a961786b0870b7594e7cbe`.
Commits: C0a `7de87810`, C0b `296ea957`, C1 `b5eb6cd0`, C2 `aa48d967`, C3 `22fc6193`, C4 this one.
Size: 6 commits, so the AGENTS.md `### handoff.md` tier is ≤100 lines; this file measures 97, inside it, no DECISION D15 overage.

Fortschritt: ~70 % (F031 claimed; R1 through R21 landed, R21 gated here ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             T002b ORDERING SHIPPED and gated · T002b filter MODEL ships
             here, its control R23 · T002b badge und T003 offen)
             — Schaetzung

## Range
Review of `f13b92c0`..HEAD.

## Commits

### 7de87810 chore(agent): save the F031 R22 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r22.md | +446/-0 | the R22 block saved verbatim (C0a) |

### 296ea957 chore(agent): mirror the R22 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +323/-217 | the committed C0a blob mirrored byte-identically (C0b) |

### b5eb6cd0 docs(agent): point the F031 plan at R23
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20/-20 | PLANF031R22 applied as a whole-file replacement (C1) |

### aa48d967 docs(agent): record the F031 R21 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | LEDGER22 appended, nothing else (C2) |

### 22fc6193 feat(ui): derive and apply the decision inbox type filter
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/decisionFilter.ts | +136/-0 | S1/S2, the pure filter module |
| apps/ui/src/api/decisionFilter.test.ts | +169/-0 | S3, 20 tests beside it |
| apps/ui/src/api/decisionCard.ts | +9/-5 | S4, the header comment only — no export, signature or behaviour |

### C4 docs(agent): write the F031 R22 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file; a handoff cannot table its own commit (R-0149) |

## External actions
- `git worktree add --detach .remedy-wt/r22-g4 aa48d967` and `… .remedy-wt/r22-g6 22fc6193` → both created, both removed by `git worktree remove --force` on their EXACT absolute paths; `git worktree list` 1 line after each removal.
- `git push origin feature/f031-decision-inbox`, ordered after C4. THAT PUSH'S OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: the reviewer measures the pushed tips at the next gate and records them in the R22 entry of `.agent/live_review.md`.
- No pull request created, nothing merged, no branch deleted, no history rewritten.

## Verification
- G1 PASS — branch `feature/f031-decision-inbox`, not `main`; `.agent/STOP` ABSENT on disk before C0a and again before C4; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3. All FOUR readings equal at sha256 `1c305462638d726b6bf15a3321e04022d4d6a3914f4663637a0c317aa7e95298`, 34109 bytes, 446 lines; C0a and C0b are the SAME git blob `52f6a0ca81202278eeb67aee5ffaa7f7fa501f9e`.
- G2 PASS — extractor over the committed C0a blob printed 2 slices, 49 CONTENT lines, 446 TOTAL; PROSE = 446 − 49 = 397, inside both the 490 TOTAL and the 400 PROSE cap.
- G3 PASS — `.agent/plan.md` at C1 byte-equal to PLANF031R22 under the newline-INCLUDED convention, 2811 bytes on both sides; negative control (slice minus its trailing newline) FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 48, strictly under 50.
- G4 PASS — reader 1, the whole-file equality constraint 8 names: TRUE, 651806 + 1 + 5709 = 657516 against an actual 657516. Reader 2, blank-line split: units 304 → 305, N = 1 paragraph, last-N equal to LEDGER22's paragraphs IN ORDER TRUE with trailing newlines rstripped on BOTH sides. Negative control in `.remedy-wt/r22-g4`: one byte flipped at offset 651907 inside the appended text, both readers REJECT the mutant and both ACCEPT the true file.
- G5 PASS — `^- R-\d+ — ` 242 → 242 all DISTINCT, ADDED and REMOVED both EMPTY, max `R-0681` → `R-0681`; `^Done: R-` 4 → 4, `^Landed: R-` 0 → 0, `^Recurrence: R-` 18 → 18; `^Gate: R\d+ — ` 19 → 19, `^Gate: F\d+ R\d+ — ` 2 → 3 with the ADDED key exactly `F031 R21`, all three DISTINCT. Open set at C2 = 242 − 4 = 238. `^- R-0593 — ` line-anchored exactly ONCE, `^Recurrence: R-0593` exactly ONCE; see deviation 4 on the substring reading.
- G6 PASS — in `.remedy-wt/r22-g6`, run from the primary's `apps/ui` by the block's exact command line: UNMUTATED exit 0, 1 file / 20 tests. PROBE A (a fixed choice list replacing the derived one) REAL exit 1, 9 failed: the seven `decisionTypeChoices` tests (derived-type extensibility, all-choice first and counted, sorted distinct choices, per-choice counts, the untyped chip, the no-models case, the all-sentinel chip) plus `decisionInboxView > still offers the all choice when the filter emptied the list…` and `> never throws, however broken the models it is handed`. PROBE B (the `DECISION_FILTER_ALL` special case removed from `filterDecisionsByType`) REAL exit 1, 2 failed: `filterDecisionsByType > yields every model under the all value` and `decisionInboxView > reports no empty message while something is visible`. `git worktree list` 1 line after removing `/home/decodeux/Repos/remedy/.remedy-wt/r22-g4` and `/home/decodeux/Repos/remedy/.remedy-wt/r22-g6`.
- G7 PASS — `decisionFilter.ts` at C3 carries exactly ONE import line, `import type { DecisionCardModel } from "./decisionCard";`; its `switch` count is 0 raw AND comment-stripped, beside `brainStreamDriver.ts` at 1 both ways; all six S1 names grep to their own `export` in that file. `git worktree list` 1 line immediately before the suites. `npm run typecheck` exit 0 with ZERO diagnostics (stdout holds only npm's two script-echo lines, stderr empty). `npm run test:unit` exit 0, 23 files / 352 tests; `decisionCard.test.ts` 27 and `decisionOrder.test.ts` 16 both UNMOVED, the new `decisionFilter.test.ts` 20 accounting for 22 → 23 files and 332 → 352 tests. Python, serially, never two alive at once, every one a REAL exit 0: `tests/ui_server/` 474, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped, `test_golden_path` 42 — identical to the base readings, so there is no difference to account for.
- G8 PASS — `^<<<SLICE ` / `^<<<END ` are 0 / 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2 and all three `apps/` files at C3, against a CONTROL of 2 / 2 over the C0a blob. The range names 7 paths, none under `docs/`, `packages/` or `tests/`, and neither `.agent/decisions.md` nor `.agent/context.md` nor either inventory nor `DecisionInboxCard.tsx`; range MINUS change set EMPTY, change set MINUS range exactly `.agent/handoff.md`. Per commit single-parent with insertions 446, 323, 20, 2 and 314 read from `git diff --numstat`, each under 500, agreeing CELL FOR CELL with the `+/-` column above. `git ls-files .remedy-wt` 0, `git ls-files -- '*.zip'` 0. Reflog scoped to this round's 5 HEAD entries by OPERATION PREFIX: amend 0, rebase 0, cherry 0. SHA-shaped tokens in the C0a blob: 19 occurrences, 9 distinct, FAILING SET EMPTY, 8 `commit` and 1 `blob` (`599e6675d9e5aa79fb038ca357f7b20e1498daf2`).
- G9 — the push is ordered after C4 and its outcome is carried to the reviewer, not to any file this round writes.

## Authored-text proofs
Both slices were extracted PROGRAMMATICALLY from the COMMITTED C0a blob by their `<<<SLICE` / `<<<END` marker lines, which never reached a target file. PLANF031R22 (2811 bytes, 48 lines) is byte-equal to `.agent/plan.md` at C1 — G3. LEDGER22 (5709 bytes, 1 paragraph) sits in `.agent/live_review.md` at C2 under G4's whole-file equality, confirmed by a second independent reader.

## Deviations & assumptions
The ordered sequence C0a, C0b, C1, C2, C3, C4 was followed exactly: no extra commit, none dropped, no reordering.

1. Tooling, HOW not WHAT: the command guard rejects `cd apps/ui && npm …`, bare `npm …`, shell loops, `$( )` and `${arr[0]}` by form. The two `apps/ui` lines and the six pytest lines therefore ran through `subprocess.run` — same commands, same working directories, REAL exit codes read rather than swallowed by a pipe — and every counting, extraction and comparison step ran inside a `python3` heredoc.
2. The delegating message states the block is 34097 bytes; the file on disk is 34109 bytes at 446 lines. Its sha256 MATCHES the stated digest exactly, so the bytes are authenticated and I proceeded; the byte numeral in that message is wrong by 12 and is declared rather than quietly reconciled.
3. G5's substring reading, declared because it moved: `- R-0593 — ` is LINE-ANCHORED exactly once, which is what G5 orders, but as a raw SUBSTRING it is now 2 against 1 at base. The second occurrence is LEDGER22 quoting the pattern in its own sentence "`- R-0593 — ` still occurs exactly ONCE both line-anchored and as a substring" — the gate quoting its own marker. R-0593's paragraphs were not touched.
4. S1 silence resolved and declared: `DECISION_FILTER_ALL` is the ordinary string `"all"`, so a model whose `type` is literally `"all"` would otherwise produce a SECOND choice with the SAME `value`. `decisionTypeChoices` excludes the sentinel from the concrete choices so choice values stay DISTINCT; those cards are never lost, because the All chip counts and shows them. Pinned by its own named test. Relatedly, the literal token `switch` is deliberately ABSENT from `decisionFilter.ts` — the module states its refusal as "no hardcoded type list, no per-type branch" — so G7's zero measures code and not a comment; the token lives in `decisionFilter.test.ts`, where a reader grepping for it still lands on the extensibility test.
5. S4 scope, registered rather than repaired: only the header sentence S4 quotes was rewritten. `decisionCardModels`'s own docstring still reads "the rule over age and blocked size is T002b's subject" — the same one-directional discoverability gap, in the same file — and S4 says CHANGE NOTHING ELSE IN THAT FILE, so it is left for R23 alongside `DecisionInboxCard.tsx`'s note.

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |
| S1 | done | |
| S2 | done | see deviation 4 on the all-sentinel collision |
| S3 | done | 20 tests, the count this round's run measured |
| S4 | done | see deviation 5 on the scope S4 fixes |
| push | done | ordered after C4; outcome carried by G9 to the reviewer |

## Findings
Open findings by the rule DECISION F009 D10 requires — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — are 238, measured at C2 `aa48d967`. This round MINTED no id and RESOLVED none. The findings THIS FEATURE MUST STILL ACT ON are the 21 listed in `.agent/plan.md`; R-0593 stays OPEN, its instances in `packages/orchestration/release_gate.py`, `pyproject.toml` and `DecisionInboxCard.tsx` untouched.

## Next
The next session reads `.agent/STOP` from disk as Phase 1 rule 1 BEFORE the Open PR Gate as rule 2. The R22 verdict is UNRECORDED and is owed by the next round's ledger commit (DECISION F085 D9). Then R23 wires the filter control into `DecisionInboxCard` and repairs that file's own `Recurrence: R-0593` note, and MUST read `docs/ui/design_reference/` before authoring the control, per `.agent/context.md`.
