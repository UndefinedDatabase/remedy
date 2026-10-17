"""An order's deliverables apart from its constraints (DECISION amend1016p D1).

On 2026-10-16 a README order of two sentences became two jobs and six tasks: the planner turned
"change only README.md", "run npm test" and "apply nothing automatically" into work of their own
(checksum manifests, a comparison copy, a modification report), and the report file it asked for
failed the review. Those sentences are CONSTRAINTS: Remedy already enforces each of them with its
own mechanisms (the scope guard, the DoD's project tests, the stop before apply, the reviewer).
They bind the work; they are never a deliverable, a milestone, a job or a task by themselves.

`split_order_scope` sorts an order's sentences by fixed patterns, English and German, with no
model call (a classifier call would spend a provider call to decide whether to spend provider
calls). A sentence that names a file is a deliverable unless it is a scope fence ("only README.md",
"no other files"). An order made only of constraints ("run npm test and report the result") asks
for exactly that work, so its sentences are then its deliverables.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

#: The block `order_file.parse_order_file_text` appends for header `constraint:` lines.
HEADER_CONSTRAINTS_MARKER = "\n\nConstraints the plan must honour:\n"

_UNIT_BREAK_RE = re.compile(r"(?<=[.!?])\s+|;\s*|\n+")
_LIST_MARKER_RE = re.compile(r"^[ \t]*(?:[-*+]|\d+[.)]|#{1,6})[ \t]+", re.MULTILINE)
_QUOTED_RE = re.compile(r"```.*?```|`[^`\n]*`|\"[^\"\n]*\"|„[^“”\n]*[“”]|“[^”\n]*”|«[^»\n]*»", re.DOTALL)
# A line that announces literal content ("… mit genau diesen zwei Sätzen:", "… with this text:"): the
# lines after it, up to the next blank line, are that part's PAYLOAD, never parts of their own. On
# 2026-10-17 the two sentences to insert counted as two more deliverables, so a one-file README order
# was "several things" and walked the full lane. A payload may open with a Markdown heading and a
# blank line ("… diesen Abschnitt:\n\n## Testbetrieb\n\nDieses …"): the heading and the paragraph
# after it are one payload (lab order of 2026-10-17, 16:00).
_PAYLOAD_INTRO_RE = re.compile(
    r"\b(?:sätzen?|satz|texte?s?|zeilen?|inhalt|wortlaut|absatz|absätzen?|abschnitt\w*|überschrift\w*|"
    r"folgendes|sentences?|lines?|text|content|wording|paragraphs?|sections?|headings?)\b[^:\n]{0,40}:"
    r"[ \t]*\n(?:[ \t]*\n)?(?:[ \t]*#{1,6}[ \t][^\n]*\n(?:[ \t]*\n)?)?(?=[ \t]*\S)(?:[^\n]*\S[^\n]*(?:\n|$))+",
    re.IGNORECASE)
_PATH_RE = re.compile(r"[\w./-]+\.[A-Za-z0-9]{1,8}\b")

# Scope fences: the files the work may touch.
_SCOPE = re.compile(
    r"\b(?:only|exclusively|ausschlie(?:ß|ss)lich|nur)\b.{0,60}\b(?:change|modify|edit|touch|"
    r"änder\w*|veränder\w*|bearbeit\w*)"
    r"|\b(?:change|modify|edit|touch|änder\w*|veränder\w*)\b.{0,30}\b(?:only|ausschlie(?:ß|ss)lich|nur)\b"
    r"|\b(?:no|keine)\s+(?:other|anderen?|weiteren?|zusätzlichen?|unrelated|new|neuen?)\s+(?:files?|dateien?)\b"
    r"|\bdo(?:\s+not|n't)\s+(?:create|add|change|modify|touch)\s+(?:any\s+)?(?:other|unrelated|new|extra)\s+files?\b"
    # "Verändere sonst nichts", "change nothing else", "leave everything else unchanged".
    r"|\b(?:change|modify|edit|touch|änder\w*|veränder\w*|bearbeit\w*)\b.{0,20}"
    r"\b(?:(?:sonst|ansonsten)\s+nichts|nichts\s+(?:anderes|weiteres|sonst)|nothing\s+else|anything\s+else)\b"
    r"|\b(?:alles\s+andere|everything\s+else)\b.{0,30}\b(?:unverändert|unchanged|untouched|as\s+it\s+is)\b"
    # "füge keine Abhängigkeiten hinzu", "add no dependencies", "don't add any dependencies".
    r"|\b(?:no|keine)\s+(?:new\s+|neuen?\s+|external\s+|externen?\s+)?(?:dependencies|abhängigkeiten)\b"
    r"|\bdo(?:\s+not|n't)\s+add\s+(?:any\s+)?(?:new\s+)?dependencies\b",
    re.IGNORECASE)
# Running or passing the project's own tests ("Führe den vorhandenen Testbefehl aus" names no "test").
_TESTS = re.compile(
    r"\b(?:run|execute|führ\w*|start\w*)\b.{0,40}\b(?:tests?|test\s?suite|npm\s+test|pytest|"
    r"testsuite|unit\s?tests?|test[\s-]?(?:command|script|runner)s?|test(?:befehl|kommando|skript|lauf)\w*|"
    r"(?:projekt|project)[\s-]?tests?)\b"
    r"|\b(?:tests?|test\s?suite|testsuite)\b.{0,30}\b(?:pass|passes|stay\s+green|green|bestehen|grün)\b"
    r"|\bmake\s+sure\b.{0,20}\btests?\b",
    re.IGNORECASE)
# Approval: nothing lands on its own.
_APPROVAL = re.compile(
    r"\b(?:do\s+not|don't|never|nicht|keine?)\b.{0,40}\b(?:apply|merge|commit|push|übernimm\w*|"
    r"übernehm\w*|anwend\w*|automatisch\w*|automatically)\b"
    r"|\b(?:apply|übernimm\w*)\b.{0,30}\b(?:nothing|nichts)\b",
    re.IGNORECASE)
# Reviewing the result or reporting the outcome, which Remedy's own review and story do.
_REVIEW = re.compile(
    r"^(?:please\s+|bitte\s+)?(?:review|check|prüf\w*|kontrollier\w*)\b.{0,30}\b(?:diff|change|changes|"
    r"änderung\w*|result|ergebnis)\b"
    r"|^(?:please\s+|bitte\s+)?(?:report|berichte\w*|melde\w*)\b.{0,40}\b(?:outcome|result|results|"
    r"ergebnis\w*|status)?",
    re.IGNORECASE)

#: Plan items that only produce a checking artifact, never the requested change itself.
_CHECKING_ARTIFACT = re.compile(
    r"\b(?:manifest\w*|checksums?|hash(?:es)?|snapshot\w*|baseline\w*|comparison\s+copy|"
    r"compare\s+(?:the\s+)?manifests?|modification\s+report|change\s+report|report\s+file|"
    r"before[- ]after|pre-run|post-run|prüfsumme\w*)\b",
    re.IGNORECASE)
_CHECKING_REQUEST = re.compile(
    r"\b(?:manifest\w*|checksums?|hash(?:es)?|snapshot\w*|baseline\w*|prüfsumme\w*|audit\w*)\b"
    r"|\b(?:write|create|generate|produce|save|erstell\w*|schreib\w*|generier\w*)\b.{0,40}"
    r"\b(?:report|bericht)\w*"
    r"|\b(?:report|bericht)\w*\s+(?:file|datei)\b|[\w-]*(?:report|bericht)[\w-]*\.\w{1,5}\b",
    re.IGNORECASE)

_RUNS_SOMETHING = re.compile(r"(?:please\s+|bitte\s+)?(?:run|execute|führ\w*|start\w*)\b", re.IGNORECASE)
_ACTION_SPLIT_RE = re.compile(r",|;|\band\b|\bund\b|\bthen\b|\bdann\b|\bsowie\b", re.IGNORECASE)
_ACTION_VERBS = frozenset({
    "add", "create", "write", "implement", "fix", "refactor", "remove", "delete", "rename",
    "update", "change", "migrate", "move", "replace", "extend", "build", "document", "introduce",
    "convert", "split", "merge", "ergänze", "füge", "erstelle", "schreibe", "implementiere",
    "behebe", "entferne", "lösche", "benenne", "aktualisiere", "ändere", "migriere", "verschiebe",
    "ersetze", "erweitere", "baue", "dokumentiere", "führe", "teile", "repariere", "korrigiere",
    "repair", "correct",
})
#: An order whose deliverables hold more actions than this asks for several things.
MAX_SIMPLE_ACTIONS = 2
#: An order whose deliverables run longer than this many sentences has several parts.
MAX_SIMPLE_SENTENCES = 2


@dataclass(frozen=True)
class OrderScope:
    """An order sorted: what to deliver and what binds it. Its layout (list, heading, semicolon) never counts."""

    deliverables: tuple[str, ...]
    constraints: tuple[str, ...]

    @property
    def actions(self) -> int:
        """How many separate actions the deliverables ask for, by their leading verbs."""
        return sum(_sentence_actions(sentence) for sentence in self.deliverables)

    @property
    def simple(self) -> bool:
        """Few parts, few actions: the same words in a list, with semicolons or in prose count the same.

        A sentence that asks for no action only describes ("add(a, b) in src/calc.js rechnet falsch",
        "Zeige durch den Test, dass …"): it is no part of its own while another sentence asks for the
        work (lab calc order of 2026-10-17, which those two sentences sent to the full lane).
        """
        working = [s for s in self.deliverables if _sentence_actions(s)]
        parts = working or self.deliverables
        return 0 < len(parts) <= MAX_SIMPLE_SENTENCES and self.actions <= MAX_SIMPLE_ACTIONS

    @property
    def single(self) -> bool:
        """Exactly one part asking for at most one action."""
        return len(self.deliverables) == 1 and self.actions <= 1


_PAYLOAD_HEAD_RE = re.compile(_PAYLOAD_INTRO_RE.pattern.split(r"[ \t]*\n", 1)[0] + r"(?=\s*\S)", re.IGNORECASE)


def order_unit_head(unit: str) -> str:
    """The words of a part that ASK, without the literal payload it announces (the text to insert):
    "Ergänze … mit genau diesen zwei Sätzen: Dieses Repository …" asks "Ergänze … Sätzen:"."""
    head = _PAYLOAD_HEAD_RE.search(unit)
    return unit[:head.end()] if head else unit


def _sentence_actions(sentence: str) -> int:
    """How many clauses of *sentence* start with an action verb."""
    count = 0
    for clause in _ACTION_SPLIT_RE.split(order_unit_head(sentence)):
        words = clause.strip().lower().split()
        count += bool(words) and words[0].strip("„\"'(") in _ACTION_VERBS
    return count


def _binds(clause: str) -> bool:
    return bool(_SCOPE.search(clause) or _TESTS.search(clause) or _APPROVAL.search(clause))


def _has_work_clause(sentence: str) -> bool:
    """A clause that starts with an action verb and is no fence, test run or approval of its own:
    "Fix parse.py, add tests and change no other files" carries work beside its fence."""
    for clause in _ACTION_SPLIT_RE.split(order_unit_head(sentence)):
        words = clause.strip().lower().split()
        if words and words[0].strip("„\"'(") in _ACTION_VERBS and not _binds(clause):
            return True
    return False


def is_constraint_sentence(sentence: str) -> bool:
    """True when *sentence* only binds the work: a scope fence, a test run, approval, review or a report."""
    text = order_unit_head(sentence.strip())
    if _has_work_clause(text):
        return False
    if _SCOPE.search(text):
        return True
    if _PATH_RE.search(text) and not _RUNS_SOMETHING.match(text):
        return False        # it names a file to work on ("run pytest tests/x.py" stays a test run)
    return bool(_TESTS.search(text) or _APPROVAL.search(text) or _REVIEW.search(text))


def is_scope_fence(sentence: str) -> bool:
    """True when *sentence* fences the work to files ("change only README.md")."""
    return bool(_SCOPE.search(sentence))


def split_order_scope(order: str) -> OrderScope:
    """Sort *order*'s sentences into deliverables and constraints (header constraints included)."""
    body, _, header_block = order.partition(HEADER_CONSTRAINTS_MARKER)
    header = tuple(line[2:].strip() for line in header_block.splitlines() if line.startswith("- "))
    sentences = _order_units(body)
    constraints = [s for s in sentences if is_constraint_sentence(s)]
    deliverables = [s for s in sentences if s not in constraints]
    if not deliverables:
        deliverables, constraints = sentences, []       # the constraints ARE the order
    return OrderScope(tuple(deliverables), tuple(constraints) + header)


def _mask_after_colon(intro: str) -> str:
    colon = intro.index(":") + 1
    return intro[:colon] + "\0" * (len(intro) - colon)


def _order_units(body: str) -> list[str]:
    """The sentences, list items and semicolon clauses of an order, in order, without list markers.

    Quoted text ("Hello; world") and the literal payload a line announces ("… these two sentences:")
    are never split, and a line that only introduces a list ("Do this:") is no part of its own.
    """
    # List markers become spaces, not nothing, so `text` and `masked` keep the same positions while
    # the payload is still found by the heading marker it may open with.
    raw = body.strip()
    text = _LIST_MARKER_RE.sub(lambda m: " " * len(m.group()), raw)
    masked = _QUOTED_RE.sub(lambda m: "\0" * len(m.group()), raw)
    masked = _PAYLOAD_INTRO_RE.sub(lambda m: _mask_after_colon(m.group()), masked)
    masked = _LIST_MARKER_RE.sub(lambda m: " " * len(m.group()), masked)
    units: list[str] = []
    start = 0
    for brk in [*_UNIT_BREAK_RE.finditer(masked), None]:
        end = len(text) if brk is None else brk.start()
        unit = " ".join(text[start:end].split())
        if brk is not None:
            start = brk.end()
        if unit.rstrip(";") and not (unit.endswith(":") and not _PATH_RE.search(unit)):
            units.append(unit)
    return units


# Writing a test is a deliverable ("add a regression test"); running the suite is a constraint.
_TEST_REQUEST = re.compile(
    r"\b(?:add|write|create|extend|include|ergänze\w*|schreib\w*|erstell\w*|füg\w*)\s+"
    r"(?:(?:a|an|some|new|the|more|einen|ein|eine|neue[nr]?|weitere)\s+)*"
    r"(?:(?:regression|unit|failing|reproducing)[ -]?)?(?:tests?|test\s?cases?|testfall|testfälle|"
    r"regressions?tests?)\b", re.IGNORECASE)
_TEST_PATH = re.compile(
    r"(?:^|/)(?:tests?|__tests__|spec|specs)/|(?:^|/)test_[^/]*$|[._-](?:test|spec)\.[A-Za-z0-9]+$"
    r"|_test\.go$", re.IGNORECASE)


def order_test_request(order: str) -> str:
    """The sentence of *order* that asks for the project's tests to RUN or pass, or "" when none does.

    A constraint, a header `constraint:` line or a deliverable ("make sure the tests pass") counts;
    a test the order asks to WRITE is a deliverable (`requests_test_files`), not a run.
    """
    scope = split_order_scope(order)
    return next((s for s in (*scope.constraints, *scope.deliverables) if _TESTS.search(order_unit_head(s))), "")


def requests_test_files(order: str) -> bool:
    """True when the order's DELIVERABLES ask for a test to be written (running tests does not count)."""
    return any(_TEST_REQUEST.search(s) for s in split_order_scope(order).deliverables)


def is_test_path(path: str) -> bool:
    """True when *path* is by its location or name a test file, whatever the language."""
    return bool(_TEST_PATH.search(path))


def is_checking_only(text: str, *, requested: str) -> bool:
    """True when a plan item (*text*) only produces a checking artifact *requested* did not ask for.

    A milestone or task of that kind (a checksum manifest, a comparison copy, a modification
    report) adds a file and a round and proves nothing Remedy's own guards do not already prove.
    """
    # A file name spells its words with `_` and `-` (change_report.md): read it as the words it is.
    words = text.replace("_", " ").replace("-", " ")
    return bool(_CHECKING_ARTIFACT.search(words)) and not _CHECKING_REQUEST.search(requested)


#: A plan item about the project's tests having run or passing, also in the planner's passive voice.
_TESTS_DONE = re.compile(
    r"\b(?:npm\s+test|pytest|test\s?suite|testsuite|tests?)\b.{0,40}\b(?:run|ran|executed|"
    r"pass\w*|green|captured|ausgeführt|bestanden|grün)\b", re.IGNORECASE)


def is_binding_plan_item(text: str, *, order: str) -> bool:
    """True when a planner's milestone or outline (*text*) only binds or checks the work.

    A checking artifact *order* never asked for binds even when it names a file (`checksums.json`,
    `change_report.md`): a file name is not a request. Any other item that names a file is work on
    that file, whatever fence it also states. Otherwise it binds when it is about the tests
    running or passing, approval, review or a report.
    """
    if is_checking_only(text, requested=order):
        return True
    if _PATH_RE.search(text) and not _RUNS_SOMETHING.match(text.strip()):
        return False
    return bool(_TESTS.search(text) or _TESTS_DONE.search(text) or _APPROVAL.search(text)
                or _REVIEW.search(text.strip()))


def _asks_for_work(order: str) -> bool:
    """True when *order* has a deliverable beyond its constraints (a test-only order has none)."""
    return any(not is_constraint_sentence(s) for s in split_order_scope(order).deliverables)


def work_milestones(drafts: list[Any], order: str) -> list[dict[str, Any]]:
    """The planner's milestones (as dicts) without those that are only a constraint or a check.

    "Run npm test" or "the codebase is unchanged after the tests" is no milestone when the order
    asks for real work: the DoD runs the tests and the scope guard holds the files. Nothing is
    dropped for an order that is itself only a test run or a report. A plan of nothing but
    constraints and checking artifacts comes back EMPTY, never as the original (R-1336 left that
    fallback keeping the unrequested artifact): the caller takes the deterministic plan instead.
    """
    dumps = [draft.model_dump() for draft in drafts]
    if not _asks_for_work(order):
        return dumps
    keep = [m for m in dumps if not is_binding_plan_item(m["goal"], order=order)]
    ids = {m["id"] for m in keep}
    for milestone in keep:
        milestone["depends_on"] = [d for d in milestone.get("depends_on", []) if d in ids]
        milestone["jobs_draft"] = [j for j in milestone.get("jobs_draft") or []
                                   if not is_binding_plan_item(
                                       f"{j.get('title', '')}. {j.get('goal', '')}", order=order)]
    return keep


def work_task_ids(tasks: list[Any], requested: str) -> set[str]:
    """The ids of the tasks that do the requested work: a task that only produces a checking
    artifact *requested* never asked for (a manifest, a checksum, a snapshot, a report) is left
    out, and at least one task always stays."""
    keep = {t.id for t in tasks if not is_checking_only(f"{t.title}. {t.goal}", requested=requested)}
    return keep or {t.id for t in tasks}
