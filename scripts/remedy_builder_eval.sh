#!/usr/bin/env bash
# remedy_builder_eval.sh — Check builder output quality.
#
# Example runs (always safe, no network):
#   scripts/remedy_builder_eval.sh --example
#   scripts/remedy_builder_eval.sh --example --json
#
# Real local model (only when explicitly enabled):
#   REMEDY_REAL_OLLAMA_EVAL=1 scripts/remedy_builder_eval.sh --ollama
#   REMEDY_REAL_OLLAMA_EVAL=1 scripts/remedy_builder_eval.sh --ollama --json
#
# --fixture is an alias for --example.
# --ollama without REMEDY_REAL_OLLAMA_EVAL=1 exits with error.

set -euo pipefail

PYTHON="${REMEDY_PYTHON:-python3}"
MODE="example"
JSON_FLAG=""

for arg in "$@"; do
    case "$arg" in
        --example|--fixture) MODE="example" ;;
        --ollama) MODE="ollama" ;;
        --json) JSON_FLAG="yes" ;;
        *) echo "Unknown argument: $arg" >&2; exit 1 ;;
    esac
done

if [ "$MODE" = "ollama" ] && [ -z "${REMEDY_REAL_OLLAMA_EVAL:-}" ]; then
    echo "ERROR: --ollama requires REMEDY_REAL_OLLAMA_EVAL=1" >&2
    echo "" >&2
    echo "  To run with a real local model:" >&2
    echo "    REMEDY_REAL_OLLAMA_EVAL=1 scripts/remedy_builder_eval.sh --ollama" >&2
    echo "" >&2
    echo "  For example runs (no network):" >&2
    echo "    scripts/remedy_builder_eval.sh --example" >&2
    exit 1
fi

if [ -z "${JSON_FLAG}" ]; then
    if [ "$MODE" = "ollama" ]; then
        echo "remedy_builder_eval: running real local model check (Ollama)"
    else
        echo "remedy_builder_eval: running example checks (no network)"
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
    recommend_prompt_changes,
    run_single_eval,
)

if mode == 'ollama':
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
        recs = recommend_prompt_changes(sc)
        data = export_scorecard_json(sc)
        data['model_profile'] = export_model_profile_json(profile)
    except ImportError:
        print('ERROR: ollama package not installed. pip install ollama', file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f'ERROR: local model unavailable: {type(exc).__name__}', file=sys.stderr)
        sys.exit(1)
else:
    tasks = standard_task_set()
    cases = [task_case_to_eval_case(t) for t in tasks]
    records = [run_single_eval('default', c.builder_output, fixture_name=c.name) for c in cases]
    sc = build_scorecard(tasks, records)
    profile = build_model_profile(sc)
    recs = recommend_prompt_changes(sc)
    data = export_scorecard_json(sc)
    data['model_profile'] = export_model_profile_json(profile)

if json_flag == 'yes':
    print(json.dumps(data, indent=2))
else:
    print(f'Model Quality Report (profile={data.get(\"prompt_profile\", \"default\")})')
    print(f'  Provider: {data[\"provider\"]}')
    print(f'  Total tasks: {data[\"total_cases\"]}')
    print(f'  Usable patch rate: {data[\"usable_patch_rate\"]:.0%}')
    print(f'  Safe rejection rate: {data[\"safe_rejection_rate\"]:.0%}')
    print(f'  Outcome accuracy: {data[\"outcome_accuracy\"]:.0%}')
    print(f'  Avg tokens: {data[\"average_tokens\"]:.0f}')
    print(f'  Needs real model check: {data[\"needs_real_model_check\"]}')
    mp = data.get('model_profile', {})
    if mp:
        print(f'  Confidence: {mp.get(\"confidence\", \"low\")}')
        print(f'  Recommendation: {mp.get(\"recommendation\", \"\")}')
    if data.get('recommendations'):
        print(f'  Advice:')
        for r in data['recommendations']:
            print(f'    - [{r[\"confidence\"]}] {r[\"suggestion\"]}')
    print(f'  Redaction: {data[\"redaction\"]}')
" "${MODE}" "${JSON_FLAG:-}"
