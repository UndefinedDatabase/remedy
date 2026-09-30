// T5_F044 T002, DECISION F044 D5 — the cockpit's one keymap: every binding the shell and the
// graph read a key press through, in one documented table (`KEYMAP_BINDINGS`, which the cheat
// overlay will render) plus one pure decision function (`keymapAction`). Remedy deliberately
// does not take a key from a field, and only Ctrl+K or Cmd+K reaches the keymap from one.
// PURE: nothing here touches the DOM; a caller reads `event.target`, `event.key` and the modifier
// flags, and this module answers what to do.

/** The minimal shape of the element a key press came from, read off `event.target`. */
export interface KeymapTarget {
  readonly tagName?: string;
  readonly isContentEditable?: boolean;
}

/** The minimal shape of a key press this module needs, read off a `KeyboardEvent`. */
export interface KeymapPress {
  readonly key: string;
  readonly ctrlKey: boolean;
  readonly metaKey: boolean;
  readonly altKey: boolean;
}

/** What a press decided, and whether a "g" is now waiting for its "p". */
export interface KeymapResult {
  readonly action: KeymapAction | null;
  readonly pendingG: boolean;
}

/** One row of the documented keymap, which the cheat overlay renders verbatim. */
export interface KeymapBinding {
  readonly keys: string;
  readonly action: KeymapAction;
  readonly label: string;
}

export type KeymapAction =
  | "open-bar"
  | "open-terms"
  | "go-projects"
  | "next-sibling"
  | "previous-sibling"
  | "zoom-in"
  | "walk-back";

/** DECISION F044 D5: every binding the keymap answers, in the order the cheat overlay shows
 *  them. */
export const KEYMAP_BINDINGS: readonly KeymapBinding[] = [
  { keys: "/ or Ctrl+K", action: "open-bar", label: "Ask or jump from the bar" },
  { keys: "?", action: "open-terms", label: "Show every term" },
  { keys: "g then p", action: "go-projects", label: "Go to the projects" },
  { keys: "j", action: "next-sibling", label: "Next node at this level" },
  { keys: "k", action: "previous-sibling", label: "Previous node at this level" },
  { keys: "Enter", action: "zoom-in", label: "Zoom into the chosen node" },
  { keys: "Esc", action: "walk-back", label: "Zoom back out" },
];

/** True for a content-editable target or one whose upper-cased tag is INPUT, TEXTAREA or
 *  SELECT — so a typed key stays text wherever one could be typed. False for null. */
export function isTypingTarget(target: KeymapTarget | null): boolean {
  if (target === null) return false;
  if (target.isContentEditable) return true;
  const tag = (target.tagName ?? "").toUpperCase();
  return tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT";
}

/** The one decision every key listener in the cockpit defers to. Applies, in order: the Ctrl+K
 *  or Cmd+K chord (without Alt) opens the bar from anywhere, a field included; any other press
 *  carrying Ctrl, Cmd or Alt, and any press from a typing target, is nothing; a waiting "g"
 *  followed by "p" goes to the projects; a bare "g" is nothing and leaves a "g" waiting; "/"
 *  opens the bar, "?" the terms, "j" and "k" walk the siblings; Enter zooms in only from the
 *  page itself or the body; Escape walks back unless a dialog is open; any other key is nothing.
 *  Every result but the one a "g" makes leaves no "g" waiting. */
export function keymapAction(
  press: KeymapPress,
  target: KeymapTarget | null,
  pendingG: boolean,
  dialogOpen: boolean,
): KeymapResult {
  const { key, ctrlKey, metaKey, altKey } = press;

  if (key.toLowerCase() === "k" && (ctrlKey || metaKey) && !altKey) {
    return { action: "open-bar", pendingG: false };
  }
  if (ctrlKey || metaKey || altKey) {
    return { action: null, pendingG: false };
  }
  if (isTypingTarget(target)) {
    return { action: null, pendingG: false };
  }
  if (pendingG && key === "p") {
    return { action: "go-projects", pendingG: false };
  }
  if (key === "g") {
    return { action: null, pendingG: true };
  }

  switch (key) {
    case "/":
      return { action: "open-bar", pendingG: false };
    case "?":
      return { action: "open-terms", pendingG: false };
    case "j":
      return { action: "next-sibling", pendingG: false };
    case "k":
      return { action: "previous-sibling", pendingG: false };
    case "Enter": {
      const tag = target === null ? null : (target.tagName ?? "").toUpperCase();
      const zoomable = target === null || tag === "BODY";
      return { action: zoomable ? "zoom-in" : null, pendingG: false };
    }
    case "Escape":
      return { action: dialogOpen ? null : "walk-back", pendingG: false };
    default:
      return { action: null, pendingG: false };
  }
}
