"""What a remote client may choose for an execution, decided by the server (exec-1017 D6).

`POST /api/v1/orders` and `POST /api/v1/jobs/{job}/run` take `builder_provider` and
`reviewer_provider` from their body and pass them to `remedy do` / `remedy job run`. Until
exec-1017 they passed any value the command line accepts, `claude-cli` included: the Claude Code
CLI runs with the host's file and shell tools OUTSIDE the tool sandbox every Pi call runs in
(DECISION amend1016sb D1 covers Pi only), so a token holder could have asked the server to run an
unsandboxed agent over a repository. Remedy deliberately does not offer that over HTTP until its
isolation is verified; it stays a command-line choice of the operator. A provider HTTP does not
offer is refused before anything starts with 400 `api_provider_not_offered`, never substituted.

Operator amendment amend1023-universe-trust (DECISION amend1023 D6) adds one exception the
operator grants by hand: a client whose registry entry holds `host_tools` (granted only by
`remedy client grant-host-tools` on this machine's command line) may name `claude-cli` as
`builder_provider` and `reviewer_provider`, which repair follows, and may choose the planner with
`planner_provider` (`ollama` or `claude-cli`). The boundary stays where it was: the property is set
on the machine where the Claude Code CLI already runs with the same rights, never over HTTP. Every
other caller, the server's own token included, is offered exactly what it was offered before.
"""
from __future__ import annotations

from typing import Any

#: The refusal token of a provider HTTP does not offer.
API_PROVIDER_NOT_OFFERED = "api_provider_not_offered"

#: Each role's providers an HTTP client may name. `ollama` alone cannot write files, so it is no
#: builder; `fake` is the deterministic test provider; `claude` is the Anthropic API (no host tools).
REMOTE_ROLE_PROVIDERS: dict[str, tuple[str, ...]] = {
    "builder": ("pi", "claude", "fake"),
    "reviewer": ("pi", "ollama", "claude", "fake"),
}

#: What a client whose entry holds `host_tools` may name over HTTP, by role (DECISION amend1023 D6):
#: `claude-cli` beside every provider above, and the planner, which no other client chooses.
HOST_TOOLS_ROLE_PROVIDERS: dict[str, tuple[str, ...]] = {
    "builder": (*REMOTE_ROLE_PROVIDERS["builder"], "claude-cli"),
    "reviewer": (*REMOTE_ROLE_PROVIDERS["reviewer"], "claude-cli"),
    "planner": ("ollama", "claude-cli"),
}

#: The client property that opens `HOST_TOOLS_ROLE_PROVIDERS`, as the registry and the answers spell it.
HOST_TOOLS_PROPERTY = "host_tools"

#: Providers the command line offers that HTTP does not, each with the reason a client is told.
CLI_ONLY_PROVIDERS: dict[str, str] = {
    "claude-cli": ("the Claude Code CLI runs with the host's file and shell tools outside Remedy's "
                   "tool sandbox, so it is offered on the operator's command line, and over HTTP only "
                   f"to a client the operator granted `{HOST_TOOLS_PROPERTY}` on this machine "
                   "(remedy client grant-host-tools)"),
}


def client_has_host_tools(client: Any) -> bool:
    """True for a client token whose registry entry holds `host_tools`; False for the server's own token."""
    return bool(getattr(client, HOST_TOOLS_PROPERTY, False))


def remote_role_providers(client: Any = None) -> dict[str, tuple[str, ...]]:
    """Each role's providers CLIENT may name over HTTP: `HOST_TOOLS_ROLE_PROVIDERS` for a client with
    `host_tools`, `REMOTE_ROLE_PROVIDERS` for every other caller (DECISION amend1023 D6)."""
    return HOST_TOOLS_ROLE_PROVIDERS if client_has_host_tools(client) else REMOTE_ROLE_PROVIDERS


#: The body keys that name a provider, the planner's included; a call naming `claude-cli` in any of
#: them is a host-tools call the ledger marks (DECISION amend1023 D6).
PROVIDER_BODY_KEYS: tuple[str, ...] = ("builder_provider", "reviewer_provider", "planner_provider")


def remote_provider_refusal(body: dict[str, Any], client: Any = None) -> str:
    """The sentence refusing a body's `builder_provider`, `reviewer_provider` or `planner_provider`, or
    "" when each it names is offered to CLIENT and available here."""
    offer = remote_role_providers(client)
    for key in PROVIDER_BODY_KEYS:
        value = body.get(key)
        role = key.removesuffix("_provider")
        offered = offer.get(role, ())
        if value is None or value in offered:
            continue
        why = (CLI_ONLY_PROVIDERS.get(str(value), "it is not a provider of this role") if offered else
               f"the planner is the server's configuration; only a client granted `{HOST_TOOLS_PROPERTY}` "
               "chooses it over HTTP")
        return (f"{key} {value!r} is not offered over HTTP: {why}; offered: "
                f"{', '.join(offered) or 'none'}. Nothing was started.")
    for key in PROVIDER_BODY_KEYS:
        value = body.get(key)
        if value in ("pi", "claude", "claude-cli") and not _available(value, None):
            return (f"{key} {value!r} is offered but not available on this server (see GET "
                    f"/api/v1/execution). Nothing was started.")
    return ""


#: The providers each role can name on the command line, in the order `remedy do` lists them.
_ROLE_PROVIDERS: dict[str, tuple[str, ...]] = {
    "planner": ("ollama", "claude-cli"),
    "builder": ("pi", "claude", "claude-cli", "fake"),
    "reviewer": ("pi", "ollama", "claude", "claude-cli", "fake"),
    "repair": ("pi", "claude", "claude-cli", "fake"),
}
#: What each provider is, in the words a client shows: where its tools run.
_PROVIDER_ISOLATION: dict[str, str] = {
    "pi": "the Pi harness inside Remedy's tool sandbox (Bubblewrap), model on the configured Ollama",
    "ollama": "a text completion from the configured Ollama endpoint; no tools, writes no file",
    "claude": "a text completion from the Anthropic API; no host tools",
    "claude-cli": "the Claude Code CLI with the host's file and shell tools, outside the tool sandbox",
    "fake": "Remedy's deterministic test provider; no model",
}

#: The routes a client reads a run's progress and evidence from.
EXECUTION_OBSERVABILITY_ROUTES: tuple[str, ...] = (
    "GET /api/v1/orders/{order}", "GET /api/v1/jobs/{job}/run", "GET /api/v1/jobs/{job}/story",
    "GET /api/v1/jobs/{job}/logs", "GET /api/v1/jobs/{job}/diff", "GET /api/v1/jobs/{job}/proof",
    "GET /api/v1/now", "GET /api/v1/jobs/{job}/insight",
)


def _available(provider: str, ollama_models: list[str] | None) -> bool:
    import shutil

    if provider == "pi":
        return shutil.which("pi") is not None
    if provider == "ollama":
        return ollama_models is not None
    if provider == "claude":
        import os
        return bool(os.environ.get("ANTHROPIC_API_KEY"))     # whether it is set, never its value
    if provider == "claude-cli":
        return shutil.which("claude") is not None
    return provider == "fake"


def _offered_over_http(role: str, provider: str, client: Any) -> bool:
    """Whether CLIENT may have PROVIDER serve ROLE over HTTP. Repair is never named over HTTP: it runs
    on the builder's provider unless the server configures one, so a client with `host_tools` that
    names `claude-cli` as builder is offered it for repair too (DECISION amend1023 D6)."""
    if role == "repair":
        return client_has_host_tools(client) and provider == "claude-cli"
    return provider in remote_role_providers(client).get(role, ())


def _not_offered_reason(role: str, provider: str, client: Any = None) -> str:
    if _offered_over_http(role, provider, client):
        return ""
    if role not in remote_role_providers(client):
        return (f"this role's provider is the server's configuration; HTTP does not choose it, except "
                f"`claude-cli` for planning and repair by a client granted `{HOST_TOOLS_PROPERTY}`")
    return CLI_ONLY_PROVIDERS.get(provider, "not a provider this role takes over HTTP")


def _role_default(role: str) -> tuple[str, str]:
    if role == "planner":
        from packages.orchestration.intake import resolve_planner_target
        provider, model = resolve_planner_target(None, None)
        return provider, model or ""
    from packages.orchestration.role_config import resolve_role_config
    config = resolve_role_config(role)
    return config.provider, config.model or ""


def execution_capabilities(client: Any = None) -> dict[str, Any]:
    """What this server offers CLIENT for an execution, read now from its own configuration.

    `GET /api/v1/execution` answers it for the calling token, `remedy client execution --json` for
    the server's own. `available` is measured (an executable found, the Ollama endpoint answering,
    an API key set) and never names a secret or a host path; `offered_over_http` and
    `selectable_over_http` are the server's rule for that caller (`remote_role_providers`, DECISION
    amend1023 D6), and `host_tools` says whether the caller holds the property.
    """
    from packages.orchestration.budget_profiles import budget_profiles_offer, provider_class
    from packages.orchestration.client_story_words import STORY_STEP_IDS
    from packages.orchestration.do_lane import DO_LANE_BOUNDED, DO_LANE_FULL, DO_LANE_HOLD
    from packages.orchestration.do_sequence import DO_SEQUENCE
    from packages.orchestration.order_file import ORDER_FILE_CAP_KEYS
    from packages.orchestration.order_verification import VERIFICATION_STATUSES
    from packages.orchestration.pi_loop_limits import pi_loop_limits
    from packages.orchestration.pi_provider import PiUnavailable, _ollama_models, ollama_host
    from packages.orchestration.public_api_writes import _ORDER_CREATE_FLAGS

    try:
        models: list[str] | None = sorted(m for m in _ollama_models(ollama_host()) if "embed" not in m)
    except PiUnavailable:
        models = None
    roles: dict[str, Any] = {}
    for role, providers in _ROLE_PROVIDERS.items():
        default_provider, default_model = _role_default(role)
        roles[role] = {
            "default_provider": default_provider, "default_model": default_model,
            "selectable_over_http": role in remote_role_providers(client),
            "providers": [{
                "id": provider, "available": _available(provider, models),
                "offered_over_http": _offered_over_http(role, provider, client),
                "isolation": _PROVIDER_ISOLATION[provider],
                "class": provider_class(provider),
                "not_offered_reason": _not_offered_reason(role, provider, client),
                "models": (models or []) if provider in ("pi", "ollama") else [],
            } for provider in providers],
        }
    limits = pi_loop_limits()
    return {
        HOST_TOOLS_PROPERTY: client_has_host_tools(client),
        "roles": roles,
        "lanes": [DO_LANE_BOUNDED, DO_LANE_FULL, DO_LANE_HOLD],
        "order_flags": list(_ORDER_CREATE_FLAGS),
        "budgets": {"order_header_caps": list(ORDER_FILE_CAP_KEYS), "body_strings": ["deadline"],
                    "an_order_needs_one_cap": True,
                    "pi_per_call": {"max_turns": limits.max_turns, "max_input_tokens": limits.max_input_tokens},
                    "profiles": budget_profiles_offer()},
        "verification": {"statuses": list(VERIFICATION_STATUSES), "command": "the project's own",
                         "command_over_http": False},
        "review_report": {"body_flag": "capture_review", "cli_flag": "--capture-review", "zip_newest": 10},
        "phases": {"do_steps": list(DO_SEQUENCE), "story_steps": list(STORY_STEP_IDS)},
        "observability": list(EXECUTION_OBSERVABILITY_ROUTES),
    }
