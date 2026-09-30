// F044 T002 — the cockpit's one keymap (DECISION F044 D5).
import { describe, expect, it } from "vitest";
import { KEYMAP_BINDINGS, isTypingTarget, keymapAction } from "./keymap";
import type { KeymapPress, KeymapTarget } from "./keymap";

function press(key: string, mods: Partial<Omit<KeymapPress, "key">> = {}): KeymapPress {
  return { key, ctrlKey: false, metaKey: false, altKey: false, ...mods };
}

const BODY: KeymapTarget = { tagName: "BODY" };
const DIV: KeymapTarget = { tagName: "DIV", isContentEditable: false };
const INPUT: KeymapTarget = { tagName: "input" };

function act(key: string, target: KeymapTarget | null = BODY, pendingG = false, dialogOpen = false,
  mods: Partial<Omit<KeymapPress, "key">> = {}) {
  return keymapAction(press(key, mods), target, pendingG, dialogOpen);
}

describe("KEYMAP_BINDINGS", () => {
  it("documents every binding, in order, as DECISION F044 D5 wrote it", () => {
    expect(KEYMAP_BINDINGS).toEqual([
      { keys: "/ or Ctrl+K", action: "open-bar", label: "Ask or jump from the bar" },
      { keys: "?", action: "open-terms", label: "Show every term" },
      { keys: "g then p", action: "go-projects", label: "Go to the projects" },
      { keys: "j", action: "next-sibling", label: "Next node at this level" },
      { keys: "k", action: "previous-sibling", label: "Previous node at this level" },
      { keys: "Enter", action: "zoom-in", label: "Zoom into the chosen node" },
      { keys: "Esc", action: "walk-back", label: "Zoom back out" },
    ]);
  });
});

describe("isTypingTarget", () => {
  it("reads a field, of any case, and anything content-editable, as text", () => {
    expect(isTypingTarget({ tagName: "INPUT" })).toBe(true);
    expect(isTypingTarget({ tagName: "textarea" })).toBe(true);
    expect(isTypingTarget({ tagName: "Select" })).toBe(true);
    expect(isTypingTarget({ tagName: "DIV", isContentEditable: true })).toBe(true);
  });

  it("reads no target, the body and an ordinary element as no field", () => {
    expect(isTypingTarget(null)).toBe(false);
    expect(isTypingTarget(BODY)).toBe(false);
    expect(isTypingTarget({ tagName: "button" })).toBe(false);
    expect(isTypingTarget({})).toBe(false);
  });
});

describe("keymapAction", () => {
  it("opens the bar on / and on Ctrl+K or Cmd+K, the chord even from a field", () => {
    expect(act("/")).toEqual({ action: "open-bar", pendingG: false });
    expect(act("k", BODY, false, false, { ctrlKey: true })).toEqual({ action: "open-bar", pendingG: false });
    expect(act("K", INPUT, false, false, { metaKey: true })).toEqual({ action: "open-bar", pendingG: false });
    expect(act("k", INPUT, true, false, { ctrlKey: true })).toEqual({ action: "open-bar", pendingG: false });
  });

  it("takes nothing else from a field, so a typed key stays text", () => {
    for (const key of ["/", "?", "j", "k", "g", "p", "Enter", "Escape"]) {
      expect(act(key, INPUT), key).toEqual({ action: null, pendingG: false });
    }
    expect(act("?", { tagName: "DIV", isContentEditable: true })).toEqual({ action: null, pendingG: false });
  });

  it("takes nothing with another modifier, and Alt spoils even the chord", () => {
    expect(act("/", BODY, false, false, { ctrlKey: true })).toEqual({ action: null, pendingG: false });
    expect(act("j", BODY, false, false, { metaKey: true })).toEqual({ action: null, pendingG: false });
    expect(act("k", BODY, false, false, { ctrlKey: true, altKey: true })).toEqual({ action: null, pendingG: false });
  });

  it("opens the terms on ?, from the page or an ordinary element", () => {
    expect(act("?")).toEqual({ action: "open-terms", pendingG: false });
    expect(act("?", null)).toEqual({ action: "open-terms", pendingG: false });
    expect(act("?", DIV)).toEqual({ action: "open-terms", pendingG: false });
  });

  it("goes to the projects on g then p, and any other key ends the wait", () => {
    expect(act("g")).toEqual({ action: null, pendingG: true });
    expect(act("p", BODY, true)).toEqual({ action: "go-projects", pendingG: false });
    expect(act("p", BODY, false)).toEqual({ action: null, pendingG: false });
    expect(act("x", BODY, true)).toEqual({ action: null, pendingG: false });
    expect(act("j", BODY, true)).toEqual({ action: "next-sibling", pendingG: false });
    expect(act("g", BODY, true)).toEqual({ action: null, pendingG: true });
  });

  it("walks the siblings on j and k", () => {
    expect(act("j")).toEqual({ action: "next-sibling", pendingG: false });
    expect(act("k")).toEqual({ action: "previous-sibling", pendingG: false });
    expect(act("J")).toEqual({ action: null, pendingG: false });
  });

  it("zooms in on Enter only from no element or the body, since Enter on a control is its own", () => {
    expect(act("Enter", null)).toEqual({ action: "zoom-in", pendingG: false });
    expect(act("Enter", BODY)).toEqual({ action: "zoom-in", pendingG: false });
    expect(act("Enter", { tagName: "button" })).toEqual({ action: null, pendingG: false });
    expect(act("Enter", DIV)).toEqual({ action: null, pendingG: false });
  });

  it("walks back on Escape unless a dialog is open", () => {
    expect(act("Escape")).toEqual({ action: "walk-back", pendingG: false });
    expect(act("Escape", DIV)).toEqual({ action: "walk-back", pendingG: false });
    expect(act("Escape", BODY, false, true)).toEqual({ action: null, pendingG: false });
  });

  it("answers nothing for any other key", () => {
    expect(act("h")).toEqual({ action: null, pendingG: false });
    expect(act("ArrowDown")).toEqual({ action: null, pendingG: false });
  });
});
