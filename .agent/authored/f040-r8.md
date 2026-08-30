# STEP R8/F040 — T002 PART 3: THE HERO CARD'S STYLESHEET

Goal: transcribe the feature file's binding CSS into a real stylesheet and pin
that transcription with a Python conformance guard, so the card the next round
mounts has a surface that cannot drift from its authority unnoticed. Book the
round 7 verdict, register R-0755 and rule DECISION F040 D9.

Base: `709dc5d9`, the round-7 handback commit and the tip of
`feature/f040-completion-digest`. Stay on that branch. Open no pull request.

WHY THE STYLESHEET AND NOT THE CARD. This repository cannot render a component
in a test (DECISION F040 D7), so a `.tsx` landing together with its stylesheet
would arrive with the stylesheet unverifiable underneath it. Splitting on this
line is the precedent F037 set at its own R9 — stylesheet plus Python guard
first, component after — and it is the split that gives this round a real red
proof instead of a green word. The `.tsx`, its mount and the copy audit are the
next round.

THE ACCEPTANCE CLAUSES THIS ROUND ANSWERS, per the counter-measure R-0754 left
behind. `docs/roadmap/features/T5_F040.md` Design carries a binding CSS block at
:58-64 and the layout sentence at :65-67. THIS ROUND MEETS the binding CSS and
the token discipline. IT DOES NOT MEET, and must not claim: the copy audit
("since you were last here"), the CTA's behaviour, the trigger wiring, or
anything requiring markup. Say so in the handback.

WHAT IS ALREADY MEASURED, so no gate rests on a guess.
- All SEVEN `--remedy-*` tokens the binding CSS names are defined in the shipped
  `apps/ui/src/styles/tokens.css`: `--remedy-radius-lg`, `--remedy-card`,
  `--remedy-shadow-soft`, `--remedy-font-ui`, `--remedy-ink`,
  `--remedy-radius-pill` and `--remedy-blue`. None is missing.
- REDUCED MOTION needs nothing from this sheet. `ux_spec.md` §16 records that
  `prefers-reduced-motion` is "already global-killed in globals.css + Provider",
  and the binding CSS declares no animation, no transition and no transform, so
  the obligation is met by carrying none. Do not add a motion block to satisfy a
  rule that is already satisfied.
- RESPONSIVE: `ux_spec.md` §15 requires only that a region not hard-code the
  frame and that it read `--remedy-left-width` / `--remedy-right-width`. This
  card is centred with `max-width` and `margin:auto` and belongs to neither side
  region, so it hard-codes no frame. Add NO breakpoint this round; a breakpoint
  with no rendered card to measure is a guess.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f040-r8.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN8
- C2  append slice RECORD8 to `.agent/live_review.md`
- C3  create `apps/ui/src/components/digest/DigestHeroCard.module.css` per SPEC
- C4  create `tests/ui_contracts/test_digest_hero_css.py` per the SPEC below
- C5  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f040-r8.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    apps/ui/src/components/digest/DigestHeroCard.module.css
    tests/ui_contracts/test_digest_hero_css.py
    .agent/handoff.md

NO `.tsx` IS CREATED OR EDITED. `apps/ui/src/api/jobDigest.ts` and
`apps/ui/src/api/digestVisibility.ts` are NOT edited — rounds 6 and 7 built them
and their guards pin them. No Python production code changes. NOTHING under
`docs/ui/design_reference/` is edited: it is the authority this round transcribes
FROM, and a round that edits its own authority proves nothing.

## Constraints

1. Apply every slice BYTE FOR BYTE. If one looks wrong, apply it as given and
   DECLARE the problem in the handback's deviations.
2. C0a is a COPY: the block is at `.remedy-wt/f040-r8-block.md`. Use
   `shutil.copyfile` for C0a and again for C0b.
3. C1 is the FIRST substantive commit, ahead of the ledger append.
4. `.agent/live_review.md` is APPEND-ONLY.
5. `.agent/plan.md` stays under 50 lines.
6. Every exit code is REAL, from `subprocess.run(...).returncode` in a script
   under the gitignored `.remedy-wt/`. Never through a pipe.
7. Mutation and red-proof checks run ONLY in a disposable `git worktree`.
8. THE BINDING VALUES ARE TRANSCRIBED, NOT REDESIGNED. Every number, token and
   keyword in the feature file's block at :58-64 appears in the stylesheet with
   the SAME value. You may adapt SELECTOR FORM to CSS-module idiom — a module
   has no global `.digest`, so the class names are local — but you may not
   change a value, drop a declaration or add a visual one. If a value looks
   wrong, transcribe it and declare the doubt.
9. `color:#fff` IS TRANSCRIBED AS WRITTEN, per DECISION F040 D9 in RECORD8 and
   finding R-0755. Do not substitute a token: no token for it exists, the
   nearest shipped sibling writes exactly `background: var(--remedy-blue);
   color: #fff;`, and the prohibition in `tokens_rules.md` is measured as
   unenforced with 217 pre-existing violations. Deviating here would put F040
   out of step with its own feature file AND with the component beside it.
10. EVERY OTHER COLOUR IS A TOKEN. Apart from that one `#fff`, the sheet
    contains no hex and no `rgb(`/`rgba(` literal; every colour is
    `var(--remedy-…)`, and every token it names is one `tokens.css` defines.
11. The `remedy` console script is DENIED to this session; use
    `python3 -m apps.cli.main ...` if needed and say so.
12. Commit subjects carry no leading-slash token, no absolute path, no
    secret-like string, and no `Co-Authored-By` trailer.
13. Push after C5. No pull request, no merge, no force-push.
14. NO TYPESCRIPT COLOUR IS ORDERED (DECISION F040 D7). Nothing this round is
    TypeScript; the stylesheet is pinned from Python, which IS red-proved.

## SANDBOX NOTES — read before writing a script

- Env-var assignment is DENIED in all three shell forms. Set it in-process with
  `os.environ[...]` or `monkeypatch.setenv`.
- `cp` is denied; copy with `shutil.copyfile`.
- `$(...)` inside a compound, `;`/`&&` chains and process substitution are
  rejected by FORM. One command per call, or a driver script run as a single
  `bash script.sh`, or `python3 - <<'PY'`.
- A `python3 -c` script containing a newline followed by `#` is rejected; use a
  script FILE for anything with comments.
- The Bash tool does not surface non-zero exits; capture
  `subprocess.run(...).returncode`.

## Slices

The authored units are PLAN8 and RECORD8, each between its own BEGIN and END
marker line. The markers are NOT part of the unit; the newline ENDING the last
content line IS.

<<<BEGIN PLAN8
# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 2, round 8.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the spec decisions D2 to D9 | done | rounds 2-8 |
| T001 the composition, endpoint, goldens | done | rounds 3-5, all PASS |
| T002 the client digest seam and its guard | done | round 6, PASS |
| T002 the trigger, dismiss and last-seen rule | done | round 7, PASS |
| T002 the hero card stylesheet and its guard | done | this round |
| T002 the card, its mount and the copy audit | open | next |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round transcribes the feature file's binding CSS into
   `DigestHeroCard.module.css` and pins it with a conformance guard, the split
   F037 used when a component could not be render-tested.
2. The next round mounts the card: the `.tsx`, the trigger wiring onto
   `digestVisibility`, the dismissal port bound at the edge per DECISION F040
   D8, and the copy audit the Acceptance names.
3. Then T003's `remedy job digest`, the end-to-end, the integration gate and
   closure.

## Risks
- R-0570, R-0752 and R-0755 stay OPEN and are routed to the paydown branch; none
  is F040's to fix. R-0753 stays OPEN as this feature's documented risk.
- THE CARD ROUND MUST SETTLE A COPY COLLISION: `ux_spec.md` §17 forbids the UI
  showing raw UUIDs, and the digest's own `primary_action.label` embeds a job-id
  prefix and a `td:` decision id — visible in the R5 goldens. The card either
  humanises that label or the envelope stops carrying it; a DECISION, not a
  silent choice.
<<<END PLAN8

<<<BEGIN RECORD8
Gate: F040 R7 — T002 PART 2, THE TRIGGER RULE. VERDICT PASS. Reviewed by re-running every gate in the reviewer's own driver; every figure reproduced. TRANSPORT is REAL at sha256 `12384650aeeec89da2c801535aaf7038df0670ead010e2dfb22baaaff7bf3e9a` over 29484 bytes, equal on all three copies. THE PLAN is byte-equal to PLAN7 at 1882 bytes and 39 lines. THE RECORD APPEND reconstructs whole at 1687401 + 1 + 7054 = 1694456, N counted as 2, order holding, base a prefix. THE LEDGER is EXACTLY what a round that neither registers nor resolves should show: registered ADDED `[]` and REMOVED `[]`, resolved ADDED `[]`, `DECISION F040` ADDED `['D8']`, one `^Gate: F040 R6 — ` line, open count UNCHANGED at 261. THE GUARD'S APPEND IS PREFIX-SHAPED, measured against the base blob: 12094 bytes to 25035, the base bytes a literal prefix of the committed file, its own sixteen tests still green among the twenty-nine. THE RULE'S PURITY was re-measured over comment- and literal-stripped source with a SALTED POSITIVE CONTROL per token: `Date.now`, `new Date`, `localStorage`, `sessionStorage`, `fetch`, `crypto` and `XMLHttpRequest` each occur ZERO times, and each salted copy proves the scan can see that token when it is there. `jobDigest.ts` is BYTE-IDENTICAL to its base blob, so the round touched nothing it said it would not. THE SEVEN-STATE PARTITION IS PINNED AT ITS SOURCE, which is the round's best idea: the guard PARSES `RunState` out of `packages/core/models.py` rather than retyping it, so `pending`, `planned`, `running`, `paused`, `completed`, `failed` and `cancelled` are read from the enum and every one is required to appear in `digestVisibility.ts` — a state added to the enum reddens this guard until the module accounts for it. THE REVIEWER RED-PROVED THE GUARD IN ITS OWN WORKTREE WITH FIVE MUTATIONS, control first in each and each reverted before the next, all REAL exit 1: a consumed `Date.now()` killed the purity assertion alone; an implementation bound to the port killed both port assertions; the audited phrase placed in the module killed both copy assertions; deleting `"pending"` killed the seven-state assertion; and a FIFTH the block did not order — collapsing `NOT_YET_STARTED_STATES` to the empty list, which is precisely the two-way partition the block was written to forbid — also killed the seven-state assertion. That fifth is the one worth recording: the defect the round exists to prevent is caught by the gate the round shipped, proved rather than argued. Each restored run returned to 29 passed at REAL exit 0 with byte equality. THE RULE ITSELF WAS READ AND IS CORRECT: the six questions are asked in an order that makes the Acceptance clause "Dismissal persists; new activity re-arms" a single strict comparison, a not-yet-started run VETOES the card ahead of the absence route, and an unrecognised state is NOT treated as settled. VITEST AND THE TYPECHECK both PASSED rather than skipped, 4 and 1 at REAL exit 0, and the vitest file was read to confirm the partition is asserted dynamically as well — it carries a seven-row state table and two cases pinning that `pending` and `planned` do not show "not even with activity since last-seen", which is the veto. FIVE SUITES all REAL exit 0: `tests/ui_contracts/` 715 to 728, a rise of exactly the THIRTEEN tests C5 adds with the four pre-existing skips unmoved, plus 46, 515, 295 and the canary 42. Tree clean, zero untracked, eight commits at insertions 389, 293, 15, 4, 185, 268, 265 and 387, every one under 500. THE WORKER'S TEN DEVIATIONS WERE ALL CORRECTLY DECLARED, and two are the reviewer's to own rather than the worker's. Deviation 2 reports that the C5 SPEC's "add a module-level `Path` beside the existing ones" and constraint 14's byte-prefix requirement CANNOT BOTH BE MET, because placing anything beside the existing constants edits the middle of the file; the worker kept the constraint, put the new `Path` at the top of the appended region, and declared it. That is the R-0636 class — a block whose two clauses cannot both be satisfied — and it is an authoring defect, caught and correctly resolved by the worker. Deviation 4 reports that `nowMs` is taken and NO branch reads it. The block anticipated exactly that and asked for it to be declared rather than papered over, and the module's answer is honest and reasoned in its own docstring — "CLOCK SKEW IS ANSWERED BY NOT ASKING", every comparison being between two stamps the same host took — with a vitest case pinning the invariance. An unused parameter is a real smell and it is accepted here on a stated argument, not overlooked.

- R-0755 — Low, A DESIGN RULE DECLARES ITS OWN ENFORCEMENT AND THAT ENFORCEMENT DOES NOT EXIST, WHILE 217 SHIPPED DECLARATIONS BREAK THE RULE. Raised by the reviewer at the F040 R7 gate, from reading `docs/ui/design_reference/tokens_rules.md` before authoring the round that transcribes F040's binding CSS. THE RULE, at that file's `## Forbidden` section: "Raw hex/rgba in component CSS or TSX (except inside `tokens.css` and the palette bridge). Enforce via stylelint `declaration-property-value-allowed-list` (colors must be `var(--remedy-…)`) + an ESLint no-color-literal rule for the graph renderer files. CI gate lands in Stage 1." THE MEASUREMENT, taken at `709dc5d9` with that exemption applied and comments stripped: component CSS holds 68 raw hex and 102 `rgb`/`rgba` literals across 17 of its 18 files, and `.tsx` sources hold 33 hex and 14 `rgba` across 7 of 37 — 217 raw colour values in the scope the rule names. THE ENFORCEMENT IS ABSENT ENTIRELY: there is no `.stylelintrc` in any of its five spellings under `apps/ui/`, the string `stylelint` does not occur in `apps/ui/package.json` at all, and the only lint script is `eslint src --ext .ts,.tsx`, so no CI stage can be running the check the rule says lands in Stage 1. LOW, and deliberately not higher: nothing renders wrongly, no test is false, and the rule's INTENT is broadly honoured — the violations are concentrated in the graph and pipeline renderers where a canvas takes literal colours, and the ordinary card CSS is token-driven. What it costs is precision: a reviewer reading `tokens_rules.md` believes a gate is standing where none is, which is how a feature comes to think it must deviate from its own binding CSS to stay legal. That is exactly what almost happened here, and DECISION F040 D9 below records the opposite conclusion. NOT F040's TO FIX: the repair either adds a toolchain dependency and a CI stage or amends the design reference, it touches 24 files this feature does not own, and AGENTS.md's Scope Control forbids mixing it into a feature branch. It routes to the same paydown branch as `R-0570` and `R-0752`. The open set was searched for the defect before this id was minted, per §3 item 30: the string `stylelint` occurs ZERO times in the whole of `.agent/live_review.md`, and no finding describes an unenforced design-reference rule. THE CHEAP HALF, for whoever takes the paydown: decide FIRST whether the rule or the code is wrong — 217 violations across two renderer families suggest the rule needs a documented carve-out for canvas colours more than the code needs 217 edits — and only then write the gate, because a gate written against a rule nobody intends to keep is a gate that will be disabled.

DECISION F040 D9 — THE BINDING CSS IS TRANSCRIBED VERBATIM, `color:#fff` INCLUDED, AND F040 DOES NOT DEVIATE FROM ITS OWN FEATURE FILE TO SATISFY AN UNENFORCED RULE. THE PROBLEM: `docs/roadmap/features/T5_F040.md:62-63` binds the hero card's CTA to `background:var(--remedy-blue);color:#fff`, and `docs/ui/design_reference/tokens_rules.md` forbids raw hex in component CSS — so the feature file and the design reference disagree about one declaration, and the round that transcribes the block has to choose. MEASURED at `709dc5d9`, and this is what settles it: the nearest shipped sibling writes the SAME PAIR, `background: var(--remedy-blue); color: #fff;` at `apps/ui/src/components/panels/RightLivePanel.module.css:122`; there is no `--remedy-on-blue` or equivalent foreground token in `apps/ui/src/styles/tokens.css` to substitute; and the prohibition is unenforced with 217 standing violations (finding R-0755). CHOSEN: transcribe the binding block verbatim, `#fff` included, and pin it — the guard asserts that this ONE literal is the sheet's only raw colour and that every other colour is a `var(--remedy-…)` naming a token `tokens.css` actually defines, which is a STRICTER property than the sheet would have had if the literal had been quietly swapped. ALTERNATIVES CONSIDERED: (a) substitute a token — rejected, none exists, so this means inventing one, and `tokens_rules.md` itself requires new tokens to arrive by their own PR rather than as a side effect of a card; (b) write `var(--remedy-ink-inverse, #fff)` against a token that does not exist — rejected as worse than either honest option, since it reads as though a token governs the value while the fallback is doing all the work; (c) amend the feature file's binding CSS — rejected, F040 may not edit its authority to make its own transcription conform, and the disagreement is the design reference's to resolve, not this feature's. HOW TO REVERSE: when the paydown adds a foreground token, the swap is one declaration in one file and one constant in the guard. WHAT IT COSTS TO BE WRONG: one literal in one stylesheet, in step with the component beside it rather than out of step with both authorities.
<<<END RECORD8

## SPEC for C3 — `apps/ui/src/components/digest/DigestHeroCard.module.css`

Read `apps/ui/src/components/diff/DiffView.module.css` for how this repository
writes a feature stylesheet transcribed from a binding block, and
`apps/ui/src/components/panels/RightLivePanel.module.css` for the card and CTA
idiom next door. A new directory `components/digest/` is correct: `components/`
is organised by area and this is the digest's.

Open with a comment naming the AUTHORITY — the feature file, its Design section,
its binding CSS block — so a reader editing a value knows what they are
contradicting, exactly as `DiffView.module.css`'s guard names its own.

TRANSCRIBE the block at `docs/roadmap/features/T5_F040.md:58-64`. It binds three
rules, and the values are not yours to change (constraint 8):

- the card itself — `max-width:720px`, `margin:32px auto`, `padding:28px`,
  `border-radius:var(--remedy-radius-lg)`, `background:var(--remedy-card)`,
  `backdrop-filter:blur(14px)`, `box-shadow:var(--remedy-shadow-soft)`;
- the headline — `font:700 22px/1.2 var(--remedy-font-ui)`,
  `color:var(--remedy-ink)`;
- the CTA — `display:inline-flex`, `padding:10px 18px`,
  `border-radius:var(--remedy-radius-pill)`, `background:var(--remedy-blue)`,
  `color:#fff`, `font-weight:600`.

SELECTOR FORM IS YOURS, VALUES ARE NOT. A CSS module has no global `.digest`, so
name the local classes in this repository's idiom and say in a comment which
binding selector each one transcribes. The feature file writes the headline as
`.digest h2`; a module may prefer a class. Either is fine; the mapping must be
stated.

Add NO animation, NO transition, NO breakpoint and NO colour beyond the block —
see the measured notes at the top of this document for why each is already
satisfied or already out of scope.

## SPEC for C4 — `tests/ui_contracts/test_digest_hero_css.py`

Read `tests/ui_contracts/test_diff_surface_css.py` end to end and follow it
closely: it is the same job for F037's stylesheet and it already solves the
problems this guard has. In particular reuse its shape of naming the AUTHORITY in
every failure message, of stripping `/* */` before reading a rule, and of failing
LOUDLY when a required selector is absent rather than passing over its absence.

Pin, over `apps/ui/src/components/digest/DigestHeroCard.module.css`:

- EVERY BINDING VALUE from the three rules above is present in the rule that
  transcribes it. Assert the values, not the selector names, since the selector
  form is the transcription's to choose: a test that asserted `.digest` would
  fail on a faithful module rename while a card that lost its `max-width` passed.
- EVERY `var(--remedy-…)` THE SHEET NAMES IS A TOKEN `apps/ui/src/styles/tokens.css`
  ACTUALLY DEFINES. Read the token names OUT of `tokens.css` by parsing
  declaration sites rather than retyping a list, so a token renamed upstream
  reddens here. Report the names found.
- THE ONE LITERAL, per DECISION F040 D9: `#fff` occurs EXACTLY ONCE in the sheet
  and it is the CTA's `color`; no other hex and no `rgb(`/`rgba(` literal occurs
  anywhere in it. This is the assertion that makes D9's "stricter than a quiet
  swap" claim true rather than rhetorical, so write it as the point it is.
- NO ANIMATION AND NO BREAKPOINT: the sheet declares no `animation`,
  `transition` or `@media`, which is what makes `ux_spec.md` §16 satisfied by
  construction rather than by a motion block nobody checked.
- A POSITIVE CONTROL proving the reader reaches the file at all, so every
  absence above is distinguishable from a blind read.

## Done when — the gates

Report ONE line per gate with its REAL exit code. Every gate runs at a commit
STRICTLY EARLIER than C5, which writes the handback.

G1 TRANSPORT, at C0b. One sha256 over three files — `.remedy-wt/f040-r8-block.md`,
   the committed `.agent/authored/f040-r8.md` and `.agent/last_block.md` — with
   the byte length, all three EQUAL. This block states no expected digest.

G2 THE PLAN, at C1. `.agent/plan.md` byte-EQUAL to PLAN8 (report both sha256),
   under 50 lines, holding `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure the pre-commit length yourself; the
   reviewer read 1694456 at `709dc5d9`. Base + one separator newline + RECORD8
   equals the committed length. TWO readings: (a) WHOLE RECONSTRUCTION; (b)
   PARAGRAPH ORDER — the last N blank-line units equal RECORD8's N paragraphs IN
   ORDER, N COUNTED by your script. Report that the base bytes are a PREFIX.
   NEGATIVE CONTROL in a disposable worktree: flip one byte inside the FIRST
   appended paragraph and report that BOTH readings reject it and accept the
   unflipped bytes.

G4 THE LEDGER, at C2. Distinct `^- R-\d+ — ` ids with ADDED exactly `['R-0755']`
   and REMOVED `[]`; distinct `^Done: R-\d+` with ADDED `[]`; distinct
   `DECISION F040 D\d+` with ADDED exactly `['D9']`; exactly one
   `^Gate: F040 R7 — ` line. Report the open count and the rise from 261.

G5 THE TRANSCRIPTION, at C3. Report, by parsing the stylesheet rather than by
   eye: every binding value from the three rules and which rule carries it; the
   full list of `--remedy-*` tokens the sheet names, each shown to be defined in
   `apps/ui/src/styles/tokens.css` with the line it is defined on; the count of
   `#fff` (exactly 1) and of every other hex and `rgb(`/`rgba(` literal (exactly
   0); and the counts of `animation`, `transition` and `@media` (each 0). Then
   confirm nothing under `docs/ui/design_reference/` and no `.tsx` is in this
   round's changed-path set.

G6 THE GUARD AND ITS RED PROOF, at C4. First
   `python3 -m pytest tests/ui_contracts/test_digest_hero_css.py -q` — REAL exit
   0 with the passed count. Then, INSIDE A DISPOSABLE WORKTREE, the UNMUTATED
   control FIRST, then FOUR mutations of the STYLESHEET, each reverted before the
   next: (a) change `max-width` from `720px` to `640px`; (b) replace
   `var(--remedy-radius-pill)` with `var(--remedy-radius-nope)`, a token
   `tokens.css` does not define; (c) add a second raw colour, say
   `border:1px solid #abc`; (d) add a `transition: all .2s ease` declaration.
   EACH must redden, and each for its OWN assertion — report the REAL exit code
   and WHICH tests died by node id, never only a count. Restore, re-run, report
   the restored exit code and byte equality. Name the worktree, remove it, and
   report `git worktree list` no longer holds it.

G7 THE FRONTEND NODES ARE UNMOVED, at C4. This round adds no TypeScript and the
   stylesheet is imported by nothing yet, so both nodes must be exactly as the
   reviewer measured them at the base — 4 passed and 1 passed, neither skipped:
   `python3 -m pytest "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" -q -rs`
   and `python3 -m pytest tests/ui_server/test_dashboard_contract.py -k typescript -q -rs`.
   Report the REAL exit code AND passed-or-SKIPPED for each. Per constraint 14 no
   TypeScript colour is ordered.

G8 THE SUITES AND THE TREE, at C4. Each its own REAL exit code:
   `python3 -m pytest tests/ui_contracts/ -q`,
   `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/docs/ -q`, and the canary
   `python3 -m pytest tests/cli/test_golden_path.py -q`. The reviewer measured
   728 passed with 4 skipped, 515, 295 and 42 at the base; `tests/ui_contracts/`
   MUST rise by the number of tests C4 adds, so report both numbers and the
   difference. Then `git status --porcelain` EMPTY, `git ls-files --others
   --exclude-standard` count 0, and the per-commit insertion counts for C0a
   through C4, every one under 500.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: the state
block, the `## Commits` table with a `+/-` column from `git diff --numstat`, the
deviations, the item-status table with every bundle item and every gate
appearing exactly once, and the next steps. State `SESSION 2` of F040 and round
8. No length cap. Record that the stylesheet is transcribed and pinned, that NO
card, NO mount and NO copy audit landed, and that the Acceptance's copy clause is
NOT discharged. Name R-0570, R-0752 and R-0755 as OPEN and routed to paydown,
R-0753 as OPEN and carried, and name the next action as T002 part 4: the hero
card `.tsx`, its mount, the trigger wiring, and the DECISION settling the raw-id
collision PLAN8's Risks names.
