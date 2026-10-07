# F287 Provider session continuity across relaunch — Repeated acceptance audit 1 (amend0930b-slow-cap hardening stage)

## What was read, and what was not

Read: `docs/roadmap/features/T3_F287.md` (in full, again, for the exact wording
of the Goal & Done and Acceptance statements); `.agent/f287_acceptance_audit.md`
(the first audit, in full, to learn the nine claims, their mutations, and the
exact wording of the standing GAP — "no proof reached the feature the way a
user does"); the `amend0930b-slow-cap` paragraph of
`docs/agents/self_drive_protocol.md` (rules (1)-(6), defining this repeat as a
re-audit of only the statements that had gaps, at most three repair rounds, and
the record it expects in the feature's Built State); `AGENTS.md` only via the
first audit's own citation (not re-read start-to-finish, since this round's
task is narrowly scoped and the first audit already recorded the operating
rules). The new test file in full,
`tests/cli/test_job_run_session_resume.py`; its direct dependencies read to
confirm the claim that it drives the real CLI —
`tests/cli/in_process_cli.py` (`run_cli_in_process`, which calls
`apps.cli.grouped.main` in-process, never `run_job` directly and never a
literal subprocess); `apps/cli/grouped.py` (dispatch-table construction);
`apps/cli/commands/do_cmd.py` in full around `_cmd_job_run` (lines 661-830),
`_cmd_run_show` (509-526), and the `COMMAND_HANDLERS` wiring for `job.run` and
`run.show` (979-1040); `apps/cli/commands/run_invocation.py` in full; the
relevant regions of `packages/orchestration/pingpong_job.py` (`run_job`'s
config-resolution block around lines 2707-2820, including the `repair_rounds`
precedence gate) and `packages/orchestration/pingpong_loop.py` (`run_pingpong`'s
round-1 resume gate, the fallback-once gate, `resume_declined_reasons`,
`_session_fields`, `repair_rounds_allowed` gating around lines 340-401); the
relevant classes in `packages/orchestration/pingpong_provider.py`
(`ClaudeCliProvider._build_impl`, `FakeProvider.build`/`review`/`_review_impl`,
to understand `pass_on_round`/`fail_on_round`); `tests/orchestration/
test_relaunch_session_resume.py`'s `_make_stand_in` and `_init_git_repo`
helpers, which the new CLI test imports and reuses; `tests/orchestration/
test_job_stop_integration.py` only for `_ONE_TASK_JOB`. Not read, as
instructed: `.agent/handoff.md`, `.agent/live_review.md`,
`.agent/live_review_archive.md`, `.agent/plan.md`, `.agent/decisions.md`,
`.agent/prose_slips.md`, anything under `.agent/authored/`, and any
`.remedy-wt/f287-r*` folder.

## How the mutations ran

One disposable worktree, `git worktree add --detach
/home/decodeux/Repos/remedy/.remedy-wt/f287-reaudit-wt 7afbf9d02`, at the
feature branch's current tip. All mutations were driven by one Python script,
`.remedy-wt/f287-reaudit/mutate_run.py` (gitignored scratch, not under
`/tmp`), which: runs each of the two distinct node ids once, unmutated, as its
own control; then, one at a time, reads the target file inside the worktree,
asserts the old snippet occurs exactly once, writes the mutated file, runs
`python3 -B -m pytest -q -p no:cacheprovider <node id>` as a subprocess with
`cwd` set to the worktree, captures the exit code and last stdout line, and
restores the file byte-for-byte in a `finally` block before the next mutation
— never two pytest processes at once, never a full module, never `-n`, never
`REMEDY_TEST_MAX_WORKERS`. No real `claude` process or network call starts in
either test: `pingpong_provider._guarded_cli_run` is replaced throughout with
the same kind of recorded stand-in `test_relaunch_session_resume.py` already
uses, and the second test's relaunch uses `FakeProvider` by name. One mutation
attempted early (forcing `apps/cli/commands/do_cmd.py`'s `repair_rounds`
CLI-override gate permanently false, to reproduce the round-8 regression the
new test's docstring describes) stayed green under mutation against the
second test — it did not reproduce the regression through this lever — so it
was discarded and replaced with a different, verified command-line-layer
mutation before being counted as a proof; it is not included in the eight
mutations below. After the eight counted mutations, `git -C
.../f287-reaudit-wt status --porcelain` was empty and `git -C
/home/decodeux/Repos/remedy status --porcelain` was empty throughout and at
the end; the worktree was then removed with `git worktree remove --force`.

**Gaps re-audited: 1. Closed: 1. Still open: 0.**

## The user-path proof

Two new tests reach F287 through the command line:
`tests/cli/test_job_run_session_resume.py::TestARelaunchThroughJobRunResumesTheParkedSession::test_the_relaunch_on_claude_cli_resumes_the_parked_session`
and `...::test_the_relaunch_on_a_provider_that_cannot_resume_names_the_decline`.
Both call `run_cli_in_process`, which runs `apps.cli.grouped.main` — the same
entry point `python -m apps.cli.grouped` / the installed `remedy` command
dispatches to — in the test process, never `run_job` or `resume_declined_reasons`
directly. The pause that parks the task is itself triggered by a nested
`run_cli_in_process(["job", "pause", ...])` call fired from inside the
recorded `claude-cli` stand-in's first builder call — the same "job pause"
command an operator would type — and the relaunch is a second `["job", "run",
...]` call. The evidence is read back with a third CLI call, `["run", "show",
relaunch_run_id, "--json"]`.

### Test 1 — `test_the_relaunch_on_claude_cli_resumes_the_parked_session`

Control (unmutated): `exit=0 last_line='1 passed in 3.47s'`.

**Mutation 1 (command-line layer, proves the user-path statement itself) —**
`apps/cli/commands/do_cmd.py`, function `_cmd_run_show`:
```
before:
    if json_output:
        emit_ok(**data)
after:
    if json_output:
        data.pop("resumed_from_run_id", None)
        emit_ok(**data)
```
Red: `exit=1 last_line='1 failed in 3.34s'`. Green (control above).
This is the mutation that matters most for the gap: it shows that `remedy run
show --json` — the command an operator actually types to read a run's
evidence — is what the test's final assertion
(`record["resumed_from_run_id"] == parked_run_id`) depends on, not only the
persisted-file layer underneath it.

**Mutation 2 (Goal & Done claim 1 — a relaunch of a pause-interrupted task on
`claude-cli` resumes the parked session) —**
`packages/orchestration/pingpong_loop.py`, function `run_pingpong` (round-1
resume-offer gate):
```
before:
            if (round_num == 1 and resume_sessions.get("builder")
                    and getattr(builder_provider, "supports_resume", False)):
                builder_call_resume = resume_sessions["builder"]
after:
            if False:
                builder_call_resume = resume_sessions["builder"]
```
Red: `exit=1 last_line='1 failed in 3.33s'`. Green (control above).

**Mutation 3 (Goal & Done claim 3 — the run's evidence records `resume_used`
true with the parked session's reference) —**
`packages/orchestration/pingpong_loop.py`, function `_session_fields`:
```
before:
        "resume_used": bool(getattr(out, "resume_used", False)),
after:
        "resume_used": False,
```
Red: `exit=1 last_line='1 failed in 3.33s'`. Green (control above).

**Mutation 4 (Acceptance claim 5 — `resume_session_ref` equal to the parked
session) —** `packages/orchestration/pingpong_provider.py`, method
`ClaudeCliProvider._build_impl`:
```
before:
                resume_session_ref=resume,
after:
                resume_session_ref="",
```
Red: `exit=1 last_line='1 failed in 3.63s'`. Green (control above).

**Verdict for test 1: PROVEN through the command line.** All four mutations
turn it red; the control is green.

### Test 2 — `test_the_relaunch_on_a_provider_that_cannot_resume_names_the_decline`

Control (unmutated): `exit=0 last_line='1 passed in 3.62s'`.

**Mutation 5 (command-line layer, the same user-path statement, second test) —**
`apps/cli/commands/do_cmd.py`, function `_cmd_run_show`:
```
before:
    if json_output:
        emit_ok(**data)
after:
    if json_output:
        data.pop("resume_declined", None)
        emit_ok(**data)
```
Red: `exit=1 last_line='1 failed in 3.81s'`. Green (control above).

**Mutation 6 (Goal & Done claim 4 — a provider that cannot resume says so in
the run's evidence instead of silently starting fresh) —**
`packages/orchestration/pingpong_loop.py`, function `run_pingpong` (the one
write site of `result.resume_declined`):
```
before:
    result.resume_declined = resume_declined_reasons(
        resume_sessions, builder=builder_provider, reviewer=reviewer_provider)
after:
    result.resume_declined = {}
```
Red: `exit=1 last_line='1 failed in 3.75s'`. Green (control above).

**Mutation 7 (Acceptance claim 8 — a provider that cannot resume records that
it did not) —** `packages/orchestration/pingpong_loop.py`, function
`resume_declined_reasons`:
```
before:
        if resume_sessions.get(role) and not getattr(provider, "supports_resume", False):
after:
        if False:
```
Red: `exit=1 last_line='1 failed in 3.89s'`. Green (control above).

**Mutation 8 (Acceptance claim 9 — a provider that cannot resume never fails
the relaunch for it) —** `packages/orchestration/pingpong_loop.py`, function
`resume_declined_reasons`:
```
before:
            declined[role] = reason
after:
            raise RuntimeError(f"relaunch failed: {role} cannot resume")
```
Red: `exit=1 last_line='1 failed in 2.54s'`. Green (control above).

**Verdict for test 2: PROVEN through the command line.** All four mutations
turn it red; the control is green.

### Gap verdict

**CLOSED.** The first audit's one standing gap was that every proof of
F287's claims called `run_job`, `run_pingpong`, or `resume_declined_reasons`
directly from test code, never through `apps.cli` or the cockpit. Round 9 adds
`tests/cli/test_job_run_session_resume.py`, which drives `remedy job run`
(twice — once to park, once to relaunch) and `remedy run show --json`
entirely through `apps.cli.grouped.main`, the real CLI dispatcher, with only
the `claude` child process and the two providers themselves stood in. Eight
mutations across both tests — four per test, at least one per test inside
`apps/cli/commands/do_cmd.py` itself — each turn red under the mutation and
green without it, covering Goal & Done claims 1, 3 and 4 and Acceptance
claims 5, 8 and 9 by name. No cockpit (`apps/ui`) path exists or was claimed;
the command-line half of "through the command line or the cockpit" is what
this round built, and it holds under mutation. Goal & Done claim 2 (the
STOP-interrupted case) and Acceptance claims 6-7 (copy-mode fallback-once)
remain proven only at the `run_job`/unit layer, as they were in the first
audit — the new CLI test exercises the PAUSE case and the declined-resume
case, not STOP or copy-mode fallback, so those three statements' standing
"proven, but not through the user path" status is unchanged by this round and
is not part of the gap this audit was repeated for.

## Inaccuracies noticed

- The module docstring's history note ("Round 8's block ordered this same
  test without `--repair-rounds` on the fake-provider relaunch; that relaunch
  inherited the parked run's persisted `repair_rounds=0` ...") could not be
  independently reproduced through the lever its own citation names
  (`packages/orchestration/pingpong_job.py::run_job`'s
  `if repair_rounds is not None:` branch): forcing the CLI's own
  `--repair-rounds` value to never reach `run_job` (via
  `apps/cli/commands/do_cmd.py`'s own, earlier `if repair_rounds is not
  None:` gate) left the second test green, not red, so the full causal
  chain the docstring recites was not confirmed end to end here. This is not
  a claim that the docstring's history is wrong — round 8's actual failure is
  outside what this audit read (`.agent/handoff.md` round 8 is explicitly
  off-limits) — only a note that the specific mechanism as quoted did not
  reproduce under the one lever this audit tried, so a reader should not take
  the docstring's parenthetical as independently re-verified by this round.
- No other inaccuracy found: the claimed CLI-only call path, the "every call
  goes through `run_cli_in_process`" claim, and the per-test field assertions
  all matched what the code does.

## Worktree

```
$ git worktree list
/home/decodeux/Repos/remedy                                                                                                                           7afbf9d02 [feature/f287-provider-session-continuity]
/home/decodeux/Repos/remedy/.remedy-wt/job-034ab8c2d9fa4013                                                                                           218eaabd6 [remedy/job-034ab8c2d9fa4013]
/home/decodeux/Repos/remedy/.remedy-wt/job-129b3ad7206d4f8d                                                                                           09441a92a [remedy/job-129b3ad7206d4f8d]
/home/decodeux/Repos/remedy/.remedy-wt/job-1fe227733cbf41eb                                                                                           218eaabd6 [remedy/job-1fe227733cbf41eb]
/home/decodeux/Repos/remedy/.remedy-wt/job-6a38b3203cca4928                                                                                           aab638e21 [remedy/job-6a38b3203cca4928]
/home/decodeux/Repos/remedy/.remedy-wt/job-d0f70d9d45dd4363                                                                                           e4fa7d06f [remedy/job-d0f70d9d45dd4363]
/home/decodeux/Repos/remedy/.remedy-wt/job-e7268925db3a4831                                                                                           cc8696a37 [remedy/job-e7268925db3a4831]
/home/decodeux/Repos/remedy/.remedy-wt/job-e7a145761bf04f86                                                                                           03d435e59 [remedy/job-e7a145761bf04f86]
/home/decodeux/Repos/remedy/.remedy-wt/job-f03587d31f444b15                                                                                           3f36bd811 [remedy/job-f03587d31f444b15]
/home/decodeux/Repos/remedy/.remedy-wt/job-f146c82a6d8e42ca                                                                                           8b6e803f7 [remedy/job-f146c82a6d8e42ca]
/home/decodeux/Repos/remedy/.remedy-wt/job-f196d785124e48bc                                                                                           3f36bd811 [remedy/job-f196d785124e48bc]
/home/decodeux/Repos/remedy/.remedy-wt/job-fd57a5d1dfe245b0                                                                                           68c833e6c [remedy/job-fd57a5d1dfe245b0]
(plus several /tmp/pytest-of-.../... entries marked "prunable", pre-existing
leftovers from unrelated prior test runs, not created or touched by this
re-audit — the same set of names the first audit already recorded as
pre-existing)
```

This re-audit's own worktree, `/home/decodeux/Repos/remedy/.remedy-wt/f287-reaudit-wt`,
is absent from this list — it was removed with `git worktree remove --force`
as this audit's last action. The `.remedy-wt/job-*` and
`/tmp/pytest-of-.../...` entries predate this audit and were not created,
entered, or modified by it.
