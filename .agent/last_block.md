--- STEP R8/F106 — T002c-ii: Reviewer fallback-once on a failed resume ---

Goal: book the round 7 verdict, then land T002c-ii — the Reviewer-side
mirror of round 7's fallback-once rule: a resume attempt that errors
falls back ONCE, same round, to `resume=None`, recorded on the new
`ReviewerOutput.resume_fallback` field, gated on `reviewer_resume_ref`
having been set AND the call erroring; a plain call failure with no
resume in play falls straight through to the EXISTING terminal-error /
malformed-output parse-retry handling, unchanged. `FakeProvider.review`
gains the same test-only `resume_fails` early-return branch
`FakeProvider.build` gained in round 7. No real adapter's
`supports_resume` turns True in production this round.
`_build_provider_evidence` / `provider_evidence.json` are NOT touched —
same carve-out as round 7. KNOWN, DECLARED SIMPLIFICATION (same as round
7's): a fallback issues a SECOND real provider call inside the SAME
round, so `result.provider_attempts` grows by one extra
"reviewer"/"attempt" entry when a round falls back — accurate, not a
defect. With T002c-ii landed, T002c is CLOSED on both sides; T002b-ii
(F111 delta-prompt shrink) and T003 remain open, not this round.

Base: `2a17ee639be5f8cc4319e57f4dd1b7e0d7e85fe9`, the tip of
`feature/f106-session-resume` after round 7. Same branch, no new branch.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f106-r8.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN8
- C2  append slice RECORD8 (the round 7 verdict) to `.agent/live_review.md`
- C3  apply the two pairs below to `packages/orchestration/pingpong_provider.py`
- C4  apply the one pair below to `packages/orchestration/pingpong_loop.py`
- C5  apply the three pairs below to `tests/orchestration/test_session_resume.py`
- C6  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f106-r8.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    packages/orchestration/pingpong_provider.py
    packages/orchestration/pingpong_loop.py
    tests/orchestration/test_session_resume.py
    .agent/handoff.md

No other file changes this round. `ClaudeProvider`/`ClaudeCliProvider`, the
Builder call site (round 7's own fallback), the parse-retry call site, and
`_build_provider_evidence` are all untouched this round.

## Constraints

1. Apply every slice/pair BYTE FOR BYTE; if one looks wrong, apply it as
   given and DECLARE the problem — never fix, rewrap or improve it.
2. C0a/C0b: `shutil.copyfile` from `.remedy-wt/f106-r8-block.md` for C0a,
   then from the committed `.agent/authored/f106-r8.md` for C0b. Never
   `cp`, never retype. Extract every slice/pair from the COMMITTED
   `.agent/authored/f106-r8.md` via the marker convention (content starts
   the line after `<<<BEGIN`, ends with the newline before `<<<END`).
3. C1 is the FIRST substantive commit, ahead of C2 (checklist item 23).
4. `.agent/live_review.md` is APPEND-ONLY; C2 appends RECORD8 and revises
   nothing already on disk.
5. NO NEW R-ID/DECISION ID MINTED. Registered 318, resolved 55 stay
   UNMOVED (measured by the reviewer at
   `2a17ee639be5f8cc4319e57f4dd1b7e0d7e85fe9`); `DECISION F\d+ D\d+ — `
   stays 19. `Gate: F106 R7 — ` 0x before C2, 1x after — RECORD8's own
   header, not a new finding.
6. `.agent/plan.md` stays under 50 lines (AGENTS.md).
7. Every exit code is REAL, from `subprocess.run(...).returncode` in a
   script under gitignored `.remedy-wt/` — never through a pipe.
8. All checks this round are read-only against the primary checkout
   (imports, `ast.parse`, pytest runs) — no worktree needed; none of
   G1-G8 below mutates a file outside a script's own transient copy.
9. `remedy` the console script is DENIED in this sandbox; use
   `python3 -m apps.cli.main ...`.
10. Commit subjects: no leading-slash token, no absolute path, no
    secret-like string, no `Co-Authored-By` trailer.
11. Push after C6. Open NO pull request — T002c-ii closes T002c (both
    sides now done); T002b-ii and T003 remain.
12. Pair shapes, measured by the reviewer's own containment test, reported
    here as the result not the method: FIVE pairs (REVIEWEROUTPUT-FIELD,
    FAKEPROVIDER-REVIEW-EARLYFAIL, REVIEWER-CALL-FALLBACK,
    TESTFILE-DOCSTRING-HEADER, TESTFILE-DOCSTRING-T002C) read `TO contains
    FROM: false` (REWRITE). The sixth, TESTFILE-APPEND, reads `TO contains
    FROM: true` (APPEND-shaped, FROM is TO's exact prefix — same shape as
    every prior round's TESTFILE-APPEND). Run the containment test
    yourself for each of the six and report beside the reviewer's; if any
    disagrees, apply the pair as given and declare the discrepancy. For
    the FIVE rewrite pairs: FROM 1x→0x, TO 0x→1x in the target file. For
    TESTFILE-APPEND: FROM 1x→1x (survives as TO's prefix), TO 0x→1x.
    Report all six readings against their own correct expectation.
13. After C3/C4, both files must still be valid Python: `python3 -c "import
    ast; ast.parse(open('packages/orchestration/pingpong_provider.py').read())"`
    and the same for `pingpong_loop.py`, both exit 0. After C5,
    `python3 -m ruff check tests/orchestration/test_session_resume.py`
    must exit 0.
14. `FAKEPROVIDER-REVIEW-EARLYFAIL` must NOT alter
    `FakeProvider().review(...)` when `resume_fails`/`supports_resume` are
    left at their defaults — G6's zero-behavior probe and the existing,
    untouched `TestZeroBehaviorChange` class prove this.
15. `REVIEWER-CALL-FALLBACK`'s FROM/TO span starts right after the PRIMARY
    attempt's own `_call_with_retry(...)` (unpaired, untouched, immediately
    above). The fallback branch inside the pair's TO reuses that call's
    EXACT SAME shape, only `resume=reviewer_resume_ref`→`resume=None` and
    a reset `reviewer_call_reasons` differ — verify by comparing the
    fallback call against the primary call immediately above the pair
    (same `on_call=_rev_trace(...)` shape too). `_finalize_call`, the
    `malformed_output:` bounded parse-retry, and the terminal-error
    handling below (unpaired, untouched) all run exactly once per round,
    against whichever `reviewer_out` the fallback leaves behind.
16. Before C4, confirm `_build_provider_evidence`, the Builder call site
    (with round 7's own fallback), and the parse-retry call site are
    UNCHANGED — `git diff --stat` for `provider_token_evidence.py` empty;
    the other two call sites read byte-identical to the round's base.

## Pairs

Each pair is FROM/TO, delimited the same way as prior rounds: content
starts the line after `<<<BEGIN` and ends with the newline before
`<<<END`.

<<<BEGIN RECORD8
Gate: F106 R7 — T002c-i: BUILDER FALLBACK-ONCE ON A FAILED RESUME. VERDICT PASS. The reviewer (a fresh session) independently re-verified round 7's committed diff `e41b96395dd4251fd458c37fe37d2e3065a1633b..2a17ee639be5f8cc4319e57f4dd1b7e0d7e85fe9` against the real files, not the worker's summary. G1 TRANSPORT: `.agent/authored/f106-r7.md` and `.agent/last_block.md` independently sha256'd at `0e918483ed59840630d8c69430f5b8cb2ef68e0063b28ea2550fdd138c175dba`, both 30595 bytes, matching each other and the handback's claim. G2 THE PLAN: `.agent/plan.md` independently sha256'd at `018804af6767866f42c8f01ee531d1dfdae3eafee2bf37037fdbca80c2b261eb`, 41 lines, holding `## Goal` and `## Next Steps`, matching the handback exactly. G3 THE RECORD APPEND: independently re-measured `.agent/live_review.md` at HEAD as 1828730 bytes, equal to the handback's own arithmetic (base 1826027 + separator + RECORD7 2702 = 1828730) — a whole-file re-check, not a re-derivation of RECORD7's own bytes from an earlier base. G4 THE LEDGER: independently re-measured with the same line-anchored regexes — registered 318, resolved 55 (distinct `Done:` ids; raw `Done:` line count 57, `R-0721`/`R-0725` each carrying two lines, the known wrinkle carried since round 5), `DECISION` 19, all unmoved from round 6; `Gate: F106 R6 — ` exactly 1x, `Gate: F106 R7 — ` exactly 0x before this entry. G5 THE CODE: read directly against the real diff rather than re-run as a mechanical occurrence count. `BuilderOutput` gains `resume_fallback: bool = False`; `FakeProvider.__init__` gains a test-only `resume_fails: bool = False`; `FakeProvider.build` gains an early-return branch — `if resume and self._supports_resume and self._resume_fails:` returns `error="resume_lost: session context unavailable"` — unreachable on every existing call site, since every one constructs `FakeProvider()` with `resume_fails` left at its default `False`. The Builder call site in `pingpong_loop.py` gains a fallback-once branch immediately after the primary `_call_with_retry(...)` call: `if builder_resume_ref and builder_out.error:` fires a second, structurally parallel `_call_with_retry(...)` with `resume=None` and a reset `builder_call_reasons`, setting `builder_out.resume_fallback = True`; confirmed the ONLY hunk in that file's diff (Reviewer call site and the bounded parse-retry call site read byte-identical to their base state). `packages/orchestration/provider_token_evidence.py` confirmed untouched, `git diff --stat` empty. `python3 -m ruff check` on all three touched files: exit 0, `All checks passed!`. G6 ZERO BEHAVIOR CHANGE: `python3 -m pytest tests/orchestration/test_pingpong.py tests/orchestration/test_provider_mode.py tests/orchestration/test_provider_evidence_integration.py -q` independently re-run, REAL exit 0, 122 passed, matching base exactly. G7 THE NEW SURFACE: `python3 -m pytest tests/orchestration/test_session_resume.py -q` independently re-run, REAL exit 0, 23 passed, matching the handback's stated count exactly; the three new `TestT002cBuilderFallbackOnce` tests read directly and confirmed correctly gated — a resume error on a repair round falls back once and the round completes with `resume_fallback` True and `resume_used` False; no fallback fires when no resume was attempted; no fallback fires when the provider does not support resume. G8 STATE READERS/CANARY: independently re-run, REAL exit 0 each — `tests/ui_server/` 515, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16, canary `tests/cli/test_golden_path.py` 42, all matching base exactly (an initial `find`-based path lookup briefly matched the WRONG same-named files outside `tests/orchestration/`/`tests/cli/`, giving 43/not-found/not-found; corrected to the actual paths before this reading — a reviewer path-lookup slip, not a defect on disk, booked to `.agent/prose_slips.md` per amend0827-process-diet rule 2, no R-id spent). G9 THE TREE: `git status --porcelain` empty, `git ls-files --others --exclude-standard` 0 untracked; every commit's insertions under 500 except the two exempt `.agent/**` verbatim-state-file commits (C0a 600, C0b 310, AGENTS.md Commit Discipline carve-out); the five code/test/state commits (C1 14, C2 2, C3 15, C4 26, C5 52) all well under 500. NO DEVIATIONS beyond the reviewer's own path-lookup slip noted above — the bundle landed exactly as the handback describes. THE ROUND PASSES: T002c-i CLOSED — the Builder side of the fallback-once rule is honest, tested, and zero-behavior-change-proven.
<<<END RECORD8

<<<BEGIN PLAN8
# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 2, round 8.

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
| T002c-i: Builder fallback-once on a failed resume | done | round 7 |
| T002c-ii: Reviewer fallback-once mirror | done | this round |
| T002b-ii: F111 delta prompt shrink | open | next |
| T003: measured fixture comparison + docs | open | |

## Next Steps
1. T002b-ii: the delta-prompt shrink via F111's existing diff-repair hunk
   selection. Needs its own research pass into the hunk-selection code
   before design — not started.
2. T003 follows once T002 is fully closed (after T002b-ii lands).

## Risks
- No adapter's `supports_resume` is true in production yet — only
  `FakeProvider`, via its test-only constructor overrides, ever resumes
  or fails a resume. None of T002a/b-i/c-i/c-ii changes observable
  behavior for `ClaudeProvider`/`ClaudeCliProvider`, or for a
  default-constructed `FakeProvider`.
<<<END PLAN8

<<<BEGIN REVIEWEROUTPUT-FIELD-FROM
    resume_used: bool = False
    resume_session_ref: str = ""
    incomplete: bool = False
<<<END REVIEWEROUTPUT-FIELD-FROM

<<<BEGIN REVIEWEROUTPUT-FIELD-TO
    resume_used: bool = False
    resume_session_ref: str = ""
    # F106 T002c: true only when a resume attempt on this round's call
    # errored and a same-round fallback to full context was taken (mirrors
    # BuilderOutput.resume_fallback).
    resume_fallback: bool = False
    incomplete: bool = False
<<<END REVIEWEROUTPUT-FIELD-TO

<<<BEGIN FAKEPROVIDER-REVIEW-EARLYFAIL-FROM
    ) -> ReviewerOutput:
        out = self._review_impl(prompt, timeout_sec=timeout_sec,
                                max_output_chars=max_output_chars)
<<<END FAKEPROVIDER-REVIEW-EARLYFAIL-FROM

<<<BEGIN FAKEPROVIDER-REVIEW-EARLYFAIL-TO
    ) -> ReviewerOutput:
        # F106 T002c: a test-only way to simulate a resume attempt that
        # errors, so the fallback-once path in pingpong_loop.py has
        # something real to fall back FROM. Only fires when a resume was
        # actually requested on a provider that claims to support it —
        # never on a plain (non-resume) call.
        if resume and self._supports_resume and self._resume_fails:
            return ReviewerOutput(
                error="resume_lost: session context unavailable",
                provider="fake",
            )
        out = self._review_impl(prompt, timeout_sec=timeout_sec,
                                max_output_chars=max_output_chars)
<<<END FAKEPROVIDER-REVIEW-EARLYFAIL-TO

<<<BEGIN REVIEWER-CALL-FALLBACK-FROM
            )

            # F012: the Reviewer attempt is finalized. Track the exact finalized context so a
            # terminal reviewer failure records F010 against it (F10).
            reviewer_final_ctx = _finalize_call(
<<<END REVIEWER-CALL-FALLBACK-FROM

<<<BEGIN REVIEWER-CALL-FALLBACK-TO
            )
            # F106 T002c: a resume attempt that errors falls back ONCE to the
            # full-context path within the same round — an honest, evidenced
            # event, never a task failure by itself (Orchestrator brief,
            # verbatim). Only fires when a resume was actually attempted
            # (``reviewer_resume_ref`` set); a plain call failure with no
            # resume in play is unaffected and falls straight through to the
            # existing terminal-error / parse-retry handling below,
            # unchanged.
            if reviewer_resume_ref and reviewer_out.error:
                _begin_stream_call(reviewer_provider, round_num, "attempt")
                reviewer_call_reasons = []
                reviewer_out = _call_with_retry(
                    lambda ts=reviewer_timeout: reviewer_provider.review(
                        reviewer_effective,
                        timeout_sec=ts,
                        max_output_chars=max_output_chars,
                        resume=None,
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
                reviewer_out.resume_fallback = True

            # F012: the Reviewer attempt is finalized. Track the exact finalized context so a
            # terminal reviewer failure records F010 against it (F10).
            reviewer_final_ctx = _finalize_call(
<<<END REVIEWER-CALL-FALLBACK-TO

<<<BEGIN TESTFILE-DOCSTRING-HEADER-FROM
"""Tests for the F106 session-resume capability surface (T001) and its
repair-path wiring (T002a, T002b-i, T002c-i).
<<<END TESTFILE-DOCSTRING-HEADER-FROM

<<<BEGIN TESTFILE-DOCSTRING-HEADER-TO
"""Tests for the F106 session-resume capability surface (T001) and its
repair-path wiring (T002a, T002b-i, T002c-i, T002c-ii).
<<<END TESTFILE-DOCSTRING-HEADER-TO

<<<BEGIN TESTFILE-DOCSTRING-T002C-FROM
T002c-i covers the Builder-side fallback-once rule: a resume attempt that
errors falls back ONCE, same round, to `resume=None`, recorded on the new
`BuilderOutput.resume_fallback` field — gated strictly on a resume having
actually been attempted, so a plain call failure is unaffected.
`FakeProvider`'s test-only `resume_fails` override makes this failure
mode reproducible without a real provider. The Reviewer-side mirror
(T002c-ii) and the delta-prompt shrink (T002b-ii) remain open.
"""
<<<END TESTFILE-DOCSTRING-T002C-FROM

<<<BEGIN TESTFILE-DOCSTRING-T002C-TO
T002c-i covers the Builder-side fallback-once rule: a resume attempt that
errors falls back ONCE, same round, to `resume=None`, recorded on the new
`BuilderOutput.resume_fallback` field — gated strictly on a resume having
actually been attempted, so a plain call failure is unaffected.
`FakeProvider`'s test-only `resume_fails` override makes this failure
mode reproducible without a real provider.

T002c-ii covers the identical rule on the Reviewer side: a resume attempt
that errors falls back ONCE, same round, to `resume=None`, recorded on the
new `ReviewerOutput.resume_fallback` field, under the same gating (a
resume must actually have been attempted). With both halves landed, T002c
is CLOSED; the delta-prompt shrink (T002b-ii) remains open.
"""
<<<END TESTFILE-DOCSTRING-T002C-TO

<<<BEGIN TESTFILE-APPEND-FROM
        assert len(result.rounds) >= 2
        assert all(rd.builder_output.resume_fallback is False for rd in result.rounds)
<<<END TESTFILE-APPEND-FROM

<<<BEGIN TESTFILE-APPEND-TO
        assert len(result.rounds) >= 2
        assert all(rd.builder_output.resume_fallback is False for rd in result.rounds)


class TestT002cReviewerFallbackOnce:
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
        assert result.rounds[1].reviewer_output.error == ""
        assert result.rounds[1].reviewer_output.resume_used is False
        assert result.rounds[1].reviewer_output.resume_fallback is True
        assert result.final_status == "staged_review_passed"

    def test_no_fallback_when_no_resume_attempted(self, demo_repo: Path):
        provider = FakeProvider(supports_resume=True, fake_session_id="sess-1", resume_fails=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
        )
        assert result.rounds[0].reviewer_output.error == ""
        assert result.rounds[0].reviewer_output.resume_fallback is False

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
        assert all(rd.reviewer_output.resume_fallback is False for rd in result.rounds)
<<<END TESTFILE-APPEND-TO

## Done when — the gates

Report ONE line per gate with its REAL exit code; every gate runs strictly before C6, which writes the handback.

G1 TRANSPORT, at C0b. Report the byte length of `.agent/authored/f106-r8.md`
   and `.agent/last_block.md`; state whether equal (reviewer holds the original).

G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to slice PLAN8 (sha256 of
   both), under 50 lines, holds `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure the pre-commit byte length
   yourself (reviewer read 1828730 at `2a17ee63`); base + `\n` + RECORD8
   must equal the committed size. TWO readings: (a) whole reconstruction;
   (b) the committed file's last blank-line unit equals RECORD8 (N=1).

G4 THE LEDGER, at C1 and C2. Registered/resolved/open unmoved from
   318/55/263. `DECISION` count 19 at both (line-anchored regex). `Gate:
   F106 R7 — ` 0x before C2, 1x after.

G5 THE CODE — PAIR SHAPE AND ORDERED APPLICATION, at C3-C5. For EACH of
   the six pairs (REVIEWEROUTPUT-FIELD, FAKEPROVIDER-REVIEW-EARLYFAIL,
   REVIEWER-CALL-FALLBACK, TESTFILE-DOCSTRING-HEADER,
   TESTFILE-DOCSTRING-T002C, TESTFILE-APPEND): run your own containment
   test and report FROM's/TO's occurrence counts before/after its commit.
   The five REWRITE pairs: FROM 1x→0x, TO 0x→1x. TESTFILE-APPEND: FROM
   1x→1x (survives as TO's prefix), TO 0x→1x. After C3/C4: `python3 -c
   "import ast;
   ast.parse(open('packages/orchestration/pingpong_provider.py').read())"`
   and the same for `pingpong_loop.py`, both exit 0. After C5: `python3
   -m ruff check tests/orchestration/test_session_resume.py` exits 0.

G6 ZERO BEHAVIOR CHANGE ON THE DEFAULT PATH, at C3/C4. `python3 -m pytest
   tests/orchestration/test_pingpong.py tests/orchestration/test_provider_mode.py
   tests/orchestration/test_provider_evidence_integration.py -q` — reviewer
   measured 122 passed at base; report yours (must be unchanged — every
   existing call site leaves `supports_resume`/`resume_fails` at default).

G7 THE NEW SURFACE, at C5. `python3 -m pytest
   tests/orchestration/test_session_resume.py -q` — report exit code and
   passed count; reviewer's own count after all three pairs apply is 26 (23
   carried in from round 7 plus 3 new in `TestT002cReviewerFallbackOnce`)
   — restate your own count; if it disagrees, report the discrepancy and
   the `--collect-only` count before ruling.

G8 THE STATE READERS, CANARY AND THE TREE. Each its own real exit code,
   after C2: `python3 -m pytest tests/ui_server/ -q`, `python3 -m pytest
   tests/orchestration/test_test_runner.py -q`, `python3 -m pytest
   tests/regression/test_resource_safety.py -q`, `python3 -m pytest
   tests/orchestration/test_integrity_gate.py -q`, canary `python3 -m
   pytest tests/cli/test_golden_path.py -q`. Reviewer measured 515, 52,
   21, 16, 42 at base; report yours. Tree, at C5: `git status --porcelain`
   empty, `git ls-files --others --exclude-standard` count 0, every
   commit's insertions under 500 (`git diff --numstat`).

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: state
block, `## Commits` table (`+/-` from `git diff --numstat`), deviations,
item-status table with every bundle item and gate exactly once, next
steps — note T002c CLOSED (both halves), T002b-ii and T003 remaining,
T002b-ii needing its own research pass into F111's hunk-selection code.
States `SESSION 2` of F106, round 8. No length cap.
