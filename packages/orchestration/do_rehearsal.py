"""F055 — a rehearsal's stop: `remedy do`'s `--rehearse` flag plans an order and halts at the
same boundary `--plan-only` halts at, naming the approval each waiting job still needs and the
run that would follow it, without running any job (DECISION F055 D1); a later round adds the
rehearsal's own record here.
"""

from __future__ import annotations

from packages.orchestration.do_context import DO_STEP_STOPPED, DoContext, _job_run_role_flags


# WHY: a rehearsal stops exactly where `--plan-only` stops, but names the approval a waiting
# job still needs before its `job run` line, so the rehearsed plan is one `yes` away from a run.
def stop_walk_for_rehearsal(ctx: DoContext) -> tuple[str, str]:
    """Stop the walk before any job runs, naming each job's approval and run command."""
    from packages.orchestration.job_plan import task_plan_blocks_execution
    from packages.orchestration.pingpong_job import load_job_plan

    for job_id in ctx.job_ids:
        job = load_job_plan(job_id)
        if job is not None and task_plan_blocks_execution(job) is not None:
            ctx.next_lines.append(f"remedy decision resolve {job_id} plan:approval --reason approve")
        ctx.next_lines.append(f"remedy job run {job_id}{_job_run_role_flags(ctx)}")
    return DO_STEP_STOPPED, (
        f"--rehearse: no job was run and nothing was written to the repository; "
        f"{len(ctx.job_ids)} job(s) rehearsed, mission plan: {ctx.mission_plan_path}")
