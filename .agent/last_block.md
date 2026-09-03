── STEP REPAIR — F109 Semantic dedupe, ROUND 9, SESSION 2 ─────────────

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

Base commit: 5a63d277a487900c0ab562159ba91d2e42bc23b6. Branch:
feature/f109-semantic-dedupe. Do not create a branch, do not switch
branch, do not create a PR, do not merge anything.

THIS IS A REPAIR ROUND. Round 8 is booked FAIL. Its change set left
`tests/orchestration/test_prompt_trace.py` RED on the branch tip — 2 failed,
44 passed — and the reviewer's round-8 gate list did not include that suite,
so the red was not seen until the next round's base measurement. The round-8
worker executed its order correctly; the fault is the reviewer's gate list.

Goal:
  Book round 8's FAIL, resolve `R-0771` (its fix is sound and independently
  verified), register `R-0772` for the red suite and REPAIR it. Then land the
  small T002c seam that was this round's original subject: the composed
  prompt REPORTS which segments it replaced instead of discarding the answer.

Bundle:
  C0a  save this block verbatim to `.agent/authored/f109-r9.md`
  C0b  mirror it to `.agent/last_block.md`
  C1   rewrite `.agent/plan.md` from SLICE PLAN
  C2   append SLICE RECORD, SLICE DONE and SLICE FINDING to
       `.agent/live_review.md`
  C3   repair the wiring guards (SPEC U) and append SLICE LANDED
  C4   `ComposedPrompt` carries the deduped names (SPEC Q) and both compose
       functions stop discarding them (SPEC R)
  C5   the cases of SPEC T in `tests/orchestration/test_semantic_dedupe.py`
  C6   rewrite `.agent/handoff.md`

Change set — these paths and no others:
  .agent/authored/f109-r9.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  tests/orchestration/test_prompt_trace.py
  packages/orchestration/prompt_segments.py
  packages/orchestration/pingpong_loop.py
  tests/orchestration/test_semantic_dedupe.py
  .agent/handoff.md

Constraints:
  1. SLICE PLAN, SLICE RECORD, SLICE DONE, SLICE FINDING and SLICE LANDED
     are applied BYTE FOR BYTE. Do not edit, rewrap, retype or improve them.
     C0a and C0b are `cp`.
  2. `.agent/live_review.md` ends WITHOUT a trailing newline at the base
     commit. Keep it that way. Nothing already in that file is edited,
     renumbered or deleted — in particular the `Landed: R-0771` line STAYS
     standing beside its new `Done:` paragraph, exactly as `R-0770`'s did.
  3. C1 lands before C2, C2 before C3, and the REPAIR (C3) lands before the
     new feature work (C4, C5). A red suite is fixed before anything is built
     on top of it.
  4. `manifest_as_dicts()` IS NOT TOUCHED and neither is
     `PromptSegmentManifestEntry`. The row keys stay exactly `name`, `rank`,
     `sha256`, `chars`, `tokens_estimated`. Gate G6 measures this directly,
     because two suites and a database schema depend on it.
  5. `packages/orchestration/prompt_trace.py` and
     `packages/orchestration/token_ledger.py` ARE NOT TOUCHED. They are not
     in the change set; if you believe one must change, stop and say so in
     the handback rather than changing it.
  6. In `pingpong_loop.py` only the edits SPEC R describes are permitted. Do
     NOT touch the resume-fallback recompositions round 8 landed, and do not
     "simplify" the two composition sites back into one — the second site is
     the `R-0771` repair and the guard SPEC U rewrites is what pins it.
  7. In `tests/orchestration/test_prompt_trace.py` only the two guard
     assertions SPEC U names are edited. No test is deleted, renamed or
     weakened, and no other assertion in that file changes.
  8. In `tests/orchestration/test_semantic_dedupe.py`, nothing already
     present is edited, reordered or deleted, with ONE named exception: the
     existing import statements may be EXTENDED. New cases go at the END.
     Reuse the existing fixtures rather than building another stack.
  9. Do NOT gate on `npm run lint` and do NOT gate on `ruff`. Follow ruff by
     construction: every new line under 120 characters, extended import
     lists in `order-by-type` isort order.
  10. Every pytest process uses `python3 -B`, and `__pycache__` is purged
      before every run of G5. G5's mutations run ONLY inside a disposable
      worktree, added and removed BY EXACT PATH, never in the primary
      checkout. Do not leave your shell's working directory inside a
      worktree you then remove.
  11. EVERY gate below — G1 through G7 — runs at C5 or earlier, so every
      reading the handback quotes already exists when C6 writes it. C6's own
      insertion count is NOT quoted anywhere in C6; the reviewer measures it.

SPEC U — repair the wiring guards (C3,
`tests/orchestration/test_prompt_trace.py`).

  Two tests are red: `test_the_builder_call_site_hands_its_composition_down`
  and `test_the_reviewer_call_site_hands_its_composition_down`. Each asserts

      assert source.count("<role>_composed = compose_<role>_prompt(") == 1

  and each now reads 2, because F109's `R-0771` repair added a SECOND,
  CORRECT composition inside the resume-fallback branch. The guard's PURPOSE
  — proving the call site hands its composition down to `build_trace_entry`
  — is untouched by that and must be KEPT. Only the arity claim is stale.

  In each of the two tests, replace that single assertion with an assertion
  that the count is 2, plus a SECOND assertion that pins WHY it is 2 rather
  than leaving a bare number that any future duplication would satisfy: take
  the source AFTER the fallback guard line
  `if <role>_resume_ref and <role>_out.error:` and assert that
  `<role>_composed = compose_<role>_prompt(` occurs in it. That way the guard
  says "one primary composition and one fallback recomposition", which is the
  real shape, instead of "some two".

  Add to each test's docstring one sentence naming F109 `R-0771` as the
  reason the count is 2: the resume fallback recomposes at full content
  because a fallback is not a resumed session. A reader who finds this guard
  after a future change must be able to tell which composition is which.

  Change NOTHING else in that file. In particular the
  `set(row) == {...}` manifest-key assertions stay exactly as they are.

SPEC Q — the field (C4, `packages/orchestration/prompt_segments.py`).

  `ComposedPrompt` gains ONE field, last, with a default so every existing
  construction keeps working untouched:

      deduped_names: tuple[str, ...] = ()

  Document it in the dataclass docstring: the names of the segments whose
  TEXT was replaced by a reference marker before composition, in the order
  they were replaced; empty for every composition that deduped nothing, which
  is every composition this module itself performs. Say plainly that
  `compose_prompt_segments` never sets it — this module has no opinion about
  dedupe and does not import it — and that F109's composition hook attaches
  it after the fact. DO NOT add it to `manifest_as_dicts()`; constraint 4 is
  that rule and this is the file where it would be easiest to break.

SPEC R — stop discarding the answer (C4, `pingpong_loop.py`). In BOTH
compose functions the tail currently reads:

      segments = registry.registered_segments()
      if dedupe_sent_hashes is not None:
          # ...comment...
          segments, _ = _dedupe_resumed_segments(
              segments, dedupe_sent_hashes, enabled=dedupe_enabled
          )
      return compose_prompt_segments(segments)

  It becomes, in both:

      segments = registry.registered_segments()
      deduped_names: tuple[str, ...] = ()
      if dedupe_sent_hashes is not None:
          segments, deduped_names = _dedupe_resumed_segments(
              segments, dedupe_sent_hashes, enabled=dedupe_enabled
          )
      return replace(compose_prompt_segments(segments), deduped_names=deduped_names)

  The existing comment explaining WHY the names were discarded is now false
  and is REPLACED by one saying they are reported on the composed prompt so a
  later reader can see what the model was not sent again, and that the
  manifest ROW shape is deliberately untouched because the `call_segments`
  table in `token_ledger.py` mirrors those keys column for column. `replace`
  is already imported in this module.

  The `deduped_names=` keyword is passed UNCONDITIONALLY, including when it
  is the empty tuple. A branch that only sets it "when something was deduped"
  would make the empty case take a different code path from the full one, and
  the empty case is the one every existing golden exercises.

SPEC T — the cases (C5, `tests/orchestration/test_semantic_dedupe.py`). Add
at the END. Use the existing helpers. These are MANDATORY:

  1. A composition that dedupes nothing reports `deduped_names == ()` —
     assert it for the BUILDER and for the REVIEWER, and for both the
     no-argument call and `dedupe_sent_hashes=None`.
  2. A composition that really dedupes reports exactly the names it replaced,
     in order. Build the sent set from a first composition's own recorded
     manifest through a real `SessionSentIndex`, as round 7's cases do.
  3. For EVERY name in `deduped_names`, that segment's entry in the second
     composition's manifest has a `chars` value equal to
     `len(dedupe_marker_for_segment(name))` — which pins the reported name to
     the segment that actually shrank, rather than to a name the caller could
     have invented. Assert also that every reported name appears in the
     manifest at all.
  4. A segment NOT in `deduped_names` kept its original `sha256` between the
     two compositions. This is the negative half of case 3, and the two
     together are what make the report trustworthy.
  5. The composed prompt a RESUMED chain produces through the real loop
     reports a non-empty `deduped_names`, and one from a chain that never
     resumes reports `()`. Reuse the existing chain fixtures; if reaching the
     composed object from a run is not possible without touching code outside
     the change set, say so and leave this case out rather than widening the
     change set.

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

Round 9, session 2 — a REPAIR round. Round 8 is booked FAIL: its
`R-0771` fix added a second, correct composition site and turned two
arity guards in `tests/orchestration/test_prompt_trace.py` red, which the
round's gate list never ran. `R-0771` resolves, `R-0772` is registered
for the red suite and repaired by rescoping both guards to the real shape
— one primary composition and one fallback recomposition. On top of that,
`ComposedPrompt` gains a `deduped_names` field so a composed prompt
reports which segments it replaced. The manifest ROW keys stay closed.

## Next Steps

- The config kill switch: a `run_pingpong` parameter forwarded to both
  compose calls as `dedupe_enabled`, proven by a resumed chain in which
  only the flag changed the outcome.
- Surface the deduped names into the prompt trace, answering the
  `schema_v` question on its own evidence. The manifest row keys stay
  closed: the `call_segments` table in `token_ledger.py` mirrors them
  column for column, so widening them is a token-ledger change.
- The measurement fixture on a resumed fixture chain, with the savings
  recorded, plus the docs (T003).
- The integration gate, then the closure sequence.

## Risks

- A suite that no round gate names can go red without anyone seeing it.
  Every block from here names the suites its change set can REACH, not
  only the ones it expects to move.
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
Gate: F109 R8 — the round 8 entry. VERDICT FAIL, AND THE FAULT IS THE REVIEWER'S GATE LIST RATHER THAN THE ROUND'S EXECUTION, over the range `81a00635d1498dbb5eb9869bb5d2a6e3e836a9f9..5a63d277a487900c0ab562159ba91d2e42bc23b6`. EVERYTHING THE BLOCK ORDERED WAS DONE AND DONE WELL, and the reviewer re-ran all of it: transport is one digest across the reviewer's scratch original, the committed `.agent/authored/f109-r8.md` and its mirror, `d4fecd3d21b3a10e573e66fb5a84b20869a1d6fa98f9d207685c371ccdcdb1d8`; the `R-0771` repair works, proven by driving the real loop with a resume-failing builder at this commit, where the builder's three calls read fresh with no marker, resumed with one, and the FALLBACK with `resume=None` carrying none, against the pre-repair reading of that same probe where the third call carried the `builder_system` marker; the reviewer's own mutations in a disposable worktree gave control exit 0 at 109 passed, deleting the two builder recomposition statements exit 1 at 2 failed including `test_a_builder_resume_fallback_sends_full_content`, and deleting `dedupe_sent_hashes` from the builder compose call exit 1 at 3 failed; every commit is single-parent with insertions 381, 249, 14, 8, 53, 204 and 427, all under 500; the opcode comparison over `pingpong_loop.py` yields ZERO deletions; `Done:` stayed at 63 as ordered; and the round even closed a hole in the reviewer's own SPEC, which named two rebindings where the REVIEWER role needs three, because the string that provider receives is `reviewer_effective` and not `reviewer_prompt`. THE VERDICT IS STILL FAIL, FOR ONE REASON: THE BRANCH TIP SHIPS A RED SUITE. `python3 -m pytest tests/orchestration/test_prompt_trace.py -q` is exit 1 at 2 failed, 44 passed at this commit. `test_the_builder_call_site_hands_its_composition_down` and its reviewer twin assert `source.count("<role>_composed = compose_<role>_prompt(") == 1`, and the `R-0771` repair correctly added a SECOND composition in the resume-fallback branch, so both read 2. Measured across the branch by the reviewer: that count is 1 at `552bbd05`, at `7ab86528` and at `81a00635`, and 2 at `5a63d277` — so this round's own change set turned the suite red. THE ROUND COULD NOT HAVE SEEN IT: gate G6 named eight suites and that was not among them, and no other gate reads that file. THE CHECKLIST ITEM THAT WOULD HAVE CAUGHT IT IS §3 ITEM 7, which exists for precisely this — grep the suite for tests that COUNT a string over a whole file before ordering a change that adds that string — and the reviewer did not run it against a block whose entire purpose was to add a second call to a named function. A green round gate over a red branch is the outcome docs/agents/planner_reviewer_prompt.md §4 item 6 forbids a PASS from describing, so the verdict is FAIL, `LAST_REVIEWED_SHA` does not advance, and `R-0772` carries the repair.
SLICE RECORD

SLICE DONE — appended in the SAME commit, as its own paragraph after SLICE
RECORD. Append a blank line, then this text:
<<<SLICE DONE
Done: R-0771 — RESOLVED, AND THE RESOLUTION CARRIES THE REVIEWER'S CORRECTION OF ITS OWN FIX CLAUSE. THE FIX is in `packages/orchestration/pingpong_loop.py` at `1b7759b7`, pinned by `tests/orchestration/test_semantic_dedupe.py` at `54f8ffa9`: each role hoists its compose keyword arguments into one dict, and the `if <role>_resume_ref and <role>_out.error:` branch recomposes at full content before the retry, rebinding the composed prompt as well as the prompt string. THE REVIEWER VERIFIED THE FIX RATHER THAN THE REPORT, driving the real loop with a resume-failing builder at `5a63d277a487900c0ab562159ba91d2e42bc23b6`: three builder calls, fresh with no marker, resumed with one, and the fallback with `resume=None` carrying none. Removing the two recomposition statements in a disposable worktree turns `test_a_builder_resume_fallback_sends_full_content` red at exit 1, so the finding's stated resolution condition — a test that drives the real loop through a fallback and fails when that recomposition is removed — is MET. This resolution stands even though the round carrying it is booked FAIL: `R-0772` is a DIFFERENT defect, in a guard this fix made stale, and the fix itself is sound. THE CORRECTION, and it is load-bearing, so it is stated rather than left to be discovered. THE FIX CLAUSE NAMED TWO REBINDINGS AND THE REVIEWER ROLE NEEDS THREE. It said to rebind `<role>_composed` and `<role>_prompt`, and on the reviewer side the string the provider actually receives is `reviewer_effective`, built by `_reviewer_effective_prompt(reviewer_prompt)` and stored by `_finalize_call` as `fallback_prompt`; rebinding only the two named names would have left the marker in the bytes and repaired that role not at all. The clause was written from the builder's shape and generalised to both roles without re-reading the reviewer's — the §3 item 34 class, a file the order was written against but not read at the point the order touched it. The round 8 worker caught it, added the third rebinding on the authority of the clause's stated purpose rather than its letter, and declared it. The earlier paragraph is NOT rewritten, per §3 item 20. A SECOND READING THE FINDING DID NOT ASK FOR, taken because the same defect class could plausibly live at a third call site: the reviewer's BOUNDED PARSE RETRY calls `reviewer_provider.review(retry_prompt, ...)` with no `resume=` argument at all, and `retry_prompt` is built from `reviewer_prompt`, so a deduped prompt reaching it would be the same defect again. It is NOT reachable, and structurally rather than luckily: the fallback branch tests `<role>_resume_ref and <role>_out.error` and therefore catches EVERY error on a resumed call, rebinding `reviewer_prompt` to the full text before the parse-retry branch is evaluated; and when no resume ref is set, no dedupe ran and there is no marker to leak. Measured by driving the real loop with a reviewer forced malformed on the resumed round: the parse retry did not fire at all, the fallback did, and its call carried no marker. No id is minted for a defect that cannot occur.
SLICE DONE

SLICE FINDING — appended in the SAME commit, as its own paragraph after
SLICE DONE. Append a blank line, then this text:
<<<SLICE FINDING
- R-0772 — High, THE BRANCH TIP SHIPS A RED SUITE: TWO ARITY GUARDS IN `tests/orchestration/test_prompt_trace.py` STILL DEMAND ONE COMPOSITION SITE PER ROLE WHERE THE `R-0771` REPAIR CORRECTLY ADDED A SECOND. Found by the REVIEWER at F109 round 9 while taking the base measurement for that round's own gate list, which is one round later than it should have been found. `test_the_builder_call_site_hands_its_composition_down` and `test_the_reviewer_call_site_hands_its_composition_down` each assert `source.count("<role>_composed = compose_<role>_prompt(") == 1` over the whole of `pingpong_loop.py`. F109's `R-0771` repair added a second, CORRECT composition inside each role's resume-fallback branch, so both counts read 2 and `python3 -m pytest tests/orchestration/test_prompt_trace.py -q` is exit 1 at 2 failed, 44 passed. Measured by the reviewer across the branch: the count is 1 at `552bbd05`, `7ab86528` and `81a00635`, and 2 at `5a63d277`, so the reddening commit is F109's own. THE DEFECT IS THE REVIEWER'S, twice over: the round 8 block ordered a second call to a named function without running §3 item 7 against it — grep the suite for tests that COUNT that string over that WHOLE file — and its gate list then named eight suites, none of which reads `pingpong_loop.py` as source text. THE PRODUCTION CODE IS NOT AT FAULT and must not be changed to satisfy the guard: the second composition is the `R-0771` repair, and reverting it would re-open a High finding. Fix: rescope both guards rather than deleting them, per §3 item 7's own counter-measure — assert the count is 2 AND assert that a composition occurs in the source that FOLLOWS the fallback guard line `if <role>_resume_ref and <role>_out.error:`, so the guard states "one primary composition and one fallback recomposition" instead of a bare number any future duplication would satisfy. Not resolved until `tests/orchestration/test_prompt_trace.py` is green at exit 0 AND deleting the fallback recomposition turns one of the two rescoped guards red.
SLICE FINDING

SLICE LANDED — appended to `.agent/live_review.md` at C3, AFTER the guard
repair. It is one line. Append a blank line, then this text:
<<<SLICE LANDED
Landed: R-0772 — both wiring guards in `tests/orchestration/test_prompt_trace.py` now assert two composition sites per role and pin the second to the resume-fallback branch, in the commit this round's SPEC U ordered.
SLICE LANDED

Done when — the gates listed below. Run every one, record its REAL exit code
and output, and give each ONE line in the handback.

  G1 TRANSPORT. `sha256sum .agent/authored/f109-r9.md .agent/last_block.md`
     prints ONE digest twice, equal to the digest the delegation wrapper
     states. Report it. The chain compares the saved copy against its mirror
     and claims nothing about the emitted bytes.

  G2 THE PLAN. `cmp` `.agent/plan.md` against the SLICE PLAN text extracted
     mechanically from `.agent/authored/f109-r9.md` — no output, exit 0.
     `wc -l .agent/plan.md` strictly under 50. `grep -c '^## Goal'` is 1 and
     `grep -c '^## Next Steps'` is 1.

  G3 THE RECORD APPENDS.
     (a) For the C2 append: report the base byte count and sha256, the total
         appended length S after stripping any trailing newline, and confirm
         the arithmetic against the actual new size. Do the same for the C3
         append. Confirm the file still ends WITHOUT a trailing newline.
     (b) A SECOND, STRUCTURALLY DIFFERENT READER: split the whole file on
         blank-line boundaries into units; let N be the number of units the
         C2 append itself contains, COUNTED by your script and not taken from
         this block; assert the LAST N units at C2 equal the appended
         paragraphs IN ORDER.
     (c) NEGATIVE CONTROL on a scratch copy under `.remedy-wt/`, never on the
         tracked file: XOR-flip one byte lying inside the FIRST appended
         paragraph, confirm reader (b) REJECTS it, report the tracked file's
         sha256 before and after to show it did not move, and delete the
         scratch copy BY EXACT PATH.
     (d) COUNTS after C3: `grep -c '^Gate: F109 R8 — '` is 1;
         `grep -c '^Done: R-0771 — '` is 1 and `grep -c '^Done: R-[0-9]\{4\} — '`
         rose by exactly 1 from the base commit; `grep -c '^- R-0772 — '` is 1
         and `grep -c '^- R-[0-9]\{4\} — '` rose by exactly 1;
         `grep -c '^Landed: R-0772 — '` is 1 and `grep -c '^Landed: R-0771 — '`
         is STILL 1.

  G4 THE EDIT SHAPE IS THE ORDERED ONE. For `test_prompt_trace.py` at C3,
     `prompt_segments.py` and `pingpong_loop.py` at C4, and
     `test_semantic_dedupe.py` at C5, read the pre-commit and post-commit
     blobs with `git show <sha>:<path>` — never by writing either revision
     over the tracked file — and compare them as SEQUENCES OF LINES with
     `difflib.SequenceMatcher(..., autojunk=False)`. Report EVERY non-equal
     opcode with its position and its lines, and account for each one against
     an edit SPEC U, SPEC Q, SPEC R or constraint 8 names. For
     `test_prompt_trace.py` specifically, report the total number of lines
     DELETED: constraint 7 permits editing two assertions and two docstrings
     and nothing else, so a large deletion there is a red gate.

  G5 THE COLOUR: control green, and every mutation below red on its named
     case. In a disposable worktree added at the C5 commit BY EXACT PATH
     under `.remedy-wt/`. FIRST, before trusting any mutation, run with the
     worktree as cwd:
       python3 -B -c "import packages.orchestration.pingpong_loop as m; print(m.__file__)"
     and confirm the path is INSIDE the worktree. Purge `__pycache__` before
     every run.
     (a) CONTROL, unmutated: run BOTH
         `python3 -B -m pytest tests/orchestration/test_semantic_dedupe.py -q`
         and `python3 -B -m pytest tests/orchestration/test_prompt_trace.py -q`.
         Both exit 0; report both passed counts.
     (b) MUTATION A — THE REGRESSION PROOF FOR `R-0772`: delete the two
         recomposition statements from the BUILDER resume-fallback branch in
         `pingpong_loop.py`. Run `test_prompt_trace.py`. One of the two
         rescoped guards must go RED. If that suite stays green, the guard
         was rescoped to a bare number and the gate has FAILED — report it as
         such rather than moving on.
     (c) MUTATION B — in the BUILDER compose function, drop the
         `deduped_names=deduped_names` keyword. Run
         `test_semantic_dedupe.py`. The failure set must INCLUDE SPEC T
         case 2.
     Before each mutation, confirm the exact text you are changing occurs
     EXACTLY ONCE in the file you are changing, and report that count; where
     it occurs twice, quote a longer unique string and say which one you
     took. Restore the file between mutations from the C5 blob by exact path.
     Afterwards confirm the worktree is clean, remove it BY EXACT PATH, run
     `git worktree prune`, and report `git worktree list`.

  G6 THE ROW SHAPE IS UNCHANGED, AND THE SUITES. First the property
     constraint 4 exists for: compose any prompt through the real producer
     and report the KEY SET of a `manifest_as_dicts()` row. It must be exactly
     `name`, `rank`, `sha256`, `chars`, `tokens_estimated` and nothing more,
     because `tests/orchestration/test_prompt_segments.py` asserts that set
     exactly and the `call_segments` table in `token_ledger.py` mirrors it
     column for column. Then run these suites SERIALLY, never two pytest
     processes alive at once, reporting each exit code and passed count. The
     count in parentheses is the REVIEWER's reading at the base commit —
     note that `test_prompt_trace.py` is RED there and MUST be green here:
       tests/orchestration/test_prompt_trace.py           (2 failed, 44 passed — MUST become exit 0)
       tests/orchestration/test_semantic_dedupe.py        (109)
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
     commit BEFORE C6, and confirm each is under 500. Take those numbers from
     `git show --numstat` and from nothing else. Compare the number you write
     in the handback's `## Commits` table, cell by cell, against the numstat
     output you quote here, and say in the handback that you did. Finally
     report the full `git diff --numstat` for
     `5a63d277a487900c0ab562159ba91d2e42bc23b6..` your last commit and confirm
     it lists exactly the change set above and nothing else.

Handback: rewrite `.agent/handoff.md`. It carries F109, ROUND 9, SESSION 2,
the branch, the commit table with subjects and its `+/-` column, the
changed-files table, ONE LINE PER GATE with its real result, the item-status
table over C0a–C6, every deviation, the open-findings count, and the next
expected action. There is no length cap. Push after C6.
