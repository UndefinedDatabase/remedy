import { describe, expect, it } from "vitest";
import { clusterBrainModel } from "./brainReducer";
import { CLUSTER_EXPECTED_MODEL, CLUSTER_INPUT_MODEL } from "./brainReducer.fixtures";
import { buildBrainLayout } from "./buildForceBrainModel";
import { expandClusterOf } from "./clusterExpansion";

// CLUSTER_INPUT_MODEL: task t1 with twelve runs; its clustered view keeps seq 5
// to 12 and folds seq 1 to 4 into `cluster:t1` (CLUSTER_EXPECTED_MODEL). The
// expected lists below are read off those two fixtures by hand.
describe("expandClusterOf", () => {
  const clustered = clusterBrainModel(CLUSTER_INPUT_MODEL);

  it("starts from the reducer's own clustered view", () => {
    expect(clustered).toEqual(CLUSTER_EXPECTED_MODEL);
  });

  it("puts the runs the chip stood for in the chip's place, in seq order", () => {
    const expanded = expandClusterOf(clustered, CLUSTER_INPUT_MODEL, "task:t1");
    expect(expanded.nodes.map((n) => n.id)).toEqual([
      "job:job-cluster", "task:t1",
      "run:t1:5", "run:t1:6", "run:t1:7", "run:t1:8", "run:t1:9", "run:t1:10", "run:t1:11", "run:t1:12",
      "run:t1:1", "run:t1:2", "run:t1:3", "run:t1:4",
    ]);
  });

  it("drops the chip's link and gives each run back its own", () => {
    const expanded = expandClusterOf(clustered, CLUSTER_INPUT_MODEL, "task:t1");
    const ids = expanded.links.map((l) => l.id);
    expect(ids).not.toContain("task:t1->cluster:t1");
    expect(ids.slice(-4)).toEqual(["task:t1->run:t1:1", "task:t1->run:t1:2", "task:t1->run:t1:3", "task:t1->run:t1:4"]);
    expect(ids).toHaveLength(CLUSTER_INPUT_MODEL.links.length);
  });

  it("keeps every other field of the clustered view, the core's state included", () => {
    const expanded = expandClusterOf(clustered, CLUSTER_INPUT_MODEL, "task:t1");
    expect([expanded.jobId, expanded.lastSeq, expanded.nodes[0]]).toEqual([clustered.jobId, clustered.lastSeq, clustered.nodes[0]]);
  });

  it("returns the clustered view itself for a task with no chip", () => {
    expect(expandClusterOf(clustered, CLUSTER_INPUT_MODEL, "task:none")).toBe(clustered);
  });
});

describe("buildBrainLayout with a focused task", () => {
  it("lays out every run of the focused task and no chip", () => {
    const layout = buildBrainLayout(CLUSTER_INPUT_MODEL, "task:t1");
    expect(layout.nodes.map((n) => n.kind).filter((k) => k === "cluster")).toEqual([]);
    expect(layout.nodes).toHaveLength(CLUSTER_INPUT_MODEL.nodes.length);
  });

  it("is the ordinary layout without a focus, or for a task with no chip", () => {
    const ordinary = buildBrainLayout(CLUSTER_INPUT_MODEL);
    expect(ordinary.nodes.some((n) => n.id === "cluster:t1")).toBe(true);
    expect(buildBrainLayout(CLUSTER_INPUT_MODEL, "task:none")).toEqual(ordinary);
  });
});
