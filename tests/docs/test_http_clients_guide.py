"""amend1015 Phase 1.3 — `docs/guides/http-clients.md` names only what the API really has.

Every route the guide calls is a registered route of `PUBLIC_API_ROUTES`, every placeholder is
one the guide declares, every refusal token it names is one the registry, a route's own text or
the machine client interface declares, and the double apply's 409 and the order key's 409 are both
written down. The guide's sequence itself runs in `tests/orchestration/test_do_then_story.py`.
"""
from __future__ import annotations

import re
from pathlib import Path

from apps.cli.client_interface import OPERATION_REFUSAL_TOKENS
from packages.orchestration.public_api_routes import PUBLIC_API_ROUTES

GUIDE = Path(__file__).resolve().parents[2] / "docs" / "guides" / "http-clients.md"
PLACEHOLDERS = {"port", "token", "project", "order", "job", "decision", "name", "why",
                "repository", "token of at least 32 characters"}
_CALL = re.compile(r"\b(GET|POST) (/api/v1/[^\s`]*)")
_CURL = re.compile(r"curl -s(?: -X (POST))? http://127\.0\.0\.1:<port>(/api/v1/[^\s\\]*)")


def _text() -> str:
    return GUIDE.read_text(encoding="utf-8")


def _registered(method: str, path: str) -> bool:
    for route in PUBLIC_API_ROUTES:
        pattern = "^" + re.sub(r"\{[a-z_]+\}", "<[a-z]+>", re.escape(route.path).replace(
            r"\{", "{").replace(r"\}", "}")) + "$"
        if route.method == method and re.match(pattern, path):
            return True
    return False


def test_every_route_the_guide_calls_is_registered():
    text = _text()
    calls = {(m, p) for m, p in _CALL.findall(text)}
    calls |= {(m or "GET", p) for m, p in _CURL.findall(text)}
    assert len(calls) >= 6
    assert sorted(c for c in calls if not _registered(*c)) == []


def test_every_placeholder_is_declared():
    used = set(re.findall(r"<([a-z][a-z0-9 ]*)>", _text()))
    assert sorted(used - PLACEHOLDERS) == []


def test_every_refusal_token_the_guide_names_is_declared():
    text = " ".join(_text().split())
    declared = {token for tokens in OPERATION_REFUSAL_TOKENS.values() for token in tokens}
    declared |= {token for route in PUBLIC_API_ROUTES for token, _status in route.refusals}
    declared |= set(re.findall(r"`([a-z_]+)`", "\n".join(r.description for r in PUBLIC_API_ROUTES)))
    named = set(re.findall(r"\b(?:40[0-9]|50[0-9]) `([a-z_]+)`", text))
    assert {"job_already_applied", "order_already_running", "api_token_invalid"} <= named
    assert sorted(named - declared - {"api_token_invalid"}) == []


def test_the_double_apply_and_the_repeated_order_are_written_as_409():
    text = " ".join(_text().split())
    assert "A second apply of the same job, for example after a lost answer, applies nothing and " \
           "answers 409 `job_already_applied`" in text
    assert "answers 409 `order_already_running`" in text
