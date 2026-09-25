// The breadcrumb chip graph_spec.md §10 puts top-left of the stage: Job, then
// the focused task, then the focused run. Each crumb shallower than the
// current level is a button that walks back to it; the current one is text.
// Hidden at L0, where the trail would be "Job" alone (DECISION F023 D2).
import type { ZoomLevel } from "./semanticZoom";
import styles from "./ZoomBreadcrumbs.module.css";

export interface ZoomBreadcrumbItem {
  level: ZoomLevel;
  label: string;
  current: boolean;
}

export function ZoomBreadcrumbs({ items, onJump }: {
  items: readonly ZoomBreadcrumbItem[];
  onJump: (level: ZoomLevel) => void;
}) {
  if (items.length <= 1) return null;
  return (
    <nav className={styles.chip} aria-label="Zoom level" data-ui="zoom-breadcrumbs">
      <ol className={styles.trail}>
        {items.map((item, index) => (
          <li key={item.level} className={styles.crumb}>
            {index > 0 && <span className={styles.separator} aria-hidden="true">›</span>}
            {item.current ? (
              <span className={styles.current} aria-current="location">{item.label}</span>
            ) : (
              <button type="button" className={styles.jump} onClick={() => onJump(item.level)}>
                {item.label}
              </button>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}
