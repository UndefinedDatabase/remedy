## What

F267 — List commands v2 completion. Every list command Remedy has now honours the shared options
`--sort`, `--desc`, `--since`, `--until` and `--limit` in its own code, and one test proves it for
every list command the command catalog holds, rather than for a sample. A second test runs the
ten-second demo: a run finished two days ago is found with the one command
`remedy run list --since 3d --until 1d`, and the runs from five days and one hour ago are not.

## Why

F262 attached the five options to every list command, but the parser accepts an option nobody
reads, so its test could not tell a command that uses the options from one that ignores them.
F273 wired the last four commands. This feature adds the proof over the whole catalog, so a list
command added later that ignores the options fails a test instead of passing unnoticed.

## Key decision (in `.agent/decisions.md`)

- F267 D1 — the test takes its commands from the catalog's own list predicate, the one the catalog
  uses to attach the options, and excludes none: all 13 list commands refuse an unknown sort field
  and name the valid ones, in text and in JSON. The four commands F262 once excluded no longer
  exist, and the test fails if any of them returns. The demo seeds `run list`'s store directly,
  because a real run cannot be dated two days back.

## How to review

Read `tests/cli/test_list_commands_everywhere.py`, the only code this feature adds; no production
file changed. The Built State of `docs/roadmap/features/T2_F267.md` names the test for each
acceptance line. Round 1's mutation proofs made `change list`, `decision list`, `mission list` and
`config list` each ignore `--sort`, took away `run list`'s date, and pointed a relative time bound
forward; each turned exactly the matching cases red, with the unmutated control green before and
after.

## Changed files

| Path | +/- |
|---|---|
| `README.md` | +9/-3 |
| `docs/agents/planner_reviewer_prompt.md` | +4/-0 |
| `docs/roadmap/STATUS.md` | +1/-1 |
| `docs/roadmap/features/T2_F267.md` | +45/-0 |
| `tests/cli/test_list_commands_everywhere.py` | +164/-0 |

## Verification

- The one full suite, in the closure's integration gate: `18945 passed, 20 skipped` at exit 0,
  no bad node (`.agent/authored/f267-closure-suite.txt`).
- Evidence job `f267r3e1001` against the fork point `9f06c509`: 773 selected tests passed at exit 0.
- Review package `remedy-review-20260924-110023-READY_FOR_REVIEW.zip`, SHA-256
  `66aa577c32cf0650a2fb42815ee20d58a78ac6f97ba836fa5536d345b11c42b7`, READY_FOR_REVIEW.

## Findings

None registered. The four open findings are owned by the next findings paydown, F284.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
