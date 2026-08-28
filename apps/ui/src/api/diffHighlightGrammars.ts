// The LAZY HALF of F256's per-line syntax highlighting (T5_F256 T001d): the
// grammar TABLES on their own, in their own module. The SCANNER that reads a
// line stays in `./diffHighlight` and is loaded eagerly, because a diff row
// cannot be drawn without it; a grammar is needed only once a file's path has
// resolved to a language, which is why this half is the one fetched lazily.
//
// WHY THE SPLIT EXISTS AT ALL, and it is an IMPORT-SHAPE rule rather than a
// highlighting one — finding `R-0732`. Until this module,
// `../components/diff/DiffView.tsx` imported `./diffHighlight` STATICALLY, for
// `composeHighlightedRuns`, and DYNAMICALLY in the same file as the bundle
// importer it hands to `loadDiffLanguageBundle`. A MODULE IMPORTED BOTH WAYS BY
// THE SAME FILE IS NOT CODE-SPLIT AT ALL: the bundler keeps it in the main
// chunk and warns that the dynamic import will not move it, so every grammar
// below shipped to every operator who never opened a diff — exactly the weight
// DECISION F256 D1 said the lazy bundles would avoid. Splitting the tables out
// is what makes the dynamically imported module one its importer does not also
// import statically. Nothing in this repository runs a bundler inside a test,
// so `tests/ui_contracts/test_diff_view_render.py` pins that shape by reading
// the component's source instead.
//
// The ONLY thing this module takes from `./diffHighlight` is the
// `DiffHighlightGrammar` TYPE. A type import is erased at build time, so it is
// no runtime edge and cannot pull the scanner back into this chunk.
import type { DiffHighlightGrammar } from "./diffHighlight";

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

/** The grammar `language` is scanned with, or `null` when there is none.
 *
 *  TOTAL: `null` in gives `null` back, and so does every id the mapping does not
 *  OWN. That `null` is not an error — `tokenizeDiffLine` reads it as "render the
 *  whole line plain", which is the same answer an unsupported language produced
 *  before the tables moved here.
 *
 *  READ THROUGH AN OWN-PROPERTY CHECK for the reason the declaration above
 *  states and finding `R-0731` proved: the id originates in a diff path from a
 *  repository this viewer does not control, so `constructor`, `__proto__`,
 *  `toString` and `hasOwnProperty` all arrive here as ordinary strings and each
 *  must answer `null`. The vitest suite pins those four by name. */
export function diffHighlightGrammarFor(
  language: string | null,
): DiffHighlightGrammar | null {
  if (
    language === null ||
    !Object.prototype.hasOwnProperty.call(DIFF_HIGHLIGHT_GRAMMARS, language)
  ) {
    return null;
  }
  return DIFF_HIGHLIGHT_GRAMMARS[language];
}
