# F287 Provider session continuity across relaunch — Acceptance audit (amend0930b-slow-cap hardening stage)

## What was read, and what was not

Read: `docs/roadmap/features/T3_F287.md` (the subject file, in full); `AGENTS.md`
(start of file, Open PR Gate and Priority sections, for the operating rules
this audit itself must obey); `docs/agents/self_drive_protocol.md` (the
amend0930b-slow-cap paragraph defining this hardening stage, and the G7/G8
guardrail paragraphs around it); `docs/system/session-resume-v1.md` (the
feature's own Built State doc, read in full, including its "Which providers
resume (F287)" section); all of `tests/orchestration/test_relaunch_session_resume.py`;
the relevant regions of `packages/orchestration/pingpong_loop.py` (`run_pingpong`'s
round-1 resume gate, the fallback-once gate, `resume_declined_reasons`,
`_session_fields`, `parked_session_refs`, `export_pingpong_json`),
`packages/orchestration/pingpong_job.py` (`run_job`'s relaunch gate around
line 3648), and `packages/orchestration/pingpong_provider.py` (`ClaudeCliProvider`,
`ClaudeProvider`, `OllamaPingPongProvider`, `FakeProvider` — `supports_resume`,
`resume_unsupported_reason`, `_build_impl`); `apps/cli/commands/do_cmd.py` and
`apps/cli/commands/job_rerun_cmd.py` (to locate the real CLI entry point for a
relaunch, `remedy job run <job_id>`, and confirm it is distinct from the
subtree-rerun command); directory listings of `tests/cli/`, `apps/ui/` and a
grep across both trees for every resume-related identifier
(`resume_used`, `resume_session_ref`, `resume_declined`, `resume_fallback`,
`parked_session_refs`, `resumed_from_run_id`). Not read, as instructed:
`.agent/handoff.md`, `.agent/live_review.md`, `.agent/live_review_archive.md`,
`.agent/plan.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, anything
under `.agent/authored/`, and any `.remedy-wt/f287-r*` folder.

## How the mutations ran

One disposable worktree, `git worktree add --detach
/home/decodeux/Repos/remedy/.remedy-wt/f287-audit-wt 4c24c266c`, created at the
pinned tip of `feature/f287-provider-session-continuity`. Every mutation was
applied by a small Python driver
(`.remedy-wt/f287-audit/mutate_run.py`, gitignored scratch, not under `/tmp`)
that reads an exact old/new snippet pair from sibling text files, asserts the
old string occurs exactly once in the target file inside the worktree, writes
the mutated file, runs `python3 -B -m pytest -q -p no:cacheprovider <node id>`
as a subprocess with `cwd` set to the worktree, captures the exit code and
last output line, and restores the file byte-for-byte in a `finally` block
before the next mutation. Nothing was mutated in the primary checkout. Each of
the six distinct test node ids used below was first run once, unmutated, as
its own control (all six passed). The nine mutations then ran strictly one at
a time, never two pytest processes concurrently, each against exactly one
node id — never a full module, never `-n`, never `REMEDY_TEST_MAX_WORKERS`.
No real `claude` process or network call starts in any of these tests; every
production-provider path used is already patched to a recorded stand-in
(`pingpong_provider._guarded_cli_run`) or a `FakeProvider`. After all nine
mutations, `git -C .../f287-audit-wt status --porcelain` was empty and
`git -C /home/decodeux/Repos/remedy status --porcelain` was empty throughout
and at the end; the worktree was then removed with `git worktree remove
--force`.

**Total claims audited: 9. Proven at once: 9. Gaps: 0 (plus 1 standing GAP: no user-path proof).**

## Claim 1 (Goal & Done) — a relaunch of a task a PAUSE interrupted, on `claude-cli`, resumes the parked session

**Test:** `tests/orchestration/test_relaunch_session_resume.py::TestAParkedClaudeCliTaskResumesOnRelaunch::test_a_git_target_pause_resumes_the_parked_builder_session_on_relaunch`

**Mutation:** `packages/orchestration/pingpong_loop.py`, function `run_pingpong` (the round-1 resume-offer gate) —
```
before:
            if (round_num == 1 and resume_sessions.get("builder")
                    and getattr(builder_provider, "supports_resume", False)):
                builder_call_resume = resume_sessions["builder"]
after:
            if False:
                builder_call_resume = resume_sessions["builder"]
```

**Red:** `MUTATED exit=1 last_line='1 failed in 3.00s'`
**Green (control, same node id, unmutated):** `CONTROL exit=0 last_line='1 passed in 3.16s'`

**Reaches the user:** No — through `run_job` called directly in test code (the test
drives a real `claude-cli` `ClaudeCliProvider` and a real git worktree, with only
`pingpong_provider._guarded_cli_run` replaced by a recorded stand-in for the
`claude` child process), not through `apps.cli` or the cockpit.

**PROVEN**

## Claim 2 (Goal & Done) — a relaunch of a task a STOP interrupted, on `claude-cli`, resumes the parked session

**Test:** `tests/orchestration/test_relaunch_session_resume.py::TestAParkedClaudeCliTaskResumesOnRelaunch::test_a_git_target_stop_resumes_the_parked_builder_session_on_relaunch`

**Mutation:** `packages/orchestration/pingpong_job.py`, function `run_job` (the relaunch's "was this task's run parked?" gate) —
```
before:
            if task.run_id and task.final_status == "stopped":
after:
            if task.run_id and False:
```

**Red:** `MUTATED exit=1 last_line='1 failed in 2.87s'`
**Green (control):** `CONTROL exit=0 last_line='1 passed in 3.15s'`

**Reaches the user:** No — `run_job` called directly in test code, same stand-in
as Claim 1. (A pause and a stop both set `final_status == "stopped"` on the
interrupted run — `_record_stop` in `pingpong_loop.py` is the one code path
both go through — so this one gate serves both cases, each proven by its own
test here and in Claim 1.)

**PROVEN**

## Claim 3 (Goal & Done) — the run's evidence records `resume_used` true with the parked session's reference

**Test:** `tests/orchestration/test_relaunch_session_resume.py::TestAParkedClaudeCliTaskResumesOnRelaunch::test_a_git_target_pause_resumes_the_parked_builder_session_on_relaunch`

**Mutation:** `packages/orchestration/pingpong_loop.py`, function `_session_fields` (the generic evidence-recording function shared by every provider and role) —
```
before:
        "resume_used": bool(getattr(out, "resume_used", False)),
after:
        "resume_used": False,
```

**Red:** `MUTATED exit=1 last_line='1 failed in 2.59s'`
**Green (control):** same as Claim 1's control (`1 passed in 3.16s`)

**Reaches the user:** No — same test as Claim 1.

**PROVEN**

## Claim 4 (Goal & Done) — every production provider that cannot resume says so in the run's evidence instead of silently starting fresh

**Test:** `tests/orchestration/test_relaunch_session_resume.py::TestAnOfferedSessionAProviderCannotResumeIsNamed::test_run_pingpong_records_the_declined_roles_in_its_export_and_on_disk`

**Mutation:** `packages/orchestration/pingpong_loop.py`, function `run_pingpong` (the one write site of `result.resume_declined`) —
```
before:
    result.resume_declined = resume_declined_reasons(
        resume_sessions, builder=builder_provider, reviewer=reviewer_provider)
after:
    result.resume_declined = {}
```

**Red:** `MUTATED exit=1 last_line='1 failed in 0.64s'`
**Green (control):** `CONTROL exit=0 last_line='1 passed in 0.99s'`

**Reaches the user:** No — direct `run_pingpong` call in test code. Note: this
test's non-resuming role is a `FakeProvider` standing in for "a provider that
cannot resume" generically; Claim 8 below proves the same mechanism against
the real `ClaudeProvider`/`OllamaPingPongProvider` classes by name.

**PROVEN**

## Claim 5 (Acceptance) — a relaunch on `claude-cli` records round 1's builder `resume_used` true with `resume_session_ref` equal to the parked session

**Test:** `tests/orchestration/test_relaunch_session_resume.py::TestAParkedClaudeCliTaskResumesOnRelaunch::test_a_git_target_pause_resumes_the_parked_builder_session_on_relaunch`

**Mutation:** `packages/orchestration/pingpong_provider.py`, method `ClaudeCliProvider._build_impl` —
```
before:
                resume_session_ref=resume,
after:
                resume_session_ref="",
```

**Red:** `MUTATED exit=1 last_line='1 failed in 2.69s'`
**Green (control):** same as Claim 1's control

**Reaches the user:** No — same test as Claim 1, this time mutated at the
provider-output layer rather than the evidence-export layer (Claim 3), giving
this claim its own distinct mutation.

**PROVEN**

## Claim 6 (Acceptance) — a refused resume falls back once to a fresh session

**Test:** `tests/orchestration/test_relaunch_session_resume.py::TestAParkedClaudeCliTaskResumesOnRelaunch::test_a_copy_mode_pause_falls_back_once_on_relaunch`

**Mutation:** `packages/orchestration/pingpong_loop.py`, function `run_pingpong` (the fallback-once gate on the Builder side) —
```
before:
            if builder_call_resume and builder_out.error:
after:
            if False and builder_call_resume and builder_out.error:
```

**Red:** `MUTATED exit=1 last_line='1 failed in 1.45s'`
**Green (control):** `CONTROL exit=0 last_line='1 passed in 1.78s'`

**Reaches the user:** No — `run_job` called directly in test code, with a
`claude-cli` run in copy mode (no git target), so the stand-in genuinely
refuses the `--resume` the relaunch offers (wrong working directory), exactly
as a real `claude --resume` would against a session it cannot find.

**PROVEN**

## Claim 7 (Acceptance) — the fallback is recorded in the run's evidence

**Test:** `tests/orchestration/test_relaunch_session_resume.py::TestAParkedClaudeCliTaskResumesOnRelaunch::test_a_copy_mode_pause_falls_back_once_on_relaunch`

**Mutation:** `packages/orchestration/pingpong_loop.py`, function `_session_fields` —
```
before:
        "resume_fallback": bool(getattr(out, "resume_fallback", False)),
after:
        "resume_fallback": False,
```

**Red:** `MUTATED exit=1 last_line='1 failed in 1.43s'`
**Green (control):** same as Claim 6's control

**Reaches the user:** No — same test as Claim 6.

**PROVEN**

## Claim 8 (Acceptance) — a provider that cannot resume records that it did not

**Test:** `tests/orchestration/test_relaunch_session_resume.py::TestAnOfferedSessionAProviderCannotResumeIsNamed::test_each_offered_role_names_its_providers_own_reason`

**Mutation:** `packages/orchestration/pingpong_loop.py`, function `resume_declined_reasons` —
```
before:
        if resume_sessions.get(role) and not getattr(provider, "supports_resume", False):
after:
        if False:
```

**Red:** `MUTATED exit=1 last_line='1 failed in 0.57s'`
**Green (control):** `CONTROL exit=0 last_line='1 passed in 0.67s'`

**Reaches the user:** No — this test calls `resume_declined_reasons` directly
as a unit, against real `ClaudeProvider()`/`OllamaPingPongProvider()`
instances (the actual production classes, not `FakeProvider`); it does not go
through `run_pingpong` or `run_job` at all.

**PROVEN**

## Claim 9 (Acceptance) — a provider that cannot resume never fails the relaunch for it

**Test:** `tests/orchestration/test_relaunch_session_resume.py::TestAnOfferedSessionAProviderCannotResumeIsNamed::test_the_relaunch_names_the_role_and_reason_the_provider_declined_to_resume`

**Mutation:** `packages/orchestration/pingpong_loop.py`, function `resume_declined_reasons` (the line that is one iteration of the per-role naming loop, turned into a bug that would have made a declined resume a terminal error rather than an evidenced no-op) —
```
before:
            declined[role] = reason
after:
            raise RuntimeError(f"relaunch failed: {role} cannot resume")
```

**Red:** `MUTATED exit=1 last_line='1 failed in 1.01s'`
**Green (control):** `CONTROL exit=0 last_line='1 passed in 1.33s'`

**Reaches the user:** No — `run_job` called directly in test code; the test
asserts `resumed.state == JOB_COMPLETED`, which is exactly what the mutation
(an exception raised mid-relaunch) breaks.

**PROVEN**

## User-path proof

**GAP: no user-path proof.** A grep of `tests/cli/`, `apps/cli/commands/` and
`apps/ui/` for every resume identifier (`resume_used`, `resume_session_ref`,
`resume_declined`, `resume_fallback`, `parked_session_refs`,
`resumed_from_run_id`) finds none outside `tests/orchestration/`. The real CLI
entry point that performs a relaunch is `remedy job run <job_id>`
(`apps/cli/commands/do_cmd.py`, which calls `pingpong_job.run_job` — confirmed
by reading the call site), distinct from `job_rerun_cmd.py`'s `rerun-subtree`,
which explicitly "names no run and starts no task itself." `tests/cli/test_job_pause.py`
does cover a `relaunch command` and a `task_resumed` event, but that is the
pause/release lifecycle event (a task leaving `paused` back to runnable), not
the provider-session-resume mechanism this feature built; it asserts nothing
about `resume_used`/`resume_session_ref`/`resume_declined`. No cockpit
(`apps/ui`) test references any of these fields either.

What such a test would have to do: drive `remedy job run <job_id>` as the CLI
would — either in-process through the `do_cmd`/`job.py` command function, or
as a subprocess (`python -m apps.cli ...` / the installed `remedy` entry
point) — against a job on a git target using `--builder-provider claude-cli
--reviewer-provider claude-cli`, with `pingpong_provider._guarded_cli_run`
patched to the same kind of recorded stand-in `test_relaunch_session_resume.py`
already uses (so no real `claude` process starts), first to pause or stop the
job mid-build through the CLI's own pause/stop command, then to run `job run`
again, then to read the relaunch's `result.json` / `remedy run show --json`
output (or the cockpit's run-detail page in a headless browser) and assert
`resume_used`, `resume_session_ref` and/or `resume_declined` the way
`test_relaunch_session_resume.py` already does at the `run_job` layer. This
was not written, per instructions.

## Docs contradictions

None found against `docs/system/session-resume-v1.md`. Specifically checked
and consistent: "claude-cli is the one production provider that resumes" —
`ClaudeCliProvider.supports_resume` returns `True`; `ClaudeProvider`/
`OllamaPingPongProvider` return `False` and expose `resume_unsupported_reason`
strings matching the doc's quoted examples verbatim (proven by Claim 8's
control). The copy-mode "always refused and falls back once... costs one
short child process and no tokens" claim matches
`test_a_copy_mode_pause_falls_back_once_on_relaunch` exactly (Claims 6–7). The
doc's "The prompt of that call stays full-context... no prompt shrink is
gated on it" is also consistent with the code read: the round-1 relaunch's
`builder_call_resume` is a separate variable from `builder_resume_ref` (the
only one that gates `builder_resume_hunks_text`), so a relaunch's resumed
round-1 call cannot reach the delta-prompt-shrink path — only a later repair
round's resume can.

## Worktree

```
$ git worktree list
/home/decodeux/Repos/remedy                                                                                                                           4c24c266c [feature/f287-provider-session-continuity]
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
(plus several /tmp/pytest-of-.../... entries marked "prunable", pre-existing leftovers from unrelated prior test runs, not created or touched by this audit)
```

The audit's own worktree, `/home/decodeux/Repos/remedy/.remedy-wt/f287-audit-wt`,
is absent from this list — it was removed with `git worktree remove --force`
as the audit's last action. The other `.remedy-wt/job-*` and
`/tmp/pytest-of-.../...` entries predate this audit and were not created,
entered, or modified by it.
