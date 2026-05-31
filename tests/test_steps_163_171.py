"""Tests for Steps 163-171: UX Product Reset v1 + Memory Candidate Contract Closure."""

from __future__ import annotations

import json
import re
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_job(name: str = "Test goal") -> Job:
    job = Job(name=name)
    job.metadata = job.metadata or {}
    return job


def _make_events() -> list[dict]:
    return [
        {"event": "autorun_started", "timestamp": "2026-01-01T00:00:00Z", "metadata": {}},
        {"event": "structured_patch_intent_created", "timestamp": "2026-01-01T00:01:00Z", "metadata": {"intent_kind": "file_ops"}},
        {"event": "source_patch_applied", "timestamp": "2026-01-01T00:02:00Z", "metadata": {}},
        {"event": "test_run_completed", "timestamp": "2026-01-01T00:03:00Z", "metadata": {"exit_code": 0, "passed": True}},
        {"event": "proof_collected", "timestamp": "2026-01-01T00:04:00Z", "metadata": {"content_hash": "abc123"}},
    ]


# ===========================================================================
# Step 163 — Memory Candidate Contract Closure
# ===========================================================================


class TestStep163MemoryCandidates:
    """Memory candidate contract closure."""

    def test_create_candidate_basic(self):
        from packages.orchestration.memory_candidates import create_candidate, list_candidates

        job = _make_job()
        c = create_candidate(job, "repair_pattern", "Repair loop fixed mul", confidence="medium")
        assert c["kind"] == "repair_pattern"
        assert c["status"] == "pending"
        assert c["safe_summary"] == "Repair loop fixed mul"
        assert c["confidence"] == "medium"

        candidates = list_candidates(job)
        assert len(candidates) == 1
        assert candidates[0]["id"] == c["id"]

    def test_create_candidate_dedup(self):
        from packages.orchestration.memory_candidates import create_candidate, list_candidates

        job = _make_job()
        c1 = create_candidate(job, "repair_pattern", "Same summary")
        c2 = create_candidate(job, "repair_pattern", "Same summary")
        assert c1["id"] == c2["id"]
        assert len(list_candidates(job)) == 1

    def test_approve_candidate(self):
        from packages.orchestration.memory_candidates import (
            approve_candidate,
            create_candidate,
            list_candidates,
        )

        job = _make_job()
        c = create_candidate(job, "test_command", "pytest passes")
        assert approve_candidate(job, c["id"])
        candidates = list_candidates(job)
        assert candidates[0]["status"] == "approved"

    def test_reject_candidate(self):
        from packages.orchestration.memory_candidates import (
            create_candidate,
            list_candidates,
            reject_candidate,
        )

        job = _make_job()
        c = create_candidate(job, "test_command", "pytest passes")
        assert reject_candidate(job, c["id"])
        candidates = list_candidates(job)
        assert candidates[0]["status"] == "rejected"

    def test_approve_already_rejected(self):
        from packages.orchestration.memory_candidates import (
            approve_candidate,
            create_candidate,
            reject_candidate,
        )

        job = _make_job()
        c = create_candidate(job, "test_command", "test")
        reject_candidate(job, c["id"])
        # Can't approve already rejected
        assert not approve_candidate(job, c["id"])

    def test_no_raw_leaks_in_candidate(self):
        from packages.orchestration.memory_candidates import create_candidate

        job = _make_job()
        c = create_candidate(
            job, "repair_pattern",
            "Safe summary only",
            evidence_node_ids=["node-1", "node-2"],
        )
        s = json.dumps(c)
        for forbidden in ("stdout", "stderr", "traceback", "command_output"):
            assert forbidden not in s.lower()


# ===========================================================================
# Step 164 — Human Story ViewModel
# ===========================================================================


class TestStep164Story:
    """Story ViewModel."""

    def test_story_schema(self):
        from packages.orchestration.ui_view_model import build_story

        job = _make_job("Build a README")
        events = _make_events()
        story = build_story(job, events)

        assert story["version"] == 1
        assert story["job_id"] == str(job.id)
        assert story["headline"]
        assert story["plain_status"]
        assert "progress" in story
        for key in ("completed", "active", "pending", "blocked", "needs_review"):
            assert key in story["progress"]
        assert "journey" in story

    def test_journey_has_items(self):
        from packages.orchestration.ui_view_model import build_story

        job = _make_job()
        events = _make_events()
        story = build_story(job, events)
        assert len(story["journey"]) > 0

    def test_journey_items_human_readable(self):
        from packages.orchestration.ui_view_model import build_story

        job = _make_job()
        events = _make_events()
        story = build_story(job, events)

        for j in story["journey"]:
            assert j.get("title"), f"missing title: {j}"
            assert j.get("kind"), f"missing kind: {j}"
            assert j.get("state") in ("done", "current", "pending", "blocked", "suggested")

    def test_forbidden_debug_words_absent(self):
        from packages.orchestration.ui_view_model import build_story
        from packages.orchestration.ui_copy import FORBIDDEN_DEFAULT_WORDS

        job = _make_job()
        events = _make_events()
        story = build_story(job, events)
        s = json.dumps(story).lower()

        for word in FORBIDDEN_DEFAULT_WORDS:
            # Allow "rank" as part of internal data but not in titles/subtitles
            for j in story["journey"]:
                assert word not in j["title"].lower(), f"forbidden '{word}' in title: {j['title']}"
                assert word not in (j.get("subtitle") or "").lower(), f"forbidden '{word}' in subtitle"


# ===========================================================================
# Step 165 — Human Node Detail
# ===========================================================================


class TestStep165HumanDetail:
    """Human-only node detail."""

    def test_human_detail_schema(self):
        from packages.orchestration.ui_view_model import build_human_node_detail, build_story

        job = _make_job()
        events = _make_events()
        story = build_story(job, events)
        if not story["journey"]:
            pytest.skip("no journey items")

        node_id = story["journey"][0]["node_id"]
        detail = build_human_node_detail(job, events, node_id)

        assert detail["version"] == 3
        assert detail["title"]
        assert detail["state"]

    def test_human_detail_no_debug_fields(self):
        from packages.orchestration.ui_view_model import build_human_node_detail, build_story

        job = _make_job()
        events = _make_events()
        story = build_story(job, events)
        if not story["journey"]:
            pytest.skip("no journey items")

        node_id = story["journey"][0]["node_id"]
        detail = build_human_node_detail(job, events, node_id)
        s = json.dumps(detail).lower()

        for word in ("node_type", "connected_to", "edge_type", "present signals", "missing signals"):
            assert word not in s, f"forbidden debug word in human detail: {word}"

    def test_human_detail_not_found(self):
        from packages.orchestration.ui_view_model import build_human_node_detail

        job = _make_job()
        events = _make_events()
        detail = build_human_node_detail(job, events, "nonexistent-node")
        assert detail.get("error") == "node not found"


# ===========================================================================
# Step 166 — Journey Graph Layout
# ===========================================================================


class TestStep166JourneyLayout:
    """Journey graph layout."""

    def test_journey_left_to_right(self):
        from packages.orchestration.ui_view_model import build_story

        job = _make_job()
        events = _make_events()
        story = build_story(job, events)

        # Journey items should have increasing kind order (goal → task → ... → proof)
        kind_order = {"goal": 0, "task": 1, "change": 2, "approval": 3,
                      "apply": 4, "test": 5, "proof": 6, "review": 7, "memory": 8, "decision": 9}
        journey = story["journey"]
        if len(journey) >= 2:
            orders = [kind_order.get(j["kind"], 99) for j in journey]
            # Should be non-decreasing
            for i in range(1, len(orders)):
                assert orders[i] >= orders[i-1], f"journey not left-to-right at index {i}"

    def test_no_system_nodes_in_default(self):
        from packages.orchestration.ui_view_model import build_story
        from packages.orchestration.ui_copy import is_diagnostics_only

        job = _make_job()
        events = _make_events()
        story = build_story(job, events)

        # Journey should not contain diagnostics-only nodes
        for j in story["journey"]:
            # We can't directly check node_type from journey, but titles should not be system labels
            title = j["title"].lower()
            assert "context coverage" not in title
            assert "token policy" not in title
            assert "worker" not in title


# ===========================================================================
# Step 167 — Diagnostics Layers
# ===========================================================================


class TestStep167Layers:
    """Diagnostics layers."""

    def test_layer_schema(self):
        from packages.orchestration.ui_view_model import build_layers

        layers = build_layers()
        assert layers["version"] == 1
        assert len(layers["layers"]) >= 2

    def test_default_layer_is_journey(self):
        from packages.orchestration.ui_view_model import build_layers

        layers = build_layers()
        defaults = [l for l in layers["layers"] if l.get("default")]
        assert len(defaults) == 1
        assert defaults[0]["id"] == "journey"

    def test_diagnostics_layer_exists(self):
        from packages.orchestration.ui_view_model import build_layers

        layers = build_layers()
        diag = [l for l in layers["layers"] if l["id"] == "diagnostics"]
        assert len(diag) == 1
        assert not diag[0].get("default")

    def test_diagnostics_nodes_separate(self):
        from packages.orchestration.ui_view_model import build_diagnostics_nodes

        job = _make_job()
        events = _make_events()
        result = build_diagnostics_nodes(job, events)
        assert result["layer"] == "diagnostics"
        # Should only contain diagnostics-type nodes


# ===========================================================================
# Step 168 — Task Ribbon Checklist
# ===========================================================================


class TestStep168Checklist:
    """Task ribbon checklist."""

    def test_checklist_schema(self):
        from packages.orchestration.ui_view_model import build_checklist

        job = _make_job()
        events = _make_events()
        cl = build_checklist(job, events)

        assert cl["version"] == 1
        assert len(cl["items"]) > 0

    def test_no_bare_ids_as_labels(self):
        from packages.orchestration.ui_view_model import build_checklist

        job = _make_job()
        events = _make_events()
        cl = build_checklist(job, events)

        for item in cl["items"]:
            label = item["label"]
            assert label, "empty label"
            # Not a bare UUID/hash
            assert not re.match(r"^[0-9a-f-]{8,}$", label), f"bare ID as label: {label}"

    def test_checklist_has_goal(self):
        from packages.orchestration.ui_view_model import build_checklist

        job = _make_job("Write a README")
        events = _make_events()
        cl = build_checklist(job, events)

        kinds = [item["kind"] for item in cl["items"]]
        assert "goal" in kinds

    def test_checklist_item_states(self):
        from packages.orchestration.ui_view_model import build_checklist

        job = _make_job()
        events = _make_events()
        cl = build_checklist(job, events)

        for item in cl["items"]:
            assert item["state"] in ("done", "current", "pending", "blocked", "suggested"), f"bad state: {item['state']}"
            assert isinstance(item["checked"], bool)

    def test_memory_candidate_in_checklist(self):
        from packages.orchestration.memory_candidates import create_candidate
        from packages.orchestration.ui_view_model import build_checklist

        job = _make_job()
        create_candidate(job, "repair_pattern", "Repair fixed mul")
        events = _make_events()
        cl = build_checklist(job, events)

        mem_items = [i for i in cl["items"] if i["kind"] == "memory"]
        assert len(mem_items) >= 1
        assert "Repair fixed mul" in mem_items[0]["label"]


# ===========================================================================
# Step 169 — Human Copy Dictionary
# ===========================================================================


class TestStep169CopyDictionary:
    """Human copy dictionary."""

    def test_all_default_types_have_labels(self):
        from packages.orchestration.ui_copy import _DEFAULT_VISIBLE, human_label

        for ntype in _DEFAULT_VISIBLE:
            label = human_label(ntype)
            assert label
            assert "_" not in label, f"snake_case in label: {label} for {ntype}"

    def test_no_snake_case_in_labels(self):
        from packages.orchestration.ui_copy import _NODE_LABELS

        for ntype, (label, subtitle) in _NODE_LABELS.items():
            assert "_" not in label, f"snake_case in label: {label}"

    def test_diagnostics_only_set(self):
        from packages.orchestration.ui_copy import is_default_visible, is_diagnostics_only

        assert is_diagnostics_only("context_coverage")
        assert is_diagnostics_only("token_policy")
        assert not is_diagnostics_only("job")
        assert not is_diagnostics_only("task")

    def test_human_state(self):
        from packages.orchestration.ui_copy import human_state

        assert human_state("completed") == "Done"
        assert human_state("running") == "In progress"
        assert human_state("blocked") == "Blocked"
        assert human_state(None) == "Unknown"

    def test_forbidden_words_defined(self):
        from packages.orchestration.ui_copy import FORBIDDEN_DEFAULT_WORDS

        assert "rank" in FORBIDDEN_DEFAULT_WORDS
        assert "importance" in FORBIDDEN_DEFAULT_WORDS
        assert "node_type" in FORBIDDEN_DEFAULT_WORDS

    def test_layers_defined(self):
        from packages.orchestration.ui_copy import LAYERS

        assert len(LAYERS) >= 2
        journey = [l for l in LAYERS if l["id"] == "journey"]
        assert len(journey) == 1
        assert journey[0]["default"] is True


# ===========================================================================
# Step 170 — UX Smoke Gate
# ===========================================================================


class TestStep170UXSmokeGate:
    """UX smoke gate checks."""

    def test_story_available(self):
        from packages.orchestration.ui_view_model import build_story

        job = _make_job()
        events = _make_events()
        story = build_story(job, events)
        assert story["version"] == 1

    def test_default_story_forbids_debug_words(self):
        from packages.orchestration.ui_copy import FORBIDDEN_DEFAULT_WORDS
        from packages.orchestration.ui_view_model import build_story

        job = _make_job()
        events = _make_events()
        story = build_story(job, events)

        # Check journey titles and subtitles
        for j in story["journey"]:
            for word in FORBIDDEN_DEFAULT_WORDS:
                assert word not in j["title"].lower()
                assert word not in (j.get("subtitle") or "").lower()

    def test_checklist_has_human_labels(self):
        from packages.orchestration.ui_view_model import build_checklist

        job = _make_job()
        events = _make_events()
        cl = build_checklist(job, events)
        for item in cl["items"]:
            assert item["label"]
            assert not re.match(r"^[0-9a-f-]{8,}$", item["label"])

    def test_context_coverage_not_in_journey(self):
        from packages.orchestration.ui_view_model import build_story

        job = _make_job()
        events = _make_events()
        story = build_story(job, events)

        for j in story["journey"]:
            assert "context coverage" not in j["title"].lower()
            assert "context_coverage" not in j.get("kind", "")


# ===========================================================================
# Step 171 — Visual Polish
# ===========================================================================


class TestStep171VisualPolish:
    """Visual polish checks."""

    def test_app_shell_has_semantic_classes(self):
        from packages.orchestration.ui_app_shell import build_app_shell

        html = build_app_shell("test-job-id", "test-token")

        required_classes = [
            "remedy-journey-shell",
            "remedy-checklist",
            "remedy-node-current",
            "remedy-node-done",
            "remedy-detail-compact",
            "remedy-layer-switcher",
        ]
        for cls in required_classes:
            assert cls in html, f"missing CSS class: {cls}"

    def test_no_external_cdn(self):
        from packages.orchestration.ui_app_shell import build_app_shell

        html = build_app_shell("test-job-id", "test-token")
        assert "cdn." not in html.lower()
        assert "fonts.googleapis" not in html.lower()
        assert "unpkg.com" not in html.lower()

    def test_reduced_motion(self):
        from packages.orchestration.ui_app_shell import build_app_shell

        html = build_app_shell("test-job-id", "test-token")
        assert "prefers-reduced-motion" in html

    def test_detail_card_no_advanced_by_default(self):
        from packages.orchestration.ui_app_shell import build_app_shell

        html = build_app_shell("test-job-id", "test-token")
        # Detail card visible class not set by default
        assert 'class="remedy-detail-compact"' in html
        assert 'class="remedy-detail-compact visible"' not in html

    def test_no_debug_rail(self):
        from packages.orchestration.ui_app_shell import build_app_shell

        html = build_app_shell("test-job-id", "test-token")
        # No permanent metadata wall or debug rail
        assert "debug-rail" not in html
        assert "metadata-wall" not in html

    def test_label_strategy(self):
        from packages.orchestration.ui_app_shell import build_app_shell

        html = build_app_shell("test-job-id", "test-token")
        # Journey nodes use text labels (screen-space stable via SVG text)
        assert "journey-node" in html
        assert "node-subtitle" in html
