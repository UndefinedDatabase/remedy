import { describe, it, expect } from "vitest";
import {
  LESSON_WRITTEN_EVENT,
  currentLessonIndex,
  lessonCommandsLine,
  decodeLessonsIndex,
  firstLessonIndex,
  lessonIndexTag,
  lessonNeighbours,
  lessonProvenanceLine,
  lessonStatusLine,
  lessonsEmptyLine,
  lessonsIndexPath,
  lessonsRefreshKey,
} from "./lessons";
import type { LessonRow } from "./lessons";
import { loadLessonsIndex } from "./remedyApi";

const READY = {
  task_id: "T001", title: "Cache the loads", run_id: "run-a", status: "ready", reason: "",
  lesson_id: "lesson-run-a", mission_id: "", model: "teacher-model",
  generated_at: "2026-09-24T00:00:00+00:00", diff_sha256: "ab",
  summary: "Caches file loads.",
  constructs: [{ name: "functools.lru_cache", what: "memoises", why_here: "repeat reads",
    judgement: "sound here" }],
  ungrounded: ["asyncio.gather"],
  commands: [{ command_id: "teacher.ask", invocation: "remedy teacher ask",
    description: "Ask the teacher." }],
};
const NONE = { task_id: "T002", title: "Not run", run_id: "", status: "none",
  reason: "this task has not run yet" };
const ENVELOPE = { job_id: "0a1b2c3d4e5f6a7b", lessons_enabled: true, lessons: [NONE, READY] };

function rowsOf(envelope: unknown): LessonRow[] {
  const index = decodeLessonsIndex(envelope);
  if (index === null) throw new Error("the envelope did not decode");
  return index.rows;
}

describe("decodeLessonsIndex", () => {
  it("reads a stored lesson and a task without one", () => {
    const index = decodeLessonsIndex(ENVELOPE);
    expect(index?.jobId).toBe("0a1b2c3d4e5f6a7b");
    expect(index?.lessonsEnabled).toBe(true);
    expect(index?.rows[1].constructs).toEqual([
      { name: "functools.lru_cache", what: "memoises", whyHere: "repeat reads", judgement: "sound here" }]);
    expect(index?.rows[0]).toEqual({ taskId: "T002", title: "Not run", runId: "", status: "none",
      reason: "this task has not run yet", summary: "", model: "", constructs: [], ungrounded: [],
      commands: [] });
    expect(index?.rows[1].commands).toEqual([
      { commandId: "teacher.ask", invocation: "remedy teacher ask", description: "Ask the teacher." }]);
  });

  it.each([
    ["no object", null],
    ["a list", []],
    ["no job id", { ...ENVELOPE, job_id: 7 }],
    ["a switch that is not a boolean", { ...ENVELOPE, lessons_enabled: "yes" }],
    ["lessons that are not a list", { ...ENVELOPE, lessons: {} }],
    ["a row with no status", { ...ENVELOPE, lessons: [{ ...NONE, status: undefined }] }],
    ["a construct with no judgement", { ...ENVELOPE, lessons: [{ ...READY,
      constructs: [{ name: "x", what: "y", why_here: "z" }] }] }],
    ["an ungrounded name that is not text", { ...ENVELOPE, lessons: [{ ...READY, ungrounded: [3] }] }],
    ["a command with no description", { ...ENVELOPE, lessons: [{ ...READY,
      commands: [{ command_id: "a.b", invocation: "remedy a b" }] }] }],
  ])("refuses the whole index for %s", (_label, raw) => {
    expect(decodeLessonsIndex(raw)).toBeNull();
  });
});

describe("the overlay's rules", () => {
  it("builds the route with the job id and token encoded", () => {
    expect(lessonsIndexPath({ jobId: "a/b", token: "t&k" }))
      .toBe("/api/jobs/a%2Fb/lessons?token=t%26k");
  });

  it("opens on the first stored lesson, or the first task when none is stored", () => {
    expect(firstLessonIndex(rowsOf(ENVELOPE))).toBe(1);
    expect(firstLessonIndex(rowsOf({ ...ENVELOPE, lessons: [NONE] }))).toBe(0);
  });

  it("keeps the operator's choice while it names a row", () => {
    const rows = rowsOf(ENVELOPE);
    expect(currentLessonIndex(rows, 0)).toBe(0);
    expect(currentLessonIndex(rows, 5)).toBe(1);
    expect(currentLessonIndex(rows, null)).toBe(1);
  });

  it("stops previous and next at the ends", () => {
    expect(lessonNeighbours(3, 0)).toEqual({ previous: null, next: 1 });
    expect(lessonNeighbours(3, 1)).toEqual({ previous: 0, next: 2 });
    expect(lessonNeighbours(3, 2)).toEqual({ previous: 1, next: null });
  });

  it("reads the index again only when the stream announces a newer lesson", () => {
    expect(lessonsRefreshKey([])).toBe(0);
    expect(lessonsRefreshKey([{ seq: 4, kind: LESSON_WRITTEN_EVENT }, { seq: 9, kind: "task_run_completed" },
      { seq: 7, kind: LESSON_WRITTEN_EVENT }])).toBe(7);
  });

  it("says why a task has no lesson, in the server's own reason", () => {
    const [none, ready] = rowsOf(ENVELOPE);
    expect(lessonStatusLine(none)).toBe("There is no lesson for this task: this task has not run yet.");
    expect([lessonIndexTag(none), lessonIndexTag(ready)]).toEqual(["No lesson", "Lesson"]);
  });

  it("names the model and what the teacher named that the change does not contain", () => {
    const ready = rowsOf(ENVELOPE)[1];
    expect(lessonProvenanceLine(ready)).toBe("Written by the teacher (teacher-model) from the change "
      + "this task recorded. One construct the teacher named but the change does not contain was left out.");
    expect(lessonProvenanceLine({ ...ready, ungrounded: [] }))
      .toBe("Written by the teacher (teacher-model) from the change this task recorded.");
  });

  it("gives an index with nothing to read one honest line", () => {
    expect(lessonsEmptyLine(decodeLessonsIndex(ENVELOPE)!)).toBeNull();
    expect(lessonsEmptyLine(decodeLessonsIndex({ ...ENVELOPE, lessons: [] })!))
      .toBe("This job has no tasks yet, so there are no lessons.");
    expect(lessonsEmptyLine(decodeLessonsIndex({ ...ENVELOPE, lessons: [NONE] })!))
      .toBe("No lesson has been stored yet; one appears after each task finishes.");
    expect(lessonsEmptyLine(decodeLessonsIndex({ ...ENVELOPE, lessons_enabled: false, lessons: [NONE] })!))
      .toBe("Lessons are switched off; the teacher.lessons setting turns them on.");
  });
});

describe("the Commands mode", () => {
  it("says so when a task's change touched no command", () => {
    const [none, ready] = rowsOf(ENVELOPE);
    expect(lessonCommandsLine(none)).toBe("This task's change touched no CLI command.");
    expect(lessonCommandsLine(ready)).toBeNull();
  });
});

describe("loadLessonsIndex", () => {
  it("reads the route through the injected fetcher", async () => {
    const asked: string[] = [];
    const index = await loadLessonsIndex({ jobId: "j1", token: "tok" }, async (path) => {
      asked.push(path);
      return ENVELOPE;
    });
    expect(asked).toEqual(["/api/jobs/j1/lessons?token=tok"]);
    expect(index?.rows.length).toBe(2);
  });

  it("answers null, never throws, when the read fails", async () => {
    const index = await loadLessonsIndex({ jobId: "j1", token: "tok" }, async () => {
      throw new Error("offline");
    });
    expect(index).toBeNull();
  });
});
