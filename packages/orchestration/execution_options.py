"""What a remote client may choose for an execution, decided by the server (exec-1017 D6).

`POST /api/v1/orders` and `POST /api/v1/jobs/{job}/run` take `builder_provider` and
`reviewer_provider` from their body and pass them to `remedy do` / `remedy job run`. Until
exec-1017 they passed any value the command line accepts, `claude-cli` included: the Claude Code
CLI runs with the host's file and shell tools OUTSIDE the tool sandbox every Pi call runs in
(DECISION amend1016sb D1 covers Pi only), so a token holder could have asked the server to run an
unsandboxed agent over a repository. Remedy deliberately does not offer that over HTTP until its
isolation is verified; it stays a command-line choice of the operator. A provider HTTP does not
offer is refused before anything starts with 400 `api_provider_not_offered`, never substituted.
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

#: Providers the command line offers that HTTP does not, each with the reason a client is told.
CLI_ONLY_PROVIDERS: dict[str, str] = {
    "claude-cli": ("the Claude Code CLI runs with the host's file and shell tools outside Remedy's "
                   "tool sandbox, so it is offered on the operator's command line only"),
}


def remote_provider_refusal(body: dict[str, Any]) -> str:
    """The sentence refusing a body's `builder_provider` or `reviewer_provider`, or "" when both are offered."""
    for role, offered in REMOTE_ROLE_PROVIDERS.items():
        value = body.get(f"{role}_provider")
        if value is None or value in offered:
            continue
        why = CLI_ONLY_PROVIDERS.get(str(value), "it is not a provider of this role")
        return (f"{role}_provider {value!r} is not offered over HTTP: {why}; offered: "
                f"{', '.join(offered)}. Nothing was started.")
    for role in REMOTE_ROLE_PROVIDERS:
        value = body.get(f"{role}_provider")
        if value in ("pi", "claude") and not _available(value, None):
            return (f"{role}_provider {value!r} is offered but not available on this server (see GET "
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


def _not_offered_reason(role: str, provider: str) -> str:
    if provider in REMOTE_ROLE_PROVIDERS.get(role, ()):
        return ""
    if role not in REMOTE_ROLE_PROVIDERS:
        return "this role's provider is the server's configuration; HTTP does not choose it"
    return CLI_ONLY_PROVIDERS.get(provider, "not a provider this role takes over HTTP")


def _role_default(role: str) -> tuple[str, str]:
    if role == "planner":
        from packages.orchestration.intake import resolve_planner_target
        provider, model = resolve_planner_target(None, None)
        return provider, model or ""
    from packages.orchestration.role_config import resolve_role_config
    config = resolve_role_config(role)
    return config.provider, config.model or ""


def execution_capabilities() -> dict[str, Any]:
    """What this server offers a client for an execution, read now from its own configuration.

    `GET /api/v1/execution` and `remedy client execution --json` answer it. `available` is measured
    (an executable found, the Ollama endpoint answering, an API key set) and never names a secret or
    a host path; `offered_over_http` is the server's rule (`REMOTE_ROLE_PROVIDERS`).
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
            "selectable_over_http": role in REMOTE_ROLE_PROVIDERS,
            "providers": [{
                "id": provider, "available": _available(provider, models),
                "offered_over_http": provider in REMOTE_ROLE_PROVIDERS.get(role, ()),
                "isolation": _PROVIDER_ISOLATION[provider],
                "class": provider_class(provider),
                "not_offered_reason": _not_offered_reason(role, provider),
                "models": (models or []) if provider in ("pi", "ollama") else [],
            } for provider in providers],
        }
    limits = pi_loop_limits()
    return {
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
