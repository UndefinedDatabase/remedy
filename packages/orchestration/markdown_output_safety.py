"""
Shared Markdown output-boundary safety helpers.

Every Remedy-generated text line that will be written into a target repository
Markdown file must pass through neutralize_markdown_html_comment_start before
being written.  This is an output-boundary defense, not a content policy — it
applies only to generated text, never to existing user file content.

Why "&lt;!--":
  HTML entity encoding is renderer-portable.  Markdown backslash escaping
  ("\\<!--") is renderer-specific and less reliable across toolchains.

Why all "<!--", not just Remedy-specific prefixes:
  LLM-generated proposed lines can contain arbitrary HTML comments.  Neutralizing
  all raw HTML comment starts closes the full injection surface at the write
  boundary rather than attempting an allowlist of known harmful prefixes.

No I/O.  No dependencies.  No policy engine.
"""

HTML_COMMENT_START      = "<!--"
HTML_COMMENT_START_SAFE = "&lt;!--"


def neutralize_markdown_html_comment_start(text: str) -> str:
    """Replace every raw HTML comment start in generated Markdown text with a safe form.

    Converts ``<!--`` → ``&lt;!--`` in *text*.  The result is valid Markdown
    that renders visibly and is unambiguously not an active HTML comment.

    *text* must be a ``str``.  Callers are responsible for normalising optional
    metadata fields (e.g. ``str(value or "")``) before passing them here.
    This keeps the helper pure and prevents silent coercion of ``None`` or other
    objects to their string representations.

    Does NOT double-encode: ``&lt;!--`` in the input is left unchanged because
    it does not contain the literal substring ``<!--``.
    """
    return text.replace(HTML_COMMENT_START, HTML_COMMENT_START_SAFE)
