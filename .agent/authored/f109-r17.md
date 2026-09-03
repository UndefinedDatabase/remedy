== STEP integration-gate / F109 — ROUND 17 ==

SESSION 4 of feature F109. Round 17. Rounds so far: 16 done, this is the 17th.
Soft limit is 25 rounds / 7 sessions (docs/agents/self_drive_protocol.md G7,
amend0827 rule 6); at 17 rounds and 4 sessions it is NOT reached, so no scope
report is due. No line of this block is a run of a repeated character, so there
is no run length to recover (§3 checklist item 37).

Scope rule, verbatim as every F109 order must carry it:
RESUMED SESSION ONLY, PROVEN SENDS ONLY.

## Goal

Run the INTEGRATION GATE for F109 — the full suite on this branch and at the
merge base, compared and attributed per docs/agents/integration_gate.md — and
land its evidence under `.agent/gate_f109_r17/`. Book round 16's PASS, resolve
`R-0780` and `R-0781`, and register and repair `R-0782`, the third stale-prose
site of the same class, found by the round 16 sweep.

## Bundle, in commit order

- C0a  save this block verbatim to `.agent/authored/f109-r17.md`
- C0b  mirror it to `.agent/last_block.md`
- C1   apply PLAN17 to `.agent/plan.md`            (FIRST substantive commit)
- C2   append RECORD17 to `.agent/live_review.md`  (verdict, two resolutions, new id)
- C3   apply PAIR E to `tests/orchestration/test_semantic_dedupe.py`
- C4   the integration gate's evidence files under `.agent/gate_f109_r17/`
- C5   rewrite `.agent/handoff.md`

## Change set — these paths and nothing else

    .agent/authored/f109-r17.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    tests/orchestration/test_semantic_dedupe.py
    .agent/gate_f109_r17/            (new directory; `.txt` files only)
    .agent/handoff.md

## Constraints

1. EVERY slice below is applied BYTE FOR BYTE — no rewrap, no re-indent, no
   improvement. If a slice looks wrong, apply it anyway and declare it in the
   handback; that is how a reviewer mistake becomes visible rather than becoming
   a silent correction.
2. `.agent/live_review.md` ends WITHOUT a trailing newline and that convention is
   preserved: append exactly the two bytes `\n\n` then RECORD17, which itself
   ends without one. Never rewrite a landed entry.
3. C3 changes ONE DOCSTRING. No executable line moves, no case is added, renamed
   or deleted, no import changes. The dedupe suite's collected count must be
   IDENTICAL before and after C3, and it is 130 at `35c0b03f`.
4. THE GATE IS RUN, NEVER ASSUMED (self_drive_protocol G4). If the gate finds a
   reproducible branch-only failure coupled to F109 code, that is a BLOCKER:
   STOP, write the handback saying so, and do NOT attempt the fix — it is its
   own reviewer-gated round (integration_gate.md step 4).
5. Evidence files are `.txt`, NEVER `.log` — `.gitignore` drops `*.log` silently
   and the review-zip guard rejects any `.log` member (R-0169).
6. WHILE A SUITE RUNS, its log is written OUTSIDE any git worktree the suite is
   measuring: write to `.remedy-wt/` (gitignored) and copy into
   `.agent/gate_f109_r17/` only AFTER the run has exited. A log growing inside a
   measured tree changes that tree's digest mid-run and produces false failures
   in the manifest-identity ids (R-0176).
7. Nothing outside the change set is edited. If the sweep finds something else,
   DECLARE it; do not repair it.
8. Never force-push, never work on main, never create or merge a PR this round.

## The sandbox deltas the gate procedure does not know about

docs/agents/integration_gate.md is the procedure and you follow it as written.
These are the local substitutions its commands need, all of them measured:

- ENV ASSIGNMENT IS DENIED in all three shell forms, so
  `REMEDY_UI_NO_AUTO_BUILD=1 pytest ...` cannot be typed. Set it IN-PROCESS and
  invoke pytest as a library, from a scratch `.py` file under `.remedy-wt/`:
  `import os; os.environ["REMEDY_UI_NO_AUTO_BUILD"] = "1"; import pytest;
  raise SystemExit(pytest.main(["-n", "auto", "-q"]))` with the working
  directory set to the tree under measurement. The gate doc's own warning stands:
  that variable is NOT trusted alone, which is what the mtime reading below is for.
- `cp` IS DENIED. Copy the UI artifacts with
  `shutil.copytree(src, dst, symlinks=True)`. **`symlinks=True` IS LOAD-BEARING
  AND IS NOT THE DEFAULT.** `copytree` defaults to `symlinks=False`, which
  DEREFERENCES npm's bin shims and has itself CAUSED 7 of 23 base-only failures
  on a previous gate (finding R-0591). The gate doc's "never symlink them" means
  do not make the DIRECTORY a symlink; the symlinks INSIDE it must survive.
- THE BASE WORKTREE IS CREATED ON A BRANCH, never detached — the self-dogfood
  branch guard refuses a detached HEAD by design (DECISION D3):
  `git worktree add -b tmp/base-gate .remedy-wt/base-gate 5e18a8536afa086b591b5a2e13009d68d6227432`
  That SHA is the merge base of `main` and this branch, measured at `35c0b03f`.
  Afterwards remove the worktree BY ITS EXACT PATH, `git worktree prune`, and
  delete the `tmp/base-gate` branch; prove the result with `git worktree list`.
- MTIME PARITY IS MEASURED AS AN EVENT, NOT AN OUTCOME (R-0444). Record the mtime
  of every file under the base worktree's `apps/ui/dist` BEFORE the base run and
  again AFTER, and report the run's own start and end timestamps as the window.
  ANY mtime falling inside that window VOIDS the parity claim and forces per-id
  attribution of every base-only failure. A content hash may accompany that
  reading but never replaces it: equal content is consistent both with no rebuild
  and with a byte-identical one.
- A KNOWN TRAP, so you do not spend the round rediscovering it (R-0736):
  `git worktree add` stamps the files it checks out with the CURRENT time, while
  `copytree` preserves the SOURCE mtimes. A naive "is dist newer than the
  checkout?" reading therefore reports a rebuild that never happened. Compare
  against the RUN WINDOW as ordered above, never against the checkout's own
  timestamps.
- THE SUITE IS LONG. Give every full-suite invocation a generous timeout and do
  not let a tool-level timeout be reported as a suite failure; if an invocation
  is cut off, say so plainly and re-run it rather than reporting its partial tail
  as a result.

## SLICE PLAN17 — the whole of `.agent/plan.md`

BEGIN PLAN17
# Plan — F109 Semantic dedupe

Branch: feature/f109-semantic-dedupe, cut from `main` at
`5e18a8536afa086b591b5a2e13009d68d6227432` (pull request 231 merged).

## Goal

Within a RESUMED session only, stop resending context the model has
already provably received: segments whose hash already went to that exact
session are replaced by short reference markers. Everywhere else full
content wins, because only a resumed session guarantees the model still
holds the prior content. The scope rule of the whole feature is "resumed
session only, proven sends only".

## Current Step

Round 17, session 4. THE INTEGRATION GATE
(docs/agents/integration_gate.md): the full suite on this branch and at
the merge base, compared, with every branch-only failure attributed, and
the evidence landed under `.agent/gate_f109_r17/`. Also book round 16's
PASS, resolve `R-0780` and `R-0781`, and register and repair `R-0782` —
the `_capture_compositions` docstring, the third stale-prose site of the
same class, which still says the dedupe report has no consumer.

## Next Steps

- The closure sequence (docs/roadmap/STATUS_closure_protocol.md):
  evidence job, a FRESH review zip, the authored STATUS line, the PR.
  That sequence also runs the single consolidation pass on the checklist
  of docs/agents/planner_reviewer_prompt.md section 3.

## Risks

- A reproducible branch-only failure coupled to F109 code is a CLOSURE
  BLOCKER and earns its own reviewer-gated round; it is never repaired
  inside the gate round that found it.
- Nothing dedupes in production: every concrete adapter returns
  `supports_resume = False`, so the mechanism is suite-only today.
  `docs/system/semantic-dedupe-v1.md` states this plainly.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each. That is `R-0778`.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
END PLAN17

## SLICE RECORD17 — appended to `.agent/live_review.md`, four paragraphs

BEGIN RECORD17
Gate: F109 R16 — the round 16 entry. VERDICT PASS, over the range `cf210f6f..35c0b03f`. THE TRANSPORT PROOF IS AGAIN A REAL ONE: the reviewer wrote the block to `.remedy-wt/f109-r16.md` before delegating, so `cmp` against `.agent/authored/f109-r16.md` compared the worker's copy to the reviewer's OWN original — exit 0, digest `b85da6a0394e996f10a3f672c1204c09024818efc41f1563388f25252e135c52` twice. ALL SIX SLICES WERE VERIFIED BYTE-IDENTICAL by the reviewer independently: `.agent/plan.md` equals PLAN16 at 43 lines, RECORD16's two paragraphs are the tail of this record, and all FOUR pairs read FROM 0x and TO 1x in their targets. THE COMMENTS-ONLY CLAIM WAS PROVED, NOT ACCEPTED, and by a reading the block did not order: the reviewer parsed the BEFORE and AFTER blob of each of `9dab6cae` and `ca4879b4` with `ast` and compared, for every definition in the file, its NAME and the number of executable statements in its body with the docstring excluded — `session_sent_index.py` at 17 definitions and `test_semantic_dedupe.py` at 154, both sets identical and both statement maps identical. So no executable line moved, which is the property constraint 3 asked for and which a line diff alone cannot establish. THE SUITE COUNTS DID NOT MOVE IN EITHER DIRECTION, as that constraint also required: 130, 54, 27, 34, 173, 295 and 42, totalling 755 at exit 0, identical to the reviewer's own reading at `cf210f6f`. THE LEDGER, recomputed as a SET DIFFERENCE per `R-0778`: 342 registered ids all distinct, 66 `Done:` lines over 64 distinct resolved ids, open set 278. THE WORKER WROTE NEITHER A `Done:` NOR A `Landed:` LINE for the two findings it repaired, which constraint 4 required and which the reviewer confirmed by counting both strings at zero — the repairs are on disk and their resolutions are the two paragraphs below, authored here. THE TREE is clean and the branch is pushed at `35c0b03f`.

Done: R-0780 — RESOLVED at `9dab6cae` and verified by the reviewer at `35c0b03f`. Both stale bullets of the "Scope boundary — deliberate absences" section in `packages/orchestration/session_sent_index.py` now name the wiring that exists: the resume-fallback bullet states that `pingpong_loop.py` invokes `invalidate_on_resume_fallback` on the Builder path and again on the Reviewer path and that the same commit `7451e9c7` added the `record_finalized_call` sites, and the dedupe bullet states that `_dedupe_resumed_segments` calls both decision functions since `24352750`, that both `compose_*` functions call that hook since `60343048`, and that the config plumbing landed at `b245e1c9`. The reviewer re-measured every one of those claims against disk rather than against the slice: `invokes it yet` and `invokes either function yet` both count 0 in that module, and in `pingpong_loop.py` `invalidate_on_resume_fallback(` and `record_finalized_call(` each occur twice while `should_dedupe_segment(` and `dedupe_marker_for_segment(` each occur once, which is exactly what the repaired text asserts. THE FIRST BULLET OF THAT SECTION WAS DELIBERATELY LEFT ALONE, and this resolution records the reasoning so that no later round reopens it as an oversight: it says the index is not persisted "here" and that writing `as_evidence_dicts()` at the finalization seam "is F109 T001b", which is an attribution of the work to a slice rather than a claim that the slice is outstanding, and both of its factual halves remain true of this module. That reading was taken twice, once when `R-0780` was registered and once at this gate.

Done: R-0781 — RESOLVED at `ca4879b4` and verified by the reviewer at `35c0b03f`, reading the module docstring ALONE via `ast.get_docstring` rather than the whole file, because the file carries an unrelated plural "the first cases in this" that a whole-file count would match as a substring. So read, the docstring contains `T003d` exactly once and `the first case` zero times: the enumeration now names the per-session sent-hash index, the composition hook and its markers, the config kill switch, the trace's record of what was not resent AND the measurement of what a run withheld, and the manifest sentence now quantifies over the cases that are about manifest SHAPE instead of naming a position that eleven call sites contradicted. Both halves of the finding's resolution condition are met. The class this finding belongs to has now cost this branch four ids — `R-0749`, `R-0773`, `R-0779` and this one — plus `R-0780` in a production module and `R-0782` below, and every one of them was a sentence that was TRUE when written and was falsified by a later round that did not sweep it.

- R-0782 — Low, A TEST HELPER'S DOCSTRING STILL SAYS THE DEDUPE REPORT HAS NO CONSUMER IN PRODUCTION CODE, AND NAMES THE PROMPT TRACE AS CARRYING THE MANIFEST BUT NOT THE REPORT. Found by the WORKER of F109 R16 during that round's G8 sweep, reported honestly against a gate that had already passed, and registered here at the reviewer's first opportunity. MEASURED INDEPENDENTLY by the reviewer at `35c0b03f`: the `_capture_compositions` helper of `tests/orchestration/test_semantic_dedupe.py` says wrapping the loop's compose functions "is how the LOOP's compositions are read without widening production code that has no consumer for the report yet", and its parenthesis says "a prompt trace carries the manifest, not the report". BOTH HALVES ARE NOW FALSE, and by the same commit: `78d2b7b5` made `build_trace_entry` in `packages/orchestration/prompt_trace.py` read `list(composed_prompt.deduped_names)`, so production code DOES consume the report, and the prompt trace DOES carry it — as the deduped NAMES rather than as the `ComposedPrompt` object. What remains true, and what the repair must keep, is the sentence's actual load: the composed OBJECT itself still never reaches `PingPongResult`, which is why the helper wraps the module namespace at all. WHY LOW: no behaviour is wrong, no gate is blind, no test is weakened and the suite is green; the damage is confined to a helper's explanation of why it exists. WHY IT IS REGISTERED AND NOT SLIPPED: the wrong state is on disk under `tests/`, which is the amend0827 rule 2 test, and this is the THIRD site of one class on this branch after `R-0780` and `R-0781` — a recurrence that the standing staleness sweep keeps catching one round after each falsification, which is the argument for the sweep rather than against it. FIX: restate the sentence so the object-versus-report distinction survives while the "no consumer" claim goes, naming `build_trace_entry` and `78d2b7b5` as the consumer that exists. Resolved when no docstring in that file says the dedupe report lacks a production consumer.
END RECORD17

## PAIR E — in `tests/orchestration/test_semantic_dedupe.py`

Containment test, run mechanically before emission: TO contains FROM: false.
REWRITE, so the proof is FROM 0x and TO 1x after C3. FROM counted in the target
at `35c0b03f`: exactly 1x.

BEGIN PAIRE_FROM
        so the run below stays the real one. The composed object itself never
        reaches ``PingPongResult`` (a prompt trace carries the manifest, not the
        report), so wrapping the two functions in the loop's own module namespace
        is how the LOOP's compositions are read without widening production code
        that has no consumer for the report yet.
END PAIRE_FROM

BEGIN PAIRE_TO
        so the run below stays the real one. The composed OBJECT itself never
        reaches ``PingPongResult``, and that is the reason this helper exists: a
        prompt trace carries the manifest and, since ``78d2b7b5``, the deduped
        NAMES that ``build_trace_entry`` reads off the composed prompt — but never
        the ``ComposedPrompt`` itself. Wrapping the two functions in the loop's
        own module namespace is therefore how the LOOP's own compositions are
        read, without widening production code that already consumes the report
        it needs.
END PAIRE_TO

## Done when — the eight gates. RUN each one and record its REAL exit code.

Every gate below runs at a commit STRICTLY EARLIER than C5, the commit that
writes the handback, so the handback can honestly quote all eight.

G1 TRANSPORT, one comparison and no chain. Run
   `cmp .remedy-wt/f109-r17.md .agent/authored/f109-r17.md` and report the exit
   code. That scratch file is the REVIEWER'S OWN original, so this comparison
   proves real transport and not merely your own self-consistency. Then report
   `sha256sum .agent/authored/f109-r17.md .agent/last_block.md` — one digest twice.

G2 THE PLAN. Extract PLAN17 by delimiter index and `cmp` it against
   `.agent/plan.md` after C1: exit 0, no output. Report `wc -l .agent/plan.md`,
   under 50 (AGENTS.md), and `grep -c '^## Goal'` and `grep -c '^## Next Steps'`,
   each 1.

G3 THE RECORD APPEND, four readings; the only slice earning full byte forensics.
   (a) ARITHMETIC. Report base size and base sha256 of `.agent/live_review.md` at
       `35c0b03f`, the appended length S, the new size, and whether base + S
       equals it. Confirm the file still ends WITHOUT a trailing newline.
   (b) A SECOND READER THAT COUNTS NO BYTE, covering the WHOLE appended region.
       Split the entire file on blank-line boundaries into units. Let N be the
       paragraph count of RECORD17 as YOUR SCRIPT COUNTS IT from the slice — do
       not take N from this block. Assert the LAST N units equal RECORD17's N
       paragraphs IN ORDER, printing each one's opening 60 characters.
   (c) A NEGATIVE CONTROL ON THE FIRST APPENDED PARAGRAPH. Copy the file to
       `.remedy-wt/live_review_negative_control_r17.md`, flip one byte INSIDE the
       FIRST appended paragraph there, and show reader (b) REJECTS the copy while
       ACCEPTING the tracked file. Report the tracked sha256 before and after to
       show it never moved, then delete that scratch file BY ITS EXACT PATH and
       report `os.path.exists` on that exact path as False.
   (d) COUNTS, AS A SET DIFFERENCE and never a subtraction (`R-0778`). Read the
       base from `git show cf210f6f:.agent/live_review.md`, never by rewinding the
       tracked file, and report five figures for base and five for the new state:
       registered ids, DISTINCT registered ids, `Done:` lines, DISTINCT resolved
       ids, and `len(set(registered) - set(resolved))`. Also report
       `grep -c '^Gate: F109 R16 — '` = 1, `grep -c '^Done: R-0780 — '` = 1,
       `grep -c '^Done: R-0781 — '` = 1 and `grep -c '^- R-0782 — '` = 1.

G4 PAIR E AND THE PROOF THAT NO CODE MOVED. Report PAIR E's FROM count in
   `tests/orchestration/test_semantic_dedupe.py` BEFORE C3 (1) and AFTER C3 (0),
   and its TO after C3 (1). Then, from `git show <sha>:<path>` blobs only, parse
   the BEFORE and AFTER blob with `ast` and report that the set of definition
   NAMES is identical and that every definition's count of executable body
   statements, with the docstring excluded, is identical. Report the dedupe
   suite's collected count before and after C3; both must read 130.

G5 THE INTEGRATION GATE — BRANCH RUN. Follow docs/agents/integration_gate.md
   step 1 exactly, at C3's tree. Record the raw tail, the FULL `FAILED` list, the
   REAL exit code and the wall time, and write the sorted failure list to
   `.agent/gate_f109_r17/branch_failed.txt`. THE REVIEWER RAN THIS SAME SUITE AT
   `35c0b03f` and measured 18937 passed, 20 skipped, ZERO failed, exit 0, in
   133.30s — so `branch_failed.txt` is expected to be EMPTY and the branch-only
   set empty with it. Report your own figures against those four; a divergence in
   any of them is worth declaring rather than smoothing over, and an empty
   failure file is a reading to be written down, not a step to skip.

G6 THE INTEGRATION GATE — BASE RUN AND COMPARISON. Follow integration_gate.md
   steps 2 and 3, with the sandbox deltas above. Write
   `.agent/gate_f109_r17/base_failed.txt`, and the two `comm` outputs as
   `branch_only.txt` and `fixed_by_branch.txt`. Report the mtime window reading
   and state plainly whether the parity claim HOLDS or is VOID. If it is VOID,
   attribute EVERY base-only id by direct evidence, naming the missing artifact
   per id — an unattributed base-only id counts as a genuine base failure and
   blocks the verdict.

G7 THE INTEGRATION GATE — ATTRIBUTION. For EVERY branch-only id, follow
   integration_gate.md step 4: re-run that exact node id SERIALLY and classify it
   as xdist-flake (serial-pass), or reproduce it at the merge base (serial-fail),
   or declare it a BLOCKER coupled to F109 code. Write the per-id table to
   `.agent/gate_f109_r17/attribution.txt`. If the branch-only set is EMPTY, say so
   and write that file stating the empty result and the command that produced it —
   an empty set is a reading, not a missing gate.

G8 THE TREE AND THE SWEEP. `git status --porcelain` EMPTY and
   `git ls-files .remedy-wt` returning nothing. Prove the base worktree and the
   `tmp/base-gate` branch are gone with `git worktree list` and `git branch
   --list 'tmp/*'`. Report each commit's insertion count from `git show --numstat`
   — the `+` column ONLY, per AGENTS.md DECISION F104 D1 — for every commit of
   this round EXCEPT C5, and compare cell by cell against your own `## Commits`
   table (§3 checklist item 28). Then re-read each file this round touched and
   report every sentence now stale, including any you did NOT repair, with the
   reason.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It has NO
length cap. It must carry: the SESSION NUMBER (4) and round (17); the item-status
table with every one of C0a, C0b, C1, C2, C3, C4, C5 appearing exactly once with
`done`, `skipped` or `deviated` and a reason; a per-commit changed-files table
with the `+/-` column; ONE LINE PER GATE G1 through G8 with its real reading; the
INTEGRATION GATE RESULT stated in one unmissable sentence — branch total, base
total, branch-only count, and whether any BLOCKER was found; the open-finding
count as a SET DIFFERENCE; your deviations and assumptions; and the next expected
action. Then `git push -u origin feature/f109-semantic-dedupe` and report the
result. Create no PR.
