# Steps 5421-5450: Prompt Trace Lens UI Repair + Real Graph Path Verification v1

## Product goal

Repair the Prompt Trace Lens UI v1 delivered in Steps 5391-5420 (job `99c7cf6d3e5d4eb6`). The previous run produced working code, but final review found five blockers:

1. A Python test has a syntax error (unterminated string literal).
2. Prompt nodes were added to `ForceBrainGraph.tsx` but the visible UI renders `BrainGraphCanvas.tsx` — prompt nodes never appear.
3. `workspace.diff` evidence truncates per-file diffs at 200 lines (`# ... N more lines truncated`).
4. Backend path sanitization is too narrow (only strips `/tmp/remedy-pingpong-*`).
5. Tests were not executed during the self-run.

This run fixes all five while carrying forward the accepted work.

## Current state

The previous run staged code across 17 files. That code lives in the staging workspace for job `99c7cf6d3e5d4eb6`. The staged code is NOT applied to the target repo. Read the safe.diff files in `remedy-job-evidence-selfrun-5391-5420-r2/task_runs/T*/safe.diff` for reference.

Key files already modified by the previous run (carry forward and fix):
- `packages/orchestration/ui_server.py` — `_build_prompt_trace_section()`, `_redact_preview()`, activity event improvements
- `apps/ui/src/api/remedyApi.ts` — `normalizePromptTrace()`, activity improvements
- `apps/ui/src/api/types.ts` — `RemedyPromptTraceItem`, `RemedyPromptTraceSummary`, `RemedyActivityItem` extensions
- `apps/ui/src/components/graph/ForceBrainGraph.tsx` — prompt node rendering (WRONG PATH)
- `apps/ui/src/components/graph/buildForceBrainModel.ts` — prompt node model building (WRONG PATH)
- `apps/ui/src/components/graph/buildForceBrainModel.test.ts` — prompt node tests (WRONG PATH)
- `apps/ui/src/components/graph/forceBrainTypes.ts` — `BrainNodeKind` extended with "prompt" (WRONG PATH)
- `apps/ui/src/components/detail/DetailPopover.tsx` — PromptTracePanel integration
- `apps/ui/src/components/prompt/PromptTracePanel.tsx` — new component
- `apps/ui/src/components/prompt/PromptTracePanel.module.css` — new CSS
- `apps/ui/src/components/shell/RemedyShell.tsx` — prompt node selection resolution
- `apps/ui/src/components/panels/ActivityFeedCard.tsx` — token estimate chips
- `apps/ui/src/components/panels/RightLivePanel.module.css` — `.activityTag` style
- `tests/ui_server/test_prompt_trace_payload.py` — backend payload tests (good)
- `tests/ui_server/test_prompt_trace_lens.py` — dashboard integration tests (BROKEN SYNTAX)
- `apps/ui/src/components/prompt/promptTraceLens.test.ts` — frontend tests (reference wrong graph path)

## Task 1: Fix backend path sanitization

Current `_redact_preview()` in `packages/orchestration/ui_server.py` only strips `/tmp/remedy-pingpong-*` staging paths. Broaden it.

The function must strip or replace with semantic placeholders:
- `/tmp/...` anything → `[staging]`
- `/home/...` → `[local]`
- `/Users/...` → `[local]`
- `/private/...` → `[local]`
- `/mnt/...` → `[local]`
- `.data/job_workspaces/...` → `[workspace]`
- `remedy-pingpong-*` paths → `[staging]`

Also ensure `_safe_rel_file()` strips absolute prefixes from `changedFilesSafe` and `safeDiffFiles` — it currently takes the basename after `/`, which is too aggressive (loses directory structure). Instead strip only the absolute prefix (everything before the repo-relative part). A safe approach: if path starts with `/`, find the last occurrence of a known repo-root marker or just strip the leading absolute portion up to and including common prefixes.

Current `_safe_rel_file`:
```python
def _safe_rel_file(name: str) -> str:
    s = str(name).strip()
    if not s:
        return ""
    if s.startswith("/"):
        s = s.rsplit("/", 1)[-1]
    return s[:120]
```

This loses directory structure (`/abs/path/packages/foo/bar.py` → `bar.py`). Fix to preserve relative structure when possible:
```python
def _safe_rel_file(name: str) -> str:
    s = str(name).strip()
    if not s:
        return ""
    if s.startswith("/"):
        # Strip absolute prefix, keep repo-relative tail
        for marker in ("packages/", "apps/", "tests/", "scripts/", "docs/", ".agent/"):
            idx = s.find(marker)
            if idx >= 0:
                s = s[idx:]
                break
        else:
            s = s.rsplit("/", 1)[-1]
    return s[:120]
```

Also apply the same broad path regex to the full dashboard JSON serialization in `_build_prompt_trace_section()` — scan each item's string fields for absolute paths.

Acceptance:
- `_redact_preview()` strips all listed absolute path prefixes
- `_safe_rel_file()` preserves repo-relative directory structure
- No `/tmp/`, `/home/`, `/Users/`, `/mnt/`, `/private/`, `.data/job_workspaces/` appear in dashboard prompt trace JSON
- Existing tests still pass after changes

## Task 2: Fix prompt nodes in visible graph path

The visible production graph is:
- `apps/ui/src/components/graph/BrainGraphStage.tsx` renders `<BrainGraphCanvas />`
- `apps/ui/src/components/graph/BrainGraphCanvas.tsx` is the actual visible SVG graph

The previous run added prompt nodes to `ForceBrainGraph.tsx` and `buildForceBrainModel.ts`. Those files exist but are NOT rendered. Prompt nodes must be in `BrainGraphCanvas.tsx`.

`BrainGraphCanvas.tsx` has a simple model:
```ts
interface DisplayNode {
  id: string;
  label: string;
  state: string;
  kind: "root" | "task";
  x: number;
  y: number;
  size: number;
}
```

And `buildDisplayModel()` builds nodes from `dashboard.tasks`.

Required changes to `BrainGraphCanvas.tsx`:

1. Extend `DisplayNode` kind to include `"prompt"`:
   ```ts
   kind: "root" | "task" | "prompt";
   ```
   Add optional fields for prompt-specific data:
   ```ts
   color?: string;
   promptRole?: string;
   promptKind?: string;
   doubleRing?: boolean;
   nodeId?: string;
   ```

2. In `buildDisplayModel()`, after creating task nodes, iterate over `dashboard.promptTrace?.items` and create prompt nodes:
   - Small radius (6 vs task's 14)
   - Position near parent task node (small angular offset)
   - Role-colored: builder=#4c83ff, reviewer=#a78bfa, repair=#f59e0b
   - Edge from task to prompt node
   - Carry `nodeId` = prompt item id for click handling

3. In the SVG render, add a prompt node case:
   - Small colored circle
   - Re-review gets double-ring (subtle outer stroke)
   - Clickable (onClick calls onSelectNode with the prompt's nodeId)
   - No label displayed (too small)

4. Update filter logic: prompt nodes should be visible when their parent task is visible. Do not count prompt nodes when filtering tasks.

5. Update `RemedyShell.tsx` prompt selection resolution to work with `BrainGraphCanvas` node IDs (prompt nodes use their prompt item id as the node id).

Do NOT remove the ForceBrainGraph prompt code — it is not harmful and may be the intended future graph. Just ensure the VISIBLE graph works.

Acceptance:
- Prompt nodes render in `BrainGraphCanvas.tsx` (the visible graph)
- Builder = blue, Reviewer = purple, Repair = amber
- Re-review has visual distinction (double-ring or similar)
- Prompt nodes are clickable → opens DetailPopover for owning task with prompt highlighted
- Decorative/root nodes remain non-clickable for prompts
- Prompt nodes do not inflate task count
- Prompt nodes position near their parent task

## Task 3: Fix workspace.diff truncation

File: `packages/orchestration/job_evidence.py`

Current code (around line 438-442):
```python
for line in unified[:200]:
    diff_lines.append(line.rstrip())
if len(unified) > 200:
    diff_lines.append(f"# ... {len(unified) - 200} more lines truncated")
```

This caps each file's diff at 200 lines, which is too aggressive for review packs.

Fix: raise the per-file cap to at least 2000 lines (or remove the cap entirely since the overall `_SAFE_DIFF_CAP` in `pingpong_loop.py` already limits the safe.diff). The workspace.diff should be the full untruncated diff of all applied files.

If removing the cap entirely, add a total cap at 500,000 chars to prevent pathological cases.

Acceptance:
- `workspace.diff` contains no `# ... N more lines truncated` markers for normal-sized files
- A file with 1000+ lines of diff is included in full
- Pathological edge case (million-line diff) is still capped at a reasonable total size
- `workspace.diff` produces valid unified diff format that can be applied with `patch -p1`

## Task 4: Fix broken test + comprehensive tests

### Fix broken syntax

File: `tests/ui_server/test_prompt_trace_lens.py` around line 100

The safe.diff redactor stripped a test string, producing invalid Python:
```python
secret=[REDACTED] SECRET SYSTEM PROMPT do-not-leak"
```

This should be a valid Python string assignment like:
```python
secret = "FAKE_SYSTEM_PROMPT_do_not_leak"
```

Fix this so the test proves no raw prompt field leaks into dashboard JSON, using a test string that won't be caught by the safe.diff redactor.

### Required tests (Python backend)

File: `tests/ui_server/test_prompt_trace_payload.py` (existing, carry forward)
File: `tests/ui_server/test_prompt_trace_lens.py` (fix syntax, carry forward, extend)

Tests must cover:
- Dashboard includes prompt trace items from `prompt_trace.jsonl`
- Redacted preview truncated at 1200 chars
- No raw unredacted prompt field in dashboard JSON
- `/home/...`, `/tmp/...`, `/Users/...`, `/mnt/...`, `.data/job_workspaces/...` stripped from preview
- `/home/...`, `/tmp/...` stripped from `changedFilesSafe`
- Missing prompt trace → explicit "absent" state with reason
- Prompt items do not inflate task count
- Evidence refs are relative paths

### Required tests (Frontend)

File: `apps/ui/src/components/prompt/promptTraceLens.test.ts` (carry forward, update)

Update to reference `BrainGraphCanvas` path if the test imports `buildForceBrainModel`. If the tests use `normalizeDashboardPayload` directly, they may not need changes. Verify and fix as needed.

Tests must cover:
- Prompt trace normalization maps payload correctly
- Unknown role/kind normalized to safe defaults
- Absent state explicit when no prompt_trace
- Prompt nodes do not count as task nodes (in visible graph)
- Selecting a task shows its prompts
- Empty prompt set for task without trace

### Required tests (Graph path)

Add at least one test proving prompt nodes appear in the `BrainGraphCanvas` display model (the `buildDisplayModel` function in `BrainGraphCanvas.tsx`). If `buildDisplayModel` is not exported, either export it for testing or test via component rendering.

Acceptance:
- All Python tests pass: `python3 -m pytest tests/ui_server/test_prompt_trace_lens.py tests/ui_server/test_prompt_trace_payload.py -q`
- No syntax errors in any test file
- At least 15 total tests across Python and frontend
- Tests cover path sanitization breadth
- Tests cover visible graph path (BrainGraphCanvas)

## Task 5: Test execution + verification pack

After implementing Tasks 1-4, create a verification artifact.

Run these commands and capture results:

```bash
python3 -m pytest tests/ui_server/test_prompt_trace_lens.py tests/ui_server/test_prompt_trace_payload.py -q
```

If UI dependencies are available:
```bash
cd apps/ui && npm run test:unit -- --run
cd apps/ui && npm run typecheck
```

Record results in the task evidence. If UI dependencies are unavailable, state that explicitly.

Also verify:
- `workspace.diff` has no `# ... more lines truncated` markers
- Dashboard JSON from `_build_job_plan_dashboard()` has no absolute paths matching `/tmp/`, `/home/`, `/Users/`, `/mnt/`, `/private/`, `.data/job_workspaces/`
- No `prompt_text_redacted` or `prompt_text` key in serialized dashboard

Acceptance:
- Python tests ran and all passed
- UI test results reported (ran or explicitly stated as unavailable)
- Verification checks documented in evidence
- No fabricated test results
