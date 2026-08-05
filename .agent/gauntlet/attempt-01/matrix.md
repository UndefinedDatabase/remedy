# Gauntlet matrix — gauntlet-attempt-01

0/10 runs flawless · **NOT A PASS**

| run | order | kind | terminal | flawless | interventions | wall | tokens in/out |
| --- | --- | --- | --- | --- | --- | --- | --- |
| run-01-g01-pure-code-change | g01-pure-code-change | pure_code_change | iteration_limit | NO | 0 | 323.9s | 0/0 |
| run-02-g02-test-add | g02-test-add | test_add | iteration_limit | NO | 0 | 420.4s | 0/0 |
| run-03-g03-small-app-feature-smoke | g03-small-app-feature-smoke | small_app_feature_with_smoke | iteration_limit | NO | 0 | 229.1s | 0/0 |
| run-04-g04-doc-generation | g04-doc-generation | doc_generation | iteration_limit | NO | 0 | 495.6s | 0/0 |
| run-05-g05-two-milestone-mission | g05-two-milestone-mission | two_milestone_mission | iteration_limit | NO | 0 | 273.2s | 0/0 |
| run-06-g06-provider-api-error-mid-move | g06-provider-api-error-mid-move | pure_code_change | iteration_failed | NO | 0 | 211.9s | 0/0 |
| run-07-g07-truncated-model-response | g07-truncated-model-response | test_add | iteration_limit | NO | 0 | 587.9s | 0/0 |
| run-08-g08-harness-death-mid-dispatch | g08-harness-death-mid-dispatch | small_app_feature_with_smoke | iteration_failed | NO | 0 | 377.9s | 0/0 |
| run-09-g09-harness-death-mid-write | g09-harness-death-mid-write | two_milestone_mission | iteration_failed | NO | 0 | 151.1s | 0/0 |
| run-10-g10-escalate-then-finish | g10-escalate-then-finish | doc_generation | iteration_limit | NO | 0 | 734.4s | 0/0 |

Failure kinds present: terminal_not_green, dod_blocking_red, unknown_postmortem

## Runs

### run-01-g01-pure-code-change — g01-pure-code-change

- Flawless: **NO**
- Terminal: iteration_limit
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 323.9s · 0 in / 0 out

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | NO |
| dod_blocking_green | NO |
| no_unknown_postmortems | yes |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

No Definition of Done was run for this job.

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| terminal_not_green | terminal_green | - | - | terminal status iteration_limit is not achieved |
| dod_blocking_red | dod_blocking_green | - | - | no dod_result.json: the DoD gate never produced a verdict |

Evidence:

- isolated_root: `run-01-g01-pure-code-change/data`
- ledger: `run-01-g01-pure-code-change/data/missions`

### run-02-g02-test-add — g02-test-add

- Flawless: **NO**
- Terminal: iteration_limit
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 420.4s · 0 in / 0 out

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | NO |
| dod_blocking_green | NO |
| no_unknown_postmortems | yes |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

No Definition of Done was run for this job.

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| terminal_not_green | terminal_green | - | - | terminal status iteration_limit is not achieved |
| dod_blocking_red | dod_blocking_green | - | - | no dod_result.json: the DoD gate never produced a verdict |

Evidence:

- isolated_root: `run-02-g02-test-add/data`
- ledger: `run-02-g02-test-add/data/missions`

### run-03-g03-small-app-feature-smoke — g03-small-app-feature-smoke

- Flawless: **NO**
- Terminal: iteration_limit
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 229.1s · 0 in / 0 out

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | NO |
| dod_blocking_green | NO |
| no_unknown_postmortems | yes |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

No Definition of Done was run for this job.

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| terminal_not_green | terminal_green | - | - | terminal status iteration_limit is not achieved |
| dod_blocking_red | dod_blocking_green | - | - | no dod_result.json: the DoD gate never produced a verdict |

Evidence:

- isolated_root: `run-03-g03-small-app-feature-smoke/data`
- ledger: `run-03-g03-small-app-feature-smoke/data/missions`

### run-04-g04-doc-generation — g04-doc-generation

- Flawless: **NO**
- Terminal: iteration_limit
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 495.6s · 0 in / 0 out

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | NO |
| dod_blocking_green | NO |
| no_unknown_postmortems | yes |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

No Definition of Done was run for this job.

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| terminal_not_green | terminal_green | - | - | terminal status iteration_limit is not achieved |
| dod_blocking_red | dod_blocking_green | - | - | no dod_result.json: the DoD gate never produced a verdict |

Evidence:

- isolated_root: `run-04-g04-doc-generation/data`
- ledger: `run-04-g04-doc-generation/data/missions`

### run-05-g05-two-milestone-mission — g05-two-milestone-mission

- Flawless: **NO**
- Terminal: iteration_limit
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 273.2s · 0 in / 0 out

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | NO |
| dod_blocking_green | NO |
| no_unknown_postmortems | yes |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

No Definition of Done was run for this job.

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| terminal_not_green | terminal_green | - | - | terminal status iteration_limit is not achieved |
| dod_blocking_red | dod_blocking_green | - | - | no dod_result.json: the DoD gate never produced a verdict |

Evidence:

- isolated_root: `run-05-g05-two-milestone-mission/data`
- ledger: `run-05-g05-two-milestone-mission/data/missions`

### run-06-g06-provider-api-error-mid-move — g06-provider-api-error-mid-move

- Flawless: **NO**
- Terminal: iteration_failed
- Operator interventions: 0
- Postmortem classes: unknown
- Wall / tokens: 211.9s · 0 in / 0 out

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | NO |
| dod_blocking_green | NO |
| no_unknown_postmortems | NO |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

No Definition of Done was run for this job.

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| terminal_not_green | terminal_green | - | - | terminal status iteration_failed is not achieved |
| dod_blocking_red | dod_blocking_green | - | - | no dod_result.json: the DoD gate never produced a verdict |
| unknown_postmortem | no_unknown_postmortems | - | - | postmortem (job) has failure class unknown — the failure was not understood |

Evidence:

- isolated_root: `run-06-g06-provider-api-error-mid-move/data`
- ledger: `run-06-g06-provider-api-error-mid-move/data/missions`

### run-07-g07-truncated-model-response — g07-truncated-model-response

- Flawless: **NO**
- Terminal: iteration_limit
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 587.9s · 0 in / 0 out

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | NO |
| dod_blocking_green | NO |
| no_unknown_postmortems | yes |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

No Definition of Done was run for this job.

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| terminal_not_green | terminal_green | - | - | terminal status iteration_limit is not achieved |
| dod_blocking_red | dod_blocking_green | - | - | no dod_result.json: the DoD gate never produced a verdict |

Evidence:

- isolated_root: `run-07-g07-truncated-model-response/data`
- ledger: `run-07-g07-truncated-model-response/data/missions`

### run-08-g08-harness-death-mid-dispatch — g08-harness-death-mid-dispatch

- Flawless: **NO**
- Terminal: iteration_failed
- Operator interventions: 0
- Postmortem classes: unknown
- Wall / tokens: 377.9s · 0 in / 0 out

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | NO |
| dod_blocking_green | NO |
| no_unknown_postmortems | NO |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

No Definition of Done was run for this job.

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| terminal_not_green | terminal_green | - | - | terminal status iteration_failed is not achieved |
| dod_blocking_red | dod_blocking_green | - | - | no dod_result.json: the DoD gate never produced a verdict |
| unknown_postmortem | no_unknown_postmortems | - | - | postmortem (job) has failure class unknown — the failure was not understood |

Evidence:

- isolated_root: `run-08-g08-harness-death-mid-dispatch/data`
- ledger: `run-08-g08-harness-death-mid-dispatch/data/missions`

### run-09-g09-harness-death-mid-write — g09-harness-death-mid-write

- Flawless: **NO**
- Terminal: iteration_failed
- Operator interventions: 0
- Postmortem classes: unknown
- Wall / tokens: 151.1s · 0 in / 0 out

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | NO |
| dod_blocking_green | NO |
| no_unknown_postmortems | NO |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

No Definition of Done was run for this job.

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| terminal_not_green | terminal_green | - | - | terminal status iteration_failed is not achieved |
| dod_blocking_red | dod_blocking_green | - | - | no dod_result.json: the DoD gate never produced a verdict |
| unknown_postmortem | no_unknown_postmortems | - | - | postmortem (job) has failure class unknown — the failure was not understood |

Evidence:

- isolated_root: `run-09-g09-harness-death-mid-write/data`
- ledger: `run-09-g09-harness-death-mid-write/data/missions`

### run-10-g10-escalate-then-finish — g10-escalate-then-finish

- Flawless: **NO**
- Terminal: iteration_limit
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 734.4s · 0 in / 0 out

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | NO |
| dod_blocking_green | NO |
| no_unknown_postmortems | yes |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

No Definition of Done was run for this job.

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| terminal_not_green | terminal_green | - | - | terminal status iteration_limit is not achieved |
| dod_blocking_red | dod_blocking_green | - | - | no dod_result.json: the DoD gate never produced a verdict |

Evidence:

- isolated_root: `run-10-g10-escalate-then-finish/data`
- ledger: `run-10-g10-escalate-then-finish/data/missions`
