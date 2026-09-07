"""R-0827 — the provider's transport vocabulary and the manifest's must agree.

`packages/orchestration/pingpong_provider.py` stamps a `mode` on every prepared
call input; `packages/orchestration/run_manifest.py` rejects any call whose mode
is outside `VALID_CALL_MODES`. Nothing related the two, so the `ollama` provider
— the one this repository's own `resolve_role_config` returns for both roles —
stamped a mode the manifest writer refused, and every run on it ended with
`run_manifest_write_failed`. These tests are that missing relation.

The provider source is read through the imported module's own `__file__` rather
than through a repo-relative path, so the file parsed here is always the file
the constant imported below runs beside, editable install or worktree alike.
"""
from __future__ import annotations

import ast
from pathlib import Path

from packages.orchestration import pingpong_provider
from packages.orchestration.run_manifest import VALID_CALL_MODES

PROVIDER_SOURCE = Path(pingpong_provider.__file__).resolve()


def stamped_modes() -> dict[str, list[int]]:
    """Every string literal the provider passes as the keyword `mode=` to a call.

    Literals are collected from the whole keyword-value subtree, not only from a
    bare `ast.Constant`, because one site stamps a conditional
    (`mode="api-structured" if structured else "api-legacy"`) and both of its
    branches are modes the manifest will see.
    """
    tree = ast.parse(PROVIDER_SOURCE.read_text(encoding="utf-8"))
    modes: dict[str, list[int]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for keyword in node.keywords:
            if keyword.arg != "mode":
                continue
            for sub in ast.walk(keyword.value):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                    modes.setdefault(sub.value, []).append(sub.lineno)
    return modes


class TestTheProviderStampsOnlyModesTheManifestAccepts:
    def test_the_collector_finds_the_provider_s_stamped_modes(self) -> None:
        """Non-vacuity: a collector that finds nothing would pass the next test."""
        modes = stamped_modes()
        assert modes, (
            f"no `mode=` keyword string literal found in {PROVIDER_SOURCE} — the "
            f"collector, not the provider, is what changed"
        )
        assert "fake" in modes, (
            "the fake provider's own mode is missing from the collected set, so "
            "the collector is not reading the provider's call sites"
        )

    def test_every_stamped_mode_is_a_valid_call_mode(self) -> None:
        """R-0827: a mode the provider stamps and the manifest rejects is a run
        that can never publish its manifest."""
        modes = stamped_modes()
        unknown = {m: lines for m, lines in modes.items() if m not in VALID_CALL_MODES}
        assert not unknown, (
            f"{PROVIDER_SOURCE.name} stamps modes that "
            f"run_manifest.VALID_CALL_MODES rejects: "
            f"{sorted((m, lines) for m, lines in unknown.items())} — every run on the "
            f"affected transport ends with run_manifest_write_failed (R-0827)"
        )


class TestTheOllamaModesAreInTheVocabulary:
    def test_ollama_legacy_is_a_valid_call_mode(self) -> None:
        """R-0827, the finding's own named mode: `ollama-legacy` is what the
        provider stamps at its two prepared-input call sites, and the operator's
        ruling is that the provider's word is correct and the vocabulary was
        incomplete."""
        assert "ollama-legacy" in VALID_CALL_MODES

    def test_ollama_native_is_a_valid_call_mode(self) -> None:
        """R-0827, widened: the same provider stamps `ollama-native` at a third
        call site the finding's own measurement did not reach. Same defect, same
        ruling, same fix."""
        assert "ollama-native" in VALID_CALL_MODES
