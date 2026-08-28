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
 *  a per-line tokenizer cannot honour more than this without lying. */
export interface DiffHighlightGrammar {
  lineComment: readonly string[];
  stringDelimiters: readonly string[];
  keywords: ReadonlySet<string>;
}

/** Freezes one grammar and its two arrays, so a caller that reaches into the
 *  exported mapping cannot mutate the rules another line will be scanned with. */
function freezeDiffHighlightGrammar(
  lineComment: readonly string[],
  stringDelimiters: readonly string[],
  keywords: readonly string[],
): DiffHighlightGrammar {
  return Object.freeze({
    lineComment: Object.freeze([...lineComment]),
    stringDelimiters: Object.freeze([...stringDelimiters]),
    keywords: new Set<string>(keywords),
  });
}

const JS_KEYWORDS: readonly string[] = [
  "as", "async", "await", "break", "case", "catch", "class", "const",
  "continue", "default", "delete", "do", "else", "enum", "export", "extends",
  "false", "finally", "for", "from", "function", "if", "implements", "import",
  "in", "instanceof", "interface", "let", "new", "null", "of", "return",
  "satisfies", "static", "super", "switch", "this", "throw", "true", "try",
  "type", "typeof", "undefined", "var", "void", "while", "yield",
];

/** The grammar per language id, keyed by the VALUES of `DIFF_SUPPORTED_LANGUAGES`
 *  in `./diffViewModel` — the ids `diffLanguageForPath` answers.
 *
 *  BUILT ON `Object.create(null)` AND READ THROUGH AN OWN-PROPERTY CHECK, both
 *  halves load-bearing, for the reason `diffViewModel.ts` states above
 *  `DIFF_SUPPORTED_LANGUAGES` and finding `R-0731` proved: the language id
 *  originates in a diff path from a repository this viewer does not control, so
 *  the key set is the attacker's and not ours. A mapping with a prototype
 *  answers `constructor` and `__proto__` with inherited values, and reading the
 *  result against `undefined` calls that a hit. Neither half may be removed as
 *  redundant — either one alone repairs the defect, which is exactly why
 *  dropping one lets a later refactor of the other restore it silently. */
export const DIFF_HIGHLIGHT_GRAMMARS: Readonly<Record<string, DiffHighlightGrammar>> =
  Object.freeze(
    Object.assign(Object.create(null) as Record<string, DiffHighlightGrammar>, {
      typescript: freezeDiffHighlightGrammar(["//"], ['"', "'", "`"], JS_KEYWORDS),
      tsx: freezeDiffHighlightGrammar(["//"], ['"', "'", "`"], JS_KEYWORDS),
      javascript: freezeDiffHighlightGrammar(["//"], ['"', "'", "`"], JS_KEYWORDS),
      jsx: freezeDiffHighlightGrammar(["//"], ['"', "'", "`"], JS_KEYWORDS),
      python: freezeDiffHighlightGrammar(
        ["#"],
        ['"""', "'''", '"', "'"],
        [
          "and", "as", "assert", "async", "await", "break", "class", "continue",
          "def", "del", "elif", "else", "except", "False", "finally", "for",
          "from", "global", "if", "import", "in", "is", "lambda", "None",
          "nonlocal", "not", "or", "pass", "raise", "return", "True", "try",
          "while", "with", "yield",
        ],
      ),
      json: freezeDiffHighlightGrammar([], ['"'], ["true", "false", "null"]),
      css: freezeDiffHighlightGrammar(
        [],
        ['"', "'"],
        [
          "auto", "block", "flex", "grid", "hidden", "important", "inherit",
          "initial", "none", "absolute", "relative", "fixed", "sticky", "solid",
          "transparent", "unset",
        ],
      ),
      markdown: freezeDiffHighlightGrammar([], ["`"], []),
      shell: freezeDiffHighlightGrammar(
        ["#"],
        ['"', "'"],
        [
          "case", "do", "done", "elif", "else", "esac", "exit", "export", "fi",
          "for", "function", "if", "in", "local", "readonly", "return", "set",
          "then", "until", "while",
        ],
      ),
      yaml: freezeDiffHighlightGrammar(
        ["#"],
        ['"', "'"],
        ["true", "false", "null", "yes", "no", "on", "off"],
      ),
      toml: freezeDiffHighlightGrammar(
        ["#"],
        ['"""', "'''", '"', "'"],
        ["true", "false"],
      ),
    }),
  );

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

/** Splits one line of diff text into typed segments for `language`.
 *
 *  TOTAL: no input throws, for any string and any language id, and a language
 *  the mapping does not OWN is an ANSWER — the whole line comes back `plain` —
 *  rather than an error, exactly as `diffLanguageForPath` answers `null`.
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
  language: string | null,
): readonly DiffHighlightSegment[] {
  if (text.length === 0) {
    return [];
  }
  if (
    language === null ||
    !Object.prototype.hasOwnProperty.call(DIFF_HIGHLIGHT_GRAMMARS, language)
  ) {
    return [{ text, kind: "plain" }];
  }
  const grammar = DIFF_HIGHLIGHT_GRAMMARS[language];
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
