STEP T001b-iii/4 — F109 Semantic dedupe (round 4, session 1)

Goal: book round 3's verdict, register the blind-gate finding round 3
surfaced, and REPAIR it — give the chain tests two DISTINCT provider
session ids so each loop seam is proven on its own instead of as a group.

SCOPE RULE, quoted verbatim in every F109 order per the feature file's
Orchestrator brief: RESUMED SESSION ONLY, PROVEN SENDS ONLY.

Base commit: f7a11ff7f663e94f9344c6f29983b4645f1e02db (round 3 close, the
tip of `feature/f109-semantic-dedupe`, already pushed). Stay on that
branch: do NOT create a branch, do NOT open a pull request, do NOT merge.

Round 3's verdict was PASS. Its wiring is correct and additive — the
reviewer read the diff and re-ran every suite. What round 3 also did,
correctly and to its credit, was report BOTH of its ordered mutations as
GREEN rather than manufacture a red. That honesty is what this round acts
on: the gate was blind, the reviewer wrote it, and it is repaired here.

WHY IT WAS BLIND, and the reviewer measured this rather than reasoning
about it. `FakeProvider` emits ONE `fake_session_id`, and round 3's chain
tests passed the SAME provider instance as both `builder_provider` and
`reviewer_provider`. Builder and Reviewer therefore recorded into the SAME
session row, so deleting either `record_finalized_call` left the row
populated by the other seam, and deleting the builder's
`invalidate_on_resume_fallback` was masked by the reviewer's firing later
on that same session. Four call sites, one observable.

THE REPAIR IS PROVEN, NOT PROPOSED. Before writing this block the reviewer
drove the real loop in a disposable worktree with TWO providers carrying
DISTINCT ids and measured: unmutated, `session_sent_evidence` holds two
rows, `sess-builder` with 9 hashes and `sess-reviewer` with 10; with the
builder `record_finalized_call` deleted, `sess-builder` DISAPPEARS
entirely and only `sess-reviewer` remains. The discriminator works.

Bundle (one commit per item, in this order):
  C0a. Save this entire step block verbatim to `.agent/authored/f109-r4.md`.
  C0b. Mirror it byte-for-byte to `.agent/last_block.md`.
  C1.  `.agent/plan.md` <- SLICE PLAN, whole-file replacement. FIRST
       substantive commit (§3 item 23 — this round touches the ledger).
  C2.  `.agent/live_review.md` <- SLICE RECORD, appended. TWO paragraphs:
       the round-3 gate entry, then the registration of `R-0770`. Findings
       persist FIRST, in their own commit, before any repair
       (docs/agents/planner_reviewer_prompt.md §4 item 4).
  C3.  `tests/orchestration/test_semantic_dedupe.py` — the repair, per
       SPEC R below. This is the ONE commit in which editing existing
       tests is not only allowed but required.
  C4.  `.agent/live_review.md` <- SLICE LANDED, appended. One line.
       You write `Landed:`, never `Done:` — only reviewer-authored text
       sets a resolution (§4 item 4).
  C5.  `.agent/handoff.md` <- rewritten per AGENTS.md `### handoff.md`,
       reporting the REAL results of gates G1 through G7, every one of
       which runs at C4 or earlier.
  Then: `git push`. The push happens AFTER C5, so the handback does NOT
  quote its result; the reviewer measures the remote tip itself.

Exact change set for this round. These paths and NO others:
  `.agent/authored/f109-r4.md`   new
  `.agent/last_block.md`          rewritten
  `.agent/plan.md`                rewritten
  `.agent/live_review.md`         appended TWICE (C2, then C4)
  `tests/orchestration/test_semantic_dedupe.py`    edited
  `.agent/handoff.md`             rewritten

Constraints:
  1. Apply every SLICE byte-for-byte. If a slice looks wrong, apply it
     anyway and DECLARE the problem in the handback's deviations.
  2. Touch no path outside the change set above. In particular
     `packages/orchestration/pingpong_loop.py` and
     `packages/orchestration/session_sent_index.py` are NOT edited this
     round: the production code is correct and the defect is in the tests
     that failed to prove it. If you believe production code must change,
     STOP and declare it.
  3. BOTH appends are appends. `.agent/live_review.md` ends WITHOUT a
     trailing newline and must still do so after each. Each append is
     exactly the two bytes `\n\n` followed by the slice's bytes, with any
     trailing newline your extractor adds stripped first.
  4. C3 EDITS EXISTING TESTS. Every case listed in SPEC R must exist and
     pass when the round ends. You may rename, split and rewrite the
     bodies of the `TestChainAgainstTheRealLoop` class; you may NOT touch
     any test outside that class, and you may NOT reduce what is asserted
     — every property round 3's chain tests pinned must still be pinned by
     some case after the repair.
  5. Test code here is described by SPEC, not sliced: you AUTHOR it.
  6. No round of F109 gates on `ruff`: this session's reviewer cannot
     execute it. Follow the repository's ruff configuration by
     construction — line length 120, import groups as the file has them.
  7. Destructive verification (G5) runs ONLY inside a disposable
     `git worktree`, DISCARDED afterwards rather than reverted. The
     primary checkout is never mutated.
     WHEN YOU RUN PYTEST IN THAT WORKTREE, FIRST PRINT
     `packages.orchestration.pingpong_loop.__file__` AND CONFIRM IT
     RESOLVES INSIDE THE WORKTREE. `remedy` is installed editable and a
     `.pth` file puts the PRIMARY checkout on `sys.path`, so a run made
     from the wrong directory silently tests the unmutated primary copy
     and every mutation comes back green for the wrong reason. Round 3
     found this hazard; it is now a standing step.
  8. Every commit's insertion count stays under 500. Report one number per
     commit for C0a through C4 — that is SIX commits and therefore six
     numbers.

SPEC R — repair of `TestChainAgainstTheRealLoop` in
`tests/orchestration/test_semantic_dedupe.py`.

  THE ONE STRUCTURAL CHANGE. Every case in this class that currently
  passes one provider as both roles now builds TWO providers with
  DISTINCT `fake_session_id` values and passes them separately:

      builder = FakeProvider(fail_on_round=1, pass_on_round=2,
                             supports_resume=True,
                             fake_session_id="sess-builder")
      reviewer = FakeProvider(fail_on_round=1, pass_on_round=2,
                              supports_resume=True,
                              fake_session_id="sess-reviewer")
      result = run_pingpong("Fix README", str(demo_repo),
                            builder_provider=builder,
                            reviewer_provider=reviewer,
                            repair_rounds=2)

  Give the class a helper that builds this pair so no case repeats it, and
  say in the class docstring WHY the two ids differ: with one shared id
  the four loop call sites collapse to a single observable and no mutation
  of an individual seam can be caught. That sentence is the finding's
  counter-measure living where the next reader will be standing.

  The cases, after the repair:
   1. THE BUILDER SEAM, PINNED ALONE. A resumed two-round chain yields a
      row whose `session_id` is exactly `"sess-builder"`, and that row's
      `sent_sha256` is non-empty. Assert the ROW EXISTS BY ID and that it
      is non-empty. Do NOT assert an exact hash count: the count follows
      from prompt composition and would pin this test to unrelated prompt
      changes. This case is what MUTATION A must break.
   2. THE REVIEWER SEAM, PINNED ALONE. The same, for a row whose
      `session_id` is exactly `"sess-reviewer"`, non-empty. This case is
      what deleting the reviewer `record_finalized_call` must break.
   3. BOTH SEAMS TOGETHER: the set of `session_id` values in
      `result.session_sent_evidence` is exactly
      `{"sess-builder", "sess-reviewer"}` — no more, no fewer — and the
      rows are sorted by `session_id`, which is the determinism
      `as_evidence_dicts` promises.
   4. Every hash in every row is a 64-character lowercase hex string, and
      each row's `sent_sha256` is sorted. (Round 3 pinned this; keep it.)
   5. A provider pair that reports NO session id leaves the evidence
      EMPTY: build both providers without `fake_session_id` and assert
      `result.session_sent_evidence == []`.
   6. THE SEAMS DO NOT LEAK INTO EACH OTHER: assert that the
      `sess-builder` row and the `sess-reviewer` row do not hold an
      identical hash set. They compose different prompts, so an assertion
      that the two sets are unequal fails the moment the two seams are
      wired to one index key — which is exactly the collapse this repair
      exists to prevent. If you find the two sets ARE equal, do NOT force
      the assertion: report it, because that would mean something real.
   7. Keep round 3's non-resuming-provider case
      (`final_status` and round count unchanged for a provider that never
      resumes), and keep its single-round case, both adapted to the
      two-provider shape where they drive the loop.
   8. THE FALLBACK CASE stays, adapted: drive the chain so the builder's
      resume attempt errors and the loop takes its same-round fallback,
      and assert the run completes and that round's `resume_fallback` is
      true. State plainly in that test's docstring that it pins the
      fallback PATH and does NOT discriminate the builder's
      `invalidate_on_resume_fallback` call — G5's probe (c) below
      establishes that, and `R-0770` records why the discriminator is not
      available until T002.

Done when — GATES. Run every one and record its REAL exit code and output.
"Green" as a word is a finding. G1 through G7 all run at C4 or earlier, so
C5 can quote every one. Report ONE LINE PER GATE in the handback.

  G1 TRANSPORT. `sha256sum .agent/authored/f109-r4.md .agent/last_block.md`
     — both equal to each other AND to `SHA256_OF_THIS_BLOCK` as stated in
     the delegation wrapper. Report the digest.

  G2 THE PLAN. At C1: `.agent/plan.md` byte-equal to SLICE PLAN by `cmp`
     against a scratch copy, never a retype; `wc -l` strictly under 50; one
     `## Goal` and one `## Next Steps`.

  G3 THE RECORD APPEND. At C2, over `.agent/live_review.md`:
     (a) BYTE ARITHMETIC. Size must be exactly 2030395 + 2 + S, where
         2030395 is the base size and S is the byte length of SLICE RECORD
         after stripping any trailing newline. Report all three. Base
         sha256
         f09af719542dbb3ecace6cc8f00cc2a1a84ed0d80e41bc965670eed177bc17d6.
     (b) A SECOND, STRUCTURALLY DIFFERENT READER. Split the whole file on
         blank lines into units. COUNT the paragraphs in SLICE RECORD
         yourself — call that N — and assert the LAST N units equal those
         N paragraphs, IN ORDER.
     (c) NEGATIVE CONTROL. On a scratch copy, flip one byte inside the
         FIRST appended paragraph — not the last — and confirm reader (b)
         REJECTS it. Report the tracked file's sha256 before and after:
         identical.
     (d) COUNTS at C2: `^- R-[0-9]\{4\} — ` goes 330 to 331 and
         `^- R-0770 — ` is exactly 1; `^Gate: F109 R3 — ` is exactly 1;
         `^Done: R-[0-9]\{4\} — ` is UNCHANGED at 62.

  G4 THE LANDED APPEND. At C4: size equals (the size you measured after
     C2) + 2 + S2, where S2 is SLICE LANDED's stripped byte length; report
     both numbers and the C2 size they build on. `^Landed: R-` goes 24 to
     25 and `^Landed: R-0770 — ` is exactly 1. `^Done: R-[0-9]\{4\} — `
     is STILL 62 — you never write a `Done:` line.

  G5 THE COLOUR, AND THIS IS THE ROUND'S POINT. Inside a DISPOSABLE
     `git worktree` added at the C3 commit, never in the primary checkout.
     Apply constraint 7's `__file__` check FIRST and report the path.
     Purge `__pycache__` before every run and use `python3 -B`. Before
     each mutation, confirm the exact text you are about to delete occurs
     EXACTLY ONCE in `packages/orchestration/pingpong_loop.py` and report
     that count.
     (a) CONTROL, unmutated:
         `python3 -B -m pytest tests/orchestration/test_semantic_dedupe.py -q`
         Report the real exit code and passed count.
     (b) MUTATION A — delete the BUILDER `record_finalized_call` call.
         Re-run. It MUST now FAIL, and the failure MUST include SPEC R
         case 1. This is the mutation that came back green in round 3; if
         it is still green the repair did not work and you must say so
         plainly rather than adjusting any test.
     (c) MUTATION B — restore, then delete the REVIEWER
         `record_finalized_call` call. Re-run. It MUST FAIL, and the
         failure MUST include SPEC R case 2.
     (d) PROBE, NOT A COLOUR — restore, then delete the BUILDER
         `invalidate_on_resume_fallback` call and re-run. REPORT THE
         RESULT HONESTLY WHATEVER IT IS. A green here is EXPECTED and is
         not a failure of this round: the record that follows the
         invalidation repopulates the same session, so no assertion
         available before T002 can separate them. Report the exit code and
         count either way; do NOT edit a test to force a red.
     Restore, then `git worktree remove --force` by exact path and
     `git worktree prune`; report `git worktree list`. Four
     `.remedy-wt/job-*` worktrees pre-date this branch and must remain.

  G6 THE SUITES. At C4, run these SERIALLY — never two pytest processes
     alive at once — and report each real exit code and count. Base counts
     measured by the reviewer at the base commit:
       `python3 -m pytest tests/orchestration/test_semantic_dedupe.py -q`
                                                    base 51, may change
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

  G7 THE TREE. At C4: `git status --porcelain` EMPTY. `git ls-files
     .remedy-wt` returns nothing. Report the insertion count of each commit
     C0a through C4 — six numbers, each under 500. Additionally report
     `git diff --numstat` over the range for
     `packages/orchestration/pingpong_loop.py` and
     `packages/orchestration/session_sent_index.py`: constraint 2 expects
     BOTH to be absent from the range entirely.

Handback: rewrite `.agent/handoff.md` per AGENTS.md `### handoff.md`. It
carries the feature and round, the SESSION NUMBER — which is 1 — the
branch, the commit SHAs, a changed-files table, ONE LINE PER GATE with its
real result, the open-findings count, the deviations, and the next expected
action. It has no length cap. An item-status table covering C0a through C5
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

Round 4 — book round 3's PASS verdict, register `R-0770` (the chain tests
proved the four loop call sites only as a GROUP, because one shared
`fake_session_id` collapsed them to a single observable), and repair it by
giving the chain tests two DISTINCT provider session ids so the Builder
and Reviewer record seams are each pinned alone. No production code
changes this round: the wiring is correct and the defect is in the tests
that failed to prove it.

## Next Steps

- T002: the composition hook — a segment whose hash the session already
  holds becomes a one-line marker, with non-resume calls bypassing the
  hook entirely, asserted by a byte-equality golden. T002 is also where
  the resume-fallback invalidation finally becomes observable, which is
  the half `R-0770` records as still unproven.
- T003: the measurement fixture, the disable flag, and the docs.
- The integration gate, then the closure sequence.

## Risks

- The parse-retry and post-mortem provider calls are still deliberately
  NOT wired into the index. That records strictly less than was sent,
  which errs in the safe direction; T002 must not assume completeness.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
SLICE PLAN>>>

SLICE RECORD — appended to `.agent/live_review.md`, preceded by exactly two
newline bytes. Two paragraphs.
<<<SLICE RECORD
Gate: F109 R3 — the round 3 entry. VERDICT PASS, AND THE ROUND'S MOST VALUABLE OUTPUT WAS A GREEN GATE HONESTLY REPORTED. THE ROUND'S SUBSTANCE: round 2's verdict and one reviewer prose slip were booked, and T001b-ii wired the finalized-call adapters into `packages/orchestration/pingpong_loop.py` at four sites — the Builder and Reviewer finalized-call seams and both resume-fallback sites — with `PingPongResult` gaining a `session_sent_evidence` field and the first chain tests in this feature that drive the real loop. TRANSPORT: the reviewer's own pre-delegation original `.remedy-wt/f109-r3.md`, the committed `.agent/authored/f109-r3.md` and `.agent/last_block.md` all independently sha256'd at `c34d14df27ad8bb2f53d58c74b5f1984dab684f4f4fdbeb9c90df853bca3ec7f`, copied rather than retyped. THE LOOP EDIT IS EXACTLY WHAT CONSTRAINT 4 DEMANDED AND THE REVIEWER READ EVERY LINE OF IT: 28 insertions and ZERO deletions, one new import, one dataclass field with a default so every existing construction site is untouched, one index per RUN placed before the round loop, and four call statements each appended after an existing statement so nothing moved; the invalidate-then-record order falls out of the existing line order rather than being imposed; and the third argument is passed at both fallback sites, which is the whole reason the adapter takes one. THE APPENDS RECONSTRUCT: `.agent/live_review.md` at 2030395 against base 2024336 plus two plus 6057, and `.agent/prose_slips.md` at 42621 against base 41716 plus two plus 903, each with N counted by the reviewer itself, the last unit byte-equal, a negative control on the FIRST appended paragraph rejected, and both files still ending without a trailing newline. Counts held: `^Gate: F109 R2 — ` 1, findings 330, `Done:` 62. THE SUITES ARE THE REVIEWER'S OWN, run serially, every one exit 0 and every one matching its base: 51, 34, 27, 81, 515, 52, 21, 16 and 42. STRUCTURE: eight single-parent commits, insertions 396, 274, 13, 3, 3, 28 and 154 for C0a through C5, all under 500; change set exactly the eight ordered paths; remote tip equal to local at `f7a11ff7f663e94f9344c6f29983b4645f1e02db`. THE ROUND ALSO SURFACED A REAL ENVIRONMENTAL HAZARD AND DEFEATED IT: `remedy` is installed editable, so a `.pth` places the PRIMARY checkout on `sys.path` and a pytest run made from the wrong directory silently imports the unmutated primary copy while appearing to test a worktree. The worker printed `pingpong_loop.__file__` in every mutation run to prove the worktree's own copy was under test, and the reviewer independently confirmed the same resolution inside its own worktree; the mutation results of rounds 1 and 2 are unaffected, because those mutations went RED, which is only possible if the mutated copy was the one imported. THE ROUND PASSES, and the finding below is registered against the reviewer's own test specification rather than against the worker's execution.

- R-0770 — Medium, THE F109 CHAIN TESTS PROVE THE FOUR LOOP CALL SITES ONLY AS A GROUP, SO DELETING EITHER RECORD SEAM LEAVES THE SUITE GREEN. Found by the WORKER at F109 round 3 while executing that round's own ordered mutations, reported honestly as green rather than forced red, and registered here at the reviewer's first opportunity. Measured by the reviewer at `f7a11ff7f663e94f9344c6f29983b4645f1e02db` in a disposable worktree, with `packages.orchestration.pingpong_loop.__file__` confirmed to resolve inside that worktree first: with the Builder `record_finalized_call` call deleted from the loop, `python3 -B -m pytest tests/orchestration/test_semantic_dedupe.py -q` exits 0 at 51 passed, identical to the unmutated control. THE CAUSE IS THE FIXTURE, NOT THE WIRING. `FakeProvider` emits a single `fake_session_id`, and round 3's chain tests passed ONE provider instance as both `builder_provider` and `reviewer_provider`, so the Builder and Reviewer seams recorded into the SAME session row; whichever seam is deleted, the other repopulates the row and every mandated assertion — which pinned only shape, never a seam-attributable value — still holds. The same collapse hides the Builder's `invalidate_on_resume_fallback`, because the Reviewer's fires later on that same session. This is the R-0712 fixture class arriving through a provider double rather than through an event fixture: a test whose two subjects share one observable cannot fail on either. THE REPAIR IS PROVEN AND IS APPLIED IN THIS ROUND'S C3. The reviewer drove the real loop with TWO providers carrying DISTINCT ids and measured, at the same commit and in the same worktree: unmutated, `session_sent_evidence` holds two rows, `sess-builder` with 9 hashes and `sess-reviewer` with 10; with the Builder `record_finalized_call` deleted, the `sess-builder` row DISAPPEARS and only `sess-reviewer` survives. A case that asserts the `sess-builder` row exists and is non-empty therefore goes red on exactly that mutation, and its mirror pins the Reviewer seam. WHAT THIS FINDING DOES NOT FIX, stated so the next round does not assume it: the resume-fallback INVALIDATION remains unproven by any test, because the `record_finalized_call` that follows an invalidation repopulates the very session just cleared, so no assertion available today separates "cleared then refilled" from "never cleared". Distinguishing them needs a segment the second call does NOT resend, which is precisely what the T002 composition hook introduces — so the discriminator lands with T002 and this finding is not resolved until a test fails when the Builder `invalidate_on_resume_fallback` call is removed. Medium rather than High because no production behaviour is wrong: the loop wiring is correct and was read line by line, and the defect is that the suite would not have caught it had it been wrong. OPEN.
SLICE RECORD>>>

SLICE LANDED — appended to `.agent/live_review.md` at C4, preceded by
exactly two newline bytes. One line.
<<<SLICE LANDED
Landed: R-0770 — the chain tests now build two providers with distinct `fake_session_id` values, so the Builder and Reviewer record seams are each pinned by a case naming their own session row; deleting either `record_finalized_call` from the loop now fails the suite. The fallback-invalidation half is unchanged and stays OPEN per the finding's own text, awaiting the T002 discriminator. Applied in C3 of F109 round 4.
SLICE LANDED>>>
