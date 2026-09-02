STEP T001b-ii/3 — F109 Semantic dedupe (round 3, session 1)

Goal: book round 2's verdict and one further reviewer prose slip, then wire
the finalized-call adapters into the real orchestration loop at all four
sites, so the index is finally fed by actual provider calls and forgets a
session the moment a resume falls back.

SCOPE RULE, quoted verbatim in every F109 order per the feature file's
Orchestrator brief: RESUMED SESSION ONLY, PROVEN SENDS ONLY.

Base commit: 4b14eb3e770a1885a73424faa0a25f7e0f237a32 (round 2 close, the
tip of `feature/f109-semantic-dedupe`, already pushed). Stay on that branch:
do NOT create a branch, do NOT open a pull request, do NOT merge anything.

Round 2's verdict was PASS. The reviewer re-ran all seven of its gates and
reproduced all three mutations itself. Nothing from round 2 is reopened.

THIS ROUND TOUCHES PRODUCTION ORCHESTRATION CODE — `pingpong_loop.py` is
the loop every real job runs. Every edit below is ADDITIVE. You change no
existing statement, no control flow, no prompt bytes and no provider call.
If any ordered edit cannot be made additively, STOP and declare it rather
than restructuring anything.

Bundle (one commit per item, in this order):
  C0a. Save this entire step block verbatim to `.agent/authored/f109-r3.md`.
  C0b. Mirror it byte-for-byte to `.agent/last_block.md`.
  C1.  `.agent/plan.md` <- SLICE PLAN, whole-file replacement. FIRST
       substantive commit (docs/agents/planner_reviewer_prompt.md §3
       item 23 — this round touches the finding ledger).
  C2.  `.agent/live_review.md` <- SLICE VERDICT, appended. The round-2
       gate entry.
  C3.  `.agent/prose_slips.md` <- SLICE SLIPS, appended. One dated line,
       recording a REVIEWER error in round 2's own block that damaged
       nothing on disk (AGENTS.md `### prose_slips.md`, operator amendment
       amend0827-process-diet rule 2 — no id, no severity, no correction
       round).
  C4.  `packages/orchestration/pingpong_loop.py` — the five additive edits
       of SPEC W below, and nothing else.
  C5.  `tests/orchestration/test_semantic_dedupe.py` — ADD the chain cases
       of SPEC C below. Change no existing test.
  C6.  `.agent/handoff.md` <- rewritten per AGENTS.md `### handoff.md`,
       reporting the REAL results of gates G1 through G7, every one of
       which runs at C5 or earlier.
  Then: `git push`. The push happens AFTER C6, so the handback does NOT
  quote its result; the reviewer measures the remote tip itself.

Exact change set for this round. These paths and NO others:
  `.agent/authored/f109-r3.md`   new
  `.agent/last_block.md`          rewritten
  `.agent/plan.md`                rewritten
  `.agent/live_review.md`         appended
  `.agent/prose_slips.md`         appended
  `packages/orchestration/pingpong_loop.py`        added to
  `tests/orchestration/test_semantic_dedupe.py`    added to
  `.agent/handoff.md`             rewritten

Constraints:
  1. Apply every SLICE byte-for-byte. If a slice looks wrong, apply it
     anyway and DECLARE the problem in the handback's deviations. Never
     silently repair a slice; never edit one to fit.
  2. Touch no path outside the change set above.
  3. BOTH appends are appends, never inserts or overwrites. Both
     `.agent/live_review.md` and `.agent/prose_slips.md` end WITHOUT a
     trailing newline at the base commit and must still end without one
     afterwards. Each append is exactly the two bytes `\n\n` followed by
     the slice's bytes, with any trailing newline your extractor adds
     stripped first.
  4. C4 is ADDITIVE ONLY, and this is the round's central safety rule. You
     ADD an import, ADD one dataclass field, ADD one local variable and ADD
     four call statements. You do not edit, reorder, reindent or delete any
     existing line of `pingpong_loop.py`. The ONLY permitted non-addition
     is that adding a name to the existing multi-line
     `from packages.orchestration...` import block may reflow that block —
     see SPEC W item 1, which prefers a NEW import statement precisely so
     that even this does not happen.
  5. Production code is described by SPEC, not sliced: you AUTHOR the
     Python in C4 and C5. Every behaviour named is mandatory and nothing
     beyond it may be added. In particular C4 adds NO new function, NO new
     class and NO branch of its own — the decision logic already shipped in
     round 2 and this round only calls it.
  6. `packages/orchestration/session_sent_index.py` is NOT in the change
     set and is not edited this round. If a call site appears to need a
     behaviour that module lacks, STOP and declare it; do not add it.
  7. No round of F109 gates on `ruff`: this session's reviewer cannot
     execute it, so such a gate would rest on your word alone. Follow the
     repository's ruff configuration by construction — line length 120,
     imports grouped `__future__`, stdlib, first-party, alphabetised
     within the first-party group.
  8. Destructive verification (G5) runs ONLY inside a disposable
     `git worktree`, DISCARDED afterwards rather than reverted. The
     primary checkout is never mutated.
  9. Every commit's insertion count stays under 500 (AGENTS.md DECISION
     F104 D1 — the `+` column only). Report one number per commit for C0a
     through C5 — that is SEVEN commits and therefore seven numbers.
 10. The three property guards still sweep every `*.py` under
     `packages/orchestration/`: `test_no_shell_true_in_orchestration`,
     `test_no_0000_in_production` and
     `test_no_bad_permit_order_in_production`, in
     `tests/orchestration/test_test_runner.py`. None is a closed-set or
     count guard; the additions satisfy all three trivially.

SPEC W — five additive edits to `packages/orchestration/pingpong_loop.py`.

  ANCHORS. The reviewer read this file at the base commit named above and
  measured every anchor there. Rounds 1 and 2 did not touch this file, so
  these readings are current. Each anchor is given as its SYMBOL TEXT with
  a line number beside it for orientation only — locate by the text, and if
  a line number disagrees with the text, TRUST THE TEXT and say so in the
  handback.

  1. THE IMPORT. Add a NEW top-level import statement in the first-party
     `from packages.orchestration...` block, in alphabetical position — the
     block runs from `artifact_summary` (line 33) through `rate_governor`
     (line 63) and beyond, so `session_sent_index` sorts after
     `run_manifest` and `scope_plan` if those are present and before any
     later name. Import exactly three names:
     `SessionSentIndex`, `invalidate_on_resume_fallback` and
     `record_finalized_call`. Write it as its own `from ... import (...)`
     statement so no existing import block is reflowed (constraint 4).

  2. THE EVIDENCE FIELD. In the `PingPongResult` dataclass (`class
     PingPongResult:`, line 111), ADD one field at the END of the field
     list, after the last existing field:

         #: F109 T001b: per-session sent-segment bookkeeping for semantic
         #: dedupe — one row per provider session, each carrying the segment
         #: hashes PROVEN delivered to it. Empty for every run that never
         #: resumed and for every provider that reports no session id.
         session_sent_evidence: list[dict] = field(default_factory=list)

     It MUST have a default so every existing construction site keeps
     working untouched. The reviewer confirmed at the base commit that
     nothing serialises this dataclass wholesale — there is no `asdict`
     call in `pingpong_loop.py` or `run_report.py` — so this field reaches
     evidence only where a caller reads it by name.

  3. THE INDEX ITSELF. Inside `run_pingpong` (`def run_pingpong(`, line
     2715), in the `try:` block that opens at line 3066, beside the
     existing initialisations `findings: list[ReviewFinding] = []`,
     `reviewer_out: ReviewerOutput | None = None` and
     `repair_triggered = False` (lines 3067-3069) and BEFORE the round loop
     `for round_num in range(1, max_rounds + 1):` (line 3071), add:

         session_sent_index = SessionSentIndex()

     One index per RUN, deliberately: it must outlive a round, because the
     whole point is what a LATER round may skip resending.

  4. THE BUILDER SITE. Two additions, in this order.
     (a) Immediately after the existing line `builder_out.resume_fallback =
         True` (line 3251), inside that same `if` body and at that same
         indentation, add a call to `invalidate_on_resume_fallback` passing
         `session_sent_index`, `builder_out`, and `builder_resume_ref or ""`
         as the third argument. THE THIRD ARGUMENT IS THE WHOLE POINT: at
         this line `builder_out` has just been REPLACED by the `resume=None`
         retry, so its own `resume_session_ref` is `""` and the id of the
         session that failed survives only in `builder_resume_ref`.
     (b) Immediately after the existing statement that assigns
         `builder_ctx = _finalize_call(` ... `ok=not bool(builder_out.error))`
         (lines 3255-3257), add two statements at that same indentation:
         a call to `record_finalized_call` passing `session_sent_index`,
         `builder_out` and `builder_composed.manifest_as_dicts()`; then
         `result.session_sent_evidence = session_sent_index.as_evidence_dicts()`.
         `builder_composed` is the `ComposedPrompt` assigned at line 3154
         and already used at line 3206; it is in scope here.

  5. THE REVIEWER SITE. The same two additions, mirrored.
     (a) Immediately after the existing line `reviewer_out.resume_fallback =
         True` (line 3548), add the `invalidate_on_resume_fallback` call
         with `reviewer_out` and `reviewer_resume_ref or ""`.
     (b) Immediately after the existing statement assigning
         `reviewer_final_ctx = _finalize_call(` ... `ok=not
         bool(reviewer_out.error))` (lines 3552-3554), add the
         `record_finalized_call` call with `reviewer_out` and
         `reviewer_composed.manifest_as_dicts()` — `reviewer_composed` is
         assigned at line 3424 and already used at line 3473 — followed by
         the same `result.session_sent_evidence` refresh.

  WHY THE ORDER WITHIN A ROUND IS INVALIDATE-THEN-RECORD, stated so it is
  not rediscovered as a bug: on the fallback path the resume failed, so the
  session's proven set is void and is cleared first; the replacement call
  then really did deliver full content to whatever session it reports, and
  recording that afterwards is correct rather than contradictory. The
  existing line order already produces this sequence, which is why both
  additions are appends after existing statements and no statement moves.

  DO NOT add any call inside the parse-retry path, the post-mortem path, or
  any other provider call this SPEC does not name. Those calls exist and
  wiring them is not this round's scope; leaving them unwired records
  strictly less than was sent, which errs in the safe direction.

SPEC C — chain cases ADDED to
`tests/orchestration/test_semantic_dedupe.py`.

  These are the first tests in this feature that run the REAL loop. Follow
  the established pattern in `tests/orchestration/test_session_resume.py`,
  which the reviewer read at the base commit: it defines an autouse fixture
  redirecting `REMEDY_DATA_DIR` to `tmp_path`, a `demo_repo` fixture
  building a minimal repo, and drives runs with
  `run_pingpong("Fix README", str(demo_repo), builder_provider=provider,
  reviewer_provider=provider, repair_rounds=2)` against
  `FakeProvider(fail_on_round=1, pass_on_round=2, supports_resume=True,
  fake_session_id="sess-1")`. Copy that shape — including both fixtures, so
  this file stays self-contained and writes nothing to the real data root.

  Put these in their own class so the existing pure unit tests stay pure,
  and say in that class's docstring that these cases run the real loop.

  These cases are mandatory:
   1. A resumed two-round chain populates the evidence: after the run,
      `result.session_sent_evidence` is non-empty, holds exactly one row,
      that row's `session_id` is `"sess-1"`, and its `sent_sha256` list is
      non-empty and sorted.
   2. Every hash in that row is a real segment hash: assert each entry is a
      64-character lowercase hex string.
   3. A provider that reports NO session id leaves the evidence EMPTY.
      Build `FakeProvider(fail_on_round=1, pass_on_round=2,
      supports_resume=True)` with no `fake_session_id` and assert
      `result.session_sent_evidence == []`. This is the proven-sends-only
      rule surviving contact with the loop.
   4. A single-round run that never resumes still records what it proved:
      assert the evidence is empty when the provider reports no session,
      and — with `fake_session_id` set — that it holds that one session.
      Whichever way it lands, ASSERT THE BEHAVIOUR THE CODE ACTUALLY HAS
      after you have run it once; do not guess, and state in the test name
      what it pins.
   5. THE FALLBACK CASE, and it is the one that matters. Drive a chain with
      `FakeProvider`'s test-only `resume_fails` override so the repair
      round's resume attempt errors and the loop takes its same-round
      fallback. Assert that the run still completes, that
      `resume_fallback` is true on that round's builder output, and that
      the evidence for the resumed session reflects the POST-fallback
      state rather than a stale pre-fallback set. Read
      `tests/orchestration/test_session_resume.py` for the exact spelling
      of the `resume_fails` override before writing this.
   6. THE LOOP IS OTHERWISE UNCHANGED: assert that a run with a
      non-resuming provider produces the same `final_status` and the same
      number of rounds as it did before this round's edits. Take those
      expected values from a real run, not from memory.

Done when — GATES. Run every one and record its REAL exit code and output.
"Green" as a word is a finding. G1 through G7 all run at C5 or earlier, so
C6 can quote every one. Report ONE LINE PER GATE in the handback.

  G1 TRANSPORT. `sha256sum .agent/authored/f109-r3.md .agent/last_block.md`
     — both must equal each other AND equal `SHA256_OF_THIS_BLOCK` as
     stated by the reviewer in the delegation wrapper. Report the digest.

  G2 THE PLAN. At C1: `.agent/plan.md` byte-equal to SLICE PLAN by `cmp`
     against a scratch copy, never a retype; `wc -l` strictly under 50; one
     `## Goal` heading and one `## Next Steps` heading.

  G3 THE VERDICT APPEND. At C2, over `.agent/live_review.md`:
     (a) BYTE ARITHMETIC. Size must be exactly 2024336 + 2 + S, where
         2024336 is the base size and S is the byte length of SLICE VERDICT
         after stripping any trailing newline your extractor added. Report
         all three numbers. Base sha256 is
         5dc6aeb1b8bccae8c8c7593aa4bc623ac5b0349e50db2fdcc68c449c56ec4d25.
     (b) A SECOND, STRUCTURALLY DIFFERENT READER. Split the whole file on
         blank lines into units. COUNT the paragraphs in SLICE VERDICT
         yourself — call that N — and assert the LAST N units equal those N
         paragraphs, in order.
     (c) NEGATIVE CONTROL. On a scratch copy, flip one byte inside the
         FIRST appended paragraph and confirm reader (b) REJECTS it. Report
         the tracked file's sha256 before and after: identical.
     (d) COUNTS. `grep -c` for `^Gate: F109 R2 — ` is exactly 1;
         `^- R-[0-9]\{4\} — ` is UNCHANGED at 330 and
         `^Done: R-[0-9]\{4\} — ` is UNCHANGED at 62 — this round
         registers no finding and resolves none.

  G4 THE SLIPS APPEND. At C3, over `.agent/prose_slips.md`: size must be
     exactly 41716 + 2 + S2, base sha256
     fae736593569c3dad97eb33d8ea9bb9b1c2494d77f5c47910bcad35b621ec3c6.
     Then the same blank-line reader: count N2 paragraphs in SLICE SLIPS
     yourself and assert the last N2 units equal them in order. Report both
     numbers and the reader's verdict.

  G5 THE COLOUR OF THE WIRING. Inside a DISPOSABLE `git worktree` added at
     the round's C5 commit, never in the primary checkout. Purge
     `__pycache__` before every run and use `python3 -B`. Before applying
     each mutation, confirm the exact text you are about to change occurs
     EXACTLY ONCE in the file you are changing, and report that count —
     a mutation that silently fails to land produces a false green.
     (a) CONTROL FIRST, unmutated:
         `python3 -B -m pytest tests/orchestration/test_semantic_dedupe.py -q`
         Record the real exit code and passed count.
     (b) MUTATION A — DELETE the builder `record_finalized_call` call added
         by SPEC W item 4(b). Re-run. It MUST fail, and the failure MUST
         include the SPEC C item 1 case, because with no builder recording
         the evidence for a resumed chain can no longer be populated.
     (c) MUTATION B — restore, then DELETE the builder
         `invalidate_on_resume_fallback` call added by SPEC W item 4(a).
         Re-run and report the result HONESTLY, whichever colour it is.
         If it stays GREEN, that is a real finding about SPEC C item 5 and
         you must say so plainly in the handback rather than adjusting
         anything: it would mean the fallback case as written does not
         actually discriminate, and the reviewer will handle it. Do NOT
         edit the test to make it red.
     Report every exit code and the failing test names for each mutation.
     Then `git worktree remove --force` by exact path and
     `git worktree prune`; report `git worktree list` afterwards. Four
     `.remedy-wt/job-*` worktrees pre-date this branch and must remain.

  G6 THE SUITES. At C5, run these SERIALLY — never two pytest processes
     alive at once — and report each real exit code and count. Base counts
     were measured by the reviewer at the base commit:
       `python3 -m pytest tests/orchestration/test_semantic_dedupe.py -q`
                                                    base 45, must GROW
       `python3 -m pytest tests/orchestration/test_pingpong.py -q`  base 34
       `python3 -m pytest tests/orchestration/test_session_resume.py -q`
                                                                    base 27
       `python3 -m pytest tests/orchestration/test_run_report.py -q` base 81
       `python3 -m pytest tests/ui_server/ -q`                      base 515
       `python3 -m pytest tests/orchestration/test_test_runner.py -q` base 52
       `python3 -m pytest tests/regression/test_resource_safety.py -q` base 21
       `python3 -m pytest tests/orchestration/test_integrity_gate.py -q` base 16
       `python3 -m pytest tests/cli/test_golden_path.py -q`          base 42
     The four state readers are ordered because the round rewrites
     `.agent/` state, and they are run AS FOUR. This round changes no file
     under `docs/roadmap/`, so the docs-round gate is deliberately NOT
     ordered. `test_pingpong.py`, `test_session_resume.py` and
     `test_run_report.py` are ordered because this round edits the loop
     they cover.

  G7 THE TREE. At C5: `git status --porcelain` EMPTY. `git ls-files
     .remedy-wt` returns nothing. Report the insertion count of each commit
     C0a through C5 — seven numbers, each under 500. Additionally report
     `git diff --numstat 4b14eb3e770a1885a73424faa0a25f7e0f237a32..` for
     `packages/orchestration/pingpong_loop.py` alone, with its DELETION
     count, which constraint 4 expects to be 0.

Handback: rewrite `.agent/handoff.md` per AGENTS.md `### handoff.md`. It
carries the feature and round, the SESSION NUMBER — which is 1 — the
branch, the commit SHAs, a changed-files table, ONE LINE PER GATE with its
real result, the open-findings count, the deviations, and the next expected
action. It has no length cap. An item-status table covering C0a through C6
is mandatory: every item appears exactly once with status `done`, `skipped`
or `deviated`, and a reason for the latter two.

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

Round 3 — book round 2's PASS verdict and one reviewer prose slip, then
land T001b-ii: wire the finalized-call adapters into
`packages/orchestration/pingpong_loop.py` at the builder and reviewer
finalized-call seams and at both resume-fallback sites, carry the result
on `PingPongResult.session_sent_evidence`, and prove it with the first
chain tests in this feature that drive the real loop. Every loop edit is
additive; no existing statement moves.

## Next Steps

- T002: the composition hook — a segment whose hash the session already
  holds becomes a one-line marker, with non-resume calls bypassing the
  hook entirely, asserted by a byte-equality golden.
- T003: the measurement fixture, the disable flag, and the docs.
- The integration gate, then the closure sequence.

## Risks

- The loop is production code every job runs. The wiring is additive and
  the round gates the three suites that cover it, but a regression here
  would reach real runs rather than only this feature.
- The parse-retry and post-mortem provider calls are deliberately NOT
  wired. That records strictly less than was sent, which errs in the safe
  direction; T002 must not assume the index is complete.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
SLICE PLAN>>>

SLICE VERDICT — appended to `.agent/live_review.md`, preceded by exactly
two newline bytes. One paragraph.
<<<SLICE VERDICT
Gate: F109 R2 — the round 2 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ FROM THE HANDBACK. THE ROUND'S SUBSTANCE: round 1's PASS verdict was booked into this record, two reviewer prose slips were appended to `.agent/prose_slips.md` without spending an id, and T001b-i landed the three finalized-call adapters — `session_id_of_finalized_call`, `record_finalized_call` and `invalidate_on_resume_fallback` — in `packages/orchestration/session_sent_index.py`, with the test file growing from 25 cases to 45. TRANSPORT HELD IN THE STRONGEST FORM AVAILABLE TO THIS WORKFLOW, and the chain is named rather than generalised, per docs/agents/planner_reviewer_prompt.md §3 item 37: the reviewer's own pre-delegation original `.remedy-wt/f109-r2.md`, the committed `.agent/authored/f109-r2.md` and the working `.agent/last_block.md` were all independently sha256'd at `ff5ef37aab57bcd49acb964921f8cdf07d740670a35260a94c9e323265d25907`, and the worker COPIED rather than retyped, so the bytes authored are the bytes that landed. THE PLAN SLICE WAS PROVED BYTE-EQUAL against the reviewer's own original at 42 lines, under the 50-line cap AGENTS.md sets, with a trailing-newline-stripped negative control printing False so the equality distinguishes rather than accepts. BOTH APPENDS WERE RECONSTRUCTED INDEPENDENTLY: `.agent/live_review.md` re-measured at 2024336 bytes against base 2018315 plus two separator bytes plus a 6019-byte slice, N counted by the reviewer itself as 1, the last unit byte-equal to the slice, and the reviewer's own negative control on the FIRST appended paragraph rejected while the tracked digest held; `.agent/prose_slips.md` re-measured at 41716 against base 40351 plus two plus 1363, N2 counted as 2, the last two units equal in order. Both files still end without a trailing newline, as constraint 3 required. THE LEDGER COUNTS MOVED EXACTLY AS ORDERED, which for a bookkeeping round means not at all: `^Gate: F109 R1 — ` is 1, findings stand at 330 and `Done:` at 62, both unchanged, because this round registered no finding and resolved none. THE THREE MUTATIONS WERE REPRODUCED BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE, on the tests the block named: the unmutated control was a real exit 0 at 45 passed; recording an errored call as proven failed exactly `test_an_errored_call_records_nothing_and_leaves_the_session_empty`; letting a non-mapping `usage_actuals` propagate failed exactly the two parametrisations of `test_a_non_mapping_usage_actuals_reads_as_no_session_and_never_raises`; and ignoring the `resumed_ref` argument failed three tests including `test_the_loops_replaced_output_invalidates_when_resumed_ref_is_passed`, which is the case that exists to prove the third argument load-bearing. That third mutation is the round's most valuable evidence and it earned its place: the reviewer independently re-read `packages/orchestration/pingpong_loop.py` and confirmed the premise the SPEC asserted — at the builder fallback the loop reassigns `builder_out` from a second `_call_with_retry` with `resume=None` and only then sets `resume_fallback = True`, and `PingPongProvider` sets `resume_session_ref` to `""` whenever `resume_used` is false, so that output genuinely cannot name the session that failed and an adapter reading only the output would invalidate nothing on precisely the path invalidation exists for. THE CODE WAS READ, NOT ONLY RUN: the module's import set is still only `__future__` and `collections.abc`, so its purity claim holds as written and no dependency on the provider layer was introduced by adapters whose whole job is to read provider objects; the new functions sit after `session_sent_index_from_evidence` and before the private helpers, keeping the public-then-private layout constraint 4 required; and neither guard is re-implemented at the adapter level, so each rule keeps exactly one site at which it can regress. THE SUITES ARE THE REVIEWER'S OWN, run serially: 45, 515, 52, 21, 16 and 42, every one exit 0 and every one identical to the base reading taken before delegation. STRUCTURE HELD: eight single-parent commits, insertions 372, 306, 15, 3, 5, 90 and 202 for C0a through C5 with the handback at 208, every one under 500; the change set is exactly the eight ordered paths; `git ls-files .remedy-wt` is empty; the primary checkout was confirmed unmutated after the mutation work with `git status --porcelain` empty and no MUTATION marker surviving; and the remote tip equals the local tip at `4b14eb3e770a1885a73424faa0a25f7e0f237a32`. FIVE DEVIATIONS WERE DECLARED AND ALL FIVE ARE ACCEPTED. The first is the REVIEWER'S OWN and is routed to `.agent/prose_slips.md` by this round's C3 rather than spending an id: the block's constraint 4 said nothing already in either file is edited, while SPEC A's final paragraph ordered the module docstring reworded, so two clauses of one block contradicted each other and the worker resolved it correctly in favour of the specific over the general and declared it. The second is not a deviation at all but a good decision reported as one — the test import was extended by adding three names INSIDE the existing parenthesised import, which is a pure insertion and left the file at 202 insertions and zero deletions. The third is one test beyond the eleven mandated, covering the output-object branch SPEC A specifies but no mandated case exercised; the production code contains exactly the three specified functions and nothing more, which the reviewer confirmed by reading the diff. The fourth is the sandbox bash guard again refusing a literal dollar sign in a quoted grep pattern, which the reviewer hit itself in round 1 and which the byte-equality proofs render moot. The fifth is the four pre-existing `.remedy-wt/job-*` worktrees, which the reviewer confirmed predate this branch and which are correctly left alone. THE ROUND PASSES. The open set stands at 268 — 330 findings minus 62 resolutions — and `.agent/candidates.md` remains EMPTY, so no block condition stands against F109.
SLICE VERDICT>>>

SLICE SLIPS — appended to `.agent/prose_slips.md`, preceded by exactly two
newline bytes. One paragraph.
<<<SLICE SLIPS
2026-09-03 · F109 R2 · The reviewer's own step block contradicted itself between two clauses: constraint 4 ruled that "Nothing already in either file is edited, reordered or deleted" for commits C4 and C5, while SPEC A's final paragraph ordered the `session_sent_index.py` module docstring reworded and three names added to its Public API list, which is an edit of existing lines in exactly one of those files. The worker resolved it correctly in favour of the specific instruction over the general one, applied the docstring change as SPEC A ordered, and declared the contradiction rather than silently choosing; the resulting commit carried 90 insertions against 2 deletions, the two deletions being precisely the old docstring bullet. Reviewer-prose contradiction between two clauses of one block, nothing wrong on disk and the intended change landed; no R-id spent (amend0827-process-diet rule 2).
SLICE SLIPS>>>
