"""Operator amendment amend1014-do-golden-path-now D4 — the progress lines of a human-facing `remedy do`.

An injected sink and clock drive every case, so no test sleeps for a real heartbeat interval.
"""
from __future__ import annotations

import pytest

INCIDENT_ORDER = "Add one concise paragraph to README.md. Change no other files."

class _Clock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now


def _progress(lines, clock):
    from packages.orchestration.do_progress import DoProgress

    # A poll of an hour keeps the heartbeat thread idle: the test drives `tick` itself.
    return DoProgress(write=lines.append, clock=clock, interval=10.0, poll=3600.0)


def test_a_step_says_it_started_before_its_body_runs_and_how_long_it_took():
    lines, clock = [], _Clock()
    seen_in_body = []
    with _progress(lines, clock).step("plan", "bounded lane") as end:
        seen_in_body.extend(lines)
        clock.now += 0.4
        end("done", "")
    assert seen_in_body == ["[remedy] plan started — bounded lane"]
    assert lines[-1] == "[remedy] plan done — 0.4s"


def test_a_blocked_step_beats_every_ten_seconds_and_not_before():
    lines, clock = [], _Clock()
    progress = _progress(lines, clock)
    with progress.step("run", "builder ollama, reviewer ollama") as end:
        clock.now += 9.0
        assert progress.tick() is False
        clock.now += 1.5
        assert progress.tick() is True
        clock.now += 4.0
        assert progress.tick() is False
        clock.now += 20.0
        assert progress.tick() is True
        end("done", "")
    beats = [line for line in lines if "elapsed" in line]
    assert beats == ["[remedy] run: builder ollama, reviewer ollama — 10s elapsed",
                     "[remedy] run: builder ollama, reviewer ollama — 34s elapsed"]


def test_a_failed_step_prints_why_and_an_exception_ends_the_step_as_failed():
    lines, clock = [], _Clock()
    progress = _progress(lines, clock)
    with progress.step("run", "x") as end:
        end("failed", "job abc ended blocked: no_file_changed")
    assert lines[-1].endswith("run failed — 0.0s: job abc ended blocked: no_file_changed")
    with pytest.raises(RuntimeError), progress.step("shape", "y"):
        raise RuntimeError("boom")
    assert "shape failed" in lines[-1]


def test_the_default_sink_writes_to_stderr_and_flushes_each_line(monkeypatch):
    from packages.orchestration import do_progress

    class Stream:
        def __init__(self):
            self.written, self.flushes = [], 0

        def write(self, text):
            self.written.append(text)

        def flush(self):
            self.flushes += 1

    stream = Stream()
    monkeypatch.setattr(do_progress.sys, "stderr", stream)
    do_progress.DoProgress().line("study started")
    assert "".join(stream.written) == "[remedy] study started\n"
    assert stream.flushes >= 1


def test_the_walker_announces_each_step_before_calling_it_and_names_the_providers():
    from packages.orchestration.do_context import DO_STEP_DONE, DoContext
    from packages.orchestration.do_sequence import DO_SEQUENCE, walk_do_sequence

    lines, clock = [], _Clock()
    ctx = DoContext(order=INCIDENT_ORDER, builder_provider="fake", reviewer_provider="fake",
                    no_llm=True)
    ctx.progress = _progress(lines, clock)
    ctx.repo_root = ""
    at_call = {}

    def step_for(name):
        def step(context):
            at_call[name] = list(lines)
            clock.now += 1.0
            return DO_STEP_DONE, f"{name} ok"
        return step

    walk_do_sequence(ctx, {name: step_for(name) for name in DO_SEQUENCE})

    for name in DO_SEQUENCE:
        assert any(line.startswith(f"[remedy] {name} started") for line in at_call[name]), name
        assert not any(line.startswith(f"[remedy] {name} done") for line in at_call[name]), name
    started = [line for line in lines if " started — " in line]
    assert [line.split()[1] for line in started] == list(DO_SEQUENCE)
    assert any("builder fake" in line and "reviewer fake" in line
               for line in started if line.startswith("[remedy] run"))
