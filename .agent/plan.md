# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20. Rounds 1 to 15 are
reviewed and 2 to 15 PASSED. T001 is CLOSED. T002 is open on the RUN side: the job
record has MOVED, both resolvers return `str`, the ping-pong and run-log stores
have one spelling on the production side, and a run is now an INVOCATION rather
than an event (DECISION F260 D7).

## Goal

SESSION 7 REACHES THE SOFT LIMIT — 25 rounds or 7 sessions, whichever comes first,
and this is session 7. The obligation is a SCOPE REPORT and then the standing
default of operator amendment amend0905-throughput: SPLIT-AND-CLOSE, executed on
this session's own authority. F260 closes at the scope it has actually built; the
remaining scope is registered as a new follow-up feature placed directly after
F260, per operator order amend0906-split-placement.

## Current Step

Round 16 brings `origin/main` onto the branch — it carries
amend0906-split-placement, the rule that governs this session's split — books the
round-15 PASS verdict and its prose slip into the record, and rewrites this plan.

## Next Steps

1. Register the follow-up feature: its detail file, its STATUS line directly after
   F260's inside the same tier heading, the README counters, the TOTAL_FEATURES
   pin and the downstream "Depends on" lines, in ONE commit; a DECISION records
   the split and how to reverse it.
2. The integration gate: the full suite at the branch head and at the merge base.
3. Closure part 1: the self-use item, the evidence job and the review zip.
4. Closure part 2: the verdict bookings and the ledger rotation.
5. Closure part 3: the STATUS accepted flip, the README sync, the handback and the
   pull request, which is left UNMERGED as the operator's review window.

## Risks

- The feature file's Orchestrator brief names the split point "between T003 and
  T004"; this split falls inside T002 and therefore amends that brief. It is ruled
  as a DECISION and proceeded under, never asked as a question
  (docs/agents/planner_reviewer_prompt.md §4 item 7).
- README.md and docs/roadmap/STATUS.md may never disagree in any committed state,
  so the registration counters and the closure flip each land in one commit.
