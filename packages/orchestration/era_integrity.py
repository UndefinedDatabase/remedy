"""F070 T002 — detecting the external-orchestration era's own failure modes.

When Remedy runs its own missions, the artifact a dispatched job hands back is
the only thing the evaluator can believe. The human-relayed split workflow
(docs/agents/split_workflow.md, in production since 2026-07-23) produced a
catalogue of ways that artifact can be wrong while LOOKING right, and every one
of them was found by a human reviewer rather than by any check. This module is
those reviewers' judgement, made mechanical.

Five classes, each extracted from a real finding in this repository's history
(the fixtures under ``tests/orchestration/fixtures/era/`` cite their commits):

* ``incomplete_handback_accounting`` — R-0141 / R-0143 / R-0145. The handback
  omits commits inside its own review range, ships a commit with no
  changed-files table, or states an external action (a PR created) as a fact
  without reporting it as an action taken.
* ``self_authored_verdict`` — R-0144. A verdict entry the reviewer never
  authored, presented as a review result while the review was still pending.
* ``silently_dropped_flag`` — R-0146. An interface advertises a flag and does
  not pass it through, so a preview request executes for real.
* ``self_consistency_proof`` — R-0147. A proof that asserts byte-identity but
  was compared against something other than the authoritative text — a
  verification claim that verifies only itself.
* ``transport_corrupted_authored_text`` — R-0148. Authored text that arrived
  corrupted (a markdown table row hard-wrapped across two physical lines) and
  was applied verbatim, faithfully, in its broken form.

**The integrity mechanism is the digest, not a wrap guard.** The feature file's
2026-07-27 note is explicit: the sha256-stamped authored-text pattern is
retained internally (hash on write, verify on read), while the copy-paste
wrap-guard rationale is transport-specific and obsolete inside Remedy. Remedy
therefore deliberately does NOT look for hard wraps here — a digest mismatch
catches every corruption a wrap guard would, and many it would not.

Every detector answers one question: does the artifact's own claim survive
being re-checked against the ground truth beside it? Nothing here re-runs a
build, contacts a provider or reads the repository.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# Defect kinds — one per finding class the era produced
# ---------------------------------------------------------------------------

DEFECT_INCOMPLETE_ACCOUNTING = "incomplete_handback_accounting"
DEFECT_SELF_AUTHORED_VERDICT = "self_authored_verdict"
DEFECT_DROPPED_FLAG = "silently_dropped_flag"
DEFECT_SELF_CONSISTENCY_PROOF = "self_consistency_proof"
DEFECT_CORRUPTED_AUTHORED_TEXT = "transport_corrupted_authored_text"

#: Defect kind -> the finding ids it was extracted from. Kept in code because a
#: flagged artifact should name the precedent a human can go read.
DEFECT_FINDING_CLASSES: dict[str, str] = {
    DEFECT_INCOMPLETE_ACCOUNTING: "R-0141/R-0143/R-0145",
    DEFECT_SELF_AUTHORED_VERDICT: "R-0144",
    DEFECT_DROPPED_FLAG: "R-0146",
    DEFECT_SELF_CONSISTENCY_PROOF: "R-0147",
    DEFECT_CORRUPTED_AUTHORED_TEXT: "R-0148",
}

#: Who is allowed to author a verdict. The worker never is — that is the whole
#: R-0144 lesson, and it is the same rule as builder-self-merge.
VERDICT_AUTHOR_REVIEWER = "reviewer"


@dataclass(frozen=True)
class EraDefect:
    """One flagged defect: what kind, which precedent, and what exactly is wrong."""

    kind: str
    detail: str
    finding_class: str = ""

    def to_json(self) -> dict[str, Any]:
        return {"kind": self.kind, "detail": self.detail,
                "finding_class": self.finding_class
                or DEFECT_FINDING_CLASSES.get(self.kind, "")}


def authored_text_digest(text: str) -> str:
    """The artifact-integrity digest: hash on write, verify on read."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class AuthoredText:
    """One authored text that crossed the dispatch boundary.

    ``declared_sha256`` was computed by the author BEFORE transport;
    ``applied_text`` is what actually landed. The pair is the whole mechanism.
    """

    name: str
    declared_sha256: str
    applied_text: str


@dataclass(frozen=True)
class ProofClaim:
    """One verification claim a handback makes, plus what it was checked against.

    ``authoritative`` is the text the claim is ABOUT. ``compared_against`` is
    the text the claim was actually checked against — usually the same string,
    and the R-0147 defect is precisely when it is not.
    """

    name: str
    needle: str
    authoritative: str
    asserted: bool
    compared_against: str = ""


@dataclass(frozen=True)
class Handback:
    """The artifact a dispatched job hands back, with its own ground truth beside it.

    Every "reported" field is the artifact's CLAIM; every plain field is what
    the loop can observe independently. A detector compares the two — it never
    takes a claim on trust, which is the one habit the era's findings were all
    about.
    """

    #: Commits that really are in the handback's review range.
    commits: tuple[str, ...] = ()
    #: Commits the handback's tables account for.
    reported_commits: tuple[str, ...] = ()
    #: commit -> the changed files its table lists. An empty tuple is a table
    #: that exists but says nothing, which is the R-0143 shape.
    changed_files_tables: dict[str, tuple[str, ...]] = field(default_factory=dict)
    #: External actions actually taken (a PR created, a branch deleted).
    external_actions: tuple[str, ...] = ()
    #: External actions the handback reports as actions taken.
    reported_actions: tuple[str, ...] = ()
    #: The verdict text the handback carries, and who wrote it.
    verdict_text: str = ""
    verdict_author: str = ""
    #: True while the review that would justify a verdict is still open.
    review_pending: bool = False
    #: Flags the interface advertises, and the flags actually passed through.
    advertised_flags: tuple[str, ...] = ()
    passed_flags: tuple[str, ...] = ()
    proofs: tuple[ProofClaim, ...] = ()
    authored_texts: tuple[AuthoredText, ...] = ()

    @classmethod
    def from_json(cls, body: Any) -> Handback:
        """Build a handback from plain data (a fixture, or a job's own record)."""
        if not isinstance(body, dict):
            raise ValueError("a handback must be an object")
        return cls(
            commits=tuple(body.get("commits") or ()),
            reported_commits=tuple(body.get("reported_commits") or ()),
            changed_files_tables={
                str(k): tuple(v or ())
                for k, v in (body.get("changed_files_tables") or {}).items()},
            external_actions=tuple(body.get("external_actions") or ()),
            reported_actions=tuple(body.get("reported_actions") or ()),
            verdict_text=str(body.get("verdict_text", "")),
            verdict_author=str(body.get("verdict_author", "")),
            review_pending=bool(body.get("review_pending", False)),
            advertised_flags=tuple(body.get("advertised_flags") or ()),
            passed_flags=tuple(body.get("passed_flags") or ()),
            proofs=tuple(
                ProofClaim(
                    name=str(p.get("name", "")),
                    needle=str(p.get("needle", "")),
                    authoritative=str(p.get("authoritative", "")),
                    asserted=bool(p.get("asserted", False)),
                    compared_against=str(p.get("compared_against", "")))
                for p in (body.get("proofs") or ())),
            authored_texts=tuple(
                AuthoredText(
                    name=str(a.get("name", "")),
                    declared_sha256=str(a.get("declared_sha256", "")),
                    applied_text=str(a.get("applied_text", "")))
                for a in (body.get("authored_texts") or ())),
        )


# ---------------------------------------------------------------------------
# The detectors
# ---------------------------------------------------------------------------


def _detect_incomplete_accounting(hb: Handback) -> list[EraDefect]:
    """R-0141 / R-0143 / R-0145 — the handback does not account for its own range."""
    out: list[EraDefect] = []
    missing = [c for c in hb.commits if c not in hb.reported_commits]
    if missing:
        out.append(EraDefect(
            DEFECT_INCOMPLETE_ACCOUNTING,
            f"{len(missing)} commit(s) inside the review range are absent "
            f"from the handback tables: {', '.join(missing)}"))
    untabled = [c for c in hb.reported_commits
                if not hb.changed_files_tables.get(c)]
    if untabled:
        out.append(EraDefect(
            DEFECT_INCOMPLETE_ACCOUNTING,
            f"{len(untabled)} reported commit(s) carry no changed-files "
            f"table: {', '.join(untabled)}"))
    unreported = [a for a in hb.external_actions if a not in hb.reported_actions]
    if unreported:
        out.append(EraDefect(
            DEFECT_INCOMPLETE_ACCOUNTING,
            f"{len(unreported)} external action(s) were taken but never "
            f"reported: {', '.join(unreported)}"))
    return out


def _detect_self_authored_verdict(hb: Handback) -> list[EraDefect]:
    """R-0144 — a verdict the reviewer never authored."""
    if not hb.verdict_text.strip():
        return []
    out: list[EraDefect] = []
    if hb.verdict_author != VERDICT_AUTHOR_REVIEWER:
        out.append(EraDefect(
            DEFECT_SELF_AUTHORED_VERDICT,
            f"the verdict is authored by {hb.verdict_author or 'nobody named'}, "
            f"not by the {VERDICT_AUTHOR_REVIEWER}"))
    if hb.review_pending:
        out.append(EraDefect(
            DEFECT_SELF_AUTHORED_VERDICT,
            "a verdict is presented while the review that would justify it "
            "is still pending"))
    return out


def _detect_dropped_flag(hb: Handback) -> list[EraDefect]:
    """R-0146 — an advertised flag that is never passed through."""
    dropped = [f for f in hb.advertised_flags if f not in hb.passed_flags]
    if not dropped:
        return []
    return [EraDefect(
        DEFECT_DROPPED_FLAG,
        f"{len(dropped)} advertised flag(s) are not passed through and are "
        f"silently ignored: {', '.join(dropped)}")]


def _detect_self_consistency_proof(hb: Handback) -> list[EraDefect]:
    """R-0147 — a proof re-checked against the authoritative text disagrees.

    The claim is not trusted; it is RE-RUN here. A claim compared against
    something other than the authoritative text is named as such, because that
    is the difference between a verification and a proof of its own premise.
    """
    out: list[EraDefect] = []
    for proof in hb.proofs:
        truth = proof.needle in proof.authoritative
        if proof.asserted == truth:
            continue
        compared = proof.compared_against or proof.authoritative
        wrong_subject = compared != proof.authoritative
        detail = (
            f"proof {proof.name!r} asserts {proof.asserted} but re-checking it "
            f"against the authoritative text gives {truth}")
        if wrong_subject:
            detail += (" — it was compared against a different text than the "
                       "one it claims to be about")
        out.append(EraDefect(DEFECT_SELF_CONSISTENCY_PROOF, detail))
    return out


def _detect_corrupted_authored_text(hb: Handback) -> list[EraDefect]:
    """R-0148 — applied text whose digest does not match what was authored.

    Hash on write, verify on read. Remedy deliberately does not look for hard
    wraps or any other transport artefact: the digest catches every corruption
    a shape heuristic would, without a second mechanism to keep in step.
    """
    out: list[EraDefect] = []
    for text in hb.authored_texts:
        if not text.declared_sha256:
            out.append(EraDefect(
                DEFECT_CORRUPTED_AUTHORED_TEXT,
                f"authored text {text.name!r} crossed the dispatch boundary "
                f"with no declared digest, so nothing can verify it"))
            continue
        actual = authored_text_digest(text.applied_text)
        if actual != text.declared_sha256:
            out.append(EraDefect(
                DEFECT_CORRUPTED_AUTHORED_TEXT,
                f"authored text {text.name!r} does not match its declared "
                f"digest (declared {text.declared_sha256[:12]}…, applied "
                f"{actual[:12]}…)"))
    return out


#: Every detector, in the order their finding ids were raised.
_DETECTORS = (
    _detect_incomplete_accounting,
    _detect_self_authored_verdict,
    _detect_dropped_flag,
    _detect_self_consistency_proof,
    _detect_corrupted_authored_text,
)


def detect_era_defects(handback: Handback | Any) -> list[EraDefect]:
    """Every defect in one handback, in detector order. Never raises on content."""
    hb = handback if isinstance(handback, Handback) else Handback.from_json(handback)
    out: list[EraDefect] = []
    for detector in _DETECTORS:
        out.extend(detector(hb))
    return out


def render_defects(defects: list[EraDefect]) -> str:
    """The refusal reason a human reads in the ledger."""
    if not defects:
        return ""
    return "; ".join(
        f"[{d.finding_class or DEFECT_FINDING_CLASSES.get(d.kind, d.kind)}] "
        f"{d.detail}"
        for d in defects)
