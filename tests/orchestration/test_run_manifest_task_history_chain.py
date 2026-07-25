"""F1 (round 15) — a task's history is MONOTONIC across the episode chain.

Round 14 froze a run's ledger, so a later episode could no longer rewrite work it admitted to. It
could still DENY the work ever happened. Reproduced against the full writer:

    ep1:  T001  expectation=executed  status=applied_to_job_workspace  run=rT001
          terminal ledger + call artifact present
    ep2:  T001  expectation=skipped   run=""   no ledger   no calls
          prior_episode_ids=[ep1]

    validate_run_manifest(ep1) = success      write ep1 = success
    validate_run_manifest(ep2) = success      write ep2 = success
    validate_ledger_chain      = success      loader/tree = success

The finality rule never fired, because there was no second ledger to compare. The OMISSION was the
erasure.

The terminal set is the committed contract's, not an invention. F011: "A task that already reached
`applied_to_job_workspace` is durable and is **never** rolled back. Nothing is converted to
`skipped`." `run_job` proves it — the resume loop `continue`s past applied/passed/skipped, and the
stop path refuses to roll those three back. A task stopped BEFORE durable completion returns to
`pending` and legitimately starts a new run; binding that would break F011's resume.
"""
from __future__ import annotations

import dataclasses

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    DISPATCH_NEVER,
    DISPATCH_PRIOR_EPISODE,
    DISPATCH_THIS_EPISODE,
    EXPECT_DISPATCHED_NO_CALLS,
    EXPECT_EXECUTED,
    EXPECT_FAILED_PRE_DISPATCH,
    EXPECT_NOT_DISPATCHED,
    EXPECT_PRIOR_EPISODE,
    EXPECT_SKIPPED,
    TERMINAL_TASK_STATES,
    CallExpectationV1,
    ManifestError,
    TaskCallExpectationV1,
    _bind_artifact_refs,
    _validate_episode_graph,
    validate_task_lifecycle_chain,
    write_run_manifest,
)


@pytest.fixture
def ep1():
    """Episode 1 executed T001 to `applied_to_job_workspace` with a terminal ledger."""
    return _bind_artifact_refs(T._mk(episode_id="ep1", calls=(T._call(seq=1),)))


def _ep2(ep1, *, exp, run="", ref="", seal="", status="skipped",
         dispatch=DISPATCH_NEVER, ledgers=()):
    m = _bind_artifact_refs(T._mk(episode_id="ep2", calls=()))
    return dataclasses.replace(
        m, prior_episode_ids=("ep1",), previous_episode_id="ep1", episode_ordinal=2,
        call_ledgers=ledgers, created_at="2026-07-15T00:02:00+00:00",
        call_expectation=CallExpectationV1(tasks=(TaskCallExpectationV1(
            task_id="T001", expectation=exp, run_id=run, ledger_ref=ref,
            finalized_calls_sha256=seal, task_status_at_finalization=status,
            dispatch_state=dispatch),)))


def _faithful(ep1):
    """What production actually records for a completed task in a later episode."""
    lg = ep1.call_ledgers[0]
    return _ep2(ep1, exp=EXPECT_PRIOR_EPISODE, run=lg.run_id, ref=lg.ref(), seal=lg.sha256(),
                status="applied_to_job_workspace", dispatch=DISPATCH_PRIOR_EPISODE,
                ledgers=(lg,))


def _probs(ep1, ep2):
    return validate_task_lifecycle_chain([ep1, ep2])


# --------------------------------------------------------------------------- the reproduction


class TestALaterEpisodeCannotEraseAnEarlierTask:
    def test_the_reproduced_case(self, ep1):
        """executed/applied -> skipped, with the ledger simply omitted."""
        probs = _probs(ep1, _ep2(ep1, exp=EXPECT_SKIPPED))
        assert probs, "a later episode erased an earlier completed task"
        assert any("cannot un-happen earlier work" in p for p in probs), probs

    def test_it_cannot_become_not_dispatched(self, ep1):
        assert _probs(ep1, _ep2(ep1, exp=EXPECT_NOT_DISPATCHED, status="pending"))

    def test_it_cannot_become_failed_pre_dispatch(self, ep1):
        assert _probs(ep1, _ep2(ep1, exp=EXPECT_FAILED_PRE_DISPATCH, status="failed"))

    def test_it_cannot_become_runless(self, ep1):
        lg = ep1.call_ledgers[0]
        probs = _probs(ep1, _ep2(ep1, exp=EXPECT_PRIOR_EPISODE, run="", ref=lg.ref(),
                                 seal=lg.sha256(), status="applied_to_job_workspace",
                                 dispatch=DISPATCH_PRIOR_EPISODE, ledgers=(lg,)))
        assert any("names run ''" in p for p in probs), probs

    def test_it_cannot_name_a_different_run(self, ep1):
        lg = ep1.call_ledgers[0]
        assert _probs(ep1, _ep2(ep1, exp=EXPECT_PRIOR_EPISODE, run="r-other", ref=lg.ref(),
                                seal=lg.sha256(), status="applied_to_job_workspace",
                                dispatch=DISPATCH_PRIOR_EPISODE, ledgers=(lg,)))

    def test_it_cannot_name_a_different_ledger(self, ep1):
        lg = ep1.call_ledgers[0]
        probs = _probs(ep1, _ep2(ep1, exp=EXPECT_PRIOR_EPISODE, run=lg.run_id,
                                 ref="call_ledgers/" + "a" * 64 + ".json", seal=lg.sha256(),
                                 status="applied_to_job_workspace",
                                 dispatch=DISPATCH_PRIOR_EPISODE, ledgers=(lg,)))
        assert any("names ledger" in p for p in probs), probs

    def test_it_cannot_reseal_the_ledger_hash(self, ep1):
        lg = ep1.call_ledgers[0]
        probs = _probs(ep1, _ep2(ep1, exp=EXPECT_PRIOR_EPISODE, run=lg.run_id, ref=lg.ref(),
                                 seal="f" * 64, status="applied_to_job_workspace",
                                 dispatch=DISPATCH_PRIOR_EPISODE, ledgers=(lg,)))
        assert any("frozen" in p for p in probs), probs


class TestTheFaithfulRepetitionPasses:
    def test_exact_prior_episode_repetition_passes(self, ep1):
        assert _probs(ep1, _faithful(ep1)) == []

    def test_many_later_episodes_all_preserve_the_prior_task(self, ep1):
        ep2 = _faithful(ep1)
        ep3 = dataclasses.replace(ep2, episode_id="ep3", episode_ordinal=3,
                                  previous_episode_id="ep2",
                                  prior_episode_ids=("ep1", "ep2"),
                                  created_at="2026-07-15T00:03:00+00:00")
        ep4 = dataclasses.replace(ep3, episode_id="ep4", episode_ordinal=4,
                                  previous_episode_id="ep3",
                                  prior_episode_ids=("ep1", "ep2", "ep3"),
                                  created_at="2026-07-15T00:04:00+00:00")
        assert validate_task_lifecycle_chain([ep1, ep2, ep3, ep4]) == []

    def test_a_single_episode_chain_is_fine(self, ep1):
        assert validate_task_lifecycle_chain([ep1]) == []


# --------------------------------------------------------------------------- skipped


class TestASkippedTaskStaysSkipped:
    @pytest.fixture
    def skipped_ep1(self):
        m = _bind_artifact_refs(T._mk(episode_id="ep1", calls=()))
        return dataclasses.replace(m, call_ledgers=(), call_expectation=CallExpectationV1(
            tasks=(TaskCallExpectationV1(
                task_id="T001", expectation=EXPECT_SKIPPED,
                task_status_at_finalization="skipped", dispatch_state=DISPATCH_NEVER),)))

    def test_a_skipped_task_repeated_as_skipped_passes(self, skipped_ep1):
        assert _probs(skipped_ep1, _ep2(skipped_ep1, exp=EXPECT_SKIPPED)) == []

    def test_a_skipped_task_cannot_gain_a_run(self, skipped_ep1):
        """`_block_job` skips the remaining pending tasks; the resume loop never revisits them."""
        probs = _probs(skipped_ep1, _ep2(skipped_ep1, exp=EXPECT_EXECUTED, run="r-new",
                                         status="applied_to_job_workspace",
                                         dispatch=DISPATCH_THIS_EPISODE))
        assert any("never reactivates it" in p for p in probs), probs

    def test_a_skipped_task_cannot_become_executed_or_dispatched(self, skipped_ep1):
        for exp in (EXPECT_EXECUTED, EXPECT_DISPATCHED_NO_CALLS, EXPECT_PRIOR_EPISODE):
            assert _probs(skipped_ep1, _ep2(skipped_ep1, exp=exp, run="r-x",
                                            status="skipped")), exp


# --------------------------------------------------------------------------- non-terminal


class TestANonTerminalTaskMayResumeUnderANewRun:
    def test_a_stopped_pending_task_may_start_a_new_run(self):
        """F011's mid-flight stop: the call in flight finished, the task waits at `pending`, and
        the resume starts a NEW run. Refusing this would break the product."""
        ep1 = _bind_artifact_refs(T._mk(episode_id="ep1", status="stopped",
                                        calls=(T._call(run="r-ep1"),)))
        ep1 = dataclasses.replace(ep1, stop_request_id="stop-1")
        assert ep1.call_expectation.tasks[0].task_status_at_finalization == "pending"
        ep2 = _bind_artifact_refs(T._mk(episode_id="ep2", calls=(T._call(run="r-ep2"),)))
        ep2 = dataclasses.replace(ep2, prior_episode_ids=("ep1",), previous_episode_id="ep1",
                                  episode_ordinal=2)
        assert validate_task_lifecycle_chain([ep1, ep2]) == []

    def test_the_earlier_run_history_is_untouched(self):
        ep1 = _bind_artifact_refs(T._mk(episode_id="ep1", status="stopped",
                                        calls=(T._call(run="r-ep1"),)))
        ep1 = dataclasses.replace(ep1, stop_request_id="stop-1")
        assert ep1.call_ledgers[0].run_id == "r-ep1"
        assert ep1.call_ledgers[0].entries

    def test_the_terminal_set_is_exactly_the_committed_contract(self):
        assert TERMINAL_TASK_STATES == {"applied_to_job_workspace", "passed", "skipped"}
        assert "pending" not in TERMINAL_TASK_STATES      # F011 returns a stopped task here
        assert "failed" not in TERMINAL_TASK_STATES
        assert "blocked" not in TERMINAL_TASK_STATES


# --------------------------------------------------------------------------- identity


def _snapshot_declaring(task_ids, episode_id):
    """An episode snapshot whose EMBEDDED job-input definition declares exactly `task_ids`."""
    from packages.orchestration.pingpong_job import ExecutionConfig, TaskEntry
    from packages.orchestration.run_manifest import build_job_input_definition

    class _J:
        job_id = "j"
        job_title = "demo"
        job_file_sha256 = "f" * 64
        isolation_mode = "worktree"
        execution_config = ExecutionConfig()
        tasks = [TaskEntry(task_id=t, source_heading_number=i + 1, title="t", body="b",
                           acceptance="a") for i, t in enumerate(task_ids)]

    snap = T._snap(job_input=build_job_input_definition(_J()))
    return T._wrap(snap, episode_id=episode_id)


class TestTheTaskListIsImmutable:
    def test_the_rule_compares_the_embedded_definition(self, ep1):
        from packages.orchestration.run_manifest import declared_job_input_task_ids
        assert declared_job_input_task_ids(ep1) == ["T001"]

    def test_a_later_episode_cannot_add_a_task(self, ep1):
        ep2 = dataclasses.replace(_faithful(ep1),
                                  episode_snapshot=_snapshot_declaring(["T001", "T002"], "ep2"))
        probs = validate_task_lifecycle_chain([ep1, ep2])
        assert any("immutable across a job's episodes" in p for p in probs), probs

    def test_a_later_episode_cannot_remove_a_task(self):
        two = _bind_artifact_refs(T._mk(episode_id="ep1", calls=(T._call(seq=1),)))
        two = dataclasses.replace(two, episode_snapshot=_snapshot_declaring(
            ["T001", "T002"], "ep1"))
        one = dataclasses.replace(_faithful(two),
                                  episode_snapshot=_snapshot_declaring(["T001"], "ep2"))
        assert any("immutable" in p for p in validate_task_lifecycle_chain([two, one]))

    def test_a_later_episode_cannot_reorder_the_tasks(self):
        a = _bind_artifact_refs(T._mk(episode_id="ep1", calls=(T._call(seq=1),)))
        a = dataclasses.replace(a, episode_snapshot=_snapshot_declaring(["T001", "T002"], "ep1"))
        b = dataclasses.replace(_faithful(a),
                                episode_snapshot=_snapshot_declaring(["T002", "T001"], "ep2"))
        probs = validate_task_lifecycle_chain([a, b])
        assert any("immutable" in p for p in probs), probs

    def test_the_same_task_list_passes(self, ep1):
        ep2 = dataclasses.replace(_faithful(ep1),
                                  episode_snapshot=_snapshot_declaring(["T001"], "ep2"))
        assert validate_task_lifecycle_chain([ep1, ep2]) == []


# --------------------------------------------------------------------------- the seams


class TestEverySeamEnforcesTheHistory:
    def test_the_canonical_chain_validator_refuses_the_erasure(self, ep1):
        bad = _ep2(ep1, exp=EXPECT_SKIPPED)
        assert _validate_episode_graph({"ep1": ep1, "ep2": bad})
        assert _validate_episode_graph({"ep1": ep1, "ep2": _faithful(ep1)}) == []

    def test_the_writer_refuses_to_publish_the_erasure(self, ep1, tmp_path):
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, ep1, root=tmp_path)
        with pytest.raises(ManifestError):
            write_run_manifest(ev, _ep2(ep1, exp=EXPECT_SKIPPED), root=tmp_path)

    def test_a_faithful_chain_still_publishes_and_reads_back(self, ep1, tmp_path):
        from packages.orchestration.run_manifest import (
            load_latest_manifest_verified,
            validate_index_and_tree,
        )
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, ep1, root=tmp_path)
        write_run_manifest(ev, _faithful(ep1), root=tmp_path)
        assert validate_index_and_tree(ev, job_id="j") == []
        assert load_latest_manifest_verified(ev, job_id="j").episode_id == "ep2"
