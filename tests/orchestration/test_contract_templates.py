"""F269 T003 — the contract templates: format, compile, proposal (DECISION F269 D1).

What D1 (1) to (3) require proof of:

  * all four shipped templates load, and each one's fixture order proposes
    that template; a bare order and a tied order propose nothing;
  * the compiled website template is origin ``template``, whole-mission,
    ``C001`` upward in file order, with the blocking flags of the file;
  * a ``check:`` line becomes that criterion's check, ``ctr-<id>``;
  * every D1 violation is refused naming the file and the line;
  * an unknown template name is refused naming the four;
  * the template is written onto a mission with no contract, and a mission
    that already has one is refused.

Nothing here calls a provider: templates compile through F061's
deterministic path.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.contract_templates import (
    CONTRACT_TEMPLATES_DIR,
    ContractTemplateError,
    compile_contract_template,
    list_contract_templates,
    load_contract_template,
    parse_contract_template,
    propose_contract_template,
    write_template_contract,
)
from packages.orchestration.dod_schema import DoDCheck
from packages.orchestration.mission_contract import (
    ContractCriterion,
    MissionContract,
    read_mission_contract,
    write_mission_contract,
)
from packages.orchestration.mission_state import create_mission, load_mission

SHIPPED = ("api-service", "cli-tool", "python-library", "website")
PROJECT = "p-f269-templates"

WEBSITE_CRITERIA = [
    ("Every page the order names is built, and a test loads each one and checks its "
     "main content.", True),
    ("Every link between the site's own pages resolves, and a test proves it.", True),
    ("The test suite passes.", True),
    ("Every page has a title and one top-level heading, and a test proves it.", False),
    ("No file is added that nothing references.", True),
    ("Code that is replaced is deleted in the same task, never left beside its "
     "replacement.", True),
    ("No stub, placeholder or TODO body survives the job.", True),
]

#: DECISION F269 D5 (5): the three hygiene criteria every template ends with,
#: each measured by one rule of ``contract_hygiene``.
HYGIENE_CRITERIA = (
    ("No file is added that nothing references.", "unreferenced"),
    ("Code that is replaced is deleted in the same task, never left beside its "
     "replacement.", "replaced"),
    ("No stub, placeholder or TODO body survives the job.", "stubs"),
)

CHECK = {"kind": "custom_cmd", "spec": {"argv": ["make", "lint"]},
         "description": "the lint target passes"}


def _template(name: str, criteria: str, *, phrases: str = "- demo\n",
              fixture: str = "Build the demo.\n") -> str:
    return (f"# Contract template — {name}\n\nFree prose.\n\n"
            f"## Proposed when the order mentions\n\n{phrases}\n"
            f"## Criteria\n\n{criteria}\n"
            f"## Fixture order\n\n{fixture}")


def _write(folder: Path, name: str, text: str) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{name}.md"
    path.write_text(text, encoding="utf-8")
    return path


# ── the shipped templates ───────────────────────────────────────────────────


def test_the_templates_are_read_from_the_source_trees_docs_contracts():
    assert CONTRACT_TEMPLATES_DIR == Path(__file__).resolve().parents[2] / "docs" / "contracts"
    assert list_contract_templates() == SHIPPED


@pytest.mark.parametrize("name", SHIPPED)
def test_a_shipped_template_loads_and_its_fixture_order_proposes_it(name):
    template = load_contract_template(name)

    assert template.name == name
    assert template.phrases and template.criteria and template.fixture_order
    assert propose_contract_template(template.fixture_order) == name


def test_a_bare_order_proposes_nothing():
    assert propose_contract_template("Write a CONTRIBUTING.md") is None


def test_a_tied_order_proposes_nothing():
    # "website" scores 1 for website, "api" scores 1 for api-service.
    order = "Build a website and an api for the bakery."
    assert propose_contract_template(order) is None


def test_a_phrase_counts_only_between_non_word_non_hyphen_characters():
    assert propose_contract_template("Build a rapid prototype") is None
    assert propose_contract_template("Build a web-site-api") is None
    assert propose_contract_template("Build the API.") == "api-service"


def test_the_compiled_website_template_is_the_files_criteria_in_order():
    criteria = compile_contract_template(load_contract_template("website"))

    assert [c.id for c in criteria] == [f"C{n:03d}" for n in range(1, 8)]
    assert [(c.text, c.blocking) for c in criteria] == WEBSITE_CRITERIA
    assert {c.origin for c in criteria} == {"template"}
    assert {c.milestones for c in criteria} == {()}
    for c in criteria:
        assert c.check["id"] == f"ctr-{c.id}"
        assert c.check["acceptance_refs"] == [f"{c.id}:0"]
        assert c.check["blocking"] is c.blocking
        DoDCheck.model_validate(c.check)


@pytest.mark.parametrize("name", SHIPPED)
def test_every_shipped_template_compiles_its_hygiene_criteria_to_their_check_lines(name):
    criteria = compile_contract_template(load_contract_template(name))
    hygiene = criteria[-len(HYGIENE_CRITERIA):]

    assert [c.text for c in hygiene] == [text for text, _ in HYGIENE_CRITERIA]
    for criterion, (_, rule) in zip(hygiene, HYGIENE_CRITERIA):
        assert criterion.blocking is True
        assert criterion.check == {
            "id": f"ctr-{criterion.id}", "kind": "custom_cmd",
            "spec": {"argv": ["python3", "-m", "packages.orchestration.contract_hygiene",
                              rule]},
            "blocking": True, "acceptance_refs": [f"{criterion.id}:0"],
            "description": f"contract hygiene: {rule}", "source": "plan_acceptance"}


def test_an_unknown_template_name_is_refused_naming_the_four():
    with pytest.raises(ContractTemplateError) as exc:
        load_contract_template("nosuch")

    assert "'nosuch'" in str(exc.value)
    for name in SHIPPED:
        assert name in str(exc.value)


# ── a fixture template under tmp_path ──────────────────────────────────────


def test_a_check_line_compiles_to_that_check(tmp_path):
    folder = tmp_path / "contracts"
    _write(folder, "demo", _template("demo", (
        "- blocking: The lint target passes.\n"
        f"  check: {json.dumps(CHECK)}\n"
        "- advisory: The test suite passes.\n")))

    first, second = compile_contract_template(load_contract_template("demo", folder))

    assert first.check == {
        "id": "ctr-C001", "kind": "custom_cmd", "spec": {"argv": ["make", "lint"]},
        "blocking": True, "acceptance_refs": ["C001:0"],
        "description": "the lint target passes", "source": "plan_acceptance"}
    assert first.blocking is True
    # The criterion without a check line is compiled by F061's compiler.
    assert second.check["id"] == "ctr-C002" and second.check["kind"] == "pytest"
    assert second.check["blocking"] is False


VIOLATIONS = [
    pytest.param(
        "# Contract template — other\n\n## Criteria\n\n- blocking: A.\n", 1,
        id="wrong-title"),
    pytest.param(
        _template("demo", "- blocking: A.\n").replace(
            "## Fixture order", "## Notes\n\nx\n\n## Fixture order"),
        13, id="unknown-section"),
    pytest.param(_template("demo", "- blocking: A.\n- must: B.\n"), 12,
                 id="malformed-bullet"),
    pytest.param(_template("demo", '- blocking: A.\n  check: {"kind": "pytest"}\n'), 12,
                 id="invalid-check"),
    pytest.param(_template("demo", ""), 14, id="no-criteria"),
]


@pytest.mark.parametrize(("text", "line"), VIOLATIONS)
def test_a_d1_violation_is_refused_naming_its_line(tmp_path, text, line):
    path = _write(tmp_path / "contracts", "demo", text)

    with pytest.raises(ContractTemplateError) as exc:
        parse_contract_template(path)

    assert str(exc.value).startswith(f"{path}:{line}: ")


def test_a_template_with_an_upper_case_phrase_or_two_fixture_paragraphs_is_refused(tmp_path):
    folder = tmp_path / "contracts"
    upper = _write(folder, "demo", _template("demo", "- blocking: A.\n", phrases="- Demo\n"))
    with pytest.raises(ContractTemplateError, match=r":7: "):
        parse_contract_template(upper)

    two = _write(folder, "demo", _template("demo", "- blocking: A.\n",
                                           fixture="First.\n\nSecond.\n"))
    with pytest.raises(ContractTemplateError, match=r":17: "):
        parse_contract_template(two)


# ── writing a template onto a mission ──────────────────────────────────────


def test_the_template_is_written_onto_a_mission_without_a_contract(tmp_path):
    mission = create_mission(PROJECT, "Build a small website", root=tmp_path)

    written = write_template_contract(PROJECT, mission.id, "website", root=tmp_path)

    stored = read_mission_contract(load_mission(PROJECT, mission.id, tmp_path))
    assert stored == written
    assert stored.template == "website"
    assert [(c.text, c.blocking) for c in stored.criteria] == WEBSITE_CRITERIA


def test_a_mission_that_already_has_a_contract_is_refused(tmp_path):
    mission = create_mission(PROJECT, "Build a small website", root=tmp_path)
    existing = MissionContract(criteria=(
        ContractCriterion(id="C001", text="Kept.", origin="planner"),))
    write_mission_contract(PROJECT, mission.id, existing, tmp_path)

    with pytest.raises(ContractTemplateError, match="already has a contract"):
        write_template_contract(PROJECT, mission.id, "website", root=tmp_path)

    assert read_mission_contract(load_mission(PROJECT, mission.id, tmp_path)) == existing
