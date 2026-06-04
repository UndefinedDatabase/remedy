import type { RemedyApiHealth } from "../../api/types";
import styles from "./DegradedBanner.module.css";

function WarningGlyph(p: React.SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" {...p}>
      <path d="M8 3L2 13h12L8 3z" />
      <line x1="8" y1="7" x2="8" y2="10" />
      <circle cx="8" cy="11.5" r=".5" fill="currentColor" />
    </svg>
  );
}

export function DegradedBanner({ apiHealth }: { apiHealth: RemedyApiHealth }) {
  if (!apiHealth.degraded) return null;
  return (
    <div className={styles.banner} role="alert" data-ui="degraded-banner">
      <WarningGlyph style={{ width: 16, height: 16, flexShrink: 0 }} />
      <span>
        Some data unavailable: {apiHealth.failedEndpoints.join(", ")}.
        Dashboard may show incomplete information.
      </span>
    </div>
  );
}
