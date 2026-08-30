--- STEP R10/F106 — fix R-0758: resume-kwarg gap in four test providers ---

Goal: book the round 9 verdict, resolve finding R-0758, and land its fix —
four test-only provider subclasses in `tests/orchestration/test_provider_retry.py`
gain an accepted `resume: str | None = None` parameter on the method that
was crashing (`TimeoutOnceFakeProvider.build`, `ReviewerTimeoutOnceFakeProvider.review`,
`NonzeroExitOnceFakeProvider.build`, and the locally-defined
`ParseRetryRateLimitedProvider.review`), so all four stop raising `TypeError`
when `pingpong_loop.py`'s Builder/Reviewer call sites pass `resume=` (every
call, since round 5/6). Small, mechanical, test-only: no production file
changes, no test assertion changes, no new test needed — the fix IS its own
regression proof, since these same 4 tests already exercise the crashing
path through `run_pingpong` and simply pass once the signatures accept the
kwarg. Two reviewer-authored process notes from round 9's own gate wording
(constraint 5 undercounting a self-quoting record; constraint 14 saying
"line" for a 3-line comment) are booked as dated `.agent/prose_slips.md`
lines this round too — neither is a product defect, per amend0827-process-diet
rule 2.

Base: `2a0e08e13ccc5e4c9aaa138e96cf440f09e08a06`, the tip of
`feature/f106-session-resume` after round 9. Same branch, no new branch.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f106-r10.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN10
- C2  append slices RECORD10 and DONER0758 (two paragraphs: the round 9
      verdict, then R-0758's resolution) to `.agent/live_review.md`
- C3  append slices PROSESLIPG4 and PROSESLIPC14 (two paragraphs) to
      `.agent/prose_slips.md`
- C4  apply the four pairs below to
      `tests/orchestration/test_provider_retry.py`
- C5  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f106-r10.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    tests/orchestration/test_provider_retry.py
    .agent/handoff.md

No other file changes this round. No production file under `packages/` or
`apps/` is touched — R-0758 is a test-only defect and its fix is test-only.

## Constraints

1. Apply every slice/pair BYTE FOR BYTE; if one looks wrong, apply it as
   given and DECLARE the problem — never fix, rewrap or improve it.
2. C0a/C0b: `shutil.copyfile` from `.remedy-wt/f106-r10-block.md` for C0a,
   then from the committed `.agent/authored/f106-r10.md` for C0b. Never
   `cp`, never retype. Extract every slice/pair from the COMMITTED
   `.agent/authored/f106-r10.md` via the marker convention (content starts
   the line after `<<<BEGIN`, ends with the newline before `<<<END`).
3. C1 is the FIRST substantive commit, ahead of C2/C3 (checklist item 23).
4. `.agent/live_review.md` is APPEND-ONLY. C2 appends RECORD10, then
   DONER0758, as TWO paragraphs in that order, and revises nothing already
   on disk. `.agent/prose_slips.md` is APPEND-ONLY; C3 appends
   PROSESLIPG4, then PROSESLIPC14, as TWO paragraphs in that order, and
   revises nothing already on disk.
5. ONE FINDING IS RESOLVED THIS ROUND: R-0758 (already registered, round
   9). NO NEW R-ID, NO NEW DECISION IS MINTED. Registered stays UNMOVED at
   319 (measured by the reviewer at `2a0e08e13ccc5e4c9aaa138e96cf440f09e08a06`);
   resolved moves 55→56 (`Done: R-0758 — ` added, distinct-id count);
   `DECISION F\d+ D\d+ — ` stays UNMOVED at 20. `Gate: F106 R9 — ` occurs
   0x before C2 and AT LEAST 1x after (RECORD10's own header; per this
   round's own PROSESLIPG4, a self-quoting record paragraph may read
   higher — do not treat a count above 1 alone as a discrepancy; read the
   ACTUAL text before declaring one).
6. `.agent/plan.md` stays under 50 lines (AGENTS.md).
7. Every exit code is REAL, from `subprocess.run(...).returncode` in a
   script under gitignored `.remedy-wt/` — never through a pipe.
8. All checks this round are read-only against the primary checkout
   (imports, `ast.parse`, pytest runs) — no worktree needed; none of
   G1-G7 below mutates a file outside a script's own transient copy.
9. `remedy` the console script is DENIED in this sandbox; use
   `python3 -m apps.cli.main ...`.
10. Commit subjects: no leading-slash token, no absolute path, no
    secret-like string, no `Co-Authored-By` trailer.
11. Push after C5. Open NO pull request — T002b-ii step 2 and T003 both
    remain open on this feature; R-0758's fix does not close the branch.
12. Pair shapes, measured by the reviewer's own containment test, reported
    here as the result not the method: all FOUR pairs (TIMEOUTONCE-BUILD,
    REVIEWERTIMEOUTONCE-REVIEW, NONZEROEXIT-BUILD, PARSERETRY-REVIEW) read
    `TO contains FROM: false` (REWRITE — each signature gains a new
    parameter and, for the first three, a new forwarded argument in the
    `super()` call, so the FROM text does not survive as a literal
    substring of the TO text). FROM occurs exactly 1x in
    `test_provider_retry.py` before C4 and 0x after, for each of the
    four; TO occurs 0x before and exactly 1x after, for each of the four.
13. After C4, `test_provider_retry.py` must still be valid Python:
    `python3 -c "import ast;
    ast.parse(open('tests/orchestration/test_provider_retry.py').read())"`
    exits 0, and `python3 -m ruff check tests/orchestration/test_provider_retry.py`
    exits 0.
14. The three pairs that forward `resume=resume` to their own `super()`
    call (TIMEOUTONCE-BUILD, REVIEWERTIMEOUTONCE-REVIEW, NONZEROEXIT-BUILD)
    must NOT change any existing test's assertions: none of the three
    classes overrides `supports_resume`, so `FakeProvider.build`/`review`'s
    own `resume_used = bool(resume) and self._supports_resume` stays
    `False` regardless of what `resume` value flows through — G5's
    zero-behavior-change reading (all 30 previously-passing tests in the
    file, unchanged assertions) is how this is proved.
15. `ParseRetryRateLimitedProvider.review` (PARSERETRY-REVIEW) never calls
    `super().review(...)` at all — it always returns one of its own three
    hardcoded `ReviewerOutput`s regardless of any argument — so its pair
    only ADDS the accepted, unused parameter; verify this yourself by
    reading the ~25 lines following the pair's own TO span in the
    committed file before applying it, confirming no `super()` call
    exists inside that method body.

## Pairs

Each pair is FROM/TO, delimited the same way as prior rounds: content
starts the line after `<<<BEGIN` and ends with the newline before `<<<END`.

<<<BEGIN RECORD10
Gate: F106 R9 — T002b-ii STEP 1: HOIST RESUME-REF BEFORE PROMPT BUILD; DECISION F106 D1 REGISTERED; R-0758 DISCOVERED AND REGISTERED. VERDICT PASS. The reviewer independently re-verified round 9's committed diff `1470c3d74133906afc760b7d0a828a4900ae49cf..2a0e08e13ccc5e4c9aaa138e96cf440f09e08a06` against the real files, not the worker's summary. G1 TRANSPORT: `.agent/authored/f106-r9.md` and `.agent/last_block.md` independently sha256'd at `8467a03410b6d4c2d8915a6ddb7a0b8a1eee8e040b5e26feffd91ac4dfcba57c`, both 35918 bytes, matching each other and the reviewer's own held scratch original `.remedy-wt/f106-r9-block.md` — three-way equal. G2 THE PLAN: `.agent/plan.md` independently sha256'd at `7d85b690799285aee85ba63c58e2e1b37e6e043cfe080fe37f0efc120fc4c911`, 41 lines, holding `## Goal` and `## Next Steps`, cross-checked byte-equal against the reviewer's own extracted PLAN9 slice directly. G3 THE RECORD APPEND, a THREE-PARAGRAPH append: independently re-measured — base 1833342 bytes (re-confirmed at `1470c3d7`) + separator + RECORD9 (5274 bytes) + separator + DECISIONF106D1 (7098 bytes) + separator + R0758 (1802 bytes) = 1847519, matching `.agent/live_review.md`'s actual committed length exactly; the committed file's last three blank-line units read byte-identical to the reviewer's own held RECORD9/DECISIONF106D1/R0758 text, in that order; the worker's own negative control (one byte flipped inside RECORD9, run in a disposable worktree, cleanly removed after) was independently re-run by the reviewer too and correctly rejected. G4 THE LEDGER: independently re-measured with substring counting (not `grep -c`, which undercounts a self-quoting single-line record — see the deviation below) — registered moves 318→319 (`R-0758` added), resolved unmoved at 55, `DECISION` moves 19→20 (`DECISION F106 D1` added), matching the block's stated expectations exactly. G5 THE CODE: read directly against the real diff. Both hoisted blocks (`builder_resume_ref`, `reviewer_resume_ref`) moved verbatim from immediately before their own `_call_with_retry(...)` call to immediately before their prompt-composition call site, each carrying exactly one NEW comment (spanning 3 physical lines, naming this round and DECISION F106 D1) — the pre-existing T002a/T002b-i comment, the condition, and the session-id extraction logic all confirmed byte-identical between old and new position by direct substring comparison. All four pairs (BUILDER-HOIST-REMOVE, BUILDER-HOIST-INSERT, REVIEWER-HOIST-REMOVE, REVIEWER-HOIST-INSERT) independently re-measured against the real committed file: FROM 0x, TO 1x post-commit, matching the block's predicted REWRITE shape for all four (containment checked both ways for each, `False`/`False`, confirming neither TO nor FROM is a substring of the other). `packages/orchestration/pingpong_provider.py` and `packages/orchestration/provider_token_evidence.py` confirmed untouched, `git diff --stat` empty for both. `ast.parse`/`ruff check` on `pingpong_loop.py`: exit 0 each. G6 ZERO BEHAVIOR CHANGE (broadened suite): `python3 -m pytest tests/orchestration/test_pingpong.py tests/orchestration/test_provider_mode.py tests/orchestration/test_provider_evidence_integration.py tests/orchestration/test_session_resume.py tests/orchestration/test_builder_prompt_golden.py tests/orchestration/test_builder_prompt_quality.py tests/orchestration/test_builder_prompt_hunk_rejections.py -q` independently re-run, REAL exit 0, 199 passed, matching the block's own stated 122+26+51=199 exactly; `tests/orchestration/test_provider_retry.py` correctly excluded from this gate per the block's own instruction, its 4 pre-existing failures being R-0758, unrelated to this round. G7 THE PROSE SLIP APPEND: independently re-measured — base 34537 bytes + separator + PROSESLIPR8 (509 bytes) = 35047, matching `.agent/prose_slips.md`'s actual committed length exactly; the committed file's last blank-line unit reads byte-identical to the reviewer's own held PROSESLIPR8 text. G8 THE TREE: `git status --porcelain` empty, `git ls-files --others --exclude-standard` 0 untracked; every commit's insertions well under 500 (395/313/16/6/2/33 across the six non-exempt-or-exempt commits, matching the handback's own reading). TWO DECLARED DEVIATIONS, BOTH INDEPENDENTLY VERIFIED AND CONFIRMED NOT DEFECTS. FIRST: the block's constraint 5 predicted `Gate: F106 R8 — ` would read exactly 1x after C2's append; it measures 2x, because RECORD9's own G4 paragraph quotes the phrase a second time inside its self-referential measurement narrative ("`Gate: F106 R8 — ` exactly 0x before this entry") — the reviewer independently confirmed this is a PRE-EXISTING, systemic property of this ledger's format, not new to this round: `Gate: F106 R7 — ` already read 2x in the file BEFORE round 9's own C2 touched it (`git show 1470c3d7:.agent/live_review.md`, substring-counted, not `grep -c`, which reports 1 because both occurrences sit on RECORD8's own single physical line). A dated prose_slip line is owed for this — the reviewer's own gate-writing habit of predicting "1x" for an append-only record's OWN header undercounts by exactly the self-quote every time a RECORD paragraph describes its own G4 reading, and the fix is to phrase such gates as "≥1x, and exactly 1x counting only the header line itself" going forward. SECOND: constraint 14 said "one added comment line each"; the added comment is one coherent note spanning 3 physical lines, not 1 — a wording imprecision, the SUBSTANCE (condition and extraction logic unchanged, only position moved) verified true by direct substring comparison. Neither deviation reflects anything wrong on disk; both are reviewer-authored prose imprecisions in the block's own constraints, per amend0827-process-diet rule 2 booked as dated `.agent/prose_slips.md` lines (this round's own C-something, see the round's own bundle) rather than R-ids or a correction round. THE ROUND PASSES: T002b-ii step 1 CLOSED — the hoist is honest, zero-behavior-change-proven against a broadened 199-test suite, and unblocks step 2's design without landing any of step 2's own risk. DECISION F106 D1 is registered and governs step 2. R-0758 is registered OPEN, a real four-test defect discovered by the round's own extra diligence, unrelated to and unaffected by the round's own change, correctly left unfixed and out of scope this round.
<<<END RECORD10

<<<BEGIN DONER0758
Done: R-0758 — RESOLVED by this round's own C4 commit (ordered per this block's own bundle — the fix has no SHA yet at the time this line is authored, per checklist item 20's R-0524 carve-out for a round's own landed change). `resume: str | None = None` is added to all four affected signatures — `TimeoutOnceFakeProvider.build`, `ReviewerTimeoutOnceFakeProvider.review`, `NonzeroExitOnceFakeProvider.build` (each forwarding `resume=resume` to its own `super().build`/`review` call, an honest no-op since none of the three overrides `supports_resume`), and the locally-defined `ParseRetryRateLimitedProvider.review` (accepted and unused, since that class never delegates to `super()` and always returns one of its three hardcoded responses regardless of any argument). VERIFIED: `python3 -m pytest tests/orchestration/test_provider_retry.py -q` reads `34 passed`, the same 30 that passed before plus the 4 R-0758 named, zero new failures.
<<<END DONER0758

<<<BEGIN PLAN10
# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 3, round 10.

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
| T002c (i+ii): fallback-once, both sides | done | rounds 7-8 |
| T002b-ii step 1: hoist resume-ref before prompt build | done | round 9 |
| R-0758: fix `test_provider_retry.py`'s `resume`-kwarg gap | done | this round |
| T002b-ii step 2: the actual delta-prompt shrink | open | next |
| T003: measured fixture comparison + docs | open | |

## Next Steps
1. T002b-ii step 2: per DECISION F106 D1, reuse `parse_diff_line_ranges`/
   `select_repair_hunks` gated on the hoisted resume-ref to shrink the
   repair-diff prompt segment when a session is being resumed; invent and
   freeze a hunk-rendering convention (none exists to borrow); reconcile
   against the prompt-golden test files only if their segment set changes.
2. T003 follows once T002 is fully closed (after T002b-ii step 2 lands).

## Risks
- No adapter's `supports_resume` is true in production yet — only
  `FakeProvider`, via its test-only constructor overrides, ever resumes
  or fails a resume. This round's fix touches only four test-only
  provider subclasses in `test_provider_retry.py`, adding an accepted,
  honestly-forwarded `resume` kwarg that changes no test's assertions.
- DECISION F106 D1's D1-compatibility reading (reusing F111's pure hunk
  functions for prompt content, never the diff-apply channel) governs
  step 2's design; step 2 must not widen it further without a new DECISION.
<<<END PLAN10

<<<BEGIN PROSESLIPG4
2026-08-30 · F106 R9 · The block's constraint 5 predicted `Gate: F106 R8 — ` would read exactly 1x after C2's append; the worker measured 2x and the reviewer independently confirmed it — RECORD9's own G4 paragraph quotes the phrase a second time while describing what it measured, and this is a PRE-EXISTING, systemic property of this ledger's format (RECORD8 already read `Gate: F106 R7 — ` 2x before round 9 touched the file, `git show`-confirmed), not a defect this round introduced. A gate over a RECORD paragraph's own header must read "≥1x, exactly 1x counting only the header line" rather than a bare "1x", because every such paragraph's own G4 description quotes the previous round's header by name. Reviewer-prose inaccuracy, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
<<<END PROSESLIPG4

<<<BEGIN PROSESLIPC14
2026-08-30 · F106 R9 · The block's constraint 14 said each hoisted block carries "one added comment line"; the worker measured the added comment as one coherent note spanning 3 physical lines, not 1, and declared the discrepancy while confirming the SUBSTANCE (condition and session-id extraction logic byte-identical, only position moved) held exactly as stated. "Line" should have read "comment" or "note" — a wording imprecision, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
<<<END PROSESLIPC14

<<<BEGIN TIMEOUTONCE-BUILD-FROM
    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> BuilderOutput:
        self._build_attempts += 1
        if self._build_attempts == 1:
            return BuilderOutput(
                error="provider_error: TimeoutExpired: timed out after 120s",
                provider="fake",
            )
        return super().build(prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars)
<<<END TIMEOUTONCE-BUILD-FROM

<<<BEGIN TIMEOUTONCE-BUILD-TO
    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> BuilderOutput:
        self._build_attempts += 1
        if self._build_attempts == 1:
            return BuilderOutput(
                error="provider_error: TimeoutExpired: timed out after 120s",
                provider="fake",
            )
        return super().build(prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars, resume=resume)
<<<END TIMEOUTONCE-BUILD-TO

<<<BEGIN REVIEWERTIMEOUTONCE-REVIEW-FROM
    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> ReviewerOutput:
        self._review_attempts += 1
        if self._review_attempts == 1:
            return ReviewerOutput(
                error="provider_error: TimeoutExpired: reviewer timed out",
                provider="fake",
            )
        return super().review(prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars)
<<<END REVIEWERTIMEOUTONCE-REVIEW-FROM

<<<BEGIN REVIEWERTIMEOUTONCE-REVIEW-TO
    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> ReviewerOutput:
        self._review_attempts += 1
        if self._review_attempts == 1:
            return ReviewerOutput(
                error="provider_error: TimeoutExpired: reviewer timed out",
                provider="fake",
            )
        return super().review(prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars, resume=resume)
<<<END REVIEWERTIMEOUTONCE-REVIEW-TO

<<<BEGIN NONZEROEXIT-BUILD-FROM
    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> BuilderOutput:
        self._build_attempts += 1
        if self._build_attempts == 1:
            return BuilderOutput(
                error="provider_error: RuntimeError: claude CLI exited 1: internal error",
                provider="fake",
            )
        return super().build(prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars)
<<<END NONZEROEXIT-BUILD-FROM

<<<BEGIN NONZEROEXIT-BUILD-TO
    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> BuilderOutput:
        self._build_attempts += 1
        if self._build_attempts == 1:
            return BuilderOutput(
                error="provider_error: RuntimeError: claude CLI exited 1: internal error",
                provider="fake",
            )
        return super().build(prompt, timeout_sec=timeout_sec, max_output_chars=max_output_chars, resume=resume)
<<<END NONZEROEXIT-BUILD-TO

<<<BEGIN PARSERETRY-REVIEW-FROM
            def review(
                self,
                prompt: str,
                *,
                timeout_sec: int = 120,
                max_output_chars: int = 50000,
            ) -> ReviewerOutput:
                self.review_calls += 1
<<<END PARSERETRY-REVIEW-FROM

<<<BEGIN PARSERETRY-REVIEW-TO
            def review(
                self,
                prompt: str,
                *,
                timeout_sec: int = 120,
                max_output_chars: int = 50000,
                resume: str | None = None,
            ) -> ReviewerOutput:
                self.review_calls += 1
<<<END PARSERETRY-REVIEW-TO

## Done when — the gates

Report ONE line per gate with its REAL exit code; every gate runs strictly before C5, which writes the handback.

G1 TRANSPORT, at C0b. Report the byte length of `.agent/authored/f106-r10.md`
   and `.agent/last_block.md`; state whether equal (reviewer holds the original).

G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to slice PLAN10 (sha256 of
   both), under 50 lines, holds `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2 — a TWO-PARAGRAPH append. Re-measure the
   pre-commit byte length yourself (reviewer read 1847519 at `2a0e08e1`);
   base + `\n` + RECORD10 + `\n` + DONER0758 must equal the committed
   size. THREE readings: (a) whole reconstruction; (b) the committed
   file's LAST TWO blank-line units equal RECORD10 then DONER0758, in
   that order; (c) a negative control in a disposable worktree — one byte
   flipped inside RECORD10 (the FIRST appended paragraph) must be
   REJECTED by reading (b). Remove the worktree after.

G4 THE LEDGER, at C1 and C2. Registered unmoved at 319. Resolved moves
   55→56 (`Done: R-0758 — ` added, distinct-id count). `DECISION F\d+
   D\d+ — ` unmoved at 20. `Gate: F106 R9 — ` 0x before C2; read the
   ACTUAL count after (may exceed 1x if RECORD10 quotes its own header —
   see constraint 5) and report it plainly rather than forcing it to 1.

G5 THE CODE — PAIR SHAPE AND ORDERED APPLICATION, at C4. For EACH of the
   four pairs (TIMEOUTONCE-BUILD, REVIEWERTIMEOUTONCE-REVIEW,
   NONZEROEXIT-BUILD, PARSERETRY-REVIEW): run your own containment test
   and report FROM's/TO's occurrence counts before/after C4. All four:
   FROM 1x→0x, TO 0x→1x. After C4: `python3 -c "import ast;
   ast.parse(open('tests/orchestration/test_provider_retry.py').read())"`
   exits 0; `python3 -m ruff check tests/orchestration/test_provider_retry.py`
   exits 0.

G6 THE FIX ITSELF AND ZERO BEHAVIOR CHANGE, at C4. `python3 -m pytest
   tests/orchestration/test_provider_retry.py -q` — reviewer measured `34
   passed` after the dry-run fix (the 30 that already passed, unchanged,
   plus the 4 R-0758 named); report your own exact count and, if it
   disagrees, the full failure output before ruling.

G7 THE PROSE SLIP APPEND, at C3 — a TWO-PARAGRAPH append. Re-measure the
   pre-commit byte length yourself (reviewer read 35047); base + `\n` +
   PROSESLIPG4 + `\n` + PROSESLIPC14 must equal the committed size; the
   committed file's last two blank-line units equal PROSESLIPG4 then
   PROSESLIPC14, in that order.

G8 THE TREE, at C4 (checked again before C5, which necessarily dirties
   the tree until its own commit). `git status --porcelain` empty, `git
   ls-files --others --exclude-standard` count 0, every commit's
   insertions under 500 (`git diff --numstat`).

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: state
block, `## Commits` table (`+/-` from `git diff --numstat`), deviations,
item-status table with every bundle item and gate exactly once, next
steps — R-0758 CLOSED, T002b-ii step 2 (the actual shrink, governed by
DECISION F106 D1) and T003 both remaining. States `SESSION 3` of F106,
round 10. No length cap.
