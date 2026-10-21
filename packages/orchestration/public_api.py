"""The public HTTP API's routes, its version and what it never publishes (F253, DECISION F253 D1).

A route under `PUBLIC_API_PREFIX` answers exactly what its twin command answers with `--json`: the
same envelope `apps/cli/json_envelope.py` builds, read from `PUBLIC_API_ROUTES` at call time so a
test can replace the registry and see the handler follow it. A route's path may carry named
segments, written `{name}`, each matching exactly one non-empty path segment and passed to the
twin's function as a keyword argument of that name; a route also declares, in `refusals`, the HTTP
status of each refusal it shares with its twin (DECISION F253 D3). The version rule: the major
number is in the path; inside `/api/v1` a route, an answer key or a refusal token is only ever
added, and each addition raises the minor number of `PUBLIC_API_VERSION`; a route that is to go is
first marked `deprecated`, which makes it answer the header `Deprecation: true` and shows it in the
page's table, and it is removed only under a new major path.

Every request under this namespace, a refused one included, appends one line to the data root's
`api/calls.jsonl` (DECISION F253 D2 (1)): the caller's token kept only as its DECISION F009 D7
fingerprint, the name of the client whose token it was (DECISION F253 D16), never the query string,
and a line that cannot be written changes nothing in the
answer sent. A route may answer one key of its twin's answer alone (`twin_key`) and takes only
the query keys it declares: each of `query` a `true`/`false` flag, each of `query_values` one
non-empty value given once; anything else answers 400 `api_query_invalid` (DECISION F253 D2 (2),
D5 (1)).

A `POST` route is a write (DECISION F253 D9): it declares the keys of its JSON body in `body` and
a `refusal_default` status, and `answer_public_api_post` answers it with the envelope of the twin
command, which the caller's runner has run as a child process. A route's argument builder may
refuse a write itself, before any command runs, by raising `PublicApiWriteRefusal` (DECISION F253
D12). A client token (DECISION F253 D16) is read from `api/clients.json` by
`packages.orchestration.api_clients`: with one, `answer_public_api_post` refuses an order outside
the client's projects or ceilings and an apply the client may not approve with 403
`api_client_policy_refused`.

`GET /api/v1/orders/{order}` (DECISION F253 D14 (4)) answers an order exactly as `remedy client
order <order> --json` does: the two share one answer-builder, `order_record_payload` in
`packages.orchestration.serve_runs`.

`POST /api/v1/jobs/{job}/run` (DECISION F253 D18) starts a job's run through the supervisor's own
`RunLauncher` and answers 202 with the run's record; its body names the builder and the reviewer
provider and no other option of `remedy job run` is offered. `GET /api/v1/jobs/{job}/run`
(DECISION F253 D20) answers that record as `remedy client run <job> --json` does, with `state` and,
once the run is not `running`, `answer`, and the 202 answer holds the same keys: the two share
`run_record_payload` in `packages.orchestration.serve_runs`.

`GET /api/v1/jobs/{job}/story` (DECISION amend1015f D14) answers one job's run story as `remedy
client story <job> --json` does: the two share `job_client_story` in
`packages.orchestration.client_story`, and a client token reads only a job of its projects.

`render_public_api_markdown` renders the generated section of `docs/system/public-http-api-v1.md`,
and `write_public_api_page` writes it there; a test holds that section equal to the rendering.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote

# DECISION F199 D3: the route table, its dataclass and its registry, lives in a module of its
# own; this module imports the names it uses from it.
from packages.orchestration.public_api_routes import PUBLIC_API_ROUTES, PublicApiRoute

# DECISION F205 D6: the write routes' argument builders and refusals live in a module of
# their own; this module imports the names it uses, and every other consumer imports from it
# (operator amendment amend1014-luna-mission-fixes D.2).
from packages.orchestration.public_api_writes import (
    _TWIN_ARGV,
    PublicApiWriteRefusal,
    _client_write_refusal,
    _order_text_and_options,
    _write_lock_key,
)

#: The path prefix every route under this registry lives below; the major version is in the path.
PUBLIC_API_PREFIX = "/api/v1"

#: This registry's own version. The minor number rises whenever a route, an answer key or a
#: refusal token is added; the major number changes only under a new path prefix. Operator
#: amendment amend1015-face-migration (DECISION amend1015f D14) raises it to `1.15` for
#: `GET /api/v1/jobs/{job}/story`, and operator order amend1015-final-closure to `1.16` for the
#: client token's refusal `api_client_policy_refused` on the proof, run and order polls
#: (DECISION amend1015c D2) and for `GET /api/v1/jobs/{job}/diff` (DECISION amend1015c D5), and
#: order exec-1017 to `1.17` for the story's `verification` and `numbers.model_turns`, and order
#: exec-1017b to `1.18` for `POST /api/v1/jobs/{job}/stop` and an order's `jobs`, and order exec-1017c
#: to `1.19` for `POST /api/v1/jobs/{job}/abandon`, `POST /api/v1/orders/{order}/cancel` and an
#: order's `phase` and `cancel`, and order exec-1018 to `1.20` for the story reasons
#: `sandbox_unavailable` and `project_rules_too_large`, an order job's phase `checked`, and a cancel
#: that ends a planner call in flight, and order exec-1018b to `1.21` for the story's `end`, and
#: F313 (DECISION F313 D1) to `1.22` for `GET /api/v1/now`, `GET /api/v1/jobs/{job}/insight` and
#: the decision route's `resumed` and `resume_refused` after an `extend`, and F078 (DECISION F078 D6)
#: to `1.23` for the interface's status answer `autonomy`, with no change over HTTP, and F141
#: (DECISION F141 D7) to `1.24` for `autonomy`'s `push_allowed` and `permissions`, with none either,
#: and F303 (DECISION F303 D3) to `1.25` for `POST /api/v1/jobs/{job}/note`, and F307
#: (DECISION F307 D11) to `1.26` for an order's `repo_path`, with no change over HTTP.
PUBLIC_API_VERSION = "1.26"

#: The feature file's initial exclusion list, in its order. These operator-console commands change
#: or recover this machine, its configuration or its queue, and are never reachable over this API.
#: Tighten-only: this list may only grow, and only under its own operator decision.
PUBLIC_API_EXCLUDED_COMMANDS: tuple[str, ...] = (
    "patch.apply",
    "patch.revert",
    "rollback.*",
    "snapshot.create",
    "config.set",
    "config.init",
    "init.run",
    "self-repair.proposal-approve",
    "self-repair.proposal-deny",
    "worker.unload",
    "runtime.stop",
    "ui.stop",
    "queue.rm",
    "queue.reclaim",
)


def command_is_excluded(command_id: str) -> bool:
    """True when `command_id` is never published: an exact entry, or under a `prefix.*` entry."""
    for entry in PUBLIC_API_EXCLUDED_COMMANDS:
        if entry.endswith(".*"):
            if command_id.startswith(entry[:-1]):
                return True
        elif command_id == entry:
            return True
    return False


def is_public_api_path(path: str) -> bool:
    """True when `path` is this namespace's own: `PUBLIC_API_PREFIX` itself or anything under it."""
    return path == PUBLIC_API_PREFIX or path.startswith(PUBLIC_API_PREFIX + "/")


def _match_route_path(template: str, path: str) -> dict[str, str] | None:
    """Bind `template`'s `{name}` segments against `path`, or None when they do not match.

    Both split on `/`; the same number of segments is required. A template segment written
    `{name}` matches exactly one non-empty path segment and binds it under `name`, percent-decoded,
    so that a decision id a client sends as `td%3A...` arrives as `td:...` (R-1192); every other
    segment must be equal (DECISION F253 D3 (1)).
    """
    template_parts = template.split("/")
    path_parts = path.split("/")
    if len(template_parts) != len(path_parts):
        return None
    bound: dict[str, str] = {}
    for template_part, path_part in zip(template_parts, path_parts):
        if template_part.startswith("{") and template_part.endswith("}"):
            if not path_part:
                return None
            bound[template_part[1:-1]] = unquote(path_part)
        elif template_part != path_part:
            return None
    return bound


def public_api_token_refusal() -> tuple[int, dict[str, Any]]:
    """The 401 a caller gets for a missing or wrong bearer token; it names the server's token and
    a client token as the two the route takes (DECISION F253 D16)."""
    from apps.cli.json_envelope import build_error

    return 401, build_error(
        "api_token_invalid",
        "this route needs the server's token or a client token as "
        "'Authorization: Bearer <token>'",
    )


def public_api_method_refusal() -> tuple[int, dict[str, Any]]:
    """The 405 a caller gets for a method this server does not answer under this namespace."""
    from apps.cli.json_envelope import build_error

    return 405, build_error(
        "api_method_not_allowed",
        "this server answers only GET under /api/v1; writes are answered by the supervisor "
        "that `remedy serve start` starts",
    )


def _client_interface_answer() -> dict[str, Any]:
    """The answer `GET /api/v1/interface` sends: `client.interface`'s own `--json` answer."""
    from apps.cli.client_interface import build_client_interface
    from apps.cli.json_envelope import build_ok

    return build_ok(**build_client_interface())


def _client_execution_answer() -> dict[str, Any]:
    """The answer `GET /api/v1/execution` sends: `remedy client execution --json` (exec-1017 D6)."""
    from apps.cli.json_envelope import build_ok
    from packages.orchestration.execution_options import execution_capabilities

    return build_ok(**execution_capabilities())


def _status_digest_answer(*, all_ended_jobs: bool = False,
                          project_ids: frozenset[str] | None = None) -> dict[str, Any]:
    """The answer `GET /api/v1/digest` sends: the `client` key of `status.run`'s `--json` answer.

    Calls `build_client_digest` directly rather than the whole `status.run` command: the digest
    reads the data root alone, while the rest of that command's answer depends on the directory
    the server happens to run in (DECISION F253 D2 (3)).
    """
    from apps.cli.json_envelope import build_ok
    from packages.orchestration.client_digest import build_client_digest

    return build_ok(**build_client_digest(every_ended_job=all_ended_jobs, project_ids=project_ids))


def _resolved_job_plan(job: str) -> tuple[tuple[str, Any] | None, dict[str, Any] | None]:
    """((the job id, its plan), None), or (None, the refusal) for a value that names no one job: the
    resolution and the messages of `resolve_job_id_or_fail` and `require_job_plan`, which a route
    must not call because both exit or raise. Shared by the proof and the logs routes."""
    from apps.cli.json_envelope import build_error
    from packages.orchestration.data_paths import JobIdAmbiguous, JobIdError, lookup_job_id
    from packages.orchestration.pingpong_job import JobNotFoundError, require_job_plan

    try:
        job_id = lookup_job_id(job)
    except JobIdAmbiguous as exc:
        matches = exc.matches
        listed = "\n".join(f"  {m[:8]}" for m in matches)
        return None, build_error(
            "ambiguous_job_id",
            f"ambiguous job id prefix '{job}' matches {len(matches)} jobs:\n{listed}",
            matches=matches,
        )
    except JobIdError:
        return None, build_error(
            "invalid_job_id", f"No job matches {job!r}. Try: remedy job list.")
    try:
        return (job_id, require_job_plan(job_id)), None
    except JobNotFoundError as exc:
        return None, build_error("job_not_found", str(exc))


def _change_proof_answer(*, job: str) -> dict[str, Any]:
    """The answer `GET /api/v1/jobs/{job}/proof` sends: what `change.proof --json` prints with no
    `--path` (DECISION F253 D3 (3)).

    Reproduces `apps.cli.commands.change._cmd_change_proof`'s own resolution, refusal messages
    included, rather than calling `apps.cli.job_id_arg.resolve_job_id_or_fail` or `fail()`
    directly: both exit the process, which a route handler must never do. The messages below are
    therefore held equal to the command's by test, not shared by import.
    """
    from apps.cli.json_envelope import build_ok
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.proof_chain import build_proof_chain, export_proof_chain_json
    from packages.orchestration.timeline import load_run_events

    resolved, refusal = _resolved_job_plan(job)
    if resolved is None:
        return refusal or {}
    job_id, plan = resolved
    data_dir = resolve_data_root()
    chain = build_proof_chain(plan, load_run_events(data_dir, job_id), path=None, data_dir=data_dir)
    return build_ok(**export_proof_chain_json(chain))


def _client_changes_answer(*, since: str | None = None,
                           project_ids: frozenset[str] | None = None) -> dict[str, Any]:
    """The answer `GET /api/v1/changes` sends: what `client changes --json` prints (DECISION
    F253 D5 (2)). Calls the same two functions its twin calls, and refuses an unreadable cursor
    with its twin's own message."""
    from apps.cli.json_envelope import build_error, build_ok
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
            return build_error("invalid_cursor", client_cursor_refusal_message(since))

    return build_ok(**build_client_changes(parsed_since, project_ids=project_ids))


def _doctor_health_answer() -> dict[str, Any]:
    """The answer `GET /api/v1/health` sends: what `doctor.health --json` prints (DECISION
    F199 D1). Runs the eight checks once; a FAIL among them is the `health_failed` refusal with
    the same document, which the route answers with HTTP 503."""
    from apps.cli.json_envelope import build_error, build_ok
    from packages.orchestration.self_health import (
        health_exit_code,
        health_failure_message,
        health_report_document,
        run_health_checks,
    )

    results = run_health_checks()
    if health_exit_code(results) == 1:
        return build_error(
            "health_failed", health_failure_message(results), **health_report_document(results),
        )
    return build_ok(**health_report_document(results))


def _doctor_logs_answer(*, job: str, run: str | None = None) -> dict[str, Any]:
    """The answer `GET /api/v1/jobs/{job}/logs` sends: what `doctor.logs --json` prints (DECISION
    F203 D5). Reads the operations log's lines of the job, oldest first, kept to one run when
    `run` is given; a job with no line answers an empty `entries`. The job is resolved as its
    twin resolves it, and only the resolved job's lines are read (operator amendment
    amend1014-luna-mission-fixes B.3)."""
    from apps.cli.json_envelope import build_ok
    from packages.orchestration.structured_log import read_log_entries

    resolved, refusal = _resolved_job_plan(job)
    if resolved is None:
        return refusal or {}
    job_id, _plan = resolved
    result = read_log_entries(job_id=job_id, run_id=run)
    return build_ok(
        job_id=job_id,
        run_id=run,
        entries=list(result.entries),
        unreadable=result.unreadable,
        files=list(result.files),
    )


def _client_story_answer(*, job: str) -> dict[str, Any]:
    """The answer `GET /api/v1/jobs/{job}/story` sends: what `remedy client story <job> --json`
    prints (DECISION amend1015f D14). The job is resolved as its twin resolves it, and the two
    share `job_client_story`."""
    from apps.cli.json_envelope import build_ok
    from packages.orchestration.client_story import job_client_story

    resolved, refusal = _resolved_job_plan(job)
    if resolved is None:
        return refusal or {}
    job_id, plan = resolved
    return build_ok(**job_client_story(job_id, plan))


def _client_diff_answer(*, job: str) -> dict[str, Any]:
    """The answer `GET /api/v1/jobs/{job}/diff` sends: what `remedy client diff <job> --json`
    prints (DECISION amend1015c D5); the two share `job_client_diff`."""
    from apps.cli.json_envelope import build_error, build_ok
    from packages.orchestration.client_diff import ClientDiffRefusal, job_client_diff

    resolved, refusal = _resolved_job_plan(job)
    if resolved is None:
        return refusal or {}
    try:
        return build_ok(**job_client_diff(*resolved))
    except ClientDiffRefusal as exc:
        return build_error(exc.token, str(exc))


def _client_now_answer(*, project_ids: frozenset[str] | None = None) -> dict[str, Any]:
    """The answer `GET /api/v1/now` sends: what `remedy client now --json` prints (DECISIONs
    F311 D1 and D6). A client token's `project_ids` filters it to its own projects' jobs and
    orders, as `GET /api/v1/digest` is filtered."""
    from apps.cli.json_envelope import build_ok
    from packages.orchestration.job_insight import now_insight

    return build_ok(**now_insight(project_ids=project_ids))


def _client_insight_answer(*, job: str, lines: str | None = None) -> dict[str, Any]:
    """The answer `GET /api/v1/jobs/{job}/insight` sends: what `remedy client insight <job>
    --json` prints (DECISIONs F311 D1 and D6). The job is resolved as its twin resolves it, and
    the two share `job_insight`."""
    from apps.cli.json_envelope import build_ok
    from packages.orchestration.job_insight import INSIGHT_LINES_DEFAULT, insight_lines, job_insight

    resolved, refusal = _resolved_job_plan(job)
    if resolved is None:
        return refusal or {}
    _job_id, plan = resolved
    return build_ok(**job_insight(
        plan, lines=insight_lines(lines) if lines is not None else INSIGHT_LINES_DEFAULT))


def _client_read_refusal(client: Any, job: str) -> str | None:
    """One sentence when a client token may not read JOB, which is not a job of one of its
    projects, else None; a value that names no one job is left to the route's own refusal."""
    from packages.orchestration.api_clients import client_lists_project
    from packages.orchestration.data_paths import JobIdError, lookup_job_id
    from packages.orchestration.pingpong_job import load_job_plan_safe
    from packages.orchestration.public_api_writes import job_project_keys

    try:
        plan, degraded = load_job_plan_safe(lookup_job_id(job))
    except JobIdError:
        return None
    if plan is None and not degraded:
        return None
    if client_lists_project(client, job_project_keys(plan)):
        return None
    return (f"the client {client.name!r} may not read job {job!r}, which is not a job of one of "
            "its projects")


def _order_answer(*, order: str) -> dict[str, Any]:
    """The answer `GET /api/v1/orders/{order}` sends: what `remedy client order <order> --json`
    prints (DECISION F253 D14 (4)). Shares `order_record_payload` with the command itself and
    with the order-create route's own 202 answer, so all three read an order alike."""
    from apps.cli.json_envelope import build_error, build_ok
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import (
        order_not_found_message,
        order_record_payload,
        read_order_record,
    )

    paths = serve_paths()
    record = read_order_record(paths, order)
    if record is None:
        return build_error("order_not_found", order_not_found_message(order))
    return build_ok(**order_record_payload(paths, record))


def _run_answer(*, job: str) -> dict[str, Any]:
    """The answer `GET /api/v1/jobs/{job}/run` sends: what `remedy client run <job> --json`
    prints (DECISION F253 D20 (3)). Shares `run_record_payload` with the command itself and with
    the run route's own 202 answer, so all three read a run alike. A value that names no one job,
    or a job with no run record, is refused `run_not_found`; `run_record_for_job_value` reads
    the job's id as the command does (R-1224)."""
    from apps.cli.json_envelope import build_error, build_ok
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import (
        run_not_found_message,
        run_record_for_job_value,
        run_record_payload,
    )

    paths = serve_paths()
    record = run_record_for_job_value(paths, job)
    if record is None:
        return build_error("run_not_found", run_not_found_message(job))
    return build_ok(**run_record_payload(paths, record))


#: Twin command id to the function that builds its answer, called with the route's own query
#: flags and bound path segments as keyword arguments, read at call time so a test that
#: monkeypatches `PUBLIC_API_ROUTES` sees the real handler behind whichever routes it leaves.
_TWIN_ANSWERS: dict[str, Any] = {
    "client.interface": _client_interface_answer,
    "client.execution": _client_execution_answer,
    "status.run": _status_digest_answer,
    "change.proof": _change_proof_answer,
    "client.changes": _client_changes_answer,
    "doctor.health": _doctor_health_answer,
    "doctor.logs": _doctor_logs_answer,
    "client.order": _order_answer,
    "client.run": _run_answer,
    "client.story": _client_story_answer,
    "client.diff": _client_diff_answer,
    "client.now": _client_now_answer,
    "client.insight": _client_insight_answer,
}


#: The read routes a client token may use only for a job of one of its projects; the server's
#: token reads every job (operator amendment amend1014-luna-mission-fixes B.3), and so does the
#: story (DECISION amend1015f D14). The proof and the run poll joined them (DECISION amend1015c
#: D2), when the check of operator order amend1015-final-closure found them answering a client
#: about another project's job, and the diff was born among them (DECISION amend1015c D5); the
#: insight joined them under F311 (DECISION F311 D6).
_CLIENT_SCOPED_TWINS = frozenset({"doctor.logs", "client.story", "change.proof", "client.run",
                                  "client.diff", "client.insight"})
#: The read routes whose answer lists many projects' records: for a client token they list only
#: its own projects' (`client_scope.client_project_ids`, DECISION amend1015c D2); `client.now`
#: joined them under F311 (DECISION F311 D6).
_CLIENT_FILTERED_TWINS = frozenset({"status.run", "client.changes", "client.now"})


def answer_public_api_get(
    path: str, query: str = "", client: Any = None,
) -> tuple[int, dict[str, Any], dict[str, str]]:
    """The (status, body, headers) this namespace answers a GET of `path` with `query`.

    Reads `PUBLIC_API_ROUTES` at call time, never at import time, so a test that replaces the
    registry sees the replacement. An unknown path answers 404 and names the page that lists the
    routes, never a hint at what the right path might be. Once a route's template matches the
    path (DECISION F253 D3 (1)), the RAW query string is parsed against that route's own `query`
    and `query_values` keys (DECISION F253 D2 (2), D5 (1)): a key of `query` takes a value of
    `true` or `false`; a key of `query_values` takes one non-empty value; a key given more than
    once, with an empty value when it is of `query_values`, with a value other than `true`/`false`
    when it is of `query`, or not declared in either, answers 400 `api_query_invalid` before the
    twin is ever asked. The twin's bound path segments, query flags and query values are then
    passed as keyword arguments; a body with `ok` true answers 200, a body with `ok` false answers
    the HTTP status `refusals` declares for its `error` — raising `KeyError` for a token the route
    never declared, which a test catches before it ships.
    """
    from apps.cli.json_envelope import build_error

    for route in PUBLIC_API_ROUTES:
        if route.method != "GET":
            continue
        segments = _match_route_path(route.path, path)
        if segments is None:
            continue
        flags: dict[str, bool] = {}
        values_kw: dict[str, str] = {}
        for key, values in parse_qs(query, keep_blank_values=True).items():
            accepted = ", ".join(f"'{k}'" for k in (*route.query, *route.query_values)) or "none"
            invalid = build_error(
                "api_query_invalid",
                f"'{key}' is not a valid query key for '{path}'; it accepts {accepted}",
            )
            if key in route.query:
                if len(values) != 1 or values[0] not in ("true", "false"):
                    return 400, invalid, {}
                flags[key] = values[0] == "true"
            elif key in route.query_values:
                if len(values) != 1 or not values[0]:
                    return 400, invalid, {}
                values_kw[key] = values[0]
            else:
                return 400, invalid, {}
        if client is not None and route.twin in _CLIENT_SCOPED_TWINS:
            refusal = _client_read_refusal(client, segments.get("job", ""))
            if refusal is not None:
                return 403, build_error("api_client_policy_refused", refusal), {}
        if client is not None and route.twin == "client.order":
            from packages.orchestration.client_scope import client_order_read_refusal

            refusal = client_order_read_refusal(client, segments.get("order", ""))
            if refusal is not None:
                return 403, build_error("api_client_policy_refused", refusal), {}
        scope: dict[str, Any] = {}
        if client is not None and route.twin in _CLIENT_FILTERED_TWINS:
            from packages.orchestration.client_scope import client_project_ids

            scope["project_ids"] = client_project_ids(client)
        body = _TWIN_ANSWERS[route.twin](**flags, **values_kw, **segments, **scope)
        if body.get("ok"):
            status = 200
        else:
            status = dict(route.refusals)[body.get("error", "")]
        headers = {"Deprecation": "true"} if route.deprecated else {}
        return status, body, headers

    return 404, build_error(
        "api_route_not_found",
        f"no route answers '{path}'; docs/system/public-http-api-v1.md lists every route",
    ), {}


_RUN_PROVIDER_KEYS: tuple[str, ...] = ("builder_provider", "reviewer_provider")


def _start_run_answer(
    path: str, job: str, body: dict[str, Any], start_run: Callable[[str, Sequence[str]], Any],
) -> tuple[int, dict[str, Any], dict[str, str]]:
    """The answer of a `starts_run` route for JOB (DECISION F253 D18 (2), (3)).

    The job is read with `lookup_job_id` and `load_job_plan_safe`: a value `lookup_job_id` refuses
    as invalid answers 404 `invalid_job_id`, one no job matches or whose record cannot be read
    answers 404 `job_not_found`, one that matches several answers 400 `ambiguous_job_id`. Then
    START_RUN is called with the full job id and the options the body gives, the builder's
    `--builder-provider=<value>` first and the reviewer's `--reviewer-provider=<value>` second;
    a `RunRefused` answers 409 with its own token and message, an `OSError` 500
    `api_command_failed`, and the run's record 202, read by `run_record_payload` as `GET
    /api/v1/jobs/{job}/run` reads it (DECISION F253 D20 (4)).
    """
    from apps.cli.json_envelope import build_error, build_ok
    from packages.orchestration.data_paths import (
        JobIdAmbiguous,
        JobIdInvalid,
        JobIdNotFound,
        lookup_job_id,
    )
    from packages.orchestration.pingpong_job import load_job_plan_safe
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import RunRefused, run_record_payload

    try:
        job_id = lookup_job_id(job)
    except JobIdAmbiguous as exc:
        listed = "\n".join(f"  {m[:8]}" for m in exc.matches)
        return 400, build_error(
            "ambiguous_job_id",
            f"ambiguous job id prefix '{job}' matches {len(exc.matches)} jobs:\n{listed}",
            matches=exc.matches), {}
    except JobIdInvalid:
        return 404, build_error(
            "invalid_job_id", f"No job matches {job!r}. Try: remedy job list."), {}
    except JobIdNotFound:
        return 404, build_error("job_not_found", f"No job matches {job!r}."), {}
    plan, _degraded = load_job_plan_safe(job_id)
    if plan is None:
        return 404, build_error(
            "job_not_found", f"job {job_id} has no record that can be read; nothing was run"), {}
    from packages.orchestration.execution_options import API_PROVIDER_NOT_OFFERED, remote_provider_refusal

    if why := remote_provider_refusal(body):
        return 400, build_error(API_PROVIDER_NOT_OFFERED, why), {}
    options = [f"--{key.replace('_', '-')}={body[key]}" for key in _RUN_PROVIDER_KEYS
               if key in body]
    try:
        record = start_run(job_id, options)
    except RunRefused as exc:
        return 409, build_error(exc.token, str(exc)), {}
    except OSError:
        return 500, build_error(
            "api_command_failed", f"the run for '{path}' could not be started; nothing runs"), {}
    return 202, build_ok(**run_record_payload(serve_paths(), record)), {}


def _body_refusal(route: PublicApiRoute, raw_body: bytes) -> tuple[dict[str, Any] | None, str]:
    """The checked JSON body of a write to ROUTE and an empty sentence, or None and why not.

    A `string` value, or an item of a `strings` value, that holds a NUL character is refused
    too: a child's arguments cannot hold one, and `subprocess.Popen` would raise out of the
    route (R-1205).
    """
    try:
        parsed = json.loads(raw_body.decode("utf-8")) if raw_body.strip() else {}
    except (UnicodeDecodeError, ValueError):
        return None, "the body is not valid JSON"
    if not isinstance(parsed, dict):
        return None, "the body must be a JSON object"
    kinds = dict(route.body)
    for key, value in parsed.items():
        if key not in kinds:
            takes = ", ".join(f"'{k}'" for k in kinds) or "none"
            return None, f"'{key}' is not a key of this route's body; it takes {takes}"
        if kinds[key] == "string":
            valid = isinstance(value, str)
            wanted = "a string"
        elif kinds[key] == "flag":
            valid = isinstance(value, bool)
            wanted = "true or false"
        else:
            valid = (isinstance(value, list) and all(isinstance(item, str) and item
                                                     for item in value))
            wanted = "a list of non-empty strings"
        if not valid:
            return None, f"'{key}' must be {wanted}"
        if kinds[key] == "string":
            texts = [value]
        elif kinds[key] == "flag":
            texts = []
        else:
            texts = value
        if any("\x00" in text for text in texts):
            return None, f"'{key}' must not hold a NUL character"
    return parsed, ""


def answer_public_api_post(
    path: str, raw_body: bytes,
    run_command: Callable[[str, list[str]], dict[str, Any] | None],
    start_order: Callable[[str, Sequence[str]], Any] | None = None,
    client: Any = None,
    start_run: Callable[[str, Sequence[str]], Any] | None = None,
) -> tuple[int, dict[str, Any], dict[str, str]]:
    """The (status, body, headers) this namespace answers a POST of `path` with `raw_body`.

    With a CLIENT (DECISION F253 D16 (5), (6)) an order outside its policy, and an apply whose
    client may not approve, answer 403 `api_client_policy_refused` and run nothing. So does a
    decision, a decline or an apply for a job outside the client's projects, and a budget answer
    above the client's ceilings (DECISION F253 D17): `_client_write_refusal` reads the job after the
    body is checked and before the may-apply check.

    DECISION F253 D9. Matches POST routes as `answer_public_api_get` matches GET routes: a path no
    route matches answers 404, a path only a GET route matches answers 405. A bound segment that
    begins with `-`, or that holds `/` or a NUL character once decoded, answers 400
    `api_path_invalid`, because a command builds a file name from its job value and a child's
    arguments cannot hold a NUL (R-1195).

    A route marked `starts_order` (DECISION F253 D14 (3)) never reaches RUN_COMMAND: with no
    START_ORDER it answers 405 `api_method_not_allowed`, exactly as a handler with no command
    runner does; otherwise its body is checked, `_order_text_and_options` builds the order's text
    and options or raises `PublicApiWriteRefusal`, START_ORDER is called with them, and the
    order it started is answered 202 with `order_record_payload` — the same answer `GET
    /api/v1/orders/{order}` and `remedy client order` give it. An `OSError` from START_ORDER —
    the order could not be started — answers 500 `api_command_failed` and nothing runs
    (R-1201).

    An order body with `order_key` (DECISION F253 D22 (2), (4), (5)) is checked first: a key that
    `ORDER_KEY_RE` does not fully match answers 400 `api_body_invalid` and nothing else is read.
    After `_order_text_and_options` has passed, and unless the body sets `new_mission`, the key's
    file (`keyed_order_file_path`, resolved) is asked of `running_mission_for_order_file`: a mission
    that has not ended answers 409 `order_already_running` with its id under `mission_id` and
    START_ORDER is not called. START_ORDER gets the key as the keyword `order_key` only when the
    body has one, so a starter of two arguments still serves an order without a key.

    A route marked `starts_run` (DECISION F253 D18) is answered the same way through START_RUN:
    with none it answers 405 `api_method_not_allowed`; once the body is checked and a client's
    checks of DECISION F253 D17 have passed, `_start_run_answer` reads the job, answers the
    refusals of D18 (2) and calls START_RUN with the full job id and the options the body gives;
    a `RunRefused` answers 409 with its own token, an `OSError` 500 `api_command_failed`, and the
    run's record 202.

    Every other route's body, not a JSON object holding only its declared keys each of its kind,
    answers 400 `api_body_invalid`; a `PublicApiWriteRefusal` from the twin's argument builder
    answers its own status and token; none of these starts a command. Otherwise RUN_COMMAND is
    called with the job or order its path names (`_write_lock_key`) and the argument list the twin's
    builder makes, and the envelope it returns is the answer: None answers 500
    `api_command_failed`, an `ok` envelope 200, a refusal the status `refusals` declares for its
    token or else the route's `refusal_default`.
    """
    from apps.cli.json_envelope import build_error, build_ok

    for route in PUBLIC_API_ROUTES:
        if route.method != "POST":
            continue
        segments = _match_route_path(route.path, path)
        if segments is None:
            continue
        for name, value in segments.items():
            if value.startswith("-"):
                return 400, build_error(
                    "api_path_invalid",
                    f"the {name} in '{path}' must not begin with '-'"), {}
            if "/" in value or "\x00" in value:
                return 400, build_error(
                    "api_path_invalid",
                    f"the {name} in '{path}' must not hold '/' or a NUL character"), {}
        if route.starts_order and start_order is None:
            return (*public_api_method_refusal(), {})
        if route.starts_run and start_run is None:
            return (*public_api_method_refusal(), {})
        checked, why = _body_refusal(route, raw_body)
        if checked is None:
            return 400, build_error("api_body_invalid", why), {}
        if route.starts_order:
            from packages.orchestration.serve_paths import serve_paths
            from packages.orchestration.serve_runs import (
                ORDER_KEY_RE,
                keyed_order_file_path,
                order_record_payload,
            )

            order_key = checked.get("order_key")
            if order_key is not None and ORDER_KEY_RE.fullmatch(order_key) is None:
                return 400, build_error(
                    "api_body_invalid",
                    "'order_key' must be 1 to 64 letters, digits, '.', '_' or '-', "
                    "beginning with a letter or a digit"), {}
            try:
                order_text, options = _order_text_and_options(checked, client)
            except PublicApiWriteRefusal as refusal:
                return refusal.status, build_error(refusal.error, refusal.message), {}
            if order_key is not None and not checked.get("new_mission"):
                from packages.orchestration.repo_mission import running_mission_for_order_file

                mission = running_mission_for_order_file(
                    str(keyed_order_file_path(serve_paths(), order_key).resolve()))
                if mission is not None:
                    return 409, build_error(
                        "order_already_running",
                        f"the order key {order_key!r} still has unfinished jobs in mission "
                        f"{mission.id} ({mission.status}); let them finish or stop them, or send "
                        "the order with new_mission true to run it again as one more order of "
                        "the same mission; nothing was run",
                        mission_id=mission.id), {}
            try:
                if order_key is None:
                    record = start_order(order_text, options)
                else:
                    record = start_order(order_text, options, order_key=order_key)
            except OSError:
                return 500, build_error(
                    "api_command_failed",
                    f"the order for '{path}' could not be started; nothing runs"), {}
            return 202, build_ok(**order_record_payload(serve_paths(), record)), {}
        if client is not None and ("job" in segments or "order" in segments):
            refusal_text = _client_write_refusal(client, segments)
            if refusal_text is None and route.twin == "decision.resolve":
                from packages.orchestration.api_clients import client_budget_answer_refusal
                from packages.orchestration.decision_queue import is_budget_decision_id

                if is_budget_decision_id(segments["decision"]):
                    refusal_text = client_budget_answer_refusal(client, checked.get("answer", []), job=segments["job"])
            if refusal_text is not None:
                return 403, build_error("api_client_policy_refused", refusal_text), {}
        if client is not None and route.twin == "job.apply" and not client.may_apply:
            return 403, build_error(
                "api_client_policy_refused",
                f"the client {client.name!r} may not approve a result into a repository; "
                "nothing was run"), {}
        if route.starts_run:
            return _start_run_answer(path, segments["job"], checked, start_run)
        try:
            argv = _TWIN_ARGV[route.twin](segments, checked)
        except PublicApiWriteRefusal as refusal:
            return refusal.status, build_error(refusal.error, refusal.message), {}
        envelope = run_command(_write_lock_key(segments), argv)
        if envelope is None:
            return 500, build_error(
                "api_command_failed",
                f"the command for '{path}' printed no answer, or took longer than allowed"), {}
        from packages.orchestration.budget_stop import resume_after_budget_extend
        envelope = resume_after_budget_extend(route.twin, segments, envelope, start_run)  # DECISION F310 D5 (4)
        status = 200 if envelope.get("ok") else dict(route.refusals).get(
            envelope.get("error", ""), route.refusal_default or 500)
        headers = {"Deprecation": "true"} if route.deprecated else {}
        return status, envelope, headers

    if any(_match_route_path(route.path, path) is not None for route in PUBLIC_API_ROUTES):
        return (*public_api_method_refusal(), {})
    return 404, build_error(
        "api_route_not_found",
        f"no route answers '{path}'; docs/system/public-http-api-v1.md lists every route",
    ), {}


#: The call ledger's own file name, under the `api` data-root class (DECISION F253 D2 (1)).
PUBLIC_API_LEDGER_NAME = "calls.jsonl"


def append_public_api_call(*, token_fp: str, client: str, method: str, path: str, status: int,
                            error: str, root: Path | None = None) -> None:
    """Append one line to the data root's `api/calls.jsonl` call ledger (DECISION F253 D2 (1)).

    CLIENT is the name of the client whose token the call presented, or the empty string
    (DECISION F253 D16 (7)); it is written as the key after `token_fp`.

    One `os.write` of one already-built line so concurrent requests never interleave; the
    directory is created at 0o700 and the file opened at 0o600, append-only. Raises `OSError` on
    failure and catches nothing itself — the caller (`_send_public_api_get`) decides whether a
    failed write may change the answer it is recording, per DECISION F009 D14 clause four.
    """
    import json
    import os
    from datetime import datetime, timezone

    from packages.orchestration.data_paths import data_class_dir

    directory = data_class_dir("api", root)
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    record = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "token_fp": token_fp,
        "client": client,
        "method": method,
        "path": path,
        "status": status,
        "error": error,
    }
    line = (json.dumps(record) + "\n").encode("utf-8")
    fd = os.open(str(directory / PUBLIC_API_LEDGER_NAME),
                 os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        os.write(fd, line)
    finally:
        os.close(fd)


#: The page this module's generated section lives in, between the two markers below; the rest of
#: the page, written by hand, states the rules the generated table only lists.
PUBLIC_API_PAGE_PATH = "docs/system/public-http-api-v1.md"
PUBLIC_API_PAGE_BEGIN = "<!-- BEGIN GENERATED by render_public_api_markdown() -->"
PUBLIC_API_PAGE_END = "<!-- END GENERATED by render_public_api_markdown() -->"


def _twin_command_line(twin: str) -> str:
    """The twin's command id spelled as the command line spells it, read from the catalog."""
    from apps.cli.command_catalog import get_command

    entry = get_command(twin)
    return f"remedy {entry.group_id} {entry.subcommand} --json"


def render_public_api_markdown() -> str:
    """The generated section of the public HTTP API page, markers included."""
    lines = [
        PUBLIC_API_PAGE_BEGIN,
        "## Routes",
        "",
        "> GENERATED from `PUBLIC_API_ROUTES` in `packages/orchestration/public_api.py`. Do not",
        "> edit this section by hand: a test fails whenever the registry and this section differ.",
        "> Regenerate it from the repository root with",
        "> `python3 -c \"from packages.orchestration.public_api import write_public_api_page; "
        "write_public_api_page()\"`.",
        "",
        f"API version: `{PUBLIC_API_VERSION}`.",
        "",
        "| Method | Path | Query or body | Answers as | Refusals | Deprecated | Description |",
        "|---|---|---|---|---|---|---|",
    ]
    for route in PUBLIC_API_ROUTES:
        deprecated = "yes" if route.deprecated else "no"
        query_cell = ", ".join(
            [f"`{key}`" for key in route.query]
            + [f"`{key}=<value>`" for key in route.query_values]
            + [f"`{key}` ({kind})" for key, kind in route.body]
        ) or "—"
        command_line = _twin_command_line(route.twin)
        if route.starts_run:
            # R-1206: the route answers 202 with the run's record, not the twin's result.
            answers_as = "the run's record, as the supervisor's `RunLauncher` writes it"
        elif route.twin_key:
            answers_as = f"`{command_line}`, its `{route.twin_key}` object"
        else:
            answers_as = f"`{command_line}`"
        refusals_cell = ", ".join(
            [f"`{token}` {status}" for token, status in route.refusals]
            + ([f"any other {route.refusal_default}"] if route.refusal_default else [])
        ) or "—"
        lines.append(
            f"| `{route.method}` | `{route.path}` | {query_cell} | {answers_as} "
            f"| {refusals_cell} | {deprecated} | {route.description} |"
        )
    lines += [
        "",
        "### Never published",
        "",
    ]
    lines += [f"- `{command_id}`" for command_id in PUBLIC_API_EXCLUDED_COMMANDS]
    lines.append(PUBLIC_API_PAGE_END)
    return "\n".join(lines) + "\n"


def write_public_api_page(path: Path | None = None) -> Path:
    """Replace the generated section of the page under `path`'s repository root."""
    base = path if path is not None else Path(__file__).resolve().parents[2]
    page = base / PUBLIC_API_PAGE_PATH
    text = page.read_text(encoding="utf-8")
    start = text.index(PUBLIC_API_PAGE_BEGIN)
    end = text.index(PUBLIC_API_PAGE_END) + len(PUBLIC_API_PAGE_END) + 1
    page.write_text(text[:start] + render_public_api_markdown() + text[end:], encoding="utf-8")
    return page
