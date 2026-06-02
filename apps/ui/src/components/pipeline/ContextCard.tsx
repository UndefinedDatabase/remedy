import type { RemedyPipeline } from "../../api/types";
import styles from "./Pipeline.module.css";

export function ContextCard({ pipeline }: { pipeline: RemedyPipeline }) {
  const ctx = pipeline.source_context;
  const mem = pipeline.memory;
  const hasContext = ctx.injected;
  const hasMemory = mem.used;

  if (!hasContext && !hasMemory) {
    return <div className={styles.contextEmpty} data-testid="context-empty">No context or memory injected</div>;
  }

  return (
    <section className={styles.contextCard} data-testid="context-card">
      {hasContext && (
        <div className={styles.contextRow}>
          <strong>Source context</strong>
          <span>{ctx.file_count ?? 0} files, {ctx.test_file_count ?? 0} test files</span>
          <span>~{ctx.estimated_tokens ?? 0} tokens{ctx.truncated ? " (truncated)" : ""}</span>
        </div>
      )}
      {hasMemory && (
        <div className={styles.contextRow}>
          <strong>Memory</strong>
          <span>{mem.item_count} items{mem.truncated ? " (truncated)" : ""}</span>
        </div>
      )}
    </section>
  );
}
