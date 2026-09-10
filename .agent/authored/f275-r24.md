STEP T001-close / F275 — ROUND 24 — THE SURVIVING SURFACES THAT ADVERTISE DELETED THINGS

Goal: repair the three places where a command, a cross-reference or an operator page
still offers the reader something this feature deleted — `remedy mission run`'s catalog
entry, the two dangling `related=` tuples, and the mission run-loop page whose Quick
start gives an operator a command that cannot run — and land the referential-closure
test R-0859 asks for, so that the next dangling cross-reference goes red instead of
quiet. Book the round 23 verdict and the findings session 13 measured while doing it.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f275-r24.md`
  C0b  mirror the COMMITTED C0a blob into `.agent/last_block.md`
  C1   `.agent/plan.md` <- PLAN24
  C2   the record: LEDGER24 appended to `.agent/live_review.md`, SLIPS24 appended to
       `.agent/prose_slips.md`
  C3   DEC24 appended to `.agent/decisions.md` — DECISION F275 D14
  C4   the catalog: pairs Q1 and Q2, and the new test Q3
  C5   the operator page: pairs Q4, Q5, Q6 and Q7
  C6   the handback

Change set — EXACTLY these paths, nothing else:
  .agent/authored/f275-r24.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  .agent/decisions.md
  apps/cli/command_catalog.py
  tests/test_command_catalog.py
  docs/system/mission-run-loop-morning-report-v0.md
  .agent/handoff.md

Constraints:
 1. Every slice between a BEGIN and END marker is applied BYTE FOR BYTE. Do not
    reflow, re-wrap, re-indent or "fix" anything inside one. If a slice looks wrong,
    apply it anyway and declare it in the handback.
 2. Marker lines are never written into any target file.
 3. THE APPEND CONVENTION for `.agent/live_review.md`, `.agent/prose_slips.md` and
    `.agent/decisions.md`, verified by the reviewer against all three files at
    `ea5f8128`: each file ends with exactly ONE newline byte. An append writes
    `pre + b"\n" + slice`, where the slice itself ends with one newline.
 4. WITHIN a slice bound for `.agent/live_review.md` or `.agent/prose_slips.md`,
    records are separated from each other by a BLANK line. Measured at `ea5f8128`:
    244 of the 258 adjacent entry pairs in `.agent/prose_slips.md` are blank-
    separated and 14 are on consecutive lines, so blank separation is the dominant
    convention rather than a universal one, and this constraint orders it rather
    than claiming it.
 5. C2 is the FIRST substantive commit of this round, before C3, C4 and C5.
 6. Q1's FROM begins with a comment line whose trailing rule is a run of exactly TEN
    U+2500 BOX DRAWINGS LIGHT HORIZONTAL characters. The length is stated because a
    run of one repeated character is the one thing a reader cannot recover by eye.
    Transport is a byte copy, so nothing retypes it — but the count is on the record.
 7. PAIR SHAPES, each classified by a containment test the reviewer RAN at
    `ea5f8128`, one reading per pair:
      Q1 TO contains FROM: false -> REWRITE. FROM occurs 1x in its target.
      Q2 TO contains FROM: false -> REWRITE. FROM occurs 1x in its target.
      Q3 TO contains FROM: false -> REWRITE. FROM occurs 1x in its target.
      Q4 TO contains FROM: false -> REWRITE. FROM occurs 1x in its target.
      Q5 TO contains FROM: false -> REWRITE. FROM occurs 1x in its target.
      Q6 TO contains FROM: false -> REWRITE. FROM occurs 1x in its target.
      Q7 TO contains FROM: false -> REWRITE. FROM occurs 1x in its target.
 8. NOTHING under `apps/ui/` is touched. DECISION F275 D14 records why the surviving
    `context_budget_optimized` residue is left standing rather than swept.
 9. Destructive verification runs ONLY inside a disposable `git worktree`, never in
    the primary checkout. Remove and prune it before the handback.
10. Read `.agent/STOP` from disk before the first commit. If it exists, write the
    handback and stop.

Done when — G1 to G8 below have all been RUN, with their real exit codes recorded,
and the handback carries ONE line per gate. Every gate runs at or before C5.

G1 TRANSPORT. `sha256` of the committed `.agent/authored/f275-r24.md` blob at C0a
equals the digest the delegation names, and the committed `.agent/last_block.md` blob
at C0b equals the same digest. Report both. Per §3 item 37 this covers those two
committed artefacts and the reviewer's scratch original, and claims nothing about the
bytes that travelled into your prompt.

G2 THE PLAN. `.agent/plan.md` at C1 is byte-identical to PLAN24. Report its byte
length and line count, which must be under the AGENTS.md cap of 50, and confirm
`^## Goal$` and `^## Next Steps$` each occur exactly once.

G3 THE RECORD, at C2, for `.agent/live_review.md` and `.agent/prose_slips.md`
separately. Reading (a), bytes: the committed post-blob equals the pre-blob, then one
newline, then the slice exactly as extracted; READ THE JOINING BYTE BACK from the post
blob at offset len(pre) and report it. Reading (b), structure: count N as the number
of blank-line-separated paragraphs IN THE SLICE with your own script — never from this
block — and compare the LAST N blank-line units of the whole post-file against those N
paragraphs IN ORDER. Negative control: flip one byte inside the FIRST appended
paragraph and confirm BOTH readers reject it while both accept the truth. Then report
over the whole post-file: `^Gate: F275 R23 ` exactly 1, `^- R-0871 — ` exactly 1,
`^Note: F275 R24 ` exactly 3, `^Done: R-0864 — ` exactly 1, and `^Done: R-0862 — `
still exactly 1. Finally report THE OPEN SET BY DISTINCT ID, every distinct id in a
`^- R-\d+ — ` paragraph minus every distinct id in a `^Done: R-\d+ — ` line. The
reviewer computed it at `ea5f8128` as 92, over 99 distinct registrations against 7
distinct resolutions. It must read 92 at C2, because this commit registers one id and
resolves one.

G4 THE DECISION, at C3, over `.agent/decisions.md`. The same two readings and the same
negative control as G3. Then report `^## DECISION F275 D14 ` as occurring exactly once
in the whole file.

G5 THE CATALOG, at C4, read through the SHIPPED reader by importing
`apps.cli.command_catalog`, never by grepping source. Report all of it:
  (a) Q1 and Q2: the FROM string reads 0x and the TO string reads 1x in
      `apps/cli/command_catalog.py`.
  (b) `len(_BASE_CATALOG)` is 222 and `len(GROUPS)` is 44, UNCHANGED from `ea5f8128` —
      this round repairs entries and deletes no command.
  (c) `get_command("mission.run")`: the option names are exactly `--iterations`,
      `--no-llm`, the project-scope option and the json option, with `--job-id`,
      `--max-steps` and `--max-seconds` ABSENT; `related` is exactly
      `("mission.report", "mission.ledger")`; and the description contains neither
      `dogfood` nor `run id`.
  (d) Resolving every `related=` tuple against the live id set gives ZERO dangling
      references. The reviewer measured TWO at `ea5f8128` — `mission.run` ->
      `dogfood.run-loop` and `repo.status` -> `readiness.show` — and this round
      repairs both.
  (e) `python3 -m ruff check apps/cli/command_catalog.py tests/test_command_catalog.py`.

G6 THE NEW TEST BITES, at C4, inside a disposable `git worktree` and never in the
primary checkout. Report four readings in this order. The UNMUTATED CONTROL:
`python3 -B -m pytest tests/test_command_catalog.py -q` is exit 0, with the passed
count. THE MUTATION: add the single string `"mission.nonexistent"` to `mission.run`'s
`related` tuple in that worktree's `apps/cli/command_catalog.py` — the bytes
`related=("mission.report", "mission.ledger")` occur exactly ONCE in that file at C4,
which is the unique revert target §3 item 25 requires. Re-run the same command: it must
be exit 1 with the failure naming
`test_every_related_reference_resolves_to_a_live_command`, and you report HOW MANY
tests failed and WHICH. THE REVERT: restore the file and confirm exit 0 at the control's
count with the worktree's `git status --porcelain` EMPTY. Purge `__pycache__` before
each run and use `python3 -B`, so no stale bytecode answers for the source.

G7 THE OPERATOR PAGE, at C5. For each of Q4, Q5, Q6 and Q7 the FROM reads 0x and the TO
reads 1x in `docs/system/mission-run-loop-morning-report-v0.md`. Then over that ONE
file report a hard zero for each of these spaced forms: `remedy dogfood create`,
`remedy dogfood run-loop`, `remedy dogfood morning-report`, `remedy dogfood step`,
`remedy dogfood replay`, `remedy dogfood show`, and `--job-id`. Also report that
`remedy self proposal-list` still reads 0, which
`tests/cli/test_product_spine.py::test_no_stale_self_proposal_list_in_mission_docs`
pins and which this round must not break.

G8 THE SUITE AND HYGIENE, at C5, from the PRIMARY checkout.
  python3 -m pytest tests/test_command_catalog.py tests/cli/test_product_spine.py tests/cli/test_worker_facade_cmd.py tests/cli/test_mission_cmd.py tests/test_grouped_cli.py -q
  python3 -m pytest tests/cli/test_golden_path.py -q
Report both real exit codes and real counts. The full suite is NOT part of this round's
gate. Then: `.agent/STOP` does not exist; `git status --porcelain` is EMPTY;
`git worktree list` holds exactly ONE entry; the branch is
`feature/f275-one-world-completion-part-three`; `git diff --name-only ea5f8128..C5`
names EXACTLY the change-set paths above other than `.agent/handoff.md`, reported as an
exact set match with MISSING and EXTRA both printed even when empty; and each commit's
insertion count from `git show --numstat`, for every commit before the handback commit,
against the AGENTS.md DECISION F104 D1 cap of 500.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md — the state
block with the SESSION NUMBER, the per-commit changed-files table with `+/-` cells
transcribed from `git show --numstat` and compared cell by cell against it, one line
per gate with its real exit code, every declared deviation, the item status table, and
the next expected action. There is no length cap. Then push.

<<<BEGIN PLAN24>>>
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 24 repairs the surviving surfaces that still offer a reader something this feature
deleted. `remedy mission run` advertises a second mode and three options no code path
honours; two `related=` tuples name commands that no longer exist; and the mission
run-loop page's Quick start gives an operator a `mission report` invocation that cannot
parse. The round lands the referential-closure test R-0859 asks for, with the mutation
colour that proves it bites, and books the round 23 verdict.

## Next Steps

1. Retire the cluster scaffolding R-0868 names — the deletion map, its two ratchets and
   the order file — repair F267's plan as the round 23 measurement re-states it, and
   banner the historical `Groups` table in `docs/system/architecture.md`.
2. T002, the atomic record flip, alone, because every later commit's size depends on it.
3. T003, the classic runner, which T002's ruling is the prerequisite for.

## Risks

- The open set is 92 by distinct id at this round's base `ea5f8128`, computed mechanically
  from the record. This round registers one and resolves one, leaving 92. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION
  F272 D12.
- Removing three advertised options is a user-visible narrowing of a SURVIVING command.
  DECISION F275 D14 rules it, and R-0871 records it; nothing is wired in to replace them.
- The advertisement guard `tests/cli/test_advertised_commands.py` is still blind to a
  whole-group deletion, which is R-0847 and is why this page survived four rounds of
  sweeps. Every remaining round sweeps the spaced form by hand.
<<<END PLAN24>>>

<<<BEGIN LEDGER24>>>
Gate: F275 R23 — the F275 round 23 entry. VERDICT PASS, written by the planner and reviewer of session 13 after reading the committed range `6f865e50`..`ea5f8128` and RE-RUNNING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was not evidence for any line here. Booked by round 24's C2 from the pushed handback, under amend0827-process-diet rule 1. SEVEN single-parent commits C0a `ca41fdc7`, C0b `0603be17`, C1 `d8184f50`, C2 `75ca69d0`, C3 `9db5326d`, C4 `64932207` and C5 `ea5f8128`, per-commit insertions 467, 445, 21, 20, 183 and 7 for the six before the handback, every one under the AGENTS.md DECISION F104 D1 cap of 500. G1 TRANSPORT covers the chain this workflow can walk and NOT the emitted bytes, per §3 item 37: the reviewer's scratch original `.remedy-wt/f275-r23.md`, the committed `.agent/authored/f275-r23.md` and the committed `.agent/last_block.md` are all 48390 bytes at `990e0f1e2e70dc575fe55935a7f19c97a795ff61280aeaa7e8a7f4fc33a71d69` and compare BYTE-EQUAL. G2: `.agent/plan.md` at C1 is 2411 bytes byte-identical to the PLAN23 slice, 43 lines against the cap of 50, with `^## Goal$` and `^## Next Steps$` each exactly once. G3 AND G4 HELD OVER THREE APPENDS, each re-run by the reviewer against the committed blobs: `.agent/live_review.md` 702413 to 717936, `.agent/prose_slips.md` 201417 to 205219 and `.agent/decisions.md` 991391 to 1005161, every post-blob equal to its pre-blob then ONE newline then the slice exactly as extracted, with the joining byte READ BACK from each post blob at offset len(pre) and reading `b'\n'` in all three rather than asserted. The structural reader counted N from each slice — 6, 4 and 20 paragraphs — and matched the last N blank-line units of each whole post-file IN ORDER. The reviewer ran its OWN negative control on the FIRST appended paragraph of the ledger slice, per §3 item 36: the byte reader rejects it, the structural reader rejects it, and both accept the truth, with the later paragraphs provably untouched by the flip. `^Gate: F275 R22 `, `^- R-0869 — `, `^- R-0870 — `, `^Done: R-0862 — `, `^Landed: R-0870 ` each read exactly 1 and `^Note: F275 R23 ` reads exactly 2; `^Landed: R-0862 ` STILL reads 1 and was NOT removed, which is DECISION F272 D10 obeyed rather than §4 item 4 read literally. THE OPEN SET WENT 91 TO 92 BY DISTINCT ID, over 99 registrations against 7 resolutions, which is correct for a round registering two ids and resolving one — and the reviewer's own pre-emission figure of 91 at the base reproduced exactly. `^## DECISION F260 D3 `, `^## DECISION F275 D12 ` and `^## DECISION F275 D13 ` each occur exactly once. G5 THE REPAIRS: for Q1, Q2 and Q3 the FROM reads 0 and the TO reads 1; for Q4 the FROM reads 0, the deleted assertion line reads 0 and the surviving assertion still reads exactly 1 — the reading §3 item 6 requires, because that TO already occurred once in the target before the edit. The reviewer re-ran the round's own commands from the primary checkout and measured 307 passed in 44.83s at exit 0 and `All checks passed!` from ruff over the four touched files, both reproducing the applied dry run this block was authored against. G6 THE SPLIT SWEEP, which is R-0869's fix clause in force for the first time: the meetable half is a HARD ZERO and holds — all five spaced advertisement forms read 0 over the 1652 tracked files outside `.agent/` and `.data/` — and the unmeetable half is a RAW LIST, printed in full and reconciled against the file set the block named IN ADVANCE. The reviewer's own sweep finds 13 occurrences on 9 lines across exactly those 8 files, with UNEXPECTED empty, and both R-0870 files now clean; the worker reported 9, which is the LINE count the gate asked for, against the reviewer's 13 OCCURRENCES, and the two readings agree on the only thing the gate is stated over, which is the file set. G7: the canary 42 passed at exit 0. G8: no `.agent/STOP`, porcelain EMPTY, ONE worktree, the branch correct, `6f865e50..64932207` naming EXACTLY the ten change-set paths with MISSING and EXTRA both empty, and every one of the eleven `+/-` cells of the handback's `## Commits` table agreeing with `git show --numstat` for its commit. ALL FOUR DECLARED DEVIATIONS ARE SUSTAINED and every one of them is the reviewer's error rather than the worker's: G1 named a BEGIN-marker digest the block does not carry, so the worker verified against the delegation's digest and said so; constraint 4 claimed a universal about the prose-slips separator that 14 of 258 pairs falsify; the P4 pair leaves the enclosing test's name and docstring arguing for the assertion it removes; and no worktree was created because no destructive check was ordered. The first, second and fourth are prose slips. The third landed on disk and is folded into R-0870 below.

- R-0871 — Medium, A SURVIVING COMMAND ADVERTISES A MODE IT NO LONGER HAS AND THREE OPTIONS NO CODE PATH READS, AND EVERY ONE OF THEM IS ACCEPTED SILENTLY. Raised by the reviewer of session 13 while measuring R-0859's two dangling `related=` tuples, which is R-0870's fix clause working as intended — the neighbourhood sweep found the defect, not the cross-reference itself. §3 item 30's search of the open set at `ea5f8128` returns no finding for it: R-0845 records the LOSS of `remedy mission run`'s second mode and says nothing about the advertisement surviving, R-0847 is about the GUARD being blind to a deleted group, and R-0861, which held the doc-page instance of this class, is RESOLVED. THE MEASUREMENT, taken at `ea5f8128` by reading the SHIPPED catalog and the SHIPPED handler rather than by grep. `apps/cli/command_catalog.py` gives `mission.run` the description "Run a mission's orchestrator loop when the id is a mission (F070); otherwise the bounded dogfood run loop for that run id", and declares `ArgDef`s for `--job-id`, `--max-steps` and `--max-seconds`. `apps/cli/grouped.py` wires all three into the parser at lines 147 to 150 and 226 to 227, with `dest` `job_id`, `max_steps` and `max_seconds`. `apps/cli/commands/worker_facade_cmd._cmd_mission_run` reads `run_id`, `project`, `iterations`, `json` and `no_llm` and NONE of those three, and its own docstring states plainly that the second mode died with the cluster. So `remedy mission run <id> --max-steps 3 --max-seconds 30 --job-id x` parses, runs, and ignores every one of them — the failure mode a flag that errors does not have, because the user is told nothing. The section comment above the entry still reads "mission (facade over dogfood run-loop + morning report)" and the `related` tuple still names `dogfood.run-loop`, which is one of R-0859's two dangling references, so this finding and that one meet in the same twenty lines. WHY MEDIUM: wrong state on disk under `apps/`, user-visible through `remedy mission run --help` and every catalog reader, and no gate in the repository can see it — the suite is green, ruff is clean, and nothing asserts that a declared option is read by the handler it is declared for. THE FIX, which this round performs: the three options and the second mode go OUT of the entry rather than being wired IN, because wiring them would be building a feature under a deletion mandate; DECISION F275 D14 records that choice and its alternative. FIX CLAUSE, binding on any later round that adds an option to a catalog entry: the option is read by the handler in the same commit, or it is not declared — a declared option is a promise the parser keeps and the handler breaks.

Note: F275 R24 — new evidence for the OPEN finding R-0870, added rather than given an id of its own per `docs/agents/planner_reviewer_prompt.md` §3 item 30, because it is the same defect in the same class and R-0870's own fix clause is what should have caught it. R-0870 records comments falsified by a deletion in files the deletion's change set did not name. THESE ARE THE THIRD AND FOURTH INSTANCES, both measured by the reviewer at `ea5f8128` while gating round 23, and both are in files that ROUND'S OWN change set DID name — which is the widening. FIRST, `packages/common/public_text_redaction.py` line 8 still reads "F275 round 21 deletes the trust gate", while round 21 MOVED the helpers and round 22 deleted the gate at `0242c0a3`; the round 23 pair repaired line 4 of that same docstring and left line 8 contradicting it four lines below. SECOND, `tests/cli/test_mission_cmd.py` carries `test_the_cockpit_no_longer_imports_the_cluster_readiness_module`, whose NAME and whose entire docstring argue for the `not in source` assertion the round 23 pair removed; what survives asserts the POSITIVE import of the carried module, so the test no longer does what it is called. The worker declared the second before the reviewer measured it, applied the slice verbatim as constraint 1 required, and was right to. WHY NEITHER IS A NEW ID: R-0870 is OPEN, its subject is exactly "a comment falsified by a deletion that no gate can see", and both are Low for the same reason — nothing executes either line. WIDENED FIX CLAUSE, replacing the reach of R-0870's original and binding on every remaining round of this feature: a pair that narrows or removes a definition, an assertion or a sentence is authored against the WHOLE enclosing unit — the docstring it sits in, the test name above it, the section comment over it — and the block states what it read, because a sweep for a deleted IDENTIFIER cannot see a sentence that describes the deleted thing in words.

Note: F275 R24 — new evidence for the OPEN finding R-0847, added rather than given an id of its own per §3 item 30, because R-0847's subject is precisely the guard that should have caught this and did not. R-0847 records that `tests/cli/test_advertised_commands.py` cannot see an advertisement whose command GROUP has been deleted. THE MEASUREMENT, taken by the reviewer at `ea5f8128`. `docs/system/mission-run-loop-morning-report-v0.md` is an operator-facing page under `docs/system/`, pinned by `tests/cli/test_product_spine.py`, and its "Internal commands (advanced)" section advertises SIX commands of the deleted `dogfood` group — create, run-loop, morning-report, step, replay and show — while its Terminology note tells the reader those commands "remain available for debugging and backwards compatibility". The sharper half is its QUICK START, which the page itself labels recommended: `remedy mission report <run_id> --job-id <job_id> --json` names a positional and an option that the shipped entry for `mission.report` does not have — its arguments are `job_id`, `--markdown` and `--json` — so the one invocation the page recommends to an operator cannot parse. This page survived R-0861's three-page sweep, which is RESOLVED, and four subsequent deletion rounds, for exactly the reason R-0847 names: every one of those rounds swept for command ids and for the spaced form of groups that still exist. R-0847's own fix clause binds the first round that may edit the scanner and this round does not edit it, so the clause is untouched; what this round repairs is the PAGE. The half of R-0847's clause naming `worker_registry.py` line 710 is already discharged by round 20 deleting that module, and this note records that so the clause is not read as outstanding in full.

Note: F275 R24 — new evidence for the OPEN finding R-0832, and the measurement that makes most of its fix clause moot, recorded rather than given an id per §3 item 30. R-0832 records that the cluster deletion map measures IMPORT edges only, so a consumer coupled to the cluster by EVENT NAME survives the deletion as dead code, and its fix asks for a second measurement recording those couplings so the deletion round removes them with their emitter. THE MEASUREMENT, taken by the reviewer at `ea5f8128` over the 1652 tracked files outside `.agent/` and `.data/`: `context_pack_created`, `NT_CONTEXT_PACK` and `_build_context_pack_node` — the whole first half of R-0832's evidence — are at ZERO, removed by the rounds that deleted their module group rather than by any map. What survives is the second half, `context_budget_optimized`, at three sites and no emitter: a schema entry in `packages/orchestration/event_schemas.py`, a bookkeeping classification in `apps/ui/src/api/actionClass.ts`, and four lines of `tests/orchestration/test_event_ledger.py` that pin the schema. SO THE COUNTER-MEASURE HAS LOST ITS SUBJECT: the deletion is finished, no further emitter can die, and the map R-0832 asks to extend is itself retired by R-0868's clause in the next round. WHAT REMAINS OWED is the residue, and DECISION F275 D14 rules it left standing rather than swept, with the reason. R-0832 STAYS OPEN and its text is not rewritten; what resolves it is the residue's removal by a feature that owns the cockpit's event vocabulary, and this note is the dated record of why this feature is not that one.

Done: R-0864 — Resolved by F275 round 23's C4 `64932207`, verified by the reviewer of session 13 reading the committed diff rather than the worker's report. Both halves the fix clause named are gone. FIRST, `tests/cli/test_product_spine.py::test_fast_lane_no_heavy_runtime_smoke` no longer names `test_overnight_executor_cli.py` in its `heavy` list; the reviewer re-measured that the three surviving entries — `test_worker_cli_runtime.py`, `test_self_dogfood_execution_cli.py` and `test_smoke_scripts.py` — all resolve to files on disk, so the guard bites for every entry it still holds, which is what made the fourth entry a defect rather than a harmless line. SECOND, `tests/cli/test_mission_cmd.py` no longer asserts `"packages.orchestration.overnight_readiness" not in source`, an assertion that could not fail for any possible future state once round 19 deleted that module; the POSITIVE assertion beside it, that `ui_server.py` imports from the carried `mission_readiness` module, survives and still bites. The round registered no `Landed:` line for this id because the block's authored text named only R-0870, which is a reviewer omission recorded as a prose slip and not a defect on disk — the fix itself landed correctly and the reviewer verified it independently before writing this paragraph. What this resolution does NOT claim is that the class is gone: a deletion round still has to search the suite for negative assertions naming what it removes, because an import goes red and a negative assertion goes quiet, and that lesson stays in R-0864's original text where a later reader will find it.
<<<END LEDGER24>>>

<<<BEGIN SLIPS24>>>
2026-09-10 · F275 R23 · The round 23 block's G1 ordered the transport digest compared against "the digest in this block's BEGIN marker", and the block carries no BEGIN marker holding a digest — its `<<<BEGIN …>>>` markers only delimit slices, and the sha256 travelled in the delegation wrapper instead. The worker verified against the wrapper's digest, said so, and all three artefacts matched, so nothing landed wrong. The lesson is that a gate naming WHERE a reference value lives is checked against the artefact that actually carries it, because under self-drive the block and the wrapper are two different texts and only one of them is copied to disk.

2026-09-10 · F275 R23 · The round 23 block's constraint 4 stated that every entry already in `.agent/prose_slips.md` is separated from its neighbour by a BLANK line, and the worker measured 244 blank-separated adjacent pairs against 14 on consecutive lines out of 258. The constraint was ORDERING the right thing and CLAIMING a universal that the file falsifies — the §3 item 11 shape, a claim about another file's contents stated as a universal nobody counted. Nothing landed wrong because the slice followed the convention the constraint ordered. The lesson is to order the format and state the measurement beside it, never to justify an order with an unmeasured "every".

2026-09-10 · F275 R23 · The round 23 block's LANDED23 slice named only R-0870, while the same round's Q3 and Q4 pairs were verbatim the repair R-0864's fix clause asks for, so R-0864's fix landed with no `Landed:` line and the finding stayed counted open with no pointer to `64932207`. The worker found it, declined to write a line the change set did not authorise, and flagged it — which is the correct handling and is why nothing is wrong on disk. The lesson is that a block whose change set discharges a fix clause writes the `Landed:` line for THAT id too, and the check is mechanical: for every fix clause the round's own DECISION says it takes, grep the block's authored text for the id.
<<<END SLIPS24>>>

<<<BEGIN DEC24>>>
## DECISION F275 D14 (2026-09-10, F275 round 24) — three rulings the D3 sequence needs: what happens to a dead option, to the last event-name residue, and to the rounds the sequence still owes

(a) A DEAD ADVERTISED OPTION IS REMOVED, NEVER WIRED. `remedy mission run` declares
    `--job-id`, `--max-steps` and `--max-seconds`; `apps/cli/grouped.py` wires all three
    into the parser and `_cmd_mission_run` reads none of them, which R-0871 measures at
    `ea5f8128`. CHOSEN: the three `ArgDef`s and the description's second mode come OUT of
    the catalog entry in this round, so the parser refuses what the handler cannot honour.
    ALTERNATIVE CONSIDERED: wire them through to `_cmd_mission_run_loop` so the flags mean
    what they say — rejected because that is building a budget feature inside a deletion
    feature, which AGENTS.md Scope Control forbids by name, and because the F070 loop's
    own budget belongs to the feature that owns that loop rather than to this one.
    CONSEQUENCE, stated because it is user-visible: an operator who has been passing
    `--max-steps` will now get an argparse error where they previously got silence. That is
    the safer direction — the flag never did anything — and R-0871 is the record of it.

(b) THE LAST EVENT-NAME RESIDUE IS LEFT STANDING, DELIBERATELY, AND RECORDED WHERE A
    READER WILL LOOK. `context_budget_optimized` survives at three sites with no emitter
    anywhere in the tree: a schema entry in `packages/orchestration/event_schemas.py`, a
    bookkeeping classification in `apps/ui/src/api/actionClass.ts`, and four pinning lines
    in `tests/orchestration/test_event_ledger.py`. CHOSEN: none of the three is touched by
    this feature. WHY: the classification is cockpit behaviour — it decides whether a kind
    is filtered out of the NowCard — so removing it is a product change to a surface F275
    has not entered in twenty-four rounds, and it carries its own vitest test that this
    workflow cannot run in the disposable worktree its guardrails require. An entry that
    classifies an event which never arrives is inert; a cockpit filter changed by a
    deletion feature is not. ALTERNATIVE CONSIDERED: delete all three in this round —
    rejected on scope and on the measurement that nothing observable depends on the entry
    existing. The `Note: F275 R24` entry on R-0832 carries the site list, so a later
    feature that owns the cockpit's event vocabulary can find it by id.

(c) THE D3 SEQUENCE RUNS ONE ROUND LONGER THAN D13 DISTRIBUTED IT. DECISION F275 D13 gave
    "the next round" R-0832's couplings, R-0859's test and repairs, R-0858's F267 repair,
    R-0843's `Groups` table and R-0868's retirement. MEASURED at `ea5f8128` while
    assembling this block: R-0859's repairs sit inside the same twenty lines as R-0871,
    which D13 could not know about because the reviewer found it while measuring R-0859;
    and the operator page R-0847's new evidence names is a fourth repair of the same class.
    Those three are one coherent change set — surviving surfaces that advertise deleted
    things — and adding the retirement of four scaffolding files plus two roadmap and docs
    repairs to them exceeds DECISION F085 D6's 490-line block cap, which DECISION F009 D16
    makes a reason not to deliver rather than a reason to trim. CHOSEN: this round takes
    the advertising surfaces; the round after it takes R-0868's retirement, R-0858's F267
    repair and R-0843's banner, and the D3 sequence closes there. ALTERNATIVE CONSIDERED:
    drop the page repair to keep D13's distribution intact — rejected because the page
    recommends an invocation that cannot parse, which is the sharpest instance of the class
    this whole feature has produced, and deferring it to keep a bookkeeping promise is the
    wrong trade.

HOW TO REVERSE: delete this decision. (a) is reversed by restoring the three `ArgDef`s and
wiring them; (b) by any feature that owns the cockpit's event vocabulary sweeping the three
sites; (c) by any later relay redistributing the remaining clauses across rounds as it
prefers, since every one of them still names the finding it discharges.
<<<END DEC24>>>

Q1 — apps/cli/command_catalog.py — REWRITE — the comment's trailing rule is 10 x U+2500
<<<BEGIN Q1 FROM>>>
    # ── mission (facade over dogfood run-loop + morning report) ──────────
    CommandEntry(
        command_id="mission.run",
        group_id="mission",
        subcommand="run",
        description="Run a mission's orchestrator loop when the id is a mission (F070); otherwise the bounded dogfood run loop for that run id. Stops on a terminal move, the iteration limit, a stop request or an escalation.",
        action_class="write_metadata",
        args=(
            ArgDef("run_id", "Mission id (F070 loop) or run id (dogfood loop)"),
            ArgDef("--job-id", "Job UUID", required=False, is_option=True),
            ArgDef("--max-steps", "Max loop steps (default 10)", required=False, is_option=True),
            ArgDef("--max-seconds", "Max wall-clock seconds (default 300)", required=False, is_option=True),
            ArgDef("--iterations", "Max orchestrator iterations this run (mission id only)", required=False, is_option=True),
            ArgDef("--no-llm", "Run without a provider — reports the honest no_provider terminal", required=False, is_option=True, is_flag=True),
            _PROJECT_SCOPE_OPT,
            _JSON_OPT,
        ),
        supports_json=True,
        related=("mission.report", "mission.ledger", "dogfood.run-loop"),
    ),
<<<END Q1 FROM>>>
<<<BEGIN Q1 TO>>>
    # ── mission (the F070 orchestrator loop, keyed on a mission id) ──────
    CommandEntry(
        command_id="mission.run",
        group_id="mission",
        subcommand="run",
        description="Run the F070 orchestrator loop for one mission. Stops on a terminal move, the iteration limit, a stop request or an escalation.",
        action_class="write_metadata",
        args=(
            ArgDef("run_id", "Mission id (F070 loop)"),
            ArgDef("--iterations", "Max orchestrator iterations this run", required=False, is_option=True),
            ArgDef("--no-llm", "Run without a provider — reports the honest no_provider terminal", required=False, is_option=True, is_flag=True),
            _PROJECT_SCOPE_OPT,
            _JSON_OPT,
        ),
        supports_json=True,
        related=("mission.report", "mission.ledger"),
    ),
<<<END Q1 TO>>>

Q2 — apps/cli/command_catalog.py — REWRITE — the repo.status cross-reference
<<<BEGIN Q2 FROM>>>
        related=("readiness.show",),
<<<END Q2 FROM>>>
<<<BEGIN Q2 TO>>>
        related=("readiness.job",),
<<<END Q2 TO>>>

Q3 — tests/test_command_catalog.py — REWRITE — the referential-closure test R-0859 asks for
<<<BEGIN Q3 FROM>>>
            assert sub == cmd.subcommand, f"command_id suffix mismatch: {cmd.command_id}"


class TestCatalogClassification:
<<<END Q3 FROM>>>
<<<BEGIN Q3 TO>>>
            assert sub == cmd.subcommand, f"command_id suffix mismatch: {cmd.command_id}"

    def test_every_related_reference_resolves_to_a_live_command(self) -> None:
        """R-0859: nothing here resolved `related=` against the catalog.

        A deletion round removes a command and its own entry, and the entries
        that POINT at it keep pointing. Every other guard in this class reads
        an entry's own fields, so a cross-reference to a command that no
        longer exists was invisible to all of them — and `remedy list` then
        offers the reader a sibling that resolves to nothing.
        """
        live = {cmd.command_id for cmd in CATALOG}
        dangling = sorted(
            (cmd.command_id, ref)
            for cmd in CATALOG
            for ref in (cmd.related or ())
            if ref not in live
        )
        assert dangling == [], f"related= names commands that do not exist: {dangling}"


class TestCatalogClassification:
<<<END Q3 TO>>>

Q4 — docs/system/mission-run-loop-morning-report-v0.md — REWRITE — the Quick start
<<<BEGIN Q4 FROM>>>
```bash
# 1. Run a bounded mission loop
remedy mission run <run_id> --job-id <job_id> --json

# 2. Read the morning report
remedy mission report <run_id> --job-id <job_id> --json
```

These are the operator-facing commands. They call the same logic as the
internal `dogfood` commands below.
<<<END Q4 FROM>>>
<<<BEGIN Q4 TO>>>
```bash
# 1. Run a bounded mission loop, keyed on a MISSION id
remedy mission run <mission_id> --json

# 2. Read the morning report, keyed on a JOB id
remedy mission report <job_id> --json
```

These are the operator-facing commands, and since F275 they are the only
ones: the internal `dogfood` group they used to wrap is deleted.
<<<END Q4 TO>>>

Q5 — docs/system/mission-run-loop-morning-report-v0.md — REWRITE — the stop conditions
<<<BEGIN Q5 FROM>>>
- Budget exhausted (step, token, or wall-clock limit reached)
- Operator stopped (manual stop command)
- Max loop steps reached (loop-level cap, default 10)
- Max loop seconds reached (wall clock, default 300)
- No safe next action
- Internal error
<<<END Q5 FROM>>>
<<<BEGIN Q5 TO>>>
- Budget exhausted (token budget reached)
- Operator stopped (manual stop command)
- Iteration cap reached (`--iterations`)
- No safe next action
- Internal error

Remedy deliberately ships no per-step or wall-clock cap on `remedy mission
run`. The `--max-steps` and `--max-seconds` flags belonged to the deleted
dogfood loop, were accepted and ignored by the surviving handler, and F275
removed them rather than wiring them in — see R-0871 and DECISION F275 D14.
<<<END Q5 TO>>>

Q6 — docs/system/mission-run-loop-morning-report-v0.md — REWRITE — the terminology note
<<<BEGIN Q6 FROM>>>
The CLI group `dogfood` is internal developer naming. Operator-facing
documentation uses:

- **Mission Run** — the bounded loop
- **Mission Report** — the morning report
- **Self-Repair Proposal** — suggested fix from analysis

The internal `dogfood` commands remain available for debugging and
backwards compatibility.

## Internal commands (advanced)

```bash
# Create a run
remedy dogfood create <job_id> --json

# Run the bounded loop (low-level)
remedy dogfood run-loop <run_id> --job-id <job_id> --max-steps 10 --max-seconds 300 --json

# Morning report (low-level)
remedy dogfood morning-report <run_id> --job-id <job_id> --json

# Single step (fine-grained control)
remedy dogfood step <run_id> <job_id> --json

# Replay analysis
remedy dogfood replay <run_id> <job_id> --json

# Quick status
remedy dogfood show <run_id> <job_id> --json
```
<<<END Q6 FROM>>>
<<<BEGIN Q6 TO>>>
The CLI group `dogfood` was internal developer naming for the prototype this
page was written against. Operator-facing documentation uses:

- **Mission Run** — the bounded loop
- **Mission Report** — the morning report

Remedy deliberately ships no low-level equivalents of these two commands.
The whole `dogfood` group — create, run-loop, morning-report, step, replay
and show — was deleted by F275 together with the module behind it, and
nothing stands in for it: there is no alias, no shim and no compatibility
reader, per AGENTS.md Scope Control. The operator-facing pair above is the
only surface, and git history is where the prototype lives now.
<<<END Q6 TO>>>

Q7 — docs/system/mission-run-loop-morning-report-v0.md — REWRITE — the self-repair section
<<<BEGIN Q7 FROM>>>
## How Self-Repair Proposals fit

The morning report shows:

- Whether proposals exist
- Latest proposal status
- How many await operator review
- Command to inspect proposals

Self-repair proposals are never auto-created by the loop. They come from
prior analysis (replay, review, test failures).
<<<END Q7 FROM>>>
<<<BEGIN Q7 TO>>>
## How Self-Repair Proposals fit

They do not, any more. The `self-repair` group and the proposal queue behind
it were deleted by F275; the approval gate F017 owns inherited the idea of a
policy-authorised approval, and no surviving command creates, lists or
approves a self-repair proposal. The finding R-0845 records what was lost and
DECISION F260 D3 records which feature took which idea.
<<<END Q7 TO>>>
