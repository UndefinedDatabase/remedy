import type { RemedyDashboard } from "../../api/types";
import { RemedyLogo } from "./RemedyLogo";
import { SideIconDock } from "./SideIconDock";
import type { RailActions } from "./railItems";
import { ProjectSwitcher } from "../shell/ProjectSwitcher";
import styles from "./LeftBrandRail.module.css";

/** What the rail says above the job's order when no project is selected. */
export const RAIL_JOB_KICKER = "Job";

// amend1015 P4.2: the rail names THIS job — its project (the switcher) and the order it was
// given (`dashboard.title`, the job's own title) — where it used to carry a design mock's
// hard-coded headline about a different product.
export function LeftBrandRail({ dashboard, actions }: { dashboard: RemedyDashboard; actions?: RailActions }) {
  return (
    <aside className={styles.rail} data-ui="left-brand-rail">
      <div className={styles.logoBlock}><RemedyLogo /></div>
      <div className={styles.copyBlock}>
        <ProjectSwitcher fallback={<div className={styles.concept}>{RAIL_JOB_KICKER}</div>} />
        <h1 data-ui="job-order">{dashboard.title}</h1>
      </div>
      <SideIconDock className={styles.dock} actions={actions} />
    </aside>
  );
}
