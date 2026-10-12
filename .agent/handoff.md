# Handoff — UI external host links

## State
Feature: UI external host links
Round: implementation
Branch: feature/ui-external-host-links
Last commit SHA: 90bc63cba (`allow cockpit LAN access`)
Pull request: #331 https://github.com/UndefinedDatabase/remedy/pull/331
Changed files: `.agent/context.md`, `.agent/decisions.md`, `.agent/handoff.md`, `.agent/plan.md`, `apps/cli/command_catalog.py`, `apps/cli/commands/ui.py`, `docs/guides/environment.md`, `docs/system/architecture.md`, `docs/system/operator-cockpit-v1.md`, `packages/orchestration/config.py`, `packages/orchestration/ui_server.py`, `tests/regression/test_named_bugs.py`, `tests/ui_server/test_dashboard_contract.py`, `tests/ui_server/test_live_state.py`

## Item Status
| Item | Status | Reason |
|---|---|---|
| UI external host links | done | CLI default asks for LAN-capable bind, loopback URL remains primary, LAN HTTP URLs are recorded, loopback-only remains available with `--host 127.0.0.1`. |

## Verification
- `python3 -m py_compile packages/orchestration/ui_server.py packages/orchestration/config.py apps/cli/commands/ui.py apps/cli/command_catalog.py` — pass.
- `scripts/remedy_pytest.sh tests/ui_server/test_dashboard_contract.py::TestUIServer tests/ui_server/test_dashboard_contract.py::TestJobSummaryCommandContract::test_ui_external_bind_is_named_and_token_gated tests/ui_server/test_dashboard_contract.py::TestJobSummaryCommandContract::test_ui_server_keeps_loopback_url tests/ui_server/test_live_state.py::TestUIServerIntegration::test_server_starts_and_writes_info tests/ui_server/test_live_state.py::TestUIServerIntegration::test_url_keeps_loopback_as_primary tests/ui_server/test_live_state.py::TestUIStartAnswersTheEnvelope::test_ui_start_json_answers_the_envelope tests/ui_server/test_live_state.py::TestServerPrefersReactDistLocalhostOnly::test_server_localhost_only tests/regression/test_named_bugs.py::TestSmokeSafety::test_ui_server_external_host_preserves_loopback_url tests/regression/test_named_bugs.py::TestSmokeOriginCheckAndUnload::test_no_bind_all_interfaces tests/regression/test_named_bugs.py::TestDevStatusCommandSchema::test_no_0000_binding tests/orchestration/test_autonomy.py::TestMutationExecutionSafetyInvariants::test_no_0000_bind tests/orchestration/test_test_runner.py::TestNoBroadExceptAndDegradedSignals::test_no_0000_in_production tests/docs/test_environment_guide.py` — 23 passed in 1.40s.
Full pytest: not run.

## Deviations
HTTPS is not implemented; the change is HTTP on the same cockpit port. TLS/certificate support would be a separate feature.

## Next Expected Action
Review PR #331; merge only through the next Open PR Gate.
