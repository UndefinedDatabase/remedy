# Plan — F256 Diff viewer completion

Branch: feature/f256-diff-viewer-completion, cut from `main` at `0e8ab5b4`.
F256 was claimed by Rule A5 as the first unchecked line of Package 1 in
`docs/roadmap/STATUS.md`.

## Goal
Finish the rendered diff viewer F037 shipped: highlighting actually rendered
rather than only modelled, the 10k-line budget measured and recorded, and the
file sidebar's visual treatment ruled by a named authority.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| claim F256 and retarget the state | done | this round |
| the per-line highlight model | done | `apps/ui/src/api/diffHighlight.ts` |
| compose the token cut with the intraline cut | open | model layer, not yet begun |
| lazy bundles, DiffView wiring, the palette | open | needs the composition first |
| rule on the sidebar's treatment | open | a ruling to record, not code |
| measure the 10k-line fixture | open | needs a real fixture and a real run |

## Next Steps
1. Compose the token cut with the intraline cut in the model layer, so one line
   carries both without either losing characters.
2. Ship the lazy per-language bundles and wire `loadDiffLanguageBundle` into
   `DiffView`, with a palette derived from custom properties already defined
   under `apps/ui/src` rather than invented.
3. Rule on the file sidebar's visual treatment and record the authority.
4. Measure the 10k-line fixture end to end and record the numbers in the
   feature file's Built State.

## Risks
- The palette may name only custom properties defined under `apps/ui/src`;
  `tests/ui_contracts/test_design_drift.py` fails any that is not.
- `npx vitest run` is gated under a 30-second timeout in
  `tests/orchestration/test_test_runner.py`.
