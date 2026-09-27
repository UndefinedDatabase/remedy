// THE STEERING NOTE, as the cockpit shows and addresses it (F030 T003, DECISION F030 D3).
//
// The stream's `steering_message_received` frame carries a `note` field of exactly four
// values — the message id, its text, the channel it arrived on and the task it addresses
// (`ui_server._steering_note_summary_payload`, DECISION F030 D3). This module reads that
// field, CHECKING every value because the envelope is parsed JSON from a server this client
// does not control, and turns it into the row the feed shows as the operator's own line. It
// also resolves the dashboard's selected task to the id `job.steer` addresses, and gives the
// steering input the sentence that tells the operator where a note goes and when it is read.
//
// THE DELIBERATE ABSENCES. It renders nothing and knows no component. A frame whose `note`
// field is missing, malformed or carries a blank text answers `null`, so the feed falls back
// to the catalog's plain line rather than inventing a note.
import type { FocusableTask } from "./feedFocus";

/** The kind of the frame that carries a steering note's text. */
export const STEERING_NOTE_EVENT = "steering_message_received";

/** One note, as the stream carries it. */
export interface SteeringNote {
  messageId: string;
  text: string;
  channel: string;
  taskId: string;
}

/** The note a frame's envelope carries, or `null` when it carries none. `taskId` is "" for a
 *  job-wide note, which is not a malformed one. */
export function readSteeringNote(envelope: Record<string, unknown>): SteeringNote | null {
  if (envelope["event"] !== STEERING_NOTE_EVENT) {
    return null;
  }
  const field = envelope["note"];
  if (typeof field !== "object" || field === null) {
    return null;
  }
  const note = field as Record<string, unknown>;
  const messageId = note["message_id"];
  const text = note["text"];
  const channel = note["channel"];
  const taskId = note["task_id"];
  if (typeof messageId !== "string" || typeof text !== "string" || text.trim() === ""
      || typeof channel !== "string" || typeof taskId !== "string") {
    return null;
  }
  return { messageId, text, channel, taskId };
}

/** The `id` of the task whose `nodeId` is `nodeId`, or "" for a null `nodeId` or no match.
 *  `job.steer`'s argument is a task's `id`, never its `nodeId`, so the shell resolves the
 *  selection to it once here rather than in every reader of the selection. */
export function steeringFocusTaskId(
  tasks: readonly FocusableTask[],
  nodeId: string | null,
): string {
  if (nodeId === null) {
    return "";
  }
  const owner = tasks.find(task => task.nodeId === nodeId);
  return owner ? owner.id : "";
}

/** What the steering input's placeholder says: which task a note addresses, or the whole job
 *  when none is selected, and when it is read either way. T5_F030.md forbids copy that
 *  promises a conversation, so this never says "reply" or "answer" — only when it is read. */
export function steeringPlaceholder(taskId: string): string {
  return taskId === ""
    ? "Note for the whole job — read at its next round"
    : `Note for task ${taskId} — read at its next round`;
}
