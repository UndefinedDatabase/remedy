"""Adversarial orders, version 1 (operator order exec-1018b P1 4): the wording varies, not the file count.

Each case walks a real `remedy do` over a small Node repository whose own `node --test` checks the
behaviour the order asks for, so a case passes only when the right files changed in the right way
and the project's tests agree: never by its routing label alone. The builder is scripted: it writes
the correct content of every file its task names (the task's title and text, which is all a model
sees too), and a `touches` list makes it also write a file it must not. The reviewer passes every
diff, so whatever holds a wrong change is Remedy's own guard, not a reviewer's luck. English and
German variants of each wording class run side by side.
"""
from __future__ import annotations

import contextlib
import io
import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from tests.orchestration.scale_harness import FakePlannerService, commit_repository, filler_files

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="the cases' projects need node")

ADVERSARIAL_MATRIX_VERSION = 1

REPO = {
    "README.md": "# shop\n\nA small shop.\n",
    "package.json": '{"name": "shop", "type": "module", "scripts": {"test": "node --test"}}\n',
    "docs/FORMAT.md": "# Format\n\nAn empty name reads Unbekannt.\n",
    "config/prod.json": '{"port": 80}\n',
    "src/format.js": "export function normalizeName(input) {\n  return input.trim();\n}\n",
    "src/index.js": 'export { normalizeName } from "./format.js";\n',
    "src/price.js": "export const round = (x) => Math.floor(x);\n",
    "src/cart.js": 'import { round } from "./price.js";\nexport const total = (xs) => round(xs.reduce((a, b) => a + b, 0));\n',
    "src/calc.js": "export function add(a, b) {\n  return a - b;\n}\n",
    "test/baseline.test.js": 'import { test } from "node:test";\ntest("baseline", () => {});\n',
    # The project's own test of cart.js: a rename that breaks its import fails it for real.
    "test/total.test.js": 'import { test } from "node:test";\nimport { strictEqual } from "node:assert";\n'
                          'import { total } from "../src/cart.js";\ntest("total", () => strictEqual(total([1, 2]), 3));\n',
}
T = 'import { test } from "node:test";\nimport { strictEqual } from "node:assert";\n'
#: The correct content of each file a case's builder may write.
CORRECT = {
    "src/format.js": 'export function normalizeName(input) {\n  return input.trim() || "Unbekannt";\n}\n',
    "src/format.js:rename": 'export function normalizePersonName(input) {\n  return input.trim();\n}\n',
    "src/index.js:rename": 'export { normalizePersonName } from "./format.js";\n',
    "test/index.test.js": T + 'import { normalizePersonName } from "../src/index.js";\n'
                          'test("renamed", () => strictEqual(normalizePersonName(" a "), "a"));\n',
    "src/price.js": "export const round = (x) => Math.round(x);\n",
    "src/price.js:rename": "export const roundPrice = (x) => Math.round(x);\n",
    "src/cart.js:rename": 'import { roundPrice } from "./price.js";\n'
                          "export const total = (xs) => roundPrice(xs.reduce((a, b) => a + b, 0));\n",
    "test/cart.test.js": T + 'import { total } from "../src/cart.js";\ntest("half up", () => strictEqual(total([1, 1.5]), 3));\n',
    "test/format.test.js": T + 'import { normalizeName } from "../src/format.js";\n'
                           'test("empty", () => strictEqual(normalizeName("  "), "Unbekannt"));\n',
    "src/calc.js": "export function add(a, b) {\n  return a + b;\n}\n",
    "test/calc.test.js": T + 'import { add } from "../src/calc.js";\ntest("add", () => strictEqual(add(2, 3), 5));\n',
    "README.md": "# shop\n\nA small shop.\n\n## Usage\n\nRun npm test.\n",
    "docs/API.md": "# API\n\n`add(a, b)` returns the sum of a and b.\n",
    "config/prod.json": '{"port": 8080}\n',
}

#: id, order, the files the correct change writes (by CORRECT key), what must hold.
CASES: list[dict[str, Any]] = [
    {"id": "two-files-one-change-en", "writes": ["src/format.js:rename", "src/index.js:rename", "test/index.test.js"],
     "order": "Rename normalizeName to normalizePersonName in src/format.js and src/index.js, and add a test in "
              "test/index.test.js. Run the tests.",
     "expect": {"state": "completed", "tasks": 1, "verification": "passed",
                "staged": ["src/format.js", "src/index.js", "test/index.test.js"]}},
    {"id": "two-files-one-change-de", "writes": ["src/format.js:rename", "src/index.js:rename", "test/index.test.js"],
     "order": "Benenne normalizeName in src/format.js und src/index.js in normalizePersonName um und ergänze einen "
              "Test in test/index.test.js. Führe die Tests aus.",
     "expect": {"state": "completed", "tasks": 1, "verification": "passed",
                "staged": ["src/format.js", "src/index.js", "test/index.test.js"]}},
    {"id": "two-files-one-file-skipped", "writes": ["src/format.js:rename"],
     "order": "Rename normalizeName to normalizePersonName in src/format.js and src/index.js.",
     "expect": {"state": "blocked", "error_has": "named_files_unchanged"}},
    {"id": "three-independent-en", "writes": ["README.md", "src/price.js", "src/format.js"],
     "order": "Add a usage section to README.md. Make src/price.js round half up. Return Unbekannt for an "
              "empty name in src/format.js.",
     "expect": {"state": "completed", "tasks": 3, "staged": ["README.md", "src/format.js", "src/price.js"]}},
    {"id": "three-independent-de", "writes": ["README.md", "src/price.js", "src/format.js"],
     "order": "1. Ergänze in README.md einen Abschnitt zur Nutzung. 2. Lass src/price.js kaufmännisch runden. "
              "3. Gib in src/format.js für einen leeren Namen Unbekannt zurück.",
     "expect": {"state": "completed", "tasks": 3, "staged": ["README.md", "src/format.js", "src/price.js"]}},
    {"id": "context-file-en", "writes": ["src/format.js", "test/format.test.js"],
     "order": "Read docs/FORMAT.md first, then fix the empty-name bug in src/format.js and add a regression "
              "test in test/format.test.js. Run the tests.",
     "expect": {"state": "completed", "verification": "passed", "staged": ["src/format.js", "test/format.test.js"]}},
    {"id": "context-file-de", "writes": ["src/format.js", "test/format.test.js"],
     "order": "Behebe den Fehler bei leeren Namen in src/format.js; das erwartete Verhalten steht in docs/FORMAT.md. "
              "Schreibe einen Regressionstest in test/format.test.js und führe die Tests aus.",
     "expect": {"state": "completed", "verification": "passed", "staged": ["src/format.js", "test/format.test.js"]}},
    {"id": "optional-file-untouched", "writes": ["src/calc.js"],
     "order": "Fix add() in src/calc.js; adjusting src/index.js is fine if it helps.",
     "expect": {"state": "completed", "staged": ["src/calc.js"]}},
    {"id": "protected-en", "writes": ["src/calc.js", "test/calc.test.js"],
     "order": "Fix add() in src/calc.js without touching src/format.js, and add a test in test/calc.test.js. "
              "Run the tests.",
     "expect": {"state": "completed", "verification": "passed", "staged": ["src/calc.js", "test/calc.test.js"]}},
    {"id": "protected-de-violated", "writes": ["src/calc.js"], "touches": ["src/format.js"],
     "order": "Repariere add() in src/calc.js. Finger weg von src/format.js.",
     "expect": {"state": "blocked", "error_has": "protected_file_changed"}},
    {"id": "guard-the-patterns-miss", "writes": ["src/calc.js"],
     "order": "Fix add() in src/calc.js. Under no circumstances modify config/prod.json.",
     # The reading is unsure of config/prod.json (`mentioned`): never told to change it, never held to.
     "expect": {"state": "completed", "staged": ["src/calc.js"], "prompt_lacks": "change each of them"}},
    {"id": "rename-public-and-callers", "writes": ["src/price.js:rename", "src/cart.js:rename"],
     "order": "Rename the public function round to roundPrice in src/price.js and update its caller in "
              "src/cart.js. Run the tests.",
     "expect": {"state": "completed", "verification": "passed", "tasks": 1, "staged": ["src/cart.js", "src/price.js"]}},
    {"id": "rename-caller-forgotten", "writes": ["src/price.js:rename"],
     "order": "Rename the public function round to roundPrice in src/price.js and update its caller in "
              "src/cart.js. Run the tests.",
     # The builder skipped the caller: the guard names it, and the project's test of cart.js is red.
     "expect": {"state": "blocked"}},
    {"id": "bugfix-needs-new-test-de", "writes": ["src/calc.js", "test/calc.test.js"],
     "order": "Die Funktion add(a, b) in src/calc.js rechnet falsch. Repariere sie und ergänze einen Regressionstest "
              "in test/calc.test.js. Führe die Projekttests aus.",
     "expect": {"state": "completed", "verification": "passed", "staged": ["src/calc.js", "test/calc.test.js"]}},
    {"id": "named-file-left-unchanged", "writes": ["src/calc.js"],
     "order": "Fix add() in src/calc.js. src/index.js re-exports it and should keep working as it is.",
     "expect": {"state": "completed", "staged": ["src/calc.js"]}},
    {"id": "docs-only-en", "writes": ["docs/API.md"],
     "order": "Document the add() function in docs/API.md. Do not change any code.",
     "expect": {"state": "completed", "staged": ["docs/API.md"]}},
    {"id": "docs-only-de", "writes": ["docs/API.md"],
     "order": "Dokumentiere die Funktion add() in docs/API.md. Am Code nichts ändern.",
     "expect": {"state": "completed", "staged": ["docs/API.md"]}},
    {"id": "verify-only-en", "writes": [],
     "order": "Just run the test suite and tell me whether it passes. Change nothing.",
     "expect": {"state": "completed", "tasks": 0, "verification": "passed", "builder_calls": 0}},
    {"id": "verify-only-de", "writes": [],
     "order": "Führe nur die Tests aus und sag mir das Ergebnis, ohne etwas zu ändern.",
     "expect": {"state": "completed", "tasks": 0, "verification": "passed", "builder_calls": 0}},
    {"id": "large-repo-tiny-change", "writes": ["README.md"], "extra_files": 2000,
     "order": "Add a usage section to README.md.",
     "expect": {"state": "completed", "tasks": 1, "staged": ["README.md"]}},
]


def _walk(case: dict[str, Any], root: Path) -> dict[str, Any]:
    from apps.cli.grouped import main
    from packages.orchestration import pingpong_loop
    from packages.orchestration.pingpong_provider import FakeProvider

    files = {**REPO, **filler_files(case.get("extra_files", 0), suffix=".txt")}
    repo = commit_repository(root / "work", files)
    prompts: list[str] = []
    with pytest.MonkeyPatch.context() as patch:
        patch.setenv("REMEDY_DATA_DIR", str(root / "data"))
        patch.chdir(repo)
        FakePlannerService(target="src/calc.js").install(patch)
        build, review = FakeProvider.build, FakeProvider.review

        def recorded_build(self, prompt, **kwargs):
            prompts.append(prompt)
            return build(self, prompt, **kwargs)

        def correct_builder(staging: Path, output: Any, goal: str) -> None:
            # Writes the files the task's title names (its deliverable, the further files of its one
            # change, its requested test); `touches` stands for a builder that also edits another.
            written = []
            for key in case["writes"]:
                path = key.split(":")[0]
                if path in goal:
                    (staging / path).parent.mkdir(parents=True, exist_ok=True)
                    (staging / path).write_text(CORRECT[key])
                    written.append(path)
            for path in case.get("touches", []):
                (staging / path).write_text(REPO[path] + "// touched\n")
                written.append(path)
            output.files_changed = written

        def passing_review(self, prompt, **kwargs):
            out = review(self, prompt, **kwargs)
            out.verdict, out.findings, out.summary = "pass", [], "looks right"
            return out
        patch.setattr(FakeProvider, "build", recorded_build)
        patch.setattr(FakeProvider, "review", passing_review)
        patch.setattr(pingpong_loop, "_apply_fake_builder_changes", correct_builder)
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.suppress(SystemExit):
            main(["do", case["order"], "--repo", ".", "--builder-provider", "fake", "--reviewer-provider", "fake",
                  "--json", "--no-ui", "--run-unattended"])
        data = json.loads(out.getvalue())
        from packages.orchestration.pingpong_job import load_job_plan
        from packages.orchestration.pingpong_loop import load_run
        jobs = [load_job_plan(j) for j in data.get("job_ids", [])]
        runs = [load_run(t.run_id) or {} for job in jobs for t in job.tasks if t.run_id]
    return {"data": data, "jobs": jobs, "prompts": prompts, "repo": repo,
            "staged": sorted({f for run in runs for f in run.get("staged_files", [])})}


def check_case(case: dict[str, Any], walk: dict[str, Any]) -> list[str]:
    expect, problems = case["expect"], []
    jobs = walk["jobs"]
    if len(jobs) != 1:
        return [f"jobs: expected 1, got {len(jobs)}: {walk['data'].get('message') or walk['data'].get('steps')}"]
    job = jobs[0]
    state = str(getattr(job.state, "value", job.state))
    if state != expect["state"]:
        problems.append(f"state: expected {expect['state']}, got {state} ({job.error[:200]})")
    if "error_has" in expect and expect["error_has"] not in (job.error or ""):
        problems.append(f"error: {expect['error_has']!r} not in {job.error!r}")
    if "tasks" in expect and len(job.tasks) != expect["tasks"]:
        problems.append(f"tasks: expected {expect['tasks']}, got {len(job.tasks)}")
    if "staged" in expect and walk["staged"] != sorted(expect["staged"]):
        problems.append(f"staged: expected {sorted(expect['staged'])}, got {walk['staged']}")
    verification = (walk["data"].get("jobs") or [{}])[0].get("verification") or {}
    if "verification" in expect and verification.get("status") != expect["verification"]:
        problems.append(f"verification: expected {expect['verification']}, got {verification}")
    if "builder_calls" in expect and len(walk["prompts"]) != expect["builder_calls"]:
        problems.append(f"builder calls: expected {expect['builder_calls']}, got {len(walk['prompts'])}")
    if "prompt_lacks" in expect and any(expect["prompt_lacks"] in p for p in walk["prompts"]):
        problems.append(f"a builder prompt says {expect['prompt_lacks']!r}")
    if any(walk["repo"].joinpath(path).read_text() != text for path, text in REPO.items()):
        problems.append("the repository itself changed: nothing may be applied")
    return problems


def test_the_matrix_is_versioned_and_covers_every_wording_class_of_the_order():
    assert ADVERSARIAL_MATRIX_VERSION == 1
    ids = {case["id"] for case in CASES}
    assert len(ids) == len(CASES)
    for needed in ("two-files-one-change", "three-independent", "context-file", "optional-file", "protected",
                   "rename-public", "bugfix-needs-new-test", "named-file-left-unchanged", "docs-only",
                   "verify-only", "large-repo-tiny-change"):
        assert any(i.startswith(needed) for i in ids), needed


@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
def test_the_order_is_done_as_its_words_ask(case, tmp_path):
    walk = _walk(case, tmp_path)

    assert check_case(case, walk) == [], {"staged": walk["staged"], "steps": walk["data"].get("steps")}
