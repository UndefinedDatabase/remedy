"""F269 T003 — the contract templates: their format, their compile and their proposal.

DECISION F269 D1.  A contract template is a human-readable page
``docs/contracts/<name>.md``: the floor of a mission's contract, never its
ceiling (DECISION amend0911-feedback D5).  Its first line is exactly
``# Contract template — <name>``, with ``<name>`` the file stem, and the
loader reads three ``## `` sections by their exact headings:

* ``## Proposed when the order mentions`` — one bullet per lowercase phrase;
* ``## Criteria`` — one bullet per criterion, ``- blocking: <text>`` or
  ``- advisory: <text>``, optionally followed by ONE line indented two
  spaces, ``check: <JSON object>``, which must validate as an F061
  ``DraftCheck`` apart from its id and is then that criterion's check;
* ``## Fixture order`` — one paragraph, the order the template's tests plan.

Prose before the first section is free.  Any other non-blank line under those
sections is refused with the file and the line named — a template is never
half-loaded, because a criterion silently dropped from the floor is a
criterion no mission is ever held to.

A template compiles to criteria with origin ``template``, whole-mission
scope and ids ``C001`` upward in file order; each check comes from its
``check:`` line or from ``mission_contract.compile_contract_criteria`` —
F061's compiler, called, never re-implemented (DECISION F269 D4 (1)).

The proposal is deterministic: each template scores the number of its phrases
that occur in the order, case-insensitive and bounded on both sides by a
character that is neither a word character nor a hyphen; the single top
scorer is proposed, and a zero top score or a tie proposes nothing.

The templates are read from the source tree, ``docs/contracts/`` beside the
``packages`` directory this module lives in (D1 (5)): the wheel does not ship
``docs/``, and distribution is F215's.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from packages.orchestration.mission_contract import (
    CONTRACT_CHECK_ID_PREFIX,
    ContractCriterion,
    MissionContract,
    compile_contract_criteria,
    read_mission_contract,
    write_mission_contract,
)

#: Where the shipped templates live: the source tree's ``docs/contracts/``.
CONTRACT_TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "docs" / "contracts"

#: The first line of a template is this prefix plus the template's file stem.
TEMPLATE_TITLE_PREFIX = "# Contract template — "

SECTION_PHRASES = "## Proposed when the order mentions"
SECTION_CRITERIA = "## Criteria"
SECTION_FIXTURE = "## Fixture order"
TEMPLATE_SECTIONS = (SECTION_PHRASES, SECTION_CRITERIA, SECTION_FIXTURE)

#: The source a ``check:`` line's check is stored with: it covers the
#: criterion's one acceptance line, as F061's own acceptance checks do.
TEMPLATE_CHECK_SOURCE = "plan_acceptance"

_CRITERION_RE = re.compile(r"^- (blocking|advisory): (\S.*)$")
_CHECK_LINE_PREFIX = "  check: "


class ContractTemplateError(ValueError):
    """A template breaks DECISION F269 D1, or cannot be used where it was asked for.

    The message names the file and, when one line is at fault, that line.
    """


@dataclass(frozen=True)
class TemplateCriterionLine:
    """One criterion bullet of a template, with its optional ``check:`` object."""

    text: str
    blocking: bool
    line: int
    check: dict[str, Any] | None = None


@dataclass(frozen=True)
class ContractTemplate:
    """A loaded, validated contract template."""

    name: str
    path: Path
    phrases: tuple[str, ...]
    criteria: tuple[TemplateCriterionLine, ...]
    fixture_order: str


def _templates_dir(directory: Path | None) -> Path:
    return CONTRACT_TEMPLATES_DIR if directory is None else Path(directory)


def list_contract_templates(directory: Path | None = None) -> tuple[str, ...]:
    """The template names — the stems of ``docs/contracts/*.md`` — sorted."""
    folder = _templates_dir(directory)
    if not folder.is_dir():
        return ()
    return tuple(sorted(p.stem for p in folder.glob("*.md") if p.is_file()))


def _template_check_body(obj: Any, criterion_id: str, blocking: bool) -> dict[str, Any]:
    """A ``check:`` object as the criterion's stored check (D1 (2)).

    Its id, refs and blocking are the criterion's: ``ctr-<id>``,
    [``<id>:0``] and the criterion's own ``blocking``.  Raises on anything
    that does not validate as an F061 ``DraftCheck``.
    """
    from packages.orchestration.dod_schema import DoDCheck, DraftCheck

    if not isinstance(obj, dict):
        raise ValueError(f"the check is not a JSON object: {obj!r}")
    draft = DraftCheck.model_validate({
        **obj, "id": f"{CONTRACT_CHECK_ID_PREFIX}{criterion_id}",
        "acceptance_refs": [f"{criterion_id}:0"], "blocking": blocking})
    return DoDCheck(**draft.model_dump(), source=TEMPLATE_CHECK_SOURCE).model_dump(
        mode="json")


def _criterion_id(number: int) -> str:
    return f"C{number:03d}"


def parse_contract_template(path: Path) -> ContractTemplate:
    """Load and validate the template at ``path``; RAISE on every D1 violation."""
    path = Path(path)
    name = path.stem
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ContractTemplateError(f"{path}: cannot be read: {exc}") from exc

    def refuse(number: int, why: str) -> ContractTemplateError:
        return ContractTemplateError(f"{path}:{number}: {why}")

    title = f"{TEMPLATE_TITLE_PREFIX}{name}"
    if not lines or lines[0] != title:
        raise refuse(1, f"the first line must be exactly {title!r}")

    section: str | None = None
    seen: set[str] = set()
    phrases: list[str] = []
    criteria: list[TemplateCriterionLine] = []
    fixture: list[str] = []
    fixture_closed = False
    check_allowed = False
    for number, line in enumerate(lines[1:], start=2):
        if line.startswith("## "):
            if line not in TEMPLATE_SECTIONS:
                raise refuse(number, f"unknown section {line!r}; the sections are "
                             f"{', '.join(repr(s) for s in TEMPLATE_SECTIONS)}")
            if line in seen:
                raise refuse(number, f"section {line!r} appears twice")
            seen.add(line)
            section, check_allowed = line, False
            continue
        if section is None:
            continue  # prose before the first section is free
        if not line.strip():
            if section == SECTION_FIXTURE and fixture:
                fixture_closed = True
            continue
        if section == SECTION_PHRASES:
            phrase = line[2:] if line.startswith("- ") else ""
            if not phrase or phrase != phrase.strip() or phrase != phrase.lower():
                raise refuse(number, "a phrase is one bullet '- <lowercase phrase>'")
            phrases.append(phrase)
        elif section == SECTION_CRITERIA:
            if line.startswith(_CHECK_LINE_PREFIX):
                if not check_allowed:
                    raise refuse(number, "a check: line must follow a criterion bullet")
                previous = criteria[-1]
                try:
                    obj = json.loads(line[len(_CHECK_LINE_PREFIX):])
                    body = _template_check_body(
                        obj, _criterion_id(len(criteria)), previous.blocking)
                except ValueError as exc:
                    raise refuse(number, f"the check is not a valid F061 check: "
                                 f"{exc}") from exc
                criteria[-1] = replace(previous, check=body)
                check_allowed = False
                continue
            match = _CRITERION_RE.match(line)
            if match is None or match.group(2) != match.group(2).strip():
                raise refuse(number, "a criterion is one bullet '- blocking: <text>' "
                             "or '- advisory: <text>'")
            criteria.append(TemplateCriterionLine(
                text=match.group(2), blocking=match.group(1) == "blocking", line=number))
            check_allowed = True
        else:
            if fixture_closed:
                raise refuse(number, "the fixture order is one paragraph")
            fixture.append(line.strip())

    for heading in TEMPLATE_SECTIONS:
        if heading not in seen:
            raise refuse(len(lines), f"the template has no {heading!r} section")
    if not criteria:
        raise refuse(len(lines), "the template has no criteria")
    if not fixture:
        raise refuse(len(lines), "the template has no fixture order")
    return ContractTemplate(name=name, path=path, phrases=tuple(phrases),
                            criteria=tuple(criteria), fixture_order=" ".join(fixture))


def load_contract_template(name: str, directory: Path | None = None) -> ContractTemplate:
    """The template called ``name``; an unknown name is refused naming the templates."""
    names = list_contract_templates(directory)
    if name not in names:
        raise ContractTemplateError(
            f"no contract template is called {name!r}; the templates are "
            f"{', '.join(names) or '(none)'}")
    return parse_contract_template(_templates_dir(directory) / f"{name}.md")


def compile_contract_template(template: ContractTemplate) -> tuple[ContractCriterion, ...]:
    """The template's criteria as contract criteria, each carrying its check (D1 (2))."""
    criteria = [ContractCriterion(id=_criterion_id(number), text=line.text,
                                  origin="template", blocking=line.blocking,
                                  check=line.check)
                for number, line in enumerate(template.criteria, start=1)]
    compiled = {c.id: c for c in compile_contract_criteria(
        [c for c in criteria if c.check is None])}
    return tuple(compiled.get(c.id, c) for c in criteria)


def _phrase_occurs(phrase: str, order: str) -> bool:
    pattern = r"(?<![\w-])" + re.escape(phrase) + r"(?![\w-])"
    return re.search(pattern, order, re.IGNORECASE) is not None


def propose_contract_template(order: str, directory: Path | None = None) -> str | None:
    """The template the order proposes (D1 (3)), or None on a zero top score or a tie."""
    scores = {name: sum(1 for phrase in load_contract_template(name, directory).phrases
                        if _phrase_occurs(phrase, order))
              for name in list_contract_templates(directory)}
    top = max(scores.values(), default=0)
    winners = [name for name, score in scores.items() if score == top]
    if top == 0 or len(winners) != 1:
        return None
    return winners[0]


def write_template_contract(project_id: str, mission_id: str, name: str,
                            root: Path | None = None,
                            directory: Path | None = None) -> MissionContract:
    """Write the template's criteria as the contract of a mission that has none yet.

    A mission that already carries a contract is refused: the template is the
    floor a new contract starts from, never a rewrite of one.
    """
    from packages.orchestration.mission_state import load_mission

    template = load_contract_template(name, directory)
    if read_mission_contract(load_mission(project_id, mission_id, root)) is not None:
        raise ContractTemplateError(
            f"mission {mission_id} already has a contract; template {name!r} "
            f"was not written")
    return write_mission_contract(
        project_id, mission_id,
        MissionContract(criteria=compile_contract_template(template), template=name),
        root)
