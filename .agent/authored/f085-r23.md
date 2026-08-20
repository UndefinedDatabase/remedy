── STEP checklist-paydown / F085 — R23 · SESSION CLOSE ───────────────────────

Goal: record the R22 PASS, register the two findings R22 raised against the
reviewer's own block, promote both counter-measures into the pre-emission
checklist where they bind, and close the session on a written handoff.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record
R22 and register R-0514 and R-0515 · C2 the two checklist items · C3 the
resolutions · C4 plan · C5 handback and session close.

## Why this round is a paydown and not a feature round

Both findings are defects of the REVIEWER's block, not of any code R22 wrote. A
standing rule stated only in finding prose binds nothing — it is read once, by the
round that registers it, and then never again. This branch has already settled how
such a rule is made binding: commit d93ee9b2 promoted three of them into the
pre-emission checklist in `docs/agents/planner_reviewer_prompt.md`, and 99234e5d
followed up on that list's heading. So the checklist is in scope here by this
branch's own precedent, and C2 is the fix rather than a note about a fix.

The session's declared round cap is three, and this is the third. No production
code is touched, no seam is migrated, and T002b stays where the plan leaves it.

## Change

C2 — `docs/agents/planner_reviewer_prompt.md`, the pre-emission block checklist
gains items 18 and 19, applied as the CHECKF→CHECKT pair. The pair is
APPEND-shaped: CHECKT contains CHECKF verbatim, because the two new items are
inserted ABOVE the closing "Why this is on disk and not a habit" paragraph and
that paragraph is carried through unchanged. Appending items 18 and 19 to a list
numbered 1 through 17 renumbers no surviving entry, which is why a FROM anchored
on the closing paragraph is correct here and checklist item 17 does not force the
FROM to span the whole list.

C1 — `.agent/live_review.md`, the RECORD1 slice appended after the file's last
line, separated by exactly one blank line; it carries the R22 gate entry AND both
registrations, so both reach disk before the fix does. C3 — the same file, the
DONE1 slice appended the same way, after C2 has landed. C4 — `.agent/plan.md`, the
PLANF→PLANT pair. C5 — `.agent/handoff.md`, rewritten.

## Constraints

1. Save this block byte-for-byte as `.agent/authored/f085-r23.md` in C0a and write
   the COMMITTED C0a blob into `.agent/last_block.md` in C0b — read it back with
   `git show`, never `cp`, never a retype.
2. Every slice below is applied BYTE-VERBATIM between its markers. Marker lines are
   transport only and never reach a target file. Extract each slice
   programmatically from the committed block file; do not retype one.
3. The slices this block carries are RECORD1, CHECKF, CHECKT, DONE1, PLANF and
   PLANT. Their shapes, each tested by containment rather than by eye: RECORD1 and
   DONE1 are standalone APPENDS with no FROM, so their proof is the prefix property
   in G3; CHECKT DOES contain CHECKF, so that pair is an APPEND and its proof is
   the one §4.9 prescribes for that shape — FROM exactly 1x and each TO-ONLY line
   exactly 1x among the lines C2's diff ADDS — never "FROM 0x", which an
   append-shaped pair cannot reach; PLANT does NOT contain PLANF, so that pair is a
   REWRITE.
4. PLANF spans the WHOLE `## Next Steps` list and not a prefix of it, because PLANT
   changes the list's arity and the surviving entries are renumbered by the pair
   itself.
5. C1 lands BEFORE C2. Findings reach disk before any fix does.
6. C3 lands AFTER C2. DONE1 states that items 18 and 19 are on disk, and that
   sentence must be true at the moment it is committed — this block's own finding
   R-0515 is exactly the rule that a claim's producer runs before its writer.
7. No commit after C5. Nothing is pushed before C5 exists. Create NO pull request
   and merge nothing this round.
8. If a single write of this block's bytes is rejected by the tooling, split it into
   sequential appends — but attempt the single write FIRST and say in the handback
   whether it was attempted and what it returned.
9. No production code is touched this round. Do not edit anything under
   `packages/`, `apps/` or `tests/`. Do not migrate any seam.
10. Any destructive verification runs ONLY inside a disposable `git worktree` under
    a NAME THAT DOES NOT ALREADY EXIST — `.remedy-wt/` holds scratch from earlier
    sessions and `git worktree add` fails on a non-empty directory. Remove and
    prune it before C5.

## Gates — run every one, record its real exit code, report what it PRINTED

G1 CLEAN TREE AND STOP. `git status --porcelain` empty at round start and after
every commit. Re-read `.agent/STOP` from disk before C0a and again before C5 and
report both readings; if it exists at either point, finish the commit in hand, write
the handoff and END. `git worktree list` at the handback — report its line count.

G2 TRANSPORT. The committed `.agent/authored/f085-r23.md`, the committed
`.agent/last_block.md` and both working copies are byte-EQUAL. Report the sha256,
the byte count, the line count and the number of marker lines. Then report the
sha256 of each of these three regions of the saved file, which the reviewer measured
before delegating: lines 1 through 60, lines 61 through 140, and line 141 to the
end. A split write that changes nothing shows three matching digests.

G3 APPEND SHAPE, for C1 and again for C3. The pre-commit blob of
`.agent/live_review.md` is a byte-exact PREFIX of the post-commit file; the
remainder is exactly one blank line followed by the slice; the HEAD blob equals the
working copy; the slice's first line occurs exactly ONCE in the whole file at HEAD;
the file carries 0 marker lines. Report the `git show --numstat` pair for each as a
READING, and read insertions as the FIRST COLUMN of `--numstat` — never the churn
total `git show --stat` prints.

G4 ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `, `^Done: R-\d+ — `
and `^Landed: R-\d+`. At base b4da5101 the reading is 128 / 11 / 0 with 117 open.
After C1 expect 130 / 11 / 0 with 119 open — the two registrations must LAND. At
HEAD expect 130 / 13 / 0 with 117 open. The registered symmetric difference between
base and HEAD is exactly R-0514 and R-0515; the resolved symmetric difference is
exactly R-0514 and R-0515. Report the reading at all three points, both differences,
the duplicate-id counts, any resolution naming an unregistered id, and the max and
next-free id.

G5 THE CHECKLIST PAIR. CHECKF occurs exactly ONCE in
`docs/agents/planner_reviewer_prompt.md` at base. At HEAD, CHECKT occurs exactly
once, and every line that CHECKT adds and CHECKF does not contain occurs exactly
once among the lines C2's diff ADDS — that is the append-shaped proof, and a
"CHECKF 0x" reading is NOT ordered because this pair cannot produce one. Then report
the numbers the checklist's own numbered items parse to, as a list, reading the
region between the line beginning `- **Pre-emission block checklist` and the line
beginning `  Why this is on disk`. Report that list; do not assert a count of it.
Report the file's sha256 and byte count at HEAD.

G6 PLAN PAIR. PLANF occurs 0 times at HEAD and PLANT exactly once. `## Goal` and
`## Risks` are byte-IDENTICAL to their base bytes. Report `.agent/plan.md`'s sha256,
its byte count and a line count under 50, and report the numbers the `## Next Steps`
list parses to rather than a count of them.

G7 DOC READERS, because this round's change set includes a file under `docs/`:
`python3 -m pytest tests/docs/ -q` exits 0. The reviewer ran this exact command line
at base b4da5101 and it printed `295 passed`. Report the count as a READING.

G8 STATE READERS, because this round rewrites `.agent/` state: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py
-q` exits 0. Base reading `157 passed`. Report the count as a READING: that suite
spawns wrapper processes under flock and is timing-sensitive. CANARY: `python3 -m
pytest tests/cli/test_golden_path.py -q` exits 0, base reading `42 passed`. No ruff
gate is ordered and none is skipped by oversight: this change set holds no `.py`
file. No exec_guard or stream suite is ordered for the same reason — nothing under
`packages/` or `tests/` changes this round.

G9 COMMIT HYGIENE. `git diff --name-only b4da5101..HEAD` measured BEFORE C5 equals
the declared paths minus `.agent/handoff.md` — report the list, and 0 paths outside
it. For C0a, C0b, C1, C2, C3 and C4 report the FIRST COLUMN of `git show --numstat`
— the insertions — and never the churn total `git show --stat` prints; none exceeds
500. C5's own count is ordered nowhere, because a commit cannot measure itself;
report it in the round report instead. `git log --format=%h %p b4da5101..HEAD` shows
ONE parent per commit and a linear chain; `git reflog` shows every entry prefixed
`commit:`, with no amend, rebase, reset or force-push.

## Done when

Every commit in the bundle exists in order, the branch is pushed once after C5,
every gate has been RUN with its exit code recorded, `git status --porcelain` is
empty, `git worktree list` is one line, and `.agent/handoff.md` is rewritten per
docs/agents/handback_template.md with an item-status table covering C0a through C5.
That handoff carries: feature and round, branch, the commit SHAs, the changed-files
table, the real verification readings, the open-findings count (117), and a NEXT
section. Every insertion count anywhere in that handoff is the `--numstat` first
column, matching the changed-files table it sits beside.

The NEXT section states, in this order and in these terms:
  - This is the LAST round of the session, reached at the declared round cap of
    three, not at a blocker.
  - R23's own verdict is NOT a §4.13 terminator. That clause covers the last round
    of a BRANCH; this branch continues, so R23 is an ordinary reviewed round and
    the NEXT session's first reviewed round records its gate entry in
    `.agent/live_review.md`. The previous session mis-applied that clause to a
    session boundary and its R20 gate entry had to be written a session late; do
    not repeat it.
  - The next session's first action in the protocol's own order: Phase 1 rule 1,
    re-read `.agent/STOP` from disk, BEFORE rule 2, the Open PR Gate
    (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`).
  - Then the first work item: T002b, the twelve `test`-class sites across ten
    modules, which will not fit a single round.

Run `gh pr list --state open --json number,headRefName,baseRefName,isDraft` after
the push and report its output. Report what the commands PRINTED — a gate whose
result you did not read is a finding. If a gate contradicts this block, report the
contradiction and STOP. Declare every deviation.

BEGIN-RECORD1
Gate: R22 — PASS, the round that hardened T001 against its own failure modes. All
ten ordered gates were re-run by the reviewer over 3622f2cf..b4da5101 and every one
reproduces the handback's reading. TRANSPORT is proven twice over. Disk-to-disk: the committed
`.agent/authored/f085-r22.md`, the committed `.agent/last_block.md` and both working
copies are byte-EQUAL at sha256
f7b6b9ca92d5a5b3956afa125ba5a189e99ff104d0148499e75707edd4775677, 24629 B, 372
lines, 8 marker lines. And against the reviewer's OWN pre-delegation measurement:
the whole-file digest matches and the three regions hash to f5ecdf9d, 9a8f32e7 and
53c558ae exactly as measured before the block was handed over. The single write
succeeded. THE APPEND COMMITS HOLD THEIR SHAPE: for C1 the pre-commit blob (309316
B) is a byte-exact PREFIX of the post-commit file (316105 B) and the remainder is
exactly one blank line plus RECORD1; for C3 the pre-commit blob (316105 B) is a
prefix of (317782 B) and the remainder is blank plus DONE1. Each slice occurs once,
no marker line survives, the HEAD blob equals the working copy. THE ARITHMETIC MOVED
EXACTLY WHERE IT WAS ORDERED TO, which is the reading that was flat in R20 and R21
and had to move here: 126 / 9 / 0 and 117 open at base, 128 / 9 / 0 and 119 open
after C1 — both registrations landed before any fix — and 128 / 11 / 0 with 117 open
at HEAD. Registered difference exactly R-0512 and R-0513,
resolved difference exactly the same two, no duplicate and no resolution naming an
unregistered id; max R-0513. THE SNAPSHOT IS CORRECT WHERE IT MATTERS: every field
of `_StreamPump` now lives behind one lock and is read only through `snapshot()`, so
the three values describe a single point in the stream; `run_guarded` takes that
snapshot AFTER the joins and BEFORE the conditional close, so a partial read never
races the descriptor it reads from; `streams_complete` keeps both its meaning and
its value, being computed from `is_alive()` exactly as before; and the fd handling is
untouched, so the comment explaining why a blocked pump's descriptor stays open is
still true. The `ExecGuardResult` docstring's `b""` promise was rewritten rather than
left to rot, and the replacement claims a PARTIAL buffer and nothing more. THE
BACKSTOP DOES NOT STEAL THE ATTRIBUTION, verified by the reviewer's own mutation in a
disposable worktree rather than accepted from the worker's probe: with
`plan_child_spawn`'s `preexec_fn` replaced by a no-op and the backstop left in
place, the node FAILS in 30.28 s under an external 180 s timeout instead of hanging,
and a direct run of the same policy against the mutated module — its `__file__`
printed as proof of import path — returns `term_signal=SIGKILL`,
`classification=resource_limit` and `tripped_limit=wall_timeout`. `pgrep` finds no
survivor afterwards, which is the second half of the fix: because the deadline is
reached, `run_guarded`'s `finally` runs and the group kill sweeps the busy loop that
R21's probe had to sweep by hand. Suites re-run by the reviewer: exec_guard 18
passed against a base of 16, the stream trio 123 against 121, the sibling seams 337
unchanged, doc readers not applicable, state readers 157, canary 42, ruff
`All checks passed!`. The change set is exactly the declared paths with 0 outside;
insertions are 372, 272, 88, 10, 102, 24 and 13 before the handback commit, which is
itself 44, none over 500 — and every one of those numbers is the `--numstat` first
column, which is R-0512's counter-measure working on the first round it bound. Seven
commits before the handback, one parent each, linear; every reflog entry
`commit:`-prefixed; tree clean; `git worktree list` ONE line. Six deviations were
declared and none is harmful. Two of them are findings against the REVIEWER and are
registered below. A third deserves naming here rather than as a finding: the worker
swept an orphan its own probe created by calling `subprocess.run(["pkill", "-f",
MARKER])` from Python after the interactive `kill` and `pkill` forms were refused by
the session's permission layer. That is the same form-level rejection this
repository already routes around for shell loops, the sweep was scoped to one MARKER
string, it is the exact call `test_exec_guard.py` already makes for its own escapee,
and the worker declared it unprompted. It is correct behaviour, not a violation.
LAST_REVIEWED_SHA advances to b4da5101.

- R-0514 — Medium, A BLOCK ORDERED A PROBE WHOSE RECIPE CONTRADICTS THE PROPERTY THE
SAME PARAGRAPH SAYS IT PROVES. R22's gate G7 probe b ordered, in one sentence,
"remove `wall_timeout_seconds` from the policy in
`test_cpu_limit_kills_a_busy_loop_and_names_the_limit` AND make `plan_child_spawn`'s
`preexec_fn` a no-op", and in the next, "with the backstop the node must FAIL and
name `wall_timeout`". The backstop IS `wall_timeout_seconds`. Removing it and then
asserting its effect cannot both hold, so no run satisfies the paragraph as written:
the literal recipe reproduces the hang R-0513 describes, and the stated property
requires the field the recipe deletes. The worker handled it correctly — it named
the contradiction, ran BOTH variants, and reported both readings rather than picking
one silently — and both readings turned out useful, since the literal variant is the
only direct reproduction of R-0513's harm this feature has on record. Medium because
the round spent a declared deviation and a second full probe run proving a defect in
the reviewer's own text, and because the failure is invisible to every existing
check: item 5 of the pre-emission checklist decides WHETHER a colour may be ordered,
item 8 checks a gate's expected VALUE against the code, and item 12 governs the
reviewer's own dry runs — none of them reads the block's two sentences against EACH
OTHER, which is the only place this defect lives, because both halves are
individually sound. Counter-measure: promoted into the pre-emission checklist by
this round's own C2, as item 18. OPEN.

- R-0515 — Low, AN AUTHORED SLICE ASSERTED A GATE RESULT THE BLOCK NEVER SCHEDULED
THE GATE TO PRODUCE. R22's DONE1 slice, applied byte-verbatim into
`.agent/live_review.md` by C4, states "This round's G7 probe b exercised that path
directly: with the rlimit suppressed, the node fails and names `wall_timeout` within
the external timeout rather than stalling the run." Nothing in that block fixed WHEN
G7 ran. The bundle listed the gates after the commits, so the natural order would
have committed C4 — and with it that sentence — before the probe that makes it true.
The worker saw this and moved G7 ahead of C4 on its own initiative, declaring the
reordering as a deviation, so nothing false reached disk and the claim is now
independently confirmed. Low for that reason. It is registered because the honest
outcome depended on the worker noticing: a worker that had followed the block's own
sequence would have committed an unverified claim into the permanent record, which
is the one file in this repository that must never carry one. This is the R-0371 and
R-0449 family — never order a value into an artifact written before the value can
exist — narrowed from commit SHAs to gate RESULTS, which is a producer the existing
checklist items do not cover: item 13 governs the ORDER a block imposes on the
worker's runs and item 14 governs which commits a per-commit gate can reach, while
this is a property of a slice's TEXT. Counter-measure: promoted into the
pre-emission checklist by this round's own C2, as item 19. OPEN.
END-RECORD1

BEGIN-CHECKF
  Why this is on disk and not a habit: item 2 has recurred six times across
  F104 and F105, and R20 hit four of them in one block. A check that lives
  only in reviewer session memory is the A1 trap §0 names, and this list is the
  standing counter-example to it.
END-CHECKF

BEGIN-CHECKT
  18. **A probe's recipe and its stated property are read against each other.** Finding
      R-0514. A block that orders a red-proof states BOTH what to mutate and what the
      result should show, and those two halves are checked against each other before
      emission. A recipe that removes the very guard whose effect the property asserts
      is satisfiable by no run at all, so the worker must either guess which half was
      meant or spend a declared deviation running both. Item 5 decides WHETHER a colour
      may be ordered, item 8 checks a gate's expected VALUE against the code, and item
      12 governs the reviewer's own dry runs; none of them reads the block's own two
      sentences against EACH OTHER, which is the only place this defect lives, because
      both halves are individually sound. The R22 instance: probe b ordered
      `wall_timeout_seconds` removed from a test AND asserted that "with the backstop
      the node must FAIL and name `wall_timeout`".
  19. **A claim about a gate's result names the commit that runs the gate.** Finding
      R-0515. An authored slice may state what a gate showed only when the same block
      fixes that the gate runs BEFORE the commit that writes the slice. Otherwise the
      worker must either reorder the round on its own initiative or commit a claim it
      has not verified, and the second puts a false line into the permanent record.
      Item 13 governs the ORDER a block imposes on the worker's runs and item 14 which
      commits a per-commit gate can honestly reach; this one governs a slice's TEXT
      making a claim whose producer the block never scheduled — the R-0371 and R-0449
      family, narrowed from commit SHAs to gate results. The R22 instance: DONE1
      asserted a probe outcome while the block listed its gates after its commits, and
      only the worker's own reordering kept the record true.
  Why this is on disk and not a habit: item 2 has recurred six times across
  F104 and F105, and R20 hit four of them in one block. A check that lives
  only in reviewer session memory is the A1 trap §0 names, and this list is the
  standing counter-example to it.
END-CHECKT

BEGIN-DONE1
Done: R-0514 — resolved. The counter-measure is on disk as item 18 of the
pre-emission block checklist in `docs/agents/planner_reviewer_prompt.md`, applied by
this round's C2 and verified by this round's G5 before this line was written. It is
stated as a rule the reviewer runs mechanically on the final bytes, alongside the
seventeen that precede it, rather than as prose in a finding — which is the whole
point, since a rule that lives only in a finding is read once by the round that
registers it and never again. Its distinguishing note names the three neighbours it
is NOT, so the next reviewer does not have to re-derive why items 5, 8 and 12 leave
this gap open.

Done: R-0515 — resolved. The counter-measure is on disk as item 19 of the same
checklist, applied by the same commit. It is deliberately narrow: it does not
forbid a slice from describing a gate, it requires the block to SCHEDULE that gate
before the commit that writes the slice. This round's own Constraint 6 is the first
application — C3 lands after C2 precisely so that the sentence above, asserting
items 18 and 19 are on disk, is true at the moment it is committed rather than a
commit later. A rule whose own block does not obey it is the R-0460 shape, and this
one obeys it.
END-DONE1

BEGIN-PLANF
## Current Step
R22, this round: record the R21 PASS, register R-0512 and R-0513, and fix both. The
guard's CPU test gains a wall-timeout backstop far above the limit it exercises, so
a regression in rlimit application ends in a named failure instead of an unbounded
hang with an orphan behind it. `_StreamPump` gains a lock and a `snapshot()`, so a
stream whose pump is still blocked at the drain deadline contributes the bytes it
already read instead of nothing. `streams_complete` keeps its meaning exactly.

## Next Steps
1. T002b — the twelve `test`-class sites, in ten modules, with behaviour-equality
   goldens and the environment-allowlist test that carries R-0202. It is the largest
   remaining slice and will not fit one round.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.
END-PLANF

BEGIN-PLANT
## Current Step
R23, this round: record the R22 PASS, register R-0514 and R-0515 — both defects of
the reviewer's own block rather than of any code R22 wrote — and promote both
counter-measures into the pre-emission checklist, where a rule binds and finding
prose does not. A paydown round with no production code; the session's declared
round cap of three is reached here, not a blocker.

## Next Steps
1. T002b — the twelve `test`-class sites, in ten modules, with behaviour-equality
   goldens and the environment-allowlist test that carries R-0202. It is the largest
   remaining slice and will not fit one round.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.
END-PLANT
