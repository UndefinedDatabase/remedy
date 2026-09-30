import { useEffect, useState } from "react";
import type { TourAnchor, TourStop, TourView } from "../../api/resultTour";
import {
  tourAnchorLabel,
  tourCanShow,
  tourGeneratorLabel,
  tourNeighbours,
  tourPanelState,
  tourProgress,
  tourStepLabel,
} from "../../api/resultTour";
import { loadTourView } from "../../api/remedyApi";
import { TourFrame } from "./TourFrame";
import styles from "./TourOverlay.module.css";

/** What the overlay says while the view is in flight. */
const TOUR_LOADING_LINE = "Reading the tour…";

/**
 * The guided result tour's browser surface (F036 T003, DECISION F036 D6): a dimmed backdrop
 * and one glass card that steps through the job's own tour, built by `resultTour.ts` from the
 * view `loadTourView` reads once. "Show me" hands the current stop's anchor to the shell and
 * lifts the backdrop, so the place the stop names is the one thing left undimmed; stepping to
 * another stop dims the page again.
 *
 * The backdrop, the card and the portal are `TourFrame`'s, the overlay engine this tour shares
 * with the first-run tour (DECISION F043 D4).
 */
export function TourOverlay({ jobId, serverToken, onClose, onShowAnchor }: {
  jobId: string;
  serverToken: string;
  onClose: () => void;
  onShowAnchor: (anchor: TourAnchor) => void;
}) {
  // `null` until the first answer; after it, the view or `null` for "could not be read".
  const [read, setRead] = useState<{ view: TourView | null } | null>(null);
  const [current, setCurrent] = useState(0);
  // Whether "Show me" was pressed for the CURRENT stop: it lifts the backdrop while the card
  // stays, and stepping to another stop clears it so the dim returns.
  const [shown, setShown] = useState(false);

  // THE READ. `cancelled` answers a response that arrives after the job or the token moved on,
  // the same guard `LessonsOverlay.tsx` and `RemedyShell.tsx`'s own loads use.
  useEffect(() => {
    let cancelled = false;
    void loadTourView({ jobId, token: serverToken }).then((view) => {
      if (!cancelled) setRead({ view });
    });
    return () => { cancelled = true; };
  }, [jobId, serverToken]);

  const panelState = tourPanelState(read ? read.view : null, read !== null);
  const stops: TourStop[] = panelState.kind === "stops" ? panelState.stops : [];
  const generator = read?.view ? read.view.tour.generator : "";
  const at = stops.length > 0 ? Math.min(current, stops.length - 1) : 0;
  const neighbours = tourNeighbours(stops.length, at);

  function stepTo(index: number | null) {
    if (index === null) return;
    setCurrent(index);
    setShown(false);
  }

  // Esc closes the overlay; the arrow keys step, exactly as Previous and Next do below.
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
      else if (event.key === "ArrowLeft") stepTo(neighbours.previous);
      else if (event.key === "ArrowRight") stepTo(neighbours.next);
    };
    window.addEventListener("keydown", onKey);
    return () => { window.removeEventListener("keydown", onKey); };
  }, [onClose, neighbours.previous, neighbours.next]);

  function handleShowMe(stop: TourStop) {
    onShowAnchor(stop.anchor);
    setShown(true);
  }

  // The backdrop stays over the page except while a stop is shown, when the place the stop
  // names is the one thing left undimmed.
  const backdropVisible = !(panelState.kind === "stops" && shown);

  return (
    <TourFrame label="Guided tour" ui={{ card: "tour-overlay", backdrop: "tour-backdrop" }}
      shown={!backdropVisible} closeLabel="Close tour" onClose={onClose}>
      {panelState.kind === "loading" && (
        <p className={styles.quiet} data-ui="tour-loading">{TOUR_LOADING_LINE}</p>
      )}
      {(panelState.kind === "unreadable" || panelState.kind === "empty") && (
        <p className={styles.quiet} data-ui="tour-message">{panelState.line}</p>
      )}
      {panelState.kind === "stops" && (
        <TourStopBody
          stops={stops}
          current={at}
          generator={generator}
          neighbours={neighbours}
          onPrevious={() => stepTo(neighbours.previous)}
          onNext={() => stepTo(neighbours.next)}
          onShowMe={handleShowMe}
        />
      )}
    </TourFrame>
  );
}

function TourStopBody({ stops, current, generator, neighbours, onPrevious, onNext, onShowMe }: {
  stops: TourStop[];
  current: number;
  generator: string;
  neighbours: { previous: number | null; next: number | null };
  onPrevious: () => void;
  onNext: () => void;
  onShowMe: (stop: TourStop) => void;
}) {
  const stop = stops[current];
  const progress = tourProgress(stops.length, current);
  return (
    <>
      <p className={styles.stepLabel}>{tourStepLabel(stops.length, current)}</p>
      <ol className={styles.progress} data-ui="tour-progress">
        {progress.map((state, index) => (
          <li key={index} data-state={state} />
        ))}
      </ol>
      <h3 className={styles.title}>{stop.title}</h3>
      <p className={styles.body}>{stop.body}</p>
      <p className={styles.anchor}>
        {stop.anchor.kind === "command"
          ? <>Command <code>{stop.anchor.ref}</code></>
          : tourAnchorLabel(stop.anchor)}
      </p>
      <p className={styles.generator}>{tourGeneratorLabel(generator)}</p>
      <div className={styles.actions}>
        <button type="button" onClick={onPrevious} disabled={neighbours.previous === null}>
          Previous
        </button>
        <button type="button" onClick={onNext} disabled={neighbours.next === null}>
          Next
        </button>
        {tourCanShow(stop.anchor) && (
          <button type="button" onClick={() => onShowMe(stop)}>Show me</button>
        )}
      </div>
    </>
  );
}
