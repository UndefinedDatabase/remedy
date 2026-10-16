"""
The write door's request handler — the one module `remedy serve start` binds to its sockets.

`_RemedyHandler` answers two things and nothing else:

  - `POST /api/jobs/<job_id>/commands`, the single write door (F009): bearer token,
    the `X-Remedy-CSRF` header, nonce replay, a per-job rate limit and an audit line for
    every attempt; the supervisor's unix socket (`serve_daemon.socket_handler_class`) and the
    command line's `serve_client` reach it;
  - the public HTTP API under `/api/v1` (F253), through `public_api`.

Every other path answers 404 to a GET that carries the token, 403 to one without it, and 405 to
every other method. The old React cockpit this module once served — its app shell, its static
assets, its auto-build, its token-gated read routes, its event stream and the dashboard builders
behind them — was deleted with the old face (operator amendment amend1015-face-migration,
DECISION amend1015f D19); the module keeps its name until F307 renames it (finding R-1330).
"""

from __future__ import annotations

import hashlib
import json
import re
import secrets
import threading
import time
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from packages.orchestration.public_api import is_public_api_path

# ---------------------------------------------------------------------------
# Loading a job for the door
# ---------------------------------------------------------------------------

def _resolve_evidence_dir(job_id: str) -> Path | None:
    """Find evidence dir for a job — the implementation moved to
    `packages.orchestration.evidence_index.resolve_job_evidence_dir`, so the
    viewer here and the F033 decision doors resolve by ONE rule. The name
    survives because callers import it, including
    `tests/orchestration/test_final_audit_evidence.py`, which imports it from
    `ui_server` directly."""
    from packages.orchestration.evidence_index import resolve_job_evidence_dir
    return resolve_job_evidence_dir(job_id)


def _safe_error(code: int, message: str) -> tuple[int, dict[str, Any]]:
    return code, {"error": message}


def _load_job(job_id_str: str) -> Any:
    """Load a job record by id, return (job, error_tuple)."""
    from packages.orchestration.data_paths import JobIdInvalid, normalize_job_id
    from packages.orchestration.pingpong_job import load_job_plan

    try:
        job_id = normalize_job_id(job_id_str)
    except JobIdInvalid:
        if re.fullmatch(r"[0-9a-fA-F]+", job_id_str):
            return None, _safe_error(404, "job not found")
        return None, _safe_error(400, "invalid job id")
    try:
        job = load_job_plan(job_id)
    except OSError:
        job = None
    if job is None:
        return None, _safe_error(404, "job not found")
    return job, None


# ---------------------------------------------------------------------------
# Command Channel — the single write door (F009 T001)
# ---------------------------------------------------------------------------

#: The double-submit header the POST door requires alongside the bearer token.
#: It carries the server token itself (DECISION F009 D11): there is no cookie to
#: double-submit against, and a cross-site page cannot set a custom header
#: without a preflight this server never grants.
COMMAND_CSRF_HEADER = "X-Remedy-CSRF"

#: Largest command request this door reads, decided from `Content-Length`
#: before a single byte of body is pulled off the socket.
COMMAND_REQUEST_MAX_BYTES = 64 * 1024

#: The one refusal for every command id this door will not accept. Remedy
#: deliberately does NOT distinguish an id that is absent from the catalog from
#: one that exists but is not UI-exposed (DECISION F009 D12): both are "not a
#: command this door accepts", and telling them apart would let a credentialed
#: caller enumerate the CLI surface through the write door.
COMMAND_NOT_EXPOSED_MESSAGE = "command is not available on this channel"

#: The config key that carries this door's minute budget. Named once so the
#: door, its tests and the registry in packages/orchestration/config.py cannot
#: drift apart.
COMMAND_RATE_LIMIT_CONFIG_KEY = "ui.command_rate_limit_per_minute"

#: How long one budget window lasts. DECISION F009 D9 fixes the unit at a
#: minute. The window TUMBLES rather than slides: a client's budget refills in
#: one step, which is the behaviour a client can reason about from a 429 alone.
COMMAND_RATE_WINDOW_SECONDS = 60.0

#: The refusal a client over its budget receives. It mirrors the shape the SSE
#: door's own 429 already uses, so both limits read the same way on the wire.
COMMAND_RATE_LIMIT_MESSAGE = "too many commands for this job"

#: What an effect that RAISED answers (DECISION F009 D18 clause four, D20). The
#: exception's own text never reaches the wire: it is written by code this door
#: does not own and may name a control path the client may not learn.
COMMAND_EFFECT_FAILED_MESSAGE = "command could not be carried out"

#: The `source` every effect dispatched here is attributed to, so a UI stop is
#: told apart from a `remedy job stop` inside the signal (DECISION F009 D20).
COMMAND_EFFECT_SOURCE = "ui"

#: What a `decision.resolve` naming no answerable decision returns (DECISION F009
#: D21). The effect RAN and DECLINED, so this is neither a shape error nor a
#: server fault, and it goes out through `_safe_error` like every other refusal
#: this door issues (DECISION F009 D22, third clause).
COMMAND_DECISION_STATE_MESSAGE = "decision is not open"

#: What a `decision.resolve` whose `args.answer` is blank once stripped returns: a 400
#: on field `answer`, audited `rejected_shape` (R-0685). Written once, a blank answer
#: would resolve the decision with nothing and could never be corrected.
COMMAND_BLANK_ANSWER_MESSAGE = "answer must not be blank"

#: What an id that `_command_is_ui_exposed` admits but no dispatch clause matches
#: returns. DECISION F009 D22 keeps the 501 as a GUARD rather than a placeholder:
#: without it such a request falls off the end of the handler with no response
#: written at all.
COMMAND_NOT_DISPATCHED_MESSAGE = "command is exposed but not dispatched"

#: The event one ACCEPTED command appends to the job's run log, and through it
#: to the F008 SSE stream (DECISION F009 D23). The spelling is the feature file's.
COMMAND_ACCEPTED_EVENT = "command.accepted"

#: What a `patch.approve-hunks` the recorder REFUSED returns. The effect RAN and
#: DECLINED — an unavailable diff, a truncated view, an unknown hunk id — so it is
#: neither a shape error nor a server fault, exactly as `decision.resolve`'s own 409.
#: The refusal's OWN code and message are deliberately not on the wire (DECISION F009
#: D18 and D22): every message this door emits goes through `_safe_error`, and the
#: operator who needs the detail has the CLI door, which is not a network boundary.
COMMAND_HUNK_DECISION_STATE_MESSAGE = "hunk decision was refused"

#: What a `chat.send` for a job that has ended returns (DECISION F264 D2). The effect
#: RAN and DECLINED — no run will ever read the message — so it is the same 409 the
#: other declining effects give, and nothing was written.
COMMAND_CHAT_STATE_MESSAGE = "job has ended and takes no message"

#: What a `job.pause` or `job.unpause` the effect REFUSED returns (DECISION F025 D2).
#: `pause_job_command`/`unpause_job_command` never raise for a refusal — a terminal
#: job state or an unknown task — so this is the 409 sibling of the other declining
#: effects, and the refusal's own `reason` text is deliberately not on the wire, the
#: same restraint `COMMAND_HUNK_DECISION_STATE_MESSAGE` already keeps.
COMMAND_PAUSE_STATE_MESSAGE = "pause or unpause was refused"

#: The ids this door dispatches. Named rather than inlined so that each second call
#: site greps to this line.
JOB_STOP_COMMAND_ID = "job.stop"
#: DECISION F025 D2's pause/unpause pair.
JOB_PAUSE_COMMAND_ID = "job.pause"
JOB_UNPAUSE_COMMAND_ID = "job.unpause"
DECISION_RESOLVE_COMMAND_ID = "decision.resolve"
HUNK_APPROVE_COMMAND_ID = "patch.approve-hunks"
CHAT_SEND_COMMAND_ID = "chat.send"
#: DECISION F015 D3: each exposed job plan edit, mapped to the `plan_editing` command it runs.
#: The id is the catalog's; the backend's name is the same words with underscores.
PLAN_EDIT_COMMAND_IDS: dict[str, str] = {
    "job.plan-edit-task": "plan_edit_task",
    "job.plan-delete-task": "plan_delete_task",
    "job.plan-reorder": "plan_reorder",
    "job.plan-merge-tasks": "plan_merge_tasks",
    "job.plan-split-task": "plan_split_task",
    "job.plan-edit-acceptance": "plan_edit_acceptance",
}

#: What a plan edit missing a usable `args.expected_version` returns: a 400 on that field,
#: refused before the plan is read. Every edit names the version it was made against.
COMMAND_PLAN_VERSION_MESSAGE = "expected_version must be the plan version the edit was made against"

#: DECISION F026 D2: the runtime task edit, through `task_edit_runtime.edit_task_at_runtime`.
JOB_EDIT_TASK_COMMAND_ID = "job.edit-task"

#: What `job.edit-task` missing a usable `args.expected_version` returns: a 400 on that
#: field, refused before the job is read. The edit names the task's own spec version, as
#: `remedy job plan-show` prints it — a DIFFERENT version scheme than the plan edits'
#: `COMMAND_PLAN_VERSION_MESSAGE` above, because the two edits refuse different states.
COMMAND_TASK_VERSION_MESSAGE = (
    "expected_version must be the task's spec version the edit was made against")

#: DECISION F027 D5: the write door's twin of `remedy job veto-task`.
JOB_VETO_TASK_COMMAND_ID = "job.veto-task"

#: DECISION F028 D5: the write door's twins of `remedy job inject`, `job inject-confirm`
#: and `job inject-answer`.
JOB_INJECT_COMMAND_ID = "job.inject"
JOB_INJECT_CONFIRM_COMMAND_ID = "job.inject-confirm"
JOB_INJECT_ANSWER_COMMAND_ID = "job.inject-answer"
JOB_INJECT_COMMAND_IDS = frozenset(
    {JOB_INJECT_COMMAND_ID, JOB_INJECT_CONFIRM_COMMAND_ID, JOB_INJECT_ANSWER_COMMAND_ID})

#: DECISION F029 D4: the write door's twin of `remedy job rerun-subtree`, shared with
#: round 5's browser through `subtree_rerun.rerun_subtree_command`.
JOB_RERUN_SUBTREE_COMMAND_ID = "job.rerun-subtree"

#: DECISION F030 D2's twin of `remedy job steer`: the write door's task-addressed note,
#: through `steering.steer_task_command`.
JOB_STEER_COMMAND_ID = "job.steer"

#: DECISION F041 D4: the write door's preview pair, recorded by
#: `preview_control.request_preview` and handed to the server's own preview worker.
JOB_PREVIEW_START_COMMAND_ID = "job.preview-start"
JOB_PREVIEW_STOP_COMMAND_ID = "job.preview-stop"
JOB_PREVIEW_COMMAND_IDS = frozenset(
    {JOB_PREVIEW_START_COMMAND_ID, JOB_PREVIEW_STOP_COMMAND_ID})

#: DECISION F015 D3: the plan edit refusals, each with its status, its audit outcome and its
#: message. The edit RAN and DECLINED for all but the argument refusals, which are shape
#: errors on field `args`. A version conflict carries the current version, and every other
#: refusal but a lock timeout carries the backend's `detail`, because it names nothing but
#: the plan's own content and the rule the edit broke — a UI must show the human why.
COMMAND_PLAN_CONFLICT_MESSAGE = "the plan changed since this edit was made"
COMMAND_PLAN_STATE_MESSAGE = "the plan is not open for editing"
COMMAND_PLAN_INVALID_MESSAGE = "the edited plan fails the planner's checks"
COMMAND_PLAN_ARGS_MESSAGE = "the plan edit's arguments were refused"

_COMMAND_RATE_LOCK = threading.Lock()
#: (token fingerprint, job id) -> (window start, commands accepted in it).
_COMMAND_RATE_WINDOWS: dict[tuple[str, str], tuple[float, int]] = {}


# Compared as BYTES: `secrets.compare_digest` raises TypeError on a non-ASCII str.
def server_token_matches(supplied_token: Any, expected_token: Any) -> bool:
    """Constant-time equality for the UI server token.

    Both sides arrive from the network — a query parameter on the GET door, a
    header on the POST door — so the comparison must neither leak the token
    through timing nor raise on attacker-chosen bytes. A missing header
    (`None`) is treated as the empty string and never reaches `.encode`.
    """
    supplied = (supplied_token or "").encode("utf-8")
    expected = (expected_token or "").encode("utf-8")
    return secrets.compare_digest(supplied, expected)


# A shape error names the offending field so a client can repair its own request.
def _command_field_error(field: str, message: str) -> tuple[int, dict[str, Any]]:
    return 400, {"error": message, "field": field}


def plan_edit_refusal(code: str, detail: str,
                      current_version: int | None) -> tuple[int, str, dict[str, Any]]:
    """The status, audit outcome and body DECISION F015 D3 rules for one refused plan edit."""
    if code == "version_conflict":
        return 409, "rejected_state", {"error": COMMAND_PLAN_CONFLICT_MESSAGE,
                                       "current_version": current_version}
    if code in ("invalid_args", "unknown_task", "unknown_command"):
        return 400, "rejected_shape", {"error": COMMAND_PLAN_ARGS_MESSAGE, "field": "args",
                                       "detail": detail}
    if code == "invalid_plan":
        return 409, "rejected_state", {"error": COMMAND_PLAN_INVALID_MESSAGE, "detail": detail,
                                       "current_version": current_version}
    if code in ("plan_not_editable", "no_task_plan"):
        return 409, "rejected_state", {"error": COMMAND_PLAN_STATE_MESSAGE, "detail": detail}
    return 500, "rejected_effect", {"error": COMMAND_EFFECT_FAILED_MESSAGE}


#: DECISION F026 D2: the four codes `task_edit_runtime.py` raises that the pre-approval
#: plan editor never does — `task_edit_refusal` answers these itself and hands every
#: other code to `plan_edit_refusal`, whose classes (a stale version, a bad shape, a
#: closed plan) apply unchanged because the runtime edit is `plan_edit_task` underneath.
COMMAND_TASK_STATE_MESSAGE = "the task is not open for a runtime edit"
_TASK_RUNTIME_REFUSAL_CODES = frozenset({
    "job_not_editable", "task_not_editable", "not_a_plan_task", "spec_archive_conflict",
})


def task_edit_refusal(code: str, detail: str,
                      current_version: int | None) -> tuple[int, str, dict[str, Any]]:
    """The status, audit outcome and body DECISION F026 D2 rules for one refused runtime edit."""
    if code in _TASK_RUNTIME_REFUSAL_CODES:
        return 409, "rejected_state", {"error": COMMAND_TASK_STATE_MESSAGE, "detail": detail}
    return plan_edit_refusal(code, detail, current_version)


# The rate limiter has to name the client it counts, and the only name a request
# carries is the secret itself — hence a digest rather than the token.
def token_fingerprint(token: Any) -> str:
    """A stable, non-reversible handle for one server token (DECISION F009 D7).

    Sixteen hex characters are sixty-four bits of SHA-256: far more than enough
    to keep two live tokens apart, and far too few to walk back to the token
    they name. The raw token is never returned, stored or logged by this
    function, which is what lets the limiter's keys appear in memory dumps,
    metrics and — from R9 — audit records without leaking credentials.
    """
    digest = hashlib.sha256((token or "").encode("utf-8")).hexdigest()
    return "tf:" + digest[:16]


def accept_command_under_rate_limit(
    fingerprint: str,
    job_id: str,
    limit: int,
    *,
    now: Any = time.monotonic,
) -> bool:
    """Spend one unit of a (fingerprint, job) minute budget, or refuse.

    The server is threaded, so the window is read and written under one lock:
    two requests arriving together must not both see the last free unit. That
    is the idiom `acquire_sse_slot` uses for the same problem in this module.
    `now` is injected the way `_send_sse_stream` injects it, so a test can
    assert the window's roll instead of waiting a minute out.

    THE WINDOW MAP IS BOUNDED HERE — this is where a reader looking for the
    bound will search. Its key holds a per-run token fingerprint and a job id
    and the process is long-lived, so an unbounded map would be a slow leak
    across a day of restarts and job switches. Every call therefore first drops
    the windows that have expired, which leaves exactly one entry per
    (fingerprint, job) pair seen inside the last window: a live working set,
    not a growing history.
    """
    with _COMMAND_RATE_LOCK:
        moment = now()
        expired = [key for key, (start, _count) in _COMMAND_RATE_WINDOWS.items()
                   if moment - start >= COMMAND_RATE_WINDOW_SECONDS]
        for key in expired:
            del _COMMAND_RATE_WINDOWS[key]
        window = (fingerprint, job_id)
        start, accepted = _COMMAND_RATE_WINDOWS.get(window, (moment, 0))
        if accepted >= limit:
            return False
        _COMMAND_RATE_WINDOWS[window] = (start, accepted + 1)
        return True


# ---------------------------------------------------------------------------
# HTTP Request Handler
# ---------------------------------------------------------------------------

def _validated_clarification_answers(
    args: dict[str, Any], questions: list[dict[str, str]],
) -> dict[str, str] | None:
    """The `answers` a task-plan approval may carry, or None to refuse it.

    DECISION F031 D26. ABSENT means "accept every default": that is DECISION
    F031 D24's original contract and the reading of every client written before
    this form existed, so it stays valid and stays the default.

    PRESENT means the operator chose, and it is then validated the way
    `apps/cli/commands/decision.py::parse_answer_options` validates `--answer`,
    because the CLI is the vocabulary this door mirrors: an unknown question id
    is a spec error there rather than a silent default.

    Remedy deliberately does NOT drop an unknown id and carry on, and a reader
    looking for that leniency should stop here: `apply_clarification_answers`
    would then write `answered_by="default"` for a question the operator really
    answered, and an assumption log that misreports who decided is worse than a
    refused request the client can correct.
    """
    raw = args.get("answers")
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        return None
    known = {str(q.get("id", "")) for q in questions}
    out: dict[str, str] = {}
    for qid, value in raw.items():
        if not isinstance(qid, str) or qid not in known:
            return None
        if not isinstance(value, str):
            return None
        out[qid] = value
    return out


class _RemedyHandler(BaseHTTPRequestHandler):
    """Token-gated API handler with exactly one mutating door.

    POST `/api/jobs/<job_id>/commands` is the single route that accepts a
    UI-initiated change (F009). Every other POST path, and every PUT and
    DELETE, answers 405 — Remedy deliberately exposes no second mutating
    route, so a reader searching for one finds this sentence instead.
    """

    server_token: str = ""
    target_job_id: str = ""
    #: The `source` the door records `job.stop`, `job.pause` and `job.unpause` with:
    #: this door's own word in a bare handler, and `"cli"` in the handler the
    #: `remedy serve start` supervisor binds to its unix socket (DECISION F200 D1 (2)).
    effect_source: str = COMMAND_EFFECT_SOURCE
    #: True only in the supervisor's socket handler: a non-empty `args.source` the
    #: command line sends with those three commands is recorded as given, as its
    #: `--source` option is when the command runs direct (DECISION F200 D3).
    client_names_source: bool = False
    #: The `CommandRunner` that answers a write under `/api/v1` (DECISION F253 D9): set only
    #: on the handlers the `remedy serve start` supervisor binds, so the cockpit's own server
    #: answers every such write 405.
    command_runner: Any = None
    #: The `OrderLauncher` that answers `POST /api/v1/orders` (DECISION F253 D14 (3)): set only
    #: on the handlers the `remedy serve start` supervisor binds, so a handler without one, the
    #: cockpit's own server included, answers that route 405 like every other write it has none
    #: of.
    order_launcher: Any = None
    #: The `RunLauncher` that answers `POST /api/v1/jobs/{job}/run` (DECISION F253 D18 (4)): set
    #: only on the handlers the `remedy serve start` supervisor binds, so a handler without one,
    #: the cockpit's own server included, answers that route 405 like every other write it has
    #: none of.
    run_launcher: Any = None

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        """Suppress default stderr logging."""

    def _effect_source_from(self, args: Any) -> str:
        """The `source` to record: `args.source` where `client_names_source` holds and
        the client sent a non-empty string, this handler's `effect_source` otherwise."""
        source = args.get("source") if isinstance(args, dict) else None
        if self.client_names_source and isinstance(source, str) and source:
            return source
        return self.effect_source

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"

        # F253: the public HTTP API namespace. It takes its token in the
        # Authorization header, never the query, and answers in the command line's
        # envelope.
        if is_public_api_path(path):
            self._send_public_api_get(path, parsed.query)
            return

        # amend1015f D19: the cockpit's read routes are gone. A caller without the
        # token still learns nothing; one with it learns only that the path is not here.
        token = (parse_qs(parsed.query).get("token") or [""])[0]
        if not server_token_matches(token, self.server_token):
            self._send_json(*_safe_error(403, "invalid token"))
            return
        self._send_json(*_safe_error(404, "not found"))

    def do_POST(self) -> None:  # noqa: N802
        # Fail closed: only an unambiguous commands path opens the write door.
        # `path` is read defensively because a request whose line never parsed
        # has none, and such a request must get 405 rather than an exception.
        parsed = urlparse(getattr(self, "path", ""))
        path = parsed.path.rstrip("/") or "/"
        # F253 R-1188: the public HTTP API's own namespace decides its own refusal,
        # in its own envelope, BEFORE the commands door is even considered.
        if is_public_api_path(path):
            if self.command_runner is not None:   # DECISION F253 D9
                self._send_public_api_post(path, parsed.query)
            else:
                self._send_public_api_refused_method("POST", path)
            return
        parts = path.split("/")
        if (len(parts) == 5 and parts[1] == "api" and parts[2] == "jobs"
                and parts[4] == "commands"):
            self._handle_command_submission(parts[3])
            return
        self._send_json(*_safe_error(405, "method not allowed"))

    # The order below is the contract: authentication is decided BEFORE shape,
    # so an unauthenticated caller never learns what this door would accept.
    def _handle_command_submission(self, job_id_str: str) -> None:
        """Authenticate, resolve and validate one UI-submitted command."""
        if not self._bearer_token_accepted():
            # DECISION F009 D14, clause one: a caller who has presented nothing gets a
            # record only where a control directory already exists, and creates none.
            self._audit_attempt(job_id_str, "rejected_token", create=False)
            self._send_json(*_safe_error(403, "invalid token"))
            return
        if not server_token_matches(self.headers.get(COMMAND_CSRF_HEADER),
                                    self.server_token):
            self._audit_attempt(job_id_str, "rejected_csrf", create=False)
            self._send_json(*_safe_error(403, "invalid csrf token"))
            return
        job, load_error = _load_job(job_id_str)
        if load_error:
            self._audit_attempt(job_id_str, "rejected_job", create=True)
            self._send_json(*load_error)
            return
        payload, shape_error = self._read_command_payload()
        if shape_error:
            self._audit_attempt(str(job.job_id), "rejected_shape", create=True)
            self._send_json(*shape_error)
            return
        if not self._command_is_ui_exposed(payload["command"]):
            self._audit_attempt(str(job.job_id), "rejected_command", create=True,
                                payload=payload)
            self._send_json(*_command_field_error(
                "command", COMMAND_NOT_EXPOSED_MESSAGE))
            return
        # DECISION F009 D15: the replay lookup sits HERE — after the exposed-subset
        # check and BEFORE the budget — and a hit spends nothing. D9 limits "the
        # maximum accepted commands" and a replay accepts nothing new: it returns a
        # decision this server already made, so charging for it would penalise the
        # client for the server's own idempotency guarantee, in precisely the
        # retry-after-a-timeout case the nonce exists to serve.
        replayed = self._replayed_command_result(str(job.job_id), payload["client_nonce"])
        if replayed is not None:
            # D15 audits the replay with the ORIGINAL attempt's outcome, and finding
            # R-0636 rules what that token may be: a replay REPEATS an acceptance
            # rather than being one, so `replayed` is its own token. T5_F035 and
            # T9_F167 read this file to count what the door did, and one token for
            # both events would make them indistinguishable to both. R-0636's payer.
            self._audit_attempt(str(job.job_id), "replayed", create=True,
                                payload=payload)
            self._send_json(replayed["status"], replayed["body"])
            return
        # The budget is spent LAST, by a request that has passed every other
        # check (DECISION F009 D13). Counting a request that was going to be
        # refused anyway would let a mid-rollout or simply buggy client lock
        # ITSELF out of a job with malformed bodies — a denial of service
        # produced by the guard rather than prevented by it.
        if not self._rate_limit_admits_command(str(job.job_id)):
            self._audit_attempt(str(job.job_id), "rejected_rate", create=True, payload=payload)
            self._send_json(*_safe_error(429, COMMAND_RATE_LIMIT_MESSAGE))
            return
        # D5 maps `job.stop` to `safe_points.request_stop`; D18 fixes the order of
        # the three writes an ACCEPTED command performs: the effect FIRST, since
        # the body is unknown until it returns; then the `accepted` audit line,
        # since the record of what this door did must not depend on a store whose
        # key the client picks; then the publication LAST, since D8's replay
        # returns the ORIGINAL result and there is none before the other two.
        if payload["command"] == JOB_STOP_COMMAND_ID:
            try:
                accepted_body = self._dispatch_job_stop(str(job.job_id), payload)
            except (OSError, RuntimeError, ValueError, TypeError):
                # D18, clause four: an effect that RAISED is neither `accepted`,
                # which would be false, nor unaudited, which would break D6.
                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            # D18, clause three: BOTH writes below fail SOFT. The stop is already
            # durable, so refusing after the fact would report a stop that really
            # was requested as one that was not.
            self._audit_attempt(str(job.job_id), "accepted", create=True, payload=payload)
            self._publish_command_result(str(job.job_id), payload["client_nonce"],
                                         accepted_body)
            self._emit_command_accepted_event(str(job.job_id), accepted_body)
            self._send_json(200, accepted_body)
            return
        # DECISION F025 D2 maps `job.pause` to `pause_control.pause_job_command`, run
        # with the door's own source. D18's order is unchanged: effect, then the audit
        # line, then the publication. Unlike `job.stop`, the effect itself can DECLINE
        # (a terminal job state, or a task id the plan does not hold) without raising —
        # D2 rules that outcome `refused`, answered 409 and audited `rejected_state`,
        # the same shape `decision.resolve`'s None return already takes.
        if payload["command"] == JOB_PAUSE_COMMAND_ID:
            try:
                accepted_body = self._dispatch_job_pause(job, payload)
            except (OSError, RuntimeError, ValueError, TypeError):
                # D18, clause four: an effect that RAISED is neither `accepted`,
                # which would be false, nor unaudited, which would break D6.
                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            if accepted_body.get("outcome") == "refused":
                self._audit_attempt(str(job.job_id), "rejected_state", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(409, COMMAND_PAUSE_STATE_MESSAGE))
                return
            # D18, clause three: both writes below fail SOFT. The pause is already
            # durable, so refusing after the fact would report a pause that really
            # was requested as one that was not.
            self._audit_attempt(str(job.job_id), "accepted", create=True, payload=payload)
            self._publish_command_result(str(job.job_id), payload["client_nonce"],
                                         accepted_body)
            self._emit_command_accepted_event(str(job.job_id), accepted_body)
            self._send_json(200, accepted_body)
            return
        # DECISION F025 D2 maps `job.unpause` to `pause_control.unpause_job_command`,
        # the reverse of the clause above, under the same rules.
        if payload["command"] == JOB_UNPAUSE_COMMAND_ID:
            try:
                accepted_body = self._dispatch_job_unpause(job, payload)
            except (OSError, RuntimeError, ValueError, TypeError):
                # D18, clause four: an effect that RAISED is neither `accepted`,
                # which would be false, nor unaudited, which would break D6.
                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            if accepted_body.get("outcome") == "refused":
                self._audit_attempt(str(job.job_id), "rejected_state", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(409, COMMAND_PAUSE_STATE_MESSAGE))
                return
            # D18, clause three: both writes below fail SOFT, for the same reason
            # the pause clause above states.
            self._audit_attempt(str(job.job_id), "accepted", create=True, payload=payload)
            self._publish_command_result(str(job.job_id), payload["client_nonce"],
                                         accepted_body)
            self._emit_command_accepted_event(str(job.job_id), accepted_body)
            self._send_json(200, accepted_body)
            return
        # DECISION F041 D4 maps `job.preview-start` and `job.preview-stop` to
        # `preview_control.request_preview`, run with the door's own source, and hands the
        # job id to the server's preview worker. D18's order is unchanged: effect, then the
        # audit line, then the publication. Unlike `job.pause`, the effect never declines —
        # a preview request is recorded whatever the current state, the same reason
        # `job.stop`'s clause above takes no declining branch — so this clause takes
        # `job.stop`'s own D18 order, with no declining branch either.
        if payload["command"] in JOB_PREVIEW_COMMAND_IDS:
            try:
                accepted_body = self._dispatch_job_preview(job, payload)
            except (OSError, RuntimeError, ValueError, TypeError):
                # D18, clause four: an effect that RAISED is neither `accepted`,
                # which would be false, nor unaudited, which would break D6.
                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            # D18, clause three: both writes below fail SOFT. The request is already
            # durable, so refusing after the fact would report a request that really
            # was recorded as one that was not.
            self._audit_attempt(str(job.job_id), "accepted", create=True, payload=payload)
            self._publish_command_result(str(job.job_id), payload["client_nonce"],
                                         accepted_body)
            self._emit_command_accepted_event(str(job.job_id), accepted_body)
            self._send_json(200, accepted_body)
            return
        # DECISION F027 D5 maps `job.veto-task` to `task_veto.veto_task_command`, run with
        # this door's own token fingerprint as the actor. D18's order is unchanged: effect,
        # then the audit line, then the publication. Unlike `job.pause`'s generic 409, the
        # refusal's own `code` and `detail` ride on the wire — `_read_command_payload`
        # already checked the reason's shape, so what reaches here is the job's or the
        # task's own state, exactly what T5_F027.md asks the operator to be told.
        if payload["command"] == JOB_VETO_TASK_COMMAND_ID:
            try:
                accepted_body = self._dispatch_veto_task(job, payload)
            except (OSError, RuntimeError, ValueError, TypeError):
                # D18, clause four: an effect that RAISED is neither `accepted`,
                # which would be false, nor unaudited, which would break D6.
                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            if accepted_body.get("outcome") == "refused":
                self._audit_attempt(str(job.job_id), "rejected_state", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(
                    409, f"{accepted_body['code']}: {accepted_body['detail']}"))
                return
            # D18, clause three: both writes below fail SOFT. The veto is already
            # durable, so refusing after the fact would report a veto that really
            # was requested as one that was not.
            self._audit_attempt(str(job.job_id), "accepted", create=True, payload=payload)
            self._publish_command_result(str(job.job_id), payload["client_nonce"],
                                         accepted_body)
            self._emit_command_accepted_event(str(job.job_id), accepted_body)
            self._send_json(200, accepted_body)
            return
        # DECISION F030 D2 maps `job.steer` to `steering.steer_task_command`, run with
        # channel `cockpit` so the record says which door the note came through, exactly as
        # `chat.send` already does for a job-wide message. D18's order is unchanged: effect,
        # then the audit line, then the publication. As `job.veto-task`'s branch above, the
        # refusal's own `code` and `detail` ride on the wire — `_read_command_payload` already
        # checked the task id's and the message's own shape before the job was read.
        if payload["command"] == JOB_STEER_COMMAND_ID:
            try:
                accepted_body = self._dispatch_steer_task(job, payload)
            except (OSError, RuntimeError, ValueError, TypeError):
                # D18, clause four: an effect that RAISED is neither `accepted`,
                # which would be false, nor unaudited, which would break D6.
                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            if accepted_body.get("outcome") == "refused":
                self._audit_attempt(str(job.job_id), "rejected_state", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(
                    409, f"{accepted_body['code']}: {accepted_body['detail']}"))
                return
            # D18, clause three: both writes below fail SOFT. The note is already
            # sealed on disk, so refusing after the fact would report a note that
            # really was recorded as one that was not.
            self._audit_attempt(str(job.job_id), "accepted", create=True, payload=payload)
            self._publish_command_result(str(job.job_id), payload["client_nonce"],
                                         accepted_body)
            self._emit_command_accepted_event(str(job.job_id), accepted_body)
            self._send_json(200, accepted_body)
            return
        # DECISION F028 D5 maps `job.inject`, `job.inject-confirm` and `job.inject-answer` to
        # `_dispatch_injection`, run with this door's own token fingerprint as the actor.
        # D18's order is unchanged: effect, then the audit line, then the publication. As
        # `job.veto-task`'s branch above, the effect's own refusal `code` and `detail` ride
        # on the wire — `_read_command_payload` already checked each command's own argument
        # shapes before the job was read.
        if payload["command"] in JOB_INJECT_COMMAND_IDS:
            try:
                accepted_body = self._dispatch_injection(job, payload)
            except (OSError, RuntimeError, ValueError, TypeError):
                # D18, clause four: an effect that RAISED is neither `accepted`,
                # which would be false, nor unaudited, which would break D6.
                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            if accepted_body.get("outcome") == "refused":
                self._audit_attempt(str(job.job_id), "rejected_state", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(
                    409, f"{accepted_body['code']}: {accepted_body['detail']}"))
                return
            # D18, clause three: both writes below fail SOFT. The injection is already
            # durable, so refusing after the fact would report an injection that really
            # was requested as one that was not.
            self._audit_attempt(str(job.job_id), "accepted", create=True, payload=payload)
            self._publish_command_result(str(job.job_id), payload["client_nonce"],
                                         accepted_body)
            self._emit_command_accepted_event(str(job.job_id), accepted_body)
            self._send_json(200, accepted_body)
            return
        # DECISION F029 D4 maps `job.rerun-subtree` to `_dispatch_rerun_subtree`, run with
        # this door's own token fingerprint as the actor. D18's order is unchanged: effect,
        # then the audit line, then the publication. As `job.veto-task`'s branch above, the
        # effect's own refusal `code` and `detail` ride on the wire — `_read_command_payload`
        # already checked the argument shapes before the job was read. `needs_confirmation`
        # is NOT a refusal — nothing was touched — so it takes the same 200 `prepared` does.
        if payload["command"] == JOB_RERUN_SUBTREE_COMMAND_ID:
            try:
                accepted_body = self._dispatch_rerun_subtree(job, payload)
            except (OSError, RuntimeError, ValueError, TypeError):
                # D18, clause four: an effect that RAISED is neither `accepted`,
                # which would be false, nor unaudited, which would break D6.
                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            if accepted_body.get("outcome") == "refused":
                self._audit_attempt(str(job.job_id), "rejected_state", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(
                    409, f"{accepted_body['code']}: {accepted_body['detail']}"))
                return
            # D18, clause three: both writes below fail SOFT. A `prepared` rerun is
            # already durable, and a `needs_confirmation` answer touched nothing at
            # all, so refusing after the fact would misreport either.
            self._audit_attempt(str(job.job_id), "accepted", create=True, payload=payload)
            self._publish_command_result(str(job.job_id), payload["client_nonce"],
                                         accepted_body)
            self._emit_command_accepted_event(str(job.job_id), accepted_body)
            self._send_json(200, accepted_body)
            return
        # D5 maps `decision.resolve` to `answer_task_decision` followed by
        # `save_job`; DECISION F009 D21 rules that BOTH are the effect, because
        # the answer is durable only once `save_job` returns. D18's write order
        # above is unchanged: effect, then the audit line, then the publication.
        if payload["command"] == DECISION_RESOLVE_COMMAND_ID:
            try:
                accepted_body = self._dispatch_decision_resolve(job, payload)
            except (OSError, RuntimeError, ValueError, TypeError):
                # D18, clause four: an effect that RAISED is neither `accepted`,
                # which would be false, nor unaudited, which would break D6.
                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            if accepted_body is None:
                # D21, clause three: the effect RAN and DECLINED — the decision
                # is absent or is no longer open, or an absent answer degraded to ""
                # and `answer_task_decision` refused it (R-0685). Nothing changed on disk, so
                # nothing is published and a retry cannot answer it differently.
                self._audit_attempt(str(job.job_id), "rejected_state", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(409, COMMAND_DECISION_STATE_MESSAGE))
                return
            # D18, clause three, re-examined by D21 and standing: both writes
            # below fail SOFT. The answer is already persisted, so refusing
            # after the fact would report an answer that really was written as
            # one that was not.
            self._audit_attempt(str(job.job_id), "accepted", create=True, payload=payload)
            self._publish_command_result(str(job.job_id), payload["client_nonce"],
                                         accepted_body)
            self._emit_command_accepted_event(str(job.job_id), accepted_body)
            self._send_json(200, accepted_body)
            return
        # DECISION F033 D4 maps `patch.approve-hunks` to `record_hunk_decision_from_view`
        # followed by `save_job`, and it RECORDS rather than applies. DECISION F009 D21's
        # rule is unchanged: BOTH are the effect, because the decision is durable only
        # once `save_job` returns. D18's write order above is unchanged too.
        if payload["command"] == HUNK_APPROVE_COMMAND_ID:
            try:
                accepted_body = self._dispatch_approve_hunks(job, payload)
            except (OSError, RuntimeError, ValueError, TypeError):
                # D18, clause four: an effect that RAISED is neither `accepted`,
                # which would be false, nor unaudited, which would break D6.
                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            if accepted_body is None:
                # D21, clause three, applied unchanged: the effect RAN and DECLINED.
                # `record_hunk_decision_from_view` writes NOTHING to `job.metadata` on
                # a refusal, so nothing changed on disk, nothing is published, and a
                # retry of the same decision cannot answer it differently.
                self._audit_attempt(str(job.job_id), "rejected_state", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(
                    409, COMMAND_HUNK_DECISION_STATE_MESSAGE))
                return
            # D18, clause three: both writes below fail SOFT. The decision is already
            # persisted, so refusing after the fact would report a decision that
            # really was recorded as one that was not.
            self._audit_attempt(str(job.job_id), "accepted", create=True, payload=payload)
            self._publish_command_result(str(job.job_id), payload["client_nonce"],
                                         accepted_body)
            self._emit_command_accepted_event(str(job.job_id), accepted_body)
            self._send_json(200, accepted_body)
            return
        # DECISION F264 D2 maps `chat.send` to `steering.record_steering_message`, the
        # one place a steering message is accepted, and it RECORDS: the run reads the
        # message at its next safe point, never inside a call. D18's write order above
        # is unchanged.
        if payload["command"] == CHAT_SEND_COMMAND_ID:
            try:
                accepted_body = self._dispatch_chat_send(job, payload)
            except (OSError, RuntimeError, ValueError, TypeError):
                # D18, clause four: an effect that RAISED is neither `accepted`,
                # which would be false, nor unaudited, which would break D6.
                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            if accepted_body is None:
                # D21, clause three, applied unchanged: the effect RAN and DECLINED,
                # because the job has ended, and nothing was written.
                self._audit_attempt(str(job.job_id), "rejected_state", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(409, COMMAND_CHAT_STATE_MESSAGE))
                return
            # D18, clause three: both writes below fail SOFT. The message is already
            # sealed on disk, so refusing after the fact would report a message that
            # really was recorded as one that was not.
            self._audit_attempt(str(job.job_id), "accepted", create=True, payload=payload)
            self._publish_command_result(str(job.job_id), payload["client_nonce"],
                                         accepted_body)
            self._emit_command_accepted_event(str(job.job_id), accepted_body)
            self._send_json(200, accepted_body)
            return
        # DECISION F015 D3 maps each `job.plan-*` edit to `plan_editing.edit_plan`, one
        # transaction on the stored plan, and D18's write order above is unchanged. A refusal
        # takes the status and outcome `plan_edit_refusal` rules for its code, and nothing was
        # written, so nothing is published. `PlanEditRefused` is caught BEFORE the generic
        # clause, of whose `ValueError` it is a kind.
        if payload["command"] in PLAN_EDIT_COMMAND_IDS:
            from packages.orchestration.plan_editing import PlanEditRefused
            try:
                accepted_body = self._dispatch_plan_edit(job, payload)
            except PlanEditRefused as exc:
                status, outcome, body = plan_edit_refusal(
                    exc.code, exc.detail, exc.current_version)
                self._audit_attempt(str(job.job_id), outcome, create=True, payload=payload)
                self._send_json(status, body)
                return
            except (OSError, RuntimeError, ValueError, TypeError):
                # D18, clause four: an effect that RAISED is neither `accepted`,
                # which would be false, nor unaudited, which would break D6.
                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            # D18, clause three: both writes below fail SOFT. The edit is already
            # persisted, so refusing after the fact would report an edit that really
            # was written as one that was not.
            self._audit_attempt(str(job.job_id), "accepted", create=True, payload=payload)
            self._publish_command_result(str(job.job_id), payload["client_nonce"],
                                         accepted_body)
            self._emit_command_accepted_event(str(job.job_id), accepted_body)
            self._send_json(200, accepted_body)
            return
        # DECISION F026 D2: `job.edit-task` runs `task_edit_runtime.edit_task_at_runtime`,
        # placed directly after the plan edits' clause above and following it exactly — same
        # write order, same refusal handling, same audit calls — with `task_edit_refusal` in
        # place of `plan_edit_refusal`, because the runtime edit is `plan_edit_task` underneath.
        if payload["command"] == JOB_EDIT_TASK_COMMAND_ID:
            from packages.orchestration.plan_editing import PlanEditRefused
            try:
                accepted_body = self._dispatch_edit_task(job, payload)
            except PlanEditRefused as exc:
                status, outcome, body = task_edit_refusal(
                    exc.code, exc.detail, exc.current_version)
                self._audit_attempt(str(job.job_id), outcome, create=True, payload=payload)
                self._send_json(status, body)
                return
            except (OSError, RuntimeError, ValueError, TypeError):
                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,
                                    payload=payload)
                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))
                return
            self._audit_attempt(str(job.job_id), "accepted", create=True, payload=payload)
            self._publish_command_result(str(job.job_id), payload["client_nonce"],
                                         accepted_body)
            self._emit_command_accepted_event(str(job.job_id), accepted_body)
            self._send_json(200, accepted_body)
            return
        # DECISION F200 D4: a command a subclass adds to this door — the `job.run` the
        # supervisor's socket handler accepts — after every clause above. The cockpit's
        # own handler adds none, so the hook answers None there and the guard below stands.
        extra = self._dispatch_extra_command(job, payload)
        if extra is not None:
            status, body, outcome = extra
            self._audit_attempt(str(job.job_id), outcome, create=True, payload=payload)
            if status == 200:
                self._publish_command_result(str(job.job_id), payload["client_nonce"], body)
                self._emit_command_accepted_event(str(job.job_id), body)
            self._send_json(status, body)
            return
        # An id `_command_is_ui_exposed` admitted that no clause above dispatches.
        # DECISION F009 D22: this is a GUARD, not a placeholder — unreachable
        # while every id in the exposed subset has a clause above, and the
        # alternative is a request that gets no response at all.
        self._audit_attempt(str(job.job_id), "not_implemented", create=True, payload=payload)
        self._send_json(*_safe_error(501, COMMAND_NOT_DISPATCHED_MESSAGE))

    def _dispatch_job_stop(self, job_id: str, payload: Any) -> dict[str, Any]:
        """Run `job.stop`'s effect and build the body DECISION F009 D18 rules for it.

        DECISION F009 D20 rules the two arguments no client supplies: `source` is
        this door, and a non-string `reason` degrades to "" rather than raising,
        because D14 types `args` as an object but never types what is inside it.
        """
        from packages.orchestration.safe_points import request_stop
        args = payload.get("args")
        reason = args.get("reason") if isinstance(args, dict) else ""
        signal = request_stop(
            job_id, reason=reason if isinstance(reason, str) else "",
            source=self._effect_source_from(args))
        return {"command": payload["command"], "outcome": "accepted",
                "request_id": signal.request_id}

    def _dispatch_job_preview(self, job: Any, payload: Any) -> dict[str, Any]:
        """Run `job.preview-start` or `job.preview-stop`'s effect and build the body
        DECISION F041 D4 rules for it.

        The door only RECORDS the request — `request_preview` runs no verb; the cockpit's
        preview worker that carried it further was deleted with the old face (amend1015f
        D19). Never declines.
        """
        from datetime import datetime, timezone

        from packages.orchestration.preview_control import request_preview
        action = "start" if payload["command"] == JOB_PREVIEW_START_COMMAND_ID else "stop"
        job_id = str(job.job_id)
        record = request_preview(job_id, action, now=datetime.now(timezone.utc))
        return {"command": payload["command"], "outcome": "accepted",
                "state": record["state"]}

    def _dispatch_job_pause(self, job: Any, payload: Any) -> dict[str, Any]:
        """Run `job.pause`'s effect and build the body DECISION F025 D2 rules for it.

        `task` is `args.task` when it is a non-empty string, `reason` is `args.reason`
        likewise, and both degrade to their absence rather than raising — the same
        rule DECISION F009 D20 gives `job.stop`'s `reason`, because `args` is
        client-supplied and this door does not know any command's argument schema.
        Unlike `job.stop`'s body, `outcome` here is NOT the literal `"accepted"`:
        it is the closed-set token `pause_job_command` itself produced — `requested`
        or `paused` — because that is what a caller needs to act on.
        """
        from packages.orchestration.pause_control import pause_job_command
        args = payload.get("args")
        task = args.get("task") if isinstance(args, dict) else None
        reason = args.get("reason") if isinstance(args, dict) else ""
        result = pause_job_command(
            job, task_id=task if isinstance(task, str) and task else None,
            reason=reason if isinstance(reason, str) else "",
            source=self._effect_source_from(args))
        return {"command": payload["command"], **result}

    def _dispatch_job_unpause(self, job: Any, payload: Any) -> dict[str, Any]:
        """Run `job.unpause`'s effect and build the body DECISION F025 D2 rules for
        it. `task` degrades the same way `_dispatch_job_pause`'s does. `outcome`
        here is one of `released`, `withdrawn`, `parked` or `not_paused` —
        `unpause_job_command`'s own token, not the literal `"accepted"`.
        """
        from packages.orchestration.pause_control import unpause_job_command
        args = payload.get("args")
        task = args.get("task") if isinstance(args, dict) else None
        result = unpause_job_command(
            job, task_id=task if isinstance(task, str) and task else None,
            source=self._effect_source_from(args))
        return {"command": payload["command"], **result}

    def _dispatch_veto_task(self, job: Any, payload: Any) -> dict[str, Any]:
        """Run `job.veto-task`'s effect and build the body DECISION F027 D5 rules for it.

        `args.task_id` and `args.reason` were already checked by
        `_read_command_payload`, so they are read directly rather than degraded — unlike
        `job.pause`'s optional `task`, a veto without either is a shape error the caller
        never reaches this method with. `veto_task_command` never raises for a refusal;
        its own `code` and `detail` ride in the returned dict unchanged, so
        `_handle_command_submission` can put them on the wire, which `job.pause`'s generic
        409 deliberately does not.
        """
        from packages.orchestration.task_veto import veto_task_command
        args = payload["args"]
        result = veto_task_command(
            job, task_id=args["task_id"], reason=args["reason"],
            actor=token_fingerprint(self._supplied_bearer_token()))
        return {"command": payload["command"], **result}

    def _dispatch_steer_task(self, job: Any, payload: Any) -> dict[str, Any]:
        """Run `job.steer`'s effect and build the body DECISION F030 D2 rules for it.

        `args.task_id` and `args.message` were already checked by `_read_command_payload`,
        so they are read directly rather than degraded, exactly as `_dispatch_veto_task`
        reads its own two required fields. `steer_task_command` never raises for a refusal;
        its own `code` and `detail` ride in the returned dict unchanged, so
        `_handle_command_submission` can put them on the wire, which `job.pause`'s generic
        409 deliberately does not. The channel is `cockpit`, so the record says which door
        a note came through, exactly as `_dispatch_chat_send`'s does for a job-wide message.
        """
        from packages.orchestration.steering import steer_task_command
        args = payload["args"]
        result = steer_task_command(
            job, args["task_id"], args["message"], channel="cockpit")
        return {"command": payload["command"], **result}

    def _dispatch_injection(self, job: Any, payload: Any) -> dict[str, Any]:
        """Run one of `job.inject`, `job.inject-confirm` or `job.inject-answer` and build
        the body DECISION F028 D5 (1) rules for it.

        None of the three effects ever raises for a refusal; each one's own `code` and
        `detail` ride in the returned dict unchanged, exactly as `_dispatch_veto_task`'s
        does. `job.inject` and `job.inject-answer` first read the job's budget state
        through `injection_budget_inputs`, DECISION F028 D4 (3)'s shared helper — a
        `TaskInjectionRefused` there is a refusal like any other, not a raised error.
        `job.inject`'s `after` argument is resolved to a planned id by `resolve_after_ref`,
        never by the command line's own resolver, which writes to the terminal.
        """
        from packages.orchestration.task_injection import (
            TaskInjectionRefused,
            answer_injection_shortfall,
            confirm_task_injection,
            draft_task_injection,
            injection_budget_inputs,
            injection_call_fn,
            resolve_after_ref,
        )

        args = payload["args"]
        command = payload["command"]
        actor = token_fingerprint(self._supplied_bearer_token())

        if command == JOB_INJECT_CONFIRM_COMMAND_ID:
            result = confirm_task_injection(job, args["confirm_token"], actor=actor)
            return {"command": command, **result}

        try:
            budgets, counters, config = injection_budget_inputs(job)
        except TaskInjectionRefused as exc:
            return {"command": command, "outcome": "refused", "code": exc.code,
                    "detail": exc.detail}

        if command == JOB_INJECT_COMMAND_ID:
            result = draft_task_injection(
                job, args["text"], call_fn=injection_call_fn(), budgets=budgets,
                counters=counters, config=config, actor=actor,
                after=resolve_after_ref(job, args.get("after")))
        else:                                           # JOB_INJECT_ANSWER_COMMAND_ID
            result = answer_injection_shortfall(
                job, args["draft_id"], args["option"], actor=actor, budgets=budgets,
                counters=counters, config=config)
        return {"command": command, **result}

    def _dispatch_rerun_subtree(self, job: Any, payload: Any) -> dict[str, Any]:
        """Run `job.rerun-subtree`'s effect and build the body DECISION F029 D4 rules for it.

        `args.task_id` was already checked by `_read_command_payload`, so it is read
        directly, unlike `model` and `confirm_cost`, which are optional and degrade to
        ``""`` and ``False`` the same way D14 rules for every other command's optional
        fields. `rerun_subtree_command` never raises: a refusal's own `code` and
        `detail` ride in the returned dict unchanged, exactly as `_dispatch_veto_task`'s
        does, and `needs_confirmation` rides the same way — it is not a refusal, and
        `_handle_command_submission` sends it as a 200 that touched nothing.
        """
        from packages.orchestration.subtree_rerun import rerun_subtree_command
        args = payload["args"]
        return {"command": payload["command"], **rerun_subtree_command(
            job, args["task_id"], model=args.get("model") or "",
            confirm_cost=bool(args.get("confirm_cost")),
            actor=token_fingerprint(self._supplied_bearer_token()))}

    def _dispatch_chat_send(self, job: Any, payload: Any) -> dict[str, Any] | None:
        """Record one steering message for the job. None means the job has ended.

        DECISION F264 D2: the message was already checked by `_read_command_payload`,
        so the only refusal left is the job's state, which the caller answers 409.
        A record that could not be WRITTEN raises `SteeringWriteError`, a
        `ValueError`, which is D18 clause four's `rejected_effect`. The channel is
        `cockpit`, so the record says which door a message came through.
        """
        from packages.orchestration.steering import (
            SteeringError,
            SteeringWriteError,
            record_steering_message,
        )
        args = payload.get("args")
        message = args.get("message") if isinstance(args, dict) else None
        state = job.state.value if hasattr(job.state, "value") else str(job.state)
        try:
            record = record_steering_message(
                str(job.job_id), message, job_state=state, channel="cockpit")
        except SteeringWriteError:
            raise
        except SteeringError:
            return None
        return {"command": payload["command"], "outcome": "accepted",
                "request_id": record["message_id"], "message_id": record["message_id"]}

    def _dispatch_decision_resolve(self, job: Any,
                                   payload: Any) -> dict[str, Any] | None:
        """Answer one decision and PERSIST it. None means the effect declined.

        DECISION F009 D21: `answer_task_decision` and `save_job` are BOTH the
        effect, because the answer is durable only once `save_job` returns, so a
        raise from either is D18 clause four's `rejected_effect`. A None return
        is NOT a failure — the decision is absent or is no longer open, or an
        absent or non-string answer degraded to "", which `answer_task_decision`
        refuses (R-0685) — and the caller answers it 409 and audits it
        `rejected_state`. A blank STRING answer never gets here: it is
        `_read_command_payload`'s 400 on field `answer`.

        DECISION F009 D22: `source` is deliberately NOT passed, so the answer
        takes `answer_task_decision`'s default of `human`. `answer_source` names
        WHO DECIDED over a closed two-value vocabulary that
        `escalation.escalation_assumptions_md` COUNTS, and a person answering
        through the UI is a human; passing this door's own name would land the
        record in neither tally. This is deliberately NOT DECISION F009 D20's
        rule for `request_stop`, whose `source` names the TRANSPORT instead.
        The door's own attribution lives in `commands_audit.jsonl` (D6).

        `decision_id` and `answer` degrade to "" when absent or non-string, for
        the reason D20 gave for `reason`: D14 types `args` as an object and never
        types what is inside it. An empty id matches no record, so the refusal
        path answers it rather than an exception.

        DECISION F031 D24 rules what a `plan:`-prefixed id means here: the door
        approves or rejects the job's PENDING task plan through
        `job_plan.resolve_task_plan_approval`, which DECISION F015 D2 runs inside
        `plan_editing.consume_plan_approval`, and it accepts exactly
        `approve` and `reject` by strict equality — the CLI's own vocabulary at
        `apps/cli/commands/decision.py` — refusing every other answer, and every
        plan that is not pending, with the same None the task-decision path
        returns. `args.answers` is DECISION F031 D26's FORM over
        `payload.clarifications`, and it is OPTIONAL. ABSENT, every open
        clarification takes its own `default_answer` and an operator approving
        from the inbox is ACCEPTING THE DEFAULTS, which is DECISION F031 D24's
        contract unchanged. PRESENT, it is validated by
        `_validated_clarification_answers`, and an unknown question id refuses
        the whole request rather than defaulting one answer silently.

        `--as-mission` is deliberately NOT reachable through this door, and a
        reader searching for it should stop here: F056 makes the mission opt-in
        an explicit flag whose default is NO, so a door that cannot carry the
        flag creates no mission, and silently creating one would be the opposite
        of that default.  The one mission this door does create is DECISION
        F269 D9 (3)'s: an explicit `yes` to a contract remainder decision, whose
        question offered exactly that, starts the follow-up mission, and the
        result carries its id as `follow_up_mission_id`.
        """
        from datetime import datetime, timezone

        from packages.orchestration.escalation import answer_task_decision
        from packages.orchestration.pingpong_job import save_job_plan
        args = payload.get("args")
        args = args if isinstance(args, dict) else {}
        decision_id = args.get("decision_id")
        answer = args.get("answer")
        # DECISION F031 D24: a `plan:`-prefixed id names the TASK PLAN's own
        # approval, so it is dispatched HERE, before `answer_task_decision` —
        # which reads escalation records alone and refuses every id that is not
        # one. This closes the half of DECISION F009 D5 that shipped the
        # extraction without the dispatch (finding R-0693).
        if isinstance(decision_id, str) and decision_id.startswith("plan:"):
            from packages.orchestration.job_plan import open_clarification_questions
            from packages.orchestration.plan_editing import (
                PlanEditRefused,
                consume_plan_approval,
            )
            fp = getattr(job, "task_plan", None)
            if not isinstance(fp, dict) or fp.get("_approval") != "pending":
                return None
            if answer not in ("approve", "reject"):
                return None
            questions = open_clarification_questions(
                fp.get("clarifications_resolved"))
            answers = _validated_clarification_answers(args, questions)
            if answers is None:
                return None
            # DECISION F015 D2: the approval is consumed under the plan-edit lock
            # against the record as it stands NOW, so a plan edit accepted after
            # `_load_job` read this job is approved, never written over. A record
            # that no longer awaits approval declines like any closed decision.
            try:
                consume_plan_approval(
                    job, reason=answer, answers=answers, questions=questions)
            except PlanEditRefused as exc:
                if exc.code != "approval_closed":
                    raise
                return None
            # `save_job` is deliberately NOT called here, and a reader who came
            # looking for it should stop here: `resolve_task_plan_approval`,
            # which `consume_plan_approval` runs, saves on BOTH of its arms, so a
            # second save would write the same object twice. The task-decision
            # path just below DOES call it, because `answer_task_decision` saves
            # nothing itself, and the difference reads as a bug without this.
            return {"command": payload["command"], "outcome": "accepted",
                    "decision_id": str(decision_id)}
        # DECISION F027 D5: a `veto:`-prefixed id names a `replan_proposal` decision
        # (DECISION F027 D4 (1)), so it is dispatched HERE, before `answer_task_decision`
        # — which reads escalation records alone and refuses every id that is not one,
        # exactly the reason the `plan:` branch above is dispatched first. `answered` is
        # returned as the accepted body unchanged; every refusal returns None, the
        # existing 409 `_handle_command_submission` already sends for this method.
        if isinstance(decision_id, str) and decision_id.startswith("veto:"):
            from packages.orchestration.veto_proposal import answer_replan_proposal
            result = answer_replan_proposal(
                job, decision_id, answer if isinstance(answer, str) else "",
                actor=token_fingerprint(self._supplied_bearer_token()))
            if result["outcome"] != "answered":
                return None
            return {"command": payload["command"], **result}
        record = answer_task_decision(
            job, decision_id if isinstance(decision_id, str) else "",
            answer=answer if isinstance(answer, str) else "",
            now=datetime.now(timezone.utc))
        if record is None:
            return None
        save_job_plan(job)
        body = {"command": payload["command"], "outcome": "accepted",
                "decision_id": str(record.get("decision_id", ""))}
        # DECISION F269 D9 (3): a `yes` to a contract remainder decision starts
        # the follow-up mission here as it does at the CLI door, so a cockpit
        # "yes" is never recorded and then silently does nothing; its id rides
        # in the result. Every other answer is recorded and no more.
        from packages.orchestration.mission_contract import (
            start_remainder_follow_up_mission,
        )
        follow_up = start_remainder_follow_up_mission(str(job.job_id), record)
        if follow_up is not None:
            body["follow_up_mission_id"] = follow_up
        return body

    def _dispatch_plan_edit(self, job: Any, payload: Any) -> dict[str, Any]:
        """Apply one job plan edit through `plan_editing.edit_plan` and build its body.

        DECISION F015 D3: `args` less `expected_version` is the backend's own argument
        object, which the backend validates, and a refusal RAISES `PlanEditRefused` for
        the caller to map. The edit log names the editor by this request's token
        fingerprint, the same handle `commands_audit.jsonl` records (DECISION F009 D7).
        """
        from packages.orchestration.plan_editing import edit_plan
        args = dict(payload["args"])
        expected_version = args.pop("expected_version")
        result = edit_plan(
            str(job.job_id), PLAN_EDIT_COMMAND_IDS[payload["command"]], args,
            expected_version=expected_version,
            actor=token_fingerprint(self._supplied_bearer_token()))
        return {"command": payload["command"], "outcome": "accepted",
                "version": result.version, "tasks": [t.id for t in result.plan.tasks]}

    def _dispatch_edit_task(self, job: Any, payload: Any) -> dict[str, Any]:
        """Apply one runtime task edit through `edit_task_at_runtime` (DECISION F026 D2).

        Mirrors `_dispatch_plan_edit` immediately above: `args["task_id"]` is the
        `TaskEntry`'s own id — the id the dashboard and the pause already use, not its
        planned id — and `args["expected_version"]` is the task's own spec version, which
        `_read_command_payload` already checked is a whole number of at least 1. A refusal
        RAISES `PlanEditRefused`, which `_handle_command_submission` maps through
        `task_edit_refusal`. The edit log names the editor by this request's token
        fingerprint, the same handle `commands_audit.jsonl` records (DECISION F009 D7).
        """
        from packages.orchestration.task_edit_runtime import edit_task_at_runtime
        args = payload["args"]
        result = edit_task_at_runtime(
            str(job.job_id), args.get("task_id"), args.get("fields"),
            expected_spec_version=args["expected_version"],
            actor=token_fingerprint(self._supplied_bearer_token()))
        return {"command": payload["command"], "outcome": "accepted", "task_id": result.task_id,
                "state": result.state, "spec_version": result.spec_version,
                "version": result.plan_version, "restored": list(result.restored)}

    def _dispatch_approve_hunks(self, job: Any,
                                payload: Any) -> dict[str, Any] | None:
        """Record one hunk decision and PERSIST it. None means the effect declined.

        DECISION F033 D4: this door RECORDS and never applies, so it writes
        `job.metadata` and touches no repository — which is why
        `packages.orchestration.hunk_apply` is in the import guard's
        `FORBIDDEN_MODULES` although nothing here imports it.

        DECISION F009 D21, applied unchanged: `record_hunk_decision_from_view` and
        `save_job` are BOTH the effect, because the decision is durable only once
        `save_job` returns, so a raise from either is D18 clause four's
        `rejected_effect`. A None return is NOT a failure — the recorder refused —
        and the caller answers it 409 and audits it `rejected_state`, exactly as
        `_dispatch_decision_resolve`'s None does.

        THE REFUSAL'S CODE AND MESSAGE ARE DELIBERATELY NOT RETURNED THROUGH THIS
        DOOR, and a reader who came looking for them should stop here. Every
        message this handler emits goes through `_safe_error`, and both existing
        409s answer with a fixed generic constant; the operator who needs to know
        WHICH refusal it was has the CLI door at `apps/cli/commands/patch.py`,
        which is not a network boundary. That is DECISION F009 D18 and D22 applied
        unchanged, not a new rule, and it mints no DECISION number of its own.

        `task_run`, `approved` and `rejected` degrade instead of raising, for the
        reason DECISION F009 D20 gave for `reason`: D14 types `args` as an object
        and never types what is inside it. `approved` and `rejected` are then
        passed STRAIGHT THROUGH — `decide_hunk_approval` is total on any input at
        all and already accepts the `{id, reason}` wire form
        `docs/roadmap/features/T5_F033.md` writes, so a second validation here
        would give one fault two names.
        """
        from datetime import datetime, timezone

        from packages.orchestration.diff_view_source import DIFF_SCOPE_JOB, build_diff_view
        from packages.orchestration.evidence_index import resolve_job_evidence_dir
        from packages.orchestration.hunk_approval import HunkApprovalRefusal
        from packages.orchestration.hunk_decision_record import record_hunk_decision_from_view
        from packages.orchestration.hunk_ledger import (
            HUNK_STATE_APPROVED,
            HUNK_STATE_PENDING,
            HUNK_STATE_REJECTED,
        )
        from packages.orchestration.pingpong_job import save_job_plan
        args = payload.get("args")
        args = args if isinstance(args, dict) else {}
        task_run = args.get("task_run")
        task_run = task_run if isinstance(task_run, str) else None
        approved = args.get("approved")
        rejected = args.get("rejected")
        # The CANONICAL id, for the reason finding R-0744 records: the evidence index
        # is keyed by the full lowercase hyphenated form and nothing else resolves it.
        evidence_dir = resolve_job_evidence_dir(str(job.job_id))
        view = build_diff_view(evidence_dir, task_id=task_run)
        # BOTH halves of the attempt key come from the ENVELOPE, which is the same key
        # the CLI door composes — so one decision has ONE key whichever door records it.
        view_task_id = view["task_id"]
        result = record_hunk_decision_from_view(
            job,
            task_id=view_task_id if view_task_id is not None else DIFF_SCOPE_JOB,
            attempt=view["source"],
            attempt_view=view,
            approved=approved if isinstance(approved, list) else [],
            rejected=rejected if isinstance(rejected, list) else [],
            now=datetime.now(timezone.utc),
        )
        if isinstance(result, HunkApprovalRefusal):
            return None
        save_job_plan(job)
        states = [entry.state for entry in result.ledger.entries]
        return {"command": payload["command"], "outcome": "accepted",
                "attempt_key": result.attempt_key,
                "approved": states.count(HUNK_STATE_APPROVED),
                "rejected": states.count(HUNK_STATE_REJECTED),
                "pending": states.count(HUNK_STATE_PENDING)}

    def _publish_command_result(self, job_id: str, client_nonce: str,
                                body: dict[str, Any]) -> None:
        """Publish one accepted result under its nonce. NEVER changes the response.

        D18 clause three: a failed publication leaves a client whose retry re-runs
        the command, tolerable only because every effect in D5's table is
        idempotent at its own layer — `request_stop` provably so.
        """
        from packages.orchestration.command_nonce import publish_nonce_result
        try:
            publish_nonce_result(job_id, client_nonce, body, status=200)
        except (OSError, RuntimeError, ValueError, TypeError):   # D18, clause three
            return

    def _emit_command_accepted_event(self, job_id: str,
                                     body: dict[str, Any]) -> None:
        """Announce one accepted command on the job's own event stream.

        DECISION F009 D23: this is D18's FOURTH write and it runs LAST, after
        the publication D18 orders third. A client that sees this frame and
        replays its nonce must find the published result, so emitting first
        would let a fast client race the door into running one effect twice.

        It fails SOFT for D18 clause three's reason: the effect is already
        durable, and a failed notification must not report a command that
        really ran as one that did not.

        `outcome` is a NAMED parameter of `RunLogWriter.log` rather than
        metadata, which is why it survives into `_safe_event_summary`'s
        envelope and reaches the SSE frame at all. The command id rides in
        metadata, where that summary drops it: the stream is the job's own
        channel and DECISION F009 D6 keeps this door's attribution in
        `commands_audit.jsonl`. This is not D6's rejected alternative (b)
        arriving by the back door — that record is per JOB and must outlive a
        run, while this is a live NOTIFICATION and the run log is exactly
        where the stream reads.
        """
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.timeline import append_run_event
        try:
            append_run_event(
                resolve_data_root(), job_id,
                event=COMMAND_ACCEPTED_EVENT,
                metadata={"outcome": "accepted",
                          "command": str(body.get("command", ""))})
        except (OSError, RuntimeError, ValueError, TypeError):   # D23, clause two
            return

    def _audit_attempt(self, job_id: str, outcome: str, *, create: bool,
                       payload: Any = None) -> bool:
        """Write one audited attempt. NEVER changes the response it is recording.

        DECISION F009 D14, clause four: for a rejection a failed audit write changes
        nothing. The refusal this door had already decided is sent unchanged and the
        exception dies here, because a full disk turning a correctly-refused 403 into a 500
        would convert a working guard into a server fault. The accepted case is not ruled
        yet and has no call site while the 501 seam stands.

        The raw token never leaves this method: only its D7 fingerprint is handed over.

        The caught set is spelled out rather than written as `except Exception`, which this
        module is guarded against by
        `tests/orchestration/test_test_runner.py::TestNoBroadExceptAndDegradedSignals`.
        It covers what the writer can actually raise: `OSError` from the filesystem,
        `RuntimeError` — which `safe_points.StopControlError` is — from a containment
        refusal, and `ValueError` / `TypeError` from serialising a payload. Naming
        `RuntimeError` rather than importing the error class keeps the door's import set at
        the one module this round adds.
        """
        from packages.orchestration.command_audit import audit_command_attempt
        body = payload if isinstance(payload, dict) else {}
        try:
            return audit_command_attempt(
                job_id,
                token_fp=token_fingerprint(self._supplied_bearer_token()),
                command=body.get("command", ""),
                args=body.get("args", {}),
                nonce=body.get("client_nonce", ""),
                outcome=outcome,
                create=create,
            )
        except (OSError, RuntimeError, ValueError, TypeError):   # D14, clause four
            return False

    def _dispatch_extra_command(
            self, job: Any, payload: Any) -> tuple[int, dict[str, Any], str] | None:
        """`(status, body, audit outcome)` for a command a subclass adds, else None.

        The cockpit's handler adds no command, so this answers None for every id;
        the supervisor's socket handler overrides it for `job.run` (DECISION F200 D4).
        """
        return None

    def _command_is_ui_exposed(self, command_id: str) -> bool:
        """True when `command_id` is one of the ids the UI door accepts.

        Imported inside the function, the idiom this module already uses for
        the same catalog in `do_run` and `proof_chain`: the
        catalog is a large module and the write door must not pull it in at
        import time.
        """
        from apps.cli.command_catalog import UI_EXPOSED_COMMANDS
        return command_id in UI_EXPOSED_COMMANDS

    def _nonce_is_a_usable_id(self, client_nonce: str) -> bool:
        """True when this nonce may become a filename in the job's control directory.

        The store owns its own character class, so the door asks it rather than keeping
        a second copy of the rule that could drift away from the one that guards the
        path. Imported inside the function, the idiom this door already uses for the
        catalog and the audit writer.
        """
        from packages.orchestration.command_nonce import nonce_is_valid
        return nonce_is_valid(client_nonce)

    def _replayed_command_result(self, job_id: str, client_nonce: str) -> Any:
        """The result already in force for this nonce, or None on a first attempt.

        DECISION F009 D15 keeps this AFTER the credentials on purpose: a lookup placed
        first would answer an unauthenticated caller out of the store and turn a nonce
        into an oracle for another client's response.

        Nothing here opens a file — `command_nonce` owns the store — and that module
        answers a store it cannot read with a miss rather than an exception, so an
        unreadable record costs one re-execution instead of turning this request into a
        500.
        """
        from packages.orchestration.command_nonce import lookup_nonce_result
        return lookup_nonce_result(job_id, client_nonce)

    def _rate_limit_admits_command(self, job_id: str) -> bool:
        """True while this token and this job still hold minute budget.

        The limit is read on every request from the process's configuration,
        which `get_config` loads once and keeps, so a change takes effect
        when the cockpit restarts (R-1100). A value that is not a whole
        number falls back to the registered default rather than raising: a
        typo in `remedy.toml` must not turn every command into a 500, and the
        door has to stay limited while the typo is there.
        """
        from packages.orchestration.config import get_config, get_key_spec
        try:
            limit = int(get_config().get(COMMAND_RATE_LIMIT_CONFIG_KEY))
        except (TypeError, ValueError):
            limit = int(get_key_spec(COMMAND_RATE_LIMIT_CONFIG_KEY).default)
        return accept_command_under_rate_limit(
            token_fingerprint(self._supplied_bearer_token()), job_id, limit)

    def _supplied_bearer_token(self) -> str:
        """The token this request presented in `Authorization`, or the empty string."""
        scheme, _, supplied = (self.headers.get("Authorization") or "").partition(" ")
        return supplied if scheme == "Bearer" else ""

    def _bearer_token_accepted(self) -> bool:
        """True when `Authorization` carries a `Bearer` token matching the server's."""
        supplied = self._supplied_bearer_token()
        if not supplied:
            return False
        return server_token_matches(supplied, self.server_token)

    def _public_api_caller(self) -> tuple[bool, Any]:
        """Who calls under `/api/v1`: `(accepted, client)` (DECISION F253 D16 (3)).

        `(False, None)` for no token and for a token nobody holds; `(True, None)` for the
        server's own token, which is decided first; `(True, client)` for a client token read
        from the operator's file at this call. Only the routes under `/api/v1` use it: the
        cockpit's command door keeps `_bearer_token_accepted`, which refuses a client token.
        """
        from packages.orchestration.api_clients import load_api_clients, match_api_client

        supplied = self._supplied_bearer_token()
        if not supplied:
            return False, None
        if server_token_matches(supplied, self.server_token):
            return True, None
        client = match_api_client(supplied, load_api_clients())
        return (client is not None), client

    def _send_public_api_answer(self, method: str, path: str, status: int,
                                 body: dict[str, Any], headers: dict[str, str],
                                 client_name: str = "") -> None:
        """Ledger one call under the public HTTP API, then send its decided answer.

        CLIENT_NAME is the name of the client whose token the call presented, empty for the
        server's token and for a refused one (DECISION F253 D16 (7)).

        The shared tail of `_send_public_api_get` and `_send_public_api_refused_method`:
        both decide their own `(status, body, headers)` first, so every attempt under this
        namespace, refused or not, appends one line to the call ledger before the answer is
        sent (DECISION F253 D2 (1)). A failed append (DECISION F009 D14 clause four) changes
        nothing in the answer: the exception dies here.
        """
        from packages.orchestration.public_api import append_public_api_call

        error = "" if body.get("ok") else body.get("error", "")
        try:
            append_public_api_call(
                token_fp=token_fingerprint(self._supplied_bearer_token()),
                client=client_name, method=method, path=path, status=status, error=error)
        except OSError:   # DECISION F253 D2 (1), F009 D14 clause four
            pass
        self._send_json(status, body, headers=headers)

    def _send_public_api_get(self, path: str, query: str) -> None:
        """Answer a GET under the public HTTP API namespace (F253, DECISIONs F253 D1 and D2).

        Authentication is decided BEFORE the route, the same order the write door
        uses: an unauthenticated caller must learn nothing about which paths exist.
        """
        from packages.orchestration.public_api import (
            answer_public_api_get,
            public_api_token_refusal,
        )

        accepted, client = self._public_api_caller()
        if not accepted:
            status, body = public_api_token_refusal()
            headers: dict[str, str] = {}
        else:
            status, body, headers = answer_public_api_get(path, query, client)
        self._send_public_api_answer("GET", path, status, body, headers,
                                     client_name=client.name if client else "")

    def _send_public_api_post(self, path: str, query: str) -> None:
        """Answer a POST under the public HTTP API namespace through `command_runner` (DECISION
        F253 D9).

        The token is decided first, before the body is read, so an unauthenticated caller
        starts no child and learns nothing; a body above `COMMAND_REQUEST_MAX_BYTES` is refused
        without being read, and a query string is refused, as no write route takes one.
        """
        from apps.cli.json_envelope import build_error
        from packages.orchestration.public_api import (
            answer_public_api_post,
            public_api_token_refusal,
        )

        headers: dict[str, str] = {}
        accepted, client = self._public_api_caller()
        if not accepted:
            status, body = public_api_token_refusal()
        else:
            declared = self.headers.get("Content-Length") or "0"
            try:
                length = int(declared)
            except ValueError:
                length = -1
            if length < 0 or length > COMMAND_REQUEST_MAX_BYTES:
                status, body = 400, build_error(
                    "api_body_invalid",
                    f"the body must be at most {COMMAND_REQUEST_MAX_BYTES} bytes, "
                    "given by a Content-Length")
            elif query:
                status, body = 400, build_error(
                    "api_query_invalid", f"'{path}' accepts no query string")
            else:
                raw_body = self.rfile.read(length) if length else b""
                start_order = self.order_launcher.start if self.order_launcher is not None else None
                start_run = (
                    (lambda job, options: self.run_launcher.start(
                        job, json_output=True, options=options))
                    if self.run_launcher is not None else None)
                status, body, headers = answer_public_api_post(
                    path, raw_body, self.command_runner.run, start_order, client=client,
                    start_run=start_run)
        self._send_public_api_answer("POST", path, status, body, headers,
                                     client_name=client.name if client else "")

    def _send_public_api_refused_method(self, method: str, path: str) -> None:
        """Answer POST, PUT or DELETE under the public HTTP API namespace (R-1188, DECISION
        F253 D3 (4)).

        The token is decided first (401 `api_token_invalid`), the same order
        `_send_public_api_get` uses, so an unauthenticated caller learns nothing before
        authenticating; only once the token is accepted does the namespace answer its own
        405 `api_method_not_allowed`.
        """
        from packages.orchestration.public_api import (
            public_api_method_refusal,
            public_api_token_refusal,
        )

        accepted, client = self._public_api_caller()
        if not accepted:
            status, body = public_api_token_refusal()
        else:
            status, body = public_api_method_refusal()
        self._send_public_api_answer(method, path, status, body, {},
                                     client_name=client.name if client else "")

    def _read_command_payload(self) -> tuple[Any, Any]:
        """Return `(payload, None)` for a well-formed body, else `(None, error)`."""
        try:
            length = int(self.headers.get("Content-Length"))
        except (TypeError, ValueError):
            return None, _command_field_error("body", "request body required")
        if length <= 0:
            return None, _command_field_error("body", "request body required")
        if length > COMMAND_REQUEST_MAX_BYTES:
            return None, _command_field_error("body", "request body too large")
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            return None, _command_field_error("body", "request body is not valid JSON")
        if not isinstance(payload, dict):
            return None, _command_field_error("body", "request body must be a JSON object")

        command = payload.get("command")
        if not isinstance(command, str) or not command:
            return None, _command_field_error("command", "command must be a non-empty string")
        client_nonce = payload.get("client_nonce")
        if not isinstance(client_nonce, str) or not client_nonce:
            return None, _command_field_error(
                "client_nonce", "client_nonce must be a non-empty string")
        # DECISION F009 D15: the nonce becomes a FILENAME in the job's control directory,
        # so its character class is the guard — the same `_ID_RE` that already validates
        # the job segment of that same path. A nonce that fails it is the shape error the
        # field already has, which means the same 400 and the same audited
        # `rejected_shape`: D14's closed outcome vocabulary gains no token for it.
        if not self._nonce_is_a_usable_id(client_nonce):
            return None, _command_field_error(
                "client_nonce",
                "client_nonce must be 1-64 characters of letters, digits, '-' or '_'")
        # `args` absent is valid and means the empty object.
        args = payload.get("args", {})
        if not isinstance(args, dict):
            return None, _command_field_error("args", "args must be a JSON object")
        # R-0685: a blank answer is a SHAPE error, refused before any decision is read,
        # so an OPEN decision is never answered "not open". An ABSENT or non-string
        # answer still degrades to "" in `_dispatch_decision_resolve`, as D14 rules.
        answer = args.get("answer")
        if (command == DECISION_RESOLVE_COMMAND_ID and isinstance(answer, str)
                and not answer.strip()):
            return None, _command_field_error("answer", COMMAND_BLANK_ANSWER_MESSAGE)
        # DECISION F264 D2: an unusable steering message is a SHAPE error on field
        # `message`, refused before the job's state is read, for R-0685's reason.
        if command == CHAT_SEND_COMMAND_ID:
            from packages.orchestration.steering import SteeringError, normalize_steering_text
            try:
                normalize_steering_text(args.get("message"))
            except SteeringError as exc:
                return None, _command_field_error("message", str(exc))
        # DECISION F027 D5: a veto names its task by a non-empty string and its reason by
        # `task_veto.validate_veto_reason`'s own shape, both refused BEFORE the job is
        # read — the schema-level refusal T5_F027.md asks for, the same restraint the
        # steering message above keeps for R-0685's reason.
        if command == JOB_VETO_TASK_COMMAND_ID:
            from packages.orchestration.task_veto import TaskVetoRefused, validate_veto_reason

            task_id = args.get("task_id")
            if not isinstance(task_id, str) or not task_id:
                return None, _command_field_error(
                    "task_id", "task_id must be a non-empty string")
            try:
                validate_veto_reason(args.get("reason"))
            except TaskVetoRefused as exc:
                return None, _command_field_error("reason", exc.detail)
        # DECISION F030 D2: a steer names its task by a non-empty string, refused before its
        # own message is checked, itself refused before the job is read, the same two-field
        # order the veto above keeps for T5_F027.md's reason.
        if command == JOB_STEER_COMMAND_ID:
            from packages.orchestration.steering import SteeringError, normalize_steering_text

            task_id = args.get("task_id")
            if not isinstance(task_id, str) or not task_id:
                return None, _command_field_error(
                    "task_id", "task_id must be a non-empty string")
            try:
                normalize_steering_text(args.get("message"))
            except SteeringError as exc:
                return None, _command_field_error("message", str(exc))
        # DECISION F028 D5: an injection command names its own fields' shapes, refused
        # BEFORE the job is read, for R-0685's reason above.
        if command == JOB_INJECT_COMMAND_ID:
            from packages.orchestration.task_injection import (
                TaskInjectionRefused,
                validate_injection_text,
            )

            try:
                validate_injection_text(args.get("text"))
            except TaskInjectionRefused as exc:
                return None, _command_field_error("text", exc.detail)
            after = args.get("after")
            if after is not None and (not isinstance(after, str) or not after):
                return None, _command_field_error(
                    "after", "after must be a non-empty string when given")
        if command == JOB_INJECT_CONFIRM_COMMAND_ID:
            confirm_token = args.get("confirm_token")
            if not isinstance(confirm_token, str) or not confirm_token:
                return None, _command_field_error(
                    "confirm_token", "confirm_token must be a non-empty string")
        if command == JOB_INJECT_ANSWER_COMMAND_ID:
            from packages.orchestration.task_injection import SHORTFALL_OPTIONS

            draft_id = args.get("draft_id")
            if not isinstance(draft_id, str) or not draft_id:
                return None, _command_field_error(
                    "draft_id", "draft_id must be a non-empty string")
            if args.get("option") not in SHORTFALL_OPTIONS:
                return None, _command_field_error(
                    "option", f"option must be one of {', '.join(SHORTFALL_OPTIONS)}")
        # DECISION F029 D4: a rerun names its task by a non-empty string, its model
        # override by a string when given, and `confirm_cost` by a bool when given,
        # each refused BEFORE the job is read, for R-0685's reason above.
        if command == JOB_RERUN_SUBTREE_COMMAND_ID:
            task_id = args.get("task_id")
            if not isinstance(task_id, str) or not task_id:
                return None, _command_field_error(
                    "task_id", "task_id must be a non-empty string")
            model_arg = args.get("model")
            if model_arg is not None and not isinstance(model_arg, str):
                return None, _command_field_error(
                    "model", "model must be a string when given")
            confirm_cost_arg = args.get("confirm_cost")
            if confirm_cost_arg is not None and not isinstance(confirm_cost_arg, bool):
                return None, _command_field_error(
                    "confirm_cost", "confirm_cost must be a bool when given")
        # DECISION F015 D3: a plan edit names the version it was made against, as a whole
        # number, or it is a shape error refused before the plan is read.
        version = args.get("expected_version")
        if command in PLAN_EDIT_COMMAND_IDS and (
                not isinstance(version, int) or isinstance(version, bool) or version < 1):
            return None, _command_field_error("expected_version", COMMAND_PLAN_VERSION_MESSAGE)
        # DECISION F026 D2: a runtime task edit names the task's own spec version, as a
        # whole number, or it is a shape error refused before the job is read — the same
        # check the plan edits run above, against the task's version scheme instead.
        if command == JOB_EDIT_TASK_COMMAND_ID and (
                not isinstance(version, int) or isinstance(version, bool) or version < 1):
            return None, _command_field_error("expected_version", COMMAND_TASK_VERSION_MESSAGE)
        return {"command": command, "client_nonce": client_nonce, "args": args}, None

    def do_PUT(self) -> None:  # noqa: N802
        # `path` is read defensively, the way `do_POST` reads it, for the same reason.
        parsed = urlparse(getattr(self, "path", ""))
        path = parsed.path.rstrip("/") or "/"
        if is_public_api_path(path):  # F253 R-1188
            self._send_public_api_refused_method("PUT", path)
            return
        self._send_json(*_safe_error(405, "method not allowed"))

    def do_DELETE(self) -> None:  # noqa: N802
        # `path` is read defensively, the way `do_POST` reads it, for the same reason.
        parsed = urlparse(getattr(self, "path", ""))
        path = parsed.path.rstrip("/") or "/"
        if is_public_api_path(path):  # F253 R-1188
            self._send_public_api_refused_method("DELETE", path)
            return
        self._send_json(*_safe_error(405, "method not allowed"))

    def _send_json(self, code: int, data: dict[str, Any],
                   headers: dict[str, str] | None = None) -> None:
        body = json.dumps(data, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)
