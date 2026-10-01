# F200 acceptance re-audit — repaired statements (amend0930b-slow-cap rule 3)

I read, in full, `docs/roadmap/features/T12_F200.md` (the whole file, treating
"Amendment — DECISION F200 D1" and the later "Amended by DECISION F200 Dn"
paragraphs as governing over the older Design/Acceptance text where they
disagree), the amend0930b-slow-cap paragraph of `docs/agents/self_drive_protocol.md`
(the full paragraph beginning "Operator amendment amend0930b-slow-cap
(2026-09-30)"), `AGENTS.md` in full, and the repository's production code and
tests relevant to the three statements below: `packages/orchestration/serve_daemon.py`,
`packages/orchestration/serve_runs.py`, `packages/orchestration/serve_paths.py`,
`apps/cli/serve_client.py`, `apps/cli/commands/job_stop_cmd.py`,
`apps/cli/commands/job_pause_cmd.py`, `apps/cli/commands/do_cmd.py`,
`packages/orchestration/ui_server.py` (the `_dispatch_job_stop` clause),
`scripts/serve/container-entrypoint.sh`, `scripts/serve/remedy-serve.service`,
`tests/orchestration/test_serve_stop_file.py`, `tests/orchestration/test_serve_artifacts.py`,
and `tests/cli/test_serve_client_scope.py`. I did not read `.agent/handoff.md`,
`.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/plan.md`,
`.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/f200_acceptance_audit.md`,
anything under `.agent/authored/`, or any `.remedy-wt/f200-*` directory other
than the two named below, as instructed.

Worktree: a disposable, detached worktree was created with
`git -C /home/decodeux/Repos/remedy worktree add --detach
/home/decodeux/Repos/remedy/.remedy-wt/f200-reaudit-wt HEAD`, at commit
`a661ffd0de8d3a3e1f33b8075bd2af2961b38c1d` (branch `feature/f200-daemon-mode`,
subject "F200 R8 C5: handback"), with `apps/ui/dist` copied into it by
`shutil.copytree(..., symlinks=True)` before any test ran. Every pytest
invocation and every mutation below ran inside that worktree, never in the
primary checkout; `git -C /home/decodeux/Repos/remedy status --porcelain`
printed nothing before the worktree was created and nothing after it was
removed. Every pytest call used exactly
`python3 -B -m pytest <one file or node id> -q -n auto -p no:cacheprovider`,
one selection at a time, never the full suite, and no run reported leftover
processes. The worktree was removed afterward with
`git -C /home/decodeux/Repos/remedy worktree remove --force
/home/decodeux/Repos/remedy/.remedy-wt/f200-reaudit-wt`, confirmed gone from
`git -C /home/decodeux/Repos/remedy worktree list`.

Statements re-audited: 3. Proven: 3. Gaps: 0.

## Statement 1 — the STOP file stops a supervised run exactly as a direct one

Quote (Acceptance as amended): "A STOP file (F011) stops a run the supervisor
started, exactly as it stops a direct run."

**What meets it.** `packages/orchestration/serve_runs.py`'s `RunLauncher.start`
runs a job's child process with `REMEDY_DATA_DIR` set to
`str(self._paths.root.parent)` — the real data root one level above the
`serve` class directory (`packages/orchestration/serve_paths.py`'s
`ServePaths.root` is the `serve` class directory itself; its parent is the
data root every other `remedy` command resolves). Because the run is plain
`remedy job run <job>` in direct mode (`DIRECT_ENV` set), it reads and writes
the SAME `safe_points` stop-request file a direct run would, under the SAME
data root. On the command-line side, `apps/cli/commands/job_stop_cmd.py`'s
`_cmd_job_stop` calls `apps.cli.serve_client.forward_effect(job_id, "job.stop",
{"reason": reason, "source": source or "cli"}, ...)` when `supervisor_answers()`
is true; `forward_effect` posts an F009 envelope to the supervisor's socket,
whose handler (`packages/orchestration/ui_server.py`'s `_dispatch_job_stop`)
calls the same `safe_points.request_stop` a direct `job stop` calls, under the
data root the socket's own process resolves. The two paths converge on the
identical stop-file mechanism; only the process that writes it differs.

**Test node ids.** `tests/orchestration/test_serve_stop_file.py` (whole file;
module-scoped `runs` fixture shared by all 6 tests):
- `test_the_run_reaches_the_same_stopped_end_in_each_mode[direct]`
- `test_the_run_reaches_the_same_stopped_end_in_each_mode[supervised]`
- `test_only_the_supervised_stop_goes_through_the_doors_audit`
- `test_the_stop_commands_output_and_exit_code_are_equal_between_modes`
- `test_the_runs_process_exit_code_is_equal_between_modes`
- `test_the_jobs_own_record_is_equal_between_modes`

**Mutation A — the supervisor's side (how its run finds the job's data root).**
File: `packages/orchestration/serve_runs.py`. Before:
`                   "REMEDY_DATA_DIR": str(self._paths.root.parent),`
After:
`                   "REMEDY_DATA_DIR": str(self._paths.root),`
Red reading: `python3 -B -m pytest tests/orchestration/test_serve_stop_file.py
-q -n auto -p no:cacheprovider` inside the worktree, exit code 1, summary
"6 errors in 26.76s" — every test errored with `AssertionError: timed out
waiting for the supervised fixture's marker` (the run subprocess could not
find the job under the wrong data root, so it never reached the point of
writing its marker). Restore verified byte-identical (sha256 match). Green
reading: the same command, exit code 0, summary "6 passed in 2.40s".

**Mutation B — the command line's client-mode stop.**
File: `apps/cli/commands/job_stop_cmd.py`. Before:
`        body = forward_effect(job_id, "job.stop", {"reason": reason, "source": source or "cli"},`
After:
`        body = forward_effect(job_id, "job.stop", {"source": source or "cli"},`
(dropping the `reason` key the client-mode stop forwards; the door's
`_dispatch_job_stop` then defaults a missing `reason` to `""`, which the job
record in turn reports back as "unknown" rather than the operator's actual
reason). Red reading: same command, exit code 1, summary "1 failed, 5 passed
in 2.58s" — `test_the_stop_commands_output_and_exit_code_are_equal_between_modes`
failed: `AssertionError: assert (0, 'Stop req...son: proof\n') == (0, 'Stop
req...n: unknown\n')`, i.e. the direct mode's stop output names reason
"proof" (the `--reason proof` both subprocesses were given) while the
mutated client-mode stop reports "unknown". Restore verified byte-identical.
Green reading: same command, exit code 0, summary "6 passed in 2.59s".

**Verdict: PROVEN.**

## Statement 2 — the container entrypoint expects an init process

Quote (Amended by DECISION F200 D8): "...the container entrypoint ... expects
the container to run with an init process."

**What meets it.** `scripts/serve/container-entrypoint.sh`'s header comment
states "Run the container with an init process, e.g. `docker run --init
...`" and explains why: "a job run started by the supervisor spawns its own
helper processes, and only an init process reaps the ones that outlive their
parent." The same requirement also appears in the built-state page
`docs/system/serve-daemon-v1.md` ("docker run --init"), so an operator
reading either the script or the docs sees it.

**Test node id.**
`tests/orchestration/test_serve_artifacts.py::test_entrypoint_and_docs_both_tell_the_operator_to_run_with_an_init_process`

**Mutation.** File: `scripts/serve/container-entrypoint.sh`. Before:
`# Run the container with an init process, e.g. `docker run --init ...`: a job`
After:
`# Run the container the normal way, e.g. `docker run ...`: a job`
Red reading: `python3 -B -m pytest
tests/orchestration/test_serve_artifacts.py::test_entrypoint_and_docs_both_tell_the_operator_to_run_with_an_init_process
-q -n auto -p no:cacheprovider` inside the worktree, exit code 1, summary
"1 failed in 0.66s" — `AssertionError: assert '--init' in '#!/usr/bin/env
bash\n# container-entrypoint.sh ...'`. Restore verified byte-identical. Green
reading: same command, exit code 0, summary "1 passed in 0.67s".

**Verdict: PROVEN.**

## Statement 3 — client mode's exact four-command boundary

Quote (Amended by DECISION F200 D4): "Client mode covers `job.stop`,
`job.pause`, `job.unpause` and `job.run`; the other commands the cockpit's
door carries run direct in both modes, as the commands it does not carry
do."

**What meets it.** `apps/cli/serve_client.py` defines `forward_effect` and
`supervisor_answers` but calls neither itself; the only call sites under
`apps/` and `packages/` are in `apps/cli/commands/job_stop_cmd.py`
(`"job.stop"`), `apps/cli/commands/job_pause_cmd.py` (`"job.pause"` and
`"job.unpause"`), and `apps/cli/commands/do_cmd.py` (`"job.run"`). Every
other door-carried command's handler runs its effect directly in both modes,
with no `supervisor_answers()`/`forward_effect` branch at all.

**Test node ids.** `tests/cli/test_serve_client_scope.py` (whole file; an
`ast`-based static scan, not an import):
- `test_every_forward_effect_command_is_one_of_the_four_door_literals`
- `test_only_the_four_command_modules_reach_the_client_bridge`

**Mutation A — a fifth command forwards through the client bridge.**
File: `apps/cli/commands/job_stop_cmd.py`. Before:
`COMMAND_HANDLERS = {`
After (inserted immediately above that line, as new dead code that is never
called — a pure AST-visible addition):
```
def _unused_cancel_forward() -> None:
    """Dead code: a mutation probe, never called. Adds a fifth literal to the
    client bridge's command set to prove test_serve_client_scope.py's guard."""
    forward_effect("job-id", "job.cancel", {}, json_output=False, error="x", subject="x")


COMMAND_HANDLERS = {
```
Red reading: `python3 -B -m pytest tests/cli/test_serve_client_scope.py -q -n
auto -p no:cacheprovider` inside the worktree, exit code 1, summary "1
failed, 1 passed in 1.61s" —
`test_every_forward_effect_command_is_one_of_the_four_door_literals` failed:
`AssertionError: assert {'job.cancel', ...} == frozenset({...})`, "Extra
items in the left set: 'job.cancel'". Restore verified byte-identical. Green
reading: same command, exit code 0, summary "2 passed in 1.54s".

**Mutation B — one of the four is dropped.**
File: `apps/cli/commands/job_pause_cmd.py`. Before:
`            job_id, "job.pause", _door_args(task_id, source, reason=reason),`
After:
`            job_id, "job.stop", _door_args(task_id, source, reason=reason),`
(the pause command now forwards the literal `"job.stop"` instead of
`"job.pause"`, so the set of forwarded literals loses `job.pause` entirely).
Red reading: same command, exit code 1, summary "1 failed, 1 passed in
1.59s" — `test_every_forward_effect_command_is_one_of_the_four_door_literals`
failed: `AssertionError: assert {'job.run', ...} == frozenset({...})`,
"Extra items in the right set: 'job.pause'" (i.e. `job.pause` is missing
from what the code actually forwards). Restore verified byte-identical.
Green reading: same command, exit code 0, summary "2 passed in 1.58s".

**Verdict: PROVEN.**
