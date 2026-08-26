── STEP R37 — F031 Decision inbox ────────────────────────────
Goal:        Record R36's PASS and R-0582's recurrence — the handback line cap
             that has been declared against, never met, for four rounds running
             — and APPLY that finding's own cheaper repair in this block's own
             Handback section, so the next handback is the first in this branch
             to fit its tier. THIS ROUND WRITES NO CODE: the whole change set is
             `.agent/` state.

Fortschritt: ~98 % (F031 claimed; R1 through R36 landed, R36 gated here ·
             T001 SHIPPED · T002 COMPLETE · T003 answer command, request,
             deep-link, submit, nonce, outcome sentence and answer flow all
             shipped; component wiring is the last T003 step) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the plan ·
             C2 the R36 gate entry and R-0582's recurrence · C3 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r37.md                             (C0a)
             .agent/last_block.md                                    (C0b)
             .agent/plan.md                                          (C1)
             .agent/live_review.md                                   (C2)
             .agent/handoff.md                                       (C3)
             This list bounds the round's WRITES, not its ACTIONS: the push
             named in G8 is ordered explicitly and is not a file (R-0674).
             `.agent/decisions.md` is NOT in it — this round rules nothing new.

── Base ──────────────────────────────────────────────────────
The round base is `cc7f72e6e341ae9ef9b89b293010a984025ef425`, the R36 handback
commit and the tip of `feature/f031-decision-inbox`; the reviewer read the local
tip, the remote-tracking ref and `git ls-remote origin` at the R36 gate and all
three agreed. Stay on that branch; never commit to `main`. Every SHA-shaped
token here resolved under `git cat-file -t`.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md` 783847 bytes and 1289 lines, ending in a newline;
  `^- R-\d+ — ` 246 all DISTINCT, maximum `R-0685`; `^Done: R-\d+ — ` 5, so the
  §3 item 10 open set is 241; `^Recurrence: R-` 25; `^Landed: R-` 0. THE GATE
  SERIES IS SPLIT by DECISION F031 D7: `^Gate: R\d+ — ` 19, frozen, and
  `^Gate: F\d+ R\d+ — ` 17. `^Gate: F031 R36 — ` occurs 0 times, so LEDGER37's
  header is the first of its key, and the three headers above it read
  `Gate: F031 R33 — the F031 R33 entry.`, `Gate: F031 R34 — the F031 R34
  entry.` and `Gate: F031 R35 — the F031 R35 entry.`, which is the shape its
  own header matches (§3 item 26).
- `- R-0582 — ` occurs exactly ONCE line-anchored, `^Done: R-0582 — ` is 0 and
  `^Recurrence: R-0582` is 0: that finding is OPEN and has no recurrence yet.
  THIS ROUND MINTS NO NEW ID. The reviewer searched the open set for the DEFECT
  itself rather than for an id (§3 item 30) and R-0582 already names it.
- `.agent/plan.md` 2695 bytes and 48 lines. `.agent/decisions.md` 599241 bytes
  and 8046 lines, its last entry `## DECISION F031 D18 (2026-08-26)`, and this
  round does not touch it.
- `docs/roadmap/**` is UNTOUCHED and no file under `apps/` moves, so neither the
  §3 docs-round gate nor any `apps/ui` command is earned. DO NOT RUN ONE.
- The six Python suites at that base, run SERIALLY by the reviewer, every one a
  REAL exit 0: `tests/ui_server/` 480, `test_test_runner` 52,
  `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/`
  525 passed with 4 skipped, and the canary `test_golden_path` 42.
- `git status --porcelain` 0 lines, `git worktree list` 1 line,
  `git ls-files .remedy-wt` 0 and the tracked zip glob 0.
- THIS BLOCK'S OWN TWO CAPS, measured on its final bytes before emission and
  stated so your re-measurement can disagree with the reviewer's, are 490 lines
  TOTAL (DECISION F085 D6) and 400 lines PROSE (DECISION F085 D5). G2 orders
  you to report both from the COMMITTED blob.

── Constraints ───────────────────────────────────────────────
1. Apply every authored SLICE BYTE FOR BYTE. Never retype, rewrap or "fix" one.
   If a slice looks wrong, apply it verbatim and DECLARE the disagreement: a
   contradiction in this block is the reviewer's defect, not yours to repair.
2. Slice transport. The reviewer's original is on disk at
   `.remedy-wt/f031-r37.md`. COPY that file to `.agent/authored/f031-r37.md` at
   C0a — never retype it — and mirror it byte-identically into
   `.agent/last_block.md` at C0b. THIS BLOCK STATES NO DIGEST OF ITSELF: a file
   cannot carry its own sha256, so the proof is G1's disk-to-disk comparison
   over four readings, which docs/agents/self_drive_protocol.md substitutes for
   the hash-stamp ritual when there is no transport. Report the digest YOU
   measure. Extract every slice PROGRAMMATICALLY out of the COMMITTED C0a blob
   by its marker LINES — `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes.
   Markers never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3 — none extra, none dropped,
   none reordered. C1 is FIRST substantive because this round writes the finding
   ledger (§3 item 23). To correct a landed commit do NOT add one outside this
   sequence — declare it, with its own `## Commits` and item-status rows.
4. Never amend, rebase, cherry-pick, force-push or rewrite history; never delete
   a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C3, and REPORT WHAT YOU
   READ rather than the value this block expects; if it is present, finish the
   commit in hand, write the handback and stop. NEVER delete that sentinel
   (R-0347).
6. The slices this block carries are the whole text PLANF031R37 and the appended
   text LEDGER37. This paragraph names them and states no count; G2 orders you
   to report the count YOUR extractor measured.
7. THE APPEND'S SHAPE, STATED ONCE HERE, WITH EVERY GATE NAMING THIS PARAGRAPH
   RATHER THAN RESTATING IT. Under the newline-INCLUDED convention each slice
   already ends in a newline, so `.agent/live_review.md` after C2 is EXACTLY its
   blob before that commit, then one newline, then LEDGER37. It receives NOTHING
   ELSE in that commit and nothing in any other commit of this round (R-0657).
   Paragraph counts are yours to measure.
8. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment test is reported and no
   FROM-zero count is ordered (§3 item 15). The plan is a WHOLE-FILE
   replacement; LEDGER37 is an append.
9. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. LEDGER37 carries no `- R-`
   paragraph and no `Done:` line, so `^- R-\d+ — ` stays 246 with the maximum
   still `R-0685` and `^Done: R-\d+ — ` stays 5, leaving the §3 item 10 open set
   UNCHANGED at 241. It carries ONE `Recurrence:` line, so `^Recurrence: R-`
   moves 25 → 26 and `^Recurrence: R-0582` moves 0 → 1. It carries ONE
   `Gate: F\d+ R\d+ — ` header, so that count moves 17 → 18 with the added key
   exactly `F031 R36`. `^Landed: R-` stays 0: WRITE NO `Landed:` LINE — R-0582
   stays OPEN, because this round applies its cheaper repair to ONE block's
   handback section and the finding asks for the practice to change, not for one
   round to comply. No landed finding paragraph is edited (§3 item 20).
10. THIS ROUND WRITES NO PRODUCTION CODE AND NO TEST. Touch nothing under
    `docs/`, `packages/`, `tests/` or `apps/`, and no `.agent/` file other than
    the five the change set names.
11. Destructive verification runs ONLY inside a disposable `git worktree` under
    `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662). This round needs none:
    G4's negative control runs IN MEMORY and never on the tracked file.
    Everything already under `.remedy-wt/` is pre-existing scratch belonging to
    no commit, this block's own file included — delete nothing you did not
    create.

<<<SLICE PLANF031R37
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `.agent/decisions.md` D1–D18.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R37 records R36's PASS and R-0582's recurrence, and applies that finding's own
cheaper repair: the gate transcript moves to the round report and the handback
keeps only the state the next session needs. This round writes no code.

## Next Steps
1. R38, the COMPONENT round and the LAST step of T003: thread the server token
   from `RemedyApp`'s `readUrlState` through `RemedyShell` and `RightLivePanel`,
   call `answerDecisionCard` on an answer click, render the message's sentence
   keyed by its tone, enable the buttons, and retire the three "nothing posts
   yet" sentences in `decisionCard.ts`, `decisionAnswer.ts` and
   `DecisionInboxCard.tsx`, which are true only while no component calls the
   flow.
2. The clarification FORM, and the ruling on `NeedsAttentionCard`'s decision
   branch (DECISION F031 D4).
3. The integration-gate round per `docs/agents/integration_gate.md`, whose
   block also carries the §3 checklist items R-0683, R-0377, R-0419, R-0429,
   R-0560, R-0582, R-0583 and R-0633 route there, then closure per
   `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- THE DEFAULT DEADLINE CREATES A TIMER IT CANNOT CANCEL, as
  `decisionAnswerFlow.ts`'s own header records: the `() => Promise<void>` seam
  DECISION F031 D18 chose carries no handle, so when the submit wins the
  20-second timer still fires. Named here because R38 wires it to a real click.
- THE SERVER STILL ACCEPTS A BLANK ANSWER AND WRITES IT ONCE. R29 stopped it in
  the browser only; DECISION F031 D14 routes that check to F009, not fixed here.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 241 at `cc7f72e6` and this round leaves it there.
- The findings THIS FEATURE MUST STILL ACT ON are R-0377, R-0403, R-0413,
  R-0419, R-0429, R-0431, R-0441, R-0445, R-0471, R-0495, R-0533, R-0560,
  R-0574, R-0582, R-0583, R-0593, R-0601, R-0622, R-0625, R-0632, R-0633,
  R-0672, R-0674, R-0675, R-0676, R-0677, R-0678, R-0679, R-0683, R-0684 and
  R-0685; R-0495 and R-0574 are the two Highs.
- BLOCK CAPS ARE TWO: 490 lines TOTAL (DECISION F085 D6) and 400 lines PROSE
  (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R37

<<<SLICE LEDGER37
Gate: F031 R36 — the F031 R36 entry. R36 PASSED ON EVERY ONE OF ITS ELEVEN GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced cell for cell. THIS WAS THE ROUND R34 NEVER STARTED, re-delegated under a new number because R34 landed a commit and earned its key (§3 item 26), and it shipped both pure modules T003 still owed. TRANSPORT HELD IN ITS STRONGEST FORM for the eighth round running: the reviewer's own scratchpad original `.remedy-wt/f031-r36.md`, the C0a blob committed at `2761e82c`, the C0b blob committed at `306e43b3` and `.agent/last_block.md` read off disk at `cc7f72e6` are ALL FOUR byte-identical at sha256 `a030211898ef02e5c973fcf337f3df061e48d723fc029f1865e13b7fae3882c7` over 37871 bytes and 481 lines, C0a and C0b resolving to the SAME git blob. THE EXTRACTION printed 3 slices, 81 content lines and 481 total, so PROSE was 400 against the 400-line cap DECISION F085 D5 sets — met EXACTLY, with zero headroom — and TOTAL 481 against the 490 DECISION F085 D6 sets. THE PLAN at `20551e0d` equals PLANF031R36 exactly at 2695 bytes and 48 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1, and 48 strictly under the 50 AGENTS.md sets. BOTH APPENDS SATISFIED WHOLE-FILE EQUALITY in the shape that block's constraint 7 states: `.agent/decisions.md` at `20551e0d` is its base blob plus one newline plus DECISIOND18, at 597218 + 1 + 2022 = 599241 against an actual 599241, and `.agent/live_review.md` at `d68fd069` is its C1 blob plus one newline plus LEDGER36, at 778079 + 1 + 5767 = 783847 against an actual 783847. THE SECOND, INDEPENDENT READER AGREED on the decisions append — a blank-line split moves the unit count 1433 to 1439, N is 6 by that split, the last six units equal DECISIOND18's six paragraphs IN ORDER with trailing newlines rstripped on BOTH sides, and the same six SWAPPED are rejected — while LEDGER36 is a single paragraph, so no order reading was ordered or taken for it. THE NEGATIVE CONTROLS WERE RUN IN MEMORY, never on a tracked file: one byte flipped inside each appended text, and each reader REJECTS its mutant while ACCEPTING the true file. THE SETS MOVED EXACTLY WHERE THAT BLOCK'S CONSTRAINT 9 ALLOWED AND NOWHERE ELSE: `^- R-\d+ — ` 246 to 246 with the ids ADDED and the ids REMOVED BOTH the EMPTY SET and all 246 DISTINCT, maximum `R-0685` unmoved; `^Done: R-\d+ — ` 5 to 5 with the ids ADDED the EMPTY SET; `^Landed: R-` 0 to 0; `^Recurrence: R-` 25 to 25, no recurrence being ordered; `^Gate: R\d+ — ` 19 to 19 frozen and `^Gate: F\d+ R\d+ — ` 16 to 17, the added key exactly `F031 R35`, all keys DISTINCT. The §3 item 10 open set is 241 at `d68fd069`. THE TWO NEW MODULES ARE WHAT S1 THROUGH S5 ORDERED, read off the C4 blobs. In `decisionOutcome.ts` `fetch`, `setTimeout`, `Date.now` and `localStorage` are 0 each, so it is pure; the five statuses are NAMED constants and the mapping is a `switch` with an honest `default`, so no range arithmetic and no `>= 500` branch exists; every sentence is a module-scope `const`; no sentence literal contains a digit, a header name or a URL; and both exported functions return a FRESH object literal rather than a shared constant. The tone rule is S2's exactly — `accepted` `ok`, `unreachable` `warn`, 429 `warn`, and 403, 400, 409, 501 and any unlisted status `error`. In `decisionAnswerFlow.ts` `fetch` and `localStorage` are 0, all four seams are optional with shipped defaults so the exported function is callable as `answerDecisionCard(target, model, text)`, both `null` paths return before the `try` block and therefore reach no submit, and the race is wrapped so no injected seam's rejection escapes. `decisionSubmit.ts` is BYTE-IDENTICAL to its base blob, so the closed outcome union is UNEDITED at `"accepted" | "refused" | "unreachable"`. In both new test files `vi.` and `globalThis` are 0, so no global was patched. THE UI GATES ARE THE REVIEWER'S OWN, run in the primary `apps/ui`: `npm run typecheck` REAL exit 0 with zero diagnostics, and `npm run test:unit` REAL exit 0 at 30 files and 448 tests, the FILE count moving 28 to 30 and the TEST total 419 to 448, a delta of exactly 29 accounted for by `decisionOutcome.test.ts` at 16 and `decisionAnswerFlow.test.ts` at 13, with all eight pre-existing decision test files UNMOVED at `decisionAnswer` 20, `decisionCard` 36, `decisionFilter` 20, `decisionFocus` 7, `decisionNonce` 9, `decisionOrder` 16, `decisionSend` 12 and `decisionSubmit` 10. THE MUTATION PROBES ARE THE REVIEWER'S OWN AND BOTH DISCRIMINATE, run in a disposable worktree created at a path that did not exist and removed BY THAT EXACT PATH, with the primary's `git status --porcelain` 0 lines after the last restore and `git worktree list` 1 line after removal. Unmutated: REAL exit 0 at 2 files and 29 tests. Probe (a), the 429 branch's tone changed from `warn` to `error` over a 61-byte string occurring exactly ONCE: REAL exit 1, 2 failed and 27 passed, the failures being the rate-budget test in `decisionOutcome.test.ts` AND the status-carrying test in `decisionAnswerFlow.test.ts`, so the flow's own tests reach the outcome module's table. Probe (b), the race replaced by a bare `await sent` over a 66-byte string occurring exactly ONCE: REAL exit 1, 3 failed and 26 passed, the three being the never-settles test, the deadline-wins test and the submit-wins-the-race test — two of them by a real 5-second timeout, which is the deadline seam genuinely failing to bound the wait. NO MUTATION CAME BACK GREEN, so neither spec left a branch unreached (R-0633). HYGIENE HELD: line-anchored `^<<<SLICE ` and `^<<<END ` are 0 in the plan and decisions at C1, in the ledger at C2 and in all four files C3 and C4 write, against a CONTROL of 3 and 3 over the C0a blob; the range `cc7f72e6`'s predecessor `ce4da4a1`..`7ac45594` names 9 paths, none under `docs/`, `packages/` or `tests/` and neither `.agent/context.md` nor either inventory file, with range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`; the seven commits `2761e82c` through `cc7f72e6` are each SINGLE-PARENT with insertions 481, 341, 52, 2, 300, 436 and 168 read from `git diff --numstat`, each under the 500 cap AGENTS.md DECISION F104 D1 sets; `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line and `git status --porcelain` 0. THE BLOCK'S OWN OBJECT IDS RESOLVE: 17 SHA-shaped occurrences, 9 distinct, 8 `commit` and 1 `blob`, failing set EMPTY. THE REFLOG, scoped to this round's entries, reads `commit` throughout, so `amend`, `rebase` and `cherry` are 0 each. THE SIX PYTHON SUITES ARE THE REVIEWER'S OWN, run SERIALLY, never two alive at once, every one a REAL exit 0 and every count identical to the base: `tests/ui_server/` 480, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped, and the canary `test_golden_path` 42. THE PUSH DISCHARGED: the local tip, the remote-tracking ref and `git ls-remote origin` all read `cc7f72e6e341ae9ef9b89b293010a984025ef425`, no pull request was created, no branch deleted and nothing merged. THE SIX DECLARED ITEMS ARE ADJUDICATED AND NONE IS A DEFECT OF THE WORKER. Three of them are the round's best work, because each names a place the reviewer's own spec stopped short and none was papered over: S1 and S2 fix a tone for `accepted`, `unreachable` and every `refused` status but state NONE for the unsendable message, and the worker derived `warn` from S2's general rule that `warn` is where sending again could plausibly help — the correct derivation, and the spec should have said so; S4's "IT NEVER THROWS" required a `try`/`catch` the block never ordered, mapping an injected seam's rejection onto the same `unreachable` message a deadline win takes, which is the only reading that satisfies the property as written; and the default deadline creates a timer it cannot cancel, because the `() => Promise<void>` seam S5 chose carries no handle, so when the submit wins that timer still fires — a residue the worker wrote into the module header rather than hiding, and one now carried in the plan's Risks because R38 wires it to a real click. The remaining three are the block being obeyed: C0a and C0b landing while the plan still described R35 is what constraint 3 orders, exit codes read through `subprocess.run(...).returncode` is a method difference over verbatim argv, and no contradiction was found inside the block. ITS `## Next` STATES NO VERDICT, NO COLOUR AND NO PASS for itself, so R-0583's defect did not recur. THE ONE DEFECT IS THE REVIEWER'S AND IT IS R-0582's, recorded beside this entry: the handback is 197 lines against the 100-line tier its 7 commits earn. THE VERDICT IS PASS.

Recurrence: R-0582 — SECOND INSTANCE, and the first outside F086. The defect is the REVIEWER'S, and it is now measurable as a TREND rather than as one round's overage: across the four rounds this branch has gated since, every single handback has declared a DECISION D15 stated-cause overage and not one has met its tier — R33 78 lines against 60, R34 132 against 100, R35 90 against 60 and R36 197 against 100, the last of those very nearly double. R-0582's closing sentence names precisely this outcome as the one that must not happen: "leaving the cap in place and declaring against it forever." WHY IT IS THE SAME FINDING AND NOT A NEW ID, per §3 item 30: R-0582 already rules that the reviewer's blocks ORDER more mandated content than the cap admits, and a second id would be two things to resolve for one rule. WHAT THIS INSTANCE ADDS, AND IT SHARPENS THE DIAGNOSIS. R-0582 read the growth as more mandated CONTENT, and at R36 that is only half true: the reviewer measured the R36 handback's `## Verification` at 80 physical lines carrying ONE entry per gate for eleven gates, hard-wrapped at 87 columns, with no transcript quoted and no section dropped — while R35's handback carried its eight gate entries UNWRAPPED, one enormous physical line each, and measured 90 lines in total. The same content therefore passes or fails a LINE cap according to the wrap width the worker happens to choose, which means the cap as written rewards the least readable formatting and measures a typographic decision rather than a quantity of evidence. That is a second, independent reason the number has stopped carrying information, and it is not one a larger cap would fix. THE CHEAPER REPAIR R-0582 ALREADY NAMED IS APPLIED BY THIS VERY BLOCK, which is the only reason this is a recurrence and not a third round of drift: the reviewer "stops ordering the full transcript into the handback and orders it into the ROUND REPORT instead, keeping the handback to the state the next session needs." R37's Handback section does exactly that — it orders the per-gate detail into the worker's final message and keeps `.agent/handoff.md` to the state AGENTS.md actually names, with verification "real, trimmed" as one line per gate. R-0582 STAYS OPEN, because one block complying is not the practice changing: the standing edit belongs to the §3 checklist and is routed to the integration-gate round's block, beside the items R-0683, R-0377, R-0419, R-0429, R-0560, R-0583 and R-0633 already route there.
<<<END LEDGER37

── Done when ─────────────────────────────────────────────────
Run every gate yourself and record its REAL exit code and REAL output. "Green"
as a word is a finding. Every gate runs at a commit STRICTLY EARLIER than C3
(§3 item 31); G8's push follows it. WHERE TO REPORT WHAT, and this differs from
earlier rounds of this branch on purpose (R-0582): the FULL per-gate detail —
every count, digest, boolean and byte arithmetic below — goes in YOUR FINAL
MESSAGE, which is the round report. `.agent/handoff.md` gets ONE LINE PER GATE:
the gate's name, whether it held, and the one or two values that would matter to
someone resuming cold. Nothing is dropped; it moves.

G1  Branch, cleanliness, transport. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`; report what `.agent/STOP` read
    from disk actually was before C0a and again before C3, per constraint 5;
    `git status --porcelain` line count after each commit through C2 is 0. Then
    report sha256, byte count and line count for FOUR readings —
    `.remedy-wt/f031-r37.md` before C0a, the committed C0a blob, the committed
    C0b blob, and `.agent/last_block.md` off disk after C0b — ALL FOUR EQUAL,
    and the git blob id of C0a's and C0b's file, the SAME id.

G2  Extraction and the block's own two caps. Run your extractor over the
    COMMITTED C0a blob and report the slice count, the CONTENT lines inside
    markers, and the TOTAL — the numbers YOUR extractor printed — then PROSE as
    TOTAL minus CONTENT, against the two caps the Base names. If either is
    exceeded say so plainly and continue; it is the reviewer's to fix.

G3  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R37 under your
    stated newline convention; report slice length, file length and convention.
    NEGATIVE CONTROL: NOT byte-equal to that slice MINUS its trailing newline.
    `^## Goal$` 1, `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G4  The append, as ONE equality over the whole file, in the shape constraint 7
    states — name that paragraph, do not restate its formula. Report the boolean
    and the byte arithmetic for `.agent/live_review.md` at C2 against the
    pre-commit length you measure yourself. Then report a SECOND, INDEPENDENT
    reading: split the committed file on blank lines, take the LAST N units, and
    confirm they equal LEDGER37's paragraphs IN ORDER, where N is the number
    YOUR split measured; give the unit count before and after, and STATE YOUR
    TRAILING-NEWLINE HANDLING, because a naive split reports FALSE on a
    byte-perfect file. That slice carries MORE THAN ONE paragraph, so ORDER is
    load-bearing: report the SWAPPED comparison too, and it must be false.
    NEGATIVE CONTROL: flip ONE byte inside the appended text; BOTH readers must
    reject the mutant and BOTH accept the true file, IN MEMORY only.

G5  The ledger sets, base versus C2 in `.agent/live_review.md`, in the shape
    constraint 9 states — report each side of every movement it names, that the
    `- R-` ids ADDED and REMOVED are BOTH the EMPTY SET, that all `^- R-\d+ — `
    ids are DISTINCT, that the maximum is still `R-0685`, and that the
    `^Done: R-\d+ — ` ids ADDED are ALSO the EMPTY SET. `^Gate: R\d+ — ` 19 → 19
    UNCHANGED, and `^Gate: F\d+ R\d+ — ` 17 → 18, the ADDED key being exactly
    `F031 R36`, all keys DISTINCT (§3 item 26). Report `^Recurrence: R-` 25 → 26,
    that `^Recurrence: R-0582` moves 0 → 1, and `^Landed: R-` 0 → 0. Report the
    §3 item 10 open set at C2 and that `- R-0582 — ` still occurs exactly ONCE
    line-anchored, so its landed paragraph was not edited.

G6  Markers, paths, commit shapes and object ids. Line-anchored `^<<<SLICE ` and
    `^<<<END ` are both 0 in `.agent/plan.md` at C1 and in `.agent/live_review.md`
    at C2, against the same counts over the COMMITTED C0a blob as a CONTROL,
    where they are NOT 0. ONLY the line-anchored reading is ordered — this block
    quotes both markers inside backticks mid-line, so a raw SUBSTRING count is
    unmeetable and is NOT ordered. `git diff --name-only <base>..C2` names NO
    path under `docs/`, `packages/`, `tests/` or `apps/`, and neither
    `.agent/context.md` nor `.agent/decisions.md` nor either inventory file; the
    range path set MINUS the change set is EMPTY and the change set MINUS the
    range is exactly `.agent/handoff.md`, which C3 writes. Over C0a..C2 report
    per commit that it is single-parent and its INSERTION count — the `+` column
    only, per AGENTS.md DECISION F104 D1 — each under 500; those same numbers
    fill the `+/-` column of the `## Commits` table, derived from
    `git diff --numstat` and NOT from `git commit`'s own summary, and you report
    that the two agree cell for cell (§3 item 28). Report `git ls-files
    .remedy-wt` as 0, the tracked zip glob as 0, and `git worktree list` as
    1 line at C2. FOR THE REFLOG state SCOPE and FIELD: over THIS ROUND'S
    entries only, by the OPERATION PREFIX before the first colon of
    `git reflog --format=%gs`, report `amend`, `rebase` and `cherry` each 0 and
    how many entries you scoped to. Finally extract every SHA-shaped token from
    the COMMITTED C0a blob with the word-bounded pattern matching 7 to 40 hex
    characters — whose boundaries do NOT match the 64-char sha256 digests this
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
    plus `tests/ui_contracts/` and the canary. Account for any difference from
    the Base's counts. Report `git worktree list` as 1 line immediately BEFORE
    the first of them. RUN NO `apps/ui` COMMAND: no file under `apps/` moves
    this round, so neither `npm run typecheck` nor `npm run test:unit` is earned
    and neither is ordered.

G8  The push. AFTER C3, run `git push origin feature/f031-decision-inbox`, then
    report that the local tip, the remote-tracking ref and `git ls-remote
    origin` for this branch all read the SAME sha. No `--force`, no
    `--force-with-lease`, no history rewrite, no branch deletion, no pull
    request, nothing merged.

── Handback ──────────────────────────────────────────────────
THIS SECTION IS DELIBERATELY SHORTER THAN THIS BRANCH'S EARLIER ONES, and the
change is finding R-0582's own cheaper repair, applied rather than quoted. Four
handbacks running have declared a DECISION D15 overage; this one is ordered to
FIT. Nothing is dropped — the per-gate detail moves to your final message.

Rewrite `.agent/handoff.md` at C3 per docs/agents/handback_template.md, carrying
exactly: feature and round; branch, base and the commit SHAs; a changed-files
table per commit; an item-status table covering every commit and the push; the
verification as AGENTS.md words it, "real, trimmed" — ONE LINE PER GATE naming
the gate, whether it held, and the value a cold reader would need; the open
findings count with the RULE and the COMMIT it was measured at (F009 D10); your
deviations; and `## Next`. Give the item-status table and the finding counts
their own headings, named as the template names them. Carry the `Fortschritt:`
block above VERBATIM — count its lines yourself; no numeral is stated here — and
if any clause of it is false of the round that actually happened, carry the
ordered bytes UNCHANGED and write the correction BESIDE them. EVERY NUMERAL YOUR
HANDBACK STATES ABOUT A LIST IS COUNTED MECHANICALLY BEFORE YOU COMMIT IT, or
the list is named and NO numeral is given (R-0441).

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve it from
AGENTS.md under `### handoff.md` against the commit count constraint 3 fixes,
and report BOTH that count and the tier. MEASURE THE FILE BEFORE YOU COMMIT IT.
If it is over the tier, that is a real result and you declare it as one — but do
not reach for DECISION D15 before you have first moved detail into the round
report, because that is the move this section exists to make.

YOUR `## Next` SECTION STATES NO VERDICT, NO COLOUR AND NO PASS for this round:
the reviewer has not read the diff when you write it, and a handback that
predicts its own gate is finding R-0583's second instance. Name instead, in
order: that the next session reads `.agent/STOP` from disk as Phase 1 rule 1
BEFORE the Open PR Gate as rule 2; that R37's verdict is NOT YET on disk and the
next reviewed round records it as the `Gate: F031 R37` entry; and that R38 is
the component round and the last step of T003 — the token threaded from
`RemedyApp`'s `readUrlState` through `RemedyShell` and `RightLivePanel`,
`answerDecisionCard` called on a click, its sentence rendered by tone, the
buttons enabled and the three "nothing posts yet" sentences retired.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────
