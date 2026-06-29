import type { RemedyPromptTraceItem } from "../../api/types";
import styles from "./PromptTracePanel.module.css";

function roleLabel(item: RemedyPromptTraceItem): string {
  if (item.promptKind === "repair") return "Repair";
  if (item.promptKind === "re-review") return "Re-review";
  if (item.role === "reviewer") return "Reviewer";
  if (item.role === "system") return "System";
  return "Builder";
}

// Maps a prompt item to a CSS accent class. Repair/re-review prompts get the
// repair accent regardless of role; otherwise the accent follows the role.
function accentClass(item: RemedyPromptTraceItem): string {
  if (item.promptKind === "repair" || item.promptKind === "re-review") return styles.repair;
  if (item.role === "reviewer") return styles.reviewer;
  if (item.role === "system") return styles.system;
  return styles.builder;
}

// Short, human-scannable form of the prompt hash (never the full digest).
function shortHash(sha: string): string {
  return sha ? sha.slice(0, 10) : "no hash";
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
        <span className={styles.count}>
          {prompts.length} prompt{prompts.length === 1 ? "" : "s"}
        </span>
      </div>

      <div className={styles.list}>
        {prompts.map((item) => (
          <article
            key={item.id}
            data-prompt-id={item.id}
            className={[
              styles.promptCard,
              accentClass(item),
              selected?.id === item.id ? styles.selected : "",
            ].filter(Boolean).join(" ")}
          >
            <div className={styles.cardTop}>
              <strong className={styles.role}>
                {roleLabel(item)} · round {item.round}
              </strong>
              <span className={styles.tokens}>
                {item.promptTokensEstimated.toLocaleString()} est. tokens
              </span>
            </div>

            <div className={styles.cardMeta}>
              <span>{item.provider || "unknown provider"}</span>
              <span className={styles.hash} title={item.promptSha256 || undefined}>
                {shortHash(item.promptSha256)}
              </span>
              {item.changedFilesSafe.length > 0 && (
                <span>
                  {item.changedFilesSafe.length} file
                  {item.changedFilesSafe.length === 1 ? "" : "s"}
                </span>
              )}
              {item.evidenceRef && (
                <span className={styles.evidence}>{item.evidenceRef}</span>
              )}
            </div>

            {item.redactedPreview && (
              <details className={styles.preview}>
                <summary>Redacted preview</summary>
                <pre className={styles.previewBody}>
                  {item.redactedPreview}
                  {item.redactedPreviewTruncated ? "\n…" : ""}
                </pre>
              </details>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}
