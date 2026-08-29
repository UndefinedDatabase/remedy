# STEP 27 — F033 Hunk-level diff approval (SESSION 7, round 27; the INTEGRATION GATE round)

Goal: run the integration gate of docs/agents/integration_gate.md — the full
suite on this branch and at the merge base, compared and attributed id by id —
and book the round 26 PASS and the `Done: R-0749` resolution alongside it. This
is the round that earns the right to say "full suite green"; no other round in
this feature may claim it.

## Bundle — the list that is executed

1. C0a: save this block verbatim to `.agent/authored/f033-r27.md`.
2. C0b: mirror the same bytes into `.agent/last_block.md`.
3. C1: rewrite `.agent/plan.md` from slice PLAN27.
4. C2: append slice RECORD27 to `.agent/live_review.md` — books the round 26
   PASS and RESOLVES R-0749.
5. C3: the integration gate itself. Run G5, G6 and G7 and commit the evidence
   files they produce under `.agent/gate_f033_r27/`.
6. C4: rewrite `.agent/handoff.md` as the handback.

## Change set — exactly these paths, nothing else

    .agent/authored/f033-r27.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/gate_f033_r27/branch_run.txt
    .agent/gate_f033_r27/branch_failed.txt
    .agent/gate_f033_r27/base_run.txt
    .agent/gate_f033_r27/base_failed.txt
    .agent/gate_f033_r27/parity.txt
    .agent/gate_f033_r27/comparison.txt
    .agent/handoff.md

An attribution file `.agent/gate_f033_r27/attribution.txt` is added to that set
IF AND ONLY IF G7 produces any id to attribute; when both comparison sets are
empty it is not created and the handback says so. No other file under
`.agent/gate_f033_r27/` may be committed.

## What the reviewer measured before writing this block, and where

Every reading below was taken by the reviewer at `7adee149`, this round's base.

- THE MERGE BASE IS `bd8d9529`. `git merge-base main HEAD` and
  `git rev-parse bd8d9529` answer the same full SHA
  `bd8d952942d8ec1d243d787ccfe16e0ad04360d2`, which is also the commit
  `.agent/plan.md` records this branch as cut from.
- THE SUITE COLLECTS 18467 TESTS at this base, in 3.82 seconds. That number is
  the collection, NOT a pass count, and G5 reports its own.
- BOTH BUILD ARTIFACTS EXIST in the primary checkout: `apps/ui/node_modules` at
  305M and `apps/ui/dist` at 432K.
- `apps/ui/node_modules` CONTAINS SYMLINKS — 23 of them within three levels,
  which are npm's bin shims. This is why G6 orders `symlinks=True` explicitly:
  `shutil.copytree` DEFAULTS to `symlinks=False` and would dereference every one
  of them, and finding R-0591 records that exact default causing 7 of 23
  base-only failures in a previous gate. The mechanism's default is the hazard,
  so the argument is ordered rather than assumed.
- `.remedy-wt/` IS INVISIBLE TO THE RUN MANIFEST. `git ls-files --others
  --exclude-standard` returns ZERO paths at this base, so a log growing there
  during a run cannot change the worktree digest — which is the SUBSTANCE of
  R-0176's "outside the repo worktree" rule, and the reason this block puts run
  logs there rather than in a location this sandbox denies.
- THE EVIDENCE DIRECTORY CONVENTION is the one `.agent/gate_f257_r6/` shows:
  `branch_run.txt`, `branch_failed.txt`, `base_run.txt`, `base_failed.txt`,
  `parity.txt`, `comparison.txt`. All `.txt`; never `.log`, which `.gitignore`
  drops silently and the review-zip guard rejects.
- THERE IS NO STALE WORKTREE. `git worktree list` shows the primary checkout
  alone.

## Slice PLAN27 — the FULL new bytes of `.agent/plan.md`

The slice is every byte BETWEEN the two marker lines, exclusive. The markers are
not part of any file.

<<<BEGIN PLAN27
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 7 of this feature, running past the
amend0827 rule 6 soft limit under the scope report that limit required.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001, T002 and T003 | done | rounds 1-24 |
| THE FEATURE'S FUNCTIONAL SCOPE | complete | at round 24 |
| R-0749, both instances landed | done | rounds 25 and 26 |
| the operator guide and its index rows | done | round 26 |
| the integration gate | open | this round |
| the closure sequence and its pull request | open | after the gate |
| R-0745, the door's transitive import closure | open | carried as a risk |

## Next Steps
1. This round books the round 26 PASS and the `Done: R-0749` resolution, then
   runs the integration gate of docs/agents/integration_gate.md: the full suite
   on this branch and at the merge base `bd8d9529`, compared and attributed.
2. Only this round's gate entry may carry a "full suite" claim. A reproducible
   branch-only failure coupled to feature code is a BLOCKER and buys its own
   reviewer-gated repair round rather than being fixed inside this one.
3. Then the closure sequence per docs/roadmap/STATUS_closure_protocol.md: the
   feature file's Built State, the evidence job, the review zip, the STATUS line
   and the pull request, which is NOT merged in this session.
4. R-0745 is Low and is not reachable from this feature's Acceptance. The
   closure protocol's precondition 1 admits a documented Medium/Low risk, so it
   is carried as one and the STATUS line reads PASS_WITH_RISKS.

## Risks
- The base worktree lacks build artifacts the suite needs. Parity is restored by
  COPY with symlinks preserved, and every base-only failure is attributed by
  direct evidence whether or not the parity claim holds.
<<<END PLAN27

## Slice RECORD27 — appended to `.agent/live_review.md`

Two paragraphs, blank-line separated.

<<<BEGIN RECORD27
Gate: F033 R26 — THE OPERATOR GUIDE, ITS INDEX ROWS, AND THE CLAIM'S FOURTH INSTANCE. THE ROUND PASSED. Every gate was re-executed by the reviewer at `7adee149` from scripts of its own, and every ordered reading reproduced. TRANSPORT: the reviewer's OWN pre-emission original, the committed `.agent/authored/f033-r26.md` and `.agent/last_block.md` are all 30483 bytes at sha256 `41ff9a4b…08283e` and BYTE-EQUAL to each other; the worker used `shutil.copyfile` and retyped nothing, including the SPEC A2 `Landed:` line, which it extracted from the committed block by script. The chain walks the emitted artefact, the saved copy and its mirror, and claims nothing about bytes never written to disk. THE PLAN is byte-EQUAL to PLAN26 at 2394 bytes over 45 lines, under the 50-line cap, holding `## Goal` and the substring `Steps`. THE RECORD APPEND at `0efdcba2` reconstructs 1611170 plus one newline plus 7077 to 1618248, base a byte PREFIX, slice an exact SUFFIX, the separator byte a newline, N COUNTED at 2, and the file's LAST TWO blank-line units equal to the slice's two paragraphs IN ORDER; the NEGATIVE CONTROL was taken at byte 1612508, an offset the reviewer chose independently of the worker's 1615413 and proved to lie inside the FIRST appended paragraph's span 1611171 to 1615897, and BOTH readers reject the flipped bytes while BOTH accept the unflipped ones. THE LEDGER at three revisions: `^- R-\d+ — ` 310 distinct UNMOVED and `^Done: R-\d+ — ` 54 lines over 52 distinct UNMOVED at all three, this round registering and resolving nothing as ordered; `^Landed: ` 21 going to 22 with `^Landed: R-0749 — ` 1 at the base and at C2 and exactly 2 at C4, the first line left standing; `^Gate: F033 R25 — ` 0 before and exactly 1 after; and the open set 258 UNMOVED. THE GUIDE AND ITS INDEX landed as one commit, which is the property that matters here rather than any count: `docs/guides/hunk-approval-user-guide-v1.md` is byte-EQUAL to slice GUIDE at 5145 bytes, each of the two APPEND-shaped pairs has its FROM occurring exactly 1x in `docs/README.md` after the commit, `git show --numstat` reads `2 0` for that file and each of the two TO-only lines occurs exactly 1x among the 2 lines the commit ADDS — and the reviewer additionally ran the link predicate `tests/docs/test_docs_consistency.py::TestPrimaryDocLinksResolve` applies, over every relative link in `docs/README.md`, finding ZERO broken. NO `FROM 0x` COUNT WAS ORDERED OR REPORTED for either index pair, because both are append-shaped and that count is unattainable by construction. THE REPAIR IS A DOCSTRING AND NOTHING ELSE: PAIRCALLER-FROM occurs 0 times and PAIRCALLER-TO exactly 1 time, `python3 -m ruff check` is a REAL exit 0, the two `ast.dump` renderings with every docstring constant blanked are EQUAL, and substituting the TO text back to the FROM text reproduces the base blob of `packages/orchestration/hunk_repair_findings.py` BYTE FOR BYTE — the stronger reading round 25 discovered and this block adopted. THE SWEEP over TRACKED content of `packages`, `apps`, `tests` and `docs` answers REAL exit 1 for `NO CALLER YET`, with a POSITIVE CONTROL finding the replacement text exactly once, so the zero is the sweep reaching the file. THE SUITES were re-run SERIALLY by the reviewer in the primary checkout, every REAL exit 0: `test_hunk_repair_findings.py` 17, `test_builder_prompt_hunk_rejections.py` 16, `tests/docs/` 295 — equal to the 295 measured at the base, so two index rows changed no count — and the canary 42. THE STRUCTURE: seven single-parent commits over `de2dc16d`..`7adee149` of 437, 345, 16, 4, 107, 7 and 206 insertions, every one under 500, the last being the handback commit no gate of the block could reach and which the reviewer measures here; `git status --porcelain` EMPTY; and the path set over the range to C4 EQUALS the declared change set minus `.agent/handoff.md` in BOTH directions. THE WORKER DECLARED SIX DEVIATIONS AND EVERY ONE IS HONEST. Two deserve naming: it ran `tests/docs/` piped to `tail` first, recognised that constraint 7 forbids taking an exit code through a pipe, re-ran it unpiped and reported only the unpiped reading; and it stated the BOUND of its own G7 reading half — that the reading covered three of the feature's modules rather than all of them — instead of letting "no fifth instance found" stand as if it were a total search. Declaring the reach of a search is the behaviour this record exists to encourage.

Done: R-0749 — BOTH INSTANCES ARE LANDED AND THE WIDENED PREDICATE IS MET BY A READING, NOT BY A STRING COUNT. The first fix landed at `9e84514a` on `packages/orchestration/pingpong_loop.py`, restating `compose_builder_prompt`'s route paragraph as the wired route it now is; the second at `3fe5db02` on `packages/orchestration/hunk_repair_findings.py`, replacing the "has NO CALLER YET" clause with the caller measured at `de2dc16d`. Both are docstring-only: for each, substituting the applied text back to the retired text reproduces that file's pre-commit blob BYTE FOR BYTE, so no executable statement moved in either. THE PREDICATE THIS FINDING WAS WIDENED TO — that no module of this feature asserts that ANY hop of the route from a recorded hunk decision to the next builder prompt is unwired, uncalled or still to come — was discharged by the reviewer at `7adee149` as a READING over TWELVE modules, two more than the extension named: the ten of `hunk_approval`, `hunk_ledger`, `hunk_identity`, `hunk_repair_findings`, `hunk_decision_record`, `pingpong_loop`, `pingpong_job`, `diff_view_source`, `diff_parser` and `apps/cli/commands/patch.py`, plus `hunk_subset_diff` and `hunk_apply`. Twelve phrasings of the class were searched and FOUR hits survive, every one of them read in full and none of them the defect: `hunk_approval.py` line 180 says normalisation happens once "so no caller has to", which is about work a caller is spared rather than a caller's absence; `hunk_approval.py` line 86 says hunks appearing in a later round render PENDING, which is the feature's own behaviour; `diff_parser.py` line 696 says a run is "not yet complete" inside a walk, which is an algorithm's own tense; and `diff_view_source.py` line 11 says "F037 R7 wires the two GET routes onto `build_diff_view`; nothing calls it before then", which NAMES the round that wired it and is therefore a history rather than an absence — the shape this whole finding family would have had if the original paragraphs had been written that way. THE LESSON THE FOUR INSTANCES PAID FOR is stated once here and belongs to the reviewer rather than to any worker: a round that COMPLETES a hop named in prose must sweep the prose that names it, and a gate proving a sentence gone from the file the reviewer was thinking about proves nothing about the file the reviewer was not. R-0747 and R-0748 were each gated by a string over a path; R-0749 is closed by a reading over a class, and that is the difference between the two outcomes.
<<<END RECORD27

## The integration gate — procedure

docs/agents/integration_gate.md is the canonical procedure and this block does
not restate it. What follows are the four points where THIS environment differs
from its plain wording, and each is an order rather than a suggestion.

P1. RUN LOGS GO UNDER `.remedy-wt/`, NOT OUTSIDE THE REPOSITORY. R-0176 requires
a growing log to be invisible to the run manifest, whose untracked input is
`git ls-files --others --exclude-standard`; `.remedy-wt/` is gitignored, so it
is invisible by that measure, and this sandbox denies every path outside the
repository. Copy each finished log into `.agent/gate_f033_r27/` only AFTER its
run has exited. Declare this in the handback as a deviation from the file's
literal wording, with `git ls-files --others --exclude-standard` counted for
paths naming `remedy-wt` as its evidence.

P2. THE ENVIRONMENT VARIABLE IS SET IN PYTHON, NEVER AS A SHELL PREFIX. The
sandbox refuses `VAR=x cmd` and `env`. Set `REMEDY_UI_NO_AUTO_BUILD` to `1` in
the runner script's own `os.environ` for the BASE run, and do NOT trust it
alone: R-0169 records a spawned build path ignoring it and rewriting `dist/`
mid-run.

P3. PARITY IS RESTORED BY COPY WITH SYMLINKS PRESERVED. Copy the primary
checkout's `apps/ui/node_modules` and `apps/ui/dist` into the base worktree with
`shutil.copytree(src, dst, symlinks=True)`. The keyword is ordered explicitly
because its DEFAULT is `False` and that default dereferences the 23 bin shims
this tree carries — finding R-0591, where the same default caused 7 of 23
base-only failures the parity existed to prevent. Never symlink the directories
themselves: the UI auto-build writes THROUGH a symlink into the primary
checkout.

P4. THE PARITY CLAIM IS MEASURED BY THE EVENT, NOT THE OUTCOME. Record the mtime
of every file under the base worktree's `apps/ui/dist` immediately before the
base run and immediately after it, and report the run's own wall-clock window.
Any mtime falling inside that window VOIDS the parity claim. A content hash may
accompany that reading but never stands alone, because equal content is
consistent both with no rebuild and with a byte-identical one — the case F009
R29 actually hit.

## Constraints

1. Apply both slices BYTE FOR BYTE. If one looks wrong, apply it as written and
   declare the problem; never silently repair it.
2. PLAN27 is a FULL REWRITE. RECORD27 is an APPEND to `.agent/live_review.md`.
   Measured by the reviewer at `7adee149`, that file is 1618414 bytes and ends
   with a newline, so the append is one blank-line separator then the slice.
   RE-MEASURE it yourself at the commit you append at rather than trusting this
   number.
3. `.agent/live_review.md` is written by ONE commit this round, C2. G3's
   arithmetic and G4's ledger readings are both taken there and at `7adee149`.
4. Do NOT delete or edit any landed `Landed:`, `Done:` or `Gate:` text, and in
   particular leave BOTH `Landed: R-0749` lines standing beside the new `Done:`
   paragraph. The record is append-only.
5. Touch no path outside the change set. This round changes NO file under
   `packages/`, `apps/`, `tests/` or `docs/` — not one. If the gate turns up a
   failure that needs a code change, that change is its own reviewer-gated
   round: report it and stop.
6. The base worktree is created ON A THROWAWAY BRANCH —
   `git worktree add -b tmp/base-gate .remedy-wt/base-gate bd8d9529` — because
   the self-dogfood branch guard refuses a detached HEAD by design and a
   detached base worktree fails the guard-dependent ids for the wrong reason.
   Remove the worktree, prune it and delete `tmp/base-gate` before the handback.
7. Destructive and environment-mutating work happens ONLY inside that worktree.
   The primary checkout satisfies `git status --porcelain` empty at the
   handback, and `git worktree list` shows the primary checkout alone.
8. NEVER delete a test, weaken an assertion or raise a ceiling to make a check
   green, and never edit a test file this round at all — constraint 5 already
   forbids the path.
9. The sandbox denies `VAR=x cmd`, `env`, `export`, `cp`, `$(...)` inside a
   compound, process substitution, a heredoc nested in `bash -c`, and a shell
   line containing a brace with a quote inside it. Write scripts under
   `.remedy-wt/` and run them as `python3 -B <path>`. REAL exit codes come from
   `subprocess.run(...).returncode` inside those scripts, never from a pipe.
10. Re-read `.agent/STOP` before starting. If it exists, stop and hand off.
11. G1 through G8 all run at or before C3; the handback commit C4 follows them.
    Clean up `.remedy-wt/base-gate` and any script you wrote there BY EXACT
    PATH, never by glob.

## Done when — G1 through G8

G1 TRANSPORT. Report `sha256` and byte length of the committed
`.agent/authored/f033-r27.md`, and the same two readings for
`.agent/last_block.md`. One digest comparison; the reviewer holds the
pre-emission original and runs the other half itself.

G2 THE PLAN. `.agent/plan.md` byte-EQUAL to PLAN27, under 50 lines, holding
`## Goal` and the substring `Steps`. Report the byte length and the line count.

G3 THE RECORD APPEND, at C2. Reconstruct the MEASURED base plus one newline plus
the byte length of RECORD27 to the committed size. Prove the pre-commit blob a
byte PREFIX and the slice an exact SUFFIX. COUNT N in the script. Compare the
file's LAST N blank-line units against the slice's paragraphs IN ORDER. Flip one
byte inside the FIRST appended paragraph, report the offset, prove it lies in
that paragraph's span, and show BOTH readers reject the flipped bytes and accept
the unflipped ones.

G4 THE LEDGER, at `7adee149` and at C2: `^- R-\d+ — ` 310 distinct UNMOVED, this
round registering nothing; `^Done: R-\d+ — ` 54 lines over 52 distinct going to
55 over 53 with the ADDED resolved id exactly `R-0749`; `^Landed: ` 22 UNMOVED
with `^Landed: R-0749 — ` still exactly 2; `^Gate: F033 R26 — ` 0 before and
exactly 1 after; and the open set 258 going to 257.

G5 THE BRANCH RUN. From the repository root, `python3 -m pytest -n auto -q`.
Report the REAL exit code, the raw tail, the wall clock in seconds, and the
pass/fail/skip counts. Write the full output to `branch_run.txt` and the sorted
`^FAILED` lines to `branch_failed.txt`, both under `.agent/gate_f033_r27/`, and
report how many lines `branch_failed.txt` holds. If the wall clock exceeds five
minutes, say so — that is a note for a perf pass, not a failure.

G6 THE BASE RUN AND ITS PARITY. Create the worktree per constraint 6 at
`bd8d9529`. Restore parity per P3, then take the `apps/ui/dist` mtime reading
per P4 BEFORE the run. Run the IDENTICAL command with `cwd` set to the worktree
and `REMEDY_UI_NO_AUTO_BUILD` set per P2. Take the mtime reading again AFTER.
Report: the copy call with its `symlinks` argument as written, the count of
symlinks that survived as symlinks in the copy, the run's wall-clock window, how
many `apps/ui/dist` mtimes fall inside it, and whether the parity claim HOLDS or
is VOID. Write `base_run.txt`, `base_failed.txt` and `parity.txt`.

G7 COMPARE AND ATTRIBUTE, WITH NO CONDITION ON EITHER HALF.
`comm -13 base_failed.txt branch_failed.txt` is the BRANCH-ONLY set and
`comm -23` is the set the branch FIXED; write both to `comparison.txt` and
report both counts. Then, whether or not parity held:
  (i) attribute EVERY branch-only id. Re-run the exact node id SERIALLY. A
      serial PASS is the xdist-flake class — record it, it is not a blocker. A
      serial FAIL is reproduced at the merge base BEFORE the feature is blamed.
      A reproducible branch-only failure coupled to feature code is a BLOCKER:
      STOP and hand back.
  (ii) attribute EVERY `comm -23` id to the environment class by DIRECT
      evidence, naming the missing artifact per id. An unattributed id counts as
      a genuine base failure and blocks the gate verdict. This obligation does
      NOT depend on the parity claim: the two are independent, and a gate that
      discharges itself when parity holds demands nothing of the ids that
      exist — finding R-0703's class, and R-0590's instance exactly.
If both sets are EMPTY, say so explicitly and create no attribution file.

G8 CLEANUP AND STRUCTURE, at C3. Remove and prune the worktree and delete
`tmp/base-gate`; report `git worktree list` showing the primary checkout alone,
and `git branch --list tmp/base-gate` empty. Then `git status --porcelain`
EMPTY; `git ls-files --others --exclude-standard` counted for paths naming
`remedy-wt`, reported as a number; per-commit insertions from C0a through C3
each under 500; and the path set over `7adee149`..C3 equal to the change set
minus `.agent/handoff.md` in BOTH directions, allowing for the conditional
attribution file.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, SESSION 7 of F033, branch, commit SHAs, changed-files table, one line per
gate G1 through G8 with its REAL exit code, the open-findings count, an
item-status table covering every Bundle item, every deviation, and the next
expected action. No length cap. State the branch run's and the base run's REAL
exit codes and counts in full — this is the one round whose numbers a closure
may cite as "full suite". If any gate is RED, do not repair on your own
initiative: report it and stop.
