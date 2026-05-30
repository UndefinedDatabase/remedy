"""Policy group command handlers."""

from __future__ import annotations

import json as _json
import sys
from typing import TYPE_CHECKING, Callable
from uuid import UUID

from packages.orchestration.storage import JobNotFoundError, load_job

if TYPE_CHECKING:
    import argparse


def _cmd_run_contract(job_id_str: str, *, json_output: bool = False) -> None:
    try:
        job_id = UUID(job_id_str)
    except ValueError:
        print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.run_contract import (
        build_default_run_contract, export_run_contract_json, summarize_run_contract,
    )
    from packages.orchestration.run_log import RunLogWriter

    contract = build_default_run_contract(job)
    if json_output:
        print(_json.dumps(export_run_contract_json(contract), sort_keys=True))
    else:
        print(summarize_run_contract(contract))

    log = RunLogWriter(job_id=job.id)
    log.log(
        "run_contract_inspected",
        autonomy_level=contract.autonomy_level,
        allowed_action_count=len(contract.allowed_actions),
        denied_action_count=len(contract.denied_actions),
        max_loops=contract.max_loops, scope=contract.scope,
    )


def _cmd_token_policy(job_id_str: str, *, json_output: bool = False) -> None:
    try:
        job_id = UUID(job_id_str)
    except ValueError:
        print(f"Error: invalid job ID: {job_id_str!r}", file=sys.stderr)
        sys.exit(1)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.token_policy import (
        build_default_token_policy, export_token_policy_json, summarize_token_policy,
    )
    from packages.orchestration.run_log import RunLogWriter

    policy = build_default_token_policy(job)
    if json_output:
        print(_json.dumps(export_token_policy_json(policy), sort_keys=True))
    else:
        print(summarize_token_policy(policy))

    log = RunLogWriter(job_id=job.id)
    log.log(
        "token_policy_inspected", scope=policy.scope,
        zero_token_step_count=len(policy.zero_token_steps),
        local_first_step_count=len(policy.local_first_steps),
        expensive_step_count=len(policy.expensive_model_steps),
    )


def _cmd_token_explain() -> None:
    print(
        "Token Economy Policy\n"
        "\n"
        "Remedy routes work through a token-aware pipeline:\n"
        "\n"
        "  Zero-token steps: command discovery, risk assessment, permission\n"
        "    checks, brain graph construction — pure local Python, no LLM.\n"
        "\n"
        "  Local-first steps: planning, verification, constitution checks —\n"
        "    prefer cheap local models (e.g. Ollama).\n"
        "\n"
        "  Expensive steps: artifact generation, complex refactoring —\n"
        "    require frontier models, budget-capped.\n"
        "\n"
        "  Prohibited payloads: raw credentials, API keys, secrets,\n"
        "    raw command output, artifact content — never sent to LLM.\n"
        "\n"
        "  Default mode: caveman (minimal tokens). Modes: caveman, compact,\n"
        "    standard — ordered by token usage.\n"
        "\n"
        "  Local-first: always true. Remote models require approval.\n"
        "  No provider execution without explicit human approval.\n"
    )


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "policy.contract": lambda args: _cmd_run_contract(args.job_id, json_output=args.json),
    "policy.token": lambda args: _cmd_token_policy(args.job_id, json_output=args.json),
    "policy.token-explain": lambda args: _cmd_token_explain(),
}
