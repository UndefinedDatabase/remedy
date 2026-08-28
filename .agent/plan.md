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
| claim F256 and retarget the state | done | `d4c00438` |
| the per-line highlight model | done | `apps/ui/src/api/diffHighlight.ts` |
| compose the token cut with the intraline cut | done | `739d31e0` |
| the DiffView wiring and the derived palette | done | `678bc698` |
| make the lazy load real, repairing `R-0732` | done | this round |
| rule on the sidebar's treatment | open | a ruling to record, not code |
| measure the 10k-line fixture | open | needs a real fixture and a real run |

## Next Steps
1. Rule on the file sidebar's visual treatment and record the authority.
2. Measure the 10k-line fixture end to end and record the numbers in the
   feature file's Built State.
3. Run the integration gate, then the closure sequence.

## Risks
- `tests/ui_contracts/test_diff_view_render.py` reads the comment-stripped
  source of `DiffView.tsx`; its `DELEGATED_RULES` and
  `REIMPLEMENTED_RULE_SPELLINGS` tuples are not to be edited.
- Moving the grammar tables must change no value in them, or a refactor has
  silently changed what a language highlights as.
