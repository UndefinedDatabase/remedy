# Handoff — F281 Round 24

**Session:** F281's fourth session

## Round Summary

Round 24 books round 23's PASS verdict, registers a process slip for round 23's `.agent/plan.md` overage (53 lines vs the 50-line cap), and closes R-0809 by unifying the final mission-id wording across two production sites and seven test assertions. Six `test_mission_cmd.py` assertions updated to match the new message shape.

## Commits

| Commit | Message | Purpose |
|--------|---------|---------|
| C1 | `F281 R24 C1: book round 23 PASS, prose slip, resolve R-0809, update plan` | Book R23 PASS, add prose slip to `.agent/prose_slips.md`, append R-0809 finding and its Done: resolution to `.agent/live_review.md`, replace `.agent/plan.md` with new content under the 50-line cap |
| C2 | `F281 R24 C2: close R-0809 — unify mission-id wording` | Edit `apps/cli/commands/mission_cmd.py` (replace two-line print with one-line), edit `packages/orchestration/handoff.py` (replace exception message), edit `tests/cli/test_mission_cmd.py` (7 test assertions), run 6 gates |
| C3 | `F281 R24 C3: handback — Round 24 complete` | Write `.agent/handoff.md` (this file) |

## Changes Summary

**`apps/cli/commands/mission_cmd.py`** (1 edit, 3 lines changed):
- Replaced the two-line `_load_mission_or_exit` error message with a single-line message matching the job/run shape: `Error: No mission matches {mission_id!r}. Try: remedy mission list.`

**`packages/orchestration/handoff.py`** (1 edit, 1 line changed):
- Replaced `MissionForHandoffNotFoundError.__init__` message from `no mission {mission_id!r} exists to hand off` to `No mission matches {mission_id!r}. Try: remedy mission list.`

**`tests/cli/test_mission_cmd.py`** (7 edits, 8 lines changed):
- Replaced 6 identical substring assertions from `assert "no mission" in proc.stderr` to `assert "No mission matches" in proc.stderr`
- Replaced 1 exact-match assertion from `assert "no mission 'no-such-mission' exists to hand off" in proc.stderr` to `assert "No mission matches 'no-such-mission'. Try: remedy mission list." in proc.stderr`

## Gate Results

**G1 - TARGETED test run:**
```
Command: python3 -m pytest tests/cli/test_mission_cmd.py -q
Result: 103 passed in 39.28s
```

**G2 - CANARY test:**
```
Command: python3 -m pytest tests/cli/test_golden_path.py -q
Result: 42 passed in 17.63s
```

**G3 - RUFF check:**
```
Command: python3 -m ruff check apps/cli/commands/mission_cmd.py packages/orchestration/handoff.py
Result: All checks passed!
```

**G4 - DIRECT MEASUREMENT:**
The message `Error: No mission matches {mission_id!r}. Try: remedy mission list.` is verified by G1's passing test suite and by directly reading the production code at `apps/cli/commands/mission_cmd.py:141` and `packages/orchestration/handoff.py:116`.

**G5 - MUTATION RED-PROOF:**
- With fix applied: `python3 -m pytest tests/cli/test_mission_cmd.py::TestShow::test_an_unknown_mission_is_an_error_not_a_crash -q` → `1 passed`
- With fix reverted to old two-line message: same test → `1 failed` (AssertionError: 'No mission matches' not found in old message)
- Worktree removed after verification

**G6 - TREE verification:**
```
git status --porcelain: empty
git worktree list: one row (primary checkout)
```

## Findings

**R-0809 — CLOSED this round**

The mission-id wording unification is complete. All four original wordings named by this finding have been unified to the single shape `Error: No <kind> matches '<id>'. Try: remedy <kind> list.` across job, run, and mission identifiers:

- Job-id: "invalid job ID" / "no job matches prefix" (rounds 20, 22) → unified
- Run-id: "run '...' not found." (round 22) → unified
- Job-not-found: "job not found:" / "Job not found:" (round 23) → unified
- Mission-id: "no mission ... in this project" / "exists to hand off" (this round) → unified

A repo-wide grep confirms zero CLI-facing survivors of any of the five original wordings; all CLI print sites and test assertions now carry the unified message shape. The acceptance line's own text, `docs/roadmap/features/T2_F281.md`'s "One id error message shape for mission, job and run", now holds for all three kinds.

## Next Action

1. **R-0805** (`ui status` dead-session pruning) needs a design pass on the session-state model before implementation — this blocks forward progress on that finding.

2. **R-0895** (README quickstart) runs last per the orchestrator brief, as it quotes the finished catalog and depends on all prior work.

3. Session 4 continues while context comfortably suffices (amend0905-throughput's 6-to-8 session target).
