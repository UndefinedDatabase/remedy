"""F260 D2: the JOB, RUN and EPISODE call sites mint through data_paths, not inline.

WHY THIS FILE EXISTS. Moving four ``uuid4().hex[:16]`` expressions onto
``mint_job_id``, ``mint_run_id`` and ``mint_episode_id`` changes no behaviour: a site
that drifts back to an inline mint still produces a correct-looking 16-hex id, so no
existing suite goes red on its own. DECISION F260 D2 is about WHICH FUNCTION names each
kind, and that is only observable by reading the call sites. These tests are that reading.

THE TWO DATACLASS DEFAULTS ARE PINNED BY OBJECT IDENTITY. ``default_factory is
data_paths.mint_job_id`` runs against the shipped function object, and — unlike any text
check — is NOT satisfied by a look-alike ``lambda: mint_job_id()``, which would pass every
behavioural test while putting the inline-expression habit straight back.

THE TWO ``active_episode_id`` ASSIGNMENTS HAVE NO OBJECT TO COMPARE — they live inside
``run_job``'s body — so they are read by parsing the module. The source is located through
the imported module's own ``__file__`` rather than by a path spelled here, so the test
reads the file that was actually imported, including inside a disposable worktree.

THE ``uuid4`` ABSENCE TEST READS ``ast.Name`` NODES, NEVER A SUBSTRING. A docstring or a
comment that DISCUSSES ``uuid4`` is not a call site, and a guard that cannot tell the two
apart would forbid the prose that explains the change.
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from packages.orchestration import data_paths, pingpong_job, pingpong_loop


def _parsed(module) -> ast.Module:
    """Parse the module that was actually imported, via its own ``__file__``."""
    return ast.parse(Path(module.__file__).read_text(encoding="utf-8"))


class TestMintCallSites:
    """The four sites DECISION F260 D2 reaches, and the imports they left behind."""

    def test_job_plan_job_id_default_is_the_mint_function_itself(self) -> None:
        """Identity, not equality: a ``lambda: mint_job_id()`` wrapper must NOT pass."""
        factory = pingpong_job.JobPlan.__dataclass_fields__["job_id"].default_factory

        assert factory is data_paths.mint_job_id

    def test_pingpong_result_run_id_default_is_the_mint_function_itself(self) -> None:
        """Same identity reading for the RUN kind (DECISION F260 D1/D2)."""
        factory = pingpong_loop.PingPongResult.__dataclass_fields__["run_id"].default_factory

        assert factory is data_paths.mint_run_id

    def test_every_active_episode_id_assignment_calls_mint_episode_id(self) -> None:
        """Both in-body episode sites, read by AST because there is no object to compare."""
        assignments = [
            node for node in ast.walk(_parsed(pingpong_job))
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Attribute) and target.attr == "active_episode_id"
                for target in node.targets
            )
        ]

        # Non-vacuity: a walk that found nothing would make the assertion below trivially true.
        assert len(assignments) == 2, (
            f"expected 2 active_episode_id assignments in pingpong_job.py, "
            f"found {len(assignments)}"
        )

        for node in assignments:
            value = node.value
            assert isinstance(value, ast.Call), (
                f"active_episode_id at line {node.lineno} is not a call"
            )
            assert isinstance(value.func, ast.Name) and value.func.id == "mint_episode_id", (
                f"active_episode_id at line {node.lineno} does not mint through "
                f"mint_episode_id"
            )

    @pytest.mark.parametrize(
        "module",
        [pingpong_job, pingpong_loop],
        ids=["pingpong_job", "pingpong_loop"],
    )
    def test_module_no_longer_names_uuid4(self, module) -> None:
        """``ast.Name`` nodes only — prose that mentions ``uuid4`` is not a call site."""
        names = [
            node for node in ast.walk(_parsed(module))
            if isinstance(node, ast.Name) and node.id == "uuid4"
        ]

        assert names == [], (
            f"{Path(module.__file__).name} still names uuid4 at lines "
            f"{[node.lineno for node in names]}"
        )
