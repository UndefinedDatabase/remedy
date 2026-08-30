--- STEP R6/F106 — T002b-i: Reviewer repair call actually resumes ---

Goal: book the round 5 verdict, then land T002b-i — the mirror of round
5's Builder-side wiring, on the Reviewer side. The repair round's PRIMARY
`review()` attempt passes `resume=<prior round's captured Reviewer
session id>`, but ONLY when the Reviewer provider's `supports_resume` is
honestly true AND a prior Reviewer session id was actually captured. The
bounded parse retry (a DIFFERENT call within the same round, triggered
only on malformed output) is explicitly NOT threaded this round — it
always sends full context; this is a declared scope line, not an
oversight. `FakeProvider.review` now honors an incoming `resume` request
the same way `FakeProvider.build` does since round 5. No real adapter's
`supports_resume` turns True in production this round. Exactly as round
5 declared and round 5's own dry-run proved necessary,
`_build_provider_evidence` and the closed-schema
`provider_evidence.json` path are NOT touched this round either — that
surfacing is still deferred, to T002b-ii or T003. The F111 delta-prompt
shrink and the fallback-once rule remain T002b-ii/T002c.

Base: `295cad25d7abd4b39f3aacc18df9fa56afd2b9cf`, the tip of
`feature/f106-session-resume` after round 5. Same branch, no new branch.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f106-r6.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN6
- C2  append slice RECORD6 (the round 5 verdict) to `.agent/live_review.md`
- C3  apply the one pair below to
      `packages/orchestration/pingpong_provider.py`
- C4  apply the one pair below to `packages/orchestration/pingpong_loop.py`
- C5  apply the two pairs below to
      `tests/orchestration/test_session_resume.py`
- C6  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f106-r6.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    packages/orchestration/pingpong_provider.py
    packages/orchestration/pingpong_loop.py
    tests/orchestration/test_session_resume.py
    .agent/handoff.md

No other file changes this round. `ClaudeProvider`/`ClaudeCliProvider` are
NOT touched — only `FakeProvider.review`. In `pingpong_loop.py`, ONLY the
Reviewer's PRIMARY attempt call site changes — the bounded parse-retry
call site (a few lines further down the same function) is NOT touched.
`_build_provider_evidence` and `packages/orchestration/
provider_token_evidence.py` are NOT touched this round (same carve-out as
round 5, constraint 13 below).

## Constraints

1. Apply every slice and pair BYTE FOR BYTE. Do not fix, rewrap or improve
   one. If a slice or pair looks wrong, apply it as given and DECLARE the
   problem.
2. C0a/C0b: `shutil.copyfile` from the reviewer's scratch original at
   `.remedy-wt/f106-r6-block.md` for C0a, then from the committed
   `.agent/authored/f106-r6.md` for C0b. Never `cp`, never retype. Extract
   every slice/pair from the COMMITTED `.agent/authored/f106-r6.md`, using
   the marker convention verified in every prior round (content starts the
   line after `<<<BEGIN` and ends WITH the newline before `<<<END`).
3. C1 is the FIRST substantive commit, ahead of C2, per checklist item 23.
4. `.agent/live_review.md` is APPEND-ONLY. C2 appends RECORD6 and revises
   nothing already on disk.
5. NO NEW R-ID IS MINTED and NO DECISION ID IS MINTED. Registered 318 and
   resolved 55 stay UNMOVED (measured by the reviewer at `295cad25`);
   `DECISION F\d+ D\d+ — ` stays 19. `Gate: F106 R5 — ` occurs 0x before C2
   and exactly 1x after — that is RECORD6's own header, not a new finding.
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
11. Push after C6. Open NO pull request — T002b-i closes only ONE more
    slice of T002; T002b-ii, T002c and T003 remain.
12. Pair shapes, measured by the reviewer's own containment test before
    emission, reported here as the result, not the method: THREE pairs
    (FAKEPROVIDER-REVIEW, REVIEWER-CALL, TESTFILE-DOCSTRING) read `TO
    contains FROM: false` — each inserts new lines INSIDE the FROM span
    rather than leaving it verbatim as a prefix, so each is a REWRITE.
    TESTFILE-APPEND reads `TO contains FROM: true` — FROM is TO's exact
    PREFIX, so it is APPEND-shaped, not a rewrite (same shape as round
    5's TESTFILE-APPEND). Run the same containment test yourself for each
    of the four independently (do not generalize from one to the rest)
    and report your own result beside the reviewer's; if any of yours
    disagrees, apply the pair as given and declare the discrepancy rather
    than silently reclassifying it. For the THREE rewrite pairs: FROM
    occurs exactly 1x in its target file before its commit and 0x after;
    TO occurs 0x before and exactly 1x after. For TESTFILE-APPEND: FROM
    occurs exactly 1x before its commit and STILL exactly 1x after (it
    survives, embedded as TO's prefix); TO occurs 0x before and exactly
    1x after. Report all four readings, each against its own correct
    expectation.
13. Before C4, confirm `_build_provider_evidence` and
    `packages/orchestration/provider_token_evidence.py` are UNCHANGED —
    `git diff --stat` for that file, and for that function's body, must
    show nothing. Round 5's own dry-run proved surfacing a `resume_*`
    field into that dict trips its closed `ALLOWED_FIELDS` schema and
    reddens `tests/orchestration/test_provider_evidence_integration.py`;
    that path is not taken here either.
14. `FAKEPROVIDER-REVIEW`'s change must NOT alter
    `FakeProvider().review(...)` behavior when `supports_resume` is left
    at its default `False` — G6's zero-behavior probe on the DEFAULT
    constructor and the existing `TestZeroBehaviorChange` class already in
    the test file (untouched this round) are how this is proved; do not
    weaken or remove either.
15. `REVIEWER-CALL`'s `reviewer_resume_ref` computation reads
    `result.rounds[-1].reviewer_output` (the PRIOR round's Reviewer
    output, not the round in progress) — this is the Reviewer-side mirror
    of round 5's `BUILDER-CALL` pair, which read
    `result.rounds[-1].builder_output` under the identical `is_repair`
    guard for the identical reason. Verify this yourself by reading round
    5's own committed `BUILDER-CALL-TO` text (already in
    `packages/orchestration/pingpong_loop.py`, a few hundred lines above
    the Reviewer call site) before applying this round's pair. Apply the
    pair regardless of what you find; DECLARE if the precedent does not
    hold.
16. The bounded parse-retry call (`retry_out = _call_with_retry(... lambda
    ts=reviewer_timeout: reviewer_provider.review(retry_prompt, ...))`,
    a few dozen lines below the pair applied at C4) is a SEPARATE call
    site and is NOT part of this round's Change set — confirm by reading
    it before and after C4 that it is byte-identical, still passing no
    `resume` kwarg at all.

## Pairs

Each pair is FROM/TO, delimited the same way as prior rounds: content
starts the line after `<<<BEGIN` and ends with the newline before
`<<<END`.

<<<BEGIN RECORD6
Gate: F106 R5 — T002a: BUILDER REPAIR CALL ACTUALLY RESUMES. VERDICT PASS. The reviewer independently re-verified round 5's committed diff `32eb35c3..295cad25` against the real files, not the worker's summary, running every gate in the primary checkout (read-only, no worktree needed per the round's own constraint 8) after having already run the identical checks in a disposable dry-run worktree BEFORE authoring the round's block. G1 TRANSPORT: `.agent/authored/f106-r5.md`, `.agent/last_block.md` AND the reviewer's own held original `.remedy-wt/f106-r5-block.md` all sha256 `0fdf7546ff8fb60d696dd08e825da04f10509d14dc00598f0c696c81a6751f36`, 28841 bytes, three-way equal — not just worker-vs-worker. G2 THE PLAN: `.agent/plan.md` byte-equal to slice PLAN5, 42 lines. G3 THE RECORD APPEND: base 1819497 + `\n` + RECORD5 (3271 bytes) = 1822769, matching the committed file exactly; both readings (whole reconstruction, last-unit-suffix) `True`, independently computed against the real base read at commit `b90e6771` (not assumed from the block's own stated base). G4 THE LEDGER: independently re-measured — registered 318, resolved 55, open 263, `DECISION` 19, all unmoved; `Gate: F106 R4 — ` count exactly 1 at HEAD. G5 THE CODE — PAIR SHAPE: independently re-measured all five pairs (FAKEPROVIDER-INIT, FAKEPROVIDER-BUILD, BUILDER-CALL, TESTFILE-DOCSTRING as REWRITE; TESTFILE-APPEND as APPEND) against the real committed files at base `32eb35c3` and at HEAD — all five read exactly as the block predicted (four 1x→0x/0x→1x, one 1x→1x/0x→1x); `ast.parse` both files exit 0; `ruff check` exit 0. G6 ZERO BEHAVIOR CHANGE: `python3 -m pytest tests/orchestration/test_pingpong.py tests/orchestration/test_provider_mode.py tests/orchestration/test_provider_evidence_integration.py -q` independently re-run, REAL exit 0, 122 passed, matching base exactly. G7 THE NEW SURFACE: `test_session_resume.py` independently re-run, REAL exit 0, 16 passed, matching the block's stated count exactly. CONSTRAINT 16's closed-schema carve-out independently confirmed: `git diff --stat 32eb35c3..HEAD -- packages/orchestration/provider_token_evidence.py` reads EMPTY — the trust-bearing `ALLOWED_FIELDS` schema is genuinely untouched. G8 STATE READERS/CANARY: independently re-run, REAL exit 0 each, 515/52/21/16/42, all matching base. G9 THE TREE: `git status --porcelain` empty, 0 untracked, every commit's insertions under 500, 8 commits landing on exactly the 8 named change-set paths, nothing else. ONE NOTE, NOT A DEFECT: this round's own block was corrected TWICE by the reviewer BEFORE delegation — an early draft wrongly classified all six candidate pairs (including a since-dropped `EVIDENCE-BLOCK` pair) as rewrite-shaped, and a first attempt to surface `resume_used` into `_build_provider_evidence` was caught by the reviewer's OWN pre-delegation dry-run reddening `test_provider_evidence_integration.py` against the closed `ProviderTokenEvidenceV1` schema — both corrections landed in the block before the worker ever saw it, so no repair round was spent and no defect reached the committed diff. THE ROUND PASSES: T002a CLOSED — the Builder side of repair-round resume threading is honest, tested, and zero-behavior-change-proven.
<<<END RECORD6

<<<BEGIN PLAN6
# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 2, round 6.

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
| T002b-i: Reviewer repair call resumes when earned | done | this round |
| T002b-ii: F111 delta prompt shrink | open | next |
| T002c: expired-session fallback-once rule (verbatim) | open | |
| T003: measured fixture comparison + docs | open | |

## Next Steps
1. T002b-i mirrors T002a on the Reviewer side: the repair round's PRIMARY
   `review()` attempt now passes `resume=<prior round's captured Reviewer
   session id>` under the identical three-way guard. The bounded parse
   retry (a different call, same round) is NOT threaded — a declared
   scope line, not an oversight.
2. T002b-ii: the delta-prompt shrink via F111's existing diff-repair hunk
   selection — the repair prompt drops the regions the resumed session
   already holds. Not started.
3. T002c: the fallback-once rule verbatim (Orchestrator brief).
4. T003 follows once T002 is fully closed.

## Risks
- No adapter's `supports_resume` is true in production yet — only
  `FakeProvider`, via its test-only constructor override, ever resumes.
  Neither T002a nor T002b-i changes observable behavior for
  `ClaudeProvider`/`ClaudeCliProvider`, or for a default-constructed
  `FakeProvider`.
<<<END PLAN6

<<<BEGIN FAKEPROVIDER-REVIEW-FROM
    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> ReviewerOutput:
        out = self._review_impl(prompt, timeout_sec=timeout_sec,
                                max_output_chars=max_output_chars)
        out.prepared_input = prepare_call_input(
            prompt=prompt, model="fake", mode="fake",
            options={"max_output_chars": max_output_chars})
        return out
<<<END FAKEPROVIDER-REVIEW-FROM

<<<BEGIN FAKEPROVIDER-REVIEW-TO
    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> ReviewerOutput:
        out = self._review_impl(prompt, timeout_sec=timeout_sec,
                                max_output_chars=max_output_chars)
        # F106 T002b: honor an incoming resume request only when this fake
        # was constructed to support it — mirrors FakeProvider.build (T002a).
        out.resume_used = bool(resume) and self._supports_resume
        out.resume_session_ref = resume if out.resume_used else ""
        if self._fake_session_id:
            out.usage_actuals = {"session_id": self._fake_session_id}
        out.prepared_input = prepare_call_input(
            prompt=prompt, model="fake", mode="fake",
            options={"max_output_chars": max_output_chars})
        return out
<<<END FAKEPROVIDER-REVIEW-TO

<<<BEGIN REVIEWER-CALL-FROM
            _begin_stream_call(reviewer_provider, round_num, "attempt")
            # ONE logical reviewer call: its attempt AND its single parse retry share this
            # sink, and nothing from the builder or an earlier round is in it.
            reviewer_call_reasons: list[str] = []
            reviewer_out = _call_with_retry(
                lambda ts=reviewer_timeout: reviewer_provider.review(
                    reviewer_effective,
                    timeout_sec=ts,
                    max_output_chars=max_output_chars,
                ),
                result=result,
                role="reviewer",
                provider=reviewer_name,
                on_call=_rev_trace(
                    reviewer_effective,
                    "review",
                    "re-review" if is_repair else "review",
                ),
                on_provider_attempt=on_provider_call,
                call_reasons=reviewer_call_reasons,
                stop_check=_stopped,
                rate_governor=_rate_governor,
            )
<<<END REVIEWER-CALL-FROM

<<<BEGIN REVIEWER-CALL-TO
            _begin_stream_call(reviewer_provider, round_num, "attempt")
            # ONE logical reviewer call: its attempt AND its single parse retry share this
            # sink, and nothing from the builder or an earlier round is in it.
            reviewer_call_reasons: list[str] = []
            # F106 T002b-i: the repair round's PRIMARY Reviewer attempt
            # resumes the prior round's Reviewer session only when the
            # provider honestly advertises support AND a session id was
            # actually captured last round — same rule as the Builder side
            # (T002a). The bounded parse retry below is a DIFFERENT call and
            # is NOT threaded this round; it stays full-context.
            reviewer_resume_ref: str | None = None
            if is_repair and getattr(reviewer_provider, "supports_resume", False) and result.rounds:
                prev_reviewer_out = result.rounds[-1].reviewer_output
                prev_actuals = getattr(prev_reviewer_out, "usage_actuals", None) or {}
                prev_session_id = str(prev_actuals.get("session_id") or "")
                if prev_session_id:
                    reviewer_resume_ref = prev_session_id
            reviewer_out = _call_with_retry(
                lambda ts=reviewer_timeout: reviewer_provider.review(
                    reviewer_effective,
                    timeout_sec=ts,
                    max_output_chars=max_output_chars,
                    resume=reviewer_resume_ref,
                ),
                result=result,
                role="reviewer",
                provider=reviewer_name,
                on_call=_rev_trace(
                    reviewer_effective,
                    "review",
                    "re-review" if is_repair else "review",
                ),
                on_provider_attempt=on_provider_call,
                call_reasons=reviewer_call_reasons,
                stop_check=_stopped,
                rate_governor=_rate_governor,
            )
<<<END REVIEWER-CALL-TO

<<<BEGIN TESTFILE-DOCSTRING-FROM
"""Tests for the F106 session-resume capability surface (T001) and its first
repair-path wiring (T002a).

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
`packages/orchestration/pingpong_loop.py`; the Reviewer call and the
delta-prompt shrink are T002b.
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
<<<END TESTFILE-DOCSTRING-TO

<<<BEGIN TESTFILE-APPEND-FROM
    def test_initial_round_never_resumes(self, demo_repo: Path):
        provider = FakeProvider(supports_resume=True, fake_session_id="sess-1")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
        )
        assert result.rounds[0].builder_output.resume_used is False
<<<END TESTFILE-APPEND-FROM

<<<BEGIN TESTFILE-APPEND-TO
    def test_initial_round_never_resumes(self, demo_repo: Path):
        provider = FakeProvider(supports_resume=True, fake_session_id="sess-1")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
        )
        assert result.rounds[0].builder_output.resume_used is False


class TestT002bReviewerResumeThreading:
    """The repair round's PRIMARY Reviewer attempt resumes only when earned."""

    def test_repair_round_resumes_when_supported_and_session_known(self, demo_repo: Path):
        provider = FakeProvider(
            fail_on_round=1, pass_on_round=2,
            supports_resume=True, fake_session_id="sess-1",
        )
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2,
        )
        assert len(result.rounds) >= 2
        assert result.rounds[0].reviewer_output.resume_used is False
        assert result.rounds[0].reviewer_output.resume_session_ref == ""
        assert result.rounds[1].reviewer_output.resume_used is True
        assert result.rounds[1].reviewer_output.resume_session_ref == "sess-1"

    def test_repair_round_does_not_resume_when_provider_unsupported(self, demo_repo: Path):
        provider = FakeProvider(
            fail_on_round=1, pass_on_round=2,
            supports_resume=False, fake_session_id="sess-1",
        )
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2,
        )
        assert len(result.rounds) >= 2
        assert all(rd.reviewer_output.resume_used is False for rd in result.rounds)

    def test_repair_round_does_not_resume_without_a_prior_session_id(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=1, pass_on_round=2, supports_resume=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2,
        )
        assert len(result.rounds) >= 2
        assert all(rd.reviewer_output.resume_used is False for rd in result.rounds)

    def test_initial_round_never_resumes(self, demo_repo: Path):
        provider = FakeProvider(supports_resume=True, fake_session_id="sess-1")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
        )
        assert result.rounds[0].reviewer_output.resume_used is False
<<<END TESTFILE-APPEND-TO

## Done when — the gates

Run each gate and report ONE line per gate with its REAL exit code. Every
gate runs at a commit STRICTLY EARLIER than C6, which writes the handback.

G1 TRANSPORT, at C0b. Report the byte length of the committed
   `.agent/authored/f106-r6.md` and `.agent/last_block.md`; state whether
   equal. No expected length stated — the reviewer holds the original.

G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to slice PLAN6 (sha256 of
   both), under 50 lines, holds `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure `.agent/live_review.md`'s
   pre-commit byte length yourself (the reviewer read 1822769 at
   `295cad25`); base + `\n` + RECORD6 must equal the committed size. TWO
   readings: (a) whole reconstruction; (b) the committed file's last
   blank-line unit equals RECORD6 exactly (N=1).

G4 THE LEDGER, at C1 and C2. Registered/resolved/open unmoved from
   318/55/263. `DECISION` count 19 at both (line-anchored regex). `Gate:
   F106 R5 — ` 0x before C2, 1x after.

G5 THE CODE — PAIR SHAPE AND ORDERED APPLICATION, at C3-C5. For EACH of
   the four pairs (FAKEPROVIDER-REVIEW, REVIEWER-CALL, TESTFILE-DOCSTRING,
   TESTFILE-APPEND): run your own containment test (`TO contains FROM`)
   and report the result; then report FROM's occurrence count in its
   target file before its commit and after, and TO's occurrence count
   before and after. For the three REWRITE pairs (all but
   TESTFILE-APPEND), FROM must read 1x→0x and TO 0x→1x. For
   TESTFILE-APPEND (append-shaped), FROM must read 1x→1x (it survives as
   TO's prefix) and TO must read 0x→1x. Then, after C3/C4: `python3 -c
   "import ast; ast.parse(open('packages/orchestration/pingpong_provider.py').read())"`
   and the same for `pingpong_loop.py`, both exit 0. After C5: `python3
   -m ruff check tests/orchestration/test_session_resume.py` exits 0.

G6 ZERO BEHAVIOR CHANGE ON THE DEFAULT PATH, at C3/C4. Run
   `python3 -m pytest tests/orchestration/test_pingpong.py
   tests/orchestration/test_provider_mode.py
   tests/orchestration/test_provider_evidence_integration.py -q` — the
   reviewer measured 122 passed at the base; report yours (must be
   unchanged — every existing call site constructs `FakeProvider()` with
   `supports_resume` left at its default `False`).

G7 THE NEW SURFACE, at C5. `python3 -m pytest
   tests/orchestration/test_session_resume.py -q` — report exit code and
   passed count; the reviewer's own count after both pairs apply is 20
   (the 16 carried in from round 5, unchanged, plus 4 new in
   `TestT002bReviewerResumeThreading`) — restate your own exact count
   rather than trusting this one; if it disagrees, report the discrepancy
   and the actual collected count via `python3 -m pytest
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
steps — explicitly note T002b-i is CLOSED and T002b-ii (F111 delta shrink)
is next. States `SESSION 2` of F106, round 6. No length cap.
