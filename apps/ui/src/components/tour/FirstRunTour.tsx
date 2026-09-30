import { useEffect, useLayoutEffect, useMemo, useState } from "react";
import {
  FIRST_RUN_STEPS,
  firstRunStepLabel,
  firstRunTourDue,
  markFirstRunTourSeen,
} from "../../api/firstRunTour";
import { tourNeighbours, tourProgress } from "../../api/resultTour";
import { TourFrame } from "./TourFrame";
import type { TourSpot } from "./TourFrame";
import styles from "./TourOverlay.module.css";

/** The step's own region, measured from the live page, or `null` when it cannot be found or
 *  has no area to spotlight. `scroll` is true only for the measurement a step change makes —
 *  a resize re-measures the SAME region without scrolling the page again. */
function measureSpot(target: string, scroll: boolean): TourSpot | null {
  const el = document.querySelector(`[data-ui="${target}"]`);
  if (!(el instanceof HTMLElement)) return null;
  if (scroll) el.scrollIntoView({ block: "nearest", inline: "nearest" });
  const box = el.getBoundingClientRect();
  if (box.width <= 0 || box.height <= 0) return null;
  return { left: box.left, top: box.top, width: box.width, height: box.height };
}

/**
 * The first-run tour (T5_F043 T003, DECISION F043 D4): six steps, each spotlighting its own
 * region of the shell through `TourFrame`, the overlay engine the result tour renders through
 * too. Skip, Finish, Close and Escape all end it.
 */
export function FirstRunTour({ onClose }: { onClose: () => void }) {
  const [current, setCurrent] = useState(0);
  const [spot, setSpot] = useState<TourSpot | null>(null);
  const step = FIRST_RUN_STEPS[current];
  const neighbours = tourNeighbours(FIRST_RUN_STEPS.length, current);

  // THE SPOT, measured before paint so the ring never flashes at the wrong place, scrolled
  // into view first since a step may point at a region the page has not shown yet.
  useLayoutEffect(() => {
    setSpot(measureSpot(step.target, true));
  }, [step.target]);

  // Re-measured on resize, without scrolling again — the region did not move in the page, the
  // viewport did.
  useEffect(() => {
    const onResize = () => setSpot(measureSpot(step.target, false));
    window.addEventListener("resize", onResize);
    return () => { window.removeEventListener("resize", onResize); };
  }, [step.target]);

  function stepTo(index: number | null) {
    if (index === null) return;
    setCurrent(index);
  }

  // Esc closes the tour; the arrow keys step, exactly as Previous and Next do below.
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
      else if (event.key === "ArrowLeft") stepTo(neighbours.previous);
      else if (event.key === "ArrowRight") stepTo(neighbours.next);
    };
    window.addEventListener("keydown", onKey);
    return () => { window.removeEventListener("keydown", onKey); };
  }, [onClose, neighbours.previous, neighbours.next]);

  const progress = tourProgress(FIRST_RUN_STEPS.length, current);

  return (
    <TourFrame label="Welcome tour" ui={{ card: "first-run-tour", backdrop: "first-run-backdrop" }}
      shown={false} spot={spot} closeLabel="Close tour" onClose={onClose}>
      <p className={styles.stepLabel}>{firstRunStepLabel(FIRST_RUN_STEPS.length, current)}</p>
      <ol className={styles.progress} data-ui="tour-progress">
        {progress.map((state, index) => (
          <li key={index} data-state={state} />
        ))}
      </ol>
      <h3 className={styles.title}>{step.title}</h3>
      <p className={styles.body}>{step.body}</p>
      <div className={styles.actions}>
        <button type="button" onClick={onClose}>Skip tour</button>
        <button type="button" onClick={() => stepTo(neighbours.previous)} disabled={neighbours.previous === null}>
          Previous
        </button>
        {neighbours.next === null ? (
          <button type="button" onClick={onClose}>Finish</button>
        ) : (
          <button type="button" onClick={() => stepTo(neighbours.next)}>Next</button>
        )}
      </div>
    </TourFrame>
  );
}

/**
 * The tour's storage edge (DECISION F043 D4): bound here, not in the shell, because the shell
 * keeps its one `window.localStorage` binding for the digest (`test_digest_mount.py`) and hands
 * this mount only a relaunch count.
 */
export function FirstRunTourMount({ relaunch }: { relaunch: number }) {
  const storage = useMemo(() => window.localStorage, []);
  const [open, setOpen] = useState(() => firstRunTourDue(storage));

  useEffect(() => {
    if (relaunch > 0) setOpen(true);
  }, [relaunch]);

  if (!open) return null;

  return (
    <FirstRunTour onClose={() => { markFirstRunTourSeen(storage); setOpen(false); }} />
  );
}
