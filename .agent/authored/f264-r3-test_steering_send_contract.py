"""F264 — the cockpit's steering sender agrees with the server it sends to.

`apps/ui/src/api/steeringSend.ts` mirrors three facts the server owns, so the operator is
refused one round trip earlier: the message limit (`steering.STEERING_MAX_CHARS`), the job
states that take no message (`pingpong_job.JOB_TERMINAL_STATES`), and the command id
(`UI_EXPOSED_COMMANDS`). A mirror that drifts would refuse a message the server takes, or
send one it refuses, so each is read out of the TypeScript source and compared with its
Python original. The components are read as source too, because no DOM harness exists:
the cockpit reaches the door only through `sendSteeringMessage` (DECISION F264 D3).
"""
from __future__ import annotations

import re
from pathlib import Path

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
SENDER = UI_SRC / "api" / "steeringSend.ts"
CARD = UI_SRC / "components" / "panels" / "ActivityFeedCard.tsx"
CHAT_INPUT = UI_SRC / "components" / "panels" / "ChatInput.tsx"


def _sender() -> str:
    return strip_ts_comments(SENDER.read_text(encoding="utf-8"))


def test_the_message_limit_is_the_servers():
    from packages.orchestration.steering import STEERING_MAX_CHARS

    [value] = re.findall(r"export const STEERING_MAX_CHARS = (\d+);", _sender())
    assert int(value) == STEERING_MAX_CHARS


def test_the_ended_states_are_the_servers_terminal_states():
    from packages.orchestration.pingpong_job import JOB_TERMINAL_STATES

    [body] = re.findall(r"export const STEERING_ENDED_STATES: readonly string\[\] = \[([^\]]*)\];",
                        _sender())
    assert set(re.findall(r'"([^"]+)"', body)) == {s.value for s in JOB_TERMINAL_STATES}


def test_the_command_is_one_the_door_exposes():
    from apps.cli.command_catalog import UI_EXPOSED_COMMANDS

    [command] = re.findall(r'export const CHAT_SEND_COMMAND = "([^"]+)";', _sender())
    assert command in UI_EXPOSED_COMMANDS


def test_the_components_reach_the_door_only_through_the_sender():
    card = strip_ts_comments(CARD.read_text(encoding="utf-8"))
    chat = strip_ts_comments(CHAT_INPUT.read_text(encoding="utf-8"))
    assert "onSend={(text) => sendSteeringMessage(target, text)}" in card
    assert "steeringIsOpen(" in card
    for source in (card, chat):
        assert "fetch(" not in source and "XMLHttpRequest" not in source


def test_a_refused_message_keeps_the_operators_text():
    chat = strip_ts_comments(CHAT_INPUT.read_text(encoding="utf-8"))
    # The text is cleared only on acceptance: a refused message is never lost.
    assert chat.count('setText("")') == 1
    assert 'if (answer.tone === "ok") {\n      setText("");' in chat
