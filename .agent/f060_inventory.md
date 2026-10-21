# F060 inventory — the review package's layers and a finished job's records

Read at `646c4b1d7` (the merge commit of pull request 374) for DECISION F060 D1. Line numbers are
those of that commit.

## The review package, layer by layer
- `scripts/make_review_zip.sh` (733 lines) drives the package: it resolves the checkout with
  `git rev-parse --show-toplevel`, selects and stages a job's evidence, stages the review reports,
  builds the manifest and calls the ZIP builder. It needs a checkout throughout.
- `scripts/build_review_manifest.py` (3495 lines, on the structure ledger) builds the root
  manifest; `_git` reads the checkout, and `_check_bundle_integrity` hashes files against the
  `file_hashes` of `current_change_content_proof.json`.
- `scripts/build_review_zip.py` (`main` on the structure ledger at 317 lines) coordinates the
  build and publishes it through `safe_publish`.
- `packages/orchestration/archive_plan.py`: `build_archive_plan(*, repo_root, subject, ...)` needs
  a repository root and a `ReviewSubjectV1`; its caps are 64 MiB per member, 2 GiB in total and
  16 MiB per generated member (`MAX_GENERATED_MEMBER_BYTES`), and a member over 1 MiB that expands
  more than 200 times on reading is refused as a bomb.
- `packages/orchestration/review_zip.py` (425 lines, not on the ledger), the one layer with no
  checkout: `build_review_zip_from_snapshot(*, out_path, snapshot, generated_members)` writes a ZIP
  from in-memory bytes with the fixed timestamp 1980-01-01, Unix type and mode bits and deflate,
  and returns `{"members", "model"}` with each member's `kind`, `mode`, `sha256`, `size`;
  `verify_review_zip(out_path, expected)` reopens a ZIP and answers a list of problems: missing,
  unexpected or duplicate members, type, mode, timestamp, size, hash, encryption, compression
  method and the bomb bounds. `validate_archive_name` refuses absolute, `..`, empty or `.`
  segments, backslashes and NUL.
- `packages/orchestration/job_evidence.py` (2992 lines, on the ledger): `export_job_evidence` (718
  lines, on the ledger) writes a job's evidence export into a folder, among its files
  `token_truth.json`, `final_verifier_report.json`, `job_flow.json`, `ownership.json`,
  `current_change_content_proof.json`, `workspace.diff`, `result.diff` and the run manifest's
  export; it writes no per-member hash manifest of its own.

## A finished job's records
- `packages/orchestration/data_paths.py`: `job_dir` is `<root>/jobs/<id>`, `job_record_path` its
  `job.json`, `job_evidence_dir` its `evidence/`, `job_dod_path` `evidence/dod.json`,
  `job_evidence_export_dir` `<root>/evidence_exports/<id>`, `resolve_job_id` the id a person types.
- The report: `evidence/report.md`, `run_report.report_path` and `write_final_report`; the
  structured sources `build_report_sources(job)` answer `ReportSources`, whose fields
  `terminal_status`, `token_description`, `cost_description`, `cost_basis`, `dod_released`,
  `dod_checks` and `open_decision_count` are the claims' natural source.
- The token truth: `token_truth.build_token_truth(evidence_dir)` and `write_token_truth`, checked by
  `token_authority.validate_token_truth`.
- The verdicts: `dod_gate.load_gate_result` (`dod_result.json`) and
  `final_verifier.build_final_verifier_report` (`final_verifier_report.json`).
- The ownership: `ownership.json`, written at a run's end by
  `pingpong_job._write_ownership_ledger_at_run_end`, built by `ownership.build_ownership_ledger`.
- The run manifest: `run_manifests/<episode>/run_manifest.json` and `run_manifest_index.json`, read
  by `run_manifest.load_latest_manifest_verified`; its module docstring carries the honesty
  sentence that inputs are verified and outputs recorded.
- Regression status has no producer of its own; the nearest is
  `final_verifier._aggregate_test_status`.

## The command line
- Every command is a group and a subcommand in `apps/cli/command_catalog.py` (on the ledger at 2314
  lines); a top-level `remedy verify` needs a `GroupDef` in `GROUPS`, an entry in
  `_DEFAULT_COMMAND` of `apps/cli/grouped.py`, and, when visible, a place in
  `VISIBLE_GROUP_ORDER`, which `tests/test_command_catalog.py` pins.
- Handlers are collected by `collect_all_handlers` in `apps/cli/commands/__init__.py`;
  `apps/cli/commands/job.py` is on the ledger at 2483 lines, so `job certificate` needs a module
  of its own.
- Exit codes come from `apps/cli/exit_codes.py` (1 failed, 3 not ready, 4 environment) and are
  listed in `docs/guides/exit-codes.md`; the guards that read a new command are
  `tests/test_command_catalog.py`, `tests/cli/test_advertised_commands.py`,
  `tests/cli/test_exit_codes.py`, `tests/orchestration/test_dead_command_check.py` and
  `tests/docs/test_vocabulary.py`.

## Absences
No `verify` command, no `job certificate` command, no module or test about certificates; the word
appears only for TLS certificate files in `sensitive_paths.py`, `archive_plan.py` and
`tool_sandbox.py`.
