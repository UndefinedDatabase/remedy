"""Unit tests for Local Model Advisor Adapter v0 (Steps 1521-1526).

Covers config/endpoint safety, response parsing + redaction, availability probe, invocation
+ private storage + idempotency + budget + anti-loop, advisor impact rules on orchestrator
decisions, and architecture guards. No real Ollama: a fake injected transport is used.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration import local_model_advisor as M


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _cfg(**kw):
    base = dict(enabled=True, endpoint="http://127.0.0.1:11434", model_name="m",
                timeout_seconds=2, max_runs=5)
    base.update(kw)
    return M.LocalAdvisorConfig(**base)


def _tx(inner=None, raw=None, tags=("m",), gen_status=200, gen_body=None, raise_exc=None):
    def tx(method, url, body, timeout):
        if raise_exc is not None:
            raise raise_exc
        if url.endswith("/api/tags"):
            return (200, json.dumps({"models": [{"name": n} for n in tags]}).encode())
        if url.endswith("/api/generate"):
            if gen_body is not None:
                return (gen_status, gen_body)
            payload = raw if raw is not None else json.dumps(inner or {"summary": "ok"})
            return (gen_status, json.dumps({"response": payload}).encode())
        return (404, b"")
    return tx


def _payload(**kw):
    base = {"current_phase": "idle", "selected_option": {"kind": "self_inspect", "label": "x"},
            "options": [], "rejected_options": [], "evidence_refs": [], "blockers": [],
            "risks": [], "loop_guard_status": "allow",
            "model_routing_plan": {"tier": "local_advisor_preferred"}, "confidence": "medium"}
    base.update(kw)
    return base


# ---------------------------------------------------------------------------
# Config + endpoint safety (Steps 1501/1506/1522)
# ---------------------------------------------------------------------------


class TestConfigEndpointSafety:
    def test_disabled_by_default(self):
        cfg = M.load_local_advisor_config(env={})
        assert cfg.enabled is False

    def test_loopback_accepted(self):
        assert M._validate_endpoint("http://127.0.0.1:11434")[0] is True
        assert M._validate_endpoint("http://localhost:11434")[0] is True
        assert M._validate_endpoint("http://[::1]:11434")[0] is True

    def test_external_host_rejected(self):
        ok, reason, label = M._validate_endpoint("http://evil.example.com:11434")
        assert ok is False
        assert reason == "non_loopback"
        assert "evil.example.com" not in label  # never echo the external host

    def test_https_external_rejected(self):
        ok, _r, label = M._validate_endpoint("https://evil.example.com")
        assert ok is False
        assert "evil" not in label

    def test_file_scheme_rejected(self):
        ok, reason, _label = M._validate_endpoint("file:///etc/passwd")
        assert ok is False
        assert reason == "scheme_not_http"

    def test_enabled_requires_loopback_and_model(self):
        env_ext = {"REMEDY_LOCAL_ADVISOR_ENABLED": "1",
                   "REMEDY_LOCAL_ADVISOR_ENDPOINT": "http://evil.com", "REMEDY_LOCAL_ADVISOR_MODEL": "m"}
        assert M.load_local_advisor_config(env=env_ext).enabled is False
        env_ok = {"REMEDY_LOCAL_ADVISOR_ENABLED": "1",
                  "REMEDY_LOCAL_ADVISOR_ENDPOINT": "http://127.0.0.1:11434",
                  "REMEDY_LOCAL_ADVISOR_MODEL": "m"}
        assert M.load_local_advisor_config(env=env_ok).enabled is True

    def test_timeout_clamped(self):
        cfg = M.load_local_advisor_config(env={"REMEDY_LOCAL_ADVISOR_TIMEOUT_SECONDS": "9999"})
        assert cfg.timeout_seconds <= M.MAX_TIMEOUT_SECONDS

    def test_availability_disabled_unavailable(self):
        av = M.check_local_advisor_availability(M.LocalAdvisorConfig(enabled=False))
        assert av.available is False
        assert av.stop_reason == M.LocalAdvisorStopReason.DISABLED

    def test_availability_loopback_available(self):
        av = M.check_local_advisor_availability(_cfg(), transport=_tx(tags=("m:latest",)))
        assert av.available is True

    def test_availability_model_missing(self):
        av = M.check_local_advisor_availability(_cfg(), transport=_tx(tags=("other",)))
        assert av.available is False
        assert av.stop_reason == M.LocalAdvisorStopReason.MODEL_MISSING

    def test_availability_timeout_safe(self):
        av = M.check_local_advisor_availability(_cfg(), transport=_tx(raise_exc=TimeoutError()))
        assert av.available is False
        assert av.stop_reason == M.LocalAdvisorStopReason.TIMEOUT
        assert "Traceback" not in av.detail


# ---------------------------------------------------------------------------
# Response parsing + redaction (Steps 1503/1508/1521/1523)
# ---------------------------------------------------------------------------


class TestParsing:
    def test_valid_json_parsed(self):
        safe, findings, status = M.parse_local_advisor_response(json.dumps(
            {"summary": "s", "concerns": [{"severity": "high", "message": "m"}],
             "missing_evidence": ["e"], "alternative_action": {"label": "L", "reason": "R"},
             "loop_risk": "low", "confidence_hint": "high"}))
        assert status == M.LocalAdvisorStatus.COMPLETED
        assert safe["confidence_hint"] == "high"
        assert safe["concerns"][0]["severity"] == "high"

    def test_unparseable_safe(self):
        safe, findings, status = M.parse_local_advisor_response("not json at all")
        assert status == M.LocalAdvisorStatus.UNPARSEABLE
        assert any(f.code == "advisor_unparseable" for f in findings)

    def test_unknown_severity_normalised(self):
        safe, _f, _s = M.parse_local_advisor_response(json.dumps(
            {"summary": "s", "concerns": [{"severity": "catastrophic", "message": "m"}],
             "loop_risk": "apocalyptic", "confidence_hint": "ultra"}))
        assert safe["concerns"][0]["severity"] == "low"
        assert safe["loop_risk"] == "none"
        assert safe["confidence_hint"] == "low"

    def test_missing_fields_tolerated(self):
        safe, _f, status = M.parse_local_advisor_response(json.dumps({"summary": "only"}))
        assert status == M.LocalAdvisorStatus.COMPLETED
        assert safe["concerns"] == [] and safe["missing_evidence"] == []

    def test_code_or_diff_flagged_high(self):
        _safe, findings, _s = M.parse_local_advisor_response(
            '{"summary":"x"}\n```python\nimport os\n```')
        assert any(f.code == "code_or_diff_in_response" and f.severity == "high" for f in findings)
        _safe2, findings2, _s2 = M.parse_local_advisor_response(
            '{"summary":"x"}\ndiff --git a/f b/f')
        assert any(f.code == "code_or_diff_in_response" for f in findings2)

    def test_secrets_paths_tracebacks_scrubbed(self):
        raw = json.dumps({
            "summary": "leak sk-abcdef0123456789abcd at /home/u/.ssh/id_rsa",
            "concerns": [{"severity": "low", "message": "Traceback (most recent call last) "
                          "AKIAABCDEFGHIJKLMNOP at /home/x/.env"}],
            "missing_evidence": ["/root/secret token=supersecretvalue123"]})
        safe, findings, _s = M.parse_local_advisor_response(raw)
        blob = json.dumps(safe) + json.dumps([f.to_dict() for f in findings])
        assert "sk-abcdef0123456789abcd" not in blob
        assert "/home/" not in blob
        assert "id_rsa" not in blob
        assert "Traceback" not in blob
        assert "supersecretvalue123" not in blob


# ---------------------------------------------------------------------------
# Invocation: storage, idempotency, budget, oversized, anti-loop (Steps 1504/1507/1511/1516)
# ---------------------------------------------------------------------------


class TestInvocation:
    def test_disabled_run_safe(self, tmp_path):
        r = M.run_local_advisor(M.LocalAdvisorRequest(payload=_payload()),
                                M.LocalAdvisorConfig(enabled=False), data_dir=tmp_path)
        assert r.status == M.LocalAdvisorStatus.DISABLED

    def test_run_stores_private_no_raw(self, tmp_path):
        inner = {"summary": "secret token=topsecretvalue99 at /home/u/.env",
                 "concerns": [], "loop_risk": "none", "confidence_hint": "low"}
        r = M.run_local_advisor(M.LocalAdvisorRequest(scope="repository", payload=_payload()),
                                _cfg(), data_dir=tmp_path, transport=_tx(inner=inner))
        assert r.status == M.LocalAdvisorStatus.COMPLETED
        rdir = tmp_path / "workspaces" / "orchestrator" / "local_advisor_runs"
        run_dir = next(rdir.glob("*"))
        names = {p.name for p in run_dir.iterdir()}
        assert names == {"prompt.md", "response.txt", "run_manifest.json"}
        manifest = (run_dir / "run_manifest.json").read_text()
        assert "topsecretvalue99" not in manifest  # raw stays in response.txt only
        export = json.dumps(M.export_local_advisor_response_json(r))
        assert "topsecretvalue99" not in export
        assert "/home/" not in export

    def test_idempotent_reuse(self, tmp_path):
        req = M.LocalAdvisorRequest(scope="repository", payload=_payload())
        r1 = M.run_local_advisor(req, _cfg(), data_dir=tmp_path, transport=_tx())
        r2 = M.run_local_advisor(req, _cfg(), data_dir=tmp_path, transport=_tx())
        assert r1.status == M.LocalAdvisorStatus.COMPLETED
        assert r2.status == M.LocalAdvisorStatus.REUSED

    def test_new_forces_fresh(self, tmp_path):
        req = M.LocalAdvisorRequest(scope="repository", payload=_payload())
        M.run_local_advisor(req, _cfg(), data_dir=tmp_path, transport=_tx())
        r2 = M.run_local_advisor(req, _cfg(), data_dir=tmp_path, transport=_tx(), new=True)
        assert r2.status == M.LocalAdvisorStatus.COMPLETED

    def test_oversized_response_rejected(self, tmp_path):
        big = b"x" * (M.MAX_RESPONSE_BYTES + 100)
        r = M.run_local_advisor(M.LocalAdvisorRequest(payload=_payload()), _cfg(),
                                data_dir=tmp_path, transport=_tx(gen_body=big))
        assert r.status == M.LocalAdvisorStatus.UNAVAILABLE
        assert r.stop_reason == M.LocalAdvisorStopReason.OVERSIZED

    def test_budget_blocks_advisor(self, tmp_path):
        cfg = _cfg(max_runs=1)
        # vary payload so the first run is not reused.
        M.run_local_advisor(M.LocalAdvisorRequest(scope="repository", payload=_payload(confidence="low")),
                            cfg, data_dir=tmp_path, transport=_tx())
        r2 = M.run_local_advisor(M.LocalAdvisorRequest(scope="repository", payload=_payload(confidence="high")),
                                 cfg, data_dir=tmp_path, transport=_tx())
        assert r2.status == M.LocalAdvisorStatus.BLOCKED
        assert r2.stop_reason == M.LocalAdvisorStopReason.BUDGET_EXHAUSTED

    def test_repeated_unavailable_suppressed(self, tmp_path):
        req = M.LocalAdvisorRequest(scope="repository", payload=_payload())
        tx_down = _tx(raise_exc=ConnectionError())
        for _ in range(M.MAX_UNAVAILABLE_REPEAT):
            r = M.run_local_advisor(req, _cfg(), data_dir=tmp_path, transport=tx_down)
            assert r.status == M.LocalAdvisorStatus.UNAVAILABLE
        # Now suppressed without even calling the transport.
        def boom(*a, **k):  # would fail if called
            raise AssertionError("transport must not be called after suppression")
        r_sup = M.run_local_advisor(req, _cfg(), data_dir=tmp_path, transport=boom)
        assert r_sup.status == M.LocalAdvisorStatus.UNAVAILABLE

    def test_usage_separate_and_tokens_unknown(self, tmp_path):
        M.run_local_advisor(M.LocalAdvisorRequest(scope="repository", payload=_payload()),
                            _cfg(), data_dir=tmp_path, transport=_tx())
        usage = M.load_local_advisor_usage("repository", tmp_path)
        assert usage["run_count"] == 1
        assert usage["tokens_used"] == "unknown"


# ---------------------------------------------------------------------------
# Advisor impact rules on orchestrator decisions (Steps 1509/1510/1524)
# ---------------------------------------------------------------------------


class TestAdvisorImpact:
    @pytest.fixture(autouse=True)
    def _enable(self, monkeypatch):
        # consult builds config from env; enable a loopback advisor (transport is injected).
        monkeypatch.setenv("REMEDY_LOCAL_ADVISOR_ENABLED", "1")
        monkeypatch.setenv("REMEDY_LOCAL_ADVISOR_ENDPOINT", "http://127.0.0.1:11434")
        monkeypatch.setenv("REMEDY_LOCAL_ADVISOR_MODEL", "m")

    def _dec(self, **kw):
        from packages.orchestration.orchestrator_brain import OrchestratorDecision, StopReason
        base = dict(decision_id="d1", scope="repository", stop_reason=StopReason.SELECTED,
                    confidence="high", selected_option={"kind": "continue_intent",
                    "label": "Continue", "score": 85}, next_safe_action="remedy do continue X --json")
        base.update(kw)
        return OrchestratorDecision(**base)

    def _sit(self, weak=False):
        from packages.orchestration.orchestrator_brain import (
            OrchestratorSituation, OrchestratorEvidenceRef)
        s = OrchestratorSituation(scope="repository",
                                  evidence_status=("degraded" if weak else "complete"))
        s.evidence_refs = [OrchestratorEvidenceRef("job", "unknown" if weak else "available")]
        return s

    def _consult(self, decision, situation, inner, tmp_path):
        from packages.orchestration import orchestrator_brain as OB
        return OB.consult_local_advisor_for_decision(
            decision, situation, data_dir=tmp_path, enabled_override=True,
            transport=_tx(inner=inner))

    def test_model_cannot_create_next_action(self, tmp_path):
        d = self._dec()
        inner = {"summary": "do this", "alternative_action": {"label": "rm -rf", "reason": "x"},
                 "concerns": [], "loop_risk": "none", "confidence_hint": "high"}
        self._consult(d, self._sit(weak=False), inner, tmp_path)
        # The action is still the deterministic command; model's "alternative" never executes.
        assert d.next_safe_action == "remedy do continue X --json"

    def test_model_cannot_override_blocker(self, tmp_path):
        from packages.orchestration.orchestrator_brain import StopReason
        d = self._dec(stop_reason=StopReason.HUMAN_REVIEW_REQUIRED, selected_option=None,
                      blockers=["review_findings_open"], confidence="high",
                      next_safe_action="remedy self inspect --json")
        inner = {"summary": "looks fine", "concerns": [], "loop_risk": "none",
                 "confidence_hint": "high"}
        self._consult(d, self._sit(weak=False), inner, tmp_path)
        assert d.stop_reason == StopReason.HUMAN_REVIEW_REQUIRED
        assert d.selected_option is None

    def test_model_can_lower_confidence(self, tmp_path):
        from packages.orchestration.orchestrator_brain import StopReason
        d = self._dec(confidence="high")
        inner = {"summary": "some risk", "concerns": [{"severity": "low", "message": "m"}],
                 "loop_risk": "low", "confidence_hint": "low"}
        self._consult(d, self._sit(weak=False), inner, tmp_path)
        assert d.confidence == "medium"  # lowered one notch
        assert d.stop_reason == StopReason.SELECTED  # action unchanged
        assert d.advisor["decision_impact"] == "confidence_adjusted"

    def test_model_can_escalate_weak_evidence(self, tmp_path):
        from packages.orchestration.orchestrator_brain import StopReason
        d = self._dec(confidence="medium")
        inner = {"summary": "risky", "concerns": [{"severity": "high", "message": "weak proof"}],
                 "missing_evidence": ["proof"], "loop_risk": "high", "confidence_hint": "low"}
        self._consult(d, self._sit(weak=True), inner, tmp_path)
        assert d.stop_reason == StopReason.HUMAN_REVIEW_REQUIRED
        assert d.selected_option is None
        assert d.next_safe_action == "remedy orchestrator report --json"
        assert d.advisor["decision_impact"] == "human_review_required"

    def test_model_cannot_strengthen_confidence(self, tmp_path):
        d = self._dec(confidence="low")
        inner = {"summary": "all good", "concerns": [], "loop_risk": "none",
                 "confidence_hint": "high"}
        self._consult(d, self._sit(weak=False), inner, tmp_path)
        assert d.confidence == "low"  # advisor can never raise confidence

    def test_unavailable_advisor_no_change(self, tmp_path):
        from packages.orchestration import orchestrator_brain as OB
        d = self._dec()
        OB.consult_local_advisor_for_decision(
            d, self._sit(), data_dir=tmp_path, enabled_override=True,
            transport=_tx(raise_exc=ConnectionError()))
        assert d.next_safe_action == "remedy do continue X --json"
        assert d.advisor["decision_impact"] == "no_change"

    def test_disabled_advisor_no_change(self, tmp_path, monkeypatch):
        from packages.orchestration import orchestrator_brain as OB
        for k in ("REMEDY_LOCAL_ADVISOR_ENABLED", "REMEDY_LOCAL_ADVISOR_ENDPOINT",
                  "REMEDY_LOCAL_ADVISOR_MODEL"):
            monkeypatch.delenv(k, raising=False)
        d = self._dec()
        OB.consult_local_advisor_for_decision(d, self._sit(), data_dir=tmp_path,
                                              enabled_override=False)
        assert d.advisor["enabled"] is False
        assert d.next_safe_action == "remedy do continue X --json"

    def test_advisor_dict_redacted_for_downstream(self, tmp_path):
        # The decision.advisor dict feeds Progress/Feature/Review/Cockpit — it must be scrubbed.
        from packages.orchestration import orchestrator_brain as OB
        from packages.orchestration import progress_ledger as PL
        from packages.orchestration.review_bundle import _build_local_advisor_summary
        d = self._dec()
        inner = {"summary": "leak sk-abcdef0123456789abcd /home/u/.ssh/id_rsa",
                 "concerns": [{"severity": "low", "message": "Traceback (most recent call last) "
                               "token=supersecretvalue321"}],
                 "missing_evidence": ["/root/.env"], "loop_risk": "none", "confidence_hint": "low"}
        self._consult(d, self._sit(weak=False), inner, tmp_path)
        export = json.dumps(OB.export_decision_json(d))
        items = PL.extract_local_advisor_items(OB.export_decision_json(d))
        blob = export + json.dumps([i.__dict__ for i in items], default=str)
        for bad in ("sk-abcdef0123456789abcd", "/home/", "id_rsa", "Traceback",
                    "supersecretvalue321"):
            assert bad not in blob


# ---------------------------------------------------------------------------
# Architecture guards (Step 1526)
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    SRC = Path("packages/orchestration/local_model_advisor.py").read_text()

    def _imports(self):
        return [ln for ln in self.SRC.splitlines()
                if ln.strip().startswith(("import ", "from "))]

    def test_no_provider_or_cloud_sdk(self):
        for ln in self._imports():
            low = ln.lower()
            for bad in ("ollama", "anthropic", "openai", "litellm", "boto3", "google.generativeai"):
                assert bad not in low, ln

    def test_no_subprocess_or_shell(self):
        for ln in self._imports():
            assert "subprocess" not in ln, ln
        assert "import subprocess" not in self.SRC
        assert "shell=True" not in self.SRC
        assert "os.system" not in self.SRC

    def test_no_browser_or_external_http_libs(self):
        for ln in self._imports():
            for bad in ("requests", "httpx", "selenium", "playwright", "aiohttp"):
                assert bad not in ln, ln

    def test_only_stdlib_urllib_for_http(self):
        # HTTP is allowed but must be stdlib urllib only.
        assert "import urllib" in self.SRC

    def test_no_apply_or_git_or_jobtasks(self):
        for ln in self._imports():
            assert "patch_apply" not in ln
            assert "source_apply" not in ln
            assert "import git" not in ln and "from git" not in ln
        assert ".tasks.append" not in self.SRC
        assert "gh pr" not in self.SRC

    def test_no_raw_fields_in_public_models(self):
        # Public dataclasses must not carry raw prompt/response text fields.
        for forbidden in ("raw_prompt", "raw_response", "prompt_text", "response_text"):
            assert forbidden not in self.SRC
