── STEP T002b/1 — F085 — R24 ─────────────────────────────────────────────────

Goal: record the R23 PASS, then open T002b by giving `exec_guard` the shared
test-class seam and migrating `test_runner.run_tests_local` — the most
load-bearing of the twelve `test`-class sites — onto it with no observable
outcome changed.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1
record R23 · C2 the shared test-class seam in `exec_guard` · C3 migrate
`run_tests_local` and retarget its mocked call sites · C4 plan · C5 handback.

This round registers NO new finding. The reviewer re-ran all nine of R23's gates
and every reading reproduced, so C1 carries a gate entry and nothing else. The
open set is unchanged at 117 and the next free id stays R-0516.

## Why this shape — read before C2

Eleven of the twelve `test`-class sites are `subprocess.run` with `cwd=` and
`timeout=`. The twelfth, the `Popen` in
`test_execution_service._run_isolated_process`, is a supervisor: it takes the
CHILD half through `plan_child_spawn` in a later round, exactly as
`stream_evidence.run_streamed_command` already does, and is NOT part of this
round.
Ten modules cannot each grow a private policy without the synonym drift
AGENTS.md's discoverability conventions forbid, so the policy and the runner
live ONCE in `exec_guard` and every test-class caller imports them.

`_builder_exec_policy` (`managed_builder_execution.py`, the symbol itself —
re-grep it, this branch has moved that file) already settled which rlimits a
stage-1 policy may set: `cpu_seconds`, `address_space_bytes` and `open_files`
stay None, because a value picked without measuring real workloads kills
legitimate runs — a parallel pytest burns CPU-seconds far faster than
wall-clock — and RLIMIT_AS cannot be classified from what `wait4` reports. The
test policy follows that precedent rather than inventing a second answer.

The environment allowlist is the one part that can break a well-behaved command,
because `run_tests_local` today passes no `env` at all and its child inherits
everything. That is why C3 ends with a REAL pytest run and not another mock.

What that golden does and does not prove, stated so no later reader overreads
it: it proves a well-behaved test command still runs end to end through the new
seam. It does NOT prove the allowlist is minimal or that a narrower one would be
caught — the reviewer measured that this fixture still passes with an EMPTY
environment, because `execvpe` falls back to `os.defpath` when PATH is absent.
Do not order or claim an allowlist-sensitivity result from it.

## Change

C2 — `packages/orchestration/exec_guard.py` and
`tests/orchestration/test_exec_guard.py`, one commit:

- `TEST_COMMAND_ENV_ALLOWLIST: tuple[str, ...]`, sorted, carrying the one-line
  WHY comment directly above it: CI, HOME, LANG, LC_ALL, LC_CTYPE, LOGNAME,
  PATH, PWD, PYTHONDONTWRITEBYTECODE, PYTHONHASHSEED, PYTHONPATH,
  PYTHONUNBUFFERED, REMEDY_UI_NO_AUTO_BUILD, SHELL, TEMP, TERM, TMP, TMPDIR, TZ,
  USER, VIRTUAL_ENV. `REMEDY_UI_NO_AUTO_BUILD` is there for carried finding
  R-0202 and gets an assertion of its own: the mid-run UI rebuild class exists
  because that variable stopped reaching a child, so an allowlist that dropped it
  would re-create the bug this feature is asked to close. Say that in one line
  where the constant is defined.
- `test_command_exec_policy(timeout_sec, cwd, *, output_cap_bytes=<default>,
  extra_env_keys=())` returning `ExecGuardPolicy` with
  `wall_timeout_seconds=float(timeout_sec)`, `cwd=cwd`, `core_file_bytes=0`, the
  given `output_cap_bytes`, `env=None`, and
  `env_allowlist=TEST_COMMAND_ENV_ALLOWLIST + tuple(extra_env_keys)`. `env=None`
  is deliberate: it makes `plan_child_spawn` build the child environment from
  `os.environ`. The docstring names which rlimits are deliberately None and cites
  `_builder_exec_policy` for the reasoning instead of restating it, and names
  `extra_env_keys` as the per-project override knob T2_F085's edge-case section
  promises.
- The default `output_cap_bytes` is 16 MiB. It MUST stay strictly above
  `test_runner.MAX_TEST_OUTPUT_BYTES` (1 MiB) or the guard would truncate before
  the caller's own truncation and `output_truncated` would stop describing what
  the caller measured. Put that reason in the code beside the value. Do not
  import `test_runner` from `exec_guard` to express it — the dependency runs the
  other way; state the relationship in words.
- `run_guarded_test_command(cmd, *, timeout_sec, cwd, extra_env_keys=())`
  returning `subprocess.CompletedProcess[bytes]`. It calls `run_guarded` with the
  policy above. On `tripped_limit == "wall_timeout"` it raises
  `subprocess.TimeoutExpired(cmd, timeout_sec, output=<guarded stdout>,
  stderr=<guarded stderr>)` — WITH the partial streams, because callers of the
  sites this seam replaces read `exc.stdout` and `exc.stderr`, and dropping them
  would throw away output the guard is already holding. A signal death is
  republished as a negative returncode in the -SIGNUM form, the same translation
  `_guarded_exit_code` already performs in `managed_builder_execution`.
  `FileNotFoundError` is deliberately NOT caught: `Popen` raises it inside
  `run_guarded` before any supervision starts, and callers already handle it.
  Write that as the deliberate-absence line the conventions ask for.
- The module docstring's PARTIAL COVERAGE bullet currently lists "the test, DoD,
  runtime, git and packaging classes" as still spawning unsupervised. That
  sentence stops being true with C3. Rewrite it to say what is true after this
  round — the test class is PARTIALLY migrated — and keep its existing refusal to
  write a count, which is there on purpose.
- Tests appended to `tests/orchestration/test_exec_guard.py`, added and not
  rewritten:
  (a) `REMEDY_UI_NO_AUTO_BUILD` is a member of `TEST_COMMAND_ENV_ALLOWLIST`;
  (b) a policy from `test_command_exec_policy` has `cpu_seconds`,
      `address_space_bytes` and `open_files` all None, `core_file_bytes` 0, and
      an `output_cap_bytes` strictly greater than
      `test_runner.MAX_TEST_OUTPUT_BYTES` — import that constant in the TEST, so
      the two move together and the guard keeps its dependency direction;
  (c) a child that DUMPS its own environment, spawned through
      `run_guarded_test_command` itself rather than through `scrub_child_env`
      alone, with a parent environment carrying `ANTHROPIC_API_KEY`, a
      non-allowlisted `MY_PROJECT_SECRET`, `REMEDY_UI_NO_AUTO_BUILD=1` and the
      real `PATH`: the dump contains `REMEDY_UI_NO_AUTO_BUILD` and `PATH` and
      contains NEITHER secret;
  (d) `extra_env_keys` reaches the child: a variable outside the base allowlist
      appears in the dump when named there and is absent when it is not;
  (e) a child that prints and FLUSHES a known line and then sleeps past a short
      `timeout_sec` raises `subprocess.TimeoutExpired` whose `output` carries
      that line — the partial-stream promise, proven rather than asserted;
  (f) a child that exits 3 comes back as a `CompletedProcess` with
      `returncode == 3` and its stdout bytes intact.

C3 — `packages/orchestration/test_runner.py`, `tests/test_test_runner.py` and
`tests/orchestration/test_test_runner.py`, one commit:

- In `run_tests_local`, the `subprocess.run(argv, cwd=..., capture_output=True,
  timeout=timeout_sec)` call becomes
  `run_guarded_test_command(argv, timeout_sec=timeout_sec, cwd=str(repo_root))`,
  with the import at module top level the way `managed_builder_execution`
  imports the guard. Everything around it stays: the
  `except subprocess.TimeoutExpired` branch, the `except FileNotFoundError`
  branch, `proc.stdout + proc.stderr`, the truncation block, the status mapping.
  `subprocess` stays imported — the module still names `subprocess.TimeoutExpired`.
- The one-line WHY comment above the call says what changed and what did not: the
  spawn is guarded since F085 T002b; the observable outcome is unchanged.
- Every `patch("subprocess.run", ...)` in those two test files — grep both for it
  and handle each hit, do not work from a line-number list — is retargeted to
  `patch("packages.orchestration.test_runner.run_guarded_test_command", ...)`.
  The mocked return values are already `CompletedProcess` objects with BYTES
  streams and stay exactly as they are; the `TimeoutExpired` side effect stays
  too, because the new seam raises that same exception.
- One of those tests asserts, off `mock_run.call_args.kwargs`, that no `shell`
  keyword was passed. Against a seam that HAS no `shell` parameter that assertion
  can never fail. Replace it — do not merely retarget it — with assertions that
  the mock was called exactly once, that its positional argv is the discovered
  candidate's argv list, and that its keyword arguments carry `timeout_sec` and a
  `cwd` equal to the repo root. Keep the test's name and its other assertions.
- One behaviour-equality golden appended to
  `tests/orchestration/test_test_runner.py`, marked `@pytest.mark.subprocess`:
  build a tmp repo with a `pyproject.toml`, a `tests/` directory and one
  trivially passing test file, call `run_tests_local` with NO mock, and assert
  `status == "passed"`, `exit_code == 0`, `blocked_reason == ""` and that the
  written output file's bytes contain `b"1 passed"`. The reviewer ran this
  end to end at base and got exactly that, with `command == "python3 -m pytest"`.
  It may not be replaced by a mock: it is the only check in the round that runs a
  real command through the new seam.

## Constraints

1. SPLIT round. C2 and C3 touch `packages/`, so nothing here may be
   self-certified; the reviewer gates it.
2. AGENTS.md in full: the self-review loop before EVERY commit, one logical step
   per commit, `.agent/plan.md` current before committing, a clean tree, the push,
   the handoff rewrite. Commit subjects carry no leading-slash token and no path.
3. Do-not-touch, from T2_F085: container isolation, provider transport timeouts,
   fence semantics. Also out of scope this round: the other eleven `test`-class
   sites, every `dod`, `runtime`, `git` and `packaging` site, and T003's network
   posture and limitations document.
4. C1 lands BEFORE C2 and C3. The verdict record persists first, so a session that
   dies mid-round still leaves R23's gate entry on disk.
5. The authored slices — RECORD1, PLANF and PLANT — are extracted
   programmatically from the COMMITTED `.agent/authored/f085-r24.md` by their
   one-line markers and applied byte-verbatim. Never retype them, never source
   them from `.remedy-wt/`, and let no marker line reach a target file.
6. Pair shapes, classified mechanically before this block was emitted, one
   reading per pair: the plan pair's TO contains its FROM — False, so it is a
   REWRITE and "PLANF 0x at HEAD" is a legitimate gate. RECORD1 is not a pair at
   all: it is an APPEND of a new paragraph at the end of the file, so its proof is
   the prefix proof in G3 and no `0x` reading is ordered for it.
7. Destructive verification — the G10 probe and anything else that mutates a
   file to observe a colour — runs ONLY inside a disposable `git worktree` under
   `.remedy-wt/`, which is gitignored. Remove and prune it before the handback.
   The primary checkout satisfies `git status --porcelain` == empty at every
   commit and at the handback.
8. The 500-line cap counts INSERTIONS — the first column of
   `git show --numstat` — never the churn total `git show --stat` prints. If C2 or
   C3 approaches it, split that commit along the file boundary already present in
   its change set and say so in the handback.
9. If any gate below comes out red, or if this block contradicts itself or the
   code, finish the commit in hand, record the contradiction in the handback and
   END the round. Do not guess and do not widen scope to route around it.

## Done when

G1 STOP AND TREE. Re-read `.agent/STOP` from disk before C0a and again before
C5 and report both readings; if it exists at either point, finish the commit in
hand, write the handoff and END. `git status --porcelain` is empty at round start
and after every commit. Report `git worktree list`'s line count at the handback.

G2 TRANSPORT. The committed `.agent/authored/f085-r24.md`, the committed
`.agent/last_block.md` and both working copies are byte-EQUAL. Report the sha256,
the byte count, the line count and the number of marker lines. Then report the
sha256 of each of these regions of the saved file, measured by the reviewer
before delegating: lines 1 through 60, lines 61 through 140, and line 141 to the
end. Three matching digests show a split write changed nothing.

G3 APPEND SHAPE for C1. The pre-commit blob of `.agent/live_review.md` is a
byte-exact PREFIX of the post-commit file; the remainder is exactly one blank
line followed by RECORD1; the HEAD blob equals the working copy; RECORD1's first
line occurs exactly ONCE in the whole file; the file carries 0 marker lines.
Report the `git show --numstat` pair as a READING, insertions being the FIRST
column.

G4 ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `,
`^Done: R-\d+ — ` and `^Landed: R-\d+`. At base f28ed65a the reading is
130 / 13 / 0 with 117 open. At HEAD it is unchanged at 130 / 13 / 0 with 117
open, because this round registers and resolves nothing. Report both readings,
the registered and resolved symmetric differences — both empty — the duplicate-id
counts, any resolution naming an unregistered id, and the max and next-free id.

G5 PLAN PAIR. PLANF occurs 0 times at HEAD and PLANT exactly once. `## Goal` and
`## Risks` are byte-IDENTICAL to their base bytes. Report `.agent/plan.md`'s
sha256, its byte count, a line count under 50, and the numbers its `## Next
Steps` list parses to rather than a count of them.

G6 LINT, run after C3: `python3 -m ruff check
packages/orchestration/exec_guard.py packages/orchestration/test_runner.py
tests/orchestration/test_exec_guard.py tests/test_test_runner.py
tests/orchestration/test_test_runner.py` exits 0. The reviewer ran this exact
command line at base f28ed65a and it printed `All checks passed!`, and proved it
non-blind by breaking imports in a disposable worktree, where it exited 1 on I001
and F401. Report the exit code and the line printed.

G7 THE MIGRATED SUITES, run after C3: `python3 -m pytest
tests/orchestration/test_exec_guard.py tests/test_test_runner.py
tests/orchestration/test_test_runner.py -q` exits 0. The reviewer's base reading
is `112 passed`. Report the HEAD count as a READING and do not predict it — this
round ADDS tests, so the number must rise, and by how much is not something this
block may assert. Report that 0 tests fail and 0 error.

G8 STATE READERS, because this round rewrites `.agent/` state: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py
-q` exits 0; base reading `157 passed`, and that suite spawns wrapper processes
under flock and is timing-sensitive, so report the count as a READING. CANARY:
`python3 -m pytest tests/cli/test_golden_path.py -q` exits 0, base reading
`42 passed`. No docs gate is ordered and none is skipped by oversight: this change
set holds no file under `docs/` or `docs/roadmap/`.

G9 COMMIT HYGIENE. `git diff --name-only f28ed65a..HEAD` measured BEFORE C5
equals the declared paths minus `.agent/handoff.md` — report the list and 0 paths
outside it. For C0a, C0b, C1, C2, C3 and C4 report the FIRST COLUMN of
`git show --numstat`; none exceeds 500. C5's own count is ordered nowhere, since a
commit cannot measure itself; report it in the round report instead. Report
`git log --format=%h %p f28ed65a..HEAD` and confirm one parent each, and report
`git reflog -10` showing no amend, rebase, reset or force-push.

G10 THE GOLDEN REACHES THE NEW SEAM — a PROBE, not an ordered colour. In a
disposable worktree at HEAD, make `run_guarded_test_command` raise immediately on
entry, run the C3 golden node alone, and REPORT what happens. The reviewer's
expectation is that it stops passing, because a golden that survives that
mutation is not exercising the migrated path at all — but report the reading you
get, whatever it is, and do not adjust the test to meet an expectation. Remove
and prune the worktree afterwards.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, branch, a per-commit changed-files table, the item-status table covering
C0a, C0b, C1, C2, C3, C4 and C5 exactly once each, the real gate readings above,
the open-findings count, and the next expected action. Repeat this Fortschritt
line verbatim, estimate label included:

Fortschritt: ~78 % (T001 gebaut · R13-R23 PASS · T002a KOMPLETT · T002b begonnen:
Seam + erster von zwölf `test`-Sites · T002b Rest, T002c-d, T003 offen) — Schätzung.

Then push the branch. Do not create a PR and do not merge anything.

BEGIN-RECORD1
Gate: R23 — PASS, a paydown round that fixed two defects of the reviewer's own
block and touched no production code. All nine ordered gates were re-run by the
reviewer over b4da5101..f28ed65a and every one reproduces the handback's reading.
TRANSPORT IS EXACT: the committed `.agent/authored/f085-r23.md`, the committed
`.agent/last_block.md` and both working copies are byte-EQUAL at sha256
6506c9cc76ba9c63d95c5f0a41fcee4d48dca39b4e26231e6f4bd66400ebb9d4, 24320 B, 368
lines, 0 trailing-whitespace lines, and the three region digests reported —
6d1b2d39, cac13512 and 8c2421ae over lines 1-60, 61-140 and 141-end — reproduce
under the newline-included convention the handback declared, so the single write
really was single. THE APPEND COMMITS HOLD THEIR SHAPE: for C1 the pre-commit
blob is a byte-exact PREFIX of the post-commit file and the remainder is exactly
one blank line plus RECORD1; for C3 the same property holds for DONE1. Each
slice occurs exactly once in the file, no marker line survives anywhere, and the
HEAD blob equals the working copy in both cases. ALL SIX SLICE DIGESTS MATCH the
handback: RECORD1 e2bb4c28, CHECKF e411b1ad, CHECKT e4799d98, DONE1 a9fccd54,
PLANF 4e11656a, PLANT b90d1cf7, each extracted here from the committed authored
file by its own marker pair and compared against the target on disk, so the
worker's applied bytes are the reviewer's authored bytes and not a retype. THE
ARITHMETIC MOVED WHERE IT WAS ORDERED TO: 128 / 11 / 0 with 117 open at base,
130 / 11 / 0 with 119 open after C1 — both registrations landed BEFORE the fix,
which is the ordering constraint 5 existed to enforce — and 130 / 13 / 0 with 117
open at HEAD. Registered and resolved symmetric differences are each exactly
R-0514 and R-0515; no duplicate id, no resolution naming an unregistered id; max
R-0515 and next free R-0516. THE COUNTER-MEASURES ARE REALLY ON DISK AS RULES:
`docs/agents/planner_reviewer_prompt.md` at HEAD hashes to 738920de and its
pre-emission checklist parses to the numbers 1 through 19 with no gap and no
repeat, so items 18 and 19 are numbered members of the list rather than prose
appended near it. The pair was append-shaped and was proved as one — CHECKT
contains CHECKF verbatim, so the unsatisfiable "CHECKF 0x" reading was correctly
never ordered. THE PLAN PAIR WAS A REWRITE and behaved like one: PLANF 0x and
PLANT 1x at HEAD, `## Goal` and `## Risks` byte-identical to their base bytes,
42 lines, under the cap. THE GATES WERE RE-RUN, NOT READ: the reviewer executed
`python3 -m pytest tests/docs/ -q` (295 passed), the four state readers (157
passed) and the canary `tests/cli/test_golden_path.py -q` (42 passed), each as
its exact ordered command line, and each reproduced the handback's number. One
correction to the record, which changes no verdict: the reviewer's first attempt
at the state-reader gate used two wrong paths, pytest reported "no tests ran"
rather than an error, and the reading was worthless until the block's own command
line was used instead — the R-0438 vacuous-gate shape, caught here by comparing
against the ordered command rather than by any gate. COMMIT HYGIENE IS CLEAN: the
changed-path set before C5 is exactly the declared one, per-commit insertions are
368, 280, 97, 23, 19, 5 and 42 with none over 500, the seven commits form a
single-parent chain, the reflog holds nothing but `commit:` entries, and the
primary checkout is porcelain-empty with one worktree. No block condition is met
and no finding is registered against this round.
END-RECORD1

BEGIN-PLANF
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
END-PLANF

BEGIN-PLANT
## Current Step
R24, this round: record the R23 PASS and open T002b. `exec_guard` gains the shared
test-class seam — an explicit environment allowlist, a policy factory and a
`subprocess.run`-shaped runner — and `test_runner.run_tests_local`, the most
load-bearing of the twelve `test`-class sites, becomes its first caller. Its mocked
call sites move onto the new seam and one real pytest run proves a well-behaved
command still works through it.

## Next Steps
1. T002b continued — the remaining `test`-class sites, including
   `test_execution_service.py`'s `Popen`, which takes the child half via
   `plan_child_spawn` rather than the runner, and which carries R-0202.
2. T002c-d — the two DoD sites and the five runtime sites, whose policy differs:
   no wall timeout, because their children are the long-lived harness.
3. T003 — network posture, the honest limitations document, the README link. Then
   the integration gate, then closure.
END-PLANT
