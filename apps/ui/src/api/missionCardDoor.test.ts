// F305 T002, DECISION F305 D2 — the mission card's two doors: each reads the path its seam names
// through the fetcher it is given, decodes what comes back, and answers `null` rather than throw.
import { describe, expect, it } from "vitest";
import { loadMissionOrders, loadProjectMissions } from "./missionCardDoor";

const missions = {
  version: 1, project_id: "p-1", slug: "alpha", degraded: false, skipped_count: 0,
  missions: [{ mission_id: "m-1", goal: "Maintain alpha", status: "active", created_at: "", order_count: 0, job_count: 0 }],
};
const orders = {
  version: 1, project_id: "p-1", slug: "alpha", mission_id: "m-1", goal: "Maintain alpha",
  orders: [], earlier_orders: 0, degraded: false,
};

function recording(answer: unknown) {
  const paths: string[] = [];
  const fetcher = (path: string): Promise<unknown> => {
    paths.push(path);
    return Promise.resolve(answer);
  };
  return { paths, fetcher };
}

describe("loadProjectMissions", () => {
  it("reads the missions route and decodes its answer", async () => {
    const { paths, fetcher } = recording(missions);
    expect(await loadProjectMissions({ project: "alpha", token: "t" }, fetcher)).toEqual(missions);
    expect(paths).toEqual(["/api/projects/alpha/missions?token=t"]);
  });
  it("answers null for a failed read and for an answer it cannot decode", async () => {
    const failing = () => Promise.reject(new Error("Request failed 404"));
    expect(await loadProjectMissions({ project: "alpha", token: "t" }, failing)).toBeNull();
    expect(await loadProjectMissions({ project: "alpha", token: "t" }, recording({ error: "x" }).fetcher)).toBeNull();
  });
});

describe("loadMissionOrders", () => {
  it("reads one mission's orders route and decodes its answer", async () => {
    const { paths, fetcher } = recording(orders);
    expect(await loadMissionOrders({ project: "alpha", missionId: "m-1", token: "t" }, fetcher)).toEqual(orders);
    expect(paths).toEqual(["/api/projects/alpha/missions/m-1/orders?token=t"]);
  });
  it("answers null for a failed read and for an answer it cannot decode", async () => {
    const failing = () => Promise.reject(new Error("Request failed 404"));
    expect(await loadMissionOrders({ project: "alpha", missionId: "m-1", token: "t" }, failing)).toBeNull();
    expect(await loadMissionOrders({ project: "alpha", missionId: "m-1", token: "t" }, recording([]).fetcher)).toBeNull();
  });
});
