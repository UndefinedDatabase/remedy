"""Every `REMEDY_*` name production code spells is a registered variable (T2_F279 T001).

DECISION F279 D2: the environment registry is the key registry of
`packages/orchestration/config.py` — one `ConfigKeySpec` per variable, carrying its type, its
default and its description — and not a second module beside it. These guards read the
production tree as SOURCE: a variable that is read, written, forwarded or named in a constant
must be registered, because a name nobody registered is a name nobody can validate, document
or report as a typo. The scan is over whole string literals, which also catches the names a
module keeps in a constant and reads through it (`PORT_ENV = "REMEDY_RUNTIME_PORT"`). The
shell scripts under `scripts/` and at the root read variables too (DECISION F279 D3), so every
`$REMEDY_*` and `${REMEDY_*` they expand is held to the same registry.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

from packages.orchestration.config import (
    all_key_specs,
    env_value,
    get_key_spec,
    unknown_env_variables,
    unparsable_env_variables,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SCANNED_ROOTS = ("packages", "apps", "scripts")
VARIABLE_NAME = re.compile(r"REMEDY_[A-Z0-9_]+")
ENV_READERS = frozenset({"get", "pop", "setdefault", "getenv"})
SHELL_EXPANSION = re.compile(r"\$\{?(REMEDY_[A-Z0-9_]+)")


def production_modules() -> list[Path]:
    modules: list[Path] = []
    for root in SCANNED_ROOTS:
        modules.extend(path for path in sorted((REPO_ROOT / root).rglob("*.py"))
                       if "node_modules" not in path.parts)
    return modules


def spelled_names(tree: ast.AST) -> set[str]:
    """Every whole string literal in `tree` that is a `REMEDY_*` variable name."""
    return {node.value for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
            and VARIABLE_NAME.fullmatch(node.value)}


def literal_env_reads(tree: ast.AST) -> set[str]:
    """The `REMEDY_*` literals passed straight to `os.environ[...]`, `.get`, `.pop`,
    `.setdefault` or `os.getenv` — T001's own wording of what the guard must hold."""
    names: set[str] = set()
    for node in ast.walk(tree):
        key = None
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Attribute) \
                and node.value.attr == "environ":
            key = node.slice
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.args \
                and node.func.attr in ENV_READERS:
            key = node.args[0]
        if isinstance(key, ast.Constant) and isinstance(key.value, str) \
                and VARIABLE_NAME.fullmatch(key.value):
            names.add(key.value)
    return names


def shell_scripts() -> list[Path]:
    return sorted([*(REPO_ROOT / "scripts").rglob("*.sh"), *REPO_ROOT.glob("*.sh")])


def module_constants(tree: ast.AST) -> dict[str, str]:
    """Module-level `NAME = "REMEDY_..."` assignments, so a read through a constant resolves."""
    return {node.targets[0].id: node.value.value for node in getattr(tree, "body", [])
            if isinstance(node, ast.Assign) and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name) and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str) and VARIABLE_NAME.fullmatch(node.value.value)}


def direct_env_reads(tree: ast.AST) -> set[str]:
    """The `REMEDY_*` names read straight off `os.environ` or `os.getenv`, through a literal or
    through a module-level constant."""
    constants = module_constants(tree)
    names: set[str] = set()
    for node in ast.walk(tree):
        key = None
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Attribute) \
                and node.value.attr == "environ" and isinstance(node.ctx, ast.Load):
            key = node.slice
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.args \
                and (node.func.attr == "getenv" or (node.func.attr in ENV_READERS
                                                     and isinstance(node.func.value, ast.Attribute)
                                                     and node.func.value.attr == "environ")):
            key = node.args[0]
        if isinstance(key, ast.Constant) and isinstance(key.value, str):
            names.add(key.value)
        elif isinstance(key, ast.Name) and key.id in constants:
            names.add(constants[key.id])
    return {name for name in names if VARIABLE_NAME.fullmatch(name)}


def registered_names() -> set[str]:
    return {spec.env_var for spec in all_key_specs()}


def scan(collect) -> dict[str, list[str]]:
    """name -> the modules that spell it, for every name `collect` finds and nobody registered."""
    registered = registered_names()
    unregistered: dict[str, list[str]] = {}
    for path in production_modules():
        for name in collect(ast.parse(path.read_text(encoding="utf-8"))):
            if name not in registered:
                unregistered.setdefault(name, []).append(str(path.relative_to(REPO_ROOT)))
    return unregistered


def test_the_scan_sees_the_production_tree():
    """A guard over an empty file list passes for every tree, so the list is measured first."""
    modules = production_modules()
    assert len(modules) > 100
    assert REPO_ROOT / "packages" / "orchestration" / "config.py" in modules


def test_every_literal_env_read_names_a_registered_variable():
    assert scan(literal_env_reads) == {}


def test_every_remedy_name_production_code_spells_is_registered():
    assert scan(spelled_names) == {}


def test_every_remedy_name_a_shell_script_expands_is_registered():
    scripts = shell_scripts()
    assert REPO_ROOT / "scripts" / "make_review_zip.sh" in scripts
    registered = registered_names()
    unregistered = {name: str(path.relative_to(REPO_ROOT)) for path in scripts
                    for name in SHELL_EXPANSION.findall(path.read_text(encoding="utf-8"))
                    if name not in registered}
    assert unregistered == {}


def test_every_registered_variable_is_a_remedy_name_and_registered_once():
    names = [spec.env_var for spec in all_key_specs()]
    assert [name for name in names if not VARIABLE_NAME.fullmatch(name)] == []
    assert len(names) == len(set(names))
    keys = [spec.key for spec in all_key_specs()]
    assert len(keys) == len(set(keys))


class TestTheEnvironmentAgainstTheRegistry:
    """The pure halves of `remedy doctor core`'s two environment warnings."""

    def test_an_unknown_name_is_named_with_its_closest_registered_match(self):
        found = unknown_env_variables({"REMEDY_UI_PROT": "8765", "PATH": "/bin"})
        assert found == [("REMEDY_UI_PROT", "REMEDY_UI_PORT")]

    def test_an_unknown_name_with_no_close_match_says_so(self):
        assert unknown_env_variables({"REMEDY_QQQQQQQQ": "1"}) == [("REMEDY_QQQQQQQQ", None)]

    def test_registered_names_and_other_prefixes_are_not_unknown(self):
        assert unknown_env_variables({"REMEDY_UI_PORT": "1", "HOME": "x", "XREMEDY_A": "1"}) == []

    def test_a_value_that_does_not_read_as_its_type_is_named(self):
        environ = {"REMEDY_UI_PORT": "eighty", "REMEDY_UI_DEMO_MODE": "on",
                   "REMEDY_BUDGET_MAX_COST_USD": "one", "REMEDY_UI_HOST": "anything"}
        found = [name for name, _spec in unparsable_env_variables(environ)]
        assert found == ["REMEDY_BUDGET_MAX_COST_USD", "REMEDY_UI_DEMO_MODE", "REMEDY_UI_PORT"]

    def test_values_that_read_as_their_type_are_not_named(self):
        environ = {"REMEDY_UI_PORT": "8765", "REMEDY_UI_DEMO_MODE": "yes",
                   "REMEDY_BUDGET_MAX_COST_USD": "1.5", "REMEDY_CLAUDE_ENABLED": "0"}
        assert unparsable_env_variables(environ) == []

    def test_a_table_valued_key_cannot_arrive_through_the_environment(self):
        spec = get_key_spec("model_routing.task_class_tiers")
        assert spec is not None and spec.value_type is dict
        assert [name for name, _ in unparsable_env_variables({spec.env_var: "x"})] == [spec.env_var]


#: The typed reads that stay direct, each with the reason the registry reader does not fit it
#: (DECISION F279 D4). `scripts/` is not scanned: its modules run as standalone scripts with
#: `scripts/` rather than the repository on `sys.path`, so they cannot import the registry.
DIRECT_TYPED_READS: dict[tuple[str, str], str] = {
    ("packages/runtimes/runtime_config.py", "REMEDY_RUNTIME_PORT"):
        "refuses a bad or out-of-range port with its own RuntimeConfigError, which callers catch",
    ("packages/runtimes/runtime_supervisor.py", "REMEDY_RUNTIME_PORT"):
        "the parent always sets it, and an unset port must fail the child at once",
}


def test_a_typed_variable_is_read_through_the_registry_reader():
    """A whole number, number or yes-or-no variable is parsed in one place, `env_value`."""
    typed = {spec.env_var for spec in all_key_specs() if spec.value_type is not str}
    found = set()
    for path in production_modules():
        rel = str(path.relative_to(REPO_ROOT))
        if rel.startswith("scripts/"):
            continue
        for name in direct_env_reads(ast.parse(path.read_text(encoding="utf-8"))) & typed:
            found.add((rel, name))
    assert found == set(DIRECT_TYPED_READS)


class TestTheRegistryReader:
    """`env_value`: the live environment, read as each variable's declared type."""

    def test_an_unset_env_only_variable_answers_its_spec_default(self):
        assert env_value("REMEDY_CLAUDE_PLANNER_TIMEOUT", {}) == 300
        assert env_value("REMEDY_UI_DEMO_MODE", {}) is False

    def test_an_unset_variable_remedy_toml_may_carry_answers_none(self):
        assert env_value("REMEDY_OLLAMA_BUILDER_TEMPERATURE", {}) is None
        assert env_value("REMEDY_UI_PORT", {}) is None

    def test_a_boolean_reads_yes_only_for_the_registered_words(self):
        for word in ("1", "true", "YES"):
            assert env_value("REMEDY_UI_DEMO_MODE", {"REMEDY_UI_DEMO_MODE": word}) is True
        for word in ("0", "", "no", "on"):
            assert env_value("REMEDY_UI_DEMO_MODE", {"REMEDY_UI_DEMO_MODE": word}) is False

    def test_numbers_are_parsed(self):
        assert env_value("REMEDY_UI_PORT", {"REMEDY_UI_PORT": "9000"}) == 9000
        temperature = env_value("REMEDY_OLLAMA_BUILDER_TEMPERATURE",
                                {"REMEDY_OLLAMA_BUILDER_TEMPERATURE": "0.25"})
        assert temperature == 0.25

    def test_a_number_that_does_not_parse_names_the_variable_and_its_type(self):
        with pytest.raises(ValueError, match="REMEDY_RUNTIME_LOG_MAX must be a whole number"):
            env_value("REMEDY_RUNTIME_LOG_MAX", {"REMEDY_RUNTIME_LOG_MAX": ""})

    def test_a_list_is_split_on_commas(self):
        assert env_value("REMEDY_SCOPE_ALLOW", {"REMEDY_SCOPE_ALLOW": "a/**, b ,"}) == ["a/**", "b"]

    def test_an_unregistered_name_is_refused(self):
        with pytest.raises(KeyError, match="REMEDY_NOT_A_REGISTERED_NAME"):
            env_value("REMEDY_NOT_A_REGISTERED_NAME", {})

    def test_the_live_environment_is_read_at_call_time(self, monkeypatch):
        monkeypatch.setenv("REMEDY_UI_DEMO_MODE", "1")
        assert env_value("REMEDY_UI_DEMO_MODE") is True
        monkeypatch.setenv("REMEDY_UI_DEMO_MODE", "0")
        assert env_value("REMEDY_UI_DEMO_MODE") is False
