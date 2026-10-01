"""Guard for finding R-0803: the suite never resolves the operator's data root.

``tests/conftest.py::_isolated_data_root`` points ``REMEDY_DATA_DIR`` at a fresh
temporary directory for every test, and ``pytest_sessionfinish`` there fails the
run when the configured data root changed. These tests pin the per-test half:
without the fixture, ``resolve_data_root()`` falls through to the configured
root and every assertion below goes red.
"""

import os
import subprocess
import sys
from pathlib import Path

from packages.orchestration import data_paths

REPO_ROOT = Path(__file__).resolve().parents[1]
REPO_DEFAULT_ROOT = Path(data_paths.__file__).resolve().parents[2] / ".data"


def test_the_resolved_root_is_under_the_pytest_temp_base(tmp_path_factory):
    root = data_paths.resolve_data_root().resolve()
    assert root != REPO_DEFAULT_ROOT
    assert root.is_relative_to(tmp_path_factory.getbasetemp().resolve())


def test_each_test_gets_a_fresh_empty_root():
    root = data_paths.resolve_data_root()
    assert root.is_dir()
    assert list(root.iterdir()) == []


def test_every_root_is_a_new_directory_under_one_parent(_data_root_allocator):
    """DECISION F294 D2: the roots share one parent and no two are the same directory."""
    root = data_paths.resolve_data_root().resolve()
    first, second = (_data_root_allocator().resolve() for _ in range(2))
    assert len({root, first, second}) == 3
    assert root.parent == first.parent == second.parent
    assert [p for p in (root, first, second) if list(p.iterdir())] == []


def test_a_root_is_made_without_numbering_the_base_directory(_data_root_allocator, monkeypatch):
    """DECISION F294 D2: after its one parent, the allocator lists no directory and starts no
    process; ``mktemp``, and the pytest helper under it, list the whole base temporary directory to
    find the next number (R-1127, DECISIONs F294 D8 and D9)."""
    def refused(*_args, **_kwargs):
        raise AssertionError("allocating a root listed a directory or started a process")

    routes = ((os, "scandir"), (os, "listdir"), (Path, "iterdir"), (Path, "glob"), (Path, "rglob"),
              (subprocess, "Popen"), (os, "system"), (os, "fork"), (os, "posix_spawn"),
              (os, "posix_spawnp"))
    with monkeypatch.context() as patched:
        for owner, name in routes:
            patched.setattr(owner, name, refused)
        roots = [_data_root_allocator() for _ in range(2)]
    assert roots[0] != roots[1]
    assert [r for r in roots if not r.is_dir()] == []


#: The audit events seen while ``_AUDIT["armed"]`` holds; the hook is installed once per test
#: process, because an audit hook can never be removed, and it records nothing while disarmed.
_AUDIT: dict = {"armed": False, "events": [], "installed": False}


def _record_audit_event(event, _args):
    if _AUDIT["armed"]:
        _AUDIT["events"].append(event)


def test_allocating_a_root_raises_no_audit_event_but_one_mkdir(_data_root_allocator):
    """R-1127: the interpreter raises an audit event inside every directory listing, started
    process and foreign-library call, so a listing function the allocator bound to a name of its
    own before this test ran is seen here although the test above cannot replace it."""
    if not _AUDIT["installed"]:
        sys.addaudithook(_record_audit_event)
        _AUDIT["installed"] = True
    _AUDIT["events"] = []
    _AUDIT["armed"] = True
    try:
        roots = [_data_root_allocator() for _ in range(2)]
    finally:
        _AUDIT["armed"] = False
    assert _AUDIT["events"] == ["os.mkdir", "os.mkdir"]
    assert roots[0] != roots[1]


def test_a_cli_subprocess_inherits_the_isolated_root():
    code = "from packages.orchestration.data_paths import resolve_data_root; print(resolve_data_root())"
    out = subprocess.run(
        [sys.executable, "-c", code], cwd=REPO_ROOT, env=os.environ.copy(),
        capture_output=True, text=True, timeout=60, check=True,
    ).stdout.strip()
    assert Path(out) == data_paths.resolve_data_root()
    assert Path(out).resolve() != REPO_DEFAULT_ROOT
