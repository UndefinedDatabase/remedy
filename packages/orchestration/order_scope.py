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

_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
_STRUCTURE_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)]|#{1,6})\s", re.MULTILINE)
_PATH_RE = re.compile(r"[\w./-]+\.[A-Za-z0-9]{1,8}\b")

# Scope fences: the files the work may touch.
_SCOPE = re.compile(
    r"\b(?:only|exclusively|ausschlie(?:ß|ss)lich|nur)\b.{0,60}\b(?:change|modify|edit|touch|"
    r"änder\w*|veränder\w*|bearbeit\w*)"
    r"|\b(?:change|modify|edit|touch|änder\w*|veränder\w*)\b.{0,30}\b(?:only|ausschlie(?:ß|ss)lich|nur)\b"
    r"|\b(?:no|keine)\s+(?:other|anderen?|weiteren?|zusätzlichen?|unrelated|new|neuen?)\s+(?:files?|dateien?)\b"
    r"|\bdo(?:\s+not|n't)\s+(?:create|add|change|modify|touch)\s+(?:any\s+)?(?:other|unrelated|new|extra)\s+files?\b",
    re.IGNORECASE)
# Running or passing the project's own tests.
_TESTS = re.compile(
    r"\b(?:run|execute|führ\w*|start\w*)\b.{0,40}\b(?:tests?|test\s?suite|npm\s+test|pytest|"
    r"testsuite|unit\s?tests?)\b"
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
    r"\b(?:manifest\w*|checksums?|hash(?:es)?|snapshot\w*|baseline\w*|report\w*|bericht\w*|"
    r"prüfsumme\w*|audit\w*)\b", re.IGNORECASE)

_RUNS_SOMETHING = re.compile(r"(?:please\s+|bitte\s+)?(?:run|execute|führ\w*|start\w*)\b", re.IGNORECASE)
_ACTION_SPLIT_RE = re.compile(r",|;|\band\b|\bund\b|\bthen\b|\bdann\b|\bsowie\b", re.IGNORECASE)
_ACTION_VERBS = frozenset({
    "add", "create", "write", "implement", "fix", "refactor", "remove", "delete", "rename",
    "update", "change", "migrate", "move", "replace", "extend", "build", "document", "introduce",
    "convert", "split", "merge", "ergänze", "füge", "erstelle", "schreibe", "implementiere",
    "behebe", "entferne", "lösche", "benenne", "aktualisiere", "ändere", "migriere", "verschiebe",
    "ersetze", "erweitere", "baue", "dokumentiere", "führe", "teile",
})
#: An order whose deliverables hold more actions than this asks for several things.
MAX_SIMPLE_ACTIONS = 2
#: An order whose deliverables run longer than this many sentences has several parts.
MAX_SIMPLE_SENTENCES = 2


@dataclass(frozen=True)
class OrderScope:
    """An order sorted: what to deliver, what binds it, and whether it declares several parts."""

    deliverables: tuple[str, ...]
    constraints: tuple[str, ...]
    structured: bool

    @property
    def actions(self) -> int:
        """How many separate actions the deliverables ask for, by their leading verbs."""
        count = 0
        for sentence in self.deliverables:
            for clause in _ACTION_SPLIT_RE.split(sentence):
                words = clause.strip().lower().split()
                count += bool(words) and words[0].strip("„\"'(") in _ACTION_VERBS
        return count

    @property
    def simple(self) -> bool:
        """One plain part: no list or heading, few sentences, few actions."""
        return (not self.structured and 0 < len(self.deliverables) <= MAX_SIMPLE_SENTENCES
                and self.actions <= MAX_SIMPLE_ACTIONS)


def _binds(clause: str) -> bool:
    return bool(_SCOPE.search(clause) or _TESTS.search(clause) or _APPROVAL.search(clause))


def _has_work_clause(sentence: str) -> bool:
    """A clause that starts with an action verb and is no fence, test run or approval of its own:
    "Fix parse.py, add tests and change no other files" carries work beside its fence."""
    for clause in _ACTION_SPLIT_RE.split(sentence):
        words = clause.strip().lower().split()
        if words and words[0].strip("„\"'(") in _ACTION_VERBS and not _binds(clause):
            return True
    return False


def is_constraint_sentence(sentence: str) -> bool:
    """True when *sentence* only binds the work: a scope fence, a test run, approval, review or a report."""
    text = sentence.strip()
    if _has_work_clause(text):
        return False
    if _SCOPE.search(text):
        return True
    if _PATH_RE.search(text) and not _RUNS_SOMETHING.match(text):
        return False        # it names a file to work on ("run pytest tests/x.py" stays a test run)
    return bool(_TESTS.search(text) or _APPROVAL.search(text) or _REVIEW.search(text))


def split_order_scope(order: str) -> OrderScope:
    """Sort *order*'s sentences into deliverables and constraints (header constraints included)."""
    body, _, header_block = order.partition(HEADER_CONSTRAINTS_MARKER)
    header = tuple(line[2:].strip() for line in header_block.splitlines() if line.startswith("- "))
    text = body.strip()
    structured = bool(_STRUCTURE_RE.search(text)) or ";" in text or "\n\n" in text
    sentences = [s.strip() for s in _SENTENCE_RE.split(" ".join(text.split())) if s.strip()]
    constraints = [s for s in sentences if is_constraint_sentence(s)]
    deliverables = [s for s in sentences if s not in constraints]
    if not deliverables:
        deliverables, constraints = sentences, []       # the constraints ARE the order
    return OrderScope(tuple(deliverables), tuple(constraints) + header, structured)


def is_checking_only(text: str, *, requested: str) -> bool:
    """True when a plan item (*text*) only produces a checking artifact *requested* did not ask for.

    A milestone or task of that kind (a checksum manifest, a comparison copy, a modification
    report) adds a file and a round and proves nothing Remedy's own guards do not already prove.
    """
    return bool(_CHECKING_ARTIFACT.search(text)) and not _CHECKING_REQUEST.search(requested)


#: A plan item about the project's tests having run or passing, also in the planner's passive voice.
_TESTS_DONE = re.compile(
    r"\b(?:npm\s+test|pytest|test\s?suite|testsuite|tests?)\b.{0,40}\b(?:run|ran|executed|"
    r"pass\w*|green|captured|ausgeführt|bestanden|grün)\b", re.IGNORECASE)


def is_binding_plan_item(text: str, *, order: str) -> bool:
    """True when a planner's milestone or outline (*text*) only binds or checks the work.

    An item that names a file is work on that file, whatever fence it also states. Otherwise it
    binds when it is about the tests running or passing, approval, review or a report, or when it
    only makes a checking artifact *order* never asked for.
    """
    if _PATH_RE.search(text) and not _RUNS_SOMETHING.match(text.strip()):
        return False
    return bool(_TESTS.search(text) or _TESTS_DONE.search(text) or _APPROVAL.search(text)
                or _REVIEW.search(text.strip())) or is_checking_only(text, requested=order)


def _asks_for_work(order: str) -> bool:
    """True when *order* has a deliverable beyond its constraints (a test-only order has none)."""
    return any(not is_constraint_sentence(s) for s in split_order_scope(order).deliverables)


def work_milestones(drafts: list[Any], order: str) -> list[dict[str, Any]]:
    """The planner's milestones (as dicts) without those that are only a constraint or a check.

    "Run npm test" or "the codebase is unchanged after the tests" is no milestone when the order
    asks for real work: the DoD runs the tests and the scope guard holds the files. Nothing is
    dropped for an order that is itself only a test run or a report, and at least one milestone,
    and one outline per milestone, always stays.
    """
    dumps = [draft.model_dump() for draft in drafts]
    if not _asks_for_work(order):
        return dumps
    keep = [m for m in dumps if not is_binding_plan_item(m["goal"], order=order)] or dumps
    ids = {m["id"] for m in keep}
    for milestone in keep:
        milestone["depends_on"] = [d for d in milestone.get("depends_on", []) if d in ids]
        outlines = milestone.get("jobs_draft") or []
        milestone["jobs_draft"] = [j for j in outlines if not is_binding_plan_item(
            f"{j.get('title', '')}. {j.get('goal', '')}", order=order)] or outlines
    return keep


def work_task_ids(tasks: list[Any], requested: str) -> set[str]:
    """The ids of the tasks that do the requested work: a task that only produces a checking
    artifact *requested* never asked for (a manifest, a checksum, a snapshot, a report) is left
    out, and at least one task always stays."""
    keep = {t.id for t in tasks if not is_checking_only(f"{t.title}. {t.goal}", requested=requested)}
    return keep or {t.id for t in tasks}
