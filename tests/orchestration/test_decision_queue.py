"""The budget decision's id and the one test of it (DECISION F253 D17 (3))."""

from __future__ import annotations

import pytest

from packages.orchestration.decision_queue import budget_decision_id, is_budget_decision_id


@pytest.mark.parametrize("decision_id", [budget_decision_id("r1"), budget_decision_id("")])
def test_a_budget_decision_id_is_recognised(decision_id: str) -> None:
    assert is_budget_decision_id(decision_id) is True


@pytest.mark.parametrize("decision_id", ["plan:abc", "veto:t1", "budget", "budgetary:x"])
def test_another_id_is_not_a_budget_decision_id(decision_id: str) -> None:
    assert is_budget_decision_id(decision_id) is False
