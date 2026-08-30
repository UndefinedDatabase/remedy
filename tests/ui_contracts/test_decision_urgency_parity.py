"""Pin: the urgency formula's two homes agree, until T002 leaves only one.

DECISION F040 D2 moved the SINGLE HOME of DECISION F031 D6's rule — a decision
card's urgency is `(blocked size + 1) * age` — into Python, as
`decision_urgency` in `packages/orchestration/decision_inbox.py`, because the
digest endpoint and `remedy job digest` both need the number and neither can
call a browser function. The browser's own copy, `decisionUrgency` in
`apps/ui/src/api/decisionOrder.ts`, still ships and still orders the live inbox,
so TWO HOMES EXIST between that decision and F040 T002, which retires the
TypeScript one. THIS FILE IS THE PIN THAT MAKES THAT SAFE: the two are asserted
equal rather than trusted, and a drift in either reddens here.

NOTHING ELSE IN THIS REPOSITORY READS THE TWO ENDS TOGETHER. The Python suite
cannot see the TypeScript, and the shipped vitest config
(`apps/ui/vitest.config.ts`, environment node, include `src/**/*.test.ts`)
cannot see the Python. So this module reads the TypeScript AS TEXT and imports
nothing from `apps/`, exactly as `tests/ui_contracts/test_apply_state_partial.py`
and `tests/ui_contracts/test_decision_answer_wiring.py` do.

Every assertion over the TypeScript runs on COMMENT-STRIPPED source. Both
implementations carry WHY comments that quote the very expressions asserted
below — `blockedCount * ageSeconds`, the null age, the clamp — so an unstripped
guard would be satisfied by the prose describing the branch rather than by the
branch (finding R-0584).

THE TABLE IS SHARED, NOT DUPLICATED. Each row of `URGENCY_TABLE` carries the
name of the TypeScript rule it exercises, and every named rule must be present
in the shipped TypeScript body; the same row's expected number is asserted
against the shipped Python. A row can therefore only pass when both halves
still implement the behaviour it names.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from packages.orchestration.decision_inbox import decision_urgency

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
# The browser's copy. Named here so that moving it without moving this constant
# makes `test_the_typescript_function_is_found_at_all` fail loudly rather than
# leaving an empty extraction to satisfy every assertion beneath it.
ORDER_MODULE = REPO_ROOT / "apps" / "ui" / "src" / "api" / "decisionOrder.ts"
TS_FUNCTION = "decisionUrgency"

#: The TypeScript rules the table below depends on, each as the exact fragment
#: the shipped, comment-stripped body must still contain. These four ARE the
#: formula: the finiteness test and the clamp on the blocked size, the null and
#: negative guard on the age, and the product with its `+ 1`.
TS_RULES = {
    "product": "return (blockedCount + 1) * age;",
    "blocked_finite": "Number.isFinite(model.blockedCount)",
    "blocked_clamp": "Math.max(0, model.blockedCount)",
    "age_guard": "rawAge !== null && Number.isFinite(rawAge) && rawAge > 0 ? rawAge : 0",
}

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


def strip_ts_comments(text: str) -> str:
    """Drop `//` and `/* */` comments, the scanner every guard in this directory uses.

    The scanned file holds no string literal carrying either marker, which is what
    lets so plain a scanner be trustworthy here.
    """
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        pair = text[i:i + 2]
        if pair == "//":
            newline = text.find("\n", i)
            i = n if newline == -1 else newline
        elif pair == "/*":
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def order_module_code() -> str:
    """The browser's ordering module with its prose removed."""
    return strip_ts_comments(ORDER_MODULE.read_text())


def typescript_urgency_body() -> str:
    """The body of `decisionUrgency`, brace depth respected, or a loud assertion.

    Scoped rather than swept: `orderDecisionInbox` sits directly below in the same
    file and CALLS this function twice, so a whole-file reading of the product
    expression could be answered by a neighbour and would stay green with this
    function's own return gone.
    """
    code = order_module_code()
    match = re.search(rf"function {TS_FUNCTION}\(", code)
    assert match, (
        f"{ORDER_MODULE.name} declares no function named {TS_FUNCTION}; this pin would "
        f"measure the Python against an empty extraction and could not fail"
    )
    start = code.index("{", match.end())
    depth = 0
    for index in range(start, len(code)):
        if code[index] == "{":
            depth += 1
        elif code[index] == "}":
            depth -= 1
            if depth == 0:
                return code[start:index + 1]
    raise AssertionError(f"the body of {TS_FUNCTION} never closes in the scanned source")


def test_the_typescript_function_is_found_at_all():
    """The extraction fails LOUDLY, here, before anything is measured against it.

    An empty body would satisfy every substring assertion's negation silently and
    would let this whole module pass against a file that no longer holds the
    formula — the failure mode a pin exists to prevent.
    """
    assert ORDER_MODULE.exists(), f"{ORDER_MODULE} is missing; the pin has no second half"
    body = typescript_urgency_body()
    assert body.strip().startswith("{") and body.strip().endswith("}")
    assert len(body) > 100, f"{TS_FUNCTION}'s body scanned as {len(body)} characters"


def test_the_typescript_still_returns_the_blocked_plus_one_times_age_shape():
    """The product, read off comment-stripped source rather than off the WHY prose.

    The comment directly above that return QUOTES `blockedCount * ageSeconds` — the
    form the `+ 1` exists to reject — so an unstripped search for the shipped shape
    would be answered by the paragraph explaining it (R-0584).
    """
    body = typescript_urgency_body()
    assert TS_RULES["product"] in body
    # And the form the decision rejects is NOT what ships, once the prose is gone.
    assert "return blockedCount * age;" not in body
    assert "blockedCount * ageSeconds" not in body


@pytest.mark.parametrize("rule", sorted(TS_RULES))
def test_every_typescript_rule_the_table_depends_on_still_ships(rule):
    """Each row's expectation rests on one of these; none may quietly disappear."""
    body = typescript_urgency_body()
    assert TS_RULES[rule] in body, (
        f"{TS_FUNCTION} no longer contains the {rule} rule {TS_RULES[rule]!r}; the "
        f"rows of URGENCY_TABLE naming it would pin the Python against nothing"
    )


def test_the_table_exercises_every_typescript_rule():
    """No rule is asserted present without a row that depends on its behaviour."""
    assert {row[3] for row in URGENCY_TABLE} | {"blocked_finite"} == set(TS_RULES)


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
