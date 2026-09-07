# Handoff — F272 One world completion, round 12

## Session

SESSION 6 of feature F272 · round 12 · rounds so far 12

Context self-assessment (amend0905-throughput): context is comfortable — this round
read two TypeScript modules and three test regions, ran four short suites and two
disposable worktrees, and wrote nine lines of production code, so a further round in
this session is affordable.

THE ROUND IS COMPLETE. C0a through C7 all landed in the ordered sequence, nothing was
reordered and no commit was made outside it. R-0821's fix is on disk: `blocked` and
`stopped` are settled states in `digestVisibility.ts` and carry `"Blocked"` and
`"Stopped"` in `digestCardCopy.ts`, and `tests/ui_contracts/` reads EXIT 0 at 809
passed, 0 failed, 4 skipped where the base read EXIT 1 at 2 failed, 807 passed, 4
skipped.

## Range

Review of `fcde1983`..`HEAD` (branch `feature/f272-one-world-completion`).

## Commits

### d1bb92a9 f272: save the round 12 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f272-r12.md` | +395 / -0 | C0a, `shutil.copyfile` of the reviewer's scratch original |

### f929564d f272: mirror the round 12 step block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +276 / -244 | C0b, byte copy of the same original |

### b3a8644e f272: set the plan to the round 12 guard and modules step
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +12 / -10 | C1, replaced by the PLANF272R12 slice |

### 879504f7 f272: book the round 11 PASS verdict, correct R-0821 and two prose slips
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4 / -0 | C2, RECORDR12 appended |
| `.agent/prose_slips.md` | +4 / -0 | C2, SLIPSR12 appended |

### 64bed56f f272: rule the run-state phrase guard a floor in DECISION F272 D9
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T2_F272.md` | +47 / -0 | C3, DECISIONR12 appended |

### a39dfe52 f272: make the run-state phrase vacuity guard a floor per DECISION F272 D9
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_contracts/test_digest_hero_card.py` | +3 / -3 | C4, `== 7` → `>= 7` at line 230 and two docstring numerals |

### dd51f8a6 f272: give blocked and stopped their place in the two digest cockpit modules
| Path | +/- | Reason |
|---|---|---|
| `apps/ui/src/api/digestVisibility.ts` | +13 / -4 | C5, `SETTLED_STATES` gains both states; two counting comments rewritten |
| `apps/ui/src/api/digestCardCopy.ts` | +5 / -2 | C5, `DIGEST_STATE_LABELS` gains both entries; the "seven" comment rewritten |

### 2868d924 f272: record R-0821 as landed by the round 12 module commit
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2 / -0 | C6, the single `Landed: R-0821` line |

### C7 — this handoff
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | self-referential | C7 cannot table the commit that writes it (R-0149 pattern) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | `.agent/authored/f272-r12.md`, `shutil.copyfile`, digest verified BEFORE any other action |
| C0b | done | `.agent/last_block.md`, byte copy of the same original |
| C1 | done | plan replaced by the PLANF272R12 slice, byte-equal at 2284 B / 44 lines |
| C2 | done | RECORDR12 and SLIPSR12 appended; every ordered count matched exactly |
| C3 | done | DECISION F272 D9 appended; headings read D1..D9 in order |
| C4 | done | ONE assertion and TWO docstrings in ONE file; the suite read EXACTLY the base afterwards |
| C5 | done | both modules; the suite went EXIT 0 at 809 / 0 / 4 |
| C6 | done | one `Landed: R-0821 — ` line, no `Done:` paragraph, no second line |
| C7 | done | this handoff |

No commit exists outside this ordered sequence: the range holds exactly eight commits
before this handoff and they are C0a, C0b, C1, C2, C3, C4, C5 and C6 in that order.

## Verification

One line per gate with its REAL exit code, then the transcripts. "Green" as a word
appears nowhere.

| Gate | Exit | Reading |
|---|---|---|
| G1 TRANSPORT | 0 | three artefacts, all 29750 bytes / 395 lines, all sha256 `bac95d44…3845a238a` |
| G2 THE RECORD | 0 | readers (a)(b)(c)(d) accept over both files; every ordered count matched, including the three that had to STAY put |
| G3 PLAN + FEATURE FILE | 0 | plan byte-equal at 2284 B / 44 lines; feature file readers accept; D1..D9 |
| G4 THE GUARD IS STILL A GUARD | 0 | (i) EXACTLY the base — EXIT 1, 2 failed, 807 passed, 4 skipped; (ii) discriminator passes; (iii) the real assertion still bites |
| G5 THE TWO RED TESTS GO GREEN | 0 | 809 passed, 0 failed, 4 skipped; red control fires naming `blocked`; both labels readable |
| G6 VITEST AND THE SUITES | 0, 0, 0 | vitest node 52 passed; `tests/docs/` 303; canary 42 — all matching base |
| G7 LINT AND INTEGRITY | 0 and 0 | ruff clean over the one changed `.py` file; integrity `"passed": true` |
| G8 THE TREE | 0 | tree empty, `git ls-files .remedy-wt` empty, both worktrees removed by exact path and pruned |

### G1 TRANSPORT — a real three-artefact chain

Per §3 item 37 this covers the saved copy and its mirror, NOT the bytes emitted into
my prompt. The digest and length were verified against the file BEFORE any other
action, and re-read here from the COMMITTED blobs.

| Artefact | Bytes | Lines | sha256 |
|---|---|---|---|
| `.remedy-wt/f272-r12-block.md` (reviewer's surviving original) | 29750 | 395 | `bac95d441478084ec6cc29c60adc7b17fc571d82b689e0ea11600fa3845a238a` |
| `.agent/authored/f272-r12.md` at HEAD (C0a) | 29750 | 395 | same |
| `.agent/last_block.md` at HEAD (C0b) | 29750 | 395 | same |

All three equal each other and equal the delegation's BLOCK_SHA, BLOCK_LENGTH and
BLOCK_LINES.

### G2 THE RECORD at C2 and at C6 — exit 0

`.agent/live_review.md` ← RECORDR12, readers (a) to (d):

- (a) BYTE: pre 1127168 → post 1132490; pre a byte-exact prefix; `post == pre + b"\n" +
  slice` TRUE; pre's terminal byte asserted to be exactly one `\n` BEFORE writing;
  post ends in exactly one `\n`. Slice 5321 bytes, sha256 `7c79ef8f7688…`.
- (b) STRUCTURAL, computed independently of (a) by splitting the WHOLE image on
  `\n{2,}`: N counted by my script from the slice's own paragraphs = 2; units 703 →
  705, delta 2; the last 2 units equal the slice's paragraphs in order; the units
  before are an unchanged prefix.
- (c) NEGATIVE CONTROL, in memory on a `bytes` object, never on disk: offset 1127189
  asserted to lie inside the FIRST appended paragraph `[1127169, 1131119)`, one bit
  flipped — reader (a) rejected AND reader (b) rejected; restored, both accepted, and
  the restored image equalled the disk image.
- (d) COUNTS before → after C2, every one exactly as ordered:

| reading | ordered | measured |
|---|---|---|
| `^- R-\d{4} — ` distinct ids | 305 → 305 | 305 → 305 |
| `^Done: R-\d{4} — ` distinct | 247 → 247 | 247 → 247 |
| open set BY DISTINCT ID | 58 → 58 | 58 → 58 |
| `^Gate: ` | 33 → 34 | 33 → 34 |
| `^Gate: F272 R11 ` | 0 → 1 | 0 → 1 |

The first three are unchanged because this round mints no id and resolves none, which
is exactly what the block ordered and what constraint 6 requires.

`.agent/prose_slips.md` ← SLIPSR12, readers (a), (b) and the same negative control:
pre 139621 → post 141124; prefix, append arithmetic and terminal newline all TRUE; N
counted 2, units 177 → 179, the last 2 units equal the slice's paragraphs in order;
the control's flip at offset 139642 (inside the first appended paragraph
`[139622, 140423)`) was rejected by both readers and the restore equalled the disk
image. Slice 1502 bytes, sha256 `fc18b45c7283…`.

AFTER C6, as the block orders:

| reading | ordered | measured |
|---|---|---|
| `^Landed: R-0821 ` | 0 → 1 | 0 → 1 |
| `^Done: R-0821 ` | still 0 | 0 |

C6's own append arithmetic: pre 1132490 → post 1132952, `post == pre + b"\n" + line`
TRUE, the appended text is exactly ONE line, and `^Gate: ` stayed 34.

### G3 THE PLAN at C1, AND THE FEATURE FILE at C3 — exit 0

Plan: `.agent/plan.md` equals the PLANF272R12 slice bytes exactly. Both byte lengths
2284. 44 lines against the AGENTS.md cap of 50. `## Goal` present, `## Next Steps`
present.

Feature file: readers (a) and (b), no negative control (gate budget). Pre 32918 →
post 35898; prefix, append arithmetic and terminal newline all TRUE; N counted 7,
units 70 → 77, the last 7 units equal the slice's paragraphs in order. Lines matching
`^### DECISION F272 D\d+ ` counted by me: 8 before, 9 after, naming in order
D1 D2 D3 D4 D5 D6 D7 D8 D9.

### G4 THE GUARD IS STILL A GUARD, at C4 — exit 0

**THE BASE, measured by me in the primary checkout before C4 was written:**

    python3 -B -m pytest tests/ui_contracts/ -q -p no:randomly
    EXIT = 1 — 2 failed, 807 passed, 4 skipped in 6.28s
    FAILED …/test_digest_card_copy.py::TestEveryRunStateIsAccountedFor::test_all_seven_run_states_are_named_by_the_label_map
    FAILED …/test_job_digest_card_contract.py::TestTheTriggerRuleIsPureAndPortless::test_all_seven_run_states_are_accounted_for_in_the_rule

Exactly the three numbers the block names, and the two failures are the pair R-0821
names.

**G4(i) AFTER C4, the same command:**

    EXIT = 1 — 2 failed, 807 passed, 4 skipped in 6.35s

EXACTLY the base, as the block requires. C4 loosened a bound that 7 already satisfied,
so nothing moved — no test changed colour, and the count proves C4 did no more than it
was ordered to.

**G4(ii) THE DISCRIMINATOR, named explicitly with its own result:**

    python3 -B -m pytest "tests/ui_contracts/test_digest_hero_card.py::\
    TestNoRuleHasASecondHome::test_the_phrase_restatement_scan_can_see_a_restated_phrase" \
        -q -p no:randomly
    EXIT = 0 — 1 passed in 0.19s

`test_the_phrase_restatement_scan_can_see_a_restated_phrase` PASSES. It was not
touched by C4 and it is the thing that keeps the loosened floor honest.

**G4(iii) THE REAL ASSERTION STILL BITES** — run in the disposable worktree
`.remedy-wt/f272-r12-g4` at `a39dfe52`, the commit C4 creates, never in the primary
checkout. `CARD` in that test module is the expression
`UI_SRC / "components" / "digest" / "DigestHeroCard.tsx"`, and I printed the path it
resolves to rather than assuming it:

    CARD RESOLVED PATH: …/.remedy-wt/f272-r12-g4/apps/ui/src/components/digest/DigestHeroCard.tsx
    exists: True   bytes: 5568   sha256 before: 1f4f084e…c92e467dc

5568 bytes, exactly as the block states. The phrase restated is the one the parser
itself returns first, `'Waiting to start'`, added as `const leak = "Waiting to start";`:

| run | exit | reading |
|---|---|---|
| before the restatement | 0 | 1 passed |
| with the phrase restated as a literal | **1** | `AssertionError: … found ['Waiting to start'] restated as literals here` |
| after restore | 0 | 1 passed |

The failure names the phrase. The restore is byte-identical — sha256 back to
`1f4f084e…c92e467dc`. Loosening `==` to `>=` did NOT turn the test vacuous.

### G5 THE TWO RED TESTS GO GREEN, at C5 — exit 0

**G5(i)** `python3 -B -m pytest tests/ui_contracts/ -q -p no:randomly`

    EXIT = 0 — 809 passed, 4 skipped in 6.70s

Against the base of 2 failed / 807 passed / 4 skipped: passed rose by exactly 2 to
**809**, failed is **0**, skipped stayed **4**. All three numbers as ordered.

**G5(ii) THE RED CONTROL**, in the disposable worktree `.remedy-wt/f272-r12-g5` at
`dd51f8a6`, the commit C5 creates. The byte string `  "blocked",\n` occurs exactly
**1** time in `digestVisibility.ts` (§3 item 25) — which is why C5 wrote that array
multi-line. File sha256 `3cceb6ea…43372ff8` before:

    python3 -B -m pytest tests/ui_contracts/test_job_digest_card_contract.py -q -p no:randomly
    before removal:            EXIT = 0 — 29 passed in 0.28s
    with "blocked" removed:    EXIT = 1 — 1 failed, 28 passed in 0.30s
    E  AssertionError: ['blocked'] appear in RunState but not in digestVisibility.ts, …
    after restore:             EXIT = 0 — 29 passed in 0.28s

The failure names `blocked` and ONLY `blocked` — `stopped` does not appear in it,
which is the discrimination the control is for. Restored file sha256 back to
`3cceb6ea…43372ff8`, byte-identical.

**G5(iii) WHAT A READER OF THE CARD ACTUALLY SEES**, parsed out of the module rather
than inferred from test names:

| call | answer | is `UNREADABLE_STATE_LABEL` |
|---|---|---|
| `digestStateLabel("blocked")` | `"Blocked"` | False |
| `digestStateLabel("stopped")` | `"Stopped"` | False |

`UNREADABLE_STATE_LABEL` is still `"State not recorded"`, unchanged. The label map
carries nine keys in `RunState` declaration order: `pending, planned, running, paused,
completed, failed, cancelled, blocked, stopped`. `DIGEST_CTA_RULE_IDS` is UNTOUCHED and
still reads `open-decision, stopped-by-operator, blocked-failed, all-green,
indeterminate` — those are rule ids from `recommended_next_action`, the different
vocabulary the module's own comment names as a trap.

### G6 VITEST AND THE SUITES — run SERIALLY, each its own invocation

| invocation | exit | summary line | base |
|---|---|---|---|
| `tests/orchestration/test_test_runner.py` (VITEST) | 0 | `52 passed in 5.86s` | 52 |
| `tests/docs/` | 0 | `303 passed in 0.49s` | 303 |
| `tests/cli/test_golden_path.py` (THE CANARY) | 0 | `42 passed in 20.84s` | 42 |

The vitest node ran in the PRIMARY CHECKOUT, the only tree carrying
`apps/ui/node_modules`. It did not go red, so there was nothing to report verbatim and
NO `.test.ts` file needed changing — the change set stayed as listed. No bare `npx` was
invoked and `npm run lint` was not run and is never ordered here.

`tests/orchestration/` and `tests/cli/` were correctly NOT run in full, for the reason
the block gives and which I verified rather than assumed: the only `.py` file this
round changed is `tests/ui_contracts/test_digest_hero_card.py`. The full changed-file
list for `fcde1983..HEAD` is the five `.agent/` paths, `docs/roadmap/features/T2_F272.md`,
the two `.ts` modules and that one test file.

### G7 LINT AND INTEGRITY, at C5 — exit 0 and exit 0

    python3 -m ruff check tests/ui_contracts/test_digest_hero_card.py
    EXIT = 0 — All checks passed!

ONE invocation over exactly the `.py` files this round changed, which is that file and
nothing else. EXIT 0, so the `--stdin-filename` pre-existing-diagnostic route was not
needed.

    python3 -m apps.cli.grouped integrity check --json
    EXIT = 0 — "passed": true, "fail_count": 0, over 5 checks

### G8 THE TREE — exit 0

- `git status --porcelain` EMPTY when C7 is staged.
- `git ls-files .remedy-wt` EMPTY.
- `git worktree list`: TWO worktrees were created and each removed BY EXACT PATH and
  pruned — `/home/decodeux/Repos/remedy/.remedy-wt/f272-r12-g4` and
  `/home/decodeux/Repos/remedy/.remedy-wt/f272-r12-g5`. Never by glob. Only the twelve
  pre-existing `remedy/job-*` entries remain, exactly as at session start. The SIX
  scratch paths I wrote under `.remedy-wt/` were deleted BY EXACT PATH:
  `r12_slices.py`, `r12_c2.py`, `r12_g4iii.py`, `r12_g5.py` and the two `__pycache__`
  entries `r12_c2.cpython-310.pyc` and `r12_slices.cpython-310.pyc`. The reviewer's own
  `.remedy-wt/f272-r12-block.md` was left where it is. See Deviation 3 on why a glob
  would have been a disaster here.
- Per-commit insertions from `git diff --numstat <parent> <commit>`, each
  single-parent, each under the DECISION F104 D1 cap of 500, each matching the
  `## Commits` table above cell for cell:

| commit | item | parents | `+` | `-` | ≤500 | matches `## Commits` |
|---|---|---|---|---|---|---|
| `d1bb92a9` | C0a | 1 | 395 | 0 | yes | yes |
| `f929564d` | C0b | 1 | 276 | 244 | yes | yes |
| `b3a8644e` | C1 | 1 | 12 | 10 | yes | yes |
| `879504f7` | C2 | 1 | 8 | 0 | yes | yes (2 rows, +4/-0 each) |
| `64bed56f` | C3 | 1 | 47 | 0 | yes | yes |
| `a39dfe52` | C4 | 1 | 3 | 3 | yes | yes |
| `dd51f8a6` | C5 | 1 | 18 | 6 | yes | yes (2 rows, +13/-4 and +5/-2) |
| `2868d924` | C6 | 1 | 2 | 0 | yes | yes |

C7 is excluded by §3 item 14: it cannot count its own insertions.

- Marker sweep, counted by me, LINES beginning `<<<BEGIN ` or `<<<END ` in every
  written non-block file: `.agent/plan.md` 0, `.agent/live_review.md` 0,
  `.agent/prose_slips.md` 0, `docs/roadmap/features/T2_F272.md` 0,
  `tests/ui_contracts/test_digest_hero_card.py` 0,
  `apps/ui/src/api/digestVisibility.ts` 0, `apps/ui/src/api/digestCardCopy.ts` 0.
  See Deviation 2 on the non-anchored substrings the ledger already carried.

- The three `.agent/STOP` readings of constraint 8, each by `os.path.exists`:

| when | `.agent/STOP` exists |
|---|---|
| before C0a | False |
| before C5 | False |
| before C7 | False |

## External actions

| action | outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f272-r12-g4 a39dfe52` | created at `a39dfe52` |
| `git worktree remove --force .remedy-wt/f272-r12-g4` | removed by exact path |
| `git worktree prune` | run after that removal |
| `git worktree add --detach .remedy-wt/f272-r12-g5 dd51f8a6` | created at `dd51f8a6` |
| `git worktree remove --force .remedy-wt/f272-r12-g5` | removed by exact path |
| `git worktree prune` | run after that removal |
| `git push -u origin feature/f272-one-world-completion` | see below |

No PR created, none merged, nothing force-pushed, no branch deleted.

## Authored-text proofs

Disk-to-disk against the COMMITTED `.agent/authored/f272-r12.md`, both sides read back
out of git rather than from my working tree:

| slice | target | bytes | mode | result | sha256 |
|---|---|---|---|---|---|
| PLANF272R12 | `.agent/plan.md` | 2284 | replace | IDENTICAL | `6835d956e384…` |
| RECORDR12 | `.agent/live_review.md` | 5321 | append | IDENTICAL | `7c79ef8f7688…` |
| SLIPSR12 | `.agent/prose_slips.md` | 1502 | append | IDENTICAL | `fc18b45c7283…` |
| DECISIONR12 | `docs/roadmap/features/T2_F272.md` | 2979 | append | IDENTICAL | `fde21e28f690…` |

All four slices were applied byte for byte, none was edited, and no `<<<BEGIN`/`<<<END`
marker LINE reached any target file. C4, C5 and C6 were a SPEC and not a slice; I wrote
that code myself.

## Deviations & assumptions

NO COMMIT WAS MADE BEYOND THE BLOCK'S ORDERED SEQUENCE, AND NONE WAS DROPPED OR
REORDERED. Per the fix clause OPEN in the record and binding on this handback: any
commit beyond the ordered sequence receives its OWN `## Commits` row and its OWN
item-status row, and the Deviations section says so in those same words. There is no
such commit — the range `fcde1983..HEAD` holds exactly eight commits before this
handoff and they are C0a, C0b, C1, C2, C3, C4, C5 and C6 in that order, C4 landing
BEFORE C5 as constraint 3 requires.

### Deviation 1 — my first reader (b) was wrong, and the C2 append was written twice

Reader (b) splits the whole image on `\n{2,}`. My first implementation compared the
pre-image's units against the post-image's units WITHOUT normalising them, and it
rejected a correct append: the pre-image's own terminal `\n` is a lone newline at the
end of `pre`, but once the append lands that same newline is the first half of the
`\n\n` separator, so the last pre-unit loses a trailing byte in the post-image and the
prefix comparison failed on a difference that is a property of the SPLITTER and not of
the disk. The negative control was uninformative in that state — reader (b) was
rejecting everything, including the restore — which is precisely how I noticed.

I did NOT commit and then fix. I reverted both files with
`git checkout -- .agent/live_review.md .agent/prose_slips.md`, confirmed
`git status --porcelain` empty, corrected the reader to strip trailing newlines per
unit with the reason written into the code as a comment, and re-ran the whole of C2
from the clean pre-image. The committed C2 is therefore a single clean append, and
every G2 number above was measured by the corrected reader. Declared because a reader
auditing this round should know one gate was authored wrong before it was authored
right, even though no wrong byte ever reached a commit.

### Deviation 2 — `.agent/live_review.md` already carried `<<<BEGIN`/`<<<END` substrings

My first marker sweep counted SUBSTRINGS and read `BEGIN=1 END=3` in
`.agent/live_review.md`, which looked like a transport leak. It is not one. Measured at
`fcde1983`, BEFORE this round wrote anything, that file already carried those counts:
they are earlier findings QUOTING the marker syntax inside prose, mid-line, and not one
of them starts a line. Line-anchored, the count is **0 before and 0 after**, and both
RECORDR12 and SLIPSR12 contribute 0 of either form. The sweep reported under G8 is the
line-anchored one, which is what "marker LINES never reach a target file" actually
means.

### Deviation 3 — the scratch cleanup was by exact path, and a glob would have been a disaster

`.remedy-wt/` holds 42 pre-existing files matching `r12_*` — `r12_g8.py`,
`r12_gates.py`, `r12_vitest.config.mjs` and so on — left by the round-12 sessions of
OTHER features. I removed only my own six paths, named individually. An
`rm .remedy-wt/r12_*` would have destroyed all 42. Recording it because this is the
first round in this feature where the never-delete-by-glob rule had a live blast radius
rather than a hypothetical one.

### Deviation 4 — no `node_modules` was copied into either worktree, and none was needed

Constraint 7 requires `shutil.copytree(..., symlinks=True)` for any VITEST run inside a
worktree. Neither destructive check this round runs vitest: G4(iii) and G5(ii) are both
pytest-only, over files read from disk as TEXT, so both worktrees ran without
`node_modules` at all. The one vitest gate, G6, ran in the PRIMARY checkout exactly as
the block orders. No `copytree` was therefore invoked, and this is a deviation from the
letter of round 11's route and not from constraint 7, whose condition never triggered.

### Deviation 5 — C5 wrote `SETTLED_STATES` multi-line, which the block implies but does not say

The block's G5(ii) counts the byte string `  "blocked",\n` — two leading spaces, a
trailing newline — and requires it to occur exactly once. That string can only exist in
a MULTI-LINE array, so C5 reformatted `SETTLED_STATES` from its one-line form into six
indented entries. I confirmed first that nothing depends on the old shape: the contract
test reads `f'"{state}"' not in code` over the whole file, so formatting is free to it,
and G6's vitest and tsc node passed afterwards. The comment above it gained a sentence
naming DECISION F272 D8 as the reason both states are settled, rather than only losing
its "four".

### Deviation 6 — the copy audit was re-measured at this tree and refused neither label

The block permits `"Blocked"` and `"Stopped"` "unless the audit refuses them at this
tree". I parsed `scrubUiText`'s `forbidden` list out of `humanCopy.ts` at `fcde1983`:
it holds 17 entries, `rank` through `traceback`, and neither `blocked` nor `stopped` nor
either capitalised form is among them. `"Blocked"` DOES occur as a literal in
`humanCopy.ts` — it is the CHECKLIST vocabulary's label for its own `blocked`, which is
the exact trap `digestCardCopy.ts`'s own comment warns about, and it constrains nothing
here because the two maps are different vocabularies. Both labels were used as
authorised.

### Assumption

None load-bearing. Every claim above is a measurement I took in this round, and each
names the tree it was taken in.

## Next

REVIEW THIS ROUND AND, ON PASS, REPLACE C6's `Landed: R-0821` LINE WITH THE AUTHORED
`Done: R-0821` RESOLUTION — that is the one thing this round is forbidden to write for
itself, and a surviving `Landed:` line is an unreviewed fix by construction. R-0821's
counter-measure survives its resolution: a block changing a state vocabulary names
`tests/ui_contracts/` in its gate list.

Then move three of DECISION F272 D6 — retype `JobPlan.state` to `RunState`, make the
six `JOB_*` constants `RunState` members, `.value` at every boundary leaving the record
— with `tests/orchestration/test_job_state_field.py` as the rendering guard that move
must keep green, D7's probe as the method for finding its site set, and
`tests/ui_contracts/` in the gate list. Phase 1 rule 1 (`.agent/STOP`) is checked
before Phase 1 rule 2, as always.
