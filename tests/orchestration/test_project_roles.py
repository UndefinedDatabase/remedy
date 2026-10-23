"""R-1326, DECISION F314 D4 — the project's own `[roles]` table of `.remedy/config.toml`.

One test per answer `read_project_roles` can give, and one per refusal it raises. Every test
writes its own `.remedy/config.toml` under `tmp_path`; none drives a job or a provider.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from packages.orchestration.project_roles import (
    PROJECT_ROLES_KEYS,
    ProjectRolesError,
    read_project_roles,
)


def _write_config(repo_root: Path, body: str) -> Path:
    conf = repo_root / ".remedy"
    conf.mkdir(parents=True, exist_ok=True)
    path = conf / "config.toml"
    path.write_text(body, encoding="utf-8")
    return path


class TestTheAnswers:
    def test_an_absent_file_answers_empty(self, tmp_path: Path) -> None:
        assert read_project_roles(tmp_path) == {}

    def test_a_file_with_no_roles_table_answers_empty(self, tmp_path: Path) -> None:
        _write_config(tmp_path, '[runtime]\ncmd = ["npm", "run", "dev"]\n')
        assert read_project_roles(tmp_path) == {}

    def test_all_three_keys_are_read(self, tmp_path: Path) -> None:
        _write_config(
            tmp_path,
            '[roles]\nbuilder = "claude-cli"\nreviewer = "fake"\nplanner = "ollama"\n',
        )
        assert read_project_roles(tmp_path) == {
            "builder": "claude-cli", "reviewer": "fake", "planner": "ollama"}


class TestTheRefusals:
    def test_a_file_that_is_not_readable_toml_is_refused(self, tmp_path: Path) -> None:
        _write_config(tmp_path, "not valid toml ][")
        with pytest.raises(ProjectRolesError, match=r"\.remedy/config\.toml"):
            read_project_roles(tmp_path)

    def test_a_roles_value_that_is_not_a_table_is_refused(self, tmp_path: Path) -> None:
        _write_config(tmp_path, 'roles = "x"\n')
        with pytest.raises(ProjectRolesError, match=r"\[roles\] must be a table"):
            read_project_roles(tmp_path)

    def test_an_unknown_key_is_refused(self, tmp_path: Path) -> None:
        assert "bogus" not in PROJECT_ROLES_KEYS
        _write_config(tmp_path, '[roles]\nbogus = "x"\n')
        with pytest.raises(ProjectRolesError, match=r"\[roles\] names 'bogus'"):
            read_project_roles(tmp_path)

    def test_a_value_that_is_not_a_non_empty_string_is_refused(self, tmp_path: Path) -> None:
        _write_config(tmp_path, "[roles]\nbuilder = 5\n")
        with pytest.raises(ProjectRolesError, match="non-empty string"):
            read_project_roles(tmp_path)

    def test_an_empty_string_value_is_refused(self, tmp_path: Path) -> None:
        _write_config(tmp_path, '[roles]\nbuilder = ""\n')
        with pytest.raises(ProjectRolesError, match="non-empty string"):
            read_project_roles(tmp_path)

    def test_a_builder_outside_the_role_provider_names_is_refused(self, tmp_path: Path) -> None:
        _write_config(tmp_path, '[roles]\nbuilder = "bogus"\n')
        with pytest.raises(ProjectRolesError, match="which is not a provider"):
            read_project_roles(tmp_path)

    def test_a_reviewer_outside_the_role_provider_names_is_refused(self, tmp_path: Path) -> None:
        _write_config(tmp_path, '[roles]\nreviewer = "bogus"\n')
        with pytest.raises(ProjectRolesError, match="which is not a provider"):
            read_project_roles(tmp_path)

    def test_a_builder_that_cannot_write_files_is_refused(self, tmp_path: Path) -> None:
        _write_config(tmp_path, '[roles]\nbuilder = "ollama"\n')
        with pytest.raises(ProjectRolesError, match="cannot write files"):
            read_project_roles(tmp_path)

    def test_a_planner_outside_the_planner_providers_is_refused(self, tmp_path: Path) -> None:
        _write_config(tmp_path, '[roles]\nplanner = "fake"\n')
        with pytest.raises(ProjectRolesError, match="which is not a planner"):
            read_project_roles(tmp_path)
