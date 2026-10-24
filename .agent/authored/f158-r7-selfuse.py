"""F158 R7 — the closure's self-use item: generate it, run it to its approval gate, record it.

Run from the primary checkout: python3 .agent/authored/f158-r7-selfuse.py
Writes .agent/selfuse_f158/ and prints every reading.
Adapted from .agent/authored/f158-r7-selfuse.py: the paths and this header differ, and one file is
added, `valuations.txt`, which holds every `calls` row the run's builds mirrored into a project
ledger beside the valuation F158 recorded for it (DECISION F158 D5), so the record shows what a
real call's normalized cost, basis and pricing version read. Every written file is masked as the
F162 script masked them (DECISION F157 D7). It installs the adapter registry into the worker
adapter slot first (DECISION F315 D2). Never applies the job.
Spends real money: at most the self_use role's default budget.
"""
import dataclasses
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, ".")

from packages.orchestration.doc_staleness import run_staleness_checks  # noqa: E402
from packages.orchestration.self_use_findings import describe_self_use_run_defects  # noqa: E402
from packages.orchestration.self_use_generator import generate_and_append_if_empty  # noqa: E402
from packages.orchestration.self_use_queue import next_self_use_item  # noqa: E402
from packages.orchestration.self_use_runner import run_next_self_use_item  # noqa: E402
from packages.orchestration.worker_adapter_slot import install_worker_adapters  # noqa: E402
from packages.providers.adapters.adapter_registry import WORKER_ADAPTERS_BY_REF  # noqa: E402
from scripts.check_agent_hygiene import _RULES, scan_agent_text  # noqa: E402

install_worker_adapters(WORKER_ADAPTERS_BY_REF)

DEST = Path(".remedy-wt/f158-r7-selfuse").resolve()
OUT = Path(".agent/selfuse_f158")

generated = generate_and_append_if_empty()
print("generate_and_append_if_empty():",
      None if generated is None else (generated.id, generated.title, generated.provenance))
pending = next_self_use_item()
print("next_self_use_item():", pending.id, pending.title, pending.provenance)

started = datetime.now(timezone.utc).isoformat()
t0 = time.monotonic()
entry, job_file_path, plan = run_next_self_use_item(DEST)
wall = time.monotonic() - t0
finished = datetime.now(timezone.utc).isoformat()

OUT.mkdir(parents=True, exist_ok=True)
(OUT / f"{entry.id}.md").write_bytes(Path(job_file_path).read_bytes())
(OUT / "entry_and_job_file.txt").write_text(
    f"Entry ID: {entry.id}\nEntry Title: {entry.title}\nEntry Provenance: {entry.provenance}\n"
    f"Entry Consumed By: {entry.consumed_by}\nJob File Path: {job_file_path}\n", encoding="utf-8")
ec = plan.execution_config
if ec is None:
    ec_dict = {}
elif hasattr(ec, "model_dump"):
    ec_dict = ec.model_dump(mode="json")
elif dataclasses.is_dataclass(ec):
    ec_dict = dataclasses.asdict(ec)
else:
    ec_dict = dict(ec)
(OUT / "execution_config.txt").write_text(json.dumps(ec_dict, indent=2, sort_keys=True) + "\n",
                                          encoding="utf-8")
state = [f"Job ID: {plan.job_id}", f"Job State: {plan.state}", f"Stop Reason: {plan.stop_reason}",
         f"Stop Source: {plan.stop_source}", f"Error: {plan.error}",
         f"Run Manifest Error: {plan.run_manifest_error}",
         f"Budgets: {json.dumps(plan.budgets, sort_keys=True, default=str)}",
         f"Budget Actuals: {json.dumps(plan.budget_actuals, sort_keys=True, default=str)}",
         f"Job Workspace: {plan.job_workspace_path}", "", "Task States:"]
for t in plan.tasks:
    state.append(f"  {t.task_id}: {t.status} (verdict: {t.reviewer_verdict}; final_status: "
                 f"{t.final_status}; repair_rounds_used: {t.repair_rounds_used}; run_id: {t.run_id})")
(OUT / "result_state.txt").write_text("\n".join(state) + "\n", encoding="utf-8")
(OUT / "timing.txt").write_text(f"Started: {started}\nFinished: {finished}\nWall seconds: {wall:.1f}\n",
                                encoding="utf-8")
paths = set(plan.root_changed_files)
for t in plan.tasks:
    if t.apply_manifest is not None and t.apply_manifest.status == "applied":
        paths.update(p.path for p in t.apply_manifest.applied_file_proofs)
(OUT / "changed_paths.txt").write_text("\n".join(sorted(paths)) + "\n" if paths else "NONE\n",
                                       encoding="utf-8")
transcript = [f"Job ID: {plan.job_id}", f"Job Title: {plan.job_title}", f"Job State: {plan.state}",
              f"Stop Reason: {plan.stop_reason}", f"Stop Source: {plan.stop_source}",
              f"Execution: {json.dumps(ec_dict, sort_keys=False)}", "", "Task Summary:"]
for t in plan.tasks:
    transcript += ["", f"Task {t.task_id}:", f"- Status: {t.status}",
                   f"- Reviewer Verdict: {t.reviewer_verdict}", f"- Final Status: {t.final_status}",
                   f"- Error: {t.error}"]
(OUT / "full_transcript.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")

# Every worker_isolation.jsonl line the run's builds wrote, read from each task's run directory,
# so the record shows which method, flags and environment names the real calls ran with.
from packages.orchestration import data_paths  # noqa: E402

iso_lines = []
for t in plan.tasks:
    if t.run_id:
        iso_file = data_paths.run_dir(t.run_id) / "worker_isolation.jsonl"
        if iso_file.is_file():
            iso_lines += [f"{t.task_id}: {line}" for line in iso_file.read_text(encoding="utf-8").splitlines()]
(OUT / "worker_isolation.txt").write_text("\n".join(iso_lines) + "\n" if iso_lines else "NONE\n",
                                          encoding="utf-8")

# Every worker_sandbox.jsonl line the run's builds wrote (DECISION F162 D5), read the same way.
from packages.orchestration.sandbox_profiles import WORKER_SANDBOX_FILENAME  # noqa: E402

sbx_lines = []
for t in plan.tasks:
    if t.run_id:
        sbx_file = data_paths.run_dir(t.run_id) / WORKER_SANDBOX_FILENAME
        if sbx_file.is_file():
            sbx_lines += [f"{t.task_id}: {line}" for line in sbx_file.read_text(encoding="utf-8").splitlines()]
(OUT / "worker_sandbox.txt").write_text("\n".join(sbx_lines) + "\n" if sbx_lines else "NONE\n",
                                        encoding="utf-8")


# Every `calls` row the run's builds mirrored into a project ledger, with the valuation F158 D5
# recorded beside it, read from each ledger under the data root without writing to any of them.
import sqlite3  # noqa: E402

val_lines = []
for ledger in sorted(data_paths.projects_dir().glob("*/ledger.sqlite")):
    conn = sqlite3.connect(f"file:{ledger}?mode=ro", uri=True)
    try:
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if "calls" not in tables:
            continue
        calls = conn.execute(
            "SELECT call_id, task_id, role, model, tokens_in, tokens_out, cost_usd, cost_basis FROM calls "
            "WHERE job_id = ? ORDER BY call_id", (plan.job_id,)).fetchall()
        for call in calls:
            val_lines.append(f"project {ledger.parent.name} call {call[0]}: task {call[1]} role {call[2]} "
                             f"model {call[3]} tokens_in {call[4]} tokens_out {call[5]} cost_usd {call[6]} "
                             f"cost_basis {call[7]}")
            row = None
            if "call_valuations" in tables:
                row = conn.execute(
                    "SELECT adapter, currency, normalized_cost, basis, pricing_version, catalog_cost, "
                    "deviation_percent, cross_check_exceeded, note FROM call_valuations WHERE call_id = ?",
                    (call[0],)).fetchone()
            val_lines.append("  NO VALUATION" if row is None else
                             f"  valuation: adapter {row[0]} currency {row[1]} normalized_cost {row[2]} "
                             f"basis {row[3]} pricing_version {row[4]} catalog_cost {row[5]} "
                             f"deviation_percent {row[6]} cross_check_exceeded {row[7]} note {row[8]!r}")
    finally:
        conn.close()
(OUT / "valuations.txt").write_text("\n".join(val_lines) + "\n" if val_lines else "NONE\n",
                                    encoding="utf-8")

# The staleness catalog over the job's result, after the run, read from the job's branch through a
# temporary worktree this script adds and removes itself when the workspace is gone.
def _stale_lines(root: Path) -> str:
    after = run_staleness_checks(root)
    return "".join(f"{c.check_id} | {c.document} | {c.claim} | {c.truth}\n" for c in after) or "NONE\n"


workspace = Path(plan.job_workspace_path) if plan.job_workspace_path else None
job_branch = f"remedy/job-{plan.job_id}"
if workspace is not None and workspace.is_dir():
    staleness = f"Read from: the job workspace {workspace}\n" + _stale_lines(workspace)
elif subprocess.run(["git", "rev-parse", "--verify", "--quiet", job_branch],
                    capture_output=True).returncode == 0:
    tree = Path(".remedy-wt/f158-r7-jobtree")
    subprocess.run(["git", "worktree", "add", "--detach", str(tree), job_branch],
                   check=True, capture_output=True)
    try:
        staleness = f"Read from: the job branch {job_branch}\n" + _stale_lines(tree.resolve())
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(tree)], check=True)
        subprocess.run(["git", "worktree", "prune"], check=True)
else:
    staleness = f"NO WORKSPACE AND NO BRANCH: {plan.job_workspace_path!r}, {job_branch}\n"
(OUT / "staleness_after.txt").write_text(staleness, encoding="utf-8")

diff = subprocess.run(["git", "diff", f"HEAD...{job_branch}"], capture_output=True, text=True)
(OUT / "job_diff.txt").write_text(
    f"$ git diff HEAD...{job_branch}  (exit {diff.returncode})\n{diff.stdout}{diff.stderr}",
    encoding="utf-8")

defects = describe_self_use_run_defects(plan)
(OUT / "run_defects.txt").write_text(
    ("From describe_self_use_run_defects():\n\n" + "".join(f"{i}. {d}\n" for i, d in enumerate(defects, 1)))
    if defects else "NONE\n", encoding="utf-8")

# The agent-state check of the commit hook refuses a path of this machine under `.agent/`, so every
# written file names the home folder `~` instead (F310 R5).
for written in OUT.iterdir():
    written.write_text(written.read_text(encoding="utf-8").replace(str(Path.home()), "~"), encoding="utf-8")


def _marker(reason: str):
    def replace(match) -> str:
        lead = match.group(0)[0] if match.group(0)[:1] in " \t'\"`(" else ""
        return f"{lead}[MASKED: {reason}]"
    return replace


# DECISION F157 D7, applied to every written file: mask what the guard refuses, or write nothing.
for written in sorted(OUT.iterdir()):
    rel = f".agent/selfuse_f158/{written.name}"
    raw = written.read_text(encoding="utf-8")
    before = scan_agent_text(rel, raw)
    if not before:
        continue
    count, lines = 0, []
    for line in raw.splitlines(keepends=True):
        for reason, pattern in _RULES:
            line, n = pattern.subn(_marker(reason), line)
            count += n
        lines.append(line)
    masked = (f"MASKED COPY: {count} match(es) on {len(before)} line(s) that the agent-state guard refuses are\n"
              "replaced by a [MASKED: <rule>] marker (DECISION F157 D7). The job branch keeps the text whole.\n"
              f"Unmasked sha256: {hashlib.sha256(raw.encode('utf-8')).hexdigest()}\n\n" + "".join(lines))
    after = scan_agent_text(rel, masked)
    if after:
        sys.exit(f"refused: the guard still finds {len(after)} line(s) in {rel}: {after}")
    written.write_text(masked, encoding="utf-8")
    print(f"masked {rel}: {count} match(es) on {len(before)} line(s)")

for name in sorted(p.name for p in OUT.iterdir()):
    print(f"=== {name} ===")
    print((OUT / name).read_text(encoding="utf-8"))
