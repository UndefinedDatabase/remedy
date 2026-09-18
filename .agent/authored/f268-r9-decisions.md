
## DECISION F268 D17 (2026-09-18, reviewer, round 9) — what D16's deletion takes with it, and the smoke section that replaces the autorun one
CONTEXT: round 8's worker measured, with D16 (1) to (3) applied as a dry run at `deac5e74`, three
consequences no clause of D16 names, and the reviewer reproduced them at `5243e0a6`: a test calling
the `do.run` handler with `--ui` and `--no-ui`; `scripts/remedy_smoke.sh` section `12ao`, which runs
`remedy do` with `--autonomy-level 6 --max-cycles 3` and checks the autorun's JSON, and whose job id
sections `12aq` and the UX smoke gate after it read; and a pin of `do.run`'s `may_mutate_repo` still
asserting False. The reviewer's scratch probe at `5243e0a6` on a fixture git repository: `remedy do
"Make tests pass" --repo <fixture> --builder-provider fake --reviewer-provider fake --no-llm --no-ui
--json` exited 0 with one job and `stopped_before_apply` true; `remedy memory candidates <that job>
--json` exited 0 at `version` 1; and the smoke script's UX gate checker, run with that job id,
exited 0 (`story=5 journey items, checklist=2 items`).
CHOSEN: (1) `test_no_ui_suppresses_ui` in `tests/orchestration/test_autorun.py` leaves with `--ui`.
(2) Smoke section `12ao` becomes a `do` sequence end-to-end: a fixture git repository with one
commit, the command above with the fixture's path, and checks that the output is JSON with a
`mission_id`, a non-empty `job_ids` and `stopped_before_apply` true; its first job id is the id the
later sections read, under the name `DO_JOB_ID`. (3) The `do.run` catalog pin in
`tests/cli/test_job_commands.py` asserts True, R-0969's value. ALTERNATIVES: delete sections `12ao`,
`12aq` and the UX gate together, rejected because the probe shows a sequence job serves the two later
sections unchanged. REVERSE: restore the section and the two tests from git history; delete this
paragraph.
