# Plan — F287 Provider session continuity across relaunch

## Goal
A relaunch of a task that a pause or a stop interrupted resumes, on the `claude-cli` provider, the
builder and reviewer sessions the task last used, so finished work is not paid for twice; every
other production provider records that it did not resume (docs/roadmap/features/T3_F287.md).
DECISION F287 D1 fixes the slices and their order.

## Current Step
Round 5 (DECISION F287 D4): `ClaudeCliProvider.supports_resume` answers true, the two pins change
with it, and `run_pingpong` with a stand-in CLI proves the repair-round resume and the fallback
once. Operator question Q8 records the ruling. This closes T001.

## Next Steps
1. T002 — a relaunch through `run_job` on `claude-cli` resumes the parked sessions; first measure
   whether the relaunch runs the provider in the parked run's working directory.
2. T003 — the other providers record that they did not resume; the operator guide names who does.
3. The amend0930b-slow-cap hardening stage (SLOW MODE), then closure.

## Risks
- The `claude` CLI keeps sessions per working directory; a relaunch in a new staging path may
  not find the parked session (T002 measures it first).
- Repair rounds on `claude-cli` now send shortened prompts to a continued session (F106, F109);
  the closure's self-use run is the first real observation (Q8).
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158 (Low) stay open,
  owned by F297.
