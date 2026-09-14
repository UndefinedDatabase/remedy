# F275 T003 — the CLASSIC STORE SEAM, ENUMERATED

## 1. What this file is

> Measured at `4921e117`, this round's base, over the tracked tree at that commit.
> This file ENUMERATES the classic store seam — every call of `save_job`,
> `load_job`, `load_job_safe` and `resolve_job_id` — which is the half of the
> atomic record flip DECISION F275 D17 sized but gave no site list. It changes
> nothing and flips nothing: NO LINE under `packages/`, `apps/`, `tests/` or
> `scripts/` moved in the round that wrote it. It is a measurement, and the
> DECISION that rules the flip's route is owed on the complete figure, of which
> this is the second of three parts — the round 36 enumeration is the first and
> the UUID-shaped sites are the third and are NOT enumerated here.

## 2. The instrument

A site is one `(path, line, function)` triple, resolved by `ast` over the
tracked `.py` files `git ls-files` names — never by grep, so a call inside a
comment or a string is not a site and a call spelled `store.save_job(...)` is.
The source is embedded here so the measurement is reproducible from this
artefact alone, which is the convention `.agent/f275_t002_flip_inventory.md` set.

```python
"""F275 T003 — enumerate the CLASSIC STORE SEAM by `ast`, at this round's base.

DECISION F275 D17 sized the flip over `Job.id` and `Job.name` and gave the rest
of the atomic commit no site list. The round 36 enumeration covers that half. This
covers the half a rename cannot reach: every call of the four classic-store
functions, which change NAME and, at `resolve_job_id`, ID SHAPE.

A site is one `(path, line, function)` triple, resolved by `ast` over the tracked
`.py` files `git ls-files` names, never by grep.
"""
import ast
import collections
import subprocess
import sys

SEAM = ("save_job", "load_job", "load_job_safe", "resolve_job_id")


def tracked():
    return [p for p in subprocess.run(["git", "ls-files", "*.py"],
                                      capture_output=True, text=True).stdout.split() if p]


def called_name(node):
    f = node.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return None


def main():
    per_file = collections.defaultdict(lambda: collections.defaultdict(set))
    parsed = failed = 0
    for path in tracked():
        try:
            tree = ast.parse(open(path, "rb").read(), filename=path)
        except SyntaxError:
            failed += 1
            continue
        parsed += 1
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                name = called_name(n)
                if name in SEAM:
                    per_file[path][name].add(n.lineno)

    prod = {p for p in per_file if not p.startswith("tests/")}
    test = {p for p in per_file if p.startswith("tests/")}
    sites = sum(len(v) for f in per_file.values() for v in f.values())
    print(f"tracked .py parsed {parsed}, unparsable {failed}")
    print(f"seam sites (path, line, function): {sites}")
    print(f"files: {len(per_file)}  production {len(prod)}  test {len(test)}")
    for name in SEAM:
        p = sum(len(per_file[f][name]) for f in prod)
        t = sum(len(per_file[f][name]) for f in test)
        print(f"  {name:<18} total {p + t:>4}  production {p:>4}  test {t:>4}")

    if len(sys.argv) > 1 and sys.argv[1] == "--rows":
        print()
        for path in sorted(per_file):
            cells = []
            for name in SEAM:
                lines = sorted(per_file[path][name])
                cells.append(f"{name}: " + (",".join(map(str, lines)) if lines else "-"))
            print(f"{path} | " + " | ".join(cells))


if __name__ == "__main__":
    main()
```

Run from the repository root, the tool written to the gitignored scratch:

```
python3 .remedy-wt/r38_seam_enum.py
python3 .remedy-wt/r38_seam_enum.py --rows
```

## 3. Figures — measured, against the reviewer's carried figures

| figure | measured | reviewer | verdict |
|---|---:|---:|---|
| tracked `.py` parsed | 991 | 991 | same |
| unparsable | 0 | 0 | same |
| seam sites (path, line, function) | 821 | 821 | same |
| files holding a seam site | 152 | 152 | same |
|   of which production | 52 | 52 | same |
|   of which test | 100 | 100 | same |
| `save_job` total | 513 | 513 | same |
| `save_job` production | 70 | 70 | same |
| `save_job` test | 443 | 443 | same |
| `load_job` total | 262 | 262 | same |
| `load_job` production | 123 | 123 | same |
| `load_job` test | 139 | 139 | same |
| `load_job_safe` total | 6 | 6 | same |
| `load_job_safe` production | 6 | 6 | same |
| `load_job_safe` test | 0 | 0 | same |
| `resolve_job_id` total | 40 | 40 | same |
| `resolve_job_id` production | 32 | 32 | same |
| `resolve_job_id` test | 8 | 8 | same |
| the enumeration renders file lines | 152 | 152 | same |
| round 36 enumeration files | 184 | 184 | same |
| seam files | 152 | 152 | same |
| union of the two file sets | 228 | 228 | same |
| files the seam ADDS (no enumerated `.id`/`.name` site) | 44 | 44 | same |
| files both instruments name | 108 | 108 | same |
| files the SEAM is blind to (round 36 only) | 76 | 76 | same |

## 4. THE ENUMERATION

One line per file, sorted by path, in the exact form the tool emits. The
numbers are the sorted distinct line numbers of each call site in that file
for that function; `-` means that function is not called in that file.

```
apps/cli/commands/brain.py | save_job: - | load_job: 25,72,123,176,289,343,368,389,414,449,497 | load_job_safe: - | resolve_job_id: -
apps/cli/commands/change.py | save_job: - | load_job: 20,45,75 | load_job_safe: - | resolve_job_id: 18,43,73
apps/cli/commands/context.py | save_job: - | load_job: 30 | load_job_safe: - | resolve_job_id: -
apps/cli/commands/contract_cmd.py | save_job: 35,74,176 | load_job: 25,64,131 | load_job_safe: - | resolve_job_id: -
apps/cli/commands/dashboard_cmd.py | save_job: - | load_job: 27,61 | load_job_safe: - | resolve_job_id: -
apps/cli/commands/decision.py | save_job: 288 | load_job: 29,256,299 | load_job_safe: - | resolve_job_id: 27
apps/cli/commands/do_cmd.py | save_job: 312,327,342,375,3008 | load_job: 2936 | load_job_safe: - | resolve_job_id: 2934
apps/cli/commands/event.py | save_job: - | load_job: 27 | load_job_safe: - | resolve_job_id: -
apps/cli/commands/file.py | save_job: - | load_job: 25 | load_job_safe: - | resolve_job_id: -
apps/cli/commands/guide.py | save_job: - | load_job: 25 | load_job_safe: - | resolve_job_id: -
apps/cli/commands/job.py | save_job: 106,347,386,411,651 | load_job: 189,235,370,393,423,438,760,987,1096,1119,1208,1567,1685,1725,1834,1889,1966,2011,2173 | load_job_safe: - | resolve_job_id: 187,233,368,391,421,436,758,985,1094,1117,1206,1565,1683,1723,1832,1887,1955,2011
apps/cli/commands/job_context_cmd.py | save_job: - | load_job: 275 | load_job_safe: - | resolve_job_id: -
apps/cli/commands/job_stop_cmd.py | save_job: - | load_job: 52 | load_job_safe: - | resolve_job_id: 119
apps/cli/commands/memory.py | save_job: 343,384 | load_job: 149,307,340,381 | load_job_safe: - | resolve_job_id: -
apps/cli/commands/patch.py | save_job: 108,137,379 | load_job: 29,65,94,123,152,189,320 | load_job_safe: - | resolve_job_id: 27,63,92,121,150,187,318
apps/cli/commands/policy.py | save_job: - | load_job: 24,59 | load_job_safe: - | resolve_job_id: -
apps/cli/commands/project.py | save_job: 164,465 | load_job: 156,452 | load_job_safe: - | resolve_job_id: 449
apps/cli/commands/propose_cmd.py | save_job: - | load_job: 43 | load_job_safe: - | resolve_job_id: -
apps/cli/commands/readiness.py | save_job: - | load_job: 24,87 | load_job_safe: - | resolve_job_id: -
apps/cli/commands/repair_cmd.py | save_job: - | load_job: 57,136,217 | load_job_safe: - | resolve_job_id: -
apps/cli/commands/repo.py | save_job: - | load_job: 62,172 | load_job_safe: - | resolve_job_id: -
apps/cli/commands/review_cmd.py | save_job: 34,115,149 | load_job: 24,70,112,146 | load_job_safe: - | resolve_job_id: -
apps/cli/commands/snapshot_cmds.py | save_job: - | load_job: 32,109 | load_job_safe: - | resolve_job_id: -
apps/cli/commands/test_cmds.py | save_job: - | load_job: 105,195 | load_job_safe: - | resolve_job_id: -
packages/orchestration/autorun.py | save_job: 153,168,602,690,700,726 | load_job: - | load_job_safe: - | resolve_job_id: -
packages/orchestration/continue_from_node.py | save_job: 100 | load_job: - | load_job_safe: - | resolve_job_id: -
packages/orchestration/do_continue.py | save_job: - | load_job: 356,564,695,734,800,806,819 | load_job_safe: - | resolve_job_id: -
packages/orchestration/do_run.py | save_job: 241,266,427,503,526 | load_job: - | load_job_safe: - | resolve_job_id: -
packages/orchestration/flight_plan.py | save_job: 824,831 | load_job: - | load_job_safe: - | resolve_job_id: -
packages/orchestration/gauntlet_runner.py | save_job: - | load_job: - | load_job_safe: 353 | resolve_job_id: -
packages/orchestration/handoff.py | save_job: - | load_job: - | load_job_safe: 255 | resolve_job_id: -
packages/orchestration/job_fulfillment.py | save_job: 587,647,669,709,761,1030 | load_job: 604,637,926,951,1028 | load_job_safe: - | resolve_job_id: -
packages/orchestration/mission_readiness.py | save_job: - | load_job: 187 | load_job_safe: - | resolve_job_id: -
packages/orchestration/mission_state.py | save_job: 1073,1117,1140 | load_job: 1046 | load_job_safe: 662 | resolve_job_id: -
packages/orchestration/orchestrator_brain.py | save_job: - | load_job: 307 | load_job_safe: - | resolve_job_id: -
packages/orchestration/orchestrator_loop.py | save_job: 1653,1947 | load_job: 375,1742,1933 | load_job_safe: - | resolve_job_id: -
packages/orchestration/patch_apply.py | save_job: 327 | load_job: - | load_job_safe: - | resolve_job_id: -
packages/orchestration/patch_revert.py | save_job: 241 | load_job: - | load_job_safe: - | resolve_job_id: -
packages/orchestration/proposed_tasks.py | save_job: 671 | load_job: 653 | load_job_safe: 699,826 | resolve_job_id: -
packages/orchestration/real_test_execution.py | save_job: - | load_job: 228,323,340,428 | load_job_safe: - | resolve_job_id: -
packages/orchestration/repair_loop.py | save_job: 103,204,247,727,915,1013,1370,1381 | load_job: 84,252,611,793,1104,1410 | load_job_safe: - | resolve_job_id: -
packages/orchestration/repair_request_builder.py | save_job: 533 | load_job: 465 | load_job_safe: - | resolve_job_id: -
packages/orchestration/self_dogfood.py | save_job: - | load_job: 373,470 | load_job_safe: - | resolve_job_id: -
packages/orchestration/self_dogfood_execution.py | save_job: - | load_job: 472,663 | load_job_safe: - | resolve_job_id: -
packages/orchestration/storage.py | save_job: - | load_job: 111 | load_job_safe: - | resolve_job_id: -
packages/orchestration/task_execution.py | save_job: - | load_job: - | load_job_safe: 203 | resolve_job_id: -
packages/orchestration/test_execution_service.py | save_job: 920,979,1032 | load_job: 594,893,947,1023 | load_job_safe: - | resolve_job_id: -
packages/orchestration/test_failure_artifact.py | save_job: 345,411 | load_job: - | load_job_safe: - | resolve_job_id: -
packages/orchestration/token_economy.py | save_job: - | load_job: 342 | load_job_safe: - | resolve_job_id: -
packages/orchestration/ui_server.py | save_job: 3333,3405 | load_job: 242 | load_job_safe: - | resolve_job_id: -
packages/orchestration/watchdog.py | save_job: 543 | load_job: 521 | load_job_safe: - | resolve_job_id: -
packages/orchestration/worker_queue.py | save_job: 534 | load_job: 451,584 | load_job_safe: - | resolve_job_id: -
tests/cli/test_decision_answers.py | save_job: 105,121,135,159,178,192,213,227,239,256,272,287 | load_job: 111,129,142,165,182,205,217,231,243,398 | load_job_safe: - | resolve_job_id: -
tests/cli/test_do_continue_cli.py | save_job: 36 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/cli/test_file_provenance_cli.py | save_job: 89 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/cli/test_golden_path.py | save_job: 207 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/cli/test_job_commands.py | save_job: 451 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/cli/test_job_context_cmd.py | save_job: 94 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/cli/test_job_digest_cli.py | save_job: 58 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/cli/test_job_report.py | save_job: 54 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/cli/test_loop_cmd.py | save_job: - | load_job: 173,187 | load_job_safe: - | resolve_job_id: -
tests/cli/test_open_decisions_view.py | save_job: 75,224,235,288,301,327 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/cli/test_orchestrator_brain_cli.py | save_job: 25 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/cli/test_patch_cmd.py | save_job: 113 | load_job: 167,190,208,223,244,261,326 | load_job_safe: - | resolve_job_id: 337,357
tests/cli/test_plan_approval.py | save_job: 388,402,417 | load_job: 264,395,409 | load_job_safe: - | resolve_job_id: -
tests/cli/test_product_spine.py | save_job: 502,586,603 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/cli/test_propose_cli.py | save_job: 45,335 | load_job: 285,301 | load_job_safe: - | resolve_job_id: -
tests/cli/test_real_test_execution_cli.py | save_job: 22 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/cli/test_repair_request_cli.py | save_job: 26 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/cli/test_repair_runtime.py | save_job: 58 | load_job: 178 | load_job_safe: - | resolve_job_id: -
tests/cli/test_repair_v1_cli.py | save_job: 35,130 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/cli/test_self_dogfood_cli.py | save_job: 25,106 | load_job: 102 | load_job_safe: - | resolve_job_id: -
tests/cli/test_self_dogfood_execution_cli.py | save_job: 33 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_approval_queue.py | save_job: 167,202,226,240,260,282,338,361,373 | load_job: 234,380 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_autonomy.py | save_job: 278,293,314,347,425,1055,1073,1088,1102,1124,1144 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_autorun.py | save_job: 188,208,227,304,321,336,351,437,455,469,533,549,571,586,608,627 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_builder_visibility.py | save_job: 17,42,62,97 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_checkpoints.py | save_job: 146 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_command_discovery.py | save_job: 239 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_diff_repair_apply.py | save_job: 55 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_do_continue.py | save_job: 82,166 | load_job: 302,406 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_do_run.py | save_job: - | load_job: 147,351 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_dod_gate.py | save_job: 293,403 | load_job: 304 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_escalation.py | save_job: 687,712,730,996 | load_job: 694,1007,1027 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_event_ledger.py | save_job: 270 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_fence_production_e2e.py | save_job: 46,160,273 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_handoff.py | save_job: 136 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_job_fulfillment.py | save_job: 345,426,494,527,574,593,623,688,954,1028,1077,1109,1130,1317,1355,1377,1400,1418,1437,1452,1471,1552,1620,1667 | load_job: 988,1037,1114,1135,1475 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_long_run_executor.py | save_job: 741,854,876,895 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_loop_run.py | save_job: 337,338,349,350 | load_job: 371,514 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_mission_e2e.py | save_job: 141,158,182,193 | load_job: 154,174,188,349 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_mission_readiness.py | save_job: 40,53,168 | load_job: 123 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_mission_state.py | save_job: 418,433,448,732,883 | load_job: 820 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_orchestrator_brain.py | save_job: 40,75,91,96,160,180 | load_job: 94,139,155,195 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_project_brain.py | save_job: 260,273,383,443,789,819,852,907,927,958,1015,1053,1108,1109,1186,1330,1353,1384,1406,1425,1448,1472 | load_job: 1059 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_proposed_tasks.py | save_job: 68 | load_job: 564,655 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_queue_executor_binding.py | save_job: - | load_job: 115,154,167 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_real_test_execution.py | save_job: 30 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_repair_apply_cycle.py | save_job: 34 | load_job: 70,83,94,118,143 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_repair_loop_hardened.py | save_job: 34,60,86,115,139,167,199 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_repair_loop_v1.py | save_job: 34,56 | load_job: 154,199,230 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_repair_request_builder.py | save_job: 41,95 | load_job: 69,71,76,110,116,122,128,134,140,147 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_repository_snapshot.py | save_job: 113 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_resume_cli.py | save_job: 59,121,233,246,258,409 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_resume_kill.py | save_job: - | load_job: 260 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_self_dogfood.py | save_job: 47,147 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_self_dogfood_execution.py | save_job: 55,108 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_source_apply.py | save_job: 147,256,698 | load_job: 268,285,288,314,341,364 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_source_apply_transaction.py | save_job: 40 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_stop_reasons.py | save_job: 121,153,171,191 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_structured_planner_cli.py | save_job: 49 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_task_execution.py | save_job: 156,169 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_test_failure_repair.py | save_job: 55 | load_job: 559,576,597,611,626 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_token_economy.py | save_job: 35 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_token_economy_integration.py | save_job: 27 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_watchdog.py | save_job: 471,595,720,889 | load_job: 493,561,579,592,768,902 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_worker_execution.py | save_job: 33,355,371,404 | load_job: 50,82,92,118,125,141,157,279,352,362,368,401 | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_worktree_lifecycle.py | save_job: 178 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/orchestration/test_worktree_resume_cli.py | save_job: 102 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/regression/test_named_bugs.py | save_job: 767,782,804,816 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/storage/test_persistence.py | save_job: 155,185,227,277,296 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/test_agent_loop.py | save_job: 717,750,760,777,801,812,825 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/test_autonomy_readiness.py | save_job: 188,210,223 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/test_brain_detail.py | save_job: 779,791,804,818,835,847,874,889,910,924 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/test_brain_smoke.py | save_job: 282,294,307,316,329,340,354,364,395,505,513,525,532,540,552,571,586,601,616,677,757,769,781,794,806 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/test_brain_viewer.py | save_job: 435,456,483,498,513,528,546,630,643,657,673,694,712,728,872 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/test_cli_main.py | save_job: 36,154,166,198,252,267,281,332,431,563,817 | load_job: 86,225,235,385,496,612,763,853,865,876,887,898,910,922,968 | load_job_safe: - | resolve_job_id: -
tests/test_cockpit.py | save_job: 583,599 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/test_context_coverage.py | save_job: 581,595,611,627,642,663,678,694,784,809,834,859,1007,1107,1115,1128,1137,1143,1162,1172,1192 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/test_data_paths.py | save_job: - | load_job: - | load_job_safe: - | resolve_job_id: 159,167,178,187,196,204
tests/test_execution_foundation.py | save_job: 60,68,76,83,90,97,106,114,122,191,199,207,216,226,242,259,274,289,303 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/test_grouped_cli.py | save_job: 180,189,197,206,269,647,663,664,675,685 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/test_memory_learn.py | save_job: 141,163,183 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/test_patch_apply.py | save_job: 1014,1028,1058,1075 | load_job: 850 | load_job_safe: - | resolve_job_id: -
tests/test_patch_intent_approval.py | save_job: 391,404,428,440,449,458,474,480,492,517,626 | load_job: 525,569,634,669 | load_job_safe: - | resolve_job_id: -
tests/test_project_brain.py | save_job: 828,841,861,891,904,916,932,968,985,1277,1287,1297,1313,1323,1333 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/test_project_constitution.py | save_job: 466,492,520,638,663,675,686 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/test_project_context_coverage.py | save_job: 646,675,700,840 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/test_run_log_cli.py | save_job: 40,247,259,272,333,434,551,639,755,889,941,1312,1385 | load_job: 867 | load_job_safe: - | resolve_job_id: -
tests/test_storage.py | save_job: 30,75,76,85,86,136,184 | load_job: 31,42,49,127,137,166,185 | load_job_safe: - | resolve_job_id: -
tests/test_timeline.py | save_job: 769 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/test_trust_report.py | save_job: 677 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/ui_contracts/test_responsive.py | save_job: 408,429,447,475 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/ui_contracts/test_ux_quality.py | save_job: 947,967,979,992,1023,1037 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/ui_server/test_command_channel.py | save_job: 74,476,518,770 | load_job: 490 | load_job_safe: - | resolve_job_id: -
tests/ui_server/test_command_dispatch.py | save_job: 76,170,215,294 | load_job: 200,221,351 | load_job_safe: - | resolve_job_id: -
tests/ui_server/test_dashboard_contract.py | save_job: 167 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/ui_server/test_decisions_endpoint.py | save_job: 37 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/ui_server/test_diff_endpoint.py | save_job: 64,278 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/ui_server/test_digest_route.py | save_job: 59 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/ui_server/test_live_state.py | save_job: 129 | load_job: - | load_job_safe: - | resolve_job_id: -
tests/ui_server/test_server_concurrency.py | save_job: 43 | load_job: - | load_job_safe: - | resolve_job_id: -
```

## 5. How this relates to `.agent/f275_t003_flip_sites.md`

THE TWO INSTRUMENTS MEASURE DIFFERENT THINGS AND NEITHER CONTAINS THE OTHER.
The round 36 enumeration lists the sites that read `Job.id` and `Job.name`, the
fields the rename touches. This file lists the sites that CALL the classic
store, which change NAME and, at `resolve_job_id`, ID SHAPE. The file sets:

- round 36 enumeration: 184 files
- this seam list: 152 files
- union: 228 files
- named by both: 108 files
- added by the seam alone: 44 files
- named by round 36 alone: 76 files

WHAT EACH IS BLIND TO, because a measurement's limits are part of its result.
The round 36 list is blind to a file that touches the classic store without
reading `.id` or `.name` — 44 files, which is why the flip cannot be planned
from that list alone. The seam list is blind to a file that reads those fields
off a job it did not load through these four functions — 76 files. Neither
sees a site that is both unexecuted and statically unprovable, and that
remainder is given NO NUMERAL here because none was measured.

THE UNION IS STILL A FLOOR. DECISION F275 D17 said of its own reading that it
is "a FLOOR on the flip's size and not a ceiling"; adding this half raises the
floor from 184 files to 228 and does not turn it into a ceiling, because the
third part of the remainder — the sites that treat a job id as a UUID rather
than as a 16-hex string — was measured only as a BOUND and a bound is recorded
as a bound.
