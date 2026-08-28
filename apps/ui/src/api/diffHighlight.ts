// The per-line syntax highlight MODEL of F256 (T5_F256 T001): one line of diff
// text turned into a flat list of typed segments. It holds no markup, chooses no
// colour, names no class and imports nothing at runtime, so every rule below is
// decidable from plain data alone and runs in the node-environment vitest config
// `apps/ui/vitest.config.ts` really executes (DECISION F031 D5). DECISION F256
// D1 is why the tokenizer is Remedy's own rather than a third-party
// highlighter's: no registry is reachable from this build environment, and a
// dependency's rules would sit outside what any runner here can execute.
//
// THE PER-LINE RULING, which is the whole shape of this module: highlighting is
// decided per LINE and never across lines. A diff omits the lines between hunks,
// so block-comment and multi-line-string state cannot be carried honestly — a
// viewer that tried would mark the wrong runs with confidence, and confident and
// wrong is worse than plain. Remedy deliberately does not track cross-line
// highlight state. A reader searching here for a block-comment rule, a
// here-document rule or a carried-over string state will not find one, and the
// absence is the ruling rather than an omission.
//
// THIS IS THE EAGER HALF, and the grammar TABLES are not here — they live in
// `./diffHighlightGrammars`, which is fetched lazily. The scanner below is what
// a diff row needs SYNCHRONOUSLY to be drawn at all, while a grammar is needed
// only once a file's path has resolved to a language, so that is where the cut
// falls. THE CUT IS ALSO WHAT MAKES THE LAZINESS REAL — finding `R-0732`: a
// module imported both statically and dynamically BY THE SAME FILE is not
// code-split at all, and `../components/diff/DiffView.tsx` imported this one
// both ways until the tables moved out, so every grammar shipped in the main
// chunk while the bundler warned that the dynamic import would move nothing.
// Every function below therefore takes a `DiffHighlightGrammar | null` as an
// ARGUMENT rather than looking a language id up in a table of its own; the
// caller owns that dependency, exactly as it already owns the intraline cut.

/** The CLOSED token set. It is small on purpose: every kind must eventually map
 *  to a custom property already defined under `apps/ui/src`, which
 *  `tests/ui_contracts/test_design_drift.py` enforces, and a larger set would
 *  invent distinctions no palette in this repository can honour. */
export const DIFF_HIGHLIGHT_TOKEN_KINDS = Object.freeze([
  "comment",
  "string",
  "number",
  "keyword",
  "plain",
] as const);

/** The union of the kinds above, derived from the tuple so the two can never
 *  drift apart. */
export type DiffHighlightTokenKind = (typeof DIFF_HIGHLIGHT_TOKEN_KINDS)[number];

/** One highlighted run of a line: the text VERBATIM and the kind to draw it as.
 *  The text is carried rather than a pair of offsets so the caller cannot
 *  mis-slice it back. */
export interface DiffHighlightSegment {
  text: string;
  kind: DiffHighlightTokenKind;
}

/** The three rules one language contributes to the scanner. Everything else —
 *  digits, identifiers, punctuation — is language-independent by design, because
 *  a per-line tokenizer cannot honour more than this without lying.
 *
 *  THE TYPE IS DECLARED HERE AND THE TABLES ARE NOT. `./diffHighlightGrammars`
 *  imports this type — a type import is erased at build time, so it is no
 *  runtime edge — and exports `diffHighlightGrammarFor`, which is the one way a
 *  language id becomes one of these. */
export interface DiffHighlightGrammar {
  lineComment: readonly string[];
  stringDelimiters: readonly string[];
  keywords: ReadonlySet<string>;
}

/** A single ASCII digit. Kept as an explicit range rather than a regular
 *  expression so it cannot match a digit from another script that the number
 *  rule was never written for. */
function isDiffHighlightDigit(character: string): boolean {
  return character >= "0" && character <= "9";
}

/** A single identifier character: ASCII letters, digits, `_` and `$`. Digits
 *  belong to the set so `value1` is one word, and the scanner reaches this test
 *  only after the digit test has failed, so `1abc` still opens with a number. */
function isDiffHighlightIdentifierCharacter(character: string): boolean {
  return (
    (character >= "a" && character <= "z") ||
    (character >= "A" && character <= "Z") ||
    isDiffHighlightDigit(character) ||
    character === "_" ||
    character === "$"
  );
}

/** The offset just past the string that opened at `from` with `delimiter`, or
 *  the end of the line when it never closes. A backslash consumes the character
 *  after it, so `"a\"b"` is one string; an unterminated string running off the
 *  end of the line is an ANSWER rather than an error, because the per-line
 *  ruling above means the closer may simply live on a line the diff omitted. */
function diffHighlightStringEnd(text: string, from: number, delimiter: string): number {
  let index = from;
  while (index < text.length) {
    if (text[index] === "\\") {
      index += 2;
      continue;
    }
    if (text.startsWith(delimiter, index)) {
      return index + delimiter.length;
    }
    index += 1;
  }
  return text.length;
}

/** The first opener in `openers` that `text` carries at `index`, or `undefined`.
 *  ARRAY ORDER IS THE PRECEDENCE, which is why the python and toml delimiter
 *  lists put `"""` before `"`: first match wins, and the shorter opener listed
 *  first would cut a triple-quoted string into three. */
function diffHighlightMatchAt(
  text: string,
  index: number,
  openers: readonly string[],
): string | undefined {
  for (const opener of openers) {
    if (opener.length > 0 && text.startsWith(opener, index)) {
      return opener;
    }
  }
  return undefined;
}

/** Splits one line of diff text into typed segments under `grammar`.
 *
 *  TOTAL: no input throws, for any string and any grammar. A `null` grammar is
 *  an ANSWER — the whole line comes back `plain` — rather than an error, exactly
 *  as `diffLanguageForPath` answers `null` for a path it does not recognise and
 *  `diffHighlightGrammarFor` answers `null` for an id its tables do not OWN.
 *  That `null` therefore covers three cases at once and renders them alike: an
 *  unsupported language, a file whose language has not been resolved yet, and a
 *  lazy grammar chunk that never arrived.
 *
 *  THE LOAD-BEARING INVARIANT, which every case below is written to preserve and
 *  the vitest suite pins for each of them: joining the returned segments' `text`
 *  in order reproduces `text` EXACTLY. A highlighter that drops or duplicates a
 *  character is worse than none, because the operator is reading the line to
 *  judge a change, and a lost character changes what the change says.
 *
 *  Scanning is left to right and FIRST MATCH WINS: a line-comment opener makes
 *  the rest of the line one `comment`; a string delimiter opens a `string`
 *  running to the next unescaped occurrence of that same delimiter or to the end
 *  of the line; a run of digits is a `number`; a run of identifier characters is
 *  a `keyword` when the grammar owns it and `plain` otherwise; anything else is
 *  `plain`. Adjacent `plain` runs are MERGED, so no two consecutive segments
 *  both carry `plain` and a renderer draws one element per visible run. */
export function tokenizeDiffLine(
  text: string,
  grammar: DiffHighlightGrammar | null,
): readonly DiffHighlightSegment[] {
  if (text.length === 0) {
    return [];
  }
  if (grammar === null) {
    return [{ text, kind: "plain" }];
  }
  const segments: DiffHighlightSegment[] = [];
  const push = (chunk: string, kind: DiffHighlightTokenKind): void => {
    if (
      kind === "plain" &&
      segments.length > 0 &&
      segments[segments.length - 1].kind === "plain"
    ) {
      segments[segments.length - 1].text += chunk;
      return;
    }
    segments.push({ text: chunk, kind });
  };

  let index = 0;
  while (index < text.length) {
    if (diffHighlightMatchAt(text, index, grammar.lineComment) !== undefined) {
      push(text.slice(index), "comment");
      index = text.length;
      continue;
    }
    const delimiter = diffHighlightMatchAt(text, index, grammar.stringDelimiters);
    if (delimiter !== undefined) {
      const end = diffHighlightStringEnd(text, index + delimiter.length, delimiter);
      push(text.slice(index, end), "string");
      index = end;
      continue;
    }
    const character = text[index];
    if (isDiffHighlightDigit(character)) {
      let end = index;
      while (end < text.length && isDiffHighlightDigit(text[end])) {
        end += 1;
      }
      push(text.slice(index, end), "number");
      index = end;
      continue;
    }
    if (isDiffHighlightIdentifierCharacter(character)) {
      let end = index;
      while (end < text.length && isDiffHighlightIdentifierCharacter(text[end])) {
        end += 1;
      }
      const word = text.slice(index, end);
      push(word, grammar.keywords.has(word) ? "keyword" : "plain");
      index = end;
      continue;
    }
    push(character, "plain");
    index += 1;
  }
  return segments;
}

/** One run of a changed line that is uniform in BOTH dimensions at once: the
 *  same intraline `marked` state and the same token `kind` over its whole
 *  `text`. It is what a renderer draws one element for, and it exists because
 *  neither cut alone describes a changed line — the word-level emphasis says
 *  WHAT changed and the syntax colour says what the line IS. */
export interface DiffHighlightRun {
  text: string;
  marked: boolean;
  kind: DiffHighlightTokenKind;
}

/** The intraline cut this module composes with, declared STRUCTURALLY rather
 *  than imported: it is the shape `splitLineIntoIntralineSegments` in
 *  `./diffViewModel` returns, and repeating it here is what keeps the header's
 *  ruling above true — this module imports nothing at runtime, so every rule in
 *  it stays decidable from plain data alone. `composeHighlightedRuns` therefore
 *  takes those segments as an ARGUMENT; the caller owns the dependency. */
export interface DiffMarkedSegment {
  text: string;
  marked: boolean;
}

/** Composes the intraline cut with the token cut of the SAME line, so one line
 *  carries word-level emphasis and syntax colour at once.
 *
 *  TOTAL: no input throws, for any segment list and any grammar. An empty
 *  list, and a list whose texts are all empty, both yield the EMPTY ARRAY —
 *  there is no run to describe, and a run carrying the empty string would render
 *  an element around nothing, which is the ruling
 *  `splitLineIntoIntralineSegments` already makes for empty content.
 *
 *  TWO PER-CHARACTER MAPS, not a merge of two run lists, for the reason that
 *  function gives for its own coverage map: each partition paints its own
 *  characters, the runs are read off afterwards, and no character can be dropped
 *  or emitted twice however the two cuts interleave — a marked run inside a
 *  token, a token inside a marked run, or boundaries that cross at an offset
 *  belonging to neither. The line is joined from the segments and tokenized
 *  ONCE, because `tokenizeDiffLine` is decided per line and re-tokenizing a
 *  fragment would score it out of context.
 *
 *  THE LOAD-BEARING INVARIANTS, each pinned separately by the vitest suite:
 *  joining the returned runs' `text` reproduces the joined input exactly; every
 *  character keeps the `marked` of the input segment covering it; and every
 *  character keeps the `kind` `tokenizeDiffLine` gives that position for the
 *  same grammar. Adjacent runs agreeing on BOTH are MERGED, so no two
 *  consecutive runs share both and a renderer draws one element per visible
 *  run.
 *
 *  THE GRAMMAR IS PASSED STRAIGHT THROUGH and is never looked up here, for the
 *  reason the header gives: the tables are the lazy half in
 *  `./diffHighlightGrammars` and this module is the eager one, so the caller
 *  hands in whatever the lazy chunk answered — including `null` while it is
 *  still in flight. */
export function composeHighlightedRuns(
  segments: readonly DiffMarkedSegment[],
  grammar: DiffHighlightGrammar | null,
): readonly DiffHighlightRun[] {
  const line = segments.map((segment) => segment.text).join("");
  if (line.length === 0) {
    return [];
  }

  const markedAt: boolean[] = new Array<boolean>(line.length).fill(false);
  let cursor = 0;
  for (const segment of segments) {
    for (let offset = 0; offset < segment.text.length; offset += 1) {
      markedAt[cursor] = segment.marked;
      cursor += 1;
    }
  }

  // `plain` is the fill rather than a hole, so a character no token claimed is
  // still an ANSWER — the same reading `tokenizeDiffLine` gives an unknown
  // language — instead of an `undefined` a renderer would have to guess at.
  const kindAt: DiffHighlightTokenKind[] = new Array<DiffHighlightTokenKind>(
    line.length,
  ).fill("plain");
  cursor = 0;
  for (const token of tokenizeDiffLine(line, grammar)) {
    for (let offset = 0; offset < token.text.length; offset += 1) {
      kindAt[cursor] = token.kind;
      cursor += 1;
    }
  }

  const runs: DiffHighlightRun[] = [];
  let runStart = 0;
  for (let index = 1; index <= line.length; index += 1) {
    if (
      index === line.length ||
      markedAt[index] !== markedAt[runStart] ||
      kindAt[index] !== kindAt[runStart]
    ) {
      runs.push({
        text: line.slice(runStart, index),
        marked: markedAt[runStart],
        kind: kindAt[runStart],
      });
      runStart = index;
    }
  }
  return runs;
}
