# Handback — F033 · ROUND 18 · the apply fold gets a shared home and its counts

> Written by the WORKER of round 18. The reviewer writes the verdict; this file
> reports what was run and what it printed. This round registered NO finding and
> resolved NONE: it wrote no `Done:` and no `Landed:` line.

## Session

SESSION 5 of feature F033 · round 18 · rounds so far 18.
The soft limit is NOT reached: 18 rounds of 25, 5 sessions of 7.

## Fortschritt

~92 % (T001 and T002 complete. T003: the fold's partial truth and the popover label
landed in round 16, the tasks-card row in round 17. THIS round moved the fold itself
out of the HTTP server into `packages/orchestration/proof_chain.py`, gave it the
APPLIED/TOTAL counts R-0738's fix asks for, and re-pointed the AST seam guard at its
new home — a move plus an addition, with no answer changed. The report line and the
rejection-to-repair injection remain, so R-0738 STAYS OPEN) — Schätzung.

## Range

Review of `2a938b5e`..`65315ec1` for the gated work — every gate below ran at a commit
no later than C6 — plus the two commits that cannot be inside it: C7, which writes this
file, and C8, which records the real push outcome after the push.
Branch `feature/f033-hunk-approval-v2`.

## Bundle item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block to `.agent/authored/f033-r18.md` | done | |
| C0b mirror it into `.agent/last_block.md` | done | |
| C1 `.agent/plan.md` <- PLAN18 | done | |
| C2 `.agent/live_review.md` <- RECORD18 | done | |
| C3 `.agent/prose_slips.md` <- SLIPS18 | done | |
| C4 the fold's new home and its counts (SPEC A) and the delegation (SPEC B) | done | |
| C5 the fold's own unit tests (SPEC D) | done | |
| C6 the re-pointed seam guard (SPEC C) | done | see deviations D2 and D3 |
| C7 `.agent/handoff.md` <- this handback | done | |
| C8 `.agent/handoff.md` <- the push outcome | done | recorded after the push |

## Commits

Every `+/-` cell below was taken from the SAME `git diff --numstat` run G8 reports and
compared to it cell by cell; they agree. No cell was filled from a file's own line count.

### a8823d55 docs(f033): save the round 18 block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f033-r18.md` | +373 -0 | C0a — the reviewer's block, byte for byte |

### f7b3440a docs(f033): mirror the round 18 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +273 -245 | C0b — same bytes, one blob id with C0a |

### 11c68c9b docs(f033): advance the plan to round 18
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +19 -17 | C1 — PLAN18 replaces the file whole (checklist item 23) |

### 440de7ea docs(f033): book the round 17 verdict
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2 -0 | C2 — RECORD18 appended; amend0827 rule 1 |

### 3b2be54e docs(f033): append the two round 17 prose slips
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/prose_slips.md` | +4 -0 | C3 — SLIPS18 appended; amend0827 rule 2 |

### ed10b57a refactor(f033): move the apply fold to proof_chain and give it counts
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/proof_chain.py` | +67 -0 | SPEC A — `TaskApplyState` and `fold_task_apply_states`, with the R-0738 WHY paragraph carried over |
| `packages/orchestration/ui_server.py` | +14 -22 | SPEC B — `_task_truth_maps` keeps its name, signature and proof half; its apply half is now a two-line adapter |

### ba89bbf3 test(f033): pin the apply fold as a function with its counts
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_proof_chain.py` | +170 -0 | SPEC D — `TestFoldTaskApplyStates`, fourteen tests over explicit inputs |

### 65315ec1 test(f033): re-point the seam guard at the fold new home
| Path | +/- | Reason |
|------|-----|--------|
| `tests/ui_contracts/test_apply_state_partial.py` | +34 -23 | SPEC C — the AST walk now names `proof_chain.py`, `fold_task_apply_states` and `state_by_task` |

### C7 and C8 (this file)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | see below | C7 writes this handback; C8 appends the real push outcome. A handoff cannot table the commit that writes it (R-0149 pattern). |

## External actions

- `git worktree add --detach /home/decodeux/Repos/remedy/.remedy-wt/r18/wt 65315ec1`
  -> exit 0, "Preparing worktree (detached HEAD 65315ec1) / HEAD is now at 65315ec1".
- `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/r18/wt` -> exit 0, no
  output. `git worktree list` afterwards shows only `/home/decodeux/Repos/remedy`.
- `git push` — see the PUSH OUTCOME section at the bottom, written by C8.
- No `gh` command was run and no PR was created or merged. F033 is not closed and the
  PR belongs to the closure sequence.

## Verification — one line per gate, real exit codes

G1 HYGIENE AND THE STOP FILE — `ls -la .agent/STOP` REAL exit 2, printing exactly
`ls: cannot access '.agent/STOP': No such file or directory`, so the sentinel does not
exist; `git status --porcelain` before C0a REAL exit 0 printing NOTHING, and again after
C6 REAL exit 0 printing NOTHING.

G2 TRANSPORT — REAL exit 0. Applied region vs the digest in each slice's own BEGIN
marker: PLAN18 whole-file region 2765 bytes sha256
`5214755bf41d758a22903a62b8d60b6df4c2ab4af7929f2c6d7779ad0b6a273a` MATCHES; RECORD18
last-5764-byte region sha256
`40df3d80c337ebf480b5638f14b8adb861d31df74436c6a067d1c7b047cb48bf` MATCHES; SLIPS18
last-1049-byte region sha256
`6372f2bbee6a23f437a09c342aa515ca7d81903e11b7da6311410826b77e4956` MATCHES. The C0a and
C0b blobs are ONE id, `096199413754f1d59f71dcee94c9a6019780a84d`, and `cmp` of BOTH
`.agent/authored/f033-r18.md` and `.agent/last_block.md` against the reviewer's file on
disk at `.remedy-wt/r18/BLOCK.md` was SILENT at REAL exit 0, 29036 bytes, sha256
`45a71a66f343fc928e215146c7a5245fa4516bfd09e2066bf4108cc6e8720309`, the digest the round
order named. THIS PROVES THE SAVED COPY, ITS MIRROR AND THE WORKING COPY AGREE; IT IS NOT
A CLAIM ABOUT THE BYTES THAT WERE EMITTED.

G3 THE RECORD APPEND at C2 — REAL exit 0, all three readings. (a) BYTES: pre-commit blob
1549707 bytes as the block states; post-commit blob 1555472 bytes (1549707 + 1 + 5764) as
the block states; pre is a byte PREFIX of post True; RECORD18 is an exact SUFFIX True; the
working copy equals the committed blob True. (b) STRUCTURE, an independent reader: N
COUNTED at 1 by the script; the post-commit file splits into 707 blank-line units; the
LAST 1 unit equals the slice's 1 paragraph IN ORDER True. (c) NEGATIVE CONTROL: the FIRST
appended paragraph was measured at 0-based content span 1549708 to 1555470, an EXACT match
for the block's stated span; containment was ASSERTED as 1549708 <= 1552589 <= 1555470
True; the byte at 1552589 was flipped IN MEMORY from `t` to `T`; reader (a) REJECTS the
flipped copy True and ACCEPTS the unflipped one True, reader (b) REJECTS it True and
ACCEPTS the unflipped one True, each run independently of the other. The tracked file on
disk was verified unchanged after the flip True.

G4 THE LEDGER after C2 — REAL exit 0, every count as a before and an after.
`^- R-\d+ — ` 306 before, 306 after, UNMOVED. `^Done: R-\d+ — ` 50 lines over 48 distinct
before, 50 over 48 after, UNMOVED. `^Landed: R-\d+ — ` 17 before, 17 after, UNMOVED.
`^Gate: F033 R17 — ` 0 before, exactly 1 after. Distinct `DECISION F033 D<n>` ids
D1 D2 D3 D4 D5 (5) before and (5) after, UNMOVED — this round ruled none. The open set,
registered minus resolved, 258 before and 258 after, UNMOVED. `^- R-0738 — ` exactly 1 at
both ends, with `^Done: R-0738 — ` 0 at both ends — the finding is ADVANCED, not resolved.

G5 THE PROSE FILES — REAL exit 0. `.agent/plan.md` after C1 is 2765 bytes over 49 lines,
byte-EQUAL to PLAN18 True (sha256 identical to the slice digest, see G2), under the
50-line cap AGENTS.md sets, and holds `## Goal` (line 6) and `## Next Steps` (line 30).
`.agent/prose_slips.md` 25942 bytes before C3 and exactly 26992 after (25942 + 1 + 1049),
the old bytes a PREFIX True and SLIPS18 an exact SUFFIX True.

G6 THE MUTATIONS at `65315ec1`, inside the disposable worktree
`/home/decodeux/Repos/remedy/.remedy-wt/r18/wt`, which held NO `__pycache__` before the
first run (`find … -name __pycache__ -type d` printed nothing) and every command run with
`python3 -B` from the worktree root over all three suites G7's first three lines name:
`python3 -B -m pytest tests/ui_contracts/test_apply_state_partial.py
tests/orchestration/test_proof_chain.py tests/ui_server/test_dashboard_cockpit_truth.py
-q --tb=no -p no:cacheprovider`.
UNMUTATED CONTROL FIRST: REAL exit 0, 163 passed (20 + 104 + 39).
(i) anchor `state_by_task[tid] = "partial"` in
`packages/orchestration/proof_chain.py` asserted to occur EXACTLY 1 time and replaced by
`state_by_task[tid] = "applied"`; REAL exit 1, 12 failed and 151 passed. THE MOST
IMPORTANT READING OF THE ROUND: the SIX seam assertions in the re-pointed
`tests/ui_contracts/test_apply_state_partial.py` went red
(`test_the_fold_assigns_the_partial_label`, `test_the_two_sets_agree_in_both_directions`
and all four `TestTheCardTellsThePartialStateApart` tests), THREE mixed-case unit tests in
`tests/orchestration/test_proof_chain.py` went red
(`test_a_mixed_group_folds_to_partial`, `test_applied_and_reverted_together_fold_to_partial`,
`test_two_tasks_in_one_chain_are_folded_independently`), and THREE in the unedited
`tests/ui_server/test_dashboard_cockpit_truth.py` went red as well. The re-pointed guard
therefore reads the fold's REAL new home; had it been left pointing at `ui_server.py` its
expected set would have been empty and these six would have passed.
(ii) anchor `applied=sum(1 for s in apply_states if s == "applied"),` in the same file
asserted EXACTLY 1 time and replaced by `applied=len(apply_states),`; REAL exit 1, 4
failed and 159 passed — `test_the_counts_on_a_mixed_group_differ_from_each_other`,
`test_the_total_is_the_group_size_when_nothing_applied`,
`test_a_reverted_change_is_not_counted_as_applied` and
`test_two_tasks_in_one_chain_are_folded_independently`, exactly the COUNT assertions of
SPEC D and nothing else. The counts are pinned.
(iii) anchor `for tid, folded in fold_task_apply_states(chain).items(): / apply_by_task[tid]
= folded.state` in `packages/orchestration/ui_server.py` asserted EXACTLY 1 time and
replaced by `apply_by_task.clear()`, so `_task_truth_maps` returns an empty apply map;
REAL exit 1, 8 failed and 155 passed, EVERY failure in
`tests/ui_server/test_dashboard_cockpit_truth.py` — the file this round does NOT edit.
The adapter is still wired to the cockpit.
Every mutated file was restored (see deviation D4 for the route) and PROVED byte-identical
against the committed blob with `git hash-object`:
`packages/orchestration/proof_chain.py` back to `c6e1c2664564850e641f53382256f7b1516d8eb6`
and `packages/orchestration/ui_server.py` back to `ae5bbfafdb8f528d3293dcea570accf33afebe2c`,
both EQUAL to `git rev-parse 65315ec1:<path>`. `git -C <worktree> status --porcelain` then
printed NOTHING and the POST-RESTORE CONTROL re-ran at REAL exit 0, 163 passed. The
worktree was removed BY ITS EXACT PATH and `git worktree list` shows only the primary
checkout.

G7 THE SUITES, run SERIALLY in the PRIMARY checkout at `65315ec1`, every REAL exit 0.
`python3 -m pytest tests/orchestration/test_proof_chain.py -q` -> 104 passed, above the
stated base of 90; the fourteen added are SPEC D's `TestFoldTaskApplyStates`.
`python3 -m pytest tests/ui_contracts/test_apply_state_partial.py -q` -> 20 passed, exactly
the expected reading — SPEC C adds no test.
`python3 -m pytest tests/ui_server/test_dashboard_cockpit_truth.py -q` -> 39 passed,
exactly the expected reading; this file was not edited and its blob id is unchanged over
the range (G8).
`python3 -m pytest tests/ui_contracts/ -q` -> 684 passed, 4 skipped, exactly the base.
`python3 -m pytest tests/orchestration/test_run_report.py -q` -> 71 passed, exactly the
base; `run_report.py` is untouched this round.
`python3 -m pytest tests/cli/test_golden_path.py -q` -> 42 passed, the canary.
The ruff gate over all four changed code files exited 0 printing `All checks passed!` —
see deviation D1 for how it was invoked.

G8 THE STRUCTURE over `2a938b5e`..`65315ec1` — REAL exit 0. EIGHT commits, every one
SINGLE-PARENT, with insertion counts from the `+` column of `git diff --numstat`: 373,
273, 19, 2, 4, 81, 170 and 34, every one UNDER the 500 AGENTS.md DECISION F104 D1 caps.
The path set over the range EQUALS the block's change set MINUS `.agent/handoff.md` in
BOTH directions: nothing unexpected present, nothing expected missing. All SIXTEEN
do-not-touch paths were read at both ends with `git rev-parse <commit>:<path>` and every
pair of blob ids is EQUAL, including `packages/orchestration/run_report.py` at
`21b1e6587dfa`, `tests/ui_server/test_dashboard_cockpit_truth.py` at `1d3b1f907c87`,
`apps/ui/src/components/detail/DetailPopover.tsx` at `ae95b80d5ac5` and
`apps/ui/src/components/panels/TaskChecklistCard.tsx` at `53e1d725138e`.

## Authored-text proofs

Three slices applied, all disk-to-disk, none edited, every one applied byte for byte.
- PLAN18 -> `.agent/plan.md`, whole-file replacement. The committed file is byte-EQUAL to
  the slice extracted from the block: 2765 bytes, sha256
  `5214755bf41d758a22903a62b8d60b6df4c2ab4af7929f2c6d7779ad0b6a273a`.
- RECORD18 -> `.agent/live_review.md`, append. The last 5764 bytes of the committed file
  hash to `40df3d80c337ebf480b5638f14b8adb861d31df74436c6a067d1c7b047cb48bf`.
- SLIPS18 -> `.agent/prose_slips.md`, append. The last 1049 bytes hash to
  `6372f2bbee6a23f437a09c342aa515ca7d81903e11b7da6311410826b77e4956`.
- Each slice was extracted with the trailing newline of its LAST content line included and
  the marker lines excluded; both candidate readings were computed and only the
  with-trailing-newline candidate matches the marker's stated byte count and digest, for
  all three slices.
- The block itself: `cmp .agent/authored/f033-r18.md .remedy-wt/r18/BLOCK.md` and
  `cmp .agent/last_block.md .remedy-wt/r18/BLOCK.md` both SILENT at REAL exit 0.

## Deviations & assumptions

D1 — G7's and constraint 9's ruff line. The bare `ruff` executable is DENIED to this
session by the sandbox, exactly as constraint 9 states, so the byte-identical check ran
through the interpreter as `python3 -m ruff check packages/orchestration/proof_chain.py
packages/orchestration/ui_server.py tests/orchestration/test_proof_chain.py
tests/ui_contracts/test_apply_state_partial.py`, REAL exit 0, printing
`All checks passed!`. Same tool, same arguments, same repository configuration; only the
entry point differs. THE FORM USED WAS `python3 -m ruff`.

D2 — ONE CHANGE BEYOND SPEC C's LETTER, in SPEC C's direction. C1 orders the constant
naming the searched FILE re-pointed at `packages/orchestration/proof_chain.py`. That
constant was named `SERVER`, and a constant named SERVER holding the path of
`proof_chain.py` is false in exactly the way C4 orders repaired in the module docstring, so
I RENAMED it to `FOLD_MODULE` and updated its six uses inside assertion messages. No
assertion was added, removed, weakened or changed in meaning; the rename is identifier-only
and the file still runs its full 20 tests. Declared because the block ordered a re-pointing,
not a rename. If the reviewer wants `SERVER` back, it is a mechanical revert of one
identifier.

D3 — SPEC C3, stated because the obligation was met a different way than the wording
anticipates. C3 assumes the new fold may name its state list something new. It does not:
the moved fold still names it `apply_states`, so the existing AST predicate was already over
the right local and discriminates as it did before (offenders measured as the empty set, and
G6(i) shows the surrounding assertions are live). To make that binding explicit rather than
incidental I added a module constant `FOLD_STATE_LIST = "apply_states"` and bound the
predicate to it instead of to an inline literal. Nothing was weakened; this is the only
addition SPEC C received.

D4 — THE G6 RESTORE ROUTE. My mutation helper's own `revert` mode failed on mutation (i) at
REAL exit 1: replacing `partial` with `applied` created a SECOND occurrence of
`state_by_task[tid] = "applied"`, so its "replacement is unique" assertion could not hold —
that is the helper being careful, not the file being wrong. I restored instead with
`git -C /home/decodeux/Repos/remedy/.remedy-wt/r18/wt checkout -- <exact path>` and PROVED
byte-identity with `git hash-object` against `git rev-parse 65315ec1:<path>`, and used the
same route for (ii) and (iii) so all three restores are proved the same way. No file was
restored from memory or by re-typing. Reported because the block says "restoring every
mutated file byte-identically and PROVING it against the committed blob" without naming a
route, and this is the route taken.

D5 — SPEC A4's `ImportError`. The clause orders the new fold to guard `ImportError`,
`AttributeError` and `TypeError`, "the same exception classes the shipped fold guards".
`fold_task_apply_states` performs NO import of its own — the import that made `ImportError`
reachable in `_task_truth_maps` is the proof-constants import, which stayed behind in
`ui_server.py` — so `ImportError` is unreachable inside the new function. I applied the
clause AS WRITTEN, all three classes, and declare the disagreement rather than dropping one:
the guard is harmless and dropping it would have been me re-deciding the reviewer's spec.

D6 — SPEC B3's SWEEP CLAIM, narrowed to what I can measure. B3 says that after C4 "the
four apply labels are literals in `proof_chain.py` and in no other production module".
That is TRUE OF THE APPLY FOLD'S LABELS: no apply-fold label literal remains in
`ui_server.py`. It is NOT true of the STRING `"partial"` as a string:
`packages/orchestration/ui_server.py` line 492 still contains `state = "partial"`, inside
`_metrics_proof_from_chain`, which is a PROOF-verification counter (`verified` vs `total`)
and has nothing to do with the apply fold. That line pre-dates this round, is outside the
round's diff, and `git diff` over the range shows only the fold's lines changed in that
file. Declared so a grep the reviewer runs does not read as a broken claim.

D7 — SPEC A did not order the module docstring of `packages/orchestration/proof_chain.py`
updated, and I did not update it. Its `Public API::` list therefore still names four
functions and not `fold_task_apply_states`, which is public and is the whole point of the
move. I left it alone rather than widening the diff past the SPEC on my own authority; the
reviewer may want a one-line addition next round.

D8 — No `Done:` and no `Landed:` line was written, and no id was minted. That is what
constraint 8 orders; it is recorded here because a reader auditing the round against its
block should see the absence was deliberate. R-0738 stays open: the report line, the third
surface its resolution names, is untouched, and `packages/orchestration/run_report.py` is
blob-identical over the range (G8).

D9 — NO DEPARTURE FROM THE ORDERED COMMIT SEQUENCE. C0a, C0b, C1, C2, C3, C4, C5, C6, C7
and C8 landed in exactly the order the block states, one commit each, with no extra commit
and none dropped. Round 17's C8 was an unordered correction; this round's C8 is the one the
block itself orders.

Assumption: none beyond the above. Where a SPEC was ambiguous the block's literal wording
was applied and the disagreement declared rather than corrected.

## Open findings

258, UNMOVED across this round. Registered 306, resolved 48 distinct. R-0738 (Medium) now
has its fold in a module both readers may import and carries the APPLIED/TOTAL counts its
resolution clause asks for, but it remains OPEN: the report line has not been written.
R-0745 (Low) remains open and belongs with the next work that touches the door's imports.

## Next

The reviewer gates round 18 and writes the verdict. If it PASSES, the next round is the
plan's step 2: THE REPORT LINE. `packages/orchestration/run_report.py` is blob-identical to
`2a938b5e` at `21b1e6587dfa` and holds no apply state at all, so `TaskOutcome` gains one and
`_task_lines` renders the mixed case with the counts `fold_task_apply_states` now returns —
which it can import from `packages/orchestration/proof_chain.py` without reaching into the
HTTP server, the dependency this round existed to remove. That is the LAST of the three
surfaces R-0738 names; only after it is R-0738 resolvable.

## Push outcome

Written by C8, AFTER the push, so it records a fact rather than a promise. C8 is itself
pushed by the round's FINAL push, which is recorded in no commit — the block states that
deliberately and the reviewer verifies the final pushed state with `git rev-parse` against
the remote.

`git push -u origin feature/f033-hunk-approval-v2` -> REAL exit 0:

    To github.com:UndefinedDatabase/remedy.git
       2a938b5e..87ce4bac  feature/f033-hunk-approval-v2 -> feature/f033-hunk-approval-v2
    Branch 'feature/f033-hunk-approval-v2' set up to track remote branch
    'feature/f033-hunk-approval-v2' from 'origin'.

A fast-forward, `2a938b5e..87ce4bac`; no force flag of any kind was used, no history was
rewritten and no branch was deleted. `git rev-parse` immediately afterwards gave
`87ce4bac9bf16ff142e3447cc7c1cdbca11d1e4a` for BOTH `HEAD` and
`origin/feature/f033-hunk-approval-v2`, so the remote carries C0a through C7 exactly. This
sentence describes only what has already happened and predicts nothing about the final
push that carries C8.
