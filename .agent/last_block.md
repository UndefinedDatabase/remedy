── STEP T002c-ii — F109 Semantic dedupe, ROUND 10, SESSION 2 ──────────

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

Base commit: d7fbff5b99d35e1601c6001086a508187eaed323. Branch:
feature/f109-semantic-dedupe. Do not create a branch, do not switch
branch, do not create a PR, do not merge anything.

THIS IS THE LAST ROUND OF SESSION 2. The handback carries the session
boundary, per the Handback section at the end of this block.

Goal:
  Book round 9's PASS, resolve `R-0772`, and land the last piece of T002c
  that this feature owns: the CONFIG KILL SWITCH. `run_pingpong` gains one
  parameter that disables semantic dedupe for a whole run, forwarded to both
  compose calls, so an operator can rule the feature out while diagnosing
  something else without editing code.

Bundle:
  C0a  save this block verbatim to `.agent/authored/f109-r10.md`
  C0b  mirror it to `.agent/last_block.md`
  C1   rewrite `.agent/plan.md` from SLICE PLAN
  C2   append SLICE RECORD and SLICE DONE to `.agent/live_review.md`
  C3   the kill switch (SPEC V)
  C4   the cases of SPEC W in `tests/orchestration/test_semantic_dedupe.py`
  C5   rewrite `.agent/handoff.md`

Change set — these paths and no others:
  .agent/authored/f109-r10.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  packages/orchestration/pingpong_loop.py
  tests/orchestration/test_semantic_dedupe.py
  .agent/handoff.md

Constraints:
  1. SLICE PLAN, SLICE RECORD and SLICE DONE are applied BYTE FOR BYTE. Do
     not edit, rewrap, retype or improve them. C0a and C0b are `cp`.
  2. `.agent/live_review.md` ends WITHOUT a trailing newline at the base
     commit. Keep it that way. Nothing already in that file is edited,
     renumbered or deleted — the `Landed: R-0772` line STAYS standing beside
     its new `Done:` paragraph, as every resolved finding's has.
  3. C1 lands before C2, and C2 before C3.
  4. In `pingpong_loop.py` ONLY the edits SPEC V describes are permitted:
     one new parameter on `run_pingpong`, its docstring sentence, and one new
     keyword argument at each of the TWO PRIMARY compose calls. Nothing else
     in that file changes. In particular:
       (a) do NOT touch either resume-fallback recomposition — they pass no
           dedupe arguments at all and must keep passing none, because a
           fallback must send full content whatever the flag says;
       (b) do NOT change the two `<role>_composed = compose_<role>_prompt(`
           statement texts themselves — two guards in
           `tests/orchestration/test_prompt_trace.py` count them and pin the
           second to the fallback branch, and G6 re-runs that suite.
  5. `packages/orchestration/prompt_segments.py`, `prompt_trace.py` and
     `token_ledger.py` ARE NOT TOUCHED and are not in the change set.
  6. In the test file, nothing already present is edited, reordered or
     deleted, with ONE named exception: the existing import statements may be
     EXTENDED. New cases go at the END. Reuse the existing chain fixtures.
  7. Do NOT gate on `npm run lint` and do NOT gate on `ruff`. Follow ruff by
     construction: every new line under 120 characters, extended import lists
     in `order-by-type` isort order.
  8. Every pytest process uses `python3 -B`, and `__pycache__` is purged
     before every run of G5. G5's mutations run ONLY inside a disposable
     worktree, added and removed BY EXACT PATH, never in the primary
     checkout. Do not leave your shell's working directory inside a worktree
     you then remove.
  9. EVERY gate below — G1 through G7 — runs at C4 or earlier, so every
     reading the handback quotes already exists when C5 writes it. C5's own
     insertion count is NOT quoted anywhere in C5; the reviewer measures it.

SPEC V — the kill switch (C3). Production code: described here, written in
the file's own idiom.

  `run_pingpong` gains ONE keyword-only parameter, placed with the other
  behaviour flags rather than at the end of the signature:

      semantic_dedupe_enabled: bool = True,

  It is forwarded to BOTH PRIMARY compose calls as

      dedupe_enabled=semantic_dedupe_enabled,

  beside the `dedupe_sent_hashes=` argument each already passes. Add a short
  comment at the first of the two naming F109 and saying what the flag is
  for; the second may point at the first rather than repeating it.

  Document the parameter in `run_pingpong`'s docstring in that function's own
  style: F109's kill switch; False disables semantic dedupe for the whole
  run, whatever the session index holds; True is the default because dedupe
  is the feature's point and the switch exists so an operator can rule it out
  while diagnosing something else.

  THE SWITCH MUST BE TOTAL, AND FORWARDING IT IS THE WHOLE IMPLEMENTATION.
  `should_dedupe_segment` consults `enabled` first and alone, and
  `_dedupe_resumed_segments` returns immediately on False. Do NOT add a
  second test of the flag anywhere, and in particular do NOT make the
  `dedupe_sent_hashes=` expression conditional on it: two guards for one
  property is how one of them stops being observable, and the `enabled`
  branch is the one the mutation red-proofs already reach.

  THE FALLBACK IS DELIBERATELY UNAFFECTED, and say so in the comment: the
  resume-fallback recompositions pass no dedupe arguments, so they send full
  content whether the flag is True or False. A fallback is not a resumed
  session; that is `R-0771` and the flag does not enter into it.

SPEC W — the cases (C4). Add at the END of the test file. Drive the REAL
loop through the existing chain fixtures. These are MANDATORY:

  1. THE SWITCH WORKS, AND ONLY THE SWITCH DIFFERS. On the same fixture, run
     a resumed repair chain twice: once with `semantic_dedupe_enabled=False`
     and once with the parameter left at its default. Assert that the
     default run composes at least one `[unchanged: ` marker and the disabled
     run composes NONE, and that BOTH reach
     `final_status == "staged_review_passed"`. The two halves belong in one
     case if that is the honest way to show nothing but the flag changed;
     split them only if the fixture forces it, and say why.
  2. THE DEDUPED-NAME REPORT AGREES WITH THE SWITCH: in the disabled run
     every composed prompt reports `deduped_names == ()`. Read the composed
     objects the same way round 9's case 5 does.
  3. A chain that NEVER RESUMES composes no marker with the flag at either
     value, and completes both times. The flag must not become the only
     thing standing between a fresh call and a marker — the resume condition
     is, and this case says so.
  4. The flag does not disturb the fallback: a resumed chain whose builder
     resume FAILS sends full content on the fallback call with the flag at
     either value. Reuse round 8's fallback fixture and its capture helper.

SLICE PLAN — the WHOLE of `.agent/plan.md`, byte for byte:
<<<SLICE PLAN
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

Round 10, session 2, the last round of that session — book round 9's PASS,
resolve `R-0772`, and land the config kill switch. `run_pingpong` gains
`semantic_dedupe_enabled`, defaulting to True and forwarded to both primary
compose calls as `dedupe_enabled`, so an operator can disable semantic
dedupe for a whole run without editing code. The resume-fallback
recompositions stay outside it: they send full content whatever the flag
says, because a fallback is not a resumed session.

## Next Steps

- Surface the deduped names into the prompt trace, answering the
  `schema_v` question on its own evidence. The manifest row keys stay
  closed: the `call_segments` table in `token_ledger.py` mirrors them
  column for column, so widening them is a token-ledger change.
- The measurement fixture on a resumed fixture chain with the savings
  recorded, plus the docs (T003).
- The integration gate, then the closure sequence.

## Risks

- A suite that no round gate names can go red without anyone seeing it.
  That is what `R-0772` was. Every block from here names the suites its
  change set can REACH, not only the ones it expects to move.
- The prompt TRACE entry is written before the provider call, so on a
  resume fallback it describes the abandoned resumed composition rather
  than the full one actually sent. The bytes sent and the recorded
  manifest were both repaired by `R-0771`; the trace ordering was not.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
SLICE PLAN

SLICE RECORD — appended to `.agent/live_review.md`. It is one paragraph.
Append a blank line, then this text, and leave the file without a trailing
newline:
<<<SLICE RECORD
Gate: F109 R9 — the round 9 entry. VERDICT PASS, AND THE BRANCH IS GREEN AGAIN, over the range `5a63d277a487900c0ab562159ba91d2e42bc23b6..d7fbff5b99d35e1601c6001086a508187eaed323`. TRANSPORT, strongest form: one digest across the reviewer's scratch original, the committed `.agent/authored/f109-r9.md` and its mirror, `7a1ccd00d93a9ed1406f3f199d684cfe8a25f07b6043cf1b163f670cba62c862`. THE REPAIR LANDED AS ORDERED AND THE RED IS GONE: `tests/orchestration/test_prompt_trace.py` is exit 0 at 46 passed, where at the base commit it was exit 1 at 2 failed, 44 passed. The two guards were RESCOPED rather than deleted, which is §3 item 7's own counter-measure: each now asserts two composition sites AND that one of them occurs in the source following its role's fallback guard line, and the edit removed exactly 2 lines — the two stale assertions — against 16 inserted. THE REVIEWER PROVED BOTH HALVES OF THAT GUARD SEPARATELY, because a rescoped guard that only ever fails on its count is a bare number wearing a better comment. Deleting the builder fallback recomposition takes the count to 1 and fails at the COUNT assertion; and a second mutation the block never ordered — keeping the count at 2 by adding a decoy composition outside the branch while removing the one inside it — fails at the FALLBACK-PINNING assertion instead, which is the case a bare number could not catch. Both were run by the reviewer in a disposable worktree added and removed by exact path. ONE CORRECTION TO THE HANDBACK, non-load-bearing and stated only so the record is not wrong: the round reported its Mutation A as failing at the fallback-pinning assertion "not the bare count", and it fails at the count, because removing the recomposition drops the count to 1 and that assertion runs first. The gate's requirement — that the suite go red — was met either way, and the pinning assertion's own value is established by the reviewer's second mutation above rather than by that one. THE ROW SHAPE STAYED CLOSED, which constraint 4 existed for: a manifest row's key set is exactly `chars`, `name`, `rank`, `sha256`, `tokens_estimated` on builder, reviewer and deduped compositions, and `deduped_names` appears in no row — so `token_ledger.py`'s `call_segments` table needs no migration and `test_token_ledger.py` is exit 0 at 120. THE SUITES ARE THE REVIEWER'S OWN, run serially, every one exit 0, base in parentheses: prompt_trace 46 (2 failed, 44 passed), semantic_dedupe 116 (109), prompt_segments 25 (25), token_ledger 120 (120), builder golden 36 (36), reviewer golden 39 (39), builder quality 14 (14), pingpong 34 (34), session_resume 27 (27) and cli golden_path 42 (42). STRUCTURE: every commit in the range is single-parent, insertions 380, 271, 21, 7, 19, 32, 175 and 398 in that order, all under 500; the range numstat lists the nine ordered paths and nothing else; the test-file addition is ONE insert of 175 lines with ZERO removed; `.agent/plan.md` is byte-equal to the authored slice at 49 lines; longest new lines are 119, 86, 102 and 92 against the configured 120; the ledger reads 333 registered, 64 resolved and 27 landed, with `Landed: R-0771` still standing beside its `Done:` paragraph; `git status --porcelain` is empty and the remote tip equals the local tip at `d7fbff5b99d35e1601c6001086a508187eaed323`. THE ROUND PASSES.
SLICE RECORD

SLICE DONE — appended in the SAME commit, as its own paragraph after SLICE
RECORD. Append a blank line, then this text:
<<<SLICE DONE
Done: R-0772 — RESOLVED. THE FIX is in `tests/orchestration/test_prompt_trace.py` at `43dc4a7f`: `test_the_builder_call_site_hands_its_composition_down` and its reviewer twin no longer assert one composition site per role. Each now asserts TWO — the primary composition and the resume-fallback recomposition `R-0771` added — and then asserts that a composition occurs in the source FOLLOWING that role's `if <role>_resume_ref and <role>_out.error:` guard line, so the guard states the real shape instead of a number any future duplication would satisfy. Each test's docstring names `R-0771` as the reason the count is 2, so the next reader can tell the two sites apart. The production code was NOT changed to satisfy the guard, which was the fix clause's central requirement: the second composition is the `R-0771` repair and reverting it would have re-opened a High finding. THE REVIEWER VERIFIED THE FIX RATHER THAN THE REPORT, at `d7fbff5b99d35e1601c6001086a508187eaed323`: the suite is exit 0 at 46 passed against exit 1 at 2 failed, 44 passed at `5a63d277a487900c0ab562159ba91d2e42bc23b6`, and both halves of the rescoped guard were shown to bite, by two mutations run in a disposable worktree — removing the fallback recomposition fails the count assertion, and a decoy composition that keeps the count at 2 while emptying the fallback branch fails the pinning assertion. The finding's stated resolution condition — the suite green AND deleting the fallback recomposition turning one of the two rescoped guards red — is MET on both clauses. WHAT THE CLASS LEAVES BEHIND is a gate-list rule rather than a code rule, and it is already written into `.agent/plan.md`'s Risks: a block that adds a call to a named function greps the suite for tests that COUNT that string over that whole file, per §3 item 7, and a block's gate list names the suites its change set can REACH rather than only those it expects to move. `R-0772` existed because the round 8 block did neither, and the red then survived a full round undetected.
SLICE DONE

Done when — the gates listed below. Run every one, record its REAL exit code
and output, and give each ONE line in the handback.

  G1 TRANSPORT. `sha256sum .agent/authored/f109-r10.md .agent/last_block.md`
     prints ONE digest twice, equal to the digest the delegation wrapper
     states. Report it. The chain compares the saved copy against its mirror
     and claims nothing about the emitted bytes.

  G2 THE PLAN. `cmp` `.agent/plan.md` against the SLICE PLAN text extracted
     mechanically from `.agent/authored/f109-r10.md` — no output, exit 0.
     `wc -l .agent/plan.md` strictly under 50. `grep -c '^## Goal'` is 1 and
     `grep -c '^## Next Steps'` is 1.

  G3 THE RECORD APPEND, at C2.
     (a) Report the base byte count and sha256, the total appended length S
         after stripping any trailing newline, and confirm the arithmetic
         against the actual new size. Confirm the file still ends WITHOUT a
         trailing newline.
     (b) A SECOND, STRUCTURALLY DIFFERENT READER: split the whole file on
         blank-line boundaries into units; let N be the number of units the
         append itself contains, COUNTED by your script and not taken from
         this block; assert the LAST N units equal the appended paragraphs IN
         ORDER.
     (c) NEGATIVE CONTROL on a scratch copy under `.remedy-wt/`, never on the
         tracked file: XOR-flip one byte lying inside the FIRST appended
         paragraph, confirm reader (b) REJECTS it, report the tracked file's
         sha256 before and after to show it did not move, and delete the
         scratch copy BY EXACT PATH.
     (d) COUNTS: `grep -c '^Gate: F109 R9 — '` is 1; `grep -c '^Done: R-0772 — '`
         is 1 and `grep -c '^Done: R-[0-9]\{4\} — '` rose by exactly 1 from
         the base commit; `grep -c '^Landed: R-0772 — '` is STILL 1;
         `grep -c '^- R-[0-9]\{4\} — '` is UNCHANGED, because this round
         registers nothing.

  G4 THE EDIT SHAPE IS THE ORDERED ONE. For `pingpong_loop.py` at C3 and the
     test file at C4, read the pre-commit and post-commit blobs with
     `git show <sha>:<path>` — never by writing either revision over the
     tracked file — and compare them as SEQUENCES OF LINES with
     `difflib.SequenceMatcher(..., autojunk=False)`. Report EVERY non-equal
     opcode with its position and its lines, and account for each one against
     an edit SPEC V or constraint 6 names. Report the total lines DELETED in
     each file; for the test file it must be 0.

  G5 THE COLOUR: control green, and every mutation below red on its named
     case. In a disposable worktree added at the C4 commit BY EXACT PATH
     under `.remedy-wt/`. FIRST, before trusting any mutation, run with the
     worktree as cwd:
       python3 -B -c "import packages.orchestration.pingpong_loop as m; print(m.__file__)"
     and confirm the path is INSIDE the worktree. Purge `__pycache__` before
     every run. The command each time is:
       python3 -B -m pytest tests/orchestration/test_semantic_dedupe.py -q
     (a) CONTROL, unmutated: exit 0, and report the passed count.
     (b) MUTATION A — make `semantic_dedupe_enabled` default to False. The
         failure set must INCLUDE the half of SPEC W case 1 that says the
         DEFAULT run still composes a marker.
     (c) MUTATION B — at the BUILDER primary compose call, replace
         `dedupe_enabled=semantic_dedupe_enabled` with `dedupe_enabled=True`,
         so the flag is accepted and ignored. The failure set must INCLUDE
         the half of SPEC W case 1 that says the DISABLED run composes none.
     Before each mutation, confirm the exact text you are changing occurs
     EXACTLY ONCE in `packages/orchestration/pingpong_loop.py`, and report
     that count; where it occurs twice, quote a longer unique string and say
     which one you took. Restore the file between mutations from the C4 blob
     by exact path. Afterwards confirm the worktree is clean, remove it BY
     EXACT PATH, run `git worktree prune`, and report `git worktree list`.
     A wider red than ordered is fine — report it; a MISSING named case is a
     failure of the gate.

  G6 THE SUITES. Run these SERIALLY, never two pytest processes alive at
     once, and report each exit code and passed count. The count in
     parentheses is the REVIEWER's reading at the base commit; only the first
     is expected to move, and only upward. `test_prompt_trace.py` is in this
     list because constraint 4(b) exists — it counts the two composition
     statements this round edits the arguments of:
       tests/orchestration/test_semantic_dedupe.py        (116)
       tests/orchestration/test_prompt_trace.py           (46)
       tests/orchestration/test_prompt_segments.py        (25)
       tests/orchestration/test_token_ledger.py           (120)
       tests/orchestration/test_builder_prompt_golden.py  (36)
       tests/orchestration/test_reviewer_prompt_golden.py (39)
       tests/orchestration/test_builder_prompt_quality.py (14)
       tests/orchestration/test_pingpong.py               (34)
       tests/orchestration/test_session_resume.py         (27)
       tests/cli/test_golden_path.py                      (42)

  G7 THE TREE. `git status --porcelain` is EMPTY. `git ls-files .remedy-wt`
     returns nothing. Report the insertion count — the `+` column only, per
     AGENTS.md DECISION F104 D1, never insertions plus deletions — for each
     commit BEFORE C5, and confirm each is under 500. Take those numbers from
     `git show --numstat` and from nothing else. Compare the number you write
     in the handback's `## Commits` table, cell by cell, against the numstat
     output you quote here, and say in the handback that you did. Finally
     report the full `git diff --numstat` for
     `d7fbff5b99d35e1601c6001086a508187eaed323..` your last commit and confirm
     it lists exactly the change set above and nothing else.

Handback: rewrite `.agent/handoff.md`. It carries F109, ROUND 10, SESSION 2,
the branch, the commit table with subjects and its `+/-` column, the
changed-files table, ONE LINE PER GATE with its real result, the item-status
table over C0a–C5, every deviation, the open-findings count, and the next
expected action. There is no length cap. Push after C5.

THIS IS THE LAST ROUND OF SESSION 2, so the handback additionally states, in
its own clearly-headed section: that session 2 ends here; that the round 10
verdict is NOT in the ledger and is booked by session 3 in the FIRST commit
of its first round; and that session 3 resumes at the prompt-trace slice
named first in `.agent/plan.md`'s Next Steps. Name the branch tip SHA there
so the next session can verify it before doing anything.
