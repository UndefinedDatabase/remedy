── STEP T002b decision — F085 — R42 ──────────────────────────────────────────

Goal: record the R41 PASS, register R-0535 and R-0536 — two defects in the reviewer's own
RECORD9 and R41 block text that R41's worker measured — and rule DECISION F085 D4, the
measured design for the `ci_run.py` migration, so R43 applies a settled design instead of
discovering it mid-round. No production code changes.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record R41 and
register R-0535 and R-0536 · C2 rule DECISION F085 D4 · C3 the plan · C4 handback.

CONVENTION, stated once and binding on every count in this block: a line count is the
`splitlines` reading — the number of lines in the text, with a trailing newline NOT
counted as an extra line. R-0536, registered by this round, is what an unstated convention
already cost.

## Change

C1 appends RECORD10 to `.agent/live_review.md` and nothing else. C2 appends DEC4 to
`.agent/decisions.md` and nothing else. C3 applies the plan pair, which spans the Current
Step block and Next Steps item 1 together because both make claims this round changes;
Next Steps items 2 and 3 and the Risks section are untouched.

Change set, named rather than counted: `.agent/authored/f085-r42.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`
and `.agent/handoff.md`. Nothing else. No production file changes and no `.py` file
changes, so this round orders no ruff run and no red proof.

Neither `docs/**` nor `docs/roadmap/**` is in that set, so no docs tier triggers. The
reviewer grepped the suite for readers of `.agent/decisions.md`: the only match,
`tests/orchestration/test_evidence_index.py`, writes its own `decisions.md` inside a
temporary git repo and asserts nothing about the real file's content. That is why C2's
gate is the append shape rather than a suite.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r42.md` by its marker pair. Never retype one, never apply one from
   the prompt. Marker lines never reach a target file.
2. Pair shape, MEASURED by the reviewer with a containment test and recorded here as that
   test's OUTPUT: PLANF10→PLANT10 reads `TO contains FROM: false`, so it is a REWRITE and
   is owed the FROM 0x / TO 1x reading. PLANF10 was measured to occur exactly 1x in
   `.agent/plan.md` at 0e2cdacd. RECORD10 and DEC4 are appends and carry no FROM.
3. Re-read `.agent/STOP` from disk before C0a and again before C4. If it exists, finish the
   commit in flight, write the handback and stop.
4. `git status --porcelain` is empty at round start and after every commit. This round
   orders no destructive check, so it creates no worktree; `git worktree list` is one line
   throughout.
5. C1 and C2 are APPENDS: for each, the pre-commit file stays a byte-exact prefix, exactly
   one blank line joins it to the slice, and the slice is not reflowed, re-wrapped or
   re-indented.
6. Nothing outside the declared change set is touched. This round registers R-0535 and
   R-0536 and resolves nothing, so the open count moves from 122 to 124.
7. If a gate comes out red, or PLANF10 does not match at exactly one place, STOP: write the
   handback naming the exact command, its exit code and its output, and do not improvise a
   repair.
8. STALENESS, standing: after C3 re-read every file this round edited and confirm no
   sentence this round put on disk was falsified by a later commit of the same round, and
   that no slice quotes another file's current wording as a claim. Name what was re-read
   and report the measurement, not a restatement of this sentence. Give special attention
   to any trailing reading whose clause qualifies an EARLIER reading with a SHA — that is
   exactly the R-0534 and R-0535 shape, and it has now landed in two consecutive rounds.
9. Do not "repair" any landed text. The clauses R-0535 and R-0536 register stay in commits
   1a29a77d and 9cc4772c. The registration IS the correction — checklist item 20.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 3; `git status --porcelain`
empty at round start and after every commit; `git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r42.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the
reviewer's own `.remedy-wt/f085-r42.md` — disk-to-disk, not a digest fallback. Report the
sha256, byte count, line count, marker-line count, and region digests over lines 1-100 and
101-end, each taken with trailing newlines included and reported with its own byte count so
an empty region is visible as empty. Measure every one; compute none by hand.

G3 APPEND SHAPE for C1 on `.agent/live_review.md` and for C2 on `.agent/decisions.md`,
reported separately for each. For each: the pre-commit blob is a byte-exact PREFIX of the
post-commit file; the remainder is exactly one blank line plus the slice; the slice is an
exact suffix; 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file — count marker
LINES, never the substring, because that regex already appears in `.agent/live_review.md`
prose. Both slices are PROSE, so the §4.9 per-line obligation applies to each and is
ordered: every line the slice contains occurs exactly once among the lines its own commit's
diff adds, EXCEPT the empty line, which is exempt because a paragraph break repeats by
construction — report how many empty lines each slice holds rather than counting them as
failures. The reviewer measured both slices to hold no duplicate non-empty line, so a
violation is a transport fault rather than a property of the text. Report
`git show --numstat` for each path.

G4 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at
base 0e2cdacd and at HEAD, from the line-start patterns for a registration, a resolution
and a landed line. The reviewer's base reading is 149 / 27 / 0, 122 open, max registered
R-0534, max resolved R-0532. At HEAD it must be 151 / 27 / 0, 124 open, max registered
R-0536, max resolved R-0532. Report the registered symmetric difference (exactly R-0535 and
R-0536), the done and landed symmetric differences (both empty), the duplicate-id count,
the count of resolutions naming an unregistered id, and the next free id, which moves from
R-0535 to R-0537.

G5 THE DECISION at HEAD after C2: `.agent/decisions.md` contains exactly one line beginning
`## DECISION F085 D4 —`, and the number of lines matching `^## DECISION F085 D\d+ —` is 3
— D2, D3 and D4, each exactly once — against 2 at the base. There is deliberately NO D1
section in that file: F085 D1 is an operator AMENDMENT recorded in the feature file rather
than a reviewer decision, and `.agent/decisions.md` at 0e2cdacd names it only in prose, so
a gate expecting D1 through D4 here would be unmeetable. Report the three heading lines
themselves rather than only the count.

G6 THE PLAN at HEAD after C3: PLANF10 occurs 0x and PLANT10 1x; `.agent/plan.md` stays
under the 50-line AGENTS.md cap and still carries `## Goal` and `## Next Steps`; 0 lines
matching `^(BEGIN|END)-[A-Z0-9]+$` reached it. The reviewer's dry run put it at 45 lines on
the convention stated at the top of this block. Report `git show --numstat` for C3.

G7 SUITES, each run in the PRIMARY checkout and never in a worktree (R-0518), each as its
exact command line, each exit 0. Both base readings were taken by the reviewer at 0e2cdacd:
- `python3 -m pytest tests/orchestration/test_test_runner.py
  tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
  tests/ui_server/test_dashboard_contract.py -rf -q` — the four files that read `.agent/`
  state live; base reading `159 passed`. A red naming
  `TestVitestFrontendTestFoundation::test_vitest_passes` with `apps/ui/node_modules` absent
  IS finding R-0518 and means the command ran in a worktree; re-run it in the primary
  checkout. Any other red is a STOP under constraint 7.
- CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base reading `42 passed`.

G8 HYGIENE. `git diff --name-only 0e2cdacd..HEAD` measured BEFORE C4 holds exactly the
change set above minus `.agent/handoff.md`, which C4 writes, and nothing else. Report
per-commit insertions for every commit BEFORE C4 — C4 cannot measure itself, so its own
insertions go in the round report — and confirm none exceeds 500. Confirm every commit has
exactly one parent and that `git reflog -10` holds only `commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch,
base SHA 0e2cdacd, a per-commit changed-files table, the item-status table covering C0a,
C0b, C1, C2, C3 and C4, the real G1-G8 results with exit codes, the open-findings count and
the next expected action. Repeat this Fortschritt line verbatim:
Fortschritt: ~77 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R41 PASS
· T002a KOMPLETT · T002b 10 von 12 Sites auf dem Seam, Design für ci_run.py als DECISION
F085 D4 gerulet, R43 setzt es um · T002c-d, T003 offen) — Schätzung, gegen die
Klassentabelle aus Amendment F085 D1 gemessen.

This handback closes a SESSION, not only a round. Keep it inside the 60-line cap, or name
the DECISION D15 stated cause and the exact mandated content behind it.

The `## Next` section MUST state that the next session's FIRST action is Phase 1 rule 1 —
re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR Gate (`gh pr list --state open
--json number,headRefName,baseRefName,isDraft`); that R42's own verdict is NOT a §4.13
terminator because this branch continues; and that the next reviewed round records R42's
gate entry. It MUST also carry this note verbatim:

  R43 applies DECISION F085 D4 to `packages/orchestration/ci_run.py`: `_run_via_subprocess`
  moves onto `run_guarded_test_command`, the per-stage budget travels through the
  `extra_env` overlay that landed at dce66faa, the captured stdout and stderr are re-emitted
  to the console before returning, and the guard's wall is set ABOVE `stage.timeout_sec` as
  a backstop so the child's own 124 exit code stays the operative timeout. D4 leaves the
  size of that grace margin to R43 and says why. R43 owes three tests it does not have
  today: that the captured output reaches the console, that the budget still arrives in the
  child, and that a wall trip maps to the `timed out` note.
  `packages/orchestration/builder_bridge.py` follows; then T002c-d, then T003 and the
  integration gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-RECORD10
Gate: R42 — the R41 entry. R41 PASSED. Every ordered gate was re-run by the reviewer over
93226220..0e2cdacd and each reproduces the handback's reading. LINE COUNTS IN THIS ENTRY
ARE `splitlines` COUNTS, stated because the convention is exactly what R-0536 below
registers. TRANSPORT WAS PROVED AGAINST THE REVIEWER'S OWN ORIGINAL: the scratch file the
block was authored into, the committed `.agent/authored/f085-r41.md` at 9cc4772c, the
committed `.agent/last_block.md` at a66aa301 and the working copies of those two paths as
they stand at 0e2cdacd are all five byte-EQUAL at sha256
a3716bdf9fa29892bbb6220a5b50bf6c73b057106e0465a28d71e3cd17febbba, 28265 B, 398 lines, 14
marker lines. THE APPEND HELD ITS SHAPE: 1a29a77d's pre-commit blob of 412143 B is a
byte-exact PREFIX of the 420193 B post-commit file, the remainder of 8050 B is one blank
line plus RECORD9, RECORD9 hashes cf21f13adb1535b6 over 8049 B and 101 lines and is an
exact suffix, the appended bytes equal the marker-pair extraction from the committed
authored block, numstat 102/0, no duplicate non-empty line among the 102 added, and no
marker line reached the file. THE ARITHMETIC MOVED AS ORDERED: 147 / 24 / 0 at 93226220
against 149 / 27 / 0 at 0e2cdacd, 123 open against 122, registered symmetric difference
exactly R-0533 and R-0534, done symmetric difference exactly R-0530, R-0531 and R-0532,
landed symmetric difference empty, no duplicate id, no resolution naming an unregistered
id. THE DOC EDITS LANDED AS TWO APPENDS: P49FROM, P49TO, CL20FROM and CL20TO each occur
exactly 1x at 0e2cdacd, and for BOTH commits the lines the diff adds equal the TO-only
lines IN ORDER — 14 for 01359f81 and 49 for 247df04b — which is the ordered-equality
reading item 9 of §4 now prescribes, applied to its own landing commit. The checklist
region reads labels 1..22 contiguous against 1..20 at the base; no marker line reached the
file. THE PLAN PAIR LANDED AS A REWRITE: PLANF9 0x and PLANT9 1x at 0e2cdacd, `## Goal`
and `## Next Steps` both present, no marker line, numstat 4/3. THE SUITES WERE RE-RUN, NOT
READ, each in the primary checkout, each exit 0: the four state readers `159 passed`
against a base of 159, and the canary `42 passed` against 42. HYGIENE IS CLEAN: the path
set before C5 is exactly the five ordered paths; walking 93226220..0e2cdacd gives
per-commit insertions 398, 361, 102, 14, 49, 4 and the handback commit's own 101, none
over 500; all seven commits are single-parent; `git reflog -10` holds only `commit:`
entries; and `git worktree list` is one line.

WHAT THE WORKER FOUND AND DID NOT TOUCH. Under constraints 8 and 9 R41's worker measured
the reviewer's own RECORD9 and the block's own predictions against the repository, found
five readings that differ, declared them and repaired none. That is the seventh
consecutive round in which the constraint-8 report produced the round's findings. The two
findings below are the reviewer's, not the worker's: R41's execution reproduced under
independent re-run in every particular.

- R-0535 — Low, THE CLAUSE THAT LANDED THE QUALIFIER RULE BROKE IT TWICE IN ITS OWN TEXT.
RECORD9, applied at commit 1a29a77d, registers R-0534 and states its counter-measure —
that a SHA qualifier attaches to EVERY reading a clause states, not only the first — and
two of RECORD9's own clauses then state a trailing reading the qualifier does not reach.
Measured: its plan clause reads "PLANF8 0x and PLANT8 1x at 93226220, `.agent/plan.md` 45
lines", and `.agent/plan.md` is 45 lines at 93226220 and at 1a29a77d but 46 at 0e2cdacd,
falsified by C4 of RECORD9's own round; its arithmetic clause closes "next free R-0533",
which is true at 93226220 and false at 1a29a77d, because RECORD9 itself registers R-0533
and R-0534 and so moves the next free id to R-0535 in the very commit that lands the
sentence. The second is the sharper of the two: no reading of the qualifier's scope makes
it true where it landed. What this is NOT is a worker error or a rule that failed — the
R41 block was authored BEFORE checklist item 20 carried the R-0534 clause, and constraint
6 put C1 ahead of C3, so RECORD9 was written under the old rule and landed under the new
one. The lesson is narrower and worth the id: a round that WRITES a checklist rule must
apply that rule to its own slices at authoring time, because the slices land in the same
round and the record does not care which commit taught it. Found by the worker under
constraint 8 and registered by the reviewer.

- R-0536 — Low, A BLOCK PREDICTED FOUR LINE COUNTS UNDER AN UNSTATED NEWLINE CONVENTION
AND EVERY ONE READ ONE HIGH. The R41 block, applied at commit 9cc4772c, stated that
`docs/agents/planner_reviewer_prompt.md` would be "707 lines at HEAD against 644 at
93226220" and that the reviewer's dry run "put it at 47 lines" for `.agent/plan.md`.
Measured at 0e2cdacd with `splitlines`: 706, 643 and 46. The reviewer counted with
`split("\n")` on text ending in a newline, which yields one trailing empty element and
therefore one extra line, while the worker counted with `splitlines`, which does not — the
same one-line divergence the newline convention exists to settle. Nothing false landed in
the repository and no gate failed, and the reason is worth recording as much as the defect:
G5 ordered "report the number rather than asserting it", so the gate asked for a
MEASUREMENT and the reviewer's wrong prediction had no gate to break. A gate that orders a
value would have failed here and cost the round a repair. The counter-measure is the one
already on disk and not followed: state the convention beside any line count a block
predicts, and default to the `splitlines` reading, which is what every worker on this
branch has used. Found by the worker under constraint 8 and registered by the reviewer.
END-RECORD10

BEGIN-DEC4
## DECISION F085 D4 — the `ci_run.py` stage spawn migrates with output re-emitted and the wall as a backstop (2026-08-17)

Ruled by the reviewer at the R41 gate under docs/agents/planner_reviewer_prompt.md §4
item 7. R42 records the ruling; R43 applies it in code, and `builder_bridge.py` follows
in a later round. Reverse it before R43 by deleting this section, or after R43 by
restoring `_run_via_subprocess` to `subprocess.run(command, check=False, cwd=cwd,
env={**os.environ, PYTEST_TIMEOUT_ENV_VAR: str(timeout_sec)})` and dropping the re-emit.

CONTEXT, measured at 0e2cdacd. `.agent/handoff.md` at 93226220 named ONE behavioural
delta for this migration — that `_run_via_subprocess` streams the child's stdout and
stderr to the console through inherited fds and returns only the returncode, while
`run_guarded_test_command` CAPTURES both streams and returns them as bytes. Two more were
measured at 0e2cdacd and are equally load-bearing. First, the seam takes a WALL timeout
and raises `subprocess.TimeoutExpired`, whereas today the per-stage budget travels to the
CHILD as `REMEDY_PYTEST_TIMEOUT_SEC` and the runner self-terminates with exit code 124,
which `run_ci_stage` reads to set `note="timed out"`. Second, the seam SCRUBS the child
environment to `TEST_COMMAND_ENV_ALLOWLIST`, where today the child inherits a full copy of
`os.environ`. A migration that addressed only the output would have changed the other two
silently.

MEASURED, not assumed, before this ruling: a pytest child spawned through
`run_guarded_test_command` with the per-stage budget supplied via the `extra_env` overlay
that landed at dce66faa received 9 environment keys, read the budget back correctly, and
ran `tests/cli/test_golden_path.py` to `42 passed` at returncode 0 in 20.7 s. The
allowlist scrub does not break a pytest child in this repository, which is what made the
env delta rulable rather than a blocker.

CHOSEN, in three parts. OUTPUT: capture, then re-emit — the guarded call keeps both
streams and `_run_via_subprocess` writes them to `sys.stdout.buffer` and
`sys.stderr.buffer` before returning, so the operator still sees every stage's output and
the guard still gets its size cap. What is LOST is live streaming: output appears when a
stage ENDS rather than as it is produced, so a long stage looks silent while it runs.
Stated plainly rather than minimised, because a CI runner that appears hung is a real
cost to whoever is watching it. WALL: a backstop set ABOVE the child's own budget, never
equal to it — the child keeps `REMEDY_PYTEST_TIMEOUT_SEC` and its 124 exit code, so the
timeout that produces a readable pytest report stays the operative one, and the guard's
wall only catches a child that ignores its own budget. ENV: the allowlist plus the
per-stage budget through `extra_env`, which is precisely the capability DECISION F085 D3
added and R39 landed.

ALTERNATIVES CONSIDERED AND REJECTED: capturing without re-emitting, rejected because a CI
runner whose stage output vanishes is worse than an unguarded one; keeping the live stream
by handing inherited fds through the guard, rejected because the output cap is enforced
WHILE the guard reads the pipes and an inherited fd is never read by the guard, so the cap
would silently not apply and the migration would buy nothing; setting the guard's wall
equal to `stage.timeout_sec`, rejected because the two deadlines would race and the guard
would sometimes win, replacing an informative pytest report with a bare kill; leaving
`ci_run.py` unmigrated and naming it in T003's limitations document, rejected because
Amendment F085 D1's class table puts the whole `test` class under stage-1 containment and
an unguarded site would make that row false.

CONSEQUENCE, stated plainly. R43 owes three tests it does not have today: that a stage's
captured output actually reaches the console, that the per-stage budget still arrives in
the child, and that a wall trip maps to the `timed out` note rather than to a bare
non-zero. The size of the grace margin between the child's budget and the guard's wall is
NOT ruled here — it is R43's to choose and to justify in code, because choosing it needs a
measurement of how long a stage takes to die on its own budget, and no such measurement
exists at 0e2cdacd. `tests/orchestration/test_ci_run.py` exercises the real
`_run_via_subprocess` for the budget pass-through, so that test changes with the
implementation and is the first place a silent regression would show.
END-DEC4

BEGIN-PLANF10
## Current Step
R41, this round: record the R40 PASS, register R-0533 and R-0534 — both defects in
RECORD8's own text — and resolve R-0530, R-0531 and R-0532 by writing their
counter-measures into `docs/agents/planner_reviewer_prompt.md`. No production code
changes; R42 takes the `ci_run.py` migration.

## Next Steps
1. T002b remainder — the two `test`-class sites still on a bare spawn. At c3201976 BOTH
   overlay one variable onto a copy of `os.environ`, so both were blocked on the same
   missing capability rather than `builder_bridge.py` alone: `ci_run.py` sets the
   per-stage pytest budget, `builder_bridge.py` sets `PYTHONDONTWRITEBYTECODE`. R38's
   `extra_env` overlay unblocks both (DECISION F085 D3). `ci_run.py` still goes first
   and still owes a DECISION on where its output goes: its spawn streams to the console
   while the seam captures, so that migration changes observable behaviour rather than
   preserving it. One or two per order, never as one group.
END-PLANF10

BEGIN-PLANT10
## Current Step
R42, this round: record the R41 PASS, register R-0535 and R-0536 — both defects in
RECORD9's own text — and rule DECISION F085 D4, the measured design for the `ci_run.py`
migration. Session-closing round: no production code changes, and R43 applies D4 in code.

## Next Steps
1. T002b remainder — the two `test`-class sites still on a bare spawn. At c3201976 BOTH
   overlay one variable onto a copy of `os.environ`, so both were blocked on the same
   missing capability rather than `builder_bridge.py` alone: `ci_run.py` sets the
   per-stage pytest budget, `builder_bridge.py` sets `PYTHONDONTWRITEBYTECODE`. R38's
   `extra_env` overlay unblocks both (DECISION F085 D3). `ci_run.py` goes first and its
   design is ruled in DECISION F085 D4: capture and re-emit the stage output, set the
   guard's wall ABOVE the child's own budget as a backstop, and carry that budget through
   `extra_env`. R43 applies it. One or two per order, never as one group.
END-PLANT10
