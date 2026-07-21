"""F017 E2E tests — real production entry points, not helpers.

Covers:
  - source_apply.apply_structured_patch: fence blocks write + Evidence artifact
  - patch_apply.apply_patch_intent: fence blocks apply
  - repo_applicator.apply_task_output_to_repo: fence raises FenceViolationError
  - resolve_fence_spec: shared resolver reads remedy.toml [remedy.scope]
  - enforce_change_set: shared adapter writes job-scoped Evidence
  - Artifact safety: abs path redaction, collision-safe naming, symlink safety
  - Dedup preserves roles: (path, op, role) triple key
  - Fail-closed builtins: RuntimeError on data-root resolution failure
  - Config enforcement: remedy.toml deny rules actually enforced
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job
from packages.orchestration.scope_fences import (
    BuiltinResolutionResult,
    ChangeSetFenceResult,
    EnforceResult,
    FenceConfigError,
    FenceSpec,
    FenceViolationError,
    TouchedPath,
    _redact_path,
    _resolve_effective_builtins_typed,
    check_change_set,
    enforce_change_set,
    resolve_effective_builtins,
    resolve_fence_spec,
    write_fence_violations_artifact,
)


# ═══════════════════════════════════════════════════════════════════════════
# resolve_fence_spec — shared effective-spec resolver
# ═══════════════════════════════════════════════════════════════════════════


class TestResolveFenceSpec:
    def test_default_no_config(self, tmp_path):
        spec = resolve_fence_spec(tmp_path)
        assert spec.allow_globs == ()
        assert spec.deny_globs == ()

    def test_reads_remedy_toml_scope(self, tmp_path):
        toml = tmp_path / "remedy.toml"
        toml.write_text(
            '[remedy.scope]\nallow = ["src/**"]\ndeny = ["vendor/**"]\n',
            encoding="utf-8",
        )
        spec = resolve_fence_spec(tmp_path)
        assert "src/**" in spec.allow_globs
        assert "vendor/**" in spec.deny_globs

    def test_job_fences_override_config(self, tmp_path):
        toml = tmp_path / "remedy.toml"
        toml.write_text(
            '[remedy.scope]\nallow = ["src/**"]\ndeny = ["vendor/**"]\n',
            encoding="utf-8",
        )
        spec = resolve_fence_spec(
            tmp_path, job_fences={"allow": ["docs/**"], "deny": []}
        )
        assert "docs/**" in spec.allow_globs
        assert "vendor/**" not in spec.deny_globs

    def test_nonexistent_toml_gives_defaults(self, tmp_path):
        spec = resolve_fence_spec(tmp_path)
        assert spec.allow_globs == ()
        assert spec.deny_globs == ()

    def test_malformed_toml_raises_fence_config_error(self, tmp_path):
        toml = tmp_path / "remedy.toml"
        toml.write_text("{{not valid toml}}", encoding="utf-8")
        with pytest.raises(FenceConfigError, match="malformed config"):
            resolve_fence_spec(tmp_path)


# ═══════════════════════════════════════════════════════════════════════════
# enforce_change_set — shared enforcement adapter
# ═══════════════════════════════════════════════════════════════════════════


class TestEnforceChangeSet:
    def test_allowed_returns_result(self, tmp_path):
        touched = [TouchedPath("src/main.py", "create")]
        result = enforce_change_set(
            tmp_path, touched,
            applicator="test", evidence_dir=tmp_path / "ev",
        )
        assert isinstance(result, EnforceResult)
        assert result.fence_result.allowed

    def test_violation_raises_with_evidence(self, tmp_path):
        touched = [TouchedPath(".git/config", "modify")]
        ev_dir = tmp_path / "evidence"
        with pytest.raises(FenceViolationError) as exc_info:
            enforce_change_set(
                tmp_path, touched,
                applicator="test_apply", job_id="j123",
                evidence_dir=ev_dir,
            )
        assert not exc_info.value.result.allowed
        job_ev = ev_dir / "jobs" / "j123"
        artifacts = list(job_ev.glob("fence_violations*.json"))
        assert len(artifacts) == 1
        data = json.loads(artifacts[0].read_text())
        assert data["schema"] == "fence_violations/v2"
        assert data["applicator"] == "test_apply"

    def test_job_scoped_evidence_dir(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        touched = [TouchedPath(".git/HEAD", "modify")]
        with pytest.raises(FenceViolationError):
            enforce_change_set(
                tmp_path, touched,
                applicator="source_apply", job_id="abc123def456",
            )
        job_dir = tmp_path / "data" / "jobs" / "abc123def456"
        assert job_dir.is_dir()
        artifacts = list(job_dir.glob("fence_violations*.json"))
        assert len(artifacts) == 1

    def test_config_deny_enforced(self, tmp_path):
        toml = tmp_path / "remedy.toml"
        toml.write_text(
            '[remedy.scope]\ndeny = ["secrets/**"]\n', encoding="utf-8",
        )
        touched = [TouchedPath("secrets/api_key.txt", "create")]
        with pytest.raises(FenceViolationError) as exc_info:
            enforce_change_set(
                tmp_path, touched,
                applicator="test", evidence_dir=tmp_path / "ev",
            )
        assert "deny_glob" in exc_info.value.result.violations[0].reason


# ═══════════════════════════════════════════════════════════════════════════
# Absolute path redaction
# ═══════════════════════════════════════════════════════════════════════════


class TestAbsPathRedaction:
    def test_relative_path_unchanged(self):
        assert _redact_path("src/main.py") == "src/main.py"

    def test_absolute_path_redacted(self):
        assert _redact_path("/home/user/project/file.py") == "<abs-redacted>"

    def test_empty_path_unchanged(self):
        assert _redact_path("") == ""

    def test_artifact_redacts_absolute_paths(self, tmp_path):
        touched = [TouchedPath("/etc/shadow", "modify")]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        path = write_fence_violations_artifact(
            result, tmp_path / "ev",
            applicator="test", job_id="j1",
        )
        data = json.loads(path.read_text())
        for v in data["violations"]:
            assert not v["path"].startswith("/")
            assert "/etc/" not in v["path"]


# ═══════════════════════════════════════════════════════════════════════════
# Collision-safe artifact naming
# ═══════════════════════════════════════════════════════════════════════════


class TestCollisionSafeNaming:
    def test_with_job_and_applicator(self, tmp_path):
        touched = [TouchedPath(".git/HEAD", "modify")]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        path = write_fence_violations_artifact(
            result, tmp_path, applicator="source_apply", job_id="abc123",
        )
        assert path.name.startswith("fence_violations_abc123_")
        assert path.name.endswith("_source_apply.json")
        assert path.exists()

    def test_without_job_id(self, tmp_path):
        touched = [TouchedPath(".git/HEAD", "modify")]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        path = write_fence_violations_artifact(
            result, tmp_path, applicator="test",
        )
        assert path.name.startswith("fence_violations_")
        assert path.name.endswith("_test.json")

    def test_without_any_context(self, tmp_path):
        touched = [TouchedPath(".git/HEAD", "modify")]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        path = write_fence_violations_artifact(result, tmp_path)
        assert path.name.startswith("fence_violations_")
        assert path.name.endswith(".json")
        assert path.exists()

    def test_event_id_in_payload(self, tmp_path):
        touched = [TouchedPath(".git/HEAD", "modify")]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        path = write_fence_violations_artifact(result, tmp_path, job_id="j1")
        import json
        data = json.loads(path.read_text())
        assert "event_id" in data
        assert len(data["event_id"]) == 8

    def test_two_writes_unique_event_ids(self, tmp_path):
        touched = [TouchedPath(".git/HEAD", "modify")]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        p1 = write_fence_violations_artifact(
            result, tmp_path, applicator="source_apply", job_id="j1",
        )
        p2 = write_fence_violations_artifact(
            result, tmp_path, applicator="patch_apply", job_id="j1",
        )
        assert p1.name != p2.name
        assert p1.exists() and p2.exists()


# ═══════════════════════════════════════════════════════════════════════════
# Dedup preserves roles
# ═══════════════════════════════════════════════════════════════════════════


class TestDedupPreservesRoles:
    def test_same_path_op_different_role_not_deduped(self, tmp_path):
        touched = [
            TouchedPath(".git/config", "modify", role="target"),
            TouchedPath(".git/config", "modify", role="source"),
        ]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        assert len(result.violations) == 2
        assert result.touched_count == 2
        roles = {v.role for v in result.violations}
        assert roles == {"target", "source"}

    def test_same_triple_deduped(self, tmp_path):
        touched = [
            TouchedPath(".git/config", "modify", role="target"),
            TouchedPath(".git/config", "modify", role="target"),
        ]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        assert len(result.violations) == 1
        assert result.touched_count == 1


# ═══════════════════════════════════════════════════════════════════════════
# Fail-closed builtins
# ═══════════════════════════════════════════════════════════════════════════


class TestFailClosedBuiltins:
    def test_data_root_failure_raises_runtime_error(self, tmp_path, monkeypatch):
        def bad_resolve():
            raise OSError("disk gone")

        monkeypatch.setattr(
            "packages.orchestration.data_paths.resolve_data_root", bad_resolve,
        )
        with pytest.raises(RuntimeError, match="data root resolution failed"):
            resolve_effective_builtins(tmp_path)

    def test_typed_result_on_success(self, tmp_path, monkeypatch):
        monkeypatch.delenv("REMEDY_DATA_DIR", raising=False)
        result = _resolve_effective_builtins_typed(tmp_path)
        assert isinstance(result, BuiltinResolutionResult)
        assert result.resolved is True

    def test_data_root_import_failure_raises(self, monkeypatch, tmp_path):
        def bad_resolve():
            raise ImportError("no data_paths")

        monkeypatch.setattr(
            "packages.orchestration.data_paths.resolve_data_root", bad_resolve,
        )
        with pytest.raises(RuntimeError, match="data root resolution failed"):
            resolve_effective_builtins(tmp_path)


# ═══════════════════════════════════════════════════════════════════════════
# Real production entry points — source_apply
# ═══════════════════════════════════════════════════════════════════════════


class TestSourceApplyFenceE2E:
    """Invoke real source_apply.apply_structured_patch with fence-violating paths."""

    def _make_job_with_intent(self, tmp_path, target_path=".git/config"):
        """Create a job with permission + approved intent targeting a path."""
        from packages.orchestration.approval_queue import (
            APPROVAL_APPROVED,
            make_intent_id,
            set_approval_state,
        )
        from packages.orchestration.permissions import Capability, set_permission

        job = Job(name="test-fence-e2e")
        set_permission(job, Capability.repo_generated_write, allow=True)
        job.metadata["target_repo"] = str(tmp_path)

        art_id = uuid4()
        from packages.core.models import Artifact
        artifact = Artifact(
            id=art_id, name="test-patch", content="",
            kind=ArtifactKind.BUILDER_PROPOSAL,
            metadata={
                "patch_intent_explanations": [{
                    "file": target_path,
                    "action": "create",
                    "risk": "low",
                    "reason": "test",
                    "summary": "test patch",
                }],
            },
        )
        job.artifacts.append(artifact)
        intent_id = make_intent_id(art_id, 0)
        set_approval_state(job, intent_id, APPROVAL_APPROVED, decided_by="test")
        return job, intent_id

    def test_fence_blocks_git_dir_write(self, tmp_path, monkeypatch):
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job, intent_id = self._make_job_with_intent(tmp_path, ".git/config")

        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path=".git/config", action="create", content="x"),),
        )
        with pytest.raises(FenceViolationError) as exc_info:
            apply_structured_patch(
                patch, tmp_path,
                data_dir=str(tmp_path / "data"),
                job_id=job.id, job=job, intent_id=intent_id,
            )
        assert not exc_info.value.result.allowed
        assert not (tmp_path / ".git" / "config").exists()

    def test_fence_blocks_config_deny(self, tmp_path, monkeypatch):
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        (tmp_path / "remedy.toml").write_text(
            '[remedy.scope]\ndeny = ["secrets/**"]\n', encoding="utf-8",
        )
        job, intent_id = self._make_job_with_intent(tmp_path, "secrets/key.txt")

        patch = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="secrets/key.txt", action="create", content="x"),),
        )
        with pytest.raises(FenceViolationError) as exc_info:
            apply_structured_patch(
                patch, tmp_path,
                data_dir=str(tmp_path / "data"),
                job_id=job.id, job=job, intent_id=intent_id,
            )
        assert "deny_glob" in exc_info.value.result.violations[0].reason


# ═══════════════════════════════════════════════════════════════════════════
# Real production entry points — repo_applicator
# ═══════════════════════════════════════════════════════════════════════════


class TestRepoApplicatorFenceE2E:
    """Invoke real repo_applicator.apply_task_output_to_repo with fenced paths."""

    def test_fence_blocks_if_route_hits_denied_path(self, tmp_path, monkeypatch):
        from packages.orchestration.repo_applicator import apply_task_output_to_repo

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))

        (tmp_path / "remedy.toml").write_text(
            '[remedy.scope]\ndeny = ["docs/**"]\n', encoding="utf-8",
        )

        artifact = Artifact(
            name="test-output",
            content="Proposed Changes:\n  - Added feature\n",
            metadata={"task_type": "documentation", "summary": "doc update"},
        )

        with pytest.raises(FenceViolationError):
            apply_task_output_to_repo(artifact, tmp_path)


# ═══════════════════════════════════════════════════════════════════════════
# Symlink safety in violation artifact
# ═══════════════════════════════════════════════════════════════════════════


class TestSymlinkSafety:
    def test_symlink_escape_detected(self, tmp_path):
        target = tmp_path / "outside"
        target.mkdir()
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "link").symlink_to(target)

        result = check_change_set(
            repo, FenceSpec(),
            [TouchedPath("link/evil.py", "create")],
        )
        assert not result.allowed
        assert "escapes_worktree" in result.violations[0].reason

    def test_symlink_within_worktree_allowed(self, tmp_path):
        (tmp_path / "real").mkdir()
        (tmp_path / "link").symlink_to(tmp_path / "real")

        result = check_change_set(
            tmp_path, FenceSpec(),
            [TouchedPath("link/file.py", "create")],
        )
        assert result.allowed


# ═══════════════════════════════════════════════════════════════════════════
# T003 — Job model fences field
# ═══════════════════════════════════════════════════════════════════════════


class TestJobFencesField:
    def test_default_none(self):
        job = Job(name="test")
        assert job.fences is None

    def test_backward_compatible_load(self):
        data = {"name": "old-job", "id": str(uuid4())}
        job = Job.model_validate(data)
        assert job.fences is None

    def test_set_fences(self):
        from packages.core.models import JobFences
        job = Job(name="test", fences=JobFences(allow=["src/**"], deny=["vendor/**"]))
        assert job.fences is not None
        assert job.fences.allow == ["src/**"]
        assert job.fences.deny == ["vendor/**"]

    def test_round_trip_json(self):
        from packages.core.models import JobFences
        job = Job(name="test", fences=JobFences(allow=["src/**"], deny=[]))
        data = job.model_dump()
        restored = Job.model_validate(data)
        assert restored.fences is not None
        assert restored.fences.allow == ["src/**"]

    def test_fences_none_round_trip(self):
        job = Job(name="test")
        data = job.model_dump()
        restored = Job.model_validate(data)
        assert restored.fences is None

    def test_closed_type_rejects_extra_fields(self):
        from packages.core.models import JobFences
        fences = JobFences(allow=["src/**"], deny=[])
        assert not hasattr(fences, "extra_field")

    def test_no_str_coercion(self):
        from packages.core.models import JobFences
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            JobFences(allow="not-a-list", deny=[])

    def test_malformed_fails_closed(self):
        from packages.core.models import JobFences
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            JobFences(allow=[123], deny=[])


# ═══════════════════════════════════════════════════════════════════════════
# T003 — Config key extension for list-of-strings
# ═══════════════════════════════════════════════════════════════════════════


class TestConfigScopeKeys:
    def test_scope_allow_key_registered(self):
        from packages.orchestration.config import get_key_spec
        spec = get_key_spec("scope.allow")
        assert spec is not None
        assert spec.value_type is list
        assert spec.env_var == "REMEDY_SCOPE_ALLOW"

    def test_scope_deny_key_registered(self):
        from packages.orchestration.config import get_key_spec
        spec = get_key_spec("scope.deny")
        assert spec is not None
        assert spec.value_type is list
        assert spec.env_var == "REMEDY_SCOPE_DENY"

    def test_env_var_comma_split(self, monkeypatch):
        from packages.orchestration.config import _coerce_value, get_key_spec
        spec = get_key_spec("scope.allow")
        result = _coerce_value("src/**,lib/**", spec)
        assert result == ["src/**", "lib/**"]

    def test_env_var_empty_string(self):
        from packages.orchestration.config import _coerce_value, get_key_spec
        spec = get_key_spec("scope.allow")
        result = _coerce_value("", spec)
        assert result == []

    def test_toml_list_passthrough(self, tmp_path):
        from packages.orchestration.config import load_config
        toml = tmp_path / "remedy.toml"
        toml.write_text(
            '[remedy.scope]\nallow = ["src/**", "lib/**"]\n',
            encoding="utf-8",
        )
        cfg = load_config(project_path=toml)
        val = cfg.get("scope.allow")
        assert val == ["src/**", "lib/**"]

    def test_scope_deny_from_env(self, monkeypatch):
        from packages.orchestration.config import load_config
        monkeypatch.setenv("REMEDY_SCOPE_DENY", "vendor/**,node_modules/**")
        cfg = load_config()
        val = cfg.get("scope.deny")
        assert val == ["vendor/**", "node_modules/**"]


# ═══════════════════════════════════════════════════════════════════════════
# T003 — CLI command catalog
# ═══════════════════════════════════════════════════════════════════════════


class TestJobFencesCLI:
    def test_command_registered(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("job.fences")
        assert cmd is not None
        assert cmd.group_id == "job"
        assert cmd.subcommand == "fences"
        assert cmd.action_class == "read_only"
        assert cmd.supports_json

    def test_handler_registered(self):
        from apps.cli.commands.job import COMMAND_HANDLERS
        assert "job.fences" in COMMAND_HANDLERS


# ═══════════════════════════════════════════════════════════════════════════
# Repair findings — centralized config (env var enforcement)
# ═══════════════════════════════════════════════════════════════════════════


class TestEnvVarEnforcement:
    """Finding #1: env vars REMEDY_SCOPE_DENY/ALLOW must be enforced."""

    def test_env_deny_enforced_via_resolve(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_SCOPE_DENY", "secrets/**")
        spec = resolve_fence_spec(tmp_path)
        assert "secrets/**" in spec.deny_globs

    def test_env_allow_enforced_via_resolve(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_SCOPE_ALLOW", "src/**")
        spec = resolve_fence_spec(tmp_path)
        assert "src/**" in spec.allow_globs

    def test_env_deny_blocks_path(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_SCOPE_DENY", "secrets/**")
        spec = resolve_fence_spec(tmp_path)
        from packages.orchestration.scope_fences import check_path
        result = check_path("secrets/key.pem", tmp_path, spec)
        assert not result.allowed

    def test_env_beats_project_toml(self, tmp_path, monkeypatch):
        (tmp_path / "remedy.toml").write_text(
            '[remedy.scope]\ndeny = ["vendor/**"]\n', encoding="utf-8",
        )
        monkeypatch.setenv("REMEDY_SCOPE_DENY", "secrets/**")
        spec = resolve_fence_spec(tmp_path)
        assert "secrets/**" in spec.deny_globs


# ═══════════════════════════════════════════════════════════════════════════
# Repair findings — FenceConfigError (fail-closed config)
# ═══════════════════════════════════════════════════════════════════════════


class TestFenceConfigErrorE2E:
    """Finding #2: malformed config must fail closed, not allow-all."""

    def test_malformed_toml_raises(self, tmp_path):
        (tmp_path / "remedy.toml").write_text("{{bad toml}}", encoding="utf-8")
        with pytest.raises(FenceConfigError, match="malformed config"):
            resolve_fence_spec(tmp_path)

    def test_non_string_glob_raises(self):
        from packages.orchestration.scope_fences import load_fence_spec
        with pytest.raises(FenceConfigError, match="must be a string"):
            load_fence_spec(job_fences={"allow": [123], "deny": []})

    def test_non_list_allow_raises(self):
        from packages.orchestration.scope_fences import load_fence_spec
        with pytest.raises(FenceConfigError, match="must be a list"):
            load_fence_spec(job_fences={"allow": "not-a-list", "deny": []})


# ═══════════════════════════════════════════════════════════════════════════
# Repair findings — closed JobFences (extra="forbid")
# ═══════════════════════════════════════════════════════════════════════════


class TestClosedJobFences:
    """Finding #3: JobFences must reject unknown fields."""

    def test_extra_field_rejected(self):
        from packages.core.models import JobFences
        from pydantic import ValidationError
        with pytest.raises(ValidationError, match="extra_forbidden"):
            JobFences(allow=["src/**"], deny=[], sneaky="hack")

    def test_valid_fields_accepted(self):
        from packages.core.models import JobFences
        fences = JobFences(allow=["src/**"], deny=["vendor/**"])
        assert fences.allow == ["src/**"]
        assert fences.deny == ["vendor/**"]


# ═══════════════════════════════════════════════════════════════════════════
# Repair findings — EffectiveFenceResult provenance
# ═══════════════════════════════════════════════════════════════════════════


class TestEffectiveFenceResult:
    """Provenance carrier for resolved fence spec."""

    def test_per_job_source(self, tmp_path):
        from packages.orchestration.scope_fences import resolve_fence_spec_effective
        result = resolve_fence_spec_effective(
            tmp_path, job_fences={"allow": ["src/**"], "deny": []},
        )
        assert result.source == "per-job"
        assert result.spec.allow_globs == ("src/**",)

    def test_central_config_source(self, tmp_path):
        from packages.orchestration.scope_fences import resolve_fence_spec_effective
        (tmp_path / "remedy.toml").write_text(
            '[remedy.scope]\ndeny = ["vendor/**"]\n', encoding="utf-8",
        )
        result = resolve_fence_spec_effective(tmp_path)
        assert result.source == "central-config"
        assert "vendor/**" in result.spec.deny_globs

    def test_defaults_source(self, tmp_path):
        from packages.orchestration.scope_fences import resolve_fence_spec_effective
        result = resolve_fence_spec_effective(tmp_path)
        assert result.source == "defaults"

    def test_env_var_source(self, tmp_path, monkeypatch):
        from packages.orchestration.scope_fences import resolve_fence_spec_effective
        monkeypatch.setenv("REMEDY_SCOPE_DENY", "secrets/**")
        result = resolve_fence_spec_effective(tmp_path)
        assert result.source == "central-config"
        assert "secrets/**" in result.spec.deny_globs


# ═══════════════════════════════════════════════════════════════════════════
# Repair findings — secure artifact writer
# ═══════════════════════════════════════════════════════════════════════════


class TestSecureArtifactWriter:
    """Finding #6: artifact writer must use atomic write with O_NOFOLLOW."""

    def test_artifact_is_regular_file(self, tmp_path):
        touched = [TouchedPath(".git/HEAD", "modify")]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        path = write_fence_violations_artifact(result, tmp_path, job_id="j1")
        assert path.is_file()
        assert not path.is_symlink()

    def test_artifact_valid_json(self, tmp_path):
        touched = [TouchedPath(".git/HEAD", "modify")]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        path = write_fence_violations_artifact(result, tmp_path, job_id="j1")
        data = json.loads(path.read_text())
        assert data["schema"] == "fence_violations/v2"
        assert "event_id" in data
        assert data["violation_count"] == 1

    def test_no_absolute_paths_in_exception(self, tmp_path):
        touched = [TouchedPath("/etc/passwd", "modify")]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        assert not result.allowed
        exc = FenceViolationError(result)
        assert "/etc/" not in str(exc)
        assert "<abs-redacted>" in str(exc)


# ═══════════════════════════════════════════════════════════════════════════
# Repair findings — ContinueStopReason.FENCE_VIOLATION
# ═══════════════════════════════════════════════════════════════════════════


class TestContinueStopReasonFenceViolation:
    """Finding #10: do_continue must use FENCE_VIOLATION, not APPLY_FAILED."""

    def test_fence_violation_stop_reason_exists(self):
        from packages.orchestration.do_continue import ContinueStopReason
        assert hasattr(ContinueStopReason, "FENCE_VIOLATION")
        assert ContinueStopReason.FENCE_VIOLATION == "fence_violation"

    def test_apply_failed_still_exists(self):
        from packages.orchestration.do_continue import ContinueStopReason
        assert hasattr(ContinueStopReason, "APPLY_FAILED")


# ═══════════════════════════════════════════════════════════════════════════
# Repair findings — repo_applicator propagates job_fences
# ═══════════════════════════════════════════════════════════════════════════


class TestRepoApplicatorJobFences:
    """Finding #8: repo_applicator must propagate job_fences."""

    def test_apply_with_job_fences_deny(self, tmp_path, monkeypatch):
        from packages.core.models import JobFences
        from packages.orchestration.repo_applicator import apply_task_output_to_repo

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))

        artifact = Artifact(
            name="test",
            content="Proposed Changes:\n  - test\n",
            metadata={"task_type": "documentation", "summary": "test"},
        )
        job_fences = {"allow": [], "deny": ["docs/**"]}
        with pytest.raises(FenceViolationError):
            apply_task_output_to_repo(artifact, tmp_path, job_fences=job_fences)

    def test_check_and_apply_propagates_fences(self, tmp_path, monkeypatch):
        from packages.core.models import JobFences
        from packages.orchestration.permissions import Capability, set_permission
        from packages.orchestration.repo_applicator import check_and_apply_to_repo

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))

        job = Job(
            name="test",
            fences=JobFences(allow=[], deny=["docs/**"]),
        )
        set_permission(job, Capability.repo_generated_write, allow=True)

        artifact = Artifact(
            name="test",
            content="Proposed Changes:\n  - test\n",
            metadata={"task_type": "documentation", "summary": "test"},
        )
        with pytest.raises(FenceViolationError):
            check_and_apply_to_repo(job, artifact, tmp_path)


# ═══════════════════════════════════════════════════════════════════════════
# Five-path production E2E — provenance + persistence + schema v2
# ═══════════════════════════════════════════════════════════════════════════


class TestProvenanceE2E:
    """enforce_change_set carries rule-level provenance through to artifact and exception."""

    def test_violation_error_carries_effective_result(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        (tmp_path / "remedy.toml").write_text(
            '[remedy.scope]\ndeny = ["vendor/**"]\n', encoding="utf-8",
        )
        touched = [TouchedPath("vendor/lib.so", "create")]
        with pytest.raises(FenceViolationError) as exc_info:
            enforce_change_set(tmp_path, touched, applicator="test", job_id="j1")
        err = exc_info.value
        assert err.effective_result is not None
        assert err.effective_result.source == "central-config"
        assert any(r.pattern == "vendor/**" for r in err.effective_result.deny_rules)

    def test_artifact_v2_has_per_violation_rule_info(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        (tmp_path / "remedy.toml").write_text(
            '[remedy.scope]\ndeny = ["secrets/**"]\n', encoding="utf-8",
        )
        touched = [TouchedPath("secrets/key.pem", "create")]
        with pytest.raises(FenceViolationError) as exc_info:
            enforce_change_set(tmp_path, touched, applicator="test", job_id="j2")
        err = exc_info.value
        assert err.artifact_path is not None
        data = json.loads(err.artifact_path.read_text())
        assert data["schema"] == "fence_violations/v2"
        assert data["schema_version"] == "2.0.0"
        v = data["violations"][0]
        assert v["matched_rule"] == "secrets/**"
        assert v["rule_kind"] == "deny"
        assert v["rule_source"] == "project"
        assert v["path_kind"] == "relative"
        assert v["reason_code"] in ("denied", "")

    def test_builtin_violation_rule_info(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        touched = [TouchedPath(".git/config", "modify")]
        with pytest.raises(FenceViolationError) as exc_info:
            enforce_change_set(tmp_path, touched, applicator="test", job_id="j3")
        err = exc_info.value
        assert err.artifact_path is not None
        data = json.loads(err.artifact_path.read_text())
        v = data["violations"][0]
        assert v["rule_kind"] == "builtin"
        assert v["rule_source"] == "builtin"
        assert v["matched_rule"] == ".git/"

    def test_per_job_fence_provenance(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        touched = [TouchedPath("lib/x.py", "create")]
        with pytest.raises(FenceViolationError) as exc_info:
            enforce_change_set(
                tmp_path, touched, applicator="test", job_id="j4",
                job_fences={"allow": ["src/**"], "deny": []},
            )
        err = exc_info.value
        assert err.effective_result.source == "per-job"
        assert any(r.source == "per_job" for r in err.effective_result.allow_rules)

    def test_env_var_provenance(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        monkeypatch.setenv("REMEDY_SCOPE_DENY", "vendor/**")
        touched = [TouchedPath("vendor/x.so", "create")]
        with pytest.raises(FenceViolationError) as exc_info:
            enforce_change_set(tmp_path, touched, applicator="test", job_id="j5")
        err = exc_info.value
        assert any(r.source == "environment" for r in err.effective_result.deny_rules)


class TestPersistenceFailureE2E:
    """Artifact write failure preserves primary FenceViolationError."""

    def test_persistence_failure_still_raises(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        data_dir = tmp_path / "data"
        data_dir.mkdir(parents=True)
        (data_dir / "jobs").write_text("blocker")

        touched = [TouchedPath(".git/config", "modify")]
        with pytest.raises(FenceViolationError) as exc_info:
            enforce_change_set(
                tmp_path, touched, applicator="test", job_id="j1",
                evidence_dir=data_dir,
            )
        err = exc_info.value
        assert err.persistence_status == "failed"
        assert err.artifact_path is None
        assert not err.result.allowed

    def test_successful_persistence_status(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        touched = [TouchedPath(".git/config", "modify")]
        with pytest.raises(FenceViolationError) as exc_info:
            enforce_change_set(
                tmp_path, touched, applicator="test", job_id="j1",
                evidence_dir=tmp_path / "data",
            )
        err = exc_info.value
        assert err.persistence_status == "persisted"
        assert err.artifact_path is not None
        assert err.artifact_path.exists()


class TestPatchApplyFenceE2E:
    """Real patch_apply.apply_patch_intent with fence-violating paths."""

    def _make_job_with_intent(self, tmp_path, target_path=".git/config"):
        from packages.orchestration.approval_queue import (
            APPROVAL_APPROVED,
            make_intent_id,
            set_approval_state,
        )
        from packages.orchestration.permissions import Capability, set_permission

        job = Job(name="test-patch-fence")
        set_permission(job, Capability.repo_generated_write, allow=True)
        job.metadata["target_repo"] = str(tmp_path)

        art_id = uuid4()
        artifact = Artifact(
            id=art_id, name="test-patch", content="# test",
            kind=ArtifactKind.BUILDER_PROPOSAL,
            metadata={
                "patch_intent_explanations": [{
                    "file": target_path,
                    "action": "create",
                    "risk": "low",
                    "reason": "test",
                    "summary": "test patch",
                }],
            },
        )
        job.artifacts.append(artifact)
        intent_id = make_intent_id(art_id, 0)
        set_approval_state(job, intent_id, APPROVAL_APPROVED, decided_by="test")
        return job, intent_id

    def test_fence_blocks_config_deny(self, tmp_path, monkeypatch):
        from packages.orchestration.patch_apply import apply_patch_intent

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        (tmp_path / "remedy.toml").write_text(
            '[remedy.scope]\ndeny = ["secrets/**"]\n', encoding="utf-8",
        )
        job, intent_id = self._make_job_with_intent(tmp_path, "secrets/key.md")

        result = apply_patch_intent(job, intent_id, data_dir=tmp_path / "data")
        assert result.state == "blocked"
        assert result.blocked_reason == "fence_violation"

    def test_fence_blocks_job_deny(self, tmp_path, monkeypatch):
        from packages.core.models import JobFences
        from packages.orchestration.patch_apply import apply_patch_intent

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job, intent_id = self._make_job_with_intent(tmp_path, "vendor/lib.md")
        job.fences = JobFences(allow=[], deny=["vendor/**"])

        result = apply_patch_intent(job, intent_id, data_dir=tmp_path / "data")
        assert result.state == "blocked"
        assert result.blocked_reason == "fence_violation"


class TestDeterministicOrderingE2E:
    """Violation ordering is deterministic including role."""

    def test_sort_by_path_op_role(self, tmp_path):
        touched = [
            TouchedPath(".git/config", "modify", role="target"),
            TouchedPath(".git/config", "modify", role="source"),
            TouchedPath(".git/HEAD", "modify", role="target"),
        ]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        paths = [(v.path, v.operation, v.role) for v in result.violations]
        assert paths == sorted(paths)

    def test_sort_stability(self, tmp_path):
        touched = [
            TouchedPath("remedy.toml", "modify", role="z"),
            TouchedPath(".git/x", "modify", role="a"),
            TouchedPath(".git/x", "modify", role="b"),
            TouchedPath("remedy.toml", "modify", role="a"),
        ]
        result = check_change_set(tmp_path, FenceSpec(), touched)
        paths = [(v.path, v.operation, v.role) for v in result.violations]
        assert paths == sorted(paths)


class TestStrictGlobContractsE2E:
    """Whitespace trimming and empty-glob rejection."""

    def test_whitespace_trimmed(self, tmp_path):
        from packages.orchestration.scope_fences import load_fence_spec
        spec = load_fence_spec(job_fences={"allow": ["  src/**  "], "deny": [" vendor/** "]})
        assert spec.allow_globs == ("src/**",)
        assert spec.deny_globs == ("vendor/**",)

    def test_empty_after_trim_rejected(self):
        from packages.orchestration.scope_fences import load_fence_spec
        with pytest.raises(FenceConfigError):
            load_fence_spec(job_fences={"allow": ["  "], "deny": []})

    def test_whitespace_only_rejected(self):
        from packages.orchestration.scope_fences import load_fence_spec
        with pytest.raises(FenceConfigError):
            load_fence_spec(job_fences={"allow": ["\t\n"], "deny": []})

    def test_empty_string_rejected(self):
        from packages.orchestration.scope_fences import load_fence_spec
        with pytest.raises(FenceConfigError):
            load_fence_spec(job_fences={"allow": [""], "deny": []})


# ═══════════════════════════════════════════════════════════════════════════
# Diagnostic sanitizer — _sanitize_diagnostic
# ═══════════════════════════════════════════════════════════════════════════


class TestSanitizeDiagnostic:
    """_sanitize_diagnostic redacts embedded private paths from persistence error messages."""

    def test_posix_path_at_start(self):
        from packages.orchestration.scope_fences import _sanitize_diagnostic
        assert "<path-redacted>" in _sanitize_diagnostic("/home/user/secret/file.py error")
        assert "/home/" not in _sanitize_diagnostic("/home/user/secret/file.py error")

    def test_posix_path_in_middle(self):
        from packages.orchestration.scope_fences import _sanitize_diagnostic
        msg = "failed to write /tmp/remedy/data/jobs/j1.json: disk full"
        result = _sanitize_diagnostic(msg)
        assert "/tmp/" not in result
        assert "<path-redacted>" in result
        assert "disk full" in result

    def test_posix_path_at_end(self):
        from packages.orchestration.scope_fences import _sanitize_diagnostic
        msg = "permission denied: /var/log/remedy.log"
        result = _sanitize_diagnostic(msg)
        assert "/var/" not in result
        assert "<path-redacted>" in result

    def test_windows_drive_path(self):
        from packages.orchestration.scope_fences import _sanitize_diagnostic
        msg = r"failed: C:\Users\admin\secret.txt"
        result = _sanitize_diagnostic(msg)
        assert "C:\\" not in result
        assert "<win-path-redacted>" in result

    def test_unc_path(self):
        from packages.orchestration.scope_fences import _sanitize_diagnostic
        msg = r"error at \\server\share\file.txt"
        result = _sanitize_diagnostic(msg)
        assert r"\\server" not in result
        assert "<unc-redacted>" in result

    def test_file_uri(self):
        from packages.orchestration.scope_fences import _sanitize_diagnostic
        msg = "see file:///home/user/docs/readme.md"
        result = _sanitize_diagnostic(msg)
        assert "file://" not in result
        assert "<file-uri-redacted>" in result

    def test_control_chars_stripped(self):
        from packages.orchestration.scope_fences import _sanitize_diagnostic
        msg = "error\x00with\x07control\x1fchars"
        result = _sanitize_diagnostic(msg)
        assert "\x00" not in result
        assert "\x07" not in result
        assert "\x1f" not in result

    def test_length_bounded(self):
        from packages.orchestration.scope_fences import _sanitize_diagnostic
        msg = "x" * 500
        result = _sanitize_diagnostic(msg)
        assert len(result) <= 200

    def test_empty_string(self):
        from packages.orchestration.scope_fences import _sanitize_diagnostic
        assert _sanitize_diagnostic("") == ""

    def test_newlines_replaced(self):
        from packages.orchestration.scope_fences import _sanitize_diagnostic
        msg = "line1\nline2\rline3"
        result = _sanitize_diagnostic(msg)
        assert "\n" not in result
        assert "\r" not in result

    def test_multiple_path_types(self):
        from packages.orchestration.scope_fences import _sanitize_diagnostic
        msg = r"err /home/x/a.py and C:\Users\b.txt and \\srv\c"
        result = _sanitize_diagnostic(msg)
        assert "/home/" not in result
        assert "C:\\" not in result
        assert r"\\srv" not in result

    def test_safe_message_unchanged(self):
        from packages.orchestration.scope_fences import _sanitize_diagnostic
        msg = "disk full: cannot create directory"
        assert _sanitize_diagnostic(msg) == msg


_GENERAL_POSIX_CASES = [
    # (input, leaked_substrings, expected_substrings, description)
    ("/workspace/company/repo/file.py", ["/workspace"], ["<path-redacted>"], "workspace root"),
    ("/data/customer/db.sqlite", ["/data/"], ["<path-redacted>"], "data root"),
    ("/srv/private/secret.txt", ["/srv/"], ["<path-redacted>"], "srv root"),
    ("/custom/path/here", ["/custom/"], ["<path-redacted>"], "custom root"),
    ("/run/user/1000/bus", ["/run/"], ["<path-redacted>"], "run root"),
    ("/nix/store/abc-123/bin/foo", ["/nix/"], ["<path-redacted>"], "nix store"),
    ("/unknown-root/deep/path.txt", ["/unknown-root/"], ["<path-redacted>"], "unknown root"),
    ("open failed at /workspace/a.py", ["/workspace"], ["open failed at", "<path-redacted>"], "path in middle"),
    ("err: /srv/x end", ["/srv/"], ["err:", "<path-redacted>", "end"], "preserves surrounding text"),
    ("/opt/local/bin/tool and /srv/db/x.db", ["/opt/", "/srv/"], ["<path-redacted>"], "multiple paths"),
    ("err /a/b/c.py and /x/y/z.py", ["/a/b/", "/x/y/"], ["<path-redacted>"], "two unknown-root paths"),
    ("errno 13: /custom/f.txt", ["/custom/"], ["errno 13:", "<path-redacted>"], "errno preserved"),
    ("[Errno 2] No such file: /deep/nested/path/f.py", ["/deep/"], ["[Errno 2] No such file:", "<path-redacted>"], "bracket errno preserved"),
    ("EACCES /private/secret", ["/private/"], ["EACCES", "<path-redacted>"], "posix error category preserved"),
    ("/a.py", ["/a.py"], ["<path-redacted>"], "short single-component path"),
    ("/dot.file/sub/path", ["/dot.file/"], ["<path-redacted>"], "dot in first segment"),
    ("/path-with-dashes/file_under.py", ["/path-with-dashes/"], ["<path-redacted>"], "dashes and underscores"),
    ("safe message no paths", [], ["safe message no paths"], "no paths unchanged"),
    ("", [], [""], "empty string"),
    ("x" * 300, [], [], "long string bounded to 200"),
    ("/mnt/vol/a.txt and /workspace/b.txt", ["/mnt/", "/workspace/"], ["<path-redacted>"], "mixed known+unknown roots"),
    ("Permission denied: '/workspace/file'", ["/workspace/"], ["Permission denied:", "<path-redacted>"], "path in quotes"),
    ("IOError at /custom/deep/path.json\n/data/other", ["/custom/", "/data/"], ["<path-redacted>"], "newline + multiple paths"),
    ("/secret.key", ["/secret.key"], ["<path-redacted>"], "root-level file"),
]


class TestGeneralPosixDiagnosticRedaction:
    """General POSIX path sanitization — any absolute path redacted."""

    @pytest.mark.parametrize(
        "raw, leaked, expected, desc",
        _GENERAL_POSIX_CASES,
        ids=[c[3] for c in _GENERAL_POSIX_CASES],
    )
    def test_general_posix_redaction(self, raw, leaked, expected, desc):
        from packages.orchestration.scope_fences import _sanitize_diagnostic
        result = _sanitize_diagnostic(raw)
        for sub in leaked:
            assert sub not in result, f"leaked {sub!r} in result: {result!r}"
        for sub in expected:
            if sub:
                assert sub in result, f"expected {sub!r} not in result: {result!r}"
        assert len(result) <= 200

    def test_deterministic_output(self):
        from packages.orchestration.scope_fences import _sanitize_diagnostic
        msg = "error at /workspace/company/secret.py: denied"
        r1 = _sanitize_diagnostic(msg)
        r2 = _sanitize_diagnostic(msg)
        assert r1 == r2

    def test_no_partial_path_prefix_leak(self):
        from packages.orchestration.scope_fences import _sanitize_diagnostic
        msg = "failed: /workspace/company/repo/file.py"
        result = _sanitize_diagnostic(msg)
        assert "/workspace" not in result
        assert "/company" not in result
        assert "/repo" not in result
        assert "file.py" not in result


# ═══════════════════════════════════════════════════════════════════════════
# Allow-list provenance — applicable_rules in violation artifact
# ═══════════════════════════════════════════════════════════════════════════


class TestAllowListProvenanceE2E:
    """not_in_allow_list violations carry rule_source and applicable_rules."""

    def test_allow_list_violation_has_source(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        touched = [TouchedPath("lib/x.py", "create")]
        with pytest.raises(FenceViolationError) as exc_info:
            enforce_change_set(
                tmp_path, touched, applicator="test", job_id="j1",
                job_fences={"allow": ["src/**"], "deny": []},
            )
        err = exc_info.value
        assert err.artifact_path is not None
        data = json.loads(err.artifact_path.read_text())
        v = data["violations"][0]
        assert v["rule_source"] != ""
        assert v["rule_kind"] == "allow"

    def test_allow_list_violation_has_applicable_rules(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        touched = [TouchedPath("vendor/x.py", "create")]
        with pytest.raises(FenceViolationError) as exc_info:
            enforce_change_set(
                tmp_path, touched, applicator="test", job_id="j2",
                job_fences={"allow": ["src/**", "docs/**"], "deny": []},
            )
        err = exc_info.value
        data = json.loads(err.artifact_path.read_text())
        v = data["violations"][0]
        assert "applicable_rules" in v
        assert len(v["applicable_rules"]) == 2
        patterns = [r["pattern"] for r in v["applicable_rules"]]
        assert "src/**" in patterns
        assert "docs/**" in patterns


# ═══════════════════════════════════════════════════════════════════════════
# JobFences strict model validation
# ═══════════════════════════════════════════════════════════════════════════


class TestJobFencesStrictValidation:
    """Pydantic model_validator rejects invalid glob entries at construction."""

    def test_trims_whitespace(self):
        from packages.core.models import JobFences
        f = JobFences(allow=["  src/**  "], deny=[" vendor/** "])
        assert f.allow == ["src/**"]
        assert f.deny == ["vendor/**"]

    def test_empty_after_trim_rejected(self):
        from packages.core.models import JobFences
        from pydantic import ValidationError
        with pytest.raises(ValidationError, match="empty"):
            JobFences(allow=["  "])

    def test_tab_only_rejected(self):
        from packages.core.models import JobFences
        from pydantic import ValidationError
        with pytest.raises(ValidationError, match="empty"):
            JobFences(deny=["\t"])

    def test_int_rejected(self):
        from packages.core.models import JobFences
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            JobFences(allow=[42])

    def test_bool_rejected(self):
        from packages.core.models import JobFences
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            JobFences(deny=[True])

    def test_nested_list_rejected(self):
        from packages.core.models import JobFences
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            JobFences(allow=[["nested"]])

    def test_dict_rejected(self):
        from packages.core.models import JobFences
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            JobFences(deny=[{"pattern": "x"}])

    def test_valid_globs_accepted(self):
        from packages.core.models import JobFences
        f = JobFences(allow=["src/**", "lib/*.py"], deny=["vendor/**"])
        assert f.allow == ["src/**", "lib/*.py"]
        assert f.deny == ["vendor/**"]

    def test_default_empty(self):
        from packages.core.models import JobFences
        f = JobFences()
        assert f.allow == []
        assert f.deny == []


# ═══════════════════════════════════════════════════════════════════════════
# repo_applicator job-scoped Evidence
# ═══════════════════════════════════════════════════════════════════════════


class TestRepoApplicatorJobScopedEvidence:
    """check_and_apply_to_repo passes job_id and evidence_dir through to enforce_change_set."""

    def test_job_scoped_artifact_via_check_and_apply(self, tmp_path, monkeypatch):
        from packages.core.models import JobFences
        from packages.orchestration.permissions import Capability, set_permission
        from packages.orchestration.repo_applicator import check_and_apply_to_repo

        data_dir = tmp_path / "data"
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))

        job = Job(
            name="test-job-scope",
            fences=JobFences(allow=[], deny=["docs/**"]),
        )
        set_permission(job, Capability.repo_generated_write, allow=True)

        artifact = Artifact(
            name="test",
            content="Proposed Changes:\n  - test\n",
            metadata={"task_type": "documentation", "summary": "test"},
        )
        with pytest.raises(FenceViolationError) as exc_info:
            check_and_apply_to_repo(job, artifact, tmp_path)

        err = exc_info.value
        assert err.artifact_path is not None
        job_dir = data_dir / "jobs" / str(job.id)
        assert job_dir.is_dir()
        artifacts = list(job_dir.glob("fence_violations*.json"))
        assert len(artifacts) == 1

    def test_persistence_failure_still_raises(self, tmp_path, monkeypatch):
        from packages.core.models import JobFences
        from packages.orchestration.permissions import Capability, set_permission
        from packages.orchestration.repo_applicator import check_and_apply_to_repo

        data_dir = tmp_path / "data"
        data_dir.mkdir(parents=True)
        (data_dir / "jobs").write_text("blocker")
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))

        job = Job(
            name="test-persist-fail",
            fences=JobFences(allow=[], deny=["docs/**"]),
        )
        set_permission(job, Capability.repo_generated_write, allow=True)

        artifact = Artifact(
            name="test",
            content="Proposed Changes:\n  - test\n",
            metadata={"task_type": "documentation", "summary": "test"},
        )
        with pytest.raises(FenceViolationError) as exc_info:
            check_and_apply_to_repo(job, artifact, tmp_path)

        err = exc_info.value
        assert err.persistence_status == "failed"
        assert err.artifact_path is None
