"""F075 T001 — the gauntlet matrix report: what the campaign proved, in two formats.

The matrix is the evidence a human reads before flipping multi-cycle defaults,
so it carries per run exactly what T1_F075.md asks for: terminal status, the
DoD matrix, postmortem classes, operator interventions, wall/tokens, and links
into that run's own evidence — plus, because this gate is about honesty, the
full criteria table and every named failure.

**The bytes are deterministic for a given evidence set.** No clock, no absolute
paths, no dict-iteration order: the report is a pure function of the recorded
evidence, which is what makes a golden-file comparison a real test instead of a
snapshot that gets re-blessed whenever it moves. The evidence directory appears
by LABEL (its basename by default), never by absolute path — an absolute path
would make the same campaign render differently on two machines.

Two renderers over one payload: :func:`matrix_json` is the machine-readable
truth, :func:`render_matrix_markdown` the human one, and
:func:`write_matrix` puts both next to the runs they judge.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from packages.orchestration.dod_gate import render_matrix as _render_dod_matrix
from packages.orchestration.gauntlet_evaluator import (
    PASS_CRITERIA,
    GauntletVerdict,
    RunVerdict,
)

#: Report schema version. Bumped when the payload shape changes, so a reader
#: never has to guess which shape it is holding.
MATRIX_VERSION = 1

#: The report file names, written side by side.
MATRIX_MARKDOWN_FILENAME = "matrix.md"
MATRIX_JSON_FILENAME = "matrix.json"

#: The summary table's columns, in render order.
SUMMARY_HEADER = ("run", "order", "kind", "terminal", "flawless",
                  "interventions", "wall", "tokens in/out")


def _wall(seconds: float) -> str:
    """Wall clock as a fixed-precision string — a float repr is not a format."""
    return f"{seconds:.1f}s"


def postmortem_classes(run: RunVerdict) -> tuple[str, ...]:
    """The failure classes this run recorded, deduplicated, in first-seen order.

    First-seen rather than sorted: the order the run met its failures is itself
    information, and it is as deterministic as the evidence file.
    """
    seen: list[str] = []
    for record in run.evidence.postmortems:
        name = str(record.get("failure_class", "") or "(absent)")
        if name not in seen:
            seen.append(name)
    return tuple(seen)


def _run_payload(run: RunVerdict) -> dict[str, Any]:
    body = run.to_json()
    body["postmortem_classes"] = list(postmortem_classes(run))
    body["dod_matrix"] = _render_dod_matrix(run.evidence.dod_result)
    return body


def matrix_json(verdict: GauntletVerdict, *, label: str | None = None) -> dict[str, Any]:
    """The machine-readable matrix. Deterministic for a given evidence set."""
    return {
        "matrix_version": MATRIX_VERSION,
        "evidence_label": label if label is not None else Path(verdict.evidence_dir).name,
        "runs_recorded": len(verdict.runs),
        "runs_flawless": verdict.flawless_count,
        "passed": verdict.passed,
        "pass_criteria": list(PASS_CRITERIA),
        "failure_kinds": list(verdict.failure_kinds()),
        "runs": [_run_payload(run) for run in verdict.runs],
    }


def matrix_json_bytes(verdict: GauntletVerdict, *, label: str | None = None) -> str:
    """The JSON report as the exact text written to disk."""
    return json.dumps(matrix_json(verdict, label=label),
                      indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _summary_rows(verdict: GauntletVerdict) -> list[tuple[str, ...]]:
    return [
        (run.run_dir,
         run.order_id or "-",
         run.evidence.kind or "-",
         run.evidence.terminal_status or "(none)",
         "yes" if run.flawless else "NO",
         str(len(run.evidence.operator_interventions)),
         _wall(run.evidence.wall_seconds),
         f"{run.evidence.tokens_in}/{run.evidence.tokens_out}")
        for run in verdict.runs
    ]


def _table(header: tuple[str, ...], rows: list[tuple[str, ...]]) -> list[str]:
    lines = ["| " + " | ".join(header) + " |",
             "| " + " | ".join("---" for _ in header) + " |"]
    lines += ["| " + " | ".join(row) + " |" for row in rows]
    return lines


def _run_section(run: RunVerdict) -> list[str]:
    ev = run.evidence
    lines = [f"### {run.run_dir} — {run.order_id or '(no order id)'}", ""]
    lines.append(f"- Flawless: **{'yes' if run.flawless else 'NO'}**")
    lines.append(f"- Terminal: {ev.terminal_status or '(none)'}")
    lines.append(f"- Operator interventions: {len(ev.operator_interventions)}")
    for command in ev.operator_interventions:
        lines.append(f"  - `{command}`")
    classes = postmortem_classes(run)
    lines.append(f"- Postmortem classes: {', '.join(classes) if classes else 'none'}")
    lines.append(f"- Wall / tokens: {_wall(ev.wall_seconds)} · "
                 f"{ev.tokens_in} in / {ev.tokens_out} out")
    lines.append("")

    lines.append("Criteria:")
    lines.append("")
    lines += _table(("criterion", "held"),
                    [(name, "yes" if run.criteria[name] else "NO")
                     for name in PASS_CRITERIA])
    lines.append("")

    lines.append("DoD matrix:")
    lines.append("")
    lines.append(_render_dod_matrix(ev.dod_result))
    lines.append("")

    if run.failures:
        lines.append("Failures:")
        lines.append("")
        lines += _table(
            ("kind", "criterion", "finding class", "injection class", "detail"),
            [(f.kind, f.criterion, f.finding_class or "-",
              f.injection_class or "-", f.detail) for f in run.failures])
        lines.append("")

    if ev.evidence_links:
        lines.append("Evidence:")
        lines.append("")
        for name, target in sorted(ev.evidence_links.items()):
            lines.append(f"- {name}: `{run.run_dir}/{target}`")
        lines.append("")
    return lines


def render_matrix_markdown(verdict: GauntletVerdict, *, label: str | None = None) -> str:
    """The human-readable matrix. Same facts as :func:`matrix_json`, same bytes twice."""
    name = label if label is not None else Path(verdict.evidence_dir).name
    lines = [f"# Gauntlet matrix — {name}", ""]
    lines.append(f"{verdict.flawless_count}/{len(verdict.runs)} runs flawless · "
                 f"**{'PASS' if verdict.passed else 'NOT A PASS'}**")
    lines.append("")
    if not verdict.runs:
        lines.append("No runs were recorded. An empty gauntlet is not a pass.")
        return "\n".join(lines) + "\n"
    lines += _table(SUMMARY_HEADER, _summary_rows(verdict))
    lines.append("")
    kinds = verdict.failure_kinds()
    lines.append(f"Failure kinds present: {', '.join(kinds) if kinds else 'none'}")
    lines.append("")
    lines.append("## Runs")
    lines.append("")
    for run in verdict.runs:
        lines += _run_section(run)
    return "\n".join(lines).rstrip("\n") + "\n"


def write_matrix(verdict: GauntletVerdict, out_dir: Path, *,
                 label: str | None = None) -> tuple[Path, Path]:
    """Write both reports into ``out_dir``; returns ``(markdown, json)`` paths."""
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / MATRIX_MARKDOWN_FILENAME
    json_path = out_dir / MATRIX_JSON_FILENAME
    md_path.write_text(render_matrix_markdown(verdict, label=label), encoding="utf-8")
    json_path.write_text(matrix_json_bytes(verdict, label=label), encoding="utf-8")
    return md_path, json_path
