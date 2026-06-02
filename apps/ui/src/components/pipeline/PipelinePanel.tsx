import type { RemedyPipeline } from "../../api/types";
import { ContextCard } from "./ContextCard";
import { PipelineTimeline } from "./PipelineTimeline";
import { StopReasonCard } from "./StopReasonCard";
import styles from "./Pipeline.module.css";

export function PipelinePanel({ pipeline }: { pipeline: RemedyPipeline | null }) {
  if (!pipeline) {
    return (
      <section className={styles.panel} data-testid="pipeline-panel">
        <header className={styles.panelHeader}><h2>Pipeline</h2></header>
        <div className={styles.empty}>No pipeline data</div>
      </section>
    );
  }

  return (
    <section className={styles.panel} data-testid="pipeline-panel">
      <header className={styles.panelHeader}><h2>Pipeline</h2></header>
      <PipelineTimeline steps={pipeline.steps} />
      <StopReasonCard pipeline={pipeline} />
      <ContextCard pipeline={pipeline} />
    </section>
  );
}
