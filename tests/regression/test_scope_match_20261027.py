"""The scope comparison of 2026-10-27 (operator amendment amend1027b-v1, A1), replayed with the fake builder.

The universe's green order to universe-chat read `changed_files_match: true` in its final review
while both file lists there were empty: with no expected set the review counted the job as
matching, and the story compared two empty sets as equal. Since then `match` is null whenever
nothing could be compared and the story says "nicht ermittelt"; it is true or false only when the
size decision's files (`scope_decision.json`) and the files of the job's diff are both known.
"""
from __future__ import annotations

import contextlib
import io
import json

from tests.orchestration.scale_harness import FakePlannerService, commit_repository

#: The lab repository; the order names no file, so the planner's size decision is asked.
LAB_FILES = {"README.md": "# lab\n", "src/app.py": "print(1)\n"}
ORDER = "Ergänze die Begrüßung um einen freundlichen Satz."


def _walk(tmp_path, monkeypatch, expected: list[str]):
    """`remedy do run` with the fake builder and reviewer; the size decision names EXPECTED."""
    from apps.cli.grouped import main
    from packages.orchestration.client_story import job_client_story
    from packages.orchestration.data_paths import job_dir
    from packages.orchestration.pingpong_job import load_job_plan

    repo = commit_repository(tmp_path / "lab", LAB_FILES)
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/dev/null")
    FakePlannerService(target="README.md", scope_answer={
        "single_job": True, "files": expected, "reason": "Eine Änderung."}).install(monkeypatch)
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.suppress(SystemExit):
        main(["do", "run", "--repo", str(repo), "--builder-provider", "fake", "--reviewer-provider", "fake",
              "--json", "--no-ui", "--run-unattended", "--", ORDER])
    [job_id] = json.loads(out.getvalue())["job_ids"]
    job = load_job_plan(job_id)
    review = job_dir(job_id) / "final_job_review.json"
    return job, job_client_story(job_id, job), json.loads(review.read_text()) if review.is_file() else None


def test_both_lists_empty_is_not_determined_never_a_match(tmp_path, monkeypatch):
    """The size decision names no file and the builder changes none: nothing to compare."""
    from packages.orchestration import pingpong_loop

    monkeypatch.setattr(pingpong_loop, "_apply_fake_builder_changes", lambda *a, **k: None)
    job, story, _review = _walk(tmp_path, monkeypatch, [])

    scope = story["scope"]
    assert scope["decided"] == "one_job"
    assert (scope["files_expected"], scope["files_touched"]) == ([], [])
    assert scope["match"] is None
    assert scope["match_text"] == "nicht ermittelt"


def test_both_lists_filled_compare_the_decision_with_the_diff(tmp_path, monkeypatch):
    """The fake builder writes `docs/README.md`; the size decision expected exactly that file."""
    job, story, review = _walk(tmp_path, monkeypatch, ["docs/README.md"])

    assert story["state"] == "done"
    scope = story["scope"]
    assert scope["files_expected"] == ["docs/README.md"]
    assert scope["files_touched"] == [change["path"] for change in story["changes"]] == ["docs/README.md"]
    assert scope["match"] is True and scope["match_text"] is None
    assert (scope["tasks"], scope["tasks_text"]) == (1, None)
    # The final review was given no expected set, so its comparison is unknown, never true.
    assert review is not None and review["changed_files_match"] is None
    assert review["scope_check"]["in_scope"] is None
