import type { RemedyDashboard } from "../../api/types";
import { RemedyLogo } from "./RemedyLogo";
import { SideIconDock } from "./SideIconDock";
import styles from "./LeftBrandRail.module.css";

export function LeftBrandRail({ dashboard: _dashboard }: { dashboard: RemedyDashboard }) {
  return (
    <aside className={styles.rail} data-ui="left-brand-rail">
      <RemedyLogo />
      <section className={styles.intro}>
        <div className={styles.concept}>CONCEPT 01 OF 10</div>
        <h1>GROWING BRAIN<br />OVERVIEW</h1>
        <p>An AI agent shipping a CLI tool that scans and summarizes codebases.</p>
      </section>
      <SideIconDock />
    </aside>
  );
}
