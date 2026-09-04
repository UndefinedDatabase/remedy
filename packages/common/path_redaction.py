"""Local-path and `file:`-URI sanitization — one implementation, two callers.

F007 built this and had it accepted after several rounds of adversarial review: quoted
paths with spaces, POSIX, Windows drive (both slash styles), UNC, `file:` URIs including
the localhost and Windows-drive spellings, percent-decoding, and — the part that is easy to
get wrong — a real scheme boundary, so `profile:`, `myfile:`, `notafile:`, `some.file:` and
`x-file:` are NOT file URIs and are left exactly as they are.

F010 needed the same thing for its post-mortems. Copying it would have created a second,
weaker scrubber that drifts away from the tested one, so the accepted implementation moved
here unchanged and both call it: `packages/runtimes/dev_server.py` (F007's shareable runtime
state) and `packages/orchestration/failure_postmortem.py` (F010's records).

Ordinary URLs are deliberately left alone — `http://127.0.0.1:5173/health` is an address,
not somebody's home directory.
"""
from __future__ import annotations

import re
from pathlib import Path, PureWindowsPath

#: Every normal absolute-path form, ANYWHERE inside a string — after `--flag=`, after
#: `key=`, inside a quote, in the middle of a diagnostic sentence:
#:
#:     /home/user/file            POSIX
#:     C:\Users\Alice\file        Windows, backslashes
#:     C:/Users/Alice/file        Windows, forward slashes
#:     \\server\share\file        UNC
#:     //server/share/file        UNC, forward slashes
#:
#: The look-behind keeps ordinary URLs intact: in ``http://127.0.0.1:5173/health`` the
#: `//` follows a colon and the path slash follows a word character, so neither starts a
#: match. A bare ``C:`` that is not followed by a separator is ordinary text, not a path,
#: and is left alone.
PATH_TAIL = r"""[^\s'"`,;)\]}]"""
ABS_PATH_RE = re.compile(
    rf"""(?<![\w:/\\])(?:
            \\\\{PATH_TAIL}+                 # \\server\share\...
          | //{PATH_TAIL}+                   # //server/share/...
          | [A-Za-z]:[\\/]{PATH_TAIL}*       # C:\... or C:/...
          | /(?=[\w.~/]){PATH_TAIL}+        # /posix/path — real path start (R-0790: excludes a bare-punctuation tail like "-" in "+/-")
        )""",
    re.VERBOSE,
)

#: What makes a token an absolute path worth redacting by value.
ABS_PREFIX_RE = re.compile(r"\A(?:/|\\\\|//|[A-Za-z]:[\\/])")

#: A QUOTED absolute path — the only form in which a path may legitimately contain
#: spaces, e.g. ``working directory "C:/Users/Alice/private dir" cannot be inspected``.
#: Unquoted, a space ends the path, and only its prefix (the private part) is removed.
QUOTED_PATH_RE = re.compile(
    r"""(['"])((?:\\\\|//|[A-Za-z]:[\\/]|/)[^'"]*)\1""")

#: A `file:` URI. It LOOKS like a URL, which is exactly why the generic path scrub — which
#: deliberately leaves URLs alone — used to walk straight past
#: ``file:///home/alice/private/secret.txt``. A file URI is not a network address: it is a
#: local path wearing a scheme, and it is redacted like one. The look-behind is the scheme
#: BOUNDARY: without it, ``profile:///home/alice/x.txt`` matched from its ``file:`` onwards
#: and came back as ``protest.txt`` — a string that is not a file URI at all being quietly
#: rewritten.
FILE_URI_RE = re.compile(
    r"""(?<![A-Za-z0-9+.\-])file:(?://)?[^\s'"`,;)\]}]*""", re.IGNORECASE)

#: Schemes that are addresses, not local paths. A `label:/abs/path` diagnostic
#: (``cwd:/tmp/secret-repo``, ``path:/home/user/private.txt``) hides an absolute path behind
#: a colon, which is exactly where ABS_PATH_RE's URL-preserving look-behind stops looking.
_ADDRESS_SCHEMES = frozenset({"http", "https", "ftp", "ftps", "ws", "wss", "file", "data",
                              "mailto"})
#: A single leading slash only: ``scheme://host/...`` is a URL spelling (``profile://…``,
#: ``myfile://…``) and F007 deliberately leaves those alone.
#: A label is at least two characters: a single letter followed by a colon is a Windows
#: DRIVE (``C:\Users\…``), which the absolute-path rule already handles properly.
LABELLED_PATH_RE = re.compile(
    rf"""(?<![A-Za-z0-9+.\-/])([A-Za-z][A-Za-z0-9_\-]+):((?:/(?!/)){PATH_TAIL}*)""")


def basename(token: str) -> str:
    """The bare file name of a POSIX, Windows or UNC path, on whatever host runs this."""
    text = str(token)
    if "\\" in text or re.match(r"\A[A-Za-z]:", text) or text.startswith("//"):
        return PureWindowsPath(text).name or "[path]"
    return Path(text).name or "[path]"


def file_uri_basename(uri: str) -> str:
    """The bare file name behind a `file:` URI, in every normal form.

    ``file:///home/alice/secret.txt``            → secret.txt
    ``file://localhost/home/alice/secret.txt``   → secret.txt
    ``file:///C:/Users/Alice/secret.txt``        → secret.txt
    ``file://server/share/secret.txt``           → secret.txt   (host is private too)
    ``file:///home/alice/private%20dir/x.txt``   → x.txt        (percent-decoded)

    Never a path operation on an arbitrary string: the URI is split first, and anything
    that does not yield a name becomes ``[path]``.
    """
    from urllib.parse import unquote, urlsplit

    try:
        parts = urlsplit(uri)
        path = unquote(parts.path or "")
    except ValueError:
        return "[path]"
    if not path:
        return "[path]"
    path = path.lstrip("/")              # /C:/Users/... and /home/... alike
    return basename(path) or "[path]"


def scrub_paths(value: str) -> str:
    """Reduce every absolute path — and every local file URI — to its bare file name.

    This is F007's accepted behaviour, unchanged. Callers that also need
    ``label:/absolute/path`` handled use :func:`scrub_labelled_paths` first.
    """
    text = FILE_URI_RE.sub(lambda m: file_uri_basename(m.group(0)), value)
    text = QUOTED_PATH_RE.sub(
        lambda m: f"{m.group(1)}{basename(m.group(2))}{m.group(1)}", text)
    return ABS_PATH_RE.sub(lambda m: basename(m.group(0)), text)


def scrub_labelled_paths(value: str) -> str:
    """``cwd:/tmp/secret-repo`` → ``cwd:secret-repo``. Addresses are left alone.

    Only the label survives; the path behind the colon is reduced to its file name. `http:`,
    `https:`, `file:` and friends are addresses (or are handled by :func:`scrub_paths`) and
    are never touched here.
    """
    def replace(match: re.Match[str]) -> str:
        label, path = match.group(1), match.group(2)
        if label.lower() in _ADDRESS_SCHEMES:
            return match.group(0)
        return f"{label}:{basename(path)}"

    return LABELLED_PATH_RE.sub(replace, value)
