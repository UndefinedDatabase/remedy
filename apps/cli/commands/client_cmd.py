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
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from apps.cli.json_envelope import emit_ok, fail

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


def _client_insight_lines(raw: object) -> int:
    """`--lines`'s text as a whole number, else `job_insight.INSIGHT_LINES_DEFAULT` (DECISION
    F311 D1: "a value that is not a whole number reads 40")."""
    from packages.orchestration.job_insight import INSIGHT_LINES_DEFAULT

    try:
        return int(str(raw))
    except (TypeError, ValueError):
        return INSIGHT_LINES_DEFAULT


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
        args.job, lines=_client_insight_lines(getattr(args, "lines", None)),
        json_output=getattr(args, "json", False)),
    "client.diff": lambda args: _cmd_client_diff(
        args.job, json_output=getattr(args, "json", False)),
}
