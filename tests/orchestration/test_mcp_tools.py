"""F303 R5 C3 — `packages/orchestration/mcp_tools`, the three tools of Remedy's MCP server
(DECISION F303 D5).

The tools are driven with a fake `run` that records each argument list it is given and answers a
chosen envelope, so no child starts; `run_remedy_json` itself is driven by a real child, over
commands that touch no model and no network.
"""
from __future__ import annotations

import pytest

from packages.orchestration.mcp_tools import (
    MCP_TOOL_NAMES,
    remedy_mcp_tools,
    run_remedy_json,
)


class _FakeRun:
    def __init__(self, answer):
        self.answer = answer
        self.calls: list[list[str]] = []

    def __call__(self, argv):
        self.calls.append(list(argv))
        return self.answer


def _tool(name: str, run) -> object:
    return {tool.name: tool for tool in remedy_mcp_tools(run=run)}[name]


def test_each_tool_runs_exactly_its_twin_command():
    run = _FakeRun({"ok": True})
    _tool("verify", run).call({"bundle": "b.zip"})
    _tool("gate_status", run).call({"job": "job-1"})
    _tool("evidence_bundle", run).call({"job": "job-2"})
    _tool("evidence_bundle", run).call({"job": "job-3", "out": "/tmp/x.zip"})
    assert run.calls == [
        ["verify", "run", "--json", "--", "b.zip"],
        ["client", "story", "--json", "--", "job-1"],
        ["job", "certificate", "--json", "--", "job-2"],
        ["job", "certificate", "--out=/tmp/x.zip", "--json", "--", "job-3"],
    ]


def test_gate_status_keeps_only_its_four_keys_of_an_ok_story():
    story = {"ok": True, "job_id": "j", "state": "done", "state_detail": "all green",
             "verification": {"checks": []}, "next_safe_action": "none", "extra": 1}
    answer = _tool("gate_status", _FakeRun(story)).call({"job": "j"})
    assert answer == {"job_id": "j", "state": "done", "state_detail": "all green",
                      "verification": {"checks": []}}


def test_gate_status_passes_a_refusal_through_unchanged():
    refusal = {"ok": False, "error": "job_not_found", "message": "no such job"}
    assert _tool("gate_status", _FakeRun(refusal)).call({"job": "j"}) == refusal


@pytest.mark.parametrize("name,arguments", [("verify", {"bundle": "b"}),
                                            ("evidence_bundle", {"job": "j"})])
def test_verify_and_evidence_bundle_answer_the_twins_envelope_unchanged(name, arguments):
    envelope = {"ok": True, "anything": [1, 2], "nested": {"a": None}}
    assert _tool(name, _FakeRun(envelope)).call(arguments) == envelope
    refusal = {"ok": False, "error": "x", "message": "y"}
    assert _tool(name, _FakeRun(refusal)).call(arguments) == refusal


@pytest.mark.parametrize("name,arguments", [
    ("verify", {}), ("verify", {"bundle": ""}), ("verify", {"bundle": 7}),
    ("verify", {"bundle": ["b"]}), ("verify", {"job": "j"}),
    ("gate_status", {}), ("gate_status", {"job": ""}), ("gate_status", {"job": None}),
    ("evidence_bundle", {}), ("evidence_bundle", {"job": ""}), ("evidence_bundle", {"job": 3}),
    ("evidence_bundle", {"job": "j", "out": ""}), ("evidence_bundle", {"job": "j", "out": 5}),
    ("evidence_bundle", {"job": "j", "out": ["p"]}),
])
def test_a_missing_empty_or_non_string_argument_is_refused_with_no_run(name, arguments):
    run = _FakeRun({"ok": True})
    answer = _tool(name, run).call(arguments)
    assert answer["ok"] is False
    assert answer["error"] == "invalid_argument"
    assert run.calls == []


def test_the_tools_are_sorted_and_each_input_schema_is_closed():
    tools = remedy_mcp_tools(run=_FakeRun({"ok": True}))
    assert [tool.name for tool in tools] == list(MCP_TOOL_NAMES) == sorted(MCP_TOOL_NAMES)
    required = {"evidence_bundle": ["job"], "gate_status": ["job"], "verify": ["bundle"]}
    for tool in tools:
        assert tool.description.strip()
        assert tool.input_schema["type"] == "object"
        assert tool.input_schema["additionalProperties"] is False
        assert tool.input_schema["required"] == required[tool.name]
        assert set(tool.input_schema["required"]) <= set(tool.input_schema["properties"])
    evidence = {tool.name: tool for tool in tools}["evidence_bundle"]
    assert set(evidence.input_schema["properties"]) == {"job", "out"}


def test_run_remedy_json_answers_the_envelope_a_real_child_prints():
    answer = run_remedy_json(["client", "interface", "--json"])
    assert answer["ok"] is True


def test_run_remedy_json_answers_mcp_tool_failed_when_the_child_prints_no_envelope():
    answer = run_remedy_json(["--no-such-flag-at-all"])
    assert answer["ok"] is False
    assert answer["error"] == "mcp_tool_failed"
    assert "no envelope" in answer["message"]


def test_run_remedy_json_answers_mcp_tool_failed_naming_the_timeout():
    answer = run_remedy_json(["client", "interface", "--json"], timeout=0.001)
    assert answer["ok"] is False
    assert answer["error"] == "mcp_tool_failed"
    assert "outlived" in answer["message"]
