# Context — F022 Live cost ticker

## Active Branch
feature/f022-live-cost-ticker, cut from `main` at `c34ef32b`, the merge commit
of pull request #211 which closed F021.

## Scope
F022 only: the budget tick emission, the MetricsBar COST metric and the terminal
reconciliation. The roadmap feature file is
`docs/roadmap/features/T5_F022.md` and its Task slicing fixes the order.

## Do not touch
Budget enforcement, the pricing and basis rules, and MetricsBar's other metrics.
The feature file's own Do-not-touch section governs and is not narrowed here.

## Assumptions
- The UI never computes money. The backend is the single arithmetic home and the
  client's only arithmetic is the fill ratio.
- No currency field is emitted unless a price basis exists, so no invented
  dollars reach the display.
- The tick is additive on the SSE transport, which enumerates no event kinds, and
  is NOT additive on the humanize catalog, which is pinned equal to the Python
  vocabulary. Both halves were measured in `.agent/f022_inventory.md`.

## Constraints
- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- A round that emits a new Python event kind adds the matching key in
  `apps/ui/src/api/humanizeCatalog.ts` in the SAME commit and gates
  `tests/ui_contracts/test_humanize_catalog.py`; the two sets are pinned EQUAL
  and neither may move alone (DECISION F022 D1).
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- This is a UI feature, so `docs/ui/design_reference/` is binding and any visual
  deviation is documented with a technical reason.

## Steps
The round map lives in the `## Steps` section of `.agent/live_review.md`, per
R-0447's remedy, and this file deliberately does not restate it: a second copy
of the map is what fell out of step and cost this feature a finding.
