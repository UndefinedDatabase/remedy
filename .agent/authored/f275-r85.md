── STEP T003 — F275 — ROUND 85 ──
Goal: Register and repair the crash round 83 introduced in `remedy project adopt`, prove the
repair against the input that crashes, and correct round 84's count of the remaining handler
parses with a census keyed on what each parsed value flows into.

Base commit: `53659062`. Round type: SPLIT, and a REPAIR round: the finding persists in its own
commit before any repair commit, per §4 item 4 of `docs/agents/planner_reviewer_prompt.md`.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r85.md`             the block, saved verbatim
C0b `.agent/last_block.md`                    mirrored FROM THE COMMITTED C0a BLOB
C1  `.agent/plan.md`                          slice PLAN85, a full replacement
C2  `.agent/live_review.md`                   slice RECORD85 appended, the round 84 verdict
C3  `.agent/live_review.md`                   slice FIND85 appended, registering `R-0882`
C4  `.agent/prose_slips.md`                   slice SLIPS85 appended
C5  `apps/cli/commands/project.py`            the repair, SPEC F
C6  `tests/cli/test_scoped_listings.py`       the regression test, SPEC T
C7  `.agent/live_review.md`                   slice DONE85 appended, resolving `R-0882`
C8  `.agent/decisions.md`                     slice DEC85 appended
C9  `.agent/handoff.md`                       the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. C3 lands `R-0882` before C5 repairs it,
so a session that dies between them leaves an open finding on disk and not a silent fix.

## Change — exactly these paths and no others

The Bundle's paths. Under `apps/` and `tests/` exactly the two paths of C5 and C6. NOTHING under
`packages/`, `docs/` or `scripts/`.

## The defect, as the reviewer measured it before authoring

`_cmd_project_adopt` in `apps/cli/commands/project.py` resolves its argument with
`resolved_id = resolve_job_id(job_id_str)` and then calls `load_job(UUID(resolved_id))` inside a
`try` that catches only `JobNotFoundError`. Before round 83 the resolver searched the classic
store alone and always returned a UUID-shaped string. Round 83 made it search both stores, so it
now returns a 16-hex id for a ping-pong job, `UUID(...)` of that raises `ValueError`, and nothing
catches it. The reviewer ran `remedy project adopt 0123456789abcdef` through the real CLI against
a data root holding one ping-pong record, in one worktree at `afffd7cc` and one at `53659062`:
the first exits 1 with `Error: no job matches prefix '0123456789abcdef'`; the second exits 1
with an uncaught traceback ending `ValueError: badly formed hexadecimal UUID string`.

## SPEC F — `apps/cli/commands/project.py`, at C5

In `_cmd_project_adopt`, the line `        job = load_job(UUID(resolved_id))` becomes EXACTLY
`        job = load_job(resolved_id)`. `storage.load_job` already accepts a `str`, and for an id
the classic store does not hold it raises `JobNotFoundError`, which that `try` already turns
into `Error: job not found: <first eight characters>` and exit 3. Nothing else in the file
changes. The file's `UUID` import stays: the reviewer counted seven other references to `UUID`
in that file at `53659062`.

## SPEC T — `tests/cli/test_scoped_listings.py`, at C6

One test in the existing class `TestScopedListingsCLI`, named EXACTLY
`test_adopting_a_pingpong_job_id_exits_cleanly_instead_of_crashing`, IN-PROCESS rather than
through a CLI subprocess. It builds a git repository with that file's `_git_repo` helper and
initialises a project in it with `_init_project`, writes a ping-pong record `job.json` inside
`<data root>/jobs/0123456789abcdef/`, sets `REMEDY_DATA_DIR` and changes directory into the
repository through `monkeypatch`, then calls `_cmd_project_adopt("0123456789abcdef")` inside
`pytest.raises(SystemExit)` and asserts the code is 3 and that captured stderr contains
`job not found`. In-process is ordered because that file's `_env` sets `PYTHONPATH` to the
working directory pytest was launched from, so a subprocess imports whichever tree the run
started in, and a red-proof that mutates one tree while importing another cannot fail.

## Constraints

1. NO SLICE IS EDITED. PLAN85, RECORD85, FIND85, SLIPS85, DONE85 and DEC85 land byte for byte; a
   discrepancy inside one is DECLARED, never repaired.
2. C5 and C6 are the worker's OWN code from the SPECs. The reviewer's candidate is deleted.
3. READ `.agent/STOP` before C0a and before C9, with real exit codes. If it appears, finish the
   commit in hand, write the handoff and end.
4. Every commit stages EXACTLY ONE path and stays under 500 insertions.
5. No `.py` under `.agent/`; scratch under `.remedy-wt/`, uncommitted.
6. No landed record is rewritten: every `.agent/live_review.md` and `.agent/decisions.md` commit
   is an APPEND with a ZERO deletion column. DECISION F275 D58's figure of ten is corrected by
   DEC85 beside it, not by editing it.
7. No `gh`, no `remedy` command outside a scratch probe, no pull request, no branch created or
   deleted, no merge, NEVER a force-push, no history rewrite.
8. The red-proof worktree is created with `git worktree add --detach` at C6 and REMOVED AND
   PRUNED before C7. The scoped suite runs in the PRIMARY checkout.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 261 lines TOTAL and 187 lines of PROSE,
   against the caps of 490 and 400.
10. THE GATES RUN AT TWO COMMITS. G4, G5 and G6 run at C6, because DONE85 at C7 and DEC85 at C8
    carry their results and item 31 of §3 requires such a gate to run STRICTLY EARLIER. G1, G2,
    G3, G7 and G8 run at C8. No gate runs after C9; C9's own numbers are the reviewer's.
11. DONE85 describes this round's own repair, so under the carve-out of item 20 of §3 it names
    this constraint's ordering instead of a SHA: the repair is C5, its test C6, and every gate
    DONE85 quotes runs at C6.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r85.md` at C0a against the block as received,
by `cmp`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob. Extract the
slices by their markers, report how many were FOUND, check each against its BEGIN-marker
sha256, and re-measure TOTAL and PROSE against constraint 9.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN85 from the COMMITTED C0a blob; at
most 50 lines; one `## Goal` and one `## Next Steps`.

G3 THE RECORD, FULL FORENSICS, for each of the four record appends: C2, C3 and C7 into
`.agent/live_review.md` and C8 into `.agent/decisions.md`. For each, read its pre-commit blob
with `git show` at that commit's PARENT and print its length; the first is 1107652 and the
decisions pre-commit length is 1257440. READER A with the arithmetic printed; READER B over the
file's LAST N blank-line units against the slice's N paragraphs IN ORDER, N counted by the
script; a letter flipped in the FIRST appended paragraph of each, REJECTED by both readers;
every deletion column 0. `.agent/prose_slips.md` at C4 equals its 294305-byte pre-commit blob
followed by exactly SLIPS85. Derive the ledger's `Gate:` header pattern from the file, report
how many it matches and that RECORD85's header matches and duplicates none. Report that after
C3 exactly one line starts `- R-0882 — ` and after C7 exactly one line starts `Done: R-0882 — `.

G4 THE REPAIR, STRUCTURALLY, at C6, with `ast`. In `_cmd_project_adopt`: no `Call` to `UUID`
whose argument is the name `resolved_id`; the whole-line count of SPEC F's new line, 1. Under
`apps/cli/`, every `UUID(...)` call classified by what its value flows into — an argument of
`load_job`, a value whose argument's source names a project, anything else — with the counts
at `53659062` and at C6. The reviewer measured 22 calls at `53659062`: 13 into `load_job`, 8
naming a project and 1 other; at C6 the `load_job` count must be one lower and the others
unchanged. Then, over `apps/` and `packages/` with `data_paths.py` excluded, every call of
`resolve_job_id`, `resolve_any_job_id` or `lookup_job_id` whose result is bound to a name that a
LATER `UUID(...)` call in the same function takes as its argument: the reviewer measured 1 at
`53659062`, this site; at C6 it must be 0. Before trusting that 0, plant one such use in a
scratch copy and show the same instrument reports it. `ruff check` over C5's and C6's paths
exits 0.

G5 THE BEHAVIOUR, at C6. (a) SPEC T's test by node id, PASSED, in the primary checkout. (b) The
scoped suite `python3 -B -m pytest tests/test_data_paths.py tests/cli/ tests/orchestration/ -q -p no:randomly`
in the primary checkout, totals REPORTED AS MEASURED, failure set EMPTY; the reviewer measured
it at `53659062` at 13260 passed, 10 skipped and 0 failed; state and account for the difference.
(c) THE CLI PROBE, both arms, each in a scratch tree built with `git archive`: at `53659062`
and at C6, run `remedy project adopt 0123456789abcdef` as `python3 -m apps.cli.grouped` with
`PYTHONPATH` set to that scratch tree and `REMEDY_DATA_DIR` to a data root holding one project
and one ping-pong record, and report each arm's exit code, whether stderr holds `Traceback`,
and its last stderr line verbatim.

G6 THE MUTATION RED-PROOF, in the worktree of constraint 8, at C6. PRINT the `__file__` of
`apps.cli.commands.project` imported inside the worktree; it must lie inside it. Purge
`__pycache__` before each run. Select the class `TestScopedListingsCLI`. CONTROL, unmutated:
every test PASSES. M1: the one line EXACTLY equal to SPEC F's new line becomes
`        job = load_job(UUID(resolved_id))`, its whole-line count reported as 1 first. Required:
ONLY `test_adopting_a_pingpong_job_id_exits_cleanly_instead_of_crashing` FAILS, and its first
error line names `ValueError`. Report every colour and exit code, restore, remove and prune.

G7 TREE, CANARY, LINT, PATH SET, OPEN SET, at C8. `git status --porcelain` prints `''`;
`git worktree list` one row; the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q`
exit 0, 42 at `53659062`; `ruff check .` exit 1 with its rows cross-checked against its own
`Found <n> errors.` line, 26 at `53659062`. The changed-path set of `53659062`..C8 against the
Bundle's paths MINUS `.agent/handoff.md`, MISSING and EXTRA by name. The open set BY DISTINCT ID
at `53659062`, after C3 and at C8: the reviewer measured 87 at `53659062`; after C3 it must be 88
with `R-0882` the only id added; at C8 87 again with `R-0882` the only id resolved; `R-0809` and
`R-0880` open throughout.

G8 THE INSERTION CAP over `53659062`..C8: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 29 of feature F275 · round 85 · rounds so far 85`; the Commits table read from
`git show --numstat` and compared cell by cell against G8, C9's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; `## Next` stating `Operator questions open: 0`.
NO SCOPE REPORT AND NO SESSION-LIMIT BANNER, by amendment amend0911-f275-to-scope.

── SLICE PLAN85 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN85 sha256=bc6516c9d26fc7d6c5ffa564caee5e182280c673e777ed2f0066d36073edaefc
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

ROUND 85 REPAIRS A CRASH ROUND 83 INTRODUCED. Once the resolver searched both job stores it could
return a 16-hex ping-pong id, and `remedy project adopt` passed that straight to `UUID(...)`,
which raised an uncaught `ValueError`. The round registers that as `R-0882`, drops the parse so
the command takes its own `job not found` path, pins it with an in-process test red-proved
against the parse, and resolves the finding. It also replaces round 84's count of the remaining
handler parses, keyed on the argument's name, with a census keyed on what each value flows into.
The round 84 verdict and its prose slips are booked.

## Next Steps

1. THE REMAINING `load_job(UUID(...))` PARSES under `apps/cli/`, counted by flow, each read for
   whether its caller keeps using the raw argument as a key, starting with `job stop`'s loader
   and its caller's normalisation. Production code, so a SPLIT round with mutation red-proofs.
2. THE FLIP, carrying DECISION F275 D48's obligations: the full suite is the backstop, the input
   is re-derived by round 82's committed generator at the flip's own base, and any site fallen
   to zero witnesses is a stop. The stale test double at
   `packages/orchestration/project_registry.py:856` is updated in the flip's own commit.
3. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- A WIDER RETURN DOMAIN REACHES EVERY CALLER. The sweep behind this round follows a returned id
  one hop inside its own function; a callee that parses it further down is not followed.
- THE INPUT SET IS REPRODUCIBLE ONLY FROM ROUND 77's TWO SCRATCH JSON FILES, and the re-key
  cannot see a deleted ruled site.
- The open set is 87 by distinct id at this round's base, with `R-0809` and `R-0880` open. Four
  are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN85

── SLICE RECORD85 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD85 sha256=3982ca823f7ce7e7282ae61d6324a26d1d9798db151c9ec26ccbcb11ca904c96

Gate: F275 R84 — the F275 round 84 entry. VERDICT PASS. Written by the planner and reviewer of session 29 after reading the committed range `dd92a035`..`53659062` and RE-DERIVING EVERY GATE AND EVERY RED-PROOF INDEPENDENTLY; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 85 that writes the record, per operator amendment amend0827-process-diet rule 1. The round changed production code and the reviewer ran its own four mutations in its own worktree before writing this.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/` blob was identical by `cmp` to the reviewer's original at 26831 bytes, `.agent/last_block.md` equalled it, all four slices matched their BEGIN-marker digests, and the block re-measured at 293 lines TOTAL and 219 PROSE. `.agent/plan.md` equalled its slice at 44 lines. The three appends were exact under reader A — 1104567 plus 3085, 292291 plus 2014 and 1253148 plus 4292 — with reader B holding at N counted from the slice as 4, 3 and 8, and a letter flipped in each FIRST appended paragraph rejected by both readers. Twenty-two paths changed; every commit staged one path except C5, which staged the thirteen handler files, and the largest commit was 293 insertions.

THE PRODUCTION CHANGE HOLDS UNDER THE REVIEWER'S OWN RE-RUN. Read with `ast` at C7, `data_paths.py` defines `JobIdError` on `ValueError` and its three subclasses on it, one `lookup_job_id` and one `resolve_job_id`, and each of the three lines the block quoted once. Every line C5 changed falls in three classes — 27 parses replaced, import lines, blank lines — plus the one `_make_writer` docstring the worker declared, and nothing else. Measured by the argument's name the handler parses went from 27 bound statements and 10 `load_job` arguments to 0 and 10. In a worktree whose module the reviewer printed as resolving inside it, the six selected tests pass unmutated; a plain `Exception` base fails the not-found test and `propose`'s missing-job test; an exiting lookup fails the not-found and message tests; a changed wrapper message fails only the message test; restoring `guide`'s parse fails only the routed-handler test. The scoped suite in the primary checkout read 13260 passed, 10 skipped and 0 failed, the base's 13255 plus exactly the five new tests; `ruff check .` rows at C7 and at the base compared as a multiset differ by nothing; the canary read 42 and the open set stayed 87.

TWO THINGS THE REVIEWER FOUND AFTER THE VERDICT, AND NEITHER UNDOES IT. First, round 84's own count was keyed on whether the argument's source names a job, and a census keyed on what the value flows into finds 13 `load_job(UUID(...))` calls rather than 10, because three pass `jid` or `resolved_id`; the worker had already flagged two of them. Second, following one of those three found a crash round 83 introduced in `remedy project adopt`, which round 85 registers as `R-0882` in its own commit. Round 84 routed exactly the statements its SPEC defined and neither discovery is in its change set.
END RECORD85

── SLICE FIND85 ── target `.agent/live_review.md` ── APPEND ──
BEGIN FIND85 sha256=ba714fa8c316af951b4a733d784186a2839e47a38d79ded392c28e60815e9f92

- R-0882 — Medium, `remedy project adopt` CRASHES WITH AN UNCAUGHT `ValueError` FOR A PING-PONG JOB ID, A REGRESSION THIS FEATURE INTRODUCED. Raised by the planner and reviewer of session 29 while preparing round 85, from a census of the handler parses keyed on what each value flows into. THE DEFECT: `_cmd_project_adopt` in `apps/cli/commands/project.py` binds `resolved_id = resolve_job_id(job_id_str)` and then calls `load_job(UUID(resolved_id))` inside a `try` that catches only `JobNotFoundError`. Until round 83 the resolver searched the classic store alone and always returned a UUID-shaped string; round 83 made it search both stores, so for a ping-pong job it returns sixteen hex characters, `UUID(...)` of those raises `ValueError`, and nothing catches it. MEASURED through the real CLI against a data root holding one project and one ping-pong record `0123456789abcdef`: in a worktree at `afffd7cc`, before round 83, the command exits 1 with `Error: no job matches prefix '0123456789abcdef'`; in a worktree at `53659062` it exits 1 with an uncaught traceback ending `ValueError: badly formed hexadecimal UUID string`. WHY NO GATE SAW IT: round 83's blast-radius reading listed every CALLER of `resolve_job_id` and never followed what each caller DID with the value it returned, and no test adopts a ping-pong job, so the scoped suite stayed green; round 83's verdict is not wrong in anything it measured and is not reopened. A sweep over every resolver call under `apps/` and `packages/`, following the returned name one hop inside its own function to a later `UUID(...)`, finds this site and no other at `53659062`; the same instrument also looks for a UUID-only attribute or a comparison with a record's `.id` on the returned name, finds none in the tree, and reported both when the reviewer planted one of each in a scratch copy. WHY MEDIUM AND NOT LOW: no state is corrupted and the exit stays non-zero, but after the flip every job id is sixteen hex characters, so the command would crash for every job rather than for one kind. FIX: pass the resolved id to `load_job` as the string it already accepts, so an id the classic store does not hold takes the handler's own `job not found` path and exit 3; pin it with an in-process test that fails with `ValueError` when the parse is restored. Owner: F275.
END FIND85

── SLICE SLIPS85 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIPS85 sha256=f268d4dafb58ee32b3af579c16a570102afeee450dfe5ada1480897972697428

2026-09-12 · F275 R84 · The round 84 block counted the handler parses still to route by whether each `UUID(...)` argument's SOURCE TEXT contains "job", and so reported ten `load_job(UUID(...))` calls where a census by flow finds thirteen: two pass `jid` and one passes `resolved_id`. The worker flagged two before the reviewer measured the third. THE RULE THAT FOLLOWS: a set of call sites is defined by what the value FLOWS INTO — the function that consumes it — and never by what the variable happens to be called, because a name is a convention and the flow is the fact.

2026-09-12 · F275 R83 · The round 83 block widened what `resolve_job_id` can return and measured its blast radius as the list of its callers, without following what any caller did with the returned value; one of them passed it to `UUID(...)`, and the resulting crash shipped under a PASS and is `R-0882`. THE RULE THAT FOLLOWS: when a change widens a function's RETURN DOMAIN, every caller's USE of the returned value is swept, one hop at least and with a planted control, because the callers list says who is affected and only the uses say how.
END SLIPS85

── SLICE DONE85 ── target `.agent/live_review.md` ── APPEND ──
BEGIN DONE85 sha256=6d68a4867d8f22e33c6946ed7a236a42affb0ff6b0411de921d31de1a460b6bb

Done: R-0882 — RESOLVED in the round that registered it. `_cmd_project_adopt` passes the resolved id to `load_job` as a string instead of through `UUID(...)`, so an id the classic store does not hold raises `JobNotFoundError`, which the handler already turns into `Error: job not found:` with the id's first eight characters and exit 3. The repair and its test land at the commits constraint 10 of round 85's block fixes as C5 and C6, and every reading below is taken at C6, before this paragraph's commit. THE REPAIR IS PINNED BY A DISCRIMINATOR: `test_adopting_a_pingpong_job_id_exits_cleanly_instead_of_crashing` runs the handler in-process against a ping-pong record and requires exit 3 with `job not found`; restoring `UUID(resolved_id)` fails that test alone, with `ValueError`, and leaves every other test of its class green. Through the real CLI the same input now exits 3 without a traceback, where at the round's base it exited 1 with one. The sweep that found the site reports no other resolver result passed to a later `UUID(...)` under `apps/` or `packages/`. WHAT IS NOT CLAIMED: a ping-pong job still cannot be ADOPTED, because adopting writes the project id into a classic record and the ping-pong store is the flip's; and the sweep follows a returned id only inside its own function, so a callee that parses it further down is not covered.
END DONE85

── SLICE DEC85 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC85 sha256=59d541e9d2f837cf5d1a0c13c0585b399f8950f72cf935de0ecf15fba5ee4b95

## DECISION F275 D59 (2026-09-12, F275 round 85) — the adopt crash is repaired by dropping a parse rather than by making adopt reach the ping-pong store, and the remaining handler parses are counted by flow, correcting D58's figure beside it

CONTEXT. Round 83 widened what `resolve_job_id` returns and round 84 routed 27 handler parses through a raising lookup, counting the rest by whether each argument's source names a job. Preparing this round, the reviewer took a census of every `UUID(...)` call under `apps/cli/` by what its value flows into, and following one of the calls that census added found `R-0882`: `remedy project adopt` now crashes on a ping-pong job id.

CHOSEN, FIRST: THE REPAIR DROPS THE PARSE. `load_job` already accepts a string, and the handler's `try` already turns `JobNotFoundError` into its own message and exit 3, so removing `UUID(...)` restores a clean exit with no new path. ALTERNATIVE: make adopt WORK for a ping-pong job by resolving through the unified store, rejected as scope — adopting writes the project id into the job record through the classic store's `save_job`, and writing into a ping-pong record is the flip's world, not a repair's.

CHOSEN, SECOND: THE REMAINING PARSES ARE COUNTED BY FLOW, AND DECISION F275 D58's FIGURE IS CORRECTED HERE RATHER THAN EDITED. At `53659062` the census finds 22 `UUID(...)` calls under `apps/cli/`: 13 whose value is an argument of `load_job`, 8 whose argument names a project and so are outside the job-id seam, and 1 validating a task id. D58 said ten `load_job` parses remained because its rule keyed on the argument's name, and three pass `jid` or `resolved_id`. D58's paragraph stays as landed; this is the figure the next round works from, one lower once this round's repair removes the adopt site.

CHOSEN, THIRD: A RETURN DOMAIN THAT WIDENS IS SWEPT BY USE, NOT BY CALLER. Over `apps/` and `packages/` with `data_paths.py` excluded, the sweep follows each resolver call's bound result to a later `UUID(...)` in the same function. It finds 64 calls and exactly one such use at `53659062`, this site. The same instrument also looks for a UUID-only attribute or a comparison with a record's `.id` on the returned name, finds none in the tree, and reported one of each when the reviewer planted them in a scratch copy; its `UUID(...)` branch is shown working by the real site it found. Its reach is one hop inside a function, and that limit is stated rather than widened here.

CONSEQUENCE. `R-0882` is registered and resolved in this round with the crash measured before and the clean exit measured after. Twelve `load_job(UUID(...))` parses remain under `apps/cli/` by flow, and the next production round reads each for whether its caller keys on the raw argument. `R-0809` and `R-0880` stay open.

HOW TO REVERSE. Restore `apps/cli/commands/project.py` and `tests/cli/test_scoped_listings.py` from `53659062` and delete this paragraph block; the adopt command then crashes on a ping-pong id again, and `R-0882`'s resolution no longer holds.
END DEC85
