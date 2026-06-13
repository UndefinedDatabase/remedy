import { describe, it, expect } from "vitest";
import { normalizeDashboardPayload } from "../../api/remedyApi";
import { buildForceBrainModel } from "./buildForceBrainModel";

function dashboardWithTasks(n: number) {
  const tasks = Array.from({ length: n }, (_, i) => ({
    id: `t${i}`, title: `Task number ${i}`, status: i % 2 === 0 ? "completed" : "pending",
    source: "real", related_node_id: `t${i}`,
  }));
  return normalizeDashboardPayload("job-1", { tasks, metrics: {} });
}

describe("buildForceBrainModel decorative-dot invariants", () => {
  it("decorative layout_only dots are never clickable", () => {
    const model = buildForceBrainModel(dashboardWithTasks(6), "large", "all");
    const decorative = model.nodes.filter(n => n.sourceKind === "layout_only" && n.kind !== "root");
    expect(decorative.length).toBeGreaterThan(0);
    expect(decorative.every(n => n.clickable === false)).toBe(true);
  });

  it("the root node is not clickable", () => {
    const model = buildForceBrainModel(dashboardWithTasks(4), "medium", "all");
    const root = model.nodes.find(n => n.kind === "root");
    expect(root?.clickable).toBe(false);
  });

  it("real clickable nodes equal the real graph node count (4 tasks -> 4 nodes)", () => {
    const dash = dashboardWithTasks(4);
    const model = buildForceBrainModel(dash, "large", "all");
    const clickable = model.nodes.filter(n => n.clickable && n.sourceKind === "real_brain");
    expect(clickable).toHaveLength(dash.graph.nodes.length);
    expect(clickable).toHaveLength(4);
  });

  it("decorative dots never exceed the cap of 90", () => {
    const model = buildForceBrainModel(dashboardWithTasks(60), "large", "all");
    const layoutOnly = model.nodes.filter(n => n.sourceKind === "layout_only");
    expect(layoutOnly.length).toBeLessThanOrEqual(90);
  });

  it("clickable count ignores decorative dots entirely", () => {
    const model = buildForceBrainModel(dashboardWithTasks(8), "large", "all");
    const clickableLayoutOnly = model.nodes.filter(n => n.clickable && n.sourceKind === "layout_only");
    expect(clickableLayoutOnly).toHaveLength(0);
  });
});
