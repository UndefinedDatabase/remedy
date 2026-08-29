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

THERE ARE TWO DOORS AND ONE IMPLEMENTATION, and the second door is why this shape exists.
``packages/orchestration/diff_view_source.py``'s ``build_diff_view`` already resolved an
attempt's artifact, already read it under ``DIFF_VIEW_MAX_ARTIFACT_BYTES``, already parsed it and
already decided ``truncated``. A caller holding that ENVELOPE has nothing to hand a text-only
recorder but the raw diff again, and re-reading and re-parsing it here would put a SECOND copy of
that byte ceiling and that truncation rule beside the first, free to drift apart from it. So
``record_hunk_decision_from_view`` takes the parsed view and holds the whole implementation, and
``record_hunk_decision`` keeps its text signature by parsing and delegating. The envelope carries
one axis the bare parse does not — ``available`` — and the ABSENCE that axis names gets a refusal
of its own, because an absent artifact is not an operator's mistake.

Public API::

    HUNK_DECISIONS_METADATA_KEY — str, the ``job.metadata`` key every decision is recorded under
    HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW — str, refusal code for a view that hides hunks
    HUNK_RECORD_REFUSAL_NO_DIFF — str, refusal code for an attempt whose diff is not there at all
    HunkDecisionRecord — the attempt key, the ledger, and the exported record written to the job
    record_hunk_decision_from_view — the ONE implementation, over an ALREADY PARSED view
    record_hunk_decision — the TEXT door: parse a diff, then delegate to the one above
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
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
#: some of the attempt's hunks. This is one of the TWO refusal codes this module mints of its own;
#: every other refusal is ``decide_hunk_approval``'s and is returned UNCHANGED, code, message and
#: offending ids intact, because this module mints no second vocabulary for faults that already
#: have one. The SPELLING deliberately matches ``hunk_subset_diff.SUBSET_REFUSAL_UNTRUSTWORTHY_VIEW``,
#: which refuses the same shape for the neighbouring reason: one untrustworthy view, one word for it.
HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW = "untrustworthy_view"

#: The attempt has no diff to decide over at all — the viewer's envelope reports ``available``
#: False, so the artifact it went looking for is simply not there. This is the SECOND and last
#: refusal code this module mints. WHY it must exist rather than letting the decision core answer:
#: an unavailable envelope carries an EMPTY ``files`` list, so the known id set is empty, so every
#: approved id would be absent from it and ``decide_hunk_approval`` would answer
#: ``REFUSAL_UNKNOWN_HUNK`` — telling the operator their ids are wrong when the truth is that the
#: ARTIFACT is missing and they were never shown an id to get right. That is the same reasoning
#: ``hunk_subset_diff.py`` gives for deciding untrustworthiness BEFORE absence: a fault in what the
#: system could show must not come back as a fault in what the operator asked for.
HUNK_RECORD_REFUSAL_NO_DIFF = "no_diff_available"

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


def _known_hunk_ids(view: Mapping[str, Any]) -> list[str]:
    """Every hunk id of every file, IN THE VIEW'S OWN ORDER — which is the DIFF's order, and the
    order ``build_hunk_ledger`` walks to emit its rows. Recovering it here rather than from the
    decision is the whole reason the ledger takes the known set as its first argument."""
    return [hunk["id"] for file_view in view["files"] for hunk in file_view["hunks"]]


# The VIEW entry point: an already-parsed view, a decision, and the job it is recorded on. This
# one holds the whole implementation; the text door below parses and delegates to it.
def record_hunk_decision_from_view(
    job: Any,
    *,
    task_id: Any,
    attempt: Any,
    attempt_view: Mapping[str, Any],
    approved: Iterable[str],
    rejected: Iterable[Any],
    now: datetime,
) -> HunkDecisionRecord | HunkApprovalRefusal:
    """Validate one hunk decision over an ALREADY PARSED ``attempt_view`` and RECORD it on ``job``.

    ``attempt_view`` is either ``diff_view_source.build_diff_view``'s envelope — which a caller
    rendering the F037 viewer already holds — or ``diff_parser.parse_unified_diff_to_view``'s bare
    view. Both are accepted, and the availability step below is the only place they differ.

    Returns a ``HunkDecisionRecord`` naming where it landed, or a ``HunkApprovalRefusal``. When a
    refusal is returned NOTHING is written to ``job.metadata`` at all: a refused decision is not a
    decision, and half-recording one would leave the operator's record claiming something nobody
    decided. Persisting the mutated job is the caller's — see the module docstring."""
    # AVAILABILITY IS DECIDED FIRST, AND ITS DEFAULT IS ``True``, and both halves of that are
    # load-bearing. ``build_diff_view`` carries an availability axis because the artifact it goes
    # looking for can simply be absent; ``parse_unified_diff_to_view`` carries NONE and emits no
    # ``available`` key at all, because text that exists IS available. Defaulting to ``True`` is
    # what lets a caller hand over a bare parse without being refused for a key that parser never
    # emits. It is decided BEFORE truncation because an unavailable envelope is not truncated, it
    # is ABSENT — there was never an artifact to cut short.
    if not attempt_view.get("available", True):
        # The envelope's OWN ``reason`` is quoted so the operator learns WHICH absence it was —
        # a missing evidence directory, a missing artifact and an unknown task run are three
        # different things to go and fix.
        reason = attempt_view.get("reason")
        return HunkApprovalRefusal(
            HUNK_RECORD_REFUSAL_NO_DIFF,
            "The attempt's diff is not available to decide over — the view reports it missing "
            f"because {reason!r} — so there are no hunks to approve or reject and a decision "
            "over it cannot be recorded at all.",
            (),
        )

    # ``truncated`` and ``files`` are read by SUBSCRIPT rather than by ``.get``: a mapping without
    # them is not a view, and defaulting either one would silently record an EMPTY decision over a
    # caller's mistake instead of letting that mistake surface. ``available`` above is the ONE key
    # read with a default, for the reason stated there.
    if attempt_view["truncated"]:
        # The known id set is INCOMPLETE, so every hunk the parser never showed would be recorded
        # as ``pending`` — a POSITIVE claim that the operator left it undecided, when in truth
        # nobody was ever shown it. ``hunk_ids`` is empty because no single id is at fault.
        return HunkApprovalRefusal(
            HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW,
            "The attempt's diff was truncated before it was fully parsed, so which hunks it does "
            "not show is unknown and a decision over it cannot be recorded honestly.",
            (),
        )

    known_ids = _known_hunk_ids(attempt_view)
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


# The TEXT entry point: a diff as text, a decision, and the job the decision is recorded on. It
# holds no second copy of anything above — it parses and delegates, and that is the whole of it.
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

    This is the TEXT door of the two. It parses the diff and hands the resulting view to
    ``record_hunk_decision_from_view``, which holds the implementation and documents the
    guarantees; a caller that ALREADY has the viewer's envelope should call that one directly
    rather than serialise a diff it has already parsed."""
    return record_hunk_decision_from_view(
        job,
        task_id=task_id,
        attempt=attempt,
        attempt_view=parse_unified_diff_to_view(attempt_diff_text),
        approved=approved,
        rejected=rejected,
        now=now,
    )
