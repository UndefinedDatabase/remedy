import type { RemedyDashboard } from "../../api/types";
import { RemedyLogo } from "./RemedyLogo";
import { SideIconDock } from "./SideIconDock";
import styles from "./LeftBrandRail.module.css";

export function LeftBrandRail({ dashboard }: { dashboard: RemedyDashboard }) {
  return (
    <aside className={styles.rail}>
      <RemedyLogo />
      <section className={styles.intro}>
        <div className={styles.concept}>{dashboard.conceptLabel}</div>
        <h1>{dashboard.title}</h1>
        <p>{dashboard.description}</p>
      </section>
      <SideIconDock />
    </aside>
  );
}
