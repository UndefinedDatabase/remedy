# Handoff — F260 One world · round 17 · the split ruled, the built scope stated

## Session

SESSION 7 of feature F260 · round 17 · rounds so far 17

`.agent/STOP` did NOT exist at the start of this round (`ls .agent/STOP` → "No
such file or directory"), was re-checked after C3 and before this handback, and
still does not exist.

Context self-assessment (amend0905-throughput): context was never a constraint
this round — five small commits, all of them `.agent/**` prose plus one
`docs/roadmap/` file, and the whole gate set ran in about 23 seconds of suite
time, almost all of it the canary.

**THIS SESSION IS AT THE SOFT LIMIT** (25 rounds or 7 sessions, whichever first;
this is session 7). This round is the FIRST HALF of the standing
amend0905-throughput default: the split is RULED as DECISION F260 D8, round 16's
verdict and the reviewer's three prose slips are booked, and F260's own feature
file now states what it built and what moves. The follow-up's REGISTRATION — its
detail file, its STATUS line, the README counters and the `TOTAL_FEATURES` pin —
is deliberately the NEXT round's, so that the ruling is recorded before it is
applied. `docs/roadmap/STATUS.md` and `README.md` were NOT touched this round.

## Range

Review of `867f34ae0c4632c961ad4a0dc9ef168d595606fc`..`HEAD`.

FIVE commits plus this handback. ALL FIVE are single-parent. They are EXACTLY the
bundle's ordered sequence C0a → C0b → C1 → C2 → C3 → C4, with nothing added,
dropped or reordered. Largest insertion count 324 (`.agent/authored/f260-r17.md`,
a single `.agent/**` state write); nothing approached the 500-insertion cap.

## Commits

`+/-` taken from `git log --numstat`, never re-derived by eye.

### feaf92845b3aed886c7ae05f1e5f198b04409745 — f260 r17: save the round 17 step block verbatim as authored text
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f260-r17.md | +324 / -0 | C0a — `shutil.copyfile` from `.remedy-wt/f260-r17-block.md`, proved by `filecmp.cmp(shallow=False)` = True and sha256 equal to the delegation digest BEFORE staging |

### 70a7e1797f2853012dad24b502397fa77773cfb9 — f260 r17: mirror the round 17 block into the last block state file
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +242 / -161 | C0b — same source file, same `shutil.copyfile` route, same two proofs |

### de90a2a705ffd9953b71346037234d5a624105b4 — f260 r17: rewrite the plan for the split ruling round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +15 / -18 | C1 — whole-file replacement by the PLAN slice plus exactly one trailing newline; 2118 bytes, 40 lines, under the 50-line cap, carrying `## Goal` and `## Next Steps` |

### f5b7c750324cfddc8c3b9287506e52e133384e9b — f260 r17: book round 16 gate record, three prose slips and DECISION D8
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | C2, written FIRST — GATE_R16 appended; 953191 → 959115 bytes |
| .agent/prose_slips.md | +6 / -0 | C2, written SECOND — SLIP21, SLIP22, SLIP23 in that order, one blank line between each; 119984 → 122752 bytes |
| .agent/decisions.md | +4 / -1 | C2, written THIRD — DEC_D8 appended by the ZERO-terminal-newline recipe `pre + b"\n\n" + DEC_D8 + b"\n"`; 848037 → 853742 bytes. The one deletion is the "\ No newline at end of file" marker line, since the recipe restores a trailing newline |

### 8459e9eaded9b81fe8fedaf8cc96ec943dc445a2 — f260 r17: state F260 built scope in its feature file and amend the split point
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F260.md | +50 / -2 | C3 — the three FROM/TO pairs applied with `str.replace(FROM, TO, 1)` after asserting each FROM occurred exactly once, then the BUILTSTATE slice appended by the recipe derived from this file's own measured terminal byte (one newline); 28449 → 32057 bytes |

### C4 — this file
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4 — a handback cannot table the commit that writes it (R-0149 pattern; constraint 9). No gate reading was taken after this file existed; the reviewer measures C4's own numbers at the next gate |

## External actions

| Command | Outcome |
|---|---|
| `sha256sum .remedy-wt/f260-r17-block.md` | exit 0; `ceec367fcf541c704f86a2d2259929445044cc49b729809a61e20fc63aeb4a03` — equals the digest the delegation names |
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | exit 0; `[]` — NO open PR. No new branch was created this round (work continued on the existing `feature/f260-one-world`), so the Open PR Gate had nothing to act on |
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
PRIMARY checkout, after C3.

| Gate | Exit | Real reading |
|---|---|---|
| G1 TRANSPORT | 0 | `.remedy-wt/f260-r17-block.md`, `.agent/authored/f260-r17.md` and `.agent/last_block.md` all sha256 `ceec367fcf541c704f86a2d2259929445044cc49b729809a61e20fc63aeb4a03` at 31781 bytes; both writes `shutil.copyfile`, both `filecmp.cmp(shallow=False)` = True, all checked BEFORE staging C0a |
| G2(a) live_review | 0 | `post == pre + b"\n" + GATE_R16 + b"\n"` True; `post[:len(pre)] == pre` True. **953191 → 959115 bytes** |
| G2(b) live_review | 0 | N **COUNTED from the slice = 1**. Blank-line units **438 → 439**. Last N units == the slice's paragraphs IN ORDER: True |
| G2(c) live_review | 0 | negative control run IN MEMORY on a `bytes` object: byte flipped at offset 953232, inside the FIRST appended paragraph — reader (a) REJECT, reader (b) REJECT. Restored: (a) accept, (b) accept, restored image == disk image True |
| G2(a) decisions | 0 | `post == pre + b"\n\n" + DEC_D8 + b"\n"` True; `post[:len(pre)] == pre` True. **848037 → 853742 bytes**; terminal newlines **0 → 1** |
| G2(b) decisions | 0 | N **COUNTED from the slice = 1**. Blank-line units **1899 → 1900**. Last N units == the slice's paragraphs IN ORDER: True |
| G2(c) decisions | 0 | negative control IN MEMORY: byte flipped at offset 848079, inside the FIRST appended paragraph — reader (a) REJECT, reader (b) REJECT. Restored: (a) accept, (b) accept, restored image == disk image True |
| G2 prose_slips | 0 | `post == pre + b"\n" + SLIP21 + b"\n\n" + SLIP22 + b"\n\n" + SLIP23 + b"\n"` True. **119984 → 122752 bytes**; blank-line units **151 → 154**; the last three units are SLIP21, SLIP22, SLIP23 **in that order**: True |
| G3 THE PLAN | 0 | `.agent/plan.md` == PLAN slice + exactly one trailing newline (True). **2118 bytes, 40 lines**, under the 50-line cap; carries `## Goal` and `## Next Steps`; zero marker lines |
| G4 PAIR P1 | 0 | FROM count BEFORE **1**; `TO contains FROM` = **true**; FROM count AFTER **1** (append-shaped, not a failure); TO count AFTER **1** |
| G4 PAIR P2 | 0 | FROM count BEFORE **1**; `TO contains FROM` = **false**; FROM count AFTER **0**; TO count AFTER **1** |
| G4 PAIR P3 | 0 | FROM count BEFORE **1**; `TO contains FROM` = **true**; FROM count AFTER **1** (append-shaped, not a failure); TO count AFTER **1** |
| G5 APPEND + RECONSTRUCTION | 0 | ONE boolean, recomputed independently from the pre-edit bytes (three `str.replace(..., 1)` then the recipe derived from the pre-edit file's own measured terminal byte of ONE newline): **whole-file reconstruction == disk: True**. **28449 → 32057 bytes**; ends with exactly **1** newline; **ZERO** lines beginning `<<<BEGIN ` or `<<<END ` |
| G6 CENSUS | 0 | `^Gate: ` = **26** ✔; `^Gate: R16 — ` = exactly **1** ✔; registrations `^- R-\d{4} — ` = **301 lines over 301 DISTINCT ids** ✔; `^Done: R-\d{4} — ` = **5 lines over 3 distinct ids** ✔; **OPEN SET BY DISTINCT ID = 298** ✔ unchanged; `.agent/live_review.md`, `.agent/prose_slips.md` and `.agent/decisions.md` each carry **0** lines beginning `<<<BEGIN ` or `<<<END ` ✔ |
| G7 `tests/docs/` | 0 | **303 passed** in 0.50 s; zero `^FAILED`, zero `^ERROR` |
| G7 `tests/orchestration/test_roadmap_index.py` | 0 | **30 passed** in 0.36 s; zero `^FAILED`, zero `^ERROR` |
| G7 `tests/cli/test_golden_path.py` (canary) | 0 | **42 passed** in 21.25 s; zero `^FAILED`, zero `^ERROR` |
| G7 `python3 -m apps.cli.grouped integrity check --json` | 0 | `"passed": true`, `"fail_count": 0`, 5 checks |
| G8 TREE | 0 | `git status --porcelain` EMPTY; `git ls-files .remedy-wt` EMPTY |
| G8 STRUCTURE | 0 | C0a 1 parent, +324; C0b 1 parent, +242; C1 1 parent, +15; C2 1 parent, +12; C3 1 parent, +50. Every insertion count under 500 |
| G8 LINT | **n/a** | `git diff --name-only 867f34ae..C3` yields 7 paths and **ZERO** with a `.py` extension, so `ruff` has no target. Reported as NOT APPLICABLE; no target was invented |

## Authored-text proofs

- **Transport is a COPY chain, never a retype.** `.remedy-wt/f260-r17-block.md`
  (the delegation's source file on disk), `.agent/authored/f260-r17.md` and
  `.agent/last_block.md` all hash to
  `ceec367fcf541c704f86a2d2259929445044cc49b729809a61e20fc63aeb4a03` at 31781
  bytes. Both writes went through `shutil.copyfile` and each was proved with
  `filecmp.cmp(shallow=False)` = True before staging.
- **Every slice was extracted from the COMMITTED authored copy** after C0a, and
  never from the delegation message and never retyped. The extractor matches
  lines EXACTLY equal to `<<<BEGIN name>>>` / `<<<END name>>>`, asserts each
  occurs exactly once, and asserts no marker line lies inside a slice body. The
  committed blob was additionally compared byte-for-byte against the working copy
  (`git show HEAD:.agent/authored/f260-r17.md` == file bytes: True).
- **Marker census in the committed authored copy**: **26** marker lines, exactly
  two per slice for all THIRTEEN slices (`P1_FROM`, `P1_TO`, `P2_FROM`, `P2_TO`,
  `P3_FROM`, `P3_TO`, `PLAN`, `GATE_R16`, `SLIP21`, `SLIP22`, `SLIP23`, `DEC_D8`,
  `BUILTSTATE`). **ZERO** marker lines reached `.agent/plan.md`,
  `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/decisions.md` or
  `docs/roadmap/features/T2_F260.md`.
- **Slice sizes**: P1_FROM 72 B / 1 line; P1_TO 427 B / 6 lines; P2_FROM 66 B /
  1 line; P2_TO 248 B / 3 lines; P3_FROM 144 B / 2 lines; P3_TO 490 B / 6 lines;
  PLAN 2117 B / 40 lines (file 2118 with its one trailing newline); GATE_R16
  5922 B / 1 line / 1 paragraph; SLIP21 925 B, SLIP22 894 B, SLIP23 943 B, each
  1 line / 1 paragraph; DEC_D8 5702 B / 2 lines / 1 paragraph; BUILTSTATE 2723 B
  / 36 lines / 3 paragraphs.
- **Every append recipe was derived from its OWN target's measured terminal
  byte**, with the `assert` executed BEFORE the write, as constraint 2 orders.
  No recipe was copied from one file to another. All three of the block's
  measurements reproduced EXACTLY: `.agent/live_review.md` 953191 B / **1**
  terminal newline → `pre + b"\n" + slice + b"\n"`; `.agent/prose_slips.md`
  119984 B / **1** terminal newline → `pre + b"\n" + S21 + b"\n\n" + S22 +
  b"\n\n" + S23 + b"\n"`; `.agent/decisions.md` 848037 B / **ZERO** terminal
  newlines → `pre + b"\n\n" + DEC_D8 + b"\n"`. A fourth measurement was taken
  independently for C3: `docs/roadmap/features/T2_F260.md` 28449 B / **1**
  terminal newline → `edited + b"\n" + BUILTSTATE + b"\n"`.
- **Blank-line unit definition**, stated so the reviewer can reproduce it: the
  WHOLE file image, with exactly one trailing newline stripped if present, split
  on `"\n\n"`. Under that definition the pre-round readings are 438 for
  `.agent/live_review.md` and 151 for `.agent/prose_slips.md`, which are exactly
  the post-round-16 numbers the previous handback recorded, so the definition is
  shared with the reviewer's.

## Deviations & assumptions

**1 — P1's TO INTERLEAVES THE HEADER NOTE CHRONOLOGICALLY.** The header block of
`docs/roadmap/features/T2_F260.md` reads, in file order, "Registered 2026-08-31"
→ (new) "BUILT across rounds 1 to 17 (2026-09-05/06)" → "Rewritten 2026-09-05".
Because P1's FROM is the 2026-08-31 line and its TO appends after it, the
2026-09-06 note now sits BEFORE the 2026-09-05 note. Applied BYTE FOR BYTE as
written (constraint 1); no slice was reordered or edited to smooth this. Nothing
is factually wrong on disk — each line is individually true — but the block's
author may want the note placed after the "Rewritten" line in a later round.

**2 — P3's TO LEAVES A 105-CHARACTER LINE.** P3's FROM ends mid-line at "never
inside T005." while the source line continues " `docs/system/". The replacement
therefore produces the line
"it carries is untouched and still binds the follow-up: never split inside T005. `docs/system/"
followed by the original "vocabulary.md` (F259) is binding..." line. The
sentence structure and the link are intact and the file is valid Markdown, but
the line is far wider than the file's ~80-column convention. Applied as written;
declared rather than reflowed.

**3 — `.agent/decisions.md`'s ZERO-NEWLINE TERMINAL BYTE IS CONFIRMED AND WAS
HANDLED SEPARATELY.** The round-16 handback's deviation 4 warned that this file
now ends without a trailing newline. Measured independently at `867f34ae`:
848037 bytes, **0** trailing newlines, sha256
`e161a74832cc6452f6fc2755d09de4bbd1fd8e3d223ec25b6410904e5cfef463` — all three
values exactly as constraint 2 states. The `assert trailing == 0` ran before the
write. The other two record files were asserted at `== 1` separately. This is not
a departure; it is recorded because it is the trap constraint 2 exists to defuse
and the next round MUST re-baseline again: `.agent/decisions.md` now ends with
**one** trailing newline at 853742 bytes.

**4 — C1 (the plan) PRECEDES C2 (the ledger)**, a departure from
planner_reviewer_prompt.md §3 item 23 that the block's own Bundle orders. Carried
unchanged. `.agent/plan.md` became current at C1, BEFORE the ledger append at C2,
which is the property item 23 protects.

**5 — NO `Done:` OR `Landed:` PARAGRAPH WAS AUTHORED** for any finding
(constraint 4). GATE_R16 is a `Gate:` record and registers nothing; the open set
is unchanged at **298 by distinct id**, confirmed by G6.

**6 — G8's LINT HALF IS NOT APPLICABLE, NOT SKIPPED FOR CONVENIENCE.** The range
`867f34ae..C3` touches exactly 7 paths, none with a `.py` extension, so `ruff`
had no target and none was invented — which is the reading the gate itself
prescribes.

**7 — SCRATCH DISCIPLINE.** Seven helper scripts were written under the
gitignored `.remedy-wt/` and run with `python3 -B`. None was ever `git add`ed;
`git ls-files .remedy-wt` is EMPTY. No worktree was created, so nothing needed
removing by exact path and nothing needed pruning.

**8 — THE BLOCK'S BASE SHA RESOLVES THIS TIME.** Unlike round 16 (SLIP21), the
full forty-character base `867f34ae0c4632c961ad4a0dc9ef168d595606fc` this block
names IS a real object and IS the branch tip and `origin/feature/f260-one-world`.
Verified with `git rev-parse HEAD` before any write. No deviation; recorded
because the previous round's defect made it worth measuring.

**9 — TWO CLAIMS INSIDE THE AUTHORED SLICES WERE NOT INDEPENDENTLY RE-MEASURED
BY THE WORKER**, and are applied on the block's authority: BUILTSTATE's round
attributions ("T001 (rounds 1 to 6)", "T002 (rounds 7 to 15)") and DEC_D8's
statement that "Every round from 2 to 16 PASSED, one round FAILED and was
repaired". These are ledger readings the reviewer holds; the worker transported
them byte-for-byte and did not verify them. Flagged so the reviewer re-reads
them at its own gate rather than treating them as worker-verified.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a — `.agent/authored/f260-r17.md` | done | `feaf9284` |
| C0b — `.agent/last_block.md` | done | `70a7e179` |
| C1 — `.agent/plan.md` from the PLAN slice | done | `de90a2a7` |
| C2 — GATE_R16, then SLIP21/22/23, then DEC_D8, ONE commit in that file order | done | `f5b7c750` |
| C3 — `docs/roadmap/features/T2_F260.md`: three pairs + BUILTSTATE append | done | `8459e9ea` |
| C4 — rewrite `.agent/handoff.md` | done | this file |
| G1 TRANSPORT | done | exit 0; one digest, three files, both `filecmp` True |
| G2(a) live_review | done | exit 0; exact image, prefix preserved, 953191 → 959115 |
| G2(b) live_review | done | exit 0; N=1 counted from the slice, units 438 → 439 |
| G2(c) live_review | done | exit 0; both readers reject the corrupted image, both accept the restored one |
| G2(a) decisions | done | exit 0; exact image, prefix preserved, 848037 → 853742, terminal 0 → 1 |
| G2(b) decisions | done | exit 0; N=1 counted from the slice, units 1899 → 1900 |
| G2(c) decisions | done | exit 0; both readers reject, both accept after restore |
| G2 prose_slips | done | exit 0; byte equality True, units 151 → 154, last three units in order |
| G3 THE PLAN | done | exit 0; 2118 bytes, 40 lines, under the cap |
| G4 THE THREE PAIRS | done | exit 0; four numbers reported for each of P1, P2, P3 |
| G5 APPEND + RECONSTRUCTION | done | exit 0; one boolean True, 28449 → 32057, one terminal newline, zero markers |
| G6 THE CENSUS | done | exit 0; 26 / `Gate: R16` ×1 / 301-over-301 / 5-over-3 / open 298 / 0 markers in all three files |
| G7 `tests/docs/` | done | exit 0; 303 passed |
| G7 `tests/orchestration/test_roadmap_index.py` | done | exit 0; 30 passed |
| G7 canary `tests/cli/test_golden_path.py` | done | exit 0; 42 passed |
| G7 `integrity check --json` | done | exit 0; `passed` true, `fail_count` 0, 5 checks |
| G8 TREE | done | exit 0; both EMPTY |
| G8 STRUCTURE | done | exit 0; five single-parent commits, insertions 324/242/15/12/50 |
| G8 LINT | skipped | ZERO `.py` files in `867f34ae..C3`; the gate itself says to report it as not applicable rather than invent a target |

## Open findings

**298 open by distinct id**, unchanged from round 16. This round registered
nothing and resolved nothing (constraint 4). Census after C2, counted by script
over `.agent/live_review.md`: 301 registrations over 301 distinct ids, 5 `Done:`
lines over 3 distinct ids, 26 `Gate:` records.

`.agent/candidates.md` was not touched this round.

## Next

**Phase 1 rule 1 first: re-read `.agent/STOP` from disk.** It did not exist at
this handback. There is no open PR for this branch and none was created
(`gh pr list --state open` → `[]`).

DECISION F260 D8 is now ON DISK and binding. The registration it rules is the
next round's, and `docs/roadmap/STATUS.md` and `README.md` are still untouched by
this session, so no committed state has them disagreeing.

1. **Register the follow-up feature** in ONE commit: its detail file, its STATUS
   line DIRECTLY AFTER F260's inside the same tier heading (amend0906-split-
   placement), the README counters, the `TOTAL_FEATURES` pin, and the six
   downstream "Depends on" lines. `tests/docs/test_docs_consistency.py` pins the
   feature count, id contiguity and the filename tier, so these are one commit or
   the suite goes red.
2. **The integration gate**: the full suite at the branch head and at the merge
   base.
3. **Closure part 1**: the self-use item, the evidence job and the review zip.
4. **Closure part 2**: the verdict bookings and the ledger rotation.
5. **Closure part 3**: the STATUS accepted flip, the README sync, the handback
   and the pull request, left UNMERGED as the operator's review window.

Byte baselines for whoever authors round 18 — every one measured this round, and
all four CHANGED: `.agent/live_review.md` **959115 bytes / 439 units / 1 terminal
newline**; `.agent/prose_slips.md` **122752 bytes / 154 units / 1 terminal
newline**; `.agent/decisions.md` **853742 bytes / 1900 units / 1 terminal newline
(it had ZERO last round)**; `docs/roadmap/features/T2_F260.md` **32057 bytes / 1
terminal newline**. Note also that the ledger rotation of amend0905-throughput
runs inside the closure sequence and will re-baseline `.agent/live_review.md`
again.

The soft-limit banner
`SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE` is NOT emitted here:
this handback is one round's report, and the session-level scope report is the
planner/reviewer session's own obligation. Claiming it in this file would be an
overclaim. The scope report's SUBSTANCE, however, is on disk as DECISION F260 D8
and as the Built State section of `docs/roadmap/features/T2_F260.md`.
