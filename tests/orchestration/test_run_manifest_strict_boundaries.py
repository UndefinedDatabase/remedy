"""F3/F14/F15 — the strict decoder is the ONLY untrusted entry point, enforced by the repo.

These are guard tests: they fail loudly if a future change reintroduces a permissive decoder or a
name-based trust precheck on a persisted-data production path.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]

#: The F012 production files that read untrusted manifest/snapshot/run state from disk.
_F012_PRODUCTION = [
    "packages/orchestration/run_manifest.py",
    "packages/orchestration/manifest_schema.py",
    "packages/orchestration/call_identity.py",
    "packages/orchestration/job_evidence.py",
    "packages/orchestration/pingpong_job.py",
    "apps/cli/commands/job_rerun_cmd.py",
]

#: The permissive constructors that must never touch disk-loaded data (F14). They are renamed to
#: `from_trusted_json` precisely so a plain `.from_json(` on an F012 type is a bug.
_F012_TYPES = ("RunManifestV1", "EpisodeInputSnapshotV1", "InputSnapshot", "FinalizedCall",
               "PreparedCallInput", "CallIdentity")


def _source(rel):
    return (_ROOT / rel).read_text()


class TestNoPermissiveDecoderOnDiskPaths:
    @pytest.mark.parametrize("rel", _F012_PRODUCTION)
    def test_no_permissive_from_json_call(self, rel):
        src = _source(rel)
        bad = [f"{t}.from_json(" for t in _F012_TYPES if f"{t}.from_json(" in src]
        assert bad == [], (
            f"{rel} calls a permissive decoder {bad}; untrusted disk records must go through "
            f"decode_*_v1 (F3/F14)")

    def test_the_trusted_constructors_are_explicitly_named(self):
        src = _source("packages/orchestration/run_manifest.py")
        assert "def from_trusted_json(" in src
        # and they are documented as trusted-only
        assert "TRUSTED" in src


class TestStrictDecodersExist:
    @pytest.mark.parametrize("name", [
        "decode_run_manifest_v1", "decode_episode_snapshot_v1", "decode_input_snapshot_v1",
        "decode_finalized_call_v1", "decode_prepared_call_input_v1", "decode_index_v1",
        "decode_job_input_definition_v1", "decode_call_identity_v1",
    ])
    def test_decoder_is_exported(self, name):
        from packages.orchestration import run_manifest as RM
        assert callable(getattr(RM, name))


class TestNoNameBasedTrustPrechecks:
    def test_manifest_trust_paths_do_not_stat_by_name(self):
        """F15: the manifest/recovery/canonical trust decisions use the anchored API. A few
        `Path` uses remain for non-trust purposes (e.g. normalising a path before anchoring);
        what must not exist is a name-based existence/type gate gating a trust decision."""
        src = _source("packages/orchestration/run_manifest.py")
        # the anchored existence probe is the decision point
        assert "_open_dir_anchored_or_missing" in src
        # the known trust helpers must not re-introduce a name-based gate
        for fn in ("def load_index_verified", "def episode_manifest_exists_anchored",
                   "def _enumerate_episode_dirs_anchored", "def read_canonical_episode_order",
                   "def read_run_manifest", "def load_episode_record_for_recovery"):
            start = src.index(fn)
            body = src[start:start + 1600]
            assert ".is_dir()" not in body, f"{fn} still gates trust on Path.is_dir()"
            assert ".read_text()" not in body, f"{fn} still reads by name"
            assert ".read_bytes()" not in body, f"{fn} still reads by name"


class TestCanonicalHelpersExist:
    def test_raw_byte_and_duplicate_key_guards_exist(self):
        from packages.orchestration import run_manifest as RM
        assert callable(RM.require_canonical_bytes)
        assert callable(RM.strict_json_loads)


# --------------------------------------------------------------------------- F11 (round 9)


#: Modules whose F012 responsibility is READING manifest/index/artifact bytes. Ordinary
#: `json.loads` is a permissive parser: it silently accepts duplicate keys (last-wins) and the
#: non-standard NaN/Infinity constants, and it raises raw `UnicodeDecodeError` on bad UTF-8.
#: Every untrusted manifest byte must go through `strict_json_loads` / `decode_*_v1` instead.
_MANIFEST_ONLY_MODULES = [
    "packages/orchestration/manifest_schema.py",
    "packages/orchestration/call_identity.py",
    "apps/cli/commands/job_rerun_cmd.py",
]

#: Substrings naming manifest/index/artifact data. A `json.loads` on a line mentioning one of
#: these is parsing F012 records permissively.
_MANIFEST_TOKENS = ("manifest", "run_manifest_index", "episode", "call_identity",
                    "prepared_call_input", "coverage", "MANIFEST_")


class TestNoRawJsonLoadsOnManifestBytes:
    """F11: no ordinary `json.loads` on raw Manifest / Index / Artifact bytes."""

    @pytest.mark.parametrize("rel", _MANIFEST_ONLY_MODULES)
    def test_manifest_modules_never_call_json_loads(self, rel):
        src = _source(rel)
        hits = [ln for ln in src.splitlines()
                if re.search(r"\bjson\.loads?\(|\b_json\.loads?\(", ln)]
        assert hits == [], (
            f"{rel} parses JSON permissively {hits}; F012 records must go through "
            f"strict_json_loads/decode_*_v1 (F11)")

    def test_run_manifest_json_loads_only_inside_strict_json_loads(self):
        """The ONE justified exception: `strict_json_loads` itself, which is the strict parser.
        It must pass both hardening hooks — duplicate-key rejection and constant rejection."""
        import ast
        src = _source("packages/orchestration/run_manifest.py")
        tree = ast.parse(src)
        owners = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            body = ast.get_source_segment(src, node) or ""
            if re.search(r"\bjson\.loads?\(", body):
                # only the function that DIRECTLY calls it, not its enclosing scopes
                inner = [n.name for n in ast.walk(node)
                         if isinstance(n, ast.FunctionDef) and n is not node
                         and re.search(r"\bjson\.loads?\(", ast.get_source_segment(src, n) or "")]
                if not inner:
                    owners.append(node.name)
        assert owners == ["strict_json_loads"], (
            f"run_manifest.py calls json.loads outside the strict parser: {owners} (F11)")
        start = src.index("def strict_json_loads(")
        body = src[start:src.index("\ndef ", start + 1)]
        assert "object_pairs_hook=_no_duplicate_keys" in body   # duplicate keys rejected
        assert "parse_constant=" in body                        # NaN/Infinity rejected

    def test_job_evidence_manifest_export_never_calls_json_loads(self):
        """job_evidence.py legitimately parses NON-manifest evidence (traces, token truth) with
        json.loads. What it must never do is parse MANIFEST bytes that way."""
        import ast
        src = _source("packages/orchestration/job_evidence.py")
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            if "manifest" not in node.name.lower():
                continue
            body = ast.get_source_segment(src, node) or ""
            calls = [ln for ln in body.splitlines()
                     if re.search(r"\bjson\.loads?\(|\b_json\.loads?\(", ln)
                     and not ln.strip().startswith("#")]
            assert calls == [], f"{node.name} parses manifest bytes permissively: {calls} (F11)"

    def test_no_manifest_line_anywhere_uses_json_loads(self):
        """Cross-module sweep: a `json.loads` on a line that names manifest/index/artifact data
        is a permissive manifest read wherever it lives."""
        offenders = []
        for rel in _F012_PRODUCTION:
            for i, ln in enumerate(_source(rel).splitlines(), 1):
                if ln.strip().startswith("#"):
                    continue
                if not re.search(r"\bjson\.loads?\(|\b_json\.loads?\(", ln):
                    continue
                low = ln.lower()
                if any(tok.lower() in low for tok in _MANIFEST_TOKENS):
                    offenders.append(f"{rel}:{i}: {ln.strip()}")
        assert offenders == [], f"permissive manifest reads remain (F11): {offenders}"


class TestNoNameBasedPrecheckInAnchoredTreeReader:
    """F12: `read_manifest_tree_bytes_anchored` decides presence on a VERIFIED handle."""

    def test_tree_reader_uses_the_anchored_probe(self):
        src = _source("packages/orchestration/run_manifest.py")
        start = src.index("def read_manifest_tree_bytes_anchored(")
        body = src[start:src.index("\ndef ", start + 1)]
        assert "_open_dir_anchored_or_missing" in body
        for bad in (".is_dir()", ".exists()", ".is_file()", ".read_bytes()", ".read_text()"):
            assert bad not in body, f"tree reader still gates trust on {bad} (F12)"
