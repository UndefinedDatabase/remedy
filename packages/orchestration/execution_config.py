"""F306 T007, R-1235's second step — the execution configuration and its two serializers, split
out of ``pingpong_job``. F306's structure step (2) for ``run_job`` adds the configuration
resolution itself. This module holds the durable ``ExecutionConfig`` dataclass, its export/import
pair (``_export_execution_config`` and ``_import_execution_config``), the two field resolvers
``default_role_provider_name`` and ``_resolve_cfg``, and ``resolve_job_execution_config``, the
function that answers the whole record. Every consumer imports these names from here
(operator amendment amend1014-luna-mission-fixes D.2).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ExecutionConfig:
    """Durable execution config for job continuation."""
    builder: str = "fake"
    builder_source: str = "default"
    reviewer: str = "fake"
    reviewer_source: str = "default"
    builder_model: str = ""
    builder_model_source: str = "default"
    builder_effort: str = ""
    builder_effort_source: str = "default"
    reviewer_model: str = ""
    reviewer_model_source: str = "default"
    reviewer_effort: str = ""
    reviewer_effort_source: str = "default"
    repair_provider: str = ""
    repair_provider_source: str = "default"
    repair_model: str = ""
    repair_model_source: str = "default"
    repair_effort: str = ""
    repair_effort_source: str = "default"
    max_rounds: int = 3
    max_rounds_source: str = "default"
    repair_rounds_allowed: int = 2
    repair_rounds_source: str = "default"
    test_command: str = ""
    test_command_source: str = "default"
    claude_cli_write_mode: str = "none"
    claude_cli_write_mode_source: str = "default"
    context_strategy: str = "task_bounded_sequential_job"
    # F012 round 4 (F2): invocation-level controls that alter execution/evidence. Material
    # inputs, persisted with their source so `explicit > persisted > default` is auditable.
    timeout_sec: int = 120
    timeout_sec_source: str = "default"
    timeout_profile: str = ""
    timeout_profile_source: str = "default"
    max_output_chars: int = 50000
    max_output_chars_source: str = "default"
    stream_evidence: bool = False
    stream_evidence_source: str = "default"
    max_tasks: int = 0
    max_tasks_source: str = "default"
    # R-1235: the two claude-cli launch keys, with their source, so the record names what this
    # run's calls actually read.
    claude_cli_customizations: bool = False
    claude_cli_customizations_source: str = "default"
    claude_cli_all_tools: bool = False
    claude_cli_all_tools_source: str = "default"


def _export_execution_config(c: ExecutionConfig | None) -> dict[str, Any] | None:
    if c is None:
        return None
    return {
        "builder": c.builder,
        "builder_source": c.builder_source,
        "reviewer": c.reviewer,
        "reviewer_source": c.reviewer_source,
        "builder_model": c.builder_model,
        "builder_model_source": c.builder_model_source,
        "builder_effort": c.builder_effort,
        "builder_effort_source": c.builder_effort_source,
        "reviewer_model": c.reviewer_model,
        "reviewer_model_source": c.reviewer_model_source,
        "reviewer_effort": c.reviewer_effort,
        "reviewer_effort_source": c.reviewer_effort_source,
        "repair_provider": c.repair_provider,
        "repair_provider_source": c.repair_provider_source,
        "repair_model": c.repair_model,
        "repair_model_source": c.repair_model_source,
        "repair_effort": c.repair_effort,
        "repair_effort_source": c.repair_effort_source,
        "max_rounds": c.max_rounds,
        "max_rounds_source": c.max_rounds_source,
        "repair_rounds_allowed": c.repair_rounds_allowed,
        "repair_rounds_source": c.repair_rounds_source,
        "test_command": c.test_command,
        "test_command_present": bool(c.test_command),
        "test_command_source": c.test_command_source,
        "claude_cli_write_mode": c.claude_cli_write_mode,
        "claude_cli_write_mode_source": c.claude_cli_write_mode_source,
        "context_strategy": c.context_strategy,
        "timeout_sec": c.timeout_sec,
        "timeout_sec_source": c.timeout_sec_source,
        "timeout_profile": c.timeout_profile,
        "timeout_profile_source": c.timeout_profile_source,
        "max_output_chars": c.max_output_chars,
        "max_output_chars_source": c.max_output_chars_source,
        "stream_evidence": c.stream_evidence,
        "stream_evidence_source": c.stream_evidence_source,
        "max_tasks": c.max_tasks,
        "max_tasks_source": c.max_tasks_source,
        "claude_cli_customizations": c.claude_cli_customizations,
        "claude_cli_customizations_source": c.claude_cli_customizations_source,
        "claude_cli_all_tools": c.claude_cli_all_tools,
        "claude_cli_all_tools_source": c.claude_cli_all_tools_source,
    }


def _import_execution_config(d: dict[str, Any] | None) -> ExecutionConfig | None:
    if d is None:
        return None
    return ExecutionConfig(
        builder=d.get("builder", "fake"),
        builder_source=d.get("builder_source", "default"),
        reviewer=d.get("reviewer", "fake"),
        reviewer_source=d.get("reviewer_source", "default"),
        builder_model=d.get("builder_model", ""),
        builder_model_source=d.get("builder_model_source", "default"),
        builder_effort=d.get("builder_effort", ""),
        builder_effort_source=d.get("builder_effort_source", "default"),
        reviewer_model=d.get("reviewer_model", ""),
        reviewer_model_source=d.get("reviewer_model_source", "default"),
        reviewer_effort=d.get("reviewer_effort", ""),
        reviewer_effort_source=d.get("reviewer_effort_source", "default"),
        repair_provider=d.get("repair_provider", ""),
        repair_provider_source=d.get("repair_provider_source", "default"),
        repair_model=d.get("repair_model", ""),
        repair_model_source=d.get("repair_model_source", "default"),
        repair_effort=d.get("repair_effort", ""),
        repair_effort_source=d.get("repair_effort_source", "default"),
        max_rounds=d.get("max_rounds", 3),
        max_rounds_source=d.get("max_rounds_source", "default"),
        repair_rounds_allowed=d.get("repair_rounds_allowed", 2),
        repair_rounds_source=d.get("repair_rounds_source", "default"),
        test_command=d.get("test_command", ""),
        test_command_source=d.get("test_command_source", "default"),
        claude_cli_write_mode=d.get("claude_cli_write_mode", "none"),
        claude_cli_write_mode_source=d.get("claude_cli_write_mode_source", "default"),
        context_strategy=d.get("context_strategy", "task_bounded_sequential_job"),
        timeout_sec=int(d.get("timeout_sec", 120) or 120),
        timeout_sec_source=d.get("timeout_sec_source", "default"),
        timeout_profile=d.get("timeout_profile", ""),
        timeout_profile_source=d.get("timeout_profile_source", "default"),
        max_output_chars=int(d.get("max_output_chars", 50000) or 50000),
        max_output_chars_source=d.get("max_output_chars_source", "default"),
        stream_evidence=bool(d.get("stream_evidence", False)),
        stream_evidence_source=d.get("stream_evidence_source", "default"),
        max_tasks=int(d.get("max_tasks", 0) or 0),
        max_tasks_source=d.get("max_tasks_source", "default"),
        claude_cli_customizations=bool(d.get("claude_cli_customizations", False)),
        claude_cli_customizations_source=d.get("claude_cli_customizations_source", "default"),
        claude_cli_all_tools=bool(d.get("claude_cli_all_tools", False)),
        claude_cli_all_tools_source=d.get("claude_cli_all_tools_source", "default"),
    )


# The recorded provider must NAME WHAT ACTUALLY RAN: a literal default made an
# unflagged run report a provider it never used (finding R-0768). One function so
# ``run_job``'s own precedence chain stops being a rival answer to role_config's.
def default_role_provider_name(role: str, injected_provider: Any = None) -> str:
    """Return the provider name to record for ``role`` when nothing was given.

    Used as ``_resolve_cfg``'s product default, i.e. only when neither an
    explicit CLI value nor a persisted one exists. An INJECTED provider object
    wins, because that object is what will really run; otherwise the answer
    comes from ``role_config``, the single seam that owns provider defaults.

    ``role_config`` is imported inside the body on purpose: this module has no
    module-level import of it, and adding one risks an import cycle.
    """
    if injected_provider is not None:
        name = getattr(injected_provider, "name", None)
        if isinstance(name, str) and name:
            return name

    from packages.orchestration import role_config

    return role_config.resolve_role_config(role).provider


def _resolve_cfg(cli_val: Any, persisted_val: Any, default: Any) -> tuple[Any, str]:
    """Resolve config field: explicit CLI > persisted > product default."""
    if cli_val is not None:
        return cli_val, "cli"
    if persisted_val is not None:
        return persisted_val, "persisted"
    return default, "default"


def _resolve_invocation_controls(
    ec: ExecutionConfig | None, *, timeout_sec: int | None, timeout_profile: str | None,
    max_output_chars: int | None, stream_evidence: bool | None, max_tasks: int | None,
    providers: tuple[str, ...] = (),
) -> dict[str, Any]:
    """Resolve the five invocation-level controls and their sources, keyed for the construction."""
    # F3: resolve the invocation-level controls with an OMISSION SENTINEL (None). Only a value
    # the caller actually supplied (``passed is not None``) is an explicit invocation — so an
    # explicit value that happens to equal the product default STILL overrides a persisted one,
    # and an omitted flag never masquerades as an explicit default. Precedence is strictly
    # explicit(non-None) > persisted > product default, mirroring ``_resolve_cfg``.
    def _resolve_inv(passed: Any, default: Any, persisted: Any):
        if passed is not None:
            return passed, "invocation"
        if persisted is not None:
            return persisted, "persisted"
        return default, "default"

    from packages.orchestration.provider_timeouts import PI_DEFAULT_TIMEOUT_SEC

    # amend1014c R2: Pi's longer agent loop is a DEFAULT, never a floor an explicit value is raised to.
    _ts_default = PI_DEFAULT_TIMEOUT_SEC if "pi" in providers else 120
    _ts, _ts_src = _resolve_inv(timeout_sec, _ts_default, ec.timeout_sec if ec else None)
    _tp, _tp_src = _resolve_inv(timeout_profile, "", ec.timeout_profile if ec else None)
    _moc, _moc_src = _resolve_inv(max_output_chars, 50000,
                                  ec.max_output_chars if ec else None)
    _se, _se_src = _resolve_inv(stream_evidence, False, ec.stream_evidence if ec else None)
    _mt, _mt_src = _resolve_inv(max_tasks, 0, ec.max_tasks if ec else None)
    return {
        "timeout_sec": _ts, "timeout_sec_source": _ts_src,
        "timeout_profile": _tp, "timeout_profile_source": _tp_src,
        "max_output_chars": _moc, "max_output_chars_source": _moc_src,
        "stream_evidence": _se, "stream_evidence_source": _se_src,
        "max_tasks": _mt, "max_tasks_source": _mt_src,
    }


def _resolve_claude_cli_launch_config(config: Any = None) -> dict[str, Any]:
    """Read the two claude-cli launch keys fresh, each with its source, for the four
    ``ExecutionConfig`` fields R-1235 asks a job's record to carry.

    ``config`` defaults to the process's cached ``get_config()`` — imported inside the body, the
    way ``claude_cli_command`` itself does. Each key's value is read through
    ``claude_cli_command._claude_cli_flag``, the same reading ``claude_cli_launch_switches`` uses
    for the call this run is about to make, so the recorded value can never drift from what ran.
    """
    if config is None:
        from packages.orchestration.config import get_config

        config = get_config()
    from packages.orchestration import claude_cli_command

    result: dict[str, Any] = {}
    for field, key in (
        ("claude_cli_customizations", "claude_cli.customizations"),
        ("claude_cli_all_tools", "claude_cli.all_tools"),
    ):
        result[field] = claude_cli_command._claude_cli_flag(config, key)
        source = config.get_source(key)
        result[f"{field}_source"] = source.value if source is not None else "default"
    return result


# F306, the structure ledger's step (2) for `run_job`: `run_job` no longer resolves its own
# configuration inline — this is the single function that does, so the recorded answer and the
# running job can never drift apart.
def resolve_job_execution_config(
    persisted: ExecutionConfig | None, *,
    builder_name: str | None = None, reviewer_name: str | None = None,
    builder_provider: Any = None, reviewer_provider: Any = None,
    builder_model: str | None = None, builder_effort: str | None = None,
    reviewer_model: str | None = None, reviewer_effort: str | None = None,
    repair_provider_name: str | None = None, repair_model: str | None = None,
    repair_effort: str | None = None, max_rounds: int | None = None,
    repair_rounds: int | None = None, repair_rounds_source: str | None = None,
    test_command: str | None = None, timeout_sec: int | None = None,
    timeout_profile: str | None = None, max_output_chars: int | None = None,
    claude_cli_write_mode: str | None = None, stream_evidence: bool | None = None,
    max_tasks: int | None = None, config: Any = None,
) -> ExecutionConfig:
    """Answer ``explicit > persisted > product default`` per execution-config field.

    ``run_job`` records exactly the answer this returns. The two claude-cli launch keys,
    ``claude_cli_customizations`` and ``claude_cli_all_tools``, are the one exception to that
    precedence chain: they are read fresh from ``config`` (R-1235), never from ``persisted``.
    """
    ec = persisted

    builder_name, builder_src = _resolve_cfg(
        builder_name, ec.builder if ec else None,
        default_role_provider_name("builder", builder_provider))
    reviewer_name, reviewer_src = _resolve_cfg(
        reviewer_name, ec.reviewer if ec else None,
        default_role_provider_name("reviewer", reviewer_provider))
    max_rounds, max_rounds_src = _resolve_cfg(
        max_rounds, ec.max_rounds if ec else None, 3)
    test_command, test_cmd_src = _resolve_cfg(
        test_command, ec.test_command if ec else None, "")
    # DECISION amend0923-selfuse-write D3, repairing R-1043: the BUILDER's
    # product default is "allowed-tools", not "none". A builder with no write
    # tool cannot change a file, so three consecutive self-use closures — F277,
    # F283 and F278 — recorded `claude_cli_write_mode: none` with source
    # `default` and returned an empty diff by construction. The builder works in
    # an isolated worktree and the approval gate in job_apply.py still stands
    # between that worktree and the branch, so this widens nothing that was not
    # already gated. THE REVIEWER IS NOT AFFECTED: its "none" is hard-coded in
    # pingpong_loop._create_provider_with_cwd and _build_provider_evidence, and
    # a reviewer that can edit what it reviews can make its verdict true.
    claude_cli_write_mode, write_mode_src = _resolve_cfg(
        claude_cli_write_mode,
        ec.claude_cli_write_mode if ec else None, "allowed-tools")

    if repair_rounds is not None:
        rr_src = repair_rounds_source or "cli"
    elif ec is not None:
        repair_rounds = ec.repair_rounds_allowed
        rr_src = "persisted"
    else:
        repair_rounds = 2
        rr_src = "default"

    builder_model, bm_src = _resolve_cfg(
        builder_model, ec.builder_model if ec else None, "")
    builder_effort, be_src = _resolve_cfg(
        builder_effort, ec.builder_effort if ec else None, "")
    reviewer_model, rm_src = _resolve_cfg(
        reviewer_model, ec.reviewer_model if ec else None, "")
    reviewer_effort, re_src = _resolve_cfg(
        reviewer_effort, ec.reviewer_effort if ec else None, "")
    repair_provider_name, rp_src = _resolve_cfg(
        repair_provider_name, ec.repair_provider if ec else None, "")
    repair_model, rpm_src = _resolve_cfg(
        repair_model, ec.repair_model if ec else None, "")
    repair_effort, rpe_src = _resolve_cfg(
        repair_effort, ec.repair_effort if ec else None, "")

    return ExecutionConfig(
        builder=builder_name, builder_source=builder_src,
        reviewer=reviewer_name, reviewer_source=reviewer_src,
        builder_model=builder_model, builder_model_source=bm_src,
        builder_effort=builder_effort, builder_effort_source=be_src,
        reviewer_model=reviewer_model, reviewer_model_source=rm_src,
        reviewer_effort=reviewer_effort, reviewer_effort_source=re_src,
        repair_provider=repair_provider_name, repair_provider_source=rp_src,
        repair_model=repair_model, repair_model_source=rpm_src,
        repair_effort=repair_effort, repair_effort_source=rpe_src,
        max_rounds=max_rounds, max_rounds_source=max_rounds_src,
        repair_rounds_allowed=repair_rounds, repair_rounds_source=rr_src,
        test_command=test_command, test_command_source=test_cmd_src,
        claude_cli_write_mode=claude_cli_write_mode,
        claude_cli_write_mode_source=write_mode_src,
        **_resolve_invocation_controls(
            ec, timeout_sec=timeout_sec, timeout_profile=timeout_profile,
            max_output_chars=max_output_chars, stream_evidence=stream_evidence,
            max_tasks=max_tasks, providers=(builder_name, reviewer_name, repair_provider_name or "")),
        **_resolve_claude_cli_launch_config(config),
    )
