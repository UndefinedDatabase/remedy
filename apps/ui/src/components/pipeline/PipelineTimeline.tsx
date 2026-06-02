import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ErrorIcon from "@mui/icons-material/Error";
import HourglassEmptyIcon from "@mui/icons-material/HourglassEmpty";
import RadioButtonUncheckedIcon from "@mui/icons-material/RadioButtonUnchecked";
import RemoveCircleOutlineIcon from "@mui/icons-material/RemoveCircleOutline";
import type { PipelineStep, PipelineStepState } from "../../api/types";
import styles from "./Pipeline.module.css";

const STEP_ICON: Record<PipelineStepState, typeof CheckCircleIcon> = {
  done: CheckCircleIcon,
  current: HourglassEmptyIcon,
  blocked: ErrorIcon,
  failed: ErrorIcon,
  skipped: RemoveCircleOutlineIcon,
  unknown: RadioButtonUncheckedIcon,
  waiting: RadioButtonUncheckedIcon,
};

export function PipelineTimeline({ steps }: { steps: PipelineStep[] }) {
  if (!steps || steps.length === 0) {
    return <div className={styles.empty} data-testid="pipeline-empty">No pipeline run yet</div>;
  }
  return (
    <ol className={styles.timeline} data-testid="pipeline-timeline">
      {steps.map((step) => {
        const Icon = STEP_ICON[step.state] || RadioButtonUncheckedIcon;
        return (
          <li key={step.id} className={`${styles.step} ${styles[step.state] || ""}`} data-state={step.state}>
            <span className={styles.stepIcon}><Icon style={{ fontSize: 14 }} /></span>
            <span className={styles.stepLabel}>{step.label}</span>
            {step.detail && <span className={styles.stepDetail}>{step.detail}</span>}
          </li>
        );
      })}
    </ol>
  );
}
