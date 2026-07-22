"""
Run Contract v1 — deterministic execution-boundary definition for a Remedy job.

A RunContract describes what a run is allowed and not allowed to do.
It is an execution boundary, not a capability promise.

Provider-neutral: no model names, no network calls, no shell execution,
no external processes.  Pure data contract only.

Public API::

    build_default_run_contract(job) -> RunContract
    evaluate_run_action(contract, action, ...) -> RunActionDecision
    export_run_contract_json(contract) -> dict[str, Any]
    summarize_run_contract(contract) -> str
    save_contract(job, contract) -> None
    load_contract(job) -> RunContract | None
    ensure_contract(job) -> RunContract
    validate_run_contract(contract) -> list[str]
    save_usage(job, usage) -> None
    load_usage(job) -> RunUsage
    check_budget(contract, usage) -> RunBudgetStatus
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from packages.core.models import Job

# ---------------------------------------------------------------------------
# Canonical action vocabulary (Step 1068)
# ---------------------------------------------------------------------------


class ContractAction:
    """Canonical action names used in RunContract allowed/denied lists.

    Not an enum — plain string constants for easy JSON serialization.
    """

    # Safe read/write actions
    PLAN = "plan"
    CONTEXT = "context"
    BUILD_ARTIFACT = "build_artifact"
    CREATE_PATCH_INTENT = "create_patch_intent"
    DISCOVER_COMMANDS = "discover_commands"
    WRITE_METADATA = "write_metadata"
    CREATE_FIX_TASK = "create_fix_task"
    # Repair Loop v1 metadata actions (Step 1204) — safe, allowed by default.
    CREATE_REPAIR_ARTIFACT = "create_repair_artifact"
    CREATE_REPAIR_PATCH_INTENT = "create_repair_patch_intent"
    # Provider Trust Gate v0 (Step 1321) — metadata-level intake of UNTRUSTED
    # external output. These are NOT provider execution (that stays CLOUD_PROVIDER,
    # denied by no_cloud). Allowed by default; create the intent still needs approval.
    PROVIDER_INTAKE = "provider_intake"
    PROVIDER_TRUST_REVIEW = "provider_trust_review"
    PROVIDER_MATERIALIZE_PATCH = "provider_materialize_patch"
    CREATE_PROVIDER_REPAIR_INTENT = "create_provider_repair_intent"
    # Provider Trust Verification v1 (Step 1553) — second-stage SAFE verification of an
    # already-quarantined candidate. NOT provider execution (that stays CLOUD_PROVIDER).
    # verify is metadata-only; verification-show is read-only. Allowed by default; never
    # applies/approves/tests/creates PRs.
    PROVIDER_VERIFY_CANDIDATE = "provider_verify_candidate"
    PROVIDER_VERIFICATION_SHOW = "provider_verification_show"
    # Expensive Builder Routing v0 (Step 1587) — routing/policy/planning ONLY. NOT builder/
    # provider/model execution and NOT candidate generation. decide is metadata-only (persists
    # a safe trace); report is read-only. Allowed by default.
    BUILDER_ROUTING_DECIDE = "builder_routing_decide"
    BUILDER_ROUTING_REPORT = "builder_routing_report"
    # Automated Local Candidate Generator v0 (Step 1618) — LOOPBACK-only local model candidate
    # generation, routing-gated, output goes through Trust Gate + Verification. NOT cloud/external
    # builder execution (distinct from CLOUD_PROVIDER). status read-only; generate metadata-only
    # (the model call is local loopback; no apply/approve). Allowed by default; the real switch is
    # the disabled-by-default generator config + the routing gate.
    LOCAL_CANDIDATE_GENERATOR_STATUS = "local_candidate_generator_status"
    LOCAL_CANDIDATE_GENERATE = "local_candidate_generate"
    # Local Candidate Quality Evaluation v1 (Step 1660) — evidence-based scoring / reporting /
    # routing-feedback ONLY. NOT generation/model/provider/apply/test. evaluate is metadata-only;
    # show/scorecard/report are read-only. Allowed by default.
    CANDIDATE_QUALITY_EVALUATE = "candidate_quality_evaluate"
    CANDIDATE_QUALITY_SHOW = "candidate_quality_show"
    CANDIDATE_QUALITY_SCORECARD = "candidate_quality_scorecard"
    CANDIDATE_QUALITY_REPORT = "candidate_quality_report"
    # External Builder Sandbox v0 (Step 1694) — UNTRUSTED external candidate INGRESS only. NOT
    # external execution / provider / model / apply / test. package-create/submit are metadata/
    # quarantine-write; show/list/report are read-only. The submitted candidate goes through the
    # existing Trust Gate + Verification + (human) approval; this never applies/approves.
    EXTERNAL_BUILDER_PACKAGE = "external_builder_package"
    EXTERNAL_BUILDER_SUBMIT = "external_builder_submit"
    EXTERNAL_BUILDER_SHOW = "external_builder_show"
    # Worker Registry + User-Selectable Route Policy v0 (Step 1726) — METADATA + POLICY only. NOT
    # worker/provider/model/Ollama/cloud execution. worker-registry-show / route-policy-show /
    # route-policy-evaluate are read-only; route-policy-set is metadata-only (persists a safe
    # per-job policy). None of these ever execute a worker, start work, or call a provider.
    WORKER_REGISTRY_SHOW = "worker_registry_show"
    ROUTE_POLICY_SHOW = "route_policy_show"
    ROUTE_POLICY_SET = "route_policy_set"
    ROUTE_POLICY_EVALUATE = "route_policy_evaluate"
    # Token Economy + Context Budget Optimizer v0 (Step 1766) — ESTIMATES + METADATA only. NOT
    # provider/model/Ollama/cloud execution, NOT real pricing. budget-show/estimate/economy-report
    # and context-pack-recommend are read-only; budget-set is metadata-only (persists a safe per-job
    # budget profile). None execute a worker, start work, or call a provider.
    TOKEN_BUDGET_SHOW = "token_budget_show"
    TOKEN_BUDGET_SET = "token_budget_set"
    TOKEN_ESTIMATE = "token_estimate"
    TOKEN_ECONOMY_REPORT = "token_economy_report"
    CONTEXT_PACK_RECOMMEND = "context_pack_recommend"
    # Model/Route Tournament Harness v0 (Step 1807) — EVIDENCE + SCORING + REPORTING only. NOT
    # provider/model/Ollama/cloud execution, NOT candidate generation, NOT worker/tournament
    # execution. tournament-report writes a safe metadata report; show/list/integrity are read-only.
    # None execute a worker, run a tournament, start work, or call a provider.
    TOURNAMENT_REPORT = "tournament_report"
    TOURNAMENT_SHOW = "tournament_show"
    TOURNAMENT_LIST = "tournament_list"
    TOURNAMENT_INTEGRITY = "tournament_integrity"
    # Overnight Mission Contract + Review/Repair Spine v0 (Step 1851) — METADATA + STATE-MACHINE +
    # EVALUATION only. NOT worker/provider/model execution, NOT test run, NOT apply/approve/git.
    # contract-create / evaluate persist safe metadata; show/next-action/cycles/readiness/integrity
    # are read-only. None execute a worker, run a test, or call a provider.
    OVERNIGHT_MISSION_CREATE = "overnight_mission_create"
    OVERNIGHT_MISSION_EVALUATE = "overnight_mission_evaluate"
    OVERNIGHT_MISSION_SHOW = "overnight_mission_show"
    # Real Test Execution + Snapshot/Rollback Proof v1 (Step 1888) — read-only result/list/integrity
    # + write_metadata snapshot/rollback proof. Test EXECUTION itself stays on the existing RUN_TEST
    # action (the contract-gated safe runner). None of these run arbitrary commands or shells.
    TEST_RESULT_SHOW = "test_result_show"
    SNAPSHOT_PROOF_CREATE = "snapshot_proof_create"
    SNAPSHOT_PROOF_SHOW = "snapshot_proof_show"
    ROLLBACK_PROOF_CREATE = "rollback_proof_create"
    ROLLBACK_PROOF_SHOW = "rollback_proof_show"
    # Token-Aware Repair Loop v1/v2 (Step 1931) — ORCHESTRATION + METADATA + EVALUATION only. NOT
    # provider/model/worker execution, NOT candidate generation, NOT apply/approve. item-create-from-
    # failure/review + policy-set persist safe metadata; evaluate persists a safe evaluation; show/list/
    # context-pack/route-recommend/attempts/policy-show/integrity are read-only. None execute a worker,
    # apply a change, run an unbounded loop, or run a test (re-test stays on the existing RUN_TEST gate).
    REPAIR_ITEM_CREATE = "repair_item_create"
    REPAIR_LOOP_EVALUATE = "repair_loop_evaluate"
    REPAIR_LOOP_POLICY_SET = "repair_loop_policy_set"
    REPAIR_LOOP_SHOW = "repair_loop_show"
    # Main Builder Adapter v0 (Step 1985) — METADATA + POLICY only. NOT provider/model/worker
    # execution, NOT candidate generation, NOT apply/approve. adapter-list/show/session-show/list/
    # integrity are read-only; adapter-enable/package-create/session-create/session-record-output/
    # session-intake are write_metadata. None execute a worker, apply a change, or call a provider.
    BUILDER_ADAPTER_SHOW = "builder_adapter_show"
    BUILDER_ADAPTER_ENABLE = "builder_adapter_enable"
    BUILDER_PACKAGE_CREATE = "builder_package_create"
    BUILDER_SESSION_CREATE = "builder_session_create"
    BUILDER_SESSION_SHOW = "builder_session_show"
    BUILDER_SESSION_INTAKE = "builder_session_intake"
    # Managed Builder Execution v1 (Step 2035) — BOUNDED MANAGED EXECUTION via command templates.
    # template-list/show/execution-show/list/debug-bundle are read-only; template-create is
    # write_metadata; approve is approval_gate; run is test_execution (bounded managed runner,
    # no shell, sanitized env, timeout, output cap). None execute arbitrary commands.
    EXECUTION_TEMPLATE_SHOW = "execution_template_show"
    EXECUTION_TEMPLATE_CREATE = "execution_template_create"
    EXECUTION_TEMPLATE_ENABLE = "execution_template_enable"
    EXECUTION_TEMPLATE_DISABLE = "execution_template_disable"
    EXECUTION_TEMPLATE_UPDATE = "execution_template_update"
    EXECUTION_APPROVE = "execution_approve"
    EXECUTION_RUN = "execution_run"
    EXECUTION_SHOW = "execution_show"
    EXECUTION_DEBUG_BUNDLE = "execution_debug_bundle"
    # v1.1: approval hardening read-only surfaces
    EXECUTION_APPROVAL_SHOW = "execution_approval_show"
    EXECUTION_APPROVAL_VALIDATE = "execution_approval_validate"
    EXECUTION_APPROVAL_LIST = "execution_approval_list"
    # v1.2: operator path (Step 2506)
    EXECUTION_OPERATOR_RUNBOOK = "execution_operator_runbook"
    EXECUTION_CLAUDE_DOCTOR = "execution_claude_doctor"
    # Repair Request Builder v0 (Step 1373) — metadata-only, provider-agnostic.
    # Prepares/exports a safe request package; NOT external execution.
    PREPARE_REPAIR_REQUEST = "prepare_repair_request"
    EXPORT_REPAIR_REQUEST = "export_repair_request"
    # Self-Dogfood Planner v0 (Step 1413) — read-only inspection/plan + metadata-only
    # ProposedTask creation. No apply/test/provider; no self-modification.
    SELF_INSPECT = "self_inspect"
    SELF_PLAN = "self_plan"
    SELF_PROPOSE_TASK = "self_propose_task"
    # Self-Dogfood Execution v0 (Step 1447) — metadata/tracking only; apply stays
    # controlled by do continue.
    SELF_EXECUTE_PREPARE = "self_execute_prepare"
    SELF_RECONCILE = "self_reconcile"
    SELF_EXECUTION_STATUS = "self_execution_status"
    # Main Orchestrator Brain v0 (Step 1478) — read-only/metadata-only decisioning.
    ORCHESTRATOR_INSPECT = "orchestrator_inspect"
    ORCHESTRATOR_DECIDE = "orchestrator_decide"
    ORCHESTRATOR_REPORT = "orchestrator_report"
    # Local Model Advisor Adapter v0 (Step 1515) — OPTIONAL loopback-only advisory critique.
    # Distinct from CLOUD_PROVIDER (external execution, denied by no_cloud) and from any
    # external builder: this is a local, advisory-only, metadata-level action. status is
    # read-only; run is metadata-only (advisory text; never executes/applies/approves).
    LOCAL_ADVISOR_STATUS = "local_advisor_status"
    LOCAL_ADVISOR_RUN = "local_advisor_run"

    # Open-Ended Dogfood Run Orchestrator + Replay Analyzer v0 (Step 2160) — METADATA + EVALUATION +
    # REPLAY only. NOT provider/model/worker execution, NOT apply/approve/git. create/step/stop persist
    # safe metadata + checkpoints; show/status/replay/checkpoints/next/evaluate/brainstorm are read-only.
    # None execute a worker, run a test, apply a change, or call a provider.
    DOGFOOD_RUN_CREATE = "dogfood_run_create"
    DOGFOOD_RUN_STEP = "dogfood_run_step"
    DOGFOOD_RUN_STOP = "dogfood_run_stop"
    DOGFOOD_RUN_SHOW = "dogfood_run_show"
    DOGFOOD_RUN_REPLAY = "dogfood_run_replay"
    DOGFOOD_RUN_EVALUATE = "dogfood_run_evaluate"
    # v1.3: bounded loop + morning report (Step 2586)
    DOGFOOD_RUN_LOOP = "dogfood_run_loop"
    DOGFOOD_MORNING_REPORT = "dogfood_morning_report"
    # v1.4: worker facade + mission facade (Step 2616)
    WORKER_DOCTOR = "worker_doctor"
    WORKER_ADD = "worker_add"
    WORKER_DISABLE = "worker_disable"
    MISSION_RUN = "mission_run"
    MISSION_REPORT = "mission_report"
    DOCTOR_CORE = "doctor_core"
    # v1.5: approval policy facade (Step 2761)
    APPROVAL_POLICY_LIST = "approval_policy_list"
    APPROVAL_POLICY_SHOW = "approval_policy_show"
    APPROVAL_POLICY_ENABLE = "approval_policy_enable"
    APPROVAL_POLICY_DISABLE = "approval_policy_disable"
    APPROVAL_POLICY_EVALUATE = "approval_policy_evaluate"
    APPROVAL_POLICY_GRANT = "approval_policy_grant"

    # Self-Repair Proposal v0 (Step 2450) — METADATA + EVALUATION only. NOT provider/model/worker
    # execution, NOT auto-apply/approve/git. proposal-create/approve/deny/edit/worker-prompt persist
    # safe metadata; proposal-show/list are read-only. None execute code or apply changes.
    SELF_REPAIR_PROPOSAL_CREATE = "self_repair_proposal_create"
    SELF_REPAIR_PROPOSAL_SHOW = "self_repair_proposal_show"
    SELF_REPAIR_PROPOSAL_LIST = "self_repair_proposal_list"
    SELF_REPAIR_PROPOSAL_APPROVE = "self_repair_proposal_approve"
    SELF_REPAIR_PROPOSAL_DENY = "self_repair_proposal_deny"
    SELF_REPAIR_PROPOSAL_EDIT = "self_repair_proposal_edit"
    SELF_REPAIR_WORKER_PROMPT = "self_repair_worker_prompt"

    # Apply actions (gated by stop_before_apply)
    APPLY = "apply"
    SOURCE_APPLY = "source_apply"
    PATCH_APPLY = "patch_apply"

    # Dangerous actions (denied by default)
    ARBITRARY_SHELL = "arbitrary_shell"
    APPLY_PATCH_WITHOUT_APPROVAL = "apply_patch_without_approval"
    MODIFY_PERMISSIONS = "modify_permissions_autonomously"
    NETWORK_FETCH = "network_fetch"
    INSTALL_PACKAGES = "install_packages"
    CLOUD_PROVIDER = "cloud_provider"

    # Test actions
    RUN_TEST = "run_test"

    # Revert actions (Step 1136) — denied by default, require explicit permission + contract grant
    REVERT = "revert"


ALL_KNOWN_ACTIONS: frozenset[str] = frozenset({
    v for k, v in vars(ContractAction).items()
    if not k.startswith("_") and isinstance(v, str)
})


# ---------------------------------------------------------------------------
# Data model (Step 1048)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RunContract:
    """Immutable execution-boundary definition for a single job run.

    Fields are deterministic and JSON-serializable.  No external calls.
    """

    version: int = 1
    contract_id: str = ""
    job_id: str = ""
    scope: str = "job"
    autonomy_level: int = 1
    allowed_actions: tuple[str, ...] = ()
    denied_actions: tuple[str, ...] = ()
    max_loops: int = 10
    max_test_runs: int = 0
    max_runtime_seconds: int = 600
    max_tokens: int = 200_000
    max_cost_cents: int = 500
    allowed_paths: tuple[str, ...] = ()
    denied_paths: tuple[str, ...] = ()
    stop_before_apply: bool = True
    stop_on_unknown_risk: bool = True
    stop_on_medium_risk: bool = False
    prefer_local: bool = True
    no_cloud: bool = True
    model_policy: str = "local_first"
    command_policy: str = "allowlist_only"
    stop_conditions: tuple[str, ...] = ()
    requires_approval_for: tuple[str, ...] = ()
    source: str = ""
    created_at: str = ""
    notes: str = ""


# ---------------------------------------------------------------------------
# Action decision result (Step 1049)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RunActionDecision:
    """Result of evaluating an action against the contract."""

    allowed: bool
    status: str  # allowed, blocked, exhausted, unknown
    reason: str
    next_safe_action: str = ""


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

_DEFAULT_ALLOWED_ACTIONS: tuple[str, ...] = (
    ContractAction.PLAN,
    ContractAction.CONTEXT,
    ContractAction.BUILD_ARTIFACT,
    ContractAction.CREATE_PATCH_INTENT,
    ContractAction.CREATE_FIX_TASK,
    ContractAction.CREATE_REPAIR_ARTIFACT,
    ContractAction.CREATE_REPAIR_PATCH_INTENT,
    ContractAction.PROVIDER_INTAKE,
    ContractAction.PROVIDER_TRUST_REVIEW,
    ContractAction.PROVIDER_MATERIALIZE_PATCH,
    ContractAction.CREATE_PROVIDER_REPAIR_INTENT,
    ContractAction.PROVIDER_VERIFY_CANDIDATE,
    ContractAction.PROVIDER_VERIFICATION_SHOW,
    ContractAction.BUILDER_ROUTING_DECIDE,
    ContractAction.BUILDER_ROUTING_REPORT,
    ContractAction.LOCAL_CANDIDATE_GENERATOR_STATUS,
    ContractAction.LOCAL_CANDIDATE_GENERATE,
    ContractAction.CANDIDATE_QUALITY_EVALUATE,
    ContractAction.CANDIDATE_QUALITY_SHOW,
    ContractAction.CANDIDATE_QUALITY_SCORECARD,
    ContractAction.CANDIDATE_QUALITY_REPORT,
    ContractAction.EXTERNAL_BUILDER_PACKAGE,
    ContractAction.EXTERNAL_BUILDER_SUBMIT,
    ContractAction.EXTERNAL_BUILDER_SHOW,
    ContractAction.WORKER_REGISTRY_SHOW,
    ContractAction.ROUTE_POLICY_SHOW,
    ContractAction.ROUTE_POLICY_SET,
    ContractAction.ROUTE_POLICY_EVALUATE,
    ContractAction.TOKEN_BUDGET_SHOW,
    ContractAction.TOKEN_BUDGET_SET,
    ContractAction.TOKEN_ESTIMATE,
    ContractAction.TOKEN_ECONOMY_REPORT,
    ContractAction.CONTEXT_PACK_RECOMMEND,
    ContractAction.TOURNAMENT_REPORT,
    ContractAction.TOURNAMENT_SHOW,
    ContractAction.TOURNAMENT_LIST,
    ContractAction.TOURNAMENT_INTEGRITY,
    ContractAction.OVERNIGHT_MISSION_CREATE,
    ContractAction.OVERNIGHT_MISSION_EVALUATE,
    ContractAction.OVERNIGHT_MISSION_SHOW,
    ContractAction.TEST_RESULT_SHOW,
    ContractAction.SNAPSHOT_PROOF_CREATE,
    ContractAction.SNAPSHOT_PROOF_SHOW,
    ContractAction.ROLLBACK_PROOF_CREATE,
    ContractAction.ROLLBACK_PROOF_SHOW,
    ContractAction.REPAIR_ITEM_CREATE,
    ContractAction.REPAIR_LOOP_EVALUATE,
    ContractAction.REPAIR_LOOP_POLICY_SET,
    ContractAction.REPAIR_LOOP_SHOW,
    ContractAction.BUILDER_ADAPTER_SHOW,
    ContractAction.BUILDER_ADAPTER_ENABLE,
    ContractAction.BUILDER_PACKAGE_CREATE,
    ContractAction.BUILDER_SESSION_CREATE,
    ContractAction.BUILDER_SESSION_SHOW,
    ContractAction.BUILDER_SESSION_INTAKE,
    ContractAction.EXECUTION_TEMPLATE_SHOW,
    ContractAction.EXECUTION_TEMPLATE_CREATE,
    ContractAction.EXECUTION_TEMPLATE_ENABLE,
    ContractAction.EXECUTION_TEMPLATE_DISABLE,
    ContractAction.EXECUTION_TEMPLATE_UPDATE,
    ContractAction.EXECUTION_APPROVE,
    ContractAction.EXECUTION_RUN,
    ContractAction.EXECUTION_SHOW,
    ContractAction.EXECUTION_DEBUG_BUNDLE,
    ContractAction.EXECUTION_APPROVAL_SHOW,
    ContractAction.EXECUTION_APPROVAL_VALIDATE,
    ContractAction.EXECUTION_APPROVAL_LIST,
    ContractAction.EXECUTION_OPERATOR_RUNBOOK,
    ContractAction.EXECUTION_CLAUDE_DOCTOR,
    ContractAction.PREPARE_REPAIR_REQUEST,
    ContractAction.EXPORT_REPAIR_REQUEST,
    ContractAction.SELF_INSPECT,
    ContractAction.SELF_PLAN,
    ContractAction.SELF_PROPOSE_TASK,
    ContractAction.SELF_EXECUTE_PREPARE,
    ContractAction.SELF_RECONCILE,
    ContractAction.SELF_EXECUTION_STATUS,
    ContractAction.ORCHESTRATOR_INSPECT,
    ContractAction.ORCHESTRATOR_DECIDE,
    ContractAction.ORCHESTRATOR_REPORT,
    ContractAction.LOCAL_ADVISOR_STATUS,
    ContractAction.LOCAL_ADVISOR_RUN,
    ContractAction.DOGFOOD_RUN_CREATE,
    ContractAction.DOGFOOD_RUN_STEP,
    ContractAction.DOGFOOD_RUN_STOP,
    ContractAction.DOGFOOD_RUN_SHOW,
    ContractAction.DOGFOOD_RUN_REPLAY,
    ContractAction.DOGFOOD_RUN_EVALUATE,
    ContractAction.DOGFOOD_RUN_LOOP,
    ContractAction.DOGFOOD_MORNING_REPORT,
    ContractAction.WORKER_DOCTOR,
    ContractAction.WORKER_ADD,
    ContractAction.WORKER_DISABLE,
    ContractAction.MISSION_RUN,
    ContractAction.MISSION_REPORT,
    ContractAction.DOCTOR_CORE,
    ContractAction.APPROVAL_POLICY_LIST,
    ContractAction.APPROVAL_POLICY_SHOW,
    ContractAction.APPROVAL_POLICY_ENABLE,
    ContractAction.APPROVAL_POLICY_DISABLE,
    ContractAction.APPROVAL_POLICY_EVALUATE,
    ContractAction.APPROVAL_POLICY_GRANT,
    ContractAction.SELF_REPAIR_PROPOSAL_CREATE,
    ContractAction.SELF_REPAIR_PROPOSAL_SHOW,
    ContractAction.SELF_REPAIR_PROPOSAL_LIST,
    ContractAction.SELF_REPAIR_PROPOSAL_APPROVE,
    ContractAction.SELF_REPAIR_PROPOSAL_DENY,
    ContractAction.SELF_REPAIR_PROPOSAL_EDIT,
    ContractAction.SELF_REPAIR_WORKER_PROMPT,
    ContractAction.DISCOVER_COMMANDS,
    ContractAction.WRITE_METADATA,
    ContractAction.RUN_TEST,
)

_DEFAULT_DENIED_ACTIONS: tuple[str, ...] = (
    ContractAction.APPLY,
    ContractAction.SOURCE_APPLY,
    ContractAction.ARBITRARY_SHELL,
    ContractAction.APPLY_PATCH_WITHOUT_APPROVAL,
    ContractAction.MODIFY_PERMISSIONS,
    ContractAction.NETWORK_FETCH,
    ContractAction.INSTALL_PACKAGES,
    ContractAction.CLOUD_PROVIDER,
    ContractAction.REVERT,
)

_DEFAULT_DENIED_PATHS: tuple[str, ...] = (
    ".env",
    ".env.secret",
    ".env.local",
    "credentials.json",
    "secrets.yaml",
    "node_modules/",
    ".git/",
)

_DEFAULT_STOP_CONDITIONS: tuple[str, ...] = (
    "max_loops_exceeded",
    "max_tokens_exceeded",
    "max_cost_exceeded",
    "all_tasks_completed",
    "permission_denied_unresolvable",
)

_DEFAULT_REQUIRES_APPROVAL: tuple[str, ...] = (
    ContractAction.PATCH_APPLY,
    ContractAction.ARBITRARY_SHELL,
    ContractAction.REVERT,
)

_APPLY_ACTIONS = frozenset({
    ContractAction.APPLY, ContractAction.SOURCE_APPLY, ContractAction.PATCH_APPLY,
})
_CLOUD_ACTIONS = frozenset({
    ContractAction.CLOUD_PROVIDER, ContractAction.NETWORK_FETCH,
    ContractAction.INSTALL_PACKAGES,
})


def build_default_run_contract(job: Job) -> RunContract:
    """Build a sensible default RunContract for a job.

    Deterministic — derives contract from job metadata only.
    No LLM calls, no network, no filesystem access.

    When ``job.budgets`` is set, overlapping fields inherit from F018
    so there is ONE budget authority — JobBudgets is canonical for
    max_tokens and max_runtime_seconds when it specifies them.
    """
    max_tokens = 200_000
    max_runtime_seconds = 600
    budgets = getattr(job, "budgets", None)
    if budgets is not None:
        if getattr(budgets, "max_total_tokens", None) is not None:
            max_tokens = budgets.max_total_tokens
        if getattr(budgets, "max_wall_clock_minutes", None) is not None:
            max_runtime_seconds = budgets.max_wall_clock_minutes * 60

    return RunContract(
        version=1,
        contract_id=f"rc-{str(job.id)[:8]}",
        job_id=str(job.id),
        scope="job",
        autonomy_level=1,
        allowed_actions=_DEFAULT_ALLOWED_ACTIONS,
        denied_actions=_DEFAULT_DENIED_ACTIONS,
        max_loops=10,
        max_test_runs=0,
        max_runtime_seconds=max_runtime_seconds,
        max_tokens=max_tokens,
        max_cost_cents=500,
        allowed_paths=(),
        denied_paths=_DEFAULT_DENIED_PATHS,
        stop_before_apply=True,
        stop_on_unknown_risk=True,
        stop_on_medium_risk=False,
        prefer_local=True,
        no_cloud=True,
        model_policy="local_first",
        command_policy="allowlist_only",
        stop_conditions=_DEFAULT_STOP_CONDITIONS,
        requires_approval_for=_DEFAULT_REQUIRES_APPROVAL,
        source="default_v1",
        created_at=datetime.now(timezone.utc).isoformat(),
        notes="Auto-generated execution boundary. Not yet user-configurable.",
    )


# ---------------------------------------------------------------------------
# Contract persistence (Step 1066)
# ---------------------------------------------------------------------------

_CONTRACT_META_KEY = "run_contract"


def _contract_from_dict(data: dict[str, Any]) -> RunContract:
    """Reconstruct a RunContract from a metadata dict."""
    # Convert list fields back to tuples
    tuple_fields = (
        "allowed_actions", "denied_actions", "allowed_paths", "denied_paths",
        "stop_conditions", "requires_approval_for",
    )
    cleaned = dict(data)
    for field in tuple_fields:
        if field in cleaned and isinstance(cleaned[field], list):
            cleaned[field] = tuple(cleaned[field])
    return RunContract(**cleaned)


def save_contract(job: Job, contract: RunContract) -> None:
    """Store a RunContract in job.metadata. Caller must persist the job."""
    job.metadata[_CONTRACT_META_KEY] = export_run_contract_json(contract)


def load_contract(job: Job) -> RunContract | None:
    """Load the persisted RunContract from job.metadata, or None if absent."""
    data = job.metadata.get(_CONTRACT_META_KEY)
    if not isinstance(data, dict):
        return None
    return _contract_from_dict(data)


def ensure_contract(job: Job) -> RunContract:
    """Return the persisted contract, creating and saving one if absent.

    Guarantees stable contract_id and created_at across reloads.
    When JobBudgets changed since the persisted contract was created,
    reconciles max_tokens and max_runtime_seconds to match.
    Caller must persist the job if this function creates a new contract.
    """
    existing = load_contract(job)
    if existing is not None:
        existing = _reconcile_budget_fields(job, existing)
        return existing
    contract = build_default_run_contract(job)
    save_contract(job, contract)
    return contract


def _reconcile_budget_fields(job: Job, contract: RunContract) -> RunContract:
    """If JobBudgets diverged from the persisted contract, update contract."""
    budgets = getattr(job, "budgets", None)
    if budgets is None:
        return contract

    want_tokens = contract.max_tokens
    want_runtime = contract.max_runtime_seconds

    if getattr(budgets, "max_total_tokens", None) is not None:
        want_tokens = budgets.max_total_tokens
    if getattr(budgets, "max_wall_clock_minutes", None) is not None:
        want_runtime = budgets.max_wall_clock_minutes * 60

    if want_tokens == contract.max_tokens and want_runtime == contract.max_runtime_seconds:
        return contract

    import logging
    logging.getLogger(__name__).warning(
        "RunContract max_tokens/max_runtime_seconds reconciled to match JobBudgets "
        "(contract had %d/%d, budgets want %d/%d)",
        contract.max_tokens, contract.max_runtime_seconds,
        want_tokens, want_runtime,
    )
    updated = RunContract(
        version=contract.version,
        contract_id=contract.contract_id,
        job_id=contract.job_id,
        scope=contract.scope,
        autonomy_level=contract.autonomy_level,
        allowed_actions=contract.allowed_actions,
        denied_actions=contract.denied_actions,
        max_loops=contract.max_loops,
        max_test_runs=contract.max_test_runs,
        max_runtime_seconds=want_runtime,
        max_tokens=want_tokens,
        max_cost_cents=contract.max_cost_cents,
        allowed_paths=contract.allowed_paths,
        denied_paths=contract.denied_paths,
        stop_before_apply=contract.stop_before_apply,
        stop_on_unknown_risk=contract.stop_on_unknown_risk,
        stop_on_medium_risk=contract.stop_on_medium_risk,
        prefer_local=contract.prefer_local,
        no_cloud=contract.no_cloud,
        model_policy=contract.model_policy,
        command_policy=contract.command_policy,
        stop_conditions=contract.stop_conditions,
        requires_approval_for=contract.requires_approval_for,
        source=contract.source,
        created_at=contract.created_at,
        notes=contract.notes,
    )
    save_contract(job, updated)
    return updated


def needs_contract_migration(job: Job) -> bool:
    """Check if a job needs contract migration (no persisted contract)."""
    return not isinstance(job.metadata.get(_CONTRACT_META_KEY), dict)


def migrate_contract(job: Job) -> RunContract:
    """Migrate an old job to have a persisted contract.

    Idempotent — returns existing contract if already present.
    Caller must persist the job after calling this.
    """
    return ensure_contract(job)


# ---------------------------------------------------------------------------
# Usage ledger (Step 1075)
# ---------------------------------------------------------------------------

_USAGE_META_KEY = "run_usage"


@dataclass
class RunUsage:
    """Tracks resource consumption against contract budgets."""

    loops_used: int = 0
    test_runs_used: int = 0
    runtime_seconds_used: float = 0.0
    tokens_used: int = 0
    cost_cents_used: float = 0.0


@dataclass(frozen=True)
class RunBudgetStatus:
    """Result of checking usage against contract budgets."""

    within_budget: bool
    exhausted_budgets: tuple[str, ...] = ()
    remaining: dict[str, Any] = field(default_factory=dict)


def _usage_to_dict(usage: RunUsage) -> dict[str, Any]:
    return {
        "loops_used": usage.loops_used,
        "test_runs_used": usage.test_runs_used,
        "runtime_seconds_used": usage.runtime_seconds_used,
        "tokens_used": usage.tokens_used,
        "cost_cents_used": usage.cost_cents_used,
    }


def save_usage(job: Job, usage: RunUsage) -> None:
    """Store usage in job.metadata. Caller must persist the job."""
    job.metadata[_USAGE_META_KEY] = _usage_to_dict(usage)


def load_usage(job: Job) -> RunUsage:
    """Load usage from job.metadata. Returns zero usage if absent."""
    data = job.metadata.get(_USAGE_META_KEY)
    if not isinstance(data, dict):
        return RunUsage()
    return RunUsage(
        loops_used=data.get("loops_used", 0),
        test_runs_used=data.get("test_runs_used", 0),
        runtime_seconds_used=data.get("runtime_seconds_used", 0.0),
        tokens_used=data.get("tokens_used", 0),
        cost_cents_used=data.get("cost_cents_used", 0.0),
    )


def check_budget(contract: RunContract, usage: RunUsage) -> RunBudgetStatus:
    """Check usage against contract budgets. Returns budget status."""
    exhausted: list[str] = []
    remaining: dict[str, Any] = {}

    if usage.loops_used >= contract.max_loops:
        exhausted.append("max_loops")
    remaining["loops"] = max(0, contract.max_loops - usage.loops_used)

    if usage.test_runs_used >= contract.max_test_runs:
        exhausted.append("max_test_runs")
    remaining["test_runs"] = max(0, contract.max_test_runs - usage.test_runs_used)

    # runtime/tokens/cost: only check if budget > 0 (0 = unlimited for v1)
    if contract.max_runtime_seconds > 0 and usage.runtime_seconds_used >= contract.max_runtime_seconds:
        exhausted.append("max_runtime_seconds")
    if contract.max_runtime_seconds > 0:
        remaining["runtime_seconds"] = max(0.0, contract.max_runtime_seconds - usage.runtime_seconds_used)

    if contract.max_tokens > 0 and usage.tokens_used >= contract.max_tokens:
        exhausted.append("max_tokens")
    if contract.max_tokens > 0:
        remaining["tokens"] = max(0, contract.max_tokens - usage.tokens_used)

    if contract.max_cost_cents > 0 and usage.cost_cents_used >= contract.max_cost_cents:
        exhausted.append("max_cost_cents")
    if contract.max_cost_cents > 0:
        remaining["cost_cents"] = max(0.0, contract.max_cost_cents - usage.cost_cents_used)

    return RunBudgetStatus(
        within_budget=len(exhausted) == 0,
        exhausted_budgets=tuple(exhausted),
        remaining=remaining,
    )


def export_usage_json(usage: RunUsage) -> dict[str, Any]:
    """Export usage as JSON-serializable dict."""
    return _usage_to_dict(usage)


def export_budget_status_json(status: RunBudgetStatus) -> dict[str, Any]:
    """Export budget status as JSON-serializable dict."""
    return {
        "within_budget": status.within_budget,
        "exhausted_budgets": list(status.exhausted_budgets),
        "remaining": status.remaining,
    }


# ---------------------------------------------------------------------------
# Contract validation (Step 1069)
# ---------------------------------------------------------------------------


def validate_run_contract(contract: RunContract) -> list[str]:
    """Validate a RunContract. Returns list of error strings (empty = valid)."""
    errors: list[str] = []

    if contract.version < 1:
        errors.append(f"version must be >= 1, got {contract.version}")

    if not contract.contract_id:
        errors.append("contract_id is empty")

    if contract.max_loops < 0:
        errors.append(f"max_loops must be >= 0, got {contract.max_loops}")

    if contract.max_test_runs < 0:
        errors.append(f"max_test_runs must be >= 0, got {contract.max_test_runs}")

    if contract.max_runtime_seconds < 0:
        errors.append(f"max_runtime_seconds must be >= 0, got {contract.max_runtime_seconds}")

    if contract.max_tokens < 0:
        errors.append(f"max_tokens must be >= 0, got {contract.max_tokens}")

    if contract.max_cost_cents < 0:
        errors.append(f"max_cost_cents must be >= 0, got {contract.max_cost_cents}")

    # Check for actions in both allowed and denied
    overlap = set(contract.allowed_actions) & set(contract.denied_actions)
    if overlap:
        errors.append(f"actions in both allowed and denied: {sorted(overlap)}")

    # Unknown actions are errors — all action strings must be canonical
    all_actions = (
        set(contract.allowed_actions)
        | set(contract.denied_actions)
        | set(contract.requires_approval_for)
    )
    unknown = all_actions - ALL_KNOWN_ACTIONS
    if unknown:
        errors.append(f"unknown actions: {sorted(unknown)}")

    # Check denied paths for absolute paths
    for p in contract.denied_paths:
        if os.path.isabs(p):
            errors.append(f"denied_paths contains absolute path: {p}")

    for p in contract.allowed_paths:
        if os.path.isabs(p):
            errors.append(f"allowed_paths contains absolute path: {p}")

    return errors


# ---------------------------------------------------------------------------
# Contract decision helper (Step 1049)
# ---------------------------------------------------------------------------


def evaluate_run_action(
    contract: RunContract,
    action: str,
    *,
    path: str | None = None,
    risk: str | None = None,
    loop_index: int | None = None,
    test_run_count: int | None = None,
    usage: RunUsage | None = None,
) -> RunActionDecision:
    """Evaluate whether an action is allowed under the contract.

    Returns a RunActionDecision with allowed, status, reason, next_safe_action.
    """
    # 1. Denied actions
    if action in contract.denied_actions:
        return RunActionDecision(
            allowed=False,
            status="blocked",
            reason=f"Action '{action}' is in denied_actions",
            next_safe_action="remedy contract inspect <job_id> --json",
        )

    # 2. Not in allowed actions
    if contract.allowed_actions and action not in contract.allowed_actions:
        return RunActionDecision(
            allowed=False,
            status="blocked",
            reason=f"Action '{action}' not in allowed_actions",
            next_safe_action="remedy contract inspect <job_id> --json",
        )

    # 3. Test run zero-budget block — run_test requires explicit max_test_runs > 0
    if action == ContractAction.RUN_TEST and contract.max_test_runs == 0:
        return RunActionDecision(
            allowed=False,
            status="exhausted",
            reason="max_test_runs is 0 — set it above 0 to enable test execution",
            next_safe_action="remedy contract set <job_id> max_test_runs <n>",
        )

    # 4. stop_before_apply blocks apply-type actions
    if contract.stop_before_apply and action in _APPLY_ACTIONS:
        return RunActionDecision(
            allowed=False,
            status="blocked",
            reason="stop_before_apply blocks apply actions",
            next_safe_action="remedy patch approve <job_id> <intent_id>",
        )

    # 5. no_cloud blocks cloud actions
    if contract.no_cloud and action in _CLOUD_ACTIONS:
        return RunActionDecision(
            allowed=False,
            status="blocked",
            reason="no_cloud blocks cloud/provider actions",
            next_safe_action="remedy contract inspect <job_id> --json",
        )

    # 6. Loop budget (from explicit param or usage)
    effective_loops = loop_index if loop_index is not None else (usage.loops_used if usage else None)
    if effective_loops is not None and effective_loops >= contract.max_loops:
        return RunActionDecision(
            allowed=False,
            status="exhausted",
            reason=f"Loop usage {effective_loops} >= max_loops {contract.max_loops}",
            next_safe_action="remedy job show <job_id> --json",
        )

    # 7. Test run budget (from explicit param or usage)
    effective_tests = test_run_count if test_run_count is not None else (usage.test_runs_used if usage else None)
    if effective_tests is not None and effective_tests >= contract.max_test_runs:
        return RunActionDecision(
            allowed=False,
            status="exhausted",
            reason=f"Test runs {effective_tests} >= max_test_runs {contract.max_test_runs}",
            next_safe_action="remedy job show <job_id> --json",
        )

    # 8. Runtime/token/cost budgets from usage
    if usage is not None:
        budget_status = check_budget(contract, usage)
        if not budget_status.within_budget:
            return RunActionDecision(
                allowed=False,
                status="exhausted",
                reason=f"Budget exhausted: {', '.join(budget_status.exhausted_budgets)}",
                next_safe_action="remedy job show <job_id> --json",
            )

    # 9. Path policy
    if path is not None:
        path_decision = _check_path_policy(contract, path)
        if path_decision is not None:
            return path_decision

    # 10. Risk policy
    if risk is not None:
        risk_lower = risk.lower()
        if risk_lower == "unknown" and contract.stop_on_unknown_risk:
            return RunActionDecision(
                allowed=False,
                status="blocked",
                reason="stop_on_unknown_risk blocks unknown-risk actions",
                next_safe_action="remedy contract inspect <job_id> --json",
            )
        if risk_lower in ("medium", "high") and contract.stop_on_medium_risk:
            return RunActionDecision(
                allowed=False,
                status="blocked",
                reason=f"stop_on_medium_risk blocks {risk_lower}-risk actions",
                next_safe_action="remedy contract inspect <job_id> --json",
            )

    return RunActionDecision(
        allowed=True,
        status="allowed",
        reason=f"Action '{action}' permitted by contract",
    )


def _path_matches(normalized: str, pattern: str) -> bool:
    """Segment-aware path matching: exact match or directory prefix only.

    .env matches .env and .env/foo but NOT .environment.py
    node_modules/ matches node_modules/foo but NOT node_modules_backup/
    """
    clean = pattern.rstrip("/")
    return normalized == clean or normalized.startswith(clean + "/")


def _check_path_policy(contract: RunContract, path: str) -> RunActionDecision | None:
    """Check path against allowed/denied path policies. Returns decision if blocked."""
    normalized = os.path.normpath(path)

    # Block absolute paths
    if os.path.isabs(normalized):
        return RunActionDecision(
            allowed=False,
            status="blocked",
            reason=f"Absolute path '{normalized}' blocked by policy",
            next_safe_action="remedy contract inspect <job_id> --json",
        )

    # Block traversal
    if ".." in normalized.split(os.sep):
        return RunActionDecision(
            allowed=False,
            status="blocked",
            reason=f"Path traversal in '{normalized}' blocked by policy",
            next_safe_action="remedy contract inspect <job_id> --json",
        )

    # Denied paths win over allowed paths (segment-aware)
    for denied in contract.denied_paths:
        if _path_matches(normalized, denied):
            return RunActionDecision(
                allowed=False,
                status="blocked",
                reason=f"Path '{normalized}' matches denied path '{denied}'",
                next_safe_action="remedy contract inspect <job_id> --json",
            )

    # If allowed_paths specified, path must match (segment-aware)
    if contract.allowed_paths:
        matched = False
        for allowed in contract.allowed_paths:
            if _path_matches(normalized, allowed):
                matched = True
                break
        if not matched:
            return RunActionDecision(
                allowed=False,
                status="blocked",
                reason=f"Path '{normalized}' not in allowed_paths",
                next_safe_action="remedy contract inspect <job_id> --json",
            )

    return None


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


def export_run_contract_json(contract: RunContract) -> dict[str, Any]:
    """Export a RunContract as a JSON-serializable dict."""
    return {
        "version":               contract.version,
        "contract_id":           contract.contract_id,
        "job_id":                contract.job_id,
        "scope":                 contract.scope,
        "autonomy_level":        contract.autonomy_level,
        "allowed_actions":       list(contract.allowed_actions),
        "denied_actions":        list(contract.denied_actions),
        "max_loops":             contract.max_loops,
        "max_test_runs":         contract.max_test_runs,
        "max_runtime_seconds":   contract.max_runtime_seconds,
        "max_tokens":            contract.max_tokens,
        "max_cost_cents":        contract.max_cost_cents,
        "allowed_paths":         list(contract.allowed_paths),
        "denied_paths":          list(contract.denied_paths),
        "stop_before_apply":     contract.stop_before_apply,
        "stop_on_unknown_risk":  contract.stop_on_unknown_risk,
        "stop_on_medium_risk":   contract.stop_on_medium_risk,
        "prefer_local":          contract.prefer_local,
        "no_cloud":              contract.no_cloud,
        "model_policy":          contract.model_policy,
        "command_policy":        contract.command_policy,
        "stop_conditions":       list(contract.stop_conditions),
        "requires_approval_for": list(contract.requires_approval_for),
        "source":                contract.source,
        "created_at":            contract.created_at,
        "notes":                 contract.notes,
    }


def export_run_action_decision_json(decision: RunActionDecision) -> dict[str, Any]:
    """Export action decision as JSON dict."""
    return {
        "allowed": decision.allowed,
        "status": decision.status,
        "reason": decision.reason,
        "next_safe_action": decision.next_safe_action,
    }


def summarize_run_contract(contract: RunContract) -> str:
    """Return a human-readable summary of the RunContract."""
    lines: list[str] = []
    lines.append("Run Contract")
    lines.append(f"  Version:         {contract.version}")
    lines.append(f"  Contract ID:     {contract.contract_id}")
    lines.append(f"  Job:             {contract.job_id[:8]}")
    lines.append(f"  Scope:           {contract.scope}")
    lines.append(f"  Autonomy:        {contract.autonomy_level}")
    lines.append(f"  Model policy:    {contract.model_policy}")
    lines.append(f"  Command policy:  {contract.command_policy}")
    lines.append(f"  Max loops:       {contract.max_loops}")
    lines.append(f"  Max test runs:   {contract.max_test_runs}")
    lines.append(f"  Max runtime:     {contract.max_runtime_seconds}s")
    lines.append(f"  Max tokens:      {contract.max_tokens:,}")
    lines.append(f"  Max cost:        {contract.max_cost_cents} cents")
    lines.append(f"  Stop before apply: {contract.stop_before_apply}")
    lines.append(f"  Stop on unknown risk: {contract.stop_on_unknown_risk}")
    lines.append(f"  Stop on medium risk:  {contract.stop_on_medium_risk}")
    lines.append(f"  Prefer local:    {contract.prefer_local}")
    lines.append(f"  No cloud:        {contract.no_cloud}")
    lines.append(f"  Source:          {contract.source}")

    lines.append("  Allowed actions:")
    for a in contract.allowed_actions:
        lines.append(f"    + {a}")

    lines.append("  Denied actions:")
    for d in contract.denied_actions:
        lines.append(f"    - {d}")

    if contract.allowed_paths:
        lines.append("  Allowed paths:")
        for p in contract.allowed_paths:
            lines.append(f"    + {p}")

    if contract.denied_paths:
        lines.append("  Denied paths:")
        for p in contract.denied_paths:
            lines.append(f"    - {p}")

    lines.append("  Stop conditions:")
    for s in contract.stop_conditions:
        lines.append(f"    * {s}")

    lines.append("  Requires approval for:")
    for r in contract.requires_approval_for:
        lines.append(f"    ! {r}")

    if contract.notes:
        lines.append(f"  Notes: {contract.notes}")

    return "\n".join(lines)
