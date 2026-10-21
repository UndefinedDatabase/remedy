"""F199 — the local crash report.

DECISION F199 D1: when a command ends on an error nobody expected, or a thread of
the serve supervisor dies on one, Remedy writes one Markdown report under the
data root (`<data root>/crash/`). A report is written only on this machine and
Remedy never sends it anywhere. Writing one never raises, so a crash report
cannot hide the error it records: any failure to write answers None.
"""

from __future__ import annotations

import json
import os
import threading
import traceback
from collections.abc import Callable
from datetime import datetime, timezone
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, distribution
from pathlib import Path

from packages.orchestration.data_paths import data_class_dir
from packages.orchestration.self_health import home_relative_text
from packages.orchestration.stream_evidence import redact_text

# How long a report keeps the `crash_reports` health check warning.
CRASH_RECENT_DAYS: int = 7

# The sentence every report ends with, so a pasted report states where it stays.
CRASH_NOTICE: str = "This report stays on this machine. Remedy never sends it anywhere."


# The one folder crash reports live in; the class name is a literal so the class registry test finds it.
def crash_reports_dir(root: Path | None = None) -> Path:
    return data_class_dir("crash", root)


# The installed version for the report header; `dev` in a checkout (packages never import apps).
def remedy_version() -> str:
    try:
        return distribution("remedy").version
    except PackageNotFoundError:
        return "dev"


# A digest of the resolved configuration, so two reports show whether the settings differed.
def config_digest() -> str:
    from packages.orchestration.run_manifest import _config_snapshot

    try:
        text = json.dumps(_config_snapshot(), sort_keys=True, default=str)
    except (OSError, ValueError):
        return "unavailable"
    return "sha256:" + sha256(text.encode("utf-8")).hexdigest()


# The report text: header lines, the traceback, the notice. The command, the error and each
# traceback entry are redacted on their own, so a private key hides only its part (R-1280).
def render_crash_report(
    error: BaseException, *, command: str, when: datetime, version: str, digest: str,
) -> str:
    moment = when if when.tzinfo is not None else when.replace(tzinfo=timezone.utc)
    stamp = moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    trace = "\n".join(
        redact_text(entry.rstrip("\n"))
        for entry in traceback.format_exception(type(error), error, error.__traceback__)
    )
    lines = [
        "# Remedy crash report",
        "",
        f"- time: {stamp}",
        f"- version: {version}",
        f"- command: {redact_text(command)}",
        f"- error: {redact_text(f'{type(error).__name__}: {error}')}",
        f"- configuration digest: {digest}",
        "",
        "## Traceback",
        "",
        "```",
        trace,
        "```",
        "",
        CRASH_NOTICE,
    ]
    return home_relative_text("\n".join(lines) + "\n")


# Write one report (folder 0700, file 0600); None on any write failure so the real error is never hidden.
def write_crash_report(
    error: BaseException, *, command: str, root: Path | None = None,
    now: datetime | None = None,
) -> Path | None:
    try:
        moment = now if now is not None else datetime.now(timezone.utc)
        text = render_crash_report(
            error, command=command, when=moment,
            version=remedy_version(), digest=config_digest())
        folder = crash_reports_dir(root)
        folder.mkdir(mode=0o700, parents=True, exist_ok=True)
        path = folder / f"{moment:%Y%m%dT%H%M%S%f}Z-{os.getpid()}.md"
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
        return path
    except (OSError, ValueError, TypeError):
        return None


# A thread that dies on an exception writes a report; the previous hook still runs, and the caller can undo.
def install_thread_crash_hook(
    command: str, root: Path | None = None,
) -> Callable[[], None]:
    previous = threading.excepthook

    def hook(args: threading.ExceptHookArgs) -> None:
        if args.exc_value is not None and not issubclass(args.exc_type, SystemExit):
            name = args.thread.name if args.thread else "unknown"
            write_crash_report(
                args.exc_value, command=f"{command} (thread {name})", root=root)
        previous(args)

    threading.excepthook = hook

    def restore() -> None:
        threading.excepthook = previous

    return restore


# The reports the health check counts: modified within `days` of `now`, newest first.
def recent_crash_reports(
    root: Path | None = None, *, now: datetime | None = None,
    days: int = CRASH_RECENT_DAYS,
) -> list[Path]:
    folder = crash_reports_dir(root)
    if not folder.is_dir():
        return []
    moment = now if now is not None else datetime.now(timezone.utc)
    cutoff = moment.timestamp() - days * 86400
    found: list[tuple[float, str, Path]] = []
    for path in folder.glob("*.md"):
        try:
            modified = path.stat().st_mtime
        except OSError:
            continue
        if modified >= cutoff:
            found.append((modified, path.name, path))
    found.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return [path for _m, _n, path in found]
