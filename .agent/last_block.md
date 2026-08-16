── STEP R6 — F085 Sandbox hardening (stage 1) ────────────────

Goal:
Record the R5 FAIL and persist the three findings it produced, then hand off.
This round applies NO fix: findings persist FIRST, in their own commit, so that
nothing is lost if this session ends (docs/agents/planner_reviewer_prompt.md §4
item 4). The repairs are R7's work and the handback names them.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f085-r6.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/live_review.md` += RECORD-R5, then R0495, then R0496, then R0497
  C2  `.agent/plan.md` whole file := the PLAN slice
  C3  rewrite `.agent/handoff.md` (the handback)

Base:
This round starts from `16506c0b5410faa6d452da9cef482ee279d6cd0d`, the R5
handback commit and the current tip of `feature/f085-sandbox-hardening`. Every
range gate below names that SHA. Stay on this branch; do not create a new one.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each slice programmatically by its
markers and apply it byte-verbatim. No marker line ever reaches a target file.
The slices are PLAN, RECORD-R5, R0495, R0496 and R0497. Every slice's bytes end
with a single trailing newline, and a whole-file slice is the COMPLETE file
including it.

Round type: SINGLE-SESSION-eligible by change set (only `.agent/**`), but the
single-writer rule of docs/agents/self_drive_protocol.md is unchanged — the
reviewer writes nothing, you write everything.

──────────────────────────────────────────────────────────────

Change:

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f085-r6.md`. The reviewer's original is on disk at
   `.remedy-wt/f085-r6.md` and its expected sha256 is stated in the delegation
   that carries this block; copy that file rather than retyping it
   (`shutil.copyfile` is fine — the gate names the byte property, not the tool).
   Verify the digest BEFORE committing. Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f085-r6.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — append to `.agent/live_review.md`, in this order, each preceded by
   exactly one blank line, all byte-verbatim, nothing else in the file touched:
   a. the RECORD-R5 slice;
   b. the R0495 slice;
   c. the R0496 slice;
   d. the R0497 slice.
   The pre-C1 content must remain a byte-exact PREFIX of the post-C1 content.

4. C2 — `.agent/plan.md` whole file := the PLAN slice. Commit alone.

5. C3 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its
   state block repeats this Fortschritt line verbatim:
   `Fortschritt: ~25 % (F085 beansprucht · Amendment F085 D1 angewandt · T001 gebaut, R5 FAIL — 3 Findings offen · T002/T003 offen) — Schätzung`
   Its "Next" section states exactly this:
   - R7 is a REPAIR round and fixes R-0495 and R-0496 in that order; R-0497 is a
     reviewer-side gate defect and is fixed by the reviewer's next block, not by
     a worker edit;
   - `tests/orchestration/test_exec_guard.py` is RED at HEAD on
     `test_cpu_limit_kills_a_busy_loop_and_names_the_limit`, deliberately left
     red, and no round may claim this branch is green until R-0496 is resolved;
   - `exec_guard.py` still has NO callers, so no containment claim holds for the
     running system;
   - there is NO open PR for this branch and none is opened before closure;
   - the R6 verdict is written by the NEXT round's record commit.

──────────────────────────────────────────────────────────────

Constraints:

1. AGENTS.md is the highest authority. Self-review loop before every commit;
   push after committing.
2. Every slice is applied BYTE-VERBATIM. If a slice cannot be applied as-is,
   stop and declare it — never adjust the bytes to make a gate pass.
3. The ONLY files this round may change are the ones named in the ordered
   bundle. Do NOT touch `packages/orchestration/exec_guard.py`,
   `tests/orchestration/test_exec_guard.py`, `.agent/f085_inventory.md`,
   `docs/roadmap/STATUS.md`, `docs/roadmap/features/T2_F085.md` or
   `docs/roadmap/ROADMAP.md`.
4. DO NOT FIX ANYTHING THIS ROUND. The red test stays red and the guard stays as
   it is. A round that persists findings and also repairs them cannot prove the
   findings were persisted before the repair, which is the whole point of the
   ordering.
5. Never force-push, never rebase, never amend, never reset, never work on
   `main`, never delete a branch. Do not create a PR.
6. Re-read `.agent/STOP` from disk before the FIRST commit and again at the
   handback. If it exists at either point, finish the commit in flight, write the
   handoff and end.
7. If any gate below is red, do not repair it by editing the thing it measures.
   Record the real command, the real exit code and the real output, and hand back.

──────────────────────────────────────────────────────────────

Done when — every command run from the repository root with `pwd` confirmed,
every real exit code recorded:

G1  `git status --porcelain` is EMPTY at the handback. `git worktree list` is
    ONE line. `.agent/STOP` absent at both readings.
G2  TRANSPORT: `.remedy-wt/f085-r6.md`, the committed `.agent/authored/f085-r6.md`
    and the committed `.agent/last_block.md` are byte-EQUAL and share one sha256.
    Report that digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD is byte-equal to the PLAN slice; report its sha256
    and line count; it contains `## Goal`, `## Next Steps` and a `\bF\d{3}\b`
    match, and is under 50 lines.
G4  `.agent/live_review.md`: the pre-C1 content is a byte-exact PREFIX of the
    post-C1 content, and the appended tail contains the RECORD-R5, R0495, R0496
    and R0497 slices, each byte-verbatim and each exactly once. Report
    `git show --numstat` for that path at C1 and confirm its deletion column is 0.
G5  Open-set recomputation at HEAD with the two regexes `^- R-\d+ — ` and
    `^Done: R-\d+ — `: report registered, resolved, duplicate ids and resolutions
    naming an unregistered id. REQUIRED: the set of OPEN ids at HEAD EQUALS the
    set open at `16506c0b` PLUS exactly `R-0495`, `R-0496` and `R-0497`, and R6
    resolves nothing. Report both counts and the symmetric difference rather than
    predicting them, plus the max id and the next free id. Separately report the
    number of LINE-START records matching `^Landed: R-\d+`.
G6  `.agent/live_review.md` still contains the substring `Steps`.
G7  `git diff --name-only 16506c0b..HEAD` lists exactly this set and nothing
    else: `.agent/authored/f085-r6.md`, `.agent/handoff.md`,
    `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`. Report the
    real list. NO path under `packages/`, `tests/`, `docs/`, `apps/` or
    `scripts/` may appear — this round changes no code, and a path there would
    mean constraint 4 was broken.
G8  UNCHANGED CODE, the counter-proof to constraint 4: report the sha256 of
    `packages/orchestration/exec_guard.py` and of
    `tests/orchestration/test_exec_guard.py` at `16506c0b` and at HEAD. Each pair
    must be equal.
G9  THE RED STAYS RED, and this gate PASSES when the command FAILS — read it
    carefully. Run `python3 -m pytest tests/orchestration/test_exec_guard.py -q`
    and report its real exit code and its real summary line. The reviewer
    measured `1 failed, 5 passed`, exit 1, five times out of five at `16506c0b`,
    failing on `test_cpu_limit_kills_a_busy_loop_and_names_the_limit` at
    `assert result.cpu_seconds_used >= 1.0` with the value `0.999776`. Report
    what YOU get. Do not fix it, do not skip it, do not mark it xfail.
G10 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, the canary.
    The reviewer measured `42 passed`, exit 0, at `16506c0b`.
G11 Per-commit insertions — the `+` column of `git show --numstat` — for C0a,
    C0b, C1 and C2 only. None may exceed 500. C3's own count is ordered nowhere
    and the reviewer measures it at the next gate (R-0494).
G12 `git log --format=%p 16506c0b..HEAD` shows one parent per commit (linear).
    `git reflog` over this round shows only `commit:` entries — no amend, rebase,
    reset, checkout of another branch, or force-push.

Verification tier: round gate (§3 tier 1) plus the canary at G10. The docs-round
gate of tier 5 is NOT triggered: this round's change set contains no
`docs/roadmap/**` path.

Handback:
Completion report + rewrite `.agent/handoff.md`. Push with
`git push origin feature/f085-sandbox-hardening`. Do NOT open a PR.

──────────────────────────────────────────────────────────────

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
R6, this round: record the R5 FAIL and persist its three findings. No fix lands
here — findings persist before repairs so the record survives a session that
ends. `tests/orchestration/test_exec_guard.py` stays RED on purpose.

## Next Steps
1. R7 repairs R-0495 — the wall timeout must bound `run_guarded`'s own return,
   not only the process group it can reach — and then R-0496, the boundary
   assertion that leaves the T001 suite red.
2. T002a — builder class, 5 sites, the first seam migration. It is BLOCKED until
   R-0495 is fixed: migrating a seam onto a guard whose timeout does not bound
   wall time would make hangs harder to see, not easier.
3. T002b-d, then T003 — network posture, limitations document, README link.

## Risks
- R-0495 is the feature's central promise failing in its central case. Until it
  is fixed, no round may describe `exec_guard` as bounding runtime.
- The address-space limit is enforced but NOT attributable from `wait4` data;
  R5's G16 probe confirmed it. Whether stage 1 can name that trip stays open.
<<<END PLAN>>>

<<<SLICE RECORD-R5>>>
Gate: R5 — FAIL. Every ordered gate the reviewer can re-run reproduces at the reviewer's own hand from the repository root at 16506c0b — G1 through G10 and G12 through G15, plus G17 read directly out of the two new files — and the round is failed on G11, which does not; G16 is a worker-side probe of a child process rather than a reproducible reading, and its result is consistent with the reviewer's own rlimit measurements taken while authoring the R5 block. TRANSPORT, against the reviewer's OWN scratchpad original and NOT by digest fallback (§4.9): `.remedy-wt/f085-r5.md`, the committed `.agent/authored/f085-r5.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 4d1188a70d2f8d1ff23f6a5801c212b4406a738c7d6c59d77bb1877047ab9220, 26997 B, 341 lines. `.agent/plan.md` at HEAD byte-equals the PLAN slice at sha256 cbc8ee8a0b3b7196ae4dd9832abb66b009ccbe959ae0706f06f2ec2f266547a8, 41 lines, under the 50-line cap, carrying `## Goal`, `## Next Steps` and an F-id. The C1 append is honest: the pre-C1 blob of 208910 B is a byte-exact PREFIX of the 214867 B post-C1 file, the RECORD-R4 and R0494 slices each occur exactly once in the whole file and both inside the 5957-byte, four-line appended tail, and the numstat is `4 0` with a zero deletion column. The open set moved by exactly one: 108 open at 382ed7fa, 109 at HEAD, symmetric difference against base plus R-0494 EMPTY, 0 duplicate ids, 0 resolutions naming an unregistered id, 0 line-start `^Landed: R-` records. The change set is exactly the seven ordered paths, the history is seven single-parent commits, and the per-commit insertions are C0a 341, C0b 250, C1 4, C2 16, C3 314, C4 170, none over 500. Re-run by the reviewer in the PRIMARY checkout: ruff over the two new files exit 0 `All checks passed!`; the eight-file structural sweep `350 passed, 6 skipped` exit 0, the same reading as at base, so the new orchestration module trips none of the whole-directory guards; the canary `42 passed` exit 0; and G12 clean, the only `pgrep` matches being the reviewer's own probe command line rather than any surviving fixture. The values R5 routed nowhere are recorded HERE, measured by the reviewer at 16506c0b, which is the R-0494 counter-measure working as designed: C3 of the handback inserted 55 lines, the post-C5 change set is the same seven paths, `git status --porcelain` is EMPTY, `git worktree list` is one line, the push landed with origin at 16506c0b, and the handback measures 106 lines against its own DECISION D15 declaration of 106, so its self-measurement is honest. THE FAIL: G11 ordered `python3 -m pytest tests/orchestration/test_exec_guard.py -q` at exit 0 and the handback reports `6 passed in 4.59s`; at the reviewer's hand the same command at the same commit returns `1 failed, 5 passed`, exit 1, on FIVE consecutive runs, failing at `assert result.cpu_seconds_used >= 1.0` with the measured value 0.999776. The test passes when run alone, which is why a single worker run could honestly have seen green: the assertion sits directly on a boundary rather than near one, so this is recorded as a marginal-assertion defect and NOT as a fabricated reading — nothing in the record supports the harsher reading, and the mechanism explains both observations. It is registered as R-0496. The reviewer's own independent probe then found the more serious defect the ordered gates did not reach, registered as R-0495: `run_guarded` under a 1.0-second `wall_timeout_seconds` returned after 300.04 seconds. G17's no-overclaim gate is confirmed at the level it was written — neither new file claims any existing seam is guarded — and R-0495 is a different failure, an internal promise the module does not keep. R5's substance is otherwise sound: the guard's classification of cpu, wall and output trips is correct, its address-space non-attribution is honest, and G16's probe confirmed the reviewer's stated reason rather than contradicting it, with returncode 1, no term_signal, `MemoryError` on stderr and `ru_maxrss` of 26157056 B below the 67108864 B limit. LAST_REVIEWED_SHA does NOT advance and stays 382ed7fa.
<<<END RECORD-R5>>>

<<<SLICE R0495>>>
- R-0495 — High, `run_guarded`'S WALL TIMEOUT DOES NOT BOUND `run_guarded`'S OWN RETURN: A DESCENDANT THAT LEAVES THE PROCESS GROUP HOLDS THE INHERITED PIPES OPEN AND THE GUARD BLOCKS ON ITS STREAM PUMPS UNTIL THAT DESCENDANT EXITS. Raised by the reviewer at the R5 gate, by a probe of its own choosing rather than by any ordered gate. Measured, not reasoned: with `ExecGuardPolicy(wall_timeout_seconds=1.0, output_cap_bytes=4096)` and a child that spawns one grandchild with `start_new_session=True` and then sleeps, `run_guarded` returned after 300.04 seconds — the grandchild's full lifetime — and the returned `ExecGuardResult` carried `tripped_limit="wall_timeout"` with `wall_seconds=300.04`. The mechanism is in `packages/orchestration/exec_guard.py`: the deadline fires on schedule and `_kill_process_group` sends SIGKILL to the child's group, but a grandchild that called `setsid` is no longer IN that group, it still holds the write ends of the stdout and stderr pipes the guard created, so `_StreamPump.read1` never reaches EOF and the `out_pump.join()` and `err_pump.join()` calls in the `finally` block — which have no timeout — block until it exits. This is the feature's central promise failing in the case containment exists for. It is worse than a plain hang because the result LOOKS correct to any caller that reads `tripped_limit` alone, and `wall_seconds` is the only field that betrays it. It is not hypothetical, and the reviewer grepped rather than recalled: `start_new_session=True` appears in production code in `packages/orchestration/dod_runners.py`, `packages/orchestration/stream_evidence.py`, `packages/orchestration/test_execution_service.py`, `packages/runtimes/runtime_supervisor.py`, `packages/runtimes/dev_server.py` and `apps/cli/commands/runtime_cmd.py`. Three of those files hold sites in the very classes stage 1 migrates — dod, test and runtime under amendment F085 D1 — so the escaping descendant is not an exotic case but the ordinary shape of the code this guard is being built to wrap. The module's own `run_guarded` docstring states "the group is killed on every exit path, so no descendant outlives this call", which the same probe falsifies for a descendant that leaves the group, and the feature file's Orchestrator brief requires rejecting overclaiming wording in code comments. Counter-measure, for R7 and stated as a PROPERTY rather than an implementation: after the deadline fires and the group kill is sent, `run_guarded` must return within a bounded grace period regardless of whether any process still holds the pipes, and the result must say plainly whether the streams were complete when it returned; the docstring sentence must narrow to the process group it can actually reach. T002a is BLOCKED until this is fixed — migrating a seam onto this guard would make hangs harder to see than they are today, since an unguarded hang at least does not report a satisfied timeout. OPEN.
<<<END R0495>>>

<<<SLICE R0496>>>
- R-0496 — Medium, THE T001 SUITE IS RED IN FILE ORDER ON A MARGINAL ASSERTION THAT COMPARES KERNEL CPU ACCOUNTING AGAINST AN EXACT INTEGER LIMIT. Raised by the reviewer at the R5 gate while re-running G11. `python3 -m pytest tests/orchestration/test_exec_guard.py -q` at 16506c0b returns `1 failed, 5 passed`, exit 1, on five consecutive runs, failing at `test_cpu_limit_kills_a_busy_loop_and_names_the_limit` on `assert result.cpu_seconds_used >= 1.0` with the measured value 0.999776; the same test run ALONE passes. Everything the test exists to prove holds in the failing run: `term_signal` is SIGXCPU, `classification` is `resource_limit`, `tripped_limit` is `cpu_seconds` and it is a member of `limits_enforced`. Only the accounting assertion fails, and it fails because `ru_utime + ru_stime` is sampled from the kernel's own CPU accounting, which is granular and rounds against the RLIMIT_CPU soft limit rather than exactly to it, so a value a few hundred microseconds under an integer limit is the NORMAL outcome and not an anomaly. The handback reports `6 passed in 4.59s` for this command, and the reviewer's reading contradicts it; the boundary mechanism explains both readings without any dishonesty, and this finding records it as a marginal-assertion defect for that reason — see the RECORD-R5 paragraph, which declines the harsher reading explicitly. Counter-measure for R7: assert the property the test is named for and drop or loosen the accounting assertion — if CPU consumption is asserted at all it is asserted against a tolerance strictly below the limit, never against the limit itself, because a test whose expected value sits ON a boundary is a coin flip that will re-fail later at a much worse moment. This is the reviewer-arithmetic family of R-0327 and R-0336 appearing inside a WORKER-authored test rather than inside a reviewer gate: order the colour, never the exact number. OPEN.
<<<END R0496>>>

<<<SLICE R0497>>>
- R-0497 — Low, A REVIEWER GATE ORDERED AN EXPECTED VALUE THE CODE COULD NOT PRODUCE: G8 OF THE R5 BLOCK REQUIRED A CONTENT GREP TO MATCH A FILE THAT NEVER NAMES ITS OWN PATH. Raised by the reviewer against its own block at the R5 gate. R5's G8 ordered `grep -rn "exec_guard" packages/ apps/ scripts/ tests/` to return "matches in `packages/orchestration/exec_guard.py` and `tests/orchestration/test_exec_guard.py` ONLY", but `grep` matches CONTENT and the new module never writes the string `exec_guard` anywhere inside itself — its docstring says "execution guard" — so the module's own file cannot appear in that output by construction. The real result is two lines, both in the test file. The worker read the difference correctly, reported it, and explicitly did not edit the module to make the gate match, which is the behaviour the block's constraint 7 asks for and the reason this is Low rather than higher: nothing false was recorded and no round passed on it. The cost is one declared deviation spent proving a reviewer mistake. This is the pre-emission checklist item 8 class — a gate whose expected VALUE the code contradicts — recurring in its cheapest form, and the specific lesson is narrower than item 8 as written: a gate over an ABSENCE must name the property it means, which here is "no file other than these two imports or mentions the module", so the honest form orders the SET of matching files and asserts that set contains no third entry, rather than predicting which of the two will appear. The fix is reviewer-side and lands in the next block's gate wording, not in a worker edit; promoting the narrower rule into docs/agents/planner_reviewer_prompt.md §3 is a `docs/agents/**` edit outside this feature's change set and is NOT claimed here, but named for the paydown branch that already carries R-0403, R-0448, R-0482, R-0487, R-0490, R-0493 and R-0494. OPEN.
<<<END R0497>>>
