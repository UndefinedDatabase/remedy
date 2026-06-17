# Review Bundle Structured Error Reporting v1

## Problem

Review Bundle sections that fail during assembly previously produced generic
`"error": "build failed"` with no diagnostic information. Operators could not
distinguish optional-data-unavailable (expected) from actual bugs, and had no
way to know what kind of failure occurred or where to look.

## Solution

### Structured section errors

When a section builder fails, the bundle now emits a structured degraded
section instead of a generic error string:

```json
{
  "status": "degraded",
  "reason": "proof_chains.json build failed",
  "error_type": "ImportError",
  "error_category": "import_error",
  "error_message": "No module named 'packages.orchestration.proof_chain'",
  "section_name": "proof_chains.json"
}
```

Error categories: `section_builder_error`, `optional_data_unavailable`,
`import_error`, `validation_error`, `io_error`, `permission_error`,
`unknown_error`.

### Redaction

Exception messages are scrubbed before inclusion:
- API keys (`sk-...`, `ghp_...`, `xoxb-...`, etc.) replaced with `[REDACTED]`
- Private paths (`/home/user/...`) replaced with `[PRIVATE_PATH]`
- Protected paths (`.env`, `credentials.json`, etc.) replaced with `[PROTECTED_PATH]`
- Messages truncated to 240 characters
- No traceback included in public bundle output

### Top-level diagnostics

`ReviewBundleResult` and the exported JSON now include:
- `diagnostics_version`: always `1` for this version
- `degraded_section_count`: number of sections that failed
- `degraded_sections`: list of filenames that degraded
- `section_error_summary`: list of `{section_name, error_type, error_category, error_message}`

The manifest JSON in the zip also includes these fields.

### Section registry

All 37 section builders are registered in `_REVIEW_BUNDLE_SECTION_SPECS`, a
deterministic ordered tuple. Each spec declares filename, builder function,
required flag, description, and argument keys.

`build_review_bundle()` iterates the registry, calling each builder through
`_build_section_safe()`, which handles structured error reporting uniformly.

### Bare exception elimination

All `except Exception:` blocks in `review_bundle.py` were converted to specific
exception types (`ImportError`, `OSError`, `ValueError`, `KeyError`,
`TypeError`, `AttributeError`) for expected failures. Unexpected exceptions
propagate to the wrapper which handles them with structured diagnostics.

One intentional broad catch remains in `_build_section_safe` — it is the
structured reporting entry point that categorizes, redacts, logs, and emits
diagnostic data.

One intentional broad catch remains on `load_job` in `build_review_bundle` —
job loading can fail with multiple exception types depending on storage state.

## How operators should interpret degraded sections

- `error_category == "import_error"`: optional dependency not available. Not a bug.
- `error_category == "io_error"`: data file missing or unreadable. Check data directory.
- `error_category == "validation_error"`: data format issue. May indicate corrupt state.
- `error_category == "section_builder_error"`: unexpected failure. This is a bug — file an issue.
- `error_category == "permission_error"`: file permission issue. Check data directory permissions.

A bundle with `degraded_section_count == 0` is fully healthy.

## What is intentionally not refactored

- `review_bundle.py` is not split into a package (deferred to a future block)
- Individual section builders are not restructured — only the assembly loop
- CLI error handling is unchanged (already graceful)
- No new exception class hierarchy

## Future work

- Split `review_bundle.py` into `packages/orchestration/review_bundle/` package
- Add repo-wide structured logging with correlation IDs
- More specific exception classes for section builders
- Per-section timeout support
