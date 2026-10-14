"""F306 T004 — the workspace identity record and its probes, split out of ``run_manifest``.

This module holds: the provider-version probe (``probe_provider_version`` and its
``_run_probe`` helper), the repo-root and sha helpers (``_remedy_repo_root``, ``_is_sha``),
the git-worktree content identity record (``WorktreeIdentity`` and its ``GIT_*`` status
vocabulary), and the read-only git-helper neutralization used while inspecting a worktree
(``_git_helper_env``, ``_helper_neutralizing_args``, the per-reading ``_READING_HELPER_ARGS``
memo), together with the typed failure modes of a verified untracked-file read
(``_UntrackedRace``, ``_UntrackedSymlink``, ``_UntrackedSpecial``, ``_UntrackedMissing``).
``run_manifest.py`` imports the names it uses, and every other consumer imports from here
(operator amendment amend1014-luna-mission-fixes D.2). The
git reads themselves — ``_git_bytes``, ``_submodule_status``, ``worktree_identity`` and
``_read_untracked_verified`` — stay on ``run_manifest``: tests replace them there, and
``_read_untracked_verified`` raises ``run_manifest``'s own ``ManifestError``, which this
module must never import.
"""
from __future__ import annotations

import contextvars
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

UNAVAILABLE = "unavailable"

_VERSION_PROBE_TIMEOUT_S = 5
_VERSION_PROBE_MAX_CHARS = 200


def _run_probe(argv: list[str], cwd: str | None = None) -> str:
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, shell=False,
                              timeout=_VERSION_PROBE_TIMEOUT_S, cwd=cwd)
    except Exception:  # noqa: BLE001 — version probe failure just means version unavailable
        return UNAVAILABLE
    if proc.returncode != 0 or not proc.stdout or not proc.stdout.strip():
        return UNAVAILABLE
    from packages.orchestration.failure_postmortem import safe_text

    return safe_text(proc.stdout.strip())[:_VERSION_PROBE_MAX_CHARS]


def probe_provider_version(provider: str, cwd: str | None = None) -> str:
    import shutil

    name = (provider or "").strip().lower()
    if name in ("", "fake"):
        return UNAVAILABLE
    exe = "claude" if name.startswith("claude") else name
    path = shutil.which(exe)
    if not path:
        return UNAVAILABLE
    return _run_probe([path, "--version"], cwd=cwd)


def _remedy_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _is_sha(v: str) -> bool:
    return len(v) == 40 and all(c in "0123456789abcdef" for c in v)


#: A worktree-identity component either succeeded (bytes), or explicitly did not. It is NEVER
#: mapped to empty bytes: a failed `git diff` that reads as "no diff" would make a dirty tree
#: look clean, which is exactly the fail-open bug F3 exists to close.
GIT_OK = "ok"
GIT_UNAVAILABLE = "unavailable"     # not a git repo / git missing
GIT_INCOMPLETE = "incomplete"       # a component failed (nonzero, timeout, unsupported file)


@dataclass(frozen=True)
class WorktreeIdentity:
    """The strict content identity of a git worktree — Remedy's or the target's.

    ``status`` is ``ok`` only when every component was collected; ``unavailable`` when the
    path is not a usable git repo; ``incomplete`` when a component failed (a git error, a
    timeout, an untracked special file) — never silently clean. The comparison treats
    ``incomplete``/``unavailable`` as a coverage problem, never as equality."""

    status: str
    head: str                       # HEAD commit sha, or "unavailable"
    digest: str                     # content digest (only meaningful when status == ok)
    problems: tuple[str, ...] = ()
    #: F4: True when the tree has staged/unstaged/untracked/submodule changes, False when a
    #: successful collection found none, None when the identity is unavailable/incomplete.
    #: ``problems`` means COLLECTION FAILURE, not dirtiness.
    dirty: bool | None = None

    def to_json(self) -> dict[str, Any]:
        return {"status": self.status, "head": self.head, "digest": self.digest,
                "problems": list(self.problems), "dirty": self.dirty}

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> WorktreeIdentity:
        return cls(status=str(d.get("status", GIT_UNAVAILABLE)),
                   head=str(d.get("head", "")), digest=str(d.get("digest", "")),
                   problems=tuple(d.get("problems") or []), dirty=d.get("dirty"))


#: F7 (round 12): every configured helper git might EXECUTE during a read-only inspection.
#:
#: A "read-only" verification that runs arbitrary repository-configured commands is not read-only:
#: `core.fsmonitor` alone was enough to make `worktree_identity()` execute a script and still
#: report `status=ok, problems=[]`. Reading a repository must never mean running its code.
#:
#: `filter.*.process` is disabled by pointing it at `false` AND clearing `required`, so a
#: required-but-disabled filter cannot turn into a silent success.
_HELPER_NEUTRALIZING_ARGS: tuple[str, ...] = (
    "-c", "core.fsmonitor=false",
    "-c", "core.fsmonitorHookVersion=0",
    "-c", "core.hooksPath=/dev/null",
    "-c", "diff.external=",
    "-c", "core.sshCommand=false",
    "-c", "protocol.ext.allow=never",
    "-c", "uploadpack.packObjectsHook=",
)

#: F7: the config a repository can point at a program, discovered per repo and neutralized.
_HELPER_CONFIG_PATTERN = r"^(filter\..*\.(clean|smudge|process|required)|diff\..*\.(command|textconv)|core\.fsmonitor)$"


def _git_helper_env() -> dict[str, str]:
    """F7: a constrained environment for read-only inspection.

    Global and system git config can point at helpers too, and they are not facts about the
    repository F012 is hashing — so they are taken out of the picture entirely rather than
    trusted to be harmless.
    """
    env = dict(os.environ)
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_SYSTEM"] = os.devnull
    env["GIT_OPTIONAL_LOCKS"] = "0"        # never take a lock for a read
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_ASKPASS"] = ""
    env["GIT_ALLOW_PROTOCOL"] = "none"
    env.pop("GIT_EXTERNAL_DIFF", None)
    env.pop("GIT_SSH_COMMAND", None)
    return env


#: F294: the helper discovery of the ONE `worktree_identity` reading in progress, per directory.
#: A reading runs six git commands back to back; discovering the configured helpers before each
#: of them started six `git config` processes where one answers them all. The memo lives only for
#: that reading and only in its own thread, so a later reading always discovers afresh.
_READING_HELPER_ARGS: contextvars.ContextVar[dict[str, list[str]] | None] = contextvars.ContextVar(
    "remedy_reading_helper_args", default=None)


def _helper_neutralizing_args(cwd: str, env: dict[str, str]) -> list[str]:
    """F7 (round 12): discover this repository's configured helpers and neutralize each one.

    The clean/smudge substitution keeps the identity meaningful: it digests the RAW working-tree
    bytes, and both sides of every comparison are captured the same way, so drift detection is
    unaffected while no configured command ever runs.

    F294: inside one `worktree_identity` reading the answer for a directory is discovered once
    and reused. Only a discovery that ended with git's own answer, exit 0 (helpers listed) or
    exit 1 (nothing configured), is remembered; a discovery that failed is retried by the next
    command.
    """
    memo = _READING_HELPER_ARGS.get()
    if memo is not None and cwd in memo:
        return list(memo[cwd])
    args = list(_HELPER_NEUTRALIZING_ARGS)
    try:
        proc = subprocess.run(
            ["git", "config", "--name-only", "--get-regexp", _HELPER_CONFIG_PATTERN],
            capture_output=True, shell=False, timeout=5, cwd=cwd, env=env)
    except Exception:  # noqa: BLE001 — helper discovery failure falls back to default neutralization
        return args
    if proc.returncode == 0:
        for name in proc.stdout.decode("utf-8", "replace").split():
            name = name.strip()
            if name.endswith((".clean", ".smudge")):
                args += ["-c", f"{name}=cat"]          # a passthrough, never the configured command
            elif name.endswith(".process"):
                args += ["-c", f"{name}=false"]
            elif name.endswith(".required"):
                args += ["-c", f"{name}=false"]        # a disabled filter must not be "required"
            elif name.endswith((".command", ".textconv")):
                args += ["-c", f"{name}="]
            elif name == "core.fsmonitor":
                args += ["-c", "core.fsmonitor=false"]
    if memo is not None and proc.returncode in (0, 1):
        memo[cwd] = list(args)          # nothing configured is git's exit 1
    return args


class _UntrackedRace(Exception):
    pass


class _UntrackedSymlink(Exception):
    pass


class _UntrackedSpecial(Exception):
    pass


class _UntrackedMissing(Exception):
    pass
