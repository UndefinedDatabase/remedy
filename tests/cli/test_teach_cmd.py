"""Tests for `remedy teach narrate` and `remedy teach ask` (F255 T002-T004).

The load-bearing property is T003's, now carried by both commands: what they
write is proven BEHAVIOURALLY rather than asserted — every file under the data
root is hashed before and after the call and the two maps are compared.

`narrate` writes NOTHING, so its comparison covers the whole tree. `ask` writes
EXACTLY one token-ledger row (DECISION F255 D10), so its comparison excludes the
ledger and its sqlite sidecars BY EXPLICIT NAME and then asserts that the
excluded set is exactly those paths. Excluding by name is the point: a silent
exclusion would hide any OTHER write and the proof would claim the opposite of
what it shows.

`ask --file` is grounding source (2)'s only production caller (finding R-0610),
so the tests for it assert what the MODEL WAS SHOWN — the prompt captured at the
transport seam — rather than what the command intended to show it.

NO TEST HERE OPENS A SOCKET. Every `ask` supplies the transport seam of
``teacher_model.ask_teacher``, so no test needs a running Ollama.

Deliberately NOT re-asserted here: the sentences themselves, which
tests/orchestration/test_teacher_narration.py pins at module level, and the
transport's own behaviour, which tests/orchestration/test_teacher_model.py pins.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

import pytest

from apps.cli.command_catalog import get_command, get_commands_for_group
from apps.cli.commands.teach_cmd import (
    _UNBILLED_NOTE,
    COMMAND_HANDLERS,
    _cmd_teach_ask,
    _cmd_teach_narrate,
)
from packages.orchestration import teacher_model
from packages.orchestration.role_config import RoleConfig
from packages.orchestration.teacher_model import TeacherReply, TeacherTransportUnavailable
from packages.orchestration.teacher_spend import TEACHER_ROLE, TeacherUsage

_JOB_ID = "3f2b1a90-0000-4000-8000-000000000001"

_EVENTS = [
    {"event": "job_created", "timestamp": "2026-08-21T00:00:01Z"},
    {"event": "task_run_started", "task_id": "t7", "timestamp": "2026-08-21T00:00:02Z"},
    {"event": "some_unlisted_event", "timestamp": "2026-08-21T00:00:03Z"},
]


def _write_run_log(root: Path, job_id: str, events: list[dict]) -> Path:
    """A run log at the real relative path ``load_run_events`` reads."""
    runs = root / "job_logs" / job_id
    runs.mkdir(parents=True, exist_ok=True)
    log = runs / "run-1.jsonl"
    log.write_text(
        "\n".join(json.dumps(e, separators=(",", ":")) for e in events) + "\n",
        encoding="utf-8",
    )
    return log


#: The ONE file `remedy teach ask` is allowed to write, plus the sqlite sidecars
#: (`-wal`, `-shm`) that come with it. Spelled out here so the read-only proof
#: excludes it BY NAME and can assert what it excluded — an exclusion nobody
#: states is an exclusion that hides every other write.
_LEDGER_NAME_PREFIX = "ledger.sqlite"


def _hash_tree(root: Path, *, excluding: str | None = None) -> dict[str, str]:
    """Every file under ``root``, mapped to the sha256 of its bytes.

    ``excluding`` drops files whose NAME starts with that prefix, and nothing
    else: no directory rule, no glob, no silent skip.
    """
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and not (excluding is not None and path.name.startswith(excluding))
    }


def _exit_code(call) -> int:
    """The exit code a CLI handler produces — 0 when it returns normally."""
    try:
        call()
    except SystemExit as exc:
        return int(exc.code or 0)
    return 0


def _ledger_rows(ledger: Path) -> list[dict]:
    """Every ledger row, read straight from SQLite."""
    conn = sqlite3.connect(ledger)
    try:
        conn.row_factory = sqlite3.Row
        return [dict(r) for r in conn.execute("SELECT * FROM calls ORDER BY call_id")]
    finally:
        conn.close()


def _answering(text: str = "here is what happened"):
    """A fake transport seam: answers offline, so no test needs a running Ollama."""
    def call(prompt: str, *, model: str) -> TeacherReply:
        return TeacherReply(text=text, usage=TeacherUsage(tokens_in=9, tokens_out=3))

    return call


def _capturing(text: str = "here is what happened"):
    """A fake transport seam that KEEPS every prompt it is handed.

    Returns the seam and the list it appends to, so a test can assert what the
    model really saw instead of trusting the command's own description of it.
    """
    prompts: list[str] = []

    def call(prompt: str, *, model: str) -> TeacherReply:
        prompts.append(prompt)
        return TeacherReply(text=text, usage=TeacherUsage(tokens_in=9, tokens_out=3))

    return call, prompts


def _failing(reason: str = "the Ollama call failed: connection refused"):
    """A fake transport seam that is UNAVAILABLE, the D9 refusal condition."""
    def call(prompt: str, *, model: str) -> TeacherReply:
        raise TeacherTransportUnavailable(reason)

    return call


@pytest.fixture()
def data_root(tmp_path, monkeypatch):
    root = tmp_path / "data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture()
def teacher_ledger(data_root, monkeypatch):
    """A registered project, so `ask` resolves a REAL ledger under the data root."""
    from packages.orchestration.project_registry import RemyProject, save_project

    project = RemyProject(name="Teacher Test Project", slug="teacher-test")
    save_project(project)
    monkeypatch.setenv("REMEDY_PROJECT", "teacher-test")
    return data_root / "projects" / str(project.id) / _LEDGER_NAME_PREFIX


class TestTeachNarrateIsReadOnly:
    """T003: the run's files are byte-identical before and after the command."""

    def test_narrating_changes_no_byte_under_the_data_root(self, data_root, capsys):
        _write_run_log(data_root, _JOB_ID, _EVENTS)
        before = _hash_tree(data_root)
        assert before, "the fixture must put at least one file on disk"

        _cmd_teach_narrate(_JOB_ID)
        capsys.readouterr()

        assert _hash_tree(data_root) == before

    def test_narrating_creates_and_removes_no_file(self, data_root, capsys):
        _write_run_log(data_root, _JOB_ID, _EVENTS)
        before = sorted(p.relative_to(data_root) for p in data_root.rglob("*"))
        _cmd_teach_narrate(_JOB_ID)
        capsys.readouterr()
        assert sorted(p.relative_to(data_root) for p in data_root.rglob("*")) == before

    def test_narrating_appends_no_run_log_event(self, data_root, capsys):
        log = _write_run_log(data_root, _JOB_ID, _EVENTS)
        before = log.read_bytes()
        _cmd_teach_narrate(_JOB_ID)
        capsys.readouterr()
        assert log.read_bytes() == before

    def test_a_job_with_no_run_log_writes_nothing_and_says_so(self, data_root, capsys):
        _cmd_teach_narrate(_JOB_ID)
        out = capsys.readouterr().out
        assert "no events yet" in out and "(0 events)" in out
        assert _hash_tree(data_root) == {}


class TestTeachReachesTaskJobs:
    """The teacher can explain a `remedy do job-run` job, not only a classic one.

    Operator dogfooding on 2026-08-25: `remedy teach narrate edbbc42bba4c4b00`
    answered "no job matches prefix" while that job's run log sat in
    `<data_root>/runs/edbbc42bba4c4b00/`. `resolve_job_id` searched
    `jobs/*.json` and returned a UUID; a task job is a DIRECTORY under
    `jobs/` named by sixteen hex characters, which is not a UUID. The
    teacher was built against the classic store and could not see a job-based
    run at all.
    """

    #: The real shape: `pingpong_job` mints `uuid4().hex[:16]`.
    TASK_JOB_ID = "edbbc42bba4c4b00"

    def _write_task_job(self, data_root: Path, job_id: str) -> None:
        from packages.orchestration.data_paths import job_dir

        job_root = job_dir(job_id, data_root)
        job_root.mkdir(parents=True)
        (job_root / "job.json").write_text(
            json.dumps({"job_id": job_id, "status": "completed"}), encoding="utf-8")

    def test_narrate_finds_a_task_job_and_reads_its_run_log(self, data_root, capsys):
        self._write_task_job(data_root, self.TASK_JOB_ID)
        _write_run_log(data_root, self.TASK_JOB_ID, _EVENTS)

        assert _exit_code(lambda: _cmd_teach_narrate(self.TASK_JOB_ID)) == 0
        out = capsys.readouterr().out

        assert "no job matches prefix" not in out
        assert f"({len(_EVENTS)} events)" in out
        assert "The job was created." in out

    def test_narrate_accepts_a_task_job_prefix(self, data_root, capsys):
        self._write_task_job(data_root, self.TASK_JOB_ID)
        _write_run_log(data_root, self.TASK_JOB_ID, _EVENTS)

        assert _exit_code(lambda: _cmd_teach_narrate(self.TASK_JOB_ID[:8])) == 0
        assert f"({len(_EVENTS)} events)" in capsys.readouterr().out

    def test_narrating_a_task_job_still_writes_nothing(self, data_root, capsys):
        """The read-only stance survives the wider resolver."""
        self._write_task_job(data_root, self.TASK_JOB_ID)
        _write_run_log(data_root, self.TASK_JOB_ID, _EVENTS)
        before = _hash_tree(data_root)
        assert before

        _cmd_teach_narrate(self.TASK_JOB_ID)
        capsys.readouterr()

        assert _hash_tree(data_root) == before

    def test_a_classic_job_still_resolves(self, data_root, capsys):
        """The wider resolver ADDS a store; it takes none away."""
        _write_run_log(data_root, _JOB_ID, _EVENTS)

        assert _exit_code(lambda: _cmd_teach_narrate(_JOB_ID)) == 0
        assert f"({len(_EVENTS)} events)" in capsys.readouterr().out

    def test_an_unknown_id_still_exits_one(self, data_root, capsys):
        assert _exit_code(lambda: _cmd_teach_narrate("dddddddddddddddd")) == 1
        assert "no job matches prefix" in capsys.readouterr().err

    def test_a_directory_without_a_job_file_is_not_a_job(self, data_root, capsys):
        """A half-created or hand-made directory must not resolve as a job."""
        from packages.orchestration.data_paths import job_dir

        job_dir(self.TASK_JOB_ID, data_root).mkdir(parents=True)

        assert _exit_code(lambda: _cmd_teach_narrate(self.TASK_JOB_ID)) == 1
        assert "no job matches prefix" in capsys.readouterr().err


class TestTeachCatalogDeclaration:
    def test_the_command_is_declared_read_only(self):
        cmd = get_command("teach.narrate")
        # T003 declares the action class as well as proving the behaviour: the
        # catalog is what a permission layer reads, and the tests above are what
        # make the declaration true rather than merely stated.
        assert cmd.action_class == "read_only"
        assert cmd.may_mutate_repo is False
        assert cmd.may_execute_commands is False
        assert cmd.requires_permission is False

    def test_ask_is_declared_write_metadata_because_it_writes_a_ledger_row(self):
        cmd = get_command("teach.ask")
        # DECISION F255 D10: `ask` writes exactly one token-ledger row, so a
        # read_only declaration here would be false — and a false declaration
        # misleads the permission layer that reads this catalog.
        assert cmd.action_class == "write_metadata"
        assert cmd.may_mutate_repo is False
        assert cmd.may_execute_commands is False
        assert cmd.supports_json is True
        assert cmd.related == ("teach.narrate",)

    def test_the_handler_table_covers_every_declared_teach_command(self):
        # EQUALITY of the two sets, never a subset: a declared command with no
        # handler and a handler with no declaration are both defects, and only
        # equality catches the second one.
        declared = {c.command_id for c in get_commands_for_group("teach")}
        assert declared == {"teach.narrate", "teach.ask"} == set(COMMAND_HANDLERS)


class TestTeachAskWritesOnlyTheLedger:
    """T004: everything under the data root is byte-identical EXCEPT the ledger."""

    def test_asking_changes_no_byte_under_the_data_root_except_the_ledger(
        self, data_root, teacher_ledger, capsys
    ):
        _write_run_log(data_root, _JOB_ID, _EVENTS)
        before = _hash_tree(data_root, excluding=_LEDGER_NAME_PREFIX)
        assert before, "the fixture must put at least one file on disk"

        _cmd_teach_ask("what happened?", job_id=_JOB_ID, call=_answering())
        capsys.readouterr()

        assert _hash_tree(data_root, excluding=_LEDGER_NAME_PREFIX) == before

    def test_the_excluded_set_is_exactly_the_ledger_and_its_sidecars(
        self, data_root, teacher_ledger, capsys
    ):
        _write_run_log(data_root, _JOB_ID, _EVENTS)

        _cmd_teach_ask("what happened?", job_id=_JOB_ID, call=_answering())
        capsys.readouterr()

        every = _hash_tree(data_root)
        kept = _hash_tree(data_root, excluding=_LEDGER_NAME_PREFIX)
        excluded = set(every) - set(kept)
        # The exclusion is NAMED, not silent: it is exactly the paths whose file
        # name begins with `ledger.sqlite`, and it is non-empty, so the test is
        # excluding something that really was written rather than nothing.
        assert excluded == {
            rel for rel in every if Path(rel).name.startswith(_LEDGER_NAME_PREFIX)
        }
        assert excluded
        assert teacher_ledger.is_file()


class TestTeachAskWritesExactlyOneRow:
    def test_one_ask_writes_exactly_one_teacher_row(self, teacher_ledger, capsys):
        _cmd_teach_ask("what is a task?", call=_answering())
        capsys.readouterr()

        rows = _ledger_rows(teacher_ledger)
        assert len(rows) == 1
        assert rows[0]["role"] == TEACHER_ROLE
        # NULL task_id is the MARK of the class (DECISION F255 D7): a question
        # is not a finalized task run and must never be queryable as one.
        assert rows[0]["task_id"] is None

    def test_the_role_split_reports_teacher_apart_from_the_mission_roles(
        self, teacher_ledger, capsys
    ):
        from packages.orchestration.token_ledger import (
            COST_BASIS_UNKNOWN,
            CallRecord,
            query_cost,
            record_call,
        )

        _cmd_teach_ask("what is a task?", call=_answering())
        capsys.readouterr()
        record_call(
            CallRecord(
                call_id="job-1:task-1",
                job_id="job-1",
                task_id="task-1",
                role="builder",
                model="mission-model",
                ts_utc="2026-08-21T00:00:00+00:00",
                tokens_in=100,
                cost_basis=COST_BASIS_UNKNOWN,
            ),
            path=teacher_ledger,
        )

        buckets = {row.bucket: row for row in query_cost(path=teacher_ledger, by="role").rows}
        assert set(buckets) == {"builder", TEACHER_ROLE}
        assert buckets[TEACHER_ROLE].calls == 1
        assert buckets[TEACHER_ROLE].tokens_in == 9


class TestTeachAskRefusesWithoutBilling:
    """A REFUSAL IS NEVER BILLED: no call happened, so no row may claim one."""

    def test_a_provider_with_no_teacher_transport_refuses_and_writes_no_row(
        self, teacher_ledger, monkeypatch, capsys
    ):
        monkeypatch.setattr(
            teacher_model,
            "resolve_role_config",
            lambda role, **kw: RoleConfig(role=role, provider="claude-cli", model="opus"),
        )

        code = _exit_code(lambda: _cmd_teach_ask("what is a task?", call=_answering()))

        out = capsys.readouterr().out
        # Exit 0: a teacher that could fail a run would not be the passive role.
        assert code == 0
        assert "claude-cli" in out and "opus" in out
        # It names Stage 1, which keeps working because Stage 1 is offline.
        assert "remedy teach narrate" in out
        assert _UNBILLED_NOTE in out
        assert not teacher_ledger.exists()

    def test_a_failing_transport_refuses_and_writes_no_row(self, teacher_ledger, capsys):
        code = _exit_code(lambda: _cmd_teach_ask("what is a task?", call=_failing()))

        out = capsys.readouterr().out
        assert code == 0
        assert "connection refused" in out
        assert "remedy teach narrate" in out
        assert _UNBILLED_NOTE in out
        assert not teacher_ledger.exists()


class TestTeachAskOutput:
    def test_the_answer_names_its_model_and_its_grounding_sources(
        self, data_root, teacher_ledger, capsys
    ):
        _write_run_log(data_root, _JOB_ID, _EVENTS)

        _cmd_teach_ask("what happened?", job_id=_JOB_ID, call=_answering())

        out = capsys.readouterr().out
        assert "here is what happened" in out
        assert "Grounding sources: ledger, concept" in out
        assert _UNBILLED_NOTE not in out

    def test_json_output_carries_the_row_id_and_the_billed_flag(self, teacher_ledger, capsys):
        _cmd_teach_ask("what is a task?", call=_answering(), json_output=True)

        payload = json.loads(capsys.readouterr().out)
        assert payload["refused"] is False
        assert payload["billed"] is True
        assert payload["call_id"] == _ledger_rows(teacher_ledger)[0]["call_id"]
        assert payload["grounding_sources"] == ["concept"]


#: The grounding file every `--file` test points at. Short and unmistakable, so
#: finding it inside a rendered prompt cannot be a coincidence.
_CODE_TEXT = "def add_two_numbers(a, b):\n    return a + b\n"


class TestTeachAskGroundsInAWorkspaceFile:
    """T004 / R-0610: `--file` gives grounding source (2) a production caller.

    Before this option existed, `code` and `code_path` were accepted by
    ``ask_teacher`` and passed by NOTHING outside the tests, so source (2) was
    reachable from the suite alone. These four hold the option to that fix.
    """

    def test_the_file_reaches_the_prompt_and_the_grounding_sources(
        self, tmp_path, data_root, teacher_ledger, capsys
    ):
        source = tmp_path / "adder.py"
        source.write_text(_CODE_TEXT, encoding="utf-8")
        call, prompts = _capturing()

        _cmd_teach_ask(
            "what does this do?", file=str(source), call=call, json_output=True
        )

        payload = json.loads(capsys.readouterr().out)
        # The model was SHOWN the code and told where it came from — asserting
        # the prompt, not the intent, is what makes this a caller proof.
        assert len(prompts) == 1
        assert _CODE_TEXT in prompts[0]
        assert str(source) in prompts[0]
        assert "code" in payload["grounding_sources"]

    def test_without_the_option_no_code_reaches_the_prompt(
        self, data_root, teacher_ledger, capsys
    ):
        call, prompts = _capturing()

        _cmd_teach_ask("what is a task?", call=call, json_output=True)

        payload = json.loads(capsys.readouterr().out)
        # Unchanged behaviour is part of the fix: the option adds a source, it
        # does not alter the answer given without it.
        assert "code" not in payload["grounding_sources"]
        assert len(prompts) == 1
        assert "[code]" not in prompts[0]

    def test_an_unreadable_path_is_said_out_loud_and_the_answer_still_comes(
        self, tmp_path, data_root, teacher_ledger, capsys
    ):
        missing = tmp_path / "no-such-file.py"
        call, prompts = _capturing()

        exit_code = _exit_code(
            lambda: _cmd_teach_ask("what does this do?", file=str(missing), call=call)
        )

        out = capsys.readouterr().out
        # Exit 0 with an answer: a teacher that could fail a run would not be
        # passive. But NEVER silently — an operator not told would believe the
        # answer had read code it never opened.
        assert exit_code == 0
        assert str(missing) in out
        assert "here is what happened" in out
        assert "Grounding sources: concept" in out
        assert "[code]" not in prompts[0]

    def test_reading_a_file_writes_nothing_and_leaves_it_untouched(
        self, tmp_path, data_root, teacher_ledger, capsys
    ):
        source = tmp_path / "adder.py"
        source.write_text(_CODE_TEXT, encoding="utf-8")
        before_source = source.read_bytes()
        _write_run_log(data_root, _JOB_ID, _EVENTS)
        before = _hash_tree(data_root, excluding=_LEDGER_NAME_PREFIX)
        assert before, "the fixture must put at least one file on disk"

        _cmd_teach_ask("what does this do?", file=str(source), call=_answering())
        capsys.readouterr()

        # The ledger row stays the only write (DECISION F255 D10), and the file
        # the teacher read is byte-identical afterwards.
        assert _hash_tree(data_root, excluding=_LEDGER_NAME_PREFIX) == before
        assert source.read_bytes() == before_source
