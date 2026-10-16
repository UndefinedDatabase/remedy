"""The urgency formula's one home, scored against a table (DECISIONs F031 D6, F040 D2).

A decision card's urgency is `(blocked size + 1) * age`, computed by `decision_urgency` in
`packages/orchestration/decision_inbox.py`. The browser's copy this table was once also checked
against was deleted with the old face (amend1015f D27), so only the Python half of the pin stays;
it moved here from `tests/ui_contracts/test_decision_urgency_parity.py`. Each row still names the
rule it exercises, so the edge cases cannot be dropped unnoticed.
"""
from __future__ import annotations

import pytest

from packages.orchestration.decision_inbox import decision_urgency

#: `(blocked size, age in seconds, urgency, the TS rule the row exercises)`.
#: A Python None is the TypeScript `null` the endpoint sends for an unreadable
#: `created_at`; both halves score it as nothing.
URGENCY_TABLE = [
    (3, 3600, 14400, "product"),
    (1, 120, 240, "product"),
    (0, 42, 42, "product"),
    (0, 0, 0, "product"),
    (5, None, 0, "age_guard"),
    (2, -3600, 0, "age_guard"),
    (-4, 60, 60, "blocked_clamp"),
]


@pytest.mark.parametrize("blocked,age,expected,rule", URGENCY_TABLE)
def test_the_python_home_scores_the_shared_table(blocked, age, expected, rule):
    """The Python half of the pin: same inputs, same numbers, same rules."""
    assert decision_urgency({"blocked_count": blocked, "age_seconds": age}) == expected


def test_the_shared_table_covers_the_cases_the_two_halves_disagree_on_most_easily():
    """A table of only ordinary rows would pass over two identical bugs.

    The null age, the negative age and the zero blocked size are exactly the
    inputs where a re-implementation drifts, so their presence is asserted rather
    than left to whoever edits the table next.
    """
    assert len(URGENCY_TABLE) >= 6
    assert any(age is None for _, age, _, _ in URGENCY_TABLE)
    assert any(age is not None and age < 0 for _, age, _, _ in URGENCY_TABLE)
    assert any(blocked == 0 for blocked, _, _, _ in URGENCY_TABLE)
    assert any(blocked < 0 for blocked, _, _, _ in URGENCY_TABLE)
