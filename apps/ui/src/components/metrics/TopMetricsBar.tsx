import { useState } from "react";
import type { RemedyMetric } from "../../api/types";
import {
  ClipboardGlyph, CalendarGlyph, TaskDoneGlyph, ChartGlyph, TokenGlyph,
  FlaskGlyph, ShieldCheckGlyph,
} from "../icons/RemedyGlyphs";
import styles from "./TopMetricsBar.module.css";

const iconByKey: Record<string, typeof ClipboardGlyph> = {
  open: ClipboardGlyph,
  planned: CalendarGlyph,
  done: TaskDoneGlyph,
  progress: ChartGlyph,
  tests: FlaskGlyph,
  proof: ShieldCheckGlyph,
  tokens: TokenGlyph,
};

const stateDotClass: Record<string, string> = {
  pass: styles.statePass,
  fail: styles.stateFail,
  none: styles.stateNone,
};

const EM_DASH = "—";

function formatTokens(value: number): string {
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M`;
  if (value >= 1_000) return `${(value / 1_000).toFixed(1)}k`;
  return String(value);
}

/** Main value text (without suffix). Unknown / em-dash safe. */
function mainValue(m: RemedyMetric): string {
  if (m.unknown || m.value === EM_DASH) return EM_DASH;
  if (m.key === "tokens") {
    return typeof m.value === "number" && m.value > 0 ? formatTokens(m.value) : EM_DASH;
  }
  return String(m.value);
}

export function TopMetricsBar({ metrics }: { metrics: RemedyMetric[] }) {
  const [tooltipKey, setTooltipKey] = useState<string | null>(null);

  return (
    <section className={`${styles.bar} remedy-glass-card`} aria-label="Project metrics" data-ui="top-metrics-bar">
      {metrics.map(m => {
        const Icon = iconByKey[m.key] || ChartGlyph;
        const isTokens = m.key === "tokens";
        const main = mainValue(m);
        const showSuffix = main !== EM_DASH && m.key !== "progress" && Boolean(m.suffix);
        const ariaValue = `${main}${showSuffix ? m.suffix : ""}`;
        const progressWidth = typeof m.value === "number" ? Math.max(0, Math.min(m.value, 100)) : 0;

        return (
          <article
            key={m.key}
            className={styles.metric}
            tabIndex={m.tooltip ? 0 : undefined}
            onMouseEnter={() => m.tooltip && setTooltipKey(m.key)}
            onMouseLeave={() => setTooltipKey(null)}
            onFocus={() => m.tooltip && setTooltipKey(m.key)}
            onBlur={() => setTooltipKey(null)}
            aria-label={`${m.label}: ${ariaValue}`}
          >
            <div className={styles.iconBox}><Icon style={{ width: 16, height: 16 }} /></div>
            <div className={styles.metricBody}>
              <div className={styles.label}>
                {m.key === "tests" && (
                  <span className={`${styles.stateDot} ${stateDotClass[m.state || "none"]}`} aria-hidden="true" />
                )}
                {m.label}
              </div>
              <div className={styles.value}>
                {main}
                {showSuffix && <span className={styles.valueSuffix}>{m.suffix}</span>}
              </div>
              {m.key === "progress" && (
                <div className={styles.progressTrack}>
                  <span style={{ width: `${progressWidth}%` }} />
                </div>
              )}
              {isTokens && main !== EM_DASH && <div className={styles.estimated}>estimated</div>}
            </div>
            {tooltipKey === m.key && m.tooltip && (
              <div className={styles.tooltip} role="tooltip" data-testid="token-tooltip">
                {Object.entries(m.tooltip).map(([role, count]) => (
                  <div key={role} className={styles.tooltipRow}>
                    <span>{role}</span>
                    <span>{formatTokens(count)}</span>
                  </div>
                ))}
              </div>
            )}
          </article>
        );
      })}
    </section>
  );
}
