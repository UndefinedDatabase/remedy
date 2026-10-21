"""The Pi provider (operator amendment amend1014b, DECISION D1 to D4), against a fake `pi` executable.

The fake records its argv, working directory, environment and agent files, can edit a file in its
cwd the way the real harness does, and prints a scripted JSONL stream. It runs inside the real tool
sandbox (DECISION amend1016sb D1), where its own directory is read-only, so it records the call
into the workspace. No test reaches a real Ollama or Pi.
"""
from __future__ import annotations

import json
import os
import stat
import textwrap
from pathlib import Path
from types import SimpleNamespace

import pytest

import packages.orchestration.pi_provider as PP
from packages.orchestration.model_aliases import resolve_model_alias
from packages.orchestration.pi_provider import (
    PI_BUILDER_TOOLS,
    PI_DEFAULT_MODEL,
    PI_REVIEWER_TOOLS,
    PiProvider,
    PiUnavailable,
    build_pi_argv,
    default_chain_checks,
    make_pi_provider,
)

_FAKE_PI = textwrap.dedent('''\
    #!/usr/bin/env python3
    import json, os, sys, time
    here = os.path.dirname(os.path.abspath(__file__))
    if sys.argv[1:] == ["--version"]:
        print("9.9.9"); sys.exit(0)
    beh = json.load(open(os.path.join(here, "behavior.json")))
    agent = os.environ.get("PI_CODING_AGENT_DIR", "")
    files = {n: open(os.path.join(agent, n)).read() for n in ("models.json", "settings.json")
             if agent and os.path.exists(os.path.join(agent, n))}
    json.dump({"argv": sys.argv[1:], "cwd": os.getcwd(), "env": dict(os.environ), "pid": os.getpid(),
               "agent_files": files}, open(os.path.join(os.getcwd(), ".fake-pi-call.json"), "w"))
    for rel, text in beh.get("edits", {}).items():
        with open(os.path.join(os.getcwd(), rel), "a") as fh:
            fh.write(text)
    out = sys.stdout.buffer
    for line in beh.get("stdout", []):
        out.write(line.encode("utf-8")); out.flush()
    sys.stderr.write(beh.get("stderr", ""))
    time.sleep(beh.get("sleep", 0))
    sys.exit(beh.get("exit", 0))
''')


def _event(event: dict) -> str:
    return json.dumps(event) + "\n"


def good_stream(text: str = "done", *, turns: int = 2) -> list[str]:
    lines = [_event({"type": "agent_start"})]
    for n in range(turns):
        last = n == turns - 1
        lines.append(_event({"type": "message_end", "message": {
            "role": "assistant", "provider": "ollama", "model": PI_DEFAULT_MODEL,
            "content": [{"type": "text", "text": text if last else ""}],
            "stopReason": "stop" if last else "toolUse",
            "usage": {"input": 100, "output": 10, "cacheRead": 0, "cacheWrite": 0,
                      "totalTokens": 110}}}))
        if not last:
            lines += [_event({"type": "tool_execution_start", "toolName": "edit"}),
                      _event({"type": "tool_execution_end", "toolName": "edit", "isError": False})]
    return lines + [_event({"type": "agent_end", "messages": [], "willRetry": False}),
                    _event({"type": "agent_settled", "aborted": False})]


class FakePi:
    def __init__(self, directory: Path, workspace: Path) -> None:
        self.dir = directory
        self.workspace = workspace

    def behave(self, **behavior) -> None:
        (self.dir / "behavior.json").write_text(json.dumps(behavior))

    def call(self) -> dict:
        return json.loads((self.workspace / ".fake-pi-call.json").read_text())


@pytest.fixture
def fake_pi(tmp_path, monkeypatch) -> FakePi:
    bindir = tmp_path / "bin"
    bindir.mkdir()
    exe = bindir / "pi"
    exe.write_text(_FAKE_PI)
    exe.chmod(exe.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("PATH", f"{bindir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("OPENAI_API_KEY", "must-not-reach-pi")
    fake = FakePi(bindir, tmp_path / "job-workspace")
    fake.behave(stdout=good_stream())
    return fake


@pytest.fixture
def workspace(tmp_path) -> Path:
    ws = tmp_path / "job-workspace"
    ws.mkdir()
    (ws / "README.md").write_text("# Test\n")
    return ws


# --- 1. the command contract ----------------------------------------------------------------

def test_builder_argv_cwd_and_environment_follow_the_contract(fake_pi, workspace, tmp_path):
    out = PiProvider(role="builder", cwd=str(workspace)).build("add a paragraph")
    assert not out.error
    call = fake_pi.call()
    argv = call["argv"]
    assert argv[:2] == ["--mode", "json"] and "--no-session" in argv
    assert argv[argv.index("--provider") + 1] == "ollama"
    assert argv[argv.index("--model") + 1] == "muse-glimmer:latest"
    assert argv[argv.index("--tools") + 1] == PI_BUILDER_TOOLS == "read,bash,edit,write,grep,find,ls"
    for flag in ("--offline", "--no-approve", "--no-extensions", "--no-mcp", "--no-skills",
                 "--no-prompt-templates", "--no-themes", "--no-context-files"):
        assert flag in argv
    assert argv[-2] == "--" and "add a paragraph" in argv[-1]
    assert Path(call["cwd"]).resolve() == workspace.resolve()
    env = call["env"]
    assert env["PI_CODING_AGENT_DIR"] == "/run/remedy/agent" and env["HOME"] == "/tmp/home"
    assert env["PI_OFFLINE"] == "1" and "OPENAI_API_KEY" not in env
    assert not (tmp_path / "data").exists() or "data" not in os.listdir(tmp_path / "data")


def test_the_agent_directory_points_pi_at_the_relay_and_the_tool_shell(fake_pi, workspace, monkeypatch):
    monkeypatch.setenv("REMEDY_OLLAMA_HOST", "http://gpu-box:11434/")
    assert not PiProvider(role="builder", cwd=str(workspace)).build("x").error
    files = fake_pi.call()["agent_files"]
    entry = json.loads(files["models.json"])["providers"]["ollama"]
    # The sandbox never learns the real endpoint: Pi talks to the relay port inside it.
    assert entry["baseUrl"] == "http://127.0.0.1:11434/v1" and entry["apiKey"] == "ollama"
    assert "gpu-box" not in files["models.json"]
    assert [m["id"] for m in entry["models"]] == ["muse-glimmer:latest"]
    assert entry["models"][0]["cost"] == {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0}
    assert json.loads(files["settings.json"]) == {"shellPath": "/run/remedy/tool-shell.sh"}


# --- 2. the reviewer is read-only -----------------------------------------------------------

def test_the_reviewer_gets_only_the_read_tools_and_every_resource_switch(fake_pi, workspace):
    fake_pi.behave(stdout=good_stream('{"verdict":"pass","findings":[],"confidence":"high","summary":"ok"}'))
    out = PiProvider(role="reviewer", cwd=str(workspace)).review("judge this diff")
    assert out.verdict == "pass" and not out.error and out.provider == "pi"
    argv = fake_pi.call()["argv"]
    tools = argv[argv.index("--tools") + 1]
    assert tools == PI_REVIEWER_TOOLS == "read,grep,find,ls"
    assert not {"bash", "edit", "write"} & set(tools.split(","))
    for flag in ("--no-extensions", "--no-mcp", "--no-skills", "--no-prompt-templates"):
        assert flag in argv


def test_the_reviewer_is_asked_for_the_requested_meaning_and_to_fail_extra_files(fake_pi, workspace):
    """amend1016p D3: a change in the right file with the wrong wording, or with a report file
    beside it, must fail review."""
    fake_pi.behave(stdout=good_stream('{"verdict":"pass","findings":[],"confidence":"high","summary":"ok"}'))
    PiProvider(role="reviewer", cwd=str(workspace)).review("judge this diff")
    prompt = fake_pi.call()["argv"][-1]
    assert "content and meaning" in prompt and "fail any file the task does not ask for" in prompt


def test_repair_roles_use_the_tools_of_their_kind():
    assert PP.pi_role_tools("repair") == PI_BUILDER_TOOLS
    assert PP.pi_role_tools("reviewer") == PI_REVIEWER_TOOLS
    assert PP.pi_role_tools("final_verifier") == PI_REVIEWER_TOOLS
    argv = build_pi_argv("/x/pi", model="m", tools="read", prompt="p")
    assert argv[0] == "/x/pi" and isinstance(argv, list)


# --- 3 (provider half). usage, turns and evidence -------------------------------------------

def test_every_model_turn_is_counted_and_the_evidence_names_the_chain(fake_pi, workspace):
    provider = PiProvider(role="builder", cwd=str(workspace))
    out = provider.build("x")
    assert out.usage_actuals["model_turns"] == 2 and out.tokens_used == 220
    assert out.usage_actuals["input_tokens"] == 200
    ev = provider.last_evidence
    assert (ev["provider"], ev["inner_provider"], ev["model"]) == ("pi", "ollama", "muse-glimmer:latest")
    assert ev["pi_version"] == "9.9.9" and ev["tool_calls"] == ["edit"] and ev["exit_code"] == 0
    assert out.files_changed == [] and out.prepared_input.mode == "pi-json"


# --- 3b. the worker pulse (DECISION F311 D2) -------------------------------------------------

@pytest.fixture
def _no_pulse_leak():
    """Reset the worker pulse's binding ContextVar before and after a test.

    `_CURRENT_PULSE` is process-wide state set by `bind_worker_pulse`; without a reset here a
    pulse bound by one test would still be current when the next, unrelated test calls a
    provider in the same worker process.
    """
    from packages.orchestration import worker_pulse as WP
    token = WP._CURRENT_PULSE.set(None)
    yield
    WP._CURRENT_PULSE.reset(token)


def test_a_bound_worker_pulse_records_the_call_s_role_round_and_stream(fake_pi, workspace, _no_pulse_leak):
    from packages.orchestration import data_paths
    from packages.orchestration.worker_pulse import bind_worker_pulse, read_worker_pulse

    data_paths.job_dir("job-with-pulse").mkdir(parents=True, exist_ok=True)
    fake_pi.behave(stdout=[
        _event({"type": "tool_execution_start", "toolName": "edit"}),
        _event({"type": "tool_execution_end", "toolName": "edit", "isError": False}),
        _event({"type": "message_end", "message": {
            "role": "assistant", "content": [{"type": "text", "text": "done"}], "stopReason": "stop",
            "usage": {"input": 10, "output": 5, "cacheRead": 0, "cacheWrite": 0, "totalTokens": 15}}}),
    ])
    bind_worker_pulse(SimpleNamespace(job_id="job-with-pulse"))
    provider = PiProvider(role="builder", cwd=str(workspace))
    provider.begin_stream_call(2, "attempt")

    provider.build("x")

    pulse = read_worker_pulse("job-with-pulse")
    assert (pulse["role"], pulse["provider"], pulse["model"], pulse["round"]) == (
        "builder", "pi", PI_DEFAULT_MODEL, 2)
    assert pulse["call_ended_at"] is not None
    assert [entry["kind"] for entry in pulse["stream"]] == ["tool_call", "tool_result", "model_text"]


def test_with_no_pulse_bound_no_worker_pulse_file_is_written(fake_pi, workspace, tmp_path, _no_pulse_leak):
    PiProvider(role="builder", cwd=str(workspace)).build("x")

    assert not list((tmp_path / "data").rglob("worker_pulse.json"))


# --- 4. failures ----------------------------------------------------------------------------

# The last column: the input tokens the failed call's stream measured before it ended, which count
# against the budgets, or None when the stream reported none (never recorded as a measured zero).
@pytest.mark.parametrize("behavior, fragment, measured_input", [
    ({"stdout": good_stream()[:-1]}, "pi_unsettled", 200),
    ({"stdout": good_stream()[:-1] + ['{"type":"agent_settled","abor']}, "pi_malformed_stream", 200),
    ({"stdout": ["not json\n"]}, "pi_malformed_stream", None),
    ({"stdout": good_stream()[:-1] + [_event({"type": "agent_settled", "aborted": True})]}, "pi_aborted", 200),
    ({"stdout": good_stream(), "exit": 3, "stderr": "boom: provider unreachable"}, "pi_exit_3", 200),
    ({"stdout": [], "exit": 1, "stderr": "only stderr"}, "pi_exit_1", None),
    ({"stdout": []}, "pi_no_response", None),
    ({"stdout": [_event({"type": "message_end", "message": {
        "role": "assistant", "content": [], "stopReason": "error", "errorMessage": "model gone"}}),
        _event({"type": "agent_settled", "aborted": False})]}, "pi_model_error", None),
])
def test_a_failed_pi_call_is_a_provider_error_with_bounded_evidence(fake_pi, workspace, behavior, fragment,
                                                                    measured_input):
    fake_pi.behave(**behavior)
    out = PiProvider(role="builder", cwd=str(workspace)).build("x")
    review = PiProvider(role="reviewer", cwd=str(workspace)).review("x")
    assert out.error.startswith("provider_error: ") and fragment in out.error and len(out.error) < 600
    assert review.error.startswith("provider_error: ") and review.error_class == "provider_error"
    for failed in (out, review):
        if measured_input is None:
            assert (failed.usage_actuals, failed.actual_missing_reason) == (None, "provider_error")
        else:
            assert failed.actual_missing_reason == ""
            assert (failed.usage_actuals["input_tokens"], failed.usage_actuals["model_turns"]) == (measured_input, 2)


def test_a_wall_clock_trip_and_the_output_cap_and_a_signal_death(fake_pi, workspace, monkeypatch):
    fake_pi.behave(stdout=good_stream(), sleep=30)
    assert "pi_timeout" in PiProvider(role="builder", cwd=str(workspace)).build("x", timeout_sec=1).error
    monkeypatch.setattr(PP, "PI_STDOUT_CAP_BYTES", 64)
    fake_pi.behave(stdout=good_stream())
    assert "pi_output_limit" in PiProvider(role="builder", cwd=str(workspace)).build("x").error
    monkeypatch.setattr(PP, "PI_STDOUT_CAP_BYTES", 64 * 1024 * 1024)
    fake_pi.behave(stdout=[], sleep=0, exit=0)
    killer = fake_pi.dir / "pi"
    killer.write_text("#!/bin/sh\nkill -TERM $$\n")
    assert "pi_killed" in PiProvider(role="builder", cwd=str(workspace)).build("x").error


# --- 5 and 6. the workspace diff is the only proof ------------------------------------------

def test_a_claimed_edit_creates_no_change_and_a_real_edit_lands_only_in_the_workspace(fake_pi, workspace, tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    (target / "README.md").write_text("# Test\n")
    fake_pi.behave(stdout=good_stream("I appended the paragraph to README.md and staged it."))
    claimed = PiProvider(role="builder", cwd=str(workspace)).build("x")
    assert "staged it" in claimed.raw_text and claimed.files_changed == []
    assert (workspace / "README.md").read_text() == "# Test\n"

    fake_pi.behave(stdout=good_stream("done"), edits={"README.md": "\nA paragraph.\n"})
    PiProvider(role="builder", cwd=str(workspace)).build("x")
    assert (workspace / "README.md").read_text() == "# Test\n\nA paragraph.\n"
    assert (target / "README.md").read_text() == "# Test\n"


def test_a_reviewer_pass_on_an_empty_diff_is_rejected_before_completion():
    from packages.orchestration.empty_diff_gate import reject_verdict_on_empty_diff
    from packages.orchestration.pingpong_provider import ReviewerOutput

    passed = ReviewerOutput(verdict="pass", summary="looks staged")
    out = reject_verdict_on_empty_diff(passed, staged_files=[], is_fake=False)
    assert out.verdict == "needs_repair" and out.findings[0].id == "EMPTY-change"
    kept = reject_verdict_on_empty_diff(ReviewerOutput(verdict="pass"), staged_files=["a"], is_fake=False)
    assert kept.verdict == "pass"
    assert reject_verdict_on_empty_diff(ReviewerOutput(verdict="pass"), staged_files=[],
                                        is_fake=True).verdict == "pass"


# --- 7. the default resolution --------------------------------------------------------------

def test_with_no_flags_every_mutating_role_resolves_to_pi_on_the_local_model():
    from packages.orchestration.execution_config import resolve_job_execution_config
    from packages.orchestration.role_config import resolve_role_config

    for role in ("builder", "reviewer", "repair"):
        cfg = resolve_role_config(role)
        assert (cfg.provider, cfg.model) == ("pi", "muse-glimmer:latest")
    ec = resolve_job_execution_config(None)
    assert (ec.builder, ec.reviewer) == ("pi", "pi")
    assert PI_DEFAULT_MODEL == resolve_model_alias("ollama-default")
    assert resolve_role_config("planner").provider == "ollama"       # the structured roles stay direct
    explicit = resolve_job_execution_config(None, builder_name="claude-cli", reviewer_name="fake")
    assert (explicit.builder, explicit.reviewer, explicit.builder_source) == ("claude-cli", "fake", "cli")


# --- 8. persistence -------------------------------------------------------------------------

def test_the_pi_provider_round_trips_through_the_persisted_execution_config():
    from packages.orchestration.execution_config import (
        _export_execution_config,
        _import_execution_config,
        resolve_job_execution_config,
    )

    ec = resolve_job_execution_config(None, builder_name="pi", builder_model="muse-glimmer:latest")
    back = _import_execution_config(_export_execution_config(ec))
    assert (back.builder, back.builder_model) == ("pi", "muse-glimmer:latest")
    again = resolve_job_execution_config(back)
    assert (again.builder, again.builder_source) == ("pi", "persisted")


# --- 9. prerequisites fail before work ------------------------------------------------------

def test_a_missing_pi_stops_with_the_action_and_falls_back_to_nothing(tmp_path, monkeypatch):
    monkeypatch.setenv("PATH", str(tmp_path))
    with pytest.raises(PiUnavailable, match="Pi is required by the default local builder"):
        make_pi_provider("builder", cwd=None)
    out = PiProvider(role="builder", cwd=None).build("x")
    assert "pi_unavailable" in out.error and out.provider == "pi"
    assert any(not ok for _n, ok, _d in default_chain_checks()[:1])


def test_an_unreachable_ollama_or_a_missing_model_stops_before_the_builder(fake_pi, workspace, monkeypatch):
    def unreachable(host):
        raise PiUnavailable(f"Ollama is not reachable at {host}")
    monkeypatch.setattr(PP, "_ollama_models", unreachable)
    with pytest.raises(PiUnavailable, match="not reachable"):
        make_pi_provider("builder", cwd=str(workspace))
    monkeypatch.setattr(PP, "_ollama_models", lambda host: ["qwen3.5:9b"])
    with pytest.raises(PiUnavailable, match="ollama pull muse-glimmer:latest"):
        make_pi_provider("builder", cwd=str(workspace))
    monkeypatch.setattr(PP, "_ollama_models", lambda host: ["muse-glimmer:latest"])
    assert make_pi_provider("reviewer", cwd=str(workspace)).name == "pi"
    with pytest.raises(PiUnavailable, match="job workspace"):
        make_pi_provider("builder", cwd=str(workspace / "gone"))


def test_the_role_factory_builds_pi_and_the_cli_refuses_a_raw_ollama_builder(fake_pi, workspace, monkeypatch):
    from packages.orchestration.role_provider_factory import create_role_provider

    monkeypatch.setattr(PP, "_ollama_models", lambda host: ["muse-glimmer:latest"])
    built = create_role_provider("pi", role="reviewer", staging_dir=str(workspace), with_failover=False)
    assert isinstance(built, PiProvider) and built.model == "muse-glimmer:latest"
    with pytest.raises(SystemExit):
        from apps.cli.commands.do_cmd import _validate_role_override
        _validate_role_override("builder", "provider", "ollama")


def test_each_call_is_recorded_in_the_run_directory_with_the_prompt_as_a_hash(fake_pi, workspace, tmp_path):
    run_dir = tmp_path / "run"
    provider = PiProvider(role="builder", cwd=str(workspace), evidence_dir=str(run_dir))
    provider.build("a secret-bearing prompt text")
    lines = (run_dir / "pi" / "builder.jsonl").read_text().splitlines()
    record = json.loads(lines[0])
    assert record["model_turns"] == 2 and record["inner_provider"] == "ollama"
    assert "secret-bearing" not in lines[0] and "<prompt sha256:" in " ".join(record["argv"])


def test_the_builder_gets_the_file_list_and_the_named_files_up_front(tmp_path):
    """Lab order of 2026-10-17: a one-line fix spent 8 of 12 turns on ls, find, grep and reads."""
    from packages.orchestration.pi_provider import builder_workspace_context

    (tmp_path / "src").mkdir()
    (tmp_path / "test").mkdir()
    (tmp_path / "src" / "calc.js").write_text("export function add(a, b) {\n  return a - b;\n}\n")
    (tmp_path / "test" / "baseline.test.js").write_text('import { test } from "node:test";\n')
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "x.js").write_text("ignored")
    (tmp_path / "link.js").symlink_to(tmp_path / "src" / "calc.js")

    text = builder_workspace_context(str(tmp_path), "Fix add in src/calc.js and add test/calc.test.js.")

    assert "- src/calc.js\n" in text and "- test/baseline.test.js\n" in text
    assert "node_modules" not in text and "link.js" not in text
    assert "--- src/calc.js ---\nexport function add" in text
    assert "--- test/baseline.test.js ---" in text          # the style for the new test file
    assert "the complete list" in text
    assert builder_workspace_context("", "x") == ""


#: The loop's builder prompt of the 2026-10-18 real run r1351 (exec-1018b D9), shortened: its file tree
#: and README section name files the task never asks for.
_LOOP_PROMPT = (
    "You are a Builder working on a software task.\n\n## Goal\nDeliver src/calc.js and its test "
    "test/calc.test.js\n\n## File Tree\n```\n.git\nAGENTS.md\nREADME.md\npackage.json\nsrc/calc.js\n"
    "src/format.js\ntest/baseline.test.js\n```\n\n## README.md\n```\n# remedy-lab\nSee package.json.\n```\n\n"
    "## Task (Round 1)\nDie Funktion add(a, b) in src/calc.js rechnet falsch. Repariere sie und ergänze einen "
    "Regressionstest in test/calc.test.js.\n")


def test_the_files_shown_up_front_are_the_ones_the_task_names_not_the_trees(tmp_path):
    """exec-1018c (P1 7): the named files were read from the WHOLE prompt, so the loop's file tree and
    README section filled the four slots with README.md, package.json and src/format.js, and the style
    file for the new test was cut: in the real run the builder's first turn was a read. AGENTS.md
    arrives as project rules and is never shown twice."""
    from packages.orchestration.pi_provider import builder_workspace_context

    for rel, text in {"src/calc.js": "export function add(a, b) {\n  return a - b;\n}\n",
                      "src/format.js": "export const f = 1;\n", "README.md": "# remedy-lab\n",
                      "package.json": "{}\n", "AGENTS.md": "Use two spaces.\n",
                      "test/baseline.test.js": 'import { test } from "node:test";\n'}.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text)

    text = builder_workspace_context(str(tmp_path), _LOOP_PROMPT)

    preread = text.split("Current content of the files the task names", 1)[1]
    shown = [line[4:-4] for line in preread.splitlines() if line.startswith("--- ") and line.endswith(" ---")]
    assert shown == ["src/calc.js", "test/baseline.test.js"], shown
    assert text.count("Use two spaces.") == 1                   # the rules, once


def test_a_named_file_deep_in_a_large_repository_is_shown_and_the_cut_list_says_it_is_cut(tmp_path):
    """A tiny edit in a large repository: the bounded listing stops long before the named file, and
    it used to be neither shown nor reachable without a search, while the prompt called the list
    complete. Named paths that escape the workspace or pass a symlink are never read."""
    from packages.orchestration.pi_provider import builder_workspace_context

    for n in range(120):
        (tmp_path / "a" / f"d{n:03}").mkdir(parents=True)
        (tmp_path / "a" / f"d{n:03}" / "f.txt").write_text("x")
    deep = tmp_path / "z" / "pkg" / "src"
    deep.mkdir(parents=True)
    (deep / "util.py").write_text("def f():\n    return 1\n")
    (tmp_path / "outside.txt").write_text("secret")
    (tmp_path / "z" / "pkg" / "lnk").symlink_to(tmp_path)

    text = builder_workspace_context(
        str(tmp_path / "."), "Fix f in z/pkg/src/util.py; see ../outside.txt and z/pkg/lnk/outside.txt.")

    assert "--- z/pkg/src/util.py ---\ndef f():" in text
    assert "the first 80; the tree is larger" in text and "the complete list" not in text
    assert "secret" not in text


# --- the repository's own instructions (exec-1018, R-1347) ---------------------------------------

_MUST = "MANDATORY: every exported function carries a docstring."


def _rules_repo(root: Path) -> Path:
    """A repository whose rules: a 27,364-character root AGENTS.md whose binding sentence is its LAST
    line (any cut would drop it), a nested pkg/AGENTS.md that contradicts the root on indentation,
    a CLAUDE.md in a folder the task does not touch, and an AGENTS.md ABOVE the repository."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "AGENTS.md").write_text("Indent with tabs.\n" + "Context line.\n" * 1950 + _MUST + "\n")
    for rel, text in {"pkg/AGENTS.md": "Indent with four spaces in this package.\n",
                      "pkg/src/util.py": "def f():\n    return 1\n",
                      "other/CLAUDE.md": "Unrelated: the docs team writes in British English.\n",
                      "other/page.md": "# page\n"}.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)
    return root


def test_every_applicable_rule_file_reaches_the_builder_whole_and_in_order(tmp_path):
    """A large root file is delivered whole (its last, binding line included), the nested file of
    the touched folder after it, with the precedence stated; an untouched folder's file and any file
    above the repository never are."""
    from packages.orchestration.pi_provider import builder_workspace_context, project_rules

    (tmp_path / "AGENTS.md").write_text("ABOVE THE REPOSITORY: never reach me.\n")
    repo = _rules_repo(tmp_path / "repo")

    text = builder_workspace_context(str(repo), "Fix f in pkg/src/util.py.")
    rules = project_rules(str(repo), "Fix f in pkg/src/util.py.")

    assert [path for path, _text in rules.files] == ["AGENTS.md", "pkg/AGENTS.md"]
    assert rules.files[0][1].endswith(_MUST) and len(rules.files[0][1]) > 27_000      # never cut
    assert text.count(_MUST) == 1 and text.index("--- AGENTS.md ---") < text.index("--- pkg/AGENTS.md ---")
    assert "a deeper file refines the ones above it" in text and "Indent with four spaces" in text
    assert "British English" not in text and "ABOVE THE REPOSITORY" not in text
    assert "is Remedy's after review, never yours" in text      # Remedy's own rules come first
    assert rules.evidence()[1] == {"path": "pkg/AGENTS.md", "chars": 40,
                                   "sha256": rules.evidence()[1]["sha256"]}


def test_a_symlinked_rule_file_or_folder_is_never_followed(tmp_path):
    from packages.orchestration.pi_provider import project_rules

    (tmp_path / "secret.md").write_text("PRIVATE\n")
    repo = tmp_path / "repo"
    (repo / "pkg").mkdir(parents=True)
    (repo / "AGENTS.md").symlink_to(tmp_path / "secret.md")
    (repo / "lnk").symlink_to(tmp_path)

    assert project_rules(str(repo), "Fix pkg/a.py and lnk/repo/x.py.").files == ()


def test_the_reviewer_is_held_to_the_same_rules_and_told_to_fail_a_break(fake_pi, tmp_path):
    repo = _rules_repo(tmp_path / "job-workspace")
    fake_pi.behave(stdout=good_stream('{"verdict":"pass","findings":[],"confidence":"high","summary":"ok"}'))

    PiProvider(role="reviewer", cwd=str(repo)).review("M pkg/src/util.py\njudge this diff")

    prompt = fake_pi.call()["argv"][-1]
    assert _MUST in prompt and "Indent with four spaces" in prompt
    assert "They bind the change: fail it when it breaks one of them" in prompt


def test_rules_reach_the_model_once_in_the_prompt_and_never_through_pi_s_own_loader(fake_pi, tmp_path):
    """Repeated Pi turns: Pi resends its conversation every turn, so the rules ride in the first message
    exactly once and Pi's own context-file loader (which also read every ancestor folder) stays off."""
    repo = _rules_repo(tmp_path / "job-workspace")
    provider = PiProvider(role="builder", cwd=str(repo))

    provider.build("Fix f in pkg/src/util.py.")

    argv = fake_pi.call()["argv"]
    assert "--no-context-files" in argv and argv[-1].count(_MUST) == 1
    assert [entry["path"] for entry in provider.last_evidence["project_rules"]] == ["AGENTS.md", "pkg/AGENTS.md"]


def test_rules_too_large_for_one_call_stop_it_before_pi_starts_and_say_so(fake_pi, tmp_path):
    """Over the ceiling Remedy neither cuts nor points: the call is refused before Pi starts, and the
    loop reads the refusal as a context error, never as a missing provider."""
    from packages.orchestration.pi_provider import PROJECT_RULES_MAX_CHARS
    from packages.orchestration.pingpong_loop import provider_failure_status

    repo = tmp_path / "job-workspace"
    repo.mkdir()
    (repo / "AGENTS.md").write_text("Rule.\n" * (PROJECT_RULES_MAX_CHARS // 6 + 10))
    (repo / "a.py").write_text("x = 1\n")
    size = len((repo / "AGENTS.md").read_text().strip())

    out = PiProvider(role="builder", cwd=str(repo)).build("Fix a.py.")

    assert out.error.startswith("provider_error: project_rules_too_large: ")
    assert f"AGENTS.md ({size:,} characters)" in out.error and "not started" in out.error
    assert not (repo / ".fake-pi-call.json").exists()         # Pi never ran
    assert provider_failure_status(out.error) == "context_error"


def test_a_failed_calls_measured_tokens_reach_the_runs_usage_and_so_the_budgets(fake_pi, workspace):
    """A Pi builder that used two turns and then crashed spent 220 tokens; the run's usage, which the
    job's and the order's budgets read, carries them instead of reporting the call unmeasured."""
    from packages.orchestration.pingpong_loop import PingPongResult, _aggregate_usage_actuals
    from packages.orchestration.pingpong_provider_call import _record_attempt

    fake_pi.behave(stdout=good_stream(), exit=3, stderr="boom")
    failed = PiProvider(role="builder", cwd=str(workspace)).build("x")
    result = PingPongResult(builder_provider="pi", reviewer_provider="pi")
    _record_attempt(result, failed, "builder", "pi", round_num=1)

    usage = _aggregate_usage_actuals(result)

    assert failed.error and usage["total_tokens"] == 220
    assert (usage["provider_call_count"], usage["actual_call_count"]) == (1, 1)


ROOT_RULES = "# Rules\n\nUse Python 3.10.\n\n## Commits\n\nOne logical step per commit.\n\n## Tests\n\nEvery fix has a test.\n"


@pytest.mark.parametrize(("nested", "delivered"), [
    (ROOT_RULES, "[identical to AGENTS.md, delivered above]"),
    ("# Package rules\n\nIndent with tabs.\n\n## Tests\n\nEvery fix has a test.\n",
     '# Package rules\n\nIndent with tabs.\n\n[the section "Tests" is identical to AGENTS.md\'s, delivered above]'),
], ids=["identical-file", "shared-section"])
def test_a_rule_that_an_upper_file_already_delivers_is_named_never_sent_twice(tmp_path, nested, delivered):
    """exec-1018b (P1 5): lossless; a nested copy of the root rules was sent twice in every model turn."""
    from packages.orchestration.pi_provider import builder_workspace_context, project_rules

    (tmp_path / "AGENTS.md").write_text(ROOT_RULES)
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "AGENTS.md").write_text(nested)
    (tmp_path / "pkg" / "a.py").write_text("x = 1\n")

    rules = project_rules(str(tmp_path), "Fix pkg/a.py.")

    assert rules.files == (("AGENTS.md", ROOT_RULES.strip()), ("pkg/AGENTS.md", delivered))
    assert builder_workspace_context(str(tmp_path), "Fix pkg/a.py.").count("Every fix has a test.") == 1


def test_a_rule_file_with_nothing_repeated_is_delivered_byte_for_byte(tmp_path):
    from packages.orchestration.pi_provider import project_rules

    nested = "# Package\n\nTabs.\n## Odd spacing\nkept as written\n\n\n## Tests\n\nOnly here.\n"
    (tmp_path / "AGENTS.md").write_text(ROOT_RULES)
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "AGENTS.md").write_text(nested)
    (tmp_path / "pkg" / "a.py").write_text("x = 1\n")

    assert project_rules(str(tmp_path), "Fix pkg/a.py.").files[1] == ("pkg/AGENTS.md", nested.strip())
