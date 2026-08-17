── STEP T002b unblock ruling — F085 — R38 ────────────────────────────────────

Goal: record the R37 PASS, register R-0528 and R-0529, and rule how the `test`-class
seam will let a call site SET an environment variable — the one capability BOTH
remaining T002b sites need. This round writes the ruling and the plan; R39 writes the
code it authorises.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record R37
and register R-0528 and R-0529 · C2 the DECISION and the plan · C3 handback.

## Change

C1 appends RECORD6 to `.agent/live_review.md` and nothing else. C2 appends DEC6 to
`.agent/decisions.md` and applies the two `.agent/plan.md` pairs, in one commit: the
ruling and the re-ordering it causes are one step.

Change set, named rather than counted: `.agent/authored/f085-r38.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`
and `.agent/handoff.md`. Nothing else. No production file and no file under `docs/`
changes, so this round orders no ruff run, no `tests/docs/` gate and no red proof.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r38.md` by its marker pair. Never retype one, never apply one
   from the prompt. Marker lines never reach a target file.
2. Pair shapes, each MEASURED by the reviewer with a containment test and recorded as
   the test's OUTPUT, one reading per pair — PLANF6A→PLANT6A and PLANF6B→PLANT6B each
   read `TO contains FROM: false`, so each is a REWRITE and each is owed the
   FROM 0x / TO 1x reading. Each FROM was measured to occur exactly 1x in `.agent/plan.md`
   at c3201976. RECORD6 and DEC6 are appends and carry no FROM.
3. Re-read `.agent/STOP` from disk before C0a and again before C3. If it exists, finish
   the commit in flight, write the handback and stop.
4. `git status --porcelain` is empty at round start and after every commit. This round
   orders no destructive check, so it creates no worktree; `git worktree list` is one
   line throughout.
5. C1 and C2's DEC6 half are APPENDS: each pre-commit file stays a byte-exact prefix,
   exactly one blank line joins it to the slice, and neither is reflowed, re-wrapped or
   re-indented.
6. Nothing outside the declared change set is touched. This round registers R-0528 and
   R-0529 and resolves nothing, so the open count moves from 118 to 120.
7. If any gate comes out red, or a FROM does not match at exactly one place in its
   target, STOP: write the handback naming the exact command, its exit code and its
   output, and do not improvise a repair.
8. STALENESS, standing: after C2 re-read every file this round edited and confirm no
   sentence this round put on disk was falsified by a later commit of the same round,
   and that no slice quotes another file's current wording as a claim. Name what was
   re-read and report the measurement, not a restatement of this sentence. This
   constraint states no property of any slice's contents.
9. Do not "repair" any landed text. The sentences R-0528 and R-0529 register stay in
   the commits holding them; the registration IS the correction — the R-0521 principle.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 3; `git status
--porcelain` empty at round start and after every commit; `git worktree list` one line
throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r38.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the
reviewer's own `.remedy-wt/f085-r38.md` — disk-to-disk, not a digest fallback. Report
the sha256, byte count, line count, marker-line count and region digests over lines
1-100, 101-200, 201-300 and 301-end, each taken with trailing newlines included.
Measure every one of those; compute none by hand.

G3 APPEND SHAPE, for C1 on `.agent/live_review.md` and C2 on `.agent/decisions.md`. For
each: the pre-commit blob is a byte-exact PREFIX of the post-commit file; the remainder
is exactly one blank line plus the slice; the slice is an exact suffix; the slice's
first line occurs once among the lines that commit's diff ADDS; 0 lines matching
`^(BEGIN|END)-[A-Z0-9]+$` land in the file — count marker LINES, never the substring,
because the quoted regex already appears in that file's prose. Report
`git show --numstat` for each path.

G4 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md`
at base c3201976 and at HEAD, from `^- R-\d{4} — `, `^Done: R-\d{4} — ` and
`^Landed: R-\d{4}`. The reviewer's base reading is 142 / 24 / 0, 118 open, max
registered R-0527, max resolved R-0527; at HEAD it must be 144 / 24 / 0, 120 open, max
registered R-0529, max resolved R-0527. Report the registered symmetric difference
(exactly R-0528 and R-0529), the done and landed symmetric differences (both empty),
the duplicate-id count, the count of resolutions naming an unregistered id, the maximum
id, and the next free id, which moves from R-0528 to R-0530.

G5 THE PLAN, measured at HEAD after C2: each plan FROM occurs 0x and each plan TO 1x;
`.agent/plan.md` stays under the 50-line AGENTS.md cap and still carries `## Goal` and
`## Next Steps`; 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` reached it. Report
`git show --numstat` for C2.

G6 SUITES, each run in the PRIMARY checkout and never in a worktree (R-0518), each as
its exact command line, each exit 0. Both base readings were taken by the reviewer at
c3201976:
- `python3 -m pytest tests/orchestration/test_test_runner.py
  tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
  tests/ui_server/test_dashboard_contract.py -rf -q` — the four files that read
  `.agent/` state live; base reading `159 passed`. A red naming
  `TestVitestFrontendTestFoundation::test_vitest_passes` with `apps/ui/node_modules`
  absent IS finding R-0518 and means the command ran in a worktree; re-run it in the
  primary checkout. Any other red is a STOP under constraint 7.
- CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base reading
  `42 passed`.

G7 HYGIENE. `git diff --name-only c3201976..HEAD` measured BEFORE C3 holds exactly the
change set above minus `.agent/handoff.md`, which C3 writes, and nothing else. Report
per-commit insertions for every commit BEFORE C3 — C3 cannot measure itself, so its own
insertions go in the round report — and confirm none exceeds 500. Confirm every commit
has exactly one parent and that `git reflog -10` holds only `commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round,
branch, base SHA c3201976, a per-commit changed-files table, the item-status table
covering C0a, C0b, C1, C2 and C3, the real G1-G7 results with exit codes, the
open-findings count and the next expected action. In `## Authored-text proofs` report
each pair under the shape constraint 2 assigns it. Repeat this Fortschritt line
verbatim:
Fortschritt: ~74 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R37
PASS · T002a KOMPLETT · T002b 10 von 12 Sites auf dem Seam, die letzten 2 durch
DECISION F085 D3 ab R39 entsperrt · T002c-d, T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section MUST state that the next session's FIRST action is Phase 1 rule 1
— re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR Gate (`gh pr list
--state open --json number,headRefName,baseRefName,isDraft`); that R38's own verdict is
NOT a §4.13 terminator because this branch continues; and that the next reviewed round
records R38's gate entry. It MUST also carry this note verbatim:

  R39 implements DECISION F085 D3 in `packages/orchestration/exec_guard.py`: an
  `extra_env` mapping on `test_command_exec_policy` and `run_guarded_test_command`
  whose entries become the scrub SOURCE overlay and whose keys join the allowlist,
  with `scrub_child_env` keeping `FORBIDDEN_ENV_KEYS` as the floor, plus the tests
  that pin the set, the floor and the untouched allowlist. No call site is migrated
  in R39. R40 then migrates `packages/orchestration/ci_run.py`, which still owes its
  own DECISION on where the stage's output goes: at c3201976 the spawn at line 79
  streams straight to the console while the seam captures.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-RECORD6
Gate: R38 — the R37 entry. R37 PASSED. Every ordered gate was re-run by the reviewer
over 483975b3..c3201976 and each reproduces the handback's reading. TRANSPORT WAS PROVED
DISK-TO-DISK: the committed `.agent/authored/f085-r37.md`, the committed
`.agent/last_block.md` at 857ca31a and both working copies are byte-EQUAL at sha256
c8efc5c06444464245a311d03acc78f008246a9c259a7100330bdeac876d8409, 21768 B, 329 lines, 10
marker lines, region digests 70737984, 9bdbc476 and 89541ee6. THE APPEND COMMIT HELD ITS
SHAPE: 75feb987's pre-commit blob 391135 B is a byte-exact PREFIX of the 397527 B
post-commit file, the remainder 6392 B is one blank line plus RECORD5, RECORD5 is an
exact suffix, its first line occurs once among the 81 lines that commit adds, numstat
81/0, and 0 lines match `^(BEGIN|END)-[A-Z0-9]+$` while the BEGIN substring occurs 15
times. THE ARITHMETIC MOVED AS ORDERED: 141 / 22 / 0 at 483975b3 against 142 / 24 / 0 at
c3201976, 119 open against 118, registered symmetric difference exactly R-0527, done
symmetric difference exactly R-0526 and R-0527, landed symmetric difference empty, no
duplicate id, no resolution naming an unregistered id, next free R-0528. THE CLAUSE
LANDED AND BOTH PAIRS WERE APPLIED VERBATIM: at c3201976 the I11F text occurs once, the
item-11, item-12 and closing-paragraph openers each occur once, all 19 TO-only lines
occur exactly once among the 19 lines 69155e06 adds, numstat 19/0, and the reviewer
reproduced both applications mechanically — each pre-commit blob with its FROM replaced
once by its TO equals the post-commit blob byte for byte, for I11F→I11T and PLANF5→PLANT5
alike. THE SUITES WERE RE-RUN, NOT READ: the four state readers `159 passed`,
`tests/docs/` `295 passed` and the canary `42 passed`, each as its exact ordered command
line in the primary checkout, each exit 0. HYGIENE IS CLEAN: the path set is the six
declared paths, per-commit insertions are 329, 264, 19, 81, 3 and the handback's own 42,
none over 500, all six commits are single-parent, the reflog holds only `commit:`
entries, the handback is 94 lines against its 100-line cap, and origin and local agree at
c3201976.

WHAT THE WORKER FOUND AND DID NOT TOUCH. Under constraint 8 R37's worker measured the
reviewer's own constraint against the slice it described, found both halves false,
declared it, and changed nothing — the third consecutive round in which the constraint-8
report produced the round's finding.

- R-0528 — Low, A BLOCK CONSTRAINT ASSERTED TWO PROPERTIES OF ITS OWN TEXT AND BOTH ARE
FALSE. Constraint 8 of the R37 block, applied at commits e2b23b33 and 857ca31a, states
that "The only file this block both edits and makes claims about is
`docs/agents/planner_reviewer_prompt.md`" and that "Every other reading RECORD5 asserts
about a state before this round names 483975b3 or an earlier SHA". Measured against
RECORD5 at c3201976, both fail. RECORD5 makes claims about three files that round edits,
not one: `docs/agents/planner_reviewer_prompt.md`, `.agent/last_block.md` and
`.agent/live_review.md`. And RECORD5's transport sentence names no SHA at all — its three
8-hex tokens 7d583ed0, ace9d813 and 9b5a9653 are region content digests and resolve to no
git object — while asserting a reading of `.agent/last_block.md` that the same round's
C0b, commit 857ca31a, falsified: that file hashes 208ad9d3 at 483975b3 and c8efc5c0 at
857ca31a and every commit after it. `.agent/last_block.md` is on
the R-0525 list of paths this workflow rewrites every round, so that sentence was owed a
SHA by a rule already on disk. This is the R-0527 shape recurring inside the very
constraint written to close R-0527, one commit before the item-11 clause forbidding it
landed. Found by the worker under constraint 8 and registered by the reviewer.

- R-0529 — Low, THE RESOLUTION THAT CLOSED R-0527 IS ITSELF AN INSTANCE OF R-0527. The
`Done: R-0527` paragraph, applied at commit 75feb987, closes with "The block that carries
this resolution applies it to itself — its constraint 8 names the one file this block
both edits and makes claims about, and asserts no property of any slice's contents."
Measured at c3201976 both halves are false, by the same readings R-0528 records: the
constraint names one file where RECORD5 claims about three, and the constraint DOES
assert a property of a slice's contents — the sentence binding every reading RECORD5
makes to name 483975b3 or earlier, which is the half the transport sentence breaks. What
separates this from R-0528 is where it landed. R-0528's text sits in a block record; this
one sits in `.agent/live_review.md`, the permanent findings register, inside the paragraph
certifying R-0527 closed — so the register now asserts a compliance nobody measured, in
the one document whose whole purpose is that its claims are measured. R37's handback
declared the constraint and did not name this second landing site, which is why it needs
an id of its own rather than a sentence inside R-0528. Per constraint 9 nothing is
rewritten: this registration is the correction.
END-RECORD6


BEGIN-DEC6
## DECISION F085 D3 — the `test`-class seam gains an `extra_env` overlay (2026-08-17)

Ruled by the reviewer at the R38 gate under docs/agents/planner_reviewer_prompt.md §4
item 7. R38 records the ruling; R39 applies it in code, and no call site migrates in
either. Reverse it before R39 by deleting this section, or after R39 by dropping the
`extra_env` parameter from `test_command_exec_policy` and `run_guarded_test_command`
and restoring `env=None`; the seam then returns to passing keys through and setting
none.

CONTEXT, measured at c3201976. Two of the twelve `test`-class sites are still on a bare
spawn, and both build their child environment the same way: `ci_run.py` line 78 overlays
`PYTEST_TIMEOUT_ENV_VAR` onto a copy of `os.environ` so each CI stage gets its own
budget, and `builder_bridge.py` line 219 overlays `PYTHONDONTWRITEBYTECODE`. The seam
offered only `extra_env_keys`, which widens the allowlist while the scrub SOURCE stays
`os.environ`, so a key the parent lacks reaches the child absent. `.agent/plan.md` at
c3201976 recorded this blocker for `builder_bridge.py` alone; it belongs to both.

CHOSEN: an `extra_env` mapping whose entries become the scrub SOURCE overlay and whose
keys join the allowlist for that call only. `scrub_child_env` keeps `FORBIDDEN_ENV_KEYS`
as the floor, so the knob cannot smuggle a secret past it, and a test pins that.

ALTERNATIVES CONSIDERED AND REJECTED: adding the two variables to
`TEST_COMMAND_ENV_ALLOWLIST`, rejected because passing a key through is not setting it —
the parent does not hold the per-stage value, and a shared allowlist is the wrong home
for one caller's variable; having each site export the variable into its own process
before spawning, rejected because that mutates the parent's environment for every
concurrent caller and outlives the call; leaving both sites unmigrated and naming them in
T003's limitations document, rejected because Amendment F085 D1's class table puts the
whole `test` class under stage-1 containment and two unguarded sites would make that row
false.

CONSEQUENCE, stated plainly rather than minimised: once R39 lands this, a caller can SET
any variable not in `FORBIDDEN_ENV_KEYS`, which is strictly more power than passing one
through, and the guard's floor is the only thing keeping that honest — so R39 owes a test
that a forbidden key handed to `extra_env` still does not reach the child. The knob
changes nothing for a caller that does not pass it: the default is `None` and the policy
stays byte-identical to today's.
END-DEC6


BEGIN-PLANF6A
## Current Step
R37, this round: record the R36 PASS, register R-0527, and resolve R-0526 and R-0527
with one checklist clause — a claim a block or a slice makes about its own text is
measured before emission. No production code changes.
END-PLANF6A


BEGIN-PLANT6A
## Current Step
R38, this round: record the R37 PASS, register R-0528 and R-0529, and give the
`test`-class seam an `extra_env` overlay so a call site can SET a variable — the one
capability both remaining T002b sites need. No call site is migrated.
END-PLANT6A


BEGIN-PLANF6B
1. T002b remainder — the two `test`-class sites still on a bare spawn, in this order.
   `ci_run.py` next: at 23b5fcd9 its only spawn streams to the console and passes no
   timeout, so moving it onto the capturing seam changes observable behaviour and the
   round that does it records where the output goes as a DECISION.
   `builder_bridge.py` comes LAST and is BLOCKED until the seam
   can SET an environment value: it puts `PYTHONDONTWRITEBYTECODE` on a full
   `os.environ` copy, while `run_guarded_test_command` only allowlists keys that
   the parent already has, so migrating it as-is would silently stop that variable
   reaching the child. One or two per order, never as one group.
END-PLANF6B


BEGIN-PLANT6B
1. T002b remainder — the two `test`-class sites still on a bare spawn. At c3201976 BOTH
   overlay one variable onto a copy of `os.environ`, so both were blocked on the same
   missing capability rather than `builder_bridge.py` alone: `ci_run.py` sets the
   per-stage pytest budget, `builder_bridge.py` sets `PYTHONDONTWRITEBYTECODE`. R38's
   `extra_env` overlay unblocks both (DECISION F085 D3). `ci_run.py` still goes first
   and still owes a DECISION on where its output goes: its spawn streams to the console
   while the seam captures, so that migration changes observable behaviour rather than
   preserving it. One or two per order, never as one group.
END-PLANT6B
