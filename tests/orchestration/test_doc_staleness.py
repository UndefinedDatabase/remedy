"""T5_F289 T001 (DECISION F289 D2) — tests for the documentation-staleness catalog.

Every check gets a STALE fixture (proves the check catches the defect it exists
for, with all four `StaleClaim` fields asserted) and a FRESH fixture (proves it
does not fire on a clean tree carrying that check's own exemptions). All
fixtures build their own root under `tmp_path` and their own `ShippedTruth`,
except :class:`TestAgainstTheRealTree`, which runs against the real repository
and the real, live catalog.
"""
from __future__ import annotations

from pathlib import Path

from packages.orchestration.doc_staleness import (
    CHECKS,
    ShippedTruth,
    StaleClaim,
    run_staleness_checks,
)

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


def _truth(**overrides) -> ShippedTruth:
    """A small, self-consistent `ShippedTruth` a test overrides piecewise."""
    defaults: dict = dict(
        groups={"job": "job", "config": "config", "settings": "config"},
        command_pairs=frozenset({
            ("job", "run"), ("job", "show"),
            ("config", "list"), ("config", "get"), ("config", "set"),
        }),
        command_ids=frozenset({
            "job.run", "job.show", "config.list", "config.get", "config.set",
        }),
        config_keys=frozenset({"data_dir", "ollama.host", "ollama.model"}),
        env_vars=frozenset({"REMEDY_DATA_DIR", "REMEDY_OLLAMA_HOST"}),
        catalog_texts=(("job.run description", "Run a job."),),
    )
    defaults.update(overrides)
    return ShippedTruth(**defaults)


def _write(root: Path, relpath: str, text: str) -> Path:
    path = root / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _fields(claim: StaleClaim) -> tuple[str, str, str, str]:
    return (claim.check_id, claim.document, claim.claim, claim.truth)


def _claims_for(root: Path, truth: ShippedTruth, check_id: str) -> list[StaleClaim]:
    """Only `check_id`'s own claims — every fixture's root is read by all twelve
    checks at once, and a fixture built to exercise one check may incidentally
    satisfy another's pattern (e.g. `docs/README.md` is every INDEX-reading
    check's document). Isolating by id keeps each test about its own check."""
    return [c for c in run_staleness_checks(root, truth) if c.check_id == check_id]


# ---------------------------------------------------------------------------
# C01 — docs_index_guide_registration
# ---------------------------------------------------------------------------


class TestC01DocsIndexGuideRegistration:
    def test_stale(self, tmp_path: Path):
        _write(tmp_path, "docs/guides/alpha.md", "# Alpha\n")
        _write(tmp_path, "docs/guides/beta.md", "# Beta\n")
        _write(tmp_path, "docs/README.md", (
            "# Index\n\n"
            "## Quick-Find Table\n\n"
            "| Keyword | File | Category |\n"
            "|---|---|---|\n"
            "| beta | [beta.md](guides/beta.md) | guide |\n"
            "| ghost | [ghost.md](guides/ghost.md) | guide |\n\n"
            "## Guides\n\n"
            "| File | Description |\n"
            "|---|---|\n"
            "| [alpha.md](guides/alpha.md) | Alpha guide |\n"
        ))
        claims = _claims_for(tmp_path, _truth(), "docs_index_guide_registration")
        assert [_fields(c) for c in claims] == [
            (
                "docs_index_guide_registration", "docs/README.md",
                "the Quick-Find Table has no link to `guides/alpha.md`",
                "`docs/guides/alpha.md` ships",
            ),
            (
                "docs_index_guide_registration", "docs/README.md",
                "the Guides section has no link to `guides/beta.md`",
                "`docs/guides/beta.md` ships",
            ),
            (
                "docs_index_guide_registration", "docs/README.md",
                "the Quick-Find Table section links `guides/ghost.md`",
                "`docs/guides/ghost.md` does not exist",
            ),
        ]

    def test_fresh(self, tmp_path: Path):
        _write(tmp_path, "docs/guides/alpha.md", "# Alpha\n")
        _write(tmp_path, "docs/README.md", (
            "# Index\n\n"
            "## Quick-Find Table\n\n"
            "| Keyword | File | Category |\n"
            "|---|---|---|\n"
            "| alpha | [alpha.md](guides/alpha.md) | guide |\n\n"
            "## Guides\n\n"
            "| File | Description |\n"
            "|---|---|\n"
            "| [alpha.md](guides/alpha.md) | Alpha guide |\n\n"
            "A fenced example of the stale shape, skipped entirely:\n"
            "```\n"
            "| ghost | [ghost.md](guides/ghost.md) | guide |\n"
            "```\n"
            "## Other\n\nNothing here.\n"
        ))
        assert _claims_for(tmp_path, _truth(), "docs_index_guide_registration") == []


# ---------------------------------------------------------------------------
# C02 — config_cli_table_complete
# ---------------------------------------------------------------------------


class TestC02ConfigCliTableComplete:
    def test_stale(self, tmp_path: Path):
        _write(tmp_path, "docs/guides/remedy-toml-user-guide.md", (
            "# Guide\n\n"
            "## CLI commands\n\n"
            "| Command | Description |\n"
            "|---|---|\n"
            "| `remedy config list` | List keys |\n"
            "| `remedy config wipe` | Not shipped |\n\n"
            "## Next\n\nMore text.\n"
        ))
        claims = _claims_for(tmp_path, _truth(), "config_cli_table_complete")
        assert [_fields(c) for c in claims] == [
            (
                "config_cli_table_complete", "docs/guides/remedy-toml-user-guide.md",
                "documents `remedy config wipe`",
                "the `config` group ships no `wipe` subcommand",
            ),
            (
                "config_cli_table_complete", "docs/guides/remedy-toml-user-guide.md",
                "the CLI commands table never documents `remedy config get`",
                "`remedy config get` ships",
            ),
            (
                "config_cli_table_complete", "docs/guides/remedy-toml-user-guide.md",
                "the CLI commands table never documents `remedy config set`",
                "`remedy config set` ships",
            ),
        ]

    def test_fresh(self, tmp_path: Path):
        _write(tmp_path, "docs/guides/remedy-toml-user-guide.md", (
            "# Guide\n\n"
            "## CLI commands\n\n"
            "| Command | Description |\n"
            "|---|---|\n"
            "| `remedy config list` | List keys |\n"
            "| `remedy config get <key>` | Get one key |\n"
            "| `remedy config set <key> <value>` | Set one key |\n\n"
            "A fenced example of the stale shape, skipped entirely:\n"
            "```\n"
            "`remedy config wipe`\n"
            "```\n"
            "## Next\n\nMore text.\n"
        ))
        assert _claims_for(tmp_path, _truth(), "config_cli_table_complete") == []


# ---------------------------------------------------------------------------
# C03 — docs_index_command_lines
# ---------------------------------------------------------------------------


class TestC03DocsIndexCommandLines:
    def test_stale(self, tmp_path: Path):
        _write(tmp_path, "docs/README.md", (
            "# Index\n\n"
            "Run `remedy widget fly` to see the crash, or `remedy job dance` for "
            "another one.\n"
        ))
        claims = _claims_for(tmp_path, _truth(), "docs_index_command_lines")
        assert [_fields(c) for c in claims] == [
            (
                "docs_index_command_lines", "docs/README.md",
                "`remedy widget fly` names the group `widget`",
                "no group `widget` ships",
            ),
            (
                "docs_index_command_lines", "docs/README.md",
                "`remedy job dance` names `job dance`",
                "`job` ships no `dance` subcommand",
            ),
        ]

    def test_fresh(self, tmp_path: Path):
        _write(tmp_path, "docs/README.md", (
            "# Index\n\n"
            "Run `remedy job run` to start a job. A placeholder line: "
            "`remedy <group> <sub>` names no real group.\n\n"
            "A fenced example of the stale shape, skipped entirely:\n"
            "```\n"
            "`remedy job dance`\n"
            "```\n"
        ))
        assert _claims_for(tmp_path, _truth(), "docs_index_command_lines") == []


# ---------------------------------------------------------------------------
# C04 — guide_relative_links
# ---------------------------------------------------------------------------


class TestC04GuideRelativeLinks:
    def test_stale(self, tmp_path: Path):
        _write(tmp_path, "docs/guides/alpha.md", (
            "# Alpha\n\nSee [missing](missing-file.md) for more.\n"
        ))
        claims = _claims_for(tmp_path, _truth(), "guide_relative_links")
        assert [_fields(c) for c in claims] == [
            (
                "guide_relative_links", "docs/guides/alpha.md",
                "links `missing-file.md`",
                "`missing-file.md` does not resolve against `docs/guides/alpha.md`'s own folder",
            ),
        ]

    def test_fresh(self, tmp_path: Path):
        _write(tmp_path, "docs/guides/other.md", "# Other\n")
        _write(tmp_path, "docs/guides/alpha.md", (
            "# Alpha\n\nSee [other](other.md) and [external](https://example.com/x) "
            "and [anchor](#alpha).\n\n"
            "A fenced example of the stale shape, skipped entirely:\n"
            "```\n"
            "[missing](nope.md)\n"
            "```\n"
        ))
        assert _claims_for(tmp_path, _truth(), "guide_relative_links") == []


# ---------------------------------------------------------------------------
# C05 — link_anchors_resolve
# ---------------------------------------------------------------------------


class TestC05LinkAnchorsResolve:
    def test_stale(self, tmp_path: Path):
        _write(tmp_path, "README.md", (
            "# Remedy\n\nSee [section](#no-such-heading).\n\n## Real Heading\n"
        ))
        claims = _claims_for(tmp_path, _truth(), "link_anchors_resolve")
        assert [_fields(c) for c in claims] == [
            (
                "link_anchors_resolve", "README.md",
                "links `#no-such-heading`",
                "no heading of `README.md` slugs to `no-such-heading`",
            ),
        ]

    def test_fresh(self, tmp_path: Path):
        _write(tmp_path, "README.md", (
            "# Remedy\n\nSee [real](#real-heading) and "
            "[external](https://example.com/x#no-such-heading) and "
            "[punctuated](#punctuated-heading).\n\n"
            "## Real Heading\n\n"
            "## Punctuated, Heading!\n\n"
            "A fenced example of the stale shape, skipped entirely:\n"
            "```\n"
            "[dead](#nope)\n"
            "```\n"
        ))
        assert _claims_for(tmp_path, _truth(), "link_anchors_resolve") == []


# ---------------------------------------------------------------------------
# C06 — doc_env_var_names
# ---------------------------------------------------------------------------


class TestC06DocEnvVarNames:
    def test_stale(self, tmp_path: Path):
        _write(tmp_path, "README.md", (
            "# Remedy\n\nSet `REMEDY_GHOST_VARIABLE` to enable the feature.\n"
        ))
        claims = _claims_for(tmp_path, _truth(), "doc_env_var_names")
        assert [_fields(c) for c in claims] == [
            (
                "doc_env_var_names", "README.md",
                "names the variable `REMEDY_GHOST_VARIABLE`",
                "`REMEDY_GHOST_VARIABLE` is not a registered environment variable",
            ),
        ]

    def test_fresh(self, tmp_path: Path):
        _write(tmp_path, "README.md", (
            "# Remedy\n\nSet `REMEDY_DATA_DIR`. Also see `REMEDY_OLLAMA_*` and "
            "`REMEDY_UI_REBUILD_SPEC.md`, and a wildcard on a name that does not "
            "itself end in an underscore: `REMEDY_UNKNOWN_TAIL*`.\n\n"
            "A fenced example of the stale shape, skipped entirely:\n"
            "```\n"
            "REMEDY_GHOST_VARIABLE\n"
            "```\n"
        ))
        # environment.md is exempt from this check entirely.
        _write(tmp_path, "docs/guides/environment.md", "REMEDY_ANOTHER_GHOST\n")
        assert _claims_for(tmp_path, _truth(), "doc_env_var_names") == []


# ---------------------------------------------------------------------------
# C07 — doc_config_keys
# ---------------------------------------------------------------------------


class TestC07DocConfigKeys:
    def test_stale(self, tmp_path: Path):
        _write(tmp_path, "README.md", (
            "# Remedy\n\nSet `ollama.ghost_key` in your config.\n"
        ))
        claims = _claims_for(tmp_path, _truth(), "doc_config_keys")
        assert [_fields(c) for c in claims] == [
            (
                "doc_config_keys", "README.md",
                "backticks the config key `ollama.ghost_key`",
                "`ollama.ghost_key` is not a registered config key",
            ),
        ]

    def test_fresh(self, tmp_path: Path):
        _write(tmp_path, "README.md", (
            "# Remedy\n\nSet `ollama.host` and `data_dir`. A file `remedy.toml` "
            "holds it. See also `job.run`, a command id and not a config key.\n\n"
            "A fenced example of the stale shape, skipped entirely:\n"
            "```\n"
            "`ollama.ghost_key`\n"
            "```\n"
        ))
        assert _claims_for(tmp_path, _truth(), "doc_config_keys") == []


# ---------------------------------------------------------------------------
# C08 — toml_fenced_block_keys
# ---------------------------------------------------------------------------


class TestC08TomlFencedBlockKeys:
    def test_stale(self, tmp_path: Path):
        _write(tmp_path, "docs/guides/alpha.md", (
            "# Alpha\n\n"
            "```toml\n"
            "[remedy]\n"
            "ghost_key = \"x\"\n\n"
            "[remedy.ollama]\n"
            "ghost_sub = 1\n"
            "```\n"
        ))
        claims = _claims_for(tmp_path, _truth(), "toml_fenced_block_keys")
        assert [_fields(c) for c in claims] == [
            (
                "toml_fenced_block_keys", "docs/guides/alpha.md",
                "a TOML example sets `ghost_key`",
                "`ghost_key` is not a registered config key",
            ),
            (
                "toml_fenced_block_keys", "docs/guides/alpha.md",
                "a TOML example sets `ollama.ghost_sub`",
                "`ollama.ghost_sub` is not a registered config key",
            ),
        ]

    def test_fresh(self, tmp_path: Path):
        _write(tmp_path, "docs/guides/alpha.md", (
            "# Alpha\n\n"
            "```toml\n"
            "[remedy]\n"
            "data_dir = \"x\"\n\n"
            "[remedy.ollama]\n"
            "host = \"y\"\n\n"
            "[other]\n"
            "ghost_key = \"ignored, reading is suspended\"\n"
            "```\n\n"
            "A fenced example of the stale shape, but NOT a toml fence, so it is "
            "not read by this check at all:\n"
            "```ini\n"
            "[remedy]\n"
            "ghost_key = \"x\"\n"
            "```\n"
        ))
        assert _claims_for(tmp_path, _truth(), "toml_fenced_block_keys") == []


# ---------------------------------------------------------------------------
# C09 — docs_index_type_column
# ---------------------------------------------------------------------------


class TestC09DocsIndexTypeColumn:
    def test_stale(self, tmp_path: Path):
        _write(tmp_path, "docs/README.md", (
            "# Index\n\n"
            "## Quick-Find Table\n\n"
            "| Keyword | File | Category |\n"
            "|---|---|---|\n"
            "| alpha | [alpha.md](guides/alpha.md) | system |\n"
            "| brain | [brain.md](system/brain.md) | guide |\n"
        ))
        claims = _claims_for(tmp_path, _truth(), "docs_index_type_column")
        assert [_fields(c) for c in claims] == [
            (
                "docs_index_type_column", "docs/README.md",
                "the Quick-Find Table row linking `guides/alpha.md` names its category `system`",
                "the link's folder is `guides`, written `guide`",
            ),
            (
                "docs_index_type_column", "docs/README.md",
                "the Quick-Find Table row linking `system/brain.md` names its category `guide`",
                "the link's folder is `system`, written `system`",
            ),
        ]

    def test_fresh(self, tmp_path: Path):
        _write(tmp_path, "docs/README.md", (
            "# Index\n\n"
            "## Quick-Find Table\n\n"
            "| Keyword | File | Category |\n"
            "|---|---|---|\n"
            "| alpha | [alpha.md](guides/alpha.md) | guide |\n"
            "| brain | [brain.md](system/brain.md) | system |\n\n"
            "A fenced example of the stale shape, skipped entirely:\n"
            "```\n"
            "| alpha | [alpha.md](guides/alpha.md) | system |\n"
            "```\n"
        ))
        assert _claims_for(tmp_path, _truth(), "docs_index_type_column") == []


# ---------------------------------------------------------------------------
# C10 — doc_source_paths
# ---------------------------------------------------------------------------


