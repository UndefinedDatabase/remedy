"""Tests: bounded repair loop with structured patch via builder bridge."""
from __future__ import annotations

import json

from packages.core.models import Job
from packages.orchestration.builder_models import BuilderOutput


def _make_output(fix_content: str, action: str = "modify") -> BuilderOutput:
    patch_text = json.dumps({
        "file_ops": [{"path": "calc.py", "action": action, "content": fix_content}]
    })
    return BuilderOutput(
        summary="Fix calc",
        proposed_changes=["Fix calc"],
        structured_patch_text=patch_text,
        structured_patch_format="json",
    )


# The calc.py the diff-mode tests start from. Line 1 and line 6 are what the
# margin must pull in: no hunk ever names them, so their presence in a carried
# hunk can only come from the context margin.
_DIFF_CALC_SOURCE = (
    "# MARGIN_ANCHOR_TOP: no hunk in these tests names this line\n"
    "def add(a, b):\n"
    "    return 0\n"
    "\n"
    "\n"
    "def unchanged_helper():\n"
    "    return 1\n"
)


def _make_diff_output(old_line: str, new_line: str) -> BuilderOutput:
    """One unified-diff patch that rewrites calc.py line 3 and nothing else."""
    diff_text = (
        "--- a/calc.py\n"
        "+++ b/calc.py\n"
        "@@ -3,1 +3,1 @@\n"
        f"-{old_line}\n"
        f"+{new_line}\n"
    )
    patch_text = json.dumps({
        "unified_diffs": [{"path": "calc.py", "diff": diff_text}]
    })
    return BuilderOutput(
        summary="Fix calc",
        proposed_changes=["Fix calc"],
        structured_patch_text=patch_text,
        structured_patch_format="json",
    )


# The APPLY-side answer shape: the diff-only repair wrapper the loop decodes,
# as distinct from `_make_diff_output`'s structured-patch `unified_diffs` block.
def _make_diff_repair_answer(diff_text: str) -> BuilderOutput:
    """One repair answer in the `{format, version, diff, files}` wrapper."""
    patch_text = json.dumps({
        "format": "unified_diff",
        "version": 1,
        "diff": diff_text,
        "files": ["calc.py"],
    })
    return BuilderOutput(
        summary="Fix calc by diff",
        proposed_changes=["Fix calc"],
        structured_patch_text=patch_text,
        structured_patch_format="json",
    )


# The diff that repairs cycle 1's wrong fix: its context matches the file on disk.
_LANDING_DIFF = (
    "--- a/calc.py\n"
    "+++ b/calc.py\n"
    "@@ -2,2 +2,2 @@\n"
    " def add(a, b):\n"
    "-    return a - b\n"
    "+    return a + b\n"
)

# The same repair with ONE context line rewritten, so the strict applier rejects
# the hunk and the whole attempt has to be discarded.
_CONFLICTING_DIFF = (
    "--- a/calc.py\n"
    "+++ b/calc.py\n"
    "@@ -2,2 +2,2 @@\n"
    " def add(a, b, c):\n"
    "-    return a - b\n"
    "+    return a + b\n"
)


def _write_diff_repo(tmp_path) -> None:
    """Lay down the calc.py / test_calc.py pair the diff-mode tests drive."""
    (tmp_path / "calc.py").write_text(_DIFF_CALC_SOURCE)
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_calc.py").write_text(
        "from calc import add\n\ndef test_add():\n    assert add(2, 3) == 5\n"
    )


def _diff_build_fn(call_count):
    """Cycle 1 applies a wrong fix (tests fail), cycle 2 the right one."""
    def build_fn(repair_ctx):
        call_count[0] += 1
        if call_count[0] == 1:
            return _make_diff_output("    return 0", "    return a - b")
        return _make_diff_output("    return a - b", "    return a + b")
    return build_fn


class TestRepairLoopSuccess:
    def test_succeeds_on_first_cycle(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop

        (tmp_path / "calc.py").write_text("def add(a, b):\n    return a - b\n")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text(
            "from calc import add\n\ndef test_add():\n    assert add(2, 3) == 5\n"
        )
        fix = "def add(a, b):\n    return a + b\n"

        def build_fn(repair_ctx):
            return _make_output(fix)

        job = Job(name="test")
        result = run_builder_bridge_loop(
            build_fn, tmp_path, job=job, data_dir=tmp_path, max_cycles=3,
        )
        assert result.success is True
        assert result.cycles_run == 1
        assert len(result.repair_contexts) == 0

    def test_succeeds_on_second_cycle(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop

        (tmp_path / "calc.py").write_text("def add(a, b):\n    return 0\n")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text(
            "from calc import add\n\ndef test_add():\n    assert add(2, 3) == 5\n"
        )

        call_count = [0]
        def build_fn(repair_ctx):
            call_count[0] += 1
            if call_count[0] == 1:
                # Wrong fix first time
                return _make_output("def add(a, b):\n    return a - b\n")
            else:
                # Correct fix
                return _make_output("def add(a, b):\n    return a + b\n")

        job = Job(name="test")
        result = run_builder_bridge_loop(
            build_fn, tmp_path, job=job, data_dir=tmp_path, max_cycles=3,
        )
        assert result.success is True
        assert result.cycles_run == 2
        assert len(result.repair_contexts) == 1


class TestRepairLoopFailure:
    def test_stops_at_max_cycles(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop

        (tmp_path / "calc.py").write_text("def add(a, b):\n    return 0\n")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text(
            "from calc import add\n\ndef test_add():\n    assert add(2, 3) == 5\n"
        )

        def build_fn(repair_ctx):
            return _make_output("def add(a, b):\n    return a - b\n")

        job = Job(name="test")
        result = run_builder_bridge_loop(
            build_fn, tmp_path, job=job, data_dir=tmp_path, max_cycles=2,
        )
        assert result.success is False
        assert result.cycles_run == 2

    def test_stops_on_parse_failure(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop

        def build_fn(repair_ctx):
            return BuilderOutput(summary="Plan", proposed_changes=["Plan stuff"])

        job = Job(name="test")
        result = run_builder_bridge_loop(
            build_fn, tmp_path, job=job, data_dir=tmp_path, max_cycles=3,
        )
        assert result.success is False
        assert result.cycles_run == 1
        assert result.final_result.stage == "parse_failed"


class TestRepairLoopRepairContext:
    def test_repair_context_passed_to_builder(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop

        (tmp_path / "calc.py").write_text("def add(a, b):\n    return 0\n")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text(
            "from calc import add\n\ndef test_add():\n    assert add(2, 3) == 5\n"
        )

        received_contexts = []
        call_count = [0]
        def build_fn(repair_ctx):
            received_contexts.append(repair_ctx)
            call_count[0] += 1
            if call_count[0] <= 1:
                return _make_output("def add(a, b):\n    return a - b\n")
            return _make_output("def add(a, b):\n    return a + b\n")

        job = Job(name="test")
        run_builder_bridge_loop(
            build_fn, tmp_path, job=job, data_dir=tmp_path, max_cycles=3,
        )
        assert received_contexts[0] is None  # First call: no repair context
        assert received_contexts[1] is not None  # Second call: has repair context
        assert "failure_kind" in received_contexts[1]


class TestRepairLoopEvents:
    def test_cycle_events_emitted(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop
        from packages.orchestration.timeline import load_run_events

        (tmp_path / "calc.py").write_text("def add(a, b):\n    return 0\n")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text(
            "from calc import add\n\ndef test_add():\n    assert add(2, 3) == 5\n"
        )

        def build_fn(repair_ctx):
            return _make_output("def add(a, b):\n    return a + b\n")

        job = Job(name="test")
        run_builder_bridge_loop(
            build_fn, tmp_path, job=job, data_dir=tmp_path, max_cycles=3,
        )
        events = load_run_events(tmp_path, job.id)
        event_types = [e["event"] for e in events]
        assert "repair_loop_cycle_started" in event_types
        assert "repair_loop_succeeded" in event_types


class TestRepairLoopDiffMode:
    """F111 T003, prompt half: which source a repair round carries."""

    def test_diff_mode_attaches_margin_expanded_hunks_to_the_repair_context(
        self, tmp_path, monkeypatch,
    ):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop

        _write_diff_repo(tmp_path)
        call_count = [0]

        job = Job(name="test")
        result = run_builder_bridge_loop(
            _diff_build_fn(call_count), tmp_path,
            job=job, data_dir=tmp_path, max_cycles=3,
        )
        assert call_count[0] == 2  # cycle 2 was reached
        assert len(result.repair_contexts) == 1

        repair_ctx = result.repair_contexts[0]
        assert repair_ctx["repair_mode"] == "diff"
        hunks = repair_ctx["diff_hunks"]
        assert hunks
        first = hunks[0]
        assert first["path"] == "calc.py"
        assert first["start_line"] == 1
        assert first["end_line"] == 6
        # The patch names line 3 only. MARGIN_ANCHOR_TOP is line 1, so it can
        # only be in the carried text because the margin expanded the range.
        assert "MARGIN_ANCHOR_TOP" in first["text"]
        assert "-    return 0" not in first["text"]

    def test_diff_mode_off_leaves_the_repair_context_on_the_full_file_path(
        self, tmp_path, monkeypatch,
    ):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop
        from packages.orchestration.timeline import load_run_events

        _write_diff_repo(tmp_path)
        call_count = [0]

        job = Job(name="test")
        result = run_builder_bridge_loop(
            _diff_build_fn(call_count), tmp_path,
            job=job, data_dir=tmp_path, max_cycles=3,
            diff_mode=False,
        )
        repair_ctx = result.repair_contexts[0]
        assert repair_ctx["repair_mode"] == "full_file"
        assert "diff_hunks" not in repair_ctx

        events = load_run_events(tmp_path, job.id)
        selected = [e for e in events if e["event"] == "repair_mode_selected"]
        assert len(selected) == 1
        assert selected[0]["metadata"]["reason"] == "diff_mode_off"

    def test_a_patch_without_line_ranges_reports_full_file_with_a_reason(
        self, tmp_path, monkeypatch,
    ):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop
        from packages.orchestration.timeline import load_run_events

        _write_diff_repo(tmp_path)

        call_count = [0]
        def build_fn(repair_ctx):
            call_count[0] += 1
            if call_count[0] == 1:
                return _make_output("def add(a, b):\n    return a - b\n")
            return _make_output("def add(a, b):\n    return a + b\n")

        job = Job(name="test")
        result = run_builder_bridge_loop(
            build_fn, tmp_path, job=job, data_dir=tmp_path, max_cycles=3,
        )
        repair_ctx = result.repair_contexts[0]
        assert repair_ctx["repair_mode"] == "full_file"

        events = load_run_events(tmp_path, job.id)
        selected = [e for e in events if e["event"] == "repair_mode_selected"]
        assert len(selected) == 1
        # A file_ops path maps to an empty range list (DECISION F111 D3); what
        # this pins is that the reason is visible, never silently absent.
        assert selected[0]["metadata"]["reason"] in ("no_ranges", "no_hunks_selected")


class TestRepairLoopDiffChannel:
    """F111 T003, apply half: what a repair round ACCEPTS back."""

    def test_a_diff_shaped_answer_lands_through_the_diff_channel(
        self, tmp_path, monkeypatch,
    ):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop
        from packages.orchestration.timeline import load_run_events

        _write_diff_repo(tmp_path)
        call_count = [0]

        def build_fn(repair_ctx):
            call_count[0] += 1
            if call_count[0] == 1:
                return _make_diff_output("    return 0", "    return a - b")
            # Cycle 2's prompt asked for a diff, so the answer arrives as one.
            assert repair_ctx["repair_mode"] == "diff"
            return _make_diff_repair_answer(_LANDING_DIFF)

        job = Job(name="test")
        result = run_builder_bridge_loop(
            build_fn, tmp_path, job=job, data_dir=tmp_path, max_cycles=3,
        )
        assert result.success is True
        assert call_count[0] == 2
        assert "    return a + b\n" in (tmp_path / "calc.py").read_text()

        events = load_run_events(tmp_path, job.id)
        applied = [e for e in events if e["event"] == "diff_repair_applied"]
        assert len(applied) == 1
        assert applied[0]["metadata"]["mode"] == "diff"
        assert applied[0]["metadata"]["applied"] is True

    def test_a_conflicting_diff_is_discarded_whole_and_the_round_falls_back(
        self, tmp_path, monkeypatch,
    ):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop
        from packages.orchestration.timeline import load_run_events

        _write_diff_repo(tmp_path)
        pre_loop_bytes = (tmp_path / "calc.py").read_bytes()
        call_count = [0]
        # calc.py as each cycle FINDS it. Cycle 1 legitimately rewrites the file,
        # so the "zero partial application" line compares the bytes the discarded
        # attempt started from against the bytes the next cycle finds.
        seen_bytes: list[bytes] = []

        def build_fn(repair_ctx):
            call_count[0] += 1
            seen_bytes.append((tmp_path / "calc.py").read_bytes())
            if call_count[0] == 1:
                return _make_diff_output("    return 0", "    return a - b")
            if call_count[0] == 2:
                return _make_diff_repair_answer(_CONFLICTING_DIFF)
            return _make_output("def add(a, b):\n    return a + b\n")

        job = Job(name="test")
        result = run_builder_bridge_loop(
            build_fn, tmp_path, job=job, data_dir=tmp_path, max_cycles=3,
        )
        assert call_count[0] == 3  # the round continued after the discard
        assert seen_bytes[0] != seen_bytes[1]  # cycle 1 really did land
        assert seen_bytes[1] == seen_bytes[2]  # the rejected diff wrote nothing
        assert pre_loop_bytes == seen_bytes[0]

        events = load_run_events(tmp_path, job.id)
        applied = [e for e in events if e["event"] == "diff_repair_applied"]
        assert len(applied) == 1
        assert applied[0]["metadata"]["mode"] == "full_fallback"
        assert applied[0]["metadata"]["fallback_reason"]

        fell_back = [
            e for e in events
            if e["event"] == "repair_round_fell_back_to_full_file"
        ]
        assert len(fell_back) == 1
        assert fell_back[0]["metadata"]["cycle"] == 2

        # Both attempts are visible in the timeline, not just the surviving one.
        started = [e for e in events if e["event"] == "repair_loop_cycle_started"]
        assert [e["metadata"]["cycle"] for e in started] == [1, 2, 3]

        last_ctx = result.repair_contexts[-1]
        assert last_ctx["repair_mode"] == "full_file"
        assert last_ctx["full_file_reason"]

    def test_a_non_diff_answer_after_a_diff_prompt_is_reported_not_crashed(
        self, tmp_path, monkeypatch,
    ):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop
        from packages.orchestration.timeline import load_run_events

        _write_diff_repo(tmp_path)
        call_count = [0]

        def build_fn(repair_ctx):
            call_count[0] += 1
            if call_count[0] == 1:
                return _make_diff_output("    return 0", "    return a - b")
            # The prompt asked for a diff; the model answered with a whole file.
            assert repair_ctx["repair_mode"] == "diff"
            return _make_output("def add(a, b):\n    return a + b\n")

        job = Job(name="test")
        result = run_builder_bridge_loop(
            build_fn, tmp_path, job=job, data_dir=tmp_path, max_cycles=3,
        )
        events = load_run_events(tmp_path, job.id)
        not_used = [e for e in events if e["event"] == "diff_repair_not_used"]
        assert len(not_used) == 1
        assert not_used[0]["metadata"]["cycle"] == 2
        assert not_used[0]["metadata"]["reason"]

        # The round still ran through the normal channel and reached a terminal
        # state: no diff apply happened, and the loop stopped with a verdict.
        assert not [e for e in events if e["event"] == "diff_repair_applied"]
        assert result.success is True
        assert result.final_result.stage == "proof_collected"
