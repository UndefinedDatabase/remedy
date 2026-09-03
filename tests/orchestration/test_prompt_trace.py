"""Tests for prompt trace redaction, capture, and evidence export.

Steps 5085-5086: Verifies that prompt traces redact secrets and capture
complete builder/reviewer metadata.
"""
from __future__ import annotations

import dataclasses
import inspect
import json

from packages.orchestration.intake import compose_intake_prompt, make_intake_call_recorder
from packages.orchestration.prompt_trace import (
    PromptTraceEntry,
    build_trace_entry,
    build_trace_summary,
    measure_dedupe_savings_from_traces,
    redact_prompt_text,
    trace_entry_to_dict,
    write_trace_jsonl,
)

# ---------------------------------------------------------------------------
# Step 5085: Prompt trace redaction
# ---------------------------------------------------------------------------


class TestPromptTraceRedaction:
    def test_redacts_api_key_env(self):
        text = "Use API_KEY=sk-abc123xyz to connect"
        result = redact_prompt_text(text)
        assert "sk-abc123xyz" not in result
        assert "API_KEY=[REDACTED]" in result

    def test_redacts_secret_env(self):
        text = "Set SECRET=my_super_secret_value"
        result = redact_prompt_text(text)
        assert "my_super_secret_value" not in result
        assert "SECRET=[REDACTED]" in result

    def test_redacts_bearer_token(self):
        text = "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.payload.sig"
        result = redact_prompt_text(text)
        assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in result
        assert "[REDACTED]" in result

    def test_redacts_sk_ant(self):
        text = "key: sk-ant-abcdefghijklmnopqrstuvwx"
        result = redact_prompt_text(text)
        assert "abcdefghijklmnopqrstuvwx" not in result
        assert "[REDACTED]" in result

    def test_redacts_sk_openai(self):
        text = "key: sk-abcdefghijklmnopqrstuvwx"
        result = redact_prompt_text(text)
        assert "sk-abcdefghijklmnopqrstuvwx" not in result

    def test_redacts_ghp(self):
        text = "token: ghp_abcdefghijklmnopqrstuvwxyz0123456789"
        result = redact_prompt_text(text)
        assert "ghp_" not in result

    def test_redacts_akia(self):
        text = "aws: AKIAIOSFODNN7EXAMPLE"
        result = redact_prompt_text(text)
        assert "AKIAIOSFODNN7EXAMPLE" not in result

    def test_redacts_private_key(self):
        text = "-----BEGIN RSA PRIVATE KEY-----\nMIIBogI...\n-----END RSA PRIVATE KEY-----"
        result = redact_prompt_text(text)
        assert "MIIBogI" not in result
        assert "[PRIVATE_KEY_REDACTED]" in result

    def test_redacts_env_content_password(self):
        text = "PASSWORD=hunter2"
        result = redact_prompt_text(text)
        assert "hunter2" not in result
        assert "PASSWORD=[REDACTED]" in result

    def test_preserves_normal_text(self):
        text = "This is a normal prompt with no secrets."
        result = redact_prompt_text(text)
        assert result == text

    def test_redacts_token_env(self):
        text = "TOKEN=abc123secret"
        result = redact_prompt_text(text)
        assert "abc123secret" not in result

    def test_redacts_credential_env(self):
        text = "CREDENTIAL=mysecretcred"
        result = redact_prompt_text(text)
        assert "mysecretcred" not in result


# ---------------------------------------------------------------------------
# Step 5086: Prompt trace completeness
# ---------------------------------------------------------------------------


class TestPromptTraceCompleteness:
    def test_builder_trace_has_required_fields(self):
        entry = build_trace_entry(
            prompt_text="Build something",
            role="builder",
            run_id="run123",
            round_num=1,
            provider="fake",
            cwd="/tmp/staging",
            write_mode="diff",
            prompt_kind="initial",
            context_categories=["file_tree", "readme"],
        )
        assert entry.role == "builder"
        assert entry.provider == "fake"
        assert entry.cwd == "/tmp/staging"
        assert entry.write_mode == "diff"
        assert entry.prompt_kind == "initial"
        assert entry.prompt_sha256
        assert entry.prompt_chars == len("Build something")
        assert entry.prompt_tokens_estimated > 0
        assert entry.context_categories == ["file_tree", "readme"]
        assert entry.created_at

    def test_reviewer_trace_has_required_fields(self):
        entry = build_trace_entry(
            prompt_text="Review changes",
            role="reviewer",
            run_id="run456",
            round_num=1,
            provider="fake",
            cwd="/tmp/staging",
            write_mode="none",
            prompt_kind="review",
            safe_diff_files=["main.py"],
            changed_files=["main.py"],
        )
        assert entry.role == "reviewer"
        assert entry.safe_diff_files == ["main.py"]
        assert entry.changed_files == ["main.py"]

    def test_prompt_hash_is_stable(self):
        text = "Deterministic prompt text"
        e1 = build_trace_entry(prompt_text=text, role="builder")
        e2 = build_trace_entry(prompt_text=text, role="builder")
        assert e1.prompt_sha256 == e2.prompt_sha256

    def test_prompt_hash_differs_for_different_text(self):
        e1 = build_trace_entry(prompt_text="text a", role="builder")
        e2 = build_trace_entry(prompt_text="text b", role="builder")
        assert e1.prompt_sha256 != e2.prompt_sha256

    def test_trace_summary_counts(self):
        entries = [
            build_trace_entry(prompt_text="b1", role="builder", provider="fake"),
            build_trace_entry(prompt_text="r1", role="reviewer", provider="fake"),
            build_trace_entry(prompt_text="b2", role="builder", provider="fake"),
        ]
        summary = build_trace_summary(entries)
        assert summary["total_prompts"] == 3
        assert summary["builder_prompts"] == 2
        assert summary["reviewer_prompts"] == 1
        assert summary["providers"] == ["fake"]

    def test_trace_to_dict_roundtrip(self):
        entry = build_trace_entry(prompt_text="test", role="builder", run_id="r1")
        d = trace_entry_to_dict(entry)
        assert d["role"] == "builder"
        assert d["run_id"] == "r1"
        assert isinstance(d["prompt_sha256"], str)

    def test_write_trace_jsonl(self, tmp_path):
        entries = [
            build_trace_entry(prompt_text="b1", role="builder"),
            build_trace_entry(prompt_text="r1", role="reviewer"),
        ]
        path = tmp_path / "trace.jsonl"
        write_trace_jsonl(entries, path)
        lines = path.read_text().strip().split("\n")
        assert len(lines) == 2
        d0 = json.loads(lines[0])
        assert d0["role"] == "builder"
        d1 = json.loads(lines[1])
        assert d1["role"] == "reviewer"

    def test_missing_trace_reported_honestly(self):
        entry = build_trace_entry(prompt_text="", role="builder")
        assert entry.prompt_chars == 0
        assert entry.prompt_tokens_estimated == 0

    def test_prompt_text_capped(self):
        long_text = "x" * 60_000
        entry = build_trace_entry(prompt_text=long_text, role="builder")
        assert entry.prompt_text_truncated is True
        assert "[PROMPT_TEXT_TRUNCATED]" in entry.prompt_text_redacted
        assert len(entry.prompt_text_redacted) < 60_000

    def test_redaction_applied_to_trace(self):
        entry = build_trace_entry(
            prompt_text="Use API_KEY=sk-secret123456789012345 here",
            role="builder",
        )
        assert "sk-secret" not in entry.prompt_text_redacted
        assert "[REDACTED]" in entry.prompt_text_redacted


# ---------------------------------------------------------------------------
# F105 T003 site 1: the composed-prompt segment manifest in call evidence
# ---------------------------------------------------------------------------


class TestSegmentManifest:
    def test_entry_without_a_composed_prompt_carries_no_manifest(self):
        entry = build_trace_entry(prompt_text="plain prompt", role="builder")
        assert entry.segment_manifest == []
        assert entry.segment_manifest_chars == 0

    def test_composed_prompt_fills_the_manifest_rows(self):
        composed = compose_intake_prompt("demo mission")
        entry = build_trace_entry(
            prompt_text=composed.text,
            role="intake",
            composed_prompt=composed,
        )
        assert [row["name"] for row in entry.segment_manifest] == [
            "intake_system",
            "intake_rules",
            "intake_mission",
        ]
        assert [row["sha256"] for row in entry.segment_manifest] == [
            m.sha256 for m in composed.manifest
        ]
        assert entry.segment_manifest_chars == len(composed.text)

    def test_manifest_chars_fall_short_of_a_schema_wrapped_prompt(self):
        """The gap is expected: DECISION F105 D3 leaves the schema tail
        `run_structured_call` appends outside every builder UNREGISTERED, so the
        manifest covers the composed base prompt only. Recording both numbers is
        what makes that coverage gap visible instead of implied."""
        composed = compose_intake_prompt("demo mission")
        entry = build_trace_entry(
            prompt_text=composed.text + "\n\nSCHEMA TAIL",
            role="intake",
            composed_prompt=composed,
        )
        assert entry.segment_manifest_chars < entry.prompt_chars

    def test_manifest_survives_the_jsonl_round_trip(self, tmp_path):
        composed = compose_intake_prompt("demo mission")
        entry = build_trace_entry(
            prompt_text=composed.text,
            role="intake",
            composed_prompt=composed,
        )
        path = tmp_path / "trace.jsonl"
        write_trace_jsonl([entry], path)
        loaded = json.loads(path.read_text().strip())
        assert loaded["segment_manifest"] == entry.segment_manifest
        assert loaded["segment_manifest_chars"] == entry.segment_manifest_chars

    def test_the_cli_recorder_passes_the_composed_prompt(self):
        """Wiring guard: a manifest field the CLI never fills fails HERE."""
        import apps.cli.commands.do_cmd as do_cmd

        traces: list = []
        composed = compose_intake_prompt("demo mission")
        recorder = make_intake_call_recorder(
            traces, composed, provider="ollama", provider_kind="ollama"
        )
        recorder(1, "ji1", False, composed.text)
        assert len(traces) == 1
        assert len(traces[0].segment_manifest) == 3

        assert "make_intake_call_recorder" in inspect.getsource(do_cmd)

    def test_the_cli_flight_plan_recorder_passes_the_composed_prompt(self):
        """Wiring guard: an unwired flight-plan manifest fails HERE (F105 R27)."""
        import apps.cli.commands.do_cmd as do_cmd
        from packages.orchestration.flight_plan import (
            compose_flight_plan_prompt,
            make_flight_plan_call_recorder,
        )

        traces: list = []
        composed = compose_flight_plan_prompt(
            {"goal": "demo"}, project_facts="pinned facts"
        )
        recorder = make_flight_plan_call_recorder(
            traces, composed, provider="ollama", provider_kind="ollama"
        )
        recorder(1, "fp1", False, composed.text)
        assert len(traces) == 1
        assert traces[0].role == "flight_plan"
        assert traces[0].prompt_kind == "flight-plan"
        assert len(traces[0].segment_manifest) == 5

        source = inspect.getsource(do_cmd)
        assert "make_flight_plan_call_recorder" in source
        assert "prompt_traces" in source

    def test_appending_traces_keeps_the_earlier_ones(self, tmp_path):
        """A replan must not truncate the traces its job's first run wrote."""
        from packages.orchestration.prompt_trace import append_trace_jsonl

        composed = compose_intake_prompt("demo mission")
        first = build_trace_entry(
            prompt_text=composed.text, role="intake", composed_prompt=composed,
        )
        second = build_trace_entry(
            prompt_text=composed.text, role="flight_plan", composed_prompt=composed,
        )
        path = tmp_path / "prompt_trace.jsonl"
        write_trace_jsonl([first], path)
        append_trace_jsonl([second], path)
        lines = path.read_text().strip().split("\n")
        assert len(lines) == 2
        assert [json.loads(x)["role"] for x in lines] == ["intake", "flight_plan"]

    def test_appending_to_a_missing_file_creates_it(self, tmp_path):
        from packages.orchestration.prompt_trace import append_trace_jsonl

        composed = compose_intake_prompt("demo mission")
        entry = build_trace_entry(
            prompt_text=composed.text, role="flight_plan", composed_prompt=composed,
        )
        path = tmp_path / "nested" / "prompt_trace.jsonl"
        append_trace_jsonl([entry], path)
        assert len(path.read_text().strip().split("\n")) == 1

    def test_the_replan_path_records_and_appends_its_traces(self):
        """Wiring guard: an unwired or truncating replan fails HERE (F105 R28)."""
        import apps.cli.commands.do_cmd as do_cmd

        source = inspect.getsource(do_cmd)
        assert "replan_traces" in source
        assert "append_trace_jsonl" in source
        assert source.count("on_call=make_flight_plan_call_recorder(") == 2

    def test_every_cli_call_site_hands_its_composition_down(self):
        """R-0256 wiring guard: a site that composes twice fails HERE."""
        import apps.cli.commands.do_cmd as do_cmd

        source = inspect.getsource(do_cmd)
        assert "composed=intake_composed," in source
        assert "composed=plan_composed," in source
        assert "composed=replan_composed," in source

    def test_the_builder_composition_traces_a_real_segment_manifest(self):
        """F115 D1 behaviour: a composed builder prompt traces with real rows.

        DECLARED DEVIATION from the F115 R2 block, gate (e1), which asks that
        `segment_manifest_chars` equal the SUM of the rows' `chars`. It cannot:
        `build_trace_entry` sets it to `len(composed_prompt.text)`
        (`prompt_trace.py:157-158`) and `compose_prompt_segments` joins segments
        with the two-character `PROMPT_SEGMENT_DELIMITER`, so a composed text of
        N segments is exactly 2*(N-1) characters longer than the sum of its
        segments. The gate's equality is unreachable for any multi-segment
        prompt, so the true accounting identity is pinned here instead.
        """
        from packages.orchestration.prompt_segments import PROMPT_SEGMENT_DELIMITER
        from packages.orchestration.pingpong_loop import compose_builder_prompt

        composed = compose_builder_prompt(
            "implement feature X",
            "job context",
            round_number=1,
            task_body="detailed task body",
            scope_contract="scope contract text",
        )
        entry = build_trace_entry(
            prompt_text=composed.text,
            role="builder",
            composed_prompt=composed,
        )
        assert entry.segment_manifest != []
        assert [row["name"] for row in entry.segment_manifest] == [
            "builder_system",
            "builder_scope_contract",
            "builder_context",
            "builder_task",
            "builder_task_body",
            "builder_directive",
        ]
        for row in entry.segment_manifest:
            assert set(row) == {"name", "rank", "sha256", "chars", "tokens_estimated"}
            assert len(row["sha256"]) == 64
            assert row["chars"] > 0
        rows = entry.segment_manifest
        boundaries = len(rows) - 1
        assert entry.segment_manifest_chars == len(composed.text)
        assert entry.segment_manifest_chars == sum(
            int(row["chars"]) for row in rows
        ) + boundaries * len(PROMPT_SEGMENT_DELIMITER)

    def test_the_builder_call_site_hands_its_composition_down(self):
        """F115 D1 wiring guard: an unwired builder trace entry fails HERE.

        The behaviour test above passes even when this call site is unwired,
        because it never touches `pingpong_loop` — which is why this guard
        exists. Same `inspect.getsource` pattern as the CLI guards above.

        THE SITES ARE SELECTED BY THE ROLE THEY DECLARE, NEVER BY POSITION.
        F109 `R-0774` added a SECOND builder append inside the resume-fallback
        branch; the old fixed index `[1]` never reached it and kept passing by
        luck, while the same insertion silently moved the reviewer guard's
        index onto a builder site — finding `R-0775`. So this case splits the
        source into ALL `build_trace_entry` append sites, keeps the TWO that
        declare `role="builder",`, and asserts of EVERY one of them that it
        hands its composition down. That pins the fallback append too, which
        no index reached before, and leaves no numeral for a future insertion
        to move.

        The count is 2 because F109 `R-0771` added a SECOND composition inside
        the resume-fallback branch — a fallback is not a resumed session, so it
        recomposes at full content — and the second assertion below pins that
        site rather than leaving a bare number any duplication would satisfy.
        """
        import packages.orchestration.pingpong_loop as pingpong_loop

        source = inspect.getsource(pingpong_loop)
        assert source.count("builder_composed = compose_builder_prompt(") == 2
        fallback = source.split("if builder_resume_ref and builder_out.error:")[1]
        assert "builder_composed = compose_builder_prompt(" in fallback
        assert "builder_prompt = builder_composed.text" in source
        sites = [
            part.split("))")[0]
            for part in source.split("result.prompt_traces.append(build_trace_entry(")[1:]
        ]
        builder_sites = [site for site in sites if 'role="builder",' in site]
        assert len(builder_sites) == 2, len(sites)
        for site in builder_sites:
            assert "prompt_text=builder_prompt," in site
            assert "composed_prompt=builder_composed," in site

    def test_the_reviewer_composition_traces_a_real_segment_manifest(self, monkeypatch):
        """F115 D1 behaviour, reviewer half: the manifest covers the composed BASE.

        The reviewer's traced text is `_reviewer_effective_prompt(...)`, which in
        structured mode appends the native-schema tail the registry deliberately
        does NOT cover (DECISION F105 D3). So `segment_manifest_chars` records the
        composed base and stays strictly BELOW `prompt_chars`, and that gap IS the
        coverage gap — recorded instead of implied. Structured mode is forced on
        here so the assertion cannot depend on the ambient environment.
        """
        from packages.orchestration.prompt_segments import PROMPT_SEGMENT_DELIMITER
        from packages.orchestration.pingpong_loop import (
            _reviewer_effective_prompt,
            compose_reviewer_prompt,
        )

        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        composed = compose_reviewer_prompt(
            "implement feature X",
            "builder did the thing",
            diff_summary="M  a.py",
            test_result="2 passed",
            files_changed=["a.py"],
            task_excerpt="detailed task body",
            task_sha256="abc",
            task_tokens_estimated=7,
            scope_contract="scope contract text",
        )
        entry = build_trace_entry(
            prompt_text=_reviewer_effective_prompt(composed.text),
            role="reviewer",
            composed_prompt=composed,
        )
        assert entry.segment_manifest != []
        assert [row["name"] for row in entry.segment_manifest] == [
            "reviewer_system",
            "reviewer_scope_contract",
            "reviewer_goal",
            "reviewer_task_input",
            "reviewer_builder_summary",
            "reviewer_files_changed",
            "reviewer_staged_diff",
            "reviewer_test_result",
        ]
        for row in entry.segment_manifest:
            assert set(row) == {"name", "rank", "sha256", "chars", "tokens_estimated"}
            assert len(row["sha256"]) == 64
            assert row["chars"] > 0
        rows = entry.segment_manifest
        boundaries = len(rows) - 1
        assert entry.segment_manifest_chars == len(composed.text)
        assert entry.segment_manifest_chars == sum(
            int(row["chars"]) for row in rows
        ) + boundaries * len(PROMPT_SEGMENT_DELIMITER)
        assert entry.segment_manifest_chars < entry.prompt_chars

    def test_the_reviewer_call_site_hands_its_composition_down(self):
        """F115 D1 wiring guard: an unwired reviewer trace entry fails HERE.

        The behaviour test above passes even when this call site is unwired,
        because it never touches `pingpong_loop` — which is why this guard
        exists. THE SITE IS SELECTED BY THE ROLE IT DECLARES, NEVER BY
        POSITION: exactly ONE `build_trace_entry` append declares
        `role="reviewer",`, and that arity is asserted before the site is
        read. The old fixed index `[2]` broke the moment F109 `R-0774` added a
        builder append earlier in the file and index 2 resolved onto it —
        finding `R-0775` — so no numeral is left here for a future insertion
        to move.

        The count is 2 because F109 `R-0771` added a SECOND composition inside
        the resume-fallback branch — a fallback is not a resumed session, so it
        recomposes at full content — and the second assertion below pins that
        site rather than leaving a bare number any duplication would satisfy.
        """
        import packages.orchestration.pingpong_loop as pingpong_loop

        source = inspect.getsource(pingpong_loop)
        assert source.count("reviewer_composed = compose_reviewer_prompt(") == 2
        fallback = source.split("if reviewer_resume_ref and reviewer_out.error:")[1]
        assert "reviewer_composed = compose_reviewer_prompt(" in fallback
        assert "reviewer_prompt = reviewer_composed.text" in source
        sites = [
            part.split("))")[0]
            for part in source.split("result.prompt_traces.append(build_trace_entry(")[1:]
        ]
        reviewer_sites = [site for site in sites if 'role="reviewer",' in site]
        assert len(reviewer_sites) == 1, len(sites)
        site = reviewer_sites[0]
        assert "prompt_text=prompt_text," in site
        assert "composed_prompt=reviewer_composed," in site


# ---------------------------------------------------------------------------
# F109: the trace names what the composition did NOT resend
# ---------------------------------------------------------------------------


class TestDedupedSegmentNames:
    """`deduped_segment_names` rides the same `composed_prompt` seam as the manifest.

    A class of its own rather than three more cases in `TestSegmentManifest`,
    because the two EMPTIES next door to each other mean different things: an
    empty `segment_manifest` says the prompt was never composed through the
    registry, an empty `deduped_segment_names` says a composed prompt withheld
    nothing. Keeping the claims apart is what stops a reader conflating them.
    """

    def test_an_entry_without_a_composed_prompt_names_nothing(self):
        entry = build_trace_entry(prompt_text="plain prompt", role="builder")
        assert entry.deduped_segment_names == []

    def test_a_composition_that_replaced_nothing_names_nothing(self):
        # THE OTHER EMPTY, AND IT IS NOT THE SAME ONE. This prompt WAS composed —
        # its manifest is populated — and simply deduped nothing, which is the
        # normal case everywhere outside a resumed session.
        composed = compose_intake_prompt("demo mission")
        entry = build_trace_entry(
            prompt_text=composed.text, role="intake", composed_prompt=composed,
        )
        assert entry.segment_manifest != []
        assert composed.deduped_names == ()
        assert entry.deduped_segment_names == []

    def test_the_names_arrive_in_order_and_as_a_list_not_the_source_tuple(self):
        # THE TYPE IS PART OF THE CLAIM, not tidiness: `asdict` serialises this
        # entry to JSON, where a tuple round-trips back as a list, so an entry
        # that kept the source tuple would describe itself one way in memory and
        # another way on disk. THE ORDER IS PART OF IT TOO — the pair below is
        # deliberately NOT the manifest's own order, so a derivation that read
        # the manifest instead of the report would fail here.
        composed = dataclasses.replace(
            compose_intake_prompt("demo mission"),
            deduped_names=("intake_rules", "intake_system"),
        )
        entry = build_trace_entry(
            prompt_text=composed.text, role="intake", composed_prompt=composed,
        )
        assert entry.deduped_segment_names == ["intake_rules", "intake_system"]
        assert isinstance(entry.deduped_segment_names, list)
        assert [row["name"] for row in entry.segment_manifest][:2] == [
            "intake_system",
            "intake_rules",
        ]


# ---------------------------------------------------------------------------
# F109 T003d: the savings the trace record itself proves
# ---------------------------------------------------------------------------


class TestMeasureDedupeSavingsFromTraces:
    """SPEC H: the arithmetic, on hand-built entries, where the numbers are exact.

    HAND-BUILT AND NOT LOOP-DRIVEN, on purpose. A real run's segment sizes move
    whenever any prompt text changes, so a case asserting them as numerals would
    pin this file to unrelated prompt edits. The real-loop claim lives in
    `tests/orchestration/test_semantic_dedupe.py` and asserts relations rather
    than numbers; the exact arithmetic is asserted here, where the inputs are
    chosen and cannot drift.
    """

    FULL_CHARS = 1200
    MARKER_CHARS = 40
    NAME = "builder_context"

    @classmethod
    def _row(cls, name: str, chars: int) -> dict[str, str | int]:
        """One manifest row in the shipped shape — `manifest_as_dicts`'s five keys."""
        return {
            "name": name,
            "rank": "job_context",
            "sha256": "0" * 64,
            "chars": chars,
            "tokens_estimated": chars // 4,
        }

    @classmethod
    def _full_entry(cls, role: str = "builder") -> PromptTraceEntry:
        """An entry that sent the segment IN FULL and withheld nothing."""
        return PromptTraceEntry(
            role=role, segment_manifest=[cls._row(cls.NAME, cls.FULL_CHARS)],
        )

    @classmethod
    def _deduped_entry(cls, role: str = "builder") -> PromptTraceEntry:
        """An entry whose manifest row for the segment is the MARKER, not the text."""
        return PromptTraceEntry(
            role=role,
            segment_manifest=[cls._row(cls.NAME, cls.MARKER_CHARS)],
            deduped_segment_names=[cls.NAME],
        )

    # -- SPEC H case 1: nothing in, nothing claimed --------------------------

    def test_no_entries_measures_nothing(self):
        measured = measure_dedupe_savings_from_traces([])

        assert measured.chars_avoided == 0
        assert measured.chars_spent_on_markers == 0
        assert measured.net_chars_saved == 0
        assert measured.deduped_occurrences_counted == 0
        assert measured.unmeasured_segment_names == ()

    # -- SPEC H case 2: entries that deduped nothing, however many -----------

    def test_entries_that_deduped_nothing_measure_nothing(self):
        # THE ENTRIES ARE REAL COMPOSITIONS as far as this function can tell —
        # populated manifests, just no withheld names — so a zero here is about
        # the absence of dedupe rather than about an empty input.
        entries = [self._full_entry(), self._full_entry(), self._full_entry("reviewer")]
        assert [e.segment_manifest for e in entries if e.segment_manifest] == [
            e.segment_manifest for e in entries
        ]

        measured = measure_dedupe_savings_from_traces(entries)

        assert measured.chars_avoided == 0
        assert measured.chars_spent_on_markers == 0
        assert measured.net_chars_saved == 0
        assert measured.deduped_occurrences_counted == 0
        assert measured.unmeasured_segment_names == ()

    # -- SPEC H case 3: the arithmetic, as exact numbers ---------------------

    def test_the_saving_is_the_full_size_minus_the_marker_it_paid_for(self):
        # THE NUMBERS ARE LITERAL ON PURPOSE. Restating them as
        # `FULL_CHARS - MARKER_CHARS` would let an implementation that never
        # subtracted anything still agree with the assertion.
        measured = measure_dedupe_savings_from_traces(
            [self._full_entry(), self._deduped_entry()],
        )

        assert measured.unmeasured_segment_names == ()
        assert measured.chars_avoided == 1200
        assert measured.chars_spent_on_markers == 40
        assert measured.net_chars_saved == 1160
        assert measured.deduped_occurrences_counted == 1

    # -- SPEC H case 4: unmeasured is NOT zero -------------------------------

    def test_a_deduped_name_with_no_observed_full_size_is_unmeasured_not_zero(self):
        # BOTH HALVES ARE ASSERTED, and the naming first. A function that simply
        # returned zeroes would satisfy the totals alone, so the totals are
        # evidence of nothing without the name that explains them.
        measured = measure_dedupe_savings_from_traces([self._deduped_entry()])

        assert measured.unmeasured_segment_names == (self.NAME,)
        assert measured.deduped_occurrences_counted == 0
        assert measured.chars_avoided == 0
        assert measured.chars_spent_on_markers == 0
        assert measured.net_chars_saved == 0

    # -- SPEC H case 5: roles do not cross -----------------------------------

    def test_one_roles_full_send_does_not_size_the_other_roles_dedupe(self):
        # THE SCOPE RULE, READ THROUGH THE TRACE. What the Builder session was
        # sent proves nothing about what the Reviewer session holds, so the
        # Reviewer's withheld name is UNMEASURED rather than measured against
        # the wrong session's number.
        crossed = measure_dedupe_savings_from_traces(
            [self._full_entry("builder"), self._deduped_entry("reviewer")],
        )

        assert crossed.unmeasured_segment_names == (self.NAME,)
        assert crossed.deduped_occurrences_counted == 0
        assert crossed.chars_avoided == 0
        assert crossed.chars_spent_on_markers == 0
        assert crossed.net_chars_saved == 0

        # THE DISCRIMINATOR: the very same pair on ONE role measures cleanly, so
        # the reading above is about the role boundary and not about these two
        # entries being unusable.
        same_role = measure_dedupe_savings_from_traces(
            [self._full_entry("reviewer"), self._deduped_entry("reviewer")],
        )

        assert same_role.unmeasured_segment_names == ()
        assert same_role.deduped_occurrences_counted == 1
        assert same_role.net_chars_saved == 1160


# ---------------------------------------------------------------------------
# Step 5088: next_approve_command unit tests
# ---------------------------------------------------------------------------


class TestNextApproveCommand:
    def test_ready_promote_emits_command(self):
        from apps.cli.commands.do_cmd import _build_next_approve_command
        cmd = _build_next_approve_command("job123", "/repo", None, True)
        assert "job123" in cmd
        assert "--approve" in cmd
        assert "--repo" in cmd

    def test_blocked_promote_emits_empty(self):
        from apps.cli.commands.do_cmd import _build_next_approve_command
        cmd = _build_next_approve_command("job123", "/repo", None, False)
        assert cmd == ""

    def test_includes_test_command(self):
        from apps.cli.commands.do_cmd import _build_next_approve_command
        cmd = _build_next_approve_command("job123", "/repo", "pytest -q", True)
        assert "--test-command" in cmd
        assert "pytest" in cmd

    def test_shell_quotes_spaces(self):
        from apps.cli.commands.do_cmd import _build_next_approve_command
        cmd = _build_next_approve_command("j1", "/my repo", "pytest tests/my test.py", True)
        assert "'/my repo'" in cmd or '"/my repo"' in cmd or "my\\ repo" in cmd
        assert "--test-command" in cmd

    def test_shell_quotes_single_quotes(self):
        from apps.cli.commands.do_cmd import _build_next_approve_command
        cmd = _build_next_approve_command("j1", "/repo", "echo 'hello'", True)
        assert "--test-command" in cmd
        assert "echo" in cmd


# ---------------------------------------------------------------------------
# Step 5089: Timeout hint tests
# ---------------------------------------------------------------------------


class TestTimeoutHint:
    def test_claude_cli_below_900_warns(self):
        from apps.cli.commands.do_cmd import _build_timeout_hint
        warning = _build_timeout_hint("claude-cli", "fake", 180)
        assert warning
        assert "900" in warning

    def test_claude_cli_reviewer_below_900_warns(self):
        from apps.cli.commands.do_cmd import _build_timeout_hint
        warning = _build_timeout_hint("fake", "claude-cli", 120)
        assert warning
        assert "900" in warning

    def test_fake_no_warning(self):
        from apps.cli.commands.do_cmd import _build_timeout_hint
        warning = _build_timeout_hint("fake", "fake", 120)
        assert warning == ""

    def test_claude_cli_at_900_no_warning(self):
        from apps.cli.commands.do_cmd import _build_timeout_hint
        warning = _build_timeout_hint("claude-cli", "claude-cli", 900)
        assert warning == ""

    def test_claude_cli_above_900_no_warning(self):
        from apps.cli.commands.do_cmd import _build_timeout_hint
        warning = _build_timeout_hint("claude-cli", "claude-cli", 1200)
        assert warning == ""
