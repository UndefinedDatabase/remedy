── STEP R32 — F031 Decision inbox ────────────────────────────
Goal:        Record R31's PASS and ship `decisionNonce.ts`, the client-nonce
             minter T003 needs before any answer can be sent: it composes a
             nonce the commands endpoint accepts, or answers `null` when it
             cannot. It is reachable by the shipped vitest config and has no
             caller. THIS ROUND WIRES NOTHING — R33 ships the operator's
             outcome sentence and threads the token through to the card.

Fortschritt: ~97 % (F031 claimed; R1 through R31 landed, R31 gated here ·
             T001 SHIPPED · T002 COMPLETE · T003 answer command, request,
             deep-link and submit seams shipped, nonce seam here, outcome
             sentence and click wiring open) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the
             plan · C2 the R31 gate entry · C3 the nonce module, its tests
             and DECISION F031 D17 · C4 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r32.md                             (C0a)
             .agent/last_block.md                                    (C0b)
             .agent/plan.md                                          (C1)
             .agent/live_review.md                                   (C2)
             apps/ui/src/api/decisionNonce.ts                  (C3, NEW)
             apps/ui/src/api/decisionNonce.test.ts             (C3, NEW)
             .agent/decisions.md                               (C3, D17)
             .agent/handoff.md                                       (C4)
             This list bounds the round's WRITES, not its ACTIONS: the push
             named in G9 is ordered explicitly and is not a file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `3f12697ca6cd14155231f5aa179eaf272ede359c`, the R31 handback
commit and the tip of `feature/f031-decision-inbox`, local and remote EQUAL —
the reviewer measured both at the R31 gate. Stay on that branch; never commit
to `main`. Every SHA-shaped token here resolved under `git cat-file -t`.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md` 747542 bytes and 1275 lines; `^- R-\d+ — ` 246 all
  DISTINCT, maximum `R-0685`; `^Done: R-\d+ — ` 5, so the §3 item 10 open set
  is 241; `^Recurrence: R-` 23; `^Landed: R-` 0. THE GATE SERIES IS SPLIT by
  DECISION F031 D7: `^Gate: R\d+ — ` 19, frozen, and `^Gate: F\d+ R\d+ — ` 12,
  the last four keys being `F031 R27` through `F031 R30`. `^Gate: F031 R31 — `
  occurs 0 times, so LEDGER32's header is the first of its key (§3 item 26).
  THIS ROUND MINTS NO ID AND RESOLVES NONE.
- `.agent/plan.md` 49 lines, 2823 bytes. `docs/roadmap/**` is UNTOUCHED, so
  the §3 docs-round gate is not earned and is not ordered.
- `apps/ui`: `npm run typecheck` exit 0, zero diagnostics on stdout and
  stderr; `npm run test:unit` exit 0 at 27 files and 410 tests, of which
  `decisionSend.test.ts` is 12, `decisionAnswer.test.ts` 20,
  `decisionCard.test.ts` 36, `decisionFilter.test.ts` 20,
  `decisionOrder.test.ts` 16, `decisionFocus.test.ts` 7 and
  `decisionSubmit.test.ts` 10. The six Python suites all exit 0; their counts
  are stated ONCE, in G7.
- `apps/ui/src/api/decisionNonce.ts` IS ABSENT AT THE BASE under
  `git ls-tree`, which is why every gate naming it names C3 and never the
  base (§3 items 21 and 24).
- THE NONCE CLASS IS ALREADY DEFINED AND IS NOT YOURS TO RESTATE.
  `apps/ui/src/api/decisionAnswer.ts` holds `COMMAND_NONCE_PATTERN` as
  `/^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$/`, mirroring `safe_points._ID_RE` on the
  server, and exports `isUsableCommandNonce`. That regex is NOT exported and
  S1 must not copy it: the class stays defined in exactly ONE place.
- NOTHING MINTS A NONCE TODAY. The reviewer grepped `apps/ui/src` for `nonce`;
  all six matching files CONSUME a caller-supplied one, so S1 is this
  browser's first minter.
- NULL IS THIS FEATURE'S WORD FOR UNSENDABLE, which is why S1 answers it
  rather than throwing: `buildDecisionResolveCommand` and
  `buildDecisionSendRequest` already answer `null` for a request that must not
  be sent — an empty job id, an empty token, a blank answer, a nonce outside
  the class, a decision that is not open — so a caller already branching on
  `null` gains no new shape from a minter that cannot mint.
- THE ABSENCE SWEEP, per R-0377's widened counter-measure, over files OUTSIDE
  this change set. `decisionCard.ts`, `decisionAnswer.ts` and
  `DecisionInboxCard.tsx` each say the SEND is still missing, and all three
  STAY TRUE here because this round adds no caller. R33 edits all three
  anyway, so that repair is DEFERRED to it on purpose and is NOT yours.
- THIS BLOCK'S OWN TWO CAPS, measured on its final bytes before emission and
  stated so your re-measurement can disagree with the reviewer's, are 490
  lines TOTAL (DECISION F085 D6) and 400 lines PROSE (DECISION F085 D5). G2
  orders you to report both from the COMMITTED blob.

── Constraints ───────────────────────────────────────────────
1. Apply every authored SLICE BYTE FOR BYTE. Never retype, rewrap or "fix"
   one. If a slice looks wrong, apply it verbatim and DECLARE the
   disagreement: a contradiction in this block is the reviewer's defect.
2. THE PRODUCTION CHANGE, ITS TESTS AND DECISION D17 ARE DESCRIBED, NOT
   SLICED. The numbered specification S1 through S3 fixes behaviour, structure
   and copy; YOU write that code, those tests and that entry under AGENTS.md's
   Mandatory Self-Review Loop and File Editing Safety Rules. Where the spec is
   silent, prefer the neighbouring module's idiom. Where it is WRONG, say so
   in the handback and do the right thing.
3. Slice transport. The reviewer's original is on disk at
   `.remedy-wt/f031-r32.md`. COPY that file to `.agent/authored/f031-r32.md`
   at C0a — never retype it — and mirror it byte-identically into
   `.agent/last_block.md` at C0b. THIS BLOCK STATES NO DIGEST OF ITSELF: a
   file cannot carry its own sha256, so the proof is the disk-to-disk
   comparison G1 orders over four readings, which is what
   docs/agents/self_drive_protocol.md substitutes for the hash-stamp ritual
   when there is no transport. Report the digest YOU measure. Extract every
   slice PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker LINES —
   `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes. Markers never reach a
   target file.
4. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4. No extra commit, none
   dropped, no reordering. C1 is FIRST substantive because this round writes
   the finding ledger (§3 item 23). To correct a landed commit, do NOT add one
   outside this sequence — declare it, and give it its own `## Commits` and
   item-status rows (R-0675).
5. Never amend, rebase, cherry-pick, force-push or rewrite history; never
   delete a branch; never merge; create no pull request.
6. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C4; if present, finish
   the commit in hand, write the handback and stop. NEVER delete that
   sentinel (R-0347).
7. The slices this block carries are the whole text PLANF031R32 and the
   appended text LEDGER32. This paragraph names them and states no count; G2
   orders you to report the count YOUR extractor measured.
8. THE ONE APPEND'S SHAPE, STATED ONCE HERE, WITH EVERY GATE NAMING THIS
   PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED convention
   each slice already ends in a newline, so `.agent/live_review.md` after C2
   is EXACTLY: its blob at C1, then one newline, then LEDGER32 — and it
   receives NOTHING ELSE in that commit, and nothing at all in any other
   commit of this round (R-0657). LEDGER32's own paragraph count is yours to
   measure; this paragraph states no number. `.agent/decisions.md` also GROWS
   at C3 by text YOU author under S3, so no equality gate is ordered over it.
9. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment test is reported and
   no FROM-zero count is ordered (§3 item 15). The plan is a WHOLE-FILE
   replacement and LEDGER32 is an append.
10. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. LEDGER32 carries no
    `- R-` paragraph, no `Done:` line and no `Recurrence:` line, so
    `^- R-\d+ — ` stays 246 with the maximum still `R-0685`, `^Done: R-\d+ — `
    stays 5, `^Recurrence: R-` stays 23 and `^Landed: R-` stays 0, leaving the
    §3 item 10 open set UNCHANGED at 241. WRITE NO `Landed:` and no `Done:`
    line. No landed finding paragraph is edited (§3 item 20).
11. TOUCH NO DOCUMENT AND NO OTHER CODE. Nothing under `docs/`, `packages/`
    or `tests/`, and neither `.agent/context.md` nor either
    `f031_*_inventory.md`. Inside `apps/` ONLY the two NEW paths the change
    set names are written — G8 lists the eleven `apps/` paths that must stay
    out of the range. THIS ROUND WIRES NOTHING: if you find yourself threading
    a token through a component, enabling an answer button, writing the
    operator's outcome sentence, or editing one of the three "nothing posts
    yet" sentences, stop — that is R33's work.
12. Destructive verification runs ONLY in a disposable `git worktree` under
    `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before the G7
    suites. Everything already there is pre-existing scratch belonging to no
    commit, this block's own file included: create no worktree at an existing
    path, and delete nothing you did not create.

── Specification (S1–S3) — the production change ─────────────
S1  THE NONCE, a NEW module `apps/ui/src/api/decisionNonce.ts`, exporting ONE
    function that answers a client nonce the commands endpoint accepts, or
    `null` when it cannot build one.
    THE GUARD IS THE EXPORTED PREDICATE, NEVER A COPIED REGEX. Import
    `isUsableCommandNonce` from `./decisionAnswer` and make it the LAST word:
    whatever this module composes, it answers that value only if the predicate
    accepts it, and `null` otherwise. Do NOT restate the character class as a
    literal — a second copy is a second thing to keep in step with the server.
    THE RANDOMNESS IS A PARAMETER with a default, the same seam DECISION F031
    D16 fixed for the send: declare a local function type answering a string,
    default it to a source naming the browser's own `crypto.randomUUID`, and a
    test then passes its own and never patches a global.
    WHAT IT COMPOSES: a short fixed PREFIX marking this browser as the origin
    of the answer — the nonce becomes a FILENAME in the job's control
    directory, as `decisionAnswer.ts` records — then the source's answer with
    every character OUTSIDE the class removed, the whole truncated so the
    result cannot exceed the 64 characters the class permits. A source whose
    answer sanitises away to nothing yields `null`.
    THE WHY COMMENTS carry the deliberate absences: no clock, no counter, no
    storage, no uniqueness claim beyond the injected source's, and no
    knowledge of what a decision or a command IS.

S2  THE TESTS, a NEW `apps/ui/src/api/decisionNonce.test.ts`, following
    `decisionSubmit.test.ts`'s idiom — a stub source passed in, no global
    touched. Assert AT LEAST: that a well-formed source yields a nonce
    `isUsableCommandNonce` accepts and that it carries the prefix; that the
    source is called exactly once; that a source answering only characters
    outside the class yields `null`; that an empty source yields `null`; that
    a very long source yields a nonce still accepted by the predicate and no
    longer than the class allows; that two DIFFERENT source values yield two
    DIFFERENT nonces, which forbids a hidden constant; and that a source
    answering permitted characters keeps them. Name each test for the property
    it pins.

S3  DECISION F031 D17, appended to `.agent/decisions.md` in the shape D1
    through D16 already use there. CHOSEN: T003's remaining work is split
    across rounds — the nonce here, the operator's outcome sentence and the
    wiring in R33 — because specifying the nonce, that sentence vocabulary,
    the token threading through three components and an async click handler in
    ONE block exceeds the caps DECISION F085 D5 and D6 set; the reviewer
    measured a two-module draft of this block at 435 prose lines against a cap
    of 400 and cut the item rather than the wording. CHOSEN: the nonce answers
    `null` rather than throwing or falling back to a constant, matching every
    other door in this chain. CHOSEN: the character class is enforced by
    importing `isUsableCommandNonce` rather than by a second copy of the
    regex, so the server's rule keeps exactly one mirror in this browser.
    ALTERNATIVE: minting the nonce inline in the click handler, rejected
    because the sanitising branch would then ship untested, which is DECISION
    F031 D5's whole reason. ALTERNATIVE: a nonce built from a clock, rejected
    because a reused value is a replay the write door would have to catch and
    because a clock makes the module untestable without freezing it. REVERSE
    it by inlining the module at its single call site.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R32
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D17.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R32 records R31's PASS and ships `decisionNonce.ts`, the client-nonce minter:
it composes a nonce the commands endpoint accepts, or answers `null` when it
cannot. It has no caller yet; R33 ships the outcome sentence and the wiring.

## Next Steps
1. R33, T003's wiring round: ship `decisionOutcome.ts`, mapping a send's result
   to the sentence and tone an operator reads; thread the server token from
   `RemedyApp`'s `readUrlState` through `RemedyShell` and `RightLivePanel`;
   call the nonce, request, submit and outcome modules on an answer click;
   enable the buttons; and retire the three "nothing posts yet" sentences in
   `decisionCard.ts`, `decisionAnswer.ts` and `DecisionInboxCard.tsx`.
2. The clarification FORM, and the ruling on `NeedsAttentionCard`'s decision
   branch (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, whose
   block also carries the §3 checklist items R-0683, R-0377, R-0419, R-0429
   and R-0560 route there, then closure per
   `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- A SEND THAT NEVER ANSWERS HAS NO DEADLINE. `submitDecisionSendRequest` sets
  no timeout by design (DECISION F031 D16), so R33's handler must not leave a
  button disabled forever on a promise that never settles; that round's block
  carries the requirement explicitly.
- THE SERVER STILL ACCEPTS A BLANK ANSWER AND WRITES IT ONCE. R29 stopped it
  in the browser only; DECISION F031 D14 routes the server-side check to F009,
  which owns the write door, and it is NOT fixed here.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 241 at `3f12697c` and this round leaves it there.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0560,
  R-0574, R-0593, R-0601, R-0622, R-0625, R-0632, R-0672, R-0674, R-0675,
  R-0676, R-0677, R-0678, R-0679, R-0683, R-0684 and R-0685; R-0495 and
  R-0574 are the two Highs.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R32

<<<SLICE LEDGER32
Gate: F031 R31 — the F031 R31 entry. R31 PASSED ON EVERY ONE OF ITS NINE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced cell for cell, and no gate needed a second attempt. TRANSPORT HELD IN ITS STRONGEST FORM for the fourth round running: the reviewer's own scratchpad original `.remedy-wt/f031-r31.md`, the C0a blob committed at `34ed2495`, the C0b blob committed at `5310e3fb` and `.agent/last_block.md` read off disk at `3f12697c` are ALL FOUR byte-identical at sha256 `57f92a38820a7d1f9d192715f6cbcaf5fe67f5152cfc5f50d249b1c709b7d91b` over 40419 bytes and 451 lines, C0a and C0b resolving to the SAME git blob `a87532620322c59bd7f0303c98da2b93ac3b8db9`. The scratchpad original still existed at review time, so this is the PRIMARY disk-to-disk proof and not the §4.9 digest fallback. THE EXTRACTION printed 2 slices, 52 content lines and 451 total, so PROSE was 399 against the 400-line cap DECISION F085 D5 sets and TOTAL 451 against the 490 DECISION F085 D6 sets. THE PLAN at `eb10e19d` equals PLANF031R31 exactly at 2823 bytes and 49 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1, and 49 strictly under the 50 AGENTS.md sets. THE C2 APPEND SATISFIED WHOLE-FILE EQUALITY: `.agent/live_review.md` at `e54dc525` is its C1 blob plus one newline plus LEDGER31, at 736829 + 1 + 10712 = 747542 against an actual 747542, and the SECOND, INDEPENDENT READER AGREED — a blank-line split moves the unit count 322 to 324, N is 2 by that split, and the LAST 2 units equal LEDGER31's 2 paragraphs IN ORDER, trailing newlines rstripped on BOTH sides. THE NEGATIVE CONTROL WAS RUN IN MEMORY, never on the tracked file: one byte flipped at offset 736880, inside the appended text, and both readers REJECT the mutant while both ACCEPT the true file. THE SETS MOVED EXACTLY WHERE THAT BLOCK'S CONSTRAINT 10 ALLOWED AND NOWHERE ELSE: `^- R-\d+ — ` 246 to 246 with the ids ADDED and the ids REMOVED BOTH the EMPTY SET and all 246 DISTINCT, maximum `R-0685` unmoved; `^Done: R-\d+ — ` 5 to 5 with the ids ADDED the EMPTY SET; `^Landed: R-` 0 to 0; `^Recurrence: R-` 22 to 23 with the added id exactly `R-0560` and `^Recurrence: R-0560` moving 0 to 1; `^Gate: R\d+ — ` 19 to 19 frozen and `^Gate: F\d+ R\d+ — ` 11 to 12, the added key exactly `F031 R30`, all keys DISTINCT. The §3 item 10 open set is 241 at `e54dc525`, `- R-0560 — ` still occurs exactly ONCE line-anchored so its landed paragraph was not edited, and `git diff --name-only` over C3 names 3 paths and does NOT name `.agent/live_review.md`. THE RED PROOF IS THE REVIEWER'S OWN AND IT WENT FURTHER THAN THE ONE ORDERED, run in a disposable worktree created at `f0254e78` at a path that did not exist and removed BY THAT EXACT PATH, with `git worktree list` 1 line and the primary's `git status --porcelain` 0 after. UNMUTATED, the ordered line from the primary's `apps/ui` gives REAL exit 0 at 24 files and 385 tests. The worker's own target REPRODUCED: the 11-byte string `: "refused"` occurs exactly ONCE in `decisionSubmit.ts`, and replacing it so every answered request maps to accepted gives REAL exit 1 at 3 failed and 382 passed, the three being the 403, 409 and 429 mapping tests — and the handback's claim that no shorter unique candidate exists CHECKS OUT, `"refused"` alone occurring 2 times and `"accepted"` 2. A SECOND, INDEPENDENT MUTATION the block never ordered confirms the other arm: replacing the catch branch's `outcome: "unreachable", status: 0`, which occurs exactly once, with the refused outcome gives REAL exit 1 at 1 failed and 384 passed, naming the rejected-send test — so S2's tests discriminate a refusal from an acceptance AND an unreachable door from a refusal. Both files were restored byte-identically and that worktree's `git status --porcelain` was 0. THE STRUCTURE IS WHAT S1 ORDERED, measured over the C3 blobs: `decisionSubmit.ts`'s ONLY import is `import type { DecisionSendRequest } from "./decisionSend";`, so the request arrives as a TYPE; the send parameter reads `send: DecisionSendFunction = (sent) =>` continuing onto a call NAMING the global `fetch` and passing the request's own four values through unchanged; `setTimeout`, `Date.now` and `crypto` are 0 each; `answerText`, `decision_id`, `client_nonce`, `taskId` and `buildDecision` are 0 each, so it reaches into no decision field; and in `decisionSubmit.test.ts` `vi.` and `globalThis` are 0, so no global was patched. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY in the primary checkout at `3f12697c`, never two alive at once, every one a REAL exit 0: `npm run typecheck` with zero diagnostics on stdout and stderr; `npm run test:unit` at 27 files and 410 tests, the FILE count 26 to 27 with the one added being `decisionSubmit.test.ts` at 10 tests of its own, and `decisionSend.test.ts` 12, `decisionAnswer.test.ts` 20, `decisionCard.test.ts` 36, `decisionFilter.test.ts` 20, `decisionOrder.test.ts` 16 and `decisionFocus.test.ts` 7 all six UNMOVED; then `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped, and the canary `test_golden_path` 42, every count identical to the base reading. HYGIENE HELD: line-anchored `^<<<SLICE ` and `^<<<END ` are 0 in `.agent/plan.md` at `eb10e19d`, `.agent/live_review.md` at `e54dc525` and all three files C3 writes, against a CONTROL of 2 and 2 over the C0a blob; the range `5ee3024b`..`f0254e78` names 7 paths, none under `docs/`, `packages/` or `tests/` and none of the twelve forbidden paths, with range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`; the six commits `34ed2495` through `3f12697c` are each SINGLE-PARENT with insertions 451, 261, 22, 4, 266 and 58 read from `git diff --numstat`, each under the 500 cap AGENTS.md DECISION F104 D1 sets, and those numbers agree cell for cell with the `+/-` column of that handback's `## Commits` table; `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line and `git status --porcelain` 0. THE BLOCK'S OWN OBJECT IDS RESOLVE: 21 SHA-shaped occurrences, 10 distinct, 9 `commit` and 1 `blob`, failing set EMPTY. THE REFLOG, scoped to this round's entries, reads `commit` throughout, so `amend`, `rebase` and `cherry` are 0 each. THE PUSH DISCHARGED: the local tip, the remote-tracking ref and `git ls-remote origin` all read `3f12697ca6cd14155231f5aa179eaf272ede359c`, no pull request was created, no branch deleted and nothing merged. THE HANDBACK IS INSIDE ITS CAP: 93 lines against the 100-line tier its 6 commits earn, with no overage line needed, and it carries `## Item status` and `## Findings` under those exact headings — the template deviation the R30 entry noted is FIXED and the R31 block's line asking for it worked. Its `Fortschritt:` block is byte-identical to the one that block carried. THE EIGHT DECLARED ITEMS ARE ADJUDICATED AND NONE IS A DEFECT OF THE ROUND: items 4, 5, 6, 7 and 8 are the block being obeyed and its scratch accounted for; item 1, an inline arrow NAMING `fetch` rather than the bare global, is the only reading satisfying both of S1's clauses, since `fetch` is a two-parameter function and is not assignable to the one-parameter send type; item 2, a tenth test widening an explicit "at least", is a widening and not a departure; item 3 is the disclosure G6 asked for and the reviewer reproduced it. NO FINDING IS MINTED. THE VERDICT IS PASS.
<<<END LEDGER32

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output, and report
ONE ENTRY PER GATE in the handback, as briefly as the ordered values allow and
with transcripts kept out (R-0582). "Green" as a word is a finding. Every gate
runs at a commit STRICTLY EARLIER than C4 (§3 item 31); G9's push follows it.

G1  Branch, cleanliness, transport. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`; `.agent/STOP` read from disk
    is ABSENT before C0a and again before C4; `git status --porcelain` line
    count after each of C0a, C0b, C1, C2 and C3 is 0. Then report sha256, byte
    count and line count for FOUR readings — `.remedy-wt/f031-r32.md` before
    C0a, the committed C0a blob, the committed C0b blob, and
    `.agent/last_block.md` off disk after C0b — ALL FOUR EQUAL, and the git
    blob id of C0a's and C0b's file, the SAME id.

G2  Extraction and the block's own two caps. Run your extractor over the
    COMMITTED C0a blob and report the slice count, the CONTENT lines inside
    markers, and the TOTAL — the numbers YOUR extractor printed — then PROSE
    as TOTAL minus CONTENT, against the two caps the Base names. If either is
    exceeded say so plainly and continue; it is the reviewer's to fix.

G3  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R32 under your
    stated newline convention; report slice length, file length and
    convention. NEGATIVE CONTROL: NOT byte-equal to that slice MINUS its
    trailing newline. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` STRICTLY
    under 50.

G4  The C2 append, as ONE equality over the whole file, in the shape
    constraint 8 states — name that paragraph, do not restate its formula.
    Report the boolean and the byte arithmetic against the C1 length you
    measure yourself. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm they
    equal LEDGER32's paragraphs IN ORDER, where N is the number YOUR split
    measured; give the unit count before and after, and STATE YOUR
    TRAILING-NEWLINE HANDLING, because a naive split reports FALSE on a
    byte-perfect file. NEGATIVE CONTROL: flip ONE byte inside the appended
    text; BOTH readers must reject the mutant and BOTH accept the true file.
    Do that flip in memory or under a disposable worktree per constraint 12,
    never on the tracked file.

G5  The ledger sets, base versus C2 in `.agent/live_review.md`, in the shape
    constraint 10 states — report each side of every movement it names, that
    the `- R-` ids ADDED and REMOVED are BOTH the EMPTY SET, that all
    `^- R-\d+ — ` ids are DISTINCT, that the maximum is still `R-0685`, and
    that the `^Done: R-\d+ — ` ids ADDED are ALSO the EMPTY SET.
    `^Gate: R\d+ — ` 19 → 19 UNCHANGED, and `^Gate: F\d+ R\d+ — ` 12 → 13, the
    ADDED key being exactly `F031 R31`, all keys DISTINCT (§3 item 26). Report
    the §3 item 10 open set at C2 and that `git diff --name-only` over C3 does
    NOT name `.agent/live_review.md` — the whole of constraint 8's "nothing at
    all in any other commit".

G6  THE RED PROOF, in a disposable worktree at C3 per constraint 12, so the
    primary checkout is never mutated, with vitest run from the PRIMARY
    checkout's `apps/ui` so the primary's `node_modules` resolves:
      npx vitest run --config <PRIMARY>/apps/ui/vitest.config.ts \
        --root <WORKTREE>/apps/ui src/api/
    Run it UNMUTATED first and report the file and test counts. Then, INSIDE
    THAT WORKTREE, in `apps/ui/src/api/decisionNonce.ts`, DEFEAT S1's
    SANITISING STEP so the source's answer reaches the result unfiltered —
    the confusion a minter would most plausibly ship, since a well-formed
    source makes the filter look redundant. THE TARGET IS YOURS TO NAME,
    because only you have written that file: choose the SHORTEST byte string
    in it that occurs EXACTLY ONCE and expresses that filtering, and report
    the string plus its measured count of 1 (§3 item 25, and R-0560's
    recurrence recorded in the F031 R30 entry — this block deliberately does
    not quote a target it cannot measure). Leave every other byte alone and
    run the same line again. IT MUST GO RED, and S2's out-of-class test is the
    one that must name it. Report the REAL exit code, the NAMES of the failing
    tests, and the failure count YOUR run measured; this block states no
    number. A GREEN means S2's tests never distinguish a sanitised nonce from
    an unsanitised one, and is reported as such rather than worked around.
    Restore the file byte-identically, report that worktree's `git status
    --porcelain` as 0, remove the worktree BY ITS EXACT PATH and report
    `git worktree list` as 1 line after, naming that path.

G7  Structure, then the suites. Report, as counts YOU measured at C3 over
    `decisionNonce.ts`: that `isUsableCommandNonce` is imported from
    `./decisionAnswer` — quote the import line; that the literal `[A-Za-z0-9`
    occurs 0 times, so the character class was not copied; that the random
    source parameter carries a DEFAULT — quote the signature; and that
    `Date.now`, `setTimeout` and `fetch` occur 0 times each. Over
    `decisionNonce.test.ts`, that `vi.` and `globalThis` occur 0 times each,
    so no global was patched. Then in the PRIMARY checkout at the C3 tree, all
    REAL exit 0, run SERIALLY and never two alive at once, with `git worktree
    list` reported as 1 line immediately BEFORE the first of them. At
    `apps/ui`: `npm run typecheck` with ZERO diagnostics on stdout and stderr;
    `npm run test:unit`, reporting the file and test counts YOUR run measured
    — `decisionSend.test.ts` must still be exactly 12,
    `decisionAnswer.test.ts` exactly 20, `decisionCard.test.ts` exactly 36,
    `decisionFilter.test.ts` exactly 20, `decisionOrder.test.ts` exactly 16,
    `decisionFocus.test.ts` exactly 7 and `decisionSubmit.test.ts` exactly 10,
    any movement in any of the seven being a finding, while the FILE count
    must be exactly 28, one more than the Base's 27, that one being
    `decisionNonce.test.ts`; report that new file's own count. Then in Python,
    by these exact command lines with no extra flag:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state gates,
    plus `tests/ui_contracts/`, plus the canary. The reviewer ran all six at
    `3f12697c` with these exact lines and measured in that order 480, 52, 21,
    16, 525 passed with 4 skipped, and 42, every one exit 0. Account for any
    difference.

G8  Markers, paths, commit shapes and object ids. Line-anchored `^<<<SLICE `
    and `^<<<END ` both 0 in `.agent/plan.md` at C1, `.agent/live_review.md`
    at C2 and every file C3 writes, against the same counts over the COMMITTED
    C0a blob as a CONTROL, where they are NOT 0. ONLY the line-anchored
    reading is ordered — this block quotes both markers inside backticks
    mid-line, so a raw SUBSTRING count is unmeetable and is NOT ordered.
    `git diff --name-only <base>..C3` names NO path under `docs/`, `packages/`
    or `tests/`, and none of `.agent/context.md`, either inventory file, or
    these eleven: `apps/ui/src/api/decisionSend.ts`,
    `apps/ui/src/api/decisionSubmit.ts`, `apps/ui/src/api/decisionAnswer.ts`,
    `apps/ui/src/api/decisionCard.ts`, `apps/ui/src/api/decisionFocus.ts`,
    `apps/ui/src/api/remedyApi.ts`, `apps/ui/src/RemedyApp.tsx`,
    `apps/ui/src/components/shell/RemedyShell.tsx`,
    `apps/ui/src/components/panels/RightLivePanel.tsx`,
    `apps/ui/src/components/panels/DecisionInboxCard.tsx` and
    `apps/ui/src/components/panels/ActivityFeedCard.tsx`; the range path set
    MINUS the change set is EMPTY and the change set MINUS the range is
    exactly `.agent/handoff.md`, which C4 writes. Over C0a..C3 report per
    commit that it is single-parent and its INSERTION count — the `+` column
    only, per AGENTS.md DECISION F104 D1 — each under 500; those same numbers
    fill the `+/-` column of the `## Commits` table, derived from
    `git diff --numstat` and NOT from `git commit`'s own summary, and you
    report that the two agree cell for cell (§3 item 28). Report
    `git ls-files .remedy-wt` as 0 and `git ls-files` over the zip glob as 0.
    FOR THE REFLOG state SCOPE and FIELD: over THIS ROUND'S entries only, by
    the OPERATION PREFIX before the first colon of `git reflog --format=%gs`,
    report `amend`, `rebase` and `cherry` each 0 and how many you scoped to.
    Finally extract every SHA-shaped token from the COMMITTED C0a blob with
    the word-bounded pattern matching 7 to 40 hex characters — whose
    boundaries do NOT match the 64-char sha256 digest this block also carries
    — pass each to `git cat-file -t`, and report the token count YOUR
    extractor measured, the type per token, and the FAILING SET, which MUST BE
    EMPTY.

G9  The push. AFTER C4, run `git push origin feature/f031-decision-inbox`. No
    `--force`, no `--force-with-lease`, no history rewrite, no branch
    deletion, no pull request. THAT PUSH'S OUTCOME IS NOT A VALUE OF ANY FILE
    THIS ROUND WRITES: the reviewer measures the pushed tips at the next gate
    and records them in the R32 entry of `.agent/live_review.md`. In
    `## External actions` write the push COMMAND and that sentence. In the
    item-status table the push row is `done`, reason "ordered after C4;
    outcome carried by G9 to the reviewer". Report the real outcome in your
    final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C4 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table per
commit, the item-status table covering C0a through C4, S1 through S3 and the
push, one entry per gate with its real result, the finding counts, and the next
expected action. Carry the `Fortschritt:` block above VERBATIM — count its
lines yourself; no numeral is stated here. Give the item-status table and the
finding counts their own headings, named as the template names them, as R31's
handback did. EVERY NUMERAL YOUR HANDBACK STATES ABOUT A LIST IS COUNTED
MECHANICALLY BEFORE YOU COMMIT IT, or the list is named and NO numeral is given
(R-0441). Any finding count carries the RULE and the COMMIT it was measured at
(F009 D10); a narrower set is "the findings this feature must still act on".

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve it from
AGENTS.md under `### handoff.md` against the commit count constraint 4 fixes,
and report BOTH that count and the tier. R29, R30 and R31 all met that tier, so
it is reachable; if the MANDATED content still does not fit, exceed it and carry
a DECISION D15 line naming your count as a NUMERAL (R-0430) and its cause.

YOUR `## Next` SECTION names, in order: that the next session reads
`.agent/STOP` from disk as Phase 1 rule 1 BEFORE the Open PR Gate as rule 2;
that the R32 verdict is UNRECORDED and owed by the next round's ledger commit
(DECISION F085 D9); and that R33 ships the outcome sentence and the wiring and
is the first round that falsifies the three "nothing posts yet" sentences.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────
