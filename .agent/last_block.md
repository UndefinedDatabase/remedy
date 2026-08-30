── STEP T002b-ii/2a — F106 ────────────────────────────────────────────────
Goal: Freeze the hunk-rendering convention DECISION F106 D1(b) requires
before T002b-ii step 2's actual prompt-shrink wiring can land: a pure
function turning a `RepairHunkSelection` (packages/orchestration/
diff_repair.py) into repair-prompt text, tested and mutation-red-proofed
in isolation. No caller is wired this round — nothing under
packages/orchestration/pingpong_loop.py or any compose_*_prompt function
changes. Zero behavior change to any existing consumer.

Bundle:
  C0a — save this step block verbatim to .agent/authored/f106-r11.md
  C0b — mirror it into .agent/last_block.md
  C1  — rewrite .agent/plan.md for round 11 (PLAN11 below)
  C2  — append RECORD11 below to .agent/live_review.md, booking round 10's
        PASS verdict (round 10 itself already ran its own full review
        before its handback; this books it per amend0827-process-diet
        rule 1 — a verdict does not buy its own round)
  C3  — append render_repair_hunks (+ 2 constants) to
        packages/orchestration/diff_repair.py
  C4  — rewrite the top import block and append TestRenderRepairHunks to
        tests/orchestration/test_diff_repair.py
  C5  — rewrite .agent/handoff.md for round 11 handback

Change: exactly the four paths named in C1-C4 plus .agent/last_block.md
(C0b) and .agent/handoff.md (C5); nothing else. No path under
packages/orchestration/pingpong_loop.py, no prompt_segments.py, no
test_builder_prompt_*.py, no test_reviewer_prompt_golden.py.

Constraints:
1. C0a/C0b are verbatim single-.agent-state-file saves (shutil.copyfile,
   never cp, never retyped) — exempt from the 500-line cap per AGENTS.md
   Commit Discipline.
2. C1 — PLAN11 is a REWRITE (full-file replacement) of .agent/plan.md,
   applied byte-for-byte via shutil.copyfile from the scratch original at
   .remedy-wt/f106-r11-plan.md. That file is 46 lines (< 50, AGENTS.md
   cap), holds `## Goal` and `## Next Steps`, sha256
   9f1beaf937d480053ba7c86d873109322310d1e92862af8ce837d254728efb29,
   2301 bytes.
3. C2 — RECORD11 is an APPEND to .agent/live_review.md: the scratch
   original at .remedy-wt/f106-r11-record11.txt (2487 bytes, sha256
   991238fbb6fc01ee4102adbb7daa53af47efcf339cf66df991d4c9abff88b9bf) is
   ONE paragraph (N=1). Apply as: read the current file (measure its own
   base length first — do not trust any number in this block over your
   own reading), append one "\n" separator plus the RECORD11 text
   verbatim. Base is expected at 1854867 bytes (re-measure it yourself;
   if it disagrees, stop and report rather than proceeding); expected
   post-C2 total is base + 1 + 2487.
4. C3 — the diff_repair.py change is a pure CODE APPEND, nothing existing
   rewritten. Apply via: read the current file, confirm it ends with
   `    return ranges\n` (the last line of changed_line_ranges_from_patch),
   then append exactly the bytes held at
   .remedy-wt/f106-r11-diffrepair-suffix.txt (1614 bytes, sha256
   1ac3775ea4adcb6c1da48a370f1dfecfc7c2ad9d96013046bd363fa8c91ef27f) —
   or, equivalently and preferably, shutil.copyfile the already-assembled
   whole file at .remedy-wt/f106-r11-diff_repair.py onto
   packages/orchestration/diff_repair.py (that scratch file's sha256 is
   unstated here on purpose — verify it yourself as
   orig-bytes-are-exact-prefix-of-new-bytes, which is the property that
   matters, not a third number to trust). Ordered-equality proof: the
   pre-commit file is a byte-exact PREFIX of the post-commit file, and
   the diff's ADDED lines are exactly the appended lines in order
   (`git show --numstat <C3 sha> -- packages/orchestration/diff_repair.py`
   for the total; the new file's tail for the order).
5. C4 has TWO parts, proved differently. Part (a) is a REWRITE: the
   existing top-of-file import block
       from packages.orchestration.diff_repair import (
           RepairHunk,
           RepairHunkSelection,
           changed_line_ranges_from_patch,
           select_repair_hunks,
       )
   becomes
       from packages.orchestration.diff_repair import (
           REPAIR_HUNKS_HEADING,
           REPAIR_HUNKS_OMITTED_INTRO,
           RepairHunk,
           RepairHunkSelection,
           changed_line_ranges_from_patch,
           render_repair_hunks,
           select_repair_hunks,
       )
   Measured (containment test, not asserted): TO does NOT contain FROM
   (`TO contains FROM: false`) — genuine REWRITE, not an append-shaped
   pair. Prove FROM 1x pre-commit -> 0x post-commit, TO 0x pre-commit ->
   1x post-commit. Part (b) is a CODE APPEND directly after part (a)'s
   edit lands: the whole scratch file at
   .remedy-wt/f106-r11-test_diff_repair.py is byte-identical to
   (orig-with-part-a-applied) + a suffix; that suffix is held separately
   at .remedy-wt/f106-r11-testdiffrepair-suffix.txt (3663 bytes, sha256
   02c5e1f6824cd25a6b765547bd59e2896f17d8e7b07ba9ea918c4b94b5988f8f).
   Simplest correct application: shutil.copyfile the whole scratch file
   .remedy-wt/f106-r11-test_diff_repair.py onto
   tests/orchestration/test_diff_repair.py directly (it already carries
   both part (a) and part (b) correctly composed and was validated
   end-to-end — ast.parse, ruff, and a live mutation red-proof — before
   this block was authored); verify the containment/ordered-equality
   properties above AFTER the copy, against the real committed diff, not
   before.
6. Mutation red-proof for C3/C4 is MANDATORY (production code) and runs
   ONLY inside a disposable git worktree, never the primary checkout
   (self_drive_protocol.md G5). Recipe: in the worktree, replace
   `parts.append(REPAIR_HUNKS_OMITTED_INTRO)` inside render_repair_hunks
   with `pass  # MUTATED` and confirm
   `python3 -B -m pytest tests/orchestration/test_diff_repair.py -q`
   goes RED (this reviewer already ran this exact recipe pre-delegation
   at base and got 1 failed / 36 passed; you are reproducing it, not
   discovering it fresh) — then revert and confirm 37 passed again before
   removing the worktree.
7. No `.agent/**` file other than plan.md, live_review.md, last_block.md,
   handoff.md and the one new authored/f106-r11.md is touched.
8. This round mints no new R-id and no new DECISION: it is executing an
   obligation DECISION F106 D1(b) already named ("invent and freeze a
   hunk-rendering convention"), not making a new architectural call.

Done when (8 gates, exact commands):
  G1 TRANSPORT — `.agent/authored/f106-r11.md` and `.agent/last_block.md`
     byte-equal (sha256 comparison), and both equal to this block's own
     bytes as the worker received them.
  G2 THE PLAN — `.agent/plan.md` sha256 equals
     9f1beaf937d480053ba7c86d873109322310d1e92862af8ce837d254728efb29,
     `wc -l < .agent/plan.md` < 50, holds `## Goal` and `## Next Steps`.
  G3 THE RECORD APPEND — re-measure `.agent/live_review.md`'s length
     immediately before C2 (call it BASE), then after C2 confirm the
     file's length equals BASE + 1 + 2487 AND the file's last blank-line
     unit (split on "\n\n") equals the RECORD11 text exactly.
  G4 THE LEDGER — line-anchored regex counts (`^- (R-\d+) — `,
     `^Done: (R-\d+) — `, `^DECISION (F\d+ D\d+) — `) over the whole file,
     before C2 and after C2: registered, resolved and DECISION counts all
     UNMOVED (this round registers nothing new).
  G5 THE CODE — `python3 -B -c "import ast; ast.parse(open(p).read())"`
     for both touched files, exit 0; `python3 -m ruff check
     packages/orchestration/diff_repair.py
     tests/orchestration/test_diff_repair.py`, exit 0, "All checks
     passed!"; the C3 ordered-equality and C4 REWRITE+APPEND proofs from
     constraints 4-5, independently re-measured against the real
     committed files.
  G6 THE TESTS — `python3 -m pytest tests/orchestration/test_diff_repair.py
     -q`, REAL exit 0, 37 passed (30 pre-existing + 7 new). Additionally
     `python3 -m pytest tests/orchestration/test_diff_repair_apply.py
     tests/orchestration/test_diff_repair_response.py
     tests/orchestration/test_builder_repair_loop.py
     tests/ui_server/test_command_channel.py -q`, REAL exit 0, 198 passed
     — every existing consumer of diff_repair.py, unchanged.
  G7 THE MUTATION RED-PROOF — constraint 6's recipe, run for real inside
     a disposable worktree, reported as: unmutated exit code + count,
     mutated exit code + count + failing test name, reverted exit code +
     count again, worktree removed, `git worktree list` afterward shows
     only the primary checkout.
  G8 THE TREE — `git status --porcelain` empty, `git ls-files --others
     --exclude-standard` empty, every commit's insertions reported via
     `git diff --numstat <sha>^..<sha>` (C0a/C0b exempt from the 500-line
     cap as verbatim `.agent/**` state-file saves).

Handback: completion report (every gate above, one line each, with the
REAL numbers you measured — never a word like "green" on its own) +
rewrite .agent/handoff.md with the standard sections (Session, Range,
Commits table with +/- per path, External actions, Verification,
Authored-text proofs, Deviations & assumptions, Next).
─────────────────────────────────────────────────────────────────────────


PLAN11 (the exact byte-for-byte content of .remedy-wt/f106-r11-plan.md;
apply via shutil.copyfile from that path, never retype):

# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 4, round 11.

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
| R-0758: fix `test_provider_retry.py`'s `resume`-kwarg gap | done | round 10 |
| T002b-ii step 2a: freeze the hunk-rendering convention | done | this round |
| T002b-ii step 2b: wire the shrink into compose_*_prompt | open | next |
| T003: measured fixture comparison + docs | open | |

## Next Steps
1. T002b-ii step 2b: add `resume_ref: str | None = None` to
   `compose_builder_prompt`/`compose_reviewer_prompt` (pingpong_loop.py);
   when set and a diff segment would fire, replace the full diff with
   `render_repair_hunks(select_repair_hunks(repo_root,
   parse_diff_line_ranges(repair_diff), ...))` (frozen this round);
   thread the round-9 hoisted `*_resume_ref` into the call sites; add a
   resume-active fixture shape to `test_builder_prompt_golden.py`/
   `test_reviewer_prompt_golden.py` (existing shapes stay unchanged).
2. T003 follows once T002 is fully closed (after step 2b lands).

## Risks
- No adapter's `supports_resume` is true in production yet — only
  `FakeProvider`, via its test-only constructor overrides, ever resumes
  or fails a resume. `render_repair_hunks` (this round) has no caller
  yet; zero behavior change held by construction, not test coverage.
- DECISION F106 D1's D1-compatibility reading (reusing F111's pure hunk
  functions for prompt content, never the diff-apply channel) governs
  step 2b's design; step 2b must not widen it further without a new
  DECISION.


RECORD11 (the exact byte-for-byte content of
.remedy-wt/f106-r11-record11.txt; apply as ONE paragraph appended to
.agent/live_review.md, never retype):

Gate: F106 R10 — R-0758 FIX: RESUME KWARG ACCEPTED BY FOUR TEST-ONLY PROVIDER SUBCLASSES. VERDICT PASS. The reviewer (a fresh session, no memory of round 10's own work) independently re-verified round 10's committed diff `2a0e08e13ccc5e4c9aaa138e96cf440f09e08a06..6f7d51fcb47dca52866d713f4f75d86423f8e532` against the real files and the round's own handback, not against the worker's summary alone. G1 TRANSPORT: `.agent/authored/f106-r10.md` and `.agent/last_block.md` independently sha256'd at `9ee2005eae0d44189e7a33a2253c862197445e76708ad801e78ce606fd16ae93`, both 25052 bytes, matching the handback's claim exactly and each other. G2 THE PLAN: `.agent/plan.md` independently confirmed to hold `## Goal` and `## Next Steps`, matching the handback's stated 42-line count; not re-extracted against a held PLAN10 scratch original, since this session holds none — accepted on the handback's own byte arithmetic. G3 THE RECORD APPEND: independently re-measured — `.agent/live_review.md` at HEAD is 1854867 bytes exactly, matching the handback's own arithmetic (1847519 + 1 + 6401 + 1 + 945); not re-run structurally a second time, since the byte total alone settles it and the appended region is untouched by this round's own work. G4 THE LEDGER: independently re-measured with line-anchored regexes over the whole file — registered 319 distinct `R-` ids, resolved 56 distinct `Done:` ids (`R-0758` now carries one), `DECISION` 20, all matching the handback exactly. G5 THE CODE: independently re-ran `python3 -m pytest tests/orchestration/test_provider_retry.py -q`, REAL exit 0, 34 passed, matching the handback's stated count exactly; independently confirmed `git diff --stat 2a0e08e1..HEAD -- packages/ apps/` is EMPTY — no production file was touched this round, exactly as the handback declares. G6/G7/G8 (the four pairs' own containment/occurrence forensics, the prose-slip append arithmetic, and the tree/lint readings): not independently re-run this round — the two checks above (a real pytest re-run and an empty production-path diff) already settle the round's one substantive claim, and the handback's own detailed readings (all four pairs FROM 1x→0x/TO 0x→1x, `ast.parse`/`ruff check` exit 0, `git status --porcelain` empty, every commit under 500 lines) are accepted rather than re-derived. THE ROUND PASSES: R-0758 CLOSED — all four test-only provider subclasses in `test_provider_retry.py` honestly forward `resume`, and zero production behavior changed.
