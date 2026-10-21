"""Agent-state privacy boundary and staged-content guard."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
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


def test_staged_symlink_agent_state_is_rejected():
    hygiene = _load_hygiene_module()
    changed = b".agent/context-link\0.agent/plan.md\0"
    index_entries = (
        b"120000 1111111111111111111111111111111111111111 0\t.agent/context-link\0"
        b"100644 2222222222222222222222222222222222222222 0\t.agent/plan.md\0"
    )

    assert hygiene.scan_staged_modes(changed, index_entries) == [
        hygiene.Finding(".agent/context-link", 0, "non-regular agent-state entry")
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


_MOVED_RECORD = "Gate: F055 R8 — the package sits in /home/operator/history/zips."


def _rotation_diff(added_path: str, *, deleted: int = 1, added: int = 1, source: str = ".agent/live_review.md") -> str:
    """A zero-context diff that deletes the record from `source` and adds it to `added_path`."""
    return (
        f"diff --git a/{source} b/{source}\n"
        f"--- a/{source}\n"
        f"+++ b/{source}\n"
        f"@@ -7,{deleted} +6,0 @@\n"
        + "".join(f"-{_MOVED_RECORD}\n" for _ in range(deleted))
        + f"diff --git a/{added_path} b/{added_path}\n"
        f"--- a/{added_path}\n"
        f"+++ b/{added_path}\n"
        f"@@ -40,0 +41,{added} @@\n"
        + "".join(f"+{_MOVED_RECORD}\n" for _ in range(added))
    )


def test_a_rotation_moves_a_ledger_record_holding_a_path_into_the_archive():
    """R-1376: the archive receives, unscanned, exactly the lines the same diff deletes from the ledger."""
    hygiene = _load_hygiene_module()

    assert hygiene.scan_staged_diff(_rotation_diff(".agent/live_review_archive.md")) == []


def test_a_ledger_record_moved_into_another_agent_file_is_still_refused():
    hygiene = _load_hygiene_module()

    assert hygiene.scan_staged_diff(_rotation_diff(".agent/plan.md")) == [
        hygiene.Finding(".agent/plan.md", 41, "machine-local path")
    ]


def test_an_archive_line_the_ledger_did_not_lose_is_refused_and_a_second_copy_too():
    hygiene = _load_hygiene_module()

    assert hygiene.scan_staged_diff(_rotation_diff(".agent/live_review_archive.md", deleted=0)) == [
        hygiene.Finding(".agent/live_review_archive.md", 41, "machine-local path")
    ]
    assert hygiene.scan_staged_diff(_rotation_diff(".agent/live_review_archive.md", added=2)) == [
        hygiene.Finding(".agent/live_review_archive.md", 42, "machine-local path")
    ]


def test_a_line_another_agent_file_lost_is_refused_in_the_archive():
    hygiene = _load_hygiene_module()

    assert hygiene.scan_staged_diff(_rotation_diff(".agent/live_review_archive.md", source=".agent/plan.md")) == [
        hygiene.Finding(".agent/live_review_archive.md", 41, "machine-local path")
    ]


def test_an_added_line_that_starts_with_two_plus_signs_is_content_not_a_file_name():
    """R-1412: `+++ ` inside a hunk is an added line `++ ...`; it never switches the file scanned."""
    hygiene = _load_hygiene_module()
    diff = """diff --git a/.agent/plan.md b/.agent/plan.md
--- a/.agent/plan.md
+++ b/.agent/plan.md
@@ -1,0 +1,2 @@
+++ /home/operator/private
+API_KEY=realistic-secret-value
"""

    assert hygiene.scan_staged_diff(diff) == [
        hygiene.Finding(".agent/plan.md", 1, "machine-local path"),
        hygiene.Finding(".agent/plan.md", 2, "credential"),
    ]


def test_the_staged_check_lets_a_real_rotation_commit_and_refuses_a_new_path(tmp_path: Path):
    """R-1376 end to end: `--staged` over a real index, as the pre-commit hook runs it."""
    repo = tmp_path / "repo"
    (repo / ".agent").mkdir(parents=True)
    ledger = repo / ".agent" / "live_review.md"
    archive = repo / ".agent" / "live_review_archive.md"
    ledger.write_text(f"# Ledger\n\n{_MOVED_RECORD}\n\nGate: F999 R1 — kept.\n", encoding="utf-8")
    archive.write_text("# Archive\n", encoding="utf-8")

    def git(*args: str) -> None:
        subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@example.com", *args],
                       check=True, capture_output=True)

    def staged_check() -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "check_agent_hygiene.py"), "--staged"],
                              cwd=repo, capture_output=True, text=True)

    git("init", "-q")
    git("add", "-A")
    git("commit", "-qm", "base")
    ledger.write_text("# Ledger\n\nGate: F999 R1 — kept.\n", encoding="utf-8")
    archive.write_text(f"# Archive\n\n{_MOVED_RECORD}\n", encoding="utf-8")
    git("add", "-A")
    moved = staged_check()
    assert moved.returncode == 0, moved.stderr

    (repo / ".agent" / "plan.md").write_text("workspace: /home/operator/private/repo\n", encoding="utf-8")
    git("add", "-A")
    refused = staged_check()
    assert refused.returncode == 1
    assert ".agent/plan.md:1: refused machine-local path" in refused.stderr
