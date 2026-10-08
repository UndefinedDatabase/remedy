"""The public HTTP API's routes, its version and what it never publishes (F253, DECISION F253 D1).

A route under `PUBLIC_API_PREFIX` answers exactly what its twin command answers with `--json`: the
same envelope `apps/cli/json_envelope.py` builds, read from `PUBLIC_API_ROUTES` at call time so a
test can replace the registry and see the handler follow it. The version rule: the major number is
in the path; inside `/api/v1` a route, an answer key or a refusal token is only ever added, and
each addition raises the minor number of `PUBLIC_API_VERSION`; a route that is to go is first
marked `deprecated`, which makes it answer the header `Deprecation: true` and shows it in the
page's table, and it is removed only under a new major path.

Every request under this namespace, a refused one included, appends one line to the data root's
`api/calls.jsonl` (DECISION F253 D2 (1)): the caller's token kept only as its DECISION F009 D7
fingerprint, never the query string, and a line that cannot be written changes nothing in the
answer sent. A route may answer one key of its twin's answer alone (`twin_key`) and takes only
the query keys it declares (`query`), each a `true`/`false` flag; anything else answers 400
`api_query_invalid` (DECISION F253 D2 (2)).

`render_public_api_markdown` renders the generated section of `docs/system/public-http-api-v1.md`,
and `write_public_api_page` writes it there; a test holds that section equal to the rendering.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs

#: The path prefix every route under this registry lives below; the major version is in the path.
PUBLIC_API_PREFIX = "/api/v1"

#: This registry's own version. The minor number rises whenever a route, an answer key or a
#: refusal token is added; the major number changes only under a new path prefix.
PUBLIC_API_VERSION = "1.1"


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


def public_api_token_refusal() -> tuple[int, dict[str, Any]]:
    """The 401 a caller gets for a missing or wrong bearer token."""
    from apps.cli.json_envelope import build_error

    return 401, build_error(
        "api_token_invalid",
        "this route needs the server's token as 'Authorization: Bearer <token>'",
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


#: Twin command id to the function that builds its answer, called with the route's own query
#: flags as keyword arguments, read at call time so a test that monkeypatches `PUBLIC_API_ROUTES`
#: sees the real handler behind whichever routes it leaves.
_TWIN_ANSWERS: dict[str, Any] = {
    "client.interface": _client_interface_answer,
    "status.run": _status_digest_answer,
}


def answer_public_api_get(
    path: str, query: str = "",
) -> tuple[int, dict[str, Any], dict[str, str]]:
    """The (status, body, headers) this namespace answers a GET of `path` with `query`.

    Reads `PUBLIC_API_ROUTES` at call time, never at import time, so a test that replaces the
    registry sees the replacement. An unknown path answers 404 and names the page that lists the
    routes, never a hint at what the right path might be. Once a route is found, the RAW query
    string is parsed against that route's own `query` keys (DECISION F253 D2 (2)): a key the route
    does not declare, a key given more than once, or a value other than `true`/`false` answers 400
    `api_query_invalid` before the twin is ever asked.
    """
    from apps.cli.json_envelope import build_error

    for route in PUBLIC_API_ROUTES:
        if route.method == "GET" and route.path == path:
            flags: dict[str, bool] = {}
            for key, values in parse_qs(query, keep_blank_values=True).items():
                if key not in route.query or len(values) != 1 or values[0] not in ("true", "false"):
                    accepted = ", ".join(f"'{k}'" for k in route.query) or "none"
                    return 400, build_error(
                        "api_query_invalid",
                        f"'{key}' is not a valid query key for '{path}'; it accepts {accepted}",
                    ), {}
                flags[key] = values[0] == "true"
            body = _TWIN_ANSWERS[route.twin](**flags)
            headers = {"Deprecation": "true"} if route.deprecated else {}
            return 200, body, headers

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
        "| Method | Path | Query | Answers as | Deprecated | Description |",
        "|---|---|---|---|---|---|",
    ]
    for route in PUBLIC_API_ROUTES:
        deprecated = "yes" if route.deprecated else "no"
        query_cell = ", ".join(f"`{key}`" for key in route.query) or "—"
        command_line = _twin_command_line(route.twin)
        answers_as = (
            f"`{command_line}`, its `{route.twin_key}` object" if route.twin_key
            else f"`{command_line}`"
        )
        lines.append(
            f"| `{route.method}` | `{route.path}` | {query_cell} | {answers_as} "
            f"| {deprecated} | {route.description} |"
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
