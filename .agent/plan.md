# Plan — F109 Semantic dedupe

Branch: feature/f109-semantic-dedupe, cut from `main` at
`5e18a8536afa086b591b5a2e13009d68d6227432` (pull request 231 merged).

## Goal

Within a RESUMED session only, stop resending context the model has
already provably received: segments whose hash already went to that exact
session are replaced by short reference markers. Everywhere else full
content wins, because only a resumed session guarantees the model still
holds the prior content. The scope rule of the whole feature is "resumed
session only, proven sends only".

## Current Step

Round 16, session 4. Clear the branch's stale prose before the
integration gate, so that gate runs over a tree whose comments are true.
Repair `R-0780`, the two deliberate absence bullets in
`session_sent_index.py` that still deny the loop wiring; register and
repair `R-0781`, the dedupe suite's module docstring, which omits the
T003d slice its own file carries and calls eleven call sites "the first
case". Also book round 15's PASS. Comments and docstrings only: no
executable line moves this round.

## Next Steps

- The integration gate (docs/agents/integration_gate.md).
- The closure sequence (docs/roadmap/STATUS_closure_protocol.md), which
  also runs the single consolidation pass on the checklist of
  docs/agents/planner_reviewer_prompt.md section 3.

## Risks

- Nothing dedupes in production: every concrete adapter returns
  `supports_resume = False`, so the mechanism is suite-only today.
  `docs/system/semantic-dedupe-v1.md` states this plainly.
- The measurement function is a library, consumed by the T003 fixture
  and by no production caller. The doc states that too.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each. That is `R-0778`.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
