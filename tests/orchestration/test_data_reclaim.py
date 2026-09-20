"""`remedy data reclaim` — the preview, the apply, and every refusal (F276 T002).

Every fixture writes a REAL job record through ``save_job_plan``, so the terminal
check these tests exercise is the one production reads, not a stub of it. No test
touches the operator's data root: each builds its own tree under ``tmp_path`` and
points ``REMEDY_DATA_DIR`` at it.
"""
from __future__ import annotations

import json
import os

import pytest

from apps.cli.grouped import main
from packages.core.models import RunState
from packages.orchestration.data_reclaim import (
    ReclaimCandidate,
    ReclaimPlan,
    apply_reclaim,
    plan_reclaim,
)
from packages.orchestration.pingpong_job import JobPlan, save_job_plan


def _job(root, state: RunState) -> str:
    """One persisted job record under ``root``, in ``state``; returns its id."""
    from packages.orchestration.data_paths import mint_job_id

    job_id = mint_job_id()
    save_job_plan(JobPlan(job_id=job_id, repo_path=str(root), state=state), root)
    return job_id


def _scratch(root, data_class: str, name: str, payload: bytes = b"x" * 64):
    """One direct child of a class directory, holding one file."""
    d = root / data_class / name
    d.mkdir(parents=True)
    (d / "big.bin").write_bytes(payload)
    return d


def _tree(root) -> set[str]:
    """Every path under ``root``, relative and sorted — the before/after measurement."""
    out = set()
    for dirpath, dirnames, filenames in os.walk(root):
        for n in list(dirnames) + list(filenames):
            out.add(os.path.relpath(os.path.join(dirpath, n), root))
    return out


@pytest.fixture()
def root(tmp_path, monkeypatch):
    r = tmp_path / "data"
    r.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(r))
    return r


def test_preview_deletes_nothing(root, capsys):
    done = _job(root, RunState.COMPLETED)
    _scratch(root, "job_workspaces", f"staging_{done}")
    before = _tree(root)

    main(["data", "reclaim"])

    assert _tree(root) == before
    out = capsys.readouterr().out
    assert f"job_workspaces/staging_{done}" in out
    assert "nothing deleted" in out


def test_apply_deletes_exactly_the_previewed_paths(root, capsys):
    done = _job(root, RunState.COMPLETED)
    live = _job(root, RunState.RUNNING)
    doomed = _scratch(root, "job_workspaces", f"staging_{done}")
    kept = _scratch(root, "job_workspaces", f"staging_{live}")

    main(["data", "reclaim", "--json"])
    previewed = {c["path"] for c in json.loads(capsys.readouterr().out)["candidates"]}
    assert previewed == {str(doomed)}

    before = _tree(root)
    main(["data", "reclaim", "--apply", "--json"])
    body = json.loads(capsys.readouterr().out)

    assert body["removed"] == [str(doomed)]
    assert not doomed.exists()
    assert kept.exists()
    # Nothing but the previewed subtree left the tree.
    gone = before - _tree(root)
    assert gone == {
        os.path.relpath(doomed, root),
        os.path.join(os.path.relpath(doomed, root), "big.bin"),
    }


def test_a_second_apply_over_the_same_state_removes_nothing_and_exits_zero(root, capsys):
    done = _job(root, RunState.COMPLETED)
    _scratch(root, "job_workspaces", f"staging_{done}")

    main(["data", "reclaim", "--apply", "--json"])
    assert len(json.loads(capsys.readouterr().out)["removed"]) == 1

    after_first = _tree(root)
    main(["data", "reclaim", "--apply", "--json"])   # exits 0 by not raising SystemExit
    body = json.loads(capsys.readouterr().out)

    assert body["removed"] == []
    assert body["freed"]["bytes"] == 0
    assert _tree(root) == after_first


@pytest.mark.parametrize("state", [
    RunState.RUNNING, RunState.PLANNED, RunState.PAUSED,
    RunState.BLOCKED, RunState.STOPPED, RunState.PENDING,
])
def test_a_non_terminal_job_workspace_is_refused_and_named(root, capsys, state):
    live = _job(root, state)
    ws = _scratch(root, "job_workspaces", f"staging_{live}")

    main(["data", "reclaim", "--apply", "--json"])
    body = json.loads(capsys.readouterr().out)

    assert body["candidates"] == []
    refused = [r for r in body["refused"] if r["path"] == str(ws)]
    assert len(refused) == 1
    assert refused[0]["reason"] == "job_not_terminal"
    assert refused[0]["name"] == f"staging_{live}"
    assert state.value in refused[0]["detail"]
    assert ws.exists()


def test_a_staging_copy_whose_job_has_no_record_is_refused_not_skipped(root, capsys):
    orphan = _scratch(root, "job_workspaces", "staging_0123456789abcdef")

    main(["data", "reclaim", "--apply", "--json"])
    body = json.loads(capsys.readouterr().out)

    refused = [r for r in body["refused"] if r["path"] == str(orphan)]
    assert len(refused) == 1
    assert refused[0]["reason"] == "job_unresolved"
    assert orphan.exists()


def test_a_path_that_is_not_a_direct_child_is_refused(root):
    done = _job(root, RunState.COMPLETED)
    ws = _scratch(root, "job_workspaces", f"staging_{done}")
    nested = ws / "nested"
    nested.mkdir()
    (nested / "f.bin").write_bytes(b"y" * 8)

    forged = ReclaimPlan(
        root=str(root), exists=True, refusals=(), unreclaimed=(),
        candidates=(ReclaimCandidate(
            data_class="job_workspaces", name="nested", path=str(nested),
            job_id=done, job_state="completed", age_days=0.0, bytes=8, files=1,
        ),),
    )
    outcome = apply_reclaim(forged)

    assert outcome.removed == ()
    assert [r.reason for r in outcome.refusals] == ["not_a_direct_child"]
    assert nested.exists()


def test_a_durable_child_and_an_unclassified_child_are_never_deleted(root, capsys):
    done = _job(root, RunState.COMPLETED)
    _scratch(root, "job_workspaces", f"staging_{done}")
    (root / "missions" / "p").mkdir(parents=True)
    (root / "missions" / "p" / "m.json").write_bytes(b"{}")
    (root / "task_jobs").mkdir()
    (root / "task_jobs" / "legacy.bin").write_bytes(b"z" * 32)

    main(["data", "reclaim", "--apply", "--json"])
    body = json.loads(capsys.readouterr().out)

    assert (root / "missions" / "p" / "m.json").exists()
    assert (root / "task_jobs" / "legacy.bin").exists()
    not_reclaimed = {u["name"]: u["class"] for u in body["not_reclaimed"]}
    assert not_reclaimed["missions"] == "durable"
    assert not_reclaimed["task_jobs"] == "unclassified"
    assert not_reclaimed["jobs"] == "durable"
    assert all(c["class"] == "job_workspaces" for c in body["candidates"])


#: DECISION F276 D3's three moves, with the child each class holds for one job and
#: the evidence inside it that outlives that job. One case per moved class, because a
#: single case would leave the other two flips green — which is exactly what the
#: registry's partition test cannot see.
_DURABLE_MOVES = [
    ("workspaces", lambda job: job, "apply_records/record.json"),
    ("runs", lambda job: "runid" + job[:11], "result.json"),
    ("job_logs", lambda job: job, "events.jsonl"),
]


@pytest.mark.parametrize("data_class,child_of,evidence", _DURABLE_MOVES,
                         ids=[m[0] for m in _DURABLE_MOVES])
def test_a_terminal_jobs_durable_child_survives_an_apply(
    root, capsys, data_class, child_of, evidence,
):
    """DECISION F276 D3: each of these mixes scratch with evidence, so it is DURABLE.

    The job is COMPLETED and the child is a direct child of a class directory, so
    EVERY other rule would make it a candidate. It is not one solely because the
    registry files its class as durable — which makes this the guard for D3.
    """
    from packages.orchestration.data_paths import classify_data_child

    done = _job(root, RunState.COMPLETED)
    child = _scratch(root, data_class, child_of(done))
    proof = child / evidence
    proof.parent.mkdir(parents=True, exist_ok=True)
    proof.write_bytes(b'{"kept":1}\n')
    doomed = _scratch(root, "job_workspaces", f"staging_{done}")

    main(["data", "reclaim", "--apply", "--json"])
    body = json.loads(capsys.readouterr().out)

    assert classify_data_child(data_class) == "durable"
    assert [c["path"] for c in body["candidates"]] == [str(doomed)]
    assert data_class not in {c["class"] for c in body["candidates"]}
    assert data_class not in {r["class"] for r in body["refused"]}
    assert {u["name"]: u["class"] for u in body["not_reclaimed"]}[data_class] == "durable"
    assert proof.exists()
    assert not doomed.exists()


def test_job_workspaces_is_the_only_class_with_candidates(root):
    """Reclaim v1 addresses one class; the registry is where that is decided."""
    from packages.orchestration.data_paths import EPHEMERAL_CLASSES

    assert {c.name for c in EPHEMERAL_CLASSES} == {"job_workspaces", "review_staging"}
    assert {c.name for c in EPHEMERAL_CLASSES if not c.prefix} == {"job_workspaces"}


def test_ordinary_refusals_exit_zero(root, capsys):
    """A refusal the operator asked for is a report, not a failure."""
    live = _job(root, RunState.RUNNING)
    _scratch(root, "job_workspaces", f"staging_{live}")

    main(["data", "reclaim", "--apply", "--json"])   # no SystemExit == exit 0

    body = json.loads(capsys.readouterr().out)
    assert [r["reason"] for r in body["refused"]] == ["job_not_terminal"]


def test_a_deletion_that_is_attempted_and_fails_exits_one(root, capsys):
    """A real failure, not a patched exception: the class dir is made unwritable.

    ``rmtree`` needs write permission on the PARENT to unlink the candidate's entry,
    so a read-and-execute-only ``job_workspaces/`` makes the deletion fail for real
    while leaving the plan's own scandir and lstat working.
    """
    if os.geteuid() == 0:
        pytest.skip("root ignores the directory mode this failure is built from")

    done = _job(root, RunState.COMPLETED)
    ws = _scratch(root, "job_workspaces", f"staging_{done}")
    class_dir = root / "job_workspaces"
    os.chmod(class_dir, 0o500)
    try:
        with pytest.raises(SystemExit) as exc:
            main(["data", "reclaim", "--apply", "--json"])
        body = json.loads(capsys.readouterr().out)
    finally:
        os.chmod(class_dir, 0o700)

    assert exc.value.code == 1
    assert body["removed"] == []
    assert [r["reason"] for r in body["refused"]] == ["delete_failed"]
    assert body["refused"][0]["path"] == str(ws)
    # The candidate survives, but NOT untouched: ``rmtree`` is not atomic, so it
    # unlinked what it could before the parent's mode stopped it. That is exactly why
    # the exit code is 1 — a half-removed candidate is not a state to report quietly.
    assert ws.exists()
    assert not (ws / "big.bin").exists()


def test_a_symlinked_candidate_is_refused_and_its_target_survives(root, tmp_path, capsys):
    done = _job(root, RunState.COMPLETED)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "precious.bin").write_bytes(b"k" * 128)
    (root / "job_workspaces").mkdir()
    link = root / "job_workspaces" / f"staging_{done}"
    link.symlink_to(outside, target_is_directory=True)

    main(["data", "reclaim", "--apply", "--json"])
    body = json.loads(capsys.readouterr().out)

    assert body["candidates"] == []
    assert [r["reason"] for r in body["refused"]] == ["symlink"]
    assert link.is_symlink()
    assert (outside / "precious.bin").exists()


def test_the_json_shape(root, capsys):
    done = _job(root, RunState.COMPLETED)
    ws = _scratch(root, "job_workspaces", f"staging_{done}")
    (root / "review_staging.AbC123").mkdir()

    main(["data", "reclaim", "--json"])
    body = json.loads(capsys.readouterr().out)

    assert set(body) == {
        "version", "root", "exists", "applied", "candidates",
        "refused", "not_reclaimed", "total", "removed", "freed",
    }
    assert body["version"] == 1
    assert body["root"] == str(root)
    assert body["exists"] is True
    assert body["applied"] is False
    assert body["removed"] == []
    assert body["freed"] == {"bytes": 0, "paths": 0}
    assert body["total"] == {"candidates": 1, "bytes": 64, "files": 1, "refused": 1}
    assert set(body["candidates"][0]) == {
        "class", "name", "path", "job_id", "job_state", "age_days", "bytes", "files",
    }
    assert body["candidates"][0]["class"] == "job_workspaces"
    assert body["candidates"][0]["path"] == str(ws)
    assert body["candidates"][0]["job_id"] == done
    assert body["candidates"][0]["job_state"] == "completed"
    assert body["candidates"][0]["bytes"] == 64
    assert set(body["refused"][0]) == {
        "class", "name", "path", "reason", "detail", "bytes", "files",
    }
    assert body["refused"][0]["reason"] == "class_not_job_keyed"
    assert body["refused"][0]["name"] == "review_staging.AbC123"


def test_a_candidates_job_id_is_read_from_its_name_and_no_file(root):
    """The id is in the child's NAME, so a listing plus one job record decides it.

    A directory under the one job-keyed class whose name does not carry the prefix
    yields no id at all, and is refused rather than guessed at.
    """
    done = _job(root, RunState.COMPLETED)
    named = _scratch(root, "job_workspaces", f"staging_{done}")
    unprefixed = _scratch(root, "job_workspaces", done)

    plan = plan_reclaim(root)

    assert [(c.path, c.job_id) for c in plan.candidates] == [(str(named), done)]
    assert [(r.name, r.reason) for r in plan.refusals] == [(done, "job_unresolved")]
    assert unprefixed.exists()


def test_plan_reclaim_writes_nothing_and_a_missing_root_is_not_an_error(tmp_path):
    absent = tmp_path / "absent"
    plan = plan_reclaim(absent)

    assert plan.exists is False
    assert plan.candidates == ()
    assert not absent.exists()
