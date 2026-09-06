# Handoff — F260 One world · round 18 · F272 registered directly after its parent

## Session

SESSION 7 of feature F260 · round 18 · rounds so far 18

`.agent/STOP` did NOT exist at the start of this round (`ls .agent/STOP` → "No
such file or directory"), was re-checked after C3 and before this handback, and
still does not exist.

Context self-assessment (amend0905-throughput): context was never a constraint
this round — five small commits, one of them the atomic registration over ten
paths, and the whole gate set ran in about 22 seconds of suite time, almost all
of it the canary.

**THIS SESSION IS AT THE SOFT LIMIT** (25 rounds or 7 sessions, whichever first;
this is session 7). This round is the SECOND HALF of the standing
amend0905-throughput default: round 17 RULED the split as DECISION F260 D8, and
this round APPLIES it. F272 — the one-world completion — is now registered, with
its STATUS line sitting immediately after F260's inside the same
`## Tier 2 — Vocabulary & Concept Block` heading, so Rule A5 proposes it before
any other unchecked feature, exactly as operator order amend0906-split-placement
requires. `docs/roadmap/STATUS.md`, `README.md`, the `TOTAL_FEATURES` pin, the new
detail file and the six downstream "Depends on" lines all moved in ONE commit; no
committed state of this branch has the README and the ledger disagreeing.

## Range

Review of `7a1ce69d594043dfaad6c69161c93613d4229821`..`HEAD`.

FIVE commits plus this handback. ALL FIVE are single-parent. They are EXACTLY the
bundle's ordered sequence C0a → C0b → C1 → C2 → C3 → C4, with nothing added,
dropped or reordered. Largest insertion count 399 (`.agent/authored/f260-r18.md`,
a single `.agent/**` state write); nothing approached the 500-insertion cap.

## Commits

`+/-` taken from `git log --numstat`, never re-derived by eye.

### b28b451e — f260: save the round 18 block verbatim as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f260-r18.md | +399 / -0 | C0a — `shutil.copyfile` from `.remedy-wt/f260-r18-block.md`, proved by `filecmp.cmp(shallow=False)` = True and sha256 equal to the delegation digest BEFORE staging |

### c4ab0416 — f260: mirror the round 18 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +337 / -262 | C0b — same source file, same `shutil.copyfile` route, same two proofs |

### e788caf0 — f260: set the plan to round 18, the follow-up registration
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +23 / -25 | C1 — whole-file replacement by the PLAN slice plus exactly one trailing newline; 1820 bytes, 38 lines, under the 50-line cap, carrying `## Goal` and `## Next Steps` |

### 13a0c3a9 — f260: book the round 17 gate record and the reviewer slip
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | C2, written FIRST — GATE_R17 appended by the recipe derived from this file's own measured terminal byte (one newline); 959115 → 964554 bytes |
| .agent/prose_slips.md | +2 / -0 | C2, written SECOND — SLIP24 appended, its own recipe derived from its own measured terminal byte (one newline); 122752 → 123846 bytes |

### 189d055d — f260: register F272, the one-world completion follow-up, directly after its parent
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F272.md | +108 / -0 | C3 — NEW FILE, the F272FILE slice plus exactly one trailing newline, written with `open(...,"wb")` and never by copying another feature file; 6852 bytes |
| docs/roadmap/STATUS.md | +1 / -0 | C3 — STATUSPAIR; the FROM spanned F260's line AND F261's, so the new line provably lands between them, inside the Tier 2 heading |
| README.md | +2 / -2 | C3 — READMECOUNT (271 → 272) and READMETIER (Tier 2 total 24 → 25; the Done column does not move, F272 being unchecked and F260 still `[~]`) |
| tests/docs/test_docs_consistency.py | +7 / -2 | C3 — PINPAIR; `TOTAL_FEATURES` 271 → 272 with the narrating comment block above it extended in the same commit |
| docs/roadmap/features/T2_F261.md | +1 / -1 | C3 — GENPAIR, the placeholder clause replaced by the concrete id |
| docs/roadmap/features/T2_F268.md | +1 / -1 | C3 — GENPAIR |
| docs/roadmap/features/T2_F269.md | +1 / -1 | C3 — GENPAIR |
| docs/roadmap/features/T2_F270.md | +1 / -1 | C3 — GENPAIR |
| docs/roadmap/features/T2_F271.md | +1 / -1 | C3 — GENPAIR |
| docs/roadmap/features/T2_F263.md | +1 / -1 | C3 — F263PAIR, the sixth dependent, which the operator's amend0906 commit did not reach |

### C4 — this file
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4 — a handback cannot table the commit that writes it (R-0149 pattern; constraint 8). No gate reading was taken after this file existed; the reviewer measures C4's own numbers at the next gate |

## External actions

| Command | Outcome |
|---|---|
| `sha256sum .remedy-wt/f260-r18-block.md` | exit 0; `657022416f31310536a64d78d191c5aa264184258399aa9f1cd10f8f6d9e62b1` — equals the digest the delegation names |
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | exit 0; `[]` — NO open PR. No new branch was created this round (work continued on `feature/f260-one-world`), so the Open PR Gate had nothing to act on |
| `git push -u origin feature/f260-one-world` | runs AFTER this file is committed; see the note under Verification |

NO git worktree was created this round, so none was removed and none needed
pruning. No PR created. No PR merged. No force push. No branch deleted. No glob
was used to remove anything. No file under `.remedy-wt/` was ever `git add`ed
(`git ls-files .remedy-wt` is EMPTY).

## Verification

ONE LINE PER GATE, with its REAL exit code. Every exit code was taken from a
Python `subprocess.run(...).returncode`; the sandbox bash guard rejects `$?`,
`$( )` and shell loop forms BY FORM. `cmp` and `remedy` are denied, so byte
comparisons went through `filecmp.cmp(shallow=False)` plus sha256, and the CLI
through `python3 -m apps.cli.grouped`. All four suites of G7 ran SERIALLY in the
PRIMARY checkout, after C3. G1 to G8 were additionally RE-RUN read-only after C3
by a harness that takes every pre-image from `git show 7a1ce69d:<path>` and exits
non-zero on any failed reading; the exit codes below are that harness's, one
subprocess per gate.

| Gate | Exit | Real reading |
|---|---|---|
| G1 TRANSPORT | 0 | `.remedy-wt/f260-r18-block.md`, `.agent/authored/f260-r18.md` and `.agent/last_block.md` all sha256 `657022416f31310536a64d78d191c5aa264184258399aa9f1cd10f8f6d9e62b1` at **28307 bytes**; both writes `shutil.copyfile`, both `filecmp.cmp(shallow=False)` = True, all checked BEFORE staging C0a |
| G2(a) live_review | 0 | `post == pre + b"\n" + GATE_R17 + b"\n"` True; `post[:len(pre)] == pre` True. **959115 → 964554 bytes** |
| G2(b) live_review | 0 | N **COUNTED from the slice = 1**. Blank-line units **439 → 440**. Last N units == the slice's paragraphs IN ORDER: True |
| G2(c) live_review | 0 | negative control run IN MEMORY on a `bytes` object: byte flipped at offset 959126, inside the FIRST appended paragraph — reader (a) REJECT, reader (b) REJECT. Restored: (a) accept, (b) accept, restored image == disk image True |
| G2 prose_slips | 0 | `post == pre + b"\n" + SLIP24 + b"\n"` True; prefix preserved. **122752 → 123846 bytes**; blank-line units **154 → 155** |
| G3 THE PLAN | 0 | `.agent/plan.md` == PLAN slice + exactly one trailing newline (True). **1820 bytes, 38 lines**, under the 50-line cap; carries `## Goal` and `## Next Steps`; zero marker lines |
| G4 STATUSPAIR | 0 | FROM count BEFORE **1**; `TO contains FROM` = **false**; FROM count AFTER **0**; TO count AFTER **1** |
| G4 READMECOUNT | 0 | FROM count BEFORE **1**; `TO contains FROM` = **false**; FROM count AFTER **0**; TO count AFTER **1** |
| G4 READMETIER | 0 | FROM count BEFORE **1**; `TO contains FROM` = **false**; FROM count AFTER **0**; TO count AFTER **1** |
| G4 PINPAIR | 0 | FROM count BEFORE **1**; `TO contains FROM` = **false**; FROM count AFTER **0**; TO count AFTER **1** |
| G4 RECONSTRUCTIONS | 0 | ONE boolean per file, recomputed from the pre-edit bytes with only that file's own pairs applied: `docs/roadmap/STATUS.md` **True**, `README.md` **True**, `tests/docs/test_docs_consistency.py` **True**; each still ends with exactly **one** newline |
| G5 GENPAIR ×5 | 0 | PER FILE, FROM before / FROM after / TO after: `T2_F261.md` **1 / 0 / 1**; `T2_F268.md` **1 / 0 / 1**; `T2_F269.md` **1 / 0 / 1**; `T2_F270.md` **1 / 0 / 1**; `T2_F271.md` **1 / 0 / 1**. Whole-file reconstruction from the pre-edit bytes True for each |
| G5 F263PAIR | 0 | `T2_F263.md` FROM before **1**, FROM after **0**, TO after **1**; whole-file reconstruction True |
| G5 SWEEP | 0 | `amend0906-split-placement` appears **0** times in all five GENPAIR files after the edit; `F272` appears **exactly once** in the single `**Tier` line of all SIX files |
| G6 THE NEW FILE | 0 | `docs/roadmap/features/T2_F272.md` **6852 bytes**, == F272FILE slice + exactly one trailing newline **True**; **ZERO** lines beginning `<<<BEGIN ` or `<<<END `; first line begins `# T2_F272 — `; `git status --porcelain` showed `?? docs/roadmap/features/T2_F272.md` — a NEW file — before staging, and `git cat-file -e 7a1ce69d:<path>` returns non-zero |
| G7 LEDGER/README | 0 | feature detail files **272**; STATUS entries **272**; ids missing from `range(1, 273)` **[] for both**; `^- \[x\] F` **73**; `^- \[~\] F` **1**; README numeral parsed by `^(\d+) of (\d+) registered items accepted\.` = **73 / 272**; `TOTAL_FEATURES` **272**; F272 filename tier **2** and STATUS tier **2**; zero duplicate ids on either side |
| G7 `tests/docs/` | 0 | **303 passed** in 0.50 s; zero `^FAILED`, zero `^ERROR` |
| G7 `tests/orchestration/test_roadmap_index.py` | 0 | **30 passed** in 0.36 s; zero `^FAILED`, zero `^ERROR` |
| G7 `tests/cli/test_golden_path.py` (canary) | 0 | **42 passed** in 21.07 s; zero `^FAILED`, zero `^ERROR` |
| G7 `python3 -m apps.cli.grouped integrity check --json` | 0 | `"passed": true`, `"fail_count": 0`, 5 checks — measured AFTER C3, as the gate orders; see deviation 2 |
| G8 LINT | 0 | `python3 -m ruff check tests/docs/test_docs_consistency.py` → **"All checks passed!"**. Confirmed by counting: `git diff --name-only 7a1ce69d..189d055d` yields **15** paths of which **exactly 1** has a `.py` extension, and it is that file |
| G8 TREE | 0 | `git status --porcelain` EMPTY; `git ls-files .remedy-wt` EMPTY |
| G8 STRUCTURE | 0 | C0a 1 parent, **+399**; C0b 1 parent, **+337**; C1 1 parent, **+23**; C2 1 parent, **+4**; C3 1 parent, **+124**. Every insertion count under 500 |

## Authored-text proofs

- **Transport is a COPY chain, never a retype.** `.remedy-wt/f260-r18-block.md`
  (the delegation's source file on disk), `.agent/authored/f260-r18.md` and
  `.agent/last_block.md` all hash to
  `657022416f31310536a64d78d191c5aa264184258399aa9f1cd10f8f6d9e62b1` at 28307
  bytes. Both writes went through `shutil.copyfile` and each was proved with
  `filecmp.cmp(shallow=False)` = True before staging.
- **Every slice was extracted from the COMMITTED authored copy** after C0a, and
  never from the delegation message and never retyped. The extractor matches
  lines EXACTLY equal to `<<<BEGIN name>>>` / `<<<END name>>>` by POSITION, not by
  blank-line separation, which matters here because several `<<<END X>>>` lines
  are immediately followed by a `<<<BEGIN Y>>>` line with no blank line between.
  The committed blob was compared byte-for-byte against the working copy
  (`git show HEAD:.agent/authored/f260-r18.md` == file bytes: True, 28307 bytes).
- **Marker census in the committed authored copy**: **32** marker lines, exactly
  two per slice for all SIXTEEN slices (`STATUSPAIR_FROM/TO`,
  `READMECOUNT_FROM/TO`, `READMETIER_FROM/TO`, `PINPAIR_FROM/TO`,
  `GENPAIR_FROM/TO`, `F263PAIR_FROM/TO`, `F272FILE`, `PLAN`, `GATE_R17`,
  `SLIP24`). **ZERO** marker lines reached `.agent/plan.md`,
  `.agent/live_review.md`, `.agent/prose_slips.md`,
  `docs/roadmap/features/T2_F272.md` or any other file this round wrote.
- **Slice sizes**: STATUSPAIR_FROM 99 B / 2 lines; STATUSPAIR_TO 214 B / 3 lines;
  READMECOUNT_FROM 36 B / 1 line; READMECOUNT_TO 36 B / 1 line; READMETIER_FROM
  44 B / 1 line; READMETIER_TO 44 B / 1 line; PINPAIR_FROM 62 B / 2 lines;
  PINPAIR_TO 402 B / 7 lines; GENPAIR_FROM 69 B / 1 line; GENPAIR_TO 108 B /
  1 line; F263PAIR_FROM 60 B / 1 line; F263PAIR_TO 168 B / 1 line; F272FILE
  6851 B / 108 lines / 15 paragraphs (file 6852 with its one trailing newline);
  PLAN 1819 B / 38 lines (file 1820); GATE_R17 5437 B / 1 line / 1 paragraph;
  SLIP24 1092 B / 1 line / 1 paragraph.
- **Every pair was applied with `str.replace(FROM, TO, 1)` AFTER an `assert` that
  the FROM occurred EXACTLY ONCE in the file being edited.** GENPAIR was asserted
  once PER FILE across its five files, never once overall.
- **Every append recipe was derived from its OWN target's measured terminal
  byte**, with the `assert` executed BEFORE the write, as constraint 2 orders. No
  recipe was copied from one file to another. Both of the block's measurements
  reproduced EXACTLY: `.agent/live_review.md` 959115 B / **1** terminal newline →
  `pre + b"\n" + GATE_R17 + b"\n"`; `.agent/prose_slips.md` 122752 B / **1**
  terminal newline → `pre + b"\n" + SLIP24 + b"\n"`.
- **Blank-line unit definition**, stated so the reviewer can reproduce it: the
  WHOLE file image, with trailing newlines stripped, split on `"\n\n"`. Under that
  definition the pre-round readings are 439 for `.agent/live_review.md` and 154
  for `.agent/prose_slips.md`, which are exactly the post-round-17 numbers the
  previous handback recorded, so the definition is shared with the reviewer's.

## Deviations & assumptions

**1 — NO SLICE, TEST OR GATE WAS ADJUSTED.** Every one of the six pairs and both
appends applied cleanly on the first attempt: all six FROMs occurred exactly once
in their own targets, all six containment readings printed `false` as the block
states, and every FROM count after its edit is 0. Nothing needed smoothing and
nothing was smoothed.

**2 — `integrity check` IS RED BEFORE C3 IS COMMITTED, GREEN AFTER, WHICH IS WHY
THE GATE SAYS "AFTER C3".** Run in the working tree before staging, the check
exits **1** on `relevant_untracked: "1 relevant untracked:
docs/roadmap/features/T2_F272.md"` — the new file is by definition untracked
until it is committed. Run after C3, it exits **0** with `"passed": true` and
`"fail_count": 0`. Recorded rather than hidden: the reported exit code 0 is the
post-C3 one the gate asks for, and the pre-C3 red is not a defect but the
check working.

**3 — `tests/docs/` COLLECTS 303 TESTS BOTH BEFORE AND AFTER THE REGISTRATION.**
Adding a 272nd feature file did not add a test to that suite, so the pass count
is unchanged at 303 from round 17. The suite's per-file checks are evidently
aggregated rather than parametrised per feature file. Flagged only so that the
reviewer does not read the identical number as a stale measurement — it was
re-measured after C3, not carried over.

**4 — C1 (the plan) PRECEDES C2 (the ledger)**, a departure from
planner_reviewer_prompt.md §3 item 23 that the block's own Bundle orders. Carried
unchanged. `.agent/plan.md` became current at C1, BEFORE the ledger append at C2,
which is the property item 23 protects.

**5 — NO `Done:` OR `Landed:` PARAGRAPH WAS AUTHORED** for any finding
(constraint 5). GATE_R17 is a `Gate:` record and registers nothing; the open set
is unchanged at **298 by distinct id**.

**6 — THE SIX DEPENDENTS ARE THE COMPLETE SET, MEASURED NOT ASSUMED.** The block
states that the operator's amend0906 commit reached five of six dependents. The
worker verified the SET independently: exactly six feature files name F260 in
their `**Tier … Depends on:` line — T2_F261, T2_F263, T2_F268, T2_F269, T2_F270,
T2_F271 — and all six were edited. No seventh exists. Note that the F272FILE
slice names **F266** in its own "Blocks/used by" list; F266's file is
`T4_F266.md` and it does NOT name F260 (or F272) in its Depends-on line, so
amend0906's rule did not reach it and it was correctly left untouched. That
leaves one one-directional cross-reference on disk — F272 claims to block F266,
F266 does not claim to depend on F272 — applied as the slice was written and
declared here rather than repaired, since repairing it would be an edit the
block did not order and a path outside the change set.

**7 — README TIER 2 IS AN AGGREGATE ACROSS FOUR TIER-2 HEADINGS.** F272's STATUS
line sits under `## Tier 2 — Vocabulary & Concept Block`, while the README row
READMETIER edits is named "Minimal Self-Build Runtime". The worker measured the
aggregate before applying: counting `- [ /x/~] F` lines under every `## Tier 2`
heading in STATUS.md gives 24 total / 16 done before the edit, matching the row
exactly, and 25 / 16 after. So the row is the tier-number aggregate and 24 → 25
is right. Recorded because the row's NAME makes the pair look mismatched.

**8 — SCRATCH DISCIPLINE.** Seven helper scripts were written under the
gitignored `.remedy-wt/` and run with `python3 -B`. None was ever `git add`ed;
`git ls-files .remedy-wt` is EMPTY. No worktree was created, so nothing needed
removing by exact path and nothing needed pruning.

**9 — THE BLOCK'S BASE SHA RESOLVES.** The full forty-character base
`7a1ce69d594043dfaad6c69161c93613d4229821` this block names IS a real object and
WAS the branch tip and `origin/feature/f260-one-world` at the start of the round.
Verified with `git rev-parse HEAD` before any write.

**10 — TWO CLAIMS INSIDE THE AUTHORED SLICES WERE NOT INDEPENDENTLY RE-MEASURED
BY THE WORKER**, and are applied on the block's authority: GATE_R17's entire
census and range narrative (it is the reviewer's own record of round 17, which
the worker transported byte-for-byte), and the F272FILE slice's assertions about
what F260 built and which of its Acceptance items were open at close. Flagged so
the reviewer re-reads them at its own gate rather than treating them as
worker-verified. The one census number the worker DID re-measure independently
after C2 agrees with GATE_R17: 301 registrations over 301 distinct ids, 5 `Done:`
lines over 3 distinct ids, open set **298** by distinct id, and `^Gate: ` now 27
with `^Gate: R17 — ` at exactly 1.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a — `.agent/authored/f260-r18.md` | done | `b28b451e` |
| C0b — `.agent/last_block.md` | done | `c4ab0416` |
| C1 — `.agent/plan.md` from the PLAN slice | done | `e788caf0` |
| C2 — GATE_R17 then SLIP24, ONE commit in that file order | done | `13a0c3a9` |
| C3 — THE REGISTRATION, ten paths, ONE atomic commit | done | `189d055d` |
| C4 — rewrite `.agent/handoff.md` | done | this file |
| G1 TRANSPORT | done | exit 0; one digest, three files, both `filecmp` True |
| G2(a) live_review | done | exit 0; exact image, prefix preserved, 959115 → 964554 |
| G2(b) live_review | done | exit 0; N=1 counted from the slice, units 439 → 440 |
| G2(c) live_review | done | exit 0; both readers reject the corrupted image, both accept the restored one |
| G2 prose_slips | done | exit 0; byte equality True, 122752 → 123846, units 154 → 155 |
| G3 THE PLAN | done | exit 0; 1820 bytes, 38 lines, under the cap |
| G4 STATUSPAIR | done | exit 0; 1 / false / 0 / 1 |
| G4 READMECOUNT | done | exit 0; 1 / false / 0 / 1 |
| G4 READMETIER | done | exit 0; 1 / false / 0 / 1 |
| G4 PINPAIR | done | exit 0; 1 / false / 0 / 1 |
| G4 RECONSTRUCTIONS | done | exit 0; one boolean per file, all three True, all three end in one newline |
| G5 GENPAIR ×5 | done | exit 0; 1 / 0 / 1 per file for all five, asserted PER FILE |
| G5 F263PAIR | done | exit 0; 1 / 0 / 1 |
| G5 SWEEP | done | exit 0; placeholder gone from all five, `F272` once in the `**Tier` line of all six |
| G6 THE NEW FILE | done | exit 0; 6852 bytes, slice + one newline, zero markers, `??` before staging |
| G7 LEDGER/README | done | exit 0; 272 / 272, no gaps, 73 / 1, README 73 of 272, pin 272, tier 2 both ways |
| G7 `tests/docs/` | done | exit 0; 303 passed |
| G7 `tests/orchestration/test_roadmap_index.py` | done | exit 0; 30 passed |
| G7 canary `tests/cli/test_golden_path.py` | done | exit 0; 42 passed |
| G7 `integrity check --json` | done | exit 0 after C3; `passed` true, `fail_count` 0, 5 checks (deviation 2) |
| G8 LINT | done | exit 0; ruff clean on the one `.py` file in the range, count confirmed |
| G8 TREE | done | exit 0; both EMPTY |
| G8 STRUCTURE | done | exit 0; five single-parent commits, insertions 399/337/23/4/124 |

## Open findings

**298 open by distinct id**, unchanged from round 17. This round registered
nothing and resolved nothing (constraint 5). Census after C2, counted by script
over `.agent/live_review.md`: 301 registrations over 301 distinct ids, 5 `Done:`
lines over 3 distinct ids, 27 `Gate:` records, `^Gate: R17 — ` exactly 1.

`.agent/candidates.md` was not touched this round.

## Next

**Phase 1 rule 1 first: re-read `.agent/STOP` from disk.** It did not exist at
this handback. There is no open PR for this branch and none was created
(`gh pr list --state open` → `[]`).

DECISION F260 D8 is now both RULED (round 17) and APPLIED (this round). F272
exists as a registered, unchecked STATUS line directly after F260's, so Rule A5
proposes it next once F260 flips to accepted.

1. **The integration gate**: the full suite at the branch head and at the merge
   base, per docs/agents/integration_gate.md. Remember the R-0736 parity trap —
   `copytree` keeps mtimes while `git worktree add` stamps newer.
2. **Closure part 1**: the self-use item, the evidence job and the review zip.
   The self-use queue is EXHAUSTED (all ten entries carry a `consumed_by`), so
   precondition 6 runs `generate_and_append_if_empty` FIRST and records
   `self-use NONE (queue exhausted)` only after that also answers `None`.
3. **Closure part 2**: the verdict bookings and the ledger rotation
   (`scripts/rotate_live_review.py`), which runs BEFORE the STATUS flip and
   re-baselines `.agent/live_review.md`.
4. **Closure part 3**: the STATUS accepted flip for F260 — `[~]` → `[x]` with its
   evidence tail — plus the README sync in the SAME commit, the handback and the
   pull request, left UNMERGED as the operator's review window.

Byte baselines for whoever authors round 19 — every one measured this round:
`.agent/live_review.md` **964554 bytes / 440 units / 1 terminal newline**;
`.agent/prose_slips.md` **123846 bytes / 155 units / 1 terminal newline**;
`.agent/plan.md` **1820 bytes**; `docs/roadmap/STATUS.md` **39107 bytes**;
`README.md` **14615 bytes**; `docs/roadmap/features/T2_F272.md` **6852 bytes**.
`.agent/decisions.md` was NOT touched this round and stands at the round-17
reading of **853742 bytes / 1 terminal newline**. Note that the ledger rotation
of amend0905-throughput runs inside the closure sequence and will re-baseline
`.agent/live_review.md` again.

The soft-limit banner
`SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE` is NOT emitted here:
this handback is one round's report, and the session-level scope report is the
planner/reviewer session's own obligation. Claiming it in this file would be an
overclaim. The scope report's SUBSTANCE is on disk as DECISION F260 D8, as the
Built State section of `docs/roadmap/features/T2_F260.md`, and now as the
registered `docs/roadmap/features/T2_F272.md`.
