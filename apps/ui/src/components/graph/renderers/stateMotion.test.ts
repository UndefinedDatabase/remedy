import { describe, expect, it } from "vitest";
import type { NodeState } from "../brainOntology";
import { rebuildBrainModel } from "../brainReducer";
import { BRAIN_DEMO_JOB_ID, BRAIN_DEMO_TASKS, brainDemoRows } from "../brainDemoRecording";
import { dashboardBrainSeeds } from "../brainView";
import { buildBrainLayout } from "../buildForceBrainModel";
import type { BrainLayoutData, BrainLayoutNode } from "../forceBrainTypes";
import {
  COMPLETION_RIPPLE_SPREAD, STATE_TRANSITION_MS, brainNeedsAnimationFrames, layoutHasPulse,
  scheduleStateTransitions, transitionFrameAt,
} from "./stateMotion";
import type { BrainAnimationNeeds, StateTransition } from "./stateMotion";

function node(id: string, state: NodeState, kind: BrainLayoutNode["kind"] = "task"): BrainLayoutNode {
  return { id, kind, state, seq: 0, depth: 1, radius: 7, x: 0, y: 0, label: "" };
}
const layout = (...nodes: BrainLayoutNode[]): BrainLayoutData => ({ nodes, links: [] });

describe("scheduleStateTransitions", () => {
  it("schedules nothing on a first paint, for a node just born, or for an unchanged node", () => {
    expect(scheduleStateTransitions(null, layout(node("a", "pass")), 0, false)).toEqual([]);
    expect(scheduleStateTransitions(layout(), layout(node("a", "pass")), 0, false)).toEqual([]);
    expect(scheduleStateTransitions(layout(node("a", "pass")), layout(node("a", "pass")), 0, false)).toEqual([]);
  });

  it("schedules one crossfade per changed node, in the next layout's order, starting now", () => {
    const before = layout(node("a", "planned"), node("b", "in_progress"), node("c", "open"));
    const after = layout(node("c", "fail"), node("a", "in_progress"), node("b", "in_progress"));
    expect(scheduleStateTransitions(before, after, 1000, false)).toEqual([
      { id: "c", from: "open", to: "fail", startMs: 1000, durationMs: STATE_TRANSITION_MS, ripple: false },
      { id: "a", from: "planned", to: "in_progress", startMs: 1000, durationMs: STATE_TRANSITION_MS, ripple: false },
    ]);
  });

  it("ends a change into pass, and only a change into pass, in a completion ripple", () => {
    const before = layout(node("a", "in_progress"), node("b", "in_progress"));
    const after = layout(node("a", "pass"), node("b", "fail"));
    expect(scheduleStateTransitions(before, after, 0, false).map((t) => [t.id, t.ripple])).toEqual([["a", true], ["b", false]]);
  });

  it("leaves the job core, which keeps its own painter, out", () => {
    const before = layout(node("job:x", "planned", "job_core"));
    const after = layout(node("job:x", "pass", "job_core"));
    expect(scheduleStateTransitions(before, after, 0, false)).toEqual([]);
  });

  it("schedules nothing under reduced motion, so a change is drawn in its new state at once", () => {
    expect(scheduleStateTransitions(layout(node("a", "in_progress")), layout(node("a", "pass")), 0, true)).toEqual([]);
  });
});

describe("transitionFrameAt", () => {
  const toPass: StateTransition = { id: "a", from: "in_progress", to: "pass", startMs: 100, durationMs: 300, ripple: true };

  it("starts wholly in the old state with the ripple at the node's edge", () => {
    expect(transitionFrameAt(toPass, 100)).toEqual({ fromAlpha: 1, toAlpha: 0, ripple: { spread: 0, alpha: 1 }, done: false });
  });

  it("crossfades linearly and eases the ripple out as it fades", () => {
    const mid = transitionFrameAt(toPass, 250);
    expect(mid.fromAlpha).toBeCloseTo(0.5, 10);
    expect(mid.toAlpha).toBeCloseTo(0.5, 10);
    expect(mid.ripple?.spread).toBeCloseTo(COMPLETION_RIPPLE_SPREAD * (1 - 0.5 ** 3), 10);
    expect(mid.ripple?.alpha).toBeCloseTo(0.5, 10);
    expect(mid.done).toBe(false);
  });

  it("ends wholly in the new state with no ripple, and stays there", () => {
    for (const now of [400, 10_000]) {
      expect(transitionFrameAt(toPass, now)).toEqual({ fromAlpha: 0, toAlpha: 1, ripple: null, done: true });
    }
  });

  it("never ripples a change that does not end in pass", () => {
    expect(transitionFrameAt({ ...toPass, to: "fail", ripple: false }, 250).ripple).toBeNull();
  });
});

describe("layoutHasPulse", () => {
  it("is true exactly when a non-core node is in progress", () => {
    expect(layoutHasPulse(layout(node("a", "pass"), node("b", "in_progress")))).toBe(true);
    expect(layoutHasPulse(layout(node("a", "pass"), node("job:x", "in_progress", "job_core")))).toBe(false);
  });
});

describe("brainNeedsAnimationFrames", () => {
  const still: BrainAnimationNeeds = {
    pageVisible: true, reducedMotion: false, birthsInFlight: false, transitionsInFlight: false, pulsing: false,
  };

  it("asks for no frame at all while the page is hidden, whatever is moving", () => {
    for (const reducedMotion of [false, true]) {
      expect(brainNeedsAnimationFrames({
        pageVisible: false, reducedMotion, birthsInFlight: true, transitionsInFlight: true, pulsing: true,
      })).toBe(false);
    }
  });

  it("keeps drawing while visible for a birth or a state change in flight", () => {
    expect(brainNeedsAnimationFrames({ ...still, birthsInFlight: true })).toBe(true);
    expect(brainNeedsAnimationFrames({ ...still, transitionsInFlight: true })).toBe(true);
  });

  it("keeps drawing for a pulse only when motion is not reduced", () => {
    expect(brainNeedsAnimationFrames({ ...still, pulsing: true })).toBe(true);
    expect(brainNeedsAnimationFrames({ ...still, pulsing: true, reducedMotion: true })).toBe(false);
  });

  it("rests when nothing moves", () => {
    expect(brainNeedsAnimationFrames(still)).toBe(false);
  });
});

describe("the demo recording's state changes", () => {
  // HAND-DERIVED from DECISION F019 D1's and DECISION F288 D3 (3)'s mapping,
  // never printed from the reducer: task_run_started puts its task in
  // progress and births its builder run in progress; task_round_completed
  // and task_round_repaired each birth a new review/repair run already in
  // its settled state (DECISION F019 D1: a birth is never a transition), so
  // neither changes anything; task_run_completed(pass) closes the run
  // task_run_started opened — the builder run keeps its birth seq as its id
  // for its whole life — and its task, to pass. Task A is
  // "fe1b5b487fda490f" (seq 0: started; 1: round-completed needs_repair; 2:
  // round-repaired changed; 3: round-completed pass; 4: run-completed pass)
  // and task B "4b3ddac9dba846af" the same shape at seq 5-9. The core is
  // left out: it keeps its own painter.
  const A = "fe1b5b487fda490f";
  const B = "4b3ddac9dba846af";
  const EXPECTED: Record<number, [string, NodeState, NodeState, boolean][]> = {
    0: [[`task:${A}`, "planned", "in_progress", false]],
    4: [[`task:${A}`, "in_progress", "pass", true], [`run:${A}:0`, "in_progress", "pass", true]],
    5: [[`task:${B}`, "planned", "in_progress", false]],
    9: [[`task:${B}`, "in_progress", "pass", true], [`run:${B}:5`, "in_progress", "pass", true]],
  };

  function replay(reducedMotion: boolean): Record<number, [string, NodeState, NodeState, boolean][]> {
    const seeds = dashboardBrainSeeds(BRAIN_DEMO_TASKS);
    const rows = brainDemoRows();
    let previous = buildBrainLayout(rebuildBrainModel(BRAIN_DEMO_JOB_ID, seeds, []));
    const seen: Record<number, [string, NodeState, NodeState, boolean][]> = {};
    rows.forEach((row, i) => {
      const next = buildBrainLayout(rebuildBrainModel(BRAIN_DEMO_JOB_ID, seeds, rows.slice(0, i + 1)));
      const changes = scheduleStateTransitions(previous, next, 0, reducedMotion);
      if (changes.length) seen[row.seq] = changes.map((t) => [t.id, t.from, t.to, t.ripple]);
      previous = next;
    });
    return seen;
  }

  it("animates every state change the recorded job made, frame by frame, and ripples each completion", () => {
    expect(replay(false)).toEqual(EXPECTED);
  });

  it("animates none of them under reduced motion", () => {
    expect(replay(true)).toEqual({});
  });
});
