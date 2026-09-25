import { describe, expect, it } from "vitest";
import type { BrainLayoutData, BrainLayoutLink, BrainLayoutNode } from "./forceBrainTypes";
import { ZOOM_HOME, type ZoomState } from "./semanticZoom";
import {
  ZOOM_CAMERA_MS, ZOOM_DIM_ALPHA, ZOOM_HOME_CAMERA, ZOOM_RUN_CAMERA, ZOOM_TASK_CAMERA,
  escapeWalksBack, focusTaskIdOf, zoomCamera, zoomCrumbLabel, zoomEmphasis,
} from "./zoomView";
import { ZOOM_IN_ABOVE, ZOOM_OUT_BELOW } from "./zoomWheel";

// A hand-written layout, so every expected set below is read off this
// literal and not computed by the layout code: core j, tasks a and b, a's
// runs a1 (in flight) and a2, b's run b1. Only the core-to-a and a-to-a1
// links are active, because a1 is the one run in flight.
function node(id: string, kind: BrainLayoutNode["kind"], depth: 0 | 1 | 2, x: number, y: number,
  parentId?: string, label = ""): BrainLayoutNode {
  return { id, kind, state: "planned", parentId, seq: 0, depth, radius: 5, x, y, label };
}
function link(source: string, target: string, active: boolean): BrainLayoutLink {
  return { id: `${source}->${target}`, source, target, depth: source === "job:j" ? 1 : 2, width: 1, active };
}
const LAYOUT: BrainLayoutData = {
  nodes: [
    node("job:j", "job_core", 0, 0, 0),
    node("task:a", "task", 1, 100, 0, "job:j", "Write the parser"),
    node("task:b", "task", 1, -100, 0, "job:j", "b"),
    node("run:a:1", "builder_run", 2, 130, 10, "task:a"),
    node("run:a:2", "review_run", 2, 130, -10, "task:a"),
    node("run:b:3", "test_run", 2, -130, 0, "task:b"),
  ],
  links: [
    link("job:j", "task:a", true),
    link("job:j", "task:b", false),
    link("task:a", "run:a:1", true),
    link("task:a", "run:a:2", false),
    link("task:b", "run:b:3", false),
  ],
};
const TA: ZoomState = { level: 1, focusId: "task:a", tab: null };
const TB: ZoomState = { level: 1, focusId: "task:b", tab: null };
const RA2: ZoomState = { level: 2, focusId: "run:a:2", tab: null };
const EA2: ZoomState = { level: 3, focusId: "run:a:2", tab: "diff" };

describe("the constants", () => {
  it("dim to graph_spec §10's 25% and move the camera over --remedy-dur-slow", () => {
    expect(ZOOM_DIM_ALPHA).toBe(0.25);
    expect(ZOOM_CAMERA_MS).toBe(350);
  });

  it("land every level's camera on the side of the wheel thresholds that level belongs to", () => {
    expect(ZOOM_HOME_CAMERA).toBeGreaterThanOrEqual(ZOOM_OUT_BELOW);
    expect(ZOOM_HOME_CAMERA).toBeLessThanOrEqual(ZOOM_IN_ABOVE);
    expect(ZOOM_TASK_CAMERA).toBeGreaterThan(ZOOM_IN_ABOVE);
    expect(ZOOM_RUN_CAMERA).toBeGreaterThan(ZOOM_IN_ABOVE);
  });
});

describe("zoomEmphasis", () => {
  it("L0: nothing dims, nothing is labelled or ringed, every active branch glows", () => {
    const e = zoomEmphasis(LAYOUT, ZOOM_HOME);
    expect([...e.dimmed]).toEqual([]);
    expect([...e.labelled]).toEqual([]);
    expect(e.ringId).toBeNull();
    expect([...e.glowing].sort()).toEqual(["job:j->task:a", "task:a->run:a:1"]);
  });

  it("L1 on a: b and b's run dim, the core does not; a is labelled and ringed; a's active links glow", () => {
    const e = zoomEmphasis(LAYOUT, TA);
    expect([...e.dimmed].sort()).toEqual(["run:b:3", "task:b"]);
    expect([...e.labelled]).toEqual(["task:a"]);
    expect(e.ringId).toBe("task:a");
    expect([...e.glowing].sort()).toEqual(["job:j->task:a", "task:a->run:a:1"]);
  });

  it("L1 on b: a's branch dims and nothing glows, because b has no run in flight", () => {
    const e = zoomEmphasis(LAYOUT, TB);
    expect([...e.dimmed].sort()).toEqual(["run:a:1", "run:a:2", "task:a"]);
    expect([...e.glowing]).toEqual([]);
  });

  it("L2 and L3 on a run: its task's branch stays lit and the ring moves to the run", () => {
    for (const state of [RA2, EA2]) {
      const e = zoomEmphasis(LAYOUT, state);
      expect([...e.dimmed].sort()).toEqual(["run:b:3", "task:b"]);
      expect([...e.labelled]).toEqual(["task:a"]);
      expect(e.ringId).toBe("run:a:2");
    }
  });

  it("a focus the filtered layout does not hold dims nothing and labels nothing", () => {
    const e = zoomEmphasis(LAYOUT, { level: 1, focusId: "task:gone", tab: null });
    expect([...e.dimmed]).toEqual([]);
    expect([...e.labelled]).toEqual([]);
    expect([...e.glowing].sort()).toEqual(["job:j->task:a", "task:a->run:a:1"]);
  });

  it("focusTaskIdOf names the task at every level", () => {
    expect([ZOOM_HOME, TA, RA2, EA2].map((s) => focusTaskIdOf(LAYOUT, s))).toEqual([null, "task:a", "task:a", "task:a"]);
  });
});

describe("zoomCamera", () => {
  it("fits the organism at L0, centres the task at L1 and the run at L2 and L3", () => {
    expect(zoomCamera(LAYOUT, ZOOM_HOME)).toEqual({ x: 0, y: 0, k: 1 });
    expect(zoomCamera(LAYOUT, TA)).toEqual({ x: 100, y: 0, k: 2 });
    expect(zoomCamera(LAYOUT, RA2)).toEqual({ x: 130, y: -10, k: 2.4 });
    expect(zoomCamera(LAYOUT, EA2)).toEqual({ x: 130, y: -10, k: 2.4 });
  });

  it("stays put when the focus has no position in this layout", () => {
    expect(zoomCamera(LAYOUT, { level: 1, focusId: "task:gone", tab: null })).toBeNull();
  });
});

describe("zoomCrumbLabel", () => {
  it("reads Job, the task's own label, and the run's legend name", () => {
    expect(zoomCrumbLabel({ level: 0, nodeId: null, current: false }, LAYOUT)).toBe("Job");
    expect(zoomCrumbLabel({ level: 1, nodeId: "task:a", current: false }, LAYOUT)).toBe("Write the parser");
    expect(zoomCrumbLabel({ level: 2, nodeId: "run:a:2", current: true }, LAYOUT)).toBe("Review run");
  });

  it("falls back to the level's word when the layout lacks the node", () => {
    expect(zoomCrumbLabel({ level: 1, nodeId: "task:gone", current: true }, LAYOUT)).toBe("Task");
    expect(zoomCrumbLabel({ level: 2, nodeId: "run:gone:1", current: true }, LAYOUT)).toBe("Run");
  });
});

describe("escapeWalksBack", () => {
  it("walks back from the page and from buttons", () => {
    expect(escapeWalksBack(null, false)).toBe(true);
    expect(escapeWalksBack({ tagName: "BODY" }, false)).toBe(true);
    expect(escapeWalksBack({ tagName: "button" }, false)).toBe(true);
  });

  it("leaves Escape to text fields and to an open dialog", () => {
    for (const tagName of ["INPUT", "textarea", "SELECT"]) expect(escapeWalksBack({ tagName }, false)).toBe(false);
    expect(escapeWalksBack({ tagName: "DIV", isContentEditable: true }, false)).toBe(false);
    expect(escapeWalksBack({ tagName: "BODY" }, true)).toBe(false);
  });
});
