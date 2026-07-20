"""Tests for scope_fences.py (F017 T001).

Covers: default allow, allow globs, deny globs, deny-over-allow,
builtin denies, empty allow list, absolute inputs, dot-dot escapes,
symlink escapes, normalization, rename source/destination checks,
1000-path performance, load precedence.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

import pytest

from packages.orchestration.scope_fences import (
    BUILTIN_DENY,
    FenceCheckResult,
    FenceSpec,
    check_path,
    load_fence_spec,
)


# ═══════════════════════════════════════════════════════════════════════════
# Default allow
# ═══════════════════════════════════════════════════════════════════════════


class TestDefaultAllow:
    """Default fence spec allows normal source paths."""

    def test_normal_source_file(self, tmp_path):
        result = check_path("src/main.py", tmp_path, FenceSpec())
        assert result.allowed
        assert result.reason == "allowed:default"

    def test_nested_path(self, tmp_path):
        result = check_path("packages/core/models.py", tmp_path, FenceSpec())
        assert result.allowed
        assert result.reason == "allowed:default"

    def test_top_level_file(self, tmp_path):
        result = check_path("README.md", tmp_path, FenceSpec())
        assert result.allowed

    def test_deeply_nested(self, tmp_path):
        result = check_path("a/b/c/d/e/f.txt", tmp_path, FenceSpec())
        assert result.allowed


# ═══════════════════════════════════════════════════════════════════════════
# Allow globs
# ═══════════════════════════════════════════════════════════════════════════


class TestAllowGlobs:
    """Allow globs restrict writes to matching paths only."""

    def test_matching_glob(self, tmp_path):
        spec = FenceSpec(allow_globs=("src/**",))
        result = check_path("src/main.py", tmp_path, spec)
        assert result.allowed
        assert result.reason == "allowed:allow_glob"

    def test_non_matching_denied(self, tmp_path):
        spec = FenceSpec(allow_globs=("src/**",))
        result = check_path("tests/test_main.py", tmp_path, spec)
        assert not result.allowed
        assert result.reason == "denied:not_in_allow_list"

    def test_multiple_allow_globs(self, tmp_path):
        spec = FenceSpec(allow_globs=("src/**", "tests/**"))
        assert check_path("src/main.py", tmp_path, spec).allowed
        assert check_path("tests/test_main.py", tmp_path, spec).allowed
        assert not check_path("docs/readme.md", tmp_path, spec).allowed

    def test_exact_file_allow(self, tmp_path):
        spec = FenceSpec(allow_globs=("Makefile",))
        assert check_path("Makefile", tmp_path, spec).allowed
        assert not check_path("README.md", tmp_path, spec).allowed

    def test_extension_allow(self, tmp_path):
        spec = FenceSpec(allow_globs=("*.py",))
        assert check_path("setup.py", tmp_path, spec).allowed
        assert not check_path("setup.cfg", tmp_path, spec).allowed


# ═══════════════════════════════════════════════════════════════════════════
# Deny globs
# ═══════════════════════════════════════════════════════════════════════════


class TestDenyGlobs:
    """Deny globs block matching paths."""

    def test_deny_blocks(self, tmp_path):
        spec = FenceSpec(deny_globs=("vendor/**",))
        result = check_path("vendor/lib.py", tmp_path, spec)
        assert not result.allowed
        assert "deny_glob" in result.reason
        assert "vendor/**" in result.reason

    def test_non_denied_passes(self, tmp_path):
        spec = FenceSpec(deny_globs=("vendor/**",))
        result = check_path("src/main.py", tmp_path, spec)
        assert result.allowed

    def test_multiple_deny_globs(self, tmp_path):
        spec = FenceSpec(deny_globs=("vendor/**", "dist/**"))
        assert not check_path("vendor/lib.py", tmp_path, spec).allowed
        assert not check_path("dist/bundle.js", tmp_path, spec).allowed
        assert check_path("src/main.py", tmp_path, spec).allowed


# ═══════════════════════════════════════════════════════════════════════════
# Deny over allow
# ═══════════════════════════════════════════════════════════════════════════


class TestDenyOverAllow:
    """Deny beats allow when both match."""

    def test_deny_wins(self, tmp_path):
        spec = FenceSpec(
            allow_globs=("src/**",),
            deny_globs=("src/generated/**",),
        )
        result = check_path("src/generated/output.py", tmp_path, spec)
        assert not result.allowed
        assert "deny_glob" in result.reason

    def test_allow_works_for_non_denied(self, tmp_path):
        spec = FenceSpec(
            allow_globs=("src/**",),
            deny_globs=("src/generated/**",),
        )
        result = check_path("src/main.py", tmp_path, spec)
        assert result.allowed

    def test_deny_checked_before_allow(self, tmp_path):
        spec = FenceSpec(
            allow_globs=("*",),
            deny_globs=("secret.key",),
        )
        assert not check_path("secret.key", tmp_path, spec).allowed
        assert check_path("public.txt", tmp_path, spec).allowed


# ═══════════════════════════════════════════════════════════════════════════
# Builtin deny
# ═══════════════════════════════════════════════════════════════════════════


class TestBuiltinDeny:
    """Builtin denies cannot be overridden."""

    def test_git_directory_file(self, tmp_path):
        result = check_path(".git/config", tmp_path, FenceSpec())
        assert not result.allowed
        assert "builtin" in result.reason
        assert "git directory" in result.reason

    def test_git_subdirectory(self, tmp_path):
        result = check_path(".git/refs/heads/main", tmp_path, FenceSpec())
        assert not result.allowed
        assert "builtin" in result.reason

    def test_git_dir_itself(self, tmp_path):
        result = check_path(".git", tmp_path, FenceSpec())
        assert not result.allowed
        assert "builtin" in result.reason

    def test_remedy_toml(self, tmp_path):
        result = check_path("remedy.toml", tmp_path, FenceSpec())
        assert not result.allowed
        assert "project config" in result.reason

    def test_remedy_config_dir(self, tmp_path):
        result = check_path(".remedy/config.toml", tmp_path, FenceSpec())
        assert not result.allowed
        assert "builtin" in result.reason

    def test_remedy_config_dir_itself(self, tmp_path):
        result = check_path(".remedy", tmp_path, FenceSpec())
        assert not result.allowed

    def test_data_dir_file(self, tmp_path):
        result = check_path(".data/jobs/abc.json", tmp_path, FenceSpec())
        assert not result.allowed
        assert "builtin" in result.reason

    def test_data_dir_itself(self, tmp_path):
        result = check_path(".data", tmp_path, FenceSpec())
        assert not result.allowed

    def test_status_file(self, tmp_path):
        result = check_path("docs/roadmap/STATUS.md", tmp_path, FenceSpec())
        assert not result.allowed
        assert "execution ledger" in result.reason

    def test_builtin_not_overridden_by_allow(self, tmp_path):
        spec = FenceSpec(allow_globs=(".git/**", "remedy.toml", ".data/**"))
        result = check_path(".git/config", tmp_path, spec)
        assert not result.allowed
        assert "builtin" in result.reason

    def test_builtin_not_overridden_by_empty_deny(self, tmp_path):
        spec = FenceSpec(deny_globs=())
        result = check_path(".git/HEAD", tmp_path, spec)
        assert not result.allowed

    def test_non_root_git_dir_denied(self, tmp_path):
        """.git as path component anywhere is denied (T002 component match)."""
        result = check_path("submodule/.git/config", tmp_path, FenceSpec())
        assert not result.allowed
        assert "builtin:git directory" in result.reason

    def test_builtin_constant_is_reviewable(self):
        assert isinstance(BUILTIN_DENY, tuple)
        assert len(BUILTIN_DENY) >= 5
        patterns = [p for p, _ in BUILTIN_DENY]
        assert ".git/" in patterns
        assert "remedy.toml" in patterns
        assert "docs/roadmap/STATUS.md" in patterns
        assert ".remedy/" in patterns
        assert ".data/" in patterns


# ═══════════════════════════════════════════════════════════════════════════
# Builtin deny immunity
# ═══════════════════════════════════════════════════════════════════════════


class TestBuiltinDenyImmunity:
    """Builtin denies override any configured allow or deny combination."""

    def test_explicit_allow_glob_for_git(self, tmp_path):
        spec = FenceSpec(allow_globs=(".git/*",))
        assert not check_path(".git/config", tmp_path, spec).allowed

    def test_explicit_allow_glob_for_status(self, tmp_path):
        spec = FenceSpec(allow_globs=("docs/**",))
        assert not check_path("docs/roadmap/STATUS.md", tmp_path, spec).allowed

    def test_explicit_allow_for_remedy_toml(self, tmp_path):
        spec = FenceSpec(allow_globs=("*.toml",))
        assert not check_path("remedy.toml", tmp_path, spec).allowed

    def test_similar_names_not_blocked(self, tmp_path):
        """remedy.toml.bak, .git-info, etc. are NOT builtin-denied."""
        assert check_path("remedy.toml.bak", tmp_path, FenceSpec()).allowed
        assert check_path(".git-info", tmp_path, FenceSpec()).allowed
        assert check_path("docs/roadmap/STATUS.md.bak", tmp_path, FenceSpec()).allowed


# ═══════════════════════════════════════════════════════════════════════════
# Empty allow list
# ═══════════════════════════════════════════════════════════════════════════


class TestEmptyAllowList:
    """Empty allow list = allow-all with logged warning."""

    def test_empty_allow_is_allow_all(self, tmp_path):
        spec = FenceSpec(allow_globs=())
        result = check_path("any/path.py", tmp_path, spec)
        assert result.allowed
        assert result.reason == "allowed:default"

    def test_empty_allow_with_deny(self, tmp_path):
        spec = FenceSpec(allow_globs=(), deny_globs=("vendor/**",))
        assert check_path("src/main.py", tmp_path, spec).allowed
        assert not check_path("vendor/lib.py", tmp_path, spec).allowed

    def test_warning_logged_on_load(self, caplog):
        with caplog.at_level(logging.WARNING, logger="packages.orchestration.scope_fences"):
            load_fence_spec(job_fences={"allow": [], "deny": ["vendor/**"]})
        assert "empty allow list" in caplog.text


# ═══════════════════════════════════════════════════════════════════════════
# Absolute path input
# ═══════════════════════════════════════════════════════════════════════════


class TestAbsolutePathInput:
    """Absolute paths always escape the worktree."""

    def test_absolute_unix(self, tmp_path):
        result = check_path("/etc/passwd", tmp_path, FenceSpec())
        assert not result.allowed
        assert result.reason == "escapes_worktree:absolute_path"

    def test_absolute_root(self, tmp_path):
        result = check_path("/", tmp_path, FenceSpec())
        assert not result.allowed
        assert "absolute_path" in result.reason

    def test_absolute_ignores_allow(self, tmp_path):
        spec = FenceSpec(allow_globs=("/**",))
        result = check_path("/etc/passwd", tmp_path, spec)
        assert not result.allowed
        assert "absolute_path" in result.reason


# ═══════════════════════════════════════════════════════════════════════════
# Dot-dot escape
# ═══════════════════════════════════════════════════════════════════════════


class TestDotDotEscape:
    """.. traversal is always denied."""

    def test_simple_dotdot(self, tmp_path):
        result = check_path("../outside.py", tmp_path, FenceSpec())
        assert not result.allowed
        assert result.reason == "escapes_worktree:dot_dot_traversal"

    def test_nested_dotdot(self, tmp_path):
        result = check_path("src/../../outside.py", tmp_path, FenceSpec())
        assert not result.allowed
        assert "dot_dot_traversal" in result.reason

    def test_deeply_nested_dotdot(self, tmp_path):
        result = check_path("a/b/../../../escape.py", tmp_path, FenceSpec())
        assert not result.allowed

    def test_non_escaping_dotdot_still_denied(self, tmp_path):
        """Even a/b/../c (which stays inside) is denied — structural rule."""
        result = check_path("a/b/../c.py", tmp_path, FenceSpec())
        assert not result.allowed
        assert "dot_dot_traversal" in result.reason

    def test_dotdot_as_substring_ok(self, tmp_path):
        """'...' or 'a..b' are valid names, not traversal."""
        assert check_path("a..b/file.py", tmp_path, FenceSpec()).allowed
        assert check_path(".../file.py", tmp_path, FenceSpec()).allowed


# ═══════════════════════════════════════════════════════════════════════════
# Symlink escape
# ═══════════════════════════════════════════════════════════════════════════


class TestSymlinkEscape:
    """Symlinks resolving outside worktree are denied."""

    def test_symlink_to_outside(self, tmp_path):
        outside = tmp_path / "outside"
        outside.mkdir()
        worktree = tmp_path / "repo"
        worktree.mkdir()
        link = worktree / "escape_link"
        link.symlink_to(outside)

        result = check_path("escape_link", worktree, FenceSpec())
        assert not result.allowed
        assert result.reason == "escapes_worktree:symlink_escape"

    def test_symlink_inside_worktree(self, tmp_path):
        worktree = tmp_path / "repo"
        worktree.mkdir()
        real = worktree / "real_dir"
        real.mkdir()
        link = worktree / "linked"
        link.symlink_to(real)

        result = check_path("linked", worktree, FenceSpec())
        assert result.allowed

    def test_chained_symlink_escape(self, tmp_path):
        outside = tmp_path / "outside"
        outside.mkdir()
        worktree = tmp_path / "repo"
        worktree.mkdir()
        mid = worktree / "mid"
        mid.symlink_to(outside)

        result = check_path("mid/file.txt", worktree, FenceSpec())
        assert not result.allowed
        assert "symlink_escape" in result.reason

    def test_nonexistent_path_allowed(self, tmp_path):
        """Non-existent path resolves within worktree — allowed."""
        result = check_path("nonexistent/deeply/nested.py", tmp_path, FenceSpec())
        assert result.allowed

    def test_symlink_to_file_outside(self, tmp_path):
        worktree = tmp_path / "repo"
        worktree.mkdir()
        outside_file = tmp_path / "secret.txt"
        outside_file.write_text("secret")
        link = worktree / "sneaky.txt"
        link.symlink_to(outside_file)

        result = check_path("sneaky.txt", worktree, FenceSpec())
        assert not result.allowed
        assert "symlink_escape" in result.reason


# ═══════════════════════════════════════════════════════════════════════════
# Path normalization
# ═══════════════════════════════════════════════════════════════════════════


class TestNormalization:
    """Paths are normalized before matching."""

    def test_redundant_separators(self, tmp_path):
        spec = FenceSpec(deny_globs=("vendor/**",))
        result = check_path("vendor//lib.py", tmp_path, spec)
        assert not result.allowed

    def test_current_dir_dot(self, tmp_path):
        spec = FenceSpec(deny_globs=("vendor/**",))
        result = check_path("./vendor/lib.py", tmp_path, spec)
        assert not result.allowed

    def test_builtin_with_dot_prefix(self, tmp_path):
        result = check_path("./.git/config", tmp_path, FenceSpec())
        assert not result.allowed
        assert "builtin" in result.reason

    def test_double_slash_in_allow(self, tmp_path):
        spec = FenceSpec(allow_globs=("src/**",))
        result = check_path("src//main.py", tmp_path, spec)
        assert result.allowed

    def test_trailing_slash_stripped(self, tmp_path):
        spec = FenceSpec(deny_globs=("vendor/**",))
        result = check_path("vendor/lib.py/", tmp_path, spec)
        assert not result.allowed

    def test_empty_path(self, tmp_path):
        result = check_path("", tmp_path, FenceSpec())
        assert not result.allowed
        assert "empty_path" in result.reason

    def test_dot_only(self, tmp_path):
        result = check_path(".", tmp_path, FenceSpec())
        assert not result.allowed
        assert "empty_path" in result.reason

    def test_dot_slash_only(self, tmp_path):
        result = check_path("./", tmp_path, FenceSpec())
        assert not result.allowed
        assert "empty_path" in result.reason


# ═══════════════════════════════════════════════════════════════════════════
# Rename source and destination
# ═══════════════════════════════════════════════════════════════════════════


class TestRenameSourceAndDestination:
    """For renames, both source and destination must be checked."""

    def test_source_allowed_dest_denied(self, tmp_path):
        spec = FenceSpec(deny_globs=("secret/**",))
        src = check_path("public/file.py", tmp_path, spec)
        dst = check_path("secret/file.py", tmp_path, spec)
        assert src.allowed
        assert not dst.allowed

    def test_both_denied(self, tmp_path):
        spec = FenceSpec(deny_globs=("private/**", "secret/**"))
        src = check_path("private/a.py", tmp_path, spec)
        dst = check_path("secret/a.py", tmp_path, spec)
        assert not src.allowed
        assert not dst.allowed

    def test_both_allowed(self, tmp_path):
        spec = FenceSpec(allow_globs=("src/**",))
        src = check_path("src/old.py", tmp_path, spec)
        dst = check_path("src/new.py", tmp_path, spec)
        assert src.allowed
        assert dst.allowed

    def test_dest_is_builtin(self, tmp_path):
        src = check_path("src/file.py", tmp_path, FenceSpec())
        dst = check_path(".git/hooks/pre-commit", tmp_path, FenceSpec())
        assert src.allowed
        assert not dst.allowed


# ═══════════════════════════════════════════════════════════════════════════
# Performance
# ═══════════════════════════════════════════════════════════════════════════


class TestPerformance:
    """1000-path check under 1 second (pure string work)."""

    def test_1000_paths_fast(self, tmp_path):
        spec = FenceSpec(
            allow_globs=("src/**", "tests/**", "docs/**"),
            deny_globs=("src/generated/**", "vendor/**"),
        )
        paths = [
            f"src/module_{i}/file_{j}.py" for i in range(100) for j in range(10)
        ]
        assert len(paths) == 1000

        start = time.monotonic()
        for p in paths:
            check_path(p, tmp_path, spec)
        elapsed = time.monotonic() - start
        assert elapsed < 1.0, f"1000 path checks took {elapsed:.2f}s"

    def test_1000_paths_with_all_deny_patterns(self, tmp_path):
        spec = FenceSpec(
            deny_globs=tuple(f"deny_{i}/**" for i in range(50)),
        )
        paths = [f"src/file_{i}.py" for i in range(1000)]

        start = time.monotonic()
        for p in paths:
            check_path(p, tmp_path, spec)
        elapsed = time.monotonic() - start
        assert elapsed < 1.0, f"1000 paths x 50 deny globs took {elapsed:.2f}s"


# ═══════════════════════════════════════════════════════════════════════════
# Load precedence
# ═══════════════════════════════════════════════════════════════════════════


class TestLoadFenceSpec:
    """Load precedence: per-job > [scope] config > defaults."""

    def test_default_is_empty(self):
        spec = load_fence_spec()
        assert spec.allow_globs == ()
        assert spec.deny_globs == ()

    def test_job_fences_loaded(self):
        spec = load_fence_spec(job_fences={
            "allow": ["src/**"],
            "deny": ["src/generated/**"],
        })
        assert spec.allow_globs == ("src/**",)
        assert spec.deny_globs == ("src/generated/**",)

    def test_config_scope_table(self, tmp_path):
        config = tmp_path / "remedy.toml"
        config.write_text(
            '[remedy.scope]\n'
            'allow = ["packages/**"]\n'
            'deny = ["packages/vendor/**"]\n',
            encoding="utf-8",
        )
        spec = load_fence_spec(config_path=config)
        assert spec.allow_globs == ("packages/**",)
        assert spec.deny_globs == ("packages/vendor/**",)

    def test_job_fences_beat_config(self, tmp_path):
        config = tmp_path / "remedy.toml"
        config.write_text(
            '[remedy.scope]\n'
            'allow = ["packages/**"]\n',
            encoding="utf-8",
        )
        spec = load_fence_spec(
            job_fences={"allow": ["src/**"], "deny": []},
            config_path=config,
        )
        assert spec.allow_globs == ("src/**",)

    def test_missing_config_falls_to_default(self):
        spec = load_fence_spec(config_path=Path("/nonexistent/remedy.toml"))
        assert spec == FenceSpec()

    def test_config_without_scope_falls_to_default(self, tmp_path):
        config = tmp_path / "remedy.toml"
        config.write_text('[remedy]\ndata_dir = ".data"\n', encoding="utf-8")
        spec = load_fence_spec(config_path=config)
        assert spec == FenceSpec()

    def test_malformed_config_falls_to_default(self, tmp_path):
        config = tmp_path / "remedy.toml"
        config.write_text("this is not valid toml {{{", encoding="utf-8")
        spec = load_fence_spec(config_path=config)
        assert spec == FenceSpec()

    def test_job_fences_deny_only(self):
        spec = load_fence_spec(job_fences={"deny": ["vendor/**"]})
        assert spec.allow_globs == ()
        assert spec.deny_globs == ("vendor/**",)

    def test_job_fences_allow_only(self):
        spec = load_fence_spec(job_fences={"allow": ["src/**"]})
        assert spec.allow_globs == ("src/**",)
        assert spec.deny_globs == ()


# ═══════════════════════════════════════════════════════════════════════════
# Result type contract
# ═══════════════════════════════════════════════════════════════════════════


class TestFenceCheckResultContract:
    """FenceCheckResult is frozen and has the right fields."""

    def test_frozen(self, tmp_path):
        result = check_path("src/main.py", tmp_path, FenceSpec())
        with pytest.raises(AttributeError):
            result.allowed = False  # type: ignore[misc]

    def test_allowed_result_fields(self, tmp_path):
        result = check_path("src/main.py", tmp_path, FenceSpec())
        assert isinstance(result.allowed, bool)
        assert isinstance(result.reason, str)
        assert result.allowed is True
        assert result.reason.startswith("allowed:")

    def test_denied_result_fields(self, tmp_path):
        result = check_path(".git/config", tmp_path, FenceSpec())
        assert result.allowed is False
        assert result.reason.startswith("denied:")

    def test_escape_result_fields(self, tmp_path):
        result = check_path("../x", tmp_path, FenceSpec())
        assert result.allowed is False
        assert result.reason.startswith("escapes_worktree:")


# ═══════════════════════════════════════════════════════════════════════════
# FenceSpec contract
# ═══════════════════════════════════════════════════════════════════════════


class TestFenceSpecContract:
    """FenceSpec is frozen and tuple-valued."""

    def test_frozen(self):
        spec = FenceSpec()
        with pytest.raises(AttributeError):
            spec.allow_globs = ("x",)  # type: ignore[misc]

    def test_default_empty(self):
        spec = FenceSpec()
        assert spec.allow_globs == ()
        assert spec.deny_globs == ()

    def test_equality(self):
        a = FenceSpec(allow_globs=("src/**",), deny_globs=("vendor/**",))
        b = FenceSpec(allow_globs=("src/**",), deny_globs=("vendor/**",))
        assert a == b
