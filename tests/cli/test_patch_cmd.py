"""F033 — `remedy patch approve-hunks`, the operator's door onto the hunk recorder.

One test per PROPERTY the command turns on. The command wires three pieces that already
carry their own suites — `resolve_job_evidence_dir` answers WHICH directory,
`build_diff_view` turns it into the viewer's envelope, and `record_hunk_decision_from_view`
validates the decision against that envelope and records the ledger — so what is pinned here
is the WIRING and nothing the three already pin for themselves:

  - the entry resolves through `get_command` and the handler is really registered, which is
    the pair `apps/cli/grouped.py` answers `Error: no handler for <id>` on when it is broken;
  - a mixed decision lands under the ENVELOPE-derived attempt key `<task_id>:<source>`, and
    `save_job` really persisted it — proved by loading the job back off disk;
  - `--reject-hunk <id>=<reason>` splits on the FIRST `=` and keeps BOTH halves VERBATIM,
    surrounding whitespace and any further `=` included;
  - a `--reject-hunk` value with no `=` comes back as the decision core's own
    `missing_reason`, NOT as a refusal this handler minted — one fault, one word for it;
  - a refusal exits 1, never calls `save_job`, and leaves `job.metadata` with no decisions
    key at all;
  - a job whose evidence directory does not resolve gets `no_diff_available`;
  - the evidence directory is resolved from the RESOLVED job id, so a short hex prefix and
    an uppercase UUID record exactly as the canonical lowercase id does (finding R-0744);
  - an unknown job id exits 1;
  - `--json` prints parseable JSON on BOTH the success and the refusal path.

The job, the isolated data root and the captured output follow `tests/cli/test_job_stop.py`
and `tests/cli/test_decision_answers.py`; the `difflib` diff recipe follows
`tests/orchestration/test_hunk_decision_record.py`. All three are RESTATED rather than
imported: a test file reaching into another test file's helpers couples two suites that have
no reason to move together.
"""

from __future__ import annotations

import difflib
import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from apps.cli.command_catalog import get_command
from apps.cli.commands import collect_all_handlers
from apps.cli.commands import patch as CMD
from packages.core.models import Job
from packages.orchestration.data_paths import job_evidence_index_dir, resolve_job_id
from packages.orchestration.diff_parser import parse_unified_diff_to_view
from packages.orchestration.diff_view_source import (
    DIFF_JOB_ARTIFACT_NAME,
    DIFF_REASON_NO_EVIDENCE_DIR,
    DIFF_TASK_RUN_ARTIFACT_NAME,
    DIFF_TASK_RUNS_DIR_NAME,
)
from packages.orchestration.evidence_index import resolve_job_evidence_dir
from packages.orchestration.hunk_approval import REFUSAL_MISSING_REASON
from packages.orchestration.hunk_decision_record import (
    HUNK_DECISIONS_METADATA_KEY,
    HUNK_RECORD_REFUSAL_NO_DIFF,
)
from packages.orchestration.storage import load_job, save_job

ORIGINAL = "\n".join(f"line {number:02d}" for number in range(1, 31)) + "\n"

#: An operator's reason carrying surrounding whitespace AND an `=` of its own, so both
#: "verbatim" and "split on the FIRST `=`" are testable claims rather than descriptions.
REASON = "  DSN=postgres://x is out of scope  "


def _edited(*replacements: tuple[str, str]) -> str:
    text = ORIGINAL
    for old, new in replacements:
        text = text.replace(old + "\n", new + "\n")
    return text


def _diff_of(new_text: str, path: str) -> str:
    return "".join(
        difflib.unified_diff(
            ORIGINAL.splitlines(True), new_text.splitlines(True),
            fromfile=f"a/{path}", tofile=f"b/{path}",
        )
    )


#: Three edits spaced further apart than twice `difflib`'s context, so they really arrive as
#: three separate hunks and a decision can leave one of them PENDING.
THREE_HUNK_DIFF = _diff_of(
    _edited(
        ("line 03", "line 03 CHANGED"),
        ("line 15", "line 15 CHANGED"),
        ("line 27", "line 27 CHANGED"),
    ),
    "f.txt",
)

HUNK_IDS = [h["id"] for h in parse_unified_diff_to_view(THREE_HUNK_DIFF)["files"][0]["hunks"]]
assert len(HUNK_IDS) == 3, f"the fixture must carry three hunks, not {len(HUNK_IDS)}"


@pytest.fixture
def isolated(tmp_path, monkeypatch) -> Path:
    """An isolated data root AND a CWD outside this repository — without the chdir the
    `remedy-job-evidence-<job_id>` fallback would resolve against the real working tree."""
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    monkeypatch.chdir(tmp_path)
    return root


def _job(job_id: UUID | None = None) -> Job:
    job = Job(id=job_id or uuid4(), name="hunk decision job",
              metadata={"unrelated": "kept"})
    save_job(job)
    return job


def _index(job: Job, evidence_dir: Path) -> None:
    index_dir = job_evidence_index_dir()
    index_dir.mkdir(parents=True, exist_ok=True)
    (index_dir / f"{job.id}.json").write_text(
        json.dumps({"job_id": str(job.id), "evidence_dir_local": str(evidence_dir)}),
        encoding="utf-8",
    )


def _evidence(tmp_path: Path, job: Job, *, task_run: str | None = None) -> Path:
    """An evidence directory carrying the job-level diff, and optionally one task run's."""
    evidence_dir = tmp_path / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / DIFF_JOB_ARTIFACT_NAME).write_text(THREE_HUNK_DIFF, encoding="utf-8")
    if task_run is not None:
        run_dir = evidence_dir / DIFF_TASK_RUNS_DIR_NAME / task_run
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / DIFF_TASK_RUN_ARTIFACT_NAME).write_text(THREE_HUNK_DIFF, encoding="utf-8")
    _index(job, evidence_dir)
    return evidence_dir


class TestItIsWiredIntoTheCli:
    def test_the_command_id_resolves_in_the_catalog(self):
        entry = get_command("patch.approve-hunks")
        assert entry.group_id == "patch" and entry.subcommand == "approve-hunks"
        assert entry.supports_json is True
        assert not entry.may_mutate_repo and not entry.requires_permission

    def test_the_handler_is_registered(self):
        """The discriminator for `Error: no handler for patch.approve-hunks` — a catalog
        entry whose handler never landed dispatches to that message and nothing else."""
        assert "patch.approve-hunks" in collect_all_handlers()


class TestTheHappyPath:
    def test_a_mixed_decision_lands_under_the_envelope_derived_attempt_key(
        self, isolated, tmp_path, capsys,
    ):
        """Both halves of the key come from the ENVELOPE: `task_id` is `job` for the
        job-level scope and `attempt` is the artifact-relative `source`."""
        job = _job()
        _evidence(tmp_path, job)

        CMD._cmd_approve_hunks(
            str(job.id),
            approve=[HUNK_IDS[0]],
            reject=[f"{HUNK_IDS[1]}={REASON}"],
        )

        reloaded = load_job(job.id)
        records = reloaded.metadata[HUNK_DECISIONS_METADATA_KEY]
        assert list(records) == [f"job:{DIFF_JOB_ARTIFACT_NAME}"]
        record = records[f"job:{DIFF_JOB_ARTIFACT_NAME}"]
        assert record["task_id"] == "job" and record["attempt"] == DIFF_JOB_ARTIFACT_NAME
        assert [row["state"] for row in record["hunks"]] == [
            "approved", "rejected", "pending"]
        assert reloaded.metadata["unrelated"] == "kept"

        out = capsys.readouterr().out
        assert f"Recorded: job:{DIFF_JOB_ARTIFACT_NAME}" in out
        assert "approved: 1" in out and "rejected: 1" in out and "pending: 1" in out
        assert "no files have been modified" in out

    def test_a_rejection_reason_survives_verbatim(self, isolated, tmp_path, capsys):
        """The split is on the FIRST `=`, so a reason carrying its own `=` arrives whole,
        and neither half is stripped."""
        job = _job()
        _evidence(tmp_path, job)

        CMD._cmd_approve_hunks(str(job.id), reject=[f"{HUNK_IDS[0]}={REASON}"])
        capsys.readouterr()

        record = load_job(job.id).metadata[HUNK_DECISIONS_METADATA_KEY][
            f"job:{DIFF_JOB_ARTIFACT_NAME}"]
        rejected = [row for row in record["hunks"] if row["state"] == "rejected"]
        assert [row["id"] for row in rejected] == [HUNK_IDS[0]]
        assert rejected[0]["reason"] == REASON

    def test_a_task_run_scope_keys_on_that_runs_own_artifact(
        self, isolated, tmp_path, capsys,
    ):
        """`--task-run` is passed through UNCHANGED, so the envelope names the task run's
        artifact and the record lands under a key distinct from the job-level one."""
        job = _job()
        _evidence(tmp_path, job, task_run="T001")

        CMD._cmd_approve_hunks(str(job.id), task_run="T001", approve=[HUNK_IDS[0]])
        capsys.readouterr()

        expected = f"T001:{DIFF_TASK_RUNS_DIR_NAME}/T001/{DIFF_TASK_RUN_ARTIFACT_NAME}"
        records = load_job(job.id).metadata[HUNK_DECISIONS_METADATA_KEY]
        assert list(records) == [expected]
        assert records[expected]["task_id"] == "T001"

    def test_json_output_is_the_exported_record(self, isolated, tmp_path, capsys):
        job = _job()
        _evidence(tmp_path, job)

        CMD._cmd_approve_hunks(str(job.id), approve=[HUNK_IDS[0]], json_output=True)

        payload = json.loads(capsys.readouterr().out)
        assert payload["task_id"] == "job"
        assert payload["attempt"] == DIFF_JOB_ARTIFACT_NAME
        assert payload["decided_at"]
        assert [row["id"] for row in payload["hunks"]] == HUNK_IDS
        assert payload == load_job(job.id).metadata[HUNK_DECISIONS_METADATA_KEY][
            f"job:{DIFF_JOB_ARTIFACT_NAME}"]


class TestItMintsNoRefusalVocabularyOfItsOwn:
    def test_a_reject_value_with_no_equals_is_the_cores_missing_reason(
        self, isolated, tmp_path, capsys,
    ):
        """The value is passed on UNCHANGED, so the fault is named once, by
        `decide_hunk_approval`, and not a second time by this handler."""
        job = _job()
        _evidence(tmp_path, job)

        with pytest.raises(SystemExit) as exc:
            CMD._cmd_approve_hunks(
                str(job.id), reject=[HUNK_IDS[0]], json_output=True)

        assert exc.value.code == 1
        payload = json.loads(capsys.readouterr().out)
        assert payload["code"] == REFUSAL_MISSING_REASON
        assert payload["hunk_ids"] == [HUNK_IDS[0]]
        assert HUNK_DECISIONS_METADATA_KEY not in load_job(job.id).metadata

    def test_an_unresolvable_evidence_directory_is_no_diff_available(
        self, isolated, tmp_path, capsys,
    ):
        """No index record and no CWD-relative directory: the envelope reports the
        directory missing and the recorder refuses over it, writing NOTHING."""
        job = _job()

        with pytest.raises(SystemExit) as exc:
            CMD._cmd_approve_hunks(
                str(job.id), approve=[HUNK_IDS[0]], json_output=True)

        assert exc.value.code == 1
        payload = json.loads(capsys.readouterr().out)
        assert payload["code"] == HUNK_RECORD_REFUSAL_NO_DIFF
        assert DIFF_REASON_NO_EVIDENCE_DIR in payload["message"]
        assert HUNK_DECISIONS_METADATA_KEY not in load_job(job.id).metadata

    def test_a_refusal_never_persists_the_job(self, isolated, tmp_path, monkeypatch, capsys):
        """THE DISCRIMINATOR for "a refused decision is not a decision": the record on disk
        is unchanged either way, so only watching `save_job` itself witnesses the claim."""
        job = _job()
        _evidence(tmp_path, job)
        calls: list[object] = []
        monkeypatch.setattr(CMD, "save_job", lambda saved: calls.append(saved))

        with pytest.raises(SystemExit):
            CMD._cmd_approve_hunks(str(job.id), reject=[HUNK_IDS[0]])

        assert calls == []
        assert "Error:" in capsys.readouterr().err

    def test_a_human_refusal_goes_to_stderr_with_the_offending_ids(
        self, isolated, tmp_path, capsys,
    ):
        job = _job()
        _evidence(tmp_path, job)

        with pytest.raises(SystemExit) as exc:
            CMD._cmd_approve_hunks(str(job.id), approve=["not-a-hunk-id"])

        assert exc.value.code == 1
        err = capsys.readouterr().err
        assert err.startswith("Error: ")
        assert "not-a-hunk-id" in err

    def test_an_unknown_job_id_exits_1(self, isolated, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_approve_hunks(str(uuid4()), approve=["h1"])

        assert exc.value.code == 1
        assert "Error:" in capsys.readouterr().err


class TestTheEvidenceDirectoryComesFromTheRESOLVEDJobId:
    """Finding R-0744, as the two forms `resolve_job_id` exists to accept.

    The index is keyed by the CANONICAL lowercase hyphenated id, so a handler that hands
    `resolve_job_evidence_dir` the operator's RAW argument reports `no_diff_available` for
    a diff sitting in the directory the index names — the misreport
    `HUNK_RECORD_REFUSAL_NO_DIFF` was minted to prevent, arriving through the id instead of
    through the artifact. The eleven tests above are BLIND to it: every one of them names
    its job by the canonical form, where raw and resolved are the same string.

    Each test below therefore asserts the RECORDED state rather than the exit code. A
    handler that merely exited 0 while recording under another key would pass an
    exit-code test and still have lost the operator's decision.
    """

    #: A job id carrying hex LETTERS, so its uppercase form is really a different string.
    #: Fixed rather than drawn from `uuid4`, which can in principle mint an all-digit id.
    CASED_JOB_ID = UUID("0a1b2c3d-4e5f-4a6b-8c7d-9e0f1a2b3c4d")

    def _premise(self, tmp_path, job) -> None:
        """The evidence directory really resolves under the job's FULL canonical id —
        the premise that makes naming the job the OTHER way a test of the resolution."""
        evidence_dir = _evidence(tmp_path, job)
        assert resolve_job_evidence_dir(str(job.id)) == evidence_dir

    def _decided(self, job) -> dict:
        """The record as it is ON DISK, so `save_job` is part of what is asserted."""
        records = load_job(job.id).metadata[HUNK_DECISIONS_METADATA_KEY]
        assert list(records) == [f"job:{DIFF_JOB_ARTIFACT_NAME}"]
        return records[f"job:{DIFF_JOB_ARTIFACT_NAME}"]

    def test_a_short_hex_prefix_records_exactly_as_the_full_id_does(
        self, isolated, tmp_path, capsys,
    ):
        """The prefix form is why `resolve_job_id` exists, and it must reach the index."""
        job = _job()
        self._premise(tmp_path, job)
        prefix = job.id.hex[:8]
        assert resolve_job_id(prefix) == job.id, "the fixture's prefix must name THIS job"

        CMD._cmd_approve_hunks(
            prefix, approve=[HUNK_IDS[0]], reject=[f"{HUNK_IDS[1]}={REASON}"])

        record = self._decided(job)
        assert record["task_id"] == "job" and record["attempt"] == DIFF_JOB_ARTIFACT_NAME
        assert [row["state"] for row in record["hunks"]] == [
            "approved", "rejected", "pending"]
        assert "no_diff_available" not in capsys.readouterr().err

    def test_an_uppercase_uuid_records_exactly_as_the_lowercase_one_does(
        self, isolated, tmp_path, capsys,
    ):
        """`UUID` normalises case, the index file does not — so only the RESOLVED id finds it."""
        job = _job(self.CASED_JOB_ID)
        self._premise(tmp_path, job)
        shouted = str(job.id).upper()
        assert shouted != str(job.id), "the fixture must really change case"
        assert resolve_job_id(shouted) == job.id

        CMD._cmd_approve_hunks(shouted, approve=[HUNK_IDS[0]])

        record = self._decided(job)
        assert [row["state"] for row in record["hunks"]] == [
            "approved", "pending", "pending"]
        assert "no_diff_available" not in capsys.readouterr().err
