"""Tests for sticky per-task actor binding (task_actor_binding)."""
from __future__ import annotations

from packages.orchestration.task_actor_binding import build_task_actor_binding


def test_basic_binding_shape_and_keys():
    binding = build_task_actor_binding(
        "T002",
        builder_provider="ollama",
        builder_model="qwen3-coder-next",
        reviewer_provider="ollama",
        reviewer_model="qwen2.5:7b",
    )
    expected_keys = {
        "task_id",
        "builder_role",
        "builder_provider",
        "builder_model_configured",
        "builder_identity",
        "reviewer_role",
        "reviewer_provider",
        "reviewer_model_configured",
        "reviewer_identity",
        "sticky_across_rounds",
        "rounds",
        "repair_rounds",
        "reviewer_findings_by_round",
        "repaired_findings_by_round",
        "unresolved_findings",
        "same_builder_used_for_repairs",
        "same_reviewer_used_for_re_review",
    }
    assert set(binding) == expected_keys
    assert binding["task_id"] == "T002"
    assert binding["builder_role"] == "builder"
    assert binding["reviewer_role"] == "reviewer"


def test_sticky_true_when_same_actors():
    binding = build_task_actor_binding(
        "T002",
        same_builder_repairs=True,
        same_reviewer_re_review=True,
    )
    assert binding["sticky_across_rounds"] is True
    assert binding["same_builder_used_for_repairs"] is True
    assert binding["same_reviewer_used_for_re_review"] is True


def test_sticky_false_when_only_builder_same():
    binding = build_task_actor_binding(
        "T002",
        same_builder_repairs=True,
        same_reviewer_re_review=False,
    )
    assert binding["sticky_across_rounds"] is False


def test_sticky_false_when_only_reviewer_same():
    binding = build_task_actor_binding(
        "T002",
        same_builder_repairs=False,
        same_reviewer_re_review=True,
    )
    assert binding["sticky_across_rounds"] is False


def test_sticky_false_when_different_actors():
    binding = build_task_actor_binding(
        "T002",
        same_builder_repairs=False,
        same_reviewer_re_review=False,
    )
    assert binding["sticky_across_rounds"] is False


def test_round_tracking():
    binding = build_task_actor_binding("T002", rounds=3, repair_rounds=2)
    assert binding["rounds"] == 3
    assert binding["repair_rounds"] == 2


def test_finding_tracking():
    binding = build_task_actor_binding(
        "T002",
        findings_by_round=[3, 1, 0],
        repaired_by_round=[2, 1, 0],
    )
    assert binding["reviewer_findings_by_round"] == [3, 1, 0]
    assert binding["repaired_findings_by_round"] == [2, 1, 0]


def test_unresolved_tracking():
    binding = build_task_actor_binding("T002", unresolved=2)
    assert binding["unresolved_findings"] == 2


def test_identity_recording():
    binding = build_task_actor_binding(
        "T002",
        builder_provider="ollama",
        builder_model="qwen3-coder-next",
        reviewer_provider="claude",
        reviewer_model="opus",
    )
    assert binding["builder_identity"] == "ollama:qwen3-coder-next"
    assert binding["reviewer_identity"] == "claude:opus"
    assert binding["builder_provider"] == "ollama"
    assert binding["builder_model_configured"] == "qwen3-coder-next"


def test_identity_none_when_both_absent():
    binding = build_task_actor_binding("T002")
    assert binding["builder_identity"] is None
    assert binding["reviewer_identity"] is None


def test_empty_rounds_defaults():
    binding = build_task_actor_binding("T002")
    assert binding["rounds"] == 0
    assert binding["repair_rounds"] == 0
    assert binding["reviewer_findings_by_round"] == []
    assert binding["repaired_findings_by_round"] == []
    assert binding["unresolved_findings"] == 0
    assert binding["sticky_across_rounds"] is False


def test_multiple_repair_rounds_sticky():
    binding = build_task_actor_binding(
        "T002",
        builder_provider="ollama",
        builder_model="qwen3-coder-next",
        reviewer_provider="ollama",
        reviewer_model="qwen3-coder-next",
        rounds=4,
        repair_rounds=3,
        findings_by_round=[5, 3, 1, 0],
        repaired_by_round=[2, 2, 1, 0],
        unresolved=0,
        same_builder_repairs=True,
        same_reviewer_re_review=True,
    )
    assert binding["rounds"] == 4
    assert binding["repair_rounds"] == 3
    assert binding["reviewer_findings_by_round"] == [5, 3, 1, 0]
    assert binding["repaired_findings_by_round"] == [2, 2, 1, 0]
    assert binding["sticky_across_rounds"] is True


def test_negative_and_none_values_clamped():
    binding = build_task_actor_binding(
        "T002",
        rounds=-1,
        repair_rounds=None,
        findings_by_round=[None, 2, -3],
        unresolved=-5,
    )
    assert binding["rounds"] == 0
    assert binding["repair_rounds"] == 0
    assert binding["reviewer_findings_by_round"] == [0, 2, 0]
    assert binding["unresolved_findings"] == 0
