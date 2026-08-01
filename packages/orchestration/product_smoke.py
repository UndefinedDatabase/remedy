"""F062 T001 — the product-smoke standard DoD block.

Green tests can still mean a broken product. This block is what closes that
gap: for a job whose project has a runnable app, the DoD gains smoke checks
proving the app actually STARTS before the job may end green.

This module owns the BLOCK — which checks exist, when they apply, and what
they are called. It does NOT own process handling: the checks are executed by
``dod_runners``, which orchestrates the F007 harness verbs (resolve the spec,
choose a port, start in its own session, probe readiness, stop the family).
The harness's process semantics are not touched or re-implemented here.

Applicability is decided at COMPILE time, from the project the DoD is being
compiled for:

  * a resolvable runtime  → the check is contributed as BLOCKING;
  * no runtime configured or detected → the check is still contributed, but
    NON-blocking, and it reports :data:`NOT_APPLICABLE_MESSAGE`. It is
    therefore visible in the matrix and gates nothing — reported, never
    silently green (P6);
  * no project context at all (the compiler was given no worktree) → the
    block contributes nothing, because it cannot honestly claim either.

v1 is HTTP level, deliberately. Clickable browser flows stay in the DoD's
``runtime_flow`` kind; no browser dependency belongs in here.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

from packages.orchestration.dod_schema import DraftCheck

if TYPE_CHECKING:  # pragma: no cover - typing only
    from packages.orchestration.dod_compiler import StandardCheckContext

#: The name this block registers under in the DoD compiler's standard-check
#: seam (F061 ``register_standard_check_provider``).
SMOKE_PROVIDER_NAME = "product_smoke"

#: The smoke checks, in the order they run. v1 ships only the first; T002 adds
#: ``core_paths_respond`` and T003 ``clean_console``.
SMOKE_APP_STARTS = "app_starts"
SMOKE_CORE_PATHS = "core_paths_respond"
SMOKE_CLEAN_CONSOLE = "clean_console"
SMOKE_CHECKS: tuple[str, ...] = (
    SMOKE_APP_STARTS, SMOKE_CORE_PATHS, SMOKE_CLEAN_CONSOLE)

#: Check ids. Stable, because they appear in the report matrix and in a held
#: job's blocker list.
CHECK_ID_APP_STARTS = "smoke-app-starts"
CHECK_ID_CORE_PATHS = "smoke-core-paths"
CHECK_ID_CLEAN_CONSOLE = "smoke-clean-console"

#: The DOCUMENTED base error markers scanned in the app's captured output.
#: Deliberately small and CASE-SENSITIVE: "error" inside ordinary prose is not
#: a fatal, and a list that matches everything would be ignored by everyone.
#: Extending it is CONFIG (``smoke.error_patterns``), not code — and config
#: only ADDS, so nothing here can be configured away.
#:
#:   Traceback (most recent call last)  — a Python traceback header
#:   ERROR                             — the conventional level marker
#:   CRITICAL / FATAL                  — higher levels
#:   Unhandled exception               — .NET/Node style fatal
#:   panic:                            — Go runtime panic
#:   Segmentation fault                — a native crash
CONSOLE_ERROR_PATTERNS: tuple[str, ...] = (
    "Traceback (most recent call last)",
    "ERROR",
    "CRITICAL",
    "FATAL",
    "Unhandled exception",
    "panic:",
    "Segmentation fault",
)

#: How many extracted routes ride along with the health path. A probe set is
#: meant to be a SMALL proof the product answers, not a crawl.
MAX_EXTRACTED_PATHS = 5

#: A route mentioned in intent or plan text: a slash-led, URL-shaped token.
_ROUTE_PATTERN = re.compile(r"/[A-Za-z0-9_\-./{}:]*")

#: Slash-led tokens that are NOT routes. A filesystem path and a source file
#: both start with "/" or carry an extension; probing them would be nonsense.
_FS_ROOTS = ("/home/", "/etc/", "/usr/", "/var/", "/tmp/", "/opt/", "/root/",
             "/bin/", "/sbin/", "/lib/", "/proc/", "/dev/", "/mnt/", "/srv/")
_FILE_SUFFIXES = (".py", ".md", ".json", ".toml", ".yaml", ".yml", ".txt",
                  ".lock", ".cfg", ".ini", ".sh", ".ts", ".tsx", ".js")

#: What a project without a runnable app is told. Not an error and not a pass:
#: the honest third answer.
NOT_APPLICABLE_MESSAGE = "smoke: not applicable (no runtime configured)"

#: What a project whose smoke is switched OFF is told. One constant, shared by
#: the compile-time row and the run-time refusal, so the two can never drift.
DISABLED_MESSAGE = "smoke: disabled by config (smoke.enabled = false)"

#: Recorded when the first attempt failed and the retry succeeded — a pass
#: that is visibly less trustworthy than a first-attempt pass (A9).
PASSED_ON_RETRY = "passed on retry"

#: How long to wait before the single retry of a failed start.
RETRY_BACKOFF_SECONDS = 1.0


def resolve_runtime(worktree_root: str | Path) -> tuple[Any | None, str]:
    """The project's runtime spec, or the reason there is none.

    Returns ``(spec, "")`` when the harness can start this project, and
    ``(None, reason)`` when it cannot. The reason is the harness's own text —
    this module never invents one.
    """
    from packages.runtimes.runtime_config import resolve_spec

    try:
        return resolve_spec(Path(worktree_root)), ""
    except Exception as exc:  # noqa: BLE001 — any resolution failure means "no runtime"
        return None, str(exc)


def app_starts_check(*, blocking: bool, description: str) -> DraftCheck:
    """The ``app_starts`` draft check, as the block contributes it."""
    return DraftCheck(
        id=CHECK_ID_APP_STARTS,
        kind="product_smoke",
        spec={"smoke": SMOKE_APP_STARTS},
        blocking=blocking,
        description=description,
    )


def _is_route(token: str) -> bool:
    """Does this slash-led token name an HTTP route rather than a file?"""
    if not token.startswith("/"):
        return False
    if token.startswith(_FS_ROOTS):
        return False
    lowered = token.lower().rstrip("/.,;:)")
    return not lowered.endswith(_FILE_SUFFIXES)


def extract_paths(ctx: StandardCheckContext) -> list[str]:
    """Routes the DoD compiler's material mentions, in first-seen order.

    The hand-off the feature file describes: intent and plan text name the
    paths this work is about ("/", the feature's route), and the smoke probes
    those alongside the configured health path. Extraction is deliberately
    conservative — a slash-led token that looks like a filesystem path or a
    source file is not a route, and a wrong guess would probe nonsense.
    """
    intake = ctx.intake or {}
    sources: list[str] = [str(intake.get("goal", "") or "")]
    for key in ("acceptance_hints", "constraints", "context_refs"):
        sources.extend(str(v) for v in (intake.get(key) or []))
    for task in getattr(ctx.plan, "tasks", []) or []:
        sources.append(str(getattr(task, "goal", "") or ""))
        sources.append(str(getattr(task, "title", "") or ""))
        sources.extend(str(a) for a in (getattr(task, "acceptance", []) or []))

    found: list[str] = []
    for text in sources:
        for match in _ROUTE_PATTERN.finditer(text):
            token = match.group().rstrip(".,;:)\"'")
            if len(token) > 1:
                token = token.rstrip("/") or "/"
            if _is_route(token) and token not in found:
                found.append(token)
                if len(found) >= MAX_EXTRACTED_PATHS:
                    return found
    return found


def core_paths_check(*, paths: list[dict[str, Any]], blocking: bool,
                     description: str) -> DraftCheck:
    """The ``core_paths_respond`` draft check, as the block contributes it."""
    return DraftCheck(
        id=CHECK_ID_CORE_PATHS,
        kind="product_smoke",
        spec={"smoke": SMOKE_CORE_PATHS, "paths": paths},
        blocking=blocking,
        description=description,
    )


def clean_console_check(*, blocking: bool, description: str) -> DraftCheck:
    """The ``clean_console`` draft check, as the block contributes it."""
    return DraftCheck(
        id=CHECK_ID_CLEAN_CONSOLE,
        kind="product_smoke",
        spec={"smoke": SMOKE_CLEAN_CONSOLE},
        blocking=blocking,
        description=description,
    )


def smoke_config() -> dict[str, Any]:
    """The smoke's config table, resolved. Never raises — a broken config
    falls back to the documented defaults rather than taking a job down."""
    out: dict[str, Any] = {
        "enabled": True, "paths": [], "error_patterns": [],
        "ready_timeout_s": None,
    }
    try:
        from packages.orchestration.config import get_config
        cfg = get_config()
    except Exception:  # noqa: BLE001 - config unavailable = documented defaults
        return out

    def _get(key: str, default: Any) -> Any:
        try:
            value = cfg.get(f"smoke.{key}")
        except Exception:  # noqa: BLE001
            return default
        return default if value is None else value

    out["enabled"] = bool(_get("enabled", True))
    out["paths"] = [str(p) for p in (_get("paths", []) or [])]
    out["error_patterns"] = [str(p) for p in (_get("error_patterns", []) or [])]
    window = _get("ready_timeout_s", None)
    out["ready_timeout_s"] = float(window) if window is not None else None
    return out


def error_patterns() -> tuple[str, ...]:
    """The base pattern list PLUS any configured additions, in that order.

    Config extends; it never replaces. A project can teach the smoke about its
    own framework's fatal, but cannot switch off the base guarantees.
    """
    extra = [p for p in smoke_config()["error_patterns"]
             if p and p not in CONSOLE_ERROR_PATTERNS]
    return CONSOLE_ERROR_PATTERNS + tuple(extra)


def scan_console(text: str, patterns: tuple[str, ...] | None = None
                 ) -> list[tuple[str, str]]:
    """``(pattern, line)`` for every console line matching a marker.

    Case-sensitive, and it returns the LINES so a red check can quote what it
    actually saw instead of asserting that something was wrong.
    """
    active = patterns if patterns is not None else error_patterns()
    hits: list[tuple[str, str]] = []
    for line in text.splitlines():
        for pattern in active:
            if pattern in line:
                hits.append((pattern, line.strip()))
                break
    return hits


def smoke_checks(ctx: StandardCheckContext) -> list[DraftCheck]:
    """The standard-check provider registered into the DoD compiler's seam.

    Contributes the smoke block's checks for the project the DoD is being
    compiled for. See the module docstring for the three applicability cases.
    """
    worktree = str(getattr(ctx, "worktree_root", "") or "").strip()
    if not worktree:
        # No project context: the compiler cannot tell whether this project
        # even has an app. Claiming either way would be an invented value.
        return []

    spec, reason = resolve_runtime(worktree)
    if spec is None:
        # ONE honest row for the whole block. The later checks are not
        # contributed at all: `core_paths_respond` would need a probe set, and
        # a project with no app has no paths — inventing one to fill a row is
        # exactly the fabricated value this block exists to avoid.
        return [app_starts_check(
            blocking=False,
            description=f"{NOT_APPLICABLE_MESSAGE}: {reason}")]

    config = smoke_config()
    if not config["enabled"]:
        # Switched off for a project that HAS an app. Say so — a disabled
        # smoke is a reported fact, not an absent row and not a pass.
        return [app_starts_check(blocking=False, description=DISABLED_MESSAGE)]

    # Ordered: the app must start before probing it is meaningful, and the
    # console is judged over the output the whole run produced.
    override = [p for p in config["paths"] if str(p).startswith("/")]
    routes = override or extract_paths(ctx)
    probe_paths: list[dict[str, Any]] = [{"path": spec.health_path}]
    for route in routes:
        if route != spec.health_path:
            probe_paths.append({"path": route})

    return [
        app_starts_check(
            blocking=True,
            description=(f"{SMOKE_APP_STARTS}: the app starts and answers "
                         f"{spec.health_path}")),
        core_paths_check(
            paths=probe_paths,
            blocking=True,
            description=(f"{SMOKE_CORE_PATHS}: "
                         f"{', '.join(p['path'] for p in probe_paths)}")),
        clean_console_check(
            blocking=True,
            description=(f"{SMOKE_CLEAN_CONSOLE}: "
                         f"{len(error_patterns())} error markers")),
    ]


def register(*, replace: bool = False) -> None:
    """Register the smoke block into the DoD compiler's standard-check seam.

    Registration is explicit, never an import side effect: a module that
    silently changes what every compiled DoD contains just by being imported
    is the opposite of the honesty this block exists to provide.
    """
    from packages.orchestration.dod_compiler import (
        register_standard_check_provider,
        registered_standard_check_providers,
        unregister_standard_check_provider,
    )

    if SMOKE_PROVIDER_NAME in registered_standard_check_providers():
        if not replace:
            return
        unregister_standard_check_provider(SMOKE_PROVIDER_NAME)
    register_standard_check_provider(SMOKE_PROVIDER_NAME, smoke_checks)


def unregister() -> None:
    """Remove the smoke block from the seam. Unknown = no-op."""
    from packages.orchestration.dod_compiler import unregister_standard_check_provider

    unregister_standard_check_provider(SMOKE_PROVIDER_NAME)


def is_registered() -> bool:
    from packages.orchestration.dod_compiler import registered_standard_check_providers

    return SMOKE_PROVIDER_NAME in registered_standard_check_providers()
