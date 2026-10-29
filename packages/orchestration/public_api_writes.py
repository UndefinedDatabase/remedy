"""F253 — the public HTTP API's write routes: the argument list each twin command runs with, and
the refusals a route makes before any command runs.

Moved out of `packages/orchestration/public_api.py` unchanged, as step (1) of that file's boundary
on `docs/system/structure-ledger-v1.md` (structure rule 2, DECISION F205 D6); every consumer
imports these names from here (operator amendment amend1014-luna-mission-fixes D.2).
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from packages.orchestration.public_api_routes import PublicApiRoute


def _decision_resolve_argv(segments: dict[str, str], body: dict[str, Any]) -> list[str]:
    """The command line `remedy decision resolve` is run with: each option as `--name=value`,
    then `--json`, then `--` so that no value is read as an option (DECISION F253 D9 (1))."""
    options = [f"--reason={body['reason']}"] if "reason" in body else []
    options += [f"--answer={answer}" for answer in body.get("answer", [])]
    return ["decision", "resolve", *options, "--json", "--", segments["job"], segments["decision"]]


def _job_decline_argv(segments: dict[str, str], body: dict[str, Any]) -> list[str]:
    """The command line `remedy job decline` is run with (DECISION F253 D11): `--reason` always,
    empty when the body names none, so the command itself refuses it with `missing_argument`
    rather than its parser with no envelope; `--source=api`, so the decline names the door it came
    through; then `--json`, `--` and the job."""
    return ["job", "decline", f"--reason={body.get('reason', '')}", "--source=api", "--json",
            "--", segments["job"]]


def _job_stop_argv(segments: dict[str, str], body: dict[str, Any]) -> list[str]:
    """The command line `remedy job stop` is run with (exec-1017b): `--reason` as the body gives it,
    `--source=api`, so the stop names the door it came through; then `--json`, `--` and the job.
    A running job stops at its next safe point, one that never started ends at once, a stopped one
    answers the stop it already had, and a completed one is refused `job_not_stoppable`."""
    return ["job", "stop", f"--reason={body.get('reason', '')}", "--source=api", "--json",
            "--", segments["job"]]


def _job_cancel_argv(segments: dict[str, str], body: dict[str, Any]) -> list[str]:
    """The command line `remedy job abandon` is run with (exec-1017c): `--reason` as the body gives it,
    `--source=api`, then `--json`, `--` and the job."""
    return ["job", "abandon", f"--reason={body.get('reason', '')}", "--source=api", "--json",
            "--", segments["job"]]


def _job_steer_argv(segments: dict[str, str], body: dict[str, Any]) -> list[str]:
    """The command line `remedy job steer` is run with (DECISION F303 D3 (1)): `--task` as the
    body gives it, `--source=api`, so the note names the door it came through; then `--json`,
    `--`, the job and the note's text, `job steer`'s own positional argument, each passed on
    as sent so the command itself refuses an empty one with `invalid_message`."""
    return ["job", "steer", f"--task={body.get('task', '')}", "--source=api", "--json",
            "--", segments["job"], body.get("text", "")]


def _order_cancel_argv(segments: dict[str, str], body: dict[str, Any]) -> list[str]:
    """The command line `remedy client cancel-order` is run with (exec-1017c): `--reason`,
    `--source=api`, `--decline-results` when the body sets `decline_results`, `--json`, `--`, the order."""
    declines = ["--decline-results"] if body.get("decline_results") else []
    return ["client", "cancel-order", f"--reason={body.get('reason', '')}", "--source=api", *declines,
            "--json", "--", segments["order"]]


class PublicApiWriteRefusal(Exception):
    """A write a route's argument builder refuses before any command runs (DECISION F253 D12)."""

    def __init__(self, status: int, error: str, message: str) -> None:
        super().__init__(message)
        self.status, self.error, self.message = status, error, message


#: The flags of the apply route's body, each passed as its `job apply` option when `true`
#: (DECISION F253 D12).
_JOB_APPLY_FLAGS: tuple[str, ...] = ("commit_auto", "commit_with_history", "push", "skip_blocked")


def _job_apply_argv(segments: dict[str, str], body: dict[str, Any]) -> list[str]:
    """The command line `remedy job apply` is run with (DECISION F253 D12): `--approve` always;
    `--repo` the repository the job's own record names, never one the caller chooses, and the job
    by its full id, so that a prefix is accepted; `--commit` when the body gives one, and each flag
    the body sets `true`; never `--test-command`, which would run a command of the caller's choice.

    A value that names no one job is passed as sent and without `--repo`, and the command refuses
    it `job_not_found` before it touches any repository. A job whose record names no repository
    is refused here with 409 `api_job_repository_unknown`, because `--repo` would otherwise mean
    the supervisor's own working folder. A record that exists and cannot be read is passed on as a
    missing one is, because `load_job_plan_safe` never raises (R-1204).
    """
    from packages.orchestration.data_paths import JobIdError, lookup_job_id
    from packages.orchestration.pingpong_job import load_job_plan_safe

    job, repo = segments["job"], []
    try:
        plan, _degraded = load_job_plan_safe(lookup_job_id(job))
    except JobIdError:
        plan = None
    if plan is not None:
        if not plan.repo_path:
            raise PublicApiWriteRefusal(
                409, "api_job_repository_unknown",
                f"job {plan.job_id}'s record names no repository, so it is not known where to "
                "apply it; nothing was run")
        job, repo = str(plan.job_id), [f"--repo={plan.repo_path}"]
    options = ["--approve", *repo]
    if "commit" in body:
        options.append(f"--commit={body['commit']}")
    options += [f"--{flag.replace('_', '-')}" for flag in _JOB_APPLY_FLAGS if body.get(flag)]
    return ["job", "apply", *options, "--json", "--", job]


def _project_ask_argv(segments: dict[str, str], body: dict[str, Any], *, client: Any = None) -> list[str]:
    """The command line `remedy client ask` is run with (amend1026 C2): `--max-total-tokens`, who asks,
    `--json`, `--`, the project and the question. A client needs `host_tools` (400
    `api_provider_not_offered`), the project in its entry and a cap within its ceiling (403
    `api_client_policy_refused`); the question and the cap are required (400 `api_body_invalid`)."""
    from packages.orchestration.api_clients import client_lists_project
    from packages.orchestration.execution_options import (
        API_PROVIDER_NOT_OFFERED,
        CLI_ONLY_PROVIDERS,
        client_has_host_tools,
    )

    question, cap = str(body.get("question") or ""), body.get("max_total_tokens")
    if not question.strip() or cap is None:
        raise PublicApiWriteRefusal(400, "api_body_invalid", "'question' and 'max_total_tokens' are required")
    if client is not None:
        if not client_has_host_tools(client):
            raise PublicApiWriteRefusal(400, API_PROVIDER_NOT_OFFERED, (
                f"an ask runs the Claude Code CLI: {CLI_ONLY_PROVIDERS['claude-cli']}; nothing was run"))
        if not client_lists_project(client, _project_keys(segments["project"])):
            raise PublicApiWriteRefusal(403, "api_client_policy_refused", (
                f"the client {client.name!r} may not ask about project {segments['project']!r}; nothing was run"))
        if client.max_total_tokens is not None and cap > client.max_total_tokens:
            raise PublicApiWriteRefusal(403, "api_client_policy_refused", (
                f"the client {client.name!r} may set 'max_total_tokens' to at most {client.max_total_tokens}, "
                f"and the ask's is {cap}; nothing was run"))
    return ["client", "ask", f"--max-total-tokens={cap}", f"--asked-by={client.name if client else 'api'}",
            "--json", "--", segments["project"], question]


def _project_keys(selector: str) -> list[str]:
    """The keys the project SELECTOR names answers to in a client's policy: its slug and its id."""
    from packages.orchestration.project_registry import list_projects_readonly

    for project in list_projects_readonly():
        if selector in (project.slug or "", str(project.id)):
            return [project.slug or "", str(project.id)]
    return [selector]


#: The write routes whose builder reads the calling client (amend1026 C2).
_CLIENT_AWARE_ARGV = frozenset({"client.ask"})


def _twin_argv(twin: str, client: Any) -> Callable[[dict[str, str], dict[str, Any]], list[str]]:
    """TWIN's argument builder, bound to CLIENT when it reads the caller (`_CLIENT_AWARE_ARGV`)."""
    builder = _TWIN_ARGV[twin]
    return (lambda segments, body: builder(segments, body, client=client)) if twin in _CLIENT_AWARE_ARGV else builder


def _runner_options(route: Any) -> dict[str, Any]:
    """The keyword options a route hands the command runner: its own `command_timeout`, when it has one."""
    timeout = getattr(route, "command_timeout", None)
    return {} if timeout is None else {"timeout": timeout}


#: Twin command id of a write route to the function that builds the argument list its command
#: runs with, from the route's bound path segments and its checked body (DECISION F253 D9). A
#: builder may raise `PublicApiWriteRefusal` instead (DECISION F253 D12).
_TWIN_ARGV: dict[str, Callable[[dict[str, str], dict[str, Any]], list[str]]] = {
    "decision.resolve": _decision_resolve_argv,
    "job.decline": _job_decline_argv,
    "job.apply": _job_apply_argv,
    "job.stop": _job_stop_argv,
    "job.abandon": _job_cancel_argv,
    "client.cancel-order": _order_cancel_argv,
    "job.steer": _job_steer_argv,
    "client.ask": _project_ask_argv,
}

#: The flags of the order-create route's body, each passed as its `remedy do` option when
#: `true` (DECISION F253 D14 (1)).
_ORDER_CREATE_FLAGS: tuple[str, ...] = ("no_llm", "new_mission", "force_job", "force_mission", "capture_review")

#: The strings of the order-create route's body, each passed as its `remedy do` option with its
#: value (DECISION F253 D14 (1)); `planner_provider` only ever reaches here from a client with
#: `host_tools`, because `remote_provider_refusal` refuses it for every other (DECISION amend1023 D6).
_ORDER_CREATE_STRINGS: tuple[str, ...] = ("builder_provider", "reviewer_provider", "planner_provider", "deadline")


def _order_text_and_options(body: dict[str, Any],
                            client: Any = None) -> tuple[str, list[str]]:
    """The order text and the `remedy do run` options BODY asks for, or `PublicApiWriteRefusal`.

    With a CLIENT (DECISION F253 D16 (5)), an order outside the client's projects or ceilings
    raises 403 `api_client_policy_refused` once its project is resolved.

    DECISION F253 D14 (1), (2): `order` is required. Before anything starts, its text is parsed
    the way `parse_order_file_text` always parses one, so a broken header or an empty order
    refuses with the parser's own token and message; its header's `project` is then resolved
    through `select_project`, exactly as `_order_repo` in `apps/cli/commands/do_cmd.py` resolves
    it for `remedy do`, except a missing or unresolved project REFUSES here rather than falling
    back to the current folder — the supervisor's own working folder is not one this order's
    caller chose, and running the order there is exactly what this refusal prevents. An order
    over several projects has each of them resolved, and a client's policy must list each one
    (R-1244, DECISION F205 D6).
    """
    from packages.orchestration.api_clients import client_order_refusal
    from packages.orchestration.execution_options import (
        API_PROVIDER_NOT_OFFERED,
        http_order_default_options,
        remote_provider_refusal,
    )
    from packages.orchestration.order_file import (
        OrderFileError,
        order_no_cap_message,
        parse_order_file_text,
    )
    from packages.orchestration.project_registry import (
        AmbiguousProjectError,
        InvalidProjectSelectorError,
        ProjectNotFoundError,
        select_project,
    )

    if "order" not in body:
        raise PublicApiWriteRefusal(400, "api_body_invalid", "'order' is required")
    if why := remote_provider_refusal(body, client):
        raise PublicApiWriteRefusal(400, API_PROVIDER_NOT_OFFERED, why)
    order_text = body["order"]
    try:
        order_file = parse_order_file_text(order_text, "order.md")
    except OrderFileError as exc:
        raise PublicApiWriteRefusal(400, exc.error, str(exc))
    if order_file.project is None:
        raise PublicApiWriteRefusal(
            409, "api_order_project_unknown",
            "the order's header names no project, so it is not known where to run it; "
            "nothing was run")
    projects = []
    for selector in order_file.projects:
        try:
            project, _source = select_project(selector, ".")
        except (AmbiguousProjectError, InvalidProjectSelectorError, ProjectNotFoundError):
            raise PublicApiWriteRefusal(
                409, "api_order_project_unknown",
                f"the order's header names the project {selector!r}, which is not "
                "registered as exactly one; nothing was run")
        projects.append(project)
    for project in projects if client is not None else []:
        refusal = client_order_refusal(
            client, (project.slug or "", str(project.id)),
            order_file.max_total_tokens, order_file.max_provider_calls)
        if refusal is not None:
            raise PublicApiWriteRefusal(403, "api_client_policy_refused", refusal)
    # The body passes no cap, so the header must (operator amendment amend1014-luna-mission-fixes
    # B.4): refused here, before anything starts, as `remedy do` refuses it.
    if all(cap is None for cap in (order_file.max_cost_usd, order_file.max_total_tokens,
                                   order_file.max_provider_calls,
                                   order_file.max_wall_clock_minutes)):
        raise PublicApiWriteRefusal(400, "order_file_no_cost_cap", order_no_cap_message("order"))
    options = [f"--{flag.replace('_', '-')}" for flag in _ORDER_CREATE_FLAGS if body.get(flag)]
    options += [f"--{key.replace('_', '-')}={body[key]}" for key in _ORDER_CREATE_STRINGS
                if key in body]
    lead = projects[0]
    options += http_order_default_options(body, client, lead.canonical_repo_path or next(iter(lead.repo_paths), None))
    return order_text, options


def _job_lock_key(job: str) -> str:
    """The job a write locks on: the full id JOB names, or JOB itself when it names no one job,
    so that a prefix and its full id wait for each other (DECISION F253 D9 (1), R-1193)."""
    from packages.orchestration.data_paths import JobIdError, lookup_job_id

    try:
        return lookup_job_id(job)
    except JobIdError:
        return job


def job_project_keys(plan: Any) -> list[str]:
    """The keys a job record answers to in a client's policy: its `project_id` and, when
    `select_project` finds that project, its slug and id; none for a job of no project or a
    record that could not be read (DECISION F253 D17 (1))."""
    from packages.orchestration.project_registry import (
        AmbiguousProjectError,
        InvalidProjectSelectorError,
        ProjectNotFoundError,
        select_project,
    )

    project_id = str(plan.project_id or "") if plan is not None else ""
    keys = [project_id] if project_id else []
    if project_id:
        try:
            project, _source = select_project(project_id, ".")
        except (AmbiguousProjectError, InvalidProjectSelectorError, ProjectNotFoundError):
            pass
        else:
            keys += [project.slug or "", str(project.id)]
    return keys


def _client_write_refusal(client: Any, segments: dict[str, str]) -> str | None:
    """One sentence when CLIENT may not write to the job or the order the path names, else None:
    a job as `_client_job_refusal` reads it, an order as its read is scoped (exec-1017c)."""
    if "job" in segments:
        return _client_job_refusal(client, segments["job"])
    from packages.orchestration.client_scope import client_order_read_refusal

    refusal = client_order_read_refusal(client, segments["order"])
    return None if refusal is None else f"{refusal}; nothing was run"


def _write_lock_key(segments: dict[str, str]) -> str:
    """The key a write waits on: the job's (`_job_lock_key`), the order's own id, or the project's."""
    if "job" in segments:
        return _job_lock_key(segments["job"])
    return f"order:{segments['order']}" if "order" in segments else f"project:{segments.get('project', '')}"


def _client_job_refusal(client: Any, job: str) -> str | None:
    """One sentence ending "; nothing was run" when JOB names a record that is not a job of one of
    CLIENT's projects, else None (DECISION F253 D17 (1)).

    The job is read as `_job_apply_argv` reads it. The keys its record answers to are its
    `project_id` and, when `select_project` finds that project, its slug and id; a job of no
    project has none, so it is outside every client's policy. A value that names no one job is
    passed on, and the command refuses it. A record that exists and cannot be read has no project
    keys, so it is refused, because `load_job_plan_safe` never raises (R-1204).
    """
    from packages.orchestration.api_clients import client_lists_project
    from packages.orchestration.data_paths import JobIdError, lookup_job_id
    from packages.orchestration.pingpong_job import load_job_plan_safe

    try:
        plan, degraded = load_job_plan_safe(lookup_job_id(job))
    except JobIdError:
        return None
    if plan is None and not degraded:
        return None
    if client_lists_project(client, job_project_keys(plan)):
        return None
    return (f"the client {client.name!r} may not act on job {job!r}, which is not a job of one of "
            "its projects; nothing was run")


#: F324: the most repair rounds a body's `repair_rounds` may name.
PUBLIC_API_REPAIR_ROUNDS_MAX = 5


def _body_refusal(route: PublicApiRoute, raw_body: bytes) -> tuple[dict[str, Any] | None, str]:
    """The checked JSON body of a write to ROUTE and an empty sentence, or None and why not; moved
    here from `public_api.py` unchanged (structure rule 2, F324).

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
        elif kinds[key] == "integer":   # amend1026 C2: a whole number above zero, never a flag
            valid, wanted = type(value) is int and value > 0, "a whole number above zero"
        elif kinds[key] == "rounds":    # F324: repair rounds, 0 to PUBLIC_API_REPAIR_ROUNDS_MAX
            valid = type(value) is int and 0 <= value <= PUBLIC_API_REPAIR_ROUNDS_MAX
            wanted = f"a whole number from 0 to {PUBLIC_API_REPAIR_ROUNDS_MAX}"
        else:
            valid = (isinstance(value, list) and all(isinstance(item, str) and item
                                                     for item in value))
            wanted = "a list of non-empty strings"
        if not valid:
            return None, f"'{key}' must be {wanted}"
        if kinds[key] == "string":
            texts = [value]
        elif kinds[key] in ("flag", "integer", "rounds"):
            texts = []
        else:
            texts = value
        if any("\x00" in text for text in texts):
            return None, f"'{key}' must not hold a NUL character"
    return parsed, ""
