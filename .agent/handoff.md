# Handback — F275 round 80

## Session

`SESSION 28 of feature F275 · round 80 · rounds so far 80`

NO SCOPE REPORT AND NO SESSION-LIMIT BANNER IS OWED. Amendment amend0911-f275-to-scope lifts
F275's soft limit of 20 sessions and 60 rounds without a replacement number, so this round prints
no `SITZUNGS-LIMIT` line.

Context self-assessment: this worker ran one repair round, spent no suite pass beyond the canary
inside it, and has ample context left; nothing about the session boundary is forced by this round.

## Range

Review of `c7ac5e00`..`HEAD` (the seven commits C0a–C5 plus this handback commit C6).

## Commits

### c51c679d F275 R80 C0a: save the round 80 step block as authored text

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r80.md` | +353 / -0 | the block transported with `shutil.copyfile`, byte-identical to `.remedy-wt/r80_block.md` |

### 12246ef0 F275 R80 C0b: mirror the round 80 block into the last-block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +201 / -219 | rewritten from the COMMITTED C0a blob, not from any working copy |

### 9522f2e9 F275 R80 C1: make the plan current for round 80

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +13 / -12 | replaced by slice PLAN80, byte for byte; the first substantive commit, per constraint 6 |

### 979f3c47 F275 R80 C2: book the round 79 reviewer verdict

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +10 / -0 | slice RECORD80 appended; the round 79 FAIL booked by the first substantive commit of round 80 |

### 3b3cd657 F275 R80 C3: append the round 79 prose slips

| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +4 / -0 | slice SLIPS80 appended; two dated lines and no id, per amend0827 rule 2 |

### 01293a06 F275 R80 C4: land the corrected attribution artefact

| Path | +/- | Reason |
|---|---|---|
| `.agent/f275_t003_frame_attribution_r80.md` | +319 / -0 | written by the worker from its own run; a NEW document beside the round 79 one, which is not edited |

### bbbfd728 F275 R80 C5: record DECISION F275 D54

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +16 / -0 | slice DEC80 APPENDED; DECISION F275 D53 is not rewritten and the deletion column is zero |

### C6 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | measured by the next gate | the round 80 handback; a handoff cannot table the commit that writes it |

THE `+/-` CELLS ABOVE WERE READ FROM `git show --numstat` AND COMPARED CELL BY CELL AGAINST G8's
OWN NUMBERS. The comparison, printed: C0a 353/0 against 353/0 EQUAL; C0b 201/219 against 201/219
EQUAL; C1 13/12 against 13/12 EQUAL; C2 10/0 against 10/0 EQUAL; C3 4/0 against 4/0 EQUAL; C4
319/0 against 319/0 EQUAL; C5 16/0 against 16/0 EQUAL. Seven of seven cell pairs equal, zero
differ. Every commit staged exactly ONE path and every insertion count is under 500.

## External actions

| Command | Outcome |
|---|---|
| `git push -u origin feature/f275-one-world-completion-part-three` | run after C6; result in the round report |
| `git worktree add` / `git worktree remove` | NOT RUN. `git worktree list` shows the primary checkout alone, and `.remedy-wt/r79_tree` is an unregistered copy that was READ and neither rebuilt nor deleted, per constraint 5 |
| `gh` / `remedy` | NOT RUN, per constraint 8. No pull request created, edited or merged; no branch created or deleted; no merge, no force-push, no history rewrite |

## Verification

Every gate wrote its own transcript under `.remedy-wt/` and the exit code below was read back out
of that file with a reader that greps `REAL_EXIT=`, not out of the process that ran it.

| Gate | Transcript | REAL exit code | Decisive reading |
|---|---|---|---|
| G1 transport, budget, slices | `.remedy-wt/r80_g1.txt` | `REAL_EXIT=0` | `cmp` exit 0 BOTH ways — the committed C0a blob against the scratch original and the worktree file against it; C0a 28559 bytes; `last_block.md` byte-identical to the COMMITTED C0a blob; SLICE CARDINALITY MEASURED **4**, every one matching the sha256 on its own BEGIN marker; TOTAL **353** against the cap of 490 and PROSE **275** against 400, both agreeing with constraint 10; repeated-character lines outside a slice **0** |
| G2 the plan | `.remedy-wt/r80_g2.txt` | `REAL_EXIT=0` | `.agent/plan.md` at C1 byte-identical to PLAN80, 2935 bytes; 48 lines, at most 50; exactly one `## Goal` and one `## Next Steps` |
| G3 the record, full forensics | `.remedy-wt/r80_g3.txt` | `REAL_EXIT=0` | reader A holds for both appends with the arithmetic printed; reader B holds at N COUNTED FROM THE SLICE as 5 for RECORD80 and 8 for DEC80; both negative controls — one ASCII letter flipped inside the FIRST appended paragraph, `G`→`H` and `D`→`E` — REJECTED by BOTH readers; deletion columns 0, 0 and 0; `prose_slips.md` equals its pre-commit blob followed by exactly SLIPS80; the `Gate:` header pattern DERIVED from the ledger, `^Gate: F\d+ R\d+ — `, matches **101 of 101** prior headers and matches RECORD80, duplicating none byte for byte |
| G4 the corrected reading | `.remedy-wt/r80_g4.txt` | `REAL_EXIT=0` | all four pinned inputs MATCH their stated size and digest; the instrument diff is **3 hunks, +135 / −7**, and every one of the seven removed lines is printed — two are the predicate's own replaced lines, five are the withdrawn narrative, and **0** are attribution-pipeline lines; the counts re-derived WITHOUT the instrument agree with its output on all five figures; both PARTITIONS hold; the CROSS-CHECK against `.agent/f275_t003_flip_residue_r77.md` is MATCH at 19 and the per-kind mappings are EQUAL; every moved row is UNHELD and the ON-site half moved by `+0` |
| G5 the artefact | `.remedy-wt/r80_g5.txt` | `REAL_EXIT=0` | committed blob byte-identical to the file the run produced, 22048 bytes; the base lookup `git cat-file -e c7ac5e00:…r80.md` exit **128**, the path's absence at the base; **175** indented non-blank lines compared, 175 matched MONOTONE with strictly increasing indices, **0 unmatchable**, first match output line 4 and last output line 287; **0** wall-clock lines and **0** three-backtick lines; all six named sections present in the block's order; the round 79 artefact byte-identical at base, at C5 and on disk, and ABSENT from the changed-path set |
| G6 tree, colours, path set | `.remedy-wt/r80_g6.txt` | `REAL_EXIT=0` | `git status --porcelain` printed the EMPTY STRING at C5 and again after the canary and ruff; `git worktree list` one row, the primary checkout; `.remedy-wt/r79_tree` present with 65181 entries; THE CANARY `python3 -B -m pytest tests/cli/test_golden_path.py -q` exit 0, **42 passed** against the 42 the reviewer measured at the base; `ruff check .` exit **1** by its own design, **26** location rows cross-checked against its own `Found 26 errors.` tally, at the frozen ceiling of 26; a FILESYSTEM sweep finding **0** `.py` files anywhere under `.agent/` |
| G7 path set and open set | `.remedy-wt/r80_g7_pre.txt` | `REAL_EXIT=0` | G7(b): **87** open BY DISTINCT ID at the base and 87 at C5, membership difference EMPTY both ways, `R-0880` OPEN at both; the CANONICAL line-count reading of `scripts/rotate_live_review.count_open_findings`, imported from the shipped file, is **85** at both, so the GAP is **2** at both and DID NOT GROW — it is R-0721 and R-0725, each carrying two `Done:` lines. G7(a) at this mode: EXTRA is already EMPTY and MISSING is exactly `.agent/handoff.md`, the one path C6 alone creates; changed paths under `packages/`, `apps/`, `tests/` or `docs/`: **0** |
| G7(a) over the full range | `.remedy-wt/r80_g7_post.txt` | run AFTER C6 — see deviation 1 | its subject includes `.agent/handoff.md`, which C6 alone creates |
| G8 the insertion cap | `.remedy-wt/r80_g8.txt` | `REAL_EXIT=0` | C0a 353, C0b 201, C1 13, C2 10, C3 4, C4 319, C5 16 — every one under 500, every commit exactly one path |

THE CORRECTED READING, WHICH IS WHAT THIS ROUND EXISTS FOR. Over the pinned capture the MESSAGE
rule admits **30** records, the CLASS rule admits **24** and REJECTS **6**; the corrected set is
**19** on a named receiver class and **5** on `NoneType`. All six rejected records carry the class
`AssertionError`, all six are nodes of `tests/orchestration/test_orchestrator_loop.py`, and every
one of them names `_FakeJob.job_id` inside an assertion's own text. The corrected named-class
count of 19 equals the figure `.agent/f275_t003_flip_residue_r77.md` records for that class, and
so does every per-kind count: `Artifact.job_id` 12, `BrainNode.task_id` 5, `BrainNode.job_id` 1,
`_FakeJob.job_id` 1. Round 79's larger number was the predicate, not the population.

THE ATTRIBUTION SPLIT, ROUND 80 BESIDE ROUND 79. Selected records 24 against round 79's 30;
attributed to an in-tree frame 24 against 30; unattributable 0 against 0; landing ON a ruled site
the corrected set holds **17 against round 79's 17**; landing NOWHERE in the corrected set **7
against round 79's 13**; distinct frame groups 8 against 14. Round 79's own numbers were
RECOMPUTED here from the same pinned records rather than quoted, and then cross-checked against
the figures round 79 printed — 17, 13 and 14 all MATCH. Six rows moved, every one of them a single
`_FakeJob.job_id` frame on an assertion line of `tests/orchestration/test_orchestrator_loop.py` at
lines 1513, 1524, 1765, 1776, 1825 and 1833, and every one of them UNHELD. The three held sites
and their frame counts are unchanged: `tests/cli/test_repair_runtime.py:68` with twelve,
`packages/orchestration/brain_detail.py:345` with four and
`packages/orchestration/project_registry.py:856` with one.

THE SELECTION PREDICATE'S CHANGE, AS A UNIFIED DIFF. This is the whole of the correction; the
instrument is round 79's with one condition added and it lives under `.remedy-wt/`, uncommitted.

    --- .remedy-wt/r79_instrument.py
    +++ .remedy-wt/r80_instrument.py
    -attr_recs = []
    +msg_recs, attr_recs, excluded = [], [], []
     for r in recs:
         m = ATTR.search(r.get("msg") or "")
         if m and m.group(2) in UNIFIED:
    -        attr_recs.append((r, m.group(1), m.group(2)))
    +        msg_recs.append((r, m.group(1), m.group(2)))
    +        if r.get("cls") == "AttributeError":
    +            attr_recs.append((r, m.group(1), m.group(2)))
    +        else:
    +            excluded.append((r, m.group(1), m.group(2)))

The corrected instrument was DERIVED from round 79's by a script of literal old-to-new string
replacements, `.remedy-wt/r80_make_instrument.py`, each required to match exactly once, so the
derivation is re-runnable by the reviewer against the pinned round 79 file.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f275-r80.md` | `cmp` against `.remedy-wt/r80_block.md` exit 0; both 28559 bytes, sha256 `286222dd…bca19c0` |
| PLAN80 | `.agent/plan.md` | byte-identical to the slice extracted from the COMMITTED C0a blob, 2935 bytes, sha256 `3e6374ad…a2888e97` |
| RECORD80 | `.agent/live_review.md` | byte-exact suffix of the post-commit file, 3772 bytes, sha256 `3fbcd97a…b96b0723b`[^1] |
| SLIPS80 | `.agent/prose_slips.md` | the post-commit file equals the pre-commit blob followed by exactly the slice, 1446 bytes, sha256 `0c0ce3ed…084d34a8` |
| DEC80 | `.agent/decisions.md` | byte-exact suffix of the post-commit file, 3758 bytes, sha256 `6f653725…a0a255e3`[^1] |

[^1]: the full digests are in `.remedy-wt/r80_g1.txt` and `.remedy-wt/r80_g3.txt`; the tails are elided here only in this table.

No slice was edited, reflowed or corrected. One discrepancy inside a slice was measured and is
declared below as deviation 3; the slice still landed exactly as written.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a block as authored text | done | |
| C0b last-block mirror | done | |
| C1 plan | done | |
| C2 ledger, the round 79 FAIL verdict | done | |
| C3 prose slips | done | |
| C4 the corrected attribution artefact | done | |
| C5 DECISION F275 D54 | done | appended; D53 untouched, deletion column zero |
| C6 the handback | done | this commit |
| G1 · G2 · G3 | done | exit 0, exit 0, exit 0 |
| G4 · G5 | done | exit 0, exit 0 |
| G6 | done | exit 0; ruff itself exits 1 at 26 rows against the ceiling of 26, which is the expected code for a run AT the ceiling |
| G7(b) and G7(a)'s EXTRA half | done | exit 0 |
| G8 | done | exit 0 |
| G7(a) over the full range to C6 | deviated | unmeetable before C6 by its own wording; run immediately after C6, transcript `.remedy-wt/r80_g7_post.txt`, real exit code in the round report |

## Deviations & assumptions

1. **G7(a) COULD NOT BE REPORTED INSIDE THE FILE ITS OWN SUBJECT CREATES.** Constraint 11 orders
   every gate run at C5, strictly before C6, so the handback can quote it; G7(a) orders its own
   reading taken AFTER C6, "unlike every other gate", because its subject includes a path C6 alone
   creates. The two cannot both hold for this one gate. What was done: the half of G7(a) that is
   decidable at C5 — EXTRA empty, no changed path under `packages/`, `apps/`, `tests/` or `docs/`,
   and MISSING exactly the one handoff path — was run at C5 and IS quoted above with its real exit
   code, and the full-range reading is taken immediately after C6 with its transcript at
   `.remedy-wt/r80_g7_post.txt` and its exit code relayed in the round report, where the reviewer
   re-runs it itself. Nothing was adjusted to route around this, no extra commit was made, and the
   block's ordered sequence is intact. This is the same class as round 79's declared deviation 1.

2. **THE CORRECTED INSTRUMENT REMOVES FIVE PRINTED LINES BEYOND THE BARE CONDITION, AND THAT IS A
   JUDGEMENT I MADE.** Constraint 2 forbids changing what the instrument prints beyond what the
   added condition and the two new sections require. Round 79's instrument printed five HARD-CODED
   narrative lines asserting that the fresh capture read six more named-class nodes than round 77
   and that the gap was what the earlier transcript could show rather than a different population.
   The added condition makes that sentence false — it is the exact sentence DECISION F275 D54
   withdraws — so leaving it would have made the saved output contradict its own counts and would
   have put a false paragraph in the file G5(b) quotes against. I read that removal as inside "what
   the added condition requires" and replaced the five lines with measured ones: round 77's
   recorded figure read out of its own CORRECTED arm, the cross-check against it, the per-kind
   comparison, and a named statement that round 79 printed a claim here which D54 withdraws. G4(b)
   prints every removed line so the reviewer can see the whole of it; no line of the attribution
   pipeline was removed and the diff's removed set is seven lines in total. If the reviewer reads
   constraint 2 more strictly than I did, this is the finding to write.

3. **RECORD80 AND DEC80 SAY "1238 RECORDS"; THE MESSAGE RULE IS APPLIED TO 1237.** Measured:
   `.remedy-wt/r79_frames.jsonl` holds **1238** non-blank JSON lines, of which **1237** carry
   `"kind": "runtest"` and **one** carries `"kind": "sessionfinish"`. The selection runs over the
   1237 runtest records — round 79's instrument prints `traceback records captured: 1237` and so
   does the corrected one. So "of 1238 records the message rule admits 30" is exact if "records"
   means the capture file's records and loose if it means the records the rule sees; every derived
   figure in both slices — 30, 24, 19, 5, 6 — reproduced exactly. Per constraint 1 the slices
   landed byte for byte and were not corrected.

4. **THE INSTRUMENT'S `PRODUCED THIS ROUND` TAG IS ROUND 79's AND IS CARRIED UNCHANGED.** Four
   inputs are tagged `PRODUCED THIS ROUND` in the digest table because that list is round 79's own
   and constraint 2 forbids retuning it. In round 80 nothing in that table was produced: no suite,
   no transform and no tree build ran. The artefact says so in its own prose directly above the
   table rather than leaving the tag to mislead.

5. **TWO GATE SCRIPTS WERE CORRECTED BEFORE THE RECORDED RUN, AND BOTH FIRST RUNS WERE RED.** G6's
   first run counted ruff rows with a pattern written for an older ruff output format and read
   **0** rows against the ceiling of 26, so G6 exited 1; this ruff prints `--> <path>:<line>:<col>`
   location lines, and the gate now counts those AND cross-checks them against ruff's own
   `Found N errors.` tally, which agree at 26. G7's first run raised `AttributeError` importing
   `scripts/rotate_live_review.py` by file path, because `dataclasses` needs the module registered
   in `sys.modules` first; the gate now registers it and imports the shipped
   `count_open_findings` rather than re-implementing it. Both failures were in my measuring
   instruments, not in the thing measured, and both are stated here rather than hidden behind a
   clean transcript.

6. **NO OTHER DEVIATION.** The ordered commit sequence is exactly the block's, with nothing added,
   dropped or reordered; every commit staged exactly one path; no path outside the Change section
   was touched; `.agent/f275_t003_frame_attribution_r79.md` was not edited, deleted or staged and
   is byte-identical at the base, at C5 and on disk; DECISION F275 D53 was not rewritten and C5's
   deletion column is zero; no suite, transform or tree build was re-run and every pinned input
   matched its digest; `.agent/STOP` was read before C0a and again before C6 and did not exist at
   either reading, at `2026-09-12T15:34:02Z` and `2026-09-12T15:49:07Z`.

## Next

The reviewer re-runs the gates and issues the round 80 verdict.

Operator questions open: 0.

The next round is THE RESOLVER COLLAPSE that DECISION F260 D5 places in T003 and DECISION F275 D37
names as the home of the id-SHAPE seam — production code, so a SPLIT round with mutation
red-proofs — and then THE FLIP itself, whose input set DECISION F275 D51 rules and which a later
decision may narrow by the three held sites this corrected table names, with the seven unheld
frames kept as a separate defect rather than folded in. `R-0880` stays OPEN: its second obligation
now has a corrected measurement behind it, and whether the transform gains a refusal is a later
decision taken with the corrected table in hand.
