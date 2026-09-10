"""F275 T003 — the three capabilities the UNIFIED job store lacked and now has.

A dry run of the classic-to-unified record flip, applied in a disposable worktree
and RUN, measured three things the classic store does and the unified store did not:

  W1  a JOBS-ROOT OVERRIDE — 186 classic call sites pass one and
      ``data_paths.job_record_path`` always accepted it, but ``save_job_plan`` and
      ``load_job_plan`` never passed it on;
  W2  CORRUPTION VISIBILITY — ``storage.load_job_safe`` returns ``(job, degraded)``
      and four production sites act on that flag, while ``load_job_plan`` answers
      ``None`` for a missing record and an unreadable one alike;
  W3  LISTING — ``storage.list_jobs`` and ``storage.list_jobs_safe`` are called at
      17 sites and the unified store had no listing function of any spelling.

DECISION F275 D23 rules that those three are widened in BEFORE the flip rather than
invented inside it, because the flip is this feature's one declared-oversize commit
and therefore the one commit that cannot be split to separate new API from the
migration onto it. These tests pin the three capabilities, the backward compatibility
that makes the widen green, and the layout rule the glob's placement obeys
(DECISION F260 D1: only ``data_paths`` spells the store's shape).

Every test isolates through ``tmp_path``, so none of them can write into the
repository's own ``.data``.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.data_paths import job_record_path, job_record_paths
from packages.orchestration.pingpong_job import (
    JobPlan,
    list_job_plans,
    list_job_plans_safe,
    load_job_plan,
    load_job_plan_safe,
    save_job_plan,
)


def _plan(job_id: str, created_at: str = "2026-09-10T12:00:00+00:00") -> JobPlan:
    """A minimal persistable JobPlan with a pinned id and timestamp."""
    return JobPlan(job_id=job_id, job_title="t-" + job_id, created_at=created_at)


def _corrupt(root: Path, job_id: str, text: str = "{not json") -> Path:
    """Write a record that EXISTS at the right path and cannot be read."""
    path = job_record_path(job_id, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


class TestTheJobsRootOverride:
    """W1: one call may name the store's base directory instead of the data root."""

    def test_a_save_under_an_explicit_root_writes_the_job_record_under_that_root(
        self, tmp_path: Path
    ) -> None:
        out = save_job_plan(_plan("aaaa000000000001"), tmp_path)

        assert out == tmp_path / "jobs" / "aaaa000000000001" / "job.json"
        assert out.is_file()

    def test_b_a_record_written_under_a_root_loads_back_through_the_same_root(
        self, tmp_path: Path
    ) -> None:
        save_job_plan(_plan("aaaa000000000002"), tmp_path)

        loaded = load_job_plan("aaaa000000000002", tmp_path)

        assert loaded is not None
        assert loaded.job_id == "aaaa000000000002"
        assert loaded.job_title == "t-aaaa000000000002"

    def test_c_a_record_under_one_root_is_invisible_under_another_root(
        self, tmp_path: Path
    ) -> None:
        here, elsewhere = tmp_path / "here", tmp_path / "elsewhere"
        save_job_plan(_plan("aaaa000000000003"), here)

        assert load_job_plan("aaaa000000000003", here) is not None
        assert load_job_plan("aaaa000000000003", elsewhere) is None

    def test_d_omitting_the_override_resolves_where_it_resolved_before(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The override is OPTIONAL: omitted, the process data root still decides.

        ``REMEDY_DATA_DIR`` points at ``tmp_path`` here so the default resolution is
        exercised for real without writing into the repository's own ``.data``.
        """
        data_dir = tmp_path / "remedy_data"
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))

        out = save_job_plan(_plan("aaaa000000000004"))

        assert out == data_dir / "jobs" / "aaaa000000000004" / "job.json"
        assert load_job_plan("aaaa000000000004") is not None


class TestCorruptionVisibilityOfOneRecord:
    """W2: the safe reader separates "no such job" from "that job's record rotted"."""

    def test_e_a_missing_record_reads_as_not_found_and_not_degraded(
        self, tmp_path: Path
    ) -> None:
        assert load_job_plan_safe("bbbb000000000001", tmp_path) == (None, False)

    def test_f_an_unreadable_record_reads_as_not_found_and_degraded(
        self, tmp_path: Path
    ) -> None:
        _corrupt(tmp_path, "bbbb000000000002")

        assert load_job_plan_safe("bbbb000000000002", tmp_path) == (None, True)

    def test_f2_a_record_whose_json_parses_into_the_wrong_shape_is_degraded_not_raised(
        self, tmp_path: Path
    ) -> None:
        """Valid JSON of the wrong TYPE reaches ``_import_job``, which raises.

        ``[]`` decodes fine, so ``JSONDecodeError`` never fires; the subscript inside
        ``_import_job`` is what fails. That is why the safe reader's except clause is
        wider than ``load_job_plan``'s.
        """
        _corrupt(tmp_path, "bbbb000000000003", text="[]")

        assert load_job_plan_safe("bbbb000000000003", tmp_path) == (None, True)

    def test_g_a_readable_record_reads_as_the_plan_and_not_degraded(
        self, tmp_path: Path
    ) -> None:
        save_job_plan(_plan("bbbb000000000004"), tmp_path)

        plan, degraded = load_job_plan_safe("bbbb000000000004", tmp_path)

        assert degraded is False
        assert plan is not None and plan.job_id == "bbbb000000000004"

    def test_h_the_plain_reader_cannot_tell_missing_from_unreadable_and_the_safe_one_can(
        self, tmp_path: Path
    ) -> None:
        """The gap this widen closes, written as a test rather than as a comment."""
        _corrupt(tmp_path, "bbbb000000000005")

        missing_plain = load_job_plan("bbbb000000000006", tmp_path)
        rotten_plain = load_job_plan("bbbb000000000005", tmp_path)
        assert missing_plain is rotten_plain is None

        missing_safe = load_job_plan_safe("bbbb000000000006", tmp_path)
        rotten_safe = load_job_plan_safe("bbbb000000000005", tmp_path)
        assert missing_safe != rotten_safe
        assert missing_safe == (None, False)
        assert rotten_safe == (None, True)


class TestListingTheUnifiedStore:
    """W3: the unified store can be enumerated, newest first, with skips named."""

    def test_i_an_absent_store_lists_nothing_and_does_not_raise(
        self, tmp_path: Path
    ) -> None:
        absent = tmp_path / "never_created"

        assert list_job_plans_safe(absent) == ([], False, [])
        assert list_job_plans(absent) == []

    def test_j_every_persisted_record_is_listed_newest_first(
        self, tmp_path: Path
    ) -> None:
        save_job_plan(_plan("cccc000000000001", "2026-09-01T00:00:00+00:00"), tmp_path)
        save_job_plan(_plan("cccc000000000003", "2026-09-03T00:00:00+00:00"), tmp_path)
        save_job_plan(_plan("cccc000000000002", "2026-09-02T00:00:00+00:00"), tmp_path)

        plans, degraded, skipped = list_job_plans_safe(tmp_path)

        assert [p.job_id for p in plans] == [
            "cccc000000000003",
            "cccc000000000002",
            "cccc000000000001",
        ]
        assert (degraded, skipped) == (False, [])

    def test_k_an_unreadable_record_is_skipped_and_named_by_its_job_id(
        self, tmp_path: Path
    ) -> None:
        save_job_plan(_plan("cccc000000000004"), tmp_path)
        _corrupt(tmp_path, "cccc000000000005")

        plans, degraded, skipped = list_job_plans_safe(tmp_path)

        assert [p.job_id for p in plans] == ["cccc000000000004"]
        assert degraded is True
        assert skipped == ["cccc000000000005"]

    def test_l_the_plain_listing_hides_the_degraded_flag(self, tmp_path: Path) -> None:
        save_job_plan(_plan("cccc000000000006"), tmp_path)
        _corrupt(tmp_path, "cccc000000000007")

        plain = list_job_plans(tmp_path)
        plans, degraded, skipped = list_job_plans_safe(tmp_path)

        assert [p.job_id for p in plain] == [p.job_id for p in plans]
        assert (degraded, skipped) == (True, ["cccc000000000007"])


class TestOnlyDataPathsSpellsTheStoreShape:
    """DECISION F260 D1: the layout glob lives in ``data_paths`` and nowhere else."""

    def test_m_the_accessor_returns_the_records_sorted_by_path(
        self, tmp_path: Path
    ) -> None:
        for job_id in ("dddd000000000003", "dddd000000000001", "dddd000000000002"):
            save_job_plan(_plan(job_id), tmp_path)

        found = job_record_paths(tmp_path)

        assert found == sorted(found)
        assert [p.parent.name for p in found] == [
            "dddd000000000001",
            "dddd000000000002",
            "dddd000000000003",
        ]
        assert {p.name for p in found} == {"job.json"}

    def test_m2_the_accessor_returns_an_empty_list_for_an_absent_store(
        self, tmp_path: Path
    ) -> None:
        assert job_record_paths(tmp_path / "never_created") == []

    def test_m3_the_classic_file_per_job_shape_is_not_what_the_accessor_finds(
        self, tmp_path: Path
    ) -> None:
        """A discriminator: the unified record is ``<id>/job.json``, never ``<id>.json``.

        Without this the glob could be widened to the classic store's shape and every
        other listing test would stay green, because a directory-per-job store has no
        top-level ``*.json`` file to confuse it.
        """
        (tmp_path / "jobs").mkdir(parents=True, exist_ok=True)
        (tmp_path / "jobs" / "dddd000000000004.json").write_text("{}")
        save_job_plan(_plan("dddd000000000005"), tmp_path)

        assert [p.parent.name for p in job_record_paths(tmp_path)] == [
            "dddd000000000005"
        ]
        plans, degraded, skipped = list_job_plans_safe(tmp_path)
        assert [p.job_id for p in plans] == ["dddd000000000005"]
        assert (degraded, skipped) == (False, [])

    def test_m4_pingpong_job_never_spells_the_store_layout_itself(self) -> None:
        """The guard this widen's first draft tripped, pinned where a reader lands.

        ``tests/test_data_paths.py`` owns the repo-wide form of this rule; this
        assertion keeps the reason for the glob's PLACEMENT next to the code that
        would otherwise move it back.
        """
        import ast
        import inspect

        from packages.orchestration import pingpong_job

        tree = ast.parse(inspect.getsource(pingpong_job))
        names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
        names |= {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}

        assert "jobs_dir" not in names
        assert "job_record_paths" in names


class TestRecordsWrittenBeforeThisRoundStillLoad:
    """The widen adds no required key, so every older record is still readable."""

    def test_n_a_record_carrying_none_of_the_new_keys_still_loads(
        self, tmp_path: Path
    ) -> None:
        path = job_record_path("eeee000000000001", tmp_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"job_id": "eeee000000000001", "created_at": "2026-01-01T00:00:00+00:00"})
            + "\n"
        )

        plan, degraded = load_job_plan_safe("eeee000000000001", tmp_path)

        assert degraded is False
        assert plan is not None and plan.job_id == "eeee000000000001"
        assert [p.job_id for p in list_job_plans(tmp_path)] == ["eeee000000000001"]
