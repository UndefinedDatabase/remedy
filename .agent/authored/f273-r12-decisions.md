
## DECISION F273 D12 (2026-09-19, reviewer, round 12) — a test run accepts the intent id an apply prints, the apply names its verifying test run, the continuation cycle is three commands, and the smoke script and its tests read what the product writes
CONTEXT: R-0921, R-0917, R-0922, R-0916, R-0899, R-0910, R-0980, R-0978 and the R-0988 this round
registers each needed a choice between routes their texts allow, taken in the round that lands the
patch (amend0917-throughput rule 3). Measured by research helpers and re-measured by the reviewer's
dry run at `4c375fc4`: `_validate_linkage` in `packages/orchestration/test_execution_service.py`
resolves an intent id against a `patch_intents` key nothing writes; `patch apply` prints no next
action; `--yes` on the run command is declared and no test drives it through the parser; the
deleted `do_continue` left no single continuation word; the smoke script's job check reads `state`
where `job show` prints `status`; section 12s requires an event only a test-only module emits;
`test_study_run_dispatch_e2e` reaches whatever model answers on the default host; and
`test_direct_run_calls_remedy_smoke` runs the script with no working directory, so its
`.data/smoke/` log lands in the checkout pytest runs from.
CHOSEN: (1) R-0921. The gate resolves an intent through `approval_queue._find_artifact_for_intent`,
the lookup `patch approve` and `patch apply` use. (2) R-0917. `verifying_test_run_action` names
`remedy test run <job> --intent-id <id> --apply-id <id>` for an applied or no-op apply; `patch
apply` prints it as its last line and carries it as `next_safe_action` in its JSON. Both ids are
the intent id, because the apply record writes `apply_id` equal to it; `--task-id` is left out
because an intent's task need not be a job task. (3) R-0922. The code half landed at `ef618eac`;
this round adds the test that runs `do run --yes` through the parser to the auto-approval branch,
with the planner stubbed so no model is called. (4) R-0916, THE RULING its Acceptance line asks
for: the continuation cycle is three surviving commands and no single word — `remedy patch apply`,
then the `remedy test run` that (2) prints with the apply record's ids, then `remedy change proof`
— with no lease or checkpoint of its own: `test run` holds its own job and repository leases,
`patch apply` is idempotent by its apply record, and each step reads the durable record the one
before wrote. A passing test run still names `job show` as its next action, not `change proof`;
that link is left as it is. (5) R-0899. The smoke check reads `status`, and a test runs it on the
`job show` output of a job created offline. (6) R-0910. A test holds every word section 0 loops
over to the catalog's own group reader, which counts an alias as the group it names, as the CLI's
dispatch does. (7) R-0980. Section 12s is dropped, and a test holds its absence. (8) R-0978. The
test points `REMEDY_OLLAMA_HOST` at a local listener that hangs up, asserts that listener was the
host asked, and lowers the subprocess timeout from 90 to 30 seconds; the test no longer depends on
any model host. (9) R-0988. The fixture imports `study` before it patches and patches `study`'s own
binding. (10) The smoke script's direct run is given a temporary working directory, so its log
never lands in a checkout; this is one writer of R-0803's class, repaired here, and R-0803 itself
still resolves at closure by its own transcript (§3 item 30: no second id).
ALTERNATIVES: making a passing test run print `change proof`, rejected as a change no finding asks
for; counting only group ids for R-0910, rejected because the dispatch accepts aliases; raising
R-0978's timeout, forbidden by its own Acceptance line.
REVERSE: restore `test_execution_service.py`, `patch_apply.py`, `apps/cli/commands/patch.py`,
`scripts/remedy_smoke.sh` and the four test files from `4c375fc4`, and delete this paragraph.
