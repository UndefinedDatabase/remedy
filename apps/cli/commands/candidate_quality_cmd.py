"""CLI handlers for ``remedy candidate-quality`` — Local Candidate Quality Evaluation v1.

``evaluate`` writes a SAFE evidence-based evaluation report; ``show``/``scorecard``/``report``/
``integrity`` are read-only. Evaluation/reporting/routing-feedback ONLY — no model calls, no
generation, no approval/apply/test/PR/git. No raw prompt/output/candidate/diff/source/secrets in
any surface.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse


def _cmd_candidate_quality_evaluate(args: Any) -> None:
    from packages.orchestration.candidate_quality import (
        evaluate_candidate_quality,
        export_candidate_quality_json,
    )
    e = evaluate_candidate_quality(
        generation_id=getattr(args, "generation_id", None) or None,
        trust_report_id=getattr(args, "trust_report_id", None) or None,
        verification_id=getattr(args, "verification_id", None) or None,
        intent_id=getattr(args, "intent_id", None) or None,
        job_id=getattr(args, "job_id", None) or None,
        new=bool(getattr(args, "new", False)),
    )
    data = export_candidate_quality_json(e)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Candidate quality: {data['evaluation_id']}")
    print(f"  outcome: {data['outcome']}  score: {data['score']['band']} "
          f"({data['score']['value']})  conf: {data['score']['confidence']}")
    for f in data.get("findings", [])[:8]:
        print(f"  - {f['severity']}: {f['code']}")
    print(f"  next: {data['next_safe_action']}")


def _cmd_candidate_quality_show(args: Any) -> None:
    from packages.orchestration.candidate_quality import get_candidate_quality_evaluation
    rec = get_candidate_quality_evaluation(args.evaluation_id)
    if rec is None:
        print("Error: evaluation not found", file=sys.stderr)
        sys.exit(1)
    if getattr(args, "json", False):
        print(json.dumps(rec, indent=2))
        return
    print(f"Candidate quality {args.evaluation_id}")
    print(f"  outcome: {rec['outcome']}  score: {rec['score']['band']} ({rec['score']['value']})")
    for f in rec.get("findings", []):
        print(f"  - {f['severity']}: {f['code']}")
    print(f"  next: {rec.get('next_safe_action', '')}")


def _cmd_candidate_quality_scorecard(args: Any) -> None:
    from packages.orchestration.candidate_quality import build_candidate_scorecards
    data = build_candidate_scorecards(
        job_id=getattr(args, "job_id", None) or None,
        model=getattr(args, "model", None) or None,
        route_tier=getattr(args, "route_tier", None) or None,
    )
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Candidate quality scorecard ({data['evaluation_count']} evaluation(s))")
    for label, b in data.get("by_model", {}).items():
        print(f"  model {label}: runs={b['run_count']} proof_rate={b['proof_verified_rate']} "
              f"reject_rate={b['rejection_rate']} avg={b['average_score']}")


def _cmd_candidate_quality_report(args: Any) -> None:
    from packages.orchestration.candidate_quality import (
        build_candidate_scorecards,
        load_candidate_quality_evaluations,
    )
    job_id = getattr(args, "job_id", None) or None
    evals = load_candidate_quality_evaluations(job_id=job_id)
    cards = build_candidate_scorecards(job_id=job_id)
    pending = [e for e in evals if e.get("outcome") == "pending_approval"]
    incomplete = [e for e in evals if e.get("outcome") == "evidence_incomplete"]
    loop = [e for e in evals if (e.get("score", {}) or {}).get("dimensions", {}).get("loop_risk") == "fail"]
    # best/worst route by average score
    by_route = cards.get("by_route_tier", {})
    ranked = sorted(by_route.items(), key=lambda kv: kv[1].get("average_score", 0.0), reverse=True)
    best = ranked[0][0] if ranked else ""
    worst = ranked[-1][0] if ranked else ""
    latest = evals[-1] if evals else None
    if getattr(args, "json", False) and not getattr(args, "markdown", False):
        print(json.dumps({"evaluation_count": len(evals), "pending_count": len(pending),
                          "incomplete_count": len(incomplete), "loop_risk_count": len(loop),
                          "best_route": best, "worst_route": worst,
                          "latest_outcome": (latest or {}).get("outcome", ""),
                          "next_safe_action": (latest or {}).get("next_safe_action",
                                                                  "remedy candidate-quality scorecard --json")},
                         indent=2))
        return
    lines = [
        f"# Candidate Quality Report — {job_id or 'repository'}",
        "",
        "## Candidate quality summary",
        f"- evaluations: {len(evals)}",
        f"- pending decisions: {len(pending)}",
        f"- evidence incomplete: {len(incomplete)}",
        "",
        "## Best / worst routes",
        f"- best: {best or '(none)'}",
        f"- worst: {worst or '(none)'}",
        "",
        "## Pending decisions",
        *([f"- {e['evaluation_id']}: {e.get('next_safe_action','')}" for e in pending[:8]] or ["- (none)"]),
        "",
        "## Missing evidence",
        f"- {len(incomplete)} evaluation(s) with incomplete evidence",
        "",
        "## Loop risks",
        f"- {len(loop)} evaluation(s) flagged loop risk",
        "",
        "## Recommended next safe action",
        f"- `{(latest or {}).get('next_safe_action', 'remedy candidate-quality scorecard --json')}`",
    ]
    print("\n".join(lines))


def _cmd_candidate_quality_integrity(args: Any) -> None:
    from packages.orchestration.candidate_quality import candidate_quality_integrity
    data = candidate_quality_integrity()
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Candidate quality integrity: passed={data['passed']} "
          f"violations={data['violation_count']}/{data['evaluation_count']}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "candidate-quality.evaluate": _cmd_candidate_quality_evaluate,
    "candidate-quality.show": _cmd_candidate_quality_show,
    "candidate-quality.scorecard": _cmd_candidate_quality_scorecard,
    "candidate-quality.report": _cmd_candidate_quality_report,
    "candidate-quality.integrity": _cmd_candidate_quality_integrity,
}
