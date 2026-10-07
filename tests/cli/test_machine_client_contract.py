"""F295 T004 — the machine client's whole path, driven through the command line alone.

`docs/roadmap/features/T12_F295.md` closes on one test that drives Remedy exactly as Luna's runner
will (`docs/roadmap/design/luna-control-plane-v1.md`, "Gate A"): an order file with a cost cap,
`remedy do <file> --json --no-ui --yes` with the fake builder and reviewer, the digest from
`remedy status --json`, one decision answered with `remedy decision resolve --json`, `remedy job
apply <job> --approve --json`, and `remedy change proof <job> --json`. This is that test.

Every command runs through `apps.cli.grouped.main` in this process, with the environment a child
process would have, in a scratch git repository and on a scratch data root. Its stdin is a stand-in
that fails the test if anything reads it, so the path is proved to ask nothing on stdin.

The decision the path answers is the budget decision: the order's run is given a deadline that has
already passed, so its budget stops it before any task runs and raises `budget:<request id>`, the
one decision a fake run raises on its own. Answering it `extend` with a later deadline lets
`remedy job run` finish the job (DECISIONs F295 D11 and D13). The same stop raised a contract
remainder decision, which the `extend` answers `no` (DECISION F295 D19), so after the run the
digest lists no open decision for the job.

The second half of this file holds the contract page, `docs/system/machine-client-contract-v1.md`,
to the gate test (DECISION F295 D17): the tables of the page's section "The path, step by step"
name exactly the commands, flags, JSON keys and exit codes the gate test uses, read from this
file's own syntax tree, and the page carries the gate test's order file byte for byte.
"""
from __future__ import annotations

import ast
import contextlib
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

#: The deadline that has passed before the run starts, and the one the answer raises it to.
PAST_DEADLINE = "2000-01-01T00:00:00+00:00"
LATER_DEADLINE = "2999-01-01T00:00:00+00:00"

#: The order as Luna's runner writes it: a header with the cost cap, then the order text.
ORDER_FILE_TEXT = "---\nmax-cost-usd: 1\n---\nAdd a line saying hello to README.md\n"

_GIT_IDENTITY = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                 "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}


class _StdinNobodyMayRead(io.TextIOBase):
    """A stdin whose every read fails the test: the path must never ask a question there."""

    def read(self, *args, **kwargs):
        raise AssertionError("the machine client's path read stdin")

    def readline(self, *args, **kwargs):
        raise AssertionError("the machine client's path read stdin")

    def isatty(self) -> bool:
        return False


def _remedy(args: list[str], cwd: Path, env: dict[str, str]) -> tuple[int, dict]:
    """Run `remedy <args> --json` here as a child process would run, and parse its one envelope."""
    from apps.cli.grouped import main

    out, err = io.StringIO(), io.StringIO()
    saved_env, saved_cwd, saved_stdin = dict(os.environ), os.getcwd(), sys.stdin
    os.environ.clear()
    os.environ.update(env)
    os.chdir(str(cwd))
    sys.stdin = _StdinNobodyMayRead()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                main([*args, "--json"])
                code = 0
            except SystemExit as exc:
                code = exc.code if isinstance(exc.code, int) else 1
    finally:
        sys.stdin = saved_stdin
        os.chdir(saved_cwd)
        os.environ.clear()
        os.environ.update(saved_env)
    try:
        body = json.loads(out.getvalue())
    except ValueError as exc:
        raise AssertionError(
            f"remedy {' '.join(args)} --json printed no single JSON envelope:\n"
            f"stdout: {out.getvalue()[-2000:]}\nstderr: {err.getvalue()[-2000:]}") from exc
    return code, body


def _scratch_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    env = {**os.environ, **_GIT_IDENTITY}
    subprocess.run(["git", "init", "-q", str(repo)], check=True, env=env)
    (repo / "README.md").write_text("# Scratch\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "README.md"], check=True, env=env)
    subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "init"], check=True, env=env)
    return repo


def _digest_job(digest: dict, job_id: str) -> dict:
    jobs = [job for job in digest["jobs"] if job["job_id"] == job_id]
    assert len(jobs) == 1, f"the digest lists job {job_id} {len(jobs)} times"
    return jobs[0]


def test_a_program_drives_an_order_file_to_its_proof_through_the_command_line(tmp_path):
    repo = _scratch_repo(tmp_path)
    order_file = tmp_path / "order.md"
    order_file.write_text(ORDER_FILE_TEXT, encoding="utf-8")
    env = {**os.environ, **_GIT_IDENTITY, "REMEDY_DATA_DIR": str(tmp_path / "data")}

    # 1. Propose: the order file, unattended, with the fake providers. The deadline has passed,
    #    so the budget stops the run before any task runs; `remedy do` says so and exits 1.
    code, done = _remedy(
        ["do", str(order_file), "--no-ui", "--yes", "--no-llm",
         "--builder-provider", "fake", "--reviewer-provider", "fake",
         "--deadline", PAST_DEADLINE], repo, env)
    assert code == 1, done
    assert len(done["job_ids"]) == 1
    job_id = done["job_ids"][0]
    mission_id = done["mission_id"]

    # 2. Read: the digest names the mission the order file started, its job, the job's state,
    #    its cost with its basis, its evidence, and the open budget decision.
    code, status = _remedy(["status"], repo, env)
    assert code == 0 and status["ok"] is True
    digest = status["client"]
    assert digest["version"] == 1
    missions = [m for project in digest["projects"] for m in project["missions"]
                if m["mission_id"] == mission_id]
    assert len(missions) == 1
    assert missions[0]["order_source_path"] == str(order_file)
    assert missions[0]["job_ids"] == [job_id]
    job = _digest_job(digest, job_id)
    assert job["mission_id"] == mission_id
    assert job["state"] == "stopped"
    assert set(job["cost"]) == {"basis", "value_usd"}
    assert Path(job["evidence"]["run_manifest_path"]).is_file()
    budget = [d for d in digest["decisions"]
              if d["job_id"] == job_id and d["type"] == "token_budget"]
    assert len(budget) == 1
    assert budget[0]["options"] == ["extend", "abandon"]
    remainder = [d for d in digest["decisions"]
                 if d["job_id"] == job_id and d["type"] == "task_decision"]
    assert len(remainder) == 1
    assert job_id not in digest["awaiting_apply"]

    # 3. Answer: the budget decision, extended past the deadline that stopped it.
    code, answered = _remedy(
        ["decision", "resolve", job_id, budget[0]["decision_id"], "--reason", "extend",
         "--answer", f"deadline={LATER_DEADLINE}"], repo, env)
    assert code == 0, answered
    assert answered["outcome"] == "extended"
    assert answered["next_command"] == f"remedy job run {job_id} --json"
    # The extend answered the remainder decision the same stop raised (DECISION F295 D19).
    assert answered["closed_decisions"] == [remainder[0]["decision_id"]]
    # The order file's header cap is the job's own budget, kept beside the raised deadline.
    assert answered["budgets"]["max_cost_usd"] == 1.0

    # 4. The answered job runs to its end through its own fake providers.
    code, ran = _remedy(["job", "run", job_id], repo, env)
    assert code == 0, ran
    code, status = _remedy(["status"], repo, env)
    digest = status["client"]
    assert _digest_job(digest, job_id)["state"] == "completed"
    assert _digest_job(digest, job_id)["waits_for_apply"] is True
    assert job_id in digest["awaiting_apply"]
    assert not [d for d in digest["decisions"] if d["job_id"] == job_id]

    # 5. Approve and apply: the reviewed result lands in the repository.
    code, applied = _remedy(["job", "apply", job_id, "--approve"], repo, env)
    assert code == 0, applied
    assert applied["status"] == "applied"
    assert applied["files_applied"]
    for path in applied["files_applied"]:
        assert (repo / path).is_file(), path

    # 6. The proof names the apply that was approved, and calls nothing verified.
    code, proof = _remedy(["change", "proof", job_id], repo, env)
    assert code == 0, proof
    assert [record["job_apply_id"] for record in proof["job_applies"]] == [applied["job_apply_id"]]
    assert proof["job_applies"][0]["status"] == "applied"
    assert proof["job_applies"][0]["files_applied"] == applied["files_applied"]
    assert proof["overall_status"] != "verified"

    # 7. The digest no longer lists the job as waiting for its apply.
    code, status = _remedy(["status"], repo, env)
    assert _digest_job(status["client"], job_id)["waits_for_apply"] is False
    assert job_id not in status["client"]["awaiting_apply"]


# The contract page and the gate test name the same things (DECISION F295 D17).

_REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PAGE = _REPO_ROOT / "docs" / "system" / "machine-client-contract-v1.md"

#: The section of the page whose tables are held to the gate test, and those tables by kind.
PATH_SECTION_HEADING = "## The path, step by step"
PAGE_TABLES = {"commands": "Commands", "flags": "Flags", "keys": "JSON keys",
               "exit codes": "Exit codes"}

#: The functions that make up the gate test: the test and the two helpers it calls.
GATE_FUNCTIONS = (
    "test_a_program_drives_an_order_file_to_its_proof_through_the_command_line",
    "_remedy",
    "_digest_job",
)


def _gate_names() -> dict[str, set[str]]:
    """The commands, flags, JSON keys and exit codes the gate test uses, read from its syntax.

    A command is `remedy` and the leading words of a list `_remedy` is called with; a flag is a
    string that starts with `--`; a JSON key is a string a subscript reads; an exit code is an
    integer `code` is compared with.
    """
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    functions = [node for node in tree.body
                 if isinstance(node, ast.FunctionDef) and node.name in GATE_FUNCTIONS]
    assert sorted(function.name for function in functions) == sorted(GATE_FUNCTIONS)
    names: dict[str, set[str]] = {kind: set() for kind in PAGE_TABLES}
    for function in functions:
        for node in ast.walk(function):
            if (isinstance(node, ast.Constant) and isinstance(node.value, str)
                    and node.value.startswith("--")):
                names["flags"].add(node.value)
            if (isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant)
                    and isinstance(node.slice.value, str)):
                names["keys"].add(node.slice.value)
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id == "_remedy" and node.args
                    and isinstance(node.args[0], ast.List)):
                words = []
                for element in node.args[0].elts:
                    if (not isinstance(element, ast.Constant) or not isinstance(element.value, str)
                            or element.value.startswith("--")):
                        break
                    words.append(element.value)
                names["commands"].add(" ".join(["remedy", *words]))
            if (isinstance(node, ast.Compare) and isinstance(node.left, ast.Name)
                    and node.left.id == "code"):
                for comparator in node.comparators:
                    if isinstance(comparator, ast.Constant) and isinstance(comparator.value, int):
                        names["exit codes"].add(str(comparator.value))
    return names


def _page_table(title: str) -> set[str]:
    """The backticked first cell of every row of the table under `### <title>` in the path section."""
    text = CONTRACT_PAGE.read_text(encoding="utf-8")
    section = text[text.index(PATH_SECTION_HEADING) + len(PATH_SECTION_HEADING):]
    section_end = section.find("\n## ")
    section = section if section_end < 0 else section[:section_end]
    marker = f"\n### {title}\n"
    table = section[section.index(marker) + len(marker):]
    table_end = table.find("\n### ")
    table = table if table_end < 0 else table[:table_end]
    cells = []
    for line in table.splitlines():
        if line.startswith("|"):
            match = re.fullmatch(r"`([^`]+)`", line.split("|")[1].strip())
            if match:
                cells.append(match.group(1))
    assert len(cells) == len(set(cells)), f"the page's {title} table names an entry twice"
    return set(cells)


@pytest.mark.parametrize("kind", sorted(PAGE_TABLES))
def test_the_contract_page_names_exactly_what_the_gate_test_uses(kind):
    used = _gate_names()[kind]
    assert used, f"no {kind} read from the gate test: the reading of its syntax is broken"
    named = _page_table(PAGE_TABLES[kind])
    assert sorted(named - used) == [], f"the page names {kind} the gate test does not use"
    assert sorted(used - named) == [], f"the gate test uses {kind} the page does not name"


def test_the_contract_page_carries_the_gate_tests_order_file():
    assert f"```\n{ORDER_FILE_TEXT}```\n" in CONTRACT_PAGE.read_text(encoding="utf-8")
