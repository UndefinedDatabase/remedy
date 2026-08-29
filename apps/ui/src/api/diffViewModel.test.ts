import { describe, it, expect, beforeEach } from "vitest";
import {
  DIFF_HUNK_COLLAPSE_THRESHOLD_LINES,
  DIFF_SUPPORTED_LANGUAGES,
  DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS,
  DIFF_VIRTUAL_OVERSCAN_ROWS,
  DIFF_VIRTUAL_ROW_HEIGHT_PX,
  DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS,
  UNIDENTIFIED_HUNK_ID_PREFIX,
  buildDiffFileSummaries,
  buildDiffRowModels,
  computeDiffRowWindow,
  defaultCollapsedHunkIds,
  diffLanguageForPath,
  diffRowWindowForViewport,
  loadDiffLanguageBundle,
  readDiffEnvelope,
  resetDiffLanguageBundleCache,
  splitLineIntoIntralineSegments,
  toggleHunkCollapse,
} from "./diffViewModel";
import type {
  DiffEnvelope,
  DiffIntralineSpan,
  DiffLanguageBundleImporter,
  DiffLine,
  DiffLineSegment,
  DiffRowModel,
  DiffRowViewportWindow,
  DiffRowWindow,
} from "./diffViewModel";

/** The envelope version the SERVER really sends. F033 R3 derived the hunk ids
 *  from content and bumped `DIFF_VIEW_VERSION` to 2, so a fixture still claiming
 *  1 would describe a server that no longer exists — and these fixtures are the
 *  only thing standing between this client and a version's worth of drift,
 *  because every payload below is built here rather than fetched. */
const WIRE_DIFF_VIEW_VERSION = 2;

/** Hunk ids in the shape `packages/orchestration/hunk_identity.py` really
 *  assigns at that version: SIXTEEN LOWERCASE HEX characters, distinct per hunk.
 *  Written out rather than recomputed here, because what a client fixture owes
 *  the server is the SHAPE of an id and never the hash behind it — the client
 *  reads ids and derives none. */
const SERVER_HUNK_ID = "3f5a9c1e0b7d2481";
const SECOND_SERVER_HUNK_ID = "a41d0c7e93b6f582";
const THIRD_SERVER_HUNK_ID = "b0e27d4a1c9f6835";

/** A hunk in the SNAKE_CASE form the endpoint really sends, carrying `count`
 *  context lines. The id is passed in because every row key derives from it. */
function wireHunk(id: string, count: number) {
  return {
    id,
    header: `@@ -1,${count} +1,${count} @@`,
    old_start: 1,
    new_start: 1,
    lines: Array.from({ length: count }, (_unused, index) => ({
      kind: "ctx",
      old_ln: index + 1,
      new_ln: index + 1,
      content: `line ${index}`,
      intraline: [],
    })),
  };
}

function wireFile(path: string, hunks: unknown[]) {
  return {
    path,
    old_path: null,
    status: "modified",
    stats: { added: 2, deleted: 1 },
    note: null,
    hunks,
  };
}

function wireEnvelope(files: unknown[]) {
  return {
    version: WIRE_DIFF_VIEW_VERSION,
    scope: "task",
    task_id: "t-1",
    source: "runs/r-1/workspace.diff",
    available: true,
    reason: null,
    truncated: false,
    task_run_ids: ["r-1", "r-2"],
    files,
  };
}

/** The same payload as `wireEnvelope([wireFile(...)])` with every dual-spelled
 *  field written in camelCase instead, so the two can be compared field for
 *  field rather than trusted separately. */
function camelPayload() {
  return {
    version: WIRE_DIFF_VIEW_VERSION,
    scope: "task",
    taskId: "t-1",
    source: "runs/r-1/workspace.diff",
    available: true,
    reason: null,
    truncated: false,
    taskRunIds: ["r-1", "r-2"],
    files: [
      {
        path: "a.py",
        oldPath: null,
        status: "modified",
        stats: { added: 2, deleted: 1 },
        note: null,
        hunks: [
          {
            id: SERVER_HUNK_ID,
            header: "@@ -1,2 +1,2 @@",
            oldStart: 1,
            newStart: 1,
            lines: [
              { kind: "ctx", oldLn: 1, newLn: 1, content: "line 0", intraline: [] },
              { kind: "ctx", oldLn: 2, newLn: 2, content: "line 1", intraline: [] },
            ],
          },
        ],
      },
    ],
  };
}

function snakePayload() {
  return {
    version: WIRE_DIFF_VIEW_VERSION,
    scope: "task",
    task_id: "t-1",
    source: "runs/r-1/workspace.diff",
    available: true,
    reason: null,
    truncated: false,
    task_run_ids: ["r-1", "r-2"],
    files: [wireFile("a.py", [wireHunk(SERVER_HUNK_ID, 2)])],
  };
}

/** An envelope with one file and one hunk of `count` lines, already read. */
function envelopeWithHunkOf(count: number): DiffEnvelope {
  return readDiffEnvelope(wireEnvelope([wireFile("a.py", [wireHunk(SERVER_HUNK_ID, count)])]));
}

describe("readDiffEnvelope", () => {
  it("reads the wire's snake_case and the app's camelCase to the same envelope", () => {
    expect(readDiffEnvelope(snakePayload())).toEqual(readDiffEnvelope(camelPayload()));
  });

  it("carries every field of a well-formed payload through unchanged", () => {
    const envelope = readDiffEnvelope(snakePayload());
    expect(envelope.available).toBe(true);
    expect(envelope.version).toBe(WIRE_DIFF_VIEW_VERSION);
    expect(envelope.scope).toBe("task");
    expect(envelope.taskId).toBe("t-1");
    expect(envelope.source).toBe("runs/r-1/workspace.diff");
    expect(envelope.taskRunIds).toEqual(["r-1", "r-2"]);
    expect(envelope.files).toHaveLength(1);
    expect(envelope.files[0].path).toBe("a.py");
    expect(envelope.files[0].stats).toEqual({ added: 2, deleted: 1 });
    expect(envelope.files[0].hunks[0].id).toBe(SERVER_HUNK_ID);
    expect(envelope.files[0].hunks[0].oldStart).toBe(1);
    expect(envelope.files[0].hunks[0].lines).toHaveLength(2);
    expect(envelope.files[0].hunks[0].lines[0].newLn).toBe(1);
  });

  it("answers a payload that is a string with the unavailable envelope", () => {
    const envelope = readDiffEnvelope("not a payload");
    expect(envelope.available).toBe(false);
    expect(envelope.files).toEqual([]);
  });

  it("answers null and undefined with the unavailable envelope rather than throwing", () => {
    expect(() => readDiffEnvelope(null)).not.toThrow();
    expect(readDiffEnvelope(null).available).toBe(false);
    expect(readDiffEnvelope(undefined).files).toEqual([]);
  });

  it("answers an array payload with the unavailable envelope", () => {
    expect(readDiffEnvelope([]).available).toBe(false);
  });

  it("refuses to look available when files is not an array", () => {
    const envelope = readDiffEnvelope({ ...snakePayload(), files: "everything" });
    expect(envelope.available).toBe(false);
    expect(envelope.files).toEqual([]);
  });

  it("drops a line whose kind is not one the contract names, keeping the rest", () => {
    const broken = wireEnvelope([
      wireFile("a.py", [
        {
          id: SERVER_HUNK_ID,
          header: "@@ -1,3 +1,3 @@",
          old_start: 1,
          new_start: 1,
          lines: [
            { kind: "ctx", old_ln: 1, new_ln: 1, content: "kept", intraline: [] },
            { kind: "sideways", old_ln: 2, new_ln: 2, content: "dropped", intraline: [] },
            { kind: "add", old_ln: null, new_ln: 3, content: "kept too", intraline: [] },
          ],
        },
      ]),
    ]);
    const lines = readDiffEnvelope(broken).files[0].hunks[0].lines;
    expect(lines.map((line) => line.content)).toEqual(["kept", "kept too"]);
  });

  it("defaults a missing intraline list to the empty array", () => {
    const noSpans = wireEnvelope([
      wireFile("a.py", [
        {
          id: SERVER_HUNK_ID,
          header: "@@ -1,1 +1,1 @@",
          old_start: 1,
          new_start: 1,
          lines: [{ kind: "ctx", old_ln: 1, new_ln: 1, content: "alpha" }],
        },
      ]),
    ]);
    expect(readDiffEnvelope(noSpans).files[0].hunks[0].lines[0].intraline).toEqual([]);
  });

  it("truncates only on a literal true, never on a truthy stand-in", () => {
    expect(readDiffEnvelope({ ...snakePayload(), truncated: true }).truncated).toBe(true);
    expect(readDiffEnvelope({ ...snakePayload(), truncated: "yes" }).truncated).toBe(false);
    expect(readDiffEnvelope({ ...snakePayload(), truncated: 1 }).truncated).toBe(false);
  });

  it("marks a hunk with no usable id UNIDENTIFIED instead of inventing a server-shaped one", () => {
    // DECISION F033 D2. The client still needs an id — every row key derives
    // from one — but the value it invents must be LEGIBLE as invented. A bare
    // `"0:0"` sits in the same field as a content id, reads as one to every
    // consumer downstream, and matches nothing the server would recognise.
    const noId = wireEnvelope([wireFile("a.py", [{ header: "@@ @@", lines: [] }])]);
    const id = readDiffEnvelope(noId).files[0].hunks[0].id;
    expect(id.startsWith(UNIDENTIFIED_HUNK_ID_PREFIX)).toBe(true);
    expect(id).not.toBe("0:0");
    expect(id.length).toBeGreaterThan(UNIDENTIFIED_HUNK_ID_PREFIX.length);
  });

  it("gives two id-less hunks in ONE file DISTINCT ids, so the collapse set still sees two", () => {
    // The property the position inside the invented id exists for: a shared id
    // would make `defaultCollapsedHunkIds` and `toggleHunkCollapse` fold the two
    // hunks into one entry of their `Set<string>` and collapse them together.
    const noIds = wireEnvelope([
      wireFile("a.py", [
        { header: "@@ -1,1 +1,1 @@", lines: [] },
        { header: "@@ -9,1 +9,1 @@", lines: [] },
      ]),
    ]);
    const hunks = readDiffEnvelope(noIds).files[0].hunks;
    expect(hunks).toHaveLength(2);
    for (const hunk of hunks) {
      expect(hunk.id.startsWith(UNIDENTIFIED_HUNK_ID_PREFIX), hunk.id).toBe(true);
    }
    expect(new Set(hunks.map((hunk) => hunk.id)).size).toBe(2);
    expect(toggleHunkCollapse(new Set([hunks[0].id]), hunks[1].id).size).toBe(2);
  });

  it("passes a well-formed SERVER hunk id through unchanged, prefixing nothing", () => {
    // The other half of DECISION F033 D2: the client is not the authority on
    // what a server id looks like, so a real one is neither validated nor
    // reshaped — a consumer that rejected ids it did not recognise would break
    // the next version bump for no gain.
    const envelope = readDiffEnvelope(
      wireEnvelope([wireFile("a.py", [wireHunk(SERVER_HUNK_ID, 1)])]),
    );
    const id = envelope.files[0].hunks[0].id;
    expect(id).toBe(SERVER_HUNK_ID);
    expect(id.startsWith(UNIDENTIFIED_HUNK_ID_PREFIX)).toBe(false);
    expect(id).toMatch(/^[0-9a-f]{16}$/);
  });

  it("never throws, however broken the payload it is handed", () => {
    const payloads: unknown[] = [0, true, "", [1, 2], { files: [null] }, { files: [{ hunks: 7 }] }];
    for (const payload of payloads) {
      expect(() => readDiffEnvelope(payload)).not.toThrow();
    }
  });
});

describe("defaultCollapsedHunkIds", () => {
  it("leaves a hunk of exactly the threshold open, because the boundary is inclusive", () => {
    const envelope = envelopeWithHunkOf(DIFF_HUNK_COLLAPSE_THRESHOLD_LINES);
    expect(defaultCollapsedHunkIds(envelope).has(SERVER_HUNK_ID)).toBe(false);
  });

  it("collapses a hunk one line past the threshold", () => {
    const envelope = envelopeWithHunkOf(DIFF_HUNK_COLLAPSE_THRESHOLD_LINES + 1);
    expect(defaultCollapsedHunkIds(envelope).has(SERVER_HUNK_ID)).toBe(true);
  });

  it("collapses nothing in an envelope of small hunks", () => {
    expect(defaultCollapsedHunkIds(readDiffEnvelope(snakePayload())).size).toBe(0);
  });

  it("collapses nothing in the unavailable envelope", () => {
    expect(defaultCollapsedHunkIds(readDiffEnvelope(null)).size).toBe(0);
  });
});

describe("toggleHunkCollapse", () => {
  it("returns the opposite membership without touching the set it was given", () => {
    const before = new Set([SERVER_HUNK_ID]);
    const opened = toggleHunkCollapse(before, SERVER_HUNK_ID);
    expect(opened.has(SERVER_HUNK_ID)).toBe(false);
    expect(before.has(SERVER_HUNK_ID)).toBe(true);
    expect(opened).not.toBe(before);
  });

  it("adds a hunk that was not collapsed and leaves the others alone", () => {
    const before = new Set([SERVER_HUNK_ID]);
    const next = toggleHunkCollapse(before, THIRD_SERVER_HUNK_ID);
    expect(next.has(THIRD_SERVER_HUNK_ID)).toBe(true);
    expect(next.has(SERVER_HUNK_ID)).toBe(true);
    expect(before.size).toBe(1);
  });

  it("round-trips a hunk back to where it started", () => {
    const before = new Set<string>();
    const there = toggleHunkCollapse(before, SERVER_HUNK_ID);
    expect(toggleHunkCollapse(there, SERVER_HUNK_ID).size).toBe(0);
  });
});

describe("buildDiffRowModels", () => {
  it("emits a head row and every line row of an open hunk", () => {
    const envelope = readDiffEnvelope(snakePayload());
    const rows = buildDiffRowModels(envelope, new Set<string>());
    expect(rows.map((row) => row.kind)).toEqual(["file", "hunkHead", "line", "line"]);
  });

  it("emits the head of a collapsed hunk and none of its lines", () => {
    const envelope = readDiffEnvelope(snakePayload());
    const rows = buildDiffRowModels(envelope, new Set([SERVER_HUNK_ID]));
    expect(rows.map((row) => row.kind)).toEqual(["file", "hunkHead"]);
  });

  it("says on the head row how many lines a collapsed hunk is hiding", () => {
    const envelope = readDiffEnvelope(snakePayload());
    const [, head] = buildDiffRowModels(envelope, new Set([SERVER_HUNK_ID]));
    expect(head.kind).toBe("hunkHead");
    if (head.kind === "hunkHead") {
      expect(head.collapsed).toBe(true);
      expect(head.hiddenLineCount).toBe(2);
    }
  });

  it("hides nothing on the head row of an open hunk", () => {
    const envelope = readDiffEnvelope(snakePayload());
    const [, head] = buildDiffRowModels(envelope, new Set<string>());
    if (head.kind === "hunkHead") {
      expect(head.collapsed).toBe(false);
      expect(head.hiddenLineCount).toBe(0);
    }
  });

  it("keeps every key unique across a two-file envelope", () => {
    const envelope = readDiffEnvelope(
      wireEnvelope([
        wireFile("a.py", [wireHunk(SERVER_HUNK_ID, 3), wireHunk(SECOND_SERVER_HUNK_ID, 2)]),
        wireFile("b.py", [wireHunk(THIRD_SERVER_HUNK_ID, 4)]),
      ]),
    );
    const rows = buildDiffRowModels(envelope, new Set<string>());
    const keys = rows.map((row) => row.key);
    expect(new Set(keys).size).toBe(keys.length);
  });

  it("keeps the keys of the rows that survive a collapse unchanged", () => {
    const envelope = readDiffEnvelope(
      wireEnvelope([
        wireFile("a.py", [wireHunk(SERVER_HUNK_ID, 2), wireHunk(SECOND_SERVER_HUNK_ID, 2)]),
      ]),
    );
    const open = buildDiffRowModels(envelope, new Set<string>());
    const half = buildDiffRowModels(envelope, new Set([SECOND_SERVER_HUNK_ID]));
    const survivors = new Set(half.map((row) => row.key));
    const openKeys = open.filter((row) => survivors.has(row.key)).map((row) => row.key);
    expect(openKeys).toEqual(half.map((row) => row.key));
  });

  it("emits a file row for a file carrying no hunks at all", () => {
    const envelope = readDiffEnvelope(wireEnvelope([wireFile("logo.png", [])]));
    const rows = buildDiffRowModels(envelope, new Set<string>());
    expect(rows.map((row) => row.kind)).toEqual(["file"]);
    expect(rows[0].key).toBe("file:0");
  });

  it("reads the envelope's own order rather than sorting it", () => {
    const envelope = readDiffEnvelope(
      wireEnvelope([wireFile("z.py", [wireHunk(SERVER_HUNK_ID, 1)]), wireFile("a.py", [])]),
    );
    const rows = buildDiffRowModels(envelope, new Set<string>());
    const paths = rows.flatMap((row) => (row.kind === "file" ? [row.file.path] : []));
    expect(paths).toEqual(["z.py", "a.py"]);
  });

  it("builds no rows at all from the unavailable envelope", () => {
    expect(buildDiffRowModels(readDiffEnvelope("broken"), new Set<string>())).toEqual([]);
  });

  it("hides the whole of a hunk collapsed by the default rule", () => {
    const envelope = envelopeWithHunkOf(DIFF_HUNK_COLLAPSE_THRESHOLD_LINES + 1);
    const rows = buildDiffRowModels(envelope, defaultCollapsedHunkIds(envelope));
    expect(rows.filter((row) => row.kind === "line")).toHaveLength(0);
    const [, head] = rows;
    if (head.kind === "hunkHead") {
      expect(head.hiddenLineCount).toBe(DIFF_HUNK_COLLAPSE_THRESHOLD_LINES + 1);
    }
  });
});

describe("buildDiffFileSummaries", () => {
  it("reports one entry per file with the stats the envelope carries", () => {
    const envelope = readDiffEnvelope(
      wireEnvelope([
        wireFile("a.py", [wireHunk(SERVER_HUNK_ID, 3), wireHunk(SECOND_SERVER_HUNK_ID, 2)]),
        wireFile("b.py", []),
      ]),
    );
    const summaries = buildDiffFileSummaries(envelope);
    expect(summaries).toHaveLength(2);
    expect(summaries[0].path).toBe("a.py");
    expect(summaries[0].added).toBe(2);
    expect(summaries[0].deleted).toBe(1);
    expect(summaries[0].hunkCount).toBe(2);
    expect(summaries[1].path).toBe("b.py");
    expect(summaries[1].hunkCount).toBe(0);
  });

  it("gives every summary the row key of that file's own row", () => {
    const envelope = readDiffEnvelope(
      wireEnvelope([wireFile("a.py", [wireHunk(SERVER_HUNK_ID, 1)]), wireFile("b.py", [])]),
    );
    const rowKeys = buildDiffRowModels(envelope, new Set<string>())
      .filter((row) => row.kind === "file")
      .map((row) => row.key);
    expect(buildDiffFileSummaries(envelope).map((entry) => entry.rowKey)).toEqual(rowKeys);
  });

  it("summarises the unavailable envelope as no files rather than as an error", () => {
    expect(buildDiffFileSummaries(readDiffEnvelope(null))).toEqual([]);
  });
});

/** One `del` line carrying exactly the spans a case is about, built directly
 *  rather than read off a payload: `readDiffEnvelope` has its own tests above,
 *  and a span this hostile would not survive being routed through one. */
function lineWith(content: string, intraline: DiffIntralineSpan[]): DiffLine {
  return { kind: "del", oldLn: 1, newLn: null, content, intraline };
}

function joined(segments: DiffLineSegment[]): string {
  return segments.map((segment) => segment.text).join("");
}

/** Every case below, named once so the round-trip property can be asserted over
 *  ALL of them rather than restated case by case. That property — the segments
 *  concatenate back to `content` — is what catches an arithmetic slip whatever
 *  form it takes: a dropped character, a duplicated one, an off-by-one clamp. */
const SEGMENT_CASES: Array<{ what: string; content: string; spans: DiffIntralineSpan[] }> = [
  { what: "no spans", content: "alpha beta", spans: [] },
  { what: "one span in the middle", content: "alpha beta gamma", spans: [[6, 4]] },
  { what: "a span at offset zero", content: "alpha beta", spans: [[0, 5]] },
  { what: "two overlapping spans", content: "abcdefgh", spans: [[1, 3], [2, 4]] },
  { what: "two out-of-order spans", content: "abcdefgh", spans: [[5, 2], [1, 2]] },
  { what: "a span past the end", content: "abc", spans: [[9, 2]] },
  { what: "a span starting exactly at the end", content: "abc", spans: [[3, 1]] },
  { what: "a span running past the end", content: "abcde", spans: [[3, 99]] },
  { what: "a zero-length and a negative-length span", content: "abcde", spans: [[1, 0], [2, -3]] },
  { what: "a span reaching back before offset zero", content: "abcde", spans: [[-2, 4]] },
  { what: "empty content", content: "", spans: [[0, 3]] },
];

describe("splitLineIntoIntralineSegments", () => {
  it("yields one unmarked segment when the line carries no spans", () => {
    expect(splitLineIntoIntralineSegments(lineWith("alpha beta", []))).toEqual([
      { text: "alpha beta", marked: false },
    ]);
  });

  it("cuts a span in the middle into unmarked, marked, unmarked", () => {
    expect(splitLineIntoIntralineSegments(lineWith("alpha beta gamma", [[6, 4]]))).toEqual([
      { text: "alpha ", marked: false },
      { text: "beta", marked: true },
      { text: " gamma", marked: false },
    ]);
  });

  it("emits no leading empty segment for a span at offset zero", () => {
    const segments = splitLineIntoIntralineSegments(lineWith("alpha beta", [[0, 5]]));
    expect(segments).toEqual([
      { text: "alpha", marked: true },
      { text: " beta", marked: false },
    ]);
    expect(segments.every((segment) => segment.text !== "")).toBe(true);
  });

  it("marks the union of two overlapping spans exactly once", () => {
    expect(splitLineIntoIntralineSegments(lineWith("abcdefgh", [[1, 3], [2, 4]]))).toEqual([
      { text: "a", marked: false },
      { text: "bcdef", marked: true },
      { text: "gh", marked: false },
    ]);
  });

  it("marks both regions when the spans arrive out of order", () => {
    expect(splitLineIntoIntralineSegments(lineWith("abcdefgh", [[5, 2], [1, 2]]))).toEqual([
      { text: "a", marked: false },
      { text: "bc", marked: true },
      { text: "de", marked: false },
      { text: "fg", marked: true },
      { text: "h", marked: false },
    ]);
  });

  it("drops a span that starts at or past the end of the content", () => {
    expect(splitLineIntoIntralineSegments(lineWith("abc", [[9, 2]]))).toEqual([
      { text: "abc", marked: false },
    ]);
    expect(splitLineIntoIntralineSegments(lineWith("abc", [[3, 1]]))).toEqual([
      { text: "abc", marked: false },
    ]);
  });

  it("clamps a span that runs past the end rather than dropping it", () => {
    expect(splitLineIntoIntralineSegments(lineWith("abcde", [[3, 99]]))).toEqual([
      { text: "abc", marked: false },
      { text: "de", marked: true },
    ]);
  });

  it("drops a zero-length and a negative-length span", () => {
    expect(splitLineIntoIntralineSegments(lineWith("abcde", [[1, 0], [2, -3]]))).toEqual([
      { text: "abcde", marked: false },
    ]);
  });

  it("clamps a span reaching back before offset zero", () => {
    expect(splitLineIntoIntralineSegments(lineWith("abcde", [[-2, 4]]))).toEqual([
      { text: "ab", marked: true },
      { text: "cde", marked: false },
    ]);
  });

  it("answers empty content with the empty array rather than an empty segment", () => {
    expect(splitLineIntoIntralineSegments(lineWith("", [[0, 3]]))).toEqual([]);
  });

  it("concatenates back to the line's own content in every case", () => {
    for (const testCase of SEGMENT_CASES) {
      const segments = splitLineIntoIntralineSegments(lineWith(testCase.content, testCase.spans));
      expect(joined(segments), testCase.what).toBe(testCase.content);
    }
  });

  it("never emits an empty segment in any case", () => {
    for (const testCase of SEGMENT_CASES) {
      const segments = splitLineIntoIntralineSegments(lineWith(testCase.content, testCase.spans));
      expect(segments.filter((segment) => segment.text === ""), testCase.what).toEqual([]);
    }
  });
});

/** A list one row longer than the threshold: the SMALLEST list that virtualizes,
 *  so the boundary is exercised from the virtualized side rather than from far
 *  above it. Every count here is derived from the constant rather than written
 *  out, which is the same discipline the collapse threshold follows. */
const VIRTUALIZED_ROWS = DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS + 1;

/** The invariant of `DiffRowWindow` as one expression, so the sum test reads as
 *  the sentence the module's comment promises rather than as arithmetic. */
function windowSum(window: DiffRowWindow): number {
  return window.rowsBefore + window.rowsInWindow + window.rowsAfter;
}

/** Row counts on both sides of the threshold, including the boundary itself and
 *  the degenerate empty list. */
const WINDOW_ROW_COUNTS = [
  0,
  1,
  17,
  DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS,
  VIRTUALIZED_ROWS,
  DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS * 5,
];

/** `[firstVisibleRowIndex, visibleRowCount, overscanRows]`, well-formed and
 *  hostile together: the sum invariant is worth pinning precisely because it
 *  must survive the inputs nothing upstream validates. */
const WINDOW_VIEWPORTS: Array<[number, number, number]> = [
  [0, 40, 0],
  [0, 40, 10],
  [500, 40, 10],
  [-5, 40, 10],
  [Number.NaN, 40, 10],
  [Number.POSITIVE_INFINITY, 40, 10],
  [9999999, 40, 10],
  [500, 0, 10],
  [500, -3, 10],
  [500, 40, -7],
  [12.9, 40.7, 3.2],
];

describe("computeDiffRowWindow", () => {
  it("does not virtualize a list AT the threshold, and draws every row", () => {
    expect(computeDiffRowWindow(DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS, 500, 40, 10)).toEqual({
      virtualized: false,
      startIndex: 0,
      endIndex: DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS,
      rowsBefore: 0,
      rowsInWindow: DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS,
      rowsAfter: 0,
    });
  });

  it("does not virtualize a list below the threshold", () => {
    expect(computeDiffRowWindow(17, 5, 4, 2)).toEqual({
      virtualized: false,
      startIndex: 0,
      endIndex: 17,
      rowsBefore: 0,
      rowsInWindow: 17,
      rowsAfter: 0,
    });
  });

  it("answers the empty list with an empty, unvirtualized window", () => {
    expect(computeDiffRowWindow(0, 0, 40, 10)).toEqual({
      virtualized: false,
      startIndex: 0,
      endIndex: 0,
      rowsBefore: 0,
      rowsInWindow: 0,
      rowsAfter: 0,
    });
  });

  it("virtualizes one row above the threshold", () => {
    expect(computeDiffRowWindow(VIRTUALIZED_ROWS, 500, 40, 0).virtualized).toBe(true);
  });

  it("widens the visible range by the overscan at BOTH ends", () => {
    const window = computeDiffRowWindow(VIRTUALIZED_ROWS, 500, 50, 10);
    expect(window.startIndex).toBe(490);
    expect(window.endIndex).toBe(560);
    expect(window.rowsInWindow).toBe(70);
  });

  it("clamps the widened window to the start of the list", () => {
    const window = computeDiffRowWindow(VIRTUALIZED_ROWS, 5, 50, 10);
    expect(window.startIndex).toBe(0);
    expect(window.rowsBefore).toBe(0);
  });

  it("clamps the widened window to the end of the list", () => {
    const window = computeDiffRowWindow(VIRTUALIZED_ROWS, VIRTUALIZED_ROWS - 5, 50, 10);
    expect(window.endIndex).toBe(VIRTUALIZED_ROWS);
    expect(window.rowsAfter).toBe(0);
  });

  it("resolves a NEGATIVE first visible index to the top of the list", () => {
    const window = computeDiffRowWindow(VIRTUALIZED_ROWS, -5, 40, 0);
    expect(window.startIndex).toBe(0);
    expect(window.endIndex).toBe(40);
  });

  it("resolves a NON-FINITE first visible index to the top of the list", () => {
    for (const hostile of [Number.NaN, Number.POSITIVE_INFINITY, Number.NEGATIVE_INFINITY]) {
      const window = computeDiffRowWindow(VIRTUALIZED_ROWS, hostile, 40, 0);
      expect(window.startIndex, `index ${hostile}`).toBe(0);
      expect(window.endIndex, `index ${hostile}`).toBe(40);
    }
  });

  it("answers a NON-POSITIVE visible count with an empty window", () => {
    for (const hostile of [0, -5]) {
      const window = computeDiffRowWindow(VIRTUALIZED_ROWS, 500, hostile, 10);
      expect(window.rowsInWindow, `visible ${hostile}`).toBe(0);
      expect(window.startIndex, `visible ${hostile}`).toBe(window.endIndex);
    }
  });

  it("resolves a NEGATIVE overscan to no overscan at all", () => {
    const window = computeDiffRowWindow(VIRTUALIZED_ROWS, 500, 50, -7);
    expect(window.startIndex).toBe(500);
    expect(window.endIndex).toBe(550);
  });

  it("clamps a first visible index PAST THE END to the end of the list", () => {
    const window = computeDiffRowWindow(VIRTUALIZED_ROWS, VIRTUALIZED_ROWS + 9999, 40, 0);
    expect(window.startIndex).toBe(VIRTUALIZED_ROWS);
    expect(window.endIndex).toBe(VIRTUALIZED_ROWS);
    expect(window.rowsBefore).toBe(VIRTUALIZED_ROWS);
    expect(window.rowsAfter).toBe(0);
  });

  it("resolves a NON-FINITE or NEGATIVE row count to the empty list", () => {
    for (const hostile of [Number.NaN, Number.POSITIVE_INFINITY, -12]) {
      const window = computeDiffRowWindow(hostile, 500, 40, 10);
      expect(window, `rowCount ${hostile}`).toEqual({
        virtualized: false,
        startIndex: 0,
        endIndex: 0,
        rowsBefore: 0,
        rowsInWindow: 0,
        rowsAfter: 0,
      });
    }
  });

  it("truncates fractional counts rather than carrying them into an index", () => {
    const window = computeDiffRowWindow(VIRTUALIZED_ROWS, 12.9, 40.7, 3.2);
    expect(window.startIndex).toBe(9);
    expect(window.endIndex).toBe(55);
  });

  it("keeps the three counts summing to the row count across every input", () => {
    for (const rowCount of WINDOW_ROW_COUNTS) {
      for (const [first, visible, overscan] of WINDOW_VIEWPORTS) {
        const what = `rows ${rowCount}, viewport ${first}/${visible}/${overscan}`;
        const window = computeDiffRowWindow(rowCount, first, visible, overscan);
        expect(windowSum(window), what).toBe(rowCount);
      }
    }
  });

  it("never puts the start past the end, and never leaves the list", () => {
    for (const rowCount of WINDOW_ROW_COUNTS) {
      for (const [first, visible, overscan] of WINDOW_VIEWPORTS) {
        const what = `rows ${rowCount}, viewport ${first}/${visible}/${overscan}`;
        const window = computeDiffRowWindow(rowCount, first, visible, overscan);
        expect(window.startIndex, what).toBeLessThanOrEqual(window.endIndex);
        expect(window.startIndex, what).toBeGreaterThanOrEqual(0);
        expect(window.endIndex, what).toBeLessThanOrEqual(rowCount);
      }
    }
  });

  it("virtualizes on the ROW COUNT alone and on nothing about the viewport", () => {
    for (const [first, visible, overscan] of WINDOW_VIEWPORTS) {
      const what = `viewport ${first}/${visible}/${overscan}`;
      expect(
        computeDiffRowWindow(DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS, first, visible, overscan)
          .virtualized,
        what,
      ).toBe(false);
      expect(
        computeDiffRowWindow(VIRTUALIZED_ROWS, first, visible, overscan).virtualized,
        what,
      ).toBe(true);
    }
  });

  it("treats the overscan as optional and defaults it to none", () => {
    expect(computeDiffRowWindow(VIRTUALIZED_ROWS, 500, 50)).toEqual(
      computeDiffRowWindow(VIRTUALIZED_ROWS, 500, 50, 0),
    );
  });
});

/** A panel measured at exactly `DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS` rows, so the
 *  measured path and the unmeasured fallback answer the same visible count and
 *  every difference between them is the fallback itself. */
const MEASURED_VIEWPORT_PX =
  DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS * DIFF_VIRTUAL_ROW_HEIGHT_PX;

/** A scroll offset of exactly FIFTY-ONE AND A HALF rows. The half is the whole
 *  point: the floor is `HALF_ROW_SCROLL_ROWS` and the ceiling one more, so the
 *  two roundings give different answers and the assertion below can tell them
 *  apart. Far enough down the list that the overscan does not clamp the
 *  difference away at the top. */
const HALF_ROW_SCROLL_ROWS = 51;
const HALF_ROW_SCROLL_PX =
  HALF_ROW_SCROLL_ROWS * DIFF_VIRTUAL_ROW_HEIGHT_PX + DIFF_VIRTUAL_ROW_HEIGHT_PX / 2;

/** A panel measured at TWO AND A HALF rows, the mirror case: the ceiling is one
 *  more than `HALF_ROW_VIEWPORT_ROWS` and the floor is that number itself, so a
 *  height division rounded the other way changes the drawn count. */
const HALF_ROW_VIEWPORT_ROWS = 2;
const HALF_ROW_VIEWPORT_PX =
  HALF_ROW_VIEWPORT_ROWS * DIFF_VIRTUAL_ROW_HEIGHT_PX + DIFF_VIRTUAL_ROW_HEIGHT_PX / 2;

/** The scale this whole round exists for: a diff far larger than any viewport,
 *  which must still be drawn as a bounded window. */
const SCALE_ROWS = 10000;

/** Offsets and heights nothing upstream validates, which must be RESOLVED here
 *  rather than carried into an index or a pixel height. */
const HOSTILE_PIXEL_VALUES = [
  Number.NaN,
  Number.POSITIVE_INFINITY,
  Number.NEGATIVE_INFINITY,
  -DIFF_VIRTUAL_ROW_HEIGHT_PX * 3,
];

describe("diffRowWindowForViewport", () => {
  it("answers an UNMEASURED viewport with a NON-EMPTY window", () => {
    // THE TRAP THIS FUNCTION EXISTS FOR. A panel's clientHeight is 0 on the
    // first render; without the fallback the visible count is 0, the window is
    // empty, nothing is drawn, the panel never scrolls and so is never measured.
    const answer = diffRowWindowForViewport(VIRTUALIZED_ROWS, 0, 0);
    expect(answer.virtualized).toBe(true);
    expect(answer.rowsInWindow).toBeGreaterThan(0);
    expect(answer.endIndex).toBeGreaterThan(answer.startIndex);
    expect(answer.rowsInWindow).toBe(
      DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS + DIFF_VIRTUAL_OVERSCAN_ROWS,
    );
  });

  it("does not virtualize below the threshold: no spacers, every row drawn", () => {
    const rows = 17;
    const answer = diffRowWindowForViewport(rows, HALF_ROW_SCROLL_PX, MEASURED_VIEWPORT_PX);
    expect(answer.virtualized).toBe(false);
    expect(answer.startIndex).toBe(0);
    expect(answer.endIndex).toBe(rows);
    expect(answer.rowsInWindow).toBe(rows);
    expect(answer.rowsBeforePx).toBe(0);
    expect(answer.rowsAfterPx).toBe(0);
  });

  it("takes the first visible row as the FLOOR of the scroll division", () => {
    const answer = diffRowWindowForViewport(
      VIRTUALIZED_ROWS,
      HALF_ROW_SCROLL_PX,
      MEASURED_VIEWPORT_PX,
    );
    expect(answer.startIndex).toBe(HALF_ROW_SCROLL_ROWS - DIFF_VIRTUAL_OVERSCAN_ROWS);
    expect(answer.startIndex).not.toBe(HALF_ROW_SCROLL_ROWS + 1 - DIFF_VIRTUAL_OVERSCAN_ROWS);
  });

  it("takes the visible count as the CEILING of the height division", () => {
    const answer = diffRowWindowForViewport(
      VIRTUALIZED_ROWS,
      HALF_ROW_SCROLL_PX,
      HALF_ROW_VIEWPORT_PX,
    );
    expect(answer.rowsInWindow).toBe(
      HALF_ROW_VIEWPORT_ROWS + 1 + 2 * DIFF_VIRTUAL_OVERSCAN_ROWS,
    );
    expect(answer.rowsInWindow).not.toBe(
      HALF_ROW_VIEWPORT_ROWS + 2 * DIFF_VIRTUAL_OVERSCAN_ROWS,
    );
  });

  it("sizes both spacers as their row count times the row height", () => {
    const answer = diffRowWindowForViewport(
      VIRTUALIZED_ROWS,
      HALF_ROW_SCROLL_PX,
      MEASURED_VIEWPORT_PX,
    );
    expect(answer.rowsBeforePx).toBe(answer.rowsBefore * DIFF_VIRTUAL_ROW_HEIGHT_PX);
    expect(answer.rowsAfterPx).toBe(answer.rowsAfter * DIFF_VIRTUAL_ROW_HEIGHT_PX);
    expect(answer.rowsBeforePx).toBeGreaterThan(0);
    expect(answer.rowsAfterPx).toBeGreaterThan(0);
  });

  it("resolves a hostile SCROLL OFFSET to the top rather than propagating it", () => {
    for (const hostile of HOSTILE_PIXEL_VALUES) {
      const answer: DiffRowViewportWindow = diffRowWindowForViewport(
        VIRTUALIZED_ROWS,
        hostile,
        MEASURED_VIEWPORT_PX,
      );
      expect(answer.startIndex, `scrollTop ${hostile}`).toBe(0);
      expect(answer.rowsBeforePx, `scrollTop ${hostile}`).toBe(0);
      expect(windowSum(answer), `scrollTop ${hostile}`).toBe(VIRTUALIZED_ROWS);
    }
  });

  it("resolves a hostile VIEWPORT HEIGHT through the unmeasured fallback", () => {
    for (const hostile of HOSTILE_PIXEL_VALUES) {
      const answer: DiffRowViewportWindow = diffRowWindowForViewport(
        VIRTUALIZED_ROWS,
        HALF_ROW_SCROLL_PX,
        hostile,
      );
      expect(answer.rowsInWindow, `height ${hostile}`).toBe(
        DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS + 2 * DIFF_VIRTUAL_OVERSCAN_ROWS,
      );
      expect(windowSum(answer), `height ${hostile}`).toBe(VIRTUALIZED_ROWS);
    }
  });

  it("draws a BOUNDED window of a ten-thousand-row diff and accounts for all of it", () => {
    // What this round exists for, asserted at the scale Acceptance names: the
    // drawn row count stays inside one viewport plus its two overscans, while
    // the two spacers and the window still add up to the whole document.
    const answer = diffRowWindowForViewport(
      SCALE_ROWS,
      HALF_ROW_SCROLL_PX,
      MEASURED_VIEWPORT_PX,
    );
    expect(answer.virtualized).toBe(true);
    expect(answer.rowsInWindow).toBeLessThanOrEqual(
      DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS + 2 * DIFF_VIRTUAL_OVERSCAN_ROWS,
    );
    expect(answer.rowsInWindow).toBeLessThan(SCALE_ROWS);
    expect(windowSum(answer)).toBe(SCALE_ROWS);
    expect(answer.rowsBeforePx + answer.rowsAfterPx).toBe(
      (SCALE_ROWS - answer.rowsInWindow) * DIFF_VIRTUAL_ROW_HEIGHT_PX,
    );
  });
});

describe("diffLanguageForPath", () => {
  it("resolves EVERY entry of the supported set from a path bearing its extension", () => {
    // Iterated from the mapping rather than transcribed, so an entry added
    // without a bundle cannot slip through untested.
    const entries = Object.entries(DIFF_SUPPORTED_LANGUAGES);
    expect(entries.length).toBeGreaterThan(0);
    for (const [extension, language] of entries) {
      expect(diffLanguageForPath(`src/sample.${extension}`), extension).toBe(language);
    }
  });

  it("names every language id it claims to support", () => {
    // The one deliberate transcription in this suite, and it is the language
    // IDS, never the extensions: an entry added under a new id turns this red,
    // which is what stops a language shipping with no test naming it.
    expect(new Set(Object.values(DIFF_SUPPORTED_LANGUAGES))).toEqual(
      new Set([
        "typescript",
        "tsx",
        "javascript",
        "jsx",
        "python",
        "json",
        "css",
        "markdown",
        "shell",
        "yaml",
        "toml",
      ]),
    );
  });

  it("folds an UPPER-CASE extension to the same language", () => {
    expect(diffLanguageForPath("App.TSX")).toBe(DIFF_SUPPORTED_LANGUAGES.tsx);
    expect(diffLanguageForPath("apps/ui/src/App.TSX")).toBe(DIFF_SUPPORTED_LANGUAGES.tsx);
  });

  it("reads the LAST dot, and reads it inside the BASENAME", () => {
    expect(diffLanguageForPath("apps/ui/src/api/diffViewModel.test.ts")).toBe(
      DIFF_SUPPORTED_LANGUAGES.ts,
    );
    expect(diffLanguageForPath("a/b.c/d.ts")).toBe(DIFF_SUPPORTED_LANGUAGES.ts);
    expect(diffLanguageForPath("a/b.c/d")).toBeNull();
  });

  it("renders a DOTFILE plain, including one named after a supported extension", () => {
    expect(diffLanguageForPath(".gitignore")).toBeNull();
    expect(diffLanguageForPath("packages/.env")).toBeNull();
    // The discriminating case: `ts` IS supported, so only the dotfile rule keeps
    // a hidden file called `ts` from being highlighted as TypeScript.
    expect(diffLanguageForPath(".ts")).toBeNull();
    expect(diffLanguageForPath("apps/ui/.ts")).toBeNull();
  });

  it("renders a path with NO dot plain", () => {
    expect(diffLanguageForPath("Makefile")).toBeNull();
    expect(diffLanguageForPath("scripts/run")).toBeNull();
  });

  it("renders the EMPTY path plain", () => {
    expect(diffLanguageForPath("")).toBeNull();
  });

  it("renders a path ENDING in a dot plain", () => {
    expect(diffLanguageForPath("trailing.")).toBeNull();
    expect(diffLanguageForPath("a/b/trailing.")).toBeNull();
  });

  it("renders an UNSUPPORTED extension plain", () => {
    expect(DIFF_SUPPORTED_LANGUAGES.rs).toBeUndefined();
    expect(diffLanguageForPath("crates/main.rs")).toBeNull();
    expect(diffLanguageForPath("notes.unknownlanguage")).toBeNull();
  });

  it("renders an extension naming an INHERITED property plain", () => {
    // Finding `R-0731`. These keys are in nobody's mapping, but a plain object
    // literal read by an `undefined` comparison answers them off
    // `Object.prototype` anyway. `toBeNull` rather than a falsy check, because
    // the wrong answers here — the `Object` constructor and `Object.prototype` —
    // are both truthy and both "not undefined".
    for (const inherited of [
      "constructor",
      "__proto__",
      "toString",
      "valueOf",
      "hasOwnProperty",
    ]) {
      expect(diffLanguageForPath(`src/x.${inherited}`), inherited).toBeNull();
    }
  });

  it("never answers a FUNCTION for an inherited extension", () => {
    // The TYPE is asserted separately from the value so that a regression to a
    // prototype value fails here even if `null` is never restored: a language id
    // is a string, and handing a function on to code expecting one is the
    // downstream half of `R-0731`. `constructor` and `__proto__` are the two the
    // defect really reached — the other three survived only because lower-casing
    // turned them into keys nothing inherits.
    expect(typeof diffLanguageForPath("src/x.constructor")).not.toBe("function");
    expect(typeof diffLanguageForPath("src/x.__proto__")).not.toBe("function");
    // `typeof null` is already `"object"`, so the type cannot discriminate the
    // `__proto__` case; identity can, and this is the exact value it answered.
    expect(diffLanguageForPath("src/x.__proto__")).not.toBe(Object.prototype);
  });

  it("builds the supported set with NO prototype to inherit from", () => {
    // The structural half of the fix, asserted where vitest can see it: a
    // mapping keyed by arbitrary external strings has nothing to inherit.
    expect(Object.getPrototypeOf(DIFF_SUPPORTED_LANGUAGES)).toBeNull();
  });
});

/** An importer that RECORDS the language of every call and answers a bundle
 *  named after it. Written here rather than reached for from a mocking library,
 *  because nothing under `apps/ui/src` uses one and this round starts nothing:
 *  counting calls needs a counter, not a framework, and a hand-written counter is
 *  readable at the point of use instead of at the point of configuration.
 *  `tests/ui_contracts/test_diff_view_model.py` holds that line mechanically. */
function countingBundleImporter(): { calls: string[]; importBundle: DiffLanguageBundleImporter } {
  const calls: string[] = [];
  return {
    calls,
    importBundle: (language: string) => {
      calls.push(language);
      return Promise.resolve({ bundleFor: language });
    },
  };
}

/** The same counter, over an importer whose promise REJECTS — a bundle chunk
 *  that did not arrive. */
function rejectingBundleImporter(): { calls: string[]; importBundle: DiffLanguageBundleImporter } {
  const calls: string[] = [];
  return {
    calls,
    importBundle: (language: string) => {
      calls.push(language);
      return Promise.reject(new Error(`no bundle chunk for ${language}`));
    },
  };
}

const PLAIN_PATHS = ["", "Makefile", ".gitignore", "trailing.", "a/b.c/d", "notes.rs"];

describe("loadDiffLanguageBundle", () => {
  beforeEach(() => {
    // The cache is module state, so a test that did not reset it would be reading
    // the previous test's imports.
    resetDiffLanguageBundleCache();
  });

  it("NEVER asks for a bundle when the language is plain", async () => {
    // Acceptance in so many words: "unknown language renders plain WITHOUT a
    // bundle fetch". The count is asserted at exactly zero, not merely falsy,
    // because "did not fetch" is the property and not "answered plain".
    const importer = countingBundleImporter();
    const answer = await loadDiffLanguageBundle("notes.unknownlanguage", importer.importBundle);
    expect(importer.calls.length).toBe(0);
    expect(answer).toEqual({ language: null, bundle: null });
  });

  it("asks for no bundle for ANY kind of plain path", async () => {
    const importer = countingBundleImporter();
    for (const plain of PLAIN_PATHS) {
      const answer = await loadDiffLanguageBundle(plain, importer.importBundle);
      expect(answer, `plain path ${JSON.stringify(plain)}`).toEqual({
        language: null,
        bundle: null,
      });
    }
    expect(importer.calls.length).toBe(0);
  });

  it("asks for NO bundle for an extension naming an INHERITED property", async () => {
    // THE POINT OF FINDING `R-0731`, and the reason it is Medium rather than
    // cosmetic: with the old plain-literal mapping this call really did reach
    // the importer — the counter read 1 — for a file Acceptance says renders
    // plain WITHOUT a bundle fetch. The count is asserted at exactly zero, the
    // same way the ordinary unknown-extension case is.
    const importer = countingBundleImporter();
    for (const path of ["src/x.constructor", "src/x.__proto__"]) {
      const answer = await loadDiffLanguageBundle(path, importer.importBundle);
      expect(answer, path).toEqual({ language: null, bundle: null });
    }
    expect(importer.calls).toEqual([]);
    expect(importer.calls.length).toBe(0);
  });

  it("imports a supported language EXACTLY once and answers its bundle", async () => {
    const importer = countingBundleImporter();
    const answer = await loadDiffLanguageBundle("apps/ui/src/main.ts", importer.importBundle);
    expect(importer.calls).toEqual([DIFF_SUPPORTED_LANGUAGES.ts]);
    expect(answer.language).toBe(DIFF_SUPPORTED_LANGUAGES.ts);
    expect(answer.bundle).toEqual({ bundleFor: DIFF_SUPPORTED_LANGUAGES.ts });
  });

  it("imports ONE bundle per language however many files ask for it", async () => {
    const importer = countingBundleImporter();
    const first = await loadDiffLanguageBundle("a.ts", importer.importBundle);
    const second = await loadDiffLanguageBundle("b/c.ts", importer.importBundle);
    expect(importer.calls.length).toBe(1);
    expect(second.bundle).toBe(first.bundle);
  });

  it("degrades a REJECTING import to plain, still reporting the language", async () => {
    const importer = rejectingBundleImporter();
    const answer = await loadDiffLanguageBundle("main.py", importer.importBundle);
    expect(answer).toEqual({ language: DIFF_SUPPORTED_LANGUAGES.py, bundle: null });
    expect(importer.calls.length).toBe(1);
  });

  it("degrades a THROWING import to plain in the same way", async () => {
    const calls: string[] = [];
    const importBundle: DiffLanguageBundleImporter = (language: string) => {
      calls.push(language);
      throw new Error("bundle chunk missing");
    };
    const answer = await loadDiffLanguageBundle("main.py", importBundle);
    expect(answer).toEqual({ language: DIFF_SUPPORTED_LANGUAGES.py, bundle: null });
    expect(calls.length).toBe(1);
  });

  it("RETRIES a language whose import failed rather than caching the failure", async () => {
    const failing = rejectingBundleImporter();
    const failed = await loadDiffLanguageBundle("main.py", failing.importBundle);
    expect(failed.bundle).toBeNull();
    const succeeding = countingBundleImporter();
    const retried = await loadDiffLanguageBundle("main.py", succeeding.importBundle);
    expect(succeeding.calls.length).toBe(1);
    expect(retried.bundle).toEqual({ bundleFor: DIFF_SUPPORTED_LANGUAGES.py });
  });

  it("really forgets what it loaded when the cache is reset", async () => {
    const importer = countingBundleImporter();
    await loadDiffLanguageBundle("a.css", importer.importBundle);
    await loadDiffLanguageBundle("a.css", importer.importBundle);
    expect(importer.calls.length).toBe(1);
    resetDiffLanguageBundleCache();
    await loadDiffLanguageBundle("a.css", importer.importBundle);
    expect(importer.calls.length).toBe(2);
  });
});

/** The Acceptance size of F037's budget, counted in BODY LINES, and deliberately
 *  the SAME ten thousand `SCALE_ROWS` above counts in rows: one number for one
 *  scale, so the window tests and the row-model tests cannot drift apart. */
const ACCEPTANCE_BODY_LINES = SCALE_ROWS;

/** The arithmetic `buildDiffRowModels` performs, written as an expression over
 *  the fixture's shape rather than as a literal somebody counted once: one file
 *  row, one hunk-head row, and one row per body line of an OPEN hunk. */
const ROWS_PER_FILE = 1;
const ROWS_PER_HUNK_HEAD = 1;
const ACCEPTANCE_ROW_COUNT =
  ACCEPTANCE_BODY_LINES + ROWS_PER_FILE + ROWS_PER_HUNK_HEAD;

/** Builds taken per recording, ODD so the median is a duration a build really
 *  took rather than the mean of the two either side of the middle. */
const BUILD_SAMPLE_COUNT = 7;

/** THE TRAP DECISION F256 D5 RECORDS, and the reason every measurement below
 *  passes THIS set. `defaultCollapsedHunkIds` collapses a hunk of ten thousand
 *  lines, and a collapsed hunk emits NO line rows, so the natural spelling —
 *  build the default set, then build the rows — returns two rows however large
 *  the fixture is and times nothing. The last test of this block pins that fact
 *  so a reader meets it as an assertion rather than as a surprise. */
const NOTHING_COLLAPSED: ReadonlySet<string> = new Set<string>();

/** The viewport a panel reports on its FIRST render: not measured yet, so both
 *  numbers are zero and `diffRowWindowForViewport` falls back to
 *  `DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS`. That is the state a ten-thousand-line
 *  diff is really first drawn in, which is why the bounded-window guard is taken
 *  there rather than at a height no first paint ever has. */
const UNMEASURED_SCROLL_PX = 0;
const UNMEASURED_VIEWPORT_PX = 0;

/** Ten times the Acceptance document, which is the whole point of the guard: the
 *  drawn row count must NOT follow it. */
const TENFOLD = 10;

/** How far below the document the drawn window must sit, as a FACTOR rather than
 *  a row count, so "far below" stays a statement about the two numbers instead of
 *  a literal that would need re-deciding whenever either of them moves. */
const FAR_BELOW_FACTOR = 100;

/** The median of an ODD-length sample list, as the middle sample after sorting —
 *  a sample rather than an interpolation, so every duration recorded below is one
 *  a build really took. */
function medianOf(samples: number[]): number {
  const sorted = [...samples].sort((left, right) => left - right);
  return sorted[(sorted.length - 1) / 2];
}

describe("the ten-thousand-line diff through the client model", () => {
  it("builds every row of the Acceptance fixture, and RECORDS what that costs", () => {
    // The CLIENT half of the figure F037's Acceptance asks to have RECORDED,
    // matching the server half `test_the_acceptance_fixture_is_served_inside_the_hang_net`
    // records in `tests/ui_server/test_diff_endpoint.py`.
    //
    // MEASURED 2026-08-28 on the machine this feature is being built on — a Linux
    // x86-64 development workstation, Node v22 under vitest, unloaded — as the
    // median of seven builds of one file and one hunk of 10,000 body lines with
    // NOTHING collapsed: MEDIAN 0.678 ms, minimum 0.271 ms, maximum 1.408 ms, for
    // 10,002 rows. The spread is the interesting half: fastest to slowest inside
    // ONE run differs by more than a factor of five, which is a millisecond of JS
    // being mostly the JIT deciding whether to compile.
    //
    // NOTHING HERE IS ASSERTED ABOUT THE DURATION, by DECISION F256 D5. The
    // fastest and slowest samples of the run recorded above differ by more than
    // fivefold, and that is the JIT deciding whether to compile rather than the
    // code doing more or less work, so a bound on it would report the machine
    // and its warm-up rather than this module. What IS asserted is
    // the WORK: a measurement of an empty answer is not a measurement, and the
    // row count is the one number that says the ten thousand lines were really
    // walked. The exact, machine-independent guard is the test below this one.
    const envelope = envelopeWithHunkOf(ACCEPTANCE_BODY_LINES);
    const samples: number[] = [];
    let rows: DiffRowModel[] = [];
    for (let build = 0; build < BUILD_SAMPLE_COUNT; build += 1) {
      const startedAt = performance.now();
      rows = buildDiffRowModels(envelope, NOTHING_COLLAPSED);
      samples.push(performance.now() - startedAt);
    }
    // PRINTED because "recorded" is half of what Acceptance asks for: a run of
    // this block reports the figures the comments carry, so re-recording them
    // after a change needs no edit here. vitest captures it, so a green run shows
    // nothing; `--reporter=verbose` or a failing file surfaces it.
    console.log(
      `F256 T002 rowModel@${ACCEPTANCE_BODY_LINES}: `
      + `median ${medianOf(samples).toFixed(3)}ms `
      + `min ${Math.min(...samples).toFixed(3)}ms `
      + `max ${Math.max(...samples).toFixed(3)}ms rows ${rows.length}`);

    expect(samples, "durations recorded").toHaveLength(BUILD_SAMPLE_COUNT);
    expect(
      rows,
      `rows built from ${ACCEPTANCE_BODY_LINES} body lines, against `
      + `${ACCEPTANCE_BODY_LINES} + ${ROWS_PER_FILE} + ${ROWS_PER_HUNK_HEAD}`,
    ).toHaveLength(ACCEPTANCE_ROW_COUNT);
    expect(
      rows.filter((row) => row.kind === "line"),
      `line rows built from ${ACCEPTANCE_BODY_LINES} body lines`,
    ).toHaveLength(ACCEPTANCE_BODY_LINES);
  });

  it("draws the SAME bounded window at ten times the Acceptance size", () => {
    // THE PROPERTY THAT MAKES A TEN-THOUSAND-LINE DIFF VIABLE AT ALL, and the
    // reason DECISION F256 D5 guards the client half with this rather than with a
    // duration: what would make the viewer unusable is drawing ten thousand rows,
    // not the sub-millisecond list build the test above records. It is decided by
    // `DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS` and `DIFF_VIRTUAL_OVERSCAN_ROWS` and by
    // nothing about the document, so it is the same integer on every machine and
    // in every run — an exact invariant where the duration above is a report.
    //
    // MEASURED 2026-08-28 in the same run as the recording above: 48 rows drawn at
    // 10,002 and 48 drawn at 100,020.
    const tenfoldRowCount = ACCEPTANCE_ROW_COUNT * TENFOLD;
    const acceptance = diffRowWindowForViewport(
      ACCEPTANCE_ROW_COUNT,
      UNMEASURED_SCROLL_PX,
      UNMEASURED_VIEWPORT_PX,
    );
    const tenfold = diffRowWindowForViewport(
      tenfoldRowCount,
      UNMEASURED_SCROLL_PX,
      UNMEASURED_VIEWPORT_PX,
    );
    console.log(
      `F256 T002 rowWindow: ${acceptance.rowsInWindow} drawn@${ACCEPTANCE_ROW_COUNT} `
      + `${tenfold.rowsInWindow} drawn@${tenfoldRowCount}`);

    expect(acceptance.virtualized, `${ACCEPTANCE_ROW_COUNT} rows`).toBe(true);
    expect(tenfold.virtualized, `${tenfoldRowCount} rows`).toBe(true);
    expect(
      tenfold.rowsInWindow,
      `${acceptance.rowsInWindow} rows drawn at ${ACCEPTANCE_ROW_COUNT} against `
      + `${tenfold.rowsInWindow} at ${tenfoldRowCount}: the drawn window must not `
      + `grow with the document`,
    ).toBe(acceptance.rowsInWindow);
    expect(
      acceptance.rowsInWindow,
      `${acceptance.rowsInWindow} rows drawn at ${ACCEPTANCE_ROW_COUNT}, against `
      + `the two constants that decide it`,
    ).toBe(DIFF_VIRTUAL_DEFAULT_VIEWPORT_ROWS + DIFF_VIRTUAL_OVERSCAN_ROWS);
    expect(
      acceptance.rowsInWindow * FAR_BELOW_FACTOR,
      `${acceptance.rowsInWindow} rows drawn of ${ACCEPTANCE_ROW_COUNT}, which is `
      + `not ${FAR_BELOW_FACTOR} times smaller`,
    ).toBeLessThan(ACCEPTANCE_ROW_COUNT);
    expect(windowSum(acceptance), `${ACCEPTANCE_ROW_COUNT} rows accounted for`)
      .toBe(ACCEPTANCE_ROW_COUNT);
    expect(windowSum(tenfold), `${tenfoldRowCount} rows accounted for`)
      .toBe(tenfoldRowCount);
  });

  it("paints the Acceptance fixture as TWO rows until the reader expands the hunk", () => {
    // THE VIEWER'S FIRST PAINT OF A TEN-THOUSAND-LINE DIFF, which is two rows: the
    // single hunk arrives COLLAPSED, because ten thousand is past
    // `DIFF_HUNK_COLLAPSE_THRESHOLD_LINES`, and a collapsed hunk emits its head
    // row and none of its lines. The ten thousand arrive only when the reader
    // expands it, and THAT is the build the recording test above measures. Pinned
    // here because it is both a real product fact and the trap that makes the
    // obvious client benchmark vacuous — see DECISION F256 D5.
    //
    // MEASURED 2026-08-28 in the same run as the two above: a collapsed set of 1,
    // 2 rows at first paint, 10,002 once expanded.
    const envelope = envelopeWithHunkOf(ACCEPTANCE_BODY_LINES);
    const collapsedByDefault = defaultCollapsedHunkIds(envelope);
    const firstPaint = buildDiffRowModels(envelope, collapsedByDefault);
    const expanded = buildDiffRowModels(envelope, NOTHING_COLLAPSED);
    console.log(
      `F256 T002 firstPaint@${ACCEPTANCE_BODY_LINES}: collapsed set `
      + `${collapsedByDefault.size} rows ${firstPaint.length} `
      + `expanded ${expanded.length}`);

    expect(
      collapsedByDefault.size,
      `hunks collapsed by default at ${ACCEPTANCE_BODY_LINES} body lines`,
    ).toBe(1);
    expect(firstPaint.map((row) => row.kind)).toEqual(["file", "hunkHead"]);
    expect(
      firstPaint,
      `rows drawn at first paint of ${ACCEPTANCE_BODY_LINES} body lines`,
    ).toHaveLength(ROWS_PER_FILE + ROWS_PER_HUNK_HEAD);
    expect(
      expanded,
      `rows drawn once the hunk of ${ACCEPTANCE_BODY_LINES} lines is expanded`,
    ).toHaveLength(ACCEPTANCE_ROW_COUNT);
  });
});
