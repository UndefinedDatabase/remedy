import type { RemedyPipeline, RemedyResume } from "../../api/types";
import { ContextCard } from "./ContextCard";
import { PipelineTimeline } from "./PipelineTimeline";
import { StopReasonCard } from "./StopReasonCard";
import styles from "./Pipeline.module.css";

function ResumeCard({ resume }: { resume: RemedyResume }) {
  if (!resume.replay_available && !resume.can_resume) return null;

  return (
    <div className={styles.resumeCard} data-testid="resume-card">
      {resume.can_resume && resume.latest_checkpoint ? (
        <>
          <strong>Resume available</strong>
          <span className={styles.resumeKind}>{resume.latest_checkpoint.kind.replace(/_/g, " ")}</span>
          {resume.latest_checkpoint.next_command && (
            <code
              className={styles.commandCode}
              onClick={() => navigator.clipboard?.writeText(resume.latest_checkpoint!.next_command)}
              title="Click to copy"
            >
              {resume.latest_checkpoint.next_command}
            </code>
          )}
        </>
      ) : resume.blocked_reason ? (
        <>
          <strong>Resume blocked</strong>
          <span className={styles.resumeBlocked}>{resume.blocked_reason.replace(/_/g, " ")}</span>
        </>
      ) : null}
    </div>
  );
}

export function PipelinePanel({ pipeline, resume }: { pipeline: RemedyPipeline | null; resume?: RemedyResume | null }) {
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
      {resume && <ResumeCard resume={resume} />}
    </section>
  );
}
