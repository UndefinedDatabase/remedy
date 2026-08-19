── STEP T002d second half — F085 — R58 ───────────────────────────────────────

Goal: finish T002d's child half. The two `runtime-build` call sites in `_auto_build_frontend`
(`packages/orchestration/ui_server.py`) stop calling `subprocess.run` directly and call
`run_guarded_runtime_build_command` with `check=True`, so the `runtime-build` policy R54 built and
R56 settled — wall timeout, output cap, pinned cwd, env allowlist — actually binds the npm
commands the UI server spawns. One new test pins the migration. This round also records the R57
PASS and the reviewer-authored resolution of R-0558.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance `.agent/plan.md`
· C2 record the R57 PASS and resolve R-0558 · C3 migrate both call sites and pin them with a test ·
C4 handback. That is SIX ordered commits, which is more than five, so the handback carries the
≤100-line allowance rather than the ≤60-line cap.

CONVENTION, binding on every count here, carried verbatim in force from the R57 block. A line count
is the `splitlines` reading — a trailing newline is NOT an extra line. A SLICE IS THE BYTES STRICTLY
BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE NEWLINE THAT TERMINATES ITS LAST CONTENT LINE:
extract it as everything after the `BEGIN-` line's own newline up to and including the newline
immediately before the `END-` line, so that `pre + slice` is already a newline-terminated file and
NO joiner and NO terminator byte is ever added. THIS BLOCK CARRIES NO APPEND AT ALL. Every one of
its six slices is a FROM/TO REWRITE pair, including the two that add new code, which is the R-0558
counter-measure applied rather than restated: a slice that adds lines to a `.py` file carries the
blank lines its target's convention requires INSIDE the slice, so the separation is a property of
bytes that were measured and not of a join shape that was reasoned about.

## Change

C1 applies PLAN12F→PLAN12T to `.agent/plan.md`, rewriting the `## Current Step` section and the
WHOLE `## Next Steps` list. C2 applies RECORD26F→RECORD26T to `.agent/live_review.md`: the FROM is
the single `Landed: R-0558` line the R57 worker wrote as the last line of that file, and the TO is
the R57 gate record followed by the reviewer-authored `Done: R-0558` that supersedes it — a
`Landed:` line is the worker's placeholder and the reviewer's resolution replaces it rather than
accumulating beside it. C3 applies FOUR pairs in ONE commit, because the three on
`packages/orchestration/ui_server.py` leave the module broken if they land apart:
DOCIMPORTF→DOCIMPORTT adds the docstring paragraph and the `exec_guard` import,
INSTALLF→INSTALLT migrates the `npm install` site, BUILDF→BUILDT migrates the `npm run build`
site, and TESTGUARDF→TESTGUARDT inserts one new test into `TestAutoBuildBehavior` in
`tests/ui_server/test_dashboard_contract.py`.

Change set, named rather than counted: `.agent/authored/f085-r58.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `packages/orchestration/ui_server.py`,
`tests/ui_server/test_dashboard_contract.py`, `.agent/handoff.md`. Nothing else. No
`docs/roadmap/**` path is in that set, so the §3 docs tier does NOT trigger and no `tests/docs/`
gate is ordered. `packages/orchestration/exec_guard.py` is NOT in it: the seam this round consumes
is finished and correct, and a call-site migration is not a licence to touch the callee. The three
`runtime-server` sites are NOT in it either; they are the next round's, and they take no wall
timeout, so bundling them here would mix two policy classes in one commit.

WHY THE SEAM IS REACHED AS A MODULE ATTRIBUTE. `DOCIMPORTT` imports the MODULE
(`from packages.orchestration import exec_guard`) and the two call sites spell
`exec_guard.run_guarded_runtime_build_command(...)`. A `from ... import
run_guarded_runtime_build_command` would bind the function into `ui_server`'s namespace at import
time, and the test TESTGUARDT patches `exec_guard.run_guarded_runtime_build_command` — which that
binding would make invisible. The import is function-local because the surrounding function
already imports `subprocess` locally and this file's other in-function import
(`ui_app_shell.build_app_shell`) uses the same idiom; a module-level import here would also be the
one place a cycle could form. `import subprocess` STAYS: the two `except` clauses name
`subprocess.CalledProcessError` and `subprocess.TimeoutExpired`, which the seam raises.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r58.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C4; if it exists, finish the commit
   in flight, write the handback and stop. `git status --porcelain` is empty at round start and
   after every commit. This round DOES order a destructive check (G9), which runs ONLY in a
   disposable `git worktree` under `.remedy-wt/` and is removed before the handback, so
   `git worktree list` is one line at round start and again at the end.
3. PAIR SHAPES. The reviewer ran the containment test on each pair at emission against that file's
   blob at b2bb3809 and prints its own output here per checklist item 15, one reading per pair:
   PLAN12F→PLAN12T `TO contains FROM: false`; RECORD26F→RECORD26T `TO contains FROM: false`;
   DOCIMPORTF→DOCIMPORTT `TO contains FROM: false`; INSTALLF→INSTALLT `TO contains FROM: false`;
   BUILDF→BUILDT `TO contains FROM: false`; TESTGUARDF→TESTGUARDT `TO contains FROM: false`. All
   six are therefore REWRITES and each owes the FROM 0x / TO 1x reading over its own post-commit
   file. Each FROM occurs EXACTLY 1x in its target at b2bb3809 — the reviewer measured all six.
   DOCIMPORT and TESTGUARD are the two easy to misread as appends: each PRESERVES its FROM's lines
   in the TO but SPLITS the contiguous byte run between them, which is why the containment test
   comes out false and why an insert-shaped edit is not what lands.
4. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of the migration. Only C0a and
   C0b may precede it. This round writes to the finding ledger, so §3 checklist item 23 binds it.
5. Every sentence in RECORD26T that states a reading of a file THIS BLOCK also edits names the SHA
   it was read at in the same clause, per checklist item 20 as R-0521 and R-0534 narrow it — the
   qualifier attaches to EVERY reading in the clause, not only the first. This binds the readings
   of `packages/orchestration/ui_server.py` and `tests/ui_server/test_dashboard_contract.py`, which
   C3 changes AFTER RECORD26T lands, and the readings of `.agent/last_block.md`, which C0b
   overwrites before it lands.
6. NO SLICE REPRODUCES A RETIRED FROM TEXT. The reviewer tested all six FROM texts against every
   later-applied text at emission and got NO hits, so every G3 FROM-0x reading stays attainable
   (checklist item 2).
7. THE WORKER AUTHORS NO LEDGER TEXT THIS ROUND. RECORD26T is reviewer text and carries both the
   gate record and the `Done:` line; do not add a `Landed:` line, do not add a `Done:` paragraph
   of your own, and do not edit RECORD26T to reconcile it with anything you measure. A disagreement
   between RECORD26T and your own reading is a finding to REPORT in the handback, never to fix.
8. THIS ROUND RESOLVES R-0558 AND REGISTERS NOTHING. Registered stays 173, done goes 27 → 28,
   landed goes 1 → 0 because RECORD26F is the only `Landed:` line in the file and the TO does not
   reproduce it, open goes 146 → 145, and the next free id stays R-0559.
9. THE MIGRATION IS BEHAVIOUR-PRESERVING AND NOTHING ELSE MOVES. Do not change the two commands,
   the 120-second timeouts, the `cwd`, the `except` tuples, the printed messages or the return
   values. `capture_output=True` is DROPPED from both calls and that is not a behaviour change: the
   guard always captures, and `run_guarded_runtime_build_command` returns a
   `CompletedProcess` with BYTES streams either way. The reviewer verified this end to end at
   b2bb3809 before ordering the round — the real `npm run build` in `apps/ui` returns rc 0 with 355
   bytes of stdout and 0 of stderr both unguarded and through the seam.
10. DO NOT REFORMAT EITHER TARGET AND DO NOT RUN `ruff --fix`. Both files R58 edits already carry
   preview-only findings at b2bb3809 — `packages/orchestration/ui_server.py` reports 3 and
   `tests/ui_server/test_dashboard_contract.py` reports 13 — and sweeping them is exactly the churn
   AGENTS.md's Code Discoverability section forbids as its own activity. G5 is narrowed accordingly
   and is stated below in the only form either file can honestly pass.
11. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three on the
   final bytes at emission and states them here: TOTAL 436, PROSE 267, RECORD26T 53. The worker
   re-measures all three from the committed `.agent/authored/f085-r58.md` and reports them; a
   mismatch is a finding against this block, not against the worker.
12. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and
   its output, and push what is committed. Never edit a slice to make a gate green, and never widen
   the change set to route around a red.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit; `git worktree list` one line at round start and at the end,
with the G9 worktree created and removed in between.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r58.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the reviewer's
`.remedy-wt/f085-r58.md` — disk-to-disk, not a digest fallback. Report sha256, byte count, line
count and marker-line count. Measure every one on every copy.

G3 SHAPES, measured SEPARATELY per pair and per path. All six pairs are REWRITES, so each owes the
SAME three readings over its own post-commit blob: its FROM occurs 0x, its TO occurs exactly 1x,
and re-applying the extracted FROM→TO to the pre-commit blob reproduces the post-commit blob
BYTE-EXACTLY. Report all three per pair, plus `git show --numstat` for each path and commit, plus
the count of lines matching `^(BEGIN|END)-[A-Z0-9]+$` in each edited file, which must be 0 — count
marker LINES, never the substring, since that regex already appears in `.agent/live_review.md`.

G4 SUITES, in the PRIMARY checkout and never in a worktree (R-0518), each exit 0. The reviewer took
every base reading below itself, in the primary checkout, at b2bb3809.
 - `python3 -m pytest tests/ui_server/test_dashboard_contract.py -rf -q` — base `70 passed`. This
   round adds exactly one test and deletes none, so REPORT the number and state whether it is 71.
 - `python3 -m pytest tests/ui_contracts/test_responsive.py -rf -q` — base `92 passed`. Ordered
   because that file asserts on the SOURCE TEXT of `packages/orchestration/ui_server.py`, which C3
   rewrites.
 - `python3 -m pytest tests/orchestration/test_exec_guard.py -rf -q` — base `35 passed`. Ordered
   because this round is the first real consumer of the seam that suite covers.
 - `python3 -m pytest tests/orchestration/test_test_runner.py
   tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
   tests/ui_server/test_dashboard_contract.py -rf -q` — base `159 passed`; two of them assert on
   `.agent/plan.md`, which C1 rewrites, and the set contains the file C3 edits, so its expected
   reading is 160.
 - CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G5 LINT, over the SAME two paths, with the repository's own `pyproject.toml` and NEVER `--isolated`
(R-0463).
 - `python3 -m ruff check packages/orchestration/ui_server.py
   tests/ui_server/test_dashboard_contract.py` — exit 0, `All checks passed!`.
 - THE NARROWED PREVIEW READING, which is the R-0558 counter-measure in the only form these two
   paths can honestly meet, since neither is preview-clean at b2bb3809. For EACH path separately,
   run `python3 -m ruff check --preview --output-format=json <path>` at b2bb3809 and at HEAD and
   compare the MULTISET OF RULE CODES, not the line numbers, which shift when lines are inserted.
   The two multisets must be IDENTICAL per path. The reviewer's base reading, measured at
   b2bb3809: `packages/orchestration/ui_server.py` → `E306` x3; and
   `tests/ui_server/test_dashboard_contract.py` → `E226` x1, `E303` x11, `W391` x1. REPORT both
   multisets at both SHAs. A NEW code, or a higher count of an existing one, is a red gate under
   constraint 12 — it means a slice failed to carry the blank lines its target's convention wants,
   which is precisely what R-0558 was registered for.

G6 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer collected
by grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. The
reviewer projected 43 lines mechanically by applying the pair to that file's blob at b2bb3809.

G7 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
b2bb3809 and at HEAD, from the line-start patterns for a registration, a resolution and a landed
line. The reviewer's base reading is 173 / 27 / 1, 146 open, max registered R-0558, max resolved
R-0532. At HEAD the reading must be 173 / 28 / 0, 145 open, max registered R-0558, max resolved
R-0558: the registered symmetric difference is EMPTY, the done symmetric difference is exactly
R-0558, and the landed symmetric difference is exactly R-0558 — that last one because the line is
REMOVED, so confirm the direction and do not report a bare set. Next free id R-0559. Report all
three symmetric differences, the duplicate-id count and the count of resolutions naming an
unregistered id, at both SHAs.

G8 HYGIENE. `git diff --name-only b2bb3809..HEAD` measured BEFORE C4 holds exactly the change set
above minus `.agent/handoff.md`, which C4 writes, and nothing else — and in particular holds NEITHER
`packages/orchestration/exec_guard.py` NOR any of `packages/orchestration/runtime_cmd.py`,
`packages/orchestration/dev_server.py` and `packages/orchestration/runtime_supervisor.py`, whose
migration is R59's. Report per-commit insertions for every commit BEFORE C4 — C4 cannot measure
itself, so its own insertions go in the round report — and confirm none exceeds 500. This branch
spent the AGENTS.md declared-oversize allowance at d4473f85, so a second oversize commit is a STOP
under constraint 12, never a declaration. Confirm every commit is single-parent.

G9 RED CONTROL, the proof the new test has teeth, run ONLY in a disposable worktree created from
HEAD under `.remedy-wt/` and removed before the handback. In that worktree, and NEVER in the
primary checkout, apply BUILDT→BUILDF alone — restoring the bare `subprocess.run` at the
`npm run build` site and leaving the `npm install` site migrated — then run
`python3 -m pytest tests/ui_server/test_dashboard_contract.py -rf -q`. ORDERED RESULT: the run is
RED and `test_auto_build_npm_commands_run_through_the_guard` is among the failures, while no other
test in that file turns red. Report the exit code, the failing test names verbatim from the `-rf`
summary and the colour of the rest — do NOT report a predicted pass count, and do not let the
reverted state reach a commit. A FRESH WORKTREE IS NOT THE PRIMARY CHECKOUT: `apps/ui/node_modules`
is untracked, so that suite skips one UI-toolchain test there and its first auto-build test may
really run `npm install` and create it. That is why G9 orders a COLOUR and no count, and it is why
every G4 reading stays in the primary checkout (R-0518). Then remove the worktree and confirm
`git worktree list` is one line and `git status --porcelain` is empty in the primary checkout.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base
SHA b2bb3809, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2, C3
and C4, the real G1-G9 results with exit codes, the open-findings count and the next expected
action. The Bundle above names six commits, which is more than five, so the ≤100-line allowance
applies; if the mandated content genuinely does not fit even that, name the DECISION D15 stated
cause and the specific mandated content behind the overage, and drop no section.
Repeat this Fortschritt line verbatim:
Fortschritt: ~96 % (T001 gebaut · R13-R55 PASS · R56 FAIL, an R57 repariert · R57 PASS · T002a
KOMPLETT · T002b KOMPLETT · T002c KOMPLETT · T002d KOMPLETT — Naht, Extraktion, Umgebungszeile und
die beiden `runtime-build`-Call-Sites gebaut · T003 offen, mitsamt den drei
`runtime-server`-Call-Sites) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: the next round is
R59, which migrates the three `runtime-server` call sites in `packages/orchestration/runtime_cmd.py`,
`packages/orchestration/dev_server.py` and `packages/orchestration/runtime_supervisor.py`; they are
`Popen`-shaped and take NO wall timeout, because a clock would kill a server mid-service, so that
round's first task is to establish whether a `runtime-server` seam exists yet or has to be built.
TWO: R59 also carries the R58 verdict, because the round that records a verdict cannot record one
on itself (docs/agents/planner_reviewer_prompt.md §4.13). THREE: a standalone closing line stating
the open findings count and the next free id as its own sentence. FOUR:
`Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, which the self-drive protocol requires
every handoff naming a next action to put ahead of the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN12F
## Current Step
R57, this round: repair the one defect R56 landed. Its C3 joined a code slice to
`tests/orchestration/test_exec_guard.py` with one blank line where that file's own convention uses
two, and the ordered `ruff` gate is blind to it because this repository does not run `--preview`
and E301-E306 are preview-only. This round registers R-0558, adds the blank line and records the
R56 FAIL. R56's production change is correct and is not touched.

## Next Steps
1. T002d's second half — migrate the two `runtime-build` sites in `_auto_build_frontend`
   (`packages/orchestration/ui_server.py`) onto `run_guarded_runtime_build_command` with
   `check=True`. Then the three `runtime-server` sites, which take no wall timeout because a
   clock would kill them mid-service.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output
   cap, and a build behind an HTTP proxy does not run under the guard at all, because the proxy
   variables are `FORBIDDEN_ENV_KEYS` members and the floor is not a row's to lift.
   Then the integration gate, then closure.
END-PLAN12F

BEGIN-PLAN12T
## Current Step
R58, this round: T002d's second half. The two `runtime-build` call sites in
`_auto_build_frontend` (`packages/orchestration/ui_server.py`) move onto
`run_guarded_runtime_build_command` with `check=True`, reached as a module attribute so a test
can patch it, and one new test pins that no bare `subprocess.run` survives in that function.
The R57 PASS and the resolution of R-0558 are recorded in the same round.

## Next Steps
1. The three `runtime-server` sites (`runtime_cmd.py`, `dev_server.py`,
   `runtime_supervisor.py`) — `Popen`-shaped, and taking NO wall timeout, because a clock
   would kill them mid-service.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output
   cap, and a build behind an HTTP proxy does not run under the guard at all, because the proxy
   variables are `FORBIDDEN_ENV_KEYS` members and the floor is not a row's to lift.
   Then the integration gate, then closure.
END-PLAN12T

BEGIN-RECORD26F
Landed: R-0558 — the two-blank-line separation PEP 8 puts between a function and the following top-level definition is restored before `_RUNTIME_BUILD_ADDED_ENV_KEYS` in `tests/orchestration/test_exec_guard.py`; the edit adds exactly one newline byte and changes no code, and `python3 -m ruff check --preview` over that path is exit 0 where it reported one E305 before; commit 356a1568, C3 of R57.
END-RECORD26F

BEGIN-RECORD26T
Gate: R58 — the R57 entry. R57 PASSED. Every ordered gate G1-G8 was re-executed by the reviewer
over 3bb82a25..b2bb3809, not read, and each reproduces the handback's reading exactly; the worker
deviated in nothing and declared its scratch honestly. LINE COUNTS ARE `splitlines` COUNTS.
TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no digest fallback:
`.remedy-wt/f085-r57.md`, the committed `.agent/authored/f085-r57.md` and the committed
`.agent/last_block.md` at b2bb3809, and both of those working copies as they stand at b2bb3809, are
all five byte-EQUAL at sha256 d186ed7740849c36c93e83bcc6ae3509ae820d743aa0eb7d06d3e575a7a18b74,
22571 B, 298 lines, 10 marker lines, which is the digest the reviewer emitted. THE SHAPES HELD.
Both REWRITES give `TO contains FROM: false`, the FROM 1x in the pre-commit blob and 0x after with
the TO exactly 1x, and in each case re-applying the extracted FROM→TO to the pre-commit blob
reproduces the post-commit blob BYTE-EXACTLY: PLAN11F→PLAN11T at ddd4f8b8 numstat `5 5`, and
FIXBLANKF→FIXBLANKT at 356a1568 numstat `1 0`, where the FROM is 142 B and the TO 143 B and
`tests/orchestration/test_exec_guard.py` goes 29917 B / 731 lines to 29918 B / 732 lines — the
whole effect is one newline byte. THE PROSE APPEND RECORD25 on `.agent/live_review.md` at a6c5176f:
byte-exact prefix, a remainder of exactly one blank line plus the slice, an exact suffix, 0 marker
LINES, and each of its 57 non-empty slice lines occurring exactly once among the 59 lines that
commit adds, numstat `59 0`. THE SUITES AND BOTH LINT HALVES WERE RE-RUN, NOT READ, in the primary
checkout with the block's exact command lines, each exit 0: the guard suite `35 passed`, the four
state readers `159 passed`, the canary `42 passed`, ruff `All checks passed!` and — the reading
this round exists for — `ruff check --preview` over the two paths `All checks passed!`. THE RED
CONTROL THE BLOCK DID NOT ORDER WAS RUN ANYWAY, in a disposable worktree since removed, because a
green preview cannot by itself tell a repaired file from one that was never broken: at 3bb82a25
that exact command is exit 1 with `Found 1 error.` and exactly one `E305` at
`tests/orchestration/test_exec_guard.py:691`, and at 49a3fdcb it is exit 0 `All checks passed!` —
so the fix has teeth and the violation was R56's alone. THE PLAN CONTRACT HELD at ddd4f8b8: 44
lines against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap F-id present, 44 being
the figure that block projected. THE ARITHMETIC MOVED EXACTLY AS ORDERED: 172 / 27 / 0 and 145 open
at 3bb82a25, 173 / 27 / 1 and 146 open at b2bb3809, the registered and landed symmetric differences
each exactly `{R-0558}` and the done symmetric difference EMPTY, with 0 duplicate ids and 0
resolutions naming an unregistered id at both SHAs. HYGIENE IS CLEAN: the path set over that range
is exactly the six the change set named and holds NEITHER `packages/orchestration/exec_guard.py`
NOR `packages/orchestration/ui_server.py`; per-commit INSERTIONS are 298, 203, 5, 59, 1, 2 and 39
for the handback commit, none over 500; all seven commits are single-parent. THE BLOCK'S OWN SIZE
re-measured from the committed file gives TOTAL 298, PROSE 199 and RECORD25 58, agreeing with that
block, and the handback's self-claim of 79 lines measures 79. TWO NUMERIC CLAIMS RECORD25 PUT INTO
THE PERMANENT RECORD WERE CHECKED RATHER THAN ACCEPTED, since a wrong count there is the R-0402
class: `--preview` over `packages`, `tests` and `apps` at 3bb82a25 reports exactly 634 findings,
and at that SHA `_ENV_DUMP` carries two blank lines above its comment block where
`_RUNTIME_BUILD_ADDED_ENV_KEYS` carried one. NOTHING FAILED and this round registers no finding.

Done: R-0558 — Resolved at R57, commit 356a1568. The two-blank-line separation PEP 8 puts between a
function and the following top-level definition is restored before `_RUNTIME_BUILD_ADDED_ENV_KEYS`
in `tests/orchestration/test_exec_guard.py`; the edit adds exactly one newline byte and changes no
code. The reviewer verified the colour in both directions in a disposable worktree, since removed:
`python3 -m ruff check --preview` over that path is exit 0 at b2bb3809 and exit 1 with exactly one
`E305` at line 691 at 3bb82a25. BOTH HALVES of the counter-measure this finding named are in force
from R58 on. First, a code slice CARRIES the blank lines its target's convention requires INSIDE
the slice — R58 goes further and uses no append at all. Second, a block editing a `.py` file gates
that path with `ruff check --preview`, narrowed where the path already carries preview findings to
a comparison of the RULE-CODE MULTISET at base and at HEAD, since a bare exit-0 gate over such a
path is unpassable: at b2bb3809 `packages/orchestration/ui_server.py` reports 3 preview findings
and `tests/ui_server/test_dashboard_contract.py` reports 13, and R58 gates both in that narrowed
form.
END-RECORD26T

BEGIN-DOCIMPORTF
    Disable with REMEDY_UI_NO_AUTO_BUILD=1 if you manage builds yourself.
    """
    import subprocess
END-DOCIMPORTF

BEGIN-DOCIMPORTT
    Disable with REMEDY_UI_NO_AUTO_BUILD=1 if you manage builds yourself.

    Both npm commands run through `run_guarded_runtime_build_command`, so the
    `runtime-build` policy — wall timeout, output cap, pinned cwd and the env
    allowlist — bounds them here instead of a bare `subprocess.run` handing the whole
    parent environment to an npm lifecycle script. The seam is reached as a module
    attribute so a test can patch it; `subprocess` stays imported for the two
    exception types the `except` clauses below name.
    """
    import subprocess

    from packages.orchestration import exec_guard
END-DOCIMPORTT

BEGIN-INSTALLF
            subprocess.run(
                ["npm", "install", "--no-audit", "--no-fund"],
                cwd=str(ui_root),
                check=True,
                capture_output=True,
                timeout=120,
            )
END-INSTALLF

BEGIN-INSTALLT
            exec_guard.run_guarded_runtime_build_command(
                ["npm", "install", "--no-audit", "--no-fund"],
                timeout_sec=120,
                cwd=str(ui_root),
                check=True,
            )
END-INSTALLT

BEGIN-BUILDF
        subprocess.run(
            ["npm", "run", "build"],
            cwd=str(ui_root),
            check=True,
            capture_output=True,
            timeout=120,
        )
END-BUILDF

BEGIN-BUILDT
        exec_guard.run_guarded_runtime_build_command(
            ["npm", "run", "build"],
            timeout_sec=120,
            cwd=str(ui_root),
            check=True,
        )
END-BUILDT

BEGIN-TESTGUARDF
                mock_run.assert_not_called()

    def test_frontend_is_stale_function_exists(self):
END-TESTGUARDF

BEGIN-TESTGUARDT
                mock_run.assert_not_called()

    def test_auto_build_npm_commands_run_through_the_guard(self):
        """Both npm commands reach the runtime-build seam; none reaches a bare run."""
        import inspect
        import subprocess as sp

        from packages.orchestration import exec_guard, ui_server

        seen = []

        def _record(cmd, *, timeout_sec, cwd, check=False):
            seen.append((list(cmd), timeout_sec, cwd, check))
            return sp.CompletedProcess(list(cmd), 0, b"", b"")

        env = os.environ.copy()
        env.pop("REMEDY_UI_NO_AUTO_BUILD", None)
        with patch.dict(os.environ, env, clear=True):
            with patch.object(exec_guard, "run_guarded_runtime_build_command", _record):
                with patch.object(sp, "run") as bare_run:
                    ui_server._auto_build_frontend()

        assert bare_run.call_count == 0
        assert seen, "the npm run build site never reached the guard"
        cmd, timeout_sec, cwd, check = seen[-1]
        assert cmd == ["npm", "run", "build"]
        assert timeout_sec == 120
        assert check is True
        assert cwd is not None and cwd.endswith("apps/ui")

        # The install site is skipped whenever node_modules is fresh, so this run may
        # never reach it. Pin that site structurally instead of by a call that depends
        # on the checkout's mtimes.
        source = inspect.getsource(ui_server._auto_build_frontend)
        assert source.count("exec_guard.run_guarded_runtime_build_command(") == 2
        assert "subprocess.run(" not in source

    def test_frontend_is_stale_function_exists(self):
END-TESTGUARDT
