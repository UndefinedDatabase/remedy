# Handback — F022 R5 (record the R4 verdict · split T001 · rule DECISION F022 D2 · build the tick emission)

Round base `94694b3f` · branch `feature/f022-live-cost-ticker` · the first F022 round to ship production code · max registered id `R-0669` at base AND at C2, no id minted, no `Done:` and no `Landed:` line written.

Fortschritt: ~15 % (T001 halb — R5 baut die Emission, R6 den Umschlag · T002
             offen · T003 offen; ab hier entsteht Produktionscode, der Bauplan
             steht seit R4 fest) — Schaetzung

## Range

Review of `94694b3f..HEAD`. C5 writes this file, so its own readings are owed to the next round's ledger entry.

## Commits

### d43b0a3b chore(agent): save the F022 R5 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f022-r5.md | +366/-0 | C0a — the block saved byte for byte |
### d63cab91 chore(agent): mirror the F022 R5 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +336/-276 | C0b — written FROM the committed C0a blob |
### ec0916aa docs(state): advance the F022 plan to R5
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +14/-12 | C1 — PLANF022R5, current step R5, next steps R6..R9 |
### 0c8d9712 docs(state): record the F022 R4 verdict and split T001 in the round map
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +7/-3 | C2 — the STEPSF022R5 map pair rewritten, GATE4 appended |
### 7fa31892 docs(state): rule the F022 tick writer as DECISION F022 D2
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +18/-0 | C3 — DEC2 appended, 9 units |
### 7f6033ca feat(orchestration): emit one budget tick per safe-point evaluation
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/safe_points.py | +91/-0 | C4 — `_emit_budget_tick` above the exhaustion test, `_budget_tick_payload`, `BUDGET_TICK_RUN_ID` |
| apps/ui/src/api/humanizeCatalog.ts | +1/-0 | C4 — the `budget.tick` key, pinned equal to the Python vocabulary |
| tests/orchestration/test_budget_tick.py | +333/-0 | C4 — new file, T1-T10 |
### C5 (grouped, R-0149 self-reference exception)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-referential | C5 — this handback; a handoff cannot table the commit that writes it |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a `.agent/authored/f022-r5.md` | done | |
| C0b `.agent/last_block.md` | done | |
| C1 `.agent/plan.md` | done | |
| C2 `.agent/live_review.md` | done | |
| C3 `.agent/decisions.md` | done | |
| C4 emission + catalog key + backend tests | done | one commit, not split |
| C5 `.agent/handoff.md` | done | |

## External actions

`git worktree add .remedy-wt/f022r5-wt 7f6033ca --detach` then `git worktree remove .remedy-wt/f022r5-wt` — the G5 negative control and the G9/G10/G11 red proofs; `git worktree list` back to 1 line.
`gh pr list --state open --json number,headRefName` → `[]`. No `gh pr create`, no `gh pr merge`, no merge of any kind.
`git push` at the end of the round.

## Verification

Transcripts are in the round report (R-0582), one line per gate here. G1-G14 ran after C4 and before C5, so this file can quote all of them.
- G1 PASS — `.agent/STOP` absent, read from disk before C0a and again before C5; branch `feature/f022-live-cost-ticker`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3 and C4.
- G2 PASS — sha256 `657abe6c545fe74321dd533fc0bd919f942a1111e3c1df004b954964b9b70e88` over 33039 bytes / 366 lines, EQUAL at all four readings — the reviewer's file `.remedy-wt/f022-r5.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` on disk — and equal to the delegation's fifth reading.
- G3 PASS — the extractor over the COMMITTED C0a blob found the slices by their marker LINES and printed 5 slices over 67 CONTENT lines, with TOTAL 366 and PROSE 299. Constraint 9's numerals reproduce exactly: 366 ≤ 490 (D6), 299 ≤ 400 (D5). No slice contains a marker line.
- G4 PASS — `.agent/plan.md` at `ec0916aa` is byte-equal to PLANF022R5 plus exactly one newline (2234 bytes against the bare slice's 2233); NEGATIVE CONTROL against the BARE slice is FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 41 ≤ 50.
- G5 PASS — RECONSTRUCTION: the round-base blob with the FROM string replaced exactly once by the TO string, then one newline + GATE4 + one newline, is BYTE-EQUAL to `0c8d9712:.agent/live_review.md` — both 497163 bytes, both sha256 `17842f0ae2d9658ab2524084af288eb31eeae1299662748d56ed35a67122425c`. FROM counts 1 → 0 and TO 0 → 1, base → C2. NEGATIVE CONTROL inside `.remedy-wt/f022r5-wt`: flipping offset 491769 from `G` to `H` at unchanged length makes the equality FAIL. Worktree removed, `git worktree list` 1 line.
- G6 PASS — the round-base blob of `.agent/decisions.md` is a byte-exact PREFIX at C3; the remainder is 5662 bytes = 1 + DEC2's 5660 + 1. INDEPENDENT reader: a blank-line splitter reads 1261 units at base and 1270 at C3, with the LAST unit at C3 equal to DEC2's own last paragraph. Lines beginning `## DECISION F022 D2 ` count 1.
- G7 PASS — base → C2: `^- R-\d+ — ` 230 → 230, all DISTINCT at both points; MAXIMUM id `R-0669` → `R-0669`; `^Done: R-` 0 → 0; `^Landed: ` 0 → 0; `^Gate: R` 4 → 5 with distinct keys 4 → 5, gaining `Gate: R4` beside `Gate: R1`, `Gate: R2`, `Gate: R3` and `Gate: R41`; ids ADDED the EMPTY SET, ids REMOVED the EMPTY SET. Every round-base figure the block states reproduced under my own measurement.
- G8 PASS — `^## Steps$` occurs exactly 1× in `.agent/live_review.md` at C2. Arrow `→` counts base → C2: 29 → 30 in `.agent/live_review.md`, 0 → 0 in `.agent/plan.md`.
- G9 PASS — `python3 -m ruff check packages/orchestration/safe_points.py tests/orchestration/test_budget_tick.py` at C4, repository configuration and NOT `--isolated`: exit 0, "All checks passed!". RED CONTROL in the disposable worktree, a one-line file whose only content is `import json`: exit 1, `F401 imported but unused`. Deleted by exact path; worktree `git status --porcelain` 0.
- G10 PASS — `python3 -m pytest tests/ui_contracts/test_humanize_catalog.py -q` at C4: exit 0, 9 passed. I measure 84 catalog keys and a derived vocabulary of 84, sets EQUAL, against the reviewer's 83 at the round base — `budget.tick` is the single addition and the only kind whose name begins `budget`. RED CONTROL: with that one catalog line deleted in the worktree the suite is exit 1, 1 failed / 8 passed, at `TestCatalogCoversTheStreamVocabulary::test_catalog_keys_equal_the_static_stream_vocabulary`, naming `budget.tick` as emitted but not catalogued. Worktree restored with `git checkout --`.
- G11 PASS — `python3 -m pytest tests/orchestration/test_budget_tick.py -q` at C4: exit 0, 10 passed. Node ids, all under `tests/orchestration/test_budget_tick.py`: `TestTickPayload::test_priced_job_with_both_limits_emits_one_full_tick` (T1), `::test_a_limitless_money_side_leaves_the_keys_out` (T2), `::test_no_budgets_and_no_counters_emit_nothing` (T3), `::test_unmeasured_calls_make_the_token_basis_a_lower_bound` (T4), `::test_an_unpriced_call_makes_the_cost_basis_a_lower_bound` (T5); `TestTickCadenceAndShape::test_a_pingpong_shaped_job_id_still_emits` (T6), `::test_an_exhausted_budget_still_ticks_and_still_stops` (T7), `::test_three_calls_write_three_ticks_into_one_file` (T8), `::test_a_failing_write_never_changes_the_decision` (T9); `TestPayloadKeysNeverCollide::test_no_payload_key_is_a_named_parameter_of_the_writer` (T10). RED-PROOF (i), the emission routed through `timeline.append_run_event`: the file goes RED, 2 failed / 8 passed, and the failures are T6 and T8 — T6 is among them, as ordered. RED-PROOF (ii), the emission moved inside `if evaluation.exhausted:`: the file goes RED, 9 failed / 1 passed, and T7 is among the failures, as ordered. Each mutation ran in `.remedy-wt/f022r5-wt` and was reverted before the next; the primary checkout was never mutated.
- G12 PASS — serially in the PRIMARY checkout at C4, each exit 0: `tests/orchestration/test_safe_points.py` 78, `test_budget_stop_integration.py` 39, `test_job_budgets.py` 135, `test_long_run_executor.py` 74, `test_predictive_budget.py` 75, `tests/ui_server/test_sse_stream.py` 66 — all six equal to the block's round-base references. Never two pytest processes at once.
- G13 PASS — the four state readers, serially at C4, each exit 0: `tests/ui_server/` 439, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16 — 528 passed in total, matching the block's 528.
- G14 PASS — the canary `python3 -m pytest tests/cli/test_golden_path.py -q` at C4: exit 0, 42 passed. Matches the block's 42.
- G15 PASS — 6 commits before C5, every one single-parent; insertions 366, 336, 14, 7, 18 and 425, each under the 500 cap; `git show --numstat` agrees cell by cell with the `## Commits` tables above; the range path union is 8, and against the Change set the difference is `.agent/handoff.md` in one direction (C5 has not landed yet) and the EMPTY SET in the other; lines beginning `<<<SLICE ` or `<<<END ` count 0 in all six files a slice landed in; `git ls-files .remedy-wt` 0; `git worktree list` 1 line; 6 reflog rows this round, amend 0, rebase 0, cherry 0.
- G16 PASS — `gh pr list --state open --json number,headRefName` printed verbatim: `[]`. No PR created, nothing merged.
- G17 PASS — CHECKED, and no sentence C1-C4 landed has gone stale at C4. Re-measured: the plan's branch point is `git merge-base HEAD main` = `c34ef32b`; its "two High findings … R-0495 and R-0574" is the severity-anchored `^- R-\d+ — High` set exactly; its R6 risk resolves — `_safe_event_summary` appears 6× in `tests/ui_server/test_sse_stream.py` and that file names a golden 8×; GATE4's transport claim re-measures (`43558c78:.agent/authored/f022-r4.md` is sha256 `3bd226db…` over 31028 bytes / 306 lines) and its `## DECISION F022 D1 ` count is 1; all ten of DEC2's file:line pointers resolve at C4 with the two granularity readings named under Deviations; my own C4 docstring's transcription of `RunLogWriter.log`'s named parameters re-derives from the signature as `event, task_id, artifact_id, provider, role, model, outcome, message`, and T10 pins it. No residual to report.

## Authored-text proofs

All five slices were extracted PROGRAMMATICALLY by their marker LINES out of the COMMITTED C0a blob `d43b0a3b:.agent/authored/f022-r5.md`, never retyped and never rewrapped. PLANF022R5 → `.agent/plan.md` byte-equal plus one newline with the bare-slice control DIFFERING; STEPSF022R5-FROM/-TO → the C2 file reconstructs BYTE-EQUAL from the base blob by one replacement, and the FROM-0×/TO-1× proof holds; GATE4 → the C2 remainder is exactly one newline + GATE4 + one newline; DEC2 → the C3 remainder is exactly one newline + DEC2 + one newline. No slice was edited.

## Deviations & assumptions

- `wc -l` of this file is 99, within the ≤100 bound the >5-commit case allows (7 commits). No DECISION D15 overage is claimed.
- NO departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5 exactly as the Bundle lists — no extra commit, none dropped, none reordered. C4 was NOT split.
- T7 measures MORE than its sentence describes, deliberately. "An EXHAUSTED budget still emits its tick" pins nothing about the emission SITE on its own: a test exercising only the exhausted arm stays GREEN under G11's mutation (ii), because that mutation still emits when exhausted. T7 therefore asserts BOTH arms in one test — the evaluation under the limit ticks, the one over it ticks too, and the second call's `should_stop`, reason and source are unchanged — which is what makes "still" measurable and what makes T7 fail under (ii) as G11 requires.
- G17 granularity, reported and NOT repaired (constraint 1): two of DEC2's ten pointers are function-level rather than statement-level. `packages/orchestration/ui_server.py:3619` is the `append_run_event(` call inside `_emit_command_accepted_event`, whose `def` is at `:3593`; `packages/orchestration/pingpong_job.py:2887` is the `def _append_job_stopped_event` line, whose `RunLogWriter(` construction is at `:2903`. Both read identically at `94694b3f` and at C4, so neither went stale this round and neither claim is false — the line named is the function that does the thing, not the statement.
- TOOLING, not scope: this session's bash guard rejects `$?`, loops and command lines carrying the literal slice-marker prefix, so every measurement was routed through python scripts under the gitignored `.remedy-wt/f022r5-scratch/`. `git ls-files .remedy-wt` reads 0.

## Next

Reviewer verdict on R5; then R6 builds the second half of T001 — widening `_safe_event_summary` CONDITIONALLY by event kind so the tick's `metadata` reaches a client without turning the exact key-set pin or the golden byte stream in `tests/ui_server/test_sse_stream.py` red.
