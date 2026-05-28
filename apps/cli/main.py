"""
Remedy CLI entrypoint — bridge to grouped CLI.

This module serves as the backward-compatible entry point. It delegates
all group commands and help rendering to the grouped CLI (apps.cli.grouped).
Old flat commands (create-job, list-jobs, etc.) are preserved for backward
compatibility and dispatch to the same handler functions in apps.cli.commands.
"""

from __future__ import annotations

import argparse
import sys

# Backward-compatible re-exports: tests and other code import _cmd_* from here.
# The actual implementations live in apps.cli.commands.* modules.
from apps.cli.commands.job import (  # noqa: F401
    _cmd_attach_repo,
    _cmd_create_job,
    _cmd_list_jobs,
    _cmd_plan_job_local,
    _cmd_run_next_task_local,
    _cmd_set_permission,
    _cmd_show_job,
    _cmd_show_permissions,
)
from apps.cli.commands.brain import (  # noqa: F401
    _cmd_agent_loop,
    _cmd_brain,
    _cmd_brain_node,
    _cmd_brain_view,
    _cmd_cockpit,
    _cmd_constitution,
    _cmd_context,
    _cmd_timeline,
    _cmd_trust_report,
)
from apps.cli.commands.patch import (  # noqa: F401
    _cmd_apply_patch_intent,
    _cmd_approve_patch_intent,
    _cmd_list_patch_intents,
    _cmd_reject_patch_intent,
    _cmd_show_patch_intent,
)
from apps.cli.commands.test_cmds import (  # noqa: F401
    _cmd_discover_commands,
    _cmd_run_tests_local,
)
from apps.cli.commands.project import (  # noqa: F401
    _cmd_attach_project_job,
    _cmd_attach_project_repo,
    _cmd_create_project,
    _cmd_list_projects,
    _cmd_project_context,
    _cmd_show_project,
)
from apps.cli.commands.policy import (  # noqa: F401
    _cmd_run_contract,
    _cmd_token_policy,
)
from apps.cli.commands.worker import _cmd_workers  # noqa: F401


def main() -> None:
    from apps.cli.command_catalog import GROUPS, get_commands_for_group

    # No args or --help -> show grouped root help
    if len(sys.argv) <= 1 or sys.argv[1] in ("-h", "--help"):
        from apps.cli.grouped import main as grouped_main
        grouped_main(sys.argv[1:])
        return

    first = sys.argv[1]
    if first in GROUPS:
        subcmds = {c.subcommand for c in get_commands_for_group(first)}
        if len(sys.argv) <= 2 or sys.argv[2] in subcmds or sys.argv[2].startswith("-"):
            from apps.cli.grouped import main as grouped_main
            grouped_main(sys.argv[1:])
            return

    # Old flat command parser for backward compatibility
    parser = argparse.ArgumentParser(prog="remedy", description="Remedy orchestration CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create-job", help="Create and persist a new job")
    create.add_argument("prompt", help="User prompt describing the job")
    create.add_argument("--project", default=None, help="Project UUID to attach the job to")
    create.add_argument("--task-type", default=None, dest="task_type")
    create.add_argument("--task-description", default=None, dest="task_description")

    subparsers.add_parser("list-jobs", help="List all persisted jobs")

    show = subparsers.add_parser("show-job", help="Print full JSON for a job")
    show.add_argument("job_id")

    plan_local = subparsers.add_parser("plan-job-local", help="Plan a job using local Ollama")
    plan_local.add_argument("job_id")

    plan = subparsers.add_parser("plan-job", help="Generate planning skeleton for a job")
    plan.add_argument("job_id")

    attach = subparsers.add_parser("attach-repo", help="Attach a repository to a job")
    attach.add_argument("job_id")
    attach.add_argument("repo_path")

    perm = subparsers.add_parser("set-permission", help="Grant or deny a permission")
    perm.add_argument("job_id")
    perm.add_argument("action", choices=["allow", "deny"])
    perm.add_argument("capability")

    show_perms = subparsers.add_parser("show-permissions", help="Show permissions")
    show_perms.add_argument("job_id")

    run_task = subparsers.add_parser("run-next-task-local", help="Execute the next pending task")
    run_task.add_argument("job_id")

    run_tests = subparsers.add_parser("run-tests-local", help="Run tests")
    run_tests.add_argument("job_id")

    discover_cmds = subparsers.add_parser("discover-commands", help="Discover commands")
    discover_cmds.add_argument("job_id")
    discover_cmds.add_argument("--json", action="store_true", default=False)

    brain_node_p = subparsers.add_parser("brain-node", help="Brain node detail")
    brain_node_p.add_argument("job_id")
    brain_node_p.add_argument("node_id")
    brain_node_p.add_argument("--json", action="store_true", default=False)

    context_p = subparsers.add_parser("context", help="Context coverage")
    context_p.add_argument("job_id")
    context_p.add_argument("--json", action="store_true", default=False)

    brain_view_p = subparsers.add_parser("brain-view", help="Brain viewer")
    brain_view_p.add_argument("job_id")

    brain_p = subparsers.add_parser("brain", help="Brain graph")
    brain_p.add_argument("job_id")
    brain_p.add_argument("--json", action="store_true", default=False)

    agent_loop_p = subparsers.add_parser("agent-loop", help="Agent loop state")
    agent_loop_p.add_argument("job_id")

    constitution_p = subparsers.add_parser("constitution", help="Project constitution")
    constitution_p.add_argument("job_id")

    trust_report = subparsers.add_parser("trust-report", help="Trust report")
    trust_report.add_argument("job_id")

    timeline = subparsers.add_parser("timeline", help="Event timeline")
    timeline.add_argument("job_id")

    cockpit = subparsers.add_parser("cockpit", help="Cockpit summary")
    cockpit.add_argument("job_id")

    list_pi = subparsers.add_parser("list-patch-intents", help="List patch intents")
    list_pi.add_argument("job_id")

    show_pi = subparsers.add_parser("show-patch-intent", help="Show patch intent")
    show_pi.add_argument("job_id")
    show_pi.add_argument("intent_id")

    approve_pi = subparsers.add_parser("approve-patch-intent", help="Approve patch intent")
    approve_pi.add_argument("job_id")
    approve_pi.add_argument("intent_id")
    approve_pi.add_argument("--reason", default=None)

    apply_pi = subparsers.add_parser("apply-patch-intent", help="Apply patch intent")
    apply_pi.add_argument("job_id")
    apply_pi.add_argument("intent_id")
    apply_pi.add_argument("--json", action="store_true", dest="json")

    reject_pi = subparsers.add_parser("reject-patch-intent", help="Reject patch intent")
    reject_pi.add_argument("job_id")
    reject_pi.add_argument("intent_id")
    reject_pi.add_argument("--reason", default=None)

    create_project = subparsers.add_parser("create-project", help="Create a project")
    create_project.add_argument("name")
    create_project.add_argument("--description", default=None)

    subparsers.add_parser("list-projects", help="List projects")

    attach_proj_repo = subparsers.add_parser("attach-project-repo", help="Attach repo to project")
    attach_proj_repo.add_argument("project_id")
    attach_proj_repo.add_argument("repo_path")

    attach_proj_job = subparsers.add_parser("attach-project-job", help="Link job to project")
    attach_proj_job.add_argument("project_id")
    attach_proj_job.add_argument("job_id")

    show_project = subparsers.add_parser("show-project", help="Show project")
    show_project.add_argument("project_id")
    show_project.add_argument("--json", action="store_true", dest="json")

    project_alias = subparsers.add_parser("project", help="Show project (alias)")
    project_alias.add_argument("project_id")
    project_alias.add_argument("--json", action="store_true", dest="json")

    project_ctx_p = subparsers.add_parser("project-context", help="Project context coverage")
    project_ctx_p.add_argument("project_id")
    project_ctx_p.add_argument("--json", action="store_true", dest="json")

    run_contract_p = subparsers.add_parser("run-contract", help="Run contract")
    run_contract_p.add_argument("job_id")
    run_contract_p.add_argument("--json", action="store_true", dest="json")

    token_policy_p = subparsers.add_parser("token-policy", help="Token policy")
    token_policy_p.add_argument("job_id")
    token_policy_p.add_argument("--json", action="store_true", dest="json")

    workers_p = subparsers.add_parser("workers", help="List workers")
    workers_p.add_argument("--json", action="store_true", dest="json")

    args = parser.parse_args()
    cmd = args.command
    if cmd == "create-job":
        _cmd_create_job(args.prompt, project_id=getattr(args, "project", None),
                        task_type=getattr(args, "task_type", None),
                        task_description=getattr(args, "task_description", None))
    elif cmd == "list-jobs":
        _cmd_list_jobs()
    elif cmd == "show-job":
        _cmd_show_job(args.job_id)
    elif cmd == "plan-job":
        from packages.orchestration.job_runner import plan_job
        from packages.orchestration.storage import load_job, save_job, JobNotFoundError
        from uuid import UUID
        try:
            job = load_job(UUID(args.job_id))
        except (ValueError, JobNotFoundError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
        result = plan_job(job)
        save_job(result.job)
        if not result.changed:
            print(f"Job {result.job.id} already planned — no changes made.")
        else:
            print(f"Job {result.job.id} planned: {len(result.job.tasks)} task(s), {len(result.job.artifacts)} artifact(s)")
    elif cmd == "plan-job-local":
        _cmd_plan_job_local(args.job_id)
    elif cmd == "attach-repo":
        _cmd_attach_repo(args.job_id, args.repo_path)
    elif cmd == "set-permission":
        _cmd_set_permission(args.job_id, args.action, args.capability)
    elif cmd == "show-permissions":
        _cmd_show_permissions(args.job_id)
    elif cmd == "run-next-task-local":
        _cmd_run_next_task_local(args.job_id)
    elif cmd == "run-tests-local":
        _cmd_run_tests_local(args.job_id)
    elif cmd == "discover-commands":
        _cmd_discover_commands(args.job_id, as_json=args.json)
    elif cmd == "brain-node":
        _cmd_brain_node(args.job_id, args.node_id, json_output=args.json)
    elif cmd == "brain":
        _cmd_brain(args.job_id, json_output=args.json)
    elif cmd == "context":
        _cmd_context(args.job_id, json_output=args.json)
    elif cmd == "brain-view":
        _cmd_brain_view(args.job_id)
    elif cmd == "agent-loop":
        _cmd_agent_loop(args.job_id)
    elif cmd == "constitution":
        _cmd_constitution(args.job_id)
    elif cmd == "trust-report":
        _cmd_trust_report(args.job_id)
    elif cmd == "timeline":
        _cmd_timeline(args.job_id)
    elif cmd == "cockpit":
        _cmd_cockpit(args.job_id)
    elif cmd == "list-patch-intents":
        _cmd_list_patch_intents(args.job_id)
    elif cmd == "show-patch-intent":
        _cmd_show_patch_intent(args.job_id, args.intent_id)
    elif cmd == "approve-patch-intent":
        _cmd_approve_patch_intent(args.job_id, args.intent_id, args.reason)
    elif cmd == "reject-patch-intent":
        _cmd_reject_patch_intent(args.job_id, args.intent_id, args.reason)
    elif cmd == "apply-patch-intent":
        _cmd_apply_patch_intent(args.job_id, args.intent_id, json_output=args.json)
    elif cmd == "create-project":
        _cmd_create_project(args.name, args.description)
    elif cmd == "list-projects":
        _cmd_list_projects()
    elif cmd == "attach-project-repo":
        _cmd_attach_project_repo(args.project_id, args.repo_path)
    elif cmd == "attach-project-job":
        _cmd_attach_project_job(args.project_id, args.job_id)
    elif cmd in ("show-project", "project"):
        _cmd_show_project(args.project_id, json_output=args.json)
    elif cmd == "project-context":
        _cmd_project_context(args.project_id, json_output=args.json)
    elif cmd == "run-contract":
        _cmd_run_contract(args.job_id, json_output=args.json)
    elif cmd == "token-policy":
        _cmd_token_policy(args.job_id, json_output=args.json)
    elif cmd == "workers":
        _cmd_workers(json_output=args.json)


if __name__ == "__main__":
    main()
