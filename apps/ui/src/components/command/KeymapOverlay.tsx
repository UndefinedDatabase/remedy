// T5_F044 T002, DECISION F044 D6 — the keymap's own cheat overlay, shown while "?" is held past
// KEYMAP_HOLD_MS (useHeldHelpKey.ts): every binding KEYMAP_BINDINGS carries, verbatim.
import { KEYMAP_BINDINGS } from "../../api/keymap";
import styles from "./KeymapOverlay.module.css";

export const KEYMAP_OVERLAY_TITLE = "Keyboard shortcuts";
export const KEYMAP_OVERLAY_HINT = "Let go of ? to close it. A quick press of ? shows every term.";

export function KeymapOverlay() {
  return (
    <section className={styles.sheet} role="dialog" aria-label={KEYMAP_OVERLAY_TITLE} data-ui="keymap-overlay">
      <h2>{KEYMAP_OVERLAY_TITLE}</h2>
      <dl className={styles.rows}>
        {KEYMAP_BINDINGS.map((binding) => (
          <div key={binding.action} className={styles.row} data-keymap-action={binding.action}>
            <dt><kbd className={styles.keys}>{binding.keys}</kbd></dt>
            <dd>{binding.label}</dd>
          </div>
        ))}
      </dl>
      <p className={styles.hint}>{KEYMAP_OVERLAY_HINT}</p>
    </section>
  );
}
