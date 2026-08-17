── STEP T002b Restprüfung — F085 — R29 ───────────────────────────────────────

Goal: record the R28 PASS, register what the Restprüfung measured, and put that
measurement on disk in the inventory of record — how many of amendment F085 D1's
twelve `test`-class sites are on the shared seam today and exactly which ones are
not. No production code is touched: every path in the change set is under
`.agent/`.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record
R28 and register R-0519 · C2 plan · C3 inventory · C4 handback.

## Why this round exists — read before C1

R28 passed every gate it ordered. The reviewer re-ran all of them over
07b1ba25..b0d09db4, including its red proof in a fresh worktree, and every
reading reproduces.

The Restprüfung R28's own plan ordered has now been done, and it corrects the
picture rather than confirming it. `.agent/plan.md` had described T002b's
remainder as "the `test`-class sites still on a bare spawn, ending with
`test_execution_service.py`'s `Popen`". That sentence is true about `Popen`
specifically and misleading about the slice: `test_execution_service.py`:323 was
the last `Popen` in the class, not the last SITE. Five of the twelve are on the
seam — `autorun.py`:382, 510 and 563, `test_runner.py`:201 and
`test_execution_service.py`:323 — and seven are still on a bare spawn.

That makes the Fortschritt line R28's handback carries, `~85 %`, an overstatement
the class table contradicts, which is why R-0519 is registered here rather than
quietly corrected. The estimate is the operator's only progress signal and it was
authored by the reviewer.

## Change

C1 — `.agent/live_review.md`, one commit, RECORD1 appended and nothing else.
RECORD1 carries the R28 gate entry and then the R-0519 registration, as one slice.

C2 — `.agent/plan.md`, one commit, the PLANF→PLANT pair. The FROM spans the whole
`## Current Step` and `## Next Steps` region so the numbered list is rewritten by
the pair itself.

C3 — `.agent/f085_inventory.md`, one commit, the INVF→INVT pair. INVT keeps the
`### test — 12` heading and its site list byte-for-byte and adds a migration-state
paragraph beneath them, so the inventory's own numbering is untouched and the
measurement lands where a reader of that file will look for it.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the
   committed `.agent/authored/f085-r29.md` by its marker pair. Never retype a
   slice, and never apply one from the delegating prompt. Marker lines never
   reach a target file.
2. Pair shapes, each MEASURED by the reviewer with a containment test rather than
   read by eye, one reading per pair: PLANF→PLANT REWRITE · INVF→INVT
   APPEND-SHAPED, because INVT contains INVF verbatim and adds only text beneath
   it. INVF therefore takes the added-lines proof of G6 and never a whole-file
   "FROM 0x" count.
3. Re-read `.agent/STOP` from disk before C0a and again before C4. If it exists,
   finish the commit in flight, write the handback and stop.
4. `git status --porcelain` is empty at round start and after every commit. No
   destructive check is ordered this round, so `git worktree list` stays one line
   throughout; if you need one anyway it goes under `.remedy-wt/` and is removed
   and pruned before the handback.
5. C1 is an APPEND: the pre-commit file stays a byte-exact prefix and exactly one
   blank line separates it from RECORD1. Do not reflow, re-wrap or re-indent it.
6. Nothing outside the declared change set is touched. This round resolves no
   finding and registers R-0519 and no other, so the done set must come out
   unchanged.
7. If any gate comes out red, or a FROM does not match at exactly one place,
   STOP: write the handback naming the exact command, its exit code and its
   output, and do not improvise a repair.
8. STALENESS, standing: after C3 re-read every edited file and confirm that no
   sentence this round put on disk was falsified by a later commit of the same
   round, and that no slice quotes another file's current wording as a claim.
   Report the check by naming what was re-read.

## Done when

G1 STATE. `.agent/STOP` absent at the two points named in constraint 3;
`git status --porcelain` empty at round start and after every commit;
`git worktree list` one line at the handback.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r29.md`, the
committed `.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report
the sha256, the byte count, the line count, the number of marker lines, and
region digests over the line ranges 1-100, 101-200 and 201-end. Do not compute
any of those numbers by hand; measure them.

G3 APPEND SHAPE for C1. The pre-commit blob of `.agent/live_review.md` is a
byte-exact PREFIX of the post-commit file; the remainder is exactly one blank
line plus RECORD1; RECORD1's first line occurs once among the lines that commit's
diff ADDS; 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file — count
marker LINES, never the substring, because `APPEND-shaped` and the quoted regex
both already appear in that file's prose and a substring count reports them.
Report `git show --numstat` for that path.

G4 ARITHMETIC. Count the registered, done and landed id sets in
`.agent/live_review.md` at base b0d09db4 and at HEAD. The reviewer's base reading
is 133 registered / 15 done / 0 landed, 118 open, max R-0518; at HEAD it must be
134 / 15 / 0 with 119 open and max R-0519. Report the registered symmetric
difference (it must hold exactly R-0519), the done and landed symmetric
differences (both empty), the count of duplicate ids, the count of resolutions
naming an unregistered id, the maximum id and the next free id.

G5 PLAN PAIR. PLANF occurs 0 times at HEAD and PLANT exactly once. `## Goal` and
`## Risks` are byte-IDENTICAL to their base bytes. Report `.agent/plan.md`'s
sha256, its byte count, a line count under 50, and the numerals its `## Next
Steps` list parses to rather than a count of them.

G6 INVENTORY PAIR. INVF is append-shaped, so report that INVF occurs exactly once
in `.agent/f085_inventory.md` at HEAD, that INVT occurs exactly once, and that the
lines C3's diff ADDS contain the line `Migration state, measured at R29:` exactly
once. Also report that the file's `### test — 12` heading and the ten site lines
beneath it are byte-IDENTICAL to their base bytes.

G7 STATE READERS AND CANARY, because this round rewrites `.agent/` state:
`python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -rf -q` exits 0, base reading
`158 passed` — report the count as a READING and never as a target. RUN IT IN THE
PRIMARY CHECKOUT AND NEVER IN A WORKTREE: R-0518 records why, and a red naming
`TestVitestFrontendTestFoundation::test_vitest_passes` with `apps/ui/node_modules`
absent IS that finding rather than a regression. Any other red is a STOP under
constraint 7. CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` exits
0, base reading `42 passed`. No ruff gate and none skipped by oversight: the
change set contains no `.py` file. No docs gate: nothing under `docs/` changes.

G8 COMMIT HYGIENE. `git diff --name-only b0d09db4..HEAD` measured BEFORE C4 holds
exactly these paths and nothing else, named rather than counted:
`.agent/authored/f085-r29.md`, `.agent/f085_inventory.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md`. Report per-commit insertions for every
commit BEFORE C4 — C4 cannot measure itself, so report its own insertions in the
round report instead — and confirm none exceeds 500. Confirm every commit has
exactly one parent and that `git reflog -12` holds only `commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, branch, base SHA, a per-commit changed-files table, the item-status table
covering C0a, C0b, C1, C2, C3 and C4, the real verification results for G1-G8
with exit codes, the open-findings count, and the next expected action. Repeat
this Fortschritt line verbatim:
Fortschritt: ~60 % (T001 gebaut · R13-R28 PASS · T002a KOMPLETT · T002b 5 von 12
Sites auf dem Seam, 7 offen · T002c-d, T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

The handback MUST state, in its `## Next` section, that the next session's first
action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the
Open PR Gate (`gh pr list --state open --json
number,headRefName,baseRefName,isDraft`). It MUST also state that R-0519 is OPEN
and awaits the next reviewed round's authored resolution, that R29's own verdict
is NOT a §4.13 terminator because this branch continues, and that the next
reviewed round records R29's gate entry in `.agent/live_review.md`.

Then `git push -u origin feature/f085-sandbox-hardening`. Create no PR and merge
nothing.

BEGIN-RECORD1
Gate: R28 — PASS, the round that put `_run_isolated_process` on the seam's child
half and closed R-0517. Every ordered gate was re-run by the reviewer over
07b1ba25..b0d09db4 and each one reproduces the handback's reading. TRANSPORT WAS
PROVED AGAINST THE REVIEWER'S OWN ORIGINAL AND NOT ONLY AGAINST A DIGEST: the
scratch file the block was authored into, the committed
`.agent/authored/f085-r28.md`, the committed `.agent/last_block.md` and both
working copies are all five byte-EQUAL at sha256
c73bac4c5553f82312b5d38669bb33de3586a897f2ec7198f39c0b1399b406d0, 21848 B, 398
lines, 26 marker lines, region digests 3866a6a1, d15e4f7e and 4b8d681f. THE
APPEND COMMIT HOLDS ITS SHAPE: C1's pre-commit blob is a byte-exact PREFIX of the
post-commit file, the remainder is exactly one blank line plus RECORD1 at numstat
71/0, RECORD1's first line occurs once among the 71 lines that commit adds, and 0
lines match `^(BEGIN|END)-[A-Z0-9]+$` while the substring `END-` hits seven times
— five older than that round and two added by RECORD1's own prose, which quotes
the regex and the word `APPEND-shaped`. A line-anchored count reports the
property; a substring count reports the prose. THE ARITHMETIC MOVED IN BOTH SETS
AT ONCE WHILE THE OPEN COUNT STAYED FLAT: 133 registered / 15 done / 0 landed at
HEAD against 132 / 14 / 0 at base, 118 open at both ends, registered symmetric
difference exactly R-0518, done symmetric difference exactly R-0517, landed
empty, no duplicate id, no resolution naming an unregistered id, max R-0518 and
next free R-0519. A flat open count across a round that both registers and
resolves is the arithmetic working, not the arithmetic standing still. THE
MIGRATION TOOK THE CHILD HALF AND LEFT THE PARENT HALF ALONE: S1F through S4F
occur 0 times at HEAD and each TO exactly once, the new test's `def` line occurs
once among the lines C3 adds, `def test_no_shell_true(self):` still occurs
exactly once in the file, and no marker line reached any target. The source
guards over `_run_isolated_process` still hold, because the migration kept
`subprocess.Popen(`, `start_new_session=True` and `DEVNULL` inside the function
and added no `subprocess.run(`. THE PROOF IS A REAL CHILD AND THE REVIEWER BROKE
IT INDEPENDENTLY: at HEAD the new node passes, and in a disposable worktree at
HEAD with the single line `preexec_fn=plan.preexec_fn,` deleted it FAILS, then
passes again once restored. The reviewer ran that recipe itself rather than
reading the worker's transcript, and the parent's own RLIMIT_CORE of (0, -1) is
what makes the child's (0, 0) an observation rather than a tautology. THE GATES
WERE RE-RUN, NOT READ: the round gate exited 0 with `98 passed` against a base of
`97 passed` the reviewer measured before the block was written, ruff over both
changed files `All checks passed!`, the four state readers `158 passed` and the
canary `42 passed`, each as its exact ordered command line. COMMIT HYGIENE IS
CLEAN: the path set is the six declared paths, per-commit insertions are 398,
334, 71, 8 and 39 with the handback's own 84 measured after it existed and none
over 500, the range is a single-parent chain, and the reflog holds only `commit:`
entries. The handback is 125 lines against the 100 a round with more than five
per-commit tables may carry; the overage is declared, names its own measured
length and names the mandated content that caused it. R-0202 is correctly still
OPEN: the migration passes the caller's already-scrubbed `env` through unchanged,
so the variable that finding names is dropped after this round by the same code
as before it. No block condition is met.

- R-0519 — Low, A PROGRESS ESTIMATE THE REVIEWER AUTHORED OVERSTATED A SLICE THE
CLASS TABLE CAN MEASURE. R28's handback carries `Fortschritt: ~85 %`, and the plan
it inherited described T002b's remainder as the `test`-class sites "ending with
`test_execution_service.py`'s `Popen`". Measured against amendment F085 D1's class
table, five of the twelve `test`-class sites are on the shared seam and seven are
not. `test_execution_service.py`:323 was the last `Popen` of the class, not its
last SITE, and the plan sentence conflated the two — which is how an estimate
built on it reached 85 % for a slice that is under half migrated. The criterion
used, so it can be re-checked: a site is ON THE SEAM when its spawn takes cwd,
env and the fork-to-exec hook from `exec_guard`, through either
`run_guarded_test_command` or `plan_child_spawn`; each of the seven remaining
files contains no reference to either symbol. Low because nothing executable
depends on the number and no gate could go red over it. It is registered rather
than corrected in silence because the Fortschritt line is the operator's only
progress signal, it is authored by the reviewer, and
docs/agents/planner_reviewer_prompt.md §2 requires it to be honest and labelled an
estimate. The counter-measure ships in this same round: C3 writes the migration
state into `.agent/f085_inventory.md` directly beneath the class list that defines
the set, so the next estimate is derived from the file that fixes the denominator
rather than from the previous estimate. OPEN.
END-RECORD1

BEGIN-PLANF
## Current Step
R28, this round: record the R27 PASS, resolve R-0517, and put
`test_execution_service._run_isolated_process` on the seam's CHILD half via
`plan_child_spawn`, keeping its own wait deadline, its process-group kill and its
file-backed streams where they are. R-0202 stays open: the environment the child
receives is unchanged by this round.

## Next Steps
1. T002b Restprüfung — re-derive the `test`-class site set from
   `.agent/f085_inventory.md` against amendment F085 D1's twelve, and name every
   site still on a bare spawn before T002b is called finished.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.
END-PLANF

BEGIN-PLANT
## Current Step
R29, this round: record the R28 PASS and register R-0519. The T002b Restprüfung
found five of the twelve `test`-class sites on the seam and seven still on a bare
spawn, which the previous Fortschritt overstated; the measurement lands in
`.agent/f085_inventory.md` beneath the class list that defines the set.

## Next Steps
1. T002b continued — the seven `test`-class sites still on a bare spawn:
   `builder_bridge.py`:220, `ci_run.py`:79, `integrity_gate.py`:283,
   `job_promote.py`:417, `mission_state.py`:833, `pingpong_loop.py`:3537 and
   `pingpong_promote.py`:326. Take them in small groups, one order per group.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.
END-PLANT

BEGIN-INVF
### test — 12
- `packages/orchestration/autorun.py`:382, 510, 563
- `packages/orchestration/builder_bridge.py`:220
- `packages/orchestration/ci_run.py`:79
- `packages/orchestration/integrity_gate.py`:283
- `packages/orchestration/job_promote.py`:417
- `packages/orchestration/mission_state.py`:833
- `packages/orchestration/pingpong_loop.py`:3537
- `packages/orchestration/pingpong_promote.py`:326
- `packages/orchestration/test_execution_service.py`:323
- `packages/orchestration/test_runner.py`:201
END-INVF

BEGIN-INVT
### test — 12
- `packages/orchestration/autorun.py`:382, 510, 563
- `packages/orchestration/builder_bridge.py`:220
- `packages/orchestration/ci_run.py`:79
- `packages/orchestration/integrity_gate.py`:283
- `packages/orchestration/job_promote.py`:417
- `packages/orchestration/mission_state.py`:833
- `packages/orchestration/pingpong_loop.py`:3537
- `packages/orchestration/pingpong_promote.py`:326
- `packages/orchestration/test_execution_service.py`:323
- `packages/orchestration/test_runner.py`:201

Migration state, measured at R29:
A site is ON THE SEAM when its spawn takes cwd, env and the fork-to-exec hook
from `exec_guard`, through either `run_guarded_test_command` or
`plan_child_spawn`. ON THE SEAM: `autorun.py` (all three, R26) and
`test_runner.py`, both through `run_guarded_test_command`, and
`test_execution_service.py` through `plan_child_spawn`'s child half at R28 —
child half only, because that site writes its output into a file handle and
returns a positional tuple, so the parent half cannot move. NOT YET:
`builder_bridge.py`, `ci_run.py`, `integrity_gate.py`, `job_promote.py`,
`mission_state.py`, `pingpong_loop.py` and `pingpong_promote.py`, none of which
references either symbol. The line numbers above are this inventory's original
R2 coordinates and were NOT re-measured for this paragraph; the migration state
was measured per FILE, by the symbols each one references. `job_promote.py` and
`integrity_gate.py` also hold spawns of other classes, which this paragraph does
not count.
END-INVT
