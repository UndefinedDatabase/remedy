import styles from "./GraphFilterChips.module.css";

const filters = [["all", "All"], ["open", "Needs work"], ["planned", "Planned"], ["done", "Done"]] as const;
export type GraphFilter = (typeof filters)[number][0];

export function GraphFilterChips({ value, onChange }: { value: GraphFilter; onChange: (value: GraphFilter) => void }) {
  return (
    <div className={styles.chips} aria-label="Graph filters">
      {filters.map(([key, label]) => (
        <button key={key} type="button" className={value === key ? styles.active : styles.chip} onClick={() => onChange(key)}>
          {key !== "all" && <span className={styles[key]} />}
          {label}
        </button>
      ))}
    </div>
  );
}
