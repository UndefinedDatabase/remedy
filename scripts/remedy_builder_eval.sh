#!/usr/bin/env bash
# remedy_builder_eval.sh — Run builder prompt quality checks.
#
# Simulated answers (always safe, no network):
#   scripts/remedy_builder_eval.sh --fixture
#   scripts/remedy_builder_eval.sh --fixture --json
#
# Real local model (only when explicitly enabled):
#   REMEDY_REAL_OLLAMA_EVAL=1 scripts/remedy_builder_eval.sh --ollama
#   REMEDY_REAL_OLLAMA_EVAL=1 scripts/remedy_builder_eval.sh --ollama --json
#
# Without REMEDY_REAL_OLLAMA_EVAL=1, --ollama shows simulated results
# and tells you how to enable real model checks.

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

if [ "$MODE" = "ollama" ] && [ -z "${REMEDY_REAL_OLLAMA_EVAL:-}" ]; then
    if [ -z "${JSON_FLAG}" ]; then
        echo "remedy_builder_eval: --ollama requested but REMEDY_REAL_OLLAMA_EVAL is not set."
        echo "  Showing simulated results below."
        echo "  To run with a real local model:"
        echo "    REMEDY_REAL_OLLAMA_EVAL=1 scripts/remedy_builder_eval.sh --ollama"
        echo ""
    fi
    MODE="fixture"
fi

if [ -z "${JSON_FLAG}" ]; then
    if [ "$MODE" = "ollama" ]; then
        echo "remedy_builder_eval: running real local model check (Ollama)"
    else
        echo "remedy_builder_eval: running with simulated answers (no network)"
    fi
fi

"${PYTHON}" -c "
import json
import sys
import os

mode = sys.argv[1]
json_flag = sys.argv[2] if len(sys.argv) > 2 else ''

from packages.orchestration.builder_eval import (
    run_fixture_eval,
    export_eval_report_json,
    standard_eval_cases,
    standard_task_set,
    task_case_to_eval_case,
    build_scorecard,
    export_scorecard_json,
    build_model_profile,
    export_model_profile_json,
    run_single_eval,
)

if mode == 'ollama' and os.environ.get('REMEDY_REAL_OLLAMA_EVAL'):
    try:
        from packages.providers.ollama_builder.provider import OllamaBuilder
        from packages.orchestration.builder_models import TaskExecutionContext
        from uuid import uuid4

        tasks = standard_task_set()
        records = []
        builder = OllamaBuilder()
        for task in tasks:
            if task.patch_json is None:
                from packages.orchestration.builder_eval import EvalRecord
                records.append(EvalRecord(
                    fixture_name=task.name,
                    provider='ollama',
                    model=builder.model,
                    prompt_variant=builder.prompt_profile_name,
                    parse_success=False,
                    parse_error_kind='no_structured_patch_text',
                    stop_reason='no_structured_patch_text',
                ))
                continue
            ctx = TaskExecutionContext(
                job_id=uuid4(), task_id=uuid4(),
                job_prompt=task.user_task,
                task_type='code_change',
                task_description=task.user_task,
            )
            try:
                output = builder.build(ctx)
                record = run_single_eval(
                    builder.prompt_profile_name, output,
                    fixture_name=task.name,
                    provider='ollama',
                    model=builder.model,
                )
                records.append(record)
            except Exception:
                from packages.orchestration.builder_eval import EvalRecord
                records.append(EvalRecord(
                    fixture_name=task.name,
                    provider='ollama',
                    model=builder.model,
                    stop_reason='provider_unavailable',
                ))
        sc = build_scorecard(tasks, records, provider='ollama', model=builder.model,
                             prompt_profile=builder.prompt_profile_name)
        profile = build_model_profile(sc)
        data = export_scorecard_json(sc)
        data['model_profile'] = export_model_profile_json(profile)
    except ImportError:
        print('ERROR: ollama package not installed. pip install ollama', file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f'ERROR: Ollama unavailable: {type(exc).__name__}', file=sys.stderr)
        sys.exit(1)
else:
    cases = standard_eval_cases()
    report = run_fixture_eval('default', cases)
    data = export_eval_report_json(report)

if json_flag == 'yes':
    print(json.dumps(data, indent=2))
else:
    if 'total_cases' in data:
        print(f'Quality Scorecard (profile={data.get(\"prompt_profile\", \"default\")})')
        print(f'  Provider: {data[\"provider\"]}')
        print(f'  Total cases: {data[\"total_cases\"]}')
        print(f'  Usable patch rate: {data[\"usable_patch_rate\"]:.0%}')
        print(f'  Safe rejection rate: {data[\"safe_rejection_rate\"]:.0%}')
        print(f'  Outcome accuracy: {data[\"outcome_accuracy\"]:.0%}')
        print(f'  Needs real model check: {data[\"needs_real_model_check\"]}')
        if data.get('recommendations'):
            print(f'  Recommendations:')
            for r in data['recommendations']:
                print(f'    - [{r[\"confidence\"]}] {r[\"suggestion\"]}')
        print(f'  Redaction: {data[\"redaction\"]}')
    else:
        m = data['metrics']
        print(f'Builder Eval Report (variant={data[\"prompt_variant\"]})')
        print(f'  Provider: {data[\"provider\"]}')
        print(f'  Total cases: {m[\"total_cases\"]}')
        print(f'  Parse success: {m[\"parse_success_count\"]}/{m[\"total_cases\"]} ({m[\"parse_success_rate\"]:.0%})')
        print(f'  Unsafe rejections: {m[\"unsafe_rejection_count\"]}')
        print(f'  Recommendation: {data[\"recommendation\"]}')
        print(f'  Redaction: {data[\"redaction\"]}')
" "${MODE}" "${JSON_FLAG:-}"
