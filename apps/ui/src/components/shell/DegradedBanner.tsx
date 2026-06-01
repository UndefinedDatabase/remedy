import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import type { RemedyApiHealth } from "../../api/types";
import styles from "./DegradedBanner.module.css";

export function DegradedBanner({ apiHealth }: { apiHealth: RemedyApiHealth }) {
  if (!apiHealth.degraded) return null;
  return (
    <div className={styles.banner} role="alert" data-ui="degraded-banner">
      <WarningAmberIcon fontSize="small" />
      <span>
        Some data unavailable: {apiHealth.failedEndpoints.join(", ")}.
        Dashboard may show incomplete information.
      </span>
    </div>
  );
}
