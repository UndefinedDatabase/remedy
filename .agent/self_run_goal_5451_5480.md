# Steps 5451-5480: Prompt Trace Lens Completion + Verification v1

## Product goal

Complete the Prompt Trace Lens UI v1 feature. Two prior runs produced partial work that was not accepted. This run carries forward all accepted pieces, fixes all blockers, and delivers a complete feature.

## What to carry forward (already accepted, do NOT rewrite from scratch)

The following patterns are accepted and must be preserved in this run:

**Backend** (`packages/orchestration/ui_server.py`):
- `_build_prompt_trace(ev_dir)` function that reads `task_runs/*/prompt_trace.jsonl`
- `_redact_preview(text)` with broad path sanitization covering `/tmp/`, `/home/`, `/Users/`, `/private/`, `/mnt/`, `.data/job_workspaces/`, `remedy-pingpong-*`
- `_safe_rel_file(name)` preserving repo-relative structure via `_REPO_ROOT_MARKERS`
- `_PATH_REDACTIONS` list of compiled regex → placeholder pairs
- `_PROMPT_TRACE_PREVIEW_MAX = 1200` cap on redacted preview
- Missing trace → explicit `"absent"` source with `missingReason`
- No raw `prompt_text` or `prompt_text_redacted` fields in output items
- Evidence refs as relative paths only
- `prompt_trace` key added to job-plan dashboard payload

**Frontend graph** (`apps/ui/src/components/graph/BrainGraphCanvas.tsx`):
- `DisplayNode` extended with `kind: "root" | "task" | "prompt"` plus `color`, `promptRole`, `promptKind`, `doubleRing`, `nodeId`
- `buildDisplayModel()` exported and creates prompt satellite nodes from `dashboard.promptTrace?.items`
- Prompt colors: builder=#4c83ff, reviewer=#a78bfa, repair=#f59e0b
- Re-review → `doubleRing: true`
- Prompt nodes clickable, filter-aware (ride parent task visibility), do not inflate task count
- SVG render: small circle, double-ring stroke for re-review, selection ring

**Frontend shell** (`apps/ui/src/components/shell/RemedyShell.tsx`):
- Prompt node click → resolve to owning task node via `promptTrace.items` lookup
- Pass `promptHighlight` to `DetailPopover`

**Evidence** (`packages/orchestration/job_evidence.py`):
- `_build_workspace_diff()` emits full per-file diff (no 200-line per-file cap)
- 500K char total cap for pathological cases

## What to fix / add

### Blocker 1: Test fixture redaction safety

Previous runs had test files where a variable assignment like `secret = "..."` was corrupted by the safe.diff redactor into `secret=[REDACTED]`, producing invalid Python.

**Rule for ALL test files in this run:** Never use variable names like `secret`, `password`, `token`, `key`, `credential`, or `api_key` in test fixtures. Never use strings containing words like `SECRET`, `SYSTEM PROMPT`, `API_KEY`, or similar patterns that trigger redaction.

Instead use completely benign patterns:
```python
marker_string = "TOP_LEVEL_PROMPT_BODY_SHOULD_NOT_LEAK_INTO_DASHBOARD"
```

This string:
- Does not contain words that trigger safe.diff redaction
- Is distinctive enough to search for in serialized output
- Proves the same thing (no raw prompt body leaks)

Apply this rule to every test file. Do not use `secret=` anywhere.

### Blocker 2: PromptTracePanel component

Create two new files:

`apps/ui/src/components/prompt/PromptTracePanel.tsx`
`apps/ui/src/components/prompt/PromptTracePanel.module.css`

The panel shows prompt details for a task or highlighted prompt. It must display per prompt card:

- Role label: "Builder", "Reviewer", "Repair", "Re-review", "System"
- Round number
- Provider name
- Estimated tokens
- Prompt hash (first 8 chars)
- Changed files (first 3, with +N overflow)
- Evidence ref
- Redacted prompt preview in a collapsed `<details>` element
- Truncation indicator when preview was capped
- Visual highlight when a prompt is selected

CSS direction: pale blue, glass, quiet, premium. Left accent rail per role (builder=blue, reviewer=green/purple, repair=amber). No dark mode required.

Integration:
- Import `PromptTracePanel` into `DetailPopover.tsx`
- When selected node is a task: show all prompts for that task
- When selected node is a prompt: show owning task's prompts with the clicked prompt highlighted
- Filter prompts by `taskId` matching the selected task's id

### Blocker 3: Full frontend types

The frontend types must preserve all backend fields. In `apps/ui/src/api/types.ts`:

```ts
export type RemedyPromptRole = "builder" | "reviewer" | "system";
export type RemedyPromptKind = "initial" | "review" | "repair" | "re-review" | "unknown";

export interface RemedyPromptTraceItem {
  id: string;
  taskId: string;
  runId: string;
  round: number;
  role: RemedyPromptRole;
  promptKind: RemedyPromptKind;
  provider: string;
  providerKind: string;
  promptSha256: string;
  promptChars: number;
  promptTokensEstimated: number;
  contextCategories: string[];
  changedFilesSafe: string[];
  safeDiffFiles: string[];
  evidenceRef: string;
  redactedPreview: string;
  redactedPreviewTruncated: boolean;
  findingIds?: string[];
}

export interface RemedyPromptTraceSummary {
  totalPrompts: number;
  builderPrompts: number;
  reviewerPrompts: number;
  repairPrompts: number;
  totalPromptTokensEstimated: number;
  items: RemedyPromptTraceItem[];
  source: "prompt_trace_jsonl" | "absent";
  missingReason?: string;
}
```

Update `RemedyDashboard` to include `promptTrace?: RemedyPromptTraceSummary | null`.

In `apps/ui/src/api/remedyApi.ts`, the `normalizePromptTrace()` function must map ALL fields from the backend payload, not just 5. Handle both snake_case and camelCase keys. Default missing fields to safe values (empty string, 0, empty array).

### Blocker 4: Activity feed improvements

In `apps/ui/src/api/remedyApi.ts`, add event label mappings:
```ts
builder_prompt_created: { actor: "Builder", kind: "build", label: "Builder prompt created" },
reviewer_prompt_created: { actor: "Reviewer", kind: "review", label: "Reviewer prompt created" },
repair_prompt_created: { actor: "Builder", kind: "build", label: "Repair prompt created" },
review_finding_rechecked: { actor: "Reviewer", kind: "review", label: "Reviewer re-check" },
```

Detect re-review: if `event_kind === "reviewer_prompt_created"` and `prompt_kind === "re-review"`, use label "Reviewer re-check".

Add `taskId` and `tokenEstimate` to `RemedyActivityItem`:
```ts
export interface RemedyActivityItem {
  id: string;
  actor: "Builder" | "Reviewer" | "User" | "System";
  message: string;
  timeLabel: string;
  kind: "build" | "review" | "user" | "system" | "test";
  taskId?: string;
  tokenEstimate?: number;
}
```

In `ActivityFeedCard.tsx`, show task ID and token estimate as compact chips when available.

In `packages/orchestration/ui_server.py`, ensure the activity event metadata includes `task_id`, `prompt_kind`, and `prompt_chars` (estimate tokens as `prompt_chars // 4`).

Add `.activityTag` CSS class to `RightLivePanel.module.css`.

### Blocker 5: workspace.diff truncation

Carry forward the fix from the previous run to `packages/orchestration/job_evidence.py`:
- Remove the 200-line per-file cap in `_build_workspace_diff()`
- Emit all unified diff lines per file
- Add a 500,000 char total cap to prevent pathological cases
- When total cap is hit, append `# ... diff truncated at 500000 chars total`
- No `# ... N more lines truncated` markers

## Task 1: Backend completion — path sanitization + prompt trace payload + activity metadata

Carry forward and verify the backend changes:

1. `_PATH_REDACTIONS`, `_redact_preview()`, `_safe_rel_file()` with `_REPO_ROOT_MARKERS` — broad path sanitization
2. `_build_prompt_trace(ev_dir)` — full prompt trace section builder
3. `_PROMPT_TRACE_PREVIEW_MAX = 1200`
4. `_empty_prompt_trace(reason)` for explicit absent states
5. `prompt_trace` added to dashboard payload via `_build_job_plan_dashboard()`
6. Activity event metadata: `task_id`, `prompt_kind`, `prompt_chars` fields passed through
7. Activity items: `token_estimate = prompt_chars // 4` when `prompt_chars > 0`

Also carry forward the workspace.diff fix in `packages/orchestration/job_evidence.py`:
- Remove 200-line per-file cap
- Add 500K char total cap

Acceptance:
- `_redact_preview()` strips all listed path families
- `_safe_rel_file()` preserves repo-relative structure
- `_build_prompt_trace()` returns full items with all fields
- Missing trace → explicit absent with reason
- No `prompt_text` or `prompt_text_redacted` in output items
- Evidence refs are relative
- Activity metadata includes task_id, prompt_kind, prompt_chars
- workspace.diff has no `# ... N more lines truncated`

## Task 2: Frontend types + normalization + activity improvements

1. Add full `RemedyPromptTraceItem`, `RemedyPromptTraceSummary`, `RemedyPromptRole`, `RemedyPromptKind` types to `types.ts`
2. Add `promptTrace?: RemedyPromptTraceSummary | null` to `RemedyDashboard`
3. Add `taskId?: string` and `tokenEstimate?: number` to `RemedyActivityItem`
4. Implement `normalizePromptTrace()` in `remedyApi.ts` mapping ALL fields (handle snake_case + camelCase)
5. Add activity event labels for prompt events
6. Detect re-review in activity normalization

Acceptance:
- All 17 fields mapped in normalizePromptTrace
- Unknown role → "system", unknown kind → "unknown"
- Missing fields → safe defaults
- Activity labels include prompt events
- RemedyDashboard includes promptTrace

## Task 3: Visible graph prompt nodes + PromptTracePanel

1. Carry forward `BrainGraphCanvas.tsx` changes:
   - `DisplayNode` extended with prompt fields
   - `buildDisplayModel()` exported, creates prompt satellite nodes
   - Role colors, double-ring, clickable, filter-aware
   - SVG prompt node rendering

2. Create `PromptTracePanel.tsx` and `PromptTracePanel.module.css`:
   - Shows prompt cards with role, round, provider, tokens, hash, files, evidence ref
   - Redacted preview in collapsed `<details>`
   - Selected prompt highlighted
   - Left accent rail per role
   - Premium quiet glass style

3. Integrate into `DetailPopover.tsx`:
   - Import PromptTracePanel
   - Filter prompts by selected task's id
   - Pass selectedPromptId for highlight

4. Update `RemedyShell.tsx`:
   - Prompt node click → resolve owning task + pass prompt highlight
   - Pass selectedPromptId or promptHighlight to DetailPopover

5. Update `ActivityFeedCard.tsx`:
   - Show taskId and tokenEstimate chips
   - Add `.activityTag` to `RightLivePanel.module.css`

Acceptance:
- PromptTracePanel.tsx and .module.css exist
- Prompt cards show all required fields
- Redacted preview collapsed by default
- Selected prompt highlighted
- DetailPopover integrates PromptTracePanel
- Prompt node click → owning task + highlight
- Activity chips for taskId and tokens
- Prompt nodes in visible graph (BrainGraphCanvas)

## Task 4: Tests — redaction-safe fixtures

CRITICAL: Do NOT use variable names `secret`, `password`, `token`, `key`, `credential`, `api_key` in any test file. Do NOT use strings containing `SECRET`, `SYSTEM PROMPT`, `API_KEY`, or similar redaction-triggering patterns.

Use benign marker strings like:
```python
marker_string = "TOP_LEVEL_PROMPT_BODY_SHOULD_NOT_LEAK_INTO_DASHBOARD"
```

### Backend tests (`tests/ui_server/test_prompt_trace_payload.py`)

At least 13 tests:
- Dashboard includes prompt trace items from prompt_trace.jsonl
- Repair prompts counted
- Preview truncated at 1200 chars
- Short preview not marked truncated
- No raw unredacted prompt field (use `marker_string` not `secret`)
- Evidence refs are relative
- Missing evidence dir → absent
- Missing task_runs → absent
- Missing jsonl → absent
- Prompt items independent of task count
- Unknown role/kind normalized
- Malformed JSON lines skipped
- Token estimate summed correctly

### Backend tests (`tests/ui_server/test_prompt_trace_lens.py`)

At least 10 tests:
- No raw prompt field leaks (use `marker_string`)
- `/home/` stripped from preview
- `/tmp/` stripped from preview
- `/Users/` stripped from preview
- `/mnt/` stripped from preview
- `.data/job_workspaces/` stripped from preview
- `/home/` and `/tmp/` stripped from changedFilesSafe
- No absolute paths in serialized section
- Repo-relative structure preserved in changedFilesSafe
- Private path stripped from preview

### Frontend tests (`apps/ui/src/components/prompt/promptTraceLens.test.ts`)

At least 8 tests:
- normalizePromptTrace maps all fields
- Unknown role/kind normalized
- Absent state explicit
- buildDisplayModel creates prompt nodes in visible graph
- Prompt nodes do not inflate task count
- Prompt node has correct role color
- Selecting a task surfaces its prompts
- Empty prompt set for task without trace

Acceptance:
- All test files are valid Python / TypeScript (no syntax errors)
- No `secret=` or `SECRET` patterns that trigger safe.diff redaction
- At least 31 total tests
- Tests prove path sanitization breadth
- Tests prove no raw prompt leak
- Tests prove visible graph integration

## Task 5: Verification + evidence quality

After Tasks 1-4 are implemented, verify evidence quality:

1. Check that workspace.diff contains no `# ... more lines truncated` markers
2. Check that workspace.diff contains no `[DIFF TRUNCATED]` markers
3. Verify all test files are syntactically valid Python (python3 -c "compile(open('file').read(), 'file', 'exec')")
4. If pytest can run, execute: `python3 -m pytest tests/ui_server/test_prompt_trace_lens.py tests/ui_server/test_prompt_trace_payload.py -q`
5. If pytest cannot run due to sandbox, report honestly and set status to NEEDS_REVIEW not READY_FOR_APPROVAL

Do NOT fabricate test results. Do NOT claim tests passed if they did not run.

Acceptance:
- workspace.diff is clean (no truncation markers)
- All test files compile without syntax errors
- Test execution results reported honestly
- If tests could not run, status is NEEDS_REVIEW or BLOCKED, not READY_FOR_APPROVAL
