# Gauntlet matrix — attempt-02

3/10 runs flawless · **NOT A PASS**

| run | order | kind | terminal | flawless | interventions | wall | tokens in/out |
| --- | --- | --- | --- | --- | --- | --- | --- |
| run-01-g01-pure-code-change | g01-pure-code-change | pure_code_change | achieved | yes | 0 | 403.6s | unmeasured |
| run-02-g02-test-add | g02-test-add | test_add | iteration_limit | NO | 0 | 903.5s | unmeasured |
| run-03-g03-small-app-feature-smoke | g03-small-app-feature-smoke | small_app_feature_with_smoke | iteration_limit | NO | 0 | 658.3s | unmeasured |
| run-04-g04-doc-generation | g04-doc-generation | doc_generation | iteration_limit | NO | 0 | 700.4s | unmeasured |
| run-05-g05-two-milestone-mission | g05-two-milestone-mission | two_milestone_mission | achieved | yes | 0 | 289.3s | unmeasured |
| run-06-g06-provider-api-error-mid-move | g06-provider-api-error-mid-move | pure_code_change | iteration_failed | NO | 0 | 335.7s | unmeasured |
| run-07-g07-truncated-model-response | g07-truncated-model-response | test_add | achieved | yes | 0 | 652.9s | unmeasured |
| run-08-g08-harness-death-mid-dispatch | g08-harness-death-mid-dispatch | small_app_feature_with_smoke | iteration_failed | NO | 0 | 274.4s | unmeasured |
| run-09-g09-harness-death-mid-write | g09-harness-death-mid-write | two_milestone_mission | iteration_failed | NO | 0 | 173.9s | unmeasured |
| run-10-g10-escalate-then-finish | g10-escalate-then-finish | doc_generation | iteration_limit | NO | 0 | 931.5s | unmeasured |

Failure kinds present: terminal_not_green, dod_blocking_red

## Runs

### run-01-g01-pure-code-change — g01-pure-code-change

- Flawless: **yes**
- Terminal: achieved
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 403.6s · tokens unmeasured

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | yes |
| dod_blocking_green | yes |
| no_unknown_postmortems | yes |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

| check | kind | blocking | status | reason | duration |
| --- | --- | --- | --- | --- | --- |
| acc-001 | pytest | yes | passed | - | 197ms |

Evidence:

- isolated_root: `run-01-g01-pure-code-change/data`
- ledger: `run-01-g01-pure-code-change/data/missions`

### run-02-g02-test-add — g02-test-add

- Flawless: **NO**
- Terminal: iteration_limit
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 903.5s · tokens unmeasured

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | NO |
| dod_blocking_green | yes |
| no_unknown_postmortems | yes |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

| check | kind | blocking | status | reason | duration |
| --- | --- | --- | --- | --- | --- |
| acc-001 | pytest | yes | passed | - | 205ms |

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| terminal_not_green | terminal_green | - | - | terminal status iteration_limit is not achieved |

Evidence:

- isolated_root: `run-02-g02-test-add/data`
- ledger: `run-02-g02-test-add/data/missions`

### run-03-g03-small-app-feature-smoke — g03-small-app-feature-smoke

- Flawless: **NO**
- Terminal: iteration_limit
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 658.3s · tokens unmeasured

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | NO |
| dod_blocking_green | yes |
| no_unknown_postmortems | yes |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

| check | kind | blocking | status | reason | duration |
| --- | --- | --- | --- | --- | --- |
| acc-001 | pytest | yes | passed | - | 195ms |

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| terminal_not_green | terminal_green | - | - | terminal status iteration_limit is not achieved |

Evidence:

- isolated_root: `run-03-g03-small-app-feature-smoke/data`
- ledger: `run-03-g03-small-app-feature-smoke/data/missions`

### run-04-g04-doc-generation — g04-doc-generation

- Flawless: **NO**
- Terminal: iteration_limit
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 700.4s · tokens unmeasured

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | NO |
| dod_blocking_green | yes |
| no_unknown_postmortems | yes |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

| check | kind | blocking | status | reason | duration |
| --- | --- | --- | --- | --- | --- |
| acc-001 | pytest | yes | passed | - | 200ms |

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| terminal_not_green | terminal_green | - | - | terminal status iteration_limit is not achieved |

Evidence:

- isolated_root: `run-04-g04-doc-generation/data`
- ledger: `run-04-g04-doc-generation/data/missions`

### run-05-g05-two-milestone-mission — g05-two-milestone-mission

- Flawless: **yes**
- Terminal: achieved
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 289.3s · tokens unmeasured

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | yes |
| dod_blocking_green | yes |
| no_unknown_postmortems | yes |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

| check | kind | blocking | status | reason | duration |
| --- | --- | --- | --- | --- | --- |
| acc-001 | pytest | yes | passed | - | 196ms |

Evidence:

- isolated_root: `run-05-g05-two-milestone-mission/data`
- ledger: `run-05-g05-two-milestone-mission/data/missions`

### run-06-g06-provider-api-error-mid-move — g06-provider-api-error-mid-move

- Flawless: **NO**
- Terminal: iteration_failed
- Operator interventions: 0
- Postmortem classes: provider_unavailable
- Wall / tokens: 335.7s · tokens unmeasured

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
| terminal_not_green | terminal_green | - | - | terminal status iteration_failed is not achieved |
| dod_blocking_red | dod_blocking_green | - | - | no dod_result.json: the DoD gate never produced a verdict |

Evidence:

- isolated_root: `run-06-g06-provider-api-error-mid-move/data`
- ledger: `run-06-g06-provider-api-error-mid-move/data/missions`

### run-07-g07-truncated-model-response — g07-truncated-model-response

- Flawless: **yes**
- Terminal: achieved
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 652.9s · tokens unmeasured

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | yes |
| dod_blocking_green | yes |
| no_unknown_postmortems | yes |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

| check | kind | blocking | status | reason | duration |
| --- | --- | --- | --- | --- | --- |
| acc-001 | pytest | yes | passed | - | 206ms |

Evidence:

- isolated_root: `run-07-g07-truncated-model-response/data`
- ledger: `run-07-g07-truncated-model-response/data/missions`

### run-08-g08-harness-death-mid-dispatch — g08-harness-death-mid-dispatch

- Flawless: **NO**
- Terminal: iteration_failed
- Operator interventions: 0
- Postmortem classes: io_failure
- Wall / tokens: 274.4s · tokens unmeasured

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
| terminal_not_green | terminal_green | - | - | terminal status iteration_failed is not achieved |
| dod_blocking_red | dod_blocking_green | - | - | no dod_result.json: the DoD gate never produced a verdict |

Evidence:

- isolated_root: `run-08-g08-harness-death-mid-dispatch/data`
- ledger: `run-08-g08-harness-death-mid-dispatch/data/missions`

### run-09-g09-harness-death-mid-write — g09-harness-death-mid-write

- Flawless: **NO**
- Terminal: iteration_failed
- Operator interventions: 0
- Postmortem classes: io_failure
- Wall / tokens: 173.9s · tokens unmeasured

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
| terminal_not_green | terminal_green | - | - | terminal status iteration_failed is not achieved |
| dod_blocking_red | dod_blocking_green | - | - | no dod_result.json: the DoD gate never produced a verdict |

Evidence:

- isolated_root: `run-09-g09-harness-death-mid-write/data`
- ledger: `run-09-g09-harness-death-mid-write/data/missions`

### run-10-g10-escalate-then-finish — g10-escalate-then-finish

- Flawless: **NO**
- Terminal: iteration_limit
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 931.5s · tokens unmeasured

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | NO |
| dod_blocking_green | yes |
| no_unknown_postmortems | yes |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

| check | kind | blocking | status | reason | duration |
| --- | --- | --- | --- | --- | --- |
| acc-001 | pytest | yes | passed | - | 195ms |

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| terminal_not_green | terminal_green | - | - | terminal status iteration_limit is not achieved |

Evidence:

- isolated_root: `run-10-g10-escalate-then-finish/data`
- ledger: `run-10-g10-escalate-then-finish/data/missions`
