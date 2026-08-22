import { describe, it, expect } from "vitest";
import { isActionKind, newestActionRow } from "./actionClass";
import { STREAM_EVENT_CATALOG } from "./humanizeCatalog";
import type { FeedRow } from "./feedRow";

function rowOf(seq: number, kind: string): FeedRow {
  return { seq, kind, line: kind, known: true, timestamp: "", outcome: "", receivedAtMs: 0, taskId: "" };
}

describe("isActionKind", () => {
  it("counts an unknown kind as action rather than demoting it", () => {
    expect(isActionKind("a_kind_no_catalog_has_heard_of")).toBe(true);
  });

  it("excludes the inspection suffixes the NowCard stays quiet about", () => {
    expect(isActionKind("brain_node_inspected")).toBe(false);
    expect(isActionKind("git_status_read")).toBe(false);
    expect(isActionKind("project_constitution_loaded")).toBe(false);
    expect(isActionKind("project_memory_recalled")).toBe(false);
    expect(isActionKind("readiness_assessed")).toBe(false);
  });

  it("excludes the named bookkeeping kinds no suffix rule catches", () => {
    expect(isActionKind("stream_cap_reached")).toBe(false);
    expect(isActionKind("token_policy_applied")).toBe(false);
  });

  it("keeps the kinds a human would call the agent working", () => {
    expect(isActionKind("task_run_started")).toBe(true);
    expect(isActionKind("verification_failed")).toBe(true);
    expect(isActionKind("source_patch_applied")).toBe(true);
  });

  it("leaves most of the catalog in the action class", () => {
    const kinds = Object.keys(STREAM_EVENT_CATALOG);
    expect(kinds.filter(isActionKind).length).toBeGreaterThan(kinds.length / 2);
  });
});

describe("newestActionRow", () => {
  it("is null when the stream has produced nothing", () => {
    expect(newestActionRow([])).toBeNull();
  });

  it("is null when every row is bookkeeping", () => {
    expect(newestActionRow([rowOf(1, "git_status_read")])).toBeNull();
  });

  it("returns the newest action row, skipping bookkeeping after it", () => {
    const rows = [rowOf(1, "task_run_started"), rowOf(2, "builder_started"), rowOf(3, "git_status_read")];
    expect(newestActionRow(rows)?.seq).toBe(2);
  });
});
