// T5_F044 T001, DECISIONS F044 D2 to D4 — the bar's dropdown sheet, its pure rules: the rows of
// its six sections (Recent, Ask, Commands, Jump, Projects, Help), ranked and highlighted by the
// fuzzy rule, the browser-remembered refs a chosen row leaves behind, the active-row cursor's
// wrap-around, and the label cut into highlighted pieces the sheet renders. THE COMMANDS SECTION
// (D3 (1)) leads with the row `routeBarText` names, when one is named, then the fuzzy-ranked
// titles of `PALETTE_COMMANDS`, cut at `COMMAND_RESULT_LIMIT`; every row but a refused command's
// carries "" as its `disabledReason`. THE ASK ROW (D4 (1)) hands a question, or a line every
// other section left unmatched, to the chat.
import type { FuzzyRange } from "./fuzzyMatch";
import { rankFuzzy } from "./fuzzyMatch";
import type { JumpTarget } from "./paletteJump";
import { JUMP_RESULT_LIMIT, rankJumpTargets } from "./paletteJump";
import type { PaletteCommand } from "./paletteCommands";
import { PALETTE_COMMANDS, paletteCommandOf } from "./paletteCommands";
import { routeBarText } from "./paletteRouting";

/** The sheet's six sections, in the order a row's section always renders under. */
export type PaletteSection = "Recent" | "Ask" | "Commands" | "Jump" | "Projects" | "Help";

export const PALETTE_SECTION_ORDER: readonly PaletteSection[] = ["Recent", "Ask", "Commands", "Jump", "Projects", "Help"];

/** All rows (`"all"`), or the Jump rows alone while an argument flow asks for a task
 *  (`"task"`) — `CommandBar.tsx` drives the mode, `buildPaletteRows` only reads it. */
export type PaletteMode = "all" | "task";

/** What choosing a row does. */
export type PaletteAction =
  | { readonly kind: "jump"; readonly nodeId: string }
  | { readonly kind: "project"; readonly slug: string }
  | { readonly kind: "terms" }
  | { readonly kind: "tour" }
  | { readonly kind: "command"; readonly command: string }
  | { readonly kind: "chat"; readonly text: string };

/** One row of the sheet. `ref` is what a browser remembers when the row is chosen — the same
 *  string as `key` for every row except a Recent one, whose `key` carries the `recent:` prefix
 *  its `ref` does not. `disabledReason` is "" for every row but a refused command's, where it
 *  doubles as the row's `hint`. */
export interface PaletteRow {
  readonly key: string;
  readonly ref: string;
  readonly section: PaletteSection;
  readonly label: string;
  readonly hint: string;
  readonly ranges: readonly FuzzyRange[];
  readonly action: PaletteAction;
  readonly disabledReason: string;
}

export const COMMAND_RESULT_LIMIT = 6;

/** The Ask row's fixed hint (DECISION F044 D4 (1)). */
export const PALETTE_ASK_HINT = "Ask the chat";

/** A project the bar can switch to. */
export interface PaletteProject {
  readonly slug: string;
  readonly name: string;
}

/** What `buildPaletteRows` needs to build one query's worth of rows. */
export interface PaletteInput {
  readonly query: string;
  readonly targets: readonly JumpTarget[];
  readonly projects: readonly PaletteProject[];
  readonly activeSlug: string;
  readonly recents: readonly string[];
  readonly commandReasons: Readonly<Record<string, string>>;
  readonly focusedTaskId: string;
  readonly mode: PaletteMode;
}

export const PROJECT_RESULT_LIMIT = 5;
export const PALETTE_RECENT_LIMIT = 5;

/** Where the browser remembers the sheet's chosen refs. */
export const PALETTE_RECENTS_KEY = "remedy:palette-recent";

/** The storage this module needs, and nothing more. */
export type PaletteRecentsStorage = Pick<Storage, "getItem" | "setItem">;

/** One piece of a highlighted label: the matched letters, or the letters around them. */
export interface LabelPiece {
  readonly text: string;
  readonly hit: boolean;
}

/** The Help section's two rows, fixed. Always `ranges: []`: a blank query shows them as they are
 *  here; a query ranks them fresh through `rankFuzzy` and replaces `ranges` with the match's. */
export const PALETTE_HELP_ROWS: readonly PaletteRow[] = [
  {
    key: "help:terms",
    ref: "help:terms",
    section: "Help",
    label: "Show every term",
    hint: "?",
    ranges: [],
    action: { kind: "terms" },
    disabledReason: "",
  },
  {
    key: "help:tour",
    ref: "help:tour",
    section: "Help",
    label: "Take the tour",
    hint: "Help",
    ranges: [],
    action: { kind: "tour" },
    disabledReason: "",
  },
];

/** The projects a bar can actually switch to: none unless there are at least two, and never the
 *  one already open. */
function switchableProjects(projects: readonly PaletteProject[], activeSlug: string): readonly PaletteProject[] {
  if (projects.length < 2) return [];
  return projects.filter((project) => project.slug !== activeSlug);
}

/** A command's OWN key of `commandReasons` — never an inherited one, so a `Record` built over a
 *  prototype (as a test's own probe does) never leaks a reason a command was not actually given. */
function ownCommandReason(commandReasons: Readonly<Record<string, string>>, command: string): string {
  return Object.prototype.hasOwnProperty.call(commandReasons, command) ? commandReasons[command] : "";
}

/** The row a remembered ref names, resolved against the CURRENT targets, switchable projects and
 *  command reasons — not only the rows a limited section currently lists — or `null` when the ref
 *  names nothing anymore (a deleted task, a project that is no longer switchable, or a command
 *  that is no longer listed). */
function refRow(
  ref: string,
  targets: readonly JumpTarget[],
  switchable: readonly PaletteProject[],
  commandReasons: Readonly<Record<string, string>>,
): { label: string; hint: string; action: PaletteAction; disabledReason: string } | null {
  if (ref.startsWith("jump:")) {
    const id = ref.slice("jump:".length);
    const target = targets.find((t) => t.id === id);
    return target
      ? { label: target.label, hint: target.kind, action: { kind: "jump", nodeId: target.nodeId }, disabledReason: "" }
      : null;
  }
  if (ref.startsWith("project:")) {
    const slug = ref.slice("project:".length);
    const project = switchable.find((p) => p.slug === slug);
    return project
      ? { label: project.name, hint: project.slug, action: { kind: "project", slug: project.slug }, disabledReason: "" }
      : null;
  }
  if (ref.startsWith("command:")) {
    const command = ref.slice("command:".length);
    const found = paletteCommandOf(command);
    if (found === null) return null;
    const reason = ownCommandReason(commandReasons, command);
    return { label: found.title, hint: reason, action: { kind: "command", command }, disabledReason: reason };
  }
  const help = PALETTE_HELP_ROWS.find((row) => row.ref === ref);
  return help ? { label: help.label, hint: help.hint, action: help.action, disabledReason: "" } : null;
}

/** THE COMMANDS SECTION (DECISION F044 D3 (1)): "" for a blank query; otherwise the routed
 *  command first (its ranked row when the fuzzy rule also matched it, else one with no range),
 *  never twice, then the rest of the fuzzy-ranked titles, the whole cut at `COMMAND_RESULT_LIMIT`. */
function buildCommandRows(
  query: string,
  commandReasons: Readonly<Record<string, string>>,
  focusedTaskId: string,
): PaletteRow[] {
  if (query.trim() === "") return [];

  const ranked = rankFuzzy(PALETTE_COMMANDS, query, (entry) => entry.title);
  const route = routeBarText(query, focusedTaskId);
  const routedCommand = route.kind === "command" ? route.command : null;

  const ordered: { entry: PaletteCommand; ranges: readonly FuzzyRange[] }[] = [];
  if (routedCommand !== null) {
    const hit = ranked.find(({ item }) => item.command === routedCommand);
    const found = hit ? hit.item : paletteCommandOf(routedCommand);
    if (found !== null) {
      ordered.push({ entry: found, ranges: hit ? hit.match.ranges : [] });
    }
  }
  for (const { item, match } of ranked) {
    if (item.command === routedCommand) continue;
    ordered.push({ entry: item, ranges: match.ranges });
  }

  return ordered.slice(0, COMMAND_RESULT_LIMIT).map(({ entry, ranges }) => {
    const reason = ownCommandReason(commandReasons, entry.command);
    return {
      key: `command:${entry.command}`,
      ref: `command:${entry.command}`,
      section: "Commands",
      label: entry.title,
      hint: reason,
      ranges,
      action: { kind: "command", command: entry.command },
      disabledReason: reason,
    };
  });
}

/** THE ASK ROW (DECISION F044 D4 (1)): the query, its white space folded to single spaces and its
 *  ends trimmed, handed to the chat. Never remembered — its `ref` names nothing `refRow` resolves. */
export function askRow(query: string): PaletteRow {
  const text = query.replace(/\s+/g, " ").trim();
  return {
    key: "ask",
    ref: "ask",
    section: "Ask",
    label: text,
    hint: PALETTE_ASK_HINT,
    ranges: [],
    action: { kind: "chat", text },
    disabledReason: "",
  };
}

/** The sheet's whole row list for one query: in "task" mode, the Jump rows alone; otherwise
 *  Recent (blank query only), then the Ask row when the routing rule reads a question or no other
 *  row matched, then Commands, then Jump, then Projects, then Help. */
export function buildPaletteRows(input: PaletteInput): PaletteRow[] {
  const isBlank = input.query.trim() === "";

  const jumpHits = rankJumpTargets(input.targets, input.query, JUMP_RESULT_LIMIT);
  const jumpRows: PaletteRow[] = jumpHits.map((hit) => ({
    key: `jump:${hit.target.id}`,
    ref: `jump:${hit.target.id}`,
    section: "Jump",
    label: hit.target.label,
    hint: hit.target.kind,
    ranges: hit.field === "label" ? hit.match.ranges : [],
    action: { kind: "jump", nodeId: hit.target.nodeId },
    disabledReason: "",
  }));

  if (input.mode === "task") {
    return jumpRows;
  }

  const switchable = switchableProjects(input.projects, input.activeSlug);
  const commandRows = buildCommandRows(input.query, input.commandReasons, input.focusedTaskId);

  const projectRows: PaletteRow[] = rankFuzzy(switchable, input.query, (project) => project.name)
    .slice(0, PROJECT_RESULT_LIMIT)
    .map(({ item, match }) => ({
      key: `project:${item.slug}`,
      ref: `project:${item.slug}`,
      section: "Projects",
      label: item.name,
      hint: item.slug,
      ranges: match.ranges,
      action: { kind: "project", slug: item.slug },
      disabledReason: "",
    }));

  const helpRows: PaletteRow[] = isBlank
    ? PALETTE_HELP_ROWS.slice()
    : rankFuzzy(PALETTE_HELP_ROWS, input.query, (row) => row.label).map(({ item, match }) => ({
        ...item,
        ranges: match.ranges,
      }));

  const recentRows: PaletteRow[] = [];
  if (isBlank) {
    for (const ref of input.recents) {
      const resolved = refRow(ref, input.targets, switchable, input.commandReasons);
      if (resolved !== null) {
        recentRows.push({
          key: `recent:${ref}`,
          ref,
          section: "Recent",
          label: resolved.label,
          hint: resolved.hint,
          ranges: [],
          action: resolved.action,
          disabledReason: resolved.disabledReason,
        });
      }
    }
  }

  const builtRows = [...recentRows, ...commandRows, ...jumpRows, ...projectRows, ...helpRows];

  if (!isBlank) {
    const route = routeBarText(input.query, input.focusedTaskId);
    if (route.kind === "chat" || builtRows.length === 0) {
      return [askRow(input.query), ...builtRows];
    }
  }

  return builtRows;
}

/** The chosen ref first, then the others without it, cut at `PALETTE_RECENT_LIMIT`. */
export function rememberPaletteRef(recents: readonly string[], ref: string): string[] {
  const rest = recents.filter((r) => r !== ref);
  return [ref, ...rest].slice(0, PALETTE_RECENT_LIMIT);
}

/** The stored array's string items, cut at the limit; nothing stored, a value that is not an
 *  array, bad JSON, or a storage that throws all answer `[]`. */
export function readPaletteRecents(storage: PaletteRecentsStorage): string[] {
  try {
    const raw = storage.getItem(PALETTE_RECENTS_KEY);
    if (raw === null) return [];
    const parsed: unknown = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed.filter((item): item is string => typeof item === "string").slice(0, PALETTE_RECENT_LIMIT);
  } catch {
    return [];
  }
}

/** `JSON.stringify` of the refs under the key, swallowing a throw — recording "recent" is
 *  best-effort, never load-bearing. */
export function writePaletteRecents(storage: PaletteRecentsStorage, recents: readonly string[]): void {
  try {
    storage.setItem(PALETTE_RECENTS_KEY, JSON.stringify(recents));
  } catch {
    // The storage is unavailable; there is nothing to record.
  }
}

/** The active row after a step of `delta` (1 down, -1 up): -1 for no rows; from outside the
 *  rows, the first going down and the last going up; otherwise one step with wrap-around. */
export function movePaletteCursor(count: number, index: number, delta: 1 | -1): number {
  if (count <= 0) return -1;
  if (index < 0 || index >= count) {
    return delta === 1 ? 0 : count - 1;
  }
  return (index + delta + count) % count;
}

/** The label cut at the ranges, in order, into pieces flagged `hit`; no piece is ever empty, and
 *  a range is clipped to the label. */
export function highlightPieces(label: string, ranges: readonly FuzzyRange[]): LabelPiece[] {
  const pieces: LabelPiece[] = [];
  let cursor = 0;
  for (const [start, end] of ranges) {
    const clippedStart = Math.max(0, Math.min(start, label.length));
    const clippedEnd = Math.max(clippedStart, Math.min(end, label.length));
    if (clippedStart > cursor) {
      pieces.push({ text: label.slice(cursor, clippedStart), hit: false });
    }
    if (clippedEnd > clippedStart) {
      pieces.push({ text: label.slice(clippedStart, clippedEnd), hit: true });
    }
    cursor = clippedEnd;
  }
  if (cursor < label.length) {
    pieces.push({ text: label.slice(cursor), hit: false });
  }
  return pieces;
}
