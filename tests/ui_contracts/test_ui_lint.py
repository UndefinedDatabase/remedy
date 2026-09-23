"""`npm run lint` in `apps/ui` is a real gate: it parses TypeScript and exits 0 (R-0622).

Until F282 the lint configuration set no TypeScript parser, so every file stopped at its first
type annotation, the `react-hooks` rules never evaluated, and the run exited 1 on parse errors
alone. This runs the app's OWN eslint binary, as `test_typescript_compiles` runs its own `tsc`,
and skips only when the UI toolchain is absent (DECISION F083 D6). The probe below goes in on
stdin under a file name inside `src/`, so the checkout is never written (R-0645).
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

UI_ROOT = Path(__file__).resolve().parents[2] / "apps" / "ui"
LOCAL_ESLINT = UI_ROOT / "node_modules" / ".bin" / "eslint"

HOOK_DEFECT = (
    'import { useEffect } from "react";\n'
    "export function Probe({ id }: { id: string }): null {\n"
    "  useEffect(() => { console.log(id); }, []);\n"
    "  return null;\n"
    "}\n"
)


def _eslint(*args: str, stdin: str | None = None) -> subprocess.CompletedProcess:
    if not LOCAL_ESLINT.is_file():
        pytest.skip(f"UI toolchain absent: {LOCAL_ESLINT.parent.parent} is missing; run `npm ci --prefix apps/ui`")
    return subprocess.run([str(LOCAL_ESLINT), *args], cwd=str(UI_ROOT), capture_output=True, timeout=120,
                          input=stdin.encode("utf-8") if stdin is not None else None)


def test_the_ui_lint_passes_with_no_problem():
    result = _eslint("src", "--max-warnings", "0")
    assert result.returncode == 0, result.stdout.decode()[-4000:]


def test_the_lint_parses_typescript_and_reaches_the_hook_rules():
    """A lint that cannot parse the language passes nothing: a real hook defect must be seen."""
    result = _eslint("--stdin", "--stdin-filename", "src/lintProbe.tsx", "--format", "json",
                     stdin=HOOK_DEFECT)
    out = result.stdout.decode()
    assert "Parsing error" not in out, out
    assert "react-hooks/exhaustive-deps" in out, out
