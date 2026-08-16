── STEP R8 — F085 Sandbox hardening (stage 1) ────────────────

Goal:
Record the R7 PASS, resolve R-0496, and fix R-0495: the wall timeout bounds the
CHILD but not `run_guarded`'s own return, because a descendant that calls
`setsid` leaves the process group, survives `_kill_process_group`, keeps the
inherited pipe write ends open and blocks the untimed `out_pump.join()` /
`err_pump.join()` for its whole life. The drain gets a bounded grace, the result
gains `streams_complete`, and a new test holds the property. Reviewer probe at
`d37d1a1e`, escapee sleeping 20s, `wall_timeout_seconds=1.0`: unfixed 20.13s,
fixed 6.00s (deadline + 5.0s grace), `streams_complete=False`, no survivors.
Findings persist FIRST (docs/agents/planner_reviewer_prompt.md §4 item 4).

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f085-r8.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/live_review.md`: LANDED-R0496 := DONE-R0496, += RECORD-R7, += R0499
  C2  `packages/orchestration/exec_guard.py` := the guard pairs applied
  C3  `tests/orchestration/test_exec_guard.py` += the NEW-TEST slice at EOF
  C4  `.agent/plan.md` whole file := the PLAN slice
  C5  rewrite `.agent/handoff.md` (the handback)

Base:
This round starts from `d37d1a1eba7ffdc7e332e8a7ab4c9c9eedf368bf`, the R7 handback
commit and the current tip of `feature/f085-sandbox-hardening`. Every range gate
below names that SHA. Stay on this branch; do not create a new one.

Slice convention:
Each authored unit below sits between a `<<<SLICE NAME>>>` marker and a
`<<<END NAME>>>` marker, each occupying a line whose ENTIRE content is that
marker. Extract each slice programmatically by those marker LINES and apply it
byte-verbatim; a `<<<` that appears mid-line inside a slice is prose and never a
marker. No marker line ever reaches a target file. The slices are PLAN,
RECORD-R7, R0499, LANDED-R0496, DONE-R0496, NEW-TEST, and the guard pairs GUARD1-FROM
and GUARD1-TO, GUARD2-FROM and GUARD2-TO, GUARD3-FROM and GUARD3-TO, GUARD4-FROM
and GUARD4-TO, GUARD5-FROM and GUARD5-TO, GUARD6-FROM and GUARD6-TO, GUARD7-FROM
and GUARD7-TO. Every slice's bytes end with a single trailing newline, and a
whole-file slice is the COMPLETE file including it.

Round type: SPLIT. The change set reaches `packages/`, so the reviewer gates and
you execute; the single-writer rule of docs/agents/self_drive_protocol.md is
unchanged — the reviewer writes nothing, you write everything.

──────────────────────────────────────────────────────────────

Change:

1. C0a — write this ENTIRE block, byte for byte, to `.agent/authored/f085-r8.md`.
   The reviewer's original is on disk at `.remedy-wt/f085-r8.md` and its expected
   sha256 is stated in the delegation that carries this block; copy that file
   rather than retyping it (`shutil.copyfile` is fine — the gate names the byte
   property, not the tool). Verify the digest BEFORE committing. Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f085-r8.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — `.agent/live_review.md`, two edits in ONE commit, in this order:
   a. replace the LANDED-R0496 slice — which is currently the LAST line of the
      file — with the DONE-R0496 slice. This is a REWRITE pair: only reviewer
      text sets Resolved, so the worker's `Landed:` record is retired here
      (docs/agents/planner_reviewer_prompt.md §4 item 4);
   b. append the RECORD-R7 slice, then the R0499 slice, each preceded by exactly
      one blank line.
   The pre-C1 content MINUS its final LANDED-R0496 line must remain a byte-exact
   PREFIX of the post-C1 content, and nothing before that line may change.

4. C2 — `packages/orchestration/exec_guard.py`. Apply every GUARD pair, each
   FROM replaced by its TO. Each FROM occurs EXACTLY ONCE in the file before its
   edit; if any occurs zero times or more than once, stop and declare it rather
   than choosing an occurrence. Shapes, stated at authoring time (§4.9):
   GUARD1, GUARD2, GUARD3, GUARD4 and GUARD7 are APPEND-shaped — each TO contains
   its FROM verbatim. GUARD5 and GUARD6 are REWRITES — their TO does not contain
   their FROM. Change nothing else in this file.

5. C3 — `tests/orchestration/test_exec_guard.py`: append the NEW-TEST slice at the
   END of the file, preceded by exactly one blank line, so the file ends with the
   new test. Nothing already in the file is touched, and no other file is.

6. C4 — `.agent/plan.md` whole file := the PLAN slice. Commit alone.

7. C5 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its
   state block repeats this Fortschritt line verbatim:
   `Fortschritt: ~35 % (F085 beansprucht · Amendment F085 D1 angewandt · T001 gebaut · R7 PASS · R-0495 und R-0496 gefixt · T002 entsperrt, offen · T003 offen) — Schätzung`
   Its "Next" section states exactly this:
   - T002a is UNBLOCKED by this round and is R9's work: the builder class, five
     call sites, the first seam migration;
   - `_StreamPump` still returns `b""` for a stream whose pump never reached EOF,
     so partial output is LOST on an incomplete drain — honest, because
     `streams_complete` says so, and lossy; the `snapshot()` refinement is named
     in the plan and is not claimed here;
   - a stream still blocked at the grace deadline leaks one pipe read end and one
     daemon thread, which the guard docstring states as the deliberate tradeoff;
   - `exec_guard.py` still has NO callers, so no containment claim holds for the
     running system;
   - there is NO open PR for this branch and none is opened before closure;
   - the R8 verdict is written by the NEXT round's record commit.

──────────────────────────────────────────────────────────────

Constraints:

1. AGENTS.md is the highest authority. Self-review loop before every commit; push
   after committing.
2. Every slice is applied BYTE-VERBATIM. If a slice cannot be applied as-is, stop
   and declare it — never adjust the bytes to make a gate pass.
3. The ONLY files this round may change are the ones named in the ordered bundle.
   Do NOT touch `.agent/f085_inventory.md`, `.agent/context.md`,
   `docs/roadmap/STATUS.md`, `docs/roadmap/features/T2_F085.md` or
   `docs/roadmap/ROADMAP.md`.
4. Do not migrate any call site onto the guard this round: T002 is R9's work and
   `exec_guard.py` still has no callers when this round ends. Do not "improve"
   anything else in either file while you are in it.
5. Never force-push, never rebase, never amend, never reset, never work on `main`,
   never delete a branch. Do not create a PR.
6. Re-read `.agent/STOP` from disk before the FIRST commit and again at the
   handback. If it exists at either point, finish the commit in flight, write the
   handoff and end.
7. If any gate below is red, do not repair it by editing the thing it measures.
   Record the real command, the real exit code and the real output, and hand back.

──────────────────────────────────────────────────────────────

Done when — every command run from the repository root with `pwd` confirmed,
every real exit code recorded:

G1  `git status --porcelain` is EMPTY at the handback. `git worktree list` is ONE
    line. `.agent/STOP` absent at both readings.
G2  TRANSPORT: `.remedy-wt/f085-r8.md`, the committed `.agent/authored/f085-r8.md`
    and the committed `.agent/last_block.md` are byte-EQUAL and share one sha256.
    Report that digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD is byte-equal to the PLAN slice; report its sha256 and
    line count; it contains `## Goal`, `## Next Steps` and a `\bF\d{3}\b` match, and
    is under 50 lines.
G4  `.agent/live_review.md`: take the pre-C1 blob, strip its final LANDED-R0496
    line, and confirm the remainder is a byte-exact PREFIX of the post-C1 content.
    Report the post-C1 remainder after that prefix and confirm it equals the
    DONE-R0496 slice, a blank line, the RECORD-R7 slice, a blank line and the
    R0499 slice, byte for byte. Report `git show --numstat` for that path at C1.
G5  Open-set recomputation at HEAD with the two regexes `^- R-\d+ — ` and
    `^Done: R-\d+ — `: report registered, resolved, duplicate ids and resolutions
    naming an unregistered id. REQUIRED: the REGISTERED set at HEAD equals the
    registered set at `d37d1a1e` PLUS exactly `R-0499`, with nothing lost, and the
    RESOLVED set at HEAD is exactly `{R-0496}` against an empty resolved set at
    `d37d1a1e`. Report both counts and the symmetric difference rather than
    predicting them, plus the max id and the next free id. Separately report the
    number of LINE-START records matching `^Landed: R-\d+`, which must be 0 — the
    one that existed at `d37d1a1e` is the line C1 retires.
G6  `.agent/live_review.md` still contains the substring `Steps`.
G7  `git diff --name-only d37d1a1e..HEAD` lists exactly this set and nothing else:
    `.agent/authored/f085-r8.md`, `.agent/handoff.md`, `.agent/last_block.md`,
    `.agent/live_review.md`, `.agent/plan.md`,
    `packages/orchestration/exec_guard.py`,
    `tests/orchestration/test_exec_guard.py`. Report the real list. NO path under
    `docs/`, `apps/` or `scripts/` may appear.
G8  PAIR PROOF, `packages/orchestration/exec_guard.py` at HEAD, over the WHOLE
    file: for GUARD5 and GUARD6 — the REWRITES — report that the FROM text occurs
    0 times and the TO text exactly 1 time. For GUARD1, GUARD2, GUARD3, GUARD4 and
    GUARD7 — the APPENDS — report that the TO text occurs exactly 1 time. Also
    report `git show --numstat` of C2 for that path.
G9  NO CALLER, the counter-proof to constraint 4: report the SET of files in
    `grep -rn "exec_guard" packages/ apps/ scripts/ tests/`. It must contain no
    entry other than `tests/orchestration/test_exec_guard.py` — the module never
    writes its own name inside itself, so it cannot appear there (R-0497).
G10 `python3 -m ruff check packages/orchestration/exec_guard.py tests/orchestration/test_exec_guard.py`
    → exit 0, using the repository's OWN configuration. Do NOT pass `--isolated`:
    it discards `pyproject.toml` and with it the lint rules this gate exists to
    run (R-0463).
G11 DETERMINISM: run `python3 -m pytest tests/orchestration/test_exec_guard.py -q`
    TEN times in a row and report the real exit code AND the real summary line of
    EACH of the ten runs, in order. ALL TEN must be exit 0 and all ten must read
    `7 passed`. The reviewer measured twelve consecutive `7 passed` runs, exit 0,
    on a scratch worktree carrying exactly these slices, so ten greens is a
    reading this code supports and not a hope (R-0498 counter-measure).
G12 RED CONTROL, inside a DISPOSABLE `git worktree` at HEAD and NEVER in the
    primary checkout (planner_reviewer_prompt.md §4 item 10): in that worktree
    ONLY, replace the single line
    `            pump.join(max(drain_deadline - time.monotonic(), 0.0))`
    with `            pump.join()` and run
    `python3 -m pytest tests/orchestration/test_exec_guard.py -q -rf` there. Report
    the exit code, the summary line and every `-rf` FAILED node id. The reviewer
    measured `1 failed, 6 passed`, exit 1, failing at
    `test_wall_timeout_bounds_the_call_when_a_descendant_escapes_the_group` on
    `assert result.streams_complete is False`. Remove and prune the worktree
    afterwards; `git status --porcelain` in the primary checkout stays EMPTY
    throughout.
G13 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, the canary. The
    reviewer measured `42 passed`, exit 0, at `d37d1a1e`.
G14 PROBE, not a colour — run the eight-file structural sweep THREE times and report
    each real exit code and each real summary line:
    `python3 -m pytest tests/orchestration/test_autonomy.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/test_no_interactive_guard.py tests/orchestration/test_review_subject_resolution.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py -q -rf`
    The reviewer measured `350 passed, 6 skipped`, exit 0, three times out of three
    at `d37d1a1e`. If a run is red, report the FAILED node id verbatim from `-rf`
    and hand back. Do not repair it and do not re-run until it goes green.
G15 Per-commit insertions — the `+` column of `git show --numstat` — for C0a, C0b,
    C1, C2, C3 and C4 only. None may exceed 500. C5's own count is ordered nowhere
    and the reviewer measures it at the next gate (R-0494, checklist item 14).
    `git log --format=%p d37d1a1e..HEAD` shows one parent per commit (linear), and
    `git reflog` over this round shows only `commit:` entries — no amend, rebase,
    reset, checkout of another branch, or force-push.

Verification tier: round gate (§3 tier 1) plus the canary at G13. The docs-round
gate of tier 5 is NOT triggered: this round's change set contains no
`docs/roadmap/**` path.

Handback:
Completion report + rewrite `.agent/handoff.md`. Push with
`git push origin feature/f085-sandbox-hardening`. Do NOT open a PR.

──────────────────────────────────────────────────────────────

<<<SLICE GUARD1-FROM>>>
    `env` is passed through unchanged: scrubbing is T002, not stage 1.
<<<END GUARD1-FROM>>>

<<<SLICE GUARD1-TO>>>
    `env` is passed through unchanged: scrubbing is T002, not stage 1.
    `stream_drain_grace_seconds` is the TOTAL extra time the guard will wait for
    both stream pumps after the child is reaped, so a descendant that escaped the
    process group and still holds the pipe cannot extend the call without bound.
<<<END GUARD1-TO>>>

<<<SLICE GUARD2-FROM>>>
    wall_timeout_seconds: float | None = None
<<<END GUARD2-FROM>>>

<<<SLICE GUARD2-TO>>>
    wall_timeout_seconds: float | None = None
    stream_drain_grace_seconds: float = 5.0
<<<END GUARD2-TO>>>

<<<SLICE GUARD3-FROM>>>
    limit is never silent.
<<<END GUARD3-FROM>>>

<<<SLICE GUARD3-TO>>>
    limit is never silent.

    `streams_complete` is False when a stream pump was still blocked when the
    drain grace ran out — an escaped descendant holding the inherited pipe. In
    that case the pump never reached EOF, so ITS `stdout`/`stderr` field is `b""`
    and only `stdout_bytes_seen`/`stderr_bytes_seen` describe what the child
    produced. A guard that returns on time and says so is better than one that
    blocks for the escapee's whole life to keep the bytes.
<<<END GUARD3-TO>>>

<<<SLICE GUARD4-FROM>>>
    stderr_bytes_seen: int
<<<END GUARD4-FROM>>>

<<<SLICE GUARD4-TO>>>
    stderr_bytes_seen: int
    streams_complete: bool
<<<END GUARD4-TO>>>

<<<SLICE GUARD5-FROM>>>
    path, so no descendant outlives this call.
<<<END GUARD5-FROM>>>

<<<SLICE GUARD5-TO>>>
    path, so no descendant of THAT GROUP outlives this call.

    A descendant that calls `setsid` leaves the group and the kill cannot reach
    it (R-0495). It still holds the inherited pipe write ends, so the guard drains
    the streams under `stream_drain_grace_seconds` and returns with
    `streams_complete=False` rather than waiting for EOF that may never come:
    `wall_timeout_seconds` bounds the CHILD, and the two together bound THIS CALL.
<<<END GUARD5-TO>>>

<<<SLICE GUARD6-FROM>>>
        out_pump.join()
        err_pump.join()
        proc.stdout.close()
        proc.stderr.close()
<<<END GUARD6-FROM>>>

<<<SLICE GUARD6-TO>>>
        # ONE deadline for BOTH pumps, so the grace is a total cost and not a
        # per-stream one that a second blocked pump could double.
        drain_deadline = time.monotonic() + policy.stream_drain_grace_seconds
        for pump in (out_pump, err_pump):
            pump.join(max(drain_deadline - time.monotonic(), 0.0))
        streams_complete = not (out_pump.is_alive() or err_pump.is_alive())
        if streams_complete:
            # Closed ONLY when no pump is still reading: closing a descriptor under
            # a blocked reader risks that thread reading a recycled fd after a later
            # open(). The pumps are daemons, so a leaked pair is the cheaper wrong.
            proc.stdout.close()
            proc.stderr.close()
<<<END GUARD6-TO>>>

<<<SLICE GUARD7-FROM>>>
        stderr_bytes_seen=err_pump.bytes_seen,
<<<END GUARD7-FROM>>>

<<<SLICE GUARD7-TO>>>
        stderr_bytes_seen=err_pump.bytes_seen,
        streams_complete=streams_complete,
<<<END GUARD7-TO>>>

<<<SLICE NEW-TEST>>>
@pytest.mark.subprocess
def test_wall_timeout_bounds_the_call_when_a_descendant_escapes_the_group():
    """A grandchild in its OWN session survives the kill and keeps holding the pipe.

    The deadline must still bound `run_guarded`'s own return (R-0495): the drain
    grace is a bounded cost on top of the deadline, not the escapee's lifetime.
    """
    escapee = (
        "import subprocess, sys, time\n"
        "subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(20)', sys.argv[1]],\n"
        "                 start_new_session=True)\n"
        "time.sleep(120)\n"
    )
    started = time.monotonic()
    result = run_guarded(
        _child(escapee),
        ExecGuardPolicy(wall_timeout_seconds=1.0, stream_drain_grace_seconds=2.0, output_cap_bytes=64 * 1024),
    )
    elapsed = time.monotonic() - started

    assert result.tripped_limit == "wall_timeout"
    assert result.streams_complete is False
    # Upper bound only: the escapee sleeps 20s, so any return well under that is
    # the property. Deadline + grace is ~3s here; 10s leaves room for a slow box.
    assert elapsed < 10.0

    # The escapee outlives the guard BY DESIGN, so this test ends it rather than
    # leaving a MARKER process that a later test's pgrep sweep would find.
    subprocess.run(["pkill", "-f", MARKER], check=False)
    for _ in range(10):
        if not _survivors():
            break
        time.sleep(0.2)
    assert _survivors() == []
<<<END NEW-TEST>>>

<<<SLICE PLAN>>>
# Plan — F085 Sandbox hardening (stage 1)

Branch: feature/f085-sandbox-hardening, cut from origin/main at a5a70621 after
the F083 closure PR #202 and the amendment PR #203 merged.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
Builder-spawned commands stop relying on prompted discipline: every builder,
test and DoD subprocess gets POSIX resource limits, a per-command wall timeout,
output-size caps, a cwd pinned inside the worktree, an environment allowlist and
a default-deny network posture — with a document that says EXACTLY what stage 1
does and does not prevent. DONE when the limits provably kill a runaway fixture
(cpu, memory, oversized output, endless sleep) and classify it `resource_limit`
with the tripped limit named, an off-scope write attempt fails, well-behaved
commands behave identically under the guard, a secret-like parent env var never
reaches a child, and the limitations document exists and is linked from the
README.

## Current Step
R8, this round: record the R7 PASS, resolve R-0496, and fix R-0495 — the wall
timeout that bounds the child but not `run_guarded`'s own return. The drain gets
a bounded grace and the result says whether the streams were complete.

## Next Steps
1. T002a — builder class, 5 sites, the first seam migration. UNBLOCKED by this
   round: the guard now bounds its own wall time, so migrating a seam onto it
   makes hangs easier to see rather than harder.
2. `_StreamPump` gains a lock and a `snapshot()` so PARTIAL output survives a
   bounded drain. R8 returns `b""` for a stream whose pump never reached EOF,
   which `streams_complete` reports honestly but which loses bytes.
3. T002b-d, then T003 — network posture, limitations document, README link.

## Risks
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading a
  recycled fd after a later `open()`, so the leak is the cheaper wrong.
- The address-space limit is enforced but NOT attributable from `wait4` data;
  R5's G16 probe confirmed it. Whether stage 1 can name that trip stays open.
<<<END PLAN>>>

<<<SLICE LANDED-R0496>>>
Landed: R-0496 — the marginal assertion now compares `cpu_seconds_used` against 0.5 instead of against the 1.0 RLIMIT_CPU limit it sat exactly on, with the kernel-accounting reason in a comment above it; `tests/orchestration/test_exec_guard.py`, commit C2 of R7.
<<<END LANDED-R0496>>>

<<<SLICE DONE-R0496>>>
Done: R-0496 — RESOLVED at R7. `assert result.cpu_seconds_used >= 1.0` became `assert result.cpu_seconds_used >= 0.5` in `test_cpu_limit_kills_a_busy_loop_and_names_the_limit`, with a comment above it naming the kernel-accounting reason the old value was a boundary: `ru_utime + ru_stime` rounds against RLIMIT_CPU rather than exactly to it. The counter-measure the finding asked for is met — the tolerance is strictly BELOW the limit and the property the test is named for, the SIGXCPU trip, is asserted separately and unchanged. The reviewer verified the fix by running `python3 -m pytest tests/orchestration/test_exec_guard.py -q` TEN times at d37d1a1e: ten exits of 0, ten `6 passed` summaries, against 8 red of 12 measured at ca5ff4f1 before the fix. The coin flip is gone by measurement rather than by assertion. Commit e77fa588, `7 1` on that path.
<<<END DONE-R0496>>>

<<<SLICE RECORD-R7>>>
Gate: R7 — PASS. Every one of the fifteen ordered gates was re-run by the reviewer from the repository root at d37d1a1e and every one reproduces the handback's reading; the round declared no deviation of substance and none was found. TRANSPORT, against the reviewer's OWN scratchpad original and NOT by digest fallback (§4.9): `.remedy-wt/f085-r7.md`, the committed `.agent/authored/f085-r7.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 f6fd67339f3c9745fb845b95a1fcb5649373c70c410a5852d97a3a7a027ca6af, 21267 B, 253 lines. `.agent/plan.md` at HEAD byte-equals the PLAN slice at sha256 1a2b4a3ed34f4a4ade3ffef65f2d307aebe67b64e549c1439a26ba7434920a45, 2297 B, 40 lines, under the 50-line cap, carrying `## Goal`, `## Next Steps` and an F-id. Both live_review appends are honest: the 225757 B base blob is a byte-exact PREFIX of the 231728 B post-C1 file, which is itself a byte-exact PREFIX of the 231994 B HEAD blob, and the numstats are `4 0` at C1 and `2 0` at C3 with both deletion columns zero. The open set moved by exactly one: 112 registered / 0 resolved / 112 open at ca5ff4f1 against 113 / 0 / 113 at HEAD, HEAD-open minus base-open = {R-0498} and base-open minus HEAD-open = {}, 0 duplicate ids, 0 resolutions naming an unregistered id, max R-0498 and next free R-0499. Exactly one LINE-START `^Landed: R-\d+` record exists and it names R-0496, which is the shape §4 item 4 asks for and which THIS round retires into the authored `Done:` above. The substring `Steps` survives 21 times. The change set is exactly the six ordered paths with nothing under `packages/`, `docs/`, `apps/` or `scripts/`, and the UNCHANGED GUARD holds: `packages/orchestration/exec_guard.py` is byte-identical at ca5ff4f1 and at HEAD at sha256 d9c77caec4ed9136868cef080bd2e2ae18c4216851507dc943d778d5c575114e, 12241 B, so constraint 4 held and no part of R-0495's fix leaked into the test round. The CPU-ASSERT pair is a REWRITE and reads as one: the FROM occurs 0 times at HEAD, the TO line exactly 1 time, numstat `7 1`. No marker line reached a target file — 0 `<<<SLICE` and 0 `<<<END` in `.agent/plan.md`, `.agent/live_review.md` and `tests/orchestration/test_exec_guard.py` — and the handback's claim about the single pre-existing `<<<` in `.agent/live_review.md` is exact: 1 occurrence at ca5ff4f1 and 1 at HEAD, in authored prose about a former gate. THE COIN FLIP IS GONE, measured and not asserted: ten consecutive runs of `python3 -m pytest tests/orchestration/test_exec_guard.py -q` at the reviewer's own hand are ten exits of 0 and ten `6 passed` summaries between 4.55s and 4.60s, against the 8 red of 12 the reviewer measured at ca5ff4f1 — which is what R-0498's counter-measure asks a colour gate to establish before it is ordered. `python3 -m ruff check` on the test file is exit 0 under the repository's own configuration; the canary is `42 passed in 20.49s`, exit 0; the eight-file structural sweep is `350 passed, 6 skipped`, exit 0, three times out of three. Per-commit insertions are C0a 253, C0b 156, C1 4, C2 7, C3 2 and C4 12, none over 500, and the history is seven single-parent commits d0e597a3←ca5ff4f1 through d37d1a1e with a reflog of `commit:` entries only. The values R7 routed nowhere are recorded HERE, measured by the reviewer at d37d1a1e, which is the R-0494 counter-measure working as designed: the handback commit d37d1a1e inserted 58 lines and deleted 42, `.agent/handoff.md` measures 103 lines against its own DECISION D15 declaration of 103 so its self-measurement is honest, `git status --porcelain` is EMPTY, `git worktree list` is one line, and origin carries d37d1a1e with no PR open. LAST_REVIEWED_SHA advances to d37d1a1e.
<<<END RECORD-R7>>>

<<<SLICE R0499>>>
- R-0499 — Low, THE EIGHT-FILE STRUCTURAL SWEEP GOES RED ABOUT ONCE IN TWENTY RUNS INSIDE A FRESH GIT WORKTREE, AND THE FAILING NODE ID HAS NEVER BEEN CAPTURED. Raised by the reviewer at the R8 authoring dry run. Two observations exist and both are inside a disposable worktree, never in the primary checkout: the F085 R7 worker saw one red in 22 runs on a scratch worktree carrying a larger draft change and did not capture the node id, and the reviewer saw one red in 14 runs on the R8 dry-run worktree and did not capture it either, because the run that produced it was not the run that carried `-rf` output to the log. The red reading is `1 failed, 348 passed, 7 skipped` against the green `350 passed, 6 skipped`, so a test that normally PASSES was SKIPPED in the same run that another test failed — which is the signature of an environment-conditional skip rather than of a logic defect. The sweep's only environment-conditional member is `test_typescript_compiles` in `tests/ui_server/test_dashboard_contract.py`, which resolves `apps/ui/node_modules/.bin/tsc` relative to the file's own tree, skips with "UI toolchain absent" when that path is missing, and otherwise shells out to a REAL `tsc --noEmit` under `timeout=30` — the one member of the eight-file sweep that depends on a heavy external toolchain and on wall-clock. `node_modules` is gitignored, so a fresh worktree's copy of it is populated out of band and its state at the worktree's FIRST sweep run is not something the sweep controls. Nothing in the F085 change set reaches any of the eight files, so this is a pre-existing property of the gate and not of the guard. Counter-measure, already applied in the block that registers this finding: the sweep is ordered as a PROBE carrying `-rf`, never as an expected COLOUR, and a red run reports its FAILED node id verbatim and hands back rather than re-running until green — which is the only way the id gets captured. The finding resolves when a red run finally names the test. Whether `test_typescript_compiles` belongs in a structural sweep at all is a question for the F252 flake work and is NOT claimed here. OPEN.
<<<END R0499>>>
