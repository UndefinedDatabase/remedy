// The DRAWING half of F037's rendering core (T5_F037 T002): the rows
// `../../api/diffViewModel` builds, turned into markup against the binding CSS
// this folder's `DiffView.module.css` carries. It DERIVES NOTHING. Which hunks
// start collapsed, what a click does to that set, which rows exist at all and
// how a changed line is cut into marked and unmarked runs are four rules that
// live in `diffViewModel.ts`, because DECISION F031 D5 keeps every decidable
// rule in the layer `apps/ui/vitest.config.ts` reaches — it collects
// `src/**/*.test.ts` in a NODE environment, so a rule written into this file
// would be a rule no suite in this repository can execute. This component owns
// only WHICH element each row becomes, WHERE the collapse set is held, and the
// two numbers no test environment here can produce — the panel's `scrollTop` and
// its `clientHeight`. It READS those two and decides nothing from them:
// `diffRowWindowForViewport` turns them into row indices and spacer pixels, so
// the arithmetic of virtual scrolling stays where vitest executes it.
//
// WHO MOUNTS THIS COMPONENT, so a reader grepping for a caller knows what they
// have found when they find one. The entry point is the `Open diff` button in
// `../detail/DetailPopover.tsx`, which emits `onOpenDiff(taskId)` and sits at
// popover level rather than inside a section, as
// `docs/ui/design_reference/component_spec.md:108` asks.
// `../shell/RemedyShell.tsx` receives that id, holds it as the open task run,
// reads the envelope for it through `loadDiffEnvelope`, and draws THIS
// component inside its diff panel beside `DiffFileSidebar`. Changing the props
// below therefore changes that shell, and the lazy language bundles landed HERE
// rather than at some new caller: the importer constant below is the only place
// in the product that names the highlight module to `loadDiffLanguageBundle`,
// which is what keeps that shell out of F256's wiring entirely.
//
// NOTHING IN THIS REPOSITORY CAN RENDER THIS FILE. There is no DOM environment
// here and the shipped vitest config reaches no markup, so what gates this
// component is `tests/ui_contracts/test_diff_view_render.py`, which reads its
// COMMENT-STRIPPED source together with the stylesheet, exactly as
// `tests/ui_contracts/test_decision_answer_wiring.py` gates the decision inbox,
// and `tsc --noEmit`, which `tests/ui_server/test_dashboard_contract.py` runs.
// A reader changing the wiring below changes that guard with it.
import { Fragment, useEffect, useState } from "react";
import {
  buildDiffRowModels,
  defaultCollapsedHunkIds,
  diffRowWindowForViewport,
  loadDiffLanguageBundle,
  splitLineIntoIntralineSegments,
  toggleHunkCollapse,
} from "../../api/diffViewModel";
import type { DiffEnvelope, DiffLineKind } from "../../api/diffViewModel";
import { composeHighlightedRuns } from "../../api/diffHighlight";
import type { DiffHighlightTokenKind } from "../../api/diffHighlight";
import styles from "./DiffView.module.css";

/** HOW THE HIGHLIGHT BUNDLE IS ASKED FOR, and it is a CALL EXPRESSION rather
 *  than a static import on purpose: DECISION F256 D1 rules that a language's
 *  tokenizer is fetched lazily, as its own chunk, instead of riding in the main
 *  chunk for every operator who never opens a diff. `loadDiffLanguageBundle`
 *  takes this function rather than naming a module itself — the model module
 *  imports nothing at runtime, which is what keeps every rule in it decidable —
 *  so THIS file is the one place in the product that names the highlight module
 *  to the loader, and it is the reason the wiring lives here rather than in
 *  `../shell/RemedyShell.tsx`.
 *
 *  IT IS NEVER INVOKED FOR A PATH THAT RENDERS PLAIN. That is the acceptance
 *  property `loadDiffLanguageBundle` owns and its vitest suite pins at a call
 *  count of exactly zero, and passing the importer instead of calling it is what
 *  lets that function decide: the language is resolved from the path first, and
 *  a plain answer never reaches this line. */
const DIFF_HIGHLIGHT_BUNDLE_IMPORTER = () => import("../../api/diffHighlight");

/** The tint a line's kind gives its row, as a `Record` lookup rather than a
 *  branch: the binding CSS composes `.diffLine.add` and `.diffLine.del` from two
 *  classes, so both must ride on the element together. `ctx` takes the empty
 *  string because an unchanged line wears the row class alone — there is no
 *  `.ctx` rule in the stylesheet and this component may not invent one. */
const DIFF_LINE_KIND_CLASS: Record<DiffLineKind, string> = {
  ctx: "",
  add: styles.add,
  del: styles.del,
};

/** The colour a RUN's token kind gives it, ruled by DECISION F256 D2 and carried
 *  as a `Record` for the same reason `DIFF_LINE_KIND_CLASS` above is one: the
 *  lookup is total over the closed kind set, so a kind added to
 *  `../../api/diffHighlight` without a class here becomes a type error rather
 *  than a run that silently renders untinted.
 *
 *  `plain` TAKES THE EMPTY STRING, exactly as `ctx` does above and for the same
 *  reason: an unhighlighted run wears no extra class, there is no `.tokPlain`
 *  rule in the stylesheet, and this component may not invent one. That single
 *  mapping is what makes an unknown language — and the moment before a known
 *  language's answer arrives — render byte for byte as this viewer rendered it
 *  before F256. */
const DIFF_HIGHLIGHT_KIND_CLASS: Record<DiffHighlightTokenKind, string> = {
  comment: styles.tokComment,
  string: styles.tokString,
  number: styles.tokNumber,
  keyword: styles.tokKeyword,
  plain: "",
};

/** What a COLLAPSED hunk head says after its header. The colon form is used
 *  because it stays grammatical at every count and so needs no plural branch in
 *  markup no rendering test reaches. The number beside it is the row's own
 *  `hiddenLineCount`, never a length this file recomputes. */
const HUNK_HIDDEN_LINES_LABEL = "Hidden lines";

/** WHY A DIFF CAN END EARLY, said on screen rather than left for the operator to
 *  infer from a diff that simply stops. `truncated` is the one flag DECISION
 *  F037 D5, D6 and D7 all feed — the parsed-body ceiling, the file ceiling and
 *  the artifact-byte ceiling — and a viewer that silently shows part of a change
 *  is the exact failure those three ceilings exist to avoid. */
const TRUNCATED_NOTICE =
  "This diff is shown as a PREFIX. The artifact was larger than the viewer's " +
  "ceilings, so files, hunk lines or bytes beyond them were never parsed and " +
  "are not on this screen (DECISION F037 D5, D6 and D7).";

/** THE ONE PIECE OF PRESENTATION THE BINDING CSS DOES NOT COVER, and it is not a
 *  new visual language. The binding CSS block of
 *  `docs/roadmap/features/T5_F037.md` styles the ROWS of a diff and says nothing
 *  about the box they scroll inside; the stylesheet beside this file transcribes
 *  that block and defines exactly six classes, so asking it for a seventh is what
 *  the CANONICAL DESIGN REFERENCE banner forbids. Virtual scrolling is
 *  meaningless without a bounded, scrolling container — a panel that grows to fit
 *  its content never scrolls, so `scrollTop` stays 0 and the window never moves —
 *  and these two declarations are the minimum that gives it one. The height is in
 *  VIEWPORT UNITS rather than pixels so the panel keeps its proportion on every
 *  screen without this file learning anything about layout. */
const DIFF_VIEW_SCROLL_STYLE = { overflowY: "auto", maxHeight: "70vh" } as const;

export interface DiffViewProps {
  /** An ALREADY-READ envelope. `readDiffEnvelope` is the single door a payload
   *  comes through and the round that fetches calls it, so this component is
   *  never the second place a malformed payload is handled: every field below is
   *  a value that door already made total. */
  envelope: DiffEnvelope;
}

export function DiffView({ envelope }: DiffViewProps) {
  // WHICH hunks are closed, and nothing else about them. The lazy initialiser
  // form is used because `defaultCollapsedHunkIds` walks the whole envelope, and
  // the eager form would re-walk it on every render only to throw the answer
  // away.
  const [collapsed, setCollapsed] = useState<ReadonlySet<string>>(
    () => defaultCollapsedHunkIds(envelope),
  );

  // A NEW ENVELOPE STARTS A NEW COLLAPSE SET. A viewer switched from one task
  // run to another must not keep the previous diff's set: its hunk ids mean
  // nothing in the new envelope, so a stale membership would close a hunk that
  // merely inherited an id and leave the genuinely huge ones open.
  useEffect(() => {
    setCollapsed(defaultCollapsedHunkIds(envelope));
  }, [envelope]);

  // WHICH LANGUAGE EACH FILE IS HIGHLIGHTED AS, keyed by the file's own path and
  // holding the model's answer verbatim: a language id, or `null` meaning "render
  // this file plain". A `Map` rather than an object literal because the keys are
  // diff paths from a repository this viewer does not control, and a lookup over
  // an inherited key is the defect finding `R-0731` recorded in the model module.
  // A path that is not a key yet is the honest reading of an answer that has not
  // arrived, and it renders plain until it does.
  const [languageByPath, setLanguageByPath] = useState<ReadonlyMap<string, string | null>>(
    () => new Map<string, string | null>(),
  );

  // A NEW ENVELOPE STARTS A NEW MAP, for the reason the collapse set above is
  // reset on a new envelope: the keys are the previous diff's paths, and a stale
  // entry would colour one task run's file as another task run's language.
  //
  // ONE ASK PER DISTINCT PATH, and the answer is stored rather than the bundle —
  // `loadDiffLanguageBundle` caches the import itself, one per language, so this
  // effect never needs to know whether a chunk is already in flight. `cancelled`
  // is the answer to a reply that comes back AFTER the envelope moved on: React
  // runs the cleanup before the next effect, so a slow import finds the flag set
  // and stores nothing, which is the shape `../shell/RemedyShell.tsx` uses for
  // its own read.
  useEffect(() => {
    let cancelled = false;
    setLanguageByPath(new Map<string, string | null>());
    for (const path of Array.from(new Set(envelope.files.map((file) => file.path)))) {
      void loadDiffLanguageBundle(path, DIFF_HIGHLIGHT_BUNDLE_IMPORTER).then((answer) => {
        if (!cancelled) {
          setLanguageByPath((current) => new Map(current).set(path, answer.language));
        }
      });
    }
    return () => { cancelled = true; };
  }, [envelope]);

  // THE TWO NUMBERS ONLY THE DOM CAN SUPPLY, held together because they are
  // read together and are meaningless apart: a scroll offset without the height
  // it was measured against names no range of rows. Both start at 0, which is
  // the honest reading of a panel that has not been rendered yet — and
  // `DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS` in the model is what stops that zero
  // from drawing an empty viewer forever.
  const [viewport, setViewport] = useState({ scrollTopPx: 0, clientHeightPx: 0 });

  // ONE WALK, and the row list is the only thing this render reads. Collapse is
  // an ARGUMENT to it rather than a filter applied afterwards, which is what
  // keeps the hidden-line counts and the row keys the model's answer instead of
  // this file's.
  const rows = buildDiffRowModels(envelope, collapsed);

  // ASK THE MODEL, RENDER THE ANSWER. Every index and every pixel below comes
  // out of this one call: which rows to draw, and how tall the two spacers that
  // stand in for the rest must be. This file performs no division, no
  // multiplication and no comparison against a row count, because any of the
  // three would be a rule `apps/ui/vitest.config.ts` could never execute.
  const rowWindow = diffRowWindowForViewport(
    rows.length,
    viewport.scrollTopPx,
    viewport.clientHeightPx,
  );
  const drawnRows = rows.slice(rowWindow.startIndex, rowWindow.endIndex);

  return (
    // NO CLASS ON THE WRAPPER. The stylesheet is a transcription of the feature
    // file's binding CSS and defines exactly six classes; inventing a seventh
    // here would be the visual language the CANONICAL DESIGN REFERENCE banner
    // forbids, so the container is a bare landmark and every styled element
    // below wears a class the sheet really carries.
    <section
      data-ui="diff-view"
      style={DIFF_VIEW_SCROLL_STYLE}
      // THE WHOLE OF THE UNTESTABLE DOM MEASUREMENT, in one expression that
      // decides nothing: it reads two numbers off the element that just
      // scrolled and stores them. Everything derived from them is the model's.
      onScroll={(event) => setViewport({
        scrollTopPx: event.currentTarget.scrollTop,
        clientHeightPx: event.currentTarget.clientHeight,
      })}
    >
      {/* THE SPACERS, and why they carry no class. They stand in for the rows
          that are not in the DOM, so the scrollbar keeps describing the WHOLE
          document rather than the window: without them a ten-thousand-row diff
          would scroll as if it were fifty rows long. Their height is the
          model's answer in pixels, and they wear an inline style because the
          binding CSS defines no class for a spacer and this component may not
          invent one. When the list is short enough to draw whole there is
          nothing to stand in for, so neither is rendered. */}
      {rowWindow.virtualized
        ? <div style={{ height: `${rowWindow.rowsBeforePx}px` }} />
        : null}
      {drawnRows.map((row) => {
        if (row.kind === "file") {
          return (
            // TWO DIFFERENT THINGS WEARING THE SAME STRING, DELIBERATELY. `key`
            // is React's reconciliation handle and never reaches the DOM, so a
            // sidebar entry has nothing to move to while it is the only one
            // here; `id` is the DOM anchor `DiffFileSidebar.tsx` looks up. The
            // string is the model's — `buildDiffFileSummaries` puts the SAME
            // value in each summary's `rowKey` — which is what lets the two
            // halves agree without either of them recomputing it.
            <div key={row.key} id={row.key}>
              <strong>{row.file.path}</strong>
              <span>{row.file.status}</span>
              <span>{`+${row.file.stats.added}`}</span>
              <span>{`-${row.file.stats.deleted}`}</span>
              {/* A file's note is prose the parser wrote — a binary marker, a
                  mode change, a rename — and it is absent far more often than
                  it is present, so it renders only when there is one. */}
              {row.file.note === null ? null : <p>{row.file.note}</p>}
            </div>
          );
        }
        if (row.kind === "hunkHead") {
          return (
            // A BUTTON, NOT A DIV. The head is the control that opens and closes
            // its hunk, and a div carries no keyboard affordance at all; the
            // explicit type stops it submitting a form it may one day sit in.
            // `aria-expanded` is the state itself rather than a second copy of
            // it — the row says whether it is collapsed, and this is that answer
            // inverted, because the attribute describes what the button REVEALS.
            <button
              key={row.key}
              type="button"
              className={styles.hunkHead}
              aria-expanded={!row.collapsed}
              onClick={() => setCollapsed((current) => toggleHunkCollapse(current, row.hunkId))}
            >
              {row.header}
              {row.collapsed ? ` · ${HUNK_HIDDEN_LINES_LABEL}: ${row.hiddenLineCount}` : ""}
            </button>
          );
        }
        // THE LANGUAGE THIS ROW IS COLOURED AS, looked up by the path of the file
        // the row belongs to. `null` covers both "this file renders plain" and
        // "its answer has not arrived", which are the same thing on screen: the
        // token cut then makes the whole line `plain` and every run wears no
        // class, so the row's markup is what it was before F256.
        const rowLanguage = languageByPath.get(envelope.files[row.fileIndex].path) ?? null;
        return (
          <div
            key={row.key}
            className={`${styles.diffLine} ${DIFF_LINE_KIND_CLASS[row.line.kind]}`.trim()}
          >
            {/* The two gutters of the binding grid. Each is BLANK rather than
                zero when its side has no number: an added line has no old line
                number and a deleted one has no new one, and a 0 in that column
                would be a position that does not exist. */}
            <span className={styles.ln}>{row.line.oldLn === null ? "" : row.line.oldLn}</span>
            <span className={styles.ln}>{row.line.newLn === null ? "" : row.line.newLn}</span>
            <span>
              {/* THE INTRALINE MARK AND THE SYNTAX COLOUR, COMPOSED — DECISION
                  F037 D9 with amendment A5 for the first and DECISION F256 D1
                  and D2 for the second. BOTH CUTS ARE THE MODEL'S: this file
                  decides neither which characters are marked nor which are
                  keywords. `composeHighlightedRuns` is what turns the two into
                  ONE list of runs uniform in both dimensions, so each run below
                  becomes exactly one element and no character is drawn twice
                  however the two cuts interleave. The intraline behaviour is
                  UNCHANGED by this composition — a marked run is still a `mark`
                  wearing `styles.intraline`, and colour is added to it rather
                  than substituted for it. The runs of ONE line are positional
                  and derived, so their index is the honest key among these
                  siblings; the ROW keys, the ones that must survive a collapse,
                  are the model's own and are used above and nowhere else. */}
              {composeHighlightedRuns(
                splitLineIntoIntralineSegments(row.line),
                rowLanguage,
              ).map((run, runIndex) => {
                const kindClass = DIFF_HIGHLIGHT_KIND_CLASS[run.kind];
                if (run.marked) {
                  return (
                    <mark
                      key={runIndex}
                      className={`${styles.intraline} ${kindClass}`.trim()}
                    >{run.text}</mark>
                  );
                }
                if (kindClass === "") {
                  return <Fragment key={runIndex}>{run.text}</Fragment>;
                }
                return <span key={runIndex} className={kindClass}>{run.text}</span>;
              })}
            </span>
          </div>
        );
      })}
      {rowWindow.virtualized
        ? <div style={{ height: `${rowWindow.rowsAfterPx}px` }} />
        : null}
      {/* OUTSIDE THE WINDOW, DELIBERATELY. The notice belongs to the ENVELOPE
          and not to any row, so it renders after the rows and after the trailing
          spacer; drawing it inside the window would let virtualization scroll
          the one warning that a diff is incomplete out of existence. */}
      {envelope.truncated ? <p>{TRUNCATED_NOTICE}</p> : null}
    </section>
  );
}
