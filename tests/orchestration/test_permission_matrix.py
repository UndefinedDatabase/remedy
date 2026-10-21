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

from packages.orchestration.autonomy_gate import (
    AUTONOMY_DEFAULT_LEVEL,
    AUTONOMY_LEVELS,
    AutonomyConfigError,
    load_autonomy_policy,
)
from packages.orchestration.config import load_config
from packages.orchestration.data_paths import job_dir
from packages.orchestration.permission_matrix import (
    APPROVAL_KIND_DECISION,
    APPROVAL_KIND_FLAG,
    APPROVAL_KIND_PROMPT,
    JOB_LEVEL_FILENAME,
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
    permission_status_rows,
    pin_job_level,
    pinned_job_level,
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
    citation = _citation("read", "L2", PERMISSION_ALLOW)
    assert verdict.cells == (citation,)
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


def test_expensive_at_l2_with_prompt_approval_allows_and_names_the_command(tmp_path):
    """DECISION F141 D5 (1): the prompt kind approves one instance like a flag does, its ref
    the command's own name."""
    cfg = _load(tmp_path)
    root = tmp_path / "data"
    approval = InstanceApproval(kind=APPROVAL_KIND_PROMPT, ref="job.resume")
    verdict = require_permission(
        "expensive", PermissionRequest(level="L2", subject="probe", approval=approval),
        config=cfg, root=root,
    )
    assert verdict.outcome == PERMISSION_ALLOW
    assert verdict.reason.endswith(
        "and this instance was approved by your answer at the prompt of job.resume."
    )
    lines = _grant_lines(root)
    assert len(lines) == 1
    assert lines[0]["approval_kind"] == APPROVAL_KIND_PROMPT
    assert lines[0]["approval_ref"] == "job.resume"


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
    assert verdict.cells == (
        _citation("commit", "L4", PERMISSION_ASK),
        _citation("dependency_change", "L4", PERMISSION_ALLOW),
    )
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


def test_instance_approval_accepts_the_prompt_kind():
    approval = InstanceApproval(kind=APPROVAL_KIND_PROMPT, ref="job.resume")
    assert approval.kind == APPROVAL_KIND_PROMPT
    assert approval.ref == "job.resume"


def test_instance_approval_rejects_an_empty_ref():
    with pytest.raises(ValueError):
        InstanceApproval(kind=APPROVAL_KIND_FLAG, ref="")


# ---------------------------------------------------------------------------
# (j) the level a job keeps from its first context (DECISION F141 D2 (2))
# ---------------------------------------------------------------------------


def test_pinned_job_level_answers_the_default_for_no_id_or_no_file(tmp_path):
    root = tmp_path / "data"
    assert pinned_job_level("", root=root) == AUTONOMY_DEFAULT_LEVEL
    assert pinned_job_level(None, root=root) == AUTONOMY_DEFAULT_LEVEL
    assert pinned_job_level("job-1", root=root) == AUTONOMY_DEFAULT_LEVEL


def test_pinned_job_level_reads_a_pinned_l4(tmp_path):
    root = tmp_path / "data"
    folder = job_dir("job-1", root)
    folder.mkdir(parents=True)
    (folder / JOB_LEVEL_FILENAME).write_text(json.dumps({"level": "L4"}), encoding="utf-8")
    assert pinned_job_level("job-1", root=root) == "L4"


def test_pinned_job_level_refuses_an_unknown_level(tmp_path):
    root = tmp_path / "data"
    folder = job_dir("job-1", root)
    folder.mkdir(parents=True)
    path = folder / JOB_LEVEL_FILENAME
    path.write_text(json.dumps({"level": "L9"}), encoding="utf-8")
    with pytest.raises(AutonomyConfigError, match=re.escape(
        f"The level recorded for job job-1 in {path} is not one of L2, L3, L4 or L5."
    )):
        pinned_job_level("job-1", root=root)


def test_pinned_job_level_refuses_text_that_is_not_json(tmp_path):
    root = tmp_path / "data"
    folder = job_dir("job-1", root)
    folder.mkdir(parents=True)
    path = folder / JOB_LEVEL_FILENAME
    path.write_text("not json at all", encoding="utf-8")
    with pytest.raises(AutonomyConfigError, match=re.escape(
        f"The level recorded for job job-1 in {path} is not one of L2, L3, L4 or L5."
    )):
        pinned_job_level("job-1", root=root)


def test_pin_job_level_writes_l2_with_exactly_three_keys_under_a_default_config(tmp_path):
    cfg = _load(tmp_path)
    root = tmp_path / "data"
    folder = job_dir("job-1", root)
    folder.mkdir(parents=True)
    assert pin_job_level("job-1", config=cfg, root=root) == "L2"
    path = folder / JOB_LEVEL_FILENAME
    record = json.loads(path.read_text(encoding="utf-8"))
    assert set(record) == {"level", "pinned_at", "config_path"}
    assert record["level"] == "L2"
    assert pinned_job_level("job-1", root=root) == "L2"


def test_pin_job_level_writes_l3_and_outlives_a_later_move_back_to_l2(tmp_path):
    evidence = tmp_path / "matrix.json"
    evidence.write_text(json.dumps({"passed": True}), encoding="utf-8")
    adr = tmp_path / "adr.md"
    adr.write_text("why", encoding="utf-8")
    cfg_l3 = _load(tmp_path, project=(
        '[remedy]\nautonomy.level = "L3"\nautonomy.gauntlet_evidence = "matrix.json"\n'
        'autonomy.change_adr = "adr.md"\n'
    ))
    root = tmp_path / "data"
    folder = job_dir("job-1", root)
    folder.mkdir(parents=True)

    assert pin_job_level("job-1", config=cfg_l3, root=root) == "L3"
    path = folder / JOB_LEVEL_FILENAME
    before = path.read_bytes()

    cfg_l2 = _load(tmp_path, project='[remedy]\nautonomy.level = "L2"\nautonomy.change_adr = "adr.md"\n')
    policy = load_autonomy_policy(cfg_l2, root=root)
    assert policy.level == "L2"

    assert pin_job_level("job-1", config=cfg_l2, root=root) == "L3"
    assert path.read_bytes() == before


def test_pin_job_level_with_no_job_folder_answers_the_level_and_writes_nothing(tmp_path):
    cfg = _load(tmp_path)
    root = tmp_path / "data"
    assert pin_job_level("job-ghost", config=cfg, root=root) == "L2"
    assert not job_dir("job-ghost", root).exists()


def test_pin_job_level_with_an_empty_id_writes_nothing(tmp_path):
    root = tmp_path / "data"
    assert pin_job_level("", root=root) == AUTONOMY_DEFAULT_LEVEL
    assert not root.exists()


# ---------------------------------------------------------------------------
# (k) permission_status_rows, the status answer's `autonomy.permissions` (DECISION F141 D7 (1))
# ---------------------------------------------------------------------------


def test_permission_status_rows_answers_eight_rows_in_order_with_seven_keys():
    rows = permission_status_rows("L2", push_allowed=True)
    assert [row["action"] for row in rows] == list(PERMISSION_ACTIONS)
    for row in rows:
        assert set(row) == {"action", "words", "L2", "L3", "L4", "L5", "now"}


def test_permission_status_rows_write_worktree_now_differs_by_level():
    l3_row = next(row for row in permission_status_rows("L3", push_allowed=True)
                  if row["action"] == "write_worktree")
    assert l3_row["now"] == PERMISSION_ASK
    l4_row = next(row for row in permission_status_rows("L4", push_allowed=True)
                  if row["action"] == "write_worktree")
    assert l4_row["now"] == PERMISSION_ALLOW


def test_permission_status_rows_with_push_disallowed_denies_now_and_keeps_cells():
    push_row = next(row for row in permission_status_rows("L2", push_allowed=False)
                    if row["action"] == "push")
    assert push_row["now"] == PERMISSION_DENY
    assert (push_row["L2"], push_row["L3"], push_row["L4"], push_row["L5"]) == (
        PERMISSION_ASK, PERMISSION_ASK, PERMISSION_ASK, PERMISSION_ASK,
    )


def test_permission_status_rows_with_push_allowed_none_the_push_row_now_is_none():
    push_row = next(row for row in permission_status_rows("L2", push_allowed=None)
                    if row["action"] == "push")
    assert push_row["now"] is None


def test_permission_status_rows_with_level_none_every_now_is_none():
    rows = permission_status_rows(None, push_allowed=True)
    assert all(row["now"] is None for row in rows)
