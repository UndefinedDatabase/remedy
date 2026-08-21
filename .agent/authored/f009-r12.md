── STEP T002/3 — F009 ────────────────────────────────────────
Goal:        Close this session's record: persist the two defects the R11 review
             found — both of them the reviewer's own — and record the R11
             verdict. NO PRODUCTION CODE IS WRITTEN.

Bundle:      C0a save this block · C0b mirror it · C1 plan · C2 register R-0636
             · C3 register R-0637 · C4 the R11 verdict · C5 handback.

THE ROUND BASE is `fde072f181e223a32e22b663f315375f753f7d45`. Every gate reading
below said to be "at the round base" is measured against that SHA. C5's own SHA
cannot exist inside C5, so C5 is named by role and the round report carries its
value (R-0371).

THIS ROUND EXISTS BECAUSE A FINDING THAT LIVES ONLY IN A SESSION'S CHAT IS LOST
WHEN THAT SESSION ENDS. The R11 review found two defects, both in the reviewer's
own R11 specification rather than in the round's work, and it verified a verdict
that no on-disk record yet carries. Persisting all three costs one short round of
no new work. NOTHING under `packages/`, `apps/`, `tests/` or `docs/` is touched.

Change set — these paths and nothing else:
  `.agent/authored/f009-r12.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `.agent/handoff.md`

Slice convention: the authored units below are delimited by `<<<SLICE <NAME>` and
`<<<END <NAME>` lines. Extract each from the COMMITTED C0a blob by those marker
lines, with a script, and apply it programmatically. The marker lines themselves
are never written into any target file.

<<<SLICE PLANF009R12
# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at `ce49348b`, the
merge commit of pull request #209. `.agent/live_review.md` is the source of truth
for the open set, the round map and the finding-id ceiling.

## Goal
Exactly ONE door for UI-initiated change: POST /api/jobs/{jid}/commands validates
against the UI-exposed catalog subset, authenticates with a bearer token plus an
X-Remedy-CSRF double-submit, rate-limits per token and job, deduplicates by
client nonce, and ENQUEUES into the existing decision, approval and control
machinery without touching files, jobs or shells directly. Every other POST, PUT
and DELETE answers 405. DONE when the exposed commands round-trip through their
effects on fixtures, replayed nonces are idempotent, unauthenticated and
cross-site attempts fail closed and are audited as rejected, and a route-walking
test plus an import guard prove no other mutating route exists.

## Current Step
R12 closes this session and writes no production code. It registers R-0636 and
R-0637 — both defects in the reviewer's own R11 specification, found by the R11
review and confirmed by the round's own declared deviations — and records the R11
verdict. T002 is built except for publication, which D15 routes to T003.

## Next Steps
1. T003's effect table per D5 — the round that retires the 501 seam. It is also
   the round that adds the `publish_nonce_result` call site, writes D14's reserved
   `accepted` outcome, moves the replay's audit token off `not_implemented`
   (R-0636) and bounds the published record (R-0637). The plan-approval extraction
   lands as its own commit and the `command.accepted` SSE event lands with it.
2. Then the client wiring that sends both headers, the route-walking 405 test and
   the import guard, the integration gate, and closure.

## Risks
- R-0636 and R-0637 are both owed by the SAME round, T003, and both are one-line
  changes there. Neither is owed a change now, and neither may be paid down
  separately: each depends on the publish call site that round introduces.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which is
  R-0622 and routes to a paydown branch.
<<<END PLANF009R12

<<<SLICE R0636
- R-0636 — Low — A REVIEWER SPEC ORDERED TWO COMMITS WHOSE REQUIREMENTS COULD NOT BOTH BE MET, TWICE IN ONE BLOCK, AND THE WORKER HAD TO SPEND BOTH DEVIATIONS PROVING IT. The R11 block, committed at `45a67196`, specified C6 and C7 independently and never read them against each other. FIRST COLLISION: C6 printed `publish_nonce_result(job_id, nonce, body, *, control_root_path=None)` returning "the body that is in force", while C7 required that the store hold the status too, "a body without its status cannot answer a replay truthfully" — the same block, forty lines apart, ordering an interface that cannot carry what the next commit must read out of it. The worker kept the printed positional shape, added a REQUIRED keyword-only `status` with no default, and returned the record; that resolution is correct and a default would have been worse, since a frozen wrong status is exactly the failure D15 exists to prevent. SECOND COLLISION, and the one with a consequence beyond the round: C7 ordered the replay audited "with the outcome the ORIGINAL attempt would have carried", while DECISION F009 D15's first half rules that only an ACCEPTED command publishes a record — so the original outcome is `accepted`, which DECISION F009 D14 RESERVES, which `packages/orchestration/command_audit.py` excludes from `OUTCOMES`, and which two tests shipped at `8d050bb3` forbid this door to write. The instruction was satisfiable by no implementation. The worker wrote `not_implemented`, which is the honest outcome while the seam stands, and named the collision in a comment at the call site rather than burying it. WHY LOW: nothing false reached disk, both suites are green, and the worker's resolutions are the ones the reviewer would have authored. THE CLASS IS THE BLOCK'S OWN INTERNAL CONSISTENCY, which checklist item 13 of `docs/agents/planner_reviewer_prompt.md` covers for a block's ORDERING and item 16 for a count against a list it NAMES, while neither reaches one commit's stated INTERFACE against another commit's stated REQUIREMENT — R-0527 is the nearest relative and it binds a constraint against a slice, not a spec against a spec. FIX, owed by the round that retires the 501 seam and by no earlier one, because both halves depend on the publish call site that round introduces: when `publish_nonce_result` gains its door caller, the replay's audit token moves off `not_implemented` to whatever that round rules a replay is — and a replay is NOT the same event as the acceptance it repeats, so a distinct token is likely the right answer rather than reusing `accepted`, which would make the two indistinguishable to `T5_F035` and `T9_F167`, the two features that read this file to count what the door did.
<<<END R0636

<<<SLICE R0637
- R-0637 — Low — THE NONCE RECORD'S SIZE BOUND IS ENFORCED WHERE IT IS READ AND NOT WHERE IT IS WRITTEN, SO A RECORD CAN BE PUBLISHED THAT CAN NEVER BE REPLAYED. Measured by the reviewer at `fde072f1` in `packages/orchestration/command_nonce.py`: `MAX_NONCE_RECORD_BYTES` is 64 KiB and it is passed to `read_verified_file` in `_read_record`, so a larger record is refused at lookup; `publish_nonce_result` does not mention the constant at all, so nothing stops one being written. The consequence is silent and is in the safe direction, which is why it is Low rather than Medium: an oversize record publishes, every later lookup of that nonce reads nothing, and the client's replay re-executes the command instead of being answered — idempotency is simply OFF for that nonce, with no error anywhere and no way for the client to tell. The docstring's own reasoning is what leaves the gap: it says the bound "matches the door's own request ceiling, so nothing that fits through the door fails to fit in the store", and that is true of the REQUEST and says nothing about the RESPONSE, which is what this store actually holds — a body the door composed, not a body the client sent. NOTHING IS BROKEN TODAY and no test is wrong: `publish_nonce_result` has no door call site at all while the 501 seam stands, by DECISION F009 D15, so no oversize record can currently be produced by any path a request can reach. That is also why this is registered rather than repaired here — the repair belongs with the caller. FIX, owed by the round that retires the seam, in the same commit that adds the publish call site: refuse an oversize record AT PUBLICATION, returning None the way every other unusable input to that function already does, so a record that cannot be replayed is never written in the first place; and state the rule in terms of the RESPONSE rather than the request, since those are the bytes being bounded. A test that publishes a record over the bound and asserts the refusal belongs with it, because the current bound has no negative control on the write side at all.
<<<END R0637

<<<SLICE LEDGER12
Gate: R12 — the R11 entry. R11 PASSED. Every gate was re-run by the reviewer and every value reproduced, both declared deviations are correct and both are the REVIEWER's defects rather than the round's — they are registered directly above as R-0636 — and the review found one further defect of its own reading, R-0637. TRANSPORT AND SLICES HELD — the scratch file as emitted, `.agent/authored/f009-r11.md` at `45a67196` and `.agent/last_block.md` at `9c83f03f` are all sha256 53fb09f242c458fb3da8c9d8f615668ded9330927d5ff5b4e01b44721a96bbb0 over 30270 bytes and 291 lines, and the reviewer's own ordered extraction gives the five slices PLANF009R11, R0635, LEDGER11, DONE0634 and DECISION15. `.agent/plan.md` at `29086a21` is BYTE-EQUAL to PLANF009R11. THE THREE APPENDS HOLD BY DIRECT COMPARISON: at `37bd4fdc`, `90c59662` and `74de46b2` the previous blob is a byte-exact prefix and each remainder is exactly a newline plus its slice, over 2312, 4964 and 3475 bytes. THE ONE REPLACEMENT IS PROVED AS ONE: at `29ee4b08` the reviewer reconstructed the C4 blob independently by replacing the single `^Landed: R-0634 — ` line of the `90c59662` blob with the DONE0634 bytes, and the reconstruction is BYTE-EQUAL to what landed; `^Landed: ` goes 1 to 0 and `^Done: R-0634 — ` 0 to 1, over a `git show --numstat` of one insertion and one deletion, which is the shape of a replacement and not of an append. THE SETS HELD line-anchored at the round base, C2, C3 and C4: `^- R-\d+ — ` 200, 201, 201 and 201 with every id DISTINCT at each, `^- R-0635 — ` 0, 1, 1 and 1, `^Done: R-\d+ — ` 1, 1, 1 and 2, `^Landed: ` 1, 1, 1 and 0, `^> Next free id` 0 throughout, `^Gate: R\d+ — ` 10, 10, 11 and 11 over that many DISTINCT keys, max id R-0635, item 10's rule giving 199 open at `29ee4b08`, and `^## DECISION F009 D\d+ — ` 14 to 15 in `.agent/decisions.md`, all DISTINCT. THE RANGE HELD: the path set from the round base to `e11fe949` is exactly the nine declared paths other than the handback's with the set difference empty both ways; ten single-parent commits with `git show --numstat` and `git diff --numstat` AGREEING on every cell, insertions 291, 187, 17, 2, 2, 1, 12, 448, 152 and 49, all under the 500-insertion cap; zero marker lines in the three committed state targets; `git ls-files .remedy-wt` 0; and a clean tree. THE SUITES ARE THE REVIEWER'S OWN, run serially in the primary checkout at `fde072f1`: the three groups EXIT 0 at 120, 42 and 507 passed, each equal to the count the handback reported and none of them predicted by it, `ruff check` EXITS 0 over the four paths, and the AST import diff over `packages/orchestration/ui_server.py` reads 62 modules against 63 with `packages.orchestration.command_nonce` the only addition and nothing removed. BOTH PROBES ARE THE REVIEWER'S OWN, in its own disposable worktree at `fde072f1` with the source restored byte-identically and the worktree pruned: against a control of 109 passed, making `lookup_nonce_result` return None unconditionally fails SEVEN node ids — the three door-level replay tests and the four store-level publication tests — and making publication overwrite instead of create-only fails TWO, `test_a_second_publish_of_one_nonce_returns_the_first_body` and `test_concurrent_publishers_of_one_nonce_all_receive_the_same_body`, which are precisely the two that assert the race convergence D8 chose one file per nonce to get. Both readings match the handback's id for id. THE CODE WAS READ AND NOT MERELY GATED: `_parse_record` refuses a boolean status explicitly, which matters because `True` is an `int` in Python and would otherwise become a status code; `lookup_nonce_result` answers every unusable input with a miss rather than an exception, so an unreadable store costs a re-execution instead of a 500; the lookup sits after the credentials, so the store can never answer an unauthenticated caller; and the nonce's character class is asked of the module that owns the path rather than copied into the door, which is the one-spelling-per-concept rule applied where it actually prevents drift. THE REVIEWER'S OWN R11 SPECIFICATION IS WHAT COST THIS ROUND ITS TWO DEVIATIONS, and the round handled both the way the protocol asks: it measured before accepting, applied the stated property, and declared the collision instead of quietly reinterpreting it.
<<<END LEDGER12

Constraints:
1. Apply PLANF009R12, R0636, R0637 and LEDGER12 BYTE FOR BYTE out of the
   committed C0a blob — those are the slices, and this list is what "every slice"
   means anywhere below. Do not retype, rewrap, reflow, reindent or
   whitespace-adjust any of them. If a slice looks wrong to you, apply it as
   written and record the objection in the handback — an objection is recorded,
   never acted on.
2. The commit order is C0a, C0b, C1, C2, C3, C4, C5 and nothing comes between
   them. C1 is the first substantive commit (checklist item 23).
3. WRITE NO CODE. Touch nothing under `packages/`, `apps/`, `tests/` or `docs/`.
   R-0636 and R-0637 each name a repair and this round performs NEITHER: both are
   owed by the round that retires the 501 seam.
4. C2, C3 and C4 are APPENDS to `.agent/live_review.md`, in that order, one
   commit each. Nothing in that file is edited — it is an append-only record.
5. `.remedy-wt/` is gitignored scratch. Every multi-step gate goes into a script
   there; `git status --porcelain` prints 0 lines after each commit.
6. Push with `git push` after C5, the last commit of this session.

Done when:
- G1 `.agent/STOP` ABSENT, read at Step 0 and again before C5.
  `git rev-parse --abbrev-ref HEAD` prints `feature/f009-single-write-channel` at
  every reading. `git status --porcelain` prints 0 lines after each of C0a
  through C5. Report the round base SHA you read at Step 0.
- G2 Transport EQUAL: the scratch file as received, `.agent/authored/f009-r12.md`
  at C0a and `.agent/last_block.md` at C0b all carry the same sha256, byte count
  and line count, equal to the digest in the task prompt. Write C0b from the
  COMMITTED C0a blob, never from the scratch file again.
- G3 Report, per slice, the newline-included sha256, byte count and line count;
  the COUNT of slices from your own ordered extraction out of the committed C0a
  blob; and the aggregate byte count, line count and slice count over them.
- G4 `.agent/plan.md` at C1 is BYTE-EQUAL to PLANF009R12. Report its line count
  against the 50-line cap; `^## Goal$` and `^## Next Steps$` each match exactly
  1 line; the first `\bF\d{3}\b` match is `F009`.
- G5 The appends at C2, C3 and C4 to `.agent/live_review.md`, each proved TWICE
  over independent extractors in the general N-paragraph form: (a) the previous
  blob is a byte-exact PREFIX and the remainder EQUALS a newline plus the slice,
  reported with its sha256, bytes and lines; (b) with N COUNTED BY YOUR SCRIPT
  AND REPORTED, the LAST N blank-line units of the whole file equal the slice's N
  paragraphs IN ORDER. NEGATIVE CONTROL on the FIRST appended paragraph of each:
  flip ONE printable ASCII byte and confirm BOTH readings REJECT it while both
  ACCEPT the unflipped value; report all four outcomes per append. The base for
  C2 is the round base, for C3 the C2 blob, and for C4 the C3 blob.
- G6 Line-anchored over `.agent/live_review.md` at the round base, at C3 and at
  C4: `^- R-\d+ — ` 201, 203 and 203 with all ids DISTINCT at each;
  `^- R-0636 — ` 0, 1 and 1; `^- R-0637 — ` 0, 1 and 1; `^Done: R-\d+ — ` 2 at
  all three; `^Landed: ` 0 at all three; `^> Next free id` 0 at all three;
  `^Gate: R\d+ — ` 11, 11 and 12 over that many DISTINCT keys. Report the max id
  at C4 and the count item 10's rule gives at C4 — line-anchored `^- R-\d+ — `
  minus line-anchored `^Done: R-\d+ — `. State that value in the handback WITH
  the rule and the commit beside it, per DECISION F009 D10, and report what your
  script printed rather than restating it here. Of the `Gate: ` lines at C4,
  report how many match `^Gate: R(\d+) — the R(\d+) entry\.` with the second
  numeral one less than the first, and quote to its first period any that does
  not — the expected reading is eleven matches and one non-match reading
  `Gate: R1 — the F008 R36 entry.`
- G7 In the PRIMARY checkout at C4, run SERIALLY, never two pytest processes at
  once, and report each exit code and its passed-plus-skipped total without
  predicting either: `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
  then `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`.
  Both must EXIT 0. This gate is ordered because R-0607's FIX clause requires it
  of any round whose change set holds an `.agent/` state file.
- G8 The range from the round base to C4: `git diff --name-only` lists EXACTLY
  the paths of the change set above other than `.agent/handoff.md`, the set
  difference empty in both directions, and holds NO path beginning `packages/`,
  `apps/`, `tests/` or `docs/` — constraint 3 as a measurement. Walk
  `git rev-list --reverse` and report, per commit, that it has ONE parent and its
  `git show --numstat` insertions, with `git diff --numstat` AGREEING on every
  cell and every cell equal to the `+/-` column of your handback's `## Commits`
  table (checklist item 28). Every commit stays under the 500-insertion cap of
  AGENTS.md DECISION F104 D1. `^<<<SLICE ` and `^<<<END ` read 0 lines in
  `.agent/plan.md` and `.agent/live_review.md`. Classify this round's own reflog
  entries by the operation before the first `:` in `%gs` and report `amend`,
  `rebase` and `cherry`, which must each be 0; assert no total over the whole
  reflog (R-0601). Report `git ls-files .remedy-wt` as a count.
- G9 The handback carries every mandated section of
  docs/agents/handback_template.md, an item-status table holding exactly one row
  for each of C0a, C0b, C1, C2, C3, C4 and C5, the round base SHA, and one line
  per gate — the raw transcripts go in the round report, not in the handback
  (R-0582). Report its line count against the 100 that a bundle of more than five
  commits allows, and if it exceeds that, carry the AGENTS.md DECISION D15
  stated-cause line naming the count and the mandated content that caused it. Its
  `## Next` section states, in this order: that THIS SESSION ENDED HERE and that
  the round wrote no production code, with the reason; that no `.agent/STOP` is
  present; that the next session's FIRST action is the `.agent/STOP` re-read
  (Phase 1 rule 1) and its SECOND the Open PR Gate (Phase 1 rule 2), which is
  EMPTY because this branch carries no pull request and F009 opens one at its own
  closure; the open-finding count from G6 WITH item 10's rule and the commit named
  beside it; that the next free id is derived with `max` over the line-anchored
  entries and what that gives; that `.agent/candidates.md` is EMPTY; that the next
  round is T003's effect table per DECISION F009 D5, which retires the 501 seam
  and is the round that owes the fixes for R-0636 and R-0637; and that R-0403,
  R-0607, R-0608, R-0609, R-0611, R-0613, R-0622, R-0630, R-0633 and R-0635 stay
  routed to a paydown branch.

Handback:    completion report + rewrite `.agent/handoff.md`. The state block
             repeats this Fortschritt line verbatim: 60 % (T001 gebaut · T002
             gebaut bis auf die Publikation — T003 öffnet die Wirkung) — Schätzung
──────────────────────────────────────────────────────────────
