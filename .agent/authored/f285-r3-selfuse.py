"""F285 R3 C3 — the closure's self-use item: generate it, run it to its approval gate, record it.

Run from the primary checkout: python3 .remedy-wt/f285-r3-payloads/selfuse.py
Writes .agent/selfuse_f285/ (the files .agent/selfuse_f026/ holds, plus changed_paths.txt) and
prints every reading. Never applies the job. Spends real money: at most 8 calls and 6.00 USD.
"""
import dataclasses
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, ".")

from packages.orchestration.self_use_findings import describe_self_use_run_defects  # noqa: E402
from packages.orchestration.self_use_generator import generate_and_append_if_empty  # noqa: E402
from packages.orchestration.self_use_queue import next_self_use_item  # noqa: E402
from packages.orchestration.self_use_runner import run_next_self_use_item  # noqa: E402

DEST = Path("/home/decodeux/Repos/remedy/.remedy-wt/f285-r3-selfuse")
OUT = Path(".agent/selfuse_f285")

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
defects = describe_self_use_run_defects(plan)
(OUT / "run_defects.txt").write_text(
    ("From describe_self_use_run_defects():\n\n" + "".join(f"{i}. {d}\n" for i, d in enumerate(defects, 1)))
    if defects else "NONE\n", encoding="utf-8")

for name in sorted(p.name for p in OUT.iterdir()):
    print(f"=== {name} ===")
    print((OUT / name).read_text(encoding="utf-8"))
