── STEP R33 — F031 Decision inbox ────────────────────────────
Goal:        Record R32's PASS and the R-0633 recurrence its red proof
             exposed, and point the plan at the wiring round. THIS ROUND
             WRITES NO CODE: its whole change set is `.agent/` state, and the
             finding it persists is the REVIEWER'S OWN defect, which the
             worker caught while executing R32 and which must not die with
             the session that found it (§4.4, findings persist FIRST).

Fortschritt: ~97 % (F031 claimed; R1 through R32 landed, R32 gated here ·
             T001 SHIPPED · T002 COMPLETE · T003 answer command, request,
             deep-link, submit and nonce seams shipped; outcome sentence and
             click wiring open) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the
             plan · C2 the R32 gate entry and R-0633's recurrence ·
             C3 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r33.md                             (C0a)
             .agent/last_block.md                                    (C0b)
             .agent/plan.md                                          (C1)
             .agent/live_review.md                                   (C2)
             .agent/handoff.md                                       (C3)
             This list bounds the round's WRITES, not its ACTIONS: the push
             named in G8 is ordered explicitly and is not a file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `1d29f32264eaea16379ad98207c2a4388705a20b`, the R32 handback
commit and the tip of `feature/f031-decision-inbox`, local and remote EQUAL —
the reviewer measured the pushed tips at the R32 gate and all three readings
agreed. Stay on that branch; never commit to `main`. Every SHA-shaped token
here resolved under `git cat-file -t`.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md` 755073 bytes and 1277 lines; `^- R-\d+ — ` 246 all
  DISTINCT, maximum `R-0685`; `^Done: R-\d+ — ` 5, so the §3 item 10 open set
  is 241; `^Recurrence: R-` 23; `^Landed: R-` 0. THE GATE SERIES IS SPLIT by
  DECISION F031 D7: `^Gate: R\d+ — ` 19, frozen, and `^Gate: F\d+ R\d+ — ` 13.
  `^Gate: F031 R32 — ` occurs 0 times, so LEDGER33's first header is the first
  of its key (§3 item 26).
- `- R-0633 — ` occurs exactly ONCE line-anchored and `^Done: R-0633 — ` and
  `^Recurrence: R-0633` are BOTH 0: that finding is OPEN and has no recurrence
  yet, so LEDGER33's second paragraph is the first of its key. THIS ROUND
  MINTS NO NEW ID — R-0633 already names the defect, and §3 item 30 rules that
  a second id for one defect is two things to resolve.
- `.agent/plan.md` 49 lines, 2803 bytes. `docs/roadmap/**` is UNTOUCHED, so
  the §3 docs-round gate is not earned and is not ordered.
- The six Python suites at that base, run SERIALLY by the reviewer, every one
  exit 0: `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety`
  21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4
  skipped, and the canary `test_golden_path` 42.
- NO CODE GATE IS ORDERED THIS ROUND and none may be reported: the change set
  holds no file under `apps/`, so `npm run typecheck`, `npm run test:unit` and
  any vitest run would measure a tree this round does not touch. The reviewer
  measured them at this base — 28 files and 419 tests, typecheck exit 0 with
  zero diagnostics — and that reading belongs to R32's gate, not to yours.
- THIS BLOCK'S OWN TWO CAPS, measured on its final bytes before emission and
  stated so your re-measurement can disagree with the reviewer's, are 490
  lines TOTAL (DECISION F085 D6) and 400 lines PROSE (DECISION F085 D5). G2
  orders you to report both from the COMMITTED blob.

── Constraints ───────────────────────────────────────────────
1. Apply every authored SLICE BYTE FOR BYTE. Never retype, rewrap or "fix"
   one. If a slice looks wrong, apply it verbatim and DECLARE the
   disagreement: a contradiction in this block is the reviewer's defect.
2. Slice transport. The reviewer's original is on disk at
   `.remedy-wt/f031-r33.md`. COPY that file to `.agent/authored/f031-r33.md`
   at C0a — never retype it — and mirror it byte-identically into
   `.agent/last_block.md` at C0b. THIS BLOCK STATES NO DIGEST OF ITSELF: a
   file cannot carry its own sha256, so the proof is the disk-to-disk
   comparison G1 orders over four readings, which is what
   docs/agents/self_drive_protocol.md substitutes for the hash-stamp ritual
   when there is no transport. Report the digest YOU measure. Extract every
   slice PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker LINES —
   `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes. Markers never reach a
   target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3. No extra commit, none
   dropped, no reordering. C1 is FIRST substantive because this round writes
   the finding ledger (§3 item 23). To correct a landed commit, do NOT add one
   outside this sequence — declare it, and give it its own `## Commits` and
   item-status rows (R-0675).
4. Never amend, rebase, cherry-pick, force-push or rewrite history; never
   delete a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C3; if present, finish
   the commit in hand, write the handback and stop. NEVER delete that
   sentinel (R-0347).
6. The slices this block carries are the whole text PLANF031R33 and the
   appended text LEDGER33. This paragraph names them and states no count; G2
   orders you to report the count YOUR extractor measured.
7. THE ONE APPEND'S SHAPE, STATED ONCE HERE, WITH EVERY GATE NAMING THIS
   PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED convention
   each slice already ends in a newline, so `.agent/live_review.md` after C2
   is EXACTLY: its blob at C1, then one newline, then LEDGER33 — and it
   receives NOTHING ELSE in that commit, and nothing at all in any other
   commit of this round (R-0657). LEDGER33's own paragraph count is yours to
   measure; this paragraph states no number.
8. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment test is reported and
   no FROM-zero count is ordered (§3 item 15). The plan is a WHOLE-FILE
   replacement and LEDGER33 is an append.
9. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. LEDGER33 carries no
   `- R-` paragraph and no `Done:` line, so `^- R-\d+ — ` stays 246 with the
   maximum still `R-0685` and `^Done: R-\d+ — ` stays 5, leaving the §3 item
   10 open set UNCHANGED at 241. It carries ONE `Recurrence:` line, so
   `^Recurrence: R-` moves 23 → 24 and `^Recurrence: R-0633` moves 0 → 1.
   `^Landed: R-` stays 0: WRITE NO `Landed:` LINE — R-0633 stays OPEN, because
   this round widens its evidence rather than discharging it. No landed
   finding paragraph is edited (§3 item 20).
10. TOUCH NO DOCUMENT AND NO CODE. Nothing under `docs/`, `packages/`,
    `tests/` or `apps/`, and neither `.agent/context.md`, `.agent/decisions.md`
    nor either `f031_*_inventory.md`. If you find yourself editing a module, a
    component or a test to make something in this block true, stop and declare
    it: this round records what already happened and changes no behaviour.
11. Destructive verification runs ONLY in a disposable `git worktree` under
    `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662). Everything already
    there is pre-existing scratch belonging to no commit, this block's own
    file included: create no worktree at an existing path, and delete nothing
    you did not create. G4's negative control may instead be done IN MEMORY,
    which is the cheaper route and is explicitly allowed.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R33
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
R33 records R32's PASS and the R-0633 recurrence R32's red proof exposed — a
reviewer gate naming a test its own mutation cannot reach. It writes no code:
the whole change set is `.agent/` state.

## Next Steps
1. R34, T003's wiring round: ship `decisionOutcome.ts`, mapping a send's result
   to the sentence and tone an operator reads; thread the server token from
   `RemedyApp`'s `readUrlState` through `RemedyShell` and `RightLivePanel`;
   call the nonce, request, submit and outcome modules on an answer click;
   enable the buttons; and retire the three "nothing posts yet" sentences in
   `decisionCard.ts`, `decisionAnswer.ts` and `DecisionInboxCard.tsx`.
2. The clarification FORM, and the ruling on `NeedsAttentionCard`'s decision
   branch (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, whose
   block also carries the §3 checklist items R-0683, R-0377, R-0419, R-0429,
   R-0560 and R-0633 route there, then closure per
   `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- A SEND THAT NEVER ANSWERS HAS NO DEADLINE. `submitDecisionSendRequest` sets
  no timeout by design (DECISION F031 D16), so R34's handler must not leave a
  button disabled forever on a promise that never settles.
- THE SERVER STILL ACCEPTS A BLANK ANSWER AND WRITES IT ONCE. R29 stopped it
  in the browser only; DECISION F031 D14 routes the server-side check to F009,
  which owns the write door, and it is NOT fixed here.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 241 at `1d29f322` and this round leaves it there; R-0633 gains a
  recurrence and stays OPEN.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0560,
  R-0574, R-0593, R-0601, R-0622, R-0625, R-0632, R-0633, R-0672, R-0674,
  R-0675, R-0676, R-0677, R-0678, R-0679, R-0683, R-0684 and R-0685; R-0495
  and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R33

<<<SLICE LEDGER33
Gate: F031 R32 — the F031 R32 entry. R32 PASSED ON EVERY ONE OF ITS NINE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced cell for cell. TRANSPORT HELD IN ITS STRONGEST FORM AND IN ITS FULLEST CHAIN for the fifth round running: the reviewer's own scratchpad original `.remedy-wt/f031-r32.md`, the C0a blob committed at `7bb36c02`, the C0b blob committed at `072b1432` and `.agent/last_block.md` read off disk at `1d29f322` are ALL FOUR byte-identical at sha256 `280515d66e57076ed2322200d802475bd2d6d79536d1af8abdc492e4d11ffdc0` over 36268 bytes and 435 lines, C0a and C0b resolving to the SAME git blob `a04ebf42af7599c3c1adabaab1bbe00dc833779b` — and that digest is the one the reviewer measured on its own bytes BEFORE emission, so the chain is closed at both ends. THE EXTRACTION printed 2 slices, 50 content lines and 435 total, so PROSE was 385 against the 400-line cap DECISION F085 D5 sets and TOTAL 435 against the 490 DECISION F085 D6 sets. THE PLAN at `c4a488b5` equals PLANF031R32 exactly at 2803 bytes and 49 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1, and 49 strictly under the 50 AGENTS.md sets. THE C2 APPEND SATISFIED WHOLE-FILE EQUALITY: `.agent/live_review.md` at `a24c3d7c` is its C1 blob plus one newline plus LEDGER32, at 747542 + 1 + 7530 = 755073 against an actual 755073, and the SECOND, INDEPENDENT READER AGREED — a blank-line split moves the unit count 324 to 325, N is 1 by that split, and the last unit equals LEDGER32's single paragraph, trailing newlines rstripped on BOTH sides. THE NEGATIVE CONTROL WAS RUN IN MEMORY, never on the tracked file: one byte flipped inside the appended text, and both readers REJECT the mutant while both ACCEPT the true file. THE SETS MOVED EXACTLY WHERE THAT BLOCK'S CONSTRAINT 10 ALLOWED AND NOWHERE ELSE: `^- R-\d+ — ` 246 to 246 with the ids ADDED and the ids REMOVED BOTH the EMPTY SET and all 246 DISTINCT, maximum `R-0685` unmoved; `^Done: R-\d+ — ` 5 to 5 with the ids ADDED the EMPTY SET; `^Landed: R-` 0 to 0; `^Recurrence: R-` 23 to 23; `^Gate: R\d+ — ` 19 to 19 frozen and `^Gate: F\d+ R\d+ — ` 12 to 13, the added key exactly `F031 R31`, all keys DISTINCT. The §3 item 10 open set is 241 at `a24c3d7c`, and `git diff --name-only` over C3 names 3 paths and does NOT name `.agent/live_review.md`. THE PRODUCTION CHANGE IS WHAT S1 AND S2 ORDERED. `decisionNonce.ts` imports `isUsableCommandNonce` from `./decisionAnswer` and asks that predicate for its LAST WORD on the composed value; the literal `[A-Za-z0-9` occurs 0 times, so the server's character class keeps exactly one mirror in this browser; the random source is a parameter reading `randomSource: NonceRandomSource = () => crypto.randomUUID()`, so the seam is injected and defaulted; and `Date.now`, `setTimeout` and `fetch` are 0 each, so it reads no clock, sets no deadline and opens no socket. In `decisionNonce.test.ts` `vi.` and `globalThis` are 0, so no global was patched. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY in the primary checkout at `1d29f322`, never two alive at once, every one a REAL exit 0: `npm run typecheck` with zero diagnostics on stdout and stderr; `npm run test:unit` at 28 files and 419 tests, the FILE count 27 to 28 with the one added being `decisionNonce.test.ts` at 9 tests of its own, and `decisionSend.test.ts` 12, `decisionAnswer.test.ts` 20, `decisionCard.test.ts` 36, `decisionFilter.test.ts` 20, `decisionOrder.test.ts` 16, `decisionFocus.test.ts` 7 and `decisionSubmit.test.ts` 10 all seven UNMOVED; then `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped, and the canary `test_golden_path` 42, every count identical to the base reading. HYGIENE HELD: line-anchored `^<<<SLICE ` and `^<<<END ` are 0 in `.agent/plan.md` at `c4a488b5`, `.agent/live_review.md` at `a24c3d7c` and all three files C3 writes, against a CONTROL of 2 and 2 over the C0a blob; the range `3f12697c`..`1e01b1b8` names 7 paths, none under `docs/`, `packages/` or `tests/` and none of the eleven forbidden `apps/` paths nor `.agent/context.md`, with range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`; the six commits `7bb36c02` through `1d29f322` are each SINGLE-PARENT with insertions 435, 236, 17, 2, 235 and 48 read from `git diff --numstat`, each under the 500 cap AGENTS.md DECISION F104 D1 sets, and those numbers agree cell for cell with the `+/-` column of that handback's `## Commits` table; `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line and `git status --porcelain` 0. THE BLOCK'S OWN OBJECT IDS RESOLVE: 20 SHA-shaped occurrences, 10 distinct, 9 `commit` and 1 `blob`, failing set EMPTY. THE REFLOG, scoped to this round's entries, reads `commit` throughout, so `amend`, `rebase` and `cherry` are 0 each. THE PUSH DISCHARGED: the local tip, the remote-tracking ref and `git ls-remote origin` all read `1d29f32264eaea16379ad98207c2a4388705a20b`, no pull request was created, no branch deleted and nothing merged. THE HANDBACK IS INSIDE ITS CAP: 95 lines against the 100-line tier its 6 commits earn, carrying `## Item status` and `## Findings` under those exact headings, and no worker-authored `Done:` paragraph anywhere in it. THE TEN DECLARED ITEMS ARE ADJUDICATED AND ONLY ONE IS A DEFECT, AND IT IS THE REVIEWER'S: item 2 is R-0633's recurrence, appended beside this entry. Item 1, an `npm run test:unit --` launcher because this session denies `npx`, is a launcher difference over a byte-identical vitest command line and is accepted. Item 3, mutating the 32-byte `.filter(isCommandNonceCharacter)` rather than the 8-byte `.filter(` because the shorter string cannot be removed without a syntax error, is the correct reading of a uniqueness order whose target must also be removable, and both counts were measured and reported. Item 4, exporting `NonceRandomSource` rather than keeping it unexported, matches `decisionSubmit.ts`'s exported `DecisionSendFunction` and is what the test file needs to type its own stub. Item 5's two literals are a LENGTH and a one-character probe, neither a restatement of the class, and the ordered `[A-Za-z0-9` count of 0 holds. Item 6, the prefix `ui-`, is the worker's choice under a spec that fixed only "a short fixed PREFIX", and it matches the prefix the existing nonce fixture in `decisionSubmit.test.ts` already carries. Items 7 through 10 are the block being obeyed and its scratch accounted for. THE VERDICT IS PASS.

Recurrence: R-0633 — SECOND INSTANCE, and the first outside F009. The defect is the REVIEWER'S, in the F031 R32 block saved at `7bb36c02`, and it was FOUND AND DECLARED BY THE WORKER as deviation 2 of the R32 handback, before the reviewer had read the diff. G6 ordered the sanitising step of `decisionNonce.ts` defeated and then stated "IT MUST GO RED, and S2's out-of-class test is the one that must name it". That test cannot name it. S2's literal out-of-class item passes a source of only forbidden characters, and with the filter defeated that source composes to `ui-!!! /// ???`, which S1's own mandated last-word guard `isUsableCommandNonce` refuses anyway — so the function still answers `null`, the assertion still holds, and the test stays GREEN under the mutation. Only a MIXED source distinguishes a filtered minter from an unfiltered one. THE REVIEWER REPRODUCED ALL OF IT at `1e01b1b8` in a disposable worktree removed by its exact path: unmutated, 25 files and 394 tests at exit 0; with `.filter(isCommandNonceCharacter)` removed, exit 1 at 1 failed and 393 passed, the single failure being `drops every character outside the server's class and mints from what is left` — the test the WORKER ADDED under S2's "assert AT LEAST" precisely because it saw the gap. THE COUNTERFACTUAL WAS MEASURED TOO, which is what makes this a finding rather than a note: with that added test removed and the same mutation applied, the suite gives exit 0 at 393 passed, so G6 AS THE BLOCK WORDED IT WOULD HAVE BEEN SILENTLY VACUOUS — the failure mode this repository spends the most effort refusing. WHY THIS IS A RECURRENCE AND NOT A NEW ID, per §3 item 30: R-0633 is OPEN and already names this defect exactly — a reviewer gate ordering a red-proof whose stated property names a test its own mutation cannot reach — and a second id would be two things to resolve for one rule. WHAT THIS INSTANCE ADDS. R-0633's own instance was an early return ABOVE the mutation point, and its FIX clause reads "derives them by READING THE GUARD'S CONTROL FLOW from the mutation point outward". This instance is a guard BELOW the mutation point: the final `isUsableCommandNonce` check re-establishes the very property the mutation was meant to break, so the observable behaviour is unchanged for the inputs the named test uses. Reading forward from the mutation is therefore not sufficient; the reading must run to the function's RETURN, and any guard between the mutation and the return that can restore the property must be enumerated. The block also broke R-0633's OTHER remedy in the same sentence — "or it names no tests at all and orders only the colour plus report the failing node ids" — because it did order the node ids and then added a naming clause beside them, which is the half that was wrong. Citing the item family while breaking it is what makes this worth recording: the R32 block quoted §3 item 25 and R-0560 in the very gate that broke item 18. THAT EDIT IS ROUTED TO THE INTEGRATION-GATE ROUND'S BLOCK, beside the items R-0683, R-0377, R-0419, R-0429 and R-0560 already route there. R-0633 stays OPEN until the checklist item lands.
<<<END LEDGER33

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output, and report
ONE ENTRY PER GATE in the handback, as briefly as the ordered values allow and
with transcripts kept out (R-0582). "Green" as a word is a finding. Every gate
runs at a commit STRICTLY EARLIER than C3 (§3 item 31); G8's push follows it.

G1  Branch, cleanliness, transport. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`; `.agent/STOP` read from disk
    is ABSENT before C0a and again before C3; `git status --porcelain` line
    count after each of C0a, C0b, C1 and C2 is 0. Then report sha256, byte
    count and line count for FOUR readings — `.remedy-wt/f031-r33.md` before
    C0a, the committed C0a blob, the committed C0b blob, and
    `.agent/last_block.md` off disk after C0b — ALL FOUR EQUAL, and the git
    blob id of C0a's and C0b's file, the SAME id.

G2  Extraction and the block's own two caps. Run your extractor over the
    COMMITTED C0a blob and report the slice count, the CONTENT lines inside
    markers, and the TOTAL — the numbers YOUR extractor printed — then PROSE
    as TOTAL minus CONTENT, against the two caps the Base names. If either is
    exceeded say so plainly and continue; it is the reviewer's to fix.

G3  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R33 under your
    stated newline convention; report slice length, file length and
    convention. NEGATIVE CONTROL: NOT byte-equal to that slice MINUS its
    trailing newline. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` STRICTLY
    under 50.

G4  The C2 append, as ONE equality over the whole file, in the shape
    constraint 7 states — name that paragraph, do not restate its formula.
    Report the boolean and the byte arithmetic against the C1 length you
    measure yourself. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm they
    equal LEDGER33's paragraphs IN ORDER, where N is the number YOUR split
    measured; give the unit count before and after, and STATE YOUR
    TRAILING-NEWLINE HANDLING, because a naive split reports FALSE on a
    byte-perfect file. This slice carries MORE THAN ONE paragraph, so ORDER is
    load-bearing and a set comparison does not discharge it. NEGATIVE CONTROL:
    flip ONE byte inside the appended text; BOTH readers must reject the
    mutant and BOTH accept the true file. Do that flip IN MEMORY, never on the
    tracked file.

G5  The ledger sets, base versus C2 in `.agent/live_review.md`, in the shape
    constraint 9 states — report each side of every movement it names, that
    the `- R-` ids ADDED and REMOVED are BOTH the EMPTY SET, that all
    `^- R-\d+ — ` ids are DISTINCT, that the maximum is still `R-0685`, and
    that the `^Done: R-\d+ — ` ids ADDED are ALSO the EMPTY SET.
    `^Gate: R\d+ — ` 19 → 19 UNCHANGED, and `^Gate: F\d+ R\d+ — ` 13 → 14, the
    ADDED key being exactly `F031 R32`, all keys DISTINCT (§3 item 26). Report
    `^Recurrence: R-` 23 → 24, that `^Recurrence: R-0633` moves 0 → 1, and
    `^Landed: R-` 0 → 0. Report the §3 item 10 open set at C2 and that
    `- R-0633 — ` still occurs exactly ONCE line-anchored, so its landed
    paragraph was not edited.

G6  Markers, paths, commit shapes and object ids. Line-anchored `^<<<SLICE `
    and `^<<<END ` both 0 in `.agent/plan.md` at C1 and `.agent/live_review.md`
    at C2, against the same counts over the COMMITTED C0a blob as a CONTROL,
    where they are NOT 0. ONLY the line-anchored reading is ordered — this
    block quotes both markers inside backticks mid-line, so a raw SUBSTRING
    count is unmeetable and is NOT ordered. `git diff --name-only <base>..C2`
    names NO path under `docs/`, `packages/`, `tests/` or `apps/`, and neither
    `.agent/context.md` nor `.agent/decisions.md` nor either inventory file;
    the range path set MINUS the change set is EMPTY and the change set MINUS
    the range is exactly `.agent/handoff.md`, which C3 writes. Over C0a..C2
    report per commit that it is single-parent and its INSERTION count — the
    `+` column only, per AGENTS.md DECISION F104 D1 — each under 500; those
    same numbers fill the `+/-` column of the `## Commits` table, derived from
    `git diff --numstat` and NOT from `git commit`'s own summary, and you
    report that the two agree cell for cell (§3 item 28). Report
    `git ls-files .remedy-wt` as 0, `git ls-files` over the zip glob as 0, and
    `git worktree list` as 1 line. FOR THE REFLOG state SCOPE and FIELD: over
    THIS ROUND'S entries only, by the OPERATION PREFIX before the first colon
    of `git reflog --format=%gs`, report `amend`, `rebase` and `cherry` each 0
    and how many you scoped to. Finally extract every SHA-shaped token from
    the COMMITTED C0a blob with the word-bounded pattern matching 7 to 40 hex
    characters — whose boundaries do NOT match the 64-char sha256 digest this
    block also carries — pass each to `git cat-file -t`, and report the token
    count YOUR extractor measured, the type per token, and the FAILING SET,
    which MUST BE EMPTY.

G7  The state readers and the canary, in the PRIMARY checkout at the C2 tree,
    all REAL exit 0, run SERIALLY and never two alive at once, by these exact
    command lines with no extra flag:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state gates,
    plus `tests/ui_contracts/`, plus the canary. The reviewer ran all six at
    `1d29f322` with these exact lines and measured in that order 480, 52, 21,
    16, 525 passed with 4 skipped, and 42, every one exit 0. Account for any
    difference. Report `git worktree list` as 1 line immediately BEFORE the
    first of them. NO `apps/ui` COMMAND IS ORDERED and none may be reported,
    for the reason the Base gives.

G8  The push. AFTER C3, run `git push origin feature/f031-decision-inbox`. No
    `--force`, no `--force-with-lease`, no history rewrite, no branch
    deletion, no pull request. THAT PUSH'S OUTCOME IS NOT A VALUE OF ANY FILE
    THIS ROUND WRITES: it is the LAST round this session runs, so its outcome
    is reported in your final message and in `## External actions`, where you
    write the push COMMAND and this sentence. In the item-status table the
    push row is `done`, reason "ordered after C3; outcome reported in the
    final message".

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C3 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table per
commit, the item-status table covering C0a through C3 and the push, one entry
per gate with its real result, the finding counts, and the next expected
action. Carry the `Fortschritt:` block above VERBATIM — count its lines
yourself; no numeral is stated here. Give the item-status table and the finding
counts their own headings, named as the template names them. EVERY NUMERAL YOUR
HANDBACK STATES ABOUT A LIST IS COUNTED MECHANICALLY BEFORE YOU COMMIT IT, or
the list is named and NO numeral is given (R-0441). Any finding count carries
the RULE and the COMMIT it was measured at (F009 D10).

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve it from
AGENTS.md under `### handoff.md` against the commit count constraint 3 fixes,
and report BOTH that count and the tier.

YOUR `## Next` SECTION names, in order: that the next session reads
`.agent/STOP` from disk as Phase 1 rule 1 BEFORE the Open PR Gate as rule 2;
that THIS ROUND'S OWN verdict has no on-disk gate entry BY CONSTRUCTION, being
the last round of the session (§4.13, the terminator), and that the reviewer's
PASS for it lives in this handoff and in the session's final message; and that
R34 is T003's wiring round, the first round that falsifies the three "nothing
posts yet" sentences, and that it must bound a send that never settles.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────
