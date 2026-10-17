"""The execution offer's part of the machine client interface (operator order exec-1017, D6).

`apps/cli/client_interface.py` imports from here the answer keys and the key tree of
`remedy client execution` (`GET /api/v1/execution`), so that module stays below the structure
ratchet's limit. The answer itself is `packages.orchestration.execution_options.execution_capabilities`.
"""

from __future__ import annotations

from typing import Any

#: The top-level keys `remedy client execution --json` answers beside the envelope's own.
CLIENT_EXECUTION_ANSWER_KEYS: tuple[str, ...] = (
    "budgets", "lanes", "observability", "order_flags", "phases", "review_report", "roles", "verification",
)

#: The keys under them; under `roles` each key is a role name.
CLIENT_EXECUTION_KEY_TREE: dict[str, Any] = {
    "roles": {"*": {"default_provider": {}, "default_model": {}, "selectable_over_http": {}, "providers": {
        "id": {}, "available": {}, "offered_over_http": {}, "isolation": {}, "not_offered_reason": {},
        "models": {}}}},
    "budgets": {"order_header_caps": {}, "body_strings": {}, "an_order_needs_one_cap": {},
                "pi_per_call": {"max_turns": {}, "max_input_tokens": {}}},
    "verification": {"statuses": {}, "command": {}, "command_over_http": {}},
    "review_report": {"body_flag": {}, "cli_flag": {}, "zip_newest": {}},
    "phases": {"do_steps": {}, "story_steps": {}},
}
