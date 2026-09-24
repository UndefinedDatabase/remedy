/**
 * The learning overlay's pure half (T5_F265 T002, DECISION F265 D3).
 *
 * The overlay renders the lessons the teacher STORED, one per completed task, as the job's
 * lessons route serves them (`GET /api/jobs/<job_id>/lessons`, DECISION F265 D2). This module
 * decodes that envelope, builds its path, and holds every rule the overlay applies: which
 * lesson opens first, which neighbours next and previous reach, what a task without a lesson
 * says, and when a stream frame means the index is worth reading again. Each row also carries
 * the CLI commands its task's diff touched, with the catalog's shipped description, which the
 * overlay's Commands mode shows (T003, DECISION F265 D4).
 *
 * IT OPENS NO SOCKET, READS NO CLOCK AND KEEPS NO STORAGE: the one read goes through
 * `loadLessonsIndex` in `remedyApi.ts`, and the component owns nothing but its selection.
 * The cockpit has no DOM harness (DECISION F031 D5), so a rule that lived in the component
 * would be a rule no test could see.
 *
 * THE DECODER REFUSES WHOLE. A row it cannot read makes the whole index unreadable rather than
 * silently shorter: an index that quietly drops a task is the thin lesson presenting itself as
 * complete that T5_F265.md forbids.
 */

/** The run-log event a stored lesson is announced by (DECISION F265 D2). */
export const LESSON_WRITTEN_EVENT = "task_lesson_written";
/** A stored lesson with a summary to read; every other status carries only a reason. */
export const LESSON_STATUS_READY = "ready";

export interface LessonConstruct { name: string; what: string; whyHere: string; judgement: string }

export interface LessonCommand { commandId: string; invocation: string; description: string }

/** What the overlay shows for the chosen task: its lesson, or the commands its change touched. */
export type LessonMode = "lesson" | "commands";

export interface LessonRow {
  taskId: string;
  title: string;
  runId: string;
  status: string;
  reason: string;
  summary: string;
  constructs: LessonConstruct[];
  ungrounded: string[];
  model: string;
  commands: LessonCommand[];
}

export interface LessonsIndex { jobId: string; lessonsEnabled: boolean; rows: LessonRow[] }

function recordOf(value: unknown): Record<string, unknown> | null {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>) : null;
}

function textOf(value: unknown): string | null {
  return typeof value === "string" ? value : null;
}

function constructOf(value: unknown): LessonConstruct | null {
  const construct = recordOf(value);
  if (construct === null) return null;
  const name = textOf(construct["name"]);
  const what = textOf(construct["what"]);
  const whyHere = textOf(construct["why_here"]);
  const judgement = textOf(construct["judgement"]);
  if (name === null || what === null || whyHere === null || judgement === null) return null;
  return { name, what, whyHere, judgement };
}

function commandOf(value: unknown): LessonCommand | null {
  const command = recordOf(value);
  if (command === null) return null;
  const commandId = textOf(command["command_id"]);
  const invocation = textOf(command["invocation"]);
  const description = textOf(command["description"]);
  if (commandId === null || invocation === null || description === null) return null;
  return { commandId, invocation, description };
}

function rowOf(value: unknown): LessonRow | null {
  const row = recordOf(value);
  if (row === null) return null;
  const taskId = textOf(row["task_id"]);
  const title = textOf(row["title"]);
  const runId = textOf(row["run_id"]);
  const status = textOf(row["status"]);
  const reason = textOf(row["reason"]);
  if (taskId === null || title === null || runId === null || status === null || reason === null) {
    return null;
  }
  // A row with no stored lesson carries none of the fields below; a stored one carries all.
  const summary = row["summary"] === undefined ? "" : textOf(row["summary"]);
  const model = row["model"] === undefined ? "" : textOf(row["model"]);
  const rawConstructs = row["constructs"] === undefined ? [] : row["constructs"];
  const rawUngrounded = row["ungrounded"] === undefined ? [] : row["ungrounded"];
  const rawCommands = row["commands"] === undefined ? [] : row["commands"];
  if (summary === null || model === null || !Array.isArray(rawConstructs)
      || !Array.isArray(rawUngrounded) || !Array.isArray(rawCommands)) {
    return null;
  }
  const constructs = rawConstructs.map(constructOf);
  const ungrounded = rawUngrounded.map(textOf);
  const commands = rawCommands.map(commandOf);
  if (constructs.some((c) => c === null) || ungrounded.some((u) => u === null)
      || commands.some((c) => c === null)) {
    return null;
  }
  return {
    taskId, title, runId, status, reason, summary, model,
    constructs: constructs as LessonConstruct[], ungrounded: ungrounded as string[],
    commands: commands as LessonCommand[],
  };
}

/** The lessons route's envelope, or `null` when any part of it cannot be read. Never throws. */
export function decodeLessonsIndex(raw: unknown): LessonsIndex | null {
  const payload = recordOf(raw);
  if (payload === null) return null;
  const jobId = textOf(payload["job_id"]);
  const lessonsEnabled = payload["lessons_enabled"];
  const rawRows = payload["lessons"];
  if (jobId === null || typeof lessonsEnabled !== "boolean" || !Array.isArray(rawRows)) return null;
  const rows = rawRows.map(rowOf);
  if (rows.some((r) => r === null)) return null;
  return { jobId, lessonsEnabled, rows: rows as LessonRow[] };
}

/** The job's lessons route, with the token the cockpit already carries. */
export function lessonsIndexPath(request: { jobId: string; token: string; baseUrl?: string }): string {
  const base = request.baseUrl ?? "";
  return `${base}/api/jobs/${encodeURIComponent(request.jobId)}/lessons`
    + `?token=${encodeURIComponent(request.token)}`;
}

/** The lesson the overlay opens on: the first stored one, or the first task when none is. */
export function firstLessonIndex(rows: readonly LessonRow[]): number {
  const first = rows.findIndex((row) => row.status === LESSON_STATUS_READY);
  return first < 0 ? 0 : first;
}

/** Where previous and next lead from `current`; `null` at either end. */
export function lessonNeighbours(count: number, current: number): {
  previous: number | null; next: number | null;
} {
  return {
    previous: current > 0 ? current - 1 : null,
    next: current + 1 < count ? current + 1 : null,
  };
}

/** The selection to show: the operator's choice while it still names a row, else the first. */
export function currentLessonIndex(rows: readonly LessonRow[], chosen: number | null): number {
  return chosen !== null && chosen >= 0 && chosen < rows.length ? chosen : firstLessonIndex(rows);
}

/** The newest stream position announcing a stored lesson, or 0; a change means "read again". */
export function lessonsRefreshKey(recent: readonly { seq: number; kind: string }[]): number {
  return recent.reduce(
    (newest, row) => (row.kind === LESSON_WRITTEN_EVENT && row.seq > newest ? row.seq : newest), 0);
}

/** The short tag the index shows beside a task's title. */
export function lessonIndexTag(row: LessonRow): string {
  return row.status === LESSON_STATUS_READY ? "Lesson" : "No lesson";
}

/** What a task without a readable lesson says, in the server's own reason. */
export function lessonStatusLine(row: LessonRow): string {
  return `There is no lesson for this task: ${row.reason}.`;
}

/** Where a stored lesson came from, and what the teacher named that the change does not use. */
export function lessonProvenanceLine(row: LessonRow): string {
  const made = `Written by the teacher (${row.model}) from the change this task recorded.`;
  const left = row.ungrounded.length;
  if (left === 0) return made;
  return `${made} ${left === 1 ? "One construct" : `${left} constructs`} the teacher named `
    + `but the change does not contain ${left === 1 ? "was" : "were"} left out.`;
}

/** The one line an index with nothing to read shows, or `null` when there is something. */
export function lessonsEmptyLine(index: LessonsIndex): string | null {
  if (index.rows.length === 0) return "This job has no tasks yet, so there are no lessons.";
  if (index.rows.some((row) => row.status === LESSON_STATUS_READY)) return null;
  return index.lessonsEnabled
    ? "No lesson has been stored yet; one appears after each task finishes."
    : "Lessons are switched off; the teacher.lessons setting turns them on.";
}

/** What the Commands mode says for a task whose change touched no CLI command, or `null`. */
export function lessonCommandsLine(row: LessonRow): string | null {
  return row.commands.length === 0 ? "This task's change touched no CLI command." : null;
}
