import { createPortal } from "react-dom";
import styles from "./TourOverlay.module.css";

/**
 * The overlay engine both tours render through (T5_F043 T003, DECISION F043 D4): the portal,
 * the dialog named by its label, its close button, and the dim — a whole-page backdrop, or,
 * given a `spot`, that same tint drawn as a ring around the named box so the region stays
 * bright and usable, the card docked at the lower left the way a shown result-tour stop already
 * docks. The result tour (`TourOverlay.tsx`) and the first-run tour (`FirstRunTour.tsx`) each
 * name their own `data-ui` values and hand this frame their own content.
 *
 * PORTALED TO `document.body`, for the reason `AddTaskSheet.tsx`'s own portal comment records
 * (R-1079): an ancestor's `backdrop-filter` confines a `position: fixed` descendant to its own
 * box, and a tour is meant to cover the whole viewport regardless of where the shell mounts it.
 */

/** One region a tour step points at, in viewport pixels. */
export interface TourSpot {
  readonly left: number;
  readonly top: number;
  readonly width: number;
  readonly height: number;
}

/** How far the spotlight ring sits beyond the spot's own box. */
export const TOUR_SPOT_PAD_PX = 6;

export function TourFrame({ label, ui, shown, spot = null, closeLabel, onClose, children }: {
  label: string;
  ui: { readonly card: string; readonly backdrop: string };
  shown: boolean;
  spot?: TourSpot | null;
  closeLabel: string;
  onClose: () => void;
  children: React.ReactNode;
}) {
  const spotDrawn = !shown && spot !== null;
  return createPortal(
    <>
      {!shown && spot === null && <div className={styles.backdrop} data-ui={ui.backdrop} />}
      {spotDrawn && spot !== null && (
        <div
          className={styles.spot}
          data-ui={ui.backdrop}
          style={{
            left: spot.left - TOUR_SPOT_PAD_PX,
            top: spot.top - TOUR_SPOT_PAD_PX,
            width: spot.width + TOUR_SPOT_PAD_PX * 2,
            height: spot.height + TOUR_SPOT_PAD_PX * 2,
          }}
        />
      )}
      <section role="dialog" aria-label={label} className={styles.card} data-ui={ui.card}
        data-shown={shown ? "true" : "false"} data-spot={spotDrawn ? "true" : "false"}>
        <header className={styles.header}>
          <h2>{label}</h2>
          <button type="button" className={styles.close} onClick={onClose}>{closeLabel}</button>
        </header>
        {children}
      </section>
    </>,
    document.body,
  );
}
