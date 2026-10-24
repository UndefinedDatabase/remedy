"""F152 T001, DECISION F152 D3 (3) to (5); T002, DECISION F152 D4 (1) — the worker isolation
module's own pure helpers."""
from __future__ import annotations

import json
import os
import stat

import pytest

from packages.contracts.adapter_contract import WorkerIsolation
from packages.orchestration.worker_isolation import (
    WORKER_ISOLATION_FILENAME,
    create_throwaway_home,
    declared_isolation,
    isolated_child_env,
    record_worker_isolation,
    remove_throwaway_home,
    worker_env_digest,
    worker_isolation_record,
)

_ADR_REF = "docs/adr/0002-claude-cli-worker-isolation.md"

_APPLIES = WorkerIsolation(
    method="tool_flag", adr_ref=_ADR_REF, tool_args=("--x",), env_allowlist=("HOME", "PATH"))
_NOT_APPLIED = WorkerIsolation(
    method="tool_flag", adr_ref=_ADR_REF, tool_args=("--x",), env_allowlist=("HOME", "PATH"),
    applies=False)
_EMPTY_ALLOWLIST = WorkerIsolation(method="tool_flag", adr_ref=_ADR_REF, tool_args=("--x",))


class TestIsolatedChildEnv:
    def test_holds_exactly_the_allowlisted_names_present_in_the_source_and_none_other(self):
        source = {"HOME": "/srv/x", "PATH": "/bin", "SECRET_TOKEN": "s", "OTHER": "o"}
        env = isolated_child_env(_APPLIES, source)
        assert env == {"HOME": "/srv/x", "PATH": "/bin"}

    def test_is_none_while_not_applies(self):
        assert isolated_child_env(_NOT_APPLIED, {"HOME": "/srv/x"}) is None

    def test_is_none_for_an_empty_allowlist(self):
        assert isolated_child_env(_EMPTY_ALLOWLIST, {"HOME": "/srv/x"}) is None


class TestDeclaredIsolation:
    def test_returns_the_adapters_own_isolation_answer(self):
        class _Declaring:
            adapter_id = "stub"

            def isolation(self):
                return _APPLIES

        assert declared_isolation(_Declaring()) is _APPLIES

    def test_raises_naming_the_adapter_for_an_isolation_answering_none(self):
        class _NoneIsolation:
            adapter_id = "stub-none"

            def isolation(self):
                return None

        with pytest.raises(TypeError, match="stub-none"):
            declared_isolation(_NoneIsolation())


class TestWorkerEnvDigest:
    def test_is_equal_for_equal_environments(self):
        env = {"HOME": "/srv/x", "PATH": "/bin"}
        assert worker_env_digest(dict(env)) == worker_env_digest(dict(env))

    def test_differs_when_a_non_secret_value_differs(self):
        first = worker_env_digest({"HOME": "/srv/x", "PATH": "/bin"})
        second = worker_env_digest({"HOME": "/srv/y", "PATH": "/bin"})
        assert first != second

    def test_is_equal_when_only_a_secret_named_value_differs(self):
        first = worker_env_digest({"HOME": "/srv/x", "ANTHROPIC_API_KEY": "sk-one"})
        second = worker_env_digest({"HOME": "/srv/x", "ANTHROPIC_API_KEY": "sk-two"})
        assert first == second

    def test_never_contains_a_value(self):
        digest = worker_env_digest({"HOME": "/srv/super-secret-path", "ANTHROPIC_API_KEY": "sk-x"})
        assert "/srv/super-secret-path" not in digest and "sk-x" not in digest

    def test_is_none_for_none(self):
        assert worker_env_digest(None) is None


class TestWorkerIsolationRecord:
    def test_fields_and_home_is_operator(self):
        env = {"HOME": "/srv/x", "PATH": "/bin"}
        record = worker_isolation_record(_APPLIES, env)
        assert record["method"] == "tool_flag"
        assert record["applied"] is True
        assert record["home"] == "operator"
        assert record["env_digest"] == worker_env_digest(env)
        assert record["names"] == ["HOME", "PATH"]
        assert record["tool_args"] == ["--x"]
        assert record["adr_ref"] == _ADR_REF

    def test_env_digest_none_and_names_empty_when_inherited(self):
        record = worker_isolation_record(_NOT_APPLIED, None)
        assert record["env_digest"] is None
        assert record["names"] == []


class TestRecordWorkerIsolation:
    def test_writes_nothing_for_a_falsy_directory(self, tmp_path):
        record_worker_isolation(
            None, role="builder", provider="claude-cli", model="m",
            record=worker_isolation_record(_APPLIES, {"HOME": "/x"}))
        record_worker_isolation(
            "", role="builder", provider="claude-cli", model="m",
            record=worker_isolation_record(_APPLIES, {"HOME": "/x"}))
        assert list(tmp_path.iterdir()) == []

    def test_appends_one_parseable_line_per_call(self, tmp_path):
        record = worker_isolation_record(_APPLIES, {"HOME": "/x", "PATH": "/bin"})
        record_worker_isolation(
            str(tmp_path), role="builder", provider="claude-cli", model="m", record=record)
        record_worker_isolation(
            str(tmp_path), role="reviewer", provider="claude-cli", model="m", record=record)
        lines = (tmp_path / WORKER_ISOLATION_FILENAME).read_text(encoding="utf-8").splitlines()
        assert len(lines) == 2
        parsed = [json.loads(line) for line in lines]
        assert [p["role"] for p in parsed] == ["builder", "reviewer"]
        assert all(p["provider"] == "claude-cli" and p["model"] == "m" for p in parsed)


class TestThrowawayHome:
    def test_create_makes_a_private_worker_home_directory(self, tmp_path):
        path = create_throwaway_home(str(tmp_path))
        assert path.startswith(str(tmp_path))
        assert os.path.basename(path).startswith("worker-home-")
        mode = stat.S_IMODE(os.stat(path).st_mode)
        assert mode == 0o700

    def test_remove_deletes_the_directory(self, tmp_path):
        path = create_throwaway_home(str(tmp_path))
        remove_throwaway_home(path)
        assert not os.path.exists(path)

    def test_remove_refuses_a_directory_not_so_named(self, tmp_path):
        other = tmp_path / "not-a-worker-home"
        other.mkdir()
        with pytest.raises(ValueError, match="worker-home-"):
            remove_throwaway_home(str(other))
        assert other.exists()
