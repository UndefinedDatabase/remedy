"""The public API's route table (DECISION F199 D3).

`PublicApiRoute` and `PUBLIC_API_ROUTES` moved unchanged out of
`packages/orchestration/public_api.py`, as step (2) of that file's boundary on
`docs/system/structure-ledger-v1.md` (structure rule 2); `public_api.py` imports both back by
name, so each import path keeps working and every function there still reads the module-level
`PUBLIC_API_ROUTES`.
"""

from __future__ import annotations

from dataclasses import dataclass


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
        path="/api/v1/execution",
        twin="client.execution",
        description=(
            "What this server offers an execution, read now from its own configuration, as `remedy "
            "client execution --json` prints it: under `roles` each of `planner`, `builder`, "
            "`reviewer` and `repair` with its `default_provider` and `default_model`, whether HTTP "
            "chooses it (`selectable_over_http`), and its `providers`, each with `id`, `available` "
            "(measured: an executable found, the Ollama endpoint answering, an API key set), "
            "`offered_over_http`, `isolation`, `not_offered_reason` and the installed `models`; then "
            "`lanes`, `order_flags`, `budgets`, `verification`, `review_report`, `phases` and "
            "`observability`. It names no secret and no host path. A provider not offered is "
            "refused by the routes that start work with 400 `api_provider_not_offered`."
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
            "holds it; `all_ended_jobs=true` lists every ended job, as `--all-ended-jobs` does. "
            "For a client token it holds only the client's own projects and their jobs."
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
            "command line, and the command's `--path` filter is not offered over HTTP. A client "
            "token reads only a job of one of its projects (403 `api_client_policy_refused`)."
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
            "`since` only a cursor is given. For a client token it lists only what belongs to the "
            "client's own projects."
        ),
    ),
    PublicApiRoute(
        method="GET",
        path="/api/v1/health",
        twin="doctor.health",
        refusals=(("health_failed", 503),),
        description=(
            "Remedy's own health, as `remedy doctor health --json` prints it: each check PASS, "
            "WARN or FAIL with its detail and hint; when a check is FAIL the route answers 503 "
            "with the same body, so a monitor can read the status alone."
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
            "HTTP. Since 1.22 a budget decision answered `extend` starts the job's run at once, and "
            "the answer names that run under `resumed`, or why it could not start under "
            "`resume_refused`; `extend` with no `answer` doubles every limit the stop exhausted."
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
        path="/api/v1/jobs/{job}/stop",
        twin="job.stop",
        body=(("reason", "string"),),
        refusal_default=409,
        refusals=(
            ("invalid_job_id", 404),
            ("job_not_found", 404),
            ("ambiguous_job_id", 400),
        ),
        description=(
            "Stops a job, as `remedy job stop <job> --reason <reason> --json` does, recorded as "
            "coming through `api`: a running job stops at its next safe point (a Pi call in "
            "flight is ended within about a second, another provider's call finishes first, "
            "nothing new starts) and stays resumable, a job that never "
            "started, such as one waiting for its predecessor, ends at once, and a job already "
            "stopped answers the stop it had with `already_stopped`; a completed job is refused "
            "with 409 `job_not_stoppable`, because its result waits for an apply or a decline. "
            "A job id prefix is accepted, and a client token stops only a job of one of its "
            "projects (403 `api_client_policy_refused`)."
        ),
    ),
    PublicApiRoute(
        method="POST",
        path="/api/v1/jobs/{job}/abandon",
        twin="job.abandon",
        body=(("reason", "string"),),
        refusal_default=409,
        refusals=(
            ("invalid_job_id", 404),
            ("job_not_found", 404),
            ("ambiguous_job_id", 400),
        ),
        description=(
            "Ends a job for good, as `remedy job abandon <job> --reason <reason> --json` does, "
            "recorded as coming through `api`: it never runs again and leaves the digest's active "
            "jobs, while its record and evidence stay readable. A job no process runs is "
            "`cancelled` at once; a running one answers `cancel_pending` true and ends `cancelled` "
            "at its next safe point, or right after its final checks when the cancel arrives while "
            "they run, and is never applied; a cancelled one answers `already_cancelled`. A completed job "
            "is refused with 409 `job_not_cancellable` (its result waits for an apply or a "
            "decline), and so is a failed one. A job id prefix is accepted, and a client token "
            "cancels only a job of one of its projects (403 `api_client_policy_refused`)."
        ),
    ),
    PublicApiRoute(
        method="POST",
        path="/api/v1/orders/{order}/cancel",
        twin="client.cancel-order",
        body=(("reason", "string"), ("decline_results", "flag")),
        refusal_default=409,
        refusals=(("order_not_found", 404),),
        description=(
            "Cancels an order a `POST` to `/api/v1/orders` started, as `remedy client cancel-order "
            "<order> --json` does, whatever it is doing: a planning order stops before its next "
            "step and a planner call in flight is ended and writes no plan, each of its jobs is cancelled as "
            "`POST /api/v1/jobs/{job}/abandon` cancels one, no job of it starts afterwards and "
            "nothing of it is applied after the request. `phase` reads `cancelling` while the walk "
            "or a job still runs and `cancelled` once nothing does; `jobs` names what the cancel "
            "did to each job. An applied result stays applied; a result waiting for its apply stays "
            "for the person's decision unless `decline_results` is `true`. A second cancel answers "
            "`already_cancelled` true. A client token cancels only an order of one of its projects "
            "(403 `api_client_policy_refused`)."
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
            "<order> --json` does: `state` reads `running`, `ended` or `lost`, `phase` what the "
            "order is doing (see `order_phases` in `GET /api/v1/interface`), `cancel` its cancel "
            "request or null, `jobs` its jobs, and `answer` "
            "holds what `remedy do` printed once the order is not `running`. A client token "
            "reads only an order whose order file names its projects (403 "
            "`api_client_policy_refused`)."
        ),
    ),
    PublicApiRoute(
        method="POST",
        path="/api/v1/orders",
        twin="client.order",
        body=(("order", "string"), ("no_llm", "flag"), ("new_mission", "flag"),
              ("force_job", "flag"), ("force_mission", "flag"), ("builder_provider", "string"),
              ("reviewer_provider", "string"), ("deadline", "string"), ("order_key", "string"),
              ("capture_review", "flag")),
        starts_order=True,
        description=(
            "Starts an order through the supervisor's own `OrderLauncher`, the way `remedy do "
            "run <options> --no-ui --run-unattended -- order.md` would inside its own folder under the "
            "data root, and answers 202 with its record read exactly as the route above reads "
            "it. `order` is the order file's whole text, header included, and required; "
            "`no_llm`, `new_mission`, `force_job`, `force_mission` and `capture_review` each pass their "
            "`remedy do` flag when `true` (`capture_review` leaves the walk's review report under the "
            "data root's `review_reports`, its id in the answer's `review_report`); `builder_provider`, "
            "`reviewer_provider` and `deadline` each pass their option with their value, and a provider "
            "HTTP does not offer (`claude-cli`, or one that is no provider of its role; see `GET "
            "/api/v1/execution`) is refused before anything starts with 400 `api_provider_not_offered`. "
            "An order whose header names no project, or "
            "one that names a project `select_project` cannot resolve to exactly one, is "
            "refused before anything starts with 409 `api_order_project_unknown`, and one whose "
            "header sets none of `max-cost-usd`, `max-total-tokens`, `max-provider-calls` and "
            "`max-wall-clock-minutes` with 400 `order_file_no_cost_cap`; every other "
            "refusal is `remedy do`'s own, read back only once the order is polled. "
            "`order_key` names the order with a key the client chooses, one to 64 letters, "
            "digits, `.`, `_` or `-`, beginning with a letter or a digit, any other value "
            "answering 400 `api_body_invalid`; an order with a key whose order file an earlier "
            "order of a mission that has not ended still has unfinished jobs for is refused "
            "before anything starts with 409 `order_already_running`, the mission's id under "
            "`mission_id`, unless `new_mission` is `true`, which adds it as one more order to the "
            "repository's one mission, and the record's `order_file` then names the key's file."
        ),
    ),
    PublicApiRoute(
        method="GET",
        path="/api/v1/jobs/{job}/logs",
        twin="doctor.logs",
        query_values=("run",),
        refusals=(("invalid_job_id", 404), ("job_not_found", 404), ("ambiguous_job_id", 400)),
        description=(
            "The operations log's lines of one job, oldest first, as `remedy doctor logs <job> "
            "--json` prints them; `run` keeps the lines of one run of a task. A job id prefix is "
            "accepted when it names one job, a job with no line answers an empty list, and a "
            "client token reads only a job of one of its projects."
        ),
    ),
    PublicApiRoute(
        method="GET",
        path="/api/v1/jobs/{job}/story",
        twin="client.story",
        refusals=(("invalid_job_id", 404), ("job_not_found", 404), ("ambiguous_job_id", 400)),
        description=(
            "One job's run story in closed words a client translates, as `remedy client story "
            "<job> --json` prints it: `order`, `state` and `state_detail`, `next` with the one "
            "next step and the route that takes it, `end` with the way out of a job that is still open "
            "(since 1.21), the five `steps` with the job's tasks under "
            "`building`, `changes`, `numbers` (null where not measured) and `note_open`. Every "
            "word is in the `story` key of `GET /api/v1/interface`. A job id prefix is accepted, "
            "and a client token reads only a job of one of its projects (403 "
            "`api_client_policy_refused`)."
        ),
    ),
    PublicApiRoute(
        method="GET",
        path="/api/v1/now",
        twin="client.now",
        description=(
            "What runs right now, in closed words a client translates, as `remedy client now "
            "--json` prints it (since 1.22): `jobs`, one entry per running job with its `order`, "
            "`project`, `state`, `phase`, `task`, `round`, `worker`, `budget` (`used` and "
            "`limits`), `last_output_s`, `stalled` with its `stall_reason`, and `waiting_on`; "
            "`orders`, the orders that wait with no running job; `model_server`, the local model "
            "server's `state`, its `loaded` models and its `queue`; `workers`; and "
            "`stall_threshold_s`. A value Remedy cannot know is null. Every word is in the "
            "`insight` key of `GET /api/v1/interface`. A client token reads only its own projects' "
            "jobs and orders."
        ),
    ),
    PublicApiRoute(
        method="GET",
        path="/api/v1/jobs/{job}/insight",
        twin="client.insight",
        query_values=("lines",),
        refusals=(("invalid_job_id", 404), ("job_not_found", 404), ("ambiguous_job_id", 400)),
        description=(
            "One job's worker seen from outside, as `remedy client insight <job> --json` prints "
            "it (since 1.22): the job's entry of `GET /api/v1/now`, plus `stream`, the worker's last "
            "`lines` stream lines (default 40, at most 200, already redacted), and `advice`, the "
            "closed words for what the operator can do. Every word is in the `insight` key of "
            "`GET /api/v1/interface`. A job id prefix is accepted, and a client token reads only "
            "a job of one of its projects (403 `api_client_policy_refused`)."
        ),
    ),
    PublicApiRoute(
        method="GET",
        path="/api/v1/jobs/{job}/diff",
        twin="client.diff",
        refusals=(("invalid_job_id", 404), ("job_not_found", 404), ("ambiguous_job_id", 400),
                  ("diff_not_ready", 409), ("diff_unavailable", 409)),
        description=(
            "One ended job's change as git prints it, as `remedy client diff <job> --json` does: "
            "`job`, `state` (`prepared`, `applied`, `declined`, `failed` or `conflict`), `files` "
            "with each file's `path`, `change` (`added`, `modified`, `deleted` or `renamed`), "
            "`added` and `removed` lines, its unified `patch` and `truncated`, and `truncated` "
            "when a patch or the list was cut. A result not yet applied is the job branch "
            "against its base commit, an applied one the commit its apply landed. A job that "
            "has not ended or waits for an answer answers 409 `diff_not_ready`, commits git "
            "no longer has 409 "
            "`diff_unavailable`. A job id prefix is accepted, and a client token reads only a "
            "job of one of its projects (403 `api_client_policy_refused`)."
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
            "refused with 404 `run_not_found`, and a client token reads only a job of one of its "
            "projects (403 `api_client_policy_refused`)."
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
            "`--builder-provider=<value>` and `--reviewer-provider=<value>`, a provider HTTP does not "
            "offer refused with 400 `api_provider_not_offered`; no other option of "
            "`remedy job run` is offered over HTTP. A job id prefix is accepted. A client waits "
            "for the run's end by polling the route above until `state` is not `running`. "
            "Refusals: `invalid_job_id` 404, `job_not_found` 404 (also for a "
            "record that cannot be read), `ambiguous_job_id` 400, `job_already_running` 409, "
            "`api_command_failed` 500 when the run cannot start, and "
            "`api_client_policy_refused` 403 for a client token's job outside its projects."
        ),
    ),
)
