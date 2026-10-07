# F116 acceptance re-audit 1 (amend0930b-slow-cap, repeat step)

Commit audited: a0188121689d3103d7f1a9c58cc1f10717b22779, branch feature/f116-cost-anomaly-alarm.

## What was read, and what was not

Read: the amend0930b-slow-cap paragraph of docs/agents/self_drive_protocol.md; AGENTS.md rules via CLAUDE.md pointer; docs/system/cost-anomaly-alarm-v1.md;
.agent/f116_acceptance_audit.md (the first audit); packages/orchestration/pingpong_job.py (burn pause part), apps/cli/commands/job.py (`_cmd_job_budget`);
tests/orchestration/test_job_burn.py and tests/orchestration/test_job_budgets.py (the burn classes). docs/roadmap/features/T3_F116.md was not re-read in full; the three claims came from the task text.
Not read: .agent/handoff.md, live_review*.md, plan.md, decisions.md, prose_slips.md, .agent/authored/, any .remedy-wt/f116-s3* or f116-r* folder.
(DECISION F116 Dn names appear inside code comments; I read only the code. The first audit's folder f116-audit was read for its mut.py and cli_driver.py, which I copied and adapted.)

## How the mutations ran

- Worktree: /home/decodeux/Repos/remedy/.remedy-wt/f116-reaudit-wt-1, detached at a01881216, removed with `worktree remove --force` at the end.
- Scripts in /home/decodeux/Repos/remedy/.remedy-wt/f116-reaudit/: `spec.json` (the three mutations), `mut.py` (control, mutate, run, `git checkout --` restore),
  `cli24.py` (command-line driver), `clirun.py` (applies each mutation, runs cli24, restores), `docmut.py` (docs mutation).
- Pytest: `python3 -B -m pytest -q -p no:cacheprovider <test ids>` with cwd = the worktree, one run at a time, no `-n`.
- Command-line proofs: in-process `apps.cli.grouped.main(["job","run",<id>,"--builder-provider","claude","--reviewer-provider","claude","--repair-rounds","0"])`,
  then `["job","budget",<id>]`, `["job","budget",<id>,"--json"]`, `["job","unpause",<id>]`, and `job run` again. REMEDY_DATA_DIR and the scratch git repo were folders
  inside the worktree (no job workspace or `remedy/job-*` branch appeared in the primary checkout; I checked the four job ids). Burn thresholds by the five
  `REMEDY_JOB_BURN_*` variables (window 1, min_samples 2, multiplier 3, min_spend 0); a stub provider reports tokens 1500, 1500, 15000, then 1500 each. The job carries the
  `auto_yes` approval audit and has NO budgets. I did not run `remedy do run --yes` (needs a live provider).
- Unmutated control first, then the mutation, then restore (`git checkout --`); tracked files were clean after each restore (only my untracked scratch folder remained).

## What really continues a burn-paused job (claim 24, by running the code)

Control CLI run, unattended spike job: `job run` -> state paused after 3 provider calls, one open decision. `job unpause <id>` exits 0, prints
"Job ... is paused and saved. continue it with: remedy job run <id>", and the state stays `paused`. A second `job run <id>` completes the job (5 calls total, state `completed`).
So `remedy job run <job_id>` continues it, and `remedy job unpause` does not. The decision impact in the product reads: "job <id> is paused; `remedy job run <id>` continues it, and answering this question only records your choice". The docs page says "`remedy job run <job_id>` continues it". Both match the product.

## Table

| Claim | Test | Mutation (file, exact change) | Control | Mutated | Verdict |
|---|---|---|---|---|---|
| 9b: the first burn decision of an unattended trip carries the whole sentence (and impact) | tests/orchestration/test_job_burn.py::test_an_unattended_trip_pauses_the_job_before_the_next_call | packages/orchestration/pingpong_job.py, the `_enqueue_burn_decision(...)` call: `question=_question,` -> `question=f"{_burn_marker} tripped",` | 1 passed | 1 failed | PROVED |
| 9b through the CLI | cli24.py: `job run` on an unattended spike job, then the open decision | same mutation | question = "[burn_alarm] The last 1 provider calls spent 15000.0 tokens each on average, more than 3 times the 1500.0 tokens per call this job spent before them (from call 3 on)." | question = "[burn_alarm] tripped" | PROVED (CLI) |
| 23: `job budget` shows the recorded burn alarm for a job with NO budgets, text and `--json` | tests/orchestration/test_job_budgets.py::TestJobBudgetCliRendersBurnReading::test_a_job_with_no_budgets_still_prints_its_recorded_burn_alarm and ::test_a_job_with_no_budgets_carries_its_burn_reading_in_json | apps/cli/commands/job.py, `_cmd_job_budget` no-budget branch: `_no_budget_burn = (getattr(_plan, "burn_reading", None) if _plan is not None else None)` -> `_no_budget_burn = None` | 2 passed | 2 failed | PROVED |
| 23 through the CLI (`grouped.main`) | cli24.py: `job budget <id>` and `job budget <id> --json` on the no-budget job | same mutation | text "no budgets configured." + "recorded burn alarm: rate: 15000.0 tokens per call against an expected 1500.0 (trailing_baseline) ..."; JSON `burn_reading` present | text only "no budgets configured."; JSON `burn_reading` absent/null | PROVED (CLI) |
| 24 (impact half): the burn decision's impact names `remedy job run <id>` | tests/orchestration/test_job_burn.py::test_an_unattended_trip_pauses_the_job_before_the_next_call (via `_expected_burn_impact`); the re-trip path is also pinned by test_a_second_trip_updates_the_open_burn_decision_in_place | packages/orchestration/pingpong_job.py, `_impact`: "is paused; `remedy job run \"" -> "is paused; `remedy job unpause \"" | 1 passed | 1 failed | PROVED |
| 24 through the CLI | cli24.py: decision impact, then `job unpause`, then `job run` | same mutation | impact names `remedy job run <id>`; unpause leaves job paused; `job run` completes it | impact names `remedy job unpause <id>` (which the CLI itself shows does not continue the job) | PROVED (CLI) |
| 24 (docs half): docs/system/cost-anomaly-alarm-v1.md names `remedy job run <job_id>` as what continues the job | none: no test in tests/ names the page or its sentence | docs/system/cost-anomaly-alarm-v1.md: "`remedy job run <job_id>` continues it" -> "`remedy job unpause <job_id>` continues it"; run against tests/docs, tests/cli/test_advertised_commands.py, tests/orchestration/test_doc_staleness.py | 377 passed | 377 passed | GAP |

## Gaps

1. Claim 24, docs half. The impact text is pinned by a test that turns red, but nothing guards the sentence on docs/system/cost-anomaly-alarm-v1.md that names the command. I changed it to say `remedy job unpause <job_id>` continues the job, which is false (the CLI proved unpause leaves the job paused), and the 377 tests in tests/docs, test_advertised_commands.py and test_doc_staleness.py stayed green. The product and today's docs agree, so this is an unguarded claim, not a wrong one. A repair needs a docs test that reads that page and asserts it names `remedy job run` (and not `remedy job unpause`) next to the burn pause, with its red proof.

Claims 9b and 23 (the first audit's gaps) now have proving tests and red mutations, in unit tests and through the command line. Claim 24's impact half is proved.

## Totals

- Claims re-audited: 3 (9b, 23, 24; claim 24 has two halves).
- PROVED: 2 whole claims (9b, 23), plus the impact half of 24; each with a unit-test mutation and a CLI mutation.
- GAP: 1 (the docs half of claim 24).
- Command-line proofs: 3, all through `apps.cli.grouped.main`, all changed under their mutation.
- Product meets all three claims.

## Cleanup evidence

`git -C /home/decodeux/Repos/remedy worktree list` (after removal; same 12 entries as at the start, wt-1 gone):

```
/home/decodeux/Repos/remedy                                  a01881216 [feature/f116-cost-anomaly-alarm]
/home/decodeux/Repos/remedy/.remedy-wt/job-034ab8c2d9fa4013  218eaabd6 [remedy/job-034ab8c2d9fa4013]
/home/decodeux/Repos/remedy/.remedy-wt/job-129b3ad7206d4f8d  09441a92a [remedy/job-129b3ad7206d4f8d]
/home/decodeux/Repos/remedy/.remedy-wt/job-1fe227733cbf41eb  218eaabd6 [remedy/job-1fe227733cbf41eb]
/home/decodeux/Repos/remedy/.remedy-wt/job-6a38b3203cca4928  aab638e21 [remedy/job-6a38b3203cca4928]
/home/decodeux/Repos/remedy/.remedy-wt/job-d0f70d9d45dd4363  e4fa7d06f [remedy/job-d0f70d9d45dd4363]
/home/decodeux/Repos/remedy/.remedy-wt/job-e7268925db3a4831  cc8696a37 [remedy/job-e7268925db3a4831]
/home/decodeux/Repos/remedy/.remedy-wt/job-e7a145761bf04f86  03d435e59 [remedy/job-e7a145761bf04f86]
/home/decodeux/Repos/remedy/.remedy-wt/job-f03587d31f444b15  3f36bd811 [remedy/job-f03587d31f444b15]
/home/decodeux/Repos/remedy/.remedy-wt/job-f146c82a6d8e42ca  8b6e803f7 [remedy/job-f146c82a6d8e42ca]
/home/decodeux/Repos/remedy/.remedy-wt/job-f196d785124e48bc  3f36bd811 [remedy/job-f196d785124e48bc]
/home/decodeux/Repos/remedy/.remedy-wt/job-fd57a5d1dfe245b0  68c833e6c [remedy/job-fd57a5d1dfe245b0]
```

Primary checkout `git status --porcelain`: (empty)
