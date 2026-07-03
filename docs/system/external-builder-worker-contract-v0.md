# External Builder Worker Contract v0 (Steps 1681–1716)

How an external worker (another agent or a human) interacts with Remedy's
[External Builder Sandbox](external-builder-sandbox-v0.md). The worker does the *building*; Remedy
does the *governing*. The worker is **never trusted**.

## 1. The worker reads a request package

Remedy exports a safe request package:

```
remedy external-builder package-create <job_id> [--task-id ...] [--route-id ...] --json
```

The package (safe JSON) contains:

- `package_id`, `job_id`, `task_id`, `route_id`, `schema_version`
- `objective` — short, scrubbed goal text
- `safe_context_refs` — failure-artifact IDs + scrubbed `safe_summary` labels (NO raw source/diff/logs)
- `allowed_output_contract`, `forbidden_content_policy`, `max_candidate_bytes`
- `expected_response_schema`, `evidence_refs`, `failure_artifact_id`

The package **never** contains secrets, raw logs, raw diffs, prompt history, or absolute paths.

## 2. Expected response schema

The worker returns **exactly one** candidate, either:

**(a) JSON candidate**
```json
{
  "summary": "short what",
  "rationale": "short why (intended-to-fix framing; NO claims of having applied/tested)",
  "target_files": ["docs/relative/path.md"],
  "unified_diff": "..."          // OR "structured_operations": [{"op":"create","path":"...","content":"..."}]
}
```

**(b) a single fenced unified diff** in a markdown file.

Write the response to a file and submit it:

```
remedy external-builder submit <package_id> --candidate-file <path> --source-label <name> --json
```

## 3. Forbidden content

- No secrets / tokens / credentials / `.env` values.
- No absolute paths; repository-relative paths only.
- No protected / generated / lock files.
- No raw logs / stdout / stderr / tracebacks.
- No claims that the change was **applied, tested, verified, merged, or deployed** — those are
  Remedy's to establish from evidence. "Intended to fix" framing is fine; "tests passed" is not.
- Exactly **one** candidate per submission.

## 4. How Remedy treats the response

The submitted file is bounded (size-capped) and protected (symlink / path-traversal /
protected-path / binary / unreadable inputs are rejected with safe errors). The accepted bytes go
**straight into the existing private quarantine** and then through:

```
quarantine → Trust Gate → Verification → Materialization (if passed) → pending repair intent → approval_required
```

- **The worker is never trusted.** Source label `external_builder:<name>` marks provenance only.
- A submission is **not** an approved intent and **not** completed work. It is `quarantined`,
  `trust_rejected`, `verification_rejected`, `needs_review`, `materialization_failed`, or
  `pending_approval`.
- **Pending approval** arises only when trust + verification pass and a supported materialization
  produced a real, human-approvable intent. A human still approves; `do continue` still applies.

## 5. Quality is judged later, from evidence

```
remedy external-builder evaluate <submission_id> --json
```

Candidate Quality scores the submission by the same evidence rules as local candidates
([candidate-quality-evaluation-v1](candidate-quality-evaluation-v1.md)): no score claims success
without verified proof; rejected/unverified → low; pending ≠ completed. Scorecards aggregate by the
`external_candidate_generator` route + `external_builder:<name>` source, feeding Builder Routing as a
read-only confidence signal (poor history → human review; never auto-runs a worker).

## 6. Why no external execution happens in Remedy

Remedy never launches the external worker, never calls a provider/model SDK, never reaches the
network, never runs a subprocess for the worker, and never auto-applies/approves/tests. The worker
runs **outside** Remedy; Remedy only ingests, governs, and records. This is the safety contract that
lets untrusted external work flow through the same gates as everything else.

## Example (safe, no secrets)

Request package objective: *"Add a missing note to docs/setup.md describing the REMEDY_DATA_DIR env
var."* → worker returns:

```json
{"summary": "Document REMEDY_DATA_DIR",
 "rationale": "Intended to close the docs gap for the data dir env var.",
 "target_files": ["docs/setup.md"],
 "structured_operations": [{"op": "modify", "path": "docs/setup.md", "content": "..."}]}
```

→ `submit` → quarantine → trust accepted → verification passed → pending intent → human approves →
`do continue` applies. No secret, no raw code dump, no execution inside Remedy.
