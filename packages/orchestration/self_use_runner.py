"""F258 T002 — carrying a planned self-use job onto the real RUN path.

:mod:`packages.orchestration.self_use_job` plans a curated queue item onto a
:class:`~packages.orchestration.pingpong_job.JobPlan` and deliberately stops
short of running it. This module is the step that runs it: it takes the
planned item through the same builder/reviewer loop, in the same isolated
worktree (or copy, when ``repo_path`` is not a git repository), under the
same budget machinery, every other job already uses —
:func:`packages.orchestration.pingpong_job.run_job` — and stops at the same
normal approval gate every job stops at.

Public API::

    SelfUseRunError: the planned item was already blocked before any task ran
    SELF_USE_ROLE: the role BOTH sides of a self-use run are configured from
    resolve_self_use_role_config() -> RoleConfig, that role with its config read
    parse_order_budget(job_markdown) -> dict, the `Budget:` line an order file
        may declare for itself, or {} when it declares none
    run_next_self_use_item(dest_dir, repo_path=".", queue_path=None, *,
        max_provider_calls=8, max_cost_usd=1.00, max_tasks=1, **run_job_kwargs)
        -> tuple[SelfUseQueueEntry, Path, JobPlan]
        (an unflagged run asks run_job for claude_cli_write_mode
        "allowed-tools" and timeout_sec 600; a declared budget outranks those
        defaults; a caller's own explicit argument outranks everything)

Deliberate absences:
  * REMEDY DELIBERATELY DOES NOT APPLY THE RUN'S RESULT. Applying stays
    behind the ``--approve`` barrier in
    :mod:`packages.orchestration.job_apply`, which never applies by itself;
    this module calls :func:`~packages.orchestration.pingpong_job.run_job`
    and nothing past it — the same stopping point
    :mod:`packages.orchestration.self_use_job`'s own docstring already names
    for planning, one step further down the same path.
  * REMEDY DELIBERATELY DOES NOT MARK A QUEUE ITEM CONSUMED. Exactly as
    :mod:`packages.orchestration.self_use_job` and
    :mod:`packages.orchestration.self_use_queue` before it: consumption is an
    edit the CLOSURE ROUND makes, which DECISION F257 D2 rules, and a run
    that can check itself off is not a gate.
  * Remedy deliberately does not mark a queue item consumed here — see
    above — but it does NOT stay silent about which PROVIDER ran. An
    unflagged ``builder_name``/``reviewer_name`` is resolved via
    :func:`~packages.orchestration.role_config.resolve_role_config`, the
    same seam :mod:`apps.cli.commands.do_cmd` resolves CLI role overrides
    through, so an unflagged self-use run genuinely resolves a real
    configured provider instead of quietly inheriting :func:`run_job`'s own
    raw ``"fake"`` fallback. If that resolution cannot produce a real
    provider, this module REFUSES with :class:`SelfUseRunError` rather than
    substitute a fake one. The fake provider stays reachable only through an
    explicit ``builder_name="fake"`` / ``reviewer_name="fake"`` argument,
    exactly as every other job test already selects it.
  * REMEDY DELIBERATELY DOES NOT RESOLVE THE PRODUCT-DEFAULT BUILDER AND
    REVIEWER ROLES HERE ANY MORE (operator amendment amend0920-selfuse-real,
    DECISION D2). Both sides come from ONE role, :data:`SELF_USE_ROLE`, whose
    built-in default is the configured frontier provider. THE REASON IS
    MEASURED, not preferred: SU-019 to SU-023 — five consecutive closures —
    each planned an item, ran it on the local model and landed no repair at
    all. A self-use run repairs THIS repository against THIS repository's
    review discipline, which is the hardest work the product does, and
    pointing it at the cheapest model made the whole track ceremonial. The
    product default for an ordinary user's job is untouched: this is the one
    path that opts out of it, and `self_use.provider` puts it back.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from packages.core.models import JobBudgets

# _TASK_HEADING_RE is the PARSER'S OWN definition of where an order file's
# prose ends and its tasks begin. parse_order_budget below reads the budget
# declaration out of that prose, so it must agree with parse_job_file about the
# boundary exactly; importing the constant is what makes the two unable to
# drift apart, and is why a private name is reached for here.
from packages.orchestration.pingpong_job import (  # noqa: PLC2701
    _TASK_HEADING_RE,
    JOB_BLOCKED,
    JobPlan,
    run_job,
)
from packages.orchestration.role_config import resolve_role_config
from packages.orchestration.self_use_job import plan_next_self_use_item
from packages.orchestration.self_use_queue import SelfUseQueueEntry

#: Role name -> the run_job() keywords that already count as an explicit
#: override for that role: the label (see
#: packages.orchestration.pingpong_job._resolve_cfg, whose "fake" fallback
#: fires when the label is left None) and the provider-object injection
#: point tests use to substitute a FakeProvider instance directly.
#:
#: THE KEYS ARE THE run_job SIDE OF THE SEAM and they do not change: run_job
#: still takes a builder and a reviewer. What changed is WHERE their runtime
#: configuration comes from — :data:`SELF_USE_ROLE` for both, rather than the
#: `builder` and `reviewer` roles one each.
_ROLE_KWARGS: dict[str, tuple[str, str]] = {
    "builder": ("builder_name", "builder_provider"),
    "reviewer": ("reviewer_name", "reviewer_provider"),
}

#: THE ONE ROLE BOTH SIDES OF A SELF-USE RUN ARE CONFIGURED FROM (operator
#: amendment amend0920-selfuse-real, DECISION D2). Its built-in defaults live
#: in packages/orchestration/role_config.py — provider `claude-cli`, model the
#: alias table's Sonnet alias — and the operator moves it with
#: `self_use.provider` / `self_use.model`.
SELF_USE_ROLE = "self_use"

#: The self-use path's own budget, and it is the PATH's, not the product's
#: (DECISION amend0920-selfuse-real D2). Eight calls is a build round, a review
#: round and two repair rounds with room for a retry — enough for a repair to
#: actually land, where six stopped runs mid-loop. One dollar bounds a closure.
_MAX_PROVIDER_CALLS = 8
_MAX_COST_USD = 1.00

#: The self-use path's own per-provider-call timeout, in seconds (R-1044).
#: run_job's product default is 120 seconds, and three consecutive closures —
#: F277's job 86f628f5e4fb4e0c, F283's 129b3ad7206d4f8d and F278's
#: e7268925db3a4831 — each spent THREE builder attempts of exactly that length
#: and delivered nothing: 3 x 120 seconds of timeout plus the [30, 120] backoff
#: schedule in packages/orchestration/provider_timeouts.py is the 510 seconds
#: each of those runs measured. A self-use call reads this repository's own
#: review discipline and answers against it, which is the longest work the
#: product asks of a provider, so it gets ten minutes rather than two.
_SELF_USE_TIMEOUT_SEC = 600


class _Unset:
    """The keyword was not passed by the caller AT ALL.

    ``None`` cannot carry this meaning: a caller passing ``max_cost_usd=None``
    is asking for no cost ceiling, which is a real choice and must outrank an
    order file's declaration. So the budget keywords default to this sentinel
    instead, and the documented defaults are applied here rather than in the
    signature.
    """

    def __repr__(self) -> str:  # pragma: no cover — diagnostics only
        return "<not passed>"


_UNSET: Any = _Unset()

#: The keys an order file's `Budget:` line may declare, and the type each one
#: is read as. Anything else in that line is a refusal, so a typo in a standing
#: order is loud rather than silently ignored.
_ORDER_BUDGET_KEYS: dict[str, type] = {
    "max_tasks": int,
    "max_provider_calls": int,
    "max_cost_usd": float,
    "timeout_sec": int,
}

#: The declaration's prefix. It sits in the order file's PROSE, before the first
#: `## Task` heading, which is exactly where pingpong_job.parse_job_file stops
#: reading — so the planner never sees it and the runner does.
_ORDER_BUDGET_PREFIX = "Budget:"


def parse_order_budget(job_markdown: str) -> dict[str, int | float]:
    """Read an order file's own budget declaration, or answer ``{}``.

    The declaration is ONE line before the first ``## Task`` heading, of the
    form ``Budget: max_tasks=5, max_provider_calls=40, max_cost_usd=10.00,
    timeout_sec=900``. Every key is optional, the order is free and the
    whitespace is loose. The FIRST such line is the declaration; a later one is
    not read, and neither is one below the first task heading.

    WHY IT LIVES IN THE ORDER FILE (R-1044): the runner's built-in bound — one
    task, eight calls, one dollar — was written for a single-finding repair
    item, and the order tier hands the same runner a five-task standing order
    it cannot begin to fit. The order knows what it costs; the runner does not.

    Raises:
        SelfUseRunError: the line is present but cannot be read. A standing
            order that declares a budget nobody can parse must not fall back
            to the small default and burn money, so this is loud.
    """
    for raw_line in job_markdown.splitlines():
        line = raw_line.strip()
        if _TASK_HEADING_RE.match(line):
            return {}
        if not line.startswith(_ORDER_BUDGET_PREFIX):
            continue
        return _read_budget_declaration(line)
    return {}


def _read_budget_declaration(line: str) -> dict[str, int | float]:
    """The one `Budget:` line, read into a dict or refused by quoting it."""

    def refuse(why: str) -> SelfUseRunError:
        return SelfUseRunError(
            f"the order file's budget line cannot be read ({why}): {line!r}. "
            "Write it as `Budget: max_tasks=5, max_provider_calls=40, "
            "max_cost_usd=10.00, timeout_sec=900`, with every key optional."
        )

    body = line[len(_ORDER_BUDGET_PREFIX):].strip()
    if not body:
        raise refuse("it declares nothing")
    declared: dict[str, int | float] = {}
    for raw_part in body.split(","):
        part = raw_part.strip()
        if not part:
            raise refuse("it holds an empty entry")
        if "=" not in part:
            raise refuse(f"the entry {part!r} is not `key=value`")
        key, _, value = part.partition("=")
        key = key.strip()
        value = value.strip()
        if key not in _ORDER_BUDGET_KEYS:
            known = ", ".join(sorted(_ORDER_BUDGET_KEYS))
            raise refuse(f"{key!r} is not a budget key; the keys are {known}")
        if key in declared:
            raise refuse(f"{key!r} is declared twice")
        try:
            declared[key] = _ORDER_BUDGET_KEYS[key](value)
        except ValueError:
            raise refuse(f"{key}={value!r} is not a number") from None
    return declared


def resolve_self_use_role_config():
    """The ``self_use`` role, with `self_use.provider` / `self_use.model` read.

    :func:`~packages.orchestration.role_config.resolve_role_config` reads no
    config file of its own — it resolves what its caller hands it — so the two
    registered keys are read HERE and handed in as the config-file layer. That
    keeps one rule: a configured value outranks the built-in default, and the
    built-in default is the frontier provider.
    """
    from packages.orchestration.config import get_config

    cfg = get_config()
    overrides: dict[str, str] = {}
    for field_name in ("provider", "model"):
        value = cfg.get(f"{SELF_USE_ROLE}.{field_name}")
        if value:
            overrides[field_name] = str(value)
    return resolve_role_config(SELF_USE_ROLE, config_file=overrides)


class SelfUseRunError(RuntimeError):
    """A planned self-use item cannot be run.

    Raised only when planning itself already blocked the item (an
    unparsable job file — ``no_tasks_found`` or worse) before any task ran.
    A job that blocks DURING execution is not this: it still ran, and its
    ``JobPlan`` is the return value, not an exception — blocking mid-run is
    an ordinary, expected outcome of the normal approval gate, exactly as it
    is for any other job.
    """


def run_next_self_use_item(
    dest_dir: Path,
    repo_path: str = ".",
    queue_path: Path | None = None,
    *,
    max_provider_calls: int | None = _UNSET,
    max_cost_usd: float | None = _UNSET,
    max_tasks: int | None = _UNSET,
    **run_job_kwargs: Any,
) -> tuple[SelfUseQueueEntry, Path, JobPlan]:
    """Plan the queue's next pending item and RUN it to the approval gate.

    Composes two existing seams and adds no new one:
    :func:`~packages.orchestration.self_use_job.plan_next_self_use_item`
    (which already persists the planned ``JobPlan``), then
    :func:`~packages.orchestration.pingpong_job.run_job` on the id it
    returns, with THIS PATH'S OWN budget attached
    (:class:`~packages.core.models.JobBudgets`, ``max_provider_calls`` 8 and
    ``max_cost_usd`` 1.00, both overridable) and an extra ``max_tasks`` cap
    alongside it — a bound written for a run that has to LAND a repair, not
    for the product at large (DECISION amend0920-selfuse-real D2). Every
    ``run_job_kwargs`` entry is forwarded unchanged, so a caller may pass
    ``repair_rounds=`` or any other keyword :func:`run_job` accepts. If the
    caller does not already supply ``builder_name``/``reviewer_name`` (or
    leaves them ``None``), this function resolves BOTH from the ONE
    :data:`SELF_USE_ROLE` via :func:`resolve_self_use_role_config` before
    calling :func:`run_job`, so an unflagged run resolves the configured
    frontier provider rather than :func:`run_job`'s own raw ``"fake"``
    fallback — and never the local model by accident. Each role also gets
    that config's model and effort unless the caller passed them (R-0890).
    An unflagged run also asks for ``claude_cli_write_mode="allowed-tools"``,
    so the builder can actually change a file (R-1043), and for a
    ``timeout_sec`` of :data:`_SELF_USE_TIMEOUT_SEC`, so one real call has
    time to answer (R-1044); a caller that passes either keyword keeps it.

    THE BUDGET IS RESOLVED IN THREE LAYERS, strongest first (R-1044): a
    keyword this caller passed explicitly, then the ``Budget:`` line the order
    file declares for itself (see :func:`parse_order_budget`), then this
    module's own defaults — ``max_provider_calls`` 8, ``max_cost_usd`` 1.00,
    ``max_tasks`` 1 and ``timeout_sec`` 600. When the planned job holds MORE
    tasks than the effective ``max_tasks``, this function refuses BEFORE any
    provider call rather than spend a budget it already knows cannot finish
    the order.

    Answers ``(entry, job_file_path, result)`` — the queue entry that was
    run, the job file :func:`plan_next_self_use_item` rendered it to, and
    the ``JobPlan`` :func:`run_job` returns (``JOB_COMPLETED`` or
    ``JOB_BLOCKED``, never applied). The returned ``JobPlan``'s
    ``execution_config`` states which provider actually ran.

    Raises:
        SelfUseJobError: the queue holds no pending item (propagated
            unchanged from :func:`plan_next_self_use_item`).
        SelfUseRunError: the planned item was already ``JOB_BLOCKED`` before
            any task ran — a curation defect, not a run outcome — OR role
            config resolution for :data:`SELF_USE_ROLE` could not produce a
            usable real provider and none was explicitly supplied (pass
            ``builder_name="fake"`` / ``reviewer_name="fake"`` explicitly to
            run under the fake provider, for tests) — OR the order file's
            ``Budget:`` line cannot be read — OR the planned job holds more
            tasks than this run may execute.
    """
    entry, job_file_path, plan = plan_next_self_use_item(dest_dir, repo_path, queue_path)
    if plan.state == JOB_BLOCKED:
        raise SelfUseRunError(
            f"{entry.id}: planning already blocked it ({plan.error!r}) — "
            "this item cannot be run"
        )
    # R-1044: the order file may declare what it costs. An explicit argument
    # from this caller always wins; otherwise the declaration wins; otherwise
    # this module's default stands.
    declared = parse_order_budget(entry.job_markdown)

    def _resolve(name: str, passed: Any, default: Any) -> Any:
        if not isinstance(passed, _Unset):
            return passed
        if name in declared:
            return declared[name]
        return default

    max_provider_calls = _resolve(
        "max_provider_calls", max_provider_calls, _MAX_PROVIDER_CALLS)
    max_cost_usd = _resolve("max_cost_usd", max_cost_usd, _MAX_COST_USD)
    max_tasks = _resolve("max_tasks", max_tasks, 1)
    # R-1044: an order the run cannot finish is refused before it costs
    # anything. `.agent/selfuse_f279/result_state.txt` is what this prevents:
    # a five-task standing order stopped at `budget_exhausted:max_cost_usd`
    # with all five tasks still pending and $1.37 spent.
    if max_tasks is not None and max_tasks > 0 and len(plan.tasks) > max_tasks:
        raise SelfUseRunError(
            f"{entry.id} has {len(plan.tasks)} tasks but this run may execute "
            f"at most {max_tasks}; declare `Budget: max_tasks={len(plan.tasks)}` "
            "in the order file or pass max_tasks."
        )
    # ONE resolution for BOTH sides: a self-use run's builder and reviewer are
    # the same configured pair (DECISION amend0920-selfuse-real D2), so they
    # cannot drift apart and the reviewer is never weaker than the builder it
    # reviews. Resolved once, outside the loop, so one config read serves both.
    role_cfg = resolve_self_use_role_config()
    for role, (name_kwarg, provider_kwarg) in _ROLE_KWARGS.items():
        if run_job_kwargs.get(name_kwarg) is not None:
            continue
        if run_job_kwargs.get(provider_kwarg) is not None:
            continue  # caller already injected a provider object explicitly
        provider = role_cfg.provider
        if not provider or provider.strip().lower() == "fake":
            raise SelfUseRunError(
                f"{entry.id}: refusing to run unflagged — role config "
                f"resolution for {SELF_USE_ROLE!r} yielded no usable real "
                f"provider ({provider!r}); pass {name_kwarg}='fake' explicitly "
                "to run under the fake provider for tests"
            )
        run_job_kwargs[name_kwarg] = provider
        # R-0890: the provider came from the role config, so its model and effort
        # do too — otherwise the job records an empty model it never ran.
        for field in ("model", "effort"):
            if run_job_kwargs.get(f"{role}_{field}") is None:
                run_job_kwargs[f"{role}_{field}"] = getattr(role_cfg, field)
    # R-1043: a builder with NO WRITE TOOL cannot land a repair, and three
    # consecutive closures recorded `claude_cli_write_mode: none` with source
    # `default` because nothing on this path ever chose one. The builder works
    # in an isolated worktree and its output still passes the human approval
    # gate in packages/orchestration/job_apply.py, so a write tool here widens
    # nothing that was not already gated. The REVIEWER is untouched: its
    # "none" is hard-coded in pingpong_loop._build_provider_evidence.
    if run_job_kwargs.get("claude_cli_write_mode") is None:
        run_job_kwargs["claude_cli_write_mode"] = "allowed-tools"
    # R-1044: two minutes is not enough for one real self-use call — see
    # _SELF_USE_TIMEOUT_SEC above for the three runs that measured it.
    if run_job_kwargs.get("timeout_sec") is None:
        run_job_kwargs["timeout_sec"] = declared.get(
            "timeout_sec", _SELF_USE_TIMEOUT_SEC)
    budgets = JobBudgets(
        max_provider_calls=max_provider_calls, max_cost_usd=max_cost_usd
    ).model_dump(mode="json")
    result = run_job(plan.job_id, budgets=budgets, max_tasks=max_tasks, **run_job_kwargs)
    return entry, job_file_path, result
