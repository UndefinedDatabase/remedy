"""F075 T003a — the live gauntlet runner: it EXECUTES, it never judges.

The evaluator (:mod:`packages.orchestration.gauntlet_evaluator`) keeps sole
authority over what "flawless" means. This module's whole job is to produce the
evidence that evaluator already knows how to read — the same
``gauntlet_run_version: 1`` bytes the dry-run fixtures carry — by driving each
frozen order through Remedy's EXISTING mission path and writing down what
happened.

Per order, in manifest order:

* a FRESH isolated data root, set through ``REMEDY_DATA_DIR`` — the same
  environment variable the product already resolves — so nothing a run does can
  reach the operator's real registry. Earned 2026-07-23: during F081 both
  worker tests and reviewer verification wrote stray projects into the real
  root, which is why the real root is hashed BEFORE and AFTER every single run
  and both digests land in the run's evidence as the criterion's own facts.
* the order's budget: ``max_iterations`` becomes the loop's ``LoopLimits``,
  ``max_tokens`` and ``max_wall_seconds`` go through the existing
  ``REMEDY_BUDGET_*`` config keys rather than a second budget mechanism.
* execution through ``create_mission`` -> ``plan_mission`` -> ``run_mission``,
  the same three verbs ``remedy mission`` drives. **The runner adds no second
  execution mechanism**, and every seam it passes defaults to production.

**Remedy deliberately does NOT let the runner absorb a product failure.** A
raise from inside ``run_mission`` is caught at the CAMPAIGN level and recorded
as a crashed — therefore failed — run, which is bookkeeping. It is never
converted into a success, and the harness never supplies the resilience the
product is supposed to demonstrate: see
:mod:`packages.orchestration.gauntlet_injection` for the boundary the loop
still lacks and the three injection classes that wait on it.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import time
from collections.abc import Callable
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from packages.orchestration.era_integrity import DEFECT_FINDING_CLASSES
from packages.orchestration.gauntlet_evidence import (
    DOD_RESULT_FILENAME,
    GAUNTLET_RUN_VERSION,
    RUN_FILENAME,
)
from packages.orchestration.gauntlet_injection import (
    RunOutcomeFacts,
    build_injectors,
    injection_json,
)
from packages.orchestration.gauntlet_orders import GauntletOrder

#: Environment keys the runner sets per run. All of them already exist — the
#: runner configures the product, it does not extend it.
ENV_DATA_ROOT = "REMEDY_DATA_DIR"
ENV_MAX_TOKENS = "REMEDY_BUDGET_MAX_TOTAL_TOKENS"
ENV_MAX_WALL_MINUTES = "REMEDY_BUDGET_MAX_WALL_CLOCK_MINUTES"

#: Where a run keeps its isolated data root, inside its own evidence directory
#: so the evidence and the world it ran in stay together.
ISOLATED_ROOT_DIRNAME = "data"

#: Where the run's own copy of the sample project is materialised. A COPY, per
#: run, inside the run's own directory: the operator's tree is never a mission
#: workspace, and two runs can never see each other's edits (R-0189).
WORKSPACE_DIRNAME = "workspace"

#: The digest of a data root that does not exist. Named rather than "" so the
#: before/after comparison is between two real answers.
ABSENT_ROOT_DIGEST = "sha256:absent"

#: Recorded when the loop measured no token usage. The run.json then carries NO
#: ``tokens`` key at all: absence is honest, a zero would be a claim (R-0178).
TOKENS_UNMEASURED = "unmeasured"

#: The terminal a run gets when it raised out of the harness rather than
#: reaching one of the loop's own terminals. Not green, and named as what it is.
TERMINAL_RUNNER_CRASHED = "runner_crashed"


# ---------------------------------------------------------------------------
# Host-state isolation
# ---------------------------------------------------------------------------

def _manifest_line(path: Path, relpath: str) -> str:
    """One file's metadata row: relpath, size, mtime_ns. No content is read."""
    try:
        stat = path.stat()
    except OSError as exc:  # unreadable is a fact about the tree, not a crash
        return f"{relpath}\t<unreadable: {exc.errno}>"
    return f"{relpath}\t{stat.st_size}\t{stat.st_mtime_ns}"


def data_root_digest(root: Path) -> str:
    """One digest over the METADATA MANIFEST of every file under a data root.

    The manifest is the sorted set of ``relpath\\tsize\\tmtime_ns`` lines.
    Paths are included and sorted, so a file that MOVES changes the digest as
    surely as a file that is written — "byte-untouched" has to mean the tree,
    not a bag of contents.

    The honest contract: this detects a file being ADDED, REMOVED, MOVED,
    RESIZED or RE-TIMESTAMPED. It does NOT detect a content edit that forges
    an identical size AND mtime_ns. That is the deliberate trade of R-0199:
    the criterion's threat model is the harness ACCIDENTALLY writing into the
    operator's real root, not an adversary covering tracks — and the previous
    content-hashing definition read ~143 GB per call (394.8 s measured, ~2.9 TB
    per 10-run campaign) to answer a question about accidents.

    The ``meta-sha256:`` prefix is load-bearing: a digest recorded under the
    old content-hashing definition can never compare equal to one recorded
    under this one, so a before/after pair can never straddle the change and
    read as "untouched".
    """
    if not root.exists():
        return ABSENT_ROOT_DIGEST
    if root.is_file():
        lines = [_manifest_line(root, root.name)]
    else:
        lines = sorted(
            _manifest_line(path, str(path.relative_to(root)))
            for path in root.rglob("*") if path.is_file())
    manifest = "\n".join(lines).encode("utf-8")
    return "meta-sha256:" + hashlib.sha256(manifest).hexdigest()


@contextmanager
def isolated_environment(data_root: Path, order: GauntletOrder):
    """Point the product at ``data_root`` under the order's budget, then restore.

    The config cache is reset on the way in AND on the way out: a cached config
    from before the swap would quietly outlive it, and the next run would
    inherit the previous run's world — which is the pollution this whole
    criterion is about.
    """
    from packages.orchestration.config import reset_config

    wall_minutes = max(1, math.ceil(order.budget["max_wall_seconds"] / 60))
    overrides = {
        ENV_DATA_ROOT: str(data_root),
        ENV_MAX_TOKENS: str(order.budget["max_tokens"]),
        ENV_MAX_WALL_MINUTES: str(wall_minutes),
    }
    saved = {key: os.environ.get(key) for key in overrides}
    os.environ.update(overrides)
    reset_config()
    try:
        yield data_root
    finally:
        for key, previous in saved.items():
            if previous is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = previous
        reset_config()


# ---------------------------------------------------------------------------
# The production verbs, injectable so tests can run without a provider
# ---------------------------------------------------------------------------

def materialise_sample_project(run_dir: Path,
                               template_dir: Path | None = None) -> Path:
    """Copy the frozen template into this run's own workspace and commit it.

    A git repository with one baseline commit, because a mission's work is a
    DIFF against something: without a baseline there is nothing for "no file
    outside the touched module changed" to be measured from. Build droppings
    are not copied — they are not the project.
    """
    import shutil
    import subprocess

    from packages.orchestration.gauntlet_orders import (
        TEMPLATE_IGNORED_DIRS,
        default_template_dir,
    )

    source = template_dir or default_template_dir()
    workspace = run_dir / WORKSPACE_DIRNAME
    shutil.copytree(source, workspace,
                    ignore=shutil.ignore_patterns(*TEMPLATE_IGNORED_DIRS))
    env = {**os.environ, "GIT_AUTHOR_NAME": "remedy-gauntlet",
           "GIT_AUTHOR_EMAIL": "gauntlet@remedy.invalid",
           "GIT_COMMITTER_NAME": "remedy-gauntlet",
           "GIT_COMMITTER_EMAIL": "gauntlet@remedy.invalid"}
    for argv in (["git", "init", "-q"],
                 ["git", "add", "-A"],
                 ["git", "commit", "-q", "-m", "baseline: the sample project"]):
        subprocess.run(argv, cwd=str(workspace), env=env, check=True,
                       capture_output=True)
    return workspace


def _default_make_project(name: str, slug: str,
                          repo_path: Path | None = None) -> str:
    from packages.orchestration.project_registry import RemyProject, save_project

    project = RemyProject(name=name, slug=slug,
                          repo_paths=[str(repo_path)] if repo_path else [],
                          canonical_repo_path=str(repo_path) if repo_path else None)
    save_project(project)
    return str(project.id)


def _default_plan_call_fn() -> Callable[[str, int], str] | None:
    from packages.orchestration.intake import make_structured_call_fn
    from packages.orchestration.mission_plan_schema import MissionPlanDraft

    return make_structured_call_fn(MissionPlanDraft)


def _default_move_call_fn() -> Callable[[str, int], str] | None:
    """The orchestrator role's call_fn — the SAME factory ``remedy mission run`` uses."""
    from packages.orchestration.intake import make_structured_call_fn
    from packages.orchestration.orchestrator_move_schema import OrchestratorMove
    from packages.orchestration.role_config import resolve_orchestrator_model

    return make_structured_call_fn(
        OrchestratorMove, model=resolve_orchestrator_model())


def _default_execute_fn(max_cycles: int,
                        repo_root: Path | None = None) -> Callable[..., Any]:
    """Bind the order's cycle budget and this run's checkout to the execute seam.

    The gauntlet is the ONE caller allowed past the F046 rollout cap (R-0187),
    and it says so here, in one place, with the order's own number. The repo
    root is the run's OWN materialised copy (R-0189), so the DoD checks run
    against the mission's world and never against the operator's tree.
    """
    from packages.orchestration.orchestrator_loop import execute_dispatched_job

    def _execute(job: Any) -> Any:
        return execute_dispatched_job(job, experiment_max_cycles=max_cycles,
                                      worktree_root=repo_root)

    return _execute


def _default_dispatch() -> Callable[..., Any]:
    """How a job is created for a milestone — run_mission's own default.

    Named explicitly so the injection driver has a production callable to
    decorate. Passing it is identical to passing nothing.
    """
    from packages.orchestration.mission_state import continue_mission

    return continue_mission


def _default_update_dossier(root: Path | None = None) -> Callable[..., Any]:
    """The per-iteration dossier refresh — run_mission's own default."""
    from packages.orchestration.orchestrator_loop import update_mission_dossier

    def refresh(project_id: str, mission_id: str, mission: Any) -> Any:
        return update_mission_dossier(project_id, mission_id, mission, root)

    return refresh


@dataclass
class RunnerDeps:
    """Every product verb the runner calls, defaulting to the production one.

    A dataclass of callables rather than module-level monkeypatching: the tests
    hand over doubles at the call site, and production never learns that tests
    exist.
    """

    make_project: Callable[..., str] = _default_make_project
    create_mission: Callable[..., Any] = None  # type: ignore[assignment]
    plan_mission: Callable[..., Any] = None  # type: ignore[assignment]
    run_mission: Callable[..., Any] = None  # type: ignore[assignment]
    load_mission: Callable[..., Any] = None  # type: ignore[assignment]
    plan_call_fn: Callable[[], Callable[[str, int], str] | None] = _default_plan_call_fn
    move_call_fn: Callable[[], Callable[[str, int], str] | None] = _default_move_call_fn
    #: The two seams only the injection driver needs. Production defaults, so
    #: wrapping one changes what happens at that seam and nothing else.
    #: How the run's own copy of the sample project is created (R-0189).
    materialise: Callable[..., Path] = None  # type: ignore[assignment]
    dispatch_fn: Callable[[], Callable[..., Any]] = _default_dispatch
    update_dossier_fn: Callable[[], Callable[..., Any]] = _default_update_dossier
    #: How a dispatched job is RUN, bound to the order's own cycle budget
    #: (R-0187) and this run's checkout (R-0189). Returns the loop's execute
    #: seam; the production default is the existing multi-cycle executor.
    execute_fn: Callable[..., Callable[..., Any]] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.create_mission is None:
            from packages.orchestration.mission_state import create_mission

            self.create_mission = create_mission
        if self.plan_mission is None:
            from packages.orchestration.mission_compiler import plan_mission

            self.plan_mission = plan_mission
        if self.run_mission is None:
            from packages.orchestration.orchestrator_loop import run_mission

            self.run_mission = run_mission
        if self.load_mission is None:
            from packages.orchestration.mission_state import load_mission

            self.load_mission = load_mission
        if self.execute_fn is None:
            self.execute_fn = _default_execute_fn
        if self.materialise is None:
            self.materialise = materialise_sample_project


# ---------------------------------------------------------------------------
# Reading back what a run left behind, inside its own isolated root
# ---------------------------------------------------------------------------

def collect_postmortems(data_root: Path) -> list[dict[str, Any]]:
    """Every F010 postmortem the run wrote, as the evidence schema wants them."""
    records: list[dict[str, Any]] = []
    for path in sorted(data_root.rglob("postmortem.json")):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            # An unreadable postmortem is itself an unclassified failure, and
            # saying so is the point of the no-unknown-postmortems criterion.
            records.append({"scope": "unreadable", "failure_class": "",
                            "detail": f"unreadable postmortem at {path.name}"})
            continue
        if isinstance(body, dict):
            records.append({"scope": str(body.get("scope", "")),
                            "failure_class": str(body.get("failure_class", "")),
                            "detail": str(body.get("raw_reason", ""))[:400]})
    return records


def collect_open_decisions(mission: Any) -> list[dict[str, Any]]:
    """Decisions still waiting on a human across the mission's jobs."""
    from packages.orchestration.escalation import open_task_decisions
    from packages.orchestration.storage import load_job_safe

    open_records: list[dict[str, Any]] = []
    for link in getattr(mission, "job_links", ()) or ():
        try:
            from uuid import UUID

            job, _ = load_job_safe(UUID(str(link.job_id)))
        except (ValueError, OSError):
            continue
        if job is None:
            continue
        for record in open_task_decisions(job):
            open_records.append({
                "decision_id": str(record.get("decision_id", "")),
                "question": str(record.get("question", ""))[:400],
            })
    return open_records


def collect_era_defects(entries: list[Any]) -> list[dict[str, Any]]:
    """Era-defect classes the loop refused a move over, read off the ledger.

    The loop already refuses to advance on a flagged handback (F070); the
    refusal reason names the class. Reading it here rather than re-detecting
    keeps one author for the judgement.
    """
    defects: list[dict[str, Any]] = []
    for entry in entries:
        body = entry.to_json() if hasattr(entry, "to_json") else entry
        outcome = body.get("outcome") if isinstance(body, dict) else None
        detail = str((outcome or {}).get("detail", ""))
        for kind in DEFECT_FINDING_CLASSES:
            if kind in detail:
                defects.append({"kind": kind, "detail": detail[:400],
                                "finding_class": DEFECT_FINDING_CLASSES[kind]})
    return defects


def _template_digest() -> str:
    """The frozen template's digest, or "" if it cannot be read.

    Never raises: a run that could not digest its own world still writes its
    evidence, and an empty string is visibly not a digest.
    """
    from packages.orchestration.gauntlet_orders import template_tree_digest

    try:
        return template_tree_digest()
    except OSError:
        return ""


def _resolved_cycles(entries: list[Any]) -> list[str]:
    """The cycle resolutions the loop recorded, read back off the ledger.

    The loop writes `cycles=<n>/<source>` (plus `OVER-CAP`) into every dispatch
    outcome; collecting them here keeps the run's evidence honest without the
    runner re-deriving anything.
    """
    seen: list[str] = []
    for entry in entries:
        body = entry.to_json() if hasattr(entry, "to_json") else entry
        detail = str(((body or {}).get("outcome") or {}).get("detail", ""))
        for part in detail.split():
            if part.startswith("cycles=") and part not in seen:
                seen.append(part)
    return seen


def measure_tokens(entries: list[Any]) -> dict[str, int] | None:
    """Token actuals summed off the ledger, or ``None`` when nothing was measured.

    ``None`` is not zero. A run whose provider reported no usage did not spend
    nothing — it reported nothing, and the run.json says that by carrying no
    ``tokens`` key at all (R-0178: the matrix must not understate cost).
    Both spellings count: ``input_tokens``/``output_tokens``, then ``prompt_tokens``/``completion_tokens`` (R-0407).
    """
    total_in = total_out = 0
    measured = False
    for entry in entries:
        body = entry.to_json() if hasattr(entry, "to_json") else entry
        usage = (body.get("cost") or {}).get("usage") if isinstance(body, dict) else None
        if not isinstance(usage, dict):
            continue
        measured = True
        total_in += int(usage.get("input_tokens") or usage.get("prompt_tokens") or 0)
        total_out += int(usage.get("output_tokens") or usage.get("completion_tokens") or 0)
    return {"in": total_in, "out": total_out} if measured else None


def latest_gate_result(mission: Any) -> dict[str, Any] | None:
    """The stored DoD verdict of the mission's most recent job, if the gate ran."""
    from packages.orchestration.dod_gate import load_gate_result

    for link in reversed(list(getattr(mission, "job_links", ()) or ())):
        try:
            stored = load_gate_result(str(link.job_id))
        except (OSError, ValueError):
            stored = None
        if stored is not None:
            return stored
    return None


# ---------------------------------------------------------------------------
# One order
# ---------------------------------------------------------------------------

@dataclass
class OrderOutcome:
    """What running one order produced, before anyone judges it."""

    order_id: str
    run_dir: Path
    terminal_status: str
    crashed: str = ""
    body: dict[str, Any] = field(default_factory=dict)


def run_order(order: GauntletOrder, *, campaign_root: Path, real_data_root: Path,
              deps: RunnerDeps | None = None,
              index: int = 1) -> OrderOutcome:
    """Execute ONE order in its own isolated world and write its evidence.

    The real data root is hashed before and after — outside the isolated
    environment, so the digests describe the operator's world rather than the
    run's — and both land in ``run.json`` whatever happens, including when the
    run crashes. A crash is a failed run with evidence, never a missing one.
    """
    from packages.orchestration.orchestrator_loop import LoopLimits

    deps = deps or RunnerDeps()
    run_dir = campaign_root / f"run-{index:02d}-{order.id}"
    run_dir.mkdir(parents=True, exist_ok=True)
    data_root = run_dir / ISOLATED_ROOT_DIRNAME

    before = data_root_digest(real_data_root)
    started = time.monotonic()
    terminal = ""
    crashed = ""
    entries: list[Any] = []
    mission: Any = None
    injectors: list[Any] = []
    gate: dict[str, Any] | None = None
    # Bound BEFORE the try (R-0180). The crash path can itself fail — a
    # collector reading a half-written root, a disk that has gone away — and an
    # unbound `body` at the hash-after line would raise NameError over the top
    # of the real error, losing the only account of what went wrong.
    body: dict[str, Any] = _minimal_body(order, before)
    # F082 T003b: which model served which role, filled in as each call_fn is
    # built and read back out into the evidence body. Bound BEFORE the try for
    # the same R-0180 reason as `body`, so the crash path still records what
    # was resolved before the crash. A role this seam cannot observe stays
    # None: an invented model is the exact class of lie F082 exists to prevent,
    # and the same honesty that keeps `repair_rounds` None rather than 0.
    # The builder is never observable here — `orchestrator_loop.py::
    # execute_dispatched_job` constructs `OllamaBuilder()` itself, so no value
    # reaches this seam at all. It is recorded as an absence on purpose.
    models: dict[str, str | None] = {
        "planner": None, "orchestrator": None, "builder": None,
    }

    try:
        with isolated_environment(data_root, order):
            workspace = deps.materialise(run_dir)
            project_id = deps.make_project(f"gauntlet {order.id}", order.id,
                                           workspace)
            mission = deps.create_mission(project_id, order.goal)
            # R-0197: the order declares its shape, so the compiler is told
            # it. One milestone of headroom, because a compiler that finds a
            # genuine prerequisite should be able to say so — what it may not
            # do is turn a one-milestone order into seven and spend the
            # budget rediscovering that (attempt 02, Finding A).
            plan_call = deps.plan_call_fn()
            models["planner"] = getattr(plan_call, "resolved_model", None)
            deps.plan_mission(project_id, mission.id, plan_call,
                              max_milestones=len(order.milestones) + 1)
            move_call = deps.move_call_fn()
            models["orchestrator"] = getattr(move_call, "resolved_model", None)
            seams = build_injectors(
                order.injections,
                call_fn=move_call,
                dispatch=deps.dispatch_fn(),
                update_dossier=deps.update_dossier_fn(),
            )
            injectors = seams.injectors
            # Remedy deliberately does NOT name the provider here, so these
            # rows reach evidence unlabelled (DECISION F105 D13). The CLI site
            # can name Ollama because its call_fn is always
            # `make_structured_call_fn`; this call_fn arrives through `deps`, a
            # seam whose purpose is being substituted, so a hardcoded label
            # would write a guess into evidence. An empty label already means
            # "the caller did not name it", which is what happened.
            result = deps.run_mission(
                mission.id,
                LoopLimits(max_iterations=order.budget["max_iterations"]),
                project_id=project_id,
                call_fn=seams.call_fn,
                dispatch=seams.dispatch,
                update_dossier=seams.update_dossier,
                execute=deps.execute_fn(order.budget["max_cycles"], workspace),
            )
            terminal = str(getattr(result, "terminal", ""))
            entries = list(getattr(result, "entries", []) or [])
            # Reloaded so the record reflects everything the run wrote.
            mission = deps.load_mission(project_id, mission.id)
            body = _evidence_body(order, terminal, time.monotonic() - started,
                                  entries, mission, injectors, before,
                                  data_root, models)
            gate = latest_gate_result(mission)
    except Exception as exc:  # a crashed run is a FAILED run, with evidence
        crashed = f"{type(exc).__name__}: {exc}"
        terminal = terminal or TERMINAL_RUNNER_CRASHED
        gate = None
        try:
            # Re-entered on purpose: the collectors read through the product's
            # own path resolution, and outside isolation that path is the
            # operator's real root — the one thing this runner must never touch.
            with isolated_environment(data_root, order):
                body = _evidence_body(order, terminal,
                                      time.monotonic() - started,
                                      entries, mission, injectors, before,
                                      data_root, models)
        except Exception as collect_exc:  # R-0180: the fallback keeps the run
            body = _minimal_body(order, before)
            body["terminal_status"] = terminal
            body["postmortems"] = [{
                "scope": "job", "failure_class": "",
                "detail": f"collecting this run's evidence also failed: "
                          f"{type(collect_exc).__name__}: {collect_exc}"}]
        body["postmortems"] = list(body["postmortems"]) + [{
            "scope": "job", "failure_class": "",
            "detail": f"the run raised out of the harness: {crashed}"}]

    body["data_root_hash_after"] = data_root_digest(real_data_root)
    (run_dir / RUN_FILENAME).write_text(
        json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if gate is not None:
        (run_dir / DOD_RESULT_FILENAME).write_text(
            json.dumps(gate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return OrderOutcome(order_id=order.id, run_dir=run_dir,
                        terminal_status=terminal, crashed=crashed, body=body)


def _minimal_body(order: GauntletOrder, before: str) -> dict[str, Any]:
    """The least evidence a run can leave and still be judged.

    Every list empty rather than absent, so the schema holds and the evaluator
    reads a real — if bare — run instead of malformed bytes.
    """
    return {
        "gauntlet_run_version": GAUNTLET_RUN_VERSION,
        "order_id": order.id,
        "kind": order.kind,
        "terminal_status": TERMINAL_RUNNER_CRASHED,
        "wall_seconds": 0.0,
        "operator_interventions": [],
        "data_root_hash_before": before,
        "postmortems": [],
        "open_decisions": [],
        "era_defects": [],
        "injections": [],
        "evidence_links": {},
        "tokens_source": TOKENS_UNMEASURED,
    }


def _evidence_body(order: GauntletOrder, terminal: str, wall: float,
                   entries: list[Any], mission: Any, injectors: list[Any],
                   before: str, data_root: Path,
                   models: dict[str, str | None] | None = None,
                   ) -> dict[str, Any]:
    """The recorded-schema body — the same bytes the dry-run evaluator judges.

    ``data_root`` is passed rather than re-read from the environment: this is
    called once from inside the run's isolation and once from the crash path,
    and a body that guessed its own root could read the operator's.
    """
    postmortems = collect_postmortems(data_root)
    body: dict[str, Any] = {
        "gauntlet_run_version": GAUNTLET_RUN_VERSION,
        "order_id": order.id,
        "kind": order.kind,
        "terminal_status": terminal,
        "wall_seconds": round(wall, 3),
        # The runner issues no command after the start command: it never reads
        # stdin and never prompts. The empty list is a measured fact, not a hope.
        "operator_interventions": [],
        "data_root_hash_before": before,
        "postmortems": postmortems,
        "open_decisions": collect_open_decisions(mission) if mission else [],
        "era_defects": collect_era_defects(entries),
        # The disposition is read off what the product DID: its terminal, and
        # whether it left a post-mortem behind.
        "injections": injection_json(
            injectors, RunOutcomeFacts(terminal=terminal,
                                       postmortems=len(postmortems))),
        "evidence_links": {"ledger": "data/missions", "isolated_root": "data"},
        # R-0187: what the order allowed, and what the run actually resolved to,
        # so an over-cap run is visible in its own evidence.
        "cycles_budget": order.budget.get("max_cycles"),
        "cycles_resolved": _resolved_cycles(entries),
        # R-0189: which world this run was given. A different template is a
        # different campaign, and the evidence says which one it was.
        "template_digest": _template_digest(),
        # F082 T003b (DECISION F082 D7 and D8): which model served which role.
        # An unobserved role is None, never a default name. The dict is copied
        # so a later mutation of the caller's own map cannot rewrite evidence
        # that has already been recorded.
        "models": dict(models) if models else {
            "planner": None, "orchestrator": None, "builder": None},
    }
    tokens = measure_tokens(entries)
    if tokens is None:
        body["tokens_source"] = TOKENS_UNMEASURED
    else:
        body["tokens"] = tokens
    return body


# ---------------------------------------------------------------------------
# The campaign
# ---------------------------------------------------------------------------

def run_campaign(orders: tuple[GauntletOrder, ...], campaign_root: Path, *,
                 deps: RunnerDeps | None = None,
                 real_data_root: Path | None = None,
                 on_order: Callable[[int, GauntletOrder, OrderOutcome], None] | None = None,
                 ) -> list[OrderOutcome]:
    """Run the frozen set once, in manifest order, keeping every run's evidence.

    A run that dies takes only itself down: every order is wrapped, so a raise
    from ``run_order`` ITSELF — its evidence write, its re-entered collectors —
    becomes a synthetic crashed outcome and the campaign continues (R-0180).
    The campaign's value is the whole matrix, and a missing run is worse than a
    failed one. ``real_data_root`` defaults to the operator's CURRENT root,
    resolved before any isolation is applied.
    """
    from packages.orchestration.data_paths import resolve_data_root

    deps = deps or RunnerDeps()
    real_root = real_data_root or resolve_data_root()
    campaign_root.mkdir(parents=True, exist_ok=True)
    outcomes: list[OrderOutcome] = []
    for index, order in enumerate(orders, start=1):
        try:
            outcome = run_order(order, campaign_root=campaign_root,
                                real_data_root=real_root, deps=deps, index=index)
        except Exception as exc:  # R-0180: the order dies, the campaign does not
            outcome = OrderOutcome(
                order_id=order.id,
                run_dir=campaign_root / f"run-{index:02d}-{order.id}",
                terminal_status=TERMINAL_RUNNER_CRASHED,
                crashed=f"{type(exc).__name__}: {exc}",
                body={})
        outcomes.append(outcome)
        if on_order is not None:
            on_order(index, order, outcome)
    return outcomes
