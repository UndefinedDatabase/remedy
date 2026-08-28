import { describe, it, expect } from "vitest";
import {
  DIFF_HUNK_COLLAPSE_THRESHOLD_LINES,
  buildDiffFileSummaries,
  buildDiffRowModels,
  defaultCollapsedHunkIds,
  readDiffEnvelope,
  splitLineIntoIntralineSegments,
  toggleHunkCollapse,
} from "./diffViewModel";
import type {
  DiffEnvelope,
  DiffIntralineSpan,
  DiffLine,
  DiffLineSegment,
} from "./diffViewModel";

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
    version: 1,
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
    version: 1,
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
            id: "0:0",
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
    version: 1,
    scope: "task",
    task_id: "t-1",
    source: "runs/r-1/workspace.diff",
    available: true,
    reason: null,
    truncated: false,
    task_run_ids: ["r-1", "r-2"],
    files: [wireFile("a.py", [wireHunk("0:0", 2)])],
  };
}

/** An envelope with one file and one hunk of `count` lines, already read. */
function envelopeWithHunkOf(count: number): DiffEnvelope {
  return readDiffEnvelope(wireEnvelope([wireFile("a.py", [wireHunk("0:0", count)])]));
}

describe("readDiffEnvelope", () => {
  it("reads the wire's snake_case and the app's camelCase to the same envelope", () => {
    expect(readDiffEnvelope(snakePayload())).toEqual(readDiffEnvelope(camelPayload()));
  });

  it("carries every field of a well-formed payload through unchanged", () => {
    const envelope = readDiffEnvelope(snakePayload());
    expect(envelope.available).toBe(true);
    expect(envelope.version).toBe(1);
    expect(envelope.scope).toBe("task");
    expect(envelope.taskId).toBe("t-1");
    expect(envelope.source).toBe("runs/r-1/workspace.diff");
    expect(envelope.taskRunIds).toEqual(["r-1", "r-2"]);
    expect(envelope.files).toHaveLength(1);
    expect(envelope.files[0].path).toBe("a.py");
    expect(envelope.files[0].stats).toEqual({ added: 2, deleted: 1 });
    expect(envelope.files[0].hunks[0].id).toBe("0:0");
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
          id: "0:0",
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
          id: "0:0",
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

  it("gives a hunk with no usable id the position the parser would have given it", () => {
    const noId = wireEnvelope([wireFile("a.py", [{ header: "@@ @@", lines: [] }])]);
    expect(readDiffEnvelope(noId).files[0].hunks[0].id).toBe("0:0");
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
    expect(defaultCollapsedHunkIds(envelope).has("0:0")).toBe(false);
  });

  it("collapses a hunk one line past the threshold", () => {
    const envelope = envelopeWithHunkOf(DIFF_HUNK_COLLAPSE_THRESHOLD_LINES + 1);
    expect(defaultCollapsedHunkIds(envelope).has("0:0")).toBe(true);
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
    const before = new Set(["0:0"]);
    const opened = toggleHunkCollapse(before, "0:0");
    expect(opened.has("0:0")).toBe(false);
    expect(before.has("0:0")).toBe(true);
    expect(opened).not.toBe(before);
  });

  it("adds a hunk that was not collapsed and leaves the others alone", () => {
    const before = new Set(["0:0"]);
    const next = toggleHunkCollapse(before, "1:0");
    expect(next.has("1:0")).toBe(true);
    expect(next.has("0:0")).toBe(true);
    expect(before.size).toBe(1);
  });

  it("round-trips a hunk back to where it started", () => {
    const before = new Set<string>();
    expect(toggleHunkCollapse(toggleHunkCollapse(before, "0:0"), "0:0").size).toBe(0);
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
    const rows = buildDiffRowModels(envelope, new Set(["0:0"]));
    expect(rows.map((row) => row.kind)).toEqual(["file", "hunkHead"]);
  });

  it("says on the head row how many lines a collapsed hunk is hiding", () => {
    const envelope = readDiffEnvelope(snakePayload());
    const [, head] = buildDiffRowModels(envelope, new Set(["0:0"]));
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
        wireFile("a.py", [wireHunk("0:0", 3), wireHunk("0:1", 2)]),
        wireFile("b.py", [wireHunk("1:0", 4)]),
      ]),
    );
    const rows = buildDiffRowModels(envelope, new Set<string>());
    const keys = rows.map((row) => row.key);
    expect(new Set(keys).size).toBe(keys.length);
  });

  it("keeps the keys of the rows that survive a collapse unchanged", () => {
    const envelope = readDiffEnvelope(
      wireEnvelope([wireFile("a.py", [wireHunk("0:0", 2), wireHunk("0:1", 2)])]),
    );
    const open = buildDiffRowModels(envelope, new Set<string>());
    const half = buildDiffRowModels(envelope, new Set(["0:1"]));
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
      wireEnvelope([wireFile("z.py", [wireHunk("0:0", 1)]), wireFile("a.py", [])]),
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
        wireFile("a.py", [wireHunk("0:0", 3), wireHunk("0:1", 2)]),
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
      wireEnvelope([wireFile("a.py", [wireHunk("0:0", 1)]), wireFile("b.py", [])]),
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
