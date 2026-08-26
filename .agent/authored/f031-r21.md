── STEP R21 — F031 Decision inbox ────────────────────────────
Goal:        RECORD ROUND, no code. Write the R20 verdict into the ledger
             under the DECISION F031 D7 key, add the two new instances the
             reviewer found to the OPEN finding R-0593 rather than minting
             an id (§3 item 30), and point the plan at R22, the T002b
             FILTERING round, with the ground the reviewer mapped.

Fortschritt: ~66 % (F031 claimed; R1 through R20 landed, R20 gated here ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             T002b ORDERING SHIPPED and gated · T002b filtering/badge und
             T003 offen) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the
             plan · C2 the R20 gate entry and the R-0593 evidence · C3
             handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r21.md                       (C0a)
             .agent/last_block.md                              (C0b)
             .agent/plan.md                                    (C1)
             .agent/live_review.md                             (C2)
             .agent/handoff.md                                 (C3)
             This list bounds the round's WRITES, not its ACTIONS: the push
             named in G9 is ordered explicitly and is not a file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `a462932f84180a14d39d3a7d5d08e0bc4d5cef88`, the R20
handback commit and the tip of `feature/f031-decision-inbox`, local and
remote EQUAL — the reviewer measured both with `git ls-remote` at the R20
gate. Stay on that branch; create none, never commit to `main`. Every
SHA-shaped token here resolved under `git cat-file -t` before emission;
the types are NOT all `commit` and G8 does not ask them to be.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md` 642904 bytes; `^- R-\d+ — ` 242 all DISTINCT,
  maximum `R-0681`; `^Done: R-\d+ — ` 4, so the §3 item 10 open set is
  238; `^Recurrence: R-` 17; `^Landed: R-` 0. THE GATE SERIES IS SPLIT by
  DECISION F031 D7: `^Gate: R\d+ — ` 19, frozen, and
  `^Gate: F\d+ R\d+ — ` 1, that one being `F031 R19`.
- `.agent/plan.md` 46 lines, 2544 bytes. `.agent/decisions.md` 572273
  bytes, `^## DECISION F031 D\d+` 7 with keys D1 through D7.
  `docs/roadmap/**` is UNTOUCHED this round, so the §3 docs-round gate is
  not earned and is not ordered.
- `apps/ui`: `npm run typecheck` exit 0 with zero diagnostics;
  `npm run test:unit` exit 0 at 22 files and 332 tests.
- The Python suites, every one exit 0: `tests/ui_server/` 474,
  `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate`
  16, `test_golden_path` 42. `tests/ui_contracts/` is NOT ordered this
  round and is not earned: no `apps/` path is in the change set.
- THIS BLOCK'S OWN TWO CAPS, measured on its final bytes before emission
  and stated so your re-measurement can disagree with the reviewer's:
  DECISION F085 D6 budgets a block at 490 lines TOTAL and DECISION F085 D5
  caps its PROSE — TOTAL minus the slice CONTENT inside the markers — at
  400. G3 orders you to report both from the COMMITTED blob.

── Why this round exists ─────────────────────────────────────
R20's verdict is owed by THIS round's ledger commit, which by DECISION
F085 D9 no artefact of R20 could carry. R20 PASSED on all twelve of its
gates, every one re-run by the reviewer off disk, and the reviewer also
re-ran probe A itself rather than accepting the worker's transcript for
it. LEDGER21 is the reading.

THE REVIEWER FOUND TWO MORE INSTANCES OF AN OPEN FINDING while reading
the code R20 shipped, and §3 item 30 forbids minting a second id for a
defect the open set already holds. R-0593 is that record — deliberate
ABSENCE notes left behind by the commit that built the thing they deny —
and EVIDENCE0593 adds the two new instances to it. The R20 worker flagged
both, correctly did NOT edit them under AGENTS.md Scope Control, and left
the call to the reviewer; this is that call.

THIS ROUND SHIPS NO CODE, and R22 is where T002b's filtering lands. The
reason is stated rather than left to be inferred: the filter needs a
CONTROL, `docs/ui/design_reference/` is binding for this feature under
`.agent/context.md`, and a UI control authored without reading that
reference is a design-fidelity violation, which §4.5 makes a BLOCK
CONDITION rather than a finding. R22 reads it first.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap or
   "fix" one. If a slice looks wrong, apply it verbatim and DECLARE the
   disagreement: a contradiction in this block is the reviewer's defect.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r21.md` at C0a and mirrored byte-identically into
   `.agent/last_block.md` at C0b. Extract every slice PROGRAMMATICALLY out
   of the COMMITTED C0a blob by its marker LINES — `<<<SLICE <NAME>` opens,
   `<<<END <NAME>` closes. Marker lines never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3. No extra commit, none
   dropped, no reordering. C1 is FIRST substantive because this round
   writes the finding ledger (§3 item 23). To correct a landed commit, do
   NOT add one outside this sequence — declare it, and give it its own
   `## Commits` and item-status rows (R-0675).
4. Never amend, rebase, cherry-pick, force-push or rewrite history; never
   delete a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C3; if present,
   finish the commit in hand, write the handback and stop. NEVER delete
   that sentinel (R-0347).
6. The slices this block carries are the whole text PLANF031R21 and the
   two appended texts LEDGER21 and EVIDENCE0593. This paragraph names them
   and states no count; G3 orders you to report the count YOUR extractor
   measured.
7. THE ONE APPEND'S SHAPE, STATED ONCE HERE, WITH EVERY GATE NAMING THIS
   PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED
   convention each slice already ends in a newline, so the target after
   the commit is EXACTLY: its blob at the commit's PARENT, then one
   newline, then LEDGER21, then one newline, then EVIDENCE0593 — the two
   slices land in ONE commit, C2, IN THAT ORDER, and `.agent/live_review.md`
   receives NOTHING ELSE in it (R-0657). Each slice's paragraph count is
   yours to measure; this paragraph states no number.
8. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment test is reported
   and no FROM-zero count is ordered (§3 item 15). The plan is a WHOLE-FILE
   replacement and the other two slices are appends.
9. THIS ROUND MINTS NO FINDING ID AND RESOLVES NONE. `^- R-\d+ — ` must be
   242 before and after, maximum staying `R-0681`, and `^Done: R-` and
   `^Landed: R-` UNCHANGED at 4 and 0, so the §3 item 10 open set stays
   238. `^Recurrence: R-` moves 17 to 18, gaining exactly `R-0593`:
   EVIDENCE0593 joins the EXISTING finding and does not replace it, and
   R-0593's own landed paragraph is NOT edited (§3 item 20).
10. TOUCH NO CODE AND NO DOCUMENT. Nothing under `apps/`, `packages/`,
    `tests/` or `docs/` is edited — the two stale comments EVIDENCE0593
    names are recorded here and repaired by R22, never by this round —
    and neither `.agent/decisions.md`, `.agent/context.md` nor either
    `f031_*_inventory.md`. This round rules no DECISION.
11. Destructive verification runs ONLY in a disposable `git worktree`
    under `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before the
    G7 suites. Everything already there is pre-existing scratch belonging
    to no commit, this block's own file included: create no worktree at an
    existing path, and delete nothing you did not create.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R21
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the pull
request #213 merge closing F022. `.agent/live_review.md` is the record and the
id ceiling, `f031_*_inventory.md` the inventories, `.agent/decisions.md` D1–D7.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact, ordered by a documented rule over age and
blocked size, and answerable from the card through the write channel.

## Current Step
R21 is a RECORD round: it writes the R20 verdict into the ledger under the
DECISION F031 D7 key and adds two new instances to the open finding R-0593
instead of minting an id. No code ships. T002b ORDERING is SHIPPED and gated.

## Next Steps
1. R22 ships T002b FILTERING by TYPE, which DECISION F031 D6 narrows from the
   feature file's "filters by type/job" because `DecisionInboxEntry` carries no
   job field. READ `docs/ui/design_reference/` FIRST — `.agent/context.md` makes
   it binding for this feature and a control authored without it is a §4.5 block
   condition, not a finding. R22 also repairs the two comments R-0593 names.
2. T002b BADGE under DECISION F031 D2: it re-derives on refetch over the
   existing SSE stream, no new event kind, D2's two constant-zero counters
   replaced.
3. T003 wires answering through the existing write channel and rules
   `NeedsAttentionCard` (DECISION F031 D4).

## Risks
- THE EMPTY-STATE TRAP IN R22, found by the reviewer while mapping the ground:
  `DecisionInboxCard` opens with `if (decisions.length === 0) return null;`. If a
  filter is applied to the list that guard reads, filtering to zero matches
  unmounts the card AND its own filter control, stranding the operator with no
  way back. The guard must read the UNFILTERED list.
- THE PURE/MARKUP SPLIT under DECISION F031 D5: the filter PREDICATE and the
  list of types offered belong in `apps/ui/src/api/`, where the shipped vitest
  config reaches them; only the control and its `useState` may live in the
  markup, which no test reaches.
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 238 at `a462932f`, unchanged by this round.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0593, R-0601, R-0622,
  R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678 and R-0679;
  R-0495 and R-0574 are the two Highs. R-0593 joins this list at C2.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
<<<END PLANF031R21

<<<SLICE LEDGER21
Gate: F031 R20 — the F031 R20 entry. R20 PASSED ON EVERY ONE OF ITS TWELVE GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly, and R20 earns no finding. TRANSPORT HELD IN ITS STRONGEST FORM, cmp-against-scratchpad rather than the digest fallback: the reviewer's own emitted `.remedy-wt/f031-r20.md` read at this round's base `a462932f`, the C0a blob committed at `2ab7d2bf`, the C0b blob committed at `b6e5eca7`, and `.agent/last_block.md` read off disk at that same base are ALL FOUR byte-identical at sha256 `befdd1eca61639d83457ef34f09d95b3820c134585322fb91f2fadc54dc0ebaa` over 34509 bytes and 479 lines, C0a and C0b resolving to the SAME git blob `ba57b10c9e9eb08277d422ffdf558ada29c5b0fd`. THE EXTRACTION printed 3 slices, 79 content lines and 479 total, so PROSE was 479 − 79 = 400 against the 400-line cap DECISION F085 D5 sets and TOTAL 479 against the 490 DECISION F085 D6 sets — inside both, the prose sitting exactly ON its cap, which the reviewer reached only after cutting the block twice from an initial 492 TOTAL and 413 PROSE. THE PLAN at `e6b865c3` equals PLANF031R20 exactly at 2544 bytes and 46 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1. THE TWO APPENDS SATISFIED WHOLE-FILE EQUALITY, each equal to its parent blob plus one newline plus its slice: `.agent/decisions.md` at `8efcab59` at 570312 + 1 + 1960 = 572273 against an actual 572273, and `.agent/live_review.md` at `bce7badc` at 638246 + 1 + 4657 = 642904 against an actual 642904, the second reader agreeing in both cases. THE HEADING SERIES `^## DECISION F031 D\d+` moved 6 to 7 gaining exactly the key `D7`, all 7 DISTINCT. THE SETS MOVED ONLY WHERE CONSTRAINT 9 ALLOWED: `^- R-\d+ — ` 242 to 242 all DISTINCT, ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0681` unchanged, and `^Done: R-` 4 to 4, `^Landed: R-` 0 to 0 and `^Recurrence: R-` 17 to 17 all UNCHANGED. THE SPLIT SERIES DECISION F031 D7 CREATED BEHAVED EXACTLY AS RULED, which is the reading this round existed to make: `^Gate: R\d+ — ` 19 to 19, frozen as D7 says it is, and `^Gate: F\d+ R\d+ — ` 0 to 1, the added key exactly `F031 R19` — so the F022 seed `Gate: R19` was neither duplicated nor rewritten, and the §3 item 26 collision that was due at this round did not occur. The §3 item 10 open set is 238 at `bce7badc`, unchanged, and R20 MINTED NO ID. THE CODE IS THE POINT OF THIS ROUND AND THE REVIEWER READ ALL OF IT. `apps/ui/src/api/decisionOrder.ts` exports exactly `decisionUrgency` and `orderDecisionInbox`, imports only the model type, orders by `isOpen` then urgency DESCENDING then `id` ASCENDING, and returns `models.slice().sort(...)` so the caller's array is never mutated — the property `remedyApi.test.ts` and `decisionCard.test.ts` depend on from a distance. `DecisionCardModel` gained `ageSeconds: number | null` and `buildDecisionCardModel` returns the local it already computed and formerly discarded; the two exact-shape `toEqual` blocks each gained exactly one line; `RightLivePanel.tsx` differs from its base blob in the import line and the one call site and in nothing else. THE REVIEWER RE-RAN PROBE A ITSELF rather than accepting a transcript for the round's central claim: in a disposable worktree at the round's head, by the block's own command line, the unmutated control passed 16 of 16 and removing the `+ 1` failed 8 — among them "leaves age as the total order among cards that block nothing" and "scores a card that blocks nothing at its own age, not at zero", which are precisely the DECISION F031 D6 departure the `+ 1` exists to make, so that departure is pinned by test and not merely by prose. THE WORKER'S DECLARED S2 DEVIATION IS ACCEPTED AND IS AN IMPROVEMENT ON THE SPEC: the reviewer's S2 named only the non-finite `blockedCount`, and a NEGATIVE one would have scored `(blockedCount + 1) * age` below zero and sorted beneath a null-age card while its own `decisionBlockedLabel` already read "blocks nothing" — the worker clamped it, pinned it with a named test, and declared it rather than silently widening scope. THE OTHER DECLARED ITEMS ARE SOUND: comparing the urgency key rather than subtracting it avoids a NaN comparator over two overflowed scores, the new field's WHY comment is what AGENTS.md's Code Discoverability Conventions ask for, and 16 tests against S8's six is the SPEC's own invitation taken up. HYGIENE HELD: markers 0 in all three targets against a control of 3 and 3 over the C0a blob; the range `a462932f`'s predecessor `ba75103e`..`bce7badc` names 10 paths, none under `docs/`, `packages/`, `tests/` or `apps/cli/`, range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`; per-commit insertions 479, 416, 22, 33, 215 and 2, each single-parent and each under the 500 cap, agreeing with the `## Commits` table cell for cell (§3 item 28); `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line and `git status --porcelain` 0; the reflog read by OPERATION PREFIX over this round's entries shows amend 0, rebase 0 and cherry 0. THE BLOCK'S OWN OBJECT IDS RESOLVE: 21 SHA-shaped occurrences, 13 distinct, failing set EMPTY, one `blob` and twelve `commit`. THE SUITES ARE THE REVIEWER'S OWN, run SERIALLY, never two alive at once, every one a REAL exit 0: `npm run typecheck` with ZERO diagnostics, `npm run test:unit` at 22 files and 332 tests with `decisionCard.test.ts` still exactly 27 and the new `decisionOrder.test.ts` 16, and in Python `tests/ui_server/` 474, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `tests/ui_contracts/` 525 passed with 4 skipped and `test_golden_path` 42 — every Python count identical to the base, which is the expected reading for a round whose only `apps/` paths are reached by no Python test. THE PUSH DISCHARGED, which is the outcome G12 of that round routed here rather than to any file R20 wrote: measured with `git ls-remote`, the local tip and `refs/heads/feature/f031-decision-inbox` are both `a462932f84180a14d39d3a7d5d08e0bc4d5cef88`, and no pull request was created, no branch deleted and nothing merged. ONE ITEM THE WORKER RAISED IS ADJUDICATED HERE AND IS NOT A FINDING: PLANF031R20 reads "`.agent/decisions.md` D1–D7" at C1, one commit before D7 lands at C2, and the worker applied it byte for byte under constraint 1 and declared it, which is the correct behaviour. It is not the §3 item 20 defect, because that item guards a sentence a LATER commit of the same block FALSIFIES and leaves permanently wrong, whereas this one is made TRUE by C2 and is correct for the entire life of the text; AGENTS.md's Commit Gate asks the plan to match the CURRENT WORK, and ruling D7 is that work. THE VERDICT IS PASS.
<<<END LEDGER21

<<<SLICE EVIDENCE0593
Recurrence: R-0593 — TWO FURTHER INSTANCES, in `apps/ui`, found by the F031 R20 WORKER while shipping T002b's ordering, correctly NOT repaired by it under AGENTS.md Scope Control, and confirmed by the reviewer at `a462932f` by reading both files. NO NEW ID IS MINTED: §3 item 30 forbids a second id for a defect the open set already holds, and R-0593 is that record — a deliberate ABSENCE note left standing by the very commit that built the thing it denies. FIRST, `apps/ui/src/api/decisionCard.ts` still reads "Remedy also deliberately does NOT sort, filter or count here: ordering over age and blocked size is T002b's subject", and T002b's ordering SHIPPED at `ab82dacd` as `apps/ui/src/api/decisionOrder.ts`. SECOND, `apps/ui/src/components/panels/DecisionInboxCard.tsx` still reads "Remedy also deliberately does NOT sort, filter, count or answer here: ordering over age and blocked size and the inbox badge are T002b's subject". NEITHER SENTENCE IS FALSE IN ITS LITERAL CLAIM — neither file sorts, and ordering IS T002b's subject — which is exactly why no gate caught them and why they are recorded rather than treated as a block condition. WHAT IS BROKEN IS THE DISCOVERABILITY THE NOTES EXIST TO SERVE: AGENTS.md requires deliberate absences to be documented "where a reader would search for them", and a reader who searches `decisionCard.ts` for the comparator is told only that it is some future slice's subject, with no pointer to the module that now holds it. The reverse pointer exists in `decisionOrder.ts`'s own header, so the gap is one-directional. THE FIX IS R22's, ordered in `.agent/plan.md` at this round's C1: each note names `apps/ui/src/api/decisionOrder.ts` and narrows its remaining absence claim to what is genuinely still absent — filtering, the badge, and in the component also answering. This entry is EVIDENCE ADDED to R-0593 and does not resolve it; R-0593 stays OPEN with its original two instances in `packages/orchestration/release_gate.py` and `pyproject.toml` untouched, and its landed paragraph is not edited (§3 item 20).
<<<END EVIDENCE0593

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output, and
report ONE LINE PER GATE in the handback, transcripts kept out of it
(R-0582). "Green" as a word is a finding. Every gate runs at a commit
STRICTLY EARLIER than C3 (§3 item 31); G9's push runs after it and names
its own carrier.

G1  Branch and cleanliness. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`. `.agent/STOP` read from
    disk is ABSENT before C0a and again before C3. Report
    `git status --porcelain` line count after each of C0a, C0b, C1 and C2;
    each must be 0.

G2  Transport. Report sha256, byte count and line count for FOUR readings:
    `.remedy-wt/f031-r21.md` before C0a, the committed C0a blob, the
    committed C0b blob, and `.agent/last_block.md` off disk after C0b. All
    four must be EQUAL. Report the git blob id of C0a's and C0b's file;
    they must be the SAME id.

G3  Extraction and the block's own two caps. Run your extractor over the
    COMMITTED C0a blob and report the slice count, the CONTENT lines
    inside markers, and the TOTAL line count — the numbers YOUR extractor
    printed. Then report PROSE, computed as TOTAL minus CONTENT, against
    the two caps the Base section names. If either is exceeded, say so
    plainly and continue — an oversize block is the reviewer's defect to
    record, not yours to fix.

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R21 under
    your stated newline convention; report slice length, file length and
    convention. NEGATIVE CONTROL: NOT byte-equal to that slice with its
    trailing newline REMOVED. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l`
    STRICTLY under 50.

G5  The C2 append, as ONE equality over the whole file, in the shape
    constraint 7 states — name that paragraph, do not restate its formula,
    and note that TWO slices land in this one commit IN THE ORDER that
    paragraph fixes. Report the boolean and the byte arithmetic against
    the base length you measure yourself. Report a SECOND, INDEPENDENT
    reading: split the committed file on blank lines, take the LAST N
    units, and confirm they equal LEDGER21's paragraphs followed by
    EVIDENCE0593's IN ORDER, where N is the number YOUR split measured;
    give the unit count before and after. NEGATIVE CONTROL: flip ONE byte
    inside the appended text; BOTH readers must reject the mutant and BOTH
    accept the true file, and the mutant is written only under a
    disposable worktree per constraint 11.

G6  The ledger sets and the SPLIT SERIES, base versus C2 in
    `.agent/live_review.md`: `^- R-\d+ — ` 242 → 242 all DISTINCT, ids
    ADDED and REMOVED both the EMPTY SET, maximum `R-0681` → `R-0681`;
    `^Done: R-` 4 → 4 and `^Landed: R-` 0 → 0, both UNCHANGED.
    `^Recurrence: R-` 17 → 18, the ADDED id being exactly `R-0593`.
    `^Gate: R\d+ — ` 19 → 19 UNCHANGED, and `^Gate: F\d+ R\d+ — ` 1 → 2,
    the ADDED key being exactly `F031 R20`, both keys DISTINCT (§3 item
    26). Report the §3 item 10 open set at C2 — paragraphs minus `Done:`
    lines — which must be 238. Report also that `- R-0593 — ` still occurs
    exactly ONCE, since EVIDENCE0593 joins that finding rather than
    replacing it and constraint 9 forbids editing its landed paragraph.

G7  Markers, paths, hygiene, and the code this round does not touch.
    Line-anchored `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md`
    at C1 and `.agent/live_review.md` at C2, against the same counts over
    the COMMITTED C0a blob as a CONTROL, where they are NOT 0. Report that
    `git diff --name-only <base>..C2` names NO path under `apps/`,
    `packages/`, `tests/` or `docs/`, and neither `.agent/decisions.md`
    nor `.agent/context.md` nor either inventory file; that the range path
    set MINUS the change set is EMPTY and the change set MINUS the range
    is exactly `.agent/handoff.md`, which C3 writes. Over C0a..C2 report
    per commit that it is single-parent and its INSERTION count — the `+`
    column only, per AGENTS.md DECISION F104 D1 — each under 500; those
    same numbers fill the `+/-` column of the `## Commits` table, derived
    from `git diff --numstat` and NOT from `git commit`'s own summary, and
    you report that the two agree cell for cell (§3 item 28). Report
    `git ls-files .remedy-wt` as 0 and `git ls-files` over `*.zip` as 0.
    FOR THE REFLOG state SCOPE and FIELD: over THIS ROUND'S entries only,
    by the OPERATION PREFIX before the first colon of
    `git reflog --format=%gs`, report `amend`, `rebase` and `cherry` each
    0 and how many entries you scoped to. Finally, in the PRIMARY checkout
    at `apps/ui`: `npm run typecheck` REAL exit 0 with ZERO diagnostics,
    and `npm run test:unit` REAL exit 0 with both counts UNCHANGED at the
    base's 22 files and 332 tests — any movement is a finding, and what
    makes them meaningful is the path reading above.

G8  The block's object ids, and the Python suites. Extract every SHA-shaped
    token from the COMMITTED C0a blob with the word-bounded pattern
    `[0-9a-f]{7,40}` — whose boundaries do NOT match the 64-char sha256
    digests this block also carries — and pass each to `git cat-file -t`.
    FAILING means the token does NOT RESOLVE, and THE FAILING SET MUST BE
    EMPTY: this block quotes no non-existent id, so it has no positive
    control. THE TYPES ARE NOT ALL `commit` AND THE GATE DOES NOT ASK THEM
    TO BE — LEDGER21 quotes the git BLOB id
    `ba57b10c9e9eb08277d422ffdf558ada29c5b0fd`, resolved to type `blob`
    before emission, every other token resolving to `commit`. Report the
    token count YOUR extractor measured, the failing set, and the type per
    token. Then, with `git worktree list` reported as 1 line immediately
    BEFORE the first pytest command, run these SERIALLY in the PRIMARY
    checkout at the C2 tree, never two at once, all exit 0:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state
    gates, plus the canary. The reviewer executed all five at the base
    `a462932f` with these exact command lines and no extra flag, and
    measured in that order 474, 52, 21, 16 and 42, every one exit 0.
    Account for any difference.

G9  The push. AFTER C3, run `git push origin feature/f031-decision-inbox`.
    No `--force`, no `--force-with-lease`, no history rewrite, no branch
    deletion, no pull request. THAT PUSH'S OUTCOME IS NOT A VALUE OF ANY
    FILE THIS ROUND WRITES: the reviewer measures the pushed tips at the
    next gate and records them in the R21 entry of `.agent/live_review.md`.
    In `## External actions` write the push COMMAND and that sentence. In
    the item-status table the push row is `done`, reason "ordered after C3;
    outcome carried by G9 to the reviewer". Report the real outcome in
    your final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C3 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table per
commit, the item-status table covering C0a through C3 and the push, ONE
LINE PER GATE with its real result, the finding counts, and the next
expected action. Carry the `Fortschritt:` block above VERBATIM — count its
lines yourself; no numeral is stated here.

EVERY NUMERAL YOUR HANDBACK STATES ABOUT A LIST IS COUNTED MECHANICALLY
BEFORE YOU COMMIT IT, or the list is named and NO numeral is given
(R-0441). Any finding count carries the RULE that produced it and the
COMMIT it was measured at, per DECISION F009 D10; a narrower set is named
"the findings this feature must still act on", never "open" unqualified.

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve it
from AGENTS.md under `### handoff.md` against the commit count constraint
3 fixes, and report BOTH that count and the tier. If the MANDATED content
genuinely does not fit, exceed it and carry a DECISION D15 "Deviations,
declared" line naming your measured count as a NUMERAL (R-0430) and the
mandated content behind it. Never drop a section to fit, and claim no
token cap: that cap was withdrawn.

THIS ROUND ENDS THE SESSION, so your `## Next` section is the next
session's first instruction and names, in order: that it reads
`.agent/STOP` from disk as Phase 1 rule 1 BEFORE the Open PR Gate as rule
2; that the R21 verdict is UNRECORDED and owed by the next round's ledger
commit (DECISION F085 D9); that R22 is T002b FILTERING by TYPE and MUST
read `docs/ui/design_reference/` before authoring any control, per
`.agent/context.md`; and that R22 also repairs the two comments
`Recurrence: R-0593` names.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────
