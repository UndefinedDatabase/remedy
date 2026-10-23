"""The context built for one builder call: moved out of `run_pingpong` as structure-ledger step
(5) of that function (DECISION F141 D2).
"""
from __future__ import annotations

from pathlib import Path

from packages.orchestration.permission_matrix import (
    PermissionRequest,
    pin_job_level,
    require_permission,
)


def build_builder_context(
    *,
    repo_path: str,
    goal: str,
    mentioned_files: list[str] | None,
    compiled_context_paths: list[str] | None,
    compiled_context_candidates: list[str] | None,
    compiled_context_token_budget: int | None,
    context_record_dir: str | Path | None,
    job_id: str = "",
) -> tuple[str, list[str]]:
    # DECISION F141 D2 (3): the `read` seam, checked against the level pinned to this job's
    # first context — before anything else, so a denied read never touches the repo.
    subject = f"the builder's context of job {job_id}" if job_id else "the builder's context"
    require_permission(
        "read", PermissionRequest(level=pin_job_level(job_id), subject=subject, job_id=job_id or None),
    )
    # F107: the COMPILED context replaces the whole-file context pack's SELECTION —
    # never its formatting — and only when the caller hands in BOTH the task's fenced
    # scope and the repo's candidate listing; one list alone is a caller mistake and
    # must not silently half-compile, so it stays on the default path.
    # Deliberately absent here: ``run_pingpong`` does NOT list the repo itself and does
    # NOT read a task's ``files_hint``. Both are the caller's, which is what keeps this
    # path opt-in and keeps ``packages/`` free of a second tree walk.
    use_compiled_context = bool(compiled_context_paths) and bool(compiled_context_candidates)
    if use_compiled_context:
        # Imported inside the branch, so the default path's import cost does not change.
        from packages.orchestration.context_compiler import (
            COMPILED_CONTEXT_SEGMENT_NAME,
            CONTEXT_SIZE_FILENAME,
            OMITTED_CONTEXT_FILENAME,
            compare_context_size,
            compile_task_context,
            render_compiled_context_text,
            write_context_size_comparison_json,
            write_omitted_context_json,
        )

        compiled_root = Path(repo_path)
        # F112 T003b2a: only override the compiler's default token budget
        # when the caller supplies one, so no existing caller's behavior
        # changes (compile_task_context's own default stays in force).
        compile_kwargs: dict[str, int] = {}
        if compiled_context_token_budget is not None:
            compile_kwargs["token_budget"] = compiled_context_token_budget
        compiled = compile_task_context(
            compiled_root, compiled_context_paths or [], compiled_context_candidates or [],
            **compile_kwargs,
        )
        context = render_compiled_context_text(compiled_root, compiled)
        categories = [COMPILED_CONTEXT_SEGMENT_NAME]
        if context_record_dir:
            record_dir = Path(context_record_dir)
            write_omitted_context_json(compiled, record_dir / OMITTED_CONTEXT_FILENAME)
            write_context_size_comparison_json(
                compare_context_size(
                    compiled_root, compiled_context_candidates or [], compiled,
                ),
                record_dir / CONTEXT_SIZE_FILENAME,
            )
    else:
        from packages.orchestration import pingpong_loop

        context, categories = pingpong_loop.build_repo_context(
            repo_path, goal, mentioned_files=mentioned_files,
        )
    return context, categories
