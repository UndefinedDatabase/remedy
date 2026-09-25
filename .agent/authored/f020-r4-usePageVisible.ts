import { useEffect, useState } from "react";

/** Whether the page is visible right now, following the document's
 *  `visibilitychange` event. The brain graph asks for no animation frame while
 *  it is hidden, so a background tab spins no CPU (motion_spec.md: "pulses
 *  pause when tab hidden"), and it keeps no timer of its own. */
export function usePageVisible(): boolean {
  const [visible, setVisible] = useState(() => typeof document === "undefined" || document.visibilityState !== "hidden");
  useEffect(() => {
    const onChange = () => setVisible(document.visibilityState !== "hidden");
    document.addEventListener("visibilitychange", onChange);
    return () => document.removeEventListener("visibilitychange", onChange);
  }, []);
  return visible;
}
