// F044 T001 — the palette's fuzzy rule (DECISION F044 D1). Every expected score below is computed
// by hand from the rule the module states, never read back from the module.
import { describe, expect, it } from "vitest";
import {
  FUZZY_SUBSEQUENCE_CAP,
  FUZZY_SUBSTRING_BASE,
  FUZZY_WORD_START_BONUS,
  fuzzyMatch,
  rankFuzzy,
} from "./fuzzyMatch";

describe("fuzzyMatch constants", () => {
  it("are the three numbers the rule names", () => {
    expect([FUZZY_SUBSTRING_BASE, FUZZY_WORD_START_BONUS, FUZZY_SUBSEQUENCE_CAP]).toEqual([1000, 500, 499]);
  });
});

describe("fuzzyMatch, a contiguous hit", () => {
  it("matches everything with score 0 and no range for an empty or blank query", () => {
    expect(fuzzyMatch("", "anything")).toEqual({ score: 0, ranges: [] });
    expect(fuzzyMatch("   ", "")).toEqual({ score: 0, ranges: [] });
  });

  it("scores a hit at the start of the text as base plus the word bonus", () => {
    expect(fuzzyMatch("err", "Error handling")).toEqual({ score: 1500, ranges: [[0, 3]] });
  });

  it("takes the first occurrence that begins a word over an earlier one inside a word", () => {
    expect(fuzzyMatch("err", "terror error")).toEqual({ score: 1493, ranges: [[7, 10]] });
  });

  it("takes the first occurrence, less its position, when none begins a word", () => {
    expect(fuzzyMatch("rro", "terror")).toEqual({ score: 998, ranges: [[2, 5]] });
  });

  it("ignores case on both sides", () => {
    expect(fuzzyMatch("ERR", "error")).toEqual({ score: 1500, ranges: [[0, 3]] });
  });

  it("reads the query's white space runs as one space and trims its ends", () => {
    expect(fuzzyMatch("  error   handling ", "Fix error handling")).toEqual({ score: 1496, ranges: [[4, 18]] });
  });

  it("counts a character after punctuation as the start of a word, and one after a digit not", () => {
    expect(fuzzyMatch("han", "error-handling")).toEqual({ score: 1494, ranges: [[6, 9]] });
    expect(fuzzyMatch("2b", "t12b")).toEqual({ score: 998, ranges: [[2, 4]] });
  });

  it("caps the position it subtracts, so a late contiguous hit still outranks any scattered one", () => {
    const match = fuzzyMatch("z", `${"a".repeat(600)}z`);
    expect(match).toEqual({ score: 501, ranges: [[600, 601]] });
  });

  it("keeps a range over the text as given when a character's lower case is longer", () => {
    expect(fuzzyMatch("x", "İx")).toEqual({ score: 999, ranges: [[1, 2]] });
  });
});

describe("fuzzyMatch, a scattered hit", () => {
  it("scores each character 1, plus 3 at a word start, plus 2 right after the previous hit", () => {
    expect(fuzzyMatch("eh", "error handling")).toEqual({ score: 8, ranges: [[0, 1], [6, 7]] });
    expect(fuzzyMatch("erh", "error handling")).toEqual({ score: 11, ranges: [[0, 2], [6, 7]] });
  });

  it("drops the query's spaces when no contiguous hit exists", () => {
    expect(fuzzyMatch("e h", "error handling")).toEqual({ score: 8, ranges: [[0, 1], [6, 7]] });
  });

  it("answers null when a character is missing or out of order", () => {
    expect(fuzzyMatch("xyz", "error")).toBeNull();
    expect(fuzzyMatch("he", "eh")).toBeNull();
  });

  it("caps the sum", () => {
    const match = fuzzyMatch("a".repeat(150), "a ".repeat(200));
    expect(match?.score).toBe(499);
    expect(match?.ranges.length).toBe(150);
  });
});

describe("rankFuzzy", () => {
  it("drops non-matches and lists the rest by score", () => {
    const ranked = rankFuzzy(["error handling", "terror", "handle errors", "xyz"], "err", (text) => text);
    expect(ranked.map((row) => [row.item, row.match.score])).toEqual([
      ["error handling", 1500],
      ["handle errors", 1493],
      ["terror", 999],
    ]);
  });

  it("breaks a tie by the shorter text, then the text by code unit, then the order given", () => {
    const items = [
      { id: 0, text: "b x" },
      { id: 1, text: "a x" },
      { id: 2, text: "cc x" },
      { id: 3, text: "a x" },
      { id: 4, text: "B x" },
    ];
    const ranked = rankFuzzy(items, "x", (item) => item.text);
    expect(ranked.map((row) => row.item.id)).toEqual([4, 1, 3, 0, 2]);
  });

  it("keeps every item for an empty query, ordered by the same tie-breaks", () => {
    const ranked = rankFuzzy(["ccc", "ab", "a", "bb", "b"], "", (text) => text);
    expect(ranked.map((row) => row.item)).toEqual(["a", "b", "ab", "bb", "ccc"]);
    expect(ranked.every((row) => row.match.score === 0 && row.match.ranges.length === 0)).toBe(true);
  });
});
