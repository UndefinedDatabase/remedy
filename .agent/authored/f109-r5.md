STEP T002a/5 — F109 Semantic dedupe (round 5, session 1)

Goal: book round 4's verdict, CORRECT a false load-bearing claim the
reviewer put into `R-0770` and RESOLVE that finding, then land T002a — the
pure dedupe DECISION: whether a given segment may be replaced by a marker,
and what that marker reads.

SCOPE RULE, quoted verbatim in every F109 order per the feature file's
Orchestrator brief: RESUMED SESSION ONLY, PROVEN SENDS ONLY.

Base commit: 2f25302e5c1e30f2d847c80a80458220702b1f52 (round 4 close, the
tip of `feature/f109-semantic-dedupe`, already pushed). Stay on that
branch: do NOT create a branch, do NOT open a pull request, do NOT merge.

Round 4's verdict was PASS, and it earned an unusual correction. Round 4's
worker proved the reviewer wrong about its own finding: the reviewer wrote
into `R-0770` that no assertion available today could separate a session
that was cleared-then-refilled from one that was never cleared, and the
worker's probe (d) came back RED, because a two-RUN comparison — a fallback
chain against a clean chain — separates them exactly. The reviewer
reproduced that independently. `R-0770`'s stated resolution condition is
therefore already met, and this round says so in the record rather than
leaving a false sentence standing.

Bundle (one commit per item, in this order):
  C0a. Save this entire step block verbatim to `.agent/authored/f109-r5.md`.
  C0b. Mirror it byte-for-byte to `.agent/last_block.md`.
  C1.  `.agent/plan.md` <- SLICE PLAN, whole-file replacement. FIRST
       substantive commit (§3 item 23 — this round touches the ledger).
  C2.  `.agent/live_review.md` <- SLICE RECORD, appended. TWO paragraphs:
       the round-4 gate entry, then the `Done:` resolution of `R-0770`
       which carries the correction.
  C3.  `packages/orchestration/session_sent_index.py` — ADD the constant
       and two functions of SPEC D below, and update the module docstring
       as SPEC D's last paragraph requires.
  C4.  `tests/orchestration/test_semantic_dedupe.py` — ADD the cases of
       SPEC E below. Change no existing test.
  C5.  `.agent/handoff.md` <- rewritten per AGENTS.md `### handoff.md`,
       reporting the REAL results of gates G1 through G6, every one of
       which runs at C4 or earlier.
  Then: `git push`. The push happens AFTER C5, so the handback does NOT
  quote its result; the reviewer measures the remote tip itself.

Exact change set for this round. These paths and NO others:
  `.agent/authored/f109-r5.md`   new
  `.agent/last_block.md`          rewritten
  `.agent/plan.md`                rewritten
  `.agent/live_review.md`         appended
  `packages/orchestration/session_sent_index.py`   added to
  `tests/orchestration/test_semantic_dedupe.py`    added to
  `.agent/handoff.md`             rewritten

Constraints:
  1. Apply every SLICE byte-for-byte. If a slice looks wrong, apply it
     anyway and DECLARE the problem in the handback's deviations.
  2. Touch no path outside the change set above. `pingpong_loop.py` is NOT
     edited this round: T002's wiring is the next round's work and this one
     ships only the decision it will call.
  3. The append is an append. `.agent/live_review.md` ends WITHOUT a
     trailing newline and must still do so afterwards: exactly the two
     bytes `\n\n` then the slice's bytes, any extractor-added trailing
     newline stripped first.
  4. C3 and C4 ADD to existing files. Nothing already in either file is
     edited, reordered or deleted, WITH ONE NAMED EXCEPTION: SPEC D's last
     paragraph orders the module docstring updated, which necessarily edits
     existing lines in `session_sent_index.py`. That exception is stated
     here so the two clauses agree — round 2 shipped a block in which they
     did not, and the worker had to spend a deviation on it.
     Place the new public names after `invalidate_on_resume_fallback` and
     BEFORE the private helpers `_segment_hashes_from_manifest` and
     `_evidence_hashes`, keeping the module's public-then-private layout.
  5. Production code is described by SPEC, not sliced: you AUTHOR it.
  6. The module stays PURE — no file read, no file write, no network, no
     provider call, and still no import from `packages.orchestration`. In
     particular do NOT import `PromptSegment` or anything else from
     `prompt_segments`: these functions take the segment's TEXT, NAME and
     HASH as plain values precisely so that the decision layer never
     depends on the composition layer it will be called from.
  7. No round of F109 gates on `ruff`: this session's reviewer cannot
     execute it. Follow the repository's ruff configuration by
     construction — line length 120, import groups as the file has them.
  8. Destructive verification (G4) runs ONLY inside a disposable
     `git worktree`, DISCARDED afterwards rather than reverted. Before
     trusting any mutation, FIRST print
     `packages.orchestration.session_sent_index.__file__` and confirm it
     resolves INSIDE the worktree: `remedy` is installed editable and a
     `.pth` puts the primary checkout on `sys.path`, so a run from the
     wrong directory silently tests the unmutated primary copy. Round 3
     found this hazard and round 4 confirmed it; it is a standing step.
  9. Every commit's insertion count stays under 500. Report one number per
     commit for C0a through C4 — that is SIX commits and therefore six
     numbers.
 10. The three property guards still sweep every `*.py` under
     `packages/orchestration/`: `test_no_shell_true_in_orchestration`,
     `test_no_0000_in_production` and
     `test_no_bad_permit_order_in_production`, in
     `tests/orchestration/test_test_runner.py`. None is a closed-set or
     count guard; these additions satisfy all three trivially.

SPEC D — one constant and two functions ADDED to
`packages/orchestration/session_sent_index.py`.

  WHY THIS EXISTS. The index knows what a session has already received.
  T002's composition hook will replace such a segment with a short
  reference marker. This round ships the DECISION and the MARKER TEXT as
  pure functions, so the hook that follows is mechanical and every rule
  about WHEN dedupe is allowed is unit-tested before it can reach a prompt.

  `DEDUPE_MIN_SEGMENT_CHARS` — int constant, value 200.
     The minimum segment length worth replacing. The feature file's
     edge-case section (A9) requires it: a marker has its own length, so
     replacing a tiny segment can cost more than it saves. Carry a comment
     saying exactly that, and naming the arithmetic: the marker for a
     typical segment name runs to roughly forty characters, so a floor of
     200 keeps the replacement worth making by a factor of several. It is
     a DEFAULT, not a law — both functions take an override.

  `dedupe_marker_for_segment(name)` -> str
     Return exactly `"[unchanged: " + name + ", previously provided]"` and
     nothing else — no trailing newline, no surrounding whitespace. The
     NAME stays in the marker deliberately, per the feature file's Design:
     the model must still be able to refer to the segment it is no longer
     being shown.
     Raise `SessionSentIndexError` when `name` is not a non-empty string
     after stripping. A nameless marker would tell the model that
     something it cannot identify was withheld, which is worse than
     sending the segment again.

  `should_dedupe_segment(text, sha256, sent_hashes, *, enabled=True,
   min_chars=DEDUPE_MIN_SEGMENT_CHARS)` -> bool
     The whole decision, in one place. Return True only when ALL of these
     hold, and False otherwise:
       - `enabled` is true. This is the config kill switch the feature
         file requires; when it is false the function returns False
         without consulting anything else, so disabling dedupe is
         provably total rather than mostly.
       - `sha256` is a non-empty string AND is present in `sent_hashes`.
         `sent_hashes` is any container supporting `in` — the frozenset
         `SessionSentIndex.sent_hashes()` returns is the intended caller.
       - `text` is a string of at least `min_chars` characters. The
         comparison is `len(text) >= min_chars`, so a segment of exactly
         `min_chars` IS deduped and one character fewer is not.
     RETURN FALSE RATHER THAN RAISING for a malformed `text` or `sha256` —
     a non-string of either kind reads as "do not dedupe". This differs
     deliberately from `record_call`, which raises on a malformed manifest,
     and the difference is worth a comment at the site: a bad record
     corrupts the index silently and must be loud, whereas a bad dedupe
     input has an obviously correct safe answer, which is to send the full
     content. Correctness before savings, as the feature's Goal says.

  Finally, UPDATE THE MODULE DOCSTRING. Its "deliberate absences" section
  currently ends with a bullet saying no prompt is rewritten here and that
  replacing an already-sent segment with a marker is F109 T002. That is now
  half true in the same way the fallback bullet was: the DECISION and the
  MARKER TEXT land here, and what remains absent is the composition hook
  that calls them and the config plumbing that supplies `enabled`. Reword
  that bullet to say exactly that, and add the three new names to the
  `Public API` list. Change nothing else in the docstring.

SPEC E — cases ADDED to `tests/orchestration/test_semantic_dedupe.py`.

  Hermetic and pure, in the style of the file's unit tests: no `tmp_path`,
  no network, no provider, no loop. Put them in their own class or classes.
  Reuse the file's existing helpers where they fit.

  These cases are mandatory:
   1. A segment that is enabled, long enough and whose hash is in the
      sent set IS deduped — the one True case.
   2. `enabled=False` returns False even when every other condition holds.
      This is the kill switch and it is the case that must never rot.
   3. A hash that is NOT in the sent set returns False.
   4. An empty `sent_hashes` returns False.
   5. BOUNDARY, both sides: text of exactly `DEDUPE_MIN_SEGMENT_CHARS`
      returns True, and text of exactly one character fewer returns False.
      Write these as two separate named cases, not one.
   6. A custom `min_chars` is honoured — pass a small override and show a
      short text deduping that the default would refuse.
   7. A non-string `text`, and a non-string or empty `sha256`, each return
      False and raise NOTHING. Parametrise over several bad values.
   8. `dedupe_marker_for_segment` returns the exact expected string for a
      known name — assert the whole string literally, not a substring.
   9. `dedupe_marker_for_segment` raises `SessionSentIndexError` for an
      empty name and for a whitespace-only name.
  10. THE THRESHOLD ACTUALLY GUARANTEES A SAVING: for a representative
      segment name, assert that
      `len(dedupe_marker_for_segment(name)) < DEDUPE_MIN_SEGMENT_CHARS`.
      This pins the constant against the marker it exists to justify, so a
      later change to either that destroys the saving fails here.
  11. END TO END WITH THE INDEX, no loop involved: record a manifest for a
      session through `record_call`, take `sent_hashes(session)`, and show
      that a segment whose hash is in that set and is long enough is
      deduped while a segment from the same manifest whose text is short
      is not. Build the manifest through the REAL producer with
      `_real_manifest_rows`, so the hashes are genuine segment hashes.

Done when — GATES. Run every one and record its REAL exit code and output.
"Green" as a word is a finding. G1 through G6 all run at C4 or earlier, so
C5 can quote every one. Report ONE LINE PER GATE in the handback.

  G1 TRANSPORT. `sha256sum .agent/authored/f109-r5.md .agent/last_block.md`
     — both equal to each other AND to `SHA256_OF_THIS_BLOCK` as stated in
     the delegation wrapper. Report the digest.

  G2 THE PLAN. At C1: `.agent/plan.md` byte-equal to SLICE PLAN by `cmp`
     against a scratch copy, never a retype; `wc -l` strictly under 50; one
     `## Goal` and one `## Next Steps`.

  G3 THE RECORD APPEND. At C2, over `.agent/live_review.md`:
     (a) BYTE ARITHMETIC. Size must be exactly 2036637 + 2 + S, where
         2036637 is the base size and S is the byte length of SLICE RECORD
         after stripping any trailing newline. Report all three. Base
         sha256
         cb8e452a71f2917e1cff20a4faac089cf30cad09cd9c80d948c2e9481a512fdb.
     (b) A SECOND, STRUCTURALLY DIFFERENT READER. Split the whole file on
         blank lines into units. COUNT the paragraphs in SLICE RECORD
         yourself — call that N — and assert the LAST N units equal those
         N paragraphs, IN ORDER.
     (c) NEGATIVE CONTROL. On a scratch copy, flip one byte inside the
         FIRST appended paragraph — not the last — and confirm reader (b)
         REJECTS it. Report the tracked sha256 before and after: identical.
     (d) COUNTS at C2: `^Done: R-[0-9]\{4\} — ` goes 62 to 63 and
         `^Done: R-0770 — ` is exactly 1; `^Gate: F109 R4 — ` is exactly 1;
         `^- R-[0-9]\{4\} — ` is UNCHANGED at 331, because this round
         registers no new finding; and `^Landed: R-` is UNCHANGED at 25 —
         the `Landed: R-0770` line STAYS beside its new `Done:` paragraph
         rather than being removed, which is this record's precedent for a
         landed fix that later earns its resolution.

  G4 THE COLOUR OF THE NEW DECISION. Inside a DISPOSABLE `git worktree`
     added at the C4 commit, never in the primary checkout. Apply
     constraint 8's `__file__` check FIRST and report the path. Purge
     `__pycache__` before every run and use `python3 -B`. Before each
     mutation confirm the text you are about to change occurs EXACTLY ONCE
     and report that count.
     (a) CONTROL, unmutated:
         `python3 -B -m pytest tests/orchestration/test_semantic_dedupe.py -q`
         Report the real exit code and passed count.
     (b) MUTATION A — make `should_dedupe_segment` ignore `enabled`.
         Re-run. It MUST fail, and the failure MUST include SPEC E case 2.
     (c) MUTATION B — restore, then change the length comparison from
         `>=` to `>`. Re-run. It MUST fail, and the failure MUST include
         the exactly-at-the-boundary case of SPEC E item 5.
     (d) MUTATION C — restore, then drop the hash-membership test so any
         hash counts as sent. Re-run. It MUST fail, and the failure MUST
         include SPEC E case 3.
     Report every exit code and the failing test names. Then
     `git worktree remove --force` by exact path and `git worktree prune`;
     report `git worktree list`. Four `.remedy-wt/job-*` worktrees pre-date
     this branch and must remain.

  G5 THE SUITES. At C4, run these SERIALLY — never two pytest processes
     alive at once — and report each real exit code and count. Base counts
     measured by the reviewer at the base commit:
       `python3 -m pytest tests/orchestration/test_semantic_dedupe.py -q`
                                                    base 55, must GROW
       `python3 -m pytest tests/orchestration/test_pingpong.py -q`  base 34
       `python3 -m pytest tests/orchestration/test_session_resume.py -q`
                                                                    base 27
       `python3 -m pytest tests/ui_server/ -q`                      base 515
       `python3 -m pytest tests/orchestration/test_test_runner.py -q` base 52
       `python3 -m pytest tests/regression/test_resource_safety.py -q` base 21
       `python3 -m pytest tests/orchestration/test_integrity_gate.py -q` base 16
       `python3 -m pytest tests/cli/test_golden_path.py -q`          base 42
     The four state readers are ordered because the round rewrites
     `.agent/` state, and they are run AS FOUR. This round changes no file
     under `docs/roadmap/`, so the docs-round gate is deliberately NOT
     ordered.

  G6 THE TREE. At C4: `git status --porcelain` EMPTY. `git ls-files
     .remedy-wt` returns nothing. Report the insertion count of each commit
     C0a through C4 — six numbers, each under 500. Additionally report
     `git diff --numstat` over the range for
     `packages/orchestration/pingpong_loop.py`: constraint 2 expects it to
     be absent from the range entirely.

Handback: rewrite `.agent/handoff.md` per AGENTS.md `### handoff.md`. It
carries the feature and round, the SESSION NUMBER — which is 1 — the
branch, the commit SHAs, a changed-files table, ONE LINE PER GATE with its
real result, the open-findings count, the deviations, and the next expected
action. It has no length cap. An item-status table covering C0a through C5
is mandatory: every item appears exactly once with status `done`, `skipped`
or `deviated`, and a reason for the latter two.

THIS IS THE LAST ROUND OF THE SESSION. The handback's "next expected
action" therefore states, for the session that follows: the reviewer's
round-5 verdict is booked into `.agent/live_review.md` in the FIRST commit
of that session's first round, and the build resumes at T002b — the
composition hook in `pingpong_loop.py` that calls
`should_dedupe_segment` and `dedupe_marker_for_segment`, with non-resume
calls bypassing it entirely under a byte-equality golden.

SLICE PLAN — whole-file replacement of `.agent/plan.md`.
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

Round 5, the last of session 1 — book round 4's PASS verdict, correct a
false load-bearing clause in `R-0770` and resolve that finding, and land
T002a: the pure dedupe DECISION in
`packages/orchestration/session_sent_index.py` —
`DEDUPE_MIN_SEGMENT_CHARS`, `should_dedupe_segment` and
`dedupe_marker_for_segment`. No prompt is rewritten yet and the loop is
not touched.

## Next Steps

- T002b: the composition hook in `packages/orchestration/pingpong_loop.py`
  that calls the decision, replaces a deduped segment's text with its
  marker while leaving rank and order untouched, and bypasses non-resume
  calls entirely under a byte-equality golden.
- T002c: record the deduped segments in the manifest so evidence shows
  what the model did NOT receive again, and plumb the config kill switch.
- T003: the measurement fixture and the docs.
- The integration gate, then the closure sequence.

## Risks

- The parse-retry and post-mortem provider calls are still NOT wired into
  the index. That records strictly less than was sent, which errs in the
  safe direction; T002b must not assume the index is complete.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
SLICE PLAN>>>

SLICE RECORD — appended to `.agent/live_review.md`, preceded by exactly two
newline bytes. Two paragraphs.
<<<SLICE RECORD
Gate: F109 R4 — the round 4 entry. VERDICT PASS, AND THE ROUND PROVED THE REVIEWER WRONG ABOUT THE REVIEWER'S OWN FINDING, WHICH IS THE BEST THING A ROUND CAN DO. THE ROUND'S SUBSTANCE: round 3's verdict was booked, `R-0770` was registered, and its repair landed — the chain tests now build TWO `FakeProvider` instances with DISTINCT `fake_session_id` values, so the Builder and Reviewer record seams are each pinned by a case naming its own session row. TRANSPORT: the reviewer's own pre-delegation original `.remedy-wt/f109-r4.md`, the committed `.agent/authored/f109-r4.md` and `.agent/last_block.md` all independently sha256'd at `7d62881a6c8ca7c7725c71f31e6751641f5719ff65f8817a0bb83c03580695fd`, copied rather than retyped. THE CHANGE SET CARRIES NO PRODUCTION CODE, exactly as constraint 2 required: `git diff --numstat` over the range names neither `packages/orchestration/pingpong_loop.py` nor `packages/orchestration/session_sent_index.py`, so the wiring reviewed at round 3 is byte-unchanged and only the tests that failed to prove it moved. THE TWO APPENDS RECONSTRUCT AS ONE CHAIN: the reviewer re-measured `.agent/live_review.md` at 2036637 bytes against base 2030395 plus two plus a 5817-byte RECORD slice plus two plus a 421-byte LANDED slice, counted N=2 and N=1 itself, confirmed the last three blank-line units equal RECORD's two paragraphs then LANDED's one IN ORDER, and ran its own negative control inside the FIRST appended paragraph, which the structural reader rejected while the tracked digest held. Counts moved exactly as ordered: findings 330 to 331 with `R-0770` present once, `Landed: R-` 24 to 25, and `Done:` UNMOVED at 62 — the worker wrote no resolution of its own, which is the rule that keeps an unreviewed fix looking like one. THE REPAIR WAS VERIFIED BY THE REVIEWER'S OWN MUTATIONS, in its own disposable worktree, with `packages.orchestration.pingpong_loop.__file__` confirmed to resolve inside that worktree before anything was trusted: the unmutated control is a real exit 0 at 55 passed; deleting the BUILDER `record_finalized_call` is exit 1 at 6 failed including `test_the_builder_seam_records_a_row_of_its_own` with `KeyError: 'sess-builder'` — the very mutation that came back GREEN at round 3, now caught; and deleting the BUILDER `invalidate_on_resume_fallback` is exit 1 at exactly 1 failed. THE SUITES ARE THE REVIEWER'S OWN, run serially, every one exit 0: 55, 34, 27, 515, 52, 21, 16 and 42. STRUCTURE: seven single-parent commits, insertions 322, 233, 13, 5, 156 and 3 for C0a through C4, all under 500; the change set is exactly the six ordered paths; `git status --porcelain` empty; remote tip equal to local at `2f25302e5c1e30f2d847c80a80458220702b1f52`. THE ROUND PASSES.

Done: R-0770 — RESOLVED, AND THE RESOLUTION CARRIES A CORRECTION OF THE FINDING'S OWN TEXT. THE FIX is in `tests/orchestration/test_semantic_dedupe.py` at `75de4b47`: `TestChainAgainstTheRealLoop` now builds two providers with distinct `fake_session_id` values, `sess-builder` and `sess-reviewer`, and each record seam is pinned by a case that names its own row. The reviewer verified the fix rather than the report, in its own disposable worktree at `2f25302e5c1e30f2d847c80a80458220702b1f52` with the imported module path confirmed first: deleting the Builder `record_finalized_call` now exits 1 at 6 failed, where the identical mutation at round 3 exited 0 at 51 passed. THE CORRECTION, and it is load-bearing, so it is stated rather than left to be discovered. `R-0770`'s own text asserted that the resume-fallback invalidation "remains unproven by any test", that "no assertion available today separates 'cleared then refilled' from 'never cleared'", and that the discriminator could not arrive before T002. THAT WAS FALSE WHEN IT WAS WRITTEN, and the round 4 worker demonstrated it by running the probe the finding said would be green. The reasoning held only for a SINGLE run, where the record following an invalidation does repopulate the session; it fails for a comparison of TWO runs, which is what round 3's own test already did. Measured by the reviewer at the commit named above: with the Builder `invalidate_on_resume_fallback` call present, the `sess-builder` row holds 8 hashes on a fallback chain against 9 on a clean chain, and with the call removed both read 9 — so `test_the_fallback_invalidation_shrinks_exactly_the_builder_row` fails, at exit 1 with `assert 9 < 9`, and it asserts in the same breath that the Reviewer row is UNCHANGED, which is the control that makes the shrinkage attributable to the seam that fell back rather than to the run differing at all. All four call sites are therefore discriminated today, and the finding's stated resolution condition — "not resolved until a test fails when the Builder `invalidate_on_resume_fallback` call is removed" — is MET. The earlier paragraph is NOT rewritten, per docs/agents/planner_reviewer_prompt.md §3 item 20: a dated correction beside a wrong sentence is how this record stays honest, and overwriting landed text would be worse. WHAT THE CLASS LEAVES BEHIND is the reviewer's own lesson rather than the fixture's: a claim that no test CAN distinguish two states is a universal over every possible test, which is not a thing a reviewer can measure, and the honest form is the one this round ran — name the probe, order it, and report the colour. The reviewer wrote the unmeasurable form into an append-only record and the worker caught it by executing it.
SLICE RECORD>>>
