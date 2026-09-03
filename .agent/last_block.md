── STEP T002b-iii — F109 Semantic dedupe, ROUND 8, SESSION 2 ──────────

Scope rule, quoted verbatim as every F109 order requires: RESUMED SESSION
ONLY, PROVEN SENDS ONLY.

Base commit: 81a00635d1498dbb5eb9869bb5d2a6e3e836a9f9. Branch:
feature/f109-semantic-dedupe. Do not create a branch, do not switch
branch, do not create a PR, do not merge anything.

Goal:
  Book round 7's PASS verdict, REGISTER the defect that round surfaced as
  `R-0771`, and FIX it: a resume FALLBACK is not a resumed session, so it
  must carry FULL content. Today it re-sends the prompt that was composed
  for the resumed session, markers and all, to a session that never
  received the originals — and then records that deduped manifest as what
  was sent. Both halves are repaired by one rebinding. Also retire the
  `_dedupe_resumed_segments` docstring's claim that it has no caller.

  THE DEFECT IS THE REVIEWER'S, NOT THE ROUND 7 WORKER'S. Round 7's SPEC K
  wired the call sites and forbade touching the fallback path; the worker
  obeyed, found this anyway, and declared it. It is registered because it
  has product effect, not because anyone executed badly.

Bundle:
  C0a  save this block verbatim to `.agent/authored/f109-r8.md`
  C0b  mirror it to `.agent/last_block.md`
  C1   rewrite `.agent/plan.md` from SLICE PLAN
  C2   append SLICE RECORD and SLICE FINDING to `.agent/live_review.md`,
       and SLICE SLIP to `.agent/prose_slips.md`
  C3   the fallback repair in `packages/orchestration/pingpong_loop.py`
       (SPEC M), plus the docstring retirement of SPEC N
  C4   the cases of SPEC O in `tests/orchestration/test_semantic_dedupe.py`,
       and the `Landed:` line of SPEC P in `.agent/live_review.md`
  C5   rewrite `.agent/handoff.md`

Change set — these paths and no others:
  .agent/authored/f109-r8.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  packages/orchestration/pingpong_loop.py
  tests/orchestration/test_semantic_dedupe.py
  .agent/handoff.md

Constraints:
  1. SLICE PLAN, SLICE RECORD, SLICE FINDING, SLICE SLIP and SLICE P are
     applied BYTE FOR BYTE. Do not edit, rewrap, retype or improve them.
     C0a and C0b are `cp`.
  2. `.agent/live_review.md` and `.agent/prose_slips.md` both end WITHOUT a
     trailing newline at the base commit. Keep it that way. Nothing already
     in either file is edited, renumbered or deleted.
  3. C1 lands before C2, and C2 before C3. The finding is REGISTERED at C2,
     before the fix exists — if this session dies mid-round the defect is
     still on the record.
  4. THE WORKER NEVER WRITES A `Done:` PARAGRAPH. SLICE P is a `Landed:`
     line and that is the only resolution marker this round may carry; the
     reviewer authors the `Done:` text at the next gate. This is
     docs/agents/planner_reviewer_prompt.md §4 item 4 and it is not
     negotiable even though the fix and the finding land together.
  5. In `pingpong_loop.py` ONLY the edits SPEC M and SPEC N describe are
     permitted. No other behaviour changes. In particular do NOT touch
     `invalidate_on_resume_fallback`, `record_finalized_call`,
     `_finalize_call`, the retry machinery, or either compose function's
     body.
  6. In the test file, nothing already present is edited, reordered or
     deleted, with ONE named exception: the existing import statements may
     be EXTENDED. New cases go at the END of the file. Reuse the existing
     `TestChainAgainstTheRealLoop` helpers — `_make_repo`, `_provider_pair`,
     `_run`, `_rows_by_session` and its fixtures — rather than building a
     second fixture stack.
  7. Do NOT gate on `npm run lint` and do NOT gate on `ruff`. Follow ruff by
     construction: every new line under 120 characters, extended import
     lists in `order-by-type` isort order.
  8. Every pytest process uses `python3 -B`, and `__pycache__` is purged
     before every run of G5. G5's mutations run ONLY inside a disposable
     worktree, added and removed BY EXACT PATH, never in the primary
     checkout. Do not leave your shell's working directory inside a
     worktree you then remove.
  9. EVERY gate below — G1 through G7 — runs at C4 or earlier, so every
     reading the handback quotes already exists when C5 writes it. C5's own
     insertion count is NOT quoted anywhere in C5; the reviewer measures it.

SPEC M — the fallback repair (C3). Production code: described here, written
in the file's own idiom. The same shape applies TWICE, once for the builder
and once for the reviewer; do both.

  Today the builder composes once, into `builder_composed` and
  `builder_prompt`, passing `dedupe_sent_hashes` when `builder_resume_ref`
  is set. When that resumed call errors, the fallback branch calls the
  provider again with `resume=None` and REUSES `builder_prompt` — which may
  carry `[unchanged: …]` markers. It then records
  `builder_composed.manifest_as_dicts()`, so the evidence claims marker
  hashes were sent when full text was.

  STEP 1 — make the argument list reusable. Hoist every keyword argument of
  the `compose_builder_prompt(` call into a local dict built immediately
  before it, named `builder_compose_args`, EXCEPT `dedupe_sent_hashes`,
  which stays at the call site because it is the one argument the two
  compositions must differ in. The two positional arguments stay positional.
  The call then reads:

      builder_composed = compose_builder_prompt(
          effective_goal, context, **builder_compose_args,
          dedupe_sent_hashes=(...unchanged expression and its comment...),
      )

  This is a pure refactor: the composed bytes must not move, and G6's prompt
  goldens are what proves they did not.

  A HAZARD THE REVIEWER HIT WHILE DRY-RUNNING THIS, so you do not have to:
  THE TWO CALL SITES DO NOT LAY OUT THEIR POSITIONAL ARGUMENTS THE SAME WAY.
  The builder passes `effective_goal, context,` on ONE line; the reviewer
  passes `effective_goal,` and `builder_out.summary,` on TWO. So "hoist every
  keyword argument" is not one textual operation applied twice — determine
  the positional/keyword boundary per call site by reading it. A hoist that
  sweeps `builder_out.summary,` into a `dict(...)` fails at RUN time, not at
  import time, with `ValueError: dictionary update sequence element #0 has
  length 1; 2 is required`, and only a test that actually drives the loop
  will catch it.

  STEP 2 — recompose at full content in the fallback. As the FIRST statements
  inside the `if builder_resume_ref and builder_out.error:` branch, before
  `_begin_stream_call` and before the retry:

      builder_composed = compose_builder_prompt(effective_goal, context, **builder_compose_args)
      builder_prompt = builder_composed.text

  with a comment naming F109 T002b and `R-0771` that says: a fallback is NOT
  a resumed session, so the scope rule forbids dedupe on it; the prompt is
  recomposed at full content because the fresh session never received the
  originals; and `builder_composed` is rebound TOO so the manifest recorded
  below describes what was actually sent rather than what the abandoned
  resumed attempt would have sent.

  Do the identical two steps on the reviewer side with
  `reviewer_compose_args`, `reviewer_composed`, `reviewer_prompt` and
  `reviewer_resume_ref`.

  WHY REBINDING BOTH NAMES IS THE WHOLE FIX, and worth stating so no one
  later "simplifies" it to one: `builder_prompt` is what the retry sends and
  what `_finalize_call` stores as `fallback_prompt`; `builder_composed` is
  what `record_finalized_call` reads the manifest from. One rebinding each
  makes the sent bytes, the stored prompt and the recorded evidence agree.

SPEC N — retire the stale claim (C3, same commit). The docstring of
`_dedupe_resumed_segments` still says NO CALLER EXISTS YET and names the
wiring as future work. It has had two callers since `60343048`. Replace that
paragraph's claim with the truth: both compose functions call it, each
behind a `dedupe_sent_hashes` parameter that bypasses by default, and what
remains absent is the config plumbing that supplies `enabled`, which is
T002c. Change nothing else in that docstring.

SPEC O — the cases (C4). Add to the END of the test file. The first is the
discriminator this whole round exists for.

  1. THE CASE THAT MUST NEVER ROT — a resume fallback sends FULL CONTENT.
     Drive the real loop with `_provider_pair(builder_resume_fails=True)`
     and `repair_rounds=2`, exactly as
     `test_a_failed_builder_resume_falls_back_within_the_same_round` does.
     Capture every prompt the BUILDER provider is actually called with,
     together with the `resume` argument of each call — wrap the provider's
     `build` so the real call still happens and the real run completes.
     Then assert:
       (a) the run reaches `final_status == "staged_review_passed"` and
           `result.rounds[1].builder_output.resume_fallback is True`, so the
           case is known to have exercised the fallback rather than passing
           vacuously;
       (b) NO call made with `resume=None` carries the substring
           `[unchanged: ` anywhere in its prompt;
       (c) at least one call made with a non-None `resume` DOES carry it —
           otherwise (b) would be satisfied by dedupe never firing at all,
           and the case would prove nothing.
     (c) is not optional decoration: it is what makes (b) a statement about
     the FALLBACK rather than about the feature being switched off.
  2. The same three assertions for the REVIEWER side. If the fixture cannot
     drive a reviewer resume failure — `_provider_pair` exposes
     `builder_resume_fails` and the reviewer provider is built without an
     equivalent — then EXTEND that helper with a `reviewer_resume_fails`
     parameter defaulting to False, which is an addition and breaks no
     existing caller. If that still cannot be made to work, leave this case
     out, say exactly what you tried, and do NOT weaken case 1.
  3. THE EVIDENCE AGREES WITH THE BYTES: in the same fallback run, every
     sha256 in the builder's recorded row corresponds to a segment of the
     prompt that was actually sent last for that session. State plainly in a
     comment how you established the correspondence; if the only honest form
     you can write is weaker than that sentence, write the weaker one and say
     so rather than overclaiming.
  4. A NON-FALLBACK resumed chain still dedupes — the property round 7
     landed must survive this repair. Reuse or extend round 7's own case
     rather than writing a third fixture.

SLICE P — appended to `.agent/live_review.md` at C4, AFTER the fix commits.
It is one line. Append a blank line, then this text, and leave the file
without a trailing newline:
<<<SLICE P
Landed: R-0771 — the fallback now recomposes at full content and rebinds the composed prompt, so the retry sends no marker and the recorded manifest describes the bytes that were sent; both roles, in the commit this round's SPEC M ordered.
SLICE P

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

Round 8, session 2 — book round 7's PASS verdict, register `R-0771` and
fix it. A resume FALLBACK is not a resumed session, yet the loop re-sent
the prompt composed for the resumed one, markers and all, into a session
that never received the originals, and then recorded that deduped
manifest as what was sent. Both roles recompose at full content inside
the fallback branch and rebind the composed prompt, so the sent bytes,
the stored fallback prompt and the recorded evidence agree. The stale
"no caller exists yet" claim in the transform's docstring is retired in
the same commit.

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
- The prompt TRACE entry is written before the provider call, so on a
  fallback it describes the resumed composition rather than the full one
  actually sent. The repair above fixes the sent bytes and the recorded
  manifest; the trace ordering is untouched and belongs with T002c's
  evidence work.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
SLICE PLAN

SLICE RECORD — appended to `.agent/live_review.md`. It is one paragraph.
Append a blank line, then this text, and leave the file without a trailing
newline:
<<<SLICE RECORD
Gate: F109 R7 — the round 7 entry. VERDICT PASS, AND THE ROUND'S BEST OUTPUT WAS A DEFECT IT WAS ORDERED NOT TO FIX, over the range `7ab865280a44e1078feb320f5508cd1901cbb27d..81a00635d1498dbb5eb9869bb5d2a6e3e836a9f9`. TRANSPORT, again the strongest form: one digest across the reviewer's own scratch original, the committed `.agent/authored/f109-r7.md` and its `.agent/last_block.md` mirror, `711f3a135f35671111975c4ec48456258156811389c6b7364e9e2db574573954`. THE WIRING IS THE ORDERED ONE: both compose functions take a keyword-only `dedupe_sent_hashes` defaulting to None and a `dedupe_enabled` kill switch, the None case skips the transform entirely, and both loop call sites pass the session's hashes only behind `if <role>_resume_ref`, so a call that is not resuming has no value it could dedupe with. THE BYPASS IS PROVEN RATHER THAN ASSERTED, and the reviewer proved it before ordering it: in a disposable worktree at the base commit the reviewer applied SPEC J itself and measured that `test_builder_prompt_golden.py` and `test_reviewer_prompt_golden.py` stayed at 36 and 39, that a no-argument composition is byte-identical to `dedupe_sent_hashes=None` AND to `frozenset()` with manifests equal, and that dedupe genuinely fires when the hashes are real — builder 529 characters to 227, reviewer 1582 to 219, names and ranks unchanged. THE SUITES ARE THE REVIEWER'S OWN, run serially, every one exit 0, base in parentheses: 105 (90), 25 (25), 36 (36), 39 (39), 14 (14), 34 (34), 27 (27) and 42 (42) — only the dedupe suite moved, and the two prompt goldens sitting exactly at base are the positive evidence for the bypass. STRUCTURE: every commit in the range is single-parent, insertions 357, 261, 16, 6, 46, 16, 267 and 445 in that order, all under 500; the range numstat lists the eight ordered paths and nothing else; the line-level opcode comparison over `pingpong_loop.py` yields ZERO deletions and eight non-equal opcodes that match the ordered edits pairwise across the two roles — two parameter insertions, two docstring insertions, two return replacements and two call-site insertions; `.agent/plan.md` is byte-equal to the authored slice at 44 lines; longest new lines are 119 and 102 against the configured 120; both appends leave the base bytes a byte-exact prefix and neither file gained a trailing newline; `git status --porcelain` empty and remote tip equal to local at `81a00635d1498dbb5eb9869bb5d2a6e3e836a9f9`. TWO THINGS THE WORKER GOT RIGHT THAT A LESSER ROUND WOULD HAVE GOT WRONG. FIRST, MUTATION B CAME BACK GREEN AND THE WORKER DIAGNOSED IT RATHER THAN REPORTING A COLOUR: the ordered mutation passed `sent_hashes(builder_resume_ref or "")` unconditionally, and `record_call` refuses an empty session id, so `sent_hashes("")` is permanently `frozenset()`, which composes byte-identical bytes to `None` — an EQUIVALENT MUTANT, unmeetable for every possible round, which the reviewer confirmed independently at this commit by both readings. The worker then ran a substitute discriminator of the same intent, using a session key the index can actually hold, and reddened exactly the non-resume chain case. That is the behaviour docs/agents/planner_reviewer_prompt.md §3 item 5 asks for, arriving from the worker instead of the reviewer. SECOND, IT FOUND `R-0771` AND LEFT IT ALONE, because SPEC K forbade touching the fallback path — the correct call, and the finding is registered beside this entry. THE REVIEWER REPRODUCED THAT DEFECT RATHER THAN ACCEPTING THE REPORT, driving the real loop with a resume-failing builder at this commit: the builder is called three times, first fresh with no markers, then with `resume='sess-builder'` carrying `[unchanged: builder_system, previously provided]`, and then AGAIN with `resume=None` still carrying that same marker. THE ROUND PASSES.
SLICE RECORD

SLICE FINDING — appended to `.agent/live_review.md` in the SAME commit as
SLICE RECORD, as its own paragraph after it. Append a blank line, then this
text, and leave the file without a trailing newline:
<<<SLICE FINDING
- R-0771 — High, A RESUME FALLBACK SENDS THE DEDUPED PROMPT INTO A SESSION THAT NEVER RECEIVED THE ORIGINALS, AND THEN RECORDS THAT MANIFEST AS WHAT WAS SENT. Found by the WORKER at F109 round 7 while executing that round's own order, declared in the handback as a recommended id rather than fixed, because SPEC K of that block forbade touching the fallback path; the defect is the REVIEWER'S, since SPEC K wired the call sites without reading the branch that reuses their output. F106 T002c gives a failed resume ONE fallback inside the same round: the loop calls the provider again with `resume=None`. That retry REUSES `<role>_prompt`, which F109 round 7 composed WITH dedupe because `<role>_resume_ref` was set — so a brand-new session receives `[unchanged: <segment>, previously provided]` for content it has never seen. Measured by the reviewer at `81a00635d1498dbb5eb9869bb5d2a6e3e836a9f9` by driving the real loop with a resume-failing builder and capturing every provider call: three builder calls, the first fresh and clean, the second with `resume='sess-builder'` carrying one marker, the THIRD with `resume=None` carrying that same marker — and the segment replaced is `builder_system`, the one that carries the safety rules about working only in staging and not touching the target repo, so the fallback call is the one that loses them. The scope rule the feature file states in every order — "resumed session only" — is violated by construction here, since a fallback is by definition not a resumed session. A SECOND HALF, same root cause: `record_finalized_call` reads `<role>_composed.manifest_as_dicts()` after the fallback, so the evidence records the MARKER hashes as sent when the retry actually sent, or should have sent, full text. Fix: inside the `if <role>_resume_ref and <role>_out.error:` branch, before the retry, recompose the prompt with NO dedupe and rebind BOTH `<role>_composed` and `<role>_prompt`, so the bytes sent, the `fallback_prompt` stored by `_finalize_call` and the manifest read by `record_finalized_call` all describe the same call. Not resolved until a test drives the real loop through a fallback and fails when that recomposition is removed.
SLICE FINDING

SLICE SLIP — appended to `.agent/prose_slips.md`. It is one paragraph.
Append a blank line, then this text, and leave the file without a trailing
newline:
<<<SLICE SLIP
2026-09-03 · F109 R7 · The reviewer's own step block ordered gate G5 mutation B to pass `session_sent_index.sent_hashes(builder_resume_ref or "")` unconditionally at the builder call site and required the non-resume chain case to go red, but `SessionSentIndex.record_call` refuses a call whose session id is empty, so `sent_hashes("")` is permanently `frozenset()` and an empty container composes byte-identical bytes to `None` — the ordered mutation was an EQUIVALENT MUTANT and no run of it could ever have produced the demanded colour. The checklist item this breaks is §3 item 5, which permits a mutation red-proof only where the mutated branch is reachable by the tests meant to redden, and the reviewer had in fact measured the `frozenset()` equivalence itself during the pre-emission dry run without connecting it to the mutation it invalidated. The worker diagnosed the equivalence inside the mutated worktree, reported the green honestly instead of reporting a colour, and ran a substitute discriminator of the same intent using a session key the index can hold, which reddened exactly the intended case. Reviewer-prose defect in a gate, nothing wrong on disk and the intended property still discriminated; no R-id spent (amend0827-process-diet rule 2).
SLICE SLIP

Done when — the gates listed below. Run every one, record its REAL exit
code and output, and give each ONE line in the handback.

  G1 TRANSPORT. `sha256sum .agent/authored/f109-r8.md .agent/last_block.md`
     prints ONE digest twice, equal to the digest the delegation wrapper
     states. Report it. The chain compares the saved copy against its mirror
     and claims nothing about the emitted bytes.

  G2 THE PLAN. `cmp` `.agent/plan.md` against the SLICE PLAN text extracted
     mechanically from `.agent/authored/f109-r8.md` — no output, exit 0.
     `wc -l .agent/plan.md` strictly under 50. `grep -c '^## Goal'` is 1 and
     `grep -c '^## Next Steps'` is 1.

  G3 THE APPENDS.
     (a) For `.agent/live_review.md` at C2: report the base byte count and
         sha256, the total slice length S after stripping any trailing
         newline, and confirm the arithmetic against the actual new size.
         Confirm the file still ends WITHOUT a trailing newline.
     (b) A SECOND, STRUCTURALLY DIFFERENT READER: split the whole file on
         blank-line boundaries into units; let N be the number of units the
         C2 append itself contains, COUNTED by your script and not taken
         from this block; assert the LAST N units equal the appended
         paragraphs IN ORDER.
     (c) NEGATIVE CONTROL on a scratch copy under `.remedy-wt/`, never on the
         tracked file: XOR-flip one byte lying inside the FIRST appended
         paragraph, confirm reader (b) REJECTS it, report the tracked file's
         sha256 before and after to show it did not move, and delete the
         scratch copy BY EXACT PATH.
     (d) COUNTS in `.agent/live_review.md` AFTER C4: `grep -c '^Gate: F109 R7 — '`
         is 1; `grep -c '^- R-[0-9]\{4\} — '` rose by exactly 1 from the base
         commit and `grep -c '^- R-0771 — '` is 1; `grep -c '^Landed: R-'`
         rose by exactly 1 and `grep -c '^Landed: R-0771 — '` is 1;
         `grep -c '^Done: R-[0-9]\{4\} — '` is UNCHANGED — this round
         resolves nothing, per constraint 4.
     (e) For `.agent/prose_slips.md`: confirm the base bytes are a byte-exact
         PREFIX of the new file, that it still ends without a trailing
         newline, and that the count of lines matching `^2026-` rose by
         exactly 1.

  G4 THE EDIT SHAPE IS THE ORDERED ONE. For `pingpong_loop.py` at C3 and for
     the test file at C4, read the pre-commit and post-commit blobs with
     `git show <sha>:<path>` — never by writing either revision over the
     tracked file — and compare them as SEQUENCES OF LINES with
     `difflib.SequenceMatcher(..., autojunk=False)`. Report EVERY non-equal
     opcode with its position and its lines, and account for each one against
     an edit SPEC M, SPEC N or constraint 6 names. SPEC M's step 1 is a
     hoist, so `replace` and `delete` opcodes ARE expected here and are not a
     finding — this gate asks that every one of them be ACCOUNTED FOR, not
     that any particular shape appear. Anything you cannot map to an ordered
     edit is a red gate: report it rather than explaining it away.

  G5 THE COLOUR OF THE REPAIR: control green, and every mutation below red
     on its named case. In a disposable worktree added at the C4 commit BY EXACT
     PATH under `.remedy-wt/`. FIRST, before trusting any mutation, run with
     the worktree as cwd:
       python3 -B -c "import packages.orchestration.pingpong_loop as m; print(m.__file__)"
     and confirm the path is INSIDE the worktree. Purge `__pycache__` before
     every run. The command each time is:
       python3 -B -m pytest tests/orchestration/test_semantic_dedupe.py -q
     (a) CONTROL, unmutated: exit 0, and report the passed count.
     (b) MUTATION A — THE REGRESSION PROOF, and the one that matters: delete
         the two recomposition statements SPEC M step 2 adds to the BUILDER
         fallback branch, restoring exactly the behaviour `R-0771` describes.
         The failure set must INCLUDE SPEC O case 1. If it does not, the fix
         is not pinned and the gate is RED regardless of what else passes.
     (c) MUTATION B — delete the `dedupe_sent_hashes` keyword from the
         BUILDER `compose_builder_prompt(` call, so dedupe never fires. The
         failure set must INCLUDE SPEC O case 1's assertion (c) — the one
         that requires a resumed call to carry a marker. This is what proves
         case 1 cannot pass by dedupe simply being off.
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
     parentheses is what the REVIEWER measured at the base commit; state
     yours beside it. Only the first is expected to move, and only upward —
     EVERY OTHER COUNT MUST BE IDENTICAL, and the two prompt goldens matter
     most, because SPEC M step 1 is a refactor of the call they cover:
       tests/orchestration/test_semantic_dedupe.py        (105)
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
     commit BEFORE C5, and confirm each is under 500. Take those numbers from
     `git show --numstat` and from nothing else. Compare the number you write
     in the handback's `## Commits` table, cell by cell, against the numstat
     output you quote here, and say in the handback that you did. Finally
     report the full `git diff --numstat` for
     `81a00635d1498dbb5eb9869bb5d2a6e3e836a9f9..` your last commit and confirm
     it lists exactly the change set above and nothing else.

Handback: rewrite `.agent/handoff.md`. It carries F109, ROUND 8, SESSION 2,
the branch, the commit table with subjects and its `+/-` column, the
changed-files table, ONE LINE PER GATE with its real result, the item-status
table over C0a–C5, every deviation, the open-findings count, and the next
expected action. There is no length cap. Push after C5.
