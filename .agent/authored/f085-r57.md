── STEP T002d repair — F085 — R57 ────────────────────────────────────────────

Goal: repair the one defect R56 landed. C3 of that round joined a CODE slice to
`tests/orchestration/test_exec_guard.py` with a single blank line, so the file now separates a
top-level definition from the function above it by one blank line where PEP 8 and that file's own
convention use two. The ordered lint gate could not see it: this repository runs `ruff` WITHOUT
`--preview`, and E301-E306 are preview-only rules, so the round's green lint was blind rather than
clean. This round registers that as R-0558, adds the missing blank line, and records the R56 FAIL.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance
`.agent/plan.md` · C2 record the R56 FAIL and register R-0558 · C3 add the missing blank line ·
C4 mark R-0558 landed · C5 handback. That is SEVEN ordered commits, which is more than five, so
the handback carries the ≤100-line allowance rather than the ≤60-line cap.

CONVENTION, binding on every count here, carried verbatim in force from the R56 block because it is
the R-0556 counter-measure. A line count is the `splitlines` reading — a trailing newline is NOT an
extra line. A SLICE IS THE BYTES STRICTLY BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE
NEWLINE THAT TERMINATES ITS LAST CONTENT LINE: extract it as everything after the `BEGIN-` line's
own newline up to and including the newline immediately before the `END-` line, so that
`pre + slice` is already a newline-terminated file and NO joiner and NO terminator byte is ever
added. RECORD25 is PROSE joined to its target by exactly one blank line. This block carries no code
APPEND at all — the code change is a FROM/TO pair, which is the R-0558 counter-measure itself.

## Change

C1 applies PLAN11F→PLAN11T to `.agent/plan.md`, rewriting the `## Current Step` section and the
WHOLE `## Next Steps` list. C2 appends RECORD25 to `.agent/live_review.md`. C3 applies
FIXBLANKF→FIXBLANKT to `tests/orchestration/test_exec_guard.py`, whose entire effect is one added
blank line: the pair spans the boundary between the last existing test and the comment that opens
the R56 append, because a blank line has no other anchor to be identified by. C4 appends a single
`Landed:` line to `.agent/live_review.md` — the ONLY text in this round the WORKER authors, per
docs/agents/planner_reviewer_prompt.md §4 item 4, which reserves `Done:` for reviewer text and
gives the worker `Landed:` for a fix that lands before its resolution is written.

Change set, named rather than counted: `.agent/authored/f085-r57.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `tests/orchestration/test_exec_guard.py`,
`.agent/handoff.md`. Nothing else. No `docs/roadmap/**` path is in that set, so the §3 docs tier
does NOT trigger and no `tests/docs/` gate is ordered. `packages/orchestration/exec_guard.py` is
NOT in it: R56's production change is correct and stays exactly as it landed — only its test
file's blank line is wrong. `packages/orchestration/ui_server.py` is not in it either; the
migration is R58's.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r57.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C5; if it exists, finish the commit
   in flight, write the handback and stop. `git status --porcelain` is empty at round start and
   after every commit. This round orders no destructive check, so it creates no worktree and
   `git worktree list` stays one line throughout.
3. PAIR SHAPES. The reviewer ran the containment test on each pair at emission against that file's
   blob at 3bb82a25 and prints its own output here per checklist item 15, one reading per pair:
   PLAN11F→PLAN11T `TO contains FROM: false`; FIXBLANKF→FIXBLANKT `TO contains FROM: false`. Both
   are therefore REWRITES and each owes the FROM 0x / TO 1x reading over its own post-commit file.
   Each FROM occurs EXACTLY 1x in its target at 3bb82a25 — the reviewer measured both. The
   FIXBLANK reading is the one that is easy to get wrong by eye: inserting a blank line looks
   append-shaped, and it is not, because the FROM's two-newline run is not contiguous in the TO.
   RECORD25 is an APPEND carrying no FROM, so no containment reading is owed for it.
4. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of the fix. Only C0a and C0b
   may precede it. This round writes to the finding ledger, so §3 checklist item 23 binds it.
5. Every sentence in RECORD25 that states a reading of a file THIS BLOCK also edits names the SHA
   it was read at in the same clause, per checklist item 20 as R-0521 and R-0534 narrow it — the
   qualifier attaches to EVERY reading in the clause, not only the first. This binds the readings
   of `tests/orchestration/test_exec_guard.py` in particular, which C3 changes AFTER RECORD25
   lands, and the readings of `.agent/last_block.md`, which C0b overwrites before it lands.
6. NO SLICE REPRODUCES A RETIRED FROM TEXT. The reviewer tested PLAN11F and FIXBLANKF against every
   later-applied text at emission and got NO hits, so both G3 FROM-0x readings stay attainable
   (checklist item 2).
7. C4's `Landed:` line is the worker's own single sentence and is not a slice: write exactly one
   line beginning `Landed: R-0558 — `, naming what changed and the SHA of C3, which exists by then
   because C4 is a separate commit. Write NOTHING else into that file in C4, and never write a
   `Done:` paragraph — only reviewer-authored text sets a resolution.
8. THIS ROUND REGISTERS R-0558 AND RESOLVES NOTHING. Registered goes 172 → 173, done stays 27,
   landed goes 0 → 1, open goes 145 → 146, and the next free id becomes R-0559. The resolution of
   R-0558 is authored by the reviewer in the NEXT round, after it has gated this fix.
9. THE FIX IS ONE BLANK LINE AND NOTHING ELSE. Do not reformat the file, do not run `ruff --fix`
   over it, do not touch the other preview-only findings anywhere in this repository. There are
   634 of them across `packages/`, `tests/` and `apps/`, measured by the reviewer at 3bb82a25, and
   sweeping them is exactly the churn AGENTS.md's Code Discoverability section forbids as its own
   activity.
10. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three on the
   final bytes at emission and states them here: TOTAL 298, PROSE 199, RECORD25 58. The worker
   re-measures all three from the committed `.agent/authored/f085-r57.md` and reports them; a
   mismatch is a finding against this block, not against the worker.
11. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and
   its output, and push what is committed. Never edit a slice to make a gate green, and never widen
   the change set to route around a red.
12. THIS ROUND ORDERS NO RED CONTROL. The reviewer proved at 3bb82a25, in its own disposable
   worktree, that the two tests R56 shipped have teeth — reverting the widened row reddens both and
   leaves the other 33 green, and making `scrub_child_env` match `NPM_CONFIG_` as a PREFIX reddens
   the second alone — and it removed that worktree. Nothing this round changes is behavioural, so
   there is no new colour to prove.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit; `git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r57.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the reviewer's
`.remedy-wt/f085-r57.md` — disk-to-disk, not a digest fallback. Report sha256, byte count, line
count and marker-line count. Measure every one on every copy.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - The TWO REWRITES of constraint 3: in each post-commit file its FROM occurs 0x and its TO exactly
   1x. Report both counts per pair and `git show --numstat` for each path and commit.
 - C2 / RECORD25 / `.agent/live_review.md`, a PROSE APPEND: the pre-commit blob is a byte-exact
   PREFIX of the post-commit file, the remainder is exactly one blank line plus the slice, the
   slice is an exact suffix, and 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file —
   count marker LINES, never the substring, since that regex already appears in that file's prose.
   §4.9's per-line PROSE obligation also applies: every non-empty line the slice contains occurs
   exactly once among the lines C2's diff adds TO THAT PATH.

G4 SUITES, in the PRIMARY checkout and never in a worktree (R-0518), each exit 0. The reviewer took
every base reading below itself, in the primary checkout, at 3bb82a25.
 - `python3 -m pytest tests/orchestration/test_exec_guard.py -rf -q` — base `35 passed`, and this
   round ships no test and deletes none, so the expected reading is `35 passed`. REPORT the number.
 - `python3 -m pytest tests/orchestration/test_test_runner.py
   tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
   tests/ui_server/test_dashboard_contract.py -rf -q` — ordered because C1 rewrites
   `.agent/plan.md`, which two of them assert on. Base `159 passed`.
 - CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G5 LINT, both halves, over the SAME two paths, with the repository's own `pyproject.toml` and NEVER
`--isolated` (R-0463). This gate is the substance of the round, so read both readings.
 - `python3 -m ruff check packages/orchestration/exec_guard.py
   tests/orchestration/test_exec_guard.py` — exit 0, `All checks passed!`. This is the gate R56
   ordered; it was green at 3bb82a25 and stays green, which is the POINT: it is the blind one.
 - `python3 -m ruff check --preview packages/orchestration/exec_guard.py
   tests/orchestration/test_exec_guard.py` — exit 0 AFTER C3. The reviewer ran this exact command
   at 3bb82a25 and got exit 1 with `Found 1 error.`, a single `E305` at
   `tests/orchestration/test_exec_guard.py:691`, and ran it over that file's blob at 49a3fdcb and
   got `All checks passed!` — so these two paths are otherwise preview-clean and this reading is
   about R56's blank line and nothing else. REPORT the exit code and the full output.

G6 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer collected
by grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. The
reviewer projected 44 lines mechanically by applying the pair to that file's blob at 3bb82a25.

G7 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
3bb82a25 and at HEAD, from the line-start patterns for a registration, a resolution and a landed
line. The reviewer's base reading is 172 / 27 / 0, 145 open, max registered R-0557, max resolved
R-0532. At HEAD the reading must be 173 / 27 / 1, 146 open, max registered R-0558: the registered
symmetric difference is exactly R-0558, the landed symmetric difference is exactly R-0558, and the
done symmetric difference is EMPTY. Next free id R-0559. Report all three symmetric differences,
the duplicate-id count and the count of resolutions naming an unregistered id, at both SHAs.

G8 HYGIENE. `git diff --name-only 3bb82a25..HEAD` measured BEFORE C5 holds exactly the change set
above minus `.agent/handoff.md`, which C5 writes, and nothing else — and in particular holds
NEITHER `packages/orchestration/exec_guard.py` NOR `packages/orchestration/ui_server.py`. Report
per-commit insertions for every commit BEFORE C5 — C5 cannot measure itself, so its own insertions
go in the round report — and confirm none exceeds 500. This branch spent the AGENTS.md
declared-oversize allowance at d4473f85, so a second oversize commit is a STOP under constraint 11,
never a declaration. Confirm every commit is single-parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base
SHA 3bb82a25, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2,
C3, C4 and C5, the real G1-G8 results with exit codes, the open-findings count and the next
expected action. The Bundle above names seven commits, which is more than five, so the ≤100-line
allowance applies; if the mandated content genuinely does not fit even that, name the DECISION D15
stated cause and the specific mandated content behind the overage, and drop no section.
Repeat this Fortschritt line verbatim:
Fortschritt: ~94 % (T001 gebaut · R13-R55 PASS · R56 FAIL, an R57 repariert · T002a KOMPLETT ·
T002b KOMPLETT · T002c KOMPLETT · T002d zur Hälfte — Naht, Extraktion und die Umgebungszeile
gebaut, die fünf Call-Sites offen · T003 offen) — Schätzung, gegen die Klassentabelle aus
Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: the next round is
R58, which migrates the two `runtime-build` call sites in `_auto_build_frontend`
(`packages/orchestration/ui_server.py`) onto `run_guarded_runtime_build_command` with `check=True`.
Then the three `runtime-server` sites, then T003, the integration gate and closure. TWO: R58 also
carries the reviewer-authored `Done: R-0558` that resolves this round's finding, replacing the
`Landed:` line C4 writes, and the R57 verdict, because the round that records a verdict cannot
record one on itself (docs/agents/planner_reviewer_prompt.md §4.13). THREE: a standalone closing
line stating the open findings count and the next free id as its own sentence. FOUR:
`Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, which the self-drive protocol requires
every handoff naming a next action to put ahead of the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN11F
## Current Step
R56, this round: settle the npm environment question T002d's second half depends on. The
`runtime-build` allowlist row is widened from the bare `test` set to the npm and node
CONFIGURATION keys a build reads, each key named in full so no credential spelled `NPM_CONFIG_*`
passes with them, and two tests pin both halves. No call site migrates here. The R55 PASS is
recorded in the same round.

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
END-PLAN11F

BEGIN-PLAN11T
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
END-PLAN11T

BEGIN-FIXBLANKF
    assert b"before" in (caught.value.output or b"")

#: The npm and node CONFIGURATION keys the `runtime-build` row adds to the `test` base.
END-FIXBLANKF

BEGIN-FIXBLANKT
    assert b"before" in (caught.value.output or b"")


#: The npm and node CONFIGURATION keys the `runtime-build` row adds to the `test` base.
END-FIXBLANKT

BEGIN-RECORD25
Gate: R57 — the R56 entry. R56 FAILED, and the failure is the reviewer's, not the worker's. Every
ordered gate G1-G8 was re-executed by the reviewer over 49a3fdcb..3bb82a25, not read, and each
reproduces the handback's reading exactly; the worker deviated in nothing, applied every slice
byte-verbatim and declared its scratch honestly. LINE COUNTS ARE `splitlines` COUNTS. TRANSPORT
HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no digest fallback: `.remedy-wt/`'s
`f085-r56.md`, the committed `.agent/authored/f085-r56.md` and the committed `.agent/last_block.md`
at 3bb82a25, and both of those working copies as they stand at 3bb82a25, are all five byte-EQUAL at
sha256 1a9fcbdbd41463fd0fcd2116837d2ec6dec100304614149609db5b467a33cb82, 24319 B, 345 lines, 12
marker lines, which is the digest the reviewer emitted. THE SHAPES HELD. Both REWRITES give
`TO contains FROM: false`, FROM 1x in the pre-commit blob and 0x after with the TO exactly 1x:
PLAN10F→PLAN10T at 9a218ec1 numstat `10 12`, and ALLOWF→ALLOWT at 94574142 numstat `17 3`. THE
PROSE APPEND RECORD24 on `.agent/live_review.md` at 33c99b54: byte-exact prefix, a remainder of
exactly one blank line plus the slice, an exact suffix, 0 marker LINES, and each of its 32
non-empty slice lines occurring exactly once among the 33 lines that commit adds, numstat `33 0`.
THE CODE APPEND TESTSNPM on `tests/orchestration/test_exec_guard.py` at 94574142 held under ORDERED
EQUALITY, numstat `44 0`: the post-commit file equals `pre + "\n" + slice` byte-exactly and that
commit's added lines are one blank line followed by the slice's lines IN ORDER. THE SUITES AND THE
ORDERED LINT WERE RE-RUN, NOT READ, in the primary checkout with the block's exact command lines,
each exit 0: the guard suite `35 passed` against a base of 33, the four state readers `159 passed`
against 159, the canary `42 passed` against 42, and ruff `All checks passed!`. THE PLAN CONTRACT
HELD at 9a218ec1: 44 lines against the 50-line cap with `## Goal`, `## Next Steps` and a roadmap
F-id present — 44 is the figure that block projected. THE ARITHMETIC DID NOT MOVE, as that round
required: 172 / 27 / 0 and 145 open at 49a3fdcb and the same at 3bb82a25, all three symmetric
differences EMPTY. HYGIENE IS CLEAN: the per-commit INSERTION counts over that range are 345, 244,
10, 33, 61 and 38 for the handback commit; none over 500; the path set measured before the handback
excludes `packages/orchestration/ui_server.py` as that change set ordered; all six commits are
single-parent. THE WIDENING ITSELF IS RIGHT AND STAYS: the reviewer proved in a disposable worktree
at 3bb82a25, since removed, that reverting the row reddens both new tests while the other 33 stay
green, and that making `scrub_child_env` match `NPM_CONFIG_` as a PREFIX leaks
`NPM_CONFIG__AUTHTOKEN` into the child and reddens the second test alone — so the by-name-never-by-
prefix property the row depends on is pinned rather than asserted. WHAT FAILED is one blank line,
registered below.

- R-0558 — a block claimed a PEP 8 blank-line property for a code append that a one-blank-line join
cannot produce, and the ordered lint gate was structurally blind to the result. Low. The R56 block's
CONVENTION said "TESTSNPM is CODE joined to its target by exactly one blank line, so the file keeps
the two-blank-line separation PEP 8 puts between top-level definitions". Those two clauses
contradict each other: joining with ONE blank line yields ONE, and at 3bb82a25
`tests/orchestration/test_exec_guard.py` separates `_RUNTIME_BUILD_ADDED_ENV_KEYS` from the
function above it by a single blank line, where that same file separates `_ENV_DUMP` from the
function above IT by two. `ruff check --preview` over that path at 3bb82a25 reports exactly one
`E305 blank-lines-after-function-or-class`, and over the same path's blob at 49a3fdcb reports
`All checks passed!`, so the violation is this round's and the file was otherwise preview-clean.
It is LOW because nothing behavioural moved and every ordered gate is honestly reproducible; what
it cost is a formatting violation in a production test file and a false sentence in the permanent
record. THE GATE COULD NOT HAVE CAUGHT IT: this repository runs `ruff` without `--preview` and
E301-E306 are preview-only, which finding R-0500 already recorded, so the reviewer's own
pre-emission dry run — which ran the block's exact ordered command, per checklist item 12 — was
blind in precisely the way that item exists to prevent. Running the whole repository under
`--preview` is NOT the counter-measure: 634 preview findings exist across `packages/`, `tests/`
and `apps/` at 3bb82a25, and sweeping them is the churn AGENTS.md's Code Discoverability section
forbids as its own activity. THE COUNTER-MEASURE IS TWO-PART, and R57 performs both. First, a code
slice CARRIES the blank lines its target's convention requires INSIDE the slice, so the separation
is a property of bytes that were measured rather than a consequence of a join shape that was
reasoned about. Second, a block whose change set appends to a `.py` file gates it with
`ruff check --preview` over THAT path alone, and only after the reviewer has read that path at the
base commit and found it preview-clean — a file with pre-existing preview findings takes the
narrower reading instead of a gate nobody can pass. Found by the reviewer while gating R56.
END-RECORD25
