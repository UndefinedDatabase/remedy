"""Property tests for F033's approved-hunk apply seam.

One test per PROPERTY the seam turns on, named for the property rather than for the function
that implements it. The properties, in the order below: a clean subset lands EXACTLY the
approved hunks and nothing else; a subset one of whose hunks cannot apply leaves every file
BYTE-IDENTICAL, which is this round's reason to exist; the blocked ids of such a failure are
the conflicting FILE's hunks and not the whole selection; a refusal from the subset builder
writes nothing and carries the builder's own code; a missing capability and an unapproved
intent each land nothing and block every selected id; a multi-file subset lands both files;
and an empty subset never reaches the applier at all.

WHY the repository is real rather than mocked: the claim under test is that NOTHING IS WRITTEN
when part of an approved selection fails, and only a real file tree can witness that. Every
such tree is built under pytest's own ``tmp_path`` — the repository under test is never this
repository — and the data directory holding the applier's snapshots sits OUTSIDE the repo tree
so that snapshot writes cannot perturb the digests the proof rests on.

The permissioned job with an approved patch intent follows the recipe
``tests/orchestration/test_source_apply.py`` already uses. It is restated here rather than
imported: a test file that reaches into another test file's helpers couples two suites that
have no reason to move together."""

from __future__ import annotations

import difflib
import hashlib
from pathlib import Path
from unittest.mock import MagicMock
from uuid import uuid4

from packages.core.models import Job, RunState
from packages.orchestration import hunk_apply
from packages.orchestration.diff_parser import parse_unified_diff_to_view
from packages.orchestration.hunk_apply import (
    HUNK_APPLY_CONFLICT,
    HUNK_APPLY_NOTHING_TO_APPLY,
    HUNK_APPLY_REFUSED,
    apply_approved_hunks,
)
from packages.orchestration.hunk_subset_diff import (
    SUBSET_REFUSAL_ABSENT_HUNK,
    ApprovedSubsetDiff,
)

ORIGINAL = "\n".join(f"line {number:02d}" for number in range(1, 21)) + "\n"


def _edited(*replacements: tuple[str, str]) -> str:
    """``ORIGINAL`` with each ``(old, new)`` whole line replaced."""
    text = ORIGINAL
    for old, new in replacements:
        text = text.replace(old + "\n", new + "\n")
    return text


def _diff_of(new_text: str, path: str) -> str:
    """A ``difflib`` unified diff carrying ``---``/``+++`` headers. Two well-separated edits
    give two hunks."""
    return "".join(
        difflib.unified_diff(
            ORIGINAL.splitlines(True), new_text.splitlines(True),
            fromfile=f"a/{path}", tofile=f"b/{path}",
        )
    )


F_EDITS = _edited(("line 03", "line 03 CHANGED"), ("line 15", "line 15 CHANGED"))
F_DIFF = _diff_of(F_EDITS, "f.txt")
G_EDITS = _edited(("line 07", "line 07 CHANGED"))
G_DIFF = _diff_of(G_EDITS, "g.txt")
BOTH_FILES_DIFF = F_DIFF + G_DIFF


def _ids(diff_text: str, file_index: int = 0) -> list[str]:
    """The hunk ids of one file of ``diff_text``, in the diff's own order."""
    return [h["id"] for h in parse_unified_diff_to_view(diff_text)["files"][file_index]["hunks"]]


def _repo_with(tmp_path: Path, **files: str) -> tuple[Path, Path]:
    """A temporary repository holding ``files``, and a data directory beside it. The data
    directory is deliberately NOT inside the repository: the applier writes its snapshot there,
    and a snapshot inside the tree would show up in every digest taken below."""
    repo = tmp_path / "repo"
    repo.mkdir()
    for name, text in files.items():
        (repo / name).write_text(text, encoding="utf-8")
    data = tmp_path / "data"
    data.mkdir()
    return repo, data


def _tree_digests(root: Path) -> dict[str, str]:
    """Every file under ``root`` by relative path, with the sha256 of its bytes."""
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _approved_job(*, allow_write: bool = True, state: str = "approved") -> tuple[Job, str]:
    """A job carrying ``repo_generated_write`` and one patch intent in ``state``, and that
    intent's id. Both knobs exist so the two boundary tests can turn exactly one of them off."""
    job = Job(
        id=uuid4(),
        name="hunk apply job",
        user_prompt="land the approved hunks",
        state=RunState.RUNNING,
        tasks=[],
        artifacts=[],
        metadata={"permissions": {"repo_generated_write": "allow"}} if allow_write else {},
    )
    artifact = MagicMock()
    artifact.id = uuid4()
    artifact.task_id = uuid4()
    intent_id = f"{artifact.id.hex[:8]}-0"
    artifact.metadata = {
        "patch_intent_explanations": [
            {"file": "f.txt", "action": "modify", "risk": "low", "reason": "test", "summary": "t"}
        ],
        "patch_intent_approvals": {
            intent_id: {
                "intent_id": intent_id,
                "state": state,
                "decided_at": "2026-01-01T00:00:00Z",
                "decided_by": "test",
            }
        },
    }
    job.artifacts = [artifact]
    return job, intent_id


def _conflict_scenario(tmp_path: Path) -> tuple[Path, Path, list[str]]:
    """A two-file selection whose SECOND file cannot apply: ``g.txt``'s context line drifted on
    disk after the diff was taken. ``f.txt`` applies cleanly and is written first, so the
    rollback — not the ordering — is what has to put it back."""
    repo, data = _repo_with(tmp_path, **{"f.txt": ORIGINAL, "g.txt": ORIGINAL})
    (repo / "g.txt").write_text(
        ORIGINAL.replace("line 06\n", "line 06 DRIFTED\n"), encoding="utf-8"
    )
    approved = [_ids(BOTH_FILES_DIFF, 0)[0], _ids(BOTH_FILES_DIFF, 1)[0]]
    return repo, data, approved


def test_a_clean_subset_lands_exactly_the_approved_hunks_and_nothing_else(tmp_path):
    repo, data = _repo_with(tmp_path, **{"f.txt": ORIGINAL})
    job, intent_id = _approved_job()
    approved = _ids(F_DIFF)[0]

    outcome = apply_approved_hunks(
        F_DIFF, [approved], repo, job=job, intent_id=intent_id, data_dir=str(data)
    )

    assert outcome.applied is True, outcome.message
    assert outcome.landed == (approved,)
    assert outcome.blocked == ()
    assert outcome.code == ""
    assert outcome.apply_id
    # The BYTES, not a line count: only the approved hunk's line moved.
    assert (repo / "f.txt").read_text(encoding="utf-8") == _edited(("line 03", "line 03 CHANGED"))


def test_a_conflicting_hunk_leaves_every_file_byte_identical(tmp_path):
    """This round's reason to exist. ``f.txt`` is written by the applier and then restored from
    the snapshot when ``g.txt`` fails, so equal digests before and after are the whole proof."""
    repo, data, approved = _conflict_scenario(tmp_path)
    job, intent_id = _approved_job()
    before = _tree_digests(repo)

    outcome = apply_approved_hunks(
        BOTH_FILES_DIFF, approved, repo, job=job, intent_id=intent_id, data_dir=str(data)
    )

    after = _tree_digests(repo)
    assert outcome.applied is False
    assert outcome.landed == ()
    assert outcome.code == HUNK_APPLY_CONFLICT
    assert after == before, f"the repository moved: {before} -> {after}"
    assert set(before) == {"f.txt", "g.txt"}


def test_the_blocked_ids_of_a_conflict_are_the_conflicting_files_hunks(tmp_path):
    """Attribution, not a blanket. ``f.txt``'s hunk was approved too and is NOT blamed: only the
    file the applier named in an error contributes its ids."""
    repo, data, approved = _conflict_scenario(tmp_path)
    job, intent_id = _approved_job()

    outcome = apply_approved_hunks(
        BOTH_FILES_DIFF, approved, repo, job=job, intent_id=intent_id, data_dir=str(data)
    )

    conflicting = _ids(BOTH_FILES_DIFF, 1)[0]
    assert outcome.blocked == (conflicting,)
    assert approved[0] not in outcome.blocked
    assert len(approved) == 2


def test_a_subset_refusal_writes_nothing_and_carries_the_builders_own_code(tmp_path):
    """The applier is never called, so the file is untouched even though the FULL diff would
    have applied cleanly to it — which is exactly what the digests pin."""
    repo, data = _repo_with(tmp_path, **{"f.txt": ORIGINAL})
    job, intent_id = _approved_job()
    before = _tree_digests(repo)

    outcome = apply_approved_hunks(
        F_DIFF, ["deadbeefdeadbeef"], repo, job=job, intent_id=intent_id, data_dir=str(data)
    )

    assert outcome.code == HUNK_APPLY_REFUSED
    assert outcome.applied is False
    assert outcome.landed == ()
    assert outcome.apply_id == ""
    assert outcome.blocked == ("deadbeefdeadbeef",)
    assert SUBSET_REFUSAL_ABSENT_HUNK in outcome.message
    assert _tree_digests(repo) == before
    assert (repo / "f.txt").read_text(encoding="utf-8") == ORIGINAL


def test_a_job_without_the_write_capability_lands_nothing_and_blocks_every_id(tmp_path):
    repo, data = _repo_with(tmp_path, **{"f.txt": ORIGINAL})
    job, intent_id = _approved_job(allow_write=False)
    approved = _ids(F_DIFF)
    before = _tree_digests(repo)

    outcome = apply_approved_hunks(
        F_DIFF, approved, repo, job=job, intent_id=intent_id, data_dir=str(data)
    )

    assert outcome.applied is False
    assert outcome.landed == ()
    assert outcome.code == HUNK_APPLY_CONFLICT
    # No file was named, because the refusal happened before any file was touched.
    assert outcome.blocked == tuple(approved)
    assert _tree_digests(repo) == before


def test_an_unapproved_intent_lands_nothing_and_blocks_every_id(tmp_path):
    repo, data = _repo_with(tmp_path, **{"f.txt": ORIGINAL})
    job, intent_id = _approved_job(state="pending")
    approved = _ids(F_DIFF)
    before = _tree_digests(repo)

    outcome = apply_approved_hunks(
        F_DIFF, approved, repo, job=job, intent_id=intent_id, data_dir=str(data)
    )

    assert outcome.applied is False
    assert outcome.landed == ()
    assert outcome.code == HUNK_APPLY_CONFLICT
    assert outcome.blocked == tuple(approved)
    assert _tree_digests(repo) == before


def test_a_multi_file_subset_lands_both_files(tmp_path):
    repo, data = _repo_with(tmp_path, **{"f.txt": ORIGINAL, "g.txt": ORIGINAL})
    job, intent_id = _approved_job()
    approved = [_ids(BOTH_FILES_DIFF, 0)[0], _ids(BOTH_FILES_DIFF, 1)[0]]

    outcome = apply_approved_hunks(
        BOTH_FILES_DIFF, approved, repo, job=job, intent_id=intent_id, data_dir=str(data)
    )

    assert outcome.applied is True, outcome.message
    assert outcome.landed == tuple(approved)
    assert (repo / "f.txt").read_text(encoding="utf-8") == _edited(("line 03", "line 03 CHANGED"))
    assert (repo / "g.txt").read_text(encoding="utf-8") == G_EDITS


def test_a_subset_with_no_file_never_reaches_the_applier(tmp_path, monkeypatch):
    """The empty subset is unreachable through ``build_approved_subset_diff``, which refuses an
    empty approved set and refuses an absent id, so the branch is reached by injection. It is
    pinned anyway: the outcome must be a named code and NOT an apply id for a mutation that
    never happened."""
    repo, data = _repo_with(tmp_path, **{"f.txt": ORIGINAL})
    job, intent_id = _approved_job()

    def _must_not_run(*args, **kwargs):
        raise AssertionError("the applier must not be called for an empty subset")

    monkeypatch.setattr(
        hunk_apply, "build_approved_subset_diff", lambda *a, **k: ApprovedSubsetDiff((), ())
    )
    monkeypatch.setattr(hunk_apply, "apply_structured_patch", _must_not_run)

    outcome = apply_approved_hunks(
        F_DIFF, _ids(F_DIFF), repo, job=job, intent_id=intent_id, data_dir=str(data)
    )

    assert outcome.code == HUNK_APPLY_NOTHING_TO_APPLY
    assert outcome.applied is False
    assert outcome.landed == ()
    assert outcome.blocked == ()
    assert outcome.apply_id == ""
