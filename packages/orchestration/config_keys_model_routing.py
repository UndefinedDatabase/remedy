"""The model routing keys of the config registry (DECISION F058 D1), and the Pi tool deadline.

Moved unchanged out of `packages/orchestration/config.py`, whose `_CONFIG_KEY_SPECS` splices
`MODEL_ROUTING_KEY_SPECS` in at the keys' own place, so the registry and the guide it renders keep
their order.
"""

from __future__ import annotations

from packages.orchestration.config_key_spec import ConfigKeySpec

# The failover chain table's key, the cooldown's key and its default, spelled once here and read
# by packages/orchestration/model_failover.py (R-1310).
FAILOVER_CHAINS_CONFIG_KEY: str = "model_failover.chains"
FAILOVER_COOLDOWN_CONFIG_KEY: str = "model_failover.cooldown_s"
FAILOVER_COOLDOWN_DEFAULT_S: int = 300

# The tier escalation's three keys and the threshold's default, spelled once here and read by
# packages/orchestration/tier_escalation.py (F296, DECISION F296 D2).
ESCALATION_ENABLED_CONFIG_KEY: str = "model_escalation.enabled"
ESCALATION_AFTER_FAILURES_CONFIG_KEY: str = "model_escalation.after_failures"
ESCALATION_AFTER_FAILURES_DEFAULT: int = 2
ESCALATION_TIERS_CONFIG_KEY: str = "model_escalation.tiers"

# The local endpoints and the side roles mapped to them, spelled once here and read by
# packages/orchestration/local_endpoints.py and side_role_routing.py (F113, DECISION F113 D1).
LOCAL_ENDPOINTS_CONFIG_KEY: str = "local_routing.endpoints"
SIDE_ROLES_CONFIG_KEY: str = "local_routing.side_roles"

MODEL_ROUTING_KEY_SPECS: tuple[ConfigKeySpec, ...] = (
    # F110's per-project override map, and the first TABLE-VALUED key in this
    # registry. The DEFAULT IS None AND NOT AN EMPTY TABLE on purpose: "no
    # override configured" and "an override table that is explicitly empty" are
    # different operator statements, and collapsing them would lose the one the
    # routing layer reports on.
    ConfigKeySpec(
        key="model_routing.task_class_tiers",
        env_var="REMEDY_MODEL_ROUTING_TASK_CLASS_TIERS",
        description=(
            "Per-project TASK CLASS to MODEL TIER map (F110). The whole "
            "[remedy.model_routing.task_class_tiers] sub-table resolves as ONE "
            "value and is laid over the shipped seed mapping in "
            "packages/orchestration/model_routing.py. The hard rules of "
            "docs/agents/model_routing_policy.md still win: a map that breaks "
            "one is REFUSED with the rule named and the shipped table is used. "
            "Configured in TOML only — an env var cannot carry a table."
        ),
        value_type=dict,
        entry_type=str,
        default=None,
    ),
    # F110's PROMOTION-EVIDENCE table, and the first table of RECORDS in this
    # registry: every entry is itself a sub-table, so it declares entry_type
    # dict where its sibling above declares str. THE READER NOW EXISTS: it is
    # role_config.resolve_promotion_evidence, which landed at 8efa2330 in
    # packages/orchestration/role_config.py beside the one that already reads
    # the tiers table. It is registered first, on purpose, so the schema is
    # pinned before routing behaviour moves against it.
    ConfigKeySpec(
        key="model_routing.promotion_evidence",
        env_var="REMEDY_MODEL_ROUTING_PROMOTION_EVIDENCE",
        description=(
            "Per-project TASK CLASS to BENCHMARK RUN map (F110). Each entry of "
            "the [remedy.model_routing.promotion_evidence] sub-table is itself a "
            "table: the documented run that LICENSES A CHEAPER TIER for that "
            "class, as docs/agents/model_routing_policy.md's 'Promotion rule' "
            "describes it. Whether a run clears the promotion bars is decided in "
            "packages/orchestration/model_routing.py, never here. Configured in "
            "TOML only — an env var cannot carry a table."
        ),
        value_type=dict,
        entry_type=dict,
        default=None,
    ),
    # F058's per-role failover chains: parsed and hard-rule-checked by
    # packages/orchestration/model_failover.py, never here.
    ConfigKeySpec(
        key=FAILOVER_CHAINS_CONFIG_KEY,
        env_var="REMEDY_MODEL_FAILOVER_CHAINS",
        description=(
            "Per-role model failover chains (F058); each entry of the "
            "[remedy.model_failover.chains] sub-table names a role and holds a list of "
            "links, each a table of exactly provider, model and tier, tried in order "
            "when the role's provider is unavailable; every link is checked against the "
            "hard rules of docs/agents/model_routing_policy.md, and a local link is "
            "allowed only for the roles routed to the cheap tier; a table that breaks a "
            "rule is refused with the rule and the link named, and no role fails over; "
            "configured in TOML only — an env var cannot carry a table."
        ),
        value_type=dict,
        entry_type=list,
        default=None,
    ),
    # WHY: the sticky window's length, so one failover does not retry the dead primary on every
    # call that follows (F058).
    ConfigKeySpec(
        key=FAILOVER_COOLDOWN_CONFIG_KEY,
        env_var="REMEDY_MODEL_FAILOVER_COOLDOWN_S",
        description=(
            "After a backup model serves a call because the role's usual provider could not be "
            "reached, how many seconds the run sends that role's next calls to its backups first "
            "before trying the usual provider again (F058); a whole number of at least 0, where 0 "
            "never holds."
        ),
        value_type=int,
        default=FAILOVER_COOLDOWN_DEFAULT_S,
    ),
    # WHY: F296's one switch; while it is off, no task's round moves to another tier.
    ConfigKeySpec(
        key=ESCALATION_ENABLED_CONFIG_KEY,
        env_var="REMEDY_MODEL_ESCALATION_ENABLED",
        description=(
            "Whether a task whose builder keeps failing on a cheaper model tier gets its next repair "
            "round on the next tier up, with its reviewer raised alongside (F296); off by default, "
            "and a provider that cannot be reached never moves a task, which stays model failover's."
        ),
        value_type=bool,
        default=False,
    ),
    ConfigKeySpec(
        key=ESCALATION_AFTER_FAILURES_CONFIG_KEY,
        env_var="REMEDY_MODEL_ESCALATION_AFTER_FAILURES",
        description=(
            "How many rounds in a row a tier's builder may fail, by red tests or a review that did not "
            "pass, before the next round moves one tier up (F296); a whole number of at least 1. Two "
            "red runs with the same failure, and a test run stopped at one of its limits, move it "
            "sooner."
        ),
        value_type=int,
        default=ESCALATION_AFTER_FAILURES_DEFAULT,
    ),
    ConfigKeySpec(
        key=ESCALATION_TIERS_CONFIG_KEY,
        env_var="REMEDY_MODEL_ESCALATION_TIERS",
        description=(
            "The model each tier runs on when a task escalates (F296); each entry of the "
            "[remedy.model_escalation.tiers] sub-table names a tier, cheap, mid or top, and holds a "
            "table of exactly provider and model; a run whose builder or reviewer is none of them "
            "never escalates; a table that cannot be read is refused with the fault named, and no "
            "task escalates; configured in TOML only — an env var cannot carry a table."
        ),
        value_type=dict,
        entry_type=dict,
        default=None,
    ),
    # WHY: F113's model servers of the operator's own, which only a side role may run on.
    ConfigKeySpec(
        key=LOCAL_ENDPOINTS_CONFIG_KEY,
        env_var="REMEDY_LOCAL_ROUTING_ENDPOINTS",
        description=(
            "The local model servers a side role may run on (F113); each entry of the "
            "[remedy.local_routing.endpoints] sub-table names a server and holds a table of exactly "
            "base_url, an http or https address of an Ollama server, and model; a server that does not "
            "answer, or does not list its model, is unavailable and the role falls back; a table that "
            "cannot be read is refused with the fault named, and no role runs locally; configured in "
            "TOML only — an env var cannot carry a table."
        ),
        value_type=dict,
        entry_type=dict,
        default=None,
    ),
    ConfigKeySpec(
        key=SIDE_ROLES_CONFIG_KEY,
        env_var="REMEDY_LOCAL_ROUTING_SIDE_ROLES",
        description=(
            "Which side role runs on which local server (F113); each entry of the "
            "[remedy.local_routing.side_roles] sub-table maps a role to a server named in "
            "local_routing.endpoints; only summary, teacher and study may be mapped, and a table that "
            "maps any other role is refused whole with the hard rule core_role_on_local_provider "
            "named; configured in TOML only — an env var cannot carry a table."
        ),
        value_type=dict,
        entry_type=str,
        default=None,
    ),
    # WHY here: the provider-execution keys live in this module; `config.py` may not grow.
    ConfigKeySpec(
        key="pi.tool_timeout_seconds",
        env_var="REMEDY_PI_TOOL_TIMEOUT_SECONDS",
        description=(
            "How many seconds one shell command of a Pi tool call may run inside the tool sandbox "
            "before it is ended, so a hanging grep or test cannot stall the job; the Pi call's "
            "own deadline still bounds the whole call (DECISION amend1016sb D2)."
        ),
        value_type=int,
        default=300,
    ),
    ConfigKeySpec(
        key="pi.max_turns_per_call",
        env_var="REMEDY_PI_MAX_TURNS_PER_CALL",
        description=(
            "How many model turns one Pi call's agent loop may take: once it has used them and asks "
            "for another tool, Remedy ends the call, keeps what it wrote and ends the task "
            "budget_exhausted; a final answer is never cut off (exec-1017 D4)."
        ),
        value_type=int,
        default=40,
    ),
    ConfigKeySpec(
        key="pi.max_input_tokens_per_call",
        env_var="REMEDY_PI_MAX_INPUT_TOKENS_PER_CALL",
        description=(
            "How many input tokens one Pi call's agent loop may consume over all its turns (each "
            "turn resends the prompt and the history) before Remedy ends it the same way; the job's "
            "remaining max_total_tokens lowers it further (exec-1017 D4)."
        ),
        value_type=int,
        default=400000,
    ),
)
