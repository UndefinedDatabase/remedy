"""Guard: the client's diff URL template agrees with the routes the server really has.

`apps/ui/src/api/remedyApi.ts` grew the DOOR the viewer fetches a diff envelope through
(`docs/roadmap/features/T5_F037.md`, T003). Its behaviour is proved by vitest in
`apps/ui/src/api/remedyApi.test.ts` — but vitest cannot see
`packages/orchestration/ui_server.py`, so the one agreement it can never check is the one
that spans both languages: whether the path the client BUILDS is a path the server ROUTES.
A client that addressed `/api/jobs/<id>/diffs` would pass every vitest assertion it has and
answer 404 in production.

This file is that check, and it is the only place in the repository where the two halves of
the diff route are read side by side. It reads all three files AS TEXT and imports nothing
from `apps/`, exactly as `tests/ui_contracts/test_diff_view_render.py` does.

Every assertion over the client runs on COMMENT-STRIPPED source. The door carries WHY
comments that NAME the very symbols asserted below — `readDiffEnvelope`, `parts[4]`,
`loadRemedyDashboard` — so an unstripped guard would be satisfied by the comment describing
the door rather than by the door (finding `R-0584`).
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CLIENT = REPO_ROOT / "apps" / "ui" / "src" / "api" / "remedyApi.ts"
CLIENT_TESTS = REPO_ROOT / "apps" / "ui" / "src" / "api" / "remedyApi.test.ts"
SERVER = REPO_ROOT / "packages" / "orchestration" / "ui_server.py"

VITEST_AUTHORITY = (
    "apps/ui/vitest.config.ts (environment: node, include: src/**/*.test.ts), "
    "DECISION F031 D5 and DECISION F037 D8"
)

# The server's own route conditions, quoted from `ui_server.py`'s `do_GET`. Each is a
# literal that route dispatch really turns on, so a rename on either side breaks a test
# here rather than a fetch in a browser.
SERVER_ROUTE_LITERALS = (
    '"diff": _build_diff_json',
    'parts[4] == "task-runs"',
    'parts[6] == "diff"',
)


def strip_ts_comments(text: str) -> str:
    """Drop `//` and `/* */` comments, the scanner `test_diff_view_render.py` uses.

    Neither file scanned through this holds a string literal carrying either marker, which
    is what lets so plain a scanner be trustworthy here.
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


def client_code() -> str:
    """The client with its prose removed — the only form the assertions below read."""
    return strip_ts_comments(CLIENT.read_text())


def ts_function_body(code: str, name: str) -> str:
    """The body of `export function <name>`, brace depth respected.

    Scoped rather than swept: `token=` occurs in `loadRemedyDashboard` too, so a whole-file
    search would be answered by the dashboard loader and would stay green with the diff
    path's token gone entirely.
    """
    match = re.search(rf"export (?:async )?function {name}\b", code)
    assert match, f"{CLIENT.name} exports no function named {name}"
    start = code.index("{", match.end())
    depth = 0
    for index in range(start, len(code)):
        if code[index] == "{":
            depth += 1
        elif code[index] == "}":
            depth -= 1
            if depth == 0:
                return code[start:index + 1]
    raise AssertionError(f"the body of {name} never closes in {CLIENT.name}")


def door_export_names(code: str) -> list[str]:
    """Every VALUE the door exports, derived from the module rather than listed.

    Scoped to names spelling `diff` because this module predates the door by many features
    and its earlier exports — `normalizePipeline`, `loadRemedyDashboard` — are gated
    elsewhere and are not this guard's subject. Types are deliberately out of scope, the
    same reach `tests/ui_contracts/test_diff_view_model.py` gives the model module: an
    `export interface` carries no runtime behaviour for a test to pin.
    """
    return re.findall(r"^export (?:async function|function|const) (\w*[Dd]iff\w*)", code, re.MULTILINE)


class TestTheStripperIsNotVacuous:
    """Without this, every assertion below is satisfiable by the door's own WHY comments,
    which name `readDiffEnvelope`, `parts[4]` and the route shapes verbatim."""

    def test_the_stripper_removes_both_comment_forms(self):
        sample = 'const a = 1; // note\n/* block */ const b = 2;'
        stripped = strip_ts_comments(sample)
        assert "note" not in stripped, "the // form must go"
        assert "block" not in stripped, "the /* */ form must go"
        assert "const b = 2;" in stripped, "and the code between them must survive"

    def test_the_client_really_loses_text_to_the_stripper(self):
        raw = CLIENT.read_text()
        assert "//" in raw and "/*" in raw, (
            f"{CLIENT.name} must keep the WHY comments the Code Discoverability Conventions "
            f"of AGENTS.md require; with no comment in the file the stripper proves nothing"
        )
        assert len(strip_ts_comments(raw)) < len(raw), (
            f"the stripper returned {CLIENT.name} unchanged, so every assertion in this "
            f"module would be satisfied by prose rather than by code (finding R-0584)"
        )

    def test_the_server_scan_finds_route_literals_at_all(self):
        server = SERVER.read_text()
        found = [literal for literal in SERVER_ROUTE_LITERALS if literal in server]
        assert len(found) > 0, (
            f"{SERVER.name} carries none of {list(SERVER_ROUTE_LITERALS)}; a route agreement "
            f"measured against an empty server side could not fail"
        )

    def test_the_export_scan_really_reaches_the_door(self):
        names = door_export_names(client_code())
        for expected in ("diffEnvelopePath", "loadDiffEnvelope"):
            assert expected in names, (
                f"the export scan over {CLIENT.name} found {names}, which does not include "
                f"{expected}; a reach test that found nothing would pass on an empty set"
            )


class TestTheJobScopeRouteAgrees:
    """(a) The job scope is dispatched by the five-segment route's handler dictionary, keyed
    on a single `parts[4]`. The client's path and that key are one agreement written twice."""

    def test_the_client_addresses_the_diff_endpoint(self):
        assert "/diff?" in client_code(), (
            f"{CLIENT.name} builds no path ending in the diff endpoint, so nothing the viewer "
            f"fetches would reach the handler {SERVER.name} registers for it"
        )

    def test_the_server_registers_the_diff_endpoint_in_its_handler_dictionary(self):
        assert '"diff": _build_diff_json' in SERVER.read_text(), (
            f"{SERVER.name} no longer registers a `diff` handler on the five-segment job "
            f"route, so the path {CLIENT.name} builds answers 404 — a break no vitest run "
            f"can see ({VITEST_AUTHORITY})"
        )


class TestTheTaskRunScopeRouteAgrees:
    """(b) The task-run scope needs a SECOND path segment, so the server spells it out as a
    structural route rather than a dictionary key. Both of its conditions are literals."""

    def test_the_client_addresses_the_task_run_segment(self):
        assert "task-runs" in client_code(), (
            f"{CLIENT.name} builds no task-run path, so a diff scoped to one attempt — half of "
            f"what T5_F037 T003 exists to fetch — is unreachable from the viewer"
        )

    def test_the_server_routes_both_segments_of_the_task_run_path(self):
        server = SERVER.read_text()
        for literal in ('parts[4] == "task-runs"', 'parts[6] == "diff"'):
            assert literal in server, (
                f"{SERVER.name} no longer tests `{literal}`, so the task-run path "
                f"{CLIENT.name} builds falls through to the 404 at the end of do_GET"
            )


class TestTheTokenTravelsOnTheDiffRoute:
    """(c) `ui_server.py` answers 403 to every `/api/` path whose `token` query parameter does
    not match, BEFORE any dispatch. A diff URL without it is refused, not routed."""

    def test_the_diff_path_carries_the_token_parameter(self):
        body = ts_function_body(client_code(), "diffEnvelopePath")
        assert "token=" in body, (
            f"diffEnvelopePath in {CLIENT.name} builds a URL with no token parameter; "
            f"{SERVER.name} rejects such a path with 403 before it looks at the route, so "
            f"every diff the viewer asked for would degrade to an unavailable envelope"
        )


class TestTheDoorNormalizesThroughOneFunction:
    """(d) DECISION F037 D8 and the model's own contract: a 403, a dead socket and a junk body
    must arrive as ONE total envelope. That is a property of the CODE, and the door's comment
    claiming it is exactly what this assertion must not be satisfied by."""

    def test_every_payload_leaves_the_door_through_the_reader(self):
        assert "readDiffEnvelope" in client_code(), (
            f"{CLIENT.name} never calls readDiffEnvelope, so a raw payload would reach the "
            f"viewer and every component downstream would have to be defensive a second time"
        )

    def test_the_loader_really_catches_a_rejection(self):
        body = ts_function_body(client_code(), "loadDiffEnvelope")
        assert "catch" in body, (
            f"loadDiffEnvelope in {CLIENT.name} has no catch clause, so a rejected fetch "
            f"propagates to the caller. The degradation path must be in the code, not only "
            f"in the WHY comment that promises it"
        )


class TestEveryDoorExportIsTested:
    """(e) The reach `tests/ui_contracts/test_diff_view_model.py` gives the model module: an
    export nobody imports is invisible to vitest and ships silently green."""

    def test_every_exported_door_name_is_named_by_the_vitest_suite(self):
        names = door_export_names(client_code())
        tests = strip_ts_comments(CLIENT_TESTS.read_text())
        untested = sorted({name for name in names if name not in tests})
        assert not untested, (
            f"{CLIENT.name} exports {untested} which {CLIENT_TESTS.name} never names, so "
            f"vitest cannot execute it and no gate in this repository would notice it break "
            f"({VITEST_AUTHORITY})"
        )
