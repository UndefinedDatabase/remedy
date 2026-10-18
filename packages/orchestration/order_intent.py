"""What an order asks Remedy to do, and what it asks of each file it names (operator order exec-1018).

`order_scope` sorts an order's sentences into deliverables and constraints; the lane then took every
path of every deliverable sentence as a file to change. Three readings were missing:

* the order's INTENT (R-1349): "Only plan how to restructure README.md; do not change anything" took
  the bounded lane and its builder changed README.md, and "Only run the project tests and report"
  planned and ran a change. `order_intent` reads `change`, `plan_only` (the walk then runs as
  `--plan-only`), `verify_only` (one job with no build task: its DoD runs the project's tests, no
  model is called) or `no_work` (a question, never a guess);
* the ROLE of each named file (R-1348): `order_file_roles` reads `required` (the order asks to change
  it), `optional` ("you may also adjust X if needed"), `context` ("see X", "as described in X") and
  `protected` ("do not change X", "X nicht ändern", "leave X unchanged"). Only required files are
  held to change (`task_deliverables.deliverable_files_refusal`), a protected one must NOT change;
* INDEPENDENCE (R-1350): `independent_parts` splits the required files into the order's own parts
  when no part refers to another (no back-reference, no shared identifier, no file of one part named
  in another), so three unrelated edits become three tasks of the one bounded job, while a rename
  and its callers stay one task.

All three are fixed patterns, English and German, and no model call, as `order_scope` is: a
classifier call would spend a provider call to decide whether to spend provider calls. Where a
reading is unsure it falls back to the old one (a file is required, parts are one task), with one
exception (exec-1018b, R-1358): a clause that matches no guard, reference or permission pattern, opens
with no known verb and states no defect or requirement, but carries a NEGATION ("Under no
circumstances modify X") is most likely a guard the patterns miss. Its file is `mentioned`: never held
to change, never a task of its own, and the builder is told to change it only as far as the order
asks. Negations are a closed class and verbs are not, so an unknown verb ("Lass src/price.js
kaufmännisch runden") keeps its file required and no part of the order is dropped. Measured on
wordings no pattern was tuned on, the patterns misread 8 of 12 before this order; what changed is
that a missed guard no longer becomes an instruction to change the file it guards.
"""
from __future__ import annotations

import re
from pathlib import PurePosixPath

from packages.orchestration.order_scope import (
    _ACTION_VERBS,
    _TESTS,
    order_test_request,
    order_unit_head,
    split_order_scope,
)
from packages.orchestration.task_deliverables import explicit_order_paths

ORDER_INTENT_CHANGE = "change"
ORDER_INTENT_PLAN_ONLY = "plan_only"
ORDER_INTENT_VERIFY_ONLY = "verify_only"
ORDER_INTENT_NO_WORK = "no_work"

FILE_ROLE_REQUIRED = "required"
FILE_ROLE_OPTIONAL = "optional"
FILE_ROLE_CONTEXT = "context"
FILE_ROLE_PROTECTED = "protected"
FILE_ROLE_MENTIONED = "mentioned"
#: When one file is named in several roles, the strongest wins: a file the order asks to change in
#: one clause is required even where another clause guards a part of it ("do not change its API").
_ROLE_RANK = {FILE_ROLE_REQUIRED: 4, FILE_ROLE_PROTECTED: 3, FILE_ROLE_MENTIONED: 2, FILE_ROLE_OPTIONAL: 1,
              FILE_ROLE_CONTEXT: 0}

# The order asks for no change at all (never "change nothing ELSE", which is a scope fence).
_NO_CHANGE = re.compile(
    r"\b(?:do\s+not|don't|never|must\s+not)\s+(?:change|modify|edit|touch|implement|write)\s+"
    r"(?:anything|any\s+(?:files?|code))\b"
    r"|\bchange\s+nothing\b|\bwithout\s+changing\s+anything\b|\bread[- ]only\b"
    r"|(?:^|[.!?;:]\s*)no\s+changes\b"
    r"|\bohne\s+(?:etwas|irgendetwas|was)\s+zu\s+(?:ändern|verändern)\b"
    r"|\b(?:ändere|verändere|änderst|veränderst)\s+(?:bitte\s+)?nichts\b"
    r"|\bnichts\s+(?:ändern|verändern|umsetzen|implementieren|anfassen)\b"
    r"|\bkeine\s+(?:datei(?:en)?|änderungen?)\s+(?:ändern|verändern|vornehmen|anfassen)\b"
    r"|\b(?:only|just|nur|lediglich)\s+(?:a\s+|einen\s+)?(?:plan\w*|planung)\b|\bplan\s+only\b",
    re.IGNORECASE)
#: Words beside a no-change that make it a fence on a part of the work, never the order's intent:
#: "change nothing ELSE", and "do not change any CODE" beside a documentation change (R-1358).
_ELSE = re.compile(r"\b(?:else|elsewhere|other|others|besides|sonst|ansonsten|anderes|anderen|weiteres|"
                   r"weiteren|woanders|anderswo|code|quellcode)\b", re.IGNORECASE)
_PLAN_WORDS = re.compile(
    r"\bplan\w*\b|\bhow\s+(?:would|should|could|to)\b|\bapproach\b|\bpropos\w*\b|\bdesign\b"
    r"|\bvorschlag\w*\b|\bschlag\w*\b(?=.{0,80}\bvor\b)|\bwie\s+(?:würde|sollte|könnte|man)\b"
    r"|\bkonzept\w*\b|\bentwurf\w*\b",
    re.IGNORECASE)
_ONLY_RUN = re.compile(r"\b(?:only|just|nur|lediglich)\s+(?:run|execute|führe|test|prüf\w*|verify|check)\w*",
                       re.IGNORECASE)

# Roles of a named file, read inside the clause that names it.
_CLAUSE_SPLIT = re.compile(r",|;|\bbut\b|\baber\b|\bsondern\b|\bwhereas\b|\bwhile\b|\bwährend\b"
                           r"|(?=\bwithout\b|\bohne\b)"     # kept: the guard reads it
                           r"|\b(?:and|und)\b(?=\s+(?:leave|keep|do\s+not|don't|never|lass\w*|nicht)\b)",
                           re.IGNORECASE)
_PROTECT = re.compile(
    r"\b(?:do\s+not|don't|never|must\s+not|nicht|nie|niemals|keinesfalls)\b.{0,40}?"
    r"\b(?:change|modify|edit|touch|alter|rewrite|änder\w*|veränder\w*|bearbeit\w*|anfass\w*|anrühr\w*)"
    r"|\b(?:change|modify|edit|touch|änder\w*|veränder\w*|bearbeit\w*)\b.{0,60}?\b(?:nicht|nie)\b"
    r"|\b(?:leave|keep|lass\w*)\b.{0,60}?\b(?:unchanged|untouched|as\s+it\s+is|unverändert|in\s+ruhe)\b"
    r"|\b(?:stays?|remains?|bleibt|bleiben)\s+(?:unchanged|untouched|as\s+it\s+is|unverändert)\b"
    r"|^\s*(?:without\s+(?:changing|touching|modifying|editing|breaking)|ohne\b.{0,60}?\b(?:\w*ändern|anzufassen))\b"
    r"|\boff[- ]limits\b|\bhands\s+off\b|\bfinger\s+weg\b",
    re.IGNORECASE)
_OPTIONAL = re.compile(
    r"\b(?:may|might|can|could|if\s+(?:needed|necessary|required)|where\s+needed|optionally|"
    r"darfst|kannst|falls\s+nötig|bei\s+bedarf|wenn\s+nötig|gegebenenfalls|ggf|"
    r"fine|allowed|ok(?:ay)?|erlaubt|in\s+ordnung)\b", re.IGNORECASE)
#: A cue right before a path that names it as a reference, not as work.
_CONTEXT_CUE = re.compile(
    r"\b(?:see|siehe|described\s+in|documented\s+in|defined\s+in|specified\s+in|explained\s+in|"
    r"as\s+in|like\s+in|like|according\s+to|following|based\s+on|per|for\s+reference\s*:?|"
    r"wie\s+in|gemäß|laut|nach\s+dem\s+vorbild\s+von|beschrieben\s+in|dokumentiert\s+in|"
    r"definiert\s+in|steht\s+in|vorbild|"
    # a reading verb right before the path (R-1358): "Read docs/X.md first", "Lies zuerst docs/X.md"
    r"(?:read|consult|use|look\s+at|lies|nutze|verwende|schau\s+dir)(?:\s+(?:first|zuerst|erst|bitte|kurz|vorher))?)"
    r"\s*(?:the\s+|der\s+|die\s+|das\s+|dem\s+|den\s+)?"
    r"(?:file\s+|datei\s+)?`?$", re.IGNORECASE)

# Parts of an order that refer to one another.
#: Imperatives that open a clause of work beside `order_scope._ACTION_VERBS`, which also counts an
#: order's actions for its lane and so stays as it is (R-1358): "register it in src/api/app.py".
_WORK_VERBS = _ACTION_VERBS | frozenset({
    "make", "register", "trim", "round", "bump", "wire", "expose", "handle", "validate", "return", "set",
    "adjust", "raise", "lower", "sort", "call", "pass", "export", "import", "mach", "registriere", "runde",
    "setze", "passe", "stelle", "erhöhe", "senke", "sortiere", "exportiere", "importiere", "validiere"})
#: A clause that is work on the files it names although no action verb opens it: a defect it states
#: ("... rechnet falsch") or a behaviour it requires ("... soll ... zurückgeben") (R-1358).
_WORK_STATEMENT = re.compile(
    r"\b(?:wrong|broken|buggy|bug|incorrect|typo|fails?|failing|crash\w*|should|must|needs?\s+to|has\s+to|"
    r"falsch|fehler\w*|kaputt|defekt|tippfehler|stimmt\s+nicht|soll\w*|muss|müssen)\b", re.IGNORECASE)

#: The closed class that tells a guard the patterns miss from work they miss (R-1358).
_NEGATION = re.compile(r"\b(?:no|not|never|nothing|without|nicht|kein\w*|nie|niemals|nichts|ohne|keinesfalls)\b"
                       r"|n't\b", re.IGNORECASE)

_BACK_REFERENCE = re.compile(
    r"\b(?:it|its|them|they|their|this|that|these|those|the\s+same|there|accordingly|"
    r"es|sie|ihn|ihm|ihr|ihre\w*|dazu|damit|davon|dafür|diese\w*|dieselbe\w*|entsprechend\w*)\b",
    re.IGNORECASE)
_IDENTIFIER = re.compile(r"`([^`\n]+)`|\b([A-Za-z_][A-Za-z0-9_]*)\(|\b([a-z]+[A-Z][A-Za-z0-9]*|[a-z0-9]+_[a-z0-9_]+)\b")


def order_intent(order: str) -> str:
    """`change`, `plan_only`, `verify_only` or `no_work`: what the order asks Remedy to do at all."""
    no_change = any(not _ELSE.search(order[max(0, m.start() - 20):m.end() + 20])
                    for m in _NO_CHANGE.finditer(order))
    scope = split_order_scope(order)
    if not no_change and not (_ONLY_RUN.search(order) and scope.actions == 0):
        return ORDER_INTENT_CHANGE
    if _PLAN_WORDS.search(order):
        return ORDER_INTENT_PLAN_ONLY
    if order_test_request(order) or _TESTS.search(order):
        return ORDER_INTENT_VERIFY_ONLY
    return ORDER_INTENT_NO_WORK


def order_file_roles(order: str) -> dict[str, str]:
    """Each path the order names, in order of appearance, with its role (see the module text)."""
    roles: dict[str, str] = {}
    for unit in _units(order):
        for clause in _CLAUSE_SPLIT.split(order_unit_head(unit)):
            for path in explicit_order_paths(clause):
                role = _clause_role(clause, path)
                if path not in roles or _ROLE_RANK[role] > _ROLE_RANK[roles[path]]:
                    roles[path] = role
    return roles


def _clause_role(clause: str, path: str) -> str:
    before = clause[:clause.find(path)] if path in clause else clause
    if _CONTEXT_CUE.search(before.rstrip()):
        return FILE_ROLE_CONTEXT
    words = clause.strip().lower().split()
    leads_with_work = bool(words) and words[0].strip("„\"'(") in _WORK_VERBS
    # "do not change anything" is the order's intent (`order_intent`), never a guard on one file.
    if _PROTECT.search(clause) and not leads_with_work and not _NO_CHANGE.search(clause):
        return FILE_ROLE_PROTECTED
    if _OPTIONAL.search(clause):
        return FILE_ROLE_OPTIONAL
    if leads_with_work or _WORK_STATEMENT.search(clause) or not _NEGATION.search(clause):
        return FILE_ROLE_REQUIRED
    return FILE_ROLE_MENTIONED


def _units(order: str) -> list[str]:
    scope = split_order_scope(order)
    return [*scope.deliverables, *scope.constraints]


def independent_parts(order: str, required: list[str]) -> list[list[str]]:
    """The required files grouped by the order's own parts when the parts are independent, else one group.

    A part is a sentence or list item that asks for work on its own files. Parts are coupled, and
    so stay one task, when a later one refers back ("it", "dazu", "the same"), when two share an
    identifier (`normalizeName`, `add(`, `user_id`), or when one names a file of another or its
    stem. Unsure is coupled.
    """
    if len(required) < 2:
        return [list(required)]
    groups: list[tuple[str, list[str]]] = []
    placed: set[str] = set()
    for unit in split_order_scope(order).deliverables:
        mine = [path for path in required if path not in placed and _names(unit, path)]
        if mine:
            groups.append((unit, mine))
            placed.update(mine)
    if len(groups) < 2 or placed != set(required):
        return [list(required)]
    for number, (unit, files) in enumerate(groups):
        head = order_unit_head(unit)
        if number and _BACK_REFERENCE.search(head):
            return [list(required)]
        others = [g for g in groups if g[1] is not files]
        if any(_names(other_unit, path) or PurePosixPath(path).stem.lower() in order_unit_head(other_unit).lower()
               for path in files for other_unit, _other in others):
            return [list(required)]
    identifiers = [_identifiers(order_unit_head(unit)) for unit, _files in groups]
    if any(identifiers[i] & identifiers[j] for i in range(len(groups)) for j in range(i + 1, len(groups))):
        return [list(required)]
    return [files for _unit, files in groups]


def _names(text: str, path: str) -> bool:
    return path in explicit_order_paths(text) or PurePosixPath(path).as_posix() in text


def _identifiers(text: str) -> set[str]:
    found: set[str] = set()
    for match in _IDENTIFIER.finditer(text):
        token = next(group for group in match.groups() if group)
        if not _looks_like_path(token):
            found.add(token.strip().lower())
    return found


def _looks_like_path(token: str) -> bool:
    return "/" in token or bool(re.search(r"\.[A-Za-z0-9]{1,8}$", token))
