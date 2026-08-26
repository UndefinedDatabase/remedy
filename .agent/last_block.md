── STEP R12 — F031 Decision inbox, T002a ─────────────────────
Goal:        Record the R11 verdict, then SHIP the decision-card
             PURE MODEL under `apps/ui/src/api/` with its `.test.ts`
             beside it — the generic options renderer that producers
             own and the inbox never hardcodes, per DECISION F031 D5.

Fortschritt: ~40 % (F031 claimed; R1 through R10 landed and gated ·
             T001 SHIPPED · T002a ships the card MODEL and its tests
             here · T002b ordering, filtering and the badge offen ·
             T003 offen) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1
             the plan · C2 the R11 gate entry · C3 the card model and
             its tests · C4 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r12.md                       (C0a)
             .agent/last_block.md                              (C0b)
             .agent/plan.md                                    (C1)
             .agent/live_review.md                             (C2)
             apps/ui/src/api/decisionCard.ts                   (C3)
             apps/ui/src/api/decisionCard.test.ts              (C3)
             .agent/handoff.md                                 (C4)
             This list bounds the round's WRITES, not its ACTIONS:
             the push named in G12 is ordered explicitly and is not a
             file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `8b4e229534c64111a1bb9391b65182631c8d57de`, the R11
handback commit and the tip of `feature/f031-decision-inbox`, local
and remote equal. Stay on that branch; create none, never commit to
`main`. Every SHA-shaped token here was passed to `git cat-file -t`
before emission and every one resolves, so G11 orders that sweep with
an EMPTY failure set and no positive control.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md`: 582367 bytes, 1201 lines; `^- R-\d+ — `
  240 all DISTINCT, maximum `R-0679`; `^Done: R-\d+ — ` 2, so the §3
  item 10 open set — the first pattern's paragraphs minus the
  second's lines — is 238; `^Recurrence: R-` 15; `^Gate: R\d+ — ` 11,
  the keys `R19` and `R1` through `R10`.
- `.agent/plan.md` 49 lines, 2894 bytes. `.agent/handoff.md` 93 lines.
- `apps/ui/src/api/` holds NO file named `decisionCard.ts` or
  `decisionCard.test.ts`: `git ls-tree` at the base prints nothing for
  either, so C3 CREATES both and edits neither.
- `npm run test:unit` in `apps/ui`: exit 0, 20 test files, 285 tests.
- `npm run typecheck` in `apps/ui`: exit 0.
- The five Python suites G11 orders, in its order: 474, 52, 21, 16, 42.

── Why this round exists ─────────────────────────────────────
R11 recorded the R9 and R10 verdicts and ruled DECISION F031 D4 and
D5. Its own verdict is owed by THIS round's ledger commit, which by
DECISION F085 D9 no artefact of R11 could carry.

D5 rules that F031's logic ships as PURE functions with `.test.ts`
beside them, because the shipped toolchain collects no component test.
C3 is that layer for the card: the model a `.tsx` will later project
without branching of its own. The feature file calls the GENERIC
options renderer the architecture line — producers own the semantics,
the inbox hardcodes no per-type form — so the model derives every
affordance from the decision's OWN payload, and the extensibility test
proves it on a type this repository has never produced.

NO LINT GATE IS ORDERED, deliberately. Measured at the base:
`npm run lint` exits 1 with 80 problems, and `npx eslint` on the
untouched pair `src/api/recency.ts` and `src/api/recency.test.ts`
fails with `Parsing error: Unexpected token type` — the configuration
parses no TypeScript, so a lint gate would be red before you start and
blind to what you write. Already REGISTERED as R-0622, still open;
this round adds evidence and mints no second id (§3 item 30).

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap or
   "fix" one. If a slice looks wrong, apply it verbatim and DECLARE
   the disagreement in the handback: a contradiction inside this block
   is the reviewer's defect, not yours.
2. THE TWO FILES OF C3 ARE NOT SLICES AND ARE NOT AUTHORED HERE. This
   block gives a numbered SPEC and you write the TypeScript yourself,
   in this repository's idiom, because reviewer-authored production
   code is code no independent reader ever reviewed. Match
   `apps/ui/src/api/recency.ts` and its test for shape: a WHY comment
   block at the top naming what the module is for and what it
   deliberately does NOT do, two-space indent, double quotes,
   semicolons, named exports, and a test opening
   `import { describe, it, expect } from "vitest";`.
3. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r12.md` at C0a and mirrored byte-identically
   into `.agent/last_block.md` at C0b. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker LINES
   — `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes. Marker lines
   never reach a target file.
4. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4. No extra
   commit, none dropped, no reordering. C1 is the FIRST substantive
   commit because this round touches the finding ledger (§3 item 23).
   The push runs after C4. To correct a landed commit, do NOT add one
   outside this sequence — declare it, and give any such commit its
   own `## Commits` row and its own item-status row (R-0675).
5. Never amend, rebase, cherry-pick, force-push or rewrite history;
   never delete a branch; never merge; create no pull request.
6. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C4; if present,
   finish the commit in hand, write the handback and stop. NEVER
   delete that sentinel (R-0347).
7. The slices this block carries are the whole text PLANF031R12 and
   the appended text GATE11. This paragraph names them and states no
   count; G3 orders you to report the count YOUR extractor measured.
8. THE ONE APPEND'S SHAPE IS STATED ONCE, HERE, WITH EVERY GATE NAMING
   THIS PARAGRAPH RATHER THAN RESTATING IT. Under the newline-INCLUDED
   convention the slice already ends in a newline, so the target is
   EXACTLY: its base blob, then one newline, then the slice. GATE11
   goes to `.agent/live_review.md` at C2, which receives NOTHING ELSE
   in that commit (R-0657). Nothing follows it, and the file ends in
   exactly one newline because the slice carries it. THIS BLOCK
   CARRIES NO FROM/TO PAIR, so no containment reading is owed.
9. THIS ROUND MINTS NO FINDING ID and writes no `Recurrence:` line.
   `^- R-\d+ — ` must be 240 before and 240 after, the maximum must
   stay `R-0679`, and `^Recurrence: R-` must be 15 before and 15
   after. R11 earned no finding: every gate reproduced under the
   reviewer's own execution.
10. Touch nothing under `packages/`, `tests/` or `docs/`, and within
    `apps/` ONLY the two new files C3 creates. Do not edit
    `RightLivePanel.tsx`, `NeedsAttentionCard.tsx`, any `.module.css`,
    `vitest.config.ts`, `package.json` or the lockfile: the `.tsx`
    projection and its mounting are T002a's SECOND round, and this one
    ships the tested layer alone.
11. Destructive verification runs ONLY in a disposable `git worktree`
    under `.remedy-wt/`, removed BY ITS EXACT PATH (R-0662) and before
    the G11 suites. Everything already under `.remedy-wt/` is
    pre-existing scratch belonging to no commit, this block's own file
    included: create no worktree at an existing path there, and delete
    nothing you did not create.

── C3 SPEC — apps/ui/src/api/decisionCard.ts ─────────────────
The module is PURE: it reads no clock, performs no I/O, imports
nothing from React and holds no state. Every function is a named
export, and any moment it needs arrives as an argument, exactly as
`recency.ts` takes `nowMs`.

S1. `DecisionAnswerKind` — a string-literal union, the members being
    `option`, `command` and `free_text`, in that order.

S2. `DecisionAnswer` — an exported interface with `kind:
    DecisionAnswerKind`, `label: string` and `value: string`.

S3. `DecisionCardModel` — an exported interface with `id`, `type`,
    `status`, `severity`, `title`, `ageLabel` and `blockedLabel` as
    `string`, `blockedCount` as `number`, `isOpen` as `boolean`, and
    `answers` as `DecisionAnswer[]`.

S4. `decisionAgeLabel(ageSeconds: number | null): string`. Null gives
    `unknown age` — the endpoint returns null for an unreadable stamp
    and the card must still render. Otherwise the largest whole unit:
    under 60 gives `<n>s`, under 3600 gives `<n>m`, under 86400 gives
    `<n>h`, and from 86400 gives `<n>d`, each truncated toward zero. A
    negative input is treated as 0.

S5. `decisionBlockedLabel(blockedCount: number): string`. 0 gives
    `blocks nothing`, 1 gives `blocks 1 task`, and n above 1 gives
    `blocks <n> tasks`. The singular matters: "blocks 1 tasks" is the
    kind of detail that makes a surface look untended.

S6. `decisionAnswers(card): DecisionAnswer[]` — THE ARCHITECTURE LINE.
    It derives affordances from the decision's OWN payload and MUST
    NOT branch on `card.type` in any way; the type is data here, never
    control flow. The rule, in order:
    (a) when `card.payload.options` is an array holding at least one
        entry, every entry becomes an `option` answer whose `label`
        and `value` are that entry rendered as a string;
    (b) otherwise, when `card.next_actions` is an array holding at
        least one entry, every entry becomes a `command` answer whose
        `label` and `value` are that entry as a string;
    (c) otherwise exactly one `free_text` answer, `label` being
        `Answer` and `value` being the empty string.
    A missing, null or non-array `payload`, `options` or `next_actions`
    falls through rather than throwing, and a non-string option is
    rendered by `String(entry)`: the payload comes from a producer this
    module does not control, and losing the question is worse than
    showing an odd label.

S7. `buildDecisionCardModel(card): DecisionCardModel`. Fills the
    interface from one card of the endpoint's `decisions` array:
    `title` is `safe_summary`, `isOpen` is `status === "open"`,
    `blockedCount` is `blocked_count` when it is a finite number and 0
    otherwise, `ageLabel` is S4 of `age_seconds`, `blockedLabel` is S5
    of `blockedCount`, and `answers` is S6. Every string field falls
    back to the empty string when absent, so no input makes this throw.

S8. `decisionCardModels(inbox): DecisionCardModel[]`. Maps S7 over
    `inbox.decisions`, returning the EMPTY ARRAY when `decisions` is
    absent or not an array. Order is preserved exactly as received:
    ordering is T002b's subject and this round imposes none.

S9. The input type. Declare the card and inbox shapes as exported
    interfaces with the endpoint's own key spellings — `id`, `type`,
    `status`, `severity`, `safe_summary`, `next_actions`, `payload`,
    `age_seconds`, `blocked_count` — with every field optional so a
    payload from a producer this module does not control still
    type-checks. Do NOT rename a key on the way in; DECISION F031 D1's
    reason is that the browser and the CLI describe one thing one way.

── C3 SPEC — apps/ui/src/api/decisionCard.test.ts ────────────
T1. Cover EVERY boundary S4 names: null, 0, 59, 60, 3599, 3600, 86399,
    86400, a multi-day value, and a negative value.
T2. Cover all three branches of S5, the singular included.
T3. Cover S6 (a), (b) and (c) separately, plus the fall-through when
    `options` is present but EMPTY, when `payload` is missing entirely,
    and when a non-string option is rendered.
T4. THE EXTENSIBILITY TEST, which the feature file calls the
    acceptance line. Build a card whose `type` is a string this
    repository has never produced — use `warp_core_alignment` — with
    two novel options, and assert its answers are exactly those two
    `option` answers. The test's name says what it proves: that a
    NOVEL type renders generically.
T5. A test asserting that two cards differing ONLY in `type`, with
    identical payloads, produce IDENTICAL `answers`. This is the
    property that makes S6's "must not branch on type" MEASURABLE
    rather than merely stated, and it is the test the red proof G9
    orders must break.
T6. S7 and S8: a full card mapping, a card with every optional field
    absent (which must not throw), and an inbox with no `decisions`
    key giving the empty array. Assert S8 preserves input order.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R12
# Plan — F031 Decision inbox

Branch: feature/f031-decision-inbox, cut from `main` at `6325ac2f`, the merge
commit of pull request #213 which closed F022. `.agent/live_review.md` is the
record and the finding-id ceiling; `.agent/f031_inventory.md` and
`.agent/f031_ui_inventory.md` are the measured inventories; `.agent/decisions.md`
carries DECISION F031 D1 through D5.

## Goal
Every open question in one calm place: the inbox renders decision cards — type,
age, blocked-subtree size — from the decision queue, live via the badge, with
branch-only blocking semantics intact. DONE when the inbox lists fixture
decisions of every PRODUCING type with correct blocked-size math, answering from
a card round-trips through the write channel into the same effects the CLI
produces, the badge tracks live, and ordering follows a documented rule over age
and blocked size rather than vibes.

## Current Step
R12 records the R11 verdict and ships T002a's tested layer: the decision-card
PURE MODEL at `apps/ui/src/api/decisionCard.ts` with `decisionCard.test.ts`
beside it, per DECISION F031 D5. The generic options renderer lives here and
derives every affordance from the decision's own payload, never from its type.

## Next Steps
1. T002a's second round projects that model into a `.tsx` card built from the
   shipped `RightLivePanel.module.css` shell per DECISION F031 D4 and mounts it
   in `RightLivePanel`; the component carries no branching of its own.
2. T002b adds ordering over age and blocked size, filtering, and the badge,
   where DECISION F031 D2 binds: the badge re-derives on refetch over the
   existing SSE stream, no new event kind ships, and the two constant-zero
   counters D2 names get replaced.
3. T003 wires answering through the write channel, and rules there whether
   `NeedsAttentionCard`'s decision branch is retired, which D4 leaves open.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 238, measured at `8b4e2295`.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0471, R-0495,
  R-0533, R-0574, R-0601, R-0622, R-0625, R-0632, R-0672, R-0674, R-0675,
  R-0676, R-0677, R-0678 and R-0679; R-0495 and R-0574 are the two Highs.
- R-0622 is live ground, not history: `npm run lint` exits 1 at 80 problems and
  eslint parses no TypeScript here, so no round of this feature can gate on it
  and every `.ts` file ships unlinted. `npm run typecheck` is the only static
  reader that works.
- The rendered markup stays reached by NO test until a DOM harness lands, which
  DECISION F031 D5 rules is its own feature. Every branch must therefore stay in
  the pure model; a branch that migrates into a `.tsx` leaves the tested region.
<<<END PLANF031R12

<<<SLICE GATE11
Gate: R11 — the F031 R11 entry. R11 PASSED ON EVERY ONE OF ITS ELEVEN GATES, AND THE REVIEWER RE-RAN EVERY ONE ITSELF off disk rather than reading the handback back; every value that handback states reproduced exactly, cell for cell, with no difference to account for. THE RANGE HELD: `99d77d5c`..`8b4e2295` is SEVEN commits, every one single-parent and correctly chained, the path set EQUAL to the block's seven-path change set with both differences EMPTY, and per-commit insertions from `git diff --numstat` of 490, 367, 21, 4, 93, 28 and 70 — each under the 500 cap AGENTS.md DECISION F104 D1 scopes to the `+` column, and each equal cell for cell to the `## Commits` table the handback carries, which is the §3 item 28 reading the reviewer took column by column rather than trusting the Verification line beside it. TRANSPORT HELD IN ITS STRONGEST FORM: the reviewer's own emitted `.remedy-wt/f031-r11.md`, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` off disk are ALL FOUR byte-identical at sha256 `8f7a61d3b41ed80f6f3b5c8454cd08af97bfbec501bf71bae271616519e1fe3e` over 40798 bytes and 490 lines, with C0a and C0b resolving to the SAME git blob `25af0eedce1fe354c0cab8cd3fd82856bf44a596`. EVERY SLICE APPLIED BYTE FOR BYTE, verified against slices the reviewer extracted mechanically from the committed C0a blob: `.agent/plan.md` at `e391ed80` equals PLANF031R11 exactly at 2894 bytes and 49 lines with the trailing-newline-removed control FALSE and `^## Goal$` and `^## Next Steps$` once each; and each of the three appends equals its base blob plus one newline plus its slice EXACTLY — 570870 + 1 + 11496 = 582367 for the ledger, 560571 + 1 + 6086 = 566658 for the decisions, 6705 + 1 + 1779 = 8485 for the feature file — with an independent blank-line split giving 285 to 287 units at N=2, 1339 to 1352 at N=13 and 14 to 18 at N=4, the last N units equal to that slice's N paragraphs IN ORDER in all three. The reviewer had PREDICTED all nine of those numbers from its own dry run before delegating, and the applied bytes reproduced every one. THE SETS MOVED ONLY WHERE CONSTRAINT 9 ALLOWED: `^- R-\d+ — ` 240 to 240 all DISTINCT with ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0679` unchanged, `^Done: R-` 2 to 2, `^Recurrence: R-` 15 to 15, and `^Gate: R\d+ — ` 9 to 11 gaining EXACTLY the keys `R9` and `R10`, all eleven keys DISTINCT — so the §3 item 26 collision the round was renumbered to avoid did not occur. THE DECISIONS LANDED: `^## DECISION ` 129 to 131, the ids added exactly `F031 D4` and `F031 D5`, each heading occurring once, the base a byte-exact PREFIX. THE FEATURE FILE LANDED: `^## ` 9 to 10 with the last now `## Design amendments (F031 R11, 2026-08-26)`, the R5 heading still present exactly once, and lines 1 and 2 BYTE-IDENTICAL to the base — the title and dependency lines `tests/orchestration/test_roadmap_index.py` parses, which the reviewer confirmed by RED CONTROL at the base before ordering the gate: breaking line 2 turns that suite red at 11 failed while appending this very section leaves it green at 30 passed. MARKERS WERE LINE-ANCHORED 0 in all four applied targets. THE SEVEN SUITES ARE THE REVIEWER'S OWN, run SERIALLY in the primary checkout with never two pytest processes alive, every one a REAL exit 0 at `tests/docs/` 295, `test_roadmap_index.py` 30, `tests/ui_server/` 474, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16 and `test_golden_path.py` 42 — identical to the readings the reviewer took at the base in a disposable worktree it then removed. HYGIENE HELD: `git ls-files .remedy-wt` 0, the zip glob 0, `git worktree list` 1 line, `git status --porcelain` 0, and the reflog read by OPERATION PREFIX shows amend 0, rebase 0 and cherry 0. THE PUSH DISCHARGED: measured by the reviewer against `git ls-remote`, the local and remote tips of `feature/f031-decision-inbox` are both `8b4e229534c64111a1bb9391b65182631c8d57de`; `gh pr list --state open` is EMPTY and nothing was merged. THE NUMBERS §3 ITEM 31 RULES NO ARTEFACT OF R11 COULD CARRY, recorded here because this entry is the first place that can hold them: the handback commit `8b4e2295` is 70 insertions and 48 deletions and single-parent, and the file it writes is 93 lines, inside the 100-line tier its constraint 3 earns. THE SEVEN DECLARED ITEMS WERE EACH INSPECTED AND EACH IS SOUND. Two deserve naming. FIRST, the `push` item-status row reads `deviated` while the push in fact discharged normally: the block ordered a push row in a table written BEFORE the push, so no honest status existed at C5, and the worker chose the one value that does not assert an unmeasured outcome and explained it — the R-0449 class, whose fix clause that block DID apply by naming the carrier in G11. The reviewer records the outcome here, which is where G11 sent it, and the next block ordering a handback will fix the row's value rather than leave a reader to meet `deviated` on a step that worked. SECOND, the worker computed all three of G5's negative controls IN MEMORY and wrote no mutant byte anywhere, which is strictly stronger than the disposable-worktree route constraint 11 permits, and it created and removed its own extractor scratch by exact path while touching nothing pre-existing. THE WORKER ALSO RE-OBTAINED FIVE READINGS the sandbox rejected by FORM rather than content, each through a differently shaped command with the same semantics, and said so — no measurement was skipped, softened or inferred. R11 MINTED NO FINDING AND EARNS NONE. ONE PIECE OF EVIDENCE IS ADDED TO AN EXISTING OPEN FINDING RATHER THAN MINTED AS A NEW ID, per §3 item 30: R-0622 records a lint configuration that parses none of the language it is aimed at, and the reviewer re-measured it at `8b4e2295` while establishing the next round's base — `npm run lint` exits 1 with 80 problems, and `npx eslint` over the UNTOUCHED pair `src/api/recency.ts` and `src/api/recency.test.ts` fails with `Parsing error: Unexpected token type`, so the finding is live ground rather than history and no `.ts` file this feature ships can be linted at all. THE VERDICT IS PASS.
<<<END GATE11

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output,
and report ONE LINE PER GATE in the handback, transcripts kept out of
it (R-0582). "Green" as a word is a finding. Every gate below runs at
a commit STRICTLY EARLIER than C4 (§3 item 31); G12 runs after it and
names its own carrier.

G1  Branch and cleanliness. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`. `.agent/STOP` read
    from disk is ABSENT before C0a and again before C4. Report
    `git status --porcelain` line count after each of C0a, C0b, C1, C2
    and C3; each must be 0.

G2  Transport. Report sha256, byte count and line count for FOUR
    readings: `.remedy-wt/f031-r12.md` before C0a, the committed C0a
    blob, the committed C0b blob, and `.agent/last_block.md` off disk
    after C0b. All four must be EQUAL. Report the git blob id of C0a's
    and C0b's file; they must be the SAME id.

G3  Extraction. Run your extractor over the COMMITTED C0a blob and
    report the slice count, the CONTENT lines inside markers, and the
    TOTAL line count. Report the numbers YOUR extractor printed.

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R12
    under your stated newline convention; report slice length, file
    length and convention. NEGATIVE CONTROL: NOT byte-equal to that
    slice with its trailing newline REMOVED. `^## Goal$` 1,
    `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G5  The append, as ONE equality over the whole file, in the shape
    constraint 8 states — name that paragraph, do not restate its
    formula. Report the boolean and the byte arithmetic against the
    base's 582367. Report a SECOND, INDEPENDENT reading: split the
    committed file on blank lines, take the LAST N units, and confirm
    they equal GATE11's N paragraphs IN ORDER, where N is the number
    YOUR split measured and not one stated here (R-0631). Give the
    unit count before and after. NEGATIVE CONTROL: flip ONE byte
    inside the FIRST paragraph the append added; BOTH readers must
    reject the mutant and BOTH accept the true file. Write any mutant
    only under a disposable worktree per constraint 11.

G6  The sets, base versus C2 in `.agent/live_review.md`:
    `^- R-\d+ — ` 240 → 240 all DISTINCT, ids ADDED and ids REMOVED
    both the EMPTY SET, maximum `R-0679` → `R-0679`, `^Done: R-`
    2 → 2, `^Recurrence: R-` 15 → 15 UNCHANGED. `^Gate: R\d+ — `
    11 → 12, gaining exactly the key `R11`, with `R19` and `R1`
    through `R10` still present, and all 12 keys DISTINCT.

G7  The two new files EXIST AND ARE NEW. Report that `git ls-tree` at
    the base prints NOTHING for either of the two paths C3 creates,
    and that both are present at C3 — so C3 CREATED both and edited no
    existing file. Report each file's line count and that
    `git diff --name-only <base>..C3` names EXACTLY those two paths
    under `apps/`.

G8  The model does what the SPEC says, measured rather than asserted.
    Report `npm run test:unit` in `apps/ui` with its REAL exit code,
    its test-FILE count and its test count: the base is 20 files and
    285 tests, so report both new numbers and the delta, and state how
    many cases YOUR `decisionCard.test.ts` contributes. Then report
    `npm run typecheck` in `apps/ui`, which must be exit 0 — it is
    exit 0 at the base, so any error is yours. NO LINT GATE IS
    ORDERED; do not run one and do not report one.

G9  RED PROOF, inside a disposable worktree at C3 and NEVER in the
    primary checkout. The property under proof is that
    `decisionAnswers` does not branch on the decision's type. Mutate
    the SHIPPED module there so that it DOES: make `decisionAnswers`
    return the empty array when `card.type` equals
    `warp_core_alignment`, changing nothing else. Re-run
    `npm run test:unit`. Report the REAL exit code, the number of
    FAILING tests, and the NAME of each failing test. At least the T4
    extensibility test and the T5 type-independence test must be among
    them, because both assert over exactly that branch. Then remove
    the worktree BY ITS EXACT PATH and report `git worktree list` as 1
    line. If the mutant does NOT go red, report that honestly and do
    not adjust the tests to suit it — a green mutant means the tests
    do not reach the property, a finding against this block not you.

G10 Markers, paths, structure and hygiene. Line-anchored `^<<<SLICE `
    and `^<<<END ` both count 0 in `.agent/plan.md` at C1,
    `.agent/live_review.md` at C2 and BOTH files C3 creates. Report
    that `git diff --name-only <base>..C3` names NO path under
    `packages/`, `tests/` or `docs/`, and neither `vitest.config.ts`
    nor `package.json` nor a lockfile nor any `.tsx` or `.module.css`.
    Over C0a..C3 report per commit that it is
    single-parent and its INSERTION count — the `+` column only, per
    AGENTS.md DECISION F104 D1 — each under 500. Those same numbers
    fill the `+/-` column of the `## Commits` table the handback
    template mandates: derive that column from `git diff --numstat`
    and NOT from the files' before/after line counts, and report that
    the table and this gate agree cell for cell (§3 item 28). Report
    the range path set MINUS the change set (EMPTY) and the change set
    MINUS the range (exactly `.agent/handoff.md`, which C4 writes).
    Report `git ls-files .remedy-wt` as 0 and `git ls-files` over
    `*.zip` as 0. FOR THE REFLOG, state the SCOPE and the FIELD in the
    reading itself: over THIS ROUND'S entries only, read by the
    OPERATION PREFIX before the first colon of
    `git reflog --format=%gs`, report `amend`, `rebase` and `cherry`
    each 0, and how many entries you scoped to.

G11 The block's own object ids, and the Python suites. Extract every
    SHA-shaped token from the COMMITTED C0a blob with the word-bounded
    pattern `[0-9a-f]{7,40}` — whose boundaries do NOT match the
    64-char sha256 digests this block also carries — and pass each to
    `git cat-file -t`. THE FAILING SET MUST BE EMPTY: this block
    quotes no non-existent id, so it has no positive control. Report
    the token count YOUR extractor measured, the failing set, and the
    type per token. Then, with `git worktree list` reported as 1 line
    immediately BEFORE the first pytest command, run these SERIALLY in
    the PRIMARY checkout at the C3 tree, never two at once, all
    exit 0:
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    These are the four state readers a round rewriting `.agent/` state
    gates, plus the canary. The reviewer executed all five at the base
    `8b4e2295` with these exact command lines and no extra flag, and
    measured in that order 474, 52, 21, 16 and 42, every one exit 0.
    Account for any difference. `tests/docs/` and the roadmap index are
    NOT ordered: no `docs/roadmap/**` path is in this change set, so
    the §3 docs-round gate is not earned.

G12 The push. AFTER C4, run
    `git push origin feature/f031-decision-inbox`. No `--force`, no
    `--force-with-lease`, no history rewrite, no branch deletion, no
    pull request. THIS GATE'S OUTCOME IS NOT A VALUE OF ANY FILE THIS
    ROUND WRITES, and its carrier is named here so you inherit ONE
    instruction rather than two: the reviewer measures the pushed tips
    at the next gate and records them in the R12 entry of
    `.agent/live_review.md`. In `## External actions` write the push
    COMMAND and that sentence. In the item-status table the push row's
    status is `done` with the reason "ordered after C4; outcome
    carried by G12 to the reviewer" — it is NOT `deviated`, because
    the step is performed exactly as ordered and only its OUTCOME
    lands elsewhere. Report the real outcome in your final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C4 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table
per commit, the item-status table covering C0a, C0b, C1, C2, C3, C4
and the push, ONE LINE PER GATE with its real result, the finding
counts, and the next expected action. Carry the `Fortschritt:` block
above VERBATIM — count its lines yourself; no numeral is stated here.

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve
it from AGENTS.md under `### handoff.md` against the commit count
constraint 4 fixes, and report BOTH that count and the tier. If the
MANDATED content genuinely does not fit, exceed it and carry a
DECISION D15 "Deviations, declared" line naming your measured count as
a NUMERAL (R-0430) and the mandated content behind it. Never drop a
section to fit, and claim no token cap: that cap was withdrawn.

Any finding count you state carries the RULE that produced it and the
COMMIT it was measured at, in the same sentence, per DECISION F009
D10. A narrower set is named "the findings this feature must still act
on" and is never called "open" unqualified.

Your `## Next` section names, in order: Phase 1 rule 1 (re-read
`.agent/STOP` from disk); that NO pull request exists for this branch
and none should be created yet; that the next round projects this
model into a `.tsx` card per DECISION F031 D4 and mounts it in
`RightLivePanel`; and that that round's ledger commit also records the
R12 verdict, which by DECISION F085 D9 no artefact of this round can
carry.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────
