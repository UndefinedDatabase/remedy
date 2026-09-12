# Handback — F275 round 81

## Session

`SESSION 28 of feature F275 · round 81 · rounds so far 81`

NO SCOPE REPORT AND NO SESSION-LIMIT BANNER IS OWED. Amendment amend0911-f275-to-scope lifts
F275's soft limit of 20 sessions and 60 rounds without a replacement number, so this round prints
no `SITZUNGS-LIMIT` line.

Context self-assessment: this worker ran one reading round, spent one canary pass and one `ruff`
pass and no other suite, and has ample context left; nothing about the session boundary is forced
by this round.

## Range

Review of `89d4772a`..`HEAD` (the seven commits C0a–C5 plus this handback commit C6).

## Commits

### c7c856f8 F275 R81 C0a: save the round 81 block as authored text

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r81.md` | +343 / -0 | the block transported with `shutil.copyfile`, byte-identical to `.remedy-wt/r81_block.md` |

### 79360bcd F275 R81 C0b: mirror the round 81 block into the last-block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +207 / -217 | rewritten from the COMMITTED C0a blob, not from any working copy |

### 2b63c899 F275 R81 C1: make the plan current for round 81

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +20 / -22 | replaced by slice PLAN81, byte for byte; the first substantive commit, per constraint 6 |

### 8c559176 F275 R81 C2: book the round 80 reviewer verdict

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +8 / -0 | slice RECORD81 appended; the round 80 PASS booked by the first substantive commit of round 81 |

### 0ed1f625 F275 R81 C3: append the round 80 prose slips

| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +4 / -0 | slice SLIPS81 appended; two dated lines and no id, per amend0827 rule 2 |

### 8213456a F275 R81 C4: land the fallback-class artefact

| Path | +/- | Reason |
|---|---|---|
| `.agent/f275_t003_owner_fallback_r81.md` | +300 / -0 | written by the worker from its own run; a NEW document, absent at this round's base |

### 3f4ca0b8 F275 R81 C5: record DECISION F275 D55

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +18 / -0 | slice DEC81 APPENDED; no landed DECISION is rewritten and the deletion column is zero |

### C6 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | measured by the next gate | the round 81 handback; a handoff cannot table the commit that writes it |

THE `+/-` CELLS ABOVE WERE READ FROM `git show --numstat` AND COMPARED CELL BY CELL AGAINST G8's
OWN NUMBERS. The comparison, printed: C0a 343/0 against 343/0 EQUAL; C0b 207/217 against 207/217
EQUAL; C1 20/22 against 20/22 EQUAL; C2 8/0 against 8/0 EQUAL; C3 4/0 against 4/0 EQUAL; C4 300/0
against 300/0 EQUAL; C5 18/0 against 18/0 EQUAL. Seven of seven cell pairs equal, zero differ.
Every commit staged exactly ONE path and every insertion count is under 500.

## External actions

| Command | Outcome |
|---|---|
| `git archive --format=tar -o .remedy-wt/r81_ef75e213.tar ef75e213` | exit 0; the archive of the base tree the recipe of the block orders |
| `tar -xf .remedy-wt/r81_ef75e213.tar -C .remedy-wt/r81_base_worker` and `… -C .remedy-wt/r81_noindex_worker` | exit 0 both; the same extraction twice, one of which is then given an index |
| `git init -q` and `git add -A -f .` inside `.remedy-wt/r81_base_worker` | exit 0 both; the index the static check's `git ls-files` needs. THE NO-INDEX COPY IS LEFT WITHOUT ONE ON PURPOSE — it is G4(c)'s negative control |
| `git push -u origin feature/f275-one-world-completion-part-three` | run after C6; result in the round report |
| `git worktree add` / `git worktree remove` | NOT RUN. `git worktree list` shows the primary checkout alone; both trees under `.remedy-wt/` are plain directory copies and neither is a registered worktree |
| `gh` / `remedy` | NOT RUN, per constraint 8. No pull request created, edited or merged; no branch created or deleted; no merge, no force-push, no history rewrite |

## Verification

Every gate wrote its own transcript under `.remedy-wt/` and the exit code below was read back out
of that file, which carries a `REAL_EXIT=` trailer written by the harness, not out of the process
that ran it.

| Gate | Transcript | REAL exit code | Decisive reading |
|---|---|---|---|
| G1 transport, budget, slices | `.remedy-wt/r81_g1.out` | `REAL_EXIT=0` | `cmp .remedy-wt/r81_block.md` against the committed C0a blob exit **0** with empty output; both 28740 bytes, sha256 `a1177ea4…8ee56fc53fa`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob; SLICE CARDINALITY MEASURED **4** — PLAN81 2808 bytes / 46 lines, RECORD81 3571 / 8, SLIPS81 1341 / 4, DEC81 4380 / 18 — every one matching the sha256 on its own BEGIN marker; TOTAL **343** against the cap of 490 and PROSE **267** against 400, both MATCHING constraint 10; repeated-character lines outside a slice **0** |
| G2 the plan | `.remedy-wt/r81_g2.out` | `REAL_EXIT=0` | `.agent/plan.md` at C1 byte-identical to PLAN81 re-extracted from the COMMITTED C0a blob, 2808 bytes, sha256 `8a6d653a…74beccd248e4`; **46** lines, at most 50; exactly one `## Goal` at line 6 and exactly one `## Next Steps` at line 25 |
| G3 the record, full forensics | `.remedy-wt/r81_g3.out` | `REAL_EXIT=0` | reader A holds for both appends with the arithmetic printed (1093634+3571=1097205 and 1239171+4380=1243551); reader B holds at N COUNTED BY THE SCRIPT as **4** for RECORD81 and **9** for DEC81; both negative controls — one ASCII letter flipped inside the FIRST appended paragraph, `G`→`g` at slice offset 1 and `D`→`d` at offset 4 — REJECTED by BOTH readers; deletion columns **0**, **0** and **0**; `.agent/prose_slips.md` equals its pre-commit blob followed by exactly SLIPS81 and nothing else; the `Gate:` header pattern DERIVED from the ledger's own 102 prior headers, `^Gate:\ F\d+\ R\d+\ `, matches **102 of 102** of them and matches RECORD81, duplicating none byte for byte |
| G4 control, columns, class | `.remedy-wt/r81_g4.out` | `REAL_EXIT=0` | all five pinned inputs MATCH their stated size and digest; THE CONTROL reproduces `.remedy-wt/r77_stage_corrected.out` with **0 differing lines**, the argument vector printed in full, the stage's own exit **0**; THE NEGATIVE CONTROL over the same extraction with no git index decides **nothing** — 994 Python files on disk, `git ls-files` returning **0**, all **2185** ruled sites reported `file unreadable at this tree`, **0** live record classes, DECIDED **0** — and therefore does NOT reproduce the pinned summary, so the control can fail; the five ruled columns split **2 CONFIRMED / 3 REFUSED**; the class is **26** over **91** multi-site lines on **2080** distinct lines over **2185** ruled sites, both partitions closed, and all four cross-checks against the block MATCH |
| G5 the artefact | `.remedy-wt/r81_g5.out` | `REAL_EXIT=0` | the committed C4 blob byte-identical to the file a re-run of the generator produces, 20054 bytes, sha256 `b28e5388…11e0e338380b`; the base lookup `git show 89d4772a:.agent/f275_t003_owner_fallback_r81.md` exit **128** with `exists on disk, but not in '89d4772a'`; **155** indented non-blank lines compared under the rule "its first character is a space and it has a non-space character", **155** matched VERBATIM at STRICTLY INCREASING indices, **0 unmatchable**, first match at saved-output line 3 and last at 172 of 174; **0** wall-clock lines and **0** three-backtick lines; **7** headings in the block's order; `R-0880` named once and stated open; the round 79 and round 80 artefacts byte-identical at the base and at C5 and ABSENT from the changed-path set |
| G6 tree, colours, path set | `.remedy-wt/r81_g6.out` | `REAL_EXIT=0` | `git status --porcelain` printed the EMPTY STRING at C5, shown as `''`; `git worktree list` **one** row, the primary checkout, while `r81_base_worker`, `r81_noindex_worker` and the reviewer's `r81_base` all exist on disk and NONE is registered — both facts hold together; THE CANARY `python3 -B -m pytest tests/cli/test_golden_path.py -q` exit **0**, **42 passed** against the 42 the block says the reviewer measured at the base; `ruff check .` exit **1** by its own design, **26** location rows counted by the gate and cross-checked against its own `Found 26 errors.` line, at the frozen ceiling of 26; a FILESYSTEM `rglob` sweep finding **0** `.py` files anywhere under `.agent/`, the same sweep reaching **2241** files |
| G7 path set and open set | `.remedy-wt/r81_g7_pre.out` | `REAL_EXIT=0` | G7(b): **87** open BY DISTINCT ID at the base and **87** at C5, membership difference EMPTY both ways, `R-0880` OPEN at both; the CANONICAL line-count reading of `scripts/rotate_live_review.count_open_findings`, imported from the shipped file, is **85** at both, so the GAP is **2** at both and DID NOT GROW — it is R-0721 and R-0725, each carrying two `Done:` lines. G7(a) at this mode: EXTRA is already EMPTY and MISSING is exactly `.agent/handoff.md`, the one path C6 alone creates; changed paths under `packages/`, `apps/`, `tests/` or `docs/`: **0** |
| G7(a) over the full range | `.remedy-wt/r81_g7_post.out` | run AFTER C6 — see deviation 1 | its subject includes `.agent/handoff.md`, which C6 alone creates |
| G8 the insertion cap | `.remedy-wt/r81_g8.out` | `REAL_EXIT=0` | C0a 343, C0b 207, C1 20, C2 8, C3 4, C4 300, C5 18 — every one under 500, every commit exactly one path |

THE FIVE RULED COLUMNS, WHICH ARE WHAT THIS ROUND EXISTS TO READ. Each receiver was read FORWARD
from its byte offset, per constraint 4:

| Site | col | receiver | shipped owner check | owners file | pre-flip source at `ef75e213` |
|---|---|---|---|---|---|
| `tests/cli/test_repair_runtime.py:68` | 19 | `job` | **CONFIRMED** | Job | `return str(job.id), str(art.id), str(data_dir)` |
| `tests/cli/test_repair_runtime.py:68` | 32 | `art` | **REFUSED**, absent from the decided set | Job | same line |
| `packages/orchestration/brain_detail.py:345` | 45 | `t` | **CONFIRMED** | Task | `task = next((t for t in job.tasks if str(t.id) == node.id), None)` |
| `packages/orchestration/brain_detail.py:345` | 54 | `node` | **REFUSED**, absent from the decided set | Task | same line |
| `packages/orchestration/project_registry.py:856` | 19 | `j` | **REFUSED**, absent from the decided set | Job | `job_map = {str(j.id): j for j in jobs}` |

MEASURED, NOT TAKEN FROM THE BLOCK: **2** of the five are CONFIRMED and **3** are REFUSED, and
2 + 3 = 5 against 5 columns. The ruled set holds all five, so the transform renames all five. The
decided set the control dumped holds **1908** of the 2185 ruled sites and the remaining **277**
are the stated blind spot, which is the partition the shipped stage's own banner prints.

THE CLASS MEASUREMENT. Over the corrected set: **2185** ruled sites on **2080** distinct
(path, line) pairs, **91** lines carrying more than one ruled site, and of those **26** on which
one SHARED owner verdict spans sites whose receiver identifiers DIFFER, **32** where the shared
verdict spans one receiver name and **33** where the verdicts DISAGREE. The two partitions close:
58 + 33 = 91 and 26 + 32 = 58. Zero sites on a multi-site line had an unreadable receiver. Both
lines behind the frames are IN the class; the third site carries one ruled column and is not a
multi-site line at all, so 16 of the 17 on-site frames sit on the class's two lines and 1 does
not — 16 + 1 = 17.

EVERY FIGURE THE BLOCK STATES REPRODUCED EXACTLY, so constraint 3's "your measurement is what the
artefact carries" bit nowhere this round: 2185, 2080, 91 and 26 all MATCH, and so does the whole
of round 80's handover re-derived from the pinned capture without quoting it — 30 records the
message rule admits, 24 the class rule admits, 6 rejected, 19 named and 5 `NoneType`, 17 on a
held site and 7 nowhere, over 3 distinct held sites.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f275-r81.md` | `cmp` against `.remedy-wt/r81_block.md` exit 0 with empty output; both 28740 bytes, sha256 `a1177ea46e337a169168c2b2c6e4fe63f57748e67af208c3396ee8cb67fc53fa` |
| PLAN81 | `.agent/plan.md` | byte-identical to the slice extracted from the COMMITTED C0a blob, 2808 bytes, sha256 `8a6d653acecb3343f262b6b6c8a8d1269c5c055a37783dc0aed874beccd248e4` |
| RECORD81 | `.agent/live_review.md` | byte-exact suffix of the post-commit file, reader A and reader B both accepting, 3571 bytes, sha256 `a81e402d0acb759914e07664f51d68cf59c81c569d66d9ca2db111e48c82a9ae` |
| SLIPS81 | `.agent/prose_slips.md` | the post-commit file equals the pre-commit blob followed by exactly the slice, 1341 bytes, sha256 `19ae53c395b461ede352f1f4e8bd0e3e2c45ccb54106bfac6114cf3b737706c1` |
| DEC81 | `.agent/decisions.md` | byte-exact suffix of the post-commit file, reader A and reader B both accepting, 4380 bytes, sha256 `da7da8c8c19f913f441fd0ebd4dfaa15cc0c9f010c67558ce5e7fa9b2be556bf` |

No slice was edited, reflowed or corrected, and no discrepancy inside a slice was found to
declare this round.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a block as authored text | done | |
| C0b last-block mirror | done | |
| C1 plan | done | |
| C2 ledger, the round 80 PASS verdict | done | |
| C3 prose slips | done | |
| C4 the fallback-class artefact | done | |
| C5 DECISION F275 D55 | done | appended; no landed DECISION rewritten, deletion column zero |
| C6 the handback | done | this commit |
| G1 · G2 · G3 | done | exit 0, exit 0, exit 0 |
| G4 · G5 | done | exit 0, exit 0 |
| G6 | done | exit 0; ruff itself exits 1 at 26 rows against the ceiling of 26, which is the expected code for a run AT the ceiling |
| G7(b) and G7(a)'s EXTRA half | done | exit 0 |
| G8 | done | exit 0 |
| G7(a) over the full range to C6 | deviated | unmeetable before C6 by its own wording; run immediately after C6, transcript `.remedy-wt/r81_g7_post.out`, real exit code in the round report |

## Deviations & assumptions

1. **G7(a) COULD NOT BE REPORTED INSIDE THE FILE ITS OWN SUBJECT CREATES.** Constraint 11 orders
   every gate except G7(a) run at C5 and then says G7(a) runs after C6; the gate's own text says
   the same. The half of G7(a) that IS decidable at C5 — EXTRA empty, no changed path under
   `packages/`, `apps/`, `tests/` or `docs/`, and MISSING exactly the one handoff path — was run
   at C5 and is quoted above with its real exit code, and the full-range reading is taken
   immediately after C6 with its transcript at `.remedy-wt/r81_g7_post.out` and its exit code
   relayed in the round report, where the reviewer re-runs it itself. Nothing was adjusted to
   route around this and no extra commit was made. This is the third round running in which the
   same path set forces the same split, which is exactly what the second SLIPS81 line predicts.

2. **I BUILT MY OWN BASE TREE AND DID NOT USE THE REVIEWER'S.** `.remedy-wt/r81_base` exists on
   disk and was left untouched. The tree the control ran over is `.remedy-wt/r81_base_worker`,
   built by the block's recipe from `git archive ef75e213` with `git init` and `git add -A -f`
   inside it, and the negative control's tree is `.remedy-wt/r81_noindex_worker`, the SAME
   extraction of the SAME archive with no `git init` at all. Both are named in G6(b) and neither
   is a registered worktree.

3. **THE CONTROL WAS RUN TWICE, BY TWO SCRIPTS, AND REPRODUCED BOTH TIMES.** A standalone
   `.remedy-wt/r81_control.py` ran it first while the recipe was being proved, and the gate-bearing
   run is the one inside `.remedy-wt/r81_instrument.py`, whose whole transcript is
   `.remedy-wt/r81_instrument.out`. The instrument was re-run as G4 after C5 and its output is
   BYTE-IDENTICAL to the saved transcript the artefact was built from; three back-to-back runs of
   the measurement gave one distinct sha256, so the listing of 26 class members is stable and not
   set-iteration order.

4. **TWO GATE SCRIPTS WERE RED ON THEIR FIRST RUN AND BOTH FAILURES WERE MINE, NOT THE SUBJECT'S.**
   G2's first run exited 1 with `FileNotFoundError` because it read the PLAN81 slice from a scratch
   path an earlier command had not actually written; it now re-extracts the slice from the
   COMMITTED C0a blob itself, which is strictly better than depending on a file beside it. G6's
   first run exited 8 because it counted ruff rows with a pattern written for an older ruff output
   format and read **0** rows against the ceiling of 26; this ruff prints a `--> <path>:<line>:<col>`
   location line per diagnostic, and the gate now counts those AND cross-checks them against ruff's
   own `Found N errors.` tally, which agree at 26. Both are stated here rather than hidden behind a
   clean transcript.

5. **A HAND-COUNTED NUMERAL WAS CAUGHT IN THE ARTEFACT'S DRAFT AND REMOVED BEFORE C4.** The draft
   said "eleven of the twenty-six members pair `pt` with `job` in one test module"; the enumeration
   the instrument prints shows NINE such members, and the sentence sat directly beside a measured
   category. It was replaced by wording that asserts no count and points the reader at the
   enumeration above it. Nothing false landed, and it is recorded here because it is the class of
   slip the ledger tracks rather than because it reached disk.

6. **NO OTHER DEVIATION.** The ordered commit sequence is exactly the block's, with nothing added,
   dropped or reordered; every commit staged exactly one path; no path outside the Change section
   was touched; the round 79 and round 80 artefacts were not edited, deleted or staged and are
   byte-identical at the base and at C5; no landed DECISION was rewritten and C5's deletion column
   is zero; nothing under `packages/`, `apps/`, `tests/` or `docs/` was touched, no suite beyond
   the canary was run and no transform was executed; every pinned input matched its digest and
   none was regenerated; no `.py` file was created anywhere inside the tracked tree and every
   script this round wrote lives under `.remedy-wt/` uncommitted; `.agent/STOP` was read before
   C0a, where it did not exist, and again before C6, where the reading is recorded in
   `.remedy-wt/r81_stop_pre_c6.out` with `REAL_EXIT=2` at `2026-09-12T16:17:21Z`. Only the second
   reading carries a wall-clock stamp, because the first was taken before the harness that writes
   one was in place; constraint 9's timestamp clause binds only if the sentinel appears, and it
   did not.

## Next

The reviewer re-runs the gates and issues the round 81 verdict.

Operator questions open: 0.

The next round DROPS THE TWO SITES DECISION F275 D55 NAMES from the flip's input and re-derives
the corrected set, which is a set subtraction and a re-key rather than a new measurement; then
THE RESOLVER COLLAPSE that DECISION F260 D5 places in T003 and DECISION F275 D37 names as the
home of the id-SHAPE seam — production code, so a SPLIT round with mutation red-proofs — and then
THE FLIP, in whose own commit the stale `_FakeJob` double at `packages/orchestration/project_registry.py:856`
is updated. `R-0880` stays OPEN: this round adds the first behavioural measurement of what the
fallback costs and two sites removed by name, and builds no refusal into the transform.
