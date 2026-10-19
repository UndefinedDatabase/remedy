"""exec-1018c — `docs/system/api-release-matrix-v1.json` is the public surface the code offers, version by version.

The release of PRs 360-364 moves the public API and the machine client interface from 1.17 to 1.21.
The matrix lists every route, story key, story word and order phase with the version that added it,
and the value changes of existing fields per version. These tests hold it to the code: nothing the
code offers is missing from it, nothing it lists is gone, and its current version is the code's.
"""
from __future__ import annotations

import json
from pathlib import Path

from apps.cli.client_interface import CLIENT_INTERFACE_VERSION
from apps.cli.client_interface_story import CLIENT_STORY_ANSWER_KEYS
from packages.orchestration.client_story_words import story_words
from packages.orchestration.order_cancel import ORDER_PHASES
from packages.orchestration.order_jobs import ORDER_JOB_PHASES
from packages.orchestration.public_api import PUBLIC_API_VERSION
from packages.orchestration.public_api_routes import PUBLIC_API_ROUTES

MATRIX = json.loads((Path(__file__).resolve().parents[2] / "docs" / "system" / "api-release-matrix-v1.json")
                    .read_text(encoding="utf-8"))


def _version(text: str) -> tuple[int, ...]:
    return tuple(int(part) for part in text.split("."))


def _code_inventory() -> dict[str, set[str]]:
    found = {"routes": {f"{r.method} {r.path}" for r in PUBLIC_API_ROUTES},
             "story_keys": set(CLIENT_STORY_ANSWER_KEYS), "order_phases": set(ORDER_PHASES),
             "order_job_phases": set(ORDER_JOB_PHASES)}
    for key, words in story_words().items():
        found[f"story.{key}"] = set(words)
    return found


def test_the_matrix_lists_exactly_what_the_code_offers():
    listed = {category: set(items) for category, items in MATRIX["inventory"].items()}
    assert listed == _code_inventory(), "record each addition in docs/system/api-release-matrix-v1.json"


def test_the_current_version_is_the_codes_and_every_item_names_a_version_of_the_matrix():
    assert MATRIX["current"] == PUBLIC_API_VERSION == CLIENT_INTERFACE_VERSION
    known = {MATRIX["baseline"], *(entry["version"] for entry in MATRIX["versions"])}
    for category, items in MATRIX["inventory"].items():
        for item, since in items.items():
            assert since in known and _version(since) <= _version(MATRIX["current"]), (category, item, since)


def test_the_versions_only_grow_and_each_names_what_it_changed():
    versions = [entry["version"] for entry in MATRIX["versions"]]
    assert versions == sorted(versions, key=_version) and versions[-1] == MATRIX["current"]
    for entry in MATRIX["versions"]:
        assert entry["added"] or entry["value_changes"], entry
        for change in entry["value_changes"]:
            assert {"field", "case", "before", "after"} <= set(change), change
