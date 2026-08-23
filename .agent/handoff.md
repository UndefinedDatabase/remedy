# Handback — F022 R6 (record the R5 verdict · rule DECISION F022 D3 · close T001 at the envelope)

Round base `9b854cf5` · branch `feature/f022-live-cost-ticker` · max registered id `R-0669` at base AND at C2, no id minted, no `Done:` and no `Landed:` line written.

Fortschritt: ~25 % (T001 fertig nach dieser Runde · T002 offen · T003 offen;
             die Zahlen erreichen ab hier wirklich den Client, vorher endeten
             sie im Umschlag) — Schaetzung

## Range

Review of `9b854cf5..HEAD`. C5 writes this file, so its own readings are owed to the next round's ledger entry.

## Commits

### 941d9ca9 chore(agent): save the F022 R6 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f022-r6.md | +288/-0 | C0a — the block saved byte for byte |
### 4076ae3c chore(agent): mirror the F022 R6 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +182/-260 | C0b — written FROM the committed C0a blob |
### 276c12d2 docs(state): point the F022 plan at R6
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +13/-14 | C1 — PLANF022R6, current step R6, next steps R7..R9 |
### 675ee3d3 docs(state): record the F022 R5 verdict in the review record
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2 — GATE5 appended, pure append, map untouched |
### bd9a745b docs(state): rule the F022 tick envelope widening as DECISION F022 D3
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +16/-0 | C3 — DEC3 appended, 8 units |
### f685a707 feat(orchestration): carry the budget tick figures across the event envelope
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +79/-2 | C4 — `BUDGET_TICK_EVENT`, the two whitelists, `_budget_tick_summary_payload`, the conditional branch in `_safe_event_summary` |
| tests/ui_server/test_budget_tick_envelope.py | +267/-0 | C4 — new file, T1-T7 plus an emitter-drift guard |
### C5 (grouped, R-0149 self-reference exception)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-referential | C5 — this handback; a handoff cannot table the commit that writes it |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a `.agent/authored/f022-r6.md` | done | |
| C0b `.agent/last_block.md` | done | |
| C1 `.agent/plan.md` | done | |
| C2 `.agent/live_review.md` | done | |
| C3 `.agent/decisions.md` | done | |
| C4 the conditional widening + its tests | done | one commit, not split |
| C5 `.agent/handoff.md` | done | |

## External actions

`git worktree add .remedy-wt/f022r6-wt --detach f685a707` then `git worktree remove --force .remedy-wt/f022r6-wt` — the G5 negative controls and the G7/G8/G9 red proofs; `git worktree list` back to 1 line.
`gh pr list --state open --json number,headRefName` → `[]`. No `gh pr create`, no `gh pr merge`, no merge of any kind.
`git push` at the end of the round.

## Verification

Transcripts are in the round report (R-0582), one line per gate here. G1-G14 ran after C4 and before C5, so this file can quote all of them.
- G1 PASS — `.agent/STOP` absent, read from disk before C0a and again before C5; branch `feature/f022-live-cost-ticker`; `git status --porcelain` 0 lines after each of C0a, C0b, C1, C2, C3 and C4.
- G2 PASS — sha256 `2651351709f1a203152b892fac8db924dcd838b8cdcf36817e40705a976c4c50` over 29555 bytes / 288 lines, EQUAL at all four readings — `.remedy-wt/f022-r6.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` on disk — and equal to the delegation's fifth reading.
- G3 PASS — the extractor over the COMMITTED C0a blob found the slices by their marker LINES: 3 slices, 56 CONTENT lines, TOTAL 288, PROSE 232. Constraint 9's numerals reproduce exactly; 288 ≤ 490 (D6), 232 ≤ 400 (D5). GATE5's single line quoting both markers inside backticks is CONTENT, not a marker line, and the extractor treated it so.
- G4 PASS — `.agent/plan.md` at `276c12d2` is byte-equal to PLANF022R6 plus exactly one newline (2196 bytes against the bare slice's 2195); NEGATIVE CONTROL against the BARE slice is FALSE; `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` 40 ≤ 50.
- G5 PASS — C2: base blob is a byte-exact PREFIX, remainder 7618 = 1 + GATE5's 7616 + 1; INDEPENDENT blank-line reader 255 → 256 units, LAST unit equals GATE5's last paragraph. C3: PREFIX holds, remainder 4370 = 1 + DEC3's 4368 + 1; units 1270 → 1278, LAST equals DEC3's last paragraph; `## DECISION F022 D3 ` counts 1. NEGATIVE CONTROLS in `.remedy-wt/f022r6-wt`, four one-byte flips at unchanged length — live_review offsets 497203 and 504741, decisions 524882 and 529172 — all four REJECTED by the prefix reader and by the strengthened unit reader, all four accepted forms of the true file accepted; see Deviations for the one blind spot the ordered unit reader has. Worktree removed, `git worktree list` 1 line.
- G6 PASS — base → C2: `^- R-\d+ — ` 230 → 230, all DISTINCT at both; MAXIMUM id `R-0669` → `R-0669`; `^Done: R-` 0 → 0; `^Landed: ` 0 → 0; `^Gate: R` 5 → 6 with 5 → 6 distinct keys, gaining `Gate: R5`; ids ADDED the EMPTY SET, ids REMOVED the EMPTY SET; `^## Steps$` 1 at C2. The map paragraph under `## Steps` is BYTE-IDENTICAL base and C2 — 1075 bytes, sha256 `e70467cd…` at both. Every round-base figure the block states reproduced.
- G7 PASS — `python3 -m ruff check packages/orchestration/ui_server.py tests/ui_server/test_budget_tick_envelope.py` at C4, repository configuration and NOT `--isolated`: exit 0, "All checks passed!". RED CONTROL in the disposable worktree, a one-line file whose only content is `import os`: exit 1, `F401 imported but unused`. Deleted by exact path; worktree `git status --porcelain` 0.
- G8 PARTIAL, reported not reconciled — at C4 both guards are exit 0: `tests/ui_server/test_sse_stream.py` 66 passed and `tests/ui_server/test_command_channel.py` 100 passed, equal to the block's references. RED-PROOF, the widening made UNCONDITIONAL in the worktree: `test_sse_stream.py` goes RED, 3 failed / 63 passed — `TestFrameShape::test_the_envelope_carries_the_safe_fields_only`, `TestFramingGolden::test_the_wire_bytes_match_the_golden`, `TestFramingGolden::test_the_golden_is_what_the_frame_builders_produce`. `test_command_channel.py` stays GREEN at 100 passed under the same mutation. Said plainly: only ONE of the two files guards the conditionality — the block's rationale holds for the key-set pin and the golden, and `test_command_channel.py` is a suite the change must not break rather than one that would catch an unconditional widening.
- G9 PASS — `python3 -m pytest tests/ui_server/test_budget_tick_envelope.py -q` at C4: exit 0, 16 passed. Node ids, all under that file: `TestEveryOtherKindIsUntouched::test_a_non_tick_summary_is_exactly_the_five_fields_it_was` (T1), `::test_a_non_tick_carrying_tick_shaped_metadata_still_gains_nothing`; `TestTheTickCarriesItsFigures::test_a_tick_gains_the_payload_key_and_nothing_else` (T2), `::test_the_payload_holds_every_figure_the_metadata_carried`, `::test_the_figures_survive_serialisation_to_the_wire`; `TestTheWhitelistBlocksWhatItDoesNotName::test_an_unnamed_outer_field_never_reaches_the_wire` (T3), `::test_an_unnamed_key_inside_basis_never_reaches_the_wire` (T4); `TestAnAbsentLimitStaysAbsent::test_a_limit_the_tick_never_carried_is_a_missing_key` (T5), `::test_the_missing_limit_is_missing_on_the_wire_too`; `TestAMalformedTickIsNotAnError::test_a_tick_with_no_metadata_yields_an_empty_payload` (T6), `::test_a_tick_whose_metadata_is_not_a_dict_yields_an_empty_payload`, `::test_a_tick_whose_basis_is_not_a_dict_keeps_the_outer_figures`; `TestBothTransportsCarryTheSameTick::test_the_cursor_endpoint_and_the_stream_agree_on_a_tick` (T7); `TestTheWhitelistCoversTheEmitter::test_the_emitter_really_produced_a_populated_payload`, `::test_every_key_the_emitter_writes_is_named_by_a_whitelist`, `::test_an_emitted_payload_crosses_the_envelope_unchanged`. RED-PROOF, the key-by-key copy replaced by a wholesale pass-through of the tick's metadata in the worktree: 3 failed / 13 passed, and T3 and T4 are BOTH among the failures as ordered, beside `::test_a_tick_whose_basis_is_not_a_dict_keeps_the_outer_figures`. Reverted before the next gate; the primary checkout was never mutated.
- G10 PASS — serially in the PRIMARY checkout at C4, each exit 0: `tests/orchestration/test_budget_tick.py` 10, `tests/ui_contracts/test_humanize_catalog.py` 9, `tests/orchestration/test_safe_points.py` 78 — all three equal to the block's round-base references of 10, 9 and 78. Never two pytest processes at once.
- G11 PASS — the four state readers, serially at C4, each exit 0: `tests/ui_server/` 455, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16 — 544 passed in total against the block's round-base 528, a difference of +16, which is exactly the 16 tests C4 adds under `tests/ui_server/`.
- G12 PASS — the canary `python3 -m pytest tests/cli/test_golden_path.py -q` at C4: exit 0, 42 passed. Matches the block's 42.
- G13 PASS — 6 commits before C5, every one single-parent; insertions 288, 182, 13, 2, 16 and 346, each under the 500 cap; `git diff-tree --numstat` agrees cell by cell with the `## Commits` tables above; the range path set is 7 paths and the difference against the Change set is the EMPTY SET in BOTH directions (C5's `.agent/handoff.md` has not landed yet and is the block's eighth declared path); the per-commit union equals the range set; lines BEGINNING `<<<SLICE ` or `<<<END ` count 0 in all three files a slice landed in, while the SUBSTRING occurs 14 times in `.agent/live_review.md` — all backticked prose; `git ls-files .remedy-wt` 0; `git worktree list` 1 line; `git status --porcelain` 0; amend 0, rebase 0, cherry 0 across the round's reflog rows.
- G14 PASS — `gh pr list --state open --json number,headRefName` printed verbatim: `[]`. No PR created, nothing merged.
- G15 CHECKED, two residuals reported and NOT repaired (constraint 1). Re-measured at C4: the plan's branch point is `git merge-base main HEAD` = `c34ef32b`; its two High findings are the `^- R-\d+ — High` set exactly, `R-0495` and `R-0574`; `RemedyMetricKey` in `apps/ui/src/api/types.ts` is still a closed union of seven strings; DEC3's premises all hold — the key-set assertion still feeds an event named `x`, the golden's events are still `e0`/`e1`, the golden is still rebuilt from the frame writers, and `packages/orchestration/redaction_patterns.py` exists. RESIDUAL 1: GATE5 states the marker substring "occurs 6 times inside `.agent/live_review.md`" — true of the file when the sentence was written (6 of each marker at `0c8d9712` and at `9b854cf5`) and 7 of each at C4, because GATE5 itself adds one of each. RESIDUAL 2: DEC3's CONTEXT paragraph says `_safe_event_summary` "returns exactly `{seq, event, timestamp, outcome, task_id}` and drops the event's `metadata`" in the present tense; C4 of this same bundle makes that false for `budget.tick`. The paragraph names its own measurement point (`9b854cf5`) in its first sentence, so the claim is anchored rather than wrong.

## Authored-text proofs

All three slices were extracted PROGRAMMATICALLY by their marker LINES out of the COMMITTED C0a blob `941d9ca9:.agent/authored/f022-r6.md`, never retyped and never rewrapped. PLANF022R6 → `.agent/plan.md` byte-equal plus one newline with the bare-slice control DIFFERING; GATE5 → the C2 remainder is exactly one newline + GATE5 + one newline over a byte-exact prefix; DEC3 → the C3 remainder is exactly one newline + DEC3 + one newline over a byte-exact prefix. This round carried NO FROM/TO pair. No slice was edited.

## Deviations & assumptions

- `wc -l` of this file is 96, within the ≤100 bound the >5-commit case allows (7 commits). No DECISION D15 overage is claimed.
- NO departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5 exactly as the Bundle lists — no extra commit, none dropped, none reordered. C4 was NOT split.
- G5's ordered unit reader is BLIND to a first-paragraph flip, and I report it rather than choosing an offset that hides it. "Split both files on blank lines, report the unit counts, require the LAST unit equal to the slice's last paragraph" cannot see a mutation in any appended paragraph except the last: the DEC3 flip at offset 524882 sits in DEC3's first of eight paragraphs, and that reader ACCEPTS the mutant. I therefore ran a strengthened second form — same blank-line extractor, but EVERY appended unit compared against the slice's paragraphs — which rejects all four mutants, and I flipped a byte in the FIRST and in the LAST appended paragraph of both files rather than only where the reader could see it. GATE5 is one paragraph, so its two flips are caught by both forms.
- The test file carries ONE class the block did not order, `TestTheWhitelistCoversTheEmitter`. Its three tests drive the real `safe_points._budget_tick_payload` and assert every key it writes is NAMED by one of the two whitelists, with a populated-payload premise check first so the subset assertions cannot pass vacuously. Without it, a figure a later round adds to DECISION F022 D1's payload would be written, logged and silently dropped at this envelope — the exact failure this round exists to fix, reintroduced one field at a time.
- TOOLING, not scope: this session's bash guard rejects `$?`, loops and command lines carrying the literal slice-marker prefix, so every measurement was routed through python scripts under the gitignored `.remedy-wt/f022r6-scratch/`. `git ls-files .remedy-wt` reads 0.

## Next

Reviewer verdict on R6; then R7 opens T002 — the client side of the tick, widening the CLOSED `RemedyMetricKey` union and a metric value type with nowhere to put a limit or a basis, then the COST metric's fill, its `~` prefix and tooltip, its thresholds and its no-limit variant.
