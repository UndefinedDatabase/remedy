# F310 round 1 — amendment 1 (reviewer, after the worker's stop before C3)

The worker stopped before committing C3, as the block orders, on one existing test that C3 made
red: `tests/cli/test_plan_approval.py::TestConfigBudgetPrecedence::test_plan_fills_unset_config_field`
asserts that a task plan's suggested `max_provider_calls` of 42 fills a limit the configuration
leaves unset. That is exactly the behaviour DECISION F310 D2 (4) removes, so the test pins the
replaced mechanism and is changed with it (AGENTS.md, "Replacing is deleting").

1. C3 gains two paths: `tests/cli/test_plan_approval.py` and this amendment's copy,
   `.agent/authored/f310-r1-amend1.md` (a Python byte copy of
   `.remedy-wt/f310-r1/prep/amend1.md`).
2. In `tests/cli/test_plan_approval.py`, that one test is renamed
   `test_a_plan_suggestion_never_fills_an_unset_config_field`, its docstring or comment, if it has
   one, says that a task plan's suggested budgets are the planner's estimate and never a limit
   (DECISION F310 D2), and its assertion on `max_provider_calls` becomes that the job's `budgets`
   carry no `max_provider_calls` while the configured `max_total_tokens` of 5000 stays. Its
   fixture and every other test of the file stay as they are.
3. Every other part of the block stands. `verify.py` now checks this amendment's copy and accepts
   the two paths in C3; its new sha256 is in the reviewer's message.
