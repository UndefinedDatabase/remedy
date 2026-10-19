"""Agent-state privacy boundary and staged-content guard."""

from __future__ import annotations

import importlib.util
import subprocess
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_hygiene_module():
    path = REPO_ROOT / "scripts" / "check_agent_hygiene.py"
    spec = importlib.util.spec_from_file_location("check_agent_hygiene", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ("text", "reason"),
    [
        ("API_KEY=realistic-secret-value", "credential"),
        ("workspace: /home/operator/private/repo", "machine-local path"),
        ("https://claude.ai/code/session_example-identifier", "provider session URL"),
        ("host: 192.168.1.20", "private network address"),
    ],
)
def test_sensitive_agent_state_additions_are_rejected(text: str, reason: str):
    hygiene = _load_hygiene_module()

    findings = hygiene.scan_agent_text(".agent/new.md", text)

    assert any(reason in finding.reason for finding in findings)


def test_redacted_portable_agent_state_is_allowed():
    hygiene = _load_hygiene_module()

    findings = hygiene.scan_agent_text(
        ".agent/plan.md",
        "# Plan\ncredential: [REDACTED]\nsource: [source_root]/packages/app.py\n",
    )

    assert findings == []


def test_staged_diff_checks_only_added_agent_state_lines():
    hygiene = _load_hygiene_module()
    diff = """diff --git a/.agent/plan.md b/.agent/plan.md
--- a/.agent/plan.md
+++ b/.agent/plan.md
@@ -1,2 +1,2 @@
-API_KEY=historical-secret-value
+credential: [REDACTED]
 context
"""

    assert hygiene.scan_staged_diff(diff) == []


def test_staged_binary_agent_state_is_rejected():
    hygiene = _load_hygiene_module()
    diff = """diff --git a/.agent/screenshot.png b/.agent/screenshot.png
new file mode 100644
Binary files /dev/null and b/.agent/screenshot.png differ
"""

    assert hygiene.scan_staged_diff(diff) == [
        hygiene.Finding(".agent/screenshot.png", 0, "binary agent-state file")
    ]


def test_pre_commit_hook_runs_agent_hygiene_guard():
    hook = (REPO_ROOT / ".githooks" / "pre-commit").read_text(encoding="utf-8")

    assert "python3 scripts/check_agent_hygiene.py --staged" in hook


def test_review_zip_excludes_all_agent_state(tmp_path: Path):
    e2e_path = REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py"
    spec = importlib.util.spec_from_file_location("_agent_hygiene_e2e", e2e_path)
    e2e = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(e2e)
    repo, base, _head = e2e._build_repo(tmp_path)
    (repo / ".agent").mkdir()
    (repo / ".agent" / "private.md").write_text("internal operator context\n")
    e2e._git(repo, "add", "-A")
    e2e._git(repo, "commit", "-qm", "agent state fixture")
    head = e2e._git(repo, "rev-parse", "HEAD").stdout.strip()
    evidence, _subject, _authority = e2e._write_evidence(repo, base, head, tmp_path / "evidence")

    proc = subprocess.run(
        ["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(evidence)],
        cwd=repo,
        capture_output=True,
        text=True,
        timeout=180,
        env={**__import__("os").environ, "PYTHONPATH": str(REPO_ROOT), "REMEDY_REVIEW_DIR": "."},
    )

    assert proc.returncode == 0, proc.stdout + proc.stderr
    [package] = list(repo.glob("remedy-review-*.zip"))
    with zipfile.ZipFile(package) as archive:
        assert not any(name == ".agent" or name.startswith(".agent/") for name in archive.namelist())
