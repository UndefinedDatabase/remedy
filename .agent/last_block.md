── STEP T002 (the state collapse, move two, re-scoped) — F272 ─
Goal:        Rename `JobPlan.status` to `JobPlan.state` at every site that is
             REALLY a JobPlan, changing no type, value, rendering or stored key;
             determine that site set by RUNTIME PROBE, not by static
             classification; rule the method as DECISION F272 D7.
Bundle:      C0a save the block · C0b mirror · C1 the plan · C2 the round 9
             verdict and finding R-0820 · C3 DECISION F272 D7 · C4 the measured
             inventory · C5 the rename · C6 the test · C7 the handback.
Change:      EXACTLY the paths under "The change set", plus every path C4's own
             measurement names, and nothing else.
Handback:    completion report + rewrite `.agent/handoff.md`.
── end header. Per §3 item 37 every run of a repeated character in this block's
frame states its length: line 1 carries a run of 2 U+2500 then a run of 1, and
this line one run of 2 — both measured, not recalled.

## What the reviewer MEASURED before ordering this (§3 item 34)

Round 9 PASSED: C0a through C3 landed as ordered, and C4/C5 did not because the
worker measured that the block's change set could not produce a correct rename
and stopped under guardrail G8 rather than commit a tree it had already measured
as 152 tests red. The defect is the reviewer's, C2 registers it as R-0820, and
this block is its repair. Every reading below was taken BY ME at `027bdc2c` over
the 1065 tracked `.py` files from `git ls-files`, none carried over from round 9.

- ROUND 9's SITE RULE IS BLIND IN BOTH DIRECTIONS. It selected a receiver by its
  NAME — a bare `Name` in (`job`, `plan`, `job_plan`, `jp`, `loaded`,
  `reloaded`, `j`, `resumed`) — and gate G4(ii) counted over that SAME set, so
  the gate could not see a site the edit missed. I reproduce its four base counts
  exactly: INSIDE the twenty `.status` 86, `.state` 11; OUTSIDE 4 and 125.
- A RECEIVER-TYPE SWEEP FINDS MORE, AND STILL NOT ALL. Counting only names
  ANNOTATED `JobPlan` or assigned from the six functions `pingpong_job.py`
  annotates as returning one, I read 17 files at 105 attribute sites and 32
  `status=` keyword arguments. It finds `packages/orchestration/
  self_use_findings.py:51` — `result.status` inside `def
  describe_self_use_run_defects(result: JobPlan)`, PRODUCTION code the twenty
  never named — and MISSES `apps/cli/commands/job_stop_cmd.py` entirely.
- ITERATED TO A FIXPOINT IT OVER-GROWS AND BECOMES UNSAFE. Admitting any
  function returning a JobPlan-bound name grows the producer set to 58 and the
  reading to 26 files at 204 sites, but that set holds `diff`, `_git`,
  `diff_trees` and eighteen `test_*` functions, so some of the 204 are NOT
  JobPlan sites. A false positive renames a working line and is as bad as a miss.
- WHY NO STATIC RULE CAN SETTLE IT. `.status` is polymorphic here — `TaskEntry`,
  `ApplyManifest`, a promotion result, an episode and `JobPlan` all carry one and
  the first four must NOT move; `tests/orchestration/test_predictive_budget.py`
  reads a JobPlan's and a TaskEntry's inside ONE generator at line 660.
- TWO STRUCTURAL STAND-INS MUST MOVE WITH THE FIELD, and no type analysis finds
  either. `_CoreJobAdapter` at `apps/cli/commands/job_stop_cmd.py:25-35` declares
  `__slots__ = ("status", …)` and sets `self.status = core_job.state.value` to
  present a Core Job as the interface `_cmd_job_stop` expects. `FakeJob` at
  `tests/orchestration/test_pingpong_integration.py:237-239` declares
  `status: str = "completed"` as the double for the JobPlan
  `apps/cli/commands/do_cmd.py:1892` reads.
- THE PROBE WORKS, AND I RAN IT. In a disposable worktree at `027bdc2c` I
  renamed the field and put a raising `status` property in its place; a read
  raises naming the CALLER's file and line. Under it
  `tests/orchestration/test_self_use_findings.py` reported
  `packages/orchestration/pingpong_job.py:667`, the `"status": job.status` line
  of `_export_job` and a real site. The worktree was removed by exact path and
  pruned; the tree is clean.
- NOTHING PINS `JobPlan`'s FIELD SET AS A CLOSED COLLECTION: the only
  `__dataclass_fields__` reference to it in `tests/` is
  `test_mint_call_sites.py:43`, reading `job_id`'s default factory. The stored
  key is already guarded and does not move —
  `tests/orchestration/test_job_evidence.py:118` and `:184` assert
  `result["manifest"]["status"]`, which stays spelled `status` under D5.
- THE BASE SUITE COUNTS, from the round 8 gate I ran myself and unchanged by
  round 9, which landed no `.py` file: `tests/orchestration/` 12838 passed and
  10 skipped, `tests/cli/` 1537, `tests/docs/` 303, canary 42.

## What the OPEN SET binds on this block (§3 item 34, last clause)

"BINDING ON THE NEXT BLOCK THAT ORDERS A HANDBACK" — APPLIED, same words, in the
Handback section. R-0819's "BINDING ON THE NEXT BLOCK … THAT GATES THE SHADOW
PROPERTY" — DECLINED AS NOT APPLICABLE: no `run_dir`/`runs_dir` gate here, still
owed by T003/T004; its GENERAL clause, run a gate at its base before ordering
it, APPLIES and was applied to every gate below.

## The change set

C2: `.agent/live_review.md`. C3: `docs/roadmap/features/T2_F272.md`.
C4: `.agent/f272_state_rename_inventory.md` (NEW).
C6: `tests/orchestration/test_job_state_field.py` (NEW).
C0a/C0b/C1/C7: `.agent/authored/f272-r10.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/handoff.md`.

C5's paths are NOT a closed list, and that is the correction this block makes.
C5 changes exactly the files C4's measurement names. My annotation-only sweep
names these seventeen as the expected core — a STARTING POINT you verify, not a
set you trust: under `apps/cli/commands/` `do_cmd.py` and `job_stop_cmd.py`;
under `packages/orchestration/` `pingpong_job.py`, `job_evidence.py`,
`job_promote.py`, `self_use_findings.py` and `ui_server.py`; under `tests/cli/`
`test_job_rerun_manifest.py`; and under `tests/orchestration/`
`test_f018_authority_integration.py`, `test_f018_package_pipeline_e2e.py`,
`test_failure_wiring.py`, `test_job_evidence.py`, `test_job_promote.py`,
`test_job_task_runner.py`, `test_job_worktree_handoff.py`,
`test_run_manifest_runtime_truth.py` and `test_self_use_findings.py`.

Round 9's worker measured eleven further files going red under a narrower
rename. EXPECT the final set to exceed this list; every file you add is reported
in the handback with the evidence that put it there, and adding a file the probe
named is INSIDE this change set and is not scope drift.

## C4 — the inventory, a SPEC and not a slice

Build `.agent/f272_state_rename_inventory.md` by MEASUREMENT in a disposable
worktree under `.remedy-wt/`, never in the primary checkout.

1. Rename the `JobPlan` dataclass field `status: str = JOB_PLANNED` to `state:
   str = JOB_PLANNED`. THE ANNOTATION STAYS `str`, THE DEFAULT STAYS
   `JOB_PLANNED`: retyping to `RunState` is D6's move three, not this round.
2. Install a raising `status` property on `JobPlan` whose getter AND setter
   append `<file>:<line>` of the CALLING frame to a log file INSIDE the
   worktree — NOT under `/tmp`, which this workflow cannot read back — then
   raise `AttributeError`.
3. Run `python3 -B -m pytest tests/orchestration/ tests/cli/ -q -p no:randomly`,
   confirming `pingpong_job` resolves from INSIDE the worktree via `__file__`.
4. Rename every site the log names. Re-run. REPEAT until the run is EXIT 0. Each
   pass finds at most one site per failing test, so several passes are expected;
   this iteration IS the measurement.
5. Rename the two structural stand-ins with their consumers: `_CoreJobAdapter`'s
   slot and assignment, and `FakeJob`'s field.
6. The inventory records per site: path, line at `027bdc2c`, enclosing function
   or class, and HOW it was classified — `probe` for one the running suite
   named, `annotation` for one my sweep named that the probe never executed,
   `stand-in` for the two above. List the `annotation`-only sites under their
   own heading: no test covers them, so nothing catches them if they are wrong.

The inventory is EVIDENCE and states what was measured, never a prediction. If
the suite cannot be driven to EXIT 0, STOP and hand off with the log: an
unconverged inventory is the guess that cost round 9.

## C5 — the rename, a SPEC and not a slice, and ONE commit

Apply the inventory to the primary checkout in ONE commit — it cannot be split,
because any intermediate commit leaves the old name on some callers and the new
on others, so the suite is red and no gate could be honest. If the insertion
count exceeds the AGENTS.md cap of 500, declare it with the inseparability
reason per the Commit Discipline exception.

TWO THINGS DO NOT MOVE, both DECISION F272 D5's ruling:
  - THE STORED JSON KEY STAYS `"status"`. In `_export_job` the entry becomes
    `"status": job.state`; in `_import_job` the argument becomes
    `state=data.get("status", JOB_PLANNED)`, so every record on disk still loads.
  - THE SIX `JOB_*` CONSTANTS KEEP THEIR NAMES, VALUES AND TYPE.

DO NOT touch `TaskEntry.status`, `ApplyManifest.status`, a promotion result's or
an episode's `status`, anything merely CONTAINING `status` (`final_status`,
`worktree_cleanup_status`, `job_status`), or the classic `Job.state` sites in
`ui_server.py` and `do_cmd.py`. A site is renamed because the probe named it or
the inventory classifies it, never because it reads well.

## C6 — the test, a SPEC and not a slice

NEW FILE `tests/orchestration/test_job_state_field.py`, following the module
docstring convention of `test_job_administrative_fields.py`. Every test carries a
one-sentence docstring saying WHAT it pins and why that could break. At minimum:

1. **The field is `state` and `status` is gone.** `"state" in
   JobPlan.__dataclass_fields__` and `"status" not in` — the second is what
   makes this a replacement rather than an addition.
2. **The default is unchanged.** `JobPlan().state == JOB_PLANNED == "planned"`.
3. **The stored key did NOT move.** `_export_job` emits a `"status"` key
   carrying the state and NO `"state"` key; `_import_job` over an old record
   whose only lifecycle key is `"status"` returns a `JobPlan` whose `state` is
   that value.
4. **The round trip.** `_import_job(json.loads(json.dumps(_export_job(plan))))`
   preserves a non-default state, asserted for at least `JOB_BLOCKED`.
5. **The rendering is unchanged** — the guard D6 exists to protect: for a job
   whose state is `JOB_BLOCKED`, `f"{job.state}"` and the exported `"status"`
   value are both the plain string `"blocked"`. This is what goes red in move
   three if the retype lands without `.value` at the boundaries.

## Constraints

1. NO SLICE IS EDITED — apply the authored texts byte for byte between their
   markers; if one looks wrong, apply it anyway and say so. C4, C5 and C6 are a
   SPEC: write that code yourself.
2. The change set is the paths listed above PLUS every path C4's measurement
   names. Report each addition with its evidence.
3. Commit order C0a, C0b, C1, C2, C3, C4, C5, C6, C7, nothing reordered; C1 is
   the first substantive commit (§3 item 23).
4. APPEND CONVENTION for `.agent/live_review.md` and
   `docs/roadmap/features/T2_F272.md`: `post == pre + b"\n" + slice`, the slice
   being the marker-delimited lines each with its terminating newline, and the
   post-image ending in exactly one `\n`. PLAN CONVENTION: `.agent/plan.md` is
   REPLACED by exactly the PLANF272R10 slice.
5. Behaviour changes: NONE. No value, type, rendering, stored key or `JOB_*`
   constant changes; this round renames one field and its two stand-ins.
6. Mint NO finding id of your own and write NO `Done:` paragraph of your own.
7. Destructive verification goes in a disposable `git worktree` under the
   gitignored `.remedy-wt/`, never the primary checkout (protocol G5); remove
   and prune it before the handback, BY EXACT PATH and never by glob.
8. Read `.agent/STOP` with `os.path.exists` before C0a, before C5 and before
   C7, and table all three; if it appears, finish only the half-written commit,
   then hand off (protocol G6).
9. `python3 -B` for every run; purge `__pycache__` in any worktree before a
   run; report each gate's REAL exit code, "green" as a word being a finding.

## Gate list — DONE WHEN

**G1 TRANSPORT.** sha256 and byte length of the committed
`.agent/authored/f272-r10.md` and `.agent/last_block.md`; both equal each other
and the BLOCK_SHA and length the delegation names. Per §3 item 37 this covers
the saved copy and its mirror, not the bytes emitted into your prompt — say so.

**G2 THE RECORD, at C2.** Readers (a) to (d) over `.agent/live_review.md`.
(a) BYTE: pre and post lengths; pre a byte-exact prefix; `post == pre + b"\n" +
slice`; pre's terminal byte asserted to be exactly one `\n` BEFORE writing; post
ends in exactly one `\n`.
(b) STRUCTURAL, computed independently of (a) by splitting the WHOLE image on
`\n{2,}`, with N COUNTED BY YOUR SCRIPT from the slice's own paragraphs and
never taken from this block: units before, after, delta; the last N units equal
the slice's paragraphs IN ORDER; the units before an unchanged prefix.
(c) NEGATIVE CONTROL in memory on a `bytes` object, never on disk: flip a byte
inside the FIRST appended paragraph, asserting the offset lies inside it first;
(a) and (b) must BOTH reject; restore and require both to accept and the
restored image to equal the disk image.
(d) COUNTS before → after C2: `^- R-\d{4} — ` distinct ids 303 → 304; `^Done:
R-\d{4} — ` distinct 247 → 247; open set BY DISTINCT ID 56 → 57; `^Gate: ` 31 →
32; `^Gate: F272 R9 ` 0 → 1; `^- R-0820 — ` 0 → 1.

**G3 THE PLAN at C1, AND THE FEATURE FILE at C3.** The plan: `.agent/plan.md`
equals the PLANF272R10 slice bytes exactly; report the equality, both byte
lengths, the line count against the AGENTS.md cap of 50, and that `## Goal` and
`## Next Steps` are present. The feature file: readers (a) and (b) of G2's
wording, no negative control (gate budget); plus the count YOU measure of
`^### DECISION F272 D\d+ ` lines and the D-number each names, in order.

**G4 THE RENAME IS COMPLETE, BY A GATE THAT CAN FAIL, at C6.** This replaces
round 9's blind count and is the reason R-0820 exists.
(i) THE RESIDUAL PROBE. In a disposable worktree at the commit C6 creates,
install the SAME raising `status` property of C4 step 2 — the field is already
`state`, so the property is the only edit — and run `python3 -B -m pytest
tests/orchestration/ tests/cli/ -q -p no:randomly`. The site log must be EMPTY
and the run EXIT 0; an empty log with a RED run proves nothing, so report both.
A non-empty log names a site C5 missed and is a finding of this round.
(ii) THE NON-VACUITY CONTROL, in that same worktree and BEFORE the reading
above: revert ONE inventory site back to `.status`, confirm the log names
exactly that site and the run is EXIT 1, then restore and confirm the file is
byte-identical. A probe that cannot catch a reverted site measures nothing.
(iii) THE FIELD: `"state" in JobPlan.__dataclass_fields__` TRUE, `"status" in`
FALSE — the base at `027bdc2c` is the inverse. Print
`packages.orchestration.pingpong_job.__file__` first.
(iv) THE STORED KEY DID NOT MOVE: for a `JobPlan` with `state=JOB_BLOCKED`,
`_export_job` has key `"status"` valued `"blocked"` and NO key `"state"`;
`_import_job` over a dict carrying `job_id` and `"status": "blocked"` and no
`"state"` key returns a `JobPlan` whose `state` is `"blocked"`.
(v) NOTHING WAS RETYPED: `type(JobPlan().state).__name__` is `str` and
`isinstance(JobPlan().state, RunState)` is FALSE.

**G5 THE PIN CAN FAIL — MUTATION RED-PROOF, in a disposable worktree at the
commit C6 creates.** Purge `__pycache__` and confirm `pingpong_job` resolves
from inside the worktree. FIRST the UNMUTATED CONTROL:
`python3 -B -m pytest tests/orchestration/test_job_state_field.py -q
-p no:randomly` must be EXIT 0; report its summary line. THEN three mutations of
the worktree's own `packages/orchestration/pingpong_job.py`, each byte string
counted in that file first where the count must be 1 (§3 item 25), each followed
by a restore and a control re-run that must be EXIT 0 again: (1) rename the
dataclass field `state` back to `status`; (2) change the exporter's key from
`"status"` to `"state"`; (3) change the importer's read from
`data.get("status", JOB_PLANNED)` to `data.get("state", JOB_PLANNED)`, the
old-record path. Each must be EXIT 1; report one exit code per mutation. A
mutation leaving the run GREEN is a test that pins nothing and is a finding.

**G6 THE SUITES, at C6, run SERIALLY, each its own invocation.** The new file,
then `tests/orchestration/`, `tests/docs/`, `tests/cli/`, then the canary
`tests/cli/test_golden_path.py`. Every one EXIT 0; report each exit code and
summary line verbatim. Base at `027bdc2c`: `tests/orchestration/` 12838 passed
and 10 skipped, `tests/docs/` 303, `tests/cli/` 1537, canary 42. A LOWER count
anywhere is a finding; `tests/orchestration/` must RISE by C6's tests.

**G7 LINT AND INTEGRITY, at C6.** `python3 -m ruff check` over exactly the `.py`
files this round changed, in ONE invocation: EXIT 0; if red, report the codes and
fix nothing outside the change set. A repo-wide `ruff check .` is NOT ordered: it
is EXIT 1 on base under OPEN finding R-0468. Then
`python3 -m apps.cli.grouped integrity check --json`: EXIT 0, `"passed": true`,
`"fail_count": 0`.

**G8 THE TREE.** `git status --porcelain` EMPTY when C7 is staged;
`git ls-files .remedy-wt` EMPTY; `git worktree list` naming every worktree you
created and confirming its removal by exact path. Per commit C0a through C6 —
NOT C7, which cannot count its own insertions (§3 item 14) — the insertion count
from `git diff --numstat <parent> <commit>`, each single-parent; those same
numbers fill the handback's `## Commits` `+/-` column, so report both readings
side by side and confirm each row cell by cell (§3 item 28). Marker sweep: the
number YOU measure of `<<<BEGIN `/`<<<END ` lines in every written non-block
file, zero in each. The three `.agent/STOP` readings as a table.

## The slices

<<<BEGIN PLANF272R10>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 9 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001 is COMPLETE;
T002 has landed the eight administrative fields and widened `RunState` to cover
every value the job lifecycle field can hold.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the eleven consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

The `state` collapse, move two of the three DECISION F272 D6 stages. Round 9
proved the site set cannot be derived from receiver names, so this round
measures it by running the suites against a raising `status` property and
renames exactly what that probe reports, plus the two structural stand-ins. The
measurement lands as an inventory beside the rename, and a new test pins the
field, the unchanged stored key, the old-record path and the rendering.

## Next Steps

1. Move three: retype `JobPlan.state` to `RunState` and make the six `JOB_*`
   constants `RunState` members, with `.value` at every boundary leaving the
   record. `RunState`'s `str()` is `'RunState.X'` while its f-string is the
   value, so move two's rendering guard is what that move must keep green.
2. The Mission extension — the order, the contract, the mission plan and the
   ordered job references.
3. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each tested on a job built through the ping-pong path.
4. T004, the classic runner and the resolver collapse; then T005, the
   reachability test and the cluster deletion, which is never split.

## Risks

- The rename cannot be staged by caller: an intermediate commit leaves both
  names live and the suite red, so it is one commit or none.
- `.status` is polymorphic here; a site is renamed only on evidence, never
  because its receiver reads like a job.
<<<END PLANF272R10>>>

<<<BEGIN RECORDR10>>>
Gate: F272 R9 — the F272 round 9 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ. Range `c1c8f76d`..`027bdc2c`, six commits, every one single-parent, in exactly the bundle's ordered sequence C0a, C0b, C1, C2, C3 and C6 with nothing added or reordered; the two ordered commits C4 and C5 are ABSENT, which is the round's whole substance and is upheld below. G1 TRANSPORT IS A REAL CHAIN AND NOT MERELY SELF-CONSISTENT: the reviewer's own scratch original `.remedy-wt/f272-r9-block.md` survived, and it, the committed `.agent/authored/f272-r9.md` and the committed `.agent/last_block.md` are all 29054 bytes at 400 lines and all hash to `08eb65d964918f29c3fcd673c46a389895a3ae6f1bb6161e98219c498b237d27`; per §3 item 37 that chain covers those three artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD reproduces byte for byte under the reviewer's own readers: `.agent/live_review.md` 1104989 to 1109691 and `.agent/prose_slips.md` 135900 to 136942, each pre-image a byte-exact prefix, `post == pre + NL + slice` TRUE for both, each terminal byte exactly one newline, reader (b) accepting both with N counted at 1 from the slice's own paragraphs and units 698 to 699 and 173 to 174; registrations 303 unchanged, resolutions 247 unchanged, open set BY DISTINCT ID 56 unchanged, `^Gate: ` 30 to 31 — exactly the counts the block ordered, the first three unchanged correctly because the round minted no id. G3 THE PLAN is 2143 bytes byte-equal to its slice at 43 lines against the cap of 50 with `## Goal` and `## Next Steps` both present, and THE FEATURE FILE appended 24461 to 27130 with reader (b) accepting at N counted 7 and units 50 to 57, its `^### DECISION F272 D\d+ ` headings reading D1 D2 D3 D4 D5 D6 in order. THE MARKER SWEEP IS 0 IN ALL FIVE WRITTEN NON-BLOCK FILES, re-counted by the reviewer. G8's per-commit insertions re-measured from `git diff --numstat` are 400, 316, 22, 4, 40 and 358, each single-parent and each under the DECISION F104 D1 cap of 500, and each matches the handback's `## Commits` table cell for cell. THE WORKER'S DEVIATION 1 IS UPHELD IN FULL AND IS THE ROUND'S WHOLE VALUE: ordered to rename `JobPlan.status` across a closed list of twenty files, it measured that the list was wrong, proved it by applying the block's own scope in a disposable worktree and running the ordered suites to EXIT 1 at 153 failed and 14222 passed, attributed exactly one of those failures to the known `node_modules` worktree artifact, listed the 23 failing files with their counts, and refused to commit a tree it had already measured as 152 tests red. It changed no code to make any gate go green and minted no id of its own, which is precisely what constraint 7 and guardrail G8 require. THE REVIEWER INDEPENDENTLY CONFIRMS THE TWO LOAD-BEARING HALVES OF THAT DEVIATION at `027bdc2c`: `packages/orchestration/self_use_findings.py` imports `JobPlan` at line 36, declares `def describe_self_use_run_defects(result: JobPlan)` at line 39 and reads `result.status` at line 51, and that file is NOT among the block's twenty; and `_CoreJobAdapter` at `apps/cli/commands/job_stop_cmd.py:25-35` together with `FakeJob` at `tests/orchestration/test_pingpong_integration.py:237-239` are structural stand-ins carrying their own `status`, which no receiver-name rule and no type analysis can reach. THE REVIEWER ALSO REPRODUCES THE BLOCK'S FOUR BASE COUNTS EXACTLY — INSIDE the twenty `.status` 86, INSIDE `.state` 11, OUTSIDE `.status` 4, OUTSIDE `.state` 125, over 1065 tracked files — which is what makes the blindness demonstrable rather than arguable: those counts are equally correct on a tree with 152 failing tests, as the worker measured and the reviewer accepts. Deviations 2, 3 and 4 are accepted as declared: the plan slice describing work that did not land is the block's own G3 byte-equality forbidding its repair, and the empty ruff file set and the unreachable suites are honest reports of an absent commit rather than passes. Round 9's defect is the REVIEWER's block and is registered as R-0820 beside this entry; no part of it is the worker's.

- R-0820 — Medium, A GATE OVER PRODUCTION CODE WAS DERIVED FROM THE SAME MISTAKEN RULE AS THE EDIT IT GATES, SO IT CERTIFIED A TREE WITH 152 FAILING TESTS AS FULLY GREEN. The defect is the reviewer's, in the F272 round 9 block, and the WORKER found it, measured it and declared it as deviation 1 rather than meeting it. That block defined the rename's change set as 122 sites across twenty files, selecting attribute sites whose receiver is a bare `Name` in (`job`, `plan`, `job_plan`, `jp`, `loaded`, `reloaded`, `j`, `resumed`), and then defined gate G4(ii) as a count over THAT SAME NAME SET. A receiver's spelling is not its type, so the rule under-selects; and because the gate inherited the rule, every site the edit missed was invisible to the gate as well. MEASURED BY THE WORKER, by applying the block's scope exactly as written in a disposable worktree and running the ordered suites: EXIT 1 at 153 failed and 14222 passed, of which 152 are caused by the rename and one is the known `node_modules` worktree artifact, across 23 files of which eleven are outside the block's twenty. On that same 152-red tree the block's G4 reads FULLY GREEN — INSIDE the twenty `.status` 0, INSIDE `.state` 97, OUTSIDE `.status` 4, OUTSIDE `.state` 125, with the four survivors printing as exactly the four named paths — so four of the block's eight gates certify a broken tree and only G6, the suites, catches it. MEASURED INDEPENDENTLY BY THE REVIEWER at `027bdc2c` over the 1065 tracked `.py` files from `git ls-files`: the four base counts reproduce at 86, 11, 4 and 125; `packages/orchestration/self_use_findings.py:51` is `result.status` inside `def describe_self_use_run_defects(result: JobPlan)` with `JobPlan` imported at line 36, PRODUCTION code the twenty never named; an annotation-only receiver-type sweep reads 17 files at 105 attribute sites and 32 `status=` keyword arguments, finding that file and MISSING `apps/cli/commands/job_stop_cmd.py` entirely; and iterating that sweep to a fixpoint over-grows its producer set to 58 entries including `diff`, `_git` and eighteen `test_*` functions, so its 204 sites carry false positives. NO STATIC RULE SETTLES IT, which is the finding's real content: `.status` is polymorphic across `TaskEntry`, `ApplyManifest`, a promotion result, an episode and `JobPlan`, and `tests/orchestration/test_predictive_budget.py:660` holds a JobPlan `.status` and a TaskEntry `.status` inside ONE generator expression. Two structural stand-ins — `_CoreJobAdapter` at `apps/cli/commands/job_stop_cmd.py:25-35`, whose `__slots__` carries `status` and which exists to present a Core Job as the interface `_cmd_job_stop` expects, and `FakeJob` at `tests/orchestration/test_pingpong_integration.py:237-239` — must move with the field and are reachable by no type analysis at all. THIS IS NOT A DUPLICATE OF R-0819, which is the same family seen from the other side: R-0819 is a gate that CANNOT PASS over `run_dir`/`runs_dir`, this is a gate that CANNOT FAIL over `JobPlan.status`, and R-0819's own closing sentence — "a gate that cannot pass and a gate that cannot fail are the same defect wearing two faces" — names the kinship without covering the instance. Searched before minting per §3 item 30 by grepping `.agent/live_review.md` for `receiver`, `blind spot`, `by name`, `name-regex` and `bare Name`; the only related open entry is R-0819 and it does not describe this gate, this rule or this field. FIX, LANDED BY THE NEXT ROUND RATHER THAN OWED: the site set is determined by RUNTIME PROBE — the field renamed and a raising `status` property put in its place, the suites run, every site the raise names renamed, iterated to EXIT 0 — because only a running object knows its own type. THE COUNTER-MEASURE THAT REACHES THE CAUSE, binding on any future block that orders a mechanical edit over a set the block itself defines: the gate MUST NOT be computed from the same predicate as the change set, and where it is, the block says so and adds an independent gate that can see what the predicate misses. Round 9 had such a gate — G6, the suites — and it was ordered at a commit the round never reached, so the only instrument that could fail was scheduled behind the one that could not. OPEN.
<<<END RECORDR10>>>

<<<BEGIN DECISIONR10>>>
### DECISION F272 D7 (2026-09-07, F272 round 10) — the `JobPlan.status` rename set is determined by RUNTIME PROBE, not by static classification, because `.status` is polymorphic in this repository and only a running object knows its own type

CONTEXT. D6 made the `state` collapse three moves and put the RENAME second.
Round 9 ordered that rename over a change set selected by the receiver's NAME
and computed its gate from the same predicate; the worker applied that scope in
a disposable worktree and measured EXIT 1 at 153 failed and 14222 passed across
23 files while the block's own G4 read fully green on that same tree. Finding
R-0820 carries the full measurement, the reviewer's independent reproduction at
`027bdc2c`, and the reason no static rule settles it: `.status` is polymorphic
across `TaskEntry`, `ApplyManifest`, a promotion result, an episode and
`JobPlan`; an annotation-only sweep misses
`apps/cli/commands/job_stop_cmd.py`; iterated to a fixpoint it over-grows and
yields false positives; and the stand-ins `_CoreJobAdapter` and `FakeJob` are
reachable by no type analysis whatever.

CHOSEN. THE SITE SET IS MEASURED, NOT INFERRED. In a disposable worktree the
dataclass field is renamed to `state` and a raising `status` property put in its
place; the suites are run; every site the raise names by caller file and line is
renamed; the loop repeats until the run is EXIT 0. That converged list is
committed as `.agent/f272_state_rename_inventory.md` beside the rename, each
site carrying its classification — `probe` for one the running suite named,
`annotation` for one a static sweep named that no test executes, `stand-in` for
a structural double. The completeness gate is the probe re-installed on the
final tree with an EMPTY site log and an EXIT 0 run, paired with a non-vacuity
control that reverts one site and requires the log to name exactly it.

NOT CHANGED: D5's atomicity requirement — the rename is still ONE commit,
because a half-renamed tree is red — its ruling that the stored JSON key stays
`"status"`, and D6's three-move staging.

ALTERNATIVES CONSIDERED. Widen the static list by hand — rejected: the reviewer
cannot enumerate what it cannot type-check, and a false positive renames a
working line. Split measurement and application into two rounds — rejected: an
inventory is trustworthy only once the suite it came from is green, so the
application IS the proof of completeness. Ship a compatibility `status` property
— rejected by AGENTS.md Scope Control: replacing is deleting, there is no attic.

CONSEQUENCE. Several full suite passes, the price of a site list nobody guessed.
The inventory stays on disk as the record of what moved and why, and T003 and
T004 inherit both the method and the file. REVERSE by deleting this section; the
rename it governs is not undone by that deletion, and D6 stands without it.
<<<END DECISIONR10>>>

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
`SESSION 4 of feature F272 · round 10`, the one-sentence context self-assessment
amend0905-throughput requires, branch, the range, a per-commit changed-files
table with real `+/-`, the item-status table covering C0a through C7 with every
item present exactly once, one line per gate G1 to G8 with its real exit code,
the G4 residual-probe and control readings, the G5 exit codes, the authored-text
proof table, deviations and the next expected action. Name every file C5 changed
beyond the seventeen listed above, each with the evidence that put it there. No
length cap. Per the fix clause OPEN in the record and binding on the next block
that orders a handback: any commit beyond the ordered sequence receives its OWN
`## Commits` row and its OWN item-status row, and the Deviations section says so
in those same words rather than beside a clause that denies it.
