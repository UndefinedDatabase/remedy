── STEP R8/~10 — F107 Context compiler v2 — persist the R7 gate, close session ──
Goal:        Put the R7 verdict and finding R-0274 on disk, advance the plan to
             R8, and rewrite .agent/handoff.md as the SESSION handoff. This
             round writes NO production code and NO tests: its entire purpose
             is that nothing this session verified dies with the session.
Bundle:      C1 authored-block save; C2 last_block mirror; C3 the two authored
             live_review pairs (LRF4 registers R-0274, LR7 appends the R7 gate
             entry); C4 plan rewrite; C5 session handoff rewrite; push;
             handback.
Change:      EXACTLY these paths and nothing else — all under .agent/:
             .agent/authored/f107-r8-1.md (new), .agent/last_block.md,
             .agent/live_review.md (authored pairs LRF4 and LR7 in C3 only),
             .agent/plan.md (full replacement PLAN7),
             .agent/handoff.md (your session-handoff rewrite).
Constraints: AGENTS.md in full. NO source file and NO test file is touched this
             round — if you find yourself opening anything under packages/,
             apps/ or tests/ to EDIT it, stop: that is R8's real work and it
             belongs to the next session. Never write a `Done:` line — the
             `Landed: R-0273` line already on disk stays exactly as it is and
             is NOT promoted, because only reviewer-authored text resolves a
             finding and R-0273's resolution has not been authored. Do NOT
             create a PR. Never touch main. Never force-push, never amend or
             rebase. Scratch only under .remedy-wt/, uncommitted. Apply
             authored slices byte for byte after sha256 verification; on
             mismatch STOP.

PROCEDURE (in order, one commit per item):
0. Preconditions: branch feature/f107-context-compiler-v2, HEAD 6acb3f04,
   `git status --porcelain` empty, `git worktree list` primary only (else STOP
   and hand back without changing anything).
1. C1 — copy .remedy-wt/f107-r8-1.block.md to .agent/authored/f107-r8-1.md and
   prove byte identity (`cmp`, or `sha256sum` of both — say which you used).
   Extract ALL FIVE slice bodies and verify each body's sha256 against its
   BEGIN marker digest BEFORE applying anything. On any mismatch STOP.
   Commit: chore(f107): save the R8 step block verbatim
2. C2 — copy the same file over .agent/last_block.md, prove byte identity.
   Commit: chore(f107): mirror the R8 block into last_block
3. C3 — apply BOTH live_review pairs in this ONE commit. BOTH ARE APPEND-
   SHAPED: each TO literally CONTAINS its FROM, so the proof is NOT "FROM 0x".
     * LRF4 — replace the single line held in slice LRF4FROM with the body of
       slice LRF4TO. That FROM is the bare "  OPEN." line that ends the R-0273
       bullet; it is the ONLY bare "  OPEN." line in the file, which you verify
       before applying. This registers R-0274 at the end of the Findings list.
     * LR7 — replace the single line held in slice LR7FROM with the body of
       slice LR7TO. This appends the R7 gate entry to the Steps section,
       keeping the gate entries contiguous and ahead of the trailing `Done:`
       and `Landed:` paragraphs.
   Apply LRF4 first, then LR7. Proof after the commit, scoped to the ADDED
   lines because the TO bodies legitimately repeat sentences the file already
   carries (planner_reviewer_prompt.md §4.9): each FROM string occurs exactly
   1x in the file; each TO-ONLY line occurs exactly 1x among the lines this
   commit's diff ADDS; and `git show --numstat HEAD -- .agent/live_review.md`
   reports 0 DELETIONS, which proves neither anchor line was edited. Also
   report `grep -c '^## Steps' .agent/live_review.md` → 1,
   `grep -c '^- R-0274' .agent/live_review.md` → 1, and
   `grep -c '^Done:' .agent/live_review.md` → 1 (the pre-existing R-0271
   resolution and no other).
   Commit: chore(f107): record the R7 gate and register R-0274
4. C4 — replace .agent/plan.md entirely with slice PLAN7; prove byte identity.
   Commit: chore(f107): advance plan to R8 T004 part 2
5. C5 — rewrite .agent/handoff.md as the SESSION handoff. This one is not a
   round handback but the session's only return channel
   (docs/agents/self_drive_protocol.md, "Ending a session"), so it covers the
   WHOLE session, not just this round. It must carry:
     - the feature and the rounds this session closed: F107 R5, R6, R7 all
       reviewed PASS, plus this state-only round R8-close;
     - the branch, the session's first and last SHA (2c75bddf -> your HEAD),
       and a per-round line giving each round's commit range and verdict;
     - a changed-files table for THIS round;
     - the verification results of THIS round (the gates below, real exit
       codes), plus a one-line statement that each earlier round's gates were
       re-run by the reviewer and are recorded in .agent/live_review.md;
     - open findings count 11 and next free ID R-0275;
     - an item-status table for C1–C5;
     - the next expected action, stated plainly: R8 = T004 part 2 — the
       `remedy job context <id> --task <tid>` CLI view, an end-to-end fixture
       task solved by the fake provider, and the size comparison in evidence;
       then the integration gate, then closure. The branch has NO PR yet and
       none is created until closure.
     - one line naming what F107 can NOT do yet: `context_compiler.py` has no
       caller outside its own tests, so the feature is a library and not yet
       something a user can run. Do not soften that.
   Cap: 60 lines, or up to 100 if the per-commit table needs it (AGENTS.md
   handoff.md rule) — never drop a mandated section to fit; if you exceed 60,
   carry the stated-cause line naming the actual count and the mandated
   content that caused it. This round has five commits and no probe
   transcripts, so 60 should be comfortable.
   Commit: chore(f107): rewrite handoff to close the session
   Then: git push (branch already tracks origin; plain push, never force)

Done when (run each, record command + real exit code + counted value):
  a. all five slice bodies' sha256 == their marker digests; the R8 block,
     .agent/authored/f107-r8-1.md and .agent/last_block.md byte-identical
     (name the tool you used).
  b. the C3 append proof from step 3: each FROM 1x in the file, each TO-only
     line 1x among the added lines, numstat deletions 0, '^## Steps' → 1,
     '^- R-0274' → 1, '^Done:' → 1.
  c. .agent/plan.md byte-identical to the verified PLAN7 bytes;
     wc -l < .agent/plan.md → 28 (PLAN7 is 28 lines).
  d. python3 -m pytest tests/orchestration/test_context_compiler.py -q
     → exit 0, 55 passed — unchanged, since this round touches no code.
  e. python3 -m pytest tests/cli/test_golden_path.py -q → exit 0 (report the
     passed count).
  f. grep -c '^<<<' on .agent/live_review.md, .agent/plan.md and
     .agent/handoff.md → 0 each (grep exit 1 is the pass).
  g. git status --porcelain → empty; git worktree list → primary only;
     HEAD == origin/feature/f107-context-compiler-v2; insertions per commit
     (git log --numstat 6acb3f04..HEAD) each < 500.
  h. git diff --name-only 6acb3f04..HEAD → exactly the five paths the Change
     line names, nothing else — and NOTHING under packages/, apps/ or tests/.
Handback:    completion report (tables + raw gate results a–h + deviations)
             — .agent/handoff.md rewritten as C5.

<<<BEGIN SLICE LRF4FROM sha256=d129628fa2837d890b9ec02919cec5ee55b52e22af5ce4ab9c9dc5ac29a41bb4 lines=1>>>
  OPEN.
<<<END SLICE LRF4FROM>>>

<<<BEGIN SLICE LRF4TO sha256=b36108edabb5c7f4e9acf8798fe58849ec504c7dbbc90e55e81fa73c09a26a03 lines=13>>>
  OPEN.
- R-0274 (Low, F107 R7): the R7 step block CONTRADICTED ITSELF about where the
  `Landed: R-0273` line belongs. Its Change line scoped `.agent/live_review.md`
  to "authored pairs LRF3 and LR6 in C3 only", while PROCEDURE step 8 directed
  the worker to write the `Landed:` line and carry it in commit C5. The same
  step also asked for "which commit" INSIDE the very commit that writes the
  line, which no commit can satisfy: a commit cannot contain its own SHA. The
  worker read both, applied the safe reading, named the commit by subject
  instead of by SHA, and DISCLOSED both points in its handback rather than
  guessing silently — the wanted behavior, and the reason neither cost a round.
  Fourth entry in the contract-accuracy class after R-0239, R-0247 and R-0272:
  a reviewer-authored block must not contradict itself and must not order a
  value that cannot exist. OPEN.
<<<END SLICE LRF4TO>>>

<<<BEGIN SLICE LR7FROM sha256=cdc1e3cf8619572f56c6d3c1c631c13c5d2c1a5256a7b675308fba47fec5ec73 lines=1>>>
  user can run. `LAST_REVIEWED_SHA` advances 54bc56c2 -> 861eb371.
<<<END SLICE LR7FROM>>>

<<<BEGIN SLICE LR7TO sha256=47bc40dde965360d2ef974ae78bd238071f6f79a9c527fa205e0078bda48ebf4 lines=48>>>
  user can run. `LAST_REVIEWED_SHA` advances 54bc56c2 -> 861eb371.
- Reviewer gate on R7 (2026-08-12): PASS. Range 861eb371..6acb3f04 = eight
  commits touching exactly the seven paths the R7 block named. Transport by the
  PRIMARY shape: `cmp` of `.remedy-wt/f107-r7-1.block.md` against
  `.agent/authored/f107-r7-1.md` and against `.agent/last_block.md` is silent,
  all three at 328 lines, and all five slice bodies recompute to their
  BEGIN-marker digests at their declared lengths (LRF3FROM 4ad9497d… 1 line,
  LRF3TO e3fdd106… 20, LR6FROM d85c84ac… 1, LR6TO dac43442… 50, PLAN6
  047fcc7a… 28); `sha256sum .agent/plan.md` returns that same PLAN6 digest.
  Both C3 pairs were APPEND-shaped and proven as such: `git show --numstat
  4909b1b1 -- .agent/live_review.md` reads `68  0` — ZERO deletions — each FROM
  still occurs exactly 1x, each of the 19 LRF3TO and 49 LR6TO TO-only lines
  occurs exactly 1x among the 68 added lines, and 0 added lines belong to
  neither body. Every scoped gate was RE-RUN by the reviewer: the module suite
  returns 55 passed (the 52 frozen tests plus 3 new), the canary returns 42
  passed, `python3 -m ruff check` returns "All checks passed!", `.agent/plan.md`
  is 28 lines, the Steps heading count is 1, `grep -c '^- R-0273'` is 1, the
  stray-marker count is 0 across the three state files, `git status
  --porcelain` is empty, HEAD equals `origin/feature/f107-context-compiler-v2`
  and `git worktree list` shows the primary checkout alone. Insertions per
  commit 328, 255, 68, 9, 16, 113, 75, 18 — each under 500. THE FIX WAS
  MEASURED, not read: the reviewer re-ran the same three-file fixture at
  `line_cap=3` that produced the R-0273 numbers, and the rendered text's
  estimate falls from 128 tokens to 46 against an `estimated_tokens` of 25 —
  the 5.1x divergence is gone. The residual 21-token gap is the block HEADER
  lines the renderer adds, it is the same ~20 tokens at the default cap, and it
  is therefore uniform overhead rather than cap drift; it is recorded here as
  an observation for R8's evidence work, NOT as a finding, because
  `estimated_tokens` is documented as a sum over file contents and the headers
  are one bounded line per included file. The reviewer ran TWO probes in a
  disposable worktree at 6acb3f04 and both reproduce the worker's numbers
  verbatim: putting the renderer back on the module default gives `1 failed, 54
  passed` on `test_signature_blocks_render_at_the_cap_the_context_was_compiled`
  `_at`, and storing the default in the constructor instead of the caller's cap
  gives `3 failed, 52 passed` — so the regression test genuinely bites and the
  handback's evidence is confirmed TRUE rather than taken on trust. That
  worktree was removed and pruned before this verdict. Both declared deviations
  are accepted. The 114-line handoff exceeds even the D15 100-line ceiling, and
  the cause is mandated content this reviewer ORDERED — gate i was required to
  carry both step-7 transcripts with failing test names and assertion texts —
  so it is a stated-cause overage and not verbosity; no section was dropped.
  The eighth commit is the right call and not a scope breach: it corrects a
  stale grep line number in the handoff, touches only a path the Change line
  already names, and was made in its own commit because amending C7 is
  forbidden — leaving a false counted value in the return channel would have
  been the worse error. One new finding, R-0274, is registered above for the
  block's own self-contradiction. `LAST_REVIEWED_SHA` advances 861eb371 ->
  6acb3f04.
<<<END SLICE LR7TO>>>

<<<BEGIN SLICE PLAN7 sha256=a065b87c36269a51fdb26939c90f2e668f828cd246ceeb9daef09938d3f7acfb lines=28>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0275. R7 reviewed PASS at 6acb3f04.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R8 — T004 part 2, NOT YET STARTED: the `remedy job context <id> --task <tid>`
CLI view that renders what a task received and what was omitted, an end-to-end
fixture task solved by the fake provider using the compiled context, and the
whole-file size comparison recorded in evidence. `compare_context_size` and
`OMITTED_CONTEXT_FILENAME` already exist for it. T001-T004-part-1 are frozen.
Note for whoever plans it: `context_compiler.py` still has NO caller outside
its own tests, so R8 is the round that makes F107 a feature rather than a
library.

## Next Steps
1. Integration gate per docs/agents/integration_gate.md.
2. Closure per docs/roadmap/STATUS_closure_protocol.md.
3. The branch has no PR yet; it is created at closure, never merged same-session.
<<<END SLICE PLAN7>>>
