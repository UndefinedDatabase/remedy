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
fingerprint, never the query string, and a line that cannot be written changes nothing in the
answer sent. A route may answer one key of its twin's answer alone (`twin_key`) and takes only
the query keys it declares: each of `query` a `true`/`false` flag, each of `query_values` one
non-empty value given once; anything else answers 400 `api_query_invalid` (DECISION F253 D2 (2),
D5 (1)).

A `POST` route is a write (DECISION F253 D9): it declares the keys of its JSON body in `body` and
a `refusal_default` status, and `answer_public_api_post` answers it with the envelope of the twin
command, which the caller's runner has run as a child process.

`render_public_api_markdown` renders the generated section of `docs/system/public-http-api-v1.md`,
and `write_public_api_page` writes it there; a test holds that section equal to the rendering.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote

#: The path prefix every route under this registry lives below; the major version is in the path.
PUBLIC_API_PREFIX = "/api/v1"

#: This registry's own version. The minor number rises whenever a route, an answer key or a
#: refusal token is added; the major number changes only under a new path prefix.
PUBLIC_API_VERSION = "1.4"


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
    #: The keys of a write route's JSON body, each with its kind: `"string"`, or `"strings"` (a
    #: list of non-empty strings) (DECISION F253 D9 (3)); `()` for a route that takes no body.
    body: tuple[tuple[str, str], ...] = ()
    #: The HTTP status of a refusal token `refusals` does not list, or None when every refusal
    #: must be listed (DECISION F253 D9 (4)).
    refusal_default: int | None = None


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
    """The 401 a caller gets for a missing or wrong bearer token."""
    from apps.cli.json_envelope import build_error

    return 401, build_error(
        "api_token_invalid",
        "this route needs the server's token as 'Authorization: Bearer <token>'",
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


#: Twin command id to the function that builds its answer, called with the route's own query
#: flags and bound path segments as keyword arguments, read at call time so a test that
#: monkeypatches `PUBLIC_API_ROUTES` sees the real handler behind whichever routes it leaves.
_TWIN_ANSWERS: dict[str, Any] = {
    "client.interface": _client_interface_answer,
    "status.run": _status_digest_answer,
    "change.proof": _change_proof_answer,
    "client.changes": _client_changes_answer,
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


def _decision_resolve_argv(segments: dict[str, str], body: dict[str, Any]) -> list[str]:
    """The command line `remedy decision resolve` is run with: each option as `--name=value`,
    then `--json`, then `--` so that no value is read as an option (DECISION F253 D9 (1))."""
    options = [f"--reason={body['reason']}"] if "reason" in body else []
    options += [f"--answer={answer}" for answer in body.get("answer", [])]
    return ["decision", "resolve", *options, "--json", "--", segments["job"], segments["decision"]]


#: Twin command id of a write route to the function that builds the argument list its command
#: runs with, from the route's bound path segments and its checked body (DECISION F253 D9).
_TWIN_ARGV: dict[str, Callable[[dict[str, str], dict[str, Any]], list[str]]] = {
    "decision.resolve": _decision_resolve_argv,
}


def _job_lock_key(job: str) -> str:
    """The job a write locks on: the full id JOB names, or JOB itself when it names no one job,
    so that a prefix and its full id wait for each other (DECISION F253 D9 (1), R-1193)."""
    from packages.orchestration.data_paths import JobIdError, lookup_job_id

    try:
        return lookup_job_id(job)
    except JobIdError:
        return job


def _body_refusal(route: PublicApiRoute, raw_body: bytes) -> tuple[dict[str, Any] | None, str]:
    """The checked JSON body of a write to ROUTE and an empty sentence, or None and why not."""
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
        else:
            valid = (isinstance(value, list) and all(isinstance(item, str) and item
                                                     for item in value))
            wanted = "a list of non-empty strings"
        if not valid:
            return None, f"'{key}' must be {wanted}"
    return parsed, ""


def answer_public_api_post(
    path: str, raw_body: bytes,
    run_command: Callable[[str, list[str]], dict[str, Any] | None],
) -> tuple[int, dict[str, Any], dict[str, str]]:
    """The (status, body, headers) this namespace answers a POST of `path` with `raw_body`.

    DECISION F253 D9. Matches POST routes as `answer_public_api_get` matches GET routes: a path no
    route matches answers 404, a path only a GET route matches answers 405. A bound segment that
    begins with `-`, or that holds `/` or a NUL character once decoded, answers 400
    `api_path_invalid`, because a command builds a file name from its job value and a child's
    arguments cannot hold a NUL (R-1195); a body that is not a JSON object holding
    only the route's declared keys, each of its kind, answers 400 `api_body_invalid`; neither
    starts a command. Otherwise RUN_COMMAND is called with the job the job segment names
    (`_job_lock_key`) and the argument list the twin's builder makes, and the envelope it returns is the answer: None answers 500
    `api_command_failed`, an `ok` envelope 200, a refusal the status `refusals` declares for its
    token or else the route's `refusal_default`.
    """
    from apps.cli.json_envelope import build_error

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
        checked, why = _body_refusal(route, raw_body)
        if checked is None:
            return 400, build_error("api_body_invalid", why), {}
        envelope = run_command(_job_lock_key(segments["job"]),
                               _TWIN_ARGV[route.twin](segments, checked))
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


def append_public_api_call(*, token_fp: str, method: str, path: str, status: int, error: str,
                            root: Path | None = None) -> None:
    """Append one line to the data root's `api/calls.jsonl` call ledger (DECISION F253 D2 (1)).

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
        answers_as = (
            f"`{command_line}`, its `{route.twin_key}` object" if route.twin_key
            else f"`{command_line}`"
        )
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
