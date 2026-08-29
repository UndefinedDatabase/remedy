"""F040 T003 — `remedy job digest <id>` is the CLI's own view of the
completion digest, the HTTP route's little sibling.

The property this file exists to defend: the CLI and the route can never
print a different envelope for the same job, because both reach it through
the SAME two calls (`resolve_job_id`/`load_job` then `load_run_events`) and
the SAME `build_job_digest` composition. Each test below carries its own
discriminator, matching the four mutations this round's guard is red-proved
against: (a) bare mode leaking JSON, (b) the JSON envelope gaining an extra
wrapping key, (c) the not-found message losing its `--json`/bare split, and
(d) short-id-prefix resolution being skipped.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from apps.cli.command_catalog import CATALOG, get_command
from apps.cli.commands.job import _cmd_job_digest
from packages.core.models import Job, RunState, Task
from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.job_digest import build_job_digest
from packages.orchestration.storage import save_job
from packages.orchestration.timeline import load_run_events

pytestmark = pytest.mark.integration

UTC = timezone.utc
T0 = datetime(2026, 7, 31, 12, 0, 0, tzinfo=UTC)


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def saved_job(*, state: RunState = RunState.COMPLETED,
              terminal: str = "all_green",
              task_status: RunState = RunState.COMPLETED) -> Job:
    job = Job(
        name="digest-job",
        user_prompt="build the thing",
        mission="Build the thing",
        tasks=[Task(description=f"task {i}", inputs={"task_type": "documentation"})
               for i in range(2)],
        state=state,
        metadata={"target_repo": "/tmp/repo", "cycle_terminal_status": terminal},
    )
    for task in job.tasks:
        task.status = task_status
    save_job(job)
    return job


class TestJsonModeMatchesTheEnvelopeExactly:
    """The exact-equality assertion that catches mutations (a) and (b) both:
    (a) would leak JSON in bare mode, not the JSON body itself, but (a)'s
    real failure surfaces via TestBareModeIsNotJson below; here the
    discriminator is that the printed payload must be BYTE-FOR-BYTE the same
    dict `build_job_digest` returns for this job — an extra wrapping key
    (mutation b) breaks the `==` immediately.
    """

    def test_the_json_payload_equals_build_job_digest_independently_computed(self, capsys):
        job = saved_job()
        _cmd_job_digest(str(job.id), json_output=True)
        payload = json.loads(capsys.readouterr().out)

        expected = build_job_digest(
            job, load_run_events(resolve_data_root(), job.id))
        assert payload == expected

    def test_the_payload_is_not_wrapped_in_an_extra_key(self, capsys):
        """Direct discriminator for mutation (b): a `{'digest': ...}` wrapper
        would still be valid JSON but would not equal the digest dict itself."""
        job = saved_job()
        _cmd_job_digest(str(job.id), json_output=True)
        payload = json.loads(capsys.readouterr().out)
        assert "digest" not in payload
        assert set(payload.keys()) == set(
            build_job_digest(job, load_run_events(resolve_data_root(), job.id)).keys())


class TestBareModeIsNotJson:
    """Direct discriminator for mutation (a): `if True:` would make bare
    mode also emit the JSON envelope, which parses cleanly as JSON — the
    opposite of what this test wants."""

    def test_bare_output_does_not_parse_as_json(self, capsys):
        job = saved_job()
        _cmd_job_digest(str(job.id))
        out = capsys.readouterr().out
        with pytest.raises(json.JSONDecodeError):
            json.loads(out)

    def test_bare_output_names_the_job_id_and_the_digest_state(self, capsys):
        job = saved_job()
        _cmd_job_digest(str(job.id))
        out = capsys.readouterr().out
        expected = build_job_digest(
            job, load_run_events(resolve_data_root(), job.id))
        assert str(job.id) in out
        assert expected["state"] in out


class TestUnknownJobId:
    """Direct discriminator for mutation (c): deleting the `if
    json_output:`/`else:` split would make the plain-text stderr line print
    even under `--json`, so bare-mode's stderr message would leak into the
    `--json` invocation's stdout-only contract."""

    UNKNOWN = "ffffffff-ffff-4fff-8fff-ffffffffffff"

    def test_bare_mode_exits_1_with_a_clean_stderr_message(self, capsys):
        with pytest.raises(SystemExit) as exc:
            _cmd_job_digest(self.UNKNOWN)
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert captured.err.strip() == f"Error: job not found: {self.UNKNOWN}"
        assert "Traceback" not in captured.err
        assert captured.out == ""

    def test_json_mode_exits_1_with_a_json_payload_on_stdout(self, capsys):
        with pytest.raises(SystemExit) as exc:
            _cmd_job_digest(self.UNKNOWN, json_output=True)
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert captured.err == ""
        payload = json.loads(captured.out)
        assert payload["error"] == "job_not_found"
        assert payload["job_id"] == self.UNKNOWN


class TestShortIdPrefixResolves:
    """Direct discriminator for mutation (d): `job_id = job_id_str` would
    skip `resolve_job_id`'s own short-prefix lookup, so an 8-character
    prefix would fail to resolve at all."""

    def test_an_eight_character_prefix_matches_the_full_id_digest(self, capsys):
        job = saved_job()
        _cmd_job_digest(str(job.id), json_output=True)
        full_payload = json.loads(capsys.readouterr().out)

        _cmd_job_digest(str(job.id)[:8], json_output=True)
        prefix_payload = json.loads(capsys.readouterr().out)

        assert prefix_payload == full_payload


class TestCatalogRegistration:

    def test_the_catalog_registers_job_digest_exactly_once(self):
        matches = [e for e in CATALOG if e.command_id == "job.digest"]
        assert len(matches) == 1, matches

    def test_the_command_declares_job_id_and_json_args(self):
        names = [a.name for a in get_command("job.digest").args]
        assert "job_id" in names
        assert "--json" in names
