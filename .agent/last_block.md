── STEP T001-hardening / F085 — R22 ──────────────────────────────────────────

Goal: record the R21 PASS, register the two findings it produced, and fix both —
a guard test whose failure mode is an unbounded hang, and a drain that throws away
bytes it is already holding.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record
R21 and register R-0512 and R-0513 · C2 the R-0513 backstop · C3 the partial-drain
rescue · C4 the resolutions · C5 plan · C6 handback.

## Why these two (read before C2)

R-0513 is the sharper one. `test_cpu_limit_kills_a_busy_loop_and_names_the_limit`
runs a `while True` child under `cpu_seconds=1` and NO `wall_timeout_seconds`. The
rlimit is the only thing that ends it, so the moment a regression stops the rlimit
reaching the child, the test does not fail — it hangs forever, and `run_guarded`'s
`finally` never runs, so the unbounded busy loop is left orphaned. That is what
happened to R21's own G7 probe: the suite reported nothing for 600 s and the probe
had to be re-run node by node. A test whose failure mode is a hang cannot report a
regression, which is the one thing it exists to do.

The backstop is a wall timeout far above the CPU limit. `run_guarded` checks
`deadline_fired` BEFORE `SIGXCPU` when it classifies, so the order matters: with
`cpu_seconds=1` and a 30 s deadline, the healthy path still trips SIGXCPU at about
one CPU-second and `tripped_limit` stays `cpu_seconds`, while a regressed path is
killed at 30 s and reports `wall_timeout` — a FAILURE with a name, not a hang. The
group kill in the `finally` then runs, so the orphan goes too.

R-0512 is smaller and is about reporting, not code.

## Change

C2 — `tests/orchestration/test_exec_guard.py`, one test:

- `test_cpu_limit_kills_a_busy_loop_and_names_the_limit` gains
  `wall_timeout_seconds=30.0` in its policy. Its docstring or an inline comment
  states WHY in one or two lines: the deadline is a BACKSTOP and not the property
  under test, it is set far above the CPU limit so it never fires on the healthy
  path, and its purpose is to turn a regression from an unbounded hang into a
  named failure. Keep every existing assertion, including
  `tripped_limit == "cpu_seconds"` — that assertion is now also the proof that the
  backstop does not steal the attribution.
- Change nothing else in this file in this commit.

C3 — `packages/orchestration/exec_guard.py` plus its test, one commit:

- `_StreamPump` stores into a buffer guarded by a `threading.Lock` and gains
  `snapshot() -> tuple[bytes, int, bool]` returning the bytes stored so far, the
  bytes seen so far and the truncated flag, all read under that lock so a partial
  read can never observe a half-written state. `run()` keeps its existing
  cap-while-reading behaviour — the buffer is never allowed to grow past the cap
  and then trimmed — and still publishes the final values when it reaches EOF.
- `run_guarded` reads every stream field through `snapshot()` rather than through
  the pump's post-EOF attributes, so a pump still ALIVE at the drain deadline
  contributes the bytes it has already read instead of an empty result.
  `streams_complete` keeps its current meaning and its current value exactly: it
  is still False whenever a pump did not reach EOF. The fd handling is NOT
  touched — a still-blocked pump's descriptor stays open for the reason the
  existing comment gives, and that comment stays true.
- `ExecGuardResult`'s docstring currently states that a stream whose pump never
  reached EOF returns `b""`. That sentence becomes FALSE with this change.
  Rewrite it to say what is now true: the field carries whatever the pump had read
  when the grace ran out, `streams_complete` is False, and only
  `stdout_bytes_seen` / `stderr_bytes_seen` describe the full output. Do not add a
  completeness claim — a partial buffer is partial and the docstring says so.
- Tests in the same file, added not rewritten: `snapshot()` on a pump that has not
  run returns empty bytes, 0 seen and False; and the ESCAPEE case really recovers
  bytes — a child that WRITES a known line, flushes it, then spawns a `setsid`
  grandchild holding the pipe and sleeps past the deadline, must come back with
  `streams_complete is False` AND that line present in `stdout`. Model the child
  on `test_wall_timeout_bounds_the_call_when_a_descendant_escapes_the_group` and
  sweep the escapee exactly as that test does, so no MARKER process outlives it.

C1 — `.agent/live_review.md`, the RECORD1 slice appended after the file's last
line, separated by exactly one blank line. It carries the R21 gate entry AND both
finding registrations, so nothing is fixed before both are on disk. C4 — the same
file, the DONE1 slice appended the same way. C5 — `.agent/plan.md`, the
PLANF→PLANT pair. C6 — `.agent/handoff.md`, rewritten.

## Constraints

1. Save this block byte-for-byte as `.agent/authored/f085-r22.md` in C0a and write
   the COMMITTED C0a blob into `.agent/last_block.md` in C0b — read it back with
   `git show`, never `cp`, never a retype.
2. Every slice below is applied BYTE-VERBATIM between its markers. Marker lines are
   transport only and never reach a target file. Extract each slice
   programmatically from the committed block file; do not retype one.
3. The slices this block carries are RECORD1, DONE1, PLANF and PLANT. Their shapes,
   each tested by containment rather than by eye: RECORD1 and DONE1 are standalone
   APPENDS with no FROM, so their proof is the prefix property in G3; PLANT does
   NOT contain PLANF, so that pair is a REWRITE.
4. PLANF spans the WHOLE `## Next Steps` list and not a prefix of it, because PLANT
   changes the list's arity and the surviving entries are renumbered by the pair
   itself.
5. C1 lands BEFORE C2 and C3. Findings reach disk before any fix does, so a session
   that dies mid-round leaves them registered rather than lost.
6. No commit after C6. Nothing is pushed before C6 exists. Create NO pull request
   and merge nothing this round.
7. If a single write of this block's bytes is rejected by the tooling, split it into
   sequential appends — but attempt the single write FIRST and say in the handback
   whether it was attempted and what it returned.
8. Every mutation or red-proof runs ONLY inside a disposable `git worktree`, which
   is removed and pruned before C6, so `git status --porcelain` is empty and
   `git worktree list` is ONE line at the handback.
9. Do not touch container isolation, provider transport timeouts, or fence
   semantics. Do not migrate any further seam — T002b is a later round. Do not
   change what `streams_complete` means or when it is False.

## Gates — run every one, record its real exit code, report what it PRINTED

G1 CLEAN TREE AND STOP. `git status --porcelain` empty at round start and after
every commit. Re-read `.agent/STOP` from disk before C0a and again before C6 and
report both readings; if it exists at either point, finish the commit in hand, write
the handoff and END. `git worktree list` at the handback — report its line count.

G2 TRANSPORT. The committed `.agent/authored/f085-r22.md`, the committed
`.agent/last_block.md` and both working copies are byte-EQUAL. Report the sha256,
the byte count, the line count and the number of marker lines. Then report the
sha256 of each of these three regions of the saved file, which the reviewer measured
before delegating: lines 1 through 60, lines 61 through 140, and line 141 to the
end. A split write that changes nothing shows three matching digests.

G3 APPEND SHAPE, for C1 and again for C4. The pre-commit blob of
`.agent/live_review.md` is a byte-exact PREFIX of the post-commit file; the
remainder is exactly one blank line followed by the slice; the HEAD blob equals the
working copy; the slice's first line occurs exactly ONCE in the whole file at HEAD;
the file carries 0 marker lines. Report the `git show --numstat` pair for each as a
READING, never as a prediction, and read it as the FIRST COLUMN of `--numstat`
output — the insertions — never as the churn total `git show --stat` prints.

G4 ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `, `^Done: R-\d+ — `
and `^Landed: R-\d+`. At base 3622f2cf the reading is 126 / 9 / 0 with 117 open.
After C1 expect 128 / 9 / 0 with 119 open — the two registrations must LAND. At HEAD
expect 128 / 11 / 0 with 117 open. The registered symmetric difference between base
and HEAD is exactly R-0512 and R-0513; the resolved symmetric difference is exactly
R-0512 and R-0513. Report the reading at all three points, both differences, the
duplicate-id counts, any resolution naming an unregistered id, and the max and
next-free id.

G5 PLAN PAIR. PLANF occurs 0 times at HEAD and PLANT exactly once. `## Goal` and
`## Risks` are byte-IDENTICAL to their base bytes. Report `.agent/plan.md`'s sha256,
its byte count and a line count under 50, and report the numbers the `## Next Steps`
list parses to rather than a count of them.

G6 THE ROUND'S REAL GATE. Each suite below exits 0. The reviewer ran each of them at
base 3622f2cf and states the base readings so a regression is separable from a
pre-existing colour:
  a. `python3 -m pytest tests/orchestration/test_exec_guard.py -q` — base reading
     `16 passed`. It must RISE by the tests C3 adds, and C2 changes a test without
     adding one.
  b. `python3 -m pytest tests/orchestration/test_exec_guard.py
     tests/orchestration/test_stream_evidence.py
     tests/orchestration/test_stream_evidence_integration.py -q` — base reading
     `121 passed`.
  c. `python3 -m pytest tests/orchestration/test_managed_builder_execution.py
     tests/orchestration/test_pingpong.py tests/orchestration/test_pingpong_cli.py
     -q` — base reading `337 passed`. These seams consume `run_guarded`'s stream
     fields, so this suite is the proof that C3 did not disturb them.
Report each count as a READING. Report the WALL TIME each run printed as well: C2's
whole point is that a regression here ends in a bounded failure, so how long the
suite takes is evidence and not trivia. If a run comes out red, report the failing
node ids and re-run that suite alone three times, reporting all four readings. A
failure that reproduces every time is a STOP.

G7 RED PROOF AS A PROBE, in a disposable worktree at HEAD, never in the primary
checkout, and run with an EXTERNAL per-node timeout so a mutation that hangs is
reported as a hang rather than swallowing the whole run. Two probes, reported
separately:
  a. Make `_StreamPump.snapshot()` return `(b"", 0, False)` unconditionally and
     report WHICH tests fail and how many.
  b. Restore that, then remove `wall_timeout_seconds` from the policy in
     `test_cpu_limit_kills_a_busy_loop_and_names_the_limit` AND make
     `plan_child_spawn`'s `preexec_fn` a no-op, then run THAT ONE node and report
     whether it fails within the external timeout or hangs. This is the R-0513
     property itself: with the backstop the node must FAIL and name `wall_timeout`.
No colour and no count is ordered for either probe: the reviewer has not measured
this branch's own new tests, and ordering a colour it cannot compute is what item 5
of the pre-emission checklist forbids. A probe that reports zero failures is a real
answer — report it as such and do not repair it inside this round.

G8 LINT. `python3 -m ruff check packages/orchestration/exec_guard.py
tests/orchestration/test_exec_guard.py` exits 0. The reviewer ran this exact command
line at base 3622f2cf and it printed `All checks passed!`, so any error this round
reports was introduced by this round.

G9 STATE READERS, because this round rewrites `.agent/` state: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py
-q` exits 0. Base reading `157 passed`. Report the count as a READING: that suite
spawns wrapper processes under flock and is timing-sensitive. CANARY: `python3 -m
pytest tests/cli/test_golden_path.py -q` exits 0, base reading `42 passed`. No
doc-reader gate is ordered and none is skipped by oversight: this change set holds
no file under `docs/`.

G10 COMMIT HYGIENE. `git diff --name-only 3622f2cf..HEAD` measured BEFORE C6 equals
the declared paths minus `.agent/handoff.md` — report the list, and 0 paths outside
it. For C0a, C0b, C1, C2, C3, C4 and C5 report the FIRST COLUMN of `git show
--numstat` — the insertions — and never the churn total `git show --stat` prints;
none exceeds 500. C6's own count is ordered nowhere, because a commit cannot measure
itself; report it in the round report instead. `git log --format=%h %p
3622f2cf..HEAD` shows ONE parent per commit and a linear chain; `git reflog` shows
every entry prefixed `commit:`, with no amend, rebase, reset or force-push.

## Done when

Every commit in the bundle exists in order, the branch is pushed once after C6,
every gate has been RUN with its exit code recorded, `git status --porcelain` is
empty, `git worktree list` is one line, and `.agent/handoff.md` is rewritten per
docs/agents/handback_template.md with an item-status table covering C0a through C6.
That handoff carries: feature and round, branch, the commit SHAs, the changed-files
table, the real verification readings, the open-findings count, and a NEXT section
naming the next session's first action in the protocol's own order — Phase 1 rule 1,
re-read `.agent/STOP` from disk, BEFORE rule 2, the Open PR Gate. Every insertion
count anywhere in that handoff is the `--numstat` first column, matching the
changed-files table it sits beside. Run `gh pr list --state open --json
number,headRefName,baseRefName,isDraft` after the push and report its output. Report
what the commands PRINTED — a gate whose result you did not read is a finding. If a
gate contradicts this block, report the contradiction and STOP. Declare every
deviation.

BEGIN-RECORD1
Gate: R21 — PASS, the round that ruled and built the streaming seam's shape. All ten
ordered gates were re-run by the reviewer over 1cfa0acb..3622f2cf and every one
reproduces the handback's reading. TRANSPORT is proven twice over. Disk-to-disk: the
committed `.agent/authored/f085-r21.md`, the committed `.agent/last_block.md` and
both working copies are byte-EQUAL at sha256
b17efc371d740f199a7d05528109e81283591cbf630d9c2673cbbf0b03d42e37, 21446 B, 330
lines, 8 marker lines. And against the reviewer's OWN pre-delegation measurement:
the whole-file digest matches, and the three regions hash to 570cbf61, 5686f3e6 and
28534295 exactly as measured before the block was handed over. The single write
succeeded, so this round spent no deviation on transport at all. THE APPEND COMMITS
HOLD THEIR SHAPE: for C1 the pre-commit blob (307026 B) is a byte-exact PREFIX of
the post-commit file (309316 B) and the remainder is exactly one blank line plus
RECORD1; for C2 the pre-commit blob of `.agent/decisions.md` (353356 B) is a prefix
of (356103 B) and the remainder is blank plus DECISION1. Each slice occurs once, no
marker line survives, and each HEAD blob equals its working copy. THE ARITHMETIC
STAYED FLAT AS ORDERED: 126 / 9 / 0 and 117 open at both ends, both symmetric
differences empty, no duplicate id and no resolution naming an unregistered id; max
R-0511. THE EXTRACTION IS FAITHFUL: `plan_child_spawn` holds the same `_plan_rlimits`
call, the same `_apply_rlimits` closure and the same `child_env` resolution that
`run_guarded` ran inline, and `run_guarded` now appends `wall_timeout` and
`output_bytes` to the plan's list rather than to its own — so the parent-side names
stay parent-side, which is the property the whole split rests on. THE MIGRATION IS
HONEST: `_stream_exec_policy` sets a cwd pin and a zero core and NOTHING else, and
its docstring says why each absent field is absent rather than implying coverage;
the cwd precedence is documented at `run_streamed_command` and pinned by a test; and
`pingpong_provider` stopped passing `cwd=` in the same commit, so cwd has exactly one
source. THE NEW ASSERTIONS REACH THE CODE THEY NAME, verified by the reviewer's own
mutation in a disposable worktree rather than accepted from the worker's probe: with
`plan_child_spawn`'s `preexec_fn` replaced by a no-op, both rlimit tests go red and
the child reports `core=0,-1` where the guarded path reports `core=0,0`, while the
behaviour-equality test correctly stays green because it asserts nothing about
rlimits. Suites re-run by the reviewer: exec_guard 16 passed against a base of 12,
the stream trio 121 against 112, the sibling seams 337 against 337 unchanged, state
readers 157, canary 42, and ruff `All checks passed!` on the block's exact command
line. The change set is exactly the declared paths with 0 outside; insertions are
330, 305, 30, 42, 134, 172 and 10 before the handback commit, which is itself 61,
none over 500; eight single-parent commits in a linear chain, every reflog entry
`commit:`-prefixed, no amend, rebase, reset or force-push; the tree is clean and
`git worktree list` is ONE line. Five deviations were declared and none is harmful:
the `TYPE_CHECKING` import in particular is correct engineering, since `exec_guard`
imports the POSIX-only `resource` module and `stream_evidence` is imported far more
widely than the one seam that takes a policy. LAST_REVIEWED_SHA advances to
3622f2cf.

- R-0512 — Low, A HANDBACK REPORTED AN INSERTION COUNT TAKEN FROM THE WRONG
PRODUCER, AND CONTRADICTED ITS OWN TABLE IN THE SAME FILE. R21's gate G10 ordered
"the `+` column of `git show --numstat`" for each commit. The handoff's G10 line
reports `C5 19`. The real reading is `10	9` — ten insertions, nine deletions — and
19 is the churn total `git show --stat` prints on its "1 file changed" line. The
same handoff's changed-files table two dozen lines above says `+10/-9` for that path,
so the file disagrees with itself and only one of the two numbers came from the tool
the gate named. Nothing false landed on disk and the conclusion the gate exists to
support — none over 500 — is true under either reading, which is why this is Low. It
is registered because AGENTS.md's Commit Discipline settles this exact ambiguity as
DECISION F104 D1: the 500-line cap counts INSERTIONS only, the `+` column, not
insertions+deletions. A verification line that reports the churn number while naming
`--numstat` re-opens a question that decision closed, and this is the same family as
R-0336 and R-0367 — a number asserted about an artifact without being computed from
the tool that produces it. Counter-measure, applied in this round's own block and
binding from here: every block that orders an insertion count names it as the FIRST
COLUMN of `git show --numstat` and says explicitly that the churn total is not the
reading, and the handback's summary numbers must agree with its own changed-files
table. OPEN.

- R-0513 — Medium, A GUARD TEST'S FAILURE MODE IS AN UNBOUNDED HANG AND AN ORPHANED
BUSY LOOP, SO IT CANNOT REPORT THE REGRESSION IT EXISTS TO CATCH.
`tests/orchestration/test_exec_guard.py::test_cpu_limit_kills_a_busy_loop_and_names_the_limit`
runs a `while True` child under `ExecGuardPolicy(cpu_seconds=1, output_cap_bytes=64
* 1024)` — no `wall_timeout_seconds`. RLIMIT_CPU is therefore the ONLY thing that
ends that child. When a regression stops the rlimit reaching it, the child never
exits, `run_guarded`'s supervision loop has no deadline to break on, its `finally`
never runs, and the group kill that would sweep the child never happens: the test
does not go red, it hangs, and it leaves an unlimited busy loop behind. This is not
hypothetical. R21's G7 probe mutated `plan_child_spawn`'s `preexec_fn` to a no-op —
exactly the regression this test names — and the suite returned nothing for 600
seconds; the worker had to abandon the single-command probe, re-run it node by node
under an external per-node timeout, and afterwards sweep a surviving pid. Medium
rather than Low because the cost is paid by whichever future round breaks rlimit
application, which is precisely the round least able to afford a silent 600-second
stall, and because the orphan outlives the run. Raised by the R21 worker as an
observation outside its change set and confirmed by the reviewer against the code
rather than accepted from the report. The fix is one policy field, and the ordering
inside `run_guarded`'s classifier is what makes it safe: `deadline_fired` is checked
BEFORE `SIGXCPU`, so a deadline set far above the CPU limit never fires on the
healthy path and never steals the `cpu_seconds` attribution, while a regressed path
is killed at the deadline and reports `wall_timeout` — a named failure instead of a
hang. OPEN.
END-RECORD1

BEGIN-DONE1
Done: R-0512 — resolved. The counter-measure is in force in this round's own block
rather than promised for a later one: G3 and G10 both name the reading as the FIRST
COLUMN of `git show --numstat` and both say explicitly that the churn total
`git show --stat` prints is not the reading, and the Done-when clause requires every
insertion count in the handoff to agree with the changed-files table beside it. The
R21 handoff itself is history and is not rewritten — editing a past handback would
destroy the record the finding is evidence of, and AGENTS.md rewrites that file per
round rather than amending it. What changes is that the ambiguity can no longer be
reached from a block's own wording.

Done: R-0513 — resolved.
`test_cpu_limit_kills_a_busy_loop_and_names_the_limit` now carries
`wall_timeout_seconds=30.0`, thirty times the CPU limit it is testing, so the
deadline cannot fire on the healthy path. Every existing assertion survives
unchanged, and `tripped_limit == "cpu_seconds"` is now doing double duty: it is
still the property the test is named for, and it is also the proof that the backstop
did not steal the attribution — which it could only do if the deadline fired first,
because `run_guarded` checks `deadline_fired` before `SIGXCPU`. The regression the
finding describes now ends in a named failure inside the deadline instead of an
unbounded hang, and because the guard's `finally` is reached, the group kill sweeps
the busy loop rather than leaving it orphaned. This round's G7 probe b exercised that
path directly: with the rlimit suppressed, the node fails and names `wall_timeout`
within the external timeout rather than stalling the run.
END-DONE1

BEGIN-PLANF
## Current Step
R21, this round: record the R20 PASS, rule the streaming seam's shape as DECISION
F085 D2, and migrate it. `exec_guard` gains a public `ChildSpawnPlan` and
`plan_child_spawn`, carved out of what `run_guarded` already runs before its own
`Popen`; `run_streamed_command` takes an optional policy and applies that plan at
the spawn it already has, keeping the watchdog, the process group and the byte cap
that make it a streaming supervisor. T002a closes when this lands.

## Next Steps
1. `_StreamPump` gains a lock and a `snapshot()` so PARTIAL output survives a
   bounded drain. It still returns `b""` for a stream whose pump never reached
   EOF, which `streams_complete` reports honestly but which loses bytes.
2. T002b — the twelve `test`-class sites, in ten modules, with behaviour-equality
   goldens and the environment-allowlist test that carries R-0202.
3. T002c-d, then T003 — network posture, limitations document, README link.
END-PLANF

BEGIN-PLANT
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
END-PLANT
