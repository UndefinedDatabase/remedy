── STEP R11 — F031 Decision inbox ────────────────────────────
Goal:        Record the R9 AND R10 verdicts in one ledger commit, then
             RULE the two gaps R9 measured — no visual authority for a
             decision card, no toolchain that can test one — as
             DECISIONs with alternatives and a reversal path, and route
             both into the feature file. No production code.

Fortschritt: ~30 % (F031 claimed; R1 through R8 landed and gated ·
             R9 and R10 landed, their verdicts recorded by THIS
             round · T001 SHIPPED — the derivation module, the read
             endpoint and 29 tests are on disk and green · T002
             unblocked by D4 and D5 · T003 offen) — Schaetzung

Bundle:      C0a save this block · C0b mirror it into last_block · C1
             the plan · C2 the R9 and R10 gate entries · C3 the two
             DECISIONs · C4 the feature-file amendment · C5 handback.

Change set:  exactly these paths, nothing else —
             .agent/authored/f031-r11.md                       (C0a)
             .agent/last_block.md                              (C0b)
             .agent/plan.md                                    (C1)
             .agent/live_review.md                             (C2)
             .agent/decisions.md                               (C3)
             docs/roadmap/features/T5_F031.md                  (C4)
             .agent/handoff.md                                 (C5)
             This list bounds the round's WRITES, not its ACTIONS:
             the push named in G11 is ordered explicitly and is not a
             file (R-0674).

── Base ──────────────────────────────────────────────────────
The round base is `99d77d5cdf2b1ebee5cb25fd18e5258a0d20c131`, the
R10 handback commit and the tip of `feature/f031-decision-inbox`,
local and remote equal. You are on `main`: check that branch out,
create none, never commit to `main`. Every SHA-shaped token here was
passed to `git cat-file -t` before emission and every one resolves,
so G10 orders that sweep with an EMPTY failure set and no positive
control.

Readings the reviewer MEASURED at that base, re-checkable there:
- `.agent/live_review.md`: 570870 bytes, 1197 lines; `^- R-\d+ — `
  240 all DISTINCT, maximum `R-0679`; `^Done: R-\d+ — ` 2, so the §3
  item 10 open set — the first pattern's paragraphs minus the
  second's lines — is 238; `^Recurrence: R-` 15; `^Gate: R\d+ — ` 9,
  the keys `R19` and `R1` through `R8`.
- `.agent/decisions.md`: 560571 bytes, 7441 lines, `^## DECISION `
  129, the highest F031 key being D3.
- `docs/roadmap/features/T5_F031.md`: 6705 bytes, 122 lines, its
  last `^## ` heading `Design amendments (F031 R5, 2026-08-23)`.
- `.agent/plan.md` 49 lines, 2964 bytes; `.agent/handoff.md` 71 lines.

── Why this round exists ─────────────────────────────────────
R10 was ORDERED as this same bundle and never executed it: it read
`.agent/STOP` before its first commit, found the sentinel present, and
stopped with a handback as its only commit. It is now ABSENT.

THE ROUND IS RENUMBERED R10 → R11 AND THAT IS DELIBERATE. R10's
handback asks for R10 to be re-run unchanged, but R10 landed a
commit and therefore earns its own `Gate: R10` ledger entry; a
second round under that number would put two paragraphs under one
key, the §3 item 26 defect R-0587 registers. The number moves, the
bundle does not.

C2 therefore carries TWO entries. Finding R-0659's standing clause
binds the reviewer here: when a round halts before its ledger
commit, the next block's ledger commit inherits BOTH the halted
round's own verdict AND whatever that round's C2 was carrying for
the round before it. R10's C2 was carrying R9. The reviewer read the
`Gate: R` key sequence for gaps before authoring: the keys present
are `R19` and `R1` through `R8`, so R9 and R10 are the two owed.

C3 and C4 are the substance. T002 has been blocked on two gaps that
are MEASURED rather than suspected. D4 rules where the card's visual
authority comes from; D5 rules how it is tested, and in doing so
corrects a sentence of the feature file that no round could have
executed as written. §4.7 requires a wrong spec routed as an
amendment rather than silently re-planned, so C4 writes both rulings
into the feature file itself.

── Constraints ───────────────────────────────────────────────
1. Apply every authored slice BYTE FOR BYTE. Never retype, rewrap,
   reflow or "fix" one. If a slice looks wrong, apply it verbatim
   and DECLARE the disagreement in the handback: a contradiction
   inside this block is the reviewer's defect, not yours.
2. Slice transport. This block is saved verbatim as
   `.agent/authored/f031-r11.md` at C0a and mirrored byte-identically
   into `.agent/last_block.md` at C0b. Extract every slice
   PROGRAMMATICALLY out of the COMMITTED C0a blob by its marker
   LINES — `<<<SLICE <NAME>` opens, `<<<END <NAME>` closes. Marker
   lines never reach a target file.
3. Commit sequence, exactly: C0a, C0b, C1, C2, C3, C4, C5. No extra
   commit, none dropped, no reordering. C1 is the FIRST substantive
   commit because this round touches the finding ledger (§3 item
   23). The push runs after C5. To correct a landed commit, do NOT
   add one outside this sequence — declare it, and give any such
   commit its own `## Commits` row and its own item-status row
   (R-0675).
4. Never amend, rebase, cherry-pick, force-push or rewrite history;
   never delete a branch; never merge; create no pull request.
5. `git status --porcelain` prints 0 lines after every commit. Read
   `.agent/STOP` from disk before C0a and again before C5; if present,
   finish the commit in hand, write the handback and stop. NEVER
   delete that sentinel (R-0347).
6. The slices this block carries are the whole text PLANF031R11 and
   the three appended texts GATES910, DECIS45 and FEATAMEND. This
   paragraph names them and states no count; G3 orders you to report
   the count YOUR extractor measured.
7. THREE SLICES ARE APPENDS AND THE SHAPE IS STATED ONCE, HERE, WITH
   EVERY GATE NAMING THIS PARAGRAPH RATHER THAN RESTATING IT. Under
   the newline-INCLUDED convention each slice already ends in a
   newline, so each target is EXACTLY: its base blob, then one
   newline, then the slice. GATES910 goes to `.agent/live_review.md`
   at C2, DECIS45 to `.agent/decisions.md` at C3, FEATAMEND to
   `docs/roadmap/features/T5_F031.md` at C4. Nothing follows in any of
   the three, each file ends in exactly one newline because its slice
   carries it, and each target receives NOTHING ELSE in its commit
   (R-0657). THIS BLOCK CARRIES NO FROM/TO PAIR, so no containment
   reading is owed and none is stated.
8. THIS ROUND MINTS NO FINDING ID and writes no `Recurrence:` line.
   `^- R-\d+ — ` must be 240 before and 240 after, the maximum must
   stay `R-0679`, and `^Recurrence: R-` must be 15 before and 15
   after. Neither R9 nor R10 earned a finding: every gate reproduced
   under the reviewer's own execution.
9. Touch nothing under `packages/`, `apps/` or `tests/`, and within
   `docs/` touch ONLY `docs/roadmap/features/T5_F031.md`. Do not
   touch `.agent/f031_inventory.md` or `.agent/f031_ui_inventory.md`
   — landed evidence is corrected by dating in a later round, never
   by editing (§3 item 20). Because this round DOES touch
   `docs/roadmap/**`, the docs-round gate of §3 applies and G10 runs
   it.
10. `docs/roadmap/ROADMAP.md` and `docs/roadmap/STATUS.md` are NOT
    touched: AGENTS.md forbids editing ROADMAP.md without an explicit
    operator request, and this round claims and closes nothing.
11. Destructive verification, if any, runs ONLY in a disposable
    `git worktree` under `.remedy-wt/`, removed BY ITS EXACT PATH
    (R-0662) and before the G10 suites. Everything already under
    `.remedy-wt/` is PRE-EXISTING scratch belonging to no commit,
    this block's own file included: do not create a worktree at any
    existing path there, and delete nothing you did not create.

── Authored slices ───────────────────────────────────────────

<<<SLICE PLANF031R11
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
R11 records the R9 and R10 verdicts in one ledger commit and rules the two
measured gaps as DECISION F031 D4 and D5, routing both into the feature file.
R10 was this same bundle and stopped on the now-absent `.agent/STOP` sentinel.
T001 is SHIPPED: the module, the route and 29 tests are green.

## Next Steps
1. T002a builds the inbox card and the GENERIC options renderer as PURE model
   functions under `apps/ui/src/api/` with `.test.ts` beside them, per D5, and
   the card shell D4 fixes; the extensibility test covers a novel options
   payload at the model layer.
2. T002b adds ordering over age and blocked size, filtering, and the badge,
   where DECISION F031 D2 binds: the badge re-derives on refetch over the
   existing SSE stream, no new event kind ships, and the two constant-zero
   counters D2 names get replaced.
3. T003 wires answering through the write channel, and rules there whether
   `NeedsAttentionCard`'s decision branch is retired, which D4 leaves open.

## Risks
- Open findings, stated with the rule and the commit DECISION F009 D10 requires:
  by §3 item 10 — every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — `
  line — the open set is 238, measured at `99d77d5c`.
- The findings THIS FEATURE MUST STILL ACT ON — a narrower set, named as what it
  is and not called "open" — are R-0403, R-0413, R-0431, R-0445, R-0471, R-0495,
  R-0533, R-0574, R-0601, R-0625, R-0632, R-0672, R-0674, R-0675, R-0676, R-0677,
  R-0678 and R-0679; R-0495 and R-0574 are the two Highs, from F085 and F086.
- D5 leaves the card's rendered markup reached by NO test, deliberately and
  scheduled rather than discovered. Every branch lives in the pure model; if a
  branch ever migrates into the component, it leaves the tested region.
- The record holds `Gate: R19` from F022 as its seed entry. If F031 reaches its
  own R19 that key collides — the §3 item 26 defect. A round before then renames
  the seed or the scheme; this bullet is the reminder.
<<<END PLANF031R11

<<<SLICE GATES910
Gate: R9 — the F031 R9 entry. R9 PASSED ON EVERY ONE OF ITS TEN GATES. This entry is written at R11 rather than at R10, because R10 was ordered to write it and stopped on the `.agent/STOP` sentinel before its ledger commit; finding R-0659's standing clause makes the next block's ledger commit inherit it, and the reviewer read the `Gate: R` key sequence for gaps before authoring and found exactly R9 and R10 owed. THE TEXT BELOW IS THE R10 REVIEWER'S, CARRIED FORWARD, AND THE R11 REVIEWER RE-MEASURED A NAMED SAMPLE OF ITS CLAIMS AT THE SHAs THEY NAME BEFORE REPRODUCING IT — the R9 block on disk is sha256 `173981e6f4409b1629f7c4db3880fbbbb7f3bda58b482c0be8300f6adeae4a8e` over 26436 bytes and 375 lines; `.agent/plan.md` at `8d31351c` is 2964 bytes over 49 lines with `^## Goal$` and `^## Next Steps$` once each; `.agent/live_review.md` at `95610316` is 566277 bytes becoming 570870 with the delta 4593 and the base blob plus one newline a byte-exact PREFIX of it; the `^Gate: R\d+ — ` keys went 8 to 9 gaining exactly `R8`; `.agent/f031_ui_inventory.md` at `000b1b63` is 263 lines carrying `## Q1` through `## Q7` in order plus `## Observations`; and the five commits of that round insert 375, 202, 13, 2 and 263, each single-parent — every one of those readings reproduced EXACTLY. The claims NOT re-measured are reproduced as what they are, the R10 reviewer's readings dated to the SHAs they name, and are not re-certified here. AS AUTHORED AT R10: R9 PASSED ON EVERY ONE OF ITS TEN GATES, AND THE REVIEWER RE-RAN EVERY EXECUTABLE ONE ITSELF rather than reading the handback's word for any of them; every value that handback states reproduced exactly. THE ROUND'S SUBSTANCE IS A MEASUREMENT, so the reviewer did not stop at the gates: EVERY CLAIM OF `.agent/f031_ui_inventory.md` WAS RE-MEASURED AGAINST THE SOURCE, because a gate proves a file's shape and never its truth. All of it held — 58 `--remedy-*` properties DEFINED under `apps/ui/src/styles/`, all in `tokens.css` with `globals.css` defining none; `NeedsAttentionCard.tsx` 50 lines, root `<section>`, `data-ui="needs-attention-card"`, five classes off `RightLivePanel.module.css`, which six OTHER components also import; the right panel composed by `RightLivePanel` in the order `LiveStatusPill`, `AgentNowCard`, `NeedsAttentionCard`, `ActivityFeedCard`, `TaskChecklistCard` inside `<aside data-ui="right-live-panel">`; the string `Needs your decision` 6 times over 4 files while `apps/ui/src/api/` holds exactly one `decisions` line, a prose comment in `budgetTick.ts`; and one `inbox` string folder-wide in the design reference, `ux_spec.md:163`, out of scope. THE TOOLCHAIN READING IS THE ONE THAT CHANGES THE PLAN: `apps/ui/vitest.config.ts` sets the environment to `node` with the single include `src/**/*.test.ts`, 20 files match it, 0 match `src/**/*.test.tsx`, and `apps/ui/package.json` carries 0 lines naming a DOM harness — so no component test is collected today, and the feature file's T002 phrase could not have been executed by any round. THE WORKER IMPROVED ON THE ORDER RATHER THAN MERELY MEETING IT: it reported `assets_spec.md:174`, a `decision` glyph row for a GRAPH NODE, as decision visual authority the reviewer's own Q1 reading had not named, so the next ruling could rule against it instead of around it. TRANSPORT HELD: `.remedy-wt/f031-r9.md` before C0a, the committed C0a blob, the committed C0b blob and `.agent/last_block.md` off disk are ALL sha256 `173981e6f4409b1629f7c4db3880fbbbb7f3bda58b482c0be8300f6adeae4a8e` over 26436 bytes and 375 lines, with C0a and C0b resolving to the SAME git blob `fc7e17798b211103f5262223d864e231eaf16f8b`; the reviewer's extractor printed 2 slices, 50 CONTENT lines and 375 TOTAL lines over 4 marker lines. `.agent/plan.md` at `8d31351c` is 2964 bytes byte-equal to PLANF031R9 under the newline-INCLUDED convention with the trailing-newline-removed control FALSE, `^## Goal$` and `^## Next Steps$` once each, 49 lines strictly under 50. THE LEDGER APPEND HELD AS ONE EQUALITY OVER THE WHOLE FILE: at `95610316` it is EXACTLY the base blob plus one newline plus GATE8, 566277 bytes becoming 570870 with the delta 4593 equal to 1 plus 4592; an independent blank-line split went 284 units to 285 with the LAST equal to GATE8; and the byte flipped at offset 566400 inside the appended paragraph was REJECTED by both readers while both accepted the true file. THE SETS MOVED ONLY WHERE CONSTRAINT 8 ALLOWED: `^- R-\d+ — ` 240 to 240 all DISTINCT, ids ADDED and ids REMOVED both the EMPTY SET, maximum `R-0679` unchanged, `^Done: R-` 2 to 2, `^Recurrence: R-` 15 to 15, and `^Gate: R\d+ — ` 8 to 9 gaining exactly the key `R8`. THE INVENTORY IS NEW AND NOT AN EDIT: `git ls-tree` at the base printed NOTHING for it, and at `000b1b63` it is 263 lines carrying `## Q1` through `## Q7` in order plus `## Observations`. MARKERS WERE LINE-ANCHORED 0 in all three applied targets at their own commits; the five-path range holds nothing under `packages/`, `apps/`, `tests/` or `docs/` and neither `.agent/decisions.md` nor `.agent/f031_inventory.md`; the range path set MINUS the change set is EMPTY and the change set MINUS the range is exactly `.agent/handoff.md`; `git ls-files .remedy-wt` is 0, the zip glob is 0, `git worktree list` is one line and `git status --porcelain` is 0. THE PER-COMMIT INSERTIONS ARE 375, 202, 13, 2 and 263 for C0a through C3, each single-parent and each under the 500 cap, AND THE `## Commits` TABLE OF THE HANDBACK AGREES WITH `git diff --numstat` CELL FOR CELL, which §3 item 28 requires and which the reviewer checked column by column rather than trusting the Verification line beside it. THE HANDBACK COMMIT `21c3f15e` IS ITSELF 55 INSERTIONS AND 42 DELETIONS AND SINGLE-PARENT — the numbers §3 item 31 rules no artefact of that round could carry, recorded here because this entry is the first place that can hold them. THE REFLOG READING STATES ITS OWN SCOPE AND FIELD: over this round's six entries, read by the OPERATION PREFIX before the first colon of `git reflog --format=%gs`, every prefix is `commit`, so amend 0, rebase 0 and cherry 0. THE BLOCK'S OWN OBJECT IDS WERE SWEPT: 12 occurrences over 6 distinct word-bounded hex tokens, every one resolving under `git cat-file -t`, so the failing set is EMPTY as that block predicted. THE FIVE SUITES ARE THE REVIEWER'S OWN, run SERIALLY with never two pytest processes alive, every one REAL exit code 0 at `tests/ui_server/` 474, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16 and `test_golden_path` 42 — cell for cell the readings the block ordered. THE PUSH DISCHARGED: measured by the reviewer against `git ls-remote`, the local and remote tips of `feature/f031-decision-inbox` are both `21c3f15e9246a88bf5ee0bea1936dac720a67ecc`; no pull request exists on that branch, and nothing was merged. THE HANDBACK DERIVED ITS OWN CAP rather than quoting one, reading the tier as 100 from the six commits its constraint 3 fixes and landing at 88 lines, so no DECISION D15 overage was owed or claimed. THE TWO DECLARED ITEMS ARE BOTH SOUND: the C5 row carries `rewrite` because a commit cannot number itself, and the shell guard's rejection of three compound commands was answered with `python3` readings of the same semantics, each stated beside its answer. THE VERDICT IS PASS.

Gate: R10 — the F031 R10 entry. R10 PASSED, AND IT PASSED BY EXECUTING NOTHING. The round was ordered as a seven-commit bundle; it read `.agent/STOP` from disk before C0a as its own constraint 5, self_drive_protocol.md Phase 1 rule 1 and guardrail G6 all require, found the sentinel PRESENT — untracked, 0 bytes, mtime 2026-08-23 18:26:38, later than the R9 handback commit and therefore raised against R10 rather than left over — and stopped, writing its handback as the round's only commit. That is the ordered behaviour for that state, so the round is a PASS on its conduct and not merely an absence of harm. THE REVIEWER RE-MEASURED EVERY CLAIM THAT HANDBACK MAKES, AT `99d77d5c`, AND EVERY ONE REPRODUCED EXACTLY: the range `21c3f15e`..`99d77d5c` is ONE commit, single-parent, its parent equal to the stated base; it touches exactly ONE path, `.agent/handoff.md`, at 46 insertions and 63 deletions, so every other file in the tree is necessarily byte-identical to its base blob and the claimed hash-equality of `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`, `.agent/decisions.md` and `docs/roadmap/features/T5_F031.md` is proved by the range rather than asserted; `.agent/authored/f031-r10.md` does not exist at that commit; `.agent/live_review.md` is 570870 bytes over 1197 lines, `.agent/decisions.md` 560571 over 7441, `docs/roadmap/features/T5_F031.md` 6705 over 122 with its last `^## ` heading still `Design amendments (F031 R5, 2026-08-23)`, and `.agent/plan.md` 2964 over 49; `^- R-\d+ — ` is 240 with maximum `R-0679`, `^Done: R-\d+ — ` is 2 and the §3 item 10 open set is therefore 238; `^Gate: R\d+ — ` is 9; `^## DECISION ` is 129 and the keys `F031 D4` and `F031 D5` are ABSENT from the repository, so T002 was still blocked exactly as that handback says. THE BLOCK IT DID NOT RUN SURVIVED INTACT: `.remedy-wt/f031-r10.md` is sha256 `ecdb2ef678797738545a392ecd15e25784c29941126a4f4684303fc94172401b` over 34222 bytes and 471 lines, all three equal to the values the handback states. THE PUSH DISCHARGED: measured against `git ls-remote`, the local and remote tips of `feature/f031-decision-inbox` are both `99d77d5cdf2b1ebee5cb25fd18e5258a0d20c131`; no pull request exists on that branch and nothing was merged. THE NUMBERS §3 ITEM 31 RULES NO ARTEFACT OF R10 COULD CARRY, recorded here because this entry is the first place that can hold them: the handback commit `99d77d5c` is 46 insertions and 63 deletions and single-parent, and the file it writes is 71 lines. THE ONE CLEAN-TREE DEVIATION IS SOUND AND WAS UNAVOIDABLE: `git status --porcelain` read 1 line rather than the ordered 0, that line being the untracked sentinel itself, which finding R-0347 forbids deleting — an ordered 0 is unreachable while the sentinel stands, and the worker was right to declare the conflict rather than resolve it by deletion. THE TIER CLAIM IS SOUND ON THIS REPOSITORY'S OWN RULING: the handback reads the 100-line tier from the seven commits its constraint 3 fixes and lands at 71, and finding R-0676 settles that the tier follows the commit count the block ORDERS, because that count is what fixes how many per-commit tables are mandated. THE `Fortschritt:` BLOCK WAS CARRIED VERBATIM AS ORDERED AND THEN CORRECTED ON THE LINE BELOW, which is the right way round: it asserts "T002 unblocked by D4 and D5" and neither DECISION exists, so carrying it uncorrected into the durable record would have been the worse defect. R10 MINTED NO FINDING AND EARNS NONE: no slice was applied, no value was fabricated, every base reading it states is true at `99d77d5c`, and the two remaining deviations — leaving `.agent/plan.md` untouched rather than substituting self-written text for an authored slice, and treating "write the handback" as commit-and-push — are both the conservative reading of a rule the block did not settle. THE ROUND NUMBER MOVES TO R11 FROM HERE, because R10's handback asks for R10 to be re-run unchanged while R10 has landed a commit and earned this key, and a second round under this number would put two paragraphs under one key — the §3 item 26 defect R-0587 registers. THE VERDICT IS PASS.
<<<END GATES910

<<<SLICE DECIS45
## DECISION F031 D4 (2026-08-26) — the inbox card reuses the SHIPPED shell, because the design reference carries no inbox component to follow

CHOSEN. T002's decision card is built from the shell `apps/ui/src` already ships:
the `card` and `cardHeader` classes of
`apps/ui/src/components/panels/RightLivePanel.module.css`, a root `<section>`
carrying its own `data-ui` value, mounted inside `RightLivePanel` beside the
cards already there, and styled ONLY with the `--remedy-*` custom properties
`apps/ui/src/styles/tokens.css` defines. The `decision` glyph of `assets_spec.md`
is reused as the type mark rather than redrawn.

THE MEASUREMENT, taken at `99d77d5c` and recorded per file and symbol in
`.agent/f031_ui_inventory.md`: `component_spec.md` names no decision, inbox or
queue COMPONENT — its one occurrence of the word `decision` is prose naming a
renderer choice in `graph_tech_recommendation.md`; the only `inbox` string
anywhere in `docs/ui/design_reference/` is `ux_spec.md:163`, which places mobile
status, digest and inbox surfaces expressly OUT of scope; and the one piece of
decision visual authority that does exist, `assets_spec.md:174`, is a glyph row
for a GRAPH NODE rather than for a card. `tokens.css` defines 58 such properties
and `globals.css` defines none; two of them, `--remedy-state-open` and
`--remedy-state-blocked`, already name states a decision card shows.

WHY REUSE RATHER THAN INVENT. The feature file's CANONICAL DESIGN REFERENCE
banner forbids builders inventing a new visual language, and a component spec
minted by a builder is exactly that. The shipped shell is not an invention: six
components other than `NeedsAttentionCard` already import that same module, so
reusing it adds no visual vocabulary at all.

THE OVERLAP THIS DECISION ALSO SETTLES. `NeedsAttentionCard` already renders a
card headed "Needs your decision", a string occurring 6 times across 4 files
under `apps/ui/src`, while NOTHING under `apps/ui/src/api/` reads the T001 route
— a surface answering to the inbox's name ships today and its data path does
not. The two stay DISTINCT in T002: that card derives from
`workerStatus.lifecycle_state` and offers a clipboard copy, while the inbox
derives from the decision queue and answers through the write channel. The inbox
card is therefore titled distinctly, and whether the older card's decision branch
is retired is T003's question, when answering actually ships.

ALTERNATIVES CONSIDERED. Extending `docs/ui/design_reference/` with an inbox
component spec first: rejected because that folder is the operator's visual
authority and a builder writing into it is the improvisation the banner names.
Improvising a card from the reference tokens alone: rejected for the same reason,
and with less precedent behind it than the shipped shell has. Deferring T002
until the operator supplies a spec: rejected because it blocks the feature on an
asynchronous human while a conforming shell already exists.

REVERSE IT by deleting this DECISION and its bullet in the `## Design amendments`
section of `docs/roadmap/features/T5_F031.md` that names R11. Should an inbox
component later reach `component_spec.md`, the card is restyled to it; nothing
else in F031 depends on this choice, because the read endpoint and the ordering
rule are independent of the shell.

## DECISION F031 D5 (2026-08-26) — the inbox is tested at the PURE layer, because the shipped UI toolchain collects no component test

CHOSEN. F031 follows the UI test strategy the repository already has instead of
changing the toolchain. T002's logic — the generic options renderer's model, the
ordering rule over age and blocked size, and the badge count — lands as PURE
functions under `apps/ui/src/api/` with `.test.ts` files beside them, and the
extensibility test that a novel options payload renders generically is a test
over that MODEL. The `.tsx` component becomes a thin projection of the model and
carries no branching of its own.

THE MEASUREMENT, taken at `99d77d5c` and recorded under Q4 and Q5 of
`.agent/f031_ui_inventory.md`: `apps/ui/vitest.config.ts` sets the environment to
`node` and carries the single include `src/**/*.test.ts`; 20 files match that
glob and 0 match `src/**/*.test.tsx`, so a `.tsx` test would not even be
COLLECTED; and `apps/ui/package.json` carries no line naming `jsdom`,
`happy-dom` or `testing-library`, so no DOM exists to render into. Three sampled
test files import pure functions and types only. The feature file's T002 asks for
"component tests", and no round could have executed that phrase as written.

ALTERNATIVES CONSIDERED. Adding a DOM harness and widening the include to
`.test.tsx`: rejected FOR THIS FEATURE, not on merit — it changes
`apps/ui/package.json`, `vitest.config.ts` and the lockfile, it needs an install
that a round's own gates cannot perform in a fresh worktree, where
`apps/ui/node_modules` is absent, and F031's scope does not authorize a toolchain
migration. It is worth doing as its own feature, and this DECISION is the record
that it is owed. Testing the cards only through the Python side: rejected because
that reaches the endpoint, which T001 already covers, and never reaches the
renderer's genericity, which the feature file calls the architecture line.
Shipping the cards untested: rejected outright.

WHAT THIS DELIBERATELY LEAVES UNTESTED, stated because DECISION F009 D16 forbids
leaving a mechanism no test can reach without saying so. The card's rendered
markup is reached by NO test under this decision. The gap is explicit and
scheduled rather than discovered, and it is bounded by the same sentence that
creates it: every branch lives in the pure model, so a branch migrating into the
component is the event that makes this gap matter, and reviewers gate on it.

REVERSE IT by deleting this DECISION and its bullet in the `## Design amendments`
section of `docs/roadmap/features/T5_F031.md` that names R11. Should a later
feature add a DOM harness to `apps/ui`, the component gains render tests without
touching the pure layer or any test this decision orders.
<<<END DECIS45

<<<SLICE FEATAMEND
## Design amendments (F031 R11, 2026-08-26)

> These rulings SUPERSEDE the sentences they name above, on the same terms as
> the R5 section: the originals stay so this file records what was planned and
> then what was ruled. Rationale, alternatives and reversal paths are in
> `.agent/decisions.md` under DECISION F031 D4 and D5.

- **D4 — the card reuses the shipped shell.** "Design (suggested shape)" says
  "Cards per the design reference". Measured at `99d77d5c`, that reference
  carries no decision, inbox or queue COMPONENT: `component_spec.md` names none,
  the folder's only `inbox` string puts mobile inbox surfaces out of scope, and
  the one decision visual it does carry is a graph-node glyph. The card is
  therefore built from the shipped `RightLivePanel.module.css` shell and the
  `--remedy-*` properties `apps/ui/src/styles/tokens.css` defines, mounted in
  `RightLivePanel`. `NeedsAttentionCard`, which already renders a card headed
  "Needs your decision" from `workerStatus`, stays DISTINCT from the inbox in
  T002; T003 rules whether its decision branch is retired.

- **D5 — the inbox is tested at the pure layer.** "Task slicing" gives T002
  "component tests". Measured at `99d77d5c`, `apps/ui/vitest.config.ts` sets the
  environment to `node` and includes only `src/**/*.test.ts`, 0 files match
  `src/**/*.test.tsx`, and `apps/ui/package.json` names no DOM harness — so no
  component test is collected and that phrase could not be executed as written.
  T002's renderer model, ordering rule and badge count ship as pure functions
  under `apps/ui/src/api/` with `.test.ts` beside them, and the extensibility
  test runs against the model. The rendered markup is deliberately reached by no
  test until a DOM harness lands as its own feature.
<<<END FEATAMEND

── Done when ─────────────────────────────────────────────────
Run every gate yourself, record its REAL exit code and REAL output,
and report ONE LINE PER GATE in the handback, transcripts kept out of
it (R-0582). "Green" as a word is a finding. Every gate below runs at
a commit STRICTLY EARLIER than C5 (§3 item 31); G11 runs after it and
names its own carrier.

G1  Branch and cleanliness. `git branch --show-current` prints
    `feature/f031-decision-inbox` and NOT `main`. `.agent/STOP` read
    from disk is ABSENT before C0a and again before C5. Report
    `git status --porcelain` line count after each of C0a, C0b, C1,
    C2, C3 and C4; each must be 0.

G2  Transport. Report sha256, byte count and line count for FOUR
    readings: `.remedy-wt/f031-r11.md` before C0a, the committed C0a
    blob, the committed C0b blob, and `.agent/last_block.md` off
    disk after C0b. All four must be EQUAL. Report the git blob id
    of C0a's and C0b's file; they must be the SAME id.

G3  Extraction. Run your extractor over the COMMITTED C0a blob and
    report the slice count, the CONTENT lines inside markers, and
    the TOTAL line count. Report the numbers YOUR extractor printed.

G4  The plan. `.agent/plan.md` at C1 is byte-equal to PLANF031R11
    under your stated newline convention; report slice length, file
    length and convention. NEGATIVE CONTROL: NOT byte-equal to that
    slice with its trailing newline REMOVED. `^## Goal$` 1,
    `^## Next Steps$` 1, `wc -l` STRICTLY under 50.

G5  The three appends, EACH as ONE equality over its whole file, in
    the shape constraint 7 states — name that paragraph, do not
    restate its formula. Report per target the boolean and the byte
    arithmetic, against the base's 570870 for the ledger, 560571 for
    the decisions and 6705 for the feature file. Report for EACH a
    SECOND, INDEPENDENT reading, one property stated once and applied
    to all three: split the committed file on blank lines, take the
    LAST N units, and confirm they equal that target's slice's N
    paragraphs IN ORDER, where N is the number YOUR split measured and
    not one stated here (R-0631). Give the unit count before and after
    for each. NEGATIVE CONTROL per target: flip ONE byte inside the
    FIRST paragraph that append added (R-0631); BOTH readers must
    reject the mutant and BOTH accept the true file. Write any mutant
    only under a disposable worktree per constraint 11.

G6  The sets, base versus C2 in `.agent/live_review.md`:
    `^- R-\d+ — ` 240 → 240 all DISTINCT, ids ADDED and ids REMOVED
    both the EMPTY SET, maximum `R-0679` → `R-0679`, `^Done: R-`
    2 → 2, `^Recurrence: R-` 15 → 15 UNCHANGED. `^Gate: R\d+ — `
    9 → 11, gaining exactly the keys `R9` and `R10`, with `R19` and
    `R1` through `R8` still present. Report also that the two added
    keys are DISTINCT from each other and from every key already
    there (§3 item 26).

G7  The two new DECISIONs. In `.agent/decisions.md` at C3, report
    `^## DECISION ` 129 → 131, the ids ADDED being exactly
    `F031 D4` and `F031 D5`, and that `^## DECISION F031 D4` and
    `^## DECISION F031 D5` each occur exactly once. Report that no
    line of the base blob changed: the base is a byte-exact PREFIX
    of the committed file, which is the same reading G5 takes and is
    reported once there.

G8  The feature file. In `docs/roadmap/features/T5_F031.md` at C4,
    report `^## ` heading count before and after, that the LAST
    heading is now the R11 amendments heading FEATAMEND opens with,
    and that the R5 amendments heading is still present exactly
    once. Report that line 1 and line 2 of the file are BYTE-
    IDENTICAL to line 1 and line 2 at the base — the title and
    dependency lines `tests/orchestration/test_roadmap_index.py`
    parses. The reviewer confirmed by red control at the base that
    breaking line 2 turns that suite red at 11 failed, while appending
    this very section leaves it green at 30 passed.

G9  Markers, paths, structure and hygiene. Line-anchored `^<<<SLICE `
    and `^<<<END ` both count 0 in `.agent/plan.md` at C1,
    `.agent/live_review.md` at C2, `.agent/decisions.md` at C3 and
    `docs/roadmap/features/T5_F031.md` at C4. Report that
    `git diff --name-only <base>..C4` names NO path under `packages/`,
    `apps/` or `tests/`, exactly ONE under `docs/`, and NEITHER
    `.agent/f031_inventory.md` NOR `.agent/f031_ui_inventory.md` NOR
    `docs/roadmap/ROADMAP.md` NOR `docs/roadmap/STATUS.md`. Over
    C0a..C4 report per commit that it
    is single-parent and its INSERTION count — the `+` column only,
    per AGENTS.md DECISION F104 D1 — each under 500. Those same
    per-commit numbers fill the `+/-` column of the `## Commits`
    table the handback template mandates: derive that column from
    `git diff --numstat` and NOT from the files' before/after line
    counts, and report that the table and this gate agree cell for
    cell (§3 item 28). Report the range path set MINUS the change
    set (EMPTY) and the change set MINUS the range (exactly
    `.agent/handoff.md`, which C5 writes). Report
    `git ls-files .remedy-wt` as 0, `git ls-files` over `*.zip` as
    0, and `git worktree list` as 1 line. FOR THE REFLOG, state the
    SCOPE and the FIELD in the reading itself: over THIS ROUND'S
    entries only, read by the OPERATION PREFIX before the first
    colon of `git reflog --format=%gs`, report `amend`, `rebase` and
    `cherry` each 0, and how many entries you scoped to.

G10 The block's own object ids, and the suites. Extract every
    SHA-shaped token from the COMMITTED C0a blob with the word-bounded
    pattern `[0-9a-f]{7,40}` — whose boundaries do NOT match the
    64-char sha256 digests this block also carries — and pass each to
    `git cat-file -t`. THE FAILING SET MUST BE EMPTY: this block quotes
    no non-existent id, so it has no positive control. Report the token
    count YOUR extractor measured, the failing set, and the type per
    token. Then, with `git worktree list` reported as 1 line
    immediately BEFORE the first pytest command, run these SERIALLY in
    the PRIMARY checkout at the C4 tree, never two at once, all exit 0:
      python3 -m pytest tests/docs/ -q
      python3 -m pytest tests/orchestration/test_roadmap_index.py -q
      python3 -m pytest tests/ui_server/ -q
      python3 -m pytest tests/orchestration/test_test_runner.py -q
      python3 -m pytest tests/regression/test_resource_safety.py -q
      python3 -m pytest tests/orchestration/test_integrity_gate.py -q
      python3 -m pytest tests/cli/test_golden_path.py -q
    The first two are the §3 docs-round gate this round earns by
    touching `docs/roadmap/**`. The reviewer executed all seven of
    these at the base `99d77d5c`, in a disposable worktree it then
    removed, with these exact command lines and no extra flag, and
    measured in that order 295, 30, 474, 52, 21, 16 and 42, every
    one exit 0. Account for any difference.

G11 The push. AFTER C5, run
    `git push origin feature/f031-decision-inbox`. No `--force`, no
    `--force-with-lease`, no history rewrite, no branch deletion, no
    pull request. THIS GATE'S OUTCOME IS NOT A VALUE OF ANY FILE
    THIS ROUND WRITES, and its carrier is named here so you inherit
    ONE instruction rather than two: the reviewer measures the
    pushed tips at the next gate and records them in the R11 entry
    of `.agent/live_review.md`. In `## External actions` write the
    push COMMAND and that sentence — which is how this block
    satisfies `docs/agents/handback_template.md` and R-0679's fix
    clause together. Report the real outcome in your final message.

── Handback ──────────────────────────────────────────────────
Rewrite `.agent/handoff.md` at C5 per docs/agents/handback_template.md:
feature and round, branch, base and commit SHAs, a changed-files table
per commit, the item-status table covering C0a, C0b, C1, C2, C3, C4,
C5 and the push, ONE LINE PER GATE with its real result, the finding
counts, and the next expected action. Carry the `Fortschritt:` block
above VERBATIM — count its lines yourself; this block states no
numeral for them.

THE HANDBACK LINE CAP: this block states no cap and no tier. Resolve
it from AGENTS.md under `### handoff.md` against the commit count
constraint 3 fixes, and report BOTH that count and the tier. If the
MANDATED content genuinely does not fit, exceed it and carry a
DECISION D15 "Deviations, declared" line naming your measured count
as a NUMERAL (R-0430) and the mandated content behind it. Never drop
a section to fit, and claim no token cap: that cap was withdrawn.

Any finding count you state carries the RULE that produced it and the
COMMIT it was measured at, in the same sentence, per DECISION F009
D10. A narrower set is named "the findings this feature must still act
on" and is never called "open" unqualified.

Your `## Next` section names, in order: Phase 1 rule 1 (re-read
`.agent/STOP` from disk); that NO pull request exists for this branch
and none should be created yet; that T002a is now UNBLOCKED and builds
the card and the generic options renderer as pure model functions
under `apps/ui/src/api/` with `.test.ts` beside them, per DECISION
F031 D4 and D5; and that T002a's first commit also records the R11
verdict, which by DECISION F085 D9 no artefact of this round can
carry.

Declare every deviation, contradiction and assumption.
──────────────────────────────────────────────────────────────
