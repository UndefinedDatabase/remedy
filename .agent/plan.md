# Plan — F048 Job queue (T1, file-based v1) — round 2

## Goal
Work can be queued per project and consumed unattended: entries are
enqueued per project, a consumer claims one atomically, state survives
restarts, and the queue is honestly listable. Round 2 finishes the
feature body: queue CLI, explicit reclaim, opt-in executor binding, and
the dedicated integration gate.

## Checklist
- [x] R1 (40c7e4d..7f05857) reviewed PASS — verdict persisted from the
      authored text f048-r2-1.md (sha256-verified, cmp exit 0)
- [ ] T003a: `remedy queue add|list|rm` + tests/cli/test_queue_cmd.py
      (rm refuses a claimed entry and names the owner)
- [ ] T003b: `remedy queue reclaim <id>` — only when the claim is older
      than the TTL (config, default 60 min) AND the owner's pid is
      verifiably dead on this host; refuse otherwise, naming the owner
- [ ] T003c: opt-in executor binding — idle multi-cycle executor pulls
      claim_next, makes a NORMAL golden-path job (intake → plan →
      approval unchanged), complete()/fail() on the entry; e2e test
- [ ] Canary: tests/cli/test_golden_path.py green
- [ ] Integration gate: full suite per docs/agents/integration_gate.md
- [ ] Handback: handoff.md rewritten, branch pushed, NO PR

## Current Step
T003a — the queue CLI, following the F147 golden-path command patterns.
Promoting `queue_root()` into data_paths.py is in scope this round.

## Next Steps
T003a → T003b → T003c → canary → integration gate → handback.

## Risks
- Do-not-touch: cron/scheduling, cross-project queues, SQLite.
- No closure work this round: no STATUS `[x]`, no evidence job, no zip,
  no PR — closure is its own reviewer-gated round.
- Approval rules unchanged: a queued entry never bypasses plan approval
  unless the run itself carries `--yes`. No hidden `--yes` default.
- No silent takeovers (P2): reclaim is explicit, TTL- and pid-gated.
- Never write into `## Verdicts` beyond applying f048-r2-1.md as
  authored; never mark findings Resolved (reviewer-only).
- Keep every commit under 500 changed lines; split if needed.
- Known risk from the R1 verdict: the T002 interleaving assertion can
  flake on a starved runner — red without a code change is an
  environment signal first.
