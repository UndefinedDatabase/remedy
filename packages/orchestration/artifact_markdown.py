"""Artifact markdown — a README rendered and sanitized on the server (F041 T001,
DECISION F041 D1).

``render_markdown`` renders a closed subset of markdown (ATX headings, paragraphs,
emphasis, code spans, fenced code, one-level lists, block quotes, rules, links and
images) and escapes every source character, so raw HTML sitting in a README is text,
never markup. ``sanitize_fragment`` then rebuilds ANY html string — the renderer's own
output included — with :mod:`html.parser` from an allowlist of tags and attributes,
dropping script-bearing elements with their content, keeping a link only to http,
https or mailto with ``rel="noopener noreferrer nofollow"``, and keeping an image only
from a path with no scheme at all. The attack corpus that pins this behaviour lives at
``tests/orchestration/test_artifact_markdown.py`` and only grows.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from html.parser import HTMLParser

#: A README over this many UTF-8 bytes is cut to its last full line before rendering.
MARKDOWN_MAX_BYTES = 262_144

#: Tags the sanitizer keeps. Everything else is either dropped-with-content
#: (:data:`DROPPED_WITH_CONTENT`) or dropped as a tag while its text survives.
ALLOWED_TAGS = frozenset({
    "a", "blockquote", "br", "code", "em", "h1", "h2", "h3", "h4", "h5", "h6",
    "hr", "img", "li", "ol", "p", "pre", "strong", "ul",
})

#: Attributes kept per kept tag; every other tag keeps none.
ALLOWED_ATTRIBUTES: dict[str, frozenset[str]] = {
    "a": frozenset({"href", "title"}),
    "img": frozenset({"alt", "src", "title"}),
}

#: Tags written without a matching close tag and never pushed onto the open-tag stack.
VOID_TAGS = frozenset({"br", "hr", "img"})

#: An element whose START tag drops every event up to and including its OWN end tag,
#: counting nested elements of the same name so a `<script><script>` pair does not
#: resume on the first `</script>`.
DROPPED_WITH_CONTENT = frozenset({
    "embed", "iframe", "math", "noscript", "object", "script", "style", "svg",
    "template", "textarea", "title", "xmp",
})

#: Schemes a kept `href` may carry. An image never carries a scheme at all.
LINK_SCHEMES = frozenset({"http", "https", "mailto"})

#: The `rel` every kept `<a>` gains, as its LAST attribute.
LINK_REL = "noopener noreferrer nofollow"

_CONTROL_OR_DEL = frozenset(chr(c) for c in range(0x21)) | {chr(0x7F)}


def safe_url(value: str, *, image: bool) -> str | None:
    """The URL to keep for `href` (``image=False``) or `src` (``image=True``), or None.

    The decision is made on a PROBE: `value` with every character from U+0000 to
    U+0020 and U+007F removed, lowercased. An empty probe, one starting ``//``, or
    one holding a backslash is refused outright. A scheme is present when a colon
    occurs before the first ``/``, ``?`` or ``#`` of the probe (whichever comes
    first, if any) — an image never keeps a scheme, and a link keeps one only from
    :data:`LINK_SCHEMES`. Anything else is a bare path or fragment and is kept,
    STRIPPED (not probed) — the returned value is always `value.strip()`.
    """
    probe = "".join(ch for ch in value if ch not in _CONTROL_OR_DEL).lower()
    if not probe or probe.startswith("//") or "\\" in probe:
        return None
    cut = len(probe)
    for marker in ("/", "?", "#"):
        idx = probe.find(marker)
        if idx != -1 and idx < cut:
            cut = idx
    colon = probe.find(":")
    if colon != -1 and colon < cut:
        if image:
            return None
        if probe[:colon] not in LINK_SCHEMES:
            return None
    return value.strip()


class _FragmentSanitizer(HTMLParser):
    """Rebuilds `markup` from :data:`ALLOWED_TAGS`, dropping everything else."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._out: list[str] = []
        self._open: list[str] = []
        self._dropping_tag: str | None = None
        self._dropping_depth = 0

    def result(self) -> str:
        for tag in reversed(self._open):
            self._out.append(f"</{tag}>")
        self._open = []
        return "".join(self._out)

    # -- html.parser callbacks ------------------------------------------------

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self._dropping_tag is not None:
            if tag == self._dropping_tag:
                self._dropping_depth += 1
            return
        if tag in DROPPED_WITH_CONTENT:
            self._dropping_tag = tag
            self._dropping_depth = 1
            return
        if tag not in ALLOWED_TAGS:
            return
        allowed = ALLOWED_ATTRIBUTES.get(tag, frozenset())
        kept: list[tuple[str, str]] = []
        for name, value in attrs:
            if name not in allowed or value is None:
                continue
            if (tag == "a" and name == "href") or (tag == "img" and name == "src"):
                resolved = safe_url(value, image=(tag == "img"))
                if resolved is None:
                    continue
                value = resolved
            kept.append((name, value))
        if tag == "a":
            kept.append(("rel", LINK_REL))
        if tag == "img" and not any(name == "src" for name, _ in kept):
            alt = next((v for n, v in kept if n == "alt"), "")
            self._out.append(html.escape(alt, quote=False))
            return
        parts = [tag] + [f'{name}="{html.escape(value, quote=True)}"' for name, value in kept]
        self._out.append("<" + " ".join(parts) + ">")
        if tag not in VOID_TAGS:
            self._open.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if self._dropping_tag is not None:
            if tag == self._dropping_tag:
                self._dropping_depth -= 1
                if self._dropping_depth == 0:
                    self._dropping_tag = None
            return
        if tag not in self._open:
            return
        while self._open:
            top = self._open.pop()
            self._out.append(f"</{top}>")
            if top == tag:
                break

    def handle_data(self, data: str) -> None:
        if self._dropping_tag is not None:
            return
        self._out.append(html.escape(data, quote=False))

    def handle_comment(self, data: str) -> None:
        pass

    def handle_decl(self, decl: str) -> None:
        pass

    def handle_pi(self, data: str) -> None:
        pass


def sanitize_fragment(markup: str) -> str:
    """Rebuild `markup` from :data:`ALLOWED_TAGS` and :data:`ALLOWED_ATTRIBUTES` alone."""
    parser = _FragmentSanitizer()
    parser.feed(markup)
    parser.close()
    return parser.result()


@dataclass(frozen=True)
class RenderedMarkdown:
    """The result of :func:`render_markdown`: sanitized HTML plus its provenance."""

    html: str
    truncated: bool
    source_bytes: int


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*$")
_RULE_RE = re.compile(r"^([-*_])(\s*\1){2,}$")
_LIST_RE = re.compile(r"^([-*+]|\d+\.)\s+(.*)$")


def _escape_run(text: str) -> str:
    return html.escape(text, quote=False)


def _render_inline(text: str) -> str:
    """The inline scanner: code spans, links/images, emphasis, else escaped text."""
    out: list[str] = []
    plain: list[str] = []
    i = 0
    n = len(text)

    def flush_plain() -> None:
        if plain:
            out.append(_escape_run("".join(plain)))
            plain.clear()

    while i < n:
        ch = text[i]
        if ch == "`":
            j = text.find("`", i + 1)
            if j != -1:
                flush_plain()
                out.append(f"<code>{_escape_run(text[i + 1:j])}</code>")
                i = j + 1
                continue
        elif ch == "!" and text[i + 1:i + 2] == "[" or ch == "[":
            is_image = ch == "!"
            label_start = i + 2 if is_image else i + 1
            rendered = _render_link_or_image(text, i, label_start, is_image)
            if rendered is not None:
                flush_plain()
                out.append(rendered[0])
                i = rendered[1]
                continue
        elif ch in ("*", "_"):
            rendered = _render_emphasis(text, i)
            if rendered is not None:
                flush_plain()
                out.append(rendered[0])
                i = rendered[1]
                continue
        plain.append(ch)
        i += 1
    flush_plain()
    return "".join(out)


def _render_emphasis(text: str, i: int) -> tuple[str, int] | None:
    marker = text[i]
    double = text[i:i + 2] == marker * 2
    needle = marker * 2 if double else marker
    start = i + len(needle)
    j = text.find(needle, start)
    if j == -1 or j == start:
        return None
    tag = "strong" if double else "em"
    inner = _escape_run(text[start:j])
    return f"<{tag}>{inner}</{tag}>", j + len(needle)


def _render_link_or_image(
    text: str, start: int, label_start: int, is_image: bool
) -> tuple[str, int] | None:
    label_end = text.find("]", label_start)
    if label_end == -1 or text[label_end + 1:label_end + 2] != "(":
        return None
    url_start = label_end + 2
    j = url_start
    n = len(text)
    while j < n and text[j] not in (" ", ")"):
        j += 1
    if j >= n:
        return None
    url = text[url_start:j]
    title: str | None = None
    if text[j] == ")":
        end_pos = j + 1
    else:
        k = j
        while k < n and text[k] == " ":
            k += 1
        if k >= n or text[k] != '"':
            return None
        title_start = k + 1
        title_end = text.find('"', title_start)
        if title_end == -1:
            return None
        if text[title_end + 1:title_end + 2] != ")":
            return None
        title = text[title_start:title_end]
        end_pos = title_end + 2

    label_text = text[label_start:label_end]
    if is_image:
        attrs = f' src="{html.escape(url, quote=True)}" alt="{html.escape(label_text, quote=True)}"'
        if title is not None:
            attrs += f' title="{html.escape(title, quote=True)}"'
        return f"<img{attrs}>", end_pos
    attrs = f' href="{html.escape(url, quote=True)}"'
    if title is not None:
        attrs += f' title="{html.escape(title, quote=True)}"'
    label_html = _render_inline(label_text)
    return f"<a{attrs}>{label_html}</a>", end_pos


def _render_blocks(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            joined = " ".join(line.strip() for line in paragraph)
            out.append(f"<p>{_render_inline(joined)}</p>")
            paragraph.clear()

    i = 0
    n = len(lines)
    while i < n:
        raw_line = lines[i]
        stripped = raw_line.strip()

        if not stripped:
            flush_paragraph()
            i += 1
            continue

        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            content: list[str] = []
            i += 1
            while i < n and not lines[i].strip().startswith(marker):
                content.append(lines[i])
                i += 1
            if i < n:
                i += 1  # consume the closing fence line
            flush_paragraph()
            out.append(f"<pre><code>{_escape_run(chr(10).join(content))}</code></pre>")
            continue

        heading = _HEADING_RE.match(stripped)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            out.append(f"<h{level}>{_render_inline(heading.group(2))}</h{level}>")
            i += 1
            continue

        if _RULE_RE.match(stripped):
            flush_paragraph()
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            parts: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                parts.append(lines[i].strip()[1:].strip())
                i += 1
            out.append(f"<blockquote><p>{_render_inline(' '.join(parts))}</p></blockquote>")
            continue

        list_match = _LIST_RE.match(stripped)
        if list_match:
            flush_paragraph()
            kind = "ul" if list_match.group(1) in ("-", "*", "+") else "ol"
            items: list[str] = []
            while i < n:
                current = lines[i].strip()
                match = _LIST_RE.match(current)
                if not match:
                    break
                item_kind = "ul" if match.group(1) in ("-", "*", "+") else "ol"
                if item_kind != kind:
                    break
                items.append(f"<li>{_render_inline(match.group(2))}</li>")
                i += 1
            out.append(f"<{kind}>{''.join(items)}</{kind}>")
            continue

        paragraph.append(raw_line)
        i += 1

    flush_paragraph()
    return "".join(out)


def render_markdown(text: str) -> RenderedMarkdown:
    """Render `text` (a closed markdown subset) to sanitized HTML.

    A source over :data:`MARKDOWN_MAX_BYTES` UTF-8 bytes is cut to that many bytes,
    decoded ignoring a split trailing character, then cut before its last newline
    (when it has one) so a truncated render never ends mid-line. `source_bytes` is
    always the WHOLE source's byte length, truncated or not.
    """
    source_bytes = len(text.encode("utf-8"))
    truncated = False
    if source_bytes > MARKDOWN_MAX_BYTES:
        cut = text.encode("utf-8")[:MARKDOWN_MAX_BYTES]
        decoded = cut.decode("utf-8", errors="ignore")
        last_newline = decoded.rfind("\n")
        if last_newline != -1:
            decoded = decoded[:last_newline]
        text = decoded
        truncated = True
    rendered = _render_blocks(text)
    return RenderedMarkdown(
        html=sanitize_fragment(rendered), truncated=truncated, source_bytes=source_bytes,
    )
