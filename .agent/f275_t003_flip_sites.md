# F275 T003 — the flip site set, ENUMERATED

Measured for the base `965ea50d`, as DECISION F275 D17's closing clause orders:
T003 re-derives the set at its own base rather than inheriting round 31's
figures. The instruments ran in a disposable `git worktree` checked out at
`d68125d1` — that base plus this round's two R-0870 prose repairs. Neither repaired
file carries a single site in the union below (zero each, checked rather than
assumed), so neither can have shifted a line number here: the reading at `d68125d1`
and the reading at `965ea50d` are the same reading.

THIS FILE ENUMERATES THE FLIP; IT DOES NOT PERFORM IT. Round 31's
`.agent/f275_t002_flip_inventory.md` SIZED the change and gave figures. This file
NAMES every site, one line per file, so that the flip commit is applied from a
committed list instead of from a measurement taken while the tree is moving
under it. The split exists because of the commit cap: a per-site enumeration is
1753 lines and cannot be one commit, while the per-FILE rendering in section 4
is 184 lines and can.

NO LINE OF THE FLIP MOVED IN THE ROUND THAT WROTE THIS FILE — stated at the width
it was measured and no wider. No path under `apps/`, `docs/` or `scripts/`
changed in round 36 at all. The only paths under `packages/` and `tests/` that
changed are the two R-0870 prose repairs committed at C3:
`packages/common/public_text_redaction.py`, a docstring sentence a later deletion
had falsified, and `tests/cli/test_mission_cmd.py`, a test whose name and
docstring had outlived the assertion they described. Neither touches a `.id` or
`.name` site.

## 1. The two runs

Both ran serially in the worktree, with `__pycache__` purged first and every run
under `python3 -B`.

### (a) the DECISION F272 D7 descriptor probe over the full suite

```
$ python3 -B -m pytest tests/ -q -p r31probe
18343 passed, 23 skipped, 1 warning in 1288.65s (0:21:28)
REAL_EXIT=0
```

The round 36 block predicted this run RED — `1 failed, 18336 passed, 29 skipped,
1 warning in 1289.85s (0:21:29)` at exit 1, the failure being
`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`,
described there as a worktree `apps/ui/node_modules` artifact and not a probe
effect. THE PREDICTION DID NOT REPRODUCE, and the difference is recorded here
rather than smoothed over. This worker's first attempt did reproduce it, with a
different mechanism than the block states: the worktree DOES have
`apps/ui/node_modules` (201 entries against the primary checkout's 205), and the
error was `ERR_MODULE_NOT_FOUND: Cannot find package 'vitest' imported from
/home/decodeux/Repos/remedy/node_modules/.vite-temp/…` — vite writing its
temporary config into the PRIMARY checkout's `node_modules` and then failing to
resolve `vitest` from there. Run in isolation immediately afterwards the same
test passed at exit 0 in 1.30s, so the failure is an order-dependent artifact of
that shared temp directory, not a property of the tree. On the run recorded above
it did not recur. The passed count is 7 higher than the block's for two reasons
that account for it exactly: the vitest test itself now passes (+1), and six
tests the earlier run skipped executed and passed instead (+6), which is also
why the skip count fell from 29 to 23.

The probe is behaviour-neutral, measured and not assumed: the golden-path canary
under `-p r31probe` read `42 passed` at exit 0.

### (b) the `ast` sweep over `git ls-files '*.py'`

Whole stdout:

```
$ python3 -B r31_static.py
tracked .py from git ls-files: 991 parsed: 991 unparsable: 0
attribute sites recorded: 4904
  verdict job      323
  verdict other    293
  verdict unknown  4288
  constructions  582
  imports        345
  annotations    368
REAL_EXIT=0
```

## 2. Figures — measured, against the block's carried figures

A site is one `(path, line, field)` triple; a changed line is one `(path, line)`
pair. The `reviewer` column carries the round 36 block's numbers verbatim, so
that any difference is visible. No measured number was edited to match one.

| figure | measured | reviewer | verdict |
|---|---:|---:|---|
| probe: sites | 1745 | 1745 | same |
| probe: distinct changed lines | 1743 | 1743 | same |
| static: provably `Job`, distinct triples | 312 | 312 | same |
| UNION: sites | 1753 | 1753 | same |
| UNION: distinct changed lines | 1751 | 1751 | same |
| UNION: production lines | 349 | 349 | same |
| UNION: production files | 68 | 68 | same |
| UNION: test lines | 1402 | 1402 | same |
| UNION: test files | 116 | 116 | same |
| provably `Job` but never executed | 8 | 8 | same |
| tracked `.py` | 991 | 991 | same |
| parsed | 991 | 991 | same |
| unparsable | 0 | 0 | same |
| `Job(...)` constructions | 582 | 582 | same |
| `Job(...)` constructions — production | 12 | 12 | same |
| `Job(...)` constructions — test | 570 | 570 | same |
| `Job` imports | 345 | 345 | same |
| `Job` imports — production | 47 | 47 | same |
| `Job` imports — test | 298 | 298 | same |
| `Job` annotations | 368 | 368 | same |
| `Job` annotations — production | 151 | 151 | same |
| `Job` annotations — test | 217 | 217 | same |
| the enumeration renders N file lines | 184 | 184 | same |

Rows measured: 23. Reading `same`: 23. Reading `differs`: 0.

Every figure the block carried reproduced exactly at this round's own base.
The union has NOT moved since the block was authored.

## 3. Provably `Job`, but never executed

The `ast` sweep proves these hold a `Job`; the probe never saw one run. They are
in the union and the flip must carry them, but no test exercises them — so if the
flip gets one wrong, nothing goes red. BY PATH AND LINE, in full:

- `packages/orchestration/decision_queue.py:1017` — field `id`
- `packages/orchestration/do_run.py:261` — field `id`
- `packages/orchestration/do_run.py:285` — field `id`
- `packages/orchestration/do_run.py:316` — field `id`
- `packages/orchestration/do_run.py:357` — field `id`
- `tests/orchestration/test_job_fulfillment.py:1087` — field `id`
- `tests/orchestration/test_real_ollama_smoke.py:165` — field `id`
- `tests/orchestration/test_token_economy_integration.py:28` — field `id`

## 4. THE ENUMERATION

One line per file, sorted by path. The numbers are the sorted distinct line
numbers of the UNION set for that file and that field; `-` means that field has
no site in that file.

```
apps/cli/commands/brain.py | id: 57,108,159,235,265,327,430,512 | name: -
apps/cli/commands/context.py | id: 55 | name: -
apps/cli/commands/do_cmd.py | id: 315,325,353,354,380,387,390,396 | name: -
apps/cli/commands/job.py | id: 107,108,113,159,244,276,351,362,412,430,479,483,499,533,547,667,794,810,992,1108,1457,1490,1549,1613,1640,1701,1759,1766,1798,1847,1860 | name: 159,1614,1641,1767,1799
apps/cli/commands/loop_cmd.py | id: 252,259 | name: -
apps/cli/commands/memory.py | id: 313,347,388 | name: -
apps/cli/commands/patch.py | id: 109,138 | name: -
apps/cli/commands/policy.py | id: 42,77 | name: -
apps/cli/commands/project.py | id: 97,198 | name: -
apps/cli/commands/repo.py | id: 178,216,225,230,248 | name: 221,248
apps/cli/commands/review_cmd.py | id: 39,119,153 | name: -
packages/orchestration/agent_loop.py | id: 137,175,202,220,236,259,413 | name: 260
packages/orchestration/approval_queue.py | id: 237 | name: -
packages/orchestration/autonomy_loop.py | id: 61,124 | name: -
packages/orchestration/autonomy_readiness.py | id: 171,379,418,425 | name: -
packages/orchestration/autorun.py | id: 154,156,320,356,370,394,405,500,509,524,530,531,532,560,565,574,586,632,643,695,703 | name: -
packages/orchestration/brain_detail.py | id: 142 | name: 293
packages/orchestration/brain_viewer.py | id: 185,203 | name: -
packages/orchestration/builder_bridge.py | id: 137,165,178,197,236,246,443,452,465,483,489,491,501,510,517,519,530,532 | name: -
packages/orchestration/cockpit.py | id: 80,381,394 | name: 81
packages/orchestration/context_coverage.py | id: 250,254,296 | name: -
packages/orchestration/context_inspector.py | id: 584 | name: -
packages/orchestration/continue_from_node.py | id: 66,70,123,127,140,149 | name: -
packages/orchestration/dashboard.py | id: 31,134 | name: -
packages/orchestration/decision_inbox.py | id: 212 | name: -
packages/orchestration/decision_queue.py | id: 92,1015,1017 | name: -
packages/orchestration/diff_repair_apply.py | id: 155 | name: -
packages/orchestration/do_run.py | id: 242,244,252,261,269,285,305,316,336,342,357,363,411,421,447,460,539 | name: -
packages/orchestration/event_replay.py | id: 349,355,362,374,386 | name: -
packages/orchestration/file_provenance.py | id: 71 | name: -
packages/orchestration/flight_plan.py | id: 835 | name: -
packages/orchestration/guidance.py | id: 42,191,211 | name: -
packages/orchestration/job_digest.py | id: 142 | name: -
packages/orchestration/job_fulfillment.py | id: 536,537 | name: -
packages/orchestration/job_runner.py | id: 79 | name: 68
packages/orchestration/llm_planner.py | id: 64,78,156 | name: 142,152
packages/orchestration/long_run_executor.py | id: 502,504,506,535,579,866,972,1125,1164,1174,1355,1390,1404,1562 | name: -
packages/orchestration/loop_run.py | id: 285 | name: -
packages/orchestration/memory_candidates.py | id: 53,85 | name: -
packages/orchestration/memory_learn.py | id: 48 | name: -
packages/orchestration/mission_state.py | id: 756,1074,1105 | name: -
packages/orchestration/orchestrator_loop.py | id: 1594,1603,1626 | name: -
packages/orchestration/patch_apply.py | id: 203,235,526,530,562,566 | name: -
packages/orchestration/patch_revert.py | id: 88,183,245,249 | name: -
packages/orchestration/project_brain.py | id: 284,304,463,476,501,521,524,642,920,981 | name: 298
packages/orchestration/project_brain_aggregate.py | id: 131,161 | name: -
packages/orchestration/project_context_coverage.py | id: 276 | name: -
packages/orchestration/project_registry.py | id: 856,868 | name: -
packages/orchestration/proof_chain.py | id: 565 | name: 566
packages/orchestration/repo_applicator.py | id: 231 | name: -
packages/orchestration/reviewer.py | id: 129 | name: 82
packages/orchestration/run_contract.py | id: 419,420 | name: -
packages/orchestration/run_report.py | id: 761,790,816,919,1007 | name: 791
packages/orchestration/self_dogfood.py | id: 270 | name: -
packages/orchestration/source_apply.py | id: 266,273 | name: -
packages/orchestration/source_context.py | id: 241 | name: -
packages/orchestration/stop_reasons.py | id: 194 | name: -
packages/orchestration/storage.py | id: 79 | name: -
packages/orchestration/task_runner.py | id: 127,144 | name: -
packages/orchestration/test_execution_service.py | id: 607,608,625,659,712,731,741,754,857,862 | name: -
packages/orchestration/test_failure_artifact.py | id: 131 | name: -
packages/orchestration/timeline.py | id: 108,389 | name: 109
packages/orchestration/token_economy.py | id: 343 | name: -
packages/orchestration/token_policy.py | id: 109 | name: -
packages/orchestration/trust_report.py | id: 79,248,374,455,464,465,471,472,486,487,493,499 | name: 80,93
packages/orchestration/ui_server.py | id: 161,555,563,580,581,588,614,747,772,828,876,1369,1414,1480,1564,1898,2070,2078,2117,2213,3097,3101,3112,3119,3128,3129,3140,3144,3151,3152,3154,3175,3183,3184,3186,3208,3216,3217,3219,3226,3389 | name: 1494
packages/orchestration/ui_view_model.py | id: 292,459,462,523,624,633,838,920,966,990,996,1097,1117 | name: 787,987
packages/orchestration/worker_queue.py | id: 483,488,502 | name: -
tests/cli/test_change_proof_cli.py | id: 81,97,111,130,146,162,178,198,217,264,279 | name: -
tests/cli/test_context_inspect_cli.py | id: 57,73,94,117,128,144,175,188,205 | name: -
tests/cli/test_context_inspect_runtime.py | id: 42,93,101,117,135,154,170,196,213 | name: -
tests/cli/test_decision_answers.py | id: 108,111,125,129,139,142,162,165,180,182,194,200,205,215,217,229,231,241,243,259,263,273,276,289,403 | name: -
tests/cli/test_do_continue_cli.py | id: 37 | name: -
tests/cli/test_file_provenance_cli.py | id: 120,131,139 | name: -
tests/cli/test_golden_path.py | id: 211 | name: 145
tests/cli/test_job_commands.py | id: 237,245,246,257,263,274,292,455 | name: -
tests/cli/test_job_context_cmd.py | id: 114,128,143,155,157,175,176,187,199,219,222 | name: -
tests/cli/test_job_digest_cli.py | id: 73,77,84,88,98,105,108,109,148,151 | name: -
tests/cli/test_job_report.py | id: 62,70,75,81,92,102,104,113,121,123,127,129,142,154,160,166,177,186,196,212,221,227,229,275,288 | name: -
tests/cli/test_loop_cmd.py | id: 173,187,252,263,311 | name: -
tests/cli/test_open_decisions_view.py | id: 176,183,188,190,198,206,216,220,226,229,237,253,257,262,264,272,278,290,303,306,329 | name: -
tests/cli/test_orchestrator_brain_cli.py | id: 26 | name: -
tests/cli/test_patch_cmd.py | id: 120,121,162,167,187,190,204,208,216,223,238,244,255,261,272,284,322,326,336,337,355,356,357 | name: -
tests/cli/test_plan_approval.py | id: 307,389,395,403,409,418 | name: -
tests/cli/test_product_spine.py | id: 515,532,590,607 | name: -
tests/cli/test_real_test_execution_cli.py | id: 23 | name: -
tests/cli/test_repair_request_cli.py | id: 27 | name: -
tests/cli/test_repair_runtime.py | id: 62,68 | name: -
tests/cli/test_repair_v1_cli.py | id: 36,131 | name: -
tests/cli/test_scoped_listings.py | id: - | name: 329
tests/cli/test_self_dogfood_cli.py | id: 26 | name: -
tests/cli/test_self_dogfood_execution_cli.py | id: 34,35,37,38 | name: -
tests/orchestration/test_approval_queue.py | id: 249,269,285,304,310,348,383,409,423,477 | name: -
tests/orchestration/test_autonomy.py | id: 121,282,297,318,351,429 | name: -
tests/orchestration/test_autorun.py | id: 611,630 | name: -
tests/orchestration/test_builder_bridge.py | id: 156 | name: -
tests/orchestration/test_builder_repair_loop.py | id: 252,311,339,376,415,458,558,609 | name: -
tests/orchestration/test_bundled_clarification.py | id: 383 | name: -
tests/orchestration/test_checkpoints.py | id: 147,148,343,351,360,365,366,376,381,397,400,402,404,421 | name: -
tests/orchestration/test_decision_inbox.py | id: 181 | name: -
tests/orchestration/test_do_continue.py | id: 102,224,287,288,302,320,321,406,409,416 | name: -
tests/orchestration/test_dod_gate.py | id: 312,316,321,323,328,333,335,342,344,352,354,356,359,360,364,369,373,378,383,384,387,420,426,428,436,439,441,450,451,453,458,459,461,477,479,480 | name: -
tests/orchestration/test_escalation.py | id: 377,378,390,596,690,694,715,718,733,865,870,878,1004,1007,1023,1027,1108 | name: -
tests/orchestration/test_event_ledger.py | id: 272,274 | name: -
tests/orchestration/test_f018_authority_integration.py | id: 418,440 | name: -
tests/orchestration/test_fence_e2e.py | id: 342,365,1282 | name: -
tests/orchestration/test_fence_production_e2e.py | id: 66,77,85,95,100,106,167,176,184,193,215,222,231,241,251,259,275,284,291,302 | name: -
tests/orchestration/test_job_budgets.py | id: - | name: 136
tests/orchestration/test_job_digest.py | id: 226,361,549 | name: -
tests/orchestration/test_job_fulfillment.py | id: 353,373,385,401,429,495,501,528,534,575,594,624,630,635,636,637,639,695,962,972,985,988,997,1029,1037,1048,1078,1087,1112,1114,1133,1135,1319,1357,1379,1402,1420,1439,1454,1473,1475,1554,1621,1668 | name: -
tests/orchestration/test_long_run_executor.py | id: 128,188,296,310,365,557,589,601,602,618,619,629,633,639,738,766,774,855,877,882,897,1004 | name: -
tests/orchestration/test_loop_run.py | id: 285,340,354,371,384,396,437,508,514 | name: 93
tests/orchestration/test_mission_readiness.py | id: 83,92,93,107,108,116,123,124,128,131,135,143,149,169,177,184,197,200 | name: -
tests/orchestration/test_mission_state.py | id: 420,425,435,437,450,452,578,579,735,805,820,833,834,837,847,863,885 | name: -
tests/orchestration/test_orchestrator_brain.py | id: 54,62,76,94,97,123,127,131,139,141,145,151,152,155,161,181,195,197,201,212,236,255,260 | name: -
tests/orchestration/test_project_brain.py | id: 608,963,973,1063,1064,1067,1068,1072,1073,1074,1082,1083,1354,1451 | name: -
tests/orchestration/test_project_scope.py | id: - | name: 193
tests/orchestration/test_proof_chain.py | id: 1071,1081,1090,1104,1107,1108,1111,1123,1124,1134,1135 | name: -
tests/orchestration/test_real_ollama_smoke.py | id: 165 | name: -
tests/orchestration/test_real_test_execution.py | id: 31 | name: -
tests/orchestration/test_repair_apply_cycle.py | id: 36,50,70,83,94,118,119,143 | name: -
tests/orchestration/test_repair_loop_hardened.py | id: 173,205 | name: -
tests/orchestration/test_repair_loop_v1.py | id: 36,57 | name: -
tests/orchestration/test_repair_request_builder.py | id: 60,63,68,69,71,75,76,96,109,110,115,116,121,122,127,128,133,134,139,140,146,147,173,216,224 | name: -
tests/orchestration/test_resume_cli.py | id: 66,67,76,81,94,99,109,122,134,291,292,320,347,351,425,436 | name: -
tests/orchestration/test_run_contract.py | id: 324,349 | name: -
tests/orchestration/test_run_report_hook.py | id: 77,87,98,103,104,109,119,128,137,140,146,193,217 | name: -
tests/orchestration/test_self_dogfood.py | id: 66,93,101,108,115,116,119,124,126,148,198 | name: -
tests/orchestration/test_self_dogfood_execution.py | id: 56,57,59,71,80,81,83,89,95,109,121,128,129,136,213 | name: -
tests/orchestration/test_self_healing_cycles.py | id: 109,208,278,542,698,704,794,810,819,880 | name: -
tests/orchestration/test_small_repo_fixtures.py | id: 183 | name: -
tests/orchestration/test_source_apply.py | id: 209,225,268,285,288,314,318,341,345,364,368,400,411,438,714 | name: -
tests/orchestration/test_source_context_quality.py | id: 85,107 | name: -
tests/orchestration/test_structured_planner_cli.py | id: 84,92,104,106,113,115,123,137,138,145,146,158,159,171,172,208,209,218,219,228,229,239,240,244,254,255,271,272,284,285 | name: -
tests/orchestration/test_task_execution.py | id: 157,170 | name: -
tests/orchestration/test_test_execution_service.py | id: 525,540,561,577,631,678,732,908 | name: -
tests/orchestration/test_test_failure_repair.py | id: 262,279,304,309,312,332,344,354,368,378,389,390,412,424,427,442,540,556,559,575,576,592,597,610,611,625,626,644,666,667,668,687,701,719,737,757,773,818,830,839,851 | name: -
tests/orchestration/test_token_economy.py | id: 36 | name: -
tests/orchestration/test_token_economy_integration.py | id: 28 | name: -
tests/orchestration/test_watchdog.py | id: 472,493,561,579,592,890,902 | name: -
tests/storage/test_persistence.py | id: 235,284,304,305 | name: -
tests/test_agent_loop.py | id: 151,229,241,249,257,269,270,282,283,297,298,306,317,326,419,436,461,531,544,575,619,708,719,721,752,755,762,764,779,781,803,805,814,816,827 | name: -
tests/test_autonomy_readiness.py | id: 192,282,291,292,302,303,313,325 | name: -
tests/test_brain_detail.py | id: 263,405,419,431,443,462,588,622,684,754,784,795,799,808,812,822,839,841,851,853,878,880,893,911,925 | name: -
tests/test_brain_smoke.py | id: 283,285,295,297,308,317,319,330,331,341,342,344,355,365,367,397,399,404,448,457,464,471,478,506,517,526,533,544,553,575,578,590,593,605,608,620,623,668,678,688,694,706,718,721,728,738,741,761,773,785,798,811 | name: -
tests/test_brain_viewer.py | id: 200,324,381,406,409,418,421,436,437,441,457,458,462,484,499,502,514,529,547,550,631,633,644,658,661,674,677,695,698,713,716,731,750,840,852,855,873,876,923,941,994,1055,1058,1070,1139,1161,1177 | name: -
tests/test_cli_execution_loop_closure.py | id: 187,222,249,317,338,357 | name: -
tests/test_cli_main.py | id: 50,59,68,76,85,86,100,111,119,127,136,145,158,170,206,214,224,225,234,235,257,271,273,285,382,385,488,496,610,612 | name: -
tests/test_cockpit.py | id: 94,153,161,164,176,179,182,217,232,233,243,244,254,255,266,267,278,281,287,299,312,313,363,377,397,419,432,449,456,457,467,468,479,487,488,508,509,527,543,554,591,594,603,631 | name: -
tests/test_context_coverage.py | id: 299,308,321,330,340,351,354,417,453,582,597,613,628,631,643,646,664,667,680,695,698,737,738,739,758,786,811,819,836,844,861,869,891,1008,1033,1034,1035,1108,1119,1129,1153,1163,1173,1194,1201 | name: -
tests/test_execution_foundation.py | id: 244,261,276,291,305 | name: -
tests/test_grouped_cli.py | id: 181,190,198,207,270 | name: -
tests/test_imports.py | id: - | name: 46
tests/test_memory_learn.py | id: 84,146,168,187 | name: -
tests/test_patch_apply.py | id: 217,850,884,893,913,924,940,958,968,978,1016,1030,1060,1077,1162,1173,1184,1528,1538,1547,1566,1576,1585,1597,1724,1735,1746,1772 | name: -
tests/test_patch_intent_approval.py | id: 397,406,430,442,451,461,482,494,503,524,525,534,535,551,559,568,569,577,584,591,599,608,633,634,642,643,658,667,668,669,676,684,691,698,706,713,714,726,727,741,742,759,760,773,774,786,800,801,811,812 | name: -
tests/test_project_brain.py | id: 240,262,280,301,331,379,392,404,414,422,426,436,461,478,530,531,580,602,635,670,738,832,836,845,847,865,867,895,897,908,910,920,925,936,972,989,991,1085,1092,1099,1106,1117,1132,1144,1222,1278,1288,1298,1314,1324,1334 | name: -
tests/test_project_constitution.py | id: 472,479,494,522,525,646,656,665,677,688,697,717,738,754,770,787,804,827 | name: -
tests/test_project_context_coverage.py | id: 215,648,656,677,684,702,707,841 | name: -
tests/test_repair_context_reviewer_memory.py | id: 307 | name: -
tests/test_run_contract.py | id: 95 | name: -
tests/test_run_log_cli.py | id: 114,116,136,138,158,160,182,184,207,209,232,251,253,263,265,276,366,368,503,505,614,616,736,738,863,867,894,896,956,958,971,973,988,990,1005,1007,1045,1047,1067,1069,1089,1091,1112,1114,1138,1140,1159,1161,1179,1181,1205,1207,1226,1228,1248,1250,1271,1273,1291,1293,1331,1333,1403,1405 | name: -
tests/test_runner.py | id: 35 | name: -
tests/test_storage.py | id: 31,33,77,78,128,137,167,185 | name: 34,89,90,129,168
tests/test_task_runner.py | id: 104,630 | name: -
tests/test_test_runner.py | id: 344 | name: -
tests/test_timeline.py | id: 305,352,362,364,377,379,388,395,405,418,430,444,454,457,472,476,479,493,496,508,511,524,527,530,533,536,542,554,557,560,573,576,578,581,583,586,597,600,602,605,607,610,624,627,629,632,634,637,651,661,664,666,678,718,724,727,739,742,745,783,787,791,797,801,813,824,848,852 | name: -
tests/test_token_policy.py | id: 80 | name: -
tests/test_trust_report.py | id: 126,222,230,238,240,249,259,270,283,298,360,368,376,378,381,430,432,444,539,574,623,685,688,695,723 | name: -
tests/test_verifier.py | id: 58,294,373 | name: -
tests/test_workspace.py | id: 155,164,173,183,196,206,222,233,393,412,430,446,457,473,491,510,525,593 | name: -
tests/ui_contracts/test_graph_architecture.py | id: 127 | name: -
tests/ui_contracts/test_responsive.py | id: 87,161,416,437,455,492 | name: -
tests/ui_contracts/test_ux_quality.py | id: 181,867,885,951,971,983,996,1027,1041 | name: -
tests/ui_server/test_auth_redaction.py | id: 37 | name: -
tests/ui_server/test_brain_view_model.py | id: 476,488,489,495,502 | name: -
tests/ui_server/test_command_channel.py | id: 75,490,776 | name: -
tests/ui_server/test_command_dispatch.py | id: 77,171,200,221,239,295,351 | name: -
tests/ui_server/test_dashboard_contract.py | id: 99,118,170 | name: -
tests/ui_server/test_decisions_endpoint.py | id: 38 | name: -
tests/ui_server/test_diff_endpoint.py | id: 65,279 | name: -
tests/ui_server/test_digest_route.py | id: 60 | name: -
tests/ui_server/test_live_state.py | id: 130 | name: -
tests/ui_server/test_server_concurrency.py | id: 44 | name: -
```

## 5. What this reading does NOT settle

THE UNION IS A FLOOR, NOT A CEILING. Each instrument is blind where the other
sees, and neither covers the overlap of the two blindnesses: the probe records
only what a test run EXECUTES, and the `ast` sweep records only what it can PROVE
holds a `Job` — from a parameter annotation, an `AnnAssign`, or an assignment
from a `Job(...)` call. A site that is BOTH never executed AND not statically
provable is invisible to both instruments and is therefore absent from every
count above.

That remainder is given NO numeral, because none was measured. The sweep did
record 4288 `.id`/`.name` attribute sites whose receiver it could not decide, and
293 it decided were not a `Job` at all. The first of those
bounds nothing useful — most of its members are plainly not jobs — so quoting it
as the remainder would be a guess wearing a digit, and it is not quoted as one.

The flip round applies section 4 and then re-runs both instruments: the honest
check on a floor is that the same measurement, taken again after the change,
reports zero surviving sites of the old spelling.
