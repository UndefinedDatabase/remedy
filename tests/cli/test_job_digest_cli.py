"""F040 T003 — the `digest` section of `remedy job show <id> --full`, formerly the
`job digest` command, is the CLI's own view of the completion digest, the HTTP
route's little sibling.

The property this file exists to defend: the CLI and the route can never
print a different envelope for the same job, because both reach it through
the SAME two calls (`resolve_job_id`/`load_job` then `load_run_events`) and
the SAME `build_job_digest` composition. Each test below carries its own
discriminator, matching the mutations the guard was red-proved against:
(a) the section's text leaking JSON, (b) the JSON envelope gaining an extra
wrapping key, and (d) short-id-prefix resolution being skipped. Mutation (c),
the not-found message losing its `--json`/bare split, left with the command:
an unknown id is `job show`'s own error, tested with `job show`.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from apps.cli.grouped import main
from packages.core.models import RunState
from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.job_digest import build_job_digest
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
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
              task_status: RunState = RunState.COMPLETED) -> JobPlan:
    job = JobPlan(
        job_title="digest-job",
        user_prompt="build the thing",
        mission="Build the thing",
        tasks=[TaskEntry(title=f"task {i}", inputs={"task_type": "documentation"})
               for i in range(2)],
        state=state,
        metadata={"target_repo": "/tmp/repo", "cycle_terminal_status": terminal},
    )
    for task in job.tasks:
        task.status = task_status
    save_job_plan(job)
    return job


def show_digest(capsys, job_id: str) -> tuple[dict, str]:
    """`job show <id> --full`: the digest section's envelope, and its text on stderr up to the next heading."""
    main(["job", "show", job_id, "--full"])
    shown = capsys.readouterr()
    text = shown.err.split("--- Digest ---\n", 1)[1].split("\n--- ", 1)[0]
    return json.loads(shown.out)["sections"]["digest"], text


class TestJsonModeMatchesTheEnvelopeExactly:
    """The exact-equality assertion that catches mutations (a) and (b) both:
    (a) would leak JSON into the section's text, not the JSON body itself, but
    (a)'s real failure surfaces via TestBareModeIsNotJson below; here the
    discriminator is that the section's data must be BYTE-FOR-BYTE the same
    dict `build_job_digest` returns for this job — an extra wrapping key
    (mutation b) breaks the `==` immediately.
    """

    def test_the_json_payload_equals_build_job_digest_independently_computed(self, capsys):
        job = saved_job()
        section, _text = show_digest(capsys, str(job.job_id))
        assert section["ok"] is True
        payload = section["data"]

        expected = build_job_digest(
            job, load_run_events(resolve_data_root(), job.job_id))
        assert payload == expected

    def test_the_payload_is_not_wrapped_in_an_extra_key(self, capsys):
        """Direct discriminator for mutation (b): a `{'digest': ...}` wrapper
        would still be valid JSON but would not equal the digest dict itself."""
        job = saved_job()
        section, _text = show_digest(capsys, str(job.job_id))
        payload = section["data"]
        assert "digest" not in payload
        assert set(payload.keys()) == set(
            build_job_digest(job, load_run_events(resolve_data_root(), job.job_id)).keys())


class TestBareModeIsNotJson:
    """Direct discriminator for mutation (a): text lines that were the JSON
    envelope would parse cleanly as JSON — the opposite of what this test
    wants."""

    def test_bare_output_does_not_parse_as_json(self, capsys):
        job = saved_job()
        _section, out = show_digest(capsys, str(job.job_id))
        with pytest.raises(json.JSONDecodeError):
            json.loads(out)

    def test_bare_output_names_the_job_id_and_the_digest_state(self, capsys):
        job = saved_job()
        _section, out = show_digest(capsys, str(job.job_id))
        expected = build_job_digest(
            job, load_run_events(resolve_data_root(), job.job_id))
        assert str(job.job_id) in out
        assert expected["state"] in out


class TestShortIdPrefixResolves:
    """Direct discriminator for mutation (d): `job_id = job_id_str` would
    skip `resolve_job_id`'s own short-prefix lookup, so an 8-character
    prefix would fail to resolve at all."""

    def test_an_eight_character_prefix_matches_the_full_id_digest(self, capsys):
        job = saved_job()
        full_section, _text = show_digest(capsys, str(job.job_id))
        assert full_section["ok"] is True

        prefix_section, _text = show_digest(capsys, str(job.job_id)[:8])

        assert prefix_section == full_section
