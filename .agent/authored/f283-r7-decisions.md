
DECISION F283 D2 (2026-09-21, round 7) — UNDER `--json` THE COST-PREVIEW ESTIMATE LINE GOES TO
STDERR, AND THE NON-TERMINAL REFUSAL GOES THROUGH `fail()`.

CONTEXT. Finding R-1024. `apps/cli/cost_preview_confirm.py::confirm_cost_preview` prints the
estimate line to stdout on every path that proceeds, and on a non-terminal stdin without `--yes`
prints an `Error:` line to stderr and exits 2 itself. Its one caller is `_cmd_job_run_cycles`,
which serves `job run` and `job resume`, and both declare `supports_json`. Under `--json` a
consumer therefore reads a prose line before the command's JSON, or reads prose and nothing.

CHOSEN. The helper takes `json_output: bool = False`, and its caller passes its own. Under the
flag, every line the helper prints for a human goes to stderr instead of stdout, byte for byte
the same text; and the non-terminal refusal becomes `fail("confirmation_required", <the same
sentence without its "Error: " prefix>, json_output=json_output, exit_code=EXIT_USAGE)`. With the
flag off nothing changes: the same lines on the same streams, the same exit code. The estimate
line is kept rather than dropped under `--json` because its docstring states why it exists — "so
the skip is visible in evidence" — and stderr keeps it visible to the operator and to any log
that captures both streams, while stdout stays the one parseable object the envelope promises.

ALTERNATIVES. Put the estimate into the command's JSON as a key — rejected for this round: the
helper returns a bool before the command has built any output, so carrying the estimate would
change the helper's return shape and every caller's success document, which is T002's sweep and
not a refusal repair. Suppress the line under `--json` — rejected: it removes the audit trail of
a skipped confirmation, which is the one thing the `--yes` branch exists to leave behind.

REVERSE by deleting this paragraph and restoring `apps/cli/cost_preview_confirm.py` and its one
call site in `apps/cli/commands/job.py` from git history at the parent of the commit that lands
this decision's patch.
