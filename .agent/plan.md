# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`.

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 (`docs/roadmap/features/T2_F281.md`).
DONE when T001 and the Acceptance list hold. As of round 26, IT DOES; the
feature is in the closure sequence.

## Current Step

ROUND 30 — CLOSURE, RETRY C. C1 books round 29's FAIL (it claimed a
BLOCKED_EVIDENCE package was ready for closure — a false live indicator,
root-caused to `.agent/handoff.md` changing between evidence staging and
the zip build). C2 rebuilds the evidence job and zip as ONE uninterrupted
sequence — no commits, no tracked-file writes in between — confirms
`READY_FOR_REVIEW`, runs the integrity check, and ONLY THEN writes the
handback as the final, separate action.

## Next Steps

1. Once a genuinely READY package exists, closure round B lands: STATUS
   line (reviewer authors), README capability sync, self_use_queue.json's
   `consumed_by` (already set to F281 in round 28 — confirm it survived),
   ledger rotation, final commit, PR. Read
   `docs/roadmap/STATUS_closure_protocol.md` step by step for the exact
   commit shape and ordering.
2. Session 4 continues while context comfortably suffices.

## Risks

- The evidence/zip staging mechanism is fragile to ANY tracked-file write
  between staging and packaging — the next round that touches it keeps the
  whole sequence to one uninterrupted burst with no commit in the middle,
  and writes the handback ONLY after a confirmed READY status.
- Round 28's self-use consumption and round 27's full-suite transcript
  both stand untouched; do not redo either.
