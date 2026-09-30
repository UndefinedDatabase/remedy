// T5_F044 T001, DECISION F044 D2 — the bar as the palette's combobox: it binds its own
// browser-storage edge for the remembered rows (the shell's one `window.localStorage` binding is
// the digest's, `tests/ui_contracts/test_digest_mount.py`), builds the sheet's rows from the
// query, and drives the dropdown sheet with the keyboard exactly as a combobox must.
import { useId, useMemo, useRef, useState } from "react";
import type { KeyboardEvent } from "react";
import type { RemedyNextAction } from "../../api/types";
import type { JumpTarget } from "../../api/paletteJump";
import type { PaletteProject, PaletteRow } from "../../api/paletteSheet";
import {
  buildPaletteRows,
  movePaletteCursor,
  readPaletteRecents,
  rememberPaletteRef,
  writePaletteRecents,
} from "../../api/paletteSheet";
import { SparkGlyph, ArrowSendGlyph } from "../icons/RemedyGlyphs";
import { PaletteSheet, paletteOptionId } from "./PaletteSheet";
import styles from "./CommandBar.module.css";

export function CommandBar({
  nextAction,
  targets,
  projects,
  activeSlug,
  onJump,
  onSwitchProject,
  onOpenTerms,
  onStartTour,
}: {
  nextAction: RemedyNextAction;
  targets: readonly JumpTarget[];
  projects: readonly PaletteProject[];
  activeSlug: string;
  onJump: (nodeId: string) => void;
  onSwitchProject: (slug: string) => void;
  onOpenTerms: () => void;
  onStartTour: () => void;
}) {
  // THE STORAGE EDGE, bound here because this is the edge — the file's only `window.localStorage`,
  // built once per mount the way RemedyShell.tsx binds its own digest port.
  const storage = useMemo(() => window.localStorage, []);
  const [recents, setRecents] = useState<readonly string[]>(() => readPaletteRecents(storage));

  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const sectionRef = useRef<HTMLElement>(null);
  const listId = useId();

  const rows = useMemo<readonly PaletteRow[]>(
    () => buildPaletteRows({ query, targets, projects, activeSlug, recents }),
    [query, targets, projects, activeSlug, recents],
  );
  const shown = open && rows.length > 0;
  const activeRowId =
    shown && activeIndex >= 0 && activeIndex < rows.length ? paletteOptionId(listId, activeIndex) : undefined;

  function chooseRow(row: PaletteRow) {
    const nextRecents = rememberPaletteRef(recents, row.ref);
    setRecents(nextRecents);
    writePaletteRecents(storage, nextRecents);
    setQuery("");
    setOpen(false);
    setActiveIndex(-1);
    switch (row.action.kind) {
      case "jump":
        onJump(row.action.nodeId);
        break;
      case "project":
        onSwitchProject(row.action.slug);
        break;
      case "terms":
        onOpenTerms();
        break;
      case "tour":
        onStartTour();
        break;
    }
  }

  function handleKeyDown(event: KeyboardEvent<HTMLInputElement>) {
    if (event.key === "ArrowDown") {
      event.preventDefault();
      setOpen(true);
      setActiveIndex((index) => movePaletteCursor(rows.length, index, 1));
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      setOpen(true);
      setActiveIndex((index) => movePaletteCursor(rows.length, index, -1));
    } else if (event.key === "Enter") {
      if (rows.length === 0) return;
      const row = activeIndex >= 0 && activeIndex < rows.length ? rows[activeIndex] : rows[0];
      chooseRow(row);
    } else if (event.key === "Escape") {
      setOpen(false);
      setActiveIndex(-1);
    }
  }

  return (
    <section ref={sectionRef} className={styles.commandBar} aria-label="Jump to anything" data-ui="command-bar">
      <div className={styles.spark}><SparkGlyph style={{ width: 16, height: 16 }} /></div>
      <input
        aria-label="Jump to a task or file"
        role="combobox"
        aria-expanded={shown}
        aria-controls={listId}
        aria-autocomplete="list"
        aria-activedescendant={activeRowId}
        value={query}
        placeholder='Jump to anything (e.g., "error handling")'
        onChange={e => { setQuery(e.target.value); setOpen(true); setActiveIndex(0); }}
        onFocus={() => setOpen(true)}
        onBlur={() => { setOpen(false); setActiveIndex(-1); }}
        onKeyDown={handleKeyDown}
      />
      <span className={styles.hint} title={`Next safe action: ${nextAction.command}`}>
        next: {nextAction.label}
      </span>
      <button
        type="button"
        className={styles.actionBtn}
        aria-label="Copy next safe command"
        title={`Copy: ${nextAction.command}`}
        onClick={() => navigator.clipboard?.writeText(nextAction.command)}
      >
        <ArrowSendGlyph style={{ width: 16, height: 16 }} />
      </button>
      {shown && (
        <PaletteSheet
          rows={rows}
          activeIndex={activeIndex}
          listId={listId}
          anchor={sectionRef.current}
          onChoose={chooseRow}
          onHover={setActiveIndex}
        />
      )}
    </section>
  );
}
