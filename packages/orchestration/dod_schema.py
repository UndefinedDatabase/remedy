"""F061 T001 — the Definition-of-Done schema.

A DoD is a versioned list of concrete, machine-checkable checks. It is the
artifact that replaces "done is when it feels done": every check names a
runnable kind, a declarative kind-specific spec, whether it blocks, and where
it came from.

Conventions follow F005 structured outputs: small models, ``extra="forbid"``,
a REQUIRED ``schema_v`` (a bare ``Literal`` with no default, so a response that
omits it is a validation failure) and the model's own version in a
``SCHEMA_V`` class constant.

Two models, deliberately distinct:

  * :class:`DoDDraft` is the PROVIDER-facing contract. It carries only the
    checks an LLM proposes from the user's intent. It cannot express
    ``source`` and it cannot claim to be compiled — those are the compiler's
    to assign.
  * :class:`DoD` is the compiled artifact. It carries ``compiled`` and
    ``origin``, and a validator makes the dishonest combination
    (``compiled=True`` on a deterministic DoD) structurally impossible.

Compile-time validation rejects detectable nonsense rather than deferring it
to a runner: an unknown kind, an empty pytest selector, an empty custom argv,
a runtime_flow with no steps, an unknown spec key, a duplicate check id, or a
``cwd`` that escapes the worktree are all refused here.

``dod_v1`` is registered in ``schemas.models.SCHEMA_REGISTRY`` (F061 R3) — by
that module, importing this one, never as a side effect of importing here. The
shared bases therefore come from :mod:`packages.orchestration.structured_base`
rather than from ``schemas.models``: that is what keeps the dependency
one-directional.
"""
from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import Field, model_validator

from packages.orchestration.structured_base import _Strict, _Structured

#: Compact schema version tags (F005 convention: short, they travel in prompts).
DOD_SCHEMA_V = "dod_v1"
DOD_DRAFT_SCHEMA_V = "dod_draft_v1"

#: The traceability rule, quoted verbatim from docs/roadmap/features/T1_F061.md
#: (Acceptance). A test asserts this string still occurs in the feature file, so
#: the rule cannot drift away from the document that orders it.
TRACEABILITY_RULE = "every plan acceptance line traceable to a check id"

#: What a check runs. ``runtime_flow`` is schema-valid from R1 on, but has no
#: runner until T003 — the runner registry fails loud on it rather than passing.
CheckKind = Literal["pytest", "lint", "build", "runtime_flow", "custom_cmd"]

#: Where a check came from. ``compiled`` = proposed by the provider from user
#: intent; ``plan_acceptance`` = generated to cover a plan acceptance line;
#: ``standard`` = contributed by a registered standard-check provider.
CheckSource = Literal["compiled", "plan_acceptance", "standard"]

#: How the DoD as a whole was produced.
DoDOrigin = Literal["provider", "deterministic"]

_MAX_CHECKS = 60
_MAX_CHECK_ID_CHARS = 64
_ID_ALLOWED_EXTRA = set("._:-")

#: Every kind may carry an optional ``cwd``: a RELATIVE subdirectory of the
#: worktree. Absolute paths and ``..`` escapes are refused at compile time —
#: a check must not be able to name its way out of the worktree (F017).
_COMMON_SPEC_KEYS = frozenset({"cwd"})

_SPEC_KEYS: dict[str, frozenset[str]] = {
    "pytest": frozenset({"selector", "args"}),
    "lint": frozenset({"tool", "args", "paths"}),
    "build": frozenset({"tool", "args", "paths"}),
    "custom_cmd": frozenset({"argv"}),
    "runtime_flow": frozenset({"steps"}),
}

#: The v1 runtime_flow vocabulary (R-0165). One action, and a closed set of
#: keys per step: a flow step that names something else is nonsense the
#: compiler can detect, so it is refused here rather than discovered by the
#: runner an hour into a job. The runner keeps its own guard — it defends DoDs
#: stored before this rule existed.
FLOW_ACTION_OPEN = "open"
_FLOW_STEP_KEYS = frozenset({"action", "path", "expect_status", "expect_text"})


class DoDSpecError(ValueError):
    """A check spec is detectably unrunnable."""


def _require_str_list(spec: dict[str, Any], key: str, kind: str) -> None:
    """A present optional list field must be a list of non-empty strings."""
    if key not in spec:
        return
    value = spec[key]
    if not isinstance(value, list):
        raise DoDSpecError(f"{kind} spec {key!r} must be a list of strings")
    for i, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise DoDSpecError(
                f"{kind} spec {key}[{i}] must be a non-empty string")


def _require_nonempty_str(spec: dict[str, Any], key: str, kind: str) -> str:
    value = spec.get(key)
    if not isinstance(value, str) or not value.strip():
        raise DoDSpecError(f"{kind} spec needs a non-empty {key!r}")
    return value


def _reject_flag_shaped(value: str, field: str, kind: str) -> None:
    """Refuse a leading-dash value in a position that names a THING, not an option.

    R-0164: a pytest selector of ``"-x"``, or a tool/argv[0] of ``"--version"``,
    is well-formed as a string but is an OPTION, not a test path or a program.
    Left alone it lands in the argv where a selector or an executable belongs
    and silently changes what runs — exactly the detectable nonsense the feature
    file orders refused at compile time.
    """
    if value.lstrip().startswith("-"):
        raise DoDSpecError(
            f"{kind} spec {field!r} must name a target, not an option: "
            f"{value!r} starts with '-'")


def _validate_cwd(spec: dict[str, Any]) -> None:
    """A spec cwd stays inside the worktree — checked before anything runs."""
    if "cwd" not in spec:
        return
    cwd = spec["cwd"]
    if not isinstance(cwd, str) or not cwd.strip():
        raise DoDSpecError("spec 'cwd' must be a non-empty relative path")
    normalized = cwd.replace("\\", "/")
    if normalized.startswith("/"):
        raise DoDSpecError(f"spec 'cwd' must be relative, got {cwd!r}")
    if any(part == ".." for part in normalized.split("/")):
        raise DoDSpecError(f"spec 'cwd' must not escape the worktree: {cwd!r}")


def validate_check_spec(kind: str, spec: dict[str, Any]) -> None:
    """Reject a detectably unrunnable spec at COMPILE time.

    This is the "nonsense check" guard the feature calls for: a compiled check
    that could never run is refused while it is still cheap to refuse, instead
    of surfacing as a mystery red hours later. It cannot prove a command works
    — only that the declaration is well-formed for its kind.
    """
    allowed = _SPEC_KEYS.get(kind)
    if allowed is None:  # pragma: no cover - CheckKind Literal blocks this first
        raise DoDSpecError(f"unrunnable check kind: {kind!r}")

    unknown = sorted(set(spec) - allowed - _COMMON_SPEC_KEYS)
    if unknown:
        raise DoDSpecError(
            f"{kind} spec has unknown key(s): {', '.join(unknown)}")

    _validate_cwd(spec)

    if kind == "pytest":
        _reject_flag_shaped(
            _require_nonempty_str(spec, "selector", kind), "selector", kind)
        _require_str_list(spec, "args", kind)
    elif kind in ("lint", "build"):
        _reject_flag_shaped(
            _require_nonempty_str(spec, "tool", kind), "tool", kind)
        _require_str_list(spec, "args", kind)
        _require_str_list(spec, "paths", kind)
    elif kind == "custom_cmd":
        argv = spec.get("argv")
        if not isinstance(argv, list) or not argv:
            raise DoDSpecError("custom_cmd spec needs a non-empty 'argv' list")
        _require_str_list(spec, "argv", kind)
        _reject_flag_shaped(str(argv[0]), "argv[0]", kind)
    elif kind == "runtime_flow":
        steps = spec.get("steps")
        if not isinstance(steps, list) or not steps:
            raise DoDSpecError("runtime_flow spec needs a non-empty 'steps' list")
        for i, step in enumerate(steps):
            _validate_flow_step(i, step)


def _validate_flow_step(i: int, step: Any) -> None:
    """One runtime_flow step, against the v1 vocabulary (R-0165).

    Every message names the step index and the rule it broke, because a flow
    can carry a dozen steps and "invalid step" would send a reader looking
    through all of them.
    """
    if not isinstance(step, dict):
        raise DoDSpecError(f"runtime_flow steps[{i}] must be an object")

    unknown = sorted(set(step) - _FLOW_STEP_KEYS)
    if unknown:
        raise DoDSpecError(
            f"runtime_flow steps[{i}] has unknown key(s): {', '.join(unknown)} "
            f"(v1 step keys: {', '.join(sorted(_FLOW_STEP_KEYS))})")

    action = step.get("action")
    if not isinstance(action, str) or not action.strip():
        raise DoDSpecError(f"runtime_flow steps[{i}] needs a non-empty 'action'")
    if action.strip() != FLOW_ACTION_OPEN:
        raise DoDSpecError(
            f"runtime_flow steps[{i}] action {action!r} is not supported "
            f"(v1 actions: {FLOW_ACTION_OPEN})")

    path = step.get("path")
    if not isinstance(path, str) or not path.strip():
        raise DoDSpecError(
            f"runtime_flow steps[{i}] needs a non-empty 'path' string")
    if not path.strip().startswith("/"):
        raise DoDSpecError(
            f"runtime_flow steps[{i}] 'path' must start with '/', got {path!r}")

    if "expect_status" in step:
        status = step["expect_status"]
        # bool is an int in Python, and `expect_status: true` is not a status.
        if isinstance(status, bool) or not isinstance(status, (int, float)):
            raise DoDSpecError(
                f"runtime_flow steps[{i}] 'expect_status' must be an integer "
                f"status code, got {status!r}")
        if isinstance(status, float) and not status.is_integer():
            raise DoDSpecError(
                f"runtime_flow steps[{i}] 'expect_status' must be an integer "
                f"status code, got {status!r}")

    if "expect_text" in step and not isinstance(step["expect_text"], str):
        raise DoDSpecError(
            f"runtime_flow steps[{i}] 'expect_text' must be a string, "
            f"got {step['expect_text']!r}")


def _validate_check_id(value: str) -> str:
    ident = value.strip()
    if not ident:
        raise DoDSpecError("check id must not be empty")
    if len(ident) > _MAX_CHECK_ID_CHARS:
        raise DoDSpecError(
            f"check id exceeds {_MAX_CHECK_ID_CHARS} chars: {ident[:20]!r}...")
    for ch in ident:
        if not (ch.isalnum() or ch in _ID_ALLOWED_EXTRA):
            raise DoDSpecError(
                f"check id {value!r} has an illegal character {ch!r}")
    return ident


class DraftCheck(_Strict):
    """One check as a PROVIDER proposes it.

    Deliberately without ``source``: a provider does not get to label where a
    check came from. The compiler assigns that.
    """

    id: str
    kind: CheckKind
    spec: dict[str, Any] = Field(default_factory=dict)
    blocking: bool = True
    #: Acceptance-line keys (``"<task_id>:<index>"``) this check covers.
    acceptance_refs: list[str] = Field(default_factory=list)
    description: str = ""

    @model_validator(mode="after")
    def _validate(self) -> DraftCheck:
        object.__setattr__(self, "id", _validate_check_id(self.id))
        validate_check_spec(self.kind, self.spec)
        return self


class DoDCheck(DraftCheck):
    """One compiled check: a draft check plus its assigned provenance."""

    source: CheckSource


class DoDDraft(_Structured):
    """Provider-proposed checks (schema ``dod_draft_v1``).

    The provider answers in this shape and nothing else. It cannot claim a
    DoD is compiled, cannot set ``source``, and cannot skip ``schema_v``.
    """

    SCHEMA_V: ClassVar[str] = DOD_DRAFT_SCHEMA_V
    schema_v: Literal["dod_draft_v1"]  # required: no default
    checks: list[DraftCheck] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_ids(self) -> DoDDraft:
        _reject_duplicate_ids(self.checks)
        return self


class DoD(_Structured):
    """A compiled Definition of Done (schema ``dod_v1``).

    ``compiled`` and ``origin`` are both required and are cross-checked: a DoD
    built without a provider can only be ``compiled=False`` with
    ``origin="deterministic"``. The dishonest combination does not validate,
    so a deterministic fallback cannot be presented as compiled by accident or
    by a later refactor.
    """

    SCHEMA_V: ClassVar[str] = DOD_SCHEMA_V
    schema_v: Literal["dod_v1"]  # required: no default
    checks: list[DoDCheck] = Field(min_length=1)
    compiled: bool  # required: no default
    origin: DoDOrigin  # required: no default

    @model_validator(mode="after")
    def _validate(self) -> DoD:
        if len(self.checks) > _MAX_CHECKS:
            raise ValueError(
                f"DoD exceeds {_MAX_CHECKS}-check cap (got {len(self.checks)})")
        _reject_duplicate_ids(self.checks)
        if self.compiled != (self.origin == "provider"):
            raise ValueError(
                "DoD.compiled must be True exactly when origin is 'provider' "
                f"(got compiled={self.compiled}, origin={self.origin!r})")
        return self

    @property
    def blocking_checks(self) -> list[DoDCheck]:
        """The checks a job-end gate would have to see green (T004 uses this)."""
        return [c for c in self.checks if c.blocking]


def _reject_duplicate_ids(checks: list[Any]) -> None:
    seen: set[str] = set()
    for check in checks:
        if check.id in seen:
            raise ValueError(f"duplicate check id: {check.id!r}")
        seen.add(check.id)
