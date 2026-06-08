import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import InfoIcon from "@mui/icons-material/Info";
import type { RemedyPipeline } from "../../api/types";
import styles from "./Pipeline.module.css";

const STOP_LABELS: Record<string, { label: string; explanation: string; requiresHuman: boolean }> = {
  approval_required: { label: "Approval required", explanation: "The patch needs human approval before it can be applied.", requiresHuman: true },
  provider_unavailable: { label: "Provider unavailable", explanation: "Ollama is not running or not reachable. Start it or switch to fixture provider.", requiresHuman: true },
  provider_output_prose_only: { label: "Model returned prose", explanation: "The model returned narrative text instead of a structured patch. Try a different model or use fixture.", requiresHuman: true },
  provider_output_malformed: { label: "Malformed output", explanation: "The model output could not be parsed into a valid patch.", requiresHuman: true },
  unsafe_shell_command: { label: "Unsafe shell command", explanation: "The model output contained shell commands, which are not allowed.", requiresHuman: false },
  validation_failed: { label: "Validation failed", explanation: "The patch structure is invalid (bad paths, missing content, etc.).", requiresHuman: false },
  unsafe_path: { label: "Unsafe path", explanation: "The patch contained an absolute path, which is not allowed.", requiresHuman: false },
  path_traversal: { label: "Path traversal", explanation: "The patch contained a path with '..' traversal.", requiresHuman: false },
  source_apply_failed: { label: "Apply failed", explanation: "The patch could not be applied to the repository.", requiresHuman: true },
  test_failed_after_apply: { label: "Tests failed", explanation: "Tests failed after the patch was applied.", requiresHuman: true },
  repair_budget_exhausted: { label: "Repair budget exhausted", explanation: "Maximum repair cycles reached without passing tests.", requiresHuman: true },
  repeated_patch_detected: { label: "Repeated patch", explanation: "The same patch was produced twice. The model may be stuck.", requiresHuman: true },
  no_structured_patch_text: { label: "No patch output", explanation: "The builder produced no structured patch text.", requiresHuman: true },
  test_timeout: { label: "Test timeout", explanation: "Test execution timed out (60s limit).", requiresHuman: true },
};

export function StopReasonCard({ pipeline }: { pipeline: RemedyPipeline }) {
  if (!pipeline.stop_reason) return null;

  const info = STOP_LABELS[pipeline.stop_reason] || {
    label: pipeline.stop_reason_label || pipeline.stop_reason.replace(/_/g, " "),
    explanation: "",
    requiresHuman: false,
  };

  const Icon = info.requiresHuman ? WarningAmberIcon : InfoIcon;

  return (
    <section className={styles.stopCard} data-testid="stop-reason-card">
      <header className={styles.stopHeader}>
        <Icon style={{ fontSize: 16 }} />
        <strong>{info.label}</strong>
        <code className={styles.stopCode}>{pipeline.stop_reason}</code>
      </header>
      {info.explanation && <p className={styles.stopExplanation}>{info.explanation}</p>}
      {pipeline.next_command && (
        <div className={styles.nextCommand} data-testid="next-command">
          <span className={styles.nextLabel}>Next:</span>
          <code
            className={styles.commandCode}
            onClick={() => navigator.clipboard?.writeText(pipeline.next_command)}
            title="Click to copy"
          >
            {pipeline.next_command}
          </code>
        </div>
      )}
    </section>
  );
}
