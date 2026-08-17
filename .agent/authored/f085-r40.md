── STEP T002b record — F085 — R40 ────────────────────────────────────────────

Goal: record the R39 PASS and register R-0531 and R-0532, both defects in the R39
block's own gate text, so the verdict and the findings are on disk before this session
ends. No production code changes.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record R39
and register R-0531 and R-0532 · C2 the plan · C3 handback.

## Change

C1 appends RECORD8 to `.agent/live_review.md` and nothing else. C2 applies the
`.agent/plan.md` pair over the Current Step block alone; Next Steps is untouched.

Change set, named rather than counted: `.agent/authored/f085-r40.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` and
`.agent/handoff.md`. Nothing else. No production file and no file under `docs/`
changes, so this round orders no ruff run, no `tests/docs/` gate and no red proof.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r40.md` by its marker pair. Never retype one, never apply one
   from the prompt. Marker lines never reach a target file.
2. Pair shape, MEASURED by the reviewer with a containment test and recorded as the
   test's OUTPUT: PLANF8→PLANT8 reads `TO contains FROM: false`, so it is a REWRITE and
   is owed the FROM 0x / TO 1x reading. PLANF8 was measured to occur exactly 1x in
   `.agent/plan.md` at d3a707f5. RECORD8 is an append and carries no FROM.
3. Re-read `.agent/STOP` from disk before C0a and again before C3. If it exists, finish
   the commit in flight, write the handback and stop.
4. `git status --porcelain` is empty at round start and after every commit. This round
   orders no destructive check, so it creates no worktree; `git worktree list` is one
   line throughout.
5. C1 is an APPEND: the pre-commit file stays a byte-exact prefix, exactly one blank
   line joins it to RECORD8, and it is not reflowed, re-wrapped or re-indented.
6. Nothing outside the declared change set is touched. This round registers R-0531 and
   R-0532 and resolves nothing, so the open count moves from 121 to 123.
7. If a gate comes out red, or PLANF8 does not match at exactly one place, STOP: write
   the handback naming the exact command, its exit code and its output, and do not
   improvise a repair.
8. STALENESS, standing: after C2 re-read every file this round edited and confirm no
   sentence this round put on disk was falsified by a later commit of the same round,
   and that no slice quotes another file's current wording as a claim. Name what was
   re-read and report the measurement, not a restatement of this sentence. Give special
   attention to any sentence quantifying over commits, files or lines — R-0530, R-0531
   and R-0532 are all that shape, and two of them landed in the round that registered
   the first.
9. Do not "repair" any landed text. The gate sentences R-0531 and R-0532 register stay
   in commit eba5de68; the registration IS the correction — the R-0521 principle.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 3; `git status
--porcelain` empty at round start and after every commit; `git worktree list` one line
throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r40.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the
reviewer's own `.remedy-wt/f085-r40.md` — disk-to-disk, not a digest fallback. Report
the sha256, byte count, line count, marker-line count, and region digests over lines
1-100, 101-end, each taken with trailing newlines included and reported with its own
byte count so an empty region is visible as empty. Measure every one; compute none by
hand.

G3 APPEND SHAPE for C1 on `.agent/live_review.md`: the pre-commit blob is a byte-exact
PREFIX of the post-commit file; the remainder is exactly one blank line plus RECORD8;
RECORD8 is an exact suffix; its first line occurs once among the lines that commit's
diff ADDS; 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file — count marker
LINES, never the substring, because the quoted regex already appears in that file's
prose. RECORD8 is PROSE, so the §4.9 per-line obligation applies to it and is ordered:
every line RECORD8 contains occurs exactly once among the lines C1's diff adds, EXCEPT
the empty line, which is exempt because a paragraph break repeats by construction —
report how many empty lines the slice holds rather than counting them as failures.
Report `git show --numstat` for that path.

G4 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md`
at base d3a707f5 and at HEAD, from `^- R-\d{4} — `, `^Done: R-\d{4} — ` and
`^Landed: R-\d{4}`. The reviewer's base reading is 145 / 24 / 0, 121 open, max
registered R-0530, max resolved R-0527; at HEAD it must be 147 / 24 / 0, 123 open, max
registered R-0532, max resolved R-0527. Report the registered symmetric difference
(exactly R-0531 and R-0532), the done and landed symmetric differences (both empty),
the duplicate-id count, the count of resolutions naming an unregistered id, the maximum
id, and the next free id, which moves from R-0531 to R-0533.

G5 THE PLAN at HEAD after C2: PLANF8 occurs 0x and PLANT8 1x; `.agent/plan.md` stays
under the 50-line AGENTS.md cap and still carries `## Goal` and `## Next Steps`; 0 lines
matching `^(BEGIN|END)-[A-Z0-9]+$` reached it. Report `git show --numstat` for C2.

G6 SUITES, each run in the PRIMARY checkout and never in a worktree (R-0518), each as
its exact command line, each exit 0. Both base readings were taken by the reviewer at
d3a707f5:
- `python3 -m pytest tests/orchestration/test_test_runner.py
  tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
  tests/ui_server/test_dashboard_contract.py -rf -q` — the four files that read
  `.agent/` state live; base reading `159 passed`. A red naming
  `TestVitestFrontendTestFoundation::test_vitest_passes` with `apps/ui/node_modules`
  absent IS finding R-0518 and means the command ran in a worktree; re-run it in the
  primary checkout. Any other red is a STOP under constraint 7.
- CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base reading
  `42 passed`.

G7 HYGIENE. `git diff --name-only d3a707f5..HEAD` measured BEFORE C3 holds exactly the
change set above minus `.agent/handoff.md`, which C3 writes, and nothing else. Report
per-commit insertions for every commit BEFORE C3 — C3 cannot measure itself, so its own
insertions go in the round report — and confirm none exceeds 500. Confirm every commit
has exactly one parent and that `git reflog -10` holds only `commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round,
branch, base SHA d3a707f5, a per-commit changed-files table, the item-status table
covering C0a, C0b, C1, C2 and C3, the real G1-G7 results with exit codes, the
open-findings count and the next expected action. Repeat this Fortschritt line verbatim:
Fortschritt: ~76 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R39
PASS · T002a KOMPLETT · T002b 10 von 12 Sites auf dem Seam, die letzten 2 ab R41
migrierbar · T002c-d, T003 offen) — Schätzung, gegen die Klassentabelle aus Amendment
F085 D1 gemessen.

This handback closes a SESSION, not only a round. Keep it inside the 60-line cap, or
name the DECISION D15 stated cause and the exact mandated content behind it: R39's
handback ran to 185 lines against a 100-line ceiling, and length is now a standing
observation on this branch rather than a one-round exception.

The `## Next` section MUST state that the next session's FIRST action is Phase 1 rule 1
— re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR Gate (`gh pr list
--state open --json number,headRefName,baseRefName,isDraft`); that R40's own verdict is
NOT a §4.13 terminator because this branch continues; and that the next reviewed round
records R40's gate entry. It MUST also carry this note verbatim:

  R41 migrates `packages/orchestration/ci_run.py` onto the seam, passing the per-stage
  budget through the `extra_env` overlay that landed at dce66faa. It still owes its own
  DECISION on where the stage output goes: at d3a707f5 `_run_via_subprocess` streams
  straight to the console and returns only the returncode, while the seam CAPTURES both
  streams, so the migration changes observable behaviour rather than preserving it. That
  decision is the round's own work and belongs in `.agent/decisions.md` before any line
  changes. `packages/orchestration/builder_bridge.py` follows it; then T002c-d, then
  T003 and the integration gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-RECORD8
Gate: R40 — the R39 entry. R39 PASSED. Every ordered gate was re-run by the reviewer over
cbcb5c23..d3a707f5 and each reproduces the handback's reading. TRANSPORT WAS PROVED
AGAINST THE REVIEWER'S OWN ORIGINAL: the scratch file the block was authored into, the
committed `.agent/authored/f085-r39.md`, the committed `.agent/last_block.md` at 757be21c
and both working copies are all five byte-EQUAL at sha256
32415af6db43f9228459a2bb05241c35c0a39073ab4ffb638d01758448f1181a, 19352 B, 349 lines, 24
marker lines. THE SEAM CHANGE IS THE FOUR PAIRS AND NOTHING ELSE: the reviewer rebuilt
`packages/orchestration/exec_guard.py` mechanically — the pre-commit blob with each FROM
replaced once by its TO equals dce66faa's blob byte for byte — and the guard's floor is
untouched, `def scrub_child_env` through its `return` hashing 3880a84d over 540 B at both
cbcb5c23 and d3a707f5. THE APPEND HELD ITS SHAPE: 607050ba's pre-commit blob 402603 B is
a byte-exact PREFIX of the 406554 B post-commit file, the remainder 3951 B is one blank
line plus RECORD7, RECORD7 is an exact suffix, its first line occurs once among the 50
lines that commit adds, numstat 50/0, and 0 marker lines reached the file. THE ARITHMETIC
MOVED IN THE REGISTERED SET ALONE: 144 / 24 / 0 at cbcb5c23 against 145 / 24 / 0 at
d3a707f5, 120 open against 121, registered symmetric difference exactly R-0530, done and
landed symmetric differences empty, no duplicate id, no resolution naming an unregistered
id, next free R-0531. THE SUITES WERE RE-RUN, NOT READ, each as its exact ordered command
line in the primary checkout, each exit 0: `test_exec_guard.py` `27 passed` against a base
of 24, the four seam consumers `262 passed` equalling their base, the four state readers
`159 passed`, ruff over the two touched paths `All checks passed!`, and the canary
`42 passed`. HYGIENE IS CLEAN: the path set is the seven declared paths, per-commit
insertions are 349, 295, 50, 66, 6 and the handback's own 147, none over 500, all six
commits are single-parent, the reflog holds only `commit:` entries, and origin and local
agree at d3a707f5.

WHAT THE WORKER FOUND AND DID NOT TOUCH. Under constraint 8 R39's worker measured two of
the reviewer's own gate sentences against the repository, found both unsatisfiable,
declared them, ran the strongest measurement each one admitted, and changed no slice. That
is the fifth consecutive round in which the constraint-8 report produced the round's
findings. Both are registered below.

- R-0531 — Low, AN APPEND OBLIGATION WRITTEN FOR PROSE WAS ORDERED OVER A CODE SLICE.
G5 of the R39 block, applied at commit eba5de68, ordered that "every line SEAMTESTS
contains occurs exactly once AMONG THE LINES C2'S DIFF ADDS". Measured at d3a707f5, four
distinct lines of that 47-line slice fail it — the empty line 12x, `    )` 4x, the
argument line `        _child(_ENV_DUMP), timeout_sec=30, cwd=None,` 3x and
`@pytest.mark.subprocess` 2x. §4.9 states the per-line count for TO-ONLY additions and
already bends where a slice legitimately repeats a sentence the file carries; what it does
not anticipate is that a CODE slice repeats lines STRUCTURALLY, because blank separators,
closing parentheses and decorators are what code is made of. The obligation is therefore
unattainable by construction for every code append, which is the R-0207 shape — demanding
a count that invites either a fabricated number or a pointless repair round — arriving
through a slice's LANGUAGE rather than through its pair shape. The worker substituted the
property that does hold and measured it: the lines C2 adds are exactly two empty lines
followed by SEAMTESTS's 47 lines IN ORDER, the pre-commit blob is a byte-exact prefix, and
the slice is an exact suffix. That ordered-equality reading is strictly stronger than the
per-line count it replaced, since it fixes position as well as multiplicity. The next
record round resolves this by writing that reading into the checklist as the form a CODE
append is owed. Found by the worker under constraint 8 and registered by the reviewer.

- R-0532 — Low, A BASELINE GATE WAS ORDERED AT A COMMIT WHERE ITS OWN PATHS DO NOT EXIST.
G6 of the R39 block, applied at commit eba5de68, ordered `ruff check` over
`packages/orchestration/exec_guard.py` and `tests/orchestration/test_exec_guard.py` "at
`origin/main` as well", so that a pre-existing error could not be read as a new one.
Measured: `git ls-tree origin/main` returns nothing for either path — `exec_guard.py` was
ADDED on this branch at e0d4d880 — so the command exits 1 with `E902 No such file or
directory` per path and produces no lint reading at all. The comparison the gate exists to
make is empty by construction. This is R-0364 recurring in the reviewer's own text: that
finding's whole content is that a gate is executed at its base BEFORE it is ordered, and
the HEAD run was executed while the origin/main run was not. A second defect rides in the
same gate: G6's preamble binds every command in it to "the PRIMARY checkout and never in a
worktree" under R-0518, while a reading at `origin/main` from a branch checkout requires
exactly the worktree that clause forbids, so the two sentences cannot both be obeyed. The
worker ran it, recorded the exit code and output, treated the green HEAD gate as the
operative one and declared the rest, which is the correct handling. Nothing false about
the repository landed. The next record round resolves this by binding a baseline gate to
paths that exist at the base it names, and by carving the worktree exception the R-0518
clause needs.
END-RECORD8

BEGIN-PLANF8
## Current Step
R39, this round: record the R38 PASS, register R-0530, and implement DECISION F085 D3 —
the `extra_env` overlay on the `test`-class seam, with the tests pinning the set, the
`FORBIDDEN_ENV_KEYS` floor and the untouched allowlist. No call site is migrated.
END-PLANF8

BEGIN-PLANT8
## Current Step
R40, this round: record the R39 PASS and register R-0531 and R-0532, the two R39 gate
sentences its worker measured as unsatisfiable. Session-closing round: no production
code changes, and R41 takes the `ci_run.py` migration.
END-PLANT8
