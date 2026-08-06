# Plan — F080 Machine-readable roadmap mirror & STATUS.md (R2)

Branch: feature/f080-roadmap-mirror — R1 PASS (LAST_REVIEWED_SHA
6787d6cf). No PR yet; F080's PR is created at closure.

## Goal
F080 R2 (SPLIT, LARGE): persist the R1 PASS verdict, then T003 — the
feature→mission adapter (detail file → PREPARED mission draft: context
input, plan seed, DoD seed, fences, each traceable to the file's
sections) with one real feature file compiled end to end, the docs
page for the `plan` CLI group, and the integration gate per
docs/agents/integration_gate.md. The adapter PREPARES: no job started,
approval left to the standard human path.

## Operator constraint (verbatim)
From 2026-08-13 the operator reaches this machine ONLY via SSH from a
phone. Starting Claude Code and invoking ONE skill must be the only
required touchpoint. Target: operational and rehearsed by 2026-08-12.

## Sequence
1. F080 (Machine-readable roadmap mirror & STATUS.md) — R2 in progress
   (T003 + docs + integration gate); closure is its own later round.
2. S1+S2 — build skill /build-remedy-self per the package: one-session
   Window-1 discipline (state probe -> decide -> rounds in-session),
   hard guardrails (PR-only merges at Open PR Gate, no force-push,
   explicit gates, .agent/STOP / session-limit / ambiguity ->
   F079 handoff + clean end).
3. S4 — rehearsal: F254 built through the skill, operator present;
   success = accepted with zero operator edits beyond starting it.
4. Normal feature flow through the skill (S5: review-zip stays the
   operator's remote window).

## Next Steps
- R2 done: verdict persisted, adapter + tests landed (T003), docs page
  registered, integration gate run — branch 15941 passed / 0 failed,
  zero branch-only failures, both base-only ids attributed
  (.agent/gate_f080_r2/attribution.txt). Branch pushed, still no PR.
- Reviewer gates R2 on the next relay.
- Then closure as its own round: evidence job, fresh review zip,
  STATUS [x], PR — not part of R2.
- Open for the reviewer: R-0205 (main is standing-red on
  test_context_mentions_resource_safety until a compliant
  .agent/context.md merges; this branch already carries one).

## Risks
- Hard date: self-drive operational and rehearsed by 2026-08-12.
- ADR-0001 (CYCLE_SAFETY_CAP) awaits human application; blocks
  multi-cycle loop delegation (S3 experiment lane), not the skill.
- The adapter's output format IS the later self-build intake
  (Orchestrator brief) — format doubts go into the handoff, not into a
  silent guess.
- R-0204 is a known xdist flake id; a recurrence in the gate is
  recorded as such with serial-rerun proof, never as a new failure.
