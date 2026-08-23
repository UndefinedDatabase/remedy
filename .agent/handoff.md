# Handback — F031 R7 (T001: the decision inbox derivation, route and tests)
Branch: feature/f031-decision-inbox · Base: e73da3ef · no PR exists.
Fortschritt: ~20 % (F031 claimed; R1 through R6 landed and gated ·
             the source inventory and the three design rulings are
             on disk · T001 ships this round · T002 and T003 offen)
             — Schaetzung
(The `Fortschritt:` block above is carried verbatim; I counted 4 lines.)

## Range
Review of e73da3ef..HEAD — 7 commits: C0a 227e74aa, C0b 5d1d532e, C1 8a0bdc18, C2 85daf94d, C3 474dd6a8, C4 ce462ecc, C5 this one.

## Commits
### 227e74aa docs(state): save the F031 R7 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f031-r7.md | +457/-0 | C0a — block saved verbatim |
### 5d1d532e docs(state): mirror the F031 R7 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +382/-235 | C0b — byte-identical mirror of C0a |
### 8a0bdc18 docs(state): plan the F031 R7 T001 build round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +21/-21 | C1 — slice PLANF031R7 |
### 85daf94d docs(review): record the F031 R6 PASS and the R-0471 recurrence
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C2 — GATE6 then RECUR471, both in this one commit |
### 474dd6a8 feat(orchestration): derive the decision inbox view with age and blocked size
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/decision_inbox.py | +101/-0 | C3 — S1-S6, no I/O, no storage |
| tests/orchestration/test_decision_inbox.py | +290/-0 | C3 — S8 (a)-(f), 25 tests |
### ce462ecc feat(ui-server): expose the decision inbox as a read endpoint
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +8/-0 | C4 — S7: `_build_decisions_json` + the one `handlers` key |
| tests/ui_server/test_decisions_endpoint.py | +112/-0 | C4 — S9, 4 tests |
### C5 this commit (R-0149 self-reference exception)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5 — this handback |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| push | deviated | ordered by G11 and run after C5, but its OUTCOME is deliberately not written here: it is not a value of any file this round writes. The reviewer measures the pushed tips and records them in the R7 entry of `.agent/live_review.md` (R-0679 fix clause) |

## External actions
`git push origin feature/f031-decision-inbox` — run after C5. This gate's outcome is not a value of any file this round writes; the reviewer measures the pushed tips at the next gate and records them in the R7 entry of `.agent/live_review.md`.
`git worktree add --detach .remedy-wt/g5neg 85daf94d` then `git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/g5neg` — the G5 mutant only. Same pair for `.remedy-wt/g9a` and `.remedy-wt/g9b` at ce462ecc, each removed BY ITS EXACT PATH and all three before the G10 suites; `git worktree list` back to 1 line. `.remedy-wt/dry` was not created, read or deleted.
No `gh` command, no pull request, nothing merged, no history rewritten.

## Verification
G1 PASS — branch `feature/f031-decision-inbox`, not `main`; `.agent/STOP` absent from disk before C0a and again before C5; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3 and C4.
G2 PASS — scratch pre-C0a, committed C0a blob, committed C0b blob and `.agent/last_block.md` off disk are ALL sha256 9b1a517f52d133c610e40608faa1a8c20c41a2e59588cb98aad13d3bbcff2d69, 33656 bytes, 457 lines; C0a's and C0b's file are the SAME git blob 98f6f251.
G3 PASS — my extractor over the committed C0a blob printed 3 slices, 51 CONTENT lines inside markers, 457 TOTAL lines (6 marker lines).
G4 PASS — `.agent/plan.md` at C1 byte-equal to PLANF031R7, 2954 bytes both, newline-INCLUDED convention; negative control with the slice's trailing newline REMOVED is FALSE at 2953; `^## Goal$` 1, `^## Next Steps$` 1; `wc -l` 49, strictly under 50.
G5 PASS — reader A, ONE boolean over the whole file in the shape constraint 8 states (that paragraph, not restated here): True; 553746 → 561117 bytes, delta 7371 = 1 + 4255 + 1 + 3114. Reader B, an independent blank-line split: 281 → 283 units, the LAST TWO equal GATE6 then RECUR471 IN ORDER. Control: byte at offset 553947, inside the FIRST appended paragraph, flipped in the disposable worktree — BOTH readers rejected the mutant and BOTH accepted the true file.
G6 PASS — `^- R-\d+ — ` 240 → 240, all DISTINCT; ids ADDED the EMPTY SET and ids REMOVED the EMPTY SET; maximum R-0679 → R-0679; `^Done: R-` 2 → 2; `^Recurrence: R-` 14 → 15, the one gained line naming R-0471; `^Gate: R\d+ — ` 6 → 7 gaining exactly the key R6, with R19, R1, R2, R3, R4 and R5 still present.
G7 PASS — `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2 and each of the four source and test files at C3 and C4; `git diff --name-only e73da3ef..ce462ecc` names 8 paths, no path under `docs/` or `apps/` and neither `.agent/decisions.md` nor `.agent/f031_inventory.md`; range MINUS change set EMPTY; change set MINUS range exactly `.agent/handoff.md`; six single-parent commits with INSERTIONS 457, 382, 21, 4, 391 and 120, each under 500; `git ls-files .remedy-wt` 0; `*.zip` 0; `git worktree list` 1 line. Reflog scoped to THIS ROUND's 6 entries (HEAD@{0}..HEAD@{5}; HEAD@{6} is the base handback), read by the OPERATION PREFIX before the first colon of `git reflog --format=%gs`: all 6 prefixes are `commit`, so amend 0, rebase 0, cherry 0.
G8 PASS — word-bounded `[0-9a-f]{7,40}` over the committed C0a blob: 10 occurrences, 7 distinct tokens, `git cat-file -t` exit 0 on every one — 6ae136b7 is a blob, and 49c50d05, 6325ac2f, c8dbf20e, e73da3ef, e73da3efd3ea0b58d1570beecaa4db34be7f2fc1 and f2a1a518 are commits. THE FAILING SET IS EMPTY, exactly as this block predicted; the 64-char sha256 digests it also carries are not matched by the pattern.
G9 (a) RED, ordered as a probe — in `.remedy-wt/g9a` at ce462ecc the blocked-count seed set was forced EMPTY unconditionally, all else intact: `1 failed, 24 passed`, real exit 1, the one failing node id `tests/orchestration/test_decision_inbox.py::test_blocked_count_equals_dag_blocked_downstream` (`assert 0 == 3`). Nothing was strengthened to make it fail.
G9 (b) RED, ordered as a probe — in `.remedy-wt/g9b` the `handlers` key `decisions` was renamed `decisionz`, the builder intact: `2 failed, 2 passed`, real exit 1, the failing node ids `tests/ui_server/test_decisions_endpoint.py::TestDecisionsEndpoint::test_decisions_endpoint_returns_the_inbox_document` and `::test_decision_card_carries_age_and_blocked_count` (404 where 200 is asserted).
G10 PASS — `git worktree list` 1 line immediately BEFORE the first pytest; seven suites run SERIALLY in the primary checkout at the C4 tree, never two pytest processes alive, REAL exit code 0 for each: test_decision_inbox 25, test_decisions_endpoint 4, `tests/ui_server/` 474, test_test_runner 52, test_resource_safety 21, test_integrity_gate 16, test_golden_path 42. THE ARITHMETIC: `tests/ui_server/` 470 → 474 = 470 + the 4 tests S9 adds, and the other four are cell for cell the readings at e73da3ef, so there is no other difference to account for. `python3 -m ruff check` over the four change-set paths under `packages/` and `tests/` with the repository's OWN configuration: real exit 0, "All checks passed!". `ui_server.py` pre-existed, so its rule-code MULTISET was compared: EMPTY at base e73da3ef and EMPTY at C4, EQUAL.
G11 — `git push origin feature/f031-decision-inbox`, run after C5. Its outcome is not a value of any file this round writes; the reviewer measures the pushed tips and records them in the R7 entry of the ledger. Reported in the round's final message.

## Authored-text proofs
3 slices applied, each extracted PROGRAMMATICALLY from the COMMITTED C0a blob by its marker LINES and never retyped: PLANF031R7 → `.agent/plan.md` (byte-equal, G4); GATE6 and RECUR471 → `.agent/live_review.md` (one whole-file equality, G5). Disk-to-disk: `.agent/authored/f031-r7.md` equals the pre-C0a scratch original and equals `.agent/last_block.md`, all at sha256 9b1a517f…cff2d69 over 33656 bytes and 457 lines.

## Deviations & assumptions
The commit sequence C0a, C0b, C1, C2, C3, C4, C5 was followed exactly — no extra commit, none dropped, no reordering. No contradiction was found inside this block; constraint 8 states the append shape once and every gate names that paragraph, which is the R-0471 counter-measure this round registers, applied to itself.
DECLARED 1 — C3 and C4 carry NO authored bytes: that code is mine, written to S1-S9 under the AGENTS.md self-review loop. Two naming rulings the block makes are visible in it: the test file is `tests/orchestration/test_decision_inbox.py` (S8, the AGENTS.md naming convention over the feature file's `tests/ui_contract/…`), and the module takes no project argument, recorded as a deliberate absence in its docstring (S6).
DECLARED 2 — the G9 (b) mutation run triggered the UI auto-build (`[remedy-ui] auto-build (dist missing)…`) INSIDE the disposable worktree `.remedy-wt/g9b`. It wrote nothing into the primary checkout: that worktree was removed by its exact path and `git status --porcelain` is 0 lines here.
ASSUMPTION 1 — session scratch for slice extraction and the gate script lives at `.remedy-wt/r7x/`, which is gitignored: `git ls-files .remedy-wt` is 0 (G7). `.remedy-wt/dry` was not touched.
ASSUMPTION 2 — the newline-INCLUDED convention, declared at G4 as the block requires, is the convention used for every slice equality this round.
FINDINGS, with the rule and the commit DECISION F009 D10 requires: by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the open set is 238, measured at 85daf94d. THIS ROUND MINTED NO ID (G6). The findings THIS FEATURE MUST STILL ACT ON, a narrower set never called "open", are R-0403, R-0413, R-0431, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678 and R-0679; R-0495 and R-0574 are the two Highs, from F085 and F086.
HANDBACK CAP, derived not quoted: constraint 3 fixes 7 commits, and 7 is more than 5, so the AGENTS.md `### handoff.md` tier is 100 lines. This file is under that tier, so no DECISION D15 overage line is owed; no mandated section was dropped, and NO token cap is claimed — that cap was withdrawn by DECISION F255 D6.

## Next
1. Phase 1 rule 1 first: re-read `.agent/STOP` from disk.
2. NO pull request exists for this branch, and none should be created yet.
3. R8 records the R7 verdict, which by DECISION F085 D9 no artefact of this round can carry, and plans T002: the cards, the generic options renderer, ordering and filtering, and the badge — where DECISION F031 D2 binds.
