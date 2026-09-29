// The Term component (T5_F043 T001, DECISION F043 D1): wraps a word in a span carrying its
// `data-term` key, and — for a key the catalog knows — a glass tooltip that opens on hover
// (after TERM_HOVER_DELAY_MS) and on focus (at once), and closes on blur, pointer-leave or
// Escape. The tooltip is portalled into `document.body` because a glass card's
// `backdrop-filter` confines a fixed descendant and a card's `overflow` clips an absolute one —
// either would trap the tip inside whatever panel the term happens to sit in.
import { useEffect, useId, useLayoutEffect, useRef, useState } from "react";
import type { KeyboardEvent, ReactNode } from "react";
import { createPortal } from "react-dom";
import { termEntry } from "../../api/terminology";
import styles from "./Term.module.css";

export const TERM_HOVER_DELAY_MS = 120;

const VIEWPORT_MARGIN = 8;
const TIP_GAP = 6;

interface TipPlacement {
  left: number;
  top: number;
}

export function Term({ term, children }: { term: string; children: ReactNode }) {
  const entry = termEntry(term);
  const spanRef = useRef<HTMLSpanElement>(null);
  const tipRef = useRef<HTMLSpanElement>(null);
  const [hovering, setHovering] = useState(false);
  const [open, setOpen] = useState(false);
  const [placement, setPlacement] = useState<TipPlacement | null>(null);
  const tipId = useId();

  // The hover delay: entering the term starts this effect; leaving before it fires cancels the
  // pending timer in the cleanup below, so nothing opens.
  useEffect(() => {
    if (!hovering) return undefined;
    const timer = window.setTimeout(() => setOpen(true), TERM_HOVER_DELAY_MS);
    return () => window.clearTimeout(timer);
  }, [hovering]);

  // Measured before paint, from the term's own box and the tip's own size, against the
  // viewport: below the term unless there is no room, then above it; never inside the margin.
  useLayoutEffect(() => {
    if (!open) return;
    const termNode = spanRef.current;
    const tipNode = tipRef.current;
    if (!termNode || !tipNode) return;
    const termBox = termNode.getBoundingClientRect();
    const width = document.documentElement.clientWidth;
    const height = document.documentElement.clientHeight;
    const tipWidth = tipNode.offsetWidth;
    const tipHeight = tipNode.offsetHeight;
    let left = termBox.left;
    left = Math.min(left, width - VIEWPORT_MARGIN - tipWidth);
    left = Math.max(VIEWPORT_MARGIN, left);
    let top = termBox.bottom + TIP_GAP;
    if (top + tipHeight > height - VIEWPORT_MARGIN) {
      top = termBox.top - TIP_GAP - tipHeight;
    }
    top = Math.max(VIEWPORT_MARGIN, top);
    setPlacement({ left, top });
  }, [open]);

  if (entry === null) {
    return <span className={styles.term} data-term={term}>{children}</span>;
  }

  const closeTooltip = () => {
    setOpen(false);
    setPlacement(null);
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLSpanElement>) => {
    if (event.key === "Escape" && open) {
      event.stopPropagation();
      closeTooltip();
    }
  };

  return (
    <span
      ref={spanRef}
      className={styles.term}
      data-term={term}
      tabIndex={0}
      aria-describedby={open ? tipId : undefined}
      onPointerEnter={() => setHovering(true)}
      onPointerLeave={() => { setHovering(false); closeTooltip(); }}
      onFocus={() => setOpen(true)}
      onBlur={closeTooltip}
      onKeyDown={handleKeyDown}
    >
      {children}
      {open && createPortal(
        <span
          ref={tipRef}
          role="tooltip"
          id={tipId}
          className={styles.tip}
          data-ui="term-tip"
          data-term-tip={term}
          data-placed={placement ? "true" : "false"}
          style={placement ? { left: placement.left, top: placement.top } : undefined}
        >
          <span className={styles.tipTitle}>{entry.title}</span>
          <span className={styles.tipBody}>{entry.body}</span>
        </span>,
        document.body,
      )}
    </span>
  );
}
