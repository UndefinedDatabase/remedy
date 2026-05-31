const conceptLabels: Record<string, string> = {
  patch_intent: "Proposed change", patch_apply: "Applied change", patch_apply_proof: "Apply proof",
  test_run: "Test result", review_recommendation: "Review suggestion", memory_candidate: "Learning suggestion",
  decision_queue: "Needs decision", approval_decision: "Approval", artifact: "Generated work",
  task: "Task", job: "Project goal", proof: "Proof", change: "Changed file"
};
const diagnosticsOnly: Record<string, string> = { context_coverage: "Context check", token_policy: "Token budget", worker_adapter: "Worker", run_event: "Run event", event_ledger: "Event ledger" };
const forbidden = ["rank", "importance", "node_type", "metadata", "present signals", "missing signals", "context coverage", "zone", "edge_type", "connected_to", "raw_stdout", "raw_stderr", "command_output", "diff_preview", "approval_reason", "traceback"];

export function humanLabel(type: string, fallback = "Work item"): string {
  const normalized = String(type || "").toLowerCase();
  return conceptLabels[normalized] ?? diagnosticsOnly[normalized] ?? fallback;
}
export function isDiagnosticsOnly(type: string): boolean {
  return Object.prototype.hasOwnProperty.call(diagnosticsOnly, String(type || "").toLowerCase());
}
export function scrubUiText(value: unknown, fallback = "Work item"): string {
  const input = String(value ?? "").replace(/\s+/g, " ").trim();
  if (!input) return fallback;
  const lower = input.toLowerCase();
  if (forbidden.some((word) => lower.includes(word))) return fallback;
  if (/^[0-9a-f]{6,}(-[0-9a-f]+)*$/i.test(input)) return fallback;
  return input.length > 92 ? `${input.slice(0, 89)}…` : input;
}
export function stateLabel(state: string): string {
  if (state === "done") return "Done";
  if (state === "current") return "In Progress";
  if (state === "blocked") return "Blocked";
  if (state === "suggested") return "Suggested";
  return "Planned";
}
