"""Guard: the completion digest's hero card is really MOUNTED into
`RemedyShell.tsx` (F040 T002, round 14) — not merely present on disk.

`jobDigest.ts` decodes the envelope, `digestVisibility.ts` decides WHEN to
show it, `browserDigestPort.ts` is the browser-local storage edge and
`DigestHeroCard.tsx` is the render — every one of those four pieces was
already built and already fully tested by its own guard in an earlier round.
THIS FILE IS THE GUARD FOR THE WIRING THAT JOINS THEM: the load, the storage
edge bound for real against `window.localStorage`, the last-seen
read-before-write pair, the dismissal read, `latestActivityMs` from the brain
stream's own ring buffer, the visibility computation, and the card's exact
placement as a sibling of the shell div rather than a fifth `<main>` child.

NOTHING IN THIS REPOSITORY CAN RENDER `RemedyShell.tsx`. There is no DOM
environment here and `apps/ui/vitest.config.ts` collects `src/**/*.test.ts`
in a NODE environment, so the frontend runner never reaches this file's
markup. The wiring is therefore gated the way every other component here is
gated — by READING it — exactly as `tests/ui_contracts/test_diff_viewer_mount.py`
gates the diff panel's own mount and `tests/ui_contracts/test_remedy_shell_stream.py`
gates the brain-stream subscription two effects above this one.

Every assertion runs over COMMENT-STRIPPED source, because the new lines
carry WHY comments that name several of the symbols asserted below (finding
`R-0584`). This file defines its own comment stripper rather than importing
one: no sibling under this directory exports its stripper as an importable
name — `test_remedy_shell_stream.py`, `test_diff_viewer_mount.py` and
`test_digest_hero_card.py` each carry their own copy of the same twelve
lines, and this file follows that established (if repetitive) convention
rather than starting a shared-import coupling none of them has.

THE `<main>`-EXTRACTION REGEX IS REPRODUCED BYTE-FOR-BYTE FROM
`test_main_layout_guard.py` RATHER THAN IMPORTED: that guard exposes the
pattern only inline inside each of its own test methods, with nothing built
as an importable constant or helper, so there is nothing here to import.
Reproducing it byte-for-byte is what lets this file prove the digest card
never becomes the `<main>` guard's uncounted fifth child using the exact same
lens that guard itself uses, without silently drifting from it.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SHELL = REPO_ROOT / "apps" / "ui" / "src" / "components" / "shell" / "RemedyShell.tsx"

# Reproduced byte-for-byte from tests/ui_contracts/test_main_layout_guard.py.
MAIN_SPAN_RE = r"<main[^>]*className=\{styles\.main\}[^>]*>(.*?)</main>"

# The six pieces constraint 5 of the round-14 block orders, IN THAT ORDER, as
# the shortest unique anchor that proves each one exists. `digestPort.readDismissal(`
# is deliberately excluded from this list even though it is one of the six:
# it occurs TWICE by design (constraint 5(iv)'s lazy initializer and
# constraint 6's `onDismissed` re-read) and is checked on its own below,
# by position, rather than folded into this strictly-one-per-anchor list.
ORDERED_UNIQUE_ANCHORS = (
    ("(i) the digest load effect", "loadJobDigest("),
    ("(ii) the storage edge", "browserDigestVisibilityPort("),
    ("(iii-read) last-seen read", "digestPort.readLastSeen("),
    ("(iii-write) last-seen write", "digestPort.writeLastSeen("),
    ("(v) latestActivityMs", "newestActionRow("),
    ("(vi) the visibility computation", "digestVisibility({"),
)


def strip_ts_comments(text: str) -> str:
    """Drop `//` and `/* */` comments. `RemedyShell.tsx` holds no string
    literal carrying either marker, which is what lets so plain a scanner be
    trustworthy here (the same reasoning every sibling guard states)."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        pair = text[i:i + 2]
        if pair == "//":
            nl = text.find("\n", i)
            i = n if nl == -1 else nl
        elif pair == "/*":
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def shell_raw() -> str:
    return SHELL.read_text()


def shell_code() -> str:
    return strip_ts_comments(shell_raw())


def main_span(raw: str) -> str:
    """The `<main>...</main>` body, extracted with the SAME regex
    `test_main_layout_guard.py` uses. Applied to RAW (unstripped) source,
    exactly as that guard applies it — this file does not change that
    guard's own lens, only reuses it."""
    match = re.search(MAIN_SPAN_RE, raw, re.DOTALL)
    assert match, f"could not find <main className={{styles.main}}> in {SHELL.name}"
    return match.group(1)


class TestTheStrippersReallyStrip:
    """Without this, every COMMENT-STRIPPED assertion below could be
    satisfied by a stripper that ate the file rather than one that read it
    (finding R-0584's own trap)."""

    def test_the_stripper_removes_a_comment_the_shell_really_carries(self):
        raw = shell_raw()
        promise = "THE STORAGE EDGE, BOUND HERE because this is the edge"
        assert promise in raw, "the mount must keep its WHY comment"
        assert promise not in strip_ts_comments(raw), "stripper must remove it"

    def test_the_stripper_leaves_the_code_around_the_comment(self):
        code = shell_code()
        assert "export function RemedyShell(" in code, (
            "a stripper that ate the code as well would make every "
            "assertion below vacuous"
        )
        assert len(code) < len(shell_raw()), (
            "the stripper returned the file unchanged, so nothing was "
            "actually stripped"
        )


class TestConstraint5SixPiecesAppearInOrder:
    """Constraint 5's six-item ORDER (i)-(vi), checked the way G5 checks it:
    by STRING OFFSET in comment-stripped source, not merely that all six
    exist. This is the general form of mutation (b) — a read/write swap is
    one instance of an order violation this test catches on its own, in
    addition to the dedicated test below naming that pair specifically."""

    def test_every_anchor_is_present_and_unique(self):
        code = shell_code()
        for label, needle in ORDERED_UNIQUE_ANCHORS:
            count = code.count(needle)
            assert count == 1, (
                f"{label} anchor {needle!r} occurs {count} times; it must "
                f"occur exactly once for its offset to be unambiguous"
            )

    def test_the_dismissal_read_occurs_exactly_twice_by_design(self):
        # (iv)'s lazy initializer, plus constraint 6's onDismissed re-read.
        # A single occurrence would mean the callback duplicates a clock
        # read instead of re-reading the port (mutation (d)'s own family);
        # three or more would mean a stray third read was introduced.
        code = shell_code()
        assert code.count("digestPort.readDismissal(") == 2, (
            "digestPort.readDismissal( must occur exactly twice: the "
            "lazy initializer (iv) and onDismissed's own re-read (constraint 6)"
        )

    def test_the_six_pieces_appear_in_source_order(self):
        code = shell_code()
        offsets = [(label, code.index(needle)) for label, needle in ORDERED_UNIQUE_ANCHORS]
        for (label_a, off_a), (label_b, off_b) in zip(offsets, offsets[1:]):
            assert off_a < off_b, (
                f"{label_a} (offset {off_a}) must precede {label_b} "
                f"(offset {off_b}) in source order per constraint 5"
            )

    def test_the_dismissal_readers_lazy_initializer_sits_between_the_storage_edge_and_the_activity_read(self):
        # (iv) itself is excluded from the strict list above because it is
        # not unique; its FIRST occurrence (the lazy initializer) must still
        # sit between (ii)/(iii) and (v)/(vi).
        code = shell_code()
        first_dismissal_read = code.index("digestPort.readDismissal(")
        storage_edge = code.index("browserDigestVisibilityPort(")
        activity_read = code.index("newestActionRow(")
        assert storage_edge < first_dismissal_read < activity_read, (
            "the dismissal read's lazy initializer (iv) must sit after the "
            "storage edge (ii) and before latestActivityMs (v)"
        )


class TestLastSeenIsReadBeforeItIsWritten:
    """Mutation (b): swapping the last-seen read and its write effect so the
    write appears in source BEFORE the read must turn this guard red. G5
    checks this by string position, not by React's own runtime order,
    because the guard cannot run React — and neither can this one."""

    def test_the_read_precedes_the_write_in_source_order(self):
        code = shell_code()
        read_idx = code.index("digestPort.readLastSeen(")
        write_idx = code.index("digestPort.writeLastSeen(")
        assert read_idx < write_idx, (
            "digestPort.readLastSeen( must appear BEFORE digestPort.writeLastSeen( "
            "in source order; the visibility rule must see the instant the "
            "operator was last here, not the one this mount is about to record"
        )

    def test_the_write_effect_body_is_only_the_one_call(self):
        # Scoped to the effect whose body calls writeLastSeen, so a stray
        # second write elsewhere in the file cannot satisfy the check above
        # by accident.
        code = shell_code()
        match = re.search(
            r"useEffect\(\s*\(\s*\)\s*=>\s*\{\s*digestPort\.writeLastSeen\(([^;]*)\);\s*\},\s*\[dashboard\.jobId\]\)",
            code,
        )
        assert match, (
            "no useEffect keyed on [dashboard.jobId] alone whose entire "
            "body is one call to digestPort.writeLastSeen(...) was found"
        )


class TestStorageEdgeBindsTheRealLocalStorage:
    """Mutation (c): deleting `window.localStorage` from the
    `browserDigestVisibilityPort(` call, leaving it called with no argument,
    must turn this guard red. Constraint 8 also requires this to be the
    ONLY occurrence of `window.localStorage` in the file."""

    def test_the_port_is_bound_against_window_localstorage(self):
        code = shell_code()
        assert re.search(r"browserDigestVisibilityPort\(\s*window\.localStorage\s*\)", code), (
            "browserDigestVisibilityPort( must be called with window.localStorage "
            "as its argument; a call with no argument (or a different storage) "
            "is not the real browser edge DECISION F040 D8 names"
        )

    def test_window_localstorage_occurs_exactly_once(self):
        code = shell_code()
        assert code.count("window.localStorage") == 1, (
            "window.localStorage must occur EXACTLY ONCE in the file — the "
            "single browserDigestVisibilityPort(window.localStorage) call — "
            "never a second direct read or write of localStorage anywhere else"
        )


class TestDismissalReReadsThePortRatherThanHardcoding:
    """Mutation (d): changing `onDismissed`'s callback to set a hard-coded
    instant instead of re-reading `digestPort.readDismissal(dashboard.jobId)`
    must turn this guard red. Constraint 6: the card's own `onDismissed`
    prop RE-READS the port rather than duplicating the card's own
    `Date.now()` read."""

    def test_on_dismissed_prop_value_re_reads_the_port(self):
        code = shell_code()
        match = re.search(r"onDismissed=\{([^}]*)\}", code)
        assert match, "the DigestHeroCard element must carry an onDismissed prop"
        value = match.group(1)
        assert "setDismissedAtMs(" in value, (
            f"onDismissed must update dismissedAtMs state; found: {value!r}"
        )
        assert "digestPort.readDismissal(dashboard.jobId)" in value, (
            f"onDismissed must RE-READ the port (digestPort.readDismissal"
            f"(dashboard.jobId)) rather than compute or hard-code an instant "
            f"of its own; found: {value!r}"
        )

    def test_the_on_dismissed_extraction_can_see_a_synthetic_prop(self):
        # Discriminator: proves the regex mechanism above is not vacuous.
        synthetic = 'x onDismissed={() => setDismissedAtMs(Date.now())} y'
        match = re.search(r"onDismissed=\{([^}]*)\}", synthetic)
        assert match and "Date.now()" in match.group(1), (
            "the onDismissed extraction cannot see a real prop value even "
            "when one is there"
        )


class TestPrimaryActionAndOpenDecisionsStayUnwired:
    """Mutation (e): adding a literal `onPrimaryAction={() => {}}` prop must
    turn this guard red. Constraint 6: `onOpenDecisions` and
    `onPrimaryAction` are OMITTED from the JSX entirely — the props are
    optional and omitting them is how "unwired" reads, rather than passing
    an explicit no-op that would misstate a decision as made."""

    def test_on_primary_action_is_not_wired_anywhere(self):
        raw = shell_raw()
        assert "onPrimaryAction" not in raw, (
            "onPrimaryAction must not occur anywhere in RemedyShell.tsx this "
            "round, not even as an explicit no-op — DECISION F040 D5's "
            "in-page action needs its own resolution design first"
        )

    def test_on_open_decisions_is_not_wired_anywhere(self):
        raw = shell_raw()
        assert "onOpenDecisions" not in raw, (
            "onOpenDecisions must not occur anywhere in RemedyShell.tsx this "
            "round; no task or decision id exists yet to focus"
        )

    def test_the_absence_scan_would_notice_either_prop_if_added(self):
        # Discriminator: a substring scan cannot be fooled by a broken
        # reader, but this proves the literal token really is detectable.
        salted = shell_raw() + '\nconst leak = onPrimaryAction;\nconst leak2 = onOpenDecisions;\n'
        assert "onPrimaryAction" in salted
        assert "onOpenDecisions" in salted


class TestTheCardIsAViewportSiblingNeverAFifthMainChild:
    """Mutation (a): moving the digest card's JSX from before the shell div
    to after it, nested one level deeper so it lands inside `<main>`'s own
    span as a fifth child, must turn this guard red. Constraint 6: the card
    is the first child of `<div className={styles.viewport}>`, immediately
    after `<DegradedBanner .../>` and BEFORE the shell div that opens
    `<main>`. Constraint 9: `<main>` gains no fifth child."""

    def test_digest_hero_card_is_rendered_exactly_once(self):
        raw = shell_raw()
        assert raw.count("<DigestHeroCard") == 1, (
            f"expected exactly one <DigestHeroCard element, found "
            f"{raw.count('<DigestHeroCard')}"
        )

    def test_digest_hero_card_does_not_appear_inside_main(self):
        raw = shell_raw()
        body = main_span(raw)
        assert "DigestHeroCard" not in body, (
            "DigestHeroCard must not appear inside <main className={styles.main}>"
            "...</main> — that is the fifth-child regression constraint 9 forbids"
        )

    def test_digest_hero_card_sits_between_the_banner_and_the_shell_div(self):
        raw = shell_raw()
        banner_idx = raw.index("<DegradedBanner")
        card_idx = raw.index("<DigestHeroCard")
        shell_div_idx = raw.index("<div className={`${styles.shell}")
        assert banner_idx < card_idx < shell_div_idx, (
            "the card must render immediately after <DegradedBanner .../> and "
            "before the shell div that opens <main>, as the FIRST new child "
            "of the viewport div"
        )

    def test_the_card_is_conditioned_on_digest_not_null(self):
        code = shell_code()
        assert re.search(r"\{digest\s*!==\s*null\s*&&", code), (
            "the card must be conditioned on `digest !== null`, never on "
            "`visibility.show` directly — the card itself already branches "
            "on that per its own constraint from an earlier round"
        )
        assert "visibility.show &&" not in code, (
            "the mount must not gate on visibility.show directly; that "
            "branch belongs to DigestHeroCard itself"
        )


class TestNoNewCapabilityBeyondTheSpec:
    """Constraint 8: no new capability is added to the shell beyond what
    this spec names. `RemedyShell.tsx` calls no `fetch` and no
    `XMLHttpRequest` directly today, and this round keeps that true."""

    def test_the_shell_still_calls_no_fetch_or_xhr_directly(self):
        code = shell_code()
        assert "fetch(" not in code, (
            "RemedyShell.tsx must not call fetch( directly; loadJobDigest "
            "is the same kind of door loadDiffEnvelope already is"
        )
        assert "XMLHttpRequest" not in code

    def test_date_now_occurs_exactly_twice_in_two_distinct_calls(self):
        # Constraint 5(vi): the file's only Date.now() call outside
        # writeLastSeen's own argument is the digestVisibility(...) call's
        # nowMs field — exactly two occurrences total, and neither
        # duplicates the other's own enclosing call expression.
        code = shell_code()
        positions = [m.start() for m in re.finditer(r"Date\.now\(\)", code)]
        assert len(positions) == 2, (
            f"Date.now() must occur exactly twice in the new lines, found "
            f"{len(positions)}"
        )
        contexts = [code[max(0, p - 40):p] for p in positions]
        assert contexts[0] != contexts[1], (
            "the two Date.now() calls must not duplicate the same "
            "enclosing call expression"
        )
        assert "writeLastSeen" in contexts[0] or "writeLastSeen" in contexts[1], (
            "one Date.now() call must be writeLastSeen's own argument"
        )
        assert "nowMs" in code[positions[0]:positions[1] + 20] or "nowMs" in contexts[1], (
            "one Date.now() call must feed the digestVisibility({...}) call's nowMs field"
        )


class TestTheMountUsesTheRealDoors:
    """The mount imports the real modules rather than reimplementing any of
    their rules — every decidable behaviour already lives in `jobDigest.ts`,
    `digestVisibility.ts`, `browserDigestPort.ts` and `actionClass.ts`, and
    this file restates none of it."""

    def test_the_shell_imports_load_job_digest(self):
        code = shell_code()
        assert re.search(r'import\s*\{[^}]*\bloadJobDigest\b[^}]*\}\s*from\s*"\.\./\.\./api/remedyApi"', code), (
            "loadJobDigest must be imported from ../../api/remedyApi, "
            "extending the existing loadDiffEnvelope import"
        )

    def test_the_shell_imports_the_storage_edge_factory(self):
        code = shell_code()
        assert 'import { browserDigestVisibilityPort } from "../../api/browserDigestPort";' in code

    def test_the_shell_imports_the_visibility_rule(self):
        code = shell_code()
        assert re.search(r'import\s*\{[^}]*\bdigestVisibility\b[^}]*\}\s*from\s*"\.\./\.\./api/digestVisibility"', code)

    def test_the_shell_imports_newest_action_row(self):
        code = shell_code()
        assert 'import { newestActionRow } from "../../api/actionClass";' in code

    def test_the_shell_imports_the_hero_card_component(self):
        code = shell_code()
        assert 'import { DigestHeroCard } from "../digest/DigestHeroCard";' in code
