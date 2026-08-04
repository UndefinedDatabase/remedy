# Gauntlet matrix — recorded

5/9 runs flawless · **NOT A PASS**

| run | order | kind | terminal | flawless | interventions | wall | tokens in/out |
| --- | --- | --- | --- | --- | --- | --- | --- |
| run-01-flawless-pure-code | fx-01-pure-code-change | pure_code_change | achieved | yes | 0 | 612.5s | 121400/28900 |
| run-02-operator-command | fx-02-operator-command | test_add | achieved | NO | 1 | 744.0s | 98200/21050 |
| run-03-unknown-postmortem | fx-03-unknown-postmortem | small_app_feature | achieved | NO | 0 | 1180.2s | 204600/47300 |
| run-04-injection-provider-api-error | fx-04-provider-api-error-mid-move | pure_code_change | achieved | yes | 0 | 803.8s | 133900/30400 |
| run-05-injection-truncated-response | fx-05-truncated-model-response | doc_generation | achieved | yes | 0 | 512.0s | 76500/19800 |
| run-06-injection-death-mid-dispatch | fx-06-harness-death-mid-dispatch | test_add | achieved | yes | 0 | 968.5s | 148300/33100 |
| run-07-injection-death-mid-write | fx-07-harness-death-mid-write | two_milestone_mission | achieved | yes | 0 | 2410.0s | 388700/91200 |
| run-08-injection-silent-success | fx-08-truncated-response-silent-success | small_app_feature | achieved | NO | 0 | 690.0s | 112700/26400 |
| run-09-injection-corrupted-artifact | fx-09-harness-death-corrupted-artifact | doc_generation | achieved | NO | 0 | 585.5s | 88100/20900 |

Failure kinds present: operator_intervention, unknown_postmortem, injection_not_degraded

## Runs

### run-01-flawless-pure-code — fx-01-pure-code-change

- Flawless: **yes**
- Terminal: achieved
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 612.5s · 121400 in / 28900 out

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
| unit_tests | command | yes | green | - | 41200ms |

Evidence:

- ledger: `run-01-flawless-pure-code/ledger.jsonl`
- report: `run-01-flawless-pure-code/report.md`

### run-02-operator-command — fx-02-operator-command

- Flawless: **NO**
- Terminal: achieved
- Operator interventions: 1
  - `remedy job resume 4f1c9a`
- Postmortem classes: none
- Wall / tokens: 744.0s · 98200 in / 21050 out

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | NO |
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
| unit_tests | command | yes | green | - | 41200ms |

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| operator_intervention | start_command_only | - | - | operator intervened after start: remedy job resume 4f1c9a |

Evidence:

- ledger: `run-02-operator-command/ledger.jsonl`
- report: `run-02-operator-command/report.md`

### run-03-unknown-postmortem — fx-03-unknown-postmortem

- Flawless: **NO**
- Terminal: achieved
- Operator interventions: 0
- Postmortem classes: unknown
- Wall / tokens: 1180.2s · 204600 in / 47300 out

Criteria:

| criterion | held |
| --- | --- |
| evidence_well_formed | yes |
| start_command_only | yes |
| terminal_green | yes |
| dod_blocking_green | yes |
| no_unknown_postmortems | NO |
| no_open_decisions | yes |
| host_data_root_untouched | yes |
| no_era_defect_classes | yes |
| injections_degraded | yes |

DoD matrix:

| check | kind | blocking | status | reason | duration |
| --- | --- | --- | --- | --- | --- |
| unit_tests | command | yes | green | - | 41200ms |

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| unknown_postmortem | no_unknown_postmortems | - | - | postmortem (task) has failure class unknown — the failure was not understood |

Evidence:

- ledger: `run-03-unknown-postmortem/ledger.jsonl`
- report: `run-03-unknown-postmortem/report.md`

### run-04-injection-provider-api-error — fx-04-provider-api-error-mid-move

- Flawless: **yes**
- Terminal: achieved
- Operator interventions: 0
- Postmortem classes: provider_unavailable
- Wall / tokens: 803.8s · 133900 in / 30400 out

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
| unit_tests | command | yes | green | - | 41200ms |

Evidence:

- ledger: `run-04-injection-provider-api-error/ledger.jsonl`
- report: `run-04-injection-provider-api-error/report.md`

### run-05-injection-truncated-response — fx-05-truncated-model-response

- Flawless: **yes**
- Terminal: achieved
- Operator interventions: 0
- Postmortem classes: parse
- Wall / tokens: 512.0s · 76500 in / 19800 out

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
| unit_tests | command | yes | green | - | 41200ms |

Evidence:

- ledger: `run-05-injection-truncated-response/ledger.jsonl`
- report: `run-05-injection-truncated-response/report.md`

### run-06-injection-death-mid-dispatch — fx-06-harness-death-mid-dispatch

- Flawless: **yes**
- Terminal: achieved
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 968.5s · 148300 in / 33100 out

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
| unit_tests | command | yes | green | - | 41200ms |

Evidence:

- ledger: `run-06-injection-death-mid-dispatch/ledger.jsonl`
- report: `run-06-injection-death-mid-dispatch/report.md`

### run-07-injection-death-mid-write — fx-07-harness-death-mid-write

- Flawless: **yes**
- Terminal: achieved
- Operator interventions: 0
- Postmortem classes: stopped
- Wall / tokens: 2410.0s · 388700 in / 91200 out

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
| unit_tests | command | yes | green | - | 41200ms |

Evidence:

- ledger: `run-07-injection-death-mid-write/ledger.jsonl`
- report: `run-07-injection-death-mid-write/report.md`

### run-08-injection-silent-success — fx-08-truncated-response-silent-success

- Flawless: **NO**
- Terminal: achieved
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 690.0s · 112700 in / 26400 out

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
| injections_degraded | NO |

DoD matrix:

| check | kind | blocking | status | reason | duration |
| --- | --- | --- | --- | --- | --- |
| unit_tests | command | yes | green | - | 41200ms |

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| injection_not_degraded | injections_degraded | - | truncated_model_response | truncated_model_response ended as silent_success — a named mishandling; expected one of ledgered_failure/retry_within_budget/escalated; recorded: truncated move accepted as a complete move; the milestone was declared done from half a payload |

Evidence:

- ledger: `run-08-injection-silent-success/ledger.jsonl`
- report: `run-08-injection-silent-success/report.md`

### run-09-injection-corrupted-artifact — fx-09-harness-death-corrupted-artifact

- Flawless: **NO**
- Terminal: achieved
- Operator interventions: 0
- Postmortem classes: none
- Wall / tokens: 585.5s · 88100 in / 20900 out

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
| injections_degraded | NO |

DoD matrix:

| check | kind | blocking | status | reason | duration |
| --- | --- | --- | --- | --- | --- |
| unit_tests | command | yes | green | - | 41200ms |

Failures:

| kind | criterion | finding class | injection class | detail |
| --- | --- | --- | --- | --- |
| injection_not_degraded | injections_degraded | - | harness_death_mid_write | harness_death_mid_write ended as corrupted_artifact_accepted — a named mishandling; expected one of ledgered_failure/retry_within_budget/escalated; recorded: the half-written dossier was read back without verifying its digest and passed to the next iteration |

Evidence:

- ledger: `run-09-injection-corrupted-artifact/ledger.jsonl`
- report: `run-09-injection-corrupted-artifact/report.md`
