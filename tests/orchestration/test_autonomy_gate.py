"""A test per matrix cell and per refusal of the autonomy level (F078, DECISION F078 D1).

Every config is built with ``load_config(project_path=..., user_path=...)`` over files under
``tmp_path``, with ``root=tmp_path / "data"`` passed to :func:`load_autonomy_policy` so nothing
this module runs ever touches the real data root.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from packages.orchestration.autonomy_gate import (
    AUTONOMY_LEVELS,
    AUTONOMY_START_MATRIX,
    START_ORIGINS,
    AutonomyConfigError,
    AutonomyPolicy,
    autonomy_may_start,
    load_autonomy_policy,
)
from packages.orchestration.config import load_config

EXPECTED_MATRIX: dict[tuple[str, str], bool] = {
    ("manual", "L2"): True,
    ("manual", "L3"): True,
    ("manual", "L4"): True,
    ("manual", "L5"): True,
    ("orchestrator", "L2"): False,
    ("orchestrator", "L3"): True,
    ("orchestrator", "L4"): True,
    ("orchestrator", "L5"): True,
    ("order-file", "L2"): False,
    ("order-file", "L3"): False,
    ("order-file", "L4"): True,
    ("order-file", "L5"): True,
    ("idea", "L2"): False,
    ("idea", "L3"): False,
    ("idea", "L4"): False,
    ("idea", "L5"): True,
}


def _load(tmp_path, project: str | None = None, user: str | None = None):
    """Load a config over ``project.toml`` / ``user.toml`` under ``tmp_path``.

    A file is written only when its text is given; otherwise the path is passed to
    ``load_config`` unwritten, which resolves it as a config source of nothing.
    """
    project_path = tmp_path / "project.toml"
    user_path = tmp_path / "user.toml"
    if project is not None:
        project_path.write_text(project, encoding="utf-8")
    if user is not None:
        user_path.write_text(user, encoding="utf-8")
    return load_config(project_path=project_path, user_path=user_path)


def _write_passing_evidence(tmp_path, name: str = "matrix.json"):
    evidence = tmp_path / name
    evidence.write_text(json.dumps({"passed": True}), encoding="utf-8")
    return evidence


def _change_lines(root):
    path = root / "autonomy" / "level_changes.jsonl"
    if not path.is_file():
        return []
    return path.read_text(encoding="utf-8").splitlines()


# ---------------------------------------------------------------------------
# (a) every matrix cell, and the matrix's own shape
# ---------------------------------------------------------------------------


def test_matrix_keys_are_the_product_of_origins_and_levels():
    assert set(AUTONOMY_START_MATRIX) == set(EXPECTED_MATRIX)
    assert set(AUTONOMY_START_MATRIX) == {(o, lvl) for o in START_ORIGINS for lvl in AUTONOMY_LEVELS}


@pytest.mark.parametrize(
    "origin,level", list(EXPECTED_MATRIX),
    ids=[f"{origin}-{level}" for origin, level in EXPECTED_MATRIX],
)
def test_matrix_cell(origin, level):
    expected = EXPECTED_MATRIX[(origin, level)]
    verdict = autonomy_may_start(origin, level)
    assert verdict.allowed == expected
    assert verdict.origin == origin
    assert verdict.level == level


# ---------------------------------------------------------------------------
# (b) the reasons, and the two unknown-input raises
# ---------------------------------------------------------------------------


def test_denied_reason_names_level_and_first_allowing_level():
    verdict = autonomy_may_start("order-file", "L3")
    assert verdict.allowed is False
    assert verdict.reason == (
        "Autonomy level L3 does not let Remedy start work that comes from an order file "
        "started without you; that needs level L4 or higher."
    )


def test_allowed_reason_is_the_allowed_sentence():
    verdict = autonomy_may_start("idea", "L5")
    assert verdict.allowed is True
    assert verdict.reason == "Autonomy level L5 lets Remedy start work that comes from an idea draft."


def test_unknown_origin_raises_value_error():
    with pytest.raises(ValueError):
        autonomy_may_start("not-an-origin", "L2")


def test_unknown_level_raises_value_error():
    with pytest.raises(ValueError):
        autonomy_may_start("manual", "L9")


# ---------------------------------------------------------------------------
# (c) no config file, and a project file at L2 with no record
# ---------------------------------------------------------------------------


def test_no_config_file_is_the_default_and_touches_nothing(tmp_path):
    cfg = _load(tmp_path)
    root = tmp_path / "data"
    policy = load_autonomy_policy(cfg, root=root)
    assert policy == AutonomyPolicy("L2", None, None, None, None)
    assert not (root / "autonomy").exists()


def test_project_file_at_l2_with_no_record_is_not_a_change(tmp_path):
    cfg = _load(tmp_path, project='[remedy]\nautonomy.level = "L2"\n')
    root = tmp_path / "data"
    policy = load_autonomy_policy(cfg, root=root)
    assert policy.level == "L2"
    assert policy.changed_from is None
    assert _change_lines(root) == []


# ---------------------------------------------------------------------------
# (d) L3 or higher without a gauntlet that proved it can be trusted
# ---------------------------------------------------------------------------


def test_l3_with_no_evidence_key_is_refused(tmp_path):
    cfg = _load(tmp_path, project='[remedy]\nautonomy.level = "L3"\n')
    project_path = str(tmp_path / "project.toml")
    with pytest.raises(AutonomyConfigError, match=re.escape(
        f"Autonomy level L3 in {project_path} lets Remedy start work on its own, so it needs "
        "the gauntlet that proved it can: set autonomy.gauntlet_evidence to the matrix.json of "
        "a gauntlet attempt that passed."
    )):
        load_autonomy_policy(cfg, root=tmp_path / "data")


def test_l3_with_missing_evidence_file_is_refused(tmp_path):
    evidence = tmp_path / "matrix.json"  # never written
    cfg = _load(tmp_path, project=(
        '[remedy]\nautonomy.level = "L3"\nautonomy.gauntlet_evidence = "matrix.json"\n'
    ))
    with pytest.raises(AutonomyConfigError, match=re.escape(
        f"The gauntlet evidence {evidence} does not exist."
    )):
        load_autonomy_policy(cfg, root=tmp_path / "data")


def test_l3_with_evidence_that_is_a_json_list_is_refused(tmp_path):
    evidence = tmp_path / "matrix.json"
    evidence.write_text("[]", encoding="utf-8")
    cfg = _load(tmp_path, project=(
        '[remedy]\nautonomy.level = "L3"\nautonomy.gauntlet_evidence = "matrix.json"\n'
    ))
    with pytest.raises(AutonomyConfigError, match=re.escape(
        f"The gauntlet evidence {evidence} is not a gauntlet matrix Remedy can read."
    )):
        load_autonomy_policy(cfg, root=tmp_path / "data")


def test_l3_with_evidence_that_is_not_json_is_refused(tmp_path):
    evidence = tmp_path / "matrix.json"
    evidence.write_text("not json at all", encoding="utf-8")
    cfg = _load(tmp_path, project=(
        '[remedy]\nautonomy.level = "L3"\nautonomy.gauntlet_evidence = "matrix.json"\n'
    ))
    with pytest.raises(AutonomyConfigError, match=re.escape(
        f"The gauntlet evidence {evidence} is not a gauntlet matrix Remedy can read."
    )):
        load_autonomy_policy(cfg, root=tmp_path / "data")


def test_l3_with_evidence_recording_a_failed_gauntlet_is_refused(tmp_path):
    evidence = tmp_path / "matrix.json"
    evidence.write_text(json.dumps({"passed": False}), encoding="utf-8")
    cfg = _load(tmp_path, project=(
        '[remedy]\nautonomy.level = "L3"\nautonomy.gauntlet_evidence = "matrix.json"\n'
    ))
    with pytest.raises(AutonomyConfigError, match=re.escape(
        f"The gauntlet evidence {evidence} records a gauntlet that did not pass."
    )):
        load_autonomy_policy(cfg, root=tmp_path / "data")


# ---------------------------------------------------------------------------
# (e) a passing gauntlet still needs its own decision record
# ---------------------------------------------------------------------------


def test_l3_with_passing_evidence_and_no_decision_record_is_refused(tmp_path):
    _write_passing_evidence(tmp_path)
    cfg = _load(tmp_path, project=(
        '[remedy]\nautonomy.level = "L3"\nautonomy.gauntlet_evidence = "matrix.json"\n'
    ))
    project_path = str(tmp_path / "project.toml")
    root = tmp_path / "data"
    with pytest.raises(AutonomyConfigError, match=re.escape(
        f"The autonomy level in {project_path} changed from L2 to L3, and every change needs "
        "its decision record: set autonomy.change_adr to the file that records why."
    )):
        load_autonomy_policy(cfg, root=root)
    assert _change_lines(root) == []


def test_l3_with_decision_record_that_does_not_exist_is_refused(tmp_path):
    _write_passing_evidence(tmp_path)
    adr = tmp_path / "adr.md"  # never written
    cfg = _load(tmp_path, project=(
        '[remedy]\nautonomy.level = "L3"\nautonomy.gauntlet_evidence = "matrix.json"\n'
        'autonomy.change_adr = "adr.md"\n'
    ))
    root = tmp_path / "data"
    with pytest.raises(AutonomyConfigError, match=re.escape(
        f"The decision record {adr} for the change from L2 to L3 does not exist."
    )):
        load_autonomy_policy(cfg, root=root)
    assert _change_lines(root) == []


def test_l3_accepted_with_evidence_and_decision_record_then_loaded_again(tmp_path):
    _write_passing_evidence(tmp_path)
    adr = tmp_path / "adr.md"
    adr.write_text("why", encoding="utf-8")
    cfg = _load(tmp_path, project=(
        '[remedy]\nautonomy.level = "L3"\nautonomy.gauntlet_evidence = "matrix.json"\n'
        'autonomy.change_adr = "adr.md"\n'
    ))
    root = tmp_path / "data"

    policy = load_autonomy_policy(cfg, root=root)
    assert policy.changed_from == "L2"
    assert policy.level == "L3"
    lines = _change_lines(root)
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert set(record) == {"at", "config_path", "from", "to", "change_adr", "source"}
    assert record["config_path"] == str(tmp_path / "project.toml")
    assert record["from"] == "L2"
    assert record["to"] == "L3"
    assert record["change_adr"] == str(adr)
    assert record["source"] == "project"

    policy_again = load_autonomy_policy(cfg, root=root)
    assert policy_again.changed_from is None
    assert _change_lines(root) == lines


# ---------------------------------------------------------------------------
# (f) a downgrade needs its own decision record too
# ---------------------------------------------------------------------------


def test_downgrade_to_l2_needs_its_own_decision_record(tmp_path):
    _write_passing_evidence(tmp_path)
    adr = tmp_path / "adr.md"
    adr.write_text("why", encoding="utf-8")
    root = tmp_path / "data"
    project_path = str(tmp_path / "project.toml")

    cfg_up = _load(tmp_path, project=(
        '[remedy]\nautonomy.level = "L3"\nautonomy.gauntlet_evidence = "matrix.json"\n'
        'autonomy.change_adr = "adr.md"\n'
    ))
    load_autonomy_policy(cfg_up, root=root)
    assert len(_change_lines(root)) == 1

    cfg_down_no_adr = _load(tmp_path, project='[remedy]\nautonomy.level = "L2"\n')
    with pytest.raises(AutonomyConfigError, match=re.escape(
        f"The autonomy level in {project_path} changed from L3 to L2, and every change needs "
        "its decision record: set autonomy.change_adr to the file that records why."
    )):
        load_autonomy_policy(cfg_down_no_adr, root=root)
    assert len(_change_lines(root)) == 1

    cfg_down = _load(tmp_path, project=(
        '[remedy]\nautonomy.level = "L2"\nautonomy.change_adr = "adr.md"\n'
    ))
    policy = load_autonomy_policy(cfg_down, root=root)
    assert policy.changed_from == "L3"
    lines = _change_lines(root)
    assert len(lines) == 2
    record = json.loads(lines[1])
    assert record["from"] == "L3"
    assert record["to"] == "L2"


# ---------------------------------------------------------------------------
# (g) none of the three keys may come from the environment
# ---------------------------------------------------------------------------


def test_level_from_environment_is_refused(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_AUTONOMY_LEVEL", "L3")
    cfg = _load(tmp_path)
    with pytest.raises(AutonomyConfigError, match=re.escape(
        "autonomy.level is set by the environment variable REMEDY_AUTONOMY_LEVEL, and the "
        "autonomy level is changed only by editing a config file. Unset REMEDY_AUTONOMY_LEVEL "
        "and set autonomy.level in remedy.toml."
    )):
        load_autonomy_policy(cfg, root=tmp_path / "data")


def test_change_adr_from_environment_is_refused(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_AUTONOMY_CHANGE_ADR", str(tmp_path / "adr.md"))
    cfg = _load(tmp_path, project='[remedy]\nautonomy.level = "L2"\n')
    with pytest.raises(AutonomyConfigError, match=re.escape(
        "autonomy.change_adr is set by the environment variable REMEDY_AUTONOMY_CHANGE_ADR, and "
        "the autonomy level is changed only by editing a config file. Unset "
        "REMEDY_AUTONOMY_CHANGE_ADR and set autonomy.change_adr in remedy.toml."
    )):
        load_autonomy_policy(cfg, root=tmp_path / "data")


# ---------------------------------------------------------------------------
# (h) a level outside L2 to L5, of either type
# ---------------------------------------------------------------------------


def test_level_l6_is_refused(tmp_path):
    cfg = _load(tmp_path, project='[remedy]\nautonomy.level = "L6"\n')
    project_path = str(tmp_path / "project.toml")
    with pytest.raises(AutonomyConfigError, match=re.escape(
        f"The autonomy level 'L6' in {project_path} is not one of L2, L3, L4 or L5."
    )):
        load_autonomy_policy(cfg, root=tmp_path / "data")


def test_level_integer_three_is_refused(tmp_path):
    cfg = _load(tmp_path, project="[remedy]\nautonomy.level = 3\n")
    project_path = str(tmp_path / "project.toml")
    with pytest.raises(AutonomyConfigError, match=re.escape(
        f"The autonomy level 3 in {project_path} is not one of L2, L3, L4 or L5."
    )):
        load_autonomy_policy(cfg, root=tmp_path / "data")


# ---------------------------------------------------------------------------
# (i) a user config's recorded change does not satisfy a project config's own
# ---------------------------------------------------------------------------


def test_user_config_change_record_does_not_count_for_project_config(tmp_path):
    root = tmp_path / "data"
    _write_passing_evidence(tmp_path)
    adr = tmp_path / "adr.md"
    adr.write_text("why", encoding="utf-8")

    # A USER config file is changed to L3 and its own record is accepted...
    user_cfg = _load(tmp_path, user=(
        '[remedy]\nautonomy.level = "L3"\nautonomy.gauntlet_evidence = "matrix.json"\n'
        'autonomy.change_adr = "adr.md"\n'
    ))
    policy_user = load_autonomy_policy(user_cfg, root=root)
    assert policy_user.changed_from == "L2"
    assert len(_change_lines(root)) == 1

    # ...which must not let a PROJECT config skip ITS OWN decision record merely because the
    # user file (cleared of its own keys here, so none of them can fall back into the project
    # lookup) already recorded a change to L3.
    project_cfg_no_adr = _load(
        tmp_path, project='[remedy]\nautonomy.level = "L3"\nautonomy.gauntlet_evidence = "matrix.json"\n',
        user="[remedy]\n",
    )
    with pytest.raises(AutonomyConfigError):
        load_autonomy_policy(project_cfg_no_adr, root=root)
    assert len(_change_lines(root)) == 1

    project_cfg = _load(
        tmp_path,
        project=(
            '[remedy]\nautonomy.level = "L3"\nautonomy.gauntlet_evidence = "matrix.json"\n'
            'autonomy.change_adr = "adr.md"\n'
        ),
        user="[remedy]\n",
    )
    policy_project = load_autonomy_policy(project_cfg, root=root)
    assert policy_project.changed_from == "L2"
    lines = _change_lines(root)
    assert len(lines) == 2
    records = [json.loads(line) for line in lines]
    config_paths = {record["config_path"] for record in records}
    assert config_paths == {str(tmp_path / "user.toml"), str(tmp_path / "project.toml")}


# ---------------------------------------------------------------------------
# (j) a relative evidence or decision-record path reads from the config file's
# own folder, never from the current working directory
# ---------------------------------------------------------------------------


def test_relative_paths_resolve_against_the_config_folder_not_cwd(tmp_path, monkeypatch):
    project_dir = tmp_path / "proj"
    project_dir.mkdir()
    evidence = project_dir / "matrix.json"
    evidence.write_text(json.dumps({"passed": True}), encoding="utf-8")
    adr = project_dir / "adr.md"
    adr.write_text("why", encoding="utf-8")
    project_path = project_dir / "remedy.toml"
    project_path.write_text(
        '[remedy]\nautonomy.level = "L3"\nautonomy.gauntlet_evidence = "matrix.json"\n'
        'autonomy.change_adr = "adr.md"\n',
        encoding="utf-8",
    )
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)

    cfg = load_config(project_path=project_path, user_path=tmp_path / "user.toml")
    policy = load_autonomy_policy(cfg, root=tmp_path / "data")
    assert policy.gauntlet_evidence == str(evidence)
    assert policy.change_adr == str(adr)
    assert policy.changed_from == "L2"


# ---------------------------------------------------------------------------
# (k) R-1321: the record is keyed by the RESOLVED config file, not the string
# load_config hands back unchanged from two different folders
# ---------------------------------------------------------------------------


def test_two_projects_at_the_relative_default_path_do_not_share_the_change_key(tmp_path, monkeypatch):
    """Before the fix, `load_config(project_path=Path("remedy.toml"), ...)` from two folders both
    wrote and read the key `"remedy.toml"`, so project B's L3 silently inherited project A's
    already-recorded change and skipped its own decision record."""
    root = tmp_path / "data"
    folder_a = tmp_path / "a"
    folder_b = tmp_path / "b"
    folder_a.mkdir()
    folder_b.mkdir()
    for folder in (folder_a, folder_b):
        (folder / "matrix.json").write_text(json.dumps({"passed": True}), encoding="utf-8")
    (folder_a / "adr.md").write_text("why", encoding="utf-8")
    (folder_a / "remedy.toml").write_text(
        '[remedy]\nautonomy.level = "L3"\nautonomy.gauntlet_evidence = "matrix.json"\n'
        'autonomy.change_adr = "adr.md"\n', encoding="utf-8",
    )
    (folder_b / "remedy.toml").write_text(
        '[remedy]\nautonomy.level = "L3"\nautonomy.gauntlet_evidence = "matrix.json"\n',
        encoding="utf-8",
    )

    monkeypatch.chdir(folder_a)
    cfg_a = load_config(project_path=Path("remedy.toml"), user_path=tmp_path / "user.toml")
    policy_a = load_autonomy_policy(cfg_a, root=root)
    assert policy_a.changed_from == "L2"
    assert len(_change_lines(root)) == 1

    # Project B, in its OWN folder, is also changing from L2 to L3 for the first time — and must
    # be refused for lacking its own decision record, not accepted because A already recorded L3.
    monkeypatch.chdir(folder_b)
    cfg_b_no_adr = load_config(project_path=Path("remedy.toml"), user_path=tmp_path / "user.toml")
    with pytest.raises(AutonomyConfigError, match=re.escape(
        "The autonomy level in remedy.toml changed from L2 to L3, and every change needs "
        "its decision record: set autonomy.change_adr to the file that records why."
    )):
        load_autonomy_policy(cfg_b_no_adr, root=root)
    assert len(_change_lines(root)) == 1

    (folder_b / "adr.md").write_text("why", encoding="utf-8")
    (folder_b / "remedy.toml").write_text(
        '[remedy]\nautonomy.level = "L3"\nautonomy.gauntlet_evidence = "matrix.json"\n'
        'autonomy.change_adr = "adr.md"\n', encoding="utf-8",
    )
    cfg_b = load_config(project_path=Path("remedy.toml"), user_path=tmp_path / "user.toml")
    policy_b = load_autonomy_policy(cfg_b, root=root)
    assert policy_b.changed_from == "L2"

    lines = _change_lines(root)
    assert len(lines) == 2
    config_paths = {json.loads(line)["config_path"] for line in lines}
    assert config_paths == {
        str((folder_a / "remedy.toml").resolve()),
        str((folder_b / "remedy.toml").resolve()),
    }


def test_l3_with_evidence_that_is_not_utf8_is_refused(tmp_path):
    """R-1321's second, smaller defect: unreadable bytes must not crash out of the loader."""
    evidence = tmp_path / "matrix.json"
    evidence.write_bytes(b"\xff\xfe\x00\x01")
    cfg = _load(tmp_path, project=(
        '[remedy]\nautonomy.level = "L3"\nautonomy.gauntlet_evidence = "matrix.json"\n'
    ))
    with pytest.raises(AutonomyConfigError, match=re.escape(
        f"The gauntlet evidence {evidence} is not a gauntlet matrix Remedy can read."
    )):
        load_autonomy_policy(cfg, root=tmp_path / "data")
