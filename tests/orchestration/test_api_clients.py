"""The client tokens and the policy the operator writes (F253, DECISION F253 D16)."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pytest

from packages.orchestration.api_clients import (
    API_CLIENT_TOKEN_MIN_LENGTH,
    API_CLIENTS_FILE_NAME,
    ApiClient,
    api_clients_path,
    client_order_refusal,
    load_api_clients,
    match_api_client,
)

TOKEN_A = "a" * 40
TOKEN_B = "b" * 32


def _entry(**changes: Any) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "name": "alpha", "token": TOKEN_A, "projects": ["demo"],
        "max_total_tokens": 1000, "max_provider_calls": 5, "may_apply": False,
    }
    entry.update(changes)
    return entry


def _write(root: Path, content: Any, mode: int = 0o600) -> Path:
    path = api_clients_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = content if isinstance(content, str) else json.dumps(content)
    path.write_text(text, encoding="utf-8")
    os.chmod(path, mode)
    return path


def test_file_lives_beside_the_ledger(tmp_path: Path) -> None:
    assert api_clients_path(tmp_path) == tmp_path / "api" / API_CLIENTS_FILE_NAME
    assert API_CLIENT_TOKEN_MIN_LENGTH == 32


def test_well_formed_file_loads_both_clients_in_order(tmp_path: Path) -> None:
    _write(tmp_path, {"clients": [
        _entry(),
        _entry(name="beta", token=TOKEN_B, projects=["x", "y"], max_total_tokens=None,
               max_provider_calls=None, may_apply=True),
    ]})
    first, second = load_api_clients(tmp_path)
    assert first == ApiClient(name="alpha", token=TOKEN_A, projects=("demo",),
                              max_total_tokens=1000, max_provider_calls=5, may_apply=False)
    assert second == ApiClient(name="beta", token=TOKEN_B, projects=("x", "y"),
                               max_total_tokens=None, max_provider_calls=None, may_apply=True)
    assert TOKEN_A not in repr(first)
    assert TOKEN_B not in repr(second)


def test_missing_file_loads_no_client(tmp_path: Path) -> None:
    assert load_api_clients(tmp_path) == ()


@pytest.mark.parametrize("mode", [0o640, 0o604, 0o660, 0o602])
def test_file_others_may_read_or_write_loads_no_client(tmp_path: Path, mode: int) -> None:
    _write(tmp_path, {"clients": [_entry()]}, mode=mode)
    assert load_api_clients(tmp_path) == ()


def test_file_that_is_not_utf8_loads_no_client(tmp_path: Path) -> None:
    path = _write(tmp_path, "{}")
    path.write_bytes(b"\xff\xfe\x00")
    assert load_api_clients(tmp_path) == ()


def test_clients_path_that_is_a_folder_loads_no_client(tmp_path: Path) -> None:
    api_clients_path(tmp_path).mkdir(parents=True, mode=0o700)
    assert load_api_clients(tmp_path) == ()


def _without(key: str) -> dict[str, Any]:
    entry = _entry()
    del entry[key]
    return {"clients": [entry]}


_BROKEN_FILES: list[tuple[str, Any]] = [
    ("not-json", "this is not json"),
    ("list-at-top", [_entry()]),
    ("second-top-key", {"clients": [_entry()], "extra": 1}),
    ("clients-not-list", {"clients": {"name": "alpha"}}),
    ("entry-not-object", {"clients": ["alpha"]}),
    *[(f"missing-{key}", _without(key)) for key in
      ("name", "token", "projects", "max_total_tokens", "max_provider_calls", "may_apply")],
    ("seventh-key", {"clients": [_entry(extra=1)]}),
    ("empty-name", {"clients": [_entry(name="")]}),
    ("short-token", {"clients": [_entry(token="t" * 31)]}),
    ("token-not-string", {"clients": [_entry(token=12345678901234567890123456789012)]}),
    ("projects-not-list", {"clients": [_entry(projects="demo")]}),
    ("projects-empty-string", {"clients": [_entry(projects=[""])]}),
    ("ceiling-zero", {"clients": [_entry(max_total_tokens=0)]}),
    ("ceiling-negative", {"clients": [_entry(max_provider_calls=-1)]}),
    ("ceiling-true", {"clients": [_entry(max_total_tokens=True)]}),
    ("ceiling-string", {"clients": [_entry(max_provider_calls="5")]}),
    ("ceiling-float", {"clients": [_entry(max_total_tokens=1.5)]}),
    ("may-apply-string", {"clients": [_entry(may_apply="yes")]}),
    ("one-name-twice", {"clients": [_entry(), _entry(token=TOKEN_B)]}),
    ("one-token-twice", {"clients": [_entry(), _entry(name="beta")]}),
]


@pytest.mark.parametrize("content", [c for _, c in _BROKEN_FILES],
                         ids=[i for i, _ in _BROKEN_FILES])
def test_file_outside_the_shape_loads_no_client(tmp_path: Path, content: Any) -> None:
    _write(tmp_path, content)
    assert load_api_clients(tmp_path) == ()


def test_one_broken_entry_voids_the_whole_file(tmp_path: Path) -> None:
    _write(tmp_path, {"clients": [_entry(), _entry(name="beta", token="short")]})
    assert load_api_clients(tmp_path) == ()


def test_match_returns_the_client_of_the_right_token_only(tmp_path: Path) -> None:
    _write(tmp_path, {"clients": [_entry(), _entry(name="beta", token=TOKEN_B)]})
    clients = load_api_clients(tmp_path)
    matched = match_api_client(TOKEN_B, clients)
    assert matched is not None and matched.name == "beta"
    assert match_api_client(TOKEN_A, clients).name == "alpha"  # type: ignore[union-attr]
    assert match_api_client("c" * 40, clients) is None
    assert match_api_client(TOKEN_A[:-1], clients) is None
    assert match_api_client("", clients) is None
    assert match_api_client("é" * 40, clients) is None
    assert match_api_client(TOKEN_A, ()) is None


def _client(**changes: Any) -> ApiClient:
    fields: dict[str, Any] = {
        "name": "alpha", "token": TOKEN_A, "projects": ("demo", "0000-id"),
        "max_total_tokens": None, "max_provider_calls": None, "may_apply": False,
    }
    fields.update(changes)
    return ApiClient(**fields)


def test_order_for_an_unlisted_project_is_refused() -> None:
    sentence = client_order_refusal(_client(), ("other", "9999-id"), None, None)
    assert sentence is not None
    assert "alpha" in sentence and sentence.endswith("; nothing was run")


def test_order_for_a_project_listed_by_slug_or_by_id_is_inside() -> None:
    assert client_order_refusal(_client(), ("demo", "9999-id"), None, None) is None
    assert client_order_refusal(_client(), ("", "0000-id"), None, None) is None


@pytest.mark.parametrize("key,ceiling_field,cap_position", [
    ("max-total-tokens:", "max_total_tokens", 0),
    ("max-provider-calls:", "max_provider_calls", 1),
])
def test_cap_outside_a_ceiling_is_refused_naming_its_header_key(
        key: str, ceiling_field: str, cap_position: int) -> None:
    client = _client(**{ceiling_field: 1000})

    def refusal(cap: str | None) -> str | None:
        caps: list[str | None] = [None, None]
        caps[cap_position] = cap
        return client_order_refusal(client, ("demo",), caps[0], caps[1])

    for bad in (None, "1001", "0", "abc"):
        sentence = refusal(bad)
        assert sentence is not None, bad
        assert key in sentence and "alpha" in sentence
        assert sentence.endswith("; nothing was run")
    assert refusal("1000") is None
    assert refusal("999") is None


def test_no_ceiling_and_no_caps_is_inside() -> None:
    assert client_order_refusal(_client(), ("demo",), None, None) is None
