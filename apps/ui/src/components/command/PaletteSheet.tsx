// T5_F044 T001, DECISIONS F044 D2 and D3 — the bar's dropdown sheet: a listbox of the palette's
// rows, grouped under their section headings, portalled into `document.body` because the bar
// carries a `backdrop-filter` glass card, which confines a fixed descendant to its own box —
// exactly the rule that already portals `Term.tsx`'s tooltip (DECISION F043 D1) — so a sheet
// anchored to a glass bar can only ever sit above the rest of the page from outside that box.
//
// `PaletteStatus` (D3 (4)) is a SIBLING of the listbox, never a child of it: a `role="listbox"`'s
// only valid children are its options, so an outcome sentence lives in its own portalled
// `role="status"` paragraph instead, placed under the bar exactly as the sheet is — the two share
// `usePalettePlacement` so a status shown while the sheet is closed still sits where the sheet
// would.
import { useLayoutEffect, useState } from "react";
import { createPortal } from "react-dom";
import { PALETTE_SECTION_ORDER, highlightPieces } from "../../api/paletteSheet";
import type { PaletteRow } from "../../api/paletteSheet";
import type { DecisionOutcomeMessage } from "../../api/decisionOutcome";
import styles from "./PaletteSheet.module.css";

export const PALETTE_SHEET_GAP_PX = 6;

/** The DOM id of one option row, built from the listbox's own id and the row's index in the
 *  whole (flattened) row list. */
export function paletteOptionId(listId: string, index: number): string {
  return `${listId}-option-${index}`;
}

interface SheetPlacement {
  readonly left: number;
  readonly top: number;
  readonly width: number;
}

/** THE PLACEMENT: measured from the anchor's own box, keyed by the anchor so a fresh bar element
 *  re-measures, and again on every resize while mounted so a placed element tracks a reflowed bar
 *  without waiting for the next keystroke. Shared by the sheet and `PaletteStatus`, unchanged in
 *  behaviour from the sheet's own earlier effect. */
function usePalettePlacement(anchor: HTMLElement | null): SheetPlacement | null {
  const [placement, setPlacement] = useState<SheetPlacement | null>(null);

  useLayoutEffect(() => {
    if (anchor === null) {
      setPlacement(null);
      return undefined;
    }
    const measure = () => {
      const box = anchor.getBoundingClientRect();
      setPlacement({ left: box.left, top: box.bottom + PALETTE_SHEET_GAP_PX, width: box.width });
    };
    measure();
    window.addEventListener("resize", measure);
    return () => { window.removeEventListener("resize", measure); };
  }, [anchor]);

  return placement;
}

export function PaletteSheet({
  rows,
  activeIndex,
  listId,
  anchor,
  onChoose,
  onHover,
}: {
  rows: readonly PaletteRow[];
  activeIndex: number;
  listId: string;
  anchor: HTMLElement | null;
  onChoose: (row: PaletteRow) => void;
  onHover: (index: number) => void;
}) {
  const placement = usePalettePlacement(anchor);

  const indexed = rows.map((row, index) => ({ row, index }));

  return createPortal(
    <div
      id={listId}
      role="listbox"
      aria-label="Command palette results"
      data-ui="palette-sheet"
      data-placed={placement !== null ? "true" : "false"}
      className={styles.sheet}
      style={placement !== null ? { left: placement.left, top: placement.top, width: placement.width } : undefined}
    >
      {PALETTE_SECTION_ORDER.map((section) => {
        const sectionRows = indexed.filter(({ row }) => row.section === section);
        if (sectionRows.length === 0) return null;
        return (
          <div key={section} role="group" aria-label={section} className={styles.group}>
            <div aria-hidden="true" className={styles.heading}>{section}</div>
            {sectionRows.map(({ row, index }) => {
              const active = index === activeIndex;
              const disabled = row.disabledReason !== "";
              return (
                <div
                  key={row.key}
                  role="option"
                  id={paletteOptionId(listId, index)}
                  aria-selected={active}
                  aria-disabled={disabled ? "true" : undefined}
                  title={disabled ? row.disabledReason : undefined}
                  data-palette-row={row.key}
                  className={styles.row}
                  onMouseDown={(event) => event.preventDefault()}
                  onClick={() => onChoose(row)}
                  onPointerMove={() => { if (!active) onHover(index); }}
                >
                  <span className={styles.label}>
                    {highlightPieces(row.label, row.ranges).map((piece, pieceIndex) =>
                      piece.hit
                        ? <mark key={pieceIndex}>{piece.text}</mark>
                        : <span key={pieceIndex}>{piece.text}</span>,
                    )}
                  </span>
                  <span className={styles.hint}>{row.hint}</span>
                </div>
              );
            })}
          </div>
        );
      })}
    </div>,
    document.body,
  );
}

/** THE OUTCOME LINE (DECISION F044 D3 (4)): a `role="status"` paragraph, placed exactly as the
 *  sheet is, in the chat outcome line's own tones. A SIBLING of the listbox rather than a row
 *  inside it — see the header — so it renders whether or not the sheet itself is shown. */
export function PaletteStatus({
  status,
  anchor,
}: {
  status: DecisionOutcomeMessage;
  anchor: HTMLElement | null;
}) {
  const placement = usePalettePlacement(anchor);

  return createPortal(
    <p
      role="status"
      data-ui="palette-outcome"
      data-tone={status.tone}
      data-placed={placement !== null ? "true" : "false"}
      className={styles.status}
      style={placement !== null ? { left: placement.left, top: placement.top, width: placement.width } : undefined}
    >
      {status.sentence}
    </p>,
    document.body,
  );
}
