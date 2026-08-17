── STEP T002a-shape / F085 — R21 ─────────────────────────────────────────────

Goal: rule the SHAPE of `stream_evidence.py`'s spawn — T002a's last site — and
migrate it, by making the guard's CHILD-side half of a policy reusable instead of
making a streaming supervisor call a buffering one.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record
the R20 PASS · C2 the shape DECISION · C3 the exec_guard extraction and its tests
· C4 the stream seam migration and its tests · C5 plan · C6 handback.

## Why this shape (read before C3)

`run_guarded` and `run_streamed_command` differ ONLY in their PARENT half.
`run_guarded` buffers both streams through `_StreamPump` and returns bytes.
`run_streamed_command` iterates stdout LINE BY LINE into `capture_stream_evidence`,
which writes evidence files as the lines arrive and cancels the child at a byte cap
through an `on_cap` callback. That is not a `subprocess.run` swap and it is not a
missing feature of the guard: incremental evidence capture is the thing that seam
exists to do.

Their CHILD half is identical and is what stage 1 is actually about: the rlimits
applied between fork and exec, the cwd the child starts in, and the environment it
inherits. `run_streamed_command` already owns a wall deadline, a process group it
can kill, an output cap and a cwd pin of its own; what it has never had is the
rlimit `preexec_fn` and the scrub. So the extraction reaches exactly the gap and
nothing else, and when T003 adds a network posture to the child half, both seams
receive it from one place rather than two.

## Change

C3 — `packages/orchestration/exec_guard.py`, one public dataclass and one public
function, both built from code that already exists in this file:

- `ChildSpawnPlan`, a frozen dataclass with fields `cwd: str | None`,
  `env: dict[str, str] | None`, `preexec_fn: Callable[[], None]`,
  `limits_enforced: tuple[str, ...]` and `limits_unsupported: tuple[str, ...]`.
  Its one-line WHY sits above it and says that it is the CHILD-side half of a
  policy — what any `Popen` must pass to obey that policy — and that the PARENT
  half (deadline, output cap, reaping) belongs to whichever supervisor spawns.
- `plan_child_spawn(policy: ExecGuardPolicy) -> ChildSpawnPlan`, holding the logic
  that `run_guarded` runs today at its `_plan_rlimits` call, its `_apply_rlimits`
  closure and its `child_env` resolution. `limits_enforced` carries ONLY the
  rlimit-derived names; `wall_timeout` and `output_bytes` are parent-side and stay
  where each supervisor appends them.
- `run_guarded` calls `plan_child_spawn` and passes `plan.cwd`, `plan.env` and
  `plan.preexec_fn` to its existing `Popen`, then appends `wall_timeout` and
  `output_bytes` to the plan's `limits_enforced` exactly as it does now. Its
  observable behaviour does not change; `ExecGuardResult` keeps every field it has.
- The module docstring's deliberate-absence list gains no new claim. If a sentence
  there becomes false because of this change, correct that sentence.

Tests, in `tests/orchestration/test_exec_guard.py`, added not rewritten:
`plan_child_spawn` on a policy with `core_file_bytes=0` names `core_file_bytes` in
`limits_enforced` and names neither `wall_timeout` nor `output_bytes`; on a policy
with `env_allowlist` set it returns an env equal to `scrub_child_env` of the same
inputs; with `env_allowlist=None` it returns `policy.env` UNCHANGED, including
`None`; its `preexec_fn` is callable and lowers RLIMIT_CORE when invoked in a
child (assert through a real guarded run, not by calling it in the test process).

C4 — the stream seam, three files in one commit because it is one migration:

- `packages/orchestration/stream_evidence.py`: `run_streamed_command` gains the
  keyword-only `policy: ExecGuardPolicy | None = None`. When a policy is given the
  function calls `plan_child_spawn` and hands `plan.cwd`, `plan.env` and
  `plan.preexec_fn` to the `Popen` it already has; the policy OWNS cwd and env in
  that case, and the function's own `cwd` argument applies only when `policy` is
  None. Say that precedence in the docstring — it is the one trap in this shape.
  `start_new_session=True`, `text=True` and `bufsize=1` stay as they are.
  `StreamRunResult` gains `limits_enforced: tuple[str, ...] = ()` and
  `limits_unsupported: tuple[str, ...] = ()` at the END of its field list, filled
  from the plan and left empty when no policy was given, so evidence records what
  was enforced instead of asserting it.
- `packages/orchestration/pingpong_provider.py`: `_stream_exec_policy(cwd)` next to
  `_cli_exec_policy`, returning `ExecGuardPolicy(cwd=cwd, core_file_bytes=0)`. Its
  docstring states, in the same honest register `_cli_exec_policy` already uses,
  what it does NOT set and why: `wall_timeout_seconds` is None because
  `run_streamed_command`'s own watchdog is the deadline for this seam and a second
  one would fight it; `output_cap_bytes` is None because that seam caps through
  `max_bytes` and `on_cap`; `env_allowlist` is None because the child is the
  operator's authenticated `claude` CLI, the same reason `_cli_exec_policy` gives.
  The call at the `run_streamed_command` site passes `policy=_stream_exec_policy(
  self._cwd)` and STOPS passing `cwd=`, so cwd has one source.
- Tests in `tests/orchestration/test_stream_evidence_integration.py`: a run given a
  policy still produces the same capture, returncode and events as one given none
  (behaviour equality, the acceptance criterion for every T002 sub-slice); a run
  given a policy reports `core_file_bytes` in `limits_enforced` while a run given
  none reports `()`; a child spawned under a policy really has RLIMIT_CORE 0,
  proved by a fixture program that prints `resource.getrlimit(RLIMIT_CORE)` and by
  reading that value back out of the captured stream. Existing call sites that pass
  no policy keep working unchanged — do not edit them.

C2 — `.agent/decisions.md`, the DECISION1 slice appended after the file's last
line, separated by exactly one blank line. C1 — `.agent/live_review.md`, the
RECORD1 slice appended the same way. C5 — `.agent/plan.md`, the PLANF→PLANT pair.
C6 — `.agent/handoff.md`, rewritten.

## Constraints

1. Save this block byte-for-byte as `.agent/authored/f085-r21.md` in C0a and write
   the COMMITTED C0a blob into `.agent/last_block.md` in C0b — read it back with
   `git show`, never `cp`, never a retype.
2. Every slice below is applied BYTE-VERBATIM between its markers. Marker lines are
   transport only and never reach a target file. Extract each slice
   programmatically from the committed block file; do not retype one.
3. The slices this block carries are RECORD1, DECISION1, PLANF and PLANT. Their
   shapes, each tested by containment rather than by eye: RECORD1 and DECISION1 are
   standalone APPENDS with no FROM, so their proof is the prefix property in G3;
   PLANT does NOT contain PLANF, so that pair is a REWRITE.
4. PLANF spans the WHOLE `## Next Steps` list and not a prefix of it, because PLANT
   changes the list's arity and the surviving entries are renumbered by the pair
   itself.
5. No commit after C6. Nothing is pushed before C6 exists. Create NO pull request
   and merge nothing this round.
6. If a single write of this block's bytes is rejected by the tooling, split it into
   sequential appends — but attempt the single write FIRST and say in the handback
   whether it was attempted and what it returned.
7. Every mutation or red-proof runs ONLY inside a disposable `git worktree`, which
   is removed and pruned before C6, so `git status --porcelain` is empty and
   `git worktree list` is ONE line at the handback.
8. Do not touch container isolation, provider transport timeouts, or fence
   semantics. Do not migrate any site outside `stream_evidence.py`'s spawn. Do not
   change `_StreamPump`: its lock-and-`snapshot()` question is a separate round.

## Gates — run every one, record its real exit code, report what it PRINTED

G1 CLEAN TREE AND STOP. `git status --porcelain` empty at round start and after
every commit. Re-read `.agent/STOP` from disk before C0a and again before C6 and
report both readings; if it exists at either point, finish the commit in hand, write
the handoff and END. `git worktree list` at the handback — report its line count.

G2 TRANSPORT. The committed `.agent/authored/f085-r21.md`, the committed
`.agent/last_block.md` and both working copies are byte-EQUAL. Report the sha256,
the byte count, the line count and the number of marker lines. Then report the
sha256 of each of these three regions of the saved file, which the reviewer measured
before delegating: lines 1 through 60, lines 61 through 140, and line 141 to the
end. A split write that changes nothing shows three matching digests.

G3 APPEND SHAPE, for C1 and again for C2. The pre-commit blob of the target is a
byte-exact PREFIX of the post-commit file; the remainder is exactly one blank line
followed by the slice; the HEAD blob equals the working copy; the slice's first line
occurs exactly ONCE in the whole file at HEAD; the file carries 0 marker lines.
Report the `git show --numstat` pair for each as a READING, never as a prediction.

G4 ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `, `^Done: R-\d+ — `
and `^Landed: R-\d+`. At base 1cfa0acb the reading is 126 / 9 / 0 with 117 open; at
HEAD expect 126 / 9 / 0 and 117 open UNCHANGED, because this round records a verdict
and neither registers nor resolves an id. Report the reading at both ends, both
symmetric differences — which must both be EMPTY — the duplicate-id counts, any
resolution naming an unregistered id, and the max and next-free id.

G5 PLAN PAIR. PLANF occurs 0 times at HEAD and PLANT exactly once. `## Goal` and
`## Risks` are byte-IDENTICAL to their base bytes. Report `.agent/plan.md`'s sha256,
its byte count and a line count under 50, and report the numbers the `## Next Steps`
list parses to rather than a count of them.

G6 THE ROUND'S REAL GATE. Each suite below exits 0. The reviewer ran each of them at
base 1cfa0acb and states the base readings so a regression is separable from a
pre-existing colour:
  a. `python3 -m pytest tests/orchestration/test_exec_guard.py -q` — this is the
     C3 refactor's behaviour-equality proof; base reading `12 passed`.
  b. `python3 -m pytest tests/orchestration/test_exec_guard.py
     tests/orchestration/test_stream_evidence.py
     tests/orchestration/test_stream_evidence_integration.py -q` — base reading
     `112 passed`, and it must RISE by the tests C3 and C4 add.
  c. `python3 -m pytest tests/orchestration/test_managed_builder_execution.py
     tests/orchestration/test_pingpong.py tests/orchestration/test_pingpong_cli.py
     -q` — base reading `337 passed`. The other two T002a seams share the code C3
     moves, so this suite is the proof that the extraction did not disturb them.
Report each count as a READING. If a run comes out red, report the failing node ids
and re-run that suite alone three times, reporting all four readings. A failure that
reproduces every time is a STOP.

G7 RED PROOF AS A PROBE, in a disposable worktree at HEAD, never in the primary
checkout. Make `plan_child_spawn` return a `ChildSpawnPlan` whose `preexec_fn` is a
function that does nothing, and report WHICH tests fail and how many. The colour is
not ordered and no count is predicted: the reviewer has not measured this branch's
own new tests, and ordering a colour it cannot compute is what item 5 of the
pre-emission checklist forbids. A probe that reports zero failures is a real answer
and means the new rlimit assertions do not reach the code they name — report it as
such and do not repair it inside this round.

G8 LINT. `python3 -m ruff check packages/orchestration/exec_guard.py
packages/orchestration/stream_evidence.py packages/orchestration/pingpong_provider.py
tests/orchestration/test_exec_guard.py
tests/orchestration/test_stream_evidence_integration.py` exits 0. The reviewer ran
this exact command line at base 1cfa0acb and it printed `All checks passed!`, so any
error this round reports was introduced by this round.

G9 STATE READERS, because this round rewrites `.agent/` state: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py
-q` exits 0. Base reading `157 passed`. Report the count as a READING: that suite
spawns wrapper processes under flock and is timing-sensitive. CANARY: `python3 -m
pytest tests/cli/test_golden_path.py -q` exits 0, base reading `42 passed`. No
doc-reader gate is ordered and none is skipped by oversight: this change set holds
no file under `docs/`.

G10 COMMIT HYGIENE. `git diff --name-only 1cfa0acb..HEAD` measured
BEFORE C6 equals the declared paths minus `.agent/handoff.md` — report the list, and
0 paths outside it. The `+` column of `git show --numstat` for C0a, C0b, C1, C2, C3,
C4 and C5: none exceeds 500. C6's own count is ordered nowhere, because a commit
cannot measure itself; report it in the round report instead. `git log --format=%h
%p 1cfa0acb..HEAD` shows ONE parent per commit and a linear chain; `git reflog` shows
every entry prefixed `commit:`, with no amend, rebase, reset or force-push.

## Done when

Every commit in the bundle exists in order, the branch is pushed once after C6,
every gate has been RUN with its exit code recorded, `git status --porcelain` is
empty, `git worktree list` is one line, and `.agent/handoff.md` is rewritten per
docs/agents/handback_template.md with an item-status table covering C0a through C6.
That handoff carries: feature and round, branch, the commit SHAs, the changed-files
table, the real verification readings, the open-findings count, and a NEXT section
naming the next session's first action in the protocol's own order — Phase 1 rule 1,
re-read `.agent/STOP` from disk, BEFORE rule 2, the Open PR Gate. Run `gh pr list
--state open --json number,headRefName,baseRefName,isDraft` after the push and report
its output. Report what the commands PRINTED — a gate whose result you did not read
is a finding. If a gate contradicts this block, report the contradiction and STOP.
Declare every deviation.

BEGIN-RECORD1
Gate: R20 — PASS, the record round that closed the previous session. All seven ordered
gates were re-run by the reviewer over 6b6cfee5..1cfa0acb and every one reproduces the
handback's reading. R20's verdict is recorded HERE rather than left in the handoff: the
§4.13 terminator covers the last round of a BRANCH, and this branch continues, so the
round is an ordinary reviewed round whose gate entry the next round writes. TRANSPORT:
the committed `.agent/authored/f085-r20.md`, the committed `.agent/last_block.md` and
both working copies are byte-EQUAL at sha256
3026ed0d86d1d40c2e5d5a57076f39d7df37b96dbaa6041d0765be5fe543fbc8, 12660 B, 174 lines.
The worker split the C0a write into six calls without first attempting one, which
constraint 6 conditioned on a rejection; it declared the deviation, and the byte
equality proves the split cost nothing. Declaring a deviation a gate can disprove is
how this loop is supposed to work. THE APPEND COMMIT HOLDS ITS SHAPE: for C1 the
pre-commit blob (303775 B) is a byte-exact PREFIX of the post-commit file (307026 B)
and the remainder is exactly one blank line plus RECORD1; `Gate: R19` occurs once in
the whole file, no marker line survives, and the HEAD blob equals the C1 blob. THE
ARITHMETIC STAYED WHERE IT WAS ORDERED TO: 126 / 9 / 0 and 117 open at base and the
same at HEAD, both symmetric differences empty, no duplicate id and no resolution
naming an unregistered id; max R-0511, next free R-0512. THE PLAN PAIR touched what it
was scoped to: `.agent/plan.md` is at sha256
4f6c8d32716a73b6deb30c4076511acc62b1e5dae2adb1fab93c993b1e5364b6, 2473 B, 41 lines
under its cap. State readers are 157 passed and the canary 42 passed, both re-run by
the reviewer rather than accepted from the report, and both from the block's exact
command lines. The change set is exactly the five declared paths with 0 outside;
insertions are 174, 111, 35 and 5 before the handback commit, which is itself 31, none
over 500; five single-parent commits in a linear chain, every reflog entry
`commit:`-prefixed, no amend, rebase, reset or force-push; the tree is clean and
`git worktree list` is ONE line. The handback measures 66 lines against its own
declared 66, with the mandated content named as the cause. LAST_REVIEWED_SHA advances
to 1cfa0acb.
END-RECORD1

BEGIN-DECISION1
## DECISION F085 D2 — the streaming seam takes the guard's CHILD half, not `run_guarded` (2026-08-17)

CONTEXT: `stream_evidence.run_streamed_command` is T002a's last unmigrated spawn.
The other two sites became `run_guarded` calls, and this one cannot: it iterates
stdout line by line into `capture_stream_evidence`, which writes evidence files as
the lines arrive and stops the child at a byte cap through an `on_cap` callback,
while `run_guarded` buffers both streams through `_StreamPump` and returns bytes at
the end. Incremental capture is what that seam exists to do, so the difference is
the feature and not a gap.

CHOSEN: split `ExecGuardPolicy`'s effect in two and share only the half that is
actually common. `exec_guard.plan_child_spawn(policy)` returns a `ChildSpawnPlan` —
the cwd, the resolved environment, the fork-to-exec `preexec_fn` and the names of
the rlimits enforced and unsupported — and BOTH supervisors pass it to their own
`Popen`. The PARENT half stays with whoever spawns: `run_guarded` keeps its
`wait4` supervision, its deadline and its pumps, and `run_streamed_command` keeps
the watchdog, process group, byte cap and stderr tail it already had. One
implementation of what a policy does TO A CHILD; two supervisors, because there
really are two.

ALTERNATIVES CONSIDERED AND REJECTED: teaching `run_guarded` a streaming mode,
rejected because it rewrites the supervision of a module T001 had just proven and
buys nothing the streaming seam does not already have; duplicating the rlimit and
scrub logic inside `stream_evidence.py`, rejected because T003 adds a network
posture to exactly that child half and a second copy is a second thing to forget;
leaving the seam unguarded and naming it in T003's limitations document, rejected
because T2_F085's Edge-cases section makes the per-class rlimit VALUES config with
per-project overrides, and a class whose only streaming site cannot receive a
configured value leaves the policy table with a hole no document closes honestly.

CONSEQUENCE: what this seam gains in stage 1 is narrow and worth stating plainly —
the rlimit `preexec_fn` and a place for the values T003 configures. It already had
a wall deadline, an output cap, a cwd pin and a killable process group. Its policy
sets no environment allowlist, for the same reason `_cli_exec_policy` sets none:
the child is the operator's authenticated `claude` CLI and reads its credentials
from the inherited environment. That is a stage-1 gap and it is owed to T003's
limitations document, not to this decision.

Reverse this decision by inlining `plan_child_spawn` back into `run_guarded` and
dropping `run_streamed_command`'s `policy` keyword; the seam returns to spawning a
child under no limits at all.
END-DECISION1

BEGIN-PLANF
## Current Step
R20, this round: record the R19 PASS and close the session on a written handoff. A
record round only — the session reached its declared round cap at R19, and opening
`stream_evidence.py`'s shape question at a session boundary is what guardrail G8 of
the self-drive protocol forbids. R20's own verdict is the §4.13 terminator: it lives
in the handoff, not on disk, and the next session must not open a repair round for it.

## Next Steps
1. `stream_evidence.py`:595 is T002a's last site and is NOT a `subprocess.run` swap:
   it streams incrementally where `run_guarded` buffers, so its shape is decided first.
2. `_StreamPump` gains a lock and a `snapshot()` so PARTIAL output survives a
   bounded drain. It still returns `b""` for a stream whose pump never reached
   EOF, which `streams_complete` reports honestly but which loses bytes.
3. T002b-d, then T003 — network posture, limitations document, README link.
END-PLANF

BEGIN-PLANT
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
END-PLANT
