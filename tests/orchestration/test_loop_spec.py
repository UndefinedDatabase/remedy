"""F045 T001 — unit tests for the loop spec model, loading and validation.

Every test writes its OWN remedy.toml under ``tmp_path`` and passes that path
explicitly. Nothing here may depend on a repo-level ``remedy.toml``: the
repository deliberately has none, and a test that started needing one would be
asserting about the operator's machine rather than about this module.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from packages.orchestration.config import load_config
from packages.orchestration.loop_spec import (
    INERT_TRIGGER_NOTICE,
    LOOP_TABLE_KEY,
    LoopSpecError,
    load_loop_specs,
    validate_loop_specs,
)


def _write(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "remedy.toml"
    path.write_text(body, encoding="utf-8")
    return path


def test_fully_populated_loop_round_trips(tmp_path: Path) -> None:
    path = _write(tmp_path, """
[[loop]]
name = "nightly-tidy"
unattended = true
report = true
notify = true

[loop.trigger]
kind = "manual"

[loop.scope]
paths = ["packages/", "tests/"]
queue = "maintenance"

[loop.action]
kind = "job"
goal_template = "tidy {project} on {date}"

[loop.budgets]
max_total_tokens = 50000
max_provider_calls = 12
max_wall_clock_minutes = 30
max_cost_usd = 1.5
deadline = "2026-09-01T00:00:00+00:00"

[loop.stop]
max_runs = 7
stop_on_failure = false
""")
    (spec,) = load_loop_specs(path)
    assert spec.name == "nightly-tidy"
    assert spec.unattended is True and spec.report is True and spec.notify is True
    assert spec.trigger.kind == "manual"
    assert spec.scope is not None
    assert spec.scope.paths == ["packages/", "tests/"]
    assert spec.scope.queue == "maintenance"
    assert spec.action.kind == "job"
    assert spec.action.goal_template == "tidy {project} on {date}"
    assert spec.action.mission is None
    assert spec.budgets is not None
    assert spec.budgets.max_total_tokens == 50000
    assert spec.budgets.max_provider_calls == 12
    assert spec.budgets.max_wall_clock_minutes == 30
    assert spec.budgets.max_cost_usd == 1.5
    assert spec.budgets.deadline == "2026-09-01T00:00:00+00:00"
    assert spec.stop is not None
    assert spec.stop.max_runs == 7
    assert spec.stop.stop_on_failure is False
    assert validate_loop_specs(path) == []


def test_missing_config_file_is_not_an_error(tmp_path: Path) -> None:
    missing = tmp_path / "remedy.toml"
    assert not missing.exists()
    assert load_loop_specs(missing) == ()
    assert validate_loop_specs(missing) == []


def test_duplicate_names_rejected_with_the_name_in_the_message(tmp_path: Path) -> None:
    path = _write(tmp_path, """
[[loop]]
name = "twice"
action = { kind = "job", goal_template = "a" }

[[loop]]
name = "twice"
action = { kind = "job", goal_template = "b" }
""")
    errors = validate_loop_specs(path)
    assert errors == ["loop 'twice': duplicate loop name"]
    with pytest.raises(LoopSpecError) as excinfo:
        load_loop_specs(path)
    assert str(excinfo.value) == "loop 'twice': duplicate loop name"
    assert excinfo.value.loop_name == "twice"


def test_unknown_key_rejected_with_the_loop_name_and_the_key(tmp_path: Path) -> None:
    path = _write(tmp_path, """
[[loop]]
name = "typo-carrier"
cadence = "daily"
action = { kind = "job", goal_template = "a" }
""")
    errors = validate_loop_specs(path)
    assert errors == ["loop 'typo-carrier': unknown key 'cadence'"]
    assert "typo-carrier" in errors[0] and "cadence" in errors[0]


def test_missing_action_rejected_with_the_loop_name(tmp_path: Path) -> None:
    path = _write(tmp_path, """
[[loop]]
name = "actionless"
""")
    assert validate_loop_specs(path) == ["loop 'actionless': action is required"]


def test_malformed_budget_rejected_with_the_loop_name(tmp_path: Path) -> None:
    path = _write(tmp_path, """
[[loop]]
name = "zero-budget"
action = { kind = "job", goal_template = "a" }
budgets = { max_total_tokens = 0 }
""")
    assert validate_loop_specs(path) == [
        "loop 'zero-budget': budgets.max_total_tokens must be a positive integer"
    ]


def test_naive_deadline_rejected_but_aware_deadline_accepted(tmp_path: Path) -> None:
    naive = _write(tmp_path, """
[[loop]]
name = "no-tz"
action = { kind = "job", goal_template = "a" }
budgets = { deadline = "2026-09-01T00:00:00" }
""")
    assert validate_loop_specs(naive) == [
        "loop 'no-tz': budgets.deadline must be an ISO 8601 timestamp with a timezone"
    ]

    aware_dir = tmp_path / "aware"
    aware_dir.mkdir()
    aware = _write(aware_dir, """
[[loop]]
name = "with-tz"
action = { kind = "job", goal_template = "a" }
budgets = { deadline = "2026-09-01T00:00:00+00:00" }
""")
    assert validate_loop_specs(aware) == []
    (spec,) = load_loop_specs(aware)
    assert spec.budgets is not None
    assert spec.budgets.deadline == "2026-09-01T00:00:00+00:00"


def test_schedule_trigger_is_valid_and_inert(tmp_path: Path) -> None:
    path = _write(tmp_path, """
[[loop]]
name = "nightly"
action = { kind = "job", goal_template = "a" }
trigger = { kind = "schedule", schedule = "0 3 * * *" }
""")
    assert validate_loop_specs(path) == []
    (spec,) = load_loop_specs(path)
    assert spec.trigger.schedule == "0 3 * * *"
    assert spec.is_inert is True
    assert INERT_TRIGGER_NOTICE == "scheduler not yet available; ran on demand"


def test_manual_trigger_is_not_inert(tmp_path: Path) -> None:
    path = _write(tmp_path, """
[[loop]]
name = "on-demand"
action = { kind = "mission", mission = "cleanup" }
""")
    (spec,) = load_loop_specs(path)
    assert spec.trigger.kind == "manual"
    assert spec.is_inert is False


def test_undefined_goal_template_variable_fails_validation(tmp_path: Path) -> None:
    bad = _write(tmp_path, """
[[loop]]
name = "bad-template"
action = { kind = "job", goal_template = "tidy {repo} for {project}" }
""")
    assert validate_loop_specs(bad) == [
        "loop 'bad-template': goal_template references undefined variable 'repo'"
    ]

    good_dir = tmp_path / "good"
    good_dir.mkdir()
    good = _write(good_dir, """
[[loop]]
name = "good-template"
action = { kind = "job", goal_template = "tidy {project} on {date}" }
""")
    assert validate_loop_specs(good) == []


def test_unnamed_entry_is_reported_by_index(tmp_path: Path) -> None:
    path = _write(tmp_path, """
[[loop]]
name = "named"
action = { kind = "job", goal_template = "a" }

[[loop]]
action = { kind = "job", goal_template = "b" }
""")
    assert validate_loop_specs(path) == ["loop #2 (no name): name is required"]


def test_validate_returns_every_error_not_just_the_first(tmp_path: Path) -> None:
    path = _write(tmp_path, """
[[loop]]
name = "first-bad"
action = { kind = "job" }

[[loop]]
name = "second-bad"
action = { kind = "mission" }
""")
    assert validate_loop_specs(path) == [
        "loop 'first-bad': action.goal_template is required for a job action",
        "loop 'second-bad': action.mission is required for a mission action",
    ]


def test_top_level_loop_table_produces_no_config_warning(tmp_path: Path) -> None:
    """DECISION D1 pinned: the loop table is invisible to load_config.

    ``load_config`` reads only the ``[remedy]`` table, so a top-level
    ``[[loop]]`` array never reaches its unknown-key check. Moving the table
    under ``[remedy]`` would make this assertion fail. The user path is pinned
    at a non-existent file so the assertion is about this config, not about
    whatever ``~/.config/remedy/remedy.toml`` happens to contain.

    The assertion scans the KEY each warning names, not the whole warning
    string: pytest's ``tmp_path`` embeds the test's own name, so this test's
    directory literally contains the word "loop" and a whole-string scan would
    match any unrelated warning purely because of where the file was written.
    """
    path = _write(tmp_path, """
[remedy]
external_memory_enabled = true

[[loop]]
name = "nightly-tidy"
action = { kind = "job", goal_template = "tidy {project}" }
budgets = { max_total_tokens = 100 }
""")
    config = load_config(project_path=path, user_path=tmp_path / "absent-user.toml")
    assert config.load_report.project_loaded is True
    reported_keys = [w.rsplit(": ", 1)[-1] for w in config.load_report.warnings
                     if w.startswith("Unknown key in ")]
    assert reported_keys == []
    assert [k for k in reported_keys if "loop" in k] == []
    assert LOOP_TABLE_KEY == "loop"
    # The same file still parses as one valid loop for this module.
    assert [s.name for s in load_loop_specs(path)] == ["nightly-tidy"]


def test_mission_template_accepts_the_defined_variables(tmp_path: Path) -> None:
    """DECISION D4: action.mission is a goal TEMPLATE, so {project}/{date} pass."""
    path = _write(tmp_path, """
[[loop]]
name = "weekly-review"
action = { kind = "mission", mission = "review {project} for the week of {date}" }
""")
    assert validate_loop_specs(path) == []
    (spec,) = load_loop_specs(path)
    assert spec.action.mission == "review {project} for the week of {date}"


def test_undefined_mission_template_variable_fails_validation(tmp_path: Path) -> None:
    """DECISION D4: an undefined placeholder fails VALIDATION, not run time (A9)."""
    path = _write(tmp_path, """
[[loop]]
name = "bad-mission"
action = { kind = "mission", mission = "review {sprint}" }
""")
    assert validate_loop_specs(path) == [
        "loop 'bad-mission': action.mission references undefined variable 'sprint'"
    ]
