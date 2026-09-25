// THE TASK SPEC VIEW (DECISION F026 D3): pure functions of a `RemedyDashboard`
// that decide what an edited task's version chip and Versions list show. Nothing
// here reaches a fetch, a clock or a DOM — every answer is a function of the
// dashboard alone, exactly as `pauseView.ts` reads the pause section.
import type { RemedyDashboard, RemedyTaskSpec, RemedyTaskSpecFields } from "./types";

/** The task's spec from the dashboard's `task_specs` section, or `undefined`
 *  when the dashboard carries no entry for it — a task never mapped from the
 *  stored plan, or a payload whose own read failed. */
export function taskSpecOf(dashboard: RemedyDashboard, taskId: string): RemedyTaskSpec | undefined {
  return dashboard.taskSpecs.tasks[taskId];
}

/** Every task id the dashboard's `task_specs` section carries, mapped to its
 *  current spec version — the seed data the canvas (S5) paints a version
 *  chip from. */
export function taskSpecVersions(dashboard: RemedyDashboard): Readonly<Record<string, number>> {
  const out: Record<string, number> = {};
  for (const [taskId, spec] of Object.entries(dashboard.taskSpecs.tasks)) {
    out[taskId] = spec.specVersion;
  }
  return out;
}

/** DECISION F026 D3 clause 2: `v<n>` for a task edited at runtime — its spec
 *  version is 2 or more — else `null`. A task never edited shows no chip. */
export function versionChipLabel(spec: RemedyTaskSpec | undefined): string | null {
  if (!spec || spec.specVersion < 2) return null;
  return `v${spec.specVersion}`;
}

/** One changed field between two spec readings: its key, its human label,
 *  and the value shown before and after — a list joined by `"; "`. */
export interface TaskSpecVersionChange {
  field: string;
  label: string;
  before: string;
  after: string;
}

/** One row of the popover's Versions list: the version it names, whether it
 *  is the current spec, the task's state at that version, when it was
 *  archived (`""` for the current row, which was never archived), and the
 *  fields that changed from the row before it. */
export interface TaskSpecVersionRow {
  specVersion: number;
  current: boolean;
  state: string;
  archivedAt: string;
  changes: TaskSpecVersionChange[];
}

// Order DECISION F026 D3 clause 3 names: title, goal, acceptance, size band, files.
const CHANGE_FIELDS: ReadonlyArray<{ field: keyof RemedyTaskSpecFields; label: string }> = [
  { field: "title", label: "Title" },
  { field: "goal", label: "Goal" },
  { field: "acceptance", label: "Acceptance" },
  { field: "estTokensBand", label: "Size band" },
  { field: "filesHint", label: "Files" },
];

function shownValue(fields: RemedyTaskSpecFields, field: keyof RemedyTaskSpecFields): string {
  const value = fields[field];
  return Array.isArray(value) ? value.join("; ") : value;
}

function changesFrom(
  previous: RemedyTaskSpecFields | null,
  next: RemedyTaskSpecFields,
): TaskSpecVersionChange[] {
  if (!previous) return [];
  const changes: TaskSpecVersionChange[] = [];
  for (const { field, label } of CHANGE_FIELDS) {
    const before = shownValue(previous, field);
    const after = shownValue(next, field);
    if (before !== after) changes.push({ field, label, before, after });
  }
  return changes;
}

/** DECISION F026 D3 clause 3: `[]` unless the task's spec version is 2 or
 *  more, else one row per archived version in ascending order, then one for
 *  the current spec — each row's `changes` against the row before it. The
 *  first row (the task's very first spec) has nothing before it, so it
 *  changed nothing and its `changes` is empty. */
export function specVersionRows(spec: RemedyTaskSpec | undefined): TaskSpecVersionRow[] {
  if (!spec || spec.specVersion < 2) return [];

  const rows: TaskSpecVersionRow[] = [];
  let previous: RemedyTaskSpecFields | null = null;
  for (const version of spec.versions) {
    rows.push({
      specVersion: version.specVersion,
      current: false,
      state: version.state,
      archivedAt: version.archivedAt,
      changes: changesFrom(previous, version),
    });
    previous = version;
  }
  rows.push({
    specVersion: spec.specVersion,
    current: true,
    state: spec.editState,
    archivedAt: "",
    changes: changesFrom(previous, spec.current),
  });
  return rows;
}
