// Binds the zoom's deep link (zoomDeepLink.ts) to the page: the link in the URL
// is read once, replayed through the machine as soon as the graph holds its
// node, and from then on the URL follows the zoom state through
// history.replaceState — no router, no navigation, no history entry per step.
// A link whose node has not arrived yet waits; the reader taking over first
// cancels it (DECISION F023 D6).
import { useEffect, useRef, useState } from "react";
import { ZOOM_HOME } from "./semanticZoom";
import type { ZoomEvent, ZoomGraph, ZoomState } from "./semanticZoom";
import { searchWithZoom, zoomLinkEvents, zoomLinkFromSearch } from "./zoomDeepLink";
import type { ZoomLink } from "./zoomDeepLink";

export function useZoomDeepLink(graph: ZoomGraph, state: ZoomState, dispatch: (event: ZoomEvent) => void): void {
  const [linkAtOpen] = useState(() => zoomLinkFromSearch(window.location.search));
  const pendingRef = useRef<ZoomLink | null>(linkAtOpen);

  useEffect(() => {
    const link = pendingRef.current;
    if (!link || !graph.has(link.focusId)) return;
    pendingRef.current = null;
    zoomLinkEvents(link).forEach(dispatch);
  }, [graph, dispatch]);

  useEffect(() => {
    if (pendingRef.current) {
      if (state === ZOOM_HOME) return;
      pendingRef.current = null;
    }
    const next = searchWithZoom(window.location.search, state);
    if (next === window.location.search) return;
    window.history.replaceState(window.history.state, "", `${window.location.pathname}${next}${window.location.hash}`);
  }, [state]);
}
