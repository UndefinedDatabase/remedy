# Plan — operator amendment amend1027-green-builds

## Goal
A claude-cli build order whose change is right ends green: the builder may run the project's
tests, the harness counts that run, no call dies after 120 seconds, and every project has its
own slug (2026-10-27). F319 closed with two real orders (universe-chat, remedy-edition).

## Current Step
Part A: the builder's Bash rules take the project's found test command and its runner
spellings; its environment carries the project's tool folders; `--permission-mode dontAsk`.

## Next Steps
1. Part A4/B: the builder's own test runs read from its stream (builder_bash_calls.json); the
   DoD always runs the project's test command; tests_not_run only with a reason.
2. Part C: providers.claude_cli.call_timeout_minutes (30), planner and scope 10 minutes; one
   retry after a timeout, named in the story.
3. Part D: remedy-edition registered and listed for orb-universe and orb-remedy; scope.files
   expected/touched/match in the story.
4. Part E: GET /api/v1/jobs/{job}/evidence, the story's order_id, contract 1.31, docs, changelog.
5. Part F: the two real orders green; F319 registered and closed; the full suite; merge, push,
   supervisor restart, handback.

## Risks
- universe-chat's suite reads the sibling universe-kit (UNIVERSE_TEST_KIT); a job worktree and
  the tool sandbox both hide it, so the project's test settings must name it.
- The repo's settings deny reading `.data/**`; evidence is read through `remedy` commands.
