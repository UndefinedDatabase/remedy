import { useState } from "react";
import type { RemedyMetric } from "../../api/types";
import { ClipboardGlyph, CalendarGlyph, TaskDoneGlyph, ChartGlyph, TokenGlyph } from "../icons/RemedyGlyphs";
import styles from "./TopMetricsBar.module.css";

const iconByKey: Record<string, typeof ClipboardGlyph> = {
  open: ClipboardGlyph,
  planned: CalendarGlyph,
  done: TaskDoneGlyph,
  progress: ChartGlyph,
  tokens: TokenGlyph,
};

function formatTokens(value: number): string {
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M`;
  if (value >= 1_000) return `${(value / 1_000).toFixed(1)}k`;
  return String(value);
}

export function TopMetricsBar({ metrics }: { metrics: RemedyMetric[] }) {
  const [tooltipKey, setTooltipKey] = useState<string | null>(null);

  return (
    <section className={`${styles.bar} remedy-glass-card`} aria-label="Project metrics" data-ui="top-metrics-bar">
      {metrics.map(m => {
        const Icon = iconByKey[m.key] || ChartGlyph;
        const isTokens = m.key === "tokens";
        const displayValue = isTokens ? (m.value > 0 ? formatTokens(m.value) : "\u2014") : `${m.value}${m.suffix || ""}`;

        return (
          <article
            key={m.key}
            className={styles.metric}
            tabIndex={m.tooltip ? 0 : undefined}
            onMouseEnter={() => m.tooltip && setTooltipKey(m.key)}
            onMouseLeave={() => setTooltipKey(null)}
            onFocus={() => m.tooltip && setTooltipKey(m.key)}
            onBlur={() => setTooltipKey(null)}
            aria-label={`${m.label}: ${displayValue}`}
          >
            <div className={styles.iconBox}><Icon style={{ width: 16, height: 16 }} /></div>
            <div className={styles.metricBody}>
              <div className={styles.label}>{m.label}</div>
              <div className={styles.value}>{displayValue}</div>
              {m.key === "progress" && (
                <div className={styles.progressTrack}>
                  <span style={{ width: `${Math.max(0, Math.min(m.value, 100))}%` }} />
                </div>
              )}
              {isTokens && m.value > 0 && <div className={styles.estimated}>estimated</div>}
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
