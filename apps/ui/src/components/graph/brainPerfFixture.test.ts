import { describe, expect, it } from "vitest";
import { buildBrainLayout } from "./buildForceBrainModel";
import {
  BRAIN_PERF_STAGE1_NODES,
  BRAIN_PERF_STAGE6_NODES,
  brainPerfLedger,
  brainPerfModel,
} from "./brainPerfFixture";
import { rebuildBrainModel } from "./brainReducer";

// Row counts, independently derived from brainPerfFixture.ts's own arithmetic
// comment (not read off a run): a non-leaveOpen normal task emits 8 rows
// (3 task_run_started + 3 task_round_completed + 1 verification_passed + 1
// task_run_completed), a leaveOpen one emits 5 (3 task_run_started + 2
// task_round_completed, its last round's review skipped). Stage 1 has N=26
// normal tasks with L=6 leaveOpen (t=0,5,10,15,20,25): (26-6)*8 + 6*5 = 190.
// Stage 6 has N=65 with L=13 (t=0,5,...,60): (65-13)*8 + 13*5 = 481.
const STAGE1_ROW_COUNT = 190;
const STAGE6_ROW_COUNT = 481;

describe("brainPerfFixture", () => {
  it("stage 1 lands exactly BRAIN_PERF_STAGE1_NODES nodes", () => {
    const layout = buildBrainLayout(brainPerfModel(BRAIN_PERF_STAGE1_NODES));
    expect(layout.nodes.length).toBe(BRAIN_PERF_STAGE1_NODES);
  });

  it("stage 6 lands exactly BRAIN_PERF_STAGE6_NODES nodes", () => {
    const layout = buildBrainLayout(brainPerfModel(BRAIN_PERF_STAGE6_NODES));
    expect(layout.nodes.length).toBe(BRAIN_PERF_STAGE6_NODES);
  });

  it("is deterministic: two calls deep-equal, for both stages", () => {
    expect(brainPerfModel(BRAIN_PERF_STAGE1_NODES)).toEqual(brainPerfModel(BRAIN_PERF_STAGE1_NODES));
    expect(brainPerfModel(BRAIN_PERF_STAGE6_NODES)).toEqual(brainPerfModel(BRAIN_PERF_STAGE6_NODES));
  });

  it("throws for a node target neither stage names", () => {
    expect(() => brainPerfModel(199)).toThrow();
  });

  for (const n of [BRAIN_PERF_STAGE1_NODES, BRAIN_PERF_STAGE6_NODES]) {
    describe(`stage n=${n}`, () => {
      it("has at least one active link (a leaveOpen task's builder run)", () => {
        const layout = buildBrainLayout(brainPerfModel(n));
        expect(layout.links.some((l) => l.active)).toBe(true);
      });

      it("every layout node has finite x and y", () => {
        const layout = buildBrainLayout(brainPerfModel(n));
        for (const node of layout.nodes) {
          expect(Number.isFinite(node.x)).toBe(true);
          expect(Number.isFinite(node.y)).toBe(true);
        }
      });
    });
  }

  it("stage 1's lastSeq equals its generated row count minus one", () => {
    const model = brainPerfModel(BRAIN_PERF_STAGE1_NODES);
    expect(model.lastSeq).toBe(STAGE1_ROW_COUNT - 1);
  });

  it("stage 6's lastSeq equals its generated row count minus one", () => {
    const model = brainPerfModel(BRAIN_PERF_STAGE6_NODES);
    expect(model.lastSeq).toBe(STAGE6_ROW_COUNT - 1);
  });

  it("stage 6's ledger runs from seq 0 without a hole and folds to exactly its model", () => {
    const { seeds, rows } = brainPerfLedger(BRAIN_PERF_STAGE6_NODES);
    expect(rows.map((r) => r.seq)).toEqual(Array.from({ length: STAGE6_ROW_COUNT }, (_, seq) => seq));
    expect(rebuildBrainModel(`perf-${BRAIN_PERF_STAGE6_NODES}`, seeds, rows)).toEqual(brainPerfModel(BRAIN_PERF_STAGE6_NODES));
    expect(() => brainPerfLedger(199)).toThrow();
  });
});
