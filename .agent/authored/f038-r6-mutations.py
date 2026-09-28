"""F038 R6 G5 — the red-proof tool. Given a worktree path, it mutates
`packages/orchestration/chat_door.py` inside that worktree, one real behaviour change at a
time, and shows that `tests/orchestration/test_chat_door.py` catches every one of them, then
restores the file byte-identical. Run directly: `python3 -B f038-r6-mutations.py <worktree>`.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

TARGET_REL = "packages/orchestration/chat_door.py"
TEST_NODE = "tests/orchestration/test_chat_door.py"


def _purge_pycache(root: Path) -> None:
    for current, dirs, _files in os.walk(root):
        if "__pycache__" in dirs:
            shutil.rmtree(Path(current, "__pycache__"))
            dirs.remove("__pycache__")


def _run_tests(root: Path) -> tuple[int, str]:
    _purge_pycache(root)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rf",
         TEST_NODE],
        cwd=str(root), env=env, capture_output=True, text=True, check=False)
    return proc.returncode, proc.stdout + proc.stderr


def _failed_count_and_nodes(output: str) -> tuple[int, list[str]]:
    nodes = [line[len("FAILED "):].split(" - ", 1)[0].strip()
             for line in output.splitlines() if line.startswith("FAILED ")]
    count = 0
    for line in output.splitlines():
        line = line.strip().strip("= ")
        if "failed" not in line:
            continue
        for token in line.split(", "):
            token = token.strip()
            if token.endswith("failed") and token[: -len("failed")].strip().isdigit():
                count = int(token[: -len("failed")].strip())
    return count, nodes


MUTATIONS: tuple[tuple[str, str, str], ...] = (
    ("r1 the CSRF header is not sent",
     '            headers={\n'
     '                "Authorization": f"Bearer {token}",\n'
     '                COMMAND_CSRF_HEADER: token,\n'
     '                "Content-Type": "application/json",\n'
     '            },\n',
     '            headers={\n'
     '                "Authorization": f"Bearer {token}",\n'
     '                "Content-Type": "application/json",\n'
     '            },\n'),
    ("r2 the Authorization header is not sent",
     '            headers={\n'
     '                "Authorization": f"Bearer {token}",\n'
     '                COMMAND_CSRF_HEADER: token,\n'
     '                "Content-Type": "application/json",\n'
     '            },\n',
     '            headers={\n'
     '                COMMAND_CSRF_HEADER: token,\n'
     '                "Content-Type": "application/json",\n'
     '            },\n'),
    ("r3 a card that is not confirmable is sent anyway, its body built without "
     "card_command_payload",
     '    body = card_command_payload(card, client_nonce=client_nonce)\n',
     '    body = {"command": card.verb, "client_nonce": client_nonce, '
     '"args": dict(card.args)}\n'),
    ("r4 the job id is not checked",
     '    if not is_safe_id(job_id):\n'
     '        raise ChatIntentError(f"job_id {job_id!r} is not a safe id")\n',
     ''),
    ("r5 the port is not checked",
     '    if not isinstance(port, int) or isinstance(port, bool) or not '
     '1 <= port <= 65535:\n'
     '        raise ChatIntentError(f"port {port!r} is not a usable port")\n',
     ''),
    ("r6 the token is not checked",
     '    if not token:\n'
     '        raise ChatIntentError("token must not be empty")\n',
     ''),
    ("r7 every answer reads as accepted",
     '    @property\n'
     '    def accepted(self) -> bool:\n'
     '        return self.status == 200\n',
     '    @property\n'
     '    def accepted(self) -> bool:\n'
     '        return True\n'),
    ("r8 the nonce sent is a fixed string rather than the one given",
     'card_command_payload(card, client_nonce=client_nonce)',
     'card_command_payload(card, client_nonce="fixed-nonce")'),
)


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    target = root / TARGET_REL
    original = target.read_bytes()

    all_caught = True

    label = "control (unmutated, first)"
    code, output = _run_tests(root)
    count, nodes = _failed_count_and_nodes(output)
    print(f"{label}: exit={code} failed={count} nodes={nodes}")
    if code != 0:
        all_caught = False

    for label, from_text, to_text in MUTATIONS:
        text = target.read_text(encoding="utf-8")
        occurrences = text.count(from_text)
        assert occurrences == 1, f"{label}: FROM text occurs {occurrences} times, not 1"
        mutated = text.replace(from_text, to_text, 1)
        target.write_text(mutated, encoding="utf-8")
        try:
            code, output = _run_tests(root)
        finally:
            target.write_bytes(original)
        count, nodes = _failed_count_and_nodes(output)
        print(f"{label}: exit={code} failed={count} nodes={nodes}")
        if code == 0:
            all_caught = False

    label = "control (unmutated, last)"
    code, output = _run_tests(root)
    count, nodes = _failed_count_and_nodes(output)
    print(f"{label}: exit={code} failed={count} nodes={nodes}")
    if code != 0:
        all_caught = False

    restored = target.read_bytes() == original
    print(f"restored byte-identical: {restored}")
    result = bool(all_caught and restored)
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
