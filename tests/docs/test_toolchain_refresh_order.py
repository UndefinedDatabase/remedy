"""`docs/orders/toolchain-refresh.md` is a job file with the sections T2_F279 T004 orders.

The self-use generator queues the file VERBATIM as a job (DECISION F279 D7), so its shape is
the job-file shape: a `# Job:` title and `## Task N` sections, each closed by an
`Acceptance:` list. The headings are pinned here, and so are the three promises T004 makes
about the order: release notes before migration, one whole-suite run, and no merge.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ORDER = REPO_ROOT / "docs" / "orders" / "toolchain-refresh.md"
HEADINGS = [
    "# Job: Refresh the pinned toolchain",
    "## Task 1 — Find the pinned tools that have a newer release",
    "## Task 2 — Read the release notes of every tool that moves",
    "## Task 3 — Raise the pins and regenerate the constraints file",
    "## Task 4 — Repair what the new versions break, and run the whole suite once",
    "## Task 5 — Open a pull request, only when the suite is green",
]


def _text() -> str:
    return ORDER.read_text(encoding="utf-8")


def test_the_order_carries_exactly_the_pinned_headings_in_order():
    assert [line for line in _text().splitlines() if line.startswith("#")] == HEADINGS


def test_every_task_closes_with_an_acceptance_list():
    sections = re.split(r"^## Task \d+ ", _text(), flags=re.M)[1:]
    assert len(sections) == len(HEADINGS) - 1
    for section in sections:
        acceptance = section.split("\nAcceptance:\n", 1)
        assert len(acceptance) == 2 and acceptance[1].lstrip().startswith("- "), section[:60]


def test_the_order_keeps_the_promises_t004_makes():
    text = _text()
    assert "remedy doctor toolchain" in text
    assert "fourteen days" in text
    assert "release notes" in text and "python3 -m pytest -n auto -q" in text
    assert "Do not merge the pull request" in text and "Nothing was merged by this job." in text


def test_the_order_is_indexed_in_the_docs_index():
    index = (REPO_ROOT / "docs" / "README.md").read_text(encoding="utf-8")
    assert index.count("](orders/toolchain-refresh.md)") == 2


def test_the_order_declares_the_budget_it_needs():
    """R-1044: the runner's one-task default cannot fit this five-task order.

    `.agent/selfuse_f279/result_state.txt` records what the absent declaration
    cost: the run stopped at `budget_exhausted:max_cost_usd` after $1.37
    against $1.00, with all five tasks still pending. The declaration is read
    by `packages.orchestration.self_use_runner.parse_order_budget`.
    """
    from packages.orchestration.self_use_runner import parse_order_budget

    declared = parse_order_budget(_text())
    assert declared, "the order must declare its own budget on one `Budget:` line"
    assert declared["max_tasks"] == len(HEADINGS) - 1, (
        "a declared task cap below the order's own task count refuses the run"
    )
    assert declared["max_provider_calls"] >= declared["max_tasks"]
    assert declared["max_cost_usd"] > 1.00
    assert declared["timeout_sec"] >= 600, (
        "Task 4 runs the whole suite, which alone takes over two minutes"
    )


def test_the_budget_line_sits_where_the_planner_cannot_see_it():
    """`parse_job_file` stops reading prose at the first `## Task` heading."""
    from packages.orchestration.pingpong_job import parse_job_file

    plan = parse_job_file(_text(), ".")
    assert len(plan.tasks) == len(HEADINGS) - 1
    assert "Budget:" not in "\n".join(t.body for t in plan.tasks)
