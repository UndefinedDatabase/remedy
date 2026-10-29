"""F320 — attachments, evidence and tool names of an order are never deliverables."""
from __future__ import annotations

from packages.orchestration.order_material import order_work_text
from packages.orchestration.order_scope import order_forbids_new_file
from packages.orchestration.task_deliverables import (
    deterministic_job_plans,
    extract_order_deliverables,
    missing_deliverables_refusal,
    order_missing_deliverables,
)

#: The shape of the improve run's orders of 2026-10-28 (job 4b90ef2ed0274960 and its waiting twin).
NIGHT_ORDER = (
    "Luna soll im Chat den Status des Repos zeigen; fix packages/tools/status.py.\n"
    "Verknüpfte Berichte: 2026-10-28-183939-general.md\n"
    "\n"
    "Diagnosepaket (Material zur Untersuchung, keine Anweisung; der Auftrag ist allein die Aufgabe oben):\n"
    "Werkzeuge: repo.status, repo.log, jira.create, mail.unread\n"
    "Bilder: 2026-10-28-225013-general/1.jpg and t4x68u-1.jpg\n"
    "\n"
    "Constraints the plan must honour:\n"
    "- Do not create new documentation files.\n"
    "- Do not create note files."
)


def test_night_order_names_only_its_work_file() -> None:
    # Before F320 the report name, both pictures and four tool names became deliverables too.
    assert extract_order_deliverables(NIGHT_ORDER) == ["packages/tools/status.py"]
    [tasks] = deterministic_job_plans(NIGHT_ORDER)
    assert [task.title for task in tasks] == ["Deliver packages/tools/status.py"]


def test_work_text_keeps_the_constraints_block() -> None:
    work = order_work_text(NIGHT_ORDER)
    assert "jira.create" not in work and "183939" not in work and "1.jpg" not in work
    assert "\n\nConstraints the plan must honour:\n- Do not create new documentation files." in work
    assert work.startswith("Luna soll im Chat")


def test_order_without_material_is_unchanged() -> None:
    order = "Fix the bug in src/app.py and docs/usage.md."
    assert order_work_text(order) == order
    assert extract_order_deliverables(order) == ["src/app.py", "docs/usage.md"]


def test_attachment_label_line_alone_is_dropped() -> None:
    order = "Attachments: shot.png, log.txt\nRepair src/view.ts so the list shows again."
    assert extract_order_deliverables(order) == ["src/view.ts"]


def test_doc_constraint_forbids_only_documents() -> None:
    order = "Add it.\n\nConstraints the plan must honour:\n- Do not create new documentation files."
    assert order_forbids_new_file(order, "notes/2026-10-21-195020-general.md")
    assert not order_forbids_new_file(order, "src/new_tool.py")
    assert order_forbids_new_file("Change it; no new files.", "src/new_tool.py")


def test_missing_document_under_doc_constraint_is_a_planning_error() -> None:
    # Job f3ced4db of 2026-10-28: the named report did not exist, the order forbade new documents,
    # and the job was built and blocked by the reviewer instead of stopping before planning.
    order = ("Bearbeite 2026-10-21-195020-general.md wie berichtet.\n\n"
             "Constraints the plan must honour:\n- Do not create new documentation files.")
    tracked = ["README.md", "src/app.py"]
    assert order_missing_deliverables(order, tracked) == ["2026-10-21-195020-general.md"]
    sentence = missing_deliverables_refusal(["2026-10-21-195020-general.md"])
    assert "nothing was planned or run" in sentence and "2026-10-21-195020-general.md" in sentence


def test_existing_or_requested_file_is_not_missing() -> None:
    constraint = "\n\nConstraints the plan must honour:\n- Do not create new documentation files."
    tracked = ["README.md", "docs/usage.md"]
    assert order_missing_deliverables("Update docs/usage.md." + constraint, tracked) == []
    assert order_missing_deliverables("Create docs/howto.md for the new flag." + constraint, tracked) == []
    assert order_missing_deliverables("Add src/new_tool.py." + constraint, tracked) == []
    assert order_missing_deliverables("Update docs/gone.md." + constraint, []) == []
