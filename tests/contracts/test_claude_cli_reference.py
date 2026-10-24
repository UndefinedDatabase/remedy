"""F151 T003: the claude-cli reference adapter's goldens and its kit run (DECISION F151 D4).

Every adapter here is built with ``config={}``, so no test reads this machine's own
configuration. The goldens compare the adapter against the EXISTING claude-cli functions it
wraps — ``build_claude_cli_args``, ``parse_cli_result_detailed``, ``capture_stream_evidence``
and the shared error predicates `_classify_error_text` asks — never against a second,
independently re-derived notion of what the claude-cli path does.
"""
from __future__ import annotations

import dataclasses
import json
from pathlib import Path

import pytest

from packages.contracts.adapter_conformance_kit import (
    AdapterSamples,
    ErrorSample,
    run_adapter_conformance,
)
from packages.contracts.adapter_contract import AdapterCapabilities, InvocationOptions, WorkerIsolation
from packages.orchestration.claude_cli_command import build_claude_cli_args
from packages.orchestration.failure_postmortem import FailureClass, _classify_error_text
from packages.orchestration.provider_names import ROLE_PROVIDER_NAMES
from packages.orchestration.schemas import ReviewVerdict, to_json_schema, to_json_schema_str
from packages.orchestration.stream_evidence import (
    EVENT_MALFORMED,
    capture_stream_evidence,
    read_run_events,
)
from packages.orchestration.token_actuals import parse_cli_result_detailed
from packages.providers.adapters.claude_cli_reference import (
    ClaudeCliReferenceAdapter,
    classify_claude_cli_error,
)

_FIXTURES_DIR = Path(__file__).resolve().parents[1] / "orchestration" / "fixtures" / "stream"
_STREAM_FIXTURES = sorted(_FIXTURES_DIR.glob("*.jsonl"))

_REVIEW_VERDICT_SCHEMA = to_json_schema(ReviewVerdict)
_REVIEW_VERDICT_SCHEMA_STR = to_json_schema_str(ReviewVerdict)

_ONE_PART_PROMPT = ("Summarize the attached diff in one paragraph.",)
_TWO_PART_PROMPT = (
    "Summarize the attached diff in one paragraph.", "List every file the change touches.")


def _adapter(**kwargs) -> ClaudeCliReferenceAdapter:
    """Every adapter this file builds, always with config={} (no machine configuration read)."""
    kwargs.setdefault("config", {})
    return ClaudeCliReferenceAdapter(**kwargs)


# -- adapter_id is a real provider name ----------------------------------------------


def test_adapter_id_is_a_role_provider_name():
    assert _adapter().adapter_id in ROLE_PROVIDER_NAMES


# -- isolation(): DECISION F152 D3 (2)'s exact declaration, spelled here independently ---------


def test_isolation_equals_decision_f152_d3_2_exactly():
    assert _adapter().isolation() == WorkerIsolation(
        method="tool_flag",
        adr_ref="docs/adr/0002-claude-cli-worker-isolation.md",
        tool_args=("--setting-sources", "project,local", "--strict-mcp-config"),
        env_allowlist=(
            "HOME", "LANG", "LC_ALL", "LC_CTYPE", "LOGNAME", "PATH", "SHELL", "TERM", "TMPDIR",
            "TZ", "USER", "ANTHROPIC_API_KEY", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
            "NO_PROXY", "http_proxy", "https_proxy", "all_proxy", "no_proxy",
        ),
        applies=True,
    )


def test_isolation_does_not_apply_with_customizations_but_is_otherwise_equal():
    plain = _adapter().isolation()
    customized = _adapter(config={"claude_cli.customizations": True}).isolation()
    assert customized.applies is False
    assert dataclasses.replace(customized, applies=True) == plain


# -- the kit: run_adapter_conformance reads () for a streaming and a non-streaming adapter ----


def test_streaming_adapter_passes_every_kit_dimension():
    adapter = _adapter(streaming=True)
    lines = tuple((_FIXTURES_DIR / "basic_session.jsonl").read_text(encoding="utf-8").splitlines())
    usage_line = lines[-1]
    samples = AdapterSamples(
        model="claude-test-model",
        stream_lines=lines,
        expected_stream_events=adapter.map_stream(lines),
        usage_raw=usage_line,
        expected_usage=adapter.map_usage(usage_line),
        error_samples=(
            ErrorSample(
                "claude CLI not found on PATH. Install Claude Code CLI to use "
                "--builder-provider claude-cli or --reviewer-provider claude-cli.",
                None, FailureClass.PROVIDER_UNAVAILABLE),
            ErrorSample("claude CLI timed out after 1s", None, FailureClass.PROVIDER_TIMEOUT),
            ErrorSample("claude CLI exited 1: boom", None, FailureClass.PROVIDER_NONZERO_EXIT),
        ),
    )
    assert run_adapter_conformance(adapter, samples) == ()


def test_non_streaming_adapter_passes_every_kit_dimension():
    adapter = _adapter(streaming=False)
    samples = AdapterSamples(
        model="claude-test-model",
        stream_lines=(), expected_stream_events=(),
        usage_raw="", expected_usage=None,
        error_samples=(
            ErrorSample(
                "claude CLI not found on PATH. Install Claude Code CLI to use "
                "--builder-provider claude-cli or --reviewer-provider claude-cli.",
                None, FailureClass.PROVIDER_UNAVAILABLE),
            ErrorSample("claude CLI timed out after 1s", None, FailureClass.PROVIDER_TIMEOUT),
        ),
    )
    assert run_adapter_conformance(adapter, samples) == ()


# -- invocation goldens: argv equals build_claude_cli_args for every role/model/schema/resume --


@pytest.mark.parametrize("role", ("builder", "reviewer"))
@pytest.mark.parametrize("model", ("", "claude-workhorse"))
@pytest.mark.parametrize("with_schema", (False, True), ids=("no-schema", "with-schema"))
@pytest.mark.parametrize("with_resume", (False, True), ids=("no-resume", "with-resume"))
def test_build_invocation_argv_matches_build_claude_cli_args(role, model, with_schema, with_resume):
    adapter = _adapter(claude_path="claude", write_mode="allowed-tools", streaming=True)
    options = InvocationOptions(
        model=model,
        output_schema=_REVIEW_VERDICT_SCHEMA if with_schema else None,
        resume_ref="sess-resume-1" if with_resume else None,
    )
    invocation = adapter.build_invocation(role, _ONE_PART_PROMPT, options)

    expected_write_mode = "allowed-tools" if role == "builder" else "none"
    expected_json_schema = _REVIEW_VERDICT_SCHEMA_STR if with_schema else ""
    expected_resume = "sess-resume-1" if with_resume else ""
    expected_argv = tuple(build_claude_cli_args(
        "claude", _ONE_PART_PROMPT[0],
        write_mode=expected_write_mode, model=model, stream_evidence=True,
        json_schema=expected_json_schema, resume_session=expected_resume, config={},
    )) + ("--setting-sources", "project,local", "--strict-mcp-config")
    assert invocation.argv == expected_argv
    if with_schema:
        assert "--json-schema" in invocation.argv
        idx = invocation.argv.index("--json-schema")
        assert invocation.argv[idx + 1] == _REVIEW_VERDICT_SCHEMA_STR


def test_build_invocation_joins_a_two_part_prompt_with_a_blank_line():
    adapter = _adapter(streaming=False)
    options = InvocationOptions(model="claude-workhorse")
    invocation = adapter.build_invocation("builder", _TWO_PART_PROMPT, options)
    assert invocation.argv[2] == "\n\n".join(_TWO_PART_PROMPT)


def test_build_invocation_raises_for_a_role_outside_builder_or_reviewer():
    adapter = _adapter()
    options = InvocationOptions(model="claude-workhorse")
    with pytest.raises(ValueError):
        adapter.build_invocation("planner", _ONE_PART_PROMPT, options)


def test_build_invocation_with_customizations_matches_build_claude_cli_args_without_safe_mode():
    # R-1438 (9): the adapter's configuration must reach build_claude_cli_args unchanged, so a
    # configuration that turns customizations on yields an argv the shared builder also yields
    # for that same configuration, and --safe-mode is absent from it.
    config = {"claude_cli.customizations": True}
    adapter = _adapter(claude_path="claude", write_mode="allowed-tools", streaming=True, config=config)
    options = InvocationOptions(model="claude-workhorse")
    invocation = adapter.build_invocation("builder", _ONE_PART_PROMPT, options)

    expected_argv = tuple(build_claude_cli_args(
        "claude", _ONE_PART_PROMPT[0],
        write_mode="allowed-tools", model="claude-workhorse", stream_evidence=True,
        json_schema="", resume_session="", config=config,
    ))
    assert invocation.argv == expected_argv
    assert "--safe-mode" not in invocation.argv


# -- stream goldens: map_stream equals capture_stream_evidence's own normalized events --------

#: Keys `capture_stream_evidence` adds that `normalize_stream_object` itself never produces: the
#: byte backreference triple (per-call capture evidence, DECISION F151 D2 (2)), the schema
#: version, and the capture-wide event sequence counter. None of the three is part of what an
#: adapter maps; stripping them is the only difference between the two event lists.
_CAPTURE_ONLY_KEYS = ("raw_line_number", "raw_byte_offset", "raw_byte_length", "schema_version", "seq")


def _without_capture_only_keys(event: dict) -> dict:
    return {k: v for k, v in event.items() if k not in _CAPTURE_ONLY_KEYS}


@pytest.mark.parametrize("fixture_path", _STREAM_FIXTURES, ids=[p.name for p in _STREAM_FIXTURES])
def test_map_stream_equals_capture_stream_evidence_for_every_fixture(fixture_path, tmp_path):
    lines = tuple(fixture_path.read_text(encoding="utf-8").splitlines())
    capture_stream_evidence(lines, tmp_path / fixture_path.stem)
    captured = read_run_events(tmp_path / fixture_path.stem / "run_events.jsonl")
    captured_events = tuple(
        _without_capture_only_keys(e) for e in captured if e.get("event_type") != EVENT_MALFORMED)
    adapter = _adapter(streaming=True)
    assert adapter.map_stream(lines) == captured_events


@pytest.mark.parametrize("fixture_path", _STREAM_FIXTURES, ids=[p.name for p in _STREAM_FIXTURES])
def test_a_non_streaming_adapter_maps_every_fixture_to_no_events(fixture_path):
    lines = tuple(fixture_path.read_text(encoding="utf-8").splitlines())
    adapter = _adapter(streaming=False)
    assert adapter.map_stream(lines) == ()


def test_map_stream_never_leaks_the_secrets_canary_text():
    fixture_path = _FIXTURES_DIR / "secrets_canary.jsonl"
    lines = tuple(fixture_path.read_text(encoding="utf-8").splitlines())
    adapter = _adapter(streaming=True)
    blob = json.dumps(adapter.map_stream(lines))
    for secret in (
        "sk-ant-api03-CANARYONEDEADBEEF0123456789",
        "CANARYTWOsecretvalue123",
        "CANARYTHREEabcdefghijklmnop",
        "ghp_CANARYFOUR1234567890abcdefghij123456",
    ):
        assert secret not in blob


# -- usage goldens: map_usage equals parse_cli_result_detailed, raw_counters echo the envelope --


def _result_lines_with_usage() -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for fixture_path in _STREAM_FIXTURES:
        for line in fixture_path.read_text(encoding="utf-8").splitlines():
            try:
                obj = json.loads(line)
            except (ValueError, TypeError):
                continue
            if isinstance(obj, dict) and obj.get("type") == "result" and isinstance(obj.get("usage"), dict):
                found.append((fixture_path.name, line))
    return found


_RESULT_LINES_WITH_USAGE = _result_lines_with_usage()


@pytest.mark.parametrize(
    "fixture_name,line", _RESULT_LINES_WITH_USAGE, ids=[n for n, _ in _RESULT_LINES_WITH_USAGE])
def test_map_usage_matches_parse_cli_result_detailed_for_every_recorded_usage(fixture_name, line):
    adapter = _adapter()
    mapped = adapter.map_usage(line)
    actuals, _reason = parse_cli_result_detailed(line)
    assert mapped is not None
    assert mapped.actuals == actuals
    assert mapped.raw_counters == json.loads(line)["usage"]


def test_map_usage_is_none_for_an_is_error_result():
    # retry_and_error.jsonl's own recorded result line: is_error true, no usage block.
    retry_fixture = _FIXTURES_DIR / "retry_and_error.jsonl"
    result_line = retry_fixture.read_text(encoding="utf-8").splitlines()[-1]
    assert json.loads(result_line)["is_error"] is True
    assert _adapter().map_usage(result_line) is None


def test_map_usage_is_none_for_an_empty_string():
    assert _adapter().map_usage("") is None


def test_map_usage_is_none_for_a_non_json_string():
    assert _adapter().map_usage("not a json string at all") is None


def test_map_usage_is_none_for_an_is_error_result_with_a_usage_object_added():
    # R-1438 (10): the parser's own None must not be overridden just because a usage object is
    # present — an is_error envelope stays None even when it carries usage, because
    # parse_cli_result_detailed itself reads is_error first.
    retry_fixture = _FIXTURES_DIR / "retry_and_error.jsonl"
    result_line = retry_fixture.read_text(encoding="utf-8").splitlines()[-1]
    payload = json.loads(result_line)
    assert payload["is_error"] is True
    payload["usage"] = {"input_tokens": 1, "output_tokens": 1}
    augmented_line = json.dumps(payload)
    actuals, _reason = parse_cli_result_detailed(augmented_line)
    assert actuals is None
    assert _adapter().map_usage(augmented_line) is None


# -- capabilities golden: the whole record equals DECISION F151 D4 (6), for both streaming flags --


@pytest.mark.parametrize("streaming", (True, False))
def test_capabilities_equals_decision_f151_d4_6_whole(streaming):
    adapter = _adapter(streaming=streaming)
    assert adapter.capabilities("any-model") == AdapterCapabilities(
        vision=False, json_schema=True, session_resume=True,
        streaming=streaming, tool_use=True, max_context_tokens=0)


# -- error goldens: classify_error matches what D4 (5) derives from _classify_error_text ------


def _expected_claude_cli_class(error_text: str, exit_code: int | None) -> FailureClass:
    """D4 (5)'s own derivation, restated here independently of the module under test."""
    if error_text.startswith("malformed_output:"):
        return FailureClass.PARSE
    from_text = _classify_error_text(error_text)
    if from_text in (
        FailureClass.PROVIDER_UNAVAILABLE, FailureClass.PROVIDER_TIMEOUT,
        FailureClass.PROVIDER_NONZERO_EXIT,
    ):
        return from_text
    if exit_code not in (None, 0):
        return FailureClass.PROVIDER_NONZERO_EXIT
    return FailureClass.UNKNOWN


#: Every distinct `raise` message `ClaudeCliProvider` carries (packages/orchestration/
#: pingpong_provider.py), copied literally with a number standing in for each placeholder, plus
#: a missing binary (the first entry, also a real raise message), a refused connection and a
#: message beginning `malformed_output:`.
_CLAUDE_CLI_ERROR_TEXTS = (
    "claude CLI not found on PATH. Install Claude Code CLI to use "
    "--builder-provider claude-cli or --reviewer-provider claude-cli.",
    "stream evidence enabled but no stream_evidence_dir was provided",
    "claude CLI timed out after 1s",
    "stream evidence cap reached after 1 bytes; provider terminated before completion",
    "claude CLI exited 1: 1",
    "claude CLI stream reported an error: 1",
    "claude CLI reported is_error=true",
    "claude CLI stream reported an error (1): 1",
    "connection refused",
    "malformed_output: invalid JSON",
)


@pytest.mark.parametrize("error_text", _CLAUDE_CLI_ERROR_TEXTS)
def test_classify_error_matches_its_derivation_for_every_claude_cli_message(error_text):
    adapter = _adapter()
    assert adapter.classify_error(error_text, None) == _expected_claude_cli_class(error_text, None)
    assert classify_claude_cli_error(error_text, None) == _expected_claude_cli_class(error_text, None)


def test_a_text_no_predicate_reads_maps_to_non_zero_exit_with_an_exit_code():
    text = "this sentence matches no predicate at all"
    assert _expected_claude_cli_class(text, 2) == FailureClass.PROVIDER_NONZERO_EXIT
    assert classify_claude_cli_error(text, 2) == FailureClass.PROVIDER_NONZERO_EXIT


def test_a_text_no_predicate_reads_maps_to_unknown_with_no_exit_code():
    text = "this sentence matches no predicate at all"
    assert _expected_claude_cli_class(text, None) == FailureClass.UNKNOWN
    assert classify_claude_cli_error(text, None) == FailureClass.UNKNOWN


# -- R-1438 (1)-(3): the three numbered classify_claude_cli_error mutations, each a direct test --


def test_a_malformed_output_text_that_also_names_a_timeout_maps_to_parse():
    # R-1438 (1): the malformed_output: check must run BEFORE the shared predicates, not after,
    # or a message that also matches is_timeout_error would be misread as a provider timeout.
    text = "malformed_output: claude CLI timed out after 1s"
    assert classify_claude_cli_error(text, None) == FailureClass.PARSE


def test_an_io_failure_text_maps_to_unknown_not_the_io_class():
    # R-1438 (2): a text the I/O predicate reads must still fold to unknown, an adapter may not
    # return the I/O class itself. "no space left on device" is read only by is_io_failure_error
    # (unlike "broken pipe", which the connection predicate also reads and classifies earlier).
    text = "write failed: no space left on device"
    assert _classify_error_text(text) == FailureClass.IO_FAILURE
    assert classify_claude_cli_error(text, None) == FailureClass.UNKNOWN


def test_an_unread_text_with_exit_code_zero_maps_to_unknown():
    # R-1438 (3): exit code 0 must never count as a non-zero exit.
    text = "this sentence matches no predicate at all"
    assert classify_claude_cli_error(text, 0) == FailureClass.UNKNOWN
