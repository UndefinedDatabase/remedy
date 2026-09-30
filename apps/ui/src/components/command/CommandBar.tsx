// T5_F044 T001, DECISIONS F044 D2 and D3 — the bar as the palette's combobox, and, since D3, the
// one place a command's argument flow runs: it binds its own browser-storage edge for the
// remembered rows (the shell's one `window.localStorage` binding is the digest's,
// `tests/ui_contracts/test_digest_mount.py`), builds the sheet's rows from the query, drives the
// dropdown sheet with the keyboard exactly as a combobox must, and, while a chosen command's flow
// is open, asks its arguments one at a time in place of a search query, sends the completed flow
// or opens the surface it names, and shows the outcome through `PaletteStatus`.
import { useEffect, useId, useMemo, useRef, useState } from "react";
import type { KeyboardEvent } from "react";
import type { RemedyNextAction } from "../../api/types";
import type { JumpTarget } from "../../api/paletteJump";
import type { PaletteMode, PaletteProject, PaletteRow } from "../../api/paletteSheet";
import {
  buildPaletteRows,
  movePaletteCursor,
  readPaletteRecents,
  rememberPaletteRef,
  writePaletteRecents,
} from "../../api/paletteSheet";
import { paletteCommandOf } from "../../api/paletteCommands";
import type { PaletteArgFlow } from "../../api/paletteArgs";
import { answerArg, argFlowComplete, currentArg, startArgFlow } from "../../api/paletteArgs";
import { sendPaletteCommand } from "../../api/paletteSend";
import type { DecisionOutcomeMessage } from "../../api/decisionOutcome";
import { SparkGlyph, ArrowSendGlyph } from "../icons/RemedyGlyphs";
import { PaletteSheet, PaletteStatus, paletteOptionId } from "./PaletteSheet";
import styles from "./CommandBar.module.css";

/** The bar's own placeholder outside a flow — the constant DECISION F044 D4 reworded, pinned by
 *  the placeholder guard, because while a flow is open the placeholder is the asked argument's
 *  prompt instead. */
export const BAR_PLACEHOLDER = 'Ask your agent or jump to anything (e.g., "improve error handling")';

export function CommandBar({
  nextAction,
  targets,
  projects,
  activeSlug,
  jobId,
  serverToken,
  commandReasons,
  focusedTaskId,
  onJump,
  onSwitchProject,
  onOpenTerms,
  onStartTour,
  onOpenSurface,
  onAskChat,
  focusRequest,
}: {
  nextAction: RemedyNextAction;
  targets: readonly JumpTarget[];
  projects: readonly PaletteProject[];
  activeSlug: string;
  jobId: string;
  serverToken: string;
  commandReasons: Readonly<Record<string, string>>;
  focusedTaskId: string;
  onJump: (nodeId: string) => void;
  onSwitchProject: (slug: string) => void;
  onOpenTerms: () => void;
  onStartTour: () => void;
  onOpenSurface: (surface: string, taskNodeId: string) => void;
  onAskChat: (text: string) => void;
  focusRequest: number;
}) {
  // THE STORAGE EDGE, bound here because this is the edge — the file's only `window.localStorage`,
  // built once per mount the way RemedyShell.tsx binds its own digest port.
  const storage = useMemo(() => window.localStorage, []);
  const [recents, setRecents] = useState<readonly string[]>(() => readPaletteRecents(storage));

  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const sectionRef = useRef<HTMLElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const listId = useId();

  // DECISION F044 D5: the keymap's "open-bar" action raises this count once per press; the bar
  // answers by focusing its own input, wherever the press came from.
  useEffect(() => {
    if (focusRequest > 0) inputRef.current?.focus();
  }, [focusRequest]);

  // THE ARGUMENT FLOW (DECISION F044 D3 (3)): `null` outside a command, else the command's own
  // walk through its arguments; and the outcome of the flow's own send or surface, shown by
  // `PaletteStatus` once the sheet itself is closed.
  const [flow, setFlow] = useState<PaletteArgFlow | null>(null);
  const [outcome, setOutcome] = useState<DecisionOutcomeMessage | null>(null);

  const askedArg = flow !== null ? currentArg(flow) : null;
  const paletteMode: PaletteMode = askedArg !== null && askedArg.kind === "task" ? "task" : "all";

  const rows = useMemo<readonly PaletteRow[]>(() => {
    if (askedArg !== null && askedArg.kind === "text") return [];
    return buildPaletteRows({
      query, targets, projects, activeSlug, recents, commandReasons, focusedTaskId, mode: paletteMode,
    });
  }, [query, targets, projects, activeSlug, recents, commandReasons, focusedTaskId, paletteMode, askedArg]);
  const shown = open && rows.length > 0;
  const activeRowId =
    shown && activeIndex >= 0 && activeIndex < rows.length ? paletteOptionId(listId, activeIndex) : undefined;

  async function completeFlow(done: PaletteArgFlow) {
    setFlow(null);
    setQuery("");
    setOpen(false);
    setActiveIndex(-1);
    if (done.entry.flow === "surface") {
      const taskId = done.values["task_id"] ?? "";
      const target = targets.find((t) => t.id === taskId);
      onOpenSurface(done.entry.surface, target ? target.nodeId : "");
      return;
    }
    if (done.entry.flow === "send") {
      const message = await sendPaletteCommand({ jobId, serverToken }, done);
      setOutcome(message);
    }
  }

  function advanceFlow(value: string) {
    if (flow === null) return;
    const next = answerArg(flow, value);
    if (next === null) return;
    setQuery("");
    if (argFlowComplete(next)) {
      void completeFlow(next);
    } else {
      setFlow(next);
    }
  }

  function cancelFlow() {
    setFlow(null);
    setQuery("");
  }

  function startCommandFlow(command: string) {
    const entry = paletteCommandOf(command);
    if (entry === null) return;
    const initial = startArgFlow(entry);
    setQuery("");
    setActiveIndex(0);
    if (argFlowComplete(initial)) {
      setOpen(false);
      void completeFlow(initial);
    } else {
      // THE SHEET STAYS OPEN: a task argument still needs the Jump rows shown, and a text
      // argument's rows are forced empty by the `rows` memo above regardless of `open`.
      setFlow(initial);
      setOpen(true);
    }
  }

  function chooseRow(row: PaletteRow) {
    if (row.disabledReason !== "") return;

    if (row.action.kind === "chat") {
      // THE ASK ROW (DECISION F044 D4 (1)): routed straight to the chat, outside any flow, never
      // remembered.
      setOutcome(null);
      setQuery("");
      setOpen(false);
      setActiveIndex(-1);
      onAskChat(row.action.text);
      return;
    }

    if (flow !== null) {
      if (row.action.kind === "jump") {
        advanceFlow(row.ref.slice("jump:".length));
      }
      return;
    }

    const nextRecents = rememberPaletteRef(recents, row.ref);
    setRecents(nextRecents);
    writePaletteRecents(storage, nextRecents);
    setOutcome(null);

    if (row.action.kind === "command") {
      startCommandFlow(row.action.command);
      return;
    }

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
      if (flow !== null && askedArg !== null && askedArg.kind === "text") {
        advanceFlow(query);
        return;
      }
      if (rows.length === 0) return;
      const row = activeIndex >= 0 && activeIndex < rows.length ? rows[activeIndex] : rows[0];
      chooseRow(row);
    } else if (event.key === "Escape") {
      if (flow !== null) {
        cancelFlow();
      } else {
        setOpen(false);
        setActiveIndex(-1);
        setOutcome(null);
      }
    } else if (event.key === "Backspace") {
      if (flow !== null && query === "") {
        cancelFlow();
      }
    }
  }

  return (
    <section ref={sectionRef} className={styles.commandBar} aria-label="Jump to anything" data-ui="command-bar">
      <div className={styles.spark}><SparkGlyph style={{ width: 16, height: 16 }} /></div>
      {flow !== null && (
        <span className={styles.chip} data-ui="palette-chip">{flow.entry.title}</span>
      )}
      <input
        ref={inputRef}
        aria-label="Jump to a task or file"
        role="combobox"
        aria-expanded={shown}
        aria-controls={listId}
        aria-autocomplete="list"
        aria-activedescendant={activeRowId}
        value={query}
        placeholder={askedArg !== null ? askedArg.prompt : BAR_PLACEHOLDER}
        onChange={e => { setQuery(e.target.value); setOpen(true); setActiveIndex(0); setOutcome(null); }}
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
      {!shown && outcome !== null && (
        <PaletteStatus status={outcome} anchor={sectionRef.current} />
      )}
    </section>
  );
}
