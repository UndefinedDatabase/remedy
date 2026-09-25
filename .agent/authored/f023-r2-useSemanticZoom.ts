// The hook graph_spec.md §10 names: it holds the semantic-zoom state for the
// stage, feeds every event through the pure machine (semanticZoom.ts), walks
// back on Escape, and re-checks the focus whenever the graph changes under it.
// Everything that decides a transition lives in the machine; this file only
// owns React state and the one window listener (DECISION F023 D2).
import { useCallback, useEffect, useLayoutEffect, useRef, useState } from "react";
import { ZOOM_HOME, zoomTransition } from "./semanticZoom";
import type { ZoomEvent, ZoomGraph, ZoomState } from "./semanticZoom";
import { escapeWalksBack } from "./zoomView";

export interface SemanticZoom {
  state: ZoomState;
  /** The last refusal's debug note, or null; shown on the stage as a data
   *  attribute for a test or a reviewer, never as UI text. */
  note: string | null;
  dispatch: (event: ZoomEvent) => void;
}

export function useSemanticZoom(graph: ZoomGraph): SemanticZoom {
  const [current, setCurrent] = useState<{ state: ZoomState; note: string | null }>({ state: ZOOM_HOME, note: null });
  const graphRef = useRef(graph);
  useLayoutEffect(() => {
    graphRef.current = graph;
  }, [graph]);

  const dispatch = useCallback((event: ZoomEvent) => {
    setCurrent((prev) => {
      const step = zoomTransition(graphRef.current, prev.state, event);
      if (step.state === prev.state && step.note === prev.note) return prev;
      return { state: step.state, note: step.note };
    });
  }, []);

  // A graph that changed under the focus never leaves it dangling.
  useEffect(() => {
    dispatch({ type: "reconcile" });
  }, [graph, dispatch]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== "Escape") return;
      const target = e.target instanceof HTMLElement ? e.target : null;
      if (!escapeWalksBack(target, document.querySelector('[role="dialog"]') !== null)) return;
      dispatch({ type: "escape" });
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [dispatch]);

  return { state: current.state, note: current.note, dispatch };
}
