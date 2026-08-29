// The PURE half of F037's rendering core (T5_F037 T002): the diff endpoint's
// envelope turned into the flat list of rows a renderer draws. It holds no
// markup, issues no fetch and touches no stylesheet, so every rule below is
// decidable from plain data alone.
//
// DECISION F031 D5 is why the rule lives HERE rather than inside `DiffView.tsx`,
// the component that draws these rows: the shipped `apps/ui/vitest.config.ts`
// collects `src/**/*.test.ts` in a NODE environment and reaches no markup at
// all, so a collapse rule or a row key written into a `.tsx` file is a rule no
// gate in this repository can execute. DECISION F037 D8 records the same
// reasoning for this feature specifically, and
// `tests/ui_contracts/test_diff_view_model.py` pins the structural half vitest
// cannot see about itself. The segments `splitLineIntoIntralineSegments`
// returns are what `DiffView.tsx` wraps in the intraline mark, and DECISION
// F037 D9 rules what that mark looks like — this module chooses no colour and
// names no class.
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

/** WHY THE PREFIX: a server hunk id is sixteen lowercase hex characters, so a
 *  string carrying this prefix cannot be mistaken for one by any consumer, which
 *  is the whole point of it (DECISION F033 D2). */
export const UNIDENTIFIED_HUNK_ID_PREFIX = "unidentified:";

/** One hunk, with the id the parser assigned. A hunk whose `id` is absent or not
 *  a string is given an id the client INVENTS, carrying
 *  `UNIDENTIFIED_HUNK_ID_PREFIX` ahead of the hunk's position: every row key
 *  below is derived from the id and a blank one would collapse two hunks onto a
 *  single key, so an id there must be, but it must not be one a consumer could
 *  read as the server's own. The position is what keeps the invented ids
 *  DISTINCT from each other; the prefix is what keeps them out of the server's
 *  id space. A real id passes through UNTOUCHED and unvalidated — this client is
 *  not the authority on what a server id looks like. */
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
    id: rawId !== "" ? rawId : `${UNIDENTIFIED_HUNK_ID_PREFIX}file${fileIndex}:hunk${hunkIndex}`,
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
 *  Declared once, here. Every other site NAMES this constant rather than
 *  repeating the number, which is what stops the rule and its tests from
 *  drifting apart, and each of these was grepped before being written down:
 *  `defaultCollapsedHunkIds` below, `diffViewModel.test.ts`,
 *  `tests/ui_contracts/test_diff_view_model.py` and
 *  `tests/ui_contracts/test_diff_view_render.py`. `DiffView.tsx` is NOT among
 *  them — it renders these rows but never names this constant, and an earlier
 *  wording of this paragraph said it did. */
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
 *  is. Its ONE consumer is `computeDiffRowWindow` below; that function and the
 *  vitest suite name this constant rather than repeating the digits, which is
 *  what keeps the rule and its own tests from drifting apart. The component
 *  names it nowhere and never did: `DiffView.tsx` calls
 *  `diffRowWindowForViewport` and derives no threshold of its own, and
 *  `tests/ui_contracts/test_diff_view_render.py` forbids it the row-height
 *  constant for the same reason. */
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
 *  hands the result here as a row index. Since F037 R21 that caller is
 *  `diffRowWindowForViewport`, below in this same module, so the division is not
 *  untestable either — vitest executes it there. What remains untestable is the
 *  DOM READ alone, `scrollTop` and `clientHeight`, and keeping that read out of
 *  this module is what puts every rule of virtual scrolling in the layer
 *  `apps/ui/vitest.config.ts` reaches (DECISION F031 D5).
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

/** The pixel height ONE row is assumed to occupy — the single number every row
 *  index and every spacer height below is computed from.
 *
 *  WHY TWENTY, AND WHY FIXING IT IS HONEST RATHER THAN LAZY:
 *  `../components/diff/DiffView.module.css` declares `.diffLine` with
 *  `font: 12.5px/1.6`, and 12.5 x 1.6 is exactly twenty, so this constant is
 *  that sheet's own line box transcribed rather than a number invented here.
 *  `tests/ui_contracts/test_diff_view_render.py` parses both numbers out of the
 *  stylesheet, multiplies them and compares the product with this declaration,
 *  so the two cannot drift apart in silence.
 *
 *  IT IS AN ESTIMATE FOR THE ROWS THAT ARE NOT LINE ROWS. A hunk-head row wears
 *  `.hunkHead` and a file row wears no class at all, so neither is exactly this
 *  tall, and a document mixing the three has a real height this number only
 *  approximates. `DIFF_VIRTUAL_OVERSCAN_ROWS` below is what absorbs that error:
 *  the window is widened at both ends by more rows than the accumulated
 *  mis-estimate can shift it, so a slightly wrong offset still lands on a drawn
 *  row rather than on a blank stripe. */
export const DIFF_VIRTUAL_ROW_HEIGHT_PX = 20;

/** Rows drawn BEYOND the viewport at each end. A row scrolled into view is then
 *  already in the document instead of mounting as the operator reaches it,
 *  which is the difference between a list that scrolls and one that flashes an
 *  empty band at every turn of the wheel. It is also the slack that absorbs the
 *  row-height estimate above. */
export const DIFF_VIRTUAL_OVERSCAN_ROWS = 8;

/** The visible-row count assumed while the panel has NOT been measured yet.
 *
 *  THIS IS THE ONE REAL TRAP OF VIRTUAL SCROLLING HERE, AND IT IS WHY THE
 *  FALLBACK IS A RULE IN THIS MODULE RATHER THAN A DEFAULT ARGUMENT ON THE
 *  CALLER'S SIDE. On the first render a panel's `clientHeight` is 0, because the
 *  element does not exist yet. A viewport height of 0 divides to a visible count
 *  of 0; `computeDiffRowWindow` answers a visible count of 0 with an EMPTY
 *  window, correctly and by its own third rule; an empty window draws no rows; a
 *  panel with no rows in it never scrolls; and a panel that never scrolls never
 *  fires the event that would have measured it. The viewer would be blank
 *  forever. Resolving it HERE puts the resolution in the layer
 *  `apps/ui/vitest.config.ts` executes (DECISION F031 D5), so the trap is held
 *  shut by a test rather than by a reviewer's memory. */
export const DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS = 40;

/** A `DiffRowWindow` with the two spacer heights already in PIXELS.
 *
 *  Declared as a named type rather than left inline because it is what a
 *  component's whole render depends on, and because the pixel fields are the
 *  reason this shape exists at all: a caller sizes its spacers straight from
 *  `rowsBeforePx` and `rowsAfterPx` and performs no arithmetic of its own, which
 *  is what keeps every number of this feature's virtualization inside the layer
 *  vitest reaches. */
export interface DiffRowViewportWindow extends DiffRowWindow {
  rowsBeforePx: number;
  rowsAfterPx: number;
}

/** The window to draw, derived from a SCROLLED VIEWPORT rather than from row
 *  indices the caller worked out itself. TOTAL: no input makes this throw.
 *
 *  It is the division a viewport forces, and it lives here for the reason
 *  DECISION F031 D5 gives: a `.tsx` file computing it would be arithmetic no
 *  suite in this repository can execute. What the component keeps is the two
 *  numbers the DOM alone can supply — `scrollTop` and `clientHeight` — and
 *  nothing decided from them.
 *
 *  THE RULES:
 *  * every argument is resolved through the same whole-count reading
 *    `computeDiffRowWindow` uses, so a NaN, an infinity, a fraction or a
 *    negative can never become an index;
 *  * the first visible row is the scroll offset divided by
 *    `DIFF_VIRTUAL_ROW_HEIGHT_PX` rounded DOWN, because a row scrolled halfway
 *    off the top is still on screen;
 *  * the visible count is the viewport height divided by the same height
 *    rounded UP, for the same reason at the other edge — a row half in view is a
 *    row that must be drawn;
 *  * an UNMEASURED viewport, meaning a resolved height of 0, falls back to
 *    `DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS`; the comment on that constant is the
 *    whole reason this function exists rather than a default argument;
 *  * the window itself is `computeDiffRowWindow`'s answer, widened by
 *    `DIFF_VIRTUAL_OVERSCAN_ROWS`. None of that function's rules — the
 *    threshold, the clamps, the invariant — is reimplemented here.
 *
 *  The two pixel heights are the row counts on either side multiplied by the row
 *  height, so the spacers keep the scrollbar describing the WHOLE document while
 *  only a window of it is in the DOM. */
export function diffRowWindowForViewport(
  rowCount: number,
  scrollTopPx: number,
  viewportHeightPx: number,
): DiffRowViewportWindow {
  const totalRows = wholeRowCount(rowCount);
  const scrollTop = wholeRowCount(scrollTopPx);
  const viewportHeight = wholeRowCount(viewportHeightPx);
  const firstVisibleRowIndex = Math.floor(scrollTop / DIFF_VIRTUAL_ROW_HEIGHT_PX);
  const visibleRowCount = viewportHeight === 0
    ? DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS
    : Math.ceil(viewportHeight / DIFF_VIRTUAL_ROW_HEIGHT_PX);
  const rowWindow = computeDiffRowWindow(
    totalRows,
    firstVisibleRowIndex,
    visibleRowCount,
    DIFF_VIRTUAL_OVERSCAN_ROWS,
  );
  return {
    ...rowWindow,
    rowsBeforePx: rowWindow.rowsBefore * DIFF_VIRTUAL_ROW_HEIGHT_PX,
    rowsAfterPx: rowWindow.rowsAfter * DIFF_VIRTUAL_ROW_HEIGHT_PX,
  };
}

/** The file extensions this viewer highlights, as a FROZEN mapping from a
 *  lower-case extension WITHOUT its dot to the language id its bundle loads
 *  under.
 *
 *  WHY THE SET IS DELIBERATELY SMALL, which is the Design section of
 *  `docs/roadmap/features/T5_F037.md` in its own words — "a small supported set;
 *  unknown languages render plain — honest, fast": every entry here is a bundle
 *  somebody has to ship to a browser, so the list is not free and grows only for
 *  a language this repository's own diffs really carry. For everything else the
 *  honest answer is plain text rather than a guess, because highlighting a file
 *  as the WRONG language is worse than not highlighting it at all — it colours
 *  tokens that are not there, and a reader has no reason to distrust it.
 *
 *  FROZEN because it is shared module state that a caller could otherwise extend
 *  at runtime, which would put a language id in the map with no bundle behind
 *  it. TWO EXTENSIONS MAY SHARE ONE ID — `yml` and `yaml` are one language — and
 *  that is why this is a mapping rather than a list of extensions.
 *
 *  ON A NULL PROTOTYPE, which is the first half of finding `R-0731`'s fix and is
 *  LOAD-BEARING rather than decorative. A plain object literal INHERITS from
 *  `Object.prototype`, so `map.constructor` answers the `Object` constructor
 *  function and `map.__proto__` answers `Object.prototype` — values nobody put
 *  in the mapping. THE GENERAL RULE, not a special case for those two names: an
 *  object literal is the wrong shape for a lookup keyed by an ARBITRARY EXTERNAL
 *  STRING, in any language with prototype inheritance. The key here is a file
 *  extension taken from a diff path, and a diff path comes from a repository
 *  this viewer does not control, so the key set is the attacker's and not ours.
 *  `Object.create(null)` gives the mapping nothing to inherit, so every miss is
 *  a real miss.
 *
 *  `diffLanguageForPath` ALSO reads this through an own-property check, and the
 *  belt-and-braces is deliberate: either change alone repairs today's defect, so
 *  either one alone would let a later refactor undoing the other silently
 *  restore it. Both are load-bearing, and neither may be removed as redundant. */
export const DIFF_SUPPORTED_LANGUAGES: Readonly<Record<string, string>> = Object.freeze(
  Object.assign(Object.create(null) as Record<string, string>, {
    ts: "typescript",
    tsx: "tsx",
    js: "javascript",
    jsx: "jsx",
    py: "python",
    json: "json",
    css: "css",
    md: "markdown",
    sh: "shell",
    yml: "yaml",
    yaml: "yaml",
    toml: "toml",
  }),
);

/** The language id to highlight `path` as, or `null` meaning "render it plain".
 *  TOTAL: no input throws, and `null` is an ANSWER rather than an error — plain
 *  is a legitimate way to render a file, which is what makes Acceptance's
 *  "unknown language renders plain" a rule rather than a failure mode.
 *
 *  THE FOUR DECISIONS, each of them a case a one-liner gets wrong:
 *
 *  * the extension is read from the BASENAME, never from the whole path. The
 *    server's diff paths are posix, so the last `/` ends the directory part, and
 *    only what follows it is examined. `a/b.c/d` carries a dot and has no
 *    extension at all; reading the last dot of the whole string would answer
 *    `c/d`, and `a/b.c/d.ts` must still answer `ts`.
 *  * the extension is what follows the LAST dot of that basename, LOWER-CASED,
 *    so `App.TSX` resolves. Case is folded because a file name's case is its
 *    author's habit and not a language.
 *  * a basename whose last dot is its FIRST character has NO extension: it is a
 *    dotfile. This is the case `split(".").pop()` gets wrong, and the
 *    DISCRIMINATING example is a basename that is nothing BUT a supported
 *    extension — a file named `.ts` is a hidden file called `ts`, not a
 *    TypeScript file, and without this rule it would be highlighted as one. A
 *    basename with no dot at all is plain for the same reason, and so is the
 *    empty path.
 *  * a basename ENDING in a dot has an EMPTY extension, which is in no supported
 *    set and is therefore plain.
 *
 *  An extension that survives all four and is still not in
 *  `DIFF_SUPPORTED_LANGUAGES` is plain. That is Acceptance's own sentence, and
 *  `loadDiffLanguageBundle` is what makes it OBSERVABLE rather than merely true:
 *  a plain answer is reached without asking for a bundle at all. */
export function diffLanguageForPath(path: string): string | null {
  const basename = path.slice(path.lastIndexOf("/") + 1);
  const dot = basename.lastIndexOf(".");
  if (dot <= 0 || dot === basename.length - 1) {
    return null;
  }
  const extension = basename.slice(dot + 1).toLowerCase();
  // ABSENCE IS DECIDED BY AN OWN-PROPERTY CHECK, never by comparing the read
  // value to `undefined`. That comparison is what finding `R-0731` was: it
  // answers "present" for every key an object INHERITS, so a path ending in
  // `.constructor` resolved to a function and then reached the bundle importer
  // that Acceptance says must never be called for a plain file. The extension is
  // an arbitrary external string — it arrives inside a diff path from a
  // repository this viewer does not control — and the safe question about such a
  // key is whether the mapping OWNS it, not whether reading it yielded something.
  // This is the second half of that fix; the declaration above builds the mapping
  // on a null prototype and is the first. BOTH ARE LOAD-BEARING: either alone
  // repairs the defect, which is exactly why removing either one as redundant
  // restores it the moment the other is refactored away.
  if (!Object.prototype.hasOwnProperty.call(DIFF_SUPPORTED_LANGUAGES, extension)) {
    return null;
  }
  return DIFF_SUPPORTED_LANGUAGES[extension];
}

/** How a syntax bundle is fetched: a function from a language id to a promise of
 *  that language's bundle. It is a TYPE AND NOTHING MORE. This module ships no
 *  bundles and imports nothing, which is the whole of what "lazy" means here — a
 *  static import of a highlighter would put every language in the main chunk and
 *  the laziness would exist only in the name of the function. */
export type DiffLanguageBundleImporter = (language: string) => Promise<unknown>;

/** What `loadDiffLanguageBundle` answers. `language` is `null` exactly when the
 *  path renders plain, and `bundle` is `null` whenever there is nothing to
 *  highlight WITH — either because the answer is plain or because the import did
 *  not arrive. The two fields are separate for that second case: a language
 *  resolved from a path stays true even when its bundle never loads. */
export interface DiffLanguageBundleAnswer {
  language: string | null;
  bundle: unknown;
}

const diffLanguageBundleCache = new Map<string, Promise<unknown>>();

/** Forget every bundle loaded so far. IT EXISTS FOR THE TESTS, and saying so is
 *  more honest than dressing it up: the cache below is module state no caller
 *  can otherwise observe, and an unobservable cache is one no gate can hold to
 *  its promise of "one import per language". A test that cannot reset it either
 *  leaks state into the next test or proves nothing. The application never calls
 *  this — a bundle stays loaded for the life of the page, which is the point. */
export function resetDiffLanguageBundleCache(): void {
  diffLanguageBundleCache.clear();
}

/** The syntax bundle for `path`'s language, loaded at most once per language.
 *  TOTAL: it never throws and never rejects, exactly as `loadDiffEnvelope` never
 *  throws — a viewer that cannot highlight still has to render the diff.
 *
 *  `importBundle` IS REQUIRED AND HAS NO DEFAULT, which is the one real design
 *  choice here. A default that threw only when called would be swallowed by this
 *  function's own degrade-to-plain rule below and arrive at the operator as "that
 *  language is not supported" — a wiring mistake wearing the costume of a correct
 *  answer. Required makes the same mistake a compile error instead, and it keeps
 *  the promise the type above makes: this module names no highlighter.
 *
 *  THE FOUR RULES:
 *
 *  * THE ACCEPTANCE PROPERTY, which is the reason this function exists rather
 *    than a `diffLanguageForPath` call at the call site: for a path that renders
 *    plain, `importBundle` IS NEVER CALLED. Not called and discarded, not called
 *    and left unawaited — never invoked, so no chunk is ever requested for a file
 *    this viewer was never going to highlight. The answer is
 *    `{ language: null, bundle: null }` and the vitest suite pins the call count
 *    at exactly zero rather than at "falsy".
 *  * A FAILING IMPORT DEGRADES TO PLAIN. Whether `importBundle` throws
 *    synchronously or returns a promise that rejects, the answer is
 *    `{ language, bundle: null }`: the language is still reported, because it was
 *    resolved from the path and remains true, and only the bundle is missing.
 *  * ONE IMPORT PER LANGUAGE. The cache is keyed by language id and holds the
 *    PROMISE rather than the resolved bundle, so two files of the same language
 *    asking at the same moment share one import instead of racing to start two.
 *  * A FAILED IMPORT IS RETRIED, NOT CACHED. The rejected promise is dropped from
 *    the cache, so a later call tries again. A bundle request fails for transient
 *    reasons — a chunk that lost the network — and caching that failure would
 *    make one bad second permanent for the life of the page, with no way for the
 *    operator to ask again short of a reload. */
export async function loadDiffLanguageBundle(
  path: string,
  importBundle: DiffLanguageBundleImporter,
): Promise<DiffLanguageBundleAnswer> {
  const language = diffLanguageForPath(path);
  if (language === null) {
    return { language: null, bundle: null };
  }
  try {
    let pending = diffLanguageBundleCache.get(language);
    if (pending === undefined) {
      pending = Promise.resolve(importBundle(language));
      diffLanguageBundleCache.set(language, pending);
    }
    return { language, bundle: await pending };
  } catch {
    diffLanguageBundleCache.delete(language);
    return { language, bundle: null };
  }
}
