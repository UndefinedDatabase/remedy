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
- [x] Handback R2; reviewer verdict R2 PASS (integration gate included)

## Closure round (STATUS_closure_protocol.md v3)
- [x] Commit A: R2 verdict persisted (f048-r3-1.md, sha256 + cmp exit 0)
- [x] Commit B: Built State in docs/roadmap/features/T1_F048.md;
      this commit's sha is ACCEPTED_HEAD (pre-zip head)
- [x] Preconditions: git status --porcelain empty · integrity check
      passed=true, 0 fails, 0 relevant untracked, no high blockers
- [x] Evidence job 58e88dd7-88c7-429f-823f-7b0e9bbb34f5 (164 passed
      across 6 measured runs); first attempt discarded — node_ids and
      output_hash producer pitfalls, recorded in the handoff
- [x] Review zip remedy-review-20260727-223612-READY_FOR_REVIEW.zip —
      READY, evidence authoritative, subject 40c7e4d..c6a0b58
- [x] Commit C (LAST, A4): authored STATUS `[x]` line (skeleton proved
      byte-identical) + evidence dir + final .agent state
- [ ] PR into main — created, NOT merged

## Current Step
Closure complete except the PR. No code changes this round.

## Next Steps
Open the PR and hand back. The PR stays OPEN: the next feature's Open PR
Gate merges it — that gap is the operator's manual-review window.

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
