── STEP close-out — F085 — R46 ───────────────────────────────────────────────

Goal: record the R45 PASS, register R-0547 for the DEC6 heading/body contradiction R45's
worker found in the reviewer's own slice, and append the correction that fixes the ruled
figure at 490 — so neither the verdict nor the finding dies with this session.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record R45,
register R-0547 and append DEC6C · C2 handback.

CONVENTION, binding on every count here: a line count is the `splitlines` reading — a trailing
newline is NOT an extra line.

## Change

C1 appends RECORD14 to `.agent/live_review.md` and DEC6C to `.agent/decisions.md`, and nothing
else. No source file is touched this round.

Change set, named rather than counted: `.agent/authored/f085-r46.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/handoff.md`. Nothing else; neither
`docs/**` nor `docs/roadmap/**` is in that set, so the §3 docs tier does not trigger. No `.py`
path changes, so no lint gate and no code suite is ordered — their absence is declared here
rather than filled with a command that could not see this round's change.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r46.md` by its marker pair. Never retype one, never apply one from
   the prompt. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C2; if it exists, finish the
   commit in flight, write the handback and stop. `git status --porcelain` is empty at round
   start and after every commit; this round orders no destructive check, so it creates no
   worktree and `git worktree list` stays one line.
3. Both of C1's slices are APPENDS of PROSE: each target file stays a byte-exact prefix,
   exactly one blank line joins it to its slice, and no slice is reflowed or re-indented.
   Neither carries a FROM, so no containment reading and no FROM/TO count is owed.
4. DEC6 as it stands at 470d2577 is NOT edited. Its heading and its CHOSEN paragraph disagree,
   and the counter-measure for landed text is an appended correction naming the commit, never
   a rewrite — checklist item 20. DEC6C is that correction.
5. Nothing outside the declared change set is touched. This round registers R-0547 and
   resolves nothing: the open count goes 134 → 135, next free id R-0548.
6. If a gate comes out red, STOP: write the handback naming the exact command, its exit code
   and its output. Never edit a slice to make a gate green.
7. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes it: 490 lines TOTAL, PROSE
   capped at 400. The reviewer measured this block at emission and states both here: PROSE 117,
   TOTAL 192. The worker re-measures both from the committed `.agent/authored/f085-r46.md` and
   reports them; a mismatch is a finding against this block, not against the worker.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain`
empty at round start and after every commit; `git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r46.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the
reviewer's `.remedy-wt/f085-r46.md` — disk-to-disk, not a digest fallback. Report sha256, byte
count, line count and marker-line count. Measure every one.

G3 APPEND SHAPE for C1, measured SEPARATELY for RECORD14 on `.agent/live_review.md` and DEC6C
on `.agent/decisions.md`. For each: the pre-commit blob is a byte-exact PREFIX of its
post-commit file, the remainder is exactly one blank line plus that slice, the slice is an
exact suffix, and 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file — count marker
LINES, never the substring, since that regex already appears in `.agent/live_review.md` prose.
Both are PROSE, so §4.9's per-line obligation applies: every line a slice contains occurs
exactly once among the lines C1's diff adds TO THAT PATH, EXCEPT the empty line — report each
slice's empty-line count. Neither slice was measured to hold a duplicate non-empty line, so a
violation is a transport fault. Report `git show --numstat` for both paths.

G4 SUITE, in the PRIMARY checkout and never in a worktree (R-0518), exit 0:
`python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
tests/ui_server/test_dashboard_contract.py -rf -q` — the four files that read `.agent/` state
live, which is the only class this round's change set can reach; base reading at 470d2577,
taken by the reviewer in the primary checkout, `159 passed`. REPORT the number this run
prints. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

G5 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
470d2577 and at HEAD, from the line-start patterns for a registration, a resolution and a
landed line. The reviewer's base reading is 161 / 27 / 0, 134 open, max registered R-0546, max
resolved R-0532. At HEAD registered must be 162, the registered symmetric difference exactly
R-0547, done and landed symmetric differences EMPTY, 135 open, next free id R-0548. Report the
three symmetric differences, the duplicate-id count and the count of resolutions naming an
unregistered id, at both SHAs.

G6 HYGIENE. `git diff --name-only 470d2577..HEAD` measured BEFORE C2 holds exactly the change
set above minus `.agent/handoff.md`, which C2 writes, and nothing else. Report per-commit
insertions for every commit BEFORE C2 — C2 cannot measure itself, so its own insertions go in
the round report — and confirm none exceeds 500. This branch already spent the AGENTS.md
declared-oversize allowance at d4473f85, so a second oversize commit is a STOP under constraint
6, never a declaration. Confirm every commit has exactly one parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch,
base SHA 470d2577, a per-commit changed-files table, the item-status table covering C0a, C0b,
C1 and C2, the real G1-G6 results with exit codes, the open-findings count and the next
expected action. Keep it inside the 60-line cap, or name the DECISION D15 stated cause and the
exact mandated content behind it. Repeat this Fortschritt line verbatim:
Fortschritt: ~85 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R45 PASS ·
T002a KOMPLETT · T002b KOMPLETT, alle Sites der Klasse auf dem Seam · T002c-d, T003 offen) —
Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section states that the next round is R47 and that a FRESH session starts it;
that R47's first two acts are the checklist item 16 widening R-0537 and R-0543 name and the
correction R-0547 asks the checklist to carry; that T002c then opens with the two DoD sites in
`packages/orchestration/dod_runners.py`, whose policy differs because their children are the
long-lived harness and take no wall timeout; and that T002d, T003, the integration gate and
closure follow. It also states that R46's own verdict is NOT on disk as a gate entry, because
the round that records a verdict cannot record one on itself (§4.13) — that absence is the
terminator, not a missing gate, and R47 must not open a repair round to close it.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-RECORD14
Gate: R46 — the R45 entry. R45 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer
over 981d08d0..470d2577, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT WAS PROVED AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with
no digest fallback: `.remedy-wt/f085-r45.md`, the committed `.agent/authored/f085-r45.md` at
d6f42cd0, the committed `.agent/last_block.md` at 6977b3e8 and both working copies as they stand
at 470d2577 are all five byte-EQUAL at sha256
448c531c3430eafe4efb0080363ff8c4e1908261f5d688bdbf248ce00c163cb0, 29951 B, 477 lines, 30 marker
lines. BOTH APPENDS HELD THEIR SHAPE: for RECORD13 on `.agent/live_review.md` and DEC6 on
`.agent/decisions.md` alike, the pre-commit blob is a byte-exact prefix, the remainder is exactly
one blank line plus the slice, the slice is an exact suffix, 0 marker LINES reached either file,
and every non-empty slice line occurs exactly once among that path's added lines — 97 slice lines
against 98 added for the first, 43 against 44 for the second. THE CODE RECONSTRUCTS:
`packages/orchestration/builder_bridge.py` at 981d08d0 with BBF1→BBT1, BBF2→BBT2 and BBF3→BBT3
applied in that order is byte-identical to the committed file at 778a74ba, sha256
5a95a367a15f9d34…; `tests/orchestration/test_builder_bridge.py` with TIMPF→TIMPT applied and
TESTS appended is byte-identical at dffeaac42c130440…, and the ORDERED EQUALITY holds on the
form G4 ordered — the intermediate text is a byte-exact prefix, TESTS an exact suffix, and the
59 lines C2 adds are TIMPT's two new import lines followed by TESTS' 57, in order. THE SUITES
WERE RE-RUN, NOT READ, each in the primary checkout, each exit 0: the five builder-bridge files
`82 passed, 1 skipped` against a base of `80 passed, 1 skipped`, the four state readers
`159 passed` against 159, and the canary `42 passed` against 42; `ruff check` over the two `.py`
paths returned `All checks passed!`. THE ARITHMETIC MOVED AS ORDERED: 161 / 27 / 0 at 470d2577
against 153 / 27 / 0 at 981d08d0, 134 open against 126, the registered symmetric difference
exactly R-0539 through R-0546, done and landed symmetric differences EMPTY, no duplicate id and
no resolution naming an unregistered id at either SHA. HYGIENE IS CLEAN: walking
981d08d0..470d2577 mechanically gives the per-commit insertion counts 477, 410, 142, 70, 7 and
58, none over 500 and so no second call on the allowance d4473f85 spent; the path set of the
range ending at 7cd2879d is exactly the seven ordered paths; all six commits are single-parent.

THE MIGRATION IS REAL, NOT MERELY APPLIED. `import os` is gone from
`packages/orchestration/builder_bridge.py` at 470d2577 and the one surviving `os.` occurrence is
inside a comment, so the module no longer builds a child environment from the parent's own — the
scrub is what the child now gets. Before delegating, the reviewer proved the same slice bytes in
a disposable worktree at 981d08d0 under four red controls, each of which exited non-zero on the
test it was aimed at: the fixture repo demanding the scrubbed token be PRESENT, the fixture repo
demanding the `PYTHONDONTWRITEBYTECODE` overlay be ABSENT, `extra_env` dropped from the guard
call, and `cwd` handed None — the last taking 60.26 s, which is the guard's own wall tripping
rather than an assertion failing. T002b is closed: every site of the `test` class named in
DECISION F085 D3 is on the seam.

WHAT THE WORKER FOUND IN THE REVIEWER'S OWN TEXT. R45's worker applied every slice byte-verbatim
and declared one contradiction rather than repairing it, which is what constraints 1 and 6 ask
for. R-0547 is that finding. It is the reviewer's error, not the worker's, and the round is a
PASS because the worker's execution reproduced in every particular under independent re-run.

- R-0547 — Medium, A DECISION'S HEADING RULED ONE NUMBER AND ITS BODY RULED ANOTHER. DECISION
F085 D6, applied at 812626d3, is headed "a block is budgeted at 480 lines TOTAL" while its
CHOSEN paragraph rules "a block is budgeted at 490 lines TOTAL" and its CONSEQUENCE paragraph
computes from 490; the R45 block's own Goal and constraint 9 also say 490. Measured at 470d2577:
the DEC6 slice contains the string 480 once, in the heading, and 490 twice, in the body. The
cause is recoverable and worth recording, because it is the shape this repository keeps paying
for: the reviewer drafted the section at 480, revised the ruled figure to 490 in the body when
the margin's justification changed, and did not sweep the heading — the R-0481 late-addition
shape, landing in the one place checklist item 16 already governs and the widening of item 16
that R45 cut for size would have caught. Nothing was decided wrongly: 477 is inside either
figure, so no round was misjudged. What is wrong is that a live rule is ambiguous on disk. DEC6C,
appended by this same commit, fixes the ruled figure at 490 without editing DEC6, per checklist
item 20's rule that landed text is corrected by appending and never by rewriting. Found by R45's
worker under its own deviation 2 and registered by the reviewer.
END-RECORD14

BEGIN-DEC6C
## DECISION F085 D6 — correction to the ruled figure (2026-08-17)

DECISION F085 D6, applied at 812626d3, is internally inconsistent: its heading says 480 lines
TOTAL and its CHOSEN and CONSEQUENCE paragraphs say 490. THE RULED FIGURE IS 490. The CHOSEN
paragraph is the operative one — it carries the reasoning for the margin and the CONSEQUENCE
paragraph computes from it, while the heading is a leftover from an earlier draft in which the
margin was justified differently. Finding R-0547 registers the defect.

D6 is not edited, because appending a correction is how landed text stays honest in this
repository and overwriting it is worse than a dated wrong sentence — docs/agents/planner_reviewer_prompt.md
§3 checklist item 20. A reader who reaches the D6 heading reaches this section too, since both
live in `.agent/decisions.md` and this one is later.

Reverse this correction by deleting this section, which restores the ambiguity rather than the
480; reverse D6 itself by deleting D6, which returns the block cap to DECISION F085 D5's
400-line PROSE rule with no budget on the total.
END-DEC6C
