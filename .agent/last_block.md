--- STEP R5/F106 — T002a: Builder repair call actually resumes ---

Goal: book the round 4 verdict, then land the FIRST slice of T002 — the
repair round's Builder call actually passes `resume=<prior round's
captured session id>`, but ONLY when the Builder provider's
`supports_resume` is honestly true AND a prior session id was actually
captured. `FakeProvider` gains a test-only `fake_session_id` constructor
override so a test can simulate a provider that reports a session id, and
now genuinely honors an incoming `resume` request when
`supports_resume=True`. No real adapter's `supports_resume` turns True in
production this round — this is honest wiring, not a capability grant.
`resume_used`/`resume_session_ref` land on the per-round `BuilderOutput`
only (already true since T001); surfacing them into the trust-bearing,
CLOSED-schema `provider_evidence.json` (`ALLOWED_FIELDS` in
`packages/orchestration/provider_token_evidence.py`) is deliberately OUT
OF SCOPE this round — that schema is a separate versioned contract with
its own downstream `TokenTruthV1` canonicalization, and belongs to T002b
or T003, not folded silently into this round's diff. The Reviewer's own
call, the F111 delta-prompt shrink and the fallback-once rule are
T002b/T002c, not this round.

Base: `32eb35c381533646eab97139ed6f930ac6e0736a`, the tip of
`feature/f106-session-resume` after round 4. Same branch, no new branch.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f106-r5.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN5
- C2  append slice RECORD5 (the round 4 verdict) to `.agent/live_review.md`
- C3  apply the two pairs below to
      `packages/orchestration/pingpong_provider.py`
- C4  apply the one pair below to `packages/orchestration/pingpong_loop.py`
- C5  apply the two pairs below to
      `tests/orchestration/test_session_resume.py`
- C6  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f106-r5.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    packages/orchestration/pingpong_provider.py
    packages/orchestration/pingpong_loop.py
    tests/orchestration/test_session_resume.py
    .agent/handoff.md

No other file changes this round. `ClaudeProvider`/`ClaudeCliProvider` are
NOT touched — only `FakeProvider`. In `pingpong_loop.py`, ONLY the Builder
call site changes — `_build_provider_evidence` and the closed-schema
`provider_evidence.json` path are explicitly NOT touched this round (see
Goal). The Reviewer call site (also in `pingpong_loop.py`, a different
function/lines) is NOT touched this round either — that is T002b, paired
with the delta-prompt shrink.

## Constraints

1. Apply every slice and pair BYTE FOR BYTE. Do not fix, rewrap or improve
   one. If a slice or pair looks wrong, apply it as given and DECLARE the
   problem.
2. C0a/C0b: `shutil.copyfile` from the reviewer's scratch original at
   `.remedy-wt/f106-r5-block.md` for C0a, then from the committed
   `.agent/authored/f106-r5.md` for C0b. Never `cp`, never retype. Extract
   every slice/pair from the COMMITTED `.agent/authored/f106-r5.md`, using
   the marker convention verified in round 3/4 (content starts the line
   after `<<<BEGIN` and ends WITH the newline before `<<<END`, i.e. the
   trailing newline before the marker is PART of the slice).
3. C1 is the FIRST substantive commit, ahead of C2, per checklist item 23.
4. `.agent/live_review.md` is APPEND-ONLY. C2 appends RECORD5 and revises
   nothing already on disk.
5. NO NEW R-ID IS MINTED and NO DECISION ID IS MINTED. Registered 318 and
   resolved 55 stay UNMOVED (measured by the reviewer at `32eb35c3`);
   `DECISION F\d+ D\d+ — ` stays 19. `Gate: F106 R4 — ` occurs 0x before C2
   and exactly 1x after — that is RECORD5's own header, not a new finding.
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
11. Push after C6. Open NO pull request — T002a closes only the first
    slice of T002; T002b, T002c and T003 remain.
12. Pair shapes, measured by the reviewer's own containment test before
    emission, reported here as the result, not the method: FOUR pairs
    (FAKEPROVIDER-INIT, FAKEPROVIDER-BUILD, BUILDER-CALL,
    TESTFILE-DOCSTRING) read `TO contains FROM: false` — each inserts new
    lines INSIDE the FROM span rather than leaving it verbatim as a
    prefix, so each is a REWRITE. TESTFILE-APPEND reads `TO contains
    FROM: true` — FROM is TO's exact PREFIX, so it is APPEND-shaped, not
    a rewrite. Run the same containment test yourself for each of the
    five independently (do not generalize from one to the rest, and do
    not assume TESTFILE-APPEND is a rewrite because the other four are)
    and report your own result beside the reviewer's; if any of yours
    disagrees, apply the pair as given and declare the discrepancy rather
    than silently reclassifying it. For the FOUR rewrite pairs: FROM
    occurs exactly 1x in its target file before its commit and 0x after;
    TO occurs 0x before and exactly 1x after. For TESTFILE-APPEND: FROM
    occurs exactly 1x before its commit and STILL exactly 1x after (it
    survives, embedded as TO's prefix — 1x→0x would be the WRONG
    expectation for an append-shaped pair); TO occurs 0x before and
    exactly 1x after. Report all five readings, each against its own
    correct expectation.
13. After C3/C4, both files must still be valid Python: `python3 -c "import
    ast; ast.parse(open('packages/orchestration/pingpong_provider.py').read())"`
    and the same for `pingpong_loop.py`, both exit 0. After C5,
    `python3 -m ruff check tests/orchestration/test_session_resume.py`
    must exit 0.
14. `FAKEPROVIDER-BUILD`'s change must NOT alter `FakeProvider().build(...)`
    behavior when `supports_resume` is left at its default `False` — G6's
    zero-behavior probe on the DEFAULT constructor and the existing
    `TestZeroBehaviorChange` class already in the test file (untouched
    this round) are how this is proved; do not weaken or remove either.
15. `BUILDER-CALL`'s `builder_resume_ref` computation reads `result.rounds`
    (the PRIOR rounds already appended, not the round in progress) — verify
    this yourself by reading the ~15 lines immediately above the pair's
    FROM span in the committed file before applying, where the existing
    `prev_test_result` computation reads `result.rounds[-1]` under the same
    `is_repair` guard for the identical reason. Apply the pair regardless
    of what you find; DECLARE if the precedent does not hold.
16. Before C4, confirm `_build_provider_evidence` and the
    `provider_evidence.json` closed-schema path in
    `packages/orchestration/provider_token_evidence.py` are UNCHANGED —
    `git diff --stat` for that file and for the evidence-building function
    must show nothing. This round proved by trying it in a disposable
    dry-run worktree that adding `resume_used` directly to that dict trips
    `ALLOWED_FIELDS`'s closed-schema check and reddens
    `tests/orchestration/test_provider_evidence_integration.py`; that path
    is deliberately not taken here.

## Pairs

Each pair is FROM/TO, delimited the same way as prior rounds: content
starts the line after `<<<BEGIN` and ends with the newline before
`<<<END`.

<<<BEGIN RECORD5
Gate: F106 R4 — T001c: THE DEDICATED TEST FILE, CLOSES T001. VERDICT PASS. The reviewer (a fresh session, no memory of round 4's own work) independently re-verified round 4's committed diff `6bef86f1..32eb35c3` against the round's own handback, not against the worker's summary. G1 TRANSPORT: `.agent/authored/f106-r4.md` and `.agent/last_block.md` sha256 `02040e0211394c0d42445410c0336cd287637f1ba4ec29b528d9a25ea67ed55b` both, confirmed by direct `sha256sum` on the committed files, matching the handback's claim exactly. G2 THE PLAN: `.agent/plan.md` sha256 `4af5dd3b2e7bd1870d2217a0a3206c86846a8e92573ea1cf226a0ad0ba77c0fe`, 36 lines (`wc -l`), matching. G3 THE RECORD APPEND: independently confirmed the file's last paragraph before this round's own append is `Gate: F106 R3 — ...` — RECORD4 landed cleanly with no residual trailing-newline defect; the round's three declared follow-up commits (`51786188`, `8e652992`, `2aa76530`) are visible in `git log --oneline` exactly where the handback places them. G4 THE LEDGER: independently re-measured with the same line-anchored regexes (`^- (R-\d{4}) — `, `^Done: (R-\d{4}) — `, `^DECISION F\d+ D\d+ — `) — registered 318, resolved 55, open 263, `DECISION` 19, all matching the handback exactly; `git status --porcelain` and `git ls-files --others --exclude-standard` both confirmed empty at the start of this review. G5 THE NEW FILE: `tests/orchestration/test_session_resume.py` sha256 `540d84639fe4da9df177fa2b40b244875f213d0781c450acd18b687d04905cae`, confirmed by direct `sha256sum`; `python3 -m pytest tests/orchestration/test_session_resume.py -q` re-run independently, REAL exit 0, 12 passed — matching the handback's dry-run reading. The handback's own two-worktree mutation red-proof (run against the final byte-correct file, with a purged `__pycache__` and `python3 -B` throughout) is accepted as sufficient and not re-executed destructively a third time against unchanged bytes. G6 EXISTING SUITE: `python3 -m pytest tests/orchestration/test_pingpong.py tests/orchestration/test_provider_mode.py tests/orchestration/test_provider_evidence_integration.py -q` re-run independently, REAL exit 0, 122 passed, matching the base exactly (this round added a test file but touched no production code). G7/G8 (state readers, canary, ruff, tree): not independently re-run this round — round 4's diff touches no path any of those five suites or the linter's target cover beyond the new test file, already re-verified above; the handback's own readings (515/52/21/16/42, `ruff` clean, tree clean, every commit's insertions under 500) are accepted. ONE NOTE, NOT A DEFECT: round 4's own Deviations item 1 (a trailing-newline extraction bug, self-caused, caught only at G8 and fixed across three follow-up commits rather than round 3's single-commit catch of the identical bug) is a documented process observation; every affected file is independently confirmed sha256-equal to its correctly-extracted slice at HEAD above, so nothing on disk is wrong. THE ROUND PASSES: T001 CLOSED — all three adapters (`FakeProvider`, `ClaudeProvider`, `ClaudeCliProvider`) share the honest `supports_resume`/`resume`/evidence-field surface, dedicated tests exist and pass, zero behavior change held throughout T001.
<<<END RECORD5

<<<BEGIN PLAN5
# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 2, round 5.

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
| T002a: Builder repair call resumes when earned | done | this round |
| T002b: Reviewer resume + F111 delta prompt shrink | open | next |
| T002c: expired-session fallback-once rule (verbatim) | open | |
| T003: measured fixture comparison + docs | open | |

## Next Steps
1. T002a wires the Builder side only: a repair round's `build()` call now
   passes `resume=<prior round's captured session id>` exactly when the
   Builder provider's `supports_resume` is true and a prior session id was
   actually captured — never guessed, never sent otherwise. `resume_used`/
   `resume_session_ref` land on the per-round `BuilderOutput` only;
   surfacing them into the closed-schema `provider_evidence.json` is
   deliberately deferred, not part of this slice.
2. T002b: the same threading on the Reviewer's `review()` call, plus the
   delta-prompt shrink via F111's existing diff-repair hunk selection.
3. T002c: the fallback-once rule verbatim (Orchestrator brief) — a resume
   attempt that errors or loses context falls back ONCE to full context
   within the same round, evidenced, never a task failure by itself.
4. T003 follows once T002 is fully closed.

## Risks
- No adapter's `supports_resume` is true in production yet — only
  `FakeProvider`, via its test-only constructor override, ever resumes.
  T002a changes no observable behavior for `ClaudeProvider`/
  `ClaudeCliProvider`, and none for a default-constructed `FakeProvider`.
<<<END PLAN5

<<<BEGIN FAKEPROVIDER-INIT-FROM
        malformed_review_recoverable: bool = False,
        supports_resume: bool = False,
    ) -> None:
        self._builder_files = builder_files or ["docs/README.md"]
        self._supports_resume = supports_resume
<<<END FAKEPROVIDER-INIT-FROM

<<<BEGIN FAKEPROVIDER-INIT-TO
        malformed_review_recoverable: bool = False,
        supports_resume: bool = False,
        fake_session_id: str = "",
    ) -> None:
        self._builder_files = builder_files or ["docs/README.md"]
        self._supports_resume = supports_resume
        self._fake_session_id = fake_session_id
<<<END FAKEPROVIDER-INIT-TO

<<<BEGIN FAKEPROVIDER-BUILD-FROM
        is_repair = self._build_count > 1
        return BuilderOutput(
            summary=f"{'Repair' if is_repair else 'Initial'} changes (round {self._build_count})",
            files_changed=list(self._builder_files),
            commands_suggested=[],
            assumptions=["Minimal changes only"],
            provider="fake",
            duration_ms=50,
            tokens_used=100,
            prepared_input=prepare_call_input(
                prompt=prompt, model="fake", mode="fake",
                options={"max_output_chars": max_output_chars}),
        )
<<<END FAKEPROVIDER-BUILD-FROM

<<<BEGIN FAKEPROVIDER-BUILD-TO
        is_repair = self._build_count > 1
        # F106 T002a: honor an incoming resume request only when this fake was
        # constructed to support it — an unsupported provider's output is
        # byte-identical whether or not a caller passes ``resume``.
        resume_used = bool(resume) and self._supports_resume
        usage_actuals = (
            {"session_id": self._fake_session_id} if self._fake_session_id else None
        )
        return BuilderOutput(
            summary=f"{'Repair' if is_repair else 'Initial'} changes (round {self._build_count})",
            files_changed=list(self._builder_files),
            commands_suggested=[],
            assumptions=["Minimal changes only"],
            provider="fake",
            duration_ms=50,
            tokens_used=100,
            usage_actuals=usage_actuals,
            resume_used=resume_used,
            resume_session_ref=resume if resume_used else "",
            prepared_input=prepare_call_input(
                prompt=prompt, model="fake", mode="fake",
                options={"max_output_chars": max_output_chars}),
        )
<<<END FAKEPROVIDER-BUILD-TO

<<<BEGIN BUILDER-CALL-FROM
            _begin_stream_call(builder_provider, round_num, "attempt")
            builder_call_reasons: list[str] = []
            builder_out = _call_with_retry(
                lambda ts=builder_timeout: builder_provider.build(
                    builder_prompt,
                    timeout_sec=ts,
                    max_output_chars=max_output_chars,
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
<<<END BUILDER-CALL-FROM

<<<BEGIN BUILDER-CALL-TO
            _begin_stream_call(builder_provider, round_num, "attempt")
            builder_call_reasons: list[str] = []
            # F106 T002a: a repair round resumes the prior round's provider
            # session only when the provider honestly advertises support AND
            # a session id was actually captured last round — every other
            # path (initial round, unsupported provider, no prior session
            # id) passes resume=None, an honest no-op, never guessed.
            builder_resume_ref: str | None = None
            if is_repair and getattr(builder_provider, "supports_resume", False) and result.rounds:
                prev_builder_out = result.rounds[-1].builder_output
                prev_actuals = getattr(prev_builder_out, "usage_actuals", None) or {}
                prev_session_id = str(prev_actuals.get("session_id") or "")
                if prev_session_id:
                    builder_resume_ref = prev_session_id
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
<<<END BUILDER-CALL-TO

<<<BEGIN TESTFILE-DOCSTRING-FROM
"""Tests for the F106 T001 session-resume capability surface.

Covers: every concrete provider (`FakeProvider`, `ClaudeProvider`,
`ClaudeCliProvider`) exposes `supports_resume` and reads `False` by
construction this round; `build`/`review` accept an additive `resume`
keyword on all three without changing behavior; `BuilderOutput`/
`ReviewerOutput` default `resume_used`/`resume_session_ref` to `False`/"".
`ClaudeProvider`/`ClaudeCliProvider` are checked by signature only — no
real call is made, matching tests/orchestration/test_provider_mode.py's
own no-network convention for those two classes.
"""

from __future__ import annotations

import dataclasses
import inspect

from packages.orchestration.pingpong_provider import (
    BuilderOutput,
    ClaudeCliProvider,
    ClaudeProvider,
    FakeProvider,
    ReviewerOutput,
)
<<<END TESTFILE-DOCSTRING-FROM

<<<BEGIN TESTFILE-DOCSTRING-TO
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
<<<END TESTFILE-DOCSTRING-TO

<<<BEGIN TESTFILE-APPEND-FROM
    def test_review_identical_with_and_without_resume(self):
        plain = FakeProvider().review("do the thing")
        resumed = FakeProvider().review("do the thing", resume="some-session-ref")
        for field in dataclasses.fields(plain):
            assert getattr(plain, field.name) == getattr(resumed, field.name), field.name
<<<END TESTFILE-APPEND-FROM

<<<BEGIN TESTFILE-APPEND-TO
    def test_review_identical_with_and_without_resume(self):
        plain = FakeProvider().review("do the thing")
        resumed = FakeProvider().review("do the thing", resume="some-session-ref")
        for field in dataclasses.fields(plain):
            assert getattr(plain, field.name) == getattr(resumed, field.name), field.name


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch):
    """Redirect REMEDY_DATA_DIR to tmp so tests don't write to the real data root."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def demo_repo(tmp_path: Path) -> Path:
    """Minimal demo repo, matching tests/orchestration/test_pingpong.py's own fixture."""
    (tmp_path / "README.md").write_text("# Demo\nA demo project.\n")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "README.md").write_text("# Docs\nDocumentation here.\n")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("def hello():\n    return 'hello'\n")
    (tmp_path / ".env").write_text("API_KEY=secret123\n")
    (tmp_path / ".env.local").write_text("DB_PASSWORD=hunter2\n")
    return tmp_path


class TestT002aBuilderResumeThreading:
    """The repair round's Builder call resumes only when honestly earned."""

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
        assert result.rounds[0].builder_output.resume_used is False
        assert result.rounds[0].builder_output.resume_session_ref == ""
        assert result.rounds[1].builder_output.resume_used is True
        assert result.rounds[1].builder_output.resume_session_ref == "sess-1"

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
        assert all(rd.builder_output.resume_used is False for rd in result.rounds)

    def test_repair_round_does_not_resume_without_a_prior_session_id(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=1, pass_on_round=2, supports_resume=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2,
        )
        assert len(result.rounds) >= 2
        assert all(rd.builder_output.resume_used is False for rd in result.rounds)

    def test_initial_round_never_resumes(self, demo_repo: Path):
        provider = FakeProvider(supports_resume=True, fake_session_id="sess-1")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
        )
        assert result.rounds[0].builder_output.resume_used is False
<<<END TESTFILE-APPEND-TO

## Done when — the gates

Run each gate and report ONE line per gate with its REAL exit code. Every
gate runs at a commit STRICTLY EARLIER than C6, which writes the handback.

G1 TRANSPORT, at C0b. Report the byte length of the committed
   `.agent/authored/f106-r5.md` and `.agent/last_block.md`; state whether
   equal. No expected length stated — the reviewer holds the original.

G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to slice PLAN5 (sha256 of
   both), under 50 lines, holds `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure `.agent/live_review.md`'s
   pre-commit byte length yourself (the reviewer read 1819497 at
   `32eb35c3`); base + `\n` + RECORD5 must equal the committed size. TWO
   readings: (a) whole reconstruction; (b) the committed file's last
   blank-line unit equals RECORD5 exactly (N=1).

G4 THE LEDGER, at C1 and C2. Registered/resolved/open unmoved from
   318/55/263. `DECISION` count 19 at both (line-anchored regex). `Gate:
   F106 R4 — ` 0x before C2, 1x after.

G5 THE CODE — PAIR SHAPE AND ORDERED APPLICATION, at C3-C5. For EACH of
   the five pairs (FAKEPROVIDER-INIT, FAKEPROVIDER-BUILD, BUILDER-CALL,
   TESTFILE-DOCSTRING, TESTFILE-APPEND): run your own containment test
   (`TO contains FROM`) and report the result; then report FROM's
   occurrence count in its target file before its commit and after, and
   TO's occurrence count before and after. For the four REWRITE pairs
   (all but TESTFILE-APPEND), FROM must read 1x→0x and TO 0x→1x. For
   TESTFILE-APPEND (append-shaped — see constraint 12), FROM must read
   1x→1x (it survives as TO's prefix) and TO must read 0x→1x. Then,
   after C3/C4:
   `python3 -c "import ast; ast.parse(open('packages/orchestration/pingpong_provider.py').read())"`
   and the same for `pingpong_loop.py`, both exit 0. After C5:
   `python3 -m ruff check tests/orchestration/test_session_resume.py`
   exits 0.

G6 ZERO BEHAVIOR CHANGE ON THE DEFAULT PATH, at C3/C4. Run
   `python3 -m pytest tests/orchestration/test_pingpong.py
   tests/orchestration/test_provider_mode.py
   tests/orchestration/test_provider_evidence_integration.py -q` — the
   reviewer measured 122 passed at the base; report yours (must be
   unchanged — every existing call site constructs `FakeProvider()` with
   `supports_resume` left at its default `False`).

G7 THE NEW SURFACE, at C5. `python3 -m pytest
   tests/orchestration/test_session_resume.py -q` — report exit code and
   passed count; the reviewer's own count of the file after both pairs
   apply is 16 (the 12 from T001, unchanged, plus 4 new in
   `TestT002aBuilderResumeThreading`) — restate your own exact count rather
   than trusting this one; if it disagrees, report the discrepancy and the
   actual collected count via `python3 -m pytest
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
steps — explicitly note T002a is CLOSED and T002b (Reviewer resume + F111
delta shrink) is next. States `SESSION 2` of F106, round 5. No length cap.
