"""F030 T003 — the cockpit's steering note agrees with the server it reads from.

`apps/ui/src/api/steeringNote.ts` reads the stream's `note` field and `steeringSend.ts`
sends `job.steer`; both mirror facts the server owns, so each is read out of the
TypeScript source and compared with its Python original, exactly as
`test_steering_send_contract.py` does for `chat.send`. The copy audit is here rather than
in a component test because DECISION F030 D3 is a REPOSITORY-WIDE promise: no file under
`apps/ui/src` may say Remedy composes a reply to a steering note.
"""
from __future__ import annotations

import re
from pathlib import Path

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
NOTE = UI_SRC / "api" / "steeringNote.ts"
SENDER = UI_SRC / "api" / "steeringSend.ts"
HUMANIZE_CATALOG = UI_SRC / "api" / "humanizeCatalog.ts"

#: The four sentences a browser file must never say about a steering note, since Remedy
#: composes none: the retired placeholder and every way of narrating a reply that isn't one.
FORBIDDEN_COPY = ("Ask something", "Builder says", "Remedy says", "replied")


def _note() -> str:
    return strip_ts_comments(NOTE.read_text(encoding="utf-8"))


def _sender() -> str:
    return strip_ts_comments(SENDER.read_text(encoding="utf-8"))


def test_the_note_event_is_declared():
    from packages.orchestration.event_names import EVENT_NAMES

    [event] = re.findall(r'export const STEERING_NOTE_EVENT = "([^"]+)";', _note())
    assert event in EVENT_NAMES


def test_the_note_fields_are_the_servers():
    from packages.orchestration.ui_server import _steering_note_summary_payload

    fields = set(re.findall(r'note\["([a-z_]+)"\]', _note()))
    assert fields == set(_steering_note_summary_payload({}))


def test_the_steer_command_is_one_the_door_exposes():
    from apps.cli.command_catalog import UI_EXPOSED_COMMANDS

    [command] = re.findall(r'export const STEER_TASK_COMMAND = "([^"]+)";', _sender())
    assert command in UI_EXPOSED_COMMANDS


def test_the_reply_framing_occurs_once_at_column_zero_and_says_what_it_means():
    catalog = strip_ts_comments(HUMANIZE_CATALOG.read_text(encoding="utf-8"))
    matches = re.findall(r"(?m)^export const STEERING_REPLY_FRAMING =", catalog)
    assert len(matches) == 1
    [value] = re.findall(r'STEERING_REPLY_FRAMING =\s*\n?\s*"([^"]+)"', catalog)
    assert "never writes a reply" in value


def test_no_browser_file_promises_a_conversation():
    for path in sorted(UI_SRC.rglob("*.ts")) + sorted(UI_SRC.rglob("*.tsx")):
        if path.name.endswith(".test.ts") or path.name.endswith(".test.tsx"):
            continue
        text = strip_ts_comments(path.read_text(encoding="utf-8"))
        for phrase in FORBIDDEN_COPY:
            assert phrase not in text, f"{path.relative_to(UI_SRC)} says {phrase!r}"
