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

`render_public_api_markdown` renders the generated section of `docs/system/public-http-api-v1.md`,
and `write_public_api_page` writes it there; a test holds that section equal to the rendering.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote

from packages.orchestration.public_api_writes import (
    _JOB_APPLY_FLAGS as _JOB_APPLY_FLAGS,
)
from packages.orchestration.public_api_writes import (
    _ORDER_CREATE_FLAGS as _ORDER_CREATE_FLAGS,
)
from packages.orchestration.public_api_writes import (
    _ORDER_CREATE_STRINGS as _ORDER_CREATE_STRINGS,
)

# DECISION F205 D6: the write routes' argument builders and refusals live in a module of
# their own; every name is imported back here by name, so every import path keeps working.
from packages.orchestration.public_api_writes import (
    _TWIN_ARGV,
    PublicApiWriteRefusal,
    _client_job_refusal,
    _job_lock_key,
    _order_text_and_options,
)
from packages.orchestration.public_api_writes import (
    _decision_resolve_argv as _decision_resolve_argv,
)
from packages.orchestration.public_api_writes import (
    _job_apply_argv as _job_apply_argv,
)
from packages.orchestration.public_api_writes import (
    _job_decline_argv as _job_decline_argv,
)

#: The path prefix every route under this registry lives below; the major version is in the path.
PUBLIC_API_PREFIX = "/api/v1"

#: This registry's own version. The minor number rises whenever a route, an answer key or a
#: refusal token is added; the major number changes only under a new path prefix.
PUBLIC_API_VERSION = "1.11"


@dataclass(frozen=True)
class PublicApiRoute:
    """One published route: its method, its full path and the command it answers like."""

    method: str
    path: str
    #: The catalog command id whose `--json` answer this route answers.
    twin: str
    #: One sentence for the page.
    description: str
    deprecated: bool = False
    #: The key of the twin's `--json` answer this route answers alone, or None for the whole answer.
    twin_key: str | None = None
    #: The query keys this route accepts, each a `true`/`false` flag (DECISION F253 D2 (2)).
    query: tuple[str, ...] = ()
    #: The query keys this route accepts with one value each, given once and never empty (DECISION F253 D5 (1)).
    query_values: tuple[str, ...] = ()
    #: The refusal tokens this route shares with its twin, each with the HTTP status it answers
    #: with (DECISION F253 D3 (2)); `()` for a route that never refuses.
    refusals: tuple[tuple[str, int], ...] = ()
    #: The keys of a write route's JSON body, each with its kind: `"string"`, `"strings"` (a list
    #: of non-empty strings) (DECISION F253 D9 (3)), or `"flag"` (`true` or `false`) (DECISION
    #: F253 D12); `()` for a route that takes no body.
    body: tuple[tuple[str, str], ...] = ()
    #: The HTTP status of a refusal token `refusals` does not list, or None when every refusal
    #: must be listed (DECISION F253 D9 (4)); also None for a `starts_order` route, whose every
    #: refusal is explicit through `PublicApiWriteRefusal` (DECISION F253 D14 (2)).
    refusal_default: int | None = None
    #: True for a write route that starts an order through the caller's own order starter rather
    #: than running its twin as a child of the command runner (DECISION F253 D14 (1), (3)).
    starts_order: bool = False
    #: True for a write route that starts a job's run through the caller's own run starter, the
    #: supervisor's `RunLauncher`, rather than running its twin as a child of the command runner
    #: (DECISION F253 D18 (1), (3)); like a `starts_order` route it has no `refusal_default`.
    starts_run: bool = False


#: Every route this registry publishes. A test pins each one by name, so an unpinned addition
#: fails the suite rather than shipping unreviewed.
PUBLIC_API_ROUTES: tuple[PublicApiRoute, ...] = (
    PublicApiRoute(
        method="GET",
        path="/api/v1/interface",
        twin="client.interface",
        description=(
            "What a program that drives Remedy can rely on: its operations, arguments, exit "
            "codes, state words, templates and budget kinds, as `remedy client interface --json` "
            "prints it."
        ),
    ),
    PublicApiRoute(
        method="GET",
        path="/api/v1/digest",
        twin="status.run",
        twin_key="client",
        query=("all_ended_jobs",),
        description=(
            "The digest a program reads about once a minute: every project with its missions, "
            "the jobs that still need something and the last ended ones, every open decision and "
            "the jobs waiting for their apply, as the `client` object of `remedy status --json` "
            "holds it; `all_ended_jobs=true` lists every ended job, as `--all-ended-jobs` does."
        ),
    ),
    PublicApiRoute(
        method="GET",
        path="/api/v1/jobs/{job}/proof",
        twin="change.proof",
        refusals=(("invalid_job_id", 404), ("job_not_found", 404), ("ambiguous_job_id", 400)),
        description=(
            "The proof of one job: what each change rests on and where its evidence is, as "
            "`remedy change proof <job> --json` prints it; a job id prefix is accepted, as on the "
            "command line, and the command's `--path` filter is not offered over HTTP."
        ),
    ),
    PublicApiRoute(
        method="GET",
        path="/api/v1/changes",
        twin="client.changes",
        query_values=("since",),
        refusals=(("invalid_cursor", 400),),
        description=(
            "What changed since a cursor: the jobs and decisions as the digest shows them, the "
            "decisions answered, the missions and the applies, with the cursor for the next "
            "read, as `remedy client changes --since <cursor> --json` prints it; without "
            "`since` only a cursor is given."
        ),
    ),
    PublicApiRoute(
        method="POST",
        path="/api/v1/jobs/{job}/decisions/{decision}",
        twin="decision.resolve",
        body=(("reason", "string"), ("answer", "strings")),
        refusal_default=409,
        refusals=(
            ("invalid_job_id", 404),
            ("job_not_found", 404),
            ("decision_not_found", 404),
            ("stop_reason_not_found", 404),
            ("proposed_task_not_found", 404),
            ("ambiguous_job_id", 400),
            ("invalid_argument", 400),
            ("missing_argument", 400),
            ("option_not_applicable", 400),
            ("answer_parse_error", 400),
            ("invalid_budget", 400),
            ("decision_not_resolvable", 400),
        ),
        description=(
            "Answers one decision of a job, as `remedy decision resolve <job> <decision> --json` "
            "does: `reason` is given as `--reason` and each `answer` as one `--answer`; a job id "
            "prefix is accepted, as on the command line, and `--as-mission` is not offered over "
            "HTTP."
        ),
    ),
    PublicApiRoute(
        method="POST",
        path="/api/v1/jobs/{job}/decline",
        twin="job.decline",
        body=(("reason", "string"),),
        refusal_default=409,
        refusals=(
            ("invalid_job_id", 404),
            ("job_not_found", 404),
            ("ambiguous_job_id", 400),
            ("missing_argument", 400),
        ),
        description=(
            "Declines a completed job's result, as `remedy job decline <job> --reason <reason> "
            "--json` does: nothing is applied and the decline is kept on the job, recorded as "
            "coming through `api`; a job that is not completed, or whose result already landed, "
            "is refused with 409."
        ),
    ),
    PublicApiRoute(
        method="POST",
        path="/api/v1/jobs/{job}/apply",
        twin="job.apply",
        body=(("commit", "string"), ("commit_auto", "flag"), ("commit_with_history", "flag"),
              ("push", "flag"), ("skip_blocked", "flag")),
        refusal_default=409,
        refusals=(
            ("job_not_found", 404),
            ("invalid_argument", 400),
        ),
        description=(
            "Approves a completed job's result and applies it to the repository the job's own "
            "record names, as `remedy job apply <job> --repo <that repository> --approve --json` "
            "does: `commit` is given as `--commit`, and each of `commit_auto`, "
            "`commit_with_history`, `push` and `skip_blocked` set to `true` as its option; a job "
            "id prefix is accepted; `--repo`, `--test-command` and `--dry-run` are not offered "
            "over HTTP, and a job whose record names no repository is refused with 409 "
            "`api_job_repository_unknown` before any command runs."
        ),
    ),
    PublicApiRoute(
        method="GET",
        path="/api/v1/orders/{order}",
        twin="client.order",
        refusals=(("order_not_found", 404),),
        description=(
            "Polls the order a `POST` to `/api/v1/orders` started, as `remedy client order "
            "<order> --json` does: `state` reads `running`, `ended` or `lost`, and `answer` "
            "holds what `remedy do` printed once the order is not `running`."
        ),
    ),
    PublicApiRoute(
        method="POST",
        path="/api/v1/orders",
        twin="client.order",
        body=(("order", "string"), ("no_llm", "flag"), ("new_mission", "flag"),
              ("force_job", "flag"), ("force_mission", "flag"), ("builder_provider", "string"),
              ("reviewer_provider", "string"), ("deadline", "string"), ("order_key", "string")),
        starts_order=True,
        description=(
            "Starts an order through the supervisor's own `OrderLauncher`, the way `remedy do "
            "run <options> --no-ui --yes -- order.md` would inside its own folder under the "
            "data root, and answers 202 with its record read exactly as the route above reads "
            "it. `order` is the order file's whole text, header included, and required; "
            "`no_llm`, `new_mission`, `force_job` and `force_mission` each pass their `remedy "
            "do` flag when `true`; `builder_provider`, `reviewer_provider` and `deadline` each "
            "pass their option with their value. An order whose header names no project, or "
            "one that names a project `select_project` cannot resolve to exactly one, is "
            "refused before anything starts with 409 `api_order_project_unknown`; every other "
            "refusal is `remedy do`'s own, read back only once the order is polled. "
            "`order_key` names the order with a key the client chooses, one to 64 letters, "
            "digits, `.`, `_` or `-`, beginning with a letter or a digit, any other value "
            "answering 400 `api_body_invalid`; an order with a key whose order file a mission "
            "that has not ended records is refused before anything starts with 409 "
            "`order_already_running`, the mission's id under `mission_id`, unless `new_mission` "
            "is `true`, and the record's `order_file` then names the key's file."
        ),
    ),
    PublicApiRoute(
        method="GET",
        path="/api/v1/jobs/{job}/run",
        twin="client.run",
        refusals=(("run_not_found", 404),),
        description=(
            "Polls the run the `POST` to this path started, answering the run's record as "
            "`remedy client run <job> --json` does: the record's keys, `state` and `answer`. A "
            "client polls it until `state` is not `running`: `state` reads `running`, `ended` or "
            "`lost`; `exit_code` is `null` until the run ends and stays `null` for a run read "
            "`lost`; `answer` is `null` while the run is `running` and afterwards holds what "
            "`remedy job run --json` printed, or `null` when it printed no envelope. A job id "
            "prefix is accepted; a value that names no one job, or a job with no run, is "
            "refused with 404 `run_not_found`."
        ),
    ),
    PublicApiRoute(
        method="POST",
        path="/api/v1/jobs/{job}/run",
        twin="job.run",
        body=(("builder_provider", "string"), ("reviewer_provider", "string")),
        starts_run=True,
        description=(
            "Starts a job's run through the supervisor's own `RunLauncher`, as `remedy job run "
            "<job> <options> --json` would, and answers 202 with the run's record: `job_id`, "
            "`pid`, `started_at`, `out_log`, `err_log`, `exit_code` and `ended_at`, the last two "
            "`null` until the run ends, and `state` and `answer` as the route above reads them. "
            "`builder_provider` and `reviewer_provider` each pass "
            "`--builder-provider=<value>` and `--reviewer-provider=<value>`; no other option of "
            "`remedy job run` is offered over HTTP. A job id prefix is accepted. A client waits "
            "for the run's end by polling the route above until `state` is not `running`. "
            "Refusals: `invalid_job_id` 404, `job_not_found` 404 (also for a "
            "record that cannot be read), `ambiguous_job_id` 400, `job_already_running` 409, "
            "`api_command_failed` 500 when the run cannot start, and "
            "`api_client_policy_refused` 403 for a client token's job outside its projects."
        ),
    ),
)

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


def _status_digest_answer(*, all_ended_jobs: bool = False) -> dict[str, Any]:
    """The answer `GET /api/v1/digest` sends: the `client` key of `status.run`'s `--json` answer.

    Calls `build_client_digest` directly rather than the whole `status.run` command: the digest
    reads the data root alone, while the rest of that command's answer depends on the directory
    the server happens to run in (DECISION F253 D2 (3)).
    """
    from apps.cli.json_envelope import build_ok
    from packages.orchestration.client_digest import build_client_digest

    return build_ok(**build_client_digest(every_ended_job=all_ended_jobs))


def _change_proof_answer(*, job: str) -> dict[str, Any]:
    """The answer `GET /api/v1/jobs/{job}/proof` sends: what `change.proof --json` prints with no
    `--path` (DECISION F253 D3 (3)).

    Reproduces `apps.cli.commands.change._cmd_change_proof`'s own resolution, refusal messages
    included, rather than calling `apps.cli.job_id_arg.resolve_job_id_or_fail` or `fail()`
    directly: both exit the process, which a route handler must never do. The messages below are
    therefore held equal to the command's by test, not shared by import.
    """
    from apps.cli.json_envelope import build_error, build_ok
    from packages.orchestration.data_paths import (
        JobIdAmbiguous,
        JobIdError,
        lookup_job_id,
        resolve_data_root,
    )
    from packages.orchestration.pingpong_job import JobNotFoundError, require_job_plan
    from packages.orchestration.proof_chain import build_proof_chain, export_proof_chain_json
    from packages.orchestration.timeline import load_run_events

    try:
        job_id = lookup_job_id(job)
    except JobIdAmbiguous as exc:
        matches = exc.matches
        listed = "\n".join(f"  {m[:8]}" for m in matches)
        return build_error(
            "ambiguous_job_id",
            f"ambiguous job id prefix '{job}' matches {len(matches)} jobs:\n{listed}",
            matches=matches,
        )
    except JobIdError:
        return build_error("invalid_job_id", f"No job matches {job!r}. Try: remedy job list.")

    try:
        plan = require_job_plan(job_id)
    except JobNotFoundError as exc:
        return build_error("job_not_found", str(exc))

    data_dir = resolve_data_root()
    chain = build_proof_chain(plan, load_run_events(data_dir, job_id), path=None, data_dir=data_dir)
    return build_ok(**export_proof_chain_json(chain))


def _client_changes_answer(*, since: str | None = None) -> dict[str, Any]:
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

    return build_ok(**build_client_changes(parsed_since))


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
    "status.run": _status_digest_answer,
    "change.proof": _change_proof_answer,
    "client.changes": _client_changes_answer,
    "client.order": _order_answer,
    "client.run": _run_answer,
}


def answer_public_api_get(
    path: str, query: str = "",
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
        body = _TWIN_ANSWERS[route.twin](**flags, **values_kw, **segments)
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
    above the client's ceilings (DECISION F253 D17): `_client_job_refusal` reads the job after the
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
    called with the job the job segment names (`_job_lock_key`) and the argument list the twin's
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
                from packages.orchestration.mission_state import running_mission_for_order_file

                mission = running_mission_for_order_file(
                    str(keyed_order_file_path(serve_paths(), order_key).resolve()))
                if mission is not None:
                    return 409, build_error(
                        "order_already_running",
                        f"the order key {order_key!r} is already run by mission {mission.id} "
                        f"({mission.status}); abandon it with `remedy mission abandon "
                        f"{mission.id}`, or send the order with new_mission true to start "
                        "another; nothing was run",
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
        if client is not None and "job" in segments:
            refusal_text = _client_job_refusal(client, segments["job"])
            if refusal_text is None and route.twin == "decision.resolve":
                from packages.orchestration.api_clients import client_budget_answer_refusal
                from packages.orchestration.decision_queue import is_budget_decision_id

                if is_budget_decision_id(segments["decision"]):
                    refusal_text = client_budget_answer_refusal(client, checked.get("answer", []))
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
        envelope = run_command(_job_lock_key(segments["job"]), argv)
        if envelope is None:
            return 500, build_error(
                "api_command_failed",
                f"the command for '{path}' printed no answer, or took longer than allowed"), {}
        if envelope.get("ok"):
            status = 200
        else:
            status = dict(route.refusals).get(envelope.get("error", ""),
                                              route.refusal_default or 500)
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
