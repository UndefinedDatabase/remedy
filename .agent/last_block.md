── STEP T003 — F275 — ROUND 83 ──
Goal: Collapse the two job-id resolvers into ONE function that reaches both job stores,
pin it with tests that go red when either half is undone, and measure exactly how far that
carries a ping-pong job id through a real command — which is one step, not all the way.

Base commit: `afffd7cc`. Round type: SPLIT. This round changes PRODUCTION CODE, so it is
never self-certified: the reviewer re-runs every gate and every red-proof before a verdict.

THE FRAME RULE, per item 37 of `docs/agents/planner_reviewer_prompt.md` §3, stated as the
property MEASURED over the final bytes: NO LINE of this block is a run of a single repeated
character, and every box-drawing rule inside the STEP and SLICE header lines is exactly two
characters long.

## Bundle — the ordered commit sequence

C0a  `.agent/authored/f275-r83.md`          the block, saved verbatim
C0b  `.agent/last_block.md`                 mirrored FROM THE COMMITTED C0a BLOB
C1   `.agent/plan.md`                       slice PLAN83, a full replacement
C2   `.agent/live_review.md`                slice RECORD83 appended
C3   `.agent/prose_slips.md`                slice SLIPS83 appended
C4   `packages/orchestration/data_paths.py` the collapse, written to SPEC P below
C5   `tests/test_data_paths.py`             the three tests, written to SPEC T below
C6   `apps/cli/commands/job_context_cmd.py` one comment the collapse falsifies
C7   `.agent/decisions.md`                  slice DEC83 appended
C8   `.agent/handoff.md`                    the handback

C1 is the FIRST SUBSTANTIVE COMMIT because this round touches the finding ledger, per item
23 of §3. C4 precedes C5 so that no commit adds a failing test: the reviewer measured that
the collapse alone changes no test's colour in the scoped suite, and the three new tests
without it would fail.

## Change — exactly these paths and no others

The paths listed in the Bundle are the whole change set. Under `packages/`, `apps/` and
`tests/` exactly the three paths of C4, C5 and C6 change. NOTHING under `docs/` or `scripts/`.
The 37 `UUID(...)` parses in the handler layer are NOT touched here — see SPEC P's last
paragraph and DEC83.

## SPEC P — `packages/orchestration/data_paths.py`, at C4

The file carries two resolvers that differ in ONE statement. `resolve_job_id` assigns
`matches = _classic_job_id_matches(raw)` and so searches the classic store alone;
`resolve_any_job_id` assigns the union of that and `_task_job_id_matches(raw)`. Measured at
`afffd7cc`: the two bodies are otherwise identical, down to both exit messages and codes.

1. In `resolve_job_id`, the statement assigning `matches` becomes EXACTLY this line, indented
   four spaces, so the red control below can find it uniquely:
       matches = sorted(set(_classic_job_id_matches(raw)) | set(_task_job_id_matches(raw)))
   Nothing else in that body changes: the `UUID(raw)` fast path, the `_SHORT_HEX_RE` guard,
   both messages and both exit codes stay byte-identical.
2. `resolve_job_id`'s docstring is REWRITTEN so it is true: it searches BOTH stores; it
   returns a `str` because only one of the two id shapes is a UUID; it is read-only; it
   exits 1 on invalid input or no match and 2 on an ambiguous prefix. Carry across the
   facts the deleted `resolve_any_job_id` docstring held that are still true — the FILE
   versus DIRECTORY distinction under one `jobs/` directory, the operator dogfooding
   incident of 2026-08-25, and why a dedupe makes an id present in both stores one match.
3. The whole `def resolve_any_job_id` — signature, docstring and body — is DELETED, and in
   its place stands a short comment and then EXACTLY this statement, on a line of its own
   at column 0:
       resolve_any_job_id = resolve_job_id
   The comment says it is an ALIAS and not a copy, so the two cannot drift apart again;
   that the name is kept because callers under `apps/cli/` read it as saying they need both
   stores; and that `tests/test_data_paths.py` pins the identity.
4. The module docstring's `Public API::` table stops saying `resolve_job_id` reads "the
   classic store" and stops listing `resolve_any_job_id` as a separate function.

WHAT SPEC P DOES NOT DO, AND DEC83 RECORDS WHY. The reviewer probed the shipped handler
`_cmd_job_status` in `apps/cli/commands/job.py` against a ping-pong job with this change
applied. The resolver now FINDS the id, and the handler then exits 1 with
`Error: job not found: <id>`, because it loads through the classic store. So this commit
moves that command's failure ONE STEP LATER; it does not make the command work. Making it
work is the handler-layer half DECISION F275 D37 names — measured at `afffd7cc` as 37
`UUID(...)` calls whose argument names a job, in 16 files under `apps/cli/` — and it is not
this round.

## SPEC T — `tests/test_data_paths.py`, at C5

Add three tests to the existing class `TestResolveJobId`, with EXACTLY these names, each
setting `REMEDY_DATA_DIR` to `tmp_path` through `monkeypatch` as that class's other tests do:

 `test_a_pingpong_job_id_resolves_through_the_one_resolver` — writes one ping-pong record,
   a `job.json` inside the directory `jobs_dir() / mint_job_id()`, and asserts that
   `resolve_job_id` returns that id for BOTH the full id and its first eight characters.
 `test_a_prefix_matching_both_stores_is_ambiguous` — writes a classic record
   `abcd1234-0000-0000-0000-000000000001.json` and a ping-pong directory `abcd12340000beef`
   holding a `job.json`, both under `jobs_dir()`, and asserts that `resolve_job_id("abcd1234")`
   raises `SystemExit` with code 2.
 `test_the_two_resolver_names_are_one_function` — asserts
   `data_paths.resolve_job_id is data_paths.resolve_any_job_id`.

No existing test is edited or deleted. The reviewer read every existing test in that file
that calls either resolver, at `afffd7cc`, and none asserts that a ping-pong id is REJECTED,
so no existing assertion is contradicted by the collapse.

## SPEC C — `apps/cli/commands/job_context_cmd.py`, at C6

One comment, inside the function that calls `resolve_any_job_id`, says in the present
tense that `resolve_job_id` "searched the classic store alone". Rewrite that comment so it
says this was true UNTIL F275 T003 collapsed the two resolvers, and that the call site keeps
the name that states what it needs. No executable line of that file changes.

## Constraints

1. NO SLICE IS EDITED. PLAN83, RECORD83, SLIPS83 and DEC83 land byte for byte. A
   discrepancy inside one is DECLARED in the handback, never repaired.
2. C4, C5 and C6 are the worker's OWN code, written from the SPECs. The reviewer wrote a
   candidate of all three in a disposable worktree to measure this block's figures and has
   NOT supplied it; the worker does not look for it.
3. READ `.agent/STOP` FROM DISK before C0a and again before C8, recording both readings with
   real exit codes. If it appears, finish the commit in hand, write the handoff and end.
4. Every commit stages EXACTLY ONE path and stays under 500 insertions.
5. No `.py` file is created under `.agent/`. Scratch lives under `.remedy-wt/`, uncommitted.
6. No landed DECISION is rewritten; DEC83 is an APPEND and C7's deletion column is ZERO.
7. No `gh` and no `remedy` command. No pull request, no branch created or deleted, no merge,
   NEVER a force-push, no history rewrite.
8. THE RED-PROOF WORKTREE, per `docs/agents/self_drive_protocol.md` G5, is created with
   `git worktree add --detach` at C6 and REMOVED AND PRUNED before C7, so `git worktree list`
   shows the primary checkout alone when G7 runs. Nothing destructive touches the primary
   checkout.
9. THE SCOPED SUITE RUNS IN THE PRIMARY CHECKOUT, never in the worktree: `apps/ui/node_modules`
   is gitignored and absent from a fresh worktree, and the reviewer measured that absence
   turning `tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`
   red in a PRISTINE worktree at `afffd7cc`, with no change applied at all.
10. THE BLOCK'S OWN SIZE, measured on its final bytes: 315 lines TOTAL and 238 lines of PROSE,
    against the caps of 490 and 400.
11. THE GATES RUN AT TWO COMMITS, AND THIS CONSTRAINT IS WHERE THAT IS STATED. G4, G5 and G6
    run at C6, because DEC83 at C7 carries their results and item 31 of §3 requires a gate
    whose reading an authored text states to run at a commit STRICTLY EARLIER than the commit
    writing it. G1, G2, G3, G7 and G8 run at C7. No gate is ordered after C8. C8's own
    insertion count and path go nowhere in this round: the REVIEWER measures them at the next
    gate and books them in the ledger. G8 is scoped to `afffd7cc`..C7 and G7's path set
    compares against the Bundle MINUS `.agent/handoff.md`.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r83.md` at C0a compared with `cmp`
against the block as received; `.agent/last_block.md` at C0b byte-identical to the COMMITTED
C0a blob. Extract each slice by its BEGIN and END markers, report how many the extraction
FOUND, and check each against the sha256 on its own BEGIN marker. Re-measure TOTAL and PROSE
against constraint 10; PROSE is TOTAL minus the slices' lines.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN83 re-extracted from the COMMITTED
C0a blob; at most 50 lines; exactly one `## Goal` and exactly one `## Next Steps`.

G3 THE RECORD, FULL FORENSICS, for `.agent/live_review.md` at C2 and `.agent/decisions.md` at
C7. READER A: post-commit file equals pre-commit blob followed by exactly the slice, the
arithmetic printed; the pre-commit lengths are 1100820 and 1248878. READER B, independent and
structural: the file's LAST N blank-line-separated units equal the slice's N paragraphs IN
ORDER, N COUNTED BY THE SCRIPT from the slice. For each append a NEGATIVE CONTROL flipping
one ASCII letter inside the FIRST appended paragraph, REJECTED by BOTH readers. Both deletion
columns 0. `.agent/prose_slips.md` at C3 equals its pre-commit blob of 289390 bytes followed by
exactly SLIPS83, deletion column 0. DERIVE the ledger's entry-header pattern from the headers
already in the file, report how many it matches, and report that RECORD83's header matches it
and duplicates none byte for byte.

G4 THE PRODUCTION CHANGE, READ STRUCTURALLY at C6 with `ast`, not with a grep. Report: the
count of `FunctionDef` nodes named `resolve_job_id`, which must be 1; named
`resolve_any_job_id`, which must be 0; the count of lines of the file EXACTLY equal to
`resolve_any_job_id = resolve_job_id`, which must be 1; the count of lines EXACTLY equal to
the four-space-indented `matches` statement of SPEC P item 1, which must be 1, and that it
lies inside `resolve_job_id`'s line span; and that NO line of `resolve_job_id` assigns
`matches = _classic_job_id_matches(raw)`. Import the module fresh and report
`resolve_job_id is resolve_any_job_id`. Report `git diff --numstat afffd7cc` for each of the
three production and test paths. `ruff check` over exactly those three paths exits 0.

G5 THE BEHAVIOUR, in the PRIMARY checkout at C6. (a) The three tests of SPEC T by node id,
each PASSED. (b) The scoped suite
`python3 -B -m pytest tests/test_data_paths.py tests/cli/ tests/orchestration/ -q -p no:randomly`
with its passed, skipped and failed totals REPORTED AS MEASURED and the failure set, which must
be EMPTY. The reviewer measured this exact command at `afffd7cc` in the primary checkout at
13252 passed, 10 skipped and 0 failed; state the difference and account for it. (c) THE
HANDLER PROBE, run in scratch and not committed: with `REMEDY_DATA_DIR` pointing at an empty
scratch root holding ONE ping-pong record, call `_cmd_job_status` from
`apps/cli/commands/job.py` with that record's full id, and report its exit code and its stderr
verbatim. Then do the same at `afffd7cc`'s version of `data_paths.py`, read with `git show`
into a scratch copy of the tree, never by overwriting the primary checkout. The two stderr
lines are what DEC83's second CHOSEN paragraph rests on.

G6 THE MUTATION RED-PROOFS, in the disposable worktree of constraint 8, at C6. FIRST, inside
that worktree, import `packages.orchestration.data_paths` and PRINT its `__file__`: it must
resolve INSIDE the worktree. The reviewer measured a probe whose test file sat outside the
worktree importing the PRIMARY checkout's module instead, so no mutation reached it — a
red-proof that cannot fail. Run every command below from inside the worktree against the
worktree's own `tests/test_data_paths.py`, scoped to the three SPEC T node ids.
 CONTROL, unmutated: all three PASS, with the exit code.
 M1: replace the one line of `data_paths.py` EXACTLY equal to SPEC P item 1's statement with
   `    matches = _classic_job_id_matches(raw)`. Required colours:
   `test_a_pingpong_job_id_resolves_through_the_one_resolver` FAILS,
   `test_a_prefix_matching_both_stores_is_ambiguous` FAILS,
   `test_the_two_resolver_names_are_one_function` PASSES.
 M2: restore, then replace the one line EXACTLY equal to `resolve_any_job_id = resolve_job_id`
   with a three-line `def resolve_any_job_id(raw: str) -> str:` whose body returns
   `resolve_job_id(raw)`. Required colours: the identity test FAILS and the other two PASS.
   BEFORE EACH MUTATION, report the count of lines EXACTLY equal to its target in that file;
   each must be 1. The text of M2's target also occurs INSIDE the module docstring's table
   once SPEC P item 4 is applied, which is why the match is on the WHOLE LINE and not on a
   substring, per item 25 of §3.
 Report each run's three colours and exit code, then remove and prune the worktree.

G7 TREE, CANARY, LINT, PATH SET, OPEN SET. `git status --porcelain` prints `''` at C7.
`git worktree list` has exactly one row. THE CANARY
`python3 -B -m pytest tests/cli/test_golden_path.py -q` exits 0 at the count it measures;
the reviewer measured 42 passed at `afffd7cc`. `ruff check .` exits 1 by its own design:
count its location rows AND cross-check that count against its own `Found <n> errors.` line;
the two must agree, and the reviewer measured 26 at `afffd7cc`, the frozen ceiling. The
changed-path set of `afffd7cc`..C7 against the Bundle MINUS `.agent/handoff.md`, MISSING and
EXTRA by name. The open set derived mechanically at `afffd7cc` and at C7 — every
`^- R-\d+ — ` minus every `^Done: R-\d+ — `, BY DISTINCT ID — with both counts, the
membership difference each way, and whether `R-0809` and `R-0880` are open at each. The
reviewer measured 87 open at `afffd7cc`. The registered, resolved and de-registered sets must
all be EMPTY.

G8 THE INSERTION CAP. Per-commit insertion and deletion counts over `afffd7cc`..C7, one row per
commit, each commit's staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md` — the Session line reading
`SESSION 29 of feature F275 · round 83 · rounds so far 83`; the Commits table with `+/-` cells
READ FROM `git show --numstat` and compared cell by cell against G8, C8's own row carrying no
numbers and saying why; the Verification table at one line per gate with its REAL exit code;
External actions; Authored-text proofs; Item-status; Deviations; and a `## Next` stating
`Operator questions open: 0`. NO SCOPE REPORT AND NO SESSION-LIMIT BANNER IS OWED, by amendment
amend0911-f275-to-scope.

── SLICE PLAN83 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN83 sha256=a88a9ab6fd644ad43dd61110b2d33bcb050695b8e3d5773a008be4e8a1f6d869
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 83 COLLAPSES THE TWO JOB-ID RESOLVERS INTO ONE. `resolve_job_id` now searches both job
stores and `resolve_any_job_id` is an alias of it rather than a second copy, which is the half
of DECISION F275 D37's seam that F260 T004 named. Three tests pin it, and the round red-proves
each against its own mutation. The round also measures how far that carries a ping-pong id
through `job status`; the reviewer's dry run before authoring found it is one step — the
resolver finds the id and the handler then fails loading it from the classic store. The round
82 verdict and its prose slips are booked.

## Next Steps

1. THE HANDLER LAYER, the other half of DECISION F275 D37: the `UUID(...)` parses in
   `apps/cli/` whose argument names a job, and the classic-only load behind them. Production
   code, so a SPLIT round with mutation red-proofs, and likely more than one.
2. THE FLIP, carrying DECISION F275 D48's obligations: the full suite is the backstop, the input
   is re-derived by round 82's committed generator at the flip's own base, and any site fallen
   to zero witnesses is a stop. The stale test double at
   `packages/orchestration/project_registry.py:856` is updated in the flip's own commit.
3. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- A RESOLVER THAT FINDS AN ID IS NOT A COMMAND THAT WORKS. `job status`, the one handler
  probed, fails one step later for a ping-pong id with a different message; the other handlers
  that load through the classic store were not probed.
- THE INPUT SET IS REPRODUCIBLE ONLY FROM ROUND 77's TWO SCRATCH JSON FILES, and the re-key
  cannot see a deleted ruled site.
- The open set is 87 by distinct id at this round's base, with `R-0809` and `R-0880` open. Four
  are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN83

── SLICE RECORD83 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD83 sha256=f83bbe9852edb1478c0f0bafe524b431222d7390fcb76d4d312d16b4b73b10e2

Gate: F275 R82 — the F275 round 82 entry. VERDICT PASS. Written by the planner and reviewer of session 29 after reading the committed range `d7cf5d58`..`afffd7cc` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 83, per operator amendment amend0827-process-diet rule 1.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The block was carried as a file under `.remedy-wt/` and copied with `shutil.copyfile`, so G1 compared the committed `.agent/authored/` blob against the reviewer's own original by `cmp` and found them identical at 33528 bytes; that establishes the saved copy equals what the reviewer wrote, which in this transport is the whole chain. `.agent/last_block.md` equalled the committed block blob, all four slices matched the sha256 on their own BEGIN markers, and the block re-measured at 392 lines TOTAL and 317 PROSE as its constraint 10 states. The ruled change set held exactly: nine paths, each commit staging one, zero paths under `packages/`, `apps/`, `tests/` or `docs/`, the largest commit 430 insertions.

EVERY GATE HOLDS UNDER THE REVIEWER'S OWN RE-DERIVATION. `.agent/plan.md` was byte-identical to its slice at 45 lines. All three appends were exact under reader A — 1097205 plus 3615, 288515 plus 875 and 1243551 plus 5327 — with reader B holding at N counted from the slice as 4, 1 and 10, and a letter flipped in the FIRST appended paragraph of each REJECTED by both readers. The canary read 42 passed, `ruff check .` 26 errors at the frozen ceiling, zero `.py` files under `.agent/` over a sweep of 2244, one worktree, and the open set 87 by distinct id at both ends with `R-0880` open and `R-0879` resolved. The reviewer re-ran the COMMITTED generator three times into one scratch directory and got ONE digest; into three different directories it gets three, and the difference is exactly the six lines in which the re-key stage prints its own output paths — so the artefact is byte-reproducible only under the directory names the worker chose, while every one of its figures reproduced under the reviewer's names: 318 of its 327 indented lines matched verbatim in order and the nine that did not are the lines naming a directory. The receiver class the artefact names was re-read with `ast`: `ProjectBrainGraph.nodes` is annotated `tuple[BrainNode, ...]` at line 257 of `packages/orchestration/project_brain.py`.

THE ROUND'S SUBSTANCE, AND THE WORKER CAUGHT TWO OF THE REVIEWER'S OWN ERRORS DOING IT. The flip's input is fixed at 2183 sites with a canonical digest and a committed producer; the subtraction took only refused sites, DECIDED staying at 1908 while REFUSED fell from 277 to 275; and the re-key's identity on this tree pair was not accepted alone, a shift control separating the scope key at 2183 from the line key at 2174. The DELETE control is what found something: the re-key does not refuse a deleted ruled statement but re-binds its key to the next attribute of that name in that scope, carrying `Job` onto a `BrainNode` receiver, which is `R-0880`'s defect by a second route and correctly minted no id. The worker DECLARED that the block's "seven other modules" carrying the delete target are six, measured over tracked files, and that G4's byte-identity clause could not hold against a SPEC ordering prose around the generator's output, running both readings and printing the containment arithmetic. It also added a third owner-check run so that artefact point 1 is a measurement and not a claim. All three were right, and the first two are recorded as prose slips rather than ids because neither left anything wrong on disk.
END RECORD83

── SLICE SLIPS83 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIPS83 sha256=c907a78f76acdc134ae0c344a367bf6c851569900c8c66a6f76e73b46ab1322e

2026-09-12 · F275 R82 · The round 82 block said the delete target "also occur[s] once in each of seven other modules" and there are six. The reviewer's count came from `grep -rc`, which matches a SUBSTRING, and `packages/orchestration/patch_apply.py` carries `_job_id_str = str(job.id)`, whose tail is the target line; so a hand-read tally of eight files became "seven others". The load-bearing half — exactly one occurrence inside the named file — was measured correctly and held. THE RULE THAT FOLLOWS: a count that supports a uniqueness claim is taken with a fixed-string whole-line match over TRACKED files, because a pattern search over a working directory counts what the pattern and the directory admit rather than what the claim is about.

2026-09-12 · F275 R82 · The round 82 block ordered the artefact to be the generator's stdout "under a title and a short opening" with five prose points after it, and then ordered G4 to prove the artefact BYTE-IDENTICAL to a fresh run of that generator. Both sentences were written by the same author and cannot both hold; the worker ran both readings and proved containment instead. THE RULE THAT FOLLOWS: an identity gate over a file the SPEC says is ASSEMBLED from generated and authored parts states CONTAINMENT with the offsets, never identity, and the two sentences are read against each other before emission as item 18 of §3 already requires of a recipe and its property.

2026-09-12 · F275 R82 · The round 82 SPEC ordered the generator to relay each sub-instrument's "whole stdout", and the committed round 59 re-key stage ends its output with a line naming the paths it wrote, so the artefact embeds the worker's scratch directory names and a re-run under any other names differs in exactly those lines. Every figure still reproduced. THE RULE THAT FOLLOWS: before ordering a tool's whole output relayed into a committed artefact, read that output for the paths and names the invoker chose, and either fix those names in the block or order them replaced by a stated label, because a reproducibility claim that silently depends on a directory name is a claim about the name.

2026-09-12 · F275 R83 · While dry-running round 83's red-proofs, the reviewer's first probe file sat OUTSIDE the disposable worktree, so pytest rooted at the primary checkout and imported its unmodified `packages/orchestration/data_paths.py`; all three candidate tests failed for a reason that had nothing to do with any mutation, and a run the other way round would have passed for the same reason. It was caught before authoring only because the failure message printed the module's path. THE RULE THAT FOLLOWS: every red-proof run inside a worktree first PRINTS the `__file__` of the module under mutation and requires it to lie inside that worktree, because a mutation that cannot reach the test produces a colour indistinguishable from one that did.
END SLIPS83

── SLICE DEC83 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC83 sha256=5d8b6c16eda73481465d9a0487a986238dff2c84443a85a91c71d0cdc2b9e6c4

## DECISION F275 D57 (2026-09-12, F275 round 83) — the two job-id resolvers become ONE function by alias, and the collapse is measured to carry a ping-pong id exactly one step through a real command

CONTEXT. DECISION F275 D37 found that the three largest residue classes of the flip's dry run are one id-SHAPE seam with two halves — a resolver that searches the classic store alone, and a handler layer that parses its argument with `UUID(...)` — and placed both in T003's resolver collapse, which DECISION F260 D5 names and which F260 T004 described as the point where `resolve_job_id` and `resolve_any_job_id` become one. Measured at `afffd7cc`, the two functions differ in ONE statement: the first assigns its matches from the classic store, the second from the union of both.

CHOSEN, FIRST: THE COLLAPSE IS AN ALIAS, NOT A COPY AND NOT A DELETION OF THE NAME. `resolve_job_id` takes the union and `resolve_any_job_id` becomes `resolve_any_job_id = resolve_job_id`. ALTERNATIVE: keep two functions with identical bodies, rejected because two definitions that must stay identical are two spellings of one concept, which is the defect `R-0814` names, and nothing would stop them drifting. ALTERNATIVE: delete the old name and rewrite its callers, rejected as scope — the callers under `apps/cli/` read that name as the statement that they need both stores, and renaming them buys nothing the alias does not.

CHOSEN, SECOND: THE COLLAPSE IS RECORDED AS NECESSARY AND NOT SUFFICIENT, AND THAT IS MEASURED. Called against a scratch root holding one ping-pong record, `_cmd_job_status` in `apps/cli/commands/job.py` exits 1 either way: before the collapse with `no job matches prefix`, and after it with `job not found`, because the handler loads through the classic store once the resolver has found the id. The failure moves one step later; the command does not start working. The half that makes it work is the handler layer DECISION F275 D37 names, measured at `afffd7cc` as 37 `UUID(...)` calls whose argument names a job in 16 files under `apps/cli/`, and it is a later round rather than this one.

CHOSEN, THIRD: THE TESTS ARE DISCRIMINATORS AND EACH IS RED-PROVED AGAINST THE HALF IT PINS. Two assertions need two mutations. Restoring the classic-only statement turns the two behavioural tests red and leaves the identity test green; replacing the alias with a second function turns the identity test red and leaves the two behavioural tests green. The reviewer measured, before authoring, that the collapse alone changes the colour of no existing test in the scoped suite — 13252 passed at the base in the primary checkout — which is precisely why a test that fails without it had to be written: a change nothing notices is a change nothing pins.

CHOSEN, FOURTH: NO FINDING IS RESOLVED AND NO ID IS MINTED. `R-0809` is OPEN and its headline names this symptom — a real id of the other store rejected as unknown — beside a second defect, four wordings for an unknown id, and its own resolution condition is the four-wordings test. The collapse changes the message a ping-pong id receives from `job status` and removes neither defect, so `R-0809` stays open with its owner unchanged and this round adds only the measured before and after. Item 30 of `docs/agents/planner_reviewer_prompt.md` §3 was applied before any id was considered.

CONSEQUENCE. One resolver reaches both job stores, and the `no job matches prefix` exit DECISION F275 D37 measured cannot now be produced by an id that exists in either store. Three tests pin the collapse and would fail if either half were undone. `job status`, the one handler probed, still fails for a ping-pong id, one step later and with a different message; the other handlers that load through the classic store were not probed and are expected to behave the same, and making them work is the next round's work.

HOW TO REVERSE. Restore `resolve_job_id`'s classic-only statement and its docstring, restore `resolve_any_job_id` as its own function from `afffd7cc`, delete the three tests and restore the one comment in `apps/cli/commands/job_context_cmd.py`. Every command then behaves as it did at `afffd7cc`, and the identity test's deletion is what stops the two names from being silently re-split.
END DEC83
