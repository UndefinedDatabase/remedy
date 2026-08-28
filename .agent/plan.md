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
| make the lazy load real, repairing `R-0732` | done | `8bcff3db` |
| rule on the sidebar's treatment | done | this round |
| measure the 10k-line fixture | open | needs a real fixture and a real run |

## Next Steps
1. Measure the 10k-line fixture end to end and record the numbers in the
   feature file's Built State, which is F256's last unbuilt piece.
2. Update `docs/roadmap/features/T5_F256.md` Built State with the three pieces
   and their test files.
3. Run the integration gate, then the closure sequence.

## Risks
- `tests/ui_contracts/test_diff_file_sidebar.py` and
  `tests/ui_contracts/test_diff_view_render.py` both read comment-stripped
  sources; a class and its rule must land in one commit or the element ships
  unstyled.
- The 10k-line measurement must be a real run against a real fixture; a budget
  is re-derived from a re-measured maximum and never raised by hand.
