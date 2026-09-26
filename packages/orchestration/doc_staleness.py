"""T5_F289 T001 (DECISION F289 D2) — the documentation-staleness catalog.

Twelve checks compare what `README.md`, `docs/README.md`, `docs/guides/*.md` and
the command catalog CLAIM with what SHIPS — the group and command surface of
`apps.cli.command_catalog` and the config-key registry of
`packages.orchestration.config`. Each check is a pure function of a root
directory and an injected :class:`ShippedTruth`, so it is provable red on a
stale fixture without touching the real repository or the real catalog. The
self-use generator's Tier 2 (`packages.orchestration.self_use_generator`) calls
:func:`run_staleness_checks` and renders the first claim no queue entry already
targets as a one-task job asking that the document be corrected.

Public API::

    StaleClaim: one document/claim/truth triple a check found
    ShippedTruth: the shipped surface a check compares a document against
    StalenessCheck: one check's identity, metadata and `run` function
    CHECKS: the twelve checks, in catalog order
    run_staleness_checks(root=None, truth=None) -> tuple[StaleClaim, ...]

Deliberate absences:
  * No check spawns a subprocess or opens a socket: every comparison reads a
    file already on disk against a :class:`ShippedTruth` already in memory.
  * A document a check would read that is absent under `root` yields no claim
    for that document — a repository fixture missing `docs/guides/` entirely
    is not staleness, it is a smaller tree. An `OSError` reading a document
    that exists is never swallowed: it propagates to the caller.
"""
from __future__ import annotations

import re
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class StaleClaim:
    """One claim a check found: a document says `claim`, but the shipped truth is `truth`."""

    check_id: str
    document: str
    claim: str
    truth: str

    @property
    def key(self) -> str:
        return f"{self.check_id}:{self.document}:{self.claim}"


@dataclass(frozen=True)
class ShippedTruth:
    """The shipped surface every check compares a document against.

    Built once from `apps.cli.command_catalog` and
    `packages.orchestration.config`, or assembled directly by a test.
    """

    #: Every group id AND alias, mapped to its own (real) group id.
    groups: dict[str, str]
    #: Every `(group_id, subcommand)` pair the catalog ships.
    command_pairs: frozenset[tuple[str, str]]
    #: Every `command_id` (`"<group_id>.<subcommand>"`) the catalog ships.
    command_ids: frozenset[str]
    #: Every registered config key (`ConfigKeySpec.key`).
    config_keys: frozenset[str]
    #: Every registered environment variable (`ConfigKeySpec.env_var`).
    env_vars: frozenset[str]
    #: `(label, text)` for every `CommandEntry.description`, `ArgDef.help` and
    #: `GroupDef.description` the catalog carries, labelled
    #: `"<command_id> description"`, `"<command_id> <arg.name> help"` and
    #: `"<group_id> description"` respectively.
    catalog_texts: tuple[tuple[str, str], ...]

    @classmethod
    def live(cls) -> ShippedTruth:
        """Build the truth from the real, shipped catalog and config registry."""
        from apps.cli.command_catalog import CATALOG, GROUPS
        from packages.orchestration.config import all_key_specs

        groups: dict[str, str] = {}
        for group_id, group in GROUPS.items():
            groups[group_id] = group_id
            for alias in group.aliases:
                groups[alias] = group_id

        command_pairs = frozenset((c.group_id, c.subcommand) for c in CATALOG)
        command_ids = frozenset(c.command_id for c in CATALOG)
        specs = all_key_specs()
        config_keys = frozenset(spec.key for spec in specs)
        env_vars = frozenset(spec.env_var for spec in specs)

        catalog_texts: list[tuple[str, str]] = []
        for group_id, group in GROUPS.items():
            catalog_texts.append((f"{group_id} description", group.description))
        for c in CATALOG:
            catalog_texts.append((f"{c.command_id} description", c.description))
            for arg in c.args:
                catalog_texts.append((f"{c.command_id} {arg.name} help", arg.help))

        return cls(
            groups=groups,
            command_pairs=command_pairs,
            command_ids=command_ids,
            config_keys=config_keys,
            env_vars=env_vars,
            catalog_texts=tuple(catalog_texts),
        )

    @property
    def key_prefixes(self) -> frozenset[str]:
        """The first dot-separated segment of every registered config key."""
        return frozenset(key.split(".", 1)[0] for key in self.config_keys)


CheckRunner = Callable[[Path, ShippedTruth], tuple[StaleClaim, ...]]


@dataclass(frozen=True)
class StalenessCheck:
    """One check: its id, the documents it reads, what it extracts and compares, and its runner."""

    check_id: str
    documents: tuple[str, ...]
    claim: str
    truth: str
    run: CheckRunner


# ---------------------------------------------------------------------------
# Shared regexes and small readers
# ---------------------------------------------------------------------------

_FENCE_MARK_RE = re.compile(r"^```")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
_SPAN_RE = re.compile(r"`([^`\n]+)`")
_KEY_NAME_RE = re.compile(r"[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+")
_KEY_NAME_WHOLE_RE = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+$")
_TWO_SEGMENT_WHOLE_RE = re.compile(r"^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$")
_REMEDY_VAR_RE = re.compile(r"(?<!\w)REMEDY_[A-Z0-9_]+")
_SOURCE_PATH_RE = re.compile(
    r"(?<![\w/])(?:packages|apps|tests|scripts)/[A-Za-z0-9_./-]+\.(?:py|ts|tsx|sh|json|toml)"
)
_TOML_TABLE_RE = re.compile(r"^\[([^\]]+)\]\s*$")
_TOML_KV_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_.]*)\s*=")

#: README, INDEX, then every GUIDES file — the fixed document order the
#: multi-document checks (C05, C06, C07, C11) sort their claims by.
_README = "README.md"
_INDEX = "docs/README.md"


def _guide_names(root: Path) -> list[str]:
    """`docs/guides/*.md` basenames, sorted — the GUIDES set."""
    guides_dir = root / "docs" / "guides"
    if not guides_dir.is_dir():
        return []
    return sorted(p.name for p in guides_dir.glob("*.md"))


def _guide_documents(root: Path) -> list[str]:
    """Every GUIDES file's repository-relative path, sorted."""
    return [f"docs/guides/{name}" for name in _guide_names(root)]


def _read(root: Path, relpath: str) -> str | None:
    """`relpath`'s text under `root`, or `None` if it does not exist. Propagates `OSError`."""
    path = root / relpath
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def _iter_lines_outside_fences(text: str) -> Iterator[tuple[int, str]]:
    """`(1-based line number, line)` for every line outside a fenced region."""
    in_fence = False
    for i, line in enumerate(text.splitlines(), start=1):
        if _FENCE_MARK_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield i, line


def _headings_outside_fences(text: str) -> list[str]:
    """Every heading's text (level 1 to 6), outside fences, in document order."""
    headings = []
    for _, line in _iter_lines_outside_fences(text):
        match = _HEADING_RE.match(line)
        if match:
            headings.append(match.group(2))
    return headings


def _slug(heading_text: str) -> str:
    """The heading's slug: stripped, lower-cased, non-word/space/hyphen chars removed, spaces to hyphens."""
    lowered = heading_text.strip().lower()
    kept = re.sub(r"[^\w\s-]", "", lowered)
    return kept.replace(" ", "-")


def _is_relative(target: str) -> bool:
    return not (
        target.startswith("http://") or target.startswith("https://") or target.startswith("mailto:")
    )


def _section_bounds(text: str, starts_with: str, *, exact: bool = False) -> tuple[int, int] | None:
    """0-based `(start, end)` line bounds of the section under the first matching `## ` heading.

    `start` is the line right after the heading; `end` is the line of the next
    `## ` heading, or the document's end. Bounds are over ALL lines (fences
    included) — a caller reads only the lines it wants outside fences via
    :func:`_section_lines_outside_fences`, so fence state is always tracked
    from the top of the document, never restarted mid-document.
    """
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if not line.startswith("## "):
            continue
        if exact and line.strip() == starts_with:
            start = i + 1
            break
        if not exact and line.startswith(starts_with):
            start = i + 1
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return start, end


def _section_lines_outside_fences(text: str, bounds: tuple[int, int]) -> list[tuple[int, str]]:
    """`(1-based line number, line)` for every line of `bounds` (0-based, half-open) outside a fence."""
    start, end = bounds
    return [
        (line_no, line)
        for line_no, line in _iter_lines_outside_fences(text)
        if start < line_no <= end
    ]


def _table_rows(lines: list[str]) -> list[list[str]]:
    """Every data row of a markdown table over `lines` — no header, no separator row."""
    rows: list[list[str]] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        body = stripped.strip("|")
        if set(body.replace("|", "").strip()) <= set("-: ") and body.strip():
            continue  # the `|---|---|` separator row
        cells = [c.strip() for c in body.split("|")]
        if cells and cells[0] in ("Keyword", "File"):
            continue  # the header row
        rows.append(cells)
    return rows


def _toml_fence_blocks(text: str) -> Iterator[tuple[list[str], int]]:
    """`(lines, 1-based start line)` for every fence whose opening line is exactly ```` ```toml ````."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].rstrip() == "```toml":
            block_start = i + 1
            j = block_start
            while j < len(lines) and not _FENCE_MARK_RE.match(lines[j]):
                j += 1
            yield lines[block_start:j], block_start + 1
            i = j + 1
        else:
            i += 1


def _sorted_claims(items: list[tuple[int, int, StaleClaim]]) -> tuple[StaleClaim, ...]:
    """`items` as `(doc_order, line_order, claim)`, sorted, claims only."""
    items.sort(key=lambda item: (item[0], item[1]))
    return tuple(claim for _, _, claim in items)


# ---------------------------------------------------------------------------
# C01 — docs_index_guide_registration
# ---------------------------------------------------------------------------


def _run_c01(root: Path, truth: ShippedTruth) -> tuple[StaleClaim, ...]:
    check_id = "docs_index_guide_registration"
    text = _read(root, _INDEX)
    if text is None:
        return ()
    quick_find_bounds = _section_bounds(text, "## Quick-Find Table", exact=True)
    guides_bounds = _section_bounds(text, "## Guides")
    quick_find_lines = (
        _section_lines_outside_fences(text, quick_find_bounds) if quick_find_bounds else None
    )
    guides_lines = _section_lines_outside_fences(text, guides_bounds) if guides_bounds else None

    def _links(lines: list[tuple[int, str]] | None) -> list[str]:
        if lines is None:
            return []
        return [m.group(1) for _, line in lines for m in _LINK_RE.finditer(line)]

    items: list[tuple[int, int, StaleClaim]] = []
    for order, name in enumerate(_guide_names(root)):
        target = f"guides/{name}"
        if quick_find_lines is not None and target not in _links(quick_find_lines):
            items.append((order, 0, StaleClaim(
                check_id, _INDEX,
                f"the Quick-Find Table has no link to `{target}`",
                f"`docs/guides/{name}` ships",
            )))
        if guides_lines is not None and target not in _links(guides_lines):
            items.append((order, 1, StaleClaim(
                check_id, _INDEX,
                f"the Guides section has no link to `{target}`",
                f"`docs/guides/{name}` ships",
            )))
    base_order = len(_guide_names(root))
    for section_name, lines in (("Quick-Find Table", quick_find_lines), ("Guides", guides_lines)):
        if lines is None:
            continue
        for target in _links(lines):
            if not target.startswith("guides/"):
                continue
            guide_name = target[len("guides/"):]
            if not (root / "docs" / "guides" / guide_name).is_file():
                items.append((base_order, 0, StaleClaim(
                    check_id, _INDEX,
                    f"the {section_name} section links `{target}`",
                    f"`docs/guides/{guide_name}` does not exist",
                )))
    return _sorted_claims(items)


# ---------------------------------------------------------------------------
# C02 — config_cli_table_complete
# ---------------------------------------------------------------------------


def _run_c02(root: Path, truth: ShippedTruth) -> tuple[StaleClaim, ...]:
    check_id = "config_cli_table_complete"
    document = "docs/guides/remedy-toml-user-guide.md"
    text = _read(root, document)
    if text is None:
        return ()
    bounds = _section_bounds(text, "## CLI commands", exact=True)
    if bounds is None:
        return ()
    documented: set[str] = set()
    for _, line in _section_lines_outside_fences(text, bounds):
        for m in _SPAN_RE.finditer(line):
            span = m.group(1)
            if span.startswith("remedy config "):
                words = span[len("remedy config "):].split()
                if words:
                    documented.add(words[0])
    shipped = {sub for (group_id, sub) in truth.command_pairs if group_id == "config"}
    items: list[tuple[int, int, StaleClaim]] = []
    for order, sub in enumerate(sorted(documented - shipped)):
        items.append((0, order, StaleClaim(
            check_id, document,
            f"documents the `config` subcommand `{sub}`",
            f"the `config` group ships no `{sub}` subcommand",
        )))
    for order, sub in enumerate(sorted(shipped - documented)):
        items.append((1, order, StaleClaim(
            check_id, document,
            f"the CLI commands table never documents the `config` subcommand `{sub}`",
            f"the `config` subcommand `{sub}` ships",
        )))
    return _sorted_claims(items)


# ---------------------------------------------------------------------------
# C03 — docs_index_command_lines
# ---------------------------------------------------------------------------


def _run_c03(root: Path, truth: ShippedTruth) -> tuple[StaleClaim, ...]:
    check_id = "docs_index_command_lines"
    text = _read(root, _INDEX)
    if text is None:
        return ()
    items: list[tuple[int, int, StaleClaim]] = []
    for line_no, line in _iter_lines_outside_fences(text):
        for m in _SPAN_RE.finditer(line):
            span = m.group(1)
            if not span.startswith("remedy "):
                continue
            words = span.split()
            if len(words) < 2 or not words[1][:1].islower():
                continue
            second = words[1]
            group_id = truth.groups.get(second)
            if group_id is None:
                items.append((0, line_no, StaleClaim(
                    check_id, _INDEX,
                    f"`{span}` names the group `{second}`",
                    f"no group `{second}` ships",
                )))
                continue
            if len(words) < 3:
                continue
            third = words[2]
            if third.startswith("-") or third.startswith("<"):
                continue
            if not third[:1].islower():
                continue
            if (group_id, third) not in truth.command_pairs:
                items.append((0, line_no, StaleClaim(
                    check_id, _INDEX,
                    f"`{span}` names `{group_id} {third}`",
                    f"`{group_id}` ships no `{third}` subcommand",
                )))
    return _sorted_claims(items)


# ---------------------------------------------------------------------------
# C04 — guide_relative_links
# ---------------------------------------------------------------------------


def _run_c04(root: Path, truth: ShippedTruth) -> tuple[StaleClaim, ...]:
    check_id = "guide_relative_links"
    items: list[tuple[int, int, StaleClaim]] = []
    for order, document in enumerate(_guide_documents(root)):
        text = _read(root, document)
        if text is None:
            continue
        guide_dir = (root / document).parent
        for line_no, line in _iter_lines_outside_fences(text):
            for m in _LINK_RE.finditer(line):
                target = m.group(1)
                if target.startswith("#") or not _is_relative(target):
                    continue
                path_part = target.split("#", 1)[0]
                resolved = (guide_dir / path_part).resolve()
                if not resolved.is_file():
                    items.append((order, line_no, StaleClaim(
                        check_id, document,
                        f"links `{target}`",
                        f"`{path_part}` does not resolve against `{document}`'s own folder",
                    )))
    return _sorted_claims(items)


# ---------------------------------------------------------------------------
# C05 — link_anchors_resolve
# ---------------------------------------------------------------------------


def _run_c05(root: Path, truth: ShippedTruth) -> tuple[StaleClaim, ...]:
    check_id = "link_anchors_resolve"
    items: list[tuple[int, int, StaleClaim]] = []
    documents = [_README, _INDEX] + _guide_documents(root)
    for order, document in enumerate(documents):
        text = _read(root, document)
        if text is None:
            continue
        doc_dir = (root / document).parent
        for line_no, line in _iter_lines_outside_fences(text):
            for m in _LINK_RE.finditer(line):
                target = m.group(1)
                if "#" not in target:
                    continue
                path_part, _, fragment = target.partition("#")
                if not _is_relative(path_part):
                    continue
                if path_part != "" and not path_part.endswith(".md"):
                    continue
                target_path = (root / document) if path_part == "" else (doc_dir / path_part).resolve()
                if not target_path.is_file():
                    continue  # left to C04
                slugs = {_slug(h) for h in _headings_outside_fences(target_path.read_text(encoding="utf-8"))}
                if fragment not in slugs:
                    items.append((order, line_no, StaleClaim(
                        check_id, document,
                        f"links `{target}`",
                        f"no heading of `{path_part or document}` slugs to `{fragment}`",
                    )))
    return _sorted_claims(items)


# ---------------------------------------------------------------------------
# C06 — doc_env_var_names
# ---------------------------------------------------------------------------


def _run_c06(root: Path, truth: ShippedTruth) -> tuple[StaleClaim, ...]:
    check_id = "doc_env_var_names"
    items: list[tuple[int, int, StaleClaim]] = []
    documents = [_README, _INDEX] + [
        d for d in _guide_documents(root) if d != "docs/guides/environment.md"
    ]
    for order, document in enumerate(documents):
        text = _read(root, document)
        if text is None:
            continue
        for line_no, line in _iter_lines_outside_fences(text):
            for m in _REMEDY_VAR_RE.finditer(line):
                var = m.group(0)
                tail = line[m.end():m.end() + 2]
                if tail[:1] == "*":
                    continue
                if var.endswith("_"):
                    continue
                if tail[:1] == "." and len(tail) > 1 and tail[1].isalpha():
                    continue
                if var not in truth.env_vars:
                    items.append((order, line_no, StaleClaim(
                        check_id, document,
                        f"names the variable `{var}`",
                        f"`{var}` is not a registered environment variable",
                    )))
    return _sorted_claims(items)


# ---------------------------------------------------------------------------
# C07 — doc_config_keys
# ---------------------------------------------------------------------------


def _run_c07(root: Path, truth: ShippedTruth) -> tuple[StaleClaim, ...]:
    check_id = "doc_config_keys"
    items: list[tuple[int, int, StaleClaim]] = []
    prefixes = truth.key_prefixes
    documents = [_README, _INDEX] + _guide_documents(root)
    for order, document in enumerate(documents):
        text = _read(root, document)
        if text is None:
            continue
        for line_no, line in _iter_lines_outside_fences(text):
            for m in _SPAN_RE.finditer(line):
                span = m.group(1)
                if not _KEY_NAME_WHOLE_RE.match(span):
                    continue
                first = span.split(".", 1)[0]
                if first not in prefixes:
                    continue
                if span in truth.command_ids:
                    continue
                if span not in truth.config_keys:
                    items.append((order, line_no, StaleClaim(
                        check_id, document,
                        f"backticks the config key `{span}`",
                        f"`{span}` is not a registered config key",
                    )))
    return _sorted_claims(items)


# ---------------------------------------------------------------------------
# C08 — toml_fenced_block_keys
# ---------------------------------------------------------------------------


def _run_c08(root: Path, truth: ShippedTruth) -> tuple[StaleClaim, ...]:
    check_id = "toml_fenced_block_keys"
    items: list[tuple[int, int, StaleClaim]] = []
    for order, document in enumerate(_guide_documents(root)):
        text = _read(root, document)
        if text is None:
            continue
        for block_lines, start_line in _toml_fence_blocks(text):
            prefix: str | None = None
            for offset, line in enumerate(block_lines):
                line_no = start_line + offset
                stripped = line.strip()
                table = _TOML_TABLE_RE.match(stripped)
                if table:
                    table_name = table.group(1).strip()
                    if table_name == "remedy":
                        prefix = ""
                    elif table_name.startswith("remedy."):
                        prefix = table_name[len("remedy."):]
                    else:
                        prefix = None
                    continue
                kv = _TOML_KV_RE.match(stripped)
                if kv and prefix is not None:
                    name = kv.group(1)
                    full_key = f"{prefix}.{name}" if prefix else name
                    if full_key not in truth.config_keys:
                        items.append((order, line_no, StaleClaim(
                            check_id, document,
                            f"a TOML example sets `{full_key}`",
                            f"`{full_key}` is not a registered config key",
                        )))
    return _sorted_claims(items)


# ---------------------------------------------------------------------------
# C09 — docs_index_type_column
# ---------------------------------------------------------------------------


def _run_c09(root: Path, truth: ShippedTruth) -> tuple[StaleClaim, ...]:
    check_id = "docs_index_type_column"
    text = _read(root, _INDEX)
    if text is None:
        return ()
    bounds = _section_bounds(text, "## Quick-Find Table", exact=True)
    if bounds is None:
        return ()
    lines = [line for _, line in _section_lines_outside_fences(text, bounds)]
    items: list[tuple[int, int, StaleClaim]] = []
    for row_no, cells in enumerate(_table_rows(lines)):
        if len(cells) < 3:
            continue
        category = cells[2]
        for m in _LINK_RE.finditer(cells[1]):
            target = m.group(1)
            folder = target.split("/", 1)[0]
            expected = "guide" if folder == "guides" else folder
            if expected != category:
                items.append((0, row_no, StaleClaim(
                    check_id, _INDEX,
                    f"the Quick-Find Table row linking `{target}` names its category `{category}`",
                    f"the link's folder is `{folder}`, written `{expected}`",
                )))
    return _sorted_claims(items)


# ---------------------------------------------------------------------------
# C10 — doc_source_paths
# ---------------------------------------------------------------------------


def _run_c10(root: Path, truth: ShippedTruth) -> tuple[StaleClaim, ...]:
    check_id = "doc_source_paths"
    items: list[tuple[int, int, StaleClaim]] = []
    for order, document in enumerate([_README, _INDEX]):
        text = _read(root, document)
        if text is None:
            continue
        for line_no, line in _iter_lines_outside_fences(text):
            for m in _SOURCE_PATH_RE.finditer(line):
                candidate = m.group(0)
                if not (root / candidate).is_file():
                    items.append((order, line_no, StaleClaim(
                        check_id, document,
                        f"names the path `{candidate}`",
                        f"`{candidate}` does not exist under the repository root",
                    )))
    return _sorted_claims(items)


# ---------------------------------------------------------------------------
# C11 — doc_dotted_command_ids
# ---------------------------------------------------------------------------


def _run_c11(root: Path, truth: ShippedTruth) -> tuple[StaleClaim, ...]:
    check_id = "doc_dotted_command_ids"
    items: list[tuple[int, int, StaleClaim]] = []
    prefixes = truth.key_prefixes
    documents = [_README, _INDEX] + _guide_documents(root)
    for order, document in enumerate(documents):
        text = _read(root, document)
        if text is None:
            continue
        for line_no, line in _iter_lines_outside_fences(text):
            for m in _SPAN_RE.finditer(line):
                span = m.group(1)
                if not _TWO_SEGMENT_WHOLE_RE.match(span):
                    continue
                first, sub = span.split(".", 1)
                group_id = truth.groups.get(first)
                if group_id is None or first in prefixes:
                    continue
                command_id = f"{group_id}.{sub}"
                if command_id not in truth.command_ids:
                    items.append((order, line_no, StaleClaim(
                        check_id, document,
                        f"backticks the command `{span}`",
                        f"`{command_id}` does not ship",
                    )))
    return _sorted_claims(items)


# ---------------------------------------------------------------------------
# C12 — catalog_text_config_keys
# ---------------------------------------------------------------------------

_CATALOG_MODULE_PATH = "apps/cli/command_catalog.py"


def _run_c12(root: Path, truth: ShippedTruth) -> tuple[StaleClaim, ...]:
    check_id = "catalog_text_config_keys"
    items: list[tuple[int, int, StaleClaim]] = []
    prefixes = truth.key_prefixes
    for order, (label, text) in enumerate(truth.catalog_texts):
        for m in _KEY_NAME_RE.finditer(text):
            start = m.start()
            if start > 0 and (text[start - 1].isalnum() or text[start - 1] in "_."):
                continue
            span = m.group(0)
            first = span.split(".", 1)[0]
            if first not in prefixes:
                continue
            if span in truth.command_ids:
                continue
            if span not in truth.config_keys:
                items.append((order, 0, StaleClaim(
                    check_id, _CATALOG_MODULE_PATH,
                    f"the text labelled `{label}` names `{span}`",
                    f"`{span}` is not a registered config key",
                )))
    return _sorted_claims(items)


# ---------------------------------------------------------------------------
# The catalog
# ---------------------------------------------------------------------------

CHECKS: tuple[StalenessCheck, ...] = (
    StalenessCheck(
        "docs_index_guide_registration", ("docs/README.md",),
        "reads every link target under the docs index's Quick-Find Table and Guides sections",
        "compares them against every shipped `docs/guides/*.md` file, both ways",
        _run_c01,
    ),
    StalenessCheck(
        "config_cli_table_complete", ("docs/guides/remedy-toml-user-guide.md",),
        "extracts the word after `remedy config ` from every backticked span in the CLI commands section",
        "compares the set against the `config` group's shipped subcommand pairs, both ways",
        _run_c02,
    ),
    StalenessCheck(
        "docs_index_command_lines", ("docs/README.md",),
        "reads the second and third words of every backticked `remedy `-prefixed span",
        "compares the second word against shipped group ids and aliases and the third against command pairs",
        _run_c03,
    ),
    StalenessCheck(
        "guide_relative_links", ("docs/guides/*.md",),
        "reads every relative markdown link target in a guide, its fragment removed",
        "resolves it against the guide's own folder and requires the file to exist",
        _run_c04,
    ),
    StalenessCheck(
        "link_anchors_resolve", ("README.md", "docs/README.md", "docs/guides/*.md"),
        "reads every relative link carrying a `#fragment` whose path is empty or ends in `.md`",
        "requires the fragment to equal the slug of a heading of the resolved target file",
        _run_c05,
    ),
    StalenessCheck(
        "doc_env_var_names", ("README.md", "docs/README.md", "docs/guides/*.md (except environment.md)"),
        "reads every `REMEDY_[A-Z0-9_]+` match not preceded by a word character, skipping wildcard and filename shapes",
        "compares each surviving match against the registered environment variable names",
        _run_c06,
    ),
    StalenessCheck(
        "doc_config_keys", ("README.md", "docs/README.md", "docs/guides/*.md"),
        "reads every backticked span that is a whole dotted key name whose first segment is a registered key prefix",
        "requires it to be a registered config key, unless it is a shipped command id instead",
        _run_c07,
    ),
    StalenessCheck(
        "toml_fenced_block_keys", ("docs/guides/*.md",),
        "reads `name = value` lines inside a ```toml fence under a `[remedy...]` table line",
        "requires the resulting dotted (or bare) key to be a registered config key",
        _run_c08,
    ),
    StalenessCheck(
        "docs_index_type_column", ("docs/README.md",),
        "reads the Quick-Find Table's third cell and every link target in its second cell",
        "requires the third cell to equal the link target's top folder, with `guides` written `guide`",
        _run_c09,
    ),
    StalenessCheck(
        "doc_source_paths", ("README.md", "docs/README.md"),
        "reads every `packages|apps|tests|scripts/...` source-shaped path not preceded by a word character or slash",
        "requires the named file to exist under the repository root",
        _run_c10,
    ),
    StalenessCheck(
        "doc_dotted_command_ids", ("README.md", "docs/README.md", "docs/guides/*.md"),
        "reads every backticked span that is a whole two-segment dotted name whose first segment is a group id and not a key prefix",
        "requires the resolved `group.subcommand` to be a shipped command id",
        _run_c11,
    ),
    StalenessCheck(
        "catalog_text_config_keys", (_CATALOG_MODULE_PATH,),
        "reads every dotted key name in a catalog description or help text whose first segment is a registered key prefix",
        "requires it to be a registered config key, unless it is a shipped command id instead",
        _run_c12,
    ),
)


def run_staleness_checks(
    root: Path | None = None, truth: ShippedTruth | None = None
) -> tuple[StaleClaim, ...]:
    """Every claim every check in :data:`CHECKS` finds, in catalog order.

    `root` defaults to the repository root and `truth` to :meth:`ShippedTruth.live`
    — a test overrides either to run the same checks against a fixture tree and
    an injected truth, never the real repository or the real catalog.
    """
    resolved_root = root if root is not None else Path(__file__).resolve().parents[2]
    resolved_truth = truth if truth is not None else ShippedTruth.live()
    claims: list[StaleClaim] = []
    for check in CHECKS:
        claims.extend(check.run(resolved_root, resolved_truth))
    return tuple(claims)
