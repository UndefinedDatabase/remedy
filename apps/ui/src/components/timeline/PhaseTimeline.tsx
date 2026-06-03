import AssignmentTurnedInOutlinedIcon from "@mui/icons-material/AssignmentTurnedInOutlined";
import CalendarMonthOutlinedIcon from "@mui/icons-material/CalendarMonthOutlined";
import CodeIcon from "@mui/icons-material/Code";
import FactCheckOutlinedIcon from "@mui/icons-material/FactCheckOutlined";
import FlagOutlinedIcon from "@mui/icons-material/FlagOutlined";
import RateReviewOutlinedIcon from "@mui/icons-material/RateReviewOutlined";
import type { RemedyPhase } from "../../api/types";
import styles from "./PhaseTimeline.module.css";

const icons = { job: AssignmentTurnedInOutlinedIcon, planning: CalendarMonthOutlinedIcon, build: CodeIcon, test: FactCheckOutlinedIcon, review: RateReviewOutlinedIcon, finalized: FlagOutlinedIcon };

export function PhaseTimeline({ phases }: { phases: RemedyPhase[] }) {
  return (
    <section className={styles.timeline} aria-label="Project timeline" data-ui="phase-timeline">
      <div className={styles.mainLine} />
      <div className={styles.phaseRow}>
        {phases.map(phase => {
          const Icon = icons[phase.id];
          return (
            <article key={phase.id} className={`${styles.phase} ${styles[phase.state]}`}>
              <div className={styles.phaseIcon}><Icon /></div>
              <span>{phase.label}</span>
            </article>
          );
        })}
      </div>
    </section>
  );
}
