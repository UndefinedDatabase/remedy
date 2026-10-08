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
export at every job terminal. F304 adds the operator's decline of a job's result (DECISION F304
D5), read through `job_apply`.
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
#: and plan approval. The first five run-log events read here are round 1's; `plan_approved`
#: joins them in round 2 (S4).
_RUN_LOG_EVENTS = ("job_paused", "task_paused", "job_resumed", "task_resumed", "job_stopped",
                   "plan_approved")

#: S3's `clarification_source` result mapped onto the actor `kind` its class carries.
_CLARIFICATION_ACTOR_KIND = {"human": "operator", "default": "default_policy", "planner": "remedy"}

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


def _hunk_decision_entries(job: Any) -> list[dict[str, Any]]:
    """S1 — every DECIDED row (approved or rejected) of every attempt's hunk ledger. An
    undecided (`HUNK_STATE_PENDING`) row yields nothing: nobody has said anything about it
    yet. The actor names no door (`ownership_actor("")`) because a hunk decision's record
    carries none — see the module docstring."""
    from packages.orchestration.hunk_decision_record import HUNK_DECISIONS_METADATA_KEY
    from packages.orchestration.hunk_ledger import HUNK_STATE_APPROVED, HUNK_STATE_REJECTED

    out: list[dict[str, Any]] = []
    records = (job.metadata or {}).get(HUNK_DECISIONS_METADATA_KEY) or {}
    for attempt_key, value in records.items():
        task_id = str(value.get("task_id", ""))
        for row in value.get("hunks") or []:
            state = row.get("state")
            if state == HUNK_STATE_APPROVED:
                action = "hunk_approved"
            elif state == HUNK_STATE_REJECTED:
                action = "hunk_rejected"
            else:
                continue                                          # HUNK_STATE_PENDING: undecided
            out.append({
                "record_ref": f"hunk:{attempt_key}:{row.get('id')}",
                "ts": str(value.get("decided_at", "")),
                "actor": ownership_actor(""),
                "action": action,
                "task_id": task_id,
                "text": row.get("reason", "") if isinstance(row.get("reason"), str) else "",
                "consequence": {
                    "kind": "landing", "task_ids": [task_id], "ref": row.get("landing", ""),
                },
                "detail": {"attempt": str(value.get("attempt", "")), "hunk_id": row.get("id", "")},
            })
    return out


def _decision_answer_entries(job: Any) -> list[dict[str, Any]]:
    """S2 — every ANSWERED task decision. An OPEN one yields nothing: it has no answer to
    attribute yet. A default answer, applied by `auto_apply_safe_default`, is recorded under
    `kind="default_policy"` — the documented default the operator accepted at plan approval,
    not a human's own words."""
    from packages.orchestration.escalation import (
        ANSWER_SOURCE_DEFAULT,
        ESCALATION_STATUS_ANSWERED,
        JOB_METADATA_ESCALATIONS_KEY,
    )

    out: list[dict[str, Any]] = []
    records = (job.metadata or {}).get(JOB_METADATA_ESCALATIONS_KEY) or []
    for record in records:
        if not isinstance(record, dict) or record.get("status") != ESCALATION_STATUS_ANSWERED:
            continue
        answer_source = record.get("answer_source")
        if answer_source == ANSWER_SOURCE_DEFAULT:
            actor = ownership_actor(answer_source, kind="default_policy")
        else:
            actor = ownership_actor(answer_source)
        task_id = str(record.get("task_id", ""))
        out.append({
            "record_ref": f"decision:{record.get('decision_id', '')}",
            "ts": str(record.get("answered_at", "")),
            "actor": actor,
            "action": "decision_answered",
            "task_id": task_id,
            "text": record.get("answer", "") if isinstance(record.get("answer"), str) else "",
            "consequence": {"kind": "answer_to_task", "task_ids": [task_id], "ref": ""},
            "detail": {"question": record.get("question", "")},
        })
    return out


def _clarification_entries(job: Any) -> list[dict[str, Any]]:
    """S3 — every RESOLVED bundled clarification (human, default or planner). An unresolved
    one (`clarification_source` reads `"unresolved"`) yields nothing. These records carry no
    time of their own, so `ts` is always ""."""
    from packages.orchestration.job_plan import clarification_source

    out: list[dict[str, Any]] = []
    body = job.task_plan or {}
    for record in body.get("clarifications_resolved") or []:
        source = clarification_source(record)
        if source == "unresolved":
            continue
        rec = record if isinstance(record, dict) else {}
        out.append({
            "record_ref": f"clarification:{rec.get('id', '')}",
            "ts": "",
            "actor": ownership_actor(source, kind=_CLARIFICATION_ACTOR_KIND[source]),
            "action": "clarification_answered",
            "task_id": "",
            "text": rec.get("answer", "") if isinstance(rec.get("answer"), str) else "",
            "consequence": {"kind": "plan_input", "task_ids": [], "ref": ""},
            "detail": {
                "question": rec.get("question", ""),
                "default_answer": rec.get("default_answer", ""),
            },
        })
    return out


def _plan_approval_actor_text(mode: str, body: Any) -> tuple[dict[str, Any], str]:
    """The actor and text one `plan_approved` moment carries, shared by the run-log event
    branch below and the plan-body fallback so the two agree by construction. An unattended
    approval (`mode == AUTO_APPROVAL_MODE`) is `auto_approved` and carries the plan body's own
    audited reason, or "" without one; any other mode carries neither door nor words."""
    from packages.orchestration.job_plan import AUTO_APPROVAL_MODE

    if mode != AUTO_APPROVAL_MODE:
        return ownership_actor(""), ""
    audit = (body or {}).get("_approval_audit") or {}
    reason = audit.get("reason")
    text = reason if isinstance(reason, str) else ""
    return ownership_actor(mode, auto_approved=True), text


def _plan_approval_body_entries(job: Any, *, event_recorded: bool) -> list[dict[str, Any]]:
    """S4's second half, read from the plan body rather than the run log: a rejected plan
    (`_approval == "rejected"`) always yields its own entry, since rejection writes no
    `plan_approved` event; an approved plan yields `plan_approved:body` ONLY when no
    `plan_approved` event was already read for this job (`event_recorded`) — the event is the
    primary record when both exist."""
    body = job.task_plan or {}
    approval = body.get("_approval")
    out: list[dict[str, Any]] = []
    if approval == "rejected":
        out.append({
            "record_ref": "plan_rejected",
            "ts": "",
            "actor": ownership_actor(""),
            "action": "plan_rejected",
            "task_id": "",
            "text": "",
            "consequence": {"kind": "plan_rejected", "task_ids": [], "ref": ""},
            "detail": {},
        })
    elif approval == "approved" and not event_recorded:
        mode = str((body.get("_approval_audit") or {}).get("mode", ""))
        actor, text = _plan_approval_actor_text(mode, body)
        out.append({
            "record_ref": "plan_approved:body",
            "ts": "",
            "actor": actor,
            "action": "plan_approved",
            "task_id": "",
            "text": text,
            "consequence": {"kind": "plan_approved", "task_ids": [], "ref": ""},
            "detail": {},
        })
    return out


def _decline_entries(job: Any) -> list[dict[str, Any]]:
    """F304's decline (DECISION F304 D5): the operator's decline of the job's result, read from
    the job's own record through `job_apply`, which owns that record's shape. A job whose result
    was never declined yields nothing."""
    from packages.orchestration.job_apply import job_result_decline

    record = job_result_decline(job)
    if record is None:
        return []
    return [{
        "record_ref": "result_declined",
        "ts": str(record.get("declined_at", "")),
        "actor": ownership_actor(record.get("source")),
        "action": "result_declined",
        "task_id": "",
        "text": str(record.get("reason", "")),
        "consequence": {"kind": "declined", "task_ids": [], "ref": ""},
        "detail": {},
    }]


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
        # S4: the dedupe key is now (event, request_id or timestamp) — the same value
        # record_ref uses — so a `plan_approved` event, which carries no request_id, dedupes
        # by its own timestamp instead of colliding with every other one on an empty string.
        ref = request_id if request_id else raw_ts
        key = (name, ref)
        if key in seen:
            continue
        seen.add(key)

        task_id = str(event.get("task_id") or "")
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
        elif name == "plan_approved":
            entry_ts = raw_ts
            entry_task_id = ""
            mode = str(md.get("approval_mode", ""))
            actor, text = _plan_approval_actor_text(mode, job.task_plan)
            consequence = {
                "kind": "plan_approved",
                "task_ids": list(md.get("task_ids") or []),
                "ref": "",
            }
            detail = {"approval_mode": mode}
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
    entries.extend(_hunk_decision_entries(job))
    entries.extend(_decision_answer_entries(job))
    entries.extend(_clarification_entries(job))
    entries.extend(_decline_entries(job))
    run_log_entries = _run_log_entries(job)
    entries.extend(run_log_entries)
    event_recorded = any(e["action"] == "plan_approved" for e in run_log_entries)
    entries.extend(_plan_approval_body_entries(job, event_recorded=event_recorded))

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
