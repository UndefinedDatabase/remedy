import { useCallback, useEffect, useRef, useState } from "react";

export function useGraphSize() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ width: 800, height: 500 });

  const updateSize = useCallback(() => {
    const el = containerRef.current;
    if (el) setSize({ width: el.clientWidth, height: el.clientHeight });
  }, []);

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    updateSize();
    const observer = new ResizeObserver(updateSize);
    observer.observe(el);
    return () => observer.disconnect();
  }, [updateSize]);

  return { containerRef, size };
}
