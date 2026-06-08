import { RemedyMark } from "../icons/RemedyGlyphs";
import styles from "./RemedyLogo.module.css";

export function RemedyLogo() {
  return (
    <div className={styles.logo} aria-label="Remedy">
      <RemedyMark className={styles.mark} />
      <span className={styles.word}>REMEDY</span>
    </div>
  );
}
