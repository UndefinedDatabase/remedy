"""F035 T001 (DECISION F035 D1) — the ownership ledger: a pure pass over the records earlier
features already write, naming who acted through which door, when, in their own words, and
what it caused. Remedy deliberately does not join the command audit (D1 (4)): every class whose
record names an actor already names the door, either `cli` on the command line or a browser
door through a fingerprint, `cockpit` or `ui`, and joining the audit to the rest by matching
times would be a guess this ledger may not make.

This module READS every record it draws on and WRITES none of them: building the ledger twice
over the same records answers equal dicts, so the file it is eventually saved to (round 2) is
regenerable and never a second truth. It imports nothing from `pingpong_job`, `ui_server` or
`apps` — every class it reads is read through the module that owns that record's shape.
Round 1 lands the classes whose records already name an actor: vetoes, veto answers,
injections, subtree reruns, plan and task edits, steering messages and notes, and the pause,
resume and stop events of the run log. Round 2 lands hunk decisions, decision answers,
clarification answers and plan approval, and writes `ownership.json` into the job's evidence
export at every job terminal.
"""
from __future__ import annotations

from typing import Any

OWNERSHIP_SCHEMA = "remedy.ownership.v1"
OWNERSHIP_FILENAME = "ownership.json"

#: DECISION F035 D1 (3): `operator` for a human, `default_policy` for a documented default the
#: operator accepted at plan approval, `remedy` for a machine choice made under the job's
#: configuration.
ACTOR_KINDS = ("operator", "default_policy", "remedy")

#: `browser` for a fingerprint, `cockpit` or `ui`; `cli` for `cli`; "" for anything else —
#: hunk decisions and clarification answers among them, whose records name no door at all.
ACTOR_DOORS = ("browser", "cli", "")

_ENTRY_KEYS = ("record_ref", "ts", "actor", "action", "task_id", "text", "consequence", "detail")
_ENTRY_STRING_KEYS = ("record_ref", "ts", "action", "task_id", "text")
_CONSEQUENCE_KEYS = ("kind", "task_ids", "ref")

#: F035 T001's second half (round 2): hunk decisions, decision answers, clarification answers
#: and plan approval. The five run-log events read here are round 1's.
_RUN_LOG_EVENTS = ("job_paused", "task_paused", "job_resumed", "task_resumed", "job_stopped")

__all__ = [
    "OWNERSHIP_SCHEMA",
    "OWNERSHIP_FILENAME",
    "ACTOR_KINDS",
    "ACTOR_DOORS",
    "OwnershipError",
    "ownership_actor",
    "ownership_entry_problems",
    "build_ownership_ledger",
]


class OwnershipError(RuntimeError):
    """The ledger could not be built: a reader's own error, an entry that fails S3's shape, or
    a duplicate `record_ref`. Loud on purpose — a silently dropped or malformed entry would
    misname who acted."""


# S2 — the actor


def ownership_actor(recorded_as: Any, *, kind: str = "operator",
                    auto_approved: bool = False) -> dict[str, Any]:
    """One actor: `kind`, `door`, `recorded_as`, `token_number` (always 0 here — round 1
    numbers fingerprints over the whole sorted ledger, not per actor), `auto_approved`.

    `recorded_as` is `str(recorded_as)`, or "" for `None`, never otherwise changed — an
    operator's own token or channel name travels unaltered. A `kind` outside `ACTOR_KINDS`
    raises `OwnershipError`: nothing renders authorless or under an invented kind.
    """
    if kind not in ACTOR_KINDS:
        raise OwnershipError(f"unknown actor kind {kind!r}; must be one of {ACTOR_KINDS}")
    recorded = "" if recorded_as is None else str(recorded_as)
    if recorded.startswith("tf:") or recorded in ("cockpit", "ui"):
        door = "browser"
    elif recorded == "cli":
        door = "cli"
    else:
        door = ""
    return {
        "kind": kind,
        "door": door,
        "recorded_as": recorded,
        "token_number": 0,
        "auto_approved": bool(auto_approved),
    }


# S3 — the entry


def ownership_entry_problems(entry: Any) -> list[str]:
    """Every readable line naming a breach of S3's shape; `[]` for a sound entry.

    Checked: the entry is a dict carrying exactly `_ENTRY_KEYS`; the string-valued keys are
    strings; `actor` is a dict whose `kind` and `door` are each inside their tuple; `consequence`
    is a dict carrying exactly `kind`, `task_ids` (a list of strings) and `ref`; `detail` is a
    dict; and `record_ref`/`action` are not empty.
    """
    if not isinstance(entry, dict):
        return ["the entry is not a dict"]

    problems: list[str] = []
    missing = [key for key in _ENTRY_KEYS if key not in entry]
    extra = sorted(set(entry) - set(_ENTRY_KEYS))
    if missing:
        problems.append(f"the entry is missing {missing}")
    if extra:
        problems.append(f"the entry carries unexpected keys {extra}")
    if missing:
        return problems

    for key in _ENTRY_STRING_KEYS:
        if not isinstance(entry[key], str):
            problems.append(f"{key!r} is not a string")

    actor = entry["actor"]
    if not isinstance(actor, dict):
        problems.append("actor is not a dict")
    else:
        if actor.get("kind") not in ACTOR_KINDS:
            problems.append(f"actor kind {actor.get('kind')!r} is outside {ACTOR_KINDS}")
        if actor.get("door") not in ACTOR_DOORS:
            problems.append(f"actor door {actor.get('door')!r} is outside {ACTOR_DOORS}")

    consequence = entry["consequence"]
    if not isinstance(consequence, dict):
        problems.append("consequence is not a dict")
    else:
        c_missing = [key for key in _CONSEQUENCE_KEYS if key not in consequence]
        c_extra = sorted(set(consequence) - set(_CONSEQUENCE_KEYS))
        if c_missing:
            problems.append(f"consequence is missing {c_missing}")
        if c_extra:
            problems.append(f"consequence carries unexpected keys {c_extra}")
        if "task_ids" in consequence:
            ids = consequence["task_ids"]
            if not isinstance(ids, list) or not all(isinstance(t, str) for t in ids):
                problems.append("consequence task_ids is not a list of strings")

    if not isinstance(entry["detail"], dict):
        problems.append("detail is not a dict")

    if entry["record_ref"] == "":
        problems.append("record_ref is empty")
    if entry["action"] == "":
        problems.append("action is empty")

    return problems


# S4 — the classes, one private reader per class


def _veto_entries(job: Any) -> list[dict[str, Any]]:
    from packages.orchestration import task_veto as _tv

    out: list[dict[str, Any]] = []
    metadata = dict((job.metadata or {}).get("task_vetoes") or {})
    for value in metadata.values():
        if "inert" in value:
            consequence = {"kind": "inert", "task_ids": [], "ref": str(value["inert"])}
        else:
            consequence = {
                "kind": "unreachable",
                "task_ids": [str(t) for t in (value.get("unreachable_task_ids") or [])],
                "ref": "",
            }
        out.append({
            "record_ref": f"veto:{value.get('request_id', '')}",
            "ts": str(value.get("requested_at", "")),
            "actor": ownership_actor(value.get("actor")),
            "action": "task_vetoed",
            "task_id": str(value.get("task_id", "")),
            "text": value.get("reason", "") if isinstance(value.get("reason"), str) else "",
            "consequence": consequence,
            "detail": {"status_at_veto": str(value.get("status_at_veto", ""))},
        })

    try:
        control_entries = _tv.vetoed_tasks(job.job_id)
    except _tv.TaskVetoError as exc:
        raise OwnershipError(f"TaskVetoError: {exc}") from exc

    all_control_ids = {entry.task_id for entry in control_entries}
    for entry in control_entries:
        if entry.task_id in metadata:
            continue                                          # already folded, read above
        other_ids = all_control_ids - {entry.task_id}
        unreachable = [
            tid for tid in _tv.veto_unreachable(job.tasks, [entry.task_id])
            if tid not in other_ids
        ]
        out.append({
            "record_ref": f"veto:{entry.request_id}",
            "ts": entry.requested_at,
            "actor": ownership_actor(entry.actor),
            "action": "task_vetoed",
            "task_id": entry.task_id,
            "text": entry.reason,
            "consequence": {"kind": "unreachable", "task_ids": unreachable, "ref": ""},
            "detail": {"status_at_veto": entry.status_at_veto},
        })
    return out


def _veto_answer_entries(job: Any) -> list[dict[str, Any]]:
    from packages.orchestration import task_veto as _tv

    try:
        answers = _tv.veto_answers(job.job_id)
    except _tv.TaskVetoError as exc:
        raise OwnershipError(f"TaskVetoError: {exc}") from exc

    out: list[dict[str, Any]] = []
    for answer in answers.values():
        out.append({
            "record_ref": f"veto_answer:{answer.request_id}",
            "ts": answer.answered_at,
            "actor": ownership_actor(answer.actor),
            "action": "veto_answered",
            "task_id": answer.task_id,
            "text": answer.option,
            "consequence": {"kind": answer.option, "task_ids": [], "ref": answer.follow_up_job_id},
            "detail": {},
        })
    return out


def _injection_entries(job: Any) -> list[dict[str, Any]]:
    from packages.orchestration import task_injection as _ti

    try:
        records = _ti.confirmed_injections(job.job_id)
    except _ti.TaskInjectionError as exc:
        raise OwnershipError(f"TaskInjectionError: {exc}") from exc

    folds = (job.metadata or {}).get("task_injections") or {}
    out: list[dict[str, Any]] = []
    for record in records:
        draft_id = record["draft_id"]
        fold = folds.get(draft_id)
        actor = ownership_actor(
            record.get("actor"), auto_approved=bool(record.get("confirmed_unseen")))
        if isinstance(fold, dict) and "task_id" in fold:
            task_id = str(fold["task_id"])
            consequence = {"kind": "task_added", "task_ids": [task_id], "ref": ""}
        elif isinstance(fold, dict) and "inert" in fold:
            task_id = ""
            consequence = {"kind": "inert", "task_ids": [], "ref": str(fold["inert"])}
        else:
            task_id = ""
            consequence = {"kind": "not_folded", "task_ids": [], "ref": ""}
        out.append({
            "record_ref": f"injection:{draft_id}",
            "ts": str(record.get("confirmed_at", "")),
            "actor": actor,
            "action": "task_injected",
            "task_id": task_id,
            "text": record.get("text", "") if isinstance(record.get("text"), str) else "",
            "consequence": consequence,
            "detail": {
                "drafted_by": record.get("drafted_by") or "",
                "planned_id": record["task"]["id"],
                "placement_basis": record["placement"]["basis"],
            },
        })
    return out


def _rerun_entries(job: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for record in job.reruns or []:
        model = record.get("model") or {}
        out.append({
            "record_ref": f"rerun:{record.get('rerun_id', '')}",
            "ts": str(record.get("at", "")),
            "actor": ownership_actor(record.get("actor")),
            "action": "subtree_rerun",
            "task_id": str(record.get("root_task_id", "")),
            "text": "",
            "consequence": {
                "kind": "subtree_reset",
                "task_ids": [str(t) for t in (record.get("subtree") or [])],
                "ref": "",
            },
            "detail": {"model_override": model.get("override") or ""},
        })
    return out


def _edit_entries(job: Any) -> list[dict[str, Any]]:
    from packages.orchestration import plan_editing as _pe

    out: list[dict[str, Any]] = []
    body = job.task_plan or {}
    for entry in body.get(_pe.EDIT_LOG_KEY) or []:
        if "injection" in entry:
            continue                                          # (c)'s own entry, not (e)'s
        runtime = entry.get("runtime")
        args = entry.get("args")
        if runtime:
            action = "task_edited"
            task_id = str((runtime or {}).get("task_id", ""))
        else:
            action = "plan_edited"
            if isinstance(args, dict) and isinstance(args.get("task_id"), str):
                task_id = args["task_id"]
            else:
                task_id = ""
        version = entry.get("version")
        out.append({
            "record_ref": f"plan_edit:v{version}",
            "ts": str(entry.get("ts", "")),
            "actor": ownership_actor(entry.get("actor")),
            "action": action,
            "task_id": task_id,
            "text": "",
            "consequence": {
                "kind": "plan_version",
                "task_ids": [task_id] if task_id else [],
                "ref": f"v{version}",
            },
            "detail": {"command": entry.get("command"), "args": args},
        })
    return out


def _steering_entries(job: Any) -> list[dict[str, Any]]:
    from packages.orchestration import steering as _st

    try:
        records = _st.list_steering_messages(job.job_id)
        consumptions = _st.list_steering_consumptions(job.job_id)
    except _st.SteeringError as exc:
        raise OwnershipError(f"SteeringError: {exc}") from exc

    out: list[dict[str, Any]] = []
    for record in records:
        note_task = _st.note_task_id(record)
        action = "note_sent" if note_task else "steering_sent"
        marker = consumptions.get(record["message_id"])
        if marker is not None:
            consequence = {
                "kind": "consumed",
                "task_ids": [str(marker.get("task_id", ""))],
                "ref": f"round {marker.get('round_number', '')}",
            }
        else:
            consequence = {"kind": "not_consumed", "task_ids": [], "ref": ""}
        out.append({
            "record_ref": f"steering:{record['message_id']}",
            "ts": str(record.get("received_at", "")),
            "actor": ownership_actor(record.get("channel")),
            "action": action,
            "task_id": note_task,
            "text": record.get("text", "") if isinstance(record.get("text"), str) else "",
            "consequence": consequence,
            "detail": {},
        })
    return out


def _run_log_entries(job: Any) -> list[dict[str, Any]]:
    from packages.orchestration import data_paths as _dp
    from packages.orchestration import timeline as _tl

    events = _tl.load_run_events(_dp.resolve_data_root(), job.job_id)
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, Any]] = []
    for event in events:
        name = event.get("event")
        if name not in _RUN_LOG_EVENTS:
            continue
        md = event.get("metadata") or {}
        request_id = str(md.get("request_id", ""))
        raw_ts = str(event.get("timestamp", ""))
        key = (name, request_id)
        if key in seen:
            continue
        seen.add(key)

        task_id = str(event.get("task_id") or "")
        ref = request_id if request_id else raw_ts
        record_ref = f"{name}:{ref}"

        if name == "job_paused":
            entry_ts = raw_ts
            entry_task_id = ""
            text = str(md.get("reason", ""))
            actor = ownership_actor(md.get("source"))
            consequence = {
                "kind": "withheld",
                "task_ids": [str(t) for t in (md.get("withheld_task_ids") or [])],
                "ref": "",
            }
            detail: dict[str, Any] = {}
        elif name == "task_paused":
            entry_ts = str(md.get("requested_at") or raw_ts)
            entry_task_id = task_id
            text = str(md.get("reason", ""))
            actor = ownership_actor(md.get("source"))
            consequence = {
                "kind": "withheld",
                "task_ids": [task_id] if task_id else [],
                "ref": "",
            }
            detail = {}
        elif name in ("job_resumed", "task_resumed"):
            entry_ts = raw_ts
            entry_task_id = "" if name == "job_resumed" else task_id
            text = ""
            # The event carries the PAUSE's source, not the resumer's, so the door is not
            # recorded here — an empty actor rather than one attributed by inference.
            actor = ownership_actor("")
            if name == "job_resumed":
                released_ids = [str(t) for t in (md.get("withheld_task_ids") or [])]
            else:
                released_ids = [task_id] if task_id else []
            consequence = {"kind": "released", "task_ids": released_ids, "ref": ""}
            detail = {"paused_by": md.get("source", "")}
        else:                                                  # job_stopped
            entry_ts = str(md.get("requested_at") or raw_ts)
            entry_task_id = task_id
            text = str(md.get("reason", ""))
            actor = ownership_actor(md.get("source"))
            consequence = {
                "kind": "stopped",
                "task_ids": [],
                "ref": str(md.get("postmortem_ref") or ""),
            }
            detail = {}

        out.append({
            "record_ref": record_ref,
            "ts": entry_ts,
            "actor": actor,
            "action": name,
            "task_id": entry_task_id,
            "text": text,
            "consequence": consequence,
            "detail": detail,
        })
    return out


# S5 — the build


def build_ownership_ledger(job: Any) -> dict[str, Any]:
    """`{"schema", "job_id", "entries"}` — the ledger for one job, over every record the
    classes above read. A `TaskVetoError`, `TaskInjectionError` or `SteeringError` from a
    reader is already raised as `OwnershipError` naming the class, `from` the original, by
    the reader that caught it.

    Entries are sorted by `(ts == "", ts, record_ref)` — timeless entries last, then by their
    own ref. Every actor whose `recorded_as` starts with `tf:` then gets `token_number` 1, 2,
    … by the order its fingerprint FIRST appears in that sorted list; every other actor keeps
    `token_number` 0. A duplicate `record_ref`, or any `ownership_entry_problems` line, raises
    `OwnershipError` listing them — before any sorting or numbering happens, so a caller sees
    every breach at once. Building twice over the same records answers equal dicts: nothing
    here reads a clock or any other non-deterministic source.
    """
    entries: list[dict[str, Any]] = []
    entries.extend(_veto_entries(job))
    entries.extend(_veto_answer_entries(job))
    entries.extend(_injection_entries(job))
    entries.extend(_rerun_entries(job))
    entries.extend(_edit_entries(job))
    entries.extend(_steering_entries(job))
    entries.extend(_run_log_entries(job))

    problems: list[str] = []
    seen_refs: set[str] = set()
    for entry in entries:
        ref = entry.get("record_ref")
        if isinstance(ref, str):
            if ref in seen_refs:
                problems.append(f"duplicate record_ref {ref!r}")
            else:
                seen_refs.add(ref)
        problems.extend(ownership_entry_problems(entry))
    if problems:
        raise OwnershipError("; ".join(problems))

    entries.sort(key=lambda e: (e["ts"] == "", e["ts"], e["record_ref"]))

    fingerprint_numbers: dict[str, int] = {}
    next_number = 1
    for entry in entries:
        recorded_as = entry["actor"].get("recorded_as", "")
        if isinstance(recorded_as, str) and recorded_as.startswith("tf:"):
            if recorded_as not in fingerprint_numbers:
                fingerprint_numbers[recorded_as] = next_number
                next_number += 1
            entry["actor"]["token_number"] = fingerprint_numbers[recorded_as]

    return {"schema": OWNERSHIP_SCHEMA, "job_id": job.job_id, "entries": entries}
