"""F075 T001 — the recorded evidence a gauntlet run leaves behind, and how to read it.

The gauntlet's pass definition (:mod:`packages.orchestration.gauntlet_evaluator`)
is a pure function over evidence. This module is the other half of that
sentence: the on-disk shape of the evidence and a loader that never raises.

Layout consumed::

    <evidence-dir>/
        <run-dir>/
            run.json          # required, gauntlet_run_version = 1
            dod_result.json   # optional, a stored dod_gate.GateResult JSON

Run order is the sorted run-directory name — a property of the bytes on disk,
never of the filesystem's iteration order, so two readers of the same evidence
produce the same matrix. A per-run directory rather than one flat campaign file
because failed attempts are KEPT (T1_F075.md) and each run links into its own
evidence.

**Reading evidence never raises.** A missing, malformed or wrong-version
``run.json`` produces a :class:`RunEvidence` carrying ``load_error`` instead of
an exception, because a gauntlet that skips the runs it cannot read would pass
by losing them. The evaluator turns that field into a named failure.

Nothing here judges anything, executes anything, or writes anything.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

#: Recorded-evidence schema version. A reader refuses a version it does not
#: know rather than guessing at a shape that moved under it.
GAUNTLET_RUN_VERSION = 1

#: The per-run evidence file inside each run directory.
RUN_FILENAME = "run.json"

#: The stored :class:`~packages.orchestration.dod_gate.GateResult` JSON, when
#: the run got far enough to have one. Optional on purpose: a run that never
#: reached the gate is a real case, and the evaluator reports it as such.
DOD_RESULT_FILENAME = "dod_result.json"

#: What a run.json says about where its token counts came from. A run whose
#: provider reported no usage did not spend nothing — it reported nothing, and
#: the difference has to survive all the way to the matrix (R-0183: attempt 1
#: displayed "0/0" on ten runs that had really spent tokens).
TOKENS_SOURCE_MEASURED = "measured"
TOKENS_SOURCE_UNMEASURED = "unmeasured"


@dataclass(frozen=True)
class RunEvidence:
    """One recorded run, exactly as it was found on disk.

    Every field is a fact the pass definition asks about; nothing is derived
    here. ``load_error`` is non-empty when the evidence could not be read.
    """

    run_dir: str
    order_id: str = ""
    kind: str = ""
    terminal_status: str = ""
    wall_seconds: float = 0.0
    tokens_in: int = 0
    tokens_out: int = 0
    #: False when nothing measured the cost. Then ``tokens_in``/``tokens_out``
    #: are 0 as a placeholder and MUST NOT be rendered as a measured zero.
    tokens_measured: bool = False
    operator_interventions: tuple[str, ...] = ()
    data_root_hash_before: str = ""
    data_root_hash_after: str = ""
    postmortems: tuple[dict[str, Any], ...] = ()
    open_decisions: tuple[dict[str, Any], ...] = ()
    era_defects: tuple[dict[str, Any], ...] = ()
    injections: tuple[dict[str, Any], ...] = ()
    evidence_links: dict[str, str] = field(default_factory=dict)
    dod_result: dict[str, Any] | None = None
    load_error: str = ""


def _as_str_tuple(raw: Any) -> tuple[str, ...]:
    if not isinstance(raw, list):
        return ()
    return tuple(str(item) for item in raw)


def _as_dict_tuple(raw: Any) -> tuple[dict[str, Any], ...]:
    if not isinstance(raw, list):
        return ()
    return tuple(item for item in raw if isinstance(item, dict))


#: Distinguishes "the field is not there" from "the field is there and wrong".
#: Absence is not malformation — a run that recorded no token count says zero
#: honestly; a run that recorded ``"many"`` does not.
_MISSING = object()


def _as_number(raw: Any, cast: Any, field: str) -> tuple[Any, str]:
    """One recorded number, or the reason it cannot be believed.

    A malformed number is a load error, never a silent zero (R-0178): the
    matrix is the report a human reads before flipping multi-cycle defaults,
    and a cost silently rendered as 0 understates exactly what that reader is
    weighing. JSON has a number type, so a string — even ``"612.5"`` — is a
    type error rather than a value to coerce. ``True`` is an ``int`` in Python
    and is refused here for the same reason.
    """
    if raw is _MISSING:
        return cast(0), ""
    if isinstance(raw, bool) or not isinstance(raw, (int, float)):
        return cast(0), f"{field} is not a number: {raw!r}"
    return cast(raw), ""


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_dirs(evidence_dir: Path) -> list[Path]:
    """Every run directory under an evidence dir, in the one canonical order.

    A directory without a ``run.json`` is not a run — the evidence area also
    holds the matrix report itself, and the reader must not trip over it.
    """
    if not evidence_dir.is_dir():
        return []
    return sorted(
        (p for p in evidence_dir.iterdir()
         if p.is_dir() and (p / RUN_FILENAME).is_file()),
        key=lambda p: p.name,
    )


def _failed(run_dir: str, order_id: str, error: str) -> RunEvidence:
    return RunEvidence(run_dir=run_dir, order_id=order_id, load_error=error)


def load_run(run_dir: Path) -> RunEvidence:
    """Read one recorded run. Never raises — an unreadable run is a FAILED run."""
    name = run_dir.name
    try:
        body = _load_json(run_dir / RUN_FILENAME)
    except FileNotFoundError:
        return _failed(name, "", f"missing {RUN_FILENAME}")
    except (OSError, ValueError) as exc:
        return _failed(name, "", f"unreadable {RUN_FILENAME}: {exc}")
    if not isinstance(body, dict):
        return _failed(name, "", f"{RUN_FILENAME} is not an object")

    order_id = str(body.get("order_id", ""))
    version = body.get("gauntlet_run_version")
    if version != GAUNTLET_RUN_VERSION:
        return _failed(name, order_id,
                       f"unsupported gauntlet_run_version {version!r} "
                       f"(expected {GAUNTLET_RUN_VERSION})")

    dod_result, error = _load_dod_result(run_dir)
    if error:
        return _failed(name, order_id, error)

    raw_tokens = body.get("tokens", _MISSING)
    if raw_tokens is _MISSING:
        tokens: dict[str, Any] = {}
    elif isinstance(raw_tokens, dict):
        tokens = raw_tokens
    else:
        return _failed(name, order_id, f"tokens is not an object: {raw_tokens!r}")

    raw_in, raw_out = tokens.get("in", _MISSING), tokens.get("out", _MISSING)
    declared = str(body.get("tokens_source", "") or "")
    # Measured means someone actually counted: the object is there, at least one
    # side of it was recorded, and the run did not itself say "unmeasured".
    tokens_measured = (declared != TOKENS_SOURCE_UNMEASURED
                       and (raw_in is not _MISSING or raw_out is not _MISSING))

    wall_seconds, wall_error = _as_number(
        body.get("wall_seconds", _MISSING), float, "wall_seconds")
    tokens_in, in_error = _as_number(raw_in, int, "tokens.in")
    tokens_out, out_error = _as_number(raw_out, int, "tokens.out")
    number_error = wall_error or in_error or out_error
    if number_error:
        return _failed(name, order_id, number_error)

    links = body.get("evidence_links")
    return RunEvidence(
        run_dir=name,
        order_id=order_id,
        kind=str(body.get("kind", "")),
        terminal_status=str(body.get("terminal_status", "")),
        wall_seconds=wall_seconds,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        tokens_measured=tokens_measured,
        operator_interventions=_as_str_tuple(body.get("operator_interventions")),
        data_root_hash_before=str(body.get("data_root_hash_before", "")),
        data_root_hash_after=str(body.get("data_root_hash_after", "")),
        postmortems=_as_dict_tuple(body.get("postmortems")),
        open_decisions=_as_dict_tuple(body.get("open_decisions")),
        era_defects=_as_dict_tuple(body.get("era_defects")),
        injections=_as_dict_tuple(body.get("injections")),
        evidence_links=({str(k): str(v) for k, v in links.items()}
                        if isinstance(links, dict) else {}),
        dod_result=dod_result,
    )


def _load_dod_result(run_dir: Path) -> tuple[dict[str, Any] | None, str]:
    """The stored gate verdict, or ``(None, "")`` when the gate never ran.

    Absent is legal; present-and-broken is not, and the difference matters: one
    is a run that stopped early, the other is evidence that cannot be believed.
    """
    path = run_dir / DOD_RESULT_FILENAME
    if not path.is_file():
        return None, ""
    try:
        loaded = _load_json(path)
    except (OSError, ValueError) as exc:
        return None, f"unreadable {DOD_RESULT_FILENAME}: {exc}"
    if not isinstance(loaded, dict):
        return None, f"{DOD_RESULT_FILENAME} is not an object"
    return loaded, ""
