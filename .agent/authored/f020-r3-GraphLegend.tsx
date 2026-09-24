import { useEffect, useId, useState } from "react";
import { legendKindRows, legendStateRows, tokenVar } from "./renderers/legendModel";
import type { LegendStateRow } from "./renderers/legendModel";
import styles from "./GraphLegend.module.css";

// The graph legend, opened from the graph's chrome. Every row comes from
// renderers/legendModel.ts, which reads the glyph and state modules the canvas
// paints from, so this component writes no kind, no state, no path and no
// colour of its own (T5_F020.md T002; DECISION F020 D3).

const KIND_ROWS = legendKindRows();
const STATE_ROWS = legendStateRows();

/** A state's swatch: a disc in the state's fill and line at its size factor,
 *  with the state's marks drawn on it from the canvas's own paths. */
function StateSwatch({ row }: { row: LegendStateRow }) {
  const r = 10 * row.sizeFactor;
  return (
    <svg className={styles.glyph} viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="12" cy="12" r={r} style={{ fill: tokenVar(row.fillToken), stroke: tokenVar(row.lineToken) }} />
      {row.marks.map((m) => (
        <g key={m.mark}>
          {m.outlineToken && (
            <path d={m.strokePath || m.fillPath} className={styles.outline} style={{ stroke: tokenVar(m.outlineToken) }} />
          )}
          {m.fillPath && <path d={m.fillPath} style={{ fill: tokenVar(m.token) }} />}
          {m.strokePath && <path d={m.strokePath} className={styles.line} style={{ stroke: tokenVar(m.token) }} />}
        </g>
      ))}
    </svg>
  );
}

export function GraphLegend() {
  const [open, setOpen] = useState(false);
  const panelId = useId();

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") setOpen(false); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  return (
    <div className={styles.legend}>
      <button
        type="button"
        className={styles.toggle}
        aria-expanded={open}
        aria-controls={panelId}
        onClick={() => setOpen(!open)}
      >
        Legend
      </button>
      {open && (
        <div id={panelId} className={styles.panel} role="dialog" aria-label="Graph legend">
          <p className={styles.heading}>Kinds</p>
          <ul className={styles.rows}>
            {KIND_ROWS.map((row) => (
              <li key={row.kind} className={styles.row}>
                <svg className={styles.glyph} viewBox="0 0 24 24" aria-hidden="true">
                  {row.fillPath && <path d={row.fillPath} className={styles.kindFill} />}
                  {row.strokePath && <path d={row.strokePath} className={styles.kindLine} />}
                </svg>
                {row.name}
              </li>
            ))}
          </ul>
          <p className={styles.heading}>States</p>
          <ul className={styles.rows}>
            {STATE_ROWS.map((row) => (
              <li key={row.state} className={styles.row}>
                <StateSwatch row={row} />
                {row.name}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
