# Context

## Active Branch
`feature/step8-repo-attachment`

## PR
None yet — will create after Step 8 is complete.

## Scope
Step 8 + 8.5: Controlled repo attachment and safe generated-file application,
plus repo applicator rule hardening (narrowed keyword table, stale-path check).
Branched from feature/step6-workspace-runtime (PR chain — Step 8 depends on
workspace/verifier code that is not yet merged to main).

## Constraints
- No Docker, no shell, no Git, no patch application
- No arbitrary LLM paths into repo writes — static keyword mapping only
- No overwriting existing repo files
- Repo writes boundary-safe: resolved path must remain inside repo_root (RuntimeError otherwise)
- Repo application only on vr.passed AND job.metadata["target_repo"] set AND keyword matched
- Stale repo path → CLI warns + skips, never fails task completion
- workspace_file and repo_applied_files are separate metadata keys
- Failed artifacts retained in job.artifacts (detached from task.output_artifact_ids after failure)
- finalize_task raises RuntimeError if output_artifact_ids empty or artifact not found on failure
- Eligible keywords: readme, changelog, architecture, design, guide, documentation, doc,
  plan, spec, requirement, acceptance, analysis
- Ineligible (removed): implementation, prepare, define, summarize, summary

## Assumptions
- LocalWorkspaceRuntime is the only runtime; Docker runtime is future
- Workspace root follows same REMEDY_DATA_DIR resolution as storage.py
- target_repo is stored as str (absolute path) in job.metadata["target_repo"]
- Repo markdown content is derived from artifact metadata + content (not workspace file)
