"""A question to a project, answered by the Claude Code CLI that may only read (operator amendment
amend1026-go-live-and-ask, Parts C2 and C3). No model is reached: a scripted `claude` stands in for
the CLI, records the command line it was started with and answers in stream-json."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration.project_ask import (
    ASK_TOOLS,
    ProjectAskError,
    ask_project,
    build_ask_argv,
)

#: Every built-in tool that writes, edits, runs a command or reaches outside: none may be named.
_FORBIDDEN_TOOLS = ("Edit", "Write", "MultiEdit", "NotebookEdit", "Bash", "PowerShell", "WebFetch",
                    "WebSearch", "Task", "Agent")

_FAKE_CLAUDE = '''#!{python}
import json, sys, time, pathlib
pathlib.Path({argv_file!r}).write_text(json.dumps(sys.argv[1:]))
mode = {mode!r}
print(json.dumps({{"type": "system", "subtype": "init", "model": "claude-test-model"}}), flush=True)
text = pathlib.Path("greet.py").read_text()
print(json.dumps({{"type": "assistant", "message": {{"id": "m1", "usage": {{"input_tokens": 40, "output_tokens": 10}},
    "content": [{{"type": "tool_use", "name": "Read", "input": {{"file_path": "greet.py"}}}}]}}}}), flush=True)
if mode == "write":
    pathlib.Path("greet.py").write_text(text + "# changed\\n")
if mode == "spend":
    print(json.dumps({{"type": "assistant", "message": {{"id": "m2", "usage": {{"input_tokens": 900, "output_tokens": 900}},
        "content": [{{"type": "text", "text": "..."}}]}}}}), flush=True)
    time.sleep(30)
print(json.dumps({{"type": "result", "subtype": "success", "is_error": False, "num_turns": 2,
    "result": "Die Datei `greet.py` entscheidet.",
    "usage": {{"input_tokens": 50, "output_tokens": 20, "cache_creation_input_tokens": 5, "cache_read_input_tokens": 700}}}}),
    flush=True)
'''


def _tree_digest(repo: Path) -> dict[str, str]:
    """Every file of REPO outside `.git`, by its bytes' digest."""
    return {str(path.relative_to(repo)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(repo.rglob("*")) if path.is_file() and ".git" not in path.relative_to(repo).parts}


@pytest.fixture()
def project(tmp_path, monkeypatch):
    from packages.orchestration.project_registry import register_project_repo

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    repo = tmp_path / "ask-repo"
    repo.mkdir()
    (repo / "greet.py").write_text("def greet(name):\n    return f'Hallo {name}'\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init"],
                   check=True)
    register_project_repo("ask-repo", repo)
    return repo, tmp_path


def _fake_claude(tmp_path: Path, mode: str = "answer") -> tuple[str, Path]:
    argv_file = tmp_path / f"argv-{mode}.json"
    script = tmp_path / f"claude-{mode}"
    script.write_text(_FAKE_CLAUDE.format(python=sys.executable, argv_file=str(argv_file), mode=mode),
                      encoding="utf-8")
    script.chmod(0o755)
    return str(script), argv_file


def test_the_command_line_names_only_the_three_reading_tools():
    """C3: no write or command tool can be called, because the command line offers and permits none."""
    argv = build_ask_argv("/usr/bin/claude", "QUESTION")
    assert ASK_TOOLS == ("Read", "Glob", "Grep")
    assert argv[argv.index("--tools") + 1] == "Read,Glob,Grep"
    assert argv[argv.index("--allowedTools") + 1] == "Read,Glob,Grep"
    assert "--restricted" in argv and "--safe-mode" in argv and "--strict-mcp-config" in argv
    assert "--dangerously-skip-permissions" not in argv and "--permission-mode" not in argv
    named = {tool for part in argv[3:] for tool in part.replace(" ", ",").split(",")}
    assert not named & set(_FORBIDDEN_TOOLS)


def test_an_ask_answers_and_leaves_the_repository_unchanged(project):
    """C3: the CLI really started reads only, the repository is byte for byte what it was, and the
    evidence lies under the data root, never in the project."""
    repo, tmp_path = project
    claude, argv_file = _fake_claude(tmp_path)
    before = _tree_digest(repo)

    answer = ask_project("ask-repo", "Welche Datei grüßt?", max_total_tokens=1000, claude_path=claude)

    assert _tree_digest(repo) == before and answer["repo_unchanged"] is True
    started = json.loads(argv_file.read_text())
    assert started[started.index("--tools") + 1] == "Read,Glob,Grep"
    assert not {tool for part in started[2:] for tool in part.split(",")} & set(_FORBIDDEN_TOOLS)
    assert answer["answer"] == "Die Datei `greet.py` entscheidet."
    assert (answer["tokens_used"], answer["calls_used"], answer["turns"], answer["model"]) == (
        70, 1, 2, "claude-test-model")
    assert answer["tokens"] == {"input": 50, "output": 20, "cache_creation": 5, "cache_read": 700}
    assert answer["tool_calls"] == ["Read"]
    folder = tmp_path / "data" / answer["evidence"]
    assert sorted(path.name for path in folder.iterdir()) == [
        "answer.md", "prompt.txt", "question.json", "result.json", "stream.jsonl", "tool_calls.jsonl"]
    assert json.loads((folder / "question.json").read_text())["question"] == "Welche Datei grüßt?"
    assert json.loads((folder / "tool_calls.jsonl").read_text()) == {"tool": "Read", "input": {"file_path": "greet.py"}}
    assert not any(path.name.startswith("ask-") for path in repo.rglob("*"))


def test_an_ask_that_left_the_repository_changed_is_refused(project):
    repo, tmp_path = project
    claude, _argv_file = _fake_claude(tmp_path, "write")
    with pytest.raises(ProjectAskError) as refused:
        ask_project("ask-repo", "Was?", max_total_tokens=1000, claude_path=claude)
    assert refused.value.error == "ask_repo_changed" and refused.value.fields["repo_unchanged"] is False


def test_an_ask_past_its_cap_is_ended(project):
    _repo, tmp_path = project
    claude, _argv_file = _fake_claude(tmp_path, "spend")
    with pytest.raises(ProjectAskError) as refused:
        ask_project("ask-repo", "Was?", max_total_tokens=500, claude_path=claude)
    assert refused.value.error == "ask_budget_exhausted"


def test_an_unknown_project_and_an_empty_question_are_refused(project):
    with pytest.raises(ProjectAskError) as unknown:
        ask_project("no-such-project", "Was?", claude_path="/bin/false")
    assert unknown.value.error == "project_not_found"
    with pytest.raises(ProjectAskError) as empty:
        ask_project("ask-repo", "  ", claude_path="/bin/false")
    assert empty.value.error == "invalid_argument"
