// The PURE half of F037's rendering core (T5_F037 T002): the diff endpoint's
// envelope turned into the flat list of rows a renderer draws. It holds no
// markup, issues no fetch and touches no stylesheet, so every rule below is
// decidable from plain data alone.
//
// DECISION F031 D5 is why the rule lives HERE rather than inside the component
// that will draw it: the shipped `apps/ui/vitest.config.ts` collects
// `src/**/*.test.ts` in a NODE environment and reaches no markup at all, so a
// collapse rule or a row key written into a `.tsx` file is a rule no gate in
// this repository can execute. DECISION F037 D8 records the same reasoning for
// this feature specifically, and `tests/ui_contracts/test_diff_view_model.py`
// pins the structural half vitest cannot see about itself. The segments
// `splitLineIntoIntralineSegments` returns at the foot of this file are what
// `DiffView.tsx` wraps in the intraline mark, and DECISION F037 D9 rules what
// that mark looks like — this module chooses no colour and names no class.
//
// Remedy deliberately does NOT re-sort files or hunks here. A reader looking
// for a comparator over paths, over change size or over status will not find
// one, and its absence is a choice: the server's order IS the reading order.
// `packages/orchestration/diff_parser.py` preserves the input order of the
// unified diff on purpose, and a second ordering applied on the client would
// silently disagree with every other surface that shows the same artifact.

/** The three line kinds `diff_parser.py` emits (`DIFF_LINE_CONTEXT`,
 *  `DIFF_LINE_ADDED`, `DIFF_LINE_DELETED`). Anything else on the wire is not a
 *  fourth kind to render — it is a payload this module does not trust. */
export type DiffLineKind = "ctx" | "add" | "del";

/** One intraline span as the parser sends it: `[startOffset, length]` in
 *  characters of that line's own `content`. */
export type DiffIntralineSpan = [number, number];

/** One rendered line of a hunk. `oldLn` is null on an added line and `newLn` is
 *  null on a deleted one, which is what the two gutter columns of the binding
 *  CSS render as blank. */
export interface DiffLine {
  kind: DiffLineKind;
  oldLn: number | null;
  newLn: number | null;
  content: string;
  intraline: DiffIntralineSpan[];
}

/** One hunk. `header` is the `@@ ... @@` line VERBATIM, section heading
 *  included, because the viewer renders it rather than rebuilding it. */
export interface DiffHunk {
  id: string;
  header: string;
  oldStart: number;
  newStart: number;
  lines: DiffLine[];
}

/** A file's `stats {+,-}` counters, as the two named integers the parser's own
 *  contract notes spell out. */
export interface DiffFileStats {
  added: number;
  deleted: number;
}

/** One file of the diff. `oldPath` is non-null only for a rename, and `hunks`
 *  is legitimately empty for a binary marker, a mode change or a pure rename. */
export interface DiffFile {
  path: string;
  oldPath: string | null;
  status: string;
  stats: DiffFileStats;
  note: string | null;
  hunks: DiffHunk[];
}

/** The whole read-endpoint payload. `available` false with an empty `files` is
 *  the shape an absent artifact arrives as, and `reason` names which absence. */
export interface DiffEnvelope {
  version: number;
  scope: string;
  taskId: string;
  source: string | null;
  available: boolean;
  reason: string | null;
  truncated: boolean;
  files: DiffFile[];
  taskRunIds: string[];
}

/** A file's own row: the sidebar and the body agree on this row's `key`. */
export interface DiffFileRow {
  kind: "file";
  key: string;
  fileIndex: number;
  file: DiffFile;
}

/** A hunk's head row. `hiddenLineCount` is how many line rows this head is
 *  standing in for, so the renderer can label a collapsed hunk without walking
 *  the hunk a second time. It is 0 while the hunk is open. */
export interface DiffHunkHeadRow {
  kind: "hunkHead";
  key: string;
  fileIndex: number;
  hunkId: string;
  header: string;
  collapsed: boolean;
  hiddenLineCount: number;
}

/** One line row of an OPEN hunk. A collapsed hunk emits none of these. */
export interface DiffLineRow {
  kind: "line";
  key: string;
  fileIndex: number;
  hunkId: string;
  line: DiffLine;
}

/** The flat row list the renderer walks, discriminated by `kind`. */
export type DiffRowModel = DiffFileRow | DiffHunkHeadRow | DiffLineRow;

/** One entry of the file sidebar T003 renders. `rowKey` is the `key` of that
 *  file's own `DiffFileRow`, so a sidebar click can scroll to its row without
 *  recomputing the row list. */
export interface DiffFileSummary {
  path: string;
  oldPath: string | null;
  status: string;
  added: number;
  deleted: number;
  hunkCount: number;
  note: string | null;
  rowKey: string;
}

const DIFF_LINE_KINDS: readonly string[] = ["ctx", "add", "del"];

/** A plain JSON object, or null for anything that is not one. Arrays are NOT
 *  records here: `raw.files[0]` being an array must fail the same way a string
 *  does rather than reading every field as undefined. */
function asRecord(value: unknown): Record<string, unknown> | null {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    return null;
  }
  return value as Record<string, unknown>;
}

/** The camelCase field if the payload carries it, else the snake_case one. The
 *  wire form is snake_case and this module's form is camelCase; reading both is
 *  what `remedyApi.ts` already does for every other endpoint, and it is the
 *  reason `readDiffEnvelope` exists at all rather than a cast. */
function pick(source: Record<string, unknown>, camel: string, snake: string): unknown {
  return source[camel] !== undefined ? source[camel] : source[snake];
}

function asString(value: unknown): string {
  return typeof value === "string" ? value : "";
}

function asNullableString(value: unknown): string | null {
  return typeof value === "string" ? value : null;
}

/** A whole number, or 0. A non-finite or non-numeric line number is not a
 *  position to scroll to, and NaN leaking into a gutter renders as "NaN". */
function asInt(value: unknown): number {
  return typeof value === "number" && Number.isFinite(value) ? Math.trunc(value) : 0;
}

/** A whole number, or null — the parser's own answer for "this line has no
 *  number on this side", which the gutter renders as blank. */
function asNullableInt(value: unknown): number | null {
  return typeof value === "number" && Number.isFinite(value) ? Math.trunc(value) : null;
}

function asStringArray(value: unknown): string[] {
  if (!Array.isArray(value)) {
    return [];
  }
  return value.filter((entry): entry is string => typeof entry === "string");
}

/** Intraline spans, dropping any entry that is not a `[start, length]` pair of
 *  finite numbers. A malformed span would be rendered as a highlight over
 *  arbitrary characters, which is worse than no highlight at all. */
function readIntralineSpans(value: unknown): DiffIntralineSpan[] {
  if (!Array.isArray(value)) {
    return [];
  }
  const spans: DiffIntralineSpan[] = [];
  for (const entry of value) {
    if (!Array.isArray(entry) || entry.length < 2) {
      continue;
    }
    const start = entry[0];
    const length = entry[1];
    if (typeof start !== "number" || typeof length !== "number") {
      continue;
    }
    if (!Number.isFinite(start) || !Number.isFinite(length)) {
      continue;
    }
    spans.push([Math.trunc(start), Math.trunc(length)]);
  }
  return spans;
}

/** One line, or null when this module refuses to render it. A `kind` outside
 *  the three the contract names is DROPPED rather than rendered as something:
 *  guessing "ctx" would show an unknown line as unchanged, which is a lie about
 *  the diff, and guessing "add" would invent a change that is not there. */
function readDiffLine(value: unknown): DiffLine | null {
  const raw = asRecord(value);
  if (raw === null) {
    return null;
  }
  const kind = asString(raw.kind);
  if (!DIFF_LINE_KINDS.includes(kind)) {
    return null;
  }
  return {
    kind: kind as DiffLineKind,
    oldLn: asNullableInt(pick(raw, "oldLn", "old_ln")),
    newLn: asNullableInt(pick(raw, "newLn", "new_ln")),
    content: asString(raw.content),
    intraline: readIntralineSpans(raw.intraline),
  };
}

/** One hunk, with the id the parser assigned. A hunk whose `id` is absent or
 *  not a string is given the `"<fileIndex>:<hunkIndex>"` the parser would have
 *  assigned, because every row key below is derived from it and a blank id
 *  would collapse two hunks onto one key. */
function readDiffHunk(value: unknown, fileIndex: number, hunkIndex: number): DiffHunk {
  const raw = asRecord(value) ?? {};
  const rawId = asString(raw.id);
  const lines: DiffLine[] = [];
  const rawLines = Array.isArray(raw.lines) ? raw.lines : [];
  for (const entry of rawLines) {
    const line = readDiffLine(entry);
    if (line !== null) {
      lines.push(line);
    }
  }
  return {
    id: rawId !== "" ? rawId : `${fileIndex}:${hunkIndex}`,
    header: asString(raw.header),
    oldStart: asInt(pick(raw, "oldStart", "old_start")),
    newStart: asInt(pick(raw, "newStart", "new_start")),
    lines,
  };
}

function readDiffFile(value: unknown, fileIndex: number): DiffFile {
  const raw = asRecord(value) ?? {};
  const stats = asRecord(raw.stats) ?? {};
  const rawHunks = Array.isArray(raw.hunks) ? raw.hunks : [];
  return {
    path: asString(raw.path),
    oldPath: asNullableString(pick(raw, "oldPath", "old_path")),
    status: asString(raw.status),
    stats: { added: asInt(stats.added), deleted: asInt(stats.deleted) },
    note: asNullableString(raw.note),
    hunks: rawHunks.map((entry, hunkIndex) => readDiffHunk(entry, fileIndex, hunkIndex)),
  };
}

/** The envelope an absent artifact arrives as, and the single answer this
 *  module gives to any payload it cannot trust. */
function unavailableDiffEnvelope(): DiffEnvelope {
  return {
    version: 0,
    scope: "",
    taskId: "",
    source: null,
    available: false,
    reason: null,
    truncated: false,
    files: [],
    taskRunIds: [],
  };
}

/** The endpoint's payload as this module's camelCase envelope. TOTAL: no input
 *  makes this throw, and anything it cannot trust becomes exactly the answer an
 *  absent artifact gives — `available` false with `files` empty.
 *
 *  THIS IS WHERE A MALFORMED PAYLOAD STOPS. Every function below reads a
 *  `DiffEnvelope` this function built, so none of them has to be defensive a
 *  second time: a string where an object belonged, a `files` that is not an
 *  array, a line whose `kind` is not one of the three the contract names — all
 *  of it is resolved here, once, and never again downstream. */
export function readDiffEnvelope(raw: unknown): DiffEnvelope {
  const source = asRecord(raw);
  if (source === null) {
    return unavailableDiffEnvelope();
  }
  const rawFiles = source.files;
  const files = Array.isArray(rawFiles)
    ? rawFiles.map((entry, fileIndex) => readDiffFile(entry, fileIndex))
    : [];
  return {
    version: asInt(source.version),
    scope: asString(source.scope),
    taskId: asString(pick(source, "taskId", "task_id")),
    source: asNullableString(source.source),
    // `available` is true only when the wire says so AND the payload really
    // carried a file list: an `available` true beside a broken `files` is the
    // one combination that would put an empty viewer behind a "loaded" label.
    available: source.available === true && Array.isArray(rawFiles),
    reason: asNullableString(source.reason),
    // Only a literal `true` truncates. A truthy string or a 1 is a payload this
    // module does not understand, and warning about lost lines that are not
    // lost teaches an operator to ignore the warning.
    truncated: source.truncated === true,
    files,
    taskRunIds: asStringArray(pick(source, "taskRunIds", "task_run_ids")),
  };
}

/** A hunk carrying MORE lines than this is collapsed when the view first
 *  opens. WHY THIS NUMBER, which the feature file's "collapsed by default
 *  beyond a size threshold" does not give: the binding CSS sets `.diffLine` at
 *  `font: 12.5px/1.6`, so one rendered line is twenty pixels tall and two
 *  hundred of them is roughly four thousand pixels — several screens of a
 *  SINGLE hunk. That is the point at which an open hunk stops being a reading
 *  aid and becomes a wall to scroll past on the way to the next file.
 *
 *  Declared once, here. Every other site — `defaultCollapsedHunkIds`, the
 *  component that will render these rows, and both test files — names this
 *  constant rather than repeating the number, which is what stops the rule and
 *  its tests from drifting apart. */
export const DIFF_HUNK_COLLAPSE_THRESHOLD_LINES = 200;

/** The hunks that start collapsed: those carrying strictly MORE than
 *  `DIFF_HUNK_COLLAPSE_THRESHOLD_LINES` lines. A hunk of EXACTLY the threshold
 *  stays OPEN — the boundary is inclusive, the same way `DIFF_VIEW_MAX_FILES`
 *  and `DIFF_VIEW_MAX_BODY_LINES` are inclusive in `diff_parser.py`, so a
 *  reader who knows one of the three ceilings knows all of them. */
export function defaultCollapsedHunkIds(envelope: DiffEnvelope): Set<string> {
  const collapsed = new Set<string>();
  for (const file of envelope.files) {
    for (const hunk of file.hunks) {
      if (hunk.lines.length > DIFF_HUNK_COLLAPSE_THRESHOLD_LINES) {
        collapsed.add(hunk.id);
      }
    }
  }
  return collapsed;
}

/** One hunk's collapse state flipped, as a NEW set. This never mutates the set
 *  it is given, for the reason `orderDecisionInbox` gives for not sorting in
 *  place: the caller's set is React state, and a mutation that leaves the
 *  identity unchanged is a re-render that silently does not happen. */
export function toggleHunkCollapse(collapsed: ReadonlySet<string>, hunkId: string): Set<string> {
  const next = new Set<string>(collapsed);
  if (next.has(hunkId)) {
    next.delete(hunkId);
  } else {
    next.add(hunkId);
  }
  return next;
}

/** The rows a renderer draws, as ONE flat array in the envelope's own order.
 *
 *  KEYS. Every row carries a `key` that is unique across the whole array and
 *  STABLE under collapse — collapsing a hunk removes line rows but renumbers
 *  nothing, so React reuses the rows that did not change. The hunk-derived keys
 *  are built from the server's own hunk `id`, which `diff_parser.py` assigns as
 *  `"<fileIndex>:<hunkIndex>"`, both zero-based and unique within one parse.
 *  Those ids are PROVISIONAL: F033 replaces them with content-hash ids so a row
 *  survives a re-parse of a changed diff, and the envelope's `version` field is
 *  the seam through which that lands. Nothing here depends on the id's SHAPE,
 *  only on the server assigning distinct ones.
 *
 *  A COLLAPSED hunk emits its head row and none of its line rows, and the head
 *  says how many lines it is hiding so the renderer can label it in one pass.
 *  A file with NO hunks — a binary marker, a mode change, a pure rename — still
 *  emits its file row, because the sidebar and the body must agree on which
 *  files exist. */
export function buildDiffRowModels(
  envelope: DiffEnvelope,
  collapsed: ReadonlySet<string>,
): DiffRowModel[] {
  const rows: DiffRowModel[] = [];
  envelope.files.forEach((file, fileIndex) => {
    rows.push({ kind: "file", key: `file:${fileIndex}`, fileIndex, file });
    for (const hunk of file.hunks) {
      const isCollapsed = collapsed.has(hunk.id);
      rows.push({
        kind: "hunkHead",
        key: `hunk:${hunk.id}`,
        fileIndex,
        hunkId: hunk.id,
        header: hunk.header,
        collapsed: isCollapsed,
        hiddenLineCount: isCollapsed ? hunk.lines.length : 0,
      });
      if (isCollapsed) {
        continue;
      }
      hunk.lines.forEach((line, lineIndex) => {
        rows.push({
          kind: "line",
          key: `line:${hunk.id}:${lineIndex}`,
          fileIndex,
          hunkId: hunk.id,
          line,
        });
      });
    }
  });
  return rows;
}

/** The file sidebar T003 renders, one entry per file in the envelope's order.
 *  It is built here rather than in the component because every value in it is
 *  decidable from the envelope alone and therefore testable; the component's
 *  job is to draw this list, not to derive it.
 *
 *  `rowKey` matches the `key` `buildDiffRowModels` gives that same file's row,
 *  which is what lets a sidebar click find its row without recomputing the row
 *  list or searching it by path. */
export function buildDiffFileSummaries(envelope: DiffEnvelope): DiffFileSummary[] {
  return envelope.files.map((file, fileIndex) => ({
    path: file.path,
    oldPath: file.oldPath,
    status: file.status,
    added: file.stats.added,
    deleted: file.stats.deleted,
    hunkCount: file.hunks.length,
    note: file.note,
    rowKey: `file:${fileIndex}`,
  }));
}

/** One consecutive run of a line's own `content`, and whether the intraline
 *  spans cover it. `marked` is the only thing this type says about appearance:
 *  the emphasis itself is two CSS rules DECISION F037 D9 rules and
 *  `DiffView.module.css` carries. */
export interface DiffLineSegment {
  text: string;
  marked: boolean;
}

/** One line's `content` cut into consecutive segments, the marked ones covering
 *  EXACTLY the characters the line's `intraline` spans cover.
 *
 *  WHY THIS IS HERE AND NOT IN THE COMPONENT: it is the last decidable rule of
 *  the rendering core, and DECISION F031 D5 keeps decidable rules in the layer
 *  the node-environment vitest config reaches. A `.tsx` file computing this
 *  would be arithmetic no suite in this repository can execute.
 *
 *  TOTAL, and the arithmetic is the whole of its difficulty. `readIntralineSpans`
 *  above checked only the SHAPE of each span — a pair of finite numbers — and
 *  nothing upstream has checked what those numbers MEAN against this particular
 *  content. So every hostile case is resolved here, once:
 *
 *  * a span starting at or past the end of the content is DROPPED;
 *  * a span running past the end is CLAMPED to it;
 *  * a zero-length or negative-length span is DROPPED;
 *  * a span reaching back before offset zero is CLAMPED to zero, which is the
 *    same reading as the clamp at the other end;
 *  * OVERLAPPING and OUT-OF-ORDER spans are resolved by marking the UNION of
 *    the characters they cover.
 *
 *  A COVERAGE MAP is what makes that union free rather than a merge routine to
 *  get wrong: each span paints its own characters, the runs are read off
 *  afterwards, and no character can be emitted twice or dropped whatever the
 *  spans overlap. The invariant a caller may rely on, and which the vitest suite
 *  pins for every case above: the concatenation of every segment's `text` equals
 *  `content` exactly. An empty `intraline` therefore yields ONE unmarked
 *  segment, and an empty `content` yields the EMPTY ARRAY — there is no run to
 *  describe, and a segment carrying the empty string would render a `mark`
 *  element around nothing. */
export function splitLineIntoIntralineSegments(line: DiffLine): DiffLineSegment[] {
  const content = line.content;
  if (content.length === 0) {
    return [];
  }
  const covered: boolean[] = new Array<boolean>(content.length).fill(false);
  for (const [start, length] of line.intraline) {
    if (length <= 0 || start >= content.length) {
      continue;
    }
    const from = start < 0 ? 0 : start;
    const until = Math.min(content.length, start + length);
    for (let index = from; index < until; index += 1) {
      covered[index] = true;
    }
  }
  const segments: DiffLineSegment[] = [];
  let runStart = 0;
  for (let index = 1; index <= content.length; index += 1) {
    if (index === content.length || covered[index] !== covered[runStart]) {
      segments.push({ text: content.slice(runStart, index), marked: covered[runStart] });
      runStart = index;
    }
  }
  return segments;
}

/** The ROW count beyond which the viewer virtualizes — draws a window of rows
 *  instead of the whole list. WHY THIS NUMBER: the Design section of
 *  `docs/roadmap/features/T5_F037.md` names "virtual scrolling >2k lines", and
 *  this constant is that sentence made executable. It counts ROWS and not diff
 *  lines, which is the more useful of the two readings here: a collapsed hunk
 *  contributes ONE head row in place of the hundreds of lines it hides, and it
 *  is rows in the document that cost a browser anything.
 *
 *  Declared once, here, exactly as `DIFF_HUNK_COLLAPSE_THRESHOLD_LINES` above
 *  is. Every other site — the function below, the component that will consume
 *  it, and the vitest suite — names this constant rather than repeating the
 *  digits, which is what keeps the rule and its own tests from drifting apart. */
export const DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS = 2000;

/** WHICH rows a virtualized viewer draws, and how many lie on either side.
 *
 *  `startIndex` is INCLUSIVE and `endIndex` EXCLUSIVE — the half-open form
 *  `Array.prototype.slice` already takes — so a caller draws its window with
 *  `rows.slice(startIndex, endIndex)` and does no arithmetic of its own.
 *  `rowsBefore` and `rowsAfter` are what the two spacer elements of a
 *  virtualized list are sized from, and `virtualized` is false when the list is
 *  short enough to draw whole, so a caller can skip the spacers entirely. */
export interface DiffRowWindow {
  virtualized: boolean;
  startIndex: number;
  endIndex: number;
  rowsBefore: number;
  rowsInWindow: number;
  rowsAfter: number;
}

/** A whole count of at least zero: the single reading this module gives any
 *  number a viewport hands it. NOTHING UPSTREAM CHECKS THESE VALUES — they come
 *  from a scroll offset divided by an element height — so a NaN, an infinity, a
 *  fraction or a negative is resolved HERE rather than becoming a slice bound
 *  that quietly returns the wrong rows. A non-finite number becomes 0 because
 *  it names no position in any list, and 0 is the one position every list has. */
function wholeRowCount(value: number): number {
  if (!Number.isFinite(value)) {
    return 0;
  }
  const whole = Math.trunc(value);
  return whole > 0 ? whole : 0;
}

/** The window a virtualized diff viewer draws, from the row COUNT and the
 *  viewport alone. TOTAL: no input makes this throw, and every answer satisfies
 *  the invariant below.
 *
 *  IT DERIVES FROM COUNTS, NEVER FROM PIXELS. This module is pure data in, pure
 *  data out and imports nothing, so a measurement of the DOM cannot reach it —
 *  the caller does the one division it owns (scroll offset by row height) and
 *  hands the result here as a row index. That division is the only untestable
 *  part of virtual scrolling, and keeping it out of this function is what puts
 *  the rest in the layer `apps/ui/vitest.config.ts` reaches (DECISION F031 D5).
 *
 *  THE RULES:
 *  * at or below `DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS` the list is NOT
 *    virtualized — the window is every row and both sides are empty, so a small
 *    diff pays none of virtualization's cost;
 *  * above it, the window is the visible range widened by `overscanRows` at
 *    BOTH ends and clamped to the list, because a row scrolled into view before
 *    it is drawn is a blank stripe the operator sees;
 *  * a visible count of zero or less yields an EMPTY window wherever the
 *    viewport sits — there is no visible range for the overscan to widen, and
 *    inventing rows around nothing would draw a viewport that does not exist;
 *  * an index past the end is CLAMPED to the end rather than refused, which
 *    reads as "you are past the last row" and is the honest answer to a scroll
 *    position the list has since outgrown.
 *
 *  THE INVARIANT A CALLER MAY RELY ON, and which the vitest suite pins across a
 *  range of inputs: `rowsBefore + rowsInWindow + rowsAfter` equals the row count
 *  EXACTLY, and `startIndex` is never past `endIndex`. Both spacers and the
 *  drawn rows therefore always account for the whole document, whatever the
 *  viewport claimed. */
export function computeDiffRowWindow(
  rowCount: number,
  firstVisibleRowIndex: number,
  visibleRowCount: number,
  overscanRows = 0,
): DiffRowWindow {
  const totalRows = wholeRowCount(rowCount);
  if (totalRows <= DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS) {
    return {
      virtualized: false,
      startIndex: 0,
      endIndex: totalRows,
      rowsBefore: 0,
      rowsInWindow: totalRows,
      rowsAfter: 0,
    };
  }
  const visible = wholeRowCount(visibleRowCount);
  const overscan = wholeRowCount(overscanRows);
  const first = Math.min(wholeRowCount(firstVisibleRowIndex), totalRows);
  const startIndex = visible === 0 ? first : Math.max(0, first - overscan);
  const endIndex = visible === 0
    ? startIndex
    : Math.min(totalRows, first + visible + overscan);
  return {
    virtualized: true,
    startIndex,
    endIndex,
    rowsBefore: startIndex,
    rowsInWindow: endIndex - startIndex,
    rowsAfter: totalRows - endIndex,
  };
}
