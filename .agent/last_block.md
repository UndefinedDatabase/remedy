── STEP T003 (2 of n) — F275 ─────────────────────────────────
Goal:        Register and repair R-0874, then retire the `job.run-next` command
             surface: its catalog entry, its dispatch line, the two `related=`
             tuples it would leave dangling, and every advertisement of it,
             which move to `job resume` under DECISION F275 D18.
Bundle:      C0a save this block · C0b mirror it · C1 the plan · C2 the round 32
             verdict, the R-0874 registration and three prose slips · C3 the
             R-0874 repair · C4 the command-surface retirement · C5 the handback.
Change:      exactly the paths listed here and nothing else —
             `.agent/authored/f275-r33.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/prose_slips.md`, `docs/system/architecture.md`,
             `apps/cli/command_catalog.py`, `apps/cli/commands/job.py`,
             `packages/orchestration/agent_loop.py`,
             `packages/orchestration/autonomy_loop.py`,
             `packages/orchestration/brain_detail.py`,
             `packages/orchestration/cockpit.py`,
             `packages/orchestration/dashboard.py`,
             `packages/orchestration/long_run_executor.py`,
             `packages/orchestration/timeline.py`,
             `packages/orchestration/trust_report.py`,
             `scripts/remedy_smoke.sh`,
             `tests/cli/test_plan_approval.py`,
             `tests/orchestration/test_long_run_executor.py`,
             `tests/test_agent_loop.py`, `tests/test_cockpit.py`,
             `tests/test_command_catalog.py`,
             `tests/test_remedy_smoke_script.py`, `tests/test_timeline.py`,
             `tests/test_trust_report.py`, plus `.agent/handoff.md` at C5.
Constraints: the numbered list below.
Done when:   gates G1 to G8 below are RUN and their real exit codes recorded.
Handback:    completion report + rewrite `.agent/handoff.md`.
──────────────────────────────────────────────────────────────

## Base

This round's base is `7d14e89f`, the tip of
`feature/f275-one-world-completion-part-three` at authoring time. Every reading
this block states was taken by the reviewer at that commit. THE WHOLE C4 CHANGE
WAS APPLIED AND RUN by the reviewer in a disposable worktree at that base before
this block was written; the numerals below are that run's, not estimates.

## Constraints

1. APPLY EVERY SLICE BYTE FOR BYTE. Never reflow, retype, trim or repair a
   slice. If a slice does not fit its target, DECLARE it and apply the rest.
2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, exactly. C1 is the first
   substantive commit, per §3 item 23, because this round touches the ledger.
3. THE CHANGE SET IS THE PATH LIST IN THE HEADER'S `Change:` LINE, together with
   `.agent/handoff.md`, which that line names separately as C5's own target.
4. EVERY APPEND IS `pre + ONE newline + slice`. At the base
   `.agent/live_review.md` is 799726 bytes and `.agent/prose_slips.md` is 219069
   bytes, each ending in a single `\n`. This round appends to those two only;
   `.agent/decisions.md` is NOT in the change set and is not touched.
5. NO PRODUCTION LINE MOVES BEFORE C3. C1 and C2 write only under `.agent/`.
6. DESTRUCTIVE VERIFICATION IS ISOLATED, inside a disposable `git worktree`
   under `.remedy-wt/`, never in the primary checkout (self_drive_protocol.md
   G5). Remove and prune it before the handback.
7. THE SUITE RUNS SERIALLY, `python3 -B -m pytest`, never `-n auto`, and only
   AFTER C4 is committed. Round 32 measured why: a tracked test file that is
   `git rm`-ed but not yet committed fails
   `tests/orchestration/test_evidence_index.py::TestPorcelainParsing::test_every_enumerated_path_exists_in_this_repo`,
   which enumerates the DIRTY set and asserts each path exists. This round
   deletes no file, but it edits many, and the rule stands: commit, then run.
   Link `apps/ui/node_modules` into any fresh worktree before a run that
   collects `tests/orchestration/test_test_runner.py`.
8. THIS ROUND REGISTERS EXACTLY ONE FINDING, R-0874, AND RESOLVES EXACTLY ONE,
   R-0874. The open set is 87 by distinct id at the base, becomes 88 at C2 when
   R-0874 is registered, and returns to 87 at C3 when the repair lands and the
   authored `Done:` paragraph is applied. Report all three readings. R-0874 is
   the next free id, which the reviewer confirmed at the base: the highest
   registered id is R-0873.
9. THE `Done:` PARAGRAPH IN THIS BLOCK IS REVIEWER-AUTHORED TEXT and is applied
   as written at C3, per §4 item 4. Do not write a `Done:` paragraph of your
   own for any other finding, and do not write a `Landed:` line for R-0874 —
   its resolution text is already authored here and lands in the same round.
10. PAIR SHAPES, from the containment test the reviewer ran at `7d14e89f`, one
    reading per pair: A1 `TO contains FROM: false` → REWRITE. A2
    `TO contains FROM: false` → REWRITE. Both carry the §4.9 FROM-0x / TO-1x
    obligation.
11. THE CATALOG COUNT FALLS BY ONE, FROM 222 TO 221, AND THE GROUP COUNT DOES
    NOT MOVE. The reviewer checked at the base that no test pins the literal
    222 for the catalog: a sweep of `tests/` for that numeral returns one hit,
    `tests/orchestration/test_run_report.py:730`, which is a job id inside a
    `remedy decision resolve` example and not a count. Report the count anyway.

## SLICE PLAN33 → whole-file replacement of `.agent/plan.md`

<<<PLAN33
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE.

## Current Step

ROUND 33 continues T003. It registers and repairs R-0874, the two sentences in
`docs/system/architecture.md` that still describe the execution loop round 32 deleted. It
then retires the `job.run-next` command surface: the catalog entry, the dispatch line, the
two `related=` tuples that would otherwise dangle, and all 29 advertisements of it across
eight orchestration modules, the smoke script and seven test files, which move to
`job resume` under DECISION F275 D18. The handler `_cmd_run_next_task_local` SURVIVES as an
internal function; only its command door closes.

## Next Steps

1. Retire the `job.run` command surface and absorb both handlers under the `job.resume`
   door, one owner and no copy, registering the `--unattended` and `--yes` surfaces
   DECISION F275 D18 names as genuinely lost.
2. The flip DECISION F275 D17 sized, as the one declared-oversize commit AGENTS.md permits
   per feature, re-deriving the site set at its own base.
3. The resolver collapse DECISION F260 D5 places in T003, and the classic store.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- A command deletion is invisible to a text sweep wherever the CLI is invoked as an argv
  LIST, because the group and the subcommand are separate elements. Round 33 found two such
  sites this way and no other instrument would have. Step 1 above re-runs that sweep.
- The open set is 87 by distinct id at this round's base `7d14e89f`. This round registers
  R-0874 and resolves it in the same round, so it returns to 87. Four are High — R-0803,
  R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
PLAN33

## SLICE RECORD33 → append to `.agent/live_review.md`

<<<RECORD33
Gate: F275 R32 — the F275 round 32 entry. VERDICT PASS, written by the planner and reviewer of session 16 after reading the committed range `9d1788fe`..`7d14e89f` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line of it. Seven single-parent commits C0a `9f3d7e13`, C0b `c56ed2bd`, C1 `ff66bce3`, C2 `2e590822`, C3 `4b06c1cc`, C4 `2680303d` and C5 `7d14e89f`, per-commit insertions 375, 348, 19, 6, 24 and 19 for the six before the handback, every one far under the AGENTS.md DECISION F104 D1 cap of 500. G1 IS A REAL TRANSPORT CHAIN AND NOT MERELY A SELF-CONSISTENT ONE: the reviewer's scratch original at `.remedy-wt/f275-r32-block.md` was written AND HASHED BEFORE delegation at `7c2e55d4fa679dd8ea4219bbd55d6ef097b24de0a193a623a697d22f20d0e0a6`, and the committed `.agent/authored/f275-r32.md` and `.agent/last_block.md` are both 37081 bytes at that same digest — one shared git blob — so the first link predates the worker; the chain covers those three artefacts and claims nothing about bytes emitted into a prompt, per §3 item 37. G2: `.agent/plan.md` byte-identical to PLAN32 at 2330 bytes, 42 lines against the cap of 50, both mandated headings exactly once. G3 over all three append targets — `.agent/live_review.md` 793191, `.agent/prose_slips.md` 217298 and `.agent/decisions.md` 1024587 bytes before — each post-blob equal to its pre-blob then ONE newline then the slice as extracted, the joining byte READ BACK at offset len(pre) and reading a newline in all three, and the structural reader counting N from each slice — 1, 2 and 12 paragraphs — and matching the last N blank-line units IN ORDER, with all three negative controls flipped INSIDE THE FIRST appended paragraph and REJECTED. `^Gate: F275 R31 ` and `^## DECISION F275 D18 ` each exactly 1. G4: THE OPEN SET IS 87 BY DISTINCT ID at the base, at C3 and at C4, over 102 registrations against 15 resolutions; this round registered none and resolved none. G5: the module-level definitions of `packages/orchestration/agent_loop.py` fall from 15 to 11, the REMOVED set is exactly `_auto_approve_low_risk_intents`, `_loop_meta`, `_run_next_task_step` and `run_agent_loop`, and the ADDED set is EMPTY — re-derived by the reviewer with `ast` against both committed blobs rather than from the diff. G6 was re-run by the reviewer in its own disposable worktree BEFORE delegation and all three mutations bite with a NAMED assertion: control 102 passed at exit 0; M1 fires `assert state.decision == AgentLoopDecision.BLOCKED`; M2 fires `assert "agent_loop_started" in EVENT_METADATA_SCHEMAS`, which proves the schemas DECISION F275 D18 deliberately keeps are still pinned after their emitter is gone; M3 fires `assert len(tpa) >= 1, "must emit token_policy_applied"`, which proves the coverage that decision says survives the deleted test really does. Every revert was verified byte-exact by sha256. G7: all four pairs applied exactly — D1, D3 and D4 FROM 1 to 0 and TO 0 to 1, and D2 FROM 1 to 0 with its TO reading 1 both before and after, which constraint 9 of that block declared in advance because D2's TO is a strict PREFIX of its FROM and a "TO 0 to 1" count would have been unsatisfiable by every possible round. THE SUITE ARITHMETIC CLOSES AGAINST THE REVIEWER'S OWN INSTRUMENT: `--collect-only` reads 18373 at the base and 18362 at the tip, a difference of exactly ELEVEN, being the ten tests of the deleted `tests/test_agent_loop_execution.py` and the one method removed from `tests/storage/test_persistence.py`, and the worker's full serial suite reads 18339 passed and 23 skipped, which sums to 18362 exactly. The reviewer re-ran the canary and the affected guards itself at 177 passed, `tests/docs/` at 306 passed and `ruff` at `All checks passed!`. G8: porcelain EMPTY, ONE worktree, `.agent/STOP` absent, and `9d1788fe..2680303d` an EXACT set match over the ten change-set paths with MISSING and EXTRA both empty. THE WORKER FOUND WHAT THE BLOCK'S OWN GATE COULD NOT AND THE REVIEWER SUSTAINS EVERY DECLARATION. G5's zero-gate was UNMEETABLE AS ORDERED and this is the reviewer's error, not the worker's: the sweep corpus included `docs`, and `docs/roadmap/features/T2_F272.md` carries four prose occurrences of `run_agent_loop` and `_run_next_task_step` at lines 707, 708 and 713 — a closed feature's plan record, which F275's own file says is kept unedited on purpose and which the worker was right to leave alone. The reviewer re-measured the sweep at `2680303d` excluding `docs/roadmap/`: all four names read ZERO. A deletion sweep over a repository that keeps its own planning history must exclude that history, or it asserts an absence the record is designed to contradict. THE ONE DEFECT WITH PRODUCT EFFECT IS REGISTERED AS R-0874 BY THIS ROUND'S C2 AND REPAIRED BY ITS C3: two sentences in `docs/system/architecture.md` still describe the deleted loop and no pair in that block reached them. NO OTHER FINDING IS REGISTERED AND NONE IS RESOLVED BY THIS GATE.

- R-0874 — MEDIUM. `docs/system/architecture.md` describes an execution loop that F275 round 32 deleted, at two sites the four authored pairs of that round did not reach, and one of them contradicts the replacement text four lines below it. Measured by the reviewer at `7d14e89f`. SITE ONE, lines 836 and 837, the opening sentence of the `### Agent Loop Contract v1 (Step 22)` section: "`packages/orchestration/agent_loop.py` defines the orchestration contract, data models, and local execution loop for coordinating agent workflows." That module no longer defines an execution loop, and the `**Purpose:**` paragraph immediately beneath it now reads "Nothing in this module executes a task" — so the page asserts and denies the same fact within four lines. SITE TWO, line 974: "The `agent_loop_task_exit` event has been removed — `SystemExit` from task runners is silently caught." That catch was the `except SystemExit: pass` inside `run_agent_loop`, deleted with it, so the sentence describes a behaviour that no longer exists anywhere. WHY THIS IS AN ID AND NOT A PROSE SLIP, per operator amendment amend0827-process-diet rule 2: this is wrong state on disk under `docs/`, not an inaccuracy in the reviewer's own block text. WHY THE BLOCK MISSED IT, recorded because the class recurs: the round 32 block chose its four pairs by grepping for the SYMBOL `run_agent_loop`, and neither of these sentences names it — the first says "execution loop" in prose and the second names an event and a Python exception. A deletion's documentation sweep must read the page for the CAPABILITY that died, not only for the identifier, which is the R-0855 neighbourhood rule reaching prose. FIX CLAUSE, binding on the block that resolves this: both sites are repaired in ONE commit by authored FROM/TO pairs, and the same commit re-reads the whole `### Agent Loop Contract v1` section for any third sentence describing execution rather than derivation.
RECORD33

## SLICE DONE33 → append to `.agent/live_review.md`, at C3, AFTER the C2 append

<<<DONE33
Done: R-0874 — RESOLVED at F275 round 33 by that round's C3, which is the commit this block's constraint 2 fixes as the repair commit; the reading is the reviewer's own, taken by APPLYING both pairs in a disposable worktree at `7d14e89f` before the round was delegated. Both sites named in the registration are repaired by authored pairs A1 and A2 in ONE commit, as the fix clause requires. A1 rewrites the section's opening sentence so that it describes what the module defines TODAY — the orchestration contract, the data models and the state derivation — and it no longer contradicts the `**Purpose:**` paragraph four lines beneath it. A2 rewrites the `SystemExit` sentence so that it records the removal of `agent_loop_task_exit` as history and does not assert a live catching behaviour, because the function that caught was deleted at round 32. THE FIX CLAUSE'S SECOND HALF WAS PERFORMED AND IT FOUND NOTHING FURTHER: the reviewer re-read the whole `### Agent Loop Contract v1 (Step 22)` section at `7d14e89f`, from its heading to the `**Authority:**` paragraph that closes it, for any third sentence describing EXECUTION rather than DERIVATION, and the remaining execution-flavoured text is the run-log event table, every row of which already reads "no live emitter" and is therefore correct rather than stale. WHAT THIS RESOLUTION DOES NOT CLAIM: the repair reaches the two sites measured plus that one section, and it is not a guard. No test in this repository asserts that a page's prose matches a deleted capability, and `tests/docs/test_named_source_paths.py` — the nearest thing — resolves PATHS, not descriptions, so a page that describes a dead mechanism while naming a live file stays invisible to it exactly as this one did. That residue is left deliberately unguarded rather than covered by a gate that could not honestly hold it, which is the same boundary DECISION F275 D16 drew for R-0873.
DONE33

## SLICE SLIPS33 → append to `.agent/prose_slips.md`

<<<SLIPS33
2026-09-10 · F275 R32 · The round 32 block ordered a zero-gate sweeping `apps packages tests scripts docs` for the four deleted `agent_loop` names, and it could not pass: `docs/roadmap/features/T2_F272.md` carries four prose occurrences at lines 707, 708 and 713, and that file is a CLOSED feature's plan record which F275's own feature file says is kept unedited on purpose. The worker declared the red rather than editing the roadmap, which is correct on both counts. A deletion sweep over a repository that keeps its own planning history must exclude `docs/roadmap/`, because a zero-gate over a record designed to remember what was deleted asserts an absence that record exists to contradict.

2026-09-10 · F275 R32 · The round 32 block's SPEC-DELETE said the module docstring listed "five emitted event names" where it listed six, and DECISION F275 D18's reversal clause said "delete this paragraph and the six above it" over a slice of twelve paragraphs, eleven of which precede the closer. Both are hand-counted numerals about text the block was itself shipping, which §3 item 11 forbids for exactly this reason, and the worker applied both byte for byte and declared them rather than reconciling. Neither is load-bearing: the docstring cut was complete regardless of the adjective, and a reversal instruction that names one paragraph too few still points at the right decision. Count the parts of a slice mechanically, or name them instead of counting them.

2026-09-10 · F275 R32 · A command deletion is INVISIBLE to every text sweep wherever the CLI is invoked as an argv LIST, because the group and the subcommand are separate elements: `subprocess.run([*_CLI, "job", "run-next", short_id])` contains neither `remedy job run-next` nor `job run-next` as a substring. The reviewer found two such sites in `tests/cli/test_plan_approval.py` only by APPLYING the round 33 change in a worktree and running the full suite, which went red at 2 failed; an `ast` sweep for the adjacent string pair then located both mechanically and confirmed there were no others. A round that retires a command surface sweeps the argv-list form with `ast` as well as the spaced form with text, and the second instrument is the one that finds the callers a grep cannot see.
SLIPS33

## PAIRS A1 and A2 → `docs/system/architecture.md`, at C3

<<<A1-FROM
`packages/orchestration/agent_loop.py` defines the orchestration contract, data models,
and local execution loop for coordinating agent workflows.
A1-FROM

<<<A1-TO
`packages/orchestration/agent_loop.py` defines the orchestration contract, the
data models and the state derivation for coordinating agent workflows. It
defines no execution loop: that loop was deleted at F275 round 32, per
DECISION F275 D18.
A1-TO

<<<A2-FROM
`outcome` is at the top-level RunEvent field, not in metadata.  The `agent_loop_task_exit` event has been removed — `SystemExit` from task runners is silently caught.
A2-FROM

<<<A2-TO
`outcome` is at the top-level RunEvent field, not in metadata.  The `agent_loop_task_exit` event was removed while the execution loop still existed, and that loop caught `SystemExit` from task runners rather than propagating it. Both are history: the loop itself was deleted at F275 round 32, so nothing in this module catches `SystemExit` today.
A2-TO

## SPEC-RETIRE → the C4 production change

The worker writes this change; it is DESCRIBED here because it is production
code. It is a UNIFORM byte-string migration plus four structural edits. The
reviewer applied all of it at `7d14e89f` and ran the full suite over it, so the
counts below are measured.

(a) THE ADVERTISEMENTS, IN THIS ORDER, over tracked files under `apps/`,
    `packages/`, `tests/` and `scripts/` — and NOT under `docs/`, which this
    round does not touch beyond C3, and NOT under `.agent/`:
      FIRST replace the byte string `remedy job run-next` with
      `remedy job resume`. The reviewer measured 21 such lines in 11 files.
      THEN replace any REMAINING `job run-next` with `job resume`. The reviewer
      measured 8 such lines in 6 files after the first pass.
    The order matters: running the bare form first would double-handle every
    prefixed site. After both passes the token `job run-next` reads ZERO over
    those four trees.

(b) THE ARGV-LIST INVOCATIONS, which no text sweep in (a) can reach. In
    `tests/cli/test_plan_approval.py`, the list literal
    `[*_CLI, "job", "run-next", short_id],` occurs exactly TWICE — the reviewer
    counted it at the base and located both with an `ast` sweep for the adjacent
    string pair. Replace both with `[*_CLI, "job", "resume", short_id],`. The
    surrounding assertions are NOT edited: `job resume` reaches the same
    plan-approval gate and exits 3 with the same two stderr strings, which the
    reviewer verified by running that file green at 27 passed after the change.

(c) THE CATALOG, `apps/cli/command_catalog.py`. DELETE the whole `CommandEntry(`
    block whose `command_id="job.run-next"` — it is ten lines and it is the only
    entry with that id. Then repair the two `related=` tuples that would
    otherwise dangle:
      `related=("job.run-next", "job.plan", "decision.list"),`  (on `job.run`)
        becomes  `related=("job.plan", "decision.list"),`
      `related=("job.create", "job.run-next"),`  (on `job.plan`)
        becomes  `related=("job.create", "job.resume"),`
    `job.resume` is chosen over `job.run` deliberately: `job.run` is retired by
    the NEXT round, and pointing at it would buy a second edit of the same line.

(d) THE DISPATCH, `apps/cli/commands/job.py`. DELETE the single line
    `    "job.run-next": lambda args: _cmd_run_next_task_local(args.job_id),`.
    `_cmd_run_next_task_local` ITSELF SURVIVES and is not touched: it is still
    called by `_cmd_job_run_cycles` whenever the resolved cycle count is one,
    which is the shipped default, and that is the path `job.resume` reaches.
    Deleting the function here would make `job.resume` a no-op, which is exactly
    what DECISION F275 D18 rules against.

(e) THE CATALOG TEST'S ID PIN, `tests/test_command_catalog.py`. The line
    `        "job.permissions", "job.run-next",` becomes
    `        "job.permissions",`.

## Done when — GATES G1 to G8

Run every gate as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and record the REAL
exit code and the REAL numbers. "Green" as a word is a finding. Every gate is
ordered at a commit STRICTLY EARLIER than C5, per §3 item 31.

**G1 TRANSPORT (at C0b).** The reviewer's scratch original is the file this
block was read from, `.remedy-wt/f275-r33-block.md`, written and hashed BEFORE
delegation. Report its sha256 and byte length and show the committed
`.agent/authored/f275-r33.md` and `.agent/last_block.md` BYTE-EQUAL to it.
`.agent/last_block.md` is written by `git cat-file blob` from the committed C0a
blob, never by a retype. State what the chain covers: three on-disk artefacts,
and not any bytes emitted into a prompt.

**G2 THE PLAN (at C1).** Committed `.agent/plan.md` byte-equal to PLAN33.
Report both byte lengths, the sha256, the line count against the cap of 50, and
`^## Goal$` and `^## Next Steps$` each exactly 1.

**G3 THE RECORD (at C2 and C3).** `.agent/live_review.md` takes TWO appends this
round, in different commits: RECORD33 at C2 and DONE33 at C3. For each, and for
SLIPS33 at C2, report the pre-size, show post == pre + ONE newline + slice, and
read the joining byte BACK at offset len(pre). Then the independent structural
reader: count N from each slice yourself, never from this block, and match the
last N blank-line units against the slice's N paragraphs IN ORDER. One negative
control per append, flipping a byte INSIDE THE FIRST appended paragraph, must be
REJECTED by BOTH readers. Confirm `.agent/live_review.md` is 799726 bytes and
`.agent/prose_slips.md` 219069 bytes at the base. Finally `^Gate: F275 R32 `,
`^- R-0874 — ` and `^Done: R-0874 — ` each exactly 1 at C3.

**G4 THE OPEN SET (at three commits).** BY DISTINCT ID, from
`.agent/live_review.md` mechanically: every `^- R-\d+ — ` id minus every
`^Done: R-\d+ — ` id. Report the count at the base `7d14e89f`, at C2 and at C3.
Expected 87, then 88, then 87. Report the ids registered and resolved this
round; each list must hold exactly `R-0874`.

**G5 THE REPAIR (at C3).** Pairs A1 and A2: FROM count in
`docs/system/architecture.md` exactly 1 before and 0 after; TO exactly 0 before
and 1 after. Then report, for the whole `### Agent Loop Contract v1 (Step 22)`
section, the count of the phrase `execution loop` before and after C3, and print
every line that still holds it, so the fix clause's second half is evidenced
rather than asserted.

**G6 THE SURFACE IS GONE AND NOTHING ELSE WENT WITH IT (at C4).** Over tracked
files under `apps/ packages/ tests/ scripts/`, report the count of `job run-next`
and of `job.run-next` BEFORE and AFTER C4 — the before readings are the evidence
the after readings need. Both must be ZERO after. Separately, and this is the
gate that matters, prove the HANDLER SURVIVED: report that
`_cmd_run_next_task_local` is still defined in `apps/cli/commands/job.py` and
still called by `_cmd_job_run_cycles`, by parsing that file with `ast` and
printing the caller's name — not by grep. Then import
`apps.cli.command_catalog` in `python3`, never the `remedy` binary, which is
denied here, and report the command count, the group count and the number of
dangling `related=` references resolved on the DOTTED id: expected 221, 44 and
ZERO.

**G7 THE ARGV SWEEP AND THE SUITE (at C4).** Re-run the `ast` sweep for the
adjacent string pair `("job", <sub>)` over every tracked `.py` file and report
every site whose second element is `run-next`; it must be EMPTY after C4, and
you must report what it read BEFORE C4 as well. Then, SERIALLY in the primary
checkout and only after C4 is committed, `python3 -B -m pytest tests/ -q`:
report the full summary line and the exit code. The reviewer ran this exact
suite over this exact change in a disposable worktree at `7d14e89f` and read
`18339 passed, 23 skipped` at exit 0, which is identical to the reading at the
base — this round adds and removes no test. Report YOUR numbers. Then the
canary `python3 -m pytest tests/cli/test_golden_path.py -q`, and
`python3 -m pytest tests/docs/ -q`, which this round owes because C3 touches a
`docs/` path.

**G8 NOTHING ELSE MOVED (at C4).** `.agent/STOP` read from disk and ABSENT.
`git status --porcelain` EMPTY. `git worktree list` exactly ONE entry. Branch
`feature/f275-one-world-completion-part-three`.
`git diff --name-only 7d14e89f..<C4>` an EXACT SET MATCH against the path list
in the header's `Change:` line, which does not include `.agent/handoff.md`,
reported as MISSING and EXTRA, both empty. Per-commit insertions for every
commit before the handback, each under the DECISION F104 D1 cap of 500. Also
report `ruff check` over every `.py` path in the change set and its exact output
line.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries the
SESSION NUMBER 16 of feature F275, round 33, ONE LINE PER GATE with real exit
codes and real numbers, the changed-files table with the `+/-` column taken from
`git diff --numstat` and not from file line counts (§3 item 28), the
item-status table, the open-findings count, and the one-sentence context
self-assessment amend0905-throughput requires. Declare every deviation.
