── STEP T003 (first consumer) / F272 — round 16 ──
Goal:   Fix a PROVEN product defect the F272 state rename left behind — `remedy
        job stop <completed-job> --json` raises `AttributeError` instead of
        printing its error JSON — and give that path the guard whose absence is
        the reason it survived.
Base:   `c80f32ce`. Branch `feature/f272-one-world-completion`. SESSION 8.

THE PRODUCTION CHANGE IS ONE LINE and is given as a FROM/TO pair. The
marker-delimited slices are byte-verbatim.

## What was measured, and why this round exists

Round 15 closed T002. Opening T003, the reviewer re-grepped the eleven consumers
F260's Design section names — that file orders a re-grep, and DECISION F272 D7
records what an inferred site set cost this branch — and found the classic-store
surface far smaller than the 2026-09-05 measurement. It also found this, at
`apps/cli/commands/job_stop_cmd.py:167`:

    "job_id": job_id, "job_status": job.status}, indent=2))

`JobPlan.status` was RENAMED to `state` in round 9 and RETYPED in round 14.
Measured at `c80f32ce` by importing the shipped modules: `JobPlan` has `state`
and has NO `status`, and `_CoreJobAdapter.__slots__` is
`('state', 'stop_request_id', 'stop_reason', 'stop_source', 'stopped_at')` —
also no `status`. So that line cannot succeed for either object it can receive.

PROVEN BY RUNNING THE SHIPPED HANDLER, not by reading it. With `_load_job`
returning a completed `JobPlan`, `_cmd_job_stop(job_id, json_output=True)`
raises `AttributeError: 'JobPlan' object has no attribute 'status'`, while the
SAME call with `json_output=False` exits 1 and prints its message correctly —
because only the JSON branch reads that attribute. The operator asking for
machine-readable output gets a traceback; the one who does not, gets the truth.

WHY NO TEST CAUGHT IT, which is the half worth keeping: `tests/cli/
test_job_stop.py` has `test_a_completed_job_is_not_told_that_work_will_stop`
covering the completed path WITHOUT `--json`, and it has
`test_an_unwritable_control_area_says_so_in_json_too` — the established "...in
JSON too" sibling. The completed case is the one pairing the file never made.
C5 makes it, and it is a real discriminator: measured in a disposable worktree
at `c80f32ce`, the guard alone is EXIT 1 with that AttributeError, and with C4
applied the same file is EXIT 0 at 27 passed.

## Bundle (ordered; commit in this order, nothing added or reordered)

- C0a save this block to `.agent/authored/f272-r16.md` by `shutil.copyfile`
- C0b mirror the same source to `.agent/last_block.md` by `shutil.copyfile`
- C1  `.agent/plan.md` REPLACED by the PLANF272R16 slice
- C2  `.agent/live_review.md` APPEND the RECORDR16 slice — the round 15 verdict
      and the R-0822 registration, BEFORE the fix, per §4 item 4
- C3  `.agent/prose_slips.md` APPEND the SLIPSR16 slice
- C4  the fix: the single FROM/TO pair below, over `job_stop_cmd.py` ONLY
- C5  `tests/cli/test_job_stop.py` INSERT the GUARDR16 slice
- C6  `.agent/live_review.md` APPEND the LANDEDR16 slice
- C7  rewrite `.agent/handoff.md`

C4 and C5 are separate so the guard's colour is attributable: C5 alone on top of
C4 is green, and the round's own red-proof (G5) is the ordered pair. C6 is
separate because a `Landed:` line may only be written once the fix is on disk,
and only the REVIEWER writes `Done:` — never you.

## Change set — these paths and no others

    .agent/authored/f272-r16.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    apps/cli/commands/job_stop_cmd.py
    tests/cli/test_job_stop.py
    .agent/handoff.md

## C4 — the one-line fix, over `apps/cli/commands/job_stop_cmd.py`

The pair is rendered AT THE FILE'S OWN INDENTATION; this fenced block adds
nothing to the content line. The FROM occurs EXACTLY 1x, measured at
`c80f32ce`. The containment test was RUN, not asserted, and its output is
`TO contains FROM: false` — this is a REWRITE, so the §4.9 rewrite counts are
attainable and are ordered in G4: FROM 1x before and 0x after, TO 0x before and
1x after.

FROM:

```
                               "job_id": job_id, "job_status": job.status}, indent=2))
```

TO:

```
                               "job_id": job_id, "job_status": job.state}, indent=2))
```

Change nothing else on that line and nothing else in the file. In particular the
JSON KEY `"job_status"` DOES NOT MOVE — it is the external contract
`tests/cli/test_job_stop.py` and the cockpit both read, and round 10 preserved it
deliberately while the Python field moved.

## Constraints

1. EVERY MARKER-DELIMITED SLICE IS APPLIED BYTE FOR BYTE, extracted
   PROGRAMMATICALLY from `.agent/authored/f272-r16.md` between its BEGIN and END
   marker lines. Never retype, reflow or fix one: if a slice looks wrong, APPLY
   IT ANYWAY and say so in the handback — the reviewer rules. Report how many
   you extracted; this block states no count of its own parts.
2. No marker line reaches any file but the two C0 copies.
3. No file outside the change set is edited, and NO EXISTING TEST is edited,
   deleted or weakened. C5 only INSERTS.
4. GUARDR16 is inserted so that it sits INSIDE `class TestItRefusesToLie`,
   immediately BEFORE the line
   `    def test_an_unwritable_control_area_is_loud_and_requests_nothing(self, job, capsys):`
   which occurs exactly 1x. The slice ends with its own blank line, so the
   anchor line follows it directly with no separator inserted.
5. ONE id is minted this round, R-0822, and RECORDR16 carries it. Mint no other.
   My two reviewer-prose slips from round 15 are SLIPSR16 lines, not ids.
6. Read `.agent/STOP` with `os.path.exists` before C0a, before C4 and before C7,
   and report all three readings. Stop and hand off if it ever exists.
7. Every commit boundary runs `git status --porcelain` and its REAL output is
   reported. G5's destructive check runs in a disposable worktree and NEVER in
   the primary checkout; remove it BY EXACT PATH, never by glob.

## Done when — the gates

Run each and record its REAL exit code. "Green" as a word is a finding. G5 runs
only in its own worktree; the rest run in the PRIMARY checkout. All run BEFORE
C7, so the handback can quote them.

G1 TRANSPORT — one digest comparison: `.agent/authored/f272-r16.md`,
`.agent/last_block.md` and `.remedy-wt/f272-r16-block.md` share one sha256, one
byte length and one line count. Report all three.

G2 THE RECORD — TWO appends land in this round, C2 and C6, and each is proved
SEPARATELY against its own pre-image.
(a) BYTE, per append: pre is a byte-exact PREFIX of post, and
`post == pre + b"\n" + slice`. C2's pre is 1149219 bytes with terminal bytes
`b'rong lines.\n'`, exactly one newline. C6's pre is whatever C2 left — read it,
do not assume it.
(b) STRUCTURAL, per append: N is COUNTED BY YOUR SCRIPT from that slice's own
blank-line paragraphs, never taken from this block; the LAST N units of the file
equal the slice's N paragraphs IN ORDER, everything before unchanged. Strip the
file's single terminal newline before splitting, and SAY that you did.
(c) NEGATIVE CONTROL, on the C2 append: flip one byte inside the FIRST appended
paragraph, in memory and never on disk; (a) and (b) must both REJECT, and both
ACCEPT once restored.
(d) COUNTS over the WHOLE round, before C2 -> after C6: `^- R-\d{4}` distinct
305 -> 306; `^Done: R-\d{4}` distinct 248 -> 248; open set BY DISTINCT ID
57 -> 58; `^Gate: ` 38 -> 39; `^Gate: F272 R15 ` 0 -> 1; `^- R-0822 ` 0 -> 1;
`^Landed: R-0822 ` 0 -> 1. REPORT EVERY ONE YOU MEASURE, and where a measurement
differs from the figure above, report the difference rather than adjusting
anything — the block's arithmetic is the reviewer's and is the thing at risk.

G3 THE PLAN — `.agent/plan.md` byte-equals the PLANF272R16 slice. Report byte
count, line count, that it is under the AGENTS.md cap of 50, and that `## Goal`
and `## Next Steps` are present.

G4 THE FIX IS REAL — three readings, the first two over the file's text and the
third against the RUNNING handler:
    (i)   the C4 REWRITE counts: `job.status` in that file 1 -> 0, and
          `job.state}, indent=2))` 0 -> 1
    (ii)  `"job_status"` — the external JSON key — occurs the SAME number of
          times before and after; report both numbers
    (iii) import the shipped `apps.cli.commands.job_stop_cmd`, point `_load_job`
          at a completed `JobPlan`, call `_cmd_job_stop(job_id,
          json_output=True)`, and report that it raises SystemExit with code 1
          and that the printed JSON has `"error": "job_not_stoppable"` and
          `"job_status": "completed"` — NOT an AttributeError

G5 RED-PROOF — the round's own ordered colour, in a disposable worktree at C5's
commit, never in the primary checkout. Purge `__pycache__`, use `python3 -B`,
and FIRST print `apps.cli.commands.job_stop_cmd.__file__` to confirm it resolves
INSIDE the worktree, because an editable install can shadow it. Then, in that
worktree, REVERT C4 ALONE — restore the single `job.status` line in
`apps/cli/commands/job_stop_cmd.py`, that exact path, where the TO string
`"job_status": job.state}, indent=2))` occurs exactly 1x; report that count
before reverting — leaving C5's guard in place, and run:

    python3 -B -m pytest tests/cli/test_job_stop.py -q -p no:randomly

Report the exit code and WHICH tests failed BY NAME. The reviewer measured
EXIT 1 with exactly `TestItRefusesToLie::test_a_completed_job_says_so_in_json_too`
failing and 26 passing, the failure carrying the real AttributeError. Then
restore C4 and re-run: the reviewer measured EXIT 0 at 27 passed. Report both
exit codes in order — a colour with no baseline is not evidence. Remove the
worktree BY EXACT PATH and show `git worktree list` after.

G6 THE SUITES — run SERIALLY, each its own invocation, each `-q -p no:randomly`,
in the primary checkout. The four state readers are run AS FOUR:

    python3 -B -m pytest tests/cli/ -q -p no:randomly
    python3 -B -m pytest tests/ui_server/ -q -p no:randomly
    python3 -B -m pytest tests/orchestration/test_test_runner.py -q -p no:randomly
    python3 -B -m pytest tests/regression/test_resource_safety.py -q -p no:randomly
    python3 -B -m pytest tests/orchestration/test_integrity_gate.py -q -p no:randomly
    python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly

`tests/cli/` base is 1537 passed; C5 adds tests, so COUNT them with `ast` over
that file before and after and RECONCILE as 1537 + <your count>, reporting the
arithmetic. The reviewer's own AST count was 1 and its measured total 1538.
`tests/orchestration/` is NOT ordered this round: C4 and C5 touch neither
`packages/` nor that suite's subjects, and G5 plus `tests/cli/` reach every line
this round changes.

G7 LINT AND INTEGRITY:

    python3 -m ruff check apps/cli/commands/job_stop_cmd.py tests/cli/test_job_stop.py
    python3 -m apps.cli.grouped integrity check --json

Bare `ruff` is denied to this environment. Report both exit codes and, for
integrity, `passed` and `fail_count`. Note that `integrity check` also reads the
finding ledger: a newly registered OPEN Medium is expected and must not turn
`high_blockers_open` red — if it does, report it rather than editing the finding.

G8 THE TREE — `git status --porcelain` empty at every commit boundary and at the
end; `git ls-files .remedy-wt` empty; `git worktree list` showing the primary
plus the twelve pre-existing `remedy/job-*` entries and nothing else. Then the
per-commit insertions from `git diff --numstat <parent> <commit>`, EXCLUDING C7,
which cannot count its own insertions. Each must be under the DECISION F104 D1
cap of 500 and match the handback's `## Commits` table cell for cell.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md, carrying
SESSION 8, the changed-files table with real `+/-` from `git diff --numstat`,
ONE LINE PER GATE with its real exit code, and an item-status table covering C0a
through C7 exactly once each. No length cap applies (amend0827 rule 3). Declare
every deviation. Push `feature/f272-one-world-completion`; create NO PR, merge
nothing, force-push nothing.

<<<BEGIN PLANF272R16>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 15 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001 and T002 are
COMPLETE: the run re-key, the eight administrative fields, the widened
`RunState`, the `state` rename and retype, the cockpit's two settled states, and
the Mission record's order and contract.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the consumers, T004 the classic
runner, T005 the reachability test and the cluster deletion.

## Current Step

T003's first consumer, and a defect found while re-grepping the consumer list:
`apps/cli/commands/job_stop_cmd.py` still reads `job.status`, a field the round 9
rename moved to `state`, on the branch that emits the completed-job error JSON.
Registered as R-0822, fixed and guarded in the same round with the JSON sibling
test the file never had.

## Next Steps

1. The rest of T003's consumers, re-grepped rather than taken from F260's
   2026-09-05 list: `teach_cmd.py`, `ui_server.py`, `job_context_cmd.py` and the
   `_JobPlanTaskAdapter` shim, each with a test on a ping-pong-created job.
2. T004, the classic runner and the resolver collapse, which is where
   `_CoreJobAdapter` dies with the classic store it exists to adapt.
3. T005, the reachability test and the cluster deletion, which is never split.

## Risks

- The five tests.md ids named in this feature's Acceptance (R-0803, R-0804,
  R-0807, R-0810, R-0812) were routed to F273 by the 2026-09-06 triage. Whether
  F272's Acceptance still requires them is UNSETTLED and must be ruled before
  closure, or the feature cannot be closed self-consistently.
<<<END PLANF272R16>>>

<<<BEGIN RECORDR16>>>
Gate: F272 R15 — the F272 round 15 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ. Range `998151b8`..`c80f32ce`, eight commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, with the change set exactly the nine ordered paths and nothing else. G1 TRANSPORT IS A REAL CHAIN AND NOT MERELY SELF-CONSISTENT: the reviewer's own scratch original `.remedy-wt/f272-r15-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f272-r15.md` and `.agent/last_block.md` are all 28937 bytes at 479 lines and all hash to `3d79218a4149682eb3f1d94bd37137add08f5d995771b0ebf3fec3987c91e224`; per §3 item 37 that chain covers those three artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD reproduces byte for byte: `.agent/live_review.md` 1145308 to 1149219, pre-image a byte-exact prefix, `post == pre + NL + slice` TRUE; registrations 305 unchanged, resolutions 248 unchanged, open set BY DISTINCT ID 57 unchanged. G3 THE PLAN is 1956 bytes byte-equal to its slice at 39 lines against the cap of 50. G4 THE EXTENSION reproduces against the SHIPPED module on all seven readings: a mission with neither field writes neither key; a pre-F272 record loads with `order` and `contract` both None and re-exports BYTE-IDENTICALLY; both setters round-trip through disk; `MISSION_SCHEMA_VERSION` is still 1; and a non-object order and a non-object contract are each refused with their own message. G5 THE RED-PROOF was re-run by the reviewer in its own disposable worktree, provenance confirmed inside it and removed afterwards by exact path: control EXIT 0 at 88 passed, mutated EXIT 1 at 2 failed and 86 passed, restored EXIT 0 at 88 — and the two that fall are exactly `test_a_mission_that_has_neither_writes_neither_key` and `test_a_record_written_before_this_round_re_exports_byte_identically`, so every pre-existing guard is blind to the additive property and only the new pair sees it. G6 THE SUITES, re-run serially: `tests/orchestration/` EXIT 0 at 12856 passed and 10 skipped, being the base of 12850 plus exactly the 6 tests C5 adds by AST count, difference 0; `tests/ui_server/` 515; `tests/docs/` 303; `test_test_runner.py` 52 — GREEN in the primary checkout, which confirms the single worktree failure the block warned of was the missing-`node_modules` artifact; `test_resource_safety.py` 21; `test_roadmap_index.py` 30; `test_integrity_gate.py` 16; the canary 42. G7 ruff EXIT 0 over both changed files, integrity EXIT 0 with `"passed": true` and `"fail_count": 0`. G8 THE TREE: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, thirteen worktree entries, and per-commit insertions 479, 434, 18, 4, 57, 102 and 88, each under the DECISION F104 D1 cap of 500. THE PRODUCTION CODE WAS SPECIFIED, NOT SLICED, and the worker's implementation is better than the specification: it carries 102 insertions against the reviewer's dry-run 90, the difference being docstrings written at the length this file already uses for `dossier_ref` and `mission_plan`. THE WORKER'S THREE DEVIATIONS ARE ALL UPHELD AND TWO OF THEM ARE THE REVIEWER'S DEFECTS. Deviation 1: G2(d) ordered `^Gate: ` 36 to 37 and `^Gate: F272 R14 ` 0 to 1, and the true readings are 36 to 38 and 0 to 2, because the RECORDR15 slice is TWO paragraphs and both begin at the line anchor with `Gate: F272 R14 ` — the reviewer's own pre-emission script printed that paragraph count and the count gate was never resolved against it. Deviation 2: the block declared `TO contains FROM: true` for both C5 import pairs; the containment test, run by the worker and independently by the reviewer, answers FALSE for both, because each TO inserts INTO the middle of its FROM rather than appending — both are REWRITEs, the post-edit FROM count of 0 is attainable and correct, and the block asserted a measurement's OUTPUT without running the measurement, which is precisely the R-0522 shape §3 item 15 exists to prevent. Neither reached disk: every FROM was unique, the replacements were exact, alphabetical import order held and ruff is clean. Deviation 3, the paragraph splitter needing a stated newline normalization, is accepted as an honest report of a first reading that was run and corrected rather than hidden. Both reviewer defects are dated lines in `.agent/prose_slips.md` under amend0827 rule 2 and spend no id. FURTHER EVIDENCE FOR THE OPEN FINDING R-0820, recorded here rather than as a second id per §3 item 30: R-0820's fix installed the runtime-probe method DECISION F272 D7 rules, and round 10's entry reports that probe converging at EXIT 0 with an EMPTY site log, with `_CoreJobAdapter` moved "together with all six of its consumers". That convergence is bounded by WHAT THE SUITE EXECUTES. Measured at `c80f32ce`, `apps/cli/commands/job_stop_cmd.py:167` still reads `job.status` on the completed-job JSON branch, which no test in the repository reaches, so the probe could not see it and the empty log was true of the reachable set only. R-0822, registered below, is that surviving site as a product defect; this paragraph is the correction to R-0820's completeness claim, and R-0820 stays OPEN.

- R-0822 — Medium, `remedy job stop <completed-job> --json` RAISES AttributeError INSTEAD OF PRINTING ITS ERROR JSON, BECAUSE ONE SITE OF THE F272 STATE RENAME SURVIVED ON A BRANCH NO TEST EXECUTES. MEASURED at `c80f32ce` by importing the shipped modules: `packages.orchestration.pingpong_job.JobPlan` has the field `state` and has NO `status` — round 9 renamed it and round 14 retyped it onto `RunState` — and `apps/cli/commands/job_stop_cmd.py`'s `_CoreJobAdapter.__slots__` is `('state', 'stop_request_id', 'stop_reason', 'stop_source', 'stopped_at')`, also without `status`. `apps/cli/commands/job_stop_cmd.py:167` nonetheless reads `job.status`, inside the `_FINISHED_STATES` branch's JSON payload, so the expression cannot succeed for EITHER object `_load_job` can return. PROVEN BY RUNNING THE SHIPPED HANDLER rather than by reading it: with `_load_job` returning a completed `JobPlan`, `_cmd_job_stop(job_id, json_output=True)` raises `AttributeError: 'JobPlan' object has no attribute 'status'`, while the identical call with `json_output=False` exits 1 and prints its message correctly — the plain-text branch never reads the attribute, which is exactly why the defect is invisible from the terminal. WHY NO GUARD SAW IT: `tests/cli/test_job_stop.py` carries `test_a_completed_job_is_not_told_that_work_will_stop`, which covers this branch WITHOUT `--json`, and carries `test_an_unwritable_control_area_says_so_in_json_too`, which is the file's own established "...in JSON too" pairing; the completed-job case is the one pairing the file never made, and the string `job_not_stoppable` appears nowhere under `tests/`. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE THIS ID WAS MINTED, per §3 item 30, by grepping `.agent/live_review.md` for `job_stop_cmd`, `job.status` and the missed-rename phrasings; the only related open entry is R-0820, and it is not a duplicate — R-0820 is a GATE derived from the same predicate as the change set it gates, whose resolution is a method, while this is a LINE of shipped product code whose resolution is one attribute name. The evidence that R-0820's probe method is complete only up to the suite's reach is added to R-0820 in the gate entry above, so the two are linked rather than merged. WHY MEDIUM: the failure is loud, confined to one error path of one command, and corrupts nothing — but it is the machine-readable path, so any script or UI calling `job stop --json` on a finished job gets a traceback and a non-contract exit instead of the documented `job_not_stoppable` payload, and `apps/cli/command_catalog.py` advertises `supports_json` True for `job.stop`. RESOLVED WHEN `job_stop_cmd.py` reads `job.state` on that branch, the external JSON key `"job_status"` is unchanged, and `tests/cli/test_job_stop.py` carries a test that exercises the completed-job `--json` path and asserts the `job_not_stoppable` payload — a test that is RED against the line as it stands today.
<<<END RECORDR16>>>

<<<BEGIN SLIPSR16>>>
2026-09-07 — F272 R15 — the round 15 block's G2(d) ordered `^Gate: ` 36 to 37 and `^Gate: F272 R14 ` 0 to 1, while its own RECORDR15 slice was TWO paragraphs each beginning at the line anchor with `Gate: F272 R14 `, so the true readings are 36 to 38 and 0 to 2; the reviewer's pre-emission script printed the paragraph count of 2 and the count gate was never resolved against it, which is §3 item 35 — a description and the enumeration it points at read against each other — reaching the block's own arithmetic.

2026-09-07 — F272 R15 — the round 15 block declared `TO contains FROM: true` for both C5 import pairs without running the containment test; the true answer is FALSE for both, because each TO inserts into the MIDDLE of its FROM rather than appending, so both are REWRITEs. Nothing wrong reached disk — each FROM was unique, the replacements exact, import order preserved, ruff clean — but writing a measurement's output format without performing the measurement is exactly the R-0522 shape §3 item 15 exists to prevent, and it was written by the reviewer that quotes that item.
<<<END SLIPSR16>>>

<<<BEGIN GUARDR16>>>
    def test_a_completed_job_says_so_in_json_too(self, job, capsys):
        """The JSON sibling of the test above.

        Its absence is why a stale attribute survived the F272 state rename: the
        plain-text branch never reads it, so only this path can see it.
        """
        job.state = JOB_COMPLETED
        _persist_job(job)

        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_stop(job.job_id, json_output=True)

        assert exc.value.code == 1
        payload = json.loads(capsys.readouterr().out)
        assert payload["ok"] is False
        assert payload["error"] == "job_not_stoppable"
        assert payload["job_status"] == JOB_COMPLETED
        assert stop_requested(job.job_id) is None

<<<END GUARDR16>>>

<<<BEGIN LANDEDR16>>>
Landed: R-0822 — `apps/cli/commands/job_stop_cmd.py` now reads `job.state` on the completed-job JSON branch, and `tests/cli/test_job_stop.py::TestItRefusesToLie::test_a_completed_job_says_so_in_json_too` exercises that path and asserts the `job_not_stoppable` payload. The external JSON key `"job_status"` is unchanged. Landed by this round's C4 and C5; the reviewer's `Done:` is owed at the next gate.
<<<END LANDEDR16>>>
