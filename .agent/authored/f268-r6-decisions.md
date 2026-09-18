
## DECISION F268 D13 (2026-09-18, reviewer, round 6) — the job evidence export writes the four flow artifacts from the job's own records
CONTEXT: R-0892. Measured at `68cf6a13` by the reviewer's research helper: `scripts/build_review_manifest.py`
`REQUIRED_ROOT_ARTIFACTS` names `job_flow.json`, `agent_run_trace.jsonl`,
`agent_run_trace_summary.json` and `command_transcript.json` beside two files the export already
writes; their only writers lived in `apps/cli/commands/do_cmd.py` and left with `do job-flow`
(commit `70c78773`); `packages/orchestration/agent_run_trace.py` still holds the trace builders and
nothing calls them to write files.
CHOSEN: `job_evidence.export_job_evidence` writes the four files at the package root from records
the job already has, never from invented values: the agent run trace and its summary through the
builders in `agent_run_trace.py` over the exported task runs; `job_flow.json` carrying the job id,
the final audit's status from the export's own `final_verifier_report.json`, the missing
observability artifacts computed against the manifest script's own required lists after every
other file is written, and the target guard's `mutated_target` from the export's `target_guard.json`;
`command_transcript.json` carrying only commands the job's records show were executed, in the shape
the deleted writer used (read at `70c78773^`), with an empty list and its reason when there were
none. A field with no source is absent or null, never filled. The check itself is unchanged.
ALTERNATIVES: drop the four files from the required lists, rejected because relaxing a trust check
is a change to that check, which R-0892's own fix clause does not ask for. REVERSE: delete the
writer step; delete this paragraph.

## DECISION F268 D14 (2026-09-18, reviewer, round 6) — the quick start in `remedy --help` is five real lines with a real example order
CHOSEN: `_QUICK_START` in `apps/cli/grouped.py` becomes five numbered command lines, each a real
command with real values and no angle-bracket placeholder: register the repository, check health,
plan an example order without running it, run it, and apply it — the example order being
`Write a CONTRIBUTING.md`, the order T2_F268.md's first Acceptance line uses. The README Quickstart
mirrors the same five lines. A test runs the five lines in order on a fixture repository, with the
fake provider chosen through the repository's own configuration rather than a flag, so every line
stays copyable as printed, and asserts each exits 0. ALTERNATIVES: keep a `"<goal>"` placeholder,
rejected because T005 asks for lines that work as printed. REVERSE: restore `_QUICK_START` and the
README section from git history; delete this paragraph.
