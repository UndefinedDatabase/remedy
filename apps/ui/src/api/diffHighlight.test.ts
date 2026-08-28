import { describe, it, expect } from "vitest";
import {
  DIFF_HIGHLIGHT_GRAMMARS,
  DIFF_HIGHLIGHT_TOKEN_KINDS,
  tokenizeDiffLine,
} from "./diffHighlight";
import type { DiffHighlightSegment, DiffHighlightTokenKind } from "./diffHighlight";

/** One row of the concatenation table: a language id and a line written to
 *  exercise that grammar's comment, string, number and keyword rules at once. */
interface HighlightCase {
  language: string | null;
  line: string;
}

/** A line per grammar, plus the two shapes no grammar owns. Every case here is
 *  checked against the S7 invariant rather than against an expected token list,
 *  because the invariant is what a reader of a changed line depends on. */
const CONCATENATION_CASES: readonly HighlightCase[] = [
  { language: "typescript", line: 'const x: number = 42; // a "quoted" tail' },
  { language: "tsx", line: 'return <div className="row">{count + 1}</div>;' },
  { language: "javascript", line: "let total = 7 + count; // sum" },
  { language: "jsx", line: "export default function Row() { return null; }" },
  { language: "python", line: 'def run(x=3):  # comment with \'quote\'\n' },
  { language: "python", line: '"""a docstring on one line""" + str(9)' },
  { language: "json", line: '{"enabled": true, "count": 12, "name": "a\\"b"}' },
  { language: "css", line: ".row { display: flex; margin: 0 8px; }" },
  { language: "markdown", line: "# Heading with `code` and 3 items" },
  { language: "shell", line: "if [ -n \"$1\" ]; then exit 0; fi # done" },
  { language: "yaml", line: "enabled: true  # 2 spaces before the comment" },
  { language: "toml", line: 'name = "remedy"  # version 3' },
  { language: "haskell", line: "main = putStrLn \"hi\" -- 5" },
  { language: null, line: 'const x = "unhighlighted"; // still whole' },
];

/** The joined `text` of every segment, which S7 requires to equal the input. */
function joinSegments(segments: readonly DiffHighlightSegment[]): string {
  return segments.map((segment) => segment.text).join("");
}

describe("tokenizeDiffLine", () => {
  it("reproduces the input exactly when the segments are joined, for every grammar and for an unknown language", () => {
    for (const testCase of CONCATENATION_CASES) {
      const segments = tokenizeDiffLine(testCase.line, testCase.language);
      expect(joinSegments(segments)).toBe(testCase.line);
    }
  });

  it("reproduces the input exactly for every declared grammar key over a hostile line", () => {
    const hostile = "a\\\"b'c`d#e//f 0123 _x$y\t{[(<>)]}\\";
    for (const language of Object.keys(DIFF_HIGHLIGHT_GRAMMARS)) {
      const segments = tokenizeDiffLine(hostile, language);
      expect(joinSegments(segments)).toBe(hostile);
    }
  });

  it("treats inherited property names as unknown languages rather than reaching an inherited value", () => {
    for (const language of ["constructor", "__proto__", "toString", "hasOwnProperty"]) {
      const segments = tokenizeDiffLine("const x = 1;", language);
      expect(segments).toEqual([{ text: "const x = 1;", kind: "plain" }]);
    }
  });

  it("produces every token kind the closed set names", () => {
    const produced = new Set<DiffHighlightTokenKind>();
    const inputs: readonly HighlightCase[] = [
      { language: "typescript", line: "// a comment" },
      { language: "typescript", line: '"a string"' },
      { language: "typescript", line: "12345" },
      { language: "typescript", line: "const" },
      { language: "typescript", line: "+++" },
    ];
    for (const testCase of inputs) {
      for (const segment of tokenizeDiffLine(testCase.line, testCase.language)) {
        produced.add(segment.kind);
      }
    }
    for (const kind of DIFF_HIGHLIGHT_TOKEN_KINDS) {
      expect(produced.has(kind)).toBe(true);
    }
  });

  it("merges adjacent plain runs so no two consecutive segments both carry plain", () => {
    const segments = tokenizeDiffLine("zz + qq ?? ww", "typescript");
    expect(joinSegments(segments)).toBe("zz + qq ?? ww");
    expect(segments).toEqual([{ text: "zz + qq ?? ww", kind: "plain" }]);
    const mixed = tokenizeDiffLine("aa 1 bb", "typescript");
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
    const segments = tokenizeDiffLine(line, "typescript");
    expect(joinSegments(segments)).toBe(line);
    const last = segments[segments.length - 1];
    expect(last.kind).toBe("string");
    expect(last.text).toBe('"never closed');
  });

  it("is total over the empty string, a whitespace-only line and a lone delimiter", () => {
    expect(tokenizeDiffLine("", "typescript")).toEqual([]);
    expect(tokenizeDiffLine("", null)).toEqual([]);
    expect(tokenizeDiffLine("   \t ", "python")).toEqual([
      { text: "   \t ", kind: "plain" },
    ]);
    expect(tokenizeDiffLine('"', "typescript")).toEqual([{ text: '"', kind: "string" }]);
    expect(tokenizeDiffLine("'", "python")).toEqual([{ text: "'", kind: "string" }]);
    expect(tokenizeDiffLine("`", "markdown")).toEqual([{ text: "`", kind: "string" }]);
  });
});
