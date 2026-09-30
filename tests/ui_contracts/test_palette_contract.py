"""Contract test: the palette's command list and the bar's routing rule agree with Python.

DECISION F044 D1 makes the write door's exposed set, ``UI_EXPOSED_COMMANDS`` in
``apps/cli/command_catalog.py``, the one source of the palette's commands, and the chat's
parse, ``parse_chat_intent`` in ``packages/orchestration/chat_intent.py``, the one source of
the bar's routing rule. This test reads ``apps/ui/src/api/paletteCommands.ts`` and
``paletteRouting.ts`` as COMMENT-STRIPPED source text, the way the other tests in this
directory read the TypeScript they gate, and runs the shared fixtures in
``paletteRouting.goldens.json`` through the chat's parse. Drift goes red from either side: a
command the door gains or loses, a chat title or required argument that changes, a verb or
question word one language reads and the other does not.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from apps.cli.command_catalog import UI_EXPOSED_COMMANDS
from packages.orchestration.chat_intent import (
    _NOTE_PATTERN,
    _QUESTION_WORDS,
    _RERUN_WORDS,
    _STOP_WORDS,
    _UNPAUSE_WORDS,
    _VETO_WORDS,
    CHAT_INTENT_ACTION,
    CHAT_INTENT_QUESTION,
    CHAT_INTENT_UNKNOWN,
    CHAT_VERB_REQUIRED_ARGS,
    CHAT_VERB_TITLES,
    parse_chat_intent,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
API_DIR = REPO_ROOT / "apps" / "ui" / "src" / "api"
COMMANDS_TS = API_DIR / "paletteCommands.ts"
ROUTING_TS = API_DIR / "paletteRouting.ts"
GOLDENS = API_DIR / "paletteRouting.goldens.json"
COMPONENTS_DIR = REPO_ROOT / "apps" / "ui" / "src" / "components"

#: One entry of `PALETTE_COMMANDS`, in the shape the list is required to keep: one field per
#: line, four spaces in, the arguments between `args: [` and the `],` that closes the entry.
ENTRY = re.compile(
    r'^    command: "([^"]+)",\n'
    r'    title: "([^"]*)",\n'
    r'    flow: "(\w+)",\n'
    r'    surface: "([^"]*)",\n'
    r'    args: \[(.*?)\],\n'
    r'  \},$',
    re.MULTILINE | re.DOTALL,
)
ARG = re.compile(r'\{ name: "(\w+)", kind: "(\w+)", required: (true|false), prompt: "([^"]*)" \}')
COMMAND_FIELD = re.compile(r'^\s*command: "', re.MULTILINE)


def strip_ts_comments(text: str) -> str:
    """Drop // and /* */ comments, keeping the newlines that end line comments so
    line-anchored scanning still sees the file's line structure."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        pair = text[i:i + 2]
        if pair == "//":
            nl = text.find("\n", i)
            i = n if nl == -1 else nl
        elif pair == "/*":
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def palette_entries() -> list[dict]:
    source = strip_ts_comments(COMMANDS_TS.read_text(encoding="utf-8"))
    entries = []
    for command, title, flow, surface, args in ENTRY.findall(source):
        entries.append({
            "command": command, "title": title, "flow": flow, "surface": surface,
            "args": [{"name": n, "kind": k, "required": r == "true", "prompt": p}
                     for n, k, r, p in ARG.findall(args)],
            "arg_text": args,
        })
    assert len(entries) == len(COMMAND_FIELD.findall(source)), "an entry left the required shape"
    return entries


def ts_string_list(source: str, name: str) -> list[str]:
    match = re.search(rf"export const {name}: readonly string\[\] = \[(.*?)\];", source, re.DOTALL)
    assert match, name
    return re.findall(r'"([^"]*)"', match.group(1))


def ts_verb_table(source: str) -> dict[str, str]:
    match = re.search(
        r"export const BAR_LEADING_VERBS: Readonly<Record<string, string>> = \{(.*?)\n\};",
        source, re.DOTALL)
    assert match
    return dict(re.findall(r'^  (\w+): "([^"]+)",$', match.group(1), re.MULTILINE))


# ---------------------------------------------------------------------------
# The command list against the write door and the chat.
# ---------------------------------------------------------------------------

def test_the_list_and_its_continuations_are_the_exposed_set():
    source = strip_ts_comments(COMMANDS_TS.read_text(encoding="utf-8"))
    listed = [entry["command"] for entry in palette_entries()]
    continuations = ts_string_list(source, "PALETTE_CONTINUATION_COMMANDS")
    assert len(listed) == len(set(listed))
    assert not set(listed) & set(continuations)
    assert set(listed) | set(continuations) == set(UI_EXPOSED_COMMANDS)


def test_every_argument_is_parsed_whole():
    for entry in palette_entries():
        rebuilt = len(entry["args"])
        written = entry["arg_text"].count("{ name:")
        assert rebuilt == written, entry["command"]


def test_a_title_the_chat_uses_is_the_chat_s_title():
    shared = [entry for entry in palette_entries() if entry["command"] in CHAT_VERB_TITLES]
    assert shared
    for entry in shared:
        assert entry["title"] == CHAT_VERB_TITLES[entry["command"]], entry["command"]


def test_a_sent_command_requires_exactly_the_chat_s_required_arguments():
    sent = [entry for entry in palette_entries()
            if entry["flow"] == "send" and entry["command"] in CHAT_VERB_REQUIRED_ARGS]
    assert sent
    for entry in sent:
        required = tuple(arg["name"] for arg in entry["args"] if arg["required"])
        assert required == CHAT_VERB_REQUIRED_ARGS[entry["command"]], entry["command"]


def test_every_surface_is_a_region_the_cockpit_renders():
    markup = "\n".join(path.read_text(encoding="utf-8") for path in sorted(COMPONENTS_DIR.rglob("*.tsx")))
    surfaces = [entry["surface"] for entry in palette_entries() if entry["flow"] == "surface"]
    assert surfaces
    for surface in surfaces:
        assert f'data-ui="{surface}"' in markup, surface


# ---------------------------------------------------------------------------
# The routing rule against the chat's parse.
# ---------------------------------------------------------------------------

def routing_source() -> str:
    return strip_ts_comments(ROUTING_TS.read_text(encoding="utf-8"))


def test_the_question_words_are_the_chat_s():
    assert tuple(ts_string_list(routing_source(), "BAR_QUESTION_WORDS")) == _QUESTION_WORDS


def test_the_note_openers_are_the_chat_s():
    openers = ts_string_list(routing_source(), "BAR_NOTE_OPENERS")
    assert _NOTE_PATTERN.pattern.startswith("^(?:" + "|".join(openers) + r")\b")


def test_the_leading_verbs_are_the_chat_s_and_name_its_commands():
    verbs = ts_verb_table(routing_source())
    assert set(verbs) == set(_STOP_WORDS | {"pause"} | _UNPAUSE_WORDS | _VETO_WORDS | _RERUN_WORDS)
    for word, command in verbs.items():
        intent = parse_chat_intent(word, focused_task_id="t1")
        assert (intent.kind, intent.verb) == (CHAT_INTENT_ACTION, command), word


GOLDEN_ROWS = json.loads(GOLDENS.read_text(encoding="utf-8"))


@pytest.mark.parametrize("row", GOLDEN_ROWS, ids=[f"{i}" for i in range(len(GOLDEN_ROWS))])
def test_the_chat_parses_every_golden_line_the_way_the_bar_routes_it(row):
    intent = parse_chat_intent(row["text"], focused_task_id=row["focused"])
    if row["route"] == "chat":
        assert intent.kind == CHAT_INTENT_QUESTION
    elif row["route"] == "command":
        assert (intent.kind, intent.verb) == (CHAT_INTENT_ACTION, row["command"])
    else:
        assert row["route"] in ("palette", "none")
        assert intent.kind == CHAT_INTENT_UNKNOWN
