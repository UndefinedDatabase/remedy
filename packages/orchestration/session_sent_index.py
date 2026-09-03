"""
Session sent-hash index — semantic dedupe bookkeeping (F109 T001a).

Remembers which prompt segments have PROVABLY been delivered to a given provider
session, so that a later call which RESUMES that same session can skip resending
them. This module is the bookkeeping half of F109 and nothing else.

The scope rule of the whole feature, verbatim, and it binds every line below:
RESUMED SESSION ONLY, PROVEN SENDS ONLY. "Proven" is the load-bearing word: a
call that did not succeed did not reach the session, and a call with no session
id has no session to remember, so neither is ever recorded. An index that
guesses what the model holds is worse than no index at all, because the
composition hook downstream would then replace content the model never saw.

This module is PURE. It reads no file, writes no file, touches no network, calls
no provider, and imports nothing from ``packages.orchestration`` — the segment
hashes it stores are produced by ``prompt_segments.ComposedPrompt`` and handed
in by the caller, so there is no second hashing scheme here.

Scope boundary — deliberate absences (a reader searching here should find this
rather than conclude the wiring was forgotten):
  - The index is NOT persisted into the job's evidence here, and nothing here
    reads it back at process start. Writing ``as_evidence_dicts()`` into the run
    evidence at the ``on_call_finalized`` seam is F109 T001b; this module only
    provides the two seams that round trip (``as_evidence_dicts`` and
    ``session_sent_index_from_evidence``).
  - The resume-fallback DECISION lives here (T001b-i):
    ``invalidate_on_resume_fallback`` decides which session a fallen-back resume
    must forget. ITS CALL SITES NOW EXIST: ``pingpong_loop.py`` invokes it on the
    Builder path and again on the Reviewer path, passing the resumed ref the loop
    still holds, and the same commit added the ``record_finalized_call`` sites
    that populate the index (T001b-ii, landed at ``7451e9c7``).
  - The dedupe DECISION and the MARKER TEXT live here (T002a):
    ``should_dedupe_segment`` decides whether a segment may be replaced, and
    ``dedupe_marker_for_segment`` says what the replacement reads. THE WHOLE
    CHAIN ABOVE THEM NOW EXISTS: ``_dedupe_resumed_segments`` in
    ``pingpong_loop.py`` calls both (F109 T002b, landed at ``24352750``), both
    ``compose_*`` functions call that hook (``60343048``), and the config
    plumbing that supplies ``enabled`` landed at ``b245e1c9``. No prompt is
    rewritten HERE, which stays true and is a statement about this module rather
    than about the feature.

Public API::

    SessionSentIndexError           — the one error type of this module
    SessionSentIndex                — the per-session sent-hash index
    session_sent_index_from_evidence(rows) -> SessionSentIndex
    session_id_of_finalized_call(output) -> str
    record_finalized_call(index, output, manifest_rows) -> int
    invalidate_on_resume_fallback(index, output, resumed_ref="") -> bool
    DEDUPE_MIN_SEGMENT_CHARS        — default minimum length worth replacing
    dedupe_marker_for_segment(name) -> str
    should_dedupe_segment(text, sha256, sent_hashes, *, enabled, min_chars) -> bool
"""

from __future__ import annotations

from collections.abc import Container, Iterable, Mapping, Sequence


class SessionSentIndexError(Exception):
    """Raised on a malformed manifest row or a malformed evidence row."""


class SessionSentIndex:
    """Which segment hashes are PROVEN to have reached which provider session.

    Construct with no arguments for an empty index. Every session's hashes live
    in their own set, keyed by session id, so two sessions can never read each
    other's sends — the cross-session leak this feature exists to prevent.
    """

    def __init__(self) -> None:
        self._sent_by_session: dict[str, set[str]] = {}

    def record_call(
        self,
        session_id: str,
        manifest_rows: Iterable[Mapping[str, object]],
        *,
        ok: bool,
    ) -> int:
        """Record the segment hashes of ONE finalized call; return how many were new.

        ``manifest_rows`` is what ``ComposedPrompt.manifest_as_dicts()`` returns:
        a sequence of mappings, each carrying a ``"sha256"`` key whose value is the
        hex digest of that segment's text. The return value counts only the hashes
        this call added that the session did not already hold.

        Records NOTHING, and returns 0, when ``ok`` is false: an unsuccessful call
        did not reach the session. Records NOTHING, and returns 0, when
        ``session_id`` is not a non-empty string after stripping: an empty key would
        become one bucket that every sessionless call shares, which is a
        cross-session leak by construction. Neither case is an error; both are
        ordinary and both are silent.

        Raises ``SessionSentIndexError`` on a malformed manifest — a row that is not
        a mapping, a row with no ``"sha256"``, or a ``"sha256"`` that is not a
        non-empty string. That is a programming error, and it must not be allowed to
        degrade into a silently smaller index.
        """
        if not ok:
            return 0
        if not isinstance(session_id, str) or not session_id.strip():
            return 0

        # Validate the WHOLE manifest before touching the index, so a malformed
        # row leaves the index exactly as it was rather than half-updated.
        hashes = _segment_hashes_from_manifest(manifest_rows)
        if not hashes:
            return 0

        already_sent = self._sent_by_session.setdefault(session_id, set())
        added = {digest for digest in hashes if digest not in already_sent}
        already_sent.update(added)
        return len(added)

    def sent_hashes(self, session_id: str) -> frozenset[str]:
        """Every hash proven sent to that session; the empty frozenset if none.

        There is deliberately no second guard for a blank session id here: the
        emptiness of an empty id is a CONSEQUENCE of ``record_call`` refusing to
        create such a key, so the rule lives in exactly one place and a regression
        in it stays visible instead of being masked here.
        """
        return frozenset(self._sent_by_session.get(session_id, frozenset()))

    def was_sent(self, session_id: str, sha256: str) -> bool:
        """True only when that exact session already holds that exact hash."""
        return sha256 in self._sent_by_session.get(session_id, frozenset())

    def invalidate_session(self, session_id: str) -> None:
        """Drop that session's set entirely; an unknown session id is a no-op.

        This is the resume-fallback safety valve. Once a resume attempt has fallen
        back to full context, nothing about what the model still holds is proven any
        more, so the honest state is "nothing sent". A fallback can fire before any
        call to that session ever succeeded, which is why an unknown id is silent
        rather than an error.
        """
        self._sent_by_session.pop(session_id, None)

    def session_ids(self) -> tuple[str, ...]:
        """Every session id the index holds, SORTED, never dict-ordered."""
        return tuple(sorted(self._sent_by_session))

    def as_evidence_dicts(self) -> list[dict]:
        """JSON-ready rows, one per session, sorted by session id.

        Both levels are sorted — the rows by session id, the hashes within a row —
        so two runs that made the same sends produce byte-identical evidence.
        """
        return [
            {
                "session_id": session_id,
                "sent_sha256": sorted(self._sent_by_session[session_id]),
            }
            for session_id in self.session_ids()
        ]


def session_sent_index_from_evidence(
    rows: Iterable[Mapping[str, object]],
) -> SessionSentIndex:
    """Rebuild an index from what ``as_evidence_dicts()`` produced.

    This is the restart honesty seam: an index rebuilt after a process restart
    contains exactly what the evidence proves and never more. Raises
    ``SessionSentIndexError`` on a row that is not a mapping, a row whose
    ``"session_id"`` is not a non-empty string, or a ``"sent_sha256"`` that is not
    a sequence of non-empty strings.
    """
    index = SessionSentIndex()
    for position, row in enumerate(rows):
        if not isinstance(row, Mapping):
            raise SessionSentIndexError(
                f"evidence row {position} is not a mapping: {type(row).__name__}"
            )
        session_id = row.get("session_id")
        if not isinstance(session_id, str) or not session_id.strip():
            raise SessionSentIndexError(
                f"evidence row {position} has no non-empty string 'session_id': {session_id!r}"
            )
        hashes = _evidence_hashes(row.get("sent_sha256"), position)
        index._sent_by_session.setdefault(session_id, set()).update(hashes)
    return index


def session_id_of_finalized_call(output: object) -> str:
    """The provider session a finalized call belongs to, or ``""`` when it has none.

    ``output`` is read DUCK-TYPED on purpose. This module deliberately does not
    import ``BuilderOutput`` or ``ReviewerOutput`` from ``pingpong_provider``,
    because that import would make the bookkeeping depend on the provider layer it
    exists to stay independent of. Both roles carry the same fields over exactly
    what is read here, so one reader serves both and no role argument is needed.

    The reading reproduces ``pingpong_loop.py`` exactly — ``str(actuals.get(
    "session_id") or "")`` over ``usage_actuals or {}`` — so the loop and the index
    can never disagree about which string names a session. A missing or None
    ``usage_actuals`` reads as an empty mapping, and None, 0 and ``""`` all become
    ``""``.

    A ``usage_actuals`` that is present but is NOT a mapping returns ``""`` rather
    than raising: this function reads foreign evidence, and an unusable reading
    means "no session", never a crash in the loop.
    """
    actuals = getattr(output, "usage_actuals", None)
    if not isinstance(actuals, Mapping):
        return ""
    return str(actuals.get("session_id") or "")


def record_finalized_call(
    index: SessionSentIndex,
    output: object,
    manifest_rows: Iterable[Mapping[str, object]],
) -> int:
    """Record ONE finalized call into ``index``; return what ``record_call`` returned.

    This is the scope rule reaching the adapter: PROVEN SENDS ONLY. The call counts
    as proven only when the output carries no ``error``, and that is what travels
    into ``record_call`` as ``ok``.

    Neither guard is re-implemented here. A call with no session id records nothing
    by the rule already inside ``record_call``, not by a second rule at this level,
    so each rule keeps exactly one site at which it can regress. This function only
    translates an output object into the three arguments ``record_call`` already
    understands.
    """
    return index.record_call(
        session_id_of_finalized_call(output),
        manifest_rows,
        ok=not getattr(output, "error", ""),
    )


def invalidate_on_resume_fallback(
    index: SessionSentIndex,
    output: object,
    resumed_ref: str = "",
) -> bool:
    """Forget the RESUMED session when a resume attempt fell back; True if it did.

    Does nothing and returns False unless the output carries ``resume_fallback``.
    Once a resume has fallen back to full context, nothing about what the model
    still holds is proven, so the honest state for that session is "nothing sent".

    WHY THE THIRD ARGUMENT IS LOAD-BEARING and not decorative: on the fallback path
    ``pingpong_loop.py`` REPLACES the output object — it calls the provider again
    with ``resume=None`` and only then sets ``resume_fallback`` on the NEW output.
    That second output resumed nothing, so its own ``resume_session_ref`` is ``""``
    and the id of the session that failed survives only in the loop's own
    ``builder_resume_ref`` / ``reviewer_resume_ref`` variable. An adapter reading
    only the output object would therefore invalidate NOTHING on exactly the path
    invalidation exists for. ``resumed_ref`` is how a caller passes the id it still
    holds; the output-object reading is kept for callers that have no such variable.

    A ref that is empty after stripping invalidates nothing and returns False:
    invalidating an unnamed session would be a guess, and guessing is the one thing
    this module refuses to do.
    """
    if not getattr(output, "resume_fallback", False):
        return False
    ref = (resumed_ref or getattr(output, "resume_session_ref", "")).strip()
    if not ref:
        return False
    index.invalidate_session(ref)
    return True


# The minimum segment length worth replacing at all. A marker has its OWN length,
# so replacing a tiny segment can cost more than it saves: the marker for a
# typical segment name runs to roughly forty characters, so a floor of 200 keeps
# the replacement worth making by a factor of several. This is a DEFAULT, not a
# law — both functions below take an override.
DEDUPE_MIN_SEGMENT_CHARS = 200


def dedupe_marker_for_segment(name: str) -> str:
    """The short reference marker that REPLACES an already-sent segment's text.

    The NAME stays inside the marker deliberately: the model must still be able to
    refer to the segment it is no longer being shown, so the marker withholds the
    content without withholding the means of asking for it back.

    Raises ``SessionSentIndexError`` when ``name`` is not a non-empty string after
    stripping. A nameless marker would tell the model that something it cannot
    identify was withheld, which is worse than simply sending the segment again.
    """
    if not isinstance(name, str) or not name.strip():
        raise SessionSentIndexError(
            f"a dedupe marker needs a non-empty segment name: {name!r}"
        )
    return f"[unchanged: {name}, previously provided]"


def should_dedupe_segment(
    text: str,
    sha256: str,
    sent_hashes: Container[str],
    *,
    enabled: bool = True,
    min_chars: int = DEDUPE_MIN_SEGMENT_CHARS,
) -> bool:
    """Whether this segment may be replaced by its marker; the WHOLE decision.

    True only when every condition holds: dedupe is ``enabled``, ``sha256`` is a
    non-empty string that ``sent_hashes`` already contains, and ``text`` is a
    string of at least ``min_chars`` characters. ``sent_hashes`` is any container
    supporting ``in`` — the frozenset ``SessionSentIndex.sent_hashes()`` returns is
    the intended caller. The length comparison is ``>=``, so a segment of exactly
    ``min_chars`` IS deduped and one character fewer is not.

    ``enabled`` is consulted FIRST and alone, so the config kill switch disables
    dedupe provably and totally rather than mostly.
    """
    if not enabled:
        return False
    # MALFORMED INPUT RETURNS FALSE RATHER THAN RAISING, and the contrast with
    # record_call is deliberate rather than an inconsistency: a bad manifest
    # corrupts the index silently and so must be loud, whereas a bad dedupe input
    # has an obviously correct safe answer — send the full content. Correctness
    # before savings.
    if not isinstance(sha256, str) or not sha256.strip():
        return False
    if sha256 not in sent_hashes:
        return False
    if not isinstance(text, str):
        return False
    return len(text) >= min_chars


def _segment_hashes_from_manifest(
    manifest_rows: Iterable[Mapping[str, object]],
) -> list[str]:
    """The ``"sha256"`` of every manifest row, in order; raises on a malformed row."""
    hashes: list[str] = []
    for position, row in enumerate(manifest_rows):
        if not isinstance(row, Mapping):
            raise SessionSentIndexError(
                f"manifest row {position} is not a mapping: {type(row).__name__}"
            )
        if "sha256" not in row:
            raise SessionSentIndexError(f"manifest row {position} has no 'sha256' key")
        digest = row["sha256"]
        if not isinstance(digest, str) or not digest.strip():
            raise SessionSentIndexError(
                f"manifest row {position} has no non-empty string 'sha256': {digest!r}"
            )
        hashes.append(digest)
    return hashes


def _evidence_hashes(value: object, position: int) -> list[str]:
    """The hashes of one evidence row; raises unless a sequence of non-empty strings.

    ``str`` and ``bytes`` are rejected explicitly even though both are sequences:
    iterating a bare string would silently accept its CHARACTERS as hashes, which
    is precisely the kind of quiet corruption this seam exists to refuse.
    """
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise SessionSentIndexError(
            f"evidence row {position} has no 'sent_sha256' sequence: {value!r}"
        )
    hashes: list[str] = []
    for digest in value:
        if not isinstance(digest, str) or not digest.strip():
            raise SessionSentIndexError(
                f"evidence row {position} has a bad 'sent_sha256' entry: {digest!r}"
            )
        hashes.append(digest)
    return hashes
