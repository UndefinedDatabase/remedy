import { NetworkLogoIcon } from "../icons/NetworkLogoIcon";
import styles from "./RemedyLogo.module.css";

export function RemedyLogo() {
  return <div className={styles.logo}><NetworkLogoIcon className={styles.mark} /><span className={styles.word}>REMEDY</span></div>;
}
