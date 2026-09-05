"""CLI handlers for the config command group."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def _redact_path(raw: str | None) -> str | None:
    """Replace absolute paths with ~ prefix or <project> tag for public display."""
    if raw is None:
        return None
    p = Path(raw)
    if not p.is_absolute():
        return raw
    try:
        relative = p.relative_to(Path.home())
        return f"~/{relative}"
    except ValueError:
        return "<absolute-path-redacted>"


def _cmd_config_list(args: argparse.Namespace) -> None:
    from packages.orchestration.config import all_key_specs, get_config
    from packages.orchestration.list_options import ListOptionError, apply_list_options

    config = get_config()
    use_json = getattr(args, "json", False)

    try:
        specs = apply_list_options(
            list(all_key_specs()),
            sort=getattr(args, "sort", None),
            desc=getattr(args, "desc", False),
            since=getattr(args, "since", None),
            until=getattr(args, "until", None),
            limit=getattr(args, "limit", None),
            sort_fields={"key": lambda s: s.key},
            default_sort_field=None,
            date_getter=None,
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if use_json:
        entries = []
        for spec in specs:
            cv = config.get_value(spec.key)
            val = cv.value if cv else None
            if spec.secret or spec.env_only:
                val = "[REDACTED]" if val is not None else None
            entries.append({
                "key": spec.key,
                "value": val,
                "source": cv.source.value if cv else "unknown",
                "env_var": spec.env_var,
                "type": spec.value_type.__name__,
                "is_default": cv.is_default if cv else True,
            })
        json.dump(entries, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return

    for spec in specs:
        cv = config.get_value(spec.key)
        val = cv.value if cv else None
        source = cv.source.value if cv else "default"
        if spec.secret or spec.env_only:
            val = "[REDACTED]" if val is not None else None
        val_str = str(val) if val is not None else "(not set)"
        print(f"  {spec.key:40s} = {val_str:30s} [{source}]")


def _cmd_config_get(args: argparse.Namespace) -> None:
    from packages.orchestration.config import get_config, get_key_spec

    key = args.key
    spec = get_key_spec(key)
    config = get_config()
    cv = config.get_value(key)
    use_json = getattr(args, "json", False)

    if cv is None and spec is None:
        print(f"Unknown config key: {key}", file=sys.stderr)
        sys.exit(1)

    val = cv.value if cv else None
    source = cv.source.value if cv else "default"
    if spec and (spec.secret or spec.env_only):
        val = "[REDACTED]" if val is not None else None

    if use_json:
        json.dump({
            "key": key,
            "value": val,
            "source": source,
            "env_var": spec.env_var if spec else None,
            "description": spec.description if spec else None,
        }, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return

    val_str = str(val) if val is not None else "(not set)"
    print(f"{key} = {val_str}")
    print(f"  source: {source}")
    if spec:
        print(f"  env var: {spec.env_var}")
        print(f"  type: {spec.value_type.__name__}")
        print(f"  description: {spec.description}")


def _cmd_config_sources(args: argparse.Namespace) -> None:
    from packages.orchestration.config import get_config

    config = get_config()
    report = config.load_report
    use_json = getattr(args, "json", False)

    if use_json:
        json.dump({
            "project_path": _redact_path(report.project_path),
            "project_loaded": report.project_loaded,
            "user_path": _redact_path(report.user_path),
            "user_loaded": report.user_loaded,
            "warnings": report.warnings,
        }, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return

    print("Config sources:")
    status = "loaded" if report.project_loaded else "not found"
    print(f"  project: {_redact_path(report.project_path)} ({status})")
    status = "loaded" if report.user_loaded else "not found"
    print(f"  user:    {_redact_path(report.user_path)} ({status})")
    if report.warnings:
        print("\nWarnings:")
        for w in report.warnings:
            print(f"  - {w}")


def _cmd_config_init(args: argparse.Namespace) -> None:
    from packages.orchestration.config import write_toml_template

    path = Path(getattr(args, "path", None) or "remedy.toml")
    use_json = getattr(args, "json", False)

    if path.exists():
        msg = f"{path} already exists. Not overwriting."
        if use_json:
            json.dump({"error": msg}, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(msg, file=sys.stderr)
        sys.exit(1)

    write_toml_template(path)
    if use_json:
        json.dump({"created": str(path)}, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"Created {path}")


def _cmd_config_set(args: argparse.Namespace) -> None:
    from packages.orchestration.config import reset_config, set_config_value

    key = args.key
    value = args.value
    use_json = getattr(args, "json", False)
    target = Path(getattr(args, "path", None) or "remedy.toml")

    try:
        set_config_value(target, key, value)
    except ValueError as exc:
        if use_json:
            json.dump({"error": str(exc)}, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(str(exc), file=sys.stderr)
        sys.exit(1)

    reset_config()
    if use_json:
        json.dump({"key": key, "value": value, "path": str(target)}, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"Set {key} = {value} in {target}")


def _cmd_config_validate(args: argparse.Namespace) -> None:
    from packages.orchestration.config import get_config, validate_config

    config = get_config()
    warnings = validate_config(config)
    use_json = getattr(args, "json", False)

    if use_json:
        json.dump({"valid": len(warnings) == 0, "warnings": warnings}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return

    if warnings:
        print("Config validation warnings:")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("Config validation: OK")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "config.list": _cmd_config_list,
    "config.show": _cmd_config_list,
    "config.get": _cmd_config_get,
    "config.sources": _cmd_config_sources,
    "config.init": _cmd_config_init,
    "config.set": _cmd_config_set,
    "config.validate": _cmd_config_validate,
}
