#!/usr/bin/env python3
"""F116 claim measurement: what Remedy already has for a cost anomaly alarm.

Run from the repository root: `python3 .agent/authored/f116-r1-measure.py`.
Reads source text and imports two modules for their constants; it starts no job,
calls no provider and writes nothing.
"""
import inspect
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))


def src(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def py_files(*tops):
    for top in tops:
        yield from sorted((ROOT / top).rglob("*.py"))


def callers(pattern, *tops):
    rx = re.compile(pattern)
    hits = {}
    for path in py_files(*tops):
        text = path.read_text(encoding="utf-8")
        n = sum(1 for line in text.splitlines()
                if rx.search(line) and not line.lstrip().startswith("def "))
        if n:
            hits[str(path.relative_to(ROOT))] = n
    return hits


from packages.orchestration import watchdog  # noqa: E402
from packages.orchestration import token_ledger  # noqa: E402

print("1. the watchdog's burn tripwire (F077)")
print("   signature:", "evaluate_burn_anomaly" + str(inspect.signature(watchdog.evaluate_burn_anomaly)))
print("   defaults:", watchdog.WatchdogThresholds())
burn_src = inspect.getsource(watchdog.evaluate_burn_anomaly)
print("   reads measured_tokens:", "measured_tokens(entry)" in burn_src,
      " reads a clock or a timestamp:", bool(re.search(r"datetime|ts_utc|time\(", burn_src)))
print("   callers outside its definition:", callers(r"evaluate_burn_anomaly\(", "packages", "apps"))
print("   tests naming it:", callers(r"evaluate_burn_anomaly|TRIP_BURN_ANOMALY|burn_anomaly", "tests"))
print("2. the job runner's safe point")
job_src = src("packages/orchestration/pingpong_job.py")
print("   'def _stop_check(' in pingpong_job.py:", job_src.count("def _stop_check("),
      " calls '_stop_check(':", job_src.count("_stop_check(") - job_src.count("def _stop_check("))
sp_src = src("packages/orchestration/safe_points.py")
print("   safe_points.should_stop order: operator stop, then budget:",
      sp_src.find("stop_requested(job_id") < sp_src.find("evaluate_budget(budgets"))
print("3. the F103 ledger as a time series")
print("   timestamp fields, first match wins:", token_ledger._TIMESTAMP_FIELDS)
crfe = inspect.getsource(token_ledger.call_records_from_evidence)
print("   per-call rows take ONE task-run timestamp:",
      "_first_string(provider_evidence, _TIMESTAMP_FIELDS)" in crfe)
loop_src = src("packages/orchestration/pingpong_loop.py")
block = loop_src[loop_src.find("attempts_evidence = ["):loop_src.find("for seq, a in enumerate(result.provider_attempts")]
usage_fn = loop_src[loop_src.find("def _attempt_usage_evidence("):]
usage_fn = usage_fn[:usage_fn.find("\ndef ")]
print("   keys of one provider attempt:", re.findall(r'"([a-z_]+)":', block),
      "plus", re.findall(r'"([a-z_]+)":', usage_fn[usage_fn.rfind("return {"):]))
print("   cost bases:", sorted(token_ledger.COST_BASES))
print("4. expectation bands (F074 is unchecked in STATUS)")
print("   modules naming an expectation band:", callers(r"expectation_band|class_expectation", "packages", "apps"))
print("5. unattended mode")
print("   escalation.auto_apply_safe_default defined:",
      "def auto_apply_safe_default(" in src("packages/orchestration/escalation.py"))
catalog = src("apps/cli/command_catalog.py")
owners = []
for m in re.finditer(r'ArgDef\("--unattended"', catalog):
    names = re.findall(r'command_id="([^"]+)"', catalog[:m.start()])
    owners.append(names[-1] if names else "?")
print("   commands declaring --unattended:", owners)
for rel in ("packages/orchestration/pingpong_job.py", "packages/orchestration/long_run_executor.py",
            "packages/orchestration/orchestrator_loop.py"):
    print("   'unattended' in", rel + ":", src(rel).count("unattended"))
print("6. what F116 would add")
for rel in ("packages/orchestration/burn_detector.py", "tests/orchestration/test_burn_detector.py"):
    print("  ", rel, "exists:", (ROOT / rel).exists())
