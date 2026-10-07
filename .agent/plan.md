# Plan — F287 Provider session continuity across relaunch

## Goal
A relaunch of a task that a pause or a stop interrupted resumes, on the `claude-cli` provider, the
builder and reviewer sessions the task last used, so finished work is not paid for twice; every
other production provider records that it did not resume (docs/roadmap/features/T3_F287.md).
DECISION F287 D1 fixes the slices and their order.

## Current Step
Round 1: claim F287, re-head `.agent/live_review.md`, book F295's round 31 and resolve R-1159,
record DECISION F287 D1 and the slice order, and save the claim's measurement as
`.agent/f287_inventory.md`. No production code.

## Next Steps
1. T001 — `claude-cli` resumes: the CLI argv carries the session, `resume` reaches every call
   path, `supports_resume` true, `resume_used` and `resume_session_ref` set; the pin in
   `tests/orchestration/test_session_resume.py` changes with it.
2. T002 — a relaunch through `run_job` on `claude-cli` resumes the parked sessions; first measure
   the relaunch's working directory.
3. T003 — the other providers record that they did not resume; the operator guide names who does.
4. The amend0930b-slow-cap hardening stage (SLOW MODE), then closure.

## Risks
- The `claude` CLI keeps sessions per working directory; a relaunch in a new staging path may
  not find the parked session (T002 measures it first).
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158 (Low) stay open,
  owned by F297.
