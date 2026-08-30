--- STEP R9/F106 — T002b-ii step 1: hoist resume-ref before prompt build ---

Goal: book the round 8 verdict, register DECISION F106 D1 (the delta-prompt
shrink's design, split into two rounds), and land ONLY the safe half this
round: `builder_resume_ref`/`reviewer_resume_ref` — both currently computed
immediately before their own `_call_with_retry(...)` call, well AFTER
`builder_composed`/`reviewer_composed` are already built — are HOISTED to
just before their prompt-composition call sites, so a LATER round can gate
the repair-diff prompt segment on the same value without recomputing it.
Same inputs (`is_repair`, `getattr(provider, "supports_resume", False)`,
`result.rounds`), same value, computed earlier only — nothing between the
old and new computation points reads or mutates any of those three inputs,
so this is byte-for-byte behavior-preserving. NO NEW PROMPT CONTENT, NO NEW
TEST, NO NEW BEHAVIOR lands this round: the round's own dry run (reviewer,
pre-delegation, disposable worktree) re-ran the full existing
`test_pingpong.py`/`test_provider_mode.py`/`test_provider_evidence_integration.py`/
`test_session_resume.py`/`test_builder_prompt_golden.py`/
`test_builder_prompt_quality.py`/`test_builder_prompt_hunk_rejections.py`
suites against the hoisted code and all passed unchanged. DECISION F106 D1
(full text in the pairs below) records why the ACTUAL delta-prompt shrink —
reusing `packages/orchestration/diff_repair.py`'s `select_repair_hunks` and
`packages/orchestration/review_scope.py`'s `parse_diff_line_ranges`, gated on
the hoisted resume-ref — is NOT this round's work: no renderer for a
`RepairHunk` selection into prompt text exists anywhere in the repository to
reuse, and inventing one in the same round as this loop restructuring would
compound two novel risks into one change set. THE REVIEWER'S OWN DRY RUN ALSO
FOUND A REAL, PRE-EXISTING DEFECT, UNRELATED TO THIS ROUND'S OWN CHANGE: four
test-only provider subclasses in `tests/orchestration/test_provider_retry.py`
do not accept the `resume` keyword the Builder/Reviewer call sites have
passed unconditionally since rounds 5-6, so `test_provider_retry.py` reads
`4 failed, 30 passed` on the CURRENT HEAD, before this round's own edit —
registered this round as R-0758, NOT fixed this round (out of scope; a
change to `test_provider_retry.py`, not to the hoisted lines). A
session-numbering correction (round 8's handback should have read SESSION 3,
not SESSION 2 — this session began after round 7's SESSION 2 ended) is
booked as one dated line
in `.agent/prose_slips.md`, not an R-id, per amend0827-process-diet rule 2.

Base: `1470c3d74133906afc760b7d0a828a4900ae49cf`, the tip of
`feature/f106-session-resume` after round 8. Same branch, no new branch.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f106-r9.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN9
- C2  append slices RECORD9, DECISIONF106D1 and R0758 (three paragraphs: the
      round 8 verdict, the new DECISION, the new finding) to
      `.agent/live_review.md`
- C3  append slice PROSESLIPR8 to `.agent/prose_slips.md`
- C4  apply the four pairs below to `packages/orchestration/pingpong_loop.py`
- C5  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f106-r9.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    packages/orchestration/pingpong_loop.py
    .agent/handoff.md

No other file changes this round. `packages/orchestration/pingpong_provider.py`
and `packages/orchestration/provider_token_evidence.py` are NOT touched, and
neither is any test file — the four pairs below are the round's entire code
change, and every existing test that already covers the touched lines is the
round's own zero-behavior-change proof.

## Constraints

1. Apply every slice/pair BYTE FOR BYTE; if one looks wrong, apply it as
   given and DECLARE the problem — never fix, rewrap or improve it.
2. C0a/C0b: `shutil.copyfile` from `.remedy-wt/f106-r9-block.md` for C0a,
   then from the committed `.agent/authored/f106-r9.md` for C0b. Never
   `cp`, never retype. Extract every slice/pair from the COMMITTED
   `.agent/authored/f106-r9.md` via the marker convention (content starts
   the line after `<<<BEGIN`, ends with the newline before `<<<END`).
3. C1 is the FIRST substantive commit, ahead of C2/C3 (checklist item 23).
4. `.agent/live_review.md` is APPEND-ONLY. C2 appends RECORD9, then
   DECISIONF106D1, then R0758, as THREE paragraphs in that order, and
   revises nothing already on disk. `.agent/prose_slips.md` is
   APPEND-ONLY; C3 appends PROSESLIPR8 and revises nothing already on disk.
5. TWO THINGS ARE MINTED THIS ROUND, BOTH FOR THE FIRST TIME ON THIS
   FEATURE: DECISION F106 D1, and finding R-0758 (searched against the
   open set first — no existing finding names `test_provider_retry.py`'s
   `resume`-kwarg gap; the DEFECT, not merely the id, was searched per
   checklist item 30). Resolved stays UNMOVED at 55 (measured by the
   reviewer at `1470c3d74133906afc760b7d0a828a4900ae49cf`). Registered
   moves 318→319 (R-0758 added). `DECISION F\d+ D\d+ — ` moves 19→20 (the
   new F106 D1 line). `Gate: F106 R8 — ` occurs 0x before C2, 1x after —
   RECORD9's own header, not a new finding.
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
11. Push after C5. Open NO pull request — this round closes only step 1 of
    T002b-ii; step 2 (the actual shrink) and T003 both remain open.
12. Pair shapes, measured by the reviewer's own containment test, reported
    here as the result not the method: all FOUR pairs (BUILDER-HOIST-REMOVE,
    BUILDER-HOIST-INSERT, REVIEWER-HOIST-REMOVE, REVIEWER-HOIST-INSERT) read
    `TO contains FROM: false` AND `FROM contains TO: false` (REWRITE — each
    TO is neither a prefix nor a suffix of its own FROM, confirmed
    mechanically rather than assumed, since a short TO that happens to be a
    literal substring of a longer FROM would make the occurrence-count gate
    below unattainable — this is exactly what the first draft of the
    REVIEWER pair got wrong before this block was emitted, caught by
    running the containment test both ways). FROM occurs exactly 1x in
    `pingpong_loop.py` before C4 and 0x after, for each of the four; TO
    occurs 0x before and exactly 1x after, for each of the four. Report all
    four readings, each measured both ways (`TO in FROM` and `FROM in TO`).
13. After C4, `pingpong_loop.py` must still be valid Python: `python3 -c
    "import ast; ast.parse(open('packages/orchestration/pingpong_loop.py').read())"`
    exits 0, and `python3 -m ruff check packages/orchestration/pingpong_loop.py`
    exits 0.
14. The hoisted `builder_resume_ref`/`reviewer_resume_ref` blocks are
    BYTE-IDENTICAL to their pre-hoist selves except for one added comment
    line each (naming this round and DECISION F106 D1) — verify this by
    reading the pair's TO text against its own FROM's corresponding
    fragment; the CONDITION (`is_repair and getattr(provider,
    "supports_resume", False) and result.rounds`) and the session-id
    extraction are unchanged, only their POSITION in the function moves.
15. Before C4, confirm `packages/orchestration/pingpong_provider.py` and
    `packages/orchestration/provider_token_evidence.py` are UNCHANGED —
    `git diff --stat` for both must show nothing, both before and after C4.
16. G6's zero-behavior-change suite is BROADER than prior T002 rounds on
    purpose: this round restructures control flow rather than only adding
    to it, so every existing test file that reaches either hoisted block
    (directly or via the prompt composers) runs, not just the usual
    three-file subset.

## Pairs

Each pair is FROM/TO, delimited the same way as prior rounds: content
starts the line after `<<<BEGIN` and ends with the newline before `<<<END`.

<<<BEGIN RECORD9
Gate: F106 R8 — T002c-ii: REVIEWER FALLBACK-ONCE ON A FAILED RESUME. VERDICT PASS. The reviewer independently re-verified round 8's committed diff `2a17ee639be5f8cc4319e57f4dd1b7e0d7e85fe9..1470c3d74133906afc760b7d0a828a4900ae49cf` against the real files, not the worker's summary. G1 TRANSPORT: `.agent/authored/f106-r8.md` and `.agent/last_block.md` independently sha256'd at `4d9f218082307c01402af19a9f61c0ccbb6a78aa666910e96feeed5eff112689`, both 24283 bytes, matching each other and the reviewer's own held scratch original `.remedy-wt/f106-r8-block.md` — three-way equal. G2 THE PLAN: `.agent/plan.md` independently sha256'd at `26f9dda00b7962ffc231b9f5e13fe1803bc012f467d494192319dd816b6acb1f`, 36 lines, holding `## Goal` and `## Next Steps`, cross-checked byte-equal against the reviewer's own extracted PLAN8 slice directly. G3 THE RECORD APPEND: independently re-measured — base 1828730 bytes (re-confirmed at `2a17ee63`) + separator + RECORD8 (4611 bytes) = 1833342, matching `.agent/live_review.md`'s actual committed length exactly; the committed file's final 4611 bytes read byte-identical to the reviewer's own held RECORD8 text. G4 THE LEDGER: independently re-measured with the same line-anchored regexes — registered 318, resolved 55 (distinct `Done:` ids; raw `Done:` line count 57, the known `R-0721`/`R-0725` double-`Done:` wrinkle carried since round 5), `DECISION` 19, all unmoved from round 7; `Gate: F106 R7 — ` exactly 1x, `Gate: F106 R8 — ` exactly 0x before this entry. G5 THE CODE: read directly against the real diff. `ReviewerOutput` gains `resume_fallback: bool = False`, mirroring `BuilderOutput`'s round-7 field with a distinguishing comment (confirmed NOT byte-identical to `BuilderOutput`'s own comment, so the two fields' occurrence counts never collide). `FakeProvider.review` gains an early-return branch — `if resume and self._supports_resume and self._resume_fails:` returns `ReviewerOutput(error="resume_lost: session context unavailable", provider="fake")` — unreachable on every existing call site by the same default-`False` argument as the Builder side. The Reviewer call site in `pingpong_loop.py` gains a fallback-once branch immediately after the primary `_call_with_retry(...)` call, structurally parallel to it (only `resume=reviewer_resume_ref` → `resume=None` and a reset `reviewer_call_reasons` differ, confirmed by direct comparison of both calls), confirmed the ONLY hunk in that file's diff — the Builder call site (round 7's own fallback) and the bounded parse-retry call site read byte-identical to their base state. `packages/orchestration/provider_token_evidence.py` confirmed untouched, `git diff --stat` empty. All six pairs (REVIEWEROUTPUT-FIELD, FAKEPROVIDER-REVIEW-EARLYFAIL, REVIEWER-CALL-FALLBACK, TESTFILE-DOCSTRING-HEADER, TESTFILE-DOCSTRING-T002C rewrite-shaped; TESTFILE-APPEND append-shaped) independently re-measured against the real committed files at base and HEAD, matching the block's own predicted shape and occurrence counts exactly (five FROM 1x→0x/TO 0x→1x, one FROM 1x→1x/TO 0x→1x). `ruff check` on all three touched files: exit 0, `All checks passed!`. G6 ZERO BEHAVIOR CHANGE: `python3 -m pytest tests/orchestration/test_pingpong.py tests/orchestration/test_provider_mode.py tests/orchestration/test_provider_evidence_integration.py -q` independently re-run, REAL exit 0, 122 passed, matching base exactly. G7 THE NEW SURFACE: `python3 -m pytest tests/orchestration/test_session_resume.py -q` independently re-run, REAL exit 0, 26 passed, matching the handback's stated count exactly (23 carried in, 3 new in `TestT002cReviewerFallbackOnce`), read directly and confirmed correctly gated on `reviewer_resume_ref` having actually been set. G8 STATE READERS/CANARY/TREE: independently re-run, REAL exit 0 each — `tests/ui_server/` 515, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16, canary `tests/cli/test_golden_path.py` 42, all matching base exactly; `git status --porcelain` empty, `git ls-files --others --exclude-standard` 0 untracked, every commit's insertions well under 500. ONE DECLARED DEVIATION, ASSESSED AND CONFIRMED NOT A DEFECT: the handback's own Deviations section flagged that C0b's `git commit`-time auto-printed summary (400 insertions/600 deletions) disagreed with `git diff --numstat`/`git log --stat` on the same commit (216/416) — independently re-confirmed both readings are real (`git diff --numstat 3034a63a^..3034a63a` reads `216 416`), both are far under the 500-line cap, the commit is separately exempt as a verbatim `.agent/**` state-file rewrite, and G1's independent sha256 equality confirms the committed bytes are correct regardless of which diffstat reading is used — a presentation difference between git's porcelain commit summary and a plain `--numstat` invocation on a full-file rewrite, not a product defect; booked to `.agent/prose_slips.md`, no R-id spent. THE ROUND PASSES: T002c-ii CLOSED — the Reviewer side of the fallback-once rule is honest, tested, and zero-behavior-change-proven, mirroring T002c-i exactly. With both halves landed, T002c (the Orchestrator brief's fallback-once rule) is now CLOSED in full.
<<<END RECORD9

<<<BEGIN DECISIONF106D1
DECISION F106 D1 — THE DELTA-PROMPT SHRINK REUSES F111'S PURE HUNK-SELECTION FUNCTIONS FOR PROMPT CONTENT ONLY, NEVER THE DIFF-APPLY CHANNEL; THIS ROUND LANDS ONLY THE SAFE PREP HOIST, NOT THE SHRINK ITSELF. THE PROBLEM: T002b-ii's own line in the feature file (docs/roadmap/features/T2_F106.md Design section) says a repair round should "send resume reference + findings delta (the diff-repair prompt without the re-shown regions the session already contains — the hunk selection shrinks accordingly)", naming F111's hunk selection as the mechanism, but research this round surfaced three real complications. (1) DECISION F111 D1 (docs/roadmap/features/T2_F111.md:74-89) explicitly scoped F111's diff channel to the bounded repair loop in `packages/orchestration/builder_bridge.py`, ruling `pingpong_loop.py` OUT because "no applicator is invoked there" and "giving it a diff-shaped response would require a new provider contract" — T002b-ii must not silently widen that boundary. (2) `packages/orchestration/diff_repair.py`'s `select_repair_hunks`/`parse_diff_line_ranges` (the latter actually lives in `packages/orchestration/review_scope.py:139` and reads a raw multi-file unified-diff STRING directly, so `diff_repair.py`'s `changed_line_ranges_from_patch`/`StructuredPatch` wrapping is unnecessary for pingpong's call shape) ARE pure functions with no dependency on the applicator — they take a repo root plus line ranges and return `RepairHunk(path, start_line, end_line, text)` tuples of raw SOURCE TEXT, never a diff-apply object — so they CAN be reused for prompt-content purposes without touching D1's actual concern. But (3) no renderer turning a `RepairHunkSelection` into prompt markdown exists ANYWHERE in the repository, not even in `builder_bridge.py`'s own home turf: `repair_ctx["diff_hunks"]` is written as raw metadata at `builder_bridge.py:374-383` and a repo-wide grep for `diff_hunks` outside test files shows it is never consumed or rendered into prompt text by any module. This round would have had to invent that convention from nothing, in the SAME round that also restructures the loop's control flow — exactly the compounded-risk shape docs/agents/self_drive_protocol.md guardrail G8 and docs/agents/planner_reviewer_prompt.md §3's pre-emission checklist exist to keep out of one change set. CHOSEN, three parts. (a) THE SHRINK'S IMPLEMENTATION IS SPLIT INTO TWO ROUNDS. This round (F106 R9) lands only a pure, zero-behavior-change prep step: `builder_resume_ref` and `reviewer_resume_ref` — both computed immediately before their respective `_call_with_retry(...)` calls at this round's base, well AFTER `builder_composed`/`reviewer_composed` are already built — are HOISTED to before their prompt-composition call sites, with the original call sites updated to reference the hoisted variable. Same inputs (`is_repair`, `getattr(provider, "supports_resume", False)`, `result.rounds`), same value, computed earlier only; nothing between the old and new computation points reads or mutates any of those three inputs, and the full existing `pingpong_loop.py`/`test_session_resume.py`/prompt-golden test suites were run green against the hoisted code before this round was ever delegated. (b) A LATER round (T002b-ii step 2, not yet designed) will consume the hoisted resume-ref to conditionally replace the full-diff prompt segment with a hunk-selected rendering — via `parse_diff_line_ranges(repair_diff)` feeding `select_repair_hunks(repo_root, ranges, margin_lines=..., max_total_chars=...)` — ONLY when the hoisted resume-ref is set (a resume will actually be attempted this round); the non-resume path keeps sending the full diff exactly as today, unconditionally. That round must also design and freeze a NEW rendering convention for `RepairHunk` results, since none exists to borrow, and must confirm whether `test_builder_prompt_golden.py`/`test_builder_prompt_quality.py`/`test_builder_prompt_hunk_rejections.py` need updating — NOT required for this round's hoist alone, confirmed by this round's own green run of all three, since the hoist changes no argument passed to `compose_builder_prompt`/`compose_reviewer_prompt`. (c) THE REUSE OF `select_repair_hunks`/`parse_diff_line_ranges` FOR PROMPT-CONTENT SHRINKING INSIDE `pingpong_loop.py` IS DECLARED COMPATIBLE WITH DECISION F111 D1: D1's stated concern is the DIFF-APPLY / response-schema channel — a concern about what the BUILDER SENDS BACK and how it gets applied — not about what CONTEXT TEXT the prompt SHOWS the builder going in. Reusing the pure selection functions to shrink outbound prompt text invokes neither the applicator nor any diff-shaped response contract, so it does not cross D1's boundary; this reading is recorded here, loud and reversible, rather than assumed silently. ALTERNATIVES CONSIDERED: (a) implement the full shrink — hoist, hunk-selection, a new renderer, and golden-test reconciliation — in this single round; rejected, because three genuinely novel, compounding design decisions (loop restructuring, an unprecedented rendering format, and a D1-boundary interpretation) in one round is exactly the risk profile the pre-emission checklist and G8 exist to keep out of a single change set, and splitting lets the hoist be verified in isolation with an airtight zero-behavior-change gate before any new rendering convention is invented. (b) defer T002b-ii entirely and move straight to T003; rejected, because T003 explicitly "follows once T002 is fully closed" per the feature file's own Task slicing and T002b-ii is the one open T002 item, so skipping it leaves T002 permanently open with no plan to close it. (c) route the shrink through `builder_bridge.py`'s existing `_attach_diff_repair_hunks`/`repair_context.py` machinery instead of reusing the bare functions directly inside `pingpong_loop.py`; rejected, because that machinery is coupled to the bounded repair loop's OWN control flow (`repair_ctx`, a `StructuredPatch`, `run_builder_bridge_loop`'s cycle), which `pingpong_loop.py` does not have and D1 explicitly did not extend there — calling the two pure functions directly, with no other `builder_bridge.py`/`repair_context.py` coupling, is the narrower and D1-consistent reuse. HOW TO REVERSE: this round's hoist is reversible by moving the two `*_resume_ref` blocks back to their original positions immediately before their `_call_with_retry(...)` calls — a pure, independent, mechanical un-hoist touching no other feature's code. The (c) D1-compatibility reading is reversible by a future round choosing not to build the shrink at all, or by building it exclusively inside `builder_bridge.py`/`repair_context.py` instead, should the operator judge the D1 boundary should hold more strictly than this decision reads it. WHAT IT COSTS TO BE WRONG: if the (c) reading is later judged too permissive, only the NEXT round's shrink implementation is affected — this round's hoist is behavior-neutral and stands regardless of which way that judgment goes, since no code lands this round that depends on the reading being correct.
<<<END DECISIONF106D1

<<<BEGIN R0758
- R-0758 — Medium — four test-only provider subclasses in `tests/orchestration/test_provider_retry.py` do not accept the `resume` keyword `packages/orchestration/pingpong_loop.py`'s Builder and Reviewer call sites have passed unconditionally since round 5 (F106 T002a) and round 6 (T002b-i): `TimeoutOnceFakeProvider.build()` (:50), `ReviewerTimeoutOnceFakeProvider.review()` (:73), `NonzeroExitOnceFakeProvider.build()` (:96), and the locally-defined `ParseRetryRateLimitedProvider.review()` (:730) inside `TestRateGovernorSeam.test_parse_retry_rate_limit_is_paced_end_to_end`. Measured directly: `python3 -m pytest tests/orchestration/test_provider_retry.py -q` reads `4 failed, 30 passed`, all four failures the identical `TypeError: ...() got an unexpected keyword argument 'resume'`, reproduced against the CURRENT HEAD (`1470c3d74133906afc760b7d0a828a4900ae49cf`) and independently reproduced against this round's own pre-hoist base too — this round's hoist changes nothing about which kwargs are passed, only when the value is computed, so it neither causes nor fixes any of the four. Discovered this round only because the reviewer ran the FULL `tests/orchestration/` suite as an extra zero-behavior-change check for the loop-restructuring hoist (constraint 16 of this round's block); none of T002's round gates (the recurring three/four-file subset, nor the state-reader/canary tier) include `test_provider_retry.py`, so these four tests have been silently red since round 5 (three rounds) or round 6 (the fourth, the Reviewer-side one). Fix: add `resume: str | None = None` to each of the four signatures as an honest, ignored no-op — the same additive-parameter shape `FakeProvider.build`/`review` themselves already use for every caller that does not opt into `resume_fails`. OPEN.
<<<END R0758

<<<BEGIN PLAN9
# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 3, round 9.

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
| T002b-ii step 1: hoist resume-ref before prompt build | done | this round |
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
  or fails a resume. This round's hoist changes no observable behavior on
  any path: the resume-ref value, its inputs and the commit order they
  are read in are unchanged, only computed earlier in the same function.
- DECISION F106 D1's D1-compatibility reading (reusing F111's pure hunk
  functions for prompt content, never the diff-apply channel) governs
  step 2's design; step 2 must not widen it further without a new DECISION.
<<<END PLAN9

<<<BEGIN PROSESLIPR8
2026-08-30 · F106 R8 · Round 8's own `.agent/plan.md`/`.agent/handoff.md` stated SESSION 2, carried forward unchanged from round 7's handback; round 7's SESSION 2 (rounds 5-7) had already ended when this new session began (a fresh session with no memory of round 7's authoring), so round 8 should have read SESSION 3 — this feature's first missed session-number increment. Corrected starting at round 9; nothing on disk under packages/apps/tests/docs is wrong, so no R-id (amend0827-process-diet rule 2).
<<<END PROSESLIPR8

<<<BEGIN BUILDER-HOIST-REMOVE-FROM
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
<<<END BUILDER-HOIST-REMOVE-FROM

<<<BEGIN BUILDER-HOIST-REMOVE-TO
            _begin_stream_call(builder_provider, round_num, "attempt")
            builder_call_reasons: list[str] = []
            builder_out = _call_with_retry(
<<<END BUILDER-HOIST-REMOVE-TO

<<<BEGIN BUILDER-HOIST-INSERT-FROM
            )

            # --- Builder phase ---
            # Compute repair diff for builder (from previous round)
            repair_diff = ""
<<<END BUILDER-HOIST-INSERT-FROM

<<<BEGIN BUILDER-HOIST-INSERT-TO
            )

            # F106 T002a: a repair round resumes the prior round's provider
            # session only when the provider honestly advertises support AND
            # a session id was actually captured last round — every other
            # path (initial round, unsupported provider, no prior session
            # id) passes resume=None, an honest no-op, never guessed.
            # F106 T002b-ii step 1 (DECISION F106 D1): hoisted here, before
            # prompt composition, so a later round can gate the repair-diff
            # segment on this same value without recomputing it.
            builder_resume_ref: str | None = None
            if is_repair and getattr(builder_provider, "supports_resume", False) and result.rounds:
                prev_builder_out = result.rounds[-1].builder_output
                prev_actuals = getattr(prev_builder_out, "usage_actuals", None) or {}
                prev_session_id = str(prev_actuals.get("session_id") or "")
                if prev_session_id:
                    builder_resume_ref = prev_session_id

            # --- Builder phase ---
            # Compute repair diff for builder (from previous round)
            repair_diff = ""
<<<END BUILDER-HOIST-INSERT-TO

<<<BEGIN REVIEWER-HOIST-REMOVE-FROM
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
<<<END REVIEWER-HOIST-REMOVE-FROM

<<<BEGIN REVIEWER-HOIST-REMOVE-TO
            _begin_stream_call(reviewer_provider, round_num, "attempt")
            # ONE logical reviewer call: its attempt AND its single parse retry share this
            # sink, and nothing from the builder or an earlier round is in it.
            reviewer_call_reasons: list[str] = []
            reviewer_out = _call_with_retry(
<<<END REVIEWER-HOIST-REMOVE-TO

<<<BEGIN REVIEWER-HOIST-INSERT-FROM
            )

            # F115 D1: compose instead of calling `_build_reviewer_prompt`, so the
            # trace entries below carry a real segment manifest. The sent bytes are
            # unchanged — `_build_reviewer_prompt` returns this same `.text`.
            reviewer_composed = compose_reviewer_prompt(
<<<END REVIEWER-HOIST-INSERT-FROM

<<<BEGIN REVIEWER-HOIST-INSERT-TO
            )

            # F106 T002b-i: the repair round's PRIMARY Reviewer attempt
            # resumes the prior round's Reviewer session only when the
            # provider honestly advertises support AND a session id was
            # actually captured last round — same rule as the Builder side
            # (T002a). The bounded parse retry below is a DIFFERENT call and
            # is NOT threaded this round; it stays full-context.
            # F106 T002b-ii step 1 (DECISION F106 D1): hoisted here, before
            # prompt composition, so a later round can gate the safe-diff
            # segment on this same value without recomputing it.
            reviewer_resume_ref: str | None = None
            if is_repair and getattr(reviewer_provider, "supports_resume", False) and result.rounds:
                prev_reviewer_out = result.rounds[-1].reviewer_output
                prev_actuals = getattr(prev_reviewer_out, "usage_actuals", None) or {}
                prev_session_id = str(prev_actuals.get("session_id") or "")
                if prev_session_id:
                    reviewer_resume_ref = prev_session_id

            # F115 D1: compose instead of calling `_build_reviewer_prompt`, so the
            # trace entries below carry a real segment manifest. The sent bytes are
            # unchanged — `_build_reviewer_prompt` returns this same `.text`.
            reviewer_composed = compose_reviewer_prompt(
<<<END REVIEWER-HOIST-INSERT-TO

## Done when — the gates

Report ONE line per gate with its REAL exit code; every gate runs strictly before C5, which writes the handback.

G1 TRANSPORT, at C0b. Report the byte length of `.agent/authored/f106-r9.md`
   and `.agent/last_block.md`; state whether equal (reviewer holds the original).

G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to slice PLAN9 (sha256 of
   both), under 50 lines, holds `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2 — a THREE-PARAGRAPH append. Re-measure the
   pre-commit byte length yourself (reviewer read 1833342 at `1470c3d7`);
   base + `\n` + RECORD9 + `\n` + DECISIONF106D1 + `\n` + R0758 must equal
   the committed size. THREE readings: (a) whole reconstruction; (b) the
   committed file's LAST THREE blank-line units equal RECORD9,
   DECISIONF106D1, R0758, in that order (the structural reader covering
   the WHOLE three-paragraph region, not just the last paragraph); (c) a
   negative control in a disposable worktree — one byte flipped inside
   RECORD9 (the FIRST appended paragraph, not the last) must be REJECTED
   by reading (b).

G4 THE LEDGER, at C1 and C2. Resolved unmoved at 55. Registered moves
   318→319 (`- R-0758 — ` added). `DECISION F\d+ D\d+ — ` moves 19→20
   (one line added: `DECISION F106 D1`). `Gate: F106 R8 — ` 0x before C2,
   1x after.

G5 THE CODE — PAIR SHAPE AND ORDERED APPLICATION, at C4. For EACH of the
   four pairs (BUILDER-HOIST-REMOVE, BUILDER-HOIST-INSERT,
   REVIEWER-HOIST-REMOVE, REVIEWER-HOIST-INSERT): run your own containment
   test BOTH WAYS (`TO in FROM` and `FROM in TO`) and report both results;
   then report FROM's/TO's occurrence counts before/after C4. All four:
   FROM 1x→0x, TO 0x→1x. After C4: `python3 -c "import ast;
   ast.parse(open('packages/orchestration/pingpong_loop.py').read())"`
   exits 0; `python3 -m ruff check packages/orchestration/pingpong_loop.py`
   exits 0.

G6 ZERO BEHAVIOR CHANGE, at C4 — the BROADENED suite per constraint 16:
   `python3 -m pytest tests/orchestration/test_pingpong.py
   tests/orchestration/test_provider_mode.py
   tests/orchestration/test_provider_evidence_integration.py
   tests/orchestration/test_session_resume.py
   tests/orchestration/test_builder_prompt_golden.py
   tests/orchestration/test_builder_prompt_quality.py
   tests/orchestration/test_builder_prompt_hunk_rejections.py -q` —
   reviewer measured 122+26+51 = 199 passed at base; report your own exact
   total and, if it disagrees, the per-file breakdown before ruling.
   `tests/orchestration/test_provider_retry.py` is DELIBERATELY EXCLUDED
   from this gate — its 4 pre-existing failures are R-0758, unrelated to
   and unaffected by this round's own edit (confirmed in R0758 itself);
   do not run it as part of this gate and do not report it as a regression.

G7 THE PROSE SLIP APPEND, at C3. Re-measure `.agent/prose_slips.md`'s
   pre-commit byte length yourself; base + `\n` + PROSESLIPR8 must equal
   the committed size, and the committed file's last blank-line unit must
   equal PROSESLIPR8 exactly.

G8 THE TREE, at C4 (checked again before C5, which necessarily dirties the
   tree until its own commit). `git status --porcelain` empty, `git
   ls-files --others --exclude-standard` count 0, every commit's
   insertions under 500 (`git diff --numstat`); `git diff --stat` for
   `packages/orchestration/pingpong_provider.py` and
   `packages/orchestration/provider_token_evidence.py` both empty,
   confirmed both before and after C4.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: state
block, `## Commits` table (`+/-` from `git diff --numstat`), deviations,
item-status table with every bundle item and gate exactly once, next
steps — T002b-ii step 1 CLOSED (the hoist), step 2 (the actual shrink) and
T003 both remaining, step 2 governed by DECISION F106 D1, and R-0758
registered OPEN (not fixed this round) for a future repair round. States
`SESSION 3` of F106, round 9. No length cap.
