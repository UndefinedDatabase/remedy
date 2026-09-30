// T5_F044 T002, DECISION F044 D6 — the one listener the graph's keys go through: every keydown
// the page receives is read through the keymap (api/keymap.ts) and handed to zoomKeys.ts, whose
// pick is dispatched to the zoom machine as the SAME click a pointer would make.
import { useEffect, useLayoutEffect, useRef } from "react";
import { keymapAction } from "../../api/keymap";
import type { ZoomEvent, ZoomGraph, ZoomState } from "./semanticZoom";
import { zoomKeyStep } from "./zoomKeys";

export function useZoomKeys(
  graph: ZoomGraph,
  state: ZoomState,
  dispatch: (event: ZoomEvent) => void,
  onPick: (nodeId: string) => void,
): void {
  const latest = useRef({ graph, state, onPick });
  useLayoutEffect(() => {
    latest.current = { graph, state, onPick };
  });

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      const target = event.target instanceof HTMLElement ? event.target : null;
      const dialogOpen = document.querySelector('[role="dialog"]') !== null;
      const { action } = keymapAction(event, target, false, dialogOpen);
      if (action === null) return;
      const step = zoomKeyStep(latest.current.graph, latest.current.state, action);
      if (step === null) return;
      event.preventDefault();
      if (step.kind === "walk-back") {
        dispatch({ type: "escape" });
      } else {
        dispatch({ type: "click", nodeId: step.nodeId });
        latest.current.onPick(step.nodeId);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [dispatch]);
}
