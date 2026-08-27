── STEP R20 — F031 Decision inbox ────────────────────────────
Goal:        Ship T002b ORDERING under DECISION F031 D6: `DecisionCardModel`
             gains `ageSeconds`, the comparator ships as its own pure module
             with its own test, and `RightLivePanel` orders the inbox before
             handing it to the card. RULE DECISION F031 D7 first — the
             feature-qualified ledger key — then record the R19 verdict
             under it.

Fortschritt: ~64 % (F031 claimed; R1 through R19 landed and gated ·
             T001 SHIPPED · T002a MODEL shipped, wired and RENDERED ·
             T002b ORDERING ships here · T002b filtering/badge und T003
             offen) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1 the
             plan · C2 DECISION F031 D7 · C3 the code · C4 the R19 gate
             entry · C5 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r20.md                       (C0a)
             .agent/last_block.md                              (C0b)
             .agent/plan.md                                    (C1)
             .agent/decisions.md                               (C2)
             apps/ui/src/api/decisionCard.ts                   (C3)
             apps/ui/src/api/decisionCard.test.ts              (C3)
             apps/ui/src/api/decisionOrder.ts                  (C3, new)
             apps/ui/src/api/decisionOrder.test.ts             (C3, new)
             apps/ui/src/components/panels/RightLivePanel.tsx  (C3)
             .agent/live_review.md                             (C4)
             .agent/handoff.md                                 (C5)
             This list bounds the round's WRITES, not its ACTIONS: the push
             named in G12 is ordered explicitly and is not a file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `ba75103eecc4c111f99ddd9c4cf6483b3c179d83`, the R19
handback commit and the tip of `feature/f031-decision-inbox`, local and
remote EQUAL — the reviewer measured both with `git ls-remote` at the R19
gate. Stay on that branch; create none, never commit to `main`. Every
SHA-shaped token here resolved under `git cat-file -t` before emission;
the types are NOT all `commit` and G12 does not ask them to be.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md` 638246 bytes; `^- R-\d+ — ` 242 all DISTINCT,
  maximum `R-0681`; `^Done: R-\d+ — ` 4, so the §3 item 10 open set — the
  first pattern's paragraphs minus the second's lines — is 238;
  `^Recurrence: R-` 17; `^Landed: R-` 0; `^Gate: R\d+ — ` 18 carrying the
  keys `R1` through `R18`, PLUS one further `Gate: R\d+ — ` line whose key
  is `R19` and whose body is F022's, making 19 in that pattern and 0 in
  `^Gate: F\d+ R\d+ — `. That seed is what C2 rules about.
- `.agent/plan.md` 49 lines, 3004 bytes. `.agent/decisions.md` 570312
  bytes, `^## DECISION F031 D\d+` 6 with keys D1 through D6.
  `docs/roadmap/**` is UNTOUCHED this round, so the §3 docs-round gate is
  not earned and is not ordered.
- `apps/ui`: `npm run typecheck` exit 0 with zero diagnostics;
  `npm run test:unit` exit 0 at 21 files and 316 tests, of which
  `src/api/decisionCard.test.ts` alone reports 27.
- The Python suites, every one exit 0: `tests/ui_server/` 474,
  `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate`
  16, `test_golden_path` 42, and `tests/ui_contracts/` 525, the last
  EARNED by C3 editing `RightLivePanel.tsx`.
- `apps/ui/src/api/decisionOrder.ts` does NOT exist at this base, and
  `ageSeconds` occurs in `apps/ui/src` only as a parameter of
  `decisionAgeLabel` and as the local at `decisionCard.ts:170`, so the
  name is free at module scope.
- THIS BLOCK'S OWN TWO CAPS, measured on its final bytes before emission
  and stated so your re-measurement can disagree with the reviewer's:
  DECISION F085 D6 budgets a block at 490 lines TOTAL and DECISION F085 D5
  caps its PROSE — TOTAL minus the slice CONTENT inside the markers — at
  400. G3 orders you to report both from the COMMITTED blob.

── Why this round exists ─────────────────────────────────────
R19's verdict is owed by THIS round's ledger commit, which by DECISION
F085 D9 no artefact of R19 could carry. R19 PASSED on all ten of its
gates, every one re-run by the reviewer off disk; LEDGER20 is the reading.

THE KEY THAT ENTRY WOULD USE IS ALREADY TAKEN, which is why C2 precedes
C4. The reviewer read all 19 gate headers at the base: the series is keyed
by the round an entry is ABOUT, not the round that writes it, so R19's
entry keys `Gate: R19` — and a `Gate: R19` line inherited from F022
already sits in the file. DECISION F031 D7 rules the feature-qualified key
BEFORE the entry is written, because §3 item 20 forbids repairing it
afterwards by rewriting.

THE ORDERING RULE NEEDS NO RULING: DECISION F031 D6 fixed it at
`24b47b3b`, mirrored at `75d4b532`; C3 implements it and rules nothing.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap or
   "fix" one. If a slice looks wrong, apply it verbatim and DECLARE the
   disagreement: a contradiction in this block is the reviewer's defect.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r20.md` at C0a and mirrored byte-identically into
   `.agent/last_block.md` at C0b. Extract every slice PROGRAMMATICALLY out
   of the COMMITTED C0a blob by its marker LINES — `<<<SLICE <NAME>` opens,
   `<<<END <NAME>` closes. Marker lines never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4, C5. No extra
   commit, none dropped, no reordering. C1 is FIRST substantive because
   this round writes the finding ledger (§3 item 23); C2 precedes C4
   because C4's header obeys the rule C2 lands. To correct a landed
   commit, do NOT add one outside this sequence — declare it, and give it
   its own `## Commits` and item-status rows (R-0675).
4. Never amend, rebase, cherry-pick, force-push or rewrite history; never
   delete a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C5; if present,
   finish the commit in hand, write the handback and stop. NEVER delete
   that sentinel (R-0347).
6. THE PRODUCTION CHANGE IS DESCRIBED, NOT SLICED. The numbered SPEC below
   fixes behaviour, seam, public surface and honesty rules; YOU write the
   TypeScript under AGENTS.md's self-review loop and its naming
   conventions. The slices this block carries are the whole text
   PLANF031R20, the appended text DECISIOND7 and the appended text
   LEDGER20 — all three `.agent/` state. This paragraph names them and
   states no count; G3 orders you to report the count YOUR extractor
   measured.
7. THE TWO APPENDS' SHAPE, STATED ONCE HERE, WITH EVERY GATE NAMING THIS
   PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED
   convention each slice already ends in a newline, so the target after
   the commit is EXACTLY: its blob at the commit's PARENT, then one
   newline, then the slice. DECISIOND7 goes to `.agent/decisions.md` at
   C2 and LEDGER20 to `.agent/live_review.md` at C4, and each of those
   commits receives NOTHING ELSE (R-0657). Each slice's paragraph count is
   yours to measure; this paragraph states no number.
8. THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment test is reported
   and no FROM-zero count is ordered (§3 item 15). The plan is a WHOLE-FILE
   replacement and the other two slices are appends.
9. THIS ROUND MINTS NO FINDING ID. `^- R-\d+ — ` must be 242 before and
   after, maximum staying `R-0681`, and `^Done: R-`, `^Landed: R-` and
   `^Recurrence: R-` all UNCHANGED at 4, 0 and 17 — this round resolves
   nothing and registers nothing, so the §3 item 10 open set stays 238.
10. TOUCH NO DOCUMENT AND NO OTHER CODE. Nothing under `docs/`,
    `packages/`, `tests/` or `apps/cli/` is edited, no `apps/ui` file
    outside the change set is edited, and neither `.agent/context.md` nor
    either `f031_*_inventory.md` — landed evidence is corrected by dating
    in a later round, never by editing (§3 item 20).
11. Destructive verification runs ONLY in a disposable `git worktree`
    under `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before the
    G11 suites. Everything already there is pre-existing scratch belonging
    to no commit, this block's own file included: create no worktree at an
    existing path, and delete nothing you did not create.
12. `npm run lint` is NOT ordered: R-0622 records that eslint parses no
    TypeScript here. `typecheck` and `test:unit` ARE ordered (G6).

── The production change, specified not sliced ───────────────
S1 NEW MODULE `apps/ui/src/api/decisionOrder.ts`, exporting exactly two
   names: `decisionUrgency(model: DecisionCardModel): number` and
   `orderDecisionInbox(models: readonly DecisionCardModel[]):
   DecisionCardModel[]`. It imports the model type from `./decisionCard`
   and nothing else. DECISION F031 D5 rules F031's logic into this pure
   layer, which the shipped vitest config reaches.
S2 `decisionUrgency` IS `(blockedCount + 1) * age`, the rule DECISION F031
   D6 fixes. `age` is `model.ageSeconds` when that is a finite number
   greater than 0, and 0 otherwise — null, non-finite and negative all
   score 0. A non-finite `blockedCount` counts 0. NO INPUT MAKES IT THROW.
S3 `orderDecisionInbox` returns a NEW array and never mutates, reorders or
   otherwise touches the array it is given. Its order is three keys, in
   this order: `isOpen` true before false; then `decisionUrgency`
   DESCENDING; then `id` ASCENDING under the default string comparison.
   `buildDecisionCardModel` defaults `id` to the empty string, so the
   order is TOTAL and a shuffled input has exactly one answer.
S4 `DecisionCardModel` in `apps/ui/src/api/decisionCard.ts` GAINS ONE
   FIELD, `ageSeconds: number | null`, and `buildDecisionCardModel`
   returns in it the local of that same name it already computes and
   currently discards. Place the field next to `ageLabel` so the formatted
   and the raw age read together. No other field changes, no signature
   changes, and `decisionCardModels` keeps the endpoint's order.
S5 THE TWO EXACT-SHAPE ASSERTIONS in `apps/ui/src/api/decisionCard.test.ts`
   — the `toEqual` of the test named "flattens a full card into the fields
   a renderer projects" and the `toEqual` of the test named "renders a card
   with every optional field absent without throwing" — each gain the ONE
   line the new field requires, and nothing else in that file changes. The
   test named "preserves the order the endpoint sent" stays exactly as is.
S6 THE SEAM is `apps/ui/src/components/panels/RightLivePanel.tsx`, whose
   one line passing `dashboard.decisionInbox` to `DecisionInboxCard`
   instead passes it through `orderDecisionInbox`. That import and that
   call are the ONLY changes to the file. The projection in
   `remedyApi.ts` is NOT touched: DECISION F031 D6 rules that ordering
   ships as its own comparator applied where the inbox is handed to the
   card, and `remedyApi.test.ts` pins the endpoint's order.
S7 THE WHY COMMENTS. The module header carries ONE fact — that the rule is
   DECISION F031 D6's, named as such — plus the deliberate-absence
   sentence a reader will search for: Remedy deliberately does NOT sort in
   `decisionCardModels`, so the rule stays visible in one place. Each
   exported function's one-line WHY sits directly above its definition,
   per AGENTS.md's Code Discoverability Conventions. Say WHY the `+ 1`
   exists at the expression itself: DECISION F031 D6 gives the reason and
   a reader standing at the expression will not have it.
S8 NEW TEST `apps/ui/src/api/decisionOrder.test.ts` pins, at least: a
   shuffled document yielding exactly one order; open cards before closed
   ones whatever their urgency; the `+ 1` making age the total order among
   cards that block NOTHING, which a literal product would tie; a null
   `ageSeconds` scoring 0 and sorting last within its group; `id`
   ascending breaking an exact urgency tie; and the input array left
   unmutated. Report the count YOUR run measured — this paragraph orders
   no numeral. Add cases the SPEC missed where you find one, and say so.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R20
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
R20 ships T002b ORDERING under DECISION F031 D6: `DecisionCardModel` gains
`ageSeconds`, the comparator ships as `apps/ui/src/api/decisionOrder.ts` with its
own test, and `RightLivePanel` orders the inbox before handing it to the card.
R20 also rules DECISION F031 D7, the feature-qualified ledger key, and records
the R19 verdict under it.

## Next Steps
1. T002b FILTERING by type — DECISION F031 D6 narrows the feature file's
   "filters by type/job" to TYPE alone, `DecisionInboxEntry` carrying no job
   field, so the job filter waits on T003's deep links.
2. T002b BADGE under DECISION F031 D2: it re-derives on refetch over the
   existing SSE stream, no new event kind, D2's two constant-zero counters
   replaced.
3. T003 wires answering through the existing write channel and rules
   `NeedsAttentionCard` (DECISION F031 D4).

## Risks
- THE SEED-KEY COLLISION IS RULED, not merely noted: `.agent/live_review.md`
  holds a `Gate: R19` line inherited from F022, so DECISION F031 D7
  feature-qualifies every gate key from the R19 entry onward and the landed seed
  is never rewritten (§3 item 20).
- Open findings, by the rule and commit DECISION F009 D10 requires: per §3 item
  10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line — the
  set is 238 at `ba75103e`.
- The findings THIS FEATURE MUST STILL ACT ON are R-0403, R-0413, R-0431,
  R-0441, R-0445, R-0471, R-0495, R-0533, R-0574, R-0601, R-0622, R-0625,
  R-0632, R-0672, R-0674, R-0675, R-0676, R-0677, R-0678 and R-0679; R-0495 and
  R-0574 are the two Highs.
- BLOCK CAPS ARE TWO, not one: 490 lines TOTAL (DECISION F085 D6) and 400 lines
  PROSE (DECISION F085 D5); every block states and re-measures both.
- THE SHIPPED MARKUP IS REACHED BY NO TEST, which DECISION F031 D5 rules its own
  feature, so this round's logic lives in the pure layer under `apps/ui/src/api/`
  and only the one-call wiring lands in `RightLivePanel.tsx`.
<<<END PLANF031R20

<<<SLICE DECISIOND7
## DECISION F031 D7 (2026-08-26) — the finding ledger's gate key is feature-qualified from the R19 entry onward

CHOSEN. Every `Gate:` entry `.agent/live_review.md` gains from this round onward
is headed `Gate: F031 R<n> — the F031 R<n> entry.` The unqualified `Gate: R<n> — `
form is retired for new entries on this branch, and no landed entry is touched.

WHY. This branch's record carries a `Gate: R19` line whose body is F022's, a seed
inherited when the ledger was reset from that feature's, alongside the keys `R1`
through `R18` from F031's own rounds. The series is keyed by the round an entry is
ABOUT, not by the round that writes it, and DECISION F085 D9 owes R19's verdict to
the NEXT round's ledger commit — so the entry recording it keys `Gate: R19` and
duplicates that seed on the exact string a later reader searches by. That is the
§3 item 26 defect, whose earlier instance left two paragraphs answering to one key.

WHY NOT REWRITE THE SEED. §3 item 20 forbids editing landed record text: a dated
correction is how this record stays honest, and an overwritten entry is worse than
a stale one. The seed also belongs to F022's history, which this branch has no
standing to edit.

WHY NOT SKIP THE ENTRY. R19's verdict would then live only in `.agent/handoff.md`,
which every round rewrites, so it would be unrecoverable one round later. The §4
item 13 terminator carve-out reaches only the LAST round of a branch, and R19 is
not that round.

CONSEQUENCE, declared so no later gate reads the split series as drift. The file
carries two header shapes for the rest of this branch: `^Gate: R\d+ — ` stops
growing where it stands, and `^Gate: F\d+ R\d+ — ` is the series that grows from
here. A gate counting gate entries names BOTH patterns, because neither alone is
the count.

REVERSE IT. Delete this decision and its heading, and head later entries
`Gate: R<n> — ` again, accepting the duplicate key. No code reads either shape.
<<<END DECISIOND7

<<<SLICE LEDGER20
Gate: F031 R19 — the F031 R19 entry, and the first written under DECISION F031 D7. R19 PASSED ON EVERY ONE OF ITS TEN GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly, and R19 earns no finding. TRANSPORT HELD IN ITS STRONGEST FORM, cmp-against-scratchpad rather than the digest fallback: the reviewer's own emitted `.remedy-wt/f031-r19.md` read at this round's base `ba75103e`, the C0a blob committed at `8171d403`, the C0b blob committed at `a0f70a9e`, and `.agent/last_block.md` read off disk at that same base are ALL FOUR byte-identical at sha256 `922693ee69434f9e53449492ea94e790074a5c0f5be7b8f193fbca7b350ee54c` over 32110 bytes and 383 lines, C0a and C0b resolving to the SAME git blob `43e2018218e06a256fe8e18a46cd7dca3ff5d57d`. THE EXTRACTION printed 4 slices, 54 content lines and 383 total, so PROSE was 383 − 54 = 329 against the 400-line cap DECISION F085 D5 sets and TOTAL 383 against the 490 DECISION F085 D6 sets: the first block to measure both, and inside both. THE PLAN at `3d2a3be2` equals PLANF031R19 exactly at 3004 bytes and 49 lines, with the trailing-newline-removed control FALSE, `^## Goal$` 1 and `^## Next Steps$` 1. THE ONE PAIR was a REWRITE and behaved as one: LANDEDFROM occurred exactly 1 time in `.agent/live_review.md` at the base and 0 after `a0ece183`, DONE0681 exactly 1 after, `git diff --numstat` for that commit named `.agent/live_review.md` alone at 1 and 1, and the file moved 629198 to 631576 bytes, exactly the +2378 the two slices' lengths predict. THE APPEND at `1e9d3a83` satisfied whole-file equality — parent blob plus one newline plus the slice, 631576 + 1 + 6669 = 638246 against an actual 638246 — and a SECOND, INDEPENDENT reader agreed: a blank-line split moved 299 units to 301 and its last 2 units equal LEDGER19's 2 paragraphs IN ORDER. THE SETS MOVED ONLY WHERE CONSTRAINT 9 ALLOWED: `^- R-\d+ — ` 242 to 242 all DISTINCT, ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0681` unchanged; `^Landed: R-` 1 to 0 and `^Done: R-` 3 to 4 gaining exactly `R-0681`; `^Recurrence: R-` 16 to 17 gaining exactly `R-0385`; `^Gate: R\d+ — ` 18 to 19 gaining exactly the key `R18`, all 19 DISTINCT. The §3 item 10 open set is 238 at `1e9d3a83`, down from 239 at the base, and R19 MINTED NO ID. THE RESOLUTION'S OWN EVIDENCE WAS SPOT-CHECKED rather than taken on trust, which is the reading a reviewer owes a text it is making permanent: at `6ede183c`, `git grep` over `apps/ui/src` counts `DecisionInboxCard` on exactly 3 lines, all three the COMPONENT and 0 of them under `apps/ui/src/api/`, and `DecisionInboxEntry` on exactly 13 lines confined to `apps/ui/src/api/decisionCard.ts` and its test, with that commit's `git diff --numstat` reading 4 and 4 for the first and 9 and 9 for the second — every figure DONE0681 states, confirmed against the tree. HYGIENE HELD: line-anchored `^<<<SLICE ` and `^<<<END ` both 0 in `.agent/plan.md` at `3d2a3be2` and in `.agent/live_review.md` at `1e9d3a83`, against a control of 4 and 4 over the C0a blob, so the reading is not vacuous; the range `6c758fc8`..`1e9d3a83` names 4 paths, none under `packages/`, `apps/`, `tests/` or `docs/`, range-minus-change-set EMPTY and change-set-minus-range exactly `.agent/handoff.md`; per-commit insertions 383, 263, 27, 1 and 4, each single-parent and each under the 500 cap, and the `## Commits` table's `+/-` column agrees with `git diff --numstat` cell for cell (§3 item 28); `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line and `git status --porcelain` 0. THE BLOCK'S OWN OBJECT IDS RESOLVE: 24 SHA-shaped occurrences, 11 distinct, failing set EMPTY, one `blob` and ten `commit`. THE CODE R19 DID NOT TOUCH IS STILL GREEN, measured by the reviewer in the primary checkout: `npm run typecheck` exit 0 with ZERO diagnostics and `npm run test:unit` exit 0 at 21 files and 316 tests, both UNCHANGED, which is the expected reading for a range holding no `apps/` path. THE FIVE PYTHON SUITES ARE THE REVIEWER'S OWN, run SERIALLY, never two alive at once, every one a REAL exit 0 and every count identical to the base: `tests/ui_server/` 474, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16 and `test_golden_path` 42. THE PUSH DISCHARGED, which is the outcome G10 of that round routed here rather than to any file R19 wrote: measured with `git ls-remote`, the local tip and `refs/heads/feature/f031-decision-inbox` are both `ba75103eecc4c111f99ddd9c4cf6483b3c179d83`, and no pull request was created, no branch deleted and nothing merged. THE VERDICT IS PASS.
<<<END LEDGER20

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output, and
report ONE LINE PER GATE in the handback, transcripts kept out of it
(R-0582). "Green" as a word is a finding. Every gate runs at a commit
STRICTLY EARLIER than C5 (§3 item 31); G12's push runs after it and names
its own carrier.

G1  Branch and cleanliness. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`. `.agent/STOP` read from
    disk is ABSENT before C0a and again before C5. Report
    `git status --porcelain` line count after each of C0a, C0b, C1, C2,
    C3 and C4; each must be 0.

G2  Transport. Report sha256, byte count and line count for FOUR readings:
    `.remedy-wt/f031-r20.md` before C0a, the committed C0a blob, the
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

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R20 under
    your stated newline convention; report slice length, file length and
    convention. NEGATIVE CONTROL: NOT byte-equal to that slice with its
    trailing newline REMOVED. `^## Goal$` 1, `^## Next Steps$` 1, `wc -l`
    STRICTLY under 50.

G5  The DECISION append at C2, as ONE equality over the whole file, in the
    shape constraint 7 states — name that paragraph, do not restate its
    formula. Report the boolean and the byte arithmetic against the base
    length you measure yourself. Report a SECOND, INDEPENDENT reading:
    split the committed file on blank lines, take the LAST N units, and
    confirm they equal DECISIOND7's N paragraphs IN ORDER, where N is the
    number YOUR split measured; give the unit count before and after.
    Then the HEADING SERIES (§3 item 26): `^## DECISION F031 D\d+` moves
    6 to 7, gaining exactly the key `D7`, with D1 through D6 still present
    and all 7 DISTINCT.

G6  The code at C3, against the SPEC. Report, each as a reading and not as
    a word: that `apps/ui/src/api/decisionOrder.ts` exports exactly the two
    names S1 fixes and imports nothing but the model type; that
    `DecisionCardModel` carries `ageSeconds` and `buildDecisionCardModel`
    returns it (S4); that `RightLivePanel.tsx` differs from its base blob
    in the import line and the one call site and NOTHING else, which you
    show with `git diff` for that path alone (S6); and that
    `apps/ui/src/api/remedyApi.ts` is NOT in this commit's path set. Then,
    in the PRIMARY checkout at `apps/ui`: `npm run typecheck` REAL exit 0
    with ZERO diagnostics on stdout and stderr, and `npm run test:unit`
    REAL exit 0 reporting Test Files EXACTLY 22 — the base's 21 plus the
    one new file, the only file-count this round can produce — and Tests
    STRICTLY GREATER than the base's 316. REPORT THE TEST NUMBER; this
    gate deliberately predicts no total, because how many cases S8 needs
    is yours to decide. Report separately that
    `src/api/decisionCard.test.ts` still reports EXACTLY 27, the base
    reading, since S5 changes assertions inside existing tests and adds
    none.

G7  THE THREE MUTATION PROBES, each a PROBE and never a predicted colour
    (§3 item 5). Create ONE disposable worktree under `.remedy-wt/` at a
    path that does not yet exist, write every mutation ONLY inside it, and
    remove it BY THAT EXACT PATH afterwards. THE MECHANISM IS NAMED
    BECAUSE A FRESH WORKTREE HAS NO `apps/ui/node_modules` (R-0518) and
    `vitest` is therefore unresolvable there: run
      npx vitest run --root <WORKTREE>/apps/ui \
        --config <PRIMARY>/apps/ui/vitest.config.ts \
        src/api/decisionOrder.test.ts
    with the working directory set to the PRIMARY `apps/ui`, so the
    primary supplies both the installed `vitest` and the config while the
    WORKTREE supplies the mutated source. Scope the run to that ONE test
    file: the component tests cannot resolve `react/jsx-dev-runtime` from
    a worktree, and that failure would be an artefact of the route rather
    than of your mutation. THE REVIEWER VERIFIED THIS EXACT COMMAND LINE
    AT THE BASE, green on the unmutated tree and red on a deliberately
    broken one, so the route is known to be able to fail.
      Probe A — remove the `+ 1` from the urgency expression.
      Probe B — remove the open-first key from the comparator.
      Probe C — remove the `id` key from the comparator.
    For EACH probe report WHICH test node ids failed and HOW MANY, plus
    the exit code. A GREEN probe is the honest answer to declare, not to
    paper over: it means the suite does not reach that branch, and it is a
    finding against the TEST rather than against the code.

G8  The ledger append at C4, in the shape constraint 7 states — name that
    paragraph, do not restate its formula. Report the whole-file equality
    boolean and the byte arithmetic against whatever C2 and C3 left, which
    you measure rather than take from here. Report the SECOND reader as in
    G5, over LEDGER20's paragraphs. NEGATIVE CONTROL: flip ONE byte inside
    the appended text; BOTH readers must reject the mutant and BOTH accept
    the true file, and the mutant is written only under the disposable
    worktree of constraint 11.

G9  The ledger sets and the SPLIT SERIES, base versus C4 in
    `.agent/live_review.md`: `^- R-\d+ — ` 242 → 242 all DISTINCT, ids
    ADDED and REMOVED both the EMPTY SET, maximum `R-0681` → `R-0681`;
    `^Done: R-` 4 → 4, `^Landed: R-` 0 → 0 and `^Recurrence: R-` 17 → 17,
    all three UNCHANGED as constraint 9 requires. THE TWO GATE PATTERNS
    ARE COUNTED SEPARATELY because DECISION F031 D7 splits the series:
    `^Gate: R\d+ — ` 19 → 19, UNCHANGED, and `^Gate: F\d+ R\d+ — ` 0 → 1,
    the added key being exactly `F031 R19`. Report the §3 item 10 open set
    at C4 — paragraphs minus `Done:` lines — which must be 238.

G10 Markers, paths and hygiene. Line-anchored `^<<<SLICE ` and `^<<<END `
    both 0 in `.agent/plan.md` at C1, `.agent/decisions.md` at C2 and
    `.agent/live_review.md` at C4, against the same counts over the
    COMMITTED C0a blob as a CONTROL, where they are NOT 0. Report that
    `git diff --name-only <base>..C4` names NO path under `docs/`,
    `packages/`, `tests/` or `apps/cli/`, and neither `.agent/context.md`
    nor either inventory file; that the range path set MINUS the change
    set is EMPTY and the change set MINUS the range is exactly
    `.agent/handoff.md`, which C5 writes. Over C0a..C4 report per commit
    that it is single-parent and its INSERTION count — the `+` column
    only, per AGENTS.md DECISION F104 D1 — each under 500; those same
    numbers fill the `+/-` column of the `## Commits` table, derived from
    `git diff --numstat` and NOT from `git commit`'s own summary, and you
    report that the two agree cell for cell (§3 item 28). Report
    `git ls-files .remedy-wt` as 0 and `git ls-files` over `*.zip` as 0.
    FOR THE REFLOG state SCOPE and FIELD: over THIS ROUND'S entries only,
    by the OPERATION PREFIX before the first colon of
    `git reflog --format=%gs`, report `amend`, `rebase` and `cherry` each
    0 and how many entries you scoped to.

G11 The Python suites. With `git worktree list` reported as 1 line
    immediately BEFORE the first pytest command, run these SERIALLY in the
    PRIMARY checkout at the C4 tree, never two at once, all exit 0:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/ui_contracts/ -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state
    gates, plus `tests/ui_contracts/` which C3 EARNS by editing
    `RightLivePanel.tsx`, plus the canary. The reviewer executed all six
    at the base `ba75103e` with these exact command lines and no extra
    flag, and measured in that order 474, 52, 21, 16, 525 and 42, every
    one exit 0. Account for any difference.

G12 The block's object ids, and the push. Extract every SHA-shaped token
    from the COMMITTED C0a blob with the word-bounded pattern
    `[0-9a-f]{7,40}` — whose boundaries do NOT match the 64-char sha256
    digests this block also carries — and pass each to `git cat-file -t`.
    FAILING means the token does NOT RESOLVE, and THE FAILING SET MUST BE
    EMPTY: this block quotes no non-existent id, so it has no positive
    control. THE TYPES ARE NOT ALL `commit` AND THE GATE DOES NOT ASK THEM
    TO BE — LEDGER20 quotes the git BLOB id
    `43e2018218e06a256fe8e18a46cd7dca3ff5d57d`, resolved to type `blob`
    before emission, every other token resolving to `commit`. Report the
    token count YOUR extractor measured, the failing set, and the type per
    token. THEN, AFTER C5, run `git push origin
    feature/f031-decision-inbox`. No `--force`, no `--force-with-lease`,
    no history rewrite, no branch deletion, no pull request. THAT PUSH'S
    OUTCOME IS NOT A VALUE OF ANY FILE THIS ROUND WRITES: the reviewer
    measures the pushed tips at the next gate and records them in the R20
    entry of `.agent/live_review.md`. In `## External actions` write the
    push COMMAND and that sentence. In the item-status table the push row
    is `done`, reason "ordered after C5; outcome carried by G12 to the
    reviewer". Report the real outcome in your final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C5 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table per
commit, the item-status table covering C0a through C5 and the push, ONE
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

Your `## Next` section names, in order: that the R20 verdict is UNRECORDED
and is owed by the next round's ledger commit (DECISION F085 D9); that
R21 is T002b FILTERING by TYPE under DECISION F031 D6, which needs no
further ruling; and that every ledger entry from here is headed under
DECISION F031 D7's feature-qualified key.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────
