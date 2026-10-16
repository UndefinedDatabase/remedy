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
                 "--no-prompt-templates", "--no-themes"):
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


# --- 4. failures ----------------------------------------------------------------------------

@pytest.mark.parametrize("behavior, fragment", [
    ({"stdout": good_stream()[:-1]}, "pi_unsettled"),
    ({"stdout": good_stream()[:-1] + ['{"type":"agent_settled","abor']}, "pi_malformed_stream"),
    ({"stdout": ["not json\n"]}, "pi_malformed_stream"),
    ({"stdout": good_stream()[:-1] + [_event({"type": "agent_settled", "aborted": True})]}, "pi_aborted"),
    ({"stdout": good_stream(), "exit": 3, "stderr": "boom: provider unreachable"}, "pi_exit_3"),
    ({"stdout": [], "exit": 1, "stderr": "only stderr"}, "pi_exit_1"),
    ({"stdout": []}, "pi_no_response"),
    ({"stdout": [_event({"type": "message_end", "message": {
        "role": "assistant", "content": [], "stopReason": "error", "errorMessage": "model gone"}}),
        _event({"type": "agent_settled", "aborted": False})]}, "pi_model_error"),
])
def test_a_failed_pi_call_is_a_provider_error_with_bounded_evidence(fake_pi, workspace, behavior, fragment):
    fake_pi.behave(**behavior)
    out = PiProvider(role="builder", cwd=str(workspace)).build("x")
    assert out.error.startswith("provider_error: ") and fragment in out.error
    assert len(out.error) < 600 and out.actual_missing_reason == "provider_error"
    review = PiProvider(role="reviewer", cwd=str(workspace)).review("x")
    assert review.error.startswith("provider_error: ") and review.error_class == "provider_error"


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
