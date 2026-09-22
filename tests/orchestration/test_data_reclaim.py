"""`remedy data reclaim` — the preview, the apply, and every refusal (F276 T002).

Every fixture writes a REAL job record through ``save_job_plan``, so the terminal
check these tests exercise is the one production reads, not a stub of it. No test
touches the operator's data root: each builds its own tree under ``tmp_path`` and
points ``REMEDY_DATA_DIR`` at it.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import time

import pytest

from apps.cli.grouped import main
from packages.core.models import RunState
from packages.orchestration.data_reclaim import (
    REFUSAL_REASONS,
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


def _backdate(path, days: float) -> None:
    """Move one path's own mtime ``days`` into the past — the orphan floor's input."""
    when = time.time() - days * 86400.0
    os.utime(path, (when, when))


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
        "schema_version", "ok",
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


# ── The orphan rule: `--orphans` ─────────────────────────────────────────────
#
# WHY IT EXISTS, measured on the operator's real data root with the command round 2
# built: `remedy data reclaim --json` read 1107 candidates worth 284 536 286 695 bytes
# against 1886 refusals, of which 1885 were `job_unresolved` worth 638 395 396 948
# bytes — and 1884 of those were `staging_<16-hex>` names with no job record on disk at
# all (`.data/jobs/000bf7ccd9cb49f8` does not exist and `job show` answers "No job
# matches"). 69 per cent of the reclaimable footprint was refused, and the feature
# file's OPERATOR STEP expects `.data` under 10 GB after a reclaim, which cannot happen
# while it stays refused.
#
# Every fixture below seeds a REAL job record wherever a record is meant to exist, so
# the "no record" these tests exercise is a real absence and not a patched lookup.

#: A 16-hex id no `_job` ever minted, so no record for it can exist by accident.
_ORPHAN_ID = "0123456789abcdef"


def test_without_the_flag_the_json_is_byte_for_byte_what_it_was(root, capsys):
    """DEFAULT OFF, pinned on the SERIALISED document rather than a parsed subset.

    The expected body is built in full here and dumped the way the command dumps it,
    so this compares STRINGS: a key the orphan rule added, a candidate it widened
    into, a total it moved — any of them reds this test. The seeded root deliberately
    holds an old orphan, so the widening this pins is one the flag really performs.
    """
    from packages.orchestration.data_footprint import child_usage

    done = _job(root, RunState.COMPLETED)
    live = _job(root, RunState.RUNNING)
    kept = _scratch(root, "job_workspaces", f"staging_{done}")
    running = _scratch(root, "job_workspaces", f"staging_{live}")
    orphan = _scratch(root, "job_workspaces", f"staging_{_ORPHAN_ID}")
    _backdate(orphan, 400)
    jobs_bytes, jobs_files = child_usage(str(root / "jobs"))

    main(["data", "reclaim", "--json"])
    out = capsys.readouterr().out

    expected = {
        "version": 1, "root": str(root), "exists": True, "applied": False,
        "candidates": [{
            "class": "job_workspaces", "name": f"staging_{done}", "path": str(kept),
            "job_id": done, "job_state": "completed", "age_days": 0.0,
            "bytes": 64, "files": 1,
        }],
        # Both refusals come from the one class directory, whose children are walked
        # in NAME order, so the expected list is sorted the same way.
        "refused": sorted([
            {"class": "job_workspaces", "name": f"staging_{_ORPHAN_ID}",
             "path": str(orphan), "reason": "job_unresolved",
             "detail": f"no readable job record for {_ORPHAN_ID}",
             "bytes": 64, "files": 1},
            {"class": "job_workspaces", "name": f"staging_{live}", "path": str(running),
             "reason": "job_not_terminal", "detail": f"job {live} is running, not terminal",
             "bytes": 64, "files": 1},
        ], key=lambda r: r["name"]),
        "not_reclaimed": [
            {"name": "jobs", "class": "durable", "bytes": jobs_bytes, "files": jobs_files},
        ],
        "total": {"candidates": 1, "bytes": 64, "files": 1, "refused": 2},
        "removed": [], "freed": {"bytes": 0, "paths": 0},
        "schema_version": 1, "ok": True,
    }
    assert out == json.dumps(expected, sort_keys=True) + "\n"


def test_an_old_orphan_becomes_a_candidate_only_with_the_flag(root, capsys):
    orphan = _scratch(root, "job_workspaces", f"staging_{_ORPHAN_ID}")
    _backdate(orphan, 30)

    main(["data", "reclaim", "--json"])
    without = json.loads(capsys.readouterr().out)
    main(["data", "reclaim", "--orphans", "--json"])
    with_flag = json.loads(capsys.readouterr().out)

    assert without["candidates"] == []
    assert [r["reason"] for r in without["refused"]] == ["job_unresolved"]
    assert [c["path"] for c in with_flag["candidates"]] == [str(orphan)]
    assert with_flag["candidates"][0]["job_id"] == _ORPHAN_ID
    assert with_flag["candidates"][0]["job_state"] == "no_record"
    assert with_flag["refused"] == []
    assert orphan.exists()          # both of those were PREVIEWS


def test_a_young_orphan_is_refused_as_orphan_too_young_even_with_the_flag(root, capsys):
    """The floor is the insurance for a record that is being written RIGHT NOW.

    Under it the child is refused rather than skipped, under its own reason, so an
    operator reading the report can see the path and why it was kept.
    """
    young = _scratch(root, "job_workspaces", f"staging_{_ORPHAN_ID}")
    _backdate(young, 0.5)

    main(["data", "reclaim", "--orphans", "--apply", "--json"])
    body = json.loads(capsys.readouterr().out)

    assert body["candidates"] == []
    assert [r["reason"] for r in body["refused"]] == ["orphan_too_young"]
    assert body["refused"][0]["detail"] == (
        "no job record, and 0.50d is under the 1.0d orphan floor")
    assert "orphan_too_young" in REFUSAL_REASONS
    assert young.exists()


def test_a_child_without_the_staging_prefix_is_never_an_orphan(root, capsys):
    """The prefix is what says "a job's staging copy lives here".

    Without it no job id is read at all, so there is no record to be missing, and
    `--orphans` must not widen to it however old it is.
    """
    stray = _scratch(root, "job_workspaces", _ORPHAN_ID)
    _backdate(stray, 400)

    main(["data", "reclaim", "--orphans", "--apply", "--json"])
    body = json.loads(capsys.readouterr().out)

    assert body["candidates"] == []
    assert [(r["name"], r["reason"]) for r in body["refused"]] == [
        (_ORPHAN_ID, "job_unresolved")]
    assert body["refused"][0]["detail"] == "no job id can be read from this path"
    assert stray.exists()


def test_a_live_jobs_staging_copy_is_never_an_orphan(root, capsys):
    """Its record EXISTS and is not terminal, so the orphan branch is never reached."""
    live = _job(root, RunState.RUNNING)
    ws = _scratch(root, "job_workspaces", f"staging_{live}")
    _backdate(ws, 400)

    main(["data", "reclaim", "--orphans", "--apply", "--json"])
    body = json.loads(capsys.readouterr().out)

    assert body["candidates"] == []
    assert [r["reason"] for r in body["refused"]] == ["job_not_terminal"]
    assert ws.exists()


def test_a_record_that_exists_but_cannot_be_read_is_never_an_orphan(root, capsys):
    """An orphan's signature is NO RECORD, not an unreadable one.

    A record that exists and will not parse belongs to a job that may still be
    running; `load_job_plan_safe`'s ``degraded`` flag is the only thing that tells the
    two apart, and both spell the same `job_unresolved` refusal without it.
    """
    from packages.orchestration.data_paths import job_record_path

    live = _job(root, RunState.RUNNING)
    job_record_path(live, root).write_text("{ not json at all")
    ws = _scratch(root, "job_workspaces", f"staging_{live}")
    _backdate(ws, 400)

    main(["data", "reclaim", "--orphans", "--apply", "--json"])
    body = json.loads(capsys.readouterr().out)

    assert body["candidates"] == []
    assert [r["reason"] for r in body["refused"]] == ["job_unresolved"]
    assert ws.exists()


def test_orphans_without_apply_deletes_nothing_and_names_both_totals(root, capsys):
    done = _job(root, RunState.COMPLETED)
    _scratch(root, "job_workspaces", f"staging_{done}")
    orphan = _scratch(root, "job_workspaces", f"staging_{_ORPHAN_ID}")
    _backdate(orphan, 30)
    before = _tree(root)

    main(["data", "reclaim", "--orphans"])

    assert _tree(root) == before
    out = capsys.readouterr().out
    assert "nothing deleted" in out
    # The operator sees the two numbers SEPARATELY before deciding.
    assert re.search(r"orphans \(no job record\):\s+1 paths\s+64 B", out)
    assert re.search(r"terminal jobs:\s+1 paths\s+64 B", out)


def test_orphans_apply_deletes_exactly_the_previewed_orphans_and_a_second_run_is_a_noop(
    root, capsys,
):
    done = _job(root, RunState.COMPLETED)
    live = _job(root, RunState.RUNNING)
    ordinary = _scratch(root, "job_workspaces", f"staging_{done}")
    running = _scratch(root, "job_workspaces", f"staging_{live}")
    old = _scratch(root, "job_workspaces", "staging_00000000deadbeef")
    young = _scratch(root, "job_workspaces", "staging_11111111feedface")
    _backdate(old, 30)
    _backdate(young, 0.25)

    main(["data", "reclaim", "--orphans", "--json"])
    previewed = {c["path"] for c in json.loads(capsys.readouterr().out)["candidates"]}
    assert previewed == {str(ordinary), str(old)}

    main(["data", "reclaim", "--orphans", "--apply", "--json"])
    body = json.loads(capsys.readouterr().out)

    assert set(body["removed"]) == previewed
    assert body["freed"] == {"bytes": 128, "paths": 2}
    assert not old.exists()
    assert not ordinary.exists()
    assert running.exists()
    assert young.exists()
    after = _tree(root)

    main(["data", "reclaim", "--orphans", "--apply", "--json"])
    second = json.loads(capsys.readouterr().out)

    assert second["removed"] == []
    assert second["freed"]["bytes"] == 0
    assert _tree(root) == after


def test_the_orphan_json_shape(root, capsys):
    """An orphan adds no key: `job_state` is the ONE mark, and it cannot collide."""
    done = _job(root, RunState.COMPLETED)
    _scratch(root, "job_workspaces", f"staging_{done}")
    old = _scratch(root, "job_workspaces", "staging_00000000deadbeef")
    young = _scratch(root, "job_workspaces", "staging_11111111feedface")
    _backdate(old, 3)
    _backdate(young, 0.25)

    main(["data", "reclaim", "--orphans", "--json"])
    body = json.loads(capsys.readouterr().out)

    assert set(body) == {
        "version", "root", "exists", "applied", "candidates",
        "refused", "not_reclaimed", "total", "removed", "freed",
        "schema_version", "ok",
    }
    by_state = {c["job_state"]: c for c in body["candidates"]}
    assert set(by_state) == {"completed", "no_record"}
    assert set(by_state["no_record"]) == set(by_state["completed"]) == {
        "class", "name", "path", "job_id", "job_state", "age_days", "bytes", "files",
    }
    assert by_state["no_record"]["path"] == str(old)
    assert by_state["no_record"]["job_id"] == "00000000deadbeef"
    assert by_state["no_record"]["age_days"] == 3.0
    # The mark is a reserved token: no RunState is spelled this way, so a reader
    # matching it exactly can never mistake an ordinary candidate for an orphan.
    assert "no_record" not in {s.value for s in RunState}
    assert [(r["name"], r["reason"]) for r in body["refused"]] == [
        ("staging_11111111feedface", "orphan_too_young")]
    assert body["total"] == {"candidates": 2, "bytes": 128, "files": 2, "refused": 1}


def test_the_default_human_preview_names_the_unresolved_bytes_and_the_flag(root, capsys):
    """DISCOVERABILITY: the flag is named where the bytes it would reclaim are printed.

    An operator staring at a `job_unresolved` refusal must not have to read the source
    to learn `--orphans` exists. The line is on the HUMAN default path ONLY, and the
    three readings below are the three states it has to get right.
    """
    done = _job(root, RunState.COMPLETED)
    _scratch(root, "job_workspaces", f"staging_{done}")
    _backdate(_scratch(root, "job_workspaces", f"staging_{_ORPHAN_ID}"), 30)
    _backdate(_scratch(root, "job_workspaces", "staging_00000000deadbeef"), 30)

    main(["data", "reclaim"])
    default = capsys.readouterr().out
    main(["data", "reclaim", "--orphans"])
    with_flag = capsys.readouterr().out

    # 1. the DEFAULT names the count, the bytes and the flag
    assert re.search(r"2 of those are job_unresolved \(128 B\) — re-run with --orphans",
                     default)
    # 2. typing the flag answers the question, so the hint is gone
    assert "re-run with --orphans" not in with_flag
    # 3. no `job_unresolved` refusal, no hint — it is an answer, never decoration
    capsys.readouterr()
    for path in root.glob("job_workspaces/staging_*"):
        if path.name != f"staging_{done}":
            shutil.rmtree(path)
    main(["data", "reclaim"])
    assert "re-run with --orphans" not in capsys.readouterr().out


def test_the_default_json_carries_no_hint_and_the_human_line_is_not_in_it(root, capsys):
    """The hint is a HUMAN line: the machine document is untouched by it.

    `test_without_the_flag_the_json_is_byte_for_byte_what_it_was` already pins the whole
    default document; this names the reason that test still passes after the hint
    landed, on a root that definitely triggers the hint.
    """
    _backdate(_scratch(root, "job_workspaces", f"staging_{_ORPHAN_ID}"), 30)

    main(["data", "reclaim", "--json"])
    out = capsys.readouterr().out

    assert "--orphans" not in out
    assert set(json.loads(out)) == {
        "version", "root", "exists", "applied", "candidates",
        "refused", "not_reclaimed", "total", "removed", "freed",
        "schema_version", "ok",
    }


def test_a_record_that_appears_between_the_plan_and_the_apply_saves_the_orphan(root):
    """The orphan VERDICT is re-derived at deletion, not only the structural rules.

    It is the verdict that authorises deleting a directory NOTHING points at, so it is
    the last one that may be taken on trust. The window is real — a job whose record is
    being written reads exactly like a job whose record is gone — and the age floor
    only narrows it. This closes it, and it needs no clock to do so.
    """
    ws = _scratch(root, "job_workspaces", f"staging_{_ORPHAN_ID}")
    _backdate(ws, 400)

    plan = plan_reclaim(root, orphans=True)
    assert [c.job_state for c in plan.candidates] == ["no_record"]

    save_job_plan(JobPlan(job_id=_ORPHAN_ID, repo_path=str(root),
                          state=RunState.RUNNING), root)
    outcome = apply_reclaim(plan)

    assert outcome.removed == ()
    assert [(r.reason, r.name) for r in outcome.refusals] == [
        ("job_unresolved", f"staging_{_ORPHAN_ID}")]
    assert f"{_ORPHAN_ID} appeared after the plan was computed" in outcome.refusals[0].detail
    assert ws.exists()


def test_an_orphan_freshened_between_the_plan_and_the_apply_is_refused_as_too_young(root):
    """The second half of the deletion-time verdict: the mtime is read again too.

    Its own test and its own mutation, because one branch of
    `_orphan_deletion_refusal` going green would otherwise hide behind the other.
    """
    ws = _scratch(root, "job_workspaces", f"staging_{_ORPHAN_ID}")
    _backdate(ws, 400)

    plan = plan_reclaim(root, orphans=True)
    assert [c.age_days for c in plan.candidates] == [400.0]

    os.utime(ws, None)                      # something touched it after the preview
    outcome = apply_reclaim(plan)

    assert outcome.removed == ()
    assert [(r.reason, r.name) for r in outcome.refusals] == [
        ("orphan_too_young", f"staging_{_ORPHAN_ID}")]
    assert ws.exists()
