// DECISION F042 D3 — the switcher lives in the brand rail's kicker: a native select, reached
// and driven by the keyboard with nothing added, shown only with more than one project to
// choose between; with one project or none it keeps the kicker the rail already draws.
import type { ChangeEvent } from "react";
import { switcherVisible } from "../../api/projectScope";
import { useProjectContext } from "./ProjectProvider";
import styles from "./ProjectSwitcher.module.css";

export const PROJECT_SWITCHER_LABEL = "Project";
export const MISSING_FOLDER_MARK = " (folder missing)";
export const NO_ACTIVE_PROJECT_OPTION = "Choose a project";

export function ProjectSwitcher({ fallback }: { fallback: React.ReactNode }) {
  const { view, active, switchTo } = useProjectContext();

  if (view === null || !switcherVisible(view)) {
    if (active === null) return <>{fallback}</>;
    return <div className={styles.kicker} data-ui="project-kicker">{active.name || active.slug}</div>;
  }

  function onChange(event: ChangeEvent<HTMLSelectElement>): void {
    const slug = event.target.value;
    if (slug !== "" && slug !== active?.slug) switchTo(slug);
  }

  return (
    <label className={styles.switcher} data-ui="project-switcher">
      <span className={styles.kicker}>{PROJECT_SWITCHER_LABEL}</span>
      <select
        className={styles.select}
        aria-label={PROJECT_SWITCHER_LABEL}
        value={active?.slug ?? ""}
        onChange={onChange}
      >
        {active === null && <option value="" disabled>{NO_ACTIVE_PROJECT_OPTION}</option>}
        {view.projects.map((p) => (
          <option key={p.slug} value={p.slug}>{p.slug}{p.repo_reachable ? "" : MISSING_FOLDER_MARK}</option>
        ))}
      </select>
    </label>
  );
}
