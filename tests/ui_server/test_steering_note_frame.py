"""
Domain tests: ui_server/test_steering_note_frame.py

F030 T003: the browser's steering note frame — `_safe_event_summary` adds a `note` of
`_steering_note_summary_payload`'s four fields for `steering_message_received` alone, and no
other kind's frame gains a `note` or `steering` key (DECISION F030 D3).
"""

from __future__ import annotations

from packages.orchestration import ui_server as mod


class TestTheSteeringNoteFrame:
    def test_a_received_frame_carries_the_four_note_fields_with_the_text_verbatim(self):
        summary = mod._safe_event_summary(6, {
            "event": "steering_message_received",
            "metadata": {"message_id": "sm-0002", "text": "watch the budget", "channel": "cli",
                         "task_id": "task-2", "record_sha256": "abc"}})
        assert summary["note"] == {"message_id": "sm-0002", "text": "watch the budget",
                                    "channel": "cli", "task_id": "task-2"}

    def test_a_job_wide_note_carries_an_empty_task_id(self):
        summary = mod._safe_event_summary(7, {
            "event": "steering_message_received",
            "metadata": {"message_id": "sm-0003", "text": "hold off", "channel": "door"}})
        assert summary["note"]["task_id"] == ""

    def test_the_note_task_id_falls_back_to_the_event_top_level_when_metadata_has_none(self):
        summary = mod._safe_event_summary(8, {
            "event": "steering_message_received", "task_id": "task-9",
            "metadata": {"message_id": "sm-0004", "text": "go slower", "channel": "cli"}})
        assert summary["note"]["task_id"] == "task-9"

    def test_the_metadata_task_id_wins_over_the_event_top_level(self):
        summary = mod._safe_event_summary(11, {
            "event": "steering_message_received", "task_id": "task-top",
            "metadata": {"message_id": "sm-0006", "text": "stay put", "channel": "cli",
                         "task_id": "task-meta"}})
        assert summary["note"]["task_id"] == "task-meta"

    def test_a_received_frame_still_carries_no_steering_key(self):
        summary = mod._safe_event_summary(9, {
            "event": "steering_message_received",
            "metadata": {"message_id": "sm-0005", "text": "note", "channel": "cli"}})
        assert "steering" not in summary

    def test_an_unknown_kind_key_set_is_still_the_base_five(self):
        summary = mod._safe_event_summary(10, {"event": "some_other_kind", "timestamp": "t",
                                                "outcome": "ok"})
        assert set(summary) == {"seq", "event", "timestamp", "outcome", "task_id"}
