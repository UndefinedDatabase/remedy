# Steps 5391-5420: Prompt Trace Lens UI v1

## Product goal

Remedy should make prompt lineage visible in the UI.

The operator should be able to see:

* which Builder prompts were sent
* which Reviewer prompts were sent
* which Repair prompts were sent
* which task each prompt belongs to
* prompt round
* provider/provider kind
* estimated prompt tokens
* prompt hash
* changed files
* findings opened/rechecked
* safe redacted prompt preview
* evidence refs

This must be visible without exposing raw secrets, raw diffs, raw stdout/stderr, or unredacted prompts.

## Current UI review

Current UI already has:

* `apps/ui/src/components/shell/RemedyShell.tsx`
* `BrainGraphStage`
* `ForceBrainGraph`
* `DetailPopover`
* `RightLivePanel`
* `ActivityFeedCard`
* `PhaseTimeline`
* backend dashboard builder in `packages/orchestration/ui_server.py`
* frontend normalization in `apps/ui/src/api/remedyApi.ts`
* typed dashboard model in `apps/ui/src/api/types.ts`

Current gap:
Prompt trace exists in Evidence, but the UI hides it. The graph mostly shows tasks/events, not prompt-lineage nodes.

## Task 1: Safe prompt trace backend payload

Extend the dashboard payload for JobPlan/job-flow jobs with a safe prompt trace section.

Add frontend/backend types roughly equivalent to:

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
  source: "prompt_trace_jsonl" | "observability_index" | "absent";
  missingReason?: string;
}
```

Backend requirements:

* Read task-level `prompt_trace.jsonl` from the resolved evidence dir.
* Do not leak absolute paths.
* Do not include raw unredacted prompts.
* Use `prompt_text_redacted` only as `redactedPreview`.
* Limit `redactedPreview` to max 1200 chars.
* Set `redactedPreviewTruncated=true` if longer.
* Include evidence refs like `task_runs/T001/prompt_trace.jsonl`.
* Missing prompt trace must be explicit, not fake empty success.
* Add `prompt_trace` or `promptTrace` to the dashboard payload.

Acceptance:
- Dashboard payload includes prompt trace items from prompt_trace.jsonl
- No raw unredacted prompt field in dashboard JSON
- redactedPreview is truncated at 1200 chars
- Missing prompt trace is explicit ("absent" with reason)
- Evidence refs are relative paths only
- No absolute local paths in payload

## Task 2: Prompt nodes in center brain graph

Extend frontend graph data so prompt trace items become real nodes in the middle graph.

Visual mapping:

* Builder prompt = small blue code circle
* Reviewer prompt = small purple person/review circle
* Repair prompt = small amber/orange wrench/retry circle
* Re-review = purple with subtle double-ring
* Prompt nodes connect to their task node
* Prompt nodes are smaller than task nodes
* Prompt nodes are clickable
* Decorative dots remain non-clickable

Do not replace the entire graph renderer. Add the smallest safe extension.

Recommended type change:

* Extend `RemedyTaskKind` with `"prompt"` or add prompt-specific graph node kind safely.
* Add prompt metadata to graph node or keep it in dashboard.promptTrace and map by node ID.

Suggested node IDs:

* `prompt:${taskId}:${role}:${round}:${promptKind}`

Suggested labels:

* `Builder r1`
* `Reviewer r1`
* `Repair r2`
* `Re-review r2`

Acceptance:
- Prompt nodes appear in graph data
- Prompt nodes are smaller than task nodes
- Prompt nodes connect to their parent task node
- Prompt nodes are clickable
- Decorative dots remain non-clickable
- Prompt nodes do not inflate task count

## Task 3: Prompt Trace Panel in DetailPopover

When a task node or prompt node is selected, the detail popover should show a compact Prompt Trace section.

Add a component:

`apps/ui/src/components/prompt/PromptTracePanel.tsx`

and CSS:

`apps/ui/src/components/prompt/PromptTracePanel.module.css`

Use this starter component shape and adapt it to current types:

```tsx
import type { RemedyPromptTraceItem } from "../../api/types";
import styles from "./PromptTracePanel.module.css";

function roleLabel(item: RemedyPromptTraceItem): string {
  if (item.promptKind === "repair") return "Repair";
  if (item.promptKind === "re-review") return "Re-review";
  return item.role === "reviewer" ? "Reviewer" : "Builder";
}

export function PromptTracePanel({
  prompts,
  selectedPromptId,
}: {
  prompts: RemedyPromptTraceItem[];
  selectedPromptId?: string | null;
}) {
  if (!prompts.length) {
    return (
      <section className={styles.panel} data-ui="prompt-trace-panel">
        <h3>Prompt trace</h3>
        <p className={styles.empty}>No prompt trace evidence for this item.</p>
      </section>
    );
  }

  const selected = selectedPromptId
    ? prompts.find((item) => item.id === selectedPromptId)
    : null;

  return (
    <section className={styles.panel} data-ui="prompt-trace-panel">
      <div className={styles.header}>
        <h3>Prompt trace</h3>
        <span>{prompts.length} prompt{prompts.length === 1 ? "" : "s"}</span>
      </div>

      <div className={styles.list}>
        {prompts.map((item) => (
          <article
            key={item.id}
            className={[
              styles.promptCard,
              styles[item.role],
              item.promptKind === "repair" ? styles.repair : "",
              selected?.id === item.id ? styles.selected : "",
            ].filter(Boolean).join(" ")}
          >
            <div className={styles.cardTop}>
              <strong>{roleLabel(item)} · round {item.round}</strong>
              <span>{item.promptTokensEstimated.toLocaleString()} est. tokens</span>
            </div>

            <div className={styles.meta}>
              <span>{item.provider}</span>
              <span>{item.promptKind}</span>
              <span title={item.promptSha256}>hash {item.promptSha256.slice(0, 8)}</span>
            </div>

            {item.changedFilesSafe.length > 0 && (
              <p className={styles.files}>
                {item.changedFilesSafe.slice(0, 3).join(", ")}
                {item.changedFilesSafe.length > 3 ? ` +${item.changedFilesSafe.length - 3}` : ""}
              </p>
            )}

            {item.redactedPreview && (
              <details className={styles.preview}>
                <summary>Redacted prompt preview</summary>
                <pre>{item.redactedPreview}{item.redactedPreviewTruncated ? "\n[…truncated]" : ""}</pre>
              </details>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}
```

Use this CSS direction:

```css
.panel {
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid var(--remedy-line);
}

.header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 10px;
}

.header h3 {
  margin: 0;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: .06em;
  color: var(--remedy-muted);
}

.header span {
  font-size: 11px;
  color: var(--remedy-faint);
}

.empty {
  margin: 6px 0 0;
  font-size: 12px;
  color: var(--remedy-faint);
}

.list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
  max-height: 270px;
  overflow: auto;
  padding-right: 2px;
}

.promptCard {
  border: 1px solid rgba(76, 131, 255, .14);
  border-radius: 14px;
  padding: 9px 10px;
  background: rgba(255,255,255,.58);
  box-shadow: 0 6px 16px rgba(55,86,138,.07);
}

.promptCard.builder {
  border-color: rgba(76, 131, 255, .22);
}

.promptCard.reviewer {
  border-color: rgba(167, 139, 250, .24);
}

.promptCard.repair {
  border-color: rgba(245, 163, 78, .28);
}

.promptCard.selected {
  box-shadow: 0 0 0 3px rgba(76, 131, 255, .12);
}

.cardTop {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.cardTop strong {
  font-size: 12px;
  color: var(--remedy-ink-strong);
}

.cardTop span {
  font-size: 11px;
  color: var(--remedy-muted);
  white-space: nowrap;
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 5px;
}

.meta span {
  font-size: 10px;
  color: var(--remedy-muted);
  background: rgba(238, 244, 255, .78);
  border: 1px solid rgba(76, 131, 255, .12);
  border-radius: 999px;
  padding: 2px 6px;
}

.files {
  margin: 6px 0 0;
  font-size: 11px;
  color: var(--remedy-ink-soft, #6f82a8);
}

.preview {
  margin-top: 7px;
}

.preview summary {
  cursor: pointer;
  font-size: 11px;
  color: var(--remedy-blue-700);
}

.preview pre {
  max-height: 150px;
  overflow: auto;
  margin: 6px 0 0;
  padding: 8px;
  border-radius: 10px;
  background: rgba(244, 248, 255, .82);
  color: var(--remedy-ink);
  font-family: var(--remedy-font-mono);
  font-size: 10px;
  line-height: 1.45;
  white-space: pre-wrap;
}
```

Integration:

* Import `PromptTracePanel` into `DetailPopover.tsx`.
* If selected node is a task, show prompts for that task.
* If selected node is a prompt, show only that prompt plus its sibling prompts for the same task.
* Never show prompt previews outside this detail panel.

Acceptance:
- PromptTracePanel component exists
- CSS matches premium quiet visual direction
- Shows builder/reviewer/repair prompts with round info
- Redacted preview is collapsed by default
- No raw unredacted prompts visible outside detail panel
- Integrates into DetailPopover

## Task 4: Prompt activity improvements

Right panel activity should show better labels for prompt events:

* `Builder prompt created`
* `Reviewer prompt created`
* `Repair prompt created`
* `Reviewer re-check`
* include task ID and token estimate when available

Do not make the right panel bigger. Keep it compact.

Acceptance:
- Activity feed shows improved prompt event labels
- Token estimate visible when available
- Panel stays compact

## Task 5: Tests

Add focused tests for:

* backend dashboard includes prompt trace items from `prompt_trace.jsonl`
* redacted prompt preview is truncated and safe
* frontend normalization maps prompt trace payload
* graph model creates clickable prompt nodes, while decorative nodes remain non-clickable
* selecting a task shows prompt trace panel
* no raw unredacted prompt field appears in dashboard JSON
* prompt nodes do not count as fake task count
* prompt trace missing state is explicit

Acceptance:
- At least 8 focused tests
- All pass
- Tests cover backend payload safety
- Tests cover frontend graph model
- Tests cover redacted preview truncation
