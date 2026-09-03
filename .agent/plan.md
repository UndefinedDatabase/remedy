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

Round 15, session 4. The T003 DOCS: `docs/system/semantic-dedupe-v1.md`
describes the built state — the sent-hash index, the composition hook,
the kill switch, the trace record and the measured savings — and is
registered in `docs/README.md` in the same commit. Also book round 14's
PASS and resolve `R-0779`, and REGISTER `R-0780`: two deliberate absence
bullets in `session_sent_index.py` still tell a reader the loop invokes
nothing, three wiring commits after it did. This round does not touch
that file.

## Next Steps

- Repair `R-0780` in `packages/orchestration/session_sent_index.py`.
- The integration gate (docs/agents/integration_gate.md).
- The closure sequence (docs/roadmap/STATUS_closure_protocol.md), which
  also runs the single consolidation pass on the checklist of
  docs/agents/planner_reviewer_prompt.md section 3.

## Risks

- Nothing dedupes in production: every concrete adapter returns
  `supports_resume = False`, so the mechanism is suite-only today. The
  doc states this plainly rather than leaving it to be discovered.
- The measurement function is a library, consumed by the T003 fixture
  and by no production caller. The doc states that too.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each. That is `R-0778`.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
