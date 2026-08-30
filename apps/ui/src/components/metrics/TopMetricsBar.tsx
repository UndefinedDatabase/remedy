import { useState } from "react";
import type { RemedyMetric } from "../../api/types";
import { formatTokenCount } from "../../api/costMetric";
import {
  ClipboardGlyph, CalendarGlyph, TaskDoneGlyph, ChartGlyph, TokenGlyph,
  FlaskGlyph, ShieldCheckGlyph, CoinGlyph,
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
  cost: CoinGlyph,
};

const stateDotClass: Record<string, string> = {
  pass: styles.statePass,
  fail: styles.stateFail,
  none: styles.stateNone,
};

/** The track treatment per threshold band, looked up from the view's own
 *  `level` so the component classifies nothing itself — DECISION F022 D5
 *  clause 1. */
const costLevelClass: Record<string, string> = {
  normal: styles.costNormal,
  warn: styles.costWarn,
  exceeded: styles.costExceeded,
};

/** The same threshold in WORDS for the accessible name: DECISION F022 D5
 *  clause 3 forbids a state a reader can only see as a tint. */
const costLevelPhrase: Record<string, string> = {
  warn: ", warning: near the budget limit",
  exceeded: ", alert: over the budget limit",
};

/** The estimate marker, which is the BASIS channel and never the threshold
 *  channel: a mark shown at a threshold would be a false claim about where the
 *  figure came from. */
export const ESTIMATE_MARK = "~";

/** Said in words beside the mark, because the mark alone is punctuation a
 *  screen reader does not narrate. */
export const ESTIMATE_PHRASE = ", estimated";

const EM_DASH = "—";

/** Main value text (without suffix). Unknown / em-dash safe. */
function mainValue(m: RemedyMetric): string {
  // The cost view has already decided its own text, its own honest em dash
  // included, so it is read before `value` is consulted at all.
  if (m.key === "cost") return m.cost ? m.cost.display : EM_DASH;
  if (m.unknown || m.value === EM_DASH) return EM_DASH;
  if (m.key === "tokens") {
    return typeof m.value === "number" && m.value > 0 ? formatTokenCount(m.value) : EM_DASH;
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
        const hasTooltip = Boolean(m.tooltip) || Boolean(m.cost);
        const costPhrase = m.cost
          ? `${m.cost.estimated ? ESTIMATE_PHRASE : ""}${costLevelPhrase[m.cost.level || ""] || ""}`
          : "";
        const costTrackClass = m.cost
          ? `${styles.costTrack} ${costLevelClass[m.cost.level || ""] || ""}`
          : "";

        return (
          <article
            key={m.key}
            className={styles.metric}
            tabIndex={hasTooltip ? 0 : undefined}
            onMouseEnter={() => hasTooltip && setTooltipKey(m.key)}
            onMouseLeave={() => setTooltipKey(null)}
            onFocus={() => hasTooltip && setTooltipKey(m.key)}
            onBlur={() => setTooltipKey(null)}
            aria-label={`${m.label}: ${ariaValue}${costPhrase}`}
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
                {m.cost?.estimated && <span className={styles.estimateMark}>{ESTIMATE_MARK}</span>}
                {main}
                {showSuffix && <span className={styles.valueSuffix}>{m.suffix}</span>}
              </div>
              {m.key === "progress" && (
                <div className={styles.progressTrack}>
                  <span style={{ width: `${progressWidth}%` }} />
                </div>
              )}
              {m.cost && m.cost.fill !== null && (
                <div className={costTrackClass}>
                  <span style={{ width: `${Math.max(0, Math.min(m.cost.fill * 100, 100))}%` }} />
                </div>
              )}
              {isTokens && main !== EM_DASH && <div className={styles.estimated}>estimated</div>}
              {/* Already worded by the reconciliation module, which is why this
                  renders the field and composes nothing (DECISION F022 D8). */}
              {m.costFinalNote && <div className={styles.estimated}>{m.costFinalNote}</div>}
            </div>
            {tooltipKey === m.key && m.tooltip && (
              <div className={styles.tooltip} role="tooltip" data-testid="token-tooltip">
                {Object.entries(m.tooltip).map(([role, count]) => (
                  <div key={role} className={styles.tooltipRow}>
                    <span>{role}</span>
                    <span>{formatTokenCount(count)}</span>
                  </div>
                ))}
              </div>
            )}
            {tooltipKey === m.key && m.cost && (
              <div className={styles.tooltip} role="tooltip" data-testid="cost-tooltip">
                {m.cost.tooltip.map(line => (
                  <div key={line} className={styles.costTooltipRow}>{line}</div>
                ))}
              </div>
            )}
          </article>
        );
      })}
    </section>
  );
}
