"""amend1027-green-builds A3: a real claude-cli builder call, never asked, runs an allowed test command and is refused another.

Builds the builder's command line exactly as Remedy does (`build_claude_cli_args`, write mode
`allowed-tools`, the project's Bash rules, `--permission-mode dontAsk`, the isolation flags) for a
throwaway Python project with one test, asks the CLI to run `python3 -m pytest -q` and then
`curl --version`, and keeps the argv, the answer and the CLI's `permission_denials`.
Usage: python3 .agent/authored/amend1027-a3-probe.py <scratch folder> <evidence file>
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from packages.orchestration.claude_cli_command import build_claude_cli_args, builder_test_commands
from packages.providers.adapters.claude_cli_reference import _ISOLATION_TOOL_ARGS

scratch, out = Path(sys.argv[1]), Path(sys.argv[2])
project = scratch / "a3-project"
shutil.rmtree(project, ignore_errors=True)
(project / "tests").mkdir(parents=True)
(project / "tests" / "test_one.py").write_text("def test_one():\n    assert 1 + 1 == 2\n")
subprocess.run(["git", "init", "-q"], cwd=project, check=True)
prompt = ("Use the Bash tool to run exactly these two commands, one after the other, each on its own: "
          "first `python3 -m pytest -q`, then `curl --version`. Do not run anything else and do not "
          "edit any file. Then answer in one line per command: the command and whether it ran or was refused.")
argv = build_claude_cli_args(shutil.which("claude") or "claude", prompt, write_mode="allowed-tools",
                             workspace=str(project)) + list(_ISOLATION_TOOL_ARGS)
done = subprocess.run(argv, cwd=project, capture_output=True, text=True, timeout=600)
envelope = json.loads(done.stdout) if done.stdout.strip().startswith("{") else {}
record = {
    "argv_without_prompt": [a for a in argv if a != prompt],
    "builder_test_commands": list(builder_test_commands(str(project))),
    "exit_code": done.returncode,
    "result": envelope.get("result"),
    "permission_denials": envelope.get("permission_denials"),
    "num_turns": envelope.get("num_turns"),
    "usage": envelope.get("usage"),
    "stderr_tail": done.stderr[-2000:],
}
out.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({k: record[k] for k in ("exit_code", "result", "permission_denials")}, indent=2, ensure_ascii=False))
