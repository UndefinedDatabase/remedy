# Handback — F033 · ROUND 19 · the run report's task line tells a mixed apply state apart

> Written by the WORKER of round 19. The reviewer writes the verdict; this file
> reports what was run and what it printed. This round registered NO finding of its
> own — R-0746 arrived in the reviewer's authored RECORD19 slice — and it wrote ONE
> `Landed:` line, for R-0746, and no `Done:` line for anything.

## Session

SESSION 5 of feature F033 · round 19 · rounds so far 19.
The soft limit is NOT reached: 19 rounds of 25, 5 sessions of 7.

## Fortschritt

~94 % (T001 and T002 complete. T003: the fold's partial truth and the popover label
landed in round 16, the tasks-card row in round 17, the fold's shared home and its
counts in round 18. THIS round built R-0738's THIRD and last surface — the run
report's own task line — and fixed R-0746 in the same round that gives the shared
fold its second importer. Rejection reasons quoted into the repair prompt remain, and
R-0738 is now RESOLVABLE but is NOT resolved here) — Schätzung.

## Range

Review of `41b83021`..`191da989` for the gated work — every gate below ran at a commit
no later than C6 — plus the two commits that cannot be inside it: C7, which writes this
file, and C8, which records the real push outcome after the push.
Branch `feature/f033-hunk-approval-v2`.

## Bundle item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block to `.agent/authored/f033-r19.md` | done | |
| C0b mirror it into `.agent/last_block.md` | done | |
| C1 `.agent/plan.md` <- PLAN19 | done | |
| C2 `.agent/live_review.md` <- RECORD19 | done | registers R-0746 |
| C3 `.agent/prose_slips.md` <- SLIPS19 | done | |
| C4 the report's apply state, its attach and its line (SPEC A) | done | |
| C5 the report's tests (SPEC B) | done | |
| C6 R-0746: the public API list and its guard (SPEC C) | deviated | see D2 — the guard SPEC C2 orders is red unless a SECOND unlisted public function is listed too |
| C7 `.agent/handoff.md` <- this handback | done | |
| C8 `.agent/handoff.md` <- the push outcome | done | recorded after the push |

## Commits

Every `+/-` cell below was taken from the SAME `git diff --numstat` run G8 reports and
compared to it cell by cell; they agree. No cell was filled from a file's own line count.

### a8a204fc docs(f033): save the round 19 block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f033-r19.md` | +351 -0 | C0a — the reviewer's block, byte for byte |

### a5f620cf docs(f033): mirror the round 19 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +215 -237 | C0b — same bytes, one blob id with C0a |

### d760fa89 docs(f033): advance the plan to round 19
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +17 -18 | C1 — PLAN19 replaces the file whole (checklist item 23) |

### e057697d docs(f033): book the round 18 verdict and register R-0746
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +4 -0 | C2 — RECORD19 appended; amend0827 rule 1 |

### bab89ad4 docs(f033): append the two round 18 prose slips
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/prose_slips.md` | +4 -0 | C3 — SLIPS19 appended; amend0827 rule 2 |

### cd7cd9c0 feat(f033): render a task apply state in the run report
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/run_report.py` | +112 -0 | SPEC A — `TaskOutcome` gains `apply_state`, `applied_changes` and `total_changes`; `APPLY_STATE_LABELS` and `_apply_clause`; `_folded_apply_states` and `_tasks_with_apply_state` behind `build_report_sources` |

### a8076e17 test(f033): pin the report task line apply clause and its attach
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_run_report.py` | +154 -1 | SPEC B — `TestTheTaskLineTellsAMixedApplyStateApart` and `TestTheApplyStateIsAttachedByTheFullTaskId`, nine tests; the one deletion is the `loop_run` import line gaining `proof_chain` |

### 191da989 fix(f033): name every public function in the proof chain API list
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2 -0 | C6 — the one `Landed: R-0746` line constraint 3 orders, and nothing else about it |
| `packages/orchestration/proof_chain.py` | +2 -0 | SPEC C1 — the `Public API::` block; see D2 for why it is two lines and not one |
| `tests/orchestration/test_run_report.py` | +47 -0 | SPEC C2 — `TestTheProofChainModuleDocumentsItsWholePublicApi`, the AST guard, plus `_public_api_block` and the `ast`/`pathlib` imports it needs |

### C7 and C8 (this file)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | see below | C7 writes this handback; C8 appends the real push outcome. A handoff cannot table the commit that writes it (R-0149 pattern). |

## External actions

- `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/r19/wt 191da989`
  -> REAL exit 0, "Preparing worktree (detached HEAD 191da989) / HEAD is now at
  191da989".
- `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/r19/wt` -> REAL exit 0, no
  output. `git worktree list` afterwards shows only `/home/decodeux/Repos/remedy`.
- `git push` — see the PUSH OUTCOME section at the bottom, written by C8.
- No `gh` command was run and no PR was created or merged. F033 is not closed and the
  PR belongs to the closure sequence.

## Verification — one line per gate, real exit codes

G1 HYGIENE AND THE STOP FILE — `ls -la /home/decodeux/Repos/remedy/.agent/STOP` REAL exit
2, printing exactly `ls: cannot access '/home/decodeux/Repos/remedy/.agent/STOP': No such
file or directory`, so the sentinel does not exist; `git status --porcelain` before C0a
REAL exit 0 printing NOTHING, and again after C6 REAL exit 0 printing NOTHING.

G2 TRANSPORT — REAL exit 0. Applied region vs the digest stamped in each slice's own
BEGIN marker: PLAN19 whole-file region at `d760fa89`, 2740 bytes, sha256
`8e33f449d67de9ab27f6d8f79f797fc4038b8ad176966aee40143abf2ad3baf4` MATCHES; RECORD19
last-8021-byte region at `e057697d`, sha256
`7f6d3ccb1526a4a731ac9ba4fdce26709327d6f0c55bbdfc0706cd2b8ac2ecc2` MATCHES; SLIPS19
last-1047-byte region at `bab89ad4`, sha256
`44aa61fab7ee3c5bbca05327fcb81d8609024922fc8a0e4254d0326d9a1e8601` MATCHES. Each region
was additionally compared to the slice RE-EXTRACTED from the block and is byte-EQUAL to
it. The C0a and C0b blobs are ONE id, `c92af81fe11a00779dd0c9537ebda796ba77334c`, 30045
bytes, sha256 `a297618f33a2f38ad327070cef9ffb490de654193197b3267f8a634cd0253789`, the
digest the round order named; `cmp .agent/authored/f033-r19.md .remedy-wt/r19/BLOCK.md`
and the same `cmp` for `.agent/last_block.md` were SILENT at REAL exit 0. THIS PROVES THE
SAVED COPY, ITS MIRROR AND THE WORKING COPY AGREE; IT IS NOT A CLAIM ABOUT THE BYTES THAT
WERE EMITTED. See D4 for why each append's region is read at the commit that applied it.

G3 THE RECORD APPEND at C2 — REAL exit 0, all three readings. (a) BYTES: pre-commit blob
1555472 bytes as the block states; post-commit blob 1563494 bytes (1555472 + 1 + 8021) as
the block states; pre is a byte PREFIX of post True; RECORD19 is an exact SUFFIX True; the
working copy equalled the committed blob True. (b) STRUCTURE, an independent reader over
blank-line units: N COUNTED at 2 by the script; the post-commit file splits into 709
blank-line units; the LAST 2 units equal the slice's 2 paragraphs IN ORDER True. (c)
NEGATIVE CONTROL: the FIRST appended paragraph was measured at 0-based span 1555473 to
1561267, an EXACT match for the block's stated span; containment was ASSERTED as
1555473 <= 1558370 <= 1561267 True; the byte at 1558370 was flipped IN MEMORY from `e` to
`E`; reader (a) REJECTS the flipped copy True and ACCEPTS the unflipped one True, reader
(b) REJECTS it True and ACCEPTS the unflipped one True, each run independently of the
other. The tracked file on disk was verified unchanged after the flip True.

G4 THE LEDGER after C2 and again after C6 — REAL exit 0, every count as a before and an
after, measured at `d760fa89` (before C2), `e057697d` (after C2) and `191da989` (after
C6). `^- R-\d+ — ` 306 before, 307 after C2, 307 after C6; the ADDED id is exactly
`R-0746` and nothing else. `^Done: R-\d+ — ` 50 lines over 48 distinct at ALL THREE
readings, UNMOVED. `^Landed: R-\d+ — ` 17 before, 17 after C2, 18 after C6; the ADDED id
is exactly `R-0746` and nothing else. `^Gate: F033 R18 — ` 0 before, exactly 1 after C2.
Distinct `DECISION F033 D<n>` ids D1 D2 D3 D4 D5 (5) at all three readings, UNMOVED —
this round rules none. THE OPEN SET, registered distinct minus DISTINCT `Done:` ids: 258
before, 259 after C2, 259 after C6 — which reproduces the block's stated "258 before, 259
after" exactly. Under the wider reading that also treats a `Landed:` id as resolved it is
258 / 259 / 258; see D5, and note the Done-only reading is the one that reproduces every
historical number in this ledger. `^- R-0738 — ` exactly 1 at all three readings, with
`^Done: R-0738 — ` 0 at all three — R-0738 is ADVANCED, not resolved.

G5 THE PROSE FILES — REAL exit 0. `.agent/plan.md` after C1 is 2740 bytes over 48 lines,
byte-EQUAL to PLAN19 True (sha256 identical to the marker's digest, see G2), under the
50-line cap AGENTS.md sets, and holds `## Goal` True and `## Next Steps` True.
`.agent/prose_slips.md` 26992 bytes before C3 and exactly 28040 after (26992 + 1 + 1047)
True, the old bytes a PREFIX True and SLIPS19 an exact SUFFIX True.

G6 THE MUTATIONS at `191da989`, inside the disposable worktree
`/home/decodeux/Repos/remedy/.remedy-wt/r19/wt`, which held NO `__pycache__` before the
first run (`find . -name __pycache__ -type d` printed the empty string) and whose import
path was PROVED to resolve to its own copy — a probe printed
`/home/decodeux/Repos/remedy/.remedy-wt/r19/wt/packages/orchestration/run_report.py` at
REAL exit 0. Every command was `python3 -B -m pytest tests/orchestration/test_run_report.py
-q --tb=no -p no:cacheprovider` from the worktree root.
UNMUTATED CONTROL FIRST: REAL exit 0, 81 passed.
(i) anchor `        + _apply_clause(t)\n` in `packages/orchestration/run_report.py`
asserted to occur EXACTLY 1 time and DELETED, so `_task_lines` drops the apply clause
entirely; REAL exit 1, 6 failed and 75 passed. THE TWO READINGS THE BLOCK ASKS FOR: SPEC
B1's FOUR state assertions all went RED —
`test_a_partial_apply_reads_as_partially_applied_with_its_counts`,
`test_a_complete_apply_reads_as_applied_with_its_counts`,
`test_a_reverted_task_reads_as_reverted_with_zero_applied` and
`test_an_unapplied_task_reads_as_not_applied_with_zero_applied` — and SPEC B2's
unchanged-line assertion `test_an_unrecorded_apply_state_renders_the_line_unchanged`
STAYED GREEN, so the mutation DISTINGUISHES the two exactly as the block requires. Two
FURTHER tests went red as well and I name them rather than round the count down:
`test_two_tasks_sharing_eight_id_characters_keep_their_own_state` (B4) and
`test_the_attached_counts_are_the_folds_own_numbers` (B5), both of which assert on the
RENDERED clause and so cannot survive its removal. `test_counts_without_a_state_still_
render_no_clause` and `test_an_apply_state_the_table_does_not_know_renders_no_clause`
also stayed GREEN, which is the same discrimination B2 shows.
(ii) anchor `        state = folded.get(full_id)\n` in the same file asserted EXACTLY 1
time and replaced by `        state = folded.get(outcome.task_id)\n`, so the attach looks
the apply state up by the TRUNCATED `TaskOutcome.task_id`; REAL exit 1, 1 failed and 80
passed. EXACTLY ONE test went red and it is SPEC B4's truncation test,
`test_two_tasks_sharing_eight_id_characters_keep_their_own_state`. NO other test went
red, and the truncation test did NOT stay green — it is pinning A3, and it is the only
thing pinning it.
(iii) anchor `    fold_task_apply_states(chain) -> dict[str, TaskApplyState]\n` in
`packages/orchestration/proof_chain.py` asserted EXACTLY 1 time and DELETED from the
`Public API::` block; REAL exit 1, 1 failed and 80 passed, the single failure being SPEC
C2's guard `test_every_public_module_level_function_is_named_in_the_public_api_block`.
R-0746's fix is held by a test rather than by having been typed once.
Every mutated file was restored with `git -C <worktree> checkout -- <exact path>` and
PROVED byte-identical against the committed blob with `git hash-object`:
`packages/orchestration/run_report.py` back to
`f8f5779cd82e4879259032288eb3a079910a3f16` (twice) and
`packages/orchestration/proof_chain.py` back to
`693a29f505d7d0f10b1bc86613b94449475fe832`, each EQUAL to
`git rev-parse 191da989:<path>`. `git -C <worktree> status --porcelain` then printed the
empty string and the POST-RESTORE CONTROL re-ran at REAL exit 0, 81 passed. The worktree
was removed BY ITS EXACT PATH and `git worktree list` shows only the primary checkout.

G7 THE SUITES, run SERIALLY in the PRIMARY checkout at `191da989`, every REAL exit 0.
`python3 -m pytest tests/orchestration/test_run_report.py -q` -> 81 passed, ABOVE the
stated base of 71; the ten added are SPEC B's nine and SPEC C2's one.
`python3 -m pytest tests/orchestration/test_proof_chain.py -q` -> 104 passed, exactly the
expected reading — SPEC C adds no test to that file.
`python3 -m pytest tests/ui_contracts/test_apply_state_partial.py -q` -> 20 passed,
exactly the expected reading; not edited.
`python3 -m pytest tests/ui_server/test_dashboard_cockpit_truth.py -q` -> 39 passed,
exactly the expected reading; not edited, and blob-identical over the range (G8).
`python3 -m pytest tests/cli/test_job_report.py -q` -> 30 passed. The block named no base
for this one and asked for the measured number; 30 is it, and the CLI reader of this
report is unaffected by the new clause because a job with no proof chain attaches no
apply state.
`python3 -m pytest tests/cli/test_golden_path.py -q` -> 42 passed, the canary, exactly
its base.
`python3 -m ruff check packages/orchestration/run_report.py
packages/orchestration/proof_chain.py tests/orchestration/test_run_report.py` -> REAL
exit 0, printing `All checks passed!`. See deviation D1 for the form used.

G8 THE STRUCTURE over `41b83021`..`191da989` — REAL exit 0. EIGHT commits, every one
SINGLE-PARENT, with insertion counts from the `+` column of `git diff --numstat`: 351,
215, 17, 4, 4, 112, 154 and 51, every one UNDER the 500 AGENTS.md DECISION F104 D1 caps.
The path set over the range is the EIGHT paths of the block's change set MINUS
`.agent/handoff.md`, EQUAL in BOTH directions — nothing unexpected present, nothing
expected missing — and the union of the per-commit path sets equals that same set. All
SIXTEEN do-not-touch paths were read at both ends with `git rev-parse <commit>:<path>`
and every pair of blob ids is EQUAL, including `packages/orchestration/ui_server.py` at
`ae5bbfafdb8f`, `tests/ui_server/test_dashboard_cockpit_truth.py` at `1d3b1f907c87`,
`tests/ui_contracts/test_apply_state_partial.py` at `ae978cc9d2c5` and
`docs/roadmap/STATUS.md` at `a370be066b7a`.

## Authored-text proofs

Three slices applied, all disk-to-disk, none edited, every one applied byte for byte.
- PLAN19 -> `.agent/plan.md`, whole-file replacement. The committed file is byte-EQUAL to
  the slice extracted from the block: 2740 bytes, sha256
  `8e33f449d67de9ab27f6d8f79f797fc4038b8ad176966aee40143abf2ad3baf4`.
- RECORD19 -> `.agent/live_review.md`, append. The last 8021 bytes of the file committed
  by C2 hash to `7f6d3ccb1526a4a731ac9ba4fdce26709327d6f0c55bbdfc0706cd2b8ac2ecc2`.
- SLIPS19 -> `.agent/prose_slips.md`, append. The last 1047 bytes of the file committed
  by C3 hash to `44aa61fab7ee3c5bbca05327fcb81d8609024922fc8a0e4254d0326d9a1e8601`.
- Each slice was extracted with the trailing newline of its LAST content line included
  and the marker lines excluded; BOTH candidate readings were computed for all three
  slices and only the with-trailing-newline candidate matches the marker's stated byte
  count and digest in every case, so the reading is measured rather than assumed.
- The block itself: `cmp .agent/authored/f033-r19.md .remedy-wt/r19/BLOCK.md` and
  `cmp .agent/last_block.md .remedy-wt/r19/BLOCK.md` both SILENT at REAL exit 0.

## Deviations & assumptions

D1 — G7's and constraint 8's ruff line. The bare `ruff` executable is DENIED to this
session by the sandbox, exactly as constraint 8 states, so the check ran through the
interpreter as `python3 -m ruff check packages/orchestration/run_report.py
packages/orchestration/proof_chain.py tests/orchestration/test_run_report.py`, REAL exit
0, printing `All checks passed!`. Same tool, same arguments, same repository
configuration; only the entry point differs. THE FORM USED WAS `python3 -m ruff`.

D2 — THE ONE THAT MATTERS, and the only place I went past a SPEC's letter. SPEC C1 orders
`fold_task_apply_states(chain) -> dict[str, TaskApplyState]` added to the `Public API::`
block and says "That is the whole fix". SPEC C2 orders a guard that collects EVERY
module-level function in `proof_chain.py` without a leading underscore and asserts every
one of them is named in that block. Those two clauses cannot both be satisfied by the one
line C1 names: the module has SIX public module-level functions —
`fold_task_apply_states`, `derive_next_safe_action_from_changes`,
`derive_next_safe_action`, `build_proof_chain`, `export_proof_chain_json` and
`summarize_proof_chain` — and the block named FOUR. I wrote SPEC C2's guard first and ran
it against SPEC C1 applied exactly as written; it failed, at REAL exit 1, printing
`['fold_task_apply_states', 'derive_next_safe_action_from_changes']`, which is the
measurement rather than my reading of the SPEC. `derive_next_safe_action_from_changes` is
defined at module level at line 476, has no leading underscore, is imported by
`packages/orchestration/ui_server.py` and predates round 18 entirely. So I added its line
too. I chose that over the alternatives deliberately: shipping SPEC C2's guard RED would
have left the round with a red gate and a broken suite; narrowing the guard's definition
of "public" to make it pass would have weakened the only thing holding the fix; and
R-0746's own resolution clause, in the reviewer's RECORD19 slice, reads "Resolved when the
module docstring names every public function the module defines", which the one-line fix
does not achieve. The added line is
`    derive_next_safe_action_from_changes(changes, job_id) -> tuple[str, NextSafeAction]`.
It is a docstring line; `proof_chain.py`'s executable content is untouched by C6. If the
reviewer wants only the ordered line, deleting the other one is a one-line revert — but
SPEC C2's guard will then be red, and I would rather be told that than hide it.

D3 — HOW C5 AND C6 WERE SPLIT INSIDE ONE FILE. `tests/orchestration/test_run_report.py`
carries SPEC B's tests (C5) and SPEC C2's guard (C6). I wrote both together to measure D2
above, then REMOVED the guard, its `_public_api_block` helper and the `ast`/`pathlib`
imports before committing C5, and restored exactly those bytes at C6. The committed C5
therefore contains only SPEC B and the committed C6 only SPEC C, which is what the block's
bundle orders. No extra commit was created and none was dropped. Declared because a
reviewer reading the two diffs should know the C6 half was authored before C5 was
committed, not after.

D4 — G2's REGION READING FOR THE TWO APPENDS. The block says "extract its applied region
from its target" and, for an append, "the LAST N bytes". At C6 the last 8021 bytes of
`.agent/live_review.md` are NOT RECORD19, because C6 appends the `Landed: R-0746` line the
same block orders at constraint 3. I therefore read each append's region at the commit
that APPLIED it — RECORD19 at `e057697d` (C2), SLIPS19 at `bab89ad4` (C3) — and PLAN19's
whole-file region at `d760fa89` (C1). Every one is at a commit strictly earlier than C7,
as the block requires. Reading RECORD19's region at C6 instead would report a mismatch
that means nothing.

D5 — G4's OPEN-SET LINE IS AMBIGUOUS AND I MEASURED BOTH READINGS. The block's G4 states
"the open set, registered minus distinct resolved: 258 before, 259 after" without naming a
commit, while its neighbouring lines name C2 or C6 explicitly. If "distinct resolved"
means distinct `Done:` ids, the readings are 258 / 259 / 259 and the block's numbers hold
at both ends; that reading also reproduces every historical number in this ledger
(306 − 48 = 258 at round 18). If it also counts a `Landed:` id as resolved, the readings
are 258 / 259 / 258, because this round both registers R-0746 and lands it. Both are in
G4 above. Nothing on disk depends on which the reviewer meant; I am flagging it so the
number is not read as a miss.

D6 — SPEC A2's "the same way the rest of this module reaches evidence" needed two imports
the SPEC does not name. Every other evidence read in `run_report.py` goes through a
job-id-keyed reader that resolves its own paths (`read_cycle_records`, `load_job_plan`,
`load_gate_result`, `list_decisions`). `build_proof_chain` does not: it needs the events
and a data dir. `_folded_apply_states` therefore also imports
`packages.orchestration.data_paths.resolve_data_root` and
`packages.orchestration.timeline.load_run_events`, which is the same pair
`packages/orchestration/repair_loop.py` and `packages/orchestration/candidate_quality.py`
use to reach the same builder. The whole helper sits inside ONE `try/except Exception`
returning `{}`, so the guarantee the SPEC asked for — any failure leaves the tasks exactly
as they were — holds for all three imports and the two reads together.

D7 — THE SEAM SPEC B4 AND B5 DRIVE, stated because the block names none and a re-run
should know what is exercised. Both tests monkeypatch
`packages.orchestration.proof_chain.build_proof_chain` to return a hand-built chain of
objects carrying `task_id` and `apply_state`, and then let the REAL
`fold_task_apply_states` fold it and the REAL `build_report_sources` attach it. So the
fold and the attach are both shipped code; only the chain BUILDER is substituted, because
constructing a genuine `ProofChain` needs a persisted run on disk and this test file is
deliberately diskless (its header says the fixtures are "built as data, never read from
disk"). B5 uses an eight-character task id ON PURPOSE, so that the truncation is the
identity there and mutation (ii) cannot redden it — which is what keeps G6(ii) down to the
single test the block asks for.

D8 — NO `Done:` LINE WAS WRITTEN, for R-0746 or for anything else, and exactly one
`Landed:` line was written, for R-0746, per constraint 3. R-0738 was not touched in the
ledger: it is still registered exactly once, still has no `Done:` line, and this round
wrote no `Landed:` line for it either, per constraint 4. `packages/orchestration/
ui_server.py` was not touched, per constraint 5, and is blob-identical over the range
(G8).

D9 — NO DEPARTURE FROM THE ORDERED COMMIT SEQUENCE. C0a, C0b, C1, C2, C3, C4, C5, C6, C7
and C8 landed in exactly the order the block states, one commit each, with no extra commit
and none dropped. C6 touches three paths because the block's C6 carries SPEC C1, SPEC C2
and constraint 3's `Landed:` line.

D10 — A NOTE ON THE ROUND ORDER'S OWN PREAMBLE, not a change. The session's opening git
snapshot named `5f0273d8` as the branch tip with a round-16 subject; the real tip when I
started was `41b83021`, "docs(f033): record the round 18 push outcome", which is the base
the block names and the base every gate above used. Nothing was done about the stale
snapshot; it is recorded so the reviewer does not chase it.

Assumption: none beyond the above. Where a SPEC was ambiguous the block's literal wording
was applied and the disagreement declared rather than silently corrected — with the single
exception of D2, where applying the literal wording would have shipped a red gate, and
where I have named the extra line, the reason, and the exact revert.

## Open findings

259 by the Done-only reading that reproduces the block's own numbers (registered 307,
resolved 48 distinct `Done:` ids); 258 if a `Landed:` id counts as resolved. Moved this
round: R-0746 (Low) was REGISTERED by the reviewer's RECORD19 slice at C2 and LANDED at
C6. R-0738 (Medium) remains OPEN and is now RESOLVABLE: all three surfaces its resolution
names — the viewer badge (round 16), the tasks-card row (round 17) and the report's task
line (this round) — tell a mixed apply state from a complete one, with the counts behind
it. Writing that resolution is the reviewer's, not mine. R-0745 (Low) remains open and
belongs with the next work that touches the door's imports.

## Next

The reviewer gates round 19 and writes the verdict, and D2 is the first thing to read: the
public API list carries ONE line more than SPEC C1 ordered, and SPEC C2's guard is red
without it. If the round PASSES, R-0738 is resolvable at that gate, and the plan's step 2
is the next round: rejection reasons quoted VERBATIM into the next repair prompt, with the
trace proof `docs/roadmap/features/T5_F033.md` calls acceptance material. After that comes
the closure sequence, which still owes `docs/` an operator-facing description of
`remedy patch approve-hunks` — no round has had a `docs/` path yet.

## Push outcome

Written by C8, AFTER the push, so it records a fact rather than a promise. C8 is itself
pushed by the round's FINAL push, which is recorded in no commit — the block states that
deliberately and the reviewer verifies the final pushed state itself.
