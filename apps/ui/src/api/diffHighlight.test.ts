import { describe, it, expect } from "vitest";
import {
  DIFF_HIGHLIGHT_TOKEN_KINDS,
  composeHighlightedRuns,
  tokenizeDiffLine,
} from "./diffHighlight";
import type {
  DiffHighlightGrammar,
  DiffHighlightRun,
  DiffHighlightSegment,
  DiffHighlightTokenKind,
  DiffMarkedSegment,
} from "./diffHighlight";
import {
  DIFF_HIGHLIGHT_GRAMMARS,
  diffHighlightGrammarFor,
} from "./diffHighlightGrammars";

/** The three grammars the tables below are named against, resolved through
 *  `diffHighlightGrammarFor` rather than transcribed: a grammar written out here
 *  would agree with itself after the real table changed. */
const TYPESCRIPT_GRAMMAR = diffHighlightGrammarFor("typescript");
const PYTHON_GRAMMAR = diffHighlightGrammarFor("python");
const MARKDOWN_GRAMMAR = diffHighlightGrammarFor("markdown");

/** One row of the concatenation table: the GRAMMAR a line is scanned under —
 *  never a language id, because `tokenizeDiffLine` no longer takes one — and a
 *  line written to exercise that grammar's comment, string, number and keyword
 *  rules at once. `language` is carried beside it only so a reader can see which
 *  id the grammar came from. */
interface HighlightCase {
  language: string | null;
  grammar: DiffHighlightGrammar | null;
  line: string;
}

/** Builds one row by RESOLVING the id, which is what keeps the two unknown ids
 *  below honest: `diffHighlightGrammarFor` answers `null` for them itself, so
 *  the unknown-language cases carry a real `null` rather than a claimed one. */
function highlightCase(language: string | null, line: string): HighlightCase {
  return { language, grammar: diffHighlightGrammarFor(language), line };
}

/** A line per grammar, plus the two shapes no grammar owns. Every case here is
 *  checked against the S7 invariant rather than against an expected token list,
 *  because the invariant is what a reader of a changed line depends on. */
const CONCATENATION_CASES: readonly HighlightCase[] = [
  highlightCase("typescript", 'const x: number = 42; // a "quoted" tail'),
  highlightCase("tsx", 'return <div className="row">{count + 1}</div>;'),
  highlightCase("javascript", "let total = 7 + count; // sum"),
  highlightCase("jsx", "export default function Row() { return null; }"),
  highlightCase("python", 'def run(x=3):  # comment with \'quote\'\n'),
  highlightCase("python", '"""a docstring on one line""" + str(9)'),
  highlightCase("json", '{"enabled": true, "count": 12, "name": "a\\"b"}'),
  highlightCase("css", ".row { display: flex; margin: 0 8px; }"),
  highlightCase("markdown", "# Heading with `code` and 3 items"),
  highlightCase("shell", "if [ -n \"$1\" ]; then exit 0; fi # done"),
  highlightCase("yaml", "enabled: true  # 2 spaces before the comment"),
  highlightCase("toml", 'name = "remedy"  # version 3'),
  highlightCase("haskell", "main = putStrLn \"hi\" -- 5"),
  highlightCase(null, 'const x = "unhighlighted"; // still whole'),
];

/** The joined `text` of every segment, which S7 requires to equal the input. */
function joinSegments(segments: readonly DiffHighlightSegment[]): string {
  return segments.map((segment) => segment.text).join("");
}

describe("diffHighlightGrammarFor", () => {
  it("answers a grammar for every id the tables own and null for null", () => {
    for (const language of Object.keys(DIFF_HIGHLIGHT_GRAMMARS)) {
      expect(diffHighlightGrammarFor(language)).toBe(DIFF_HIGHLIGHT_GRAMMARS[language]);
    }
    expect(diffHighlightGrammarFor(null)).toBeNull();
    expect(diffHighlightGrammarFor("haskell")).toBeNull();
    expect(diffHighlightGrammarFor("")).toBeNull();
  });

  it("treats inherited property names as unowned ids rather than reaching an inherited value", () => {
    // Finding `R-0731` at its new home: the tables moved to
    // `./diffHighlightGrammars`, and this is the property that moved with them.
    // A language id arrives inside a diff path from a repository this viewer does
    // not control, so each of these four is an ordinary string and each must
    // answer `null` — a mapping with a prototype would hand back a function.
    for (const language of ["constructor", "__proto__", "toString", "hasOwnProperty"]) {
      expect(diffHighlightGrammarFor(language)).toBeNull();
      expect(tokenizeDiffLine("const x = 1;", diffHighlightGrammarFor(language))).toEqual([
        { text: "const x = 1;", kind: "plain" },
      ]);
    }
  });
});

describe("tokenizeDiffLine", () => {
  it("reproduces the input exactly when the segments are joined, for every grammar and for an unknown language", () => {
    for (const testCase of CONCATENATION_CASES) {
      const segments = tokenizeDiffLine(testCase.line, testCase.grammar);
      expect(joinSegments(segments)).toBe(testCase.line);
    }
  });

  it("reproduces the input exactly for every declared grammar key over a hostile line", () => {
    const hostile = "a\\\"b'c`d#e//f 0123 _x$y\t{[(<>)]}\\";
    for (const language of Object.keys(DIFF_HIGHLIGHT_GRAMMARS)) {
      const segments = tokenizeDiffLine(hostile, diffHighlightGrammarFor(language));
      expect(joinSegments(segments)).toBe(hostile);
    }
  });

  it("returns the whole line plain for a null grammar", () => {
    expect(tokenizeDiffLine("const x = 1;", null)).toEqual([
      { text: "const x = 1;", kind: "plain" },
    ]);
  });

  it("produces every token kind the closed set names", () => {
    const produced = new Set<DiffHighlightTokenKind>();
    const inputs: readonly HighlightCase[] = [
      highlightCase("typescript", "// a comment"),
      highlightCase("typescript", '"a string"'),
      highlightCase("typescript", "12345"),
      highlightCase("typescript", "const"),
      highlightCase("typescript", "+++"),
    ];
    for (const testCase of inputs) {
      for (const segment of tokenizeDiffLine(testCase.line, testCase.grammar)) {
        produced.add(segment.kind);
      }
    }
    for (const kind of DIFF_HIGHLIGHT_TOKEN_KINDS) {
      expect(produced.has(kind)).toBe(true);
    }
  });

  it("merges adjacent plain runs so no two consecutive segments both carry plain", () => {
    const segments = tokenizeDiffLine("zz + qq ?? ww", TYPESCRIPT_GRAMMAR);
    expect(joinSegments(segments)).toBe("zz + qq ?? ww");
    expect(segments).toEqual([{ text: "zz + qq ?? ww", kind: "plain" }]);
    const mixed = tokenizeDiffLine("aa 1 bb", TYPESCRIPT_GRAMMAR);
    expect(mixed).toEqual([
      { text: "aa ", kind: "plain" },
      { text: "1", kind: "number" },
      { text: " bb", kind: "plain" },
    ]);
    for (let index = 1; index < mixed.length; index += 1) {
      expect(mixed[index].kind === "plain" && mixed[index - 1].kind === "plain").toBe(
        false,
      );
    }
  });

  it("ends an unterminated string at the end of the line", () => {
    const line = 'const greeting = "never closed';
    const segments = tokenizeDiffLine(line, TYPESCRIPT_GRAMMAR);
    expect(joinSegments(segments)).toBe(line);
    const last = segments[segments.length - 1];
    expect(last.kind).toBe("string");
    expect(last.text).toBe('"never closed');
  });

  it("is total over the empty string, a whitespace-only line and a lone delimiter", () => {
    expect(tokenizeDiffLine("", TYPESCRIPT_GRAMMAR)).toEqual([]);
    expect(tokenizeDiffLine("", null)).toEqual([]);
    expect(tokenizeDiffLine("   \t ", PYTHON_GRAMMAR)).toEqual([
      { text: "   \t ", kind: "plain" },
    ]);
    expect(tokenizeDiffLine('"', TYPESCRIPT_GRAMMAR)).toEqual([
      { text: '"', kind: "string" },
    ]);
    expect(tokenizeDiffLine("'", PYTHON_GRAMMAR)).toEqual([{ text: "'", kind: "string" }]);
    expect(tokenizeDiffLine("`", MARKDOWN_GRAMMAR)).toEqual([
      { text: "`", kind: "string" },
    ]);
  });
});

/** One row of the composition table: the GRAMMAR the line is scanned under and
 *  the intraline cut of one line, in the shape `splitLineIntoIntralineSegments`
 *  returns it. The table covers all three ways the two cuts can meet — a marked
 *  run INSIDE a token, a token INSIDE a marked run, and boundaries crossing at an
 *  offset belonging to neither cut — because those are the cases a merge of two
 *  run lists gets wrong. */
interface CompositionCase {
  grammar: DiffHighlightGrammar | null;
  segments: readonly DiffMarkedSegment[];
}

const COMPOSITION_CASES: readonly CompositionCase[] = [
  // a marked run strictly inside one `string` token
  {
    grammar: diffHighlightGrammarFor("typescript"),
    segments: [
      { text: 'const label = "hello ', marked: false },
      { text: "world", marked: true },
      { text: '";', marked: false },
    ],
  },
  // the `number` and `keyword` tokens strictly inside one marked run
  {
    grammar: diffHighlightGrammarFor("typescript"),
    segments: [
      { text: "let ", marked: false },
      { text: "total = 42 + rest", marked: true },
      { text: ";", marked: false },
    ],
  },
  // both boundaries fall inside a token: the marked cut opens mid-`def` and
  // closes inside the trailing comment, so neither cut owns either offset
  {
    grammar: diffHighlightGrammarFor("python"),
    segments: [
      { text: "de", marked: true },
      { text: "f run(x=3):  # ta", marked: false },
      { text: "il", marked: true },
    ],
  },
  {
    grammar: diffHighlightGrammarFor("json"),
    segments: [{ text: '{"count": 12}', marked: true }],
  },
  {
    grammar: diffHighlightGrammarFor("css"),
    segments: [{ text: ".row { display: flex; }", marked: false }],
  },
  {
    grammar: diffHighlightGrammarFor("shell"),
    segments: [
      { text: "if [ ", marked: true },
      { text: '-n "$1" ', marked: false },
      { text: "];", marked: true },
      { text: " then exit 0; fi # done", marked: false },
    ],
  },
  // `haskell` is an id no table owns, so this row's grammar really is `null`
  {
    grammar: diffHighlightGrammarFor("haskell"),
    segments: [
      { text: "main = putStrLn ", marked: false },
      { text: '"hi"', marked: true },
      { text: " -- 5", marked: false },
    ],
  },
  {
    grammar: null,
    segments: [
      { text: "const x = ", marked: true },
      { text: '"unhighlighted"; // whole', marked: false },
    ],
  },
];

/** The joined `text` of every run, which S6(a) requires to equal the joined
 *  input. */
function joinRuns(runs: readonly DiffHighlightRun[]): string {
  return runs.map((run) => run.text).join("");
}

/** The whole line the intraline cut describes. */
function joinMarkedSegments(segments: readonly DiffMarkedSegment[]): string {
  return segments.map((segment) => segment.text).join("");
}

/** The `marked` flag per CHARACTER, read off the input segments — the reference
 *  S6(b) compares the composed runs against. */
function markedPerCharacter(segments: readonly DiffMarkedSegment[]): boolean[] {
  const flags: boolean[] = [];
  for (const segment of segments) {
    for (let offset = 0; offset < segment.text.length; offset += 1) {
      flags.push(segment.marked);
    }
  }
  return flags;
}

/** The token `kind` per CHARACTER, read off `tokenizeDiffLine` itself — the
 *  reference S6(c) compares the composed runs against, so the test cannot drift
 *  from the tokenizer it is pinning against. */
function kindPerCharacter(
  line: string,
  grammar: DiffHighlightGrammar | null,
): DiffHighlightTokenKind[] {
  const kinds: DiffHighlightTokenKind[] = [];
  for (const segment of tokenizeDiffLine(line, grammar)) {
    for (let offset = 0; offset < segment.text.length; offset += 1) {
      kinds.push(segment.kind);
    }
  }
  return kinds;
}

/** The composed runs expanded back to one entry per character, which is how both
 *  per-position invariants are checked without assuming a run layout. */
function runsPerCharacter(
  runs: readonly DiffHighlightRun[],
): { marked: boolean; kind: DiffHighlightTokenKind }[] {
  const cells: { marked: boolean; kind: DiffHighlightTokenKind }[] = [];
  for (const run of runs) {
    for (let offset = 0; offset < run.text.length; offset += 1) {
      cells.push({ marked: run.marked, kind: run.kind });
    }
  }
  return cells;
}

describe("composeHighlightedRuns", () => {
  it("reproduces the joined segments exactly when the returned runs are joined", () => {
    for (const testCase of COMPOSITION_CASES) {
      const line = joinMarkedSegments(testCase.segments);
      const runs = composeHighlightedRuns(testCase.segments, testCase.grammar);
      expect(joinRuns(runs)).toBe(line);
    }
  });

  it("gives every character the marked flag of the input segment covering it", () => {
    for (const testCase of COMPOSITION_CASES) {
      const runs = composeHighlightedRuns(testCase.segments, testCase.grammar);
      const cells = runsPerCharacter(runs);
      const expected = markedPerCharacter(testCase.segments);
      expect(cells.length).toBe(expected.length);
      expect(cells.map((cell) => cell.marked)).toEqual(expected);
    }
  });

  it("gives every character the kind tokenizeDiffLine gives that position for the same grammar", () => {
    for (const testCase of COMPOSITION_CASES) {
      const line = joinMarkedSegments(testCase.segments);
      const runs = composeHighlightedRuns(testCase.segments, testCase.grammar);
      const cells = runsPerCharacter(runs);
      const expected = kindPerCharacter(line, testCase.grammar);
      expect(cells.length).toBe(expected.length);
      expect(cells.map((cell) => cell.kind)).toEqual(expected);
    }
  });

  it("merges adjacent runs that agree on both marked and kind", () => {
    for (const testCase of COMPOSITION_CASES) {
      const runs = composeHighlightedRuns(testCase.segments, testCase.grammar);
      for (let index = 1; index < runs.length; index += 1) {
        expect(
          runs[index].marked === runs[index - 1].marked &&
            runs[index].kind === runs[index - 1].kind,
        ).toBe(false);
      }
    }
    expect(
      composeHighlightedRuns(
        [
          { text: "aa ", marked: false },
          { text: "bb", marked: false },
        ],
        TYPESCRIPT_GRAMMAR,
      ),
    ).toEqual([{ text: "aa bb", marked: false, kind: "plain" }]);
    expect(
      composeHighlightedRuns(
        [
          { text: "let ", marked: false },
          { text: "n = ", marked: true },
          { text: "9", marked: true },
        ],
        TYPESCRIPT_GRAMMAR,
      ),
    ).toEqual([
      { text: "let", marked: false, kind: "keyword" },
      { text: " ", marked: false, kind: "plain" },
      { text: "n = ", marked: true, kind: "plain" },
      { text: "9", marked: true, kind: "number" },
    ]);
  });

  it("is total over an empty list and over segments whose texts are all empty", () => {
    expect(composeHighlightedRuns([], TYPESCRIPT_GRAMMAR)).toEqual([]);
    expect(composeHighlightedRuns([], null)).toEqual([]);
    expect(composeHighlightedRuns([{ text: "", marked: true }], PYTHON_GRAMMAR)).toEqual(
      [],
    );
    expect(
      composeHighlightedRuns(
        [
          { text: "", marked: false },
          { text: "", marked: true },
        ],
        null,
      ),
    ).toEqual([]);
  });

  it("returns every run plain for an unowned language while the marked flags survive unchanged", () => {
    const segments: readonly DiffMarkedSegment[] = [
      { text: "fn main() { ", marked: false },
      { text: 'println!("hi 42")', marked: true },
      { text: " } // tail", marked: false },
    ];
    for (const language of ["rust", "constructor", "__proto__", ""]) {
      const runs = composeHighlightedRuns(segments, diffHighlightGrammarFor(language));
      expect(joinRuns(runs)).toBe(joinMarkedSegments(segments));
      expect(runs.every((run) => run.kind === "plain")).toBe(true);
      expect(runsPerCharacter(runs).map((cell) => cell.marked)).toEqual(
        markedPerCharacter(segments),
      );
    }
  });
});
