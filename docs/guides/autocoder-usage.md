# Autocoder Usage Guide

## Pipeline Overview

The autocoder pipeline runs in stages:

1. **Builder**: Calls the selected provider (fixture or Ollama) to generate a structured patch
2. **Parse**: Validates the patch format, paths, and safety constraints
3. **Intent**: Creates a patch intent record with change explanations
4. **Approval**: Gates application — requires human approval at autonomy < 3
5. **Apply**: Writes the approved patch to repository files via `source_apply`
6. **Test**: Runs discovered tests against the patched code
7. **Proof**: Records content hash + test result as proof of successful change

Each stage can stop the pipeline with an explicit `stop_reason`.

## Quick Start

### Fixture smoke (CI-safe, no Ollama required)

```sh
remedy do run "fix the add function" --repo /tmp/myrepo --builder-provider fixture --autonomy-level 4 --max-cycles 1 --json
```

### Real Ollama via `remedy do` (requires running Ollama)

```sh
remedy do run "add a hello() function" --repo /tmp/myrepo --builder-provider ollama --autonomy-level 2 --max-cycles 1 --json
```

### Real Ollama smoke via pytest (opt-in)

```sh
REMEDY_REAL_OLLAMA_SMOKE=1 python3 -m pytest tests/orchestration/test_real_do_ollama_smoke.py -v
```

### Free VRAM after testing

```sh
remedy worker unload --provider ollama --all
```

**Warning:** Real Ollama is local, model-quality-dependent, and not guaranteed to produce a valid patch. Output quality varies by model, quantization, and prompt complexity. Normal CI does not require Ollama.

## Builder Providers

| Provider   | What it does                                | When to use                     |
|------------|---------------------------------------------|---------------------------------|
| `none`     | No builder runs (default)                   | Inspection, dry run             |
| `fixture`  | Deterministic fixture, no LLM               | CI, testing, demos              |
| `ollama`   | Calls real local Ollama model               | Local model experiments         |

Select with `--builder-provider none|fixture|ollama`.

Legacy `--fixture-builder true|repair-loop` still works but `--builder-provider` takes precedence.

## Autonomy Levels

| Level | Label    | What happens                                          |
|-------|----------|-------------------------------------------------------|
| 0     | observe  | Dry run, show plan only                               |
| 1     | propose  | Create job + task, no execution                       |
| 2     | generate | Run builder, create patch intent (needs approval)     |
| 3     | apply    | Apply approved patches                                |
| 4     | test     | Run tests after apply                                 |
| 5     | revert   | Revert failed applies                                 |
| 6     | loop     | Repair loop (re-propose after failure)                |

**Recommended first run:** autonomy level 2 (generate). This runs the builder and creates a patch intent, but stops for approval before any repo writes.

## Inspecting Results

### Job summary (JSON output)

```sh
remedy do run "fix the bug" --repo ./myrepo --builder-provider fixture --json
```

Output (version 2) includes:
- `stage`: current pipeline stage
- `stop_reason`: why the pipeline stopped (string, empty on success)
- `provider`: which builder provider was used
- `cycles_run`: number of repair cycles executed
- `structured_patch_created`: whether a structured patch was produced
- `approval_required`: whether human approval is needed
- `source_patch_applied`: whether the patch was applied
- `tests_passed`: whether tests passed after apply

### Dashboard JSON

```sh
remedy do run "fix the bug" --repo ./myrepo --builder-provider fixture --ui
```

Dashboard shows:
- `builder_patch_parsed`: true/false
- `stop_reason`: explicit reason if pipeline stopped
- `repair_loop_cycle`: current cycle number
- `repair_loop_max_cycles`: configured maximum

### Check status

```sh
remedy dev status --json
```

### Inspect patch intents

```sh
remedy patch list <job_id>
remedy patch show <job_id> <intent_id>
```

### Approve or reject a patch

```sh
remedy patch approve <job_id> <intent_id> --reason "looks good"
remedy patch reject <job_id> <intent_id> --reason "unsafe path"
```

### Apply an approved patch

```sh
remedy patch apply <job_id> <intent_id> --json
```

### Run tests for a job

```sh
remedy test run <job_id>
```

## Stop Reasons

When the pipeline stops, the `stop_reason` field explains why:

| Stop Reason                      | Meaning                                    | What To Do                           |
|----------------------------------|--------------------------------------------|--------------------------------------|
| `provider_output_prose_only`     | Model returned narrative, not code         | Adjust prompt or try different model  |
| `provider_output_malformed`      | Model output couldn't be parsed            | Check model compatibility             |
| `unsafe_shell_command`           | Output contained shell commands            | Model tried to run commands           |
| `validation_failed`              | Patch structure invalid (bad paths, etc.)  | Check model output format             |
| `unsafe_path`                    | Absolute path in patch output              | Model used `/` prefix — not allowed   |
| `path_traversal`                 | Path contains `..` traversal               | Model tried to escape repo root       |
| `approval_required`              | Autonomy too low for auto-apply            | Increase autonomy or approve manually |
| `source_apply_failed`            | Patch couldn't be applied to repo          | Check file state and patch format     |
| `test_failed_after_apply`        | Tests failed after patch was applied       | Inspect test output                   |
| `repair_budget_exhausted`        | Max repair cycles reached                  | Increase --max-cycles or fix manually |
| `repeated_patch_detected`        | Same patch produced twice in repair loop   | Model stuck, try different approach   |
| `no_structured_patch_text`       | No patch in builder output                 | Check task description                |
| `provider_unavailable`           | Ollama or provider not reachable           | Start Ollama: `ollama serve`          |
| `test_timeout`                   | Test execution timed out (60s)             | Check test performance                |

## Repair Loop

The repair loop runs up to `--max-cycles` attempts:

1. Build: call builder for structured patch
2. Parse: validate patch format and safety
3. Intent: create patch intent with approval
4. Apply: write patch to repo files
5. Test: run discovered test command
6. If tests fail: build repair context, go to step 1
7. If tests pass: collect proof, stop

The loop stops early on:
- Repeated identical patch (same content hash)
- Parse failure (prose-only, malformed, unsafe)
- Apply failure
- Budget exhaustion (max cycles reached)

## Environment Variables

| Variable                          | Purpose                                    |
|-----------------------------------|--------------------------------------------|
| `REMEDY_REAL_OLLAMA_SMOKE`        | Enable real Ollama smoke test (`=1`)       |
| `REMEDY_OLLAMA_BUILDER_MODEL`     | Override builder model name                |
| `REMEDY_OLLAMA_MODEL`             | Fallback model name                        |
| `REMEDY_OLLAMA_HOST`              | Ollama server URL (default: localhost)     |
| `REMEDY_OLLAMA_BUILDER_TEMPERATURE` | Sampling temperature                     |
| `REMEDY_OLLAMA_BUILDER_NUM_PREDICT` | Max tokens to generate                   |
| `REMEDY_DATA_DIR`                 | Data storage directory                     |
