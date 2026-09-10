── STEP T003 (1 of n) — F275 ─────────────────────────────────
Goal:        Rule which live command inherits the classic runner's execution
             path, then delete the half of that path that no production caller
             reaches — `agent_loop.run_agent_loop` and its private helpers.
Bundle:      C0a save this block · C0b mirror it · C1 the plan · C2 the round 31
             verdict and two prose slips · C3 DECISION F275 D18 · C4 the
             production deletion and its docs repair · C5 the handback.
Change:      exactly the paths listed here and nothing else —
             `.agent/authored/f275-r32.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/prose_slips.md`, `.agent/decisions.md`,
             `packages/orchestration/agent_loop.py`,
             `tests/test_agent_loop_execution.py` (deleted),
             `tests/storage/test_persistence.py`,
             `docs/system/architecture.md`, plus `.agent/handoff.md` at C5.
Constraints: the numbered list below.
Done when:   gates G1 to G8 below are RUN and their real exit codes recorded.
Handback:    completion report + rewrite `.agent/handoff.md`.
──────────────────────────────────────────────────────────────

## Base

This round's base is `9d1788fe`, the tip of
`feature/f275-one-world-completion-part-three` at authoring time. Every reading
this block states was taken by the reviewer at that commit, in the primary
checkout, before delegation.

## Constraints

1. APPLY EVERY SLICE BYTE FOR BYTE. A slice is never reflowed, retyped,
   trimmed or repaired. If a slice does not fit its target, DECLARE it in the
   handback and apply the rest; never silently reconcile.
2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, exactly. No extra commit,
   no dropped commit, no reordering. C1 is the first substantive commit, which
   is what §3 item 23 requires of a round that touches the finding ledger.
3. THE CHANGE SET IS THE PATH LIST IN THE HEADER'S `Change:` LINE, together with
   `.agent/handoff.md`, which that line names separately as C5's own target. A
   path not named there is not written, not created and not deleted.
4. EVERY APPEND IS `pre + ONE newline + slice`. All three append targets end in
   a single `\n` at the base: `.agent/live_review.md` at 793191 bytes,
   `.agent/prose_slips.md` at 217298 bytes, `.agent/decisions.md` at 1024587
   bytes. Those three figures are the reviewer's own readings at `9d1788fe`.
5. NO PRODUCTION LINE MOVES BEFORE C4. C1, C2 and C3 write only under `.agent/`.
6. DESTRUCTIVE VERIFICATION IS ISOLATED. Every mutation and every red proof runs
   inside a disposable `git worktree` under `.remedy-wt/`, never in the primary
   checkout, per self_drive_protocol.md G5. Remove and prune it before the
   handback; `git worktree list` must read exactly ONE entry at C5.
7. THE SUITE RUNS SERIALLY. `python3 -B -m pytest tests/ -q`, no `-n auto`. A
   fresh worktree has no `apps/ui/node_modules`; link it before any run that
   collects `tests/orchestration/test_test_runner.py`, or that class fails on an
   unresolvable `vitest/config`, which is a worktree artifact and not a result.
8. THIS ROUND REGISTERS NO FINDING AND RESOLVES NONE. The open set is 87 by
   distinct id at the base and must read 87 at C4. The next free id is R-0874
   and this round does not spend it. The reason is measured, not assumed, and
   is stated in DECISION32: the deleted function has no production caller, so
   amend0908-f275-finish rule 4's "user-observable behaviour lost" is empty for
   this change set.
9. PAIR SHAPES, from the containment test the reviewer ran at `9d1788fe`, one
   reading per pair: D1 `TO contains FROM: false` → REWRITE. D2
   `TO contains FROM: false` → REWRITE. D3 `TO contains FROM: false` → REWRITE.
   D4 `TO contains FROM: false` → REWRITE. All four are rewrites, so each
   carries the §4.9 FROM-0x obligation.
   D2 IS THE ONE EXCEPTION TO THE TO-1x HALF, and the block states it rather
   than ordering a count no run can produce. D2 deletes a line from a
   four-line code fence, so its TO is a strict PREFIX of its FROM and already
   occurs once in `docs/system/architecture.md` at the base — the reviewer
   measured `TO x1` there at `9d1788fe`. Demanding "TO 0 to 1" for D2 would be
   unsatisfiable by every possible round. D2's honest gate is the one G7 orders:
   FROM 1 to 0, the `run_agent_loop(job, *, max_cycles=3` signature 1 to 0, and
   the `derive_agent_loop_state` signature line UNCHANGED at exactly 1.
10. THE PROSE SLIPS TARGET IS READ BEFORE IT IS APPENDED TO. Round 31's own slip
    records a booking round that trusted its carrier instead of its target.
    Confirm that neither SLIPS32 line is already present in
    `.agent/prose_slips.md` at the base before appending, and report the reading.
11. THE FULL SUITE RUNS ONLY AFTER C4 IS COMMITTED, NEVER WITH THE DELETION
    STAGED. This is not style; the reviewer hit it while dry-running this exact
    change and it would otherwise cost the round a false red.
    `tests/orchestration/test_evidence_index.py::TestPorcelainParsing::test_every_enumerated_path_exists_in_this_repo`
    calls `dirty_source_test_files(root)` and asserts every path it enumerates
    EXISTS on disk. A tracked test file that has been `git rm`-ed but not yet
    committed is in the dirty set and is not on disk, so the guard fails with
    `enumerated a nonexistent path: tests/test_agent_loop_execution.py` for
    exactly as long as the working tree is dirty. Measured in the disposable
    worktree at `9d1788fe`: with the change applied and UNCOMMITTED the suite
    reads `1 failed, 18337 passed, 24 skipped`; with the same change COMMITTED
    the guard's own file reads `33 passed` at exit 0. The guard is correct and
    is not to be touched.

## SLICE PLAN32 → whole-file replacement of `.agent/plan.md`

<<<PLAN32
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE.

## Current Step

ROUND 32 opens T003. It rules the inheritance question T003 owes before any command dies —
which live command inherits a bounded-cycles run and a single-pass run — against the shipped
catalog by import, and records it as DECISION F275 D18. It then lands the one half of the
classic runner that no production caller reaches: `run_agent_loop` in
`packages/orchestration/agent_loop.py`, its three private helpers, the tests that exist only
to drive it, and the architecture page's description of it.

## Next Steps

1. Delete the `job.run` and `job.run-next` command surface under the D18 ruling: the catalog
   entries, the dispatch entries, the two `related=` tuples that would otherwise dangle, and
   the advertisements in the eight orchestration modules that print them.
2. Absorb the two handlers under the `job.resume` door, one owner and no copy, and register
   the surfaces D18 names as genuinely lost.
3. The flip DECISION F275 D17 sized, as the one declared-oversize commit AGENTS.md permits
   per feature, re-deriving the site set at its own base.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- The open set is 87 by distinct id at this round's base `9d1788fe`, over 102 registrations
  against 15 resolutions. This round registers none and resolves none, so it stays 87. Four
  are High — R-0803, R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per
  DECISION F272 D12.
- Step 1 above turns two surviving `related=` tuples dangling the moment the commands die.
  The catalog integrity guard resolves every tuple against the live id set, so that repair
  is not optional and belongs in the same commit as the deletion.
PLAN32

## SLICE RECORD32 → append to `.agent/live_review.md`

<<<RECORD32
Gate: F275 R31 — the F275 round 31 entry. VERDICT PASS, written by the planner and reviewer of session 15 after reading the committed range `0b009325`..`f605901d` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs, and booked here by round 32 rather than by a round of its own, per operator amendment amend0827-process-diet rule 1, carried from the pushed `.agent/handoff.md` at `9d1788fe`. The worker's report was evidence for no line of it. Seven single-parent commits C0a `817ba547`, C0b `184f1edc`, C1 `a53343c8`, C2 `293b54d3`, C3 `123554a5`, C4 `0ce086ae` and C5 `f605901d`, per-commit insertions 381, 326, 17, 8, 498 and 16 for the six before the handback, every one under the AGENTS.md DECISION F104 D1 cap of 500. G1 IS A REAL TRANSPORT CHAIN AND NOT MERELY A SELF-CONSISTENT ONE, which is the distinction §3 item 37 exists to force: the reviewer's scratch original at `.remedy-wt/f275-r31-block.md` was written AND HASHED BEFORE delegation at `cbd927e5268daac8557291e99fc6b50dd99ece78adf448e6bb133036f8b2bf19`, and both committed copies are 33235 bytes at that same digest, so the first link of the chain predates the worker. G2: `.agent/plan.md` byte-identical to PLAN31 at 1918 bytes, 37 lines against the cap of 50, both mandated headings exactly once. G3 over ALL THREE append targets — `.agent/live_review.md` 790277, `.agent/prose_slips.md` 215418 and `.agent/decisions.md` 1017073 bytes before — each post-blob equal to its pre-blob then ONE newline then the slice as extracted from the committed C0a blob, the joining byte READ BACK at offset len(pre) and reading a newline in all three, the structural reader counting N from each slice — 1, 3 and 8 paragraphs — and matching the last N blank-line units IN ORDER, and all three negative controls flipped INSIDE THE FIRST appended paragraph and REJECTED by BOTH readers. G4: THE OPEN SET IS 87 BY DISTINCT ID at the base and 87 at the round's tip, over 102 registrations against 15 resolutions; this round registered none and resolved none. G5 and G6 ARE THE ROUND'S REAL EVIDENCE AND THE REVIEWER RAN THE MEASUREMENT ITSELF BEFORE DELEGATING: the DECISION F272 D7 descriptor probe was built by the reviewer, corrected twice against its own failures, and the FULL SUITE was run under it TWICE at `0b009325`, reading `18350 passed, 23 skipped` at exit 0 both times and 1757 executed `Job` sites both times; the worker's two runs read the same summary line at exit 0 and its symmetric difference over `(owner, field, mode, path, line, function)` is EMPTY at 2734 records each, so the probe reproduces across FOUR independent full-suite runs. G8: porcelain EMPTY, ONE worktree, no `.agent/STOP`, the change set an EXACT set match over seven paths, and NO path under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` in the whole range — which is T002's own "no production line moves", met. TWO CORRECTIONS ARE CARRIED IN THIS ENTRY RATHER THAN AS SEPARATE IDS, because neither left a wrong state on disk under `packages/`, `apps/`, `tests/` or `docs/`. FIRST, THE LARGE DEVIATION IS A REVIEWER SPEC DEFECT AND ITS CAUSE IS MEASURED: the worker read the alternative route at 977 sites over 976 lines where the block states 1201 over 1087, because `JobPlan` is a DATACLASS whose generated `__init__` carries the literal `co_filename` `<string>`, and SPEC-PROBE clause (d) said the walk stops at the innermost frame "whose filename lies under the worktree root" without saying the test reads the RAW filename — `os.path.abspath("<string>")` resolves under that root, so the walk halted at a synthetic frame and every construction write collapsed into one key per field. The arithmetic closes exactly: 960 + 15 + 1 + 1 = 977 against 960 + 15 + 113 + 113 = 1201. For the purpose T002 states, attributing outward to the construction site is the correct reading, so the block's 1201 over 1087 stands and the inventory's figure is an undercount of the ALTERNATIVE route alone; nothing load-bearing moves, because DECISION F275 D17 rejects that route on a line count far over the 500-insertion cap and 976 is as far over as 1087. THE RULED SITE SET IS UNTOUCHED: all twelve probe and union figures agree exactly, the union at 1768 sites over 1766 distinct changed lines, 357 production in 68 files and 1409 test in 117 files, with 11 provably-`Job` sites never executed and 92 that a static sweep positively attributes to something other than `Job`. SECOND, DECISION F275 D17's SENTENCE THAT ZERO COMMITS ON THIS BRANCH EXCEED 500 INSERTIONS IS TOO WIDE BY A QUANTIFIER, and this is its dated correction rather than a rewrite of the landed text, per §3 item 20. Measured at `f605901d`: two MERGE commits do exceed it — `a1df5d70` at 805 and `b6e0f257` at 804 insertions against their first parents, both merging `main` into this branch to bring in amend0908-brainstorm-intake — and the reviewer's original walk used `git log --numstat`, which emits no diff for a merge, so those two were read as zero rather than examined. Over the commits carrying AUTHORED work the claim holds and is stronger than D17 states: the maximum single-parent insertion count across that range is 498, and it is round 31's own C3. The RULING is untouched, because a merge importing upstream history is not a commit whose diff a worker authored and it cannot spend the declared-oversize allowance AGENTS.md rations per feature. THE REMAINING DECLARED DIFFERENCES ARE SMALL, EXPLAINED AND ACCEPTED: the worker's static sweep proves 322 sites where the reviewer's proves 325 and reads 587 constructions against 586, because it additionally resolves a call whose callee is an ATTRIBUTE named `Job`, and it names the one extra site; both readings put 11 in the never-executed set and both produce the SAME union, which is the figure the ruling uses. The pilot suite run the worker discarded is correctly classified — a lint-ceiling test reddened by the worker's own untracked instruments and a vitest test reddened by a fresh worktree having no `node_modules`, with that class re-run WITHOUT the probe and green, which is exactly the discriminator G5 ordered. Trimming the inventory to 498 insertions is accepted: the worker compacted the STATIC instrument's source and verified its output `cmp`-identical after every edit rather than dropping content SPEC-INVENTORY mandates, and spending F275's one oversize allowance on an inventory would have contradicted the decision that round exists to record. NO FINDING IS REGISTERED AND NONE IS RESOLVED BY THIS GATE.
RECORD32

## SLICE SLIPS32 → append to `.agent/prose_slips.md`

<<<SLIPS32
2026-09-10 · F275 R31 · The round 31 block's SPEC-PROBE told the worker to attribute an access to the innermost stack frame "whose filename lies under the worktree root" without saying that the test reads the RAW `co_filename`, and a dataclass's generated `__init__` carries the literal filename `<string>`, which `os.path.abspath` resolves to a path UNDER that root. The worker's faithful implementation therefore stopped the walk at a synthetic frame and collapsed every `JobPlan` construction write into one key per field, reading the alternative route at 977 sites where the reviewer read 1201. Both instruments were correct against the words; the words admitted two readings, and the one the reviewer never considered is the one a path-normalising helper makes natural. A spec that names a PREDICATE over a filename says which string the predicate is applied to, because `<string>`, `<stdin>` and `<frozen importlib._bootstrap>` are filenames that are not paths and every one of them normalises into whatever directory happens to be current.

2026-09-10 · F275 R31 · DECISION F275 D17 landed the sentence that ZERO commits on this branch exceed 500 insertions, measured with `git log --numstat`, which emits NO diff for a merge commit — so the two merges bringing `main` into this branch, at 805 and 804 insertions against their first parents, were read as zero rather than examined. The claim is true of every commit carrying authored work, where the real maximum is 498, and the ruling that rests on it is unaffected; the quantifier is simply wider than the measurement that produced it. A sweep that quantifies over COMMITS states which commits its tool can SEE, because the commit shapes a tool silently skips are exactly the ones nobody thinks to check.
SLIPS32

## SLICE DECISION32 → append to `.agent/decisions.md`

<<<DECISION32
## DECISION F275 D18 (2026-09-10, F275 round 32) — T003's inheritance ruling: the classic runner's COMMAND SURFACE dies and its EXECUTION PATH is inherited by `job.resume`; `run_agent_loop` dies outright and inherits nothing

CONTEXT. `docs/roadmap/features/T2_F275.md` T003 deletes `job.run --cycles`, `job.run-next`, their handlers and their tests. Operator amendment amend0908-f275-finish rule 4 requires that a surviving importer lose the import and the code path in the SAME commit, and that any user-observable behaviour lost be registered as a finding naming the inheriting feature — never a stub, shim or copy. Session 15's handoff deferred one question to this round and named four candidate inheritors — `do.run`, `do.continue`, `worker.run` and `mission.run` — without measuring which of them actually inherits a bounded-cycles run. Every reading below was taken by the reviewer at `9d1788fe` against the SHIPPED catalog by import and against the source on disk, not from the handoff.

WHAT THE CATALOG HOLDS, measured by importing `apps.cli.command_catalog` at `9d1788fe`: 222 commands in 44 groups, of which 27 are in the `job` group. Exactly three entries carry an argument named `--cycles`: `job.run`, `job.resume` and — as `--max-cycles` — `do.run`. `job.resume`'s own description is "Resume a job. Without --checkpoint: continue from the newest valid cycle checkpoint (F047)", its argument list carries `--cycles` with the help text "Maximum cycles for the resumed run (capped by the rollout default)", and its `related=` tuple already names `job.run`.

CHOSEN — `job.resume` INHERITS BOTH, BY ABSORPTION RATHER THAN BY REDIRECTION, and the ruling rests on three measurements rather than on the shape of the names. FIRST, `job.resume` is ALREADY the second caller of the bounded-cycles handler: `_cmd_job_resume` ends at `apps/cli/commands/job.py:1076` with `_cmd_job_run_cycles(job_id_str, cycles=cycles, json_output=json_output)`. SECOND, it already performs the identical plan-approval gate, and the source says so in its own comment at that call site's third step — "the same check `remedy job run` makes". THIRD, and this is the measurement that rules out the obvious alternative, the SINGLE PASS IS NOT A SEPARABLE SURFACE: `_cmd_job_run_cycles` delegates to `_cmd_run_next_task_local` whenever `resolved.max_cycles <= 1`, and one cycle is the SHIPPED DEFAULT under the F046 rollout cap until the F075 milestone gate raises it. Deleting `_cmd_run_next_task_local` outright would therefore leave `job.resume` a no-op under today's configuration. The two handlers move under the `job.resume` door as private functions of the surviving command, ONE OWNER AND NO COPY, which is a move and not the compatibility shim AGENTS.md's Scope Control forbids.

WHAT IS GENUINELY LOST AND OWES A FINDING WHEN THE SURFACE DIES, stated here so the round that deletes the commands does not have to re-derive it: the `--unattended` flag and the `--yes` cost-preview skip at the `job.run` door, because `_cmd_job_resume` passes neither to the handler it calls; and `job.run-next` as a user-visible single-pass entry point. Those are the amend0908 rule 4 registrations that round owes, and they are NOT owed by this round, which deletes no command.

WHAT THE SAME ROUND MUST REPAIR IN THE SAME COMMIT, measured rather than predicted: deleting the two commands leaves TWO surviving `related=` references dangling — `job.plan` names `job.run-next` and `job.resume` names `job.run` — and `tests/test_command_catalog.py::TestCatalogIntegrity::test_every_related_reference_resolves_to_a_live_command` resolves every tuple against the live id set, so the suite goes RED unless both tuples move in that commit. `tests/test_command_catalog.py:252` additionally pins `job.run-next` in a literal id list.

THE HALF THIS ROUND LANDS, AND WHY IT INHERITS NOTHING. `packages/orchestration/agent_loop.py` carries a second, independent door to the same single pass: `_run_next_task_step` imports `_cmd_run_next_task_local` from the CLI and is called only from `run_agent_loop`. An `ast` sweep over all 991 tracked `.py` files at `9d1788fe` finds NO production caller of `run_agent_loop` anywhere: its only readers are `tests/test_agent_loop_execution.py`, which exists solely to drive it, and one test in `tests/storage/test_persistence.py`. `docs/system/architecture.md` had already recorded that state in its own prose — "which no production caller reaches; DECISION F272 D13 assigns that function to T004's classic-runner deletion" — and all six of its cycle events are already tabled there as "no live emitter". So nothing user-observable is lost, no finding is owed under amend0908 rule 4, and the open set stays at 87.

THE NEIGHBOURHOOD OF THAT DELETION WAS SWEPT RATHER THAN EYEBALLED, because an anchor that leaves its helpers behind is the R-0855 shape. Of the module's 15 module-level definitions, 11 SURVIVE — `AgentRole`, `AgentAdapterSpec`, `AgentLoopStage`, `AgentLoopDecision`, `AgentLoopState`, `default_agent_loop_state`, `derive_agent_loop_state`, `summarize_agent_loop_state`, `_find_current_blocker`, `_format_blocker` and `_next_action` — because `apps/cli/commands/brain.py` reads `derive_agent_loop_state` and `summarize_agent_loop_state` for the live `dev agent-loop` command, and the rest are reachable from those two or from `tests/test_agent_loop.py`. Exactly TWO become readerless once the anchors go and are deleted in the SAME commit: `_auto_approve_low_risk_intents` and `_loop_meta`, each of whose only in-file caller is `run_agent_loop`. The first sweep the reviewer ran got this wrong and is recorded so the method is not repeated: it asked "is this definition reachable from the removed pair", which marks a helper of a SURVIVING function as an orphan whenever the removed pair also calls that survivor, and it labelled `_find_current_blocker` an orphan although `derive_agent_loop_state` calls it. The correct question is the reverse one — close the survivor set forward from the definitions a surviving FILE reads, then subtract it from the anchors' reach.

THE EVENT SCHEMAS STAY, and this is the one part of the ruling that is a judgement rather than a measurement. `agent_loop_started`, `agent_loop_cycle_started` and `agent_loop_completed` keep their entries in `packages/orchestration/event_schemas.py` and their pins in `tests/orchestration/test_event_ledger.py`, because run logs already written on disk carry those events and the ledger validates what it READS rather than only what it writes. The repository's own precedent is on disk and was measured, not recalled: `docs/system/architecture.md` already tables `agent_loop_decision`, `agent_loop_cycle_completed` and `agent_loop_paused` as "no live emitter", so a registered schema with no live emitter is an accepted state here and not a defect this round introduces.

ONE TEST DIES WITH ITS VEHICLE AND LOSES NO COVERAGE, which was checked before it was ordered rather than after. `tests/storage/test_persistence.py::test_token_policy_applied_event_schema` calls `run_agent_loop(job, max_cycles=1)` purely to make a `token_policy_applied` event appear, then asserts that event's metadata keyset. `packages/orchestration/autonomy_loop.py` emits the SAME event from `_emit_token_policy_applied` at loop start, and the very next test in that same file already asserts it through that emitter. The property therefore keeps a test after the deletion, through the surviving emitter, and no assertion is weakened to make a deletion green.

ALTERNATIVES CONSIDERED. (a) DELETE BOTH HANDLERS OUTRIGHT and register the lost bounded-cycles run as a finding — rejected on the third measurement above: it leaves `job.resume`, a command no deletion list names and whose whole purpose is resuming a bounded run, a no-op under the shipped default. (b) GIVE THE SINGLE PASS TO `do.continue` OR `worker.run --once` — rejected on what those commands actually do: `do.continue` runs one continuation cycle for an APPROVED INTENT and `worker.run` processes jobs off the local queue, and neither runs a job's next PENDING task through `task_runner.run_next_task`, which is what `job.run-next` means. (c) GIVE IT TO `mission.run` — rejected because that command drives the F070 orchestrator loop over a MISSION, a different record entirely. (d) KEEP `run_agent_loop` until the command deletion lands, so the whole classic runner dies in one commit — rejected because it is separable by measurement rather than by preference, it has no production caller, and F275's one declared-oversize allowance is reserved by DECISION F275 D17 for the flip.

HOW TO REVERSE. Delete this paragraph and the six above it. The absorption in the CHOSEN clause binds the round that deletes the command surface and nothing earlier; this round's own change set is the `run_agent_loop` half alone, which reverses by `git revert` of its single commit.
DECISION32

## SPEC-DELETE → the C4 production change

The worker writes this code; it is DESCRIBED here, not sliced, because it is
production code and §3 forbids the reviewer to author it. Four files move.

(a) `packages/orchestration/agent_loop.py` — DELETE exactly four module-level
    definitions and nothing else: `run_agent_loop`, `_run_next_task_step`,
    `_auto_approve_low_risk_intents` and `_loop_meta`. The other ELEVEN
    module-level definitions stay untouched, byte for byte. Delete also the
    module docstring's description of the execution loop and its five emitted
    event names, and any import that only those four functions used — `ruff` is
    the check that catches a missed one, and it is ordered in G6 for exactly
    that reason.

(b) `tests/test_agent_loop_execution.py` — DELETE the whole file with `git rm`.
    Its every test drives `run_agent_loop`.

(c) `tests/storage/test_persistence.py` — DELETE only the method
    `test_token_policy_applied_event_schema` and nothing else. The test
    immediately after it, which asserts the same event through the autonomy
    loop's emitter, STAYS and is not edited.

(d) `docs/system/architecture.md` — apply the four pairs D1 to D4 below.

## PAIRS D1 to D4 → `docs/system/architecture.md`

<<<D1-FROM
**Purpose:** State derivation (read-only, deterministic) plus a local execution loop
(`run_agent_loop`) that drives plan → build → approve → test → repeat cycles.
External tools (Claude Code, Copilot CLI) are not called — execution delegates to
existing CLI command handlers (task runner, test runner).
D1-FROM

<<<D1-TO
**Purpose:** State derivation only — read-only, deterministic and inspect-only.
The local execution loop that once drove plan → build → approve → test → repeat
cycles was DELETED at F275 round 32 together with the classic-runner handler it
delegated to, per DECISION F275 D18; it had no production caller. Nothing in
this module executes a task, and `remedy dev agent-loop` reads derived state.
D1-TO

<<<D2-FROM
derive_agent_loop_state(job, events, *, max_cycles=3) -> AgentLoopState
run_agent_loop(job, *, max_cycles=3, auto_approve_low_risk=False, run_tests=True) -> AgentLoopState
D2-FROM

<<<D2-TO
derive_agent_loop_state(job, events, *, max_cycles=3) -> AgentLoopState
D2-TO

<<<D3-FROM
The six cycle events below keep their schemas in
`packages/orchestration/event_schemas.py` and are still emitted by
`agent_loop.run_agent_loop()`, which no production caller reaches; DECISION F272
D13 assigns that function to T004's classic-runner deletion.
D3-FROM

<<<D3-TO
The six cycle events below keep their schemas in
`packages/orchestration/event_schemas.py` and now have no emitter at all: the
function that emitted them was DELETED at F275 round 32, per DECISION F275 D18.
The schemas are kept deliberately, because run logs already written on disk
carry those events and the ledger validates what it READS, not only what it
writes.
D3-TO

<<<D4-FROM
All `agent_loop_*` events emitted by `run_agent_loop()` use the same metadata schema:
D4-FROM

<<<D4-TO
All `agent_loop_*` execution events already recorded in run logs on disk carry
the same metadata schema:
D4-TO

## Done when — GATES G1 to G8

Run every gate as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and record the REAL
exit code and the REAL numbers. "Green" as a word is a finding. G1 to G4 and G6
to G8 are ordered at commits STRICTLY EARLIER than C5, which writes the
handback, per §3 item 31; C5's own insertion count is not gated and is not
reported as a gate reading.

**G1 TRANSPORT (at C0b).** The reviewer's scratch original is the file this
block was read from, `.remedy-wt/f275-r32-block.md`, written and hashed BEFORE
delegation. Report its sha256 and byte length, and show that the committed
`.agent/authored/f275-r32.md` and the committed `.agent/last_block.md` are
BYTE-EQUAL to it. `.agent/last_block.md` is written by `git cat-file blob` from
the committed C0a blob, never by a retype. State what the chain covers: three
artefacts, and not any bytes emitted into a prompt (§3 item 37).

**G2 THE PLAN (at C1).** Committed `.agent/plan.md` byte-equal to the PLAN32
slice. Report both byte lengths, the sha256, the line count against the cap of
50, and the counts of `^## Goal$` and `^## Next Steps$`, each of which must
read exactly 1.

**G3 THE RECORD, three append targets (at C3).** For `.agent/live_review.md`,
`.agent/prose_slips.md` and `.agent/decisions.md`: report the pre-size, confirm
it equals constraint 4's figure, and show post == pre + ONE newline + slice.
Read the joining byte BACK at offset len(pre) and report it. Then the
independent structural reader: count N from each slice yourself — do not take N
from this block — and match the last N blank-line units of the whole file
against the slice's N paragraphs IN ORDER. Three negative controls, each
flipping one byte INSIDE THE FIRST appended paragraph, must be REJECTED by BOTH
readers. Finally `^Gate: F275 R31 ` must read exactly 1 and
`^## DECISION F275 D18 ` exactly 1.

**G4 THE OPEN SET (at C3).** BY DISTINCT ID, from `.agent/live_review.md`
mechanically: every `^- R-\d+ — ` id minus every `^Done: R-\d+ — ` id. Report
the count at the base `9d1788fe` and at C3; both must read 87. Report the ids
registered this round and the ids resolved this round; both lists must be
EMPTY. Report the constraint 10 reading for `.agent/prose_slips.md`: whether
either SLIPS32 line was already present at the base.

**G5 THE SURVIVORS KEEP THEIR READERS (at C4).** In the primary checkout,
report the module-level definition names of `packages/orchestration/agent_loop.py`
before and after C4, as two sorted lists, and the set difference. The removed
set must be exactly `_auto_approve_low_risk_intents`, `_loop_meta`,
`_run_next_task_step`, `run_agent_loop`; the surviving list must hold 11 names.
Then a repo-wide sweep over `apps packages tests scripts docs` for each of
those four names: each must read ZERO occurrences after C4. Report the counts
BEFORE as well — an absence proves nothing without the presence beside it.

**G6 THE SURVIVING PATH STILL HAS TEETH — RED PROOF (at C4).** In a disposable
worktree at C4, with `node_modules` linked and `__pycache__` purged, run
`python3 -B -m pytest tests/test_agent_loop.py tests/orchestration/test_event_ledger.py tests/storage/test_persistence.py -q`
UNMUTATED FIRST and report its exit code and pass count as the control. Then
THREE mutations, each reverted byte-exactly before the next, each reported with
WHICH assertion fired and not merely with an exit code:
  M1 — in `derive_agent_loop_state`, replace the single line
       `blocked_reason = _find_current_blocker(job, events)` with
       `blocked_reason = None`, preserving its indentation. That line occurs
       exactly ONCE in `packages/orchestration/agent_loop.py`, which the
       reviewer counted at `9d1788fe`; the file is the revert target and the
       byte string is unique inside it. Expect RED in `tests/test_agent_loop.py`.
  M2 — remove the `agent_loop_started` entry from `EVENT_METADATA_SCHEMAS` in
       `packages/orchestration/event_schemas.py`. Expect RED in
       `tests/orchestration/test_event_ledger.py`, which proves the schemas
       DECISION32 keeps are still pinned after their emitter is gone.
  M3 — in `packages/orchestration/autonomy_loop.py`, make
       `_emit_token_policy_applied` return without emitting. Expect RED in
       `tests/storage/test_persistence.py`, which proves the coverage
       DECISION32 says survives the deleted test really does.
Also run `ruff check packages/orchestration/agent_loop.py tests/storage/test_persistence.py`
and report its exact output line; it is the only check that catches a name left
behind by an incomplete deletion.
THE REVIEWER RAN THIS WHOLE GATE ITSELF at `9d1788fe` before delegating, in its
own disposable worktree, and all three mutations bite with a NAMED assertion:
control `102 passed` at exit 0; M1 fires
`assert state.decision == AgentLoopDecision.BLOCKED`; M2 fires
`assert "agent_loop_started" in EVENT_METADATA_SCHEMAS`; M3 fires
`assert len(tpa) >= 1, "must emit token_policy_applied"`. Each revert was
verified byte-exact by sha256. Report YOUR readings, not these.

**G7 THE PAIRS AND THE SUITE (at C4).** Each of D1 to D4: FROM count in
`docs/system/architecture.md` BEFORE the edit exactly 1, AFTER exactly 0. For
D1, D3 and D4 the TO must go 0 to 1. For D2, per constraint 9, report instead:
the `run_agent_loop(job, *, max_cycles=3` signature 1 to 0, and the line
`derive_agent_loop_state(job, events, *, max_cycles=3) -> AgentLoopState`
unchanged at exactly 1 before and after. Then, SERIALLY in the primary checkout,
`python3 -B -m pytest tests/ -q` and report the full summary line and the exit
code. The reviewer measured the collection delta itself at `9d1788fe`, by
`--collect-only` before and after applying this change in a disposable
worktree: 18373 tests collected BEFORE and 18362 AFTER, a difference of exactly
ELEVEN, being the TEN tests in `tests/test_agent_loop_execution.py` and the ONE
method C4 removes from `tests/storage/test_persistence.py`. Reproduce that
delta the same way — `--collect-only` at the base and at C4 — and print the
removed node ids, rather than asserting the number. Round 31 read 18350 passed
and 23 skipped over 18373 collected at its own base.
Then the canary, `python3 -m pytest tests/cli/test_golden_path.py -q`, and
`python3 -m pytest tests/docs/ -q`, which this round owes because its change set
holds a `docs/` path.

**G8 NOTHING ELSE MOVED (at C4).** `.agent/STOP` read from disk and ABSENT.
`git status --porcelain` EMPTY. `git worktree list` exactly ONE entry. Branch
`feature/f275-one-world-completion-part-three`. `git diff --name-only 9d1788fe..<C4>`
an EXACT SET MATCH against the path list in the header's `Change:` line, which
does not include `.agent/handoff.md`, reported as MISSING and EXTRA, both of
which must be empty. Per-commit
insertions for every commit before the handback, each under the DECISION F104
D1 cap of 500. Report the shipped catalog's command count, group count and its
count of dangling `related=` references resolved on the DOTTED id: 222, 44 and
ZERO, unchanged, because this round deletes no command. Take that reading by
IMPORTING `apps.cli.command_catalog` in `python3`, never by invoking the
`remedy` binary, which is denied in this environment; resolve `related=` on the
dotted id, because round 28's worker split on whitespace and reported a false
alarm on every reference.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries the
SESSION NUMBER 16 of feature F275, round 32, ONE LINE PER GATE with real exit
codes and real numbers, the changed-files table with the `+/-` column taken from
`git diff --numstat` and not from file line counts (§3 item 28), the
item-status table, the open-findings count, and the one-sentence context
self-assessment amend0905-throughput requires. Declare every deviation; a
deviation honestly declared costs this round nothing, and a slice quietly
reconciled costs it the verdict.
