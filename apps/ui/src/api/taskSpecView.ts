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

/** DECISION F026 D4 clause 1 — the closed set `RemedyTaskSpec.editState` may
 *  actually carry, other than `""` (not editable right now). Named rather
 *  than inlined so `taskEditAction` greps to the one place that owns it. */
const EDITABLE_STATES: ReadonlySet<string> = new Set(["waiting", "paused", "failed"]);

/** Everything the edit affordance needs to open a form for one task: the
 *  entry id the door's `job.edit-task` reads (`taskId`, NOT `plannedId`),
 *  the planned id for display, the spec version the form must send back as
 *  `expected_version`, the runtime state that gates the affordance, and the
 *  current fields to prefill it from. */
export interface TaskEditAction {
  taskId: string;
  plannedId: string;
  specVersion: number;
  editState: "waiting" | "paused" | "failed";
  current: RemedyTaskSpecFields;
}

/** DECISION F026 D4 clause 1: `null` unless the task's spec exists AND its
 *  `editState` is one of the three names a runtime edit is open for — a task
 *  with no spec (never mapped from the stored plan, or a payload whose own
 *  read failed) and a task whose `editState` is `""` (not editable right
 *  now, e.g. running or already applied) both answer `null`, so the popover
 *  offers the "Edit task" control only for a task this reading calls
 *  editable. */
export function taskEditAction(dashboard: RemedyDashboard, taskId: string): TaskEditAction | null {
  const spec = taskSpecOf(dashboard, taskId);
  if (!spec || !EDITABLE_STATES.has(spec.editState)) return null;
  return {
    taskId,
    plannedId: spec.plannedId,
    specVersion: spec.specVersion,
    editState: spec.editState as "waiting" | "paused" | "failed",
    current: spec.current,
  };
}

/** The edit form's own draft shape: every field as the browser edits it —
 *  `acceptance` and `files` as MULTI-LINE STRINGS, one entry per line, the
 *  same shape a `<textarea>` holds — never as the backend's arrays, which
 *  `changedTaskFields` below is the one place that converts between the two. */
export interface TaskEditDraft {
  title: string;
  goal: string;
  band: string;
  acceptance: string;
  files: string;
}

/** ONLY the backend fields `changedTaskFields` found changed, in the backend's
 *  OWN key spellings — `task_edit_runtime.edit_task_at_runtime`'s `fields`
 *  argument accepts exactly these five and nothing else. Every key is
 *  OPTIONAL and OMITTED rather than sent as the unchanged value, because an
 *  edit log that recorded every field on every save could never tell a real
 *  change from a field the operator never touched. */
export interface TaskEditFields {
  title?: string;
  goal?: string;
  acceptance?: string[];
  est_tokens_band?: string;
  files_hint?: string[];
}

/** One multi-line textarea's value, split into the backend's array shape:
 *  each line trimmed, then every blank line dropped — the same normalization
 *  `changesFrom` above already renders back with `"; "`, applied here on the
 *  way IN so a trailing blank line or stray leading space never becomes a
 *  spurious "changed" reading. */
function draftLines(text: string): string[] {
  return text.split("\n").map((line) => line.trim()).filter((line) => line !== "");
}

/** DECISION F026 D4 clause 2: the draft against the spec it was opened from,
 *  reduced to ONLY what differs — `{}` for an untouched draft, so Save stays
 *  disabled and, were it ever sent regardless, the door would see an empty
 *  `fields` and refuse it. `title` and `goal` compare as typed; `acceptance`
 *  and `files` compare the NORMALIZED lines against the current array, so
 *  re-typing the same criteria with extra blank lines is not a change. */
export function changedTaskFields(
  current: RemedyTaskSpecFields,
  draft: TaskEditDraft,
): TaskEditFields {
  const out: TaskEditFields = {};
  if (draft.title !== current.title) {
    out.title = draft.title;
  }
  if (draft.goal !== current.goal) {
    out.goal = draft.goal;
  }
  const acceptance = draftLines(draft.acceptance);
  if (acceptance.join("\n") !== current.acceptance.join("\n")) {
    out.acceptance = acceptance;
  }
  if (draft.band !== current.estTokensBand) {
    out.est_tokens_band = draft.band;
  }
  const files = draftLines(draft.files);
  if (files.join("\n") !== current.filesHint.join("\n")) {
    out.files_hint = files;
  }
  return out;
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
