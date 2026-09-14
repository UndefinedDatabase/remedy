"""F275 — a page that names a source file must name one that exists.

Finding R-0873 recorded a class the advertisement guard
(``tests/cli/test_advertised_commands.py``) is structurally blind to: a page can
document a mechanism that has been deleted without ever spelling one of its
commands. Most of that class needs a human ruling, but one part of it does not —
a page that names a MODULE PATH is making a claim that is true or false on disk,
and nothing was checking it. At F275 round 30 four such claims were false, in
three pages, every one of them a file this feature had deleted.

WHY THE CORPUS IS THE OPERATOR-FACING ONE AND NOT ALL OF ``docs/``. The same two
trees the advertisement guard sweeps, for the same reason: these are the pages an
operator reads as instructions. The trees deliberately left out are left out
because a path that does not resolve is CORRECT in them:

* ``docs/roadmap/`` describes what SHALL BE (AGENTS.md, Documentation Structure),
  so a feature file names the module its feature will create. 187 unresolved
  paths live there by design.
* ``docs/ui/design_reference/`` is a target spec in the same sense.
* ``docs/agents/`` quotes findings ABOUT paths that do not resolve — finding
  R-0559's own text in ``planner_reviewer_prompt.md`` names three such paths in
  order to say they are wrong, and a guard that cannot tell a quotation from a
  claim is satisfied by the quotation (the R-0584 class).
* ``docs/archive/`` records abandoned designs and is expected to name their
  modules.

That exclusion is a property of the corpus, not a way to make the sweep pass: no
page under ``docs/system/`` or ``docs/guides/`` is skipped.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

#: The same two trees ``tests/cli/test_advertised_commands.py`` sweeps.
_OPERATOR_FACING_ROOTS: tuple[str, ...] = ("docs/system", "docs/guides")

#: A source path as a page writes one. ``tsx`` precedes ``ts`` in the extension
#: alternation on purpose: with ``ts`` first, ``RemedyShell.tsx`` matches as
#: ``RemedyShell.ts`` and the guard reports a miss on a file that exists.
_SOURCE_PATH_RE = re.compile(
    r"(?:packages|apps|tests|scripts)/[\w./-]*\.(?:tsx|ts|py|sh|json|toml)"
)


def _tracked_files() -> set[str]:
    listing = subprocess.run(
        ["git", "ls-files"], cwd=REPO_ROOT,
        capture_output=True, text=True, check=True,
    ).stdout
    return set(listing.splitlines())


def collect_named_source_paths() -> tuple[int, list[str]]:
    """Return (paths named, sites naming a path that does not exist)."""
    tracked = _tracked_files()
    named = 0
    missing: list[str] = []
    for root in _OPERATOR_FACING_ROOTS:
        listing = subprocess.run(
            ["git", "ls-files", root], cwd=REPO_ROOT,
            capture_output=True, text=True, check=True,
        ).stdout
        for relative_path in listing.splitlines():
            if not relative_path.endswith(".md"):
                continue
            source = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
            for line_number, line in enumerate(source.splitlines(), 1):
                for match in _SOURCE_PATH_RE.finditer(line):
                    named += 1
                    if match.group(0) not in tracked:
                        missing.append(f"{relative_path}:{line_number}: {match.group(0)}")
    return named, missing


def test_every_source_path_an_operator_facing_page_names_exists() -> None:
    named, missing = collect_named_source_paths()

    # Anti-blindness: a sweep that matches nothing satisfies a zero-gate
    # perfectly. The real figure was 244 when this guard was written, so 100 is
    # a floor with room rather than a pin on today's count.
    assert named > 100, f"the source-path sweep went blind: only {named} paths matched"

    assert not missing, (
        "an operator-facing page names a source file that does not exist — "
        "delete or repair the reference in the same commit as the file:\n"
        + "\n".join(missing)
    )


def test_the_sweep_reports_a_path_that_does_not_exist() -> None:
    """The guard's own discriminator: it must be able to find a miss."""
    tracked = _tracked_files()

    assert "packages/orchestration/no_such_module.py" not in tracked
    assert _SOURCE_PATH_RE.findall(
        "see `packages/orchestration/no_such_module.py` for details"
    ) == ["packages/orchestration/no_such_module.py"]


def test_the_extension_alternation_does_not_truncate_tsx() -> None:
    """``.tsx`` must not be read as ``.ts`` — that reported a false miss."""
    assert _SOURCE_PATH_RE.findall("`apps/ui/src/RemedyApp.tsx` composes") == [
        "apps/ui/src/RemedyApp.tsx"
    ]
