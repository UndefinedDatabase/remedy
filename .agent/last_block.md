# STEP 26 — F033 Hunk-level diff approval (SESSION 7, round 26; past the soft limit, under the delivered scope report)

Goal: give the operator the `docs/` description of `remedy patch approve-hunks`
that no round of this feature has yet been allowed a path for, register it in
the documentation index in the same commit, and retire the FOURTH instance of
the claim R-0747, R-0748 and R-0749 have each retired once — the round-25 worker
found it and correctly declined to repair it outside its change set.

## Bundle — the list that is executed

1. C0a: save this block verbatim to `.agent/authored/f033-r26.md`.
2. C0b: mirror the same bytes into `.agent/last_block.md`.
3. C1: rewrite `.agent/plan.md` from slice PLAN26.
4. C2: append slice RECORD26 to `.agent/live_review.md` — books the round 25
   PASS and EXTENDS R-0749, which is NOT resolved this round.
5. C3: create `docs/guides/hunk-approval-user-guide-v1.md` from slice GUIDE, and
   in the SAME commit apply pairs PAIR-QUICKFIND and PAIR-GUIDES to
   `docs/README.md`. The file and its index rows land together or not at all:
   `tests/docs/test_docs_consistency.py::TestPrimaryDocLinksResolve` reads
   `docs/README.md` and fails on a link with no file behind it.
6. C4: SPEC A — the R-0749 fourth-instance repair, pair PAIR-CALLER, and in the
   SAME commit the second `Landed: R-0749` line of SPEC A2.
7. C5: rewrite `.agent/handoff.md` as the handback.

## Change set — exactly these paths, nothing else

    .agent/authored/f033-r26.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    docs/guides/hunk-approval-user-guide-v1.md
    docs/README.md
    packages/orchestration/hunk_repair_findings.py
    .agent/handoff.md

## What the reviewer measured before writing this block, and where

Every reading below was taken by the reviewer at `de2dc16d`, this round's base.

- THE FOURTH INSTANCE IS REAL. `packages/orchestration/hunk_repair_findings.py`
  says the module "has NO CALLER YET — the round that wires its output into the
  next builder prompt follows this one", while
  `packages/orchestration/pingpong_loop.py` imports
  `render_rejection_findings` at its line 34 and calls it inside
  `compose_builder_prompt` at its line 977. Round 21 falsified that sentence.
- IT IS THE ONLY REMAINING ONE. The reviewer swept the feature's ten modules for
  the class — `NO CALLER YET`, `no caller`, `nothing calls`, `not yet`,
  `unwired`, `not wired`, `follows this one`, `a later round`,
  `DELIBERATE ABSENCE` — and read every hit. Two need saying because they look
  like the class and are NOT: `diff_view_source.py` line 11 names the round that
  wired it, which is a history and not an absence; and
  `hunk_decision_record.py` line 20 says "IT PERSISTS NOTHING. It MUTATES
  `job.metadata` and returns", which is TRUE and is scoped to the module's own
  storage I/O rather than to the record's durability — it is not R-0747's claim
  and must not be edited.
- THE FROM SPAN of PAIR-CALLER occurs EXACTLY ONCE in its file: 585 bytes over
  7 lines. The reviewer dry-ran the repair with a red control: the AST reading
  of G6 answers True for the repaired bytes and False for a control that
  additionally renames `render_rejection_findings`, and
  `python3 -m ruff check --stdin-filename
  packages/orchestration/hunk_repair_findings.py -` exits 0 over them.
- THE INDEX ANCHORS ARE UNIQUE. Each of the two FROM lines occurs exactly once
  in `docs/README.md`, and `docs/README.md` states no count of its own rows, so
  adding two drifts no numeral.
- `python3 -m pytest tests/docs/ -q` is a REAL exit 0 at 295 passed at this
  base, so any red there is this round's.
- THE GUIDE'S FACTS were each read out of the shipped code rather than from any
  feature file: the seven refusal codes and their CHECK ORDER, the two-axis
  ledger vocabulary, `unattempted` as the only landing a recording can write,
  the attempt key's replace-on-re-decision rule, the split on the FIRST `=`, the
  16-hex-character id and its stability property, and both diff routes.

## SPEC A — the R-0749 fourth-instance repair

A1. Apply PAIR-CALLER below to
`packages/orchestration/hunk_repair_findings.py`. The reviewer ran the
containment test at `de2dc16d` and the result is `TO contains FROM: false`, so
it is a REWRITE and the obligation is PAIRCALLER-FROM 0x and PAIRCALLER-TO
exactly 1x in the file after the commit. Report both counts. Change nothing
else in that file: this round alters a docstring and no executable statement,
which is what G6's AST reading measures.

A2. In the SAME commit append to `.agent/live_review.md` exactly one line:

    Landed: R-0749 — the claim's fourth instance is removed from the module docstring's caller clause, packages/orchestration/hunk_repair_findings.py, C4 of round 26.

This is the SECOND `Landed:` line for this id and the first one STAYS. Write no
`Done:` paragraph: R-0749 is resolved by the reviewer at the next gate, once
both of its instances are landed.

## Slice PLAN26 — the FULL new bytes of `.agent/plan.md`

The slice is every byte BETWEEN the two marker lines, exclusive. The markers are
not part of any file.

<<<BEGIN PLAN26
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
| R-0749 first instance, the loop docstring | landed | round 25 |
| the operator guide and its index rows | open | this round |
| R-0749 fourth instance, the renderer docstring | open | this round |
| the integration gate round | open | next |
| the closure sequence and its pull request | open | after the gate |
| R-0745, the door's transitive import closure | open | carried as a risk |

## Next Steps
1. This round books the round 25 PASS, ships the operator guide for
   `remedy patch approve-hunks` with its two `docs/README.md` index rows in the
   same commit, and retires the claim's fourth instance.
2. R-0749 stays OPEN until both of its instances are landed and the reviewer
   resolves it; the round after this one books that resolution alongside its own
   first commits, never in a round of its own.
3. Then the integration gate per docs/agents/integration_gate.md, then the
   closure sequence and its pull request.
4. R-0745 is Low and is not reachable from this feature's Acceptance. The
   closure protocol's precondition 1 admits a documented Medium/Low risk, so it
   is carried as one rather than blocking a feature that has met its Acceptance.

## Risks
- R-0745 stays OPEN at closure and the STATUS line therefore reads
  PASS_WITH_RISKS. Its fix recommends a transitive-closure guard test, which is
  a hardening task deserving its own round rather than a corner of a closure.
- The claim R-0747 opened has now been found in four files across five rounds.
  Its resolution predicate is worded over the CLAIM, so the reviewer resolves it
  only after reading the feature's modules rather than counting a string.
<<<END PLAN26

## Slice RECORD26 — appended to `.agent/live_review.md`

Two paragraphs, blank-line separated. Neither begins with `- R-`, so the
registration count does not move this round.

<<<BEGIN RECORD26
Gate: F033 R25 — THE ROUND 24 VERDICT BOOKED, R-0748 RESOLVED, AND THE CLAIM'S THIRD INSTANCE RETIRED FROM THE LOOP DOCSTRING. THE ROUND PASSED. Every gate was re-executed by the session-7 reviewer at `de2dc16d` from scripts of its own, and every ordered reading reproduced. TRANSPORT is the strongest this workflow can produce and the verdict states exactly what it covers: the reviewer's OWN pre-emission original, the committed `.agent/authored/f033-r25.md` and `.agent/last_block.md` are all 25113 bytes at sha256 `88dd0980…3323ab` and BYTE-EQUAL to each other, so one end of the comparison is the emitted artefact itself rather than a third copy of the worker's — the worker used `shutil.copyfile` and retyped nothing. This chain still says nothing about bytes never written to disk, and does not claim to. THE PROSE FILES: `.agent/plan.md` byte-EQUAL to PLAN25 at 2329 bytes over 43 lines, under the 50-line cap, holding `## Goal` and the substring `Steps`; `.agent/prose_slips.md` reconstructs 31337 plus one newline plus 597 to 31935, base a byte PREFIX and slice an exact SUFFIX. THE RECORD APPEND at `8c5ecfdb` reconstructs 1602790 plus one newline plus 8215 to 1611006, base a byte PREFIX, slice an exact SUFFIX, the separator byte a newline, N COUNTED at 3 by the reviewer's own script, and the file's LAST THREE blank-line units equal to the slice's three paragraphs IN ORDER. THE NEGATIVE CONTROL was taken at byte 1603702, an offset the reviewer chose independently of the worker's 1604957 and proved to lie inside the FIRST appended paragraph's span 1602791 to 1607124: BOTH readers reject the flipped bytes and BOTH accept the unflipped ones. THE LEDGER walked at three revisions: `^- R-\d+ — ` 309 distinct going to 310 with the ADDED id exactly `R-0749`; `^Done: R-\d+ — ` 53 lines over 51 distinct going to 54 over 52 with the ADDED resolved id exactly `R-0748`; `^Landed: ` 20 going to 21 with `^Landed: R-0749 — ` 0 at the base and at C2 and exactly 1 at C4, and the landed `Landed: R-0748` line still standing beside its new `Done:` paragraph; `^Gate: F033 R24 — ` 0 before and exactly 1 after; and the open set 258 at all three revisions, one registration against one resolution. THE REPAIR IS A DOCSTRING AND NOTHING ELSE, and the reviewer took a reading STRONGER than the one it ordered: PAIRROUTE-FROM occurs 0 times and PAIRROUTE-TO exactly 1 time, `python3 -m ruff check` is a REAL exit 0, the two `ast.dump` renderings with every docstring constant blanked are EQUAL at 476252 characters each — and substituting the TO text back to the FROM text reproduces the base blob of `packages/orchestration/pingpong_loop.py` BYTE FOR BYTE, which proves the pair is the ONLY change to that file rather than merely that no statement moved. THE SWEEP WAS RUN OVER TRACKED CONTENT, which is the round-24 lesson applied: `git grep -c -F` over `packages`, `apps`, `tests` and `docs` answers REAL exit 1 for each of `no round has wired`, `ONE HOP STILL MISSING`, `this segment never registers` and `persists no decision`, and a POSITIVE CONTROL over the same four trees finds the replacement text exactly once in the repaired file — so the zero counts are the sweep reaching the file and finding nothing, not the sweep missing the file. THE SUITES were re-run SERIALLY by the reviewer in the primary checkout, every REAL exit 0: `test_builder_prompt_hunk_rejections.py` 16, `test_builder_prompt_golden.py` 21, `test_pingpong.py` 34, and the canary 42. THE STRUCTURE: seven single-parent commits over `d81acca5`..`de2dc16d`, `git status --porcelain` EMPTY, and the path set over the range to C4 EQUALS the declared change set minus `.agent/handoff.md` in BOTH directions. THE WORKER'S BEST ACT THIS ROUND WAS NOT A GATE. G6's reading half — the clause that asks for a reading rather than a count, because R-0749's predicate is worded over a CLAIM — turned up a FOURTH instance of that claim in `packages/orchestration/hunk_repair_findings.py`, and the worker declared it and did NOT repair it, because that path is outside the round's change set and the block forbids repairing on the worker's own initiative. That is exactly the required behaviour, it is the reason the reading half was ordered at all, and the reviewer confirms the instance independently at `de2dc16d`. Two smaller deviations are honest and need no action: the worker reported the AST dump length as 477810 where the reviewer's own reader measures 476252, which is a property of two different blanking implementations and not of the file, and the EQUALITY both measured is what the gate asserts; and one compound `bash` line was refused by the harness and replaced with separate simple calls, with no workaround attempted.

R-0749 EXTENSION — A FOURTH INSTANCE, FOUND BY THE ROUND-25 WORKER, AND WHY THIS IS NOT A NEW ID. Under docs/agents/planner_reviewer_prompt.md §3 item 30 a new id is minted only after the open set is searched for the DEFECT, and R-0749 is OPEN and is that defect, so this evidence joins it rather than spending R-0750. The contrast with R-0748 is deliberate and is the rule working in both directions: R-0747 had already been RESOLVED when its second instance was found, and reopening a resolved finding in an append-only record is worse than registering the escapee, whereas R-0749 is landed but unresolved and can still carry this. THE INSTANCE, measured by the reviewer at `de2dc16d`: `packages/orchestration/hunk_repair_findings.py` states in its module docstring that the module "has NO CALLER YET — the round that wires its output into the next builder prompt follows this one", while `packages/orchestration/pingpong_loop.py` imports `render_rejection_findings` at line 34 and calls it inside `compose_builder_prompt` at line 977. Round 21 falsified that sentence and swept nothing. So the claim R-0747 opened has now been found in FOUR files across FIVE rounds, and every one of them was a paragraph true on the day it was written and falsified by a later round that completed the hop the paragraph named. THE REVIEWER SWEPT THE CLASS RATHER THAN THE INSTANCE this time, over the ten modules of this feature, and reports the two hits that resemble it and are NOT it: `diff_view_source.py` line 11 names the round that wired its routes, which is a history rather than an absence, and `hunk_decision_record.py` line 20 says "IT PERSISTS NOTHING. It MUTATES `job.metadata` and returns", which is TRUE and is scoped to that module's own storage I/O rather than to the record's durability. Neither is edited. THE FIX CLAUSE IS WIDENED ACCORDINGLY and replaces the job-level wording of the registration: R-0749 is Resolved when no module of this feature asserts that ANY hop of the route from a recorded hunk decision to the next builder prompt is unwired, uncalled or still to come — a reading taken over the CLAIM, over the modules, and never over a list of strings, because four path-scoped and string-scoped gates in a row each proved a sentence gone from the file the reviewer was thinking about and nothing about the file it was not.
<<<END RECORD26

## Slice GUIDE — the FULL bytes of the new file `docs/guides/hunk-approval-user-guide-v1.md`

<<<BEGIN GUIDE
# Hunk-level diff approval — user guide (v1)

`remedy patch approve-hunks` records an operator's decision over the individual hunks of
a job's diff: which are approved, which are rejected, and why. It RECORDS and never
applies — no file in your repository is modified by it — and the reason you give for a
rejected hunk is quoted VERBATIM into the next builder prompt, which is what turns a
rejection into a repair instruction.

```
remedy patch approve-hunks <job-id> [--task-run <task-id>]
                           [--approve-hunk <hunk-id>]...
                           [--reject-hunk <hunk-id>=<reason>]...
                           [--json]
```

`<job-id>` may be any prefix a job id resolves by, the same as the other `remedy patch`
commands. Both hunk options are repeatable: give one occurrence per hunk.

## Where hunk ids come from

A hunk id is 16 lowercase hex characters. You do not invent one — read it from the diff
view, either in the UI's diff viewer or from the HTTP API:

    GET /api/jobs/<job-id>/diff                             the job-level diff
    GET /api/jobs/<job-id>/task-runs/<task-id>/diff         one task run's diff

Each file entry of that view carries a `hunks` list, and each hunk carries its `id`.

The id is CONTENT-DERIVED and carries no position. It is computed over the file's path,
the hunk's OLD side — its context and deleted lines, never its added lines — and the
hunk's occurrence rank among byte-identical old sides within the same file. The property
you may rely on: a hunk KEEPS its id when other hunks in its file move, grow or vanish,
and when its OWN added lines change, because a second proposed fix for the same original
text is the same hunk. It changes only when the path changes or when the hunk's own old
side does. A decision you record therefore survives the builder rewriting its answer.

## Choosing the scope

Omit `--task-run` to decide over the JOB-level diff. Pass it to decide over one task
run's diff, named exactly as that run appears under `task_runs/` in the job's evidence.

The scope you choose is the scope the decision is recorded under, and the two do not
mix: a decision recorded at job scope is deliberately NOT quoted into any single task's
next prompt, because it was never attributed to one.

## What a recorded decision holds

Every hunk of the chosen diff appears in the record on two independent axes.

STATE is what you decided: `approved`, `rejected` or `pending`. A hunk you named in
neither option is `pending`, and that is a legitimate answer rather than an error — a
hunk appearing for the first time in a later round inherits no decision.

LANDING is what became of the bytes: `landed`, `not_landed` or `unattempted`. Recording
a decision never runs an apply, so every entry this command writes lands `unattempted`.
That is not a synonym for `not_landed`: the first means no apply has run, the second
means one ran and these bytes did not reach the branch.

Deciding the same scope twice REPLACES the earlier record rather than adding a second,
so you may revise freely while the landing is still `unattempted`.

## Output

Without `--json`, four lines:

    Recorded: <task-id>:<attempt>
      approved: 2
      rejected: 1
      pending: 5
    Note: the decision is metadata only — no files have been modified.

With `--json`, the record itself is printed with sorted keys — `task_id`, `attempt`,
`decided_at` and `hunks` — where each row of `hunks` carries exactly `id`, `state`,
`reason` and `landing`, and nothing derived.

## When the command refuses

A refusal exits 1 and writes NOTHING to the job: a refused decision is not a
half-recorded one. Without `--json` the message goes to stderr, with the offending ids
on a following `hunks:` line; with `--json` the refusal is printed as `code`, `message`
and `hunk_ids`. The codes, in the order they are checked:

    no_diff_available   the attempt has no diff to decide over at all
    untrustworthy_view  the diff was truncated, so which hunks it omits is unknown
    empty_decision      you approved nothing and rejected nothing
    duplicate_hunk      an id repeats within --approve-hunk, or within --reject-hunk
    overlapping_sets    an id appears in both
    unknown_hunk        an id is not among the hunks this diff carries
    missing_reason      a rejection carries no reason, or only whitespace

The FIRST code that trips is the one you see, and `hunk_ids` names every offending id at
once rather than one per round-trip.

## Reasons are held byte for byte

`--reject-hunk <id>=<reason>` splits on the FIRST `=`, so a reason may itself contain an
`=` and survives whole. The reason is stored exactly as typed — surrounding whitespace,
interior blank lines and tabs included — and reaches the next builder prompt unchanged:

    remedy patch approve-hunks 4f2a \
        --approve-hunk 1c9e0b77a4d3f215 \
        --reject-hunk 8b31c04ef7a9d260="renames a public name; keep the old spelling"

Remedy deliberately does not reformat, wrap, truncate or normalise a rejection reason.
They are the operator's own words, and the next round is told to act on them.
<<<END GUIDE

## Pair PAIR-QUICKFIND — the Quick-Find table of `docs/README.md`

Containment test run by the reviewer at `de2dc16d`: `TO contains FROM: true`, so
this is an APPEND-shaped pair and NO `FROM 0x` count is ordered for it. The
obligation is §4.9's: the FROM line occurs exactly 1x in the file after the
commit, and the ONE TO-only line occurs exactly 1x among the lines C3's diff
ADDS. The FROM occurs exactly once at this base.

<<<BEGIN PAIRQUICK-FROM
| job budget | [job-budget-enforcement-v0.md](system/job-budget-enforcement-v0.md) | system |
<<<END PAIRQUICK-FROM

<<<BEGIN PAIRQUICK-TO
| hunk approval | [hunk-approval-user-guide-v1.md](guides/hunk-approval-user-guide-v1.md) | guide |
| job budget | [job-budget-enforcement-v0.md](system/job-budget-enforcement-v0.md) | system |
<<<END PAIRQUICK-TO

## Pair PAIR-GUIDES — the Guides table of `docs/README.md`

Containment test run by the reviewer at `de2dc16d`: `TO contains FROM: true`, so
this is an APPEND-shaped pair and NO `FROM 0x` count is ordered for it. The same
§4.9 obligation applies. The FROM occurs exactly once at this base.

<<<BEGIN PAIRGUIDES-FROM
| [job-context-view-user-guide-v0.md](guides/job-context-view-user-guide-v0.md) | What one task's compiled context carries and what was omitted |
<<<END PAIRGUIDES-FROM

<<<BEGIN PAIRGUIDES-TO
| [hunk-approval-user-guide-v1.md](guides/hunk-approval-user-guide-v1.md) | Recording a hunk-level approve and reject decision over a job's diff |
| [job-context-view-user-guide-v0.md](guides/job-context-view-user-guide-v0.md) | What one task's compiled context carries and what was omitted |
<<<END PAIRGUIDES-TO

## Pair PAIR-CALLER — `packages/orchestration/hunk_repair_findings.py`

Containment test run by the reviewer at `de2dc16d`: `TO contains FROM: false`.
It is therefore a REWRITE, and the gate is PAIRCALLER-FROM 0x and PAIRCALLER-TO
exactly 1x after the commit. The FROM occurs exactly once in the file at that
commit, at 585 bytes over 7 lines. Neither text is indented; both sit at column
one inside the module docstring.

<<<BEGIN PAIRCALLER-FROM
DELIBERATE ABSENCE — this module is PURE: text and data in, text out. It reads no file,
runs no subprocess, opens no socket, reads no environment variable, keeps no state and logs
nothing, and it imports the standard library and ``packages.orchestration.hunk_ledger`` and
nothing else. It also does NOT build the ledger it renders (that is
``packages/orchestration/hunk_ledger.py``), does not decide whether a decision is coherent
(``packages/orchestration/hunk_approval.py``), and has NO CALLER YET — the round that wires
its output into the next builder prompt follows this one.
<<<END PAIRCALLER-FROM

<<<BEGIN PAIRCALLER-TO
DELIBERATE ABSENCE — this module is PURE: text and data in, text out. It reads no file,
runs no subprocess, opens no socket, reads no environment variable, keeps no state and logs
nothing, and it imports the standard library and ``packages.orchestration.hunk_ledger`` and
nothing else. It also does NOT build the ledger it renders (that is
``packages/orchestration/hunk_ledger.py``) and does not decide whether a decision is coherent
(``packages/orchestration/hunk_approval.py``). ITS CALLER IS THE BUILDER PROMPT: measured at
``de2dc16d``, ``packages/orchestration/pingpong_loop.py`` imports ``render_rejection_findings``
and calls it inside ``compose_builder_prompt``, where the rendered text becomes the
``builder_hunk_rejections`` segment.
<<<END PAIRCALLER-TO

## Constraints

1. Apply every slice and every pair BYTE FOR BYTE. If one looks wrong, apply it
   as written and declare the problem; never silently repair it.
2. PLAN26 is a FULL REWRITE. GUIDE is a NEW FILE and its bytes are the whole of
   it. RECORD26 and the `Landed:` line are APPENDS to `.agent/live_review.md`.
   Measured by the reviewer at `de2dc16d`, that file is 1611170 bytes and ends
   with a newline, so the append is one blank-line separator then the slice.
   RE-MEASURE it yourself at the commit you append at rather than trusting this
   number.
3. `.agent/live_review.md` is written by TWO commits: C2 appends RECORD26, C4
   appends the single `Landed:` line. G3's arithmetic is measured at C2 and
   G4's ledger readings at `de2dc16d`, at C2 and at C4.
4. Do NOT delete or edit any landed `Landed:`, `Done:` or `Gate:` text, and in
   particular leave the FIRST `Landed: R-0749` line standing. The record is
   append-only.
5. The guide file and BOTH `docs/README.md` pairs land in ONE commit, C3. A
   commit holding the index rows without the file leaves `docs/README.md` with
   a link to nothing, which is a red `tests/docs/` and a false index.
6. Touch no path outside the change set. In particular do NOT touch
   `packages/orchestration/pingpong_loop.py`,
   `packages/orchestration/diff_view_source.py`,
   `packages/orchestration/hunk_decision_record.py`, any other file under
   `docs/guides/`, or anything under `docs/roadmap/`.
7. The sandbox denies `VAR=x cmd`, `env`, `export`, `cp`, `$(...)` inside a
   compound, process substitution, a heredoc nested in `bash -c`, and a shell
   line containing a brace with a quote inside it. Write scripts under
   `.remedy-wt/` and run them as `python3 -B <path>`; use `python3 -m ruff`.
   REAL exit codes come from `bash -c '<cmd>; echo "REAL_EXIT=$?"'` with NO PIPE.
8. Every absence gate of this round is run over TRACKED CONTENT with
   `git grep`, never with a plain recursive grep.
9. This round mutates no executable code, so it orders NO mutation red-proof and
   needs no disposable worktree. G6's AST reading stands in its place and the
   reviewer dry-ran it with a red control. The primary checkout satisfies
   `git status --porcelain` empty at the handback.
10. Re-read `.agent/STOP` before starting. If it exists, stop and hand off.
11. G1 through G8 all run at C4, before the handback commit C5.

## Done when — G1 through G8

G1 TRANSPORT. Report `sha256` and byte length of the committed
`.agent/authored/f033-r26.md`, and the same two readings for
`.agent/last_block.md`. One digest comparison; the reviewer holds the
pre-emission original and runs the other half itself.

G2 THE PLAN. `.agent/plan.md` byte-EQUAL to PLAN26, under 50 lines, holding
`## Goal` and the substring `Steps`. Report the byte length and the line count.

G3 THE RECORD APPEND, at C2. Reconstruct the MEASURED base plus one newline plus
the byte length of RECORD26 to the committed size. Prove the pre-commit blob a
byte PREFIX and the slice an exact SUFFIX. COUNT N in the script. Compare the
file's LAST N blank-line units against the slice's paragraphs IN ORDER. Flip one
byte inside the FIRST appended paragraph, report the offset, prove it lies in
that paragraph's span, and show BOTH readers reject the flipped bytes and accept
the unflipped ones.

G4 THE LEDGER, at `de2dc16d`, at C2 and at C4: `^- R-\d+ — ` 310 distinct
UNMOVED at all three, this round registering nothing; `^Done: R-\d+ — ` 54 lines
over 52 distinct UNMOVED at all three, this round resolving nothing;
`^Landed: ` 21 going to 22 with `^Landed: R-0749 — ` 1 at the base and at C2 and
exactly 2 at C4; `^Gate: F033 R25 — ` 0 before and exactly 1 after; and the open
set 258 UNMOVED at all three.

G5 THE GUIDE AND ITS INDEX, at C3. (a) `docs/guides/hunk-approval-user-guide-v1.md`
is byte-EQUAL to slice GUIDE; report its byte length. (b) In `docs/README.md`
each of PAIRQUICK-FROM and PAIRGUIDES-FROM occurs exactly 1 time, and each of the
two TO-only lines occurs exactly 1 time AMONG THE LINES C3's diff ADDS — measure
that with `git show --numstat` for the total and a per-line count over the added
lines, and report both numbers. Do NOT order or report a `FROM 0x` count for
either pair: both are APPEND-shaped and that count is unattainable by
construction. (c) `python3 -m pytest tests/docs/ -q` is a REAL exit 0; report the
pass count and compare it against the 295 measured at the base.

G6 THE REPAIR IS A DOCSTRING AND NOTHING ELSE, at C4. (a)
`python3 -m ruff check packages/orchestration/hunk_repair_findings.py` exits 0.
(b) In that file the PAIRCALLER-FROM text occurs 0 times and the PAIRCALLER-TO
text exactly 1 time. (c) THE AST READING: parse the file at `de2dc16d` and at
C4, blank every docstring constant of every module, class and function node in
both trees, and show `ast.dump` of the two is EQUAL. (d) THE STRONGER READING
the round-25 gate found and this one adopts: substituting PAIRCALLER-TO back to
PAIRCALLER-FROM in the committed file reproduces the base blob BYTE FOR BYTE.
Report it as a boolean.

G7 THE CLAIM IS GONE, READ RATHER THAN COUNTED. With `git grep` over TRACKED
content of `packages`, `apps`, `tests` and `docs` at C4, `NO CALLER YET` occurs
0 times; report the command and the count, and report a POSITIVE CONTROL showing
the same sweep finds `ITS CALLER IS THE BUILDER PROMPT` exactly once, so the zero
is the sweep reaching the file. Then READ these three files and report one
sentence each on whether any docstring or comment in them still asserts that a
hop of the route from a recorded hunk decision to the builder prompt is unwired,
uncalled or still to come: `packages/orchestration/hunk_repair_findings.py`,
`packages/orchestration/hunk_ledger.py` and `packages/orchestration/hunk_approval.py`.
This half is a reading, not a count.

G8 SUITES AND STRUCTURE, at C4. SERIALLY, each with its REAL exit code and pass
count: `python3 -m pytest tests/orchestration/test_hunk_repair_findings.py -q`;
`python3 -m pytest tests/orchestration/test_builder_prompt_hunk_rejections.py -q`;
`python3 -m pytest tests/docs/ -q`; and the canary
`python3 -m pytest tests/cli/test_golden_path.py -q`. Then `git status
--porcelain` EMPTY; per-commit insertions from C0a through C4 each under 500;
and the path set over `de2dc16d`..C4 equal to the change set minus
`.agent/handoff.md` in BOTH directions.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, SESSION 7 of F033, branch, commit SHAs, changed-files table, one line per
gate G1 through G8 with its REAL exit code, the open-findings count, an
item-status table covering every Bundle and SPEC item, every deviation, and the
next expected action. No length cap. If any gate is RED, do not repair on your
own initiative: report it and stop.
