# Handoff — F272 One world completion, round 11

## Session

SESSION 6 of feature F272 · round 11 · rounds so far 11

Context self-assessment (amend0905-throughput): context is comfortable — this round
read two TypeScript modules and four test files, ran short suites only, and wrote no
production code, so a further round in this session is affordable.

THE ROUND STOPPED AT C4 ON THE CONDITION THE BLOCK ITSELF NAMES. C0a through C3
landed in the ordered sequence. C4 was NOT committed and C5 was NOT written, because
`tests/ui_contracts/` — this round's gate, which the block forbids editing — CANNOT
reach EXIT 0 with C4 applied: a THIRD test in that directory pins the label map at
exactly seven entries and goes red the moment the two new ones are added. That is
measured, not predicted, and the measurement is below. The block says in its own
words: "If a test there cannot pass without being changed, STOP and hand off — that
is a finding about this block, not a licence to edit the gate." So I stopped.

## Range

Review of `1bfb1cd9`..`HEAD` (branch `feature/f272-one-world-completion`).

## Commits

### 3599cfd9 f272: save the round 11 step block as authored text
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f272-r11.md` | +363 / -0 | C0a, `shutil.copyfile` of the reviewer's scratch original |

### dee60fac f272: mirror the round 11 step block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +277 / -314 | C0b, byte copy of the same original |

### 1a2c0017 f272: set the plan to the round 11 cockpit state step
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +16 / -17 | C1, replaced by the PLANF272R11 slice |

### 6373dc0e f272: book the round 10 PASS verdict, register R-0821 and three prose slips
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4 / -0 | C2, RECORDR11 appended |
| `.agent/prose_slips.md` | +6 / -0 | C2, SLIPSR11 appended |

### 35f50db8 f272: rule blocked and stopped as settled cockpit states in DECISION F272 D8
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T2_F272.md` | +45 / -0 | C3, DECISIONR11 appended |

### C6 — this handoff
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | self-referential | C6 cannot table the commit that writes it (R-0149 pattern) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | `.agent/authored/f272-r11.md`, byte copy, digest verified before any other action |
| C0b | done | `.agent/last_block.md`, byte copy of the same original |
| C1 | done | plan replaced by the PLANF272R11 slice, byte-equal; its prose is now stale — Deviation 2 |
| C2 | done | RECORDR11 and SLIPSR11 appended; every ordered count matched exactly |
| C3 | done | DECISION F272 D8 appended; headings read D1..D8 in order |
| C4 | skipped | NOT COMMITTED. Its gate `tests/ui_contracts/` cannot reach EXIT 0 without an edit to `tests/ui_contracts/test_digest_hero_card.py`, which the block forbids. Measured in a disposable worktree; see G4 |
| C5 | skipped | a `Landed: R-0821` line would be false — C4 did not land. Constraint 6 leaves me no wording for "attempted", and inventing one is not mine to do |
| C6 | done | this handoff |

No commit exists outside this ordered sequence; the range holds exactly five commits
before this handoff and they are C0a, C0b, C1, C2 and C3 in that order.

## Verification

One line per gate with its REAL exit code, then the transcripts. "Green" as a word
appears nowhere; where a gate is red or unreachable it says so and says why.

| Gate | Exit | Reading |
|---|---|---|
| G1 TRANSPORT | 0 | three artefacts, all 32960 bytes / 363 lines, all sha256 `6575c005…5be9d1d3` |
| G2 THE RECORD | 0 | readers (a)(b)(c)(d) accept over both files; all six ordered counts matched |
| G3 PLAN + FEATURE FILE | 0 | plan byte-equal at 2187 B / 42 lines; feature file readers accept; D1..D8 |
| G4 THE TWO RED TESTS | **1** | UNREACHABLE AS ORDERED. C4 fixes both ordered tests and reddens a third. The red control, the label reading and the two-file run all pass — see below |
| G5 VITEST | 0 | `52 passed`, in the primary checkout AND, separately, in a worktree with C4 applied |
| G6 THE SUITES | 0 and 0 | `tests/docs/` 303, canary 42, both matching base |
| G7 LINT AND INTEGRITY | n/a and 0 | ruff's ordered file set is EMPTY — no `.py` file changed; integrity EXIT 0 |
| G8 THE TREE | 0 | tree empty, `git ls-files .remedy-wt` empty, the one worktree removed by exact path |

### G1 TRANSPORT — a real three-artefact chain

Per §3 item 37 this covers the saved copy and its mirror, not the bytes emitted into
my prompt.

| Artefact | Bytes | Lines | sha256 |
|---|---|---|---|
| `.remedy-wt/f272-r11-block.md` (reviewer's surviving original) | 32960 | 363 | `6575c005b2b8bfca32818ff20c24122921aa205a86858f310b3860f75be9d1d3` |
| `.agent/authored/f272-r11.md` at HEAD (C0a) | 32960 | 363 | same |
| `.agent/last_block.md` at HEAD (C0b) | 32960 | 363 | same |

All three equal each other and equal the delegation's BLOCK_SHA, BLOCK_LENGTH and
BLOCK_LINES. Verified BEFORE any other action was taken, and re-read from the
COMMITTED blobs afterwards.

### G2 THE RECORD at C2 — exit 0

`.agent/live_review.md` ← RECORDR11, readers (a) to (d):

- (a) BYTE: pre 1118077 → post 1127168; pre a byte-exact prefix; `post == pre + b"\n" +
  slice` TRUE; pre's terminal byte asserted to be exactly one `\n` BEFORE writing;
  post ends in exactly one `\n`. Slice 9090 bytes, sha256 `caed60c3f12d…`.
- (b) STRUCTURAL, computed independently of (a) by splitting the WHOLE image on
  `\n{2,}`: N counted by my script from the slice's own paragraphs = 2; units 701 →
  703, delta 2; the last 2 units equal the slice's paragraphs in order; the units
  before are an unchanged prefix.
- (c) NEGATIVE CONTROL, in memory on a `bytes` object, never on disk: offset 1118098
  asserted to lie inside the FIRST appended paragraph, one bit flipped — reader (a)
  rejected AND reader (b) rejected; restored, both accepted, and the restored image
  equalled the disk image.
- (d) COUNTS before → after C2, every one exactly as ordered:

| reading | ordered | measured |
|---|---|---|
| `^- R-\d{4} — ` distinct ids | 304 → 305 | 304 → 305 |
| `^Done: R-\d{4} — ` distinct | 247 → 247 | 247 → 247 |
| open set BY DISTINCT ID | 57 → 58 | 57 → 58 |
| `^Gate: ` | 32 → 33 | 32 → 33 |
| `^Gate: F272 R10 ` | 0 → 1 | 0 → 1 |
| `^- R-0821 — ` | 0 → 1 | 0 → 1 |

AFTER C5 the block orders `^Landed: R-0821 ` 0 → 1. C5 did not happen, so the
measured reading is 0 → **0**, and `^Done: R-0821 ` is 0, as it must be.

`.agent/prose_slips.md` ← SLIPSR11, readers (a) and (b) and the same negative
control: pre 136942 → post 139621; prefix, append arithmetic and terminal newline all
TRUE; N counted 3, units 174 → 177, last 3 units equal the slice's paragraphs in
order; the control's flip at offset 136963 was rejected by both readers and the
restore equalled the disk image. Slice 2678 bytes, sha256 `2b6ac0dd5af6…`.

### G3 THE PLAN at C1, AND THE FEATURE FILE at C3 — exit 0

Plan: `.agent/plan.md` equals the PLANF272R11 slice bytes exactly. Both byte lengths
2187. 42 lines against the AGENTS.md cap of 50. `## Goal` present, `## Next Steps`
present.

Feature file: readers (a) and (b), no negative control (gate budget). Pre 30008 →
post 32918; prefix, append arithmetic and terminal newline all TRUE; N counted 7,
units 63 → 70, last 7 units equal the slice's paragraphs in order. Lines matching
`^### DECISION F272 D\d+ ` counted by me: 7 before, 8 after, naming in order
D1 D2 D3 D4 D5 D6 D7 D8.

### G4 THE TWO RED TESTS — the gate the round could not reach, measured five ways

ALL OF G4 RAN IN THE DISPOSABLE WORKTREE `.remedy-wt/f272-r11-probe` AT `1bfb1cd9`,
never in the primary checkout, and C4 was never committed. `node_modules` and
`apps/ui/node_modules` were restored into it with `shutil.copytree(..., symlinks=True)`
— the argument, not the default, per R-0591 and constraint 7.

**THE BASE, in the primary checkout, unmodified:**

    python3 -B -m pytest tests/ui_contracts/ -q -p no:randomly
    EXIT = 1 — 2 failed, 807 passed, 4 skipped in 6.77s

exactly the three numbers the block names. The worktree reads 806 passed / 5 skipped
for the same two failures — one further skip inside a worktree — so every comparison
below is worktree-against-worktree.

**THE FIVE MEASUREMENTS.** C4 was written to the letter of the spec: `"blocked"` and
`"stopped"` appended to `SETTLED_STATES`, the two counting comments rewritten to name
the set instead of counting it, and `"blocked": "Blocked"` and `"stopped": "Stopped"`
appended to `DIGEST_STATE_LABELS` with its "seven" comment rewritten.

| # | tree | exit | summary | the tests that failed |
|---|---|---|---|---|
| M1 | control, C4 absent | 1 | 2 failed, 806 passed, 5 skipped | the two the block names |
| M2 | BOTH modules edited | **1** | 1 failed, 807 passed, 5 skipped | `test_digest_hero_card.py::TestNoRuleHasASecondHome::test_no_run_state_phrase_is_restated_as_a_literal` |
| M3 | `digestVisibility.ts` ONLY | 1 | 1 failed, 807 passed, 5 skipped | the copy one only — this half introduces NO new red |
| M4 | `digestCardCopy.ts` ONLY | 1 | 2 failed, 806 passed, 5 skipped | the contract one, plus the hero-card one — this half is the whole cause |
| M5 | both modules + `== 7` → `>= 7` in the gate file | **0** | 808 passed, 5 skipped | none |

**WHY THE THIRD TEST GOES RED.** `tests/ui_contracts/test_digest_hero_card.py:230`,
inside `TestNoRuleHasASecondHome`, is a vacuity guard on its own parser:

    phrases = digest_state_phrases()
    assert len(phrases) == 7, (...)

`digest_state_phrases()` parses `DIGEST_STATE_LABELS` out of `digestCardCopy.ts`. Two
new entries make it 9, and the guard is written as an EQUALITY where its own docstring
("a reader that returns almost nothing would make the loop below vacuous") wants a
FLOOR. It is the same defect class as R-0821 itself — a hard-coded seven that goes
stale the day the enum widens — one layer further out, and it is invisible until the
fix for R-0821 lands. The assertion it guards (`restated == []`, no state phrase
restated as a literal in `DigestHeroCard.tsx`) still holds for all nine phrases: M5
shows the whole suite at EXIT 0 once the constant is a floor.

There is no honest C4 that avoids it. Any two entries make the count 9; the only ways
round it are to not add them (leaving the ordered test red), to hide them from the
parser with computed keys (gaming a guard), or to edit the gate (forbidden here). So
G4(i) is UNREACHABLE inside this block's change set, and I stopped rather than
committing a change whose gate is red or widening the change set to route around it.

**G4(ii) THE RED CONTROL — the gate can still fail, and was shown to fail.** Run with
C4 applied in the worktree. The byte string `  "blocked",\n` occurs exactly 1 time in
`digestVisibility.ts` (§3 item 25). Removed it, file sha256 `4808d86a…dfe2bc1d` before:

    python3 -B -m pytest tests/ui_contracts/test_job_digest_card_contract.py -q -p no:randomly
    EXIT = 1 — 1 failed, 28 passed in 0.25s
    E  AssertionError: ['blocked'] appear in RunState but not in digestVisibility.ts, …

The failure names `blocked` and nothing else. Restored: sha256 back to
`4808d86a…dfe2bc1d`, byte-identical, and the re-run reads EXIT 0 at 29 passed.

**G4(iii) WHAT A READER OF THE CARD ACTUALLY SEES**, parsed out of the module rather
than inferred from the test names, with C4 applied:

| call | answer | is `UNREADABLE_STATE_LABEL` |
|---|---|---|
| `digestStateLabel("blocked")` | `"Blocked"` | False |
| `digestStateLabel("stopped")` | `"Stopped"` | False |

`UNREADABLE_STATE_LABEL` is still `"State not recorded"`, unchanged. The label map
carries nine keys, in `RunState` declaration order; `SETTLED_STATES` reads `paused,
completed, failed, cancelled, blocked, stopped`.

**THE TWO ORDERED FILES ALONE, with C4 applied:**

    python3 -B -m pytest tests/ui_contracts/test_digest_card_copy.py \
        tests/ui_contracts/test_job_digest_card_contract.py -q -p no:randomly
    EXIT = 0 — 52 passed in 0.29s

52 passed is exactly the reading the reviewer's bisection took at `b5cde726`, the
commit before round 8 widened the enum. C4 restores those two files to their
pre-round-8 state precisely.

### G5 VITEST — exit 0, twice

    python3 -B -m pytest tests/orchestration/test_test_runner.py -q -p no:randomly
    PRIMARY CHECKOUT, at the commit handed back:  EXIT = 0 — 52 passed in 5.87s
    WORKTREE WITH C4 APPLIED:                     EXIT = 0 — 52 passed in 3.54s

The second run is the one that matters and was the reason for the `copytree`: it is
this repository's own route to `npx vitest run` over the whole UI suite, so it gates
all three `.test.ts` files that import the modules C4 edits. No bare `npx` was
invoked. C4 is vitest-safe: `digestVisibility.test.ts` and `digestCardCopy.test.ts`
each hold a seven-row state table, but each asserts only that ITS OWN table lists
those seven — neither compares itself to `RunState` — so widening the modules moves
nothing there.

### G6 THE SUITES — run SERIALLY, each its own invocation

| invocation | exit | summary line | base at `1bfb1cd9` |
|---|---|---|---|
| `tests/docs/` | 0 | `303 passed in 0.49s` | 303 |
| `tests/cli/test_golden_path.py` (THE CANARY) | 0 | `42 passed in 20.98s` | 42 |

`tests/orchestration/` and `tests/cli/` were correctly NOT run in full, for the reason
the block gives: no `.py` file changed this round, and G5 already runs the one
orchestration node this change could reach. The whole change set is four `.agent/`
files and one `docs/` file.

### G7 LINT AND INTEGRITY — an empty ruff set, stated rather than passed

The `.py` files this round changed: NONE. The full changed-file list for
`1bfb1cd9..HEAD` is `.agent/authored/f272-r11.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md`, `.agent/prose_slips.md` and
`docs/roadmap/features/T2_F272.md`. So ruff's ordered file set is EMPTY and ruff was
not run: an empty invocation would report a pass that measured nothing. `npm run
lint` was not run and is never ordered in this repository.

`python3 -m apps.cli.grouped integrity check --json`: EXIT 0, `"passed": true`,
`"fail_count": 0`, over 5 checks.

### G8 THE TREE — exit 0

- `git status --porcelain` EMPTY when C6 is staged.
- `git ls-files .remedy-wt` EMPTY.
- `git worktree list`: ONE worktree was created and removed BY EXACT PATH and pruned —
  `/home/decodeux/Repos/remedy/.remedy-wt/f272-r11-probe`. Never by glob. Only the
  twelve pre-existing `remedy/job-*` entries remain, exactly as before. The FOUR
  scratch files I wrote under `.remedy-wt/` were deleted by exact path, never by
  glob: `r11_c2.py`, `r11_c3.py`, `r11_c4_probe.py` and `r11_g8.py`. The reviewer's
  own `.remedy-wt/f272-r11-block.md` was left where it is.
- Per-commit insertions from `git diff --numstat <parent> <commit>`, each
  single-parent, each under the DECISION F104 D1 cap of 500, each matching the
  `## Commits` table above cell for cell:

| commit | item | parents | `+` | `-` | ≤500 | matches `## Commits` |
|---|---|---|---|---|---|---|
| `3599cfd9` | C0a | 1 | 363 | 0 | yes | yes |
| `dee60fac` | C0b | 1 | 277 | 314 | yes | yes |
| `1a2c0017` | C1 | 1 | 16 | 17 | yes | yes |
| `6373dc0e` | C2 | 1 | 10 | 0 | yes | yes (2 rows) |
| `35f50db8` | C3 | 1 | 45 | 0 | yes | yes |

C6 is excluded by §3 item 14: it cannot count its own insertions. C4 and C5 have no
row because they were not committed.

- Marker sweep, counted by me, lines beginning `<<<BEGIN ` or `<<<END ` in every
  written non-block file: `.agent/plan.md` 0, `.agent/live_review.md` 0,
  `.agent/prose_slips.md` 0, `docs/roadmap/features/T2_F272.md` 0.

- The three `.agent/STOP` readings of constraint 8, each by `os.path.exists`:

| when | `.agent/STOP` exists |
|---|---|
| before C0a | False |
| before C4 | False |
| before C6 | False |

## External actions

| action | outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f272-r11-probe 1bfb1cd9` | created at `1bfb1cd9` |
| `git worktree remove --force .remedy-wt/f272-r11-probe` | removed by exact path |
| `git worktree prune` | run after the removal |
| `git push -u origin feature/f272-one-world-completion` | see below |

No PR created, none merged, nothing force-pushed, no branch deleted.

## Authored-text proofs

Disk-to-disk against the committed `.agent/authored/f272-r11.md`:

| slice | target | bytes | mode | result | sha256 |
|---|---|---|---|---|---|
| PLANF272R11 | `.agent/plan.md` | 2187 | replace | IDENTICAL | `3682beb3c561…` |
| RECORDR11 | `.agent/live_review.md` | 9090 | append | IDENTICAL | `caed60c3f12d…` |
| SLIPSR11 | `.agent/prose_slips.md` | 2678 | append | IDENTICAL | `2b6ac0dd5af6…` |
| DECISIONR11 | `docs/roadmap/features/T2_F272.md` | 2909 | append | IDENTICAL | `437bdbcbb405…` |

All four slices were applied byte for byte, none was edited, and no
`<<<BEGIN`/`<<<END` marker LINE reached any target file. C4 and C5 were a SPEC and not
a slice, and neither was committed.

## Deviations & assumptions

TWO COMMITS OF THE ORDERED SEQUENCE WERE NOT MADE, AND NO COMMIT WAS MADE BEYOND IT.
Per the fix clause OPEN in the record and binding on this handback: any commit beyond
the ordered sequence receives its OWN `## Commits` row and its OWN item-status row,
and the Deviations section says so in those same words. There is no such commit — the
range `1bfb1cd9..HEAD` holds exactly five commits before this handoff, they are C0a,
C0b, C1, C2 and C3 in that order, and the departure runs the other way: C4 and C5 are
ABSENT, each with its own item-status row saying so.

### Deviation 1 — C4 and C5 were not committed, on the block's own STOP condition

Stated in full under G4. In one sentence: the ordered gate `tests/ui_contracts/`
cannot read EXIT 0 with C4 applied, because a third test in that directory pins
`len(phrases) == 7` over the very map C4 widens, and the block forbids editing that
directory. I applied C4 in a disposable worktree, measured it five ways, proved the
red control fires, proved vitest unaffected, proved the two ordered tests go green and
the third goes red, then discarded it. C5's `Landed:` line would have asserted a fix
that is not on the branch, so it was not written.

WHAT THE NEXT ROUND NEEDS, so this costs one small round and not a session: land C4
exactly as measured, and change ONE character in
`tests/ui_contracts/test_digest_hero_card.py:230` from `== 7` to `>= 7` (or, better,
to a comparison against `run_state_values()`, which that file does not yet import).
M5 shows that combination at EXIT 0, 808 passed, 5 skipped. Whether the gate file may
be edited is a ruling for the reviewer, not a call for me: it is the same edit R-0821
already argues for one layer in, and refusing it leaves the cockpit unable to name two
states the orchestrator really produces.

### Deviation 2 — the plan and the record now describe a fix that did not land

Constraint 1 is absolute — "if one looks wrong, apply it anyway and say so" — so all
four slices went in byte for byte, and two of them now overstate what is on disk:

- `.agent/plan.md` (C1) says "This round gives them their place", and the round did
  not.
- `.agent/live_review.md` (C2), inside R-0821, says "FIX, LANDED BY THIS ROUND:
  `blocked` and `stopped` join `SETTLED_STATES` and gain `DIGEST_STATE_LABELS`
  entries". They do not yet. Everything else in that registration — the bisection, the
  two module readings, the product effect, the counter-measure — is accurate and was
  independently reproduced by me at base.
- `docs/roadmap/features/T2_F272.md` (C3) states DECISION F272 D8. A DECISION is a
  RULING and the ruling stands on its own; but its REVERSE clause ("REVERSE by
  removing the two entries from each module") names entries that do not exist yet.

I did not edit a single byte of any of them. Correcting them is the reviewer's, and
the cheapest correction is the next round landing C4, after which all three read true.

### Deviation 3 — the block's G4 gate was run in a worktree, and C4 lives nowhere now

The block places G4(ii) in a disposable worktree at "the commit C4 creates". There is
no such commit, so the whole of G4 ran in a worktree at `1bfb1cd9` with C4 applied to
the working tree and never committed. The primary checkout never carried the edit;
`git status --porcelain` was empty at every point after C3. The exact C4 text is not
preserved anywhere on the branch — it is reproducible from the spec in
`.agent/authored/f272-r11.md`, and the shape it took is recorded under G4(iii) above:
`SETTLED_STATES` gains `"blocked"` and `"stopped"` as a six-element multi-line array,
`DIGEST_STATE_LABELS` gains `"blocked": "Blocked"` and `"stopped": "Stopped"` in
`RunState` declaration order, and the two comments that counted the partition — "the
most report-worthy rest of the four" and "The seven members of `RunState`" — were
rewritten to name the set instead, per the block's preference for naming over
counting.

### Deviation 4 — `node_modules` was copied into the worktree, 305 MB

Constraint 7's route, taken as written: `shutil.copytree(..., symlinks=True)` for both
`node_modules` and `apps/ui/node_modules`, rather than round 10's symlink. It is what
made the C4 vitest run possible at all, and it is also why the worktree's
`tests/ui_contracts/` reading is 5 skipped where the primary reads 4 — the extra skip
is not the `tsc` node, which ran. The whole worktree was removed by exact path.

### Deviation 5 — the labels were chosen without needing the copy audit's permission

The block says use `"Blocked"` and `"Stopped"` unless the copy audit refuses them. It
did not refuse: `scrubUiText`'s forbidden-word list, parsed out of `humanCopy.ts`,
holds neither word, both are short capitalised phrases in the voice of `"Paused"` and
`"Cancelled"`, and both are distinct from every existing phrase, which
`digestCardCopy.test.ts` requires. They also collide with nothing in
`DIGEST_CTA_RULE_IDS`, which I did not touch: `"blocked-failed"` does not contain the
literal `"blocked"` including its closing quote, which is exactly why the ordered test
was failing rather than passing by accident.

### Assumption

None load-bearing. Every claim above is a measurement I took in this round, and each
names the tree it was taken in.

## Next

RULE ON C4's BLOCKER, which is the one thing this round could not decide for itself:
may `tests/ui_contracts/test_digest_hero_card.py:230` change `len(phrases) == 7` to a
floor, so that the R-0821 fix can land? Everything else is measured and ready — M5 in
the table above is the whole answer at EXIT 0, 808 passed, 5 skipped. The next block
can be small: C4 as specified, that one-character gate repair, C5's `Landed:` line,
and the handback. Then move three of DECISION F272 D6 — retype `JobPlan.state` to
`RunState`, make the six `JOB_*` constants members, `.value` at every boundary leaving
the record — with `tests/ui_contracts/` in its gate list, which R-0821's
counter-measure now makes binding on exactly that round. Phase 1 rule 1
(`.agent/STOP`) is checked before Phase 1 rule 2, as always.
