import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import type { RemedyNextAction } from "../../api/types";
import styles from "./CommandBar.module.css";

export function CommandBar({ nextAction }: { nextAction: RemedyNextAction }) {
  return (
    <section className={styles.commandBar} aria-label="Command search" data-ui="command-bar">
      <div className={styles.spark}><AutoAwesomeIcon fontSize="small" /></div>
      <input readOnly aria-label="Ask Remedy" value="" placeholder={`Ask your agent or jump to anything (e.g., "${nextAction.label}")`} />
      <button type="button" aria-label="Copy suggested command" title={`Copy command: ${nextAction.command}`} onClick={() => navigator.clipboard?.writeText(nextAction.command)}>
        <ArrowBackIcon />
      </button>
    </section>
  );
}
