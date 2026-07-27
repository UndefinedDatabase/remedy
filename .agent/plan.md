# Plan — F048 Job queue (T1, file-based v1)

## Goal
Work can be queued per project and consumed unattended: entries are
enqueued per project, a consumer claims one atomically (two consumers
never claim the same entry), state survives restarts, and the queue is
honestly listable even with corrupt entry files. v1 is FILE-BASED to
match the existing atomic per-entity JSON storage — SQLite migration is
a later feature's decision.

## Checklist
- [x] Open PR Gate: PR #153 (F047) merged; main @ 40c7e4d
- [x] Claim: STATUS.md F048 → `[~]`; live_review.md reset (authored,
      sha256-verified); branch feature/f048-job-queue
- [ ] Inspection: locate the existing atomic create-if-absent primitive
      (stop-file / storage layer) — T001 MUST reuse it
- [ ] T001: job_queue.py entry store + enqueue/claim_next/release/
      complete/fail + (priority desc, created_at asc) ordering +
      corrupt-entry-tolerant listing + tests/orchestration/test_job_queue.py
- [ ] T002: tests/orchestration/test_queue_concurrency.py — N ≥ 20
      entries, TWO real subprocess consumers, ≥ 3 repeats, disjoint claim
      sets, full coverage, zero double-claims
- [ ] Canary: tests/cli/test_golden_path.py green
- [ ] Handback: handoff.md rewritten, branch pushed, NO PR this round
- [ ] T003 (next round): CLI `remedy queue add|list|rm|reclaim`,
      executor binding, end-to-end queued-goal-to-planned-job test
- [ ] Integration gate + closure (later rounds)

## Current Step
Inspection (item 3): find the atomic create-if-absent pattern, record
file:line and the exact primitive in the handoff. Then T001.

## Next Steps
T001 → T002 → canary → handback. T003 is a separate round.

## Risks
- Do-not-touch this feature: cron/scheduling, cross-project queues,
  SQLite.
- Do-not-touch this round: CLI commands, multi-cycle-executor changes
  (both are T003); stale-claim takeover logic — stale claims stay
  visible, explicit reclaim is T003.
- Never write into `## Verdicts` in live_review.md; never mark findings
  Resolved (reviewer-only).
- T002 must not "pass" by serializing consumers (whole-drain lock or
  single-process fallback) — that is a FAIL.
- Keep every commit under 500 changed lines; split if needed.
