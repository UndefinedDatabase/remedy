# STEP 25 — F033 Hunk-level diff approval (SESSION 7, round 25; the soft limit is reached at this round)

Goal: book the round 24 PASS and the `Done: R-0748` resolution into the record,
then retire the SAME false claim from the THIRD file it stands in — the
`compose_builder_prompt` docstring in `packages/orchestration/pingpong_loop.py`,
which still tells a reader that the job-level hop is unwired after round 24
wired it. Registered below as R-0749.

## Bundle — the list that is executed

1. C0a: save this block verbatim to `.agent/authored/f033-r25.md`.
2. C0b: mirror the same bytes into `.agent/last_block.md`.
3. C1: rewrite `.agent/plan.md` from slice PLAN25.
4. C2: append slice RECORD25 to `.agent/live_review.md` — books the round 24
   PASS, RESOLVES R-0748 and REGISTERS R-0749.
5. C3: append slice SLIPS25 to `.agent/prose_slips.md`.
6. C4: SPEC A — the R-0749 repair, pair PAIR-ROUTE, and in the SAME commit the
   `Landed: R-0749` line of SPEC A3.
7. C5: rewrite `.agent/handoff.md` as the handback.

## Change set — exactly these paths, nothing else

    .agent/authored/f033-r25.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    packages/orchestration/pingpong_loop.py
    .agent/handoff.md

## What the reviewer measured before writing this block, and where

Every reading below was taken by the reviewer at `d81acca5`, this round's base.

- THE DEFECT IS REAL AND IT IS EXACTLY ONE SPAN. `git grep -c -F` over the
  tracked content of `packages`, `apps`, `tests` and `docs` answers 1 for each
  of `no round has wired`, `ONE HOP STILL MISSING` and
  `this segment never registers`, and every one of those three hits is
  `packages/orchestration/pingpong_loop.py`. No other file carries the claim.
- THE CLAIM IS FALSE AT THIS BASE. The paragraph says the job-level caller is
  unwired and that production `hunk_ledger` is therefore `None`. Round 24
  landed that wiring: `packages/orchestration/pingpong_job.py` defines
  `_recorded_hunk_ledger_for_task` and its `run_pingpong` call passes
  `hunk_ledger=_recorded_hunk_ledger_for_task(job, task)`.
- R-0748's OWN PREDICATE STILL HOLDS, so resolving it is honest: over the same
  four trees `persists no decision` occurs 0 times. That predicate was
  STRING-scoped, this third instance carries the same claim in other words, and
  that is precisely why it survived a green gate — which is what R-0749's fix
  clause is written against.
- NO TEST READS THIS DOCSTRING. `tests/orchestration/test_builder_prompt_golden.py`
  pins RENDERS, not source bytes; `test_builder_prompt_hunk_rejections.py`
  mentions the module by path in its own prose only; and no test in the
  repository asserts any substring of `compose_builder_prompt.__doc__`.
- THE FROM SPAN of PAIR-ROUTE occurs EXACTLY ONCE in its file at `d81acca5`:
  1260 bytes over 17 lines.
- THE AST GATE OF G5 DISCRIMINATES, dry-run by the reviewer at `d81acca5` with a
  red control: comparing `ast.dump` of the module with every docstring constant
  blanked, the repaired file answers True against the base and a control that
  additionally renames the `builder_directive` segment literal answers False.
- `python3 -m ruff check --stdin-filename packages/orchestration/pingpong_loop.py -`
  over the repaired bytes exits 0.

## SPEC A — the R-0749 repair

A1. Apply PAIR-ROUTE below to `packages/orchestration/pingpong_loop.py`. The
reviewer ran the containment test at `d81acca5` and the result is
`TO contains FROM: false`, so it is a REWRITE and the obligation is
PAIRROUTE-FROM 0x and PAIRROUTE-TO exactly 1x in the file after the commit.
Report both counts.

A2. Change NOTHING else in that file. This round alters a docstring and no
executable statement, which is what G5's AST reading measures. If applying the
pair seems to require any other edit, stop and declare it rather than making it.

A3. In the SAME commit append to `.agent/live_review.md` exactly one line:

    Landed: R-0749 — the retired claim's third instance is removed from compose_builder_prompt's docstring, packages/orchestration/pingpong_loop.py, C4 of round 25.

Write NO `Done:` paragraph. `Done:` is reviewer-authored text only.

## Slice PLAN25 — the FULL new bytes of `.agent/plan.md`

The slice is every byte BETWEEN the two marker lines, exclusive. The markers are
not part of any file.

<<<BEGIN PLAN25
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 7 of this feature, which is the last under
the amend0827 rule 6 soft limit; the scope report it requires is written.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 stable ids, viewer v2, consolidation | done | round 5 |
| T002 decision core, subset apply, ledger, the door | done | rounds 6-15 |
| T003 partial truth on all three surfaces, R-0738 | done | rounds 16-19 |
| T003 rejection to repair, rendered, wired, end to end | done | rounds 20-24 |
| THE FEATURE'S FUNCTIONAL SCOPE | complete | at round 24 |
| R-0749, the retired claim's third instance | open | this round |
| the operator guide for `patch approve-hunks` | open | next round |
| the integration gate round | open | after the guide |
| the closure sequence and its pull request | open | after the gate |
| R-0745, the door's transitive import closure | open | carried as a risk |

## Next Steps
1. This round books the round 24 PASS and the `Done: R-0748` resolution, and
   retires the same false claim from the third file it reached.
2. Then the `docs/` round: an operator guide for `remedy patch approve-hunks`
   under `docs/guides/`, registered in the `docs/README.md` index in the same
   commit, gated with `python3 -m pytest tests/docs/ -q` beside the canary.
3. Then the integration gate per docs/agents/integration_gate.md, then the
   closure sequence and its pull request.
4. R-0745 is Low and is not reachable from this feature's Acceptance. The
   closure protocol's precondition 1 admits a documented Medium/Low risk, so it
   is carried as one rather than blocking a feature that has met its Acceptance.

## Risks
- R-0745 stays OPEN at closure and the STATUS line therefore reads
  PASS_WITH_RISKS. Its fix recommends a transitive-closure guard test, which is
  a hardening task deserving its own round rather than a corner of a closure.
<<<END PLAN25

## Slice RECORD25 — appended to `.agent/live_review.md`

Three paragraphs, blank-line separated.

<<<BEGIN RECORD25
Gate: F033 R24 — THE JOB-LEVEL CALLER SUPPLIES THE RECORDED LEDGER, AND THE FEATURE'S FUNCTIONAL SCOPE CLOSED. THE ROUND PASSED. This entry books, under operator amendment amend0827-process-diet rule 1, the verdict the SESSION-6 reviewer reached at `a54f943e` and committed and pushed in `.agent/handoff.md` at `d81acca5`; it is written into this record by the first commits of round 25 rather than by a round of its own, and every reading in this paragraph is that reviewer's, taken at `a54f943e`, not a re-run by the session-7 reviewer that writes it here. TRANSPORT: `cmp` of the committed `.agent/authored/f033-r24.md` against that reviewer's own pre-emission original was SILENT, as was the comparison against `.agent/last_block.md`; the worker copied the file with `shutil.copyfile` rather than retyping it. That chain walks the saved copy, its mirror and the working copy, so it establishes SELF-CONSISTENCY and is not a claim about the emitted bytes. THE PAIR: PAIRDOC-FROM occurs 0 times and PAIRDOC-TO exactly 1 time in the acceptance test file, and round 23's superseding comment block is preserved untouched, as ordered. THE SWEEP, which is R-0748's actual fix: `persists no decision` and `persists NOTHING` each occur ZERO times across `packages/`, `apps/`, `tests/` and `docs/`, confirmed in four independent forms — `git grep` over tracked content, a source-only grep, and a broad grep that also reads binaries — all at REAL exit 1. THE PROSE FILES: `.agent/plan.md` byte-EQUAL to PLAN24 at 46 lines; `.agent/prose_slips.md` reconstructs 30807 plus one newline plus 529 to 31337. THE RECORD APPEND at `90af5927` reconstructs 1595141 plus one newline plus 7458 to 1602600, base a byte PREFIX, slice an exact SUFFIX, N COUNTED at 2, and a negative control at byte 1596121 — that reviewer's own offset, inside the FIRST appended paragraph's span 1595142 to 1600036 — REJECTED by both readers, which accepted the unflipped bytes. THE LEDGER: registered 308 to 309 with the ADDED id exactly `R-0748`; `Done:` 53 lines over 51 distinct UNMOVED at all three revisions; `Landed:` 19 to 20 with `^Landed: R-0748 — ` 0 before C4 and exactly 1 at it; `^Gate: F033 R23 — ` 0 before and exactly 1 after; and the open set 257 to 258. THE CODE: `python3 -m ruff check` exits 0 over all three changed files; the helper is module-level; and the `run_pingpong` call passes `hunk_ledger=_recorded_hunk_ledger_for_task(job, task)`. THE MUTATIONS were re-run in that reviewer's own disposable worktree at C6 with its OWN anchors, each asserted UNIQUE and the file restored and proved byte-identical by sha256: control a REAL exit 0 at 10 passed; a fixed task id is exit 1 at 4 failed, naming the different-task test and the job-scope boundary test; removing the structural guard is exit 1 at exactly 2 failed, both attribute-access cases, which shows the outer guard and the reader's own guard are measured by DISJOINT tests; and removing the wiring is exit 1 at 1 failed. THE SUITES were re-run SERIALLY in the primary checkout, every REAL exit 0: the five orchestration suites 274 together, and the canary 42. THE STRUCTURE: nine single-parent commits over `c9dd471f`..`a54f943e` of 334, 262, 22, 4, 2, 11, 49, 241 and 262 insertions, every one under 500, the last being the handback commit no gate of the block could reach; and the path set to C6 EQUALS the declared change set in BOTH directions. TWO DEVIATIONS WERE WORTH MORE THAN THE GATES AND BOTH ARE RECORDED HERE. The first: G5 went RED on its first run because a plain recursive grep matched a stale gitignored `__pycache__` artifact compiled from the pre-repair source while `git grep` over tracked content was already clean — the fault is the REVIEWER'S GATE, not the repository, and the counter-measure is to sweep TRACKED CONTENT. The second: the worker observed that a worktree mutation could import the PRIMARY checkout through a `.pth` on `sys.path` and therefore be vacuous, and the reviewer SETTLED it rather than accepting it — measured at `5cb87f37`, under `cwd=<worktree>` both a plain script run and a pytest run resolve `packages.orchestration.pingpong_job` to the WORKTREE's copy, because the working directory precedes the `.pth` entry, so the mutation proofs of rounds 21 through 24 were not vacuous and the reds corroborate it independently.

Done: R-0748 — THE FALSE CLAUSE IS GONE FROM THE ACCEPTANCE TEST AND THE FINDING'S OWN PREDICATE IS MET, WHILE THE CLAIM IT NAMED SURVIVES ELSEWHERE AND IS REGISTERED BELOW AS R-0749. The fix landed at `7cb78726` on `tests/orchestration/test_builder_prompt_hunk_rejections.py`: the module-docstring paragraph was rewritten so the retired reason is gone rather than annotated, and round 23's superseding comment block lower in the file was left untouched, exactly as the fix clause asked. THE PREDICATE THIS FINDING SET ITSELF IS MEASURED AND HOLDS: the session-7 reviewer re-ran the sweep at `d81acca5` with `git grep -c -F` over the tracked content of `packages`, `apps`, `tests` and `docs`, and `persists no decision` occurs 0 times there. R-0748 IS THEREFORE RESOLVED AND ITS SUCCESSOR IS NOT A REOPENING. What the predicate could not reach is stated plainly because it is the lesson: the clause was worded as a STRING sweep over a CLAIM-scoped defect, so a third instance carrying the same claim in different words passed the gate untouched. R-0749 below is that instance, and its own resolution is worded over the CLAIM rather than over any wording of it. This is the third file the one claim reached — `pingpong_loop.py` as R-0747, the acceptance test as R-0748, and `pingpong_loop.py`'s own docstring again as R-0749 — and the count is recorded here because it is the argument for gating a claim semantically the first time.

- R-0749 — Low, THE CLAIM R-0747 AND R-0748 RETIRED IS STILL STANDING IN A THIRD PLACE, AND ROUND 24 IS WHAT MADE IT FALSE. Raised by the reviewer at the F033 R24 gate, in the round that books that gate. MEASURED at `d81acca5`: `packages/orchestration/pingpong_loop.py` gives `compose_builder_prompt` a docstring paragraph headed "THE ROUTE FROM A STORED DECISION, AND THE ONE HOP STILL MISSING", which tells a reader that "What no round has wired yet is the JOB-level caller: `packages/orchestration/pingpong_job.py` ... and until it does, production `hunk_ledger` is `None` and this segment never registers." ROUND 24 WIRED EXACTLY THAT CALLER, at `7c02e01f`: `pingpong_job.py` defines `_recorded_hunk_ledger_for_task` and its `run_pingpong` call passes `hunk_ledger=_recorded_hunk_ledger_for_task(job, task)`, so production `hunk_ledger` is a real ledger whenever the task has a recorded decision and the segment does register. The paragraph was TRUE when it was written and round 24 falsified it without touching it — which is a different failure from R-0747 and R-0748, where the sentence was false on the day it landed, and it is why the finding is raised against the round that made it false rather than against the round that wrote it. WHY LOW: no behaviour is wrong, no test is weakened, and by AST the module's statements are untouched by the repair; the defect is a false explanatory paragraph in a production module, met by a reader trying to learn where the feature's last hop lives — and this paragraph is the one place in the source that documents that route end to end, so a reader who trusts it concludes the feature is unfinished. WHY IT ESCAPED TWICE OVER, which is the part worth keeping: R-0748's resolution predicate counted a STRING over four trees, and this instance carries the same claim in entirely different words, so the gate was green and the claim was alive; and no gate of round 24 asked what its OWN change had falsified elsewhere. A round that completes a route named in prose must sweep the prose that names it. FIX: rewrite that paragraph so it states the route as it now IS, naming the commit its reading was taken at, and leave every executable statement of the module unchanged. Resolved when no file under `packages/`, `apps/`, `tests/` or `docs/` asserts that the job-level `hunk_ledger` hop is unwired, unbuilt or missing — a reading taken over the CLAIM and not over any one wording of it.
<<<END RECORD25

## Slice SLIPS25 — appended to `.agent/prose_slips.md`

One paragraph.

<<<BEGIN SLIPS25
2026-08-29 · F033 R24 · The block's G5 ordered an absence swept "across `packages/`, `apps/`, `tests/` and `docs/`" and a plain recursive grep run that way also reads gitignored build artifacts, so the gate went red against a stale `__pycache__` object compiled from the pre-repair source while `git grep` over tracked content was already clean; the worker removed that one file by exact path, re-ran the gate unmodified and declared it, and an absence gate must be worded and run over TRACKED CONTENT, because such a gate can be red while the source property holds and green while it does not.
<<<END SLIPS25

## Pair PAIR-ROUTE — `packages/orchestration/pingpong_loop.py`

Containment test run by the reviewer at `d81acca5`: `TO contains FROM: false`.
It is therefore a REWRITE, and the gate is PAIRROUTE-FROM 0x and PAIRROUTE-TO
exactly 1x after the commit. The FROM occurs exactly once in the file at that
commit, at 1260 bytes over 17 lines. Both texts are indented four spaces,
because both sit inside a function docstring; the indentation is part of the
bytes.

<<<BEGIN PAIRROUTE-FROM
    THE ROUTE FROM A STORED DECISION, AND THE ONE HOP STILL MISSING.
    :func:`run_pingpong` now carries a ``hunk_ledger`` parameter of its own and
    forwards it UNCHANGED to the call below, so the loop supplies whatever
    ledger it is GIVEN. It does not go and find one: it holds no job.
    ``packages/orchestration/hunk_decision_record.py`` writes each exported
    ledger onto ``job.metadata`` under the key ``hunk_decisions``, keyed by
    attempt, ``save_job`` at the write door makes that record durable, and the
    same module reads the latest one back for a task with
    ``load_latest_hunk_ledger_from_metadata`` — that reader takes the metadata
    MAPPING, so it drags no storage behind it. What no round has wired yet is
    the JOB-level caller: ``packages/orchestration/pingpong_job.py`` is where
    the job is actually held at its :func:`run_pingpong` call, so it is the one
    place that can read the decision and pass it, and until it does, production
    ``hunk_ledger`` is ``None`` and this segment never registers. That hop is
    deliberately its own round, because a call site wired without a test that
    follows a decision through to the composed prompt would look like the
    feature working while proving nothing at all.
<<<END PAIRROUTE-FROM

<<<BEGIN PAIRROUTE-TO
    THE ROUTE FROM A STORED DECISION, AND WHERE EACH HOP LIVES.
    :func:`run_pingpong` carries a ``hunk_ledger`` parameter of its own and
    forwards it UNCHANGED to the call below, so the loop supplies whatever
    ledger it is GIVEN. It does not go and find one: it holds no job.
    ``packages/orchestration/hunk_decision_record.py`` writes each exported
    ledger onto ``job.metadata`` under the key ``hunk_decisions``, keyed by
    attempt, ``save_job`` at the write door makes that record durable, and the
    same module reads the latest one back for a task with
    ``load_latest_hunk_ledger_from_metadata`` — that reader takes the metadata
    MAPPING, so it drags no storage behind it. THE JOB-LEVEL CALLER IS WIRED:
    measured at ``d81acca5``, ``packages/orchestration/pingpong_job.py`` holds
    the job at its :func:`run_pingpong` call and passes
    ``hunk_ledger=_recorded_hunk_ledger_for_task(job, task)``, so a decision an
    operator recorded for a task reaches this segment in production. ``None``
    stays the answer for a round with no recorded decision, and the segment
    then registers not at all — which is the ordinary case, not a gap.
<<<END PAIRROUTE-TO

## Constraints

1. Apply every slice and the pair BYTE FOR BYTE. If one looks wrong, apply it as
   written and declare the problem; never silently repair it.
2. PLAN25 is a FULL REWRITE. RECORD25 and SLIPS25 are APPENDS. Measured by the
   reviewer at `d81acca5`, `.agent/live_review.md` is 1602790 bytes and
   `.agent/prose_slips.md` is 31337 bytes, and BOTH end with a newline, so each
   append is one blank-line separator then the slice. RE-MEASURE both yourself
   at the commit you append at rather than trusting these numbers: the R23 block
   got one of them wrong by reading it at the wrong commit.
3. `.agent/live_review.md` is written by TWO commits: C2 appends RECORD25, C4
   appends the single `Landed:` line. G3's arithmetic is measured at C2 and
   G4's ledger readings at `d81acca5`, at C2 and at C4.
4. Do NOT delete or edit any landed `Landed:`, `Done:` or `Gate:` text. The
   record is append-only.
5. Touch no path outside the change set. In particular do NOT touch
   `packages/orchestration/pingpong_job.py`,
   `tests/orchestration/test_builder_prompt_hunk_rejections.py`,
   `tests/orchestration/test_pingpong_job_hunk_ledger.py`, or anything under
   `docs/`. The `docs/` guide is the NEXT round's work and is not this one's.
6. The sandbox denies `VAR=x cmd`, `env`, `export`, `cp`, `$(...)` inside a
   compound, process substitution, a heredoc nested in `bash -c`, and a shell
   line containing a brace with a quote inside it. Write scripts under
   `.remedy-wt/` and run them as `python3 -B <path>`; use `python3 -m ruff`.
   REAL exit codes come from `bash -c '<cmd>; echo "REAL_EXIT=$?"'` with NO PIPE.
7. Every absence gate of this round is run over TRACKED CONTENT with
   `git grep`, never with a plain recursive grep — that is the round 24 lesson
   recorded in SLIPS25, and applying it here is the point of recording it.
8. This round mutates no executable code, so it orders NO mutation red-proof and
   needs no disposable worktree. G5's AST reading is what stands in its place,
   and the reviewer dry-ran it with a red control before ordering it. The
   primary checkout satisfies `git status --porcelain` empty at the handback.
9. Re-read `.agent/STOP` before starting. If it exists, stop and hand off.
10. G1 through G7 all run at C4, before the handback commit C5.

## Done when — G1 through G7

G1 TRANSPORT. Report `sha256` and byte length of the committed
`.agent/authored/f033-r25.md`, and the same two readings for
`.agent/last_block.md`. One digest comparison; the reviewer holds the
pre-emission original and runs the other half itself.

G2 THE PROSE FILES. `.agent/plan.md` byte-EQUAL to PLAN25, under 50 lines,
holding `## Goal` and the substring `Steps`. `.agent/prose_slips.md`
reconstructs its MEASURED base plus one newline plus the byte length of SLIPS25
to its committed size; report all three numbers, the base measured and not taken
from this block.

G3 THE RECORD APPEND, at C2. Reconstruct the MEASURED base plus one newline plus
the byte length of RECORD25 to the committed size. Prove the pre-commit blob a
byte PREFIX and the slice an exact SUFFIX. COUNT N in the script. Compare the
file's LAST N blank-line units against the slice's paragraphs IN ORDER. Flip one
byte inside the FIRST appended paragraph, report the offset, prove it lies in
that paragraph's span, and show BOTH readers reject the flipped bytes and accept
the unflipped ones.

G4 THE LEDGER, at `d81acca5`, at C2 and at C4: `^- R-\d+ — ` 309 distinct going
to 310 with the ADDED id exactly `R-0749`; `^Done: R-\d+ — ` 53 lines over 51
distinct going to 54 over 52 with the ADDED resolved id exactly `R-0748`;
`^Landed: ` 20 going to 21 with `^Landed: R-0749 — ` 0 before C4 and exactly 1
at it, and the landed `Landed: R-0748` line still standing; `^Gate: F033 R24 — `
0 before and exactly 1 after; and the open set 258 going to 258 — one
registration and one resolution in the same round, so report BOTH ends and the
intermediate value at C2.

G5 THE REPAIR IS A DOCSTRING AND NOTHING ELSE, at C4. Report each of these with
its real reading. (a) `python3 -m ruff check
packages/orchestration/pingpong_loop.py` exits 0. (b) In that file the
PAIRROUTE-FROM text occurs 0 times and the PAIRROUTE-TO text exactly 1 time.
(c) THE AST READING: parse the file at `d81acca5` and at C4, blank every
docstring constant of every module, class and function node in both trees, and
show `ast.dump` of the two is EQUAL — so not one executable statement moved.
Print the two dumps' lengths and the boolean.

G6 THE CLAIM IS GONE, SWEPT SEMANTICALLY. With `git grep` over TRACKED content
of `packages`, `apps`, `tests` and `docs`, at C4: each of the three strings
`no round has wired`, `ONE HOP STILL MISSING` and `this segment never registers`
occurs 0 times, and `persists no decision` also occurs 0 times, which is
R-0748's own predicate re-measured at the commit that resolves it. Report the
command and all four counts. Then READ, and report in one sentence each, every
remaining hit of `git grep -n -F "hunk_ledger" -- packages apps` that is a
COMMENT or DOCSTRING rather than code, and say for each whether it asserts the
hop is unwired. This half is a reading, not a count: R-0749's resolution is
worded over the CLAIM, so a count of three strings cannot discharge it alone.

G7 SUITES AND STRUCTURE, at C4. SERIALLY, each with its REAL exit code and pass
count: `python3 -m pytest tests/orchestration/test_builder_prompt_hunk_rejections.py -q`;
`python3 -m pytest tests/orchestration/test_builder_prompt_golden.py -q`;
`python3 -m pytest tests/orchestration/test_pingpong.py -q`; and the canary
`python3 -m pytest tests/cli/test_golden_path.py -q`. Then `git status
--porcelain` EMPTY; per-commit insertions from C0a through C4 each under 500;
and the path set over `d81acca5`..C4 equal to the change set minus
`.agent/handoff.md` in BOTH directions.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, SESSION 7 of F033, branch, commit SHAs, changed-files table, one line per
gate G1 through G7 with its REAL exit code, the open-findings count, an
item-status table covering every Bundle and SPEC item, every deviation, and the
next expected action. No length cap. If any gate is RED, do not repair on your
own initiative: report it and stop.
