import styles from "./GraphFilterChips.module.css";

const filters = [["all", "All"], ["open", "Needs work"], ["planned", "Planned"], ["done", "Done"]] as const;
export type GraphFilter = (typeof filters)[number][0];

const dotClass: Record<string, string> = {
  open: styles.dotOpen,
  planned: styles.dotPlanned,
  done: styles.dotDone,
};

export function GraphFilterChips({ value, onChange }: { value: GraphFilter; onChange: (value: GraphFilter) => void }) {
  return (
    <div className={styles.chips} role="group" aria-label="Graph filters">
      {filters.map(([key, label]) => (
        <button
          key={key}
          type="button"
          className={value === key ? `${styles.chip} ${styles.chipActive}` : styles.chip}
          aria-pressed={value === key}
          onClick={() => onChange(key)}
        >
          {key !== "all" && <span className={`${styles.dot} ${dotClass[key]}`} aria-hidden="true" />}
          {label}
        </button>
      ))}
    </div>
  );
}
