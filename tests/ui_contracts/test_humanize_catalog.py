"""Contract test: the humanize catalog's key set IS the Python stream vocabulary.

DECISION F021 D3 rules that T001's coverage constant is DERIVED rather than
hand-seeded, so this test re-derives the set of event kinds a reader can actually
receive from the Python sources and asserts it EQUALS the key set of
``apps/ui/src/api/humanizeCatalog.ts``. Drift then goes red from EITHER side: a
new Python emitter with no catalog entry, and a catalog entry no emitter can
produce.

Remedy deliberately asserts SET EQUALITY and never a literal size here. A number
written down beside the catalog would be a second source of truth, and the one
this feature started from was already wrong.

The catalog is read as SOURCE TEXT, the way every other test in this directory
reads the TypeScript it gates, and every assertion runs against COMMENT-STRIPPED
source: a key named inside the WHY comment above the definition must not satisfy
a guard about the data below it (finding R-0584).
"""
from __future__ import annotations

import ast
import re
from functools import lru_cache
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CATALOG = REPO_ROOT / "apps" / "ui" / "src" / "api" / "humanizeCatalog.ts"
TRACE_MODULE = REPO_ROOT / "packages" / "orchestration" / "agent_run_trace.py"
UI_SERVER_MODULE = REPO_ROOT / "packages" / "orchestration" / "ui_server.py"

#: The roots DECISION F021 D3 measures. `packages/` alone was the scope error the
#: decision corrects: the eleven narrated events are emitted from `apps/cli/`.
EMITTER_ROOTS = ("packages", "apps", "scripts")

#: One catalog entry, in the shape the catalog is required to keep:
#: two spaces, a double-quoted key, a colon, one space, a double-quoted line.
CATALOG_ENTRY = re.compile(r'^  "([^"]+)": "', re.MULTILINE)


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


def extract_catalog_keys(source: str) -> list[str]:
    """The catalog keys, in file order, from comment-stripped TypeScript source."""
    return CATALOG_ENTRY.findall(strip_ts_comments(source))


def _event_argument(call: ast.Call) -> ast.expr | None:
    """The event argument of a run-log emission call, or None if this is not one.

    A call site qualifies when the callee is an attribute named ``log`` or
    ``append_run_event``, or a bare name ``append_run_event``, and an event
    argument is present: the first positional argument for ``log``, or the
    ``event=`` keyword for either.
    """
    func = call.func
    if isinstance(func, ast.Attribute):
        name = func.attr
    elif isinstance(func, ast.Name):
        name = func.id
        if name != "append_run_event":
            return None
    else:
        return None
    if name not in ("log", "append_run_event"):
        return None
    for keyword in call.keywords:
        if keyword.arg == "event":
            return keyword.value
    if name == "log" and call.args:
        return call.args[0]
    return None


@lru_cache(maxsize=1)
def emission_literals() -> frozenset[str]:
    """Distinct string-constant event names passed at run-log emission sites.

    The sites that compute their name at runtime cannot be reached by any static
    walk. They are covered by the generic line in ``humanize.ts`` instead, which
    is why that line is a contract and not a nicety.
    """
    names: set[str] = set()
    for root in EMITTER_ROOTS:
        for path in sorted((REPO_ROOT / root).rglob("*.py")):
            try:
                tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                argument = _event_argument(node)
                if isinstance(argument, ast.Constant) and isinstance(argument.value, str):
                    names.add(argument.value)
    return frozenset(names)


def _module_assignments(path: Path) -> dict[str, ast.expr]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: dict[str, ast.expr] = {}
    for node in tree.body:
        targets = (
            node.targets if isinstance(node, ast.Assign)
            else [node.target] if isinstance(node, ast.AnnAssign) and node.value
            else []
        )
        for target in targets:
            if isinstance(target, ast.Name):
                found[target.id] = node.value
    return found


@lru_cache(maxsize=1)
def trace_event_kinds() -> frozenset[str]:
    """``TRACE_EVENT_KINDS`` — the JobPlan branch of ``_load_events`` writes these
    straight into the envelope's ``event`` field, so a reader receives them."""
    value = _module_assignments(TRACE_MODULE)["TRACE_EVENT_KINDS"]
    assert isinstance(value, ast.Call), "TRACE_EVENT_KINDS must stay a frozenset({...})"
    return frozenset(element.value for element in value.args[0].elts)


@lru_cache(maxsize=1)
def stream_owned_kinds() -> frozenset[str]:
    """The VALUES of ``_STREAM_EVENT_KINDS`` — the trace kinds normalized stream
    events become. The keys are stream event TYPES and never reach the feed."""
    value = _module_assignments(TRACE_MODULE)["_STREAM_EVENT_KINDS"]
    assert isinstance(value, ast.Dict), "_STREAM_EVENT_KINDS must stay a dict literal"
    return frozenset(item.value for item in value.values)


@lru_cache(maxsize=1)
def command_accepted_kind() -> str:
    """``COMMAND_ACCEPTED_EVENT`` reaches the stream through a module constant
    rather than a call-site literal, so the AST walk above cannot see it."""
    value = _module_assignments(UI_SERVER_MODULE)["COMMAND_ACCEPTED_EVENT"]
    assert isinstance(value, ast.Constant) and isinstance(value.value, str)
    return value.value


def static_stream_vocabulary() -> frozenset[str]:
    """Every event kind a reader can receive that can be enumerated statically."""
    return (
        emission_literals()
        | trace_event_kinds()
        | stream_owned_kinds()
        | {command_accepted_kind()}
    )


class TestCommentStripping:
    def test_stripper_removes_a_comment_the_file_really_carries(self):
        raw = CATALOG.read_text()
        assert "// The stream event kinds this UI can name" in raw, (
            "the catalog must keep its WHY comment"
        )
        assert "The stream event kinds this UI can name" not in strip_ts_comments(raw), (
            "stripper must remove it"
        )


class TestKeyExtractor:
    def test_extractor_finds_a_key_the_catalog_really_carries(self):
        keys = extract_catalog_keys(CATALOG.read_text())
        assert "verification_passed" in keys, (
            "the extractor must read real catalog entries, or the equality below "
            "is an assertion about the empty set"
        )

    def test_a_key_written_only_inside_a_comment_is_not_extracted(self):
        source = (
            '// "commented_out_kind": "A line nobody renders.",\n'
            'export const STREAM_EVENT_CATALOG = {\n'
            '  // "another_commented_kind": "Also not data.",\n'
            '  "real_kind": "A line a feed row renders.",\n'
            '};\n'
        )
        assert extract_catalog_keys(source) == ["real_kind"], (
            "a key inside a comment must not count as a catalog entry"
        )

    def test_extractor_reads_every_entry_line_of_the_catalog(self):
        keys = extract_catalog_keys(CATALOG.read_text())
        assert len(keys) == len(set(keys)), (
            f"duplicate catalog keys: {sorted(k for k in set(keys) if keys.count(k) > 1)}"
        )


class TestDerivation:
    def test_the_emitter_walk_finds_call_sites(self):
        assert emission_literals(), "the AST walk found no run-log emission literal"

    def test_the_defined_trace_sets_are_read(self):
        assert trace_event_kinds(), "TRACE_EVENT_KINDS came back empty"
        assert stream_owned_kinds(), "_STREAM_EVENT_KINDS values came back empty"
        assert command_accepted_kind() == "command.accepted"


class TestCatalogCoversTheStreamVocabulary:
    def test_the_catalog_is_non_empty(self):
        assert extract_catalog_keys(CATALOG.read_text()), "no catalog entry was read"

    def test_the_derived_vocabulary_is_non_empty(self):
        assert static_stream_vocabulary(), "the derived kind set is empty"

    def test_catalog_keys_equal_the_static_stream_vocabulary(self):
        catalogued = set(extract_catalog_keys(CATALOG.read_text()))
        derived = set(static_stream_vocabulary())
        missing = sorted(derived - catalogued)
        extra = sorted(catalogued - derived)
        assert not missing and not extra, (
            "the humanize catalog has drifted from the Python emitters.\n"
            f"emitted but NOT in the catalog ({len(missing)}): {missing}\n"
            f"in the catalog but NOT emitted ({len(extra)}): {extra}"
        )
