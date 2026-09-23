"""F258 T002 — tests for running a planned self-use item to the approval gate.

The load-bearing tests here are
:meth:`TestRunNextSelfUseItem.test_it_runs_the_planned_item_to_completion`,
which pins that a real run happens (not merely a plan), and
:meth:`TestRunNextSelfUseItem.test_a_blocked_plan_raises_rather_than_running`,
which pins that a curation defect is refused loudly rather than run anyway.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

import packages.orchestration.self_use_runner as self_use_runner
from packages.orchestration.pingpong_job import JOB_COMPLETED
from packages.orchestration.pingpong_provider import FakeProvider
from packages.orchestration.role_config import DEFAULT_PROVIDER, RoleConfig
from packages.orchestration.self_use_runner import SelfUseRunError, run_next_self_use_item

_PENDING_ITEM = {
    "id": "SU-042",
    "title": "A curated item",
    "why": "Because the track must run on something.",
    "job_markdown": (
        "# Job: Demo\n\n## Task 1\nDo the thing.\n\nAcceptance:\n- it is done\n"
    ),
    "consumed_by": "",
    "provenance": "operator-curated (fixture)",
}

_BLOCKED_ITEM = {
    "id": "SU-043",
    "title": "A malformed item",
    "why": "Because a curation defect must be caught, not run.",
    "job_markdown": "# Job: Empty job\n\nThis file has no task headings.\n",
    "consumed_by": "",
    "provenance": "operator-curated (fixture)",
}


def _pass_provider() -> FakeProvider:
    return FakeProvider(pass_on_round=1, fail_on_round=99)


@pytest.fixture
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=str(repo), capture_output=True, text=True, check=True
    ).stdout


@pytest.fixture
def demo_repo(tmp_path: Path) -> Path:
    """A real git repo, so the run takes the ISOLATED WORKTREE path (T002's own words)."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@e.com")
    _git(repo, "config", "user.name", "T")
    _git(repo, "config", "commit.gpgsign", "false")
    (repo / "README.md").write_text("# Demo\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "init")
    return repo


def _write_queue(tmp_path: Path, items: list[dict]) -> Path:
    path = tmp_path / "self_use_queue.json"
    body = {"schema_version": 2, "description": "fixture queue", "items": items}
    path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    return path


class TestRunNextSelfUseItem:
    """Planning happens once, running happens once, applying never happens."""

    def test_it_runs_the_planned_item_to_completion(self, tmp_path, isolate_data_root, demo_repo):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])
        entry, job_file_path, result = run_next_self_use_item(
            tmp_path / "jobs",
            str(demo_repo),
            queue_path=queue_path,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        assert entry.id == "SU-042"
        assert job_file_path.exists()
        assert result.state == JOB_COMPLETED
        assert result.isolation_mode == "worktree"

    def test_it_attaches_the_small_budget(self, tmp_path, isolate_data_root, demo_repo):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])
        _entry, _path, result = run_next_self_use_item(
            tmp_path / "jobs",
            str(demo_repo),
            queue_path=queue_path,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        # amend0920-selfuse-real D2 raised this path's own bound: six stopped a
        # run mid-loop where the repair round was the point.
        assert result.budgets["max_provider_calls"] == 8
        assert result.budgets["max_cost_usd"] == 1.00

    def test_it_never_mutates_the_target_repo(self, tmp_path, isolate_data_root, demo_repo):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])
        before = _git(demo_repo, "status", "--porcelain")
        run_next_self_use_item(
            tmp_path / "jobs",
            str(demo_repo),
            queue_path=queue_path,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        after = _git(demo_repo, "status", "--porcelain")
        assert before == after == ""

    def test_it_never_marks_the_queue_item_consumed(self, tmp_path, isolate_data_root, demo_repo):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])
        before = queue_path.read_text(encoding="utf-8")
        run_next_self_use_item(
            tmp_path / "jobs",
            str(demo_repo),
            queue_path=queue_path,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        assert queue_path.read_text(encoding="utf-8") == before

    def test_a_blocked_plan_raises_rather_than_running(self, tmp_path, isolate_data_root, demo_repo):
        queue_path = _write_queue(tmp_path, [dict(_BLOCKED_ITEM)])
        with pytest.raises(SelfUseRunError) as excinfo:
            run_next_self_use_item(tmp_path / "jobs", str(demo_repo), queue_path=queue_path)
        assert "SU-043" in str(excinfo.value)

    def test_an_exhausted_queue_raises_the_planning_error(self, tmp_path, isolate_data_root, demo_repo):
        consumed = dict(_PENDING_ITEM, id="SU-041", consumed_by="F256")
        queue_path = _write_queue(tmp_path, [consumed])
        from packages.orchestration.self_use_job import SelfUseJobError

        with pytest.raises(SelfUseJobError):
            run_next_self_use_item(tmp_path / "jobs", str(demo_repo), queue_path=queue_path)


class TestUnflaggedProviderResolution:
    """R-0757: an unflagged run must resolve a REAL configured provider, never
    silently inherit run_job's own raw "fake" fallback.

    WHICH provider that is changed at amend0920-selfuse-real (DECISION D2): both
    sides now come from the one `self_use` role, whose built-in default is the
    frontier provider, rather than one each from the product-default `builder`
    and `reviewer` roles. R-0757's own rule — resolve something real or refuse —
    is untouched and still pinned below.
    """

    def test_it_resolves_the_self_use_role_when_unflagged(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])
        captured: dict = {}

        def _stub_run_job(job_id, **kwargs):
            captured.update(kwargs)
            return "STUB_RESULT"

        monkeypatch.setattr(self_use_runner, "run_job", _stub_run_job)

        _entry, _path, result = run_next_self_use_item(
            tmp_path / "jobs", str(demo_repo), queue_path=queue_path
        )

        assert result == "STUB_RESULT"
        assert captured["builder_name"] == "claude-cli"
        assert captured["reviewer_name"] == "claude-cli"
        assert captured["builder_name"] != DEFAULT_PROVIDER, (
            "the whole point of DECISION D2: this path opts OUT of the product "
            "default, so a run never reaches the local model by accident"
        )

    def test_it_refuses_rather_than_run_fake_when_resolution_names_fake(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])

        def _fake_resolve(role, *args, **kwargs):
            return RoleConfig(role=role, provider="fake", model="m", effort="medium")

        monkeypatch.setattr(self_use_runner, "resolve_role_config", _fake_resolve)

        called = {"run_job": False}

        def _stub_run_job(job_id, **kwargs):
            called["run_job"] = True
            return "SHOULD_NOT_RUN"

        monkeypatch.setattr(self_use_runner, "run_job", _stub_run_job)

        with pytest.raises(SelfUseRunError, match="no usable real provider"):
            run_next_self_use_item(tmp_path / "jobs", str(demo_repo), queue_path=queue_path)

        assert called["run_job"] is False

    def test_explicit_fake_name_bypasses_resolution(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])
        captured: dict = {}

        def _stub_run_job(job_id, **kwargs):
            captured.update(kwargs)
            return "STUB_RESULT"

        monkeypatch.setattr(self_use_runner, "run_job", _stub_run_job)

        run_next_self_use_item(
            tmp_path / "jobs",
            str(demo_repo),
            queue_path=queue_path,
            builder_name="fake",
            reviewer_name="fake",
        )

        assert captured["builder_name"] == "fake"
        assert captured["reviewer_name"] == "fake"

    def test_explicit_provider_object_bypasses_resolution(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])
        captured: dict = {}

        def _stub_run_job(job_id, **kwargs):
            captured.update(kwargs)
            return "STUB_RESULT"

        monkeypatch.setattr(self_use_runner, "run_job", _stub_run_job)

        run_next_self_use_item(
            tmp_path / "jobs",
            str(demo_repo),
            queue_path=queue_path,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
        )

        assert "builder_name" not in captured
        assert "reviewer_name" not in captured
        assert isinstance(captured["builder_provider"], FakeProvider)

    def test_an_unflagged_run_records_the_role_configs_models(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        """R-0890: the job's execution record names the role config's builder and
        reviewer model, not an empty model with source ``default``. The provider
        the resolved name would build is swapped for a fake, so nothing leaves
        the process; the model it was asked for is recorded too."""
        from packages.orchestration import pingpong_loop

        asked: dict = {}

        def _fake_create(name, *, role, model="", **_kw):
            asked[role] = (name, model)
            return _pass_provider()

        monkeypatch.setattr(pingpong_loop, "_create_provider_with_cwd", _fake_create)
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])

        _entry, _path, result = run_next_self_use_item(
            tmp_path / "jobs", str(demo_repo), queue_path=queue_path, repair_rounds=0
        )

        # Both sides come from the ONE self_use role (amend0920-selfuse-real D2),
        # so the expectation is read from that role rather than from two.
        builder_cfg = reviewer_cfg = self_use_runner.resolve_self_use_role_config()
        assert builder_cfg.model and reviewer_cfg.model
        ec = result.execution_config
        assert ec.builder_model == builder_cfg.model
        assert ec.reviewer_model == reviewer_cfg.model
        assert ec.builder_model_source != "default"
        assert ec.reviewer_model_source != "default"
        assert ec.builder_effort == builder_cfg.effort
        assert ec.reviewer_effort == reviewer_cfg.effort
        assert asked["builder"] == (builder_cfg.provider, builder_cfg.model)
        assert asked["reviewer"] == (reviewer_cfg.provider, reviewer_cfg.model)


class TestGenerateThenRunEndToEnd:
    """The Acceptance criterion in ``docs/roadmap/features/T5_F258.md``: one full
    generate → plan → run cycle, proved end-to-end by a test fixture."""

    def test_a_generated_item_plans_and_runs(self, tmp_path, isolate_data_root, demo_repo):
        from packages.orchestration.self_use_generator import generate_and_append_if_empty

        queue_path = _write_queue(tmp_path, [])
        ledger_path = tmp_path / "live_review.md"
        ledger_path.write_text(
            # The FIX: sentence is what makes the finding eligible at all
            # (amend0920-selfuse-real D2); without it Tier 1 offers nothing and
            # the end-to-end cycle this test exists for never starts.
            "- R-0001 — Low, A TEST FINDING FOR THE FIXTURE. FIX: fix the thing "
            "described here.\n",
            encoding="utf-8",
        )
        # The standing order (DECISION F279 D7) is pointed at a missing file: this test is the
        # ledger tier's generate-to-run cycle, and the order tier would answer first.
        generated = generate_and_append_if_empty(queue_path=queue_path, ledger_path=ledger_path,
                                                 order_path=tmp_path / "no-order.md")
        assert generated is not None
        assert generated.provenance.startswith("generated (self-use-generator tier 1")

        entry, job_file_path, result = run_next_self_use_item(
            tmp_path / "jobs",
            str(demo_repo),
            queue_path=queue_path,
            builder_provider=_pass_provider(),
            reviewer_provider=_pass_provider(),
            repair_rounds=0,
        )
        assert entry.id == generated.id
        assert job_file_path.exists()
        assert result.state == JOB_COMPLETED


# ---------------------------------------------------------------------------
# amend0920-selfuse-real Part B.2 — the `self_use` role and this path's budget
# ---------------------------------------------------------------------------


class TestTheSelfUseRoleAndItsBudget:
    """DECISION amend0920-selfuse-real D2.

    SU-019 to SU-023 each ran on the local model and landed no repair. The run
    now resolves the configured frontier provider, with a budget written for a
    run that has to finish: at most 8 provider calls and 1.00 USD per closure.
    """

    def _captured_run_kwargs(self, tmp_path, demo_repo, monkeypatch, **kwargs):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])
        captured: dict = {}

        def _stub_run_job(job_id, **run_kwargs):
            captured.update(run_kwargs)
            return "STUB_RESULT"

        monkeypatch.setattr(self_use_runner, "run_job", _stub_run_job)
        run_next_self_use_item(
            tmp_path / "jobs", str(demo_repo), queue_path=queue_path, **kwargs
        )
        return captured

    def test_the_run_kwargs_carry_the_claude_cli_and_the_sonnet_model(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        from packages.orchestration.model_aliases import resolve_model_alias

        captured = self._captured_run_kwargs(tmp_path, demo_repo, monkeypatch)
        sonnet = resolve_model_alias("claude-workhorse")
        assert captured["builder_name"] == "claude-cli"
        assert captured["reviewer_name"] == "claude-cli"
        assert captured["builder_model"] == sonnet
        assert captured["reviewer_model"] == sonnet

    def test_the_call_cap_is_eight_and_the_cost_bound_one_dollar(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        captured = self._captured_run_kwargs(tmp_path, demo_repo, monkeypatch)
        budgets = captured["budgets"]
        assert budgets["max_provider_calls"] == 8, (
            "six stopped a run mid-loop; DECISION D2 buys the repair round"
        )
        assert budgets["max_cost_usd"] == 1.00

    def test_the_caller_still_overrides_the_budget(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        captured = self._captured_run_kwargs(
            tmp_path, demo_repo, monkeypatch, max_provider_calls=2, max_cost_usd=0.10,
        )
        assert captured["budgets"]["max_provider_calls"] == 2
        assert captured["budgets"]["max_cost_usd"] == 0.10

    def test_both_sides_come_from_ONE_role_and_cannot_drift_apart(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        """The builder and the reviewer of a self-use run are the same pair."""
        captured = self._captured_run_kwargs(tmp_path, demo_repo, monkeypatch)
        assert captured["builder_name"] == captured["reviewer_name"]
        assert captured["builder_model"] == captured["reviewer_model"]
        assert captured["builder_effort"] == captured["reviewer_effort"]

    def test_it_reads_the_self_use_role_and_not_the_builder_or_reviewer_role(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        """The roles asked for are named, so a silent return to the old pair reddens."""
        asked: list[str] = []
        real = self_use_runner.resolve_role_config

        def _spy(role, *args, **kwargs):
            asked.append(role)
            return real(role, *args, **kwargs)

        monkeypatch.setattr(self_use_runner, "resolve_role_config", _spy)
        self._captured_run_kwargs(tmp_path, demo_repo, monkeypatch)

        assert asked == ["self_use"], f"resolved {asked!r}"

    def test_an_injected_provider_object_still_wins(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        captured = self._captured_run_kwargs(
            tmp_path, demo_repo, monkeypatch,
            builder_provider=_pass_provider(), reviewer_provider=_pass_provider(),
        )
        assert "builder_name" not in captured
        assert "reviewer_name" not in captured

    def test_an_explicit_name_still_wins(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        captured = self._captured_run_kwargs(
            tmp_path, demo_repo, monkeypatch,
            builder_name="fake", reviewer_name="fake",
        )
        assert captured["builder_name"] == "fake"
        assert captured["reviewer_name"] == "fake"

    def test_the_operator_can_put_the_track_back_on_the_local_model(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        """`self_use.provider` is the reverse switch DECISION D2 promises."""
        monkeypatch.setenv("REMEDY_SELF_USE_PROVIDER", "ollama")
        monkeypatch.setenv("REMEDY_SELF_USE_MODEL", "muse-glimmer:latest")
        from packages.orchestration.config import reset_config

        reset_config()
        try:
            captured = self._captured_run_kwargs(tmp_path, demo_repo, monkeypatch)
            assert captured["builder_name"] == "ollama"
            assert captured["builder_model"] == "muse-glimmer:latest"
        finally:
            reset_config()


# ---------------------------------------------------------------------------
# amendment amend0923-selfuse-write — R-1043 and R-1044: the run can DELIVER
# ---------------------------------------------------------------------------


class TestTheBuilderCanWriteAndHasTimeToAnswer:
    """R-1043 and R-1044, registered 2026-09-23.

    Three consecutive closures recorded `claude_cli_write_mode: none` with
    source `default`, so their builder had no write tool and no self-use run
    could change a file; and every one of those runs spent three 120-second
    provider timeouts before giving up. The runner therefore asks for a write
    tool and for ten minutes per call, and a caller's own value still wins.
    """

    def _captured(self, tmp_path, demo_repo, monkeypatch, **kwargs):
        queue_path = _write_queue(tmp_path, [dict(_PENDING_ITEM)])
        captured: dict = {}

        def _stub_run_job(job_id, **run_kwargs):
            captured.update(run_kwargs)
            return "STUB_RESULT"

        monkeypatch.setattr(self_use_runner, "run_job", _stub_run_job)
        run_next_self_use_item(
            tmp_path / "jobs", str(demo_repo), queue_path=queue_path, **kwargs
        )
        return captured

    def test_an_unflagged_run_gives_the_builder_a_write_tool(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        captured = self._captured(tmp_path, demo_repo, monkeypatch)
        assert captured["claude_cli_write_mode"] == "allowed-tools", (
            "R-1043: a builder with no write tool returns an empty diff by "
            "construction, which is the whole purpose of the self-use track"
        )

    def test_the_caller_still_chooses_the_write_mode(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        captured = self._captured(
            tmp_path, demo_repo, monkeypatch, claude_cli_write_mode="none"
        )
        assert captured["claude_cli_write_mode"] == "none"

    def test_an_unflagged_run_waits_ten_minutes_for_a_call(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        captured = self._captured(tmp_path, demo_repo, monkeypatch)
        assert captured["timeout_sec"] == 600, (
            "R-1044: three closures burned 3 x 120 s of timeout and delivered "
            "nothing; the self-use path waits long enough for one real answer"
        )

    def test_the_caller_still_chooses_the_timeout(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        captured = self._captured(tmp_path, demo_repo, monkeypatch, timeout_sec=45)
        assert captured["timeout_sec"] == 45


_FIVE_TASK_MARKDOWN = (
    "# Job: A standing order\n\n"
    "Some prose the planner ignores.\n\n"
    "## Task 1\nOne.\n\nAcceptance:\n- done\n\n"
    "## Task 2\nTwo.\n\nAcceptance:\n- done\n\n"
    "## Task 3\nThree.\n\nAcceptance:\n- done\n\n"
    "## Task 4\nFour.\n\nAcceptance:\n- done\n\n"
    "## Task 5\nFive.\n\nAcceptance:\n- done\n"
)

_BUDGET_LINE = (
    "Budget: max_tasks=5, max_provider_calls=40, max_cost_usd=10.00, timeout_sec=900"
)

_FIVE_TASK_MARKDOWN_WITH_BUDGET = _FIVE_TASK_MARKDOWN.replace(
    "Some prose the planner ignores.\n",
    "Some prose the planner ignores.\n\n" + _BUDGET_LINE + "\n",
)


def _order_item(markdown: str, item_id: str = "SU-099") -> dict:
    return {
        "id": item_id,
        "title": "A standing order",
        "why": "Because an order tier hands the runner more than one task.",
        "job_markdown": markdown,
        "consumed_by": "",
        "provenance": "generated (fixture, order tier)",
    }


class TestAnOrderFileDeclaresItsOwnBudget:
    """R-1044, registered 2026-09-23.

    `.agent/selfuse_f279/result_state.txt` records a five-task order stopped
    at `budget_exhausted:max_cost_usd` with all five tasks still pending: the
    runner's one-task, eight-call, one-dollar bound was written for a
    single-finding repair item and cannot fit a standing order. An order file
    may now declare what it needs, and a run that cannot fit the order it was
    given refuses before it spends anything.
    """

    def _run(self, tmp_path, demo_repo, monkeypatch, markdown, **kwargs):
        queue_path = _write_queue(tmp_path, [_order_item(markdown)])
        captured: dict = {}
        called = {"run_job": False}

        def _stub_run_job(job_id, **run_kwargs):
            called["run_job"] = True
            captured.update(run_kwargs)
            return "STUB_RESULT"

        monkeypatch.setattr(self_use_runner, "run_job", _stub_run_job)
        try:
            run_next_self_use_item(
                tmp_path / "jobs", str(demo_repo), queue_path=queue_path, **kwargs
            )
        finally:
            self._called = called
        return captured

    def test_a_five_task_order_without_a_budget_line_refuses_before_spending(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        with pytest.raises(SelfUseRunError, match="has 5 tasks but this run may execute at most 1"):
            self._run(tmp_path, demo_repo, monkeypatch, _FIVE_TASK_MARKDOWN)
        assert self._called["run_job"] is False, (
            "R-1044: the whole point is that nothing is paid for before the refusal"
        )

    def test_the_declared_budget_is_what_the_run_is_given(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        captured = self._run(
            tmp_path, demo_repo, monkeypatch, _FIVE_TASK_MARKDOWN_WITH_BUDGET
        )
        assert captured["max_tasks"] == 5
        assert captured["budgets"]["max_provider_calls"] == 40
        assert captured["budgets"]["max_cost_usd"] == 10.00
        assert captured["timeout_sec"] == 900

    def test_an_explicit_argument_beats_the_declared_budget(
        self, tmp_path, isolate_data_root, demo_repo, monkeypatch
    ):
        with pytest.raises(SelfUseRunError, match="has 5 tasks but this run may execute at most 2"):
            self._run(
                tmp_path, demo_repo, monkeypatch,
                _FIVE_TASK_MARKDOWN_WITH_BUDGET, max_tasks=2,
            )
        assert self._called["run_job"] is False

    def test_the_planner_never_sees_the_budget_line(self):
        """`parse_job_file` ignores everything before the first task heading."""
        from packages.orchestration.pingpong_job import parse_job_file

        plan = parse_job_file(_FIVE_TASK_MARKDOWN_WITH_BUDGET, ".")
        bodies = "\n".join(t.body for t in plan.tasks)
        assert "Budget:" not in bodies
        assert len(plan.tasks) == 5


class TestParseOrderBudget:
    """The declaration is read from the order file, or refused by name."""

    def test_it_reads_every_key_in_any_order_with_loose_whitespace(self):
        declared = self_use_runner.parse_order_budget(
            "# Job: x\n\n"
            "Budget:   timeout_sec = 900 ,max_cost_usd=10.00,  max_tasks=5 , "
            "max_provider_calls=40\n\n## Task 1\nBody.\n"
        )
        assert declared == {
            "max_tasks": 5,
            "max_provider_calls": 40,
            "max_cost_usd": 10.00,
            "timeout_sec": 900,
        }

    def test_keys_are_optional(self):
        assert self_use_runner.parse_order_budget(
            "Budget: max_tasks=3\n\n## Task 1\nBody.\n"
        ) == {"max_tasks": 3}

    def test_no_budget_line_is_an_empty_declaration_not_an_error(self):
        assert self_use_runner.parse_order_budget(_FIVE_TASK_MARKDOWN) == {}

    def test_a_budget_line_after_the_first_task_heading_is_not_read(self):
        assert self_use_runner.parse_order_budget(
            "## Task 1\nBody.\n\nBudget: max_tasks=5\n"
        ) == {}

    @pytest.mark.parametrize("line", [
        "Budget:",
        "Budget: max_tasks",
        "Budget: max_tasks=",
        "Budget: max_tasks=many",
        "Budget: max_widgets=5",
        "Budget: max_tasks=5, max_tasks=6",
    ])
    def test_a_malformed_line_refuses_and_names_the_line(self, line):
        with pytest.raises(SelfUseRunError) as excinfo:
            self_use_runner.parse_order_budget(line + "\n\n## Task 1\nBody.\n")
        assert line in str(excinfo.value), "the refusal must quote the line it read"
