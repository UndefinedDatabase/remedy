"""CLI handlers for the config command group."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def _cmd_config_list(args: argparse.Namespace) -> None:
    from packages.orchestration.config import all_key_specs, get_config

    config = get_config()
    use_json = getattr(args, "json", False)

    if use_json:
        entries = []
        for spec in all_key_specs():
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

    for spec in all_key_specs():
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
            "project_path": report.project_path,
            "project_loaded": report.project_loaded,
            "user_path": report.user_path,
            "user_loaded": report.user_loaded,
            "warnings": report.warnings,
        }, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return

    print("Config sources:")
    status = "loaded" if report.project_loaded else "not found"
    print(f"  project: {report.project_path} ({status})")
    status = "loaded" if report.user_loaded else "not found"
    print(f"  user:    {report.user_path} ({status})")
    if report.warnings:
        print("\nWarnings:")
        for w in report.warnings:
            print(f"  - {w}")


def _cmd_config_init(args: argparse.Namespace) -> None:
    from packages.orchestration.config import write_toml_template

    path = Path("remedy.toml")
    if path.exists():
        print(f"{path} already exists. Not overwriting.", file=sys.stderr)
        sys.exit(1)
    write_toml_template(path)
    print(f"Created {path}")


def _cmd_config_set(args: argparse.Namespace) -> None:
    from packages.orchestration.config import get_key_spec, reset_config, set_config_value

    key = args.key
    value = args.value
    spec = get_key_spec(key)

    if spec and spec.env_only:
        print(f"Key {key!r} is env-only. Set via {spec.env_var} environment variable.", file=sys.stderr)
        sys.exit(1)

    path = Path("remedy.toml")
    set_config_value(path, key, value)
    reset_config()
    print(f"Set {key} = {value} in {path}")


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
    "config.get": _cmd_config_get,
    "config.sources": _cmd_config_sources,
    "config.init": _cmd_config_init,
    "config.set": _cmd_config_set,
    "config.validate": _cmd_config_validate,
}
