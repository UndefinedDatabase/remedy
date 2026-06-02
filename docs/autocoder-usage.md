# Autocoder Usage Guide

## Quick Start

### Fixture smoke (CI-safe, no Ollama required)

```sh
remedy do "fix the add function" --repo /tmp/myrepo --fixture-builder true --autonomy-level 4 --max-cycles 1 --json
```

### Real Ollama smoke (pytest only, not wired to `remedy do`)

Real Ollama integration is tested via pytest, not the CLI:

```sh
REMEDY_REAL_OLLAMA_SMOKE=1 python3 -m pytest tests/orchestration/test_real_ollama_smoke.py -v
```

The `remedy do` command does not yet invoke OllamaBuilder directly.
That integration is a future step.

### Free VRAM after testing

```sh
ollama stop <model-name>
```

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

**Recommended first run:** autonomy level 3 (apply). This creates the patch and applies it, but does not auto-run tests. You can inspect the result before proceeding.

## Inspecting Results

### Job summary (JSON output)

```sh
remedy do "fix the bug" --repo ./myrepo --fixture-builder true --json
```

Output includes:
- `stage`: current pipeline stage
- `cycles_run`: number of repair cycles executed
- `structured_patch_created`: whether a structured patch was produced
- `approval_required`: whether human approval is needed
- `source_patch_applied`: whether the patch was applied
- `tests_passed`: whether tests passed after apply

### Dashboard JSON

```sh
# Start with UI:
remedy do "fix the bug" --repo ./myrepo --fixture-builder true --ui

# Dashboard shows:
# - builder_patch_parsed: true/false
# - stop_reason: explicit reason if pipeline stopped
# - repair_loop_cycle: current cycle number
# - repair_loop_max_cycles: configured maximum
```

## Stop Reasons

When the pipeline stops, the `stop_reason` field explains why:

| Stop Reason                      | Meaning                                    | What To Do                           |
|----------------------------------|--------------------------------------------|--------------------------------------|
| `provider_output_prose_only`     | Model returned narrative, not code         | Adjust prompt or try different model  |
| `provider_output_malformed`      | Model output couldn't be parsed            | Check model compatibility             |
| `unsafe_shell_command`           | Output contained shell commands            | Model tried to run commands           |
| `unsafe_path` / `path_traversal`| Output targeted dangerous paths            | Model tried to write outside repo     |
| `validation_failed`              | Patch structure invalid                    | Check model output format             |
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
