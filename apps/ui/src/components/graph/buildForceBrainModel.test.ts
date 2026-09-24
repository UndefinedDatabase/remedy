import { describe, it, expect } from "vitest";
import { seedBrainModel } from "./brainReducer";
import {
  CLUSTER_EXPECTED_MODEL, CLUSTER_INPUT_MODEL, GOLDEN_A_MODEL, GOLDEN_B_MODEL,
} from "./brainReducer.fixtures";
import {
  BRAIN_CORE_RADIUS, BRAIN_GOLDEN_ANGLE, BRAIN_RUN_DISTANCE, buildBrainLayout,
} from "./buildForceBrainModel";
import type { BrainModel } from "./brainOntology";
import type { BrainLayoutData } from "./forceBrainTypes";

/** Recursively freezes a value so a mutating write throws in strict mode
 *  (vitest's ESM test files run strict) — the no-mutation proof for
 *  buildBrainLayout below. */
function deepFreeze<T>(value: T): T {
  if (value && typeof value === "object" && !Object.isFrozen(value)) {
    Object.freeze(value);
    for (const child of Object.values(value as Record<string, unknown>)) {
      deepFreeze(child);
    }
  }
  return value;
}

/** Euclidean distance from the origin — every task sits BRAIN_TASK_RING_RADIUS
 *  from it (graph_spec §6 core-task distance), and every child
 *  BRAIN_RUN_DISTANCE from its task, not the origin (graph_spec §6
 *  task-run distance). */
function distance(ax: number, ay: number, bx = 0, by = 0): number {
  return Math.sqrt((ax - bx) ** 2 + (ay - by) ** 2);
}

/** Angle from the origin to (x, y), normalized to [0, 2π) so two angles a
 *  golden-angle apart can be diffed mod 2π without a sign ambiguity. */
function angleOf(x: number, y: number): number {
  const a = Math.atan2(y, x);
  return a < 0 ? a + 2 * Math.PI : a;
}

const EPS = 1e-9;

describe("buildBrainLayout", () => {
  describe("truth rule (graph_spec §8): output ids equal the clustered model's, in order", () => {
    it("golden B: clusterBrainModel(GOLDEN_B_MODEL) is unchanged (no task over threshold 8), so the layout's ids equal GOLDEN_B_MODEL's own ids", () => {
      const layout = buildBrainLayout(GOLDEN_B_MODEL);
      expect(layout.nodes.map((n) => n.id)).toEqual(GOLDEN_B_MODEL.nodes.map((n) => n.id));
      expect(layout.links.map((l) => l.id)).toEqual(GOLDEN_B_MODEL.links.map((l) => l.id));
    });

    it("the cluster fixture: buildBrainLayout(CLUSTER_INPUT_MODEL) clusters internally, so its ids equal CLUSTER_EXPECTED_MODEL's (11 finished + 1 open runs -> 7 kept + 1 open + 1 cluster node)", () => {
      const layout = buildBrainLayout(CLUSTER_INPUT_MODEL);
      expect(layout.nodes.map((n) => n.id)).toEqual(CLUSTER_EXPECTED_MODEL.nodes.map((n) => n.id));
      expect(layout.links.map((l) => l.id)).toEqual(CLUSTER_EXPECTED_MODEL.links.map((l) => l.id));
    });

    it("no decor, no invented node: layout node/link counts equal the clustered model's exactly", () => {
      const layout = buildBrainLayout(CLUSTER_INPUT_MODEL);
      expect(layout.nodes).toHaveLength(CLUSTER_EXPECTED_MODEL.nodes.length);
      expect(layout.links).toHaveLength(CLUSTER_EXPECTED_MODEL.links.length);
    });
  });

  it("pins the core at the origin, depth 0, radius 26 (graph_spec §4)", () => {
    const layout = buildBrainLayout(GOLDEN_B_MODEL);
    const core = layout.nodes.find((n) => n.kind === "job_core");
    expect(core).toMatchObject({ x: 0, y: 0, fx: 0, fy: 0, depth: 0, radius: BRAIN_CORE_RADIUS });
    expect(BRAIN_CORE_RADIUS).toBe(26);
  });

  it("every task sits BRAIN_TASK_RING_RADIUS (150) from the core, depth 1, radius 7 (graph_spec §4, §6)", () => {
    const layout = buildBrainLayout(GOLDEN_B_MODEL);
    const tasks = layout.nodes.filter((n) => n.kind === "task");
    expect(tasks).toHaveLength(2); // t1, t2
    for (const task of tasks) {
      expect(distance(task.x, task.y)).toBeCloseTo(150, 9);
      expect(task.depth).toBe(1);
      expect(task.radius).toBe(7);
    }
  });

  it("consecutive tasks by rank differ by the golden angle, mod 2π (graph_spec §6)", () => {
    // GOLDEN_B_MODEL: task:t1 rank 0, task:t2 rank 1 -> consecutive in angle order.
    // graph_spec §6 calls for "golden-angle" spacing; hand-derived here from
    // that constant's standard closed form (π·(3 − √5)), computed
    // independently of the exported BRAIN_GOLDEN_ANGLE so a mutation to that
    // constant's VALUE cannot make this expectation drift along with it.
    const layout = buildBrainLayout(GOLDEN_B_MODEL);
    const t1 = layout.nodes.find((n) => n.id === "task:t1")!;
    const t2 = layout.nodes.find((n) => n.id === "task:t2")!;
    const diff = (angleOf(t2.x, t2.y) - angleOf(t1.x, t1.y) + 2 * Math.PI) % (2 * Math.PI);
    const handDerivedGoldenAngle = Math.PI * (3 - Math.sqrt(5));
    const goldenModTau = handDerivedGoldenAngle % (2 * Math.PI);
    expect(Math.abs(diff - goldenModTau)).toBeLessThan(EPS);
  });

  it("the exported BRAIN_GOLDEN_ANGLE constant itself equals π·(3 − √5)", () => {
    expect(BRAIN_GOLDEN_ANGLE).toBeCloseTo(Math.PI * (3 - Math.sqrt(5)), 12);
  });

  it("the seed angle (task rank 0's own angle) is equal for the same job id and differs for two different job ids", () => {
    // seedAngle = 2π * the first draw of seededRng(model.jobId || "default"); task 0's
    // angle IS seedAngle (i = 0 * BRAIN_GOLDEN_ANGLE adds nothing), so comparing two
    // rank-0 tasks' angles is comparing the seed angles directly, with no need to
    // reimplement the RNG in this test.
    const taskSeed = [{ id: "t1", status: "pending", rank: 0 }];
    const jobOne = seedBrainModel("job-one", taskSeed);
    const jobOneAgain = seedBrainModel("job-one", taskSeed);
    const jobTwo = seedBrainModel("job-two", taskSeed);

    const angleOfRankZero = (model: BrainModel) => {
      const layout = buildBrainLayout(model);
      const task = layout.nodes.find((n) => n.kind === "task")!;
      return angleOf(task.x, task.y);
    };

    expect(angleOfRankZero(jobOne)).toBeCloseTo(angleOfRankZero(jobOneAgain), 9);
    expect(Math.abs(angleOfRankZero(jobOne) - angleOfRankZero(jobTwo))).toBeGreaterThan(EPS);
  });

  it("every child sits BRAIN_RUN_DISTANCE (34) from its TASK, not the core (graph_spec §6)", () => {
    const layout = buildBrainLayout(GOLDEN_B_MODEL);
    const byId = new Map(layout.nodes.map((n) => [n.id, n]));
    const children = layout.nodes.filter((n) => n.depth === 2);
    expect(children.length).toBeGreaterThan(0);
    for (const child of children) {
      const task = byId.get(child.parentId!)!;
      expect(distance(child.x, child.y, task.x, task.y)).toBeCloseTo(34, 9);
    }
    expect(BRAIN_RUN_DISTANCE).toBe(34);
  });

  it("a task's children are symmetric about its own angle (chronological fan, graph_spec §3): the offsets (k - (n-1)/2) always sum to 0", () => {
    // GOLDEN_A_MODEL's t1 has exactly 3 children (builder_run seq1, review_run seq2,
    // test_run seq3), ordered by seq: k=0,1,2, n=3 -> offsets -1, 0, +1 (rad 0.35 each)
    // -> offset angles -0.35, 0, +0.35 relative to the task's own angle: symmetric.
    const layout = buildBrainLayout(GOLDEN_A_MODEL);
    const task = layout.nodes.find((n) => n.kind === "task")!;
    const taskAngle = angleOf(task.x, task.y);
    const children = layout.nodes.filter((n) => n.parentId === task.id);
    expect(children).toHaveLength(3);
    const offsets = children.map((c) => {
      const raw = angleOf(c.x, c.y) - taskAngle;
      // fold into (-π, π] so the three offsets are comparable as signed values
      return raw > Math.PI ? raw - 2 * Math.PI : raw < -Math.PI ? raw + 2 * Math.PI : raw;
    });
    const sum = offsets.reduce((a, b) => a + b, 0);
    expect(Math.abs(sum)).toBeLessThan(1e-6);
  });

  it("labels: a seeded task's title when non-empty, else its bare id; every other node's label is empty", () => {
    const seeded = seedBrainModel("job-labels", [
      { id: "t1", status: "pending", rank: 0, title: "Fix the flaky test" },
      { id: "t2", status: "pending", rank: 1 },
    ]);
    const layout = buildBrainLayout(seeded);
    const t1 = layout.nodes.find((n) => n.id === "task:t1")!;
    const t2 = layout.nodes.find((n) => n.id === "task:t2")!;
    const core = layout.nodes.find((n) => n.kind === "job_core")!;
    expect(t1.label).toBe("Fix the flaky test");
    expect(t2.label).toBe("t2"); // "task:t2" with the "task:" prefix stripped
    expect(core.label).toBe("");
  });

  it("link depth/width: depth 1 core->task width 2.2, depth 2 task->child width 1.4 (graph_spec §6 trunk decay)", () => {
    const layout = buildBrainLayout(GOLDEN_B_MODEL);
    const coreLinks = layout.links.filter((l) => l.depth === 1);
    const childLinks = layout.links.filter((l) => l.depth === 2);
    expect(coreLinks).toHaveLength(2); // job->t1, job->t2
    expect(childLinks).toHaveLength(6); // t1's 5 runs + t2's 1 run
    expect(coreLinks.every((l) => l.width === 2.2)).toBe(true);
    expect(childLinks.every((l) => l.width === 1.4)).toBe(true);
  });

  it("active is true exactly on golden B's in-progress flows (graph_spec §7, §8)", () => {
    // GOLDEN_B_MODEL: task:t2 is "blocked" but its child run:t2:8 is "in_progress",
    // so BOTH job->t2 (task-with-in_progress-child) and t2->run:t2:8 (target itself
    // in_progress) are active; every other link's target is resolved (pass/blocked/fail)
    // with no in_progress descendant, so every other link is inactive.
    const layout = buildBrainLayout(GOLDEN_B_MODEL);
    const activeIds = layout.links.filter((l) => l.active).map((l) => l.id).sort();
    expect(activeIds).toEqual(["job:job-b->task:t2", "task:t2->run:t2:8"].sort());
  });

  it("is deterministic: two calls on the same model deepEqual", () => {
    const a = buildBrainLayout(GOLDEN_B_MODEL);
    const b = buildBrainLayout(GOLDEN_B_MODEL);
    expect(a).toEqual(b);
  });

  it("never mutates its input: a deep-frozen model does not throw", () => {
    const frozen: BrainModel = deepFreeze(structuredClone(GOLDEN_B_MODEL));
    let layout: BrainLayoutData | undefined;
    expect(() => { layout = buildBrainLayout(frozen); }).not.toThrow();
    expect(layout!.nodes.length).toBeGreaterThan(0);
  });
});
