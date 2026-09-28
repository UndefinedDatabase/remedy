import { describe, expect, it } from "vitest";
import { BRAIN_DEMO_FRAMES, BRAIN_DEMO_JOB_ID, brainDemoRows } from "../graph/brainDemoRecording";
import { decodeStoryExport, storyExportVersionLine, STORY_EXPORT_SCHEMA, STORY_EXPORT_UNREADABLE_LINE } from "./storyExport";

// HAND-DERIVED: a story payload shaped exactly as
// `packages/orchestration/story_export.py`'s `build_story_payload` would write
// it for the demo recording (`brainDemoRecording.ts`) — the same job id, task
// ids and titles, and `BRAIN_DEMO_FRAMES` reused directly as `frames`, so
// `rows` below can be checked against `brainDemoRows()` without recomputing
// anything the code under test also computes.
function demoPayload(): unknown {
  return {
    schema: STORY_EXPORT_SCHEMA,
    job_id: BRAIN_DEMO_JOB_ID,
    dashboard: {
      tasks: [
        { id: "fe1b5b487fda490f", title: "Deliver src/main.py", status: "completed", related_node_id: "fe1b5b487fda490f" },
        { id: "4b3ddac9dba846af", title: "Deliver README.md", status: "completed", related_node_id: "4b3ddac9dba846af" },
      ],
      live: { running: false },
      story: { step_ms: 300, chapter_pause_ms: 900 },
    },
    frames: BRAIN_DEMO_FRAMES,
    ownership: { schema: "remedy.ownership.v1", job_id: BRAIN_DEMO_JOB_ID, entries: [], error: "" },
  };
}

describe("decodeStoryExport", () => {
  it("reads the demo recording's shape ok: rows, job id, tasks, live, story and ownership", () => {
    const result = decodeStoryExport(demoPayload());
    expect(result.ok).toBe(true);
    if (!result.ok) return;
    expect(result.story.rows).toEqual(brainDemoRows());
    expect(result.story.dashboard.jobId).toBe(BRAIN_DEMO_JOB_ID);
    expect(result.story.dashboard.tasks.map((t) => t.id)).toEqual(["fe1b5b487fda490f", "4b3ddac9dba846af"]);
    expect(result.story.dashboard.tasks.map((t) => t.label)).toEqual(["Deliver src/main.py", "Deliver README.md"]);
    expect(result.story.dashboard.live.running).toBe(false);
    expect(result.story.dashboard.story).toEqual({ step_ms: 300, chapter_pause_ms: 900 });
    expect(result.story.ownership).toEqual({
      schema: "remedy.ownership.v1", jobId: BRAIN_DEMO_JOB_ID, entries: [], error: "",
    });
  });

  it("refuses a payload naming remedy.story.v2 with its version line", () => {
    const payload = demoPayload() as Record<string, unknown>;
    const result = decodeStoryExport({ ...payload, schema: "remedy.story.v2" });
    expect(result).toEqual({ ok: false, message: storyExportVersionLine("remedy.story.v2") });
  });

  it("reads the unreadable line for null, an array, a string, and every structurally malformed payload", () => {
    const payload = demoPayload() as Record<string, unknown>;
    const cases: unknown[] = [
      null,
      [],
      "not a story export",
      { job_id: BRAIN_DEMO_JOB_ID, dashboard: payload.dashboard, frames: [] }, // no schema
      { ...payload, job_id: 7 }, // a number job id
      { ...payload, dashboard: [] }, // an array dashboard
      { ...payload, frames: {} }, // an object for frames
      { ...payload, frames: [{ event: {} }] }, // a frame with no seq
    ];
    for (const c of cases) {
      expect(decodeStoryExport(c)).toEqual({ ok: false, message: STORY_EXPORT_UNREADABLE_LINE });
    }
  });

  it("an unreadable ownership view reads ok with ownership null", () => {
    const payload = demoPayload() as Record<string, unknown>;
    const result = decodeStoryExport({ ...payload, ownership: { schema: "not-the-ownership-schema" } });
    expect(result.ok).toBe(true);
    if (result.ok) expect(result.story.ownership).toBeNull();
  });
});
