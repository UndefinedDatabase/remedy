
## DECISION F276 D8 (2026-09-20, reviewer, round 7) — a limit the operator can be stopped by is a limit the operator can see BY NAME, and the guard for that is written over the model rather than over the missing name

CONTEXT: R-1006, raised at round 6's gate and measured at `b9e55410` by driving the real
`apps.cli.commands.job._cmd_job_budget` over a persisted job. `remedy job budget <job_id>`
renders its limits as one hand-written `if _budgets.<field> is not None` line per limit. That
block was written when `JobBudgets` had five fields; T004 added a sixth and did not touch it, so
the disk floor is the one limit whose NAME never appears. The pair of numbers is not lost — the
evaluation's own `free_disk: <free>/<floor> bytes` source line prints whenever an evaluation ran
— and `--json` carries the field, because that path is `model_dump`. The `elif _budgets_dict`
fallback directly beside the block prints every key it holds, so the two branches of the same
command disagree about the same job.

CHOSEN. (1) The floor is printed in that block, as `min_free_disk_bytes`, the FIELD name, which
is the label every other limit there already uses and the string `budget_exhausted:<limit>`, the
config key `budget.min_free_disk_bytes` and the `--json` `limits` object all spell the same way.
(2) It is listed LAST, after `deadline`. The block's order is neither `_LIMIT_ORDER` nor the
model's declaration order — `max_cost_usd` and `max_wall_clock_minutes` sit the other way round
from both — so there is no rule to follow, and appending is the one position that disturbs no
ordering an existing test pins; `tests/orchestration/test_job_budgets.py` asserts
`max_total_tokens < max_cost_usd < max_wall_clock_minutes` and nothing else about position.
`_LIMIT_ORDER`'s reason for putting the disk FIRST is about which single limit a stop REPORTS,
which this listing is not. (3) The guard is written over `JobBudgets.model_fields`, not over the
one missing name: a test that configures every field of the model and asserts that every field
name appears in the output goes red for the SEVENTH limit exactly as it would have gone red for
the sixth. A second, narrow test pins the floor's own printed value, because the universal would
also be satisfied by printing the name beside the wrong number. (4) Nothing else about the
command changes — not the `--json` shape, not the source lines, not the `_budgets_dict`
fallback, not the cost rendering.

CONSEQUENCE: a configured disk floor appears in `remedy job budget <job_id>` under its own name,
and the next limit added to `JobBudgets` cannot reach a release with this rendering one field
behind the model. This is the same defect class as R-0225 and as the hand-written manifest key
set this feature's own round 6 replaced with `run_manifest._budget_allowed_keys()` — a second
spelling of a model's field set, drifting — arriving in a RENDERING rather than in a schema, and
it is answered the same way: derive, or guard against the derivation.

ALTERNATIVES: leaving it and carrying R-1006 to the next findings-paydown feature, rejected
because the field is this feature's own and the repair is nine lines with a guard, so carrying it
would close F276 knowing one of its own surfaces is incomplete; rewriting the block as a loop over
`model_fields`, rejected because `max_cost_usd` and `deadline` have genuinely different renderings
(`$%.4f` and `.isoformat()`) and a loop would either lose those or re-introduce a per-field
special case with none of the clarity; listing the floor FIRST to mirror `_LIMIT_ORDER`, rejected
under (2).

REVERSE: delete the two printing lines and their comment from
`apps/cli/commands/job.py::_cmd_job_budget`, delete the class
`TestEveryConfiguredLimitIsNamedInTheTextOutput` from `tests/orchestration/test_job_budgets.py`,
and delete this paragraph.
