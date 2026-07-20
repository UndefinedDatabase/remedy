"""Tests for F017 T002 — applicator enforcement, change-set preflight,
violation Evidence, and postmortem classification.

Covers:
  - .git component match (nested path, not just root prefix)
  - Dynamic data-dir builtin deny via extra_builtin_denies
  - resolve_effective_builtins with overridden REMEDY_DATA_DIR
  - TouchedPath / FenceViolation / ChangeSetFenceResult contracts
  - check_change_set: all violations collected, deterministic order, dedup
  - FenceViolationError carries stable result
  - check_change_set with mixed allowed/denied → blocked
  - Batch atomicity: one bad path blocks entire set
  - write_fence_violations_artifact schema and content
  - FENCE_VIOLATION in FailureClass enum
  - FenceViolationError classified as fence_violation by postmortem
  - fence_violation in TERMINAL_STATUS_CLASSES
  - load_fence_spec with worktree_root populates extra_builtin_denies
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from packages.orchestration.scope_fences import (
    BUILTIN_DENY,
    ChangeSetFenceResult,
    FenceSpec,
    FenceViolation,
    FenceViolationError,
    TouchedPath,
    check_change_set,
    check_path,
    load_fence_spec,
    resolve_effective_builtins,
    write_fence_violations_artifact,
)


# ═══════════════════════════════════════════════════════════════════════════
# Scope 1: T001 builtin-boundary repairs
# ═══════════════════════════════════════════════════════════════════════════


class TestGitComponentMatch:
    """`.git` denied as path component anywhere, not just root prefix."""

    def test_root_git_still_denied(self, tmp_path):
        result = check_path(".git/config", tmp_path, FenceSpec())
        assert not result.allowed
        assert "git directory" in result.reason

    def test_nested_git_denied(self, tmp_path):
        result = check_path("submodule/.git/config", tmp_path, FenceSpec())
        assert not result.allowed
        assert "builtin:git directory" in result.reason

    def test_deeply_nested_git_denied(self, tmp_path):
        result = check_path("vendor/sub/deep/.git/HEAD", tmp_path, FenceSpec())
        assert not result.allowed

    def test_dot_git_bare_component_denied(self, tmp_path):
        result = check_path("foo/.git/objects/pack/idx", tmp_path, FenceSpec())
        assert not result.allowed

    def test_git_in_name_not_denied(self, tmp_path):
        """A file named 'git' or '.gitignore' should NOT trigger component match."""
        r1 = check_path("src/.gitignore", tmp_path, FenceSpec())
        assert r1.allowed
        r2 = check_path("src/git/main.py", tmp_path, FenceSpec())
        assert r2.allowed

    def test_allow_glob_cannot_override_nested_git(self, tmp_path):
        spec = FenceSpec(allow_globs=("submodule/.git/*",))
        result = check_path("submodule/.git/config", tmp_path, spec)
        assert not result.allowed


class TestDynamicDataDir:
    """Effective Remedy data dir protected via extra_builtin_denies."""

    def test_extra_builtin_denies_field_default(self):
        spec = FenceSpec()
        assert spec.extra_builtin_denies == ()

    def test_extra_builtin_denies_blocks_path(self, tmp_path):
        spec = FenceSpec(
            extra_builtin_denies=(("custom_data/", "effective Remedy data directory"),),
        )
        result = check_path("custom_data/jobs/j1.json", tmp_path, spec)
        assert not result.allowed
        assert "builtin:" in result.reason

    def test_resolve_effective_builtins_default_data(self, tmp_path, monkeypatch):
        monkeypatch.delenv("REMEDY_DATA_DIR", raising=False)
        result = resolve_effective_builtins(tmp_path)
        assert isinstance(result, tuple)

    def test_resolve_effective_builtins_custom_inside_worktree(self, tmp_path, monkeypatch):
        custom = tmp_path / "my_data"
        custom.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(custom))
        result = resolve_effective_builtins(tmp_path)
        assert len(result) == 1
        assert result[0][0] == "my_data/"
        assert "effective Remedy data directory" in result[0][1]

    def test_resolve_effective_builtins_outside_worktree(self, tmp_path, monkeypatch):
        other = tmp_path / "other"
        other.mkdir()
        worktree = tmp_path / "repo"
        worktree.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(other))
        result = resolve_effective_builtins(worktree)
        assert result == ()

    def test_resolve_effective_builtins_is_default_dot_data(self, tmp_path, monkeypatch):
        data = tmp_path / ".data"
        data.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data))
        result = resolve_effective_builtins(tmp_path)
        assert result == ()

    def test_load_fence_spec_with_worktree_root(self, tmp_path, monkeypatch):
        custom = tmp_path / "my_data"
        custom.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(custom))
        spec = load_fence_spec(worktree_root=tmp_path)
        assert len(spec.extra_builtin_denies) == 1
        assert spec.extra_builtin_denies[0][0] == "my_data/"

    def test_custom_data_dir_path_denied(self, tmp_path, monkeypatch):
        custom = tmp_path / "remedy_store"
        custom.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(custom))
        spec = load_fence_spec(worktree_root=tmp_path)
        result = check_path("remedy_store/jobs/abc.json", tmp_path, spec)
        assert not result.allowed
        assert "builtin:" in result.reason


# ═══════════════════════════════════════════════════════════════════════════
# Scope 2: Change-set preflight API
# ═══════════════════════════════════════════════════════════════════════════


class TestTouchedPath:
    def test_frozen(self):
        tp = TouchedPath(path="src/main.py", operation="modify", role="target")
        with pytest.raises(AttributeError):
            tp.path = "other"  # type: ignore[misc]

    def test_defaults(self):
        tp = TouchedPath(path="x.py", operation="create")
        assert tp.role == "target"


class TestFenceViolation:
    def test_frozen(self):
        v = FenceViolation(
            path=".git/config", normalized=".git/config",
            operation="create", role="target", reason="denied:builtin:git directory",
        )
        with pytest.raises(AttributeError):
            v.path = "other"  # type: ignore[misc]


class TestChangeSetFenceResult:
    def test_allowed_empty_set(self, tmp_path):
        result = check_change_set(tmp_path, FenceSpec(), [])
        assert result.allowed
        assert result.violations == ()
        assert result.touched_count == 0

    def test_all_allowed(self, tmp_path):
        touched = [
            TouchedPath("src/a.py", "create"),
            TouchedPath("src/b.py", "modify"),
        ]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        assert result.allowed
        assert result.touched_count == 2

    def test_single_violation(self, tmp_path):
        touched = [TouchedPath(".git/config", "modify")]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        assert not result.allowed
        assert len(result.violations) == 1
        assert result.violations[0].path == ".git/config"
        assert "builtin" in result.violations[0].reason

    def test_mixed_allowed_and_denied(self, tmp_path):
        touched = [
            TouchedPath("src/ok.py", "create"),
            TouchedPath(".git/config", "modify"),
            TouchedPath("remedy.toml", "modify"),
        ]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        assert not result.allowed
        assert len(result.violations) == 2
        assert result.touched_count == 3

    def test_all_violations_collected_no_short_circuit(self, tmp_path):
        touched = [
            TouchedPath(".git/HEAD", "modify"),
            TouchedPath(".remedy/config", "modify"),
            TouchedPath("remedy.toml", "modify"),
        ]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        assert len(result.violations) == 3

    def test_deterministic_ordering(self, tmp_path):
        touched = [
            TouchedPath("remedy.toml", "modify"),
            TouchedPath(".git/HEAD", "modify"),
            TouchedPath(".remedy/x", "create"),
        ]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        paths = [v.path for v in result.violations]
        assert paths == sorted(paths)

    def test_dedup_same_path_same_operation(self, tmp_path):
        touched = [
            TouchedPath(".git/HEAD", "modify"),
            TouchedPath(".git/HEAD", "modify"),
        ]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        assert len(result.violations) == 1
        assert result.touched_count == 1

    def test_same_path_different_operation_not_deduped(self, tmp_path):
        touched = [
            TouchedPath("remedy.toml", "modify"),
            TouchedPath("remedy.toml", "delete"),
        ]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        assert len(result.violations) == 2

    def test_rename_roles(self, tmp_path):
        touched = [
            TouchedPath("src/old.py", "rename_src", role="rename_source"),
            TouchedPath(".git/new", "rename_dst", role="rename_dest"),
        ]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        assert not result.allowed
        assert len(result.violations) == 1
        assert result.violations[0].role == "rename_dest"

    def test_batch_atomicity_one_bad_blocks_all(self, tmp_path):
        touched = [
            TouchedPath("src/a.py", "create"),
            TouchedPath("src/b.py", "create"),
            TouchedPath(".git/objects/pack/idx", "create"),
            TouchedPath("src/c.py", "create"),
        ]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        assert not result.allowed
        assert result.touched_count == 4

    def test_deny_glob_in_change_set(self, tmp_path):
        spec = FenceSpec(deny_globs=("*.log",))
        touched = [
            TouchedPath("src/main.py", "modify"),
            TouchedPath("output/build.log", "create"),
        ]
        result = check_change_set(tmp_path, spec, touched)
        assert not result.allowed
        assert len(result.violations) == 1
        assert result.violations[0].path == "output/build.log"

    def test_violation_normalized_field(self, tmp_path):
        touched = [TouchedPath("./src/../.git/config", "modify")]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        assert not result.allowed


class TestFenceViolationError:
    def test_carries_result(self, tmp_path):
        touched = [TouchedPath(".git/HEAD", "modify")]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        err = FenceViolationError(result)
        assert err.result is result
        assert "fence violation" in str(err).lower()
        assert ".git/HEAD" in str(err)

    def test_is_exception(self):
        assert issubclass(FenceViolationError, Exception)

    def test_many_violations_truncated_message(self, tmp_path):
        touched = [
            TouchedPath(f".remedy/f{i}.json", "create")
            for i in range(10)
        ]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        err = FenceViolationError(result)
        assert "and 7 more" in str(err)


# ═══════════════════════════════════════════════════════════════════════════
# Scope 4: Violation Evidence + postmortem
# ═══════════════════════════════════════════════════════════════════════════


class TestFenceViolationsArtifact:
    def test_writes_json_on_violation(self, tmp_path):
        touched = [
            TouchedPath(".git/HEAD", "modify"),
            TouchedPath("remedy.toml", "modify"),
        ]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        evidence_dir = tmp_path / "evidence"
        path = write_fence_violations_artifact(
            result, evidence_dir,
            applicator="source_apply", job_id="j1", intent_id="i1",
        )
        assert path is not None
        assert path.name == "fence_violations_j1_source_apply.json"
        data = json.loads(path.read_text())
        assert data["schema"] == "fence_violations/v1"
        assert data["applicator"] == "source_apply"
        assert data["job_id"] == "j1"
        assert data["intent_id"] == "i1"
        assert data["touched_count"] == 2
        assert data["violation_count"] == 2
        assert len(data["violations"]) == 2
        for v in data["violations"]:
            assert "path" in v
            assert "normalized" in v
            assert "operation" in v
            assert "role" in v
            assert "reason" in v

    def test_returns_none_when_allowed(self, tmp_path):
        result = check_change_set(tmp_path, FenceSpec(), [])
        path = write_fence_violations_artifact(result, tmp_path / "ev")
        assert path is None

    def test_creates_evidence_dir(self, tmp_path):
        touched = [TouchedPath(".git/HEAD", "modify")]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        evidence_dir = tmp_path / "nested" / "deep" / "evidence"
        path = write_fence_violations_artifact(result, evidence_dir)
        assert path is not None
        assert evidence_dir.is_dir()

    def test_no_absolute_paths_in_artifact(self, tmp_path):
        touched = [TouchedPath(".git/HEAD", "modify")]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        path = write_fence_violations_artifact(
            result, tmp_path / "ev", applicator="test",
        )
        raw = path.read_text()
        assert str(tmp_path) not in raw


class TestPostmortemClassification:
    def test_fence_violation_in_failure_class(self):
        from packages.orchestration.failure_postmortem import FailureClass

        assert hasattr(FailureClass, "FENCE_VIOLATION")
        assert FailureClass.FENCE_VIOLATION.value == "fence_violation"

    def test_fence_violation_error_classified(self, tmp_path):
        from packages.orchestration.failure_postmortem import (
            FailureClass,
            FailureSignals,
            classify,
        )

        touched = [TouchedPath(".git/HEAD", "modify")]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        err = FenceViolationError(result)

        signals = FailureSignals(exception=err)
        classification = classify(signals)
        assert classification.failure_class == FailureClass.FENCE_VIOLATION
        assert classification.signal_source == "typed_exception"

    def test_fence_violation_terminal_status(self):
        from packages.orchestration.failure_postmortem import (
            FailureClass,
            FailureSignals,
            TERMINAL_STATUS_CLASSES,
            classify,
        )

        assert "fence_violation" in TERMINAL_STATUS_CLASSES
        assert TERMINAL_STATUS_CLASSES["fence_violation"] == FailureClass.FENCE_VIOLATION

        signals = FailureSignals(terminal_status="fence_violation")
        classification = classify(signals)
        assert classification.failure_class == FailureClass.FENCE_VIOLATION

    def test_fence_violation_error_wins_over_terminal_status(self, tmp_path):
        from packages.orchestration.failure_postmortem import (
            FailureClass,
            FailureSignals,
            classify,
        )

        touched = [TouchedPath(".git/HEAD", "modify")]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        err = FenceViolationError(result)

        signals = FailureSignals(
            exception=err,
            terminal_status="worktree_conflict",
        )
        classification = classify(signals)
        assert classification.failure_class == FailureClass.FENCE_VIOLATION


# ═══════════════════════════════════════════════════════════════════════════
# Integration: end-to-end fence enforcement scenarios
# ═══════════════════════════════════════════════════════════════════════════


class TestEndToEnd:
    def test_nested_git_in_change_set_blocks(self, tmp_path):
        touched = [
            TouchedPath("src/main.py", "create"),
            TouchedPath("vendor/dep/.git/HEAD", "modify"),
        ]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        assert not result.allowed
        assert result.violations[0].path == "vendor/dep/.git/HEAD"

    def test_custom_data_dir_in_change_set(self, tmp_path, monkeypatch):
        custom = tmp_path / "mydata"
        custom.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(custom))
        spec = load_fence_spec(worktree_root=tmp_path)
        touched = [
            TouchedPath("mydata/jobs/x.json", "create"),
            TouchedPath("src/ok.py", "create"),
        ]
        result = check_change_set(tmp_path, spec, touched)
        assert not result.allowed
        assert len(result.violations) == 1
        assert result.violations[0].path == "mydata/jobs/x.json"

    def test_full_flow_violation_to_evidence_to_classification(self, tmp_path):
        from packages.orchestration.failure_postmortem import (
            FailureClass,
            FailureSignals,
            classify,
        )

        touched = [
            TouchedPath("src/ok.py", "create"),
            TouchedPath(".git/objects/ab/cd", "create"),
            TouchedPath("remedy.toml", "modify"),
        ]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        assert not result.allowed
        assert len(result.violations) == 2

        ev_dir = tmp_path / "evidence"
        artifact = write_fence_violations_artifact(
            result, ev_dir, applicator="test", job_id="j42",
        )
        assert artifact is not None
        data = json.loads(artifact.read_text())
        assert data["violation_count"] == 2

        err = FenceViolationError(result)
        signals = FailureSignals(exception=err)
        c = classify(signals)
        assert c.failure_class == FailureClass.FENCE_VIOLATION
