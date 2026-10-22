"""F203 — the `print` ratchet over `packages/` (DECISION F203 D3).

`pyproject.toml` selects ruff's T20 for `packages/` (the tests, `apps/` and `scripts/` are
excused by per-file ignores: a command line prints by design), so `ruff check .` — which the CI
`budgets` stage requires to report zero findings — fails on any unmarked `print`. A call that
must print carries `# noqa: T201 — <reason>`. This test holds the other half: every such mark
states a reason, the number of marks never rises, the rule stays selected, and the one
`packages/` file excused as a whole is the one DECISION F203 D3 names.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCANNED_ROOTS = ("packages",)
MARK = re.compile(r"#\s*noqa:\s*T201\b(?P<rest>.*)")
REASONED = re.compile(r"^ — \S")

#: The number of reasoned `print` marks when T20 was turned on. Only ever falls: the commit
#: that removes a mark lowers this number in the same commit, and it is never raised.
MAX_EXCUSED = 8


def _marks() -> list[tuple[str, int, str]]:
    found = []
    for top in SCANNED_ROOTS:
        for path in sorted((REPO / top).rglob("*.py")):
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                match = MARK.search(line)
                if match:
                    found.append((path.relative_to(REPO).as_posix(), number, match.group("rest")))
    return found


def test_every_excused_print_states_a_reason():
    bare = [f"{path}:{number}" for path, number, rest in _marks() if not REASONED.match(rest)]
    assert not bare, f"`# noqa: T201` without a reason after ' — ': {bare}"


def test_the_count_of_excused_prints_never_rises():
    count = len(_marks())
    assert count <= MAX_EXCUSED, (
        f"{count} excused print calls, above the frozen {MAX_EXCUSED}: write a record "
        f"through `logging` instead of excusing the print")
    assert count == MAX_EXCUSED, (
        f"{count} excused print calls, below {MAX_EXCUSED}: lower MAX_EXCUSED to "
        f"{count} in this commit so the ratchet cannot let one back in")


def test_t20_stays_selected():
    text = (REPO / "pyproject.toml").read_text(encoding="utf-8")
    select = re.search(r"^select = \[(.*?)\]", text, re.M)
    assert select is not None and '"T20"' in select.group(1)


def test_no_file_in_packages_is_excused_whole():
    """`serve_http_handler.py` was the last, for its frontend build's output; that build was deleted
    (amend1015f D3), so no file under packages/ prints freely any more."""
    text = (REPO / "pyproject.toml").read_text(encoding="utf-8")
    section = text.split("[tool.ruff.lint.per-file-ignores]", 1)[1].split("\n[", 1)[0]
    keys = re.findall(r'^"(packages/[^"]*)"\s*=\s*\[(.*?)\]', section, re.M)
    excused = [key for key, codes in keys if '"T20"' in codes]
    assert excused == [], (
        f"files in packages/ excused from T20 as a whole: {excused}")
