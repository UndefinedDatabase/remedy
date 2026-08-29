"""RECORDING an operator's hunk decision on the job it belongs to — the write door's effect.

WHY this module exists: DECISION F033 D4 rules what the ``approve_hunks`` write door actually
DOES. It validates the decision, builds the hunk ledger with every landing ``unattempted``, and
records that ledger on the job; the apply runs later, on the job branch, where an APPROVED patch
intent exists. This module is that effect. It is the seam between an operator's decision and the
job it is recorded on, and it does nothing else.

DELIBERATE ABSENCE — IT APPLIES NOTHING. It does not import
``packages/orchestration/hunk_apply.py``, ``packages/orchestration/source_apply.py`` or any other
applicator, it touches no repository, and it never learns whether the approved set would apply
cleanly. That is a CONSTRAINT rather than an oversight, and it exists to satisfy in SUBSTANCE the
guard ``TestCommandDoorImportGuard`` in ``tests/ui_server/test_command_channel.py`` states in
words: "the write door ENQUEUES, it never applies". That guard's ``_door_imports`` walks the AST
of the door's own methods and collects DIRECT imports only, so a door importing a module that
imports the applier would PASS it while running the applier inside an HTTP handler — defeating the
guard by NAME rather than by substance. Nothing reachable from the door may drag the applier behind
it, so this module, which the door will import, drags nothing.

DELIBERATE ABSENCE — IT PERSISTS NOTHING. It MUTATES ``job.metadata`` and returns; writing the job
back to disk is the CALLER's, exactly as ``escalation.answer_task_decision`` answers a decision and
leaves the persisting call to the door. ``packages/orchestration/ui_server.py``'s
``_dispatch_decision_resolve`` says so in as many words, and DECISION F009 D21 makes both halves
one effect there. So this module imports no storage either, and a reader who came looking for the
write should stop at this paragraph: there is none here, and that is on purpose.

It imports the standard library, ``packages.orchestration.diff_parser``,
``packages.orchestration.hunk_approval`` and ``packages.orchestration.hunk_ledger``, and nothing
else. A reader who wants whether a decision is coherent at all wants
``packages/orchestration/hunk_approval.py``; one who wants the record's SHAPE wants
``packages/orchestration/hunk_ledger.py``; one who wants which bytes an approved selection means
wants ``packages/orchestration/hunk_subset_diff.py``; one who wants the apply seam itself wants
``packages/orchestration/hunk_apply.py``.

THIS MODULE IS NOT TOTAL, and unlike its two pure dependencies it must not pretend to be.
``hunk_approval`` and ``hunk_ledger`` are text-in, text-out and run while the approval screen
renders, so a raise there takes down the very screen that exists to show the operator what is
strange, and totality there costs nothing because there is nothing that can legitimately fail.
Here there is: this module READS AND MUTATES ``job.metadata``, and a job whose metadata is not a
dict, or whose attribute access raises, is a REAL programming error the caller must see.
Flattening that into a polite refusal would report "the diff was untrustworthy" for a broken
caller. So it catches nothing it cannot name. A non-string ``task_id`` or ``attempt`` is NOT that
class — those are identifiers a caller may legitimately hand over as a ``UUID`` or an ``int`` — and
they are coerced to text.

Public API::

    HUNK_DECISIONS_METADATA_KEY — str, the ``job.metadata`` key every decision is recorded under
    HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW — str, the one refusal code this module mints
    HunkDecisionRecord — the attempt key, the ledger, and the exported record written to the job
    record_hunk_decision — validate one decision, build its ledger, and record it on the job
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from packages.orchestration.diff_parser import parse_unified_diff_to_view
from packages.orchestration.hunk_approval import HunkApprovalRefusal, decide_hunk_approval
from packages.orchestration.hunk_ledger import (
    HunkDecisionLedger,
    build_hunk_ledger,
    export_hunk_ledger,
)

#: The key on ``job.metadata`` under which every hunk decision is recorded.
HUNK_DECISIONS_METADATA_KEY = "hunk_decisions"

#: The view cannot be trusted to name every hunk — it is truncated, so the parser never showed
#: some of the attempt's hunks. This is the ONE refusal code this module mints of its own; every
#: other refusal is ``decide_hunk_approval``'s and is returned UNCHANGED, code, message and
#: offending ids intact, because this module mints no second vocabulary for faults that already
#: have one. The SPELLING deliberately matches ``hunk_subset_diff.SUBSET_REFUSAL_UNTRUSTWORTHY_VIEW``,
#: which refuses the same shape for the neighbouring reason: one untrustworthy view, one word for it.
HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW = "untrustworthy_view"

#: The key ``export_hunk_ledger`` writes its rows under, and the key this module writes them under
#: too — the ledger's OWN rows, unwrapped, so the record does not carry a ``hunks`` inside a
#: ``hunks``. RE-STATED rather than imported because that name is private in ``hunk_ledger``.
_LEDGER_ROWS_KEY = "hunks"

#: The four keys one recorded decision carries, and the only ones it carries.
_RECORD_KEYS = ("task_id", "attempt", "decided_at", _LEDGER_ROWS_KEY)


@dataclass(frozen=True)
class HunkDecisionRecord:
    """What was recorded, in the three forms a caller needs.

    ``attempt_key`` is where on ``job.metadata`` it landed, ``ledger`` is the structured record
    for anything that wants to render badges without re-reading the job, and ``exported`` is the
    JSON-safe dict actually written — the SAME object, not a copy, so a caller comparing them is
    comparing what is on the job."""

    attempt_key: str
    ledger: HunkDecisionLedger
    exported: dict


def _attempt_key(task_id: str, attempt: str) -> str:
    """The key one attempt's record lives under. Both halves arrive ALREADY coerced to text.

    A SECOND decision on the SAME key REPLACES the first rather than appending: an operator may
    revise a decision while the landing is still ``unattempted``, and two records for one attempt
    would leave the viewer choosing between them with nothing to choose on."""
    return f"{task_id}:{attempt}"


def _known_hunk_ids(view: dict) -> list[str]:
    """Every hunk id of every file, IN THE VIEW'S OWN ORDER — which is the DIFF's order, and the
    order ``build_hunk_ledger`` walks to emit its rows. Recovering it here rather than from the
    decision is the whole reason the ledger takes the known set as its first argument."""
    return [hunk["id"] for file_view in view["files"] for hunk in file_view["hunks"]]


# The one entry point: a diff, a decision, and the job the decision is recorded on.
def record_hunk_decision(
    job: Any,
    *,
    task_id: Any,
    attempt: Any,
    attempt_diff_text: str,
    approved: Iterable[str],
    rejected: Iterable[Any],
    now: datetime,
) -> HunkDecisionRecord | HunkApprovalRefusal:
    """Validate one hunk decision over ``attempt_diff_text`` and RECORD it on ``job``.

    Returns a ``HunkDecisionRecord`` naming where it landed, or a ``HunkApprovalRefusal``. When a
    refusal is returned NOTHING is written to ``job.metadata`` at all: a refused decision is not a
    decision, and half-recording one would leave the operator's record claiming something nobody
    decided. Persisting the mutated job is the caller's — see the module docstring."""
    view = parse_unified_diff_to_view(attempt_diff_text)
    if view["truncated"]:
        # The known id set is INCOMPLETE, so every hunk the parser never showed would be recorded
        # as ``pending`` — a POSITIVE claim that the operator left it undecided, when in truth
        # nobody was ever shown it. ``hunk_ids`` is empty because no single id is at fault.
        return HunkApprovalRefusal(
            HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW,
            "The attempt's diff was truncated before it was fully parsed, so which hunks it does "
            "not show is unknown and a decision over it cannot be recorded honestly.",
            (),
        )

    known_ids = _known_hunk_ids(view)
    decision = decide_hunk_approval(known_ids, approved, rejected)
    if isinstance(decision, HunkApprovalRefusal):
        return decision

    # ``apply_attempted`` is LEFT AT ITS DEFAULT, so every entry lands ``unattempted``. That is the
    # whole of DECISION F033 D4: recording a decision is not applying it, and a viewer must not
    # show a landing verdict before any apply has run. ``applied`` and ``landed_hunk_ids`` are
    # never passed from here — a later apply, on the job branch, is what revises those.
    ledger = build_hunk_ledger(known_ids, decision)

    task_text = str(task_id)
    attempt_text = str(attempt)
    attempt_key = _attempt_key(task_text, attempt_text)
    exported = dict(
        zip(
            _RECORD_KEYS,
            (
                task_text,
                attempt_text,
                now.isoformat(),
                export_hunk_ledger(ledger)[_LEDGER_ROWS_KEY],
            ),
        )
    )

    records = job.metadata.setdefault(HUNK_DECISIONS_METADATA_KEY, {})
    records[attempt_key] = exported
    return HunkDecisionRecord(attempt_key, ledger, exported)
