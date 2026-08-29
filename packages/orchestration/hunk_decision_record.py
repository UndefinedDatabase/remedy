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

THE TWO RECORDING DOORS ARE NOT TOTAL, and unlike this module's two pure dependencies they must
not pretend to be. ``hunk_approval`` and ``hunk_ledger`` are text-in, text-out and run while the
approval screen renders, so a raise there takes down the very screen that exists to show the
operator what is strange, and totality there costs nothing because there is nothing that can
legitimately fail. Here there is: the two doors READ AND MUTATE ``job.metadata``, and a job whose
metadata is not a dict, or whose attribute access raises, is a REAL programming error the caller
must see. Flattening that into a polite refusal would report "the diff was untrustworthy" for a
broken caller. So they catch nothing they cannot name. A non-string ``task_id`` or ``attempt`` is
NOT that class — those are identifiers a caller may legitimately hand over as a ``UUID`` or an
``int`` — and they are coerced to text. THE READER BELOW IS THE ONE EXCEPTION AND IT IS TOTAL:
``load_latest_hunk_ledger_from_metadata`` mutates nothing and answers an EMPTY ledger for every
input it cannot read, because it runs while the next builder prompt is being composed, where a
raise would take down the ROUND rather than surface a caller's mistake to an operator.

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
    load_latest_hunk_ledger_from_metadata — the READ side: a task's LATEST decision, as a ledger
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
    import_hunk_ledger,
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


# One record's ``decided_at`` read as a time, or nothing — the ranking key of the reader below.
def _parsed_decision_stamp(value: Any) -> datetime | None:
    """``value`` as a ``datetime``, or ``None`` when ``datetime.fromisoformat`` will not parse it.

    THE SEPARATE PARSE GUARD, deliberately NOT folded into the structural guard below. A stamp
    that does not parse belongs to an ORDINARY record the reader must still rank — it simply
    loses to every record that carries a readable one — while a SHAPE the reader cannot read at
    all is a different fault with a different answer, an empty ledger. Keeping the two apart is
    what makes each of them observable: a red-proof aimed at the structural guard feeds a
    malformed shape, one aimed at this guard feeds a malformed stamp, exactly as
    ``hunk_ledger.import_hunk_ledger`` separates its own structural guard from ``_total_text``.

    Never raises: ``datetime.fromisoformat`` refuses a non-string with a ``TypeError`` and an
    unreadable string with a ``ValueError``, and both mean one thing here — this record carries
    no time to order it by."""
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return None


# The READ side of this module, and the inverse of what the two doors above write: the LATEST
# decision one task has recorded, rebuilt into the ledger a repair prompt can quote.
def load_latest_hunk_ledger_from_metadata(
    metadata: Any,
    *,
    task_id: Any,
) -> HunkDecisionLedger:
    """The ledger of the decision most recently RECORDED for ``task_id`` in ``metadata``.

    ``metadata`` is a job's ``metadata`` MAPPING — the very object the two doors above write
    into — and never a job, a job id or a path. ``task_id`` is coerced to text, exactly as the
    doors coerce it before composing an attempt key.

    SELECTION, the whole rule in one sentence: among the records under
    ``HUNK_DECISIONS_METADATA_KEY`` whose ``task_id`` equals ``str(task_id)``, the winner is the
    one carrying the GREATEST ``decided_at`` that ``datetime.fromisoformat`` parses; a record
    whose ``decided_at`` does not parse can NEVER beat one that does; and if none parses, or
    several tie, the LAST in the mapping's iteration order wins — which for a record loaded from
    JSON is insertion order, so the most recently written of them. Nothing here sorts the KEYS.
    An attempt key is ``task:attempt`` and ``"t-1:10"`` sorts before ``"t-1:9"``, so ranking by
    id would start answering with the wrong attempt the moment a task reaches ten.

    THE REBUILD IS ``hunk_ledger.import_hunk_ledger``'s, handed the winning record WHOLE. That
    works because ``_LEDGER_ROWS_KEY`` above and the export root key the importer reads are
    deliberately the SAME name, and the comment on that constant is where the deliberateness is
    recorded. A stored record therefore ALREADY has the shape the importer reads, so this module
    walks no rows of its own: there is ONE inverse of the export in this repository rather than
    two, and two would drift apart the day either shape moves.

    TOTAL — it never raises, on any input at all: ``None`` metadata, a non-mapping, no decisions
    key, a decisions value that is not a mapping, a record that is not a mapping, a record
    missing a key. Every one of them yields an EMPTY ledger and never a PARTIAL one, for the
    reason ``import_hunk_ledger`` gives — a half-built result's missing half is invisible to
    whoever reads it next. THE STRUCTURAL GUARD IS THE ONE ``try`` BELOW and there is
    deliberately no second one inside it, because a redundant inner layer would make this one
    unobservable and a guard no test can redden is a guard nobody knows is there;
    ``_parsed_decision_stamp`` above is the SEPARATE parse guard.

    AN EMPTY LEDGER IS ALSO THE HONEST ANSWER FOR "this task recorded no decision at all", and
    that is NOT an error. A caller cannot tell the two apart, deliberately: to a prompt they mean
    the same thing — there is nothing of the operator's to quote — so a refusal object here would
    buy nothing but the same branch written twice at every call site.

    DELIBERATE ABSENCE — THIS PERFORMS NO STORAGE I/O, and taking a MAPPING rather than a job id
    or a path is how that is enforced rather than merely promised. A reader who came here looking
    for a job load, a persisting write or a file read should stop at this paragraph: there is
    none, and the CALLER that already holds the job supplies the mapping. DECISION F033 D4's
    standing property — nothing the write door imports drags a storage write or an applier behind
    it — is stated in the module docstring above, and this function is bound by it too."""
    try:
        wanted = str(task_id)
        winner: Any = None
        best: datetime | None = None
        for record in metadata[HUNK_DECISIONS_METADATA_KEY].values():
            if record["task_id"] != wanted:
                continue
            stamp = _parsed_decision_stamp(record["decided_at"])
            # An unparseable stamp NEVER displaces a parseable one. Everything else displaces:
            # the first match, a later record while the incumbent has no stamp at all, a greater
            # stamp, and an EQUAL stamp — that last one is how "several tie, the last wins" is
            # spelled, and it is why the comparison is ``>=`` rather than ``>``.
            if winner is None or best is None:
                winner, best = record, stamp
            elif stamp is not None and stamp >= best:
                winner, best = record, stamp
        if winner is None:
            return HunkDecisionLedger(())
        return import_hunk_ledger(winner)
    except Exception:
        return HunkDecisionLedger(())
