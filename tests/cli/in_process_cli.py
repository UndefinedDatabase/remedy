"""Remedy's command line run in the test process, answered as `subprocess.run` answers a child.

DECISION F294 D4, shared by DECISION F294 D5. A test whose subject is not the child process can
run its setup commands here: a child process starts a fresh interpreter and reads Remedy's own
checkout again, work the test process has already done. The child's surroundings are kept: its
environment, its working directory, an empty stdin, its captured output, and its exit code,
including 1 with the traceback on stderr for an exception nothing caught.
"""
from __future__ import annotations

import contextlib
import io
import os
import subprocess
import sys
import traceback

#: The child process this stands in for, as the answer's `args` names it.
CLI_CHILD_ARGV = [sys.executable, "-m", "apps.cli.grouped"]


def run_cli_in_process(args, cwd, env) -> subprocess.CompletedProcess:
    """Run `remedy <args>` here, in ``cwd`` with ``env`` as the whole environment."""
    from apps.cli.grouped import main

    out, err = io.StringIO(), io.StringIO()
    saved_env, saved_cwd, saved_stdin = dict(os.environ), os.getcwd(), sys.stdin
    os.environ.clear()
    os.environ.update(env)
    os.chdir(str(cwd))
    sys.stdin = io.StringIO("")
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                main(list(args))
                code = 0
            except SystemExit as exc:
                code = exc.code
            except Exception:  # noqa: BLE001 — a child process prints the traceback and exits 1
                traceback.print_exc()
                code = 1
    finally:
        sys.stdin = saved_stdin
        os.chdir(saved_cwd)
        os.environ.clear()
        os.environ.update(saved_env)
    if code is None:
        code = 0
    elif not isinstance(code, int):
        err.write(f"{code}\n")
        code = 1
    return subprocess.CompletedProcess([*CLI_CHILD_ARGV, *args], code, out.getvalue(),
                                       err.getvalue())
