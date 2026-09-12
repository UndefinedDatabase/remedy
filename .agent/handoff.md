# Handback — F275 round 79

## Session

`SESSION 28 of feature F275 · round 79 · rounds so far 79`

NO SCOPE REPORT AND NO SESSION-LIMIT BANNER IS OWED. Amendment amend0911-f275-to-scope, restored
to `docs/agents/self_drive_protocol.md` by round 78, lifts F275's soft limit of 20 sessions and
60 rounds without a replacement number, so this round prints no `SITZUNGS-LIMIT` line.

Context self-assessment: this worker ran one round, spent one twenty-minute suite pass inside it,
and has ample context left; nothing about the session boundary is forced by this round.

## Range

Review of `d3610730`..`HEAD` (the seven commits C0a–C5 plus this handback commit C6).

## Commits

### 38891491 F275 R79 C0a: save the round 79 block as authored text

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r79.md` | +371 / -0 | the block transported with `shutil.copyfile`, byte-identical to `.remedy-wt/r79_block.md` |

### 57fb2761 F275 R79 C0b: mirror the round 79 block into the last-block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +261 / -237 | rewritten from the COMMITTED C0a blob, not from any working copy |

### 973951a6 F275 R79 C1: make the plan current for round 79

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +20 / -21 | replaced by slice PLAN79, byte for byte; the first substantive commit, per constraint 6 |

### 012e4e63 F275 R79 C2: book the round 78 reviewer verdict

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +10 / -0 | slice RECORD79 appended; the round 78 PASS booked by the first substantive commit of round 79 |

### dc4bfdde F275 R79 C3: append the round 78 prose slips

| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +4 / -0 | slice SLIPS79 appended; two dated lines and no id, per amend0827 rule 2 |

### 3c9630ba F275 R79 C4: land the frame attribution artefact

| Path | +/- | Reason |
|---|---|---|
| `.agent/f275_t003_frame_attribution_r79.md` | +389 / -0 | written by the worker from its own run; the block ships no slice for it |

### 8cf18f84 F275 R79 C5: record DECISION F275 D53

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +16 / -0 | slice DEC79 appended; the attribution rule and the rebuild-under-a-control ruling |

### C6 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | measured by the next gate | the round 79 handback; a handoff cannot table the commit that writes it |

THE `+/-` CELLS ABOVE WERE READ FROM `git show --numstat` AND COMPARED CELL BY CELL AGAINST G8's
OWN NUMBERS. The comparison, printed: C0a 371/0 against 371/0 EQUAL; C0b 261/237 against 261/237
EQUAL; C1 20/21 against 20/21 EQUAL; C2 10/0 against 10/0 EQUAL; C3 4/0 against 4/0 EQUAL; C4
389/0 against 389/0 EQUAL; C5 16/0 against 16/0 EQUAL. Seven of seven cells pairs equal, zero
differ. Every commit staged exactly ONE path and every insertion count is under 500.

## External actions

| Command | Outcome |
|---|---|
| `git push -u origin feature/f275-one-world-completion-part-three` | run after C6; result in the round report |
| `git worktree add` | NOT RUN. The tree was built as an unregistered copy, so `git worktree list` still shows the primary checkout alone |
| `gh` / `remedy` | NOT RUN, per constraint 8. No pull request created, edited or merged; no branch created or deleted; no merge, no force-push, no history rewrite |

## Verification

Every gate wrote its own transcript under `.remedy-wt/` and the exit code below was read back out
of that file, not out of the process that ran it.

| Gate | Transcript | REAL exit code | Decisive reading |
|---|---|---|---|
| G1 transport, budget, slices | `.remedy-wt/r79_g1.txt` | `EXIT=0` | `cmp` exit 0; C0a blob 31699 bytes equal to the scratch original; `last_block.md` equal to the COMMITTED blob; SLICE CARDINALITY MEASURED 4, all four matching their own BEGIN digest; TOTAL 371 against the cap of 490 and PROSE 294 against 400; repeated-character lines outside a slice 0 |
| G2 the plan | `.remedy-wt/r79_g2.txt` | `EXIT=0` | `.agent/plan.md` at C1 byte-identical to PLAN79; 47 lines, at most 50; exactly one `## Goal` and one `## Next Steps` |
| G3 the record, full forensics | `.remedy-wt/r79_g3.txt` | `EXIT=0` | reader A holds for both appends; reader B holds at N counted from the slice as 5 and 8; both negative controls, flipped inside the FIRST appended paragraph, rejected by BOTH readers, with the unmutated controls accepted; deletion columns 0, 0 and 0; `prose_slips.md` equals its pre-commit blob followed by exactly SLIPS79; the `Gate:` header pattern derived from 100 prior headers matches 100 of 100 and matches RECORD79, duplicating none |
| G4(a) the tree before the transform | `.remedy-wt/r79_g4a.txt` | `EXIT=0` | 994 tracked `.py` files compared against `ef75e213`, 0 differing, 0 missing, path lists equal |
| G4(b) the transform control | `.remedy-wt/r79_g4b.txt` | `EXIT=0` | per-line diff of the two summaries EMPTY, 24 rule rows equal row for row, argument vector reported |
| G4(c)(d) totals and artefacts | `.remedy-wt/r79_g4cd.txt` | `EXIT=0` | bad nodes 1204 round 77 against 1207 round 79, difference +3 which is 0.25 per cent; every `.remedy-wt/r79_*` file present; the built tree present and pinned |
| G5 the artefact | `.remedy-wt/r79_g5.txt` | `EXIT=0` | committed blob byte-identical to the file the run produced; base lookup exit 128; 224 indented lines matched MONOTONE with strictly increasing indices and 0 unmatchable; 0 wall-clock lines and 0 three-backtick lines; all named sections present |
| G6(a) the tree is clean | `.remedy-wt/r79_g6a.txt` | `EXIT=0` | `git status --porcelain` printed the EMPTY STRING at C5 |
| G6(b) worktrees | `.remedy-wt/r79_g6b.txt` | `EXIT=0` | one line, the primary checkout at `8cf18f84`; no registered worktree was created, so none was removed or pruned |
| G6(c) THE CANARY | `.remedy-wt/r79_g6c.txt` | `EXIT=0` | `42 passed`, against the 42 the reviewer measured at this round's base |
| G6(d) ruff | `.remedy-wt/r79_g6d_ruff.txt` | `EXIT=1` | `Found 26 errors.` — 26 rows against the frozen ceiling of 26. Ruff exits non-zero whenever it reports a row, so exit 1 is the expected code for a run AT the ceiling, and it is the same code round 77's transcript carries |
| G6(d) the sweep | `.remedy-wt/r79_g6d.txt` | `EXIT=0` | the ruff row count read back as 26 against the ceiling, and a FILESYSTEM sweep finding 0 `.py` files anywhere under `.agent/` |
| G7(b) the open set | `.remedy-wt/r79_g7b.txt` | `EXIT=0` | 87 open by distinct id at the base and 87 at C5, membership difference EMPTY both ways, `R-0880` OPEN at both readings |
| G7(a) the path set | `.remedy-wt/r79_g7a.txt` | run AFTER C6 — see the deviation below | its subject includes `.agent/handoff.md`, which C6 alone creates |
| G8 the insertion cap | `.remedy-wt/r79_g8.txt` | `EXIT=0` | C0a 371, C0b 261, C1 20, C2 10, C3 4, C4 389, C5 16 — every one under 500, every commit one path |

THE CONTROL THAT GUARDED THE EXPENSIVE STEP. The transform was re-run over the rebuilt tree before
the suite was touched and its summary reproduced `.remedy-wt/r77_tf_corr.out` exactly: 2185 ruled
keys all resolving with none NOT resolving, 263 files rewritten, 0 skipped unparsable, 0 left
alone as would-break, 6078 total rewrites, and the per-rule table equal row for row. The
argument vector, which the block deliberately did not name, was
`python3 -B .remedy-wt/r69_flip_transform_guarded.py .remedy-wt/r79_tree
.remedy-wt/r77_corrected.json .remedy-wt/r77_corrected_owners.json .remedy-wt/r61_status.json`.
The fourth argument was found in round 69's own guard-test script, and the reproduction is the
evidence that it is the right one.

THE READING THE ROUND EXISTS TO PRODUCE. Thirty `AttributeError` records name a unified
attribute — 25 on a named receiver class and 5 on `NoneType`. Every one of the thirty has a frame
inside the built tree, so the UNATTRIBUTABLE set is EMPTY. SEVENTEEN of the thirty land on a
ruled site the corrected set holds and THIRTEEN land nowhere in it. Twelve of the seventeen are
one site, `tests/cli/test_repair_runtime.py:68`, and the other held sites are
`packages/orchestration/brain_detail.py:345` with four and
`packages/orchestration/project_registry.py:856` with one.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f275-r79.md` | `cmp` against `.remedy-wt/r79_block.md` exit 0; both 31699 bytes, sha256 `74a527df…0ca851dd` |
| PLAN79 | `.agent/plan.md` | byte-identical to the slice extracted from the COMMITTED C0a blob, 2732 bytes, sha256 `f2339a78…684235c2` |
| RECORD79 | `.agent/live_review.md` | byte-exact suffix of the post-commit file, 4821 bytes, sha256 `959bf44b…91a25290` |
| SLIPS79 | `.agent/prose_slips.md` | the post-commit file equals the pre-commit blob followed by exactly the slice, 2123 bytes, sha256 `cc0134f8…4a0c70435`[^1] |
| DEC79 | `.agent/decisions.md` | byte-exact suffix of the post-commit file, 4134 bytes, sha256 `f117f403…7a9260b53`[^1] |

[^1]: the full digests are in `.remedy-wt/r79_g1.txt`; the tails are elided here only in this table.

No slice was edited, reflowed or corrected, and no discrepancy was found in any of the four.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a block as authored text | done | |
| C0b last-block mirror | done | |
| C1 plan | done | |
| C2 ledger, the round 78 verdict | done | |
| C3 prose slips | done | |
| C4 the attribution artefact | done | |
| C5 DECISION F275 D53 | done | |
| C6 the handback | done | this commit |
| G1 · G2 · G3 | done | exit 0, exit 0, exit 0 |
| G4(a) · G4(b) · G4(c)(d) | done | exit 0, exit 0, exit 0 |
| G5 · G6(a) · G6(b) · G6(c) | done | exit 0, exit 0, exit 0, exit 0 |
| G6(d) | done | ruff exit 1 at 26 rows against the ceiling of 26; the sweep exit 0 |
| G7(b) · G8 | done | exit 0, exit 0 |
| G7(a) | deviated | unmeetable before C6 by its own wording; run immediately after C6, transcript `.remedy-wt/r79_g7a.txt`, real exit code in the round report |

## Deviations & assumptions

1. **G7(a) COULD NOT BE REPORTED INSIDE THE FILE ITS OWN SUBJECT CREATES.** The block orders G7(a)
   run AFTER C6 and also orders every gate reported in the handback, which C6 writes. The two
   cannot both hold for this one gate: its transcript does not exist while this file is being
   written. The gate is run immediately after C6, its transcript is `.remedy-wt/r79_g7a.txt`, and
   its real exit code and readings are relayed in the round report, where the reviewer re-runs it
   itself. Nothing was adjusted to route around this and no extra commit was made; the block's
   ordered sequence is intact. This is the same class as the round 78 slip the SLIPS79 slice
   records, now narrowed to the one gate the block deliberately placed after C6.
2. **THE SELECTED NODE SET IS 30 NODES WIDER THAN ROUND 77's, AND THE REASON IS THE INVOCATION.**
   Rounds 76 and 77 ran pytest against `tests` alone; this round ran it at the tree's root, which
   additionally collects the vendored sample project under `scripts/gauntlet_sample_project/`. All
   thirty extra nodes passed and none is a bad node, so the bad-node comparison is unaffected. The
   difference was measured with a collect-only pass against round 76's saved listing rather than
   asserted. That collect-only pass is an EXTRA measurement the block did not order; it runs no
   test and was taken only to explain a numeral the gate asked me to state.
3. **THREE BAD NODES ARE THIS ROUND's AND NOT ROUND 77's, AT 0.25 PER CENT.** G4(c) obliges a
   declaration above five per cent and this is below it, but the cause was measured and is stated
   anyway. All three read the repository's own git history — a head sha and a list of deleted
   modules — and the tree this round built is a fresh `git init` over an extracted archive with no
   commit in it. That is a property of how the tree was built, not of the ruled site set. None of
   the three is an `AttributeError` on a unified attribute, so none enters the attribution.
4. **THE CAPTURE USED A REPORTING-ONLY PYTEST PLUGIN.** The block ordered FULL TRACEBACKS and did
   not name a mechanism. The run used `--tb=long` AND a plugin loaded with `-p` off a PYTHONPATH
   entry holding that one file, which records each failure's raw frame list as JSON. The plugin
   lives under `.remedy-wt/r79_plugin/`, never inside the tree and never committed, so the tree
   the suite ran against is exactly the transformed tree G4(a) and G4(b) pin. Its own error-record
   count is zero. It was smoke-tested on one test file before the twenty-minute pass was spent.
5. **`.remedy-wt/r79_*` HOLDS A FEW FILES THIS WORKER DID NOT WRITE.** G4(d) lists the whole glob
   for completeness; `r79_probe_inputs.py`, `r79_recon*.py` and `r79_stamp.py` are the reviewer's
   own pre-authoring probes and predate the delegation. Everything else under that glob is this
   round's.
6. **NO OTHER DEVIATION.** The ordered commit sequence is exactly the block's, with nothing added,
   dropped or reordered; every commit staged exactly one path; no path outside the Change section
   was touched; `.agent/STOP` was read before C0a and again before C6 and did not exist at either
   reading, at `2026-09-12T16:38:19` and `2026-09-12T17:21:50`.

## Next

The reviewer re-runs the gates and issues the round 79 verdict.

Operator questions open: 0.

The next round is THE RESOLVER COLLAPSE that DECISION F260 D5 places in T003 and DECISION F275 D37
names as the home of the id-SHAPE seam — production code, so a SPLIT round with mutation
red-proofs — and then THE FLIP itself, whose input set DECISION F275 D51 rules and which this
round's table now lets a later decision narrow by up to seventeen frames' worth of sites, with the
thirteen unheld frames named as a separate defect rather than folded in. `R-0880` stays OPEN: its
second obligation now has its measurement, and whether the transform gains a refusal is a later
decision taken with the table in hand.
