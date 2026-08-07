# Plan — S1+S2 self-drive skill (R1); F080 closed and merged

Branch: feature/selfdrive-skill. PR #184 (the ADR-0001 cycle-cap
micro-round) merged at this round's Open PR Gate. F080 is accepted and
merged; Rule A5 still names F103 (Token ledger, SQLite) as the next
ROADMAP feature — this track is infrastructure and claims no STATUS
line.

## Goal
Build the one-session build discipline: docs/agents/self_drive_protocol.md
(roles, phases, guardrails), the `/build-remedy-self` command, the
remedy-self-drive skill, docs-index registration, and test pins — so the
operator can start Claude Code, invoke ONE skill, and have a feature
built end to end with the review discipline intact.

## Operator constraint (verbatim)
From 2026-08-13 the operator reaches this machine ONLY via SSH from a
phone. Starting Claude Code and invoking ONE skill must be the only
required touchpoint. Target: operational and rehearsed by 2026-08-12.

## Current Step
R1 — four commits on feature/selfdrive-skill, each with its own gate:
(1) state + candidate sweep + closure-protocol pitfall (d);
(2) the protocol doc + docs/README.md registration;
(3) the skill + the command + .claude/README.md contents;
(4) the pins in tests/test_agent_tooling.py.
Stop at the first red verification (AGENTS.md If Blocked).

## Next Steps
- R2: reviewer gates R1, repairs findings, then decides the S4
  rehearsal round.
- S4: rehearsal — F254 built end to end through the skill with the
  operator present; success = accepted with zero operator edits beyond
  starting it.
- Then normal feature flow through the skill, starting at F103.

## Risks
- Hard date 2026-08-12; today is 2026-08-07, so R1+R2 leave a buffer of
  roughly three days for the rehearsal and one repair round.
- The reviewer's independence is weaker in one session than across two
  windows. Mitigated by DECISION D6 (delegated worker subagent, one per
  round) — not eliminated. The review zip stays the operator's
  out-of-band window.
- ADR-0001 is applied (CYCLE_SAFETY_CAP 8, DEFAULT_MAX_CYCLES 1), so
  S3's delegation lane is unblocked; it stays out of scope for R1.
