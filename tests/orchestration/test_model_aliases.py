"""Tests for packages.orchestration.model_aliases — the built-in model alias table.

Covers the table's own contract (resolution, loud failure, sorted accessors) and
the F254 RELOCATION: the ids role_config.py, pingpong_provider.py, config.py's
key registry and the two Ollama providers hand out must be exactly the ones the
alias table holds. Pure in-process assertions — no network, no
ANTHROPIC_API_KEY, no config file, no environment variable.
"""
from __future__ import annotations

import ast
import inspect
from pathlib import Path

import pytest

from packages.orchestration import config, pingpong_provider, role_config
from packages.orchestration.model_aliases import (
    MODEL_ALIASES,
    builtin_model_ids,
    known_model_aliases,
    resolve_model_alias,
)


class TestResolveModelAlias:
    def test_table_is_not_empty(self):
        assert MODEL_ALIASES

    @pytest.mark.parametrize("alias", sorted(MODEL_ALIASES))
    def test_every_alias_resolves_to_a_non_empty_id(self, alias):
        resolved = resolve_model_alias(alias)
        assert isinstance(resolved, str)
        assert resolved
        assert resolved == MODEL_ALIASES[alias]

    def test_unknown_alias_raises_key_error_naming_the_alias(self):
        with pytest.raises(KeyError) as excinfo:
            resolve_model_alias("claude-nonexistent")
        message = str(excinfo.value)
        assert "claude-nonexistent" in message

    def test_unknown_alias_message_lists_the_known_aliases(self):
        with pytest.raises(KeyError) as excinfo:
            resolve_model_alias("claude-nonexistent")
        message = str(excinfo.value)
        for alias in known_model_aliases():
            assert alias in message

    def test_unknown_alias_never_falls_back_to_a_guess(self):
        # Failing loud is the point: a silent fallback would ship a model
        # nobody chose, which is the drift the table exists to stop.
        with pytest.raises(KeyError):
            resolve_model_alias("")


class TestAccessors:
    def test_known_model_aliases_are_sorted(self):
        aliases = known_model_aliases()
        assert list(aliases) == sorted(aliases)

    def test_known_model_aliases_cover_the_table(self):
        assert set(known_model_aliases()) == set(MODEL_ALIASES)

    def test_builtin_model_ids_are_sorted(self):
        ids = builtin_model_ids()
        assert list(ids) == sorted(ids)

    def test_builtin_model_ids_have_no_duplicates(self):
        ids = builtin_model_ids()
        assert len(ids) == len(set(ids))

    def test_builtin_model_ids_cover_every_value(self):
        assert set(builtin_model_ids()) == set(MODEL_ALIASES.values())


class TestRelocationIsFaithful:
    """F254: relocating the ids must not change a single resolved value."""

    def test_provider_default_models_table(self):
        assert role_config._PROVIDER_DEFAULT_MODELS == {
            "ollama": resolve_model_alias("ollama-default"),
            "claude-cli": resolve_model_alias("claude-flagship"),
            "claude": resolve_model_alias("claude-flagship"),
            "fake": resolve_model_alias("fake"),
            "fixture": resolve_model_alias("fixture"),
        }

    def test_global_default_model_is_the_ollama_alias(self):
        assert role_config.DEFAULT_MODEL == resolve_model_alias("ollama-default")

    def test_claude_provider_signature_default(self):
        signature = inspect.signature(pingpong_provider.ClaudeProvider.__init__)
        default = signature.parameters["model"].default
        assert default == resolve_model_alias("claude-workhorse")

    def test_claude_provider_instance_uses_the_workhorse_alias(self):
        # Constructing the provider does no I/O: the SDK client is created
        # lazily, so this needs neither the network nor ANTHROPIC_API_KEY.
        provider = pingpong_provider.ClaudeProvider()
        assert provider._model == resolve_model_alias("claude-workhorse")

    def test_ollama_builder_default_model(self):
        # Imported inside the test: the provider module is optional runtime
        # surface (the `ollama` package is not a hard dependency), and the
        # import itself does no I/O.
        from packages.providers.ollama_builder import provider as ollama_builder

        assert ollama_builder._DEFAULT_MODEL == resolve_model_alias("ollama-default")

    def test_ollama_planner_default_model(self):
        from packages.providers.ollama_planner import provider as ollama_planner

        assert ollama_planner._DEFAULT_MODEL == resolve_model_alias("ollama-default")

    def test_ollama_model_config_key_default(self):
        # Looked up by KEY, never by position: the registry is a tuple and a
        # hardcoded index would silently point at another key once one is
        # inserted above it.
        spec = config.get_key_spec("ollama.model")
        assert spec is not None
        assert spec.default == resolve_model_alias("ollama-default")


# ---------------------------------------------------------------------------
# F254 acceptance criterion 2: no built-in model id outside the alias table
# ---------------------------------------------------------------------------

#: The one module allowed to spell a concrete id — it IS the table.
ALIAS_MODULE_RELPATH = "packages/orchestration/model_aliases.py"

#: Where the scan looks. Product code only; tests and scripts are free to name
#: an id, because pinning a value is what a test is for.
SCANNED_ROOTS = ("packages", "apps")

#: Directories that hold no reviewable source: compiled caches and the runtime
#: state tree Remedy writes under `.data/`.
SKIPPED_DIR_NAMES = frozenset({"__pycache__", ".data"})


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _python_sources() -> list[Path]:
    root = _repo_root()
    found: list[Path] = []
    for base in SCANNED_ROOTS:
        for path in sorted((root / base).rglob("*.py")):
            if SKIPPED_DIR_NAMES & set(path.relative_to(root).parts):
                continue
            found.append(path)
    return found


def _docstring_node_ids(tree: ast.AST) -> set[int]:
    """Identify the module/class/function docstrings so the scan can skip them.

    A docstring that quotes a default is DOCUMENTATION of that default, not the
    default itself (DECISION D11, docs/roadmap/features/T2_F254.md) — the alias
    module's own prose and any module explaining what it used to hardcode must
    stay legal.
    """
    docstrings: set[int] = set()
    holders = (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
    for node in ast.walk(tree):
        if not isinstance(node, holders):
            continue
        body = getattr(node, "body", None)
        if not body:
            continue
        first = body[0]
        if (isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)):
            docstrings.add(id(first.value))
    return docstrings


def _spelled_builtin_ids() -> list[tuple[str, int, str]]:
    """Every built-in model id spelled as a real string constant, with location.

    The scan parses with `ast` ON PURPOSE, and that choice is the mechanism
    behind the D11 boundary rather than a style preference: COMMENTS ARE
    INVISIBLE TO `ast` BY CONSTRUCTION — the parser discards them — so an
    illustrative id in a `#` comment can never be flagged, and no allow-list of
    line numbers has to be maintained to keep it that way. Do NOT "improve"
    this into a regex or a text search: that would lose the property, and the
    first comment mentioning an old id would go red.

    Docstrings are excluded explicitly (see :func:`_docstring_node_ids`) for
    the same reason, and sample-config prose in `.toml`/`.md` is never read
    because only `*.py` is walked.
    """
    root = _repo_root()
    builtin_ids = set(MODEL_ALIASES.values())
    offences: list[tuple[str, int, str]] = []
    for path in _python_sources():
        relpath = path.relative_to(root).as_posix()
        if relpath == ALIAS_MODULE_RELPATH:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        docstrings = _docstring_node_ids(tree)
        for node in ast.walk(tree):
            if (isinstance(node, ast.Constant)
                    and isinstance(node.value, str)
                    and id(node) not in docstrings
                    and node.value in builtin_ids):
                offences.append((relpath, node.lineno, node.value))
    return offences


class TestNoBuiltinModelIdOutsideTheAliasTable:
    """F254 acceptance: one table, and nothing else spells a concrete id.

    The Goal's binding reading is "every hardcoded default model id", dated or
    not (DECISION D11), so an undated id such as the Ollama default is in scope
    exactly like a May-2025 Claude id.
    """

    def test_scan_actually_reads_files(self):
        # A scan over an empty file list would pass forever. Pin that it found
        # real sources, and that the alias module was among them before it was
        # excluded by name.
        sources = _python_sources()
        assert len(sources) > 50
        relpaths = {p.relative_to(_repo_root()).as_posix() for p in sources}
        assert ALIAS_MODULE_RELPATH in relpaths

    def test_the_alias_table_holds_ids_the_scan_would_flag(self):
        # If the table were empty, or its values were blank, the scan below
        # would be vacuously green.
        assert MODEL_ALIASES
        assert all(v.strip() for v in MODEL_ALIASES.values())

    def test_no_builtin_model_id_is_spelled_outside_the_alias_module(self):
        offences = _spelled_builtin_ids()
        assert not offences, (
            "built-in model ids may only be spelled in "
            f"{ALIAS_MODULE_RELPATH}; import the alias and resolve it instead. "
            "Offending string constants:\n"
            + "\n".join(f"  {relpath}:{line}: {value!r}"
                        for relpath, line, value in sorted(offences))
        )
