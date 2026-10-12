// F305 T002, DECISIONS F305 D1 and D2 — the cockpit's mission card seam. The envelopes below are
// shaped after what `project_missions_view` and `mission_orders_view` in
// `packages/orchestration/mission_cockpit.py` answer for an order over two repositories: two jobs
// in alpha's mission, one in beta's.
import { describe, expect, it } from "vitest";
import {
  MISSING_JOB_LABEL,
  MISSION_COCKPIT_VERSION,
  UNREADABLE_JOB_LABEL,
  chainReachLine,
  chipLabel,
  chipOpenable,
  decodeMissionOrders,
  decodeProjectMissions,
  earlierOrdersLine,
  missionCardLine,
  missionOrdersPath,
  orderUsageLine,
  projectMissionsPath,
} from "./missionCard";
import type { MissionChip } from "./missionCard";

const card = {
  mission_id: "m-alpha", goal: "Maintain alpha", status: "active",
  created_at: "2026-10-12T09:00:00+00:00", order_count: 1, job_count: 2,
};
const missionsEnvelope = {
  version: 1, project_id: "11111111-1111-4111-8111-111111111111", slug: "alpha",
  missions: [card], degraded: false, skipped_count: 0,
};
const chip = (jobId: string, slug: string, title: string): MissionChip => ({
  job_id: jobId, project_id: `${slug}-id`, slug, repo_name: slug, title, state: "completed",
});
const order = {
  order_id: "o-1", title: "Add a health route", created_at: "2026-10-12T09:00:00+00:00",
  kind: "build", sealed: false, correlation_id: "c-1", job_count: 2,
  usage: { calls: 2, tokens: { input: 150, output: 25, cache_read: 7, cache_creation: null } },
  chain: [chip("j1", "alpha", "alpha first"), chip("j2", "beta", "beta only"), chip("j3", "alpha", "alpha second")],
};
const ordersEnvelope = {
  version: 1, project_id: "11111111-1111-4111-8111-111111111111", slug: "alpha",
  mission_id: "m-alpha", goal: "Maintain alpha", orders: [order], earlier_orders: 0, degraded: false,
};

describe("decodeProjectMissions", () => {
  it("reads the server's envelope whole", () => {
    expect(decodeProjectMissions(missionsEnvelope)).toEqual(missionsEnvelope);
    expect(MISSION_COCKPIT_VERSION).toBe(1);
  });
  it("refuses another version, a missing project id or a missions value that is no array", () => {
    expect(decodeProjectMissions({ ...missionsEnvelope, version: 2 })).toBeNull();
    expect(decodeProjectMissions({ ...missionsEnvelope, project_id: 7 })).toBeNull();
    expect(decodeProjectMissions({ ...missionsEnvelope, missions: {} })).toBeNull();
    expect(decodeProjectMissions([missionsEnvelope])).toBeNull();
    expect(decodeProjectMissions(null)).toBeNull();
  });
  it("drops a card without a mission id and reads bad counts as zero", () => {
    const decoded = decodeProjectMissions({
      ...missionsEnvelope,
      missions: [{ goal: "no id" }, { ...card, order_count: -3, job_count: "two" }],
    });
    expect(decoded?.missions).toEqual([{ ...card, order_count: 0, job_count: 0 }]);
  });
});

describe("decodeMissionOrders", () => {
  it("reads the server's envelope whole", () => {
    expect(decodeMissionOrders(ordersEnvelope)).toEqual(ordersEnvelope);
  });
  it("refuses another version, a missing mission id or an orders value that is no array", () => {
    expect(decodeMissionOrders({ ...ordersEnvelope, version: 0 })).toBeNull();
    expect(decodeMissionOrders({ ...ordersEnvelope, mission_id: null })).toBeNull();
    expect(decodeMissionOrders({ ...ordersEnvelope, orders: "none" })).toBeNull();
  });
  it("keeps the row of jobs linked before order records and drops a chip without a job id", () => {
    const before = { ...order, order_id: "", chain: [{ slug: "alpha" }, chip("j9", "alpha", "old")] };
    const decoded = decodeMissionOrders({ ...ordersEnvelope, orders: [before, 5] });
    expect(decoded?.orders.map((row) => row.order_id)).toEqual([""]);
    expect(decoded?.orders[0].chain.map((c) => c.job_id)).toEqual(["j9"]);
  });
  it("reads a usage it cannot read as null calls and null tokens", () => {
    const decoded = decodeMissionOrders({ ...ordersEnvelope, orders: [{ ...order, usage: { calls: null } }] });
    expect(decoded?.orders[0].usage).toEqual({
      calls: null, tokens: { input: null, output: null, cache_read: null, cache_creation: null },
    });
  });
});

describe("the paths", () => {
  it("name the two routes with every part percent-encoded", () => {
    expect(projectMissionsPath({ project: "al pha", token: "t/1" })).toBe(
      "/api/projects/al%20pha/missions?token=t%2F1");
    expect(missionOrdersPath({ project: "alpha", missionId: "m/1", token: "t", baseUrl: "http://x" })).toBe(
      "http://x/api/projects/alpha/missions/m%2F1/orders?token=t");
  });
});

describe("the words", () => {
  it("say a mission's size", () => {
    expect(missionCardLine(card)).toBe("1 order · 2 jobs");
    expect(missionCardLine({ ...card, order_count: 3, job_count: 1 })).toBe("3 orders · 1 job");
  });
  it("say an order's calls and tokens and never a cost", () => {
    expect(orderUsageLine(order.usage)).toBe("2 model calls · 150 tokens in, 25 out");
    expect(orderUsageLine({ calls: 1, tokens: { input: null, output: 4, cache_read: null, cache_creation: null } }))
      .toBe("1 model call · 0 tokens in, 4 out");
    expect(orderUsageLine({ calls: 3, tokens: { input: null, output: null, cache_read: 1, cache_creation: null } }))
      .toBe("3 model calls · tokens not reported");
    expect(orderUsageLine({ calls: 0, tokens: order.usage.tokens })).toBe("No model calls");
    expect(orderUsageLine({ calls: null, tokens: order.usage.tokens })).toBe("Model calls: not readable");
    expect(orderUsageLine(order.usage)).not.toContain("$");
  });
  it("say how far a chain reached", () => {
    expect(chainReachLine(order.chain)).toBe("3 jobs in 2 projects");
    expect(chainReachLine([order.chain[0]])).toBe("1 job in 1 project");
  });
  it("label a chip by its project and its repository's folder", () => {
    expect(chipLabel(order.chain[1])).toBe("beta · beta");
    expect(chipLabel({ ...order.chain[1], repo_name: "" })).toBe("beta");
  });
  it("open no cockpit for a job the store no longer holds or cannot read", () => {
    expect(chipOpenable(order.chain[0])).toBe(true);
    expect(chipOpenable({ ...order.chain[0], state: MISSING_JOB_LABEL })).toBe(false);
    expect(chipOpenable({ ...order.chain[0], state: UNREADABLE_JOB_LABEL })).toBe(false);
  });
  it("count the orders not shown", () => {
    expect(earlierOrdersLine(0)).toBe("");
    expect(earlierOrdersLine(1)).toBe("1 earlier order is not shown.");
    expect(earlierOrdersLine(4)).toBe("4 earlier orders are not shown.");
  });
});
