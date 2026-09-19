"""Every collected test is selected by some CI stage (F273 T015 (b)).

`fast` excludes `slow` and `standard` selects `(integration or subprocess)`, so
a test marked only `slow` that lives outside the path-marked directories would
belong to no stage and never run in CI, silently. This guard makes it loud.

It asserts COVERAGE only. Overlap is not a defect here: `budgets` and `smoke`
select by path on top of the marker stages by construction, which
`packages/orchestration/ci_stages.py` states. A stage CI does not run still
covers its tests when it names the manual command that runs them (`excluded`).

The corpus is collected ONCE, in a child pytest, with each item's marker names.
Every stage's selection is then evaluated in-process from the stage table: the
marker expression through pytest's own `-m` expression evaluator, the path
arguments by prefix. Nothing is re-collected per stage and nothing is written
outside `tmp_path`. The failure names the uncovered node ids, never a count.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from _pytest.mark.expression import Expression

from packages.orchestration.ci_stages import CI_STAGES, pytest_argv_for_stage

REPO_ROOT = Path(__file__).resolve().parents[2]

#: Runs in a child interpreter: collect the whole corpus the way CI's stages do
#: (no path argument, from the repository root) and dump node id -> marker names
#: AFTER every `pytest_collection_modifyitems` hook, conftest's path marks included.
_COLLECT = """
import json, sys
import pytest

class _Dump:
    def pytest_collection_finish(self, session):
        rows = {item.nodeid: sorted({m.name for m in item.iter_markers()})
                for item in session.items}
        with open(sys.argv[1], "w", encoding="utf-8") as fh:
            json.dump(rows, fh)

sys.exit(pytest.main(["--collect-only", "-q", "-p", "no:cacheprovider"], plugins=[_Dump()]))
"""


def _collect_corpus(out: Path) -> dict[str, list[str]]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTEST_")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, "-B", "-c", _COLLECT, str(out)],
        cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=600,
    )
    assert proc.returncode == 0, proc.stdout[-2000:] + proc.stderr[-2000:]
    return json.loads(out.read_text(encoding="utf-8"))


def _stage_selects(stage, nodeid: str, markers: set[str]) -> bool:
    argv = pytest_argv_for_stage(stage)
    expression = argv[argv.index("-m") + 1]
    paths = [a for a in argv if a not in ("-m", expression, "-q")]
    if paths and not any(nodeid == p or nodeid.startswith((p + "::", p.rstrip("/") + "/"))
                         for p in paths):
        return False
    return Expression.compile(expression).evaluate(
        lambda name, /, **kwargs: not kwargs and name in markers)


@pytest.mark.subprocess
def test_every_collected_test_is_selected_by_a_stage(tmp_path):
    corpus = _collect_corpus(tmp_path / "corpus.json")
    assert corpus, "the collection returned no node ids"
    covering = [s for s in CI_STAGES if s.runs_in_ci or s.manual_command.strip()]
    uncovered = sorted(
        nodeid for nodeid, markers in corpus.items()
        if not any(_stage_selects(s, nodeid, set(markers)) for s in covering)
    )
    assert not uncovered, (
        "these tests belong to no CI stage and to no stage with a manual command, "
        "so nothing ever runs them:\n" + "\n".join(uncovered))
