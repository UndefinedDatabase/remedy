// T5_F044 T001, DECISION F044 D2 — the bar's dropdown sheet, its pure rules: the rows of its
// four sections (Recent, Jump, Projects, Help), ranked and highlighted by the fuzzy rule, the
// browser-remembered refs a chosen row leaves behind, the active-row cursor's wrap-around, and
// the label cut into highlighted pieces the sheet renders.
import type { FuzzyRange } from "./fuzzyMatch";
import { rankFuzzy } from "./fuzzyMatch";
import type { JumpTarget } from "./paletteJump";
import { JUMP_RESULT_LIMIT, rankJumpTargets } from "./paletteJump";

/** The sheet's four sections, in the order a row's section always renders under. */
export type PaletteSection = "Recent" | "Jump" | "Projects" | "Help";

export const PALETTE_SECTION_ORDER: readonly PaletteSection[] = ["Recent", "Jump", "Projects", "Help"];

/** What choosing a row does. */
export type PaletteAction =
  | { readonly kind: "jump"; readonly nodeId: string }
  | { readonly kind: "project"; readonly slug: string }
  | { readonly kind: "terms" }
  | { readonly kind: "tour" };

/** One row of the sheet. `ref` is what a browser remembers when the row is chosen — the same
 *  string as `key` for every row except a Recent one, whose `key` carries the `recent:` prefix
 *  its `ref` does not. */
export interface PaletteRow {
  readonly key: string;
  readonly ref: string;
  readonly section: PaletteSection;
  readonly label: string;
  readonly hint: string;
  readonly ranges: readonly FuzzyRange[];
  readonly action: PaletteAction;
}

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
  },
  {
    key: "help:tour",
    ref: "help:tour",
    section: "Help",
    label: "Take the tour",
    hint: "Help",
    ranges: [],
    action: { kind: "tour" },
  },
];

/** The projects a bar can actually switch to: none unless there are at least two, and never the
 *  one already open. */
function switchableProjects(projects: readonly PaletteProject[], activeSlug: string): readonly PaletteProject[] {
  if (projects.length < 2) return [];
  return projects.filter((project) => project.slug !== activeSlug);
}

/** The row a remembered ref names, resolved against the CURRENT targets and switchable
 *  projects — not only the rows a limited section currently lists — or `null` when the ref
 *  names nothing anymore (a deleted task, or a project that is no longer switchable). */
function refRow(
  ref: string,
  targets: readonly JumpTarget[],
  switchable: readonly PaletteProject[],
): { label: string; hint: string; action: PaletteAction } | null {
  if (ref.startsWith("jump:")) {
    const id = ref.slice("jump:".length);
    const target = targets.find((t) => t.id === id);
    return target ? { label: target.label, hint: target.kind, action: { kind: "jump", nodeId: target.nodeId } } : null;
  }
  if (ref.startsWith("project:")) {
    const slug = ref.slice("project:".length);
    const project = switchable.find((p) => p.slug === slug);
    return project ? { label: project.name, hint: project.slug, action: { kind: "project", slug: project.slug } } : null;
  }
  const help = PALETTE_HELP_ROWS.find((row) => row.ref === ref);
  return help ? { label: help.label, hint: help.hint, action: help.action } : null;
}

/** The sheet's whole row list for one query: Recent (blank query only), then Jump, then
 *  Projects, then Help. */
export function buildPaletteRows(input: PaletteInput): PaletteRow[] {
  const isBlank = input.query.trim() === "";
  const switchable = switchableProjects(input.projects, input.activeSlug);

  const jumpHits = rankJumpTargets(input.targets, input.query, JUMP_RESULT_LIMIT);
  const jumpRows: PaletteRow[] = jumpHits.map((hit) => ({
    key: `jump:${hit.target.id}`,
    ref: `jump:${hit.target.id}`,
    section: "Jump",
    label: hit.target.label,
    hint: hit.target.kind,
    ranges: hit.field === "label" ? hit.match.ranges : [],
    action: { kind: "jump", nodeId: hit.target.nodeId },
  }));

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
      const resolved = refRow(ref, input.targets, switchable);
      if (resolved !== null) {
        recentRows.push({
          key: `recent:${ref}`,
          ref,
          section: "Recent",
          label: resolved.label,
          hint: resolved.hint,
          ranges: [],
          action: resolved.action,
        });
      }
    }
  }

  return [...recentRows, ...jumpRows, ...projectRows, ...helpRows];
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
