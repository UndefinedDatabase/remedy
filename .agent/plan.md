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
- [x] Inspection: secure_fs.write_file_atomically(create_only=True) —
      os.link no-clobber (secure_fs.py:532), as used by the F011 stop
      request (safe_points.py:372). T001 reuses it unchanged.
- [x] T001: job_queue.py entry store + enqueue/claim_next/release/
      complete/fail + (priority desc, created_at asc) ordering +
      corrupt-entry-tolerant listing; 26 tests green
- [x] T002: tests/orchestration/test_queue_concurrency.py — 24 entries,
      TWO real subprocess consumers, 3 repeats, disjoint claim sets, full
      coverage, zero double-claims; 6 tests green
- [x] Canary: tests/cli/test_golden_path.py — 42 passed
- [ ] Handback: handoff.md rewritten, branch pushed, NO PR this round
- [ ] T003 (next round): CLI `remedy queue add|list|rm|reclaim`,
      executor binding, end-to-end queued-goal-to-planned-job test
- [ ] Integration gate + closure (later rounds)

## Current Step
Handback. T001 and T002 are built and green, canary green. Path scheme:
<data_root>/queue/<project_id>/<entry_id>.json plus <entry_id>.claim.

## Next Steps
Push the branch and hand back for review of the branch point..HEAD.
No PR this round. T003 is the next round.

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
