STEP T001b/2 — F109 Semantic dedupe (round 2, session 1)

Goal: book round 1's verdict and the reviewer's two prose slips into the
record, then land T001b-i — the finalized-call adapter that decides WHICH
session a call belongs to, records it only when it is proven, and forgets a
session the moment a resume falls back.

SCOPE RULE, quoted verbatim in every F109 order per the feature file's
Orchestrator brief: RESUMED SESSION ONLY, PROVEN SENDS ONLY.

Base commit: bdd628508408970e3eb519eb25bef88483e5168a (round 1 close, the
tip of `feature/f109-semantic-dedupe`, already pushed). Stay on that branch:
do NOT create a branch, do NOT open a pull request, do NOT merge anything.

Round 1's verdict was PASS. The reviewer re-ran every one of its eight gates
itself. Nothing from round 1 is reopened here.

Bundle (one commit per item, in this order):
  C0a. Save this entire step block verbatim to `.agent/authored/f109-r2.md`.
  C0b. Mirror it byte-for-byte to `.agent/last_block.md`.
  C1.  `.agent/plan.md` <- SLICE PLAN, whole-file replacement. FIRST
       substantive commit, because this round touches the finding ledger
       (docs/agents/planner_reviewer_prompt.md §3 item 23).
  C2.  `.agent/live_review.md` <- SLICE VERDICT, appended. The round-1
       gate entry.
  C3.  `.agent/prose_slips.md` <- SLICE SLIPS, appended. Two dated lines,
       both recording REVIEWER prose errors from round 1, neither of which
       damaged anything on disk (AGENTS.md `### prose_slips.md`, operator
       amendment amend0827-process-diet rule 2 — no id, no severity, no
       correction round).
  C4.  `packages/orchestration/session_sent_index.py` — ADD the three
       adapter functions of SPEC A below, and update the module docstring
       as SPEC A's last paragraph requires. Change no existing behaviour.
  C5.  `tests/orchestration/test_semantic_dedupe.py` — ADD the cases of
       SPEC B below. Change no existing test.
  C6.  `.agent/handoff.md` <- rewritten per AGENTS.md `### handoff.md`,
       reporting the REAL results of gates G1 through G7, every one of
       which runs at C5 or earlier.
  Then: `git push`. The push happens AFTER C6, so the handback does NOT
  quote its result; the reviewer measures the remote tip itself.

Exact change set for this round. These paths and NO others:
  `.agent/authored/f109-r2.md`   new
  `.agent/last_block.md`          rewritten
  `.agent/plan.md`                rewritten
  `.agent/live_review.md`         appended
  `.agent/prose_slips.md`         appended
  `packages/orchestration/session_sent_index.py`   added to
  `tests/orchestration/test_semantic_dedupe.py`    added to
  `.agent/handoff.md`             rewritten

Constraints:
  1. Apply every SLICE byte-for-byte. If a slice looks wrong, apply it
     anyway and DECLARE the problem in the handback's deviations. Never
     silently repair a slice; never edit one to fit.
  2. Touch no path outside the change set above.
  3. BOTH appends are appends: never an insert, never an overwrite. Both
     `.agent/live_review.md` and `.agent/prose_slips.md` end WITHOUT a
     trailing newline at the base commit, and both must still end without
     one afterwards. Each append is exactly the two bytes `\n\n` followed
     by the slice's bytes, where the slice's own trailing newline — if
     your extraction tool adds one — is stripped first. Round 1 declared
     this same point as its deviation 3; it is stated here so it is a rule
     rather than a discovery.
  4. C4 and C5 ADD to existing files. Nothing already in either file is
     edited, reordered or deleted. The new adapter functions are PUBLIC
     API and belong with the other public names — place them after
     `session_sent_index_from_evidence` and BEFORE the private helpers
     `_segment_hashes_from_manifest` and `_evidence_hashes`, so the
     module keeps its existing public-then-private layout.
  5. Production code is described by SPEC, not sliced: you AUTHOR the
     Python in C4 and C5. Every behaviour named in the SPEC is mandatory
     and nothing beyond it may be added.
  6. The module stays PURE — no file read, no file write, no network, no
     provider call, and still no import from `packages.orchestration`.
     The adapters take the provider output object and read its attributes
     DUCK-TYPED with `getattr`; they must not import `BuilderOutput`,
     `ReviewerOutput` or anything else from `pingpong_provider`, because
     that import would make this module depend on the provider layer it
     exists to stay independent of.
  7. No round of F109 gates on `ruff`: this session's reviewer cannot
     execute it, so such a gate would rest on your word alone. Follow the
     repository's ruff configuration by construction instead — line length
     120, imports grouped `__future__`, stdlib, first-party.
  8. Destructive verification (G5) runs ONLY inside a disposable
     `git worktree`, DISCARDED afterwards rather than reverted. The
     primary checkout is never mutated.
  9. Every commit's insertion count stays under 500 (AGENTS.md DECISION
     F104 D1 — the `+` column only). Report one number per commit for C0a
     through C5 — that is SEVEN commits and therefore seven numbers.
 10. The three property guards named in round 1 still sweep every `*.py`
     under `packages/orchestration/`:
     `test_no_shell_true_in_orchestration`,
     `test_no_0000_in_production` and
     `test_no_bad_permit_order_in_production`, all in
     `tests/orchestration/test_test_runner.py`. The adapters satisfy all
     three trivially; none is a closed-set or count guard.

SPEC A — three functions ADDED to
`packages/orchestration/session_sent_index.py`.

  WHY THIS EXISTS. The index of round 1 knows how to remember a send. It
  does not know how to read a finalized provider call — which session that
  call belonged to, whether the call actually succeeded, or whether a
  resume fell back and invalidated everything the index believed. These
  three functions are that reading, and they are the whole of the decision
  logic, so the loop wiring that follows in the next round is mechanical.

  The reviewer measured the shapes these functions read, at the base
  commit named above, so the SPEC does not guess:
    - `BuilderOutput` and `ReviewerOutput`
      (`packages/orchestration/pingpong_provider.py`) BOTH carry `error`
      (str, empty when the call succeeded), `usage_actuals`
      (`dict | None`, carrying a `"session_id"` key when the provider
      reported one), `resume_used` (bool), `resume_session_ref` (str) and
      `resume_fallback` (bool). The two are structurally identical over
      exactly the fields these adapters read, which is why ONE duck-typed
      adapter serves both roles and no role argument is needed.
    - `packages/orchestration/pingpong_loop.py` reads the prior round's
      session id as `str(prev_actuals.get("session_id") or "")`, where
      `prev_actuals` is `getattr(prev_builder_out, "usage_actuals", None)
      or {}`. `session_id_of_finalized_call` below reproduces exactly that
      reading, so the loop and the index can never disagree about which
      string names a session.

  `session_id_of_finalized_call(output)` -> str
     The provider session this finalized call belongs to, or `""` when it
     has none. Read `usage_actuals` with `getattr(output, ...)`, treat a
     missing or None value as an empty mapping, take `"session_id"`, and
     coerce with `str(... or "")` so None, 0 and "" all become `""`. If
     `usage_actuals` is present but is not a mapping, return `""` rather
     than raising: this function reads foreign evidence and an unusable
     reading means "no session", never a crash in the loop.

  `record_finalized_call(index, output, manifest_rows)` -> int
     Record one finalized call into `index` and return what
     `SessionSentIndex.record_call` returned. The call COUNTS AS PROVEN
     only when `getattr(output, "error", "")` is falsy; pass that as `ok`.
     Pass `session_id_of_finalized_call(output)` as the session id, so a
     call with no session records nothing by the rule already in
     `record_call` rather than by a second rule here. Do NOT re-implement
     either guard; this function only translates an output object into the
     three arguments `record_call` already understands.

  `invalidate_on_resume_fallback(index, output, resumed_ref="")` -> bool
     The resume-fallback safety valve, and the reason it takes a THIRD
     argument. Return False and do nothing unless
     `getattr(output, "resume_fallback", False)` is true. When it is,
     invalidate the session that was being RESUMED — which is
     `resumed_ref` when the caller supplies it, otherwise
     `getattr(output, "resume_session_ref", "")`. Strip it; if the result
     is empty, return False and invalidate nothing, because invalidating
     an unnamed session would be a guess. Otherwise call
     `index.invalidate_session(...)` and return True.
     THE THIRD ARGUMENT IS LOAD-BEARING AND THIS IS THE REASON: the
     reviewer read `pingpong_loop.py` at the base commit, and on the
     fallback path the loop REPLACES the output object — it calls the
     provider again with `resume=None` and then sets `resume_fallback` on
     the NEW output. That second output resumed nothing, so its own
     `resume_session_ref` is `""` and the id of the session that failed
     lives only in the loop's `builder_resume_ref` variable. An adapter
     that read only the output object would therefore invalidate NOTHING
     on exactly the path invalidation exists for. `resumed_ref` is how the
     caller passes the id it still holds; the output-object fallback is
     kept for callers that have no such variable.

  Finally, UPDATE THE MODULE DOCSTRING. Its "deliberate absences" section
  currently says that nothing invalidates a session on its own and that
  wiring the resume fallback is T001b. That is now half true: the DECISION
  logic lands here, and only the CALL SITES in `pingpong_loop.py` remain.
  Reword that bullet to say exactly that, and add the three new names to
  the `Public API` list at the end of the docstring. Change nothing else
  in the docstring.

SPEC B — cases ADDED to `tests/orchestration/test_semantic_dedupe.py`.

  Hermetic and pure, as the existing file is: no `tmp_path`, no network,
  no provider, no sleep. Reuse the file's existing `_real_manifest_rows`,
  `_sample_rows` and `_digests` helpers rather than writing new ones.
  Define ONE small local stand-in for a provider output — a plain class or
  a `SimpleNamespace` factory carrying `error`, `usage_actuals`,
  `resume_used`, `resume_session_ref` and `resume_fallback` — and note in
  a comment that it is duck-typed on purpose, mirroring the adapters. Do
  NOT import from `pingpong_provider`.

  These cases are mandatory:
   1. `session_id_of_finalized_call` returns the id when `usage_actuals`
      carries one.
   2. It returns `""` when `usage_actuals` is None, when it is `{}`, when
      `"session_id"` is absent, and when `"session_id"` is None or `""`.
   3. It returns `""` — and does NOT raise — when `usage_actuals` is
      present but is not a mapping (pass a list and an int).
   4. A successful output with a session id records every manifest hash
      for that session, and `record_finalized_call` returns the same
      count `record_call` would.
   5. An output whose `error` is a non-empty string records NOTHING, and
      the session stays empty. This is the proven-sends-only rule reaching
      the adapter.
   6. An output with no session id records NOTHING even when it succeeded.
   7. `invalidate_on_resume_fallback` returns False and changes nothing
      when `resume_fallback` is false, even when a `resumed_ref` is
      supplied — the guard is the flag, not the argument.
   8. When `resume_fallback` is true and `resumed_ref` names a session the
      index holds, that session's set is emptied, the function returns
      True, and every OTHER session is untouched.
   9. THE LOOP'S REAL SHAPE, and it is the case that matters most: an
      output with `resume_fallback` true and `resume_session_ref` EMPTY —
      exactly what the loop's second call produces — still invalidates the
      right session when `resumed_ref` is passed, and invalidates NOTHING
      when it is not. Write both halves, and name the second one so a
      reader can see it is the failure the third argument prevents.
  10. `invalidate_on_resume_fallback` returns False when the resolved ref
      is whitespace only.
  11. END TO END over the three adapters, no loop involved: record a
      manifest for session "s1" from a successful output; assert it is
      held; then feed a fallback output naming "s1" as `resumed_ref`;
      assert the session is empty and that a later successful call to
      "s1" repopulates it. This is the honest lifecycle the feature
      claims, asserted in one test.

Done when — GATES. Run every one and record its REAL exit code and output.
"Green" as a word is a finding. G1 through G7 all run at C5 or earlier, so
C6 can quote every one. Report ONE LINE PER GATE in the handback.

  G1 TRANSPORT. `sha256sum .agent/authored/f109-r2.md .agent/last_block.md`
     — both must equal each other AND equal `SHA256_OF_THIS_BLOCK` as
     stated by the reviewer in the delegation wrapper. Report the digest.

  G2 THE PLAN. At C1: `.agent/plan.md` byte-equal to SLICE PLAN by `cmp`
     against a scratch copy, never a retype; `wc -l` strictly under 50;
     one `## Goal` heading and one `## Next Steps` heading.

  G3 THE VERDICT APPEND. At C2, over `.agent/live_review.md`:
     (a) BYTE ARITHMETIC. Size must be exactly 2018315 + 2 + S, where
         2018315 is the base size and S is the byte length of SLICE
         VERDICT after stripping any trailing newline your extractor
         added. Report all three numbers. Base sha256 is
         3a5981497bb3ada18babe0a906f4c6160a42563671b1350001fac74b0d2bc90e.
     (b) A SECOND, STRUCTURALLY DIFFERENT READER. Split the whole file on
         blank lines into units. COUNT the paragraphs in SLICE VERDICT
         yourself — call that N — and assert the LAST N units of the file
         equal those N paragraphs, in order.
     (c) NEGATIVE CONTROL. On a scratch copy, flip one byte inside the
         FIRST appended paragraph and confirm reader (b) REJECTS it.
         Report the tracked file's sha256 before and after: identical.
     (d) COUNTS. `grep -c` for `^Gate: F109 R1 — ` is exactly 1.
         `^- R-[0-9]\{4\} — ` is UNCHANGED at 330 and
         `^Done: R-[0-9]\{4\} — ` is UNCHANGED at 62 — this round
         registers no finding and resolves none.

  G4 THE SLIPS APPEND. At C3, over `.agent/prose_slips.md`:
     size must be exactly 40351 + 2 + S2, where 40351 is the base size and
     S2 is the byte length of SLICE SLIPS after the same trailing-newline
     strip; base sha256
     b00c1f249fce5ea243ea5963eee4453ac08a73fad1198c4b103f7e355e90e97c.
     Then the same blank-line reader as G3(b): count N2 paragraphs in
     SLICE SLIPS yourself and assert the last N2 units equal them in
     order. Report both numbers and the reader's verdict.

  G5 THE COLOUR OF THE NEW CODE. Inside a DISPOSABLE `git worktree` added
     at the round's C5 commit, never in the primary checkout. Purge
     `__pycache__` before every run and use `python3 -B`.
     (a) CONTROL FIRST, unmutated:
         `python3 -B -m pytest tests/orchestration/test_semantic_dedupe.py -q`
         Record the real exit code and passed count. A colour with no
         baseline is not evidence.
     (b) MUTATION A. In `record_finalized_call`, invert the proven test so
         a call with a non-empty `error` is recorded as ok. Re-run. It
         MUST fail, and the failure MUST include the SPEC B item 5 case.
     (c) MUTATION B. Restore, then in `invalidate_on_resume_fallback` make
         the function prefer `getattr(output, "resume_session_ref", "")`
         and ignore the `resumed_ref` argument entirely. Re-run. It MUST
         fail, and the failure MUST include the SPEC B item 9 case — this
         is the mutation that proves the third argument is load-bearing
         rather than decorative.
     (d) MUTATION C. Restore, then in `session_id_of_finalized_call` let a
         non-mapping `usage_actuals` propagate its exception instead of
         returning `""`. Re-run. It MUST fail on the SPEC B item 3 case.
     Report every exit code and the failing test names for each mutation.
     Then `git worktree remove --force` and `git worktree prune`; report
     `git worktree list` afterwards. Four `.remedy-wt/job-*` worktrees
     pre-date this branch and are expected to remain — leave them alone.

  G6 THE SUITES. At C5, run these SERIALLY — never two pytest processes
     alive at once — and report each real exit code and count. The base
     counts were measured by the reviewer at the base commit:
       `python3 -m pytest tests/orchestration/test_semantic_dedupe.py -q`
                                                    base 25, must GROW
       `python3 -m pytest tests/ui_server/ -q`                base 515
       `python3 -m pytest tests/orchestration/test_test_runner.py -q`
                                                              base  52
       `python3 -m pytest tests/regression/test_resource_safety.py -q`
                                                              base  21
       `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`
                                                              base  16
       `python3 -m pytest tests/cli/test_golden_path.py -q`    base  42
     This round changes no file under `docs/roadmap/`, so the docs-round
     gate is deliberately NOT ordered; the four state readers are ordered
     because the round rewrites `.agent/` state, and they are run AS FOUR.

  G7 THE TREE. At C5: `git status --porcelain` EMPTY. `git ls-files
     .remedy-wt` returns nothing. Report the insertion count of each
     commit C0a through C5 — seven numbers, each under 500. The C6
     handback commit's own count is NOT owed and is not reported.

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

Round 2 — book round 1's PASS verdict and the reviewer's two prose slips
into the record, then land T001b-i: the finalized-call adapter in
`packages/orchestration/session_sent_index.py`. Three functions read a
provider output and decide which session it belongs to, whether it was
proven, and which session a resume fallback must forget. The module stays
pure and still imports nothing from the provider layer.

## Next Steps

- T001b-ii: wire those adapters into `packages/orchestration/pingpong_loop.py`
  at the builder and reviewer finalized-call seams and at both resume
  fallback sites, and persist the index into the job's evidence.
- T002: the composition hook — a segment whose hash the session already
  holds becomes a one-line marker, with non-resume calls bypassing the
  hook entirely, asserted by a byte-equality golden.
- T003: the measurement fixture, the disable flag, and the docs.
- The integration gate, then the closure sequence.

## Risks

- On the loop's fallback path the output object is REPLACED, so the
  failed session's id survives only in the loop's own variable. The
  adapter therefore takes it as an argument; a version reading only the
  output would invalidate nothing exactly when it matters.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
SLICE PLAN>>>

SLICE VERDICT — appended to `.agent/live_review.md`, preceded by exactly
two newline bytes. One paragraph.
<<<SLICE VERDICT
Gate: F109 R1 — the round 1 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ FROM THE HANDBACK. THE ROUND'S SUBSTANCE: F109 was claimed in `docs/roadmap/STATUS.md`, the one closure candidate F108 left open was registered as `R-0769` and `.agent/candidates.md` was emptied, and T001a landed as `packages/orchestration/session_sent_index.py` with 25 unit tests in `tests/orchestration/test_semantic_dedupe.py`. TRANSPORT HELD IN THE STRONGEST FORM THIS WORKFLOW CAN PRODUCE, which is worth stating precisely because docs/agents/planner_reviewer_prompt.md §3 item 37 warns that a self-drive transport chain normally proves only that the worker was self-consistent: the reviewer wrote its own pre-delegation original to `.remedy-wt/f109-r1.md`, the worker COPIED rather than retyped it, and `.remedy-wt/f109-r1.md`, the committed `.agent/authored/f109-r1.md` and the working `.agent/last_block.md` were all independently sha256'd by the reviewer at `5652e93f880d9ee7972a7bbc5a486a148aae6b5201ed94e06ffb7c68d483df03` — three readings including the reviewer's own, so the bytes authored are demonstrably the bytes that landed, and the chain this verdict claims is exactly the chain that was walked. THE THREE WHOLE-FILE SLICES WERE PROVED BYTE-EQUAL AGAINST THE REVIEWER'S OWN ORIGINAL, not against a retype: `.agent/plan.md` at 41 lines, `.agent/context.md` at 55 and `.agent/candidates.md` at 17, and for each the reviewer ran a trailing-newline-stripped negative control which printed False, so every equality distinguishes the two candidates rather than accepting both. THE PAIR WAS MEASURED, NOT ASSERTED: STATUSFROM occurs 0 times in `docs/roadmap/STATUS.md` and STATUSTO exactly 1, the containment test printed `TO contains FROM: false` confirming the REWRITE shape the block declared, `^- \[x\] F` is 67 at the base commit and 67 after, and `^- \[~\] F` is 1, at the cap `tests/docs/test_docs_consistency.py` enforces at its line 328. THE LEDGER APPEND WAS RECONSTRUCTED INDEPENDENTLY: the reviewer re-measured the file at 2018315 bytes against base 2015028 plus the two separator bytes plus a slice of 3285, confirmed the file still ends without a trailing newline, counted N=1 paragraphs itself rather than taking the block's number, confirmed the last unit byte-equal to the slice, and ran its OWN negative control flipping a byte inside the FIRST appended paragraph, which the structural reader rejected while the tracked file's digest stayed `3a5981497bb3ada18babe0a906f4c6160a42563671b1350001fac74b0d2bc90e` throughout. The counts moved exactly as ordered: findings 329 to 330 with `R-0769` present once, and `Done:` unmoved at 62. THE MUTATION RED-PROOF WAS REPRODUCED BY THE REVIEWER IN ITS OWN DISPOSABLE WORKTREE, not accepted from the handback: the unmutated control was a real exit 0 at 25 passed, removing the `ok` guard produced exit 1 with exactly one failure and it was the `ok=False` case, and accepting an empty `session_id` produced exit 1 with exactly two failures and they were the empty-id and whitespace-id cases — the colours the block ordered, on the tests the block named. The worktree was removed and pruned, and the primary checkout was confirmed unmutated afterwards, `git status --porcelain` empty and the `if not ok:` guard still present. THE SUITES ARE THE REVIEWER'S OWN, run serially with never two pytest processes alive: 25, 295, 30, 515, 52, 21, 16 and 42, every one exit 0 and every one identical to the base reading taken before the round was delegated. STRUCTURE HELD: eight single-parent commits, insertions 458, 455, 28, 28, 11, 211 and 329 for C0a through C5 with the handback commit at 216, every one under 500; the reflog carries no amend, rebase, cherry-pick or reset; no merge commit exists in the range; `git ls-files .remedy-wt` is empty; and the remote tip equals the local tip at `bdd628508408970e3eb519eb25bef88483e5168a`. THE CODE WAS READ, NOT ONLY RUN: the module imports only `collections.abc`, so its docstring's purity claim is true as written; `record_call` validates the whole manifest before mutating the index, so a malformed row leaves the index untouched rather than half-updated; and `_evidence_hashes` rejects `str` and `bytes` explicitly, without which a bare string would have been accepted as a sequence of one-character hashes. The worker's decision to leave `sent_hashes` WITHOUT a redundant blank-id guard is correct and is recorded here as the right call: a second guard there would have masked the empty-id mutation and made that red-proof unfalsifiable, so the single-sited rule is what makes the colour real. FOUR DEVIATIONS WERE DECLARED AND ALL FOUR ARE ACCEPTED. Two are the REVIEWER'S OWN ERRORS and are routed to `.agent/prose_slips.md` by this round's C3 rather than spending an id, per AGENTS.md `### prose_slips.md` and operator amendment amend0827-process-diet rule 2: the block's G8 clause said "six numbers" over a bundle its own text enumerates as seven commits, and the block's G4(a) never said whether S included a trailing newline. Neither left anything wrong on disk. The third deviation is environmental and was independently corroborated — the sandbox bash guard rejects a literal dollar sign inside a quoted grep pattern, which the reviewer hit itself when its own `^## Open candidates$` grep was refused; the worker routed those greps through a no-shell argv runner so grep received each pattern byte-for-byte, and in every case the reviewer's own byte-equality proof over the same file is strictly stronger than the count the grep would have produced. The fourth is a true statement about pre-existing state: four `.remedy-wt/job-*` worktrees at `f0e6b9a3`, `21a45836` and `4b49af98` predate this branch, and the reviewer confirmed all four are older than it and that only the round's own G6 worktree was removed. THE ROUND PASSES. The open set stands at 268 — 330 findings minus 62 resolutions — and `.agent/candidates.md` is EMPTY, so no block condition stands against F109.
SLICE VERDICT>>>

SLICE SLIPS — appended to `.agent/prose_slips.md`, preceded by exactly two
newline bytes. Two paragraphs.
<<<SLICE SLIPS
2026-09-03 · F109 R1 · The reviewer's own step block ordered gate G8 to report the insertion count of "each commit from C0a through C5 — six numbers", while the same block's Bundle enumerates C0a, C0b, C1, C2, C3, C4 and C5, which is seven; the worker applied the clause as written per constraint 1, reported all seven counts and declared the contradiction. The checklist item this breaks is §3 item 32 — a clause naming a KIND of the block's own parts states no COUNT of that kind — and the block's arithmetic was right while only the adjective was wrong. Reviewer-prose miscount, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).

2026-09-03 · F109 R1 · The reviewer's own step block defined gate G4(a)'s byte arithmetic as "2015028 + 2 + S, where S is the byte length of SLICE RECORD as saved to scratch" without saying whether S included the trailing newline a POSIX text extractor appends, while the same block's constraint 4 required the appended file to end WITHOUT one; the worker resolved the ambiguity correctly in favour of constraint 4 (S = 3285, not 3286), landed the correct bytes and declared the discrepancy so a reviewer recomputing S from the raw slice would not read it as a mismatch. Reviewer-prose ambiguity between two clauses of one block, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
SLICE SLIPS>>>
