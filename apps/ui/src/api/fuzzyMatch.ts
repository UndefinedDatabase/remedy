// T5_F044 T001, DECISION F044 D1 — the palette's fuzzy rule: a contiguous hit of the whole query
// outranks every scattered hit, a hit that begins a word outranks one inside a word, case is
// ignored, and the match answers the ranges a row highlights. Every section of the palette ranks
// through this module.

/** A half-open range of UTF-16 code units into the text a match was found in. */
export type FuzzyRange = readonly [number, number];

/** A match's score and the ranges of the text it covers. */
export interface FuzzyMatch {
  readonly score: number;
  readonly ranges: readonly FuzzyRange[];
}

/** One item ranked by its fuzzy match. */
export interface FuzzyRanked<T> {
  readonly item: T;
  readonly match: FuzzyMatch;
}

export const FUZZY_SUBSTRING_BASE = 1000;
export const FUZZY_WORD_START_BONUS = 500;
export const FUZZY_SUBSEQUENCE_CAP = 499;

const WORD_CHAR = /[\p{L}\p{N}]/u;

/** Lower-cases a single UTF-16 code unit, keeping it as it is when its lower case is longer than
 *  one unit, so a folded text is exactly as long as the text. */
function foldUnit(unit: string): string {
  const lower = unit.toLowerCase();
  return lower.length === 1 ? lower : unit;
}

/** Folds a whole string one UTF-16 code unit at a time. */
function fold(text: string): string {
  let out = "";
  for (let i = 0; i < text.length; i += 1) {
    out += foldUnit(text[i]);
  }
  return out;
}

/** The query's runs of white space read as one space, its ends trimmed. */
function normalizeQuery(query: string): string {
  return query.replace(/\s+/g, " ").trim();
}

function isWordStart(foldedText: string, index: number): boolean {
  if (index === 0) return true;
  return !WORD_CHAR.test(foldedText[index - 1]);
}

/** The contiguous hit's index and whether it begins a word: the first occurrence that is a word
 *  start, else the first occurrence, else null when the query is not a contiguous substring. */
function firstContiguousHit(
  foldedText: string,
  foldedQuery: string,
): { index: number; wordStart: boolean } | null {
  const firstIndex = foldedText.indexOf(foldedQuery);
  if (firstIndex === -1) return null;
  let searchFrom = 0;
  for (;;) {
    const found = foldedText.indexOf(foldedQuery, searchFrom);
    if (found === -1) break;
    if (isWordStart(foldedText, found)) return { index: found, wordStart: true };
    searchFrom = found + 1;
  }
  return { index: firstIndex, wordStart: false };
}

function mergeRanges(indices: readonly number[]): FuzzyRange[] {
  const ranges: FuzzyRange[] = [];
  for (const index of indices) {
    const last = ranges[ranges.length - 1];
    if (last !== undefined && last[1] === index) {
      ranges[ranges.length - 1] = [last[0], index + 1];
    } else {
      ranges.push([index, index + 1]);
    }
  }
  return ranges;
}

/** The scattered hit: the query's units less its spaces, each found at its earliest index after
 *  the previous hit, scored 1 plus 3 at a word start plus 2 right after the previous hit, capped,
 *  merged into maximal ranges; a unit not found answers null. */
function scatteredMatch(foldedText: string, foldedQuery: string): FuzzyMatch | null {
  const units = foldedQuery.split("").filter((unit) => unit !== " ");
  const indices: number[] = [];
  let score = 0;
  let previousIndex = -1;
  for (const unit of units) {
    const found = foldedText.indexOf(unit, previousIndex + 1);
    if (found === -1) return null;
    let hitScore = 1;
    if (isWordStart(foldedText, found)) hitScore += 3;
    if (previousIndex !== -1 && found === previousIndex + 1) hitScore += 2;
    score += hitScore;
    indices.push(found);
    previousIndex = found;
  }
  return { score: Math.min(score, FUZZY_SUBSEQUENCE_CAP), ranges: mergeRanges(indices) };
}

export function fuzzyMatch(query: string, text: string): FuzzyMatch | null {
  const normalized = normalizeQuery(query);
  if (normalized === "") return { score: 0, ranges: [] };
  const foldedQuery = fold(normalized);
  const foldedText = fold(text);
  const contiguous = firstContiguousHit(foldedText, foldedQuery);
  if (contiguous !== null) {
    const score = FUZZY_SUBSTRING_BASE
      + (contiguous.wordStart ? FUZZY_WORD_START_BONUS : 0)
      - Math.min(contiguous.index, FUZZY_SUBSEQUENCE_CAP);
    return { score, ranges: [[contiguous.index, contiguous.index + foldedQuery.length]] };
  }
  return scatteredMatch(foldedText, foldedQuery);
}

export function rankFuzzy<T>(
  items: readonly T[],
  query: string,
  textOf: (item: T) => string,
): FuzzyRanked<T>[] {
  const rows: { item: T; match: FuzzyMatch; text: string; index: number }[] = [];
  items.forEach((item, index) => {
    const text = textOf(item);
    const match = fuzzyMatch(query, text);
    if (match !== null) rows.push({ item, match, text, index });
  });
  rows.sort((a, b) => {
    if (a.match.score !== b.match.score) return b.match.score - a.match.score;
    if (a.text.length !== b.text.length) return a.text.length - b.text.length;
    if (a.text !== b.text) return a.text < b.text ? -1 : 1;
    return a.index - b.index;
  });
  return rows.map(({ item, match }) => ({ item, match }));
}
