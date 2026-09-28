"""F036 R2 G5 — red-proof tool: mutate result_tour.py's F036 T002 code, prove
each mutation turns tests/orchestration/test_result_tour.py red, restore.

Usage:
    python3 -B .agent/authored/f036-r2-mutations.py <worktree-path>

For each mutation below: edit `packages/orchestration/result_tour.py` INSIDE
the given worktree (asserting the FROM text occurs exactly once), run the
result-tour test file from the worktree's own root with that root FIRST on
sys.path (via PYTHONPATH) after purging `__pycache__`, restore the original
bytes, and print one line: the label, the exit code, the failed count and the
failing node ids. An unmutated control runs first and last. Ends with
"restored byte-identical: <bool>" and "ALL MUTATIONS CAUGHT AND RESTORED
CLEANLY: <bool>".
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

TARGET_REL = "packages/orchestration/result_tour.py"
TEST_REL = "tests/orchestration/test_result_tour.py"

#: (label, FROM text, TO text) — each FROM text must occur exactly once in
#: the unmutated file; each mutation is a real behaviour change S1-S6 of the
#: F036 R2 block names.
MUTATIONS: tuple[tuple[str, str, str], ...] = (
    ("m1 claim check ignores numbers",
     "for number in _TOUR_NUMBER_RE.findall(text):",
     "for number in []:  # MUTATED: ignore numbers"),
    ("m2 claim check ignores backtick spans",
     "for span in _TOUR_BACKTICK_SPAN_RE.findall(text):",
     "for span in []:  # MUTATED: ignore backtick spans"),
    ("m3 claim check ignores paths",
     "for path in _TOUR_PATH_TOKEN_RE.findall(stripped_text):",
     "for path in []:  # MUTATED: ignore paths"),
    ("m4 denylist matched case-sensitively, before lower-casing",
     "if re.search(pattern, lowered):",
     "if re.search(pattern, text):  # MUTATED: case-sensitive"),
    ("m5 mechanical first stop not put first",
     "resolve_tour_stops([mechanical_first, *sound_stops], context)",
     "resolve_tour_stops([*sound_stops, mechanical_first], context)  # MUTATED: order"),
    ("m6 PROVIDER_CALL_ERRORS holds no RuntimeError",
     "types: list[type[BaseException]] = [OSError, RuntimeError, ValueError, ImportError]",
     "types: list[type[BaseException]] = [OSError, ValueError, ImportError]"
     "  # MUTATED: no RuntimeError"),
    ("m7 a generated tour keeps even one stop, no fallback for fewer than two",
     "if len(kept) < 2:",
     "if len(kept) < 1:  # MUTATED: no fallback for one"),
    ("m8 a not-ok outcome is labelled summary-role",
     '''    if not outcome.ok:
        classification = classify(
            FailureSignals(error_class=outcome.error_class, error_text=outcome.hint))
        return _assemble_fallback_tour(
            job, sources, context,
            f"{TOUR_GENERATOR_FALLBACK}:{classification.failure_class.value}")''',
     '''    if not outcome.ok:
        classification = classify(
            FailureSignals(error_class=outcome.error_class, error_text=outcome.hint))
        return _assemble_fallback_tour(
            job, sources, context,
            TOUR_GENERATOR_SUMMARY_ROLE)  # MUTATED: mislabeled'''),
    ("m9 tour_call_fn binds GeneratedSummaryContent from artifact_summary instead",
     "return make_structured_call_fn(GeneratedTourContent, model=role_cfg.model)",
     "from packages.orchestration.artifact_summary import "
     "GeneratedSummaryContent as _MutatedContent\n"
     "    return make_structured_call_fn(_MutatedContent, model=role_cfg.model)"
     "  # MUTATED: wrong schema"),
    ("m10 the structured call is made with allow_parse_retry=False",
     "GeneratedTourContent, prompt, call_fn, on_call=on_call, allow_parse_retry=True,",
     "GeneratedTourContent, prompt, call_fn, on_call=on_call, allow_parse_retry=False,"
     "  # MUTATED"),
)

_FAILED_COUNT_RE = re.compile(r"(\d+) failed")
_FAILED_NODE_RE = re.compile(r"^FAILED (\S+)", re.MULTILINE)


def _purge_pycache(root: Path) -> None:
    for directory in root.rglob("__pycache__"):
        if directory.is_dir():
            shutil.rmtree(directory, ignore_errors=True)


def _run_tests(root: Path) -> tuple[int, int, list[str]]:
    """Run the result-tour test file inside *root*; (exit_code, failed_count, failing_ids)."""
    _purge_pycache(root)
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(root) + (os.pathsep + existing if existing else "")
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST_REL],
        cwd=str(root), env=env, capture_output=True, text=True,
    )
    output = proc.stdout + proc.stderr
    failed_match = _FAILED_COUNT_RE.search(output)
    failed_count = int(failed_match.group(1)) if failed_match else 0
    failing_ids = _FAILED_NODE_RE.findall(output)
    return proc.returncode, failed_count, failing_ids


def _report(label: str, exit_code: int, failed_count: int, failing_ids: list[str]) -> None:
    print(f"{label}: exit={exit_code} failed={failed_count} nodes={failing_ids}")


def main() -> None:
    worktree = Path(sys.argv[1]).resolve()
    target = worktree / TARGET_REL
    original_bytes = target.read_bytes()
    original_text = original_bytes.decode("utf-8")

    exit_code, failed_count, failing_ids = _run_tests(worktree)
    _report("control (before)", exit_code, failed_count, failing_ids)
    control_before_ok = exit_code == 0 and failed_count == 0

    all_caught = True
    for label, from_text, to_text in MUTATIONS:
        occurrences = original_text.count(from_text)
        assert occurrences == 1, f"{label}: FROM text occurs {occurrences} times, not 1"
        mutated_text = original_text.replace(from_text, to_text, 1)
        target.write_text(mutated_text, encoding="utf-8")
        try:
            exit_code, failed_count, failing_ids = _run_tests(worktree)
        finally:
            target.write_bytes(original_bytes)
        _report(label, exit_code, failed_count, failing_ids)
        if failed_count < 1:
            all_caught = False

    exit_code, failed_count, failing_ids = _run_tests(worktree)
    _report("control (after)", exit_code, failed_count, failing_ids)
    control_after_ok = exit_code == 0 and failed_count == 0

    restored = target.read_bytes() == original_bytes
    print(f"restored byte-identical: {restored}")

    overall = all_caught and control_before_ok and control_after_ok and restored
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {overall}")


if __name__ == "__main__":
    main()
