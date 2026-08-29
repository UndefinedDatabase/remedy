# Handback — F040 · SESSION 2 · round 8 — T002 PART 3: THE HERO CARD'S STYLESHEET

> Written by the WORKER in C5, the last commit of the bundle. Every exit code
> below is REAL, taken from `subprocess.run(...).returncode` inside a script
> under the gitignored `.remedy-wt/`; not one was read through a pipe or from
> `$?`.

## Session

SESSION 2 of feature F040 · round 8 · rounds so far 8.

The soft limit (25 rounds / 7 sessions, amend0827 rule 6) is not approached, so
no scope report is owed. `.agent/STOP` did not exist at any reading this round —
checked before the first commit and again before this one.

## Range

Review of `709dc5d9`..`HEAD` on branch `feature/f040-completion-digest`. The
base is round 7's handback commit and was the tip of the branch when this round
opened. No new branch was cut, no pull request opened, nothing merged, nothing
force-pushed, and no commit touched `main`.

## What this round did and did NOT do

DID: transcribed the binding CSS block of
`docs/roadmap/features/T5_F040.md:58-64` into a real stylesheet at
`apps/ui/src/components/digest/DigestHeroCard.module.css`, and pinned that
transcription with a Python conformance guard at
`tests/ui_contracts/test_digest_hero_css.py` — red-proved with four stylesheet
mutations, each dying on its own assertion. Booked the round 7 verdict,
registered R-0755 and ruled DECISION F040 D9.

DID NOT, and this round claims none of it: NO hero card `.tsx` was created, NO
mount landed, NO trigger was wired, and NO copy audit was performed. The
Acceptance clause about the returning-user copy ("since you were last here") is
NOT discharged, nor is the CTA's behaviour, nor the trigger wiring, nor anything
requiring markup. The split is the one F037 used at its own R9 and is recorded
in the block's rationale: this repository cannot render a component in a test
(DECISION F040 D7), so shipping the sheet with a Python guard first is what buys
this round a real red proof instead of a green word.

## Commits

Six commits, C0a through C4, plus this one. `+/-` is from
`git diff --numstat <sha>^ <sha>`.

### e6fdea5f docs(f040): save the round 8 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f040-r8.md` | +314 / -0 | C0a — the round's step block saved verbatim with `shutil.copyfile`, per constraint 2 |

### 8ff37c54 docs(f040): mirror the round 8 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +219 / -294 | C0b — the same bytes mirrored, again by `shutil.copyfile`; git reports the pair as an 86% rewrite, so `git commit`'s own line reads `314 insertions(+), 389 deletions(-)` while `--numstat` reads 219/294 on the same commit. Both are under 500; the table carries the `--numstat` figure the template asks for |

### 6103af94 docs(f040): retarget the plan at the hero card stylesheet
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +18 / -16 | C1 — rewritten byte-for-byte from slice PLAN8; the first substantive commit, ahead of the ledger append (constraint 3) |

### b9b15ff1 docs(f040): book the round 7 verdict and R-0755
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +6 / -0 | C2 — slice RECORD8 appended: the R7 PASS verdict, finding R-0755 and DECISION F040 D9. Append-only (constraint 4) |

### 771288fd feat(f040): transcribe the hero card binding stylesheet
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/components/digest/DigestHeroCard.module.css` | +60 / -0 | C3 — new file, new directory `components/digest/`. Three rules transcribed from the feature file's binding block; header comment names the authority and states the selector mapping |

### 14ef067e test(f040): pin the hero card stylesheet to its binding block
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_contracts/test_digest_hero_css.py` | +256 / -0 | C4 — seven tests: a positive control, one per binding rule, the token-definition sweep, the single-literal pin of D9, and the no-motion/no-breakpoint pin |

### C5 — this commit
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this rewrite | C5 — the handback. A handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add .remedy-wt/f040r8-g3wt HEAD` | exit 0 — G3's negative control |
| `git worktree remove --force .remedy-wt/f040r8-g3wt` | exit 0 — removed; `git worktree list` no longer holds it |
| `git worktree add .remedy-wt/f040r8-g6wt HEAD` | exit 0 — G6's red proof |
| `git worktree remove --force .remedy-wt/f040r8-g6wt` | exit 0 — removed; `git worktree list` shows only the primary checkout |
| `git push -u origin feature/f040-completion-digest` | run after this commit; result recorded in the session output |

No pull request was created, edited or merged. No `gh` command was run. No
force-push, no branch deletion, no history rewrite. The `remedy` console script
is denied to this session (constraint 11) and was not invoked; nothing this
round needed it, so no `python3 -m apps.cli.main` fallback was used either.

## Verification

Eight gates, each at a commit strictly earlier than C5. One line per gate with
its REAL exit code, then the decisive readings.

| Gate | At | REAL exit code |
|---|---|---|
| G1 TRANSPORT | C0b `8ff37c54` | 0 |
| G2 THE PLAN | C1 `6103af94` | 0 |
| G3 THE RECORD APPEND | C2 `b9b15ff1` | 0 |
| G4 THE LEDGER | C2 `b9b15ff1` | 0 |
| G5 THE TRANSCRIPTION | C3 `771288fd` | 0 |
| G6 THE GUARD AND ITS RED PROOF | C4 `14ef067e` | 0 |
| G7 THE FRONTEND NODES ARE UNMOVED | C4 `14ef067e` | 0 |
| G8 THE SUITES AND THE TREE | C4 `14ef067e` | 0 |

### G1 TRANSPORT — REAL exit code 0

One sha256 over three files, all equal:

    .remedy-wt/f040-r8-block.md  sha256=faa78f87e238e94ca7aea52c2a009d155dcfed083ab5e3ac70550deed30d321c  bytes=26546
    .agent/authored/f040-r8.md   sha256=faa78f87e238e94ca7aea52c2a009d155dcfed083ab5e3ac70550deed30d321c  bytes=26546
    .agent/last_block.md         sha256=faa78f87e238e94ca7aea52c2a009d155dcfed083ab5e3ac70550deed30d321c  bytes=26546
    ALL THREE EQUAL: True

The block states no expected digest, so this is a three-way equality and not a
comparison against a written constant. The digest was verified against the
dispatch message before any file was written.

### G2 THE PLAN — REAL exit code 0

    PLAN8 slice    sha256=7f5ac75a13437b4f07ffb3305ffca9e912d6f0bc16a6267284df62edc1fb6122 bytes=1969
    .agent/plan.md sha256=7f5ac75a13437b4f07ffb3305ffca9e912d6f0bc16a6267284df62edc1fb6122 bytes=1969
    BYTE-EQUAL: True
    line count: 41  under 50: True
    holds '## Goal': True   holds '## Next Steps': True

### G3 THE RECORD APPEND — REAL exit code 0

Pre-commit length re-measured by the script, not taken from the block:

    PRE-COMMIT base bytes: 1694456        (equals the reviewer's reading at 709dc5d9)
    RECORD8 bytes: 9514
    base ends with newline: True
    arithmetic: 1694456 + 1 + 9514 = 1703971
    committed bytes: 1703971
    (a) WHOLE RECONSTRUCTION: True
    N counted by this script: 3
    (b) PARAGRAPH ORDER, last 3 units equal RECORD8's 3 in order: True
        para 1: 'Gate: F040 R7 — T002 PART 2, THE TRIGGER RULE. VERDICT PASS. Reviewed …'
        para 2: '- R-0755 — Low, A DESIGN RULE DECLARES ITS OWN ENFORCEMENT AND THAT EN…'
        para 3: 'DECISION F040 D9 — THE BINDING CSS IS TRANSCRIBED VERBATIM, `color:#ff…'
    BASE BYTES ARE A PREFIX: True
    committed sha256=0a14f7fcd04cd5cce45f5edf663df3dc01086e29cc369f9920b2e3e1c3cda6f0 bytes=1703971

NEGATIVE CONTROL, in the disposable worktree `.remedy-wt/f040r8-g3wt`:

    worktree copy bytes: 1703971  equal to primary committed: True
    UNFLIPPED: reading (a) accepts: True   reading (b) accepts: True
    flip offset 1694557, inside the FIRST appended paragraph (which ends at 1699065): True
    byte at 1694557: 't' -> 'u'
    FLIPPED:  reading (a) accepts: False  reading (b) accepts: False
    BOTH READINGS REJECT THE FLIP: True
    RESTORED: reading (a) accepts: True   reading (b) accepts: True
    git worktree remove --force  -> REAL exit code 0
    git worktree list -> only /home/decodeux/Repos/remedy; 'f040r8-g3wt' still listed: False

Both readings therefore discriminate: they accept the real bytes and reject a
single flipped byte inside the first appended paragraph.

### G4 THE LEDGER — REAL exit code 0

Distinct-id sets, taken before and after the C2 commit over the same file:

    registered ADDED: ['R-0755']   REMOVED: []
    resolved ADDED: []
    DECISION F040 ADDED: ['DECISION F040 D9']
    count of '^Gate: F040 R7 — ' lines: 1
    open count before: 261   after: 262   rise: 1

The rise of exactly one is what a round that registers one finding and resolves
none must show.

### G5 THE TRANSCRIPTION — REAL exit code 0

Read by parsing the stylesheet with comments stripped, never by eye. Every
binding value, and the rule that carries it:

    .heroCard      max-width:720px                            True
    .heroCard      margin:32px auto                           True
    .heroCard      padding:28px                               True
    .heroCard      border-radius:var(--remedy-radius-lg)      True
    .heroCard      background:var(--remedy-card)              True
    .heroCard      backdrop-filter:blur(14px)                 True
    .heroCard      box-shadow:var(--remedy-shadow-soft)       True
    .heroHeadline  font:700 22px/1.2 var(--remedy-font-ui)    True
    .heroHeadline  color:var(--remedy-ink)                    True
    .heroCta       display:inline-flex                        True
    .heroCta       padding:10px 18px                          True
    .heroCta       border-radius:var(--remedy-radius-pill)    True
    .heroCta       background:var(--remedy-blue)              True
    .heroCta       color:#fff                                 True
    .heroCta       font-weight:600                            True

Every `--remedy-*` token the sheet names, each shown defined in
`apps/ui/src/styles/tokens.css` with its definition line:

    --remedy-blue           line 21
    --remedy-card           line 48
    --remedy-font-ui        line  3
    --remedy-ink            line  6
    --remedy-radius-lg      line 57
    --remedy-radius-pill    line 63
    --remedy-shadow-soft    line 66

Seven named, seven defined, none missing.

    '#fff' count: 1   other hex literals: 0 []   rgb(/rgba( literals: 0
    animation: 0   transition: 0   @media: 0

Changed-path set for `709dc5d9..HEAD` at C3:

    .agent/authored/f040-r8.md
    .agent/last_block.md
    .agent/live_review.md
    .agent/plan.md
    apps/ui/src/components/digest/DigestHeroCard.module.css

    under docs/ui/design_reference/: []      .tsx paths: []

Nothing under `docs/ui/design_reference/` is touched — it is the authority this
round transcribes FROM — and no `.tsx` is in the set.

### G6 THE GUARD AND ITS RED PROOF — REAL exit code 0

First, in the primary checkout:

    $ python3 -m pytest tests/ui_contracts/test_digest_hero_css.py -q
    7 passed in 0.18s
    REAL exit code: 0

Then inside the disposable worktree `.remedy-wt/f040r8-g6wt`, with every
`__pycache__` purged and every run under `python3 -B`. Control FIRST, each
mutation reverted before the next, node ids never summarised to a count:

    [control]  REAL exit 0   7 passed              failing node ids: none

    [a max-width 720px -> 640px]                   REAL exit 1   1 failed, 6 passed
        tests/ui_contracts/test_digest_hero_css.py::TestDigestHeroStylesheet::test_the_card_rule_carries_every_binding_value
        reverted, sha256 back to original: True

    [b --remedy-radius-pill -> --remedy-radius-nope]  REAL exit 1   2 failed, 5 passed
        tests/ui_contracts/test_digest_hero_css.py::TestDigestHeroStylesheet::test_every_referenced_token_is_defined_in_the_shipped_sheet
        tests/ui_contracts/test_digest_hero_css.py::TestDigestHeroStylesheet::test_the_cta_rule_carries_every_binding_value
        reverted, sha256 back to original: True

    [c add `border: 1px solid #abc`]               REAL exit 1   1 failed, 6 passed
        tests/ui_contracts/test_digest_hero_css.py::TestDigestHeroStylesheet::test_the_cta_white_is_the_only_raw_colour_in_the_sheet
        reverted, sha256 back to original: True

    [d add `transition: all .2s ease`]             REAL exit 1   1 failed, 6 passed
        tests/ui_contracts/test_digest_hero_css.py::TestDigestHeroStylesheet::test_the_sheet_declares_no_motion_and_no_breakpoint
        reverted, sha256 back to original: True

    [restored] REAL exit 0   7 passed              failing node ids: none
    byte equality with the committed stylesheet: True; with the primary checkout: True
    git worktree remove --force -> REAL exit code 0
    git worktree list -> 'f040r8-g6wt' still listed: False

Each mutation reddens, and each reddens its own assertion. Mutation (b) kills
TWO tests rather than one, and that is honest rather than a defect of the
design: naming a token `tokens.css` does not define both breaks the CTA's bound
`border-radius` value AND breaks the token-definition sweep. It is the only
mutation of the four that reaches the token sweep, so the four remain mutually
distinguishable. See deviation 3.

### G7 THE FRONTEND NODES ARE UNMOVED — REAL exit code 0

    $ python3 -m pytest "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation" -q -rs
    4 passed in 1.23s
    REAL exit code: 0        PASSED, not skipped

    $ python3 -m pytest tests/ui_server/test_dashboard_contract.py -k typescript -q -rs
    1 passed, 73 deselected in 2.02s
    REAL exit code: 0        PASSED, not skipped

Both are exactly as the reviewer measured them at the base — 4 and 1, neither
skipped. This round adds no TypeScript and the stylesheet is imported by
nothing yet, so no TypeScript colour was ordered and none was taken
(constraint 14, DECISION F040 D7).

### G8 THE SUITES AND THE TREE — REAL exit code 0

Four suites, run serially, each its own REAL exit code:

    $ python3 -m pytest tests/ui_contracts/ -q      735 passed, 4 skipped in 5.84s    REAL exit 0
    $ python3 -m pytest tests/ui_server/ -q         515 passed in 33.52s              REAL exit 0
    $ python3 -m pytest tests/docs/ -q              295 passed in 0.44s               REAL exit 0
    $ python3 -m pytest tests/cli/test_golden_path.py -q   42 passed in 20.74s        REAL exit 0

`tests/ui_contracts/` rose from the base 728 to 735, a difference of **7**,
which is exactly the number of tests C4 adds; the four pre-existing skips are
unmoved. `tests/ui_server/`, `tests/docs/` and the canary are unchanged at 515,
295 and 42.

    $ git status --porcelain                 -> EMPTY (True)
    $ git ls-files --others --exclude-standard -> untracked count 0

Per-commit insertions, C0a through C4, from `git diff --numstat`:

    e6fdea5f  +314   under 500: True
    8ff37c54  +219   under 500: True
    6103af94  +18    under 500: True
    b9b15ff1  +6     under 500: True
    771288fd  +60    under 500: True
    14ef067e  +256   under 500: True

Every one is under 500 insertions. No oversize commit is declared, because
there is none.

## Authored-text proofs

Two reviewer-authored slices were applied this round. Both were extracted
MECHANICALLY from `.remedy-wt/f040-r8-block.md` by a script
(`.remedy-wt/f040r8/extract.py`) that splits on the exact marker lines
`<<<BEGIN NAME` / `<<<END NAME`, drops the markers and keeps the newline ending
the last content line. Neither was retyped.

| Slice | Applied to | Slice sha256 / bytes | Disk sha256 / bytes | Equal |
|---|---|---|---|---|
| PLAN8 | `.agent/plan.md` | `7f5ac75a…1f6122` / 1969 | `7f5ac75a…1f6122` / 1969 | yes, byte-for-byte |
| RECORD8 | appended to `.agent/live_review.md` | `79f9dcc5…7bd643` / 9514 | reconstructed exactly as base + `\n` + slice, 1694456 + 1 + 9514 = 1703971 | yes |

The step block itself was copied, not authored: `.agent/authored/f040-r8.md` and
`.agent/last_block.md` both carry
`faa78f87e238e94ca7aea52c2a009d155dcfed083ab5e3ac70550deed30d321c` over 26546
bytes, identical to the source file (G1).

## Deviations & assumptions

1. **Commit sequence: NONE. The bundle ran C0a, C0b, C1, C2, C3, C4, C5 in the
   block's order, with no extra commit, no dropped commit and no reordering.**
   Stated here explicitly because this section, not the commit table, is where
   an auditor reads whether a round followed its block (finding R-0485).

2. **The `--numstat` and the `git commit` insertion figures disagree for C0b.**
   `git commit` printed `314 insertions(+), 389 deletions(-)` with
   `rewrite .agent/last_block.md (86%)`; `git diff --numstat 8ff37c54^ 8ff37c54`
   reads `219 294`. The two differ only in how the rewrite is diffed, not in the
   file's content — the file's sha256 equals the block's exactly (G1). The
   commit table carries the `--numstat` figure the handback template asks for,
   and the `git commit` figure is recorded here so the reviewer re-running
   either command sees both. Both are under 500 on either reading.

3. **Mutation (b) of G6 kills two tests, not one.** The block asks that each
   mutation redden "for its OWN assertion". Replacing
   `var(--remedy-radius-pill)` with an undefined `var(--remedy-radius-nope)`
   fails BOTH the CTA's binding-value test (the bound declaration is
   `border-radius:var(--remedy-radius-pill)`, so the CTA rule no longer carries
   its full set) AND the token-definition sweep. This is a property of the
   mutation, not of the guard: the mutation changes two things at once, a bound
   value and a token name. The four mutations remain mutually distinguishable —
   (b) is the only one that reaches the token sweep — and every failing node id
   is reported above rather than a count.

4. **The guard locates each binding rule by its DECLARATIONS, never by its
   selector name.** The SPEC requires asserting the values and not the selector
   names, because the module's selector form is the transcription's to choose.
   The implementation therefore searches every parsed rule for the one carrying
   a binding rule's complete declaration set, and additionally asserts that
   EXACTLY ONE rule carries it — a card whose bound declarations were split
   across two rules would be as unreviewable as one that lost them. The
   binding selectors `.digest`, `.digest h2` and `.digest .cta` appear in
   failure TEXT only, where they name the authority.

5. **The stylesheet's class names are `.heroCard`, `.heroHeadline` and
   `.heroCta`.** A CSS module has no global `.digest` (constraint 8 permits
   adapting selector FORM), and camelCase is this package's convention — the
   same mapping `DiffView.module.css` documents for F037. The mapping from each
   binding selector to each local class is stated in the stylesheet's header
   comment, as the SPEC requires.

6. **`color: #fff` is transcribed verbatim, per constraint 9 and DECISION
   F040 D9, and no doubt is declared about it.** The value was checked rather
   than assumed: `apps/ui/src/styles/tokens.css` defines no `--remedy-*`
   foreground token to carry it, and the nearest shipped sibling
   `apps/ui/src/components/panels/RightLivePanel.module.css` writes the same
   `background: var(--remedy-blue); color: #fff;` pair. The guard pins it as the
   sheet's ONLY raw colour, which is the stricter property D9 trades for.

7. **No breakpoint, no motion block, no extra colour was added**, per the
   block's measured notes. The guard asserts the ABSENCE of `animation`,
   `transition`, `transform` and `@media` rather than the presence of a motion
   rule, so `ux_spec.md` §16 stays satisfied by construction. `transform` is
   asserted in addition to the two the SPEC names; the block's own rationale
   states the binding CSS "declares no animation, no transition and no
   transform", so the third is the same obligation and not a widened scope.

8. **A NEW DIRECTORY was created: `apps/ui/src/components/digest/`.** The change
   set names the file inside it, and `components/` is organised by area, so this
   is the digest's. No other path outside the change set was created, edited or
   deleted.

9. **Sandbox: `cp` and env-var assignment were not used.** Both copies (C0a,
   C0b) went through `shutil.copyfile` per constraint 2. Every command ran as a
   single Bash invocation of one `python3 <script>`, with no `&&` chain, no
   `$(...)` inside a compound and no process substitution. Every exit code
   quoted above is `subprocess.run(...).returncode`. The `remedy` console script
   was not invoked (constraint 11).

10. **Scratch scripts live under the gitignored `.remedy-wt/f040r8/`** and are
    not in the change set; `git status --porcelain` is empty and
    `git ls-files --others --exclude-standard` counts 0 (G8). The two
    disposable worktrees were created under `.remedy-wt/` and both were removed;
    `git worktree list` shows only the primary checkout.

## Item status

Every bundle item and every gate, exactly once.

| Item | Status | Reason |
|---|---|---|
| C0a save the block to `.agent/authored/f040-r8.md` | done | `e6fdea5f`, by `shutil.copyfile` |
| C0b mirror the same bytes into `.agent/last_block.md` | done | `8ff37c54`, by `shutil.copyfile` |
| C1 rewrite `.agent/plan.md` from PLAN8 | done | `6103af94`, byte-equal |
| C2 append RECORD8 to `.agent/live_review.md` | done | `b9b15ff1`, append-only |
| C3 create `DigestHeroCard.module.css` | done | `771288fd`, 60 insertions |
| C4 create `tests/ui_contracts/test_digest_hero_css.py` | done | `14ef067e`, 7 tests |
| C5 rewrite `.agent/handoff.md` | done | this commit |
| G1 TRANSPORT | done | REAL exit 0 |
| G2 THE PLAN | done | REAL exit 0 |
| G3 THE RECORD APPEND | done | REAL exit 0, negative control included |
| G4 THE LEDGER | done | REAL exit 0 |
| G5 THE TRANSCRIPTION | done | REAL exit 0 |
| G6 THE GUARD AND ITS RED PROOF | done | REAL exit 0, four mutations |
| G7 THE FRONTEND NODES ARE UNMOVED | done | REAL exit 0, 4 and 1, neither skipped |
| G8 THE SUITES AND THE TREE | done | REAL exit 0, 735/515/295/42, tree clean |
| R-0570 | open | routed to the paydown branch; not F040's to fix |
| R-0752 | open | routed to the paydown branch; not F040's to fix |
| R-0755 | open | registered this round in C2; routed to the paydown branch, not F040's to fix |
| R-0753 | open | carried as this feature's documented risk |

No item was skipped and none deviated.

## Findings

REGISTERED this round: **R-0755** (Low) — a design rule in
`docs/ui/design_reference/tokens_rules.md` declares its own stylelint/ESLint
enforcement, that enforcement does not exist anywhere under `apps/ui/`, and 217
shipped declarations break the rule. Full text is in `.agent/live_review.md` at
C2. Not F040's to fix: the repair either adds a toolchain dependency and a CI
stage or amends the design reference, and it touches files this feature does not
own.

RESOLVED this round: none.

OPEN and routed to the paydown branch: **R-0570**, **R-0752**, **R-0755**.
OPEN and carried as this feature's documented risk: **R-0753**.
Open findings count after C2: **262**, a rise of exactly 1 from 261.

DECISION ruled this round: **F040 D9** — the binding CSS is transcribed verbatim,
`color:#fff` included, and F040 does not deviate from its own feature file to
satisfy an unenforced rule.

## Next

T002 PART 4: the hero card `.tsx`, its mount and the copy audit. Concretely:
create the component that consumes
`apps/ui/src/components/digest/DigestHeroCard.module.css`, wire its trigger onto
the already-shipped `apps/ui/src/api/digestVisibility.ts`, bind the dismissal
port at the edge per DECISION F040 D8, and perform the copy audit the Acceptance
names — which this round did NOT discharge.

That round must also settle the collision PLAN8's Risks records and rule it as a
DECISION rather than choosing silently: `ux_spec.md` §17 forbids the UI showing
raw UUIDs, while the digest envelope's `primary_action.label` embeds a job-id
prefix and a `td:` decision id, visible in the R5 goldens. Either the card
humanises that label or the envelope stops carrying it.

Before that round is authored, Phase 1 rule 1 comes first: re-read `.agent/STOP`
from disk. Then rule 2, the Open PR Gate.
