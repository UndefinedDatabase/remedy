"""The capability routes: where a run decides a registered feature's capability for the pair it
actually built, and where that decision's evidence is written and read back (DECISION F157 D3).

A route decides only a feature the run asked for — a stream is decided only when the run requested
stream evidence — and calls `require_or_degrade` with its register key as a string literal, so the
consumer guard of `tests/contracts/test_capability_matrix.py` reads every key this module names.
"""
from __future__ import annotations

import json
from pathlib import Path

from packages.contracts.capability_matrix import (
    CAPABILITY_MODE_NATIVE,
    CapabilityDecision,
    capability_decision_record,
    capability_degradation_entries,
    require_or_degrade,
)
from packages.orchestration.structured_outputs import reviewer_structured_enabled
from packages.orchestration.worker_adapter_slot import installed_worker_adapter

# WHY: the one file name every route writes to and every reader opens, named once (DECISION F157 D3 (3)).
CAPABILITY_DECISIONS_FILENAME = "capability_decisions.jsonl"


# WHY: the route for `stream_evidence_capture`, a literal key so the matrix's consumer guard holds.
def stream_capture_route(model: str, **settings) -> CapabilityDecision:
    return require_or_degrade(
        "stream_evidence_capture",
        installed_worker_adapter("claude-cli", streaming=True, **settings),
        model,
    )


# WHY: the route for `reviewer_schema_gate`, a literal key so the matrix's consumer guard holds.
def reviewer_schema_route(model: str, **settings) -> CapabilityDecision:
    return require_or_degrade(
        "reviewer_schema_gate",
        installed_worker_adapter("claude-cli", **settings),
        model,
    )


# WHY: the route for `parked_session_resume`, a literal key so the matrix's consumer guard holds.
def parked_resume_route(model: str, **settings) -> CapabilityDecision:
    return require_or_degrade(
        "parked_session_resume",
        installed_worker_adapter("claude-cli", **settings),
        model,
    )


# WHY: the claude-cli provider's one reviewer-schema reading (DECISION F157 D4 (2)): the operator
# switch and the route's answer together, so a degraded adapter never claims native enforcement.
def routed_reviewer_schema(model: str) -> bool:
    return (
        reviewer_structured_enabled()
        and reviewer_schema_route(model).mode == CAPABILITY_MODE_NATIVE
    )


# WHY: the claude-cli provider's one resume reading (DECISION F157 D4 (2)): the route's answer for
# `parked_session_resume`, the only input `ClaudeCliProvider.supports_resume` needs.
def routed_parked_resume(model: str) -> bool:
    return parked_resume_route(model).mode == CAPABILITY_MODE_NATIVE


# WHY: the run's decisions live beside the run, one line per provider build that decided anything
# (DECISION F157 D3 (3)); both run-record writers this would otherwise touch are structure-ledger rows.
def record_capability_decisions(
    evidence_dir: str | None, *, role: str, provider: str, model: str,
    decisions: tuple[CapabilityDecision, ...],
) -> None:
    if not evidence_dir or not decisions:
        return
    directory = Path(evidence_dir)
    directory.mkdir(parents=True, exist_ok=True)
    line = json.dumps(
        {
            "role": role,
            "provider": provider,
            "model": model,
            "decisions": [capability_decision_record(d) for d in decisions],
        },
        sort_keys=True,
    )
    with open(directory / CAPABILITY_DECISIONS_FILENAME, "a", encoding="utf-8") as handle:
        handle.write(line + "\n")


# WHY: `create_role_provider`'s one call for the claude-cli build's whole set of decisions
# (DECISION F157 D4 (3)): resume on every role, the reviewer's schema for the reviewer, the
# stream setting when requested, recorded in one line only when something degraded (D4 (4)).
def routed_claude_cli_build(
    role: str, model: str, requested_stream: bool, evidence_dir: str | None,
) -> bool:
    decisions = [parked_resume_route(model)]
    if role == "reviewer":
        decisions.append(reviewer_schema_route(model))
    stream_decision: CapabilityDecision | None = None
    if requested_stream:
        stream_decision = stream_capture_route(model)
        decisions.append(stream_decision)
    if any(decision.mode != CAPABILITY_MODE_NATIVE for decision in decisions):
        record_capability_decisions(
            evidence_dir, role=role, provider="claude-cli", model=model,
            decisions=tuple(decisions),
        )
    if stream_decision is None:
        return False
    return stream_decision.mode == CAPABILITY_MODE_NATIVE


# WHY: the run's degradations, read back from the evidence file this module writes.
def read_capability_degradations(evidence_dir: str | None) -> list[dict]:
    if not evidence_dir:
        return []
    path = Path(evidence_dir) / CAPABILITY_DECISIONS_FILENAME
    if not path.is_file():
        return []
    decisions: list[CapabilityDecision] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        try:
            parsed = json.loads(raw_line)
        except json.JSONDecodeError:
            continue
        if not isinstance(parsed, dict):
            continue
        for record in parsed.get("decisions", []):
            decisions.append(CapabilityDecision(
                feature_key=record["feature_key"], mode=record["mode"],
                strategy=record["strategy"], missing=tuple(record["missing"]),
            ))
    return capability_degradation_entries(decisions)
