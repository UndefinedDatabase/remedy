"""F278 T003 — the blind-exception ratchet.

`pyproject.toml` selects ruff's BLE001 outside `tests/`, so `ruff check .` — which the CI
`budgets` stage requires to report zero findings — fails on any unmarked `except Exception`.
A handler that must catch everything carries `# noqa: BLE001 — <reason>`. This test holds
the other half: every such mark states a reason, the number of marks never rises, and the
rule stays selected.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCANNED_ROOTS = ("packages", "apps", "scripts")
MARK = re.compile(r"#\s*noqa:\s*BLE001\b(?P<rest>.*)")
REASONED = re.compile(r"^ — \S")

#: The number of excused blind handlers when BLE001 was turned on. Only ever falls: the
#: commit that removes a mark lowers this number in the same commit, and it is never raised.
MAX_EXCUSED = 290


def _marks() -> list[tuple[str, int, str]]:
    found = []
    for top in SCANNED_ROOTS:
        for path in sorted((REPO / top).rglob("*.py")):
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                match = MARK.search(line)
                if match:
                    found.append((path.relative_to(REPO).as_posix(), number, match.group("rest")))
    return found


def test_every_excused_handler_states_a_reason():
    bare = [f"{path}:{number}" for path, number, rest in _marks() if not REASONED.match(rest)]
    assert not bare, f"`# noqa: BLE001` without a reason after ' — ': {bare}"


def test_the_count_of_excused_handlers_never_rises():
    count = len(_marks())
    assert count <= MAX_EXCUSED, (
        f"{count} excused blind handlers, above the frozen {MAX_EXCUSED}: narrow the new "
        f"handler to the exceptions it expects instead of excusing it")
    assert count == MAX_EXCUSED, (
        f"{count} excused blind handlers, below {MAX_EXCUSED}: lower MAX_EXCUSED to "
        f"{count} in this commit so the ratchet cannot let one back in")


def test_ble001_stays_selected():
    text = (REPO / "pyproject.toml").read_text(encoding="utf-8")
    select = re.search(r"^select = \[(.*?)\]", text, re.M)
    assert select is not None and '"BLE001"' in select.group(1)
