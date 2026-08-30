--- STEP R7/F106 — T002c-i: Builder fallback-once on a failed resume ---

Goal: book the round 6 verdict, then land T002c-i — the Orchestrator
brief's fallback-once rule, on the Builder side only: a resume attempt
that errors falls back ONCE, within the same round, to the full-context
path (`resume=None`), and the fallback is recorded honestly on
`BuilderOutput.resume_fallback` (a new field). Fallback firing is gated
on `builder_resume_ref` having been set (a resume was actually
attempted) AND the resulting call erroring — a plain call failure with no
resume in play is completely unaffected and falls straight through to the
EXISTING terminal-error handling, unchanged. `FakeProvider` gains a
test-only `resume_fails` constructor override so a test can force a
resume attempt to error, giving the fallback path something real to fall
back FROM. No real adapter's `supports_resume` turns True in production
this round. As in rounds 5 and 6, `_build_provider_evidence` and the
closed-schema `provider_evidence.json` path are NOT touched —
`resume_fallback` lives on `BuilderOutput` only, same carve-out. KNOWN,
DECLARED SIMPLIFICATION: a fallback issues a SECOND real provider call
inside the SAME round, so `result.provider_attempts` legitimately grows
by one extra "builder"/"attempt" entry for a round that fell back — this
is accurate (two calls really happened) and is not treated as a defect;
downstream consumers that assume exactly one builder attempt per round
are not a thing that exists today (verify this yourself before applying,
per constraint 15). The Reviewer-side mirror (T002c-ii) and the F111
delta-prompt shrink (T002b-ii) remain open, not this round.

Base: `e41b96395dd4251fd458c37fe37d2e3065a1633b`, the tip of
`feature/f106-session-resume` after round 6. Same branch, no new branch.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f106-r7.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN7
- C2  append slice RECORD7 (the round 6 verdict) to `.agent/live_review.md`
- C3  apply the three pairs below to
      `packages/orchestration/pingpong_provider.py`
- C4  apply the one pair below to `packages/orchestration/pingpong_loop.py`
- C5  apply the two pairs below to
      `tests/orchestration/test_session_resume.py`
- C6  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f106-r7.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    packages/orchestration/pingpong_provider.py
    packages/orchestration/pingpong_loop.py
    tests/orchestration/test_session_resume.py
    .agent/handoff.md

No other file changes this round. `ClaudeProvider`/`ClaudeCliProvider` are
NOT touched — only `BuilderOutput`'s field list and `FakeProvider`. In
`pingpong_loop.py`, ONLY the Builder call site's fallback logic is added —
the Reviewer call site, the parse-retry call site, and
`_build_provider_evidence` are all untouched this round.

## Constraints

1. Apply every slice and pair BYTE FOR BYTE. Do not fix, rewrap or improve
   one. If a slice or pair looks wrong, apply it as given and DECLARE the
   problem.
2. C0a/C0b: `shutil.copyfile` from the reviewer's scratch original at
   `.remedy-wt/f106-r7-block.md` for C0a, then from the committed
   `.agent/authored/f106-r7.md` for C0b. Never `cp`, never retype. Extract
   every slice/pair from the COMMITTED `.agent/authored/f106-r7.md`, using
   the marker convention verified in every prior round.
3. C1 is the FIRST substantive commit, ahead of C2, per checklist item 23.
4. `.agent/live_review.md` is APPEND-ONLY. C2 appends RECORD7 and revises
   nothing already on disk.
5. NO NEW R-ID IS MINTED and NO DECISION ID IS MINTED. Registered 318 and
   resolved 55 stay UNMOVED (measured by the reviewer at `e41b9639`);
   `DECISION F\d+ D\d+ — ` stays 19. `Gate: F106 R6 — ` occurs 0x before C2
   and exactly 1x after — that is RECORD7's own header, not a new finding.
6. `.agent/plan.md` stays under 50 lines (AGENTS.md).
7. Every exit code is REAL, from `subprocess.run(...).returncode` in a
   script under the gitignored `.remedy-wt/`. Never through a pipe.
8. This round's checks are all read-only against the primary checkout
   (imports, `ast.parse`, pytest runs) — no destructive check and no
   worktree is needed this round; none of G1-G9 below mutates a file
   outside a script's own transient copy.
9. `remedy` the console script is DENIED in this sandbox; use
   `python3 -m apps.cli.main ...`.
10. Commit subjects: no leading-slash token, no absolute path, no
    secret-like string, no `Co-Authored-By` trailer.
11. Push after C6. Open NO pull request — T002c-i closes only one more
    slice of T002; T002b-ii, T002c-ii and T003 remain.
12. Pair shapes, measured by the reviewer's own containment test before
    emission, reported here as the result, not the method: FIVE pairs
    (BUILDEROUTPUT-FIELD, FAKEPROVIDER-INIT, FAKEPROVIDER-BUILD,
    BUILDER-CALL-FALLBACK, TESTFILE-DOCSTRING) read `TO contains FROM:
    false` (REWRITE — new lines inserted INSIDE the FROM span). The
    sixth, TESTFILE-APPEND, reads `TO contains FROM: true` (APPEND-shaped,
    FROM is TO's exact prefix — same shape as every prior round's
    TESTFILE-APPEND). Run the containment test yourself for each of the
    six independently and report your own result beside the reviewer's;
    if any disagrees, apply the pair as given and declare the discrepancy
    rather than silently reclassifying it. For the FIVE rewrite pairs:
    FROM occurs exactly 1x in its target file before its commit and 0x
    after; TO occurs 0x before and exactly 1x after. For TESTFILE-APPEND:
    FROM occurs exactly 1x before and STILL exactly 1x after (survives as
    TO's prefix); TO occurs 0x before and exactly 1x after. Report all six
    readings, each against its own correct expectation.
13. After C3/C4, both files must still be valid Python: `python3 -c "import
    ast; ast.parse(open('packages/orchestration/pingpong_provider.py').read())"`
    and the same for `pingpong_loop.py`, both exit 0. After C5,
    `python3 -m ruff check tests/orchestration/test_session_resume.py`
    must exit 0.
14. `FAKEPROVIDER-BUILD`'s change must NOT alter `FakeProvider().build(...)`
    behavior when `resume_fails` is left at its default `False` (nor when
    `supports_resume` is left at its default `False`) — G6's zero-behavior
    probe and the existing `TestZeroBehaviorChange` class (untouched this
    round) are how this is proved; do not weaken or remove either.
15. `BUILDER-CALL-FALLBACK`'s fallback branch reuses the EXACT SAME
    `_call_with_retry(...)` shape as the primary attempt immediately above
    it, only swapping `resume=builder_resume_ref` for `resume=None` and
    resetting `builder_call_reasons` — verify this yourself by comparing
    the two `_call_with_retry(...)` calls in the pair's own TO text before
    applying it, they must be structurally parallel. `_finalize_call` and
    the terminal-error handling immediately below (unpaired, untouched by
    this round) run exactly ONCE per round, against whichever `builder_out`
    the fallback logic leaves behind (the fallback's own result if a
    fallback fired, the primary attempt's result otherwise) — confirm this
    by reading the ~10 lines immediately following the pair's TO span in
    the committed file.
16. Before C4, confirm `_build_provider_evidence`, the Reviewer call site,
    and the parse-retry call site are all UNCHANGED — `git diff --stat`
    for `packages/orchestration/provider_token_evidence.py` must show
    nothing, and a manual before/after read of both other call sites (a
    few hundred lines apart in the same file) must show them
    byte-identical to their state at the round's base.

## Pairs

Each pair is FROM/TO, delimited the same way as prior rounds: content
starts the line after `<<<BEGIN` and ends with the newline before
`<<<END`.

<<<BEGIN RECORD7
Gate: F106 R6 — T002b-i: REVIEWER REPAIR CALL ACTUALLY RESUMES. VERDICT PASS. The reviewer independently re-verified round 6's committed diff `295cad25..e41b9639` against the real files, not the worker's summary, after having already dry-run every pair and gate in a disposable worktree BEFORE authoring the round's block. G1 TRANSPORT: `.agent/authored/f106-r6.md`, `.agent/last_block.md` AND the reviewer's own held original `.remedy-wt/f106-r6-block.md` all sha256 `46d680906294e77aea4ef2795e40eb7783460706a551af44184b9a5711bc8f90`, 28738 bytes, three-way equal. G2 THE PLAN: `.agent/plan.md` byte-equal to slice PLAN6, 41 lines. G3 THE RECORD APPEND: base 1822769 + `\n` + RECORD6 (3257 bytes) = 1826027, matching the committed file exactly; both readings (whole reconstruction, last-unit-suffix) `True`, computed against the real base read at commit `37c6ac78^`. G4 THE LEDGER: independently re-measured — registered 318, resolved 55, open 263, `DECISION` 19, all unmoved; `Gate: F106 R5 — ` count exactly 1 at HEAD. G5 THE CODE — PAIR SHAPE: independently re-measured all four pairs (FAKEPROVIDER-REVIEW, REVIEWER-CALL, TESTFILE-DOCSTRING as REWRITE; TESTFILE-APPEND as APPEND) against the real committed files at base `295cad25` and at HEAD — all four read exactly as the block predicted; `ast.parse` both files exit 0; `ruff check` exit 0. G6 ZERO BEHAVIOR CHANGE: `python3 -m pytest tests/orchestration/test_pingpong.py tests/orchestration/test_provider_mode.py tests/orchestration/test_provider_evidence_integration.py -q` independently re-run, REAL exit 0, 122 passed, matching base exactly. G7 THE NEW SURFACE: `test_session_resume.py` independently re-run, REAL exit 0, 20 passed, matching the block's stated count exactly. Constraint 13's closed-schema carve-out independently confirmed: `git diff --stat 295cad25..HEAD -- packages/orchestration/provider_token_evidence.py` reads EMPTY. Constraint 16's parse-retry carve-out independently confirmed: the `retry_out = _call_with_retry(...)` call site at lines 3310-3315, read directly, still passes no `resume` kwarg, byte-identical to its state at the round's base. G8 STATE READERS/CANARY: independently re-run, REAL exit 0 each, 515/52/21/16/42, all matching base. G9 THE TREE: `git status --porcelain` empty, 0 untracked, every commit's insertions under 500, 8 commits landing on exactly the 8 named change-set paths, nothing else. NO DEVIATIONS declared this round — the bundle landed exactly as ordered. THE ROUND PASSES: T002b-i CLOSED — the Reviewer side of repair-round resume threading (PRIMARY attempt only, by explicit, verified scope) is honest, tested, and zero-behavior-change-proven, mirroring T002a exactly.
<<<END RECORD7

<<<BEGIN PLAN7
# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 2, round 7.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 (a/b/c): capability surface, all 3 adapters, tests | done | rounds 2-4 |
| T002a: Builder repair call resumes when earned | done | round 5 |
| T002b-i: Reviewer repair call resumes when earned | done | round 6 |
| T002c-i: Builder fallback-once on a failed resume | done | this round |
| T002b-ii: F111 delta prompt shrink | open | next |
| T002c-ii: Reviewer fallback-once mirror | open | |
| T003: measured fixture comparison + docs | open | |

## Next Steps
1. T002c-i: a Builder resume attempt that errors falls back ONCE, same
   round, to `resume=None`, recorded on the new `BuilderOutput.
   resume_fallback` field. Gated strictly on a resume having been
   attempted; a plain call failure is unaffected.
2. T002b-ii: the delta-prompt shrink via F111's existing diff-repair hunk
   selection. Needs its own research pass into the hunk-selection code
   before design — not started.
3. T002c-ii: the identical fallback-once mirror on the Reviewer side.
4. T003 follows once T002 is fully closed.

## Risks
- No adapter's `supports_resume` is true in production yet — only
  `FakeProvider`, via its test-only constructor overrides, ever resumes
  or fails a resume. None of T002a/b-i/c-i changes observable behavior
  for `ClaudeProvider`/`ClaudeCliProvider`, or for a default-constructed
  `FakeProvider`.
<<<END PLAN7

<<<BEGIN BUILDEROUTPUT-FIELD-FROM
    resume_used: bool = False
    resume_session_ref: str = ""
    incomplete: bool = False
    stream_cap_reached: bool = False
    stream_call_id: str = ""
    stream_artifact_refs: list[str] = field(default_factory=list)
    prepared_input: Any = None  # F012: fingerprint of the EXACT transport request


@dataclass
class ReviewFinding:
<<<END BUILDEROUTPUT-FIELD-FROM

<<<BEGIN BUILDEROUTPUT-FIELD-TO
    resume_used: bool = False
    resume_session_ref: str = ""
    # F106 T002c: true only when a resume attempt on this round's call
    # errored and a same-round fallback to full context was taken.
    resume_fallback: bool = False
    incomplete: bool = False
    stream_cap_reached: bool = False
    stream_call_id: str = ""
    stream_artifact_refs: list[str] = field(default_factory=list)
    prepared_input: Any = None  # F012: fingerprint of the EXACT transport request


@dataclass
class ReviewFinding:
<<<END BUILDEROUTPUT-FIELD-TO

<<<BEGIN FAKEPROVIDER-INIT-FROM
        malformed_review_recoverable: bool = False,
        supports_resume: bool = False,
        fake_session_id: str = "",
    ) -> None:
        self._builder_files = builder_files or ["docs/README.md"]
        self._supports_resume = supports_resume
        self._fake_session_id = fake_session_id
<<<END FAKEPROVIDER-INIT-FROM

<<<BEGIN FAKEPROVIDER-INIT-TO
        malformed_review_recoverable: bool = False,
        supports_resume: bool = False,
        fake_session_id: str = "",
        resume_fails: bool = False,
    ) -> None:
        self._builder_files = builder_files or ["docs/README.md"]
        self._supports_resume = supports_resume
        self._fake_session_id = fake_session_id
        self._resume_fails = resume_fails
<<<END FAKEPROVIDER-INIT-TO

<<<BEGIN FAKEPROVIDER-BUILD-FROM
    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> BuilderOutput:
        self._build_count += 1
        if self._builder_error:
            return BuilderOutput(
                error=self._builder_error,
                provider="fake",
            )
        is_repair = self._build_count > 1
<<<END FAKEPROVIDER-BUILD-FROM

<<<BEGIN FAKEPROVIDER-BUILD-TO
    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> BuilderOutput:
        self._build_count += 1
        if self._builder_error:
            return BuilderOutput(
                error=self._builder_error,
                provider="fake",
            )
        # F106 T002c: a test-only way to simulate a resume attempt that
        # errors, so the fallback-once path in pingpong_loop.py has
        # something real to fall back FROM. Only fires when a resume was
        # actually requested on a provider that claims to support it —
        # never on a plain (non-resume) call.
        if resume and self._supports_resume and self._resume_fails:
            return BuilderOutput(
                error="resume_lost: session context unavailable",
                provider="fake",
            )
        is_repair = self._build_count > 1
<<<END FAKEPROVIDER-BUILD-TO

<<<BEGIN BUILDER-CALL-FALLBACK-FROM
            builder_out = _call_with_retry(
                lambda ts=builder_timeout: builder_provider.build(
                    builder_prompt,
                    timeout_sec=ts,
                    max_output_chars=max_output_chars,
                    resume=builder_resume_ref,
                ),
                result=result,
                role="builder",
                provider=builder_name,
                on_provider_attempt=on_provider_call,
                call_reasons=builder_call_reasons,
                stop_check=_stopped,
                rate_governor=_rate_governor,
            )
            rd.builder_output = builder_out
<<<END BUILDER-CALL-FALLBACK-FROM

<<<BEGIN BUILDER-CALL-FALLBACK-TO
            builder_out = _call_with_retry(
                lambda ts=builder_timeout: builder_provider.build(
                    builder_prompt,
                    timeout_sec=ts,
                    max_output_chars=max_output_chars,
                    resume=builder_resume_ref,
                ),
                result=result,
                role="builder",
                provider=builder_name,
                on_provider_attempt=on_provider_call,
                call_reasons=builder_call_reasons,
                stop_check=_stopped,
                rate_governor=_rate_governor,
            )
            # F106 T002c: a resume attempt that errors falls back ONCE to the
            # full-context path within the same round — an honest, evidenced
            # event, never a task failure by itself (Orchestrator brief,
            # verbatim). Only fires when a resume was actually attempted
            # (``builder_resume_ref`` set); a plain call failure with no
            # resume in play is unaffected and falls straight through to the
            # existing terminal-error handling below, unchanged.
            if builder_resume_ref and builder_out.error:
                _begin_stream_call(builder_provider, round_num, "attempt")
                builder_call_reasons = []
                builder_out = _call_with_retry(
                    lambda ts=builder_timeout: builder_provider.build(
                        builder_prompt,
                        timeout_sec=ts,
                        max_output_chars=max_output_chars,
                        resume=None,
                    ),
                    result=result,
                    role="builder",
                    provider=builder_name,
                    on_provider_attempt=on_provider_call,
                    call_reasons=builder_call_reasons,
                    stop_check=_stopped,
                    rate_governor=_rate_governor,
                )
                builder_out.resume_fallback = True
            rd.builder_output = builder_out
<<<END BUILDER-CALL-FALLBACK-TO

<<<BEGIN TESTFILE-DOCSTRING-FROM
"""Tests for the F106 session-resume capability surface (T001) and its
repair-path wiring (T002a, T002b-i).

T001 covers: every concrete provider (`FakeProvider`, `ClaudeProvider`,
`ClaudeCliProvider`) exposes `supports_resume` and reads `False` by
construction this round; `build`/`review` accept an additive `resume`
keyword on all three without changing behavior; `BuilderOutput`/
`ReviewerOutput` default `resume_used`/`resume_session_ref` to `False`/"".
`ClaudeProvider`/`ClaudeCliProvider` are checked by signature only — no
real call is made, matching tests/orchestration/test_provider_mode.py's
own no-network convention for those two classes.

T002a covers: the repair round's Builder call actually passes `resume=`
built from the PRIOR round's captured session id, only when the Builder
provider honestly advertises `supports_resume`; every other path (initial
round, unsupported provider, no prior session id) passes `resume=None`.
`resume_used`/`resume_session_ref` land on the per-round `BuilderOutput`
only — surfacing them into the trust-bearing, closed-schema
`provider_evidence.json` is explicitly out of scope this round (see the
round's own step block). Real network/CLI providers are unaffected — this
round's production change lives only in the Builder call site of
`packages/orchestration/pingpong_loop.py`.

T002b-i covers the identical rule on the Reviewer side: the repair
round's PRIMARY `review()` attempt passes `resume=` built from the PRIOR
round's captured Reviewer session id, under the same three-way guard
(supported, is-repair, prior session id known). The bounded parse retry
(a separate call within the same round) is explicitly NOT threaded this
round — it always sends full context. `ReviewerOutput.resume_used`/
`resume_session_ref` land the same way `BuilderOutput`'s do; the
delta-prompt shrink (F111 hunk selection) is T002b-ii, still open.
"""

from __future__ import annotations

import dataclasses
import inspect
from pathlib import Path

import pytest

from packages.orchestration.pingpong_loop import run_pingpong
from packages.orchestration.pingpong_provider import (
    BuilderOutput,
    ClaudeCliProvider,
    ClaudeProvider,
    FakeProvider,
    ReviewerOutput,
)
<<<END TESTFILE-DOCSTRING-FROM

<<<BEGIN TESTFILE-DOCSTRING-TO
"""Tests for the F106 session-resume capability surface (T001) and its
repair-path wiring (T002a, T002b-i, T002c-i).

T001 covers: every concrete provider (`FakeProvider`, `ClaudeProvider`,
`ClaudeCliProvider`) exposes `supports_resume` and reads `False` by
construction this round; `build`/`review` accept an additive `resume`
keyword on all three without changing behavior; `BuilderOutput`/
`ReviewerOutput` default `resume_used`/`resume_session_ref` to `False`/"".
`ClaudeProvider`/`ClaudeCliProvider` are checked by signature only — no
real call is made, matching tests/orchestration/test_provider_mode.py's
own no-network convention for those two classes.

T002a covers: the repair round's Builder call actually passes `resume=`
built from the PRIOR round's captured session id, only when the Builder
provider honestly advertises `supports_resume`; every other path (initial
round, unsupported provider, no prior session id) passes `resume=None`.
`resume_used`/`resume_session_ref` land on the per-round `BuilderOutput`
only — surfacing them into the trust-bearing, closed-schema
`provider_evidence.json` is explicitly out of scope this round (see the
round's own step block). Real network/CLI providers are unaffected — this
round's production change lives only in the Builder call site of
`packages/orchestration/pingpong_loop.py`.

T002b-i covers the identical rule on the Reviewer side: the repair
round's PRIMARY `review()` attempt passes `resume=` built from the PRIOR
round's captured Reviewer session id, under the same three-way guard
(supported, is-repair, prior session id known). The bounded parse retry
(a separate call within the same round) is explicitly NOT threaded this
round — it always sends full context. `ReviewerOutput.resume_used`/
`resume_session_ref` land the same way `BuilderOutput`'s do.

T002c-i covers the Builder-side fallback-once rule: a resume attempt that
errors falls back ONCE, same round, to `resume=None`, recorded on the new
`BuilderOutput.resume_fallback` field — gated strictly on a resume having
actually been attempted, so a plain call failure is unaffected.
`FakeProvider`'s test-only `resume_fails` override makes this failure
mode reproducible without a real provider. The Reviewer-side mirror
(T002c-ii) and the delta-prompt shrink (T002b-ii) remain open.
"""

from __future__ import annotations

import dataclasses
import inspect
from pathlib import Path

import pytest

from packages.orchestration.pingpong_loop import run_pingpong
from packages.orchestration.pingpong_provider import (
    BuilderOutput,
    ClaudeCliProvider,
    ClaudeProvider,
    FakeProvider,
    ReviewerOutput,
)
<<<END TESTFILE-DOCSTRING-TO

<<<BEGIN TESTFILE-APPEND-FROM
    def test_initial_round_never_resumes(self, demo_repo: Path):
        provider = FakeProvider(supports_resume=True, fake_session_id="sess-1")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
        )
        assert result.rounds[0].reviewer_output.resume_used is False
<<<END TESTFILE-APPEND-FROM

<<<BEGIN TESTFILE-APPEND-TO
    def test_initial_round_never_resumes(self, demo_repo: Path):
        provider = FakeProvider(supports_resume=True, fake_session_id="sess-1")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
        )
        assert result.rounds[0].reviewer_output.resume_used is False


class TestT002cBuilderFallbackOnce:
    """A resume attempt that errors falls back once to full context, same round."""

    def test_resume_error_falls_back_and_round_completes(self, demo_repo: Path):
        provider = FakeProvider(
            fail_on_round=1, pass_on_round=2,
            supports_resume=True, fake_session_id="sess-1", resume_fails=True,
        )
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2,
        )
        assert len(result.rounds) >= 2
        assert result.rounds[1].builder_output.error == ""
        assert result.rounds[1].builder_output.resume_used is False
        assert result.rounds[1].builder_output.resume_fallback is True
        assert result.final_status == "staged_review_passed"

    def test_no_fallback_when_no_resume_attempted(self, demo_repo: Path):
        provider = FakeProvider(supports_resume=True, fake_session_id="sess-1", resume_fails=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
        )
        assert result.rounds[0].builder_output.error == ""
        assert result.rounds[0].builder_output.resume_fallback is False

    def test_no_fallback_when_provider_unsupported(self, demo_repo: Path):
        provider = FakeProvider(
            fail_on_round=1, pass_on_round=2,
            supports_resume=False, fake_session_id="sess-1", resume_fails=True,
        )
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2,
        )
        assert len(result.rounds) >= 2
        assert all(rd.builder_output.resume_fallback is False for rd in result.rounds)
<<<END TESTFILE-APPEND-TO

## Done when — the gates

Run each gate and report ONE line per gate with its REAL exit code. Every
gate runs at a commit STRICTLY EARLIER than C6, which writes the handback.

G1 TRANSPORT, at C0b. Report the byte length of the committed
   `.agent/authored/f106-r7.md` and `.agent/last_block.md`; state whether
   equal. No expected length stated — the reviewer holds the original.

G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to slice PLAN7 (sha256 of
   both), under 50 lines, holds `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure `.agent/live_review.md`'s
   pre-commit byte length yourself (the reviewer read 1826027 at
   `e41b9639`); base + `\n` + RECORD7 must equal the committed size. TWO
   readings: (a) whole reconstruction; (b) the committed file's last
   blank-line unit equals RECORD7 exactly (N=1).

G4 THE LEDGER, at C1 and C2. Registered/resolved/open unmoved from
   318/55/263. `DECISION` count 19 at both (line-anchored regex). `Gate:
   F106 R6 — ` 0x before C2, 1x after.

G5 THE CODE — PAIR SHAPE AND ORDERED APPLICATION, at C3-C5. For EACH of
   the six pairs (BUILDEROUTPUT-FIELD, FAKEPROVIDER-INIT,
   FAKEPROVIDER-BUILD, BUILDER-CALL-FALLBACK, TESTFILE-DOCSTRING,
   TESTFILE-APPEND): run your own containment test (`TO contains FROM`)
   and report the result; then report FROM's occurrence count in its
   target file before its commit and after, and TO's occurrence count
   before and after. For the five REWRITE pairs (all but TESTFILE-APPEND),
   FROM must read 1x→0x and TO 0x→1x. For TESTFILE-APPEND (append-shaped),
   FROM must read 1x→1x (survives as TO's prefix) and TO 0x→1x. Then,
   after C3/C4: `python3 -c "import ast;
   ast.parse(open('packages/orchestration/pingpong_provider.py').read())"`
   and the same for `pingpong_loop.py`, both exit 0. After C5: `python3
   -m ruff check tests/orchestration/test_session_resume.py` exits 0.

G6 ZERO BEHAVIOR CHANGE ON THE DEFAULT PATH, at C3/C4. Run
   `python3 -m pytest tests/orchestration/test_pingpong.py
   tests/orchestration/test_provider_mode.py
   tests/orchestration/test_provider_evidence_integration.py -q` — the
   reviewer measured 122 passed at the base; report yours (must be
   unchanged — every existing call site constructs `FakeProvider()` with
   `supports_resume`/`resume_fails` left at their defaults).

G7 THE NEW SURFACE, at C5. `python3 -m pytest
   tests/orchestration/test_session_resume.py -q` — report exit code and
   passed count; the reviewer's own count after both pairs apply is 23
   (the 20 carried in from round 6, unchanged, plus 3 new in
   `TestT002cBuilderFallbackOnce`) — restate your own exact count rather
   than trusting this one; if it disagrees, report the discrepancy and
   the actual collected count via `python3 -m pytest
   tests/orchestration/test_session_resume.py -q --collect-only` before
   ruling on pass/fail.

G8 THE STATE READERS AND CANARY, after C2. Each its own real exit code:
   `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/orchestration/test_test_runner.py -q`,
   `python3 -m pytest tests/regression/test_resource_safety.py -q`,
   `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`, and
   the canary `python3 -m pytest tests/cli/test_golden_path.py -q`. The
   reviewer measured 515, 52, 21, 16, 42 at the base; report yours.

G9 THE TREE, at C5. `git status --porcelain` empty, `git ls-files --others
   --exclude-standard` count 0, every commit's insertions under 500 (`git
   diff --numstat`).

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: state
block, `## Commits` table with `+/-` from `git diff --numstat`, deviations,
item-status table with every bundle item and every gate exactly once, next
steps — explicitly note T002c-i is CLOSED, and that T002b-ii (F111 delta
shrink) and T002c-ii (Reviewer fallback mirror) both remain, with T002b-ii
needing its own research pass into F111's hunk-selection code before a
round can be designed for it. States `SESSION 2` of F106, round 7. No
length cap.
