# Context — F031 Decision inbox

## Active Branch
feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge commit
of pull request #213 which closed F022.

## Scope
F031 only: the decision read endpoint and blocked-size computation, the inbox
cards with their generic options renderer, ordering, filtering and badge, and
the answer wiring through the existing write channel. The roadmap feature file
is `docs/roadmap/features/T5_F031.md` and its Task slicing fixes the order.

## Do not touch
The decision queue's storage format and its CLI semantics, and the write
channel's nonce and audit behaviour. The feature file's own Do-not-touch
section governs and is not narrowed here.

## Assumptions
- The decision queue is and stays FILE-BASED. The inbox is a READ VIEW plus
  command wiring, never a storage migration; an earlier sketch's "(SQLite)" is
  explicitly not the design.
- The card renderer is generic over the decision's options payload. No
  per-type form is hardcoded, which the extensibility test pins.
- Answering reuses the existing decision-answer command through the write
  channel rather than adding a second write path.

## Constraints
- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- This is a UI feature, so `docs/ui/design_reference/` is binding and any
  visual deviation is documented with a technical reason.

## Steps
The round map lives in the `## Steps` section of `.agent/live_review.md`, per
R-0447's remedy, and this file deliberately does not restate it: a second copy
of the map is what fell out of step and cost F022 a finding.
