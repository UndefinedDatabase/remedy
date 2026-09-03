── STEP T002b-ii — F109 Semantic dedupe, ROUND 7, SESSION 2 ───────────

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

Base commit: 7ab865280a44e1078feb320f5508cd1901cbb27d. Branch:
feature/f109-semantic-dedupe. Do not create a branch, do not switch
branch, do not create a PR, do not merge anything.

Goal:
  Book round 6's PASS verdict, then give `_dedupe_resumed_segments` its
  CALLERS: both compose functions gain a dedupe parameter that BYPASSES BY
  DEFAULT, and the two loop call sites supply the session's sent hashes
  ONLY when a resume ref is actually set. The byte-equality golden for the
  non-resume path is this round's first acceptance item, per the feature
  file's Acceptance section.

Bundle:
  C0a  save this block verbatim to `.agent/authored/f109-r7.md`
  C0b  mirror it to `.agent/last_block.md`
  C1   rewrite `.agent/plan.md` from SLICE PLAN
  C2   append SLICE RECORD to `.agent/live_review.md` and SLICE SLIP to
       `.agent/prose_slips.md`
  C3   the two compose functions gain the parameter (SPEC J)
  C4   the two loop call sites supply the hashes (SPEC K)
  C5   add the cases of SPEC L to `tests/orchestration/test_semantic_dedupe.py`
  C6   rewrite `.agent/handoff.md`

Change set — these paths and no others:
  .agent/authored/f109-r7.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  packages/orchestration/pingpong_loop.py
  tests/orchestration/test_semantic_dedupe.py
  .agent/handoff.md

Constraints:
  1. SLICE PLAN, SLICE RECORD and SLICE SLIP are applied BYTE FOR BYTE. Do
     not edit, rewrap, retype or improve them. C0a and C0b are `cp`.
  2. `.agent/live_review.md` and `.agent/prose_slips.md` both end WITHOUT a
     trailing newline at the base commit. Keep it that way. Nothing already
     in either file is edited, renumbered or deleted.
  3. C1 lands before C2, and C2 before C3.
  4. In `pingpong_loop.py` ONLY these edits are permitted, and no other line
     of that file changes:
       (a) the two parameter additions of SPEC J;
       (b) the two return-statement replacements of SPEC J;
       (c) the two call-site keyword additions of SPEC K.
     No import statement needs to change this round — `Container` and
     `_dedupe_resumed_segments` are already in scope at the base commit.
     Confirm that before you start, and if it turns out an import IS needed,
     add it and declare it.
  5. NO SIGNATURE BREAKS. Both new parameters are KEYWORD-ONLY and both
     carry defaults. Every existing caller of either compose function keeps
     working unchanged and composes BYTE-IDENTICAL bytes. `_build_builder_prompt`
     and `_build_reviewer_prompt` are NOT touched: they do not pass the new
     parameters, so they bypass, and that is the intended behaviour rather
     than an omission.
  6. In the test file, nothing already present is edited, reordered or
     deleted, with ONE named exception: the existing
     `from packages.orchestration.pingpong_loop import ...` statement may be
     EXTENDED. New cases go at the END of the file. Reuse the existing
     helpers `_real_manifest_rows`, `_registered_segments`, `_sha256_by_name`
     and the `TRANSFORM_*` constants; do not redefine any of them.
  7. Do NOT gate on `npm run lint` and do NOT gate on `ruff`. Follow ruff by
     construction: every new line under 120 characters, and any extended
     import list in the repo's `order-by-type` isort order.
  8. Every pytest process uses `python3 -B`, and `__pycache__` is purged
     before every run of G5. G5's mutations run ONLY inside a disposable
     worktree, added and removed BY EXACT PATH, never in the primary
     checkout.
  9. EVERY gate below — G1 through G7 — runs at C5 or earlier, so every
     reading the handback quotes already exists when C6 writes it. C6's own
     insertion count is NOT quoted anywhere in C6; the reviewer measures it.

SPEC J — the two compose functions (C3). Production code: described here,
written in the file's own idiom.

  `compose_builder_prompt` and `compose_reviewer_prompt` EACH gain two
  keyword-only parameters, placed last in their signature, immediately
  before the closing `) -> ComposedPrompt:`:

      dedupe_sent_hashes: Container[str] | None = None,
      dedupe_enabled: bool = True,

  `None` is the BYPASS and it is the default: when `dedupe_sent_hashes` is
  None the transform is not called at all, and the composed bytes are
  exactly what the base commit produced. That is what makes the golden in
  SPEC L provable rather than merely likely.

  Each function's final statement is currently, and identically in both:

      return compose_prompt_segments(registry.registered_segments())

  That exact line occurs EXACTLY TWICE in the file — confirm the count is 2
  before you change anything — and BOTH occurrences become:

      segments = registry.registered_segments()
      if dedupe_sent_hashes is not None:
          # F109 T002b: the replaced NAMES are discarded here on purpose.
          # ``ComposedPrompt`` carries text and manifest, and widening it to
          # carry the deduped names is T002c, which is the slice that needs
          # them. Threading a value no caller reads would be a second seam
          # to keep honest for a round with nothing to read it.
          segments, _ = _dedupe_resumed_segments(
              segments, dedupe_sent_hashes, enabled=dedupe_enabled
          )
      return compose_prompt_segments(segments)

  Document both parameters in each function's docstring in that file's own
  style: `dedupe_sent_hashes` is the set of segment hashes this session has
  PROVABLY already received, `None` meaning no dedupe at all; `dedupe_enabled`
  is the kill switch, and its config plumbing is still T002c.

SPEC K — the two call sites (C4). In `run_pingpong`, the builder composes
at the statement beginning `builder_composed = compose_builder_prompt(` and
the reviewer at `reviewer_composed = compose_reviewer_prompt(`. Add ONE
keyword argument to each call, keeping each under 120 characters:

  builder:
      dedupe_sent_hashes=(
          session_sent_index.sent_hashes(builder_resume_ref) if builder_resume_ref else None
      ),

  reviewer: the same, with `reviewer_resume_ref` in both places.

  THE CONDITION IS THE SCOPE RULE, in the only form that cannot drift: a
  call that is not resuming passes None and therefore cannot dedupe, and it
  is structurally impossible for it to do otherwise because there is no
  other value to pass. Put a short comment above each saying so, naming
  F109 T002b and the scope rule.

  Do NOT touch `record_finalized_call`, `invalidate_on_resume_fallback` or
  `result.session_sent_evidence`. Recording what was actually sent is
  already correct, and a deduped call really did send the marker.

SPEC L — the cases (C5). One new class at the end of the file, plus the
import extension. Build prompts through the real compose functions; use the
existing helpers. These cases are MANDATORY:

  THE GOLDEN — the feature file's first acceptance item, and the reason the
  default is None:
  1. For the BUILDER, over at least three different prompt shapes (vary
     `findings`, `safe_diff` and `round_number` so the shapes really differ),
     `compose_builder_prompt(...)` called with NO dedupe argument and called
     with `dedupe_sent_hashes=None` produce byte-identical `.text` AND equal
     manifests. Assert the manifests, not only the text.
  2. The same for the REVIEWER, over at least two shapes.
  3. `dedupe_sent_hashes=frozenset()` — empty but NOT None, so the transform
     really runs — also produces byte-identical `.text` to the no-argument
     call. This is the case that proves the bypass is about the DATA and not
     only about the None check.

  THE DEDUPE ACTUALLY FIRING:
  4. Compose a builder prompt once; build the sent set from THAT composition's
     own `manifest_as_dicts()` through a real `SessionSentIndex.record_call(...,
     ok=True)` and `sent_hashes(...)`; compose the SAME arguments again with
     that set. Assert at least one segment's text is now exactly
     `dedupe_marker_for_segment(<that segment's name>)`, that the second
     composition is strictly SHORTER, and that the manifest's NAMES and RANKS
     are unchanged between the two compositions.
  5. `dedupe_enabled=False` with that same full sent set produces text
     byte-identical to the no-dedupe composition. The kill switch again, now
     at the composition seam.

  THE SCOPE RULE AT THE CALL SITE — drive the REAL loop with `FakeProvider`
  in a tmp_path, in the style the existing `TestChainAgainstTheRealLoop`
  already uses; reuse its provider construction rather than inventing another:
  6. A chain with NO resume — providers that do not advertise resume support,
     or a run that never reaches a repair round — completes and NO composed
     prompt anywhere in it contains the marker prefix `[unchanged: `. Assert
     over the run's real recorded prompts, not over a re-composition.
  7. A RESUMED repair chain reaches a round whose composed prompt DOES carry
     at least one `[unchanged: ` marker, and the run still completes. If the
     fixture cannot be driven into that state with the providers this file
     already builds, do NOT fabricate it and do NOT weaken case 6: implement
     everything else, report exactly what you tried and what the run produced,
     and leave this case out with that explanation. A missing case honestly
     reported is a good outcome; a passing case that proves nothing is not.

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

Round 7, session 2 — book round 6's PASS verdict, then give the transform
`_dedupe_resumed_segments` its callers. `compose_builder_prompt` and
`compose_reviewer_prompt` each gain a keyword-only `dedupe_sent_hashes`
that defaults to None and bypasses entirely, plus a `dedupe_enabled` kill
switch; the two call sites in `run_pingpong` pass the session's sent
hashes only when a resume ref is actually set, so a non-resuming call has
no value it could dedupe with. The byte-equality golden for the
non-resume path is this round's first acceptance item.

## Next Steps

- Record the deduped segments in the manifest so evidence shows what the
  model did NOT receive again, and plumb the config kill switch through to
  `dedupe_enabled` (T002c).
- The measurement fixture on a resumed fixture chain, with the savings
  recorded, plus the docs (T003).
- The integration gate, then the closure sequence.

## Risks

- The parse-retry and post-mortem provider calls are still NOT wired into
  the index. That records strictly less than was sent, which errs in the
  safe direction; nothing may assume the index is complete.
- A deduped call records the MARKER's hash as sent, which is honest but
  not useful. T002c's manifest annotation is what makes the evidence
  readable; until then the marker hashes are harmless noise in the index.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
SLICE PLAN

SLICE RECORD — appended to `.agent/live_review.md`. It is one paragraph.
Append a blank line, then this text, and leave the file without a trailing
newline:
<<<SLICE RECORD
Gate: F109 R6 — the round 6 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ FROM THE HANDBACK, over the range `552bbd05ca3d458ef966b4d87157f62e917d444a..7ab865280a44e1078feb320f5508cd1901cbb27d`. TRANSPORT, AND THIS ROUND IT IS THE STRONGEST FORM AVAILABLE: `sha256sum` over the committed `.agent/authored/f109-r6.md`, its `.agent/last_block.md` mirror AND the reviewer's own scratch original printed one digest three times, `0debfaf9b922bb9620608bf726baa948b083fd01349020af65876d3df7cae7e7` — so the chain reaches back past the worker's own output to the file the reviewer wrote, which is the `cmp`-against-scratchpad proof docs/agents/planner_reviewer_prompt.md §4 item 9 names as primary, and it is stated here because the previous round could claim only the weaker two-artefact form. THE PRODUCTION CODE IS THE ROUND'S POINT AND IT IS SOUND: `_dedupe_resumed_segments` consults `enabled` first and alone; it takes each segment's sha256 from the SHIPPED PRODUCER via `compose_prompt_segments((segment,)).manifest[0].sha256` rather than recomputing one with `hashlib`, which is what makes a drift between the dedupe decision and the index that recorded those hashes impossible rather than merely unlikely, and composing one segment at a time keeps that correct for a duplicate segment NAME that a manifest-wide name lookup would have collapsed; only `text` is rewritten, through `dataclasses.replace`, so names and ranks survive by construction and the returned order is the INPUT order, never a rank sort. THE ABSENCE OF A CALLER IS THE ROUND'S SAFETY PROPERTY AND IT WAS MEASURED SEMANTICALLY: an `ast` walk of `packages/orchestration/pingpong_loop.py` at `7ab865280a44e1078feb320f5508cd1901cbb27d` finds 0 `ast.Call` nodes resolving to `_dedupe_resumed_segments` and exactly 1 `ast.FunctionDef` of that name, so the file is "defined and uncalled" rather than "absent", which a text count could not have distinguished and a docstring naming the function would have defeated. THE COLOUR IS THE REVIEWER'S OWN, run in a disposable worktree added at `7ab865280a44e1078feb320f5508cd1901cbb27d` by exact path and removed by exact path afterwards, with `packages.orchestration.pingpong_loop.__file__` confirmed to resolve INSIDE that worktree before any mutation was trusted: the unmutated control is a real exit 0 at 90 passed; deleting the `enabled` early return is exit 1 at 1 failed, `test_the_kill_switch_returns_every_segment_unchanged_and_no_names`; making the True branch append the segment unchanged is exit 1 at 5 failed including `test_a_long_already_sent_segment_becomes_its_marker_with_name_and_rank_kept`; deleting the replaced-name append is exit 1 at 7 failed including `test_the_replaced_names_are_exactly_the_replaced_segments_in_order`. THE TWO WIDE REDS ARE PRINCIPLED RATHER THAN COLLATERAL, which is why they are recorded instead of merely allowed: the kill-switch case asserts the SAME input deduped under the default before flipping the flag, so nothing but the flag differs, and that positive control is what a name-append mutation legitimately breaks — a discriminator doing its job. THE SUITES ARE THE REVIEWER'S OWN, run serially, every one exit 0, with the base count in parentheses: 90 (79), 25 (25), 36 (36), 39 (39), 34 (34), 27 (27), 52 (52) and 42 (42) — only the dedupe suite moved, and `test_builder_prompt_golden.py` and `test_reviewer_prompt_golden.py` sitting exactly at their base counts are the positive evidence for the uncalled claim rather than decoration beside it. STRUCTURE: every commit in the range is single-parent, with insertions 355, 323, 21, 3, 67, 191 and 369 in that order, all under 500; the range's `git diff --numstat` lists the seven ordered paths and nothing else; `.agent/plan.md` is byte-equal to the authored slice at 48 lines; longest new lines are 119 and 101 against the configured 120; `git status --porcelain` is empty and the remote tip equals the local tip at `7ab865280a44e1078feb320f5508cd1901cbb27d`. THE ROUND'S ONE FAILED CLAUSE WAS THE REVIEWER'S, NOT THE WORKER'S: gate G4 demanded the line-level opcodes be `equal` and `insert` ONLY, while SPEC G and constraint 6 of that same block ordered three SINGLE-LINE import statements extended, which at line granularity can only ever surface as a `replace` — the clause was unmeetable for the round it was written for. The worker applied the SPEC, measured the opcodes and declared the contradiction rather than routing around it, and the measurement it reported is the one the reviewer reproduced: delete count 0 in both files, every `replace` accounted for by a named import extension. Nothing is wrong on disk, so no id is spent and the slip is booked in `.agent/prose_slips.md` per amend0827-process-diet rule 2. THE ROUND PASSES.
SLICE RECORD

SLICE SLIP — appended to `.agent/prose_slips.md`. It is one paragraph.
Append a blank line, then this text, and leave the file without a trailing
newline:
<<<SLICE SLIP
2026-09-03 · F109 R6 · The reviewer's own step block ordered gate G4 to prove that the line-level opcodes between the pre-commit and post-commit blobs of `packages/orchestration/pingpong_loop.py` and the test file were `equal` and `insert` ONLY, with no `replace`, while SPEC G and constraint 6 of that same block explicitly ordered three SINGLE-LINE import statements to be EXTENDED — and extending a one-line statement can only ever surface as a `replace` at line granularity, so the clause was unmeetable for every possible execution of the round it was written for. The worker applied the SPEC as ordered, measured the opcodes, reported a delete count of 0 in both files with every `replace` quoted and matched to a named import extension, and declared the contradiction instead of narrowing the SPEC to fit the gate. The checklist neighbours are §3 item 18, which reads an ordered recipe against the property it must establish, and §3 item 8, which reads a gate's expected VALUE against the code — neither was run against the block's own two halves here. Reviewer-prose contradiction between a gate and a SPEC of one block, nothing wrong on disk and the intended change landed; no R-id spent (amend0827-process-diet rule 2).
SLICE SLIP

Done when — the gates listed below. Run every one, record its REAL exit
code and output, and give each ONE line in the handback.

  G1 TRANSPORT. `sha256sum .agent/authored/f109-r7.md .agent/last_block.md`
     prints ONE digest twice, equal to the digest the delegation wrapper
     states. Report it. The chain compares the saved copy against its mirror
     and claims nothing about the emitted bytes.

  G2 THE PLAN. `cmp` `.agent/plan.md` against the SLICE PLAN text extracted
     mechanically from `.agent/authored/f109-r7.md` — no output, exit 0.
     `wc -l .agent/plan.md` strictly under 50. `grep -c '^## Goal'` is 1 and
     `grep -c '^## Next Steps'` is 1.

  G3 THE TWO APPENDS, at C2.
     (a) For `.agent/live_review.md`: report the base byte count and sha256,
         the slice length S after stripping any trailing newline, and confirm
         base + 2 + S equals the actual new size. Confirm the file still ends
         WITHOUT a trailing newline.
     (b) A SECOND, STRUCTURALLY DIFFERENT READER over that file: split the
         whole file on blank-line boundaries into units; let N be the number
         of units the SLICE RECORD itself contains, COUNTED by your script
         and not taken from this block; assert the LAST N units equal the
         slice's paragraphs IN ORDER.
     (c) NEGATIVE CONTROL on a scratch copy under `.remedy-wt/`, never on the
         tracked file: XOR-flip one byte lying inside the FIRST appended
         paragraph, confirm reader (b) REJECTS it, report the tracked file's
         sha256 before and after to show it did not move, and delete the
         scratch copy BY EXACT PATH.
     (d) COUNTS in `.agent/live_review.md`: `grep -c '^Gate: F109 R6 — '` is
         1; `grep -c '^- R-[0-9]\{4\} — '`, `grep -c '^Done: R-[0-9]\{4\} — '`
         and `grep -c '^Landed: R-'` are each UNCHANGED from the base commit.
         No finding is registered or resolved this round.
     (e) For `.agent/prose_slips.md`: confirm the base bytes are a byte-exact
         PREFIX of the new file, that it still ends without a trailing
         newline, and that the count of lines matching `^2026-` rose by
         exactly 1.

  G4 THE EDIT SHAPE IS THE ORDERED ONE. For `pingpong_loop.py` at C3 and C4
     and for the test file at C5, read the pre-commit and post-commit blobs
     with `git show <sha>:<path>` — never by writing either revision over the
     tracked file — and compare them as SEQUENCES OF LINES with
     `difflib.SequenceMatcher(..., autojunk=False)`. Report EVERY non-equal
     opcode with its position and its lines. The requirement is not a shape:
     it is that every non-equal opcode is ACCOUNTED FOR by an edit constraint
     4 or constraint 6 names — the two parameter additions, the two return
     replacements, the two call-site additions, the test import extension and
     the test append — and that NOTHING ELSE appears. State the mapping opcode
     by opcode. Report the delete count separately; outside the replacements
     named above it must be 0.

  G5 THE COLOUR OF THE WIRING: control green, all three mutations red on the
     named cases. In a disposable worktree added at the C5 commit BY EXACT
     PATH under `.remedy-wt/`. FIRST, before trusting any mutation, run with
     the worktree as cwd:
       python3 -B -c "import packages.orchestration.pingpong_loop as m; print(m.__file__)"
     and confirm the path is INSIDE the worktree — an editable install can
     otherwise shadow it and every colour would be a reading of the wrong
     file. Purge `__pycache__` before every run. The command each time is:
       python3 -B -m pytest tests/orchestration/test_semantic_dedupe.py -q
     (a) CONTROL, unmutated: exit 0, and report the passed count.
     (b) MUTATION A — remove the `is not None` guard so the transform runs
         unconditionally. The failure set must INCLUDE a SPEC L golden case
         (1, 2 or 3). This is the mutation that proves the golden can fail.
     (c) MUTATION B — at the BUILDER call site, drop the conditional and pass
         `session_sent_index.sent_hashes(builder_resume_ref or "")`
         unconditionally. The failure set must INCLUDE SPEC L case 6, the
         non-resume chain. If case 6 was implemented but case 7 was not, this
         mutation is still required and still must redden case 6.
     (d) MUTATION C — make `dedupe_enabled` default to False. The failure set
         must INCLUDE SPEC L case 4.
     Before each mutation, confirm the exact text you are changing occurs
     EXACTLY ONCE in `packages/orchestration/pingpong_loop.py`, and report
     that count; where it occurs twice, quote a longer unique string and say
     which one you took. Restore with `git checkout --
     packages/orchestration/pingpong_loop.py` between mutations. Afterwards
     confirm the worktree is clean, remove it BY EXACT PATH with
     `git worktree remove --force <path>`, run `git worktree prune`, and
     report `git worktree list`. A wider red than ordered is fine — report
     it; a MISSING named case is a failure of the gate.

  G6 THE SUITES. Run these SERIALLY, never two pytest processes alive at
     once, and report each exit code and passed count. The count in
     parentheses is what the REVIEWER measured at the base commit; state
     yours beside it. Only the first is expected to move, and only upward —
     EVERY OTHER COUNT MUST BE IDENTICAL, and the two prompt goldens are the
     ones that matter, because they are what proves the default really
     bypasses:
       tests/orchestration/test_semantic_dedupe.py        (90)
       tests/orchestration/test_prompt_segments.py        (25)
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
     `git show --numstat` and from nothing else: a full-file rewrite's line
     counts before and after are NOT its numstat columns. Compare the number
     you write in the handback's `## Commits` table, cell by cell, against
     the numstat output you quote here, and say in the handback that you did.
     Finally report the full `git diff --numstat` for
     `7ab865280a44e1078feb320f5508cd1901cbb27d..` your last commit and confirm
     it lists exactly the change set above and nothing else.

Handback: rewrite `.agent/handoff.md`. It carries F109, ROUND 7, SESSION 2,
the branch, the commit table with subjects and its `+/-` column, the
changed-files table, ONE LINE PER GATE with its real result, the item-status
table over C0a–C6, every deviation, the open-findings count, and the next
expected action. There is no length cap. Push after C6.
