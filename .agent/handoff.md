# Handoff — F115 Prompt breakdown & cost report · Round 2

Branch: feature/f115-prompt-cost-report. Last reviewed SHA a414c0c6 (R1 PASS).
No PR this round (per block). Open findings: 2 (R-0320 Low carried from F111,
R-0321 Low inventory miscount). Next free finding ID: R-0322.

## Item status

| Item | Status   | Reason |
|------|----------|--------|
| C1a  | done     | |
| C1b  | done     | |
| C2   | done     | |
| C3   | done     | |
| C4   | done     | |
| C5   | deviated | gate (e1)'s `segment_manifest_chars == sum(rows.chars)` clause is arithmetically impossible; see Deviation below |
| C6   | done     | |

## Commits

| SHA | Subject | Insertions |
|-----|---------|-----------|
| 37388ba9 | chore(f115): save the R2 step block verbatim | 264 |
| 5cdb7729 | chore(f115): mirror the R2 block into last_block | 220 |
| da225248 | chore(f115): register R-0321 from the R1 gate | 14 |
| e8961e4a | docs(f115): correct the manifest premise and record DECISION D1 | 43 |
| e65152b3 | feat(f115): give the builder trace entry its segment manifest | 6 |
| 2487eeb7 | test(f115): pin the builder trace manifest and its wiring | 65 |
| (C6) | chore(f115): refresh the plan and write the R2 handoff | see below |

## Changed files

| Path | Commit |
|------|--------|
| .agent/authored/f115-r2-1.md | 37388ba9 (new) |
| .agent/last_block.md | 5cdb7729 |
| .agent/live_review.md | da225248 |
| docs/roadmap/features/T2_F115.md | e8961e4a |
| packages/orchestration/pingpong_loop.py | e65152b3 |
| tests/orchestration/test_prompt_trace.py | 2487eeb7 |
| .agent/plan.md | C6 |
| .agent/handoff.md | C6 |

## Gates (measured)

- a. `cmp` exit 0. sha256 both
  5862cbeb20d1336d9cc02f07cc6d99bb222502dfc171bdec07dd1c5330d751ee.
  `wc -lc` authored: 264 16356.
- b. `^- R-0321`: 1 · `^- R-0`: 2 · `^Done:`: 0.
- c. `DECISION F115 D1`: 2 (was 0 before the round).
  `pytest tests/docs/ -q`: 294 passed in 0.30s, exit 0.
- d. `pytest test_builder_prompt_golden.py test_reviewer_prompt_golden.py
  test_builder_repair_loop.py -q`: 51 passed in 4.65s, exit 0. Same-object
  proof, three lines of the C4 diff: `builder_composed = compose_builder_prompt(`
  · `builder_prompt = builder_composed.text` · `composed_prompt=builder_composed,`.
  One composition, one `.text`, and that same `builder_prompt` feeds
  `builder_prompt_chars` (:2822/:2824), `prompt_text=` (:2829) and
  `builder_provider.build(builder_prompt, …)` (:2850).
- e. Added `tests/orchestration/test_prompt_trace.py::TestSegmentManifest::
  test_the_builder_composition_traces_a_real_segment_manifest` (e1) and
  `::test_the_builder_call_site_hands_its_composition_down` (e2). Both PASSED;
  whole file 44 passed in 0.24s, exit 0.
- f. RED-PROOF in disposable worktree `.remedy-wt/f115-redproof` (C4 reverted):
  e2 FAILED (`assert 0 == 1` on the `builder_composed = compose_builder_prompt(`
  count) — the guard guards. e1 PASSED unchanged, which is exactly why e2 is
  required. Worktree removed; `git worktree list` shows only
  `/home/decodeux/Repos/remedy 2487eeb7 [feature/f115-prompt-cost-report]`.
- g. `pytest tests/cli/test_golden_path.py -q`: 42 passed in 19.62s, exit 0.
- h. `wc -l .agent/plan.md`: 41.
- i. `git status --porcelain` empty. `git diff --name-only 0d6c97aa..HEAD`
  lists 13 paths = the nine R1 paths + the four new ones, nothing else.
  `git rev-list --left-right --count origin/…...HEAD`: 0 0.
- j. REPORT ONLY, reviewer site NOT wired. `_build_reviewer_prompt(...)`
  :2987-3001; `reviewer_prompt_chars` :3004; `_reviewer_effective_prompt(
  reviewer_prompt)` :3008 is called with ONE argument, so `hint` takes its
  default `""` on the first attempt — the hint IS empty there. But the traced
  text still is not the composed text: `_reviewer_effective_prompt` :2088-2103
  returns `native_schema_prompt(base, hint)` in structured mode, and
  `structured_outputs.py:65-73` appends `"\n\n" + NATIVE_SCHEMA_INSTRUCTION`
  (:62) UNCONDITIONALLY. In legacy mode it returns `base` unchanged. The only
  non-empty hint comes from the parse-retry path: `_parse_hint =
  getattr(reviewer_out, "parse_hint", "")` :3098, used at
  `_reviewer_effective_prompt(reviewer_prompt, _parse_hint)` :3102, traced
  separately via `_rev_trace(retry_prompt, "parse-retry", …)` :3121. So R3 must
  decide what `composed_prompt` means when the sent text is base + tail (+ hint):
  the F105 D3 precedent is that the manifest covers the composed BASE only and
  `segment_manifest_chars < prompt_chars` records the gap.

## Next expected action

Planner writes the R3 block: the reviewer site under the gate (j) decision,
then the planner site in `apps/cli/commands/job.py:236`.

Deviations, declared: 114 lines, over the 60-line cap (AGENTS.md DECISION D15).
Cause is mandated content only — the seven-row item-status table, the
seven-row commit table, the eight-row changed-files table, and the ten gate
results a-j required as REAL measured values, of which (f) and (j) are
themselves multi-part. No section was dropped to meet the cap.

C5 deviation, stated: gate (e1) asks that `segment_manifest_chars` equal the
SUM of the manifest rows' `chars`. It cannot. `build_trace_entry` sets it to
`len(composed_prompt.text)` (`prompt_trace.py:157-158`, and the dataclass
comment at :79-83 says so), while `compose_prompt_segments` joins segments
with the two-character `PROMPT_SEGMENT_DELIMITER`, so the composed text is
2*(N-1) characters longer than the sum of its rows. Measured on the e1 fixture:
6 rows, `len(text)` 793, sum of `chars` 783, gap 10 = 2*5. The whole repo
already pins the `len(composed.text)` reading (`test_prompt_trace.py:230`,
`test_mission_compiler.py:1117`). e1 therefore asserts both true identities —
`segment_manifest_chars == len(composed.text)` AND `== sum(chars) +
boundaries*len(PROMPT_SEGMENT_DELIMITER)` — and the test docstring names the
deviation. Nothing outside the block's path list was touched to achieve it;
`prompt_trace.py` was NOT edited.

Fortschritt: 15 % (R1 Inventar ✅ · T001a läuft · T001 · T002 · T003 offen) — Schätzung
