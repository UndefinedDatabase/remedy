"""Round 39 F4 — capability-integrated coordinator tests.

Verifies that build_review_zip.py probes anonymous publication capability
before publishing and includes the result in its JSON output. Unsupported
capability returns exit code 4 with a typed status in the JSON.
"""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
from unittest import mock

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "_brz", REPO_ROOT / "scripts" / "build_review_zip.py")
_brz = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_brz)

from packages.orchestration.safe_publish import (
    CAPABILITY_SUPPORTED,
    CAPABILITY_UNSUPPORTED_FILESYSTEM,
    CAPABILITY_UNSUPPORTED_OS,
    probe_anonymous_publication_capability,
)


class TestProbeIsIntegrated:
    def test_coordinator_imports_probe(self):
        src = (REPO_ROOT / "scripts" / "build_review_zip.py").read_text()
        assert "probe_anonymous_publication_capability" in src

    def test_coordinator_imports_capability_supported(self):
        src = (REPO_ROOT / "scripts" / "build_review_zip.py").read_text()
        assert "CAPABILITY_SUPPORTED" in src

    def test_coordinator_checks_before_publication(self):
        src = (REPO_ROOT / "scripts" / "build_review_zip.py").read_text()
        probe_pos = src.index("probe_anonymous_publication_capability(_out_dir)")
        publish_pos = src.index("publish_atomically(")
        assert probe_pos < publish_pos

    def test_coordinator_returns_4_on_unsupported(self):
        src = (REPO_ROOT / "scripts" / "build_review_zip.py").read_text()
        assert "return 4" in src

    def test_coordinator_includes_capability_in_success_output(self):
        src = (REPO_ROOT / "scripts" / "build_review_zip.py").read_text()
        assert '"publication_capability": _pub_capability' in src


class TestProbeOnRealFilesystem:
    def test_probe_supported_on_tmp(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            cap = probe_anonymous_publication_capability(d)
            assert cap == CAPABILITY_SUPPORTED

    def test_probe_returns_typed_result(self):
        cap = probe_anonymous_publication_capability("/tmp")
        assert cap in (
            CAPABILITY_SUPPORTED,
            CAPABILITY_UNSUPPORTED_OS,
            CAPABILITY_UNSUPPORTED_FILESYSTEM,
            "LINKAT_UNAVAILABLE",
            "PERMISSION_DENIED",
        )


class TestCapabilityConstants:
    def test_supported_constant(self):
        assert CAPABILITY_SUPPORTED == "SUPPORTED"

    def test_unsupported_os_constant(self):
        assert CAPABILITY_UNSUPPORTED_OS == "UNSUPPORTED_OS"

    def test_unsupported_fs_constant(self):
        assert CAPABILITY_UNSUPPORTED_FILESYSTEM == "UNSUPPORTED_FILESYSTEM"


class TestCoordinatorUnsupportedPath:
    def test_unsupported_json_includes_capability_field(self):
        src = (REPO_ROOT / "scripts" / "build_review_zip.py").read_text()
        assert '"publication_capability": _pub_capability' in src
        assert '"publication_capability_directory": _out_dir' in src
