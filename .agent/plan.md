# Plan — operator amendment amend1027-green-builds

## Goal
A claude-cli build order whose change is right ends green: the builder may run the project's
tests, the harness counts that run, no call dies after 120 seconds, and every project has its
own slug (2026-10-27). F319 closed with two real orders (universe-chat, remedy-edition).

## Current Step
Parts B and C: the builder's own test runs read from its stream; the DoD always runs the
project's command, blocking, with the order's time limit; tests_not_run only with a reason; a
claude-cli call gets 30 minutes (bounded by the job's wall clock) and one repeat after a
time-out. Part A is committed.

## Next Steps
1. The story: verification (tested_by, reason, output), scope.match, order_id, retries; 1.31.
2. Part D: remedy-edition registered and listed for orb-universe and orb-remedy.
3. Part E: GET /api/v1/jobs/{job}/evidence, docs, changelog.
4. Part F: the two real orders green; F319 registered and closed; the full suite; merge, push,
   supervisor restart, handback.

## Risks
- universe-chat's suite reads the sibling universe-kit (UNIVERSE_TEST_KIT); a job worktree and
  the tool sandbox both hide it, so the project's test settings must name it.
- The repo's settings deny reading `.data/**`; evidence is read through `remedy` commands.
