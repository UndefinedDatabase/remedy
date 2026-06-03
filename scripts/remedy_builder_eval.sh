#!/usr/bin/env bash
# remedy_builder_eval.sh — Run builder prompt evaluation.
#
# Fixture mode (always safe, no network):
#   scripts/remedy_builder_eval.sh --fixture
#
# Real Ollama mode (opt-in, requires local Ollama):
#   scripts/remedy_builder_eval.sh --ollama
#
# JSON output:
#   scripts/remedy_builder_eval.sh --fixture --json

set -euo pipefail

PYTHON="${REMEDY_PYTHON:-python3}"
MODE="fixture"
JSON_FLAG=""

for arg in "$@"; do
    case "$arg" in
        --fixture) MODE="fixture" ;;
        --ollama)  MODE="ollama" ;;
        --json)    JSON_FLAG="yes" ;;
        *) echo "Unknown argument: $arg" >&2; exit 1 ;;
    esac
done

if [ -z "${JSON_FLAG}" ]; then
    if [ "$MODE" = "ollama" ]; then
        echo "remedy_builder_eval: REMEDY_REAL_OLLAMA_EVAL=1 exported for pytest"
        echo "remedy_builder_eval: fixture eval shown below; use pytest for real Ollama tests"
    else
        echo "remedy_builder_eval: running fixture mode (no network)"
    fi
fi

if [ "$MODE" = "ollama" ]; then
    export REMEDY_REAL_OLLAMA_EVAL=1
fi

"${PYTHON}" -c "
import json
import sys

from packages.orchestration.builder_eval import (
    run_fixture_eval,
    export_eval_report_json,
    standard_eval_cases,
)

cases = standard_eval_cases()
report = run_fixture_eval('default', cases)
data = export_eval_report_json(report)

json_flag = sys.argv[1] if len(sys.argv) > 1 else ''
if json_flag == 'yes':
    print(json.dumps(data, indent=2))
else:
    m = data['metrics']
    print(f'Builder Eval Report (variant={data[\"prompt_variant\"]})')
    print(f'  Provider: {data[\"provider\"]}')
    print(f'  Total cases: {m[\"total_cases\"]}')
    print(f'  Parse success: {m[\"parse_success_count\"]}/{m[\"total_cases\"]} ({m[\"parse_success_rate\"]:.0%})')
    print(f'  Unsafe rejections: {m[\"unsafe_rejection_count\"]}')
    print(f'  Avg tokens: {m[\"average_estimated_tokens\"]:.0f}')
    print(f'  Recommendation: {data[\"recommendation\"]}')
    if m['failure_counts_by_error_kind']:
        print(f'  Failures: {m[\"failure_counts_by_error_kind\"]}')
    if m['stop_reason_counts']:
        print(f'  Stop reasons: {m[\"stop_reason_counts\"]}')
    print(f'  Redaction: {data[\"redaction\"]}')
" "${JSON_FLAG:-}"
