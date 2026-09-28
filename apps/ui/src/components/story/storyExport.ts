// T5_F039.md T003, DECISION F039 D7 — the story's DATA half read back: decodes
// exactly what `packages/orchestration/story_export.py`'s `build_story_payload`
// writes, through the cockpit's own decoders — `normalizeDashboardPayload`,
// `feedRowOf` and `decodeOwnershipView` — never a second reading of the same
// shapes. Remedy deliberately refuses another schema rather than guess at its
// shape: a story exported by a version of Remedy this player does not
// recognise reads as unreadable, never as a best-effort partial render.
import { normalizeDashboardPayload } from "../../api/remedyApi";
import type { RemedyDashboard } from "../../api/types";
import { feedRowOf } from "../../api/feedRow";
import type { FeedRow } from "../../api/feedRow";
import { decodeOwnershipView } from "../../api/ownership";
import type { OwnershipView } from "../../api/ownership";

export const STORY_EXPORT_SCHEMA = "remedy.story.v1";

/** The exported page's own element id (F039 T003, DECISION F039 D8): the one place
 *  `packages/orchestration/story_export.py`'s `render_story_html` writes the payload's JSON,
 *  and the one place `storyPlayerMain.tsx` reads it back. Pinned equal in both languages by
 *  `tests/orchestration/test_story_export.py`. */
export const STORY_DATA_ELEMENT_ID = "remedy-story-data";

/** The one line a decoded story shows for a payload this player cannot read at
 *  all: not a plain object, missing its schema, or carrying a field of the
 *  wrong shape. Never the server's own error text. */
export const STORY_EXPORT_UNREADABLE_LINE = "This story's data could not be read.";

/** The one line a decoded story shows for a payload naming a schema OTHER than
 *  `STORY_EXPORT_SCHEMA`: this player recognises the shape well enough to know
 *  it is a story, and well enough to know it is not this one. */
export function storyExportVersionLine(schema: string): string {
  return `This story was written by a version of Remedy this player does not read (${schema}).`;
}

/** A decoded export: the same dashboard shape the live cockpit renders, the
 *  event rows through the cockpit's own frame parser, and the ownership view
 *  — `null` when the export's own `ownership` field could not be read. */
export interface StoryExport {
  dashboard: RemedyDashboard;
  rows: FeedRow[];
  ownership: OwnershipView | null;
}

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isFrame(value: unknown): value is { seq: number; event: unknown } {
  return isPlainObject(value) && typeof value["seq"] === "number";
}

/** Decode one exported story payload. NEVER THROWS: every failure — a payload
 *  that is not a plain object, one naming another schema, one missing a
 *  required field, or one whose frames are malformed — answers `{ ok: false,
 *  message }` with a fixed line rather than propagating a parse error to the
 *  player. */
export function decodeStoryExport(raw: unknown): { ok: true; story: StoryExport } | { ok: false; message: string } {
  if (!isPlainObject(raw)) {
    return { ok: false, message: STORY_EXPORT_UNREADABLE_LINE };
  }
  const schema = raw["schema"];
  if (typeof schema === "string" && schema !== STORY_EXPORT_SCHEMA) {
    return { ok: false, message: storyExportVersionLine(schema) };
  }
  const jobId = raw["job_id"];
  const dashboard = raw["dashboard"];
  const frames = raw["frames"];
  if (
    typeof schema !== "string"
    || typeof jobId !== "string"
    || !isPlainObject(dashboard)
    || !Array.isArray(frames)
  ) {
    return { ok: false, message: STORY_EXPORT_UNREADABLE_LINE };
  }
  if (!frames.every(isFrame)) {
    return { ok: false, message: STORY_EXPORT_UNREADABLE_LINE };
  }
  return {
    ok: true,
    story: {
      dashboard: normalizeDashboardPayload(jobId, dashboard),
      rows: frames.map((frame) => feedRowOf(frame, 0)),
      ownership: decodeOwnershipView(raw["ownership"]),
    },
  };
}

/** Read the story embedded in the exported page's own `<script type="application/json"
 *  id={STORY_DATA_ELEMENT_ID}>` element (F039 T003, DECISION F039 D8): `text` absent (the
 *  element itself is missing) and a `text` `JSON.parse` cannot read both answer the same
 *  unreadable line `decodeStoryExport` uses for any other unrecognised shape; anything that
 *  parses goes through `decodeStoryExport`, never a second reading of its rules. */
export function readEmbeddedStory(
  text: string | null,
): { ok: true; story: StoryExport } | { ok: false; message: string } {
  if (text === null) {
    return { ok: false, message: STORY_EXPORT_UNREADABLE_LINE };
  }
  try {
    return decodeStoryExport(JSON.parse(text));
  } catch {
    return { ok: false, message: STORY_EXPORT_UNREADABLE_LINE };
  }
}
