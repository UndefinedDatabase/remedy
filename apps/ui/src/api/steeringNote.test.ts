import { describe, expect, it } from "vitest";
import { readSteeringNote, steeringFocusTaskId, steeringPlaceholder } from "./steeringNote";

describe("readSteeringNote", () => {
  it("reads a well-formed note", () => {
    const note = readSteeringNote({
      event: "steering_message_received",
      note: { message_id: "sm-0001", text: "watch the budget", channel: "cli",
              task_id: "task-1" },
    });
    expect(note).toEqual({
      messageId: "sm-0001", text: "watch the budget", channel: "cli", taskId: "task-1",
    });
  });

  it("keeps an empty task id: a job-wide note is not a malformed one", () => {
    const note = readSteeringNote({
      event: "steering_message_received",
      note: { message_id: "sm-0002", text: "hold off", channel: "door", task_id: "" },
    });
    expect(note?.taskId).toBe("");
  });

  it("answers null for any other event kind", () => {
    expect(readSteeringNote({
      event: "steering_message_consumed",
      note: { message_id: "sm-0001", text: "x", channel: "cli", task_id: "" },
    })).toBeNull();
  });

  it("answers null when note is missing or not an object", () => {
    expect(readSteeringNote({ event: "steering_message_received" })).toBeNull();
    for (const broken of [null, "a string", 7, []]) {
      expect(readSteeringNote({ event: "steering_message_received", note: broken })).toBeNull();
    }
  });

  it("answers null when a field is missing or not a string", () => {
    const base = { message_id: "sm-0001", text: "x", channel: "cli", task_id: "" };
    for (const field of ["message_id", "text", "channel", "task_id"]) {
      const note = { ...base, [field]: 42 };
      expect(readSteeringNote({ event: "steering_message_received", note })).toBeNull();
    }
  });

  it("answers null for a blank text, even after trimming", () => {
    const note = readSteeringNote({
      event: "steering_message_received",
      note: { message_id: "sm-0001", text: "   ", channel: "cli", task_id: "" },
    });
    expect(note).toBeNull();
  });
});

describe("steeringFocusTaskId", () => {
  const tasks = [{ id: "task-1", nodeId: "node-1" }, { id: "task-2", nodeId: "node-2" }];

  it("answers the id of the task whose nodeId matches", () => {
    expect(steeringFocusTaskId(tasks, "node-2")).toBe("task-2");
  });

  it("answers empty for a null nodeId", () => {
    expect(steeringFocusTaskId(tasks, null)).toBe("");
  });

  it("answers empty for a nodeId no task carries", () => {
    expect(steeringFocusTaskId(tasks, "node-9")).toBe("");
  });
});

describe("steeringPlaceholder", () => {
  it("names the task for a focused id", () => {
    expect(steeringPlaceholder("task-1")).toBe("Note for task task-1 — read at its next round");
  });

  it("names the whole job for an empty id", () => {
    expect(steeringPlaceholder("")).toBe("Note for the whole job — read at its next round");
  });
});
