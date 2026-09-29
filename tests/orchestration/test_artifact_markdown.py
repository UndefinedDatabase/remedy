"""F041 T001 — the attack corpus of the sanitized markdown pipeline (DECISION F041 D1).

THE CORPUS IS A DELIVERABLE AND ONLY GROWS. Every vector a review finds that this pipeline let
through, or that nobody had tried yet, is added below with the output it must produce, in the
round that finds it; a vector is never removed, and an expected output is never loosened to
make a run green. Each vector is judged three ways: its whole output equals the literal beside
it, an audit written HERE, from literal sets rather than the module's own, finds nothing, and
sanitizing the output again changes nothing.
"""

from __future__ import annotations

from html.parser import HTMLParser

import pytest

from packages.orchestration.artifact_markdown import (
    MARKDOWN_MAX_BYTES,
    RenderedMarkdown,
    render_markdown,
    safe_url,
    sanitize_fragment,
)

#: What the audit lets through, written out rather than imported: an audit that read the
#: module's own sets could never disagree with the module.
AUDIT_TAGS = {
    "a", "blockquote", "br", "code", "em", "h1", "h2", "h3", "h4", "h5", "h6",
    "hr", "img", "li", "ol", "p", "pre", "strong", "ul",
}
AUDIT_ATTRIBUTES = {"a": {"href", "title", "rel"}, "img": {"alt", "src", "title"}}
AUDIT_REL = "noopener noreferrer nofollow"


class _Audit(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.problems: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag not in AUDIT_TAGS:
            self.problems.append(f"tag {tag}")
        names = [name for name, _ in attrs]
        if tag == "a" and names[-1:] != ["rel"]:
            self.problems.append("a without rel last")
        for name, value in attrs:
            if name not in AUDIT_ATTRIBUTES.get(tag, set()):
                self.problems.append(f"attribute {tag}.{name}")
            elif name == "rel" and value != AUDIT_REL:
                self.problems.append(f"rel {value!r}")
            elif name in ("href", "src"):
                probe = "".join(ch for ch in (value or "") if ord(ch) > 32 and ord(ch) != 127)
                probe = probe.lower()
                head = probe.split("/", 1)[0].split("?", 1)[0].split("#", 1)[0]
                if probe.startswith("//") or "\\" in probe:
                    self.problems.append(f"network path {tag}.{name}")
                elif ":" in head and (name == "src" or head.split(":", 1)[0] not in
                                      {"http", "https", "mailto"}):
                    self.problems.append(f"scheme {tag}.{name}={value!r}")

    def handle_comment(self, data):
        self.problems.append("comment")

    def handle_decl(self, decl):
        self.problems.append("declaration")

    def handle_pi(self, data):
        self.problems.append("processing instruction")


def _audit(markup: str) -> list[str]:
    audit = _Audit()
    audit.feed(markup)
    audit.close()
    return audit.problems


#: (label, source HTML, the sanitizer's whole output)
HTML_ATTACK_CORPUS = [
    ('script', '<script>alert(1)</script>',
     ''),
    ('script-uppercase-src', '<SCRIPT SRC=//x.example/x.js></SCRIPT>',
     ''),
    ('img-onerror', '<img src=x onerror=alert(1)>',
     '<img src="x">'),
    ('a-javascript', '<a href="javascript:alert(1)">x</a>',
     '<a rel="noopener noreferrer nofollow">x</a>'),
    ('a-entity-javascript', '<a href="&#x6A;avascript:alert(1)">x</a>',
     '<a rel="noopener noreferrer nofollow">x</a>'),
    ('a-leading-space-javascript', '<a href=" javascript:alert(1)">x</a>',
     '<a rel="noopener noreferrer nofollow">x</a>'),
    ('a-tab-javascript', '<a href="java&#9;script:alert(1)">x</a>',
     '<a rel="noopener noreferrer nofollow">x</a>'),
    ('a-onclick', '<a href="https://ok.example" onclick="alert(1)">x</a>',
     '<a href="https://ok.example" rel="noopener noreferrer nofollow">x</a>'),
    ('a-vbscript', '<a href="vbscript:msgbox(1)">x</a>',
     '<a rel="noopener noreferrer nofollow">x</a>'),
    ('a-data', '<a href="data:text/html;base64,PHNjcmlwdD4=">x</a>',
     '<a rel="noopener noreferrer nofollow">x</a>'),
    ('a-protocol-relative', '<a href="//evil.example/">x</a>',
     '<a rel="noopener noreferrer nofollow">x</a>'),
    ('a-backslash', '<a href="/\\evil.example/">x</a>',
     '<a rel="noopener noreferrer nofollow">x</a>'),
    ('a-space-protocol-relative', '<a href=" //evil.example/">x</a>',
     '<a rel="noopener noreferrer nofollow">x</a>'),
    ('svg-onload', '<svg onload=alert(1)><circle/></svg>',
     ''),
    ('svg-script', '<svg><script>alert(1)</script></svg>',
     ''),
    ('iframe', '<iframe src="https://x.example"></iframe>',
     ''),
    ('object', '<object data="x.swf"></object>',
     ''),
    ('embed', '<embed src=x>',
     ''),
    ('style-element', '<style>body{background:url(javascript:alert(1))}</style>',
     ''),
    ('style-attribute', '<p style="background:url(javascript:alert(1))">x</p>',
     '<p>x</p>'),
    ('comment', '<!--<script>alert(1)</script>-->',
     ''),
    ('math-mutation', '<math><mtext><table><mglyph><style><img src=x onerror=alert(1)>',
     ''),
    ('noscript-mutation', '<noscript><p title="</noscript><img src=x onerror=alert(1)>">',
     ''),
    ('form-action', '<form action="javascript:alert(1)"><input type=submit></form>',
     ''),
    ('meta-refresh', '<meta http-equiv="refresh" content="0;url=javascript:alert(1)">',
     ''),
    ('base-href', '<base href="javascript:alert(1)//">',
     ''),
    ('split-script', '<scr<script>ipt>alert(1)</script>',
     'ipt&gt;alert(1)'),
    ('details-ontoggle', '<details open ontoggle=alert(1)>x</details>',
     'x'),
    ('img-data', '<img src="data:image/svg+xml;base64,PHN2Zz4=" alt="d">',
     'd'),
    ('img-external', '<img src="https://track.example/p.png" alt="t">',
     't'),
    ('img-unterminated', '<img src="x" onerror="alert(1)"',
     ''),
    ('textarea', '<textarea><script>alert(1)</script></textarea>',
     ''),
]

#: (label, source markdown, the renderer's whole output)
MARKDOWN_ATTACK_CORPUS = [
    ('md-javascript-link', '[x](javascript:alert(1))',
     '<p><a rel="noopener noreferrer nofollow">x</a>)</p>'),
    ('md-mixed-case-link', '[x](JaVaScRiPt:alert(1))',
     '<p><a rel="noopener noreferrer nofollow">x</a>)</p>'),
    ('md-entity-link', '[x](&#106;avascript:alert(1))',
     '<p><a href="&amp;#106;avascript:alert(1" rel="noopener noreferrer nofollow">x</a>)</p>'),
    ('md-vbscript-link', '[x](vbscript:msgbox(1))',
     '<p><a rel="noopener noreferrer nofollow">x</a>)</p>'),
    ('md-data-link', '[x](data:text/html;base64,PHNjcmlwdD4=)',
     '<p><a rel="noopener noreferrer nofollow">x</a></p>'),
    ('md-protocol-relative-link', '[x](//evil.example/)',
     '<p><a rel="noopener noreferrer nofollow">x</a></p>'),
    ('md-data-image', '![x](data:image/svg+xml;base64,PHN2Zz4=)',
     '<p>x</p>'),
    ('md-javascript-image', '![x](javascript:alert(1))',
     '<p>x)</p>'),
    ('md-external-image', '![x](https://track.example/p.png)',
     '<p>x</p>'),
    ('md-title-breakout', '[x](https://a.example "a&quot;><script>alert(1)</script>")',
     '<p><a href="https://a.example" title="a&amp;quot;&gt;&lt;script&gt;alert(1)&lt;/script&gt;" rel="noopener noreferrer nofollow">x</a></p>'),
    ('md-code-span', '`<script>alert(1)</script>`',
     '<p><code>&lt;script&gt;alert(1)&lt;/script&gt;</code></p>'),
    ('md-raw-html', '<img src=x onerror=alert(1)>',
     '<p>&lt;img src=x onerror=alert(1)&gt;</p>'),
    ('md-heading-html', '# <script>alert(1)</script>',
     '<h1>&lt;script&gt;alert(1)&lt;/script&gt;</h1>'),
    ('md-fence-html', '```\n<script>alert(1)</script>\n```',
     '<pre><code>&lt;script&gt;alert(1)&lt;/script&gt;</code></pre>'),
    ('md-list-html', '- <iframe src=x></iframe>',
     '<ul><li>&lt;iframe src=x&gt;&lt;/iframe&gt;</li></ul>'),
    ('md-link-label-html', '[<b onmouseover=alert(1)>x</b>](https://a.example)',
     '<p><a href="https://a.example" rel="noopener noreferrer nofollow">&lt;b onmouseover=alert(1)&gt;x&lt;/b&gt;</a></p>'),
]


@pytest.mark.parametrize(("label", "source", "expected"), HTML_ATTACK_CORPUS,
                         ids=[row[0] for row in HTML_ATTACK_CORPUS])
def test_an_html_vector_is_neutralized_by_the_sanitizer(label, source, expected):
    out = sanitize_fragment(source)
    assert out == expected
    assert _audit(out) == []
    assert sanitize_fragment(out) == out


@pytest.mark.parametrize(("label", "source", "expected"), HTML_ATTACK_CORPUS,
                         ids=[row[0] for row in HTML_ATTACK_CORPUS])
def test_an_html_vector_in_a_readme_is_shown_as_text(label, source, expected):
    # Raw HTML is never markup in a README: the renderer escapes it before the sanitizer runs.
    out = render_markdown(source).html
    assert "<" not in out.removeprefix("<p>").removesuffix("</p>")
    assert _audit(out) == []


@pytest.mark.parametrize(("label", "source", "expected"), MARKDOWN_ATTACK_CORPUS,
                         ids=[row[0] for row in MARKDOWN_ATTACK_CORPUS])
def test_a_markdown_vector_is_neutralized_by_the_renderer(label, source, expected):
    out = render_markdown(source).html
    assert out == expected
    assert _audit(out) == []
    assert sanitize_fragment(out) == out


@pytest.mark.parametrize(("value", "image", "expected"), [
    ("https://a.example/x", False, "https://a.example/x"),
    ("http://a.example", False, "http://a.example"),
    ("mailto:a@b.example", False, "mailto:a@b.example"),
    ("  docs/guide.md  ", False, "docs/guide.md"),
    ("#section", False, "#section"),
    ("captures/a.png", True, "captures/a.png"),
    ("https://a.example/p.png", True, None),
    ("javascript:alert(1)", False, None),
    ("JAVASCRIPT:alert(1)", False, None),
    ("java\tscript:alert(1)", False, None),
    ("\x01javascript:alert(1)", False, None),
    ("vbscript:x", False, None),
    ("data:text/html,x", False, None),
    ("data:image/png;base64,x", True, None),
    ("ftp://a.example", False, None),
    ("//evil.example", False, None),
    (" \t//evil.example", False, None),
    ("/\\evil.example", False, None),
    ("", False, None),
    (" \t", False, None),
])
def test_safe_url_keeps_only_the_schemes_it_names(value, image, expected):
    assert safe_url(value, image=image) == expected


def test_a_readme_renders_the_subset_it_supports():
    source = (
        "# Title\n\nSome *em*, **strong** and `c<d>`.\n\n- a\n- [b](https://b.example)\n\n"
        "1. one\n2. two\n\n> quoted\n\n---\n\n![shot](captures/a.png)\n\n```py\nx < 1 & y\n```\n"
        "[mail](mailto:a@b.example)"
    )
    assert render_markdown(source) == RenderedMarkdown(
        html=(
            '<h1>Title</h1><p>Some <em>em</em>, <strong>strong</strong> and <code>c&lt;d&gt;'
            '</code>.</p><ul><li>a</li><li><a href="https://b.example" rel="noopener noreferrer'
            ' nofollow">b</a></li></ul><ol><li>one</li><li>two</li></ol><blockquote><p>quoted'
            '</p></blockquote><hr><p><img src="captures/a.png" alt="shot"></p><pre><code>x &lt;'
            ' 1 &amp; y</code></pre><p><a href="mailto:a@b.example" rel="noopener noreferrer'
            ' nofollow">mail</a></p>'
        ),
        truncated=False,
        source_bytes=len(source.encode("utf-8")),
    )


def test_an_empty_readme_renders_nothing():
    assert render_markdown("") == RenderedMarkdown(html="", truncated=False, source_bytes=0)


def test_a_readme_at_the_cap_is_rendered_whole():
    source = "line\n" * (MARKDOWN_MAX_BYTES // 5)
    assert len(source.encode("utf-8")) <= MARKDOWN_MAX_BYTES
    rendered = render_markdown(source)
    assert rendered.truncated is False
    assert rendered.html.count("line") == MARKDOWN_MAX_BYTES // 5


def test_a_readme_over_the_cap_is_cut_at_its_last_full_line():
    lines = MARKDOWN_MAX_BYTES // 5
    source = "line\n" * lines + "tail-beyond-the-cap\n"
    rendered = render_markdown(source)
    assert rendered.truncated is True
    assert rendered.source_bytes == len(source.encode("utf-8"))
    assert "tail-beyond-the-cap" not in rendered.html
    assert rendered.html.count("line") == lines


def test_a_multibyte_character_is_never_split_by_the_cap():
    # One ASCII byte first, so the cap falls inside the last two-byte character.
    source = "a" + "é" * MARKDOWN_MAX_BYTES
    rendered = render_markdown(source)
    assert rendered.truncated is True
    assert rendered.html == "<p>a" + "é" * (MARKDOWN_MAX_BYTES // 2 - 1) + "</p>"


def test_unclosed_and_stray_tags_leave_well_formed_markup():
    assert sanitize_fragment("<p><strong>x") == "<p><strong>x</strong></p>"
    assert sanitize_fragment("x</p></em>") == "x"
    assert sanitize_fragment("<ul><li>a<li>b</ul>") == "<ul><li>a<li>b</li></li></ul>"
    assert sanitize_fragment("a &amp; b &lt;c&gt;") == "a &amp; b &lt;c&gt;"
