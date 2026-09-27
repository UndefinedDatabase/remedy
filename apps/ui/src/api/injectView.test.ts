import { describe, expect, it } from "vitest";
import {
  INJECTED_TASK_ORIGIN,
  ORIGIN_CHIP_TEXT,
  ORIGIN_CHIP_TITLE,
  taskOriginChip,
} from "./injectView";

describe("taskOriginChip", () => {
  it("answers the words for a task whose origin is human_injected", () => {
    expect(taskOriginChip({ origin: INJECTED_TASK_ORIGIN })).toBe(ORIGIN_CHIP_TEXT);
    expect(taskOriginChip({ origin: "human_injected" })).toBe("Added by you");
  });

  it("is null for a task with no origin at all", () => {
    expect(taskOriginChip({})).toBeNull();
  });

  it("is null for a task whose origin is the empty string", () => {
    expect(taskOriginChip({ origin: "" })).toBeNull();
  });

  it("is null for a task with any other origin", () => {
    expect(taskOriginChip({ origin: "planner" })).toBeNull();
  });

  it("is null for a null or undefined task", () => {
    expect(taskOriginChip(null)).toBeNull();
    expect(taskOriginChip(undefined)).toBeNull();
  });

  it("the title names the one sentence both mounts share", () => {
    expect(ORIGIN_CHIP_TITLE).toBe("You added this task while the job was running.");
  });
});
