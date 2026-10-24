"""The capability routes: where a run decides a registered feature's capability for the pair it
actually built, and where that decision's evidence is written and read back (DECISION F157 D3).

A route decides only a feature the run asked for — a stream is decided only when the run requested
stream evidence — and calls `require_or_degrade` with its register key as a string literal, so the
read guard of `tests/contracts/test_capability_matrix.py` reads every key this module names.
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


# WHY: `create_role_provider`'s one call for `stream_evidence_capture`, the request and the
# register's answer together, so the setting a provider actually gets is what the evidence names.
def routed_stream_evidence(
    role: str, model: str, requested: bool, evidence_dir: str | None,
) -> bool:
    if not requested:
        return False
    decision = stream_capture_route(model)
    record_capability_decisions(
        evidence_dir, role=role, provider="claude-cli", model=model, decisions=(decision,),
    )
    return decision.mode == CAPABILITY_MODE_NATIVE


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
