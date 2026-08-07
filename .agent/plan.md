# Plan — S1+S2 self-drive skill BUILT and accepted; S4 rehearsal next

Branch: feature/selfdrive-skill · PR #185 open and unmerged by design —
it merges at the next work item's Open PR Gate, which is the operator's
manual-review window. R1 through R4 all PASSed; 0 open findings; next
free finding ID R-0211 — R-0210 was raised and fixed in R4. R5 is the
S4 rehearsal session's opening round.

## Goal
The one-session build discipline is on the branch: the protocol
(docs/agents/self_drive_protocol.md), both entry points (the
remedy-self-drive skill and the build-remedy-self command), the docs
and .claude registrations, and three pins that keep the guardrails from
being dropped silently. The operator can start Claude Code, invoke ONE
skill, and have a feature built with the review discipline intact.

## Operator constraint (verbatim)
From 2026-08-13 the operator reaches this machine ONLY via SSH from a
phone. Starting Claude Code and invoking ONE skill must be the only
required touchpoint. Target: operational and rehearsed by 2026-08-12.

## Current Step
R5 — the S4 rehearsal session's opening round: record the R4 PASS
verdict in .agent/live_review.md so the build's evidence chain is
closed before PR #185 is merged. This round performs no merge and
creates no branch; the Open PR Gate is the next round's first action.

## Next Steps
- S4 rehearsal, FRESH session: build F254 (Model alias table & dead-model
  doctor check) end to end through the skill, operator present. Success
  = F254 accepted with zero operator edits beyond starting the session.
  Its Open PR Gate merges PR #185 first.
- If the rehearsal surfaces findings: one repair round, then re-run it.
- Then normal feature flow through the skill, starting at F103 (Token
  ledger, SQLite) — Rule A5 already names it.

## Risks
- Phases 1 and 2 of the protocol have never run for real; only Phase 0
  is proven by execution. The rehearsal is the first real exercise and
  is deliberately supervised.
- Hard date 2026-08-12; today is 2026-08-07, leaving room for the
  rehearsal plus one repair round.
- The reviewer's independence is weaker in one session than across two
  windows. Mitigated by D6 (delegated worker subagent, one per round) —
  not eliminated. The review zip stays the operator's out-of-band
  window and is unaffected by any of this.
