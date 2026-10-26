"""Client group command handlers (F298 T001, DECISION F298 D2; F253 S3a, DECISION F253 D4 (3);
F253 S5a, DECISION F253 D13).

`remedy client interface` prints the machine client interface that
`apps/cli/client_interface.py` builds from the code: with `--json` as one envelope whose keys are
the document's, and otherwise as a short summary a person reads.

`remedy client changes` prints what changed since a cursor the client holds, from
`packages.orchestration.client_changes.build_client_changes`.

`remedy client order <order>` reads an order the supervisor started as a record of its own
(`packages.orchestration.serve_runs.read_order_record`): its state, its exit code and, once it is
not `running`, the answer `remedy do` printed. An order id that names no record is refused
`order_not_found`, exit 3.

`remedy client run <job>` reads the run the supervisor started for a job (F253, DECISION F253
D20), as `remedy client order` reads an order: the job's run record
(`packages.orchestration.serve_runs.read_run_record`), its `state` and, once that is not
`running`, the `answer` `remedy job run` printed. A value that names no one job, or a job with no
run record, is refused `run_not_found`, exit 3.

`remedy client story <job>` prints one job's run story
(`packages.orchestration.client_story.job_client_story`, operator amendment
amend1015-face-migration, DECISION amend1015f D14), the answer `GET /api/v1/jobs/{job}/story`
sends. The job is resolved as `remedy doctor logs` resolves it.

`remedy client now` and `remedy client insight <job>` are the twins of F311's insight
(`packages.orchestration.job_insight.now_insight` and `.job_insight`, DECISION F311 D1): what runs
now, and one job's worker seen from outside, in the closed words `remedy client interface`'s
`insight` key names.

`remedy client show [<client>]`, `remedy client grant-host-tools <client>` and `remedy client
revoke-host-tools <client>` read and change the operator's client registry (`api/clients.json`,
operator amendment amend1023-universe-trust, DECISION amend1023 D6). They are operator commands on
this machine and are never reachable over HTTP; `show` prints no token, only its fingerprint.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from apps.cli.json_envelope import emit_ok, fail
from packages.orchestration.job_insight import insight_lines

if TYPE_CHECKING:
    import argparse


def _cmd_client_interface(*, json_output: bool = False) -> None:
    from apps.cli.client_interface import build_client_interface

    interface = build_client_interface()
    if json_output:
        emit_ok(**interface)
        return
    print(f"Machine client interface {interface['interface_version']}")
    print("Operations:")
    for operation in interface["operations"]:
        print(f"  {operation['command']} — {operation['description']}")
    print(f"Job states: {', '.join(interface['job_states'])}")
    print(f"Mission statuses: {', '.join(interface['mission_statuses'])}")
    print(f"Contract templates: {', '.join(interface['contract_templates']) or '(none)'}")
    print(f"Budget kinds: {', '.join(interface['budget_kinds'])}")
    codes = ", ".join(f"{entry['code']} {entry['name']}" for entry in interface["exit_codes"])
    print(f"Exit codes: {codes}")
    print(f"Digest (remedy status --json, under client): {', '.join(interface['digest'])}")
    print("A program reads the whole interface with: remedy client interface --json")


def _cmd_client_execution(*, json_output: bool = False) -> None:
    """`remedy client execution`: `execution_options.execution_capabilities`, the answer of
    `GET /api/v1/execution` (operator order exec-1017, D6)."""
    from packages.orchestration.execution_options import execution_capabilities

    capabilities = execution_capabilities()
    if json_output:
        emit_ok(**capabilities)
        return
    for role, offer in capabilities["roles"].items():
        shown = ", ".join(f"{p['id']}{'' if p['available'] else ' (not available)'}"
                          f"{'' if p['offered_over_http'] else ' (command line only)'}" for p in offer["providers"])
        print(f"{role}: default {offer['default_provider']} {offer['default_model']}".rstrip() + f"; {shown}")
    print(f"Lanes: {', '.join(capabilities['lanes'])}; order flags: {', '.join(capabilities['order_flags'])}")
    print("A program reads all of it with: remedy client execution --json")


def _cmd_client_changes(*, since: str | None, json_output: bool = False) -> None:
    from packages.orchestration.client_changes import (
        build_client_changes,
        client_cursor_refusal_message,
        parse_client_cursor,
    )

    parsed_since = None
    if since is not None:
        try:
            parsed_since = parse_client_cursor(since)
        except ValueError:
            fail(
                "invalid_cursor",
                client_cursor_refusal_message(since),
                json_output=json_output, exit_code=2,
            )

    changes = build_client_changes(parsed_since)
    if json_output:
        emit_ok(**changes)
        return
    print(f"Jobs changed: {len(changes['jobs'])}")
    print(f"Decisions open: {len(changes['decisions'])}")
    print(f"Decisions closed: {len(changes['closed_decisions'])}")
    print(f"Missions changed: {len(changes['missions'])}")
    print(f"Applies changed: {len(changes['applies'])}")
    print(f"Next cursor: {changes['cursor']}")


def _cmd_client_order(order_id: str, *, json_output: bool = False) -> None:
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import (
        order_not_found_message,
        order_record_payload,
        read_order_record,
    )

    paths = serve_paths()
    record = read_order_record(paths, order_id)
    if record is None:
        fail(
            "order_not_found",
            order_not_found_message(order_id),
            json_output=json_output, exit_code=3,
        )
    # `order_record_payload` is a call, not a dict literal, so it is unresolved to
    # tests/cli/test_client_interface.py's static answer-key reader by construction; the site is
    # hand-verified there (`apps.cli.commands.client_cmd:_cmd_client_order:**payload`).
    payload = order_record_payload(paths, record)
    if json_output:
        emit_ok(**payload)
        return
    print(f"Order {record.order_id}: {payload['state']}")


def _cmd_client_run(job: str, *, json_output: bool = False) -> None:
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import (
        run_not_found_message,
        run_record_for_job_value,
        run_record_payload,
    )

    paths = serve_paths()
    # The job's id is read where `GET /api/v1/jobs/{job}/run` reads it (R-1224).
    record = run_record_for_job_value(paths, job)
    if record is None:
        fail(
            "run_not_found",
            run_not_found_message(job),
            json_output=json_output, exit_code=3,
        )
    # As `_cmd_client_order`: a call, hand-verified in tests/cli/test_client_interface.py
    # (`apps.cli.commands.client_cmd:_cmd_client_run:**payload`).
    payload = run_record_payload(paths, record)
    if json_output:
        emit_ok(**payload)
        return
    print(f"Run of job {record.job_id}: {payload['state']}")


def _cmd_client_story(job: str, *, json_output: bool = False) -> None:
    from apps.cli.job_id_arg import resolve_job_id_or_fail
    from packages.orchestration.client_story import job_client_story
    from packages.orchestration.pingpong_job import JobNotFoundError, require_job_plan

    job_id = resolve_job_id_or_fail(job, json_output=json_output)
    try:
        plan = require_job_plan(job_id)
    except JobNotFoundError as exc:
        fail("job_not_found", str(exc), json_output=json_output)
    # A call, hand-verified in tests/cli/test_client_interface.py
    # (`apps.cli.commands.client_cmd:_cmd_client_story:**story`).
    story = job_client_story(job_id, plan)
    if json_output:
        emit_ok(**story)
        return
    print(f"Job {job_id}: {story['state']}, next {story['next']['action']}")


def _cmd_client_now(*, json_output: bool = False) -> None:
    from packages.orchestration.job_insight import now_insight

    # A call, hand-verified in tests/cli/test_client_interface.py
    # (`apps.cli.commands.client_cmd:_cmd_client_now:**answer`).
    answer = now_insight()
    if json_output:
        emit_ok(**answer)
        return
    print(f"{len(answer['jobs'])} job(s) running, {len(answer['orders'])} order(s) waiting, "
         f"model server {answer['model_server']['state']}")


def _cmd_client_insight(job: str, *, lines: int, json_output: bool = False) -> None:
    from apps.cli.job_id_arg import resolve_job_id_or_fail
    from packages.orchestration.job_insight import job_insight
    from packages.orchestration.pingpong_job import JobNotFoundError, require_job_plan

    job_id = resolve_job_id_or_fail(job, json_output=json_output)
    try:
        plan = require_job_plan(job_id)
    except JobNotFoundError as exc:
        fail("job_not_found", str(exc), json_output=json_output)
    # A call, hand-verified in tests/cli/test_client_interface.py
    # (`apps.cli.commands.client_cmd:_cmd_client_insight:**answer`).
    answer = job_insight(plan, lines=lines)
    if json_output:
        emit_ok(**answer)
        return
    print(f"Job {job_id}: {answer['phase']}, "
         f"{'stalled (' + answer['stall_reason'] + ')' if answer['stalled'] else 'not stalled'}, "
         f"advice: {', '.join(answer['advice'])}")


def _cmd_client_diff(job: str, *, json_output: bool = False) -> None:
    from apps.cli.job_id_arg import resolve_job_id_or_fail
    from packages.orchestration.client_diff import ClientDiffRefusal, job_client_diff
    from packages.orchestration.pingpong_job import JobNotFoundError, require_job_plan

    job_id = resolve_job_id_or_fail(job, json_output=json_output)
    try:
        plan = require_job_plan(job_id)
    except JobNotFoundError as exc:
        fail("job_not_found", str(exc), json_output=json_output)
    try:
        # A call, hand-verified in tests/cli/test_client_interface.py
        # (`apps.cli.commands.client_cmd:_cmd_client_diff:**answer`).
        answer = job_client_diff(job_id, plan)
    except ClientDiffRefusal as exc:
        fail(exc.token, str(exc), json_output=json_output, exit_code=3)
    if json_output:
        emit_ok(**answer)
        return
    print(f"Job {job_id}: {answer['state']}")
    for row in answer["files"]:
        print(f"  {row['change']:<8} +{row['added']} -{row['removed']} {row['path']}")
    for row in answer["files"]:
        print(row["patch"], end="")


def _cmd_client_order_story(order_id: str, *, json_output: bool = False) -> None:
    """`remedy client order-story <order>`: the order's story, the answer `GET /api/v1/orders/{order}/story`
    sends (DECISION amend1023 D11)."""
    from packages.orchestration.order_story import order_story_answer

    answer = order_story_answer(order=order_id)
    if not answer["ok"]:
        fail(answer["error"], answer["message"], json_output=json_output, exit_code=3)
    story = {key: value for key, value in answer.items() if key not in ("ok", "schema_version")}
    if json_output:
        emit_ok(**story)
        return
    print(f"Order {story['order_id']}: {story['phase']}")
    for mission in story["missions"]:
        for milestone in mission["milestones"]:
            for job in milestone["jobs"]:
                print(f"  {job['number']}. {job['state']} {job['tasks']['done']}/{job['tasks']['total']} {job['title']}")


def _cmd_client_order_review(order_id: str, *, json_output: bool = False) -> None:
    """`remedy client order-review <order>`: the order's review report as Markdown, the answer
    `GET /api/v1/orders/{order}/review` sends (amend1026 D3)."""
    from packages.orchestration.order_review import order_review_answer

    answer = order_review_answer(order=order_id)
    if not answer["ok"]:
        fail(answer["error"], answer["message"], json_output=json_output, exit_code=3)
    review = {key: value for key, value in answer.items() if key not in ("ok", "schema_version")}
    if json_output:
        emit_ok(**review)
        return
    print(review["markdown"], end="")


def _cmd_client_projects(*, json_output: bool = False) -> None:
    """`remedy client projects`: every registered project, the answer `GET /api/v1/projects` sends the
    server's own token; a client token's answer holds only its own projects (amend1026 C1)."""
    from packages.orchestration.client_projects import client_projects

    listing = client_projects()
    if json_output:
        emit_ok(**listing)
        return
    for project in listing["projects"]:
        test = project["last_test"]["status"] if project["last_test"] else "none"
        print(f"{project['slug']}: {project['open_jobs']} open, last job {project['last_job_at'] or 'none'}, "
              f"last test {test} — {project['repo_path'] or '(no repository)'}")


def _client_entry(client: Any) -> dict[str, Any]:
    """One client as `remedy client show` answers it: its policy and its token's fingerprint, never the token."""
    from packages.orchestration.serve_http_handler import token_fingerprint

    return {"name": client.name, "projects": list(client.projects),
            "max_total_tokens": client.max_total_tokens, "max_provider_calls": client.max_provider_calls,
            "may_apply": client.may_apply, "host_tools": client.host_tools,
            "token_fp": token_fingerprint(client.token)}


def _cmd_client_show(name: str | None, *, json_output: bool = False) -> None:
    """`remedy client show [<client>]`: every client of the registry, or the one NAME names."""
    from packages.orchestration.api_clients import api_clients_path, load_api_clients

    clients = [client for client in load_api_clients() if name is None or client.name == name]
    if name is not None and not clients:
        fail("client_not_found", f"no client named {name!r} in {api_clients_path()}",
             json_output=json_output, exit_code=3)
    entries = [_client_entry(client) for client in clients]
    if json_output:
        emit_ok(clients=entries)
        return
    if not entries:
        print(f"No client in {api_clients_path()}.")
    for entry in entries:
        print(f"{entry['name']}: projects {', '.join(entry['projects']) or '(none)'}; "
              f"may_apply {str(entry['may_apply']).lower()}; host_tools {str(entry['host_tools']).lower()}; "
              f"token {entry['token_fp']}")


def _cmd_client_host_tools(name: str, *, granted: bool, json_output: bool = False) -> None:
    """`remedy client grant-host-tools` and `revoke-host-tools` (DECISION amend1023 D6)."""
    from packages.orchestration.api_clients import ApiClientRegistryError, set_client_host_tools

    try:
        client = set_client_host_tools(name, granted)
    except ApiClientRegistryError as exc:
        fail(exc.error, str(exc), json_output=json_output,
             exit_code=3 if exc.error == "client_not_found" else 1)
    except OSError as exc:
        fail("client_registry_unwritable", f"the client registry could not be written: {exc}; nothing was changed",
             json_output=json_output)
    entry = _client_entry(client)
    if json_output:
        emit_ok(client=entry)
        return
    print(f"{entry['name']}: host_tools {str(entry['host_tools']).lower()}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "client.interface": lambda args: _cmd_client_interface(json_output=getattr(args, "json", False)),
    "client.execution": lambda args: _cmd_client_execution(json_output=getattr(args, "json", False)),
    "client.changes": lambda args: _cmd_client_changes(
        since=getattr(args, "since", None), json_output=getattr(args, "json", False)),
    "client.order": lambda args: _cmd_client_order(
        args.order, json_output=getattr(args, "json", False)),
    "client.run": lambda args: _cmd_client_run(
        args.job, json_output=getattr(args, "json", False)),
    "client.story": lambda args: _cmd_client_story(
        args.job, json_output=getattr(args, "json", False)),
    "client.now": lambda args: _cmd_client_now(json_output=getattr(args, "json", False)),
    "client.insight": lambda args: _cmd_client_insight(
        args.job, lines=insight_lines(getattr(args, "lines", None)),
        json_output=getattr(args, "json", False)),
    "client.diff": lambda args: _cmd_client_diff(
        args.job, json_output=getattr(args, "json", False)),
    "client.order-story": lambda args: _cmd_client_order_story(
        args.order, json_output=getattr(args, "json", False)),
    "client.order-review": lambda args: _cmd_client_order_review(
        args.order, json_output=getattr(args, "json", False)),
    "client.projects": lambda args: _cmd_client_projects(json_output=getattr(args, "json", False)),
    "client.show": lambda args: _cmd_client_show(
        getattr(args, "client", None), json_output=getattr(args, "json", False)),
    "client.grant-host-tools": lambda args: _cmd_client_host_tools(
        args.client, granted=True, json_output=getattr(args, "json", False)),
    "client.revoke-host-tools": lambda args: _cmd_client_host_tools(
        args.client, granted=False, json_output=getattr(args, "json", False)),
}
