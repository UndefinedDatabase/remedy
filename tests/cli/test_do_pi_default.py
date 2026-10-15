"""Operator amendment amend1014b — the two incident commands back to back, through a fake `pi`.

`remedy do ... --apply` then `remedy do ... --commit-auto`, with no provider flag, no commit,
stash or reset between them. The fake `pi` executable edits the README in its working directory
the way the real harness does (the builder) or prints a passing verdict (the reviewer).
"""
from __future__ import annotations

import json
import os
import stat
import subprocess
import textwrap
from pathlib import Path

import pytest

import packages.orchestration.pi_provider as PP
from apps.cli.grouped import main
from tests.cli.test_do_bounded_lane import INCIDENT_ORDER, _commit_repo, _git

SECOND_ORDER = ("Add one concise project-description paragraph below the existing last scentence "
                "in README.md. Change no other files.")

_FAKE_PI = textwrap.dedent('''\
    #!/usr/bin/env python3
    import json, os, sys
    if sys.argv[1:] == ["--version"]:
        print("9.9.9"); sys.exit(0)
    argv = sys.argv[1:]
    tools = argv[argv.index("--tools") + 1]
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "calls.log"), "a") as log:
        log.write(json.dumps({"tools": tools, "cwd": os.getcwd()}) + "\\n")
    def emit(event):
        sys.stdout.write(json.dumps(event) + "\\n"); sys.stdout.flush()
    emit({"type": "agent_start"})
    if "edit" in tools:
        with open("README.md") as fh:
            seen = fh.read()
        with open("README.md", "a") as fh:
            fh.write("\\nParagraph %d.\\n" % (seen.count("Paragraph") + 1))
        text = "Appended a paragraph."
        emit({"type": "tool_execution_start", "toolName": "edit", "args": {"secret": "s3cr3t"}})
        emit({"type": "tool_execution_end", "toolName": "edit", "isError": False})
    else:
        text = json.dumps({"verdict": "pass", "findings": [], "confidence": "high", "summary": "ok"})
    emit({"type": "message_end", "message": {"role": "assistant", "provider": "ollama",
          "model": "muse-glimmer:latest", "stopReason": "stop",
          "content": [{"type": "text", "text": text}],
          "usage": {"input": 5, "output": 2, "cacheRead": 0, "cacheWrite": 0, "totalTokens": 7}}})
    emit({"type": "agent_end", "messages": [], "willRetry": False})
    emit({"type": "agent_settled", "aborted": False})
''')


@pytest.fixture
def pi_world(tmp_path, monkeypatch):
    bindir = tmp_path / "bin"
    bindir.mkdir()
    exe = bindir / "pi"
    exe.write_text(_FAKE_PI)
    exe.chmod(exe.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("PATH", f"{bindir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setattr(PP, "_ollama_models", lambda host: ["muse-glimmer:latest"])
    target = _commit_repo(tmp_path / "test", {"README.md": "# Test\n"})
    monkeypatch.chdir(target)
    return target, bindir / "calls.log"


def _calls(log: Path) -> list[dict]:
    return [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []


def test_json_stays_one_envelope_progress_names_the_chain_and_the_target_is_untouched(pi_world, capsys):
    target, log = pi_world

    main(["do", INCIDENT_ORDER, "--repo", ".", "--no-ui", "--json"])

    out, err = capsys.readouterr()
    envelope = json.loads(out)                          # exactly one document, nothing else
    assert isinstance(envelope, dict)
    assert "message_end" not in out + err and "s3cr3t" not in out + err   # no raw Pi JSONL leaks
    calls = _calls(log)
    assert [c["tools"] for c in calls] == ["read,bash,edit,write,grep,find,ls", "read,grep,find,ls"]
    assert all(".remedy-wt" in c["cwd"] and Path(c["cwd"]) != target for c in calls)
    assert (target / "README.md").read_text() == "# Test\n"
    assert _git(target, "status", "--porcelain") == ""


def test_the_human_progress_names_pi_and_the_model(pi_world, capsys):
    main(["do", INCIDENT_ORDER, "--repo", ".", "--no-ui"])
    err = capsys.readouterr().err
    assert "run started — builder pi (ollama/muse-glimmer:latest), reviewer pi (ollama/muse-glimmer:latest)" in err


def test_apply_then_commit_auto_run_back_to_back_with_no_flags_and_no_ceremony(pi_world, capsys):
    target, log = pi_world

    main(["do", INCIDENT_ORDER, "--repo", ".", "--no-ui", "--apply"])
    capsys.readouterr()
    assert _git(target, "status", "--porcelain").split() == ["M", "README.md"]       # applied, not committed
    after_b = (target / "README.md").read_text()
    assert after_b == "# Test\n\nParagraph 1.\n"
    head_b = _git(target, "rev-parse", "HEAD")

    main(["do", SECOND_ORDER, "--repo", ".", "--no-ui", "--commit-auto"])
    out = capsys.readouterr()

    assert (target / "README.md").read_text() == after_b + "\nParagraph 2.\n"           # built on B's bytes
    assert _git(target, "status", "--porcelain") == ""                                 # clean afterwards
    assert _git(target, "rev-list", "--count", f"{head_b.strip()}..HEAD").strip() == "1"
    assert _git(target, "show", "--name-only", "--format=", "HEAD").split() == ["README.md"]
    assert _git(target, "stash", "list") == ""
    assert "commit or stash" not in out.out + out.err
    assert len(_calls(log)) == 4                                                       # 2 builders, 2 reviewers


def test_an_unrelated_dirty_file_is_preserved_and_named(pi_world, capsys):
    target, _log = pi_world
    (target / "notes.txt").write_text("n\n")
    _git(target, "add", "notes.txt")
    _git(target, "commit", "-qm", "notes")
    (target / "notes.txt").write_text("n, edited by hand\n")

    main(["do", INCIDENT_ORDER, "--repo", ".", "--no-ui", "--commit-auto"])
    out = capsys.readouterr().out

    assert _git(target, "show", "--name-only", "--format=", "HEAD").split() == ["README.md"]
    assert _git(target, "status", "--porcelain").split() == ["M", "notes.txt"]
    assert (target / "notes.txt").read_text() == "n, edited by hand\n"
    assert _git(target, "stash", "list") == ""
    assert "notes.txt" in out


def test_a_raw_ollama_builder_is_refused_before_anything_runs(pi_world, capsys):
    target, log = pi_world
    with pytest.raises(SystemExit) as exc:
        main(["do", INCIDENT_ORDER, "--repo", ".", "--no-ui", "--builder-provider", "ollama"])
    assert exc.value.code == 2 and "--builder-provider pi" in capsys.readouterr().err
    assert _calls(log) == [] and subprocess.run(["git", "worktree", "list"], cwd=target,
                                                capture_output=True, text=True).stdout.count("\n") == 1


def test_the_docs_and_the_help_describe_pi_the_model_and_a_dirty_tree_without_the_old_promise():
    """Test 18: Pi is the default harness, --apply applies, --commit-auto selects, no clean-tree demand."""
    from apps.cli.command_catalog_do import DO_COMMANDS  # the do.run catalog entry's module
    root = Path(__file__).resolve().parents[2]
    guide = (root / "docs/guides/do-run-v1.md").read_text()
    quick = (root / "docs/guides/simple-operator-quickstart-v0.md").read_text()
    for needle in ("Pi is the default execution harness", "muse-glimmer:latest", "`--apply`",
                   "`--commit-auto` commits only the files the job changed",
                   "A dirty working tree is the baseline", "target_changed_during_run"):
        assert needle in guide, needle
    assert 'remedy do "' in quick and "--apply" in quick and "Pi and Ollama" in quick
    for text in (guide, quick):
        assert "commit or stash first" not in text and "must be clean" not in text
    help_text = " ".join(arg.help for cmd in DO_COMMANDS for arg in cmd.args
                         if arg.name in ("--builder-provider", "--reviewer-provider"))
    assert "pi" in help_text and "muse-glimmer:latest" in help_text


def test_a_target_edited_during_the_run_blocks_the_apply_with_the_token_and_survives(pi_world, capsys, monkeypatch):
    """Acceptance E in miniature: the human edit lands after the job captured its start state."""
    target, _log = pi_world
    from packages.orchestration import pingpong_job

    real = pingpong_job.run_job

    def run_then_edit(*args, **kwargs):
        job = real(*args, **kwargs)
        (target / "README.md").write_text("# Test\n\nA human edit made while the job ran.\n")
        return job

    monkeypatch.setattr(pingpong_job, "run_job", run_then_edit)
    with pytest.raises(SystemExit):
        main(["do", INCIDENT_ORDER, "--repo", ".", "--no-ui", "--apply"])

    err = capsys.readouterr().err
    assert "target_changed_during_run: README.md changed in the target" in err
    assert (target / "README.md").read_text() == "# Test\n\nA human edit made while the job ran.\n"
    assert _git(target, "rev-list", "--count", "HEAD").strip() == "1"
