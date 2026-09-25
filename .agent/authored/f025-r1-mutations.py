#!/usr/bin/env python3
"""F025 R1 G5 — red-prove tests/orchestration/test_pause_control.py against pause_control.py.

Usage: python3 -B f025-r1-mutations.py <worktree-path>

For each mutation, edits packages/orchestration/pause_control.py INSIDE the worktree
(asserting its FROM text occurs exactly once), purges __pycache__, runs
`python3 -B -m pytest -q -p no:cacheprovider` over tests/orchestration/test_pause_control.py
from the worktree's root, restores the original bytes, and prints one line: label, real exit
code, failed count, failing node ids. An unmutated control run brackets the mutations, first
and last. Ends with "restored byte-identical: True" per file and
"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>".
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TARGET_REL = "packages/orchestration/pause_control.py"
TEST_REL = "tests/orchestration/test_pause_control.py"

M1_FROM = '''        if existing is not None:
            return _parse_pause_signal(jid, existing)'''
M1_TO = '''        if existing is not None:
            return PauseSignal(jid, _sp.new_request_id(),
                               _bounded(reason, _sp.MAX_REASON_CHARS, UNKNOWN_REASON),
                               _bounded(source, _sp.MAX_SOURCE_CHARS, UNKNOWN_SOURCE),
                               _sp.utc_now_iso())'''

M2_FROM = '''    if raw is None:
        return None
    return _parse_pause_signal(jid, raw)'''
M2_TO = '''    if raw is None:
        return None
    return None  # MUTATED'''

M3_FROM = '''    archive_fd = None
    try:
        archive_fd = _open_named_dir(job_fd, PAUSE_ARCHIVE_DIRNAME, create=True)
        assert archive_fd is not None
        name = f"{signal.request_id}.json"'''
M3_TO = '''    archive_fd = None
    try:
        _fs.require_writable_dir(job_fd, error_cls=PauseControlError, noun="pause-control",
                                 label=PAUSE_REQUEST_FILENAME)
        _fs.unlink_at(PAUSE_REQUEST_FILENAME, job_fd, error_cls=PauseControlError,
                      noun="pause request")  # MUTATED: removed before the archive publish
        archive_fd = _open_named_dir(job_fd, PAUSE_ARCHIVE_DIRNAME, create=True)
        assert archive_fd is not None
        name = f"{signal.request_id}.json"'''

M4_FROM = '''        if pending_raw is not None:
            pending_signal = _parse_pause_signal(jid, pending_raw)
            if pending_signal.request_id == signal.request_id:'''
M4_TO = '''        if pending_raw is not None:
            pending_signal = _parse_pause_signal(jid, pending_raw)
            if True:  # MUTATED: id match no longer required'''

M5_FROM = '''PAUSE_ARCHIVE_DIRNAME = "pause_archive"'''
M5_TO = '''PAUSE_ARCHIVE_DIRNAME = "archive"  # MUTATED: collides with the stop's archive/'''

M6_FROM = '''    if outcome not in _VALID_SETTLE_OUTCOMES:
        raise PauseControlError(
            f"unknown pause outcome {outcome!r}: expected one of "
            f"{sorted(_VALID_SETTLE_OUTCOMES)}")'''
M6_TO = '''    pass  # MUTATED: outcome validation removed'''

M7_FROM = '''        if existing is not None:
            return _parse_task_pause(jid, existing)'''
M7_TO = '''        if existing is not None:
            return TaskPause(jid, tid, _sp.new_request_id(),
                             _bounded(reason, _sp.MAX_REASON_CHARS, UNKNOWN_REASON),
                             _bounded(source, _sp.MAX_SOURCE_CHARS, UNKNOWN_SOURCE),
                             _sp.utc_now_iso())'''

M8_FROM = '''        if raw is None:
            return None
        pause = _parse_task_pause(jid, raw)'''
M8_TO = '''        if raw is None:
            raw = _fs.json_bytes(TaskPause(jid, tid, _sp.new_request_id(), UNKNOWN_REASON,
                                           UNKNOWN_SOURCE, _sp.utc_now_iso()).to_json())
        pause = _parse_task_pause(jid, raw)  # MUTATED: fabricated an entry'''

M9_FROM = '''            out.append(_parse_task_pause(jid, raw))'''
M9_TO = '''            try:
                out.append(_parse_task_pause(jid, raw))
            except PauseControlError:
                continue  # MUTATED: dropped instead of raised'''

M10_FROM = '''def _task_pause_filename(task_id: str) -> str:
    """The file is named by a digest of the id, never by the id itself (S4): an id holding
    ``/``, ``..`` or any other path-shaped text can never become — or escape — a path
    component."""
    digest = hashlib.sha256(task_id.encode("utf-8")).hexdigest()[:32]
    return f"{digest}.json"'''
M10_TO = '''def _task_pause_filename(task_id: str) -> str:
    """MUTATED: named by the raw id."""
    return f"{task_id}.json"'''

M11_FROM = '''        if idx_start is not None:
            for pid in order_list[idx_start:]:
                if pid in pending_set:
                    withheld_set.add(pid)'''
M11_TO = '''        if idx_start is not None:
            for pid in order_list[idx_start:idx_start + 1]:  # MUTATED: only the one task
                if pid in pending_set:
                    withheld_set.add(pid)'''

M12_FROM = '''        idx_start = next(
            (i for i, pid in enumerate(order_list) if pid in paused_pending), None)
        if idx_start is not None:'''
M12_TO = '''        idx_start = next(
            (i for i, pid in enumerate(order_list) if pid in paused_pending), None)
        if idx_start is not None:
            idx_start = 0  # MUTATED: also withhold everything before it'''

M13_FROM = '''        while queue:
            current = queue.pop(0)
            for dependent in dependents.get(current, ()):
                if dependent in withheld_set:
                    continue
                if dependent not in pending_set:
                    continue                       # not pending: never withheld, never spreads
                withheld_set.add(dependent)
                queue.append(dependent)'''
M13_TO = '''        while queue:
            current = queue.pop(0)
            for dependent in dependents.get(current, ()):
                if dependent in withheld_set:
                    continue
                if dependent not in pending_set:
                    continue
                withheld_set.add(dependent)
                # MUTATED: no queue.append -- propagation stops after one hop'''

M14_FROM = '''        withheld_set = set(paused_pending)
        queue: list[str] = list(paused_pending)'''
M14_TO = '''        withheld_set = set(paused_set)  # MUTATED: seeded from ALL paused ids
        queue: list[str] = list(paused_set)'''

M15_FROM = '''def _bounded(text: Any, limit: int, fallback: str) -> str:
    cleaned = safe_text(str(text or "")).replace("\\n", " ").replace("\\r", " ").strip()
    if not cleaned:
        return fallback
    return cleaned[:limit]'''
M15_TO = '''def _bounded(text: Any, limit: int, fallback: str) -> str:
    cleaned = safe_text(str(text or "")).replace("\\n", " ").replace("\\r", " ").strip()
    if not cleaned:
        return fallback
    return cleaned  # MUTATED: no truncation'''

MUTATIONS = [
    ("m1", "request_pause overwrites a pending request with a new id", M1_FROM, M1_TO),
    ("m2", "pause_requested always returns None", M2_FROM, M2_TO),
    ("m3", "settle_pause removes the pending file BEFORE publishing the archive",
     M3_FROM, M3_TO),
    ("m4", "settle_pause removes a pending file whose request id differs", M4_FROM, M4_TO),
    ("m5", "the pause archive is written under the stop's archive/ directory", M5_FROM, M5_TO),
    ("m6", "settle_pause accepts an unknown outcome", M6_FROM, M6_TO),
    ("m7", "request_task_pause replaces an existing entry with a new request id",
     M7_FROM, M7_TO),
    ("m8", "release_task_pause of an unpaused task writes an archive entry", M8_FROM, M8_TO),
    ("m9", "paused_tasks skips an entry it cannot parse", M9_FROM, M9_TO),
    ("m10", "the task file is named by the raw task id instead of its digest",
     M10_FROM, M10_TO),
    ("m11", "the linear mask withholds only the paused task, not the tasks after it",
     M11_FROM, M11_TO),
    ("m12", "the linear mask also withholds the pending tasks BEFORE the paused one",
     M12_FROM, M12_TO),
    ("m13", "the graph mask withholds direct dependents only, not transitive ones",
     M13_FROM, M13_TO),
    ("m14", "a paused task that is not pending still withholds its dependents",
     M14_FROM, M14_TO),
    ("m15", "the reason is stored unbounded", M15_FROM, M15_TO),
]


def purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        for f in sorted(cache_dir.rglob("*"), reverse=True):
            f.unlink() if f.is_file() else f.rmdir()
        cache_dir.rmdir()


def run_pytest(worktree: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "--tb=no", "-rf", TEST_REL],
        cwd=str(worktree), capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def parse_summary(output: str) -> tuple[int, list[str]]:
    ids = [line[len("FAILED "):].split(" - ")[0].strip()
          for line in output.splitlines() if line.startswith("FAILED ")]
    return len(ids), ids


def report(label: str, desc: str, code: int, failed: int, ids: list[str]) -> str:
    shown = ", ".join(ids) if ids else "(none)"
    return f"{label}: {desc} -- exit={code} failed={failed} failing_node_ids=[{shown}]"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f025-r1-mutations.py <worktree-path>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()
    target = worktree / TARGET_REL
    original = target.read_bytes()
    all_caught = True
    restores_ok = True

    purge_pycache(worktree)
    code, out = run_pytest(worktree)
    failed, ids = parse_summary(out)
    print(report("control (before)", "unmutated control run", code, failed, ids))
    if code != 0 or failed != 0:
        all_caught = False

    for label, desc, from_text, to_text in MUTATIONS:
        text = original.decode("utf-8")
        occurrences = text.count(from_text)
        if occurrences != 1:
            print(f"{label}: {desc} -- ABORT: FROM occurs {occurrences} times, expected 1")
            all_caught = False
            continue
        target.write_text(text.replace(from_text, to_text, 1), encoding="utf-8")

        purge_pycache(worktree)
        code, out = run_pytest(worktree)
        failed, ids = parse_summary(out)
        print(report(label, desc, code, failed, ids))
        if not (code != 0 and failed >= 1):
            all_caught = False

        target.write_bytes(original)
        restored = target.read_bytes() == original
        print(f"{label}: restored byte-identical: {restored}")
        restores_ok = restores_ok and restored

    purge_pycache(worktree)
    code, out = run_pytest(worktree)
    failed, ids = parse_summary(out)
    print(report("control (after)", "unmutated control run", code, failed, ids))
    if code != 0 or failed != 0:
        all_caught = False

    final_restored = target.read_bytes() == original
    print(f"{TARGET_REL}: restored byte-identical: {final_restored}")
    restores_ok = restores_ok and final_restored

    overall = all_caught and restores_ok
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {overall}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
