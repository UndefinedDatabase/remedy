--- STEP R4/F106 — T001c: the dedicated test file, closes T001 ---

Goal: book the round 3 verdict, then write
`tests/orchestration/test_session_resume.py` — the file the feature file's
own Do-not-touch section names as the suggested test path. Covers all
three adapters' `supports_resume` default, the additive `resume` keyword's
signature on every `build`/`review`, the two evidence fields' defaults, and
a zero-behavior-change property test on `FakeProvider`. This closes T001;
T002 (repair-path integration) is the next feature slice, not this round.

Base: `6bef86f19a4e10e40fc61d4dc8b0b715f3ecaffa`, the tip of
`feature/f106-session-resume` after round 3. Same branch, no new branch.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f106-r4.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN4
- C2  append slice RECORD4 (the round 3 verdict) to `.agent/live_review.md`
- C3  write `tests/orchestration/test_session_resume.py` from slice
      TESTFILE1 (new file — no FROM/TO pair, straight write)
- C4  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f106-r4.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    tests/orchestration/test_session_resume.py
    .agent/handoff.md

No file under `packages/`, `apps/` or `docs/` changes this round.
`.agent/prose_slips.md` is NOT touched this round (round 3's slip already
landed).

## Constraints

1. Apply TESTFILE1 and every other slice BYTE FOR BYTE. If one looks
   wrong, apply it as given and DECLARE the problem.
2. C0a/C0b: `shutil.copyfile` from the reviewer's scratch original at
   `.remedy-wt/f106-r4-block.md` for C0a, then from the committed
   `.agent/authored/f106-r4.md` for C0b. Never `cp`, never retype.
3. C1 is the FIRST substantive commit, ahead of C2, per checklist item 23.
4. `.agent/live_review.md` is APPEND-ONLY. C2 appends RECORD4 and revises
   nothing already on disk.
5. NO NEW R-ID IS MINTED and NO DECISION ID IS MINTED. Registered 318 and
   resolved 55 stay UNMOVED (measured at `6bef86f1`); `DECISION` stays 19
   — the reviewer independently re-measured this at round 3's review and
   confirms 19, not round 3's worker-reported 20 (a counting slip in that
   worker's own report, not a ledger defect; see RECORD4). `Gate: F106 R3
   — ` occurs 0x before C2 and exactly 1x after.
6. `.agent/plan.md` stays under 50 lines (AGENTS.md).
7. `tests/orchestration/test_session_resume.py` is a genuinely NEW file —
   confirm with `git ls-tree HEAD -- tests/orchestration/test_session_resume.py`
   returning nothing before C3, and returning a blob after.
8. Every exit code is REAL, from `subprocess.run(...).returncode` in a
   script under the gitignored `.remedy-wt/`. Never through a pipe.
9. G5's mutation red-proof is the only destructive check this round and
   runs in its own disposable worktree, never the primary checkout, which
   satisfies `git status --porcelain` empty at every commit.
10. `remedy` the console script is DENIED in this sandbox; use
    `python3 -m apps.cli.main ...`.
11. Commit subjects: no leading-slash token, no absolute path, no
    secret-like string, no `Co-Authored-By` trailer.
12. Push after C4. Open NO pull request — T001 closes this round but the
    feature (T002, T003) is not done; the PR is created at the feature's
    closure, not here.
13. TESTFILE1 makes NO real network or subprocess call: every
    `ClaudeProvider`/`ClaudeCliProvider` assertion is signature-only
    (`inspect.signature`), never a `.build()`/`.review()` call on those two
    classes, matching round 3's G6(b) precedent. Verify this yourself by
    reading TESTFILE1's own body before applying it.

## Slices

Delimited the same way as prior rounds: content starts the line after
`<<<BEGIN` and ends with the newline before `<<<END`.

<<<BEGIN RECORD4
Gate: F106 R3 — T001b: CLAUDEPROVIDER + CLAUDECLIPROVIDER SURFACE. VERDICT PASS. The reviewer re-ran every gate independently against the real diff `f05c3d61..6bef86f1`, inside a disposable review worktree removed after. G1 TRANSPORT: `.agent/authored/f106-r3.md`/`.agent/last_block.md` both 17246 bytes, byte-equal to the reviewer's own scratch original. G2 THE PLAN: `.agent/plan.md` byte-equal to slice PLAN3, 33 lines. G3 THE RECORD APPEND: base 1813434 + `\n` + RECORD3 (2759 bytes) = 1816194, matching the committed file exactly; whole-reconstruction and paragraph-order readings both `True`; negative control in a disposable worktree (removed after) rejected the flipped byte on both readings, accepted the unflipped one on both. G4 THE LEDGER: 318 registered / 55 resolved / 263 open, unchanged at C1/C2; `Gate: F106 R2 — ` 0x before C2, 1x after; `.agent/prose_slips.md` grew by exactly PROSESLIP3's byte length plus one separator. ONE DISCREPANCY, INVESTIGATED AND RESOLVED: the round 3 worker's own gate report stated the `DECISION` count as 20; the reviewer independently re-measured with a line-anchored `^DECISION F\d+ D\d+ — ` regex at both the round's base (`f05c3d61`) and its HEAD and got 19 at both — UNMOVED, matching every prior round's reading. The file itself is correct; the worker's own count was a measurement slip in its report, not a defect on disk, and is not a finding (no R-id spent; the invariant "unmoved" holds under the reviewer's correct number). G5 THE CODE: all six pairs (CLAUDEPROVIDER-NAME, CLAUDEPROVIDER-BUILD, CLAUDEPROVIDER-REVIEW, CLICLIPROVIDER-NAME, CLICLIPROVIDER-BUILD, CLICLIPROVIDER-REVIEW) independently re-measured — the two NAME pairs append-shaped and checked POSITIONALLY (CLAUDEPROVIDER-NAME-TO at byte offset 12763, strictly between the two class lines; CLICLIPROVIDER-NAME-TO at offset 38580, after `class ClaudeCliProvider:` with no intervening class line) rather than by a bare count, since their TO halves are byte-identical to each other; the other four REWRITE-shaped, FROM 1x→0x and TO 0x→1x for every one; `ast.parse` and the four-class import both exit 0. G6 THE FULL SURFACE: existing suite 122 passed matching base; read-only probe confirmed `.supports_resume` False on fresh `ClaudeProvider()`/`ClaudeCliProvider()` instances and `resume` present with default `None` on both classes' `build`/`review` signatures, with no `.build()`/`.review()` call made on either. G7 STATE READERS/CANARY: 515/52/21/16/42, all matching base. G8 TREE AND LINT: `ruff check` `All checks passed!`; tree clean, no untracked files; every commit's insertions under 500 by `git diff --numstat` (338/0, 191/253, 11/13, 1/1, 2/0, 12/0, 2/0, 55/43 across the round's eight commits — one more than the block's planned seven, see below). ONE DECLARED DEVIATION: an extra commit (`7e35635a`) fixed a trailing-newline bug in the worker's OWN plan.md-rewrite script mid-round, before C2 — not a defect in the block's own slices (PLAN3 byte-equality at HEAD confirms the FINAL state is correct), and honestly declared rather than silently folded into C1. THE ROUND PASSES: the change set matched the block's seven named paths exactly (the eighth commit is the same-path fixup, not a scope addition), tree clean and pushed, no worktree survived.
<<<END RECORD4

<<<BEGIN PLAN4
# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 1, round 4.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F106 claim, branch, shape inventory | done | round 1 |
| T001a: Protocol + evidence fields + FakeProvider | done | round 2 |
| T001b: ClaudeProvider + ClaudeCliProvider, same surface | done | round 3 |
| T001c: `tests/orchestration/test_session_resume.py` | done | this round — T001 CLOSED |
| T002 repair-path integration + delta shrink + expired fallback | open | next session; gated on T001 (done) and F111 (accepted) |
| T003 measured fixture comparison + docs | open | |

## Next Steps
1. T001 is complete: all three adapters share the `supports_resume`/
   `resume`/evidence-field surface, dedicated tests exist and pass, zero
   behavior change proved by property test and by the existing suite.
2. Next session opens T002: thread `resume`/session-id through the repair
   path in `packages/orchestration/pingpong_loop.py`, shrink the repair
   prompt via the existing diff-repair (F111) hunk selection, and
   implement the fallback-once rule verbatim per the Orchestrator brief.
3. T003 (measured fixture comparison + docs) follows T002.

## Risks
- None new. No adapter's `supports_resume` turns True until T002 actually
  wires resume behavior end to end — T001 only builds the honest surface.
<<<END PLAN4

<<<BEGIN TESTFILE1
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


class TestSupportsResumeDefaultsFalse:
    """Every adapter is honestly unsupported until T002 wires one."""

    def test_fake_provider_default_false(self):
        assert FakeProvider().supports_resume is False

    def test_fake_provider_constructor_override(self):
        assert FakeProvider(supports_resume=True).supports_resume is True

    def test_claude_provider_false(self):
        assert ClaudeProvider().supports_resume is False

    def test_claude_cli_provider_false(self):
        assert ClaudeCliProvider().supports_resume is False


class TestResumeParameterIsAdditive:
    """`resume` is accepted everywhere, with a `None` default, real call unmade."""

    def test_fake_provider_build_accepts_resume(self):
        sig = inspect.signature(FakeProvider.build)
        assert "resume" in sig.parameters
        assert sig.parameters["resume"].default is None

    def test_fake_provider_review_accepts_resume(self):
        sig = inspect.signature(FakeProvider.review)
        assert "resume" in sig.parameters
        assert sig.parameters["resume"].default is None

    def test_claude_provider_build_and_review_accept_resume(self):
        for meth in ("build", "review"):
            sig = inspect.signature(getattr(ClaudeProvider, meth))
            assert "resume" in sig.parameters
            assert sig.parameters["resume"].default is None

    def test_claude_cli_provider_build_and_review_accept_resume(self):
        for meth in ("build", "review"):
            sig = inspect.signature(getattr(ClaudeCliProvider, meth))
            assert "resume" in sig.parameters
            assert sig.parameters["resume"].default is None


class TestEvidenceFieldsDefault:
    """`resume_used`/`resume_session_ref` are honest, inert defaults."""

    def test_builder_output_defaults(self):
        out = BuilderOutput()
        assert out.resume_used is False
        assert out.resume_session_ref == ""

    def test_reviewer_output_defaults(self):
        out = ReviewerOutput()
        assert out.resume_used is False
        assert out.resume_session_ref == ""


class TestZeroBehaviorChange:
    """Passing `resume=` to `FakeProvider` changes nothing observable.

    `ClaudeProvider`/`ClaudeCliProvider` are excluded from this class: they
    require real network/CLI access to exercise `build`/`review` at all,
    which is out of scope for this round (their signatures are covered
    above; the behavior-equality property is the same by construction,
    since `resume` is accepted and unused on every adapter this round).
    """

    def test_build_identical_with_and_without_resume(self):
        plain = FakeProvider().build("do the thing")
        resumed = FakeProvider().build("do the thing", resume="some-session-ref")
        for field in dataclasses.fields(plain):
            assert getattr(plain, field.name) == getattr(resumed, field.name), field.name

    def test_review_identical_with_and_without_resume(self):
        plain = FakeProvider().review("do the thing")
        resumed = FakeProvider().review("do the thing", resume="some-session-ref")
        for field in dataclasses.fields(plain):
            assert getattr(plain, field.name) == getattr(resumed, field.name), field.name
<<<END TESTFILE1

## Done when — the gates

Run each gate and report ONE line with its REAL exit code. Every gate runs
at a commit STRICTLY EARLIER than C4, which writes the handback.

G1 TRANSPORT, at C0b. Report the byte length of the committed
   `.agent/authored/f106-r4.md` and `.agent/last_block.md`; state whether
   equal. No expected length stated — the reviewer holds the original.

G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to slice PLAN4 (sha256 of
   both), under 50 lines, holds `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure `.agent/live_review.md`'s
   pre-commit byte length (the reviewer read 1816194 at `6bef86f1`); base +
   `\n` + RECORD4 must equal the committed size. TWO readings: (a) whole
   reconstruction; (b) last blank-line unit equals RECORD4 (N=1). NEGATIVE
   CONTROL in a disposable worktree removed after: one byte flipped inside
   RECORD4 rejected by both readings, unflipped accepted by both.

G4 THE LEDGER, at C1 and C2. Registered/resolved/open unmoved from
   318/55/263. `DECISION` count 19 at both (line-anchored regex — see
   constraint 5's note on round 3's discrepancy). `Gate: F106 R3 — ` 0x
   before C2, 1x after.

G5 THE NEW FILE AND ITS MUTATION RED-PROOF, at C3. Confirm
   `tests/orchestration/test_session_resume.py` is byte-equal to slice
   TESTFILE1 (sha256 of both), and confirm via
   `git ls-tree 6bef86f1 -- tests/orchestration/test_session_resume.py`
   that the path did not exist at the base. Run
   `python3 -m pytest tests/orchestration/test_session_resume.py -q` —
   report exit code and passed count; the reviewer measured 12 passed
   green at dry-run. Then, in a disposable worktree (removed after): (a)
   flip `FakeProvider.__init__`'s `supports_resume: bool = False,` default
   to `True` and confirm `test_fake_provider_default_false` alone goes
   red, nothing else; restore. (b) make `FakeProvider.build` return
   `resume_used=True` whenever `resume` is truthy (a one-line insertion
   right after `self._build_count += 1`) and confirm
   `test_build_identical_with_and_without_resume` alone goes red; restore.
   Report both mutated-red and restored-green readings, with passed/failed
   counts.

G6 EXISTING SUITE UNAFFECTED, at C3. `python3 -m pytest
   tests/orchestration/test_pingpong.py
   tests/orchestration/test_provider_mode.py
   tests/orchestration/test_provider_evidence_integration.py -q` — the
   reviewer measured 122 passed at the base; report yours (must be
   unchanged, this round adds a test file but touches no production code).

G7 THE STATE READERS AND CANARY, after C2. Each its own real exit code:
   `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/orchestration/test_test_runner.py -q`,
   `python3 -m pytest tests/regression/test_resource_safety.py -q`,
   `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`, and
   the canary `python3 -m pytest tests/cli/test_golden_path.py -q`. The
   reviewer measured 515, 52, 21, 16, 42 at the base; report yours.

G8 THE TREE AND LINT, at C3. `python3 -m ruff check
   tests/orchestration/test_session_resume.py` — the reviewer measured
   `All checks passed!` at dry-run; report your exit code and output. `git
   status --porcelain` empty, `git ls-files --others --exclude-standard`
   count 0, every commit's insertions under 500 (`git diff --numstat`).

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: state
block, `## Commits` table with `+/-` from `git diff --numstat`, deviations,
item-status table with every bundle item and every gate exactly once, next
steps — explicitly note T001 is CLOSED and the feature's next slice is
T002. States `SESSION 1` of F106, round 4. No length cap.
