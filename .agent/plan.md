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
- [x] T003a: `remedy queue add|list|rm` + tests/cli/test_queue_cmd.py;
      `queue_root()` promoted into data_paths.queue_dir(); 21 tests green
- [x] T003b: `remedy queue reclaim <id>` — TTL gate (config
      queue.reclaim_ttl_minutes, default 60) AND verifiably-gone owner
      (this host + dead pid); refusals name the owner; 34 tests green
- [x] T003c: opt-in executor binding (config queue.executor_binding,
      default off) — an idle run pulls claim_next, makes a NORMAL job that
      stops at PLANNED, complete()/fail() on the entry; 9 e2e tests green
- [x] Canary: tests/cli/test_golden_path.py — 42 passed
- [x] Integration gate: branch 159F/14147P vs base 201F/14017P; 7
      branch-only ids, all serial-PASS (xdist-flake class), no F048 test
      in either failure list → no blocker
- [ ] Handback: handoff.md rewritten, branch pushed, NO PR

## Current Step
Handback. The feature body is complete: store, CLI, reclaim, binding.

## Next Steps
Reviewer verdict on 7f05857..HEAD. Closure is its own round: STATUS
`[x]`, evidence job, review zip, PR — none of it done here.

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
