"""A test per cell and per answer of the permission matrix (F141, DECISION F141 D1).

Every config is built with ``load_config(project_path=..., user_path=...)`` over files under
``tmp_path``, with ``root=tmp_path / "data"`` passed to the matrix's own functions, so nothing
this module runs ever touches the real data root.
"""
from __future__ import annotations

import itertools
import json
import re
from datetime import datetime, timezone

import pytest

from packages.orchestration.autonomy_gate import AUTONOMY_LEVELS, AutonomyConfigError
from packages.orchestration.config import load_config
from packages.orchestration.permission_matrix import (
    APPROVAL_KIND_DECISION,
    APPROVAL_KIND_FLAG,
    PERMISSION_ACTIONS,
    PERMISSION_ALLOW,
    PERMISSION_ASK,
    PERMISSION_CELLS,
    PERMISSION_DENY,
    PERMISSION_GRANTS_FILENAME,
    PERMISSION_MATRIX,
    InstanceApproval,
    PermissionRefusedError,
    PermissionRequest,
    push_allowed_by_config,
    require_permission,
    require_permissions,
)

# DECISION F141 D1 (2), independent of the module's own literal table, so the two can diverge and
# red this test rather than agreeing with itself.
EXPECTED_MATRIX: dict[tuple[str, str], str] = {
    ("read", "L2"): PERMISSION_ALLOW,
    ("read", "L3"): PERMISSION_ALLOW,
    ("read", "L4"): PERMISSION_ALLOW,
    ("read", "L5"): PERMISSION_ALLOW,
    ("write_worktree", "L2"): PERMISSION_ASK,
    ("write_worktree", "L3"): PERMISSION_ASK,
    ("write_worktree", "L4"): PERMISSION_ALLOW,
    ("write_worktree", "L5"): PERMISSION_ALLOW,
    ("commit", "L2"): PERMISSION_ASK,
    ("commit", "L3"): PERMISSION_ASK,
    ("commit", "L4"): PERMISSION_ASK,
    ("commit", "L5"): PERMISSION_ALLOW,
    ("push", "L2"): PERMISSION_ASK,
    ("push", "L3"): PERMISSION_ASK,
    ("push", "L4"): PERMISSION_ASK,
    ("push", "L5"): PERMISSION_ASK,
    ("dependency_change", "L2"): PERMISSION_ASK,
    ("dependency_change", "L3"): PERMISSION_ASK,
    ("dependency_change", "L4"): PERMISSION_ALLOW,
    ("dependency_change", "L5"): PERMISSION_ALLOW,
    ("destructive", "L2"): PERMISSION_ASK,
    ("destructive", "L3"): PERMISSION_ASK,
    ("destructive", "L4"): PERMISSION_ASK,
    ("destructive", "L5"): PERMISSION_ASK,
    ("expensive", "L2"): PERMISSION_ASK,
    ("expensive", "L3"): PERMISSION_ASK,
    ("expensive", "L4"): PERMISSION_ASK,
    ("expensive", "L5"): PERMISSION_ALLOW,
    ("external_call", "L2"): PERMISSION_ALLOW,
    ("external_call", "L3"): PERMISSION_ALLOW,
    ("external_call", "L4"): PERMISSION_ALLOW,
    ("external_call", "L5"): PERMISSION_ALLOW,
}

# The words each action's sentence names (DECISION F141 D1 (4)), copied here independent of the
# module's own private table, so an expected sentence is built without importing it.
WORDS: dict[str, str] = {
    "read": "read your project's files",
    "write_worktree": "write a job's result into your project's files",
    "commit": "commit in your project's repository",
    "push": "push to your project's remote",
    "dependency_change": "change your project's dependencies",
    "destructive": "delete files or run a migration in your project",
    "expensive": "start work estimated above your cost threshold",
    "external_call": "run a command that reaches the network",
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


def _grant_lines(root) -> list[dict]:
    path = root / "autonomy" / PERMISSION_GRANTS_FILENAME
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _citation(action: str, level: str, cell: str) -> str:
    return f"({action}, {level}) = {cell}"


# ---------------------------------------------------------------------------
# (a) every cell against the test's own literal table
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "action, level", list(EXPECTED_MATRIX), ids=[f"{a}-{lvl}" for a, lvl in EXPECTED_MATRIX],
)
def test_matrix_cell_matches_decision_f141_d1(action, level):
    assert PERMISSION_MATRIX[(action, level)] == EXPECTED_MATRIX[(action, level)]


def test_matrix_keys_are_exactly_the_product_of_actions_and_levels():
    assert set(PERMISSION_MATRIX) == set(itertools.product(PERMISSION_ACTIONS, AUTONOMY_LEVELS))


def test_every_matrix_value_is_a_known_cell():
    assert all(value in PERMISSION_CELLS for value in PERMISSION_MATRIX.values())


# ---------------------------------------------------------------------------
# (b) read at L2
# ---------------------------------------------------------------------------


def test_read_at_l2_allows_without_asking_and_writes_nothing(tmp_path):
    cfg = _load(tmp_path)
    root = tmp_path / "data"
    verdict = require_permission(
        "read", PermissionRequest(level="L2", subject="probe"), config=cfg, root=root,
    )
    assert verdict.outcome == PERMISSION_ALLOW
    assert verdict.actions == ("read",)
    assert verdict.cells == (PERMISSION_ALLOW,)
    citation = _citation("read", "L2", PERMISSION_ALLOW)
    assert verdict.reason == (
        f"Autonomy level L2 lets Remedy {WORDS['read']} without asking ({citation})."
    )
    assert not (root / "autonomy").exists()


# ---------------------------------------------------------------------------
# (c) ask without an approval
# ---------------------------------------------------------------------------


def test_dependency_change_at_l2_with_no_approval_asks_naming_l4(tmp_path):
    cfg = _load(tmp_path)
    root = tmp_path / "data"
    verdict = require_permission(
        "dependency_change", PermissionRequest(level="L2", subject="probe"), config=cfg, root=root,
    )
    assert verdict.outcome == PERMISSION_ASK
    citation = _citation("dependency_change", "L2", PERMISSION_ASK)
    assert verdict.reason == (
        f"Autonomy level L2 asks before Remedy may {WORDS['dependency_change']} ({citation}): "
        "approve this instance, or raise the level to L4 with its decision record."
    )
    assert not (root / "autonomy").exists()


def test_push_at_l5_with_no_approval_asks_with_no_level_sentence(tmp_path):
    cfg = _load(tmp_path)
    root = tmp_path / "data"
    verdict = require_permission(
        "push", PermissionRequest(level="L5", subject="probe"), config=cfg, root=root,
    )
    assert verdict.outcome == PERMISSION_ASK
    assert verdict.reason.endswith("no level lets Remedy do it without asking.")
    assert not (root / "autonomy").exists()


# ---------------------------------------------------------------------------
# (d) ask satisfied by an approval
# ---------------------------------------------------------------------------


def test_commit_at_l2_with_flag_approval_allows_and_audits_one_line(tmp_path):
    cfg = _load(tmp_path)
    root = tmp_path / "data"
    approval = InstanceApproval(kind=APPROVAL_KIND_FLAG, ref="--commit")
    when = datetime(2026, 10, 21, 12, 0, 0, tzinfo=timezone.utc)
    verdict = require_permission(
        "commit",
        PermissionRequest(level="L2", subject="probe", job_id="job1", approval=approval),
        config=cfg, root=root, now=when,
    )
    assert verdict.outcome == PERMISSION_ALLOW
    citation = _citation("commit", "L2", PERMISSION_ASK)
    assert verdict.reason == (
        f"Autonomy level L2 asks before Remedy may {WORDS['commit']} ({citation}), and this "
        "instance was approved by your flag --commit."
    )
    lines = _grant_lines(root)
    assert len(lines) == 1
    line = lines[0]
    assert set(line) == {
        "at", "action", "level", "cell", "approval_kind", "approval_ref", "job_id", "subject",
    }
    assert line["at"] == when.isoformat()
    assert line["action"] == "commit"
    assert line["level"] == "L2"
    assert line["cell"] == PERMISSION_ASK
    assert line["approval_kind"] == APPROVAL_KIND_FLAG
    assert line["approval_ref"] == "--commit"
    assert line["job_id"] == "job1"
    assert line["subject"] == "probe"


def test_commit_at_l2_with_decision_approval_allows_and_names_it(tmp_path):
    cfg = _load(tmp_path)
    root = tmp_path / "data"
    approval = InstanceApproval(kind=APPROVAL_KIND_DECISION, ref="D-42")
    verdict = require_permission(
        "commit", PermissionRequest(level="L2", subject="probe", approval=approval),
        config=cfg, root=root,
    )
    assert verdict.outcome == PERMISSION_ALLOW
    assert verdict.reason.endswith("and this instance was approved by your answer to decision D-42.")
    lines = _grant_lines(root)
    assert len(lines) == 1
    assert lines[0]["approval_kind"] == APPROVAL_KIND_DECISION
    assert lines[0]["approval_ref"] == "D-42"


# ---------------------------------------------------------------------------
# (e) the push switch
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("level", AUTONOMY_LEVELS)
def test_push_refused_at_every_level_when_switch_is_off(tmp_path, level):
    cfg = _load(tmp_path, project="[remedy]\nautonomy.allow_push = false\n")
    root = tmp_path / "data"
    approval = InstanceApproval(kind=APPROVAL_KIND_FLAG, ref="--push")
    with pytest.raises(PermissionRefusedError) as exc_info:
        require_permission(
            "push", PermissionRequest(level=level, subject="probe", approval=approval),
            config=cfg, root=root,
        )
    exc = exc_info.value
    assert exc.action == "push"
    assert exc.level == level
    assert exc.cell == PERMISSION_DENY
    citation = _citation("push", level, PERMISSION_DENY)
    assert exc.reason == (
        f"Remedy may not {WORDS['push']} ({citation}): autonomy.allow_push is false in your "
        "configuration, at every autonomy level."
    )
    assert not (root / "autonomy").exists()


def test_push_at_l2_asks_when_no_config_file_sets_the_switch(tmp_path):
    cfg = _load(tmp_path)
    root = tmp_path / "data"
    verdict = require_permission(
        "push", PermissionRequest(level="L2", subject="probe"), config=cfg, root=root,
    )
    assert verdict.outcome == PERMISSION_ASK


# ---------------------------------------------------------------------------
# (f) the switch read from the environment, and a non-boolean value
# ---------------------------------------------------------------------------


def test_push_allowed_by_config_env_sourced_value_is_refused(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_AUTONOMY_ALLOW_PUSH", "false")
    cfg = _load(tmp_path)
    with pytest.raises(AutonomyConfigError, match=re.escape(
        "autonomy.allow_push is set by the environment variable REMEDY_AUTONOMY_ALLOW_PUSH, and "
        "what Remedy may do is changed only by editing a config file. Unset "
        "REMEDY_AUTONOMY_ALLOW_PUSH and set autonomy.allow_push in remedy.toml."
    )):
        push_allowed_by_config(cfg)


def test_push_allowed_by_config_non_boolean_value_is_refused(tmp_path):
    """A project-sourced value is read RAW: ``_resolve_key`` in ``config.py`` never coerces a
    TOML-sourced value to its declared type, only an environment-sourced one (via
    ``_coerce_value``). So a quoted ``"yes"`` written in ``remedy.toml`` instead of a TOML boolean
    reaches this check unchanged and the loader lets it through, which is what this test proves.
    An environment-sourced non-boolean value can never reach this check: ``_coerce_value`` always
    turns a boolean-typed env var into ``True`` or ``False`` first, and even if it did not, the
    test above shows the ENV-source check raises before the bool-ness check ever runs.
    """
    cfg = _load(tmp_path, project='[remedy]\nautonomy.allow_push = "yes"\n')
    with pytest.raises(AutonomyConfigError, match=re.escape(
        "autonomy.allow_push must be true or false, not 'yes'."
    )):
        push_allowed_by_config(cfg)


# ---------------------------------------------------------------------------
# (g) the conjunction
# ---------------------------------------------------------------------------


def test_conjunction_at_l4_with_no_approval_asks_naming_only_commit(tmp_path):
    cfg = _load(tmp_path)
    root = tmp_path / "data"
    verdict = require_permissions(
        ("dependency_change", "commit"), PermissionRequest(level="L4", subject="probe"),
        config=cfg, root=root,
    )
    assert verdict.outcome == PERMISSION_ASK
    assert verdict.actions == ("commit", "dependency_change")
    assert WORDS["commit"] in verdict.reason
    assert WORDS["dependency_change"] not in verdict.reason
    assert not (root / "autonomy").exists()


def test_conjunction_at_l4_with_approval_allows_and_audits_commit_only(tmp_path):
    cfg = _load(tmp_path)
    root = tmp_path / "data"
    approval = InstanceApproval(kind=APPROVAL_KIND_FLAG, ref="--commit")
    verdict = require_permissions(
        ("dependency_change", "commit"),
        PermissionRequest(level="L4", subject="probe", approval=approval),
        config=cfg, root=root,
    )
    assert verdict.outcome == PERMISSION_ALLOW
    assert verdict.actions == ("commit", "dependency_change")
    lines = _grant_lines(root)
    assert len(lines) == 1
    assert lines[0]["action"] == "commit"


def test_conjunction_read_and_push_with_switch_off_is_refused_even_with_approval(tmp_path):
    cfg = _load(tmp_path, project="[remedy]\nautonomy.allow_push = false\n")
    root = tmp_path / "data"
    approval = InstanceApproval(kind=APPROVAL_KIND_FLAG, ref="--push")
    with pytest.raises(PermissionRefusedError) as exc_info:
        require_permissions(
            ("read", "push"), PermissionRequest(level="L2", subject="probe", approval=approval),
            config=cfg, root=root,
        )
    assert exc_info.value.action == "push"
    assert not (root / "autonomy").exists()


# ---------------------------------------------------------------------------
# (h) a deny cell always refuses, approval or not
# ---------------------------------------------------------------------------


def test_a_denied_cell_refuses_even_with_approval_and_writes_nothing(tmp_path, monkeypatch):
    monkeypatch.setitem(PERMISSION_MATRIX, ("read", "L2"), PERMISSION_DENY)
    cfg = _load(tmp_path)
    root = tmp_path / "data"
    approval = InstanceApproval(kind=APPROVAL_KIND_FLAG, ref="--approve")
    with pytest.raises(PermissionRefusedError) as exc_info:
        require_permission(
            "read", PermissionRequest(level="L2", subject="probe", approval=approval),
            config=cfg, root=root,
        )
    exc = exc_info.value
    citation = _citation("read", "L2", PERMISSION_DENY)
    assert exc.reason == f"Autonomy level L2 does not let Remedy {WORDS['read']} ({citation})."
    assert not (root / "autonomy").exists()


# ---------------------------------------------------------------------------
# (i) ValueError for malformed input
# ---------------------------------------------------------------------------


def test_require_permissions_rejects_no_actions():
    with pytest.raises(ValueError):
        require_permissions((), PermissionRequest(level="L2", subject="probe"))


def test_require_permissions_rejects_a_repeated_action():
    with pytest.raises(ValueError):
        require_permissions(("read", "read"), PermissionRequest(level="L2", subject="probe"))


def test_require_permissions_rejects_an_unknown_action():
    with pytest.raises(ValueError):
        require_permissions(("not-a-real-action",), PermissionRequest(level="L2", subject="probe"))


def test_require_permissions_rejects_an_unknown_level():
    with pytest.raises(ValueError):
        require_permissions(("read",), PermissionRequest(level="L9", subject="probe"))


def test_instance_approval_rejects_an_unknown_kind():
    with pytest.raises(ValueError):
        InstanceApproval(kind="not-a-kind", ref="x")


def test_instance_approval_rejects_an_empty_ref():
    with pytest.raises(ValueError):
        InstanceApproval(kind=APPROVAL_KIND_FLAG, ref="")
